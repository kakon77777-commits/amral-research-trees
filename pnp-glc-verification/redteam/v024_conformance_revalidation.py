#!/usr/bin/env python3
"""AI-2 bounded read-only conformance review for frozen PNP-GLC I0 v0.2.4.

The candidate root is never written. The 153 manifest-listed paths are pinned
once, all execution and valid-signature variants run in a temporary snapshot,
and the same 153 paths plus the manifest file are checked again afterward.
No network access is used and no P/NP inference is made.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import re
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
MANIFEST = ROOT / "SHA256SUMS-v0.2.4-candidate.txt"
SCHEMA_REL = "schemas/run-record.schema.v0.2.4-candidate.json"
VALIDATOR_REL = "src/pnp_glc_i0/semantic_validator_v024.py"
KEY = ROOT.parents[1] / "work" / "i0-v021-trace-signing-key.pem"

EXPECTED_CORE = {
    "manifest": "73ed3607ead3f50502dcefa3142dffee01aac8576c045f05ca96deb9669f77fe",
    SCHEMA_REL: "16ebcc7de4196d0c46fc9c309f2060f856e321c0012c5b775390c04234f9dcc8",
    VALIDATOR_REL: "b744c9c20c510fe39f132e0dfb4aac50e6e3e573b48b7f1ae19494f5d5195fed",
    "artifacts-v0.2.4/candidate-projection-spec.v0.2.4.json":
        "ccf57716e63ad6b627f48688925054975254a88344e7f84ecbec9cf0145b9d6d",
    "artifacts-v0.2.4/artifact-closure-spec.v0.2.4.json":
        "579b6f7da8be3712fe6130ad900cf0cba189496100548cbf87655687a7690588",
    "artifacts-v0.2.4/evidence-role-spec.v0.2.4.json":
        "4efc4c71c6275227b14429e58fcecc4e949459918315d27cc476765c7d24d850",
    "fixtures-v0.2.4/manifest.json":
        "5f79e8dc3ebad4a9ba8c32c7092cdf52307220d08ef1d83efd399b12b00b7ab1",
    "scripts/reproduce_closure_class_v024.py":
        "5f0fb64d1bb6da17804088260fca94a92f21dd4c2f5fac1a9605f9f3bad303db",
    "scripts/reproduce_oracle_decl_family_v024.py":
        "0a0ea8607d2e07e6189acc52b698e781cf742c6523c4d46ff3f02330af1b779b",
    "i0-run-report.v0.2.4-candidate.json":
        "fc25c0e04d44accc0f5232b4f852056b870d82059f7542d4307ec966c0eb9300",
}

PREDECESSORS = {
    "v0.2.2": (
        ROOT / "SHA256SUMS-v0.2.2-candidate.txt",
        "ab63a7d921f04e71bdfc8cca0f681e81e9a1ba2aaac89e1674a6d0c883a8ec0b",
        98,
    ),
    "v0.2.3": (
        ROOT / "SHA256SUMS-v0.2.3-candidate.txt",
        "7aafa47149ad3bca042a62fc8c708d61d5ad41a7acf7f4f4a897318f0063c817",
        121,
    ),
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


def parse_manifest(path: Path) -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    errors: list[str] = []
    try:
        lines = path.read_bytes().decode("utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        return {}, [str(error)]
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            errors.append(f"line {number}: malformed")
            continue
        digest, relative = parts
        relative = relative.lstrip("*").replace("\\", "/")
        if not re.fullmatch(r"[0-9A-Fa-f]{64}", digest):
            errors.append(f"line {number}: bad digest")
            continue
        if relative in entries:
            errors.append(f"line {number}: duplicate {relative}")
            continue
        target = (ROOT / relative).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"line {number}: path escapes root: {relative}")
            continue
        entries[relative] = digest.lower()
    return entries, errors


def verify_manifest(path: Path) -> dict[str, Any]:
    entries, format_errors = parse_manifest(path)
    missing: list[str] = []
    mismatches: dict[str, dict[str, str]] = {}
    for relative, expected in entries.items():
        target = ROOT / relative
        if not target.is_file():
            missing.append(relative)
            continue
        actual = sha256(target.read_bytes())
        if actual != expected:
            mismatches[relative] = {"expected": expected, "actual": actual}
    return {
        "manifest_sha256": sha256(path.read_bytes()) if path.is_file() else None,
        "entries": len(entries),
        "format_errors": format_errors,
        "missing": missing,
        "mismatches": mismatches,
    }


def pin_frozen() -> tuple[dict[str, str], dict[str, bytes], dict[str, tuple[int, int, str]]]:
    entries, errors = parse_manifest(MANIFEST)
    if errors:
        raise ValueError(errors)
    frozen: dict[str, bytes] = {}
    metadata: dict[str, tuple[int, int, str]] = {}
    for relative, expected in entries.items():
        path = ROOT / relative
        data = path.read_bytes()
        actual = sha256(data)
        if actual != expected:
            raise ValueError(f"manifest mismatch: {relative}: {actual} != {expected}")
        stat = path.stat()
        frozen[relative] = data
        metadata[relative] = (stat.st_size, stat.st_mtime_ns, actual)
    manifest_stat = MANIFEST.stat()
    metadata["<manifest>"] = (
        manifest_stat.st_size,
        manifest_stat.st_mtime_ns,
        sha256(MANIFEST.read_bytes()),
    )
    return entries, frozen, metadata


def frozen_metadata(entries: Mapping[str, str]) -> dict[str, tuple[int, int, str]]:
    result: dict[str, tuple[int, int, str]] = {}
    for relative in entries:
        path = ROOT / relative
        if not path.is_file():
            result[relative] = (-1, -1, "missing")
            continue
        stat = path.stat()
        result[relative] = (stat.st_size, stat.st_mtime_ns, sha256(path.read_bytes()))
    if MANIFEST.is_file():
        stat = MANIFEST.stat()
        result["<manifest>"] = (
            stat.st_size,
            stat.st_mtime_ns,
            sha256(MANIFEST.read_bytes()),
        )
    else:
        result["<manifest>"] = (-1, -1, "missing")
    return result


def materialize_snapshot(target: Path, frozen: Mapping[str, bytes]) -> None:
    """Create a version-bounded runtime copy, then overwrite exact frozen bytes."""

    for source in sorted(ROOT.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT)
        lowered = relative.as_posix().lower()
        if (
            "__pycache__" in relative.parts
            or source.suffix.lower() == ".pyc"
            or "v0.2.5" in lowered
            or "v025" in lowered
            or "_ai2-" in lowered
        ):
            continue
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    for relative, data in frozen.items():
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    parent_schema = ROOT.parent / "run-record.schema.json"
    (target.parent / "run-record.schema.json").write_bytes(parent_schema.read_bytes())


def import_file(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_command(root: Path, arguments: list[str], timeout: int = 180) -> dict[str, Any]:
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
        timeout=timeout,
        check=False,
    )
    return {
        "exit": completed.returncode,
        "output": completed.stdout,
        "tail": completed.stdout[-2000:],
    }


def report_dict(report: Any) -> dict[str, Any]:
    return {
        "structural_ok": report.structural_ok,
        "semantic_ok": report.semantic_ok,
        "admission_pass": report.admission_pass,
        "final_completion": report.final_completion,
        "record_accepted": report.record_accepted,
        "issue_codes": sorted({issue.code for issue in report.issues}),
    }


def main() -> int:
    entries, frozen, before_metadata = pin_frozen()

    current = verify_manifest(MANIFEST)
    core_actual = {
        relative: sha256(frozen[relative])
        for relative in EXPECTED_CORE
        if relative != "manifest"
    }
    core_expected = {
        relative: expected
        for relative, expected in EXPECTED_CORE.items()
        if relative != "manifest"
    }
    predecessor_evidence: dict[str, Any] = {}
    predecessors_ok = True
    for name, (path, expected_hash, expected_count) in PREDECESSORS.items():
        evidence = verify_manifest(path)
        evidence["expected_manifest_sha256"] = expected_hash
        evidence["expected_entries"] = expected_count
        predecessor_evidence[name] = evidence
        predecessors_ok = predecessors_ok and (
            evidence["manifest_sha256"] == expected_hash
            and evidence["entries"] == expected_count
            and not evidence["format_errors"]
            and not evidence["missing"]
            and not evidence["mismatches"]
        )
    identity_ok = (
        current["manifest_sha256"] == EXPECTED_CORE["manifest"]
        and current["entries"] == 153
        and not current["format_errors"]
        and not current["missing"]
        and not current["mismatches"]
        and core_actual == core_expected
        and predecessors_ok
    )
    add_result(
        "IDENTITY-024",
        "Observation",
        identity_ok,
        {
            "v0.2.4": current,
            "core_hashes_match": core_actual == core_expected,
            "predecessors": predecessor_evidence,
        },
    )

    with tempfile.TemporaryDirectory(prefix="pnp-glc-v024-ai2-") as temporary:
        snapshot = Path(temporary) / "pnp-glc-i0"
        materialize_snapshot(snapshot, frozen)

        suites: dict[str, Any] = {}
        expected_counts = {
            "tests": 14,
            "tests_v021": 11,
            "tests_v022": 15,
            "tests_v023": 16,
            "tests_v024": 19,
        }
        suites_ok = True
        for suite, expected_count in expected_counts.items():
            run = run_command(snapshot, ["-m", "unittest", "discover", "-s", suite, "-q"])
            match = re.search(r"Ran (\d+) tests?", run["output"])
            count = int(match.group(1)) if match else None
            suites[suite] = {"exit": run["exit"], "tests": count, "tail": run["tail"]}
            suites_ok = suites_ok and run["exit"] == 0 and count == expected_count

        closure_run = run_command(
            snapshot,
            ["scripts/reproduce_closure_class_v024.py", str(snapshot)],
        )
        oracle_run = run_command(
            snapshot,
            ["scripts/reproduce_oracle_decl_family_v024.py", str(snapshot)],
        )
        try:
            closure_json = json.loads(closure_run["output"])
        except json.JSONDecodeError:
            closure_json = {}
        try:
            oracle_json = json.loads(oracle_run["output"])
        except json.JSONDecodeError:
            oracle_json = {}
        closure_target_ok = (
            closure_run["exit"] == 0
            and closure_json.get("classification_probe_count") == 20
            and closure_json.get("scope_check_count") == 7
            and closure_json.get("all_conformant") is True
            and closure_json.get("unexpected") == []
        )
        oracle_target_ok = (
            oracle_run["exit"] == 0
            and oracle_json.get("negative_probe_count") == 9
            and oracle_json.get("positive_control_count") == 3
            and oracle_json.get("all_conformant") is True
            and oracle_json.get("unexpected") == []
            and all(
                probe.get("trace_authenticity") == "pass"
                and probe.get("actual_family_oracle_status") == "pass"
                and probe.get("binding_issue_present") is True
                and probe.get("record_accepted") is False
                for probe in oracle_json.get("probes", [])
            )
        )
        add_result(
            "BUILTIN-REGRESSIONS-024",
            "Experiment",
            suites_ok and closure_target_ok and oracle_target_ok,
            {
                "test_suites": suites,
                "test_total": sum(expected_counts.values()),
                "closure": {
                    "exit": closure_run["exit"],
                    "classification_probe_count": closure_json.get("classification_probe_count"),
                    "scope_check_count": closure_json.get("scope_check_count"),
                    "unexpected": closure_json.get("unexpected"),
                },
                "oracle": {
                    "exit": oracle_run["exit"],
                    "negative_probe_count": oracle_json.get("negative_probe_count"),
                    "positive_control_count": oracle_json.get("positive_control_count"),
                    "unexpected": oracle_json.get("unexpected"),
                },
            },
        )

        sys.path.insert(0, str(snapshot / "src"))
        sys.path.insert(0, str(snapshot / "scripts"))
        import pnp_glc_i0.semantic_validator_v024 as validator
        generator = import_file(
            "ai2_generate_fixtures_v024",
            snapshot / "scripts" / "generate_fixtures_v024.py",
        )
        schema_path = snapshot / SCHEMA_REL
        schema_bytes = schema_path.read_bytes()
        schema = validator._load_json_object_bytes(schema_bytes, source="schema")
        schema_checker = Draft202012Validator(schema)

        fixture_manifest = validator.load_json(snapshot / "fixtures-v0.2.4" / "manifest.json")
        fixture_mismatches: dict[str, Any] = {}
        accepted_count = 0
        for name, expected in fixture_manifest["fixtures"].items():
            report = validator.validate_path(
                snapshot / "fixtures-v0.2.4" / f"{name}.json",
                schema_path,
                snapshot,
            ).to_dict()
            if report["record_accepted"]:
                accepted_count += 1
            differences = {
                key: {"expected": value, "actual": report.get(key)}
                for key, value in expected.items()
                if report.get(key) != value
            }
            if differences:
                fixture_mismatches[name] = differences
        add_result(
            "FIXTURE-MATRIX-024",
            "Experiment",
            len(fixture_manifest["fixtures"]) == 42
            and accepted_count == 6
            and not fixture_mismatches,
            {
                "fixture_count": len(fixture_manifest["fixtures"]),
                "accepted_count": accepted_count,
                "mismatches": fixture_mismatches,
            },
        )

        gate_profiles = (
            "legit",
            "robust-legit",
            "neutral-legit",
            "robust-neutral-legit",
            "2sat-sat",
            "2sat-unsat",
            "cheat",
            "unknown-gate",
        )
        gate_schema_accepts: list[str] = []
        gate_total = 0
        for name in gate_profiles:
            baseline = validator.load_json(
                snapshot / "fixtures-v0.2.4" / f"{name}.json"
            )
            for gate, current_value in baseline["validation_receipt"]["gates"].items():
                gate_total += 1
                mutated = copy.deepcopy(baseline)
                mutated["validation_receipt"]["admission_pass"] = False
                mutated["validation_receipt"]["final_completion"] = False
                mutated["validation_receipt"]["gates"][gate] = (
                    validator.PASS
                    if current_value == validator.NOT_APPLICABLE
                    else validator.NOT_APPLICABLE
                )
                if schema_checker.is_valid(mutated):
                    gate_schema_accepts.append(f"{name}:{gate}")
        add_result(
            "GATE-APPLICABILITY-024",
            "Schema conformance",
            gate_total == 8 * 18 and not gate_schema_accepts,
            {"mutations_checked": gate_total, "schema_accepted": gate_schema_accepts},
        )

        raw_evidence: dict[str, Any] = {}
        for name in ("negative-zero", "unpaired-surrogate"):
            raw_evidence[name] = report_dict(
                validator.validate_path(
                    snapshot / "fixtures-v0.2.4" / f"{name}.json",
                    schema_path,
                    snapshot,
                )
            )
        raw_evidence["wrong-schema"] = report_dict(
            validator.validate_bytes(
                (snapshot / "fixtures-v0.2.4" / "legit.json").read_bytes(),
                b"{}",
                snapshot,
            )
        )
        raw_evidence["duplicate-record-key"] = report_dict(
            validator.validate_bytes(
                b'{"schema_version":"0.2.4","schema_version":"0.2.4"}',
                schema_bytes,
                snapshot,
            )
        )
        derived_codes = {
            "fabricated-problem-size": "problem-size-derivation",
            "fabricated-failure-frontier": "failure-frontier-derivation",
            "declared-answer-access-mismatch": "answer-access-family-binding",
            "fabricated-states-999": "derived-gate-mismatch",
            "fabricated-transition-digest": "derived-gate-mismatch",
        }
        derived_evidence: dict[str, Any] = {}
        derived_ok = True
        for name, required_code in derived_codes.items():
            item = report_dict(
                validator.validate_path(
                    snapshot / "fixtures-v0.2.4" / f"{name}.json",
                    schema_path,
                    snapshot,
                )
            )
            derived_evidence[name] = item
            derived_ok = derived_ok and (
                not item["record_accepted"] and required_code in item["issue_codes"]
            )
        raw_ok = (
            not raw_evidence["negative-zero"]["structural_ok"]
            and "record-parse" in raw_evidence["negative-zero"]["issue_codes"]
            and not raw_evidence["unpaired-surrogate"]["record_accepted"]
            and "canonical-unicode-scalar"
            in raw_evidence["unpaired-surrogate"]["issue_codes"]
            and not raw_evidence["wrong-schema"]["structural_ok"]
            and "schema-byte-pin-mismatch" in raw_evidence["wrong-schema"]["issue_codes"]
            and not raw_evidence["duplicate-record-key"]["structural_ok"]
            and "record-parse" in raw_evidence["duplicate-record-key"]["issue_codes"]
            and not hasattr(validator, "validate_record")
        )
        add_result(
            "TRUST-BOUNDARY-DERIVATION-024",
            "Negative unit tests",
            raw_ok and derived_ok,
            {
                "public_validate_record_present": hasattr(validator, "validate_record"),
                "raw_schema": raw_evidence,
                "derived_mirrors": derived_evidence,
            },
        )

        regeneration_before = {
            relative: (snapshot / relative).read_bytes()
            for relative in entries
            if (snapshot / relative).is_file()
        }
        schema_build = run_command(snapshot, ["scripts/build_schema_v024.py"])
        fixture_build = run_command(
            snapshot,
            ["scripts/generate_fixtures_v024.py", "--signing-key", str(KEY)],
        )
        regeneration_mismatches = sorted(
            relative
            for relative, expected_bytes in regeneration_before.items()
            if not (snapshot / relative).is_file()
            or (snapshot / relative).read_bytes() != expected_bytes
        )
        generated_json_count = len(
            list((snapshot / "fixtures-v0.2.4").rglob("*.json"))
            + list((snapshot / "artifacts-v0.2.4").rglob("*.json"))
        )
        add_result(
            "ISOLATED-REGENERATION-024",
            "Experiment",
            schema_build["exit"] == 0
            and fixture_build["exit"] == 0
            and generated_json_count == 137
            and len(regeneration_before) == 153
            and not regeneration_mismatches,
            {
                "schema_builder_exit": schema_build["exit"],
                "fixture_generator_exit": fixture_build["exit"],
                "fixture_artifact_json_count": generated_json_count,
                "manifest_paths_compared": len(regeneration_before),
                "mismatches": regeneration_mismatches,
            },
        )

        closure_spec = validator.load_json(
            snapshot / "artifacts-v0.2.4" / "artifact-closure-spec.v0.2.4.json"
        )
        judgments = closure_spec.get("judgments", {})
        normative = closure_spec.get("normative_precedence", "")
        generic_references = {
            "SupportedEnvelopeHeader.applicable_when": judgments.get(
                "SupportedEnvelopeHeader", {}
            ).get("applicable_when"),
            "UnsupportedEnvelope.predicate": judgments.get(
                "UnsupportedEnvelope", {}
            ).get("predicate"),
        }
        undefined_generic = (
            isinstance(normative, str)
            and "judgments object" in normative
            and "normative" in normative
            and "GenericEnvelopeShape" not in judgments
            and all(
                isinstance(value, str) and "GenericEnvelopeShape" in value
                for value in generic_references.values()
            )
            and "base_envelope_shape" in closure_spec
        )
        add_result(
            "CLOSURE-JUDGMENT-COMPLETENESS-01",
            "Definition/interface dependency-completeness blocker; no admission bypass",
            undefined_generic,
            {
                "normative_precedence": normative,
                "judgment_keys": sorted(judgments),
                "references_to_undefined_symbol": generic_references,
                "base_envelope_shape_outside_judgments": (
                    "base_envelope_shape" in closure_spec
                ),
                "executable_regression": False,
                "repair_obligation": (
                    "define judgments.GenericEnvelopeShape, add explicit false->Malformed/FAIL "
                    "and OpaqueLeaf classification, fully qualify every judgment dependency, "
                    "and test symbolic dependency closure"
                ),
            },
        )

        loaded_key = serialization.load_pem_private_key(KEY.read_bytes(), password=None)
        if not isinstance(loaded_key, Ed25519PrivateKey):
            raise TypeError("fixture key is not Ed25519")
        key = loaded_key
        public_artifact = validator.load_json(
            snapshot / "artifacts-v0.2.4" / "trace-public-key.v0.2.4.json"
        )
        expected_public = __import__("base64").b64decode(
            public_artifact["public_key_base64"], validate=True
        )
        actual_public = key.public_key().public_bytes_raw()
        if actual_public != expected_public:
            raise ValueError("test key does not match frozen public key artifact")

        def signed_case(
            label: str,
            mutate: Callable[[dict[str, Any], dict[str, Any]], None],
            base: str = "legit",
        ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
            initial_store = validator.ArtifactIndex(snapshot)
            source = validator.load_json(
                snapshot / "fixtures-v0.2.4" / f"{base}.json"
            )
            source_trace = copy.deepcopy(
                initial_store.load_json(source["validation_receipt"]["trace_sha256"])
            )
            record, trace = generator.clone_candidate(source, source_trace, f"ai2-{label}")
            mutate(record, trace)
            generator.finalize_fixture(f"ai2-{label}", record, trace, key)
            path = snapshot / "fixtures-v0.2.4" / f"ai2-{label}.json"
            materialized = validator.load_json(path)
            live_store = validator.ArtifactIndex(snapshot)
            live_trace = live_store.load_json(
                materialized["validation_receipt"]["trace_sha256"]
            )
            closure = validator._artifact_closure(
                validator._direct_receipt_reference_map(materialized), live_store
            )
            operational_status, operational_issues = validator._operational_reference_status(
                materialized, live_trace, live_store, closure
            )
            report = validator.validate_path(path, schema_path, snapshot)
            summary = {
                "schema_valid": schema_checker.is_valid(materialized),
                "signature_status": validator._trace_authenticity_status(
                    materialized, live_store
                ),
                "closure_status": closure.status,
                "operational_reference_status": operational_status,
                "operational_issue_codes": sorted(
                    {issue.code for issue in operational_issues}
                ),
                "projection_bound": (
                    live_trace.get("candidate_projection_sha256")
                    == validator.candidate_projection_sha256(materialized)
                    == materialized["validation_receipt"]["candidate_projection_sha256"]
                ),
                "actual_family_oracle_status": validator._independent_oracle_status(
                    materialized
                ),
                **report_dict(report),
            }
            return summary, materialized, live_trace

        def set_path(
            path: tuple[str, ...], value: Any
        ) -> Callable[[dict[str, Any], dict[str, Any]], None]:
            def mutate(record: dict[str, Any], _trace: dict[str, Any]) -> None:
                target: dict[str, Any] = record
                for component in path[:-1]:
                    target = target[component]
                target[path[-1]] = copy.deepcopy(value)
            return mutate

        cheat = validator.load_json(snapshot / "fixtures-v0.2.4" / "cheat.json")
        advice_value = cheat["mechanism"]["admissibility"]["advice"]
        advice_summary, advice_record, advice_trace = signed_case(
            "advice-decl-ledger",
            set_path(("mechanism", "admissibility", "advice"), advice_value),
        )
        advice_context = {
            "declared_advice": advice_record["mechanism"]["admissibility"]["advice"],
            "uniform": advice_record["mechanism"]["admissibility"]["uniform"],
            "program_quantifiers": advice_record["mechanism"]["admissibility"][
                "program_quantifiers"
            ],
            "advice_generator_ref": advice_record["mechanism"]["admissibility"][
                "advice_generator_ref"
            ],
            "declared_answer_access": advice_record["mechanism"]["admissibility"][
                "declared_answer_access"
            ],
            "observed_answer_access": advice_record["validation_receipt"][
                "observed_answer_access"
            ],
            "ledger_advice_bytes": advice_record["ledger"]["description_bytes"]["advice"],
            "ledger_generated_table_bytes": advice_record["ledger"]["description_bytes"][
                "generated_tables"
            ],
            "trace_generation_account": advice_trace["resource_samples"]["admission_costs"][
                "advice_generation"
            ],
        }
        advice_witness = (
            advice_context["declared_advice"] == "one truth table per n"
            and advice_context["uniform"] is True
            and advice_context["program_quantifiers"]
            == "exists-one-program-for-all-input-lengths"
            and advice_context["advice_generator_ref"] is None
            and advice_context["declared_answer_access"] == "none"
            and advice_context["observed_answer_access"] == "none"
            and advice_context["ledger_advice_bytes"] == 0
            and advice_context["ledger_generated_table_bytes"] == 0
            and advice_summary["schema_valid"]
            and advice_summary["signature_status"] == validator.PASS
            and advice_summary["closure_status"] == validator.PASS
            and advice_summary["operational_reference_status"] == validator.PASS
            and advice_summary["projection_bound"]
            and advice_summary["actual_family_oracle_status"] == validator.PASS
            and advice_summary["record_accepted"]
            and not advice_summary["issue_codes"]
        )
        add_result(
            "ADVICE-DECL-LEDGER-01",
            "Accepted-record declaration/ledger consistency Counterexample",
            advice_witness,
            {
                "valid_signature_result": advice_summary,
                "declaration_and_account": advice_context,
                "scope_boundary": (
                    "the frozen legitimate computation and family-selected oracle still execute; "
                    "this does not show actual truth-table resource hiding or a correctness bypass"
                ),
                "repair_obligation": (
                    "replace free-text advice with typed advice_mode; derive ExpectedAdviceDecl "
                    "from family/mechanism and require two-way consistency with generator ref, "
                    "uniform/program quantifiers, access, ledger bytes, and generation account; "
                    "otherwise explicitly move the string to a nonnormative annotation"
                ),
            },
        )

        oracle_variants = {
            "checks-reordered": set_path(
                ("mechanism", "oracle", "checks"),
                ["prefix invariant", "answer"],
            ),
            "obligations-reordered": set_path(
                ("mechanism", "oracle", "obligations"),
                ["prefix-invariant", "answer"],
            ),
            "version-old": set_path(("mechanism", "oracle", "version"), "0.2.3"),
            "independent-false": set_path(
                ("mechanism", "oracle", "independent"), False
            ),
            "source-hash-to-rule": set_path(
                ("mechanism", "oracle", "sha256"),
                f"sha256:{validator.PINNED_PARITY_RULE_HASH}",
            ),
        }
        oracle_variant_evidence: dict[str, Any] = {}
        oracle_variants_ok = True
        for label, mutate in oracle_variants.items():
            summary, _, _ = signed_case(f"oracle-{label}", mutate)
            oracle_variant_evidence[label] = summary
            oracle_variants_ok = oracle_variants_ok and (
                summary["schema_valid"]
                and summary["signature_status"] == validator.PASS
                and summary["projection_bound"]
                and summary["actual_family_oracle_status"] == validator.PASS
                and not summary["record_accepted"]
            )
        add_result(
            "ORACLE-SIBLING-FIELDS-024",
            "Valid-signature negative unit tests",
            oracle_variants_ok and oracle_target_ok,
            {
                "built_in_cross_family_status_and_field_cases": 9,
                "independent_additional_cases": oracle_variant_evidence,
            },
        )

        def role_and_baseline(record: dict[str, Any], _trace: dict[str, Any]) -> None:
            record["mechanism"]["role"] = "candidate"
            record["mechanism"]["baseline_id"] = "fabricated-baseline"

        metadata_variants = {
            "mechanism-name": set_path(
                ("mechanism", "name"), "Per-length truth table"
            ),
            "operations-empty": set_path(("mechanism", "operations"), []),
            "role-plus-baseline": role_and_baseline,
            "hardware": set_path(
                ("mechanism", "admissibility", "hardware"),
                "unbounded answer-oracle machine",
            ),
            "generator-name": set_path(
                ("problem", "generator", "name"), "answer-oracle-generated"
            ),
            "generator-seed": set_path(("problem", "generator", "seed"), 999),
            "instance-id": set_path(
                ("problem", "instance_id"), "fabricated-instance"
            ),
        }
        metadata_evidence: dict[str, Any] = {}
        for label, mutate in metadata_variants.items():
            summary, _, _ = signed_case(f"metadata-{label}", mutate)
            metadata_evidence[label] = summary
        metadata_observed = all(
            item["schema_valid"]
            and item["signature_status"] == validator.PASS
            and item["projection_bound"]
            and item["record_accepted"]
            and not item["issue_codes"]
            for item in metadata_evidence.values()
        )
        add_result(
            "SIGNED-SIBLING-DECLARATION-SURFACE-024",
            "Scoped Observation / definition surface, not separately promoted",
            metadata_observed,
            {
                "accepted_valid_signature_variants": metadata_evidence,
                "classification_boundary": (
                    "name/generator/instance fields may be identifiers or annotations; role/baseline, "
                    "operations and hardware look semantic but frozen v0.2.4 does not state an exact "
                    "ExpectedMechanismDecl contract. Only the independently sufficient advice "
                    "declaration/ledger contradiction is promoted as a blocker here."
                ),
            },
        )

    after_metadata = frozen_metadata(entries)
    changed = sorted(
        path
        for path in set(before_metadata) | set(after_metadata)
        if before_metadata.get(path) != after_metadata.get(path)
    )
    add_result(
        "FROZEN-PATHS-READONLY-024",
        "Provenance",
        not changed,
        {
            "manifest_listed_paths": len(entries),
            "manifest_file_also_monitored": True,
            "changed_frozen_paths": changed,
            "candidate_root_writes_in_monitored_domain": len(changed),
            "nonmanifest_successor_paths": "outside the requested provenance domain",
        },
    )

    unexpected = [result["probe_id"] for result in RESULTS if not result["conforms"]]
    blockers = [
        "CLOSURE-JUDGMENT-COMPLETENESS-01",
        "ADVICE-DECL-LEDGER-01",
    ]
    payload = {
        "scope": (
            "bounded local read-only exact-byte software conformance review; "
            "valid-signature variants only in an isolated copy; no network; no P/NP inference"
        ),
        "overall_disposition": "FAIL / " + " + ".join(blockers),
        "promotion_blockers": blockers,
        "targeted_v024_fixes": {
            "CLOSURE-CLASS-01": "CLOSED/PASS in bounded executable scope",
            "CLOSURE-EDGE-SCOPE-01": "CLOSED/PASS in bounded executable/scope checks",
            "ORACLE-DECL-FAMILY-01": "CLOSED/PASS in bounded valid-signature checks",
        },
        "unexpected_results": unexpected,
        "probe_groups": len(RESULTS),
        "candidate_root_writes": len(changed),
        "provenance_domain": "153 v0.2.4 manifest paths plus the manifest file",
        "candidate_status": "CANDIDATE_UNPROMOTED",
        "board_success": False,
        "shared_repo_authorization": False,
        "p_np_claim": False,
        "results": RESULTS,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
