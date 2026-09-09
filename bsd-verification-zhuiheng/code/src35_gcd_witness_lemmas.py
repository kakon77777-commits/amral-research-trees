"""Gate 35 — the GCD witness lemmas, run, and the empty set they do not survive.

數學戰士「墜衡」 / AMRAL Research Lab.

`00_GCD_Witness_Lemmas` is four short paragraphs and it is the algebraic floor
under both prime routers. For multiplicative bad primes ℓ it writes
`n_ℓ = v_ℓ(Δ_E)` and states:

    generic witness       for odd p not itself multiplicative,
                          ∃ℓ: p ∤ n_ℓ  ⟺  p ∤ gcd_ℓ n_ℓ
    fixed multiplicative  for p itself multiplicative the witness must be
                          distinct: ∃ℓ ≠ p with p ∤ n_ℓ — a leave-one-out
    nonsplit FW witness   the same lemma after restricting to the nonsplit
                          multiplicative primes

and closes: "This is the exact algebraic reason the all-prime witness problem
is finite." Every witness `17_696e1_All_Prime_Router` picks — ℓ = 29 in Case A,
ℓ = 29 in Case B, the 3↔29 swap in Case C, ℓ = 29 again in FW-H3 — is an
instance of one of these three, and none of them is computed anywhere in the
corpus. This runs them.

THE GCD OF AN EMPTY SET IS 0, AND EVERY PRIME DIVIDES 0. That is the whole
danger in the third lemma. It restricts to the nonsplit multiplicative primes,
and if that restriction empties the set then the lemma does not become
vacuously true — it says every odd prime is a failure, because `p | 0` always.
A gate that reported "gcd = 1, no failures" without ever exhibiting a curve
where the set empties would be reporting an accident as a check, so the empty
case is **searched for and exhibited** rather than described.

Bad primes are found from the discriminant, not assumed, for the reason RUN-030
recorded: a certificate that is handed its inputs is checking the hand.

Usage:  python code/src35_gcd_witness_lemmas.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src35-gcd-witness.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
FAMILY_BOUND = 4000
SEARCH_BOX = 6                            # |a4|, |a6| bound for the empty-set hunt


def factor(n: int) -> dict[int, int]:
    """Trial division. n here is a discriminant, so it has small factors and a
    possibly large square-free-ish remainder, which is returned as itself."""
    n, out, d = abs(n), {}, 2
    while d * d <= n:
        while n % d == 0:
            n //= d
            out[d] = out.get(d, 0) + 1
        d += 1 if d == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def multiplicative_data(ainvs: list[int]) -> dict:
    """Every bad prime with its reduction type, split/nonsplit and n_ℓ.

    The bad primes are read off the discriminant of the given model. A prime
    can appear in that factorisation and still be good if the model is
    non-minimal there, which Tate's algorithm reports, so the split is taken
    from `reduction_data` rather than from the factorisation.
    """
    _, _, _, _, disc = anchor.b_invariants(ainvs)
    if disc == 0:
        return {"singular": True}
    rows, mult, add = [], [], []
    for p in sorted(factor(disc)):
        d = tate.reduction_data(ainvs, p, want_c=True)
        kod = d.get("kodaira")
        row = {"p": p, "kodaira": kod, "v_disc": d.get("v_disc"),
               "f": d.get("f"), "c": d.get("c")}
        if "split_multiplicative" in d:
            row["split"] = d["split_multiplicative"]
            row["n"] = d["v_disc"]
            row["type"] = "multiplicative"
            mult.append(row)
        elif d.get("f", 0) >= 2:
            row["type"] = "additive"
            add.append(row)
        else:
            row["type"] = "good (non-minimal model)"
        rows.append(row)
    return {"singular": False, "discriminant": disc, "rows": rows,
            "multiplicative": mult, "additive": add,
            "nonsplit": [r for r in mult if not r["split"]]}


def odd_prime_divisors(n: int, bound: int = 10_000) -> list[int] | str:
    """The odd primes dividing n — the failure set of the lemma.

    `gcd = 0` is the case the lemma's phrasing hides: every prime divides 0, so
    the failure set is *all* odd primes, and that is returned as a statement
    rather than as a list that would have to be infinite.
    """
    if n == 0:
        return "every odd prime (gcd of an empty set is 0, and p | 0 always)"
    return [p for p in anchor.sieve(bound) if p > 2 and n % p == 0]


def generic_witness(md: dict) -> dict:
    """Lemma 1: for odd p not multiplicative, a witness exists iff p ∤ gcd n_ℓ."""
    ns = [r["n"] for r in md["multiplicative"]]
    g = math.gcd(*ns) if ns else 0
    return {"lemma": "generic witness",
            "multiplicative_primes": [r["p"] for r in md["multiplicative"]],
            "n_ell": {str(r["p"]): r["n"] for r in md["multiplicative"]},
            "gcd": g,
            "failure_set": odd_prime_divisors(g),
            "witness_exists_for_every_odd_nonmultiplicative_p": g not in (0,)
            and not [p for p in anchor.sieve(200) if p > 2 and g % p == 0]}


def leave_one_out(md: dict) -> dict:
    """Lemma 2: for p itself multiplicative the witness must be a different ℓ."""
    mult = md["multiplicative"]
    rows = []
    for r in mult:
        p = r["p"]
        others = [s for s in mult if s["p"] != p]
        g = math.gcd(*[s["n"] for s in others]) if others else 0
        chosen = next((s["p"] for s in others if s["n"] % p), None)
        rows.append({"p": p, "others": [s["p"] for s in others],
                     "gcd_of_others": g,
                     "witness": chosen,
                     "n_at_witness": next((s["n"] for s in others
                                           if s["p"] == chosen), None),
                     "ok": chosen is not None})
    return {"lemma": "fixed multiplicative (leave-one-out)", "rows": rows,
            "all_have_a_distinct_witness": all(r["ok"] for r in rows)}


def nonsplit_witness(md: dict) -> dict:
    """Lemma 3: the same gcd after restricting to nonsplit multiplicative ℓ.

    The restriction is where the set can empty, so the size of what survives it
    is reported alongside the gcd. A singleton means the FW-H3 route has one
    witness and no redundancy: it is not failing, but nothing is spare.
    """
    ns = md["nonsplit"]
    g = math.gcd(*[r["n"] for r in ns]) if ns else 0
    return {"lemma": "nonsplit FW witness",
            "multiplicative_primes": [r["p"] for r in md["multiplicative"]],
            "nonsplit_primes": [r["p"] for r in ns],
            "survived_the_restriction": f"{len(ns)} of "
                                        f"{len(md['multiplicative'])}",
            "gcd": g,
            "failure_set": odd_prime_divisors(g),
            "redundancy": ("none — a single witness; if it were split too the "
                           "set would be empty and every odd p would fail"
                           if len(ns) == 1 else
                           "the set is empty: the lemma fails at every odd p"
                           if not ns else f"{len(ns)} independent witnesses")}


def small_curves(box: int):
    """A-invariant box, nonsingular models only. Used to hunt for the empty
    cases rather than to name a curve from memory."""
    for a1 in (0, 1):
        for a2 in (-1, 0, 1):
            for a3 in (0, 1):
                for a4 in range(-box, box + 1):
                    for a6 in range(-box, box + 1):
                        ai = [a1, a2, a3, a4, a6]
                        if anchor.b_invariants(ai)[4] != 0:
                            yield ai


def empty_set_search(box: int = SEARCH_BOX) -> dict:
    """Find curves where each set empties, and show what the lemma then says.

    Two shapes are wanted:
      no multiplicative primes at all   lemma 1's gcd is 0
      multiplicative primes, all split  lemma 3's gcd is 0 while lemma 1's is not

    The second is the sharp one: lemma 1 passes and lemma 3 fails on the same
    curve, so "the gcd is 1" for one lemma says nothing about the other.
    """
    no_mult, all_split, scanned = None, None, 0
    for ai in small_curves(box):
        scanned += 1
        md = multiplicative_data(ai)
        if md["singular"]:
            continue
        mult = md["multiplicative"]
        if not mult and md["additive"] and no_mult is None:
            no_mult = {"ainvs": ai, "discriminant": md["discriminant"],
                       "bad": [(r["p"], r["type"], r.get("kodaira"))
                               for r in md["rows"]],
                       "lemma1_gcd": generic_witness(md)["gcd"],
                       "lemma1_failure_set": generic_witness(md)["failure_set"]}
        if mult and not md["nonsplit"] and all_split is None:
            g1 = generic_witness(md)
            g3 = nonsplit_witness(md)
            all_split = {"ainvs": ai, "discriminant": md["discriminant"],
                         "multiplicative": [r["p"] for r in mult],
                         "all_split": True,
                         "lemma1_gcd": g1["gcd"],
                         "lemma1_failure_set": g1["failure_set"],
                         "lemma3_gcd": g3["gcd"],
                         "lemma3_failure_set": g3["failure_set"]}
        if no_mult and all_split:
            break
    return {"models_scanned": scanned,
            "no_multiplicative_primes": no_mult,
            "multiplicative_but_all_split": all_split,
            "why": ("without these two the gate would report gcd = 1 for "
                    "696.e1 and never show that a different curve makes the "
                    "same lemma say every odd prime fails")}


def family(bound: int = FAMILY_BOUND) -> dict:
    """The three lemmas for E^(q) at every member of 𝒫 below the bound.

    `17_696e1_All_Prime_Router` Case C asserts the twist's multiplicative primes
    are still exactly 3 and 29 with both valuations 1. That is an assertion
    about every member, and it is what keeps the gcd at 1 for the whole family.
    """
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = []
    for q in members:
        tw = mz.quadratic_twist(BASE, q)
        md = multiplicative_data(tw)
        g1, g3 = generic_witness(md), nonsplit_witness(md)
        add = [r["p"] for r in md["additive"]]
        rows.append({
            "q": q, "twist_ainvs": tw,
            "multiplicative": {str(r["p"]): r["n"]
                               for r in md["multiplicative"]},
            "nonsplit": [r["p"] for r in md["nonsplit"]],
            "additive": add,
            "q_is_additive_for_the_twist": q in add,
            "lemma1_gcd": g1["gcd"], "lemma3_gcd": g3["gcd"],
            "matches_case_C": ([r["p"] for r in md["multiplicative"]] == [3, 29]
                               and all(r["n"] == 1
                                       for r in md["multiplicative"])),
        })
    return {"bound": bound, "members": len(members), "rows": rows,
            "every_member_matches_case_C": all(r["matches_case_C"]
                                               for r in rows),
            "every_member_has_q_additive": all(r["q_is_additive_for_the_twist"]
                                               for r in rows),
            "gcds_all_one": all(r["lemma1_gcd"] == 1 and r["lemma3_gcd"] == 1
                                for r in rows)}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    md = multiplicative_data(BASE)
    l1, l2, l3 = generic_witness(md), leave_one_out(md), nonsplit_witness(md)
    empty = empty_set_search()
    fam_rows = family()

    ok = (l1["gcd"] == 1 and l2["all_have_a_distinct_witness"]
          and l3["gcd"] == 1
          and fam_rows["every_member_matches_case_C"]
          and fam_rows["gcds_all_one"]
          and empty["multiplicative_but_all_split"] is not None
          and empty["multiplicative_but_all_split"]["lemma3_gcd"] == 0)

    log = {
        "gate": "src35 — the GCD witness lemmas, run",
        "source": "00_GCD_Witness_Lemmas, used by 12_Hybrid_Odd_Prime_Router "
                  "and 17_696e1_All_Prime_Router",
        "curve": BASE,
        "bad_primes_found_from_the_discriminant": md["rows"],
        "lemma_1_generic": l1,
        "lemma_2_leave_one_out": l2,
        "lemma_3_nonsplit": l3,
        "the_empty_set": empty,
        "the_family": fam_rows,
        "what_this_settles": (
            "every witness the two routers pick is an instance of one of these "
            "three lemmas, and all three now have computed inputs: the "
            "multiplicative primes are found from the discriminant, the "
            "split/nonsplit classification is computed rather than quoted, and "
            "the gcd is taken over what was found"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  696.e1  Δ = {md['discriminant']}")
    for r in md["rows"]:
        extra = ("split" if r.get("split") else "nonsplit") if "split" in r else ""
        print(f"    p = {r['p']:<4} {r['type']:<16} {str(r['kodaira']):<5} "
              f"v_Δ = {r['v_disc']:<3} {extra}")
    print()
    print(f"  lemma 1  gcd n_ℓ = {l1['gcd']}   failures: {l1['failure_set']}")
    for r in l2["rows"]:
        print(f"  lemma 2  p = {r['p']:<4} witness ℓ = {r['witness']} "
              f"(n = {r['n_at_witness']})")
    print(f"  lemma 3  nonsplit {l3['nonsplit_primes']} "
          f"({l3['survived_the_restriction']})  gcd = {l3['gcd']}   "
          f"failures: {l3['failure_set']}")
    print(f"           redundancy: {l3['redundancy']}")
    print()
    am = empty["multiplicative_but_all_split"]
    nm = empty["no_multiplicative_primes"]
    print(f"  the empty set, over {empty['models_scanned']} models scanned")
    if nm:
        print(f"    no multiplicative primes  {nm['ainvs']}  "
              f"lemma 1 gcd = {nm['lemma1_gcd']} → {nm['lemma1_failure_set']}")
    if am:
        print(f"    all split                 {am['ainvs']}  "
              f"mult {am['multiplicative']}  lemma 1 gcd = {am['lemma1_gcd']}, "
              f"lemma 3 gcd = {am['lemma3_gcd']}")
        print(f"      → lemma 3 failure set: {am['lemma3_failure_set']}")
    print()
    f = fam_rows
    print(f"  the family: {f['members']} members below {f['bound']}")
    print(f"    multiplicative still exactly (3, 29) with n = 1: "
          f"{f['every_member_matches_case_C']}")
    print(f"    q additive for its own twist:                     "
          f"{f['every_member_has_q_additive']}")
    print(f"    both gcds equal 1 for every member:               "
          f"{f['gcds_all_one']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
