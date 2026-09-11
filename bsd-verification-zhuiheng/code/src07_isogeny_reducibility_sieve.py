"""Gate 07 — the 5- and 7-isogeny columns, with p=3 as a control.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-006 closed the 3-isogeny half of the census's removal evidence and named
what it left: the 5- and 7-isogeny columns, 115 and 7 curves.

WHY p=3's METHOD DOES NOT GENERALISE. For n = 3 a Galois-stable subgroup is
{O, P, -P}, determined by the single value x(P), so stability is exactly
x(P) ∈ Q and the question reduces to a rational root of ψ₃. For n = 5 the
subgroup {O, ±P, ±2P} has four non-zero points and TWO distinct x-coordinates,
x(P) and x(2P); Galois need only preserve the SET. So an n-isogeny corresponds
to a degree-(n-1)/2 rational factor of ψ_n, not to a rational root — a
factorisation problem, not a root-finding one.

THE CRITERION USED INSTEAD. A rational n-isogeny makes the mod-n Galois
representation reducible, hence conjugate to upper-triangular. Then for every
prime p of good reduction with p ≠ n, the characteristic polynomial of Frobenius

    x² - a_p x + p

has a root mod n, which is to say **a_p² - 4p is a square mod n**.

Contrapositive, and exact:

    some good p with a_p² - 4p a non-residue mod n  ⟹  no rational n-isogeny.

One-sided, like RUN-006's sieve, and reported as such. Passing at every prime
tested is not evidence of an isogeny.

a_p is computed as p + 1 - #E(F_p), and #E(F_p) from Legendre symbols rather
than by counting pairs: for each x the equation is a quadratic in y with
discriminant (a₁x+a₃)² + 4(x³+a₂x²+a₄x+a₆), contributing 1 + χ(disc) points.
That is O(p) per prime instead of O(p²), and exact.

THE CONTROL, and it is the point of running n=3 at all. RUN-006 decided every
one of the 4,062 curves exactly. So this sieve's n=3 refutations must be a
SUBSET of the curves RUN-006 found to have no rational root. A single refutation
of a curve RUN-006 proved has an isogeny would mean this gate's criterion or
its arithmetic is wrong — and would have to be believed over the sieve, not
over the exact result.

Usage:  python code/src07_isogeny_reducibility_sieve.py
"""

from __future__ import annotations

import collections
import csv
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
import census_pkg                                          # noqa: E402

PKG = census_pkg.PKG
CENSUS = PKG / "results" / "algorithm1_removed_census.csv"
ARITH = PKG / "inputs" / "metadata" / "old_base_curve_arithmetic.json"
PRIOR = ROOT / "data" / "gate-logs" / "src06-three-isogeny-sieve.json"
OUT = ROOT / "data" / "gate-logs" / "src07-isogeny-reducibility.json"

TEST_PRIMES = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
               61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
NS = (3, 5, 7)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def divides_discriminant(ainvs: list[int], p: int) -> bool:
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return disc % p == 0


def a_p(ainvs: list[int], p: int) -> int | None:
    """Trace of Frobenius at p, or None where the reduction is singular.

    The singular case is decided by the discriminant, not by Hasse. An earlier
    version of this function returned None when |a_p|² > 4p, with a comment
    saying "a singular reduction shows up as a count that Hasse cannot
    accommodate." **That comment was false and the branch was dead.** At a
    prime of bad reduction a_p is 0 or ±1 — split multiplicative +1, non-split
    −1, additive 0 — which satisfies |a_p| ≤ 2√p for every p ≥ 1. The guard
    could never fire, so it never distinguished anything.

    RUN-007's verdicts are unaffected: its caller filters bad primes with
    divides_discriminant() before ever reaching here, so the dead guard was
    never load-bearing. It is replaced by the condition it was pretending to
    be, which the drill now exercises at a bad prime.
    """
    if divides_discriminant(ainvs, p):
        return None
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    total = 1                                   # point at infinity
    for x in range(p):
        d = ((a1 * x + a3) ** 2 + 4 * (x * x * x + a2 * x * x + a4 * x + a6)) % p
        total += 1 + legendre(d, p)
    return p + 1 - total


def is_square_mod(a: int, n: int) -> bool:
    a %= n
    return any((r * r) % n == a for r in range(n))


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

    # RUN-006's exact answer for n = 3, used only as a control.
    exact3 = None
    if PRIOR.exists():
        prior = json.loads(PRIOR.read_text(encoding="utf-8"))
        if prior.get("counts", {}).get("EXACT_disagrees_with_the_package") == 0 \
                and prior.get("counts", {}).get("REFUTED_package_says_true_but_no_rational_root") == 0:
            exact3 = {r["curve_label"]: r["has_isogeny_3"].strip().lower() == "true"
                      for r in rows}

    result = {n: {"refuted": [], "unresolved": [], "agree_false": [],
                  "contradicts_claim": []} for n in NS}
    witness = {n: collections.Counter() for n in NS}
    control_violations = []

    for r in rows:
        label = r["curve_label"]
        inv = ainvs.get(label)
        if inv is None:
            continue
        claims = {3: r["has_isogeny_3"].strip().lower() == "true",
                  5: r["has_isogeny_5"].strip().lower() == "true",
                  7: r["has_isogeny_7"].strip().lower() == "true"}
        pending = {n for n in NS}
        for p in TEST_PRIMES:
            if not pending:
                break
            if divides_discriminant(inv, p):
                continue
            ap = a_p(inv, p)
            if ap is None:
                continue
            d = ap * ap - 4 * p
            for n in sorted(pending):
                if p == n:
                    continue
                if not is_square_mod(d, n):
                    witness[n][p] += 1
                    pending.discard(n)
                    if claims[n]:
                        result[n]["contradicts_claim"].append(
                            {"label": label, "prime": p, "a_p": ap,
                             "a_p^2-4p mod n": d % n})
                    else:
                        result[n]["agree_false"].append(label)
                    result[n]["refuted"].append(label)
        for n in pending:
            result[n]["unresolved"].append({"label": label,
                                            "package_says": claims[n]})

    # Control: every n=3 refutation must be a curve RUN-006 proved has no
    # rational root. A refutation of a proven isogeny indicts this gate.
    if exact3 is not None:
        for label in result[3]["refuted"]:
            if exact3.get(label):
                control_violations.append(label)

    counts = {}
    for n in NS:
        claims_true = sum(1 for r in rows
                          if r[f"has_isogeny_{n}"].strip().lower() == "true")
        counts[f"n={n}"] = {
            "package_says_true": claims_true,
            "refuted_by_a_prime": len(result[n]["refuted"]),
            "of_those_contradicting_the_package": len(result[n]["contradicts_claim"]),
            "confirmed_false": len(result[n]["agree_false"]),
            "unresolved": len(result[n]["unresolved"]),
            "unresolved_that_package_calls_false": sum(
                1 for u in result[n]["unresolved"] if not u["package_says"]),
        }

    log = {
        "gate": "src07_isogeny_reducibility_sieve",
        "criterion": (
            "a rational n-isogeny makes the mod-n representation reducible, so "
            "x² - a_p x + p has a root mod n for every good p ≠ n, i.e. "
            "a_p² - 4p is a square mod n"),
        "one_sided": (
            "a non-residue at some good prime refutes; passing everywhere is "
            "NOT evidence of an isogeny and is reported unresolved"),
        "why_not_psi_n_roots": (
            "for n ≥ 5 an order-n subgroup has (n-1)/2 distinct x-coordinates "
            "and Galois need only preserve the set, so an isogeny is a "
            "degree-(n-1)/2 rational FACTOR of ψ_n, not a rational root. "
            "RUN-006's method is special to n = 3"),
        "primes_tested": TEST_PRIMES,
        "counts": counts,
        "control_n3_against_RUN006": {
            "ran": exact3 is not None,
            "violations": control_violations,
            "meaning": (
                "RUN-006 decided all 4,062 curves exactly. Any curve refuted "
                "here that RUN-006 proved has a rational 3-isogeny would indict "
                "this gate's criterion or its arithmetic, not the package."),
        },
        "contradicting_the_package": {
            f"n={n}": result[n]["contradicts_claim"][:20] for n in NS},
        "witness_prime_distribution": {
            f"n={n}": {str(k): v for k, v in sorted(witness[n].items())}
            for n in NS},
        "unresolved_sample": {
            f"n={n}": result[n]["unresolved"][:5] for n in NS},
        "ok": (not control_violations
               and all(not result[n]["contradicts_claim"] for n in NS)),
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    for n in NS:
        c = counts[f"n={n}"]
        print(f"  n = {n}")
        print(f"    package says true              : {c['package_says_true']:>6,}")
        print(f"    refuted by a prime             : {c['refuted_by_a_prime']:>6,}"
              f"   contradicting the package: {c['of_those_contradicting_the_package']}")
        print(f"    unresolved                     : {c['unresolved']:>6,}"
              f"   of which package says false: {c['unresolved_that_package_calls_false']}")
    print()
    ctl = log["control_n3_against_RUN006"]
    print(f"  control against RUN-006 (n=3) ran: {ctl['ran']}   "
          f"violations: {len(ctl['violations'])}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
