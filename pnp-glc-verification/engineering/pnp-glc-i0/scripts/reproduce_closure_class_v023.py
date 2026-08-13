"""Executable CLOSURE-CLASS-01 regression for the v0.2.3 candidate.

Exit zero requires every malformed unsupported envelope to classify as FAIL,
every complete unsupported envelope to classify as UNKNOWN, and a pinned
supported run-spec to classify as PASS. These are interface conformance checks;
they make no P/NP claim.
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

    import pnp_glc_i0.semantic_validator_v023 as validator

    case_root = root / "artifacts-v0.2.3" / "closure-classification"
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

    supported = root / "artifacts-v0.2.3" / "run-standard.v0.2.3.json"
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
    unexpected = [probe["name"] for probe in probes if not probe["conformant"]]
    print(
        json.dumps(
            {
                "classification": "Experiment / interface regression",
                "validator_version": validator.VALIDATOR_VERSION,
                "probe_count": len(probes),
                "unexpected": unexpected,
                "all_conformant": not unexpected,
                "admission_bypass_claim": False,
                "p_np_claim": False,
                "probes": probes,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
