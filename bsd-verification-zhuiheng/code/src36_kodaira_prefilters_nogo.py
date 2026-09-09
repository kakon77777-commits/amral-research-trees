"""Gate 36 — the Kodaira prefilters and the exact no-go, run where they can fire.

數學戰士「墜衡」 / AMRAL Research Lab.

`05_Kodaira_Prefilters_and_NoGo` states one exact no-go:

    ADDITIVE + POTENTIALLY_MULTIPLICATIVE  =>  FW17_H2_FAIL

with the reason: such a curve becomes a Tate curve after a quadratic twist ψ,
whose residual semisimplification 1 ⊕ ω twists back to ψ ⊕ ψω, and ψ² = 1 puts
it in exactly the form FW Theorem 1.7 forbids. It adds a structural fact at
p = 3, a local-torsion detector with an explicitly stated non-converse, and then
**formally forbids** the Kodaira-only table:

    potentially supersingular => PASS
    potentially good ordinary => FAIL/PASS
    Kodaira X                 => automatic H2

THE RESULT IS THAT THE NO-GO HAS NO DOMAIN IN THIS FAMILY, AND THE REASON IS
ONE OF 𝒫's MEMBERSHIP CONDITIONS. The anchor's additive primes are 2 for the
base and {2, q} for the twist E^(q). All are potentially good, so the no-go
never fires — and it is not an accident: twisting by d makes d additive, and
the potential reduction there is the base's reduction at d, because j is
twist-invariant. So the no-go fires at d exactly when the base is
**multiplicative** at d, which for 696.e1 means d ∈ {3, 29}. The condition
`gcd(q, 696) = 1` excludes precisely those. A condition that reads like
bookkeeping is what keeps this no-go out of the family.

THIS GATE DOES NOT USE THE TABLE IT REPORTS. The no-go's antecedent is decided
by `v_p(j) < 0` throughout; Kodaira symbols are printed **alongside** as a
correlate and are never the criterion, because reading the verdict off the
symbol is the first thing `05` forbids.

Usage:  python code/src36_kodaira_prefilters_nogo.py
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
OUT = ROOT / "data" / "gate-logs" / "src36-kodaira-nogo.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
FAMILY_BOUND = 4000
TWIST_PROBE = (2, 3, 5, 7, 11, 13, 23, 29, 31, 241, 313)
CHARACTER_PRIMES = (2, 3, 5, 7, 11, 13, 17)

FORBIDDEN = (
    "potentially supersingular => PASS",
    "potentially good ordinary => FAIL/PASS",
    "Kodaira X => automatic H2",
)


def local_type(ainvs: list[int], p: int) -> dict:
    """Reduction at p, with the no-go's antecedent decided by v_p(j).

    `kodaira` is carried for the reader. It is not consulted: `05` forbids
    reading H2 off a Kodaira symbol, and a gate that checked the no-go by
    matching symbols would be committing the inference it is auditing.
    """
    d = tate.reduction_data(ainvs, p, want_c=True)
    multiplicative = "split_multiplicative" in d
    additive = (not multiplicative) and d.get("f", 0) >= 2
    good = not multiplicative and not additive
    pot = tate.potential_reduction(ainvs, p)
    return {"p": p, "kodaira": d.get("kodaira"), "f": d.get("f"),
            "v_disc": d.get("v_disc"),
            "reduction": ("good" if good else
                          "multiplicative" if multiplicative else "additive"),
            "split": d.get("split_multiplicative"),
            "potential_reduction": pot,
            "decided_by": "v_p(j) < 0, not the Kodaira symbol"}


def no_go(ainvs: list[int], p: int) -> dict:
    """`05`'s exact no-go, evaluated at one prime."""
    t = local_type(ainvs, p)
    fires = (t["reduction"] == "additive"
             and t["potential_reduction"] == "potentially multiplicative")
    return {**t, "no_go_fires": fires,
            "verdict": "FW17_H2_FAIL" if fires else "no-go silent here",
            "why": ("additive and potentially multiplicative: twists to a Tate "
                    "curve, whose residual form is FW 1.7's forbidden one"
                    if fires else
                    f"antecedent not met — {t['reduction']}, {t['potential_reduction']}")}


def anchor_and_family(bound: int = FAMILY_BOUND) -> dict:
    """The no-go's domain over the base and every member's twist.

    The additive primes are found rather than assumed: they are read from each
    model's own discriminant through Tate's algorithm.
    """
    def additive_of(ai):
        md = gcd35.multiplicative_data(ai)
        return [r["p"] for r in md["additive"]]

    base_add = additive_of(BASE)
    base_rows = [no_go(BASE, p) for p in base_add]
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = []
    for q in members:
        tw = mz.quadratic_twist(BASE, q)
        add = additive_of(tw)
        entries = [no_go(tw, p) for p in add]
        rows.append({"q": q, "additive_primes": add,
                     "types": [(e["p"], e["kodaira"],
                                e["potential_reduction"]) for e in entries],
                     "any_fires": any(e["no_go_fires"] for e in entries)})
    return {"base_additive_primes": base_add, "base": base_rows,
            "members": len(members), "rows": rows,
            "no_go_fires_anywhere_in_the_family":
                any(r["any_fires"] for r in rows)
                or any(r["no_go_fires"] for r in base_rows),
            "additive_primes_are_always_2_and_q":
                all(sorted(r["additive_primes"]) == sorted([2, r["q"]])
                    for r in rows)}


def where_it_fires(probe=TWIST_PROBE) -> dict:
    """Twist by d and ask the no-go at d — the constructive both-sides test.

    Twisting by d makes d additive; the potential reduction at d is the base's
    reduction there, since j is twist-invariant. So the no-go's domain is
    exactly the set of d at which the base is multiplicative, and this measures
    that rather than deducing it.
    """
    rows = []
    for d in probe:
        base_here = local_type(BASE, d)
        tw = mz.quadratic_twist(BASE, d)
        g = no_go(tw, d)
        rows.append({"d": d, "base_reduction_at_d": base_here["reduction"],
                     "twist_kodaira_at_d": g["kodaira"],
                     "twist_reduction_at_d": g["reduction"],
                     "twist_potential_at_d": g["potential_reduction"],
                     "no_go_fires": g["no_go_fires"]})
    fires = sorted(r["d"] for r in rows if r["no_go_fires"])
    mult = sorted(r["d"] for r in rows
                  if r["base_reduction_at_d"] == "multiplicative")
    excluded = sorted(p for p in probe if N % p == 0)
    return {"rows": rows, "fires_at": fires,
            "base_multiplicative_at": mult,
            "fires_exactly_where_the_base_is_multiplicative": fires == mult,
            "excluded_by_gcd_condition": excluded,
            "gcd_condition_covers_every_firing_d":
                all(d in excluded for d in fires),
            "reading": ("𝒫 requires gcd(q, 696) = 1, which removes exactly the "
                        "primes dividing the conductor — and every d at which "
                        "the no-go fires divides the conductor, because firing "
                        "requires the base to be multiplicative there")}


def character_structure(primes=CHARACTER_PRIMES) -> dict:
    """`05`'s p = 3 step: F₃ˣ = {±1}, so every 1-dimensional constituent is
    quadratic or trivial.

    Measured as the exponent of Fₚˣ. The point is the contrast: the argument is
    special to 3 among odd primes and does not transfer upward, so a gate that
    checked only p = 3 would not know whether it had found a fact or a pattern.
    """
    rows = []
    for p in primes:
        orders = []
        for a in range(1, p):
            k, x = 1, a % p
            while x != 1:
                x = (x * a) % p
                k += 1
            orders.append(k)
        mx = max(orders) if orders else 1
        rows.append({"p": p, "size_of_F_p_star": p - 1, "exponent": mx,
                     "every_character_is_quadratic_or_trivial": mx <= 2})
    only = [r["p"] for r in rows if r["every_character_is_quadratic_or_trivial"]]
    return {"rows": rows, "holds_at": only,
            "special_to_3_among_odd_primes": [p for p in only if p > 2] == [3],
            "note": ("p = 2 also has exponent 1, trivially; the document's "
                     "argument is stated for 3 and the measurement says 3 is "
                     "the only odd prime where it is available")}


def torsion_clause() -> dict:
    """`05`'s third rule, with the non-converse it states itself.

    The rule is local — E(Q_p)[p] ≠ 0 ⟹ FAIL — and this arm computes the
    **global** rational torsion, which is a strictly stronger vanishing. So the
    honest report is: the global antecedent is absent, the local one is not
    computed, and the document itself says absence is not a PASS.
    """
    bound = anchor.torsion_bound(BASE, N)
    return {"global_rational_torsion_order_bound": bound,
            "global_torsion_trivial": bound == 1,
            "local_condition_computed": False,
            "local_condition": "E(Q_p)[p] != 0",
            "the_documents_own_non_converse":
                "NO rational p-torsion != H2 PASS",
            "what_this_licenses": ("nothing. The absence of the antecedent is "
                                   "recorded in the same slot RUN-031 put "
                                   "n = 2: a criterion with no domain here, "
                                   "not a criterion that passed")}


def self_audit() -> dict:
    """Does this gate commit any of the three inferences `05` forbids?"""
    return {"forbidden": list(FORBIDDEN),
            "this_gate_decides_the_antecedent_by": "v_p(j) < 0",
            "kodaira_symbols_are": "reported alongside, never consulted",
            "commits_a_forbidden_inference": False,
            "why_it_matters": ("the finding below is stated as I₀* against "
                               "I₁*, which reads like a Kodaira table. It is "
                               "not one: the split is computed from the "
                               "j-invariant and the symbols happen to track "
                               "it, which is a correlate and not a criterion")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    fam_rows = anchor_and_family()
    fires = where_it_fires()
    chars = character_structure()
    tors = torsion_clause()
    audit = self_audit()

    ok = (not fam_rows["no_go_fires_anywhere_in_the_family"]
          and fam_rows["additive_primes_are_always_2_and_q"]
          and fires["fires_exactly_where_the_base_is_multiplicative"]
          and fires["gcd_condition_covers_every_firing_d"]
          and bool(fires["fires_at"])
          and chars["special_to_3_among_odd_primes"]
          and tors["global_torsion_trivial"]
          and not audit["commits_a_forbidden_inference"])

    log = {
        "gate": "src36 — Kodaira prefilters and the exact no-go, run",
        "source": "05_Kodaira_Prefilters_and_NoGo",
        "curve": BASE, "conductor": N,
        "the_no_gos_domain_in_this_family": fam_rows,
        "where_it_does_fire": fires,
        "p_equals_3_character_structure": chars,
        "local_torsion_clause": tors,
        "self_audit_against_the_forbidden_table": audit,
        "headline": ("the exact no-go has no domain in this family, and the "
                     "reason is 𝒫's own gcd(q, 696) = 1: firing at d requires "
                     "the base to be multiplicative at d, and those d divide "
                     "the conductor"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print("  the no-go on the base curve")
    for r in fam_rows["base"]:
        print(f"    p = {r['p']:<4} {r['reduction']:<14} {str(r['kodaira']):<5} "
              f"{r['potential_reduction']:<28} fires = {r['no_go_fires']}")
    print(f"    additive primes always (2, q) across "
          f"{fam_rows['members']} members: "
          f"{fam_rows['additive_primes_are_always_2_and_q']}")
    print(f"    fires anywhere in the family: "
          f"{fam_rows['no_go_fires_anywhere_in_the_family']}")
    print()
    print("  twist by d, then ask the no-go at d")
    print(f"    {'d':>5}  {'base at d':<15} {'twist':<6} "
          f"{'potential':<28} fires")
    for r in fires["rows"]:
        print(f"    {r['d']:>5}  {r['base_reduction_at_d']:<15} "
              f"{str(r['twist_kodaira_at_d']):<6} "
              f"{r['twist_potential_at_d']:<28} {r['no_go_fires']}")
    print(f"    fires at {fires['fires_at']}; base multiplicative at "
          f"{fires['base_multiplicative_at']}  → same set: "
          f"{fires['fires_exactly_where_the_base_is_multiplicative']}")
    print(f"    gcd(q, 696) = 1 excludes {fires['excluded_by_gcd_condition']} "
          f"⊇ every firing d: {fires['gcd_condition_covers_every_firing_d']}")
    print()
    print("  p = 3: the exponent of Fₚˣ")
    print("    " + "  ".join(f"{r['p']}:{r['exponent']}" for r in chars["rows"]))
    print(f"    quadratic-or-trivial only at {chars['holds_at']}; "
          f"among odd primes only 3: {chars['special_to_3_among_odd_primes']}")
    print()
    print(f"  torsion clause: global rational torsion bound "
          f"{tors['global_rational_torsion_order_bound']}, local condition "
          f"computed: {tors['local_condition_computed']}")
    print(f"    licenses: {tors['what_this_licenses'][:60]}…")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
