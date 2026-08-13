"""Versioned external semantic validator for run-record schema v0.2.0.

The JSON Schema layer rejects internally contradictory records. This module
independently resolves content, replays the trace, derives every applicable
gate, and checks the external validation receipt.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker

from .oracles import (
    assignment_satisfies_2sat,
    parity_oracle,
    verify_unsat_certificate,
)


VALIDATOR_VERSION = "0.2.0"
GATE_VERSION = "i0-admission-gate/0.2.0"
PROJECTION_SPEC_ID = "urn:evemisslab:pnp-glc:candidate-projection:0.2.0"
TRACE_PRODUCER = "pnp-glc-i0-capability-sandbox"
PASS = "pass"
FAIL = "fail"
UNKNOWN = "unknown"
NOT_APPLICABLE = "not-applicable"
MAX_SAFE_INTEGER = 9_007_199_254_740_991

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
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


PINNED_VALIDATOR_BYTES = Path(__file__).read_bytes()
PINNED_VALIDATOR_HASH = sha256_bytes(PINNED_VALIDATOR_BYTES)


def normalize_hash(reference: str) -> str:
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


def load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON number: {token}")
        ),
    )
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


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
                "candidate projection v0.2.0 admits integers only",
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


def _receipt_reference_set(record: Mapping[str, Any]) -> set[str]:
    receipt = record["validation_receipt"]
    mechanism = record["mechanism"]
    admissibility = mechanism["admissibility"]
    references = {
        receipt["schema_sha256"],
        receipt["validator_sha256"],
        receipt["projection_spec_sha256"],
        receipt["capability_sandbox_ref"],
        receipt["run_spec_ref"],
        receipt["trace_sha256"],
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
            "validator-version-mismatch",
            "$.validation_receipt.validator_sha256",
            normalize_hash(receipt["validator_sha256"]),
            current_validator_hash,
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

    expected_references = _receipt_reference_set(record)
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
    refs_resolved = not unresolved and declared_references == expected_references

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
        "refs_resolved_pass": PASS if refs_resolved else FAIL,
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
        if replay.ok and ledger["resource_account_complete"]
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
        and refs_resolved
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
    schema = load_json(schema_path)
    record = load_json(record_path)
    return validate_record(
        record,
        schema,
        artifact_root,
        schema_sha256=sha256_path(schema_path),
    )
