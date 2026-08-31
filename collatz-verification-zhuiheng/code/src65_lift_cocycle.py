"""RUN-046 — independent recheck of Hard-Zeta round A-U.2d.18.

`Double-Canonical Critical Cylinder Spectral Rigidity` (source item 65).
數學戰士「墜衡」.

The round replaces A-U.2d.17's real-valued slack profile with an INTEGER one.
For suffix length `ell`, with `Q_ell` the suffix valuation sum,

    eps_ell := ceil(beta ell) - beta ell,     m_ell := Q_ell - ceil(beta ell)

and `H_{h-ell} = m_ell + eps_ell`. That makes almost every statement in the
round checkable with no logarithm at all, because

  * `ceil(beta ell) = (3^ell).bit_length()` -- `beta*ell` is never an integer;
  * `2^{eps_ell} = 2^{ceil(beta ell)} / 3^ell`, an exact rational;
  * the mechanical increments `a_ell = ceil(beta ell) - ceil(beta(ell-1))` are
    integers in {1,2}, and `beta > 3/2` forbids two consecutive ones.

Three things this gate does that the shipped checker does not.

First, the shipped checker computes `ceil(BETA*l)` in float64. That is SAFE at
the sizes it uses, and this gate proves it rather than assuming it: the exact
ceiling is compared against the float64 one over the whole range, and the
closest approach of `beta*ell` to an integer is measured, so the margin is a
number rather than a hope.

Second, `H_{h-ell} = m_ell + eps_ell` and the reindexed Laplace identity are
IDENTITIES -- the second is A-U.2d.17's identity with `i = h - ell`, which
RUN-045 already showed is the definition of `B_w`. What can be wrong is the
reindexing, so the two indexings are compared term by term.

Third, two of the bundle's twelve counters are vacuous. Its
`near_linear_gap_algebra` block asserts `lower > 0` for `lower = N/(R+1)` with
`N >= 10^6` -- true for every admissible input. Its
`positive_lift_drop_algebra` block asserts `drop >= 2-beta-1e-15` for
`drop = m + eps - beta + 1`, in which `beta` cancels exactly, leaving
`m + eps >= 1` with `m >= 1` an integer. Twenty thousand of its assertion
executions test a quantity against itself; this gate demonstrates the
cancellation rather than restating it.

Usage:
    python code/src65_lift_cocycle.py --bundle <dir> [--limit N]
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

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src47_survival_closure import rational_digits                 # noqa: E402
from src53_plateau_reset import (                                   # noqa: E402
    accelerated, bracket_decimal, cumulative, ln2_bracket, v2,
)
from src54_low_source_saturation import (                           # noqa: E402
    ln_bracket, simplify, ulps_against_bracket, widen,
)
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    b_of, beta_hi, beta_lo, log2_any, log2_int, prefix_sums,
    suffix_supercritical, verdict_with_budget,
)

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d18_Double_Canonical_Critical_Cylinder"
         "_Spectral_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d18_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d18_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d18_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d18.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.18_AU2d18.md"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def step(n: int) -> tuple[int, int]:
    t = 3 * n + 1
    k = v2(t)
    return t >> k, k


def ceil_beta(ell: int) -> int:
    """`ceil(beta * ell)`, with no logarithm.

    `beta * ell` is irrational for `ell >= 1`, so the ceiling is one above the
    floor, and the floor is `(3^ell).bit_length() - 1`.
    """
    return (3 ** ell).bit_length() if ell else 0


def mech_a(ell: int) -> int:
    return ceil_beta(ell) - ceil_beta(ell - 1)


def two_pow_eps(ell: int) -> Fraction:
    """`2^{eps_ell} = 2^{ceil(beta ell)} / 3^ell`, exact."""
    return Fraction(1 << ceil_beta(ell), 3 ** ell)


def p2(k: int) -> Fraction:
    """`2^k` as an exact rational, for ANY integer `k`.

    `1 << k` raises on a negative exponent, and a negative lift is a finding
    this gate must report through `lift.lift_negative` rather than crash on
    four sections later. Nothing here needs `k` to be nonnegative.
    """
    return Fraction(1 << k) if k >= 0 else Fraction(1, 1 << -k)


def lift_profile(word: tuple[int, ...]) -> list[int]:
    """`m_ell = Q_ell - ceil(beta ell)` for `0 <= ell <= h`, integers only."""
    h, run, out = len(word), 0, [0]
    for ell in range(1, h + 1):
        run += word[h - ell]
        out.append(run - ceil_beta(ell))
    return out


def local_bridges(limit_y: int, max_steps: int
                  ) -> list[tuple[int, int, int, tuple[int, ...], tuple[int, ...]]]:
    """The bundle's finite-bridge population, rebuilt from its definition.

    Same shape as A-U.2d.17's but wider -- `limit_y = 35000`, `max_steps = 44`
    rather than 25000 and 36, which is why the reported count moves from 874 to
    1228. Values are carried so the reverse cocycle can be checked on the real
    states rather than on the word alone.
    """
    out = []
    for y in range(7, limit_y + 1, 2):
        if y % 3 == 0 or y % 12 not in (7, 11):
            continue
        vals, qs, seen, cur = [y], [], {y}, y
        for s in range(1, max_steps + 1):
            cur, q = step(cur)
            if cur in seen:
                break
            seen.add(cur)
            vals.append(cur)
            qs.append(q)
            if s >= 2 and cur > y and cur % 12 in (7, 11):
                inter = vals[1:-1]
                if inter and cur < min(inter) and qs[0] == 1:
                    tail = tuple(qs[1:])
                    if tail and suffix_supercritical(tail):
                        out.append((y, vals[1], cur, tuple(vals), tail))
            if cur == 1:
                break
    return out


def abstract_zero_lift(h: int) -> tuple[list[int], list[int], list[int], Fraction, int]:
    """Theorem 14.1's construction, rebuilt from the paper's three steps.

    Rise by one for `M = ceil(2 log2 h)` reverse positions, hold, then descend
    one unit at each of the final `M` mechanical twos. `ceil(2 log2 h)` is
    computed as the bit length of `h^2`, so no logarithm enters.
    """
    a = [0] + [mech_a(ell) for ell in range(1, h + 1)]
    M = (h * h - 1).bit_length()                 # = ceil(2 log2 h) for h >= 2
    twos = [ell for ell in range(1, h + 1) if a[ell] == 2]
    if len(twos) < M or twos[-M] <= M + 2:
        return a, [], [], Fraction(0), M
    first_descent = twos[-M]
    m = [0] * (h + 1)
    for ell in range(1, M + 1):
        m[ell] = m[ell - 1] + 1
    for ell in range(M + 1, first_descent):
        m[ell] = M
    cur = M
    for ell in range(first_descent, h + 1):
        if a[ell] == 2 and cur > 0:
            cur -= 1
        m[ell] = cur
    q = [a[ell] + m[ell] - m[ell - 1] for ell in range(1, h + 1)]
    mass = sum(p2(-x) for x in m[1:])
    return a, m, q, mass, M


# ---------------------------------------------------------------------------
# instrument
# ---------------------------------------------------------------------------

def check_instrument() -> dict:
    out: dict = {"checks": 0, "failed": []}

    def want(name: str, ok: bool) -> None:
        out["checks"] += 1
        if not ok:
            out["failed"].append(name)

    b_lo, b_hi = beta_lo(), beta_hi()
    want("beta bracket has width", b_lo < b_hi)
    lo, hi = log2_any(Fraction(3))
    want("log2(3) agrees with beta", lo <= b_hi and hi >= b_lo)

    # the exact ceiling, both ways round: it must equal the bracketed value AND
    # must not equal the floor, or a function returning the bit length minus
    # one would pass.
    bad, flat = 0, 0
    for ell in (1, 2, 7, 41, 306, 1000):
        c = ceil_beta(ell)
        if not (c - 1 < ell * b_lo and ell * b_hi < c):
            bad += 1
        if c == (3 ** ell).bit_length() - 1:
            flat += 1
    want("ceil(beta l) brackets beta*l strictly on both sides", bad == 0)
    want("ceil(beta l) is not the floor", flat == 0)

    # `2^{eps_l} = 2^{ceil(beta l)} / 3^l` must land in (1,2)
    bad = 0
    for ell in range(1, 300):
        e = two_pow_eps(ell)
        if not 1 < e < 2:
            bad += 1
    want("2^{eps_l} lies strictly between one and two", bad == 0)

    # the mechanical alphabet, and the fact Theorem 14.1's construction needs
    bad, consec = 0, 0
    for ell in range(1, 4000):
        if mech_a(ell) not in (1, 2):
            bad += 1
        if ell > 1 and mech_a(ell - 1) == 1 and mech_a(ell) == 1:
            consec += 1
    want("a_l is one or two", bad == 0)
    want("beta > 3/2 forbids two consecutive mechanical ones", consec == 0)
    want("both symbols actually occur",
         any(mech_a(l) == 1 for l in range(1, 50))
         and any(mech_a(l) == 2 for l in range(1, 50)))

    # the residue lemma behind Theorem 13.1: 2 = -1 mod 3, so the parity of the
    # valuation is forced by the reverse state's class
    bad = 0
    for q in range(1, 40):
        for v in (1, 2):
            ok = (pow(2, q, 3) * v) % 3 == 1
            if ok != (q % 2 == (0 if v == 1 else 1)):
                bad += 1
    want("2^q v = 1 mod 3 iff q has the parity pi(v)", bad == 0)

    # Corollary 11.2's two elementary inequalities, at rational points
    l2_lo, l2_hi = ln2_bracket()
    want("ln2 bracket straddles 0.693", l2_lo < Fraction(694, 1000)
         and l2_hi > Fraction(693, 1000))
    bad = 0
    for y in (1, 2, 3, 7, 101, 10 ** 6):
        x = Fraction(1, 3 * y)
        lo, hi = ln_bracket(1 + x)
        if not lo >= Fraction(1, 3 * y + 1):
            bad += 1
        if not Fraction(1, 3 * y + 1) >= Fraction(1, 4 * y):
            bad += 1
    want("ln(1+1/3Y) >= 1/(3Y+1) >= 1/(4Y) for Y >= 1", bad == 0)
    return out


# ---------------------------------------------------------------------------
# is their float64 ceiling safe at the sizes they use?
# ---------------------------------------------------------------------------

def check_float_ceiling(limit: int = 20000, prec: int = 200) -> dict:
    """The shipped checker computes `ceil(BETA*l)` in float64.

    That is a real risk -- `beta*l` never lands on an integer, but a float64
    product can, and the ceiling would then be one too low. Measured rather
    than assumed.

    Building `3^l` for every `l` up to twenty thousand costs half a minute in
    Fraction gcds, and none of it is needed: a certified bracket for `beta`
    scaled to `prec` bits decides `floor(beta*l)` by integer division whenever
    its two ends agree, and `l` times a `2^-prec` bracket is `2^-185` here
    against a closest approach near `2^-16`. The exact `(3^l).bit_length()`
    route is still run at a handful of levels, including the minimiser, so the
    fixed-point route is anchored to the certified one rather than trusted.
    """
    t: dict = {"levels": 0, "float_ceiling_disagreements": 0,
               "first_disagreement": None,
               "fixed_point_undecided": 0,
               "fixed_point_disagreeing_with_the_exact_route": 0,
               "exact_levels_cross_checked": 0,
               "closest_approach_level": None,
               "closest_approach": None,
               "float64_error_at_that_level": None,
               "margin_ratio": None}
    b_lo, b_hi = beta_tight()
    scale = 1 << prec
    n_lo = (b_lo.numerator * scale) // b_lo.denominator
    n_hi = -((-b_hi.numerator * scale) // b_hi.denominator)
    beta_f = math.log2(3)
    worst, worst_l = None, None
    for ell in range(1, limit + 1):
        t["levels"] += 1
        f_lo, f_hi = (ell * n_lo) >> prec, (ell * n_hi) >> prec
        if f_lo != f_hi:
            t["fixed_point_undecided"] += 1
            continue
        exact = f_lo + 1                      # ceil, since beta*ell is irrational
        if math.ceil(beta_f * ell) != exact:
            t["float_ceiling_disagreements"] += 1
            if t["first_disagreement"] is None:
                t["first_disagreement"] = ell
        # fractional part of beta*ell in fixed point, and its distance to the
        # nearer end of the unit interval
        frac = (ell * n_lo) - (f_lo << prec)
        d = min(frac, scale - frac)
        if worst is None or d < worst:
            worst, worst_l = d, ell
    # anchor the fixed-point route to the certified one at a few levels
    for ell in (1, 2, 41, 306, worst_l or 1, limit):
        t["exact_levels_cross_checked"] += 1
        f = ((ell * n_lo) >> prec) + 1
        if f != (3 ** ell).bit_length():
            t["fixed_point_disagreeing_with_the_exact_route"] += 1
    t["closest_approach_level"] = worst_l
    t["closest_approach"] = float(Fraction(worst, scale)) if worst else None
    # a double's error in beta*ell is about ell ulps of beta
    err = 2.0 ** -52 * beta_f * limit
    t["float64_error_at_that_level"] = err
    # `closest_approach` is None when every level came back undecided, which is
    # itself a reported failure; the ratio must not raise on top of it
    t["margin_ratio"] = (None if not (t["closest_approach"] and err)
                         else t["closest_approach"] / err)
    return t


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
               "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    l2_lo, l2_hi = widen(*ln2_bracket(), 40)
    pb = frontier["beta"]
    items = [
        ("beta", b_lo, b_hi, pb, 4),
        ("beta_minus_1", b_lo - 1, b_hi - 1, pb - 1.0, 12),
        ("two_minus_beta", 2 - b_hi, 2 - b_lo, 2.0 - pb, 20),
        ("near_linear_gap_exponent_limit", Fraction(1), Fraction(1), 1.0, 4),
        ("first_hit_single_cylinder_exponent_limit",
         1 / (b_hi - 1), 1 / (b_lo - 1), 1.0 / (pb - 1.0), 12),
        ("first_hit_formal_joint_ratio_exponent_limit",
         2 / (b_hi - 1), 2 / (b_lo - 1), 2 * (1.0 / (pb - 1.0)), 12),
        ("zero_lift_reciprocal_mass_ceiling",
         4 * l2_lo, 4 * l2_hi, 4 * math.log(2), 4),
    ]
    for name, lo, hi, chain, budget in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        rpt = report.get("constants", {}).get(name)
        if rpt is not None and rpt != pub:
            t["frontier_and_report_disagreeing"] += 1
        row = {"constant": name, "published": repr(pub), "budget": budget}
        verdict, d = verdict_with_budget(pub, lo, hi, chain, budget)
        if verdict == "undecided":
            t["undecided_brackets"] += 1
        elif verdict == "exact":
            t["exact_to_the_last_bit"] += 1
        elif verdict == "the float64 chain":
            t["from_the_float64_chain_not_the_nearest_double"] += 1
        else:
            t["disagreeing_with_both_evaluations"] += 1
        row["verdict"] = verdict if d == 0 else "%+d ulp, %s" % (d, verdict)
        row["nearest_double"] = repr(float(lo))
        t["rows"].append(row)
    return t


# ---------------------------------------------------------------------------
# the lift profile
# ---------------------------------------------------------------------------

def check_lift(limit: int, max_steps: int) -> dict:
    t: dict = {"bridges": 0, "sources": 0, "longest_tail": 0,
               "profile_positions": 0,
               "rank_one_upper_violations": 0,
               "rank_one_lower_violations": 0,
               "left_record_not_below_the_endpoint": 0,
               "source_not_three_y_plus_one_over_two": 0,
               "lift_negative": 0,
               "lift_nonnegative_disagreeing_with_supercriticality": 0,
               "slack_decomposition_violations": 0,
               "recurrence_theorem_8_1_violations": 0,
               "lift_descends_by_more_than_one": 0,
               "lift_descends_at_a_mechanical_one": 0,
               "total_lift_not_q_minus_ceil_beta_h": 0,
               "zero_total_lift": 0, "positive_total_lift": 0,
               "largest_interior_lift": 0,
               "descents_seen": 0}
    sources: set[int] = set()
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        t["bridges"] += 1
        h, Q = len(w), sum(w)
        t["longest_tail"] = max(t["longest_tail"], h)

        # Theorem 6.1, in integers. Both halves, because the upper one follows
        # from `y < Z` and the lower from the record ordering; a check of only
        # one would miss half the statement.
        if not X < Fraction(3 * Z + 1, 2):
            t["rank_one_upper_violations"] += 1
        if not Z < X:
            t["rank_one_lower_violations"] += 1
        if not y < Z:
            t["left_record_not_below_the_endpoint"] += 1
        if X != (3 * y + 1) // 2 or (3 * y + 1) % 2:
            t["source_not_three_y_plus_one_over_two"] += 1

        ms = lift_profile(w)
        for ell in range(1, h + 1):
            t["profile_positions"] += 1
            # Theorem 7.1. `m_ell >= 0` is EQUIVALENT to suffix
            # supercriticality, so the two are compared rather than one being
            # assumed: `Q_ell > beta ell` iff `Q_ell >= ceil(beta ell)`.
            q_ell = sum(w[h - ell:])
            if ms[ell] < 0:
                t["lift_negative"] += 1
            if (ms[ell] >= 0) != ((1 << q_ell) > 3 ** ell):
                t["lift_nonnegative_disagreeing_with_supercriticality"] += 1
            # `H_{h-ell} = m_ell + eps_ell` is an identity; its content is the
            # suffix indexing, so compare `2^{-H}` against `2^{-m} 2^{-eps}`
            # as exact rationals.
            lhs = Fraction(3 ** ell, 1 << q_ell)
            rhs = p2(-ms[ell]) / two_pow_eps(ell)
            if lhs != rhs:
                t["slack_decomposition_violations"] += 1
            # Theorem 8.1
            a = mech_a(ell)
            if ms[ell] - ms[ell - 1] != w[h - ell] - a:
                t["recurrence_theorem_8_1_violations"] += 1
            if ms[ell] < ms[ell - 1]:
                t["descents_seen"] += 1
                if ms[ell] < ms[ell - 1] - 1:
                    t["lift_descends_by_more_than_one"] += 1
                if a != 2:
                    t["lift_descends_at_a_mechanical_one"] += 1
        if ms[h] != Q - ceil_beta(h):
            t["total_lift_not_q_minus_ceil_beta_h"] += 1
        if ms[h] == 0:
            t["zero_total_lift"] += 1
        else:
            t["positive_total_lift"] += 1
        t["largest_interior_lift"] = max(t["largest_interior_lift"], max(ms))
        sources.add(y)
    t["sources"] = len(sources)
    return t


# ---------------------------------------------------------------------------
# the Laplace budget, reindexed
# ---------------------------------------------------------------------------

def check_budget(limit: int, max_steps: int) -> dict:
    """Theorem 9.1 and the plateau, with the reindexing checked and the
    vacuity counted.

    `sum_ell 2^{-m_ell-eps_ell} = 3(Z - 2^{-E}X)` is A-U.2d.17's identity under
    `i = h - ell`, and RUN-045 showed that identity is the definition of `B_w`.
    So the substance here is (a) that the two indexings agree term by term and
    (b) the strict inequality `sum 2^{-m_ell} < 6Z` that follows from
    `eps < 1`.
    """
    t: dict = {"bridges": 0, "reindexing_violations": 0,
               "laplace_identity_violations": 0,
               "budget_theorem_9_1_violations": 0,
               "budget_is_not_within_a_factor_two_of_the_identity": 0,
               "quantile_instances": 0,
               "quantile_violations": 0,
               "quantile_instances_that_are_not_vacuous": 0,
               "sharp_quantile_instances_that_are_not_vacuous": 0,
               "sharp_quantile_violations": 0,
               "budget_over_six_z_ratio_smallest": None}
    smallest = None
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        t["bridges"] += 1
        h, Q = len(w), sum(w)
        P = prefix_sums(w)
        ms = lift_profile(w)

        # (a) the reindexing, term by term
        old = [Fraction(3 ** (h - i), 1 << (Q - P[i])) for i in range(h)]
        new = [p2(-ms[ell]) / two_pow_eps(ell)
               for ell in range(1, h + 1)]
        # `old != list(reversed(new))` is the whole test; comparing the
        # sorted lists as well adds nothing, since equal reversals are equal
        # multisets.
        if old != list(reversed(new)):
            t["reindexing_violations"] += 1
        s_real = sum(new)
        if s_real != 3 * (Fraction(Z) - Fraction(3 ** h, 1 << Q) * X):
            t["laplace_identity_violations"] += 1

        # (b) the integer budget
        s_int = sum(p2(-m) for m in ms[1:])
        if not s_int < 6 * Z:
            t["budget_theorem_9_1_violations"] += 1
        # eps in (0,1) gives 2^{-m-eps} in (2^{-m-1}, 2^{-m}), so the integer
        # sum must sit between the real one and twice it
        if not s_real < s_int < 2 * s_real:
            t["budget_is_not_within_a_factor_two_of_the_identity"] += 1
        r = s_int / (6 * Z)
        if smallest is None or r > smallest:
            smallest = r

        for a in range(1, 13):
            t["quantile_instances"] += 1
            cnt = sum(1 for m in ms[1:] if m < a)
            if not cnt < 6 * Z * (1 << a):
                t["quantile_violations"] += 1
            if 6 * Z * (1 << a) < h:
                t["quantile_instances_that_are_not_vacuous"] += 1
            if s_int * (1 << a) < h:
                t["sharp_quantile_instances_that_are_not_vacuous"] += 1
            if not cnt < s_int * (1 << a):
                t["sharp_quantile_violations"] += 1
    t["budget_over_six_z_ratio_smallest"] = (None if smallest is None
                                             else float(smallest))
    return t


# ---------------------------------------------------------------------------
# the mechanical cocycle
# ---------------------------------------------------------------------------

def check_cocycle(limit: int, max_steps: int) -> dict:
    """Theorems 12.1, 12.2 and their closed form, in exact rationals."""
    t: dict = {"bridges": 0, "steps": 0,
               "reverse_recursion_violations": 0,
               "lifted_cocycle_theorem_12_1_violations": 0,
               "normalized_cocycle_theorem_12_2_violations": 0,
               "closed_form_violations": 0,
               "weight_outside_one_half_to_two": 0,
               "u_zero_not_the_endpoint": 0,
               "u_h_not_the_source_on_a_zero_lift_bridge": 0,
               "residue_parity_theorem_13_1_violations": 0,
               "residue_parity_not_equal_to_the_valuation_parity": 0,
               "reverse_state_outside_one_or_two_mod_three": 0,
               "zero_lift_bridges": 0}
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        t["bridges"] += 1
        h = len(w)
        ms = lift_profile(w)
        tail = list(vals[1:])                 # X ... Z, length h+1
        rev = list(reversed(tail))            # V_0 = Z ... V_h = X
        U = [rev[ell] * p2(-ms[ell]) for ell in range(h + 1)]
        if U[0] != Z:
            t["u_zero_not_the_endpoint"] += 1
        if ms[h] == 0:
            t["zero_lift_bridges"] += 1
            if U[h] != X:
                t["u_h_not_the_source_on_a_zero_lift_bridge"] += 1
        for ell in range(h):
            t["steps"] += 1
            q = w[h - 1 - ell]
            # the plain reverse recursion, from the forward map
            if 3 * rev[ell + 1] + 1 != (1 << q) * rev[ell]:
                t["reverse_recursion_violations"] += 1
            a = mech_a(ell + 1)
            # Theorem 12.1: the exponent rewritten through the lift increment
            if rev[ell + 1] != (p2(a + ms[ell + 1] - ms[ell]) * rev[ell]
                                - 1) / 3:
                t["lifted_cocycle_theorem_12_1_violations"] += 1
            # Theorem 12.2
            if U[ell + 1] != ((1 << a) * U[ell]
                              - p2(-ms[ell + 1])) / 3:
                t["normalized_cocycle_theorem_12_2_violations"] += 1
            # Theorem 13.1, and the fact it reduces to
            if rev[ell] % 3 not in (1, 2):
                t["reverse_state_outside_one_or_two_mod_three"] += 1
            pi = 0 if rev[ell] % 3 == 1 else 1
            if (a + ms[ell + 1] - ms[ell]) % 2 != pi:
                t["residue_parity_theorem_13_1_violations"] += 1
            if q % 2 != pi:
                t["residue_parity_not_equal_to_the_valuation_parity"] += 1
        # the closed form of section 12
        eh = two_pow_eps(h)
        acc = sum(eh / two_pow_eps(ell) * p2(-ms[ell])
                  for ell in range(1, h + 1))
        if U[h] != eh * Z - acc / 3:
            t["closed_form_violations"] += 1
        for ell in range(1, h + 1):
            wgt = eh / two_pow_eps(ell)
            if not Fraction(1, 2) < wgt < 2:
                t["weight_outside_one_half_to_two"] += 1
    return t


# ---------------------------------------------------------------------------
# the zero-lift class
# ---------------------------------------------------------------------------

def check_zero_lift(limit: int, max_steps: int) -> dict:
    """Theorem 11.1 and Corollary 11.2, exactly.

    `P_down = (Z/X) 2^E` and `2^E = 2^{m_h} 2^{eps_h}`, so on a zero-lift
    bridge `P_down = (Z/X) 2^{ceil(beta h)}/3^h` is an exact rational and the
    bound `< 2` needs no floating point. The bundle floats the product first.
    """
    l2_lo, l2_hi = widen(*ln2_bracket(), 40)
    t: dict = {"zero_lift_bridges": 0, "positive_lift_bridges": 0,
               "excess_decomposition_violations": 0,
               "product_identity_violations": 0,
               "product_theorem_11_1_violations": 0,
               "reciprocal_mass_corollary_11_2_violations": 0,
               "reciprocal_mass_decided_by_the_float64_form": 0,
               "largest_product_seen": None,
               "largest_reciprocal_mass_seen": None,
               "reciprocal_ceiling": float(4 * l2_lo)}
    big_p, big_r = None, None
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        h, Q = len(w), sum(w)
        ms = lift_profile(w)
        if ms[h] != 0:
            t["positive_lift_bridges"] += 1
            continue
        t["zero_lift_bridges"] += 1
        # `E = m_h + eps_h` exponentiates to `2^E = 2^{m_h} 2^{eps_h}`, and
        # `2^E = 2^Q/3^h`. Testing `Q - ceil_beta(h) == 0` here would re-test
        # the condition that selected this branch; the decomposition is the
        # statement with content, and it is an exact rational one.
        if Fraction(1 << Q, 3 ** h) != p2(ms[h]) * two_pow_eps(h):
            t["excess_decomposition_violations"] += 1
        tail = list(vals[1:])
        prod = Fraction(1)
        for v in tail[:-1]:
            prod *= Fraction(3 * v + 1, 3 * v)
        # the identity the theorem rests on, checked rather than assumed
        if prod != Fraction(Z, X) * two_pow_eps(h):
            t["product_identity_violations"] += 1
        if not prod < 2:
            t["product_theorem_11_1_violations"] += 1
        if big_p is None or prod > big_p:
            big_p = prod
        recip = sum(Fraction(1, v) for v in tail[:-1])
        if not recip < 4 * l2_lo:
            t["reciprocal_mass_corollary_11_2_violations"] += 1
        # the bundle compares a float64 sum against 4*log(2)+1e-12
        f = sum(1.0 / v for v in tail[:-1])
        if (f < 4 * math.log(2) + 1e-12) != (recip < 4 * l2_hi):
            t["reciprocal_mass_decided_by_the_float64_form"] += 1
        if big_r is None or recip > big_r:
            big_r = recip
    t["largest_product_seen"] = None if big_p is None else float(big_p)
    t["largest_reciprocal_mass_seen"] = None if big_r is None else float(big_r)
    return t


# ---------------------------------------------------------------------------
# Theorem 14.1's countermodel, rebuilt
# ---------------------------------------------------------------------------

def check_abstract(lengths: tuple[int, ...] = (128, 256, 512, 1024, 2048, 4096)
                   ) -> dict:
    t: dict = {"levels": 0, "constructions_that_failed_their_precondition": 0,
               "lift_not_starting_at_zero": 0, "lift_not_ending_at_zero": 0,
               "lift_negative": 0, "valuation_outside_one_to_three": 0,
               "total_valuation_not_the_ceiling": 0,
               "laplace_mass_at_or_above_six": 0,
               "rise_mass_at_or_above_one": 0,
               "plateau_mass_at_or_above_one_over_h": 0,
               "descent_mass_at_or_above_four": 0,
               "a_height_held_more_than_twice_in_the_descent": 0,
               "rows": []}
    for h in lengths:
        t["levels"] += 1
        a, m, q, mass, M = abstract_zero_lift(h)
        if not m:
            t["constructions_that_failed_their_precondition"] += 1
            continue
        if m[0] != 0:
            t["lift_not_starting_at_zero"] += 1
        if m[h] != 0:
            t["lift_not_ending_at_zero"] += 1
        if any(x < 0 for x in m):
            t["lift_negative"] += 1
        if any(not 1 <= x <= 3 for x in q):
            t["valuation_outside_one_to_three"] += 1
        if sum(q) != ceil_beta(h):
            t["total_valuation_not_the_ceiling"] += 1
        if not mass < 6:
            t["laplace_mass_at_or_above_six"] += 1
        # The paper's proof splits the mass three ways, and each part carries
        # its own bound: rise < 1, plateau = O(h 2^-M) < 1/h, descent < 4
        # because no height is held more than twice. Checking only the total
        # would let two of the three be wrong in compensating directions.
        rise = sum(p2(-m[ell]) for ell in range(1, M + 1))
        first_descent = next(ell for ell in range(M + 1, h + 1)
                             if m[ell] < M) if any(
                                 m[ell] < M for ell in range(M + 1, h + 1)) else h + 1
        plateau = sum(p2(-m[ell])
                      for ell in range(M + 1, first_descent))
        descent = sum(p2(-m[ell])
                      for ell in range(first_descent, h + 1))
        if not rise < 1:
            t["rise_mass_at_or_above_one"] += 1
        if not plateau < Fraction(1, h):
            t["plateau_mass_at_or_above_one_over_h"] += 1
        if not descent < 4:
            t["descent_mass_at_or_above_four"] += 1
        held: dict[int, int] = {}
        for ell in range(first_descent, h + 1):
            held[m[ell]] = held.get(m[ell], 0) + 1
        if any(v > 2 for v in held.values()):
            t["a_height_held_more_than_twice_in_the_descent"] += 1
        t["rows"].append({"h": h, "M": M, "max_q": max(q),
                          "lift_sum": float(mass),
                          "rise": float(rise), "plateau": float(plateau),
                          "descent": float(descent)})
    return t


# ---------------------------------------------------------------------------
# the two synthetic blocks in the shipped checker
# ---------------------------------------------------------------------------

def check_their_algebra() -> dict:
    """Two of the bundle's twelve counters test a quantity against itself.

    `near_linear_gap_algebra` asserts `lower > 0` where `lower = N/(R+1)`,
    `N >= 10^6`, `R >= 1`. No admissible input can make that false, and the
    exponent statement the block is named for is never evaluated.

    `positive_lift_drop_algebra` asserts `drop >= 2 - beta - 1e-15` where
    `drop = (m + eps) - (beta - 1)`. Subtract the two sides and `beta`
    cancels, leaving `m + eps >= 1 - 1e-15` with `m >= 1` an integer. This is
    demonstrated, not asserted: the difference is evaluated with beta at BOTH
    ends of a certified bracket, and the two results must be identical --
    which is exactly what it means for beta not to participate.
    """
    b_lo, b_hi = beta_lo(), beta_hi()
    t: dict = {"near_linear_samples": 0,
               "near_linear_samples_that_could_have_failed": 0,
               "near_linear_smallest_left_side": None,
               "drop_samples": 0,
               "drop_samples_that_could_have_failed": 0,
               "drop_difference_depends_on_beta": 0,
               "drop_smallest_margin": None}
    smallest = None
    # their range: N in [10^6, 10^12), eta in [0, 0.2), R = max(1, N^eta)
    for i in range(10000):
        n = 10 ** 6 + (i * 7919) % (10 ** 12 - 10 ** 6)
        eta = (i % 200) / 1000.0
        r = max(1, int(n ** eta))
        t["near_linear_samples"] += 1
        low = Fraction(n, r + 1)
        if not low > 0:
            t["near_linear_samples_that_could_have_failed"] += 1
        if smallest is None or low < smallest:
            smallest = low
    t["near_linear_smallest_left_side"] = float(smallest)

    # their range: m in [1,20], eps in [0,1)
    tight = None
    for i in range(10000):
        m = 1 + (i % 20)
        eps = Fraction(i % 997, 997)
        # Evaluate the SAME expression with beta at each end of a certified
        # bracket. If the two agree the parameter does not participate, which
        # is what "beta cancels" means operationally.
        at_lo = ((m + eps) - (b_lo - 1)) - (2 - b_lo)
        at_hi = ((m + eps) - (b_hi - 1)) - (2 - b_hi)
        t["drop_samples"] += 1
        if at_lo != at_hi:
            t["drop_difference_depends_on_beta"] += 1
        if not at_lo >= -Fraction(1, 10 ** 15):
            t["drop_samples_that_could_have_failed"] += 1
        if tight is None or at_lo < tight:
            tight = at_lo
    t["drop_smallest_margin"] = float(tight)
    return t


# ---------------------------------------------------------------------------
# first-spike cylinder
# ---------------------------------------------------------------------------

def check_first_spike(limit: int, window: int = 60,
                      lam: Fraction = Fraction(1, 10)) -> dict:
    """Section 16, with `2^{delta_v-delta_s} = 3^{v-s}/2^{K_v-K_s}` again."""
    a, b = lam.numerator, lam.denominator
    t: dict = {"orbits": 0, "first_hits": 0,
               "first_hit_below_the_threshold": 0,
               "first_hit_not_minimal": 0,
               "overshoot_above_one_step": 0,
               "length_bound_violations": 0,
               "length_bound_attained_with_no_additive_constant": 0,
               "prefix_valuation_below_the_length": 0,
               "source_inside_its_cylinder": 0,
               "source_outside_its_cylinder": 0,
               "endpoint_inside_its_cylinder": 0,
               "endpoint_outside_its_cylinder": 0}
    for y0 in range(7, limit + 1, 2):
        if y0 % 3 == 0:
            continue
        word, values = accelerated(y0, max_steps=window)
        if len(word) < 3:
            continue
        t["orbits"] += 1
        K = cumulative(word)
        thresh = Fraction(y0 ** a)
        for v in range(1, len(word) + 1):
            if Fraction(3 ** v, 1 << K[v]) ** b >= thresh:
                break
        else:
            continue
        t["first_hits"] += 1
        ell, dK = v, K[v]
        cur = Fraction(3 ** ell, 1 << dK)
        if not cur ** b >= thresh:
            t["first_hit_below_the_threshold"] += 1
        if ell >= 1 and Fraction(3 ** (ell - 1), 1 << K[ell - 1]) ** b >= thresh:
            t["first_hit_not_minimal"] += 1
        if not cur ** b < Fraction(3, 2) ** b * thresh:
            t["overshoot_above_one_step"] += 1
        if not dK >= ell:
            t["length_bound_violations"] += 1
        if dK == ell:
            t["length_bound_attained_with_no_additive_constant"] += 1
        P = sum(word[:ell])
        if not P >= ell:
            t["prefix_valuation_below_the_length"] += 1
        if values[0] < (1 << (P + 1)):
            t["source_inside_its_cylinder"] += 1
        else:
            t["source_outside_its_cylinder"] += 1
        if values[ell] < 3 ** ell:
            t["endpoint_inside_its_cylinder"] += 1
        else:
            t["endpoint_outside_its_cylinder"] += 1
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"examples": 0, "x_disagreeing": 0, "z_disagreeing": 0,
               "exponent_word_disagreeing": 0, "h_disagreeing": 0,
               "total_lift_disagreeing": 0, "max_lift_disagreeing": 0,
               "lift_sum_disagreeing": 0,
               "tail_product_disagreeing": 0,
               "reciprocal_mass_disagreeing": 0,
               "tail_not_suffix_supercritical": 0,
               "sources_appearing_more_than_once": 0,
               "rows": []}
    seen: dict[int, int] = {}
    for ex in report.get("zero_lift_finite_examples", []):
        t["examples"] += 1
        y = ex["y"]
        seen[y] = seen.get(y, 0) + 1
        vals, qs, cur = [y], [], y
        for _ in range(60):
            cur, q = step(cur)
            vals.append(cur)
            qs.append(q)
            if cur == ex["Z"] and len(qs) >= 2:
                break
        X, Z, w = vals[1], vals[-1], tuple(qs[1:])
        if X != ex["X"]:
            t["x_disagreeing"] += 1
        if Z != ex["Z"]:
            t["z_disagreeing"] += 1
        if list(w) != list(ex["tail_code"]):
            t["exponent_word_disagreeing"] += 1
        if len(w) != ex["h"]:
            t["h_disagreeing"] += 1
        if not suffix_supercritical(w):
            t["tail_not_suffix_supercritical"] += 1
        h = len(w)
        ms = lift_profile(w)
        if ms[h] != ex["integer_lift_total"]:
            t["total_lift_disagreeing"] += 1
        if max(ms) != ex["max_lift"]:
            t["max_lift_disagreeing"] += 1
        mass = sum(p2(-m) for m in ms[1:])
        if float(mass) != ex["lift_sum"]:
            t["lift_sum_disagreeing"] += 1
        tail = vals[1:]
        prod = Fraction(1)
        for v in tail[:-1]:
            prod *= Fraction(3 * v + 1, 3 * v)
        if float(prod) != ex["tail_product"]:
            t["tail_product_disagreeing"] += 1
        recip = sum(Fraction(1, v) for v in tail[:-1])
        if float(recip) != ex["reciprocal_mass"]:
            t["reciprocal_mass_disagreeing"] += 1
        t["rows"].append({"y": y, "X": X, "Z": Z, "h": h, "word": list(w),
                          "lift_profile": ms[1:], "lift_sum": str(mass),
                          "product": rational_digits(prod, 9)})
    t["sources_appearing_more_than_once"] = sum(1 for v in seen.values() if v > 1)
    return t


def check_countermodels(report: dict, mine: dict) -> dict:
    t: dict = {"rows_published": 0, "rows_i_rebuilt": 0,
               "h_disagreeing": 0, "m_disagreeing": 0,
               "max_q_disagreeing": 0, "lift_sum_disagreeing": 0}
    ours = {r["h"]: r for r in mine["rows"]}
    for row in report.get("abstract_height_only_countermodels", []):
        t["rows_published"] += 1
        r = ours.get(row["h"])
        if r is None:
            t["h_disagreeing"] += 1
            continue
        t["rows_i_rebuilt"] += 1
        if r["M"] != row["M"]:
            t["m_disagreeing"] += 1
        if r["max_q"] != row["max_q"]:
            t["max_q_disagreeing"] += 1
        if r["lift_sum"] != row["lift_sum"]:
            t["lift_sum_disagreeing"] += 1
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
               "validation_digest_mismatches": 0,
               "validation_size_mismatches": 0,
               "files_absent_from_the_validation_record": [],
               "duplicate_file_pairs": []}
    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    t["files_present"] = len(present)
    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()
              for n in present}
    listed: dict[str, str] = {}
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
    by_digest: dict[str, list[str]] = {}
    for n, d in actual.items():
        by_digest.setdefault(d, []).append(n)
    t["duplicate_file_pairs"] = [sorted(v) for v in by_digest.values()
                                 if len(v) > 1]
    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = val.get("files", val.get("source_files", {}))
    with_digest = set()
    if isinstance(files, dict):
        for n, r in files.items():
            t["validation_per_file_entries"] += 1
            if isinstance(r, dict) and "sha256" in r:
                t["validation_entries_with_a_digest"] += 1
                with_digest.add(n)
                if n in actual and actual[n] != r["sha256"]:
                    t["validation_digest_mismatches"] += 1
            size = (r or {}).get("bytes", (r or {}).get("size_bytes"))
            if size is not None and n in present:
                if (bundle / n).stat().st_size != size:
                    t["validation_size_mismatches"] += 1
    named = set(files) | set(val.get("json_parse", {}) or {})
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in named]
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_all_ok_flag"] = val.get("all_ok")
    t["validation_top_level_keys"] = sorted(val)
    t["validation_json_parse_entries"] = len(val.get("json_parse", {}) or {})
    t["validation_json_parse_not_true"] = sum(
        1 for v in (val.get("json_parse", {}) or {}).values() if v is not True)
    t["validation_python_compile_flag"] = val.get("python_compile")
    t["validation_file_ok_flags_not_true"] = sum(
        1 for r in files.values()
        if isinstance(r, dict) and r.get("ok") is not True)
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    t: dict = {"paper_proved_items": 0, "ledger_proved_items": 0,
               "paper_open_items": 0, "ledger_open_items": 0,
               "paper_no_go_headings": 0,
               "paper_no_go_headings_in_section_18": 0,
               "ledger_no_go_items": 0,
               "ledger_has_an_open_key": False,
               "open_items_absent_from_the_ledger": [],
               "no_go_headings_absent_from_the_ledger": [],
               "heuristic_failed_its_positive_control": 0,
               "heuristic_failed_its_negative_control": 0}
    proved = re.search(r"## 22\.1(.*?)## 22\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(
            re.findall(r"^\d+\. ", proved.group(1), re.M))
    openb = re.search(r"## 22\.4(.*?)(?:\n---|\Z)", paper, re.S)
    bullets = []
    if openb:
        bullets = [b.strip(" -;.") for b in
                   re.findall(r"^- (.+)$", openb.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
    # every NO-GO heading in the paper, not only section 18's: two of them
    # live in sections 6 and 14, and a regex anchored on "18." would miss them
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    t["paper_no_go_headings_in_section_18"] = sum(
        1 for n, _ in no_go if n.startswith("18."))
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
        hit = sum(1 for w in words if w[:7] in blob)
        return hit >= max(1, len(words) // 2)

    t["open_items_absent_from_the_ledger"] = [b for b in bullets
                                              if not covered(b)]
    t["no_go_headings_absent_from_the_ledger"] = [
        n for n, h in no_go if not covered(h)]
    present_text = " ".join(str(x) for x in
                            (ledger.get(proved_key, []) or [""])[:1])
    t["heuristic_failed_its_positive_control"] = int(
        bool(present_text) and not covered(present_text))
    t["heuristic_failed_its_negative_control"] = int(
        covered("quokka bandersnatch flimflam zeppelin marzipan"))
    return t


def check_their_claims(report: dict, res: dict) -> dict:
    lf, bu, co = res["lift"], res["budget"], res["cocycle"]
    mine = {
        "finite_local_bridges": lf["bridges"],
        "rank_one_record_ratio": lf["bridges"],
        "lift_profile_nonnegative": lf["bridges"],
        "lift_recurrence_exact": lf["profile_positions"],
        "lift_laplace_budget": bu["bridges"],
        "mechanical_cocycle_exact": co["steps"],
        "zero_lift_constant_product": res["zero_lift"]["zero_lift_bridges"],
        "zero_lift_harmonic_bound": res["zero_lift"]["zero_lift_bridges"],
        "canonical_collapse_cases": res["collapse"]["both_inside_their_moduli"],
        "abstract_bounded_q_lift_excursions": res["abstract"]["levels"],
        "near_linear_gap_algebra": res["their_algebra"]["near_linear_samples"],
        "positive_lift_drop_algebra": res["their_algebra"]["drop_samples"],
    }
    rows = [{"check": k, "theirs": v, "mine": mine.get(k)}
            for k, v in report.get("checks", {}).items()]
    return {"rows": rows,
            "checks_i_did_not_reproduce": sum(1 for r in rows
                                              if r["mine"] is None),
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "counts_i_reproduce_exactly": sum(
                1 for r in rows if r["mine"] is not None
                and r["mine"] == r["theirs"])}


def check_collapse(limit: int, max_steps: int) -> dict:
    """A-U.2d.17's collapse, carried forward so their count can be matched."""
    t: dict = {"bridges": 0, "source_inside_its_modulus": 0,
               "endpoint_inside_its_modulus": 0, "both_inside_their_moduli": 0,
               "source_congruence_violations": 0,
               "endpoint_congruence_violations": 0,
               "collapse_violations": 0}
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        t["bridges"] += 1
        h, Q = len(w), sum(w)
        B = b_of(w)
        m2, m3 = 1 << (Q + 1), 3 ** h
        r2 = ((1 << Q) - B) * pow(3 ** h, -1, m2) % m2
        r3 = B * pow(1 << Q, -1, m3) % m3
        if (X - r2) % m2:
            t["source_congruence_violations"] += 1
        if (Z - r3) % m3:
            t["endpoint_congruence_violations"] += 1
        a, b = X < m2, Z < m3
        t["source_inside_its_modulus"] += int(a)
        t["endpoint_inside_its_modulus"] += int(b)
        if a and b:
            t["both_inside_their_moduli"] += 1
            if r2 != X or r3 != Z:
                t["collapse_violations"] += 1
    return t


SECTIONS = ("instrument", "ceiling", "constants", "lift", "budget",
            "cocycle", "zero_lift", "abstract", "their_algebra",
            "first_spike", "examples", "countermodels", "collapse",
            "artifacts", "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("ceiling", "float_ceiling_disagreements"),
    ("ceiling", "fixed_point_undecided"),
    ("ceiling", "fixed_point_disagreeing_with_the_exact_route"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("constants", "frontier_and_report_disagreeing"),
    ("lift", "rank_one_upper_violations"),
    ("lift", "rank_one_lower_violations"),
    ("lift", "left_record_not_below_the_endpoint"),
    ("lift", "source_not_three_y_plus_one_over_two"),
    ("lift", "lift_negative"),
    ("lift", "lift_nonnegative_disagreeing_with_supercriticality"),
    ("lift", "slack_decomposition_violations"),
    ("lift", "recurrence_theorem_8_1_violations"),
    ("lift", "lift_descends_by_more_than_one"),
    ("lift", "lift_descends_at_a_mechanical_one"),
    ("lift", "total_lift_not_q_minus_ceil_beta_h"),
    ("budget", "reindexing_violations"),
    ("budget", "laplace_identity_violations"),
    ("budget", "budget_theorem_9_1_violations"),
    ("budget", "budget_is_not_within_a_factor_two_of_the_identity"),
    ("budget", "quantile_violations"),
    ("budget", "sharp_quantile_violations"),
    ("cocycle", "reverse_recursion_violations"),
    ("cocycle", "lifted_cocycle_theorem_12_1_violations"),
    ("cocycle", "normalized_cocycle_theorem_12_2_violations"),
    ("cocycle", "closed_form_violations"),
    ("cocycle", "weight_outside_one_half_to_two"),
    ("cocycle", "u_zero_not_the_endpoint"),
    ("cocycle", "u_h_not_the_source_on_a_zero_lift_bridge"),
    ("cocycle", "residue_parity_theorem_13_1_violations"),
    ("cocycle", "residue_parity_not_equal_to_the_valuation_parity"),
    ("cocycle", "reverse_state_outside_one_or_two_mod_three"),
    ("zero_lift", "excess_decomposition_violations"),
    ("zero_lift", "product_identity_violations"),
    ("zero_lift", "product_theorem_11_1_violations"),
    ("zero_lift", "reciprocal_mass_corollary_11_2_violations"),
    ("abstract", "constructions_that_failed_their_precondition"),
    ("abstract", "lift_not_starting_at_zero"),
    ("abstract", "lift_not_ending_at_zero"),
    ("abstract", "lift_negative"),
    ("abstract", "valuation_outside_one_to_three"),
    ("abstract", "total_valuation_not_the_ceiling"),
    ("abstract", "laplace_mass_at_or_above_six"),
    ("abstract", "rise_mass_at_or_above_one"),
    ("abstract", "plateau_mass_at_or_above_one_over_h"),
    ("abstract", "descent_mass_at_or_above_four"),
    ("abstract", "a_height_held_more_than_twice_in_the_descent"),
    ("their_algebra", "drop_difference_depends_on_beta"),
    ("first_spike", "first_hit_below_the_threshold"),
    ("first_spike", "first_hit_not_minimal"),
    ("first_spike", "overshoot_above_one_step"),
    ("first_spike", "length_bound_violations"),
    ("first_spike", "prefix_valuation_below_the_length"),
    ("examples", "x_disagreeing"),
    ("examples", "z_disagreeing"),
    ("examples", "exponent_word_disagreeing"),
    ("examples", "h_disagreeing"),
    ("examples", "total_lift_disagreeing"),
    ("examples", "max_lift_disagreeing"),
    ("examples", "lift_sum_disagreeing"),
    ("examples", "tail_product_disagreeing"),
    ("examples", "reciprocal_mass_disagreeing"),
    ("examples", "tail_not_suffix_supercritical"),
    ("countermodels", "h_disagreeing"),
    ("countermodels", "m_disagreeing"),
    ("countermodels", "max_q_disagreeing"),
    ("countermodels", "lift_sum_disagreeing"),
    ("collapse", "source_congruence_violations"),
    ("collapse", "endpoint_congruence_violations"),
    ("collapse", "collapse_violations"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_digest_mismatches"),
    ("artifacts", "validation_size_mismatches"),
    ("artifacts", "validation_json_parse_not_true"),
    ("artifacts", "validation_file_ok_flags_not_true"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("ceiling", "levels"),
    ("ceiling", "exact_levels_cross_checked"),
    ("constants", "constants_checked"),
    ("lift", "bridges"),
    ("lift", "profile_positions"),
    ("lift", "descents_seen"),
    ("lift", "largest_interior_lift"),
    ("budget", "bridges"),
    ("budget", "quantile_instances"),
    ("cocycle", "bridges"),
    ("cocycle", "steps"),
    ("cocycle", "zero_lift_bridges"),
    ("zero_lift", "zero_lift_bridges"),
    ("abstract", "levels"),
    ("their_algebra", "near_linear_samples"),
    ("their_algebra", "drop_samples"),
    ("first_spike", "orbits"),
    ("first_spike", "first_hits"),
    ("examples", "examples"),
    ("countermodels", "rows_published"),
    ("countermodels", "rows_i_rebuilt"),
    ("collapse", "bridges"),
    ("collapse", "both_inside_their_moduli"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("ceiling", "closest_approach_level"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("lift", "sources"),
    ("lift", "longest_tail"),
    ("lift", "zero_total_lift"),
    ("lift", "positive_total_lift"),
    ("budget", "quantile_instances_that_are_not_vacuous"),
    ("budget", "sharp_quantile_instances_that_are_not_vacuous"),
    ("zero_lift", "positive_lift_bridges"),
    ("zero_lift", "reciprocal_mass_decided_by_the_float64_form"),
    ("their_algebra", "near_linear_samples_that_could_have_failed"),
    ("their_algebra", "drop_samples_that_could_have_failed"),
    ("first_spike", "length_bound_attained_with_no_additive_constant"),
    ("first_spike", "source_inside_its_cylinder"),
    ("first_spike", "source_outside_its_cylinder"),
    ("first_spike", "endpoint_inside_its_cylinder"),
    ("first_spike", "endpoint_outside_its_cylinder"),
    ("examples", "sources_appearing_more_than_once"),
    ("collapse", "source_inside_its_modulus"),
    ("collapse", "endpoint_inside_its_modulus"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
    ("artifacts", "validation_entries_with_a_digest"),
    ("artifacts", "validation_json_parse_entries"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "paper_no_go_headings_in_section_18"),
    ("ledger", "ledger_no_go_items"),
    ("their_claims", "checks_i_did_not_reproduce"),
    ("their_claims", "checks_they_report_as_zero"),
    ("their_claims", "counts_i_reproduce_exactly"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=35000)
    ap.add_argument("--max-steps", type=int, default=44)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    res: dict = {}
    errors: dict = {"%s_raised" % s: 0 for s in SECTIONS}
    errors["messages"] = []

    def run(name: str, fn):
        """A section that raises has no verdict, so the drill would score a
        defect reaching it as malformed and the hole would stay invisible.
        Turn any internal exception into a named failure counter instead."""
        try:
            res[name] = fn()
        except Exception as exc:                        # noqa: BLE001
            res[name] = {}
            errors["%s_raised" % name] = 1
            errors["messages"].append("%s: %s: %s"
                                      % (name, type(exc).__name__, exc))

    run("instrument", check_instrument)
    run("ceiling", check_float_ceiling)
    run("constants", lambda: check_constants(frontier, report))
    run("lift", lambda: check_lift(a.limit, a.max_steps))
    run("budget", lambda: check_budget(a.limit, a.max_steps))
    run("cocycle", lambda: check_cocycle(a.limit, a.max_steps))
    run("zero_lift", lambda: check_zero_lift(a.limit, a.max_steps))
    run("abstract", check_abstract)
    run("their_algebra", check_their_algebra)
    run("first_spike", lambda: check_first_spike(min(a.limit, 4000)))
    run("examples", lambda: check_examples(report))
    run("countermodels", lambda: check_countermodels(report, res["abstract"]))
    run("collapse", lambda: check_collapse(a.limit, a.max_steps))
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
        "run": "RUN-046", "round": "A-U.2d.18", "bundle": str(bundle),
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
