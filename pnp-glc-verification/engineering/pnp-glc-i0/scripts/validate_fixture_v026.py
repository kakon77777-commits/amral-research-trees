"""Minimal manifest-bounded CLI for one frozen v0.2.6 fixture."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    parser.add_argument("fixture", nargs="?", default="legit")
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    from pnp_glc_i0 import semantic_validator_v026 as validator

    fixture = root / "fixtures-v0.2.6" / f"{args.fixture}.json"
    schema = root / "schemas" / "run-record.schema.v0.2.6-candidate.json"
    report = validator.validate_path(fixture, schema, root)
    payload = {
        "admission_pass": report.admission_pass,
        "final_completion": report.final_completion,
        "fixture": args.fixture,
        "issue_codes": sorted({issue.code for issue in report.issues}),
        "record_accepted": report.record_accepted,
        "semantic_ok": report.semantic_ok,
        "structural_ok": report.structural_ok,
        "validator_module": "src/pnp_glc_i0/semantic_validator_v026.py",
        "validator_version": validator.VALIDATOR_VERSION,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if report.record_accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
