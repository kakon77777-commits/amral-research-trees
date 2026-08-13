#!/usr/bin/env python3
"""Bounded local conformance review for frozen PNP-GLC I0 v0.2.3.

The candidate root is read only.  Every exercised file is first pinned from the
121-entry frozen manifest and copied into a temporary snapshot.  Mutations and
fixture regeneration occur only in that snapshot.  No network access is used,
and no P/NP inference is made.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
import shutil
import subprocess
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
MANIFEST_PATH = ROOT / "SHA256SUMS-v0.2.3-candidate.txt"
SCHEMA_REL = "schemas/run-record.schema.v0.2.3-candidate.json"
VALIDATOR_REL = "src/pnp_glc_i0/semantic_validator_v023.py"
FIXTURE_KEY_PATH = (
    ROOT.parents[1] / "work" / "i0-v021-trace-signing-key.pem"
)

EXPECTED_CORE_HASHES = {
    "manifest": "7aafa47149ad3bca042a62fc8c708d61d5ad41a7acf7f4f4a897318f0063c817",
    SCHEMA_REL: "dce6f0c95b95d9377ba7af9f9537bdc277cdf0e68ce74b9ad3bf83db2b011895",
    VALIDATOR_REL: "b0dc4ec989f93ebd557c4c8bfa3004e33b2bbae0eb0f8fa5622489b2d148097b",
    "artifacts-v0.2.3/artifact-closure-spec.v0.2.3.json":
        "4e978ef2a2df0fed51e94e89e6305294a9b7965ad86ab6888ee857da4854643b",
    "artifacts-v0.2.3/evidence-role-spec.v0.2.3.json":
        "fb5c3be06ba68716492b96664bf8fd5c6154c1159025e5f1d278fad1c0b3cbfb",
    "fixtures-v0.2.3/manifest.json":
        "189967b7f60968be2aced2a0b4ee5e8885fbbfd997916ba18f55b33f3a4aa5d1",
    "artifacts-v0.2.3/closure-classification/manifest.json":
        "46721dbe2e8a5e4ce1144da2957c7688059637149dddadff766b517001c6de06",
    "scripts/reproduce_closure_class_v023.py":
        "90aae cdd4214ac188a35f1dbf4894819cfe727c0d9e63a1a39e0d574335806f2".replace(" ", ""),
    "i0-run-report.v0.2.3-candidate.json":
        "7d32357291b59de472a266baad63f7bbb469b60f58bcd727df5d3a35899125eb",
}

RESULTS: list[dict[str, Any]] = []


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add_result(
    probe_id: str,
    classification: str,
    conforms: bool,
    evidence: Mapping[str, Any],
) -> None:
    RESULTS.append(
        {
            "probe_id": probe_id,
            "classification": classification,
            "conforms": bool(conforms),
            "evidence": dict(evidence),
        }
    )


def manifest_entries(manifest_bytes: bytes) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in manifest_bytes.decode("utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(maxsplit=1)
        relative = relative.lstrip("*").replace("\\", "/")
        target = (ROOT / relative).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise ValueError(f"manifest path escapes root: {relative}") from exc
        if relative in entries:
            raise ValueError(f"duplicate manifest path: {relative}")
        if len(digest) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in digest):
            raise ValueError(f"invalid digest for {relative}")
        entries[relative] = digest.lower()
    return entries


def pin_frozen_bytes() -> tuple[bytes, dict[str, str], dict[str, bytes], dict[str, tuple[int, int, str]]]:
    manifest_bytes = MANIFEST_PATH.read_bytes()
    entries = manifest_entries(manifest_bytes)
    frozen: dict[str, bytes] = {}
    metadata: dict[str, tuple[int, int, str]] = {}
    for relative, expected in entries.items():
        path = ROOT / relative
        data = path.read_bytes()
        actual = sha256(data)
        if actual != expected:
            raise ValueError(f"manifest mismatch: {relative}: {actual}")
        stat = path.stat()
        frozen[relative] = data
        metadata[relative] = (stat.st_size, stat.st_mtime_ns, actual)
    manifest_stat = MANIFEST_PATH.stat()
    metadata["<manifest>"] = (
        manifest_stat.st_size,
        manifest_stat.st_mtime_ns,
        sha256(manifest_bytes),
    )
    return manifest_bytes, entries, frozen, metadata


def frozen_metadata(entries: Mapping[str, str]) -> dict[str, tuple[int, int, str]]:
    result: dict[str, tuple[int, int, str]] = {}
    for relative in entries:
        path = ROOT / relative
        if not path.is_file():
            result[relative] = (-1, -1, "missing")
            continue
        stat = path.stat()
        result[relative] = (stat.st_size, stat.st_mtime_ns, sha256(path.read_bytes()))
    if MANIFEST_PATH.is_file():
        stat = MANIFEST_PATH.stat()
        result["<manifest>"] = (
            stat.st_size,
            stat.st_mtime_ns,
            sha256(MANIFEST_PATH.read_bytes()),
        )
    else:
        result["<manifest>"] = (-1, -1, "missing")
    return result


def materialize_snapshot(target: Path, frozen: Mapping[str, bytes]) -> None:
    """Create a version-bounded runtime copy, then overwrite frozen v0.2.3 bytes.

    The 121-entry v0.2.3 manifest is a version delta rather than a standalone
    runtime closure: unchanged modules (parity/oracles/2-SAT), predecessor
    fixtures, and the parent v0.2 schema are intentionally outside it.  The
    review copy therefore includes the local predecessor context while
    excluding concurrently added v0.2.4 successor paths.  Exact v0.2.3 files
    are written from the already hash-verified in-memory snapshots.
    """

    for source in sorted(ROOT.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT)
        lowered = relative.as_posix().lower()
        if (
            "__pycache__" in relative.parts
            or source.suffix.lower() == ".pyc"
            or "v0.2.4" in lowered
            or "v024" in lowered
        ):
            continue
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())

    for relative, data in frozen.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    parent_schema = ROOT.parent / "run-record.schema.json"
    (target.parent / "run-record.schema.json").write_bytes(parent_schema.read_bytes())


sys.path.insert(0, str(ROOT / "src"))
from pnp_glc_i0 import semantic_validator_v023 as V  # noqa: E402


class SyntheticStore:
    def __init__(self, values: Mapping[str, bytes]):
        self.values = dict(values)

    def resolve(self, reference: str) -> tuple[tuple[Path, bytes], ...]:
        value = self.values.get(V.normalize_hash(reference))
        if value is None:
            return ()
        return ((Path(f"synthetic-{V.normalize_hash(reference)}.json"), value),)


def json_bytes(value: Any, *, pretty: bool = False) -> bytes:
    if pretty:
        return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = V._load_json_object_bytes(path.read_bytes(), source=str(path))
    return copy.deepcopy(dict(value))


def report_dict(report: V.ValidationReport) -> dict[str, Any]:
    return {
        "structural_ok": report.structural_ok,
        "semantic_ok": report.semantic_ok,
        "admission_pass": report.admission_pass,
        "final_completion": report.final_completion,
        "record_accepted": report.record_accepted,
        "issue_codes": sorted({issue.code for issue in report.issues}),
    }


def validate_object(record: Mapping[str, Any], schema_bytes: bytes, root: Path) -> V.ValidationReport:
    return V.validate_bytes(json_bytes(record), schema_bytes, root)


def write_json(path: Path, value: Mapping[str, Any]) -> bytes:
    data = json_bytes(value, pretty=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def load_fixture(root: Path, name: str) -> dict[str, Any]:
    return load_json(root / "fixtures-v0.2.3" / f"{name}.json")


def recompute_receipt_closure(record: dict[str, Any], root: Path) -> str:
    store = V.ArtifactIndex(root)
    closure = V._artifact_closure(V._direct_receipt_reference_map(record), store)
    record["validation_receipt"]["resolved_evidence_hashes"] = [
        f"sha256:{reference}" for reference in sorted(closure.references)
    ]
    return closure.status


def load_fixture_key(root: Path) -> Ed25519PrivateKey:
    key = serialization.load_pem_private_key(FIXTURE_KEY_PATH.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("fixture key is not Ed25519")
    public_artifact = load_json(root / "artifacts-v0.2.3" / "trace-public-key.v0.2.3.json")
    expected = base64.b64decode(public_artifact["public_key_base64"], validate=True)
    actual = key.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )
    if actual != expected:
        raise ValueError("fixture key does not match the pinned test public key")
    return key


def signed_copy_case(
    root: Path,
    key: Ed25519PrivateKey,
    label: str,
    base_name: str,
    mutate: Callable[[dict[str, Any], dict[str, Any]], None],
    *,
    map_mode: str = "actual",
    map_transform: Callable[[dict[str, str]], dict[str, str]] | None = None,
    sync_resource_samples: bool = True,
) -> dict[str, Any]:
    record = load_fixture(root, base_name)
    store = V.ArtifactIndex(root)
    trace = copy.deepcopy(store.load_json(record["validation_receipt"]["trace_sha256"]))
    mutate(record, trace)

    trace["events"] = copy.deepcopy(record["events"])
    trace["candidate_output"] = copy.deepcopy(record["candidate_result"])
    trace["certificate_refs"] = copy.deepcopy(record["candidate_result"]["certificate_refs"])
    if sync_resource_samples:
        for field in ("space_bytes", "description_bytes", "admission_costs", "precision", "counts"):
            trace["resource_samples"][field] = copy.deepcopy(record["ledger"][field])

    projection_hash = V.candidate_projection_sha256(record)
    trace["candidate_projection_sha256"] = projection_hash
    record["validation_receipt"]["candidate_projection_sha256"] = projection_hash

    if map_mode == "actual":
        signed_map = dict(V._actual_operational_reference_map(record))
    elif map_mode == "expected":
        signed_map = dict(V._expected_operational_reference_map(record))
    else:
        raise ValueError(map_mode)
    if map_transform is not None:
        signed_map = map_transform(signed_map)
    trace["operational_reference_map"] = V._canonical_operational_reference_map(signed_map)
    record["validation_receipt"]["operational_reference_map_sha256"] = (
        V.operational_reference_map_sha256(signed_map)
    )

    local_dir = root / "_ai2-conformance"
    trace_bytes = write_json(local_dir / f"{label}.trace.json", trace)
    trace_hash = sha256(trace_bytes)
    trace_ref = f"sha256:{trace_hash}"
    public_ref = f"sha256:{V.PINNED_TRACE_PUBLIC_KEY_HASH}"
    signature = key.sign(V.TRACE_SIGNATURE_CONTEXT + bytes.fromhex(trace_hash))
    authenticity = {
        "artifact_envelope": {
            "spec_id": V.ARTIFACT_CLOSURE_SPEC_ID,
            "artifact_type": "trace-authenticity-receipt",
            "version": V.VALIDATOR_VERSION,
            "edges": [
                {"role": "trace", "expected_type": "capability-trace", "sha256": trace_ref},
                {"role": "public-key", "expected_type": "ed25519-public-key", "sha256": public_ref},
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
    closure_status = recompute_receipt_closure(record, root)

    schema_bytes = (root / SCHEMA_REL).read_bytes()
    schema = V._load_json_object_bytes(schema_bytes, source="schema")
    schema_valid = Draft202012Validator(schema).is_valid(record)
    report = validate_object(record, schema_bytes, root)
    authenticity_status = V._trace_authenticity_status(record, V.ArtifactIndex(root))
    return {
        "schema_valid": schema_valid,
        "signature_status": authenticity_status,
        "closure_status": closure_status,
        **report_dict(report),
    }


def probe_identity(manifest_bytes: bytes, entries: Mapping[str, str], frozen: Mapping[str, bytes]) -> None:
    actual = {relative: sha256(frozen[relative]) for relative in EXPECTED_CORE_HASHES if relative != "manifest"}
    expected = {relative: digest for relative, digest in EXPECTED_CORE_HASHES.items() if relative != "manifest"}
    add_result(
        "IDENTITY-023",
        "Observation",
        len(entries) == 121
        and sha256(manifest_bytes) == EXPECTED_CORE_HASHES["manifest"]
        and actual == expected,
        {
            "manifest_entries": len(entries),
            "manifest_hash": sha256(manifest_bytes),
            "core_hashes_match": actual == expected,
            "manifest_mismatches": [],
        },
    )


def run_command(root: Path, arguments: list[str]) -> dict[str, Any]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONUTF8"] = "1"
    completed = subprocess.run(
        [sys.executable, *arguments],
        cwd=root,
        env=environment,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    return {
        "exit": completed.returncode,
        "output": completed.stdout,
        "tail": completed.stdout[-2000:],
    }


def probe_builtin_suites(root: Path) -> None:
    suites = {
        name: run_command(root, ["-m", "unittest", "discover", "-s", name, "-q"])
        for name in ("tests", "tests_v021", "tests_v022", "tests_v023")
    }
    reproducer = run_command(
        root,
        ["scripts/reproduce_closure_class_v023.py", str(root)],
    )
    parsed: dict[str, Any] = {}
    try:
        parsed = json.loads(reproducer["output"])
    except json.JSONDecodeError:
        pass
    conforms = all(item["exit"] == 0 for item in suites.values()) and (
        reproducer["exit"] == 0
        and parsed.get("probe_count") == 17
        and parsed.get("all_conformant") is True
    )
    add_result(
        "BUILTIN-SUITES-023",
        "Experiment",
        conforms,
        {
            "suite_exit": {name: item["exit"] for name, item in suites.items()},
            "expected_test_counts": {"tests": 14, "tests_v021": 11, "tests_v022": 15, "tests_v023": 16},
            "closure_reproducer_exit": reproducer["exit"],
            "closure_probe_count": parsed.get("probe_count"),
            "closure_all_conformant": parsed.get("all_conformant"),
        },
    )


def probe_fixture_matrix(root: Path) -> None:
    schema_path = root / SCHEMA_REL
    manifest = load_json(root / "fixtures-v0.2.3" / "manifest.json")
    mismatches: dict[str, Any] = {}
    for name, expected in manifest["fixtures"].items():
        actual = V.validate_path(root / "fixtures-v0.2.3" / f"{name}.json", schema_path, root).to_dict()
        differing = {
            key: {"expected": value, "actual": actual[key]}
            for key, value in expected.items()
            if actual[key] != value
        }
        if differing:
            mismatches[name] = differing
    add_result(
        "FIXTURE-MATRIX-023",
        "Experiment",
        len(manifest["fixtures"]) == 33 and not mismatches,
        {"fixture_count": len(manifest["fixtures"]), "mismatches": mismatches},
    )


def closure_status(envelope: Any) -> str:
    reference = "a" * 64
    artifact = json_bytes({"artifact_envelope": envelope})
    return V._artifact_closure({"run-spec": reference}, SyntheticStore({reference: artifact})).status


def probe_envelope_shape_matrix() -> None:
    unsupported = "urn:unsupported:closure:9"
    valid = {
        "spec_id": unsupported,
        "artifact_type": "future-run-spec",
        "version": "9.0",
        "edges": [],
    }
    cases: dict[str, tuple[Any, str]] = {
        "shape-valid-future-type": (copy.deepcopy(valid), V.UNKNOWN),
        "shape-valid-known-type": ({**copy.deepcopy(valid), "artifact_type": "run-spec"}, V.UNKNOWN),
        "shape-valid-future-version": ({**copy.deepcopy(valid), "version": "future"}, V.UNKNOWN),
        "envelope-not-object": ([], V.FAIL),
    }
    for member in ("spec_id", "artifact_type", "version", "edges"):
        item = copy.deepcopy(valid)
        item.pop(member)
        cases[f"missing-{member}"] = (item, V.FAIL)
    for member in ("spec_id", "artifact_type", "version"):
        for label, value in (("null", None), ("integer", 1), ("boolean", True), ("array", []), ("object", {}), ("empty", "")):
            item = copy.deepcopy(valid)
            item[member] = value
            cases[f"{member}-{label}"] = (item, V.FAIL)
    for label, value in (("null", None), ("string", "[]"), ("object", {}), ("integer", 1), ("boolean", True)):
        item = copy.deepcopy(valid)
        item["edges"] = value
        cases[f"edges-{label}"] = (item, V.FAIL)

    edge = {
        "role": "future-child",
        "expected_type": "future-artifact",
        "sha256": "sha256:" + "b" * 64,
    }
    valid_edge = {**copy.deepcopy(valid), "edges": [edge]}
    cases["shape-valid-edge-unresolved-under-unsupported-spec"] = (valid_edge, V.UNKNOWN)
    for label, value in (("null", None), ("array", []), ("string", "x"), ("integer", 1)):
        item = copy.deepcopy(valid_edge)
        item["edges"] = [value]
        cases[f"edge-{label}"] = (item, V.FAIL)
    for member in ("role", "expected_type", "sha256"):
        item = copy.deepcopy(valid_edge)
        item["edges"][0].pop(member)
        cases[f"edge-missing-{member}"] = (item, V.FAIL)
    item = copy.deepcopy(valid_edge)
    item["edges"][0]["extra"] = 1
    cases["edge-extra-member"] = (item, V.FAIL)
    for member in ("role", "expected_type"):
        for label, value in (("null", None), ("integer", 1), ("boolean", True), ("empty", "")):
            item = copy.deepcopy(valid_edge)
            item["edges"][0][member] = value
            cases[f"edge-{member}-{label}"] = (item, V.FAIL)
    for label, value in (
        ("null", None),
        ("integer", 1),
        ("empty", ""),
        ("short", "a" * 63),
        ("bad-prefix", "sha512:" + "a" * 64),
        ("nonhex", "z" * 64),
    ):
        item = copy.deepcopy(valid_edge)
        item["edges"][0]["sha256"] = value
        cases[f"edge-sha256-{label}"] = (item, V.FAIL)
    item = copy.deepcopy(valid_edge)
    item["edges"].append(copy.deepcopy(edge))
    item["edges"][1]["sha256"] = "sha256:" + "c" * 64
    cases["edge-duplicate-role"] = (item, V.FAIL)

    supported_wrong_version = copy.deepcopy(valid)
    supported_wrong_version["spec_id"] = V.ARTIFACT_CLOSURE_SPEC_ID
    cases["supported-wrong-version"] = (supported_wrong_version, V.FAIL)
    supported_unknown_type = copy.deepcopy(valid)
    supported_unknown_type["spec_id"] = V.ARTIFACT_CLOSURE_SPEC_ID
    supported_unknown_type["version"] = V.VALIDATOR_VERSION
    cases["supported-unknown-type"] = (supported_unknown_type, V.FAIL)

    observations = {name: closure_status(value) for name, (value, _) in cases.items()}
    failures = {
        name: {"expected": expected, "actual": observations[name]}
        for name, (_, expected) in cases.items()
        if observations[name] != expected
    }
    fail_count = sum(1 for _, expected in cases.values() if expected == V.FAIL)
    unknown_count = sum(1 for _, expected in cases.values() if expected == V.UNKNOWN)
    add_result(
        "ENVELOPE-SHAPE-MATRIX-023",
        "Negative unit test",
        len(cases) >= 50 and not failures,
        {
            "case_count": len(cases),
            "expected_fail": fail_count,
            "expected_unknown": unknown_count,
            "mismatches": failures,
            "v022_minimal_case_actual": observations["missing-artifact_type"],
            "unsupported_with_valid_edge_missing_child_actual": observations[
                "shape-valid-edge-unresolved-under-unsupported-spec"
            ],
        },
    )


def probe_supported_edge_relations(root: Path) -> None:
    a, b, c = "a" * 64, "b" * 64, "c" * 64
    spec = V.ARTIFACT_CLOSURE_SPEC_ID

    def env(artifact_type: str, edges: list[dict[str, str]]) -> bytes:
        return json_bytes(
            {
                "artifact_envelope": {
                    "spec_id": spec,
                    "artifact_type": artifact_type,
                    "version": V.VALIDATOR_VERSION,
                    "edges": edges,
                }
            }
        )

    wrong_relation = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {
                a: env("run-spec", [{"role": "fairness-spec", "expected_type": "ed25519-public-key", "sha256": b}]),
                b: env("ed25519-public-key", []),
            }
        ),
    ).status
    missing_child = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {a: env("run-spec", [{"role": "fairness-spec", "expected_type": "fairness-spec", "sha256": b}])}
        ),
    ).status
    child_type_mismatch = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {
                a: env("run-spec", [{"role": "fairness-spec", "expected_type": "fairness-spec", "sha256": b}]),
                b: env("ed25519-public-key", []),
            }
        ),
    ).status
    duplicate_role = V._artifact_closure(
        {"run-spec": a},
        SyntheticStore(
            {
                a: env(
                    "run-spec",
                    [
                        {"role": "fairness-spec", "expected_type": "fairness-spec", "sha256": b},
                        {"role": "fairness-spec", "expected_type": "fairness-spec", "sha256": c},
                    ],
                ),
                b: env("fairness-spec", []),
                c: env("fairness-spec", []),
            }
        ),
    ).status
    supported_path = root / "artifacts-v0.2.3" / "run-standard.v0.2.3.json"
    supported_ref = f"sha256:{sha256(supported_path.read_bytes())}"
    supported = V._artifact_closure({"run-spec": supported_ref}, V.ArtifactIndex(root)).status
    evidence = {
        "supported-run-standard": supported,
        "wrong-parent-role-child-relation": wrong_relation,
        "missing-transitive-child": missing_child,
        "resolved-child-type-mismatch": child_type_mismatch,
        "duplicate-edge-role": duplicate_role,
    }
    add_result(
        "SUPPORTED-EDGE-RELATIONS-023",
        "Negative unit test",
        evidence
        == {
            "supported-run-standard": V.PASS,
            "wrong-parent-role-child-relation": V.FAIL,
            "missing-transitive-child": V.FAIL,
            "resolved-child-type-mismatch": V.FAIL,
            "duplicate-edge-role": V.FAIL,
        },
        evidence,
    )


def probe_edge_scope_ambiguity(root: Path) -> None:
    """Confirm the frozen Definition/interface has two reasonable readings.

    This is not an executable acceptance failure: FAIL and UNKNOWN both block
    admission.  It is a status-uniqueness problem in the normative artifact.
    """

    witness_path = (
        root
        / "artifacts-v0.2.3"
        / "closure-classification"
        / "shape-valid-unsupported-future-type.json"
    )
    witness = load_json(witness_path)
    envelope = witness["artifact_envelope"]
    witness_ref = f"sha256:{sha256(witness_path.read_bytes())}"
    actual = V._artifact_closure(
        {"run-spec": witness_ref}, V.ArtifactIndex(root)
    ).status
    closure_spec = load_json(
        root / "artifacts-v0.2.3" / "artifact-closure-spec.v0.2.3.json"
    )
    expected_type_rule = closure_spec["edge_shape"]["expected_type"]
    parent_relation = V.EDGE_RELATIONS.get(envelope["artifact_type"])
    source_text = (root / VALIDATOR_REL).read_text(encoding="utf-8")
    current_text = (root / "CURRENT-v0.2.3-candidate.md").read_text(encoding="utf-8")
    diff_text = (root / "SCHEMA-DIFF-v0.2.2-to-v0.2.3.md").read_text(encoding="utf-8")

    evidence = {
        "witness": {
            "artifact_type": envelope["artifact_type"],
            "spec_id": envelope["spec_id"],
            "edge": envelope["edges"][0],
            "generic_shape_valid": V._envelope_shape(envelope) is not None,
        },
        "parent_relation": parent_relation,
        "validator_actual": actual,
        "frozen_definition_wording": expected_type_rule,
        "definition_status": closure_spec.get("status"),
        "generic_reading": (
            "edge_shape.expected_type applies during generic EnvelopeShape; "
            "the parent relation is undefined, yielding FAIL or an undefined judgment"
        ),
        "supported_only_reading": (
            "parent/role/child relation is checked only after supported spec_id "
            "dispatch, yielding UNKNOWN"
        ),
        "source_supported_only": "checked only for the supported" in source_text,
        "current_supported_only": "支援的 spec 才進一步驗" in current_text,
        "schema_diff_supported_only": "只有 supported spec 才檢查" in diff_text,
        "admission_effect": "both FAIL and UNKNOWN block admission",
    }
    ambiguity_confirmed = (
        evidence["witness"]["generic_shape_valid"]
        and envelope["spec_id"] != V.ARTIFACT_CLOSURE_SPEC_ID
        and parent_relation is None
        and actual == V.UNKNOWN
        and expected_type_rule == "must equal the pinned parent-type/role relation"
        and evidence["definition_status"] == "Definition-interface-candidate"
        and evidence["source_supported_only"]
        and evidence["current_supported_only"]
        and evidence["schema_diff_supported_only"]
    )
    add_result(
        "CLOSURE-EDGE-SCOPE-01",
        "Definition ambiguity / promotion blocker; admission-blocking under both readings",
        ambiguity_confirmed,
        evidence,
    )


def probe_signed_reference_cases(root: Path, key: Ed25519PrivateKey) -> None:
    two_sat_contract = load_json(root / "artifacts-v0.2.3" / "contract-2sat.v0.2.3.json")

    def run_spec(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["validation_receipt"]["run_spec_ref"] = f"sha256:{V.PINNED_RUN_STANDARD_HASH}"

    def sandbox(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["validation_receipt"]["capability_sandbox_ref"] = f"sha256:{V.PINNED_RUN_STANDARD_HASH}"

    def contract(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["problem"]["contract"]["sha256"] = f"sha256:{V.PINNED_TWO_SAT_CONTRACT_HASH}"
        record["problem"]["contract"]["id"] = two_sat_contract["contract_id"]
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

    def rule(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        rule_ref = f"sha256:{V.PINNED_TWO_SAT_RULE_HASH}"
        admissibility = record["mechanism"]["admissibility"]
        for field in ("builder_ref", "step_ref", "decode_ref"):
            admissibility[field] = rule_ref
        for event in record["events"]:
            event["transition_rule_ref"] = rule_ref

    no_change = lambda _record, _trace: None

    def omit_contract(values: dict[str, str]) -> dict[str, str]:
        values.pop("contract")
        return values

    def duplicate_role_alias(values: dict[str, str]) -> dict[str, str]:
        values["extra-receipt-role"] = V.PINNED_TRACE_PUBLIC_KEY_HASH
        return values

    cases = {
        "run-spec-robust-to-standard": signed_copy_case(root, key, "run-spec", "robust-legit", run_spec),
        "sandbox-to-run-spec": signed_copy_case(root, key, "sandbox", "legit", sandbox),
        "parity-contract-to-2sat-contract": signed_copy_case(root, key, "contract", "legit", contract),
        "invariant-to-contract": signed_copy_case(root, key, "invariant", "legit", invariant),
        "parity-rule-to-2sat-rule": signed_copy_case(root, key, "rule", "legit", rule),
        "signed-map-omits-contract": signed_copy_case(
            root, key, "map-omit", "legit", no_change, map_mode="expected", map_transform=omit_contract
        ),
        "signed-map-extra-role": signed_copy_case(
            root, key, "map-extra", "legit", no_change, map_mode="expected", map_transform=duplicate_role_alias
        ),
    }
    failures = {
        name: item
        for name, item in cases.items()
        if not (
            item["schema_valid"]
            and item["signature_status"] == V.PASS
            and not item["record_accepted"]
        )
    }
    add_result(
        "SIGNED-REFERENCE-MATRIX-023",
        "Negative unit test",
        not failures,
        {"case_count": len(cases), "failures": failures, "cases": cases},
    )


def probe_oracle_declaration_binding(root: Path, key: Ed25519PrivateKey) -> None:
    """Check whether signed oracle name/checks are bound to problem family."""

    two_sat_oracle = load_fixture(root, "2sat-sat")["mechanism"]["oracle"]
    two_sat_unsat_oracle = load_fixture(root, "2sat-unsat")["mechanism"]["oracle"]
    frozen_report = load_json(root / "i0-run-report.v0.2.3-candidate.json")
    family_binding_claim = frozen_report["candidate_scope"][
        "family_bound_contract_oracle_rule_invariant"
    ]

    def name_only(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["mechanism"]["oracle"]["name"] = two_sat_oracle["name"]

    def checks_only(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["mechanism"]["oracle"]["checks"] = copy.deepcopy(two_sat_oracle["checks"])

    def both(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["mechanism"]["oracle"]["name"] = two_sat_oracle["name"]
        record["mechanism"]["oracle"]["checks"] = copy.deepcopy(two_sat_oracle["checks"])

    def sat_declares_unsat_check(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["mechanism"]["oracle"]["checks"] = copy.deepcopy(
            two_sat_unsat_oracle["checks"]
        )

    def unsat_declares_sat_check(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["mechanism"]["oracle"]["checks"] = copy.deepcopy(two_sat_oracle["checks"])

    variants = {
        "name-only": signed_copy_case(root, key, "oracle-name", "legit", name_only),
        "checks-only": signed_copy_case(root, key, "oracle-checks", "legit", checks_only),
        "name-and-checks": signed_copy_case(root, key, "oracle-both", "legit", both),
        "2sat-sat-declares-unsat-check": signed_copy_case(
            root, key, "oracle-sat-as-unsat", "2sat-sat", sat_declares_unsat_check
        ),
        "2sat-unsat-declares-sat-check": signed_copy_case(
            root, key, "oracle-unsat-as-sat", "2sat-unsat", unsat_declares_sat_check
        ),
    }
    accepted = {
        name: item
        for name, item in variants.items()
        if (
            item["schema_valid"]
            and item["signature_status"] == V.PASS
            and item["closure_status"] == V.PASS
            and item["record_accepted"]
        )
    }
    witness_confirmed = family_binding_claim is True and len(accepted) == len(variants)
    add_result(
        "ORACLE-DECL-FAMILY-01",
        (
            "Counterexample to family-binding of accepted oracle name/checks; "
            "if those fields are annotations, the frozen interface leaves that status undefined"
        ),
        witness_confirmed,
        {
            "base_family": "PARITY",
            "substituted_declaration_source": "2-SAT fixture",
            "shared_source_hash": f"sha256:{V.PINNED_ORACLE_HASH}",
            "frozen_family_binding_claim": family_binding_claim,
            "accepted_variants": sorted(accepted),
            "variants": variants,
            "execution_boundary": (
                "the validator still selects and executes parity_oracle from problem.family; "
                "this witness concerns accepted declaration/provenance consistency, not oracle correctness"
            ),
            "repair_obligation": (
                "bind name/checks to family, or normatively mark them nonsemantic annotations "
                "and remove any claim that they identify the executed oracle"
            ),
        },
    )


def probe_trace_signature_pairing(root: Path) -> None:
    schema_bytes = (root / SCHEMA_REL).read_bytes()
    record = load_fixture(root, "legit")
    source = load_fixture(root, "2sat-sat")
    receipt = record["validation_receipt"]
    receipt["trace_sha256"] = source["validation_receipt"]["trace_sha256"]
    receipt["trace_authenticity_ref"] = source["validation_receipt"]["trace_authenticity_ref"]
    closure_status = recompute_receipt_closure(record, root)
    transplanted = validate_object(record, schema_bytes, root)
    signature_status = V._trace_authenticity_status(record, V.ArtifactIndex(root))

    builtins: dict[str, Any] = {}
    for name in ("bad-trace-signature", "tampered-record", "tampered-trace"):
        builtins[name] = report_dict(
            V.validate_path(root / "fixtures-v0.2.3" / f"{name}.json", root / SCHEMA_REL, root)
        )
    evidence = {
        "valid-signature-trace-auth-transplant": {
            "signature_status": signature_status,
            "closure_status": closure_status,
            **report_dict(transplanted),
        },
        "builtins": builtins,
    }
    conforms = (
        signature_status == V.PASS
        and not transplanted.record_accepted
        and all(not item["record_accepted"] for item in builtins.values())
    )
    add_result("TRACE-SIGNATURE-PAIRING-023", "Negative unit test", conforms, evidence)


def probe_schema_and_raw_domain(root: Path) -> None:
    schema_path = root / SCHEMA_REL
    negative_zero = V.validate_path(root / "fixtures-v0.2.3" / "negative-zero.json", schema_path, root)
    surrogate = V.validate_path(root / "fixtures-v0.2.3" / "unpaired-surrogate.json", schema_path, root)
    wrong_schema = V.validate_bytes((root / "fixtures-v0.2.3" / "legit.json").read_bytes(), b"{}", root)
    duplicate_key = V.validate_bytes(b'{"schema_version":"0.2.3","schema_version":"0.2.3"}', schema_path.read_bytes(), root)
    newline_equal = V.canonical_json_bytes(json.loads(r'{"x":"\n"}')) == V.canonical_json_bytes(
        json.loads(r'{"x":"\u000a"}')
    )
    evidence = {
        "public_validate_record_present": hasattr(V, "validate_record"),
        "negative_zero": report_dict(negative_zero),
        "surrogate": report_dict(surrogate),
        "wrong_schema_bytes": report_dict(wrong_schema),
        "duplicate_record_key": report_dict(duplicate_key),
        "equivalent_newline_spellings": newline_equal,
    }
    conforms = (
        not hasattr(V, "validate_record")
        and not negative_zero.structural_ok
        and "record-parse" in evidence["negative_zero"]["issue_codes"]
        and not surrogate.record_accepted
        and "canonical-unicode-scalar" in evidence["surrogate"]["issue_codes"]
        and not wrong_schema.structural_ok
        and "schema-byte-pin-mismatch" in evidence["wrong_schema_bytes"]["issue_codes"]
        and not duplicate_key.structural_ok
        and "record-parse" in evidence["duplicate_record_key"]["issue_codes"]
        and newline_equal
    )
    add_result("SCHEMA-RAW-DOMAIN-023", "Conformance", conforms, evidence)


def probe_derived_mirrors(root: Path) -> None:
    expected_codes = {
        "fabricated-problem-size": "problem-size-derivation",
        "fabricated-failure-frontier": "failure-frontier-derivation",
        "declared-answer-access-mismatch": "answer-access-family-binding",
        "fabricated-states-999": "derived-gate-mismatch",
        "fabricated-transition-digest": "derived-gate-mismatch",
    }
    evidence: dict[str, Any] = {}
    conforms = True
    for name, required in expected_codes.items():
        report = V.validate_path(root / "fixtures-v0.2.3" / f"{name}.json", root / SCHEMA_REL, root)
        item = report_dict(report)
        evidence[name] = item
        conforms = conforms and not report.record_accepted and required in item["issue_codes"]
    add_result("DERIVED-MIRRORS-023", "Negative unit test", conforms, evidence)


def probe_resource_mirrors(root: Path, key: Ed25519PrivateKey) -> None:
    def change_space(record: dict[str, Any], _trace: dict[str, Any]) -> None:
        record["ledger"]["space_bytes"]["peak"] += 1

    mismatch = signed_copy_case(
        root,
        key,
        "resource-mismatch",
        "legit",
        change_space,
        sync_resource_samples=False,
    )
    attested = signed_copy_case(
        root,
        key,
        "resource-attested",
        "legit",
        change_space,
        sync_resource_samples=True,
    )
    conforms = (
        mismatch["schema_valid"]
        and mismatch["signature_status"] == V.PASS
        and not mismatch["record_accepted"]
        and attested["schema_valid"]
        and attested["signature_status"] == V.PASS
        and attested["record_accepted"]
    )
    add_result(
        "RESOURCE-MIRRORS-023",
        "Scoped Observation",
        conforms,
        {
            "record_trace_mismatch": mismatch,
            "matching_signed_raw_measurement": attested,
            "scope": "acceptance authenticates the test signer's raw measurement; it does not independently measure hardware",
        },
    )


def probe_gate_applicability(root: Path) -> None:
    schema = V._load_json_object_bytes((root / SCHEMA_REL).read_bytes(), source="schema")
    checker = Draft202012Validator(schema)
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
        baseline = load_fixture(root, name)
        for gate, current in baseline["validation_receipt"]["gates"].items():
            total += 1
            mutated = copy.deepcopy(baseline)
            mutated["validation_receipt"]["admission_pass"] = False
            mutated["validation_receipt"]["final_completion"] = False
            mutated["validation_receipt"]["gates"][gate] = (
                V.PASS if current == V.NOT_APPLICABLE else V.NOT_APPLICABLE
            )
            if checker.is_valid(mutated):
                schema_accepted.append(f"{name}:{gate}")
    add_result(
        "GATE-APPLICABILITY-023",
        "Schema conformance",
        total == len(fixture_names) * len(V.GATE_KEYS) and not schema_accepted,
        {"mutations_checked": total, "schema_accepted": schema_accepted},
    )


def probe_regeneration(root: Path) -> None:
    outputs = sorted(
        list((root / "fixtures-v0.2.3").rglob("*.json"))
        + list((root / "artifacts-v0.2.3").rglob("*.json"))
    )
    before = {path.relative_to(root).as_posix(): path.read_bytes() for path in outputs}
    schema_before = (root / SCHEMA_REL).read_bytes()
    schema_run = run_command(root, ["scripts/build_schema_v023.py"])
    fixture_run = run_command(
        root,
        ["scripts/generate_fixtures_v023.py", "--signing-key", str(FIXTURE_KEY_PATH)],
    )
    after_paths = sorted(
        list((root / "fixtures-v0.2.3").rglob("*.json"))
        + list((root / "artifacts-v0.2.3").rglob("*.json"))
    )
    after = {path.relative_to(root).as_posix(): path.read_bytes() for path in after_paths}
    mismatches = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
    schema_equal = (root / SCHEMA_REL).read_bytes() == schema_before
    add_result(
        "ISOLATED-REGENERATION-023",
        "Experiment",
        len(before) == 107
        and schema_run["exit"] == 0
        and fixture_run["exit"] == 0
        and schema_equal
        and not mismatches,
        {
            "output_count": len(before),
            "schema_builder_exit": schema_run["exit"],
            "fixture_generator_exit": fixture_run["exit"],
            "schema_byte_identical": schema_equal,
            "fixture_artifact_mismatches": mismatches,
        },
    )


def main() -> int:
    manifest_bytes, entries, frozen, before_metadata = pin_frozen_bytes()
    probe_identity(manifest_bytes, entries, frozen)

    with tempfile.TemporaryDirectory(prefix="pnp-glc-v023-conformance-") as temporary:
        snapshot_root = Path(temporary) / "pnp-glc-i0"
        materialize_snapshot(snapshot_root, frozen)
        probe_builtin_suites(snapshot_root)
        probe_fixture_matrix(snapshot_root)
        probe_envelope_shape_matrix()
        probe_supported_edge_relations(snapshot_root)
        probe_edge_scope_ambiguity(snapshot_root)
        key = load_fixture_key(snapshot_root)
        probe_signed_reference_cases(snapshot_root, key)
        probe_oracle_declaration_binding(snapshot_root, key)
        probe_trace_signature_pairing(snapshot_root)
        probe_schema_and_raw_domain(snapshot_root)
        probe_derived_mirrors(snapshot_root)
        probe_resource_mirrors(snapshot_root, key)
        probe_gate_applicability(snapshot_root)
        probe_regeneration(snapshot_root)

    after_metadata = frozen_metadata(entries)
    changed = sorted(
        path
        for path in set(before_metadata) | set(after_metadata)
        if before_metadata.get(path) != after_metadata.get(path)
    )
    add_result(
        "FROZEN-PATHS-READONLY-023",
        "Provenance",
        not changed,
        {
            "manifest_listed_paths": len(entries),
            "manifest_file_also_monitored": True,
            "changed_frozen_paths": changed,
            "candidate_root_writes_in_monitored_domain": len(changed),
            "nonmanifest_successor_paths": "out of provenance domain by design",
        },
    )

    unexpected = [result["probe_id"] for result in RESULTS if not result["conforms"]]
    blockers = [
        result["probe_id"]
        for result in RESULTS
        if result["probe_id"] in {
            "CLOSURE-EDGE-SCOPE-01",
            "ORACLE-DECL-FAMILY-01",
        }
        and result["conforms"]
    ]
    executable_blockers = [
        blocker for blocker in blockers if blocker == "ORACLE-DECL-FAMILY-01"
    ]
    payload = {
        "scope": "local read-only software conformance review; no network; no P/NP inference",
        "overall_disposition": (
            "FAIL / " + " + ".join(blockers)
            if blockers
            else "bounded PASS" if not unexpected else "FAIL / unexpected conformance result"
        ),
        "executable_conformance_disposition": (
            "FAIL / " + " + ".join(executable_blockers)
            if executable_blockers
            else "bounded PASS" if not unexpected else "FAIL / unexpected conformance result"
        ),
        "promotion_blockers": blockers,
        "probe_groups": len(RESULTS),
        "unexpected_results": unexpected,
        "candidate_root_writes": len(changed),
        "provenance_domain": "121 v0.2.3 manifest paths plus the manifest file",
        "results": RESULTS,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
