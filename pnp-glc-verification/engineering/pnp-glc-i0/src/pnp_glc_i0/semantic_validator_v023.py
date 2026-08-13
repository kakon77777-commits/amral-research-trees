"""Versioned external semantic validator for run-record schema v0.2.3.

The JSON Schema layer rejects internally contradictory records. This module
independently resolves a transitive content closure, authenticates the trace,
executes the pinned I0 transition semantics, derives resource folds, checks
every applicable gate, and checks the external validation receipt.

Scope is deliberately bounded: transition execution supports the two PARITY-0
mechanisms and deterministic 2-SAT. Unsupported mechanisms produce ``unknown``
and fail closed. The AI-3 Lean admission kernel is a reference for the
four-valued gate matrix only; it is not a proof of this validator or replay.
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
from .parity import TruthTableFamily, stream_parity, verify_prefix_invariant
from .two_sat import solve_2sat


VALIDATOR_VERSION = "0.2.3"
GATE_VERSION = "i0-admission-gate/0.2.3"
PROJECTION_SPEC_ID = "urn:evemisslab:pnp-glc:candidate-projection:0.2.3"
ARTIFACT_CLOSURE_SPEC_ID = "urn:evemisslab:pnp-glc:artifact-closure:0.2.3"
EVIDENCE_ROLE_SPEC_ID = "urn:evemisslab:pnp-glc:evidence-roles:0.2.3"
TRACE_PRODUCER = "pnp-glc-i0-capability-sandbox"
TRACE_SIGNER_ID = "i0-test-trace-signer-20260809"
TRACE_MEASUREMENT_MODEL = "authenticated-i0-single-worker-linear/0.2.3"
TRACE_SIGNATURE_CONTEXT = b"pnp-glc-i0-trace-v0.2.3\0"
PASS = "pass"
FAIL = "fail"
UNKNOWN = "unknown"
NOT_APPLICABLE = "not-applicable"
MAX_SAFE_INTEGER = 9_007_199_254_740_991

# These literals pin the independently reviewed interface artifacts and code.
# A changed file must produce a new validator version rather than silently
# changing the meaning of this candidate.
PINNED_SCHEMA_HASH = "dce6f0c95b95d9377ba7af9f9537bdc277cdf0e68ce74b9ad3bf83db2b011895"
PINNED_PROJECTION_SPEC_HASH = "35d21683177a849fd8ad331451a818be1ee2e7605cf4b11f54ff5cccfed69251"
PINNED_CLOSURE_SPEC_HASH = "4e978ef2a2df0fed51e94e89e6305294a9b7965ad86ab6888ee857da4854643b"
PINNED_ROLE_SPEC_HASH = "fb5c3be06ba68716492b96664bf8fd5c6154c1159025e5f1d278fad1c0b3cbfb"
PINNED_TRACE_PUBLIC_KEY_HASH = "7ee6a19c624608b63f5fd8a6783dca38cd97c3415eee1ca3fa5456e14cf7fbc4"
PINNED_SANDBOX_HASH = "eaea725eff69aa9952222acd2d195862d05778f33e642220746c4eae0c1aba4b"
PINNED_RUN_STANDARD_HASH = "eaaf66a382ec890ddc7be9330f605d3db38b6f4b23d1827a0f13563e8dc4089b"
PINNED_RUN_ROBUST_HASH = "c3d2ff9b4c8ebf98b5dd84597116aeff85cd05b06bcd82b005e5c37810ac5ee9"
PINNED_MAXIMAL_HASH = "36b26d735437e6b88e24d083e1a1e31d6249029c72ab82cc00cc9a4de6192efa"
PINNED_FAIRNESS_HASH = "b8eac472f05307e55a594b637b0a9d7bcdbcc8d1744df4ee01b480b556c1ce6d"
PINNED_PARITY_INVARIANT_HASH = "969f90f5a64434e9260915d974f33592aaf08445ba5646e9b763dfde4ca86162"
PINNED_PARITY_CONTRACT_HASH = "6022e93777a987bf4fa20b37fc0c7ce6e8764d6f2fa6a0bd1b096548b388b19c"
PINNED_TWO_SAT_CONTRACT_HASH = "2a35af1bd8b1c1df3e45e3252a75975bc4f59ba23ea2635ccceff5192bee423d"
PINNED_PARITY_RULE_HASH = "bdfb4cd28a8730aa99b058dd6567027b98f0125fbf503a42e0fb895c686aedef"
PINNED_ORACLE_HASH = "c8c5f6a0c132b11c56fd7964b737c1eb4f0b6a8674c7de8adcda50ca4b54efce"
PINNED_TWO_SAT_RULE_HASH = "ed1028c0263dc5a69864fb42d02ada9756b40ee51149d9dd376dd206622a8971"

EDGE_RELATIONS: Mapping[str, Mapping[str, str]] = {
    "candidate-projection-spec": {},
    "artifact-closure-spec": {},
    "evidence-role-spec": {},
    "ed25519-public-key": {},
    "capability-trace": {},
    "capability-sandbox": {"legacy-policy-source": "opaque-content"},
    "run-spec": {
        "legacy-run-source": "opaque-content",
        "maximality-spec": "maximal-run-spec",
        "fairness-spec": "fairness-spec",
    },
    "maximal-run-spec": {"legacy-maximal-source": "opaque-content"},
    "fairness-spec": {"legacy-fairness-source": "opaque-content"},
    "invariant-spec": {"legacy-invariant-source": "opaque-content"},
    "correctness-contract": {
        "oracle-source": "opaque-content",
        "invariant-spec": "invariant-spec",
    },
    "trace-authenticity-receipt": {
        "trace": "capability-trace",
        "public-key": "ed25519-public-key",
    },
}

SANDBOX_RESOURCE_BUDGET: Mapping[str, int] = {
    "max_total_time_ns": 1_000_000_000,
    "max_peak_space_bytes": 10_000_000,
    "max_description_bytes": 10_000_000,
    "max_advice_bytes": 0,
    "parallel_workers_peak": 1,
}

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
    artifact_types: Mapping[str, str]


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


def _parse_json_int(token: str) -> int:
    if token == "-0":
        raise ValueError("negative zero is outside the v0.2.3 canonical domain")
    return int(token)


def _load_json_object_bytes(data: bytes, *, source: str) -> Mapping[str, Any]:
    value = json.loads(
        data.decode("utf-8"),
        object_pairs_hook=_unique_object,
        parse_int=_parse_json_int,
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
                    "candidate projection v0.2.3 admits integers only",
                )
        )
        return issues
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            issues.append(
                ValidationIssue(
                    "canonical-unicode-scalar",
                    path,
                    "string contains an unpaired UTF-16 surrogate, not a Unicode scalar value",
                )
            )
            return issues
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
            if any(0xD800 <= ord(character) <= 0xDFFF for character in key):
                issues.append(
                    ValidationIssue(
                        "canonical-key-scalar",
                        f"{path}.{key!r}",
                        "object key contains an unpaired UTF-16 surrogate",
                    )
                )
                continue
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
            parse_int=_parse_json_int,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ValueError(f"non-finite JSON number: {token}")
            ),
        )
        if not isinstance(value, dict):
            raise ValueError(f"expected JSON object: {path}")
        return value


def _rule_hash_for_record(record: Mapping[str, Any]) -> str | None:
    family = record["problem"]["family"]
    mechanism_id = record["mechanism"]["id"]
    if family == "PARITY" and mechanism_id in {"parity-stream", "parity-table-family"}:
        return PINNED_PARITY_RULE_HASH
    if family == "2-SAT" and mechanism_id == "2sat-kosaraju":
        return PINNED_TWO_SAT_RULE_HASH
    return None


def _actual_operational_reference_map(record: Mapping[str, Any]) -> dict[str, str]:
    receipt = record["validation_receipt"]
    mechanism = record["mechanism"]
    admissibility = mechanism["admissibility"]
    references: dict[str, str] = {
        "schema": receipt["schema_sha256"],
        "validator": receipt["validator_sha256"],
        "projection-spec": receipt["projection_spec_sha256"],
        "closure-spec": receipt["artifact_closure_spec_ref"],
        "role-spec": receipt["evidence_role_spec_ref"],
        "capability-sandbox": receipt["capability_sandbox_ref"],
        "run-spec": receipt["run_spec_ref"],
        "trace-public-key": receipt["trace_public_key_ref"],
        "builder": admissibility["builder_ref"],
        "step": admissibility["step_ref"],
        "decode": admissibility["decode_ref"],
        "oracle": mechanism["oracle"]["sha256"],
        "contract": record["problem"]["contract"]["sha256"],
    }
    optional_receipt = {
        "maximal-run-spec": receipt["maximal_run_spec_ref"],
        "fairness-spec": receipt["fairness_spec_ref"],
    }
    optional_mechanism = {
        "advice-generator": admissibility["advice_generator_ref"],
        "local-invariant": admissibility["local_invariant_ref"],
    }
    for role, reference in {**optional_receipt, **optional_mechanism}.items():
        if reference is not None:
            references[role] = reference
    for index, event in enumerate(record["events"]):
        if event["transition_rule_ref"] is not None:
            references[f"event:{index}:transition-rule"] = event["transition_rule_ref"]
        if event["invariant_ref"] is not None:
            references[f"event:{index}:invariant"] = event["invariant_ref"]
    for index, reference in enumerate(record["candidate_result"]["certificate_refs"]):
        references[f"certificate:{index}"] = reference
    return {role: normalize_hash(reference) for role, reference in references.items()}


def _expected_operational_reference_map(record: Mapping[str, Any]) -> dict[str, str]:
    robust = record["mechanism"]["run_quantifier"] == "robust"
    rule_hash = _rule_hash_for_record(record)
    if rule_hash is None:
        return {}
    family = record["problem"]["family"]
    mechanism_id = record["mechanism"]["id"]
    references = {
        "schema": PINNED_SCHEMA_HASH,
        "validator": PINNED_VALIDATOR_HASH,
        "projection-spec": PINNED_PROJECTION_SPEC_HASH,
        "closure-spec": PINNED_CLOSURE_SPEC_HASH,
        "role-spec": PINNED_ROLE_SPEC_HASH,
        "capability-sandbox": PINNED_SANDBOX_HASH,
        "run-spec": PINNED_RUN_ROBUST_HASH if robust else PINNED_RUN_STANDARD_HASH,
        "trace-public-key": PINNED_TRACE_PUBLIC_KEY_HASH,
        "builder": rule_hash,
        "step": rule_hash,
        "decode": rule_hash,
        "oracle": PINNED_ORACLE_HASH,
        "contract": (
            PINNED_PARITY_CONTRACT_HASH
            if family == "PARITY"
            else PINNED_TWO_SAT_CONTRACT_HASH
        ),
    }
    if robust:
        references["maximal-run-spec"] = PINNED_MAXIMAL_HASH
        references["fairness-spec"] = PINNED_FAIRNESS_HASH
    if mechanism_id == "parity-table-family":
        references["advice-generator"] = rule_hash
    if mechanism_id == "parity-stream":
        references["local-invariant"] = PINNED_PARITY_INVARIANT_HASH
    for index, _event in enumerate(record["events"]):
        references[f"event:{index}:transition-rule"] = rule_hash
        if mechanism_id == "parity-stream":
            references[f"event:{index}:invariant"] = PINNED_PARITY_INVARIANT_HASH
    if mechanism_id == "parity-stream":
        references["certificate:0"] = PINNED_PARITY_INVARIANT_HASH
    return references


def _canonical_operational_reference_map(
    references: Mapping[str, str]
) -> dict[str, str]:
    return {
        role: f"sha256:{normalize_hash(reference)}"
        for role, reference in sorted(references.items())
    }


def operational_reference_map_sha256(references: Mapping[str, str]) -> str:
    canonical = _canonical_operational_reference_map(references)
    return sha256_bytes(canonical_json_bytes(canonical))


def _direct_role_expected_type(role: str) -> str | None:
    exact = {
        "schema": "opaque-content",
        "validator": "opaque-content",
        "projection-spec": "candidate-projection-spec",
        "closure-spec": "artifact-closure-spec",
        "role-spec": "evidence-role-spec",
        "capability-sandbox": "capability-sandbox",
        "run-spec": "run-spec",
        "maximal-run-spec": "maximal-run-spec",
        "fairness-spec": "fairness-spec",
        "trace-public-key": "ed25519-public-key",
        "trace": "capability-trace",
        "trace-authenticity": "trace-authenticity-receipt",
        "builder": "opaque-content",
        "step": "opaque-content",
        "decode": "opaque-content",
        "advice-generator": "opaque-content",
        "oracle": "opaque-content",
        "contract": "correctness-contract",
        "local-invariant": "invariant-spec",
    }
    if role in exact:
        return exact[role]
    if role.startswith("event:") and role.endswith(":transition-rule"):
        return "opaque-content"
    if role.startswith("event:") and role.endswith(":invariant"):
        return "invariant-spec"
    if role.startswith("certificate:"):
        return "invariant-spec"
    return None


def _direct_receipt_reference_map(record: Mapping[str, Any]) -> dict[str, str]:
    receipt = record["validation_receipt"]
    references = _actual_operational_reference_map(record)
    references.update(
        {
            "trace": normalize_hash(receipt["trace_sha256"]),
            "trace-authenticity": normalize_hash(
                receipt["trace_authenticity_ref"]
            ),
        }
    )
    return references


def _direct_receipt_reference_set(record: Mapping[str, Any]) -> set[str]:
    """Compatibility projection for fixture tooling; roles are retained above."""

    return set(_direct_receipt_reference_map(record).values())


def _envelope_shape(
    envelope: Any,
) -> tuple[str, str, str, list[Mapping[str, Any]]] | None:
    """Validate the spec-independent envelope shape before spec dispatch.

    This deliberately does not require ``artifact_type`` or ``version`` to be
    supported. A complete future envelope is UNKNOWN; a malformed future
    envelope is FAIL. Generic role-bearing edge syntax belongs to the base
    shape, while parent/role/child semantics are checked only for the supported
    closure specification.
    """

    if not isinstance(envelope, dict):
        return None
    spec_id = envelope.get("spec_id")
    artifact_type = envelope.get("artifact_type")
    version = envelope.get("version")
    edges = envelope.get("edges")
    if (
        not isinstance(spec_id, str)
        or not spec_id
        or not isinstance(artifact_type, str)
        or not artifact_type
        or not isinstance(version, str)
        or not version
        or not isinstance(edges, list)
    ):
        return None

    edge_roles: set[str] = set()
    for edge in edges:
        if not isinstance(edge, dict) or set(edge) != {
            "role",
            "expected_type",
            "sha256",
        }:
            return None
        role = edge["role"]
        expected_type = edge["expected_type"]
        if (
            not isinstance(role, str)
            or not role
            or not isinstance(expected_type, str)
            or not expected_type
            or role in edge_roles
        ):
            return None
        try:
            normalize_hash(edge["sha256"])
        except ValueError:
            return None
        edge_roles.add(role)
    return spec_id, artifact_type, version, edges


def _artifact_closure(
    direct_references: Mapping[str, str] | Iterable[str], store: ArtifactIndex
) -> ClosureResult:
    """Resolve and type-check the role-bearing fixed-point closure."""

    references: set[str] = set()
    artifact_types: dict[str, str] = {}
    expected_types: dict[str, set[str]] = {}
    status = PASS
    if isinstance(direct_references, Mapping):
        queue: deque[tuple[str, str | None]] = deque()
        for role, reference in direct_references.items():
            expected_type = _direct_role_expected_type(role)
            if expected_type is None:
                status = FAIL
            queue.append((normalize_hash(reference), expected_type))
    else:
        queue = deque((normalize_hash(ref), None) for ref in direct_references)
    while queue:
        reference, expected_type = queue.popleft()
        if expected_type is not None:
            expected_types.setdefault(reference, set()).add(expected_type)
            if len(expected_types[reference]) > 1:
                status = FAIL
        if reference in artifact_types:
            if expected_type is not None and artifact_types[reference] != expected_type:
                status = FAIL
            continue
        if reference in references:
            continue
        references.add(reference)
        snapshots = store.resolve(reference)
        if not snapshots:
            status = FAIL
            continue
        _, snapshot = snapshots[0]
        value: Any = None
        try:
            value = json.loads(
                snapshot.decode("utf-8"),
                object_pairs_hook=_unique_object,
                parse_int=_parse_json_int,
                parse_constant=lambda token: (_ for _ in ()).throw(
                    ValueError(f"non-finite JSON number: {token}")
                ),
            )
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
            artifact_types[reference] = "opaque-content"
            if expected_type not in (None, "opaque-content"):
                status = FAIL
            continue
        if not isinstance(value, dict) or "artifact_envelope" not in value:
            artifact_types[reference] = "opaque-content"
            if expected_type not in (None, "opaque-content"):
                status = FAIL
            continue
        shape = _envelope_shape(value["artifact_envelope"])
        if shape is None:
            status = FAIL
            artifact_types[reference] = "invalid-envelope"
            continue
        envelope_spec_id, artifact_type, version, edges = shape
        if envelope_spec_id != ARTIFACT_CLOSURE_SPEC_ID:
            if status != FAIL:
                status = UNKNOWN
            artifact_types[reference] = "unknown-envelope"
            continue
        if version != VALIDATOR_VERSION or artifact_type not in EDGE_RELATIONS:
            status = FAIL
            artifact_types[reference] = "invalid-envelope"
            continue
        artifact_types[reference] = artifact_type
        if expected_type is not None and artifact_type != expected_type:
            status = FAIL
        edge_roles: set[str] = set()
        relation = EDGE_RELATIONS[artifact_type]
        for edge in edges:
            role = edge["role"]
            child_type = edge["expected_type"]
            if role in edge_roles or relation.get(role) != child_type:
                status = FAIL
                continue
            edge_roles.add(role)
            try:
                child_hash = normalize_hash(edge["sha256"])
            except ValueError:
                status = FAIL
                continue
            queue.append((child_hash, child_type))
    return ClosureResult(frozenset(references), status, artifact_types)


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
            or envelope.get("version") != VALIDATOR_VERSION
        ):
            return FAIL
        edges = envelope.get("edges")
        if not isinstance(edges, list):
            return FAIL
        expected_edges = {
            (
                "trace",
                "capability-trace",
                trace_hash,
            ),
            (
                "public-key",
                "ed25519-public-key",
                public_key_hash,
            ),
        }
        try:
            actual_edges = {
                (
                    edge["role"],
                    edge["expected_type"],
                    normalize_hash(edge["sha256"]),
                )
                for edge in edges
                if isinstance(edge, dict)
                and set(edge) == {"role", "expected_type", "sha256"}
            }
        except (KeyError, TypeError, ValueError):
            return FAIL
        if len(actual_edges) != len(edges) or actual_edges != expected_edges:
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
            or key_envelope.get("version") != VALIDATOR_VERSION
            or key_envelope.get("edges") != []
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


def _operational_reference_status(
    record: Mapping[str, Any],
    trace: Mapping[str, Any],
    store: ArtifactIndex,
    closure: ClosureResult,
) -> tuple[str, tuple[ValidationIssue, ...]]:
    """Bind field roles to exact I0 artifacts and to the signed trace map."""

    issues: list[ValidationIssue] = []
    try:
        actual = _actual_operational_reference_map(record)
        expected = _expected_operational_reference_map(record)
    except (KeyError, TypeError, ValueError) as error:
        return FAIL, (
            ValidationIssue(
                "operational-reference-map",
                "$.validation_receipt",
                f"cannot derive operational reference map: {error}",
            ),
        )
    if not expected:
        return UNKNOWN, (
            ValidationIssue(
                "unsupported-operational-family",
                "$.mechanism.id",
                "no pinned v0.2.3 operational role map exists for this family/mechanism",
            ),
        )

    all_roles = sorted(set(actual) | set(expected))
    for role in all_roles:
        if actual.get(role) != expected.get(role):
            issues.append(
                ValidationIssue(
                    "operational-role-binding",
                    f"$.operational_reference_map.{role}",
                    f"expected {expected.get(role)!r}, resolved {actual.get(role)!r}",
                )
            )

    expected_canonical = _canonical_operational_reference_map(expected)
    if trace.get("operational_reference_map") != expected_canonical:
        issues.append(
            ValidationIssue(
                "signed-operational-map-mismatch",
                "$.trace.operational_reference_map",
                "signed trace map does not equal the validator-derived role map",
            )
        )
    expected_map_hash = operational_reference_map_sha256(expected)
    try:
        receipt_map_hash = normalize_hash(
            record["validation_receipt"]["operational_reference_map_sha256"]
        )
    except (KeyError, TypeError, ValueError):
        receipt_map_hash = ""
    if receipt_map_hash != expected_map_hash:
        issues.append(
            ValidationIssue(
                "operational-map-hash-mismatch",
                "$.validation_receipt.operational_reference_map_sha256",
                "receipt does not bind the validator-derived role map",
            )
        )

    direct = _direct_receipt_reference_map(record)
    for role, reference in direct.items():
        expected_type = _direct_role_expected_type(role)
        actual_type = closure.artifact_types.get(normalize_hash(reference))
        if expected_type is None or actual_type != expected_type:
            issues.append(
                ValidationIssue(
                    "direct-role-type",
                    f"$.operational_reference_map.{role}",
                    f"expected artifact type {expected_type!r}, resolved {actual_type!r}",
                )
            )

    def resolved(role: str) -> Mapping[str, Any] | None:
        reference = expected.get(role)
        if reference is None:
            return None
        try:
            return store.load_json(reference)
        except (FileNotFoundError, TypeError, ValueError, json.JSONDecodeError) as error:
            issues.append(
                ValidationIssue(
                    "typed-artifact-unreadable",
                    f"$.operational_reference_map.{role}",
                    str(error),
                )
            )
            return None

    projection = resolved("projection-spec")
    closure_spec = resolved("closure-spec")
    role_spec = resolved("role-spec")
    sandbox = resolved("capability-sandbox")
    run_spec = resolved("run-spec")
    contract = resolved("contract")
    public_key = resolved("trace-public-key")

    if projection is not None and (
        projection.get("spec_id") != PROJECTION_SPEC_ID
        or projection.get("version") != VALIDATOR_VERSION
    ):
        issues.append(
            ValidationIssue(
                "projection-spec-semantics",
                "$.validation_receipt.projection_spec_sha256",
                "projection spec id/version does not match v0.2.3",
            )
        )
    if closure_spec is not None and (
        closure_spec.get("spec_id") != ARTIFACT_CLOSURE_SPEC_ID
        or closure_spec.get("version") != VALIDATOR_VERSION
    ):
        issues.append(
            ValidationIssue(
                "closure-spec-semantics",
                "$.validation_receipt.artifact_closure_spec_ref",
                "closure spec id/version does not match v0.2.3",
            )
        )
    expected_edges = {
        parent: dict(relation)
        for parent, relation in EDGE_RELATIONS.items()
        if relation
    }
    if role_spec is not None and (
        role_spec.get("spec_id") != EVIDENCE_ROLE_SPEC_ID
        or role_spec.get("version") != VALIDATOR_VERSION
        or role_spec.get("allowed_edges") != expected_edges
    ):
        issues.append(
            ValidationIssue(
                "role-spec-semantics",
                "$.validation_receipt.evidence_role_spec_ref",
                "role spec id/version/edge relation differs from the pinned validator",
            )
        )
    if sandbox is not None and (
        sandbox.get("producer") != TRACE_PRODUCER
        or sandbox.get("measurement_model") != TRACE_MEASUREMENT_MODEL
        or sandbox.get("resource_budget") != dict(SANDBOX_RESOURCE_BUDGET)
    ):
        issues.append(
            ValidationIssue(
                "sandbox-semantics",
                "$.validation_receipt.capability_sandbox_ref",
                "sandbox producer, measurement model, or budget is not pinned",
            )
        )

    mode = record["mechanism"]["run_quantifier"]
    if run_spec is not None and (
        run_spec.get("mode") != mode
        or run_spec.get("nonempty_witness")
        != "successful start-to-terminal executable trace"
    ):
        issues.append(
            ValidationIssue(
                "run-spec-semantics",
                "$.validation_receipt.run_spec_ref",
                "run spec mode or executable nonempty witness is wrong",
            )
        )
    if mode == "robust":
        maximal = resolved("maximal-run-spec")
        fairness = resolved("fairness-spec")
        if maximal is None or maximal.get("mode") != "robust":
            issues.append(
                ValidationIssue(
                    "maximal-spec-semantics",
                    "$.validation_receipt.maximal_run_spec_ref",
                    "robust maximal-run spec is missing or has the wrong mode",
                )
            )
        if fairness is None or fairness.get("mode") != "robust":
            issues.append(
                ValidationIssue(
                    "fairness-spec-semantics",
                    "$.validation_receipt.fairness_spec_ref",
                    "robust fairness spec is missing or has the wrong mode",
                )
            )

    family = record["problem"]["family"]
    contract_id = "I0-PARITY" if family == "PARITY" else "I0-2SAT"
    if contract is not None and (
        contract.get("family") != family
        or contract.get("contract_id") != contract_id
        or record["problem"]["contract"].get("completion_requirements")
        != contract.get("completion_requirements")
    ):
        issues.append(
            ValidationIssue(
                "contract-family-binding",
                "$.problem.contract.sha256",
                "contract artifact family/id/requirements do not match the record",
            )
        )
    if public_key is not None and (
        public_key.get("algorithm") != "Ed25519"
        or public_key.get("key_id") != TRACE_SIGNER_ID
    ):
        issues.append(
            ValidationIssue(
                "public-key-semantics",
                "$.validation_receipt.trace_public_key_ref",
                "public key algorithm/key id differs from the pinned signer",
            )
        )

    mechanism_id = record["mechanism"]["id"]
    if mechanism_id == "parity-stream":
        invariant = resolved("local-invariant")
        if invariant is None or (
            invariant.get("family") != "PARITY"
            or invariant.get("mechanism") != "parity-stream"
        ):
            issues.append(
                ValidationIssue(
                    "invariant-family-binding",
                    "$.mechanism.admissibility.local_invariant_ref",
                    "invariant artifact is not bound to uniform streaming PARITY",
                )
            )

    declaration_checks = (
        (record.get("schema_version"), VALIDATOR_VERSION),
        (record["mechanism"].get("version"), VALIDATOR_VERSION),
        (record["mechanism"]["oracle"].get("version"), VALIDATOR_VERSION),
        (record["problem"]["generator"].get("version"), VALIDATOR_VERSION),
        (record["problem"]["contract"].get("version"), VALIDATOR_VERSION),
        (record["problem"]["contract"].get("id"), contract_id),
        (record["mechanism"]["oracle"].get("independent"), True),
        (record["mechanism"]["admissibility"].get("finite_precision"), True),
        (record["mechanism"]["admissibility"].get("randomness"), "none"),
        (record["mechanism"]["admissibility"].get("interaction"), "none"),
        (
            record["mechanism"]["admissibility"].get("parallelism"),
            "single worker",
        ),
    )
    if any(actual_value != expected_value for actual_value, expected_value in declaration_checks):
        issues.append(
            ValidationIssue(
                "candidate-version-family-binding",
                "$.problem",
                "candidate declarations do not match the pinned v0.2.3 family interface",
            )
        )

    issues.extend(_family_context_issues(record, trace, family, mechanism_id))

    trace_envelope = trace.get("artifact_envelope")
    if not isinstance(trace_envelope, dict) or (
        trace_envelope.get("spec_id") != ARTIFACT_CLOSURE_SPEC_ID
        or trace_envelope.get("artifact_type") != "capability-trace"
        or trace_envelope.get("version") != VALIDATOR_VERSION
        or trace_envelope.get("edges") != []
    ):
        issues.append(
            ValidationIssue(
                "trace-envelope-semantics",
                "$.trace.artifact_envelope",
                "trace is not a v0.2.3 capability-trace envelope",
            )
        )

    return (FAIL if issues else PASS), tuple(issues)


def _family_context_issues(
    record: Mapping[str, Any],
    trace: Mapping[str, Any],
    family: str,
    mechanism_id: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        parameters = record["problem"]["generator"]["parameters"]
        size = record["problem"]["size"]
        description = record["ledger"]["description_bytes"]
        if family == "PARITY":
            expected_size = {"n": len(parameters["bits"])}
            expected_axes = [
                {"name": "n", "value": len(parameters["bits"]), "unit": "bits"},
                {
                    "name": "advice",
                    "value": description["advice"],
                    "unit": "bytes",
                },
            ]
            expected_access = (
                "truth-table"
                if mechanism_id == "parity-table-family"
                else "none"
            )
        else:
            expected_size = {
                "n": int(parameters["variable_count"]),
                "m": len(parameters["clauses"]),
            }
            expected_axes = [
                {
                    "name": "variables",
                    "value": int(parameters["variable_count"]),
                    "unit": "variables",
                },
                {
                    "name": "clauses",
                    "value": len(parameters["clauses"]),
                    "unit": "clauses",
                },
            ]
            expected_access = "none"
        if size != expected_size:
            issues.append(
                ValidationIssue(
                    "problem-size-derivation",
                    "$.problem.size",
                    "problem size is not derived from the pinned input parameters",
                )
            )
        if record["failure_frontier"].get("axes") != expected_axes:
            issues.append(
                ValidationIssue(
                    "failure-frontier-derivation",
                    "$.failure_frontier.axes",
                    "failure-frontier axes are not derived from the instance and ledger",
                )
            )
        declared_access = record["mechanism"]["admissibility"].get(
            "declared_answer_access"
        )
        observed_access = trace.get("answer_access")
        if declared_access != expected_access or observed_access != expected_access:
            issues.append(
                ValidationIssue(
                    "answer-access-family-binding",
                    "$.mechanism.admissibility.declared_answer_access",
                    "declared and signed observed answer access must match the pinned mechanism",
                )
            )
    except (KeyError, TypeError, ValueError, OverflowError):
        issues.append(
            ValidationIssue(
                "problem-context-unreadable",
                "$.problem.generator.parameters",
                "pinned family parameters are missing or ill-typed",
            )
        )
    return issues


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


def _uniformity_status(record: Mapping[str, Any]) -> str:
    try:
        mechanism_id = record["mechanism"]["id"]
        admissibility = record["mechanism"]["admissibility"]
        actual = (
            admissibility["uniform"],
            admissibility["program_quantifiers"],
        )
        if mechanism_id in {"parity-stream", "2sat-kosaraju"}:
            return (
                PASS
                if actual
                == (True, "exists-one-program-for-all-input-lengths")
                else FAIL
            )
        if mechanism_id == "parity-table-family":
            return (
                FAIL
                if actual == (False, "for-all-lengths-exists-program")
                else FAIL
            )
        return UNKNOWN
    except (KeyError, TypeError):
        return FAIL


def _advice_generation_status(record: Mapping[str, Any]) -> str:
    try:
        if record["mechanism"]["id"] != "parity-table-family":
            return NOT_APPLICABLE
        bits = record["problem"]["generator"]["parameters"]["bits"]
        table = TruthTableFamily.build(len(bits))
        description = record["ledger"]["description_bytes"]
        generation = record["ledger"]["admission_costs"]["advice_generation"]
        if (
            description["advice"] != table.advice_bytes
            or description["generated_tables"] != table.advice_bytes
            or generation["peak_output_bytes"] != table.advice_bytes
        ):
            return FAIL
        return PASS
    except (KeyError, TypeError, ValueError):
        return FAIL


def _proof_verification_status(record: Mapping[str, Any]) -> str:
    try:
        if record["mechanism"]["id"] != "parity-stream":
            return NOT_APPLICABLE
        bits = record["problem"]["generator"]["parameters"]["bits"]
        result = stream_parity(bits)
        return PASS if verify_prefix_invariant(bits, result) else FAIL
    except (KeyError, TypeError, ValueError):
        return FAIL


def _advice_budget_status(record: Mapping[str, Any]) -> str:
    try:
        ledger = record["ledger"]
        return (
            PASS
            if ledger["description_bytes"]["advice"]
            <= SANDBOX_RESOURCE_BUDGET["max_advice_bytes"]
            and ledger["admission_costs"]["advice_generation"][
                "peak_output_bytes"
            ]
            <= SANDBOX_RESOURCE_BUDGET["max_advice_bytes"]
            else FAIL
        )
    except (KeyError, TypeError):
        return FAIL


def _resource_budget_status(record: Mapping[str, Any]) -> str:
    if record["mechanism"]["resource_regime"] != "resource-bounded":
        return NOT_APPLICABLE
    try:
        ledger = record["ledger"]
        description_total = sum(ledger["description_bytes"].values())
        within = (
            ledger["time_ns"]["total"]
            <= SANDBOX_RESOURCE_BUDGET["max_total_time_ns"]
            and ledger["space_bytes"]["peak"]
            <= SANDBOX_RESOURCE_BUDGET["max_peak_space_bytes"]
            and description_total
            <= SANDBOX_RESOURCE_BUDGET["max_description_bytes"]
            and ledger["counts"]["parallel_workers_peak"]
            <= SANDBOX_RESOURCE_BUDGET["parallel_workers_peak"]
        )
        return PASS if within else FAIL
    except (KeyError, TypeError):
        return FAIL


def _run_gate_status(
    record: Mapping[str, Any], transition_execution_status: str
) -> tuple[str, str, str]:
    if transition_execution_status != PASS:
        status = transition_execution_status
        robust = record["mechanism"]["run_quantifier"] == "robust"
        return (
            status,
            status if robust else NOT_APPLICABLE,
            status if robust else NOT_APPLICABLE,
        )
    try:
        events = record["events"]
        terminal = bool(events) and events[-1]["to_state"] == "terminal"
        if not terminal:
            return FAIL, FAIL, FAIL
        if record["mechanism"]["run_quantifier"] == "robust":
            # I0 admits one deterministic finite run. Successful pinned replay
            # reaches terminal, so the singleton family is nonempty, maximal,
            # and fair under the two pinned bounded-I0 specifications.
            return PASS, PASS, PASS
        return PASS, NOT_APPLICABLE, NOT_APPLICABLE
    except (KeyError, TypeError, IndexError):
        return FAIL, FAIL, FAIL


def _provenance_status(
    trace: Mapping[str, Any],
    authenticity_status: str,
    operational_status: str,
    validator_independent: bool,
) -> str:
    if authenticity_status == FAIL or operational_status == FAIL:
        return FAIL
    if authenticity_status == UNKNOWN or operational_status == UNKNOWN:
        return UNKNOWN
    observed = _trace_gate(trace, "provenance_pass")
    if observed != PASS:
        return observed
    return PASS if validator_independent else FAIL


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


def _validate_parsed_record(
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
            "role-spec-version-pin-mismatch",
            "$.validation_receipt.evidence_role_spec_ref",
            normalize_hash(receipt["evidence_role_spec_ref"]),
            PINNED_ROLE_SPEC_HASH,
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

    direct_references = _direct_receipt_reference_map(record)
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
    operational_status, operational_issues = _operational_reference_status(
        record, trace, store, closure
    )
    issues.extend(operational_issues)
    if operational_status == FAIL:
        refs_resolved_status = FAIL
    elif operational_status == UNKNOWN and refs_resolved_status == PASS:
        refs_resolved_status = UNKNOWN

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

    uniformity_status = _uniformity_status(record)
    advice_generation_status = _advice_generation_status(record)
    proof_verification_status = _proof_verification_status(record)
    advice_budget_status = _advice_budget_status(record)
    resource_budget_status = _resource_budget_status(record)
    run_nonempty_status, maximality_status, fairness_status = _run_gate_status(
        record, transition_execution_status
    )
    provenance_status = _provenance_status(
        trace,
        authenticity_status,
        operational_status,
        receipt["validator_independent"],
    )
    declared_answer_access = admissibility["declared_answer_access"]
    answer_access_status = (
        authenticity_status
        if observed_answer_access == declared_answer_access == "none"
        else FAIL
    )
    oracle_free_status = (
        answer_access_status if admissibility["oracle_free"] else FAIL
    )
    expected_gates: dict[str, str] = {
        "uniformity_pass": uniformity_status,
        "provenance_pass": provenance_status,
        "refs_resolved_pass": refs_resolved_status,
        "builder_execution_pass": transition_execution_status,
        "advice_generation_pass": advice_generation_status,
        "proof_verification_pass": proof_verification_status,
        "advice_budget_pass": advice_budget_status,
        "answer_access_pass": answer_access_status,
        "resource_budget_pass": resource_budget_status,
        "resource_account_pass": PASS
        if replay.ok
        and resource_derivation_status == PASS
        and ledger["resource_account_complete"]
        else FAIL,
        "oracle_free_pass": oracle_free_status,
        "replay_pass": PASS if replay.ok else FAIL,
        "run_class_nonempty": run_nonempty_status,
        "maximality_pass": maximality_status,
        "fairness_pass": fairness_status,
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
        and operational_status == PASS
        and refs_resolved_status == PASS
        and transition_execution_status == PASS
        and resource_derivation_status == PASS
        and proof_verification_status in {PASS, NOT_APPLICABLE}
        and replay.outstanding_debt == 0
        else FAIL
    )
    expected_correctness = {
        "oracle_pass": oracle_status,
        "contract_pass": contract_status,
        "complete_pass": PASS
        if replay.ok
        and transition_execution_status == PASS
        and candidate_result["status"] in {"sat", "unsat", "complete"}
        else FAIL,
        "budget_pass": resource_budget_status,
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


def validate_bytes(
    record_bytes: bytes,
    schema_bytes: bytes,
    artifact_root: Path,
) -> ValidationReport:
    """Supported API: hash, parse, and use caller inputs from exact bytes."""

    schema_hash = sha256_bytes(schema_bytes)
    if schema_hash != PINNED_SCHEMA_HASH:
        return ValidationReport(
            schema_version=None,
            validator_version=VALIDATOR_VERSION,
            structural_ok=False,
            semantic_ok=False,
            admission_pass=None,
            final_completion=None,
            issues=(
                ValidationIssue(
                    "schema-byte-pin-mismatch",
                    "$schema",
                    f"expected {PINNED_SCHEMA_HASH}, received {schema_hash}",
                ),
            ),
        )
    try:
        schema = _load_json_object_bytes(schema_bytes, source="schema-bytes")
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        return ValidationReport(
            schema_version=None,
            validator_version=VALIDATOR_VERSION,
            structural_ok=False,
            semantic_ok=False,
            admission_pass=None,
            final_completion=None,
            issues=(ValidationIssue("schema-parse", "$schema", str(error)),),
        )
    try:
        record = _load_json_object_bytes(record_bytes, source="record-bytes")
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        return ValidationReport(
            schema_version=None,
            validator_version=VALIDATOR_VERSION,
            structural_ok=False,
            semantic_ok=False,
            admission_pass=None,
            final_completion=None,
            issues=(ValidationIssue("record-parse", "$", str(error)),),
        )
    return _validate_parsed_record(
        record,
        schema,
        artifact_root,
        schema_sha256=schema_hash,
    )


def validate_path(
    record_path: Path,
    schema_path: Path,
    artifact_root: Path,
) -> ValidationReport:
    # Parse, hash, and use each caller-supplied file from one byte snapshot.
    schema_bytes = schema_path.read_bytes()
    record_bytes = record_path.read_bytes()
    return validate_bytes(record_bytes, schema_bytes, artifact_root)
