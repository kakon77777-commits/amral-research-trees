#!/usr/bin/env python3
"""Verify every manifest-covered file directly inside the packaged ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    zip_path = args.zip_path.resolve()
    report_path = args.report or zip_path.with_suffix(zip_path.suffix + ".verification.json")

    checks: dict[str, bool] = {}
    failures: list[dict[str, object]] = []
    with zipfile.ZipFile(zip_path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        checks["no_duplicate_entry_names"] = len(names) == len(set(names))
        checks["all_entry_paths_safe"] = all(
            not PurePosixPath(name).is_absolute()
            and ".." not in PurePosixPath(name).parts
            for name in names
        )
        manifest_names = [name for name in names if name.endswith("/ARTIFACT_MANIFEST.json")]
        checks["exactly_one_manifest"] = len(manifest_names) == 1
        if len(manifest_names) != 1:
            payload = {
                "status": "FAIL",
                "zip": str(zip_path),
                "checks": checks,
                "failures": [{"manifest_candidates": manifest_names}],
            }
            write_json(report_path, payload)
            print(json.dumps(payload, indent=2))
            return 1

        manifest_name = manifest_names[0]
        prefix = manifest_name[: -len("ARTIFACT_MANIFEST.json")]
        manifest = json.loads(archive.read(manifest_name).decode("utf-8"))
        expected_names = {prefix + entry["path"] for entry in manifest["files"]}
        expected_names.add(manifest_name)
        checks["entry_set_matches_manifest"] = set(names) == expected_names
        for entry in manifest["files"]:
            name = prefix + entry["path"]
            try:
                content = archive.read(name)
            except KeyError:
                failures.append({"path": entry["path"], "error": "missing"})
                continue
            actual = {"bytes": len(content), "sha256": sha256(content)}
            if actual["bytes"] != entry["bytes"] or actual["sha256"] != entry["sha256"]:
                failures.append(
                    {
                        "path": entry["path"],
                        "expected": {"bytes": entry["bytes"], "sha256": entry["sha256"]},
                        "actual": actual,
                    }
                )
        checks["all_manifest_hashes_match"] = not failures
        checks["zip_crc_test_passes"] = archive.testzip() is None
        checks["manifest_file_count_matches"] = manifest[
            "file_count_excluding_manifest"
        ] == len(manifest["files"])

    passed = all(checks.values())
    payload = {
        "schema_version": "1.0",
        "status": "PASS" if passed else "FAIL",
        "zip": str(zip_path),
        "zip_bytes": zip_path.stat().st_size,
        "zip_sha256": sha256(zip_path.read_bytes()),
        "entry_count": len(names),
        "manifest_covered_file_count": len(manifest["files"]),
        "checks": checks,
        "failures": failures,
    }
    write_json(report_path, payload)
    zip_path.with_suffix(zip_path.suffix + ".sha256").write_text(
        f"{payload['zip_sha256']}  {zip_path.name}\n", encoding="ascii", newline="\n"
    )
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
