"""RUN-035 — independent recheck of Hard-Zeta round A-U.2d.7.

`Plateau-Reset Quantization Rigidity` (source item 53). 數學戰士「墜衡」.

The round's decidable core is section 3: the crossing slope

    xi_i = D_i/L_i = Q_i/L_i - beta

changes along a nested chain by an EXACT INTEGER ratio,

    xi_{i+1} - xi_i = J_i/(L_i L_{i+1}),   J_i = Q_{i+1}L_i - Q_i L_{i+1}.

Beta cancels identically, so the whole of section 3 is decidable in exact
rational arithmetic with no logarithm anywhere. That is what this gate checks
at scale, together with section 4.4, Lemma 5.1 and section 11, all of which are
likewise pure algebra on the renewal annulus.

Sections 4.3, 5.4, 6, 7 and 9 are NOT of that kind. Every one of them is
derived from B-survival inputs -- the origin-slack budget `H < B`, the endpoint
budget `sum E_i < 2B`, and the overshoot bound `D_i/L_i < 1/(3 y_i ln 2)` --
which a real orbit does not owe anyone. Checking those caps against real orbits
regardless is how RUN-032 flagged 10214 of 10214 chains and learned nothing, so
this gate MEASURES the premises instead and verifies the derivations on a grid.

Every bracket used here is certified inside this file:

  * `ln 2` from `sum_{k>=1} 1/(k 2^k)` with its exact tail bound,
  * `log2 3` by comparing `3^q` against `2^p` as integers,
  * `sqrt 2` from integer square roots,

so no floating-point reference is consulted anywhere in the constants check.

Usage:
    python code/src53_plateau_reset.py --bundle <dir> [--limit N] [--out FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from fractions import Fraction
from math import isqrt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src47_survival_closure import decimal_verdict            # noqa: E402

PAPER = "Hard_Zeta_Phase_II_Round_AU2d7_Plateau_Reset_Quantization_Rigidity_v0.1.md"
REPORT = "Hard_Zeta_AU2d7_checker_report.json"
STDOUT = "checker_stdout.txt"
FRONTIER = "Hard_Zeta_AU2d7_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d7_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d7.json"

# Every integer `check_derivations` reports, named once so that a counter added
# later without being listed here makes the run REFUSE rather than pass quietly.
DERIVATION_COUNTERS = (
    "B_below_L_over_3_y1_ln2_violations",
    "cor_6_2_not_implied_by_thm_6_1",
    "X_r_not_a_root_of_a_x2_plus_b_x",
    "thm_7_1_inversion_violations",
    "cor_7_2_not_implied",
    "cor_9_3_B_below_one_over_L_violations",
    "thm_9_4_depth_bound_violations",
    "log2_1_plus_x_below_x_over_ln2_violations",
)


# ---------------------------------------------------------------------------
# certified rational brackets -- the instrument, checked before it is used
# ---------------------------------------------------------------------------

def ln2_bracket(terms: int = 220) -> tuple[Fraction, Fraction]:
    """`ln 2 = sum_{k>=1} 1/(k 2^k)`, a positive series with an exact tail bound.

    The tail past `N` is `sum_{k>N} 1/(k 2^k) < (1/(N+1)) sum_{k>N} 2^-k
    = 1/((N+1) 2^N)`, so partial sum and partial sum plus that bound straddle
    `ln 2` with no floating point and no library constant involved.
    """
    s = Fraction(0)
    for k in range(1, terms + 1):
        s += Fraction(1, k * (1 << k))
    return s, s + Fraction(1, (terms + 1) << terms)


def beta_bracket(q: int = 10 ** 6) -> tuple[Fraction, Fraction]:
    """Two rationals straddling `log2 3`, certified by construction.

    `floor(beta q)` is `(3^q).bit_length() - 1`, so `p/q < beta < (p+1)/q` with
    nothing to trust. The first version of this function hard-coded a pair of
    rationals believed to be convergents; `190537/120200` is 1.58516..., ABOVE
    beta, so the "lower" bound was an upper bound. The assertion below is why
    that never reached a result -- but the real fix is that almost nothing in
    this file needs a bracket at all, see `beta_sign`.
    """
    p = (3 ** q).bit_length() - 1
    lo, hi = Fraction(p, q), Fraction(p + 1, q)
    assert 2 ** p < 3 ** q, "beta lower bound is not below"
    assert 2 ** (p + 1) > 3 ** q, "beta upper bound is not above"
    return lo, hi


def beta_sign(c: int, k: int) -> int:
    """Sign of `c*beta + k`, exactly.

    `c beta + k = log2(3^c 2^k)`, so the sign is decided by comparing
    `3^c 2^k` with 1 -- an exact rational comparison, no bracket and no
    logarithm. Every positivity claim in section 1 is of this shape.
    """
    v = Fraction(3) ** c * Fraction(2) ** k
    return (v > 1) - (v < 1)


def beta_cmp(a: int, b: int) -> int:
    """Sign of `a/b - beta` for `b > 0`: compare `2^a` with `3^b`."""
    x, y = 2 ** a, 3 ** b
    return (x > y) - (x < y)


def beta_linear_exceeds(c: int, k: int, t: Fraction) -> bool:
    """Is `c*beta + k > t` for a rational `t`? Exact, via `2^N` against `3^D`."""
    if c == 0:
        return Fraction(k) > t
    bound = (t - k) / c
    n, d = bound.numerator, bound.denominator
    return beta_cmp(n, d) < 0 if c > 0 else beta_cmp(n, d) > 0


def sqrt_bracket(lo: Fraction, hi: Fraction, digits: int = 60
                 ) -> tuple[Fraction, Fraction]:
    """Rational bracket for `sqrt(x)` given a rational bracket for `x`."""
    scale = 10 ** digits
    a = isqrt(int(lo * scale * scale))
    b = isqrt(int(hi * scale * scale)) + 1
    return Fraction(a, scale), Fraction(b, scale)


def bracket_decimal(lo: Fraction, hi: Fraction, places: int) -> str | None:
    """A decimal string for a value known to lie in [lo, hi], or None if the
    bracket is too loose to pin `places` digits. Truncating, never rounding --
    `decimal_verdict` does the rounding, and doing it twice is how RUN-029
    published a finding against correct arithmetic."""
    scale = 10 ** places
    a, b = int(lo * scale), int(hi * scale)
    if a != b:
        return None
    sign = "-" if a < 0 else ""
    a = abs(a)
    return "%s%d.%s" % (sign, a // scale, str(a % scale).zfill(places))


# ---------------------------------------------------------------------------
# orbits, first crossings, and the active nested chains
# ---------------------------------------------------------------------------

def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def accelerated(start: int, max_steps: int = 6000) -> tuple[list[int], list[int]]:
    y, word, values = start, [], [start]
    while y != 1 and len(word) < max_steps:
        t = 3 * y + 1
        k = v2(t)
        word.append(k)
        y = t >> k
        values.append(y)
    return word, values


def cumulative(word: list[int]) -> list[int]:
    out, run = [0], 0
    for q in word:
        run += q
        out.append(run)
    return out


def slack_is_smaller(K: list[int], u: int, s: int) -> bool:
    """`delta_u < delta_s`, decided by comparing `3^(u-s)` with `2^(K_u-K_s)`."""
    return Fraction(3) ** (u - s) < Fraction(2) ** (K[u] - K[s])


def crossings_and_stalks(K: list[int], n: int
                         ) -> tuple[list[int | None], list[tuple[int, ...]]]:
    """First crossings, plus the stalk `{s <= t : e(s) > t}` at every position.

    THE STALK IS THE CHAIN. Section 1 asks for `s_1 < ... < s_r <= t < e_i`, so
    an active nested chain is exactly the set of first-crossing intervals
    covering one position -- which laminarity totally orders by inclusion, and
    which the sweep already has on its stack.

    Building the chain instead from the records of `delta` looks equivalent and
    is not: records only guarantee `delta` increasing, and two record intervals
    can be DISJOINT, which makes `h_i = e_i - e_{i+1}` negative. That admitted
    33052 edges with `Delta_i < 1` out of 86539 and would have been published as
    a violation of a boxed claim that in fact holds everywhere.
    """
    e: list[int | None] = [None] * (n + 1)
    stack: list[int] = []
    stalks: list[tuple[int, ...]] = []
    for u in range(n + 1):
        while stack and slack_is_smaller(K, u, stack[-1]):
            e[stack.pop()] = u
        stack.append(u)
        stalks.append(tuple(stack))
    return e, stalks


def chains_of(K: list[int], n: int, e: list[int | None],
              stalks: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    out, seen = [], set()
    for st in stalks:
        ch = tuple(s for s in st if e[s] is not None)
        if len(ch) < 2 or ch in seen:
            continue
        seen.add(ch)
        out.append(ch)
    return out


_UB: dict[int, Fraction] = {}


def u_beta(L: int) -> Fraction:
    """`U_beta(L) = (1/3) sum_{j<L} 2^(-{beta j})`, exactly (RUN-027)."""
    if L in _UB:
        return _UB[L]
    total, p3 = Fraction(0), 1
    for j in range(L):
        total += Fraction(1 << (p3.bit_length() - 1), p3)
        p3 *= 3
    _UB[L] = total / 3
    return _UB[L]


# ---------------------------------------------------------------------------
# section 3, section 4.4, Lemma 5.1 -- pure algebra, no survival input
# ---------------------------------------------------------------------------

def check_slope_quantization(limit: int, beta_lo: Fraction, beta_hi: Fraction
                             ) -> dict:
    t = {
        "orbits": 0, "chains": 0, "edges": 0, "max_depth": 0, "max_L": 0,
        "plateau_edges": 0, "strict_edges": 0, "unit_strict_edges": 0,
        "genuine_resets_J_negative": 0, "unit_resets": 0, "J_zero_edges": 0,
        "jump_law_violations": 0,
        "quantization_violations": 0,
        "quantization_below_one_over_L_squared": 0,
        "renewal_identity_violations": 0,
        "endpoints_not_nested_h_negative": 0,
        "A_not_positive": 0, "D_not_positive": 0, "E_not_positive": 0,
        "plateau_J_not_equal_to_Pi": 0,
        "plateau_determinant_below_one": 0,
        "plateau_Pi_two_forms_disagree": 0,
        "strict_determinant_below_one": 0,
        "strict_Delta_two_forms_disagree": 0,
        "strict_J_formula_violations": 0,
        "theorem_4_4_violations": 0,
        "lemma_5_1_chains_checked": 0, "lemma_5_1_violations": 0,
        "L_not_strictly_decreasing": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, stalks = crossings_and_stalks(K, n)
        t["orbits"] += 1
        for ch in chains_of(K, n, e, stalks):
            t["chains"] += 1
            t["max_depth"] = max(t["max_depth"], len(ch))
            L1 = e[ch[0]] - ch[0]
            t["max_L"] = max(t["max_L"], L1)
            plateau_mass = 0
            for a, b in zip(ch, ch[1:]):
                ea, eb = e[a], e[b]
                La, Lb = ea - a, eb - b
                Qa, Qb = K[ea] - K[a], K[eb] - K[b]
                g, p = b - a, K[b] - K[a]
                h, r = ea - eb, K[ea] - K[eb]
                t["edges"] += 1
                if h < 0:
                    t["endpoints_not_nested_h_negative"] += 1
                if La <= Lb:
                    t["L_not_strictly_decreasing"] += 1

                # every quantity is a beta-linear pair (coefficient, constant),
                # and its sign is decided exactly by `3^c 2^k` against 1
                A, E = (g, -p), (-h, r)
                Di, Dj = (-La, Qa), (-Lb, Qb)
                for pair, key in ((A, "A_not_positive"), (Di, "D_not_positive"),
                                  (Dj, "D_not_positive")):
                    if beta_sign(*pair) <= 0:
                        t[key] += 1
                if h > 0 and beta_sign(*E) <= 0:
                    t["E_not_positive"] += 1

                # Theorem 3.2 -- beta cancels, so this is exact in Q
                J = Qb * La - Qa * Lb
                if Fraction(Qb, Lb) - Fraction(Qa, La) != Fraction(J, La * Lb):
                    t["jump_law_violations"] += 1
                if J == 0:
                    t["J_zero_edges"] += 1
                else:
                    if abs(Fraction(J, La * Lb)) < Fraction(1, La * Lb):
                        t["quantization_violations"] += 1
                    if abs(Fraction(J, La * Lb)) < Fraction(1, L1 * L1):
                        t["quantization_below_one_over_L_squared"] += 1

                if (A[0] + Di[0] - Dj[0] - E[0],
                        A[1] + Di[1] - Dj[1] - E[1]) != (0, 0):
                    t["renewal_identity_violations"] += 1

                if h == 0:
                    t["plateau_edges"] += 1
                    plateau_mass += g * Lb
                    Pi = Qb * g - p * Lb
                    if J != Pi:
                        t["plateau_J_not_equal_to_Pi"] += 1
                    if Pi < 1:
                        t["plateau_determinant_below_one"] += 1
                    # Pi_i = g_i D_{i+1} + L_{i+1} A_i, as a beta-linear pair
                    two = (g * Dj[0] + Lb * A[0], g * Dj[1] + Lb * A[1])
                    if two != (0, Pi):
                        t["plateau_Pi_two_forms_disagree"] += 1
                else:
                    t["strict_edges"] += 1
                    Delta = r * g - p * h
                    if Delta < 1:
                        t["strict_determinant_below_one"] += 1
                    if Delta == 1:
                        t["unit_strict_edges"] += 1
                    two = (g * E[0] + h * A[0], g * E[1] + h * A[1])
                    if two != (0, Delta):
                        t["strict_Delta_two_forms_disagree"] += 1
                    form = ((g + h) * Dj[0] - Lb * (E[0] - A[0]),
                            (g + h) * Dj[1] - Lb * (E[1] - A[1]))
                    if form != (0, J):
                        t["strict_J_formula_violations"] += 1
                    if J < 0:
                        t["genuine_resets_J_negative"] += 1
                        if Delta == 1:
                            t["unit_resets"] += 1
                        # Theorem 4.4: E_i - A_i > 1/L_{i+1}, decided exactly
                        if not beta_linear_exceeds(E[0] - A[0], E[1] - A[1],
                                                   Fraction(1, Lb)):
                            t["theorem_4_4_violations"] += 1
            # Lemma 5.1 -- sum over plateau edges of g_i L_{i+1} < L^2/2
            t["lemma_5_1_chains_checked"] += 1
            if not Fraction(plateau_mass) < Fraction(L1 * L1, 2):
                t["lemma_5_1_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# section 11 -- unit-reset orientation, also pure algebra
# ---------------------------------------------------------------------------

def check_orientation(limit: int) -> dict:
    t = {
        "unit_strict_edges": 0, "annulus_premise_holds": 0,
        "annulus_premise_fails": 0,
        "mediant_below_beta": 0,
        "mediant_below_beta_with_J_not_positive": 0,
        "unit_resets": 0,
        "reset_child_slope_not_between_beta_and_mediant": 0,
        "reset_mediant_not_above_beta": 0,
        "farey_neighbour_identity_violations": 0,
        "child_denominator_below_2g_plus_h": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, stalks = crossings_and_stalks(K, n)
        for ch in chains_of(K, n, e, stalks):
            for a, b in zip(ch, ch[1:]):
                ea, eb = e[a], e[b]
                h = ea - eb
                if h <= 0:
                    continue
                g, p = b - a, K[b] - K[a]
                r = K[ea] - K[eb]
                if r * g - p * h != 1:
                    continue
                t["unit_strict_edges"] += 1
                La, Lb = ea - a, eb - b
                Qa, Qb = K[ea] - K[a], K[eb] - K[b]
                J = Qb * La - Qa * Lb
                mu = Fraction(p + r, g + h)
                child = Fraction(Qb, Lb)
                # p/g < beta < r/h, mu vs beta, child vs beta: four comparisons
                # of a small rational against beta, each exactly `2^a` vs `3^b`
                if beta_cmp(p, g) < 0 and beta_cmp(r, h) > 0:
                    t["annulus_premise_holds"] += 1
                else:
                    t["annulus_premise_fails"] += 1
                # (p+r)g - p(g+h) = rg - ph = 1, so p/g and mu are Farey
                # neighbours; this is an integer identity, not an estimate.
                if (p + r) * g - p * (g + h) != 1:
                    t["farey_neighbour_identity_violations"] += 1
                if beta_cmp(p + r, g + h) < 0:
                    t["mediant_below_beta"] += 1
                    if not J > 0:
                        t["mediant_below_beta_with_J_not_positive"] += 1
                if J < 0:
                    t["unit_resets"] += 1
                    if not (beta_cmp(Qb, Lb) > 0 and child < mu):
                        t["reset_child_slope_not_between_beta_and_mediant"] += 1
                    if not beta_cmp(p + r, g + h) > 0:
                        t["reset_mediant_not_above_beta"] += 1
                    if child.denominator < 2 * g + h:
                        t["child_denominator_below_2g_plus_h"] += 1
    return t


# ---------------------------------------------------------------------------
# the B-survival premises -- MEASURED, not imposed
# ---------------------------------------------------------------------------

def check_premises(limit: int, beta_lo: Fraction, beta_hi: Fraction,
                   a_lo: Fraction, a_hi: Fraction) -> dict:
    """How often does a real orbit satisfy what sections 4.3-9 assume?

    RUN-032 flagged 10214 of 10214 chains by applying a cap whose corridor
    premise none of them met. The premise comes first here, and the caps are
    applied only where it holds.
    """
    t = {
        "chains": 0, "intervals": 0,
        "u_beta_above_L_over_3": 0,
        "survival_bound_holds": 0, "survival_bound_fails": 0,
        "survival_bound_undecided": 0,
        "chains_where_every_interval_survives": 0,
        "chains_meeting_the_origin_slack_budget_H_lt_B": 0,
        "chains_meeting_the_endpoint_budget_sumE_lt_2B": 0,
        "chains_meeting_every_premise": 0,
        "theorem_4_3_checked": 0, "theorem_4_3_violations": 0,
        "theorem_5_4_checked": 0, "theorem_5_4_violations": 0,
        "theorem_6_1_checked": 0, "theorem_6_1_violations": 0,
        "high_source_chains": 0, "high_source_undecided": 0,
        "high_source_with_the_survival_slope_bound": 0,
        "high_source_slope_bound_undecided": 0,
        "high_source_all_slopes_equal": 0,
        "high_source_without_plateaus": 0,
        "high_source_depth_at_most_4": 0,
        "high_source_max_depth": 0,
        "chains_with_more_than_one_slope": 0,
        "distinct_slopes_closer_than_one_over_L_squared": 0,
    }
    r2_lo, r2_hi = sqrt_bracket(Fraction(2), Fraction(2))
    c2_lo = 6 + 4 * r2_lo                    # (2 + sqrt 2)^2, lower bound
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, stalks = crossings_and_stalks(K, n)
        for ch in chains_of(K, n, e, stalks):
            t["chains"] += 1
            r, s1, sr = len(ch), ch[0], ch[-1]
            L, y1 = e[s1] - s1, values[s1]
            if u_beta(L) > Fraction(L, 3):
                t["u_beta_above_L_over_3"] += 1
            u = u_beta(L) / y1
            b_lo = (2 * u / (2 + u)) * a_lo       # ln(1+u) >= 2u/(2+u)
            b_hi = u * a_hi                        # ln(1+u) <= u

            survives = True
            for s in ch:
                t["intervals"] += 1
                Li, Qi, yi = e[s] - s, K[e[s]] - K[s], values[s]
                lhs_lo = (Fraction(Qi) - beta_hi * Li) * 3 * yi
                lhs_hi = (Fraction(Qi) - beta_lo * Li) * 3 * yi
                if lhs_hi < Fraction(Li) * a_lo:
                    t["survival_bound_holds"] += 1
                elif lhs_lo >= Fraction(Li) * a_hi:
                    t["survival_bound_fails"] += 1
                    survives = False
                else:
                    t["survival_bound_undecided"] += 1
                    survives = False
            if survives:
                t["chains_where_every_interval_survives"] += 1

            Hc, Hk = sr - s1, -(K[sr] - K[s1])
            H_hi = Hc * (beta_hi if Hc >= 0 else beta_lo) + Hk
            D1c, D1k = -(e[s1] - s1), K[e[s1]] - K[s1]
            Drc, Drk = -(e[sr] - sr), K[e[sr]] - K[sr]
            Ec, Ek = Hc + D1c - Drc, Hk + D1k - Drk
            E_hi = Ec * (beta_hi if Ec >= 0 else beta_lo) + Ek
            origin_ok = H_hi < b_lo
            endpoint_ok = E_hi < 2 * b_lo
            if origin_ok:
                t["chains_meeting_the_origin_slack_budget_H_lt_B"] += 1
            if endpoint_ok:
                t["chains_meeting_the_endpoint_budget_sumE_lt_2B"] += 1

            plateaus = sum(1 for a, b in zip(ch, ch[1:]) if e[a] == e[b])
            d = (r - 1) - plateaus
            if origin_ok and endpoint_ok and survives:
                t["chains_meeting_every_premise"] += 1
                t["theorem_4_3_checked"] += 1
                if not Fraction(d * d) < c2_lo * L * b_lo:
                    t["theorem_4_3_violations"] += 1
                cap_p = Fraction(L * L) * a_lo / (3 * y1) + 2 * L * b_lo
                t["theorem_5_4_checked"] += 1
                if not Fraction(plateaus) < cap_p:
                    t["theorem_5_4_violations"] += 1
                t["theorem_6_1_checked"] += 1
                root_lo, _ = sqrt_bracket(Fraction(L) * b_lo, Fraction(L) * b_lo)
                if not Fraction(r - 1) < cap_p + (2 + r2_lo) * root_lo:
                    t["theorem_6_1_violations"] += 1

            slopes = {Fraction(K[e[s]] - K[s], e[s] - s) for s in ch}
            if len(slopes) > 1:
                t["chains_with_more_than_one_slope"] += 1
                ordered = sorted(slopes)
                for x, y in zip(ordered, ordered[1:]):
                    if y - x < Fraction(1, L * L):
                        t["distinct_slopes_closer_than_one_over_L_squared"] += 1

            if Fraction(y1) > Fraction(L * L) * a_hi / 3:
                t["high_source_chains"] += 1
                t["high_source_max_depth"] = max(t["high_source_max_depth"], r)
                if len(slopes) == 1:
                    t["high_source_all_slopes_equal"] += 1
                if plateaus == 0:
                    t["high_source_without_plateaus"] += 1
                if r <= 4:
                    t["high_source_depth_at_most_4"] += 1
                verdicts = []
                for s in ch:
                    Li, Qi = e[s] - s, K[e[s]] - K[s]
                    xi_lo = (Fraction(Qi) - beta_hi * Li) / Li
                    xi_hi = (Fraction(Qi) - beta_lo * Li) / Li
                    thr = Fraction(1, L * L)
                    verdicts.append(True if xi_hi < thr
                                    else False if xi_lo >= thr else None)
                if None in verdicts:
                    t["high_source_slope_bound_undecided"] += 1
                elif all(verdicts):
                    t["high_source_with_the_survival_slope_bound"] += 1
            elif not Fraction(y1) < Fraction(L * L) * a_lo / 3:
                t["high_source_undecided"] += 1
    return t


# ---------------------------------------------------------------------------
# the derivations, on a grid -- these are implications, not orbit facts
# ---------------------------------------------------------------------------

def check_derivations(a_lo: Fraction, a_hi: Fraction) -> dict:
    """Do the conditional results actually follow from their own premises?

    A cap no real orbit can be tested against is not therefore unfalsifiable:
    its DERIVATION is arithmetic, and arithmetic can be checked.
    """
    r2_lo, r2_hi = sqrt_bracket(Fraction(2), Fraction(2))
    b2_lo = (6 + 4 * r2_lo) * a_lo / 3          # b^2 = (6+4sqrt2)/(3 ln 2)
    b2_hi = (6 + 4 * r2_hi) * a_hi / 3
    b_lo, b_hi = sqrt_bracket(b2_lo, b2_hi)
    t = {
        "grid_points": 0,
        "B_below_L_over_3_y1_ln2_violations": 0,
        "cor_6_2_not_implied_by_thm_6_1": 0,
        "X_r_not_a_root_of_a_x2_plus_b_x": 0,
        "thm_7_1_inversion_violations": 0,
        "cor_7_2_not_implied": 0,
        "cor_9_3_B_below_one_over_L_violations": 0,
        "thm_9_4_depth_bound_violations": 0,
        "log2_1_plus_x_below_x_over_ln2_violations": 0,
    }
    # 2 b^2 / a = 2(6+4 sqrt 2)/3 = (12+8 sqrt 2)/3 -- the ln 2 cancels, so the
    # round's `7.7712...` is ALGEBRAIC, and `< 8` is decidable in exact rationals.
    two_b2_over_a_lo = (12 + 8 * r2_lo) / 3
    two_b2_over_a_hi = (12 + 8 * r2_hi) / 3
    t["two_b_squared_over_a_is_algebraic"] = bracket_decimal(
        two_b2_over_a_lo, two_b2_over_a_hi, 12)
    t["two_b_squared_over_a_below_8"] = bool(two_b2_over_a_hi < 8)

    for L in (2, 3, 5, 8, 13, 21, 34, 55, 89):
        for y1 in (3, 7, 27, 255, 4095, 65535):
            u = u_beta(L) / y1
            B_lo = (2 * u / (2 + u)) * a_lo
            B_hi = u * a_hi
            # log2(1+x) < x/ln2, used to get B < L/(3 y1 ln 2)
            if not B_hi < u * a_hi + Fraction(1, 10 ** 30):
                t["log2_1_plus_x_below_x_over_ln2_violations"] += 1
            if not B_hi < Fraction(L) * a_hi / (3 * y1) + Fraction(1, 10 ** 30):
                t["B_below_L_over_3_y1_ln2_violations"] += 1
            x_lo, x_hi = sqrt_bracket(Fraction(L * L, y1), Fraction(L * L, y1))
            for r in (2, 3, 5, 9, 17, 33, 65):
                t["grid_points"] += 1
                # Theorem 6.1's right side, then Corollary 6.2's; the second
                # must be the weaker of the two, since it is 6.1 relaxed.
                root_hi = sqrt_bracket(Fraction(L) * B_hi, Fraction(L) * B_hi)[1]
                master_hi = (Fraction(L * L) * a_hi / (3 * y1) + 2 * L * B_hi
                             + (2 + r2_hi) * root_hi)
                explicit_lo = Fraction(L * L) * a_lo / y1 + b_lo * x_lo
                if master_hi > explicit_lo:
                    t["cor_6_2_not_implied_by_thm_6_1"] += 1
                # X_r, the positive root of a x^2 + b x = r - 1
                disc_lo, disc_hi = sqrt_bracket(
                    b2_lo + 4 * a_lo * (r - 1), b2_hi + 4 * a_hi * (r - 1))
                X_lo = (disc_lo - b_hi) / (2 * a_hi)
                X_hi = (disc_hi - b_lo) / (2 * a_lo)
                if not (a_lo * X_lo * X_lo + b_lo * X_lo <= r - 1
                        <= a_hi * X_hi * X_hi + b_hi * X_hi):
                    t["X_r_not_a_root_of_a_x2_plus_b_x"] += 1
                # Theorem 7.1: r - 1 < a x^2 + b x  =>  x > X_r  =>  y1 < L^2/X_r^2
                if a_hi * x_hi * x_hi + b_hi * x_hi > r - 1:
                    if X_hi > 0 and not Fraction(y1) < Fraction(L * L) / (X_lo * X_lo):
                        t["thm_7_1_inversion_violations"] += 1
                # Corollary 7.2 for r >= 9
                if r >= 9 and a_hi * x_hi * x_hi + b_hi * x_hi > r - 1:
                    if not Fraction(y1) < 2 * Fraction(L * L) * a_hi / (r - 1):
                        t["cor_7_2_not_implied"] += 1
                # Corollary 9.3 / Theorem 9.4 under the high-source hypothesis
                if Fraction(y1) > Fraction(L * L) * a_hi / 3:
                    if not B_hi < Fraction(1, L):
                        t["cor_9_3_B_below_one_over_L_violations"] += 1
                    root = sqrt_bracket(Fraction(L) * B_hi, Fraction(L) * B_hi)[1]
                    if not (2 + r2_hi) * root < 4:
                        t["thm_9_4_depth_bound_violations"] += 1
    t["b_value"] = bracket_decimal(b_lo, b_hi, 12)
    return t


# ---------------------------------------------------------------------------
# constants, against certified brackets rather than a floating-point reference
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, paper: str, a_lo: Fraction, a_hi: Fraction
                    ) -> dict:
    import struct

    def bits(x: float) -> int:
        return struct.unpack("<q", struct.pack("<d", x))[0]

    r2_lo, r2_hi = sqrt_bracket(Fraction(2), Fraction(2))
    b2_lo = (6 + 4 * r2_lo) * a_lo / 3
    b2_hi = (6 + 4 * r2_hi) * a_hi / 3
    b_lo, b_hi = sqrt_bracket(b2_lo, b2_hi)
    rho = Fraction("4.1164")
    brackets = {
        "one_over_ln2": (a_lo, a_hi),
        "high_source_threshold_coefficient_1_over_3ln2": (a_lo / 3, a_hi / 3),
        "strict_explicit_coefficient": (b_lo, b_hi),
        "depth_source_simple_coefficient_2_over_ln2": (2 * a_lo, 2 * a_hi),
        "disjoint_backbone_power": (1 / (1 + 1 / (rho + 1)),) * 2,
        "dense_overlap_required_power": (1 - 1 / (1 + 1 / (rho + 1)),) * 2,
    }
    published = frontier["constants"]
    rows, drifted, unbracketed = {}, [], []
    for name, (lo, hi) in brackets.items():
        if name not in published:
            unbracketed.append(name)
            continue
        value = published[name]
        mid = bracket_decimal(lo, hi, 30)
        if mid is None:
            unbracketed.append(name)
            continue
        drift = abs(bits(value) - bits(float(Fraction(mid))))
        rows[name] = {"published": value, "reference": mid[:22],
                      "ulps_from_the_nearest_double": drift}
        if drift:
            drifted.append(name)
    # the two inherited powers must still sum to exactly one
    pair_sum = (published.get("disjoint_backbone_power", 0)
                + published.get("dense_overlap_required_power", 0))
    # 2/ln2 must be exactly twice 1/ln2 as doubles -- multiplying by two is exact
    doubling = (published.get("depth_source_simple_coefficient_2_over_ln2")
                == 2 * published.get("one_over_ln2", 0))

    # DISCOVER the paper's published decimals rather than asserting them: a
    # hard-coded digit string is a second place to make the typo the check
    # exists to catch, and a decimal I cannot identify is itself worth naming.
    references = {
        "1/ln2": (a_lo, a_hi),
        "1/(3 ln2)": (a_lo / 3, a_hi / 3),
        "2/ln2": (2 * a_lo, 2 * a_hi),
        "(2+sqrt2)/sqrt(3 ln2)": (b_lo, b_hi),
        "(12+8 sqrt2)/3": ((12 + 8 * r2_lo) / 3, (12 + 8 * r2_hi) / 3),
        "sqrt 2": (r2_lo, r2_hi),
    }
    inline, unidentified = {}, []
    for shown in re.findall(r"=\s*\n?([0-9]+\.[0-9]{4,})\\ldots", paper):
        places = len(shown.split(".")[1])
        hit = None
        for name, (lo, hi) in references.items():
            ref = bracket_decimal(lo, hi, places + 6)
            if ref is None:
                continue
            if abs(Fraction(ref) - Fraction(shown)) < Fraction(1, 10 ** places):
                hit = (name, ref)
                break
        if hit is None:
            unidentified.append(shown)
            continue
        name, ref = hit
        inline[name] = dict(decimal_verdict(shown, ref), published=shown)
    return {
        "rows": rows, "off_by_at_least_one_ulp": drifted,
        "not_bracketed_here": unbracketed,
        "rho_star_agrees": published.get("rho_star_inherited") == 4.1164,
        "the_two_inherited_powers_sum_to_one": pair_sum == 1.0,
        "2_over_ln2_is_exactly_twice_1_over_ln2": doubling,
        "the_paper_and_the_frontier_agree_on_1_over_3ln2": (
            published.get("high_source_threshold_coefficient_1_over_3ln2")
            == float(Fraction(inline["1/(3 ln2)"]["published"]))
            if "1/(3 ln2)" in inline else None),
        "inline_decimals_in_the_paper": inline,
        "published_decimals_this_run_could_not_identify": unidentified,
    }


# ---------------------------------------------------------------------------
# the NEW artifact: a machine-readable theorem ledger
# ---------------------------------------------------------------------------

def check_ledger(ledger: dict, paper: str, frontier: dict, report: dict) -> dict:
    """The bundle states its ledger TWICE -- as prose in section 22 and as JSON.

    Two renderings of one thing is a fidelity test that needs no mathematics:
    count the paper's own numbered entries and compare. This is a structural
    count, not a keyword search, because a name-based grep tests one guessed
    encoding and cannot tell `absent` from `written differently`.
    """
    prose_start = paper.index("## 22.1 Proved internally")
    prose_end = paper.index("## 22.2 Inherited")
    prose_items = re.findall(r"^(\d+)\. ", paper[prose_start:prose_end], re.M)
    inherited = re.findall(r"^- A-U\.2d\.\d", paper[
        paper.index("## 22.2 Inherited"):paper.index("## 22.3 External")], re.M)
    external = re.findall(r"^- ", paper[
        paper.index("## 22.3 External"):paper.index("## 22.4 Context")], re.M)
    context = re.findall(r"^- ", paper[
        paper.index("## 22.4 Context"):paper.index("# 23. Checker scope")], re.M)
    no_go_headings = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)
    theorems = re.findall(r"^## Theorem (\d+\.\d+) — (.+)$", paper, re.M)

    missing_arxiv = [src["source"] for src in ledger.get("external_inputs", [])
                     for tok in re.findall(r"arXiv:([0-9.v]+)", src["source"])
                     if tok.split("v")[0] not in paper]
    inherited_named = [x for x in ledger.get("inherited_internal", [])
                       if re.match(r"A-U\.2d\.\d", x)
                       and re.match(r"A-U\.2d\.\d", x).group(0) in paper]
    return {
        "paper_section_22_1_numbered_results": len(prose_items),
        "ledger_internal_theorems": len(ledger.get("internal_theorems", [])),
        "internal_shortfall_against_the_paper_s_own_list":
            len(prose_items) - len(ledger.get("internal_theorems", [])),
        "paper_numbered_theorem_headings": len(theorems),
        "paper_no_go_headings": len(no_go_headings),
        "ledger_no_go_entries": len(ledger.get("no_go", [])),
        "no_go_shortfall": len(no_go_headings) - len(ledger.get("no_go", [])),
        "paper_section_22_2_inherited": len(inherited),
        "ledger_inherited": len(ledger.get("inherited_internal", [])),
        "inherited_rounds_named_and_present_in_the_paper": len(inherited_named),
        "paper_section_22_3_external": len(external),
        "ledger_external": len(ledger.get("external_inputs", [])),
        "external_sources_whose_arxiv_id_is_absent_from_the_paper": missing_arxiv,
        "paper_section_22_4_context": len(context),
        "ledger_context_only": len(ledger.get("context_only", [])),
        "round_agrees_across_ledger_frontier_and_report":
            ledger.get("round") == frontier.get("round") == report.get("round"),
        "next_round_agrees_between_ledger_and_frontier":
            ledger.get("next") == frontier.get("next_round"),
        "status_agrees_between_ledger_and_frontier":
            ledger.get("status") == frontier.get("status"),
        "ledger_status": ledger.get("status"),
        "frontier_status": frontier.get("status"),
        "no_go_headings_in_the_paper": [h for h, _ in no_go_headings],
        "paper_no_go_titles_with_no_ledger_entry_sharing_a_keyword": [
            "%s %s" % (num, title) for num, title in no_go_headings
            if not any(w in entry.lower() for entry in ledger.get("no_go", [])
                       for w in re.findall(r"[a-z-]{6,}", title.lower()))],
        "the_ledger_status_is_the_weaker_of_the_two": (
            ledger.get("status", "") in frontier.get("status", "")
            and ledger.get("status") != frontier.get("status")),
    }


# ---------------------------------------------------------------------------

def check_shipped_examples(report: dict) -> dict:
    """Recompute the checker's own unit-reset examples from their integers."""
    rows, bad = [], []
    seen = set()
    for ex in report.get("unit_reset_examples", []):
        key = tuple(sorted(ex.items()))
        if key in seen:
            continue
        seen.add(key)
        g, p, h, r = ex["g"], ex["p"], ex["h"], ex["r"]
        Li, Lj, Qi, Qj = ex["Li"], ex["Lj"], ex["Qi"], ex["Qj"]
        mu = Fraction(p + r, g + h)
        child = Fraction(Qj, Lj)
        facts = {
            "J_recomputes": Qj * Li - Qi * Lj == ex["J"],
            "J_negative": ex["J"] < 0,
            "determinant_is_one": r * g - p * h == 1,
            "L_consistent": Lj == Li - h - g,
            "Q_consistent": Qj == Qi - r - p,
            "annulus_brackets_beta": beta_cmp(p, g) < 0 and beta_cmp(r, h) > 0,
            "mediant_above_beta": beta_cmp(p + r, g + h) > 0,
            "child_between_beta_and_mediant": beta_cmp(Qj, Lj) > 0 and child < mu,
            "child_denominator_at_least_2g_plus_h":
                child.denominator >= 2 * g + h,
        }
        rows.append({**ex, "mediant": "%d/%d" % (mu.numerator, mu.denominator),
                     "child_slope": "%d/%d" % (child.numerator, child.denominator),
                     **facts})
        if not all(facts.values()):
            bad.append(ex)
    return {"distinct_examples": len(rows), "rows": rows,
            "examples_failing_a_clause": bad,
            "clauses_per_example": 9}


def check_artifacts(bundle: pathlib.Path) -> dict:
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    if "artifact_sha256_before_manifest" in validation:
        listed = dict(validation["artifact_sha256_before_manifest"])
        shape = "dict keyed by filename (item 50)"
        digests = {k: v for k, v in listed.items()}
    elif isinstance(validation.get("files"), list):
        listed = {rec["file"]: rec for rec in validation["files"]}
        shape = "list of file records (items 51, 52)"
        digests = {k: v["sha256"] for k, v in listed.items()}
    elif isinstance(validation.get("files"), dict):
        listed = validation["files"]
        shape = "dict of file records keyed by filename (item 53)"
        digests = {k: v["sha256"] for k, v in listed.items()}
    else:
        listed, digests, shape = {}, {}, "UNRECOGNISED"

    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    verified, mismatched = [], []
    for name, want in digests.items():
        path = bundle / name
        if not path.exists():
            mismatched.append({"file": name, "why": "listed but absent"})
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        (verified if got == want else mismatched).append(
            name if got == want else {"file": name, "listed": want, "actual": got})
    a = (bundle / REPORT).read_bytes()
    b = (bundle / STDOUT).read_bytes()
    return {
        "validation_record_shape": shape,
        "files_in_the_bundle": len(present),
        "files_listed_in_the_validation_record": len(digests),
        "verified": len(verified),
        "sha256_mismatches": mismatched,
        "present_but_not_covered": [p for p in present if p not in digests],
        "the_record_says_all_ok": validation.get("all_ok"),
        "report_and_stdout_byte_identical": a == b,
        "stdout_is_the_report_plus": (b[len(a):].decode("utf-8", "replace")
                                      if b.startswith(a) and b != a else ""),
        "report_bytes": len(a), "stdout_bytes": len(b),
    }


def check_their_claims(report: dict, res: dict) -> dict:
    sq, ori, pre = res["slope_quantization"], res["orientation"], res["premises"]
    mapping = {
        "crossing-slope integer jump xi_{i+1}-xi_i = J_i/(L_i L_{i+1}) on "
        "random next-smaller chains":
            sq["jump_law_violations"] == 0 and sq["quantization_violations"] == 0,
        "plateau J_i = Pi_i >= 1 and strict determinant Delta_i >= 1":
            sq["plateau_J_not_equal_to_Pi"] == 0
            and sq["plateau_determinant_below_one"] == 0
            and sq["strict_determinant_below_one"] == 0,
        "rational separation threshold 1/L^2 underlying high-source "
        "equal-slope collapse":
            pre["distinct_slopes_closer_than_one_over_L_squared"] == 0
            and pre["chains_with_more_than_one_slope"] > 0,
        "global plateau determinant split and sum g_i L_{i+1} < L^2/2 ingredient":
            sq["plateau_Pi_two_forms_disagree"] == 0
            and sq["plateau_determinant_below_one"] == 0
            and sq["lemma_5_1_violations"] == 0,
        "unit strict reset orientation: J<0 implies upper mediant and "
        "child-denominator lower bound":
            ori["reset_child_slope_not_between_beta_and_mediant"] == 0
            and ori["reset_mediant_not_above_beta"] == 0
            and ori["child_denominator_below_2g_plus_h"] == 0,
    }
    stated = list(report.get("verified_statements", report.get("verified_claims", [])))
    checked = {c: mapping[c] for c in stated if c in mapping}
    return {
        "the_key_the_report_uses": ("verified_statements" if "verified_statements"
                                    in report else "verified_claims"),
        "claims_the_checker_states": len(stated),
        "independently_confirmed": sum(1 for v in checked.values() if v),
        "independently_contradicted": sorted(k for k, v in checked.items() if not v),
        "not_covered_by_this_run": [c for c in stated if c not in mapping],
        "the_checker_s_own_not_verified_list": report.get("not_verified", []),
    }


# ---------------------------------------------------------------------------

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                                   # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=4000)
    ap.add_argument("--out")
    args = ap.parse_args()
    bundle = pathlib.Path(args.bundle)

    paper = (bundle / PAPER).read_text(encoding="utf-8")
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))

    beta_lo, beta_hi = beta_bracket()
    ln2_lo, ln2_hi = ln2_bracket()
    a_lo, a_hi = 1 / ln2_hi, 1 / ln2_lo

    res: dict = {
        "tool": "src53_plateau_reset.py",
        "round": report.get("round"),
        "orbit_limit": args.limit,
        "instrument": {
            "beta_bracket": ["%d/%d" % (beta_lo.numerator, beta_lo.denominator),
                             "%d/%d" % (beta_hi.numerator, beta_hi.denominator)],
            "beta_bracket_certified_by": "3^q > 2^p and 3^q' < 2^p' as integers",
            "ln2_bracket_width_below": "1e-%d" % (
                len(str((ln2_hi - ln2_lo).denominator)) - 1),
            "ln2_certified_by": "sum 1/(k 2^k) with tail < 1/((N+1) 2^N)",
            "one_over_ln2_to_20_places": bracket_decimal(a_lo, a_hi, 20),
        },
    }
    res["slope_quantization"] = check_slope_quantization(args.limit, beta_lo, beta_hi)
    res["orientation"] = check_orientation(args.limit)
    res["premises"] = check_premises(args.limit, beta_lo, beta_hi, a_lo, a_hi)
    res["derivations"] = check_derivations(a_lo, a_hi)
    res["constants"] = check_constants(frontier, paper, a_lo, a_hi)
    res["ledger"] = check_ledger(ledger, paper, frontier, report)
    res["shipped_examples"] = check_shipped_examples(report)
    res["artifacts"] = check_artifacts(bundle)
    res["their_claims"] = check_their_claims(report, res)

    sq, ori = res["slope_quantization"], res["orientation"]
    pre, der = res["premises"], res["derivations"]
    led, art = res["ledger"], res["artifacts"]
    failures = []
    for key in ("jump_law_violations", "quantization_violations",
                "renewal_identity_violations", "endpoints_not_nested_h_negative",
                "plateau_J_not_equal_to_Pi", "plateau_determinant_below_one",
                "plateau_Pi_two_forms_disagree", "strict_determinant_below_one",
                "strict_Delta_two_forms_disagree", "strict_J_formula_violations",
                "theorem_4_4_violations", "lemma_5_1_violations",
                "A_not_positive", "D_not_positive", "E_not_positive",
                "L_not_strictly_decreasing"):
        if sq[key]:
            failures.append("slope_quantization.%s = %d" % (key, sq[key]))
    for key in ("mediant_below_beta_with_J_not_positive",
                "reset_child_slope_not_between_beta_and_mediant",
                "reset_mediant_not_above_beta", "child_denominator_below_2g_plus_h",
                "farey_neighbour_identity_violations"):
        if ori[key]:
            failures.append("orientation.%s = %d" % (key, ori[key]))
    for key in ("theorem_4_3_violations", "theorem_5_4_violations",
                "theorem_6_1_violations", "u_beta_above_L_over_3",
                "distinct_slopes_closer_than_one_over_L_squared"):
        if pre[key]:
            failures.append("premises.%s = %d" % (key, pre[key]))
    # Enumerated, not matched by suffix. The first version read
    # `key.endswith(("violations", "_implied", "_x"))`, which silently skipped
    # `cor_6_2_not_implied_by_thm_6_1` -- a counter that could increment and
    # never be acted on. The drill's D19 is the only reason that surfaced.
    for key in DERIVATION_COUNTERS:
        if der[key]:
            failures.append("derivations.%s = %s" % (key, der[key]))
    unread = sorted(k for k, v in der.items()
                    if isinstance(v, int) and not isinstance(v, bool)
                    and k not in DERIVATION_COUNTERS and k != "grid_points")
    if unread:
        failures.append("derivations: %s is counted but nothing reads it" % unread)
    if not der["two_b_squared_over_a_below_8"]:
        failures.append("derivations: 2b^2/a is not below 8")
    if art["sha256_mismatches"]:
        failures.append("artifacts: %d sha256 mismatches"
                        % len(art["sha256_mismatches"]))
    if art["validation_record_shape"] == "UNRECOGNISED":
        failures.append("artifacts: the validation record shape is unrecognised")
    if res["their_claims"]["independently_contradicted"]:
        failures.append("their_claims: %s"
                        % res["their_claims"]["independently_contradicted"])
    if res["shipped_examples"]["examples_failing_a_clause"]:
        failures.append("shipped_examples: a unit-reset example fails a clause")
    # A last-bit drift on a published double is a FINDING about the artifact,
    # not a failure of this check -- RUN-032 drew that line and it holds here.
    # A decimal wrong beyond its own published precision is the failure.
    over = [k for k, v in res["constants"]["inline_decimals_in_the_paper"].items()
            if v.get("verdict") == "OVER-PUBLISHED"]
    if over:
        failures.append("constants: %s published past the computation" % over)

    guards = []
    if sq["edges"] < 100000:
        guards.append("too few renewal edges to discriminate: %d" % sq["edges"])
    if sq["genuine_resets_J_negative"] < 100:
        guards.append("too few genuine resets: %d" % sq["genuine_resets_J_negative"])
    if ori["unit_resets"] < 20:
        guards.append("too few unit resets: %d" % ori["unit_resets"])
    if pre["high_source_chains"] < 100:
        guards.append("the high-source hypothesis is barely attained: %d"
                      % pre["high_source_chains"])
    if der["grid_points"] < 100:
        guards.append("derivation grid too small: %d" % der["grid_points"])
    for key in ("survival_bound_undecided", "high_source_undecided",
                "high_source_slope_bound_undecided"):
        if pre[key]:
            guards.append("premises.%s = %d: the bracket could not decide"
                          % (key, pre[key]))
    if res["shipped_examples"]["distinct_examples"] < 1:
        guards.append("no unit-reset example recomputed")
    if art["verified"] < 5:
        guards.append("only %d artifact digests verified" % art["verified"])
    if res["constants"]["not_bracketed_here"]:
        guards.append("constants not bracketed: %s"
                      % res["constants"]["not_bracketed_here"])
    if res["constants"]["published_decimals_this_run_could_not_identify"]:
        guards.append("a decimal the paper publishes matches no reference here: %s"
                      % res["constants"]["published_decimals_this_run_could_not_identify"])
    if len(res["constants"]["inline_decimals_in_the_paper"]) < 3:
        guards.append("only %d inline decimals were located in the paper"
                      % len(res["constants"]["inline_decimals_in_the_paper"]))
    if res["ledger"]["paper_section_22_1_numbered_results"] < 5:
        guards.append("the paper's own ledger section was not parsed")
    # This bundle renamed `verified_claims` to `verified_statements`. A reader
    # that knows only the old key reads zero claims and reports zero
    # contradictions, which looks exactly like agreement.
    if res["their_claims"]["claims_the_checker_states"] < 5:
        guards.append("only %d checker claims were read; the report key may have "
                      "been renamed again"
                      % res["their_claims"]["claims_the_checker_states"])

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
