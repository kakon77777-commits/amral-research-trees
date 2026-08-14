"""Independent recheck of the Paper 05 KL constant — digits and meaning.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, Collatz Operation Translation Series, Paper 05 / validation.json.

The claim
---------
`validation.json` records, for the `p05_binomial_and_k16_benchmark` group:

    alpha = 0.6309297535714574
    KL    = 0.03468818523201744

and the subject's suite asserts the second to within 1e-14 of

    D = alpha*ln(alpha/0.5) + (1-alpha)*ln((1-alpha)/0.5).

Checking that a float literal matches a float computation is the weakest
possible form of this check: both sides are doubles, both are computed the same
way, and neither is pinned to the real number. Two things are done instead.

1. The digits are recomputed in 60-digit arithmetic, so the published constant
   is compared against the real value rather than against another double.

2. The constant's *role* is verified. D is the Kullback-Leibler divergence of
   Bernoulli(alpha) from Bernoulli(1/2), and the reason it appears in Paper 05 is
   that it governs how fast the non-contracting fraction 1 - P_k(3) decays. That
   is a statement with consequences, and the consequences are measured on exact
   binomial tails:

     upper: 1 - P_k  <=  exp(-k D)                     for every k tested
     rate : -(ln(1 - P_k) + k D) grows like (1/2) ln k

   The second is the sharp one. If D were even slightly wrong, the residual
   would grow or shrink linearly in k instead of logarithmically, and the ratio
   below would diverge instead of settling near 1/2.

Nothing here bears on the Collatz conjecture.

Usage:  python code/ot_paper05_kl_recheck.py
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from math import comb

getcontext().prec = 60

PUBLISHED_ALPHA = "0.6309297535714574"
PUBLISHED_KL = "0.03468818523201744"
KS = (50, 100, 250, 500, 1000, 2000, 4000, 8000)


def hp_alpha() -> Decimal:
    return Decimal(2).ln() / Decimal(3).ln()


def hp_kl(a: Decimal) -> Decimal:
    return a * (a / Decimal("0.5")).ln() + (1 - a) * ((1 - a) / Decimal("0.5")).ln()


def exact_tail_count(k: int, u_max: int) -> int:
    """The integer count of length-k words on the non-contracting side."""
    return sum(comb(k, u) for u in range(u_max + 1, k + 1))


def exact_upper_tail(k: int, u_max: int) -> Decimal:
    """1 - P_k as an exact rational, then converted at 60 digits.

    u_max is the exact largest u with 3^u < 2^k, found by integer comparison
    rather than by a floating floor."""
    return Decimal(exact_tail_count(k, u_max)) / (Decimal(2) ** k)


def exact_u_max(k: int) -> int:
    u, p = 0, 1
    while p * 3 < 2 ** k:
        p *= 3
        u += 1
    return u


def main() -> int:
    rep = {
        "tool": "ot_paper05_kl_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 05 / validation.json (Neo.K)",
        "scope": "exact binomial tails and 60-digit arithmetic; not a Collatz proof",
        "checks": {},
        "subject_findings": [],
        "stated_limits": [],
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        """A check is about whether THIS recheck ran soundly. Its failure means
        the instrument is broken and the run must not be trusted."""
        rep["checks"][name] = {"pass": bool(ok), **({"detail": detail} if detail else {})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    def finding(name: str, holds: bool, detail: str) -> None:
        """A finding is about the SUBJECT. A defect in the subject must be
        reportable without being indistinguishable from a broken instrument, so
        findings are recorded and do not set the run's exit status."""
        rep["checks"][name] = {"subject_claim_holds": bool(holds), "detail": detail}
        if not holds:
            rep["subject_findings"].append({"claim": name, "detail": detail})

    # --- 1. the digits, against the real value ------------------------------
    a = hp_alpha()
    D = hp_kl(a)
    a_pub = Decimal(PUBLISHED_ALPHA)
    D_pub = Decimal(PUBLISHED_KL)
    # a double carries ~17 significant digits; the published literals should
    # agree with the real value to within one unit in the last place they state
    import math

    a_err = abs(a - a_pub)
    D_err = abs(D - D_pub)
    ulp = Decimal(math.ulp(float(D_pub)))

    # What the published literals ARE: the faithful output of evaluating the
    # stated expression in double precision. That much holds exactly.
    alpha_f = math.log(2) / math.log(3)
    D_f = alpha_f * math.log(alpha_f / 0.5) + (1 - alpha_f) * math.log((1 - alpha_f) / 0.5)
    check("P05_published_literals_are_the_faithful_double_output_of_the_stated_expression",
          float(a_pub) == alpha_f and float(D_pub) == D_f)

    # What they are NOT: the nearest double to the real value. The KL literal
    # carries the rounding error accumulated by that expression.
    nearest = float(D)
    check("P05_published_KL_agrees_with_the_real_value_to_16_significant_digits",
          D > 0 and D_err / abs(D) < Decimal("1e-15"),
          f"relative error {D_err / abs(D):.3e}, D = {D:.6e}")
    finding("P05_published_KL_is_the_nearest_double_to_the_real_value",
            float(D_pub) == nearest,
            f"published {D_pub!s} is {D_err / ulp:.2f} ULP from the real value; the "
            f"nearest double is {nearest!r}. The literal is the faithful output of "
            f"the stated float expression, so this is accumulated rounding rather "
            f"than a typo, and only the 17th significant digit is affected.")
    check("P05_published_alpha_is_the_nearest_double_to_the_real_value",
          float(a_pub) == float(a), f"|alpha - published| = {a_err:.3e}")

    rep["measured"]["high_precision"] = {
        "alpha_30_digits": str(+a)[:32],
        "KL_30_digits": str(+D)[:32],
        "published_alpha": PUBLISHED_ALPHA,
        "published_KL": PUBLISHED_KL,
        "KL_abs_error": f"{D_err:.4e}",
        "KL_rel_error": f"{D_err / D:.4e}",
        "KL_error_in_ULP": f"{D_err / ulp:.2f}",
        "KL_nearest_double_to_real_value": repr(nearest),
        "KL_last_reliable_significant_digit": 16,
        "note": (
            "The published KL literal is exactly what the stated float expression "
            "produces, so it is not a typo. It is 2.79 ULP from the real value "
            "because the expression accumulates rounding, so its 17th significant "
            "digit is wrong: the real value continues ...45938, the literal states "
            "...44. The subject's own assertion cannot detect this, because it "
            "compares that same float computation against the literal with a 1e-14 "
            "tolerance — a self-comparison. Nothing in the series depends on the "
            "17th digit; this is a precision-reporting defect, not a mathematical one."
        ),
    }

    # D must be strictly positive, which is what makes 1 - P_k decay at all;
    # it vanishes exactly when alpha = 1/2, i.e. at the m = 4 phase boundary.
    check("P05_KL_is_strictly_positive_because_alpha_exceeds_one_half",
          D > 0 and a > Decimal("0.5"))
    check("P05_KL_vanishes_exactly_at_alpha_one_half",
          abs(hp_kl(Decimal("0.5"))) < Decimal("1e-50"))

    # --- 2. the constant's role, on exact tails -----------------------------
    rows = []
    chernoff_ok = True
    for k in KS:
        u_max = exact_u_max(k)
        tail = exact_upper_tail(k, u_max)
        # Chernoff at the alpha threshold. Our tail starts above alpha*k, so it
        # is a subset of the event Chernoff bounds, and the inequality must hold.
        bound = (-D * k).exp()
        if not tail <= bound:
            chernoff_ok = False
        residual = -(tail.ln() + D * k)
        rows.append({
            "k": k,
            "exact_u_max": u_max,
            "one_minus_P_k": f"{tail:.6e}",
            "exp_minus_kD": f"{bound:.6e}",
            "residual": f"{residual:.6f}",
            "residual_over_ln_k": f"{residual / Decimal(k).ln():.6f}",
        })
    check("P05_KL_upper_bound_holds_on_every_exact_tail", chernoff_ok)

    # The Chernoff inequality carries a factor of several in headroom, so it
    # cannot notice a one-step error in the class boundary or a double-counted
    # tail term. Two direct pins, both added after the drill showed their absence:
    #
    #   (a) the exact boundary agrees with the independent floating route
    #       floor(k * ln2/ln3) — a different derivation, verified separately in
    #       the Paper 07 recheck;
    #   (b) the tail and the contracting fraction are exact complements. A tail
    #       that starts one term too early breaks this immediately.
    import math

    boundary_ok = complement_ok = True
    for k in KS:
        u_max = exact_u_max(k)
        if u_max != math.floor(math.log(2) / math.log(3) * k):
            boundary_ok = False
        head = sum(comb(k, u) for u in range(0, u_max + 1))
        if head + exact_tail_count(k, u_max) != 2 ** k:
            complement_ok = False
    check("P05_exact_class_boundary_agrees_with_the_independent_float_route", boundary_ok)
    check("P05_contracting_fraction_and_tail_are_exact_complements", complement_ok)

    # The sharp part. If D is the true rate, then
    #     residual = -(ln(1 - P_k) + k D)  =  (1/2) ln k + O(1)
    # so `residual - (1/2) ln k` stays inside a fixed window. If D were wrong by
    # any relative amount, that quantity would instead drift LINEARLY in k.
    #
    # The window is not tight, and deliberately so: the tail starts at
    # u_max + 1, and the fractional part of alpha*k oscillates, which puts an
    # O(1) wobble on the residual. Boundedness is the claim; smoothness is not.
    offsets = [Decimal(r["residual"]) - Decimal("0.5") * Decimal(r["k"]).ln() for r in rows]
    for r, o in zip(rows, offsets):
        r["residual_minus_half_ln_k"] = f"{o:.4f}"
    bounded = all(abs(o) < 2 for o in offsets)
    drift = abs(offsets[-1] - offsets[0])
    check("P05_KL_is_the_actual_decay_rate_of_the_non_contracting_fraction",
          bounded, f"offsets {[f'{o:.3f}' for o in offsets]}")
    check("P05_KL_rate_offset_does_not_drift_with_k",
          drift < 1, f"offset moved {drift:.3f} between k={KS[0]} and k={KS[-1]}")

    # Controls: a deliberately wrong D must break the rate test, at a range of
    # sizes. This is what makes the check above worth reading — it is shown to
    # be able to fail, and to fail harder as k grows.
    wrongs = {}
    for factor in ("1.02", "1.01", "1.001", "0.999"):
        D_wrong = D * Decimal(factor)
        row = {}
        for k in (KS[len(KS) // 2], KS[-1]):
            tail = exact_upper_tail(k, exact_u_max(k))
            off = -(tail.ln() + D_wrong * k) - Decimal("0.5") * Decimal(k).ln()
            row[str(k)] = f"{off:.3f}"
        row["rejected_at_k_max"] = abs(Decimal(row[str(KS[-1])])) >= 2
        wrongs[factor] = row
    check("P05_KL_rate_test_rejects_a_one_percent_wrong_constant",
          wrongs["1.01"]["rejected_at_k_max"] and wrongs["1.02"]["rejected_at_k_max"],
          f"offsets under wrong D: {wrongs}")

    # How sharp the test actually is, stated rather than implied. A relative
    # error eps in D displaces the offset by eps*D*k, so it clears the O(1)
    # window only once k is of order 2/(eps*D). At k = 8000 that resolves about
    # 0.7%; a 0.1% error is NOT detectable here, and is measured to confirm it.
    eps_resolved = Decimal(2) / (D * Decimal(KS[-1]))
    rep["stated_limits"].append({
        "limit": "sensitivity of the KL rate test",
        "at_k": KS[-1],
        "smallest_relative_error_in_D_this_resolves": f"{eps_resolved:.2%}",
        "formula": "a relative error eps needs k of order 2/(eps*D) to clear the O(1) window",
        "measured_non_detection": (
            f"a 0.1% wrong D gives offset {wrongs['1.001'][str(KS[-1])]} at k={KS[-1]}, "
            f"inside the window, so it is not rejected — as the formula predicts"
        ),
        "consequence": (
            "the rate test confirms D is the decay rate to about one part in a "
            "hundred; the 60-digit digit comparison is what pins it further"
        ),
    })

    rep["measured"]["exact_tail_rate"] = rows
    rep["measured"]["wrong_D_controls"] = wrongs

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
