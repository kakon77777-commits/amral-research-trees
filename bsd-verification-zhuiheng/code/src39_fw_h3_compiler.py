"""Gate 39 — the FW-H3 compiler, run, and the clause its boxed certificate drops.

數學戰士「墜衡」 / AMRAL Research Lab.

`09_FW_H3_Exact_Compiler` is the document RUN-033 and RUN-035 have been circling.
It defines

    W_-(E) = { ell : ell || N_E, E nonsplit multiplicative at ell }

    FW-H3(E, p)  <=>  exists ell in W_-(E),  ell != p,  p does not divide
                      v_ell(Delta_min)

and then offers a uniform certificate: with

    g_-(E) = gcd over ell in W_-(E) of v_ell(Delta_min),

if `W_-(E)` is non-empty and `g_-(E) = 2^a` then no odd prime divides all the
witness valuations, so

    for all p > 2,  FW-H3(E, p) = PASS,

on a single finite base certificate.

THE GCD ARGUMENT DOES NOT SEE THE `ell != p` CLAUSE. It shows no odd `p` divides
every witness valuation, which is the third condition. The second one removes
`ell = p` from the candidates, and when `W_-(E)` is a **singleton** that removes
the only candidate there is. For 696.e1, RUN-033 measured `W_- = {29}` — one
witness, no spare — so the boxed `for all p > 2` is false at exactly one prime,
and this gate finds it by testing the criterion against the conclusion rather
than by arguing.

WHETHER THAT MATTERS IS A ROUTING QUESTION, AND THE ANSWER IS NO — for this
curve. `12_Hybrid_Odd_Prime_Router` sends a fixed multiplicative `p | N` to P3,
the leave-one-out over *all* multiplicative primes, not to FW; RUN-033 ran that
and found `p = 29` takes `ell = 3`. So the family theorem survives the gap
because 29 never asks FW-H3 in the first place. Both halves are reported.

Usage:  python code/src39_fw_h3_compiler.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src39-fw-h3.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
P_BOUND = 400                             # odd p at which the criterion is run
FAMILY_BOUND = 4000
SEARCH_BOX = 8


def w_minus(ainvs: list[int]) -> list[dict]:
    """W_-(E): the nonsplit multiplicative primes, with their valuations.

    `ell || N` is multiplicative reduction, so the set is read off Tate's
    algorithm rather than off the conductor separately.
    """
    md = gcd35.multiplicative_data(ainvs)
    if md.get("singular"):
        return []
    return [{"ell": r["p"], "v_disc": r["n"]} for r in md["nonsplit"]]


def g_minus(w: list[dict]) -> int:
    """gcd of the witness valuations. 0 when W_- is empty, which is the case the
    document's premise excludes and the reason it excludes it."""
    return math.gcd(*[r["v_disc"] for r in w]) if w else 0


def is_power_of_two(n: int) -> bool:
    return n > 0 and n & (n - 1) == 0


def h3(w: list[dict], p: int) -> dict:
    """The criterion exactly as written, `ell != p` included."""
    usable = [r for r in w if r["ell"] != p and r["v_disc"] % p]
    excluded = [r["ell"] for r in w if r["ell"] == p]
    return {"p": p, "witness": usable[0]["ell"] if usable else None,
            "pass": bool(usable),
            "candidates_excluded_by_ell_neq_p": excluded}


def uniform_certificate(ainvs: list[int], bound: int = P_BOUND) -> dict:
    """The document's premise, its boxed conclusion, and the conclusion tested.

    The test is the point: the certificate is evaluated for every odd `p` up to
    the bound by the criterion itself, and any `p` where the two disagree is
    reported. A certificate that is only ever restated cannot be wrong.
    """
    w = w_minus(ainvs)
    g = g_minus(w)
    premise = bool(w) and is_power_of_two(g)
    rows = [h3(w, p) for p in anchor.sieve(bound) if p > 2]
    failures = [r for r in rows if not r["pass"]]
    return {"W_minus": [r["ell"] for r in w],
            "valuations": {str(r["ell"]): r["v_disc"] for r in w},
            "g_minus": g,
            "g_minus_is_a_power_of_two": is_power_of_two(g),
            "premise_holds": premise,
            "boxed_conclusion": "for all p > 2, FW-H3(E, p) = PASS",
            "odd_p_tested": len(rows),
            "p_where_the_criterion_FAILS": [r["p"] for r in failures],
            "why_they_fail": [
                {"p": r["p"],
                 "reason": f"W_- = {[x['ell'] for x in w]} and the ell != p "
                           f"clause removes "
                           f"{r['candidates_excluded_by_ell_neq_p']}, leaving "
                           f"no candidate"}
                for r in failures],
            "conclusion_holds_as_stated": not failures,
            "the_gap": ("the gcd argument establishes the third clause only. "
                        "The second, ell != p, is invisible to it, and when "
                        "W_- is a singleton it removes the only candidate"
                        if failures else "none found below the bound")}


def routing_answer(bound: int = P_BOUND) -> dict:
    """Does the gap reach the family theorem? Only if such a p asks FW-H3.

    `12_Hybrid_Odd_Prime_Router` P3 routes a fixed multiplicative `p | N` to the
    leave-one-out over ALL multiplicative primes, which is `00_GCD_Witness_Lemmas`
    lemma 2 and not FW. So the question is whether every failing `p` is one the
    router sends elsewhere, and whether that other branch has a witness.
    """
    cert = uniform_certificate(BASE, bound)
    md = gcd35.multiplicative_data(BASE)
    mult = [r["p"] for r in md["multiplicative"]]
    l2 = gcd35.leave_one_out(md)
    rows = []
    for p in cert["p_where_the_criterion_FAILS"]:
        in_mult = p in mult
        alt = next((r for r in l2["rows"] if r["p"] == p), None)
        rows.append({"p": p,
                     "is_a_fixed_multiplicative_prime": in_mult,
                     "router_branch": "P3 (fixed multiplicative)" if in_mult
                                      else "NOT routed away — this would reach FW",
                     "P3_witness": alt["witness"] if alt else None,
                     "P3_witness_is_split": (alt is not None and alt["witness"]
                                             is not None
                                             and alt["witness"] not in
                                             [x["ell"] for x in w_minus(BASE)]),
                     "covered": in_mult and alt is not None
                                and alt["witness"] is not None})
    return {"failing_p": cert["p_where_the_criterion_FAILS"], "rows": rows,
            "every_failing_p_is_routed_away": all(r["covered"] for r in rows),
            "reading": ("the gap is real in the document's stated generality "
                        "and does not reach this family, because every p where "
                        "FW-H3 has no witness is a fixed multiplicative prime "
                        "that P3 takes instead — with a witness FW-H3 could not "
                        "have used, since it is split")}


def family(bound: int = FAMILY_BOUND) -> dict:
    """W_-, g_- and the failing set for every member's twist.

    `09`'s last section claims the H3 witness is preserved along the family
    whenever every `ell | N` splits in `Q(sqrt d)` — which is `03`'s lemma C,
    measured in RUN-035. This runs the compiler itself on each member.
    """
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = []
    for q in members:
        tw = mz.quadratic_twist(BASE, q)
        c = uniform_certificate(tw, 200)
        rows.append({"q": q, "W_minus": c["W_minus"], "g_minus": c["g_minus"],
                     "premise_holds": c["premise_holds"],
                     "failing_p": c["p_where_the_criterion_FAILS"]})
    base = uniform_certificate(BASE, 200)
    return {"members": len(members), "rows": rows,
            "W_minus_identical_to_the_base_for_every_member":
                all(r["W_minus"] == base["W_minus"] for r in rows),
            "g_minus_identical": all(r["g_minus"] == base["g_minus"]
                                     for r in rows),
            "same_failing_set": all(
                r["failing_p"] == base["p_where_the_criterion_FAILS"]
                for r in rows),
            "base_W_minus": base["W_minus"], "base_g_minus": base["g_minus"]}


def premise_failures(box: int = SEARCH_BOX) -> dict:
    """Curves where the certificate's premise correctly refuses.

    Two shapes: `W_-` empty, where `g_- = 0` is not a power of two and the
    document's own condition rules the curve out; and `g_-` divisible by an odd
    prime, where the certificate must not fire and that odd prime really does
    fail the criterion. Without both, "the premise holds for 696.e1" is a fact
    about one curve rather than a test of the premise.
    """
    empty, odd_g = None, None
    scanned = 0
    for ai in gcd35.small_curves(box):
        scanned += 1
        w = w_minus(ai)
        g = g_minus(w)
        if not w and empty is None:
            empty = {"ainvs": ai, "W_minus": [], "g_minus": g,
                     "premise_holds": is_power_of_two(g),
                     "note": "gcd of an empty set is 0, which is not a power "
                             "of two, so the document's own premise refuses"}
        if w and not is_power_of_two(g) and odd_g is None:
            odd = next(p for p in (3, 5, 7, 11, 13, 17, 19, 23) if g % p == 0)
            odd_g = {"ainvs": ai, "W_minus": [r["ell"] for r in w],
                     "valuations": {str(r["ell"]): r["v_disc"] for r in w},
                     "g_minus": g, "an_odd_prime_dividing_it": odd,
                     "criterion_at_that_p": h3(w, odd),
                     "premise_holds": False}
        if empty and odd_g:
            break
    return {"models_scanned": scanned, "W_minus_empty": empty,
            "g_minus_with_an_odd_factor": odd_g,
            "why": ("the premise must be shown to refuse somewhere, or "
                    "'the premise holds here' is not a test of it")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    cert = uniform_certificate(BASE)
    route = routing_answer()
    fam_rows = family()
    pf = premise_failures()

    ok = (cert["premise_holds"]
          and not cert["conclusion_holds_as_stated"]      # the gap is found
          and cert["p_where_the_criterion_FAILS"] == [29]
          and route["every_failing_p_is_routed_away"]
          and fam_rows["W_minus_identical_to_the_base_for_every_member"]
          and fam_rows["g_minus_identical"] and fam_rows["same_failing_set"]
          and pf["W_minus_empty"] is not None
          and pf["g_minus_with_an_odd_factor"] is not None
          and not pf["g_minus_with_an_odd_factor"]["criterion_at_that_p"]["pass"])

    log = {
        "gate": "src39 — the FW-H3 compiler, run",
        "source": "09_FW_H3_Exact_Compiler",
        "curve": BASE, "conductor": N,
        "the_certificate": cert,
        "does_the_gap_reach_the_family": route,
        "the_family": fam_rows,
        "where_the_premise_refuses": pf,
        "headline": ("the boxed 'for all p > 2, FW-H3 = PASS' is false at "
                     "p = 29 for this curve, because W_- is the singleton {29} "
                     "and the ell != p clause removes its only member. The gcd "
                     "argument cannot see that clause. The family theorem is "
                     "unaffected: 29 is a fixed multiplicative prime the router "
                     "sends to P3, whose witness is 3 — split, and so not "
                     "usable by FW-H3 anyway"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  W_-(696.e1) = {cert['W_minus']}   valuations "
          f"{cert['valuations']}   g_- = {cert['g_minus']}")
    print(f"  premise (W_- non-empty and g_- a power of 2): "
          f"{cert['premise_holds']}")
    print(f"  boxed conclusion: {cert['boxed_conclusion']}")
    print(f"  tested at {cert['odd_p_tested']} odd primes below {P_BOUND} → "
          f"FAILS at {cert['p_where_the_criterion_FAILS']}")
    for r in cert["why_they_fail"]:
        print(f"    p = {r['p']}: {r['reason']}")
    print()
    print("  does the gap reach the family theorem?")
    for r in route["rows"]:
        print(f"    p = {r['p']:<4} {r['router_branch']}   P3 witness ℓ = "
              f"{r['P3_witness']} (split: {r['P3_witness_is_split']})   "
              f"covered: {r['covered']}")
    print(f"    every failing p routed away: "
          f"{route['every_failing_p_is_routed_away']}")
    print()
    f = fam_rows
    print(f"  the family: {f['members']} members, W_- = {f['base_W_minus']}, "
          f"g_- = {f['base_g_minus']}")
    print(f"    identical W_- / g_- / failing set across members: "
          f"{f['W_minus_identical_to_the_base_for_every_member']} / "
          f"{f['g_minus_identical']} / {f['same_failing_set']}")
    print()
    print(f"  where the premise refuses, over {pf['models_scanned']} models")
    e, o = pf["W_minus_empty"], pf["g_minus_with_an_odd_factor"]
    if e:
        print(f"    W_- empty       {e['ainvs']}   g_- = {e['g_minus']} → "
              f"premise {e['premise_holds']}")
    if o:
        print(f"    g_- odd factor  {o['ainvs']}   W_- = {o['W_minus']} "
              f"{o['valuations']}  g_- = {o['g_minus']}, divisible by "
              f"{o['an_odd_prime_dividing_it']}")
        print(f"      criterion at p = {o['an_odd_prime_dividing_it']}: "
              f"pass = {o['criterion_at_that_p']['pass']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
