from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pnp_glc_i0.semantic_validator_v022 import (  # noqa: E402
    ArtifactIndex,
    _artifact_closure,
    _direct_receipt_reference_map,
    _operational_reference_status,
    _trace_authenticity_status,
    load_json,
    validate_path,
)


def main() -> int:
    schema = ROOT / "schemas" / "run-record.schema.v0.2.2-candidate.json"
    fixture_root = ROOT / "fixtures-v0.2.2"
    store = ArtifactIndex(ROOT)
    cases = {}
    ok = True
    for name in (
        "receipt-ref-substitution",
        "robust-ref-type-confusion",
        "cross-role-contract-invariant",
    ):
        path = fixture_root / f"{name}.json"
        record = load_json(path)
        trace = store.load_json(record["validation_receipt"]["trace_sha256"])
        closure = _artifact_closure(
            _direct_receipt_reference_map(record), store
        )
        operational, operational_issues = _operational_reference_status(
            record, trace, store, closure
        )
        report = validate_path(path, schema, ROOT)
        cases[name] = {
            "signature_status": _trace_authenticity_status(record, store),
            "closure_status": closure.status,
            "operational_reference_status": operational,
            "operational_issue_codes": sorted(
                {issue.code for issue in operational_issues}
            ),
            "semantic_ok": report.semantic_ok,
            "record_accepted": report.record_accepted,
        }
        ok = ok and cases[name]["signature_status"] == "pass"
        ok = ok and operational == "fail" and not report.record_accepted
    payload = {
        "status": "Experiment",
        "expected": "all valid-signature REF-TYPE attacks are rejected",
        "cases": cases,
        "all_expected": ok,
        "nonclaim": "no P/NP implication",
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
