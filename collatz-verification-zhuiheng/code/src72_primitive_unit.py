"""RUN-053 — independent recheck of Hard-Zeta round A-U.2d.25.

`Primitive Defect Cylinder / Compensation-Seesaw Discrepancy Rigidity`
(source item 72). 數學戰士「墜衡」.

A-U.2d.24 bounded a general block defect by `|d| < 2^Q 3^L`, which RUN-052
measured as loose by a factor of three. Specialised to ONE edge this round
replaces it with a strip that is sharp at both ends,

    -2^q < d < 3,      and     d > 0  =>  d in {1, 2},

collapses the three compensation types into exact arithmetic gates, and gives
the primitive unit an exact transport law

    u'/u = 2^{-c2} 3^{c3} (1 + d/(3n)).

Four things this gate adds.

**Two float-guarded inequalities are re-derived in exact integers.** Their
checker writes `A + BETA*(B+1) < q + 1e-12` and `A + BETA*Bp < q + 1e-12`;
under `2^{beta m} = 3^m` these are `2^A 3^{B+1} < 2^q` and `2^A 3^{Bp} < 2^q`.
Both routes are computed and any disagreement counted.

**The strip is measured for tightness at BOTH ends.** `d < 3` is attained at
`d = 2`; the lower end is scored as the largest `-d/2^q` seen, which is the
honest way to say how sharp `-2^q < d` is.

**Their window triangle bound is implied edge by edge.** `|c2 - beta c3|` is
`|log2(u'/u) - eps|`, so the inequality is the triangle inequality applied to
Theorem 5.1, term by term -- and their assertion sums the terms first. The
per-term slack is measured here, since a sum of non-negative terms cannot go
negative however it is grouped.

**Every by-construction block gets a control.** Two window telescopings hold
because the edges chain; three synthetic blocks hold because each `assert`
restates the line above it. Each is re-run with exactly that property broken
and the failures counted.

Usage:
    python code/src72_primitive_unit.py --bundle <dir>
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
from fractions import Fraction
from random import Random

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src54_low_source_saturation import widen                       # noqa: E402
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    beta_hi, beta_lo, verdict_with_budget,
)

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d25_Primitive_Defect_Cylinder_"
         "Compensation_Seesaw_Discrepancy_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d25_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d25_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d25_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d25.json"
CHECKSUMS = "CHECKSUMS.sha256"

MODS = (3, 9, 27, 81, 243)
Y_LIMIT = 12000
STEPS = 14
EDGES_PER_ORBIT = 11


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def vp(n: int, p: int) -> int | None:
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


def unit_part(n: int):
    a, b = vp(n, 2), vp(n, 3)
    return a, b, n // ((1 << a) * 3 ** b)


def edge(x: int, z: int, q: int, m: int):
    """One accelerated edge at modulus `m`, with both compensation depths."""
    r, s = x % m, z % m
    n, n2 = (x - r) // m, (z - s) // m
    if n <= 0 or n2 <= 0:
        return None
    num = 1 + 3 * r - (1 << q) * s
    if num % m:
        return "defect not integral"
    d = num // m
    if (1 << q) * n2 != 3 * n + d:
        return "quotient identity failed"
    a, b, u = unit_part(n)
    ap, bp, up = unit_part(n2)
    c2, c3 = q + ap - a, 1 + b - bp
    if d == 0:
        typ = "zero"
    elif c2 > 0 and c3 > 0:
        typ = "sync"
    elif c2 > 0:
        typ = "BE"
    elif c3 > 0:
        typ = "TE"
    else:
        typ = "BAD"
    return {"x": x, "z": z, "q": q, "M": m, "n": n, "np": n2, "d": d,
            "A": a, "B": b, "u": u, "Ap": ap, "Bp": bp, "up": up,
            "c2": c2, "c3": c3, "typ": typ}


def population():
    out, errs = [], []
    for m in MODS:
        for y in range(7, Y_LIMIT, 2):
            if y % 3 == 0:
                continue
            st, qs = orbit(y, STEPS)
            for i, q in enumerate(qs[:EDGES_PER_ORBIT]):
                rec = edge(st[i], st[i + 1], q, m)
                if isinstance(rec, dict):
                    out.append(rec)
                elif isinstance(rec, str):
                    errs.append(rec)
    return out, errs


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
    want("vp of zero is None", vp(0, 2) is None and vp(0, 3) is None)
    want("the accelerated step agrees with the definition", syr(7) == (11, 1))
    want("the unit part strips both primes", unit_part(2 ** 3 * 3 ** 2 * 5)
         == (3, 2, 5))

    # the exact form of the round's two beta-inequalities
    bad = 0
    for a in range(0, 12):
        for b in range(0, 8):
            for q in range(1, 30):
                if (((1 << a) * 3 ** b < (1 << q))
                        != (a + math.log2(3) * b < q)):
                    bad += 1
    want("2^A 3^B < 2^q decides A + beta B < q", bad == 0)

    # the triangle inequality the window bound rests on, by hand
    bad = 0
    for x in (-2.5, -0.5, 0.0, 0.5, 3.25):
        for e in (-1.5, 0.0, 0.75):
            if not abs(x) + abs(e) + 1e-12 >= abs(x - e):
                bad += 1
    want("|x| + |e| >= |x - e|", bad == 0)

    # Theorem 3.1's arithmetic on a hand case: d = 1 + 3r - 2^q s over M
    want("the one-edge defect uses B_P = 1",
         edge(7, 11, 1, 3)["d"] == (1 + 3 * (7 % 3) - 2 * (11 % 3)) // 3)
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
               "frontier_constants_with_no_closed_form_here": [],
               "rows": []}
    lo, hi = widen(*beta_tight(), 40)
    b = math.log2(3)
    items = [
        ("beta", lo, hi, b, 4),
        ("beta_minus_1", lo - 1, hi - 1, b - 1, 8),
        ("two_minus_beta", 2 - hi, 2 - lo, 2 - b, 20),
        ("resonance_threshold_inherited", (lo - 1) / hi, (hi - 1) / lo,
         (b - 1) / b, 12),
    ]
    rc = report.get("constants", {})
    for name, blo, bhi, chain, budget in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        row = {"constant": name, "frontier": repr(pub), "budget": budget}
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
    # a value carried as a short decimal has no bracket to be checked against;
    # say so rather than scoring it against a guess
    known = {n for n, *_ in items}
    t["frontier_constants_with_no_closed_form_here"] = sorted(
        k for k, v in frontier.items()
        if isinstance(v, float) and k not in known)
    for k in t["frontier_constants_with_no_closed_form_here"]:
        if k in rc and rc[k] != frontier[k]:
            t["frontier_and_report_disagreeing"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 3.1 -- the sharp one-step strip
# ---------------------------------------------------------------------------

def check_strip(edges: list) -> dict:
    t: dict = {"edges": 0,
               "strip_upper_violations": 0,
               "strip_lower_violations": 0,
               "positive_defect_not_one_or_two": 0,
               "positive_defects": 0,
               "negative_defects": 0,
               "zero_defects": 0,
               "upper_end_attained": 0,
               "largest_lower_ratio_numerator": 0,
               "largest_lower_ratio_denominator": 1,
               "block_bound_from_the_previous_round_violations": 0}
    bn, bd = 0, 1
    for r in edges:
        t["edges"] += 1
        d, q = r["d"], r["q"]
        if not d < 3:
            t["strip_upper_violations"] += 1
        if not -(1 << q) < d:
            t["strip_lower_violations"] += 1
        if d == 2:
            t["upper_end_attained"] += 1
        if d > 0:
            t["positive_defects"] += 1
            if d not in (1, 2):
                t["positive_defect_not_one_or_two"] += 1
        elif d < 0:
            t["negative_defects"] += 1
            if -d * bd > bn * (1 << q):
                bn, bd = -d, (1 << q)
        else:
            t["zero_defects"] += 1
        # the previous round's block bound, specialised to one edge
        if not abs(d) < (1 << q) * 3:
            t["block_bound_from_the_previous_round_violations"] += 1
    t["largest_lower_ratio_numerator"] = bn
    t["largest_lower_ratio_denominator"] = bd
    return t


# ---------------------------------------------------------------------------
# Theorems 4.1, 4.2, 4.3 -- the compensation gates
# ---------------------------------------------------------------------------

def check_gates(edges: list) -> dict:
    t: dict = {"zero": 0, "sync": 0, "binary_exclusive": 0,
               "ternary_exclusive": 0, "unclassified": 0,
               "zero_defect_unit_not_invariant": 0,
               "zero_defect_depths_not_zero": 0,
               "te_defect_not_two": 0, "te_valuation_not_one": 0,
               "te_output_not_coprime": 0, "te_depths_wrong": 0,
               "te_unit_formula_violations": 0, "te_unit_not_increasing": 0,
               "be_defect_not_negative": 0, "be_valuation_below_two": 0,
               "be_ternary_not_deeper": 0, "be_defect_valuation_wrong": 0,
               "be_xi_not_odd_positive": 0, "be_unit_formula_violations": 0,
               "be_unit_not_decreasing": 0,
               "be_reservoir_bound_violations": 0,
               "sync_defect_valuations_wrong": 0,
               "sync_omega_not_coprime": 0,
               "sync_cylinder_violations": 0,
               "sync_positive_normal_form_violations": 0,
               "sync_negative_omega_not_negative": 0,
               "sync_negative_reservoir_violations": 0,
               "float_reservoir_route_disagreeing": 0,
               "reservoir_tests": 0,
               "sync_positive": 0, "sync_negative": 0}
    bf = math.log2(3)
    for r in edges:
        typ, d, q = r["typ"], r["d"], r["q"]
        a, b, u = r["A"], r["B"], r["u"]
        ap, bp, up = r["Ap"], r["Bp"], r["up"]
        c2, c3 = r["c2"], r["c3"]
        if typ == "BAD":
            t["unclassified"] += 1
            continue
        if typ == "zero":
            t["zero"] += 1
            if up != u:
                t["zero_defect_unit_not_invariant"] += 1
            if not (c2 == 0 and c3 == 0):
                t["zero_defect_depths_not_zero"] += 1
        elif typ == "TE":
            t["ternary_exclusive"] += 1
            if d != 2:
                t["te_defect_not_two"] += 1
            if q != 1:
                t["te_valuation_not_one"] += 1
            if not (ap == 0 and bp == 0):
                t["te_depths_wrong"] += 1
            if a < 1 or c2 != 1 - a or c3 != 1 + b:
                t["te_depths_wrong"] += 1
            if math.gcd(up, 6) != 1:
                t["te_output_not_coprime"] += 1
            if up != (1 << (a - 1)) * 3 ** (b + 1) * u + 1 if a >= 1 else True:
                t["te_unit_formula_violations"] += 1
            if not up > u:
                t["te_unit_not_increasing"] += 1
        elif typ == "BE":
            t["binary_exclusive"] += 1
            if not d < 0:
                t["be_defect_not_negative"] += 1
            if q < 2:
                t["be_valuation_below_two"] += 1
            if bp < b + 1:
                t["be_ternary_not_deeper"] += 1
            if d != 0 and vp(d, 2) != a:
                t["be_defect_valuation_wrong"] += 1
            den = (1 << a) * 3 ** (b + 1)
            if (-d) % den:
                t["be_unit_formula_violations"] += 1
            else:
                xi = (-d) // den
                if xi < 1 or xi % 2 == 0:
                    t["be_xi_not_odd_positive"] += 1
                if c3 <= 0 and u != xi + (1 << c2) * 3 ** (-c3) * up:
                    t["be_unit_formula_violations"] += 1
            if not u > up:
                t["be_unit_not_decreasing"] += 1
            # A + beta(B+1) < q  <->  2^A 3^{B+1} < 2^q
            t["reservoir_tests"] += 1
            exact = (1 << a) * 3 ** (b + 1) < (1 << q)
            if not exact:
                t["be_reservoir_bound_violations"] += 1
            if exact != (a + bf * (b + 1) < q + 1e-12):
                t["float_reservoir_route_disagreeing"] += 1
        else:
            t["sync"] += 1
            if d == 0 or vp(d, 2) != a or vp(d, 3) != bp:
                t["sync_defect_valuations_wrong"] += 1
                continue
            om = d // ((1 << a) * 3 ** bp)
            if math.gcd(abs(om), 6) != 1:
                t["sync_omega_not_coprime"] += 1
            if (1 << c2) * up != 3 ** c3 * u + om:
                t["sync_cylinder_violations"] += 1
            if d > 0:
                t["sync_positive"] += 1
                if not (d in (1, 2) and bp == 0 and om == 1
                        and a == (0 if d == 1 else 1)):
                    t["sync_positive_normal_form_violations"] += 1
            else:
                t["sync_negative"] += 1
                if not om < 0:
                    t["sync_negative_omega_not_negative"] += 1
                t["reservoir_tests"] += 1
                exact = (1 << a) * 3 ** bp < (1 << q)
                if not exact:
                    t["sync_negative_reservoir_violations"] += 1
                if exact != (a + bf * bp < q + 1e-12):
                    t["float_reservoir_route_disagreeing"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 5.1 and its corollaries -- exact, in rationals
# ---------------------------------------------------------------------------

def check_transport(edges: list) -> dict:
    t: dict = {"edges": 0,
               "transport_violations": 0,
               "zero_defect_transport_not_trivial": 0,
               "exclusive_seesaw_violations": 0,
               "seesaw_population": 0}
    for r in edges:
        t["edges"] += 1
        d, n, u, up = r["d"], r["n"], r["u"], r["up"]
        c2, c3 = r["c2"], r["c3"]
        lhs = Fraction(up, u)
        rhs = (Fraction(3 ** c3) if c3 >= 0 else Fraction(1, 3 ** -c3))
        rhs /= (Fraction(1 << c2) if c2 >= 0 else Fraction(1, 1 << -c2))
        rhs *= Fraction(3 * n + d, 3 * n)
        if lhs != rhs:
            t["transport_violations"] += 1
        if d == 0 and lhs != 1:
            t["zero_defect_transport_not_trivial"] += 1
        # Corollary 5.3: an exclusive edge moves the unit one way only
        if r["typ"] in ("TE", "BE"):
            t["seesaw_population"] += 1
            if r["typ"] == "TE" and not up > u:
                t["exclusive_seesaw_violations"] += 1
            if r["typ"] == "BE" and not u > up:
                t["exclusive_seesaw_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 6.1 and 8.1 -- the window products, with the chain broken
# ---------------------------------------------------------------------------

def check_windows(trials: int = 6000, seed: int = 26081525) -> dict:
    t: dict = {"windows": 0, "edges_in_windows": 0,
               "correction_product_violations": 0,
               "unit_window_transport_violations": 0,
               "triangle_bound_violations": 0,
               "triangle_terms": 0,
               "triangle_terms_with_negative_slack": 0,
               "broken_windows": 0,
               "broken_correction_product_failures": 0,
               "broken_unit_transport_failures": 0}
    bf = math.log2(3)
    rng = Random(seed)
    for _ in range(trials):
        m = rng.choice(MODS)
        y = rng.randrange(7, Y_LIMIT, 2)
        if y % 3 == 0:
            continue
        st, qs = orbit(y, STEPS)
        a = rng.randint(0, 6)
        b = rng.randint(a + 2, 13)
        rows = [edge(st[i], st[i + 1], qs[i], m) for i in range(a, b)]
        if any(not isinstance(x, dict) for x in rows):
            continue
        t["windows"] += 1
        t["edges_in_windows"] += len(rows)
        n0, n1 = rows[0]["n"], rows[-1]["np"]
        q = sum(x["q"] for x in rows)
        ell = len(rows)
        prod = Fraction(1)
        for x in rows:
            prod *= Fraction(3 * x["n"] + x["d"], 3 * x["n"])
        if Fraction(n1, n0) != Fraction(3 ** ell, 1 << q) * prod:
            t["correction_product_violations"] += 1
        uprod = Fraction(1)
        for x in rows:
            step = (Fraction(3 ** x["c3"]) if x["c3"] >= 0
                    else Fraction(1, 3 ** -x["c3"]))
            step /= (Fraction(1 << x["c2"]) if x["c2"] >= 0
                     else Fraction(1, 1 << -x["c2"]))
            uprod *= step * Fraction(3 * x["n"] + x["d"], 3 * x["n"])
        if Fraction(rows[-1]["up"], rows[0]["u"]) != uprod:
            t["unit_window_transport_violations"] += 1
        # their triangle bound sums first; it is implied TERM BY TERM
        du = ie = imb = 0.0
        for x in rows:
            t["triangle_terms"] += 1
            e = math.log2(1 + x["d"] / (3 * x["n"]))
            one_du = abs(math.log2(x["up"] / x["u"]))
            one_imb = abs(x["c2"] - bf * x["c3"])
            if one_du + abs(e) + 1e-12 < one_imb:
                t["triangle_terms_with_negative_slack"] += 1
            du += one_du
            ie += abs(e)
            imb += one_imb
        if not du + ie + 1e-10 >= imb:
            t["triangle_bound_violations"] += 1
        # the control: drop the middle edge so the window no longer chains
        if len(rows) < 3:
            continue
        cut = rows[:1] + rows[2:]
        t["broken_windows"] += 1
        q2 = sum(x["q"] for x in cut)
        l2 = len(cut)
        p2 = Fraction(1)
        for x in cut:
            p2 *= Fraction(3 * x["n"] + x["d"], 3 * x["n"])
        if Fraction(cut[-1]["np"], cut[0]["n"]) != Fraction(3 ** l2,
                                                            1 << q2) * p2:
            t["broken_correction_product_failures"] += 1
        u2 = Fraction(1)
        for x in cut:
            step = (Fraction(3 ** x["c3"]) if x["c3"] >= 0
                    else Fraction(1, 3 ** -x["c3"]))
            step /= (Fraction(1 << x["c2"]) if x["c2"] >= 0
                     else Fraction(1, 1 << -x["c2"]))
            u2 *= step * Fraction(3 * x["n"] + x["d"], 3 * x["n"])
        if Fraction(cut[-1]["up"], cut[0]["u"]) != u2:
            t["broken_unit_transport_failures"] += 1
    return t


# ---------------------------------------------------------------------------
# their three synthetic blocks, each with its construction broken
# ---------------------------------------------------------------------------

def check_synthetic(trials: int = 20000, seed: int = 26081525) -> dict:
    t: dict = {"sync_attempts": 0, "sync_constructions": 0,
               "sync_equation_violations": 0,
               "sync_equation_violations_when_the_divisibility_is_dropped": 0,
               "te_trials": 0, "te_not_increasing": 0,
               "te_not_increasing_when_the_offset_is_removed": 0,
               "be_trials": 0, "be_not_decreasing": 0,
               "be_not_decreasing_when_the_pump_is_removed": 0}
    rng = Random(seed)
    for _ in range(30000):
        t["sync_attempts"] += 1
        c2 = rng.randint(1, 18)
        c3 = rng.randint(1, 14)
        u = rng.randrange(1, 500, 2)
        while u % 3 == 0:
            u += 2
        om = rng.choice((-1, 1))
        num = 3 ** c3 * u + om
        if num > 0 and num % (1 << c2) == 0:
            up = num // (1 << c2)
            if math.gcd(up, 6) == 1:
                t["sync_constructions"] += 1
                if (1 << c2) * up != 3 ** c3 * u + om:
                    t["sync_equation_violations"] += 1
        # the control: take the quotient WITHOUT requiring divisibility
        up2 = num // (1 << c2)
        if num > 0 and (1 << c2) * up2 != num:
            t["sync_equation_violations_when_the_divisibility_is_dropped"] += 1

    rng = Random(seed + 1)
    for _ in range(trials):
        t["te_trials"] += 1
        a = rng.randint(1, 12)
        b = rng.randint(0, 8)
        u = rng.randrange(1, 300, 2)
        while u % 3 == 0:
            u += 2
        up = (1 << (a - 1)) * 3 ** (b + 1) * u + 1
        if not up > u:
            t["te_not_increasing"] += 1
        # the control: the `+1` and the multiplier are what force the increase
        if not (0 * u + 1) > u:
            t["te_not_increasing_when_the_offset_is_removed"] += 1

        t["be_trials"] += 1
        c2b = rng.randint(1, 10)
        g = rng.randint(0, 6)
        upb = rng.randrange(1, 200, 2)
        while upb % 3 == 0:
            upb += 2
        xi = rng.randrange(1, 100, 2)
        ub = xi + (1 << c2b) * 3 ** g * upb
        if not ub > upb:
            t["be_not_decreasing"] += 1
        if not xi > upb:
            t["be_not_decreasing_when_the_pump_is_removed"] += 1
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"rows": 0, "groups": 0,
               "quotient_identity_violations": 0,
               "depth_fields_disagreeing": 0,
               "unit_fields_disagreeing": 0,
               "strip_violations": 0,
               "class_disagreeing_with_the_defect_sign": 0}
    for key, rows in (report.get("examples", {}) or {}).items():
        t["groups"] += 1
        for ex in rows:
            t["rows"] += 1
            q, d, n, n2 = ex["q"], ex["d"], ex["n"], ex["np"]
            if (1 << q) * n2 != 3 * n + d:
                t["quotient_identity_violations"] += 1
            if q + ex["Ap"] - ex["A"] != ex["c2"] or \
                    1 + ex["B"] - ex["Bp"] != ex["c3"]:
                t["depth_fields_disagreeing"] += 1
            if (n // ((1 << ex["A"]) * 3 ** ex["B"]) != ex["u"]
                    or n2 // ((1 << ex["Ap"]) * 3 ** ex["Bp"]) != ex["up"]):
                t["unit_fields_disagreeing"] += 1
            if not -(1 << q) < d < 3:
                t["strip_violations"] += 1
            tag = key.rsplit("_", 1)[-1]
            sign = "pos" if d > 0 else "neg" if d < 0 else "zero"
            if tag != sign:
                t["class_disagreeing_with_the_defect_sign"] += 1
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
    files = val.get("files")
    files = files if isinstance(files, dict) else {}
    named = set(files)
    lst = val.get("files_checked")
    if isinstance(lst, list):
        named |= {n for n in lst if isinstance(n, str)}
    t["validation_names_files_as_a_bare_list"] = int(isinstance(lst, list))
    for key in ("json_parse", "python_compile"):
        entry = val.get(key)
        if isinstance(entry, dict):
            if all(isinstance(k, str) for k in entry):
                named |= set(entry)
            if isinstance(entry.get("file"), str):
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
    # `status: "PASS"` is a string, not a boolean; a reader that only looks for
    # boolean flags reports None and a real "FAIL" would vanish with it
    for key in ("all_pass", "overall_pass", "pass", "status"):
        if key in val:
            t["validation_pass_flag_key"] = key
            t["validation_all_pass_flag"] = val[key]
            break
    t["validation_pass_flag_is_a_string"] = int(
        isinstance(t["validation_all_pass_flag"], str))
    t["validation_pass_flag_not_passing"] = int(
        t["validation_all_pass_flag"] not in (True, "PASS", "pass", None))
    probs = val.get("problems")
    t["validation_problems_listed"] = len(probs) if isinstance(probs,
                                                               list) else 0
    t["validation_names_no_files_at_all"] = int(
        not isinstance(files, dict) or not files) and int(
        not isinstance(lst, list))
    t["validation_records_no_pass_flag_at_all"] = int(
        t["validation_pass_flag_key"] is None)
    t["validation_top_level_keys"] = sorted(val)
    t["validation_top_level_flags_not_true"] = sum(
        1 for k, v in val.items() if isinstance(v, bool) and v is not True)
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
               "ledger_has_no_no_go_key": 0,
               "heuristic_failed_its_positive_control": 0,
               "heuristic_failed_its_negative_control": 0}
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    # `.` matches newlines under re.S, so a greedy `.*` on the heading line
    # runs to the end of the document and backtracks to the wrong `$`
    m = re.search(r"^#+ [^\n]*Proved internally[^\n]*$(.*?)^#+ ",
                  paper, re.M | re.S)
    if m:
        t["paper_proved_items"] = len(re.findall(r"^\d+\. ", m.group(1), re.M))
    m = re.search(r"^#+ [^\n]*Explicitly open[^\n]*$(.*?)(?:^#+ |\Z)",
                  paper, re.M | re.S)
    bullets = []
    if m:
        bullets = [b.strip(" -;.")
                   for b in re.findall(r"^- (.+)$", m.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
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
    t["ledger_has_no_no_go_key"] = int(
        not any(("no_go" in k.lower() or "nogo" in k.lower()
                 or "sealed" in k.lower()) for k in ledger))
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


def check_population(edges: list, errs: list) -> dict:
    return {"edges": len(edges), "moduli": len(MODS),
            "sources": len({r["x"] for r in edges}),
            "malformed_edges": len(errs)}


def check_their_claims(report: dict, res: dict) -> dict:
    st, ga, tp = res["strip"], res["gates"], res["transport"]
    wi, sy = res["windows"], res["synthetic"]
    same = {
        "sharp_one_step_defect_strip": st["edges"],
        "primitive_unit_transport_exact": tp["edges"],
        "zero_defect_unit_invariance": ga["zero"],
        "positive_defect_is_1_or_2": st["positive_defects"],
        "synchronized_primitive_gate": ga["sync"],
        "positive_sync_unit_defect": ga["sync_positive"],
        "negative_sync_low_reservoir": ga["sync_negative"],
        "binary_exclusive_negative_pump": ga["binary_exclusive"],
        "ternary_exclusive_atomic_reset": ga["ternary_exclusive"],
        "exclusive_unit_monotonicity": tp["seesaw_population"],
        "synthetic_TE_unit_reset": sy["te_trials"],
        "synthetic_BE_unit_pump": sy["be_trials"],
    }
    other = {
        "synthetic_primitive_sync_equations": ("synthetic.sync_constructions",
                                               sy["sync_constructions"]),
        "quotient_correction_product_exact": ("windows.windows",
                                              wi["windows"]),
        "primitive_unit_window_transport_exact": ("windows.windows",
                                                  wi["windows"]),
        "unit_variation_triangle_bound": ("windows.windows", wi["windows"]),
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
    for field, mine in (("actual_quotient_active_edges",
                         res["population"]["edges"]),):
        rows.append({"check": field, "theirs": report.get(field),
                     "mine": mine, "basis": "same population"})
        exact += int(report.get(field) == mine)
    return {"rows": rows,
            "checks_not_covered_at_all": sum(1 for r in rows
                                             if r["basis"] == "not covered"),
            "checks_covered_by_a_different_population": covered,
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "counts_i_reproduce_exactly": exact}


SECTIONS = ("instrument", "constants", "population", "strip", "gates",
            "transport", "windows", "synthetic", "examples", "artifacts",
            "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("population", "malformed_edges"),
    ("strip", "strip_upper_violations"),
    ("strip", "strip_lower_violations"),
    ("strip", "positive_defect_not_one_or_two"),
    ("strip", "block_bound_from_the_previous_round_violations"),
    ("gates", "unclassified"),
    ("gates", "zero_defect_unit_not_invariant"),
    ("gates", "zero_defect_depths_not_zero"),
    ("gates", "te_defect_not_two"),
    ("gates", "te_valuation_not_one"),
    ("gates", "te_output_not_coprime"),
    ("gates", "te_depths_wrong"),
    ("gates", "te_unit_formula_violations"),
    ("gates", "te_unit_not_increasing"),
    ("gates", "be_defect_not_negative"),
    ("gates", "be_valuation_below_two"),
    ("gates", "be_ternary_not_deeper"),
    ("gates", "be_defect_valuation_wrong"),
    ("gates", "be_xi_not_odd_positive"),
    ("gates", "be_unit_formula_violations"),
    ("gates", "be_unit_not_decreasing"),
    ("gates", "be_reservoir_bound_violations"),
    ("gates", "sync_defect_valuations_wrong"),
    ("gates", "sync_omega_not_coprime"),
    ("gates", "sync_cylinder_violations"),
    ("gates", "sync_positive_normal_form_violations"),
    ("gates", "sync_negative_omega_not_negative"),
    ("gates", "sync_negative_reservoir_violations"),
    ("gates", "float_reservoir_route_disagreeing"),
    ("transport", "transport_violations"),
    ("transport", "zero_defect_transport_not_trivial"),
    ("transport", "exclusive_seesaw_violations"),
    ("windows", "correction_product_violations"),
    ("windows", "unit_window_transport_violations"),
    ("windows", "triangle_bound_violations"),
    ("windows", "triangle_terms_with_negative_slack"),
    ("synthetic", "sync_equation_violations"),
    ("synthetic", "te_not_increasing"),
    ("synthetic", "be_not_decreasing"),
    ("examples", "quotient_identity_violations"),
    ("examples", "depth_fields_disagreeing"),
    ("examples", "unit_fields_disagreeing"),
    ("examples", "strip_violations"),
    ("examples", "class_disagreeing_with_the_defect_sign"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_file_pass_flags_not_true"),
    ("artifacts", "validation_top_level_flags_not_true"),
    ("artifacts", "validation_pass_flag_not_passing"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("population", "edges"),
    ("population", "sources"),
    ("strip", "edges"),
    ("strip", "positive_defects"),
    ("strip", "negative_defects"),
    ("strip", "zero_defects"),
    ("strip", "upper_end_attained"),
    ("gates", "zero"),
    ("gates", "sync"),
    ("gates", "binary_exclusive"),
    ("gates", "ternary_exclusive"),
    ("gates", "sync_positive"),
    ("gates", "sync_negative"),
    ("gates", "reservoir_tests"),
    ("transport", "edges"),
    ("transport", "seesaw_population"),
    ("windows", "windows"),
    ("windows", "edges_in_windows"),
    ("windows", "triangle_terms"),
    ("windows", "broken_windows"),
    ("windows", "broken_correction_product_failures"),
    ("windows", "broken_unit_transport_failures"),
    ("synthetic", "sync_attempts"),
    ("synthetic", "sync_constructions"),
    ("synthetic",
     "sync_equation_violations_when_the_divisibility_is_dropped"),
    ("synthetic", "te_trials"),
    ("synthetic", "te_not_increasing_when_the_offset_is_removed"),
    ("synthetic", "be_trials"),
    ("synthetic", "be_not_decreasing_when_the_pump_is_removed"),
    ("examples", "rows"),
    ("examples", "groups"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "frontier_and_report_disagreeing"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("population", "moduli"),
    ("strip", "largest_lower_ratio_numerator"),
    ("strip", "largest_lower_ratio_denominator"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
    ("artifacts", "validation_entries_with_a_digest"),
    ("artifacts", "validation_records_no_pass_flag_at_all"),
    ("artifacts", "validation_names_files_as_a_bare_list"),
    ("artifacts", "validation_names_no_files_at_all"),
    ("artifacts", "validation_pass_flag_is_a_string"),
    ("artifacts", "validation_problems_listed"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "ledger_no_go_items"),
    ("ledger", "ledger_has_no_no_go_key"),
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

    edges, errs = population()

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
    run("population", lambda: check_population(edges, errs))
    run("strip", lambda: check_strip(edges))
    run("gates", lambda: check_gates(edges))
    run("transport", lambda: check_transport(edges))
    run("windows", check_windows)
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
        "run": "RUN-053", "round": "A-U.2d.25", "bundle": str(bundle),
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
