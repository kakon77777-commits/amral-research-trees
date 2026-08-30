"""Emit RUN-040's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src59_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src59-au2d12.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src59-drill.json"
REPORT = ROOT / "reports" / "RUN-040-HARD-ZETA-AU2D12-TRANSPORT-HIERARCHY.md"
FIGURES = ROOT / "data" / "gate-logs" / "src59-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src59_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    # accept either the whole gate log or its `results` block, so
    # `emitter_guard_demo.py` -- which hands every emitter its raw log -- can
    # drive this one too. Every other gate in the tree puts its sections at the
    # top level; this one nests them, and the demo should not have to know.
    g = g.get("results", g)
    hi, rec, gen = g["hierarchy"], g["records"], g["generating"]
    ch, di, inh = g["chernoff"], g["diophantine"], g["inherited"]
    orb, cyl, pr = g["orbits"], g["cylinders"], g["premise_reach"]
    cs, cx = g["constants"], g["crossover"]
    led, ar, tc = g["ledger"], g["artifacts"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The block hierarchy, checked with integer arithmetic only.** "
        "`q_m = floor(beta m)` is `(3**m).bit_length() - 1`, so no logarithm "
        "enters: `C_m^-`, `gamma_m` and `alpha^_m` are exact rationals and "
        "either equal the published values or do not.",
        "",
        "| `m` | `q_m` | `alpha^_m` | beats `alpha_27` | `alpha^` float | `mu_m` |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in hi["rows"]:
        out.append("| %d | %d | `%s` | %s | %s | `%s` |" % (
            r["m"], r["q_floor"], r["alpha_hat"],
            "yes" if r["beats_alpha_27"] else "NO",
            "exact" if r["alpha_float_ulps"] == 0
            else "%+d ulp" % r["alpha_float_ulps"],
            r["mu_exact"]))
    out += [
        "",
        "%d levels. `q_m` disagreements **%d**, `C_m^-` **%d**, `gamma_m` "
        "**%d**, `alpha^_m` **%d**, and `alpha^_12 < alpha_27` holds (%d "
        "failures). Every `alpha_hat_float` is the nearest double to its own "
        "exact rational (%d off). Frontier, checker report and block-data file "
        "agree with each other (%d, %d disagreements)."
        % (hi["levels"], hi["q_floor_disagreeing_with_floor_beta_m"],
           hi["C_minus_disagreeing_with_the_binomial_sum"],
           hi["gamma_disagreeing_with_its_definition"],
           hi["alpha_hat_disagreeing_with_corollary_8_2"],
           hi["alpha_hat_12_not_below_alpha_27"],
           hi["alpha_hat_float_not_the_nearest_double"],
           hi["frontier_disagreeing_with_the_block_data"],
           hi["report_disagreeing_with_the_block_data"]),
        "",
        "**The record set.** Recomputing every level to `m = %d` gives **%d** "
        "running minima, and the shipped `record_minima_through_m150` list "
        "matches on every field (%d set disagreements, %d row disagreements). "
        "The sequence is genuinely not monotone: `alpha^` rose at **%d** of "
        "the %d levels. The smallest value reached is `%s`."
        % (rec["levels_recomputed"], rec["records_recomputed"],
           rec["record_set_disagreeing_with_the_report"],
           rec["record_rows_disagreeing_in_a_field"],
           rec["levels_where_alpha_rose"], rec["levels_recomputed"],
           rec["smallest_alpha_float"]),
        "",
        "**Lemma 10.1 by convolution, not by the closed form.** `3 C_m^- = "
        "Pr(G_1+...+G_m <= q_m)` was checked over %d levels by an exact "
        "convolution of the geometric law, which never mentions "
        "`binom(Q-1,m-1)` -- **%d** violations. The closed form itself was "
        "checked against brute-force enumeration of compositions on %d cases, "
        "**%d** disagreements."
        % (gen["levels"], gen["lemma_10_1_violations"],
           gen["compositions_enumerated"],
           gen["N_m_Q_disagreeing_with_composition_enumeration"]),
        "",
        "**The two halves of the closure.** Chernoff: `C_m^- <= (1/3)e^{-I_beta m}` "
        "over %d levels, **%d** violations, tightest at `m = %s` where the "
        "actual is %.3f of the bound -- so the inequality is not slack to the "
        "point of meaninglessness. The claimed optimum was checked "
        "independently: `-f(t)` exceeded `I_beta` at **%d** of %d grid points, "
        "and re-deriving `I_beta` through `e^{t*} = beta/(2(beta-1))` gives "
        "`%s` (%d identity violations). Diophantine: over %d block lengths, "
        "`eps+` left (0,1) **%d** times and `gamma_m >= (ln2) eps+` "
        "failed **%d**; the convexity step `2^x - 1 >= (ln2)x` failed **%d** "
        "of %d grid points."
        % (ch["levels"], ch["chernoff_capacity_violations"],
           ch["tightest_at_m"], ch["tightest_ratio"],
           ch["grid_points_beating_I_beta"], ch["grid_points"],
           ch["I_beta_from_t_star"], ch["optimum_identity_violations"],
           di["levels"], di["epsilon_plus_outside_the_unit_interval"],
           di["gamma_below_log2_times_epsilon_plus"],
           di["convexity_violations"], di["convexity_grid_points"]),
        "",
        "**Section 15 derives the formula RUN-039 had to fit.** `mu = "
        "(theta* - alpha)/(1 - alpha)` is exactly section 15's "
        "`(theta* - eps)/(1 - eps)`. Applied to the four inherited exponents "
        "`1/6`, `1/9`, `4/45`, `1373/25856` it reproduces all %d published "
        "source exponents, **%d** disagreements:"
        % (inh["exponents_checked"], inh["disagreeing_with_the_formula"]),
        "",
        "| inherited `alpha` | published `mu` | verdict |",
        "| --- | --- | --- |",
    ]
    for r in inh["rows"]:
        out.append("| `%s` | %s | %s |"
                   % (r["alpha"], r["published"], r["verdict"]["verdict"]))
    out += [
        "",
        "**On real orbits.** %d accelerated segments were built from %d "
        "sources, none with a repeated state (%d). Theorem 3.1 is an exact "
        "identity and was checked on **%d** sliding blocks: **%d** violations. "
        "Theorem 4.1 held on all %d summed balances (**%d**), Theorem 5.1 on "
        "all %d finance inequalities (**%d**), and Theorem 6.1 on **%d** exact "
        "words (**%d**)."
        % (orb["segments_built"], orb["starts_tried"],
           orb["segments_with_a_repeated_state"],
           orb["sliding_block_identities_checked"],
           orb["theorem_3_1_violations"], orb["summed_balances_checked"],
           orb["theorem_4_1_violations"], orb["finance_inequalities_checked"],
           orb["theorem_5_1_violations"], orb["exact_words_checked"],
           orb["theorem_6_1_violations"]),
        "",
        "**Section 1 states a weaker premise than section 4 uses.** Section 1 "
        "asks that every state *before* the endpoint be at least `y`; "
        "section 4 then bounds `sum 1/Y_n^2` over `n = 0..L`, endpoint "
        "included. Running Theorem 4.1 under section 1's reading -- same "
        "source, same bound, one extra state, the one below `y` -- gives "
        "**%d violations out of %d**. Under section 4's reading, %d."
        % (orb["theorem_4_1_violations_under_the_section_1_reading"],
           orb["loose_readings_available"], orb["theorem_4_1_violations"]),
        "",
        "**The premise sections 7-8 need is met once.** They require "
        "`L >= max{m,y}`. Scanning %d odd 3-free sources produced %d "
        "suffix-minimum segments, of which **%d** has `L >= y` (`y = %s`). "
        "Mean excursion length is %s and the longest anywhere in the range is "
        "%d, at `y = %d` -- the excursion above `y` grows like `log y` while "
        "`y` grows linearly. So Theorems 7.1, 8.1 and Corollary 8.2 were "
        "exercised %d times, and their zero violations are reported as the "
        "thin evidence they are, not as coverage."
        % (pr["sources_scanned"], pr["segments_built"],
           pr["segments_with_L_at_least_y"],
           ", ".join(str(q["y"]) for q in pr["qualifying_sources"]),
           pr["mean_excursion_length"], pr["longest_excursion"],
           pr["longest_excursion_at_y"], orb["theorem_8_1_checked"]),
        "",
        "**Source cylinders.** Section 6 says an exact exponent word of total "
        "valuation `Q` selects one source class mod `2^(Q+1)`, and at most two "
        "progressions mod `3*2^(Q+1)` after the 3-sieve. Over %d sources and "
        "%d distinct words (largest `Q` reached %d), words spanning more than "
        "one class: **%d**; more than two phases: **%d**. %d words had a "
        "single source and could not have disagreed, leaving %d that could."
        % (cyl["sources_scanned"], cyl["words_seen"], cyl["largest_Q_reached"],
           cyl["words_spanning_more_than_one_class_mod_2Qplus1"],
           cyl["words_spanning_more_than_two_classes_mod_3_2Qplus1"],
           cyl["words_with_only_one_source_seen"],
           cyl["words_seen"] - cyl["words_with_only_one_source_seen"]),
        "",
        "**Where the certificate actually overtakes the old one.** "
        "Corollary 8.2 is `P <= exp(B_m/3)(L/y)^{alpha^_m}`, and the exponents "
        "do fall. The additive constants rise faster. Giving A-U.2d.11 the "
        "most generous possible constant -- zero -- the crossover is:",
        "",
        "| `m` | `B_m` (recomputed) | `log10(L/y)` before the new exponent wins |",
        "| --- | --- | --- |",
    ]
    bm = {r["m"]: r for r in hi["rows"]}
    for r in cx["rows"]:
        out.append("| %d | `%s` | %s |"
                   % (r["m"], bm[r["m"]]["B_m_bracket"],
                      r["log10_of_L_over_y_at_crossover"]))
    out += [
        "",
        "Measured on the one segment that meets the premise, Corollary 8.2's "
        "bound exceeds the actual product by these orders of magnitude, by "
        "block length: `%s`. Their own report renders the same ratio at "
        "`m = 12` as `0.0`, which is a float64 underflow rather than a "
        "measurement." % json.dumps(orb["slack_log10_by_m"]),
        "",
        "**Constants and their provenance.** `beta` is the nearest double "
        "(%d off). `I_beta` is `%s` and the published 15 digits are %s. "
        "`theta*` is where a rounding enters: `rho* = 4.1164` makes "
        "`theta* = 1/(rho*+1)` the exact rational `%s`, whose nearest double "
        "is `%s`, but the artifact ships `%s` -- which is what "
        "`1/(1 + float(4.1164))` evaluates to, because `float(4.1164)` is "
        "`4.11639999999999961...`. That single rounding is inherited by all "
        "%d `dense_source_floor_mu` values: each matches the float64 chain at "
        "0 ulps and the exact rational at 1 (2 at `m = 48`). Formula "
        "disagreements: **%d**."
        % (cs["beta_float_not_the_nearest_double"],
           cs["rows"][1]["bracket_to_18_places"],
           cs["I_beta_decimal_verdict"]["verdict"],
           cs["theta_star_exact"],
           cs["rows"][0]["nearest_double_to_the_exact_rational"],
           cs["rows"][0]["published"],
           hi["mu_matching_the_float64_chain_not_the_exact_rational"],
           cs["theta_star_disagreeing_with_both_evaluations"]),
        "",
        "**Artifacts.** %d files, %d carrying a digest, **%d** mismatches, "
        "**%d** manifest lines naming a file that is not there. The one file "
        "with no digest anywhere is `%s`. RUN-039's finding is fixed: the "
        "builder `build_AU2d12_artifacts.py` **is** covered this time (%s). "
        "The validation record still carries no digests of its own -- %d of "
        "its entries list a file without one."
        % (ar["files_present"], ar["digests_listed"], ar["digest_mismatches"],
           ar["checksum_lines_naming_a_missing_file"],
           ", ".join(ar["files_with_no_digest_anywhere"]),
           ar["builder_covered_by_a_digest"],
           ar["validation_entries_without_a_digest"]),
        "",
        "**Ledger coverage.** The paper lists %d proved items, %d explicitly "
        "open problems and %d numbered NO-GO headings. The ledger carries %d, "
        "%d and %d. It still has no `open` key of any kind -- the second round "
        "running. Open items with no trace in it: %s. NO-GO headings with no "
        "trace: %s."
        % (led["paper_proved_items"], led["paper_open_items"],
           led["paper_no_go_headings"], led["ledger_proved_items"],
           led["ledger_open_items"], led["ledger_no_go_items"],
           json.dumps(led["open_items_absent_from_the_ledger"]),
           json.dumps(led["no_go_headings_absent_from_the_ledger"]) or "none"),
        "",
        "**Their counters beside mine.** Different populations, so a "
        "difference is information rather than a fault; %d of their checks "
        "had no counterpart here." % tc["checks_i_did_not_reproduce"],
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
        "**Drill.** %d defects planted one at a time, **%d caught**, %d "
        "malformed, %d missed; %d were caught only by a counter other than the "
        "one aimed at. All %d anchors matched exactly one place before "
        "anything was planted. %d of %d controls undisturbed. The gate came "
        "back byte-identical."
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
                          "failures": g.get("failures"),
                          "guards": g.get("empty_populations")},
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
        print(json.dumps({"tool": "src59_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src59_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
