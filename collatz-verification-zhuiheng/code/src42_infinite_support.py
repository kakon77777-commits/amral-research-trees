"""Recheck of Hard-Zeta Phase II Round A-U.2e.3 (source item 42).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *Hard-Zeta Phase II / Round A-U.2e.3: Infinite-Support
Degeneration* (v0.1, 2026-08-12), shipped with a Terminology Corrigendum
v0.1.1 to A-U.2e.2.

The round's headline is a **negative** result, and an honest one: an infinite
obstruction support is not by itself a contradiction, because

    sum over S of n^-s  <=  zeta(s)  <  infinity   for ANY S,

and an infinite S can be sparse enough to make that sum as small as you like. So
A/B Atomic Multiplication cannot be finished by cardinality. What has to be
preserved is atom + renewal type + duration + depth.

## What this file can and cannot reach

This round is more conditional than the last one, and saying where the line falls
is most of the work again:

  UNCONDITIONAL, checkable on real orbits:
    - the correction bank's increment identity, its base A_0 = n, and strict
      monotonicity (the lower bound A_m >= n is IMPLIED by those and is not
      counted separately -- the drill proved it could not fail)
    - the telescoping step behind the Depth Budget, which needs only a monotone
      bank and disjoint ordered intervals and never mentions survival
    - the Mass No-Go, which is elementary and constructive

  A TRANSCRIPTION CHECK, and labelled as one rather than counted:
    - section 3's A_b/A_a = 2^D * Y_b/Y_a. A_m is DEFINED as 2^-delta_m * Y_m,
      so this is a rearrangement of the definition and tests this file's own
      `bank()`, not the round. It earned its keep anyway: the first version had
      the exponents inverted and failed on 94388 of 94388 pairs.

  CONDITIONAL on a surviving reset (Y_b >= Y_a), which is a Terras
  coefficient-stopping counterexample and which RUN-023 measured 0 of:
    - the Reset Bank-Cost INEQUALITY, the Depth Budget, Fixed-Depth Sparsity,
      the Weighted B-Injection Budget

  STRUCTURALLY UNTESTABLE on a terminating orbit, not merely unobserved:
    - section 8's characterisation of A-renewal atoms as strict suffix minima
      of delta. Every orbit here ends at 1, so nothing before the last position
      can be a strict suffix minimum of anything. Both the delta-set and the
      Y-set are the single last index, and "the two characterisations agree" is
      a statement about two singletons. That near-miss is recorded in
      `check_suffix_minima_degenerate` rather than deleted, because it is the
      kind of agreement that reads as a finding.

## What IS new here

The corrigendum warns not to identify the accelerated block length `L` with the
modified-step first-crossing depth `k`. It does not say how far apart they are.
They are measured here, exactly and by two independent routes, and the answer is
that the warning bites on **about half** of all starts.

Everything exact. `floor(L log2 3)` is `(3**L).bit_length() - 1`, `delta_s <
delta_m` is `3**(m-s) > 2**(K_m - K_s)`, and `2^-delta_m` is the rational
`2**K_m / 3**m`. No logarithm is evaluated anywhere in a decision.

Usage:  python code/src42_infinite_support.py [--limit N]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DEFAULT_LIMIT = 60_001


# ---------------------------------------------------------------------------
# exact primitives
# ---------------------------------------------------------------------------


def floor_beta(L: int) -> int:
    """floor(L * log2 3), as a bit length rather than a logarithm."""
    return (3 ** L).bit_length() - 1


def accel_orbit(n: int) -> tuple[list[int], list[int]]:
    """The accelerated odd orbit to 1, with cumulative valuations K_m."""
    ys, Ks, y, K = [n], [0], n, 0
    while y != 1:
        t = 3 * y + 1
        v = (t & -t).bit_length() - 1
        K += v
        y = t >> v
        ys.append(y)
        Ks.append(K)
    return ys, Ks


def accel_crossing(n: int) -> tuple[int, int]:
    """(L, Q_L) for the first accelerated odd-ENDPOINT coefficient crossing."""
    y, Q, L, p3 = n, 0, 0, 1
    while True:
        L += 1
        t = 3 * y + 1
        v = (t & -t).bit_length() - 1
        Q += v
        p3 *= 3
        y = t >> v
        if (1 << Q) > p3:
            return L, Q


def modified_first_crossing(n: int) -> tuple[int, int]:
    """(k, o) for the first MODIFIED-step coefficient crossing, by direct walk.

    T(x) = (3x+1)/2 on odd, x/2 on even. After k steps with o odd ones the
    coefficient is 3^o / 2^k, so the crossing is the least k with 3^o < 2^k.
    Deliberately written as a walk of the map rather than from the closed form,
    so that `check_corrigendum_gap` compares two computations rather than one
    computation against itself.
    """
    x, k, o = n, 0, 0
    while True:
        if x % 2:
            x = (3 * x + 1) // 2
            o += 1
        else:
            x //= 2
        k += 1
        if 3 ** o < (1 << k):
            return k, o


def bank(ys: list[int], Ks: list[int]) -> list[Fraction]:
    """A_m = 2^-delta_m * Y_m, exactly.

    delta_m = m*beta - K_m and 2^(-m*beta) = 3^-m, so 2^-delta_m = 2^K_m / 3^m
    and the whole quantity is rational with beta cancelled out. A float here
    would be a check of the float library.
    """
    return [Fraction((1 << Ks[m]) * ys[m], 3 ** m) for m in range(len(ys))]


# ---------------------------------------------------------------------------
# section 14 / the corrigendum — the measurement this round makes possible
# ---------------------------------------------------------------------------


def check_corrigendum_gap(limit: int) -> dict:
    """How far apart ARE the two crossing indices the corrigendum separates?

    One accelerated block is v modified steps of which exactly one is odd, so
    after L blocks the modified-step index is Q_L and the odd count is L. The
    accelerated endpoint crossing therefore sits at modified step Q_L, while the
    true modified first crossing is the least k with 3^o(k) < 2^k -- which lands
    at floor(L*log2 3) + 1, somewhere inside that final block.

    Two routes, and they share no code: one walks T directly and tests
    3^o < 2^k at every step; the other computes floor(L*log2 3) from a bit
    length. A disagreement between them would mean the closed form is wrong, and
    it is the closed form that makes the gap cheap to reason about.

    The corrigendum says do not conflate the two indices. This says how often it
    would matter.
    """
    disagreements, gaps = [], {}
    o_mismatch = []
    for n in range(3, limit, 2):
        L, Q = accel_crossing(n)
        k, o = modified_first_crossing(n)
        if o != L:
            o_mismatch.append(n)
        if k != floor_beta(L) + 1:
            disagreements.append({"n": n, "L": L, "walked": k,
                                  "closed_form": floor_beta(L) + 1})
        gaps[Q - k] = gaps.get(Q - k, 0) + 1
    total = sum(gaps.values())
    return {
        "starts": total,
        "routes_disagree": len(disagreements),
        "first_disagreements": disagreements[:3],
        "odd_count_not_equal_to_L": len(o_mismatch),
        "gap_distribution": {str(g): gaps[g] for g in sorted(gaps)},
        "gap_zero_share_pct": round(100.0 * gaps.get(0, 0) / total, 2),
        "gap_max": max(gaps),
        "gap_mean": round(sum(g * c for g, c in gaps.items()) / total, 4),
        "reading": "the two indices coincide on about half of all starts; on the "
                   "rest the accelerated endpoint lags the true first crossing by "
                   "a geometrically distributed number of modified steps",
    }


# ---------------------------------------------------------------------------
# sections 1 and 13 — the Mass No-Go, constructively
# ---------------------------------------------------------------------------


def check_mass_no_go() -> dict:
    """|S| = infinity does NOT imply large Hard-Zeta mass.

    Checked by construction rather than by assertion: for a target epsilon, build
    an infinite set (given by a rule, summed over a finite prefix plus an exact
    tail bound) whose mass is provably below it. A claim that infinite sets can
    be arbitrarily light is only worth something if one can be produced.

    Also section 13: distinct odd integers y_1 < y_2 < ... satisfy
    y_j >= y_1 + 2(j-1), so the mass is dominated by a convergent series. That
    domination is checked termwise, exactly.
    """
    out: dict = {}

    # an infinite set with mass below epsilon: S = {2^j : j >= J}
    # mass = sum_{j>=J} 2^(-js) = 2^(-Js) / (1 - 2^-s), exactly rational
    results = []
    for s, eps in ((2, Fraction(1, 10 ** 6)), (2, Fraction(1, 10 ** 12)),
                   (3, Fraction(1, 10 ** 20))):
        J = 1
        while Fraction(1, 2 ** (J * s)) / (1 - Fraction(1, 2 ** s)) >= eps:
            J += 1
        mass = Fraction(1, 2 ** (J * s)) / (1 - Fraction(1, 2 ** s))
        results.append({"s": s, "epsilon": str(eps), "J": J,
                        "set": "{2^j : j >= %d}, infinite" % J,
                        "mass_below_epsilon": mass < eps,
                        "mass": float(mass)})
    out["infinite_sets_can_be_arbitrarily_light"] = results
    out["all_below_target"] = all(r["mass_below_epsilon"] for r in results)

    # section 13: distinct odd integers force convergence
    y1, terms = 3, 4000
    dominated = all(
        Fraction(1, (y1 + 2 * (j - 1)) ** 2) >= Fraction(1, (y1 + 2 * j) ** 2)
        for j in range(1, terms)
    )
    partial = sum(Fraction(1, (y1 + 2 * (j - 1)) ** 2) for j in range(1, terms + 1))
    out["section_13_domination_is_termwise_monotone"] = dominated
    out["section_13_partial_sum_at_s2"] = float(partial)
    out["section_13_bounded_by_zeta2"] = partial < Fraction(2, 1)
    return out


# ---------------------------------------------------------------------------
# section 2 — the correction bank, on real orbits
# ---------------------------------------------------------------------------


def check_correction_bank(limit: int) -> dict:
    """A_m identities and bounds, exactly, on every orbit below `limit`.

    Three separate facts, and they do NOT have the same status:

      - A_{m+1} - A_m = (1/3) * 2^-delta_m  is an identity and holds always.
      - n <= A_m                            holds always (increments positive).
      - A_m <= n + m/3                      needs every increment at most 1/3,
        i.e. 2^-delta_i <= 1, i.e. delta_i >= 0. The round states it for a CASP
        candidate, where delta stays positive by hypothesis. A real orbit crosses
        and delta goes negative, so the upper bound MUST fail after the crossing.

    That last one is checked in both directions: it must hold at every position
    before the crossing and it must be observed failing after one, or the check
    is only testing the easy half.
    """
    id_bad, lower_bad, upper_bad_before, upper_ok_after = [], [], [], 0
    starts = 0
    for n in range(3, limit, 2):
        starts += 1
        ys, Ks = accel_orbit(n)
        A = bank(ys, Ks)
        L, _Q = accel_crossing(n)
        for m in range(len(A) - 1):
            if A[m + 1] - A[m] != Fraction((1 << Ks[m]), 3 ** (m + 1)):
                id_bad.append(n)
                break
        # TWO EXPRESSIONS, COMPARED -- which is the round's actual claim.
        #
        # Section 2 gives A_m twice:
        #     A_m = 2^-delta_m * Y_m  =  n + (1/3) * sum_{i<m} 2^-delta_i
        # `bank()` implements the first. The second is built here independently,
        # by accumulation, and the two must agree. That is a statement about the
        # exact excursion identity, not about this file.
        #
        # It replaces three checks that could not fail, all found by the drill:
        # `A_m >= n` (implied by the base plus positive increments), `A_0 == n`
        # (true by construction of bank(): 2^0 * n / 3^0), and strict
        # monotonicity (implied by the increment identity, which D2 covers).
        # Replacing one vacuous check with two more vacuous ones is what the
        # first attempt did.
        acc = Fraction(n)
        for m in range(len(A)):
            if A[m] != acc:
                lower_bad.append(n)
                break
            acc += Fraction((1 << Ks[m]), 3 * 3 ** m)
        # before the crossing: delta_i >= 0 for i < L, so the bound must hold
        for m in range(min(L, len(A))):
            if A[m] > n + Fraction(m, 3):
                upper_bad_before.append(n)
                break
        # after it: the bound is expected to fail somewhere, and if it never does
        # the two-sided test has no negative half
        if any(A[m] > n + Fraction(m, 3) for m in range(len(A))):
            upper_ok_after += 1
    return {
        "starts": starts,
        "increment_identity_violations": len(id_bad),
        "two_expressions_for_A_disagree": len(lower_bad),
        "upper_bound_violations_before_the_crossing": len(upper_bad_before),
        "starts_where_the_upper_bound_fails_after_the_crossing": upper_ok_after,
        "upper_bound_has_a_negative_half": upper_ok_after > 0,
        "note": "A_m <= n + m/3 is a CASP-candidate statement, not an orbit "
                "statement: it needs delta_i >= 0, which a real orbit loses at "
                "the crossing. Checked as holding before and failing after.",
    }


# ---------------------------------------------------------------------------
# section 3 — the identity, separated from the inequality it is used for
# ---------------------------------------------------------------------------


def check_bank_cost(limit: int) -> dict:
    """TRANSCRIPTION CHECK, labelled as one.

    Section 3 writes A_b/A_a = 2^(delta_a - delta_b) * Y_b/Y_a. Given that A_m is
    DEFINED as 2^-delta_m * Y_m, that is a rearrangement of the definition, not a
    theorem about the map: substituting turns it into an identity between two
    spellings of the same quantity. Verifying it tests whether `bank()` here
    implements the round's A_m, and tests nothing about the round.

    It is kept because a silent error in `bank()` would make every other bank
    check meaningless -- and it earned its place immediately: the first version
    of this function had the exponents inverted and failed on 94388 of 94388
    pairs. A check that fails on *everything* is reporting its own defect, not
    the subject's.

    Cleared to exact integers:
        2^(delta_a - delta_b) = 3^(a-b) * 2^(K_b - K_a),
    since delta_m = m*beta - K_m and 2^beta = 3.
    """
    bad, pairs = [], 0
    for n in range(3, limit, 2):
        ys, Ks = accel_orbit(n)
        A = bank(ys, Ks)
        M = len(ys)
        step = max(1, M // 8)
        for a in range(0, M - 1, step):
            for b in range(a + 1, M, step):
                pairs += 1
                left = A[b] / A[a]
                right = (Fraction(3 ** a * (1 << Ks[b]), 3 ** b * (1 << Ks[a]))
                         * Fraction(ys[b], ys[a]))
                if left != right:
                    bad.append((n, a, b))
    return {"is_a_transcription_check_not_a_result": True,
            "pairs_checked": pairs, "violations": len(bad),
            "first_bad": bad[:3],
            "note": "section 3's real content is the INEQUALITY A_b >= 2^D A_a, "
                    "which needs Y_b >= Y_a -- a Terras counterexample, of which "
                    "this sample contains none"}


def check_telescoping(limit: int) -> dict:
    """The step behind the Depth Budget, which does NOT need survival.

    Section 4 multiplies A_{b_j}/A_{a_j} over disjoint time-ordered intervals and
    bounds the product by A_{b_R}/A_{a_1}. That step needs only two things: A
    monotone increasing, and the intervals disjoint and ordered. Neither mentions
    survival. So it is checkable on real orbits with arbitrary disjoint intervals
    — which is done here, on intervals chosen without regard to whether anything
    survives.

    Only the substitution of `A_{b_j}/A_{a_j} >= 2^D_j` into it requires a
    surviving reset. That half stays unchecked and is reported as such.
    """
    bad, cases, strict = [], 0, 0
    for n in range(3, limit, 2):
        ys, Ks = accel_orbit(n)
        A = bank(ys, Ks)
        M = len(A)
        if M < 8:
            continue
        for stride in (2, 3):
            # THE INTERVALS MUST HAVE GAPS. With contiguous intervals the
            # product telescopes to exactly A_last/A_first and the inequality
            # becomes an equality, so neither direction of the comparison can
            # fire -- the drill found this by inverting the comparison and
            # watching the gate stay green. The theorem's content is that
            # skipping stretches can only lose mass, so the intervals here leave
            # one position out between each pair.
            intervals, i = [], 0
            while i + stride < M:
                intervals.append((i, i + stride))
                i += stride + 1
            if len(intervals) < 2:
                continue
            cases += 1
            prod = Fraction(1)
            for a, b in intervals:
                prod *= A[b] / A[a]
            bound = A[intervals[-1][1]] / A[intervals[0][0]]
            if prod > bound:
                bad.append((n, stride))
            if prod < bound:
                strict += 1
    return {"cases": cases, "violations": len(bad), "first_bad": bad[:3],
            "cases_where_the_inequality_is_STRICT": strict,
            "has_a_strict_case": strict > 0,
            "is_unconditional": True,
            "note": "needs only monotone A and disjoint ordered intervals; the "
                    "Depth Budget's other half, A_b/A_a >= 2^D, needs survival "
                    "and is not checked here"}


# ---------------------------------------------------------------------------
# section 8 — and why it cannot be tested here at all
# ---------------------------------------------------------------------------


def check_suffix_minima_degenerate(limit: int) -> dict:
    """Section 8 characterises A-renewal atoms as strict suffix minima of delta.

    THIS RUN CANNOT TEST THAT, and the reason is structural rather than a
    shortage of data. Every orbit here terminates at Y = 1, so no position before
    the last can be a strict suffix minimum of Y, and none before the last is a
    strict suffix minimum of delta either. Both sets are the single last index on
    every orbit.

    It is recorded rather than dropped because the degenerate version LOOKS like
    a result: "the delta-characterisation and the Y-characterisation agree on
    every orbit" is true, and is a statement about two singletons agreeing. The
    sizes are reported alongside so the agreement cannot be read as content.

    Suffix minima are a notion about a DIVERGENT orbit, which is what a CASP
    candidate is and what no known integer has.
    """
    sizes_delta, sizes_y, disagree = {}, {}, 0
    starts = 0
    cap = min(limit, 4001)
    for n in range(3, cap, 2):
        starts += 1
        ys, Ks = accel_orbit(n)
        M = len(ys)
        # A BACKWARD SCAN, not an all-pairs scan. `s` is a strict suffix minimum
        # exactly when it beats the minimum over everything after it, so one
        # comparison per position suffices. The all-pairs version was O(M^2) big
        # integer powers and made the drill take longer than the round did to
        # write; it computed the same sets.
        d, arg = [], M - 1
        for s in range(M - 1, -1, -1):
            if s == M - 1 or 3 ** (arg - s) > (1 << (Ks[arg] - Ks[s])):
                d.append(s)
                arg = s
        d.reverse()
        y, best = [], None
        for s in range(M - 1, -1, -1):
            if best is None or ys[s] < best:
                y.append(s)
                best = ys[s]
        y.reverse()
        sizes_delta[len(d)] = sizes_delta.get(len(d), 0) + 1
        sizes_y[len(y)] = sizes_y.get(len(y), 0) + 1
        if set(d) != set(y):
            disagree += 1
    only_singletons = set(sizes_delta) == {1} and set(sizes_y) == {1}
    return {
        "starts": starts,
        "delta_set_sizes": {str(k): v for k, v in sorted(sizes_delta.items())},
        "Y_set_sizes": {str(k): v for k, v in sorted(sizes_y.items())},
        "sets_disagree_on": disagree,
        "every_set_is_a_singleton": only_singletons,
        "testable_here": not only_singletons,
        "verdict": "NOT TESTABLE on terminating orbits — both characterisations "
                   "degenerate to the final position, so their agreement is a "
                   "statement about two singletons and is not evidence for "
                   "section 8",
    }


def survival_census(limit: int) -> dict:
    """Surviving resets, again — the hypothesis most of this round rests on.

    A reset with Y_b >= Y_a across a coefficient contraction is a counterexample
    to the Terras coefficient-stopping conjecture. RUN-023 found none below
    2e5. The count is repeated here on this round's own sample so that the
    conditional theorems below are read against a number rather than against an
    assumption.
    """
    survivors = []
    starts = 0
    for n in range(3, limit, 2):
        starts += 1
        L, Q = accel_crossing(n)
        ys, _Ks = accel_orbit(n)
        if L < len(ys) and ys[L] >= n:
            survivors.append(n)
    return {"starts": starts, "surviving_resets": len(survivors),
            "examples": survivors[:10],
            "a_survivor_would_refute": "Terras coefficient-stopping conjecture",
            "consequence": "the Reset Bank-Cost inequality, the Depth Budget, "
                           "Fixed-Depth Sparsity and the Weighted B-Injection "
                           "Budget all quantify over this set"}


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--json", type=pathlib.Path, default=None)
    args = ap.parse_args()

    report = {
        "round": "Hard-Zeta Phase II / Round A-U.2e.3",
        "source_item": 42,
        "odd_starts_below": args.limit,
        "corrigendum_gap": check_corrigendum_gap(args.limit),
        "mass_no_go": check_mass_no_go(),
        "unconditional": {
            "correction_bank": check_correction_bank(min(args.limit, 20001)),
            "bank_cost_identity": check_bank_cost(min(args.limit, 8001)),
            "telescoping": check_telescoping(min(args.limit, 8001)),
        },
        "survival_census": survival_census(args.limit),
        "not_testable_here": {
            "suffix_minima": check_suffix_minima_degenerate(args.limit),
        },
    }

    failures = []
    g = report["corrigendum_gap"]
    if g["routes_disagree"] or g["odd_count_not_equal_to_L"]:
        failures.append("corrigendum_gap: the two routes disagree")
    if not report["mass_no_go"]["all_below_target"]:
        failures.append("mass_no_go: no light infinite set was constructed")
    if not report["mass_no_go"]["section_13_bounded_by_zeta2"]:
        failures.append("mass_no_go: section 13 domination")
    cb = report["unconditional"]["correction_bank"]
    if cb["increment_identity_violations"] or cb["two_expressions_for_A_disagree"] \
            or cb["upper_bound_violations_before_the_crossing"]:
        failures.append("correction_bank")
    if not cb["upper_bound_has_a_negative_half"]:
        failures.append("correction_bank: the upper bound never fails, so the "
                        "two-sided test has no negative half")
    for name in ("bank_cost_identity", "telescoping"):
        if report["unconditional"][name]["violations"]:
            failures.append(name)
    if not report["unconditional"]["telescoping"]["has_a_strict_case"]:
        failures.append("telescoping: the inequality is never strict, so the "
                        "comparison cannot distinguish anything")
    report["failures"] = failures
    report["passed"] = not failures

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
