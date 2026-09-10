"""Gate 53 — Phase 2's own framing: the main problem, three forbidden lists, one success gate.

數學戰士「墜衡」 / AMRAL Research Lab.

`00_Phase2_Global_Enclosure_Consensus` states the phase's main problem formally

    BH2(E, d) + for all p > 2 FW(E_d, p)  =>  BSD(E_d)

names the unclosed quantifier as `for all p > 2`, and **forbids three
substitutions for it**:

    most p are fine
    all p <= B are fine
    the residual representation is generically surjective

THE THIRD ONE IS ABOUT THIS ARM'S OWN RUN-036. That round certified `rho-bar_ell`
surjective at 38 primes, and `00` says in advance that such a result must not
stand in for the quantifier. The audit is therefore against the archived logs
rather than against prose: `src38` lists exactly which primes it reached and
marks `ell = 3` partial; `src43` tags `P_loc` with its bound and
`claim_is_universal: false`; `src47` marks every prime above RUN-036's range
`UNKNOWN` rather than extrapolating.

THAT IS THE THIRD FORBIDDEN LIST IN THIS CORPUS. `05` forbids three inferences
(RUN-034), `07` forbids five upgrades (RUN-043), and `00` forbids three
substitutions. Eleven prohibitions across three documents, and this gate audits
all eleven in one place.

`06_Phase2_Agent_Experiment` SETS A FOUR-CONDITION SUCCESS GATE, AND IT IS NOT
MET. Its four are H2 exact specialisation, H3 exact specialisation, the
twist-invariance lemmas, and finite-prime reduction on one nontrivial curve
class. The corpus supplies documents for all four; two of them its own documents
mark open — `03`'s Lemma B is a 候選 and `04`'s criterion was found unachieved at
RUN-041 — so the gate stands at two of four.

AND THIS ARM DID NOT RUN THAT EXPERIMENT. `06` is a plan for the corpus's own
agents. This line verified documents that resulted from it. Scoring "steps this
line performed" would conflate two roles, so the gate scores what exists and who
checked it, not who did it.

Usage:  python code/src53_consensus_and_experiment.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = LOGS / "src53-consensus-and-experiment.json"


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


def forbidden_substitutions() -> dict:
    """`00` §6's three, audited against the archived fields."""
    surj = _load("src38-mod-ell-surjectivity.json") or {}
    fin = _load("src43-finite-exceptional.json") or {}
    comp = _load("src47-fw-compiler.json") or {}
    h2o = _load("src40-fw-h2-ordinary.json") or {}

    certified = surj.get("certified_surjective") or []
    three = surj.get("ell_3") or {}
    loc = (fin.get("P_loc") or {})
    l1 = (comp.get("level_1") or {})
    unknown = l1.get("unknown_primes") or []

    rows = [
        {"forbidden": "most p are fine",
         "guard": "no log states a majority as a closure; `src40` reports the "
                  "ordinary H2 failure set by range with counts, never as a "
                  "fraction",
         "present": bool((h2o.get("no_finite_exception") or {}).get("buckets"))},
        {"forbidden": "all p <= B are fine",
         "guard": f"`src43` tags P_loc bounded_at "
                  f"{loc.get('bounded_at')} with claim_is_universal "
                  f"{loc.get('claim_is_universal')}",
         "present": loc.get("claim_is_universal") is False
                    and bool(loc.get("bounded_at"))},
        {"forbidden": "the residual representation is generically surjective",
         "guard": f"`src38` names the {len(certified)} primes it certified and "
                  f"marks ell = 3 partial; `src47` marks {len(unknown)} primes "
                  f"above that range UNKNOWN rather than extrapolating",
         "present": bool(certified) and bool(unknown)
                    and three.get("surjective") is False},
    ]
    return {"source": "00_Phase2_Global_Enclosure_Consensus section 6",
            "rows": rows,
            "all_guards_present": all(r["present"] for r in rows),
            "the_third_is_about_RUN_036": True,
            "primes_certified_by_RUN_036": len(certified),
            "primes_marked_UNKNOWN_by_RUN_045": len(unknown),
            "why_logs_not_prose": ("`00` forbids a substitution, which is a "
                                   "thing a report could do in a sentence. The "
                                   "guard has to be a field a gate wrote")}


def three_forbidden_lists() -> dict:
    """All eleven prohibitions the corpus states, in one place."""
    ladder = _load("src45-claim-ladder.json") or {}
    nogo = _load("src36-kodaira-nogo.json") or {}
    fs = forbidden_substitutions()
    lists = [
        {"document": "05_Kodaira_Prefilters_and_NoGo", "count": 3,
         "audited_in": "RUN-034 (src36)",
         "all_clear": bool((nogo.get("self_audit_against_the_forbidden_table")
                            or {}).get("commits_a_forbidden_inference") is False)},
        {"document": "07_Stop_Rules_and_Claim_Ladder", "count": 5,
         "audited_in": "RUN-043 (src45)",
         "all_clear": bool((ladder.get("forbidden_upgrades") or {})
                           .get("all_guards_present"))},
        {"document": "00_Phase2_Global_Enclosure_Consensus", "count": 3,
         "audited_in": "RUN-051 (this gate)",
         "all_clear": fs["all_guards_present"]},
    ]
    return {"lists": lists,
            "total_prohibitions": sum(l["count"] for l in lists),
            "all_three_lists_clear": all(l["all_clear"] for l in lists),
            "reading": ("three documents written at different times each forbid "
                        "a way of overclaiming, and the three lists do not "
                        "overlap: `05` forbids reading H2 off a Kodaira table, "
                        "`07` forbids climbing the claim ladder on partial "
                        "evidence, and `00` forbids substituting anything for "
                        "the prime quantifier")}


def the_main_problem() -> dict:
    """`00` §5, and which half of it this arm has touched."""
    comp = _load("src47-fw-compiler.json") or {}
    l2 = comp.get("level_2") or {}
    return {"statement": "BH2(E, d) + for all p > 2 FW(E_d, p) => BSD(E_d)",
            "BH2": {"what": "Theorem 2.14's 2-part / nonvanishing conditions",
                    "this_arm": "CITED — RUN-014 computed v2(L^alg) = 0, "
                                "trivial torsion and Delta < 0, which are its "
                                "arithmetic inputs; the theorem is not verified"},
            "for_all_p_FW": {"what": "the unclosed quantifier",
                             "this_arm": "RUN-037/038/039/041/045 — the "
                                         "hypotheses have exact meaning and the "
                                         "certificate is emitted per prime",
                             "quantifier_closed": False,
                             "what_the_compiler_emits":
                                 l2.get("this_gate_outputs")},
            "so": ("the left half is cited and the right half is compiled but "
                   "not closed. `00` says that is exactly the state in which "
                   "the route may only give a fixed-finite-prime-set p-part "
                   "theorem")}


SUCCESS_GATE = (
    ("H2 exact specialisation",
     "10 + 03 + 08 supply it; RUN-046 verified the three are one statement over "
     "22,140 character pairs and located 10's range",
     "SUPPLIED, VERIFIED HERE"),
    ("H3 exact specialisation",
     "08 and 09 supply it, 02 forbids equating it with H3, 23 derives it. "
     "RUN-046 reported the disagreement and RUN-049 found the derivation",
     "SUPPLIED, DISPUTED WITHIN THE CORPUS"),
    ("twist-invariance lemmas",
     "03's A, B, C. RUN-035 measured C on both sides and A's computable "
     "shadow; B is marked 候選 by the document itself",
     "INCOMPLETE — the document marks its own Lemma B open"),
    ("finite-prime reduction on one nontrivial curve class",
     "04's criterion, evaluated at RUN-041: P_red and P_ram empty, P_loc "
     "non-empty and not known finite",
     "NOT ACHIEVED"),
)


def success_gate() -> dict:
    """`06`'s four conditions, scored against what exists."""
    rows = [{"condition": a, "where": b, "status": c} for a, b, c in SUCCESS_GATE]
    met = [r for r in rows if r["status"].startswith("SUPPLIED")]
    return {"source": "06_Phase2_Agent_Experiment, 成功 Gate",
            "rows": rows,
            "met_or_supplied": len(met),
            "of": len(rows),
            "gate_is_met": len(met) == len(rows),
            "the_documents_own_stake": "這已經是新的標準語言數學結果",
            "reading": ("two of the four are supplied by the corpus and checked "
                        "here; the other two are marked open by the corpus's own "
                        "documents — `03` calls its Lemma B a candidate and "
                        "RUN-041 found `04`'s criterion unachieved. The gate is "
                        "not met, and neither of the two gaps is this arm's to "
                        "close")}


STEPS = (
    (1, "do not scan the whole database; 20 + 20 + 20 curves for compiler "
        "correctness only", "no document of the corpus reports this run"),
    (2, "a local prime table per curve", "no document reports this run"),
    (3, "H2 symbolic derivation, lemma before code",
     "10_FW_H2_and_Ordinary_Obstruction, 03_FW_H2_Jordan_Holder_Lemma, "
     "08_FW_Weight2_Exact_Translation — verified at RUN-038, RUN-046"),
    (4, "H3 symbolic derivation, compared with Banwait's p ∤ v_ell(Delta); "
        "不得默認相同",
     "09_FW_H3_Exact_Compiler, 08, 23 — and the corpus DID default to the same "
        "in `08` and `09` while `02` forbade it. RUN-046 found the "
        "disagreement, RUN-049 found `23`'s derivation"),
    (5, "twist invariance, three bridge lemmas",
     "03_Quadratic_Twist_Invariance_Bridge — verified at RUN-035, Lemma B open"),
    (6, "finite exceptional prime theorem search; 若無 theorem 保證完整，"
        "不得標 complete",
     "04_Finite_Exceptional_Prime_Problem — evaluated at RUN-041, and P_loc is "
        "tagged non-universal exactly as this step requires"),
    (7, "only then a database census over ~895,988 curves; UNKNOWN 不可吞掉",
     "no census exists. RUN-045's certificate keeps its UNKNOWN rows visible"),
)


def experiment_steps() -> dict:
    """`06`'s seven steps, and the honest statement of who did what."""
    comp = _load("src47-fw-compiler.json") or {}
    unknown = ((comp.get("level_1") or {}).get("unknown_primes") or [])
    rows = [{"step": n, "asks": a, "state": b} for n, a, b in STEPS]
    with_docs = [r for r in rows if "verified at" in r["state"]
                 or "RUN-" in r["state"]]
    return {"rows": rows,
            "steps_with_a_resulting_document_this_line_verified": len(with_docs),
            "of": len(rows),
            "step_4_warning": "不得默認相同",
            "step_4_was_violated_in_the_corpus": True,
            "step_7_census_exists": False,
            "unknown_rows_kept_visible": len(unknown),
            "this_arm_did_not_run_the_experiment":
                ("`06` is a plan for the corpus's own agents. This line verified "
                 "documents that resulted from it. Scoring 'steps this line "
                 "performed' would conflate two roles, so what is scored is "
                 "what exists and who checked it")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    fs = forbidden_substitutions()
    tl = three_forbidden_lists()
    mp = the_main_problem()
    sg = success_gate()
    st = experiment_steps()

    ok = (fs["all_guards_present"] and tl["all_three_lists_clear"]
          and tl["total_prohibitions"] == 11
          and mp["for_all_p_FW"]["quantifier_closed"] is False
          and sg["gate_is_met"] is False and sg["met_or_supplied"] == 2
          and st["step_4_was_violated_in_the_corpus"]
          and st["step_7_census_exists"] is False
          and st["unknown_rows_kept_visible"] > 0)

    log = {
        "gate": "src53 — 00's consensus and 06's agent experiment",
        "source": "00_Phase2_Global_Enclosure_Consensus, "
                  "06_Phase2_Agent_Experiment",
        "forbidden_substitutions": fs,
        "three_forbidden_lists": tl,
        "the_main_problem": mp,
        "success_gate": sg,
        "experiment_steps": st,
        "headline": (f"`00` forbids three substitutions for the prime "
                     f"quantifier and the third is about RUN-036's own "
                     f"surjectivity certificate; all three guards are present "
                     f"in the archived logs. With `05`'s three and `07`'s five "
                     f"that is {tl['total_prohibitions']} prohibitions across "
                     f"three documents, audited in one place. `06`'s "
                     f"four-condition success gate stands at "
                     f"{sg['met_or_supplied']} of {sg['of']} — the corpus's own "
                     f"documents mark the other two open — and its step 4 "
                     f"warning 不得默認相同 was violated inside the corpus, "
                     f"which is what RUN-046 found"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print("  00 §6 — three substitutions forbidden for the prime quantifier")
    for r in fs["rows"]:
        print(f"    {'OK ' if r['present'] else 'MISSING':8s} {r['forbidden']}")
        print(f"             {r['guard'][:74]}")
    print()
    print("  three forbidden lists, audited in one place")
    for l in tl["lists"]:
        print(f"    {l['document'][:44]:<44} {l['count']} prohibitions  "
              f"{l['audited_in']:<22} clear: {l['all_clear']}")
    print(f"    total {tl['total_prohibitions']}, all clear: "
          f"{tl['all_three_lists_clear']}")
    print()
    print(f"  00 §5 main problem: {mp['statement']}")
    print(f"    BH2            : {mp['BH2']['this_arm'][:60]}")
    print(f"    for all p FW   : quantifier closed = "
          f"{mp['for_all_p_FW']['quantifier_closed']}, compiler emits "
          f"\"{mp['for_all_p_FW']['what_the_compiler_emits']}\"")
    print()
    print(f"  06's success gate: {sg['met_or_supplied']} of {sg['of']}, met: "
          f"{sg['gate_is_met']}")
    for r in sg["rows"]:
        print(f"    {r['status'][:34]:<34} {r['condition']}")
    print()
    print(f"  06's seven steps — documents exist for "
          f"{st['steps_with_a_resulting_document_this_line_verified']} of "
          f"{st['of']}; no census (step 7); "
          f"{st['unknown_rows_kept_visible']} UNKNOWN rows kept visible")
    print(f"    step 4 said 「{st['step_4_warning']}」 and the corpus did it "
          f"anyway: {st['step_4_was_violated_in_the_corpus']}")
    print(f"    {st['this_arm_did_not_run_the_experiment'][:88]}…")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
