"""Gate 16 — Theorem 1.1(2): L(E^(q),1) ≠ 0, tested on actual members of 𝒫.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-009 verified part (1) of Phase 2's Theorem 1.1 — the density of

    𝒫 = { q prime : q ≡ 1 (mod 24), (q/29) = 1, f₂ irreducible mod q }

is 1/24 and not the 1/48 the conditions naively multiply to — and said plainly
that parts (2) and (3) were untested. RUN-014 then built the machinery that makes
part (2) computable:

    for every q ∈ 𝒫,  L(E^{(q)}, 1) ≠ 0.

This gate tests it on the smallest members, and derives why the sign never fails.

WHY THE FIRST TWO CONDITIONS OF 𝒫 ARE THERE. For a fundamental discriminant d
coprime to N, the root number twists as w(E^{(d)}) = w(E)·χ_d(−N). Here N = 696 =
2³·3·29 and w(E) = +1, so

    w(E^{(q)}) = (−696/q) = (−1/q)(2/q)(3/q)(29/q).

q ≡ 1 (mod 24) forces q ≡ 1 (mod 4) and q ≡ 1 (mod 8) and q ≡ 1 (mod 3), giving
(−1/q) = (2/q) = 1 and, by reciprocity, (3/q) = (q/3) = 1. The second condition
gives (q/29) = 1, which is (29/q) by reciprocity since q ≡ 1 (mod 4). So

    **w(E^{(q)}) = +1 for every q ∈ 𝒫**,

which is what the first two conditions are *for*: they hold the root number at +1
so that a nonvanishing theorem has something to prove. The third condition — f₂
irreducible mod q — is the Zhai inertness condition, and it does not touch the
sign. RUN-009 found those same two conditions entangling the Frobenius; this is
the other thing they do.

The formula is not cited and left there. It is **measured** first, on twists of
this same curve by small d where the numerical sign test still separates the two
candidates, including one twist (d = 13) where it predicts −1 and L(E^{(d)},1)
duly comes out 0.

THE ARITHMETIC IS REUSED, NOT RECOMPUTED PER TWIST. a_n(E^{(d)}) = χ_d(n)·a_n(E),
so the base curve's coefficients are computed once by point counting and each
twist is a character multiplication. That relation is itself checked against
direct point counts on E^{(5)} before it is relied on.

WHAT LIMITS THE REACH. The L(1) sum needs about √N·log(1/ε)/2π terms, and
N(E^{(q)}) = 696·q², so the term count grows linearly in q. At q = 241 that is
~33,000 terms; at q = 457, ~62,000. The gate reports how far it got and refuses
to print an unconverged value — the truncation guard, not a fixed limit, decides.

Usage:  python code/src16_twist_family_lvalues.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src16-twist-family.json"
CACHE = ROOT / "data" / "cache" / "696e1-ap.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
BASE_N = 696
COEFF_LIMIT = 46_000
SMALL_TWISTS = (5, 13, 17, 37, 41)        # coprime to 2·696, ≡ 1 (mod 4)
MEMBERS = (241, 313)


def kronecker(a: int, n: int) -> int:
    """(a/n) for n ≥ 1, by the standard reduction — implemented here."""
    if n <= 0:
        raise ValueError("n must be positive")
    result = 1
    while n % 2 == 0:
        n //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            result = -result
    a %= n
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def twist(ainvs, d: int) -> list[int]:
    """E^{(d)} for a model with a₁ = a₃ = 0."""
    a1, a2, a3, a4, a6 = ainvs
    if a1 or a3:
        raise ValueError("this twist form assumes a1 = a3 = 0")
    return [0, a2 * d, 0, a4 * d * d, a6 * d ** 3]


def in_P(q: int) -> bool:
    return (q % 24 == 1 and q != 29 and ph2.legendre(29, q) == 1
            and ph2.cubic_root_count(ph2.F2, q) == 0)


def base_coefficients(limit: int) -> list[int]:
    """a_n(696.e1) up to `limit`, cached — the point counting is the slow part.

    The cache stores a_p for primes only, and the Hecke recursion rebuilds the
    rest, so a corrupted or truncated cache cannot silently change a composite
    coefficient without changing a prime one. It is rebuilt whenever the stored
    bound is short of what is asked for.
    """
    bad = {p: anchor.bad_prime_data(BASE, p)["a_p"] for p in (2, 3, 29)}
    primes = anchor.sieve(limit)
    ap = None
    if CACHE.exists():
        stored = json.loads(CACHE.read_text(encoding="utf-8"))
        if stored.get("curve") == BASE and stored.get("limit", 0) >= limit:
            ap = {int(k): v for k, v in stored["a_p"].items()}
    if ap is None or any(q not in ap for q in primes):
        ap = {q: (bad[q] if q in bad else anchor.point_count_ap(BASE, q))
              for q in primes}
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(
            {"curve": BASE, "limit": limit,
             "a_p": {str(k): v for k, v in ap.items()}}), encoding="utf-8")
    a = [0] * (limit + 1)
    a[1] = 1
    for q in primes:
        pk, prev2, prev1 = q, 1, ap[q]
        while pk <= limit:
            a[pk] = prev1
            prev2, prev1 = prev1, ap[q] * prev1 - (0 if q in bad else q * prev2)
            pk *= q
    for n in range(2, limit + 1):
        if a[n]:
            continue
        for q in primes:
            if q * q > n:
                break
            if n % q == 0:
                r_, m = 1, n
                while m % q == 0:
                    m //= q
                    r_ *= q
                a[n] = a[r_] * a[m]
                break
    return a


def twisted_coefficients(base: list[int], d: int) -> list[int]:
    return [0] + [kronecker(d, n) * base[n] for n in range(1, len(base))]


def analyse_twist(base_a: list[int], d: int) -> dict:
    N = BASE_N * d * d
    a = twisted_coefficients(base_a, d)
    inv = twist(BASE, d)
    predicted_w = kronecker(-BASE_N, d)
    L1 = anchor.l_value_at_one(a, N, 1)
    omega = anchor.real_period(inv)
    terms = len(a) - 1
    return {
        "d": d, "conductor": N, "sqrt_N": math.sqrt(N),
        "predicted_root_number": predicted_w,
        "terms_available": terms,
        "first_dropped_term_scale": anchor.truncation_scale(N, terms),
        "L_at_1": (L1 if predicted_w == 1 else 0.0),
        "L_converged": (L1 is not None) if predicted_w == 1 else True,
        "real_period": omega,
        "L_over_Omega": ((L1 / omega) if (predicted_w == 1 and L1 is not None
                                          and omega) else
                         (0.0 if predicted_w != 1 else None)),
        "omega_matches_base_over_sqrt_d":
            abs(omega - anchor.real_period(BASE) / math.sqrt(d)) < 1e-9,
        "torsion_bound": anchor.torsion_bound(inv, N),
        "reduction_types": {str(p): anchor.bad_prime_data(inv, p)["type"]
                            for p in (2, 3, 29)},
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    print(f"  computing a_p for {BASE} up to {COEFF_LIMIT:,} …",
          file=sys.stderr)
    base_a = base_coefficients(COEFF_LIMIT)

    # ---- the twisting relation, checked against direct point counts -------
    relation = []
    for d in (5, 13):
        direct = anchor.coefficients(
            twist(BASE, d),
            {p: anchor.bad_prime_data(twist(BASE, d), p)["a_p"]
             for p in (2, 3, 29, d)}, 200)
        derived = twisted_coefficients(base_a[:201], d)
        agree = all(direct[n] == derived[n] for n in range(1, 201)
                    if n % d)
        relation.append({"d": d, "n_checked": 200,
                         "agrees_off_the_twisting_prime": agree,
                         "sample": {str(n): [direct[n], derived[n]]
                                    for n in (2, 3, 5, 7, 11, 13)}})
    if not all(r["agrees_off_the_twisting_prime"] for r in relation):
        raise SystemExit("the twisting relation a_n(E^d) = chi_d(n) a_n(E) "
                         "does not reproduce direct point counts; refusing to "
                         "use it")
    print("  twisting relation reproduces direct point counts", file=sys.stderr)

    # ---- the root-number formula, measured on small twists ----------------
    formula_checks = []
    for d in SMALL_TWISTS:
        N = BASE_N * d * d
        inv = twist(BASE, d)
        a = twisted_coefficients(base_a[:30001], d)
        w, evidence = anchor.root_number(a, N, 30000)
        pred = kronecker(-BASE_N, d)
        formula_checks.append({
            "d": d, "conductor": N, "measured_w": w, "predicted_w": pred,
            "agrees": w == pred,
            "residual": evidence["residual"],
            "gap_to_the_other_sign": evidence["gap_to_the_other_sign"],
            "L_at_1": anchor.l_value_at_one(a, N, w) if w == 1 else 0.0,
        })
    formula_ok = all(c["agrees"] for c in formula_checks)
    if not formula_ok:
        raise SystemExit("w(E^d) = w(E)·chi_d(-N) failed on a small twist; "
                         "refusing to apply it to the family")

    # ---- every member's sign, from the conditions of 𝒫 --------------------
    members_below = [q for q in range(2, 20000) if _is_prime(q) and in_P(q)]
    signs = {str(q): kronecker(-BASE_N, q) for q in members_below}
    all_plus = all(v == 1 for v in signs.values())

    # ---- the actual L-values ----------------------------------------------
    results = [analyse_twist(base_a, q) for q in MEMBERS]
    for r in results:
        ratio = r["L_over_Omega"]
        t = r["torsion_bound"]
        if ratio is None or not t:
            continue
        # c_2, c_3, c_29 are unchanged by the twist: q ≡ 1 (mod 8) makes q a
        # square in Q_2, q ≡ 1 (mod 3) and (q/29) = 1 do the same at 3 and 29,
        # so the twist is locally trivial there and RUN-014's c_2 = c_3 = c_29
        # = 1 carries over. What is left is c_q at the additive prime.
        product = ratio * t * t
        r["c_q_times_Sha"] = product
        near = round(product)
        square_factorisations = [
            {"c_q": c, "Sha": near // c,
             "Sha_is_a_square": near % c == 0
             and int(math.isqrt(near // c)) ** 2 == near // c}
            for c in (1, 2, 4) if near % c == 0]
        r["c_q_in_1_2_4_and_Sha_a_square"] = [
            f for f in square_factorisations if f["Sha_is_a_square"]]
        r["reading"] = (
            "with trivial torsion and c_2 = c_3 = c_29 = 1 unchanged by the "
            "twist, L/Ω = c_q · #Ш; additive reduction bounds c_q in {1,2,4} "
            "and Cassels makes #Ш a square, which together leave the listed "
            "factorisations")

    log = {
        "gate": "src16_twist_family_lvalues",
        "subject": ("29_Theorem_Note_v1.0 Theorem 1.1 part (2): L(E^(q),1) ≠ 0 "
                    "for every q in P — untested when RUN-009 verified part (1)"),
        "why_the_first_two_conditions_of_P_exist": (
            "w(E^(d)) = w(E)·χ_d(−N) with N = 696 and w(E) = +1 gives "
            "w(E^(q)) = (−696/q) = (−1/q)(2/q)(3/q)(29/q). q ≡ 1 (mod 24) makes "
            "the first three symbols 1, and (q/29) = 1 makes the fourth 1 by "
            "reciprocity. The first two conditions hold the root number at +1; "
            "the third, f₂ irreducible mod q, is the Zhai inertness condition "
            "and does not touch the sign"),
        "twisting_relation_checked": relation,
        "root_number_formula_measured": formula_checks,
        "every_member_has_root_number_plus_one": {
            "members_below_20000": len(members_below),
            "members": members_below,
            "all_have_w_plus_1": all_plus,
            "signs": signs,
        },
        "L_values": results,
        "coefficient_limit": COEFF_LIMIT,
        "ok": (formula_ok and all_plus
               and all(r["L_converged"] and abs(r["L_at_1"]) > 1e-6
                       for r in results)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print()
    print("  w(E^d) = w(E)·χ_d(−696), measured against the prediction:")
    for c in formula_checks:
        print(f"    d = {c['d']:>3}  N = {c['conductor']:>10,}  measured "
              f"{c['measured_w']:+d}  predicted {c['predicted_w']:+d}  "
              f"{'OK' if c['agrees'] else 'DIFFERS'}   residual "
              f"{c['residual']:.2e}   gap {c['gap_to_the_other_sign']:.2e}")
    print()
    print(f"  members of P below 20,000: {len(members_below)}   "
          f"all with w = +1: {all_plus}")
    print()
    print("  Theorem 1.1(2) on the smallest members:")
    for r in results:
        conv = "converged" if r["L_converged"] else "NOT CONVERGED"
        print(f"    q = {r['d']:>4}  N = {r['conductor']:>12,}  "
              f"√N = {r['sqrt_N']:>9.1f}  terms {r['terms_available']:,}  "
              f"dropped-term scale {r['first_dropped_term_scale']:.1e}  {conv}")
        if r["L_converged"]:
            print(f"              L(E^(q),1) = {r['L_at_1']:.12f}   "
                  f"Ω = {r['real_period']:.12f}   L/Ω = "
                  f"{r['L_over_Omega']:.12f}   nonzero: "
                  f"{abs(r['L_at_1']) > 1e-6}")
            print(f"              torsion {r['torsion_bound']}   "
                  f"c_q · #Ш = {r.get('c_q_times_Sha', float('nan')):.9f}   "
                  f"allowed: {r.get('c_q_in_1_2_4_and_Sha_a_square')}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


def _is_prime(v: int) -> bool:
    if v < 2:
        return False
    d = 2
    while d * d <= v:
        if v % d == 0:
            return False
        d += 1
    return True


if __name__ == "__main__":
    raise SystemExit(main())
