"""Emit RUN-038's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src57_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src57-au2d10.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src57-drill.json"
REPORT = ROOT / "reports" / "RUN-038-HARD-ZETA-AU2D10-VALUATION-HARMONIC-DEFICIT.md"
FIGURES = ROOT / "data" / "gate-logs" / "src57-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src57_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    rf, cap, pr = g["reciprocal_flow"], g["capacities"], g["product"]
    ex, m9, cm = g["exponents"], g["mod9"], g["countermodel"]
    cs, led, ar = g["constants"], g["ledger"], g["artifacts"]
    tc = g["their_claims"]

    out = [
        BEGIN, "",
        "**The reciprocal flow, exactly.** Theorem 3.1 is an identity between "
        "rationals and Corollary 3.2 telescopes it; neither needs a hypothesis.",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("accelerated edges from %d orbits" % rf["orbits"], "Theorem 3.1",
         rf["edges"]),
        ("…**violations of the identity**",
         "`1/Y_j − 1/Y_{j+1} = (3−2^q)/(3Y_j) + 1/(3Y_jY_{j+1})`",
         rf["identity_violations"]),
        ("first-crossing segments", "longest `L` = %d" % rf["max_L"],
         rf["segments"]),
        ("…**violations of the telescope**",
         "`Σ(2^q−3)/Y_j = −3/y + 3/z + C_cross`", rf["telescope_violations"]),
        ("…where the balance is not equivalent to `z > y`",
         "Theorem 4.1 IS the telescope plus that premise",
         rf["the_balance_is_not_equivalent_to_the_endpoint_premise"]),
        ("…**meeting `z > y`**, the premise Theorem 4.1 needs",
         "a first-crossing endpoint is where the slack drops",
         rf["segments_meeting_the_endpoint_premise_z_above_y"]),
        ("…Theorem 4.1 applied / violated", "premise-gated",
         "%d / %d" % (rf["theorem_4_1_checked"], rf["theorem_4_1_violations"])),
        ("…**meeting Lemma 5.1's premise**",
         "every state, the endpoint included, at or above the source",
         rf["segments_where_every_state_including_the_endpoint_is_above_y"]),
        ("…cross term above `1/y² + 1/(2y)` / above `9/(14y)`",
         "premise-gated; %d segments have a source below 7"
         % rf["segments_with_a_source_below_seven"],
         "%d / %d" % (rf["cross_term_above_one_over_y_squared_plus_one_over_two_y"],
                      rf["cross_term_above_nine_over_fourteen_y"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**The harmonic capacities, which need no survival premise at all.**",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("segments checked", "longest `L` = %d" % cap["max_L"], cap["segments"]),
        ("…**violations of Theorem 6.1** `S₁ ≤ 2/y + log(1+6L/y)/6`",
         "%d segments have no `q = 1` edge at all"
         % cap["segments_with_no_q_equal_1_edge"], cap["q1_capacity_violations"]),
        ("…**violations of Theorem 6.2** `S₂ ≤ 2/y + log(1+12L/y)/12`",
         "must be zero", cap["q2_capacity_violations"]),
        ("…**violations of Theorem 7.1**",
         "`S_tot < log(1+6L/y)/5 + log(1+12L/y)/15 + 289/(70y)`",
         cap["theorem_7_1_violations"]),
        ("…where `289/70` fails to decompose",
         "`(6/5)(2) + (4/5)(2) + (1/5)(9/14)`, exactly",
         cap["the_289_over_70_constant_does_not_decompose"]),
        ("low-source segments `7 ≤ y ≤ L`",
         "of %d; Corollaries 9.1 and 9.2 live here" % pr["segments"],
         pr["low_source_segments_7_le_y_le_L"]),
        ("…**violations of Corollary 9.1** `𝒫 < C₁₀(L/y)^{4/45}`",
         "must be zero", pr["corollary_9_1_violations"]),
        ("…**violations of Theorem 9.2** `𝒫/𝒫₆ ≤ C_rel(L/y)^{−1/45}`",
         "the polynomial gain beyond the 3-sieve", pr["theorem_9_2_violations"]),
        ("…violations of the `𝒫₆ ≥ (63L/25y)^{1/9}` floor it rests on",
         "must be zero", pr["p6_lower_bound_violations"]),
        ("…admissible positions above `y + 3k + 1`",
         "the A-U.2d.9 placement this round reuses",
         pr["admissible_upper_placement_violations"]),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**The exponent, empirically.** `P_RF` is an envelope, so a real segment "
        "need only stay under it; what is checked is that the envelope's own "
        "measured exponent falls toward `4/45 = 0.0889`.",
        "",
        "| `y` | `L` | `P_RF` exponent → `4/45` | `𝒫₆` exponent → `1/9` |",
        "| --- | --- | --- | --- |",
    ]
    for r in ex["rows"]:
        out.append("| `%d` | `%d` | `%s` | `%s` |"
                   % (r["y"], r["L"], r["rf_exponent"], r["p6_exponent"]))
    out += [
        "",
        "Non-monotone steps toward `4/45`: `%d`, out to `L = %d`."
        % (ex["rf_exponent_not_approaching_four_forty_fifths"], ex["largest_L"]),
        "",
        "**The mod-9 target cost, and the span theorem whose premise real "
        "orbits meet.** As at A-U.2d.9, first-crossing subcriticality is what a "
        "first-crossing interval *is*, decidable as `2^Q < 3^m`.",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("edges checked against the mod-9 law", "`2^q·m ≡ 4 or 7 (mod 9)`",
         m9["edges"]),
        ("…**targets outside `{4,7} (mod 9)`**", "must be zero",
         m9["targets_not_4_or_7_mod_9"]),
        ("…**edges below their target cost**", "`q ≥ c(m mod 9)`",
         m9["edges_below_their_target_cost"]),
        ("cost-table entries rederived from the valuation arithmetic",
         "the table is checked, not transcribed and trusted",
         m9["cost_table_entries_checked"]),
        ("…disagreeing with it", "must be zero",
         m9["cost_table_entries_disagreeing_with_the_valuation_arithmetic"]),
        ("capacity windows enumerated", "`N_c ≤ W/9 + 2`", m9["capacity_windows"]),
        ("…exceeding that capacity", "must be zero",
         m9["windows_where_a_cost_class_exceeds_W_over_9_plus_2"]),
        ("proper prefixes examined", "longest `m` = %d" % m9["max_prefix_length"],
         m9["prefixes"]),
        ("…**meeting subcriticality** `2^Q < 3^m`", "%d fail"
         % m9["prefixes_failing_subcriticality"],
         m9["prefixes_meeting_subcriticality"]),
        ("…failing the valuation floor `Σq ≥ 3m − W/3 − 6`",
         "the step the span bound rests on", m9["valuation_floor_violations"]),
        ("…**Theorem 15.1 applied / violated**", "`W > 3(3−β)m − 18`",
         "%d / %d" % (m9["theorem_15_1_checked"], m9["theorem_15_1_violations"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**The round's own countermodel, checked against its own closed forms.** "
        "Section 16 gives `D(t) = Σ t^{k−1}/(3·2^k) = 1/(3(2−t))` and an average "
        "valuation tending to `2/(2−t)`. Eliminating `t` between them leaves a "
        "relation between the round's *reported* numbers: `avg_q → 6·|S_X|/X`.",
        "",
        "| `X` | reported count | reported `avg_q` | implied by the density | gap | `t` recovered |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in cm["rows"]:
        out.append("| `%d` | `%d` | `%.10f` | `%.6f` | `%s` | `%.6f` |"
                   % (r["X"], r["count"], r["reported_avg_q"],
                      r["implied_by_the_reported_density"], r["gap"],
                      r["t_recovered_from_the_density"]))
    out += [
        "",
        "The gap shrinks monotonically across the three sizes, which is what the "
        "`+ o(X)` in `|S_X| = D(t)X + o(X)` predicts, and the recovered `t` "
        "converges. Both series agree with their closed forms as exact "
        "rationals (`%d` and `%d` disagreements), `t_β = 2(1−1/β)` is exactly "
        "where the average reaches `β` (`%d` failures), the class densities "
        "`d_k = 1/(3·2^k)` check out on `%d` classes, and no reported average "
        "exceeds `β` (`%d`). The round's `max_rf_actual_ratio` is `%s`, at most "
        "one: `%s`."
        % (cm["density_series_disagrees_with_its_closed_form"],
           cm["average_series_disagrees_with_its_closed_form"],
           cm["t_beta_does_not_make_the_average_equal_beta"],
           cm["class_densities_checked"],
           cm["rows_where_the_average_exceeds_beta"],
           cm["their_max_rf_actual_ratio"], cm["the_ratio_is_at_most_one"]),
        "",
        "**Constants, against their closed forms.**",
        "",
        "| constant | published | closed form | ulps |",
        "| --- | --- | --- | --- |",
    ]
    for name, row in cs["rows"].items():
        out.append("| `%s` | `%s` | `%s` | `%s` |"
                   % (name, row["published"], row["closed_form"],
                      row.get("ulps", "undecided")))
    chain = cs["the_derivation_chain_in_float64"]
    out += [
        "",
        "The chain again, and this time the **root itself drifts**. Every link "
        "reproduces by redoing the arithmetic in float64 on the already-rounded "
        "parent: `C₁₀/6` gives the published `C₁₀^{(r)}` (`%s`), that raised to "
        "`−45/41` gives `c₁₀` (`%s`), the float64 `θ★` through `μ10`'s formula "
        "gives `μ10` (`%s`), and `C₁₀/(63/25)^{1/9}` gives `C_rel` (`%s`)."
        % (chain["C10_depth_is_the_published_C10_divided_by_six_as_doubles"],
           chain["c10_is_the_published_C10_depth_to_the_minus_forty_five_forty_firsts"],
           chain["mu10_is_the_float64_theta_star_put_through_its_formula"],
           chain["Crel_is_the_published_C10_over_the_float64_ninth_root"]),
        "",
        "The two artifacts disagree on `%d` constants and use `%d` different "
        "names for the same quantity (`%d` keys appear only in the checker "
        "report, `%d` only in the frontier)."
        % (len(cs["constants_the_two_artifacts_disagree_on"]),
           len(cs["constants_renamed_between_the_two_artifacts"]),
           len(cs["keys_only_in_the_checker_report"]),
           len(cs["keys_only_in_the_frontier"])),
        "",
        "A-U.2d.9's span coefficient is quoted here as %s. The correctly "
        "rounded double is `%s`; that round's own constants frontier had `%s`, "
        "so the wrong value did **not** travel forward."
        % (", ".join("`%s`" % s for s in
                     cs["the_AU2d9_constant_carried_forward"]
                     ["the_paper_quotes_AU2d9_span_as"]) or "not at all",
           cs["the_AU2d9_constant_carried_forward"]["the_correctly_rounded_double_is"],
           cs["the_AU2d9_constant_carried_forward"]["the_AU2d9_frontier_had"]),
        "",
        "| the paper prints | verdict |",
        "| --- | --- |",
    ]
    for name, row in cs["inline_decimals_in_the_paper"].items():
        out.append("| `%s` = `%s…` | %s |" % (name, row["published"],
                                              row["verdict"]))

    out += [
        "",
        "**The ledger against the paper's own section 22, and the manifests.**",
        "",
        "| the paper says | the JSON ledger says | shortfall |",
        "| --- | --- | --- |",
    ]
    for row in led["table"]:
        out.append("| §%s: `%d` | `%s`: `%d` | `%d` |"
                   % (row["paper_section"], row["paper_items"],
                      row["ledger_key"], row["ledger_items"], row["shortfall"]))
    out += [
        "",
        "The paper carries `%d` `NO-GO` headings (`%s`) against the ledger's "
        "`%d`; titles with no ledger entry sharing a distinctive word: %s."
        % (led["paper_no_go_headings"],
           ", ".join(led["no_go_headings_in_the_paper"]),
           led["ledger_no_go_entries"],
           "; ".join("*%s*" % s for s in
                     led["paper_no_go_titles_with_no_ledger_entry_sharing_a_keyword"])
           or "none"),
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    tail = [
        ("files in the bundle",
         "`CHECKSUMS.sha256` lists %d, the validation record %d"
         % (ar["listed_in_CHECKSUMS"], ar["listed_in_the_validation_record"]),
         ar["files_in_the_bundle"]),
        ("…digests that do not reproduce, in either manifest", "must be zero",
         len(ar["CHECKSUMS_mismatches"]) + len(ar["validation_record_mismatches"])),
        ("…where the two manifests disagree", "on the files both list",
         len(ar["digests_disagreeing_between_the_two_manifests"])),
        ("…files covered by neither",
         ", ".join(ar["covered_by_neither_manifest"]) or "none",
         len(ar["covered_by_neither_manifest"])),
        ("validation-record shape", ar["validation_record_shape"], "—"),
        ("the checker's named checks independently confirmed",
         "of %d; %d named as not covered here"
         % (tc["checks_the_report_names"], len(tc["not_covered_by_this_run"])),
         tc["independently_confirmed"]),
        ("this run's own bracket self-checks",
         "%d failed" % len(g["instrument_selfcheck"]["failed"]),
         g["instrument_selfcheck"]["checks"]),
        ("defects planted / caught by the check named for each",
         "%d robustness property; %d malformed; %d controls, %d undisturbed"
         % (d["counts"]["robustness_properties"], d["counts"]["malformed"],
            d["counts"]["controls"], d["counts"]["controls_undisturbed"]),
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in tail:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**Not covered here**, named rather than implied: "
        + "; ".join("*%s*" % c for c in tc["not_covered_by_this_run"]) + ".",
        "",
        "Every figure above is emitted by `code/src57_emit_report_block.py` from "
        "the gate logs. None is typed into this file.",
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
            print(json.dumps({"error": "missing log", "path": str(path)}, indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    if not g.get("passed"):
        print(json.dumps({"error": "the recheck is red",
                          "failures": g.get("failures"),
                          "guards": g.get("non_vacuity_guards")},
                         indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red", "counts": d.get("counts")},
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
        print(json.dumps({"tool": "src57_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src57_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
