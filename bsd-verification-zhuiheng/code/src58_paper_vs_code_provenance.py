"""Gate 58 — the rule that produced each artefact, read from the upstream diffs and tested on the data.

數學戰士「墜衡」 / AMRAL Research Lab.

`02_Paper_vs_Current_Code_Audit` opens with: the GitHub implementation is not a
plain transcription of the paper's pseudocode. RUN-055 measured one consequence
without knowing the cause — the 1,355 base curves missing from the upstream
twist blob are exactly the 1,355 with a 3/5/7-isogeny, and the 2,707 removed for
|a_3| = 3 are all present in it. This gate reads the cause from the package's
own archived diffs and tests it against the data.

THREE VERSIONS OF ALGORITHM 1's ISOGENY CONDITION, at three commits:

  7286794  (generated the twist blob)
           non_isogeny_primes = set(bad_primes) and set([3,5,7])
           Python's `and` returns its second operand whenever the first is
           truthy, and bad_primes is non-empty for every curve — so this is
           UNCONDITIONALLY {3, 5, 7}, whatever was intended.

  1a0489c  (the OLD base, 40,749)
           A := {3 if 3 | N or |a3| = 3} ∪ {5 if 5 | N} ∪ {7 if 7 | N}
           CONDITIONAL — an isogeny at p is only fatal when p | N (or, for 3,
           when |a_3| = 3). Strictly weaker than the line above.

  31fae20  (CURRENT, 36,687)
           for every p in {3,5,7}, no rational p-isogeny — unconditional again —
           PLUS a separate filter a_3 != ±3.

The sequence is strict -> relaxed -> strict + a_3, and the twist blob was frozen
at the first stage. That is the mechanism behind PROVENANCE.md's sentence "OLD
base and OLD Algorithm2.py changed after the OLD twist JSON's last-change
commit, while the JSON blob stayed identical."

AND IT PREDICTS SOMETHING TESTABLE. If the OLD base came from the relaxed rule,
then every one of its 1,355 isogeny curves must ESCAPE that rule's trigger:
a 3-isogeny only with 3 ∤ N and |a_3| != 3, a 5-isogeny only with 5 ∤ N, a
7-isogeny only with 7 ∤ N. One counterexample and the story is wrong.

Usage:  python code/src58_paper_vs_code_provenance.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
PKG = cmap.PKG
SRC = PKG / "sources"
DIFF_GEN_OLD = SRC / "Algorithm1_generator_7286794_to_old_1a0489.diff"
DIFF_OLD_CUR = SRC / "Algorithm1_old_1a0489_to_current_31fae.diff"
PROVENANCE = SRC / "PROVENANCE.md"
RUN_LOG = PKG / "logs" / "run.log"
OUT = LOGS / "src58-paper-vs-code-provenance.json"

COMMITS = {"generator": "72867942accf94b9513857a2c0bae3895af8e9bc",
           "old": "1a0489c3c3099dd0c248624e6621df73ae8f0d43",
           "current": "31fae20c8df3f1f0383f41112b914d4995d5809d"}


# ----------------------------------------------------------- the three rules

def three_rules() -> dict:
    """Locate each version's condition text in the archived diffs."""
    g2o = DIFF_GEN_OLD.read_text(encoding="utf-8") if DIFF_GEN_OLD.exists() else ""
    o2c = DIFF_OLD_CUR.read_text(encoding="utf-8") if DIFF_OLD_CUR.exists() else ""
    gen_line = "non_isogeny_primes = set(bad_primes) and set([3,5,7])"
    old_line = "A := {3 if 3 | N or |a3| = 3}"
    cur_line = "for every p in {3, 5, 7}, E admits no rational p-isogeny"
    a3_line = "def filter_CONDITION_a3"
    return {
        "generator_7286794": {
            "rule": gen_line,
            "found_as_removed_line_in_gen_to_old_diff":
                ("-        " + gen_line) in g2o,
            "evaluates_to": "{3, 5, 7} unconditionally — see and_semantics()"},
        "old_1a0489c": {
            "rule": old_line + " ∪ {5 if 5 | N} ∪ {7 if 7 | N}",
            "found_as_added_line_in_gen_to_old_diff": old_line in g2o,
            "found_as_removed_line_in_old_to_current_diff": old_line in o2c,
            "character": "CONDITIONAL — weaker than both neighbours"},
        "current_31fae20": {
            "rule": cur_line + "; and separately a_3 != ±3",
            "found_as_added_line_in_old_to_current_diff": cur_line in o2c,
            "a3_filter_added_in_old_to_current_diff": a3_line in o2c,
            "character": "unconditional again, plus E2 as its own filter"},
        "sequence": "strict -> relaxed -> strict + a_3",
        "diffs_present": bool(g2o) and bool(o2c)}


def and_semantics(base: list[dict]) -> dict:
    """What `set(bad_primes) and set([3,5,7])` actually evaluates to.

    Not what it was meant to do — what Python does with it. `x and y` is `y`
    whenever `x` is truthy, and a non-empty set is truthy. So the expression is
    {3, 5, 7} for every curve whose bad-prime set is non-empty, which is every
    curve of conductor > 1.
    """
    demo_nonempty = (set([2, 7]) and set([3, 5, 7]))
    demo_empty = (set() and set([3, 5, 7]))
    empties = sum(1 for r in base if not r["conductor_primes"])
    return {"expression": "set(bad_primes) and set([3,5,7])",
            "with_bad_primes_{2,7}": sorted(demo_nonempty),
            "with_bad_primes_empty": sorted(demo_empty),
            "base_curves_with_empty_bad_primes": empties,
            "so_on_every_base_curve_it_is": [3, 5, 7],
            "what_this_is_not": ("a claim about intent. `&` would have given "
                                 "bad_primes ∩ {3,5,7}, which is the OLD rule's "
                                 "shape; `and` gives {3,5,7}. Which was meant "
                                 "is not measurable here. What it evaluates to "
                                 "is")}


# --------------------------------------------------------------- the test

def relaxed_rule_removes(row: dict) -> bool:
    """`1a0489c`'s A-set rule, applied to one removed-census row."""
    N = int(row["conductor"])
    a3 = int(row["a3"]) if row["a3"] not in ("", None) else 0
    has3 = row["has_isogeny_3"] == "True"
    has5 = row["has_isogeny_5"] == "True"
    has7 = row["has_isogeny_7"] == "True"
    A = set()
    if N % 3 == 0 or abs(a3) == 3:
        A.add(3)
    if N % 5 == 0:
        A.add(5)
    if N % 7 == 0:
        A.add(7)
    return (3 in A and has3) or (5 in A and has5) or (7 in A and has7)


def the_prediction(base: list[dict], removed: list[dict]) -> dict:
    """If the OLD base came from the relaxed rule, none of its 1,355 isogeny
    curves may trip that rule. Tested on every one."""
    iso_rows = [r for r in removed if r["isogeny_set_357"] not in ("", "NONE")]
    tripped = [r["curve_label"] for r in iso_rows if relaxed_rule_removes(r)]
    # and the same rows under the STRICT rule must all be removed:
    strict = [r["curve_label"] for r in iso_rows
              if (r["has_isogeny_3"] == "True" or r["has_isogeny_5"] == "True"
                  or r["has_isogeny_7"] == "True")]
    labels = {r["curve_label"] for r in base}
    iso_in_old_base = sum(1 for r in iso_rows if r["curve_label"] in labels)
    return {"isogeny_curves_in_removed_census": len(iso_rows),
            "of_which_in_the_OLD_base": iso_in_old_base,
            "that_the_relaxed_rule_would_have_removed": len(tripped),
            "examples_tripped": tripped[:5],
            "that_the_strict_rule_removes": len(strict),
            "prediction_holds": not tripped and len(strict) == len(iso_rows),
            "reading": ("every isogeny curve in the OLD base has its isogeny at "
                        "a prime the relaxed rule does not inspect — 3 ∤ N with "
                        "|a_3| != 3, or 5 ∤ N, or 7 ∤ N. That is why the OLD "
                        "base kept them and the blob, frozen under the strict "
                        "rule, never had them")}


def the_three_artefacts(base: list[dict], removed: list[dict]) -> dict:
    """Blob keys, OLD base, CURRENT base — each against the rule that made it."""
    pv = cmap.provenance_of_the_twist_map(base, removed)
    new_map = cmap.load_new_map()
    a3 = {r["curve_label"] for r in removed if r["abs_a3_eq_3"] == "True"}
    iso = {r["curve_label"] for r in removed
           if r["isogeny_set_357"] not in ("", "NONE")}
    labels = {r["curve_label"] for r in base}
    return {"blob_7286794": {
                "keys": pv["in_old_map"],
                "equals_base_minus_isogeny_set": pv["missing_is_exactly_the_isogeny_set"],
                "rule": "strict {3,5,7}, no a_3"},
            "old_base_1a0489c": {
                "curves": len(labels),
                "contains_all_isogeny_curves": iso <= labels,
                "contains_all_a3_curves": a3 <= labels,
                "rule": "relaxed A-set"},
            "current_base_31fae20": {
                "curves": len(set(new_map)),
                "equals_old_minus_iso_union_a3":
                    set(new_map) == labels - (iso | a3),
                "removed": len(iso | a3),
                "rule": "strict {3,5,7} + a_3 != ±3"},
            "all_three_consistent": (
                pv["missing_is_exactly_the_isogeny_set"]
                and iso <= labels and a3 <= labels
                and set(new_map) == labels - (iso | a3))}


# ----------------------------------------------------- 02's pins, audited

def pins_02_demands() -> dict:
    """`02` §6: a reproduction must pin five things. §5: two flags go in
    metadata. §7: four rank fields stay distinct. Present / absent / N-A by the
    package's own stated scope."""
    prov = PROVENANCE.read_text(encoding="utf-8") if PROVENANCE.exists() else ""
    log = RUN_LOG.read_text(encoding="utf-8") if RUN_LOG.exists() else ""
    base0 = cmap.load_base()[0]
    pins = [
        {"pin": "paper version", "state": "ABSENT",
         "evidence": "no arXiv id or paper version string anywhere in the "
                     "package"},
        {"pin": "repository commit / file SHA", "state": "PRESENT",
         "evidence": "three commits, four blob SHA-1s, ecdata commit and shard "
                     "SHA-256s in sources/PROVENANCE.md and run.log",
         "check": all(c in prov for c in COMMITS.values())
                  and all(c in log for c in (COMMITS["old"], COMMITS["current"]))},
        {"pin": "Sage version", "state": "N/A BY SCOPE",
         "evidence": "PROVENANCE.md: a Sage/LMFDB replay 'is intentionally not "
                     "represented as completed here' — no Sage was run, so "
                     "there is no version to pin",
         "check": "intentionally not represented as completed" in prov},
        {"pin": "LMFDB release", "state": "PARTIAL",
         "evidence": "no LMFDB release pinned; the ecdata commit 25cec5e is "
                     "pinned instead, and ecdata is LMFDB's upstream for these "
                     "tables"},
        {"pin": "runtime flags", "state": "N/A BY SCOPE",
         "evidence": "skip_filter_S / skip_BSD_at_2_check appear only in the "
                     "archived upstream source, never as recorded values — "
                     "consistent with no Algorithm 2 run having happened"},
    ]
    flags_in_metadata = False
    for f in (PKG / "inputs" / "metadata").glob("*.json"):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if "skip_filter_S" in t or "skip_BSD_at_2_check" in t:
            flags_in_metadata = True
    rank_fields = ["algebraic rank", "analytic rank", "special value "
                   "nonvanishing", "proof/evidence type"]
    present_rank = [k for k in base0 if "rank" in k.lower()]
    return {"pins": pins,
            "present": sum(p["state"] == "PRESENT" for p in pins),
            "absent": sum(p["state"] == "ABSENT" for p in pins),
            "partial": sum(p["state"] == "PARTIAL" for p in pins),
            "not_applicable_by_scope": sum(p["state"] == "N/A BY SCOPE"
                                           for p in pins),
            "section_5_flags_recorded_in_metadata": flags_in_metadata,
            "section_7_rank_fields_demanded": rank_fields,
            "section_7_rank_fields_in_base_record": present_rank,
            "section_7_count": f"{len(present_rank)} of {len(rank_fields)}",
            "reading": ("the package is an exact ARTEFACT census and says so; "
                        "`02` §6's pins are for a REPRODUCTION. Two are N/A by "
                        "that scope, one is present, one partial, and one — "
                        "the paper version — is simply absent. §7's rank "
                        "fields are 0 of 4, which matters because Theorem "
                        "2.18 is stated for analytic rank 0 and the package "
                        "carries no rank evidence of either kind")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    doc = DOCS / "02_Paper_vs_Current_Code_Audit.md"
    text = doc.read_text(encoding="utf-8") if doc.exists() else ""
    base = cmap.load_base()
    removed = cmap.load_removed()

    rules = three_rules()
    sem = and_semantics(base)
    pred = the_prediction(base, removed)
    art = the_three_artefacts(base, removed)
    pins = pins_02_demands()

    ok = (bool(text) and "不是單純照抄" in text
          and rules["diffs_present"]
          and rules["generator_7286794"]["found_as_removed_line_in_gen_to_old_diff"]
          and rules["old_1a0489c"]["found_as_added_line_in_gen_to_old_diff"]
          and rules["old_1a0489c"]["found_as_removed_line_in_old_to_current_diff"]
          and rules["current_31fae20"]["found_as_added_line_in_old_to_current_diff"]
          and rules["current_31fae20"]["a3_filter_added_in_old_to_current_diff"]
          and sem["so_on_every_base_curve_it_is"] == [3, 5, 7]
          and sem["base_curves_with_empty_bad_primes"] == 0
          and pred["prediction_holds"]
          and art["all_three_consistent"]
          and pins["present"] == 1 and pins["absent"] == 1
          and pins["section_7_rank_fields_in_base_record"] == [])

    log = {
        "gate": "src58 — the rule behind each artefact, from the diffs, tested on the data",
        "source": "02_Paper_vs_Current_Code_Audit",
        "document_found": bool(text),
        "commits": COMMITS,
        "three_rules": rules,
        "and_semantics": sem,
        "the_prediction": pred,
        "the_three_artefacts": art,
        "pins_02_demands": pins,
        "headline": (f"Algorithm 1's isogeny condition went strict -> relaxed -> "
                     f"strict + a_3 across the three archived commits, and the "
                     f"twist blob was frozen at the first. The relaxed rule "
                     f"predicts that all {pred['isogeny_curves_in_removed_census']:,} "
                     f"isogeny curves in the OLD base escape its trigger — "
                     f"{pred['that_the_relaxed_rule_would_have_removed']} do not. "
                     f"Blob = base minus isogeny set, CURRENT = OLD minus "
                     f"(isogeny ∪ a_3): {art['all_three_consistent']}. The "
                     f"generator's `set(bad_primes) and set([3,5,7])` evaluates "
                     f"to {{3,5,7}} on every curve, whatever was meant. Of "
                     f"`02` §6's five pins: {pins['present']} present, "
                     f"{pins['partial']} partial, {pins['absent']} absent, "
                     f"{pins['not_applicable_by_scope']} N/A by the package's "
                     f"stated scope; §7's rank fields: "
                     f"{pins['section_7_count']}"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print("  three versions of Algorithm 1's isogeny condition, from the diffs")
    for k in ("generator_7286794", "old_1a0489c", "current_31fae20"):
        r = rules[k]
        print(f"    {k:<18} {r['rule'][:70]}")
    print(f"    sequence: {rules['sequence']}")
    print()
    print(f"  `{sem['expression']}` with bad primes {{2,7}} -> "
          f"{sem['with_bad_primes_{2,7}']}; empty -> "
          f"{sem['with_bad_primes_empty']}; base curves with empty bad primes: "
          f"{sem['base_curves_with_empty_bad_primes']}")
    print()
    print(f"  the prediction: {pred['isogeny_curves_in_removed_census']:,} "
          f"isogeny curves, {pred['of_which_in_the_OLD_base']:,} in the OLD "
          f"base; relaxed rule would remove "
          f"{pred['that_the_relaxed_rule_would_have_removed']}; strict removes "
          f"{pred['that_the_strict_rule_removes']:,} -> holds: "
          f"{pred['prediction_holds']}")
    print()
    for k, v in art.items():
        if isinstance(v, dict):
            print(f"  {k:<22} {json.dumps({a: b for a, b in v.items() if a != 'rule'})[:80]}")
    print(f"  all three consistent: {art['all_three_consistent']}")
    print()
    print("  02 §6 pins")
    for p in pins["pins"]:
        print(f"    {p['state']:<14} {p['pin']}")
    print(f"  02 §5 flags recorded as metadata values: "
          f"{pins['section_5_flags_recorded_in_metadata']}")
    print(f"  02 §7 rank fields in the base record: {pins['section_7_count']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
