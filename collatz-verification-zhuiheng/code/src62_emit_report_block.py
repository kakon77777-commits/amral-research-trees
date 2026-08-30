"""Emit RUN-043's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src62_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src62-au2d15.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src62-drill.json"
REPORT = ROOT / "reports" / "RUN-043-HARD-ZETA-AU2D15-RECORD-SPARSITY.md"
FIGURES = ROOT / "data" / "gate-logs" / "src62-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src62_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, q1 = g["instrument"], g["constants"], g["q1"]
    rec, enc, sh = g["records"], g["enclosure"], g["shallow"]
    ar, led, tc = g["artifacts"], g["ledger"], g["their_claims"]

    out = [
        BEGIN, "",
        "**Section 10's inequality, on segments that need no premise.** "
        "`N_1(s,g) >= (2-beta) g + (delta_{s+g} - delta_s)` was checked on "
        "**%d** pairs rooted at a suffix minimum and, as a control that the "
        "root really is unnecessary, **%d** rooted anywhere: **%d** and **%d** "
        "violations. The valuation-sum identity it rests on failed **%d** "
        "times, and no valuation below one was seen (**%d**). The tightest "
        "case has slack **%s** — attained, not loose — at `g = %s` with "
        "`N_1 = %s`. The bare floor `(2-beta)g` without the correction term "
        "failed **%d** times on this population."
        % (q1["pairs_from_a_suffix_minimum"], q1["pairs_from_an_arbitrary_root"],
           q1["exact_inequality_violations"],
           q1["exact_inequality_violations_off_a_record"],
           q1["valuation_sum_identity_violations"], q1["a_valuation_below_one"],
           q1["tightest_slack_in_the_inequality"]["slack"],
           q1["tightest_slack_in_the_inequality"]["g"],
           q1["tightest_slack_in_the_inequality"]["N1"],
           q1["pairs_where_the_floor_alone_would_fail"]),
        "",
        "**The record process.** %d orbits carried two or more records "
        "(longest chain %d), giving **%d** record edges. The exact multiplier "
        "`Y_b 2^p = Y_a 3^g P` — written with no `beta`, so no bracket decides "
        "it — failed **%d** times; the product concatenation "
        "`prod P_j = P_{c1,cR}` **%d**; record values were non-increasing "
        "**%d**; Lemma 11.1's span `Y_max - Y_s >= 3g-7` **%d** of %d; the "
        "`U_6` capacity behind it **%d**; and section 7's state-ceiling "
        "identity **%d**."
        % (rec["orbits_with_two_or_more_records"], rec["largest_record_count"],
           rec["record_edges"], rec["exact_multiplier_violations"],
           rec["product_concatenation_violations"],
           rec["record_values_not_increasing"], rec["lemma_11_1_violations"],
           rec["lemma_11_1_checked"], rec["gap_duration_above_the_U6_capacity"],
           rec["state_ceiling_identity_violations"]),
        "",
        "**Theorem 4.1 has an empty population, and so does its tail.** Of the "
        "%d record edges, **%d ascend, %d descend, %d are undecided**. So "
        "`V^-_rec` is identically zero: the theorem was exercised **%d** times "
        "(**%d** violations), and the tail bound **%d** times out of %d tails "
        "examined. The bundle reports the same thing — `record_slack_drop_edge` "
        "and `record_descent_implies_crossing` are both zero in its own "
        "checker report, and section 18 says it in prose."
        % (rec["record_edges"], rec["record_slack_ascending"],
           rec["record_slack_descending"], rec["record_slack_undecided"],
           rec["theorem_4_1_checked"], rec["theorem_4_1_violations"],
           rec["tail_descents"], rec["tail_checked"]),
        "",
        "**The enclosure, as the exponent algebra it is.** Over %d grid "
        "points, with the slacks sampled relative to `log2 N` so the "
        "hypothesis is reachable (**%d** of them satisfy it): Theorem 8.1 "
        "**%d** violations, Corollary 8.2 **%d**, and the inversion behind "
        "Corollary 6.3 **%d**."
        % (enc["grid_points"], enc["antecedent_holds"],
           enc["enclosure_violations"], enc["corollary_8_2_violations"],
           enc["support_transfer_inversion_violations"]),
        "",
        "**Corollary 12.1 needs a B source.** Across %d orbits and **%d** "
        "suffix minima there are **%d**, so it was exercised **%d** times. "
        "That denominator is the report, not the zero violations."
        % (sh["orbits"], sh["suffix_minima"], sh["B_sources_found"],
           sh["corollary_12_1_checked"]),
        "",
        "**Constants.** %d checked: **%d** disagree with both readings of "
        "their own formula, %d are the nearest double, %d are what the same "
        "formula gives in float64, and %d brackets could not decide."
        % (cs["constants_checked"], cs["disagreeing_with_both_evaluations"],
           cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["undecided_brackets"]),
        "",
        "| constant | published | nearest double | vs bracket | vs float64 chain |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in cs["rows"]:
        out.append("| `%s` | %s | %s | %s | %s |" % (
            r["name"], r["published"], r["nearest_double"],
            "exact" if r["ulps_vs_bracket"] == 0
            else "%+d ulp" % r["ulps_vs_bracket"],
            "exact" if r["ulps_vs_float64_chain"] == 0
            else "%+d ulp" % r["ulps_vs_float64_chain"]))
    out += [
        "",
        "**Artifacts.** %d files, %d carrying a `CHECKSUMS` digest, **%d** "
        "mismatches, **%d** manifest lines naming a missing file; the only "
        "file with no digest anywhere is `%s`. The source-validation record "
        "carries **%d per-file entries and %d digests** (`%s`) — it reports "
        "`status = %s` and %s a checker-stdout digest, but the per-file table "
        "RUN-042 verified is gone. Its top-level keys are now `%s`."
        % (ar["files_present"], ar["digests_listed"], ar["digest_mismatches"],
           ar["checksum_lines_naming_a_missing_file"],
           ", ".join(ar["files_with_no_digest_anywhere"]),
           ar["validation_per_file_entries"],
           ar["validation_entries_with_a_digest"],
           "carries per-file digests" if ar["validation_carries_per_file_digests"]
           else "carries none",
           ar["validation_status"],
           "does carry" if ar["validation_has_a_checker_stdout_digest"]
           else "does not carry",
           ", ".join("`%s`" % k for k in ar["validation_top_level_keys"])),
        "",
        "**Ledger coverage.** The paper lists %d proved items, %d open "
        "problems and %d NO-GO headings; the ledger carries %d, %d and %d, "
        "with an `open` key (%s). Open items with no trace: %s. NO-GO "
        "headings with no trace: %s. The heuristic that decides those two "
        "lists now has controls at both ends and failed neither (%d, %d)."
        % (led["paper_proved_items"], led["paper_open_items"],
           led["paper_no_go_headings"], led["ledger_proved_items"],
           led["ledger_open_items"], led["ledger_no_go_items"],
           led["ledger_has_an_open_key"],
           json.dumps(led["open_items_absent_from_the_ledger"])
           if led["open_items_absent_from_the_ledger"] else "none",
           json.dumps(led["no_go_headings_absent_from_the_ledger"])
           if led["no_go_headings_absent_from_the_ledger"] else "none",
           led["heuristic_failed_its_positive_control"],
           led["heuristic_failed_its_negative_control"]),
        "",
        "**Their counters beside mine.** %d of their checks had no "
        "counterpart here; **%d** of the nine they report as zero, and **%d** "
        "of those we both report as zero. The two large counts beside them — "
        "`record_total_down_variation` and `record_tail_drop` — are "
        "evaluations of a quantity their own `record_slack_drop_edge = 0` "
        "makes identically zero."
        % (tc["checks_i_did_not_reproduce"], tc["checks_they_report_as_zero"],
           tc["checks_we_both_report_as_zero"]),
        "",
        "| check | theirs | mine |",
        "| --- | --- | --- |",
    ]
    for r in tc["rows"]:
        out.append("| `%s` | %s | %s |"
                   % (r["check"], r["theirs"],
                      "—" if r["mine"] is None else r["mine"]))
    t = d["totals"]
    out += [
        "",
        "**Instrument self-checks:** %d, %d failed."
        % (ins["checks"], len(ins["failed"])),
        "",
        "**Drill.** %d defects planted one at a time, **%d caught**, %d "
        "malformed, %d missed; %d were caught only by a counter other than the "
        "one aimed at. All %d anchors matched exactly one place before "
        "anything was planted. %d of %d controls undisturbed, and the gate "
        "came back byte-identical."
        % (t["defects"], t["caught"], t["malformed"], t["missed"],
           t["caught_but_by_another_counter"], d["anchors_matching_once"],
           t["controls_undisturbed"], t["controls"]),
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
        print(json.dumps({"tool": "src62_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src62_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
