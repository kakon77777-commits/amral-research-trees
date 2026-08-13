"""Read-only regression check for v0.2.2 envelope classification ordering.

Exit 0 means the candidate classifies an envelope with an unsupported spec id
and missing required members as malformed/FAIL.  Exit 1 reproduces the frozen
v0.2.2 inconsistency (actual UNKNOWN).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    import pnp_glc_i0.semantic_validator_v022 as validator

    value = {
        "artifact_envelope": {
            "spec_id": "urn:unsupported:closure:9"
            # artifact_type, version, and edges are deliberately missing.
        }
    }
    with TemporaryDirectory() as directory:
        artifact = Path(directory) / "malformed-unsupported.json"
        artifact.write_text(json.dumps(value), encoding="utf-8")
        reference = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()
        result = validator._artifact_closure(
            {"run-spec": reference}, validator.ArtifactIndex(Path(directory))
        )

    conformant = result.status == validator.FAIL
    print(
        json.dumps(
            {
                "classification": "Counterexample to interface consistency",
                "expected_by_frozen_spec": validator.FAIL,
                "actual": result.status,
                "conformant": conformant,
                "admission_bypass": False,
                "note": "UNKNOWN is still admission-blocking; the defect is the required-member ordering contract.",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if conformant else 1


if __name__ == "__main__":
    raise SystemExit(main())
