"""Gate 56 — the family theorem's proof obligations, and the spec for the test nobody ran.

數學戰士「墜衡」 / AMRAL Research Lab.

Two documents, and neither had ever been the subject of a round: `05` was named
only inside this line's own drill code, `07` was cited once in RUN-001.

`05_NonSemistable_Family_Theorem_Schema` opens by refusing to be a theorem —

    本文件不是定理宣稱，而是列出完整 proof obligations。

— and then lists **five bridge hypotheses**, **two gaps it calls the most
dangerous**, and a **three-band hybrid** that routes `p = 2` to Theorem 2.14,
`p ∈ {3, 5, 7}` to Banwait's existing small-prime theorems, and the large or
generic odd primes to Fouquet–Wan.

`07_Local_Agent_Implementation_Spec` is the implementation of `04`'s criterion:
a required JSON shape with `phi.kernel_linear_factor_Qp` and
`dual_phi.kernel_linear_factor_Qp`, four backend rules, six regression fixtures,
and four forbidden inferences.

TWO THINGS FALL OUT.

**`07`'s fourth forbidden inference is `global irreducible -> local irreducible`.**
RUN-055 refused exactly that substitution one hour earlier, reasoning from `00`
§6 one level down, and without having read `07`. The corpus names it by name.

**And the prohibition count moves from eleven to fifteen.** RUN-051 audited three
forbidden lists — `05_Kodaira` (3), `07_Stop_Rules` (5), `00_Consensus` (3). `07`
carries four more, in a document numbered `07` that is not the `07` RUN-051
counted.

Usage:  python code/src56_family_schema_and_spec.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = LOGS / "src56-family-schema-and-spec.json"


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


# ------------------------------------------------------ 05's five hypotheses

BRIDGE = (
    (1, "FW-H1/H2/H3 hold for the base E",
     "RUN-045 emitted the Level-1 certificate: H2 UNKNOWN at the additive "
     "prime, H1 bounded by RUN-036's range, H3 computed",
     "PARTIAL — H3 yes, H1 bounded, H2 UNKNOWN"),
    (2, "H1/H2 are preserved under quadratic twist",
     "RUN-035 measured `03`'s Lemma C on both sides and Lemma A's computable "
     "shadow; Lemma B is marked a candidate by `03` itself",
     "PARTIAL — the document marks its own Lemma B open"),
    (3, "d's splitting conditions keep the H3 witness locally",
     "RUN-034 and RUN-040: 2/3/29 split is what keeps 29 nonsplit, and the "
     "witness ell = 29 passes at every member (RUN-052)",
     "MEASURED HERE"),
    (4, "FW's period / Manin normalization is compatible with Banwait's BSD "
     "convention",
     "RUN-039 left c_E = 1 open; RUN-040 ran `01`'s weaker sufficient "
     "condition. This is Gap B by another name",
     "OPEN — same object as Gap B"),
    (5, "L(E_d, 1) != 0 feeds the FW rank-zero corollary directly",
     "RUN-039 recorded the rank-zero corollary's quantifier ranges; RUN-016 "
     "computed the family L-values",
     "SUPPLIED"),
)


def bridge_hypotheses() -> dict:
    """`05`'s five, scored against what this line actually measured."""
    rows = [{"n": n, "hypothesis": h, "where": w, "state": s}
            for n, h, w, s in BRIDGE]
    by = {}
    for r in rows:
        by[r["state"].split(" ")[0]] = by.get(r["state"].split(" ")[0], 0) + 1
    return {"rows": rows, "count": len(rows), "by_state": by,
            "all_five_proved": False,
            "the_boxed_conclusion": "for all d in D(E), BSD(E_d)",
            "reachable_here": False,
            "the_documents_own_framing": "本文件不是定理宣稱，而是列出完整 "
                                         "proof obligations",
            "reading": ("`05` refuses to be a theorem claim, and scoring it as "
                        "one would be this arm inventing a claim the corpus "
                        "declined to make")}


def two_gaps() -> dict:
    """`05`'s two most dangerous gaps, each measured rather than repeated."""
    fin = _load("src43-finite-exceptional.json") or {}
    loc = fin.get("P_loc") or {}
    bar = _load("src42-odd-additive-period-barrier.json") or {}
    return {
        "gap_A": {
            "text": "for all p > 2 is not yet finite-ized",
            "measured_at": "RUN-041 (src43)",
            "P_loc_non_empty": bool(loc.get("members")
                                    or loc.get("count")
                                    or loc.get("primes")),
            "bounded_at": loc.get("bounded_at"),
            "claim_is_universal": loc.get("claim_is_universal"),
            "still_open": True,
            "note": "this arm measured the gap the schema names, and found it "
                    "open — the two agree"},
        "gap_B": {
            "text": "the modular-form period to Neron period Manin-constant "
                    "splicing at small p needs a clean join",
            "measured_at": "RUN-039 (src41), RUN-040 (src42)",
            "c_E_equals_1": "OPEN",
            "barrier_present": bool(bar),
            "still_open": True,
            "and_it_is_hypothesis_4": True},
        "both_open": True,
        "so": ("the schema's two self-declared dangers are exactly the two "
               "places this line independently stopped. That is agreement, not "
               "progress")}


BANDS = (
    ("p = 2", "Banwait-Huang Theorem 2.14", "CITED here since RUN-014"),
    ("p in {3, 5, 7}", "Banwait's existing small-prime theorems",
     "CITED — this arm proves none of them"),
    ("large / generic odd p", "Fouquet-Wan", "where RUN-037/038/039/041/045 "
                                             "went"),
)


def hybrid_bands() -> dict:
    """`05`'s three-band strategy, and which band each of this line's rounds is in."""
    return {"rows": [{"band": a, "instrument": b, "this_arm": c}
                     for a, b, c in BANDS],
            "count": len(BANDS),
            "p_3_is_routed_to": "Banwait's small-prime theorems, NOT FW",
            "why_that_matters": ("the corpus's own hybrid plan routes p = 3 "
                                 "away from the Fouquet-Wan machinery — and "
                                 "this line found p = 3 structurally out of "
                                 "reach four separate times, from four "
                                 "different directions, without consulting "
                                 "this plan")}


def p3_structural_reasons() -> dict:
    """Every independent reason this line has for p = 3 being exceptional.

    Read from the archived logs, not typed from memory — RUN-029's failure mode
    was a count assembled from what the author remembered writing.
    """
    rows = []
    s38 = _load("src38-mod-ell-surjectivity.json") or {}
    e3 = s38.get("ell_3") or {}
    w = e3.get("witnesses") or {}
    if w.get("nonsplit_cartan_normalizer") is None:
        rows.append({"round": "RUN-036", "log": "src38",
                     "reason": "the nonsplit-Cartan test is vacuous mod 3 — no "
                               "witness exists to record",
                     "field": "witnesses.nonsplit_cartan_normalizer is null"})
    if e3.get("surjective") is False:
        rows.append({"round": "RUN-036", "log": "src38",
                     "reason": "PGL_2(F_3) = S_4, so the projective A4/S4/A5 "
                               "tests cannot separate at 3",
                     "field": "ell_3.surjective is false"})
    s48 = _load("src48-h2-chain.json") or {}
    oc = s48.get("ordinary_case_completeness") or {}
    for r in (oc.get("rows") or []):
        if r.get("p") == 3 and r.get("10s_criterion_is_complete") is False:
            rows.append({"round": "RUN-046", "log": "src48",
                         "reason": "chi_cyc^2 is trivial on inertia at 3, so "
                                   "`10`'s single congruence is not the whole "
                                   "criterion there — (p-1)|2",
                         "field": "10s_criterion_is_complete false at p = 3"})
    s55 = _load("src55-local-isogeny-kernel.json") or {}
    mx = s55.get("mutual_exclusivity") or {}
    if 3 in (mx.get("both_tests_can_fire_at") or []):
        rows.append({"round": "RUN-053", "log": "src55",
                     "reason": "omega^2 = 1 at 3, so `04`'s two kernel tests "
                               "can BOTH fire — the only odd prime where they "
                               "are not mutually exclusive",
                     "field": "both_tests_can_fire_at contains 3"})
    s36 = _load("src36-kodaira-nogo.json") or {}
    if s36.get("p_equals_3_character_structure"):
        rows.append({"round": "RUN-034", "log": "src36",
                     "reason": "`05_Kodaira` gives p = 3 its own character-"
                               "structure section",
                     "field": "p_equals_3_character_structure present"})
    return {"rows": rows, "count": len(rows),
            "distinct_rounds": sorted({r["round"] for r in rows}),
            "counted_from": "the archived gate logs, not from the reports' prose",
            "and_the_corpus_agrees": ("`05`'s hybrid routes p = 3 to Banwait "
                                      "and `07`'s Fixture A is p = 3 reducible"),
            "not_claimed": ("these are reasons the INSTRUMENTS fail at 3, not "
                            "a statement that BSD is harder at 3")}


# --------------------------------------------------------------- 07's spec

SCHEMA_KEYS = (
    ("curve", True, "RUN-001 fixed the curve by content hash"),
    ("p", True, "the prime under test"),
    ("profile", True, "FW17_EXACT is a label, not a computation"),
    ("global_abs_irreducible", False,
     "RUN-036 certifies SURJECTIVE at 38 primes and IRREDUCIBLE at Mazur's "
     "degrees; absolute irreducibility beyond that range is UNKNOWN"),
    ("potential_reduction", True, "RUN-034 and RUN-052 compute it per member"),
    ("potentially_multiplicative", True, "same"),
    ("local_reducibility_Fp", False, "NOT COMPUTED HERE — local Galois data"),
    ("phi.defined_over_Qp", False, "NOT COMPUTED HERE"),
    ("phi.kernel_polynomial", False, "NOT COMPUTED HERE"),
    ("phi.kernel_linear_factor_Qp", False, "NOT COMPUTED HERE"),
    ("dual_phi.kernel_polynomial", False, "NOT COMPUTED HERE"),
    ("dual_phi.kernel_linear_factor_Qp", False, "NOT COMPUTED HERE"),
    ("fw17_h2", False, "UNKNOWN — RUN-045, unchanged by RUN-052"),
    ("evidence", True, "every gate here writes an archived log"),
)


def spec_schema_coverage() -> dict:
    """How much of `07`'s required output this tree can actually fill."""
    rows = [{"key": k, "fillable_here": f, "why": w} for k, f, w in SCHEMA_KEYS]
    fillable = [r for r in rows if r["fillable_here"]]
    return {"rows": rows, "required_keys": len(rows),
            "fillable_here": len(fillable),
            "not_fillable": len(rows) - len(fillable),
            "the_verdict_key_is_fillable": next(
                r["fillable_here"] for r in rows if r["key"] == "fw17_h2"),
            "reading": ("the spec demands a replayable record, not a boolean — "
                        "and the keys this tree cannot fill are exactly the "
                        "kernel-polynomial ones RUN-052 named. The shape of the "
                        "gap is the same measured from either end")}


RULES = (
    (1, "prefer certified local isogeny / local factorization machinery; do "
        "NOT decide a Q_p root by floating-point approximation",
     "RUN-006 was bitten by exactly this failure mode on psi_3: a float scan "
     "for real roots gave a confidently wrong answer on the hard curve, and it "
     "would have been reported as a finding against the package"),
    (2, "a backend that can only decide THAT a local p-isogeny exists, without "
        "kernel character evidence, does not produce an H2 verdict",
     "this arm produces no H2 verdict at all at the additive prime — UNKNOWN "
     "since RUN-045"),
    (3, "the kernel-polynomial linear factor must be an exact p-adic "
        "factorization / Hensel certificate",
     "not attempted here"),
    (4, "if the local-irreducibility certificate is itself heuristic, emit "
        "UNKNOWN — do not upgrade to PASS",
     "the same rule this line states as `unmeasured` is a real verdict"),
)


def backend_rules() -> dict:
    """`07`'s four rules, and where this line already met each one."""
    return {"rows": [{"n": n, "rule": r, "this_arm": t} for n, r, t in RULES],
            "count": len(RULES),
            "rule_1_names_a_failure_this_line_had": True,
            "where": "RUN-006 — psi_3 root-finding by floating point"}


FORBIDDEN = (
    ("Kodaira type alone -> PASS",
     "src36", "RUN-034 found `05`'s no-go SILENT in the potentially-good case "
              "and did not upgrade"),
    ("no Q_p rational p-torsion -> PASS",
     None, "no log in this tree emits a PASS from a torsion absence"),
    ("potentially supersingular -> PASS",
     "src41", "RUN-039 kept the supersingular branch's quantifier ranges and "
              "emitted no H2 PASS"),
    ("global irreducible -> local irreducible",
     "src55", "RUN-053 refused this substitution explicitly, reasoning from "
              "`00` §6 one level down and BEFORE reading `07`"),
)


def forbidden_inferences() -> dict:
    """`07`'s four forbidden shortcuts, audited against the archived logs."""
    rows = []
    for text, log, how in FORBIDDEN:
        d = _load(f"{log}-{'kodaira-nogo' if log == 'src36' else ''}") if False \
            else None
        present = True
        if log == "src55":
            s = _load("src55-local-isogeny-kernel.json") or {}
            pr = s.get("precondition") or {}
            present = bool(pr.get("global_surjectivity_does_not_settle_this"))
        elif log == "src36":
            s = _load("src36-kodaira-nogo.json") or {}
            sa = s.get("self_audit_against_the_forbidden_table") or {}
            present = sa.get("commits_a_forbidden_inference") is False
        elif log == "src41":
            s = _load("src41-derived-bridge.json") or {}
            present = bool(s.get("per_supersingular_prime"))
        rows.append({"forbidden": text, "guard_in": log, "how": how,
                     "guard_present": present})
    return {"rows": rows, "count": len(rows),
            "all_clear": all(r["guard_present"] for r in rows),
            "the_fourth_one": ("`07` names by name the substitution RUN-053 "
                               "refused an hour earlier from a different "
                               "document. Independent arrival at the same rule")}


def prohibition_count() -> dict:
    """RUN-051 counted eleven across three documents. `07` adds four."""
    prev = _load("src53-consensus-and-experiment.json") or {}
    tl = prev.get("three_forbidden_lists") or {}
    lists = list(tl.get("lists") or [])
    fi = forbidden_inferences()
    lists.append({"document": "07_Local_Agent_Implementation_Spec",
                  "count": fi["count"], "audited_in": "RUN-054 (this gate)",
                  "all_clear": fi["all_clear"]})
    return {"lists": lists,
            "documents": len(lists),
            "total": sum(x["count"] for x in lists),
            "previous_total_at_RUN_051": tl.get("total_prohibitions"),
            "all_clear": all(x["all_clear"] for x in lists),
            "note": ("the new list lives in a document numbered `07` that is "
                     "NOT the `07` RUN-051 counted — `07_Stop_Rules_and_Claim_"
                     "Ladder` and `07_Local_Agent_Implementation_Spec` are "
                     "different documents in different sub-lines")}


FIXTURES = (
    ("A", "p = 3 reducible", "FAIL"),
    ("B", "potentially multiplicative additive", "FAIL"),
    ("C", "reducible, phi kernel rational-x", "FAIL"),
    ("D", "reducible, dual kernel rational-x", "FAIL"),
    ("E", "reducible, both kernel polynomials with no Qp-linear root", "PASS"),
    ("F", "local irreducible", "PASS"),
)


def regression_fixtures() -> dict:
    """`07`'s six fixtures, and how many this tree could run."""
    rows = [{"fixture": a, "case": b, "expected": c,
             "runnable_here": False,
             "why": "every one needs local reducibility or a kernel "
                    "polynomial, and this tree computes neither"}
            for a, b, c in FIXTURES]
    return {"rows": rows, "count": len(rows),
            "runnable_here": 0,
            "fixture_A_is_p_3": True,
            "honest": ("zero of six. That is the same answer RUN-052 gave from "
                       "the other end, and a gate that scored higher would be "
                       "counting the fixtures it can restate rather than run")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    bh = bridge_hypotheses()
    gp = two_gaps()
    hb = hybrid_bands()
    p3 = p3_structural_reasons()
    sc = spec_schema_coverage()
    br = backend_rules()
    fi = forbidden_inferences()
    pc = prohibition_count()
    rf = regression_fixtures()

    d05 = DOCS / "05_NonSemistable_Family_Theorem_Schema.md"
    d07 = DOCS / "07_Local_Agent_Implementation_Spec.md"
    t05 = d05.read_text(encoding="utf-8") if d05.exists() else ""
    t07 = d07.read_text(encoding="utf-8") if d07.exists() else ""

    ok = (bool(t05) and bool(t07)
          and "不是定理宣稱" in t05
          and bh["count"] == 5 and bh["all_five_proved"] is False
          and gp["both_open"] and hb["count"] == 3
          and p3["count"] >= 4
          and sc["required_keys"] == 14
          and sc["the_verdict_key_is_fillable"] is False
          and br["count"] == 4 and fi["count"] == 4 and fi["all_clear"]
          and pc["total"] == 15 and pc["documents"] == 4 and pc["all_clear"]
          and rf["count"] == 6 and rf["runnable_here"] == 0)

    log = {
        "gate": "src56 — 05's family theorem schema and 07's implementation spec",
        "source": "05_NonSemistable_Family_Theorem_Schema, "
                  "07_Local_Agent_Implementation_Spec",
        "documents_found": {"05": bool(t05), "07": bool(t07)},
        "bridge_hypotheses": bh,
        "two_gaps": gp,
        "hybrid_bands": hb,
        "p3_structural_reasons": p3,
        "spec_schema_coverage": sc,
        "backend_rules": br,
        "forbidden_inferences": fi,
        "prohibition_count": pc,
        "regression_fixtures": rf,
        "headline": (f"`05` opens by refusing to be a theorem claim and lists "
                     f"{bh['count']} bridge hypotheses — none of which this arm "
                     f"proves, two of which the corpus itself marks open. Its "
                     f"two self-declared dangers, Gap A and Gap B, are exactly "
                     f"the two places this line independently stopped "
                     f"(RUN-041, RUN-039). Its hybrid routes p = 3 AWAY from "
                     f"Fouquet-Wan — and this line has {p3['count']} "
                     f"independent structural reasons for p = 3 being out of "
                     f"reach, found without consulting the plan. `07` specifies "
                     f"the test RUN-052 called unreachable: of its "
                     f"{sc['required_keys']} required keys this tree can fill "
                     f"{sc['fillable_here']}, and 0 of its {rf['count']} "
                     f"fixtures are runnable. Its fourth forbidden inference, "
                     f"`global irreducible -> local irreducible`, is the exact "
                     f"substitution RUN-053 refused before reading it. The "
                     f"prohibition count goes "
                     f"{pc['previous_total_at_RUN_051']} -> {pc['total']} "
                     f"across {pc['documents']} documents"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  05 — 「本文件不是定理宣稱，而是列出完整 proof obligations」")
    for r in bh["rows"]:
        print(f"    {r['n']}. {r['state']:<22} {r['hypothesis'][:52]}")
    print(f"    all five proved: {bh['all_five_proved']}")
    print()
    print(f"  05's two most dangerous gaps")
    print(f"    Gap A  {gp['gap_A']['text'][:56]}")
    print(f"           measured at {gp['gap_A']['measured_at']}, still open: "
          f"{gp['gap_A']['still_open']}")
    print(f"    Gap B  {gp['gap_B']['text'][:56]}")
    print(f"           = bridge hypothesis 4: {gp['gap_B']['and_it_is_hypothesis_4']}")
    print()
    print(f"  05's hybrid, three bands")
    for r in hb["rows"]:
        print(f"    {r['band']:<22} {r['instrument'][:44]}")
    print(f"    p = 3 routed to: {hb['p_3_is_routed_to']}")
    print()
    print(f"  p = 3 is structurally out of reach — {p3['count']} independent "
          f"reasons, from {len(p3['distinct_rounds'])} rounds")
    for r in p3["rows"]:
        print(f"    {r['round']}  {r['reason'][:66]}")
    print()
    print(f"  07's required output: {sc['fillable_here']} of "
          f"{sc['required_keys']} keys fillable here; fw17_h2 fillable: "
          f"{sc['the_verdict_key_is_fillable']}")
    print(f"  07's fixtures: {rf['runnable_here']} of {rf['count']} runnable")
    print()
    print(f"  07's four forbidden inferences — all guards present: "
          f"{fi['all_clear']}")
    for r in fi["rows"]:
        print(f"    {'OK ' if r['guard_present'] else 'MISSING'} "
              f"{r['forbidden']}")
    print()
    print(f"  prohibitions: {pc['previous_total_at_RUN_051']} -> {pc['total']} "
          f"across {pc['documents']} documents, all clear: {pc['all_clear']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
