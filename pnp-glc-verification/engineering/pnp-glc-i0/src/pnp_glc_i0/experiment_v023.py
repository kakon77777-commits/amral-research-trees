"""Reproducible bounded I0 v0.2.3 candidate experiment runner."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .experiment_v021 import run_i0 as run_v021
from .semantic_validator_v023 import (
    ArtifactIndex,
    _artifact_closure,
    _direct_receipt_reference_map,
    _operational_reference_status,
    _trace_authenticity_status,
    load_json,
    sha256_path,
    validate_path,
)


def _validation_summary(
    project_root: Path, schema: Path, fixture: Path
) -> dict[str, Any]:
    report = validate_path(fixture, schema, project_root)
    return {
        "structural_ok": report.structural_ok,
        "semantic_ok": report.semantic_ok,
        "admission_pass": report.admission_pass,
        "final_completion": report.final_completion,
        "record_accepted": report.record_accepted,
        "issue_codes": sorted({issue.code for issue in report.issues}),
    }


def run_i0(
    project_root: Path, *, seed: int = 20260809, max_parity_n: int = 12
) -> dict[str, Any]:
    report = run_v021(
        project_root, seed=seed, max_parity_n=max_parity_n
    )
    schema = project_root / "schemas" / "run-record.schema.v0.2.3-candidate.json"
    fixtures = project_root / "fixtures-v0.2.3"
    manifest = load_json(fixtures / "manifest.json")
    admission = {
        name: _validation_summary(project_root, schema, fixtures / f"{name}.json")
        for name in manifest["fixtures"]
    }

    store = ArtifactIndex(project_root)
    closure_case_root = (
        project_root / "artifacts-v0.2.3" / "closure-classification"
    )
    closure_case_manifest = load_json(closure_case_root / "manifest.json")
    closure_classification_reality_test: dict[str, Any] = {}
    for name, expected in closure_case_manifest["expected_status"].items():
        path = closure_case_root / f"{name}.json"
        actual = _artifact_closure(
            {"run-spec": "sha256:" + sha256_path(path)}, store
        ).status
        closure_classification_reality_test[name] = {
            "expected": expected,
            "actual": actual,
            "conformant": actual == expected,
        }
    ref_type: dict[str, Any] = {}
    for name in (
        "receipt-ref-substitution",
        "robust-ref-type-confusion",
        "cross-role-contract-invariant",
    ):
        record = load_json(fixtures / f"{name}.json")
        trace = store.load_json(record["validation_receipt"]["trace_sha256"])
        closure = _artifact_closure(
            _direct_receipt_reference_map(record), store
        )
        operational, operational_issues = _operational_reference_status(
            record, trace, store, closure
        )
        ref_type[name] = {
            "trace_authenticity": _trace_authenticity_status(record, store),
            "closure_status": closure.status,
            "operational_reference_status": operational,
            "operational_issue_codes": sorted(
                {issue.code for issue in operational_issues}
            ),
            "record_accepted": admission[name]["record_accepted"],
        }

    report.update(
        {
            "experiment_id": "I0-v0.2.3-candidate-20260809",
            "status": "Experiment candidate; pending independent acceptance",
            "admission": admission,
            "ref_type_reality_tests": ref_type,
            "trust_boundary": {
                "supported_interfaces": [
                    "ValidateBytes(recordBytes,schemaBytes,artifactSnapshot)",
                    "validate_path snapshots both input files then calls ValidateBytes",
                ],
                "private_helper": "_validate_parsed_record; no mapping plus claimed hash API",
                "schema_snapshot": "schema parse and SHA-256 derive from the same bytes",
                "artifact_snapshot": "ArtifactIndex hash/parse/use derives from one in-memory byte snapshot",
            },
            "raw_parse_domain": {
                "negative_zero": admission["negative-zero"],
                "unpaired_surrogate": admission["unpaired-surrogate"],
                "policy": "raw integer token -0 is rejected; all candidate keys and strings must be Unicode scalar NFC",
            },
            "closure_classification": [
                "Leaf: no envelope",
                "Malformed/FAIL: missing or ill-typed required member",
                "Unsupported/UNKNOWN: shape-valid unsupported spec_id",
                "Traverse: supported valid role-bearing envelope",
            ],
            "closure_classification_reality_test": {
                "classification": "Experiment / interface regression",
                "cases": closure_classification_reality_test,
                "all_conformant": all(
                    item["conformant"]
                    for item in closure_classification_reality_test.values()
                ),
                "admission_bypass_claim": False,
                "p_np_claim": False,
            },
            "candidate_scope": {
                "role_bearing_closure": True,
                "signed_operational_reference_map": True,
                "field_role_type_id_version_mode_binding": True,
                "family_bound_contract_oracle_rule_invariant": True,
                "gate_assignment_conformant_schema": True,
                "independent_acceptance": "pending",
            },
        }
    )
    report["prov_derive_reality_tests"] = {
        name: admission[name]
        for name in (
            "fabricated-states-999",
            "fabricated-transition-digest",
        )
    }
    for case in report["two_sat"]["cases"]:
        fixture_name = case["record_fixture"]
        record = load_json(fixtures / f"{fixture_name}.json")
        case["end_to_end_record_accepted"] = admission[fixture_name][
            "record_accepted"
        ]
        case["resource_ledger"] = record["ledger"]
    report["nonclaims"].extend(
        [
            "v0.2.3 candidate has not been independently accepted or promoted",
            "role/type checks do not constitute a proof of the research framework",
            "successful I0 experiments do not generalize to general SAT or P=NP",
        ]
    )
    return report


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--max-parity-n", type=int, default=12)
    args = parser.parse_args()
    report = run_i0(
        args.project_root.resolve(),
        seed=args.seed,
        max_parity_n=args.max_parity_n,
    )
    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
