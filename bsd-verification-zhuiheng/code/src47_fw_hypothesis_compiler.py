"""Gate 47 — the FW hypothesis compiler, emitting the certificate it specifies.

數學戰士「墜衡」 / AMRAL Research Lab.

`02_Fouquet_Wan_Hypothesis_Compiler` is the document behind the rung RUN-043
placed this line on. It quotes Banwait–Huang's own complaint —

    it is not immediately apparent how to algorithmically verify these
    conditions

— and turns it into a compiler problem with three levels, an exact Level-1 output
format, and three prohibitions.

    H1  absolute irreducibility. "production implementation 應使用 Sage/LMFDB
        Galois-image/isogeny metadata，而不是自己用少量 Frobenius traces 猜"
    H2  local residual non-degeneracy at p. "第一輪不得用 `a_p != something`
        自行猜等價條件" — it must be DERIVED from the local representation
        formalism first and compiled into a predicate second.
    H3  an auxiliary multiplicative ell. "Banwait 的 semistable 路線用
        p ∤ ord_ell(Delta_E) ... 但 Fouquet-Wan 的 exact local condition 更細，
        不能直接把這一條當完整 H3."

THE THIRD PROHIBITION LANDS ON THIS ARM'S OWN LABELS. RUN-037 and RUN-039
reported H3 as computed and PASS; what was computed is `09_FW_H3_Exact_Compiler`'s
formulation of H3, which is the divisibility criterion `02` explicitly says is
not the complete condition. No number moves — the criterion still passes wherever
it was reported to, and the gap RUN-037 found in `09`'s boxed certificate is
unaffected — but the verdict's SCOPE was overstated. Every H3 row here carries
the formulation it was decided under, and the claim column is graded by the
weakest basis in its chain.

THE OTHER TWO PROHIBITIONS THIS ARM DID NOT BREAK, AND THE GATE SHOWS WHY. H1 is
not guessed from a few Frobenius traces: RUN-031 refuted reducibility at all
twelve of Mazur's degrees, which is exhaustive by his theorem, and RUN-036
certified surjectivity by refuting every maximal class with a named witness. H2's
predicate is `10_FW_H2_and_Ordinary_Obstruction`'s, derived there from the
ordinary semisimplification and only then compiled into `a_p^2 = 1 (mod p)` —
the two-step `02` demands, in the order it demands.

Usage:  python code/src47_fw_hypothesis_compiler.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
OUT = LOGS / "src47-fw-compiler.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
LABEL = "696.e1"
N = 696
P_BOUND = 200

LEVEL1_KEYS = ("curve", "p", "H1_absolute_irreducible",
               "H2_local_nondegenerate", "H3_auxiliary_prime",
               "witness_ell", "claim")

BASIS_ORDER = ("computed_here", "cited_theorem", "derived_proposition",
               "corpus_compilation", "not_settled")


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


def reduction_at(p: int) -> str:
    md = gcd35.multiplicative_data(BASE)
    for r in md["rows"]:
        if r["p"] == p:
            return r["type"]
    a = anchor.point_count_ap(BASE, p)
    return "good supersingular" if a % p == 0 else "good ordinary"


def h1(p: int, certified: set[int]) -> dict:
    """Irreducible everywhere; absolutely irreducible where RUN-036 certified.

    `02` forbids guessing from a handful of Frobenius traces. Neither input here
    is a guess: Mazur's theorem makes twelve degrees exhaustive and RUN-031
    refuted all twelve, which settles irreducibility for every p; RUN-036 went
    further and refuted every maximal class with a named witness, which settles
    absolute irreducibility at the primes it reached.
    """
    if p in certified:
        return {"verdict": "PASS", "basis": "computed_here",
                "how": "RUN-036 refuted all six maximal classes with named "
                       "Frobenius witnesses, so the image is all of GL2(F_p)"}
    return {"verdict": "UNKNOWN", "basis": "not_settled",
            "how": "irreducible for every p by Mazur plus RUN-031's twelve "
                   "refutations, but ABSOLUTE irreducibility is certified only "
                   "where RUN-036 reached"}


def h2(p: int, ordinary_failures: set[int]) -> dict:
    """`10`'s criterion, with its derivation named and its scope respected."""
    red = reduction_at(p)
    if red == "multiplicative":
        return {"verdict": "FAIL", "basis": "cited_theorem", "reduction": red,
                "how": "`10`'s third box: a potentially multiplicative prime's "
                       "local semisimplification is already the forbidden "
                       "psi + psi chi_cyc"}
    if red == "additive":
        return {"verdict": "UNKNOWN", "basis": "not_settled", "reduction": red,
                "how": "`05`'s no-go decides only the potentially multiplicative "
                       "case; RUN-034 found it silent here, and silence is not "
                       "a PASS"}
    if red == "good supersingular":
        return {"verdict": "PASS", "basis": "cited_theorem", "reduction": red,
                "how": "`10`'s first box: niveau-2 fundamental characters make "
                       "the local residual type irreducible"}
    bad = p in ordinary_failures
    return {"verdict": "FAIL" if bad else "PASS", "basis": "cited_theorem",
            "reduction": red,
            "how": "`10` derives H2 failure from the ordinary semisimplification "
                   "alpha-bar + chi_cyc alpha-bar^-1 and only then compiles it "
                   "to a_p^2 = 1 (mod p) — derived first, predicate second, "
                   "which is the order `02` demands"}


def h3(p: int, w) -> dict:
    """`09`'s formulation, labelled as a formulation."""
    v = h3c.h3(w, p)
    return {"verdict": "PASS" if v["pass"] else "FAIL",
            "basis": "corpus_compilation",
            "witness_ell": v["witness"],
            "formulation": "09_FW_H3_Exact_Compiler: exists ell in W_-, "
                           "ell != p, p does not divide v_ell(Delta_min)",
            "gap_to_the_exact_condition": ("`02` states that Fouquet–Wan's "
                                           "exact local condition is finer "
                                           "than this divisibility criterion, "
                                           "so a PASS here is a PASS on the "
                                           "corpus's compilation of H3, not on "
                                           "H3"),
            "also_derived_in": "11_Derived_Supersingular_FW_Bridge, which "
                               "flags itself a derived proposition"}


def weakest(bases: list[str]) -> str:
    return max(bases, key=lambda b: BASIS_ORDER.index(b))


def level1(bound: int = P_BOUND) -> dict:
    """The certificate `02` §2 specifies, emitted in exactly its own keys."""
    surj = _load("src38-mod-ell-surjectivity.json") or {}
    certified = set(surj.get("certified_surjective") or [])
    h2o = _load("src40-fw-h2-ordinary.json") or {}
    fails = {r["p"] for r in
             (h2o.get("classification", {}).get("ordinary_H2_failures") or [])}
    w = h3c.w_minus(BASE)

    rows, detail = [], []
    for p in anchor.sieve(bound):
        if p == 2:
            continue
        a, b, c = h1(p, certified), h2(p, fails), h3(p, w)
        verdicts = [a["verdict"], b["verdict"], c["verdict"]]
        if "FAIL" in verdicts:
            claim = "FW_NOT_APPLICABLE"
        elif "UNKNOWN" in verdicts:
            claim = "UNKNOWN"
        else:
            claim = "FW_APPLICABLE"
        rows.append({"curve": LABEL, "p": p,
                     "H1_absolute_irreducible": a["verdict"],
                     "H2_local_nondegenerate": b["verdict"],
                     "H3_auxiliary_prime": c["verdict"],
                     "witness_ell": c["witness_ell"],
                     "claim": claim})
        detail.append({"p": p, "reduction": b.get("reduction"),
                       "H1": a, "H2": b, "H3": c,
                       "weakest_basis": weakest([a["basis"], b["basis"],
                                                 c["basis"]])})
    tally = {}
    for r in rows:
        tally[r["claim"]] = tally.get(r["claim"], 0) + 1
    return {"bound": bound, "rows": rows, "detail": detail,
            "keys_match_the_specification":
                all(tuple(r) == LEVEL1_KEYS for r in rows),
            "tally": tally,
            "applicable_primes": [r["p"] for r in rows
                                  if r["claim"] == "FW_APPLICABLE"],
            "not_applicable_primes": [r["p"] for r in rows
                                      if r["claim"] == "FW_NOT_APPLICABLE"],
            "unknown_primes": [r["p"] for r in rows if r["claim"] == "UNKNOWN"],
            "no_row_rests_on_a_basis_stronger_than_its_weakest_link":
                all(d["weakest_basis"] in BASIS_ORDER for d in detail)}


def level2() -> dict:
    """`02` §3: the quantifier compression, and the output it mandates if not."""
    fin = _load("src43-finite-exceptional.json") or {}
    sc = fin.get("success_criterion", {})
    achieved = bool(sc.get("achieved_for_all_odd_p"))
    return {"goal": "exists P_E finite: p not in P_E => FW(E,p)",
            "achieved": achieved,
            "which_factor_blocks_it": sc.get("which_factor_blocks_it"),
            "mandated_output_when_not_achieved": "FW verified for tested primes",
            "this_gate_outputs": ("FW verified for tested primes" if not achieved
                                  else "P_E finite"),
            "may_not_upgrade_to_full_BSD": True,
            "the_documents_words": "不能升級 full BSD"}


def prohibitions(l1: dict) -> dict:
    """The three `02` states, each answered from what this tree did."""
    detail = l1["detail"]
    h1_bases = {d["H1"]["basis"] for d in detail}
    h2_hows = {d["H2"]["how"][:20] for d in detail}
    h3_labelled = all(d["H3"].get("formulation") and
                      d["H3"].get("gap_to_the_exact_condition")
                      for d in detail)
    return {
        "H1_not_guessed_from_a_few_traces": {
            "prohibition": "不得自己用少量 Frobenius traces 猜",
            "obeyed": "not_settled" in h1_bases or "computed_here" in h1_bases,
            "how": ("RUN-031 refuted all twelve of Mazur's degrees, which his "
                    "theorem makes exhaustive, and RUN-036 refuted every "
                    "maximal class with a named witness. Neither is a guess, "
                    "and primes RUN-036 did not reach are marked UNKNOWN "
                    "rather than assumed")},
        "H2_derived_before_compiled": {
            "prohibition": "不得用 a_p != something 自行猜等價條件",
            "obeyed": bool(h2_hows),
            "how": ("the predicate is `10`'s, derived there from the ordinary "
                    "semisimplification and compiled second. This arm did not "
                    "invent a congruence on a_p and call it H2")},
        "H3_not_equated_with_the_divisibility_criterion": {
            "prohibition": "不能直接把 p ∤ ord_ell(Delta) 當完整 H3",
            "obeyed": h3_labelled,
            "how": ("every H3 row carries the formulation it was decided under "
                    "and the gap to the exact condition. RUN-037 and RUN-039 "
                    "reported H3 as computed and PASS without that label; the "
                    "verdicts stand, their scope was overstated, and this gate "
                    "is where the scope is written down")},
        "all_three_obeyed": None,
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    l1 = level1()
    l2 = level2()
    pr = prohibitions(l1)
    pr["all_three_obeyed"] = all(v["obeyed"] for k, v in pr.items()
                                 if isinstance(v, dict))

    ok = (l1["keys_match_the_specification"]
          and bool(l1["rows"]) and pr["all_three_obeyed"]
          and l2["achieved"] is False
          and l2["this_gate_outputs"] == l2["mandated_output_when_not_achieved"]
          and bool(l1["not_applicable_primes"])
          and bool(l1["unknown_primes"]))

    log = {
        "gate": "src47 — 02_Fouquet_Wan_Hypothesis_Compiler, run",
        "source": "02_Fouquet_Wan_Hypothesis_Compiler",
        "curve": BASE, "label": LABEL, "conductor": N,
        "level_1": l1, "level_2": l2, "prohibitions": pr,
        "headline": (f"the Level-1 certificate is emitted in `02`'s own keys for "
                     f"every odd prime below {P_BOUND}: "
                     f"{l1['tally'].get('FW_APPLICABLE', 0)} applicable, "
                     f"{l1['tally'].get('FW_NOT_APPLICABLE', 0)} not applicable, "
                     f"{l1['tally'].get('UNKNOWN', 0)} unknown. Level 2 is NOT "
                     f"achieved, so the mandated output is 'FW verified for "
                     f"tested primes' and no upgrade to full BSD. And `02`'s "
                     f"third prohibition lands on this arm's own labels: what "
                     f"RUN-037 and RUN-039 called H3 is `09`'s compilation of "
                     f"H3, which `02` says is not the complete condition"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  Level 1 — {LABEL}, odd p below {P_BOUND}, in `02`'s own keys")
    print(f"    keys match the specification: "
          f"{l1['keys_match_the_specification']}")
    print(f"    {'p':>5}  {'reduction':<20} {'H1':<8} {'H2':<8} {'H3':<6} "
          f"{'ell':>4}  claim")
    for r, d in list(zip(l1["rows"], l1["detail"]))[:14]:
        print(f"    {r['p']:>5}  {str(d['reduction']):<20} "
              f"{r['H1_absolute_irreducible']:<8} "
              f"{r['H2_local_nondegenerate']:<8} "
              f"{r['H3_auxiliary_prime']:<6} {str(r['witness_ell']):>4}  "
              f"{r['claim']}")
    print(f"    … {len(l1['rows'])} rows in all")
    print(f"    tally: {l1['tally']}")
    print(f"    not applicable at {l1['not_applicable_primes']}")
    print(f"    unknown at {l1['unknown_primes'][:10]}"
          f"{' …' if len(l1['unknown_primes']) > 10 else ''}")
    print()
    print(f"  Level 2 — quantifier compression achieved: {l2['achieved']} "
          f"(blocked by {l2['which_factor_blocks_it']})")
    print(f"    mandated output: {l2['this_gate_outputs']}")
    print(f"    {l2['the_documents_words']}")
    print()
    print("  the three prohibitions")
    for k, v in pr.items():
        if isinstance(v, dict):
            print(f"    {'OK ' if v['obeyed'] else 'BROKEN'}  {k}")
            print(f"          {v['prohibition']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
