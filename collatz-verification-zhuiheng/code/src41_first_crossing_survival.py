"""Recheck of Hard-Zeta Phase II Round A-U.2e.2 (source item 41).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Hard-Zeta Phase II / Round A-U.2e.2: First-Crossing
Correction Caps, a Diophantine Survival Gate, and A/B Atomic Multiplication*
(v0.1, 2026-08-12).

The round proves a chain of inequalities about a **local first coefficient
crossing** — the first accelerated block on which the coefficient skeleton turns
from expanding to contracting — and then about those crossings that **survive**,
meaning the coefficient crossed but the actual value did not descend.

Splitting the round in two is most of this run's work, because the two halves
have completely different evidential status:

  UNCONDITIONAL, and checkable on real orbits:
    - First-Crossing Correction Bound       B_L <= L*3^(L-1)
    - First-Crossing Reset Inequality       Y_{a+L} <= 2^-D (Y_a + L/3)
    - Universal First-Crossing Correction Cap, and its equivalence
      Y_a <= c_fc  <=>  Y_{a+L} >= Y_a

  CONDITIONAL on a surviving crossing existing:
    - First-Crossing Survival Cost          L >= 3(2^D - 1) Y_a
    - Duration-Diophantine Dichotomy
    - Polynomial Survival-Time Corollary

**A surviving first crossing is a counterexample to the Terras coefficient-
stopping conjecture.** So the second group is not merely unverified here — it is
about a set this run measures to be EMPTY, and reporting "all conditional bounds
hold" over an empty set would be the emptiest kind of pass. That count is
reported first, as a number, before any of those bounds is mentioned.

What is NOT empty, and is the real measurement in this file: how close a genuine
orbit comes to the correction cap, and where those near misses sit arithmetically.
The round argues that a surviving crossing must either last a long time or have
Q_L/L land on an exceptional Diophantine approximation to log2(3). That mechanism
leaves a trace **below** the survival threshold, and it is measured here against a
control — because "the top ten contain 8/5" means nothing until you know what
share of ordinary crossings contain it too.

Everything is exact. `Q_L > beta*L` is evaluated as `2^Q_L > 3^L`, `2^D` as the
rational `2^Q_L / 3^L`, and `p/q < log2 3` as `2^p < 3^q`. No logarithm is
evaluated anywhere in the decision path; a float check here would be a check of
the float library.

Usage:  python code/src41_first_crossing_survival.py [--limit N]
Env:    COLLATZ_TREE_ROOT  (defaults to this tree)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DEFAULT_LIMIT = 200_001          # odd starts 3, 5, ..., LIMIT-1

# ---------------------------------------------------------------------------
# exact primitives
# ---------------------------------------------------------------------------


def below_beta(p: int, q: int) -> bool:
    """p/q < log2(3), exactly.

    p/q < log2 3  <=>  p < q*log2 3  <=>  2^p < 3^q.
    """
    return (1 << p) < 3 ** q


def best_approximation_set(max_q: int) -> set[Fraction]:
    """Every best rational approximation to log2(3) with denominator <= max_q.

    The Stern-Brocot path to an irrational consists exactly of its continued-
    fraction convergents and the intermediate fractions (semiconvergents) between
    them — the set Niu's observation is about. Built by mediant descent with the
    exact comparison above, so no continued fraction is ever computed from a
    floating-point value.

    Cross-checked in `check_best_approximations` against the classical equal
    temperaments 19/12, 65/41 and 84/53, which are these convergents under a
    different name and were written down for unrelated reasons.
    """
    lo, hi, out = (1, 1), (2, 1), set()
    while True:
        m = (lo[0] + hi[0], lo[1] + hi[1])
        if m[1] > max_q:
            return out
        out.add(Fraction(*m))
        lo, hi = (m, hi) if below_beta(*m) else (lo, m)


def beta_bounds(max_q: int = 2_000_000) -> tuple[Fraction, Fraction]:
    """lo < log2(3) < hi, from the same mediant descent, with exact comparisons.

    Used wherever a quantity involving beta must be DECIDED but the exact integer
    form (`2^(2*L*Q)` against `2*3^(2*L*L)`) would build a multi-megabit integer.
    A comparison the bracket cannot settle is reported as undecided rather than
    rounded, so tightening the bracket can only turn "undecided" into an answer
    and never turn one answer into the other.
    """
    lo, hi = (1, 1), (2, 1)
    while True:
        m = (lo[0] + hi[0], lo[1] + hi[1])
        if m[1] > max_q:
            return Fraction(*lo), Fraction(*hi)
        lo, hi = (m, hi) if below_beta(*m) else (lo, m)


def first_crossing(y0: int, cap: int = 20_000):
    """The local first coefficient crossing from odd `y0`.

    Walks the accelerated odd map S(y) = (3y+1)/2^v2(3y+1), accumulating

        Q_j = sum of valuations,   B_j = 3*B_{j-1} + 2^{Q_{j-1}},  B_0 = 0,

    and stops at the first L with 2^{Q_L} > 3^L. Because log2(3) is irrational,
    Q_j is never exactly beta*j, so that first L automatically has every proper
    prefix expanding — the round's hypothesis is satisfied by construction rather
    than by an extra test, and this note is here so that absence is not read as a
    missing check.

    Returns (L, Q_L, B_L, Y_{a+L}, 3^L) or None if `cap` blocks are exhausted.
    """
    if y0 % 2 == 0 or y0 < 3:
        raise ValueError("first_crossing needs an odd start >= 3, got %r" % y0)
    y, Q, B, L, p3 = y0, 0, 0, 0, 1
    while L < cap:
        L += 1
        t = 3 * y + 1
        v = (t & -t).bit_length() - 1
        B = 3 * B + (1 << Q)
        Q += v
        p3 *= 3
        y = t >> v
        if (1 << Q) > p3:
            return L, Q, B, y, p3
    return None


# ---------------------------------------------------------------------------
# §0  the round's numerical constant
# ---------------------------------------------------------------------------


def check_constant() -> dict:
    """sqrt(3*ln2/2), the constant in the Duration-Diophantine Dichotomy.

    The paper prints 1.019666990169... . Recomputed here rather than copied, and
    bracketed by exact rationals so the digits rest on an enclosure rather than on
    one library's rounding: with 2^(-1/2) < ln2 < 0.6931472,

        sqrt(3*ln2/2) in (sqrt(3*lo/2), sqrt(3*hi/2)).
    """
    from decimal import Decimal, getcontext

    getcontext().prec = 50
    # ln 2 to 40 correct digits, bracketed
    lo = Decimal("0.6931471805599453094172321214581765680754")
    hi = Decimal("0.6931471805599453094172321214581765680756")
    val_lo = (Decimal(3) * lo / 2).sqrt()
    val_hi = (Decimal(3) * hi / 2).sqrt()
    printed = Decimal("1.019666990169")
    # The paper prints twelve decimals followed by "...", so the test is whether
    # the true value ROUNDS to what is printed -- not whether it starts with it.
    # A prefix match would call the paper wrong for correctly rounding
    # 1.0196669901688... up to 1.019666990169, which is a defect in the checker
    # rather than in the round.
    unit = Decimal(1).scaleb(-12)
    rounds_to = (abs(val_lo - printed) <= unit / 2) and (abs(val_hi - printed) <= unit / 2)
    return {
        "paper_prints": str(printed),
        "enclosure_low": str(val_lo)[:22],
        "enclosure_high": str(val_hi)[:22],
        "enclosure_is_tight_to_20_digits": str(val_lo)[:22] == str(val_hi)[:22],
        "printed_digits_agree": rounds_to,
        "comparison": "true value rounds to the printed 12 decimals",
        "recomputed_15_digits": str(val_lo)[:17],
    }


def check_best_approximations() -> dict:
    """The approximation set, cross-checked against numbers found for other reasons.

    19/12, 65/41 and 84/53 are the equal temperaments of Western music theory,
    written down centuries before anyone asked about Collatz. If the mediant
    descent implemented here is right, they must appear; if it is subtly wrong,
    they are the kind of thing that would go missing. This is a second method
    meeting the first on the same objects.
    """
    approx = best_approximation_set(400)
    classical = {
        "3/2": Fraction(3, 2),
        "8/5": Fraction(8, 5),
        "19/12 (12-tone)": Fraction(19, 12),
        "65/41 (41-tone)": Fraction(65, 41),
        "84/53 (53-tone)": Fraction(84, 53),
    }
    present = {name: (f in approx) for name, f in classical.items()}
    # and a NEGATIVE control: a fraction near log2 3 that must NOT be a best
    # approximation, or the set is simply everything
    # A negative control must not reduce to a member: 22/14 does NOT work, because
    # Fraction(22,14) IS 11/7 and 11/7 is on the path. Each of these is checked in
    # lowest terms and verified to be a genuine non-member.
    negatives = {
        "17/11": Fraction(17, 11) not in approx,
        "50/31": Fraction(50, 31) not in approx,
        "13/8": Fraction(13, 8) not in approx,
        "1000/631": Fraction(1000, 631) not in approx,
    }
    return {
        "size_q_le_400": len(approx),
        "classical_all_present": all(present.values()),
        "classical": present,
        "non_members_rejected": all(negatives.values()),
        "negative_control": negatives,
    }


# ---------------------------------------------------------------------------
# §1  the sweep
# ---------------------------------------------------------------------------


def sweep(limit: int) -> list[tuple]:
    """(cap_ratio, n, L, Q, B, Y_end, 3^L) for every odd start below `limit`."""
    rows = []
    for n in range(3, limit, 2):
        got = first_crossing(n)
        if got is None:                                # pragma: no cover
            raise RuntimeError("no first crossing within the cap for n=%d" % n)
        L, Q, B, y_end, p3 = got
        # c_fc = B_L / (2^Q_L - 3^L); the denominator is positive by construction
        cap_ratio = Fraction(B, ((1 << Q) - p3) * n)
        rows.append((cap_ratio, n, L, Q, B, y_end, p3))
    return rows


# ---------------------------------------------------------------------------
# §2  unconditional claims, on real orbits
# ---------------------------------------------------------------------------


def check_closed_form(rows: list[tuple]) -> dict:
    """TRANSCRIPTION CHECK, labelled as one.

    Y_{a+L} * 2^Q_L == 3^L * Y_a + B_L is the closed form this file's own walk was
    written from. Confirming it tests the transcription and nothing about the
    round. It is here because a silent transcription error would make every
    inequality below meaningless, and NOT here as evidence for the paper.
    """
    bad = [n for _, n, L, Q, B, y_end, p3 in rows if y_end * (1 << Q) != p3 * n + B]
    return {"is_a_transcription_check_not_a_result": True,
            "checked": len(rows), "violations": len(bad), "first_bad": bad[:3]}


def check_correction_bound(rows: list[tuple]) -> dict:
    """First-Crossing Correction Bound: B_L <= L * 3^(L-1).

    Real content, not a rearrangement: it needs every proper prefix to satisfy
    2^{Q_{i-1}} < 3^{i-1}, which is the first-crossing hypothesis.

    The tightness ratio is reported because a bound that is never within orders of
    magnitude of its subject constrains nothing downstream, and the Survival Cost
    is derived through this one.
    """
    worst, worst_big, bad, degenerate = Fraction(0), Fraction(0), [], []
    for _, n, L, Q, B, _y, p3 in rows:
        limit = L * (p3 // 3)
        if B > limit:
            bad.append(n)
        if limit <= 0:
            # Found by the drill: a wrong power made `limit` zero at L=1 and the
            # ratio below raised ZeroDivisionError, so the run died instead of
            # reporting the violation it had just recorded. A check that crashes
            # is not a check that failed -- the caller sees no verdict at all.
            degenerate.append(n)
            continue
        r = Fraction(B, limit)
        worst = max(worst, r)
        if L >= 2:
            worst_big = max(worst_big, r)
    return {"checked": len(rows), "violations": len(bad), "first_bad": bad[:3],
            "degenerate_bound": len(degenerate),
            # At L = 1 the bound reads B_1 <= 1*3^0 = 1 and B_1 IS 1, so the ratio
            # is exactly 1 for half the population and a maximum taken over all L
            # reports the tightness of the trivial case and nothing else. The
            # L >= 2 figure is the one that says whether the bound constrains
            # anything -- the Survival Cost is derived through it.
            "max_B_over_bound_all_L": float(worst),
            "max_B_over_bound_L_ge_2": float(worst_big),
            "note": "the all-L figure is saturated by L=1, where B_1 = 1 = 1*3^0"}


def check_reset_inequality(rows: list[tuple]) -> dict:
    """First-Crossing Reset Inequality: Y_{a+L} <= 2^-D (Y_a + L/3).

    Cleared of denominators so it is an integer comparison:
    3 * Y_{a+L} * 2^Q_L <= 3^L * (3*Y_a + L).
    """
    bad, worst, identity_broken = [], None, []
    for _, n, L, Q, B, y_end, p3 in rows:
        lhs = 3 * y_end * (1 << Q)
        rhs = p3 * (3 * n + L)
        if lhs > rhs:
            bad.append(n)
        # A RATIO IS THE WRONG INSTRUMENT HERE. lhs/rhs tends to 1 as Y_a grows for
        # any B whatsoever, so its maximum over a sample reports the largest start
        # in the sample and nothing about the bound. The slack is what carries the
        # content, and the slack turns out to be an identity:
        #
        #   rhs - lhs = 3^L(3 Y_a + L) - 3(3^L Y_a + B) = L*3^L - 3B
        #             = 3 * (L*3^(L-1) - B),
        #
        # the Y_a terms cancelling exactly. So the reset inequality's slack IS
        # three times the correction bound's slack, at every crossing, and the
        # reset inequality says nothing about Y_a at all. That identity is
        # asserted rather than the ratio measured -- and it is the same fact z3
        # confirms independently over a declared box in felra/au2e2.
        if rhs - lhs != 3 * (L * (p3 // 3) - B):
            identity_broken.append(n)
        slack = rhs - lhs
        worst = min(worst, slack) if worst is not None else slack
    return {"checked": len(rows), "violations": len(bad), "first_bad": bad[:3],
            "slack_identity_violations": len(identity_broken),
            "first_identity_break": identity_broken[:3],
            "min_slack": str(worst),
            "identity": "rhs - lhs == 3*(L*3^(L-1) - B), so the reset inequality "
                        "is the correction bound restated and carries no "
                        "information about Y_a"}


def check_cap_equivalence(rows: list[tuple]) -> dict:
    """Y_a <= c_fc  <=>  Y_{a+L} >= Y_a, checked in BOTH directions.

    One direction alone would be satisfied by a rule that never fires. The paper
    states the cap as a necessary condition on a correction-delay starting value;
    it is in fact an equivalence, and both halves are asserted here so that a
    change making the cap trivially true or trivially false shows up.
    """
    mismatches, cap_holds, survives = [], 0, 0
    for ratio, n, L, Q, B, y_end, p3 in rows:
        by_cap = ratio >= 1                       # Y_a <= c_fc
        by_orbit = y_end >= n                     # no actual descent
        cap_holds += by_cap
        survives += by_orbit
        if by_cap != by_orbit:
            mismatches.append(n)
    return {"checked": len(rows), "mismatches": len(mismatches),
            "first_mismatch": mismatches[:3],
            "cap_satisfied_count": cap_holds, "survivor_count": survives,
            # WITH BOTH COUNTS AT ZERO THIS CHECK IS VACUOUS. Every real start has
            # by_cap = by_orbit = False, so the comparison never distinguishes
            # anything and would pass just as happily if the cap were computed
            # wrongly. It is reported rather than deleted because "no real start
            # reaches the cap" is itself the finding; the equivalence gets its
            # true branch from `check_cap_equivalence_branches` below.
            "is_vacuous_here": cap_holds == 0 and survives == 0,
            "true_branch_tested_in": "check_cap_equivalence_branches"}


def check_cap_threshold_on_real_rows(rows: list[tuple]) -> dict:
    """The correction cap, tested at its own threshold on every real crossing.

    `check_cap_equivalence` compares "is the cap met" against "did it fail to
    descend", and on real orbits both are False at every start -- so it passes
    however the cap is computed. The drill proved that: corrupting the cap's
    denominator left the whole run green.

    This check does not ask whether a real start meets the cap. It takes each real
    crossing's own (L, Q_L, B_L) and probes the cap AT its threshold, from both
    sides:

        y* = floor(c_fc)   must not descend      3^L y* + B >= 2^Q y*
        y* + 1             must descend          3^L z  + B <  2^Q z

    Both sides are exercised at every row regardless of where the real start sits,
    so a wrong denominator moves the threshold and one of the two fails. The
    starts probed are not the orbit's own start and are not claimed to be
    reachable -- this is a test of the cap formula, not of the Collatz map.
    """
    below_fail, above_fail = [], []
    for ratio, n, L, Q, B, _y, p3 in rows:
        denom = (1 << Q) - p3
        if denom <= 0:                                     # pragma: no cover
            below_fail.append((n, L, Q))
            continue
        y_star = B // denom
        if y_star >= 1 and not (p3 * y_star + B) >= y_star * (1 << Q):
            below_fail.append((n, L, Q, y_star))
        z = y_star + 1
        if not (p3 * z + B) < z * (1 << Q):
            above_fail.append((n, L, Q, z))
    return {"checked": len(rows),
            "at_threshold_should_not_descend__failures": len(below_fail),
            "just_above_threshold_should_descend__failures": len(above_fail),
            "below_examples": below_fail[:3], "above_examples": above_fail[:3],
            "note": "probes each real crossing's cap from both sides, so this one "
                    "is not vacuous even though no real start reaches the cap"}


def check_cap_equivalence_branches(triples: list[tuple]) -> dict:
    """Y_a <= c_fc <=> Y_{a+L} >= Y_a, with BOTH branches actually exercised.

    On real orbits the cap is never reached, so the equivalence above is tested
    only on its false side. Here each synthetic configuration is used twice: once
    with the largest integer AT OR BELOW the cap, which must give no descent, and
    once with that integer PLUS ONE, which must give descent. A rule that always
    answered "no descent", or always "descent", fails one of the two.
    """
    below_fail, above_fail = [], []
    for y, L, Q, B in triples:
        p3 = 3 ** L
        # y <= c_fc  =>  Y_end >= y
        if not (p3 * y + B) >= y * (1 << Q):
            below_fail.append((y, L, Q))
        # y+1 > c_fc  =>  Y_end < y+1
        z = y + 1
        if not (p3 * z + B) < z * (1 << Q):
            above_fail.append((z, L, Q))
    return {"is_algebra_not_orbit_data": True,
            "configurations": len(triples),
            "at_or_below_cap_should_not_descend__failures": len(below_fail),
            "just_above_cap_should_descend__failures": len(above_fail),
            "below_examples": below_fail[:3], "above_examples": above_fail[:3]}


# ---------------------------------------------------------------------------
# §3  the non-vacuity report, before any conditional bound is mentioned
# ---------------------------------------------------------------------------


def survival_census(rows: list[tuple]) -> dict:
    """How many real first crossings SURVIVE, and how close the rest come.

    A survivor satisfies Y_{a+L} >= Y_a: the coefficient skeleton turned
    contracting and the value still did not fall. That is exactly a counterexample
    to the Terras coefficient-stopping conjecture, so a nonzero count here would be
    a far larger event than a verification note. A zero count is the expected
    outcome, and it is the reason every bound in §4 is checked as algebra rather
    than on orbits.

    `max_cap_ratio` is the measurement that is NOT vacuous: the largest
    c_fc / Y_a attained, where survival needs >= 1.
    """
    survivors = [n for _, n, _L, _Q, _B, y_end, _p in rows if y_end >= n]
    top = sorted(rows, key=lambda r: r[0], reverse=True)[:10]
    return {
        "starts_walked": len(rows),
        "survivors": len(survivors),
        "survivor_starts": survivors[:20],
        "a_survivor_would_refute": "Terras coefficient-stopping conjecture",
        "max_cap_ratio": float(top[0][0]),
        "max_cap_ratio_exact": str(top[0][0]),
        "max_cap_ratio_at_n": top[0][1],
        "survival_threshold": 1.0,
        "nearest_ten": [
            {"n": n, "L": L, "Q": Q, "Q_over_L": str(Fraction(Q, L)),
             "cap_ratio": round(float(r), 6), "Y_end_over_Y_a": round(y / n, 6)}
            for r, n, L, Q, _B, y, _p in top
        ],
    }


# ---------------------------------------------------------------------------
# §4  the conditional theorems, checked as ALGEBRA
# ---------------------------------------------------------------------------


def synthetic_survivors(max_L: int = 60) -> list[tuple]:
    """Triples (Y_a, L, Q, B) satisfying the round's hypotheses, built by hand.

    Real orbits produce no survivors (§3), so the conditional theorems cannot be
    tested on orbit data at all. They can still be tested as arithmetic: build a
    valuation word whose partial sums stay under beta*j and cross at j = L, take
    the B it determines, and pick a positive integer Y_a at or below the cap.

    This tests the round's ALGEBRA and says nothing about whether such a
    configuration is reachable by the Collatz map — which is the whole open
    question. Labelled accordingly in the output so the two are never read as one.
    """
    out = []
    for L in range(2, max_L + 1):
        # Q_L is the smallest integer strictly above beta*L
        Q = 0
        while (1 << Q) <= 3 ** L:
            Q += 1
        # a word with the prefix property: put the valuation mass as late as
        # possible, which also maximises B and hence the cap
        Qs, run = [0], 0
        ok = True
        for j in range(1, L + 1):
            step = 1
            while j < L and (1 << (run + step)) >= 3 ** j:
                step -= 1
                if step == 0:
                    break
            run += step if j < L else Q - run
            if j < L and (1 << run) >= 3 ** j:
                ok = False
                break
            Qs.append(run)
        if not ok or Qs[-1] != Q:
            continue
        B = sum(3 ** (L - i) * (1 << Qs[i - 1]) for i in range(1, L + 1))
        cap = Fraction(B, (1 << Q) - 3 ** L)
        y = int(cap)                       # the largest integer at or below c_fc
        if y >= 2:
            out.append((y, L, Q, B))
    return out


def check_survival_cost(triples: list[tuple]) -> dict:
    """First-Crossing Survival Cost: L >= 3(2^D - 1) Y_a, cleared of denominators.

    2^D = 2^Q / 3^L, so 3(2^D - 1) Y_a <= L becomes the integer comparison
        3 * (2^Q - 3^L) * Y_a <= L * 3^L.
    The equivalent form D <= log2(1 + L/(3 Y_a)) becomes
        3 * Y_a * 2^Q <= 3^L * (3*Y_a + L),
    and both are asserted, because the paper derives one from the other and a
    transcription slip between them would otherwise pass.
    """
    bad_a, bad_b = [], []
    for y, L, Q, B in triples:
        p3 = 3 ** L
        if not 3 * ((1 << Q) - p3) * y <= L * p3:
            bad_a.append(y)
        if not 3 * y * (1 << Q) <= p3 * (3 * y + L):
            bad_b.append(y)
    return {"is_algebra_not_orbit_data": True,
            "triples": len(triples),
            "violations_cost_form": len(bad_a),
            "violations_log_form": len(bad_b)}


def check_legendre_gate(triples: list[tuple]) -> dict:
    """Duration-Diophantine Dichotomy, and WHY its two branches never both fail.

    The round states the dichotomy as an either/or: a surviving crossing has
    either L >= sqrt(3*ln2/2 * Y_a) or Q_L/L a continued-fraction convergent of
    log2(3). Checking that no configuration fails both is a weak test if one
    branch happens to hold everywhere -- and it does. The reason is worth stating,
    because it makes the dichotomy sharper than an either/or:

        the correction cap gives    Y_a <= L / (3(2^D - 1)),
        and                          2^D - 1 >= D*ln2,
        so if D >= 1/(2L)  then      Y_a <= L / (3*ln2/(2L)) = 2L^2/(3*ln2),

    which IS the duration branch. So the duration branch is IMPLIED BY THE CAP
    whenever D >= 1/(2L); and when D < 1/(2L), Legendre's criterion gives the
    convergent branch directly. The two branches are not independent alternatives
    a configuration must choose between -- they are the two sides of a partition
    on D against 1/(2L), and neither can fail on its own side.

    That is what is asserted here: the partition is exhaustive, and each side
    delivers its own branch. `satisfy_neither` is still reported, but the
    load-bearing assertions are the two implications.
    """
    LN2_LO = Fraction(6931471805599453, 10 ** 16)
    LN2_HI = Fraction(6931471805599454, 10 ** 16)
    lo, hi = beta_bounds()

    small_D, large_D, undecided = 0, 0, []
    duration_missing_on_large_D, neither = [], []
    for y, L, Q, B in triples:
        # D = Q - beta*L, bracketed
        d_lo, d_hi = Q - hi * L, Q - lo * L
        thresh = Fraction(1, 2 * L)
        if d_hi < thresh:
            legendre_side = True
        elif d_lo >= thresh:
            legendre_side = False
        else:
            undecided.append((y, L, Q))
            continue

        duration = 2 * L * L >= 3 * LN2_HI * y
        if legendre_side:
            small_D += 1
        else:
            large_D += 1
            # the implication this section exists to test
            if not duration:
                duration_missing_on_large_D.append((y, L, Q))
        if not duration and not legendre_side:
            neither.append((y, L, Q))

    return {"is_algebra_not_orbit_data": True,
            "configurations": len(triples),
            "D_below_half_over_L__legendre_side": small_D,
            "D_at_or_above_half_over_L__duration_side": large_D,
            "duration_branch_failed_on_the_duration_side": len(duration_missing_on_large_D),
            "counterexamples": duration_missing_on_large_D[:3],
            "satisfy_neither": len(neither),
            "undecided_by_beta_bracket": len(undecided),
            "structure": "the cap forces the duration branch whenever D >= 1/(2L), "
                         "so the dichotomy is a partition on D against 1/(2L) "
                         "rather than a choice between independent alternatives"}


def measure_legendre_distance(rows: list[tuple]) -> dict:
    """How close do REAL first crossings come to the Legendre regime D < 1/(2L)?

    The partition above is about hypothetical survivors. This is the same quantity
    on orbits that exist: 2*L*D, which is below 1 exactly when Q_L/L is forced to
    be a convergent. It is a measurement rather than a check -- there is no claim
    here to pass or fail -- and it is reported because a dichotomy whose
    Diophantine side is never approached by anything real is worth knowing about.
    """
    lo, hi = beta_bounds()
    vals = []
    for _r, n, L, Q, _B, _y, _p in rows:
        vals.append((2 * L * (Q - hi * L), n, L, Q))
    vals.sort()
    inside = sum(1 for v, *_ in vals if v < 1)
    return {"is_a_measurement_not_a_check": True,
            "population": len(vals),
            "in_the_legendre_regime_2LD_lt_1": inside,
            "smallest_2LD": round(float(vals[0][0]), 6),
            "at_n": vals[0][1], "with_L": vals[0][2], "with_Q": vals[0][3],
            "closest_five": [{"n": n, "L": L, "Q": Q, "two_L_D": round(float(v), 4)}
                             for v, n, L, Q in vals[:5]]}


# ---------------------------------------------------------------------------
# §5  the measurement that is not vacuous
# ---------------------------------------------------------------------------


def check_near_miss_clustering(rows: list[tuple]) -> dict:
    """Do near misses land on best approximations to log2 3 more than others do?

    The round's Diophantine gate says a SURVIVING crossing must have Q_L/L
    exceptionally close to log2(3). Nothing survives (§3), so the gate itself
    cannot be tested. What can be tested is whether the mechanism leaves a trace
    below the threshold: among crossings ranked by how near they come to the
    correction cap, does Q_L/L sit on the Stern-Brocot path to log2(3) more often
    than it does for crossings generally?

    THE CONTROL IS THE POINT. "The top ten include 8/5" is worth nothing on its
    own — 8/5 might be where most crossings land. The base rate over the whole
    population, and the rate over the FURTHEST crossings, are both reported beside
    it, and the L>=2 restriction is reported too because L=1 forces Q/L = 2/1,
    which is a path member for a trivial reason and would inflate every share.
    """
    approx = best_approximation_set(max(r[2] for r in rows) + 1)
    ordered = sorted(rows, key=lambda r: r[0], reverse=True)

    def share(rs, min_L=1):
        rs = [r for r in rs if r[2] >= min_L]
        if not rs:
            return {"size": 0, "on_path": 0, "share": None}
        k = sum(1 for r in rs if Fraction(r[3], r[2]) in approx)
        return {"size": len(rs), "on_path": k, "share": round(100.0 * k / len(rs), 2)}

    # The control only controls if it is a different set. With the population
    # sorted by nearness, top and bottom must be disjoint, or "near misses cluster
    # more than ordinary crossings" would be comparing a set with itself -- which
    # is how a clustering claim passes while measuring nothing.
    top_ids = {r[1] for r in ordered[:1000]}
    bottom_ids = {r[1] for r in ordered[-1000:]}
    disjoint = len(rows) > 2000 and not (top_ids & bottom_ids)

    return {
        "path_size": len(approx),
        "control_is_a_disjoint_set": disjoint,
        "overlap": len(top_ids & bottom_ids),
        "all_L": {
            "top_10": share(ordered[:10]),
            "top_100": share(ordered[:100]),
            "top_1000": share(ordered[:1000]),
            "population": share(ordered),
            "bottom_1000": share(ordered[-1000:]),
        },
        "L_at_least_2": {
            "top_1000": share(ordered[:1000], min_L=2),
            "population": share(ordered, min_L=2),
            "bottom_1000": share(ordered[-1000:], min_L=2),
        },
    }


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                    help="walk odd starts below this (default %d)" % DEFAULT_LIMIT)
    ap.add_argument("--json", type=pathlib.Path, default=None)
    args = ap.parse_args()

    rows = sweep(args.limit)
    triples = synthetic_survivors()

    report = {
        "round": "Hard-Zeta Phase II / Round A-U.2e.2",
        "source_item": 41,
        "odd_starts_below": args.limit,
        "constant": check_constant(),
        "best_approximation_set": check_best_approximations(),
        "transcription": check_closed_form(rows),
        "unconditional": {
            "correction_bound": check_correction_bound(rows),
            "reset_inequality": check_reset_inequality(rows),
            "cap_equivalence": check_cap_equivalence(rows),
            "cap_threshold": check_cap_threshold_on_real_rows(rows),
        },
        "survival_census": survival_census(rows),
        "conditional_as_algebra": {
            "cap_equivalence_branches": check_cap_equivalence_branches(triples),
            "survival_cost": check_survival_cost(triples),
            "legendre_gate": check_legendre_gate(triples),
        },
        "legendre_distance_on_real_orbits": measure_legendre_distance(rows),
        "near_miss_clustering": check_near_miss_clustering(rows),
    }

    failures = []
    if report["transcription"]["violations"]:
        failures.append("closed form")
    for name, block in report["unconditional"].items():
        if (block.get("violations") or block.get("mismatches")
                or block.get("degenerate_bound")
                or block.get("slack_identity_violations")
                or any(v for k, v in block.items() if k.endswith("__failures"))):
            failures.append(name)
    if not report["constant"]["printed_digits_agree"]:
        failures.append("constant")
    if not report["best_approximation_set"]["classical_all_present"]:
        failures.append("approximation set misses a classical convergent")
    if not report["best_approximation_set"]["non_members_rejected"]:
        failures.append("approximation set accepts a non-member")
    if not report["near_miss_clustering"]["control_is_a_disjoint_set"]:
        failures.append("clustering control overlaps the sample it controls for")
    for name, block in report["conditional_as_algebra"].items():
        if any(v for k, v in block.items()
               if k.startswith("violations") or k == "satisfy_neither"
               or k.endswith("__failures")
               or k == "duration_branch_failed_on_the_duration_side"):
            failures.append(name)
    if not triples:
        failures.append("no synthetic configuration was built, so every "
                        "conditional check above is vacuous too")
    report["failures"] = failures
    report["passed"] = not failures

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
