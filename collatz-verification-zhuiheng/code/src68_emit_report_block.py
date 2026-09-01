"""Emit RUN-049's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src68_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src68-au2d21.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src68-drill.json"
REPORT = ROOT / "reports" / "RUN-049-HARD-ZETA-AU2D21-LOOP-DEFECT.md"
FIGURES = ROOT / "data" / "gate-logs" / "src68-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src68_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    sp, fc, df = g["surplus"], g["faithful_core"], g["defects"]
    sg, sc, ta = g["semigroup"], g["screening"], g["their_algebra"]
    ex, af, led, tc = (g["examples"], g["artifacts"], g["ledger"],
                       g["their_claims"])

    out = [
        BEGIN, "",
        "**The population.** **%d** bridges from **%d** distinct sources "
        "(longest tail %d), of which **%d** have zero total lift and **%d** do "
        "not — the fifth round running in which the positive-lift branch has "
        "no finite instance."
        % (pop["bridges"], pop["sources"], pop["longest_tail"],
           pop["zero_lift"], pop["positive_lift"]),
        "",
        "**Theorem 3.1's surplus budget, and it binds.** The surplus identity "
        "`sum(q-1) = ceil(beta h) - h` failed **%d** times across **%d** "
        "bridges. The budget `A_k (s_k - 1) <= surplus` failed **%d** times "
        "over **%d** bridge-precision levels. Unlike the loop-mass bound of "
        "the previous round, this one is **live**: **%d** levels carry an "
        "alias-large edge, the largest count on one bridge is **%d**, and on "
        "**%d of %d levels** (%s) one more alias edge would have broken it — "
        "with a smallest slack of **%s**, so it is not merely tight but "
        "attained."
        % (sp["surplus_identity_violations"], sp["bridges"],
           sp["budget_theorem_3_1_violations"], sp["levels"],
           sp["levels_with_an_alias_large_edge"],
           sp["largest_alias_count_seen"],
           sp["levels_where_the_budget_binds"], sp["levels"],
           pct(sp["levels_where_the_budget_binds"], sp["levels"]),
           sp["smallest_budget_slack_seen"]),
        "",
        "**Theorem 4.1's faithful core.** Over **%d** bridge-precision levels, "
        "**%d** cycles and **%d** retained edges: **%d** edges at or above the "
        "period, **%d** labels not unique in the faithful range over **%d** "
        "brute-force uniqueness checks — the claim that makes the core "
        "*faithful*, and the one thing in the round that cannot be checked by "
        "algebra alone. Cycles longer than the period **%d**; total faithful "
        "mass **%d**. The finite mass bound failed **%d** times and is "
        "positive on **%d of %d levels** (%s), so it discriminates on a "
        "minority — better than the previous round's 4 in 3,826, still worth "
        "the denominator. The high-lift refinement failed **%d** times."
        % (fc["levels"], fc["cycles"], fc["edges"],
           fc["retained_edge_at_or_above_the_period"],
           fc["label_not_unique_in_the_faithful_range"],
           fc["uniqueness_checks"], fc["cycle_longer_than_the_period"],
           fc["total_faithful_mass"], fc["mass_below_the_finite_bound"],
           fc["levels_where_the_bound_is_positive"], fc["levels"],
           pct(fc["levels_where_the_bound_is_positive"], fc["levels"]),
           fc["high_lift_mass_below_its_bound"]),
        "",
        "**NO-GO 12.1, measured.** Over **%d** graph cycles from **%d** "
        "bridges: **%d** fail to return to their residue, **%d** violate "
        "Theorem 9.1's certificate, and **%d** have a non-integral defect — "
        "the certificate is exact on *every* cycle, spliced or not, exactly as "
        "the round says. Theorem 10.2's quotient-layer lift is a different "
        "matter. Of the cycles, **%d are contiguous** and **%d are spliced** "
        "(%s). The lift holds on **%d of %d contiguous** cycles and fails on "
        "**%d of %d spliced** ones — with **%d** spliced cycles where it "
        "happened to hold anyway. A clean separation: licensed everywhere it "
        "is licensed, and false everywhere it is not. Largest absolute defect "
        "seen **%d**; **%d** defects are zero (%s), so the object is not "
        "degenerate."
        % (df["cycles"], df["bridges"],
           df["cycle_does_not_return_to_its_residue"],
           df["certificate_theorem_9_1_violations"],
           df["defect_not_integral"], df["contiguous_cycles"],
           df["spliced_cycles"],
           pct(df["spliced_cycles"], df["cycles"]),
           df["contiguous_cycles"]
           - df["quotient_lift_violations_on_contiguous_cycles"],
           df["contiguous_cycles"],
           df["quotient_lift_violations_on_spliced_cycles"],
           df["spliced_cycles"],
           df["quotient_lift_holds_anyway_on_a_spliced_cycle"],
           df["largest_absolute_defect_seen"], df["defects_that_are_zero"],
           pct(df["defects_that_are_zero"], df["cycles"])),
        "",
        "**Theorem 11.1, and what self-composition cannot see.** Over **%d** "
        "residue classes: **%d** self-compositions and **%d** distinct pairs. "
        "The true law failed **%d** times on self and **%d** on distinct "
        "pairs. The coefficient-swapped law — `2^{Q_D} d(C) + 3^{L_C} d(D)` "
        "instead of `3^{L_D} d(C) + 2^{Q_C} d(D)` — disagreed with the true "
        "one on **%d of %d** self-compositions and agreed with it on **%d of "
        "%d** distinct pairs, disagreeing on **%d**. So the two laws are "
        "**indistinguishable under self-composition and separated by every "
        "distinct pair**. The bundle runs twenty self-compositions. **%d** "
        "composite defects were non-integral and **%d** composed cycles failed "
        "to return; **%d** pairs turned out to be the same word."
        % (sg["residue_classes"], sg["self_compositions"],
           sg["distinct_pairs"], sg["true_law_violations_on_self"],
           sg["true_law_violations_on_distinct_pairs"],
           sg["swapped_law_disagreeing_on_self"], sg["self_compositions"],
           sg["swapped_law_agreeing_on_distinct_pairs"], sg["distinct_pairs"],
           sg["swapped_law_disagreeing_on_distinct_pairs"],
           sg["composite_defect_not_integral"],
           sg["composed_cycle_does_not_return"], sg["pair_words_identical"]),
        "",
        "**Theorems 6.1 and 7.1, on real words and for sharpness.** Over "
        "**%d** real bridge words and **%d** synthetic endpoint words and "
        "**%d** synthetic source words: **%d** endpoint screening violations, "
        "**%d** disagreements between the whole-word residue and the k-term "
        "suffix formula, **%d** source screening violations. Sharpness matters "
        "as much as the horizon: over **%d** probes, a change to the LAST "
        "valuation — inside every horizon — moved nothing **%d** times, and a "
        "change to the FIRST — outside it — moved something **%d** times. "
        "Without both, \"depends only on the final K\" would be satisfied by a "
        "residue that never moves at all."
        % (sc["real_words"], sc["synthetic_words"],
           sc["synthetic_source_words"],
           sc["endpoint_screening_violations"],
           sc["endpoint_suffix_formula_violations"],
           sc["source_screening_violations"], sc["sharpness_probes"],
           sc["changes_inside_the_horizon_that_moved_nothing"],
           sc["changes_outside_the_horizon_that_moved_something"]),
        "",
        "**Three of the bundle's thirteen counters cannot fail.** "
        "`faithful_core_asymptotic_algebra` runs **%d** iterations and asserts "
        "`gamma < eta` (arranged by the `max(gamma+1e-3, eta)` on the line "
        "above — **%d** could have failed), `1-eta+gamma < 1` (the same "
        "inequality restated — **%d** samples where the two differed), and "
        "`C_FAITH > 0` on a constant computed outside the loop (**%d** samples "
        "where it varied). `polynomial_precision_horizon_algebra` runs **%d** "
        "and asserts a quantity whose smallest margin over the same ranges is "
        "**%.1f** (**%d** could have failed). "
        "`near_full_almost_total_loop_algebra` runs **%d** and asserts "
        "`1/(log h)^A < 1` with `log h >= 100`, smallest margin **%.4f** "
        "(**%d** could have failed). Thirty thousand executions; fifth round "
        "running, and every shape is one this sweep has already catalogued."
        % (ta["faithful_core_samples"],
           ta["faithful_core_gamma_not_below_eta"],
           ta["faithful_core_second_assertion_differing_from_the_first"],
           ta["faithful_core_constant_varying_across_the_loop"],
           ta["horizon_samples"], ta["horizon_smallest_margin"],
           ta["horizon_could_have_failed"], ta["near_full_samples"],
           ta["near_full_smallest_margin"], ta["near_full_could_have_failed"]),
        "",
        "**All twenty published cycle examples, rebuilt.** **%d** disagreeing "
        "lengths, **%d** valuation sums, **%d** defects, **%d** cycles failing "
        "to return, **%d** certificate violations, **%d** labels at or above "
        "the period."
        % (ex["length_disagreeing"], ex["valuation_sum_disagreeing"],
           ex["defect_disagreeing"], ex["cycle_does_not_return"],
           ex["certificate_violations"], ex["label_at_or_above_the_period"]),
        "",
        "| `M` | `r` | word | `L` | `Q` | defect |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in ex["rows"]:
        out.append("| %d | %d | `%s` | %d | %d | %d |"
                   % (row["M"], row["r"], row["word"], row["L"], row["Q"],
                      row["defect"]))
    out += [
        "",
        "**Constants.** %d checked: **%d** disagree with both readings of "
        "their own formula, %d are the nearest double, %d are the float64 "
        "chain, %d brackets could not decide, and the frontier and the report "
        "disagree on **%d**."
        % (cs["constants_checked"], cs["disagreeing_with_both_evaluations"],
           cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["undecided_brackets"], cs["frontier_and_report_disagreeing"]),
        "",
        "| constant | frontier | report | nearest double | verdict |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in cs["rows"]:
        out.append("| `%s` | %s | %s | %s | %s |"
                   % (row["constant"], row["frontier"], row["report"],
                      row.get("nearest_double", "—"), row["verdict"]))
    out += [
        "",
        "**Artifacts.** %d files, %d carrying a `CHECKSUMS` digest, **%d** "
        "mismatches, **%d** manifest lines naming a missing file; %s carry no "
        "digest anywhere. The source-validation record names **%d** files and "
        "digests **%d** of them, reporting `status = %s` with **%d** issues "
        "and **%d** flags not true; its nine counter values disagree with the "
        "checker report **%d** times. %d files are absent from it: %s."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "no files",
           af["validation_files_named"],
           af["validation_entries_with_a_digest"], af["validation_status"],
           af["validation_issue_entries"], af["validation_flags_not_true"],
           af["validation_counts_disagreeing_with_the_report"],
           len(af["files_absent_from_the_validation_record"]),
           ", ".join("`%s`" % n
                     for n in af["files_absent_from_the_validation_record"])),
        "",
        "**Ledger coverage.** The paper lists %d proved items, %d open "
        "problems and %d NO-GO headings; the ledger carries %d, %d and %d, "
        "with an `open` key (%s). Open items with no trace: %s. NO-GO "
        "headings with no trace: %s. The heuristic deciding those lists has "
        "controls at both ends and failed neither (%d, %d)."
        % (led["paper_proved_items"], led["paper_open_items"],
           led["paper_no_go_headings"], led["ledger_proved_items"],
           led["ledger_open_items"], led["ledger_no_go_items"],
           led["ledger_has_an_open_key"],
           ", ".join(led["open_items_absent_from_the_ledger"]) or "none",
           ", ".join(led["no_go_headings_absent_from_the_ledger"]) or "none",
           led["heuristic_failed_its_positive_control"],
           led["heuristic_failed_its_negative_control"]),
        "",
        "**Their counters beside mine**, keyed on their names rather than "
        "mine: %d of %d had no counterpart here, %d are reported as zero, and "
        "**%d of %d are reproduced exactly** from the definition."
        % (tc["checks_i_did_not_reproduce"], len(tc["rows"]),
           tc["checks_they_report_as_zero"], tc["counts_i_reproduce_exactly"],
           len(tc["rows"])),
        "",
        "| check | theirs | mine |",
        "| --- | --- | --- |",
    ]
    for row in tc["rows"]:
        out.append("| `%s` | %s | %s |"
                   % (row["check"], row["theirs"],
                      "—" if row["mine"] is None else row["mine"]))
    tot = d["totals"]
    out += [
        "",
        "**Instrument and drill.** %d instrument self-checks, %d failed. The "
        "mutation drill planted **%d** defects: **%d** caught by the check "
        "they attack, **%d** missed, **%d** malformed, %d caught only by "
        "another counter; %d of %d controls left the gate undisturbed."
        % (ins["checks"], len(ins["failed"]), tot["defects"], tot["caught"],
           tot["missed"], tot["malformed"],
           tot["caught_but_by_another_counter"],
           tot["controls_undisturbed"], tot["controls"]),
        "", END,
    ]
    return "\n".join(out)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (GATE_LOG, DRILL_LOG):
        if not path.exists():
            print(json.dumps({"error": "missing log", "path": str(path)},
                             indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    if not g.get("passed"):
        print(json.dumps({"error": "the recheck is red",
                          "failures": g.get("failures")},
                         indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red",
                          "totals": d.get("totals")},
                         indent=2, ensure_ascii=False))
        return 2
    guard = check_against_snapshot(build, [g, d], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to",
                          "guard": guard}, indent=2))
        return 2
    block = build(g, d)
    text = REPORT.read_text(encoding="utf-8")
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail
    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src68_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src68_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
