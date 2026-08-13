#!/usr/bin/env python3
"""Local, read-only conformance checks for frozen PNP-GLC I0 v0.2.2.

The candidate root is read only.  Schema-valid reference substitutions that
need a fresh signed trace are assembled under a temporary copy using the
non-production fixture key.  No network access is used and no P/NP inference
is made.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Mapping

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from jsonschema import Draft202012Validator


sys.dont_write_bytecode = True

ROOT = Path(
    r"C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering"
    r"\outputs\pnp-glc-i0"
)
SCHEMA_PATH = ROOT / "schemas" / "run-record.schema.v0.2.2-candidate.json"
FIXTURES = ROOT / "fixtures-v0.2.2"
ARTIFACTS = ROOT / "artifacts-v0.2.2"
CHECKSUM_PATH = ROOT / "SHA256SUMS-v0.2.2-candidate.txt"
FIXTURE_KEY_PATH = (
    ROOT.parents[1] / "work" / "i0-v021-trace-signing-key.pem"
)

EXPECTED_HASHES = {
    CHECKSUM_PATH: "ab63a7d921f04e71bdfc8cca0f681e81e9a1ba2aaac89e1674a6d0c883a8ec0b",
    SCHEMA_PATH: "bdbb386ce7eaab5377344bf29762ccbe45ea6371ac72742de509467cb70bb556",
    ROOT / "src" / "pnp_glc_i0" / "semantic_validator_v022.py":
        "7da459e8ad9fb3f8a49faa312a612f05484588143f36ff0918d090d6b1965ae5",
    ARTIFACTS / "candidate-projection-spec.v0.2.2.json":
        "7860aa7a741fae5dcc6846b614c16450d29d17573563d6373a243931b9b51e57",
    ARTIFACTS / "artifact-closure-spec.v0.2.2.json":
        "11f6cb511adfcf9528d11390e59ce1b52d8f709053ff5aa7295230f5b3e604eb",
    ARTIFACTS / "evidence-role-spec.v0.2.2.json":
        "2fefa7aacb9b6d914c3b78cdb2c187262d12a35bd56b14fd5882a71b84991a3f",
}

sys.path.insert(0, str(ROOT / "src"))
from pnp_glc_i0 import semantic_validator_v022 as V  # noqa: E402


SCHEMA_BYTES = SCHEMA_PATH.read_bytes()
SCHEMA = V._load_json_object_bytes(SCHEMA_BYTES, source="schema")
SCHEMA_CHECKER = Draft202012Validator(SCHEMA)
STORE = V.ArtifactIndex(ROOT)

RESULTS: list[dict[str, Any]] = []


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_snapshot(root: Path) -> dict[str, tuple[int, int, str]]:
    snapshot: dict[str, tuple[int, int, str]] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            stat = path.stat()
            snapshot[path.relative_to(root).as_posix()] = (
                stat.st_size,
                stat.st_mtime_ns,
                sha256(path.read_bytes()),
            )
    return snapshot


def add_result(
    probe_id: str,
    classification: str,
    expected_observation: bool,
    evidence: Mapping[str, Any],
) -> None:
    RESULTS.append(
        {
            "probe_id": probe_id,
            "classification": classification,
            "expected_observation": expected_observation,
            "evidence": dict(evidence),
        }
    )


def load_fixture(name: str) -> dict[str, Any]:
    return copy.deepcopy(
        V._load_json_object_bytes(
            (FIXTURES / f"{name}.json").read_bytes(), source=name
        )
    )


def report_dict(report: V.ValidationReport) -> dict[str, Any]:
    return {
        "structural_ok": report.structural_ok,
        "semantic_ok": report.semantic_ok,
        "admission_pass": report.admission_pass,
        "final_completion": report.final_completion,
        "record_accepted": report.record_accepted,
        "issue_codes": sorted({issue.code for issue in report.issues}),
    }


def validate_object(record: Mapping[str, Any], root: Path = ROOT) -> V.ValidationReport:
    encoded = json.dumps(
        record,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return V.validate_bytes(encoded, SCHEMA_BYTES, root)


def recompute_receipt_closure(record: dict[str, Any], root: Path = ROOT) -> str:
    store = V.ArtifactIndex(root)
    closure = V._artifact_closure(V._direct_receipt_reference_map(record), store)
    record["validation_receipt"]["resolved_evidence_hashes"] = [
        f"sha256:{reference}" for reference in sorted(closure.references)
    ]
    return closure.status


def write_json(path: Path, value: Mapping[str, Any]) -> bytes:
    data = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def load_fixture_key() -> Ed25519PrivateKey:
    key = serialization.load_pem_private_key(
        FIXTURE_KEY_PATH.read_bytes(), password=None
    )
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("fixture key is not Ed25519")
    public_artifact = V._load_json_object_bytes(
        (ARTIFACTS / "trace-public-key.v0.2.2.json").read_bytes(),
        source="public-key",
    )
    expected_public = base64.b64decode(
        public_artifact["public_key_base64"], validate=True
    )
    actual_public = key.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )
    if actual_public != expected_public:
        raise ValueError("fixture key does not match pinned public artifact")
    return key


def signed_copy_case(
    temp_root: Path,
    key: Ed25519PrivateKey,
    label: str,
    base_name: str,
    mutate: Callable[[dict[str, Any], dict[str, Any]], None],
    *,
    map_mode: str = "actual",
    map_transform: Callable[[dict[str, str]], dict[str, str]] | None = None,
    sync_resource_samples: bool = True,
) -> dict[str, Any]:
    record = load_fixture(base_name)
    baseline_store = V.ArtifactIndex(ROOT)
    trace = copy.deepcopy(
        baseline_store.load_json(record["validation_receipt"]["trace_sha256"])
    )
    mutate(record, trace)

    trace["events"] = copy.deepcopy(record["events"])
    trace["candidate_output"] = copy.deepcopy(record["candidate_result"])
    trace["certificate_refs"] = copy.deepcopy(
        record["candidate_result"]["certificate_refs"]
    )
    if sync_resource_samples:
        for field in (
            "space_bytes",
            "description_bytes",
            "admission_costs",
            "precision",
            "counts",
        ):
            trace["resource_samples"][field] = copy.deepcopy(
                record["ledger"][field]
            )
    projection_hash = V.candidate_projection_sha256(record)
    trace["candidate_projection_sha256"] = projection_hash
    record["validation_receipt"]["candidate_projection_sha256"] = projection_hash

    if map_mode == "actual":
        signed_map = V._actual_operational_reference_map(record)
    elif map_mode == "expected":
        signed_map = V._expected_operational_reference_map(record)
    else:
        raise ValueError(map_mode)
    signed_map = dict(signed_map)
    if map_transform is not None:
        signed_map = map_transform(signed_map)
    trace["operational_reference_map"] = V._canonical_operational_reference_map(
        signed_map
    )
    record["validation_receipt"][
        "operational_reference_map_sha256"
    ] = V.operational_reference_map_sha256(signed_map)

    local_dir = temp_root / "_ai2-conformance"
    trace_bytes = write_json(local_dir / f"{label}.trace.json", trace)
    trace_hash = sha256(trace_bytes)
    trace_ref = f"sha256:{trace_hash}"
    public_ref = f"sha256:{V.PINNED_TRACE_PUBLIC_KEY_HASH}"
    signature = key.sign(
        V.TRACE_SIGNATURE_CONTEXT + bytes.fromhex(trace_hash)
    )
    authenticity = {
        "artifact_envelope": {
            "spec_id": V.ARTIFACT_CLOSURE_SPEC_ID,
            "artifact_type": "trace-authenticity-receipt",
            "version": V.VALIDATOR_VERSION,
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
        "receipt_version": V.VALIDATOR_VERSION,
        "algorithm": "Ed25519",
        "signer_id": V.TRACE_SIGNER_ID,
        "public_key_ref": public_ref,
        "trace_sha256": trace_ref,
        "signature_base64": base64.b64encode(signature).decode("ascii"),
    }
    auth_bytes = write_json(local_dir / f"{label}.trace-auth.json", authenticity)
    receipt = record["validation_receipt"]
    receipt["trace_sha256"] = trace_ref
    receipt["trace_authenticity_ref"] = f"sha256:{sha256(auth_bytes)}"
    receipt["trace_public_key_ref"] = public_ref
    receipt["trace_signer_id"] = V.TRACE_SIGNER_ID
    receipt["observed_answer_access"] = trace["answer_access"]
    closure_status = recompute_receipt_closure(record, temp_root)

    schema_valid = SCHEMA_CHECKER.is_valid(record)
    report = validate_object(record, temp_root)
    temp_store = V.ArtifactIndex(temp_root)
    authenticity_status = V._trace_authenticity_status(record, temp_store)
    return {
        "schema_valid": schema_valid,
        "signature_status": authenticity_status,
        "closure_status": closure_status,
        **report_dict(report),
    }


class SyntheticStore:
    def __init__(self, values: Mapping[str, bytes]):
        self.values = dict(values)

    def resolve(self, reference: str) -> tuple[tuple[Path, bytes], ...]:
        value = self.values.get(V.normalize_hash(reference))
        return () if value is None else ((Path(f"synthetic-{reference}.json"), value),)


def envelope(artifact_type: str, edges: list[dict[str, str]], *, spec: str | None = None) -> bytes:
    body: dict[str, Any] = {
        "artifact_type": artifact_type,
        "version": V.VALIDATOR_VERSION,
        "edges": edges,
    }
    if spec is not None:
        body["spec_id"] = spec
    return json.dumps({"artifact_envelope": body}, separators=(",", ":")).encode(
        "utf-8"
    )


def probe_identity() -> None:
    actual = {str(path): sha256(path.read_bytes()) for path in EXPECTED_HASHES}
    expected = {str(path): digest for path, digest in EXPECTED_HASHES.items()}
    count = 0
    failures: list[str] = []
    for line in CHECKSUM_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(maxsplit=1)
        path = ROOT / relative.lstrip("*").replace("/", "\\")
        count += 1
        if not path.is_file():
            failures.append(f"missing:{relative}")
        elif sha256(path.read_bytes()) != digest.lower():
            failures.append(f"mismatch:{relative}")
    add_result(
        "IDENTITY-022",
        "Observation",
        actual == expected and count == 98 and not failures,
        {
            "core_hashes_match": actual == expected,
            "checksum_entries": count,
            "checksum_failures": failures,
        },
    )


def probe_builtin_matrix() -> None:
    manifest = V._load_json_object_bytes(
        (FIXTURES / "manifest.json").read_bytes(), source="manifest"
    )
    mismatches: dict[str, Any] = {}
    for name, expected in manifest["fixtures"].items():
        actual = V.validate_path(
            FIXTURES / f"{name}.json", SCHEMA_PATH, ROOT
        ).to_dict()
        differing = {
            key: {"expected": value, "actual": actual[key]}
            for key, value in expected.items()
            if actual[key] != value
        }
        if differing:
            mismatches[name] = differing
    add_result(
        "FIXTURE-MATRIX-022",
        "Experiment",
        len(manifest["fixtures"]) == 31 and not mismatches,
        {"fixture_count": len(manifest["fixtures"]), "mismatches": mismatches},
    )


def probe_reference_substitutions(temp_root: Path, key: Ed25519PrivateKey) -> None:
    def run_spec(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["validation_receipt"]["run_spec_ref"] = (
            f"sha256:{V.PINNED_RUN_STANDARD_HASH}"
        )

    def sandbox(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["validation_receipt"]["capability_sandbox_ref"] = (
            f"sha256:{V.PINNED_RUN_STANDARD_HASH}"
        )

    two_sat_contract = V._load_json_object_bytes(
        (ARTIFACTS / "contract-2sat.v0.2.2.json").read_bytes(),
        source="2sat-contract",
    )

    def contract(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["problem"]["contract"]["sha256"] = (
            f"sha256:{V.PINNED_TWO_SAT_CONTRACT_HASH}"
        )
        record["problem"]["contract"]["completion_requirements"] = copy.deepcopy(
            two_sat_contract["completion_requirements"]
        )

    def invariant(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        contract_ref = f"sha256:{V.PINNED_PARITY_CONTRACT_HASH}"
        record["mechanism"]["admissibility"]["local_invariant_ref"] = contract_ref
        record["candidate_result"]["certificate_refs"] = [contract_ref]
        for event in record["events"]:
            event["invariant_ref"] = contract_ref
        record["events"][-1]["output_sha256"] = "sha256:" + sha256(
            V.canonical_json_bytes(record["candidate_result"])
        )

    cases = {
        "run-spec robust-to-standard": signed_copy_case(
            temp_root, key, "run-spec", "robust-legit", run_spec
        ),
        "sandbox-to-run-spec": signed_copy_case(
            temp_root, key, "sandbox", "legit", sandbox
        ),
        "PARITY-contract-to-2SAT-contract": signed_copy_case(
            temp_root, key, "contract", "legit", contract
        ),
        "invariant-to-contract": signed_copy_case(
            temp_root, key, "invariant", "legit", invariant
        ),
    }
    expected = all(
        value["schema_valid"]
        and value["signature_status"] == V.PASS
        and not value["record_accepted"]
        for value in cases.values()
    )
    add_result(
        "REFERENCE-SUBSTITUTION-022",
        "Negative unit test",
        expected,
        cases,
    )


def probe_operational_maps(temp_root: Path, key: Ed25519PrivateKey) -> None:
    no_change = lambda _record, _trace: None

    def omit_contract(values: dict[str, str]) -> dict[str, str]:
        values.pop("contract")
        return values

    def add_extra(values: dict[str, str]) -> dict[str, str]:
        values["extra-receipt-role"] = V.PINNED_TRACE_PUBLIC_KEY_HASH
        return values

    cases = {
        "signed-map-missing-contract": signed_copy_case(
            temp_root,
            key,
            "map-missing",
            "legit",
            no_change,
            map_mode="expected",
            map_transform=omit_contract,
        ),
        "signed-map-extra-role": signed_copy_case(
            temp_root,
            key,
            "map-extra",
            "legit",
            no_change,
            map_mode="expected",
            map_transform=add_extra,
        ),
    }

    receipt = load_fixture("legit")
    receipt["validation_receipt"]["operational_reference_map_sha256"] = "f" * 64
    receipt_case = report_dict(validate_object(receipt))
    receipt_case["schema_valid"] = SCHEMA_CHECKER.is_valid(receipt)
    cases["receipt-map-hash-change"] = receipt_case

    expected = all(
        value["schema_valid"] and not value["record_accepted"]
        for value in cases.values()
    )
    add_result("OPERATIONAL-MAP-022", "Negative unit test", expected, cases)


def probe_trace_receipt_pairing() -> None:
    record = load_fixture("legit")
    source = load_fixture("2sat-sat")
    record["validation_receipt"]["trace_sha256"] = source["validation_receipt"][
        "trace_sha256"
    ]
    record["validation_receipt"]["trace_authenticity_ref"] = source[
        "validation_receipt"
    ]["trace_authenticity_ref"]
    closure_status = recompute_receipt_closure(record)
    report = validate_object(record)
    evidence = {
        "schema_valid": SCHEMA_CHECKER.is_valid(record),
        "signature_status": V._trace_authenticity_status(record, STORE),
        "closure_status": closure_status,
        **report_dict(report),
    }
    add_result(
        "TRACE-PAIRING-022",
        "Negative unit test",
        evidence["schema_valid"]
        and evidence["signature_status"] == V.PASS
        and not evidence["record_accepted"],
        evidence,
    )


def probe_envelope_classification() -> None:
    a = "a" * 64
    b = "b" * 64
    c = "c" * 64
    spec = V.ARTIFACT_CLOSURE_SPEC_ID

    missing_spec = V._artifact_closure(
        {"run-spec": a}, SyntheticStore({a: envelope("run-spec", [])})
    )
    unsupported = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore({a: envelope("run-spec", [], spec="urn:unsupported")}),
    )
    unsupported_incomplete_bytes = json.dumps(
        {"artifact_envelope": {"spec_id": "urn:unsupported:closure:9"}},
        separators=(",", ":"),
    ).encode("utf-8")
    unsupported_incomplete = V._artifact_closure(
        {"run-spec": a}, SyntheticStore({a: unsupported_incomplete_bytes})
    )
    wrong_edge = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {
                a: envelope(
                    "run-spec",
                    [
                        {
                            "role": "fairness-spec",
                            "expected_type": "ed25519-public-key",
                            "sha256": b,
                        }
                    ],
                    spec=spec,
                ),
                b: envelope("ed25519-public-key", [], spec=spec),
            }
        ),
    )
    duplicate_edge = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {
                a: envelope(
                    "run-spec",
                    [
                        {
                            "role": "fairness-spec",
                            "expected_type": "fairness-spec",
                            "sha256": b,
                        },
                        {
                            "role": "fairness-spec",
                            "expected_type": "fairness-spec",
                            "sha256": c,
                        },
                    ],
                    spec=spec,
                ),
                b: envelope("fairness-spec", [], spec=spec),
                c: envelope("fairness-spec", [], spec=spec),
            }
        ),
    )
    missing_child = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {
                a: envelope(
                    "run-spec",
                    [
                        {
                            "role": "fairness-spec",
                            "expected_type": "fairness-spec",
                            "sha256": b,
                        }
                    ],
                    spec=spec,
                )
            }
        ),
    )
    relation_cycle = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {
                a: envelope(
                    "run-spec",
                    [
                        {
                            "role": "fairness-spec",
                            "expected_type": "fairness-spec",
                            "sha256": b,
                        }
                    ],
                    spec=spec,
                ),
                b: envelope(
                    "fairness-spec",
                    [
                        {
                            "role": "legacy-fairness-source",
                            "expected_type": "opaque-content",
                            "sha256": a,
                        }
                    ],
                    spec=spec,
                ),
            }
        ),
    )
    evidence = {
        "missing-required-spec-id": missing_spec.status,
        "shape-valid-unsupported-spec": unsupported.status,
        "unsupported-spec-with-missing-required-members": (
            unsupported_incomplete.status
        ),
        "wrong-edge-type": wrong_edge.status,
        "duplicate-edge-role": duplicate_edge.status,
        "missing-child": missing_child.status,
        "typed-relation-cycle": relation_cycle.status,
    }
    expected = evidence == {
        "missing-required-spec-id": V.FAIL,
        "shape-valid-unsupported-spec": V.UNKNOWN,
        "unsupported-spec-with-missing-required-members": V.UNKNOWN,
        "wrong-edge-type": V.FAIL,
        "duplicate-edge-role": V.FAIL,
        "missing-child": V.FAIL,
        "typed-relation-cycle": V.FAIL,
    }
    add_result("ENVELOPE-CLASS-022", "Negative unit test", expected, evidence)
    add_result(
        "CLOSURE-CLASS-01",
        "Counterexample / promotion blocker; fail-closed",
        unsupported_incomplete.status == V.UNKNOWN,
        {
            "minimal_artifact": {
                "artifact_envelope": {"spec_id": "urn:unsupported:closure:9"}
            },
            "frozen_spec_expected": V.FAIL,
            "validator_actual": unsupported_incomplete.status,
            "reason": (
                "required artifact_type/version/edges must be shape-checked before "
                "an unsupported spec_id is classified unknown"
            ),
            "admission_effect": "unknown still blocks admission",
        },
    )


def probe_raw_and_schema_bytes() -> None:
    negative_zero = V.validate_path(
        FIXTURES / "negative-zero.json", SCHEMA_PATH, ROOT
    )
    surrogate = V.validate_path(
        FIXTURES / "unpaired-surrogate.json", SCHEMA_PATH, ROOT
    )
    wrong_schema = V.validate_bytes(
        (FIXTURES / "legit.json").read_bytes(), b"{}", ROOT
    )
    newline_equal = V.canonical_json_bytes(json.loads(r'{"x":"\n"}')) == (
        V.canonical_json_bytes(json.loads(r'{"x":"\u000a"}'))
    )
    evidence = {
        "raw-negative-zero": report_dict(negative_zero),
        "unpaired-surrogate": report_dict(surrogate),
        "wrong-schema-bytes": report_dict(wrong_schema),
        "equivalent-newline-spellings": newline_equal,
    }
    expected = (
        not negative_zero.structural_ok
        and negative_zero.issues[0].code == "record-parse"
        and "negative zero" in negative_zero.issues[0].message
        and not surrogate.record_accepted
        and "canonical-unicode-scalar"
        in {issue.code for issue in surrogate.issues}
        and not wrong_schema.structural_ok
        and wrong_schema.issues[0].code == "schema-byte-pin-mismatch"
        and newline_equal
    )
    add_result("RAW-SCHEMA-BYTES-022", "Conformance", expected, evidence)


def probe_derived_fields() -> None:
    expected_codes = {
        "fabricated-problem-size": "problem-size-derivation",
        "fabricated-failure-frontier": "failure-frontier-derivation",
        "declared-answer-access-mismatch": "answer-access-family-binding",
        "fabricated-states-999": "derived-gate-mismatch",
        "fabricated-transition-digest": "derived-gate-mismatch",
    }
    evidence: dict[str, Any] = {}
    expected = True
    for name, required_code in expected_codes.items():
        report = V.validate_path(FIXTURES / f"{name}.json", SCHEMA_PATH, ROOT)
        item = report_dict(report)
        evidence[name] = item
        expected = expected and not report.record_accepted and required_code in item[
            "issue_codes"
        ]
    add_result("DERIVED-MIRRORS-022", "Negative unit test", expected, evidence)


def probe_resource_mirrors(temp_root: Path, key: Ed25519PrivateKey) -> None:
    def change_space(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["ledger"]["space_bytes"]["peak"] += 1

    inconsistent = signed_copy_case(
        temp_root,
        key,
        "resource-inconsistent",
        "legit",
        change_space,
        sync_resource_samples=False,
    )
    attested = signed_copy_case(
        temp_root,
        key,
        "resource-attested",
        "legit",
        change_space,
        sync_resource_samples=True,
    )
    evidence = {
        "record-trace-mismatch": inconsistent,
        "matching-signed-raw-measurement": attested,
        "scope": (
            "space/description/admission/precision are authenticated raw "
            "measurements; acceptance establishes signer binding, not independent measurement"
        ),
    }
    expected = (
        inconsistent["schema_valid"]
        and inconsistent["signature_status"] == V.PASS
        and not inconsistent["record_accepted"]
        and attested["schema_valid"]
        and attested["signature_status"] == V.PASS
        and attested["record_accepted"]
    )
    add_result("RESOURCE-MIRROR-022", "Scoped Observation", expected, evidence)


def probe_gate_applicability() -> None:
    fixture_names = (
        "legit",
        "robust-legit",
        "neutral-legit",
        "robust-neutral-legit",
        "2sat-sat",
        "2sat-unsat",
        "cheat",
        "unknown-gate",
    )
    total = 0
    schema_accepted: list[str] = []
    for name in fixture_names:
        baseline = load_fixture(name)
        for gate, current in baseline["validation_receipt"]["gates"].items():
            total += 1
            mutated = copy.deepcopy(baseline)
            mutated["validation_receipt"]["admission_pass"] = False
            mutated["validation_receipt"]["final_completion"] = False
            mutated["validation_receipt"]["gates"][gate] = (
                V.PASS if current == V.NOT_APPLICABLE else V.NOT_APPLICABLE
            )
            if SCHEMA_CHECKER.is_valid(mutated):
                schema_accepted.append(f"{name}:{gate}")
    add_result(
        "GATE-APPLICABILITY-022",
        "Schema conformance",
        total == len(fixture_names) * len(V.GATE_KEYS) and not schema_accepted,
        {"mutations_checked": total, "schema_accepted": schema_accepted},
    )


def main() -> int:
    before = tree_snapshot(ROOT)
    probe_identity()
    probe_builtin_matrix()

    key = load_fixture_key()
    with tempfile.TemporaryDirectory(prefix="pnp-glc-v022-conformance-") as name:
        temp_root = Path(name) / "pnp-glc-i0"
        shutil.copytree(
            ROOT,
            temp_root,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        probe_reference_substitutions(temp_root, key)
        probe_operational_maps(temp_root, key)
        probe_resource_mirrors(temp_root, key)

    probe_trace_receipt_pairing()
    probe_envelope_classification()
    probe_raw_and_schema_bytes()
    probe_derived_fields()
    probe_gate_applicability()

    after = tree_snapshot(ROOT)
    changed_paths = sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )
    add_result(
        "CANDIDATE-ROOT-READONLY-022",
        "Provenance",
        not changed_paths,
        {"candidate_root_writes": len(changed_paths), "changed_paths": changed_paths},
    )

    unexpected = [
        result["probe_id"]
        for result in RESULTS
        if not result["expected_observation"]
    ]
    blockers = [
        result["probe_id"]
        for result in RESULTS
        if result["probe_id"] == "CLOSURE-CLASS-01"
        and result["expected_observation"]
    ]
    payload = {
        "scope": "local read-only software conformance review; no network; no P/NP inference",
        "overall_disposition": (
            "FAIL / CLOSURE-CLASS-01"
            if blockers
            else "bounded PASS" if not unexpected else "FAIL / unexpected result"
        ),
        "promotion_blockers": blockers,
        "probe_count": len(RESULTS),
        "unexpected_results": unexpected,
        "candidate_root_writes": len(changed_paths),
        "results": RESULTS,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
