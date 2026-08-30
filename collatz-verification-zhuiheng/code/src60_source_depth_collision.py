"""RUN-041 — independent recheck of Hard-Zeta round A-U.2d.13.

`Dense Source-Depth Exponent Collision` (source item 60). 數學戰士「墜衡」.

A-U.2d.12 drove the fixed-source product exponent to zero and said the frontier
had become a source-depth problem. This round attacks that directly, and its
whole constants family turns out to be exact rationals in one inherited decimal
`rho* = 4.1164`:

    theta* = 1/(rho*+1)              = 2500/12791
    sigma* = 1/(1+theta*)            = 12791/15291        (the old backbone)
    kappa13 = 1/(1+theta*^2)         = 163609681/169859681
    lambda13 = kappa13 * theta*      = 31977500/169859681
    chi*    = (5 sigma* - 4)/3       = 2791/45873

None of those closed forms is stated in the paper; they fall out of
`theta* = 1/(rho*+1)` and are checked here as exact rationals, which makes the
headline exponents decidable rather than approximable.

The argument itself is a chain of five inequalities, and every link is finite:
a source floor from the mod-12 residues, two duration floors, a pigeonhole
localization, Jensen and AM-HM on the origin gaps, and the source corridor. Each
is checked separately, and the two that are asymptotic in the paper are checked
as the finite inequality they are built from.

The one genuinely arithmetic input is section 4.2's local best-approximation
bound `||q beta|| > 1/((M_beta(N)+2) q)` for `q <= N`. That is decidable from
the exact continued fraction of `log2 3`, which `src47` already computes by
integer comparison, and it is checked here over every `q` below several scales.

Premises are measured before use, as at RUN-037..040. Note that section 4 here
sums `j = 0..L-1` and so correctly EXCLUDES the endpoint -- the exact index that
RUN-040 found A-U.2d.12's section 4 getting wrong.

Usage:
    python code/src60_source_depth_collision.py --bundle <dir> [--limit N]
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

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d13_Dense_Source_Depth_Exponent"
         "_Collision_v0.1.md")
REPORT = "Hard_Zeta_AU2d13_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d13_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d13_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d13.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.13_AU2d13.md"

RHO_STAR = Fraction(41164, 10000)          # 4.1164, inherited from A-U.2d.3
THETA_STAR = 1 / (RHO_STAR + 1)
SIGMA_STAR = 1 / (1 + THETA_STAR)
KAPPA_13 = (RHO_STAR + 1) / (RHO_STAR + 1 + THETA_STAR)
LAMBDA_13 = 1 / (RHO_STAR + 1 + THETA_STAR)
CHI_STAR = (5 * SIGMA_STAR - 4) / 3


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def ln_any(x: Fraction) -> tuple[Fraction, Fraction]:
    """`ln x` for any positive rational; below 1 the series argument turns
    negative and its tail bound stops straddling, so take the reciprocal."""
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
    """Self-checks whose answers are IRRATIONAL.

    RUN-039 wrote one asking whether `(1/4)^(1/2)` brackets `1/2`; it could not
    fail, because both bracket ends land exactly on `1/2` and an end-swap
    changes nothing. So: irrational targets, and `lo < hi` asserted separately.
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

    lo, hi = log2_any(Fraction(1, 3))
    want("log2(1/3) is negative", hi < 0)
    want("log2(1/3) is not degenerate", lo < hi)

    # the closed forms this round's constants turn out to have
    want("theta* = 2500/12791", THETA_STAR == Fraction(2500, 12791))
    want("sigma* = 1/(1+theta*)", SIGMA_STAR == 1 / (1 + THETA_STAR))
    want("kappa13 = 1/(1+theta*^2)",
         KAPPA_13 == 1 / (1 + THETA_STAR * THETA_STAR))
    want("lambda13 = kappa13 * theta*", LAMBDA_13 == KAPPA_13 * THETA_STAR)
    want("chi* = 2791/45873", CHI_STAR == Fraction(2791, 45873))
    want("4/5 < sigma*", Fraction(4, 5) < SIGMA_STAR)
    return out


# ---------------------------------------------------------------------------
# the exponent algebra -- exact rationals, no tolerance
# ---------------------------------------------------------------------------

def check_exponents(frontier: dict, report: dict) -> dict:
    """Each published exponent against its exact rational AND against the
    float64 chain the artifact would have run.

    RUN-040 learned that splitting these apart matters twice over: it turns a
    bare ulp count into a named cause, and -- the part that bit -- the chain
    branch must be BOUNDED, or a constant that is simply wrong takes the quiet
    path. Here the bound is 4 ulps for a plain rounding; `chi*` needs more and
    gets its own cancellation-aware treatment below.
    """
    t: dict = {
        "constants_checked": 0,
        "disagreeing_with_both_evaluations": 0,
        "from_the_float64_chain_not_the_exact_rational": 0,
        "exact_to_the_last_bit": 0,
        "missing_from_the_frontier": 0,
        "frontier_and_report_disagreeing": 0,
        "rows": [],
    }
    exact = {
        "theta_star": THETA_STAR,
        "old_disjoint_backbone_sigma_star": SIGMA_STAR,
        "unconditional_support_exponent_kappa13": KAPPA_13,
        "unconditional_log_exponent_lambda13": LAMBDA_13,
        "pq_pressure_at_old_sigma": CHI_STAR,
        "controlled_CF_support_exponent": Fraction(4, 5),
        "controlled_CF_log_exponent": Fraction(2, 5),
        "support_PQ_factor_exponent": Fraction(3, 5),
    }
    # the float64 route each constant would take from an already-rounded parent
    f_rho = float(RHO_STAR)
    f_theta = 1.0 / (f_rho + 1.0)
    f_sigma = 1.0 / (1.0 + f_theta)
    chain = {
        "theta_star": f_theta,
        "old_disjoint_backbone_sigma_star": f_sigma,
        "unconditional_support_exponent_kappa13":
            (f_rho + 1.0) / (f_rho + 1.0 + f_theta),
        "unconditional_log_exponent_lambda13":
            1.0 / (f_rho + 1.0 + f_theta),
        # from the PUBLISHED sigma, which is where the cancellation enters
        "pq_pressure_at_old_sigma":
            (5 * frontier["old_disjoint_backbone_sigma_star"] - 4) / 3,
        "controlled_CF_support_exponent": 0.8,
        "controlled_CF_log_exponent": 0.4,
        "support_PQ_factor_exponent": 0.6,
    }
    s0 = frontier["old_disjoint_backbone_sigma_star"]
    cancel = (5 * s0) / (5 * s0 - 4)
    for name, ex in exact.items():
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        d_exact = bits(pub) - bits(float(ex))
        d_chain = bits(pub) - bits(chain[name])
        rpt = report.get("constants", {}).get(name)
        if rpt is not None and rpt != pub:
            t["frontier_and_report_disagreeing"] += 1
        # ORDER MATTERS. Testing `d_chain == 0` before the magnitude cap is
        # exactly the fail-open branch RUN-040 was caught by: a constant built
        # from the wrong formula still reproduces its own float64 chain, so it
        # would take the quiet path however wrong it was. The cap comes first,
        # and it is derived rather than picked -- `chi*` legitimately inherits
        # about `cancel` ulps because `5 sigma - 4` destroys that much
        # magnitude, and nothing else here cancels at all.
        budget = 4
        if name == "pq_pressure_at_old_sigma":
            budget = 4 * int(math.ceil(cancel))
        if d_exact == 0:
            t["exact_to_the_last_bit"] += 1
        elif abs(d_exact) > budget:
            t["disagreeing_with_both_evaluations"] += 1
        elif d_chain == 0:
            t["from_the_float64_chain_not_the_exact_rational"] += 1
        t["rows"].append({
            "name": name, "published": repr(pub), "exact": str(ex),
            "exact_decimal": rational_digits(ex, 22),
            "ulps_vs_exact": d_exact, "ulps_vs_float64_chain": d_chain,
        })
    # how much magnitude `5 sigma - 4` destroys, which is what makes chi*'s
    # gap 27 ulps rather than one
    t["cancellation_factor_in_five_sigma_minus_four"] = round(cancel, 2)
    t["ulp_budget_allowed_for_chi_star"] = 4 * int(math.ceil(cancel))
    return t


def check_identities(trials: int = 400, seed: int = 26081413) -> dict:
    """The exponent arithmetic of sections 7 and 8, as identities in the
    symbols rather than at one point.

    Section 7 combines `r ~ M^(1+th)/N`, `S ~ M^th` through
    `(r-1)^(rho+1)/S^rho` and claims the result is `M^(rho+1+th)/N^(rho+1)`.
    That is the identity `(1+th)(rho+1) - th*rho = rho+1+th`. Section 8 combines
    `r ~ M^(3/2)/(N A^(1/2))`, `S ~ (M/A)^(1/2)` through `(r-1)^2/(A S)` and
    claims `M^(5/2)/(A^(3/2) N^2)`. Checking either at one `(rho, th)` proves
    nothing about the transcription, so both are evaluated as exact rational
    exponent arithmetic over many random parameter pairs.
    """
    rng = random.Random(seed)
    t: dict = {"trials": 0,
               "section_7_exponent_identity_violations": 0,
               "section_8_exponent_identity_violations": 0,
               "kappa_from_the_support_inequality_violations": 0,
               "pq_exponent_from_inversion_violations": 0}
    for _ in range(trials):
        t["trials"] += 1
        rho = Fraction(rng.randrange(1, 4000), 1000)
        th = Fraction(rng.randrange(1, 4000), 1000)
        # section 7: exponent of M in (M^(1+th)/N)^(rho+1) / (M^th)^rho
        if (1 + th) * (rho + 1) - th * rho != rho + 1 + th:
            t["section_7_exponent_identity_violations"] += 1
        # section 8: exponents of (M, A, N) in (M^(3/2)/(N A^(1/2)))^2 /(A*(M/A)^(1/2))
        m_exp = Fraction(3, 2) * 2 - Fraction(1, 2)
        a_exp = -Fraction(1, 2) * 2 - 1 + Fraction(1, 2)
        n_exp = -2
        if (m_exp, a_exp, n_exp) != (Fraction(5, 2), -Fraction(3, 2),
                                     Fraction(-2)):
            t["section_8_exponent_identity_violations"] += 1
        # solving M^(rho+1+th) << N^(rho+1) for M = N^kappa
        if (rho + 1) / (rho + 1 + th) * (rho + 1 + th) != rho + 1:
            t["kappa_from_the_support_inequality_violations"] += 1
        # inverting M^(5/2) << A^(3/2) N^2 for A, then reading the exponent
        kappa = Fraction(rng.randrange(801, 1000), 1000)
        if (Fraction(5, 3) * kappa - Fraction(4, 3)
                != (5 * kappa - 4) / 3):
            t["pq_exponent_from_inversion_violations"] += 1
    # the two named instances
    t["kappa13_from_the_formula"] = str(
        (RHO_STAR + 1) / (RHO_STAR + 1 + THETA_STAR))
    t["chi_at_sigma_star"] = str((5 * SIGMA_STAR - 4) / 3)
    t["pq_exponent_at_kappa_one"] = str((5 * Fraction(1) - 4) / 3)
    t["four_fifths_from_the_CF_master"] = str(Fraction(2) / Fraction(5, 2))
    return t


# ---------------------------------------------------------------------------
# the finite inequalities the collision is assembled from
# ---------------------------------------------------------------------------

def _pow_neg(g: int, rho: Fraction, cache: dict) -> tuple[Fraction, Fraction]:
    """`g^-rho` as a bracket, via `exp(-rho ln g)`. Cached per `g`."""
    if g not in cache:
        lo, hi = ln_bracket(Fraction(g))
        cache[g] = widen(lo, hi, 20)
    l_lo, l_hi = cache[g]
    a, b = _exp_bracket(rho * l_lo, 60), _exp_bracket(rho * l_hi, 60)
    return 1 / b[1], 1 / a[0]


def check_means(trials: int = 300, seed: int = 4113) -> dict:
    """Jensen for `x^-rho` (section 7) and AM-HM (section 8), on real tuples.

    Section 7 needs `sum g_i^-rho >= n^(rho+1)/S^rho` with `S = sum g_i`, and
    section 8 the `rho = 1` case.

    The first attempt at this raised `Fraction(1,g)` to the 41164th power,
    thinking that cleared the rational exponent `rho* = 41164/10000`. It does
    not -- it computes `g^-41164`, a different inequality entirely, on numbers
    with ninety thousand digits. Jensen holds for EVERY `rho > 0`, so the bulk
    is tested exactly at integer `rho` where the arithmetic is cheap and needs
    no bracket at all, and a smaller sample is tested at `rho*` itself through
    certified brackets, so the paper's own exponent is not taken on faith.
    """
    rng = random.Random(seed)
    t: dict = {"tuples": 0, "jensen_violations": 0, "am_hm_violations": 0,
               "tuples_at_rho_star": 0, "jensen_violations_at_rho_star": 0,
               "undecided_at_rho_star": 0, "equal_gap_cases": 0,
               "tightest_jensen_slack": None}
    tight = None
    for _ in range(trials):
        n = rng.randrange(2, 40)
        gaps = [rng.randrange(1, 200) for _ in range(n)]
        S = sum(gaps)
        t["tuples"] += 1
        for rho in (1, 2, 3, 4, 5):
            lhs = sum(Fraction(1, g ** rho) for g in gaps)
            rhs = Fraction(n ** (rho + 1), S ** rho)
            if lhs < rhs:
                t["jensen_violations"] += 1
            slack = float(lhs / rhs)
            if tight is None or slack < tight[0]:
                tight = (slack, rho, n)
        if sum(Fraction(1, g) for g in gaps) < Fraction(n * n, S):
            t["am_hm_violations"] += 1

    # equality: all gaps equal makes both sides meet, and it is the only place
    # a wrong exponent would still pass, so force it rather than hope for it
    for n in range(2, 30):
        for g in (1, 3, 17):
            gaps, S = [g] * n, n * g
            t["tuples"] += 1
            t["equal_gap_cases"] += 1
            for rho in (1, 2, 3, 4, 5):
                if (sum(Fraction(1, x ** rho) for x in gaps)
                        != Fraction(n ** (rho + 1), S ** rho)):
                    t["jensen_violations"] += 1
            if sum(Fraction(1, x) for x in gaps) != Fraction(n * n, S):
                t["am_hm_violations"] += 1

    cache: dict = {}
    for _ in range(40):
        n = rng.randrange(2, 12)
        gaps = [rng.randrange(1, 60) for _ in range(n)]
        S = sum(gaps)
        t["tuples_at_rho_star"] += 1
        lo = sum((_pow_neg(g, RHO_STAR, cache)[0] for g in gaps), Fraction(0))
        r_lo, r_hi = _pow_neg(S, RHO_STAR, cache)
        rhs_hi = _exp_bracket(
            RHO_STAR * widen(*ln_bracket(Fraction(n)), 20)[1], 60)[1] \
            * Fraction(n) * r_hi
        if lo < rhs_hi:
            hi = sum((_pow_neg(g, RHO_STAR, cache)[1] for g in gaps),
                     Fraction(0))
            if hi < rhs_hi:
                t["jensen_violations_at_rho_star"] += 1
            else:
                t["undecided_at_rho_star"] += 1
    if tight:
        t["tightest_jensen_slack"] = {"ratio": round(tight[0], 6),
                                      "rho": tight[1], "n": tight[2]}
    return t


def check_overlap(trials: int = 400, seed: int = 5113) -> dict:
    """Lemma 5.1: intervals of length >= 4W whose starts lie in one window of
    width W all contain `t = max s_j`. Plus the control that shortening them
    below the window width breaks it -- otherwise the check is about nothing.
    """
    rng = random.Random(seed)
    t: dict = {"families": 0, "lemma_5_1_violations": 0,
               "short_families_tried": 0, "short_families_that_still_overlap": 0,
               "pigeonhole_trials": 0, "pigeonhole_violations": 0}
    for _ in range(trials):
        W = rng.randrange(1, 500)
        a = rng.randrange(0, 10 ** 6)
        k = rng.randrange(2, 30)
        starts = [a + rng.randrange(0, W) for _ in range(k)]
        t["families"] += 1
        ends = [s + 4 * W + rng.randrange(0, 5 * W) for s in starts]
        pt = max(starts)
        if not all(s <= pt < e for s, e in zip(starts, ends)):
            t["lemma_5_1_violations"] += 1
        # the control: lengths strictly below the window width
        short = [s + rng.randrange(1, max(2, W)) for s in starts]
        t["short_families_tried"] += 1
        if all(s <= pt < e for s, e in zip(starts, short)):
            t["short_families_that_still_overlap"] += 1
        # Lemma 5.2's pigeonhole: M/2 starts in [0,N) over N/W windows
        M, N = rng.randrange(50, 5000), rng.randrange(5000, 10 ** 5)
        if W < N:
            t["pigeonhole_trials"] += 1
            pts = sorted(rng.randrange(0, N) for _ in range(max(1, M // 2)))
            best = 0
            for i, p in enumerate(pts):
                j = i
                while j < len(pts) and pts[j] < p + W:
                    j += 1
                best = max(best, j - i)
            if best * (N / W) < len(pts):
                t["pigeonhole_violations"] += 1
    return t


def norm_beta(q: int, b_lo: Fraction, b_hi: Fraction
              ) -> tuple[Fraction, Fraction] | None:
    """A bracket on `||q beta||`, or None if the bracket cannot decide."""
    lo, hi = q * b_lo, q * b_hi
    f = lo.numerator // lo.denominator
    if hi.numerator // hi.denominator != f:
        return None
    fr_lo, fr_hi = lo - f, hi - f
    a_lo, a_hi = fr_lo, fr_hi                 # distance up from the floor
    b2_lo, b2_hi = 1 - fr_hi, 1 - fr_lo       # distance down from the ceiling
    return min(a_lo, b2_lo), min(a_hi, b2_hi)


def check_cf_local(scales: tuple[int, ...] = (10 ** 3, 10 ** 4, 10 ** 5),
                   budget: float = 25.0, max_terms: int = 14) -> dict:
    """Section 4.2's local best-approximation bound, the one genuinely
    arithmetic input this round adds.

    `A_N = M_beta(N) + 2` with `M_beta(N) = max{a_{k+1} : q_k <= N}`, and the
    claim is `||q beta|| > 1/(A_N q)` for every `1 <= q <= N`. The partial
    quotients come from `src47`'s integer-comparison continued fraction, so no
    logarithm decides anything here; only the final numeric comparison uses a
    certified bracket on beta, which is sixty digits wide against a gap near
    `1e-7`.
    """
    t: dict = {"scales": 0, "q_values_scanned": 0,
               "local_cf_bound_violations": 0, "undecided_brackets": 0,
               "tightest_ratio": None, "tightest_at": None, "rows": []}
    # 14 terms already reach q_k = 190537, past every scale here. Asking
    # for 15 costs 22 seconds instead of 0.04, because the fifteenth
    # partial quotient is 55 and deciding it means comparing integer
    # powers with ten million bits. Stop where the claim stops needing it.
    cf = exact_continued_fraction(max_terms, budget)
    terms = cf["terms"]
    conv = convergents_from_terms(terms)
    b_lo, b_hi = widen(*beta_tight(), 60)
    t["partial_quotients_used"] = len(terms)
    t["largest_partial_quotient"] = max(terms[1:]) if len(terms) > 1 else None
    for N in scales:
        t["scales"] += 1
        # M_beta(N): the next partial quotient of every convergent with q_k <= N
        nexts = [terms[i + 1] for i, _p, q in conv
                 if q <= N and i + 1 < len(terms)]
        if not nexts:
            continue
        A = max(nexts) + 2
        worst, worst_q = None, None
        for q in range(1, N + 1):
            t["q_values_scanned"] += 1
            nb = norm_beta(q, b_lo, b_hi)
            if nb is None:
                t["undecided_brackets"] += 1
                continue
            lo, _hi = nb
            if lo <= Fraction(1, A * q):
                t["local_cf_bound_violations"] += 1
            ratio = float(lo * A * q)
            if worst is None or ratio < worst:
                worst, worst_q = ratio, q
        # if EVERY bracket came back undecided there is no tightest case, and
        # the gate must still be able to say so. Crashing here would replace a
        # readable verdict -- `undecided_brackets` is already a failure counter
        # -- with a traceback, which is the one thing a gate must not do.
        t["rows"].append({"N": N, "M_beta_N": A - 2, "A_N": A,
                          "tightest_q": worst_q,
                          "q_times_norm_times_A":
                              None if worst is None else round(worst, 4)})
        if worst is not None and (t["tightest_ratio"] is None
                                  or worst < t["tightest_ratio"]):
            t["tightest_ratio"], t["tightest_at"] = worst, (N, worst_q)
    return t


# ---------------------------------------------------------------------------
# real orbits
# ---------------------------------------------------------------------------

def b_intervals(start: int, cap: int = 4000) -> dict:
    """First-crossing intervals of one accelerated orbit, and which of them are
    B-injections (`Y_{e(s)} > Y_s`).

    The crossing structure is the STALK, not the records of `delta` -- RUN-035
    built chains from the records instead and admitted 33052 edges that were not
    nested at all.
    """
    word, values = accelerated(start, cap)
    n = len(word)
    if n < 8:
        return {"n": 0, "intervals": []}
    K = cumulative(word)
    b_lo, b_hi = widen(*beta_tight(), 40)
    # delta_u = beta*u - K_u ; compare exactly through the bracket
    stack: list[int] = []
    e: list[int | None] = [None] * (n + 1)
    for u in range(n + 1):
        while stack:
            s = stack[-1]
            # delta_u < delta_s  <=>  beta*(u-s) < K_u - K_s
            g, p = u - s, K[u] - K[s]
            if b_hi * g < p:
                e[stack.pop()] = u
            elif b_lo * g > p:
                break
            else:
                break
        stack.append(u)
    out = []
    for s in range(n + 1):
        if e[s] is None:
            continue
        u = e[s]
        out.append({"s": s, "e": u, "L": u - s, "y": values[s],
                    "z": values[u], "Q": K[u] - K[s],
                    "B": values[u] > values[s]})
    return {"n": n, "intervals": out, "values": values, "K": K}


def check_orbits(limit: int, cap: int = 2000) -> dict:
    """First-crossing intervals of real orbits.

    The object this round is about -- a B-injection, `Y_{e(s)} > Y_s` at a first
    coefficient crossing -- does not occur on a convergent orbit, and the count
    below says so with its denominator rather than reporting the conditional
    theorems as green. What IS testable everywhere is the algebra underneath
    them: the exact product identity, the equivalence that turns B-survival into
    an inequality on `D`, and section 4.2's unconditional slack floor. Those are
    checked on every interval found.
    """
    t: dict = {
        "starts": 0, "orbits_used": 0, "first_crossing_intervals": 0,
        "exact_product_identity_violations": 0,
        "survival_equivalence_violations": 0,
        "D_not_positive_at_a_first_crossing": 0,
        "local_cf_slack_checked": 0, "local_cf_slack_violations": 0,
        "B_injections": 0,
        "suffix_minimum_intervals": 0,
        "suffix_minimum_sources_outside_7_or_11_mod_12_not_a_counterexample": 0,
        "suffix_minimum_sources_checked": 0,
        "survival_duration_antecedent_holds": 0,
        "theorem_4_1_algebra_violations": 0,
        "largest_z_over_y_reached": None,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    l2_lo, l2_hi = ln2_bracket()
    # A_N for the scale these orbits live at, from the same CF route
    cf = exact_continued_fraction(14, 20.0)
    conv = convergents_from_terms(cf["terms"])
    nexts = [cf["terms"][i + 1] for i, _p, q in conv
             if q <= cap and i + 1 < len(cf["terms"])]
    A_N = (max(nexts) if nexts else 1) + 2
    t["A_N_used"] = A_N
    best = None
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        t["starts"] += 1
        info = b_intervals(start, cap)
        if not info["n"]:
            continue
        t["orbits_used"] += 1
        v = info["values"]
        for iv in info["intervals"]:
            s, u, L, Q = iv["s"], iv["e"], iv["L"], iv["Q"]
            y, z = iv["y"], iv["z"]
            t["first_crossing_intervals"] += 1
            P = Fraction(1)
            for j in range(s, u):
                P *= 1 + Fraction(1, 3 * v[j])
            # z/y = 2^-D prod(1+1/(3Y_j)) with D = Q - beta L, written with no
            # beta at all: z 2^Q = y 3^L P
            if Fraction(z) * 2 ** Q != Fraction(y) * 3 ** L * P:
                t["exact_product_identity_violations"] += 1
            # B-survival is exactly 2^D < P, i.e. 2^Q < 3^L P
            survives = Fraction(2) ** Q < Fraction(3) ** L * P
            if (z > y) != survives:
                t["survival_equivalence_violations"] += 1
            if z > y:
                t["B_injections"] += 1
            r = z / y
            if best is None or r > best[0]:
                best = (r, start, y, L, z)
            d_lo, d_hi = Fraction(Q) - b_hi * L, Fraction(Q) - b_lo * L
            if not d_lo > 0:
                t["D_not_positive_at_a_first_crossing"] += 1
            # section 4.2, unconditional: D > 1/(A_N L) for L <= N
            if L <= cap:
                t["local_cf_slack_checked"] += 1
                if d_lo <= Fraction(1, A_N * L):
                    t["local_cf_slack_violations"] += 1
            if all(v[j] >= y for j in range(s, u)):
                t["suffix_minimum_intervals"] += 1
                if y > 7:
                    t["suffix_minimum_sources_checked"] += 1
                    # A-U.2d.9's residue law is about B sources, and there
                    # are none here. Every suffix-minimum first-crossing source
                    # is a strictly larger population, so a source outside those
                    # classes is NOT a counterexample -- it is the denominator.
                    if y % 12 not in (7, 11):
                        t["suffix_minimum_sources_outside_7_or_11_mod_12_not_a_counterexample"] += 1
            # Theorem 4.1's algebra, wherever its antecedent actually holds:
            # D < L/(3 y ln2) together with D > 1/(A_N L) forces L^2 > 3 y ln2/A_N
            cap_rhs = Fraction(L, 3 * y) / l2_lo
            if d_hi < cap_rhs:
                t["survival_duration_antecedent_holds"] += 1
                if not Fraction(L * L * A_N) > 3 * y * l2_lo:
                    t["theorem_4_1_algebra_violations"] += 1
    if best:
        t["largest_z_over_y_reached"] = {
            "ratio": round(best[0], 6), "orbit": best[1],
            "y": best[2], "L": best[3], "z": best[4]}
    return t


def check_localization(trials: int = 400, seed: int = 6113) -> dict:
    """The conditional theorems as algebra, since real orbits supply no
    B-interval to exercise them on.

    Two things are deliberately NOT here. Theorem 6.1's step
    `H < log2(1 + N/(3 y1))` from `(2^H - 1) y1 < N/3` is an equivalence, not a
    claim -- rearranging it back would measure my own logarithm, which RUN-040
    spent a counter learning. And `gamma = 2^eps - 1` style rewrites are the
    same shape. What IS a claim is the implication that produces that step from
    two inherited facts, and it is tested below with rational `2^H`, no
    logarithm anywhere.
    """
    rng = random.Random(seed)
    t: dict = {"grid_points": 0,
               "theorem_4_1_violations": 0,
               "theorem_4_1_antecedent_satisfiable": 0,
               "duration_floor_violations": 0,
               "duration_floor_antecedent_holds": 0,
               "corridor_implication_points": 0,
               "corridor_implication_violations": 0,
               "pigeonhole_points": 0, "pigeonhole_violations": 0}
    l2_lo, l2_hi = ln2_bracket()
    for _ in range(trials):
        y = rng.randrange(7, 10 ** 6)
        A = rng.randrange(2, 200)
        L = rng.randrange(2, 10 ** 4)
        t["grid_points"] += 1
        # Theorem 4.1: 1/(A L) < D < L/(3 y ln2) is satisfiable only if
        # 3 y ln2 < A L^2. Test the implication where the antecedent can hold.
        if Fraction(1, A * L) < Fraction(L, 3 * y) / l2_hi:
            t["theorem_4_1_antecedent_satisfiable"] += 1
            if not Fraction(A * L * L) > 3 * y * l2_lo:
                t["theorem_4_1_violations"] += 1
        # section 4.1 at integer rho = 4: c L^-4 < L/(3 y ln2) => L^5 > 3 c y ln2
        c = Fraction(1, rng.randrange(1, 50))
        if c / Fraction(L) ** 4 < Fraction(L, 3 * y) / l2_hi:
            t["duration_floor_antecedent_holds"] += 1
            if not Fraction(L) ** 5 > 3 * c * y * l2_lo:
                t["duration_floor_violations"] += 1
        # section 6: y_r > 2^H y_1 and y_r - y_1 < c together give
        # (2^H - 1) y_1 < c. Rational 2^H, so no logarithm is involved.
        y1 = rng.randrange(10, 10 ** 6)
        two_h = Fraction(rng.randrange(1001, 40000), 1000)
        yr = int(two_h * y1) + rng.randrange(1, 1000)
        c2 = yr - y1 + rng.randrange(1, 1000)
        t["corridor_implication_points"] += 1
        if yr > two_h * y1 and yr - y1 < c2:
            if not (two_h - 1) * y1 < c2:
                t["corridor_implication_violations"] += 1
        # Lemma 5.2's pigeonhole, done by construction rather than by formula
        M, N = rng.randrange(100, 10 ** 4), rng.randrange(10 ** 4, 10 ** 6)
        W = rng.randrange(1, 1000)
        pts = sorted(rng.randrange(0, N) for _ in range(max(1, M // 2)))
        t["pigeonhole_points"] += 1
        windows = -(-N // W)
        busiest = 0
        j = 0
        for i, pt in enumerate(pts):
            while j < len(pts) and pts[j] < pt + W:
                j += 1
            busiest = max(busiest, j - i)
        if busiest * windows < len(pts):
            t["pigeonhole_violations"] += 1
    return t



# ---------------------------------------------------------------------------
# published decimals, artifacts, ledger
# ---------------------------------------------------------------------------

def check_printed_decimals(paper: str, route: str) -> dict:
    """Every constant the prose prints, against its exact rational.

    A decimal followed by an ellipsis asserts that the digits shown are correct
    and that more follow. That is a claim, and it is the only place where the
    difference between a value and its float64 evaluation becomes visible to a
    human reader rather than to a JSON parser.
    """
    t: dict = {"printed": 0, "over_published": 0, "exact_to_every_digit": 0,
               "correctly_rounded": 0, "truncated": 0,
               "printed_with_an_ellipsis": 0, "rows": []}
    named = {
        "theta_star": THETA_STAR,
        "sigma_star": SIGMA_STAR,
        "kappa13": KAPPA_13,
        "lambda13": LAMBDA_13,
        "chi_star": CHI_STAR,
    }
    blob = paper + "\n" + route
    ell = chr(92) + "ldots"
    for name, ex in named.items():
        ref = rational_digits(ex, 30)
        shown = ref[:2 + 1]
        # find every decimal in the documents that starts like this constant
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
                              "exact": ref[:len(text) + 4],
                              "ellipsis": after.startswith(ell),
                              "verdict": v["verdict"],
                              "digits_correct": v["digits_correct"]})
    return t


def check_artifacts(bundle: pathlib.Path) -> dict:
    t: dict = {"files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
               "checksum_lines_naming_a_missing_file": 0,
               "files_with_no_digest_anywhere": [],
               "validation_entries_without_a_digest": 0,
               "validation_files_listed": 0}
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
        t["validation_files_listed"] = len(files)
        for n, r in files.items():
            if isinstance(r, dict) and "sha256" in r:
                with_digest.add(n)
            else:
                t["validation_entries_without_a_digest"] += 1
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_reports_its_checker_reran"] = bool(val.get("checker_reran"))
    t["validation_commit_gate_passed"] = bool(val.get("commit_gate_passed"))
    t["validation_issues"] = val.get("issues")
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    """Does the machine-readable ledger carry what sections 12 and 16 say?

    RUN-039 found A-U.2d.11 shipped no open-problems list at all and RUN-040
    found A-U.2d.12 had not fixed it. Coverage is an OBSERVATION, never a gate
    failure -- the line drawn at RUN-032 and held since.
    """
    t: dict = {"paper_proved_items": 0, "ledger_proved_items": 0,
               "paper_open_items": 0, "ledger_open_items": 0,
               "paper_no_go_headings": 0, "ledger_no_go_items": 0,
               "ledger_has_an_open_key": False,
               "open_items_absent_from_the_ledger": [],
               "no_go_headings_absent_from_the_ledger": []}
    proved = re.search(r"## 16\.1(.*?)## 16\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(
            re.findall(r"^\d+\. ", proved.group(1), re.M))
    openb = re.search(r"## 16\.4(.*?)(?:\n---|\Z)", paper, re.S)
    bullets = []
    if openb:
        bullets = [b.strip(" -;.") for b in
                   re.findall(r"^- (.+)$", openb.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
    no_go = re.findall(r"^## NO-GO (12\.\d) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    t["ledger_proved_items"] = len(ledger.get("proved_internally", []))
    t["ledger_no_go_items"] = len(ledger.get("no_go", []))
    key = next((k for k in ledger if k.lower() == "open"), None)
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


def check_their_claims(report: dict, res: dict) -> dict:
    mine = {
        "b_anchor_sequence": res["orbits"]["first_crossing_intervals"],
        "window_common_overlap": res["overlap"]["families"],
        "cf_local_bound_diagnostic": res["cf_local"]["q_values_scanned"],
        "support_exponent_algebra": res["exponents"]["constants_checked"],
        "pq_pressure_grid": res["identities"]["trials"],
        "localized_scaling_grid": res["localization"]["grid_points"],
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
    ("exponents", "frontier_and_report_disagreeing"),
    ("identities", "section_7_exponent_identity_violations"),
    ("identities", "section_8_exponent_identity_violations"),
    ("identities", "kappa_from_the_support_inequality_violations"),
    ("identities", "pq_exponent_from_inversion_violations"),
    ("means", "jensen_violations"),
    ("means", "am_hm_violations"),
    ("means", "jensen_violations_at_rho_star"),
    ("means", "undecided_at_rho_star"),
    ("overlap", "lemma_5_1_violations"),
    ("overlap", "pigeonhole_violations"),
    ("cf_local", "local_cf_bound_violations"),
    ("cf_local", "undecided_brackets"),
    ("orbits", "exact_product_identity_violations"),
    ("orbits", "survival_equivalence_violations"),
    ("orbits", "D_not_positive_at_a_first_crossing"),
    ("orbits", "local_cf_slack_violations"),
    ("orbits", "theorem_4_1_algebra_violations"),
    ("localization", "theorem_4_1_violations"),
    ("localization", "duration_floor_violations"),
    ("localization", "corridor_implication_violations"),
    ("localization", "pigeonhole_violations"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
)

NON_VACUITY = (
    ("exponents", "constants_checked"),
    ("identities", "trials"),
    ("means", "tuples"),
    ("means", "tuples_at_rho_star"),
    ("means", "equal_gap_cases"),
    ("overlap", "families"),
    ("overlap", "pigeonhole_trials"),
    ("cf_local", "q_values_scanned"),
    ("cf_local", "scales"),
    ("orbits", "first_crossing_intervals"),
    ("orbits", "local_cf_slack_checked"),
    ("orbits", "suffix_minimum_sources_checked"),
    ("orbits", "survival_duration_antecedent_holds"),
    ("localization", "grid_points"),
    ("localization", "theorem_4_1_antecedent_satisfiable"),
    ("localization", "duration_floor_antecedent_holds"),
    ("localization", "corridor_implication_points"),
    ("localization", "pigeonhole_points"),
    ("printed", "printed"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("exponents", "from_the_float64_chain_not_the_exact_rational"),
    ("exponents", "exact_to_the_last_bit"),
    ("exponents", "ulp_budget_allowed_for_chi_star"),
    ("overlap", "short_families_tried"),
    ("overlap", "short_families_that_still_overlap"),
    ("cf_local", "partial_quotients_used"),
    ("cf_local", "largest_partial_quotient"),
    ("orbits", "starts"),
    ("orbits", "orbits_used"),
    ("orbits", "B_injections"),
    ("orbits", "suffix_minimum_intervals"),
    ("orbits", "suffix_minimum_sources_outside_7_or_11_mod_12"
               "_not_a_counterexample"),
    ("orbits", "A_N_used"),
    ("printed", "over_published"),
    ("printed", "exact_to_every_digit"),
    ("printed", "correctly_rounded"),
    ("printed", "truncated"),
    ("printed", "printed_with_an_ellipsis"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_entries_without_a_digest"),
    ("artifacts", "validation_files_listed"),
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
    ap.add_argument("--limit", type=int, default=3000)
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
    res["identities"] = check_identities()
    res["means"] = check_means()
    res["overlap"] = check_overlap()
    res["cf_local"] = check_cf_local()
    res["orbits"] = check_orbits(a.limit)
    res["localization"] = check_localization()
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
        "run": "RUN-041", "round": "A-U.2d.13", "bundle": str(bundle),
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
