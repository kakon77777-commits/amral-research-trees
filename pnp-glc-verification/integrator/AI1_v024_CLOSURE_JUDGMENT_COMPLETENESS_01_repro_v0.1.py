from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


EXPECTED_SPEC_SHA256 = (
    "579B6F7DA8BE3712FE6130AD900CF0CBA189496100548CBF87655687A7690588"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only v0.2.4 closure judgment dependency check"
    )
    parser.add_argument("candidate_root", type=Path)
    args = parser.parse_args()
    root = args.candidate_root.resolve()
    sys.path.insert(0, str(root / "src"))

    import pnp_glc_i0.semantic_validator_v024 as validator

    spec_path = (
        root
        / "artifacts-v0.2.4"
        / "artifact-closure-spec.v0.2.4.json"
    )
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    judgments = spec.get("judgments", {})

    references: list[dict[str, str]] = []
    for judgment_name, judgment in judgments.items():
        for field, value in judgment.items():
            if isinstance(value, str) and "GenericEnvelopeShape" in value:
                references.append(
                    {
                        "path": f"$.judgments.{judgment_name}.{field}",
                        "value": value,
                    }
                )

    store = validator.ArtifactIndex(root)
    cases = root / "artifacts-v0.2.4" / "closure-classification"

    def closure_status(name: str) -> str:
        path = cases / f"{name}.json"
        reference = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        return validator._artifact_closure(
            {"run-spec": reference}, store
        ).status

    output = {
        "classification": "Definition/interface dependency check",
        "spec_sha256": sha256(spec_path),
        "spec_hash_exact": sha256(spec_path) == EXPECTED_SPEC_SHA256,
        "normative_precedence": spec.get("normative_precedence"),
        "judgment_keys": sorted(judgments),
        "generic_envelope_shape_defined_in_judgments": (
            "GenericEnvelopeShape" in judgments
        ),
        "generic_envelope_shape_references": references,
        "top_level_base_envelope_shape_present": bool(
            spec.get("base_envelope_shape")
        ),
        "normative_dependency_closed": (
            not references or "GenericEnvelopeShape" in judgments
        ),
        "executable_controls": {
            "complete_unsupported": closure_status(
                "shape-valid-unsupported-future-type"
            ),
            "malformed_unsupported": closure_status(
                "unsupported-missing-artifact-type"
            ),
        },
        "admission_bypass_claim": False,
        "p_np_claim": False,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if output["normative_dependency_closed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
