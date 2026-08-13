"""Reproducible bounded I0 v0.2.4 candidate experiment runner."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .experiment_v021 import run_i0 as run_v021
from .semantic_validator_v024 import (
    ARTIFACT_CLOSURE_SPEC_ID,
    EDGE_RELATIONS,
    ArtifactIndex,
    _artifact_closure,
    _direct_receipt_reference_map,
    _independent_oracle_status,
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
    schema = project_root / "schemas" / "run-record.schema.v0.2.4-candidate.json"
    fixtures = project_root / "fixtures-v0.2.4"
    manifest = load_json(fixtures / "manifest.json")
    admission = {
        name: _validation_summary(project_root, schema, fixtures / f"{name}.json")
        for name in manifest["fixtures"]
    }

    store = ArtifactIndex(project_root)
    closure_case_root = (
        project_root / "artifacts-v0.2.4" / "closure-classification"
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
    closure_spec = load_json(
        project_root
        / "artifacts-v0.2.4"
        / "artifact-closure-spec.v0.2.4.json"
    )
    judgments = closure_spec["judgments"]
    generic = judgments["GenericEdgeShape"]
    supported_header = judgments["SupportedEnvelopeHeader"]
    supported_relation = judgments["SupportedEdgeRelation"]
    unsupported = judgments["UnsupportedEnvelope"]
    future_case = load_json(
        closure_case_root / "shape-valid-unsupported-future-type.json"
    )
    future_type = future_case["artifact_envelope"]["artifact_type"]
    closure_edge_scope_checks = {
        "normative_precedence_declared": bool(
            closure_spec.get("normative_precedence")
        ),
        "generic_relation_not_required": any(
            "EDGE_RELATIONS domain" in item
            for item in generic["does_not_require"]
        ),
        "supported_header_pins_spec_version_and_type_domain": (
            ARTIFACT_CLOSURE_SPEC_ID in supported_header["applicable_when"]
            and "0.2.4" in supported_header["predicate"]
            and "EDGE_RELATIONS domain" in supported_header["predicate"]
        ),
        "supported_relation_iff_supported_header": (
            supported_relation["applicable_iff"]
            == "judgments.SupportedEnvelopeHeader holds"
        ),
        "unsupported_relation_not_applicable": (
            "unsupported spec_id"
            in supported_relation["not_applicable_when"]
        ),
        "unsupported_result_unknown": unsupported["result"] == "UNKNOWN",
        "future_parent_has_no_current_relation": future_type not in EDGE_RELATIONS,
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
    oracle_declaration_reality_tests: dict[str, Any] = {}
    for name in (
        "parity-with-2sat-oracle-declaration",
        "2sat-with-parity-oracle-declaration",
        "2sat-sat-with-unsat-oracle-declaration",
        "2sat-unsat-with-sat-oracle-declaration",
        "parity-with-2sat-oracle-oracle_id-only",
        "parity-with-2sat-oracle-entrypoint-only",
        "parity-with-2sat-oracle-name-only",
        "parity-with-2sat-oracle-checks-only",
        "parity-with-2sat-oracle-obligations-only",
    ):
        record = load_json(fixtures / f"{name}.json")
        oracle_declaration_reality_tests[name] = {
            "actual_family_oracle_status": _independent_oracle_status(record),
            "record_accepted": admission[name]["record_accepted"],
            "issue_codes": admission[name]["issue_codes"],
        }

    report.update(
        {
            "experiment_id": "I0-v0.2.4-candidate-20260809",
            "status": "Experiment candidate; pending independent acceptance",
            "admission": admission,
            "ref_type_reality_tests": ref_type,
            "oracle_declaration_reality_tests": oracle_declaration_reality_tests,
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
            "closure_edge_scope_reality_test": {
                "classification": "Definition/interface conformance checks",
                "checks": closure_edge_scope_checks,
                "all_conformant": all(closure_edge_scope_checks.values()),
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
            "v0.2.4 candidate has not been independently accepted or promoted",
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
