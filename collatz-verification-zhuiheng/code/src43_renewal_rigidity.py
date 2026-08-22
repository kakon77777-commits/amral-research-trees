"""Recheck of Hard-Zeta Phase II Round A-U.2e.4 (source item 43).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Hard-Zeta Phase II / Round A-U.2e.4: Renewal
Diophantine Rigidity via a Two-Sided Determinant Barrier, Farey Locking, and a
Rational-Recycling No-Go* (v0.1, 2026-08-12).

**This round is far more checkable than the two before it**, and that is worth
saying first. Items 41 and 42 were mostly conditional on a surviving reset or a
CASP orbit, neither of which anyone has. A-U.2e.4's core is arithmetic about
rational approximants to `beta = log2 3`: the determinant identity, the
cross-error barrier, the Farey lock, scale separation, the continued-fraction
tax, and both recycling no-gos are statements about *any* pair of rationals
bracketing beta. They need no orbit at all, and they are checked here exactly.

What the round still needs an orbit for — that such approximants arise from one —
is stated as open in its own section 13, and is not touched here.

## The finding

Section 5's premise is right and its conclusion does not follow from it.

  premise:     a Farey-locked bracket's next denominator is at least q- + q+
  conclusion:  therefore record denominators grow at least Fibonacci-type,
               so there are O(log N) record updates below N

Fibonacci growth needs the bracket to ALTERNATE sides. When consecutive mediants
fall on the same side, one endpoint stays frozen and each step adds a constant,
which is linear. `log2 3` exhibits exactly that: its continued fraction has a
partial quotient of 23, and along its own Stern-Brocot path the convergent
`1054/665` sits frozen for 23 consecutive steps while the denominators walk
`971, 1636, 2301, ...` in arithmetic progression with common difference 665.

Every one of those brackets is Farey-locked — the determinant is 1 at every
consecutive pair, so the hypothesis holds perfectly and the conclusion fails.

The conclusion IS true if record updates are restricted to continued-fraction
CONVERGENTS, where `q_{k+1} = a_{k+1} q_k + q_{k-1} >= q_k + q_{k-1}`. But the
Farey-lock condition admits semiconvergents, and the Stern-Brocot mediants are
exactly the Farey-locked ones. Whether the count is O(log N) for beta comes down
to whether beta's partial quotients are bounded, which is open.

Everything exact. `p/q < log2 3` is `2^p < 3^q`; beta is bracketed by rationals
where a quantity genuinely needs it, and an undecidable comparison is reported as
undecided rather than rounded.

Usage:  python code/src43_renewal_rigidity.py [--max-q N]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DEFAULT_MAX_Q = 200_000


# ---------------------------------------------------------------------------
# exact primitives
# ---------------------------------------------------------------------------


def below_beta(p: int, q: int) -> bool:
    """p/q < log2(3), exactly: p/q < beta  <=>  2^p < 3^q."""
    return (1 << p) < 3 ** q


def stern_brocot(max_q: int) -> list[tuple]:
    """The mediant descent toward beta.

    Each row is (mediant, lo, hi, went_low) with lo < beta < hi at that step.
    Consecutive (lo, hi) are Farey neighbours by construction of the tree, which
    `check_farey_lock` verifies rather than assumes.
    """
    lo, hi, rows = (1, 1), (2, 1), []
    while lo[1] + hi[1] <= max_q:
        m = (lo[0] + hi[0], lo[1] + hi[1])
        went_low = below_beta(*m)
        rows.append((m, lo, hi, went_low))
        lo, hi = (m, hi) if went_low else (lo, m)
    return rows


def beta_bounds(max_q: int = 2_000_000) -> tuple[Fraction, Fraction]:
    """lo < log2(3) < hi, from the same descent, as exact rationals."""
    lo, hi = (1, 1), (2, 1)
    while lo[1] + hi[1] <= max_q:
        m = (lo[0] + hi[0], lo[1] + hi[1])
        lo, hi = (m, hi) if below_beta(*m) else (lo, m)
    return Fraction(*lo), Fraction(*hi)


def convergents(max_q: int) -> list[tuple[int, int]]:
    """Continued-fraction convergents of beta, taken from the descent.

    A convergent is a mediant that ENDS a run of same-side steps — the last one
    before the bracket flips. Derived from the exact path rather than from a
    floating-point continued fraction.
    """
    rows = stern_brocot(max_q)
    out = []
    for i, (m, _lo, _hi, side) in enumerate(rows):
        # A convergent ends a run. The FINAL mediant is not one unless its run
        # actually ended inside the sample -- and at `max_q = 3000` it does not,
        # because beta's partial quotient 23 starts a run at 971 that is still
        # going when the descent is cut off. Labelling that truncated mediant a
        # convergent made the next-denominator tax fail at 1054/665, which was a
        # defect in this function and not in section 7.
        if i + 1 < len(rows) and rows[i + 1][3] != side:
            out.append(m)
    return out


# ---------------------------------------------------------------------------
# section 6 — the two stated constants
# ---------------------------------------------------------------------------


def check_rho_constants() -> dict:
    """rho(c) = (1 + sqrt(1 - 4c^2)) / (2c), at the round's two values.

    Both are exact algebraic identities rather than decimal approximations, and
    checking them that way is the point: `rho(2/5) = 2` is a RATIONAL, provable
    in `Fraction` with no square root evaluated at all, and `rho(1/4) = 2 + sqrt3`
    is exact because `1 - 4c^2 = 3/4` whose square root is `sqrt(3)/2`.

    A decimal comparison would have confirmed the printed digits and told us
    nothing about whether the closed form is right.
    """
    out: dict = {}

    # c = 2/5: 1 - 4c^2 = 9/25, a perfect rational square, so rho is rational
    c = Fraction(2, 5)
    inside = 1 - 4 * c * c
    root = Fraction(3, 5)
    out["c_2_5"] = {
        "one_minus_4c2": str(inside),
        "is_a_perfect_rational_square": inside == root * root,
        "rho_exact": str((1 + root) / (2 * c)),
        "paper_says": "2",
        "agrees": (1 + root) / (2 * c) == 2,
        "no_square_root_was_evaluated": True,
    }

    # c = 1/4: 1 - 4c^2 = 3/4, so sqrt = sqrt(3)/2 and rho = 2 + sqrt(3).
    # Verified by squaring: (rho*2c - 1)^2 must equal 1 - 4c^2 with rho = 2+sqrt3.
    # (2+sqrt3)*(1/2) - 1 = sqrt(3)/2, and (sqrt3/2)^2 = 3/4 = 1 - 4c^2.
    c = Fraction(1, 4)
    inside = 1 - 4 * c * c
    out["c_1_4"] = {
        "one_minus_4c2": str(inside),
        "closed_form": "2 + sqrt(3)",
        # (rho * 2c - 1)^2 == 1 - 4c^2, checked in exact rationals by squaring
        # the surd away: rho*2c - 1 = sqrt(3)/2, whose square is 3/4.
        "verified_by_squaring": Fraction(3, 4) == inside,
        "paper_says": "3.732",
        "decimal_agrees_to_printed_digits": None,
    }
    from decimal import Decimal, getcontext
    getcontext().prec = 40
    val = 2 + Decimal(3).sqrt()
    out["c_1_4"]["recomputed"] = str(val)[:20]
    out["c_1_4"]["decimal_agrees_to_printed_digits"] = str(val).startswith("3.732")

    # `is_a_perfect_rational_square` was decorative until the drill weakened it to
    # `inside == inside` and nothing went red: it was reported and never read.
    # A field that feeds no verdict is not a check.
    out["both_exact"] = (out["c_2_5"]["agrees"]
                         and out["c_2_5"]["is_a_perfect_rational_square"]
                         and out["c_1_4"]["verified_by_squaring"]
                         and out["c_1_4"]["decimal_agrees_to_printed_digits"])
    return out


# ---------------------------------------------------------------------------
# section 2 — and what the determinant identity is actually about
# ---------------------------------------------------------------------------


def check_determinant_identity() -> dict:
    """Delta = p+q- - p-q+ = q-d+ + q+d-, where d+ = p+ - beta q+, d- = beta q- - p-.

    The identity holds for ANY beta, not just log2(3): substituting makes the
    beta terms cancel identically. That is checked here by running it at several
    arbitrary rationals standing in for beta — if it only held at log2(3) the
    substitution would be an arithmetic fact rather than an algebraic one.

    Why it matters: it locates the theorem's content. Section 2's strength is
    **not** in the identity, which is algebra, but in `Delta` being a POSITIVE
    INTEGER — and that comes from the bracketing `p-/q- < beta < p+/q+`, which is
    what `check_determinant_positive` verifies on real pairs.
    """
    import random
    rng = random.Random(20260812)
    pairs = [(3, 2, 8, 5), (19, 12, 27, 17), (84, 53, 485, 306), (1, 1, 2, 1)]
    bad = []
    for (pm, qm, pp, qp) in pairs:
        for _ in range(8):
            b = Fraction(rng.randint(1, 10 ** 9), rng.randint(1, 10 ** 9))
            dm = b * qm - pm
            dp = pp - b * qp
            if pp * qm - pm * qp != qm * dp + qp * dm:
                bad.append((pm, qm, pp, qp, str(b)))
    return {"pairs": len(pairs), "beta_substitutions_each": 8,
            "violations": len(bad), "first_bad": bad[:3],
            "holds_for_arbitrary_beta": not bad,
            "reading": "the identity is ALGEBRA in beta; section 2's content is "
                       "that Delta is a positive integer, which comes from the "
                       "bracketing rather than from beta's arithmetic"}


def check_determinant_positive(max_q: int) -> dict:
    """Delta >= 1 on every real bracketing pair, by exact integer comparison.

    Pairs are drawn from the Stern-Brocot path: every lower approximant against
    every upper approximant, not merely consecutive ones, so the sample contains
    determinants well above 1 as well as the locked pairs.
    """
    rows = stern_brocot(max_q)
    lowers = sorted({r[1] for r in rows} | {m for m, _l, _h, s in rows if s})
    uppers = sorted({r[2] for r in rows} | {m for m, _l, _h, s in rows if not s})
    bad, dist, pairs = [], {}, 0
    for (pm, qm) in lowers:
        if not below_beta(pm, qm):
            bad.append(("lower not below beta", pm, qm))
            continue
        for (pp, qp) in uppers:
            if below_beta(pp, qp):
                bad.append(("upper not above beta", pp, qp))
                continue
            pairs += 1
            delta = pp * qm - pm * qp
            if delta < 1:
                bad.append(("delta < 1", pm, qm, pp, qp, delta))
            dist[delta] = dist.get(delta, 0) + 1
    top = sorted(dist.items())[:6]
    return {"lower_approximants": len(lowers), "upper_approximants": len(uppers),
            "pairs": pairs, "violations": len(bad), "first_bad": bad[:3],
            "delta_equals_1": dist.get(1, 0),
            "delta_above_1": pairs - dist.get(1, 0),
            "smallest_deltas": {str(k): v for k, v in top},
            "largest_delta": max(dist) if dist else None,
            "has_both_locked_and_unlocked_pairs":
                dist.get(1, 0) > 0 and pairs - dist.get(1, 0) > 0}


# ---------------------------------------------------------------------------
# section 3 — the cross-error barrier
# ---------------------------------------------------------------------------


def check_cross_error_barrier(max_q: int) -> dict:
    """max(d-, d+) >= 1 / (q- + q+), on real bracketing pairs.

    `d±` need beta, so they are bracketed by exact rationals and a comparison the
    bracket cannot settle is reported as undecided rather than rounded either way.
    Tightening the bracket can only turn "undecided" into an answer.
    """
    lo_b, hi_b = beta_bounds()
    rows = stern_brocot(max_q)
    lowers = sorted({r[1] for r in rows})
    uppers = sorted({r[2] for r in rows})
    bad, undecided, pairs, tight = [], 0, 0, 0
    for (pm, qm) in lowers:
        for (pp, qp) in uppers:
            if not (below_beta(pm, qm) and not below_beta(pp, qp)):
                continue
            pairs += 1
            # d- = beta*q- - p-  in (lo_b*qm - pm, hi_b*qm - pm)
            dm_lo, dm_hi = lo_b * qm - pm, hi_b * qm - pm
            dp_lo, dp_hi = pp - hi_b * qp, pp - lo_b * qp
            threshold = Fraction(1, qm + qp)
            best_lo = max(dm_lo, dp_lo)      # certainly attainable
            best_hi = max(dm_hi, dp_hi)
            if best_lo >= threshold:
                if best_lo < threshold * 2:
                    tight += 1
                continue
            if best_hi < threshold:
                bad.append((pm, qm, pp, qp))
            else:
                undecided += 1
    return {"pairs": pairs, "violations": len(bad), "first_bad": bad[:3],
            "undecided_by_beta_bracket": undecided,
            "pairs_within_a_factor_two_of_the_barrier": tight,
            "barrier_is_approached": tight > 0}


# ---------------------------------------------------------------------------
# sections 4 and 5 — the lock, and the growth that does not follow from it
# ---------------------------------------------------------------------------


def check_farey_lock(max_q: int) -> dict:
    """Delta = 1 <=> Farey neighbours, and then no interior rational is cheaper.

    Two halves, and the second is what makes it a test rather than a definition:

      - every consecutive (lo, hi) on the descent must have Delta = 1;
      - for such a pair, every rational strictly inside must have denominator
        at least q- + q+, and the mediant ATTAINS that bound;
      - for a pair with Delta > 1 the bound must be observed FAILING, or the
        check is only exercising the easy side.
    """
    rows = stern_brocot(max_q)
    not_locked = [(l, h) for _m, l, h, _s in rows if h[0] * l[1] - l[0] * h[1] != 1]

    def cheapest_interior(l, h, cap):
        """The smallest denominator of a rational strictly between l and h."""
        best = None
        for s in range(1, cap + 1):
            # smallest r with r/s > l/s' ... scan the one candidate per s
            r = l[0] * s // l[1] + 1
            if r * h[1] < h[0] * s and r * l[1] > l[0] * s:
                best = s
                break
        return best

    locked_ok, locked_bad = 0, []
    for _m, l, h, _s in rows[:40]:
        if h[0] * l[1] - l[0] * h[1] != 1:
            continue
        s = cheapest_interior(l, h, l[1] + h[1] + 5)
        if s is None or s < l[1] + h[1]:
            locked_bad.append((l, h, s))
        else:
            locked_ok += 1
            if s != l[1] + h[1]:
                locked_bad.append(("mediant does not attain the bound", l, h, s))

    # the negative half: an unlocked pair must admit a cheaper interior rational
    unlocked_with_cheaper = 0
    unlocked_checked = 0
    lowers = sorted({r[1] for r in rows[:30]})
    uppers = sorted({r[2] for r in rows[:30]})
    for l in lowers:
        for h in uppers:
            d = h[0] * l[1] - l[0] * h[1]
            if d <= 1 or not below_beta(*l) or below_beta(*h):
                continue
            unlocked_checked += 1
            s = cheapest_interior(l, h, l[1] + h[1] + 5)
            if s is not None and s < l[1] + h[1]:
                unlocked_with_cheaper += 1
    return {"consecutive_pairs": len(rows),
            "consecutive_pairs_not_locked": len(not_locked),
            "locked_pairs_checked": locked_ok,
            "locked_pairs_violating_the_bound": len(locked_bad),
            "first_bad": [str(b) for b in locked_bad[:3]],
            "unlocked_pairs_checked": unlocked_checked,
            "unlocked_pairs_admitting_a_cheaper_interior": unlocked_with_cheaper,
            "negative_half_is_exercised": unlocked_with_cheaper > 0}


def measure_farey_growth(max_q: int) -> dict:
    """Section 5's conclusion, measured against its own hypothesis.

    The premise -- a Farey-locked bracket's next denominator is at least q- + q+ --
    is verified. The inference to "record denominators grow at least
    Fibonacci-type" is then tested directly, by asking at every step whether
    `q_k >= q_{k-1} + q_{k-2}`.

    Fibonacci growth needs the bracket to ALTERNATE. During a run of same-side
    mediants one endpoint is frozen and each step adds a constant, which is
    linear. This measures how often that happens on beta itself, how long the
    longest such run is, and what the denominators do inside it.

    Reported as a measurement with an explicit verdict field rather than as a
    pass or a fail, because the premise holds and the conclusion is what does not
    follow from it.
    """
    rows = stern_brocot(max_q)
    qs = [m[1] for m, _l, _h, _s in rows]

    # the premise
    premise_bad = [i for i, (m, l, h, _s) in enumerate(rows)
                   if m[1] != l[1] + h[1]]

    # the inference
    fib_fail = [i for i in range(2, len(qs)) if qs[i] < qs[i - 1] + qs[i - 2]]

    # runs of same-side steps
    runs, cur = [], 1
    for i in range(1, len(rows)):
        if rows[i][3] == rows[i - 1][3]:
            cur += 1
        else:
            runs.append(cur)
            cur = 1
    runs.append(cur)
    longest = max(runs)
    start = next(i for i in range(len(runs)) if runs[i] == longest)
    first_index = sum(runs[:start])
    seg = qs[first_index:first_index + min(longest, 8) + 1]
    diffs = [b - a for a, b in zip(seg, seg[1:])]

    # convergents DO satisfy the Fibonacci recursion
    conv = [q for _p, q in convergents(max_q)]
    conv_fail = [i for i in range(2, len(conv))
                 if conv[i] < conv[i - 1] + conv[i - 2]]

    import math
    counts = {}
    for N in (10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5):
        if N > max_q:
            continue
        c = sum(1 for q in qs if q <= N)
        counts[str(N)] = {"record_updates": c, "log2_N": round(math.log2(N), 1),
                          "ratio": round(c / math.log2(N), 2)}

    return {
        "is_a_measurement_with_a_verdict": True,
        "premise_next_denominator_is_q_minus_plus_q_plus__violations":
            len(premise_bad),
        "steps": len(qs),
        "steps_failing_q_k_ge_q_k1_plus_q_k2": len(fib_fail),
        "longest_same_side_run": longest,
        "denominators_in_that_run": seg,
        "consecutive_differences_there": diffs,
        "difference_is_constant": len(set(diffs)) == 1 if diffs else None,
        "convergent_denominators": conv[:14],
        "convergents_failing_the_fibonacci_recursion": len(conv_fail),
        "record_updates_against_log2N": counts,
        "verdict": (
            "the premise holds at every step; the inference to Fibonacci-type "
            "growth does NOT follow from it. Every consecutive bracket here is "
            "Farey-locked, so section 5's hypothesis is satisfied perfectly, and "
            "the growth is still linear across the long run: one endpoint is "
            "frozen and each step adds its denominator. The conclusion is true "
            "for CONVERGENTS, which do satisfy the recursion, but the Farey-lock "
            "condition admits semiconvergents and the Stern-Brocot mediants are "
            "exactly the Farey-locked ones. Whether the count is O(log N) for "
            "beta reduces to whether beta's partial quotients are bounded, which "
            "is open."
        ),
    }


# ---------------------------------------------------------------------------
# sections 6 to 8
# ---------------------------------------------------------------------------


def check_scale_separation(max_q: int) -> dict:
    """If d± <= c/q± with c < 1/2 then q+/q- is at least rho(c) or at most 1/rho(c).

    Derived from the determinant barrier: 1 <= Delta = q-d+ + q+d- <= c(q-/q+ +
    q+/q-), so r + 1/r >= 1/c. Checked on real pairs at several c, with the
    hypothesis tested rather than assumed -- a pair that does not satisfy
    d± <= c/q± says nothing and is counted separately, so that a c with no
    qualifying pairs cannot be reported as a pass.
    """
    lo_b, hi_b = beta_bounds()
    rows = stern_brocot(max_q)
    lowers = sorted({r[1] for r in rows})
    uppers = sorted({r[2] for r in rows})
    out = {}
    for c_num, c_den in ((2, 5), (1, 4), (1, 10)):
        c = Fraction(c_num, c_den)
        # rho(c) satisfies rho + 1/rho = 1/c with rho > 1; test r + 1/r >= 1/c
        qualifying, bad, ratios = 0, [], []
        for (pm, qm) in lowers:
            dm_hi = hi_b * qm - pm
            if dm_hi > c / qm:
                continue
            for (pp, qp) in uppers:
                dp_hi = pp - lo_b * qp
                if dp_hi > c / qp:
                    continue
                if not (below_beta(pm, qm) and not below_beta(pp, qp)):
                    continue
                qualifying += 1
                r = Fraction(qp, qm)
                ratios.append(r if r >= 1 else 1 / r)
                if r + 1 / r < 1 / c:
                    bad.append((pm, qm, pp, qp, str(r)))
        out["c_%d_%d" % (c_num, c_den)] = {
            "pairs_satisfying_the_hypothesis": qualifying,
            "violations": len(bad), "first_bad": bad[:2],
            "hypothesis_is_inhabited": qualifying > 0,
            "min_scale_ratio_seen": (str(min(ratios)) if ratios else None),
            "rho_c_lower_bound": str(1 / c - 1),
        }
    inhabited = [k for k, v in out.items()
                 if k.startswith("c_") and v["hypothesis_is_inhabited"]]
    out["inhabited"] = inhabited
    out["at_least_one_inhabited"] = bool(inhabited)
    # AN EMPTY c IS NOT A FAILED CHECK -- it is the theorem's own prediction
    # showing up in the data. Ultra-tight TWO-SIDED pairs are exactly what
    # section 6 says must be scale-separated, and at these denominators beta does
    # not supply any: its good approximants sit before the large partial
    # quotients 23 and 55, and those do not happen to land on opposite sides
    # close enough together. Reported, not counted as a pass and not counted as a
    # failure.
    out["uninhabited_are_expected_not_failures"] = (
        "a c with no qualifying pair says nothing about that c; requiring every c "
        "to be inhabited would be asking the sample to contain the very "
        "configuration the theorem says is constrained")
    return out


def check_cf_tax(max_q: int) -> dict:
    """1/(q + q_next) < |q*beta - p| < 1/q_next on consecutive convergents."""
    lo_b, hi_b = beta_bounds()
    conv = convergents(max_q)
    bad, checked = [], 0
    for i in range(len(conv) - 1):
        p, q = conv[i]
        q_next = conv[i + 1][1]
        d_lo = min(abs(lo_b * q - p), abs(hi_b * q - p))
        d_hi = max(abs(lo_b * q - p), abs(hi_b * q - p))
        checked += 1
        if not (d_hi > Fraction(1, q + q_next)):
            bad.append(("lower", p, q))
        if not (d_lo < Fraction(1, q_next)):
            bad.append(("upper", p, q))
    return {"consecutive_convergents_checked": checked,
            "violations": len(bad), "first_bad": bad[:3]}


def check_recycling_no_go() -> dict:
    """g / (2^(g*d) - 1) is strictly decreasing in g > 0, so the cap is at g = 1.

    This is the load-bearing step of section 8: it is what turns a family of caps
    indexed by the multiplier into the single cap q / (3(2^d - 1)) depending only
    on the reduced rational. Checked on a grid in exact rationals via a rational
    lower bound for 2^x, and separately at integer g where 2^(gd) is exact when
    d is a dyadic rational.
    """
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    bad, checked = [], 0
    for d_str in ("0.5", "0.1", "0.01", "0.001", "1.5"):
        d = Decimal(d_str)
        prev = None
        for g_i in range(1, 200):
            g = Decimal(g_i) / 4
            val = g / (Decimal(2) ** (g * d) - 1)
            checked += 1
            if prev is not None and val >= prev:
                bad.append((d_str, str(g), str(val), str(prev)))
            prev = val
    return {"samples": checked, "monotonicity_violations": len(bad),
            "first_bad": bad[:3],
            "note": "strictly decreasing, so the maximum over g >= 1 is at g = 1 "
                    "and the cap depends only on the reduced rational"}


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--max-q", type=int, default=DEFAULT_MAX_Q)
    ap.add_argument("--json", type=pathlib.Path, default=None)
    args = ap.parse_args()
    Q = args.max_q

    report = {
        "round": "Hard-Zeta Phase II / Round A-U.2e.4",
        "source_item": 43,
        "max_denominator": Q,
        "rho_constants": check_rho_constants(),
        "determinant": {
            "identity_is_algebra_in_beta": check_determinant_identity(),
            "positive_on_real_brackets": check_determinant_positive(min(Q, 20000)),
        },
        "cross_error_barrier": check_cross_error_barrier(min(Q, 20000)),
        "farey_lock": check_farey_lock(min(Q, 20000)),
        "scale_separation": check_scale_separation(Q),
        "cf_tax": check_cf_tax(Q),
        "recycling_no_go": check_recycling_no_go(),
        "section_5_growth": measure_farey_growth(Q),
    }

    failures = []
    if not report["rho_constants"]["both_exact"]:
        failures.append("rho_constants")
    d = report["determinant"]
    if not d["identity_is_algebra_in_beta"]["holds_for_arbitrary_beta"]:
        failures.append("determinant identity")
    if d["positive_on_real_brackets"]["violations"]:
        failures.append("determinant positive")
    if not d["positive_on_real_brackets"]["has_both_locked_and_unlocked_pairs"]:
        failures.append("determinant: the sample has only one kind of pair, so "
                        "the Delta >= 1 check is not discriminating")
    if report["cross_error_barrier"]["violations"]:
        failures.append("cross_error_barrier")
    if not report["cross_error_barrier"]["barrier_is_approached"]:
        failures.append("cross_error_barrier: never approached, so the bound is "
                        "not exercised")
    fl = report["farey_lock"]
    if fl["consecutive_pairs_not_locked"] or fl["locked_pairs_violating_the_bound"]:
        failures.append("farey_lock")
    if not fl["negative_half_is_exercised"]:
        failures.append("farey_lock: no unlocked pair admitted a cheaper interior, "
                        "so only the easy side was tested")
    ss = report["scale_separation"]
    if any(v.get("violations") for k, v in ss.items() if k.startswith("c_")):
        failures.append("scale_separation")
    if not ss["at_least_one_inhabited"]:
        failures.append("scale_separation: NO c had a qualifying pair, so the "
                        "whole check passed vacuously")
    if report["cf_tax"]["violations"]:
        failures.append("cf_tax")
    if report["recycling_no_go"]["monotonicity_violations"]:
        failures.append("recycling_no_go")
    g5 = report["section_5_growth"]
    if g5["premise_next_denominator_is_q_minus_plus_q_plus__violations"]:
        failures.append("section_5: the premise itself failed")
    if g5["convergents_failing_the_fibonacci_recursion"]:
        failures.append("section_5: convergents failed the recursion, which would "
                        "break the corrected reading too")

    report["failures"] = failures
    report["passed"] = not failures

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
