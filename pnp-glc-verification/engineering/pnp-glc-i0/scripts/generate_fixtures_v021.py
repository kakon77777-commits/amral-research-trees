from __future__ import annotations

import argparse
import base64
import copy
import json
import sys
from pathlib import Path
from typing import Any, Mapping

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_fixtures as v020  # noqa: E402
from pnp_glc_i0.semantic_validator_v021 import (  # noqa: E402
    ARTIFACT_CLOSURE_SPEC_ID,
    GATE_VERSION,
    PASS,
    PINNED_TRACE_PUBLIC_KEY_HASH,
    PROJECTION_SPEC_ID,
    TRACE_MEASUREMENT_MODEL,
    TRACE_PRODUCER,
    TRACE_SIGNATURE_CONTEXT,
    TRACE_SIGNER_ID,
    ArtifactIndex,
    _artifact_closure,
    _direct_receipt_reference_set,
    _two_sat_candidate_result,
    candidate_projection_sha256,
    canonical_json_bytes,
    sha256_bytes,
    sha256_path,
)


SCHEMA = ROOT / "schemas" / "run-record.schema.v0.2.1-candidate.json"
VALIDATOR = ROOT / "src" / "pnp_glc_i0" / "semantic_validator_v021.py"
PARITY = ROOT / "src" / "pnp_glc_i0" / "parity.py"
TWO_SAT = ROOT / "src" / "pnp_glc_i0" / "two_sat.py"
ORACLES = ROOT / "src" / "pnp_glc_i0" / "oracles.py"
ARTIFACTS = ROOT / "artifacts-v0.2.1"
FIXTURES = ROOT / "fixtures-v0.2.1"
TRACES = ARTIFACTS / "traces"
AUTH = ARTIFACTS / "auth"
PROJECTION_SPEC = ARTIFACTS / "candidate-projection-spec.v0.2.1.json"
CLOSURE_SPEC = ARTIFACTS / "artifact-closure-spec.v0.2.1.json"
PUBLIC_KEY = ARTIFACTS / "trace-public-key.v0.2.1.json"
PARITY_CONTRACT = ARTIFACTS / "contract-parity.v0.2.1.json"
TWO_SAT_CONTRACT = ARTIFACTS / "contract-2sat.v0.2.1.json"

# These v0.2 artifacts are reused by content hash; frozen files are never edited.
SANDBOX = ROOT / "artifacts" / "sandbox-policy.v0.2.0.json"
RUN_STANDARD = ROOT / "artifacts" / "run-standard.v0.2.0.json"
RUN_ROBUST = ROOT / "artifacts" / "run-robust.v0.2.0.json"
MAXIMAL = ROOT / "artifacts" / "maximal-run.v0.2.0.json"
FAIRNESS = ROOT / "artifacts" / "fairness.v0.2.0.json"
INVARIANT = ROOT / "artifacts" / "parity-invariant.v0.2.0.md"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def hash_ref(path: Path) -> str:
    return f"sha256:{sha256_path(path)}"


def load_private_key(path: Path) -> Ed25519PrivateKey:
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("fixture signing key must be Ed25519")
    return key


def version_parity_candidate(
    name: str,
    *,
    cheat: bool,
    robust: bool,
    resource_bounded: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    record, trace = v020.build_candidate(
        name,
        cheat=cheat,
        robust=robust,
        resource_bounded=resource_bounded,
    )
    record["schema_version"] = "0.2.1"
    record["recorded_at"] = "2026-08-09T07:30:00Z"
    record["provenance"]["sources"][0].update(
        {
            "id": "run-record-v0.2.1-candidate",
            "locator": "schemas/run-record.schema.v0.2.1-candidate.json",
            "version": "0.2.1-candidate",
            "sha256": hash_ref(SCHEMA),
        }
    )
    record["provenance"]["implementation"].update(
        {
            "version": "0.2.1",
            "dependencies": [
                {"name": "jsonschema", "version": "4.26.0"},
                {"name": "cryptography", "version": "49.0.0"},
            ],
        }
    )
    claim = record["claims"][0]
    claim["source_refs"] = ["run-record-v0.2.1-candidate"]
    claim["assumptions"] = [
        "test trace signer private key remained outside published artifacts",
        "pinned I0 transition semantics",
    ]
    claim["failure_conditions"].extend(
        ["invalid trace signature", "unreconstructible transition or resource fold"]
    )
    record["mechanism"]["version"] = "0.2.1"
    record["mechanism"]["oracle"]["version"] = "0.2.1"
    record["problem"]["generator"]["version"] = "0.2.1"
    record["problem"]["contract"].update(
        {
            "version": "0.2.1",
            "sha256": hash_ref(PARITY_CONTRACT),
            "completion_requirements": [
                "correct parity and prefix invariant when applicable",
                "authenticated transition and resource derivation",
                "zero outstanding semantic-loss debt",
            ],
        }
    )
    trace.update(
        {
            "trace_version": "0.2.1",
            "gate_version": GATE_VERSION,
            "projection_spec_id": PROJECTION_SPEC_ID,
            "measurement_model": TRACE_MEASUREMENT_MODEL,
        }
    )
    trace["artifact_envelope"] = trace_envelope(record)
    trace["candidate_projection_sha256"] = candidate_projection_sha256(record)
    return record, trace


def trace_envelope(record: Mapping[str, Any]) -> dict[str, Any]:
    references: set[str] = set(record["candidate_result"]["certificate_refs"])
    for event in record["events"]:
        for key in ("transition_rule_ref", "invariant_ref"):
            if event[key] is not None:
                references.add(event[key])
    return {
        "spec_id": ARTIFACT_CLOSURE_SPEC_ID,
        "artifact_type": "capability-trace",
        "typed_refs": sorted(references),
    }


def build_two_sat_candidate(
    name: str, *, variable_count: int, clauses: list[list[int]]
) -> tuple[dict[str, Any], dict[str, Any]]:
    record, trace = version_parity_candidate(
        name, cheat=False, robust=False, resource_bounded=True
    )
    parameters = {"variable_count": variable_count, "clauses": clauses}
    candidate_result = _two_sat_candidate_result(parameters)
    input_payload = {"variable_count": variable_count, "clauses": clauses}
    input_hash = f"sha256:{sha256_bytes(canonical_json_bytes(input_payload))}"
    intermediate_hash = "sha256:" + sha256_bytes(
        canonical_json_bytes(
            {"state": ["2sat", variable_count, candidate_result["status"]]}
        )
    )
    result_hash = f"sha256:{sha256_bytes(canonical_json_bytes(candidate_result))}"
    rule_ref = hash_ref(TWO_SAT)
    events = [
        {
            "seq": 0,
            "kind": "solve",
            "from_state": "start",
            "to_state": "computed",
            "representation_before": "2cnf",
            "representation_after": "scc-result",
            "input_sha256": input_hash,
            "output_sha256": intermediate_hash,
            "transition_rule_ref": rule_ref,
            "invariant_ref": None,
            "time_ns": v020.costs(construction=19, update=31),
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
            "representation_before": "scc-result",
            "representation_after": "decision-certificate",
            "input_sha256": intermediate_hash,
            "output_sha256": result_hash,
            "transition_rule_ref": rule_ref,
            "invariant_ref": None,
            "time_ns": v020.costs(decode=11, verify=17),
            "debt_added": [],
            "debt_retired": [],
            "status": "ok",
            "failure": None,
        },
    ]
    code_bytes = TWO_SAT.stat().st_size
    description = {
        "program_code": code_bytes,
        "advice": 0,
        "builder_artifacts": code_bytes,
        "generated_tables": 0,
        "proof": 0,
    }
    record["experiment"].update(
        {
            "id": f"2SAT-I0-{candidate_result['status']}",
            "hypothesis_id": "pinned-2sat-end-to-end-certificate",
            "series_semantics": "fixed-program-scaling",
        }
    )
    record["claims"] = [
        {
            "id": "2SAT-I0-END-TO-END",
            "label": "Experiment",
            "statement": "The pinned SCC baseline result is replayed and independently checked on this fixture.",
            "status": "active",
            "source_refs": ["run-record-v0.2.1-candidate"],
            "domain": "bounded 2-SAT I0 fixtures",
            "quantifiers": ["one fixed solver for all encoded 2-SAT instances"],
            "assumptions": [
                "test trace signer private key remained outside published artifacts",
                "pinned deterministic Kosaraju implementation",
            ],
            "failure_conditions": [
                "invalid assignment or UNSAT path certificate",
                "invalid trace signature",
                "transition/resource derivation mismatch",
            ],
        }
    ]
    record["problem"] = {
        "family": "2-SAT",
        "instance_id": f"2sat-{candidate_result['status']}-{name}",
        "input_sha256": input_hash,
        "generator": {
            "name": "fixed-fixture",
            "version": "0.2.1",
            "seed": 0,
            "parameters": parameters,
        },
        "size": {"n": variable_count, "m": len(clauses)},
        "contract": {
            "id": "I0-2SAT",
            "version": "0.2.1",
            "sha256": hash_ref(TWO_SAT_CONTRACT),
            "completion_requirements": [
                "SAT assignment or UNSAT mutual implication paths verify",
                "authenticated transition and resource derivation",
                "zero outstanding semantic-loss debt",
            ],
        },
    }
    record["mechanism"] = {
        "id": "2sat-kosaraju",
        "name": "Deterministic implication graph plus Kosaraju SCC",
        "version": "0.2.1",
        "role": "baseline",
        "resource_regime": "resource-bounded",
        "run_quantifier": "standard",
        "baseline_id": None,
        "operations": ["build", "solve", "decode", "verify"],
        "admissibility": {
            "uniform": True,
            "oracle_free": True,
            "finite_precision": True,
            "program_quantifiers": "exists-one-program-for-all-input-lengths",
            "builder_ref": rule_ref,
            "step_ref": rule_ref,
            "decode_ref": rule_ref,
            "declared_answer_access": "none",
            "advice_generator_ref": None,
            "local_invariant_ref": None,
            "randomness": "none",
            "interaction": "none",
            "advice": "none",
            "parallelism": "single worker",
            "hardware": "abstract deterministic machine",
        },
        "oracle": {
            "name": "independent 2-SAT certificate oracle",
            "version": "0.2.1",
            "independent": True,
            "checks": ["assignment" if candidate_result["status"] == "sat" else "mutual implication paths"],
            "sha256": hash_ref(ORACLES),
        },
    }
    record["ledger"].update(
        {
            "time_ns": v020.sum_costs(events),
            "space_bytes": {
                "peak": 2048,
                "final": len(canonical_json_bytes(candidate_result)),
                "artifacts": sum(description.values()),
            },
            "description_bytes": description,
            "admission_costs": {
                "builder": {
                    "time_ns": 19,
                    "peak_space_bytes": 1024,
                    "peak_output_bytes": code_bytes,
                },
                "advice_generation": {
                    "time_ns": 0,
                    "peak_space_bytes": 0,
                    "peak_output_bytes": 0,
                },
                "proof_verification": {
                    "time_ns": 0,
                    "peak_space_bytes": 0,
                    "peak_output_bytes": 0,
                },
            },
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
    )
    record["events"] = events
    record["candidate_result"] = candidate_result
    record["failure_frontier"] = {
        "axes": [
            {"name": "variables", "value": variable_count, "unit": "variables"},
            {"name": "clauses", "value": len(clauses), "unit": "clauses"},
        ],
        "first_observed_failure": None,
        "censored": False,
        "interpretation": "Experiment only; no P=NP or P!=NP inference.",
    }
    trace.update(
        {
            "answer_access": "none",
            "candidate_output": candidate_result,
            "certificate_refs": [],
            "events": events,
            "resource_samples": resource_samples(record),
        }
    )
    trace["artifact_envelope"] = trace_envelope(record)
    trace["candidate_projection_sha256"] = candidate_projection_sha256(record)
    return record, trace


def resource_samples(record: Mapping[str, Any]) -> dict[str, Any]:
    ledger = record["ledger"]
    return {
        key: copy.deepcopy(ledger[key])
        for key in (
            "space_bytes",
            "description_bytes",
            "admission_costs",
            "precision",
            "counts",
        )
    }


def authenticity_artifact(
    trace_ref: str,
    private_key: Ed25519PrivateKey,
    *,
    valid_signature: bool,
) -> dict[str, Any]:
    trace_hash = trace_ref.removeprefix("sha256:")
    signature = private_key.sign(
        TRACE_SIGNATURE_CONTEXT + bytes.fromhex(trace_hash)
    )
    if not valid_signature:
        signature = bytes([signature[0] ^ 1]) + signature[1:]
    public_ref = f"sha256:{PINNED_TRACE_PUBLIC_KEY_HASH}"
    return {
        "artifact_envelope": {
            "spec_id": ARTIFACT_CLOSURE_SPEC_ID,
            "artifact_type": "trace-authenticity-receipt",
            "typed_refs": sorted([trace_ref, public_ref]),
        },
        "receipt_version": "0.2.1",
        "algorithm": "Ed25519",
        "signer_id": TRACE_SIGNER_ID,
        "public_key_ref": public_ref,
        "trace_sha256": trace_ref,
        "signature_base64": base64.b64encode(signature).decode("ascii"),
    }


def gate_values(
    record: Mapping[str, Any],
    trace: Mapping[str, Any],
    *,
    cheat: bool,
    authenticity: str = "pass",
    transition: str = "pass",
    resource_derivation: str = "pass",
    refs: str = "pass",
) -> dict[str, str]:
    robust = record["mechanism"]["run_quantifier"] == "robust"
    bounded = record["mechanism"]["resource_regime"] == "resource-bounded"
    proof_applicable = (
        record["mechanism"]["admissibility"]["local_invariant_ref"] is not None
        or record["ledger"]["description_bytes"]["proof"] > 0
    )
    provenance = trace["gate_evidence"].get("provenance_pass", True)
    if provenance is True:
        provenance_gate = "pass"
    elif provenance is False:
        provenance_gate = "fail"
    else:
        provenance_gate = "unknown"
    return {
        "uniformity_pass": "fail" if cheat else "pass",
        "provenance_pass": provenance_gate,
        "refs_resolved_pass": refs,
        "builder_execution_pass": "pass",
        "advice_generation_pass": "pass" if cheat else "not-applicable",
        "proof_verification_pass": "pass" if proof_applicable else "not-applicable",
        "advice_budget_pass": "fail" if cheat else "pass",
        "answer_access_pass": "fail" if cheat else "pass",
        "resource_budget_pass": "pass" if bounded else "not-applicable",
        "resource_account_pass": "pass" if resource_derivation == "pass" else "fail",
        "oracle_free_pass": "fail" if cheat else "pass",
        "replay_pass": "pass",
        "run_class_nonempty": "pass",
        "maximality_pass": "pass" if robust else "not-applicable",
        "fairness_pass": "pass" if robust else "not-applicable",
        "trace_authenticity_pass": authenticity,
        "transition_execution_pass": transition,
        "resource_derivation_pass": resource_derivation,
    }


def finalize_fixture(
    name: str,
    record: dict[str, Any],
    trace: dict[str, Any],
    private_key: Ed25519PrivateKey,
    *,
    cheat: bool = False,
    valid_signature: bool = True,
    claimed_authenticity: str = "pass",
    claimed_transition: str = "pass",
    claimed_resource_derivation: str = "pass",
    claimed_refs: str = "pass",
    admission: bool | None = None,
    run_spec_override: str | None = None,
) -> dict[str, Any]:
    record.pop("validation_receipt", None)
    trace["run_id"] = record["run_id"]
    trace["candidate_output"] = copy.deepcopy(record["candidate_result"])
    trace["certificate_refs"] = copy.deepcopy(
        record["candidate_result"]["certificate_refs"]
    )
    trace["candidate_projection_sha256"] = candidate_projection_sha256(record)
    trace["artifact_envelope"] = trace_envelope(record)
    trace_path = TRACES / f"{name}.trace.json"
    write_json(trace_path, trace)
    trace_ref = hash_ref(trace_path)
    auth_payload = authenticity_artifact(
        trace_ref, private_key, valid_signature=valid_signature
    )
    auth_path = AUTH / f"{name}.trace-auth.json"
    write_json(auth_path, auth_payload)

    robust = record["mechanism"]["run_quantifier"] == "robust"
    bounded = record["mechanism"]["resource_regime"] == "resource-bounded"
    gates = gate_values(
        record,
        trace,
        cheat=cheat,
        authenticity=claimed_authenticity,
        transition=claimed_transition,
        resource_derivation=claimed_resource_derivation,
        refs=claimed_refs,
    )
    if admission is None:
        admission = all(
            status == "pass"
            for key, status in gates.items()
            if status != "not-applicable"
        )
    maximal_ref = hash_ref(MAXIMAL) if robust else None
    fairness_ref = hash_ref(FAIRNESS) if robust else None
    record["validation_receipt"] = {
        "receipt_version": "0.2.1",
        "decision_source": "external-validator",
        "gate_version": GATE_VERSION,
        "schema_sha256": hash_ref(SCHEMA),
        "validator_sha256": hash_ref(VALIDATOR),
        "validator_independent": True,
        "projection_spec_id": PROJECTION_SPEC_ID,
        "projection_spec_sha256": hash_ref(PROJECTION_SPEC),
        "candidate_projection_sha256": candidate_projection_sha256(record),
        "capability_sandbox_ref": hash_ref(SANDBOX),
        "run_spec_ref": run_spec_override
        or hash_ref(RUN_ROBUST if robust else RUN_STANDARD),
        "maximal_run_spec_ref": maximal_ref,
        "fairness_spec_ref": fairness_ref,
        "trace_sha256": trace_ref,
        "trace_authenticity_ref": hash_ref(auth_path),
        "trace_public_key_ref": hash_ref(PUBLIC_KEY),
        "trace_signer_id": TRACE_SIGNER_ID,
        "artifact_closure_spec_ref": hash_ref(CLOSURE_SPEC),
        "resolved_evidence_hashes": [],
        "observed_answer_access": trace["answer_access"],
        "gates": gates,
        "admission_pass": admission,
        "correctness": {
            "oracle_pass": "pass",
            "contract_pass": "pass"
            if claimed_authenticity == "pass"
            and claimed_transition == "pass"
            and claimed_resource_derivation == "pass"
            else "fail",
            "complete_pass": "pass",
            "budget_pass": "pass" if bounded else "not-applicable",
            "outstanding_loss_debt": 0,
        },
        "final_completion": admission,
        "reasons": [] if admission else ["one or more admission gates did not pass"],
    }
    store = ArtifactIndex(ROOT)
    closure = _artifact_closure(_direct_receipt_reference_set(record), store)
    record["validation_receipt"]["resolved_evidence_hashes"] = [
        f"sha256:{reference}" for reference in sorted(closure.references)
    ]
    write_json(FIXTURES / f"{name}.json", record)
    return record


def clone_for_attack(
    record: Mapping[str, Any], trace: Mapping[str, Any], name: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    item = copy.deepcopy(record)
    item.pop("validation_receipt", None)
    item["run_id"] = name
    item["experiment"]["id"] = f"PARITY-0-{name}"
    attack_trace = copy.deepcopy(trace)
    attack_trace["run_id"] = name
    return item, attack_trace


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signing-key", required=True, type=Path)
    args = parser.parse_args()
    private_key = load_private_key(args.signing_key)
    FIXTURES.mkdir(parents=True, exist_ok=True)
    TRACES.mkdir(parents=True, exist_ok=True)
    AUTH.mkdir(parents=True, exist_ok=True)

    records: dict[str, dict[str, Any]] = {}
    traces: dict[str, dict[str, Any]] = {}

    for name, cheat, robust, bounded in (
        ("legit", False, False, True),
        ("cheat", True, False, True),
        ("robust-legit", False, True, True),
        ("neutral-legit", False, False, False),
        ("robust-neutral-legit", False, True, False),
    ):
        record, trace = version_parity_candidate(
            name, cheat=cheat, robust=robust, resource_bounded=bounded
        )
        records[name] = finalize_fixture(
            name, record, trace, private_key, cheat=cheat
        )
        traces[name] = trace

    record, trace = version_parity_candidate(
        "unknown-gate", cheat=False, robust=False, resource_bounded=True
    )
    trace["gate_evidence"]["provenance_pass"] = "unknown"
    records["unknown-gate"] = finalize_fixture(
        "unknown-gate", record, trace, private_key, admission=False
    )
    traces["unknown-gate"] = trace

    for name, variable_count, clauses in (
        ("2sat-sat", 3, [[1, 2], [-1, 3], [-2, -3]]),
        ("2sat-unsat", 1, [[1, 1], [-1, -1]]),
    ):
        record, trace = build_two_sat_candidate(
            name, variable_count=variable_count, clauses=clauses
        )
        records[name] = finalize_fixture(name, record, trace, private_key)
        traces[name] = trace

    # Schema-level contradictions from the frozen counterexample suite.
    negative: dict[str, dict[str, Any]] = {}
    item = copy.deepcopy(records["legit"])
    item["candidate_result"]["admission_pass"] = True
    negative["self-report"] = item

    item = copy.deepcopy(records["robust-legit"])
    item["validation_receipt"]["maximal_run_spec_ref"] = None
    item["validation_receipt"]["fairness_spec_ref"] = None
    negative["robust-null-spec"] = item

    item = copy.deepcopy(records["legit"])
    item["validation_receipt"]["gates"]["uniformity_pass"] = "fail"
    item["validation_receipt"]["admission_pass"] = True
    negative["failed-gate-admission"] = item

    item = copy.deepcopy(records["legit"])
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

    item = copy.deepcopy(records["legit"])
    item["candidate_result"]["status"] = "unknown"
    item["validation_receipt"]["final_completion"] = True
    negative["unknown-final"] = item

    item = copy.deepcopy(records["legit"])
    item["candidate_result"]["final_completion"] = True
    negative["circular-field"] = item

    # Record and trace integrity negatives.
    item = copy.deepcopy(records["legit"])
    item["candidate_result"]["answer"] ^= 1
    negative["tampered-record"] = item

    item, attack_trace = clone_for_attack(
        records["legit"], traces["legit"], "tampered-trace"
    )
    attack_trace["events"][0]["from_state"] = "forged-start"
    negative["tampered-trace"] = finalize_fixture(
        "tampered-trace", item, attack_trace, private_key
    )

    item, attack_trace = clone_for_attack(
        records["legit"], traces["legit"], "fabricated-states-999"
    )
    item["ledger"]["counts"]["states"] = 999
    attack_trace["resource_samples"]["counts"]["states"] = 999
    negative["fabricated-states-999"] = finalize_fixture(
        "fabricated-states-999", item, attack_trace, private_key
    )

    item, attack_trace = clone_for_attack(
        records["legit"], traces["legit"], "fabricated-transition-digest"
    )
    fabricated = "sha256:" + ("e" * 64)
    item["events"][0]["output_sha256"] = fabricated
    item["events"][1]["input_sha256"] = fabricated
    attack_trace["events"] = copy.deepcopy(item["events"])
    negative["fabricated-transition-digest"] = finalize_fixture(
        "fabricated-transition-digest", item, attack_trace, private_key
    )

    item, attack_trace = clone_for_attack(
        records["legit"], traces["legit"], "bad-trace-signature"
    )
    negative["bad-trace-signature"] = finalize_fixture(
        "bad-trace-signature",
        item,
        attack_trace,
        private_key,
        valid_signature=False,
    )

    missing_ref = "sha256:" + ("f" * 64)
    transitive_parent = {
        "artifact_envelope": {
            "spec_id": ARTIFACT_CLOSURE_SPEC_ID,
            "artifact_type": "run-spec",
            "typed_refs": [missing_ref],
        },
        "mode": "standard",
        "version": "0.2.1-negative-fixture",
    }
    transitive_path = ARTIFACTS / "negative-missing-transitive-parent.json"
    write_json(transitive_path, transitive_parent)
    item, attack_trace = clone_for_attack(
        records["legit"], traces["legit"], "missing-transitive-ref"
    )
    negative["missing-transitive-ref"] = finalize_fixture(
        "missing-transitive-ref",
        item,
        attack_trace,
        private_key,
        run_spec_override=hash_ref(transitive_path),
    )

    item, attack_trace = clone_for_attack(
        records["legit"], traces["legit"], "unresolved-event-ref"
    )
    item["events"][0]["transition_rule_ref"] = missing_ref
    attack_trace["events"] = copy.deepcopy(item["events"])
    negative["unresolved-event-ref"] = finalize_fixture(
        "unresolved-event-ref", item, attack_trace, private_key
    )

    item = copy.deepcopy(records["legit"])
    item["problem"]["instance_id"] = "parity-e\u0301"
    negative["canonicalization-variant"] = item

    for name, value in negative.items():
        write_json(FIXTURES / f"{name}.json", value)

    accepted = {
        "legit",
        "robust-legit",
        "neutral-legit",
        "robust-neutral-legit",
        "2sat-sat",
        "2sat-unsat",
    }
    honest_rejected = {"cheat", "unknown-gate"}
    structural_rejected = {
        "self-report",
        "robust-null-spec",
        "failed-gate-admission",
        "false-final-completion",
        "unknown-final",
        "circular-field",
    }
    semantic_rejected = set(negative) - structural_rejected
    fixture_names = sorted(accepted | honest_rejected | set(negative))
    manifest_fixtures: dict[str, dict[str, Any]] = {}
    for name in fixture_names:
        if name in accepted:
            manifest_fixtures[name] = {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": True,
                "final_completion": True,
                "record_valid": True,
                "record_accepted": True,
            }
        elif name in honest_rejected:
            manifest_fixtures[name] = {
                "structural_ok": True,
                "semantic_ok": True,
                "admission_pass": False,
                "final_completion": False,
                "record_valid": True,
                "record_accepted": False,
            }
        elif name in structural_rejected:
            manifest_fixtures[name] = {"structural_ok": False}
        elif name in semantic_rejected:
            manifest_fixtures[name] = {
                "structural_ok": True,
                "semantic_ok": False,
                "record_valid": False,
                "record_accepted": False,
            }
    manifest = {
        "schema": "schemas/run-record.schema.v0.2.1-candidate.json",
        "validator": "src/pnp_glc_i0/semantic_validator_v021.py",
        "status": "Experiment fixtures; no P/NP conclusion",
        "fixtures": manifest_fixtures,
    }
    write_json(FIXTURES / "manifest.json", manifest)


if __name__ == "__main__":
    main()
