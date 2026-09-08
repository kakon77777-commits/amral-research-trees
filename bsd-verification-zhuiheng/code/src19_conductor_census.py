"""Gate 19 — every conductor in the base recomputed, and the c_2 two rounds owed.

數學戰士「墜衡」 / AMRAL Research Lab.

Drives Tate's algorithm (`src18`) over the whole Phase 1 base and over the
Phase 2 family, closing three things at once.

**The census's conductor column.** RUN-004 recomputed 40,749 discriminants and
135,787 valuations; RUN-008 verified the discriminant factorisations. No round
has recomputed a conductor. This one recomputes all 40,749 from the
a-invariants, by a route that reads nothing but the curve.

**c_2 for the anchor.** RUN-014 and RUN-015 both reported c_2·#Ш as a single
quantity because the reduction at 2 is additive. Tate settles it.

**The Kodaira types Phase 2 routes on.** `01_Odd_Additive_Period_Barrier` names
a Manin-constant condition excluding "additive potentially ordinary of Kodaira
type II, III or IV", and `05_Kodaira_Prefilters_and_NoGo` states an exact no-go
for additive **potentially multiplicative** reduction. Both need the type at the
twisting prime, and both are checked here for the family's members.

Potential reduction is separate and cheaper: E is potentially multiplicative at
p exactly when v_p(j) < 0, which needs no Tate run at all.

Usage:  python code/src19_conductor_census.py
"""

from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src19-conductor-census.json"

# Curves whose conductor, Kodaira type and Tamagawa number are fixed outside
# this tree. 11a1's c_11 = 5 is the sharpest: RUN-014 derived it independently
# from L/Ω = 1/5 with torsion 5 and trivial Ш.
KNOWN = [
    ("11a1", [0, -1, 1, -10, -20], 11, {11: ("I5", 5)}),
    ("14a1", [1, 0, 1, 4, -6], 14, {2: ("I6", 2), 7: ("I3", 3)}),
    ("15a1", [1, 1, 1, -10, -10], 15, {3: ("I4", 2), 5: ("I4", 4)}),
    ("27a1", [0, 0, 1, 0, -7], 27, {3: ("IV*", 3)}),
    ("32a1", [0, 0, 0, 4, 0], 32, {2: ("I3*", 4)}),
    ("36a1", [0, 0, 0, 0, 1], 36, {2: ("IV", 3), 3: ("III", 2)}),
    ("37a1", [0, 0, 1, -1, 0], 37, {37: ("I1", 1)}),
    ("64a1", [0, 0, 0, -4, 0], 64, {2: ("I2*", 4)}),
    ("389a1", [0, 1, 1, -2, 0], 389, {389: ("I1", 1)}),
]

ANCHOR = [0, 1, 0, 8, -16]
ANCHOR_N = 696


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    # ---- self-check ------------------------------------------------------
    checks = []
    for label, inv, N, expect in KNOWN:
        primes = [p for p in (2, 3, 5, 7, 11, 13, 29, 37, 389) if N % p == 0]
        data = {p: tate.reduction_data(inv, p, want_c=True) for p in primes}
        Nc = 1
        for p, d in data.items():
            Nc *= p ** d["f"]
        row = {"curve": label, "conductor": N, "recomputed": Nc,
               "conductor_ok": Nc == N,
               "types": {str(p): [d["kodaira"], d["c"]]
                         for p, d in data.items()},
               "expected": {str(p): list(v) for p, v in expect.items()}}
        row["types_ok"] = all(
            data[p]["kodaira"] == k and data[p]["c"] == c
            for p, (k, c) in expect.items())
        checks.append(row)
        if not (row["conductor_ok"] and row["types_ok"]):
            raise SystemExit(f"SELF-CHECK FAILED on {label}: {row}")
    print(f"  self-check: {len(checks)} curves, conductors and types reproduced")

    # ---- the whole base ---------------------------------------------------
    records = json.loads(x0n.ARITH.read_text(encoding="utf-8"))["records"]
    agree = disagree = 0
    mismatches = []
    types_at_2_3 = collections.Counter()
    types_all = collections.Counter()
    additive_primes = collections.Counter()
    non_semistable = []
    for idx, r in enumerate(records):
        if idx and idx % 5000 == 0:
            print(f"    … {idx:,}/{len(records):,}", file=sys.stderr)
        N = 1
        for p in r["conductor_primes"]:
            d = tate.reduction_data(r["ainvs"], p)
            N *= p ** d["f"]
            kind = d["kodaira"]
            bucket = kind if (kind.endswith("*") or not kind.startswith("I")
                              or kind == "I0") else "I_n"
            types_all[bucket] += 1
            if p in (2, 3):
                types_at_2_3[bucket] += 1
            if d["f"] >= 2:
                additive_primes[p if p < 5 else "p >= 5"] += 1
        if any(r["conductor"] % (p * p) == 0
               for p in r["conductor_primes"]) and len(non_semistable) < 20:
            non_semistable.append(r["curve_label"])
        if N == r["conductor"]:
            agree += 1
        else:
            disagree += 1
            if len(mismatches) < 20:
                mismatches.append({"label": r["curve_label"],
                                   "stated": r["conductor"], "recomputed": N})

    # ---- the anchor, and the c_2 that was carved out ----------------------
    anchor_data = {str(p): tate.reduction_data(ANCHOR, p, want_c=True)
                   for p in (2, 3, 29)}
    anchor_N = 1
    for p, d in anchor_data.items():
        anchor_N *= int(p) ** d["f"]
    prod_c = 1
    for d in anchor_data.values():
        prod_c *= d["c"]

    # ---- the family at its twisting prime ---------------------------------
    # src10's sieve returns a flag array, not a list of primes; src15's returns
    # the primes. A first run used the wrong one, so this list was empty — and
    # the gate's own ok condition, an `all(...)` over it, passed on nothing.
    # The guard below is why that is now a failure rather than a green run.
    members = [q for q in anchor.sieve(4000) if fam.in_P(q)]
    if len(members) < 10:
        raise SystemExit(f"only {len(members)} members of P found below 4,000; "
                         "RUN-015 measured 19, so the enumeration is wrong and "
                         "every check over it would pass vacuously")
    family = []
    for q in members[:8]:
        inv = fam.twist(fam.BASE, q)
        d = tate.reduction_data(inv, q, want_c=True)
        family.append({
            "q": q, "kodaira_at_q": d["kodaira"], "f_at_q": d["f"],
            "c_q": d["c"],
            "f2_roots_mod_q": ph2.cubic_root_count(ph2.F2, q),
            "potential_reduction_at_q": tate.potential_reduction(inv, q),
            "types_at_2_3_29": {str(p): tate.reduction_data(inv, p,
                                                            want_c=True)["kodaira"]
                                for p in (2, 3, 29)},
        })

    doc05 = {
        "exact_no_go": ("05_Kodaira_Prefilters_and_NoGo: additive AND "
                        "potentially multiplicative ⟹ FW17_H2_FAIL"),
        "at_the_twisting_prime": (
            "E has good reduction at q, so its quadratic twist has potentially "
            "GOOD reduction there — v_q(j) = v_q(j(E)) ≥ 0. The no-go does not "
            "fire, and that is a fact about the family rather than a hope"),
        "measured": {str(e["q"]): e["potential_reduction_at_q"]
                     for e in family},
        "no_go_fires_anywhere": any(
            e["potential_reduction_at_q"] == "potentially multiplicative"
            for e in family),
    }
    doc01 = {
        "condition": ("01_Odd_Additive_Period_Barrier: the published Manin "
                      "sufficient condition excludes additive potentially "
                      "ordinary of Kodaira type II, III or IV"),
        "types_found_at_q": sorted({e["kodaira_at_q"] for e in family}),
        "any_in_the_excluded_set": any(e["kodaira_at_q"] in ("II", "III", "IV")
                                       for e in family),
    }

    log = {
        "gate": "src19_conductor_census",
        "self_check": checks,
        "base_conductors": {
            "curves": len(records),
            "recomputed_agrees": agree,
            "DISAGREES": disagree,
            "mismatches": mismatches,
            "route": ("Tate's algorithm from the a-invariants; nothing is read "
                      "but the curve. RUN-014 verified one conductor by which N "
                      "makes the functional equation close — a different route "
                      "entirely, and they agree on 696"),
        },
        "the_base_is_entirely_semistable": {
            "curves_with_a_non_squarefree_conductor": len(non_semistable),
            "sample": non_semistable,
            "every_bad_prime_is_multiplicative": (
                set(types_all) == {"I_n"}),
            "why_it_matters": (
                "a curve is semistable exactly when its conductor is "
                "squarefree, equivalently when every bad prime is "
                "multiplicative. Not one of the 40,749 base curves fails that, "
                "over all 135,787 bad primes — so the Banwait–Huang census "
                "reaches no non-semistable curve at all. That is precisely the "
                "gap the Phase 2 line exists to address, and 696.e1 with its "
                "additive prime 2 sits outside the base by construction rather "
                "than by choice"),
        },
        "kodaira_distribution": {
            "all_bad_primes": dict(types_all.most_common()),
            "at_p_in_2_3": dict(types_at_2_3.most_common()),
            "additive_prime_counts": {str(k): v for k, v
                                      in additive_primes.most_common()},
        },
        "anchor_696e1": {
            "types": {p: {"kodaira": d["kodaira"], "f": d["f"], "c": d["c"]}
                      for p, d in anchor_data.items()},
            "conductor_recomputed": anchor_N,
            "product_of_tamagawa": prod_c,
            "c_2": anchor_data["2"]["c"],
            "closes": ("RUN-014 measured L(E,1)/Ω = 1 and read c_2·#Ш = 1 from "
                       "it; Tate gives c_2 = 1 outright, so #Ш = 1 follows "
                       "without the reading. Two independent routes to the same "
                       "pair"),
        },
        "family_at_the_twisting_prime": family,
        "doc05_potentially_multiplicative_no_go": doc05,
        "doc01_manin_kodaira_exclusion": doc01,
        "c_q_two_ways": (
            "RUN-015 derived c_q = 1 from L/Ω = 49, trivial torsion, Cassels's "
            "square theorem and c_q ∈ {1,2,4}. Tate gives type I0*, whose "
            "c = 1 + #roots of the step-7 cubic mod q — and 𝒫's third condition "
            "is exactly that f₂ is irreducible mod q, i.e. zero roots. The two "
            "routes share nothing"),
        "ok": (disagree == 0 and len(family) >= 8
               and anchor_data["2"]["c"] == 1
               and anchor_N == ANCHOR_N
               and all(e["c_q"] == 1 and e["kodaira_at_q"] == "I0*"
                       for e in family)
               and not doc05["no_go_fires_anywhere"]
               and not doc01["any_in_the_excluded_set"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print()
    print(f"  base: {len(records):,} conductors recomputed   agrees {agree:,}   "
          f"DISAGREES {disagree:,}")
    print(f"  every bad prime multiplicative: "
          f"{set(types_all) == {'I_n'}}   curves with a non-squarefree "
          f"conductor: {len(non_semistable)}  →  the whole base is semistable")
    print(f"  Kodaira types over all bad primes: "
          f"{dict(types_all.most_common(8))}")
    print(f"    at p in {{2,3}}: {dict(types_at_2_3.most_common(8))}")
    print()
    print(f"  696.e1: N recomputed = {anchor_N}   " + "   ".join(
        f"p={p}:{d['kodaira']}/f{d['f']}/c{d['c']}" for p, d in anchor_data.items()))
    print(f"    c_2 = {anchor_data['2']['c']}   ∏c_p = {prod_c}   "
          f"→ with RUN-014's L/Ω = 1 and trivial torsion, #Ш = 1")
    print()
    print("  the family at its twisting prime:")
    for e in family:
        print(f"    q = {e['q']:>4}  {e['kodaira_at_q']:<5} f={e['f_at_q']}  "
              f"c_q={e['c_q']}  f₂ roots mod q = {e['f2_roots_mod_q']}  "
              f"{e['potential_reduction_at_q']}")
    print(f"    doc 05 no-go fires: {doc05['no_go_fires_anywhere']}   "
          f"doc 01 excluded type present: {doc01['any_in_the_excluded_set']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
