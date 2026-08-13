"""Executable closure classification/scope regression for v0.2.6.

Exit zero requires every malformed unsupported envelope to classify as FAIL,
every complete unsupported envelope to classify as UNKNOWN, and a pinned
supported run-spec to classify as PASS. These are interface conformance checks;
the frozen normative spec must also scope current parent-role relations to
supported spec ids only. They make no P/NP claim.

The v0.2.6 checks also require every supported decision branch to produce a
unique terminal result or a fully qualified next judgment transition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    import pnp_glc_i0.semantic_validator_v026 as validator

    case_root = root / "artifacts-v0.2.6" / "closure-classification"
    manifest = json.loads((case_root / "manifest.json").read_text(encoding="utf-8"))
    store = validator.ArtifactIndex(root)
    probes: list[dict[str, object]] = []
    for name, expected in manifest["expected_status"].items():
        path = case_root / f"{name}.json"
        actual = validator._artifact_closure(
            {"run-spec": digest(path)}, store
        ).status
        probes.append(
            {
                "name": name,
                "expected": expected,
                "actual": actual,
                "conformant": actual == expected,
            }
        )

    supported = root / "artifacts-v0.2.6" / "run-standard.v0.2.6.json"
    supported_actual = validator._artifact_closure(
        {"run-spec": digest(supported)}, store
    ).status
    probes.append(
        {
            "name": "supported-run-standard",
            "expected": validator.PASS,
            "actual": supported_actual,
            "conformant": supported_actual == validator.PASS,
        }
    )

    spec = json.loads(
        (
            root
            / "artifacts-v0.2.6"
            / "artifact-closure-spec.v0.2.6.json"
        ).read_text(encoding="utf-8")
    )
    judgments = spec.get("judgments", {})
    generic = judgments.get("GenericEdgeShape", {})
    generic_envelope = judgments.get("GenericEnvelopeShape", {})
    opaque_leaf = judgments.get("OpaqueLeaf", {})
    supported_header = judgments.get("SupportedEnvelopeHeader", {})
    supported_relation = judgments.get("SupportedEdgeRelation", {})
    supported_traversal = judgments.get("SupportedTraversal", {})
    unsupported = judgments.get("UnsupportedEnvelope", {})
    future_value = json.loads(
        (
            case_root / "shape-valid-unsupported-future-type.json"
        ).read_text(encoding="utf-8")
    )
    future_type = future_value["artifact_envelope"]["artifact_type"]
    dependencies = {
        name: body.get("depends_on")
        for name, body in judgments.items()
        if isinstance(body, dict)
    }
    dependency_refs = [
        reference
        for values in dependencies.values()
        if isinstance(values, list)
        for reference in values
    ]
    dependency_targets = [
        reference.removeprefix("judgments.")
        for reference in dependency_refs
        if isinstance(reference, str) and reference.startswith("judgments.")
    ]
    false_result = generic_envelope.get("false_result", {})
    generic_true = generic_envelope.get("true_result", {})
    header_false = supported_header.get("false_result", {})
    header_true = supported_header.get("true_result", {})
    relation_false = supported_relation.get("false_result", {})
    relation_true = supported_relation.get("true_result", {})
    fixed_point_results = supported_traversal.get("fixed_point_results", {})

    transition_refs: list[str] = []
    for body in judgments.values():
        if not isinstance(body, dict):
            continue
        for outcome_name in ("false_result", "true_result"):
            outcome = body.get(outcome_name)
            if not isinstance(outcome, dict):
                continue
            next_transition = outcome.get("next_transition")
            if isinstance(next_transition, str):
                transition_refs.append(next_transition)
            next_transitions = outcome.get("next_transitions")
            if isinstance(next_transitions, list):
                transition_refs.extend(next_transitions)
        child_dispatch = body.get("child_dispatch")
        if isinstance(child_dispatch, list):
            transition_refs.extend(child_dispatch)
    transition_targets = [
        reference.removeprefix("judgments.")
        for reference in transition_refs
        if reference.startswith("judgments.")
    ]
    scope_checks = {
        "normative-precedence-declared": bool(spec.get("normative_precedence")),
        "generic-relation-not-required": any(
            "EDGE_RELATIONS domain" in item
            for item in generic.get("does_not_require", [])
        ),
        "supported-header-pins-spec-version-and-type-domain": (
            validator.ARTIFACT_CLOSURE_SPEC_ID
            in supported_header.get("applicable_when", "")
            and validator.VALIDATOR_VERSION
            in supported_header.get("predicate", "")
            and "EDGE_RELATIONS domain"
            in supported_header.get("predicate", "")
        ),
        "supported-relation-iff-supported-header": (
            supported_relation.get("applicable_iff")
            == "judgments.SupportedEnvelopeHeader holds"
        ),
        "unsupported-relation-not-applicable": (
            "unsupported spec_id"
            in supported_relation.get("not_applicable_when", "")
        ),
        "unsupported-result-unknown": unsupported.get("result") == "UNKNOWN",
        "future-parent-has-no-current-relation": (
            future_type not in validator.EDGE_RELATIONS
        ),
        "generic-envelope-judgment-present": bool(generic_envelope),
        "opaque-leaf-judgment-present": bool(opaque_leaf),
        "all-judgments-declare-dependencies": (
            len(dependencies) == len(judgments)
            and all(isinstance(values, list) for values in dependencies.values())
        ),
        "dependency-refs-fully-qualified": all(
            isinstance(reference, str) and reference.startswith("judgments.")
            for reference in dependency_refs
        ),
        "dependency-targets-resolve": all(
            target in judgments for target in dependency_targets
        ),
        "supported-header-depends-generic-envelope": (
            supported_header.get("depends_on")
            == ["judgments.GenericEnvelopeShape"]
        ),
        "unsupported-depends-generic-envelope": (
            unsupported.get("depends_on")
            == ["judgments.GenericEnvelopeShape"]
        ),
        "generic-false-is-malformed-fail": (
            false_result.get("classification") == "Malformed"
            and false_result.get("gate_result") == "FAIL"
            and false_result.get("traversal") == "do not traverse"
        ),
        "base-envelope-shape-is-derived-view": (
            spec.get("base_envelope_shape", {}).get("normative_status")
            == "derived-view-only"
            and spec.get("base_envelope_shape", {}).get("derived_from")
            == "judgments.GenericEnvelopeShape"
        ),
        "normative-graph-dependency-rule-declared": (
            "Every symbolic dependency or transition"
            in spec.get("normative_precedence", "")
        ),
    }
    totality_checks = {
        "generic-valid-dispatch-is-total": (
            generic_true.get("terminal") is False
            and generic_true.get("gate_result") == "PASS"
            and generic_true.get("next_transitions")
            == [
                "judgments.UnsupportedEnvelope",
                "judgments.SupportedEnvelopeHeader",
            ]
            and "exactly one" in generic_true.get("dispatch_rule", "")
        ),
        "supported-header-false-terminal": (
            header_false.get("terminal") is True
            and header_false.get("classification") == "Malformed"
            and header_false.get("gate_result") == "FAIL"
            and header_false.get("traversal") == "do not traverse"
        ),
        "supported-header-true-unique-transition": (
            header_true.get("terminal") is False
            and header_true.get("gate_result") == "PASS"
            and header_true.get("next_transition")
            == "judgments.SupportedEdgeRelation"
        ),
        "supported-relation-false-terminal": (
            relation_false.get("terminal") is True
            and relation_false.get("relation_status") == "invalid"
            and relation_false.get("classification") == "Malformed"
            and relation_false.get("gate_result") == "FAIL"
            and relation_false.get("traversal") == "do not traverse"
        ),
        "supported-relation-true-unique-transition": (
            relation_true.get("terminal") is False
            and relation_true.get("relation_status") == "valid"
            and relation_true.get("classification") == "Traverse"
            and relation_true.get("gate_result") == "PASS"
            and relation_true.get("next_transition")
            == "judgments.SupportedTraversal"
        ),
        "supported-relation-declares-totality": (
            "exactly one" in supported_relation.get("totality", "")
            and "false_result" in supported_relation.get("totality", "")
            and "true_result" in supported_relation.get("totality", "")
        ),
        "supported-traversal-depends-relation": (
            supported_traversal.get("depends_on")
            == ["judgments.SupportedEdgeRelation"]
        ),
        "supported-traversal-child-dispatch-total": (
            supported_traversal.get("child_dispatch")
            == ["judgments.OpaqueLeaf", "judgments.GenericEnvelopeShape"]
        ),
        "fixed-point-terminal-trichotomy": (
            set(fixed_point_results)
            == {
                "any_reachable_fail",
                "no_fail_and_any_reachable_unknown",
                "queue_empty_all_reachable_pass",
            }
            and {
                value.get("gate_result")
                for value in fixed_point_results.values()
                if isinstance(value, dict)
            }
            == {"FAIL", "UNKNOWN", "PASS"}
            and all(
                isinstance(value, dict) and value.get("terminal") is True
                for value in fixed_point_results.values()
            )
        ),
        "transition-refs-fully-qualified": all(
            reference.startswith("judgments.") for reference in transition_refs
        ),
        "transition-targets-resolve": (
            len(transition_targets) == len(transition_refs)
            and all(target in judgments for target in transition_targets)
        ),
    }
    unexpected = [probe["name"] for probe in probes if not probe["conformant"]]
    unexpected.extend(
        name for name, conformant in scope_checks.items() if not conformant
    )
    unexpected.extend(
        name for name, conformant in totality_checks.items() if not conformant
    )
    print(
        json.dumps(
            {
                "classification": "Experiment / interface regression",
                "validator_version": validator.VALIDATOR_VERSION,
                "classification_probe_count": len(probes),
                "scope_check_count": len(scope_checks),
                "terminal_totality_check_count": len(totality_checks),
                "unexpected": unexpected,
                "all_conformant": not unexpected,
                "admission_bypass_claim": False,
                "p_np_claim": False,
                "probes": probes,
                "scope_checks": scope_checks,
                "terminal_totality_checks": totality_checks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
