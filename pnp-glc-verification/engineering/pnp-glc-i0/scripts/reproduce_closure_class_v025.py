"""Executable closure classification/scope regression for v0.2.5.

Exit zero requires every malformed unsupported envelope to classify as FAIL,
every complete unsupported envelope to classify as UNKNOWN, and a pinned
supported run-spec to classify as PASS. These are interface conformance checks;
the frozen normative spec must also scope current parent-role relations to
supported spec ids only. They make no P/NP claim.
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

    import pnp_glc_i0.semantic_validator_v025 as validator

    case_root = root / "artifacts-v0.2.5" / "closure-classification"
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

    supported = root / "artifacts-v0.2.5" / "run-standard.v0.2.5.json"
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
            / "artifacts-v0.2.5"
            / "artifact-closure-spec.v0.2.5.json"
        ).read_text(encoding="utf-8")
    )
    judgments = spec.get("judgments", {})
    generic = judgments.get("GenericEdgeShape", {})
    generic_envelope = judgments.get("GenericEnvelopeShape", {})
    opaque_leaf = judgments.get("OpaqueLeaf", {})
    supported_header = judgments.get("SupportedEnvelopeHeader", {})
    supported_relation = judgments.get("SupportedEdgeRelation", {})
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
            "Every symbolic dependency in judgments"
            in spec.get("normative_precedence", "")
        ),
    }
    unexpected = [probe["name"] for probe in probes if not probe["conformant"]]
    unexpected.extend(
        name for name, conformant in scope_checks.items() if not conformant
    )
    print(
        json.dumps(
            {
                "classification": "Experiment / interface regression",
                "validator_version": validator.VALIDATOR_VERSION,
                "classification_probe_count": len(probes),
                "scope_check_count": len(scope_checks),
                "unexpected": unexpected,
                "all_conformant": not unexpected,
                "admission_bypass_claim": False,
                "p_np_claim": False,
                "probes": probes,
                "scope_checks": scope_checks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
