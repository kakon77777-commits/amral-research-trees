#!/usr/bin/env python3
"""Build a deterministic manifest and ZIP for the v0.5 artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


FIXED_ZIP_TIME = (2026, 8, 12, 0, 0, 0)
MANIFEST_NAME = "ARTIFACT_MANIFEST.json"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return (
        path.is_file()
        and MANIFEST_NAME not in relative.parts
        and "__pycache__" not in relative.parts
        and path.suffix.lower() not in {".pyc", ".pyo"}
    )


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output or root.parent / f"{root.name}.zip").resolve()
    if output == root or root in output.parents:
        raise ValueError("ZIP output must be outside the artifact root")

    files = sorted(
        (path for path in root.rglob("*") if included(path, root)),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    entries = []
    for path in files:
        content = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(content),
                "sha256": sha256_bytes(content),
            }
        )
    manifest = {
        "schema_version": "1.0",
        "artifact": root.name,
        "created_date": "2026-08-12",
        "hash_algorithm": "SHA256",
        "manifest_self_excluded_from_hash_list": True,
        "excluded_patterns": ["**/__pycache__/**", "**/*.pyc", "**/*.pyo"],
        "file_count_excluding_manifest": len(entries),
        "total_bytes_excluding_manifest": sum(entry["bytes"] for entry in entries),
        "files": entries,
    }
    manifest_path = root / MANIFEST_NAME
    write_json(manifest_path, manifest)

    packaged_files = [*files, manifest_path]
    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        allowZip64=True,
    ) as archive:
        for path in packaged_files:
            relative = PurePosixPath(root.name) / PurePosixPath(
                path.relative_to(root).as_posix()
            )
            info = zipfile.ZipInfo(str(relative), date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, path.read_bytes(), compresslevel=9)

    payload = {
        "status": "BUILT",
        "zip": str(output),
        "zip_bytes": output.stat().st_size,
        "zip_sha256": sha256_bytes(output.read_bytes()),
        "entries": len(packaged_files),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
