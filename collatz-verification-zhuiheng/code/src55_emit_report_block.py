"""Emit RUN-037's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src55_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src55-au2d9.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src55-drill.json"
REPORT = ROOT / "reports" / "RUN-037-HARD-ZETA-AU2D9-ORBIT-PACKING-DEFICIT.md"
FIGURES = ROOT / "data" / "gate-logs" / "src55-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src55_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    sv, pk, gam = g["sieve"], g["packing"], g["gamma"]
    ex, ag, qc = g["exponents"], g["anchor_gap"], g["qclass"]
    gr, dc, cs = g["grids"], g["depth_cap"], g["constants"]
    led, ar, tc = g["ledger"], g["artifacts"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The sieve and what it buys, on real orbits.** Every row is decided "
        "in integers.",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("odd integers mapped through `Syr`", "Theorem 3.1",
         sv["odd_integers_mapped"]),
        ("…**images divisible by three**", "must be zero",
         sv["images_divisible_by_three"]),
        ("post-entry orbit states", "Corollary 3.2, `1` or `5 (mod 6)`",
         sv["post_entry_states"]),
        ("…outside `{1,5} (mod 6)`", "must be zero",
         sv["states_not_1_or_5_mod_6"]),
        ("post-entry sources with `L ≥ 2`",
         "%d pre-entry sources excluded" % sv["pre_entry_sources_excluded"],
         sv["post_entry_sources_with_L_at_least_2"]),
        ("…not `3 (mod 4)` / not `7` or `11 (mod 12)`",
         "A-U.2d.5's result and Corollary 3.3's refinement of it",
         "%d / %d" % (sv["sources_not_3_mod_4"],
                      sv["sources_not_7_or_11_mod_12"])),
        ("**sources with `L = 1`, which the premise excludes**",
         "of which %d are outside `{7,11} (mod 12)`"
         % sv["L_equal_1_sources_not_7_or_11_mod_12"],
         sv["sources_with_L_equal_1"]),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))
    out += [
        "",
        "That last row is the reason the premise is stated. Corollary 3.3 "
        "refines a result that needs `L ≥ 2`; applied to every first-crossing "
        "source instead, **%d** of them would have been reported as violations "
        "of a theorem that holds."
        % sv["L_equal_1_sources_not_7_or_11_mod_12"],
        "",
        "**The sieved packing and its Gamma form.**",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("segments meeting the packing premise",
         "source minimal and states distinct; %d fail"
         % pk["segments_failing_distinctness_or_minimality"],
         pk["segments_meeting_the_packing_premise"]),
        ("…sorted states below their admissible position `a_k(y)`",
         "Definition 4.1, longest `L` = %d" % pk["max_L"],
         pk["sorted_state_below_its_admissible_position"]),
        ("…explicit admissible positions wrong",
         "`a_{2m} = y+6m`, `a_{2m+1} = y+6m+4` or `+2`",
         pk["explicit_admissible_position_errors"]),
        ("…`a_k(y)` below the uniform bound `y+3k−1`", "must be zero",
         pk["uniform_lower_bound_a_k_below_y_plus_3k_minus_1"]),
        ("…**violations of Theorem 4.2** `𝒫 ≤ 𝒫₆(y,L)`", "must be zero",
         pk["sieved_envelope_violations"]),
        ("…where the sieved envelope exceeds the odd one",
         "the deficit must point the right way",
         pk["sieved_envelope_above_the_odd_envelope"]),
        ("…**where Theorem 5.1's two-progression form ≠ the product**",
         "as exact Pochhammer quotients",
         pk["two_progression_form_disagrees_with_the_product"]),
        ("designed `(y,L)` pairs for Theorem 5.1, largest `L` = %d"
         % gam["largest_L"],
         "exact disagreements: %d" % gam["exact_disagreements"], gam["pairs"]),
        ("…disagreeing with `math.lgamma` beyond its cancellation bound",
         "worst error `%.3e`, `%.2f×` the bound the subtraction costs"
         % (gam["worst_lgamma_absolute_error"],
            gam["worst_error_over_its_cancellation_bound"]),
         gam["lgamma_disagreements_beyond_cancellation"]),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))
    out += [
        "",
        "The shipped checker reports `max_gamma_relative_error = %s`. This "
        "run's is `%s`: at integer `n` the Gamma quotient is the Pochhammer "
        "product it was built from, so both sides are one rational."
        % (tc["their_worst_gamma_error"], tc["this_run_s_gamma_error"]),
        "",
        "**The exponents, empirically.** `𝒫₆ = Θ(L^{1/9})` and "
        "`𝒫₆/𝒫_odd = Θ(L^{−1/18})` are asymptotic, so what is checked is that "
        "the measured exponent moves toward the claim and that the deficit "
        "stays negative — not that either is reached at finite `L`.",
        "",
        "| `y` | `L` | sieved exponent → `1/9` | odd exponent → `1/6` | deficit |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in ex["rows"]:
        out.append("| `%d` | `%d` | `%s` | `%s` | `%s` |"
                   % (r["y"], r["L"], r["sieved_exponent"], r["odd_exponent"],
                      r["deficit_exponent"]))
    out += [
        "",
        "Non-monotone steps toward `1/9`: `%d`; toward `1/6`: `%d`; deficits "
        "not negative: `%d`."
        % (ex["sieved_exponent_not_approaching_one_ninth"],
           ex["odd_exponent_not_approaching_one_sixth"],
           ex["deficit_exponent_not_negative"]),
        "",
        "**Lemma 7.1, split into the half that can be enumerated and the half "
        "that cannot be tested.**",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("residue sets of `{7,11} (mod 12)` anchors enumerated",
         "depths 2 to 6", ag["residue_sets_enumerated"]),
        ("…**spans below `6(r−1) − 2`**", "the proof's own phase allowance",
         ag["spans_below_six_r_minus_eight"]),
        ("…tight sets whose last anchor is not `11 (mod 12)`",
         "the proof's phase claim",
         ag["tight_sets_whose_last_anchor_is_not_11_mod_12"]),
        ("…tight sets whose next admissible state is not exactly `2` higher",
         "what closes the gap to `6(r−1)`",
         ag["tight_sets_whose_next_admissible_state_is_not_two_higher"]),
        ("chains built", "deepest `r` = %d" % ag["max_depth"], ag["chains"]),
        ("…**where `z₁ > y_r`**, the premise Lemma 7.1 needs",
         "a first-crossing endpoint is where the slack drops",
         ag["chains_where_the_outer_endpoint_exceeds_the_inner_source"]),
        ("…Lemma 7.1 applied / violated", "premise-gated",
         "%d / %d" % (ag["lemma_7_1_checked"], ag["lemma_7_1_violations"])),
        ("**Theorem 8.1's two forms disagreeing**",
         "universal algebra, checked on all %d chains" % dc["chains"],
         dc["the_two_forms_of_8_1_are_not_equivalent"]),
        ("…Theorem 8.1 applied / violated",
         "%d chains are in the low-source regime `7 ≤ y₁ ≤ L`"
         % dc["low_source_chains_7_le_y1_le_L"],
         "%d / %d" % (dc["theorem_8_1_checked"], dc["theorem_8_1_violations"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**Section 11 — the one theorem here whose premise real orbits do "
        "meet.** Theorem 11.2 assumes first-crossing subcriticality, "
        "`Σq_j < βm`, which is what a first-crossing interval *is*; the test is "
        "the exact integer comparison `2^Q < 3^m`.",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("valuations `k` checked for Lemma 11.1",
         "`q(n) = k` must select exactly one class mod `2^{k+1}`",
         qc["valuations_checked"]),
        ("…selecting a number of classes other than one", "must be zero",
         qc["valuation_classes_not_exactly_one_mod_2_to_k_plus_1"]),
        ("capacity windows enumerated",
         "`N_k ≤ W/(3·2^k) + 1` — the `3` is the sieve",
         qc["capacity_windows"]),
        ("…exceeding that per-valuation capacity", "must be zero",
         qc["windows_where_N_k_exceeds_W_over_three_two_to_k_plus_one"]),
        ("…**exceeding the weighted bound `17W/24 + 12`**",
         "where the `17/24` in the theorem comes from",
         qc["windows_where_the_weighted_capacity_exceeds_17W_over_24_plus_12"]),
        ("proper prefixes examined", "longest `m` = %d" % qc["max_prefix_length"],
         qc["prefixes"]),
        ("…**meeting subcriticality** `2^Q < 3^m`",
         "%d fail; %d have a repeated state"
         % (qc["prefixes_failing_subcriticality"],
            qc["prefixes_with_repeated_states"]),
         qc["prefixes_meeting_subcriticality"]),
        ("…**Theorem 11.2 applied / violated**",
         "`W > (24/17)((4−β)(L−1) − 12)`",
         "%d / %d" % (qc["theorem_11_2_checked"], qc["theorem_11_2_violations"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "**Sections 6 and 8 as implications**, over `%d` grid points of which "
        "`%d` are low-source:" % (gr["grid_points"], gr["low_source_grid_points"]),
        "",
        "| derivation | violations |",
        "| --- | --- |",
    ]
    for what, key in (
        ("**Theorem 6.1** the 3-sieved harmonic bound", "theorem_6_1_violations"),
        ("**Corollary 6.2** `𝒫₆ ≤ C₆(L/y)^{1/9}`", "corollary_6_2_violations"),
        ("**Corollary 8.2** follows from the exact cap of 8.1",
         "corollary_8_2_not_implied_by_8_1"),
        ("**Corollary 8.3** inverts it", "corollary_8_3_inversion_violations"),
        ("`μ9 = (9θ★−1)/8` as stated", "mu9_not_nine_theta_minus_one_over_eight"),
        ("`1/18 = 1/6 − 1/9`", "deficit_exponent_not_one_sixth_minus_one_ninth"),
    ):
        out.append("| %s | `%d` |" % (what, gr[key]))

    out += [
        "",
        "**Constants, against their closed forms.** `θ★ = %s` and "
        "`μ9 = %s` are exactly rational."
        % (gr["theta_star_exact"], gr["mu9_exact"]),
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
        "The drift is a chain, and every link reproduces. `C₉` is the published "
        "`C₆` divided by six **as doubles**: `%s`. `c₉` is that `C₉` raised to "
        "`−9/8` as doubles: `%s`. `μ9` is the float64 `θ★` put through its own "
        "formula: `%s`. And the checker report's spacing is the float64 "
        "reciprocal of the density: `%s`. Each derived constant inherits its "
        "parent's rounding instead of being computed from the closed form."
        % (chain["C9_is_the_published_C6_divided_by_six_as_doubles"],
           chain["c9_is_the_published_C9_to_the_minus_nine_eighths_as_doubles"],
           chain["mu9_is_the_float64_theta_star_put_through_its_formula"],
           chain["the_spacing_is_the_float64_reciprocal_of_the_density"]),
        "",
        "**The two artifacts disagree on `%d` constant%s** and rename `%d`:"
        % (len(cs["constants_the_two_artifacts_disagree_on"]),
           "" if len(cs["constants_the_two_artifacts_disagree_on"]) == 1 else "s",
           len(cs["constants_renamed_between_the_two_artifacts"])),
        "",
        "| constant | checker report | constants frontier | ulps apart |",
        "| --- | --- | --- | --- |",
    ]
    for row in cs["constants_the_two_artifacts_disagree_on"]:
        out.append("| `%s` | `%s` | `%s` | `%d` |"
                   % (row["constant"], row["checker_report"], row["frontier"],
                      row["ulps_apart"]))
    for row in cs["constants_renamed_between_the_two_artifacts"]:
        out.append("| renamed | `%s` | `%s` | — |"
                   % (row["checker_report"], row["frontier"]))
    out += [
        "",
        "| the paper prints | verdict |",
        "| --- | --- |",
    ]
    for name, row in cs["inline_decimals_in_the_paper"].items():
        out.append("| `%s` = `%s…` | %s |" % (name, row["published"],
                                              row["verdict"]))

    out += [
        "",
        "**The ledger against the paper's own section 18.**",
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
        "§14's `%d` `NO-GO` headings against the ledger's `%d`; titles with no "
        "ledger entry sharing a distinctive word: %s."
        % (led["paper_no_go_headings"], led["ledger_no_go_entries"],
           "; ".join("*%s*" % s for s in
                     led["paper_no_go_titles_with_no_ledger_entry_sharing_a_keyword"])
           or "none"),
        "",
        "**The manifests.**",
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
        ("…**digests the record gives with no filename at all**",
         "resolved by looking the digest up among the files: %s"
         % (", ".join("%s → %s" % (r["block"], r["resolves_to"])
                      for r in ar["…resolved_by_looking_the_digest_up_among_the_files"])
            or "none"),
         ar["digests_the_record_gives_without_a_filename"]),
        ("…files covered by neither manifest",
         "`%s`; a scope note declares it: `%s`"
         % (", ".join(ar["covered_by_neither_manifest"]) or "none",
            ar["the_scope_note_declares_the_gap"]),
         len(ar["covered_by_neither_manifest"])),
        ("validation-record shape", ar["validation_record_shape"], "—"),
        ("the record says its checker rerun matches its report",
         "its own claim, not rechecked here",
         ar["the_record_says_the_checker_rerun_matches_its_report"]),
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
        "Every figure above is emitted by `code/src55_emit_report_block.py` from "
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
        print(json.dumps({"tool": "src55_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src55_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
