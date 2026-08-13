from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "SHA256SUMS-v0.2.2-candidate.txt"


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    if path == OUTPUT or "__pycache__" in path.parts or path.suffix == ".pyc":
        return False
    if relative in {
        "schemas/run-record.schema.v0.2.2-candidate.json",
        "src/pnp_glc_i0/semantic_validator_v022.py",
        "src/pnp_glc_i0/experiment_v022.py",
        "scripts/build_schema_v022.py",
        "scripts/generate_fixtures_v022.py",
        "scripts/reproduce_ref_type_v022.py",
        "scripts/make_checksums_v022.py",
        "tests_v022/test_semantic_validator_v022.py",
        "requirements-v0.2.2-candidate.txt",
        "i0-run-report.v0.2.2-candidate.json",
        "CURRENT-v0.2.2-candidate.md",
        "SCHEMA-DIFF-v0.2.1-to-v0.2.2.md",
        "REF-TYPE-01-REPRO-v0.2.2.md",
        "VALIDATION-REPORT-v0.2.2-candidate.md",
    }:
        return True
    return relative.startswith("fixtures-v0.2.2/") or relative.startswith(
        "artifacts-v0.2.2/"
    )


def main() -> None:
    paths = [
        path for path in ROOT.rglob("*") if path.is_file() and included(path)
    ]
    lines = []
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
