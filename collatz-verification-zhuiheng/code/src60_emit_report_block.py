"""Emit RUN-041's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src60_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src60-au2d13.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src60-drill.json"
REPORT = ROOT / "reports" / "RUN-041-HARD-ZETA-AU2D13-SOURCE-DEPTH-COLLISION.md"
FIGURES = ROOT / "data" / "gate-logs" / "src60-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src60_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ex, idn, mn = g["exponents"], g["identities"], g["means"]
    ov, cf, orb = g["overlap"], g["cf_local"], g["orbits"]
    loc, pr = g["localization"], g["printed"]
    ar, led, tc = g["artifacts"], g["ledger"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The constants family is one rational parameter.** Taking the "
        "paper's own `rho* = 4.1164` and `theta* = 1/(rho*+1)` at face value, "
        "every headline exponent has an exact closed form -- two of which the "
        "paper never states:",
        "",
        "| constant | closed form | exact rational | published | vs exact | vs float64 chain |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    forms = {
        "theta_star": "1/(rho*+1)",
        "old_disjoint_backbone_sigma_star": "**1/(1+theta*)**",
        "unconditional_support_exponent_kappa13": "**1/(1+theta*^2)**",
        "unconditional_log_exponent_lambda13": "kappa13 * theta*",
        "pq_pressure_at_old_sigma": "(5 sigma* - 4)/3",
        "controlled_CF_support_exponent": "2 / (5/2)",
        "controlled_CF_log_exponent": "1 / (5/2)",
        "support_PQ_factor_exponent": "(3/2) / (5/2)",
    }
    for r in ex["rows"]:
        out.append("| `%s` | %s | `%s` | %s | %s | %s |" % (
            r["name"], forms.get(r["name"], "—"), r["exact"], r["published"],
            "exact" if r["ulps_vs_exact"] == 0
            else "%+d ulp" % r["ulps_vs_exact"],
            "exact" if r["ulps_vs_float64_chain"] == 0
            else "%+d ulp" % r["ulps_vs_float64_chain"]))
    out += [
        "",
        "%d constants checked. **%d** disagree with both readings of their own "
        "formula, **%d** are the nearest double to the exact rational, and "
        "**%d** are what the same formula gives when evaluated in float64 from "
        "an already-rounded parent. `chi*` is the outlier at %+d ulps, and the "
        "reason is arithmetic rather than error: `5 sigma* - 4` collapses "
        "4.18 to 0.18, a **%s-fold** loss of magnitude that turns `sigma*`'s "
        "single ulp into about that many. Its allowed budget here is derived "
        "from that factor (%d ulps), not chosen."
        % (ex["constants_checked"], ex["disagreeing_with_both_evaluations"],
           ex["exact_to_the_last_bit"],
           ex["from_the_float64_chain_not_the_exact_rational"],
           [r["ulps_vs_exact"] for r in ex["rows"]
            if r["name"] == "pq_pressure_at_old_sigma"][0],
           ex["cancellation_factor_in_five_sigma_minus_four"],
           ex["ulp_budget_allowed_for_chi_star"]),
        "",
        "**The exponent algebra, as identities rather than at one point.** "
        "Section 7 assembles `M^(rho+1+th)/N^(rho+1)` out of `r ~ M^(1+th)/N` "
        "and `S ~ M^th`, which is the identity `(1+th)(rho+1) - th*rho = "
        "rho+1+th`; section 8 assembles `M^(5/2)/(A^(3/2) N^2)`. Checking "
        "either at the paper's own `(rho, theta)` would prove nothing about "
        "the transcription, so both were evaluated over %d random rational "
        "parameter pairs: **%d** and **%d** violations. Solving the support "
        "inequality for `kappa` and inverting the CF master for the "
        "partial-quotient exponent gave **%d** and **%d**. The named instances "
        "come out `%s`, `%s`, `%s` and `%s`."
        % (idn["trials"], idn["section_7_exponent_identity_violations"],
           idn["section_8_exponent_identity_violations"],
           idn["kappa_from_the_support_inequality_violations"],
           idn["pq_exponent_from_inversion_violations"],
           idn["kappa13_from_the_formula"], idn["chi_at_sigma_star"],
           idn["four_fifths_from_the_CF_master"],
           idn["pq_exponent_at_kappa_one"]),
        "",
        "**The convexity steps.** Section 7 needs Jensen for `x^-rho` and "
        "section 8 the AM-HM case. Over %d tuples: **%d** and **%d** "
        "violations, with %d forced equal-gap tuples where both sides meet "
        "exactly -- the only place a wrong exponent would still pass. The "
        "paper's own `rho*` was then checked separately through certified "
        "brackets on %d tuples: **%d** violations, **%d** undecided."
        % (mn["tuples"], mn["jensen_violations"], mn["am_hm_violations"],
           mn["equal_gap_cases"], mn["tuples_at_rho_star"],
           mn["jensen_violations_at_rho_star"], mn["undecided_at_rho_star"]),
        "",
        "**The localization lemma.** Lemma 5.1 -- intervals of length `>= 4W` "
        "with starts inside one window of width `W` all contain the latest "
        "start -- held on %d random families, **%d** violations. Its control "
        "matters more: shortening the same intervals below the window width "
        "broke the overlap in %d of %d families, so the lemma is not passing "
        "because it cannot fail. The pigeonhole behind Lemma 5.2 was checked "
        "by construction rather than by formula on %d families, **%d** "
        "violations."
        % (ov["families"], ov["lemma_5_1_violations"],
           ov["short_families_tried"] - ov["short_families_that_still_overlap"],
           ov["short_families_tried"], ov["pigeonhole_trials"],
           ov["pigeonhole_violations"]),
        "",
        "**The one arithmetic input, decided from the exact continued "
        "fraction.** Section 4.2 needs `||q beta|| > 1/((M_beta(N)+2) q)` for "
        "every `q <= N`. The partial quotients of `log2 3` come from `src47`'s "
        "integer-comparison route, so no logarithm decides anything; only the "
        "final comparison uses a sixty-digit bracket against a gap near "
        "`1e-7`. Across %d scales and **%d** values of `q`: **%d** violations, "
        "**%d** undecided. The bound is not slack -- at its tightest, "
        "`q*||q beta||*A_N` comes to **%.4f**, at `N = %s`, `q = %s`."
        % (cf["scales"], cf["q_values_scanned"],
           cf["local_cf_bound_violations"], cf["undecided_brackets"],
           cf["tightest_ratio"], cf["tightest_at"][0], cf["tightest_at"][1]),
        "",
        "| `N` | `M_beta(N)` | `A_N` | tightest `q` | `q ||q beta|| A_N` |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in cf["rows"]:
        out.append("| %d | %d | %d | %s | %.4f |"
                   % (r["N"], r["M_beta_N"], r["A_N"], r["tightest_q"],
                      r["q_times_norm_times_A"]))
    out += [
        "",
        "**On real orbits, the object of the round does not occur.** A "
        "B-injection is a first coefficient crossing with `Y_{e(s)} > Y_s`. "
        "Across %d first-crossing intervals from %d orbits there are **%d** of "
        "them; the closest any interval gets is `z/y = %s` (orbit %s, "
        "`y = %s`, `L = %s`). That is a fact about convergent orbits, not a "
        "defect -- the theorems are about the hypothetical divergent branch -- "
        "but it means Theorems 4.1 and 6.1 cannot be exercised here, and their "
        "zero violations would be vacuous. What is testable everywhere was "
        "tested instead."
        % (orb["first_crossing_intervals"], orb["orbits_used"],
           orb["B_injections"], orb["largest_z_over_y_reached"]["ratio"],
           orb["largest_z_over_y_reached"]["orbit"],
           orb["largest_z_over_y_reached"]["y"],
           orb["largest_z_over_y_reached"]["L"]),
        "",
        "The exact product identity `z 2^Q = y 3^L prod(1+1/(3Y_j))`, written "
        "with no `beta` at all, held on all %d intervals (**%d** violations), "
        "and so did the equivalence that turns B-survival into an inequality "
        "on `D` (**%d**). `D > 0` at every first crossing (**%d** failures). "
        "Section 4.2's unconditional slack floor `D > 1/(A_N L)` was checked "
        "on **%d** intervals: **%d** violations. Theorem 4.1's algebra was "
        "exercised on the **%d** intervals where its antecedent actually "
        "holds: **%d** violations."
        % (orb["first_crossing_intervals"],
           orb["exact_product_identity_violations"],
           orb["survival_equivalence_violations"],
           orb["D_not_positive_at_a_first_crossing"],
           orb["local_cf_slack_checked"], orb["local_cf_slack_violations"],
           orb["survival_duration_antecedent_holds"],
           orb["theorem_4_1_algebra_violations"]),
        "",
        "A denominator worth stating plainly: of %d suffix-minimum "
        "first-crossing sources, %d fall outside `7, 11 mod 12`. That is **not** "
        "a counterexample to A-U.2d.9's residue law, which is about B sources, "
        "of which there are none. It is the size of the gap between the "
        "population the law constrains and the population a real orbit offers."
        % (orb["suffix_minimum_sources_checked"],
           orb["suffix_minimum_sources_outside_7_or_11_mod_12"
               "_not_a_counterexample"]),
        "",
        "**The conditional theorems as algebra.** Over %d synthetic parameter "
        "points: Theorem 4.1 **%d** violations (antecedent satisfiable at %d "
        "of them), the unconditional duration floor **%d** (%d), the section 6 "
        "corridor implication **%d** of %d, and Lemma 5.2's pigeonhole **%d** "
        "of %d."
        % (loc["grid_points"], loc["theorem_4_1_violations"],
           loc["theorem_4_1_antecedent_satisfiable"],
           loc["duration_floor_violations"],
           loc["duration_floor_antecedent_holds"],
           loc["corridor_implication_violations"],
           loc["corridor_implication_points"], loc["pigeonhole_violations"],
           loc["pigeonhole_points"]),
        "",
        "**What the prose prints.** %d decimal instances of these five "
        "constants appear across the paper and route map, **all %d of them "
        "followed by an ellipsis** -- which asserts the digits shown are "
        "correct and more follow. **%d** are over-published against the exact "
        "rational, %d are exact to every digit, and %d is truncated rather "
        "than rounded. `lambda13` is the only constant printed correctly "
        "everywhere it appears."
        % (pr["printed"], pr["printed_with_an_ellipsis"], pr["over_published"],
           pr["exact_to_every_digit"], pr["truncated"]),
        "",
        "**Artifacts.** %d files, %d carrying a digest, **%d** mismatches, "
        "**%d** manifest lines naming a file that is not there; the only file "
        "with no digest anywhere is `%s`, which cannot pin itself. The "
        "validation record lists %d files and **%d of them carry no hash** -- "
        "it records `checker_reran = %s`, `commit_gate_passed = %s` and "
        "`issues = %s` instead. That is the third round running with a "
        "digest-free validation record."
        % (ar["files_present"], ar["digests_listed"], ar["digest_mismatches"],
           ar["checksum_lines_naming_a_missing_file"],
           ", ".join(ar["files_with_no_digest_anywhere"]),
           ar["validation_files_listed"],
           ar["validation_entries_without_a_digest"],
           ar["validation_reports_its_checker_reran"],
           ar["validation_commit_gate_passed"],
           json.dumps(ar["validation_issues"])),
        "",
        "**Ledger coverage — the finding from the last two rounds is fixed.** "
        "The paper lists %d proved items, %d explicitly open problems and %d "
        "numbered NO-GO headings; the ledger carries %d, %d and %d. It **has "
        "an `open` key** this time (%s), and all %d open items are present, "
        "the Collatz conjecture among them. NO-GO headings with no trace in "
        "it: %s."
        % (led["paper_proved_items"], led["paper_open_items"],
           led["paper_no_go_headings"], led["ledger_proved_items"],
           led["ledger_open_items"], led["ledger_no_go_items"],
           led["ledger_has_an_open_key"], led["paper_open_items"],
           json.dumps(led["no_go_headings_absent_from_the_ledger"])
           if led["no_go_headings_absent_from_the_ledger"] else "none"),
        "",
        "**Their counters beside mine.** Different populations, so a "
        "difference is information rather than a fault; %d of their checks had "
        "no counterpart here." % tc["checks_i_did_not_reproduce"],
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
        print(json.dumps({"tool": "src60_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src60_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
