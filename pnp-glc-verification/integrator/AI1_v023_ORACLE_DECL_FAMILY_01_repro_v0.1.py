from __future__ import annotations

import argparse
import copy
import json
import sys
import types
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Local v0.2.3 oracle-declaration family conformance reproduction"
    )
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--signing-key", required=True, type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    sys.path.insert(0, str(root / "src"))
    sys.path.insert(0, str(root / "scripts"))

    # The frozen 121-path manifest includes generate_fixtures_v023.py but not
    # its legacy generator dependency chain. The two legacy functions are not
    # used by this reproduction, so provide an inert import-time placeholder.
    sys.modules["generate_fixtures_v021"] = types.ModuleType(
        "generate_fixtures_v021"
    )

    import generate_fixtures_v023 as gen
    from pnp_glc_i0.semantic_validator_v023 import (
        ArtifactIndex,
        _artifact_closure,
        _direct_receipt_reference_map,
        _independent_oracle_status,
        _trace_authenticity_status,
        validate_path,
    )

    fixture_name = "ai1-oracle-decl-family-01"
    schema_path = root / "schemas" / "run-record.schema.v0.2.3-candidate.json"
    base_path = root / "fixtures-v0.2.3" / "legit.json"
    other_path = root / "fixtures-v0.2.3" / "2sat-sat.json"

    base = json.loads(base_path.read_text(encoding="utf-8"))
    other = json.loads(other_path.read_text(encoding="utf-8"))
    initial_store = ArtifactIndex(root)
    trace = initial_store.load_json(base["validation_receipt"]["trace_sha256"])

    candidate, candidate_trace = gen.clone_candidate(base, trace, fixture_name)
    candidate["mechanism"]["oracle"] = copy.deepcopy(
        other["mechanism"]["oracle"]
    )
    private_key = gen.load_private_key(args.signing_key)
    gen.finalize_fixture(
        fixture_name,
        candidate,
        candidate_trace,
        private_key,
        sign_actual_operational_map=True,
    )

    record_path = root / "fixtures-v0.2.3" / f"{fixture_name}.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    final_store = ArtifactIndex(root)
    report = validate_path(record_path, schema_path, root)
    closure = _artifact_closure(
        _direct_receipt_reference_map(record), final_store
    )

    payload = {
        "fixture": str(record_path),
        "problem_family": record["problem"]["family"],
        "mechanism_id": record["mechanism"]["id"],
        "oracle_declaration": record["mechanism"]["oracle"],
        "trace_authenticity_status": _trace_authenticity_status(
            record, final_store
        ),
        "closure_status": closure.status,
        "independent_oracle_status": _independent_oracle_status(record),
        "validation": report.to_dict(),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
