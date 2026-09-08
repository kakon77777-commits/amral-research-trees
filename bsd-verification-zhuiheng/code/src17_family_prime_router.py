"""Gate 17 — the family's "automatic ordinary" claim and the all-prime router's exhaustion.

數學戰士「墜衡」 / AMRAL Research Lab.

`16_696e1_Chebotarev_Support` derives something the third condition of 𝒫 gets
for free, and states it as a boxed claim:

    q inert in the cubic field ⟺ Frob_q is an order-3 element of
    GL₂(F₂) ≅ S₃, whose characteristic polynomial X² + X + 1 has trace 1, so
    a_q(E) is **odd**. If q ≥ 5 were supersingular then q | a_q, and Hasse
    forces a_q = 0, contradicting oddness. Hence q ∈ 𝒫 ⟹ q is good ordinary.

That argument is exactly checkable, and so is the thing it needs to be worth
anything: **a_q is not odd for most primes.** If a_q were odd everywhere the
derivation would be true and empty. The mod-2 image here is all of S₃ (f₂ is
irreducible with non-square discriminant), so Chebotarev predicts odd a_q at
density 2/6 = 1/3 — the gate measures that rather than assuming it.

It also checks the document's one explicit number, a_241(E) = −7, and the
residue claim 241 ≡ 9 (mod 29) with 9 a square.

`17_696e1_All_Prime_Router` then closes with an exhaustion claim: for E_q the
odd primes are exactly

    p = q (additive) | multiplicative at 3 and 29 | good ordinary | good
    supersingular,

"四類已覆蓋，所以 prime router 沒有遺漏 branch". That is a partition assertion
about every odd prime, and this gate classifies them directly for the first
member q = 241 and checks each falls in exactly one class.

Finally, `17` asserts that E_q carries no rational prime-degree isogeny. RUN-007's
X₀(n) machinery decides that for n = 2, 3, 5, 7 — and only those. Mazur's theorem
allows prime degrees 2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163, so this gate
closes four of twelve and says which eight it does not reach rather than reporting
a partial check as a whole one.

Usage:  python code/src17_family_prime_router.py
"""

from __future__ import annotations

import collections
import json
import math
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src17-family-router.json"

BASE = [0, 1, 0, 8, -16]
BASE_N = 696
FIRST_MEMBER = 241
PRIME_SCAN = 20_000
ROUTER_SCAN = 3_000
REDUNDANCY_SCAN = 200_000
MAZUR_DEGREES = (2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163)
COVERED = (2, 3, 5, 7)


def a_p_of(ainvs, p: int) -> int:
    return p + 1 - anchor.point_count(ainvs, p)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    # reuse gate 16's cached a_p for the base curve rather than recounting
    base_a = fam.base_coefficients(PRIME_SCAN)
    primes = [p for p in anchor.sieve(PRIME_SCAN) if p > 3]

    # ---- the parity of a_p, and whether the claim is vacuous ---------------
    parity = collections.Counter()
    in_family, violations = [], []
    for p in primes:
        if BASE_N % p == 0:
            continue
        ap = base_a[p]
        odd = ap % 2 != 0
        inert = ph2.cubic_root_count(ph2.F2, p) == 0
        parity[(inert, odd)] += 1
        if inert != odd and len(violations) < 20:
            violations.append({"p": p, "a_p": ap, "f2_irreducible": inert,
                               "a_p_odd": odd})
        if ph2.in_P(p) if hasattr(ph2, "in_P") else fam.in_P(p):
            supersingular = ap % p == 0
            in_family.append({"q": p, "a_q": ap, "a_q_odd": odd,
                              "ordinary": not supersingular})

    odd_total = sum(v for (_i, o), v in parity.items() if o)
    tested = sum(parity.values())
    equivalence_holds = all(i == o for (i, o) in parity)

    automatic_ordinary = {
        "claim": ("q ∈ 𝒫 ⟹ a_q(E) is odd ⟹ q is good ordinary for E"),
        "primes_tested": tested,
        "a_p_odd_exactly_when_f2_is_irreducible": equivalence_holds,
        "counterexamples": violations,
        "density_of_odd_a_p": odd_total / tested if tested else None,
        "chebotarev_prediction": 1 / 3,
        "why_that_matters": (
            "if a_p were odd for every p the derivation would be true and "
            "empty; the mod-2 image is all of S₃, so odd a_p has density 1/3 "
            "and the condition is doing real work"),
        "members_of_P_below_scan": len(in_family),
        "all_members_have_odd_a_q": all(m["a_q_odd"] for m in in_family),
        "all_members_are_ordinary": all(m["ordinary"] for m in in_family),
        "members": in_family[:30],
    }

    # ---- is 𝒫's second condition independent of its other two? ------------
    #
    # f₂ irreducible mod q puts Frobenius in A₃, so (disc(f₂)/q) = 1. RUN-009
    # established that disc(f₂) has squarefree part −174 = (−6)·29 and that
    # q ≡ 1 (mod 24) already forces (−6/q) = 1. Together those give (29/q) = 1
    # without the second condition being stated at all. Measured rather than
    # left as an argument.
    cross = collections.Counter()
    stray = []
    for q in anchor.sieve(REDUNDANCY_SCAN):
        if q % 24 != 1 or q == 29:
            continue
        irr = ph2.cubic_root_count(ph2.F2, q) == 0
        res = ph2.legendre(29, q) == 1
        cross[(irr, res)] += 1
        if irr and not res and len(stray) < 20:
            stray.append(q)
    tot = sum(cross.values())
    redundancy = {
        "claim": ("𝒫's condition (q/29) = 1 is implied by q ≡ 1 (mod 24) "
                  "together with f₂ irreducible mod q"),
        "derivation": ("f₂ irreducible ⟹ Frobenius is a 3-cycle ⟹ Frob ∈ A₃ ⟹ "
                       "(disc(f₂)/q) = 1; squarefree part of disc(f₂) is "
                       "−174 = (−6)·29 and q ≡ 1 (mod 24) gives (−6/q) = 1, so "
                       "(29/q) = 1"),
        "primes_q_equiv_1_mod_24_below": REDUNDANCY_SCAN,
        "cross_tabulation": {f"f2_irreducible={i}, (q/29)=1 is {r}": v
                             for (i, r), v in sorted(cross.items())},
        "irreducible_but_non_residue": cross[(True, False)],
        "counterexamples": stray,
        "condition_is_redundant": cross[(True, False)] == 0,
        "P_f2_irreducible_given_first_condition":
            (cross[(True, True)] + cross[(True, False)]) / tot if tot else None,
        "consequence_for_the_density": (
            "RUN-009 read δ(𝒫) = (1/8)·(1/2)·(2/3); with the redundancy the "
            "same number is (1/8)·(1/3), where the 1/3 already contains the "
            "1/2 that the second condition was supplying. The density is "
            "unchanged and the derivation is one step shorter"),
        "not_an_error": ("the set 𝒫 is the same either way — the theorem states "
                         "three conditions where two determine the set"),
    }

    # ---- the document's explicit numbers -----------------------------------
    a241 = base_a[FIRST_MEMBER]
    explicit = {
        "document_states_a_241": -7,
        "recomputed_a_241": a241,
        "agrees": a241 == -7,
        "241_mod_24": FIRST_MEMBER % 24,
        "241_mod_29": FIRST_MEMBER % 29,
        "241_mod_29_is_a_square": ph2.legendre(FIRST_MEMBER, 29) == 1,
        "f2_irreducible_mod_241": ph2.cubic_root_count(ph2.F2, FIRST_MEMBER) == 0,
        "241_is_in_P": fam.in_P(FIRST_MEMBER),
    }

    # ---- the all-prime router's exhaustion, for E_q with q = 241 -----------
    q = FIRST_MEMBER
    twisted = fam.twist(BASE, q)
    Nq = BASE_N * q * q
    classes = collections.Counter()
    unclassified = []
    for p in anchor.sieve(ROUTER_SCAN):
        if p == 2:
            continue                       # the router is stated for odd p
        if p == q:
            classes["p = q, additive"] += 1
            continue
        if p in (3, 29):
            d = anchor.bad_prime_data(twisted, p)
            if d["type"].endswith("multiplicative"):
                classes[f"multiplicative at {p}"] += 1
            else:
                unclassified.append({"p": p, "type": d["type"]})
            continue
        ap = a_p_of(twisted, p)
        if ap % p == 0:
            classes["good supersingular"] += 1
        else:
            classes["good ordinary"] += 1
    total_odd = sum(classes.values())
    router = {
        "curve": f"E^({q})", "conductor": Nq,
        "odd_primes_below": ROUTER_SCAN,
        "classes": dict(classes),
        "total_classified": total_odd,
        "unclassified": unclassified,
        "exhaustion_holds": not unclassified,
        "note": ("every odd prime below the scan falls in exactly one of the "
                 "four classes the router names; p = 2 is outside its scope"),
    }

    # ---- no rational prime-degree isogeny, as far as X₀(n) reaches ---------
    j = x0n.j_invariant(twisted)
    iso = {"j": str(j), "degrees_checked": [], "degrees_not_checked":
           [n for n in MAZUR_DEGREES if n not in COVERED]}
    if j in (Fraction(0), Fraction(1728)):
        iso["set_aside"] = True
    else:
        fac = x0n.factorise(j.denominator) if j.denominator > 1 else {}
        for n in COVERED:
            pts = x0n.rational_points(j, n, fac)
            iso["degrees_checked"].append(
                {"n": n, "decided": pts is not None,
                 "has_rational_isogeny": bool(pts) if pts is not None else None})
    iso["none_of_the_checked_degrees_occurs"] = all(
        e["decided"] and not e["has_rational_isogeny"]
        for e in iso["degrees_checked"])
    iso["scope"] = ("Mazur allows prime degrees 2, 3, 5, 7, 11, 13, 17, 19, 37, "
                    "43, 67, 163; the X₀(n) method here is built for the "
                    "genus-0 cases it was validated on, so eight of the twelve "
                    "are not covered and are named rather than passed over")

    log = {
        "gate": "src17_family_prime_router",
        "automatic_ordinary": automatic_ordinary,
        "second_condition_is_implied": redundancy,
        "explicit_numbers": explicit,
        "all_prime_router_exhaustion": router,
        "no_rational_prime_degree_isogeny": iso,
        "ok": (equivalence_holds and explicit["agrees"]
               and automatic_ordinary["all_members_are_ordinary"]
               and automatic_ordinary["all_members_have_odd_a_q"]
               and router["exhaustion_holds"]
               and iso.get("none_of_the_checked_degrees_occurs", False)
               and redundancy["condition_is_redundant"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    ao = automatic_ordinary
    print(f"  a_p odd ⟺ f₂ irreducible mod p, over {tested:,} primes: "
          f"{ao['a_p_odd_exactly_when_f2_is_irreducible']}   "
          f"counterexamples: {len(violations)}")
    print(f"    density of odd a_p : {ao['density_of_odd_a_p']:.6f}   "
          f"(Chebotarev predicts 1/3 = {1/3:.6f}) — so the condition is not "
          f"vacuous")
    print(f"    members of 𝒫 below {PRIME_SCAN:,}: {len(in_family)}   "
          f"all a_q odd: {ao['all_members_have_odd_a_q']}   "
          f"all ordinary: {ao['all_members_are_ordinary']}")
    print()
    print(f"  𝒫's (q/29) condition, against q ≡ 1 (mod 24) below "
          f"{REDUNDANCY_SCAN:,}:")
    for k, v in redundancy["cross_tabulation"].items():
        print(f"    {k:<44} {v:>7,}")
    print(f"    irreducible but NOT a residue: "
          f"{redundancy['irreducible_but_non_residue']}  ⟹  condition is "
          f"redundant: {redundancy['condition_is_redundant']}")
    print()
    print(f"  a_241(E) recomputed = {a241}   document states −7   "
          f"agrees: {explicit['agrees']}")
    print(f"    241 mod 24 = {explicit['241_mod_24']}   241 mod 29 = "
          f"{explicit['241_mod_29']} (square: "
          f"{explicit['241_mod_29_is_a_square']})   f₂ irreducible: "
          f"{explicit['f2_irreducible_mod_241']}   241 ∈ 𝒫: "
          f"{explicit['241_is_in_P']}")
    print()
    print(f"  all-prime router on E^({q}), odd primes below {ROUTER_SCAN:,}:")
    for k, v in sorted(router["classes"].items()):
        print(f"    {k:<26} {v:>6,}")
    print(f"    exhaustion holds: {router['exhaustion_holds']}   "
          f"unclassified: {len(unclassified)}")
    print()
    print(f"  rational prime-degree isogenies of E^({q}):")
    for e in iso["degrees_checked"]:
        print(f"    n = {e['n']:>3}  decided: {e['decided']}   has one: "
              f"{e['has_rational_isogeny']}")
    print(f"    not covered by this gate: {iso['degrees_not_checked']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
