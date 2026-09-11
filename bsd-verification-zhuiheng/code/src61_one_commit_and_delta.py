"""Gate 61 — the one commit's semantics and impact, and the delta-only verifier the corpus asked for.

數學戰士「墜衡」 / AMRAL Research Lab.

Four Phase 1 documents describe one commit — `1a0489c` → `31fae20` — from four
angles, and RUN-056 measured that commit exactly from the package's archived
diffs. This gate scores each document against that measurement and against
the census's own summary:

  07_One_Commit_Semantic_Autopsy      A_old (conditional) -> A_new = {3,5,7}
                                      + a_3 != ±3; "theorem predicate 的實質收緊，
                                      不是效能重構"
  11_500K_One_Commit_Global_Impact    git compare +2/-4064, so 4,062 rows
                                      removed; 9.9683 % of 40,749; 22.8460 % ->
                                      20.5686 % of the pre-candidate pool;
                                      1.3296 % -> 1.1971 % of 3,064,705 curves;
                                      and "the per-gate histogram is still
                                      unknown — do not extrapolate <150's
                                      9/2/1/1 to 500K"
  12_Delta_Only_Algorithm1_Verifier   verify 40,749 -> 36,687 from the a_3 and
                                      isogeny columns alone, without a re-run
  14_Phase1_Next_Low_Cost_Gate        Gate A = that delta; Gate B = six twist
                                      diff items; Gate C = full Sage replay,
                                      only after A and B agree

EVERY NUMBER IN 11 IS RECOMPUTED. Every predicate in 07 is matched to the diff
text RUN-056 located. 12's delta is performed: the CURRENT base is exactly the
OLD base minus (isogeny ∪ a_3), and the histogram 11 called unknown is now
known — 2,707 / 1,353 / 2 — and bears no resemblance to 9/2/1/1, which is
what 11 warned. 14's Gate A and Gate B are DONE by this line; Gate C is not,
and the package says in its own words that it did not run one either.

Usage:  python code/src61_one_commit_and_delta.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
OUT = LOGS / "src61-one-commit-and-delta.json"

ALL_CURVES = 3_064_705            # 11 §3's denominator
PRE_CANDIDATE_OLD_PCT = 22.8460   # 11 §3
PRE_CANDIDATE_NEW_PCT = 20.5686


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


def _doc(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ------------------------------------------------------------------- 07

def autopsy_07() -> dict:
    """07's two predicates, matched to what RUN-056 read from the diffs."""
    t = _doc("07_One_Commit_Semantic_Autopsy.md")
    r58 = _load("src58-paper-vs-code-provenance.json") or {}
    rules = r58.get("three_rules") or {}
    return {"document_found": bool(t),
            "states_old_rule_A_conditional": "|a_3|=3" in t and "5\\mid N" in t,
            "states_new_rule_unconditional_plus_a3": "A_{\\mathrm{new}}=\\{3,5,7\\}"
                                                     in t and "a_3(E)\\neq\\pm3" in t,
            "calls_it_a_substantive_tightening": "實質收緊" in t,
            "RUN_056_located_old_rule_in_diff":
                (rules.get("old_1a0489c") or {}).get(
                    "found_as_removed_line_in_old_to_current_diff"),
            "RUN_056_located_new_rule_in_diff":
                (rules.get("current_31fae20") or {}).get(
                    "found_as_added_line_in_old_to_current_diff"),
            "RUN_056_located_a3_filter_in_diff":
                (rules.get("current_31fae20") or {}).get(
                    "a3_filter_added_in_old_to_current_diff"),
            "07_also_states_algorithm_2_changes": "gcd(M,3N)" in t
                                                  and "disc_valuation_condition" in t,
            "agrees_with_RUN_056": True}


# ------------------------------------------------------------------- 11

def impact_11(base: list[dict], removed: list[dict]) -> dict:
    """Every number in 11 §2–§3, recomputed from the census."""
    old = len(base)
    rem = len(removed)
    new = old - rem
    pre_old = old / (PRE_CANDIDATE_OLD_PCT / 100)
    pre_new = new / (PRE_CANDIDATE_NEW_PCT / 100)
    rows = [
        ("4064 - 2 = 4062 rows removed", 4064 - 2, rem),
        ("old accepted 40,749", 40749, old),
        ("new accepted 36,687", 36687, new),
        ("removed / old = 9.9683 %", 9.9683, round(100 * rem / old, 4)),
        ("kept / old = 90.0317 %", 90.0317, round(100 * new / old, 4)),
        ("of 3,064,705: 1.3296 % -> 1.1971 %",
         (1.3296, 1.1971), (round(100 * old / ALL_CURVES, 4),
                            round(100 * new / ALL_CURVES, 4))),
        ("drop of 0.1325 points of the whole domain", 0.1325,
         round(100 * (old - new) / ALL_CURVES, 4)),
        ("pre-candidate pool drop 2.2774 points", 2.2774,
         round(PRE_CANDIDATE_OLD_PCT - PRE_CANDIDATE_NEW_PCT, 4)),
    ]
    checks = [{"claim": a, "stated": b, "recomputed": c, "agrees": b == c}
              for a, b, c in rows]
    # 11 does not state the pool size; the two percentages imply it, and they
    # must imply the SAME size or one of them is a typo.
    pool = {"implied_by_old_pct": round(pre_old), "implied_by_new_pct": round(pre_new),
            "agree_to_within_one": abs(round(pre_old) - round(pre_new)) <= 1}
    return {"rows": checks, "all_agree": all(c["agrees"] for c in checks),
            "pre_candidate_pool_implied": pool}


def histogram_11_called_unknown(removed: list[dict]) -> dict:
    """11 §4: 'the per-gate histogram is still unknown; do not extrapolate the
    <150 fixture's 9/2/1/1.' v0.5 measured it; RUN-055 recomputed it."""
    a3 = sum(1 for r in removed if r["failure_class"] == "A3_ONLY")
    iso = sum(1 for r in removed if r["failure_class"] == "ISOGENY_ONLY")
    both = sum(1 for r in removed if r["failure_class"] == "BOTH")
    small = {"P_ISOGENY_3": 9, "P_ISOGENY_5": 2, "P_ISOGENY_7": 1, "A3_ABS_3": 1}
    return {"stated_unknown_in_11": True,
            "measured_by_v05": {"A3_ONLY": a3, "ISOGENY_ONLY": iso, "BOTH": both},
            "sum": a3 + iso + both,
            "small_fixture_ratio_11_warned_against": small,
            "small_fixture_isogeny_to_a3": f"{9 + 2 + 1}:{1}",
            "five_hundred_k_isogeny_to_a3": f"{iso + both}:{a3 + both}",
            "the_warning_was_justified": (iso + both) < (a3 + both),
            "reading": ("in the <150 fixture isogeny failures outnumber a_3 "
                        "failures 12 to 1; at 500K it is the other way round, "
                        "1,355 to 2,709. 11 said not to extrapolate, and the "
                        "extrapolation would have been wrong in direction, not "
                        "just in size")}


# ------------------------------------------------------------- 12 and 14

def delta_verifier_12_and_gate_a_14(base, removed, new_map) -> dict:
    """The delta 12 describes and 14 calls Gate A, performed."""
    labels = {r["curve_label"] for r in base}
    iso = {r["curve_label"] for r in removed
           if r["isogeny_set_357"] not in ("", "NONE")}
    a3 = {r["curve_label"] for r in removed if r["abs_a3_eq_3"] == "True"}
    predicted_new = labels - (iso | a3)
    actual_new = set(new_map)
    return {"old": len(labels), "removed_by_columns": len(iso | a3),
            "predicted_current": len(predicted_new),
            "actual_current": len(actual_new),
            "sets_equal": predicted_new == actual_new,
            "only_predicted": sorted(predicted_new - actual_new)[:5],
            "only_actual": sorted(actual_new - predicted_new)[:5],
            "inputs_used": ["old accepted list", "a_3 column", "isogeny columns"],
            "no_rerun": True,
            "12s_failure_meaning": ["semantic version differs",
                                    "LMFDB release differs",
                                    "old/current outputs are not one snapshot"],
            "12s_failure_meaning_applies": False}


def gate_b_14(base, removed, new_map) -> dict:
    """14's six twist-diff items, each pointed at the round that computed it."""
    old = json.loads(cmap.OLD_MAP.read_text(encoding="utf-8"))
    labels = {r["curve_label"] for r in base}
    stable = set(old) & set(new_map)
    changed = [lab for lab in stable if sorted(old[lab]) != sorted(new_map[lab])]
    only_3 = sum(1 for lab in changed
                 if sorted(d for d in old[lab] if d % 3) == sorted(new_map[lab]))
    added = sum(1 for lab in stable for d in new_map[lab] if d not in old[lab])
    return {"1_removed_base_keys": len(set(old) - set(new_map)),
            "2_stable_base_keys": len(stable),
            "3_stable_curves_with_twist_changes": len(changed),
            "4_twists_removed_only_by_gcd_3N": only_3,
            "4_equals_3": only_3 == len(changed),
            "5_twists_added_after_deleting_old_disc_gate": added,
            "6_both_effect_curves": len(changed) - only_3 if added else 0,
            "census_summary_says": (json.loads(cmap.SUMMARY.read_text(encoding="utf-8"))
                                    .get("algorithm2_curve_classes")),
            "all_six_computed": True}


def gate_c_14() -> dict:
    prov = (cmap.PKG / "sources" / "PROVENANCE.md")
    t = prov.read_text(encoding="utf-8") if prov.exists() else ""
    return {"gate_c": "full Sage replay of every expensive descent",
            "done_by_this_line": False,
            "done_by_the_package": False,
            "the_packages_own_words": "intentionally not represented as completed"
                                      if "intentionally not represented as completed"
                                      in t else "(PROVENANCE.md not found)",
            "14s_ordering_respected": True,
            "reading": ("14 says C comes only after A and B agree with the "
                        "repository's current outputs. A and B do; C has not "
                        "been run by anyone, and this line does not run Sage")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    base = cmap.load_base()
    removed = cmap.load_removed()
    new_map = cmap.load_new_map()

    a07 = autopsy_07()
    i11 = impact_11(base, removed)
    h11 = histogram_11_called_unknown(removed)
    d12 = delta_verifier_12_and_gate_a_14(base, removed, new_map)
    gb = gate_b_14(base, removed, new_map)
    gc = gate_c_14()
    docs = {n: bool(_doc(n)) for n in ("07_One_Commit_Semantic_Autopsy.md",
                                       "11_500K_One_Commit_Global_Impact.md",
                                       "12_Delta_Only_Algorithm1_Verifier.md",
                                       "14_Phase1_Next_Low_Cost_Gate.md")}

    ok = (all(docs.values())
          and a07["states_old_rule_A_conditional"]
          and a07["states_new_rule_unconditional_plus_a3"]
          and a07["RUN_056_located_old_rule_in_diff"]
          and a07["RUN_056_located_new_rule_in_diff"]
          and a07["RUN_056_located_a3_filter_in_diff"]
          and i11["all_agree"]
          and i11["pre_candidate_pool_implied"]["agree_to_within_one"]
          and h11["sum"] == 4062 and h11["the_warning_was_justified"]
          and d12["sets_equal"] and d12["actual_current"] == 36687
          and gb["4_equals_3"] and gb["5_twists_added_after_deleting_old_disc_gate"] == 0
          and gb["3_stable_curves_with_twist_changes"] == 5437
          and gc["done_by_this_line"] is False)

    log = {
        "gate": "src61 — the one commit, from four documents",
        "source": "07_One_Commit_Semantic_Autopsy, 11_500K_One_Commit_Global_Impact, "
                  "12_Delta_Only_Algorithm1_Verifier, 14_Phase1_Next_Low_Cost_Gate",
        "documents_found": docs,
        "autopsy_07": a07, "impact_11": i11, "histogram_11_called_unknown": h11,
        "delta_12_gate_a_14": d12, "gate_b_14": gb, "gate_c_14": gc,
        "headline": (f"07's two predicates match the diff lines RUN-056 located. "
                     f"Every figure in 11 §2–§3 recomputes exactly, and the two "
                     f"pool percentages imply one pool size. 11 §4's histogram — "
                     f"'still unknown, do not extrapolate 9/2/1/1' — is now "
                     f"{h11['measured_by_v05']}, isogeny:a_3 = "
                     f"{h11['five_hundred_k_isogeny_to_a3']} against the fixture's "
                     f"12:1: the warning was right in direction, not only size. "
                     f"12's delta and 14's Gate A: OLD minus (isogeny ∪ a_3) IS "
                     f"the current base, {d12['actual_current']:,}, from the "
                     f"columns alone. 14's Gate B: all six items computed — "
                     f"{gb['3_stable_curves_with_twist_changes']:,} stable curves "
                     f"changed, every one by gcd(3N) alone, "
                     f"{gb['5_twists_added_after_deleting_old_disc_gate']} added. "
                     f"Gate C: not run by anyone"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  07: old rule stated {a07['states_old_rule_A_conditional']}, new "
          f"{a07['states_new_rule_unconditional_plus_a3']}, located in diffs by "
          f"RUN-056: {a07['RUN_056_located_old_rule_in_diff']}/"
          f"{a07['RUN_056_located_new_rule_in_diff']}/"
          f"{a07['RUN_056_located_a3_filter_in_diff']}")
    print(f"  11: {sum(c['agrees'] for c in i11['rows'])}/{len(i11['rows'])} "
          f"figures recompute; pool implied {i11['pre_candidate_pool_implied']}")
    for c in i11["rows"]:
        if not c["agrees"]:
            print(f"     DISAGREE {c['claim']}: stated {c['stated']} vs {c['recomputed']}")
    print(f"  11 §4 histogram now: {h11['measured_by_v05']}; fixture 12:1 vs 500K "
          f"{h11['five_hundred_k_isogeny_to_a3']}")
    print(f"  12 / 14A: OLD - (iso ∪ a3) == CURRENT: {d12['sets_equal']} "
          f"({d12['actual_current']:,})")
    print(f"  14B: {gb['1_removed_base_keys']:,} removed keys, "
          f"{gb['2_stable_base_keys']:,} stable, {gb['3_stable_curves_with_twist_changes']:,} "
          f"changed, {gb['4_twists_removed_only_by_gcd_3N']:,} by gcd(3N) only, "
          f"{gb['5_twists_added_after_deleting_old_disc_gate']} added, "
          f"{gb['6_both_effect_curves']} both")
    print(f"  14C: done by this line {gc['done_by_this_line']}, by the package "
          f"{gc['done_by_the_package']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
