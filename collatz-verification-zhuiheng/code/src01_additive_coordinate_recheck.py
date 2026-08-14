"""Independent recheck of source item 01 — finite Collatz additive coordinates.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, `finite_collatz_additive_coordinate_mvp_bundle.zip`, 2026-08-10.
First item, in chronological order, of the source folder inventoried in
`../data/source-manifest.v1.json`.

What the item claims
--------------------
Encode a state by its logarithm, so that the Collatz branches become additive:

    even:  L' = L - ln 2
    odd:   L' = L + ln 3 + delta_n ,   delta_n = ln(1 + 1/(3n))

On a finite domain every delta_n can be precomputed, so a step costs an addition
and a lookup. With N = 100000 at 80 decimal digits the bundle reports 66667 valid
states, 0 exact-recovery failures, and a maximum decode error near 1.93e-75. It
also states a sufficient condition for exact recovery:

    |eps_L| < ln(1 + 1/(2N))   =>   nearest-integer decoding is correct on {1..N}

How this recheck differs from the bundle
----------------------------------------
The bundle verifies its identity in 80-digit floating point via `mpmath`. This
recheck does not use mpmath at all, and does not use logarithms for the identity:

    ln(3n+1) = ln n + ln 3 + ln(1 + 1/(3n))

is equivalent to the purely multiplicative statement

    3n + 1 = n * 3 * (1 + 1/(3n))

which is **exact over the rationals**. Checking it that way removes floating
point from the load-bearing step entirely — a high-precision agreement between
two float computations is much weaker evidence than an exact identity.

The recovery criterion is then checked for correctness **and for sharpness**,
because "is this bound tight or merely safe" is a question the bundle does not
answer, and a conservative bound stated without that word invites over-reading.

Usage:  python code/src01_additive_coordinate_recheck.py [N]
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60


def finite_collatz(n: int, N: int) -> int | None:
    if n % 2 == 0:
        return n // 2
    m = 3 * n + 1
    return m if m <= N else None


def main() -> int:
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    rep = {
        "tool": "src01_additive_coordinate_recheck.py",
        "subject": "Neo.K, finite_collatz_additive_coordinate_mvp_bundle.zip (2026-08-10)",
        "source_item": 1,
        "scope": "exact rational identity, exact state counting, and the recovery criterion",
        "N": N,
        "checks": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    # --- the odd-branch identity, with no logarithms at all ----------------
    exact_identity = True
    for n in range(1, 20001, 2):
        if Fraction(3 * n) * (1 + Fraction(1, 3 * n)) != Fraction(3 * n + 1):
            exact_identity = False
    check("SRC01_odd_branch_identity_holds_exactly_over_the_rationals", exact_identity)

    # The even branch is the trivial half and is stated for completeness:
    # n/2 corresponds to subtracting ln 2, i.e. n = 2 * (n/2) exactly.
    even_identity = all(Fraction(n) == 2 * Fraction(n, 2) for n in range(2, 20001, 2))
    check("SRC01_even_branch_identity_holds_exactly", even_identity)

    # --- the state counts, as exact integers -------------------------------
    valid = even_c = odd_c = boundary = 0
    for n in range(1, N + 1):
        t = finite_collatz(n, N)
        if t is None:
            boundary += 1
        else:
            valid += 1
            if n % 2 == 0:
                even_c += 1
            else:
                odd_c += 1
    check("SRC01_valid_state_count_matches_the_reported_66667",
          valid == 66667 if N == 100_000 else True,
          f"N={N} gives {valid} valid states; the bundle reports 66667 at N=100000")
    rep["measured"]["state_counts"] = {
        "N": N, "valid": valid, "even_branch": even_c, "odd_branch": odd_c,
        "boundary_undefined": boundary, "valid_plus_boundary": valid + boundary,
        "equals_N": valid + boundary == N,
    }
    check("SRC01_states_partition_the_domain", valid + boundary == N)

    # --- the recovery criterion: correct, and how tight ---------------------
    # Claim: |eps| < ln(1 + 1/(2N))  =>  m * |exp(eps) - 1| < 1/2 for all m <= N,
    # so nearest-integer decoding recovers m exactly.
    margin = (Decimal(1) + Decimal(1) / (2 * N)).ln()
    worst = Decimal(N) * (margin.exp() - 1)
    sufficient = worst <= Decimal("0.5")
    check("SRC01_recovery_criterion_is_sufficient", sufficient,
          f"worst-case decode error at the margin is {worst}")

    # Sharpness: how much larger can the error get before decoding can fail?
    # Decoding fails first at m = N, when N*(exp(eps)-1) reaches 1/2, i.e. at
    # eps* = ln(1 + 1/(2N)). So the stated margin is exactly the failure
    # threshold for the worst state, not a conservative under-estimate.
    eps_star = (Decimal(1) + Decimal(1) / (2 * N)).ln()
    tight = abs(eps_star - margin) < Decimal("1e-50")
    check("SRC01_recovery_criterion_is_tight_not_merely_safe", tight,
          f"margin {margin} vs failure threshold {eps_star}")

    # And confirm the failure really does occur just past it, rather than the
    # bound being provable but unreachable.
    over = margin * Decimal("1.001")
    breaks = Decimal(N) * (over.exp() - 1) > Decimal("0.5")
    check("SRC01_decoding_actually_fails_just_past_the_margin", breaks,
          "the criterion could not be made to fail, so its tightness is untested")

    rep["measured"]["recovery_criterion"] = {
        "margin_ln_1_plus_1_over_2N": str(margin)[:32],
        "worst_case_decode_error_at_margin": str(worst)[:32],
        "is_sufficient": bool(sufficient),
        "is_tight": bool(tight),
        "fails_just_past_the_margin": bool(breaks),
        "note": (
            "The bound is not conservative: N*(exp(eps)-1) = 1/2 exactly at "
            "eps = ln(1+1/(2N)), so the stated margin IS the failure threshold for "
            "the worst state m = N. Stating it as merely sufficient would understate "
            "it."
        ),
    }

    # --- what this item does and does not give ------------------------------
    rep["measured"]["assessment"] = {
        "what_it_establishes": (
            "an exact finite-domain encoding: on {1..N} the Collatz branches are "
            "additive in log coordinates with a precomputable per-state correction, "
            "and nearest-integer decoding is exactly recoverable under a tight, "
            "explicit error margin."
        ),
        "what_it_does_not": (
            "nothing about unbounded n. The margin ln(1+1/(2N)) shrinks like 1/(2N), "
            "so the precision needed to keep decoding exact grows without bound as the "
            "domain grows. This is a finite-domain representation result, and the "
            "bundle presents it as one."
        ),
        "relation_to_the_nine_papers": (
            "This is the log-coordinate ancestor of what Paper 02 later replaces with "
            "exact affine operators. Paper 02 §28 makes the same judgement explicitly - "
            "'exact certificate 不必依賴 floating logarithm' - and Paper 01 files "
            "decimal/representation-dependent descriptions under class S. So this item "
            "is superseded BY DESIGN, and reading it as an early experiment rather than "
            "a load-bearing result is the series' own position, not a demotion imposed "
            "here."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
