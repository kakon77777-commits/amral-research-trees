from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any

from jsonschema import Draft202012Validator


ENGINEERING_ROOT = Path(
    r"C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0"
)
SCHEMA_REL = Path("schemas/run-record.schema.v0.2.0-candidate.json")
SPEC_REL = Path("artifacts/candidate-projection-spec.v0.2.0.json")
VALIDATOR_REL = Path("src/pnp_glc_i0/semantic_validator.py")
LEGIT_RECORD_REL = Path("fixtures/legit.json")
LEGIT_TRACE_REL = Path("artifacts/traces/legit.trace.json")
WORK_ROOT = Path(__file__).resolve().parent.parent / "work"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_validator(snapshot_root: Path) -> ModuleType:
    package_root = snapshot_root / "src" / "pnp_glc_i0"
    package_name = (
        "projection_redteam_package_"
        + sha256_bytes(str(snapshot_root).encode("utf-8"))[:12]
    )
    package_spec = importlib.util.spec_from_file_location(
        package_name,
        package_root / "__init__.py",
        submodule_search_locations=[str(package_root)],
    )
    if package_spec is None or package_spec.loader is None:
        raise RuntimeError(f"cannot import validator package snapshot: {package_root}")
    package = importlib.util.module_from_spec(package_spec)
    sys.modules[package_name] = package
    package_spec.loader.exec_module(package)

    module_path = snapshot_root / VALIDATOR_REL
    module_name = package_name + ".semantic_validator"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import validator snapshot: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def python_canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def proposed_projection(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key != "validation_receipt"}


def proposed_projection_hash(record: dict[str, Any]) -> str:
    return sha256_bytes(python_canonical_bytes(proposed_projection(record)))


def minimal_candidate_record(answer: int, states: int) -> dict[str, Any]:
    return {
        "schema_version": "0.2.0",
        "run_id": "negative-family",
        "events": [{"seq": 0, "kind": "stop"}],
        "ledger": {"counts": {"states": states}},
        "candidate_result": {
            "status": "complete",
            "answer": answer,
            "certificate_refs": [],
        },
        "validation_receipt": {
            "candidate_projection_sha256": "0" * 64,
            "trace_sha256": "0" * 64,
            "final_completion": False,
        },
    }


def minimal_trace(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "projection_spec_id": "urn:evemisslab:pnp-glc:candidate-projection:0.2.0",
        "candidate_projection_sha256": proposed_projection_hash(record),
        "run_id": record["run_id"],
        "gate_version": "i0-admission-gate/0.2.0",
    }


def utf16_sort_key(value: str) -> tuple[int, ...]:
    encoded = value.encode("utf-16-be")
    return tuple(
        int.from_bytes(encoded[index : index + 2], "big")
        for index in range(0, len(encoded), 2)
    )


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def refresh_receipt_and_trace(
    validator: ModuleType,
    snapshot_root: Path,
    record: dict[str, Any],
    trace: dict[str, Any],
) -> None:
    receipt = record["validation_receipt"]
    receipt["schema_sha256"] = "sha256:" + sha256_path(snapshot_root / SCHEMA_REL)
    receipt["validator_sha256"] = "sha256:" + sha256_path(snapshot_root / VALIDATOR_REL)
    receipt["projection_spec_sha256"] = "sha256:" + sha256_path(snapshot_root / SPEC_REL)
    receipt["candidate_projection_sha256"] = "sha256:" + validator.candidate_projection_sha256(record)
    trace["candidate_projection_sha256"] = validator.candidate_projection_sha256(record)

    trace_path = snapshot_root / LEGIT_TRACE_REL
    trace_path.write_text(
        json.dumps(trace, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    receipt["trace_sha256"] = "sha256:" + sha256_path(trace_path)
    receipt["resolved_evidence_hashes"] = [
        "sha256:" + digest for digest in sorted(validator._receipt_reference_set(record))
    ]


def validate_mutated_legit(
    base_snapshot: Path,
    mutation: str,
) -> dict[str, Any]:
    case_root = base_snapshot.parent / f"case-{mutation}"
    shutil.copytree(base_snapshot, case_root)
    validator = load_validator(case_root)
    schema = validator.load_json(case_root / SCHEMA_REL)
    record = copy.deepcopy(validator.load_json(case_root / LEGIT_RECORD_REL))
    trace = copy.deepcopy(validator.load_json(case_root / LEGIT_TRACE_REL))

    if mutation == "wrong-answer":
        # The fixture input bits are [1,0,1,1], whose parity is 1. Replace the
        # answer by 0, mirror it in the trace, and repair only self-consistency
        # hashes. The trace's oracle_pass/contract_pass claims are left true.
        record["candidate_result"]["answer"] = 0
        trace["candidate_output"] = copy.deepcopy(record["candidate_result"])
        terminal_hash = validator.sha256_bytes(
            validator.canonical_json_bytes(record["candidate_result"])
        )
        record["events"][-1]["output_sha256"] = "sha256:" + terminal_hash
        trace["events"] = copy.deepcopy(record["events"])
    elif mutation == "fabricated-ledger":
        record["ledger"]["counts"]["states"] = 999
        trace["resource_samples"]["counts"] = copy.deepcopy(
            record["ledger"]["counts"]
        )
    elif mutation == "fabricated-transition":
        fabricated_digest = "sha256:" + "e" * 64
        record["events"][0]["output_sha256"] = fabricated_digest
        record["events"][1]["input_sha256"] = fabricated_digest
        trace["events"] = copy.deepcopy(record["events"])
    elif mutation == "unresolved-event-ref":
        dead_hash = "sha256:" + "f" * 64
        record["events"][0]["transition_rule_ref"] = dead_hash
        trace["events"] = copy.deepcopy(record["events"])
    else:
        raise ValueError(mutation)

    refresh_receipt_and_trace(validator, case_root, record, trace)
    report = validator.validate_record(
        record,
        schema,
        case_root,
        schema_sha256=sha256_path(case_root / SCHEMA_REL),
    )
    return report.to_dict()


def main() -> None:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="projection-snapshot-", dir=WORK_ROOT) as temp_name:
        snapshot_root = Path(temp_name) / "pnp-glc-i0"
        shutil.copytree(ENGINEERING_ROOT, snapshot_root)
        validator = load_validator(snapshot_root)
        schema = validator.load_json(snapshot_root / SCHEMA_REL)
        spec = validator.load_json(snapshot_root / SPEC_REL)

        results: dict[str, Any] = {
            "scope": "engineering provenance gate only; no P/NP inference",
            "source_snapshot": {
                "schema_sha256": sha256_path(snapshot_root / SCHEMA_REL),
                "projection_spec_sha256": sha256_path(snapshot_root / SPEC_REL),
                "validator_sha256": sha256_path(snapshot_root / VALIDATOR_REL),
            },
        }

        # N1: excluding the whole validation receipt produces an acyclic order:
        # candidate projection -> trace -> external receipt.
        record = minimal_candidate_record(answer=0, states=1)
        proposed_before = proposed_projection_hash(record)
        record["validation_receipt"]["candidate_projection_sha256"] = proposed_before
        proposed_after = proposed_projection_hash(record)
        current_before = validator.candidate_projection_sha256(record)
        record["validation_receipt"]["candidate_projection_sha256"] = current_before
        current_after = validator.candidate_projection_sha256(record)
        assert proposed_before == proposed_after
        assert current_before == current_after
        results["N1_self_reference"] = {
            "proposal_stable_after_receipt_update": True,
            "snapshot_validator_stable_after_receipt_update": True,
            "direct_cycle_observed": False,
            "condition": "schema validation must precede projection and every validator-derived field stays in validation_receipt",
        }

        # N2a: permissive parsing collapses duplicate-member provenance. The
        # snapshot's file loader correctly rejects it; all other entrypoints
        # must preserve the same strict-byte boundary.
        duplicate_bytes = b'{"x":0,"x":1}'
        clean_bytes = b'{"x":1}'
        duplicate_value = json.loads(duplicate_bytes)
        clean_value = json.loads(clean_bytes)
        duplicate_collapses = (
            python_canonical_bytes(duplicate_value) == python_canonical_bytes(clean_value)
        )
        assert duplicate_collapses
        strict_rejected = False
        try:
            json.loads(duplicate_bytes, object_pairs_hook=strict_pairs)
        except ValueError:
            strict_rejected = True
        assert strict_rejected

        # N2b: the prose says controls are escaped, but does not state whether
        # short escapes or \u00xx are canonical. These spellings parse equally
        # but hash differently.
        short_escape = b'{"x":"\\n"}'
        unicode_escape = b'{"x":"\\u000a"}'
        assert json.loads(short_escape) == json.loads(unicode_escape)
        assert sha256_bytes(short_escape) != sha256_bytes(unicode_escape)

        # N2c: scalar-value ordering is explicitly different from RFC 8785's
        # UTF-16 code-unit order. Pin this as a cross-implementation vector.
        ordering_object = {"\ue000": 1, "\U0001f600": 2}
        scalar_bytes = python_canonical_bytes(ordering_object)
        jcs_ordered = dict(
            sorted(ordering_object.items(), key=lambda item: utf16_sort_key(item[0]))
        )
        jcs_bytes = json.dumps(
            jcs_ordered, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        assert scalar_bytes != jcs_bytes

        # The transport schema admits floats in projected extension points, but
        # the semantic canonical-domain gate rejects them. That layering passes.
        size_schema = schema["$defs"]["problem"]["properties"]["size"]
        answer_schema = schema["$defs"]["candidateResult"]["properties"]["answer"]
        frontier_value_schema = schema["$defs"]["failureFrontier"]["properties"]["axes"]["items"]["properties"]["value"]
        schema_accepts_float = all(
            (
                Draft202012Validator(size_schema).is_valid({"ratio": 0.5}),
                Draft202012Validator(answer_schema).is_valid(0.5),
                Draft202012Validator(frontier_value_schema).is_valid(0.5),
            )
        )
        canonical_rejects_float = False
        canonical_rejects_nan = False
        canonical_rejects_non_nfc = False
        for value, flag_name in (
            ({"x": 0.5}, "float"),
            ({"x": float("nan")}, "nan"),
            ({"x": "e\u0301"}, "nfc"),
        ):
            try:
                validator.canonical_json_bytes(value)
            except ValueError:
                if flag_name == "float":
                    canonical_rejects_float = True
                elif flag_name == "nan":
                    canonical_rejects_nan = True
                else:
                    canonical_rejects_non_nfc = True
        assert canonical_rejects_float and canonical_rejects_nan and canonical_rejects_non_nfc
        results["N2_canonicalization"] = {
            "duplicate_input_collapses_under_permissive_parse": duplicate_collapses,
            "snapshot_strict_parser_policy": strict_rejected,
            "escape_spellings_same_value_different_hash": True,
            "scalar_order_sha256": sha256_bytes(scalar_bytes),
            "utf16_jcs_order_sha256": sha256_bytes(jcs_bytes),
            "schema_accepts_projected_floats": schema_accepts_float,
            "semantic_gate_rejects_float_nan_non_nfc": True,
        }

        # N3: all currently declared validator fields are in the excluded
        # receipt. The schema's closed root protects against accidental extras.
        receipt_variant = copy.deepcopy(record)
        receipt_variant["validation_receipt"]["final_completion"] = True
        assert (
            validator.candidate_projection_sha256(record)
            == validator.candidate_projection_sha256(receipt_variant)
        )
        results["N3_validator_field_separation"] = {
            "snapshot_excludes_entire_receipt": True,
            "schema_rejects_unknown_root_fields": schema.get("additionalProperties") is False,
            "condition": "projection is computed only after validation against the pinned schema",
        }

        # N4: the four-field proposal alone accepts producer-chosen record/hash
        # pairs. The snapshot now rejects an independently wrong PARITY answer,
        # but still treats a mirrored resource summary and an unexecuted
        # transition-hash chain as replay evidence.
        record_zero = minimal_candidate_record(answer=0, states=1)
        record_one = minimal_candidate_record(answer=1, states=999)
        trace_zero = minimal_trace(record_zero)
        trace_one = minimal_trace(record_one)
        assert trace_zero["candidate_projection_sha256"] == proposed_projection_hash(record_zero)
        assert trace_one["candidate_projection_sha256"] == proposed_projection_hash(record_one)
        wrong_answer_report = validate_mutated_legit(snapshot_root, "wrong-answer")
        fabricated_ledger_report = validate_mutated_legit(snapshot_root, "fabricated-ledger")
        fabricated_transition_report = validate_mutated_legit(
            snapshot_root, "fabricated-transition"
        )
        assert wrong_answer_report["record_accepted"] is False
        assert fabricated_ledger_report["record_accepted"] is True
        assert fabricated_transition_report["record_accepted"] is True
        results["N4_hash_match_without_semantic_derivation"] = {
            "minimal_four_field_bindings_both_pass": True,
            "wrong_parity_answer_rejected": not wrong_answer_report["record_accepted"],
            "fabricated_states_999_ledger_accepted": fabricated_ledger_report[
                "record_accepted"
            ],
            "fabricated_intermediate_transition_digest_accepted": fabricated_transition_report[
                "record_accepted"
            ],
            "why": "trace equality proves mirroring; counts are copied from resource_samples and transition rules are not executed",
        }

        # N5: verify that ArtifactIndex keeps and reuses the exact bytes it
        # hashed, rather than reopening a mutable path.
        toctou_root = Path(temp_name) / "toctou"
        toctou_root.mkdir()
        artifact_path = toctou_root / "artifact.json"
        good_bytes = b'{"trusted":true}'
        bad_bytes = b'{"trusted":false}'
        artifact_path.write_bytes(good_bytes)
        index = validator.ArtifactIndex(toctou_root)
        indexed_hash = sha256_bytes(good_bytes)
        assert index.contains(indexed_hash)
        artifact_path.write_bytes(bad_bytes)
        loaded = index.load_json(indexed_hash)
        assert loaded == {"trusted": True}
        results["N5_toctou"] = {
            "indexed_hash_still_resolves": index.contains(indexed_hash),
            "loaded_value_after_swap": loaded,
            "indexed_sha256": indexed_hash,
            "loaded_bytes_sha256": sha256_bytes(bad_bytes),
            "same_hashed_snapshot_used": True,
            "toctou_negative_rejected": True,
        }

        # N6: certificate refs and per-event transition/invariant refs must all
        # be walked. The dead event reference must fail admission.
        unresolved_report = validate_mutated_legit(snapshot_root, "unresolved-event-ref")
        assert unresolved_report["record_accepted"] is False
        results["N6_unresolved_content_ref"] = {
            "dead_event_transition_ref_rejected": not unresolved_report["record_accepted"],
            "issues": unresolved_report["issues"],
            "direct_event_ref_closure_present": True,
            "remaining_condition": "apply the same rule transitively to typed refs inside resolved artifacts",
        }

        root_required = set(schema["required"])
        source_text = (snapshot_root / VALIDATOR_REL).read_text(encoding="utf-8")
        results["implementation_alignment_observation"] = {
            "schema_fields": sorted(
                root_required.intersection({"candidate_result", "validation_receipt"})
            ),
            "validator_uses_candidate_result": 'record["candidate_result"]' in source_text,
            "validator_uses_validation_receipt": 'record["validation_receipt"]' in source_text,
            "projection_excludes_validation_receipt": True,
            "spec_projection_exclusion": spec["projection"]["exclude"],
        }

        print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
