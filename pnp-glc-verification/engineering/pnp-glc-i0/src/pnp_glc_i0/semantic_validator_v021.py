"""Versioned external semantic validator for run-record schema v0.2.1.

The JSON Schema layer rejects internally contradictory records. This module
independently resolves a transitive content closure, authenticates the trace,
executes the pinned I0 transition semantics, derives resource folds, checks
every applicable gate, and checks the external validation receipt.

Scope is deliberately bounded: transition execution currently supports the
two PARITY-0 mechanisms. Unsupported mechanisms produce ``unknown`` and fail
closed.  The AI-3 Lean admission kernel is a reference for the four-valued gate
matrix only; it is not a proof of this validator or its replay implementation.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import unicodedata
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator, FormatChecker

from . import oracles as oracle_module
from . import parity as parity_module
from . import two_sat as two_sat_module
from .oracles import (
    assignment_satisfies_2sat,
    parity_oracle,
    verify_unsat_certificate,
)
from .parity import TruthTableFamily, stream_parity
from .two_sat import solve_2sat


VALIDATOR_VERSION = "0.2.1"
GATE_VERSION = "i0-admission-gate/0.2.1"
PROJECTION_SPEC_ID = "urn:evemisslab:pnp-glc:candidate-projection:0.2.1"
ARTIFACT_CLOSURE_SPEC_ID = "urn:evemisslab:pnp-glc:artifact-closure:0.2.1"
TRACE_PRODUCER = "pnp-glc-i0-capability-sandbox"
TRACE_SIGNER_ID = "i0-test-trace-signer-20260809"
TRACE_MEASUREMENT_MODEL = "authenticated-i0-single-worker-linear/0.2.1"
TRACE_SIGNATURE_CONTEXT = b"pnp-glc-i0-trace-v0.2.1\0"
PASS = "pass"
FAIL = "fail"
UNKNOWN = "unknown"
NOT_APPLICABLE = "not-applicable"
MAX_SAFE_INTEGER = 9_007_199_254_740_991

# These literals pin the independently reviewed interface artifacts and code.
# A changed file must produce a new validator version rather than silently
# changing the meaning of this candidate.
PINNED_SCHEMA_HASH = "567417a82ea82c8c2ce7ec81df1b4bec5876044f54213446e4ce298ceade6c2b"
PINNED_PROJECTION_SPEC_HASH = "70caae9973a3a02ad8f45364be2175a51ba62c6c0d75b6c807b7b8dfb5bbd115"
PINNED_CLOSURE_SPEC_HASH = "b466bf8d630bac4b1a42a28f534c5d20a0713d418ccb3826ed69ff71d7585c94"
PINNED_TRACE_PUBLIC_KEY_HASH = "27d25ebf48c59e9aff166d32970c3444dc78e25c352f012b3998b0626dfb2a3d"
PINNED_PARITY_RULE_HASH = "bdfb4cd28a8730aa99b058dd6567027b98f0125fbf503a42e0fb895c686aedef"
PINNED_ORACLE_HASH = "c8c5f6a0c132b11c56fd7964b737c1eb4f0b6a8674c7de8adcda50ca4b54efce"
PINNED_TWO_SAT_RULE_HASH = "ed1028c0263dc5a69864fb42d02ada9756b40ee51149d9dd376dd206622a8971"

GATE_KEYS = (
    "uniformity_pass",
    "provenance_pass",
    "refs_resolved_pass",
    "builder_execution_pass",
    "advice_generation_pass",
    "proof_verification_pass",
    "advice_budget_pass",
    "answer_access_pass",
    "resource_budget_pass",
    "resource_account_pass",
    "oracle_free_pass",
    "replay_pass",
    "run_class_nonempty",
    "maximality_pass",
    "fairness_pass",
    "trace_authenticity_pass",
    "transition_execution_pass",
    "resource_derivation_pass",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


PINNED_VALIDATOR_BYTES = Path(__file__).read_bytes()
PINNED_VALIDATOR_HASH = sha256_bytes(PINNED_VALIDATOR_BYTES)
PINNED_PARITY_RULE_BYTES = Path(parity_module.__file__).read_bytes()
PINNED_ORACLE_BYTES = Path(oracle_module.__file__).read_bytes()
PINNED_TWO_SAT_RULE_BYTES = Path(two_sat_module.__file__).read_bytes()


def normalize_hash(reference: str) -> str:
    if not isinstance(reference, str):
        raise ValueError(f"SHA-256 reference must be a string: {reference!r}")
    value = reference.removeprefix("sha256:").lower()
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"invalid SHA-256 reference: {reference!r}")
    return value


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class ReplayResult:
    ok: bool
    outstanding_debt: int
    issues: tuple[ValidationIssue, ...]


@dataclass(frozen=True)
class ClosureResult:
    references: frozenset[str]
    status: str


@dataclass(frozen=True)
class ValidationReport:
    schema_version: str | None
    validator_version: str
    structural_ok: bool
    semantic_ok: bool
    admission_pass: bool | None
    final_completion: bool | None
    issues: tuple[ValidationIssue, ...]

    @property
    def record_valid(self) -> bool:
        return self.structural_ok and self.semantic_ok

    @property
    def record_accepted(self) -> bool:
        return self.record_valid and self.admission_pass is True

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["record_valid"] = self.record_valid
        payload["record_accepted"] = self.record_accepted
        return payload


def _json_path(parts: Iterable[Any]) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def _unique_object(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _load_json_object_bytes(data: bytes, *, source: str) -> Mapping[str, Any]:
    value = json.loads(
        data.decode("utf-8"),
        object_pairs_hook=_unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON number: {token}")
        ),
    )
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {source}")
    return value


def load_json(path: Path) -> Mapping[str, Any]:
    return _load_json_object_bytes(path.read_bytes(), source=str(path))


def _canonical_domain_issues(value: Any, path: str = "$") -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if value is None or isinstance(value, bool):
        return issues
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            issues.append(
                ValidationIssue(
                    "canonical-integer-range",
                    path,
                    "integer exceeds the projection specification's exact range",
                )
            )
        return issues
    if isinstance(value, float):
        issues.append(
            ValidationIssue(
                "canonical-float-forbidden",
                path,
                    "candidate projection v0.2.1 admits integers only",
            )
        )
        return issues
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            issues.append(
                ValidationIssue(
                    "canonical-unicode-nfc",
                    path,
                    "string is not Unicode NFC",
                )
            )
        return issues
    if isinstance(value, list):
        for index, item in enumerate(value):
            issues.extend(_canonical_domain_issues(item, f"{path}[{index}]"))
        return issues
    if isinstance(value, dict):
        for key, item in value.items():
            if unicodedata.normalize("NFC", key) != key:
                issues.append(
                    ValidationIssue(
                        "canonical-key-nfc",
                        f"{path}.{key}",
                        "object key is not Unicode NFC",
                    )
                )
            issues.extend(_canonical_domain_issues(item, f"{path}.{key}"))
        return issues
    issues.append(
        ValidationIssue(
            "canonical-type",
            path,
            f"unsupported projection value type: {type(value).__name__}",
        )
    )
    return issues


def canonical_json_bytes(value: Any) -> bytes:
    issues = _canonical_domain_issues(value)
    if issues:
        raise ValueError(issues[0].message)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def candidate_projection(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in record.items()
        if key != "validation_receipt"
    }


def candidate_projection_sha256(record: Mapping[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(candidate_projection(record)))


class ArtifactIndex:
    """Read-only content-addressed view over a trusted artifact directory."""

    def __init__(self, root: Path):
        self.root = root.resolve()
        if not self.root.is_dir():
            raise ValueError(f"artifact root is not a directory: {self.root}")
        by_hash: dict[str, list[tuple[Path, bytes]]] = {}
        for path in sorted(self.root.rglob("*")):
            if path.is_file():
                resolved = path.resolve()
                snapshot = resolved.read_bytes()
                by_hash.setdefault(sha256_bytes(snapshot), []).append(
                    (resolved, snapshot)
                )
        self._by_hash = by_hash

    def resolve(self, reference: str) -> tuple[tuple[Path, bytes], ...]:
        return tuple(self._by_hash.get(normalize_hash(reference), ()))

    def contains(self, reference: str) -> bool:
        return bool(self.resolve(reference))

    def load_json(self, reference: str) -> Mapping[str, Any]:
        snapshots = self.resolve(reference)
        if not snapshots:
            raise FileNotFoundError(reference)
        path, snapshot = snapshots[0]
        value = json.loads(
            snapshot.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ValueError(f"non-finite JSON number: {token}")
            ),
        )
        if not isinstance(value, dict):
            raise ValueError(f"expected JSON object: {path}")
        return value


def _direct_receipt_reference_set(record: Mapping[str, Any]) -> set[str]:
    receipt = record["validation_receipt"]
    mechanism = record["mechanism"]
    admissibility = mechanism["admissibility"]
    references = {
        receipt["schema_sha256"],
        receipt["validator_sha256"],
        receipt["projection_spec_sha256"],
        receipt["artifact_closure_spec_ref"],
        receipt["capability_sandbox_ref"],
        receipt["run_spec_ref"],
        receipt["trace_sha256"],
        receipt["trace_authenticity_ref"],
        receipt["trace_public_key_ref"],
        admissibility["builder_ref"],
        admissibility["step_ref"],
        admissibility["decode_ref"],
        mechanism["oracle"]["sha256"],
        record["problem"]["contract"]["sha256"],
    }
    for key in ("maximal_run_spec_ref", "fairness_spec_ref"):
        if receipt[key] is not None:
            references.add(receipt[key])
    for key in ("advice_generator_ref", "local_invariant_ref"):
        if admissibility[key] is not None:
            references.add(admissibility[key])
    for event in record["events"]:
        for key in ("transition_rule_ref", "invariant_ref"):
            if event[key] is not None:
                references.add(event[key])
    references.update(record["candidate_result"]["certificate_refs"])
    return {normalize_hash(reference) for reference in references}


def _artifact_closure(
    direct_references: Iterable[str], store: ArtifactIndex
) -> ClosureResult:
    """Resolve the fixed-point closure from one immutable byte snapshot.

    Non-JSON and non-enveloped JSON artifacts are leaves. A known typed
    envelope contributes its ``typed_refs``. Malformed envelopes fail; an
    envelope carrying an unknown specification is ``unknown`` and blocks
    admission without pretending to be a conclusive missing-content failure.
    """

    references: set[str] = set()
    queue: deque[str] = deque(normalize_hash(ref) for ref in direct_references)
    status = PASS
    while queue:
        reference = queue.popleft()
        if reference in references:
            continue
        references.add(reference)
        snapshots = store.resolve(reference)
        if not snapshots:
            status = FAIL
            continue
        _, snapshot = snapshots[0]
        try:
            value = json.loads(
                snapshot.decode("utf-8"),
                object_pairs_hook=_unique_object,
                parse_constant=lambda token: (_ for _ in ()).throw(
                    ValueError(f"non-finite JSON number: {token}")
                ),
            )
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
            continue
        if not isinstance(value, dict) or "artifact_envelope" not in value:
            continue
        envelope = value["artifact_envelope"]
        if not isinstance(envelope, dict):
            status = FAIL
            continue
        if envelope.get("spec_id") != ARTIFACT_CLOSURE_SPEC_ID:
            if status != FAIL:
                status = UNKNOWN
            continue
        artifact_type = envelope.get("artifact_type")
        typed_refs = envelope.get("typed_refs")
        if (
            not isinstance(artifact_type, str)
            or not artifact_type
            or not isinstance(typed_refs, list)
            or not all(isinstance(item, str) for item in typed_refs)
        ):
            status = FAIL
            continue
        try:
            normalized = [normalize_hash(item) for item in typed_refs]
        except ValueError:
            status = FAIL
            continue
        if len(normalized) != len(set(normalized)):
            status = FAIL
            continue
        queue.extend(normalized)
    return ClosureResult(frozenset(references), status)


def _trace_authenticity_status(
    record: Mapping[str, Any], store: ArtifactIndex
) -> str:
    receipt = record["validation_receipt"]
    try:
        trace_hash = normalize_hash(receipt["trace_sha256"])
        public_key_hash = normalize_hash(receipt["trace_public_key_ref"])
        if public_key_hash != PINNED_TRACE_PUBLIC_KEY_HASH:
            return FAIL
        if receipt["trace_signer_id"] != TRACE_SIGNER_ID:
            return FAIL

        authenticity = store.load_json(receipt["trace_authenticity_ref"])
        envelope = authenticity.get("artifact_envelope")
        if not isinstance(envelope, dict):
            return FAIL
        if (
            envelope.get("spec_id") != ARTIFACT_CLOSURE_SPEC_ID
            or envelope.get("artifact_type") != "trace-authenticity-receipt"
        ):
            return FAIL
        typed_refs = envelope.get("typed_refs")
        if not isinstance(typed_refs, list):
            return FAIL
        if {normalize_hash(item) for item in typed_refs} != {
            trace_hash,
            public_key_hash,
        }:
            return FAIL
        if (
            authenticity.get("receipt_version") != VALIDATOR_VERSION
            or authenticity.get("algorithm") != "Ed25519"
            or authenticity.get("signer_id") != TRACE_SIGNER_ID
            or normalize_hash(authenticity.get("public_key_ref", ""))
            != public_key_hash
            or normalize_hash(authenticity.get("trace_sha256", "")) != trace_hash
        ):
            return FAIL

        public_key_artifact = store.load_json(receipt["trace_public_key_ref"])
        key_envelope = public_key_artifact.get("artifact_envelope")
        if not isinstance(key_envelope, dict):
            return FAIL
        if (
            key_envelope.get("spec_id") != ARTIFACT_CLOSURE_SPEC_ID
            or key_envelope.get("artifact_type") != "ed25519-public-key"
            or key_envelope.get("typed_refs") != []
            or public_key_artifact.get("algorithm") != "Ed25519"
            or public_key_artifact.get("key_id") != TRACE_SIGNER_ID
        ):
            return FAIL
        public_bytes = base64.b64decode(
            public_key_artifact["public_key_base64"], validate=True
        )
        signature = base64.b64decode(
            authenticity["signature_base64"], validate=True
        )
        if len(public_bytes) != 32 or len(signature) != 64:
            return FAIL
        public_key = Ed25519PublicKey.from_public_bytes(public_bytes)
        public_key.verify(
            signature,
            TRACE_SIGNATURE_CONTEXT + bytes.fromhex(trace_hash),
        )
        return PASS
    except (
        FileNotFoundError,
        binascii.Error,
        InvalidSignature,
        KeyError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ):
        return FAIL


def _trace_gate(trace: Mapping[str, Any], key: str) -> str:
    gates = trace.get("gate_evidence")
    if not isinstance(gates, dict):
        return UNKNOWN
    value = gates.get(key, "unknown")
    if value is True:
        return PASS
    if value is False:
        return FAIL
    if value == "unknown":
        return UNKNOWN
    return UNKNOWN


def _independent_oracle_status(record: Mapping[str, Any]) -> str:
    if sha256_bytes(PINNED_ORACLE_BYTES) != PINNED_ORACLE_HASH:
        return UNKNOWN
    try:
        if normalize_hash(record["mechanism"]["oracle"]["sha256"]) != PINNED_ORACLE_HASH:
            return FAIL
    except (KeyError, TypeError, ValueError):
        return FAIL
    family = record["problem"]["family"]
    parameters = record["problem"]["generator"]["parameters"]
    result = record["candidate_result"]
    try:
        if family == "PARITY":
            bits = parameters["bits"]
            return PASS if parity_oracle(bits, result["answer"]) else FAIL
        if family == "2-SAT":
            clauses = [tuple(clause) for clause in parameters["clauses"]]
            if result["status"] == "sat":
                assignment_payload = result["answer"]["assignment"]
                assignment = {
                    int(variable): bool(value)
                    for variable, value in assignment_payload.items()
                }
                return PASS if assignment_satisfies_2sat(clauses, assignment) else FAIL
            if result["status"] == "unsat":
                answer = result["answer"]
                return PASS if verify_unsat_certificate(
                    clauses,
                    int(answer["unsat_variable"]),
                    answer["positive_to_negative"],
                    answer["negative_to_positive"],
                ) else FAIL
            return FAIL
    except (KeyError, TypeError, ValueError, IndexError):
        return FAIL
    return UNKNOWN


def _two_sat_candidate_result(parameters: Mapping[str, Any]) -> dict[str, Any]:
    variable_count = int(parameters["variable_count"])
    clauses = [tuple(int(literal) for literal in clause) for clause in parameters["clauses"]]
    solved = solve_2sat(variable_count, clauses)
    if solved.status == "sat":
        answer: dict[str, Any] = {
            "assignment": {
                str(variable): bool(value)
                for variable, value in sorted((solved.assignment or {}).items())
            }
        }
    else:
        answer = {
            "unsat_variable": solved.unsat_variable,
            "positive_to_negative": list(solved.positive_to_negative),
            "negative_to_positive": list(solved.negative_to_positive),
        }
    return {
        "status": solved.status,
        "answer": answer,
        "certificate_refs": [],
        "notes": "Experiment only; no P/NP conclusion.",
    }


def _transition_execution_status(record: Mapping[str, Any]) -> str:
    """Execute pinned semantics and derive both transition digests.

    Returning ``unknown`` for an unsupported mechanism is intentional: it is a
    bounded I0 executable interface, not a universal interpreter.
    """

    try:
        family = record["problem"]["family"]
        parameters = record["problem"]["generator"]["parameters"]
        mechanism = record["mechanism"]
        admissibility = mechanism["admissibility"]
        events = record["events"]
        if len(events) != 2:
            return UNKNOWN

        if family == "PARITY" and mechanism["id"] in {
            "parity-stream",
            "parity-table-family",
        }:
            if sha256_bytes(PINNED_PARITY_RULE_BYTES) != PINNED_PARITY_RULE_HASH:
                return UNKNOWN
            rule_hash = PINNED_PARITY_RULE_HASH
            bits = parameters["bits"]
            if not isinstance(bits, list):
                return FAIL
            if mechanism["id"] == "parity-stream":
                answer = stream_parity(bits).answer
            else:
                answer = TruthTableFamily.build(len(bits)).decide(bits)
            certificate_refs = (
                []
                if admissibility["local_invariant_ref"] is None
                else [admissibility["local_invariant_ref"]]
            )
            expected_result = {
                "status": "complete",
                "answer": answer,
                "certificate_refs": certificate_refs,
                "notes": "Experiment only; no P/NP conclusion.",
            }
            input_payload = {"bits": bits}
            intermediate_payload = {"state": [len(bits), answer]}
            before_representation = "bit-vector"
            computed_representation = "parity-state"
            terminal_representation = "answer-bit"
        elif family == "2-SAT" and mechanism["id"] == "2sat-kosaraju":
            if sha256_bytes(PINNED_TWO_SAT_RULE_BYTES) != PINNED_TWO_SAT_RULE_HASH:
                return UNKNOWN
            rule_hash = PINNED_TWO_SAT_RULE_HASH
            expected_result = _two_sat_candidate_result(parameters)
            input_payload = {
                "variable_count": int(parameters["variable_count"]),
                "clauses": parameters["clauses"],
            }
            intermediate_payload = {
                "state": [
                    "2sat",
                    int(parameters["variable_count"]),
                    expected_result["status"],
                ]
            }
            before_representation = "2cnf"
            computed_representation = "scc-result"
            terminal_representation = "decision-certificate"
        else:
            return UNKNOWN

        for key in ("builder_ref", "step_ref", "decode_ref"):
            if normalize_hash(admissibility[key]) != rule_hash:
                return FAIL
        if admissibility["advice_generator_ref"] is not None and normalize_hash(
            admissibility["advice_generator_ref"]
        ) != rule_hash:
            return FAIL

        expected_input_hash = sha256_bytes(canonical_json_bytes(input_payload))
        expected_intermediate_hash = sha256_bytes(
            canonical_json_bytes(intermediate_payload)
        )
        expected_result_hash = sha256_bytes(canonical_json_bytes(expected_result))
        if normalize_hash(record["problem"]["input_sha256"]) != expected_input_hash:
            return FAIL
        if record["candidate_result"] != expected_result:
            return FAIL

        expected_controls = (
            {
                "seq": 0,
                "kind": "solve",
                "from_state": "start",
                "to_state": "computed",
                "representation_before": before_representation,
                "representation_after": computed_representation,
                "input_sha256": expected_input_hash,
                "output_sha256": expected_intermediate_hash,
                "transition_rule_ref": rule_hash,
                "status": "ok",
                "failure": None,
            },
            {
                "seq": 1,
                "kind": "stop",
                "from_state": "computed",
                "to_state": "terminal",
                "representation_before": computed_representation,
                "representation_after": terminal_representation,
                "input_sha256": expected_intermediate_hash,
                "output_sha256": expected_result_hash,
                "transition_rule_ref": rule_hash,
                "status": "ok",
                "failure": None,
            },
        )
        for event, expected in zip(events, expected_controls):
            for key, expected_value in expected.items():
                actual = event[key]
                if key.endswith("sha256") or key == "transition_rule_ref":
                    actual = normalize_hash(actual)
                if actual != expected_value:
                    return FAIL
        return PASS
    except (KeyError, TypeError, ValueError, IndexError, RuntimeError):
        return FAIL


def _derived_event_counts(events: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    states = {
        state
        for event in events
        for state in (event["from_state"], event["to_state"])
    }
    kinds = [event["kind"] for event in events]
    return {
        "states": len(states),
        "branches": 1 if events else 0,
        "switches": kinds.count("state-switch"),
        "rollbacks": kinds.count("rollback"),
        "reroutes": kinds.count("reroute"),
        "refinements": kinds.count("refine"),
        "restarts": kinds.count("restart"),
        "parallel_workers_peak": 1 if events else 0,
    }


def _resource_derivation_status(
    record: Mapping[str, Any],
    trace: Mapping[str, Any],
    replay: ReplayResult,
    authenticity_status: str,
) -> str:
    """Derive event metrics and authenticate raw sandbox measurements.

    Counts, time, and debt are recomputed from events. Space, description,
    admission-cost, and precision samples are raw measurements; they are
    admitted only when covered by the pinned Ed25519 trace receipt.
    """

    if authenticity_status != PASS:
        return authenticity_status
    if trace.get("measurement_model") != TRACE_MEASUREMENT_MODEL:
        return UNKNOWN
    try:
        ledger = record["ledger"]
        events = record["events"]
        samples = trace["resource_samples"]
        if not isinstance(samples, dict):
            return FAIL
        if ledger["counts"] != _derived_event_counts(events):
            return FAIL
        if samples.get("counts") != ledger["counts"]:
            return FAIL

        time_keys = tuple(ledger["time_ns"].keys())
        folded_time = {key: 0 for key in time_keys}
        for event in events:
            for key in time_keys:
                folded_time[key] += event["time_ns"][key]
        if folded_time != ledger["time_ns"]:
            return FAIL

        for key in (
            "space_bytes",
            "description_bytes",
            "admission_costs",
            "precision",
        ):
            if samples.get(key) != ledger[key]:
                return FAIL
        debt = ledger["semantic_loss_debt"]
        if debt["outstanding"] != replay.outstanding_debt or not replay.ok:
            return FAIL
        return PASS
    except (KeyError, TypeError, ValueError):
        return FAIL


def _replay_trace(
    record: Mapping[str, Any],
    trace: Mapping[str, Any],
    store: ArtifactIndex,
) -> ReplayResult:
    issues: list[ValidationIssue] = []
    events = record["events"]
    trace_events = trace.get("events")
    if trace_events != events:
        issues.append(
            ValidationIssue(
                "replay-events-mismatch",
                "$.trace.events",
                "trace events do not exactly reproduce the record event stream",
            )
        )

    candidate_result = record["candidate_result"]
    trace_output = trace.get("candidate_output")
    if trace_output != candidate_result:
        issues.append(
            ValidationIssue(
                "replay-result-mismatch",
                "$.trace.candidate_output",
                "trace output does not reproduce candidate_result",
            )
        )
    if isinstance(trace_output, dict) and {
        "admission_pass",
        "final_completion",
        "validation_receipt",
    }.intersection(trace_output):
        issues.append(
            ValidationIssue(
                "candidate-self-report",
                "$.trace.candidate_output",
                "candidate output contains an external-validator field",
            )
        )

    certificate_refs = candidate_result["certificate_refs"]
    if trace.get("certificate_refs") != certificate_refs:
        issues.append(
            ValidationIssue(
                "replay-certificate-mismatch",
                "$.trace.certificate_refs",
                "trace certificate refs differ from candidate_result",
            )
        )
    for reference in certificate_refs:
        if not store.contains(reference):
            issues.append(
                ValidationIssue(
                    "certificate-unresolved",
                    "$.candidate_result.certificate_refs",
                    f"certificate artifact does not resolve: {reference}",
                )
            )

    if events:
        if events[0]["input_sha256"].removeprefix("sha256:").lower() != normalize_hash(
            record["problem"]["input_sha256"]
        ):
            issues.append(
                ValidationIssue(
                    "replay-input-mismatch",
                    "$.events[0].input_sha256",
                    "first event is not bound to the problem input",
                )
            )
        for index, event in enumerate(events):
            if event["seq"] != index:
                issues.append(
                    ValidationIssue(
                        "replay-sequence",
                        f"$.events[{index}].seq",
                        "event sequence must be contiguous from zero",
                    )
                )
            if index:
                previous = events[index - 1]
                if event["from_state"] != previous["to_state"]:
                    issues.append(
                        ValidationIssue(
                            "replay-state-chain",
                            f"$.events[{index}].from_state",
                            "state chain is discontinuous",
                        )
                    )
                if event["representation_before"] != previous["representation_after"]:
                    issues.append(
                        ValidationIssue(
                            "replay-representation-chain",
                            f"$.events[{index}].representation_before",
                            "representation chain is discontinuous",
                        )
                    )
        terminal = events[-1]
        if terminal["kind"] not in {"stop", "commit"} or terminal["status"] != "ok":
            issues.append(
                ValidationIssue(
                    "replay-terminal",
                    f"$.events[{len(events) - 1}]",
                    "last event must be a successful stop or commit",
                )
            )
        try:
            result_hash = sha256_bytes(canonical_json_bytes(candidate_result))
        except ValueError:
            result_hash = ""
        if normalize_hash(terminal["output_sha256"]) != result_hash:
            issues.append(
                ValidationIssue(
                    "replay-output-hash",
                    f"$.events[{len(events) - 1}].output_sha256",
                    "terminal output hash does not derive candidate_result",
                )
            )
    else:
        issues.append(ValidationIssue("replay-empty", "$.events", "event stream is empty"))

    time_keys = tuple(record["ledger"]["time_ns"].keys())
    folded_time = {key: 0 for key in time_keys}
    for event in events:
        event_total = sum(
            value for key, value in event["time_ns"].items() if key != "total"
        )
        if event["time_ns"]["total"] != event_total:
            issues.append(
                ValidationIssue(
                    "replay-event-time-total",
                    f"$.events[{event['seq']}].time_ns.total",
                    "event total is not the sum of its resource-time components",
                )
            )
        for key in time_keys:
            folded_time[key] += event["time_ns"][key]
    if folded_time != record["ledger"]["time_ns"]:
        issues.append(
            ValidationIssue(
                "replay-time-fold",
                "$.ledger.time_ns",
                "ledger time account is not the sum of event time accounts",
            )
        )

    samples = trace.get("resource_samples")
    if not isinstance(samples, dict):
        samples = {}
    for key in ("space_bytes", "description_bytes", "admission_costs", "precision", "counts"):
        if samples.get(key) != record["ledger"][key]:
            issues.append(
                ValidationIssue(
                    "replay-resource-fold",
                    f"$.ledger.{key}",
                    "ledger field does not match trace resource samples",
                )
            )

    open_debt: set[str] = set()
    ever_added: set[str] = set()
    peak_open = 0
    for event in events:
        for debt_id in event["debt_added"]:
            if debt_id in open_debt:
                issues.append(
                    ValidationIssue(
                        "replay-debt-duplicate",
                        f"$.events[{event['seq']}].debt_added",
                        f"debt {debt_id!r} was already open",
                    )
                )
            open_debt.add(debt_id)
            ever_added.add(debt_id)
        for debt_id in event["debt_retired"]:
            if debt_id not in open_debt:
                issues.append(
                    ValidationIssue(
                        "replay-debt-retire",
                        f"$.events[{event['seq']}].debt_retired",
                        f"debt {debt_id!r} was not open",
                    )
                )
            else:
                open_debt.remove(debt_id)
        peak_open = max(peak_open, len(open_debt))

    debt_ledger = record["ledger"]["semantic_loss_debt"]
    registered_ids = {item["id"] for item in debt_ledger["registered"]}
    if registered_ids != ever_added:
        issues.append(
            ValidationIssue(
                "replay-debt-registry",
                "$.ledger.semantic_loss_debt.registered",
                "registered debt IDs do not equal the event-fold debt IDs",
            )
        )
    if debt_ledger["peak_open"] != peak_open:
        issues.append(
            ValidationIssue(
                "replay-debt-peak",
                "$.ledger.semantic_loss_debt.peak_open",
                "peak_open is not derived from event debt deltas",
            )
        )
    if debt_ledger["outstanding"] != len(open_debt):
        issues.append(
            ValidationIssue(
                "replay-debt-outstanding",
                "$.ledger.semantic_loss_debt.outstanding",
                "outstanding debt is not derived from event debt deltas",
            )
        )

    return ReplayResult(
        ok=not issues,
        outstanding_debt=len(open_debt),
        issues=tuple(issues),
    )


def validate_record(
    record: Mapping[str, Any],
    schema: Mapping[str, Any],
    artifact_root: Path,
    *,
    schema_sha256: str,
) -> ValidationReport:
    structural_errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(record),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if structural_errors:
        return ValidationReport(
            schema_version=record.get("schema_version") if isinstance(record, dict) else None,
            validator_version=VALIDATOR_VERSION,
            structural_ok=False,
            semantic_ok=False,
            admission_pass=None,
            final_completion=None,
            issues=tuple(
                ValidationIssue("schema", _json_path(error.absolute_path), error.message)
                for error in structural_errors
            ),
        )

    issues = _canonical_domain_issues(candidate_projection(record), "$.candidate_projection")
    store = ArtifactIndex(artifact_root)
    receipt = record["validation_receipt"]
    admissibility = record["mechanism"]["admissibility"]
    ledger = record["ledger"]
    candidate_result = record["candidate_result"]

    current_validator_hash = PINNED_VALIDATOR_HASH
    binding_checks = (
        (
            "schema-hash-mismatch",
            "$.validation_receipt.schema_sha256",
            normalize_hash(receipt["schema_sha256"]),
            normalize_hash(schema_sha256),
        ),
        (
            "schema-version-pin-mismatch",
            "$.validation_receipt.schema_sha256",
            normalize_hash(schema_sha256),
            PINNED_SCHEMA_HASH,
        ),
        (
            "validator-version-mismatch",
            "$.validation_receipt.validator_sha256",
            normalize_hash(receipt["validator_sha256"]),
            current_validator_hash,
        ),
        (
            "projection-version-pin-mismatch",
            "$.validation_receipt.projection_spec_sha256",
            normalize_hash(receipt["projection_spec_sha256"]),
            PINNED_PROJECTION_SPEC_HASH,
        ),
        (
            "closure-version-pin-mismatch",
            "$.validation_receipt.artifact_closure_spec_ref",
            normalize_hash(receipt["artifact_closure_spec_ref"]),
            PINNED_CLOSURE_SPEC_HASH,
        ),
        (
            "trace-public-key-pin-mismatch",
            "$.validation_receipt.trace_public_key_ref",
            normalize_hash(receipt["trace_public_key_ref"]),
            PINNED_TRACE_PUBLIC_KEY_HASH,
        ),
    )
    for code, path, actual, expected in binding_checks:
        if actual != expected:
            issues.append(
                ValidationIssue(code, path, f"expected {expected}, record contains {actual}")
            )

    if not receipt["validator_independent"]:
        issues.append(
            ValidationIssue(
                "validator-not-independent",
                "$.validation_receipt.validator_independent",
                "the pinned validator must be independent of candidate execution",
            )
        )

    try:
        projection_spec = store.load_json(receipt["projection_spec_sha256"])
        if projection_spec.get("spec_id") != receipt["projection_spec_id"]:
            issues.append(
                ValidationIssue(
                    "projection-spec-id",
                    "$.validation_receipt.projection_spec_id",
                    "resolved projection spec has a different id",
                )
            )
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        issues.append(
            ValidationIssue(
                "projection-spec-unreadable",
                "$.validation_receipt.projection_spec_sha256",
                str(error),
            )
        )

    try:
        expected_projection_hash = candidate_projection_sha256(record)
    except ValueError:
        expected_projection_hash = ""
    if normalize_hash(receipt["candidate_projection_sha256"]) != expected_projection_hash:
        issues.append(
            ValidationIssue(
                "candidate-projection-mismatch",
                "$.validation_receipt.candidate_projection_sha256",
                "receipt does not bind the canonical candidate projection",
            )
        )

    direct_references = _direct_receipt_reference_set(record)
    closure = _artifact_closure(direct_references, store)
    expected_references = set(closure.references)
    declared_references = {
        normalize_hash(reference) for reference in receipt["resolved_evidence_hashes"]
    }
    if declared_references != expected_references:
        issues.append(
            ValidationIssue(
                "resolved-ref-set-mismatch",
                "$.validation_receipt.resolved_evidence_hashes",
                "receipt must bind the complete operational evidence set",
            )
        )
    unresolved = sorted(
        reference for reference in expected_references if not store.contains(reference)
    )
    for reference in unresolved:
        issues.append(
            ValidationIssue(
                "unresolved-ref",
                "$.validation_receipt.resolved_evidence_hashes",
                f"no trusted artifact has SHA-256 {reference}",
            )
        )
    if closure.status == UNKNOWN:
        refs_resolved_status = UNKNOWN
    elif closure.status == FAIL or unresolved:
        refs_resolved_status = FAIL
    else:
        refs_resolved_status = PASS
    if declared_references != expected_references:
        refs_resolved_status = FAIL

    trace: Mapping[str, Any] = {}
    try:
        trace = store.load_json(receipt["trace_sha256"])
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        issues.append(
            ValidationIssue(
                "trace-unreadable",
                "$.validation_receipt.trace_sha256",
                str(error),
            )
        )

    if trace:
        checks = (
            ("trace-version", "$.trace.trace_version", trace.get("trace_version"), VALIDATOR_VERSION),
            ("trace-producer", "$.trace.producer", trace.get("producer"), TRACE_PRODUCER),
            ("trace-run-id", "$.trace.run_id", trace.get("run_id"), record["run_id"]),
            ("trace-gate-version", "$.trace.gate_version", trace.get("gate_version"), GATE_VERSION),
            (
                "trace-projection-spec",
                "$.trace.projection_spec_id",
                trace.get("projection_spec_id"),
                PROJECTION_SPEC_ID,
            ),
            (
                "trace-record-binding",
                "$.trace.candidate_projection_sha256",
                trace.get("candidate_projection_sha256"),
                expected_projection_hash,
            ),
        )
        for code, path, actual, expected in checks:
            if actual != expected:
                issues.append(ValidationIssue(code, path, f"expected {expected!r}, got {actual!r}"))

    authenticity_status = _trace_authenticity_status(record, store)

    observed_answer_access = trace.get("answer_access", "unknown")
    if receipt["observed_answer_access"] != observed_answer_access:
        issues.append(
            ValidationIssue(
                "answer-access-mismatch",
                "$.validation_receipt.observed_answer_access",
                "receipt must equal the capability trace observation",
            )
        )

    replay = _replay_trace(record, trace, store) if trace else ReplayResult(
        ok=False,
        outstanding_debt=ledger["semantic_loss_debt"]["outstanding"],
        issues=(),
    )
    issues.extend(replay.issues)
    transition_execution_status = (
        _transition_execution_status(record) if trace else UNKNOWN
    )
    resource_derivation_status = (
        _resource_derivation_status(record, trace, replay, authenticity_status)
        if trace
        else UNKNOWN
    )
    context_integrity_ok = not issues

    advice_applicable = (
        admissibility["advice_generator_ref"] is not None
        or ledger["description_bytes"]["advice"] > 0
        or ledger["description_bytes"]["generated_tables"] > 0
    )
    proof_applicable = (
        admissibility["local_invariant_ref"] is not None
        or ledger["description_bytes"]["proof"] > 0
    )
    robust = record["mechanism"]["run_quantifier"] == "robust"
    resource_bounded = record["mechanism"]["resource_regime"] == "resource-bounded"

    provenance_observed = _trace_gate(trace, "provenance_pass")
    expected_gates: dict[str, str] = {
        "uniformity_pass": PASS
        if admissibility["uniform"]
        and admissibility["program_quantifiers"]
        == "exists-one-program-for-all-input-lengths"
        else FAIL,
        "provenance_pass": PASS
        if provenance_observed == PASS and receipt["validator_independent"]
        else provenance_observed,
        "refs_resolved_pass": refs_resolved_status,
        "builder_execution_pass": _trace_gate(trace, "builder_execution_pass"),
        "advice_generation_pass": _trace_gate(trace, "advice_generation_pass")
        if advice_applicable
        else NOT_APPLICABLE,
        "proof_verification_pass": _trace_gate(trace, "proof_verification_pass")
        if proof_applicable
        else NOT_APPLICABLE,
        "advice_budget_pass": _trace_gate(trace, "advice_budget_pass"),
        "answer_access_pass": PASS if observed_answer_access == "none" else FAIL,
        "resource_budget_pass": _trace_gate(trace, "resource_budget_pass")
        if resource_bounded
        else NOT_APPLICABLE,
        "resource_account_pass": PASS
        if replay.ok
        and resource_derivation_status == PASS
        and ledger["resource_account_complete"]
        else FAIL,
        "oracle_free_pass": PASS
        if admissibility["oracle_free"] and observed_answer_access == "none"
        else FAIL,
        "replay_pass": PASS if replay.ok else FAIL,
        "run_class_nonempty": _trace_gate(trace, "run_class_nonempty"),
        "maximality_pass": _trace_gate(trace, "maximality_pass")
        if robust
        else NOT_APPLICABLE,
        "fairness_pass": _trace_gate(trace, "fairness_pass")
        if robust
        else NOT_APPLICABLE,
        "trace_authenticity_pass": authenticity_status,
        "transition_execution_pass": transition_execution_status,
        "resource_derivation_pass": resource_derivation_status,
    }

    for gate in GATE_KEYS:
        if receipt["gates"][gate] != expected_gates[gate]:
            issues.append(
                ValidationIssue(
                    "derived-gate-mismatch",
                    f"$.validation_receipt.gates.{gate}",
                    f"derived {expected_gates[gate]!r}, receipt has {receipt['gates'][gate]!r}",
                )
            )

    standard_specs_ok = (
        receipt["maximal_run_spec_ref"] is None
        and receipt["fairness_spec_ref"] is None
    )
    robust_specs_ok = (
        receipt["maximal_run_spec_ref"] is not None
        and receipt["fairness_spec_ref"] is not None
    )
    specs_ok = robust_specs_ok if robust else standard_specs_ok
    if not specs_ok:
        issues.append(
            ValidationIssue(
                "run-spec-applicability",
                "$.validation_receipt",
                "robust requires maximal/fairness specs; standard requires both null",
            )
        )

    applicable_gates = {
        "uniformity_pass",
        "provenance_pass",
        "refs_resolved_pass",
        "builder_execution_pass",
        "advice_budget_pass",
        "answer_access_pass",
        "resource_account_pass",
        "oracle_free_pass",
        "replay_pass",
        "run_class_nonempty",
        "trace_authenticity_pass",
        "transition_execution_pass",
        "resource_derivation_pass",
    }
    if advice_applicable:
        applicable_gates.add("advice_generation_pass")
    if proof_applicable:
        applicable_gates.add("proof_verification_pass")
    if resource_bounded:
        applicable_gates.add("resource_budget_pass")
    if robust:
        applicable_gates.update({"maximality_pass", "fairness_pass"})

    applicability_ok = all(
        (
            expected_gates[gate] == PASS
            if gate in applicable_gates
            else expected_gates[gate] == NOT_APPLICABLE
        )
        for gate in GATE_KEYS
    )
    expected_admission = (
        receipt["validator_independent"]
        and context_integrity_ok
        and bool(trace)
        and refs_resolved_status == PASS
        and replay.ok
        and specs_ok
        and applicability_ok
    )
    if receipt["admission_pass"] is not expected_admission:
        issues.append(
            ValidationIssue(
                "admission-postcondition-mismatch",
                "$.validation_receipt.admission_pass",
                f"derived {expected_admission}, receipt has {receipt['admission_pass']}",
            )
        )

    correctness = receipt["correctness"]
    oracle_status = _independent_oracle_status(record)
    contract_status = (
        PASS
        if oracle_status == PASS
        and replay.ok
        and authenticity_status == PASS
        and transition_execution_status == PASS
        and resource_derivation_status == PASS
        and replay.outstanding_debt == 0
        else FAIL
    )
    expected_correctness = {
        "oracle_pass": oracle_status,
        "contract_pass": contract_status,
        "complete_pass": PASS
        if replay.ok
        and candidate_result["status"] in {"sat", "unsat", "complete"}
        else FAIL,
        "budget_pass": _trace_gate(trace, "budget_pass")
        if resource_bounded
        else NOT_APPLICABLE,
        "outstanding_loss_debt": replay.outstanding_debt,
    }
    for key, expected in expected_correctness.items():
        if correctness[key] != expected:
            issues.append(
                ValidationIssue(
                    "correctness-receipt-mismatch",
                    f"$.validation_receipt.correctness.{key}",
                    f"derived {expected!r}, receipt has {correctness[key]!r}",
                )
            )

    expected_completion = (
        expected_admission
        and expected_correctness["oracle_pass"] == PASS
        and expected_correctness["contract_pass"] == PASS
        and expected_correctness["complete_pass"] == PASS
        and expected_gates["resource_account_pass"] == PASS
        and replay.outstanding_debt == 0
        and (
            not resource_bounded
            or (
                expected_correctness["budget_pass"] == PASS
                and expected_gates["resource_budget_pass"] == PASS
            )
        )
    )
    if receipt["final_completion"] is not expected_completion:
        issues.append(
            ValidationIssue(
                "completion-postcondition-mismatch",
                "$.validation_receipt.final_completion",
                f"derived {expected_completion}, receipt has {receipt['final_completion']}",
            )
        )

    return ValidationReport(
        schema_version=record["schema_version"],
        validator_version=VALIDATOR_VERSION,
        structural_ok=True,
        semantic_ok=not issues,
        admission_pass=expected_admission,
        final_completion=expected_completion,
        issues=tuple(issues),
    )


def validate_path(
    record_path: Path,
    schema_path: Path,
    artifact_root: Path,
) -> ValidationReport:
    # Parse, hash, and use each caller-supplied file from one byte snapshot.
    schema_bytes = schema_path.read_bytes()
    record_bytes = record_path.read_bytes()
    schema = _load_json_object_bytes(schema_bytes, source=str(schema_path))
    record = _load_json_object_bytes(record_bytes, source=str(record_path))
    return validate_record(
        record,
        schema,
        artifact_root,
        schema_sha256=sha256_bytes(schema_bytes),
    )
