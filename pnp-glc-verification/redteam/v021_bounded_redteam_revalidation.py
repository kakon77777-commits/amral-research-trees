#!/usr/bin/env python3
"""Read-only bounded adversarial probes for frozen PNP-GLC I0 v0.2.1.

The candidate tree is never written.  Temporary files are used only to test
raw-input/canonicalization and snapshot behavior.  This script makes no P/NP
claim; it audits the engineering/provenance gate at the pinned v0.2.1 hashes.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


ROOT = Path(
    r"C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering"
    r"\outputs\pnp-glc-i0"
)
FIXTURES = ROOT / "fixtures-v0.2.1"
SCHEMA_PATH = ROOT / "schemas" / "run-record.schema.v0.2.1-candidate.json"
VALIDATOR_PATH = ROOT / "src" / "pnp_glc_i0" / "semantic_validator_v021.py"
PROJECTION_PATH = (
    ROOT / "artifacts-v0.2.1" / "candidate-projection-spec.v0.2.1.json"
)
CLOSURE_PATH = (
    ROOT / "artifacts-v0.2.1" / "artifact-closure-spec.v0.2.1.json"
)
PUBLIC_KEY_PATH = ROOT / "artifacts-v0.2.1" / "trace-public-key.v0.2.1.json"
MANIFEST_PATH = FIXTURES / "manifest.json"
CHECKSUM_PATH = ROOT / "SHA256SUMS-v0.2.1.txt"

EXPECTED_HASHES = {
    SCHEMA_PATH: "567417a82ea82c8c2ce7ec81df1b4bec5876044f54213446e4ce298ceade6c2b",
    VALIDATOR_PATH: "c777bc631303e977f025fc17aab455cfee3cdfa2b5c1a23166a51ec5e9e99cd4",
    PROJECTION_PATH: "70caae9973a3a02ad8f45364be2175a51ba62c6c0d75b6c807b7b8dfb5bbd115",
    CLOSURE_PATH: "b466bf8d630bac4b1a42a28f534c5d20a0713d418ccb3826ed69ff71d7585c94",
    PUBLIC_KEY_PATH: "27d25ebf48c59e9aff166d32970c3444dc78e25c352f012b3998b0626dfb2a3d",
    MANIFEST_PATH: "6081a4839bb75c2d80e8b856f7018cd2887acccbfd8067bcfdc417b53f4a79b3",
    CHECKSUM_PATH: "4f5925cd2a449549f9629017e538f5fa341fa8baecb4a5bb3f8b93ed005ebd6a",
}

sys.path.insert(0, str(ROOT / "src"))
from pnp_glc_i0 import semantic_validator_v021 as V  # noqa: E402


SCHEMA_BYTES = SCHEMA_PATH.read_bytes()
SCHEMA = V._load_json_object_bytes(SCHEMA_BYTES, source=str(SCHEMA_PATH))
SCHEMA_HASH = hashlib.sha256(SCHEMA_BYTES).hexdigest()


RESULTS: list[dict[str, Any]] = []


def emit(
    probe_id: str,
    classification: str,
    expectation_met: bool,
    evidence: Mapping[str, Any],
) -> None:
    RESULTS.append(
        {
            "probe_id": probe_id,
            "classification": classification,
            "expectation_met": expectation_met,
            "evidence": dict(evidence),
        }
    )


def load_fixture(name: str) -> dict[str, Any]:
    return dict(
        V._load_json_object_bytes(
            (FIXTURES / f"{name}.json").read_bytes(),
            source=name,
        )
    )


def validate_object(
    record: Mapping[str, Any], schema: Mapping[str, Any] = SCHEMA
) -> V.ValidationReport:
    return V.validate_record(
        record,
        schema,
        ROOT,
        schema_sha256=SCHEMA_HASH,
    )


def recompute_receipt_closure(record: dict[str, Any]) -> V.ClosureResult:
    store = V.ArtifactIndex(ROOT)
    closure = V._artifact_closure(V._direct_receipt_reference_set(record), store)
    record["validation_receipt"]["resolved_evidence_hashes"] = [
        f"sha256:{reference}" for reference in sorted(closure.references)
    ]
    return closure


def issue_codes(report: V.ValidationReport) -> list[str]:
    return sorted({issue.code for issue in report.issues})


def fixture_status(name: str) -> dict[str, Any]:
    report = V.validate_path(FIXTURES / f"{name}.json", SCHEMA_PATH, ROOT)
    return {
        "structural_ok": report.structural_ok,
        "semantic_ok": report.semantic_ok,
        "admission_pass": report.admission_pass,
        "final_completion": report.final_completion,
        "record_accepted": report.record_accepted,
        "issues": issue_codes(report),
    }


def probe_identity_and_checksums() -> None:
    actual = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in EXPECTED_HASHES}
    expected = {str(path): digest for path, digest in EXPECTED_HASHES.items()}
    hash_ok = actual == expected

    checked = 0
    failures: list[str] = []
    for line in CHECKSUM_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected_digest, relative = line.split(maxsplit=1)
        relative = relative.lstrip("*")
        path = ROOT / Path(relative.replace("/", "\\"))
        checked += 1
        if not path.is_file():
            failures.append(f"missing:{relative}")
            continue
        actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_digest.lower() != expected_digest.lower():
            failures.append(f"mismatch:{relative}")
    emit(
        "IDENTITY-01",
        "Observation",
        hash_ok and checked == 69 and not failures,
        {
            "core_hashes_match": hash_ok,
            "checksum_entries": checked,
            "checksum_failures": failures,
        },
    )


def probe_baselines() -> None:
    names = [
        "legit",
        "robust-legit",
        "neutral-legit",
        "robust-neutral-legit",
        "2sat-sat",
        "2sat-unsat",
    ]
    statuses = {name: fixture_status(name) for name in names}
    emit(
        "BASELINE-01",
        "Observation",
        all(item["record_accepted"] for item in statuses.values()),
        statuses,
    )


def probe_prov_derive() -> None:
    store = V.ArtifactIndex(ROOT)
    cases: dict[str, dict[str, Any]] = {}
    for name in ("fabricated-states-999", "fabricated-transition-digest"):
        record = load_fixture(name)
        receipt = record["validation_receipt"]
        trace = store.load_json(receipt["trace_sha256"])
        authenticity = V._trace_authenticity_status(record, store)
        replay = V._replay_trace(record, trace, store)
        transition = V._transition_execution_status(record)
        resource = V._resource_derivation_status(record, trace, replay, authenticity)
        report = validate_object(record)
        cases[name] = {
            "signature": authenticity,
            "structural_replay": replay.ok,
            "transition_derivation": transition,
            "resource_derivation": resource,
            "record_accepted": report.record_accepted,
            "issues": issue_codes(report),
        }
    expected = (
        cases["fabricated-states-999"]["signature"] == V.PASS
        and cases["fabricated-states-999"]["structural_replay"]
        and cases["fabricated-states-999"]["resource_derivation"] == V.FAIL
        and not cases["fabricated-states-999"]["record_accepted"]
        and cases["fabricated-transition-digest"]["signature"] == V.PASS
        and cases["fabricated-transition-digest"]["structural_replay"]
        and cases["fabricated-transition-digest"]["transition_derivation"] == V.FAIL
        and not cases["fabricated-transition-digest"]["record_accepted"]
    )
    emit("PROV-DERIVE-01", "Closed regression", expected, cases)


def probe_signature_transplants() -> None:
    store = V.ArtifactIndex(ROOT)

    bad = load_fixture("bad-trace-signature")
    bad_trace = store.load_json(bad["validation_receipt"]["trace_sha256"])
    bad_report = validate_object(bad)

    transplanted_auth = load_fixture("legit")
    source = load_fixture("2sat-sat")
    transplanted_auth["validation_receipt"]["trace_authenticity_ref"] = source[
        "validation_receipt"
    ]["trace_authenticity_ref"]
    recompute_receipt_closure(transplanted_auth)
    transplanted_auth_report = validate_object(transplanted_auth)

    transplanted_key = load_fixture("legit")
    transplanted_key["validation_receipt"]["trace_public_key_ref"] = transplanted_key[
        "problem"
    ]["contract"]["sha256"]
    recompute_receipt_closure(transplanted_key)
    transplanted_key_report = validate_object(transplanted_key)

    transplanted_signer = load_fixture("legit")
    transplanted_signer["validation_receipt"]["trace_signer_id"] = "attacker-producer"
    transplanted_signer_report = validate_object(transplanted_signer)

    evidence = {
        "producer_string_only": {
            "producer_matches": bad_trace.get("producer") == V.TRACE_PRODUCER,
            "authenticity": V._trace_authenticity_status(bad, store),
            "record_accepted": bad_report.record_accepted,
        },
        "auth_receipt_transplant": {
            "authenticity": V._trace_authenticity_status(transplanted_auth, store),
            "record_accepted": transplanted_auth_report.record_accepted,
            "issues": issue_codes(transplanted_auth_report),
        },
        "public_key_role_transplant": {
            "authenticity": V._trace_authenticity_status(transplanted_key, store),
            "record_accepted": transplanted_key_report.record_accepted,
            "issues": issue_codes(transplanted_key_report),
        },
        "signer_string_transplant": {
            "record_accepted": transplanted_signer_report.record_accepted,
            "issues": issue_codes(transplanted_signer_report),
        },
    }
    expected = (
        evidence["producer_string_only"]["producer_matches"]
        and evidence["producer_string_only"]["authenticity"] == V.FAIL
        and not evidence["producer_string_only"]["record_accepted"]
        and evidence["auth_receipt_transplant"]["authenticity"] == V.FAIL
        and not evidence["auth_receipt_transplant"]["record_accepted"]
        and evidence["public_key_role_transplant"]["authenticity"] == V.FAIL
        and not evidence["public_key_role_transplant"]["record_accepted"]
        and not evidence["signer_string_transplant"]["record_accepted"]
    )
    emit("SIG-TRANSPLANT-01", "Closed attack surface", expected, evidence)


class _OneReadSnapshot:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.data = data
        self.read_count = 0

    def read_bytes(self) -> bytes:
        self.read_count += 1
        if self.read_count != 1:
            raise AssertionError(f"{self.name} was reopened")
        return self.data

    def __str__(self) -> str:
        return self.name


def probe_toctou() -> None:
    record_bytes = (FIXTURES / "legit.json").read_bytes()
    schema_snapshot = _OneReadSnapshot("schema-snapshot", SCHEMA_BYTES)
    record_snapshot = _OneReadSnapshot("record-snapshot", record_bytes)
    path_report = V.validate_path(record_snapshot, schema_snapshot, ROOT)

    with tempfile.TemporaryDirectory(prefix="pnp-glc-v021-toctou-") as temp_name:
        temp_root = Path(temp_name)
        artifact_path = temp_root / "artifact.json"
        old_bytes = b'{"generation":"old"}'
        new_bytes = b'{"generation":"new"}'
        artifact_path.write_bytes(old_bytes)
        index = V.ArtifactIndex(temp_root)
        old_hash = V.sha256_bytes(old_bytes)
        artifact_path.write_bytes(new_bytes)
        pinned_bytes = index.resolve(old_hash)[0][1]
        parsed_generation = index.load_json(old_hash)["generation"]
        new_hash_visible = index.contains(V.sha256_bytes(new_bytes))

    evidence = {
        "schema_read_count": schema_snapshot.read_count,
        "record_read_count": record_snapshot.read_count,
        "snapshot_record_accepted": path_report.record_accepted,
        "artifact_old_bytes_retained": pinned_bytes == old_bytes,
        "artifact_parse_uses_old_bytes": parsed_generation == "old",
        "post_index_replacement_visible": new_hash_visible,
    }
    expected = (
        evidence["schema_read_count"] == 1
        and evidence["record_read_count"] == 1
        and evidence["snapshot_record_accepted"]
        and evidence["artifact_old_bytes_retained"]
        and evidence["artifact_parse_uses_old_bytes"]
        and not evidence["post_index_replacement_visible"]
    )
    emit("TOCTOU-01", "Closed attack surface for validate_path/ArtifactIndex", expected, evidence)


class _SyntheticStore:
    def __init__(self, values: Mapping[str, bytes]):
        self.values = dict(values)

    def resolve(self, reference: str) -> tuple[tuple[Path, bytes], ...]:
        value = self.values.get(V.normalize_hash(reference))
        if value is None:
            return ()
        return ((Path(f"synthetic-{reference}.json"), value),)


def _envelope(spec_id: Any, artifact_type: Any, refs: Any) -> bytes:
    value = {
        "artifact_envelope": {
            "spec_id": spec_id,
            "artifact_type": artifact_type,
            "typed_refs": refs,
        }
    }
    return json.dumps(value, separators=(",", ":")).encode("utf-8")


def probe_fixed_point_closure() -> None:
    a = "a" * 64
    b = "b" * 64
    missing = "c" * 64
    known = V.ARTIFACT_CLOSURE_SPEC_ID

    cycle_store = _SyntheticStore(
        {
            a: _envelope(known, "cycle-a", [f"sha256:{b}"]),
            b: _envelope(known, "cycle-b", [f"sha256:{a}"]),
        }
    )
    cycle = V._artifact_closure([a], cycle_store)

    missing_store = _SyntheticStore(
        {a: _envelope(known, "parent", [f"sha256:{missing}"])}
    )
    missing_result = V._artifact_closure([a], missing_store)

    malformed_store = _SyntheticStore(
        {
            a: json.dumps(
                {
                    "artifact_envelope": {
                        "spec_id": known,
                        "artifact_type": "missing-typed-refs",
                    }
                }
            ).encode("utf-8")
        }
    )
    malformed = V._artifact_closure([a], malformed_store)

    unknown_store = _SyntheticStore({a: _envelope("urn:unknown", "x", [])})
    unknown = V._artifact_closure([a], unknown_store)

    missing_spec_store = _SyntheticStore(
        {
            a: json.dumps(
                {
                    "artifact_envelope": {
                        "artifact_type": "missing-spec-id",
                        "typed_refs": [],
                    }
                }
            ).encode("utf-8")
        }
    )
    missing_spec = V._artifact_closure([a], missing_spec_store)

    evidence = {
        "synthetic_cycle": {
            "status": cycle.status,
            "closure_size": len(cycle.references),
        },
        "missing_transitive": missing_result.status,
        "malformed_known_envelope": malformed.status,
        "unknown_spec": unknown.status,
        "missing_required_spec_id": missing_spec.status,
        "spec_requires_missing_member_to_fail": True,
    }
    core_expected = (
        cycle.status == V.PASS
        and cycle.references == frozenset({a, b})
        and missing_result.status == V.FAIL
        and malformed.status == V.FAIL
        and unknown.status == V.UNKNOWN
    )
    emit("CLOSURE-FIXPOINT-01", "Closed bounded algorithm probes", core_expected, evidence)
    emit(
        "CLOSURE-CLASS-01",
        "Fail-closed classification correction",
        missing_spec.status == V.UNKNOWN,
        {
            "observed": missing_spec.status,
            "specified": V.FAIL,
            "impact": "blocks admission, but malformed is mislabeled unknown",
        },
    )


def probe_ref_type_confusion() -> None:
    # AI-1 minimal variant: robust run spec replaced by the standard run spec.
    wrong_run_spec = load_fixture("robust-legit")
    standard_run_ref = load_fixture("legit")["validation_receipt"]["run_spec_ref"]
    wrong_run_spec["validation_receipt"]["run_spec_ref"] = standard_run_ref
    closure_one = recompute_receipt_closure(wrong_run_spec)
    wrong_run_report = validate_object(wrong_run_spec)

    # AI-3 stronger variant: four receipt-only operational roles all point to
    # the pinned Ed25519 public-key artifact.  Candidate projection/signature
    # remain unchanged; only the external receipt and declared closure change.
    key_substitution = load_fixture("robust-legit")
    public_key_ref = key_substitution["validation_receipt"]["trace_public_key_ref"]
    for field in (
        "run_spec_ref",
        "maximal_run_spec_ref",
        "fairness_spec_ref",
        "capability_sandbox_ref",
    ):
        key_substitution["validation_receipt"][field] = public_key_ref
    closure_four = recompute_receipt_closure(key_substitution)
    key_report = validate_object(key_substitution)

    store = V.ArtifactIndex(ROOT)
    evidence = {
        "robust_to_standard_run_spec": {
            "signature": V._trace_authenticity_status(wrong_run_spec, store),
            "closure": closure_one.status,
            "structural_ok": wrong_run_report.structural_ok,
            "semantic_ok": wrong_run_report.semantic_ok,
            "admission_pass": wrong_run_report.admission_pass,
            "final_completion": wrong_run_report.final_completion,
            "record_accepted": wrong_run_report.record_accepted,
            "issues": issue_codes(wrong_run_report),
        },
        "four_roles_to_public_key": {
            "signature": V._trace_authenticity_status(key_substitution, store),
            "closure": closure_four.status,
            "structural_ok": key_report.structural_ok,
            "semantic_ok": key_report.semantic_ok,
            "admission_pass": key_report.admission_pass,
            "final_completion": key_report.final_completion,
            "record_accepted": key_report.record_accepted,
            "issues": issue_codes(key_report),
        },
    }
    reproduced = all(
        item["signature"] == V.PASS
        and item["closure"] == V.PASS
        and item["structural_ok"]
        and item["semantic_ok"]
        and item["admission_pass"]
        and item["final_completion"]
        and item["record_accepted"]
        and not item["issues"]
        for item in evidence.values()
    )
    emit("REF-TYPE-01", "Counterexample / admission blocker", reproduced, evidence)


def probe_canonicalization() -> None:
    newline_short = V.canonical_json_bytes(json.loads(r'{"x":"\n"}'))
    newline_unicode = V.canonical_json_bytes(json.loads(r'{"x":"\u000a"}'))

    nfd_rejected = False
    try:
        V.canonical_json_bytes({"x": "e\u0301"})
    except ValueError:
        nfd_rejected = True

    float_rejected = False
    try:
        V.canonical_json_bytes({"x": 0.0})
    except ValueError:
        float_rejected = True

    large_integer_rejected = False
    try:
        V.canonical_json_bytes({"x": V.MAX_SAFE_INTEGER + 1})
    except ValueError:
        large_integer_rejected = True

    legit_bytes = (FIXTURES / "legit.json").read_bytes()
    legit_text = legit_bytes.decode("utf-8")
    negative_zero_text = legit_text.replace('"seed": 0', '"seed": -0', 1)
    replacement_count = int(negative_zero_text != legit_text)

    negative_zero_accepted = False
    same_parsed_record = False
    surrogate_exception = "none"
    surrogate_canonical_exception = "none"
    surrogate_record_accepted: bool | None = None
    surrogate_issue_codes: list[str] = []
    with tempfile.TemporaryDirectory(prefix="pnp-glc-v021-canon-") as temp_name:
        temp_root = Path(temp_name)
        negative_zero_path = temp_root / "negative-zero.json"
        negative_zero_path.write_text(negative_zero_text, encoding="utf-8")
        original = V._load_json_object_bytes(legit_bytes, source="legit")
        altered = V._load_json_object_bytes(
            negative_zero_path.read_bytes(), source="negative-zero"
        )
        same_parsed_record = original == altered
        negative_zero_report = V.validate_path(negative_zero_path, SCHEMA_PATH, ROOT)
        negative_zero_accepted = negative_zero_report.record_accepted

        surrogate = copy.deepcopy(original)
        surrogate["candidate_result"]["notes"] = "\ud800"
        surrogate_path = temp_root / "unpaired-surrogate.json"
        surrogate_path.write_bytes(
            json.dumps(surrogate, ensure_ascii=True, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        try:
            surrogate_report = V.validate_path(surrogate_path, SCHEMA_PATH, ROOT)
            surrogate_record_accepted = surrogate_report.record_accepted
            surrogate_issue_codes = issue_codes(surrogate_report)
        except Exception as error:  # Deliberately records fail-closed/crash behavior.
            surrogate_exception = type(error).__name__
        try:
            V.canonical_json_bytes({"x": "\ud800"})
        except Exception as error:
            surrogate_canonical_exception = type(error).__name__

    evidence = {
        "newline_and_u000a_canonicalize_equal": newline_short == newline_unicode,
        "canonical_newline_bytes": newline_short.decode("utf-8"),
        "nfd_rejected": nfd_rejected,
        "float_rejected": float_rejected,
        "large_integer_rejected": large_integer_rejected,
        "negative_zero_replacement_count": replacement_count,
        "negative_zero_parses_identically": same_parsed_record,
        "negative_zero_record_accepted": negative_zero_accepted,
        "unpaired_surrogate_validator_exception": surrogate_exception,
        "unpaired_surrogate_canonical_exception": surrogate_canonical_exception,
        "unpaired_surrogate_record_accepted": surrogate_record_accepted,
        "unpaired_surrogate_issue_codes": surrogate_issue_codes,
    }
    core_expected = (
        newline_short == newline_unicode
        and nfd_rejected
        and float_rejected
        and large_integer_rejected
    )
    emit("CANON-CORE-01", "Closed bounded canonical probes", core_expected, evidence)
    emit(
        "CANON-NEGZERO-01",
        "Canonical-spec conformance counterexample",
        replacement_count == 1 and same_parsed_record and negative_zero_accepted,
        {
            "specified": "negative zero forbidden",
            "observed": "raw -0 is parsed as int 0 and accepted under the existing signature",
        },
    )
    emit(
        "CANON-SURROGATE-01",
        "Fail-closed Observation; explicit-domain diagnostic hardening",
        surrogate_exception == "none"
        and surrogate_canonical_exception == "UnicodeEncodeError"
        and surrogate_record_accepted is False
        and "candidate-projection-mismatch" in surrogate_issue_codes,
        {
            "observed": (
                "canonical serializer raises UnicodeEncodeError; validate_path catches it "
                "as ValueError and rejects via an empty expected projection hash"
            ),
            "validator_exception": surrogate_exception,
            "record_accepted": surrogate_record_accepted,
            "diagnostic": "indirect candidate-projection-mismatch, not explicit surrogate-domain issue",
        },
    )


def probe_schema_mapping_binding() -> None:
    record = load_fixture("legit")
    record["validation_receipt"]["schema_bypass_probe"] = True
    pinned_schema_errors = list(Draft202012Validator(SCHEMA).iter_errors(record))

    # validate_record trusts the caller-supplied digest string independently of
    # the supplied schema mapping.  The empty schema accepts the extra receipt
    # field, while candidate projection and the valid signed trace are unchanged.
    report = V.validate_record(
        record,
        {},
        ROOT,
        schema_sha256=SCHEMA_HASH,
    )
    evidence = {
        "pinned_schema_rejects": bool(pinned_schema_errors),
        "caller_supplied_empty_schema_accepted": report.record_accepted,
        "structural_ok": report.structural_ok,
        "semantic_ok": report.semantic_ok,
        "admission_pass": report.admission_pass,
        "final_completion": report.final_completion,
        "issues": issue_codes(report),
        "validate_path_affected": False,
    }
    emit(
        "SCHEMA-BIND-API-01",
        "Interface blocker if validate_record is supported; otherwise hardening correction",
        evidence["pinned_schema_rejects"]
        and evidence["caller_supplied_empty_schema_accepted"]
        and not evidence["issues"],
        evidence,
    )


def probe_oracle_contract() -> None:
    sat = load_fixture("2sat-sat")
    unsat = load_fixture("2sat-unsat")
    sat_report = validate_object(sat)
    unsat_report = validate_object(unsat)

    sat_bad = copy.deepcopy(sat)
    sat_bad["candidate_result"]["answer"]["assignment"] = {}
    unsat_bad = copy.deepcopy(unsat)
    unsat_bad["candidate_result"]["answer"]["positive_to_negative"] = [1]
    unsat_bad["candidate_result"]["answer"]["negative_to_positive"] = [-1]

    evidence = {
        "sat_end_to_end_accepted": sat_report.record_accepted,
        "unsat_end_to_end_accepted": unsat_report.record_accepted,
        "sat_tamper_oracle": V._independent_oracle_status(sat_bad),
        "sat_tamper_transition": V._transition_execution_status(sat_bad),
        "unsat_tamper_oracle": V._independent_oracle_status(unsat_bad),
        "unsat_tamper_transition": V._transition_execution_status(unsat_bad),
    }
    expected = (
        sat_report.record_accepted
        and unsat_report.record_accepted
        and evidence["sat_tamper_oracle"] == V.FAIL
        and evidence["sat_tamper_transition"] == V.FAIL
        and evidence["unsat_tamper_oracle"] == V.FAIL
        and evidence["unsat_tamper_transition"] == V.FAIL
    )
    emit("ORACLE-CONTRACT-01", "Closed bounded execution probes", expected, evidence)


def probe_gate_and_completion_bypass() -> None:
    base = load_fixture("legit")
    gate_results: dict[str, Any] = {}
    for gate in V.GATE_KEYS:
        mutated = copy.deepcopy(base)
        old = mutated["validation_receipt"]["gates"][gate]
        mutated["validation_receipt"]["gates"][gate] = (
            V.FAIL if old == V.PASS else V.PASS
        )
        report = validate_object(mutated)
        gate_results[gate] = {
            "from": old,
            "to": mutated["validation_receipt"]["gates"][gate],
            "record_accepted": report.record_accepted,
            "structural_ok": report.structural_ok,
            "issues": issue_codes(report),
        }

    na_record = copy.deepcopy(base)
    na_record["validation_receipt"]["gates"]["uniformity_pass"] = V.NOT_APPLICABLE
    na_record["validation_receipt"]["admission_pass"] = False
    na_record["validation_receipt"]["final_completion"] = False
    schema_accepts_na = not list(Draft202012Validator(SCHEMA).iter_errors(na_record))
    na_report = validate_object(na_record)

    false_admission = fixture_status("failed-gate-admission")
    false_completion = fixture_status("false-final-completion")
    robust_null = fixture_status("robust-null-spec")

    all_gate_mutations_rejected = all(
        not item["record_accepted"] for item in gate_results.values()
    )
    evidence = {
        "gate_mutations_rejected": all_gate_mutations_rejected,
        "gate_count": len(gate_results),
        "gate_details": gate_results,
        "universal_gate_na_schema_accepts_when_admission_false": schema_accepts_na,
        "universal_gate_na_semantic_accepts": na_report.record_accepted,
        "universal_gate_na_semantic_issues": issue_codes(na_report),
        "failed_gate_admission_fixture": false_admission,
        "false_final_completion_fixture": false_completion,
        "robust_null_spec_fixture": robust_null,
    }
    expected = (
        all_gate_mutations_rejected
        and not na_report.record_accepted
        and not false_admission["record_accepted"]
        and not false_completion["record_accepted"]
        and not robust_null["record_accepted"]
    )
    emit("GATE-BYPASS-01", "No bounded semantic bypass found", expected, evidence)
    emit(
        "GATE-SCHEMA-NA-01",
        "Two-layer Observation",
        schema_accepts_na and not na_report.record_accepted,
        {
            "schema_alone": "accepts N/A on universally applicable gate when admission=false",
            "external_semantic_validator": "rejects",
        },
    )


def main() -> int:
    probe_identity_and_checksums()
    probe_baselines()
    probe_prov_derive()
    probe_signature_transplants()
    probe_toctou()
    probe_fixed_point_closure()
    probe_ref_type_confusion()
    probe_canonicalization()
    probe_schema_mapping_binding()
    probe_oracle_contract()
    probe_gate_and_completion_bypass()

    unexpected = [item["probe_id"] for item in RESULTS if not item["expectation_met"]]
    payload = {
        "scope": "frozen v0.2.1 engineering/provenance gate only; no P/NP inference",
        "candidate_root_writes": 0,
        "overall_disposition": "FAIL / REF-TYPE-01",
        "probe_count": len(RESULTS),
        "unexpected_probe_results": unexpected,
        "results": RESULTS,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if unexpected else 0


if __name__ == "__main__":
    raise SystemExit(main())
