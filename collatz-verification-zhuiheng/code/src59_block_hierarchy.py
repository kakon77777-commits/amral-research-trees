"""RUN-040 — independent recheck of Hard-Zeta round A-U.2d.12.

`3-Adic Transport Hierarchy Closure` (source item 59). 數學戰士「墜衡」.

A-U.2d.11 shipped an exact rational dual certificate and asked whether its
finite-state exponents tend to zero. This round answers a *different*, stronger
question -- and says so plainly. It does not settle the A-U.2d.11 LP; it builds
a second hierarchy, indexed by block length `m` rather than by modulus `3^h`,
from a fact the LP relaxation throws away: one trajectory must realise every
overlapping exponent block at once.

Almost all of it is decidable with integer arithmetic alone:

    q_m       = floor(beta m)                      (compare 2^k with 3^m)
    C_m^-     = sum_{Q=m}^{q_m} binom(Q-1,m-1)/(3 2^Q)
    gamma_m   = 2^(q_m+1)/3^m - 1
    alpha^_m  = (1/3)(1 + 1/gamma_m) C_m^-

No logarithm is needed for any of that -- `floor(m log2 3)` is
`(3**m).bit_length() - 1`, and the rest is rational. The Chernoff half of the
closure does need `I_beta`, and the constants `K_m`, `B_m` need logarithms, so
those go through the certified brackets of `src53`/`src54`/`src55`.

Section 15's source floor is checked against the closed form this sweep derived
at RUN-039, `mu = (theta* - alpha)/(1 - alpha)`, which section 15 turns out to
*derive*: it is exactly `(theta* - eps)/(1 - eps)`. That makes RUN-039's fitted
formula a quoted step here, so the four inherited exponents are checked too.

Premises are measured before they are used, as at RUN-037/038/039. Two of them
matter: section 4's arithmetic needs every state *including the endpoint* to be
at least `y` (section 1 states it only for states *before* the endpoint), and
sections 7-8 additionally need `L >= y`, which is a strong demand on a real
orbit and is counted rather than assumed.

Usage:
    python code/src59_block_hierarchy.py --bundle <dir> [--limit N] [--out F]
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
from math import comb

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src47_survival_closure import (                               # noqa: E402
    decimal_verdict, rational_digits,
)
from src53_plateau_reset import (                                   # noqa: E402
    accelerated, bracket_decimal, ln2_bracket, v2,
)
from src54_low_source_saturation import (                           # noqa: E402
    _exp_bracket, ln_bracket, simplify, ulps_against_bracket, widen,
)
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d12_3Adic_Transport_Hierarchy_Closure"
         "_v0.1.md")
REPORT = "Hard_Zeta_AU2d12_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d12_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d12_theorem_ledger.json"
BLOCKS = "Hard_Zeta_AU2d12_block_hierarchy_data.json"
VALIDATION = "SOURCE_VALIDATION_AU2d12.json"
CHECKSUMS = "CHECKSUMS.sha256"
BUILDER = "build_AU2d12_artifacts.py"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.12_AU2d12.md"

ALPHA_27 = Fraction(1373, 25856)          # the A-U.2d.11 committed exponent
RHO_STAR = Fraction(41164, 10000)         # 4.1164, inherited


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


# ---------------------------------------------------------------------------
# brackets
# ---------------------------------------------------------------------------

def ln_any(x: Fraction) -> tuple[Fraction, Fraction]:
    """`ln x` for any positive rational. `ln_bracket` asserts `x >= 1`; below 1
    the series argument is negative and its tail bound no longer straddles, so
    take the reciprocal and flip the bracket instead of trusting the series
    outside its stated domain."""
    assert x > 0
    if x >= 1:
        return ln_bracket(x)
    lo, hi = ln_bracket(1 / x)
    return -hi, -lo


def exp_bracket_signed(lo: Fraction, hi: Fraction, digits: int = 18,
                       terms: int = 50) -> tuple[Fraction, Fraction]:
    """`e^t` for `t` in a bracket that may be negative.

    The argument is widened onto a short denominator FIRST. `_exp_bracket`
    multiplies its argument in 120 times, so a 60-digit input leaves the
    intermediate rationals seven thousand digits long, and this routine is
    called once per level. That is what put RUN-039 past eight minutes in a
    different guise; the fix is the same one -- keep the operands small, since
    a bracket that is wider than necessary is still a bracket, while a slow one
    stops being usable.
    """
    lo, hi = widen(lo, hi, digits)

    def one(t: Fraction, upper: bool) -> Fraction:
        if t >= 0:
            return _exp_bracket(t, terms)[1 if upper else 0]
        a, b = _exp_bracket(-t, terms)
        return 1 / (a if upper else b)
    return one(lo, False), one(hi, True)


def i_beta_bracket() -> tuple[Fraction, Fraction]:
    """`I_beta = beta ln2 - beta ln beta + (beta-1) ln(beta-1)`, beta = log2 3.

    Signs matter for the bracket ends: `ln beta > 0` because `beta > 1`, while
    `ln(beta-1) < 0` because `beta - 1 < 1`, so the third term is negative and
    its ends swap.
    """
    b_lo, b_hi = beta_tight()
    b_lo, b_hi = widen(b_lo, b_hi, 40)
    l2_lo, l2_hi = ln2_bracket()
    lb_lo, lb_hi = ln_any(b_lo)[0], ln_any(b_hi)[1]
    lm_lo, lm_hi = ln_any(b_lo - 1)[0], ln_any(b_hi - 1)[1]
    assert lb_lo > 0 and lm_hi < 0, "sign assumption behind the bracket ends"
    lo = b_lo * l2_lo - b_hi * lb_hi + (b_hi - 1) * lm_lo
    hi = b_hi * l2_hi - b_lo * lb_lo + (b_lo - 1) * lm_hi
    return widen(lo, hi, 40)


# ---------------------------------------------------------------------------
# the block hierarchy -- exact, integer arithmetic only
# ---------------------------------------------------------------------------

def q_floor(m: int) -> int:
    """`floor(beta m) = floor(log2 3^m)`, exactly, with no logarithm at all."""
    k = (3 ** m).bit_length() - 1
    assert 2 ** k <= 3 ** m < 2 ** (k + 1), "bit_length is not the floor"
    return k


def c_minus(m: int, q: int | None = None) -> Fraction:
    """`sum_{Q=m}^{q_m} binom(Q-1,m-1)/(3 2^Q)` -- section 7."""
    if q is None:
        q = q_floor(m)
    return sum((Fraction(comb(Q - 1, m - 1), 3 * 2 ** Q)
                for Q in range(m, q + 1)), Fraction(0))


def gamma_m(m: int, q: int | None = None) -> Fraction:
    """`2^(q_m+1)/3^m - 1` -- section 5."""
    if q is None:
        q = q_floor(m)
    return Fraction(2 ** (q + 1), 3 ** m) - 1


def alpha_hat(m: int) -> Fraction:
    """`(1/3)(1 + 1/gamma_m) C_m^-` -- section 8."""
    q = q_floor(m)
    return (1 + 1 / gamma_m(m, q)) * c_minus(m, q) / 3


def n_minus(m: int, q: int | None = None) -> int:
    if q is None:
        q = q_floor(m)
    return sum(comb(Q - 1, m - 1) for Q in range(m, q + 1))


def k_m_bracket(m: int) -> tuple[Fraction, Fraction]:
    """`K_m = 2 N_m^-/7 + sum N_{m,Q}/(3 2^Q) log(1 + 3 2^(Q+1))` -- section 7."""
    q = q_floor(m)
    lo = hi = Fraction(2 * n_minus(m, q), 7)
    for Q in range(m, q + 1):
        w = Fraction(comb(Q - 1, m - 1), 3 * 2 ** Q)
        a, b = ln_any(Fraction(1 + 3 * 2 ** (Q + 1)))
        lo, hi = lo + w * a, hi + w * b
    return widen(lo, hi, 30)


def b_m_bracket(m: int) -> tuple[Fraction, Fraction]:
    """`B_m = (1+1/gamma_m) K_m + E*_m/gamma_m + (m-1)/7` -- section 8."""
    g = gamma_m(m)
    k_lo, k_hi = k_m_bracket(m)
    e_lo, e_hi = _exp_bracket(Fraction(m, 21))
    s_lo = Fraction(m, 7) + Fraction(3 * m, 98) * e_lo
    s_hi = Fraction(m, 7) + Fraction(3 * m, 98) * e_hi
    f = 1 + 1 / g
    return widen(f * k_lo + s_lo / g + Fraction(m - 1, 7),
                 f * k_hi + s_hi / g + Fraction(m - 1, 7), 20)


def mu_dense(alpha: Fraction, theta: Fraction) -> Fraction:
    """Section 15's source floor exponent, `(theta* - eps)/(1 - eps)` at
    `eps = alpha`. RUN-039 fitted this shape to four published numbers; this
    round derives it, so here it is a quoted step rather than a guess."""
    return (theta - alpha) / (1 - alpha)


# ---------------------------------------------------------------------------
# instrument
# ---------------------------------------------------------------------------

def check_instrument() -> dict:
    """Every self-check here asks for an IRRATIONAL answer.

    RUN-039 wrote one that asked whether `(1/4)^(1/2)` brackets `1/2`. It does,
    and it could not do otherwise: `1/2` is exactly representable on the fixed
    denominator every bracket is widened onto, so both ends landed on it and a
    planted end-swap changed nothing. A bracket has two failure modes -- the
    value outside, and the ends reversed -- and only the second needs the ends
    to differ. So: irrational test values, and `lo < hi` asserted separately.
    """
    out: dict = {"checks": 0, "failed": []}

    def want(name: str, ok: bool) -> None:
        out["checks"] += 1
        if not ok:
            out["failed"].append(name)

    l2_lo, l2_hi = ln2_bracket()
    a, b = ln_any(Fraction(1, 2))
    want("ln(1/2) brackets -ln2", a <= -l2_hi + Fraction(1, 10**60)
         and b >= -l2_lo - Fraction(1, 10**60))
    want("ln(1/2) bracket is not degenerate", a < b)

    e_lo, e_hi = exp_bracket_signed(Fraction(-1), Fraction(-1))
    d_lo, d_hi = _exp_bracket(Fraction(1))
    # both brackets hold the same irrational, so they must overlap. A literal
    # decimal here would only be as good as the digits I typed, and nine of
    # them were already too few for a forty-digit bracket.
    want("e^-1 overlaps 1/e", e_lo <= 1 / d_lo and e_hi >= 1 / d_hi)
    want("e^-1 bracket is not degenerate", e_lo < e_hi)

    i_lo, i_hi = i_beta_bracket()
    want("I_beta bracket is not degenerate", i_lo < i_hi)
    want("I_beta is positive", i_lo > 0)

    # the m=1 row of their own diagnostics, reproduced from the definitions
    want("q_1 = 1", q_floor(1) == 1)
    want("C_1^- = 1/6", c_minus(1) == Fraction(1, 6))
    want("gamma_1 = 1/3", gamma_m(1) == Fraction(1, 3))
    want("alpha^_1 = 2/9", alpha_hat(1) == Fraction(2, 9))

    # floor(beta m) must never be reachable by 2^k = 3^m
    want("no power of two equals a power of three",
         all(2 ** q_floor(m) < 3 ** m for m in range(1, 60)))
    return out


# ---------------------------------------------------------------------------
# sections 5, 7, 8, 9 -- the exact hierarchy
# ---------------------------------------------------------------------------

def check_hierarchy(blocks: dict, frontier: dict, report: dict,
                    theta: Fraction) -> dict:
    t: dict = {
        "levels": 0,
        "q_floor_disagreeing_with_floor_beta_m": 0,
        "C_minus_disagreeing_with_the_binomial_sum": 0,
        "gamma_disagreeing_with_its_definition": 0,
        "alpha_hat_disagreeing_with_corollary_8_2": 0,
        "alpha_hat_float_not_the_nearest_double": 0,
        "mu_dense_disagreeing_with_the_section_15_formula": 0,
        "mu_matching_the_float64_chain_not_the_exact_rational": 0,
        "B_star_outside_its_bracket": 0,
        "B_star_within_float64_accumulation_of_the_bracket": 0,
        "frontier_disagreeing_with_the_block_data": 0,
        "report_disagreeing_with_the_block_data": 0,
        "rows": [],
    }
    fr = {int(r["m"]): r for r in frontier["selected_block_levels"]}
    rp = {int(k): v for k, v in report["exact_selected_block_exponents"].items()}
    for row in blocks["selected_exact_levels"]:
        m = int(row["m"])
        t["levels"] += 1
        q = q_floor(m)
        cm, gm, ah = c_minus(m, q), gamma_m(m, q), alpha_hat(m)
        if q != int(row["q_floor"]):
            t["q_floor_disagreeing_with_floor_beta_m"] += 1
        if cm != Fraction(row["C_minus"]):
            t["C_minus_disagreeing_with_the_binomial_sum"] += 1
        if gm != Fraction(row["gamma"]):
            t["gamma_disagreeing_with_its_definition"] += 1
        if ah != Fraction(row["alpha_hat_exact"]):
            t["alpha_hat_disagreeing_with_corollary_8_2"] += 1
        # an exact rational converts to its own nearest double, so this is a
        # direct bit comparison and needs no bracket
        d_ulps = bits(row["alpha_hat_float"]) - bits(float(ah))
        if d_ulps:
            t["alpha_hat_float_not_the_nearest_double"] += 1
        mu = mu_dense(ah, theta)
        pub_mu = row["dense_source_floor_mu"]
        mu_ulps = bits(pub_mu) - bits(float(mu))
        # the same formula run the way the artifact ran it: float64 throughout,
        # from a theta* that was itself evaluated in float64 off a rounded rho*
        th_f = 1.0 / (float(RHO_STAR) + 1.0)
        mu_chain = (th_f - float(ah)) / (1 - float(ah))
        chain_ulps = bits(pub_mu) - bits(mu_chain)
        # the chain reading excuses a ROUNDING, so it must be bounded like one.
        # Unbounded, it swallowed a theta* built from the wrong exponent
        # entirely -- the drill planted exactly that and this counter stayed
        # silent while a sibling caught it.
        if mu_ulps and (chain_ulps or abs(mu_ulps) > 2):
            t["mu_dense_disagreeing_with_the_section_15_formula"] += 1
        elif mu_ulps:
            t["mu_matching_the_float64_chain_not_the_exact_rational"] += 1
        b_lo, b_hi = b_m_bracket(m)
        pub_b = row["explicit_log_prefactor_Bstar"]
        # `B_m` is a sum of `q_m - m + 1` terms reaching 3e20, evaluated in
        # float64. Its last bit is therefore accumulated rounding, not a
        # published digit, and an ulp test on it measures their summation
        # order. Compare where the value actually lives: relative size.
        rel = 0.0 if b_lo <= Fraction(pub_b) <= b_hi else float(
            min(abs(Fraction(pub_b) - b_lo), abs(Fraction(pub_b) - b_hi))
            / b_hi)
        if rel > 1e-13:
            t["B_star_outside_its_bracket"] += 1
        elif rel > 0:
            t["B_star_within_float64_accumulation_of_the_bracket"] += 1
        f, r = fr.get(m, {}), rp.get(m, {})
        if (f.get("alpha_hat_exact") != row["alpha_hat_exact"]
                or f.get("C_minus") != row["C_minus"]
                or f.get("gamma") != row["gamma"]):
            t["frontier_disagreeing_with_the_block_data"] += 1
        if (r.get("alpha_exact") != row["alpha_hat_exact"]
                or r.get("C_minus") != row["C_minus"]
                or r.get("gamma") != row["gamma"]
                or r.get("q_floor") != row["q_floor"]):
            t["report_disagreeing_with_the_block_data"] += 1
        t["rows"].append({
            "m": m, "q_floor": q, "alpha_hat": str(ah),
            "alpha_float_ulps": d_ulps, "mu_exact": str(mu),
            "mu_ulps": mu_ulps,
            "B_m_bracket": bracket_decimal(b_lo, b_hi, 3),
            "beats_alpha_27": ah < ALPHA_27,
        })
    t["alpha_hat_12_not_below_alpha_27"] = int(alpha_hat(12) >= ALPHA_27)
    return t


def check_records(blocks: dict, report: dict, upto: int = 150) -> dict:
    """`record_minima_through_m150`: recompute every level and take the running
    minima. The paper says the sequence need not be monotone in `m`, so the
    record set is the real claim, not the ordering."""
    t: dict = {
        "levels_recomputed": 0, "records_recomputed": 0,
        "record_set_disagreeing_with_the_report": 0,
        "record_rows_disagreeing_in_a_field": 0,
        "levels_where_alpha_rose": 0,
    }
    shipped = report["diagnostics"]["record_minima_through_m150"]
    best, mine = None, []
    for m in range(1, upto + 1):
        t["levels_recomputed"] += 1
        q = q_floor(m)
        a = alpha_hat(m)
        if best is not None and a > best:
            t["levels_where_alpha_rose"] += 1
        if best is None or a < best:
            best = a
            mine.append({"m": m, "q_floor": q, "C_minus": str(c_minus(m, q)),
                         "gamma": str(gamma_m(m, q)), "alpha_hat": str(a),
                         "alpha_float": float(a)})
    t["records_recomputed"] = len(mine)
    if [r["m"] for r in mine] != [r["m"] for r in shipped]:
        t["record_set_disagreeing_with_the_report"] = 1
    for a, b in zip(mine, shipped):
        if any(a[k] != b[k] for k in ("m", "q_floor", "C_minus", "gamma",
                                      "alpha_hat")):
            t["record_rows_disagreeing_in_a_field"] += 1
        elif bits(a["alpha_float"]) != bits(b["alpha_float"]):
            t["record_rows_disagreeing_in_a_field"] += 1
    t["smallest_alpha_reached"] = str(best)
    t["smallest_alpha_float"] = float(best)
    return t


# ---------------------------------------------------------------------------
# section 10 -- the generating identity and the Chernoff half
# ---------------------------------------------------------------------------

def check_generating(upto: int = 60) -> dict:
    """Lemma 10.1, `3 C_m^- = Pr(G_1+...+G_m <= q_m)`, by exact convolution.

    The point of doing it this way is that the convolution never mentions
    `binom(Q-1,m-1)`. If the closed form for the number of compositions were
    wrong, `C_m^-` and a re-derivation from the same closed form would agree
    with each other and both be wrong; a DP over the geometric law would not.
    """
    t: dict = {
        "levels": 0,
        "lemma_10_1_violations": 0,
        "N_m_Q_disagreeing_with_composition_enumeration": 0,
        "compositions_enumerated": 0,
        "distributions_not_summing_below_one": 0,
    }
    # brute-force compositions, for the range where enumeration is affordable
    def compositions(Q: int, m: int) -> int:
        if m == 1:
            return 1 if Q >= 1 else 0
        return sum(compositions(Q - a, m - 1) for a in range(1, Q - m + 2))

    for m in range(1, 8):
        for Q in range(m, m + 9):
            t["compositions_enumerated"] += 1
            if compositions(Q, m) != comb(Q - 1, m - 1):
                t["N_m_Q_disagreeing_with_composition_enumeration"] += 1

    # every level is truncated at ONE ceiling, not at its own q_m. Truncating
    # each level at `q_m + 1` silently drops the states that level m+1 needs,
    # because `q_{m+1}` can exceed `q_m + 1` -- the convolution would then
    # undercount and agree with nothing, which is a slow way to find out.
    ceiling = q_floor(upto) + 2
    step = {k: Fraction(1, 2 ** k) for k in range(1, ceiling + 1)}
    cur = dict(step)
    for m in range(1, upto + 1):
        t["levels"] += 1
        q = q_floor(m)
        if m > 1:
            nxt: dict[int, Fraction] = {}
            for a, pa in cur.items():
                for k in range(1, ceiling - a + 1):
                    nxt[a + k] = nxt.get(a + k, Fraction(0)) + pa * step[k]
            cur = nxt
        tail = sum((v for Q, v in cur.items() if Q <= q), Fraction(0))
        if tail != 3 * c_minus(m, q):
            t["lemma_10_1_violations"] += 1
        if sum(cur.values()) > 1:
            t["distributions_not_summing_below_one"] += 1
    return t


def check_chernoff(i_lo: Fraction, i_hi: Fraction, upto: int = 150) -> dict:
    """Theorem 10.2, `C_m^- <= (1/3) e^{-I_beta m}`, plus the claim that the
    stated `t_*` really optimises the Chernoff exponent."""
    t: dict = {
        "levels": 0, "chernoff_capacity_violations": 0,
        "tightest_ratio": 0.0, "tightest_at_m": None,
        "grid_points": 0, "grid_points_beating_I_beta": 0,
        "optimum_identity_violations": 0,
    }
    for m in range(1, upto + 1):
        t["levels"] += 1
        lo, hi = exp_bracket_signed(-i_hi * m, -i_lo * m)
        rhs_lo = lo / 3
        cm = c_minus(m)
        if cm > rhs_lo:
            t["chernoff_capacity_violations"] += 1
        ratio = float(cm) / float(rhs_lo)
        if ratio > t["tightest_ratio"]:
            t["tightest_ratio"], t["tightest_at_m"] = ratio, m

    # `-f(t) = log(2 e^t - 1) - beta t` must not exceed I_beta anywhere
    b_lo, b_hi = widen(*beta_tight(), 40)
    for n in range(1, 200):
        s = Fraction(n, 50)
        t["grid_points"] += 1
        e_lo, e_hi = exp_bracket_signed(s, s)
        # `_ln_core` raises its argument to the 161st power, so hand it a short
        # rational; the bracket only widens, and the claim needs nothing finer
        hi_arg = simplify(2 * e_hi - 1, 15)[1]
        lo_arg = simplify(2 * e_lo - 1, 15)[0]
        if ln_any(hi_arg)[1] - b_lo * s > i_hi:
            if ln_any(lo_arg)[0] - b_hi * s > i_hi:
                t["grid_points_beating_I_beta"] += 1

    # e^{t*} = beta/(2(beta-1)) reproduces I_beta through the same formula
    l2_lo, l2_hi = ln2_bracket()
    lb_lo, lb_hi = ln_any(b_lo)[0], ln_any(b_hi)[1]
    lm_lo, lm_hi = ln_any(b_lo - 1)[0], ln_any(b_hi - 1)[1]
    ts_lo = lb_lo - l2_hi - lm_hi          # t* = ln beta - ln2 - ln(beta-1)
    ts_hi = lb_hi - l2_lo - lm_lo
    # at t*, 2 e^{t*} - 1 = 1/(beta-1), so -f(t*) = -ln(beta-1) - beta t*
    alt_lo = -lm_hi - b_hi * ts_hi
    alt_hi = -lm_lo - b_lo * ts_lo
    if alt_hi < i_lo or alt_lo > i_hi:
        t["optimum_identity_violations"] = 1
    t["I_beta_from_t_star"] = bracket_decimal(*widen(alt_lo, alt_hi, 30), 9)
    return t


def check_diophantine(upto: int = 400) -> dict:
    """Section 11: `gamma_m = 2^{eps+} - 1`, `eps+ >= ||beta m||`, and the
    convexity step `2^x - 1 >= (log 2) x`."""
    t: dict = {
        "levels": 0,
        "epsilon_plus_outside_the_unit_interval": 0,
        "gamma_below_log2_times_epsilon_plus": 0,
        "convexity_grid_points": 0, "convexity_violations": 0,
        "smallest_epsilon_plus": None, "smallest_epsilon_plus_at_m": None,
    }
    l2_lo, l2_hi = ln2_bracket()
    for n in range(0, 200):
        x = Fraction(n, 50)
        t["convexity_grid_points"] += 1
        p_lo, p_hi = exp_bracket_signed(x * l2_lo, x * l2_hi)
        if p_lo - 1 < l2_hi * x and p_hi - 1 < l2_lo * x:
            t["convexity_violations"] += 1
    b_lo, b_hi = widen(*beta_tight(), 60)
    for m in range(1, upto + 1):
        t["levels"] += 1
        q = q_floor(m)
        ep_lo, ep_hi = (q + 1) - b_hi * m, (q + 1) - b_lo * m
        # `eps+ >= ||beta m||` is NOT a testable claim: `||beta m||` is
        # `min(beta m - q, eps+)`, so `eps+` is one of the two arguments and the
        # inequality holds by definition. Written as a check it was a branch
        # that could never fire, which is worse than no check. What a phase read
        # from the wrong side does break is that `eps+` lies in (0,1) at all.
        if not (0 < ep_lo and ep_hi < 1):
            t["epsilon_plus_outside_the_unit_interval"] += 1
        # `gamma_m = 2^{eps+} - 1` is not a claim to test: `3^m = 2^{beta m}`
        # exactly, so it is the same number written twice, and bracketing an
        # exponential to "confirm" it would only measure my own series. The
        # substantive step of section 11 is the convexity bound below.
        g = gamma_m(m, q)
        if g < l2_lo * ep_lo:
            t["gamma_below_log2_times_epsilon_plus"] += 1
        if t["smallest_epsilon_plus"] is None or ep_hi < t["smallest_epsilon_plus"]:
            t["smallest_epsilon_plus"] = float(ep_hi)
            t["smallest_epsilon_plus_at_m"] = m
    return t


def check_inherited_exponents(paper: str, theta: Fraction) -> dict:
    """Section 15's four previous source exponents against the SAME formula.

    RUN-039 fitted `mu = (theta* - alpha)/(1 - alpha)` to the numbers four
    rounds had published without ever stating it. Section 15 derives it here,
    from `r <= C y^{1-eps} L^eps` and `r >~ N^{theta*}`. So the formula is now
    quoted rather than guessed, and its four inherited outputs are a cross-round
    check on both this round and the previous four.
    """
    t: dict = {"exponents_checked": 0, "disagreeing_with_the_formula": 0,
               "published_not_found_in_the_paper": 0, "rows": []}
    body = paper.split("The previous finite-level source exponents were")
    # stop at the sentence that ends the list -- a 900-character window runs on
    # into `mu -> theta_star = 0.195449...`, which is not one of the four and
    # made a correct check report a miscount
    tail = body[-1].split("replaces this finite sequence")[0] if len(body) > 1 \
        else ""
    found = re.findall(r"(0\.\d{6,})\\ldots", tail)
    inherited = [Fraction(1, 6), Fraction(1, 9), Fraction(4, 45), ALPHA_27]
    if len(found) != len(inherited):
        t["published_not_found_in_the_paper"] = 1
    for alpha, pub in zip(inherited, found):
        t["exponents_checked"] += 1
        mu = mu_dense(alpha, theta)
        v = decimal_verdict(pub, rational_digits(mu, 30))
        if v["verdict"] == "OVER-PUBLISHED":
            t["disagreeing_with_the_formula"] += 1
        t["rows"].append({"alpha": str(alpha), "published": pub,
                          "mu_exact": str(mu), "verdict": v})
    return t


# ---------------------------------------------------------------------------
# sections 3-8 on real orbits
# ---------------------------------------------------------------------------

def suffix_minimum(y: int, cap: int = 400) -> dict | None:
    """The maximal accelerated segment rooted at `y` whose states never fall
    below `y`.

    Section 1 states the premise as "every state BEFORE its endpoint is a
    distinct odd integer at least y". Section 4 then sums `1/Y_t` over
    `t = L-m+1..L` and `1/Y_n^2` over `n = 0..L`, and bounds both using
    `Y >= y` -- for the endpoint too. Those are different premises. RUN-038 was
    caught by exactly this shape once already (Lemma 5.1, endpoint included),
    so both readings are built here and both are counted.
    """
    word, values = accelerated(y, cap)
    L = 0
    while L + 1 < len(values) and values[L + 1] >= y:
        L += 1
    if L < 2:
        return None
    strict = values[:L + 1]
    return {
        "y": y, "L": L, "word": word[:L], "values": strict,
        "endpoint_below_y": L + 1 < len(values) and values[L + 1] < y,
        "distinct": len(set(strict)) == len(strict),
        "loose_values": values[:L + 2] if L + 1 < len(values) else strict,
    }


def block_data(seg: dict, m: int) -> list[dict]:
    v, w = seg["values"], seg["word"]
    L = seg["L"]
    out = []
    for j in range(0, L - m + 1):
        Q = sum(w[j:j + m])
        P = Fraction(1)
        for t in range(j, j + m):
            P *= 1 + Fraction(1, 3 * v[t])
        out.append({"j": j, "Q": Q, "P": P, "g": Fraction(2 ** Q, 3 ** m),
                    "word": tuple(w[j:j + m])})
    return out


def e_bound(m: int, y: int, upper: bool = True) -> Fraction:
    """`E_m(y) = m/y + (3m/(14y)) exp(m/(3y))`."""
    e = _exp_bracket(Fraction(m, 3 * y))[1 if upper else 0]
    return Fraction(m, y) + Fraction(3 * m, 14 * y) * e


def check_orbits(limit: int, blocks: tuple[int, ...] = (2, 3, 4, 6, 12)
                 ) -> dict:
    t: dict = {
        "starts_tried": 0, "segments_built": 0,
        "segments_with_a_repeated_state": 0,
        "segments_meeting_the_section_1_reading": 0,
        "segments_meeting_the_stronger_section_4_reading": 0,
        "segments_with_L_at_least_y": 0,
        "sliding_block_identities_checked": 0,
        "theorem_3_1_violations": 0,
        "summed_balances_checked": 0,
        "theorem_4_1_violations": 0,
        "theorem_4_1_violations_under_the_section_1_reading": 0,
        "loose_readings_available": 0,
        "finance_inequalities_checked": 0,
        "theorem_5_1_violations": 0,
        "exact_words_checked": 0,
        "theorem_6_1_violations": 0,
        "theorem_7_1_checked": 0, "theorem_7_1_violations": 0,
        "theorem_8_1_checked": 0, "theorem_8_1_violations": 0,
        "corollary_8_2_checked": 0, "corollary_8_2_violations": 0,
        "slack_log10_by_m": {},
    }
    slack: dict[int, float] = {}
    for y in range(7, limit, 2):
        if y % 3 == 0:
            continue                       # post-entry sources are 3-free
        t["starts_tried"] += 1
        seg = suffix_minimum(y)
        if seg is None:
            continue
        t["segments_built"] += 1
        if not seg["distinct"]:
            t["segments_with_a_repeated_state"] += 1
            continue
        t["segments_meeting_the_section_1_reading"] += 1
        if all(x >= y for x in seg["values"]):
            t["segments_meeting_the_stronger_section_4_reading"] += 1
        if seg["L"] >= y:
            t["segments_with_L_at_least_y"] += 1
        v, L = seg["values"], seg["L"]
        for m in blocks:
            if L < m + 1:
                continue
            bd = block_data(seg, m)
            for b in bd:
                j = b["j"]
                t["sliding_block_identities_checked"] += 1
                lhs = (b["g"] - 1) / v[j]
                rhs = (Fraction(1, v[j + m]) - Fraction(1, v[j])
                       + (b["P"] - 1) / v[j + m])
                if lhs != rhs:
                    t["theorem_3_1_violations"] += 1
            total = sum((b["g"] - 1) / v[b["j"]] for b in bd)
            t["summed_balances_checked"] += 1
            if total > e_bound(m, y):
                t["theorem_4_1_violations"] += 1
            # the weaker reading: endpoint allowed below y. Same bound, same
            # source, one more state -- and that state is the small one the
            # section 4 arithmetic assumed away.
            if seg["endpoint_below_y"]:
                lv = seg["loose_values"]
                lw = seg["word"] + [v2(3 * lv[L] + 1)]
                lseg = {"values": lv, "word": lw, "L": L + 1, "y": y}
                lbd = block_data(lseg, m)
                lt = sum((b["g"] - 1) / lv[b["j"]] for b in lbd)
                t["loose_readings_available"] += 1
                if lt > e_bound(m, y):
                    t["theorem_4_1_violations_under_the_section_1_reading"] += 1
            q_m = q_floor(m)
            s_neg = sum((Fraction(1, v[b["j"]]) for b in bd if b["Q"] <= q_m),
                        Fraction(0))
            s_pos = sum((Fraction(1, v[b["j"]]) for b in bd if b["Q"] > q_m),
                        Fraction(0))
            t["finance_inequalities_checked"] += 1
            if gamma_m(m, q_m) * s_pos > s_neg + e_bound(m, y):
                t["theorem_5_1_violations"] += 1
            by_word: dict[tuple, Fraction] = {}
            for b in bd:
                by_word[b["word"]] = (by_word.get(b["word"], Fraction(0))
                                      + Fraction(1, v[b["j"]]))
            for w, mass in by_word.items():
                Q = sum(w)
                t["exact_words_checked"] += 1
                cap = (Fraction(2, y)
                       + ln_any(1 + Fraction(3 * 2 ** (Q + 1) * L, y))[1]
                       / (3 * 2 ** Q))
                if mass > cap:
                    t["theorem_6_1_violations"] += 1
            if L >= y and L >= m:
                lgl = ln_any(Fraction(L, y))
                k_hi = k_m_bracket(m)[1]
                t["theorem_7_1_checked"] += 1
                if s_neg > c_minus(m, q_m) * lgl[1] + k_hi:
                    t["theorem_7_1_violations"] += 1
                a_m = (1 + 1 / gamma_m(m, q_m)) * c_minus(m, q_m)
                bh = b_m_bracket(m)[1]
                recip = sum((Fraction(1, x) for x in v[:L]), Fraction(0))
                t["theorem_8_1_checked"] += 1
                bound = a_m * lgl[1] + bh
                if recip > bound:
                    t["theorem_8_1_violations"] += 1
                # the ratio their report renders as a float underflows to 0.0;
                # report it in orders of magnitude instead
                slack[m] = max(slack.get(m, 0.0),
                               float((bound - recip) / 3) / math.log(10))
                t["corollary_8_2_checked"] += 1
                prod = Fraction(1)
                for x in v[:L]:
                    prod *= 1 + Fraction(1, 3 * x)
                if ln_any(simplify(prod, 25)[0])[0] > bound / 3:
                    t["corollary_8_2_violations"] += 1
    t["slack_log10_by_m"] = {str(k): round(vv, 1)
                             for k, vv in sorted(slack.items())}
    return t


def check_cylinders(limit: int, blocks: tuple[int, ...] = (3, 4, 5)) -> dict:
    """Section 6: an exact exponent word of total valuation `Q` selects ONE
    source class mod `2^(Q+1)`, and after the 3-sieve at most two progressions
    mod `3*2^(Q+1)`."""
    t: dict = {
        "sources_scanned": 0, "words_seen": 0,
        "words_spanning_more_than_one_class_mod_2Qplus1": 0,
        "words_spanning_more_than_two_classes_mod_3_2Qplus1": 0,
        "repeated_word_same_residue_checks": 0,
        "largest_Q_reached": 0,
        "words_with_only_one_source_seen": 0,
    }
    for m in blocks:
        groups: dict[tuple, list[int]] = {}
        for x in range(5, limit, 2):
            if x % 3 == 0:
                continue
            t["sources_scanned"] += 1
            w, _ = accelerated(x, m + 2)
            if len(w) < m:
                continue
            groups.setdefault(tuple(w[:m]), []).append(x)
        for w, xs in groups.items():
            Q = sum(w)
            t["words_seen"] += 1
            t["largest_Q_reached"] = max(t["largest_Q_reached"], Q)
            t["repeated_word_same_residue_checks"] += max(0, len(xs) - 1)
            if len(xs) < 2:
                # a singleton cannot disagree with itself; counted so the
                # headline number is not inflated by words that test nothing
                t["words_with_only_one_source_seen"] += 1
            if len({x % (2 ** (Q + 1)) for x in xs}) > 1:
                t["words_spanning_more_than_one_class_mod_2Qplus1"] += 1
            if len({x % (3 * 2 ** (Q + 1)) for x in xs}) > 2:
                t["words_spanning_more_than_two_classes_mod_3_2Qplus1"] += 1
    return t


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, blocks: dict, report: dict, paper: str,
                    i_lo: Fraction, i_hi: Fraction) -> dict:
    """theta*, I_beta, beta -- and where each published float came from.

    `rho* = 4.1164` is a decimal, so `theta* = 1/(rho*+1)` is an exact rational,
    `2500/12791`. Whether the shipped double is the correctly rounded value of
    THAT, or the result of running the same formula in float64 from an already
    rounded `rho*`, is the difference RUN-036 spent a run learning to tell
    apart. Both are computed here and compared bit for bit.
    """
    t: dict = {
        "constants_checked": 0,
        "theta_star_disagreeing_with_both_evaluations": 0,
        "theta_star_from_the_float64_chain_not_the_exact_rational": 0,
        "I_beta_outside_its_bracket": 0,
        "I_beta_published_below_double_precision": 0,
        "beta_float_not_the_nearest_double": 0,
        "constants_disagreeing_across_artifacts": 0,
        "over_published_decimals": 0,
        "rows": [],
    }
    theta = 1 / (RHO_STAR + 1)
    t["theta_star_exact"] = str(theta)
    t["constants_checked"] += 1
    pub_theta = frontier["theta_star"]
    exact_double = float(theta)
    chain_double = 1.0 / (float(RHO_STAR) + 1.0)
    d_exact = bits(pub_theta) - bits(exact_double)
    d_chain = bits(pub_theta) - bits(chain_double)
    if abs(d_exact) > 2 and abs(d_chain) > 2:
        # neither reading of the formula produces it: that would be an error
        t["theta_star_disagreeing_with_both_evaluations"] = 1
    elif d_exact and not d_chain:
        # it IS the formula, evaluated in float64 from an already-rounded rho*
        t["theta_star_from_the_float64_chain_not_the_exact_rational"] = 1
    t["rows"].append({
        "name": "theta_star", "published": repr(pub_theta),
        "exact_rational": str(theta),
        "nearest_double_to_the_exact_rational": repr(exact_double),
        "float64_chain_from_rho_star": repr(chain_double),
        "ulps_vs_exact": bits(pub_theta) - bits(exact_double),
        "ulps_vs_float64_chain": bits(pub_theta) - bits(chain_double),
    })

    t["constants_checked"] += 1
    pub_i = frontier["chernoff_rate_I_beta"]
    # the artifact writes fifteen significant digits; a double carries
    # seventeen. Asking how many ulps away it is measures the two it did not
    # write, which is how RUN-036 once published 75 and 78929 ulps of nothing.
    # The value question is whether it lies in the bracket at its own precision.
    if not (i_lo - Fraction(1, 10 ** 15) <= Fraction(pub_i)
            <= i_hi + Fraction(1, 10 ** 15)):
        t["I_beta_outside_its_bracket"] = 1
    v = ulps_against_bracket(pub_i, i_lo, i_hi)
    if v["decided"] and v["ulps"]:
        t["I_beta_published_below_double_precision"] = 1
    dec = bracket_decimal(i_lo, i_hi, 18)
    t["rows"].append({"name": "I_beta",
                      "published": repr(frontier["chernoff_rate_I_beta"]),
                      "bracket_to_18_places": dec, "verdict": v})
    if dec is not None:
        t["I_beta_decimal_verdict"] = decimal_verdict(
            "%.15f" % frontier["chernoff_rate_I_beta"], dec)
        if t["I_beta_decimal_verdict"]["verdict"] == "OVER-PUBLISHED":
            t["over_published_decimals"] += 1

    t["constants_checked"] += 1
    b_lo, b_hi = beta_tight()
    vb = ulps_against_bracket(frontier["beta"], b_lo, b_hi)
    if vb["decided"] and vb["ulps"]:
        t["beta_float_not_the_nearest_double"] = 1
    t["rows"].append({"name": "beta", "published": repr(frontier["beta"]),
                      "verdict": vb})

    for key in ("beta", "rho_star", "theta_star", "chernoff_rate_I_beta"):
        t["constants_checked"] += 1
        vals = {frontier.get(key), blocks.get(key),
                report["constants"].get(key)}
        vals.discard(None)
        if len(vals) > 1:
            t["constants_disagreeing_across_artifacts"] += 1
    # the paper prints I_beta to fifteen places
    for shown in re.findall(r"=\s*(0\.0549\d+)\\ldots", paper):
        t["constants_checked"] += 1
        if dec is not None:
            vv = decimal_verdict(shown, dec)
            if vv["verdict"] == "OVER-PUBLISHED":
                t["over_published_decimals"] += 1
            t["rows"].append({"name": "I_beta in the paper", "published": shown,
                              "verdict": vv})
    return t


def check_crossover(blocks: dict) -> dict:
    """Where the new certificate actually beats the old one.

    Corollary 8.2 is `P <= exp(B_m/3) (L/y)^alpha^_m`, and `alpha^_12` really is
    below `alpha_27`. But `B_m` is not small, and their own report renders the
    actual-to-bound ratio at m=12 as `0.0`, which is a float underflow rather
    than a measurement. This computes the `L/y` at which the new exponent
    overtakes the old one, giving A-U.2d.11 the most generous possible additive
    constant -- zero. It is a scope observation, not a defect: section 8 claims
    the constants are explicit and finite, and they are.
    """
    t: dict = {"levels": 0, "rows": []}
    for row in blocks["selected_exact_levels"]:
        m = int(row["m"])
        a = alpha_hat(m)
        if a >= ALPHA_27:
            continue
        t["levels"] += 1
        b_hi = b_m_bracket(m)[1]
        need = (b_hi / 3) / (ALPHA_27 - a)          # ln(L/y) at the crossover
        l10 = float(need) / math.log(10)
        t["rows"].append({"m": m, "alpha_hat": str(a),
                          "log10_of_L_over_y_at_crossover": round(l10, 1)})
    return t


# ---------------------------------------------------------------------------
# artifacts and ledger
# ---------------------------------------------------------------------------

def check_artifacts(bundle: pathlib.Path) -> dict:
    t: dict = {
        "files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
        "files_with_no_digest_anywhere": [],
        "checksum_lines_naming_a_missing_file": 0,
        "validation_entries_without_a_digest": 0,
        "builder_covered_by_a_digest": False,
    }
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
    files = val.get("files", {})
    with_digest = set()
    if isinstance(files, dict):
        for n, r in files.items():
            if isinstance(r, dict) and "sha256" in r:
                with_digest.add(n)
            else:
                t["validation_entries_without_a_digest"] += 1
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["builder_covered_by_a_digest"] = (BUILDER in listed
                                        or BUILDER in with_digest)
    t["validation_status"] = val.get("status")
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    """Does the machine-readable ledger carry what section 22 and section 18
    say? RUN-039 found the previous round shipped no open-problems list at all,
    so this one counts the paper's own bullets and compares.

    Coverage gaps are OBSERVATIONS. The gate does not go red over an artifact's
    index -- that line was drawn at RUN-032 and has held since.
    """
    t: dict = {
        "paper_proved_items": 0, "ledger_proved_items": 0,
        "paper_open_items": 0, "ledger_open_items": 0,
        "paper_no_go_headings": 0, "ledger_no_go_items": 0,
        "ledger_has_an_open_key": False,
        "open_items_absent_from_the_ledger": [],
        "no_go_headings_absent_from_the_ledger": [],
        "next_round_disagreeing_with_the_paper": 0,
        "frontier_disagreeing_with_the_paper": 0,
    }
    proved = re.search(r"## 22\.1(.*?)## 22\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(re.findall(r"^\d+\. ", proved.group(1),
                                                 re.M))
    openb = re.search(r"## 22\.4(.*?)(?:\n---|\Z)", paper, re.S)
    bullets: list[str] = []
    if openb:
        bullets = [b.strip(" -;.") for b in
                   re.findall(r"^- (.+)$", openb.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
    no_go = re.findall(r"^## NO-GO (18\.\d) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)

    t["ledger_proved_items"] = len(ledger.get("proved_internal", []))
    t["ledger_no_go_items"] = len(ledger.get("explicit_no_go_boundaries", []))
    open_key = next((k for k in ledger if "open" in k.lower()), None)
    t["ledger_has_an_open_key"] = open_key is not None
    t["ledger_open_items"] = len(ledger.get(open_key, [])) if open_key else 0

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
    if ledger.get("next_round", "").split("--")[0].strip() not in paper:
        if "A-U.2d.13" not in ledger.get("next_round", ""):
            t["next_round_disagreeing_with_the_paper"] = 1
    if "Subpolynomial Block-Transport" not in ledger.get("updated_frontier",
                                                         ""):
        t["frontier_disagreeing_with_the_paper"] = 1
    return t


def check_their_claims(report: dict, res: dict) -> dict:
    """Their checker's own counters beside mine. Different populations, so a
    difference is information, not a failure -- what matters is that nothing
    they counted is something I could not reproduce at all."""
    mine = {
        "exact_sliding_block_identities":
            res["orbits"]["sliding_block_identities_checked"],
        "exact_summed_block_balances": res["orbits"]["summed_balances_checked"],
        "finite_block_error_bounds": res["orbits"]["summed_balances_checked"],
        "exact_code_source_residue_checks": res["cylinders"]["words_seen"],
        "repeated_code_same_residue_checks":
            res["cylinders"]["repeated_word_same_residue_checks"],
        "chernoff_capacity_checks": res["chernoff"]["levels"],
        "symbolic_diophantine_envelope_numeric_sanity_checks":
            res["diophantine"]["levels"],
        "actual_explicit_product_bound_checks":
            res["orbits"]["corollary_8_2_checked"],
    }
    rows = []
    for k, theirs in report["checks"].items():
        rows.append({"check": k, "theirs": theirs, "mine": mine.get(k)})
    return {"rows": rows, "checks_i_did_not_reproduce":
            sum(1 for r in rows if r["mine"] is None)}


# ---------------------------------------------------------------------------

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("hierarchy", "q_floor_disagreeing_with_floor_beta_m"),
    ("hierarchy", "C_minus_disagreeing_with_the_binomial_sum"),
    ("hierarchy", "gamma_disagreeing_with_its_definition"),
    ("hierarchy", "alpha_hat_disagreeing_with_corollary_8_2"),
    ("hierarchy", "alpha_hat_float_not_the_nearest_double"),
    ("hierarchy", "mu_dense_disagreeing_with_the_section_15_formula"),
    ("hierarchy", "B_star_outside_its_bracket"),
    ("hierarchy", "frontier_disagreeing_with_the_block_data"),
    ("hierarchy", "report_disagreeing_with_the_block_data"),
    ("hierarchy", "alpha_hat_12_not_below_alpha_27"),
    ("records", "record_set_disagreeing_with_the_report"),
    ("records", "record_rows_disagreeing_in_a_field"),
    ("generating", "lemma_10_1_violations"),
    ("generating", "N_m_Q_disagreeing_with_composition_enumeration"),
    ("generating", "distributions_not_summing_below_one"),
    ("chernoff", "chernoff_capacity_violations"),
    ("chernoff", "grid_points_beating_I_beta"),
    ("chernoff", "optimum_identity_violations"),
    ("diophantine", "epsilon_plus_outside_the_unit_interval"),
    ("diophantine", "gamma_below_log2_times_epsilon_plus"),
    ("diophantine", "convexity_violations"),
    ("inherited", "disagreeing_with_the_formula"),
    ("inherited", "published_not_found_in_the_paper"),
    ("orbits", "theorem_3_1_violations"),
    ("orbits", "theorem_4_1_violations"),
    ("orbits", "theorem_5_1_violations"),
    ("orbits", "theorem_6_1_violations"),
    ("orbits", "theorem_7_1_violations"),
    ("orbits", "theorem_8_1_violations"),
    ("orbits", "corollary_8_2_violations"),
    ("orbits", "segments_with_a_repeated_state"),
    ("cylinders", "words_spanning_more_than_one_class_mod_2Qplus1"),
    ("cylinders", "words_spanning_more_than_two_classes_mod_3_2Qplus1"),
    ("constants", "theta_star_disagreeing_with_both_evaluations"),
    ("constants", "I_beta_outside_its_bracket"),
    ("constants", "beta_float_not_the_nearest_double"),
    ("constants", "constants_disagreeing_across_artifacts"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
)

# populations that must not be empty, or the counters above measure nothing
NON_VACUITY = (
    ("hierarchy", "levels"),
    ("records", "records_recomputed"),
    ("generating", "levels"),
    ("generating", "compositions_enumerated"),
    ("chernoff", "levels"),
    ("chernoff", "grid_points"),
    ("diophantine", "levels"),
    ("diophantine", "convexity_grid_points"),
    ("inherited", "exponents_checked"),
    ("orbits", "sliding_block_identities_checked"),
    ("orbits", "summed_balances_checked"),
    ("orbits", "exact_words_checked"),
    ("orbits", "finance_inequalities_checked"),
    ("cylinders", "words_seen"),
    ("cylinders", "repeated_word_same_residue_checks"),
    ("constants", "constants_checked"),
    ("premise_reach", "segments_built"),
    # this population is a single segment (y=31) in the whole scanned range,
    # so it is the one most likely to vanish unnoticed
    ("orbits", "theorem_7_1_checked"),
)


def check_premise_reach(limit: int = 60000) -> dict:
    """How often does a real orbit meet the premise sections 7-8 need?

    Theorem 7.1 needs `y >= 7` and `L >= y`; Theorem 8.1 needs
    `L >= max{m, y}`. Both are statements about the hypothetical divergent
    branch, where a segment stays above its source for a long time by
    construction. A real orbit does not: the excursion above `y` lasts about
    `log y` steps while `y` itself grows linearly, so the premise is met almost
    nowhere. This counts the denominator rather than leaving "0 violations" to
    look like coverage it is not -- an unmet premise makes a check vacuous, and
    a vacuous check that reads green is worth less than no check at all.
    """
    t: dict = {
        "sources_scanned": 0, "segments_built": 0,
        "segments_with_L_at_least_y": 0,
        "longest_excursion": 0, "longest_excursion_at_y": None,
        "mean_excursion_length": 0.0,
        "qualifying_sources": [],
    }
    total = 0
    for y in range(7, limit, 2):
        if y % 3 == 0:
            continue
        t["sources_scanned"] += 1
        seg = suffix_minimum(y, 900)
        if seg is None:
            continue
        t["segments_built"] += 1
        L = seg["L"]
        total += L
        if L > t["longest_excursion"]:
            t["longest_excursion"], t["longest_excursion_at_y"] = L, y
        if L >= y:
            t["segments_with_L_at_least_y"] += 1
            if len(t["qualifying_sources"]) < 20:
                t["qualifying_sources"].append({"y": y, "L": L})
    if t["segments_built"]:
        t["mean_excursion_length"] = round(total / t["segments_built"], 2)
    return t

# counters that are DIAGNOSTICS: denominators, populations, provenance. Listing
# them is not decoration -- an integer in none of the three lists can increment
# forever unread, which is exactly how RUN-035 shipped a run with sixteen drills
# audited by nothing while reporting ok.
OBSERVATIONS = (
    ("instrument", "checks"),
    ("hierarchy", "B_star_within_float64_accumulation_of_the_bracket"),
    ("hierarchy", "mu_matching_the_float64_chain_not_the_exact_rational"),
    ("records", "levels_recomputed"),
    ("records", "levels_where_alpha_rose"),
    ("chernoff", "tightest_at_m"),
    ("diophantine", "smallest_epsilon_plus_at_m"),
    ("orbits", "starts_tried"),
    ("orbits", "segments_built"),
    ("orbits", "segments_meeting_the_section_1_reading"),
    ("orbits", "segments_meeting_the_stronger_section_4_reading"),
    ("orbits", "segments_with_L_at_least_y"),
    ("orbits", "loose_readings_available"),
    ("orbits", "theorem_4_1_violations_under_the_section_1_reading"),
    ("orbits", "theorem_8_1_checked"),
    ("orbits", "corollary_8_2_checked"),
    ("cylinders", "sources_scanned"),
    ("cylinders", "largest_Q_reached"),
    ("cylinders", "words_with_only_one_source_seen"),
    ("constants", "I_beta_undecided"),
    ("constants", "I_beta_published_below_double_precision"),
    ("constants", "over_published_decimals"),
    ("constants", "theta_star_from_the_float64_chain_not_the_exact_rational"),
    ("crossover", "levels"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_entries_without_a_digest"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "ledger_no_go_items"),
    ("ledger", "next_round_disagreeing_with_the_paper"),
    ("ledger", "frontier_disagreeing_with_the_paper"),
    ("premise_reach", "sources_scanned"),
    ("premise_reach", "segments_with_L_at_least_y"),
    ("premise_reach", "longest_excursion"),
    ("premise_reach", "longest_excursion_at_y"),
    ("their_claims", "checks_i_did_not_reproduce"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=4000)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    blocks = json.loads((bundle / BLOCKS).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    i_lo, i_hi = i_beta_bracket()
    theta = 1 / (RHO_STAR + 1)

    res: dict = {}
    res["instrument"] = check_instrument()
    res["hierarchy"] = check_hierarchy(blocks, frontier, report, theta)
    res["records"] = check_records(blocks, report)
    res["generating"] = check_generating()
    res["chernoff"] = check_chernoff(i_lo, i_hi)
    res["diophantine"] = check_diophantine()
    res["inherited"] = check_inherited_exponents(paper, theta)
    res["orbits"] = check_orbits(a.limit)
    res["premise_reach"] = check_premise_reach()
    res["cylinders"] = check_cylinders(min(a.limit * 4, 40000))
    res["constants"] = check_constants(frontier, blocks, report, paper,
                                       i_lo, i_hi)
    res["crossover"] = check_crossover(blocks)
    res["artifacts"] = check_artifacts(bundle)
    res["ledger"] = check_ledger(ledger, paper)
    res["their_claims"] = check_their_claims(report, res)

    failures = []
    for sec, key in FAILURE_COUNTERS:
        v = res[sec][key]
        if (len(v) if isinstance(v, list) else v):
            failures.append("%s.%s = %s" % (sec, key, v))
    vacuous = ["%s.%s" % (s, k) for s, k in NON_VACUITY if not res[s][k]]

    # every integer counter must be either a declared failure or a declared
    # observation. An unlisted one could increment forever unread -- that is
    # how RUN-035 shipped a run with sixteen drills audited by nothing.
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
        "run": "RUN-040", "round": "A-U.2d.12", "bundle": str(bundle),
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
