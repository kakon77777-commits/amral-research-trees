"""Emit RUN-046's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src65_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src65-au2d18.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src65-drill.json"
REPORT = ROOT / "reports" / "RUN-046-HARD-ZETA-AU2D18-LIFT-COCYCLE.md"
FIGURES = ROOT / "data" / "gate-logs" / "src65-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src65_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, ce, cs = g["instrument"], g["ceiling"], g["constants"]
    lf, bu, co = g["lift"], g["budget"], g["cocycle"]
    zl, ab, ta = g["zero_lift"], g["abstract"], g["their_algebra"]
    fs, ex, cm = g["first_spike"], g["examples"], g["countermodels"]
    cl, af, led, tc = (g["collapse"], g["artifacts"], g["ledger"],
                       g["their_claims"])

    out = [
        BEGIN, "",
        "**The exact ceiling, and whether their float64 one is safe.** "
        "`ceil(beta l) = (3^l).bit_length()` because `beta*l` is never an "
        "integer. The shipped checker computes it as `ceil(log2(3)*l)` in "
        "float64. Over **%d** levels the two agree **%d** times out of %d "
        "(first disagreement: %s), the certified fixed-point route was "
        "undecided **%d** times and disagreed with the exact `3^l` route on "
        "**%d** of the %d levels cross-checked. The closest `beta*l` comes to "
        "an integer over that range is **%.3e**, at l = %d, against a float64 "
        "error near **%.2e** — a margin of about **%.1f million**. Their "
        "shortcut is safe at these sizes, and now that is a measurement."
        % (ce["levels"], ce["levels"] - ce["float_ceiling_disagreements"],
           ce["levels"], ce["first_disagreement"], ce["fixed_point_undecided"],
           ce["fixed_point_disagreeing_with_the_exact_route"],
           ce["exact_levels_cross_checked"], ce["closest_approach"],
           ce["closest_approach_level"], ce["float64_error_at_that_level"],
           (ce["margin_ratio"] or 0) / 1e6),
        "",
        "**The lift profile, in integers.** **%d** bridges from **%d** "
        "distinct sources (longest tail %d), **%d** profile positions. "
        "Theorem 6.1's `Z < X < (3Z+1)/2`: **%d** upper and **%d** lower "
        "violations, with `y < Z` failing **%d** times and "
        "`X = (3y+1)/2` **%d**. Theorem 7.1's `m_l >= 0`: **%d** negative, "
        "and **%d** positions where `m_l >= 0` disagreed with the suffix "
        "supercriticality it is equivalent to. The decomposition "
        "`2^{-H} = 2^{-m} 2^{-eps}`, as exact rationals: **%d**. Theorem "
        "8.1's `m_{l+1} - m_l = q_{h-l} - a_{l+1}`: **%d**. Across **%d** "
        "descents, **%d** fell by more than one and **%d** happened at a "
        "mechanical one — both impossible, and both counted rather than "
        "assumed. The total lift disagreed with `Q - ceil(beta h)` **%d** "
        "times."
        % (lf["bridges"], lf["sources"], lf["longest_tail"],
           lf["profile_positions"], lf["rank_one_upper_violations"],
           lf["rank_one_lower_violations"],
           lf["left_record_not_below_the_endpoint"],
           lf["source_not_three_y_plus_one_over_two"], lf["lift_negative"],
           lf["lift_nonnegative_disagreeing_with_supercriticality"],
           lf["slack_decomposition_violations"],
           lf["recurrence_theorem_8_1_violations"], lf["descents_seen"],
           lf["lift_descends_by_more_than_one"],
           lf["lift_descends_at_a_mechanical_one"],
           lf["total_lift_not_q_minus_ceil_beta_h"]),
        "",
        "**Every bridge has zero total lift.** **%d of %d** — the "
        "positive-lift branch of Theorem 15.1 and the rarity bound of "
        "Theorem 10.1 have **no finite instance at all** at this scale. The "
        "profile is not flat, though: the largest interior lift reached is "
        "**%d**, so the excursion structure the round is about is genuinely "
        "present. RUN-045 found the same thing on A-U.2d.17's smaller "
        "population; this is the same fact on 1228 bridges under the "
        "bundle's own wider definition."
        % (lf["zero_total_lift"], lf["bridges"], lf["largest_interior_lift"]),
        "",
        "**The Laplace budget, reindexed.** The identity is A-U.2d.17's under "
        "`i = h - l`, and RUN-045 showed that one is the definition of `B_w`, "
        "so what is checked here is the reindexing itself: term by term "
        "against the old order, **%d** violations, with the identity **%d**. "
        "Theorem 9.1's `sum 2^{-m_l} < 6Z`: **%d** violations on **%d** "
        "bridges, and the integer sum failed to sit between the real one and "
        "twice it **%d** times — the sandwich `eps in (0,1)` forces and the "
        "only place the reindexing could hide. The largest ratio to the "
        "ceiling actually seen is **%.4f**, so `6Z` is loose by a factor of "
        "about %d. The quantile bound was exercised on **%d** instances with "
        "**%d** violations, of which **%d** were non-vacuous; replacing `6Z` "
        "by the sum it bounds gives **%d** non-vacuous instances, **%d** "
        "violations."
        % (bu["reindexing_violations"], bu["laplace_identity_violations"],
           bu["budget_theorem_9_1_violations"], bu["bridges"],
           bu["budget_is_not_within_a_factor_two_of_the_identity"],
           bu["budget_over_six_z_ratio_smallest"],
           int(1 / max(bu["budget_over_six_z_ratio_smallest"], 1e-9)),
           bu["quantile_instances"], bu["quantile_violations"],
           bu["quantile_instances_that_are_not_vacuous"],
           bu["sharp_quantile_instances_that_are_not_vacuous"],
           bu["sharp_quantile_violations"]),
        "",
        "**The mechanical cocycle.** On **%d** bridges and **%d** steps: the "
        "plain reverse recursion **%d** violations; Theorem 12.1's rewritten "
        "exponent **%d**; Theorem 12.2's normalized form "
        "`U_{l+1} = (2^a U_l - 2^{-m_{l+1}})/3` **%d**; the closed form "
        "`U_h = 2^{eps_h} Z - (1/3) sum 2^{eps_h-eps_l} 2^{-m_l}` **%d**; the "
        "weights outside `(1/2, 2)` **%d**. Boundary conditions: `U_0 != Z` "
        "**%d** times, and on the **%d** zero-lift bridges `U_h != X` **%d**. "
        "Theorem 13.1's residue parity **%d**, and the fact it reduces to "
        "`q = pi(V_l) mod 2` disagreed **%d** times; **%d** reverse states "
        "fell outside `1, 2 mod 3`."
        % (co["bridges"], co["steps"], co["reverse_recursion_violations"],
           co["lifted_cocycle_theorem_12_1_violations"],
           co["normalized_cocycle_theorem_12_2_violations"],
           co["closed_form_violations"], co["weight_outside_one_half_to_two"],
           co["u_zero_not_the_endpoint"], co["zero_lift_bridges"],
           co["u_h_not_the_source_on_a_zero_lift_bridge"],
           co["residue_parity_theorem_13_1_violations"],
           co["residue_parity_not_equal_to_the_valuation_parity"],
           co["reverse_state_outside_one_or_two_mod_three"]),
        "",
        "**The zero-lift class, without floating point.** "
        "`P_down = (Z/X) 2^{eps_h}` is an exact rational once `m_h = 0`, so "
        "Theorem 11.1's `P_down < 2` needs no float. On **%d** zero-lift "
        "bridges (**%d** positive-lift): the excess decomposition "
        "`2^E = 2^{m_h} 2^{eps_h}` **%d** violations, the product identity "
        "**%d**, the bound itself **%d**, and Corollary 11.2's reciprocal "
        "mass against a certified `4 ln 2 = %.6f` **%d**. The bundle's "
        "float64 form with its `1e-12` fudge would have decided differently "
        "on **%d**. Largest product actually seen **%.6f**, largest "
        "reciprocal mass **%.6f** — the ceiling is loose by a factor of about "
        "%d, which is worth saying beside a zero."
        % (zl["zero_lift_bridges"], zl["positive_lift_bridges"],
           zl["excess_decomposition_violations"],
           zl["product_identity_violations"],
           zl["product_theorem_11_1_violations"], zl["reciprocal_ceiling"],
           zl["reciprocal_mass_corollary_11_2_violations"],
           zl["reciprocal_mass_decided_by_the_float64_form"],
           zl["largest_product_seen"], zl["largest_reciprocal_mass_seen"],
           int(zl["reciprocal_ceiling"] / max(zl["largest_reciprocal_mass_seen"],
                                              1e-12))),
        "",
        "**Theorem 14.1's countermodel, rebuilt from the paper's three "
        "steps** rather than accepted. **%d** lengths, **%d** failing their "
        "precondition. `m_0 = 0` **%d** violations, `m_h = 0` **%d**, "
        "`m_l >= 0` **%d**, `q in {1,2,3}` **%d**, `sum q = ceil(beta h)` "
        "**%d**, `sum 2^{-m_l} < 6` **%d**. The paper's proof splits that "
        "mass three ways and each part has its own bound: rise `< 1` **%d** "
        "violations, plateau `< 1/h` **%d**, descent `< 4` **%d**, and a "
        "height held more than twice during the descent **%d** — checking "
        "only the total would let two of the three be wrong in compensating "
        "directions."
        % (ab["levels"], ab["constructions_that_failed_their_precondition"],
           ab["lift_not_starting_at_zero"], ab["lift_not_ending_at_zero"],
           ab["lift_negative"], ab["valuation_outside_one_to_three"],
           ab["total_valuation_not_the_ceiling"],
           ab["laplace_mass_at_or_above_six"], ab["rise_mass_at_or_above_one"],
           ab["plateau_mass_at_or_above_one_over_h"],
           ab["descent_mass_at_or_above_four"],
           ab["a_height_held_more_than_twice_in_the_descent"]),
        "",
        "| `h` | `M` | `max q` | `sum 2^-m` | rise | plateau | descent |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in ab["rows"]:
        out.append("| %d | %d | %d | %.6f | %.6f | %.6f | %.6f |"
                   % (row["h"], row["M"], row["max_q"], row["lift_sum"],
                      row["rise"], row["plateau"], row["descent"]))
    out += [
        "",
        "**Two of their twelve counters test a quantity against itself.** "
        "`near_linear_gap_algebra` asserts `lower > 0` for "
        "`lower = N/(R+1)` with `N >= 10^6` and `R >= 1`. Over **%d** samples "
        "at their stated ranges, **%d** could have failed, and the smallest "
        "left side seen is **%.0f**. `positive_lift_drop_algebra` asserts "
        "`drop >= 2 - beta - 1e-15` for `drop = (m + eps) - (beta - 1)`; "
        "subtract the two sides and `beta` cancels, leaving `m + eps >= 1` "
        "with `m >= 1` an integer. Evaluated with `beta` at BOTH ends of a "
        "certified bracket over **%d** samples, the two results differ **%d** "
        "times — which is what it means for the parameter not to participate "
        "— and **%d** samples could have failed, the tightest margin being "
        "**%.1f**. Twenty thousand of their assertion executions carry no "
        "information about `beta`, the bridge, or the round."
        % (ta["near_linear_samples"],
           ta["near_linear_samples_that_could_have_failed"],
           ta["near_linear_smallest_left_side"], ta["drop_samples"],
           ta["drop_difference_depends_on_beta"],
           ta["drop_samples_that_could_have_failed"],
           ta["drop_smallest_margin"]),
        "",
        "**All twelve published zero-lift examples, rebuilt from the map.** "
        "**%d** disagreeing values of `X`, **%d** of `Z`, **%d** exponent "
        "words, **%d** lengths, **%d** total lifts, **%d** maximum lifts, "
        "**%d** lift sums, **%d** tail products, **%d** reciprocal masses, "
        "**%d** tails not suffix-supercritical. **%d** source appears more "
        "than once."
        % (ex["x_disagreeing"], ex["z_disagreeing"],
           ex["exponent_word_disagreeing"], ex["h_disagreeing"],
           ex["total_lift_disagreeing"], ex["max_lift_disagreeing"],
           ex["lift_sum_disagreeing"], ex["tail_product_disagreeing"],
           ex["reciprocal_mass_disagreeing"],
           ex["tail_not_suffix_supercritical"],
           ex["sources_appearing_more_than_once"]),
        "",
        "| `y` | `X` | `Z` | `h` | word | lift profile | `sum 2^-m` | `P_down` |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in ex["rows"]:
        out.append("| %d | %d | %d | %d | `%s` | `%s` | `%s` | %s |"
                   % (row["y"], row["X"], row["Z"], row["h"], row["word"],
                      row["lift_profile"], row["lift_sum"], row["product"]))
    out += [
        "",
        "**Their six abstract countermodel rows**, rebuilt: **%d** of **%d** "
        "reproduced, **%d** disagreeing `M`, **%d** disagreeing `max q`, "
        "**%d** disagreeing Laplace mass."
        % (cm["rows_i_rebuilt"], cm["rows_published"], cm["m_disagreeing"],
           cm["max_q_disagreeing"], cm["lift_sum_disagreeing"]),
        "",
        "**A-U.2d.17's collapse, carried forward.** On the same **%d** "
        "bridges: **%d** source and **%d** endpoint congruence violations, "
        "with the source inside its modulus on **%d** and the endpoint on "
        "**%d**, both on **%d** (%s), and **%d** collapse violations there."
        % (cl["bridges"], cl["source_congruence_violations"],
           cl["endpoint_congruence_violations"],
           cl["source_inside_its_modulus"], cl["endpoint_inside_its_modulus"],
           cl["both_inside_their_moduli"],
           pct(cl["both_inside_their_moduli"], cl["bridges"]),
           cl["collapse_violations"]),
        "",
        "**The first-spike slice at the new scale.** Over **%d** orbits, "
        "**%d** reached the threshold: **%d** below it, **%d** not minimal, "
        "**%d** overshooting more than one step's slack gain, **%d** "
        "violating the length bound, **%d** prefix valuations below the "
        "length. The bound is attained with no additive constant on **%d**. "
        "Containment is asymptotic and at these scales holds for a minority: "
        "source inside **%d** / outside **%d**, endpoint inside **%d** / "
        "outside **%d**."
        % (fs["orbits"], fs["first_hits"], fs["first_hit_below_the_threshold"],
           fs["first_hit_not_minimal"], fs["overshoot_above_one_step"],
           fs["length_bound_violations"],
           fs["prefix_valuation_below_the_length"],
           fs["length_bound_attained_with_no_additive_constant"],
           fs["source_inside_its_cylinder"], fs["source_outside_its_cylinder"],
           fs["endpoint_inside_its_cylinder"],
           fs["endpoint_outside_its_cylinder"]),
        "",
        "**Constants.** %d checked: **%d** disagree with both readings of "
        "their own formula, %d are the nearest double, %d are what the same "
        "formula gives in float64, %d brackets could not decide."
        % (cs["constants_checked"], cs["disagreeing_with_both_evaluations"],
           cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["undecided_brackets"]),
        "",
        "| constant | published | nearest double | budget | verdict |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in cs["rows"]:
        out.append("| `%s` | %s | %s | %d | %s |"
                   % (row["constant"], row["published"],
                      row.get("nearest_double", "—"), row["budget"],
                      row["verdict"]))
    out += [
        "",
        "**Artifacts.** %d files, %d carrying a `CHECKSUMS` digest, **%d** "
        "mismatches, **%d** manifest lines naming a missing file; the only "
        "file with no digest anywhere is %s. The source-validation record "
        "names **%d** files and digests **%d** of them (**%d** digest and "
        "**%d** size mismatches), reports `all_ok = %s`, **%d** `json_parse` "
        "entries with **%d** not true, `python_compile = %s`, and **%d** "
        "per-file `ok` flags not true. %d files are absent from it: %s."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "none",
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           af["validation_digest_mismatches"], af["validation_size_mismatches"],
           af["validation_all_ok_flag"], af["validation_json_parse_entries"],
           af["validation_json_parse_not_true"],
           af["validation_python_compile_flag"],
           af["validation_file_ok_flags_not_true"],
           len(af["files_absent_from_the_validation_record"]),
           ", ".join("`%s`" % n
                     for n in af["files_absent_from_the_validation_record"])),
        "",
        "**Ledger coverage.** The paper lists %d proved items, %d open "
        "problems, and %d NO-GO headings of which %d are in section 18; the "
        "ledger carries %d, %d and %d, with an `open` key (%s). Open items "
        "with no trace: %s. NO-GO headings with no trace: %s. The heuristic "
        "deciding those lists has controls at both ends and failed neither "
        "(%d, %d)."
        % (led["paper_proved_items"], led["paper_open_items"],
           led["paper_no_go_headings"],
           led["paper_no_go_headings_in_section_18"],
           led["ledger_proved_items"], led["ledger_open_items"],
           led["ledger_no_go_items"], led["ledger_has_an_open_key"],
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
        print(json.dumps({"tool": "src65_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src65_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
