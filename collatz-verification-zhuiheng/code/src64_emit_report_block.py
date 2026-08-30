"""Emit RUN-045's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src64_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src64-au2d17.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src64-drill.json"
REPORT = ROOT / "reports" / "RUN-045-HARD-ZETA-AU2D17-SMALL-ENDPOINT-CYLINDER.md"
FIGURES = ROOT / "data" / "gate-logs" / "src64-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src64_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, br = g["instrument"], g["constants"], g["bridges"]
    ca, pl, ar = g["canonical"], g["plateau"], g["area"]
    fh, tg, ex = g["first_hit"], g["their_guards"], g["examples"]
    rc, en = g["records"], g["entropy"]
    af, led, tc = g["artifacts"], g["ledger"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The affine relation, in integers.** Section 5's Endpoint-Laplace "
        "identity multiplied by `2^Q` is term-by-term the definition of "
        "`B_w`, so the identity carries no information on its own; the "
        "content is `2^Q Z = 3^h X + B_w` on real orbit data. Across **%d** "
        "bridges from **%d** distinct sources (longest tail %d): **%d** "
        "affine violations, **%d** disagreements with the closed form for "
        "`B_w`, **%d** violations of the published rational form, **%d** "
        "non-positive Laplace sums. Every suffix supercritical on **%d** "
        "suffixes: **%d**. Lemma 8.2's correction floor **%d**. Theorem 8.3, "
        "as the rational inequality `2^Q/3^h >= 1 + (5-(2/3)^h)/Z` rather "
        "than the bundle's float64 form with its `1e-12` fudge: **%d** "
        "violations, tightest slack **%s**, and the fudge changed the verdict "
        "on **%d** of them."
        % (br["bridges"], br["sources"], br["longest_tail"],
           br["affine_identity_violations"],
           br["b_w_not_matching_the_closed_form"],
           br["laplace_identity_violations"], br["laplace_sum_not_positive"],
           br["suffixes_checked"], br["suffix_not_supercritical"],
           br["correction_floor_violations"],
           br["excess_floor_theorem_8_3_violations"],
           ("%.6f" % br["smallest_excess_floor_slack"]),
           br["excess_floor_decided_by_the_float64_fudge"]),
        "",
        "**The phases, and the integer lift.** Source outside `11, 17 mod 18` "
        "**%d**; endpoint outside `7, 11 mod 12` **%d**; endpoint not below "
        "the source **%d**; Lemma 8.1's `X-Z >= 4` **%d**, with the smallest "
        "gap actually seen **%d** — the residue argument admits 4 and nothing "
        "near it occurs. The integer lift `m_h = Q - ceil(beta h)` was "
        "negative **%d** times and **zero on %d of %d** bridges, so every "
        "finite bridge sits at the first critical integer and its excess IS "
        "the one-sided phase; the phase left the unit interval **%d** times."
        % (br["source_outside_11_or_17_mod_18"],
           br["endpoint_outside_7_or_11_mod_12"],
           br["endpoint_not_below_the_source"], br["phase_gap_violations"],
           br["smallest_phase_gap_seen"], br["integer_lift_negative"],
           br["integer_lift_zero"], br["bridges"],
           br["one_sided_phase_outside_the_unit_interval"]),
        "",
        "**Double-canonical collapse, with the guard counted.** The "
        "congruences hold for every word; the collapse to equality needs the "
        "smallness, and the shipped checker tests both behind one `if`. Here "
        "the congruence is checked on all **%d** bridges — **%d** source and "
        "**%d** endpoint violations — while the source lies inside its "
        "modulus on **%d**, the endpoint on **%d**, and both on **%d** "
        "(%s). Theorem 4.1's equality on those: **%d** violations, **%d** "
        "representatives failing their own defining congruence, and **%d** "
        "cases where the collapse would have been claimed outside the moduli."
        % (ca["bridges"], ca["source_congruence_violations"],
           ca["endpoint_congruence_violations"],
           ca["source_inside_its_modulus"], ca["endpoint_inside_its_modulus"],
           ca["both_inside_their_moduli"],
           pct(ca["both_inside_their_moduli"], ca["bridges"]),
           ca["collapse_violations"],
           ca["representative_does_not_satisfy_its_congruence"],
           ca["collapse_asserted_outside_the_moduli"]),
        "",
        "**Jensen on real bridges, as an integer inequality.** "
        "`2^{sum H_i} = 2^A / 3^{h(h+1)/2}` because the triangular number is "
        "an integer, so Theorem 6.1 is `2^A S^h >= h^h 3^{h(h+1)/2}`. On "
        "**%d** bridges: **%d** violations. Corollary 5.2's `S < 3Z` **%d**, "
        "and the elementary `S < h` **%d**. The published weaker form "
        "`avg H > log2(h/3Z)` has a **positive right side on %d of %d** "
        "bridges — below that it states nothing — while the exact form is "
        "live on every one. Theorem 6.2 was exercised on **%d** instances "
        "with **%d** violations, of which **%d** were non-vacuous; replacing "
        "the `3Z` by the `S` it bounds gives **%d** non-vacuous instances, "
        "**%d** violations."
        % (pl["bridges"], pl["jensen_theorem_6_1_violations"],
           pl["laplace_sum_not_below_three_z"], pl["laplace_sum_not_below_h"],
           pl["jensen_weaker_bound_with_a_positive_right_side"], pl["bridges"],
           pl["quantile_instances"], pl["quantile_theorem_6_2_violations"],
           pl["quantile_instances_that_are_not_vacuous"],
           pl["sharp_quantile_instances_that_are_not_vacuous"],
           pl["sharp_quantile_violations"]),
        "",
        "**The weighted area is an identity; its components are not.** Both "
        "sides of Theorem 7.1 reduce to `A - beta h(h+1)/2`, so the bundle's "
        "float64 comparison with a `1e-10` tolerance compares a quantity with "
        "itself. The two pieces that can be wrong are integer statements: the "
        "rearrangement `sum_i (Q - P_i) = sum_k k q_k` **%d** violations and "
        "the triangular sum **%d**, with the surplus total **%d**. Theorem "
        "7.2's finite content is `2(A - M) >= (h+1)(Q - h)`: **%d** bridges "
        "below the midpoint, **%d exactly at it** — attained on every "
        "single-step bridge, where `k` can only be 1 — and **%d** past it, "
        "the largest excess %s positions."
        % (ar["rearrangement_violations"], ar["triangular_sum_violations"],
           ar["surplus_total_not_q_minus_h"],
           ar["centre_of_mass_before_the_midpoint"],
           ar["centre_of_mass_exactly_at_the_midpoint"],
           ar["centre_of_mass_past_the_midpoint"],
           ("%.3f" % ar["largest_midpoint_excess_seen"])),
        "",
        "**The first-hit slice needs no `O(1)`.** `2^{delta_v - delta_s} = "
        "3^{v-s}/2^{K_v-K_s}`, so every inequality in section 10 is a "
        "comparison of integers. Over **%d** orbits, **%d** reached the "
        "threshold: **%d** below it, **%d** not minimal, **%d** overshooting "
        "more than one step's slack gain, **%d** violating the length bound, "
        "**%d** slack-step ratio disagreements, **%d** prefix valuations "
        "below the length and **%d** disagreeing with the cumulative sum. The "
        "published `ell >= lambda/(beta-1) log2 N + O(1)` needs no additive "
        "constant: it reduces to `K_v - K_s >= v - s`, and the bound is "
        "**attained on %d** of the %d. Theorem 10.1's containment is "
        "asymptotic and at these scales holds for a minority — source inside "
        "its cylinder **%d**, outside **%d**; endpoint inside **%d**, outside "
        "**%d** — the largest N still outside being %s."
        % (fh["orbits"], fh["first_hits"], fh["first_hit_below_the_threshold"],
           fh["first_hit_not_minimal"], fh["overshoot_above_one_step"],
           fh["length_bound_violations"], fh["slack_step_ratio_violations"],
           fh["prefix_valuation_below_the_length"],
           fh["prefix_valuation_not_matching_the_cumulative_sum"],
           fh["length_bound_attained_with_no_additive_constant"],
           fh["first_hits"], fh["source_inside_its_cylinder"],
           fh["source_outside_its_cylinder"],
           fh["endpoint_inside_its_cylinder"],
           fh["endpoint_outside_its_cylinder"],
           fh["largest_n_with_the_source_outside"]),
        "",
        "**Their own counters increment once per sample, not once per "
        "assertion.** All three of the shipped checker's assertion sites sit "
        "behind an `if`. Reimplementing its sampling scheme independently at "
        "its stated parameters: of **%d** residue samples the source formula "
        "is actually tested on **%d** (%s) and the endpoint formula on **%d** "
        "(%s), with **%d** and **%d** violations where they do fire. Of "
        "**%d** quantile samples the Jensen assertion runs on **%d** (%s) — "
        "its `if h > 3Z` guard — and the Markov bound is non-trivial on "
        "**%d** (%s); **%d** and **%d** violations."
        % (tg["residue_samples"], tg["residue_source_assert_fired"],
           pct(tg["residue_source_assert_fired"], tg["residue_samples"]),
           tg["residue_endpoint_assert_fired"],
           pct(tg["residue_endpoint_assert_fired"], tg["residue_samples"]),
           tg["residue_source_violations"], tg["residue_endpoint_violations"],
           tg["quantile_samples"], tg["quantile_jensen_guard_open"],
           pct(tg["quantile_jensen_guard_open"], tg["quantile_samples"]),
           tg["quantile_bound_not_vacuous"],
           pct(tg["quantile_bound_not_vacuous"], tg["quantile_samples"]),
           tg["quantile_jensen_violations"], tg["quantile_markov_violations"]),
        "",
        "**The record-gap population, where the phase hypotheses apply.** "
        "The bundle's bridges are local cylinder witnesses, not orbit records "
        "— one source can contribute several, and its own example list does. "
        "On **%d** genuine consecutive suffix-minimum gaps from **%d** "
        "sources: affine **%d**, Laplace **%d**, `X-Z>=4` **%d**, endpoint "
        "phase **%d**, `Z = 3 mod 4` **%d** (the condition that needs the "
        "record structure rather than the word), and **%d** violations across "
        "**%d** suffixes. Smallest gap seen %d."
        % (rc["gaps"], rc["sources"], rc["affine_identity_violations"],
           rc["laplace_identity_violations"], rc["phase_gap_violations"],
           rc["endpoint_outside_7_or_11_mod_12"],
           rc["endpoint_not_three_mod_four"], rc["suffix_not_supercritical"],
           rc["suffixes_checked"], rc["smallest_phase_gap_seen"]),
        "",
        "**All ten published finite examples, rebuilt from the map.** **%d** "
        "disagreeing values of `X`, **%d** of `Z`, **%d** exponent words, "
        "**%d** lengths, **%d** first steps not of valuation one, **%d** "
        "Laplace sums, **%d** excess decimals, **%d** phase floors, **%d** "
        "tails not suffix-supercritical, **%d** geometry violations. **%d** "
        "source appears more than once — `y = 155` reaches both `Z = 175` and "
        "`Z = 167`, and at most one of those can be its next record."
        % (ex["x_disagreeing"], ex["z_disagreeing"],
           ex["exponent_word_disagreeing"], ex["h_disagreeing"],
           ex["first_step_not_valuation_one"], ex["laplace_sum_disagreeing"],
           ex["excess_decimal_disagreeing"], ex["phase_floor_disagreeing"],
           ex["tail_not_suffix_supercritical"], ex["geometry_violations"],
           ex["sources_appearing_more_than_once"]),
        "",
        "| `y` | `X` | `Z` | `h` | word | `sum 2^-H_i` | `X - Z` |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in ex["rows"]:
        out.append("| %d | %d | %d | %d | `%s` | `%s` | %d |"
                   % (row["y"], row["X"], row["Z"], row["h"],
                      row["word"], row["laplace_sum"], row["X_minus_Z"]))
    out += [
        "",
        "**NO-GO 11.1's entropy rate, watched converging.** `log2 C(Q-1,h-1)/h "
        "-> e_beta` at `Q = ceil(beta h)`, over **%d** levels: **%d** where "
        "the gap to `e_beta` failed to shrink, **%d** where the rate exceeded "
        "`beta`, which would be impossible."
        % (en["levels"], en["gap_not_shrinking"], en["entropy_rate_above_beta"]),
        "",
        "| `h` | `Q = ceil(beta h)` | rate | gap to `e_beta` |",
        "| --- | --- | --- | --- |",
    ]
    for row in en["rows"]:
        out.append("| %d | %d | %s | %.4f |"
                   % (row["h"], row["Q"], row["rate"], row["gap_to_e_beta"]))
    out += [
        "",
        "**Constants.** %d checked: **%d** disagree with both readings of "
        "their own formula, %d are the nearest double, %d are what the same "
        "formula gives in float64, %d brackets could not decide. Each budget "
        "is `4 x (largest operand / result)` — the factor by which the "
        "formula magnifies one ulp of its inputs — and the budget is tested "
        "BEFORE the chain excuse."
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
        "file with no digest anywhere is %s. No two files carry the same "
        "bytes — `CHECKER_STDOUT_AU2d17.txt` is the checker report plus "
        "%s, where RUN-044's was byte-identical to it. The source-validation "
        "record names **%d** files and digests **%d** of them (**%d** digest "
        "mismatches, **%d** size mismatches), reports `all_ok = %s` with "
        "**%d** issues, a compile return code of %s and an execution return "
        "code of %s, and its nine counter values disagree with the checker "
        "report **%d** times. %d files are absent from it: %s."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "none",
           # the log stores a bytes repr; render the common case in words
           # rather than pasting `b'\\n'` into prose
           ("a single trailing newline"
            if af["stdout_extra_bytes"] == repr(b"\n")
            else "the trailing bytes %s" % af["stdout_extra_bytes"]),
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           af["validation_digest_mismatches"], af["validation_size_mismatches"],
           af["validation_all_ok_flag"], af["validation_issue_entries"],
           af["validation_compile_returncode"],
           af["validation_execution_returncode"],
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
        "**%d are reproduced exactly** from the definition. The ninth is not "
        "a disagreement: `random_exact_residue_checks` is a sample size, and "
        "mine is larger."
        % (tc["checks_i_did_not_reproduce"], len(tc["rows"]),
           tc["checks_they_report_as_zero"], tc["counts_i_reproduce_exactly"]),
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
        print(json.dumps({"tool": "src64_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src64_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
