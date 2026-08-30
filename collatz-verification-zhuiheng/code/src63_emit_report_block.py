"""Emit RUN-044's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src63_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src63-au2d16.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src63-drill.json"
REPORT = ROOT / "reports" / "RUN-044-HARD-ZETA-AU2D16-RECORD-GAP-TRANSPORT.md"
FIGURES = ROOT / "data" / "gate-logs" / "src63-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src63_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, bk = g["instrument"], g["constants"], g["bank"]
    gp, tr, ph = g["gaps"], g["transport"], g["phases"]
    ex, ep = g["examples"], g["exponents"]
    ar, led, tc = g["artifacts"], g["ledger"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The correction bank, in integers.** `A_n = 2^K_n Y_n / 3^n` and the "
        "claimed increment is `2^K_{n+1} Y_{n+1} - 3 * 2^K_n Y_n = 2^K_n`, "
        "with no `beta` and no bracket. Across %d orbits and **%d steps**: "
        "**%d** identity violations, **%d** non-monotone steps, **%d** "
        "increments differing from the claimed value. Theorem 5.1 is proved "
        "through this coordinate, so it is the one place a bracket could have "
        "hidden an error."
        % (bk["orbits"], bk["steps"], bk["bank_identity_violations"],
           bk["bank_not_strictly_increasing"],
           bk["bank_increment_not_the_claimed_value"]),
        "",
        "**Consecutive-record gaps.** %d orbit windows gave **%d** gaps with "
        "`g >= 2` (longest %d). Lemma 4.1 **%d** violations; Theorem 4.2's "
        "ratio cap **%d**; `q_{s+1}=1` **%d**; `x = (3y+1)/2` **%d**; record "
        "values non-increasing **%d**; Theorem 5.1 **%d**; Corollary 5.2 on "
        "**%d** tail suffixes **%d**; Theorem 6.1's exact identity — written "
        "as `z 2^Q = x 3^h P` so no `beta` decides it — **%d**; the tail "
        "excess non-positive **%d**; the net record motion not below "
        "`beta-1` **%d**; the value-peak span `M >= z+3g-4` **%d**."
        % (gp["orbits"], gp["gaps_with_g_at_least_two"], gp["largest_gap_seen"],
           gp["lemma_4_1_violations"], gp["theorem_4_2_ratio_cap_violations"],
           gp["first_step_valuation_not_one"],
           gp["x_not_three_y_plus_one_over_two"],
           gp["record_values_not_increasing"], gp["theorem_5_1_violations"],
           gp["corollary_5_2_suffixes_checked"], gp["corollary_5_2_violations"],
           gp["theorem_6_1_identity_violations"], gp["tail_excess_not_positive"],
           gp["net_record_slack_not_below_beta_minus_one"],
           gp["value_peak_span_violations"]),
        "",
        "**Bidirectional transport.** Theorem 8.1's ascent bound was checked "
        "on **%d** gaps: **%d** violations, tightest slack **%s** — attained, "
        "so it cannot be passed by accident. The peak never fell at an "
        "endpoint (**%d**) and was always the interior maximum (**%d** "
        "failures). Theorem 8.2 is labelled an identity and is one, so its two "
        "components were checked separately (**%d**, **%d**); the derived "
        "`N_{>=2}` count bound, which is a genuine claim, was exercised on "
        "**%d** descents with **%d** violations."
        % (tr["ascent_theorem_8_1_checked"],
           tr["ascent_theorem_8_1_violations"],
           tr["tightest_ascent_slack"]["slack"], tr["peaks_at_an_endpoint"],
           tr["peak_is_not_the_interior_maximum"],
           tr["descent_valuation_sum_identity_violations"],
           tr["descent_slack_identity_violations"],
           tr["descent_count_bound_checked"],
           tr["descent_count_bound_violations"]),
        "",
        "**The landing phases.** Across **%d** gaps there were **%d** "
        "`7 mod 12` endpoints and **%d** `11 mod 12` endpoints, and none "
        "outside those classes (**%d**). No landing valuation equalled one "
        "(**%d**). The parity rule failed **%d** times for phase 7 and **%d** "
        "for phase 11; the toll fell below its floor **%d** times; the mod-3 "
        "lemma `z = 2^{-q} mod 3` disagreed **%d** times; and the source "
        "phases `11, 17 mod 18` failed **%d** times, with **%d** sources "
        "outside `7, 11 mod 12`."
        % (ph["gaps"], ph["phase7_endpoints"], ph["phase11_endpoints"],
           ph["endpoint_outside_7_or_11_mod_12"],
           ph["landing_valuation_equal_to_one"],
           ph["phase7_valuation_not_even_at_least_two"],
           ph["phase11_valuation_not_odd_at_least_three"],
           ph["landing_toll_below_its_floor"],
           ph["endpoint_mod_three_disagreeing_with_two_to_the_minus_q"],
           ph["source_phase_not_matching_11_or_17_mod_18"],
           ph["source_outside_7_or_11_mod_12"]),
        "",
        "**The two bridges NO-GO 13.7 ships, rebuilt from the map.** %d "
        "examples: **%d** disagreeing values of `x`, **%d** of `z`, **%d** "
        "exponent words, **%d** first steps not of valuation one, **%d** "
        "geometry violations, **%d** tails not suffix-supercritical, **%d** "
        "landing-phase violations."
        % (ex["examples"], ex["x_disagreeing"], ex["z_disagreeing"],
           ex["exponent_word_disagreeing"], ex["first_step_not_valuation_one"],
           ex["geometry_violations"], ex["tail_not_suffix_supercritical"],
           ex["landing_phase_violations"]),
        "",
        "| `y` | `x` | `z` | word | `y mod 12` | `x mod 18` | `z mod 12` | `q_t` |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in ex["rows"]:
        out.append("| %d | %d | %d | `%s` | %d | %d | %d | %d |"
                   % (r["y"], r["x"], r["z"], r["word"], r["y_mod_12"],
                      r["x_mod_18"], r["z_mod_12"], r["q_t"]))
    out += [
        "",
        "**Section 10's pigeonhole**, which is the part of that section with "
        "content: **%d** violations over %d constructed partitions. There is "
        "deliberately no exponent check beside it — `R <= N^(4/5)` forcing "
        "`N/R >= N^(1/5)` is `N^4 >= R^5` written twice."
        % (ep["pigeonhole_violations"], ep["pigeonhole_points"]),
        "",
        "**Constants.** %d checked: **%d** disagree with both readings of "
        "their own formula, %d are the nearest double, %d are what the same "
        "formula gives in float64, %d brackets could not decide. The two "
        "landing tolls differ by exactly one in float64 (%d)."
        % (cs["constants_checked"], cs["disagreeing_with_both_evaluations"],
           cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["undecided_brackets"],
           cs["the_two_tolls_differ_by_exactly_one"]),
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
        "file with no digest anywhere is `%s`. Two files carry the same bytes "
        "under different names: %s. The source-validation record names **%d** "
        "files and digests **%d** of them (%d mismatches), reports "
        "`validation_passed = %s` with %d checks and **%d** not true, and "
        "leaves %d files unnamed: %s."
        % (ar["files_present"], ar["digests_listed"], ar["digest_mismatches"],
           ar["checksum_lines_naming_a_missing_file"],
           ", ".join(ar["files_with_no_digest_anywhere"]),
           json.dumps(ar["duplicate_file_pairs"]),
           ar["validation_per_file_entries"],
           ar["validation_entries_with_a_digest"],
           ar["validation_digest_mismatches"], ar["validation_passed_flag"],
           ar["validation_check_entries"], ar["validation_checks_not_true"],
           len(ar["files_absent_from_the_validation_record"]),
           ", ".join("`%s`" % n
                     for n in ar["files_absent_from_the_validation_record"])),
        "",
        "**Ledger coverage.** The paper lists %d proved items, %d open "
        "problems and %d NO-GO headings; the ledger carries %d, %d and %d, "
        "with an `open` key (%s). Open items with no trace: %s. NO-GO headings "
        "with no trace: %s. The heuristic deciding those lists has controls at "
        "both ends and failed neither (%d, %d)."
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
        "**Their counters beside mine**, keyed on their names rather than "
        "mine: %d of %d had no counterpart here, and %d are reported as zero."
        % (tc["checks_i_did_not_reproduce"], len(tc["rows"]),
           tc["checks_they_report_as_zero"]),
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
        print(json.dumps({"tool": "src63_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src63_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
