from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from pnp_glc_i0.semantic_validator import (  # noqa: E402
    GATE_VERSION,
    PROJECTION_SPEC_ID,
    TRACE_PRODUCER,
    candidate_projection_sha256,
    canonical_json_bytes,
    sha256_bytes,
    sha256_path,
)
from pnp_glc_i0.parity import stream_parity  # noqa: E402


SCHEMA = ROOT / "schemas" / "run-record.schema.v0.2.0-candidate.json"
FIXTURES = ROOT / "fixtures"
TRACES = ROOT / "artifacts" / "traces"
VALIDATOR = ROOT / "src" / "pnp_glc_i0" / "semantic_validator.py"
PARITY = ROOT / "src" / "pnp_glc_i0" / "parity.py"
ORACLES = ROOT / "src" / "pnp_glc_i0" / "oracles.py"
PROJECTION_SPEC = ROOT / "artifacts" / "candidate-projection-spec.v0.2.0.json"
SANDBOX = ROOT / "artifacts" / "sandbox-policy.v0.2.0.json"
RUN_STANDARD = ROOT / "artifacts" / "run-standard.v0.2.0.json"
RUN_ROBUST = ROOT / "artifacts" / "run-robust.v0.2.0.json"
MAXIMAL = ROOT / "artifacts" / "maximal-run.v0.2.0.json"
FAIRNESS = ROOT / "artifacts" / "fairness.v0.2.0.json"
INVARIANT = ROOT / "artifacts" / "parity-invariant.v0.2.0.md"
CONTRACT = ROOT / "artifacts" / "contract-parity.v0.2.0.json"

TIME_KEYS = (
    "construction",
    "generation",
    "update",
    "decode",
    "lift",
    "verify",
    "recovery",
    "restart",
    "parallel_work",
    "oracle",
    "total",
)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def hash_ref(path: Path) -> str:
    return f"sha256:{sha256_path(path)}"


def costs(**values: int) -> dict[str, int]:
    result = {key: int(values.get(key, 0)) for key in TIME_KEYS if key != "total"}
    result["total"] = sum(result.values())
    return result


def sum_costs(events: list[dict[str, Any]]) -> dict[str, int]:
    return {
        key: sum(event["time_ns"][key] for event in events)
        for key in TIME_KEYS
    }


def build_candidate(
    run_id: str,
    *,
    cheat: bool,
    robust: bool,
    resource_bounded: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    bits = (1, 0, 1, 1)
    answer = stream_parity(bits).answer
    parity_ref = hash_ref(PARITY)
    oracle_ref = hash_ref(ORACLES)
    invariant_ref = None if cheat else hash_ref(INVARIANT)
    certificate_refs = [] if cheat else [hash_ref(INVARIANT)]
    input_hash = f"sha256:{sha256_bytes(canonical_json_bytes({'bits': list(bits)}))}"

    candidate_result = {
        "status": "complete",
        "answer": answer,
        "certificate_refs": certificate_refs,
        "notes": "Experiment only; no P/NP conclusion.",
    }
    result_hash = f"sha256:{sha256_bytes(canonical_json_bytes(candidate_result))}"
    intermediate_hash = f"sha256:{sha256_bytes(canonical_json_bytes({'state': [4, answer]}))}"

    first_cost = (
        costs(construction=11, generation=101, update=17)
        if cheat
        else costs(construction=11, update=17)
    )
    second_cost = costs(decode=7, verify=13)
    events = [
        {
            "seq": 0,
            "kind": "solve",
            "from_state": "start",
            "to_state": "computed",
            "representation_before": "bit-vector",
            "representation_after": "parity-state",
            "input_sha256": input_hash,
            "output_sha256": intermediate_hash,
            "transition_rule_ref": parity_ref,
            "invariant_ref": invariant_ref,
            "time_ns": first_cost,
            "debt_added": [],
            "debt_retired": [],
            "status": "ok",
            "failure": None,
        },
        {
            "seq": 1,
            "kind": "stop",
            "from_state": "computed",
            "to_state": "terminal",
            "representation_before": "parity-state",
            "representation_after": "answer-bit",
            "input_sha256": intermediate_hash,
            "output_sha256": result_hash,
            "transition_rule_ref": parity_ref,
            "invariant_ref": invariant_ref,
            "time_ns": second_cost,
            "debt_added": [],
            "debt_retired": [],
            "status": "ok",
            "failure": None,
        },
    ]
    description = {
        "program_code": PARITY.stat().st_size,
        "advice": 16 if cheat else 0,
        "builder_artifacts": PARITY.stat().st_size,
        "generated_tables": 16 if cheat else 0,
        "proof": 0 if cheat else INVARIANT.stat().st_size,
    }
    admission_costs = {
        "builder": {
            "time_ns": 11,
            "peak_space_bytes": 256,
            "peak_output_bytes": PARITY.stat().st_size,
        },
        "advice_generation": {
            "time_ns": 101 if cheat else 0,
            "peak_space_bytes": 16 if cheat else 0,
            "peak_output_bytes": 16 if cheat else 0,
        },
        "proof_verification": {
            "time_ns": 13 if not cheat else 0,
            "peak_space_bytes": 512 if not cheat else 0,
            "peak_output_bytes": 0,
        },
    }
    ledger = {
        "time_ns": sum_costs(events),
        "space_bytes": {"peak": 1024, "final": 1, "artifacts": sum(description.values())},
        "description_bytes": description,
        "admission_costs": admission_costs,
        "precision": {"model": "finite exact bit/integer", "peak_bits": 64},
        "counts": {
            "states": 3,
            "branches": 1,
            "switches": 0,
            "rollbacks": 0,
            "reroutes": 0,
            "refinements": 0,
            "restarts": 0,
            "parallel_workers_peak": 1,
        },
        "semantic_loss_debt": {
            "registered": [],
            "peak_open": 0,
            "outstanding": 0,
        },
        "resource_account_complete": True,
    }
    record: dict[str, Any] = {
        "schema_version": "0.2.0",
        "run_id": run_id,
        "recorded_at": "2026-08-09T06:00:00Z",
        "track": "algorithm",
        "ctcl": {
            "instant": "ctcl:instant:b8ce3d5a-9369-4c60-8436-737ecd818ac7",
            "role": "coordination-only",
        },
        "experiment": {
            "id": "PARITY-0-cheat" if cheat else "PARITY-0-legit",
            "phase": "I0",
            "status": "completed",
            "hypothesis_id": "terminal-only-is-insufficient",
            "seed": 0,
            "series_semantics": "pointwise-envelope" if cheat else "fixed-program-scaling",
            "pre_registered_metrics": [
                "admission_pass",
                "construction",
                "generation",
                "advice_bytes",
            ],
        },
        "provenance": {
            "sources": [
                {
                    "id": "run-record-v0.2-candidate",
                    "kind": "implementation",
                    "locator": "schemas/run-record.schema.v0.2.0-candidate.json",
                    "version": "0.2.0-candidate",
                    "sha256": hash_ref(SCHEMA),
                    "applicable_domain": "I0 engineering records",
                    "accessed_at": "2026-08-09T06:00:00Z",
                    "visibility": "shared",
                }
            ],
            "implementation": {
                "name": "pnp-glc-i0",
                "version": "0.2.0",
                "revision": "candidate",
                "dirty": False,
                "runtime": "CPython >=3.11",
                "dependencies": [{"name": "jsonschema", "version": ">=4.20"}],
            },
        },
        "claims": [
            {
                "id": "PARITY-0",
                "label": "Experiment",
                "statement": "Terminal-only parity reports do not establish uniform provenance.",
                "status": "active",
                "source_refs": ["run-record-v0.2-candidate"],
                "domain": "bounded materialized I0 fixtures",
                "quantifiers": [
                    "legit: exists one program for all input lengths",
                    "cheat: for all lengths exists a program",
                ],
                "assumptions": ["trusted external trace producer"],
                "failure_conditions": [
                    "unresolved evidence",
                    "nonuniform quantifier",
                    "answer access",
                ],
            }
        ],
        "problem": {
            "family": "PARITY",
            "instance_id": f"parity-n{len(bits)}",
            "input_sha256": input_hash,
            "generator": {
                "name": "fixed-fixture",
                "version": "0.2.0",
                "seed": 0,
                "parameters": {"bits": list(bits)},
            },
            "size": {"n": len(bits)},
            "contract": {
                "id": "I0-PARITY",
                "version": "0.2.0",
                "sha256": hash_ref(CONTRACT),
                "completion_requirements": [
                    "correct parity",
                    "verified trace",
                    "zero outstanding debt",
                ],
            },
        },
        "mechanism": {
            "id": "parity-table-family" if cheat else "parity-stream",
            "name": "Per-length truth table" if cheat else "Uniform streaming PARITY",
            "version": "0.2.0",
            "role": "candidate" if cheat else "baseline",
            "resource_regime": (
                "resource-bounded" if resource_bounded else "resource-neutral"
            ),
            "run_quantifier": "robust" if robust else "standard",
            "baseline_id": None if not cheat else "parity-stream",
            "operations": ["build", "step", "decode", "verify"],
            "admissibility": {
                "uniform": not cheat,
                "oracle_free": True,
                "finite_precision": True,
                "program_quantifiers": (
                    "for-all-lengths-exists-program"
                    if cheat
                    else "exists-one-program-for-all-input-lengths"
                ),
                "builder_ref": parity_ref,
                "step_ref": parity_ref,
                "decode_ref": parity_ref,
                "declared_answer_access": "truth-table" if cheat else "none",
                "advice_generator_ref": parity_ref if cheat else None,
                "local_invariant_ref": invariant_ref,
                "randomness": "none",
                "interaction": "none",
                "advice": "one truth table per n" if cheat else "none",
                "parallelism": "single worker",
                "hardware": "abstract deterministic machine",
            },
            "oracle": {
                "name": "independent parity oracle",
                "version": "0.2.0",
                "independent": True,
                "checks": ["answer", "prefix invariant" if not cheat else "answer"],
                "sha256": oracle_ref,
            },
        },
        "ledger": ledger,
        "events": events,
        "candidate_result": candidate_result,
        "failure_frontier": {
            "axes": [
                {"name": "n", "value": len(bits), "unit": "bits"},
                {
                    "name": "advice",
                    "value": description["advice"],
                    "unit": "bytes",
                },
            ],
            "first_observed_failure": (
                "nonuniform/advice/answer-access admission gates" if cheat else None
            ),
            "censored": False,
            "interpretation": "Experiment only; no P=NP or P!=NP inference.",
        },
    }

    trace = {
        "trace_version": "0.2.0",
        "producer": TRACE_PRODUCER,
        "run_id": run_id,
        "gate_version": GATE_VERSION,
        "projection_spec_id": PROJECTION_SPEC_ID,
        "candidate_projection_sha256": candidate_projection_sha256(record),
        "answer_access": "truth-table" if cheat else "none",
        "candidate_output": candidate_result,
        "certificate_refs": certificate_refs,
        "events": events,
        "resource_samples": {
            key: ledger[key]
            for key in (
                "space_bytes",
                "description_bytes",
                "admission_costs",
                "precision",
                "counts",
            )
        },
        "gate_evidence": {
            "provenance_pass": True,
            "builder_execution_pass": True,
            "advice_generation_pass": True,
            "proof_verification_pass": not cheat,
            "advice_budget_pass": not cheat,
            "resource_budget_pass": True if resource_bounded else "unknown",
            "run_class_nonempty": True,
            "maximality_pass": True if robust else "unknown",
            "fairness_pass": True if robust else "unknown",
            "oracle_pass": True,
            "contract_pass": True,
            "complete_pass": True,
            "budget_pass": True if resource_bounded else "unknown",
        },
    }
    return record, trace


def attach_receipt(
    record: dict[str, Any],
    trace_path: Path,
    *,
    cheat: bool,
    robust: bool,
    resource_bounded: bool,
) -> None:
    trace_ref = hash_ref(trace_path)
    parity_ref = hash_ref(PARITY)
    invariant_ref = None if cheat else hash_ref(INVARIANT)
    gates = {
        "uniformity_pass": "fail" if cheat else "pass",
        "provenance_pass": "pass",
        "refs_resolved_pass": "pass",
        "builder_execution_pass": "pass",
        "advice_generation_pass": "pass" if cheat else "not-applicable",
        "proof_verification_pass": "not-applicable" if cheat else "pass",
        "advice_budget_pass": "fail" if cheat else "pass",
        "answer_access_pass": "fail" if cheat else "pass",
        "resource_budget_pass": "pass" if resource_bounded else "not-applicable",
        "resource_account_pass": "pass",
        "oracle_free_pass": "fail" if cheat else "pass",
        "replay_pass": "pass",
        "run_class_nonempty": "pass",
        "maximality_pass": "pass" if robust else "not-applicable",
        "fairness_pass": "pass" if robust else "not-applicable",
    }
    maximal_ref = hash_ref(MAXIMAL) if robust else None
    fairness_ref = hash_ref(FAIRNESS) if robust else None
    references = {
        hash_ref(SCHEMA),
        hash_ref(VALIDATOR),
        hash_ref(PROJECTION_SPEC),
        hash_ref(SANDBOX),
        hash_ref(RUN_ROBUST if robust else RUN_STANDARD),
        trace_ref,
        parity_ref,
        hash_ref(ORACLES),
        hash_ref(CONTRACT),
    }
    if invariant_ref:
        references.add(invariant_ref)
    if maximal_ref:
        references.add(maximal_ref)
    if fairness_ref:
        references.add(fairness_ref)

    record["validation_receipt"] = {
        "receipt_version": "0.2.0",
        "decision_source": "external-validator",
        "gate_version": GATE_VERSION,
        "schema_sha256": hash_ref(SCHEMA),
        "validator_sha256": hash_ref(VALIDATOR),
        "validator_independent": True,
        "projection_spec_id": PROJECTION_SPEC_ID,
        "projection_spec_sha256": hash_ref(PROJECTION_SPEC),
        "candidate_projection_sha256": candidate_projection_sha256(record),
        "capability_sandbox_ref": hash_ref(SANDBOX),
        "run_spec_ref": hash_ref(RUN_ROBUST if robust else RUN_STANDARD),
        "maximal_run_spec_ref": maximal_ref,
        "fairness_spec_ref": fairness_ref,
        "trace_sha256": trace_ref,
        "resolved_evidence_hashes": sorted(references),
        "observed_answer_access": "truth-table" if cheat else "none",
        "gates": gates,
        "admission_pass": not cheat,
        "correctness": {
            "oracle_pass": "pass",
            "contract_pass": "pass",
            "complete_pass": "pass",
            "budget_pass": "pass" if resource_bounded else "not-applicable",
            "outstanding_loss_debt": 0,
        },
        "final_completion": not cheat,
        "reasons": (
            [
                "nonuniform quantifier",
                "truth-table answer access",
                "advice budget exceeded",
            ]
            if cheat
            else []
        ),
    }


def generate_valid_fixture(
    name: str,
    *,
    cheat: bool = False,
    robust: bool = False,
    resource_bounded: bool = True,
) -> dict[str, Any]:
    record, trace = build_candidate(
        name,
        cheat=cheat,
        robust=robust,
        resource_bounded=resource_bounded,
    )
    trace_path = TRACES / f"{name}.trace.json"
    write_json(trace_path, trace)
    attach_receipt(
        record,
        trace_path,
        cheat=cheat,
        robust=robust,
        resource_bounded=resource_bounded,
    )
    write_json(FIXTURES / f"{name}.json", record)
    return record


def main() -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    TRACES.mkdir(parents=True, exist_ok=True)

    legit = generate_valid_fixture("legit", cheat=False, robust=False)
    cheat = generate_valid_fixture("cheat", cheat=True, robust=False)
    robust_legit = generate_valid_fixture("robust-legit", cheat=False, robust=True)
    neutral_legit = generate_valid_fixture(
        "neutral-legit", cheat=False, robust=False, resource_bounded=False
    )
    robust_neutral_legit = generate_valid_fixture(
        "robust-neutral-legit", cheat=False, robust=True, resource_bounded=False
    )

    unknown_gate, unknown_trace = build_candidate(
        "unknown-gate", cheat=False, robust=False, resource_bounded=True
    )
    unknown_trace["gate_evidence"]["provenance_pass"] = "unknown"
    unknown_trace_path = TRACES / "unknown-gate.trace.json"
    write_json(unknown_trace_path, unknown_trace)
    attach_receipt(
        unknown_gate,
        unknown_trace_path,
        cheat=False,
        robust=False,
        resource_bounded=True,
    )
    unknown_gate["validation_receipt"]["gates"]["provenance_pass"] = "unknown"
    unknown_gate["validation_receipt"]["admission_pass"] = False
    unknown_gate["validation_receipt"]["final_completion"] = False
    unknown_gate["validation_receipt"]["reasons"] = [
        "provenance evidence is incomplete"
    ]
    write_json(FIXTURES / "unknown-gate.json", unknown_gate)

    negative: dict[str, dict[str, Any]] = {}

    item = copy.deepcopy(legit)
    item["candidate_result"]["admission_pass"] = True
    negative["self-report"] = item

    item = copy.deepcopy(robust_legit)
    item["validation_receipt"]["maximal_run_spec_ref"] = None
    item["validation_receipt"]["fairness_spec_ref"] = None
    negative["robust-null-spec"] = item

    item = copy.deepcopy(legit)
    item["validation_receipt"]["gates"]["uniformity_pass"] = "fail"
    item["validation_receipt"]["gates"]["provenance_pass"] = "fail"
    item["validation_receipt"]["admission_pass"] = True
    negative["failed-gate-admission"] = item

    item = copy.deepcopy(legit)
    item["validation_receipt"]["correctness"].update(
        {
            "oracle_pass": "fail",
            "contract_pass": "fail",
            "complete_pass": "fail",
            "budget_pass": "fail",
            "outstanding_loss_debt": 1,
        }
    )
    item["validation_receipt"]["gates"]["resource_account_pass"] = "fail"
    item["ledger"]["resource_account_complete"] = False
    item["ledger"]["semantic_loss_debt"]["outstanding"] = 1
    item["validation_receipt"]["final_completion"] = True
    negative["false-final-completion"] = item

    item = copy.deepcopy(legit)
    item["candidate_result"]["status"] = "unknown"
    item["validation_receipt"]["final_completion"] = True
    negative["unknown-final"] = item

    item = copy.deepcopy(legit)
    item["candidate_result"]["answer"] ^= 1
    negative["tampered-record"] = item

    legit_trace = json.loads((TRACES / "legit.trace.json").read_text(encoding="utf-8"))
    tampered_trace = copy.deepcopy(legit_trace)
    tampered_trace["candidate_output"]["answer"] ^= 1
    tampered_trace_path = TRACES / "tampered-trace.trace.json"
    write_json(tampered_trace_path, tampered_trace)
    item = copy.deepcopy(legit)
    old_trace = item["validation_receipt"]["trace_sha256"]
    new_trace = hash_ref(tampered_trace_path)
    item["validation_receipt"]["trace_sha256"] = new_trace
    refs = item["validation_receipt"]["resolved_evidence_hashes"]
    item["validation_receipt"]["resolved_evidence_hashes"] = sorted(
        new_trace if reference == old_trace else reference for reference in refs
    )
    negative["tampered-trace"] = item

    item = copy.deepcopy(legit)
    event_trace = copy.deepcopy(legit_trace)
    missing_ref = "sha256:" + ("f" * 64)
    item["events"][0]["transition_rule_ref"] = missing_ref
    event_trace["events"][0]["transition_rule_ref"] = missing_ref
    projection_hash = candidate_projection_sha256(item)
    item["validation_receipt"]["candidate_projection_sha256"] = projection_hash
    event_trace["candidate_projection_sha256"] = projection_hash
    event_trace_path = TRACES / "unresolved-event-ref.trace.json"
    write_json(event_trace_path, event_trace)
    old_trace = item["validation_receipt"]["trace_sha256"]
    new_trace = hash_ref(event_trace_path)
    item["validation_receipt"]["trace_sha256"] = new_trace
    refs = item["validation_receipt"]["resolved_evidence_hashes"]
    item["validation_receipt"]["resolved_evidence_hashes"] = sorted(
        {
            *(new_trace if reference == old_trace else reference for reference in refs),
            missing_ref,
        }
    )
    negative["unresolved-event-ref"] = item

    item = copy.deepcopy(legit)
    item["candidate_result"]["final_completion"] = True
    negative["circular-field"] = item

    item = copy.deepcopy(legit)
    item["problem"]["instance_id"] = "parity-e\u0301"
    negative["canonicalization-variant"] = item

    for name, value in negative.items():
        write_json(FIXTURES / f"{name}.json", value)

    manifest = {
        "schema": "schemas/run-record.schema.v0.2.0-candidate.json",
        "validator": "src/pnp_glc_i0/semantic_validator.py",
        "fixtures": {
            "legit": {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": True,
                "final_completion": True,
                "record_valid": True,
                "record_accepted": True,
            },
            "cheat": {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": False,
                "final_completion": False,
                "record_valid": True,
                "record_accepted": False,
            },
            "robust-legit": {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": True,
                "final_completion": True,
                "record_valid": True,
                "record_accepted": True,
            },
            "neutral-legit": {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": True,
                "final_completion": True,
                "record_valid": True,
                "record_accepted": True,
            },
            "robust-neutral-legit": {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": True,
                "final_completion": True,
                "record_valid": True,
                "record_accepted": True,
            },
            "unknown-gate": {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": False,
                "final_completion": False,
                "record_valid": True,
                "record_accepted": False,
            },
            "self-report": {"structural_ok": False},
            "robust-null-spec": {"structural_ok": False},
            "failed-gate-admission": {"structural_ok": False},
            "false-final-completion": {"structural_ok": False},
            "unknown-final": {"structural_ok": False},
            "tampered-record": {
                "structural_ok": True,
                "semantic_ok": False,
                "record_valid": False,
                "record_accepted": False,
            },
            "tampered-trace": {
                "structural_ok": True,
                "semantic_ok": False,
                "record_valid": False,
                "record_accepted": False,
            },
            "unresolved-event-ref": {
                "structural_ok": True,
                "semantic_ok": False,
                "record_valid": False,
                "record_accepted": False,
            },
            "circular-field": {"structural_ok": False},
            "canonicalization-variant": {
                "structural_ok": True,
                "semantic_ok": False,
                "record_valid": False,
                "record_accepted": False,
            },
        },
    }
    write_json(FIXTURES / "manifest.json", manifest)


if __name__ == "__main__":
    main()
