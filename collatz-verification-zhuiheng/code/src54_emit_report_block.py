"""Emit RUN-036's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src54_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src54-au2d8.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src54-drill.json"
REPORT = ROOT / "reports" / "RUN-036-HARD-ZETA-AU2D8-LOW-SOURCE-SATURATION.md"
FIGURES = ROOT / "data" / "gate-logs" / "src54-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src54_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    seg, gam, dep = g["segments"], g["gamma"], g["harmonic_depth"]
    gr, car, cs = g["grids"], g["au2d7_carryover"], g["constants"]
    led, ar, tc = g["ledger"], g["artifacts"], g["their_claims"]

    out = [
        BEGIN, "",
        "**Sections 3, 4 and 5 on real orbits.** Every row is decided in exact "
        "rational arithmetic. No logarithm and no Gamma function is evaluated "
        "anywhere in this table.",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    rows = [
        ("accelerated segments from %d orbits" % seg["orbits"],
         "longest `L` = %d, largest source = %d" % (seg["max_L"], seg["max_source"]),
         seg["segments"]),
        ("…**violations of Theorem 3.1** `z/y = (3^L/2^Q)·∏(1+1/(3Y_j))`",
         "exact Fractions, must be zero", seg["product_identity_violations"]),
        ("…where the `2^(−D)` form differs from the `3^L/2^Q` form",
         "the same thing, since `2^(βL) = 3^L`",
         seg["two_forms_of_the_identity_disagree"]),
        ("segments meeting §4's premise",
         "source is the segment minimum and the states are distinct; %d and %d fail"
         % (seg["sources_that_are_not_the_segment_minimum"],
            seg["segments_with_a_repeated_state"]),
         seg["segments_meeting_the_packing_premise"]),
        ("…**violations of Theorem 4.1** `𝒫 ≤ 𝒫(y,L)`",
         "checked on all %d of them" % seg["envelopes_compared"],
         seg["packing_envelope_violations"]),
        ("…sorted states falling below `y + 2k`",
         "the bound the envelope rests on", seg["sorted_state_below_y_plus_2k"]),
        ("**Theorem 5.1** segments where the Gamma form ≠ the product",
         "as an exact Pochhammer quotient", seg["gamma_form_disagrees_with_the_product"]),
        ("…designed `(y,L)` pairs, largest `L` = %d" % gam["largest_L"],
         "exact disagreements: %d" % gam["exact_disagreements"], gam["pairs"]),
        ("…**disagreeing with `math.lgamma` beyond its cancellation bound**",
         "worst error `%.3e`, which is `%.2f×` the bound the subtraction costs"
         % (gam["worst_lgamma_absolute_error"],
            gam["worst_error_over_its_cancellation_bound"]),
         gam["lgamma_disagreements_beyond_cancellation"]),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out += [
        "",
        "The shipped checker reports `max_gamma_log2_abs_error = %s` for this "
        "identity. This run's error is `%s`, because for integer `L` the Gamma "
        "quotient **is** the Pochhammer product and there is nothing to compare."
        % (tc["their_worst_gamma_error"], tc["this_run_s_gamma_error"]),
        "",
        "**Theorem 9.1's premise, measured.** 9.1 is Theorem 7.2 rearranged, and "
        "7.2 descends from the inherited `y_r > 2^H y_1` and `z_1 > y_r`. Those "
        "describe the hypothetical divergent orbit, not a real one.",
        "",
        "| premise | of | met |",
        "| --- | --- | --- |",
    ]
    prem = [
        ("§4's packing premise", "%d chains" % dep["chains"],
         dep["chains_meeting_the_packing_premise"]),
        ("**`z_1 > y_r`**, the outer endpoint above the innermost source",
         "%d chains" % dep["chains"],
         dep["chains_where_the_outer_endpoint_exceeds_the_inner_source"]),
        ("`y_r ≥ y_1 + 4(r−1)`, the `3 (mod 4)` source spacing",
         "%d chains" % dep["chains"],
         dep["chains_with_4_apart_sources_y_r_ge_y_1_plus_4r_minus_4"]),
        ("**the endpoint-gap premise** `z_1/y_1 > 1 + (4r−2)/y_1`",
         "%d chains" % dep["chains"], dep["chains_meeting_the_endpoint_gap_premise"]),
        ("every premise at once", "%d chains" % dep["chains"],
         dep["chains_meeting_every_premise"]),
    ]
    for what, of, met in prem:
        out.append("| %s | %s | `%s` |" % (what, of, met))
    out += [
        "",
        "So Theorem 9.1 was applied to **%d** chains. It was not tested here and "
        "this run does not claim otherwise. What *is* universal and was checked "
        "on all **%d** chains is the round's algebra: `1 + (4r−2)/y₁ < 𝒫` and "
        "`r < ½ + y₁(𝒫−1)/4` are one inequality, and they disagreed on `%d` of "
        "them. The low-source regime `3 ≤ y₁ ≤ L` is attained by `%d` chains, so "
        "the regime itself is not vacuous; the premise above it is."
        % (dep["theorem_9_1_checked"], dep["chains"],
           dep["the_two_forms_of_9_1_are_not_equivalent"],
           dep["low_source_chains_3_le_y1_le_L"]),
        "",
        "**Sections 5.2 and 9.2 as implications**, over `%d` grid points in "
        "`(y, L)` of which `%d` are in the low-source regime:"
        % (gr["grid_points"], gr["low_source_grid_points"]),
        "",
        "| derivation | violations |",
        "| --- | --- |",
    ]
    for what, key in (
        ("**Theorem 5.2** sharp: `R ≤ 1/(3y ln2) + ln(1+2L/y)/(6 ln2)`",
         "harmonic_envelope_violations"),
        ("**Theorem 5.2** coarse: `R < L/(3y ln2)`", "coarse_envelope_violations"),
        ("**Corollary 9.2** follows from the exact cap of 9.1",
         "sixth_root_cap_violations"),
        ("…and its inversion `y₁ > c_H(r−½)^(6/5)L^(−1/5)`",
         "sixth_root_inversion_violations"),
        ("`μ★ = (6θ★−1)/5` as stated", "mu_star_not_six_theta_minus_one_over_five"),
        ("the old exponent is `θ★/(1+θ★)`",
         "old_exponent_not_theta_over_one_plus_theta"),
    ):
        out.append("| %s | `%d` |" % (what, gr[key]))

    out += [
        "",
        "**Section 15's floors, recomputed from A-U.2d.7 — the round RUN-035 "
        "verified.** `Y_ver = 2075·2^60 = %d` recomputes exactly: `%s`. Each row "
        "is `X_r·√Y_ver` with `X_r` the positive root of `ax²+bx = r−1`, "
        "compared against the published double by bracket, never by rendering a "
        "decimal."
        % (car["verified_floor"], car["verified_floor_recomputes"]),
        "",
        "| depth `r` | published | ulps from the nearest double |",
        "| --- | --- | --- |",
    ]
    for row in car["rows"]:
        out.append("| `%s` | `%s` | `%s` |"
                   % (row["depth"], row["published"],
                      row.get("ulps", "undecided")))
    out += [
        "",
        "`√(3 ln2·Y_ver)` is `%d` ulps from its published value and `log₂Y_ver` "
        "is `%d`. The inversion first becomes **sharper** than the high-source "
        "route at depth `%d`; the paper tabulates from `r ≥ 9`, and the "
        "checker's `r = %s` row is correct arithmetic that is not the binding "
        "constraint there."
        % (car["high_source_floor"]["ulps"], car["log2_floor"]["ulps"],
           car["inversion_sharper_from_depth"],
           ", ".join(str(x) for x in
                     car["depths_where_the_inversion_is_published_but_weaker"])
           or "none"),
        "",
        "**Constants.** `θ★` and `μ★` are exactly rational: `θ★ = %s` and "
        "`μ★ = %s`, both determined by `ρ★ = 4.1164`."
        % (gr["theta_star_exact"], gr["mu_star_exact"]),
        "",
        "| constant | published | exact | ulps |",
        "| --- | --- | --- | --- |",
    ]
    for name, row in cs["rows"].items():
        out.append("| `%s` | `%s` | `%s` | `%d` |"
                   % (name, row["published"], row["exact"],
                      row["ulps_from_the_nearest_double"]))
    for name in ("C_H", "c_H"):
        out.append("| `%s` | `%s` | `%s` (%s) | `%s` |"
                   % (name, cs[name]["published"], cs[name]["closed_form"],
                      cs[name]["recomputed"][:18], cs[name].get("ulps", "?")))
    out += [
        "",
        "The drift is not a mystery. `1/(4.1164+1)` evaluated in float64 "
        "reproduces the published `theta_star` bit for bit: `%s`; and "
        "`(6θ−1)/5` from that float reproduces `mu_star`: `%s`. The two "
        "rationals were computed in doubles rather than exactly, while the "
        "**transcendental** constants — `C_H`, `log₂Y_ver`, `√(3 ln2 Y_ver)` — "
        "are the exact nearest doubles."
        % (cs["the_published_value_is_the_float64_evaluation"]["theta_star"],
           cs["the_published_value_is_the_float64_evaluation"]["mu_star"]),
        "",
        "| the paper prints | verdict |",
        "| --- | --- |",
    ]
    for name, row in cs["inline_decimals_in_the_paper"].items():
        out.append("| `%s` = `%s…` | %s |" % (name, row["published"], row["verdict"]))

    out += [
        "",
        "**The theorem ledger against the paper's own section 21.**",
        "",
        "| the paper says | the JSON ledger says | shortfall |",
        "| --- | --- | --- |",
    ]
    for row in led["table"]:
        out.append("| §%s: `%d` | `%s`: `%d` | `%d` |"
                   % (row["paper_section"], row["paper_items"],
                      row["ledger_key"], row["ledger_items"], row["shortfall"]))
    ext = led["paper_external_inputs_with_no_ledger_entry_sharing_a_keyword"]
    out += [
        "",
        "§17's `%d` `NO-GO` headings match the ledger's `%d` exactly — the gap "
        "A-U.2d.7 had is closed. Of §21.3's `%d` external inputs the one with no "
        "ledger entry sharing a distinctive word is **%s**. §21.5's three "
        "bullets are not missing but **merged** into two entries: `%d` bullets "
        "have no entry, `%d` are undecidable by that test. The ledger no longer "
        "carries a `status` (`%s`) or a `next` (`%s`) field, so A-U.2d.7's "
        "disagreement between ledger and frontier cannot recur."
        % (led["paper_no_go_headings"], led["ledger_no_go_entries"],
           ext["bullets"],
           "; ".join("*%s*" % s for s in ext["with_no_ledger_entry"]) or "none",
           len(led["paper_open_questions_with_no_ledger_entry_sharing_a_keyword"]
               ["with_no_ledger_entry"]),
           len(led["paper_open_questions_with_no_ledger_entry_sharing_a_keyword"]
               ["undecidable_by_this_test"]),
           led["the_ledger_declares_a_status"],
           led["the_ledger_declares_a_next_round"]),
        "",
        "**Two manifests, and they agree.**",
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]
    tail = [
        ("files in the bundle",
         "`CHECKSUMS.sha256` lists %d, the validation record %d"
         % (ar["listed_in_CHECKSUMS"], ar["listed_in_the_validation_record"]),
         ar["files_in_the_bundle"]),
        ("…digests in `CHECKSUMS` that do not reproduce", "must be zero",
         len(ar["CHECKSUMS_mismatches"])),
        ("…digests in the validation record that do not reproduce",
         "must be zero", len(ar["validation_record_mismatches"])),
        ("…**where the two manifests disagree**", "on the files both list",
         len(ar["digests_disagreeing_between_the_two_manifests"])),
        ("…files covered by **neither**",
         "`%s`; the scope note declares it: `%s`"
         % (", ".join(ar["covered_by_neither_manifest"]) or "none",
            ar["the_scope_note_declares_the_gap"]),
         len(ar["covered_by_neither_manifest"])),
        ("validation-record shape", ar["validation_record_shape"], "—"),
        ("a `checker_stdout.txt` is shipped",
         "the first bundle since item 49 without one",
         ar["a_stdout_transcript_is_shipped"]),
        ("the checker's named checks independently confirmed",
         "of %d under the key `checks`; %d named as not covered here"
         % (tc["checks_the_report_names"], len(tc["not_covered_by_this_run"])),
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
        "**Not covered here**, named rather than implied: "
        + "; ".join("*%s*" % c for c in tc["not_covered_by_this_run"]) + ".",
        "",
        "Every figure above is emitted by `code/src54_emit_report_block.py` from "
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
        print(json.dumps({"tool": "src54_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src54_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
