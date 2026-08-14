"""Independent recheck of source items 04-05 — the v3 threshold benchmark.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, `collatz_operation_translation_v3_threshold_bundle.zip` and
`collatz_ot_v3_threshold_benchmark.csv`, 2026-08-10 22:16 — nine minutes after
item 03.

What changed in nine minutes
----------------------------
Item 03 fixed `k = 16`. This one compiles the descent test into a residue-specific
integer threshold and **sweeps k over {8, 12, 16, 18, 20} at three domain sizes**.
The hot loop becomes a mask, a shift, a lookup and an integer comparison.

The interesting content is not the timings — those are machine-specific and this
recheck does not attempt to reproduce them. It is the **shape of the prune ratio
as k grows**, and that shape is not what one would guess:

    k = 8   0.85547
    k = 12  0.80615     <- falls
    k = 16  0.89494     <- rises past both
    k = 18  0.88106     <- falls again
    k = 20  0.86841

Bigger k is **not** monotonically better. This recheck establishes why: those
ratios are Paper 05's binomial cylinder density `P_k = A_k / 2^k` with
`A_k = sum_{u <= floor(k ln2/ln3)} C(k,u)`, and `P_k` oscillates because the
threshold `floor(k ln2/ln3)` advances by 0 or 1 as k increments. `P_k -> 1` only
in the limit, and the approach is not from below at every step.

So the sweep is measuring a theoretical quantity, and the measurement can be
checked against the closed form rather than only against itself.

Checks performed
----------------
1. Every `certified` and `fallback` pair against this arm's Rust engine — a
   separate implementation — at all 15 (k, domain) combinations.
2. Every `prune_ratio` against `certified / (certified + fallback)` exactly.
3. Every domain total against `2^e - 2`, the `[2, 2^e)` convention established
   for item 03.
4. Every prune ratio against Paper 05's `P_k`, with the finite-domain deviation
   measured rather than ignored.
5. The README's "best measured configuration" claim, which is about speedup and
   not about prune ratio — worth separating, since `k = 16` has the better ratio.

Usage:  python code/src04_v3_threshold_recheck.py <benchmark.csv> [engine]
"""

from __future__ import annotations

import csv
import json
import pathlib
import subprocess
import sys
from fractions import Fraction
from math import comb, floor, log

ROOT = pathlib.Path(__file__).resolve().parent.parent


def A_k(k: int) -> int:
    """Paper 05's contracting-cylinder count, by the exact integer boundary."""
    u_max, p = 0, 1
    while p * 3 < 2 ** k:
        p *= 3
        u_max += 1
    return sum(comb(k, u) for u in range(u_max + 1))


def main() -> int:
    csv_path = pathlib.Path(sys.argv[1])
    engine = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "build" / "collatz_verify.exe"

    rep = {
        "tool": "src04_v3_threshold_recheck.py",
        "subject": "Neo.K, collatz_ot_v3_threshold bundle and benchmark (2026-08-10 22:16)",
        "source_items": [4, 5],
        "scope": (
            "the arithmetic content of the k-sweep. Timings are machine-specific and are "
            "deliberately not reproduced; nothing here depends on them."
        ),
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    rows = []
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append({
                "exp": int(r["exp"]), "limit": int(r["limit"]), "k": int(r["k"]),
                "certified": int(r["certified"]), "fallback": int(r["fallback"]),
                "prune_ratio": float(r["prune_ratio"]),
            })

    ratio_ok = domain_ok = engine_ok = True
    table = []
    for row in rows:
        e, k = row["exp"], row["k"]
        total = row["certified"] + row["fallback"]
        if total != 2 ** e - 2:
            domain_ok = False
        exact_ratio = Fraction(row["certified"], total)
        if abs(float(exact_ratio) - row["prune_ratio"]) > 1e-15:
            ratio_ok = False

        # independent implementation: the Rust engine's block classification
        out = subprocess.run(
            [str(engine), "--block", str(k), "--to", str(2 ** e)],
            capture_output=True, text=True, encoding="utf-8", check=True)
        d = json.loads(out.stdout)
        # engine scans [1, 2^e); the bundle's domain is [2, 2^e), and n = 1 is an
        # equality case, so drop exactly one equality to compare like with like
        eng_cert = d["strict_descent"]
        eng_fallback = (d["equality"] - 1) + d["ascent"]
        if eng_cert != row["certified"] or eng_fallback != row["fallback"]:
            engine_ok = False

        Pk = Fraction(A_k(k), 2 ** k)
        table.append({
            "exp": e, "k": k,
            "certified": row["certified"], "engine_certified": eng_cert,
            "fallback": row["fallback"], "engine_fallback": eng_fallback,
            "prune_ratio": float(exact_ratio),
            "paper05_P_k": float(Pk),
            "deviation_from_P_k": float(exact_ratio - Pk),
        })

    check("SRC04_certified_and_fallback_match_the_rust_engine", engine_ok)
    check("SRC04_prune_ratios_equal_certified_over_total", ratio_ok)
    check("SRC04_every_domain_total_is_2e_minus_2", domain_ok)

    # the ratios are Paper 05's cylinder density, to within a finite-domain
    # boundary correction that shrinks as the domain grows
    dev_by_k = {}
    for t in table:
        dev_by_k.setdefault(t["k"], []).append((t["exp"], abs(t["deviation_from_P_k"])))
    close = all(abs(t["deviation_from_P_k"]) < 1e-5 for t in table)
    check("SRC04_prune_ratios_are_Paper_05_cylinder_densities", close,
          f"largest deviation {max(abs(t['deviation_from_P_k']) for t in table):.3e}")
    shrinks = all(
        max(d for e_, d in v) == max(d for e_, d in v if e_ == min(e2 for e2, _ in v))
        for v in dev_by_k.values())
    check("SRC04_finite_domain_deviation_shrinks_as_the_domain_grows", shrinks,
          f"{ {k: [f'{d:.2e}' for _, d in sorted(v)] for k, v in dev_by_k.items()} }")

    # non-monotonicity is a real structural fact, not noise
    at24 = {t["k"]: t["prune_ratio"] for t in table if t["exp"] == 24}
    nonmono = at24[12] < at24[8] and at24[16] > at24[8] and at24[18] < at24[16] and at24[20] < at24[18]
    check("SRC04_prune_ratio_is_not_monotone_in_k", nonmono, f"{at24}")

    # and the closed form reproduces that shape exactly
    Pk_shape = {k: float(Fraction(A_k(k), 2 ** k)) for k in (8, 12, 16, 18, 20)}
    shape_ok = (Pk_shape[12] < Pk_shape[8] and Pk_shape[16] > Pk_shape[8]
                and Pk_shape[18] < Pk_shape[16] and Pk_shape[20] < Pk_shape[18])
    check("SRC04_the_closed_form_P_k_reproduces_the_same_non_monotone_shape", shape_ok,
          f"{Pk_shape}")

    # the README's "best configuration" is about speed, not prune ratio
    best_ratio_k = max(at24, key=lambda k: at24[k])
    check("SRC04_k16_has_the_best_prune_ratio_at_2_24", best_ratio_k == 16,
          f"best prune ratio at k={best_ratio_k}")

    rep["counts"]["benchmark_rows"] = len(rows)
    rep["counts"]["engine_cross_checks"] = len(rows)
    rep["measured"]["sweep"] = table
    rep["measured"]["P_k_closed_form"] = Pk_shape
    rep["measured"]["floor_alpha_k"] = {
        k: floor(k * log(2) / log(3)) for k in (8, 12, 16, 18, 20)}
    rep["measured"]["assessment"] = {
        "what_it_establishes": (
            "the descent test compiles to a residue-indexed integer threshold, and the "
            "resulting prune ratio is exactly Paper 05's cylinder density P_k = A_k/2^k "
            "up to a finite-domain correction that shrinks as the domain grows. The sweep "
            "is therefore measuring a theoretical quantity, and it measures it correctly."
        ),
        "the_non_monotonicity": (
            "Prune ratio rises to k = 16 and then FALLS at 18 and 20. That is not noise "
            "and not a defect: floor(k ln2/ln3) advances by 0 or 1 as k increments, so "
            "P_k oscillates on its way to 1. k = 16 sits at a favourable step of that "
            "staircase. Choosing a larger k costs table-build time AND gives a worse "
            "prune ratio, which is worth knowing before anyone assumes deeper is better."
        ),
        "reading_the_README_precisely": (
            "The bundle's 'best measured configuration at n < 2^24: k = 18' is a claim "
            "about SPEEDUP, and it is correct on its own numbers. k = 16 has the better "
            "PRUNE RATIO - 0.89494 against 0.88106. Both statements are true of different "
            "quantities, and the README lists the k = 18 ratio right beside the word "
            "'best', where it could be read as claiming the ratio too."
        ),
        "not_reproduced": (
            "every timing column. They are machine-specific, and no check here depends "
            "on one."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
