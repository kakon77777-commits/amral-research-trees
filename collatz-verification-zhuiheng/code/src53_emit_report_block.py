"""Emit RUN-035's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src53_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src53-au2d7.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src53-drill.json"
REPORT = ROOT / "reports" / "RUN-035-HARD-ZETA-AU2D7-PLATEAU-RESET.md"
FIGURES = ROOT / "data" / "gate-logs" / "src53-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src53_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    sq, ori, pre = g["slope_quantization"], g["orientation"], g["premises"]
    der, cs, led = g["derivations"], g["constants"], g["ledger"]
    ar, tc, ex = g["artifacts"], g["their_claims"], g["shipped_examples"]
    inline = cs["inline_decimals_in_the_paper"]

    out = [
        BEGIN, "",
        "**Section 3, on real orbits.** Every row below is decided in exact "
        "rational arithmetic; `beta` cancels out of the jump law, so no "
        "logarithm is evaluated anywhere in this table.",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("active nested chains built from %d orbits" % sq["orbits"],
         "deepest `r` = %d, longest `L` = %d" % (sq["max_depth"], sq["max_L"]),
         sq["chains"]),
        ("renewal edges across them",
         "%d plateau, %d strict, of which %d have determinant one"
         % (sq["plateau_edges"], sq["strict_edges"], sq["unit_strict_edges"]),
         sq["edges"]),
        ("…**violations of the jump law** `xi_{i+1}−xi_i = J_i/(L_iL_{i+1})`",
         "exact Fractions, must be zero", sq["jump_law_violations"]),
        ("…`J_i ≠ 0` failing the `1/(L_iL_{i+1})` quantization",
         "%d edges have `J_i = 0`" % sq["J_zero_edges"],
         sq["quantization_violations"]),
        ("…falling below the coarser `1/L²`", "the bound section 9 uses",
         sq["quantization_below_one_over_L_squared"]),
        ("**genuine resets**, `J_i < 0`",
         "of which %d have determinant one" % sq["unit_resets"],
         sq["genuine_resets_J_negative"]),
        ("…**Theorem 4.4 violations** `E_i − A_i > 1/L_{i+1}`",
         "decided as `2^N` against `3^D`, not as a bracket",
         sq["theorem_4_4_violations"]),
        ("plateau edges where `J_i ≠ Π_i` / `Π_i < 1` / the two forms disagree",
         "`Π_i = Q_{i+1}g_i − p_iL_{i+1} = g_iD_{i+1} + L_{i+1}A_i`",
         "%d / %d / %d" % (sq["plateau_J_not_equal_to_Pi"],
                           sq["plateau_determinant_below_one"],
                           sq["plateau_Pi_two_forms_disagree"])),
        ("strict edges where `Δ_i < 1` / the two forms disagree / `J_i` misfits",
         "`Δ_i = r_ig_i − p_ih_i = g_iE_i + h_iA_i`",
         "%d / %d / %d" % (sq["strict_determinant_below_one"],
                           sq["strict_Delta_two_forms_disagree"],
                           sq["strict_J_formula_violations"])),
        ("renewal identity `A_i + D_i = D_{i+1} + E_i` failing",
         "as a beta-linear pair, must be the pair `(0,0)`",
         sq["renewal_identity_violations"]),
        ("`A_i`, `D_i`, `E_i` not positive / endpoints not nested",
         "sign decided exactly by `3^c 2^k` against 1",
         "%d / %d" % (sq["A_not_positive"] + sq["D_not_positive"]
                      + sq["E_not_positive"],
                      sq["endpoints_not_nested_h_negative"])),
        ("**Lemma 5.1** chains where `Σ g_iL_{i+1} ≥ L²/2`",
         "checked on all %d chains" % sq["lemma_5_1_chains_checked"],
         sq["lemma_5_1_violations"]),
        ("**§11** unit strict edges, all with `p_i/g_i < β < r_i/h_i`",
         "the annulus premise, tested not assumed: %d fail"
         % ori["annulus_premise_fails"], ori["annulus_premise_holds"]),
        ("…with the mediant below `β`, where `J_i > 0` must hold",
         "%d counterexamples" % ori["mediant_below_beta_with_J_not_positive"],
         ori["mediant_below_beta"]),
        ("…**unit resets** failing child-slope / mediant / denominator `≥ 2g+h`",
         "of %d unit resets" % ori["unit_resets"],
         "%d / %d / %d" % (ori["reset_child_slope_not_between_beta_and_mediant"],
                           ori["reset_mediant_not_above_beta"],
                           ori["child_denominator_below_2g_plus_h"])),
        ("…Farey-neighbour identity `(p+r)g − p(g+h) = 1` failing",
         "an integer identity, not an estimate",
         ori["farey_neighbour_identity_violations"]),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**The premises sections 4.3 to 9 stand on.** These are B-survival "
        "properties. A real orbit does not owe them, and the point of measuring "
        "is that the caps cannot be tested where they are absent.",
        "",
        "| premise | of | met |",
        "| --- | --- | --- |",
    ]
    prem = [
        ("overshoot `D_i/L_i < 1/(3y_i ln2)`",
         "%d nested intervals" % pre["intervals"], pre["survival_bound_holds"]),
        ("…chains where **every** interval meets it",
         "%d chains" % pre["chains"], pre["chains_where_every_interval_survives"]),
        ("origin-slack budget `H < B(L,y₁)`",
         "%d chains" % pre["chains"],
         pre["chains_meeting_the_origin_slack_budget_H_lt_B"]),
        ("endpoint budget `Σ E_i < 2B`", "%d chains" % pre["chains"],
         pre["chains_meeting_the_endpoint_budget_sumE_lt_2B"]),
        ("**every premise at once**", "%d chains" % pre["chains"],
         pre["chains_meeting_every_premise"]),
    ]
    for what, of, met in prem:
        out.append("| %s | %s | `%s` |" % (what, of, met))
    out += [
        "",
        "So Theorems 4.3, 5.4 and 6.1 were applied to **%d** chain%s and held "
        "there — a denominator that settles nothing, and is reported rather than "
        "dressed up. `U_β(L) ≤ L/3` was verified exactly on every chain "
        "(`%d` violations)."
        % (pre["chains_meeting_every_premise"],
           "" if pre["chains_meeting_every_premise"] == 1 else "s",
           pre["u_beta_above_L_over_3"]),
        "",
        "Section 9's hypothesis is attainable and common — **%d** of %d chains "
        "satisfy `y₁ > L²/(3 ln2)`. Its conclusions do not follow on them: "
        "`%d` have all crossing slopes equal, `%d` have no plateau, `%d` have "
        "`r ≤ 4` (deepest seen: `%d`). That is not a counterexample. Theorem "
        "9.2 also needs the survival slope bound `ξ_i < 1/L²`, which **%d** of "
        "those %d chains satisfy, and section 1 declares it. The separation "
        "half of Lemma 9.1 is pure arithmetic and does hold: of %d chains with "
        "more than one slope, `%d` have two distinct `Q_i/L_i` closer than "
        "`1/L²`."
        % (pre["high_source_chains"], pre["chains"],
           pre["high_source_all_slopes_equal"], pre["high_source_without_plateaus"],
           pre["high_source_depth_at_most_4"], pre["high_source_max_depth"],
           pre["high_source_with_the_survival_slope_bound"],
           pre["high_source_chains"], pre["chains_with_more_than_one_slope"],
           pre["distinct_slopes_closer_than_one_over_L_squared"]),
        "",
        "**The derivations, which are arithmetic and can be checked.** Over "
        "`%d` grid points in `(L, y₁, r)`:" % der["grid_points"],
        "",
        "| derivation | violations |",
        "| --- | --- |",
    ]
    for what, key in (
        ("`B(L,y₁) < L/(3y₁ln2)`, from `log₂(1+x) < x/ln2` and `U_β(L) ≤ L/3`",
         "B_below_L_over_3_y1_ln2_violations"),
        ("Corollary 6.2 is implied by Theorem 6.1", "cor_6_2_not_implied_by_thm_6_1"),
        ("`X_r` is the positive root of `ax² + bx = r−1`",
         "X_r_not_a_root_of_a_x2_plus_b_x"),
        ("Theorem 7.1's inversion `y₁ < L²/X_r²`", "thm_7_1_inversion_violations"),
        ("Corollary 7.2 for `r ≥ 9`", "cor_7_2_not_implied"),
        ("Corollary 9.3's `B < 1/L`", "cor_9_3_B_below_one_over_L_violations"),
        ("Theorem 9.4's `(2+√2)√(LB) < 4`", "thm_9_4_depth_bound_violations"),
    ):
        out.append("| %s | `%d` |" % (what, der[key]))
    out += [
        "",
        "Corollary 7.2's threshold `2b²/a` is **algebraic**: the `ln 2` in `a` "
        "cancels the one inside `b²`, leaving `(12+8√2)/3 = %s…`, which is "
        "below 8: `%s`. The round prints it as `%s`."
        % (der["two_b_squared_over_a_is_algebraic"],
           der["two_b_squared_over_a_below_8"],
           inline.get("(12+8 sqrt2)/3", {}).get("published", "?")),
        "",
        "**The theorem ledger, a new artifact this round, against the paper's "
        "own section 22.**",
        "",
        "| the paper says | the JSON ledger says |",
        "| --- | --- |",
        "| §22.1 lists `%d` internally proved results | `internal_theorems` has "
        "`%d` — **%d fewer** |" % (led["paper_section_22_1_numbered_results"],
                                   led["ledger_internal_theorems"],
                                   led["internal_shortfall_against_the_paper_s_own_list"]),
        "| §18 carries `%d` `NO-GO` headings | `no_go` has `%d` — **%d fewer** |"
        % (led["paper_no_go_headings"], led["ledger_no_go_entries"],
           led["no_go_shortfall"]),
        "| §22.2 lists `%d` inherited rounds | `%d`, all `%d` named and present "
        "in the paper |" % (led["paper_section_22_2_inherited"],
                            led["ledger_inherited"],
                            led["inherited_rounds_named_and_present_in_the_paper"]),
        "| §22.3 lists `%d` external inputs | `%d`, arXiv ids absent from the "
        "paper: `%d` |" % (led["paper_section_22_3_external"], led["ledger_external"],
                           len(led["external_sources_whose_arxiv_id_is_absent_from_the_paper"])),
        "| §22.4 lists `%d` context-only source | `%d` |"
        % (led["paper_section_22_4_context"], led["ledger_context_only"]),
        "",
        "The one `NO-GO` with no ledger entry sharing any of its keywords is "
        "**%s**. Round name agrees across ledger, frontier and checker report: "
        "`%s`; next round agrees: `%s`; **status does not**: the ledger says "
        "`%s`, the frontier says `%s`."
        % ("; ".join(led["paper_no_go_titles_with_no_ledger_entry_sharing_a_keyword"])
           or "none",
           led["round_agrees_across_ledger_frontier_and_report"],
           led["next_round_agrees_between_ledger_and_frontier"],
           led["ledger_status"], led["frontier_status"]),
        "",
        "**Constants, against brackets certified in this file** — `ln 2` from "
        "`Σ 1/(k2^k)` with its exact tail, `log₂3` from `(3^q).bit_length()`, "
        "`√2` from integer square roots. No floating-point reference is "
        "consulted. `1/ln2` to 20 places: `%s`."
        % g["instrument"]["one_over_ln2_to_20_places"],
        "",
        "| constant | published | ulps from the nearest double |",
        "| --- | --- | --- |",
    ]
    for name, row in cs["rows"].items():
        out.append("| `%s` | `%s` | `%d` |"
                   % (name, row["published"], row["ulps_from_the_nearest_double"]))
    out += [
        "",
        "| the paper prints | verdict |",
        "| --- | --- |",
    ]
    for name, row in inline.items():
        out.append("| `%s` = `%s…` | %s |" % (name, row["published"], row["verdict"]))
    out += [
        "",
        "The frontier and the paper **disagree** on `1/(3 ln2)`: `%s`. The "
        "paper's `%s` is the correctly rounded double; the frontier's `%s` is "
        "one ulp away. The other `%d` frontier constants are exact, the two "
        "inherited powers still sum to one (`%s`), and `2/ln2` is exactly twice "
        "`1/ln2` as doubles (`%s`)."
        % (cs["the_paper_and_the_frontier_agree_on_1_over_3ln2"],
           inline.get("1/(3 ln2)", {}).get("published", "?"),
           cs["rows"]["high_source_threshold_coefficient_1_over_3ln2"]["published"],
           len(cs["rows"]) - len(cs["off_by_at_least_one_ulp"]),
           cs["the_two_inherited_powers_sum_to_one"],
           cs["2_over_ln2_is_exactly_twice_1_over_ln2"]),
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    tail = [
        ("shipped unit-reset examples recomputed",
         "%d clauses each; %d failing" % (ex["clauses_per_example"],
                                          len(ex["examples_failing_a_clause"])),
         ex["distinct_examples"]),
        ("validation-record files verified",
         "shape: %s; uncovered: %d" % (ar["validation_record_shape"],
                                       len(ar["present_but_not_covered"])),
         ar["verified"]),
        ("the checker's stated claims independently confirmed",
         "of %d under the key `%s`; %d named as not covered here"
         % (tc["claims_the_checker_states"], tc["the_key_the_report_uses"],
            len(tc["not_covered_by_this_run"])),
         tc["independently_confirmed"]),
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
        "**The two transcripts.** `checker_stdout.txt` is byte-identical to the "
        "checker report: `%s` (both `%d` bytes)."
        % (ar["report_and_stdout_byte_identical"], ar["report_bytes"]),
        "",
        "**Not covered here**, named rather than implied: "
        + "; ".join("*%s*" % c for c in tc["not_covered_by_this_run"]) + ".",
        "",
        "Every figure above is emitted by `code/src53_emit_report_block.py` from "
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
        print(json.dumps({"tool": "src53_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src53_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
