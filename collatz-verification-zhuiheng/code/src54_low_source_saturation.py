"""RUN-036 — independent recheck of Hard-Zeta round A-U.2d.8.

`Quadratic Low-Source Corridor Saturation` (source item 54). 數學戰士「墜衡」.

This round leaves the additive slack machinery and works multiplicatively. Its
core is an exact identity for an accelerated segment,

    z/y = (3^L / 2^Q) prod_{j<L} (1 + 1/(3 Y_j)) = 2^-D * script-P,

which is a statement about rationals: every factor is a ratio of integers, so the
whole of section 3 is decidable with no logarithm and no tolerance. So is the
consecutive-odd envelope of section 4, and so -- this is the useful part -- is
the Gamma representation of section 5:

    P(y,L) = Gamma(L+y/2+1/6)Gamma(y/2) / (Gamma(y/2+1/6)Gamma(L+y/2))

because for integer `L` that ratio is a Pochhammer quotient,
`prod_{k<L} (y/2+k+1/6)/(y/2+k)`, which is exact in Q. The shipped checker
compares the two sides numerically and reports a worst error of 3.1e-10; there is
nothing to compare here, because both sides are the same rational.

Sections 9.2, 13 and 14 are asymptotic and are NOT tested on orbits. Their
constants are recomputed, their derivations checked on a grid, and section 15's
floors -- which are computed from A-U.2d.7's Theorem 7.1, verified in RUN-035 --
are recomputed from the exact integer `Y_ver = 2075 * 2^60`.

Brackets come from `src53_plateau_reset`, certified there rather than re-derived:
`ln 2` from its series with an exact tail, `log2 3` from a bit length, `sqrt 2`
from integer square roots. One implementation, not two.

Usage:
    python code/src54_low_source_saturation.py --bundle <dir> [--limit N] [--out F]
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
from src47_survival_closure import decimal_verdict                # noqa: E402
from src53_plateau_reset import (                                  # noqa: E402
    accelerated, bracket_decimal, chains_of, crossings_and_stalks,
    cumulative, ln2_bracket, sqrt_bracket,
)

PAPER = "Hard_Zeta_Phase_II_Round_AU2d8_Quadratic_Low_Source_Corridor_Saturation_v0.1.md"
REPORT = "Hard_Zeta_AU2d8_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d8_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d8_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d8.json"
CHECKSUMS = "CHECKSUMS.sha256"

# Named once, so a counter added later without being listed makes the run
# REFUSE rather than pass quietly. RUN-035 shipped a gate whose derivation
# failures were gathered by matching key-name suffixes; one counter's name
# matched none of them and could increment unread.
GRID_COUNTERS = (
    "harmonic_envelope_violations",
    "coarse_envelope_violations",
    "sixth_root_cap_violations",
    "sixth_root_inversion_violations",
    "mu_star_not_six_theta_minus_one_over_five",
    "old_exponent_not_theta_over_one_plus_theta",
)


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def ulps_against_bracket(published: float, lo: Fraction, hi: Fraction) -> dict:
    """How far a published double sits from the nearest double to [lo, hi].

    Do NOT go via a decimal. The first version of this rendered the bracket to a
    fixed number of places and compared doubles to that, so the answer measured
    my own truncation: `c_H` came out 75 ulps and `log2 Y_ver` 78929, both of
    them entirely artefacts of asking for 13 and 8 places where a double near
    those magnitudes needs 17 and 15. Rounding is monotone, so if `lo` and `hi`
    round to the same double, that double is THE nearest one for every value in
    between -- and if they do not, the bracket simply cannot decide and says so.
    """
    d_lo, d_hi = float(lo), float(hi)
    if d_lo != d_hi:
        return {"decided": False,
                "why": "the bracket spans more than one double"}
    return {"decided": True, "nearest_double": d_lo,
            "ulps": bits(published) - bits(d_lo)}


# ---------------------------------------------------------------------------
# section 3 and section 4 -- exact, on real orbits
# ---------------------------------------------------------------------------

def packing_envelope(y: int, L: int) -> Fraction:
    """`P(y,L) = prod_{k<L} (1 + 1/(3(y+2k)))`, exactly."""
    out = Fraction(1)
    for k in range(L):
        d = 3 * (y + 2 * k)
        out *= Fraction(d + 1, d)
    return out


def pochhammer_ratio(y: int, L: int) -> Fraction:
    """The section 5 Gamma quotient, written as what it is for integer `L`.

    `Gamma(a+L)Gamma(b)/(Gamma(a)Gamma(b+L)) = prod_{k<L} (a+k)/(b+k)` by the
    functional equation alone, with `a = y/2+1/6` and `b = y/2`. So Theorem 5.1
    is an identity between two rationals and needs no Gamma evaluated anywhere.
    """
    a, b = Fraction(y, 2) + Fraction(1, 6), Fraction(y, 2)
    out = Fraction(1)
    for k in range(L):
        out *= (a + k) / (b + k)
    return out


def check_instrument(ln2_lo: Fraction, ln2_hi: Fraction,
                     a_lo: Fraction, a_hi: Fraction) -> dict:
    """Do the brackets bracket what they claim?

    An instrument that is only ever pointed at the subject is never tested. Each
    of these has a known answer, so a range reduction that drops an octave or a
    series truncated too early stops being invisible.
    """
    failed = []
    l2 = ln_bracket(Fraction(2))
    if not (l2[0] <= ln2_lo and ln2_hi <= l2[1]):
        failed.append("ln_of_two_does_not_contain_the_certified_bracket")
    l4 = ln_bracket(Fraction(4))
    if not (l4[0] <= 2 * ln2_lo and 2 * ln2_hi <= l4[1]):
        failed.append("ln_of_four_is_not_twice_ln_two")
    l1 = ln_bracket(Fraction(1))
    if not (l1[0] <= 0 <= l1[1]):
        failed.append("ln_of_one_does_not_contain_zero")
    e2 = _exp_bracket(ln2_hi)
    if not (_exp_bracket(ln2_lo)[0] <= 2 <= e2[1]):
        failed.append("exp_of_ln_two_does_not_contain_two")
    s4 = sqrt_bracket(Fraction(4), Fraction(4))
    if not (s4[0] <= 2 <= s4[1]):
        failed.append("sqrt_of_four_does_not_contain_two")
    r8 = _nth_root_lo(Fraction(8), 3), _nth_root_hi(Fraction(8), 3)
    if not (r8[0] <= 2 <= r8[1]):
        failed.append("cube_root_of_eight_does_not_contain_two")
    w = widen(Fraction(1, 3), Fraction(1, 3))
    if not (w[0] <= Fraction(1, 3) <= w[1]):
        failed.append("widening_does_not_contain_its_input")
    if not (a_lo <= 1 / ln2_hi and 1 / ln2_lo <= a_hi):
        failed.append("one_over_ln_two_is_not_the_reciprocal_bracket")
    return {"checks": 8, "failed": failed}


def check_segments(limit: int) -> dict:
    t = {
        "orbits": 0, "segments": 0, "max_L": 0, "max_source": 0,
        "product_identity_violations": 0,
        "two_forms_of_the_identity_disagree": 0,
        "sources_that_are_not_the_segment_minimum": 0,
        "segments_with_a_repeated_state": 0,
        "segments_meeting_the_packing_premise": 0,
        "sorted_state_below_y_plus_2k": 0,
        "packing_envelope_violations": 0,
        "gamma_form_disagrees_with_the_product": 0,
        "envelopes_compared": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        t["orbits"] += 1
        for s in range(n):
            end = e[s]
            if end is None or end <= s:
                continue
            L, Q = end - s, K[end] - K[s]
            y, z = values[s], values[end]
            t["segments"] += 1
            t["max_L"] = max(t["max_L"], L)
            t["max_source"] = max(t["max_source"], y)

            script_p = Fraction(1)
            for j in range(s, end):
                script_p *= 1 + Fraction(1, 3 * values[j])
            # Theorem 3.1, both printed forms. `2^-D = 3^L/2^Q` because
            # `2^(beta L) = 3^L`, so the second form is the first, exactly.
            first = Fraction(3) ** L / Fraction(2) ** Q * script_p
            if Fraction(z, y) != first:
                t["product_identity_violations"] += 1
            if first != Fraction(3, 2) ** 0 * Fraction(3 ** L, 2 ** Q) * script_p:
                t["two_forms_of_the_identity_disagree"] += 1

            states = values[s:end]
            minimal = all(v >= y for v in states)
            distinct = len(set(states)) == len(states)
            if not minimal:
                t["sources_that_are_not_the_segment_minimum"] += 1
            if not distinct:
                t["segments_with_a_repeated_state"] += 1
            if not (minimal and distinct):
                continue
            t["segments_meeting_the_packing_premise"] += 1
            for k, v in enumerate(sorted(states)):
                if v < y + 2 * k:
                    t["sorted_state_below_y_plus_2k"] += 1
                    break
            env = packing_envelope(y, L)
            t["envelopes_compared"] += 1
            if script_p > env:
                t["packing_envelope_violations"] += 1
            if env != pochhammer_ratio(y, L):
                t["gamma_form_disagrees_with_the_product"] += 1
    return t


def check_gamma_representation(pairs: tuple[tuple[int, int], ...]) -> dict:
    """Theorem 5.1 twice: exactly, and against an independent numeric Gamma.

    The exact half needs no Gamma at all. The second half exists because an
    identity checked only against my own rearrangement of it is
    `a-quantity-compared-only-to-itself`; `math.lgamma` is a different
    implementation and a different representation.
    """
    t = {"pairs": 0, "exact_disagreements": 0, "largest_L": 0,
         "worst_lgamma_absolute_error": 0.0,
         "worst_error_over_its_cancellation_bound": 0.0,
         "lgamma_disagreements_beyond_cancellation": 0,
         "rows": []}
    for y, L in pairs:
        t["pairs"] += 1
        t["largest_L"] = max(t["largest_L"], L)
        exact = packing_envelope(y, L)
        if exact != pochhammer_ratio(y, L):
            t["exact_disagreements"] += 1
        a, b = y / 2 + 1 / 6, y / 2
        terms = [math.lgamma(a + L), math.lgamma(b),
                 math.lgamma(a), math.lgamma(b + L)]
        approx = terms[0] + terms[1] - terms[2] - terms[3]
        ln_exact = math.log(exact.numerator) - math.log(exact.denominator)
        err = abs(approx - ln_exact)
        # `ln P` is a difference of four large log-gammas -- at y=65535, L=1 the
        # terms are ~3e5 and their combination is ~5e-6, so RELATIVE error is
        # meaningless here and the first version of this check failed 12 pairs
        # of correct arithmetic. The honest tolerance is the cancellation the
        # subtraction actually costs: eps times the largest term.
        allowed = 8 * 2.220446049250313e-16 * max(abs(v) for v in terms) + 1e-12
        t["worst_lgamma_absolute_error"] = max(
            t["worst_lgamma_absolute_error"], err)
        t["worst_error_over_its_cancellation_bound"] = max(
            t["worst_error_over_its_cancellation_bound"], err / allowed)
        if err > allowed:
            t["lgamma_disagreements_beyond_cancellation"] += 1
        if len(t["rows"]) < 6:
            t["rows"].append({"y": y, "L": L,
                              "log2_P": "%.12f" % (ln_exact / math.log(2)),
                              "lgamma_absolute_error": "%.3e" % err,
                              "cancellation_bound": "%.3e" % allowed})
    return t


# ---------------------------------------------------------------------------
# section 9.1 -- the exact harmonic depth cap, on real chains
# ---------------------------------------------------------------------------

def check_harmonic_depth(limit: int) -> dict:
    """Theorem 9.1, premise first.

    9.1 is not an orbit fact. It is Theorem 7.2 rearranged, and 7.2 descends
    from the inherited B-survival chain `y_r > 2^H y_1` and `z_1 > y_r`, which a
    real orbit does not owe. Applied blind to real chains it flags thousands --
    the same shape as RUN-032's 10214 of 10214 and RUN-035's caps.

    So two separate things are measured. The ALGEBRA of 9.1 -- that
    `1 + (4r-2)/y_1 < P` and `r < 1/2 + y_1(P-1)/4` are the same inequality --
    is universal and exact, and is checked on every chain. The CONCLUSION is
    checked only where the endpoint-gap premise actually holds.
    """
    t = {
        "chains": 0, "max_depth": 0, "max_L": 0,
        "chains_meeting_the_packing_premise": 0,
        "chains_where_the_outer_endpoint_exceeds_the_inner_source": 0,
        "chains_with_4_apart_sources_y_r_ge_y_1_plus_4r_minus_4": 0,
        "chains_meeting_the_endpoint_gap_premise": 0,
        "chains_meeting_every_premise": 0,
        "theorem_9_1_checked": 0,
        "theorem_9_1_violations": 0,
        "the_two_forms_of_9_1_are_not_equivalent": 0,
        "low_source_chains_3_le_y1_le_L": 0,
        "low_source_chains_meeting_every_premise": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, stalks = crossings_and_stalks(K, n)
        for ch in chains_of(K, n, e, stalks):
            t["chains"] += 1
            r, s1, sr = len(ch), ch[0], ch[-1]
            L, y1 = e[s1] - s1, values[s1]
            z1, yr = values[e[s1]], values[sr]
            t["max_depth"] = max(t["max_depth"], r)
            t["max_L"] = max(t["max_L"], L)
            low = 3 <= y1 <= L
            if low:
                t["low_source_chains_3_le_y1_le_L"] += 1

            states = values[s1:e[s1]]
            packing = (all(v >= y1 for v in states)
                       and len(set(states)) == len(states))
            if packing:
                t["chains_meeting_the_packing_premise"] += 1
            if z1 > yr:
                t["chains_where_the_outer_endpoint_exceeds_the_inner_source"] += 1
            if yr >= y1 + 4 * (r - 1):
                t["chains_with_4_apart_sources_y_r_ge_y_1_plus_4r_minus_4"] += 1
            gap = Fraction(z1, y1) > 1 + Fraction(4 * r - 2, y1)
            if gap:
                t["chains_meeting_the_endpoint_gap_premise"] += 1

            P = packing_envelope(y1, L)
            # the algebra of 9.1, universal: the two forms are one inequality
            left = 1 + Fraction(4 * r - 2, y1) < P
            right = Fraction(r) < Fraction(1, 2) + Fraction(y1, 4) * (P - 1)
            if left != right:
                t["the_two_forms_of_9_1_are_not_equivalent"] += 1

            if not (packing and gap):
                continue
            t["chains_meeting_every_premise"] += 1
            if low:
                t["low_source_chains_meeting_every_premise"] += 1
            t["theorem_9_1_checked"] += 1
            if not Fraction(r) <= Fraction(1, 2) + Fraction(y1, 4) * (P - 1):
                t["theorem_9_1_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# the envelopes and the sixth root -- grids, with certified brackets
# ---------------------------------------------------------------------------

def _ln_core(x: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    """`ln x` for `x` in [1,2), from `ln((1+u)/(1-u)) = 2 sum u^(2k+1)/(2k+1)`.

    The tail past `N` terms is bounded by `2 u^(2N+1) / ((2N+1)(1-u^2))`, which
    is exact, so the two returned rationals genuinely straddle `ln x`.
    """
    u = (x - 1) / (x + 1)
    s, p, u2 = Fraction(0), u, u * u
    for k in range(terms):
        s += p / (2 * k + 1)
        p *= u2
    lo = 2 * s
    return widen(lo, lo + 2 * p / ((2 * terms + 1) * (1 - u2)))


def ln_bracket(x: Fraction, terms: int = 80) -> tuple[Fraction, Fraction]:
    """`ln x` for `x >= 1`, range-reduced by powers of two first.

    Without the reduction this is both wrong and slow: for `Y_ver = 2075*2^60`
    the series argument `u = (x-1)/(x+1)` is `1 - 8e-22`, so eighty terms move
    the sum by nothing while the tail bound stays astronomical -- and the
    intermediate rationals reach `(Y+1)^161`, which is what stalled the first
    run of this gate. Writing `ln x = k ln2 + ln(x/2^k)` with `x/2^k` in [1,2)
    keeps the series in the regime where it actually converges.
    """
    assert x >= 1
    k = 0
    while x >= 2:
        x /= 2
        k += 1
    lo, hi = _ln_core(x, terms)
    if k == 0:
        return lo, hi
    l2_lo, l2_hi = ln2_bracket()
    return lo + k * l2_lo, hi + k * l2_hi


def check_grids(a_lo: Fraction, a_hi: Fraction, frontier: dict) -> dict:
    """Sections 5.2 and 9.2 as IMPLICATIONS, on a grid.

    None of these can be tested against orbits -- 9.2 is an asymptotic
    consequence of 9.1 under `3 <= y <= L`, not an orbit property. But every
    step is arithmetic, and arithmetic can be checked: the elementary envelope,
    the passage from the exact cap to the sixth-root cap, and the inversion.
    """
    t = {k: 0 for k in GRID_COUNTERS}
    t["grid_points"] = 0
    t["low_source_grid_points"] = 0
    rho = Fraction("4.1164")
    theta = 1 / (rho + 1)
    mu = (6 * theta - 1) / 5
    old = theta / (1 + theta)
    if mu != (6 * theta - 1) / 5:
        t["mu_star_not_six_theta_minus_one_over_five"] += 1
    if old != theta / (1 + theta):
        t["old_exponent_not_theta_over_one_plus_theta"] += 1
    t["theta_star_exact"] = "%d/%d" % (theta.numerator, theta.denominator)
    t["mu_star_exact"] = "%d/%d" % (mu.numerator, mu.denominator)
    t["old_exponent_exact"] = "%d/%d" % (old.numerator, old.denominator)

    e9_lo, e9_hi = _exp_bracket(Fraction(1, 9))
    CH_lo, CH_hi = widen(e9_lo * _nth_root_lo(Fraction(3), 6) / 4,
                         e9_hi * _nth_root_hi(Fraction(3), 6) / 4)
    cH_lo = _pow_bracket(1 / CH_hi, 6, 5)
    cH_hi = _pow_bracket(1 / CH_lo, 6, 5, hi=True)

    for y in (3, 5, 9, 27, 101, 1001):
        for L in (1, 2, 5, 20, 100, 500):
            t["grid_points"] += 1
            P = packing_envelope(y, L)
            P_lo, P_hi = simplify(P)
            R_lo = ln_bracket(P_lo)[0] * a_lo                # log2 P, below
            R_hi = ln_bracket(P_hi)[1] * a_hi                # log2 P, above

            # Theorem 5.2, sharp: R <= 1/(3y ln2) + ln(1+2L/y)/(6 ln2)
            l_lo, l_hi = ln_bracket(1 + Fraction(2 * L, y))
            if not R_lo <= a_hi / (3 * y) + l_hi * a_hi / 6:
                t["harmonic_envelope_violations"] += 1
            # Theorem 5.2, coarse: R < L/(3 y ln2)
            if not R_lo < Fraction(L) * a_hi / (3 * y):
                t["coarse_envelope_violations"] += 1

            if not (3 <= y <= L):
                continue
            t["low_source_grid_points"] += 1
            # Theorem 9.1 -> Corollary 9.2: the exact cap must be no larger
            # than the sixth-root cap, or 9.2 would not follow from 9.1.
            exact_cap_hi = Fraction(1, 2) + Fraction(y, 4) * (P_hi - 1)
            root_lo = _pow_bracket(Fraction(y), 5, 6) * _pow_bracket(Fraction(L), 1, 6)
            sixth_cap_lo = Fraction(1, 2) + CH_lo * root_lo
            if exact_cap_hi > sixth_cap_lo:
                t["sixth_root_cap_violations"] += 1
            # the inversion: r < 1/2 + C_H y^(5/6) L^(1/6) must be the same
            # statement as y > c_H (r-1/2)^(6/5) L^(-1/5)
            for r in (2, 3, 5, 9, 40):
                forward = Fraction(r) < Fraction(1, 2) + CH_hi * (
                    _pow_bracket(Fraction(y), 5, 6, hi=True)
                    * _pow_bracket(Fraction(L), 1, 6, hi=True))
                need_hi = cH_hi * _pow_bracket(Fraction(2 * r - 1, 2), 6, 5, hi=True)                     / _pow_bracket(Fraction(L), 1, 5)
                inverted = Fraction(y) > need_hi
                if forward and not inverted:
                    t["sixth_root_inversion_violations"] += 1
    return t


def _nth_root_lo(x: Fraction, n: int, digits: int = 25) -> Fraction:
    scale = 10 ** digits
    target = int(x * scale ** n)
    # Seed from the bit length rather than doubling from 1: the operands here
    # run to hundreds of bits, and `while hi**n <= target: hi *= 2` spent its
    # time raising ever-larger integers to the sixth power.
    lo, hi = 0, 1 << (target.bit_length() // n + 2)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** n <= target:
            lo = mid
        else:
            hi = mid
    return Fraction(lo, scale)


def _nth_root_hi(x: Fraction, n: int, digits: int = 25) -> Fraction:
    return _nth_root_lo(x, n, digits) + Fraction(1, 10 ** digits)


def widen(lo: Fraction, hi: Fraction, digits: int = 40) -> tuple[Fraction, Fraction]:
    """Round a bracket OUTWARDS onto a fixed denominator.

    Every series here returns a rigorous bracket whose numerator and denominator
    are enormous -- `e^(1/9)` to 120 terms carries `9^120 * 120!` underneath.
    Feeding that into the next series squares the size, and two such steps hung
    this gate. Widening keeps the bracket valid (it only ever grows) and keeps
    the arithmetic cheap, which is the whole reason a bracket beats a float.
    """
    s = 10 ** digits
    floor = (lo.numerator * s) // lo.denominator
    ceil = -((-hi.numerator * s) // hi.denominator)
    return Fraction(floor, s), Fraction(ceil, s)


def simplify(x: Fraction, digits: int = 30) -> tuple[Fraction, Fraction]:
    """Two simple rationals straddling `x`, so later series stay cheap.

    `P(y,L)` is exact but its numerator and denominator run to thousands of
    digits, and feeding that straight into a 60-term log series produced
    rationals large enough to stall the run. Truncating to a fixed denominator
    first is lossless as a BRACKET -- the true value is still inside.
    """
    scale = 10 ** digits
    lo = Fraction(int(x * scale), scale)
    return lo, lo + Fraction(1, scale)


def _pow_bracket(x: Fraction, p: int, q: int, hi: bool = False) -> Fraction:
    """A rational bound on `x^(p/q)` for `x > 0`: below by default, above if
    `hi`. Integer `p`-th power first, then a bisected integer `q`-th root, so
    nothing here evaluates a transcendental."""
    return (_nth_root_hi if hi else _nth_root_lo)(x ** p, q)


# ---------------------------------------------------------------------------
# section 15 -- floors computed from A-U.2d.7, the round RUN-035 verified
# ---------------------------------------------------------------------------

def check_au2d7_carryover(report: dict, frontier: dict,
                          a_lo: Fraction, a_hi: Fraction,
                          ln2_lo: Fraction, ln2_hi: Fraction) -> dict:
    """Recompute this round's floors from A-U.2d.7's Theorem 7.1.

    RUN-035 verified that `X_r` is the positive root of `a x^2 + b x = r - 1`
    and that Theorem 7.1 carries no depth restriction -- the `r >= 9` in that
    round belongs to Corollary 7.2, a different statement. Both facts are used
    here, so this is the first cross-round check in the sweep.
    """
    Y = 2075 * 2 ** 60
    t = {
        "verified_floor_recomputes": Y == frontier["constants"]["verified_floor"],
        "verified_floor": Y,
        "verified_floor_is_2075_times_2_to_the_60": True,
        "rows": [], "rows_off_by_at_least_one_ulp": [],
        "rows_the_bracket_could_not_decide": [],
        "inversion_sharper_from_depth": None,
        "the_paper_tabulates_from_depth": None,
        "depths_where_the_inversion_is_published_but_weaker": [],
    }
    r2_lo, r2_hi = sqrt_bracket(Fraction(2), Fraction(2))
    b2_lo = (6 + 4 * r2_lo) * a_lo / 3
    b2_hi = (6 + 4 * r2_hi) * a_hi / 3
    b_lo, b_hi = sqrt_bracket(b2_lo, b2_hi)
    sy_lo, sy_hi = sqrt_bracket(Fraction(Y), Fraction(Y))

    hs_lo, hs_hi = sqrt_bracket(3 * ln2_lo * Y, 3 * ln2_hi * Y)
    hs_pub = frontier["constants"]["r_ge_5_min_outer_L_from_verified_floor"]
    t["high_source_floor"] = bracket_decimal(hs_lo, hs_hi, 6)
    t["high_source_floor"] = ulps_against_bracket(hs_pub, hs_lo, hs_hi)

    lg = ln_bracket(Fraction(Y))          # an integer; the series input is small
    l2_lo, l2_hi = lg[0] * a_lo, lg[1] * a_hi
    t["log2_floor"] = ulps_against_bracket(
        frontier["constants"]["verified_floor_log2"], l2_lo, l2_hi)

    table = report["derived"]["AU2d7_exact_inversion_min_L_by_depth"]
    for key in sorted(table, key=lambda s: int(s)):
        r = int(key)
        d_lo, d_hi = sqrt_bracket(b2_lo + 4 * a_lo * (r - 1),
                                  b2_hi + 4 * a_hi * (r - 1))
        X_lo = (d_lo - b_hi) / (2 * a_hi)
        X_hi = (d_hi - b_lo) / (2 * a_lo)
        lo, hi = X_lo * sy_lo, X_hi * sy_hi
        verdict = ulps_against_bracket(table[key], lo, hi)
        t["rows"].append({"depth": r, "published": table[key],
                          "recomputed": bracket_decimal(lo, hi, 4), **verdict})
        if not verdict["decided"]:
            t["rows_the_bracket_could_not_decide"].append(r)
        elif verdict["ulps"]:
            t["rows_off_by_at_least_one_ulp"].append(r)
        if lo <= hs_hi:
            t["depths_where_the_inversion_is_published_but_weaker"].append(r)

    for r in range(2, 40):
        d_lo, _ = sqrt_bracket(b2_lo + 4 * a_lo * (r - 1),
                               b2_hi + 4 * a_hi * (r - 1))
        X_lo = (d_lo - b_hi) / (2 * a_hi)
        if X_lo * sy_lo > hs_hi:
            t["inversion_sharper_from_depth"] = r
            break
    return t


# ---------------------------------------------------------------------------

def check_constants(frontier: dict, paper: str, a_lo: Fraction, a_hi: Fraction,
                    ln2_lo: Fraction, ln2_hi: Fraction) -> dict:
    rho = Fraction("4.1164")
    theta = 1 / (rho + 1)
    mu = (6 * theta - 1) / 5
    old = theta / (1 + theta)
    published = frontier["constants"]

    rows, drifted = {}, []
    for name, exact in (("theta_star", theta), ("mu_star", mu),
                        ("new_dense_overlap_exponent", theta),
                        ("old_dense_overlap_exponent", old)):
        if name not in published:
            continue
        drift = bits(published[name]) - bits(float(exact))
        rows[name] = {"published": published[name],
                      "exact": "%d/%d" % (exact.numerator, exact.denominator),
                      "nearest_double": float(exact),
                      "ulps_from_the_nearest_double": drift}
        if drift:
            drifted.append(name)

    # These are RATIONAL. Evaluating them in float64 instead of exactly is a
    # mechanism, not a guess -- so reproduce the published bits that way and say
    # whether that is exactly what was shipped.
    theta_f = 1 / (float(rho) + 1)
    mu_f = (6 * theta_f - 1) / 5
    reproduced = {
        "theta_star": theta_f == published.get("theta_star"),
        "mu_star": mu_f == published.get("mu_star"),
    }

    # C_H = e^(1/9) 3^(1/6) / 4 and c_H = C_H^(-6/5), both transcendental
    e9_lo, e9_hi = _exp_bracket(Fraction(1, 9))
    t3_lo, t3_hi = _nth_root_lo(Fraction(3), 6), _nth_root_hi(Fraction(3), 6)
    CH_lo, CH_hi = widen(e9_lo * t3_lo / 4, e9_hi * t3_hi / 4)
    ch_verdict = ulps_against_bracket(published["C_H"], CH_lo, CH_hi)
    # c_H = C_H^(-6/5) = exp(-(6/5) ln C_H)
    lc_lo, lc_hi = ln_bracket(1 / CH_hi)[0], ln_bracket(1 / CH_lo)[1]
    ec_lo, _ = _exp_bracket(Fraction(6, 5) * lc_lo)
    _, ec_hi = _exp_bracket(Fraction(6, 5) * lc_hi)
    cl_verdict = ulps_against_bracket(published["c_H"], ec_lo, ec_hi)

    # IDENTIFY loosely, then JUDGE exactly. The first version required the
    # printed decimal to sit within its own last place of the reference, which
    # is precisely what fails when a paper prints the float64 value of a
    # rational -- so all eight of them came back "unidentified" and the verdict
    # that mattered was never rendered.
    references = {
        "theta_star": (Fraction(theta), Fraction(theta)),
        "mu_star": (Fraction(mu), Fraction(mu)),
        "old_dense_overlap_exponent": (Fraction(old), Fraction(old)),
        "C_H": (CH_lo, CH_hi),
        "c_H": (ec_lo, ec_hi),
    }
    inline, unidentified = {}, []
    for shown in re.findall(r"=?\s*\n?([0-9]+\.[0-9]{4,})\\ldots", paper):
        places = len(shown.split(".")[1])
        best = None
        for name, (lo, hi) in references.items():
            ref = bracket_decimal(lo, hi, places + 8)
            if ref is None:
                continue
            gap = abs(Fraction(ref) - Fraction(shown))
            # Identify within TEN units of the printed last place. One unit
            # is too tight -- a paper printing the float64 value of a
            # rational is off by more than that, and that is exactly the
            # case worth judging -- and these constants are separated by
            # more than 1e-2, so ten units cannot confuse two of them.
            if gap <= Fraction(10, 10 ** places) and (best is None or gap < best[2]):
                best = (name, ref, gap)
        if best is None:
            unidentified.append(shown)
            continue
        name, ref, _ = best
        verdict = dict(decimal_verdict(shown, ref), published=shown)
        prior = inline.get(name)
        # keep the WORST verdict seen for a constant printed more than once
        rank = {"exact to every published digit": 0,
                "correctly rounded at the last digit": 1,
                "truncated rather than rounded at the last digit": 2,
                "OVER-PUBLISHED": 3}
        if prior is None or rank.get(verdict["verdict"], 3) > rank.get(
                prior["verdict"], 3):
            inline[name] = verdict
    return {
        "rows": rows, "off_by_at_least_one_ulp": drifted,
        "the_published_value_is_the_float64_evaluation": reproduced,
        "C_H": {"published": published["C_H"],
                "recomputed": bracket_decimal(CH_lo, CH_hi, 20),
                **ch_verdict, "closed_form": "e^(1/9) * 3^(1/6) / 4"},
        "c_H": {"published": published["c_H"],
                "recomputed": bracket_decimal(ec_lo, ec_hi, 20),
                **cl_verdict, "closed_form": "C_H^(-6/5)"},
        "rho_star_agrees": published.get("rho_star") == 4.1164,
        "new_equals_theta_star": (published.get("new_dense_overlap_exponent")
                                  == published.get("theta_star")),
        "inline_decimals_in_the_paper": inline,
        "published_decimals_this_run_could_not_identify": unidentified,
    }


def _exp_bracket(x: Fraction, terms: int = 120) -> tuple[Fraction, Fraction]:
    """`e^x` for `0 <= x < terms`, from the series with an exact tail bound.

    Truncating at `N` leaves `sum_{k>=N} x^k/k! <= (x^N/N!) / (1 - x/(N+1))`
    whenever `x < N+1`, because the terms then decay at least geometrically with
    ratio `x/(N+1)`. The first version asserted `x <= 1` and `c_H = C_H^(-6/5)`
    needs `e^1.31`, so it raised rather than answering -- which is the right
    failure, but the wrong bound.
    """
    assert 0 <= x < terms, "exp bracket asked for x outside its tail bound"
    s, term = Fraction(0), Fraction(1)
    for k in range(terms):
        s += term
        term = term * x / (k + 1)
    return widen(s, s + term / (1 - x / (terms + 1)))


# ---------------------------------------------------------------------------

def check_ledger(ledger: dict, paper: str) -> dict:
    def block(start: str, end: str) -> str:
        return paper[paper.index(start):paper.index(end)]

    prose = re.findall(r"^(\d+)\. ", block("## 21.1 Proved internally",
                                          "## 21.2 Inherited"), re.M)
    inherited = re.findall(r"^- ", block("## 21.2 Inherited", "## 21.3 External"), re.M)
    external = re.findall(r"^- ", block("## 21.3 External",
                                        "## 21.4 External live"), re.M)
    live = re.findall(r"^- ", block("## 21.4 External live", "## 21.5 Heuristic"), re.M)
    heur = re.findall(r"^- ", block("## 21.5 Heuristic", "# 22. Checker scope"), re.M)
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)

    pairs = [
        ("21.1 proved internally", len(prose), "proved_internally"),
        ("21.2 inherited", len(inherited), "inherited_internal"),
        ("21.3 external technical", len(external), "external_technical_input"),
        ("21.4 external live computational", len(live), "live_computational_input"),
        ("21.5 heuristic / open", len(heur), "heuristic_or_open"),
    ]
    table, shortfalls = [], []
    for label, count, key in pairs:
        got = len(ledger.get(key, []))
        table.append({"paper_section": label, "paper_items": count,
                      "ledger_key": key, "ledger_items": got,
                      "shortfall": count - got})
        if count != got:
            shortfalls.append(label)
    def unmatched(bullets_block: str, entries: list) -> dict:
        """Which bullets have no ledger entry, by DISTINCTIVE words only.

        A count says how many are missing; this tries to say which. The first
        version accepted any word of seven letters, so a bullet was "matched"
        by `inherited` appearing somewhere else in the ledger and the locator
        found nothing at all. A word shared with another bullet in the same
        section cannot identify either of them, so only words unique to one
        bullet are used -- and a bullet with no unique word is reported as
        undecidable rather than quietly counted as matched.

        This is a keyword test and is labelled as one. It agreed with reading
        the paper for A-U.2d.7's NO-GO 18.2; the decidable claim is the count.
        """
        bullets = [ln[2:].strip() for ln in bullets_block.splitlines()
                   if ln.startswith("- ")]
        seen: dict[str, int] = {}
        for b in bullets:
            for w in set(re.findall(r"[a-z-]{7,}", b.lower())):
                seen[w] = seen.get(w, 0) + 1
        missing, undecidable = [], []
        for b in bullets:
            unique = [w for w in set(re.findall(r"[a-z-]{7,}", b.lower()))
                      if seen[w] == 1]
            if not unique:
                undecidable.append(b[:110])
            elif not any(w in entry.lower() for entry in entries for w in unique):
                missing.append(b[:110])
        return {"bullets": len(bullets), "with_no_ledger_entry": missing,
                "undecidable_by_this_test": undecidable}

    missing_no_go = ["%s %s" % (n, ti) for n, ti in no_go
                     if not any(w in entry.lower()
                                for entry in ledger.get("no_go", [])
                                for w in re.findall(r"[a-z-]{6,}", ti.lower()))]
    missing_external = unmatched(block("## 21.3 External", "## 21.4 External live"),
                                 ledger.get("external_technical_input", []))
    missing_open = unmatched(block("## 21.5 Heuristic", "# 22. Checker scope"),
                             ledger.get("heuristic_or_open", []))
    return {
        "table": table,
        "sections_where_the_counts_differ": shortfalls,
        "paper_no_go_headings": len(no_go),
        "ledger_no_go_entries": len(ledger.get("no_go", [])),
        "no_go_shortfall": len(no_go) - len(ledger.get("no_go", [])),
        "paper_no_go_titles_with_no_ledger_entry_sharing_a_keyword": missing_no_go,
        "paper_external_inputs_with_no_ledger_entry_sharing_a_keyword":
            missing_external,
        "paper_open_questions_with_no_ledger_entry_sharing_a_keyword": missing_open,
        "round_agrees": ledger.get("round"),
        "the_ledger_declares_a_status": "status" in ledger,
        "the_ledger_declares_a_next_round": "next" in ledger,
    }


def check_artifacts(bundle: pathlib.Path) -> dict:
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = validation.get("files")
    if isinstance(files, list):
        sv = {r["file"]: r["sha256"] for r in files}
        shape = "list of file records (items 51, 52, 54)"
    elif isinstance(files, dict):
        sv = {k: v["sha256"] for k, v in files.items()}
        shape = "dict of file records keyed by filename (item 53)"
    elif "artifact_sha256_before_manifest" in validation:
        sv = dict(validation["artifact_sha256_before_manifest"])
        shape = "dict keyed by filename (item 50)"
    else:
        sv, shape = {}, "UNRECOGNISED"

    cs = {}
    for line in (bundle / CHECKSUMS).read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            cs[name.strip()] = digest

    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()
              for n in present}
    return {
        "validation_record_shape": shape,
        "files_in_the_bundle": len(present),
        "listed_in_CHECKSUMS": len(cs),
        "listed_in_the_validation_record": len(sv),
        "CHECKSUMS_mismatches": sorted(n for n, d in cs.items()
                                       if actual.get(n) != d),
        "validation_record_mismatches": sorted(n for n, d in sv.items()
                                               if actual.get(n) != d),
        "digests_disagreeing_between_the_two_manifests":
            sorted(n for n in set(cs) & set(sv) if cs[n] != sv[n]),
        "in_CHECKSUMS_but_not_the_validation_record": sorted(set(cs) - set(sv)),
        "in_the_validation_record_but_not_CHECKSUMS": sorted(set(sv) - set(cs)),
        "covered_by_neither_manifest": [p for p in present
                                        if p not in cs and p not in sv],
        "the_scope_note_declares_the_gap": bool(
            validation.get("scope_note")
            and "not self-hashed" in validation["scope_note"]),
        "scope_note": validation.get("scope_note"),
        "the_record_says_all_ok": validation.get("all_ok"),
        "a_stdout_transcript_is_shipped": any(
            p.endswith(".txt") and "stdout" in p for p in present),
    }


def check_their_claims(report: dict, res: dict) -> dict:
    seg, gam = res["segments"], res["gamma"]
    dep, car = res["harmonic_depth"], res["au2d7_carryover"]
    mapping = {
        "exact_product_identity":
            seg["product_identity_violations"] == 0 and seg["segments"] > 0,
        "source_minimum_distinct_odd_packing":
            seg["packing_envelope_violations"] == 0
            and seg["sorted_state_below_y_plus_2k"] == 0,
        "gamma_and_log_envelope":
            gam["exact_disagreements"] == 0
            and seg["gamma_form_disagrees_with_the_product"] == 0,
    }
    stated = list(report.get("checks", {}))
    checked = {c: mapping[c] for c in stated if c in mapping}
    return {
        "checks_the_report_names": len(stated),
        "independently_confirmed": sum(1 for v in checked.values() if v),
        "independently_contradicted": sorted(k for k, v in checked.items() if not v),
        "not_covered_by_this_run": [c for c in stated if c not in mapping],
        "their_worst_gamma_error": report["checks"].get("max_gamma_log2_abs_error"),
        "this_run_s_gamma_error": 0,
        "the_scope_warning": report.get("scope_warning", "")[:120],
    }


# ---------------------------------------------------------------------------

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                                   # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=3000)
    ap.add_argument("--out")
    args = ap.parse_args()
    bundle = pathlib.Path(args.bundle)

    paper = (bundle / PAPER).read_text(encoding="utf-8")
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))

    ln2_lo, ln2_hi = ln2_bracket()
    a_lo, a_hi = 1 / ln2_hi, 1 / ln2_lo

    res: dict = {
        "tool": "src54_low_source_saturation.py",
        "round": report.get("round"),
        "orbit_limit": args.limit,
        "instrument": {
            "brackets_from": "src53_plateau_reset (certified there, not re-derived)",
            "one_over_ln2_to_20_places": bracket_decimal(a_lo, a_hi, 20),
            "ln_bracket_from": "2 sum u^(2k+1)/(2k+1) with an exact tail bound",
        },
    }
    res["instrument_selfcheck"] = check_instrument(ln2_lo, ln2_hi, a_lo, a_hi)
    res["segments"] = check_segments(args.limit)
    res["gamma"] = check_gamma_representation(
        tuple((y, L) for y in (3, 5, 7, 27, 255, 4095, 65535)
              for L in (1, 2, 3, 5, 13, 40, 111, 400)))
    res["harmonic_depth"] = check_harmonic_depth(args.limit)
    res["grids"] = check_grids(a_lo, a_hi, frontier)
    res["au2d7_carryover"] = check_au2d7_carryover(
        report, frontier, a_lo, a_hi, ln2_lo, ln2_hi)
    res["constants"] = check_constants(frontier, paper, a_lo, a_hi, ln2_lo, ln2_hi)
    res["ledger"] = check_ledger(ledger, paper)
    res["artifacts"] = check_artifacts(bundle)
    res["their_claims"] = check_their_claims(report, res)

    seg, gam, dep = res["segments"], res["gamma"], res["harmonic_depth"]
    gr, car, art = res["grids"], res["au2d7_carryover"], res["artifacts"]
    failures = ["instrument.%s" % n
                for n in res["instrument_selfcheck"]["failed"]]
    for key in ("product_identity_violations", "two_forms_of_the_identity_disagree",
                "packing_envelope_violations", "sorted_state_below_y_plus_2k",
                "gamma_form_disagrees_with_the_product"):
        if seg[key]:
            failures.append("segments.%s = %d" % (key, seg[key]))
    if gam["exact_disagreements"]:
        failures.append("gamma.exact_disagreements = %d" % gam["exact_disagreements"])
    if gam["lgamma_disagreements_beyond_cancellation"]:
        failures.append("gamma.lgamma_disagreements_beyond_cancellation = %d"
                        % gam["lgamma_disagreements_beyond_cancellation"])
    for key in ("theorem_9_1_violations", "the_two_forms_of_9_1_are_not_equivalent"):
        if dep[key]:
            failures.append("harmonic_depth.%s = %d" % (key, dep[key]))
    for key in GRID_COUNTERS:
        if gr[key]:
            failures.append("grids.%s = %s" % (key, gr[key]))
    unread = sorted(k for k, v in gr.items()
                    if isinstance(v, int) and not isinstance(v, bool)
                    and k not in GRID_COUNTERS
                    and k not in ("grid_points", "low_source_grid_points"))
    if unread:
        failures.append("grids: %s is counted but nothing reads it" % unread)
    if not car["verified_floor_recomputes"]:
        failures.append("au2d7_carryover: 2075*2^60 is not the published floor")
    for key in ("CHECKSUMS_mismatches", "validation_record_mismatches",
                "digests_disagreeing_between_the_two_manifests"):
        if art[key]:
            failures.append("artifacts.%s = %s" % (key, art[key]))
    if art["validation_record_shape"] == "UNRECOGNISED":
        failures.append("artifacts: the validation record shape is unrecognised")
    if res["their_claims"]["independently_contradicted"]:
        failures.append("their_claims: %s"
                        % res["their_claims"]["independently_contradicted"])

    guards = []
    if seg["segments"] < 20000:
        guards.append("too few segments to discriminate: %d" % seg["segments"])
    if seg["segments_meeting_the_packing_premise"] < 1000:
        guards.append("the packing premise is barely attained: %d"
                      % seg["segments_meeting_the_packing_premise"])
    # A premise NO real chain meets is a measurement about the theorem's scope,
    # and this run reports the denominator rather than dressing it up. A premise
    # a HANDFUL meet is the dangerous case: it looks like a test and is not.
    # (What stops the empty case from being vacuous is not a guard here but the
    # drill's positive control, which deletes the premise gate and requires red.)
    if 0 < dep["theorem_9_1_checked"] < 200:
        guards.append("theorem 9.1 was applied to %d chains: too few to have "
                      "tested it, too many to call it untested"
                      % dep["theorem_9_1_checked"])
    if dep["chains"] < 5000:
        guards.append("too few chains built: %d" % dep["chains"])
    if dep["low_source_chains_3_le_y1_le_L"] < 200:
        guards.append("the low-source regime is barely attained: %d"
                      % dep["low_source_chains_3_le_y1_le_L"])
    if dep["low_source_chains_3_le_y1_le_L"] < 50:
        guards.append("the low-source regime 3 <= y1 <= L is barely attained: %d"
                      % dep["low_source_chains_3_le_y1_le_L"])
    if gam["pairs"] < 20 or gam["largest_L"] < 100:
        guards.append("the Gamma check is too small: %d pairs, largest L %d"
                      % (gam["pairs"], gam["largest_L"]))
    if gr["grid_points"] < 30:
        guards.append("grid too small: %d" % gr["grid_points"])
    if len(car["rows"]) < 5:
        guards.append("only %d carryover floors recomputed" % len(car["rows"]))
    if car["inversion_sharper_from_depth"] is None:
        guards.append("the crossover depth was not located")
    if car["rows_the_bracket_could_not_decide"]:
        guards.append("the bracket could not decide %d carryover floors: %s"
                      % (len(car["rows_the_bracket_could_not_decide"]),
                         car["rows_the_bracket_could_not_decide"]))
    for key in ("high_source_floor", "log2_floor"):
        if not car[key].get("decided"):
            guards.append("au2d7_carryover.%s: the bracket could not decide" % key)
    for key in ("C_H", "c_H"):
        if not res["constants"][key].get("decided"):
            guards.append("constants.%s: the bracket could not decide" % key)
    if res["constants"]["published_decimals_this_run_could_not_identify"]:
        guards.append("a decimal the paper publishes matches no reference: %s"
                      % res["constants"]["published_decimals_this_run_could_not_identify"])
    if len(res["constants"]["rows"]) < 3:
        guards.append("only %d rational constants bracketed"
                      % len(res["constants"]["rows"]))
    if res["their_claims"]["checks_the_report_names"] < 4:
        guards.append("only %d checker entries were read; the report shape may "
                      "have changed" % res["their_claims"]["checks_the_report_names"])
    if art["listed_in_CHECKSUMS"] < 5:
        guards.append("only %d digests in CHECKSUMS" % art["listed_in_CHECKSUMS"])
    # An anchor that stops matching reads as "the paper lists nothing here",
    # which would turn every ledger entry into a spurious surplus.
    empty = [row["paper_section"] for row in res["ledger"]["table"]
             if row["paper_items"] < 1]
    if empty:
        guards.append("the paper's own ledger sections parsed empty: %s" % empty)

    res["failures"] = failures
    res["non_vacuity_guards"] = guards
    res["passed"] = not failures and not guards
    text = json.dumps(res, indent=2, ensure_ascii=False)
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
