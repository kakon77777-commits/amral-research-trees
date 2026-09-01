"""Emit RUN-048's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src67_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src67-au2d20.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src67-drill.json"
REPORT = ROOT / "reports" / "RUN-048-HARD-ZETA-AU2D20-RETURN-LOOPS.md"
FIGURES = ROOT / "data" / "gate-logs" / "src67-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src67_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    lo, sb, la = g["locality"], g["source_budget"], g["labels"]
    al, lp, cm = g["alias"], g["loops"], g["clean_mass"]
    ta, nf, ex = g["their_algebra"], g["near_full"], g["examples"]
    af, led, tc = g["artifacts"], g["ledger"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The population.** **%d** bridges from **%d** distinct sources "
        "(longest tail %d), of which **%d** have zero total lift and **%d** do "
        "not — the fourth round running in which the positive-lift branch has "
        "no finite instance."
        % (pop["bridges"], pop["sources"], pop["longest_tail"],
           pop["zero_lift"], pop["positive_lift"]),
        "",
        "**Theorem 3.1, in the form it is stated in.** The boxed statement is a "
        "**k-term** sum, and its content is that the terms past `j = k` "
        "contribute nothing modulo `3^k`. Over **%d** bridges and **%d** "
        "levels: the truncated sum **%d** violations, the full sum **%d**, the "
        "two disagreeing **%d**, a tail term not divisible by the modulus "
        "**%d**, and the bundle's own form — the k-suffix's endpoint "
        "representative against `Z mod 3^k` — **%d**. Same value, different "
        "sentence: the bundle verifies that the suffix determines the residue, "
        "not that only the first k terms of the sum do."
        % (lo["bridges"], lo["levels"], lo["truncated_sum_violations"],
           lo["full_sum_violations"], lo["truncation_changes_the_residue"],
           lo["tail_term_not_divisible_by_the_modulus"],
           lo["suffix_representative_violations"]),
        "",
        "**Theorem 4.1, both halves separately.** "
        "`P_r <= ceil(beta h) - ceil(beta(h-r)) <= 2r` has a left inequality "
        "that is zero total lift plus suffix supercriticality and a right one "
        "that is `a_j <= 2` summed; the bundle asserts them in one chained "
        "expression, so a failure of either reads the same. Over **%d** "
        "prefixes: **%d** and **%d** violations. Both are tight — the left is "
        "**attained %d** times (%s) and the right **%d** — and the largest "
        "`P_r / r` seen is exactly **%.1f**, so `2r` is reached. A single "
        "valuation exceeded `2r` **%d** times."
        % (sb["prefixes"], sb["left_inequality_violations"],
           sb["right_inequality_violations"], sb["left_inequality_attained"],
           pct(sb["left_inequality_attained"], sb["prefixes"]),
           sb["right_inequality_attained"],
           sb["largest_prefix_over_r_seen"],
           sb["single_valuation_above_two_r"]),
        "",
        "**Theorem 5.1 and Corollary 5.2, checked sharp.** Over **%d** "
        "precisions: the period disagreeing with `2M/3` **%d** times; **%d** "
        "transition pairs below the period with **%d** label collisions; and "
        "**%d** residues where no collision occurs AT the period — the "
        "sharpness the bundle does not test, and without which a period three "
        "times too long would pass. Over **%d** sheet checks, **%d** residues "
        "carried more than three labels and **%d** carried exactly three, so "
        "the bound is attained on every one; **%d** precisions failed to "
        "attain it."
        % (la["levels"], la["period_disagreeing_with_two_thirds_m"],
           la["pairs"], la["label_collisions_below_the_period"],
           la["no_collision_at_the_period"], la["sheet_checks"],
           la["more_than_three_sheets"],
           la["residues_with_exactly_three_sheets"],
           la["three_sheets_never_attained"]),
        "",
        "**Theorem 6.1's alias budget.** Over **%d** bridge-precision pairs: "
        "**%d** violations of `B_k s_k <= Q_h`, **%d** of the `q >= 2M` form, "
        "and **%d** total valuations disagreeing with `ceil(beta h)`. **%d** "
        "of the pairs actually contain an alias-large edge, and the largest "
        "count on one bridge is **%d** — so the budget is not bounding an "
        "empty set."
        % (al["levels"], al["budget_theorem_6_1_violations"],
           al["large_edge_budget_violations"],
           al["total_valuation_not_the_ceiling"],
           al["levels_with_an_alias_large_edge"],
           al["largest_alias_count_seen"]),
        "",
        "**The return loops and Theorem 11.1's certificate.** **%d** loops "
        "built from the real orbits across **%d** bridge-precision pairs, "
        "total edge mass **%d**. The certificate "
        "`(2^{Q_C} - 3^{L_C}) r_C = B_C mod M`: **%d** violations. The exact "
        "integer identity it is a shadow of: **%d**. Loop endpoints not "
        "congruent: **%d**. Certificates trivially zero on both sides: **%d**. "
        "The bundle's loop block verifies mass lower bounds only, so the "
        "certificate is checked here for the first time."
        % (lp["loops"], lp["levels"], lp["total_loop_edge_mass"],
           lp["certificate_theorem_11_1_violations"],
           lp["segment_affine_identity_violations"],
           lp["loop_endpoints_not_congruent"],
           lp["certificate_trivially_zero"]),
        "",
        "**\"Return loop\" names two objects, and the period bounds one of "
        "them.** The ERASED CYCLE — the stack vertices from the first "
        "occurrence on, all carrying distinct unit residues — is bounded by "
        "`s_k = 2M/3` because there are only that many units to be distinct "
        "in: **%d** violations, longest cycle seen **%d**. The ORBIT SEGMENT "
        "carrying the certificate is a different thing, because it can enclose "
        "previously erased loops: **%d of %d** exceed the period (%s), longest "
        "**%d**, and **%d** (%s) differ from their own erased cycle at all. "
        "Applying either bound to the other object reads as a violation; the "
        "certificate holds on all %d regardless."
        % (lp["erased_cycle_longer_than_the_period"],
           lp["longest_erased_cycle_seen"],
           lp["segment_longer_than_the_period"], lp["loops"],
           pct(lp["segment_longer_than_the_period"], lp["loops"]),
           lp["longest_loop_seen"],
           lp["segment_longer_than_its_erased_cycle"],
           pct(lp["segment_longer_than_its_erased_cycle"], lp["loops"]),
           lp["loops"]),
        "",
        "**Theorem 9.1's finite bound is vacuous on almost everything.** "
        "Rebuilt from the construction over **%d** bridges, **%d** "
        "bridge-precision levels and **%d** clean runs: **%d** masses below "
        "the bound. But the bound `h + 1 - (b + 2L + 1) s_k` is **positive on "
        "%d of %d levels** (%s) — everywhere else it is negative and the "
        "comparison says nothing. Where it is positive the smallest slack is "
        "**%d** and it is attained **%d** times. So three checks that ARE "
        "total were added instead: a clean run must contain no low-lift vertex "
        "(**%d**) and no `q >= 2M` edge (**%d**), and loop erasure must "
        "conserve edges, `erased + (path - 1) = run` (**%d**). The drill found "
        "that gap: four defects in this section moved nothing until those "
        "three existed. Total clean mass **%d**; residual paths longer than "
        "the period **%d**; the bundle's float loop depth disagreeing with the "
        "exact integer one **%d**."
        % (cm["bridges"], cm["levels"], cm["runs"],
           cm["mass_below_the_finite_bound"],
           cm["levels_where_the_bound_is_positive"], cm["levels"],
           pct(cm["levels_where_the_bound_is_positive"], cm["levels"]),
           cm["smallest_mass_minus_bound_seen"],
           cm["levels_where_the_bound_is_attained"],
           cm["low_lift_vertex_inside_a_clean_run"],
           cm["large_edge_inside_a_clean_run"],
           cm["erasure_accounting_violations"], cm["total_clean_mass"],
           cm["residual_path_longer_than_the_period"],
           cm["float_depth_disagreeing_with_the_integer_one"]),
        "",
        "**Their two synthetic blocks, and a fourth shape.** "
        "`fixed_power_high_lift_algebra` runs **%d** iterations and asserts "
        "three things: `gamma < eta`, arranged by the `max(gamma+0.01, eta)` "
        "on the line above (**%d** could have failed); `1-eta+gamma < 1`, "
        "which is the same inequality restated (**%d** samples where the two "
        "differed); and `C_LOOP > 0` on a constant computed outside the loop "
        "(**%d** samples where it varied). "
        "`boundary_alias_no_go_algebra` is the fourth shape this sweep has "
        "seen: the assertion is preceded by a **repair branch** that fixes any "
        "input that would fail it. Over **%d** samples the repair fired **%d** "
        "times and **%d** would have failed without it — the smallest left "
        "side before the repair is **%.4f**, after it **%.4f**. The repair is "
        "not merely protective; at these sampling ranges it never runs."
        % (ta["high_lift_samples"], ta["high_lift_gamma_not_below_eta"],
           ta["high_lift_second_assertion_differing_from_the_first"],
           ta["high_lift_constant_varying_across_the_loop"],
           ta["alias_samples"], ta["alias_repair_fired"],
           ta["alias_would_have_failed_without_the_repair"],
           ta["alias_smallest_left_side_before_the_repair"],
           ta["alias_smallest_left_side_after_the_repair"]),
        "",
        "**Their near-full diagnostic rows**, rebuilt: **%d** of **%d** "
        "reproduced, **%d** disagreeing `k`, **%d** alias bounds, **%d** "
        "faithful-run bounds, **%d** modulus-bracket violations. The two "
        "end-to-end trend assertions — the alias fraction falling and the "
        "faithful run growing — hold (**%d**, **%d**), and the rows are not "
        "monotone in between, which the bundle's own comment says."
        % (nf["rows_i_rebuilt"], nf["rows_published"], nf["k_disagreeing"],
           nf["alias_bound_disagreeing"], nf["faithful_run_disagreeing"],
           nf["modulus_bracket_violations"],
           nf["alias_fraction_not_decreasing_end_to_end"],
           nf["faithful_run_not_increasing_end_to_end"]),
        "",
        "| `log10 h` | `k` | alias bound | alias fraction | faithful run |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in nf["rows"]:
        out.append("| %d | %d | %d | %.4f | %d |"
                   % (row["h_power10"], row["k"], row["alias_bound"],
                      row["alias_fraction"], row["faithful_run"]))
    out += [
        "",
        "**All twelve published loop examples, rebuilt from the map.** **%d** "
        "not found in my population, **%d** disagreeing `X`, **%d** `Z`, "
        "**%d** lengths, **%d** moduli, **%d** periods, **%d** low-vertex "
        "counts, **%d** large-edge counts, **%d** lower bounds, and **%d** "
        "masses below their own published bound."
        % (ex["example_not_found_in_my_population"], ex["x_disagreeing"],
           ex["z_disagreeing"], ex["h_disagreeing"],
           ex["modulus_disagreeing"], ex["phi_disagreeing"],
           ex["low_vertex_count_disagreeing"],
           ex["large_edge_count_disagreeing"], ex["lower_bound_disagreeing"],
           ex["mass_below_their_lower_bound"]),
        "",
        "| `y` | `X` | `Z` | `h` | `M` | `s_k` | low vertices | `q >= 2M` | their mass | their bound |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in ex["rows"]:
        out.append("| %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |"
                   % (row["y"], row["X"], row["Z"], row["h"], row["M"],
                      row["phi"], row["low_vertices"], row["q_ge_2M"],
                      row["their_mass"], row["their_lower_bound"]))
    out += [
        "",
        "**Constants.** %d checked: **%d** disagree with both readings of "
        "their own formula, %d are the nearest double, %d are the float64 "
        "chain, %d brackets could not decide, and the frontier and the report "
        "disagree on **%d** — RUN-047's finding did not recur. **%d** group of "
        "report keys carries the same value under two names: %s."
        % (cs["constants_checked"], cs["disagreeing_with_both_evaluations"],
           cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["undecided_brackets"], cs["frontier_and_report_disagreeing"],
           cs["duplicate_keys_carrying_the_same_value"],
           "; ".join(", ".join("`%s`" % n for n in grp)
                     for grp in cs["duplicate_key_groups"]) or "none"),
        "",
        "| constant | frontier | report | verdict |",
        "| --- | --- | --- | --- |",
    ]
    for row in cs["rows"]:
        out.append("| `%s` | %s | %s | %s |"
                   % (row["constant"], row["frontier"], row["report"],
                      row["verdict"]))
    out += [
        "",
        "**Artifacts.** %d files, %d carrying a `CHECKSUMS` digest, **%d** "
        "mismatches, **%d** manifest lines naming a missing file; the only "
        "file with no digest anywhere is %s. The source-validation record "
        "names **%d** files and digests **%d** of them, reporting "
        "`status = %s` with **%d** issues, `json_parse_ok = %s`, "
        "`python_compile_ok = %s`, and **%d** per-file flag sets not fully "
        "true. %d files are absent from it: %s."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "none",
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"], af["validation_status"],
           af["validation_issue_entries"], af["validation_json_parse_ok"],
           af["validation_python_compile_ok"], af["validation_flags_not_true"],
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
        print(json.dumps({"tool": "src67_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src67_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
