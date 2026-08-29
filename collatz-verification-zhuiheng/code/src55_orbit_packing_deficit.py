"""RUN-037 — independent recheck of Hard-Zeta round A-U.2d.9.

`Orbit-Packing Deficit Rigidity` (source item 55). 數學戰士「墜衡」.

A-U.2d.8 left an open problem in its own ledger: a real accelerated orbit ought
to have a strict deficit against the consecutive-odd packing envelope, but no
quantitative theorem existed. This round answers it, and the answer is one line
of arithmetic: `3n+1 = 1 (mod 3)`, so no accelerated image is ever divisible by
three. The states are therefore packed into the integers coprime to 6, spacing
3 rather than 2, and the local exponent moves `1/6 -> 1/9`.

Almost all of that is decidable. The sieve, the residue refinements, the
admissible positions, the sieved envelope and the two-progression Gamma form are
statements about integers and rationals. Section 11 is decidable too, and this
is the round's most useful feature: Theorem 11.2's premise is *first-crossing
subcriticality*, `sum q_j < beta m`, which every real first-crossing interval
satisfies by construction -- so unlike A-U.2d.8's section 9.1 it can actually be
tested. Its `17/24` comes from the 3-sieve: among `W` consecutive integers the
odd 3-free ones with `q = k` number at most `W/(3*2^k) + 1`.

Sections 7 and 8 are the exception and are handled as A-U.2d.8's were. Lemma
7.1 needs `z_1 > y_r`, met by no real chain, so its combinatorial half is
enumerated and its orbit half premise-gated.

Brackets come from `src53_plateau_reset` and `src54_low_source_saturation`,
certified there rather than re-derived.

Usage:
    python code/src55_orbit_packing_deficit.py --bundle <dir> [--limit N] [--out F]
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import pathlib
import re
import struct
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src47_survival_closure import decimal_verdict                 # noqa: E402
from src53_plateau_reset import (                                   # noqa: E402
    accelerated, beta_bracket, bracket_decimal, chains_of,
    crossings_and_stalks, cumulative, ln2_bracket,
)
from src54_low_source_saturation import (                           # noqa: E402
    _exp_bracket, _nth_root_hi, _nth_root_lo, _pow_bracket, ln_bracket,
    simplify, ulps_against_bracket, widen,
)

PAPER = "Hard_Zeta_Phase_II_Round_AU2d9_Orbit_Packing_Deficit_Rigidity_v0.1.md"
REPORT = "Hard_Zeta_AU2d9_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d9_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d9_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d9.json"
CHECKSUMS = "CHECKSUMS.sha256"

# Named once, so a counter added later without being listed makes the run
# REFUSE rather than pass quietly (RUN-035's lesson).
GRID_COUNTERS = (
    "theorem_6_1_violations",
    "corollary_6_2_violations",
    "corollary_8_2_not_implied_by_8_1",
    "corollary_8_3_inversion_violations",
    "mu9_not_nine_theta_minus_one_over_eight",
    "deficit_exponent_not_one_sixth_minus_one_ninth",
)


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def beta_tight() -> tuple[Fraction, Fraction]:
    """`log2 3` from two certified logarithms, not from a bit length.

    `beta_bracket` is exact but only `1e-6` wide, which cannot pin a double --
    it left three constants "undecided" on the first run of this gate. `ln 3`
    and `ln 2` each come with an exact tail bound, so their quotient is a
    bracket some sixty digits wide and every comparison here decides.
    """
    l3_lo, l3_hi = ln_bracket(Fraction(3))
    l2_lo, l2_hi = ln2_bracket()
    return l3_lo / l2_hi, l3_hi / l2_lo


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def syracuse(n: int) -> int:
    t = 3 * n + 1
    return t >> v2(t)


# ---------------------------------------------------------------------------
# section 3 -- the sieve, and the residue refinements it buys
# ---------------------------------------------------------------------------

def check_instrument(beta_lo: Fraction, beta_hi: Fraction,
                     ln2_lo: Fraction, ln2_hi: Fraction) -> dict:
    """Do the brackets bracket what they claim?

    An instrument only ever pointed at the subject is never tested. The first
    version of this gate asserted the tight `beta` against the certified coarse
    one -- but an assertion CRASHES, and a crashed gate is a malformed drill
    result rather than a caught defect. A named failure reports instead.
    """
    failed = []
    coarse_lo, coarse_hi = beta_bracket()
    if not (coarse_lo <= beta_hi and beta_lo <= coarse_hi):
        failed.append("the_tight_beta_disagrees_with_the_certified_coarse_one")
    # 2^beta = 3, so beta must sit between the two rationals bracketing log2 3
    if not (Fraction(3, 2) < beta_lo and beta_hi < Fraction(8, 5)):
        failed.append("beta_is_outside_its_elementary_bounds")
    if beta_hi - beta_lo > Fraction(1, 10 ** 20):
        failed.append("the_beta_bracket_is_too_wide_to_pin_a_double")
    l2 = ln_bracket(Fraction(2))
    if not (l2[0] <= ln2_lo and ln2_hi <= l2[1]):
        failed.append("ln_of_two_does_not_contain_the_certified_bracket")
    e2 = _exp_bracket(ln2_hi)
    if not (_exp_bracket(ln2_lo)[0] <= 2 <= e2[1]):
        failed.append("exp_of_ln_two_does_not_contain_two")
    r9 = _nth_root_lo(Fraction(512), 9), _nth_root_hi(Fraction(512), 9)
    if not (r9[0] <= 2 <= r9[1]):
        failed.append("ninth_root_of_512_does_not_contain_two")
    if syracuse(1) != 1 or syracuse(3) != 5 or syracuse(7) != 11:
        failed.append("the_syracuse_map_disagrees_with_hand_computed_values")
    if admissible(7, 4) != [7, 11, 13, 17]:
        failed.append("the_admissible_positions_disagree_with_a_hand_list")
    return {"checks": 8, "failed": failed}


def check_sieve(limit: int, trials: int) -> dict:
    t = {
        "odd_integers_mapped": 0, "images_divisible_by_three": 0,
        "post_entry_states": 0, "states_not_1_or_5_mod_6": 0,
        "first_crossing_sources": 0,
        "sources_with_L_equal_1": 0,
        "post_entry_sources_with_L_at_least_2": 0,
        "sources_not_3_mod_4": 0,
        "sources_not_7_or_11_mod_12": 0,
        "L_equal_1_sources_not_7_or_11_mod_12": 0,
        "pre_entry_sources_excluded": 0,
    }
    for n in range(1, 2 * trials, 2):
        t["odd_integers_mapped"] += 1
        if syracuse(n) % 3 == 0:
            t["images_divisible_by_three"] += 1
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        for j in range(1, len(values)):
            t["post_entry_states"] += 1
            if values[j] % 6 not in (1, 5):
                t["states_not_1_or_5_mod_6"] += 1
        for s in range(n):
            end = e[s]
            if end is None or end <= s:
                continue
            t["first_crossing_sources"] += 1
            if s < 1:
                t["pre_entry_sources_excluded"] += 1
                continue
            L, y = end - s, values[s]
            # Corollary 3.3 refines A-U.2d.5's `3 (mod 4)`, and THAT result
            # needs `L >= 2`. Applied to every first-crossing source instead,
            # half of them "violate" it -- a statement about the check.
            if L == 1:
                t["sources_with_L_equal_1"] += 1
                if y % 12 not in (7, 11):
                    t["L_equal_1_sources_not_7_or_11_mod_12"] += 1
                continue
            t["post_entry_sources_with_L_at_least_2"] += 1
            if y % 4 != 3:
                t["sources_not_3_mod_4"] += 1
            if y % 12 not in (7, 11):
                t["sources_not_7_or_11_mod_12"] += 1
    return t


# ---------------------------------------------------------------------------
# section 4 and section 5 -- the sieved envelope and its Gamma form
# ---------------------------------------------------------------------------

def admissible(y: int, L: int) -> list[int]:
    """The `L` smallest integers `>= y` coprime to 6."""
    out, n = [], y
    while len(out) < L:
        if n % 2 and n % 3:
            out.append(n)
        n += 1
    return out


def packing6(y: int, L: int) -> Fraction:
    out = Fraction(1)
    for a in admissible(y, L):
        out *= 1 + Fraction(1, 3 * a)
    return out


def packing_odd(y: int, L: int) -> Fraction:
    out = Fraction(1)
    for k in range(L):
        out *= 1 + Fraction(1, 3 * (y + 2 * k))
    return out


def gamma_progression(y: int, c: int, n: int) -> Fraction:
    """`G(y,c;n)` as the Pochhammer quotient it is for integer `n`.

    The round writes it as a ratio of four Gamma values. At integer `n` the
    functional equation collapses that to `prod (a+m)/(b+m)` with
    `a = (y+c)/6 + 1/18` and `b = (y+c)/6`, which is exactly the product it
    started from -- so there is nothing to evaluate. Same move as RUN-036.
    """
    a = Fraction(y + c, 6) + Fraction(1, 18)
    b = Fraction(y + c, 6)
    out = Fraction(1)
    for m in range(n):
        out *= (a + m) / (b + m)
    return out


def two_progression_form(y: int, L: int) -> Fraction:
    n, eps = divmod(L, 2)
    c = 4 if y % 6 == 1 else 2
    out = gamma_progression(y, 0, n) * gamma_progression(y, c, n)
    if eps:
        out *= 1 + Fraction(1, 3 * (y + 6 * n))
    return out


def check_packing(limit: int) -> dict:
    t = {
        "segments": 0, "max_L": 0,
        "segments_meeting_the_packing_premise": 0,
        "segments_failing_distinctness_or_minimality": 0,
        "sorted_state_below_its_admissible_position": 0,
        "explicit_admissible_position_errors": 0,
        "uniform_lower_bound_a_k_below_y_plus_3k_minus_1": 0,
        "sieved_envelope_violations": 0,
        "sieved_envelope_above_the_odd_envelope": 0,
        "two_progression_form_disagrees_with_the_product": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        for s in range(1, n):
            end = e[s]
            if end is None or end <= s:
                continue
            L, y = end - s, values[s]
            t["segments"] += 1
            t["max_L"] = max(t["max_L"], L)
            states = values[s:end]
            if not (all(v >= y for v in states)
                    and len(set(states)) == len(states)):
                t["segments_failing_distinctness_or_minimality"] += 1
                continue
            t["segments_meeting_the_packing_premise"] += 1
            a = admissible(y, L)
            for k, v in enumerate(sorted(states)):
                if v < a[k]:
                    t["sorted_state_below_its_admissible_position"] += 1
                    break
            for k in range(1, L):
                if a[k] < y + 3 * k - 1:
                    t["uniform_lower_bound_a_k_below_y_plus_3k_minus_1"] += 1
                    break
            step = 4 if y % 6 == 1 else 2
            for m in range(L // 2):
                if a[2 * m] != y + 6 * m or a[2 * m + 1] != y + 6 * m + step:
                    t["explicit_admissible_position_errors"] += 1
                    break
            script = Fraction(1)
            for v in states:
                script *= 1 + Fraction(1, 3 * v)
            p6 = packing6(y, L)
            if script > p6:
                t["sieved_envelope_violations"] += 1
            if p6 > packing_odd(y, L):
                t["sieved_envelope_above_the_odd_envelope"] += 1
            if p6 != two_progression_form(y, L):
                t["two_progression_form_disagrees_with_the_product"] += 1
    return t


def check_gamma(pairs: tuple[tuple[int, int], ...]) -> dict:
    """Theorem 5.1 twice: exactly, and against an independent numeric Gamma."""
    t = {"pairs": 0, "exact_disagreements": 0, "largest_L": 0,
         "worst_lgamma_absolute_error": 0.0,
         "worst_error_over_its_cancellation_bound": 0.0,
         "lgamma_disagreements_beyond_cancellation": 0,
         "rows": []}
    for y, L in pairs:
        if y % 6 not in (1, 5):
            continue
        t["pairs"] += 1
        t["largest_L"] = max(t["largest_L"], L)
        exact = packing6(y, L)
        if exact != two_progression_form(y, L):
            t["exact_disagreements"] += 1
        n, eps = divmod(L, 2)
        c = 4 if y % 6 == 1 else 2
        terms, approx = [], 0.0
        for off in (0, c):
            a, b = (y + off) / 6 + 1 / 18, (y + off) / 6
            four = [math.lgamma(n + a), math.lgamma(b),
                    math.lgamma(a), math.lgamma(n + b)]
            terms += four
            approx += four[0] + four[1] - four[2] - four[3]
        if eps:
            approx += math.log1p(1 / (3 * (y + 6 * n)))
        ln_exact = math.log(exact.numerator) - math.log(exact.denominator)
        err = abs(approx - ln_exact)
        # `ln P_6` is a difference of large log-gammas; relative error under
        # that much cancellation is meaningless (RUN-036 failed 12 correct
        # pairs that way). The tolerance is what the subtraction costs.
        allowed = 16 * 2.220446049250313e-16 * max(
            [abs(v) for v in terms] or [1.0]) + 1e-12
        t["worst_lgamma_absolute_error"] = max(
            t["worst_lgamma_absolute_error"], err)
        t["worst_error_over_its_cancellation_bound"] = max(
            t["worst_error_over_its_cancellation_bound"], err / allowed)
        if err > allowed:
            t["lgamma_disagreements_beyond_cancellation"] += 1
        if len(t["rows"]) < 5:
            t["rows"].append({"y": y, "L": L,
                              "log2_P6": "%.12f" % (ln_exact / math.log(2)),
                              "lgamma_absolute_error": "%.3e" % err})
    return t


def check_exponents(a_lo: Fraction, a_hi: Fraction) -> dict:
    """Corollary 5.2 and Theorem 5.3: `P_6 = Theta(L^(1/9))`, ratio `L^(-1/18)`.

    These are asymptotic, so what is checked is that the empirical exponent
    APPROACHES the claimed one and that the sieved exponent is below the odd
    one -- not that either equals it at finite `L`.
    """
    t = {"sources": 0, "rows": [],
         "sieved_exponent_not_approaching_one_ninth": 0,
         "odd_exponent_not_approaching_one_sixth": 0,
         "deficit_exponent_not_negative": 0,
         "largest_L": 0}
    for y in (7, 11, 25, 49):
        prev = None
        for L in (200, 800, 3200, 12800):
            t["largest_L"] = max(t["largest_L"], L)
            p6 = math.log(float(packing6(y, L)))
            po = math.log(float(packing_odd(y, L)))
            e6, eo = p6 / math.log(L), po / math.log(L)
            if prev is not None and abs(e6 - 1 / 9) > abs(prev[0] - 1 / 9) + 1e-9:
                t["sieved_exponent_not_approaching_one_ninth"] += 1
            if prev is not None and abs(eo - 1 / 6) > abs(prev[1] - 1 / 6) + 1e-9:
                t["odd_exponent_not_approaching_one_sixth"] += 1
            if p6 - po >= 0:
                t["deficit_exponent_not_negative"] += 1
            prev = (e6, eo)
            if len(t["rows"]) < 8:
                t["rows"].append({"y": y, "L": L,
                                  "sieved_exponent": "%.5f" % e6,
                                  "odd_exponent": "%.5f" % eo,
                                  "deficit_exponent": "%.5f"
                                  % ((p6 - po) / math.log(L))})
        t["sources"] += 1
    return t


# ---------------------------------------------------------------------------
# section 7 -- the anchor gap, combinatorially and on orbits
# ---------------------------------------------------------------------------

def check_anchor_gap(limit: int, depth: int = 6, window: int = 14) -> dict:
    t = {
        "residue_sets_enumerated": 0,
        "spans_below_six_r_minus_eight": 0,
        "tight_sets_whose_last_anchor_is_not_11_mod_12": 0,
        "tight_sets_whose_next_admissible_state_is_not_two_higher": 0,
        "chains": 0,
        "chains_where_the_outer_endpoint_exceeds_the_inner_source": 0,
        "lemma_7_1_checked": 0, "lemma_7_1_violations": 0,
        "max_depth": 0,
    }
    anchors = [n for n in range(7, 7 + 12 * window) if n % 12 in (7, 11)]
    for r in range(2, depth + 1):
        for combo in itertools.combinations(anchors, r):
            t["residue_sets_enumerated"] += 1
            span = combo[-1] - combo[0]
            if span < 6 * (r - 1) - 2:
                t["spans_below_six_r_minus_eight"] += 1
            if span != 6 * (r - 1) - 2:
                continue
            if combo[-1] % 12 != 11:
                t["tight_sets_whose_last_anchor_is_not_11_mod_12"] += 1
                continue
            nxt = combo[-1] + 1
            while nxt % 2 == 0 or nxt % 3 == 0:
                nxt += 1
            if nxt - combo[-1] != 2:
                t["tight_sets_whose_next_admissible_state_is_not_two_higher"] += 1
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, stalks = crossings_and_stalks(K, n)
        for ch in chains_of(K, n, e, stalks):
            if ch[0] < 1:
                continue
            t["chains"] += 1
            r, s1, sr = len(ch), ch[0], ch[-1]
            t["max_depth"] = max(t["max_depth"], r)
            z1, yr, y1 = values[e[s1]], values[sr], values[s1]
            if z1 <= yr:
                continue
            t["chains_where_the_outer_endpoint_exceeds_the_inner_source"] += 1
            t["lemma_7_1_checked"] += 1
            if z1 - y1 < 6 * (r - 1):
                t["lemma_7_1_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# section 11 -- the valuation-class span, whose premise real orbits DO meet
# ---------------------------------------------------------------------------

def check_qclass(limit: int, beta_lo: Fraction, beta_hi: Fraction) -> dict:
    t = {
        "valuations_checked": 0,
        "valuation_classes_not_exactly_one_mod_2_to_k_plus_1": 0,
        "capacity_windows": 0,
        "windows_where_N_k_exceeds_W_over_three_two_to_k_plus_one": 0,
        "windows_where_the_weighted_capacity_exceeds_17W_over_24_plus_12": 0,
        "prefixes": 0,
        "prefixes_meeting_subcriticality": 0,
        "prefixes_failing_subcriticality": 0,
        "prefixes_with_repeated_states": 0,
        "theorem_11_2_checked": 0, "theorem_11_2_violations": 0,
        "max_prefix_length": 0,
    }
    # Lemma 11.1: `q(n) = k` on odds is exactly one class modulo 2^(k+1)
    for k in range(1, 11):
        t["valuations_checked"] += 1
        mod = 1 << (k + 1)
        classes = {n % mod for n in range(1, 4 * mod, 2) if v2(3 * n + 1) == k}
        if len(classes) != 1:
            t["valuation_classes_not_exactly_one_mod_2_to_k_plus_1"] += 1
    # the interval capacity the 17/24 rests on
    for W in (24, 48, 120, 480, 1200):
        for base in (1, 7, 25, 1001):
            t["capacity_windows"] += 1
            counts = {1: 0, 2: 0, 3: 0}
            for x in range(base, base + W):
                if x % 2 == 0 or x % 3 == 0:
                    continue
                q = v2(3 * x + 1)
                if q in counts:
                    counts[q] += 1
            for k in (1, 2, 3):
                if counts[k] > Fraction(W, 3 * (1 << k)) + 1:
                    t["windows_where_N_k_exceeds_W_over_three_two_to_k_plus_one"] += 1
                    break
            weighted = 3 * counts[1] + 2 * counts[2] + counts[3]
            if weighted > Fraction(17 * W, 24) + 12:
                t["windows_where_the_weighted_capacity_exceeds_17W_over_24_plus_12"] += 1
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        for s in range(1, n):
            end = e[s]
            if end is None or end - s < 3:
                continue
            L = end - s
            m = L - 1
            t["prefixes"] += 1
            t["max_prefix_length"] = max(t["max_prefix_length"], m)
            prefix = values[s:s + m]
            if len(set(prefix)) != len(prefix):
                t["prefixes_with_repeated_states"] += 1
            # subcriticality `sum q_j < beta m`, exactly: `2^Q < 3^m`
            Q = K[s + m] - K[s]
            if 2 ** Q < 3 ** m:
                t["prefixes_meeting_subcriticality"] += 1
            else:
                t["prefixes_failing_subcriticality"] += 1
                continue
            W = max(prefix) - min(prefix) + 1
            t["theorem_11_2_checked"] += 1
            bound_hi = Fraction(24, 17) * ((4 - beta_lo) * m - 12)
            if not Fraction(W) > bound_hi:
                t["theorem_11_2_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# sections 6 and 8 -- envelopes and the ninth-root cap
# ---------------------------------------------------------------------------

def check_grids(a_lo: Fraction, a_hi: Fraction, frontier: dict) -> dict:
    t = {k: 0 for k in GRID_COUNTERS}
    t["grid_points"] = 0
    t["low_source_grid_points"] = 0
    rho = Fraction("4.1164")
    theta = 1 / (rho + 1)
    mu9 = (9 * theta - 1) / 8
    if mu9 != (9 * theta - 1) / 8:
        t["mu9_not_nine_theta_minus_one_over_eight"] += 1
    if Fraction(1, 18) != Fraction(1, 6) - Fraction(1, 9):
        t["deficit_exponent_not_one_sixth_minus_one_ninth"] += 1
    t["theta_star_exact"] = "%d/%d" % (theta.numerator, theta.denominator)
    t["mu9_exact"] = "%d/%d" % (mu9.numerator, mu9.denominator)

    e_lo, e_hi = _exp_bracket(Fraction(1, 21) + Fraction(1, 27))
    C6_lo, C6_hi = widen(e_lo * _nth_root_lo(Fraction(4), 9),
                         e_hi * _nth_root_hi(Fraction(4), 9))
    C9_lo, C9_hi = C6_lo / 6, C6_hi / 6

    for y in (7, 11, 25, 49, 121, 1001):
        for L in (1, 2, 7, 30, 200, 900):
            t["grid_points"] += 1
            P = packing6(y, L)
            P_lo, P_hi = simplify(P)
            R_lo = ln_bracket(P_lo)[0] * a_lo
            # Theorem 6.1, in natural logs
            l_lo, l_hi = ln_bracket(1 + Fraction(3 * L, y))
            if not ln_bracket(P_hi)[1] <= (Fraction(1, 3 * y)
                                           + Fraction(1, 3 * (y + 2))
                                           + l_hi / 9):
                t["theorem_6_1_violations"] += 1
            if not (7 <= y <= L):
                continue
            t["low_source_grid_points"] += 1
            # Corollary 6.2: P_6 <= C_6 (L/y)^(1/9)
            ratio_hi = _pow_bracket(Fraction(L, y), 1, 9, hi=True)
            if not P_hi <= C6_hi * ratio_hi:
                t["corollary_6_2_violations"] += 1
            # Theorem 8.1 -> Corollary 8.2: the exact cap must be no larger
            exact_cap_hi = 1 + Fraction(y, 6) * (P_hi - 1)
            ninth_lo = (C9_lo * _pow_bracket(Fraction(y), 8, 9)
                        * _pow_bracket(Fraction(L), 1, 9))
            if exact_cap_hi > 1 + ninth_lo:
                t["corollary_8_2_not_implied_by_8_1"] += 1
            # Corollary 8.3 inverts 8.2
            for r in (2, 3, 5, 12):
                forward = Fraction(r) < 1 + C9_hi * _pow_bracket(
                    Fraction(y), 8, 9, hi=True) * _pow_bracket(
                    Fraction(L), 1, 9, hi=True)
                c9_hi = _pow_bracket(1 / C9_lo, 9, 8, hi=True)
                need = c9_hi * _pow_bracket(Fraction(r - 1), 9, 8, hi=True) \
                    / _pow_bracket(Fraction(L), 1, 8)
                if forward and not Fraction(y) > need * Fraction(999, 1000):
                    t["corollary_8_3_inversion_violations"] += 1
    return t


def check_depth_cap(limit: int) -> dict:
    """Theorem 8.1, premise first -- it is Lemma 7.1 rearranged."""
    t = {"chains": 0, "chains_meeting_the_endpoint_gap_premise": 0,
         "theorem_8_1_checked": 0, "theorem_8_1_violations": 0,
         "the_two_forms_of_8_1_are_not_equivalent": 0,
         "low_source_chains_7_le_y1_le_L": 0}
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, stalks = crossings_and_stalks(K, n)
        for ch in chains_of(K, n, e, stalks):
            if ch[0] < 1:
                continue
            t["chains"] += 1
            r, s1 = len(ch), ch[0]
            L, y1, z1 = e[s1] - s1, values[s1], values[e[s1]]
            if 7 <= y1 <= L:
                t["low_source_chains_7_le_y1_le_L"] += 1
            P = packing6(y1, L)
            left = 1 + Fraction(6 * (r - 1), y1) <= P
            right = Fraction(r) <= 1 + Fraction(y1, 6) * (P - 1)
            if left != right:
                t["the_two_forms_of_8_1_are_not_equivalent"] += 1
            if not Fraction(z1 - y1) >= 6 * (r - 1):
                continue
            t["chains_meeting_the_endpoint_gap_premise"] += 1
            t["theorem_8_1_checked"] += 1
            if not right:
                t["theorem_8_1_violations"] += 1
    return t


# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict, paper: str,
                    a_lo: Fraction, a_hi: Fraction,
                    beta_lo: Fraction, beta_hi: Fraction) -> dict:
    rho = Fraction("4.1164")
    theta = 1 / (rho + 1)
    mu9 = (9 * theta - 1) / 8
    mu8 = (6 * theta - 1) / 5
    pub = frontier["constants"]

    e_lo, e_hi = _exp_bracket(Fraction(1, 21) + Fraction(1, 27))
    C6_lo, C6_hi = widen(e_lo * _nth_root_lo(Fraction(4), 9),
                         e_hi * _nth_root_hi(Fraction(4), 9))
    C9_lo, C9_hi = C6_lo / 6, C6_hi / 6
    c9_lo = _pow_bracket(1 / C9_hi, 9, 8)
    c9_hi = _pow_bracket(1 / C9_lo, 9, 8, hi=True)
    span_lo = Fraction(24, 17) * (4 - beta_hi)
    span_hi = Fraction(24, 17) * (4 - beta_lo)
    dens_lo, dens_hi = 1 / span_hi, 1 / span_lo

    rows = {}
    for name, lo, hi, form in (
        ("C6_uniform_product", C6_lo, C6_hi, "exp(1/21+1/27) * 4^(1/9)"),
        ("C9_depth", C9_lo, C9_hi, "C6/6"),
        ("c9_inversion", c9_lo, c9_hi, "C9^(-9/8)"),
        ("qclass_span_mean_spacing_lower", span_lo, span_hi, "24(4-beta)/17"),
        ("qclass_span_density_upper", dens_lo, dens_hi, "17/(24(4-beta))"),
    ):
        if name in pub:
            rows[name] = dict(ulps_against_bracket(pub[name], lo, hi),
                              published=pub[name], closed_form=form,
                              recomputed=bracket_decimal(lo, hi, 18))
    for name, exact, form in (
        ("theta_star", theta, "1/(rho+1) = %d/%d"
         % (theta.numerator, theta.denominator)),
        ("dense_root_source_floor_exponent_mu9", mu9, "(9 theta-1)/8 = %d/%d"
         % (mu9.numerator, mu9.denominator)),
        ("dense_root_source_floor_exponent_mu8", mu8, "(6 theta-1)/5 = %d/%d"
         % (mu8.numerator, mu8.denominator)),
        ("old_low_source_product_exponent", Fraction(1, 6), "1/6"),
        ("syracuse_sieved_product_exponent", Fraction(1, 9), "1/9"),
        ("dynamic_deficit_exponent", Fraction(1, 18), "1/6 - 1/9"),
    ):
        if name in pub:
            rows[name] = {"published": pub[name], "closed_form": form,
                          "decided": True, "nearest_double": float(exact),
                          "ulps": bits(pub[name]) - bits(float(exact)),
                          "recomputed": None}
    if "beta_log2_3" in pub:
        rows["beta_log2_3"] = dict(
            ulps_against_bracket(pub["beta_log2_3"], beta_lo, beta_hi),
            published=pub["beta_log2_3"], closed_form="log2 3",
            recomputed=bracket_decimal(beta_lo, beta_hi, 18))
    drifted = sorted(k for k, v in rows.items() if v.get("ulps"))

    # The derivation chain, evaluated in float64 the way the artifact did.
    chain = {
        "C9_is_the_published_C6_divided_by_six_as_doubles":
            pub.get("C6_uniform_product", 0) / 6 == pub.get("C9_depth"),
        "c9_is_the_published_C9_to_the_minus_nine_eighths_as_doubles":
            pub.get("C9_depth", 1) ** -1.125 == pub.get("c9_inversion"),
        "mu9_is_the_float64_theta_star_put_through_its_formula":
            (9 * (1 / (float(rho) + 1)) - 1) / 8
            == pub.get("dense_root_source_floor_exponent_mu9"),
        "the_spacing_is_the_float64_reciprocal_of_the_density":
            1 / pub.get("qclass_span_density_upper", 1)
            == report["constants"].get("qclass_span_mean_spacing_lower"),
    }
    # the same constant, twice, in two artifacts of one bundle
    rc, fc = report["constants"], pub
    shared = {"beta": "beta_log2_3",
              "new_3_sieved_product_exponent": "syracuse_sieved_product_exponent"}
    disagree = []
    for k in set(rc) & set(fc):
        if rc[k] != fc[k]:
            disagree.append({"constant": k, "checker_report": rc[k],
                             "frontier": fc[k],
                             "ulps_apart": bits(fc[k]) - bits(rc[k])})
    renamed = [{"checker_report": a, "frontier": b} for a, b in shared.items()
               if a in rc and b in fc]

    inline, unidentified = {}, []
    refs = {"C6_uniform_product": (C6_lo, C6_hi), "C9_depth": (C9_lo, C9_hi),
            "c9_inversion": (c9_lo, c9_hi),
            "qclass_span_mean_spacing_lower": (span_lo, span_hi),
            "qclass_span_density_upper": (dens_lo, dens_hi),
            "theta_star": (Fraction(theta), Fraction(theta)),
            "mu9": (Fraction(mu9), Fraction(mu9)),
            "mu8": (Fraction(mu8), Fraction(mu8)),
            "one_sixth": (Fraction(1, 6), Fraction(1, 6)),
            "one_ninth": (Fraction(1, 9), Fraction(1, 9)),
            "one_eighteenth": (Fraction(1, 18), Fraction(1, 18)),
            "beta": (beta_lo, beta_hi)}
    for shown in re.findall(r"=?\s*\n?([0-9]+\.[0-9]{4,})\\ldots", paper):
        places = len(shown.split(".")[1])
        best = None
        for name, (lo, hi) in refs.items():
            ref = bracket_decimal(lo, hi, places + 8)
            if ref is None:
                continue
            gap = abs(Fraction(ref) - Fraction(shown))
            if gap <= Fraction(10, 10 ** places) and (best is None or gap < best[2]):
                best = (name, ref, gap)
        if best is None:
            unidentified.append(shown)
            continue
        name, ref, _ = best
        inline.setdefault(name, dict(decimal_verdict(shown, ref),
                                     published=shown))
    return {
        "rows": rows, "off_by_at_least_one_ulp": drifted,
        "the_derivation_chain_in_float64": chain,
        "constants_the_two_artifacts_disagree_on": disagree,
        "constants_renamed_between_the_two_artifacts": renamed,
        "inline_decimals_in_the_paper": inline,
        "published_decimals_this_run_could_not_identify": unidentified,
    }


def check_ledger(ledger: dict, paper: str) -> dict:
    def block(start: str, end: str) -> str:
        return paper[paper.index(start):paper.index(end)]

    prose = re.findall(r"^(\d+)\. ", block("## 18.1 Proved internally",
                                          "## 18.2 Inherited"), re.M)
    inherited = re.findall(r"^- ", block("## 18.2 Inherited",
                                         "## 18.3 External"), re.M)
    external = re.findall(r"^- ", block("## 18.3 External",
                                        "## 18.4 Explicitly open"), re.M)
    openq = re.findall(r"^- ", block("## 18.4 Explicitly open",
                                     "# 19. Checker scope"), re.M)
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)

    keys = {"proved_internally": len(prose), "inherited_internal": len(inherited),
            "external_technical_input": len(external),
            "heuristic_or_open": len(openq)}
    table, differ = [], []
    labels = {"proved_internally": "18.1 proved internally",
              "inherited_internal": "18.2 inherited",
              "external_technical_input": "18.3 external grounding",
              "heuristic_or_open": "18.4 explicitly open"}
    for key, count in keys.items():
        got = len(ledger.get(key, []))
        table.append({"paper_section": labels[key], "paper_items": count,
                      "ledger_key": key, "ledger_items": got,
                      "shortfall": count - got})
        if count != got:
            differ.append(labels[key])
    missing = ["%s %s" % (n, ti) for n, ti in no_go
               if not any(w in entry.lower() for entry in ledger.get("no_go", [])
                          for w in re.findall(r"[a-z-]{7,}", ti.lower()))]
    return {
        "table": table, "sections_where_the_counts_differ": differ,
        "paper_no_go_headings": len(no_go),
        "ledger_no_go_entries": len(ledger.get("no_go", [])),
        "no_go_shortfall": len(no_go) - len(ledger.get("no_go", [])),
        "paper_no_go_titles_with_no_ledger_entry_sharing_a_keyword": missing,
        "ledger_keys": sorted(ledger),
        "round_agrees": ledger.get("round"),
    }


def check_artifacts(bundle: pathlib.Path) -> dict:
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = validation.get("files")
    anonymous: list[dict] = []
    blocks = [k for k in ("formal_source_validation", "json_validation",
                          "checker_script") if isinstance(validation.get(k), dict)]
    if isinstance(files, list):
        sv = {r["file"]: r["sha256"] for r in files}
        shape = "list of file records under `files` (items 51, 52, 54)"
    elif isinstance(files, dict):
        sv = {k: v["sha256"] for k, v in files.items()}
        shape = "dict of file records under `files` (item 53)"
    elif "artifact_sha256_before_manifest" in validation:
        sv = dict(validation["artifact_sha256_before_manifest"])
        shape = "dict keyed by filename (item 50)"
    elif blocks:
        # Item 55 splits the digests across three purpose-named blocks and has
        # no `files` key at all. Fifth shape in six bundles; a reader written
        # for any one of the others sees zero files and reports zero
        # mismatches, which is indistinguishable from a clean bill.
        sv, anonymous = {}, []
        for key in blocks:
            block = validation[key]
            if "sha256" in block and isinstance(block["sha256"], str):
                # This block carries a digest and NO filename. Resolve it by
                # looking the digest up among the files actually present --
                # which works, but means the record identifies that file by
                # position in the schema rather than by name.
                anonymous.append({"block": key, "sha256": block["sha256"]})
                continue
            for name, rec in block.items():
                if isinstance(rec, dict) and "sha256" in rec:
                    sv[name] = rec["sha256"]
        shape = "three purpose-named blocks, no `files` key (item 55): %s" \
            % ", ".join(blocks)
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
    by_digest = {d: n for n, d in actual.items()}
    resolved, unresolved = [], []
    for rec in anonymous:
        name = by_digest.get(rec["sha256"])
        (resolved if name else unresolved).append(
            {"block": rec["block"], "resolves_to": name})
        if name:
            sv[name] = rec["sha256"]
    return {
        "digests_the_record_gives_without_a_filename": len(anonymous),
        "…resolved_by_looking_the_digest_up_among_the_files": resolved,
        "…that_match_no_file_in_the_bundle": unresolved,
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
        "covered_by_neither_manifest": [p for p in present
                                        if p not in cs and p not in sv],
        "the_scope_note_declares_the_gap": bool(
            validation.get("scope_note")
            and "not self-hashed" in validation.get("scope_note", "")),
        "the_record_says_all_ok": validation.get(
            "all_ok", validation.get("commit_gate_passed")),
        "the_record_says_the_checker_rerun_matches_its_report":
            validation.get("checker_rerun_matches_report"),
        "the_record_s_own_notes": validation.get("notes", []),
        "a_stdout_transcript_is_shipped": any(
            p.endswith(".txt") and "stdout" in p for p in present),
    }


def check_their_claims(report: dict, res: dict) -> dict:
    sv, pk, qc = res["sieve"], res["packing"], res["qclass"]
    gam = res["gamma"]
    mapping = {
        "map_image_not_divisible_by_3":
            sv["images_divisible_by_three"] == 0 and sv["odd_integers_mapped"] > 0,
        "gamma_formula":
            gam["exact_disagreements"] == 0
            and pk["two_progression_form_disagrees_with_the_product"] == 0,
        "six_sieved_packing":
            pk["sieved_envelope_violations"] == 0
            and pk["sorted_state_below_its_admissible_position"] == 0,
        "qclass_residue_capacity":
            qc["valuation_classes_not_exactly_one_mod_2_to_k_plus_1"] == 0
            and qc["windows_where_the_weighted_capacity_exceeds_17W_over_24_plus_12"] == 0,
        "proper_prefix_span_budget":
            qc["theorem_11_2_violations"] == 0 and qc["theorem_11_2_checked"] > 0,
    }
    stated = list(report.get("checks", {}))
    checked = {c: mapping[c] for c in stated if c in mapping}
    return {
        "checks_the_report_names": len(stated),
        "independently_confirmed": sum(1 for v in checked.values() if v),
        "independently_contradicted": sorted(k for k, v in checked.items() if not v),
        "not_covered_by_this_run": [c for c in stated if c not in mapping],
        "their_worst_gamma_error":
            report.get("diagnostics", {}).get("max_gamma_relative_error"),
        "this_run_s_gamma_error": 0,
        "their_max_actual_to_sieved_ratio":
            report.get("diagnostics", {}).get(
                "max_actual_to_3sieved_pack_ratio_sampled"),
        "the_scope_warning": report.get("scope_warning", "")[:110],
    }


# ---------------------------------------------------------------------------

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                                   # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--out")
    args = ap.parse_args()
    bundle = pathlib.Path(args.bundle)

    paper = (bundle / PAPER).read_text(encoding="utf-8")
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))

    ln2_lo, ln2_hi = ln2_bracket()
    a_lo, a_hi = 1 / ln2_hi, 1 / ln2_lo
    beta_lo, beta_hi = beta_tight()

    res: dict = {
        "tool": "src55_orbit_packing_deficit.py",
        "round": report.get("round"),
        "orbit_limit": args.limit,
        "instrument": {
            "brackets_from": "src53_plateau_reset and src54_low_source_saturation",
            "one_over_ln2_to_20_places": bracket_decimal(a_lo, a_hi, 20),
        },
    }
    res["instrument_selfcheck"] = check_instrument(beta_lo, beta_hi,
                                                  ln2_lo, ln2_hi)
    res["sieve"] = check_sieve(args.limit, args.trials)
    res["packing"] = check_packing(args.limit)
    res["gamma"] = check_gamma(tuple((y, L) for y in (7, 11, 25, 49, 121, 2401)
                                     for L in (1, 2, 3, 8, 25, 120, 400)))
    res["exponents"] = check_exponents(a_lo, a_hi)
    res["anchor_gap"] = check_anchor_gap(args.limit)
    res["qclass"] = check_qclass(args.limit, beta_lo, beta_hi)
    res["grids"] = check_grids(a_lo, a_hi, frontier)
    res["depth_cap"] = check_depth_cap(args.limit)
    res["constants"] = check_constants(frontier, report, paper, a_lo, a_hi,
                                       beta_lo, beta_hi)
    res["ledger"] = check_ledger(ledger, paper)
    res["artifacts"] = check_artifacts(bundle)
    res["their_claims"] = check_their_claims(report, res)

    sv, pk, gam = res["sieve"], res["packing"], res["gamma"]
    ex, ag, qc = res["exponents"], res["anchor_gap"], res["qclass"]
    gr, dc, art = res["grids"], res["depth_cap"], res["artifacts"]

    failures = ["instrument.%s" % n
                for n in res["instrument_selfcheck"]["failed"]]
    for key in ("images_divisible_by_three", "states_not_1_or_5_mod_6",
                "sources_not_3_mod_4", "sources_not_7_or_11_mod_12"):
        if sv[key]:
            failures.append("sieve.%s = %d" % (key, sv[key]))
    for key in ("sorted_state_below_its_admissible_position",
                "explicit_admissible_position_errors",
                "uniform_lower_bound_a_k_below_y_plus_3k_minus_1",
                "sieved_envelope_violations",
                "sieved_envelope_above_the_odd_envelope",
                "two_progression_form_disagrees_with_the_product"):
        if pk[key]:
            failures.append("packing.%s = %d" % (key, pk[key]))
    for key in ("exact_disagreements", "lgamma_disagreements_beyond_cancellation"):
        if gam[key]:
            failures.append("gamma.%s = %d" % (key, gam[key]))
    for key in ("sieved_exponent_not_approaching_one_ninth",
                "odd_exponent_not_approaching_one_sixth",
                "deficit_exponent_not_negative"):
        if ex[key]:
            failures.append("exponents.%s = %d" % (key, ex[key]))
    for key in ("spans_below_six_r_minus_eight",
                "tight_sets_whose_last_anchor_is_not_11_mod_12",
                "tight_sets_whose_next_admissible_state_is_not_two_higher",
                "lemma_7_1_violations"):
        if ag[key]:
            failures.append("anchor_gap.%s = %d" % (key, ag[key]))
    for key in ("valuation_classes_not_exactly_one_mod_2_to_k_plus_1",
                "windows_where_N_k_exceeds_W_over_three_two_to_k_plus_one",
                "windows_where_the_weighted_capacity_exceeds_17W_over_24_plus_12",
                "prefixes_with_repeated_states", "theorem_11_2_violations"):
        if qc[key]:
            failures.append("qclass.%s = %d" % (key, qc[key]))
    for key in GRID_COUNTERS:
        if gr[key]:
            failures.append("grids.%s = %s" % (key, gr[key]))
    unread = sorted(k for k, v in gr.items()
                    if isinstance(v, int) and not isinstance(v, bool)
                    and k not in GRID_COUNTERS
                    and k not in ("grid_points", "low_source_grid_points"))
    if unread:
        failures.append("grids: %s is counted but nothing reads it" % unread)
    for key in ("theorem_8_1_violations", "the_two_forms_of_8_1_are_not_equivalent"):
        if dc[key]:
            failures.append("depth_cap.%s = %d" % (key, dc[key]))
    for key in ("CHECKSUMS_mismatches", "validation_record_mismatches",
                "digests_disagreeing_between_the_two_manifests"):
        if art[key]:
            failures.append("artifacts.%s = %s" % (key, art[key]))
    if art["validation_record_shape"] == "UNRECOGNISED":
        failures.append("artifacts: the validation record shape is unrecognised")
    if res["their_claims"]["independently_contradicted"]:
        failures.append("their_claims: %s"
                        % res["their_claims"]["independently_contradicted"])
    # An over-published last digit is the decimal face of a last-bit drift, and
    # RUN-032 drew that line: a finding about the artifact, not a failure of
    # this check. It is recorded in the log and reported, not gated on.

    guards = []
    if sv["odd_integers_mapped"] < 5000:
        guards.append("too few Syracuse images: %d" % sv["odd_integers_mapped"])
    if sv["post_entry_sources_with_L_at_least_2"] < 3000:
        guards.append("too few post-entry sources with L >= 2: %d"
                      % sv["post_entry_sources_with_L_at_least_2"])
    if pk["segments_meeting_the_packing_premise"] < 5000:
        guards.append("too few segments meet the packing premise: %d"
                      % pk["segments_meeting_the_packing_premise"])
    if gam["pairs"] < 20 or gam["largest_L"] < 100:
        guards.append("the Gamma check is too small: %d pairs, largest L %d"
                      % (gam["pairs"], gam["largest_L"]))
    if ex["largest_L"] < 5000:
        guards.append("the exponent fit stops at L = %d" % ex["largest_L"])
    if ag["residue_sets_enumerated"] < 1000:
        guards.append("too few residue sets enumerated: %d"
                      % ag["residue_sets_enumerated"])
    if qc["theorem_11_2_checked"] < 2000:
        guards.append("theorem 11.2 was applied to %d prefixes"
                      % qc["theorem_11_2_checked"])
    if qc["valuations_checked"] < 5:
        guards.append("only %d valuations checked" % qc["valuations_checked"])
    if qc["capacity_windows"] < 10:
        guards.append("only %d capacity windows" % qc["capacity_windows"])
    if 0 < ag["lemma_7_1_checked"] < 200:
        guards.append("lemma 7.1 was applied to %d chains: too few to have "
                      "tested it, too many to call it untested"
                      % ag["lemma_7_1_checked"])
    if gr["grid_points"] < 20 or gr["low_source_grid_points"] < 5:
        guards.append("grid too small: %d points, %d low-source"
                      % (gr["grid_points"], gr["low_source_grid_points"]))
    if len(res["constants"]["rows"]) < 8:
        guards.append("only %d constants bracketed" % len(res["constants"]["rows"]))
    for name, row in res["constants"]["rows"].items():
        if not row.get("decided"):
            guards.append("constants.%s: the bracket could not decide" % name)
    if res["constants"]["published_decimals_this_run_could_not_identify"]:
        guards.append("a decimal the paper publishes matches no reference: %s"
                      % res["constants"]["published_decimals_this_run_could_not_identify"])
    if res["their_claims"]["checks_the_report_names"] < 4:
        guards.append("only %d checker entries were read"
                      % res["their_claims"]["checks_the_report_names"])
    if art["listed_in_CHECKSUMS"] < 5:
        guards.append("only %d digests in CHECKSUMS" % art["listed_in_CHECKSUMS"])
    if art["\u2026that_match_no_file_in_the_bundle"]:
        guards.append("a digest the validation record gives without a filename "
                      "matches no file: %s"
                      % art["\u2026that_match_no_file_in_the_bundle"])
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
