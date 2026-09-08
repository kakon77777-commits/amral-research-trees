"""Gate 06 — test the census's 3-isogeny column, one-sidedly and exactly.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-005 verified the arithmetic half of the census's removal accounting and
stated the gap it left: the 3/5/7-isogeny determinations were read from the
package, not recomputed. This gate closes part of that, for p = 3.

THE CRITERION. E/Q has a rational 3-isogeny iff it has a Galois-stable subgroup
C of order 3. Writing C = {O, P, -P}, stability is equivalent to σP ∈ {P, -P}
for every σ, which is equivalent to x(P) being Galois-fixed, i.e. x(P) ∈ Q. And
x(P) is a root of the 3-division polynomial

    ψ₃(x) = 3x⁴ + b₂x³ + 3b₄x² + 3b₆x + b₈.

So **E has a rational 3-isogeny ⟺ ψ₃ has a rational root.**

WHY THIS IS A SIEVE AND NOT A DECISION. Finding rational roots exactly would
need the divisors of b₈, and |b₈| here reaches 26 digits — not feasible for
4,062 curves. But one direction is cheap and exact. A rational root has
denominator dividing the leading coefficient 3, so for every prime p ≠ 3 it
reduces to a root of ψ₃ in F_p. Contrapositive:

    ψ₃ has no root mod p for some p ≠ 3  ⟹  no rational root  ⟹  no 3-isogeny.

That gives three verdicts, and the third is a real one:

  REFUTED   the package says `has_isogeny_3 = True`, and some prime witnesses
            that ψ₃ has no rational root. The package would be wrong.
  CONFIRMED the package says False, and a prime witnesses it.
  UNRESOLVED ψ₃ has roots modulo every prime tested. Says nothing either way —
            reported as unresolved, never as agreement.

A curve passing the sieve at every prime is NOT evidence of an isogeny: quartics
with roots modulo every prime and none over Q exist. Reporting UNRESOLVED as
support would be the failure this arm exists to catch, so the counts are kept
apart and the gate's verdict depends only on REFUTED being empty.

Usage:  python code/src06_three_isogeny_sieve.py
"""

from __future__ import annotations

import collections
import csv
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = (pathlib.Path("D:/我的研究/學術討論/論文/數學/BSD")
       / "BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12")
CENSUS = PKG / "results" / "algorithm1_removed_census.csv"
ARITH = PKG / "inputs" / "metadata" / "old_base_curve_arithmetic.json"
OUT = ROOT / "data" / "gate-logs" / "src06-three-isogeny-sieve.json"

PRIMES = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]


def psi3_coeffs(a1: int, a2: int, a3: int, a4: int, a6: int) -> list[int]:
    """[c0, c1, c2, c3, c4] of ψ₃ = 3x⁴ + b₂x³ + 3b₄x² + 3b₆x + b₈."""
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return [b8, 3 * b6, 3 * b4, b2, 3]


def has_root_mod(coeffs: list[int], p: int) -> bool:
    c = [x % p for x in coeffs]
    for x in range(p):
        v = 0
        for k in range(len(c) - 1, -1, -1):
            v = (v * x + c[k]) % p
        if v == 0:
            return True
    return False



def divisors_within_budget(n: int, budget: int = 2_000_000) -> list[int] | None:
    """All positive divisors of |n|, or None if trial division exceeds budget.

    Returning None rather than a partial list matters: a truncated divisor set
    would let a curve WITH a rational root be reported as having none, turning
    an unfinished computation into a false refutation.
    """
    n = abs(n)
    if n == 0:
        return None                      # handled separately: x = 0 is a root
    fac, d, rem = {}, 2, n
    while d * d <= rem:
        if d > budget:
            return None
        while rem % d == 0:
            fac[d] = fac.get(d, 0) + 1
            rem //= d
        d += 1 if d == 2 else 2
    if rem > 1:
        fac[rem] = fac.get(rem, 0) + 1
    divs = [1]
    for q, e in fac.items():
        divs = [x * q ** k for x in divs for k in range(e + 1)]
    return sorted(divs)


def rational_root_exists(coeffs: list[int]) -> bool | None:
    """True/False if decidable within budget, else None (undecided).

    coeffs is [c0..c4] of psi3; a rational root u/v in lowest terms has
    v | 3 (the leading coefficient) and u | c0.
    """
    c0 = coeffs[0]
    if c0 == 0:
        return True                      # x = 0 is a root
    divs = divisors_within_budget(c0)
    if divs is None:
        return None
    from fractions import Fraction
    for u in divs:
        for su in (u, -u):
            for v in (1, 3):
                x = Fraction(su, v)
                val = sum(Fraction(c) * x ** k for k, c in enumerate(coeffs))
                if val == 0:
                    return True
    return False



def rational_root_by_monic_scan(coeffs: list[int]) -> bool:
    """Decide a rational root without factoring, exactly.

    Substituting y = 3x turns psi3 into a MONIC integer quartic

        y^4 + b2 y^3 + 9 b4 y^2 + 27 b6 y + 27 b8,

    so any rational root is an integer, and integers are bounded by a
    Cauchy-type bound. Candidates are then cut by allowed residues modulo small
    primes before any big-integer evaluation — on the one curve that reached
    this path, 3.2 million candidates fell to 2.

    Every arithmetic step is on Python ints. A float pass was tried first and
    was WRONG: with coefficients near 1e21 it reported one real root where a
    quartic with positive leading coefficient must have an even number, and
    found no rational root on a curve that has one at x = 163100.
    """
    b8, c1, c2, b2, _ = coeffs           # coeffs = [b8, 3b6, 3b4, b2, 3]
    mono = [27 * b8, 9 * c1, 3 * c2, b2, 1]  # 27b8, 27b6=9*(3b6), 9b4=3*(3b4)

    bound = 0
    for i, c in enumerate(mono[:4]):
        if c:
            bound = max(bound, 2 * int(abs(c) ** (1.0 / (4 - i))) + 2)

    allowed = []
    for q in (5, 7, 11, 13, 17, 19, 23):
        cq = [c % q for c in mono]
        allowed.append((q, {r for r in range(q)
                            if sum(cq[k] * pow(r, k, q) for k in range(5)) % q == 0}))
    if any(not ok for _, ok in allowed):
        return False                     # no residue anywhere: no integer root

    for y in range(-bound, bound + 1):
        if any(y % q not in ok for q, ok in allowed):
            continue
        v = 0
        for c in reversed(mono):
            v = v * y + c
        if v == 0:
            return True
    return False


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (CENSUS, ARITH):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")

    ainvs = {r["curve_label"]: r["ainvs"]
             for r in json.loads(ARITH.read_text(encoding="utf-8"))["records"]}
    rows = list(csv.DictReader(CENSUS.open(encoding="utf-8")))

    refuted, confirmed, unresolved = [], [], []
    exact_agree, exact_disagree, fell_back = [], [], []
    verdict_by_claim = collections.Counter()
    witness_prime = collections.Counter()

    for r in rows:
        label = r["curve_label"]
        inv = ainvs.get(label)
        if inv is None:
            continue
        claim = r["has_isogeny_3"].strip().lower() == "true"
        coeffs = psi3_coeffs(*inv)

        witness = None
        for p in PRIMES:
            if not has_root_mod(coeffs, p):
                witness = p
                break

        if witness is None:
            # The sieve could not decide. Try to settle it exactly, which is
            # feasible whenever b8 factors within budget.
            exact = rational_root_exists(coeffs)
            if exact is None:
                # b8 did not factor within budget. Fall back to the monic
                # substitution, which needs no factorisation at all.
                exact = rational_root_by_monic_scan(coeffs)
                fell_back.append(label)
            if False:
                pass
            elif exact == claim:
                exact_agree.append(label)
                verdict_by_claim[(claim, "EXACT_AGREES")] += 1
            else:
                exact_disagree.append({"label": label, "package_says": claim,
                                       "rational_root_exists": exact})
                verdict_by_claim[(claim, "EXACT_DISAGREES")] += 1
        else:
            witness_prime[witness] += 1
            if claim:
                refuted.append({"label": label, "package_says": True,
                                "witness_prime": witness,
                                "psi3_has_no_root_mod": witness})
                verdict_by_claim[(claim, "REFUTED")] += 1
            else:
                confirmed.append({"label": label, "witness_prime": witness})
                verdict_by_claim[(claim, "CONFIRMED")] += 1

    claims_true = sum(1 for r in rows
                      if r["has_isogeny_3"].strip().lower() == "true")
    log = {
        "gate": "src06_three_isogeny_sieve",
        "criterion": ("E/Q has a rational 3-isogeny iff ψ₃ has a rational root; "
                      "a rational root has denominator dividing the leading "
                      "coefficient 3, so it reduces mod every prime p ≠ 3"),
        "one_sided": (
            "no root mod some p ⇒ no rational root ⇒ no 3-isogeny. The converse "
            "does NOT hold: a quartic can have roots modulo every prime and none "
            "over Q, so passing the sieve everywhere is not evidence of an "
            "isogeny and is reported as UNRESOLVED, never as agreement."),
        "primes_tested": PRIMES,
        "counts": {
            "curves_tested": len(rows),
            "package_says_has_isogeny_3": claims_true,
            "REFUTED_package_says_true_but_no_rational_root": len(refuted),
            "CONFIRMED_package_says_false_and_a_prime_witnesses_it": len(confirmed),
            "EXACT_agrees_with_the_package": len(exact_agree),
            "EXACT_disagrees_with_the_package": len(exact_disagree),
            "decided_by_monic_scan_after_factoring_failed": len(fell_back),
            "UNRESOLVED_still_undecided": len(unresolved),
        },
        "verdict_by_claim": {f"package_says_{c}/{v}": n
                             for (c, v), n in sorted(
                                 verdict_by_claim.items(),
                                 key=lambda kv: (str(kv[0][0]), kv[0][1]))},
        "witness_prime_distribution": {str(k): v for k, v in
                                       sorted(witness_prime.items())},
        "REFUTED": refuted[:50],
        "EXACT_disagreements": exact_disagree[:50],
        "curves_needing_the_monic_fallback": fell_back,
        "exact_method": (
            "for curves the sieve could not decide, rational roots are found "
            "exactly: u/v with v | 3 and u | b8, enumerated from a full "
            "factorisation of b8. If trial division exceeds budget the routine "
            "returns undecided rather than a partial divisor set — a truncated "
            "set would turn an unfinished computation into a false refutation."),
        "unresolved_sample": unresolved[:10],
        "what_unresolved_means": (
            "this gate could not decide. Every UNRESOLVED curve the package "
            "calls True remains read-from-the-package, exactly as before this "
            "gate ran — the gap is narrowed, not closed."),
        "ok": len(refuted) == 0 and len(exact_disagree) == 0,
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    c = log["counts"]
    print(f"  curves tested                       : {c['curves_tested']:>6,}")
    print(f"  package says has_isogeny_3 = True   : {c['package_says_has_isogeny_3']:>6,}")
    print()
    print(f"  REFUTED   (says True, no rational root) : {c['REFUTED_package_says_true_but_no_rational_root']:>6,}")
    print(f"  CONFIRMED (says False, prime witnesses) : {c['CONFIRMED_package_says_false_and_a_prime_witnesses_it']:>6,}")
    print(f"  EXACT agrees with the package           : {c['EXACT_agrees_with_the_package']:>6,}")
    print(f"  EXACT disagrees                         : {c['EXACT_disagrees_with_the_package']:>6,}")
    print(f"  decided by the monic fallback           : {c['decided_by_monic_scan_after_factoring_failed']:>6,}")
    print(f"  UNRESOLVED (still undecided)            : {c['UNRESOLVED_still_undecided']:>6,}")
    print()
    for k, v in log["verdict_by_claim"].items():
        print(f"    {k:<34} {v:>6,}")
    if refuted:
        print()
        print("  REFUTED curves:")
        for x in refuted[:20]:
            print(f"    {x['label']}  ψ₃ has no root mod {x['witness_prime']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
