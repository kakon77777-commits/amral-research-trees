from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Local valid-signature v0.2.4 advice declaration/ledger check"
    )
    parser.add_argument("candidate_root", type=Path)
    parser.add_argument("--signing-key", required=True, type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))
    sys.path.insert(0, str(root / "scripts"))

    import generate_fixtures_v024 as generator
    from pnp_glc_i0.semantic_validator_v024 import (
        ArtifactIndex,
        _artifact_closure,
        _direct_receipt_reference_map,
        _independent_oracle_status,
        _trace_authenticity_status,
        validate_path,
    )

    name = "ai1-advice-decl-ledger-01"
    base = json.loads(
        (root / "fixtures-v0.2.4" / "legit.json").read_text(
            encoding="utf-8"
        )
    )
    initial_store = ArtifactIndex(root)
    trace = initial_store.load_json(
        base["validation_receipt"]["trace_sha256"]
    )
    record, cloned_trace = generator.clone_candidate(base, trace, name)
    record["mechanism"]["admissibility"]["advice"] = (
        "one truth table per n"
    )
    private_key = generator.load_private_key(args.signing_key)
    generator.finalize_fixture(
        name,
        record,
        cloned_trace,
        private_key,
        sign_actual_operational_map=True,
    )

    record_path = root / "fixtures-v0.2.4" / f"{name}.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    store = ArtifactIndex(root)
    report = validate_path(
        record_path,
        root / "schemas" / "run-record.schema.v0.2.4-candidate.json",
        root,
    )
    admissibility = record["mechanism"]["admissibility"]
    ledger = record["ledger"]
    output = {
        "classification": "Accepted-record declaration/ledger conformance",
        "advice_declaration": admissibility["advice"],
        "uniform": admissibility["uniform"],
        "program_quantifiers": admissibility["program_quantifiers"],
        "advice_generator_ref": admissibility["advice_generator_ref"],
        "declared_answer_access": admissibility["declared_answer_access"],
        "ledger_advice_bytes": ledger["description_bytes"]["advice"],
        "ledger_generated_tables": ledger["description_bytes"][
            "generated_tables"
        ],
        "advice_generation_account": ledger["admission_costs"][
            "advice_generation"
        ],
        "trace_authenticity": _trace_authenticity_status(record, store),
        "closure": _artifact_closure(
            _direct_receipt_reference_map(record), store
        ).status,
        "actual_family_oracle": _independent_oracle_status(record),
        "validation": report.to_dict(),
        "correctness_bypass_claim": False,
        "p_np_claim": False,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    contradiction_accepted = (
        report.record_accepted
        and admissibility["advice"] != "none"
        and admissibility["advice_generator_ref"] is None
        and ledger["description_bytes"]["advice"] == 0
        and ledger["description_bytes"]["generated_tables"] == 0
    )
    return 1 if contradiction_accepted else 0


if __name__ == "__main__":
    raise SystemExit(main())
