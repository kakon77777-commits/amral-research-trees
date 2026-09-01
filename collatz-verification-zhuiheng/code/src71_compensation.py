"""RUN-052 — independent recheck of Hard-Zeta round A-U.2d.24.

`Binary Replenishment / Ternary Reset Rigidity` (source item 71). 數學戰士「墜衡」.

A-U.2d.23 made a zero-defect return an exact cross-adic transport law. This
round prices the NONZERO-defect regions that have to perform the replenishment.
For a contiguous path with `x = r + Mn`, `z = s + Mn'` and `n, n' > 0`, define

    A  = v2(n),  A' = v2(n'),  B = v3(n),  B' = v3(n')
    c2 = Q + A' - A            (binary divisibility recovered)
    c3 = L + B  - B'           (ternary divisibility removed)

against the pure multiplier `A' = A - Q`, `B' = B + L`. Then `d = 0` exactly
when `c2 = c3 = 0`, the quadrant `c2 <= 0, c3 <= 0` is empty of nonzero
defects, and a synchronized event carries an exact primitive cylinder equation
`2^{c2} u' = 3^{c3} u + omega` in a small CRT window.

Five things this gate adds.

**Theorem 5.1's barrier `|d| < 2^Q 3^L` is loose by exactly a factor of 3.**
Measured over their whole population the largest ratio is 1/3, and the sharp
form `|d| <= 2^Q 3^{L-1}` is ATTAINED. Both are scored.

**Theorems 7.1 and 7.2 have no counter of their own.** The ultrametric
alignment laws -- `v2(d) = A` with a congruence mod `2^{c2}`, and `v3(d) = B'`
with a congruence mod `3^{c3}` -- are asserted inside their validator and
counted nowhere, on the largest populations in the round.

**Two assertions in the exclusive branches restate their own hypotheses.**
`c3 <= 0` IS `B' >= B + L` by the definition of `c3`, and `c2 <= 0` IS
`A - A' >= Q`. Both predicates are evaluated separately here and their
disagreement counted, so the claim is a measurement rather than an assertion.

**Two blocks are true by construction, and each gets a control.** Their
telescoping holds because the partition is built consecutive; their synthetic
quadrant block holds because both terms carry `2^{Q+A'} 3^{B+L}`. Each is
re-run with that one property broken, and the failures counted -- an assertion
that only goes red once its construction is violated has content but cannot be
exercised by any generated input.

**`v2`/`v3` of zero return None.** Theirs raises, which is safer than a
sentinel but forces the guard to live at every call site.

Usage:
    python code/src71_compensation.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import re
import struct
import sys
from random import Random

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src54_low_source_saturation import widen                       # noqa: E402
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    b_of, beta_hi, beta_lo, verdict_with_budget,
)

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d24_Binary_Replenishment_Ternary_Reset"
         "_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d24_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d24_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d24_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d24.json"
CHECKSUMS = "CHECKSUMS.sha256"

MODS = (3, 9, 27, 81)
Y_LIMIT = 5000
STEPS = 14


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def vp(n: int, p: int) -> int | None:
    """`v_p(n)`, or None for zero. Theirs raises `ValueError`, which is safer
    than a sentinel but puts the guard at every call site instead of here."""
    if n == 0:
        return None
    n, c = abs(n), 0
    while n % p == 0:
        n //= p
        c += 1
    return c


def syr(y: int) -> tuple[int, int]:
    x = 3 * y + 1
    q = 0
    while x % 2 == 0:
        q += 1
        x //= 2
    return x, q


def orbit(y: int, steps: int):
    st, qs = [y], []
    for _ in range(steps):
        y, q = syr(y)
        st.append(y)
        qs.append(q)
    return st, qs


def segment(st, qs, i: int, j: int, m: int):
    """Their `seg`, recomputed: the quotient states and both depths."""
    word = tuple(qs[i:j])
    ell, q = len(word), sum(word)
    bc = b_of(word)
    x, z = st[i], st[j]
    if (1 << q) * z != 3 ** ell * x + bc:
        return "affine identity failed"
    r, s = x % m, z % m
    n, n2 = (x - r) // m, (z - s) // m
    if n <= 0 or n2 <= 0:
        return None
    num = bc + 3 ** ell * r - (1 << q) * s
    if num % m:
        return "defect not integral"
    d = num // m
    a, ap = vp(n, 2), vp(n2, 2)
    bt, bp = vp(n, 3), vp(n2, 3)
    return {"x": x, "z": z, "n": n, "np": n2, "L": ell, "Q": q, "Bcode": bc,
            "d": d, "A": a, "Ap": ap, "Bt": bt, "Bp": bp,
            "c2": q + ap - a, "c3": ell + bt - bp, "word": word, "M": m}


def population():
    """Their exact enumeration: four moduli, odd `y` below 5000 not divisible
    by 3, 14 accelerated steps, windows `i in [0,7)`, `j <= i+6`."""
    out = []
    for m in MODS:
        for y in range(7, Y_LIMIT, 2):
            if y % 3 == 0:
                continue
            st, qs = orbit(y, STEPS)
            for i in range(0, 7):
                for j in range(i + 1, min(STEPS, i + 6) + 1):
                    rec = segment(st, qs, i, j, m)
                    if isinstance(rec, dict):
                        out.append(rec)
                    elif isinstance(rec, str):
                        out.append({"__error__": rec})
    return out


# ---------------------------------------------------------------------------
# instrument
# ---------------------------------------------------------------------------

def check_instrument() -> dict:
    out: dict = {"checks": 0, "failed": []}

    def want(name: str, ok: bool) -> None:
        out["checks"] += 1
        if not ok:
            out["failed"].append(name)

    want("beta bracket has width", beta_lo() < beta_hi())
    want("vp of zero is None, not a raise and not a sentinel",
         vp(0, 2) is None and vp(0, 3) is None)
    bad = sum(1 for a in range(9)
              if vp(2 ** a * 5, 2) != a or vp(3 ** a * 5, 3) != a)
    want("vp is exact", bad == 0)
    want("the accelerated step agrees with the definition", syr(7) == (11, 1))

    # the affine code, against a hand case
    want("B_P composes", b_of((1, 2)) == 3 * 1 + 2 * 1)

    # the two predicates the round's exclusive branches assert
    bad = 0
    for ell in range(1, 8):
        for q in range(ell, ell + 6):
            for a in range(0, 6):
                for ap in range(0, 6):
                    if ((q + ap - a <= 0) != (a - ap >= q)):
                        bad += 1
    want("c2 <= 0 and A - A' >= Q are the same predicate", bad == 0)
    bad = 0
    for ell in range(1, 8):
        for bt in range(0, 6):
            for bp in range(0, 6):
                if ((ell + bt - bp <= 0) != (bp >= bt + ell)):
                    bad += 1
    want("c3 <= 0 and B' >= B + L are the same predicate", bad == 0)

    # the sharpened barrier must be strictly inside the published one
    bad = sum(1 for ell in range(1, 10) for q in range(ell, ell + 5)
              if not (1 << q) * 3 ** (ell - 1) < (1 << q) * 3 ** ell)
    want("2^Q 3^{L-1} is strictly inside 2^Q 3^L", bad == 0)
    return out


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict) -> dict:
    t: dict = {"constants_checked": 0,
               "disagreeing_with_both_evaluations": 0,
               "from_the_float64_chain_not_the_nearest_double": 0,
               "exact_to_the_last_bit": 0,
               "undecided_brackets": 0,
               "missing_from_the_frontier": 0,
               "frontier_and_report_disagreeing": 0,
               "frontier_constants_the_checker_never_computes": [],
               "rows": []}
    lo, hi = widen(*beta_tight(), 40)
    b = math.log2(3)
    items = [
        ("beta", lo, hi, b, 4),
        ("beta_minus_1", lo - 1, hi - 1, b - 1, 8),
        ("two_minus_beta", 2 - hi, 2 - lo, 2 - b, 20),
        ("resonance_threshold", (lo - 1) / hi, (hi - 1) / lo, (b - 1) / b, 12),
    ]
    rc = report.get("constants", {})
    for name, blo, bhi, chain, budget in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        rpt = rc.get(name)
        row = {"constant": name, "frontier": repr(pub), "report": repr(rpt),
               "budget": budget}
        if rpt is not None and rpt != pub:
            t["frontier_and_report_disagreeing"] += 1
            row["frontier_minus_report_ulps"] = bits(pub) - bits(rpt)
        verdict, dd = verdict_with_budget(pub, blo, bhi, chain, budget)
        if verdict == "undecided":
            t["undecided_brackets"] += 1
        elif verdict == "exact":
            t["exact_to_the_last_bit"] += 1
        elif verdict == "the float64 chain":
            t["from_the_float64_chain_not_the_nearest_double"] += 1
        else:
            t["disagreeing_with_both_evaluations"] += 1
        row["verdict"] = verdict if dd == 0 else "%+d ulp, %s" % (dd, verdict)
        t["rows"].append(row)
    numeric = {k: v for k, v in frontier.items() if isinstance(v, float)}
    t["frontier_constants_the_checker_never_computes"] = sorted(
        k for k in numeric if k not in rc)
    return t


# ---------------------------------------------------------------------------
# Theorems 4.1 and 5.1
# ---------------------------------------------------------------------------

def check_bounds(segs: list) -> dict:
    """The affine-correction bound and the defect-product barrier.

    Both are scored for ATTAINMENT as well as for violation, because the two
    turn out to have opposite tightness: 4.1's upper bound is reached, while
    5.1 carries a spare factor of three.
    """
    t: dict = {"segments": 0,
               "affine_lower_bound_violations": 0,
               "affine_upper_bound_violations": 0,
               "affine_upper_bound_attained": 0,
               "affine_loose_upper_bound_violations": 0,
               "barrier_violations": 0,
               "sharpened_barrier_violations": 0,
               "sharpened_barrier_attained": 0,
               "largest_barrier_numerator": 0,
               "largest_barrier_denominator": 0}
    best_num, best_den = 0, 1
    for r in segs:
        t["segments"] += 1
        ell, q, bc, d = r["L"], r["Q"], r["Bcode"], r["d"]
        tight = (1 << (q - ell)) * (3 ** ell - (1 << ell))
        if not bc > 0:
            t["affine_lower_bound_violations"] += 1
        if not bc <= tight:
            t["affine_upper_bound_violations"] += 1
        if bc == tight:
            t["affine_upper_bound_attained"] += 1
        if not bc < (1 << (q - ell)) * 3 ** ell:
            t["affine_loose_upper_bound_violations"] += 1
        if not abs(d) < (1 << q) * 3 ** ell:
            t["barrier_violations"] += 1
        # the sharp form, measured: |d| <= 2^Q 3^{L-1}
        sharp = (1 << q) * 3 ** (ell - 1)
        if not abs(d) <= sharp:
            t["sharpened_barrier_violations"] += 1
        if abs(d) == sharp:
            t["sharpened_barrier_attained"] += 1
        if abs(d) * best_den > best_num * ((1 << q) * 3 ** ell):
            best_num, best_den = abs(d), (1 << q) * 3 ** ell
    t["largest_barrier_numerator"] = best_num
    t["largest_barrier_denominator"] = best_den
    return t


# ---------------------------------------------------------------------------
# Theorem 6.1 and Corollary 6.2
# ---------------------------------------------------------------------------

def check_equivalence(segs: list) -> dict:
    t: dict = {"segments": 0, "zero_defect": 0, "nonzero_defect": 0,
               "equivalence_violations": 0,
               "zero_defect_with_nonzero_compensation": 0,
               "zero_compensation_with_nonzero_defect": 0,
               "double_deficit_violations": 0,
               "nonzero_with_c2_positive_only": 0,
               "nonzero_with_c3_positive_only": 0,
               "nonzero_with_both_positive": 0}
    for r in segs:
        t["segments"] += 1
        d, c2, c3 = r["d"], r["c2"], r["c3"]
        zero_comp = (c2 == 0 and c3 == 0)
        if (d == 0) != zero_comp:
            t["equivalence_violations"] += 1
            if d == 0:
                t["zero_defect_with_nonzero_compensation"] += 1
            else:
                t["zero_compensation_with_nonzero_defect"] += 1
        if d == 0:
            t["zero_defect"] += 1
            continue
        t["nonzero_defect"] += 1
        if not (c2 > 0 or c3 > 0):
            t["double_deficit_violations"] += 1
        if c2 > 0 and c3 > 0:
            t["nonzero_with_both_positive"] += 1
        elif c2 > 0:
            t["nonzero_with_c2_positive_only"] += 1
        else:
            t["nonzero_with_c3_positive_only"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 7.1 and 7.2 -- the laws with no counter of their own
# ---------------------------------------------------------------------------

def check_alignment(segs: list) -> dict:
    t: dict = {"binary_alignment_population": 0,
               "ternary_alignment_population": 0,
               "binary_valuation_violations": 0,
               "binary_congruence_violations": 0,
               "ternary_valuation_violations": 0,
               "ternary_congruence_violations": 0,
               "defect_zero_while_a_depth_is_positive": 0}
    for r in segs:
        d, c2, c3 = r["d"], r["c2"], r["c3"]
        a, bp, ell, q = r["A"], r["Bp"], r["L"], r["Q"]
        n, n2 = r["n"], r["np"]
        if c2 > 0:
            t["binary_alignment_population"] += 1
            if d == 0:
                t["defect_zero_while_a_depth_is_positive"] += 1
            elif vp(d, 2) != a:
                t["binary_valuation_violations"] += 1
            if ((d >> a) + 3 ** ell * (n >> a)) % (1 << c2):
                t["binary_congruence_violations"] += 1
        if c3 > 0:
            t["ternary_alignment_population"] += 1
            if d == 0:
                t["defect_zero_while_a_depth_is_positive"] += 1
            elif vp(d, 3) != bp:
                t["ternary_valuation_violations"] += 1
            if ((d // 3 ** bp) - (1 << q) * (n2 // 3 ** bp)) % (3 ** c3):
                t["ternary_congruence_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 8.1 and 9.1
# ---------------------------------------------------------------------------

def check_primitive(segs: list) -> dict:
    t: dict = {"synchronized": 0,
               "u_not_coprime_to_six": 0,
               "omega_not_coprime_to_six": 0,
               "cylinder_equation_violations": 0,
               "binary_residue_violations": 0,
               "ternary_residue_violations": 0,
               "crt_window_violations": 0,
               "sharpened_window_violations": 0,
               "sharpened_window_attained": 0,
               "windows_within_a_factor_of_two_of_failing": 0,
               "largest_window_numerator": 0,
               "largest_window_denominator": 0}
    bn, bd = 0, 1
    for r in segs:
        c2, c3 = r["c2"], r["c3"]
        if not (c2 > 0 and c3 > 0):
            continue
        t["synchronized"] += 1
        a, ap, bt, bp = r["A"], r["Ap"], r["Bt"], r["Bp"]
        n, n2, d, ell, q = r["n"], r["np"], r["d"], r["L"], r["Q"]
        u = n // ((1 << a) * 3 ** bt)
        up = n2 // ((1 << ap) * 3 ** bp)
        om = d // ((1 << a) * 3 ** bp)
        if math.gcd(abs(u), 6) != 1 or math.gcd(abs(up), 6) != 1:
            t["u_not_coprime_to_six"] += 1
        if math.gcd(abs(om), 6) != 1:
            t["omega_not_coprime_to_six"] += 1
        if (1 << c2) * up != 3 ** c3 * u + om:
            t["cylinder_equation_violations"] += 1
        if (om + 3 ** c3 * u) % (1 << c2):
            t["binary_residue_violations"] += 1
        if (om - (1 << c2) * up) % (3 ** c3):
            t["ternary_residue_violations"] += 1
        dmod = (1 << c2) * 3 ** c3
        lhs = abs(om) * (1 << ap) * 3 ** bt
        if not lhs < dmod:
            t["crt_window_violations"] += 1
        # the same spare factor of three the defect barrier carries: the sharp
        # form is 3|omega| 2^{A'} 3^{B} <= 2^{c2} 3^{c3}
        if not 3 * lhs <= dmod:
            t["sharpened_window_violations"] += 1
        if 3 * lhs == dmod:
            t["sharpened_window_attained"] += 1
        if not 2 * lhs < dmod:
            t["windows_within_a_factor_of_two_of_failing"] += 1
        if lhs * bd > bn * dmod:
            bn, bd = lhs, dmod
    t["largest_window_numerator"] = bn
    t["largest_window_denominator"] = bd
    return t


# ---------------------------------------------------------------------------
# Theorem 11.1 -- and the two assertions that restate their hypotheses
# ---------------------------------------------------------------------------

def check_trichotomy(segs: list) -> dict:
    """The exclusive-channel consequences, measured against their hypotheses.

    Their validator asserts `B' >= B + L` under `c3 <= 0` and `A - A' >= Q`
    under `c2 <= 0`. By the definitions `c3 = L + B - B'` and `c2 = Q + A' - A`
    each of those IS its own hypothesis. Rather than assert that, both
    predicates are evaluated on every segment and their disagreement counted.
    """
    t: dict = {"segments": 0,
               "binary_exclusive": 0, "ternary_exclusive": 0,
               "ternary_overdrain_violations": 0,
               "binary_overdrain_violations": 0,
               "c3_nonpositive_disagreeing_with_B_prime_bound": 0,
               "c2_nonpositive_disagreeing_with_A_bound": 0,
               "predicate_pairs_compared": 0,
               "trichotomy_classes_unaccounted": 0}
    for r in segs:
        t["segments"] += 1
        c2, c3, d = r["c2"], r["c3"], r["d"]
        a, ap, bt, bp, ell, q = (r["A"], r["Ap"], r["Bt"], r["Bp"],
                                 r["L"], r["Q"])
        t["predicate_pairs_compared"] += 2
        if (c3 <= 0) != (bp >= bt + ell):
            t["c3_nonpositive_disagreeing_with_B_prime_bound"] += 1
        if (c2 <= 0) != (a - ap >= q):
            t["c2_nonpositive_disagreeing_with_A_bound"] += 1
        if d == 0:
            continue
        if c2 > 0 and c3 <= 0:
            t["binary_exclusive"] += 1
            if not bp >= bt + ell:
                t["ternary_overdrain_violations"] += 1
        elif c2 <= 0 and c3 > 0:
            t["ternary_exclusive"] += 1
            if not a - ap >= q:
                t["binary_overdrain_violations"] += 1
        elif not (c2 > 0 and c3 > 0):
            t["trichotomy_classes_unaccounted"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 12.1 -- with the construction broken as a control
# ---------------------------------------------------------------------------

def check_telescoping(trials: int = 4000, seed: int = 26081424) -> dict:
    """Their partition sum, and the same sum on non-consecutive blocks.

    The identity `sum c2 = Q + A'_last - A_first` holds because consecutive
    blocks share an endpoint, so `A'_i` and `A_{i+1}` are the same valuation of
    the same number. Their generator always builds it that way. Breaking only
    that property is what shows the assertion has content.
    """
    t: dict = {"partitions": 0, "blocks": 0,
               "binary_telescoping_violations": 0,
               "ternary_telescoping_violations": 0,
               "zero_block_with_nonzero_compensation": 0,
               "broken_partitions": 0,
               "broken_binary_telescoping_failures": 0,
               "broken_ternary_telescoping_failures": 0}
    rng = Random(seed)
    for _ in range(trials):
        m = rng.choice(MODS)
        y = rng.randrange(7, Y_LIMIT, 2)
        if y % 3 == 0:
            continue
        st, qs = orbit(y, STEPS)
        a = rng.randint(0, 5)
        b = rng.randint(a + 2, 12)
        inner = sorted(rng.sample(range(a + 1, b),
                                  min(3, max(0, b - a - 1))))
        pts = [a] + inner + [b]
        rows = [segment(st, qs, u, v, m) for u, v in zip(pts, pts[1:])]
        if any(not isinstance(x, dict) for x in rows):
            continue
        t["partitions"] += 1
        t["blocks"] += len(rows)
        q = sum(x["Q"] for x in rows)
        ell = sum(x["L"] for x in rows)
        if sum(x["c2"] for x in rows) != q + rows[-1]["Ap"] - rows[0]["A"]:
            t["binary_telescoping_violations"] += 1
        if sum(x["c3"] for x in rows) != ell + rows[0]["Bt"] - rows[-1]["Bp"]:
            t["ternary_telescoping_violations"] += 1
        for x in rows:
            if x["d"] == 0 and not (x["c2"] == 0 and x["c3"] == 0):
                t["zero_block_with_nonzero_compensation"] += 1
        # the control: shift each block's start so the blocks no longer chain
        shifted = [segment(st, qs, u + 1, v, m)
                   for u, v in zip(pts, pts[1:]) if v > u + 1]
        if not shifted or any(not isinstance(x, dict) for x in shifted):
            continue
        t["broken_partitions"] += 1
        q2 = sum(x["Q"] for x in shifted)
        l2 = sum(x["L"] for x in shifted)
        if sum(x["c2"] for x in shifted) != (q2 + shifted[-1]["Ap"]
                                             - shifted[0]["A"]):
            t["broken_binary_telescoping_failures"] += 1
        if sum(x["c3"] for x in shifted) != (l2 + shifted[0]["Bt"]
                                             - shifted[-1]["Bp"]):
            t["broken_ternary_telescoping_failures"] += 1
    return t


# ---------------------------------------------------------------------------
# their two synthetic blocks, each with the construction broken
# ---------------------------------------------------------------------------

def check_synthetic(trials: int = 20000, seed: int = 26081424) -> dict:
    t: dict = {"word_trials": 0,
               "word_lower_bound_violations": 0,
               "word_upper_bound_violations": 0,
               "word_upper_bound_attained": 0,
               "word_valuation_below_length": 0,
               "quadrant_trials": 0,
               "quadrant_divisibility_violations": 0,
               "quadrant_size_violations": 0,
               "quadrant_zero_defects": 0,
               "free_quadrant_trials": 0,
               "free_quadrant_divisibility_failures": 0,
               "free_quadrant_size_failures": 0}
    rng = Random(seed)
    for _ in range(trials):
        t["word_trials"] += 1
        ell = rng.randint(1, 12)
        word = tuple(rng.randint(1, 7) for _ in range(ell))
        q, bc = sum(word), b_of(word)
        if q < ell:
            t["word_valuation_below_length"] += 1
        tight = (1 << (q - ell)) * (3 ** ell - (1 << ell))
        if not bc > 0:
            t["word_lower_bound_violations"] += 1
        if not bc <= tight:
            t["word_upper_bound_violations"] += 1
        if bc == tight:
            t["word_upper_bound_attained"] += 1

    def quadrant(rng2: Random, forbidden: bool):
        ell = rng2.randint(1, 10)
        q = rng2.randint(ell, ell + 15)
        ap = rng2.randint(0, 10)
        bt = rng2.randint(0, 10)
        if forbidden:
            a = rng2.randint(q + ap, q + ap + 8)
            bp = rng2.randint(bt + ell, bt + ell + 8)
        else:
            a = rng2.randint(0, q + ap + 8)
            bp = rng2.randint(0, bt + ell + 8)
        u = rng2.randrange(1, 100, 2)
        while u % 3 == 0:
            u += 2
        up = rng2.randrange(1, 100, 2)
        while up % 3 == 0:
            up += 2
        n = (1 << a) * 3 ** bt * u
        n2 = (1 << ap) * 3 ** bp * up
        d = (1 << q) * n2 - 3 ** ell * n
        mod = (1 << q) * 3 ** ell
        return d % mod == 0, (d == 0 or abs(d) >= mod), d == 0

    rng = Random(seed + 1)
    for _ in range(trials):
        t["quadrant_trials"] += 1
        div, size, zero = quadrant(rng, True)
        t["quadrant_divisibility_violations"] += int(not div)
        t["quadrant_size_violations"] += int(not size)
        t["quadrant_zero_defects"] += int(zero)
    rng = Random(seed + 1)
    for _ in range(trials):
        t["free_quadrant_trials"] += 1
        div, size, _z = quadrant(rng, False)
        t["free_quadrant_divisibility_failures"] += int(not div)
        t["free_quadrant_size_failures"] += int(not size)
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"synchronized_rows": 0, "exclusive_rows": 0,
               "depth_fields_disagreeing": 0,
               "quotient_identity_violations": 0,
               "barrier_violations": 0,
               "class_disagreeing_with_the_depths": 0}
    for key, tag in (("synchronized_examples", "sync"),
                     ("exclusive_examples", "excl")):
        for ex in report.get(key, []) or []:
            if tag == "sync":
                t["synchronized_rows"] += 1
            else:
                t["exclusive_rows"] += 1
            ell, q, d = ex["L"], ex["Q"], ex["d"]
            a, ap, bt, bp = ex["A"], ex["Ap"], ex["Bt"], ex["Bp"]
            if q + ap - a != ex["c2"] or ell + bt - bp != ex["c3"]:
                t["depth_fields_disagreeing"] += 1
            if not abs(d) < (1 << q) * 3 ** ell:
                t["barrier_violations"] += 1
            both = ex["c2"] > 0 and ex["c3"] > 0
            if tag == "sync" and not both:
                t["class_disagreeing_with_the_depths"] += 1
            if tag == "excl" and both:
                t["class_disagreeing_with_the_depths"] += 1
            # the affine identity, recomputed from the published endpoints
            if (1 << q) * ex["z"] - 3 ** ell * ex["x"] <= 0:
                t["quotient_identity_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# artifacts and ledger
# ---------------------------------------------------------------------------

def check_artifacts(bundle: pathlib.Path) -> dict:
    t: dict = {"files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
               "checksum_lines_naming_a_missing_file": 0,
               "files_with_no_digest_anywhere": [],
               "validation_per_file_entries": 0,
               "validation_entries_with_a_digest": 0,
               "files_absent_from_the_validation_record": [],
               "duplicate_file_pairs": []}
    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    t["files_present"] = len(present)
    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()
              for n in present}
    listed: dict = {}
    for line in (bundle / CHECKSUMS).read_text(encoding="utf-8").splitlines():
        if line.strip():
            d, n = line.split(None, 1)
            listed[n.strip()] = d
    t["digests_listed"] = len(listed)
    for n, d in listed.items():
        if n not in actual:
            t["checksum_lines_naming_a_missing_file"] += 1
        elif actual[n] != d:
            t["digest_mismatches"] += 1
    by: dict = {}
    for n, d in actual.items():
        by.setdefault(d, []).append(n)
    t["duplicate_file_pairs"] = [sorted(v) for v in by.values() if len(v) > 1]
    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    # Eleventh round, eleventh shape. Seen so far: `files` as a dict of
    # per-file results; `json_parse`/`python_compile` as dicts; and now
    # `files_checked` as a bare list with those two as plain booleans and no
    # overall pass flag at all. A reader that assumes one shape reports the
    # others as absent, which is how a real False becomes a None.
    files = val.get("files")
    files = files if isinstance(files, dict) else {}
    named = set(files)
    listed_names = val.get("files_checked")
    if isinstance(listed_names, list):
        named |= {n for n in listed_names if isinstance(n, str)}
    t["validation_names_files_as_a_bare_list"] = int(
        isinstance(listed_names, list))
    for key in ("json_parse", "python_compile"):
        entry = val.get(key)
        if isinstance(entry, dict):
            named |= set(entry) if all(isinstance(k, str) for k in entry)                 else set()
            if "file" in entry and isinstance(entry["file"], str):
                named.add(entry["file"])
    with_digest = set()
    for n, r in files.items():
        t["validation_per_file_entries"] += 1
        if isinstance(r, dict) and "sha256" in r:
            t["validation_entries_with_a_digest"] += 1
            with_digest.add(n)
    t["files_absent_from_the_validation_record"] = [n for n in present
                                                    if n not in named]
    t["files_with_no_digest_anywhere"] = [n for n in present
                                          if n not in listed
                                          and n not in with_digest]
    t["validation_pass_flag_key"] = None
    t["validation_all_pass_flag"] = None
    for key in ("all_pass", "overall_pass", "pass"):
        if key in val:
            t["validation_pass_flag_key"] = key
            t["validation_all_pass_flag"] = val[key]
            break
    t["validation_records_no_pass_flag_at_all"] = int(
        t["validation_pass_flag_key"] is None)
    t["validation_top_level_keys"] = sorted(val)
    t["validation_top_level_flags_not_true"] = sum(
        1 for k, v in val.items()
        if isinstance(v, bool) and v is not True)
    t["validation_file_pass_flags_not_true"] = sum(
        1 for r in files.values()
        if isinstance(r, dict) and r.get("pass") is not True)
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    t: dict = {"paper_proved_items": 0, "ledger_proved_items": 0,
               "paper_open_items": 0, "ledger_open_items": 0,
               "paper_no_go_headings": 0, "ledger_no_go_items": 0,
               "ledger_has_an_open_key": False,
               "open_items_absent_from_the_ledger": [],
               "no_go_headings_absent_from_the_ledger": [],
               "heuristic_failed_its_positive_control": 0,
               "heuristic_failed_its_negative_control": 0}
    pr = re.search(r"## 22\.1(.*?)## 22\.2", paper, re.S)
    if pr:
        t["paper_proved_items"] = len(re.findall(r"^\d+\. ", pr.group(1), re.M))
    ob = re.search(r"## 22\.4(.*?)(?:\n---|\Z)", paper, re.S)
    bullets = []
    if ob:
        bullets = [b.strip(" -;.")
                   for b in re.findall(r"^- (.+)$", ob.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    proved_key = None
    for k in ledger:
        low = k.lower()
        if "proved" in low:
            proved_key = k
            t["ledger_proved_items"] = len(ledger[k])
        elif "no_go" in low or "nogo" in low or "sealed" in low:
            t["ledger_no_go_items"] = len(ledger[k])
        elif "open" in low:
            t["ledger_has_an_open_key"] = True
            t["ledger_open_items"] = len(ledger[k])
    blob = json.dumps(ledger).lower()

    def covered(text: str) -> bool:
        words = [w for w in re.findall(r"[a-z_]{4,}", text.lower())
                 if w not in ("which", "these", "there", "their", "about",
                              "that", "with", "from", "this", "than")]
        if not words:
            return True
        return sum(1 for w in words if w[:7] in blob) >= max(1, len(words) // 2)

    t["open_items_absent_from_the_ledger"] = [b for b in bullets
                                              if not covered(b)]
    t["no_go_headings_absent_from_the_ledger"] = [n for n, hd in no_go
                                                  if not covered(hd)]
    first = " ".join(str(x) for x in (ledger.get(proved_key, []) or [""])[:1])
    t["heuristic_failed_its_positive_control"] = int(bool(first)
                                                     and not covered(first))
    t["heuristic_failed_its_negative_control"] = int(
        covered("quokka bandersnatch flimflam zeppelin marzipan"))
    return t


def check_population(segs: list, errors: list) -> dict:
    return {"segments": len(segs),
            "moduli": len(MODS),
            "sources": len({r["x"] for r in segs}),
            "malformed_segments": len(errors),
            "longest_segment": max((r["L"] for r in segs), default=0)}


def check_their_claims(report: dict, res: dict) -> dict:
    bd, eq, pr = res["bounds"], res["equivalence"], res["primitive"]
    tr, te, sy = res["trichotomy"], res["telescoping"], res["synthetic"]
    al = res["alignment"]
    same = {
        "affine_correction_bound": bd["segments"],
        "defect_product_barrier": bd["segments"],
        "zero_defect_equivalence": bd["segments"],
        "no_double_deficit": eq["nonzero_defect"],
        "primitive_sync_equation": pr["synchronized"],
        "primitive_crt_window": pr["synchronized"],
        "binary_exclusive_overcharge": tr["binary_exclusive"],
        "ternary_exclusive_overdrain": tr["ternary_exclusive"],
        "random_word_correction_bound": sy["word_trials"],
        "synthetic_double_deficit_product_divisibility": sy["quadrant_trials"],
    }
    other = {
        "compensation_telescoping": ("telescoping.partitions",
                                     te["partitions"]),
    }
    rows, exact, covered = [], 0, 0
    for k, v in report.get("checks", {}).items():
        if k in same:
            rows.append({"check": k, "theirs": v, "mine": same[k],
                         "basis": "same population"})
            exact += int(same[k] == v)
        elif k in other:
            nm, cnt = other[k]
            rows.append({"check": k, "theirs": v, "mine": cnt, "basis": nm})
            covered += 1
            exact += int(cnt == v)
        else:
            rows.append({"check": k, "theirs": v, "mine": None,
                         "basis": "not covered"})
    seg_field = report.get("actual_quotient_active_segments")
    rows.append({"check": "actual_quotient_active_segments",
                 "theirs": seg_field, "mine": res["population"]["segments"],
                 "basis": "same population"})
    exact += int(seg_field == res["population"]["segments"])
    rows.append({"check": "(Theorems 7.1/7.2 -- no counter of their own)",
                 "theirs": None,
                 "mine": al["binary_alignment_population"],
                 "basis": "alignment.binary_alignment_population"})
    return {"rows": rows,
            "checks_not_covered_at_all": sum(1 for r in rows
                                             if r["basis"] == "not covered"),
            "checks_covered_by_a_different_population": covered,
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "counts_i_reproduce_exactly": exact}


SECTIONS = ("instrument", "constants", "population", "bounds", "equivalence",
            "alignment", "primitive", "trichotomy", "telescoping",
            "synthetic", "examples", "artifacts", "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("population", "malformed_segments"),
    ("bounds", "affine_lower_bound_violations"),
    ("bounds", "affine_upper_bound_violations"),
    ("bounds", "affine_loose_upper_bound_violations"),
    ("bounds", "barrier_violations"),
    ("bounds", "sharpened_barrier_violations"),
    ("equivalence", "equivalence_violations"),
    ("equivalence", "zero_defect_with_nonzero_compensation"),
    ("equivalence", "zero_compensation_with_nonzero_defect"),
    ("equivalence", "double_deficit_violations"),
    ("alignment", "binary_valuation_violations"),
    ("alignment", "binary_congruence_violations"),
    ("alignment", "ternary_valuation_violations"),
    ("alignment", "ternary_congruence_violations"),
    ("alignment", "defect_zero_while_a_depth_is_positive"),
    ("primitive", "u_not_coprime_to_six"),
    ("primitive", "omega_not_coprime_to_six"),
    ("primitive", "cylinder_equation_violations"),
    ("primitive", "binary_residue_violations"),
    ("primitive", "ternary_residue_violations"),
    ("primitive", "crt_window_violations"),
    ("primitive", "sharpened_window_violations"),
    ("trichotomy", "ternary_overdrain_violations"),
    ("trichotomy", "binary_overdrain_violations"),
    ("trichotomy", "trichotomy_classes_unaccounted"),
    ("trichotomy", "c3_nonpositive_disagreeing_with_B_prime_bound"),
    ("trichotomy", "c2_nonpositive_disagreeing_with_A_bound"),
    ("telescoping", "binary_telescoping_violations"),
    ("telescoping", "ternary_telescoping_violations"),
    ("telescoping", "zero_block_with_nonzero_compensation"),
    ("synthetic", "word_lower_bound_violations"),
    ("synthetic", "word_upper_bound_violations"),
    ("synthetic", "word_valuation_below_length"),
    ("synthetic", "quadrant_divisibility_violations"),
    ("synthetic", "quadrant_size_violations"),
    ("examples", "depth_fields_disagreeing"),
    ("examples", "quotient_identity_violations"),
    ("examples", "barrier_violations"),
    ("examples", "class_disagreeing_with_the_depths"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_file_pass_flags_not_true"),
    ("artifacts", "validation_top_level_flags_not_true"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("population", "segments"),
    ("population", "sources"),
    ("bounds", "segments"),
    ("bounds", "affine_upper_bound_attained"),
    ("bounds", "sharpened_barrier_attained"),
    ("equivalence", "zero_defect"),
    ("equivalence", "nonzero_defect"),
    ("equivalence", "nonzero_with_both_positive"),
    ("equivalence", "nonzero_with_c2_positive_only"),
    ("equivalence", "nonzero_with_c3_positive_only"),
    ("alignment", "binary_alignment_population"),
    ("alignment", "ternary_alignment_population"),
    ("primitive", "synchronized"),
    ("primitive", "sharpened_window_attained"),
    ("trichotomy", "binary_exclusive"),
    ("trichotomy", "ternary_exclusive"),
    ("trichotomy", "predicate_pairs_compared"),
    ("telescoping", "partitions"),
    ("telescoping", "blocks"),
    ("telescoping", "broken_partitions"),
    ("telescoping", "broken_binary_telescoping_failures"),
    ("synthetic", "word_trials"),
    ("synthetic", "word_upper_bound_attained"),
    ("synthetic", "quadrant_trials"),
    ("synthetic", "free_quadrant_divisibility_failures"),
    ("examples", "synchronized_rows"),
    ("examples", "exclusive_rows"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "frontier_and_report_disagreeing"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("population", "moduli"),
    ("population", "longest_segment"),
    ("bounds", "largest_barrier_numerator"),
    ("bounds", "largest_barrier_denominator"),
    ("equivalence", "segments"),
    ("primitive", "windows_within_a_factor_of_two_of_failing"),
    ("primitive", "largest_window_numerator"),
    ("primitive", "largest_window_denominator"),
    ("trichotomy", "segments"),
    ("telescoping", "broken_ternary_telescoping_failures"),
    ("synthetic", "quadrant_zero_defects"),
    ("synthetic", "free_quadrant_trials"),
    ("synthetic", "free_quadrant_size_failures"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
    ("artifacts", "validation_entries_with_a_digest"),
    ("artifacts", "validation_records_no_pass_flag_at_all"),
    ("artifacts", "validation_names_files_as_a_bare_list"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "ledger_no_go_items"),
    ("their_claims", "checks_not_covered_at_all"),
    ("their_claims", "checks_covered_by_a_different_population"),
    ("their_claims", "checks_they_report_as_zero"),
    ("their_claims", "counts_i_reproduce_exactly"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    raw = population()
    segs = [r for r in raw if "__error__" not in r]
    errs = [r for r in raw if "__error__" in r]

    res: dict = {}
    errors: dict = {"%s_raised" % s: 0 for s in SECTIONS}
    errors["messages"] = []

    def run(name: str, fn):
        try:
            res[name] = fn()
        except Exception as exc:                        # noqa: BLE001
            res[name] = {}
            errors["%s_raised" % name] = 1
            errors["messages"].append("%s: %s: %s"
                                      % (name, type(exc).__name__, exc))

    run("instrument", check_instrument)
    run("constants", lambda: check_constants(frontier, report))
    run("population", lambda: check_population(segs, errs))
    run("bounds", lambda: check_bounds(segs))
    run("equivalence", lambda: check_equivalence(segs))
    run("alignment", lambda: check_alignment(segs))
    run("primitive", lambda: check_primitive(segs))
    run("trichotomy", lambda: check_trichotomy(segs))
    run("telescoping", check_telescoping)
    run("synthetic", check_synthetic)
    run("examples", lambda: check_examples(report))
    run("artifacts", lambda: check_artifacts(bundle))
    run("ledger", lambda: check_ledger(ledger, paper))
    run("their_claims", lambda: check_their_claims(report, res))
    res["errors"] = errors

    failures = []
    for sec, key in FAILURE_COUNTERS:
        v = res.get(sec, {}).get(key, 0)
        if (len(v) if isinstance(v, list) else v):
            failures.append("%s.%s = %s" % (sec, key, v))
    if errors["messages"]:
        failures.append("errors.messages = %s" % errors["messages"][:3])
    vacuous = ["%s.%s" % (s, k) for s, k in NON_VACUITY
               if not res.get(s, {}).get(k)]

    declared = ({(s, k) for s, k in FAILURE_COUNTERS}
                | {(s, k) for s, k in NON_VACUITY}
                | {(s, k) for s, k in OBSERVATIONS})
    unread = []
    for sec, body in res.items():
        if not isinstance(body, dict):
            continue
        for k, v in body.items():
            if isinstance(v, bool) or not isinstance(v, int):
                continue
            if (sec, k) in declared:
                continue
            unread.append("%s.%s" % (sec, k))

    out = {
        "run": "RUN-052", "round": "A-U.2d.24", "bundle": str(bundle),
        "passed": not failures and not vacuous,
        "failures": failures,
        "empty_populations": vacuous,
        "counters_not_in_the_failure_or_population_lists": sorted(unread),
        "results": res,
    }
    text = json.dumps(out, indent=2, ensure_ascii=False, default=str)
    if a.out:
        pathlib.Path(a.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
