from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "artifacts-v0.2.5"
OUTPUT = ROOT / "artifacts-v0.2.6"
STATIC_NAMES = (
    "artifact-closure-spec.v0.2.5.json",
    "candidate-projection-spec.v0.2.5.json",
    "capability-sandbox.v0.2.5.json",
    "contract-2sat.v0.2.5.json",
    "contract-parity.v0.2.5.json",
    "evidence-role-spec.v0.2.5.json",
    "fairness.v0.2.5.json",
    "maximal-run.v0.2.5.json",
    "negative-malformed-role-edge.json",
    "negative-missing-envelope-spec-id.json",
    "parity-invariant.v0.2.5.json",
    "run-robust.v0.2.5.json",
    "run-standard.v0.2.5.json",
    "trace-public-key.v0.2.5.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: version_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [version_value(item) for item in value]
    if isinstance(value, str):
        return value.replace("0.2.5", "0.2.6").replace(
            "2026-08-09", "2026-08-10"
        )
    return value


def strings(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, str):
        yield value


def replace_hash_refs(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {
            key: replace_hash_refs(item, replacements)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [replace_hash_refs(item, replacements) for item in value]
    if isinstance(value, str) and value.startswith("sha256:"):
        return "sha256:" + replacements.get(value.removeprefix("sha256:"), value.removeprefix("sha256:"))
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def totalize_closure_spec(spec: dict[str, Any]) -> None:
    judgments = spec["judgments"]
    generic = judgments["GenericEnvelopeShape"]
    generic["false_result"].update({"terminal": True})
    generic["true_result"] = {
        "classification": "GenericValid",
        "dispatch_rule": (
            "exactly one of judgments.UnsupportedEnvelope or "
            "judgments.SupportedEnvelopeHeader is selected by spec_id equality"
        ),
        "gate_result": "PASS",
        "next_transitions": [
            "judgments.UnsupportedEnvelope",
            "judgments.SupportedEnvelopeHeader",
        ],
        "terminal": False,
    }

    header = judgments["SupportedEnvelopeHeader"]
    header.pop("failure_result", None)
    header["false_result"] = {
        "classification": "Malformed",
        "gate_result": "FAIL",
        "terminal": True,
        "traversal": "do not traverse",
    }
    header["true_result"] = {
        "classification": "SupportedHeaderValid",
        "gate_result": "PASS",
        "next_transition": "judgments.SupportedEdgeRelation",
        "terminal": False,
    }

    relation = judgments["SupportedEdgeRelation"]
    relation["false_result"] = {
        "classification": "Malformed",
        "gate_result": "FAIL",
        "relation_status": "invalid",
        "terminal": True,
        "traversal": "do not traverse",
    }
    relation["true_result"] = {
        "classification": "Traverse",
        "gate_result": "PASS",
        "next_transition": "judgments.SupportedTraversal",
        "relation_status": "valid",
        "terminal": False,
    }
    relation["totality"] = (
        "for every applicable envelope exactly one of false_result or "
        "true_result is selected by the predicate"
    )

    judgments["SupportedTraversal"] = {
        "applicable_iff": "judgments.SupportedEdgeRelation holds",
        "child_dispatch": [
            "judgments.OpaqueLeaf",
            "judgments.GenericEnvelopeShape",
        ],
        "depends_on": ["judgments.SupportedEdgeRelation"],
        "fixed_point_results": {
            "any_reachable_fail": {
                "gate_result": "FAIL",
                "terminal": True,
            },
            "no_fail_and_any_reachable_unknown": {
                "gate_result": "UNKNOWN",
                "terminal": True,
            },
            "queue_empty_all_reachable_pass": {
                "gate_result": "PASS",
                "terminal": True,
            },
        },
        "transition": (
            "enqueue every relation-valid edge exactly once by content hash; "
            "dispatch each resolved child through child_dispatch; stop at the "
            "unique fixed_point_results branch"
        ),
    }

    spec["normative_precedence"] = (
        "The complete normative classification graph is the judgments object, "
        "including every structured false_result, true_result, child_dispatch, "
        "and fixed_point_results branch. Every symbolic dependency or transition "
        "reference must be a fully qualified judgments.<name> reference resolving "
        "inside this object. Top-level base_envelope_shape, closure_algorithm, "
        "edge_shape, and envelope_classification_order are derived views with no "
        "independent normative force."
    )


def main() -> None:
    parent_hash_to_name = {
        sha256(PARENT / name): name for name in STATIC_NAMES
    }
    drafts: dict[str, Any] = {}
    for parent_name in STATIC_NAMES:
        value = version_value(
            json.loads((PARENT / parent_name).read_text(encoding="utf-8"))
        )
        if parent_name == "artifact-closure-spec.v0.2.5.json":
            totalize_closure_spec(value)
        drafts[parent_name] = value

    unresolved = set(STATIC_NAMES)
    new_hashes: dict[str, str] = {}
    while unresolved:
        progressed = False
        for parent_name in sorted(unresolved):
            dependencies = {
                parent_hash_to_name[item.removeprefix("sha256:")]
                for item in strings(drafts[parent_name])
                if item.startswith("sha256:")
                and item.removeprefix("sha256:") in parent_hash_to_name
            }
            if not dependencies.issubset(new_hashes):
                continue
            replacements = {
                old_hash: new_hashes[target]
                for old_hash, target in parent_hash_to_name.items()
                if target in dependencies
            }
            value = replace_hash_refs(copy.deepcopy(drafts[parent_name]), replacements)
            output_name = parent_name.replace("0.2.5", "0.2.6")
            output_path = OUTPUT / output_name
            write_json(output_path, value)
            new_hashes[parent_name] = sha256(output_path)
            unresolved.remove(parent_name)
            progressed = True
        if not progressed:
            raise RuntimeError(f"cyclic static artifact dependencies: {sorted(unresolved)}")

    print(
        json.dumps(
            {
                "version": "0.2.6",
                "files": {
                    name.replace("0.2.5", "0.2.6"): new_hashes[name]
                    for name in sorted(new_hashes)
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
