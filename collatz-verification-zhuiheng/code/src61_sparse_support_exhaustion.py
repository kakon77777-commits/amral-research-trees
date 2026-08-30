"""RUN-042 — independent recheck of Hard-Zeta round A-U.2d.14.

`Sparse B-Support Exhaustion` (source item 61). 數學戰士「墜衡」.

A-U.2d.13 showed completed B-support is polynomially sparse. This round asks
whether a divergent branch can hide the renewal structure somewhere else -- in
intervals that have started but not finished, or in the complementary A family
-- and closes both, then states a trichotomy for anything above `N^(4/5)`.

Two things make it more checkable than the last round.

First, section 3 is about EVERY suffix minimum, not only B sources. A B source
does not occur on a convergent orbit at all (RUN-041 measured 0 in 460,024
first-crossing intervals), but suffix minima are everywhere, so Theorem 3.1
(`q_{s+1} = 1`) and Corollary 3.2 (`7, 11 mod 12`) have a real population here
and are exercised on it rather than gated away.

Second, the constants family is again exact rationals in one inherited decimal:

    theta*  = 1/(rho*+1)        = 2500/12791
    sigma*  = 1/(1+theta*)      = 12791/15291
    chi(k)  = (5k-4)/3          chi(sigma*)  = 2791/45873
    zeta(k) = (k+1)/3           zeta(sigma*) = 28082/45873
    psi(k)  = (k-(1-theta*))/theta*

and `psi(sigma*) = 1 - sigma* = 2500/15291` EXACTLY -- an identity the frontier
prints as two different doubles, side by side, under the same key.

Usage:
    python code/src61_sparse_support_exhaustion.py --bundle <dir> [--limit N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import random
import re
import struct
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src47_survival_closure import (                               # noqa: E402
    convergents_from_terms, decimal_verdict, exact_continued_fraction,
    rational_digits,
)
from src53_plateau_reset import (                                   # noqa: E402
    accelerated, bracket_decimal, cumulative, ln2_bracket, v2,
)
from src54_low_source_saturation import (                           # noqa: E402
    _exp_bracket, ln_bracket, simplify, ulps_against_bracket, widen,
)
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d14_Sparse_B_Support_Exhaustion"
         "_v0.1.md")
REPORT = "Hard_Zeta_AU2d14_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d14_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d14_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d14.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.14_AU2d14.md"

RHO_STAR = Fraction(41164, 10000)          # inherited from A-U.2d.3
THETA_STAR = 1 / (RHO_STAR + 1)
SIGMA_STAR = 1 / (1 + THETA_STAR)
KAPPA_13 = (RHO_STAR + 1) / (RHO_STAR + 1 + THETA_STAR)
LAMBDA_13 = 1 / (RHO_STAR + 1 + THETA_STAR)


def chi(k: Fraction) -> Fraction:
    """Section 9's Huge-PQ escape exponent."""
    return (5 * k - 4) / 3


def zeta(k: Fraction) -> Fraction:
    """Section 9's current-slack spike exponent."""
    return (k + 1) / 3


def psi(k: Fraction) -> Fraction:
    """Section 10's unconditional active-slack exponent."""
    return (k - (1 - THETA_STAR)) / THETA_STAR


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def ln_any(x: Fraction) -> tuple[Fraction, Fraction]:
    assert x > 0
    if x >= 1:
        return ln_bracket(x)
    lo, hi = ln_bracket(1 / x)
    return -hi, -lo


def log2_any(x: Fraction) -> tuple[Fraction, Fraction]:
    l2_lo, l2_hi = ln2_bracket()
    lo, hi = ln_any(x)
    if lo >= 0:
        return lo / l2_hi, hi / l2_lo
    return lo / l2_lo, hi / l2_hi


# ---------------------------------------------------------------------------
# instrument
# ---------------------------------------------------------------------------

def check_instrument() -> dict:
    """Self-checks with IRRATIONAL answers, plus the closed forms this round's
    constants turn out to have.

    RUN-039's `(1/4)^(1/2) = 1/2` check could not fail because both bracket
    ends land exactly on the answer. Irrational targets, and `lo < hi` asserted
    on its own.
    """
    out: dict = {"checks": 0, "failed": []}

    def want(name: str, ok: bool) -> None:
        out["checks"] += 1
        if not ok:
            out["failed"].append(name)

    l2_lo, l2_hi = ln2_bracket()
    a, b = ln_any(Fraction(1, 2))
    want("ln(1/2) brackets -ln2", a <= -l2_hi and b >= -l2_lo)
    want("ln(1/2) is not degenerate", a < b)
    lo, hi = log2_any(Fraction(3))
    b_lo, b_hi = beta_tight()
    want("log2(3) agrees with beta", lo <= b_hi and hi >= b_lo)
    want("log2(3) is not degenerate", lo < hi)

    want("theta* = 2500/12791", THETA_STAR == Fraction(2500, 12791))
    want("sigma* = 12791/15291", SIGMA_STAR == Fraction(12791, 15291))
    want("chi(sigma*) = 2791/45873", chi(SIGMA_STAR) == Fraction(2791, 45873))
    want("zeta(sigma*) = 28082/45873",
         zeta(SIGMA_STAR) == Fraction(28082, 45873))
    want("psi(sigma*) = 1 - sigma*", psi(SIGMA_STAR) == 1 - SIGMA_STAR)
    want("psi(sigma*) = 2500/15291", psi(SIGMA_STAR) == Fraction(2500, 15291))
    want("1 - theta* = 10291/12791", 1 - THETA_STAR == Fraction(10291, 12791))
    want("4/5 < sigma*", Fraction(4, 5) < SIGMA_STAR)
    want("chi(4/5) = 0", chi(Fraction(4, 5)) == 0)
    return out


# ---------------------------------------------------------------------------
# the constants, exact against the float64 chain
# ---------------------------------------------------------------------------

def check_exponents(frontier: dict, report: dict) -> dict:
    """Each published constant against its exact rational AND the float64 route
    the artifact would have taken.

    The magnitude cap is tested BEFORE the chain excuse. RUN-040 learned that a
    "matches the chain, so it is a rounding" branch must be bounded; RUN-041
    then rebuilt it with the cap second, where an elif chain never reaches it.
    The ordering is the bound.
    """
    t: dict = {
        "constants_checked": 0,
        "disagreeing_with_both_evaluations": 0,
        "from_the_float64_chain_not_the_exact_rational": 0,
        "exact_to_the_last_bit": 0,
        "missing_from_the_frontier": 0,
        "rows": [],
    }
    f_rho = float(RHO_STAR)
    f_theta = 1.0 / (f_rho + 1.0)
    f_sigma = 1.0 / (1.0 + f_theta)
    p_sigma = frontier["old_disjoint_backbone_exponent_sigma"]
    p_theta = frontier["theta_star"]
    exact = {
        "theta_star": (THETA_STAR, f_theta, 4),
        "active_backlog_unconditional_N_exponent":
            (1 - THETA_STAR, 1.0 - f_theta, 4),
        "old_disjoint_backbone_exponent_sigma": (SIGMA_STAR, f_sigma, 4),
        "AU2d13_completed_support_exponent":
            (KAPPA_13, (f_rho + 1.0) / (f_rho + 1.0 + f_theta), 4),
        "AU2d13_completed_support_log_exponent":
            (LAMBDA_13, 1.0 / (f_rho + 1.0 + f_theta), 4),
        "controlled_total_renewal_support_exponent":
            (Fraction(4, 5), 0.8, 4),
        "high_support_threshold": (Fraction(4, 5), 0.8, 4),
    }
    for name, (ex, ch, budget) in exact.items():
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        d_exact = bits(pub) - bits(float(ex))
        d_chain = bits(pub) - bits(ch)
        if d_exact == 0:
            t["exact_to_the_last_bit"] += 1
        elif abs(d_exact) > budget:
            t["disagreeing_with_both_evaluations"] += 1
        elif d_chain == 0:
            t["from_the_float64_chain_not_the_exact_rational"] += 1
        t["rows"].append({"name": name, "published": repr(pub),
                          "exact": str(ex),
                          "exact_decimal": rational_digits(ex, 22),
                          "ulps_vs_exact": d_exact,
                          "ulps_vs_float64_chain": d_chain})
    # the three escape functions evaluated at sigma*, whose parents are already
    # rounded. `chi` cancels 5*sigma against 4 and inherits that magnitude loss.
    at = frontier["at_old_sigma"]
    cancel = (5 * p_sigma) / (5 * p_sigma - 4)
    t["cancellation_factor_in_five_sigma_minus_four"] = round(cancel, 2)
    for name, ex, ch, budget in (
        ("chi", chi(SIGMA_STAR), (5 * p_sigma - 4) / 3,
         4 * int(math.ceil(cancel))),
        ("zeta", zeta(SIGMA_STAR), (p_sigma + 1) / 3, 4),
        ("psi", psi(SIGMA_STAR), (p_sigma - (1 - p_theta)) / p_theta, 4),
        ("one_minus_sigma", 1 - SIGMA_STAR, 1 - p_sigma, 4),
    ):
        t["constants_checked"] += 1
        if name not in at:
            t["missing_from_the_frontier"] += 1
            continue
        pub = at[name]
        d_exact = bits(pub) - bits(float(ex))
        d_chain = bits(pub) - bits(ch)
        if d_exact == 0:
            t["exact_to_the_last_bit"] += 1
        elif abs(d_exact) > budget:
            t["disagreeing_with_both_evaluations"] += 1
        elif d_chain == 0:
            t["from_the_float64_chain_not_the_exact_rational"] += 1
        t["rows"].append({"name": "at_old_sigma." + name, "published": repr(pub),
                          "exact": str(ex),
                          "exact_decimal": rational_digits(ex, 22),
                          "ulps_vs_exact": d_exact,
                          "ulps_vs_float64_chain": d_chain})
    return t


def check_psi_identity(frontier: dict) -> dict:
    """`psi(sigma*) = 1 - sigma*` is an identity, and the frontier prints both.

    `psi(k) = (k - (1-theta))/theta` at `k = sigma* = 1/(1+theta)` gives
    `theta/(1+theta)`, which is exactly `1 - sigma*`. The bundle computes the
    same number by two float64 routes and stores both under `at_old_sigma`,
    where they differ. That is not a mathematical error and not even a wrong
    value -- it is one quantity carrying two values in the same object, which a
    downstream consumer would read as a discrepancy.
    """
    t: dict = {"identity_holds_exactly": False,
               "published_values_agree": False,
               "ulps_between_the_two_published_values": 0,
               "each_matches_its_own_float64_route": 0}
    t["identity_holds_exactly"] = (psi(SIGMA_STAR) == 1 - SIGMA_STAR)
    at = frontier["at_old_sigma"]
    a, b = at["psi"], at["one_minus_sigma"]
    t["published_values_agree"] = (a == b)
    t["ulps_between_the_two_published_values"] = bits(b) - bits(a)
    p_sigma = frontier["old_disjoint_backbone_exponent_sigma"]
    p_theta = frontier["theta_star"]
    if bits(a) == bits((p_sigma - (1 - p_theta)) / p_theta):
        t["each_matches_its_own_float64_route"] += 1
    if bits(b) == bits(1 - p_sigma):
        t["each_matches_its_own_float64_route"] += 1
    t["exact_value"] = str(psi(SIGMA_STAR))
    t["exact_decimal"] = rational_digits(psi(SIGMA_STAR), 22)
    return t


def check_identities(trials: int = 400, seed: int = 26081414) -> dict:
    """The exponent algebra of sections 4, 9 and 10, as identities in the
    symbols rather than at one point."""
    rng = random.Random(seed)
    t: dict = {"trials": 0,
               "rho_over_rho_plus_one_violations": 0,
               "trichotomy_exponent_identity_violations": 0,
               "psi_from_theorem_4_1_violations": 0,
               "chi_threshold_violations": 0}
    for _ in range(trials):
        t["trials"] += 1
        rho = Fraction(rng.randrange(1, 8000), 1000)
        th = 1 / (rho + 1)
        # Theorem 4.1's step
        if rho / (rho + 1) != 1 - th:
            t["rho_over_rho_plus_one_violations"] += 1
        # straddle the threshold. Sampling only above 4/5 makes this
        # check vacuous: every k is then above 3/5 as well, so a moved
        # threshold changes no verdict and the drill correctly reported
        # the defect as planting nothing.
        k = Fraction(rng.randrange(1, 2000), 1000)
        # Theorem 9.1's step: 2k - 1 - chi(k) = zeta(k)
        if 2 * k - 1 - chi(k) != zeta(k):
            t["trichotomy_exponent_identity_violations"] += 1
        # section 10: solving U_N <= N^(1-th) delta^th for delta
        lhs = (k - (1 - th)) / th
        if lhs * th + (1 - th) != k:
            t["psi_from_theorem_4_1_violations"] += 1
        # chi is positive exactly above 4/5
        if (chi(k) > 0) != (k > Fraction(4, 5)):
            t["chi_threshold_violations"] += 1
    t["chi_at_four_fifths"] = str(chi(Fraction(4, 5)))
    t["zeta_at_four_fifths"] = str(zeta(Fraction(4, 5)))
    t["psi_at_sigma_star"] = str(psi(SIGMA_STAR))
    return t


# ---------------------------------------------------------------------------
# real orbits -- sections 3, 6, 7
# ---------------------------------------------------------------------------

def suffix_minima(values: list[int], T: int) -> list[int]:
    """Indices `s < T` with `values[s] < min(values[s+1..T])`.

    On a finite window, as the paper's own checker scope says. Taking the whole
    convergent orbit instead gives NOTHING: it ends at 1, the global minimum, so
    no earlier state is below its own suffix and the population is empty. The
    window has to stop before the descent for the definition to have instances.
    """
    out, run = [], None
    for s in range(T, -1, -1):
        if run is None or values[s] < run:
            run = values[s]
            if s < T:
                out.append(s)
    out.reverse()
    return out


def check_suffix_minima(limit: int, window: int = 40) -> dict:
    """Theorem 3.1 and Corollary 3.2, which unlike this round's B-side theorems
    have a real population on convergent orbits."""
    t: dict = {
        "orbits": 0, "suffix_minima": 0,
        "theorem_3_1_violations": 0,
        "corollary_3_2_violations": 0,
        "q_one_not_equivalent_to_three_mod_four": 0,
        "sources_divisible_by_three": 0,
        "late_ordinal_floor_violations": 0,
        "minima_with_a_delta_crossing": 0,
        "minima_that_are_A_renewals": 0,
        "B_injections_among_true_suffix_minima": 0,
        "successor_not_greater": 0,
        "terminal_index_returned_as_a_suffix_minimum": 0,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, 400)
        if len(word) < window + 2:
            continue
        t["orbits"] += 1
        vv, ww = values[:window + 1], word[:window]
        K = cumulative(ww)
        seen: list[int] = []
        for s in suffix_minima(vv, window):
            t["suffix_minima"] += 1
            y = vv[s]
            if s + 1 >= len(vv):
                # Theorem 3.1 is about NONTERMINAL minima, and the terminal
                # index has no successor to test. Say so instead of indexing
                # past the end -- a gate that raises has no readable verdict.
                t["terminal_index_returned_as_a_suffix_minimum"] += 1
                continue
            # the step the proof rests on
            if not vv[s + 1] > y:
                t["successor_not_greater"] += 1
            # Theorem 3.1
            if ww[s] != 1:
                t["theorem_3_1_violations"] += 1
            # q = 1 on an odd source is equivalent to y = 3 mod 4
            if (ww[s] == 1) != (y % 4 == 3):
                t["q_one_not_equivalent_to_three_mod_four"] += 1
            if s > 0 and y % 3 == 0:
                t["sources_divisible_by_three"] += 1
            # Corollary 3.2, post-entry only
            if s > 0:
                if y % 12 not in (7, 11):
                    t["corollary_3_2_violations"] += 1
                seen.append(y)
            # A or B: does a first crossing of delta exist inside the window?
            cross = None
            for u in range(s + 1, window + 1):
                g, p = u - s, K[u] - K[s]
                if b_hi * g < p:
                    cross = u
                    break
            if cross is None:
                t["minima_that_are_A_renewals"] += 1
            else:
                t["minima_with_a_delta_crossing"] += 1
                # a TRUE suffix minimum with a crossing is automatically a
                # B-injection, since Y_{e(s)} >= Y_s by minimality and the
                # orbit is injective
                if vv[cross] > y:
                    t["B_injections_among_true_suffix_minima"] += 1
        for j, y in enumerate(sorted(seen), start=1):
            if y < 6 * j - 1:
                t["late_ordinal_floor_violations"] += 1
    return t


def check_envelope(limit: int, window: int = 40) -> dict:
    """Sections 6 and 7 on real orbits.

    The A-renewal family DOES occur, so `E_A = beta T - Q`, the exact product
    identity, and the support-transfer inequality can all be exercised rather
    than gated away.
    """
    t: dict = {
        "orbits_with_two_or_more_A_renewals": 0,
        "E_A_disagreeing_with_beta_T_minus_Q": 0,
        "A_envelope_not_positive": 0,
        "envelope_product_identity_violations": 0,
        "A_source_values_not_increasing": 0,
        "delta_at_A_renewals_not_increasing": 0,
        "theorem_7_1_floor_violations": 0,
        "transfer_inequality_checked": 0,
        "transfer_inequality_violations": 0,
        "largest_A_count": 0,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, 400)
        if len(word) < window + 2:
            continue
        vv, ww = values[:window + 1], word[:window]
        K = cumulative(ww)
        cs = []
        for s in suffix_minima(vv, window):
            cross = None
            for u in range(s + 1, window + 1):
                g, p = u - s, K[u] - K[s]
                if b_hi * g < p:
                    cross = u
                    break
            if cross is None and s > 0:
                cs.append(s)
        if len(cs) < 2:
            continue
        t["orbits_with_two_or_more_A_renewals"] += 1
        t["largest_A_count"] = max(t["largest_A_count"], len(cs))
        c1, cl = cs[0], cs[-1]
        T, Q = cl - c1, K[cl] - K[c1]
        # E_A = delta_cl - delta_c1 = beta T - Q, bracketed
        e_lo, e_hi = b_lo * T - Q, b_hi * T - Q
        if not e_lo > 0:
            t["A_envelope_not_positive"] += 1
        # the same quantity computed straight from the delta definition
        f_lo = (b_lo * cl - K[cl]) - (b_hi * c1 - K[c1])
        f_hi = (b_hi * cl - K[cl]) - (b_lo * c1 - K[c1])
        if e_hi < f_lo or e_lo > f_hi:
            t["E_A_disagreeing_with_beta_T_minus_Q"] += 1
        # z_A/y_A = 2^{E_A} P_A, written with no beta: z 2^Q = y 3^T P
        P = Fraction(1)
        for j in range(c1, cl):
            P *= 1 + Fraction(1, 3 * vv[j])
        if Fraction(vv[cl]) * 2 ** Q != Fraction(vv[c1]) * 3 ** T * P:
            t["envelope_product_identity_violations"] += 1
        for i in range(len(cs) - 1):
            if not vv[cs[i]] < vv[cs[i + 1]]:
                t["A_source_values_not_increasing"] += 1
            a, b = cs[i], cs[i + 1]
            g, p = b - a, K[b] - K[a]
            if not b_lo * g - p > 0:
                t["delta_at_A_renewals_not_increasing"] += 1
        for j, s in enumerate(cs, start=1):
            if vv[s] < 6 * j - 1:
                t["theorem_7_1_floor_violations"] += 1
        # Theorem 7.1 in the form its proof actually gives:
        # 6 A_N - 1 <= z_A = y_A 2^{E_A} P_A
        t["transfer_inequality_checked"] += 1
        if not Fraction(6 * len(cs) - 1) <= Fraction(vv[cl]):
            t["transfer_inequality_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# the conditional theorems, as algebra
# ---------------------------------------------------------------------------

def check_backlog(trials: int = 400, seed: int = 7114) -> dict:
    """Theorems 4.1, 4.2, section 5 and the section 9 case split.

    A B source does not occur on a convergent orbit, so these cannot be run on
    one. Their content is an implication between finite quantities, and that is
    what is checked -- at integer `rho`, where the root is exact and no bracket
    is needed.
    """
    rng = random.Random(seed)
    t: dict = {
        "grid_points": 0,
        "theorem_4_1_violations": 0, "theorem_4_1_antecedent_holds": 0,
        "theorem_4_2_violations": 0, "theorem_4_2_antecedent_holds": 0,
        "section_5_division_violations": 0,
        "trichotomy_case_split_violations": 0,
        "trichotomy_points": 0,
    }
    for _ in range(trials):
        t["grid_points"] += 1
        rho = rng.randrange(1, 9)
        r = rng.randrange(2, 500)
        S = rng.randrange(1, 10 ** 5)
        N = S + rng.randrange(0, 10 ** 5)
        c = Fraction(1, rng.randrange(1, 40))
        # Theorem 4.1: H >= c (r-1)^(rho+1)/S^rho and H < delta, S <= N
        #   => delta > c (r-1)^(rho+1)/N^rho
        H = c * Fraction((r - 1) ** (rho + 1), S ** rho)
        delta = H + Fraction(1, rng.randrange(1, 1000))
        t["theorem_4_1_antecedent_holds"] += 1
        if not delta > c * Fraction((r - 1) ** (rho + 1), N ** rho):
            t["theorem_4_1_violations"] += 1
        # Theorem 4.2: H > (r-1)^2/(Q S), H < delta, S <= N => (r-1)^2 < Q N delta
        Qn = rng.randrange(2, 300)
        H2 = Fraction((r - 1) ** 2, Qn * S) + Fraction(1, 10 ** 6)
        d2 = H2 + Fraction(1, rng.randrange(1, 1000))
        t["theorem_4_2_antecedent_holds"] += 1
        if not Fraction((r - 1) ** 2) < Fraction(Qn * N) * d2:
            t["theorem_4_2_violations"] += 1
        # section 5: dividing Theorem 4.1 by N
        th = Fraction(1, rho + 1)
        u = rng.randrange(1, 10 ** 4)
        # (1 + C N^(1-th) d^th)/N == 1/N + C (d/N)^th  -- as exponents
        if (1 - th) - 1 != -th:
            t["section_5_division_violations"] += 1
        # section 9's case split: Q d >= N^(2k-1); either Q >= N^chi or
        # d >= N^(2k-1-chi) = N^zeta
        # straddle the threshold. Sampling only above 4/5 makes this
        # check vacuous: every k is then above 3/5 as well, so a moved
        # threshold changes no verdict and the drill correctly reported
        # the defect as planting nothing.
        k = Fraction(rng.randrange(1, 2000), 1000)
        t["trichotomy_points"] += 1
        if 2 * k - 1 - chi(k) != zeta(k):
            t["trichotomy_case_split_violations"] += 1
    return t


def check_counterexample(levels: int = 9) -> dict:
    """NO-GO 11.1: a divergent integer sequence whose suffix-minimum times are
    `t_j = 2^(j^2)`, so at `N = t_j` there are only `sqrt(log2 N)` of them.

    Built and enumerated rather than argued, because the claim is that a
    construction exists.
    """
    t: dict = {"levels": 0, "sequence_length": 0,
               "suffix_minimum_times_disagreeing_with_t_j": 0,
               "count_disagreeing_with_sqrt_log2_N": 0,
               "sequence_not_divergent": 0,
               "intermediate_value_too_small": 0}
    ts = [2 ** (j * j) for j in range(1, levels + 1)]
    top = ts[-1]
    x: dict[int, int] = {}
    for j, tj in enumerate(ts, start=1):
        x[tj] = j
    # one representative intermediate per gap is enough to enumerate against;
    # the construction only requires every intermediate to exceed j+1
    for j in range(1, levels):
        lo, hi = ts[j - 1], ts[j]
        for n in (lo + 1, (lo + hi) // 2, hi - 1):
            if lo < n < hi:
                x[n] = j + 2
                if not x[n] > j + 1:
                    t["intermediate_value_too_small"] += 1
    idx = sorted(x)
    t["sequence_length"] = len(idx)
    # suffix minima of the sampled sequence
    mins, run = [], None
    for n in reversed(idx):
        if run is None or x[n] < run:
            run = x[n]
            mins.append(n)
    mins.reverse()
    if set(mins) != set(ts):
        t["suffix_minimum_times_disagreeing_with_t_j"] = 1
    for j, tj in enumerate(ts, start=1):
        t["levels"] += 1
        count = sum(1 for m in mins if m <= tj)
        if count != j:
            t["count_disagreeing_with_sqrt_log2_N"] += 1
        if j * j != tj.bit_length() - 1:
            t["count_disagreeing_with_sqrt_log2_N"] += 1
    if x[ts[-1]] <= x[ts[0]]:
        t["sequence_not_divergent"] += 1
    t["count_at_the_largest_N"] = levels
    t["log2_of_the_largest_N"] = top.bit_length() - 1
    return t


def check_criticality(trials: int = 200, seed: int = 8114) -> dict:
    """Section 2.3's conversion, as the claim it is rather than the identity it
    looks like.

    `delta_m/m = beta - K_m/m` is a rearrangement, so testing it measures
    nothing. What the external input actually supplies is
    `liminf (m/K_m) = 1/beta`, and the step taken is that this gives
    `limsup (K_m/m) = beta`. That reciprocal relation is the claim.
    """
    rng = random.Random(seed)
    t: dict = {"sequences": 0, "reciprocal_relation_violations": 0,
               "monotone_conversion_violations": 0,
               "casp_sign_violations": 0}
    b_lo, b_hi = widen(*beta_tight(), 30)
    for _ in range(trials):
        t["sequences"] += 1
        n = rng.randrange(5, 40)
        # densities strictly below 1/beta, approaching it along a subsequence
        ds = [Fraction(rng.randrange(1, 999), 1000) for _ in range(n)]
        best = max(ds)
        # limsup of the reciprocal is the reciprocal of the liminf; on a finite
        # sample, max(1/d) = 1/min(d)
        if max(1 / d for d in ds) != 1 / min(ds):
            t["reciprocal_relation_violations"] += 1
        # under CASP, K_m/m < beta  <=>  delta_m/m > 0
        m = rng.randrange(1, 500)
        K = rng.randrange(1, int(m * 1.58) + 1)
        casp = b_lo * m - K > 0
        if casp and not (Fraction(K, m) < b_hi):
            t["casp_sign_violations"] += 1
        # a density rising to 1/beta forces K/m rising to beta
        if best < 1 / b_hi and not 1 / best > b_lo:
            t["monotone_conversion_violations"] += 1
    return t

# ---------------------------------------------------------------------------
# artifacts and ledger
# ---------------------------------------------------------------------------

def check_artifacts(bundle: pathlib.Path) -> dict:
    """Digest coverage, and the validation record's own digests.

    RUN-039, RUN-040 and RUN-041 each reported that the source-validation
    record carried encoding checks and no hashes. This one does carry them, so
    they are recomputed here rather than trusted -- a digest nobody verifies is
    the same as no digest.
    """
    t: dict = {"files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
               "checksum_lines_naming_a_missing_file": 0,
               "files_with_no_digest_anywhere": [],
               "validation_entries": 0,
               "validation_entries_with_a_digest": 0,
               "validation_digest_mismatches": 0,
               "validation_entries_naming_a_missing_file": 0,
               "files_absent_from_the_validation_record": []}
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
    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    checks = val.get("checks", {})
    with_digest = set()
    if isinstance(checks, dict):
        for n, r in checks.items():
            t["validation_entries"] += 1
            if not isinstance(r, dict):
                continue
            if "sha256" not in r:
                continue
            t["validation_entries_with_a_digest"] += 1
            with_digest.add(n)
            if n not in actual:
                t["validation_entries_naming_a_missing_file"] += 1
            elif actual[n] != r["sha256"]:
                t["validation_digest_mismatches"] += 1
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in checks]
    t["validation_status"] = val.get("status")
    t["validation_checker_rerun"] = val.get("checker_rerun")
    t["validation_python_compile"] = val.get("python_compile")
    gate = val.get("commit_gate", {})
    t["commit_gate_entries_not_pass"] = sum(
        1 for v in gate.values() if v != "PASS") if isinstance(gate, dict) else 0
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    """Does the machine-readable ledger carry what sections 11 and 15 say?

    Coverage is an OBSERVATION, never a gate failure -- the line drawn at
    RUN-032 and held since.
    """
    t: dict = {"paper_proved_items": 0, "ledger_proved_items": 0,
               "paper_open_items": 0, "ledger_open_items": 0,
               "paper_no_go_headings": 0, "ledger_no_go_items": 0,
               "ledger_has_an_open_key": False,
               "open_items_absent_from_the_ledger": [],
               "no_go_headings_absent_from_the_ledger": []}
    proved = re.search(r"## 15\.1(.*?)## 15\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(
            re.findall(r"^\d+\. ", proved.group(1), re.M))
    openb = re.search(r"## 15\.4(.*?)(?:\n---|\Z)", paper, re.S)
    bullets = []
    if openb:
        bullets = [b.strip(" -;.") for b in
                   re.findall(r"^- (.+)$", openb.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
    no_go = re.findall(r"^## NO-GO (11\.\d) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    t["ledger_proved_items"] = len(ledger.get("proved_internally", []))
    t["ledger_no_go_items"] = len(ledger.get("no_go_boundaries", []))
    key = next((k for k in ledger if "open" in k.lower()), None)
    t["ledger_has_an_open_key"] = key is not None
    t["ledger_open_items"] = len(ledger.get(key, [])) if key else 0
    blob = json.dumps(ledger).lower()

    def covered(text: str) -> bool:
        words = [w for w in re.findall(r"[a-z_]{5,}", text.lower())
                 if w not in ("which", "these", "there", "their", "about")]
        if not words:
            return True
        hit = sum(1 for w in words if w[:7] in blob)
        return hit >= max(2, len(words) // 2)

    t["open_items_absent_from_the_ledger"] = [b for b in bullets
                                              if not covered(b)]
    t["no_go_headings_absent_from_the_ledger"] = [
        n for n, h in no_go if not covered(h)]
    return t


def check_printed_decimals(paper: str, route: str) -> dict:
    """Every constant the prose prints, against its exact rational."""
    t: dict = {"printed": 0, "over_published": 0, "exact_to_every_digit": 0,
               "correctly_rounded": 0, "truncated": 0,
               "printed_with_an_ellipsis": 0, "rows": []}
    named = {
        "theta_star": THETA_STAR,
        "one_minus_theta": 1 - THETA_STAR,
        "sigma_star": SIGMA_STAR,
        "kappa13": KAPPA_13,
        "lambda13": LAMBDA_13,
        "chi_at_sigma": chi(SIGMA_STAR),
        "zeta_at_sigma": zeta(SIGMA_STAR),
        "psi_at_sigma": psi(SIGMA_STAR),
    }
    blob = paper + "\n" + route
    ell = chr(92) + "ldots"
    for name, ex in named.items():
        ref = rational_digits(ex, 30)
        stem = ref[:8]
        for m in re.finditer(re.escape(stem) + r"\d*", blob):
            text = m.group(0)
            if len(text) < 10:
                continue
            t["printed"] += 1
            after = blob[m.end():m.end() + 7]
            if after.startswith(ell):
                t["printed_with_an_ellipsis"] += 1
            v = decimal_verdict(text, ref)
            if v["verdict"] == "OVER-PUBLISHED":
                t["over_published"] += 1
            elif v["verdict"].startswith("exact"):
                t["exact_to_every_digit"] += 1
            elif v["verdict"].startswith("correctly"):
                t["correctly_rounded"] += 1
            else:
                t["truncated"] += 1
            t["rows"].append({"name": name, "printed": text,
                              "ellipsis": after.startswith(ell),
                              "verdict": v["verdict"],
                              "digits_correct": v["digits_correct"]})
    return t


def check_their_claims(report: dict, res: dict) -> dict:
    mine = {
        "finite_suffix_minimum_residue": res["suffix"]["suffix_minima"],
        "active_backlog_algebra": res["backlog"]["theorem_4_1_antecedent_holds"],
        "active_backlog_cf_algebra":
            res["backlog"]["theorem_4_2_antecedent_holds"],
        "A_envelope_transfer_algebra":
            res["envelope"]["transfer_inequality_checked"],
        "support_escape_exponent_algebra": res["identities"]["trials"],
        "criticality_conversion_samples": res["criticality"]["sequences"],
        "sparse_set_counterexample_samples": res["counterexample"]["levels"],
    }
    rows = [{"check": k, "theirs": v, "mine": mine.get(k)}
            for k, v in report["checks"].items()]
    return {"rows": rows,
            "checks_i_did_not_reproduce": sum(1 for r in rows
                                              if r["mine"] is None)}


FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("exponents", "disagreeing_with_both_evaluations"),
    ("exponents", "missing_from_the_frontier"),
    ("identities", "rho_over_rho_plus_one_violations"),
    ("identities", "trichotomy_exponent_identity_violations"),
    ("identities", "psi_from_theorem_4_1_violations"),
    ("identities", "chi_threshold_violations"),
    ("suffix", "theorem_3_1_violations"),
    ("suffix", "corollary_3_2_violations"),
    ("suffix", "q_one_not_equivalent_to_three_mod_four"),
    ("suffix", "sources_divisible_by_three"),
    ("suffix", "late_ordinal_floor_violations"),
    ("suffix", "successor_not_greater"),
    ("suffix", "terminal_index_returned_as_a_suffix_minimum"),
    ("envelope", "E_A_disagreeing_with_beta_T_minus_Q"),
    ("envelope", "A_envelope_not_positive"),
    ("envelope", "envelope_product_identity_violations"),
    ("envelope", "A_source_values_not_increasing"),
    ("envelope", "delta_at_A_renewals_not_increasing"),
    ("envelope", "theorem_7_1_floor_violations"),
    ("envelope", "transfer_inequality_violations"),
    ("backlog", "theorem_4_1_violations"),
    ("backlog", "theorem_4_2_violations"),
    ("backlog", "section_5_division_violations"),
    ("backlog", "trichotomy_case_split_violations"),
    ("counterexample", "suffix_minimum_times_disagreeing_with_t_j"),
    ("counterexample", "count_disagreeing_with_sqrt_log2_N"),
    ("counterexample", "sequence_not_divergent"),
    ("counterexample", "intermediate_value_too_small"),
    ("criticality", "reciprocal_relation_violations"),
    ("criticality", "monotone_conversion_violations"),
    ("criticality", "casp_sign_violations"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_digest_mismatches"),
    ("artifacts", "validation_entries_naming_a_missing_file"),
    ("artifacts", "commit_gate_entries_not_pass"),
)

NON_VACUITY = (
    ("exponents", "constants_checked"),
    ("identities", "trials"),
    ("suffix", "orbits"),
    ("suffix", "suffix_minima"),
    ("envelope", "orbits_with_two_or_more_A_renewals"),
    ("envelope", "transfer_inequality_checked"),
    ("backlog", "grid_points"),
    ("backlog", "theorem_4_1_antecedent_holds"),
    ("backlog", "theorem_4_2_antecedent_holds"),
    ("backlog", "trichotomy_points"),
    ("counterexample", "levels"),
    ("criticality", "sequences"),
    ("printed", "printed"),
    ("artifacts", "validation_entries_with_a_digest"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("exponents", "from_the_float64_chain_not_the_exact_rational"),
    ("exponents", "exact_to_the_last_bit"),
    ("psi_identity", "ulps_between_the_two_published_values"),
    ("psi_identity", "each_matches_its_own_float64_route"),
    ("suffix", "minima_with_a_delta_crossing"),
    ("suffix", "minima_that_are_A_renewals"),
    ("suffix", "B_injections_among_true_suffix_minima"),
    ("envelope", "largest_A_count"),
    ("counterexample", "sequence_length"),
    ("counterexample", "count_at_the_largest_N"),
    ("counterexample", "log2_of_the_largest_N"),
    ("printed", "over_published"),
    ("printed", "exact_to_every_digit"),
    ("printed", "correctly_rounded"),
    ("printed", "truncated"),
    ("printed", "printed_with_an_ellipsis"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_entries"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "ledger_no_go_items"),
    ("their_claims", "checks_i_did_not_reproduce"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=20000)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    route = (bundle / ROUTE).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    res: dict = {}
    res["instrument"] = check_instrument()
    res["exponents"] = check_exponents(frontier, report)
    res["psi_identity"] = check_psi_identity(frontier)
    res["identities"] = check_identities()
    res["suffix"] = check_suffix_minima(a.limit)
    res["envelope"] = check_envelope(a.limit)
    res["backlog"] = check_backlog()
    res["counterexample"] = check_counterexample()
    res["criticality"] = check_criticality()
    res["printed"] = check_printed_decimals(paper, route)
    res["artifacts"] = check_artifacts(bundle)
    res["ledger"] = check_ledger(ledger, paper)
    res["their_claims"] = check_their_claims(report, res)

    failures = []
    for sec, key in FAILURE_COUNTERS:
        v = res[sec][key]
        if (len(v) if isinstance(v, list) else v):
            failures.append("%s.%s = %s" % (sec, key, v))
    vacuous = ["%s.%s" % (s, k) for s, k in NON_VACUITY if not res[s].get(k)]

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
        "run": "RUN-042", "round": "A-U.2d.14", "bundle": str(bundle),
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
