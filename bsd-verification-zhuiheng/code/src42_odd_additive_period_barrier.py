"""Gate 42 — the odd-additive period barrier, run where the family meets it.

數學戰士「墜衡」 / AMRAL Research Lab.

`01_Odd_Additive_Period_Barrier` identifies an obstruction that is not
Iwasawa-theoretic at all. Fouquet–Wan permits any reduction type at `p`, so a
fixed odd additive bad prime is not excluded by the theorem; what fails is the
**period normalisation**. FW Corollary 1.10 uses the modular period, which for
an elliptic curve differs from the Néron period by the Manin constant. At a good
supersingular `p` that is harmless, because the Manin constant's prime divisors
are supported at additive primes — and at a fixed **additive** `p` that argument
is unavailable, `p` being exactly such a prime.

The document then names a published sufficient condition:

    p >= 11;
    the local reduction is not additive potentially ordinary of Kodaira type
    II, III or IV;
    the twist is optimal.

Then the known Manin-constant result gives `p` does not divide `c`.

THIS IS THE PIECE `11`'s SAFE CONDITION WAS AVOIDING. RUN-039 left `c_E = 1`
open, which is what `11_Derived_Supersingular_FW_Bridge` proposes requiring
outright. `01`'s condition asks for less — `p` not dividing `c`, at the one
prime that needs it — and it is checkable for every member of this family.

THE FAMILY MEETS THE BARRIER AT EXACTLY ONE PRIME PER MEMBER, AND CLEARS IT
STRUCTURALLY. The base has additive reduction only at 2, which is not odd, so
the barrier is empty for it. Each twist `E^(q)` is additive at `q`, and the
twisting valuations are forced: `d` squarefree, coprime to `N`, with `E` good at
`d`, gives `(v_d(c4), v_d(c6), v_d(Delta)) = (2, 3, 6)`, which is Kodaira `I0*`
— never II, III or IV. That is measured on every member rather than deduced.

WHAT IS NOT COMPUTED IS SAID. "Potentially ordinary" is part of the excluded
description and this arm does not compute the ordinarity of a potential good
reduction. It is not needed here: the Kodaira type alone already places the
family outside the excluded set, whatever the ordinarity. And `p` not dividing
`c` is then a CITED theorem, not a computation.

Usage:  python code/src42_odd_additive_period_barrier.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src42-odd-additive-barrier.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
FAMILY_BOUND = 4000
EXCLUDED_TYPES = ("II", "III", "IV")
MIN_P = 11
PROBE_PRIMES = (11, 13, 17, 19, 23, 29, 31, 37)


def valuations_at(ainvs: list[int], p: int) -> dict:
    """(v_p(c4), v_p(c6), v_p(Δ)) for the given model."""
    b2, b4, b6, b8, disc = anchor.b_invariants(ainvs)
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    big = 10 ** 9
    return {"v_c4": tate.valuation(c4, p) if c4 else big,
            "v_c6": tate.valuation(c6, p) if c6 else big,
            "v_disc": tate.valuation(disc, p) if disc else big}


def odd_additive_primes(ainvs: list[int]) -> list[int]:
    """The odd primes of additive reduction — where the barrier applies."""
    md = gcd35.multiplicative_data(ainvs)
    if md.get("singular"):
        return []
    return [r["p"] for r in md["additive"] if r["p"] % 2]


def barrier(ainvs: list[int], p: int) -> dict:
    """`01`'s sufficient condition at one odd additive prime."""
    r = tate.reduction_data(ainvs, p, want_c=True)
    kod = r.get("kodaira")
    v = valuations_at(ainvs, p)
    big_enough = p >= MIN_P
    excluded_type = kod in EXCLUDED_TYPES
    return {"p": p, "kodaira": kod, "valuations": v,
            "p_at_least_11": big_enough,
            "kodaira_is_excluded": excluded_type,
            "potentially_ordinary_computed": False,
            "condition_met": big_enough and not excluded_type,
            "optimality": "cited",
            "conclusion_if_met": "p does not divide c — the known "
                                 "Manin-constant result, cited",
            "note": ("the excluded set is additive POTENTIALLY ORDINARY of "
                     "type II, III or IV. The ordinarity is not computed here "
                     "and is not needed: the type already places this prime "
                     "outside the set" if not excluded_type else
                     "the type is inside the excluded set, so the ordinarity "
                     "would have to be settled before the condition applies")}


def base_curve() -> dict:
    """The barrier is empty for the base, and that is the reason, not luck."""
    md = gcd35.multiplicative_data(BASE)
    add = [r["p"] for r in md["additive"]]
    odd = odd_additive_primes(BASE)
    return {"additive_primes": add, "odd_additive_primes": odd,
            "barrier_applies": bool(odd),
            "why": ("the only additive prime of 696.e1 is 2, and `01`'s "
                    "obstruction is about a fixed ODD additive prime. p = 2 is "
                    "routed to Banwait–Huang by 12's P0 and never reaches the "
                    "period argument this document is about")}


def family(bound: int = FAMILY_BOUND) -> dict:
    """Every member's odd additive prime, put through the condition."""
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = []
    for q in members:
        tw = mz.quadratic_twist(BASE, q)
        odd = odd_additive_primes(tw)
        per = [barrier(tw, p) for p in odd]
        rows.append({"q": q, "odd_additive_primes": odd,
                     "is_exactly_q": odd == [q],
                     "rows": per,
                     "all_conditions_met": bool(per)
                                           and all(x["condition_met"]
                                                   for x in per),
                     "kodaira": [x["kodaira"] for x in per],
                     "valuations": [x["valuations"] for x in per]})
    forced = all(r["valuations"] and r["valuations"][0]["v_c4"] == 2
                 and r["valuations"][0]["v_c6"] == 3
                 and r["valuations"][0]["v_disc"] == 6 for r in rows)
    return {"members": len(members), "rows": rows,
            "odd_additive_prime_is_always_q": all(r["is_exactly_q"]
                                                  for r in rows),
            "every_member_meets_the_condition": all(r["all_conditions_met"]
                                                    for r in rows),
            "kodaira_always_I0star": all(r["kodaira"] == ["I0*"]
                                         for r in rows),
            "valuations_are_forced_2_3_6": forced,
            "why_forced": ("for d squarefree, coprime to N and good for E, the "
                           "twist scales c4 by d², c6 by d³ and Δ by d⁶, so at "
                           "p = d the valuations are exactly (2, 3, 6) — which "
                           "is I0*, and never II, III or IV")}


def the_excluded_types_are_reachable() -> dict:
    """The excluded set must be non-empty somewhere, or the condition is untested.

    Constructed rather than searched: `y² = x³ + p` and `y² = x³ + px` are
    additive at `p` with small `c4`/`c6` valuations, and Tate's algorithm is
    left to say which Kodaira types they actually carry. Reporting "no member of
    the family is type II, III or IV" without ever exhibiting one would be the
    same as reporting an empty list as a finding.
    """
    found, rows = {}, []
    for p in PROBE_PRIMES:
        for label, ai in (("y² = x³ + p", [0, 0, 0, 0, p]),
                          ("y² = x³ + px", [0, 0, 0, p, 0]),
                          ("y² = x³ + p²", [0, 0, 0, 0, p * p]),
                          ("y² = x³ + p²x", [0, 0, 0, p * p, 0])):
            r = tate.reduction_data(ai, p, want_c=True)
            kod = r.get("kodaira")
            rows.append({"p": p, "curve": label, "ainvs": ai, "kodaira": kod})
            if kod in EXCLUDED_TYPES and kod not in found:
                found[kod] = {"p": p, "curve": label, "ainvs": ai,
                              "kodaira": kod,
                              "valuations": valuations_at(ai, p),
                              "condition_met": barrier(ai, p)["condition_met"]}
    return {"probes": rows, "excluded_types_found": sorted(found),
            "examples": found,
            "all_three_reachable": sorted(found) == sorted(EXCLUDED_TYPES),
            "at_least_one_reachable": bool(found),
            "and_the_condition_fails_there": all(not v["condition_met"]
                                                 for v in found.values())}


def link_to_run_039() -> dict:
    """What this closes of RUN-039's open item, and what it does not."""
    return {"RUN_039_left_open": "c_E = 1, `11`'s safe period condition",
            "what_01_offers_instead": "p does not divide c, at the odd additive "
                                      "prime, under a published sufficient "
                                      "condition",
            "weaker_but_enough": ("the p-part of BSD needs p not to divide the "
                                  "Manin constant, not the constant to be 1"),
            "still_cited": ("the Manin-constant result itself. This gate "
                            "checks the condition's hypotheses and never the "
                            "theorem they feed"),
            "c_E_is_still_not_computed": True}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    b = base_curve()
    f = family()
    ex = the_excluded_types_are_reachable()
    lk = link_to_run_039()

    ok = (not b["barrier_applies"]
          and f["odd_additive_prime_is_always_q"]
          and f["every_member_meets_the_condition"]
          and f["kodaira_always_I0star"]
          and f["valuations_are_forced_2_3_6"]
          and ex["at_least_one_reachable"]
          and ex["and_the_condition_fails_there"]
          and lk["c_E_is_still_not_computed"])

    log = {
        "gate": "src42 — the odd-additive period barrier, run",
        "source": "01_Odd_Additive_Period_Barrier",
        "curve": BASE, "conductor": N,
        "the_condition": ["p >= 11",
                          "local reduction not additive potentially ordinary "
                          "of Kodaira type II, III or IV",
                          "the twist is optimal (cited)"],
        "base_curve": b,
        "the_family": f,
        "the_excluded_types_are_reachable": ex,
        "link_to_RUN_039": lk,
        "headline": (f"the barrier is empty for the base — its only additive "
                     f"prime is 2 — and each of the {f['members']} members "
                     f"meets it at exactly one prime, q itself, where the "
                     f"Kodaira type is I0* for every member because the twist "
                     f"forces the valuations to (2, 3, 6). I0* is not among "
                     f"II, III, IV, so `01`'s sufficient condition is met "
                     f"throughout and p does not divide c follows from the "
                     f"cited Manin-constant result"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  base curve: additive at {b['additive_primes']}, odd additive "
          f"{b['odd_additive_primes']} → barrier applies: "
          f"{b['barrier_applies']}")
    print()
    print(f"  the family: {f['members']} members")
    print(f"    the odd additive prime is always q       : "
          f"{f['odd_additive_prime_is_always_q']}")
    print(f"    Kodaira type there is always I0*         : "
          f"{f['kodaira_always_I0star']}")
    print(f"    valuations forced to (2, 3, 6)           : "
          f"{f['valuations_are_forced_2_3_6']}")
    print(f"    01's condition met by every member       : "
          f"{f['every_member_meets_the_condition']}")
    print(f"    (p ≥ 11 holds: the smallest member is "
          f"{f['rows'][0]['q']})")
    print()
    print(f"  the excluded types are reachable: {ex['excluded_types_found']}")
    for k, v in ex["examples"].items():
        print(f"    {k:<4} {v['curve']:<14} p = {v['p']:<4} {v['ainvs']}  "
              f"condition met: {v['condition_met']}")
    print(f"    all three of II, III, IV: {ex['all_three_reachable']}   "
          f"condition fails at each: {ex['and_the_condition_fails_there']}")
    print()
    print(f"  RUN-039 left open: {lk['RUN_039_left_open']}")
    print(f"    01 offers instead: {lk['what_01_offers_instead']}")
    print(f"    c_E still not computed here: {lk['c_E_is_still_not_computed']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
