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

import generate_fixtures_v021 as v021  # noqa: E402
from pnp_glc_i0.semantic_validator_v022 import (  # noqa: E402
    ARTIFACT_CLOSURE_SPEC_ID,
    EVIDENCE_ROLE_SPEC_ID,
    GATE_VERSION,
    NOT_APPLICABLE,
    PASS,
    PINNED_CLOSURE_SPEC_HASH,
    PINNED_FAIRNESS_HASH,
    PINNED_MAXIMAL_HASH,
    PINNED_PARITY_CONTRACT_HASH,
    PINNED_PARITY_INVARIANT_HASH,
    PINNED_PROJECTION_SPEC_HASH,
    PINNED_ROLE_SPEC_HASH,
    PINNED_RUN_ROBUST_HASH,
    PINNED_RUN_STANDARD_HASH,
    PINNED_SANDBOX_HASH,
    PINNED_SCHEMA_HASH,
    PINNED_TRACE_PUBLIC_KEY_HASH,
    PINNED_TWO_SAT_CONTRACT_HASH,
    PROJECTION_SPEC_ID,
    TRACE_MEASUREMENT_MODEL,
    TRACE_SIGNATURE_CONTEXT,
    TRACE_SIGNER_ID,
    VALIDATOR_VERSION,
    ArtifactIndex,
    _actual_operational_reference_map,
    _artifact_closure,
    _canonical_operational_reference_map,
    _direct_receipt_reference_map,
    _expected_operational_reference_map,
    candidate_projection_sha256,
    canonical_json_bytes,
    operational_reference_map_sha256,
    sha256_bytes,
    sha256_path,
)


SCHEMA = ROOT / "schemas" / "run-record.schema.v0.2.2-candidate.json"
VALIDATOR = ROOT / "src" / "pnp_glc_i0" / "semantic_validator_v022.py"
ARTIFACTS = ROOT / "artifacts-v0.2.2"
FIXTURES = ROOT / "fixtures-v0.2.2"
TRACES = ARTIFACTS / "traces"
AUTH = ARTIFACTS / "auth"
PROJECTION_SPEC = ARTIFACTS / "candidate-projection-spec.v0.2.2.json"
CLOSURE_SPEC = ARTIFACTS / "artifact-closure-spec.v0.2.2.json"
ROLE_SPEC = ARTIFACTS / "evidence-role-spec.v0.2.2.json"
PUBLIC_KEY = ARTIFACTS / "trace-public-key.v0.2.2.json"
SANDBOX = ARTIFACTS / "capability-sandbox.v0.2.2.json"
RUN_STANDARD = ARTIFACTS / "run-standard.v0.2.2.json"
RUN_ROBUST = ARTIFACTS / "run-robust.v0.2.2.json"
MAXIMAL = ARTIFACTS / "maximal-run.v0.2.2.json"
FAIRNESS = ARTIFACTS / "fairness.v0.2.2.json"
INVARIANT = ARTIFACTS / "parity-invariant.v0.2.2.json"
PARITY_CONTRACT = ARTIFACTS / "contract-parity.v0.2.2.json"
TWO_SAT_CONTRACT = ARTIFACTS / "contract-2sat.v0.2.2.json"


def write_json(path: Path, value: Any, *, ensure_ascii: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            value,
            ensure_ascii=ensure_ascii,
            sort_keys=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def hash_ref(path: Path) -> str:
    return f"sha256:{sha256_path(path)}"


def load_private_key(path: Path) -> Ed25519PrivateKey:
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("fixture signing key must be Ed25519")
    return key


def trace_envelope() -> dict[str, Any]:
    return {
        "spec_id": ARTIFACT_CLOSURE_SPEC_ID,
        "artifact_type": "capability-trace",
        "version": VALIDATOR_VERSION,
        "edges": [],
    }


def version_candidate(
    record: dict[str, Any], trace: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    record.pop("validation_receipt", None)
    record["schema_version"] = VALIDATOR_VERSION
    record["recorded_at"] = "2026-08-09T09:00:00Z"
    record["provenance"]["sources"][0].update(
        {
            "id": "run-record-v0.2.2-candidate",
            "locator": "schemas/run-record.schema.v0.2.2-candidate.json",
            "version": "0.2.2-candidate",
            "sha256": hash_ref(SCHEMA),
        }
    )
    record["provenance"]["implementation"].update(
        {
            "version": VALIDATOR_VERSION,
            "dependencies": [
                {"name": "jsonschema", "version": "4.26.0"},
                {"name": "cryptography", "version": "49.0.0"},
            ],
        }
    )
    for claim in record["claims"]:
        claim["source_refs"] = ["run-record-v0.2.2-candidate"]
        if "role/type-safe evidence closure" not in claim["failure_conditions"]:
            claim["failure_conditions"].append(
                "role/type-safe evidence closure failure"
            )
    record["mechanism"]["version"] = VALIDATOR_VERSION
    record["mechanism"]["oracle"]["version"] = VALIDATOR_VERSION
    record["problem"]["generator"]["version"] = VALIDATOR_VERSION
    record["problem"]["contract"]["version"] = VALIDATOR_VERSION

    if record["problem"]["family"] == "PARITY":
        record["problem"]["contract"]["sha256"] = hash_ref(PARITY_CONTRACT)
        record["problem"]["contract"]["completion_requirements"] = [
            "correct parity",
            "executed prefix invariant when applicable",
            "typed and authenticated evidence binding",
            "transition/resource derivation",
            "zero outstanding semantic-loss debt",
        ]
        if record["mechanism"]["id"] == "parity-stream":
            invariant_ref = hash_ref(INVARIANT)
            record["mechanism"]["admissibility"][
                "local_invariant_ref"
            ] = invariant_ref
            record["candidate_result"]["certificate_refs"] = [invariant_ref]
            for event in record["events"]:
                event["invariant_ref"] = invariant_ref
            record["events"][-1]["output_sha256"] = "sha256:" + sha256_bytes(
                canonical_json_bytes(record["candidate_result"])
            )
    else:
        record["problem"]["contract"]["sha256"] = hash_ref(TWO_SAT_CONTRACT)
        record["problem"]["contract"]["completion_requirements"] = [
            "SAT assignment or UNSAT mutual implication paths verify",
            "typed and authenticated evidence binding",
            "transition/resource derivation",
            "zero outstanding semantic-loss debt",
        ]

    trace.update(
        {
            "trace_version": VALIDATOR_VERSION,
            "gate_version": GATE_VERSION,
            "projection_spec_id": PROJECTION_SPEC_ID,
            "measurement_model": TRACE_MEASUREMENT_MODEL,
            "artifact_envelope": trace_envelope(),
        }
    )
    return record, trace


def parity_candidate(
    name: str, *, cheat: bool, robust: bool, bounded: bool
) -> tuple[dict[str, Any], dict[str, Any]]:
    record, trace = v021.version_parity_candidate(
        name,
        cheat=cheat,
        robust=robust,
        resource_bounded=bounded,
    )
    return version_candidate(record, trace)


def two_sat_candidate(
    name: str, *, variable_count: int, clauses: list[list[int]]
) -> tuple[dict[str, Any], dict[str, Any]]:
    record, trace = v021.build_two_sat_candidate(
        name, variable_count=variable_count, clauses=clauses
    )
    return version_candidate(record, trace)


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
    public_ref = hash_ref(PUBLIC_KEY)
    return {
        "artifact_envelope": {
            "spec_id": ARTIFACT_CLOSURE_SPEC_ID,
            "artifact_type": "trace-authenticity-receipt",
            "version": VALIDATOR_VERSION,
            "edges": [
                {
                    "role": "trace",
                    "expected_type": "capability-trace",
                    "sha256": trace_ref,
                },
                {
                    "role": "public-key",
                    "expected_type": "ed25519-public-key",
                    "sha256": public_ref,
                },
            ],
        },
        "receipt_version": VALIDATOR_VERSION,
        "algorithm": "Ed25519",
        "signer_id": TRACE_SIGNER_ID,
        "public_key_ref": public_ref,
        "trace_sha256": trace_ref,
        "signature_base64": base64.b64encode(signature).decode("ascii"),
    }


def gate_values(record: Mapping[str, Any], trace: Mapping[str, Any]) -> dict[str, str]:
    mechanism_id = record["mechanism"]["id"]
    robust = record["mechanism"]["run_quantifier"] == "robust"
    bounded = record["mechanism"]["resource_regime"] == "resource-bounded"
    table = mechanism_id == "parity-table-family"
    stream = mechanism_id == "parity-stream"
    provenance = trace["gate_evidence"].get("provenance_pass", True)
    provenance_gate = (
        PASS if provenance is True else "fail" if provenance is False else "unknown"
    )
    answer_access = trace.get("answer_access") == "none"
    return {
        "uniformity_pass": "fail" if table else PASS,
        "provenance_pass": provenance_gate,
        "refs_resolved_pass": PASS,
        "builder_execution_pass": PASS,
        "advice_generation_pass": PASS if table else NOT_APPLICABLE,
        "proof_verification_pass": PASS if stream else NOT_APPLICABLE,
        "advice_budget_pass": "fail" if table else PASS,
        "answer_access_pass": PASS if answer_access else "fail",
        "resource_budget_pass": PASS if bounded else NOT_APPLICABLE,
        "resource_account_pass": PASS,
        "oracle_free_pass": PASS if answer_access else "fail",
        "replay_pass": PASS,
        "run_class_nonempty": PASS,
        "maximality_pass": PASS if robust else NOT_APPLICABLE,
        "fairness_pass": PASS if robust else NOT_APPLICABLE,
        "trace_authenticity_pass": PASS,
        "transition_execution_pass": PASS,
        "resource_derivation_pass": PASS,
    }


def receipt_shell(
    record: Mapping[str, Any], trace: Mapping[str, Any]
) -> dict[str, Any]:
    robust = record["mechanism"]["run_quantifier"] == "robust"
    bounded = record["mechanism"]["resource_regime"] == "resource-bounded"
    gates = gate_values(record, trace)
    admission = all(value in {PASS, NOT_APPLICABLE} for value in gates.values())
    return {
        "receipt_version": VALIDATOR_VERSION,
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
        "maximal_run_spec_ref": hash_ref(MAXIMAL) if robust else None,
        "fairness_spec_ref": hash_ref(FAIRNESS) if robust else None,
        "trace_sha256": "sha256:" + "0" * 64,
        "trace_authenticity_ref": "sha256:" + "0" * 64,
        "trace_public_key_ref": hash_ref(PUBLIC_KEY),
        "trace_signer_id": TRACE_SIGNER_ID,
        "artifact_closure_spec_ref": hash_ref(CLOSURE_SPEC),
        "evidence_role_spec_ref": hash_ref(ROLE_SPEC),
        "operational_reference_map_sha256": "0" * 64,
        "resolved_evidence_hashes": [],
        "observed_answer_access": trace["answer_access"],
        "gates": gates,
        "admission_pass": admission,
        "correctness": {
            "oracle_pass": PASS,
            "contract_pass": PASS,
            "complete_pass": PASS,
            "budget_pass": PASS if bounded else NOT_APPLICABLE,
            "outstanding_loss_debt": 0,
        },
        "final_completion": admission,
        "reasons": [] if admission else ["one or more admission gates did not pass"],
    }


def finalize_fixture(
    name: str,
    record: dict[str, Any],
    trace: dict[str, Any],
    private_key: Ed25519PrivateKey,
    *,
    valid_signature: bool = True,
    receipt_overrides: Mapping[str, Any] | None = None,
    sign_actual_operational_map: bool = False,
    sync_trace_events: bool = True,
) -> dict[str, Any]:
    record.pop("validation_receipt", None)
    record["run_id"] = name
    trace["run_id"] = name
    if sync_trace_events:
        trace["events"] = copy.deepcopy(record["events"])
    trace["candidate_output"] = copy.deepcopy(record["candidate_result"])
    trace["certificate_refs"] = copy.deepcopy(
        record["candidate_result"]["certificate_refs"]
    )
    trace["candidate_projection_sha256"] = candidate_projection_sha256(record)
    trace["artifact_envelope"] = trace_envelope()

    receipt = receipt_shell(record, trace)
    if receipt_overrides:
        receipt.update(copy.deepcopy(dict(receipt_overrides)))
    record["validation_receipt"] = receipt
    expected_map = _expected_operational_reference_map(record)
    signed_map = (
        _actual_operational_reference_map(record)
        if sign_actual_operational_map
        else expected_map
    )
    trace["operational_reference_map"] = _canonical_operational_reference_map(
        signed_map
    )
    receipt["operational_reference_map_sha256"] = operational_reference_map_sha256(
        signed_map
    )

    trace_path = TRACES / f"{name}.trace.json"
    write_json(trace_path, trace)
    trace_ref = hash_ref(trace_path)
    auth_payload = authenticity_artifact(
        trace_ref, private_key, valid_signature=valid_signature
    )
    auth_path = AUTH / f"{name}.trace-auth.json"
    write_json(auth_path, auth_payload)
    receipt["trace_sha256"] = trace_ref
    receipt["trace_authenticity_ref"] = hash_ref(auth_path)

    store = ArtifactIndex(ROOT)
    closure = _artifact_closure(_direct_receipt_reference_map(record), store)
    receipt["resolved_evidence_hashes"] = [
        f"sha256:{reference}" for reference in sorted(closure.references)
    ]
    write_json(FIXTURES / f"{name}.json", record)
    return record


def clone_candidate(
    record: Mapping[str, Any], trace: Mapping[str, Any], name: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate = copy.deepcopy(record)
    candidate.pop("validation_receipt", None)
    candidate["run_id"] = name
    candidate["experiment"]["id"] = f"I0-{name}"
    cloned_trace = copy.deepcopy(trace)
    cloned_trace["run_id"] = name
    return candidate, cloned_trace


def recompute_closure(record: dict[str, Any]) -> None:
    store = ArtifactIndex(ROOT)
    closure = _artifact_closure(_direct_receipt_reference_map(record), store)
    record["validation_receipt"]["resolved_evidence_hashes"] = [
        f"sha256:{reference}" for reference in sorted(closure.references)
    ]


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
        record, trace = parity_candidate(
            name, cheat=cheat, robust=robust, bounded=bounded
        )
        records[name] = finalize_fixture(name, record, trace, private_key)
        traces[name] = trace

    record, trace = parity_candidate(
        "unknown-gate", cheat=False, robust=False, bounded=True
    )
    trace["gate_evidence"]["provenance_pass"] = "unknown"
    records["unknown-gate"] = finalize_fixture(
        "unknown-gate", record, trace, private_key
    )
    traces["unknown-gate"] = trace

    for name, variable_count, clauses in (
        ("2sat-sat", 3, [[1, 2], [-1, 3], [-2, -3]]),
        ("2sat-unsat", 1, [[1, 1], [-1, -1]]),
    ):
        record, trace = two_sat_candidate(
            name, variable_count=variable_count, clauses=clauses
        )
        records[name] = finalize_fixture(name, record, trace, private_key)
        traces[name] = trace

    negative: dict[str, dict[str, Any]] = {}

    # Schema-level contradiction family.
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

    # Integrity and derivation negatives.
    item = copy.deepcopy(records["legit"])
    item["candidate_result"]["answer"] ^= 1
    negative["tampered-record"] = item

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "tampered-trace"
    )
    attack_trace["events"][0]["from_state"] = "forged-start"
    negative["tampered-trace"] = finalize_fixture(
        "tampered-trace",
        item,
        attack_trace,
        private_key,
        sync_trace_events=False,
    )

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "fabricated-states-999"
    )
    item["ledger"]["counts"]["states"] = 999
    attack_trace["resource_samples"]["counts"]["states"] = 999
    negative["fabricated-states-999"] = finalize_fixture(
        "fabricated-states-999", item, attack_trace, private_key
    )

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "fabricated-transition-digest"
    )
    fabricated = "sha256:" + "e" * 64
    item["events"][0]["output_sha256"] = fabricated
    item["events"][1]["input_sha256"] = fabricated
    attack_trace["events"] = copy.deepcopy(item["events"])
    negative["fabricated-transition-digest"] = finalize_fixture(
        "fabricated-transition-digest", item, attack_trace, private_key
    )

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "fabricated-problem-size"
    )
    item["problem"]["size"]["n"] = 999
    negative["fabricated-problem-size"] = finalize_fixture(
        "fabricated-problem-size", item, attack_trace, private_key
    )

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "fabricated-failure-frontier"
    )
    item["failure_frontier"]["axes"][0]["value"] = 999
    negative["fabricated-failure-frontier"] = finalize_fixture(
        "fabricated-failure-frontier", item, attack_trace, private_key
    )

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "declared-answer-access-mismatch"
    )
    item["mechanism"]["admissibility"]["declared_answer_access"] = "truth-table"
    negative["declared-answer-access-mismatch"] = finalize_fixture(
        "declared-answer-access-mismatch", item, attack_trace, private_key
    )

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "bad-trace-signature"
    )
    negative["bad-trace-signature"] = finalize_fixture(
        "bad-trace-signature",
        item,
        attack_trace,
        private_key,
        valid_signature=False,
    )

    # Exact REF-TYPE-01: receipt-only robust -> standard substitution, no resign.
    item = copy.deepcopy(records["robust-legit"])
    item["validation_receipt"]["run_spec_ref"] = hash_ref(RUN_STANDARD)
    recompute_closure(item)
    negative["receipt-ref-substitution"] = item

    # AI-3's stronger type-confusion family, also without resigning.
    item = copy.deepcopy(records["robust-legit"])
    public_ref = hash_ref(PUBLIC_KEY)
    for key in (
        "run_spec_ref",
        "maximal_run_spec_ref",
        "fairness_spec_ref",
        "capability_sandbox_ref",
    ):
        item["validation_receipt"][key] = public_ref
    recompute_closure(item)
    negative["robust-ref-type-confusion"] = item

    # Valid-signature candidate/trace cross-role substitution.
    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "cross-role-contract-invariant"
    )
    contract_ref = hash_ref(PARITY_CONTRACT)
    invariant_ref = hash_ref(INVARIANT)
    item["problem"]["contract"]["sha256"] = invariant_ref
    item["mechanism"]["admissibility"]["local_invariant_ref"] = contract_ref
    item["candidate_result"]["certificate_refs"] = [contract_ref]
    for event in item["events"]:
        event["invariant_ref"] = contract_ref
    item["events"][-1]["output_sha256"] = "sha256:" + sha256_bytes(
        canonical_json_bytes(item["candidate_result"])
    )
    negative["cross-role-contract-invariant"] = finalize_fixture(
        "cross-role-contract-invariant",
        item,
        attack_trace,
        private_key,
        sign_actual_operational_map=True,
    )

    # Role-bearing edge and missing-transitive evidence attacks.
    missing_ref = "sha256:" + "f" * 64
    malformed_parent = {
        "artifact_envelope": {
            "spec_id": ARTIFACT_CLOSURE_SPEC_ID,
            "artifact_type": "run-spec",
            "version": VALIDATOR_VERSION,
            "edges": [
                {
                    "role": "fairness-spec",
                    "expected_type": "ed25519-public-key",
                    "sha256": hash_ref(PUBLIC_KEY),
                },
                {
                    "role": "legacy-run-source",
                    "expected_type": "opaque-content",
                    "sha256": missing_ref,
                },
            ],
        },
        "mode": "standard",
        "nonempty_witness": "successful start-to-terminal executable trace",
    }
    malformed_path = ARTIFACTS / "negative-malformed-role-edge.json"
    write_json(malformed_path, malformed_parent)
    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "malformed-role-edge"
    )
    negative["malformed-role-edge"] = finalize_fixture(
        "malformed-role-edge",
        item,
        attack_trace,
        private_key,
        receipt_overrides={"run_spec_ref": hash_ref(malformed_path)},
        sign_actual_operational_map=True,
    )

    missing_spec_parent = {
        "artifact_envelope": {
            "artifact_type": "run-spec",
            "version": VALIDATOR_VERSION,
            "edges": [],
        },
        "mode": "standard",
        "nonempty_witness": "successful start-to-terminal executable trace",
    }
    missing_spec_path = ARTIFACTS / "negative-missing-envelope-spec-id.json"
    write_json(missing_spec_path, missing_spec_parent)
    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "missing-envelope-spec-id"
    )
    negative["missing-envelope-spec-id"] = finalize_fixture(
        "missing-envelope-spec-id",
        item,
        attack_trace,
        private_key,
        receipt_overrides={"run_spec_ref": hash_ref(missing_spec_path)},
        sign_actual_operational_map=True,
    )

    item, attack_trace = clone_candidate(
        records["legit"], traces["legit"], "unresolved-event-ref"
    )
    item["events"][0]["transition_rule_ref"] = missing_ref
    negative["unresolved-event-ref"] = finalize_fixture(
        "unresolved-event-ref",
        item,
        attack_trace,
        private_key,
        sign_actual_operational_map=True,
    )

    item = copy.deepcopy(records["legit"])
    item["problem"]["instance_id"] = "parity-e\u0301"
    negative["canonicalization-variant"] = item

    item = copy.deepcopy(records["legit"])
    item["problem"]["instance_id"] = "\ud800"
    negative["unpaired-surrogate"] = item

    for name, value in negative.items():
        write_json(
            FIXTURES / f"{name}.json",
            value,
            ensure_ascii=(name == "unpaired-surrogate"),
        )

    # RawParseDomain fixture: keep the signed semantic value at integer zero,
    # but spell one raw token as -0. The strict tokenizer must reject it before
    # Python can erase the lexical distinction.
    negative_zero_path = FIXTURES / "negative-zero.json"
    negative_zero_text = (FIXTURES / "legit.json").read_text(encoding="utf-8")
    negative_zero_text = negative_zero_text.replace('"seed": 0', '"seed": -0', 1)
    negative_zero_path.write_text(negative_zero_text, encoding="utf-8", newline="\n")
    negative["negative-zero"] = copy.deepcopy(records["legit"])

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
        "negative-zero",
    }
    manifest_fixtures: dict[str, dict[str, Any]] = {}
    for name in sorted(accepted | honest_rejected | set(negative)):
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
        else:
            manifest_fixtures[name] = {
                "structural_ok": True,
                "semantic_ok": False,
                "record_valid": False,
                "record_accepted": False,
            }
    write_json(
        FIXTURES / "manifest.json",
        {
            "schema": "schemas/run-record.schema.v0.2.2-candidate.json",
            "validator": "src/pnp_glc_i0/semantic_validator_v022.py",
            "status": "Experiment fixtures; no P/NP conclusion",
            "fixtures": manifest_fixtures,
        },
    )


if __name__ == "__main__":
    main()
