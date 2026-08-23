"""Recheck of Hard-Zeta Phase II Round A-U.2d (source item 44).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Hard-Zeta Phase II / Round A-U.2d: Transducer
Rationality via Source Freeze, Bi-Exact Renewal, and a Complexity-Transfer
No-Go* (v0.1, 2026-08-12), shipped with `Hard_Zeta_AU2d_Literature_Notes_v0.1.md`.

**The round is a negative result about proof architecture, and it says so.** It
does not close CASP; it proves why transducer rationality *alone* cannot. Once a
positive integer source freezes, its lift tail is `0^inf` for EVERY positive
integer source, so any statistic reading only that tail takes the same value on a
convergent orbit, a hypothetical divergent one, and a CASP candidate.

That makes it unusually checkable for a Hard-Zeta round: source freeze, endpoint
exposure, the bi-exact horizon and the adelic bank identity are all statements
about **actual positive integers**, verifiable on real orbits without any
hypothetical object.

## What is measured here that the round does not state

Section 15 concludes `F_23(y)/L(y) -> 0` — the source is frozen and the endpoint
exact long before a large B-atom's first coefficient crossing. That is derived
under `L(y) >= c*y^kappa`, which holds for SURVIVING crossings, of which nobody
has an instance.

On real orbits the ordering is **reversed**, and overwhelmingly: the first
crossing happens *before* the source freezes. The share is measured below. This
is not a correction — the round is explicitly about the hypothetical large
B-atom — but "the obstruction lives in the bi-exact regime" reads very
differently once you know that essentially no real start is in that regime when
it crosses.

Everything exact: `2^Q > 3^L` for the crossing, modular arithmetic in `Z/2^N` for
the 2-adic source series, exact `Fraction` for the bank. No logarithm is
evaluated in a decision path; `floor(log2 y)` is a bit length and
`floor(log_{3/2} y)` is bracketed by exact integer powers.

Usage:  python code/src44_source_freeze.py [--limit N]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DEFAULT_LIMIT = 200_001


# ---------------------------------------------------------------------------
# exact primitives
# ---------------------------------------------------------------------------


def accel_tail(n: int, shift: int, blocks: int) -> tuple[int, list[int], list[int]]:
    """(Y_s, local cumulative valuations Q_0..Q_blocks, local endpoints).

    The accelerated odd map S(y) = (3y+1)/2^v2(3y+1), advanced `shift` blocks and
    then recorded for `blocks` more. Q is LOCAL: Q_j = K_{s+j} - K_s.
    """
    y = n
    for _ in range(shift):
        t = 3 * y + 1
        y = t >> ((t & -t).bit_length() - 1)
    y_s = y
    Qs, ys, Q = [0], [y], 0
    for _ in range(blocks):
        t = 3 * y + 1
        v = (t & -t).bit_length() - 1
        Q += v
        y = t >> v
        Qs.append(Q)
        ys.append(y)
    return y_s, Qs, ys


def floor_log2(y: int) -> int:
    """floor(log2 y) as a bit length, not a logarithm."""
    return y.bit_length() - 1


def floor_log32(y: int) -> int:
    """floor(log_{3/2} y), by exact integer comparison of 3^k against 2^k*y.

    (3/2)^k <= y  <=>  3^k <= 2^k * y, all integers.
    """
    k = 0
    while 3 ** (k + 1) <= (1 << (k + 1)) * y:
        k += 1
    return k


def first_crossing_length(n: int, cap: int = 20000) -> int | None:
    """The first accelerated odd-ENDPOINT coefficient crossing, 2^Q_L > 3^L."""
    y, Q, L, p3 = n, 0, 0, 1
    while L < cap:
        L += 1
        t = 3 * y + 1
        v = (t & -t).bit_length() - 1
        Q += v
        p3 *= 3
        y = t >> v
        if (1 << Q) > p3:
            return L
    return None


# ---------------------------------------------------------------------------
# section 2 — every odd endpoint is the 2-adic source of its own future tail
# ---------------------------------------------------------------------------


def check_shift_hereditary_source(limit: int) -> dict:
    """B(sigma^s q) = Y_s, in Z_2.

    The round's deepest checkable claim: the inverse-code series

        B(q) = - sum_{j>=0} 2^{Q_j} / 3^{j+1}

    converges 2-adically, and for the tail beginning at any shift it equals that
    shift's own endpoint. Evaluated in Z/2^N with the modular inverse of 3, so no
    2-adic library is involved and nothing is approximated.

    **A negative control runs beside it**, and it is not decoration: pairing one
    orbit's tail with a DIFFERENT orbit's endpoint must fail. Without it, a
    modular arithmetic slip that made everything congruent to everything would
    read as a perfect confirmation.
    """
    matches, mismatches, controls_ok, controls_bad = 0, [], 0, []
    cases = []
    n = 3
    while n < min(limit, 40001) and len(cases) < 400:
        for s in (0, 1, 3, 7):
            cases.append((n, s))
        n += 2 * max(1, (min(limit, 40001) // 400))
    for (n, s) in cases:
        y_s, Qs, _ys = accel_tail(n, s, 30)
        J = min(22, len(Qs) - 1)
        N = Qs[J]
        if N < 8:
            continue
        mod = 1 << N
        inv3 = pow(3, -1, mod)
        acc = 0
        for j in range(J):
            acc = (acc + pow(2, Qs[j], mod) * pow(inv3, j + 1, mod)) % mod
        b = (-acc) % mod
        if b == y_s % mod:
            matches += 1
        else:
            mismatches.append((n, s, y_s, b, N))
        # negative control: the same series against a different orbit's endpoint
        other, _Q2, _y2 = accel_tail(n + 2, s, 30)
        if other % mod != y_s % mod:
            if b != other % mod:
                controls_ok += 1
            else:
                controls_bad.append((n, s))
    return {"cases": matches + len(mismatches),
            "matches": matches, "mismatches": len(mismatches),
            "first_mismatch": mismatches[:3],
            "negative_controls_that_correctly_failed": controls_ok,
            "negative_controls_that_wrongly_matched": len(controls_bad),
            "control_is_exercised": controls_ok > 0}


# ---------------------------------------------------------------------------
# sections 4, 5, 8, 9 — the horizons
# ---------------------------------------------------------------------------


def check_horizons(limit: int) -> dict:
    """F_2(y) <= floor(log2 y), F_3 exposure, and the bi-exact horizon.

    Three separate facts:

      - F_2(y) = min{m : 2^{Q_m + 1} > y} is at most floor(log2 y), because
        every valuation is at least 1 so Q_m >= m.
      - m >= F_3(y) = floor(log_{3/2} y) + 1 forces Y_{s+m} < 3^m, via
        S(x) < 2x for odd x > 1.
      - F_23 = max of the two is at most floor(log_{3/2} y) + 1, because
        log_{3/2} y > log2 y for y > 1.

    The tightness of the first is reported, because a bound never approached
    would say little: `max_ratio` reaching 1 means it is attained.
    """
    f2_bad, exposure_bad, horizon_bad = [], [], []
    ratios, worst_ratio, attained = [], Fraction(0), 0
    horizons_strictly_dominated = 0
    starts = 0
    step = max(2, ((limit - 3) // 4000) | 1)
    for n in range(3, limit, step):
        if n % 2 == 0:
            continue
        starts += 1
        h2 = floor_log2(n)
        _y, Qs, ys = accel_tail(n, 0, max(h2 + 4, 8))
        # F_2
        f2 = next((m for m in range(len(Qs)) if (1 << (Qs[m] + 1)) > n), None)
        if f2 is None or f2 > h2:
            f2_bad.append((n, f2, h2))
            continue
        if h2:
            r = Fraction(f2, h2)
            ratios.append(r)
            worst_ratio = max(worst_ratio, r)
            attained += (r == 1)
        # F_3 exposure: for m >= F_3, Y_{s+m} < 3^m
        f3 = floor_log32(n) + 1
        for m in range(f3, min(len(ys), f3 + 6)):
            if not ys[m] < 3 ** m:
                exposure_bad.append((n, m, ys[m]))
                break
        # THE DEFINING PROPERTY, not the function against itself.
        #
        # `max(F_2, F_3) <= floor(log_{3/2} y) + 1` is a tautology when F_3 is
        # DEFINED as that expression -- the drill proved it by replacing
        # floor_log32 with floor_log2 and watching the gate stay green, because
        # both sides moved together. What section 9 actually rests on is that
        # floor(log2 y) <= floor(log_{3/2} y), so the 3-adic horizon dominates.
        # So the defining inequalities of floor_log32 are asserted directly,
        # k = floor(log_{3/2} y) means  3^k <= 2^k*y  and  3^(k+1) > 2^(k+1)*y,
        # and the domination is asserted separately.
        k = floor_log32(n)
        if not (3 ** k <= (1 << k) * n and 3 ** (k + 1) > (1 << (k + 1)) * n):
            horizon_bad.append(("floor_log32 fails its defining property", n, k))
        elif h2 > k:
            horizon_bad.append(("floor(log2 y) exceeds floor(log_{3/2} y)", n, h2, k))
        elif max(f2, f3) > k + 1:
            horizon_bad.append(("bi-exact horizon exceeds its bound", n, f2, f3))
        if h2 < k:
            horizons_strictly_dominated += 1
    return {"starts": starts,
            "freeze_bound_violations": len(f2_bad), "first_bad_freeze": f2_bad[:3],
            "endpoint_exposure_violations": len(exposure_bad),
            "first_bad_exposure": exposure_bad[:3],
            "bi_exact_horizon_violations": len(horizon_bad),
            "mean_F2_over_floor_log2": round(float(sum(ratios) / len(ratios)), 4)
            if ratios else None,
            "max_F2_over_floor_log2": float(worst_ratio),
            "starts_where_the_bound_is_ATTAINED": attained,
            "starts_where_log2_is_STRICTLY_below_log32": horizons_strictly_dominated,
            "domination_is_strict_somewhere": horizons_strictly_dominated > 0,
            "bound_is_attained": attained > 0}


def check_contraction() -> dict:
    """S(x) < 2x for odd x > 1, and S(1) = 1 — the step behind endpoint exposure.

    Exhaustive over a range rather than sampled, because it is cheap and because
    the inequality is what makes `Y_{s+m} < 2^m y` and hence the whole exposure
    argument work. Also proved in one line: v >= 1 so S(x) <= (3x+1)/2 < 2x iff
    x > 1 — the run confirms the transcription, not the arithmetic.
    """
    bad, checked = [], 0
    for x in range(3, 200001, 2):
        t = 3 * x + 1
        s = t >> ((t & -t).bit_length() - 1)
        checked += 1
        if not s < 2 * x:
            bad.append(x)
    t = 4
    s1 = t >> ((t & -t).bit_length() - 1)
    return {"odd_x_checked": checked, "violations": len(bad), "first_bad": bad[:3],
            "S_of_1_is_1": s1 == 1,
            "note": "one line of algebra: v >= 1 gives S(x) <= (3x+1)/2, which is "
                    "< 2x exactly when x > 1"}


# ---------------------------------------------------------------------------
# sections 10 and 11 — the bi-exact relation and the adelic bank
# ---------------------------------------------------------------------------


def check_bank(limit: int) -> dict:
    """A_m = y + sum_{j<m} 2^{Q_j}/3^{j+1} = 2^{Q_m} Y_{s+m} / 3^m, and v2(A_m) = Q_m.

    Two expressions for the same rational, built independently and compared —
    which is the lesson item 43 taught about checks that cannot fail. The
    2-adic valuation claim is then exact: numerator carries 2^{Q_m} and both
    Y_{s+m} and 3^m are odd.

    The Archimedean bound `y <= A_m <= y + m/3` needs every prefix subcritical,
    which a real orbit loses at the crossing — so it is checked as holding before
    and required to be seen FAILING after, exactly as in RUN-024.
    """
    two_expr_bad, val_bad, before_bad = [], [], []
    fails_after = 0
    starts = 0
    step = max(2, ((limit - 3) // 1200) | 1)
    for n in range(3, limit, step):
        if n % 2 == 0:
            continue
        starts += 1
        y_s, Qs, ys = accel_tail(n, 0, 24)
        L = first_crossing_length(n) or len(Qs)
        acc = Fraction(y_s)
        for m in range(len(Qs)):
            closed = Fraction((1 << Qs[m]) * ys[m], 3 ** m)
            if acc != closed:
                two_expr_bad.append((n, m))
                break
            # v2 of the rational: numerator 2^{Q_m} * odd, denominator odd
            num, den = closed.numerator, closed.denominator
            v2 = (num & -num).bit_length() - 1
            if den % 2 == 0 or v2 != Qs[m]:
                val_bad.append((n, m, v2, Qs[m]))
                break
            if m < min(L, len(Qs)) and closed > y_s + Fraction(m, 3):
                before_bad.append((n, m))
                break
            acc += Fraction(1 << Qs[m], 3 ** (m + 1))
        else:
            if any(Fraction((1 << Qs[m]) * ys[m], 3 ** m) > y_s + Fraction(m, 3)
                   for m in range(len(Qs))):
                fails_after += 1
    return {"starts": starts,
            "two_expressions_disagree": len(two_expr_bad),
            "first_bad": two_expr_bad[:3],
            "v2_of_bank_not_equal_to_Q": len(val_bad),
            "archimedean_bound_violations_before_the_crossing": len(before_bad),
            "starts_where_it_fails_after_the_crossing": fails_after,
            "has_a_negative_half": fails_after > 0}


# ---------------------------------------------------------------------------
# section 15 — the scale separation, and which way it actually points
# ---------------------------------------------------------------------------


def measure_freeze_versus_crossing(limit: int) -> dict:
    """Does the source freeze BEFORE the first crossing, on orbits that exist?

    Section 15 concludes `F_23(y) < L(y)` for large surviving B-atoms, from
    `L(y) >= c*y^kappa`. That hypothesis is about SURVIVING crossings, which
    RUN-023 measured 0 of below 2e5.

    This asks the same question of real starts, where `L` is the ordinary first
    crossing length. It is a measurement with a verdict, not a pass or a fail:
    the round's implication is not contradicted by real orbits being in the other
    regime, because they do not satisfy its hypothesis. What the number gives is
    a sense of how far the bi-exact regime is from anything exhibitable.
    """
    before = after = equal = 0
    examples = []
    step = max(2, ((limit - 3) // 30000) | 1)
    for n in range(3, limit, step):
        if n % 2 == 0:
            continue
        L = first_crossing_length(n)
        if L is None:
            continue
        h2 = floor_log2(n)
        _y, Qs, _ys = accel_tail(n, 0, max(h2 + 4, 8))
        f2 = next((m for m in range(len(Qs)) if (1 << (Qs[m] + 1)) > n), h2)
        f23 = max(f2, floor_log32(n) + 1)
        if f23 < L:
            before += 1
            if len(examples) < 5:
                examples.append({"n": n, "F2": f2, "F23": f23, "L": L})
        elif f23 > L:
            after += 1
        else:
            equal += 1
    tot = before + after + equal
    return {"is_a_measurement_with_a_verdict": True,
            "starts": tot,
            "source_frozen_before_the_crossing": before,
            "share_pct": round(100.0 * before / tot, 2) if tot else None,
            "crossing_first": after,
            "crossing_first_pct": round(100.0 * after / tot, 2) if tot else None,
            "tie": equal,
            "examples_in_the_bi_exact_regime": examples,
            "verdict": (
                "on real starts the ordering is REVERSED almost always: the first "
                "coefficient crossing happens before the source freezes. Section "
                "15's regime is reached under L(y) >= c*y^kappa, which is the "
                "surviving-crossing hypothesis, and RUN-023 found no surviving "
                "crossing below 2e5. So the bi-exact regime the round locates the "
                "obstruction in is not a regime any exhibitable start is in when "
                "it crosses."
            )}


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--json", type=pathlib.Path, default=None)
    args = ap.parse_args()

    report = {
        "round": "Hard-Zeta Phase II / Round A-U.2d",
        "source_item": 44,
        "odd_starts_below": args.limit,
        "shift_hereditary_source": check_shift_hereditary_source(args.limit),
        "horizons": check_horizons(args.limit),
        "contraction": check_contraction(),
        "adelic_bank": check_bank(args.limit),
        "freeze_versus_crossing": measure_freeze_versus_crossing(args.limit),
    }

    failures = []
    sh = report["shift_hereditary_source"]
    if sh["mismatches"]:
        failures.append("shift_hereditary_source")
    if sh["negative_controls_that_wrongly_matched"]:
        failures.append("shift_hereditary_source: a wrong endpoint matched")
    if not sh["control_is_exercised"]:
        failures.append("shift_hereditary_source: the negative control never ran, "
                        "so the match is not discriminating")
    h = report["horizons"]
    for key, name in (("freeze_bound_violations", "freeze bound"),
                      ("endpoint_exposure_violations", "endpoint exposure"),
                      ("bi_exact_horizon_violations", "bi-exact horizon")):
        if h[key]:
            failures.append("horizons: " + name)
    if not h["bound_is_attained"]:
        failures.append("horizons: the freeze bound is never attained, so its "
                        "tightness is unmeasured")
    if not h["domination_is_strict_somewhere"]:
        failures.append("horizons: floor(log2 y) never falls strictly below "
                        "floor(log_{3/2} y), so the domination is untested")
    if report["contraction"]["violations"] or not report["contraction"]["S_of_1_is_1"]:
        failures.append("contraction")
    b = report["adelic_bank"]
    if b["two_expressions_disagree"] or b["v2_of_bank_not_equal_to_Q"] \
            or b["archimedean_bound_violations_before_the_crossing"]:
        failures.append("adelic_bank")
    if not b["has_a_negative_half"]:
        failures.append("adelic_bank: the Archimedean bound never fails, so the "
                        "two-sided test has no negative half")

    report["failures"] = failures
    report["passed"] = not failures

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
