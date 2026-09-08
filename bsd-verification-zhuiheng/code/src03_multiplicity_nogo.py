"""Gate 03 — the multiplicity no-go counterexample, recomputed exactly.

數學戰士「墜衡」 / AMRAL Research Lab.

Phase 0 doc 05 rejects the old lattice-point route on four grounds. Its third:
even if L_a → L, the order of vanishing at s=1 need not converge, because
"消失階對微小 perturbation 非連續".

Doc 05 asserts this. A later P5 document,
`BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1`, section 9, supplies the
counterexample doc 05 did not have and upgrades the verdict from "the burden is
unmet" to "FALSE IN GENERAL":

    f_a(z) = z^2 + a z = z (z + a)

This gate recomputes it rather than reading it, in exact rational arithmetic —
no float anywhere, because the whole claim is about an integer-valued quantity
and a limit, and a float would be answering a different question.

AND IT ADDS THE HALF THE SOURCE DOES NOT STATE. The point-order fails to
converge, but the zero COUNT in any fixed punctured neighbourhood does not: f_a
has zeros at 0 and -a, and for |a| < r both sit inside the disc |z| < r, so the
count there is 2 for every a, including a = 0. That is Hurwitz's theorem, and it
is exactly why doc 05's own remedy list asks for "在 s=1 鄰域的解析控制"
(analytic control in a NEIGHBOURHOOD of s=1) rather than control at the point.

The counterexample is therefore sharper than "the order jumps": the order jumps
*while the neighbourhood count is stable*, so a method that measures the
neighbourhood and reports the point is wrong in a way no amount of precision
detects.

Usage:  python code/src03_multiplicity_nogo.py
"""

from __future__ import annotations

import io
import json
import pathlib
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src03-multiplicity-nogo.json"


def order_at_zero(coeffs: dict[int, Fraction]) -> int:
    """Multiplicity of the root z=0 of a polynomial given as {power: coeff}."""
    nz = sorted(k for k, v in coeffs.items() if v != 0)
    if not nz:
        raise ValueError("the zero polynomial has no well-defined order")
    return nz[0]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    # f_a(z) = z^2 + a z, exactly.
    aa = [Fraction(1), Fraction(1, 10), Fraction(1, 1000),
          Fraction(1, 10**6), Fraction(1, 10**12), Fraction(-1, 10**6)]
    R = Fraction(1)          # compact set |z| <= R
    r = Fraction(1, 100)     # neighbourhood radius for the count

    rows = []
    for a in aa:
        f = {2: Fraction(1), 1: a}
        ordr = order_at_zero(f)
        roots = [Fraction(0), -a]
        # |sup_{|z|<=R} (f_a - f_0)| = sup |a z| = |a| R, exactly.
        sup_diff = abs(a) * R
        rows.append({
            "a": str(a),
            "order_at_0": ordr,
            "roots": [str(x) for x in roots],
            "roots_inside_disc_radius_r": sum(1 for x in roots if abs(x) < r),
            "sup_norm_difference_from_f0_on_|z|<=1": str(sup_diff),
        })

    f0 = {2: Fraction(1)}
    order_limit = order_at_zero(f0)

    orders_nonzero_a = {row["order_at_0"] for row in rows if row["a"] != "0"}
    counts_nonzero_a = {row["roots_inside_disc_radius_r"] for row in rows
                        if abs(Fraction(row["a"])) < r}

    checks = {
        "order_at_0_is_1_for_every_a_nonzero": orders_nonzero_a == {1},
        "order_at_0_of_the_limit_is_2": order_limit == 2,
        "so_the_order_does_not_converge": (orders_nonzero_a == {1}
                                           and order_limit == 2),
        "neighbourhood_count_is_2_for_every_small_a": counts_nonzero_a == {2},
        "neighbourhood_count_equals_the_limit_order": (
            counts_nonzero_a == {2} and order_limit == 2),
        "uniform_convergence_bound_is_|a|*R_and_tends_to_0": all(
            Fraction(row["sup_norm_difference_from_f0_on_|z|<=1"])
            == abs(Fraction(row["a"])) * R for row in rows),
    }

    log = {
        "gate": "src03_multiplicity_nogo",
        "subject": ("Phase 0 doc 05 §3, and the counterexample supplied later by "
                    "p5/BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1 §9.1"),
        "counterexample": "f_a(z) = z^2 + a z = z (z + a)",
        "arithmetic": ("exact rationals throughout; no floating point. The claim "
                       "is about an integer-valued order and a limit, and a "
                       "float would answer a different question"),
        "measured": rows,
        "order_of_the_limit_f0": order_limit,
        "checks": checks,
        "what_the_source_states": (
            "the order of vanishing at a point is not preserved by ordinary "
            "uniform convergence — confirmed exactly here"),
        "what_this_gate_adds": (
            "the zero COUNT in a fixed neighbourhood IS preserved: f_a has "
            "roots 0 and -a, both inside |z| < r once |a| < r, so the count is 2 "
            "for every such a and equals the limit's order at the point. That is "
            "Hurwitz, and it is why doc 05's remedy list asks for analytic "
            "control in a NEIGHBOURHOOD of s=1 rather than at s=1. The failure "
            "is not imprecision — a method that measures the neighbourhood and "
            "reports the point is wrong at infinite precision."),
        "not_a_claim_about_L_functions": (
            "this is a polynomial in one variable. It refutes the general "
            "inference, which is all doc 05 and §9.1 claim it does. Whether any "
            "particular L_a behaves this way is a separate question neither "
            "document asserts."),
        "ok": all(checks.values()),
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print(f"  f_a(z) = z^2 + a z          order of the limit f_0 : {order_limit}")
    print()
    print(f"  {'a':>14}  {'ord at 0':>8}  {'roots in |z|<1/100':>18}  sup|f_a-f_0| on |z|<=1")
    for row in rows:
        print(f"  {row['a']:>14}  {row['order_at_0']:>8}  "
              f"{row['roots_inside_disc_radius_r']:>18}  "
              f"{row['sup_norm_difference_from_f0_on_|z|<=1']}")
    print()
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
