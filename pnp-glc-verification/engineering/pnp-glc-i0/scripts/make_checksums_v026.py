from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "SHA256SUMS-v0.2.6-candidate.txt"
RUNTIME_DESCRIPTOR = (
    ROOT
    / "artifacts-v0.2.6"
    / "acceptance-runtime-closure.v0.2.6.json"
)
PACKET_PATHS = {
    "ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01-REPRO-v0.2.6.md",
    "CLOSURE-SUPPORTED-RELATION-RESULT-01-REPRO-v0.2.6.md",
    "CURRENT-v0.2.6-candidate.md",
    "FROZEN-LIVE-REPORT-SCOPE-01-REPRO-v0.2.6.md",
    "SCHEMA-DIFF-v0.2.5-to-v0.2.6.md",
    "VALIDATION-REPORT-v0.2.6-candidate.md",
    "runtime-isolation-report.v0.2.6.json",
}


def main() -> None:
    descriptor = json.loads(RUNTIME_DESCRIPTOR.read_text(encoding="utf-8"))
    included = set(descriptor["required_paths"]) | PACKET_PATHS
    missing = sorted(path for path in included if not (ROOT / path).is_file())
    if missing:
        raise FileNotFoundError(f"manifest inputs missing: {missing}")

    candidate_named = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
        and (
            "v0.2.6" in path.relative_to(ROOT).as_posix()
            or "v026" in path.relative_to(ROOT).as_posix()
        )
        and path != OUTPUT
    }
    omitted = sorted(candidate_named - included)
    if omitted:
        raise RuntimeError(f"v0.2.6 files omitted from manifest: {omitted}")

    lines = []
    for relative in sorted(included):
        path = ROOT / relative
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        lines.append(f"{digest}  {relative}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
