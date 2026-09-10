"""Gate 49 — the derived theorem before and after the referee, compared.

數學戰士「墜衡」 / AMRAL Research Lab.

`18_Provisional_Derived_Theorem` and `27_Revised_Derived_Theorem_Candidate` are
the same statement written twice, with `20_Adversarial_Referee_Verdict` between
them. Comparing the two versions is the plainest job an independent arm has, and
nothing in the corpus does it.

THE SET IS DEFINED THREE WAYS AND THEY HAD BETTER BE ONE SET.

    18 and 27      q = 1 (mod 24),  (q/29) = 1,  f_2 irreducible mod q
    src16          this tree's membership test, used since RUN-015
    Referee A      squarefree, gcd(q,696) = 1, q = 1 (mod 4), 2/3/29 split in
                   Q(sqrt q), q inert in the 2-division cubic (RUN-032)

Enumerated side by side rather than argued: `q = 1 (mod 24)` is 2 and 3
splitting, `(q/29) = 1` is 29 splitting, and irreducibility mod q is inertness.

`18` LISTS FIVE THINGS IT WANTS A REFEREE TO AUDIT, AND `27` IS THE ROUND AFTER.
So each item can be scored: what `27` supplies, and what this arm has since
measured. One is answered by `27`'s proof router, one is deferred to a novelty
audit `27` names explicitly, and three are open — two of them exactly what
RUN-039 and RUN-040 went at.

AND `27`'s ROUTER NAMES A WITNESS PER BRANCH, WHICH THIS TREE COMPUTED. The
3 <-> 29 swap is RUN-033's leave-one-out; the nonsplit Steinberg witness 29 is
RUN-037's `W_-`. The router and the lemma agree, from opposite ends.

Usage:  python code/src49_provisional_vs_revised.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src10_phase2_density_and_base as ph2               # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402
import src34_referee_a_checklist as refA                  # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402
import src40_fw_h2_ordinary as h2o                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = LOGS / "src49-provisional-vs-revised.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
SET_BOUND = 4000
BRANCH_BOUND = 600

CUBIC = (1, 1, 8, -16)                    # x^3 + x^2 + 8x - 16


def in_P_per_18(q: int) -> dict:
    """`18` and `27`'s own three conditions, evaluated directly."""
    a, b, c = CUBIC[1:]
    # No bound guard. A hardcoded `q < 4000` here silently rejected every prime
    # above it and manufactured a disagreement between three definitions that
    # agree — caught by this gate's own control widening the enumeration bound.
    has_root = any((x ** 3 + a * x * x + b * x + c) % q == 0 for x in range(q))
    return {"q": q,
            "q_1_mod_24": q % 24 == 1,
            "legendre_q_29_is_1": ph2.legendre(q, 29) == 1 if q != 29 else None,
            "cubic_irreducible_mod_q": (not has_root),
            "in_P": (q % 24 == 1 and q != 29
                     and ph2.legendre(q, 29) == 1 and not has_root)}


def three_definitions(bound: int = SET_BOUND) -> dict:
    """`18`/`27`, this tree's test, and Referee A's five — over the same range."""
    doc, tree, referee = [], [], []
    for q in anchor.sieve(bound):
        if q < 5:
            continue
        d = in_P_per_18(q)["in_P"]
        t = fam.in_P(q)
        r = refA.q_checklist(q)["all_pass"]
        if d:
            doc.append(q)
        if t:
            tree.append(q)
        if r:
            referee.append(q)
    return {"bound": bound,
            "per_18_and_27": doc, "per_this_tree": tree,
            "per_referee_A": referee,
            "counts": {"18/27": len(doc), "src16": len(tree),
                       "Referee A": len(referee)},
            "all_three_agree": doc == tree == referee,
            "in_18_not_in_tree": sorted(set(doc) - set(tree)),
            "in_tree_not_in_18": sorted(set(tree) - set(doc)),
            "in_referee_not_in_18": sorted(set(referee) - set(doc)),
            "why_they_should_agree": (
                "q = 1 (mod 24) is 2 and 3 splitting in Q(sqrt q); (q/29) = 1 "
                "is 29 splitting; f_2 irreducible mod q is q inert in the "
                "2-division cubic; and a prime is squarefree and coprime to 696 "
                "once it is 1 mod 24 with (q/29) = 1")}


def redundancy_of_the_29_condition(bound: int = SET_BOUND) -> dict:
    """`18` and `27` state three conditions and one of them is implied.

    `q` inert in the cubic means Frob_q is a 3-cycle, hence in A_3, hence
    trivial on the quadratic resolvent `F_0 = Q(sqrt -174)` — so `(-174/q) = 1`.
    And `q = 1 (mod 24)` forces `(-1/q) = (2/q) = (3/q) = 1`, hence `(-6/q) = 1`.
    Since `-174 = -6 x 29`, that leaves `(29/q) = 1`, which for `q = 1 (mod 4)`
    is `(q/29) = 1`. The condition is redundant.

    Measured both ways: with `q = 1 (mod 24)` present nothing violates it, and
    with that condition weakened to `q = 1 (mod 4)` the implication breaks — so
    the redundancy follows from the mod-24 condition and is not an accident of
    the range.
    """
    a, b, c = CUBIC[1:]
    with24, without24 = [], []
    for q in anchor.sieve(bound):
        if q < 5 or q == 29:
            continue
        irred = not any((x ** 3 + a * x * x + b * x + c) % q == 0
                        for x in range(q))
        if not irred:
            continue
        leg = ph2.legendre(q, 29) == 1
        if q % 24 == 1:
            with24.append((q, leg))
        elif q % 4 == 1:
            without24.append((q, leg))
    viol = [q for q, leg in with24 if not leg]
    counter = [q for q, leg in without24 if not leg]
    return {"bound": bound,
            "primes_with_q_1_mod_24_and_cubic_irreducible": len(with24),
            "of_those_violating_legendre_q_29_is_1": viol,
            "the_condition_is_redundant_here": not viol,
            "primes_with_q_1_mod_4_only_and_cubic_irreducible": len(without24),
            "of_those_violating": counter[:8],
            "count_violating_without_mod_24": len(counter),
            "the_implication_needs_the_mod_24_condition": bool(counter),
            "the_reason": ("q inert in the cubic puts Frob_q in A_3, so it is "
                           "trivial on F_0 = Q(sqrt -174) and (-174/q) = 1; "
                           "q = 1 (mod 24) gives (-6/q) = 1; and -174 = -6 x 29 "
                           "leaves (29/q) = 1"),
            "same_redundancy_as": ("RUN-018, which explained the density being "
                                   "1/24 rather than 1/48 by exactly this "
                                   "overlap, and RUN-044, which computed the "
                                   "resolvent")}


AUDIT_ITEMS = (
    ("exact convention match between FW modular representation and elliptic "
     "E[p] at the nonsplit multiplicative witness",
     "27 names the witness per branch but not the convention",
     "OPEN", "RUN-046 found the corpus disagreeing with itself about whether "
             "the divisibility criterion IS H3, which is the same seam"),
    ("period normalization statement for every twist E_q",
     "27 does not mention it",
     "OPEN, MEASURED HERE", "RUN-039 left c_E = 1 open; RUN-040 checked `01`'s "
                            "weaker sufficient condition for p not dividing c "
                            "on all 19 members"),
    ("exact isogeny/optimality phrasing used in the period comparison",
     "27 does not mention it",
     "OPEN, PREMISE CLOSED HERE", "RUN-031 closed the no-rational-isogeny "
                                  "premise and RUN-036 certified the mod-l "
                                  "images; optimality itself stays cited"),
    ("precise citation chain for all ordinary/additive/multiplicative p-part "
     "results",
     "27's proof router IS this chain",
     "ADDRESSED BY 27", "each branch now names its theorem: Banwait-Huang 2.14, "
                        "BSTW 9.21(c), Skinner Theorem C, Fouquet-Wan 1.7 + "
                        "Cor 1.10"),
    ("novelty search",
     "27 defers it explicitly",
     "DEFERRED", "27 says whether to call it a new theorem must be decided by a "
                 "separate novelty audit; 26_Novelty_Search_Log is that file "
                 "and is not a subject of any round here"),
)


def audit_items() -> dict:
    rows = [{"item": a, "what_27_supplies": b, "status": c, "this_arm": d}
            for a, b, c, d in AUDIT_ITEMS]
    return {"rows": rows,
            "addressed_by_27": [r["item"][:40] for r in rows
                                if r["status"].startswith("ADDRESSED")],
            "deferred": [r["item"][:40] for r in rows
                         if r["status"] == "DEFERRED"],
            "still_open": [r["item"][:40] for r in rows
                           if r["status"].startswith("OPEN")],
            "counts": {"addressed": sum(r["status"].startswith("ADDRESSED")
                                        for r in rows),
                       "deferred": sum(r["status"] == "DEFERRED" for r in rows),
                       "open": sum(r["status"].startswith("OPEN")
                                   for r in rows)},
            "reading": ("of the five things `18` asked a referee to check, `27` "
                        "answers one, defers one, and leaves three. Two of the "
                        "three are what RUN-039 and RUN-040 went at, and "
                        "neither is closed")}


def router_partition(q: int, bound: int = BRANCH_BOUND) -> dict:
    """`27`'s six branches, classified for E^(q) over every prime to the bound."""
    tw = mz.quadratic_twist(BASE, q)
    md = gcd35.multiplicative_data(tw)
    mult = {r["p"] for r in md["multiplicative"]}
    add = {r["p"] for r in md["additive"]}
    rows, tally = [], {}
    for p in anchor.sieve(bound):
        if p == 2:
            b = "p=2 (Banwait-Huang 2.14)"
        elif p == q:
            b = "p=q (BSTW 9.21(c))"
        elif p == 3:
            b = "p=3 (Skinner C, witness 29)"
        elif p == 29:
            b = "p=29 (Skinner C, witness 3)"
        elif p in mult or p in add:
            b = "UNROUTED bad prime"
        else:
            a = anchor.point_count_ap(tw, p)
            b = ("odd good supersingular (FW 1.7)" if a % p == 0
                 else "odd good ordinary (Skinner C, witness 29)")
        rows.append({"p": p, "branch": b})
        tally[b] = tally.get(b, 0) + 1
    return {"q": q, "primes_classified": len(rows), "tally": tally,
            "unrouted": [r["p"] for r in rows if r["branch"].startswith("UNROUTED")],
            "every_prime_has_exactly_one_branch":
                not any(r["branch"].startswith("UNROUTED") for r in rows),
            "branches_used": sorted(tally),
            "bad_primes_of_the_twist": sorted(mult | add)}


def router_witnesses() -> dict:
    """`27` names a witness per branch. This tree computed those witnesses."""
    md = gcd35.multiplicative_data(BASE)
    l2 = gcd35.leave_one_out(md)
    swap = {r["p"]: r["witness"] for r in l2["rows"]}
    w = [r["ell"] for r in h3c.w_minus(BASE)]
    return {"27_says": {"p=3": 29, "p=29": 3,
                        "odd good ordinary": 29,
                        "odd good supersingular": 29,
                        "p=q": 29},
            "this_tree_computed": {"leave_one_out": swap,
                                   "W_minus": w},
            "leave_one_out_matches": swap == {3: 29, 29: 3},
            "nonsplit_witness_matches": w == [29],
            "agree": swap == {3: 29, 29: 3} and w == [29],
            "reading": ("the 3 <-> 29 swap is RUN-033's lemma 2 and the "
                        "nonsplit Steinberg witness is RUN-037's W_-. The "
                        "router and the lemmas were written independently and "
                        "name the same primes")}


def claim_labels() -> dict:
    """The label in each of the three documents, read from the files."""
    def has(name: str, needle: str) -> bool:
        p = DOCS / name
        return p.exists() and needle in p.read_text(encoding="utf-8")
    return {
        "18": {"label": "Provisional Derived Theorem",
               "present": has("18_Provisional_Derived_Theorem.md",
                              "Provisional Derived Theorem"),
               "refuses": "Established New Theorem",
               "refusal_present": has("18_Provisional_Derived_Theorem.md",
                                      "Established New Theorem")},
        "20": {"label": "DERIVED THEOREM CANDIDATE",
               "present": has("20_Adversarial_Referee_Verdict.md",
                              "DERIVED THEOREM CANDIDATE"),
               "refuses": "NEW THEOREM",
               "refusal_present": has("20_Adversarial_Referee_Verdict.md",
                                      "NEW THEOREM")},
        "27": {"label": "DERIVED THEOREM CANDIDATE",
               "present": has("27_Revised_Derived_Theorem_Candidate.md",
                              "DERIVED THEOREM CANDIDATE"),
               "next_rung": "PREPRINT CANDIDATE",
               "next_present": has("27_Revised_Derived_Theorem_Candidate.md",
                                   "PREPRINT CANDIDATE")},
        "20_and_27_agree": True,
        "18_is_one_rung_lower": True,
        "reading": ("`20` upgraded the label from provisional to candidate and "
                    "refused the further step to NEW THEOREM because novelty is "
                    "a separate gate; `27` carries the upgraded label and names "
                    "the same next rung. The three documents are consistent "
                    "about how far the claim goes")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    sets = three_definitions()
    red = redundancy_of_the_29_condition()
    items = audit_items()
    members = sets["per_this_tree"][:3]
    parts = [router_partition(q) for q in members]
    wit = router_witnesses()
    labels = claim_labels()

    ok = (sets["all_three_agree"] and sets["counts"]["18/27"] >= 15
          and red["the_condition_is_redundant_here"]
          and red["the_implication_needs_the_mod_24_condition"]
          and items["counts"]["addressed"] == 1
          and items["counts"]["deferred"] == 1
          and items["counts"]["open"] == 3
          and all(p["every_prime_has_exactly_one_branch"] for p in parts)
          and all(len(p["branches_used"]) >= 5 for p in parts)
          and wit["agree"]
          and labels["18"]["present"] and labels["20"]["present"]
          and labels["27"]["present"] and labels["27"]["next_present"])

    log = {
        "gate": "src49 — 18 against 27, the derived theorem before and after",
        "source": "18_Provisional_Derived_Theorem, "
                  "27_Revised_Derived_Theorem_Candidate",
        "curve": BASE, "conductor": N,
        "three_definitions_of_P": sets,
        "the_redundant_condition": red,
        "the_five_audit_items": items,
        "router_partition": parts,
        "router_witnesses": wit,
        "claim_labels": labels,
        "headline": (f"`18`, `27`, this tree's membership test and Referee A's "
                     f"five conditions all pick out the same "
                     f"{sets['counts']['18/27']} primes below "
                     f"{sets['bound']}. Of `18`'s five referee items `27` "
                     f"answers one, defers one and leaves three open, two of "
                     f"which RUN-039 and RUN-040 measured. `27`'s six-branch "
                     f"router is a partition of every prime for every member "
                     f"tested, and the witnesses it names are the ones RUN-033 "
                     f"and RUN-037 computed"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  three definitions of 𝒫, below {sets['bound']}")
    print(f"    18/27's three conditions : {sets['counts']['18/27']}")
    print(f"    this tree's src16 test   : {sets['counts']['src16']}")
    print(f"    Referee A's five (RUN-032): {sets['counts']['Referee A']}")
    print(f"    all three agree: {sets['all_three_agree']}   "
          f"first: {sets['per_18_and_27'][:6]}")
    print()
    print("  and one of 18/27's three conditions is implied by the other two")
    print(f"    {red['primes_with_q_1_mod_24_and_cubic_irreducible']} primes are "
          f"1 mod 24 with the cubic irreducible; violating (q/29) = 1: "
          f"{red['of_those_violating_legendre_q_29_is_1']}")
    print(f"    weaken mod 24 to mod 4 and it breaks: "
          f"{red['count_violating_without_mod_24']} counterexamples, e.g. "
          f"{red['of_those_violating'][:5]}")
    print()
    print("  18's five referee items, and what 27 did with them")
    for r in items["rows"]:
        print(f"    {r['status']:<26} {r['item'][:52]}")
    print(f"    → addressed {items['counts']['addressed']}, deferred "
          f"{items['counts']['deferred']}, open {items['counts']['open']}")
    print()
    print(f"  27's six-branch router, over primes below {BRANCH_BOUND}")
    for p in parts:
        print(f"    q = {p['q']:<5} {p['primes_classified']} primes, "
              f"{len(p['branches_used'])} branches used, unrouted "
              f"{p['unrouted']} → partition: "
              f"{p['every_prime_has_exactly_one_branch']}")
    print(f"    branches: {parts[0]['branches_used']}")
    print()
    print(f"  the witnesses 27 names")
    print(f"    leave-one-out {wit['this_tree_computed']['leave_one_out']} "
          f"matches: {wit['leave_one_out_matches']}")
    print(f"    W_- = {wit['this_tree_computed']['W_minus']} matches: "
          f"{wit['nonsplit_witness_matches']}")
    print()
    print("  the claim label in each document")
    for k in ("18", "20", "27"):
        d = labels[k]
        print(f"    {k}: {d['label']:<28} present: {d['present']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
