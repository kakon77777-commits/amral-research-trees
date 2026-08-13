"""Deterministic, manifest-scoped I0 v0.2.6 experiment report."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any, Iterable

from .oracles import (
    assignment_satisfies_2sat,
    exhaustive_2sat,
    parity_oracle,
    verify_unsat_certificate,
)
from .parity import stream_parity, verify_prefix_invariant
from .semantic_validator_v026 import (
    ArtifactIndex,
    _advice_declaration_matches,
    _artifact_closure,
    _independent_oracle_status,
    _trace_authenticity_status,
    load_json,
    sha256_path,
    validate_path,
)
from .two_sat import solve_2sat


REPORT_VERSION = "0.2.6"
DEFAULT_SEED = 20260810
DEFAULT_TWO_SAT_SEED = 20260809
DEFAULT_VARIABLE_COUNTS = (1, 2, 3, 4, 5, 6)
DEFAULT_CASES_PER_VARIABLE_COUNT = 250


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


def _two_sat_crosscheck(
    *,
    seed: int = DEFAULT_TWO_SAT_SEED,
    variable_counts: Iterable[int] = DEFAULT_VARIABLE_COUNTS,
    cases_per_variable_count: int = DEFAULT_CASES_PER_VARIABLE_COUNT,
) -> dict[str, Any]:
    counts = tuple(variable_counts)
    rng = random.Random(seed)
    digest = hashlib.sha256()
    strata: list[dict[str, Any]] = []
    total = 0
    mismatch_total = 0
    certificate_failure_total = 0
    for variable_count in counts:
        literals = [
            literal
            for variable in range(1, variable_count + 1)
            for literal in (variable, -variable)
        ]
        sat_count = 0
        unsat_count = 0
        mismatches = 0
        certificate_failures = 0
        for case_index in range(cases_per_variable_count):
            clauses = [
                (rng.choice(literals), rng.choice(literals))
                for _ in range(rng.randrange(0, 3 * variable_count + 1))
            ]
            result = solve_2sat(variable_count, clauses)
            exhaustive = exhaustive_2sat(variable_count, clauses)
            expected_sat = exhaustive is not None
            actual_sat = result.status == "sat"
            if actual_sat:
                sat_count += 1
                certificate_pass = assignment_satisfies_2sat(
                    clauses, result.assignment or {}
                )
            else:
                unsat_count += 1
                certificate_pass = verify_unsat_certificate(
                    clauses,
                    result.unsat_variable or 0,
                    result.positive_to_negative,
                    result.negative_to_positive,
                )
            if actual_sat != expected_sat:
                mismatches += 1
            if not certificate_pass:
                certificate_failures += 1
            material = {
                "case_index": case_index,
                "certificate_pass": certificate_pass,
                "clauses": [list(clause) for clause in clauses],
                "exhaustive_status": "sat" if expected_sat else "unsat",
                "solver_status": result.status,
                "variable_count": variable_count,
            }
            digest.update(
                json.dumps(
                    material,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
                + b"\n"
            )
        total += cases_per_variable_count
        mismatch_total += mismatches
        certificate_failure_total += certificate_failures
        strata.append(
            {
                "cases": cases_per_variable_count,
                "certificate_failures": certificate_failures,
                "mismatches": mismatches,
                "sat": sat_count,
                "unsat": unsat_count,
                "variable_count": variable_count,
            }
        )
    return {
        "algorithm": "deterministic implication graph plus SCC",
        "all_pass": mismatch_total == 0 and certificate_failure_total == 0,
        "case_generation": (
            "one Random(seed) stream; variable_count ascending; each case has "
            "randrange(0,3*n+1) clauses and two choice(literals) draws per clause"
        ),
        "cases_per_variable_count": cases_per_variable_count,
        "certificate_failure_total": certificate_failure_total,
        "evidence_digest_sha256": digest.hexdigest().upper(),
        "mismatch_total": mismatch_total,
        "oracle": "exhaustive_2sat plus assignment/certificate verification",
        "seed": seed,
        "strata": strata,
        "total_cases": total,
        "variable_counts": list(counts),
    }


def run_i0(
    project_root: Path,
    *,
    seed: int = DEFAULT_SEED,
    two_sat_crosscheck_seed: int = DEFAULT_TWO_SAT_SEED,
    max_parity_n: int = 12,
) -> dict[str, Any]:
    project_root = project_root.resolve()
    schema = project_root / "schemas" / "run-record.schema.v0.2.6-candidate.json"
    fixtures = project_root / "fixtures-v0.2.6"
    artifacts = project_root / "artifacts-v0.2.6"
    fixture_manifest = load_json(fixtures / "manifest.json")
    admission = {
        name: _validation_summary(project_root, schema, fixtures / f"{name}.json")
        for name in fixture_manifest["fixtures"]
    }

    parity_rng = random.Random(seed)
    parity_cases: list[dict[str, Any]] = []
    for bit_count in range(max_parity_n + 1):
        bits = [parity_rng.randrange(2) for _ in range(bit_count)]
        result = stream_parity(bits)
        answer_pass = parity_oracle(bits, result.answer)
        invariant_pass = verify_prefix_invariant(bits, result)
        parity_cases.append(
            {
                "answer_pass": answer_pass,
                "bit_count": bit_count,
                "invariant_pass": invariant_pass,
            }
        )

    two_sat_representatives: list[dict[str, Any]] = []
    for fixture_name in ("2sat-sat", "2sat-unsat"):
        record = load_json(fixtures / f"{fixture_name}.json")
        parameters = record["problem"]["generator"]["parameters"]
        clauses = [tuple(clause) for clause in parameters["clauses"]]
        result = solve_2sat(parameters["variable_count"], clauses)
        oracle_pass = (
            assignment_satisfies_2sat(clauses, result.assignment or {})
            if result.status == "sat"
            else verify_unsat_certificate(
                clauses,
                result.unsat_variable or 0,
                result.positive_to_negative,
                result.negative_to_positive,
            )
        )
        two_sat_representatives.append(
            {
                "fixture": fixture_name,
                "oracle_pass": oracle_pass,
                "record_accepted": admission[fixture_name]["record_accepted"],
                "status": result.status,
            }
        )

    store = ArtifactIndex(project_root)
    closure_case_root = artifacts / "closure-classification"
    closure_manifest = load_json(closure_case_root / "manifest.json")
    closure_cases: dict[str, Any] = {}
    for name, expected in closure_manifest["expected_status"].items():
        path = closure_case_root / f"{name}.json"
        actual = _artifact_closure(
            {"run-spec": "sha256:" + sha256_path(path)}, store
        ).status
        closure_cases[name] = {
            "actual": actual,
            "conformant": actual == expected,
            "expected": expected,
        }
    closure_spec = load_json(artifacts / "artifact-closure-spec.v0.2.6.json")
    relation = closure_spec["judgments"]["SupportedEdgeRelation"]
    traversal = closure_spec["judgments"]["SupportedTraversal"]
    closure_totality = {
        "false_terminal_fail": (
            relation["false_result"]["terminal"] is True
            and relation["false_result"]["gate_result"] == "FAIL"
            and relation["false_result"]["traversal"] == "do not traverse"
        ),
        "true_unique_transition": (
            relation["true_result"]["terminal"] is False
            and relation["true_result"]["classification"] == "Traverse"
            and relation["true_result"]["next_transition"]
            == "judgments.SupportedTraversal"
        ),
        "fixed_point_terminal_trichotomy": (
            {item["gate_result"] for item in traversal["fixed_point_results"].values()}
            == {"PASS", "FAIL", "UNKNOWN"}
            and all(
                item["terminal"] is True
                for item in traversal["fixed_point_results"].values()
            )
        ),
    }

    advice_cases: dict[str, Any] = {}
    for name in (
        "advice-table-with-null-generator-zero-ledger",
        "advice-none-with-table-generator-ledger",
        "parity-stream-with-coherent-table-advice",
        "parity-table-with-coherent-none-advice",
    ):
        record = load_json(fixtures / f"{name}.json")
        trace = store.load_json(record["validation_receipt"]["trace_sha256"])
        advice_cases[name] = {
            "direct_advice_match": _advice_declaration_matches(record, trace),
            "record_accepted": admission[name]["record_accepted"],
            "structural_ok": admission[name]["structural_ok"],
            "trace_authenticity": _trace_authenticity_status(record, store),
        }

    oracle_cases: dict[str, Any] = {}
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
        oracle_cases[name] = {
            "actual_family_oracle_status": _independent_oracle_status(record),
            "record_accepted": admission[name]["record_accepted"],
        }

    crosscheck = _two_sat_crosscheck(seed=two_sat_crosscheck_seed)
    generation_command = (
        "python -I -B scripts/run_experiment_v026.py . --seed 20260810 "
        "--two-sat-crosscheck-seed 20260809 --max-parity-n 12 "
        "--output i0-run-report.v0.2.6-candidate.json"
    )
    return {
        "admission": admission,
        "advice_declaration_reality_tests": advice_cases,
        "candidate_scope": {
            "advice_decl_ledger_closed_bounded": True,
            "closure_judgment_dependency_closed": True,
            "closure_supported_relation_total": all(closure_totality.values()),
            "independent_acceptance": "pending",
            "manifest_runtime_closure": "tested separately in frozen isolation report",
        },
        "classification": "Experiment; no P/NP conclusion",
        "closure_classification_reality_test": {
            "all_conformant": all(item["conformant"] for item in closure_cases.values()),
            "cases": closure_cases,
        },
        "closure_supported_relation_totality": {
            "all_conformant": all(closure_totality.values()),
            "checks": closure_totality,
        },
        "experiment_id": "I0-v0.2.6-candidate-20260810",
        "frozen_evidence_scope": {
            "generation_command": generation_command,
            "report_location": "i0-run-report.v0.2.6-candidate.json",
            "two_sat_crosscheck_json_pointer": "/two_sat/deterministic_crosscheck",
            "two_sat_crosscheck_replay_command": (
                "python -I -B scripts/reproduce_live_report_scope_v026.py ."
            ),
        },
        "nonclaims": [
            "the candidate is unpromoted pending independent acceptance",
            "bounded experiments do not generalize to general SAT or P=NP",
            "a failed engineering gate would not imply P!=NP",
        ],
        "oracle_declaration_reality_tests": oracle_cases,
        "parameters": {
            "max_parity_n": max_parity_n,
            "seed": seed,
            "two_sat_crosscheck_seed": two_sat_crosscheck_seed,
        },
        "parity": {
            "all_pass": all(
                item["answer_pass"] and item["invariant_pass"]
                for item in parity_cases
            ),
            "cases": parity_cases,
        },
        "status": "CANDIDATE_UNPROMOTED / pending AI-1 managed bounded acceptance",
        "two_sat": {
            "deterministic_crosscheck": crosscheck,
            "representative_cases": two_sat_representatives,
        },
        "version": REPORT_VERSION,
    }


def render_report(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
