"""RUN-051 — independent recheck of Hard-Zeta round A-U.2d.23.

`Quotient-State Resonance and Defect-Carry Rigidity` (source item 70).
數學戰士「墜衡」.

A-U.2d.22 left the quotient trajectory `n` as the hidden object. This round
prices the most dangerous low-defect mechanism: a contiguous return with zero
defect. Because the accelerated states are odd and `M = 3^k` is odd, such a
return is more rigid than the previous round said --

    n = 2^{Q+1} v,   n' = 2 * 3^L v,   v >= 1

with an exact cross-adic transfer `nu2(n') = nu2(n) - Q`,
`nu3(n') = nu3(n) + L`: the return spends binary divisibility to buy ternary
divisibility, at a fixed rate.

Four things this gate adds.

**The round states four inequalities with `beta` in them and evaluates every one
in float64.** All four are exact in integers under `2^{beta m} = 3^m`:

    Q > beta L                     <->  2^Q > 3^L
    m_in > Q + log2(M/Z0)          <->  2^{m_in} Z0 > 2^Q M
    cap < (beta-1) p + 1           <->  2^{cap + p} < 2 * 3^p
    L < ((beta-1)p - log2(M/Z0) + 1)/beta
                                   <->  3^L M 2^p < 2 * 3^p Z0

Both routes are computed and any disagreement is counted.

**Theorem 7.1's uniqueness half is decided for every `q`, not scanned.** A
length-one zero-defect return needs `1 = (2^q - 3) r` with `r >= 1`, so
`2^q - 3` divides 1 and `q = 2, r = 1` is forced. The bundle scans `q < 20`,
`r < 100` instead, and that loop carries no counter.

**Theorem 15.1's converse and Theorem 16.1's `only if` half are counted.** The
bundle tests the forward direction of each and leaves the other half either
uncounted or unstated.

**Their three synthetic blocks are measured rather than trusted.** Two of the
accounting assertions are identities by construction -- they survive inputs
that violate the property the block is about -- and the reservoir block's two
counters both increment outside a guard that opens on part of the samples.

Usage:
    python code/src70_quotient_resonance.py --bundle <dir> [--limit N]
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
from math import ceil
from random import Random

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src54_low_source_saturation import widen                       # noqa: E402
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    b_of, beta_hi, beta_lo, verdict_with_budget,
)
from src65_lift_cocycle import (                                    # noqa: E402
    ceil_beta, lift_profile, local_bridges,
)

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d23_Quotient_State_Resonance_and_"
         "Defect_Carry_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d23_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d23_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d23_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d23.json"
CHECKSUMS = "CHECKSUMS.sha256"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def v2(n: int) -> int | None:
    """`v_2(n)`, or None for zero. Their checker returns 10**9 for zero, which
    is a real number that participates in comparisons; None cannot."""
    if n == 0:
        return None
    n, a = abs(n), 0
    while n % 2 == 0:
        n //= 2
        a += 1
    return a


def v3(n: int) -> int | None:
    if n == 0:
        return None
    n, a = abs(n), 0
    while n % 3 == 0:
        n //= 3
        a += 1
    return a


def syr_step(n: int) -> tuple[int, int]:
    m = 3 * n + 1
    q = 0
    while m % 2 == 0:
        m //= 2
        q += 1
    return m, q


def path_defect(word, r: int, s: int, m: int) -> int | None:
    ell, q = len(word), sum(word)
    num = b_of(word) + 3 ** ell * r - (1 << q) * s
    return num // m if num % m == 0 else None


def mechanical_cap(ell: int, h: int) -> int:
    """`ceil(beta h) - ceil(beta ell) - (h - ell)`, exactly."""
    return ceil_beta(h) - ceil_beta(ell) - (h - ell)


def zero_lift(limit: int, max_steps: int):
    out = []
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        ms = lift_profile(w)
        if not w or ms[len(w)] != 0:
            continue
        out.append((y, X, Z, list(vals[1:]), w, ms))
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
    want("v2 and v3 of zero are None, not a large number",
         v2(0) is None and v3(0) is None)

    bad = 0
    for a in range(0, 9):
        if v2(2 ** a * 7) != a or v3(3 ** a * 7) != a:
            bad += 1
    want("v2 and v3 are exact", bad == 0)

    # the four exact reformulations, each against its float route on cases
    # chosen so both routes are unambiguous
    bad = 0
    for ell in range(1, 60):
        for q in (ell, ell + 1, 2 * ell):
            if ((1 << q) > 3 ** ell) != (q > math.log2(3) * ell):
                bad += 1
    want("2^Q > 3^L decides Q > beta L", bad == 0)

    bad = 0
    for p in range(1, 40):
        for cap in (0, 1, p // 2, p):
            exact = (1 << (cap + p)) < 2 * 3 ** p
            flt = cap < (math.log2(3) - 1) * p + 1
            if exact != flt:
                bad += 1
    want("2^{cap+p} < 2*3^p decides cap < (beta-1)p + 1", bad == 0)

    # the accelerated step, and Theorem 7.1's atomic transition by hand
    want("syr_step agrees with the definition", syr_step(7) == (11, 1))
    bad = 0
    for k in range(1, 5):
        for v in (1, 2, 5):
            m = 3 ** k
            z, q = syr_step(1 + 8 * m * v)
            if q != 2 or z != 1 + 6 * m * v:
                bad += 1
    want("x = 1 + 8Mv steps to 1 + 6Mv with q = 2", bad == 0)

    want("the length-one zero-defect equation is 1 = (2^q - 3) r",
         b_of((2,)) + 3 * 1 - (1 << 2) * 1 == 0)

    # ceil_beta against a slow reference
    bad = sum(1 for n in range(1, 200)
              if ceil_beta(n) != -((-(3 ** n).bit_length()) // 1)
              and ceil_beta(n) != (3 ** n).bit_length())
    want("ceil_beta is the bit length of 3^n", bad == 0)
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
               "frontier_constants_sharing_a_value": [],
               "rows": []}
    lo, hi = widen(*beta_tight(), 40)
    b = math.log2(3)
    items = [
        ("beta", lo, hi, b, 4),
        ("beta_minus_1", lo - 1, hi - 1, b - 1, 8),
        ("resonance_mass_threshold", (lo - 1) / hi, (hi - 1) / lo,
         (b - 1) / b, 12),
        ("faithful_core_mass", 2 - hi, 2 - lo, 2 - b, 20),
        ("faithful_minus_resonance_threshold",
         (2 - hi) - (hi - 1) / lo, (2 - lo) - (lo - 1) / hi,
         (2 - b) - (b - 1) / b, 40),
        ("binary_replenishment_at_faithful_benchmark",
         lo * (2 - hi) - (hi - 1), hi * (2 - lo) - (lo - 1),
         b * (2 - b) - (b - 1), 40),
        ("temporal_delay_L_coefficient", lo / (hi - 1), hi / (lo - 1),
         b / (b - 1), 12),
        ("inverse_beta_minus_1", 1 / (hi - 1), 1 / (lo - 1), 1 / (b - 1), 12),
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
        verdict, d = verdict_with_budget(pub, blo, bhi, chain, budget)
        if verdict == "undecided":
            t["undecided_brackets"] += 1
        elif verdict == "exact":
            t["exact_to_the_last_bit"] += 1
        elif verdict == "the float64 chain":
            t["from_the_float64_chain_not_the_nearest_double"] += 1
        else:
            t["disagreeing_with_both_evaluations"] += 1
        row["verdict"] = verdict if d == 0 else "%+d ulp, %s" % (d, verdict)
        t["rows"].append(row)

    # a frontier value with no generator in the checker is hand-typed, and a
    # per-file check cannot see it -- only the two artifacts side by side can
    numeric = {k: v for k, v in frontier.items() if isinstance(v, float)}
    t["frontier_constants_the_checker_never_computes"] = sorted(
        k for k in numeric if k not in rc)
    seen: dict = {}
    for k, v in sorted(numeric.items()):
        seen.setdefault(v, []).append(k)
    t["frontier_constants_sharing_a_value"] = [sorted(v) for v in seen.values()
                                               if len(v) > 1]
    return t


# ---------------------------------------------------------------------------
# Theorems 3.1, 4.1 -- the parity-refined resonance and its transfer
# ---------------------------------------------------------------------------

def check_resonance(bridges: list, depth: int = 5, window: int = 12) -> dict:
    t: dict = {"bridges": 0, "windows": 0, "returns": 0,
               "zero_defect_returns": 0,
               "defect_not_integral": 0,
               "quotient_affine_violations": 0,
               "zero_defect_not_supercritical": 0,
               "float_supercritical_route_disagreeing": 0,
               "quotient_not_positive": 0,
               "parity_refinement_violations": 0,
               "u_odd_so_the_previous_rounds_form_was_tight": 0,
               "n_out_not_the_refined_form": 0,
               "cross_adic_two_violations": 0,
               "cross_adic_three_violations": 0,
               "smallest_v": None,
               "largest_L": 0}
    smallest_v = None
    bf = math.log2(3)
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        for k in range(1, min(depth, h) + 1):
            m = 3 ** k
            for a in range(h):
                for b in range(a + 1, min(h, a + window) + 1):
                    if states[a] % m != states[b] % m:
                        continue
                    t["windows"] += 1
                    r = states[a] % m
                    sub = w[a:b]
                    d = path_defect(sub, r, r, m)
                    if d is None:
                        t["defect_not_integral"] += 1
                        continue
                    ell, q = b - a, sum(sub)
                    n = (states[a] - r) // m
                    n2 = (states[b] - r) // m
                    t["returns"] += 1
                    if (1 << q) * n2 != 3 ** ell * n + d:
                        t["quotient_affine_violations"] += 1
                    if d != 0:
                        continue
                    t["zero_defect_returns"] += 1
                    t["largest_L"] = max(t["largest_L"], ell)
                    sup = (1 << q) > 3 ** ell
                    if not sup:
                        t["zero_defect_not_supercritical"] += 1
                    if sup != (q > bf * ell):
                        t["float_supercritical_route_disagreeing"] += 1
                    if n <= 0 or n2 <= 0:
                        t["quotient_not_positive"] += 1
                        continue
                    # Theorem 3.1: n = 2^{Q+1} v, n' = 2*3^L v, v >= 1
                    if n % (1 << (q + 1)):
                        t["parity_refinement_violations"] += 1
                        continue
                    v = n // (1 << (q + 1))
                    if v < 1:
                        t["parity_refinement_violations"] += 1
                    if n2 != 2 * 3 ** ell * v:
                        t["n_out_not_the_refined_form"] += 1
                    # the previous round only claimed n = 2^Q u with u >= 1;
                    # every u here is even, which is exactly the sharpening
                    if (n // (1 << q)) % 2:
                        t["u_odd_so_the_previous_rounds_form_was_tight"] += 1
                    if smallest_v is None or v < smallest_v:
                        smallest_v = v
                    # Theorem 4.1
                    if v2(n2) != v2(n) - q:
                        t["cross_adic_two_violations"] += 1
                    if v3(n2) != v3(n) + ell:
                        t["cross_adic_three_violations"] += 1
    t["smallest_v"] = smallest_v
    return t


# ---------------------------------------------------------------------------
# Theorem 5.1 -- the mechanical descent-capacity ceiling
# ---------------------------------------------------------------------------

def check_capacity(bridges: list) -> dict:
    t: dict = {"bridges": 0, "positions": 0,
               "capacity_violations": 0,
               "hmax_violations": 0,
               "float_hmax_route_disagreeing": 0,
               "hmax_violations_without_the_plus_one": 0,
               "positions_attaining_the_capacity": 0,
               "smallest_capacity_slack": None,
               "smallest_hmax_slack": None,
               "largest_hmax_seen": 0}
    small = None
    hslack: list = [None]
    bf = math.log2(3)
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        hmax = 0
        for ell in range(h + 1):
            t["positions"] += 1
            cap = mechanical_cap(ell, h)
            slack = cap - ms[ell]
            if slack < 0:
                t["capacity_violations"] += 1
            if slack == 0:
                t["positions_attaining_the_capacity"] += 1
            if small is None or slack < small:
                small = slack
            hmax = max(hmax, ms[ell])
        t["largest_hmax_seen"] = max(t["largest_hmax_seen"], hmax)
        # the same theorem's two halves have opposite tightness: the
        # per-position ceiling is attained, while the global H_max corollary
        # keeps an integer slack of `ceil(beta h) - h - H_max`
        hs = ceil_beta(h) - h - hmax
        if hslack[0] is None or hs < hslack[0]:
            hslack[0] = hs
        # H_max < (beta-1)h + 1  <->  2^{H_max + h} < 2 * 3^h
        exact = (1 << (hmax + h)) < 2 * 3 ** h
        if not exact:
            t["hmax_violations"] += 1
        if exact != (hmax < (bf - 1) * h + 1):
            t["float_hmax_route_disagreeing"] += 1
        # the corollary is stated as H_max < (beta-1)h + 1. The `+1` is what
        # the leading 2 encodes, and it turns out not to be load-bearing here:
        # H_max < (beta-1)h alone is scored separately.
        if not (1 << (hmax + h)) < 3 ** h:
            t["hmax_violations_without_the_plus_one"] += 1
    t["smallest_capacity_slack"] = small
    t["smallest_hmax_slack"] = hslack[0]
    return t


# ---------------------------------------------------------------------------
# Theorem 6.1 -- the temporal delay, in exact integers
# ---------------------------------------------------------------------------

def check_delay(bridges: list, depth: int = 5, window: int = 12) -> dict:
    t: dict = {"nodes": 0,
               "lift_toll_violations": 0,
               "capacity_below_the_delay_bound_violations": 0,
               "chained_delay_violations": 0,
               "length_bound_violations": 0,
               "float_toll_route_disagreeing": 0,
               "float_length_route_disagreeing": 0,
               "tolls_one_bit_from_failing": 0,
               "tightest_toll_margin": None,
               "smallest_prefix_p": None}
    tight = None
    small_p = None
    bf = math.log2(3)
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        z0 = states[h]
        for k in range(1, min(depth, h) + 1):
            m = 3 ** k
            for a in range(h):
                for b in range(a + 1, min(h, a + window) + 1):
                    if states[a] % m != states[b] % m:
                        continue
                    r = states[a] % m
                    sub = w[a:b]
                    d = path_defect(sub, r, r, m)
                    if d != 0:
                        continue
                    n = (states[a] - r) // m
                    n2 = (states[b] - r) // m
                    if n <= 0 or n2 <= 0:
                        continue
                    t["nodes"] += 1
                    ell, q, p = b - a, sum(sub), a
                    m_in = ms[h - a]
                    # m_in > Q + log2(M/Z0)  <->  2^{m_in} Z0 > 2^Q M
                    ok = (1 << m_in) * z0 > (1 << q) * m
                    if not ok:
                        t["lift_toll_violations"] += 1
                    if ok != (m_in > q + math.log2(m / z0) - 1e-12):
                        t["float_toll_route_disagreeing"] += 1
                    # written with the halving moved to the other side: m_in is
                    # 0 at the source end, and `1 << -1` raises rather than
                    # reporting anything
                    if not (1 << m_in) * z0 > (1 << (q + 1)) * m:
                        t["tolls_one_bit_from_failing"] += 1
                    rat = ((1 << m_in) * z0) / ((1 << q) * m)
                    if tight is None or rat < tight:
                        tight = rat
                    cap = mechanical_cap(h - a, h)
                    # cap < (beta-1)p + 1  <->  2^{cap+p} < 2 * 3^p, and a
                    # negative exponent is a true instance, not a crash
                    cap_ok = (cap + p < 0
                              or (1 << (cap + p)) < 2 * 3 ** p)
                    if m_in > cap or not cap_ok:
                        t["capacity_below_the_delay_bound_violations"] += 1
                    # (beta-1)p + 1 > Q + log2(M/Z0)
                    #   <->  2 * 3^p * Z0 > 2^{Q+p} * M
                    if not 2 * 3 ** p * z0 > (1 << (q + p)) * m:
                        t["chained_delay_violations"] += 1
                    # L < ((beta-1)p - log2(M/Z0) + 1)/beta
                    #   <->  3^L * M * 2^p < 2 * 3^p * Z0
                    lexact = 3 ** ell * m * (1 << p) < 2 * 3 ** p * z0
                    if not lexact:
                        t["length_bound_violations"] += 1
                    lf = ell < ((bf - 1) * p - math.log2(m / z0) + 1) / bf
                    if lexact != lf:
                        t["float_length_route_disagreeing"] += 1
                    if small_p is None or p < small_p:
                        small_p = p
    t["tightest_toll_margin"] = None if tight is None else round(tight, 4)
    t["smallest_prefix_p"] = small_p
    return t


# ---------------------------------------------------------------------------
# Theorem 7.1 -- decided for every q, not scanned
# ---------------------------------------------------------------------------

def check_atomic(kmax: int = 8, vmax: int = 12, qmax: int = 4000) -> dict:
    """`1 = (2^q - 3) r` with `r >= 1` forces `q = 2, r = 1`.

    `2^q - 3` must be a positive divisor of 1, so it must equal 1. That decides
    every `q >= 1` at once. The bundle scans `q < 20, r < 100` instead, whose
    assert body is reachable exactly once -- and which carries no counter.
    """
    t: dict = {"q_values_decided": 0, "solutions_found": 0,
               "solutions_other_than_q2_r1": 0,
               "q_values_where_the_divisor_exceeds_one": 0,
               "bounded_scan_iterations": 0,
               "bounded_scan_assert_reached": 0,
               "transitions_checked": 0,
               "atomic_valuation_not_two": 0,
               "atomic_target_wrong": 0,
               "atomic_defect_not_zero": 0,
               "atomic_endpoints_not_congruent": 0}
    for q in range(1, qmax + 1):
        t["q_values_decided"] += 1
        c = (1 << q) - 3
        # for q >= 3 the divisor is at least 5, so it cannot divide 1 -- which
        # is what decides every q at once, rather than a bounded scan
        if c > 1:
            t["q_values_where_the_divisor_exceeds_one"] += 1
        if c > 0 and 1 % c == 0:
            r = 1 // c
            if r >= 1:
                t["solutions_found"] += 1
                if (q, r) != (2, 1):
                    t["solutions_other_than_q2_r1"] += 1
    # what their loop actually reaches, measured on their own bounds
    for q in range(1, 20):
        for r in range(1, 100):
            t["bounded_scan_iterations"] += 1
            if 1 - ((1 << q) - 3) * r == 0:
                t["bounded_scan_assert_reached"] += 1
    # the existence half: the actual accelerated transition
    for k in range(1, kmax + 1):
        m = 3 ** k
        for v in range(1, vmax + 1):
            t["transitions_checked"] += 1
            x = 1 + 8 * m * v
            z, q = syr_step(x)
            if q != 2:
                t["atomic_valuation_not_two"] += 1
            if z != 1 + 6 * m * v:
                t["atomic_target_wrong"] += 1
            if x % m != 1 or z % m != 1:
                t["atomic_endpoints_not_congruent"] += 1
            if path_defect((2,), 1, 1, m) != 0:
                t["atomic_defect_not_zero"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 8.1 -- exact q = 2 resonance runs
# ---------------------------------------------------------------------------

def check_runs(kmax: int = 7, tmax: int = 40) -> dict:
    t: dict = {"runs": 0, "steps": 0,
               "valuation_not_two": 0,
               "state_not_congruent_to_one": 0,
               "start_quotient_wrong": 0,
               "end_quotient_wrong": 0,
               "two_adic_spend_wrong": 0,
               "three_adic_gain_wrong": 0,
               "run_defect_not_zero": 0,
               "longest_run": 0}
    for k in range(1, kmax + 1):
        m = 3 ** k
        for tt in range(1, tmax + 1):
            for v in (1, 2, 5):
                t["runs"] += 1
                n0 = (1 << (2 * tt + 1)) * v
                states = [1 + m * n0]
                qs = []
                for _ in range(tt):
                    z, q = syr_step(states[-1])
                    states.append(z)
                    qs.append(q)
                    t["steps"] += 1
                if qs != [2] * tt:
                    t["valuation_not_two"] += 1
                if any(x % m != 1 for x in states):
                    t["state_not_congruent_to_one"] += 1
                if (states[0] - 1) // m != n0:
                    t["start_quotient_wrong"] += 1
                nt = (states[-1] - 1) // m
                if nt != 2 * 3 ** tt * v:
                    t["end_quotient_wrong"] += 1
                a2, b2 = v2(n0), v2(nt)
                a3, b3 = v3(n0), v3(nt)
                if None in (a2, b2) or a2 - b2 != 2 * tt:
                    t["two_adic_spend_wrong"] += 1
                if None in (a3, b3) or b3 - a3 != tt:
                    t["three_adic_gain_wrong"] += 1
                # the whole run is one zero-defect return of length t
                if path_defect(tuple(qs), 1, 1, m) != 0:
                    t["run_defect_not_zero"] += 1
                t["longest_run"] = max(t["longest_run"], tt)
    return t


# ---------------------------------------------------------------------------
# Theorems 15.1 and 16.1 -- the reset and the replenishment cylinder
# ---------------------------------------------------------------------------

def check_reset(bridges: list, depth: int = 5, window: int = 12) -> dict:
    """Theorem 15.1 in BOTH directions, and Theorem 16.1's iff in both.

    The bundle counts only `v3(d) < L`; its converse branch raises but
    increments nothing, and Theorem 16.1's `only if` half is not tested at all.
    """
    t: dict = {"nonzero_defect_nodes": 0,
               "low_activation_nodes": 0,
               "high_activation_nodes": 0,
               "reset_violations": 0,
               "converse_violations": 0,
               "replenishment_forward_violations": 0,
               "replenishment_converse_violations": 0,
               "replenishment_probes": 0,
               "largest_b_probed": 0}
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        for k in range(1, min(depth, h) + 1):
            m = 3 ** k
            for a in range(h):
                for b in range(a + 1, min(h, a + window) + 1):
                    sub = w[a:b]
                    ra, sb = states[a] % m, states[b] % m
                    d = path_defect(sub, ra, sb, m)
                    if d is None:
                        continue
                    ell, q = b - a, sum(sub)
                    n = (states[a] - ra) // m
                    n2 = (states[b] - sb) // m
                    if n2 <= 0:
                        continue
                    if d != 0:
                        t["nonzero_defect_nodes"] += 1
                        aa = v3(d)
                        if aa < ell:
                            t["low_activation_nodes"] += 1
                            if v3(n2) != aa:
                                t["reset_violations"] += 1
                        else:
                            t["high_activation_nodes"] += 1
                            # the converse the bundle only raises on
                            if v3(n2) is None or v3(n2) < ell:
                                t["converse_violations"] += 1
                    # Theorem 16.1, both directions
                    val = 3 ** ell * n + d
                    nu = v2(n2)
                    for bb in range(0, min((nu or 0) + 3, 8)):
                        t["replenishment_probes"] += 1
                        t["largest_b_probed"] = max(t["largest_b_probed"], bb)
                        lhs = nu is not None and nu >= bb
                        rhs = val % (1 << (q + bb)) == 0
                        if lhs and not rhs:
                            t["replenishment_forward_violations"] += 1
                        if rhs and not lhs:
                            t["replenishment_converse_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 10.1, 11.1, 12.1, 13.1 -- their three synthetic blocks, measured
# ---------------------------------------------------------------------------

def check_synthetic(trials: int = 20000, seed: int = 26081423) -> dict:
    """Reimplement their generators and ask what the assertions can see.

    Not a re-run of their script: the generators are rewritten here and each
    assertion is scored twice, once on their inputs and once on inputs built to
    violate the property the block is named for. An assertion that stays green
    on both is an identity of the construction, not a test of the claim.
    """
    t: dict = {"accounting_trials": 0,
               "telescoping_Q_violations": 0,
               "telescoping_L_violations": 0,
               "supercriticality_violations": 0,
               "slack_bound_violations": 0,
               "telescoping_still_green_on_broken_input": 0,
               "supercriticality_red_on_broken_input": 0,
               "reservoir_trials": 0,
               "reservoir_guard_opened": 0,
               "reservoir_assertion_violations": 0,
               "reservoir_counters_incremented_outside_the_guard": 2,
               "smallest_reservoir_margin": None}
    bf = math.log2(3)

    def accounting(rng: Random, broken: bool):
        j = rng.randint(1, 10)
        qs, ls = [], []
        s2, s3 = [rng.randint(0, 120)], [rng.randint(0, 120)]
        e2, e3, g2, g3 = [], [], [], []
        for jj in range(j):
            ell = rng.randint(1, 12)
            q = ceil(bf * ell) + rng.randint(0, 4)
            if broken:
                q = max(1, q - 3)
            if s2[-1] < q + 1:
                s2[-1] = q + 1 + rng.randint(0, 20)
            e2.append(s2[-1] - q)
            e3.append(s3[-1] + ell)
            qs.append(q)
            ls.append(ell)
            if jj + 1 < j:
                a2 = rng.randint(-min(e2[-1], 10), 18)
                a3 = rng.randint(-min(e3[-1], 18), 10)
                g2.append(a2)
                g3.append(a3)
                s2.append(max(0, e2[-1] + a2))
                s3.append(max(0, e3[-1] + a3))
        ag2 = [s2[i + 1] - e2[i] for i in range(j - 1)]
        ag3 = [s3[i + 1] - e3[i] for i in range(j - 1)]
        lq, ll = sum(qs), sum(ls)
        telq = s2[0] + sum(ag2) - e2[-1]
        tell = e3[-1] - s3[0] - sum(ag3)
        r2 = sum(max(g, 0) for g in ag2)
        return (lq != telq, ll != tell, not lq > bf * ll,
                not lq <= s2[0] + r2)

    rng = Random(seed)
    for _ in range(trials):
        t["accounting_trials"] += 1
        a, b, c, d = accounting(rng, False)
        t["telescoping_Q_violations"] += int(a)
        t["telescoping_L_violations"] += int(b)
        t["supercriticality_violations"] += int(c)
        t["slack_bound_violations"] += int(d)
    rng = Random(seed + 1)
    for _ in range(trials):
        a, b, c, _d = accounting(rng, True)
        if not a and not b:
            t["telescoping_still_green_on_broken_input"] += 1
        t["supercriticality_red_on_broken_input"] += int(c)

    rng = Random(seed + 2)
    theta = (bf - 1) / bf
    margin = None
    for _ in range(trials):
        t["reservoir_trials"] += 1
        h = rng.randint(1000, 10 ** 8)
        gamma = rng.uniform(0.05, 0.45)
        logh = math.log2(h)
        c = gamma * logh - rng.uniform(0, 0.01) * logh
        hmax = (bf - 1) * h + 1
        r0 = rng.uniform(0, h)
        lower2 = max(0.0, bf * r0 - hmax + c - 1)
        lower3 = max(0.0, r0 - (hmax - c + 1) / bf)
        if r0 / h > theta + 0.02:
            t["reservoir_guard_opened"] += 1
            if not (lower2 / h > bf * 0.019 and lower3 / h > 0.019):
                t["reservoir_assertion_violations"] += 1
            gap = min(lower2 / h - bf * 0.019, lower3 / h - 0.019)
            if margin is None or gap < margin:
                margin = gap
    t["smallest_reservoir_margin"] = (None if margin is None
                                      else round(margin, 6))
    return t


# ---------------------------------------------------------------------------
# the previous round's population, as an independent witness
# ---------------------------------------------------------------------------

def check_cross_round(limit: int = 220000, max_steps: int = 110) -> dict:
    """Theorems 3.1 and 4.1 against RUN-050's bridges and RUN-050's walker.

    A different limit, and the interval family comes from the erasure walker
    rather than this round's window scan -- so the two populations are not the
    same objects. If the sharpening only held on the sample this round happens
    to enumerate, it would show here.
    """
    from src69_defect_tree import erasure_intervals                # noqa: PLC0415
    from src69_defect_tree import zero_lift as zl69                # noqa: PLC0415
    t: dict = {"bridges": 0, "zero_defect_returns": 0,
               "parity_refinement_violations": 0,
               "n_out_not_the_refined_form": 0,
               "cross_adic_two_violations": 0,
               "cross_adic_three_violations": 0,
               "u_odd_on_the_previous_population": 0,
               "smallest_v": None}
    smallest = None
    for y, X, Z, states, w, ms in zl69(limit, max_steps):
        t["bridges"] += 1
        h = len(w)
        for k in range(1, min(5, h) + 1):
            m = 3 ** k
            for a, b, r in erasure_intervals(states, m):
                sub = w[a:b]
                d = path_defect(sub, r, r, m)
                if d != 0:
                    continue
                ell, q = b - a, sum(sub)
                n = (states[a] - r) // m
                n2 = (states[b] - r) // m
                if n <= 0 or n2 <= 0:
                    continue
                t["zero_defect_returns"] += 1
                if n % (1 << (q + 1)):
                    t["parity_refinement_violations"] += 1
                    continue
                v = n // (1 << (q + 1))
                if v < 1:
                    t["parity_refinement_violations"] += 1
                if n2 != 2 * 3 ** ell * v:
                    t["n_out_not_the_refined_form"] += 1
                if (n // (1 << q)) % 2:
                    t["u_odd_on_the_previous_population"] += 1
                if v2(n2) != v2(n) - q:
                    t["cross_adic_two_violations"] += 1
                if v3(n2) != v3(n) + ell:
                    t["cross_adic_three_violations"] += 1
                if smallest is None or v < smallest:
                    smallest = v
    t["smallest_v"] = smallest
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"zero_rows": 0, "nonzero_rows": 0,
               "quotient_identity_violations": 0,
               "parity_refinement_violations": 0,
               "valuation_fields_disagreeing": 0,
               "supercriticality_violations": 0,
               "nonzero_row_defect_valuation_disagreeing": 0,
               "nonzero_row_quotient_identity_violations": 0,
               "rows": []}
    for ex in report.get("zero_defect_examples", []) or []:
        t["zero_rows"] += 1
        m, ell, q = ex["M"], ex["L"], ex["Q"]
        n, n2 = ex["n_in"], ex["n_out"]
        if (1 << q) * n2 != 3 ** ell * n:
            t["quotient_identity_violations"] += 1
        if n % (1 << (q + 1)) or n2 != 2 * 3 ** ell * (n // (1 << (q + 1))):
            t["parity_refinement_violations"] += 1
        if (v2(n) != ex["nu2_in"] or v2(n2) != ex["nu2_out"]
                or v3(n) != ex["nu3_in"] or v3(n2) != ex["nu3_out"]):
            t["valuation_fields_disagreeing"] += 1
        if not (1 << q) > 3 ** ell:
            t["supercriticality_violations"] += 1
        t["rows"].append({"M": m, "L": ell, "Q": q, "p": ex["forward_prefix_p"],
                          "n_in": n, "n_out": n2, "m_in": ex["m_in"]})
    for ex in report.get("nonzero_defect_examples", []) or []:
        t["nonzero_rows"] += 1
        m, ell, q, d = ex["M"], ex["L"], ex["Q"], ex["defect"]
        n, n2 = ex["n_in"], ex["n_out"]
        if (1 << q) * n2 != 3 ** ell * n + d:
            t["nonzero_row_quotient_identity_violations"] += 1
        aa = v3(d)
        if aa is not None and aa < ell and n2 > 0 and v3(n2) != aa:
            t["nonzero_row_defect_valuation_disagreeing"] += 1
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
    files = val.get("files", {}) or {}
    named = set(files) | set(val.get("json_parse", {}) or {})
    pc = val.get("python_compile")
    if isinstance(pc, dict) and "file" in pc:
        named.add(pc["file"])
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
    # the key has been `all_pass` and is now `overall_pass`; reading only
    # one name would render a real False as None
    t["validation_all_pass_flag"] = (val.get("all_pass")
                                     if "all_pass" in val
                                     else val.get("overall_pass"))
    t["validation_pass_flag_key"] = ("all_pass" if "all_pass" in val
                                     else "overall_pass"
                                     if "overall_pass" in val else None)
    t["validation_records_no_pass_flag_at_all"] = int(
        "all_pass" not in val and "overall_pass" not in val)
    t["validation_top_level_keys"] = sorted(val)
    t["validation_file_pass_flags_not_true"] = sum(
        1 for r in files.values()
        if isinstance(r, dict) and r.get("pass") is not True)
    t["validation_json_parse_not_true"] = sum(
        1 for r in (val.get("json_parse", {}) or {}).values()
        if isinstance(r, dict) and r.get("pass") is not True)
    t["validation_python_compile_not_true"] = int(
        isinstance(pc, dict) and pc.get("pass") is not True)
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
    pr = re.search(r"## 24\.1(.*?)## 24\.2", paper, re.S)
    if pr:
        t["paper_proved_items"] = len(re.findall(r"^\d+\. ", pr.group(1), re.M))
    ob = re.search(r"## 24\.4(.*?)(?:\n---|\Z)", paper, re.S)
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


def check_population(bridges: list) -> dict:
    return {"bridges": len(bridges),
            "sources": len({r[0] for r in bridges}),
            "longest_tail": max((len(r[4]) for r in bridges), default=0)}


def check_their_claims(report: dict, res: dict) -> dict:
    rs, cp, dl = res["resonance"], res["capacity"], res["delay"]
    rt, rn, at = res["reset"], res["runs"], res["atomic"]
    sy = res["synthetic"]
    # their zero-defect window scan is deterministic (`for a in range(h): for
    # b in range(a+1, min(h, a+12)+1)`), so those counts are reproductions on
    # the same population, not coincidences on a different one
    same = {
        "finite_zero_lift_bridges": res["population"]["bridges"],
        "mechanical_descent_capacity": cp["positions"],
        "zero_defect_actual_returns": rs["zero_defect_returns"],
        "zero_defect_parity_refinement": rs["zero_defect_returns"],
        "zero_defect_cross_adic_transfer": rs["zero_defect_returns"],
        "zero_defect_temporal_delay": dl["nodes"],
        "atomic_q2_resonance_runs": rn["runs"],
        "resonance_accounting_synthetic": sy["accounting_trials"],
    }
    other = {
        "general_quotient_affine_identity": ("resonance.returns", rs["returns"]),
        "binary_output_divisibility_identity": ("reset.replenishment_probes",
                                                rt["replenishment_probes"]),
        "nonzero_defect_ternary_reset": ("reset.low_activation_nodes",
                                         rt["low_activation_nodes"]),
        "reservoir_to_lift_algebra": ("synthetic.reservoir_guard_opened",
                                      sy["reservoir_guard_opened"]),
        "linear_mass_recharge_threshold_algebra":
            ("synthetic.reservoir_guard_opened", sy["reservoir_guard_opened"]),
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
    rows.append({"check": "(Theorem 7.1 uniqueness -- no counter of their own)",
                 "theirs": None, "mine": at["q_values_decided"],
                 "basis": "atomic.q_values_decided"})
    return {"rows": rows,
            "checks_not_covered_at_all": sum(1 for r in rows
                                             if r["basis"] == "not covered"),
            "checks_covered_by_a_different_population": covered,
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "counts_i_reproduce_exactly": exact}


SECTIONS = ("instrument", "constants", "population", "resonance", "capacity",
            "delay", "atomic", "runs", "reset", "synthetic",
            "cross_round", "examples",
            "artifacts", "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("resonance", "defect_not_integral"),
    ("resonance", "quotient_affine_violations"),
    ("resonance", "zero_defect_not_supercritical"),
    ("resonance", "float_supercritical_route_disagreeing"),
    ("resonance", "quotient_not_positive"),
    ("resonance", "parity_refinement_violations"),
    ("resonance", "n_out_not_the_refined_form"),
    ("resonance", "cross_adic_two_violations"),
    ("resonance", "cross_adic_three_violations"),
    ("capacity", "capacity_violations"),
    ("capacity", "hmax_violations"),
    ("capacity", "float_hmax_route_disagreeing"),
    ("delay", "lift_toll_violations"),
    ("delay", "capacity_below_the_delay_bound_violations"),
    ("delay", "chained_delay_violations"),
    ("delay", "length_bound_violations"),
    ("delay", "float_toll_route_disagreeing"),
    ("delay", "float_length_route_disagreeing"),
    ("atomic", "solutions_other_than_q2_r1"),
    ("atomic", "atomic_valuation_not_two"),
    ("atomic", "atomic_target_wrong"),
    ("atomic", "atomic_defect_not_zero"),
    ("atomic", "atomic_endpoints_not_congruent"),
    ("runs", "valuation_not_two"),
    ("runs", "state_not_congruent_to_one"),
    ("runs", "start_quotient_wrong"),
    ("runs", "end_quotient_wrong"),
    ("runs", "two_adic_spend_wrong"),
    ("runs", "three_adic_gain_wrong"),
    ("runs", "run_defect_not_zero"),
    ("reset", "reset_violations"),
    ("reset", "converse_violations"),
    ("reset", "replenishment_forward_violations"),
    ("reset", "replenishment_converse_violations"),
    ("synthetic", "telescoping_Q_violations"),
    ("synthetic", "telescoping_L_violations"),
    ("synthetic", "supercriticality_violations"),
    ("synthetic", "slack_bound_violations"),
    ("synthetic", "reservoir_assertion_violations"),
    ("cross_round", "parity_refinement_violations"),
    ("cross_round", "n_out_not_the_refined_form"),
    ("cross_round", "cross_adic_two_violations"),
    ("cross_round", "cross_adic_three_violations"),
    ("examples", "quotient_identity_violations"),
    ("examples", "parity_refinement_violations"),
    ("examples", "valuation_fields_disagreeing"),
    ("examples", "supercriticality_violations"),
    ("examples", "nonzero_row_defect_valuation_disagreeing"),
    ("examples", "nonzero_row_quotient_identity_violations"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_file_pass_flags_not_true"),
    ("artifacts", "validation_json_parse_not_true"),
    ("artifacts", "validation_python_compile_not_true"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("population", "bridges"),
    ("population", "sources"),
    ("resonance", "windows"),
    ("resonance", "returns"),
    ("resonance", "zero_defect_returns"),
    ("capacity", "positions"),
    ("capacity", "positions_attaining_the_capacity"),
    ("delay", "nodes"),
    ("atomic", "q_values_decided"),
    ("atomic", "solutions_found"),
    ("atomic", "transitions_checked"),
    ("runs", "runs"),
    ("runs", "steps"),
    ("reset", "nonzero_defect_nodes"),
    ("reset", "low_activation_nodes"),
    ("reset", "high_activation_nodes"),
    ("reset", "replenishment_probes"),
    ("synthetic", "accounting_trials"),
    ("synthetic", "reservoir_trials"),
    ("synthetic", "reservoir_guard_opened"),
    ("synthetic", "supercriticality_red_on_broken_input"),
    ("synthetic", "telescoping_still_green_on_broken_input"),
    ("cross_round", "bridges"),
    ("cross_round", "zero_defect_returns"),
    ("examples", "zero_rows"),
    ("examples", "nonzero_rows"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "frontier_and_report_disagreeing"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("population", "longest_tail"),
    ("resonance", "bridges"),
    ("resonance", "u_odd_so_the_previous_rounds_form_was_tight"),
    ("resonance", "smallest_v"),
    ("resonance", "largest_L"),
    ("capacity", "bridges"),
    ("capacity", "smallest_capacity_slack"),
    ("capacity", "smallest_hmax_slack"),
    ("capacity", "largest_hmax_seen"),
    ("capacity", "hmax_violations_without_the_plus_one"),
    ("delay", "tolls_one_bit_from_failing"),
    ("delay", "tightest_toll_margin"),
    ("delay", "smallest_prefix_p"),
    ("atomic", "q_values_where_the_divisor_exceeds_one"),
    ("atomic", "bounded_scan_iterations"),
    ("atomic", "bounded_scan_assert_reached"),
    ("runs", "longest_run"),
    ("reset", "largest_b_probed"),
    ("synthetic", "reservoir_counters_incremented_outside_the_guard"),
    ("synthetic", "smallest_reservoir_margin"),
    ("cross_round", "u_odd_on_the_previous_population"),
    ("cross_round", "smallest_v"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
    ("artifacts", "validation_records_no_pass_flag_at_all"),
    ("artifacts", "validation_entries_with_a_digest"),
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
    ap.add_argument("--limit", type=int, default=180000)
    ap.add_argument("--max-steps", type=int, default=110)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    bridges = zero_lift(a.limit, a.max_steps)

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
    run("population", lambda: check_population(bridges))
    run("resonance", lambda: check_resonance(bridges))
    run("capacity", lambda: check_capacity(bridges))
    run("delay", lambda: check_delay(bridges))
    run("atomic", check_atomic)
    run("runs", check_runs)
    run("reset", lambda: check_reset(bridges))
    run("synthetic", check_synthetic)
    run("cross_round", check_cross_round)
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
        "run": "RUN-051", "round": "A-U.2d.23", "bundle": str(bundle),
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
