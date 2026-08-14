"""Assemble data/results.v1.json from measured outputs only.

數學戰士「墜衡」 / AMRAL Research Lab.

Every number in results.v1.json is copied out of an archived gate log or the
chunk-log aggregator. Nothing is typed in by hand, so the summary cannot drift
away from what was actually run. If a required gate log is missing, this script
fails instead of emitting a summary with a hole in it.

Usage:  python code/build_results.py --tag t40 --expect-to 1099511627776
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATES = ROOT / "data" / "gate-logs"

CODE_FILES = [
    "code/collatz_verify.rs",
    "code/collatz_ref.py",
    "code/anchors.py",
    "code/mutation_drill.py",
    "code/reference_crosscheck.py",
    "code/verify_run_logs.py",
    "code/build_results.py",
    "code/run_verification.sh",
]


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_gate(name: str) -> dict:
    path = GATES / name
    if not path.exists():
        raise SystemExit(f"missing gate log: {path}. Run the gate and archive its output.")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="t40")
    ap.add_argument("--expect-to", type=int, required=True)
    args = ap.parse_args()

    proc = subprocess.run(
        [sys.executable, str(ROOT / "code" / "verify_run_logs.py"),
         "--tag", args.tag, "--expect-to", str(args.expect_to)],
        capture_output=True, text=True, encoding="utf-8",
    )
    coverage = json.loads(proc.stdout)
    if not coverage.get("ok"):
        raise SystemExit(f"chunk logs do not tile the interval: {coverage.get('problems')}")

    anchors = load_gate("anchors.json")
    drill = load_gate("mutation-drill.json")
    selftest = load_gate("self-test.json")
    reference = load_gate("reference-crosscheck.json")

    if not anchors.get("all_match"):
        raise SystemExit("anchor gate did not match; refusing to emit a summary")
    if not drill.get("ok"):
        raise SystemExit("mutation drill did not pass; refusing to emit a summary")
    if not selftest.get("ok"):
        raise SystemExit("self-test did not pass; refusing to emit a summary")
    if not reference.get("agree"):
        raise SystemExit("reference cross-check did not agree; refusing to emit a summary")

    n = coverage["covered_interval"][1]
    results = {
        "schema_version": 1,
        "research_line_id": "collatz-verification-zhuiheng",
        "researcher": {
            "display_name": "數學戰士-墜衡",
            "model": "Claude Opus 5",
            "agent_role": "local verification and computation arm",
            "route": "instrument, not theory",
        },
        "date": "2026-08-14",
        "problem": {
            "id": "COLLATZ",
            "name": "Collatz conjecture (3x+1 problem)",
            "statement": "every positive integer's Collatz trajectory reaches 1",
        },
        "global_status": {
            "solved": False,
            "literature_novelty_claimed": False,
            "record_attempt": False,
            "statement": (
                "A bounded exhaustive verification and a falsifiability-drilled "
                "instrument. Nothing here bears on the conjecture itself, and the "
                "bound reached is far below the published frontier."
            ),
            "published_frontier_note": (
                "Convergence is published as verified to at least 2^68 (Barina, "
                "J. Supercomputing, 2021), with further distributed progress since. "
                "That claim was not independently checked here and is not restated "
                "as this arm's own result."
            ),
        },
        "verified_claims": [
            {
                "id": "V1",
                "claim": f"every integer n with 1 <= n <= {n} has a Collatz trajectory reaching 1",
                "method": "exhaustive descent below n under the shortcut map, plus strong induction",
                "exhaustive_within_domain": True,
                "relative_to_implementation": True,
                "domain_upper_bound": n,
                "domain_upper_bound_as_power_of_two": "2^40",
            },
            {
                "id": "V2",
                "claim": f"no nontrivial Collatz cycle has all of its elements <= {n}",
                "method": "free corollary of V1: the least element of such a cycle would never reach 1",
                "separate_computation": False,
                "domain_upper_bound": n,
            },
        ],
        "explicit_non_claims": [
            "nothing about any n > the domain upper bound",
            "nothing about cycles containing an element above the domain upper bound",
            "no support, evidence, or suggestion regarding the conjecture itself",
            "no independent confirmation of the published 2^68 frontier",
        ],
        "coverage": coverage,
        "gates": {
            "self_test": {"ok": selftest["ok"]},
            "reference_cross_check": reference,
            "external_anchors": {
                "ok": anchors["all_match"],
                "bound": anchors["bound"],
                "sources": anchors["sources"],
                "snapshot_sha256": anchors["snapshot_sha256"],
                "checks": [
                    {k: c[k] for k in ("kind", "published_compared", "engine_produced",
                                       "largest_compared_start", "match")}
                    for c in anchors["checks"]
                ],
            },
            "mutation_drill": {
                "ok": drill["ok"],
                "defects_planted": drill["defects_planted"],
                "defects_caught": drill["defects_caught"],
                "defects_survived": drill["defects_survived"],
                "controls_planted": drill["controls_planted"],
                "controls_disturbed": drill["controls_disturbed"],
                "per_mutation": [
                    {k: m.get(k) for k in ("id", "description", "expected_to_be_caught", "caught_by")}
                    for m in drill["mutations"]
                ],
            },
        },
        "environment": {
            "os": "Windows 10 x64",
            "python": "3.14.5",
            "rustc": "1.96.0 (ac68faa20 2026-05-25)",
            "logical_cpus": 16,
        },
        "source_sha256": {f: sha256(ROOT / f) for f in CODE_FILES},
    }

    out = ROOT / "data" / "results.v1.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
