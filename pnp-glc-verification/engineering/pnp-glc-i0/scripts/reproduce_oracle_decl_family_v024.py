"""Executable ORACLE-DECL-FAMILY-01 regression for v0.2.4.

The negative records retain valid trace signatures and correct family-selected
oracle execution, but carry a transplanted oracle declaration. Acceptance must
fail specifically at declaration/provenance binding. No P/NP claim is made.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


NEGATIVE_FIXTURES = (
    "parity-with-2sat-oracle-declaration",
    "2sat-with-parity-oracle-declaration",
    "2sat-sat-with-unsat-oracle-declaration",
    "2sat-unsat-with-sat-oracle-declaration",
    "parity-with-2sat-oracle-oracle_id-only",
    "parity-with-2sat-oracle-entrypoint-only",
    "parity-with-2sat-oracle-name-only",
    "parity-with-2sat-oracle-checks-only",
    "parity-with-2sat-oracle-obligations-only",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    import pnp_glc_i0.semantic_validator_v024 as validator

    fixtures = root / "fixtures-v0.2.4"
    schema = root / "schemas" / "run-record.schema.v0.2.4-candidate.json"
    store = validator.ArtifactIndex(root)
    probes: list[dict[str, object]] = []
    for name in NEGATIVE_FIXTURES:
        path = fixtures / f"{name}.json"
        record = validator.load_json(path)
        report = validator.validate_path(path, schema, root)
        codes = {issue.code for issue in report.issues}
        probe = {
            "name": name,
            "trace_authenticity": validator._trace_authenticity_status(
                record, store
            ),
            "actual_family_oracle_status": validator._independent_oracle_status(
                record
            ),
            "binding_issue_present": (
                "oracle-declaration-family-binding" in codes
            ),
            "record_accepted": report.record_accepted,
        }
        probe["conformant"] = (
            probe["trace_authenticity"] == validator.PASS
            and probe["actual_family_oracle_status"] == validator.PASS
            and probe["binding_issue_present"] is True
            and probe["record_accepted"] is False
        )
        probes.append(probe)

    positive_controls: dict[str, bool] = {}
    for name in ("legit", "2sat-sat", "2sat-unsat"):
        positive_controls[name] = validator.validate_path(
            fixtures / f"{name}.json", schema, root
        ).record_accepted
    unexpected = [probe["name"] for probe in probes if not probe["conformant"]]
    unexpected.extend(
        f"positive-control:{name}"
        for name, accepted in positive_controls.items()
        if not accepted
    )
    print(
        json.dumps(
            {
                "classification": "Experiment / declaration-provenance regression",
                "validator_version": validator.VALIDATOR_VERSION,
                "negative_probe_count": len(probes),
                "positive_control_count": len(positive_controls),
                "unexpected": unexpected,
                "all_conformant": not unexpected,
                "correctness_bypass_claim": False,
                "p_np_claim": False,
                "probes": probes,
                "positive_controls": positive_controls,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
