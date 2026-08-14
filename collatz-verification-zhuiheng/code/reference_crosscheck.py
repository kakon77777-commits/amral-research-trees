"""Cross-check the Rust engine against the Python bigint reference.

數學戰士「墜衡」 / AMRAL Research Lab.

The two implementations share no code, no language, and no arithmetic model:
the engine is Rust with fixed-width `u128` and a congruence sieve, the
reference is Python with arbitrary-precision integers and no sieve at all. They
are compared on identical intervals, quantity by quantity.

This is the gate that catches defects which the engine's own self-test cannot
see, because the self-test is written by the same hand as the engine.

Usage:  python code/reference_crosscheck.py [lo] [hi]
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BINARY = ROOT / "build" / "collatz_verify.exe"
COMPARED = (
    "odd_starts_checked",
    "max_sigma",
    "max_sigma_at",
    "max_expansion_peak",
    "max_expansion_at",
)
# k is varied as well: the reference has no sieve, so agreeing with it at
# several k at once also pins the sieve against a sieve-free walk.
SIEVES = (1, 6, 14, 20, 24)


def main() -> int:
    sys.path.insert(0, str(ROOT / "code"))
    import collatz_ref

    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 300_000

    expected = collatz_ref.verify_descent(lo, hi)
    runs = []
    for k in SIEVES:
        proc = subprocess.run(
            [str(BINARY), "--from", str(lo), "--to", str(hi),
             "--sieve", str(k), "--threads", "4"],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        got = json.loads(proc.stdout)
        diffs = {
            key: {"reference": expected[key], "engine": got.get(key)}
            for key in COMPARED
            if expected[key] != got.get(key)
        }
        runs.append({
            "sieve_k": k,
            "resolved_by_one_k_step_jump": got["resolved_by_one_k_step_jump"],
            "needed_iteration": got["needed_iteration"],
            "disagreements": diffs,
            "agree": not diffs,
        })

    # A cross-check on an interval where the sieve never hands anything to the
    # iterative path, or where nothing interesting happens, would agree for the
    # wrong reason. Both conditions are asserted, not assumed.
    exercised = all(r["needed_iteration"] > 0 for r in runs)
    nontrivial = expected["max_sigma"] > 1 and expected["odd_starts_checked"] > 1000

    report = {
        "tool": "reference_crosscheck.py",
        "interval": [lo, hi],
        "reference_implementation": "collatz_ref.py (CPython arbitrary-precision, no sieve)",
        "engine_implementation": "collatz_verify.rs (u128, congruence sieve, 4 threads)",
        "quantities_compared": list(COMPARED),
        "reference_result": expected,
        "runs": runs,
        "iterative_path_exercised_at_every_k": exercised,
        "interval_is_nontrivial": nontrivial,
        "agree": all(r["agree"] for r in runs) and exercised and nontrivial,
    }
    print(json.dumps(report, indent=2))
    return 0 if report["agree"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
