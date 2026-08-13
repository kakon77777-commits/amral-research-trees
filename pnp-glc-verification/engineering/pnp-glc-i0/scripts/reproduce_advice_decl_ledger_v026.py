"""Targeted ADVICE-DECL-LEDGER-01 regression for frozen-candidate v0.2.6.

The probes distinguish internal schema contradictions from schema-valid records
whose typed advice mode disagrees with the validator-derived mechanism context.
They are bounded record-consistency experiments and make no P/NP claim.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    import pnp_glc_i0.semantic_validator_v026 as validator

    schema = root / "schemas" / "run-record.schema.v0.2.6-candidate.json"
    store = validator.ArtifactIndex(root)
    negative_expectations = {
        "advice-table-with-null-generator-zero-ledger": False,
        "advice-none-with-table-generator-ledger": False,
        "parity-stream-with-coherent-table-advice": True,
        "parity-table-with-coherent-none-advice": True,
    }
    probes: list[dict[str, object]] = []
    for name, expected_structural in negative_expectations.items():
        path = root / "fixtures-v0.2.6" / f"{name}.json"
        record = validator.load_json(path)
        trace = store.load_json(record["validation_receipt"]["trace_sha256"])
        report = validator.validate_path(path, schema, root)
        binding_issue = any(
            issue.code == "advice-declaration-ledger-binding"
            for issue in report.issues
        )
        direct_match = validator._advice_declaration_matches(record, trace)
        conformant = (
            report.structural_ok is expected_structural
            and validator._trace_authenticity_status(record, store)
            == validator.PASS
            and not direct_match
            and not report.record_accepted
            and (binding_issue if expected_structural else True)
        )
        probes.append(
            {
                "name": name,
                "expected_structural": expected_structural,
                "structural_ok": report.structural_ok,
                "binding_issue_present": binding_issue,
                "direct_advice_match": direct_match,
                "record_accepted": report.record_accepted,
                "conformant": conformant,
            }
        )

    positive_controls: dict[str, bool] = {}
    for name in ("legit", "2sat-sat", "2sat-unsat"):
        path = root / "fixtures-v0.2.6" / f"{name}.json"
        record = validator.load_json(path)
        trace = store.load_json(record["validation_receipt"]["trace_sha256"])
        report = validator.validate_path(path, schema, root)
        positive_controls[name] = (
            record["mechanism"]["admissibility"]["advice_mode"] == "none"
            and validator._advice_declaration_matches(record, trace)
            and report.record_accepted
        )

    cheat_path = root / "fixtures-v0.2.6" / "cheat.json"
    cheat = validator.load_json(cheat_path)
    cheat_trace = store.load_json(cheat["validation_receipt"]["trace_sha256"])
    table_binding_control = (
        cheat["mechanism"]["admissibility"]["advice_mode"]
        == "per-input-length-truth-table"
        and validator._advice_declaration_matches(cheat, cheat_trace)
        and not validator.validate_path(cheat_path, schema, root).record_accepted
    )

    unexpected = [probe["name"] for probe in probes if not probe["conformant"]]
    unexpected.extend(
        name for name, conformant in positive_controls.items() if not conformant
    )
    if not table_binding_control:
        unexpected.append("table-binding-control")
    print(
        json.dumps(
            {
                "classification": "Experiment / declaration-ledger regression",
                "validator_version": validator.VALIDATOR_VERSION,
                "negative_probe_count": len(probes),
                "positive_control_count": len(positive_controls),
                "table_binding_control": table_binding_control,
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
