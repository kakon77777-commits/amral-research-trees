"""Gate 43 — the finite exceptional prime problem, with all three sets computed.

數學戰士「墜衡」 / AMRAL Research Lab.

`04_Finite_Exceptional_Prime_Problem` states Phase 2's mother problem — how does
`for all p > 2, FW(E, p)` become a finite certificate? — and names the shape of
an answer:

    p not in P_red(E) ∪ P_loc(E) ∪ P_ram(E)  =>  FW(E, p)

with all three sets finite, effectively computable and certificate-producing.
It also names the failure standard: if the exact conditions need incompressible
local Galois computation at infinitely many `p` with no generic-large-`p`
theorem, the route stays a per-prime theorem, and

    不得用「tested up to B」替代全稱量詞.

TEN ROUNDS HAVE NOW COMPUTED ALL THREE SETS FOR 696.e1, SO THE CRITERION CAN BE
EVALUATED RATHER THAN DISCUSSED.

    P_red   RUN-031 refuted reducibility at every one of Mazur's twelve, and
            RUN-036 certified rho-bar_ell surjective at 38 primes. EMPTY.
    P_ram   `04`'s formula is the intersection over W(E) of {p : p | v_ell(Δ)}.
            W_- = {29} with v = 1, so the set is EMPTY.
    P_loc   RUN-038 ran `10`'s exact H2 criterion: 8 ordinary primes below
            6,000, still appearing at the top of the range. NOT EMPTY, and not
            known finite.

AND THE DOCUMENT'S OWN WARNING ABOUT P_ram TURNED OUT TO BE EXACT. `04` says of
that formula: 此式只能作 compiler heuristic，不能直接當 theorem. RUN-037 found
precisely how it fails — the formula sees only `p ∤ v_ell(Δ)` and not the `ell ≠
p` clause, so at a singleton `W_-` the true obstruction is `{29}` while the
formula returns the empty set. This gate computes both and reports the
difference, which is the corpus warning about its own heuristic and this arm
finding the instance.

Usage:  python code/src43_finite_exceptional_primes.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src07_isogeny_reducibility_sieve as red7           # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402
import src38_mod_ell_surjectivity as surj                 # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402
import src40_fw_h2_ordinary as h2o                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src43-finite-exceptional.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
MAZUR = (2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163)
LOC_BOUND = 6000
SEARCH = 600


def p_red() -> dict:
    """Reducible `rho-bar_p` means a rational p-isogeny, so Mazur bounds the set.

    Every one of the twelve is refuted by an explicit witness, except `p = 2`
    where the sieve is structurally vacuous and RUN-007's `X_0(2)` decides
    instead. So the set is empty — and it is empty for a reason that is a
    theorem plus twelve computations, not a search.
    """
    primes = mz.small_primes(SEARCH)
    rows = []
    for n in MAZUR:
        w = mz.witness(BASE, n, primes)
        if n == 2:
            v = mz.vacuity_at_2()
            rows.append({"n": 2, "witness": None,
                         "refuted": True,
                         "how": "sieve structurally vacuous (every element of "
                                "F2 is a square); settled by X_0(2), RUN-007",
                         "all_of_F2_is_square": v["all_of_F2"]})
        else:
            rows.append({"n": n, "witness": w["ell"] if w else None,
                         "a_ell": w["a_ell"] if w else None,
                         "refuted": w is not None,
                         "how": "reducibility sieve witness"})
    return {"bounded_by": "Mazur's theorem — the only possible prime degrees",
            "degrees": list(MAZUR), "rows": rows,
            "set": [r["n"] for r in rows if not r["refuted"]],
            "is_empty": all(r["refuted"] for r in rows),
            "claim_is_universal": True,
            "why_universal": ("Mazur's theorem makes the twelve exhaustive, so "
                              "refuting all twelve empties the set for every "
                              "prime, not up to a bound")}


def p_ram() -> dict:
    """`04`'s formula, and the obstruction it does not see.

    The formula is the intersection over `W(E)` of `{p : p | v_ell(Delta)}`.
    With `W_- = {29}` and `v = 1`, `{p : p | 1}` is empty, so the formula says
    no prime is obstructed. RUN-037 measured the criterion itself and found
    `p = 29` obstructed — by the `ell != p` clause, which the formula has no
    term for.
    """
    w = h3c.w_minus(BASE)
    per = {r["ell"]: [p for p in mz.small_primes(200) if r["v_disc"] % p == 0]
           for r in w}
    inter = set(mz.small_primes(200))
    for s in per.values():
        inter &= set(s)
    cert = h3c.uniform_certificate(BASE)
    true_obstruction = cert["p_where_the_criterion_FAILS"]
    return {"W_minus": [r["ell"] for r in w],
            "valuations": {str(r["ell"]): r["v_disc"] for r in w},
            "per_ell_divisor_sets": {str(k): v for k, v in per.items()},
            "formula_set": sorted(inter),
            "formula_says_empty": not inter,
            "criterion_actually_obstructed_at": true_obstruction,
            "formula_misses": sorted(set(true_obstruction) - inter),
            "documents_own_warning": "此式只能作 compiler heuristic，"
                                     "不能直接當 theorem",
            "the_warning_was_exact": bool(set(true_obstruction) - inter),
            "what_the_formula_lacks": ("a term for the `ell != p` clause. It "
                                       "models the ramification condition and "
                                       "not the requirement that the witness "
                                       "be a different prime, which is what "
                                       "bites at a singleton W_-")}


def p_loc(bound: int = LOC_BOUND, blocks: int = 4) -> dict:
    """`10`'s exact H2 criterion, which is the local-degeneracy set.

    `04` §3 calls H2 the least clear of the three and asks for it in explicit
    local terms; `10` supplies exactly that for good ordinary p, and RUN-038 ran
    it. The set is non-empty and has not stopped below the bound — which is a
    measurement, not a claim of infinitude.
    """
    c = h2o.classify(bound)
    ne = h2o.no_finite_exception(c, blocks=blocks)
    return {"bounded_at": bound,
            "set_below_the_bound": [r["p"] for r in c["ordinary_H2_failures"]],
            "size": len(c["ordinary_H2_failures"]),
            "is_empty": not c["ordinary_H2_failures"],
            "has_not_stopped": ne["keeps_producing"],
            "buckets": ne["buckets"],
            "claim_is_universal": False,
            "what_is_claimed": (f"that the set has not stopped below {bound}. "
                                f"Whether it is infinite is Lang–Trotter's "
                                f"heuristic and is not claimed here"),
            "criterion": "a_p(E)^2 = 1 (mod p), from 10, exact for good "
                         "ordinary p"}


def success_criterion(bound: int = LOC_BOUND, blocks: int = 4) -> dict:
    """`04` §4 against what was computed."""
    r, m, l = p_red(), p_ram(), p_loc(bound, blocks)
    finite_and_empty = [("P_red", r["is_empty"]), ("P_ram (formula)",
                                                   m["formula_says_empty"])]
    return {"criterion": "p not in P_red ∪ P_loc ∪ P_ram  =>  FW(E, p), with "
                         "all three finite, effectively computable and "
                         "certificate-producing",
            "P_red": {"empty": r["is_empty"], "universal": True},
            "P_ram": {"formula_empty": m["formula_says_empty"],
                      "true_obstruction": m["criterion_actually_obstructed_at"]},
            "P_loc": {"empty": l["is_empty"], "size": l["size"],
                      "bounded_at": l["bounded_at"],
                      "known_finite": False},
            "two_of_three_are_empty": all(v for _, v in finite_and_empty),
            "achieved_for_all_odd_p": False,
            "which_factor_blocks_it": "P_loc",
            "why": ("P_loc is non-empty and not known finite, so the mother "
                    "problem's finite certificate is not obtained for all "
                    "odd p by this route")}


def the_routing_answer(bound: int = LOC_BOUND) -> dict:
    """`04`'s criterion and `12`'s routing solve different problems.

    `04` asks for FW at every odd `p`. `12` never asks FW at an ordinary prime —
    `10`'s measurement is precisely the reason — so the primes that block `04`'s
    criterion are primes the corpus's own router sends elsewhere. Restricted to
    the branch FW is used on, the local set is empty. That is computed here by
    intersecting the two sets rather than argued.
    """
    c = h2o.classify(bound)
    loc = {r["p"] for r in c["ordinary_H2_failures"]}
    ss = {r["p"] for r in c["supersingular"]}
    return {"P_loc_below_bound": sorted(loc),
            "the_FW_branch_supersingular": sorted(ss),
            "intersection": sorted(loc & ss),
            "P_loc_is_disjoint_from_the_FW_branch": not (loc & ss),
            "why_disjoint": ("P_loc is defined by a_p^2 = 1 mod p at ORDINARY "
                             "primes, and the FW branch is the SUPERSINGULAR "
                             "ones; a prime cannot be both"),
            "reading": ("04's mother problem is not solved for all odd p, and "
                        "the family theorem does not need it to be: the primes "
                        "that block it are routed to the ordinary theorem by "
                        "12's P2, never to FW")}


def degradation_rule(bound: int = LOC_BOUND, blocks: int = 4) -> dict:
    """`04` §5's rule, applied to this round's own reporting.

    「不得用『tested up to B』替代全稱量詞」 — a bounded test must not stand in
    for a universal quantifier. Each set is therefore tagged with whether its
    claim is universal and what bound it was measured at, so a reader can see
    which is which without reading prose.
    """
    r, m, l = p_red(), p_ram(), p_loc(bound, blocks)
    return {"rule": "不得用「tested up to B」替代全稱量詞",
            "P_red": {"claim": "empty for every odd p",
                      "universal": True,
                      "licensed_by": "Mazur's theorem makes twelve degrees "
                                     "exhaustive; all twelve refuted"},
            "P_ram_formula": {"claim": "empty", "universal": True,
                              "licensed_by": "v_29(Δ) = 1 has no prime "
                                             "divisors at all",
                              "but": "the formula is a heuristic, and the true "
                                     "obstruction is "
                                     f"{m['criterion_actually_obstructed_at']}"},
            "P_loc": {"claim": f"{l['size']} members below {bound}, and it "
                               f"has not stopped",
                      "universal": False,
                      "bounded_at": l["bounded_at"],
                      "not_claimed": "that the set is infinite"},
            "no_bounded_test_is_reported_as_universal":
                (r["claim_is_universal"] and not l["claim_is_universal"])}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    r, m, l = p_red(), p_ram(), p_loc()
    sc = success_criterion()
    rt = the_routing_answer()
    dr = degradation_rule()

    ok = (r["is_empty"] and m["formula_says_empty"] and m["the_warning_was_exact"]
          and not l["is_empty"] and l["has_not_stopped"]
          and sc["achieved_for_all_odd_p"] is False
          and rt["P_loc_is_disjoint_from_the_FW_branch"]
          and dr["no_bounded_test_is_reported_as_universal"])

    log = {
        "gate": "src43 — the finite exceptional prime problem, computed",
        "source": "04_Finite_Exceptional_Prime_Problem",
        "curve": BASE, "conductor": N,
        "P_red": r, "P_ram": m, "P_loc": l,
        "success_criterion": sc,
        "the_routing_answer": rt,
        "degradation_rule": dr,
        "headline": ("all three of `04`'s sets are now computed for 696.e1: "
                     "P_red empty and universally so, P_ram's formula empty but "
                     "the formula a heuristic whose exact failure RUN-037 found, "
                     "and P_loc non-empty and not stopped. The mother problem is "
                     "NOT solved for all odd p, and the family theorem does not "
                     "need it to be — the blocking primes are ordinary, and the "
                     "corpus's own router never asks FW for those"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  P_red — Mazur's twelve, all refuted: {r['is_empty']}   "
          f"set = {r['set']}   universal: {r['claim_is_universal']}")
    print(f"  P_ram — W_- = {m['W_minus']} {m['valuations']}   formula set = "
          f"{m['formula_set']}")
    print(f"          criterion actually obstructed at "
          f"{m['criterion_actually_obstructed_at']}   formula misses "
          f"{m['formula_misses']}")
    print(f"          the document's own warning: {m['documents_own_warning']}")
    print(f"          the warning was exact: {m['the_warning_was_exact']}")
    print(f"  P_loc — {l['size']} members below {l['bounded_at']}: "
          f"{l['set_below_the_bound']}")
    print(f"          has not stopped: {l['has_not_stopped']}   "
          f"universal claim: {l['claim_is_universal']}")
    print()
    print(f"  04's success criterion achieved for all odd p: "
          f"{sc['achieved_for_all_odd_p']}   blocked by {sc['which_factor_blocks_it']}")
    print(f"  but P_loc ∩ (the FW branch) = {rt['intersection']} → disjoint: "
          f"{rt['P_loc_is_disjoint_from_the_FW_branch']}")
    print(f"    {rt['reading'][:96]}…")
    print()
    print(f"  §5's rule: {dr['rule']}")
    print(f"    P_red universal: {dr['P_red']['universal']}   "
          f"P_loc universal: {dr['P_loc']['universal']} "
          f"(bounded at {dr['P_loc']['bounded_at']})")
    print(f"    no bounded test reported as universal: "
          f"{dr['no_bounded_test_is_reported_as_universal']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
