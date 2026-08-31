"""Emit RUN-047's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src66_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src66-au2d19.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src66-drill.json"
REPORT = ROOT / "reports" / "RUN-047-HARD-ZETA-AU2D19-CARRY-CONJUGACY.md"
FIGURES = ROOT / "data" / "gate-logs" / "src66-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src66_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    ca, ne, tw = g["carry"], g["neutrality"], g["tower"]
    al, me, ex = g["aliasing"], g["mesoscopic"], g["examples"]
    af, led, tc = g["artifacts"], g["ledger"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The two artifacts disagree on `beta`.** %d of %d numeric constants "
        "differ between the frontier and the checker report. The frontier's "
        "values match **neither** the nearest double nor the float64 chain "
        "(%d of them), while the report's are %d exact and %d the chain. This "
        "is a finding about the artifact, recorded here rather than counted as "
        "a gate failure — the same line RUN-032 drew for artifact coverage."
        % (cs["frontier_and_report_disagreeing"], cs["constants_checked"],
           cs["frontier_constants_matching_no_evaluation"],
           cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"]),
        "",
        "| constant | frontier | report | gap | frontier verdict | report verdict |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in cs["rows"]:
        out.append("| `%s` | %s | %s | %s ulp | %s | %s |"
                   % (row["constant"], row["frontier"], row["report"],
                      row.get("frontier_minus_report_ulps", "—"),
                      row["frontier_verdict"], row.get("report_verdict", "—")))
    out += [
        "",
        "**The population.** **%d** bridges from **%d** distinct sources "
        "(longest tail %d), of which **%d** have zero total lift and **%d** "
        "do not — the third round running in which the positive-lift branch "
        "has no finite instance."
        % (pop["bridges"], pop["sources"], pop["longest_tail"],
           pop["zero_lift"], pop["positive_lift"]),
        "",
        "**The carry conjugacy, exactly.** `W_l = 3^l V_l / 2^{Q_l}` on **%d** "
        "bridges, **%d** steps, **%d** positions. The definition **%d** "
        "violations; `W_0 = Z` **%d**; `W_h = 2^{-eps_h} X` **%d**; Theorem "
        "3.1's `W_{l+1} = W_l - 3^l/2^{Q_{l+1}}` **%d**; strict decrease "
        "**%d**; the iterated form `W_l = Z - sum_j 3^{j-1}/2^{Q_j}` **%d**. "
        "Theorem 4.1's band `Z/2 < W_l <= Z` **%d**, and Corollary 4.2's "
        "dyadic window **%d**, with the identity `V_l = 2^{m_l+eps_l} W_l` "
        "they both rest on **%d**. Largest interior lift **%d**."
        % (ca["bridges"], ca["steps"], ca["positions"],
           ca["carry_definition_violations"],
           ca["carry_start_not_the_endpoint"],
           ca["carry_end_not_the_phased_source"],
           ca["carry_recurrence_theorem_3_1_violations"],
           ca["carry_not_strictly_decreasing"],
           ca["iterated_carry_form_violations"],
           ca["carry_band_theorem_4_1_violations"],
           ca["dyadic_window_corollary_4_2_violations"],
           ca["state_is_not_the_phased_carry"], ca["largest_lift_seen"]),
        "",
        "**The band is loose and the sharper window is attained at both "
        "ends.** The smallest `W_h/Z` seen is **%.6f**, so the `Z/2` floor of "
        "Theorem 4.1 is nowhere near approached. Section 4's sharper form is "
        "written `2^{m+eps-eps_h} X <= V_l < 2^{m+eps} Z`: the lower end is "
        "attained **%d** times and the upper end **%d** times, once per bridge "
        "each — at `l = h` and at `l = 0`, where `V_0 = Z` exactly. So the "
        "strict `<` on the right is wrong at one endpoint. Violations: **%d** "
        "below and **%d** above. Corollary 4.2's phase-free version, which is "
        "what the bundle checks, is strict at both ends and clean."
        % (ca["smallest_carry_over_z"], ca["sharper_window_lower_attained"],
           ca["sharper_window_upper_attained"],
           ca["sharper_window_lower_violations"],
           ca["sharper_window_upper_violations"]),
        "",
        "**Mechanical neutrality.** Over **%d** intervals: the band "
        "`2^{ceil(beta s)-ceil(beta r)}/3^{s-r}` outside `(1/2,2)` **%d** "
        "times, and the phase form `2^{eps_s}/2^{eps_r}` disagreeing **%d** "
        "on **%d** sampled intervals. The alphabet itself, checked over the "
        "whole range rather than on the sampled intervals: **%d** symbols "
        "outside `{1,2}` and **%d** consecutive mechanical ones — the first is "
        "`beta in (1,2)`, the second `beta > 3/2`, and the band tests neither. "
        "The telescoping cross-check failed **%d** times. Widest ratio seen "
        "**%.6f**, narrowest **%.6f**."
        % (ne["intervals"], ne["band_violations"],
           ne["phase_form_violations"], ne["telescoping_checks"],
           ne["mechanical_symbol_outside_one_or_two"],
           ne["two_consecutive_mechanical_ones"],
           ne["telescoping_violations"], ne["widest_ratio_seen"],
           ne["narrowest_ratio_seen"]),
        "",
        "**The nested endpoint tower.** On **%d** bridges and **%d** levels: "
        "Theorem 6.1's congruence `Z = sum_j 3^{j-1} 2^{-Q_j} mod 3^l` **%d** "
        "violations, and its Archimedean counterpart "
        "`Z - sum_j 3^{j-1}/2^{Q_j} = 3^l V_l / 2^{Q_l}` **%d** — two "
        "completions of one identity, so both are checked. Theorem 7.1's "
        "stabilization is guarded by `3^l > Z`, which opens on **%d** of the "
        "levels (%s); it failed **%d** times there, and at the **%d** levels "
        "below the stabilization depth the representative disagreed with "
        "`Z mod 3^l` **%d** times. `k_0` disagreed with the least power **%d** "
        "times; the largest seen is **%d**."
        % (tw["bridges"], tw["levels"],
           tw["congruence_theorem_6_1_violations"],
           tw["archimedean_carry_form_violations"],
           tw["stabilization_levels"],
           pct(tw["stabilization_levels"], tw["levels"]),
           tw["stabilization_theorem_7_1_violations"],
           tw["levels_below_the_stabilization_depth"],
           tw["representative_at_a_shallow_level_not_z_mod_three_to_the_l"],
           tw["k0_disagreeing_with_the_least_power"], tw["largest_k0_seen"]),
        "",
        "**Valuation aliasing.** **%d** precisions, **%d** samples. The order "
        "of 2 modulo `3^{k+1}` failed to be `2*3^k` **%d** times; the reverse "
        "predecessor was non-integral **%d** times — checked by exact "
        "divisibility, where the bundle uses floor division and arranges the "
        "parity so it never has to; Theorem 8.1's "
        "`R_{q+2*3^k}(V) = R_q(V) mod 3^k` **%d** violations. Two sharpness "
        "counters: aliasing at a THIRD of the period **%d** times, and "
        "aliasing one level deeper than claimed **%d** — the period is the "
        "sharp one for that precision, in both directions."
        % (al["levels"], al["samples"], al["order_violations"],
           al["predecessor_not_integral"],
           al["aliasing_theorem_8_1_violations"],
           al["aliasing_at_a_shorter_period"],
           al["aliasing_holds_one_level_deeper"]),
        "",
        "**Their mesoscopic block asserts the definition of a ceiling.** "
        "`kcrit = ceil(log_3 target)`, then `3^kcrit >= target`, "
        "`3^{kcrit-1} < target` and `3^{kcrit-2} < target` — the first two are "
        "what a ceiling means and the third follows from the second. Over "
        "**%d** samples at their ranges: **%d** violations of the definition "
        "and **%d** cases where the third did not follow from the second. All "
        "three are computed in float64, so the only way any could fail is a "
        "rounding across an integer; the closest `log_3(target)` came to one "
        "is **%.3e**, against a double's error near `1e-15` — a margin of "
        "**%.1f billion**, and **%d** samples could have failed."
        % (me["samples"], me["ceiling_definition_violations"],
           me["third_assertion_not_implied_by_the_second"],
           me["closest_log_to_an_integer"],
           (me["smallest_margin_ratio"] or 0) / 1e9,
           me["samples_that_could_have_failed"]),
        "",
        "**All ten published examples, rebuilt from the map.** **%d** "
        "disagreeing `X`, **%d** `Z`, **%d** exponent words, **%d** lengths, "
        "**%d** maximum lifts, **%d** stabilization depths, **%d** final "
        "carries — compared as exact rationals, not as floats. **%d** source "
        "appears more than once."
        % (ex["x_disagreeing"], ex["z_disagreeing"],
           ex["exponent_word_disagreeing"], ex["h_disagreeing"],
           ex["max_lift_disagreeing"], ex["stabilization_depth_disagreeing"],
           ex["carry_final_disagreeing"],
           ex["sources_appearing_more_than_once"]),
        "",
        "| `y` | `X` | `Z` | `h` | word | lift profile | `k_0` | `W_h` | `W_h/Z` |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in ex["rows"]:
        out.append("| %d | %d | %d | %d | `%s` | `%s` | %d | `%s` | %.6f |"
                   % (row["y"], row["X"], row["Z"], row["h"], row["word"],
                      row["lift_profile"], row["k0"], row["carry_final"],
                      row["carry_over_z"]))
    out += [
        "",
        "**Artifacts.** %d files, %d carrying a `CHECKSUMS` digest, **%d** "
        "mismatches, **%d** manifest lines naming a missing file; the only "
        "file with no digest anywhere is %s. The source-validation record "
        "names **%d** files and digests **%d** of them — none — reporting "
        "`all_ok = %s`, `checker_rerun = %s`, `python_compile.ok = %s`, with "
        "**%d** markdown `ok` flags and **%d** json `parse_ok` flags not true. "
        "%d files are absent from it: %s."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "none",
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           af["validation_all_ok_flag"], af["validation_checker_rerun"],
           af["validation_python_compile_ok"],
           af["validation_file_ok_flags_not_true"],
           af["validation_json_parse_not_true"],
           len(af["files_absent_from_the_validation_record"]),
           ", ".join("`%s`" % n
                     for n in af["files_absent_from_the_validation_record"])),
        "",
        "**Ledger coverage.** The paper lists %d proved items, %d open "
        "problems and %d NO-GO headings; the ledger carries %d, %d and %d, "
        "with an `open` key (%s). Open items with no trace: %s. NO-GO "
        "headings with no trace: %s — the ledger merges nine headings into "
        "six entries rather than dropping any. The heuristic deciding those "
        "lists has controls at both ends and failed neither (%d, %d)."
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
        print(json.dumps({"tool": "src66_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src66_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
