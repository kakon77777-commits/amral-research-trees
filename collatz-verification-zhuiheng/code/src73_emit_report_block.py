"""Emit RUN-054's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src73_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src73-au2d26.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src73-drill.json"
REPORT = ROOT / "reports" / "RUN-054-HARD-ZETA-AU2D26-UNIT-SYNC.md"
FIGURES = ROOT / "data" / "gate-logs" / "src73-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src73_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    tp, sy, va = g["transport"], g["sync_toll"], g["variation"]
    cf, ma, xp = g["cf"], g["masters"], g["exponent"]
    ex, af, led = g["examples"], g["artifacts"], g["ledger"]
    tc = g["their_claims"]
    tot = d["totals"]

    out = [
        BEGIN, "",
        "**The population.** Deterministic again — five moduli, odd sources "
        "below 9000 not divisible by three, thirteen edges per orbit — so it "
        "reproduces exactly: **%d** quotient-active edges from **%d** start "
        "states, **%d** malformed, **%d** unclassified. By type: **%d** zero, "
        "**%d** synchronized, **%d** binary-exclusive, **%d** "
        "ternary-exclusive."
        % (pop["edges"], pop["sources"], pop["malformed_edges"],
           pop["unclassified"], pop["zero"], pop["sync"],
           pop["binary_exclusive"], pop["ternary_exclusive"]),
        "",
        "**Theorem 3.1's transport identity, exact.** They assert it in "
        "float64 with a `2e-11` tolerance. Checked as an exact `Fraction` on "
        "all **%d** edges: **%d** violations. The largest float error their "
        "tolerance was covering is of order **1e%d** — their allowance is "
        "**%d times** the error it needed to absorb, on a statement that is "
        "exact in rationals and needs no allowance at all. At their own "
        "tolerance, **%d** violations."
        % (tp["edges"], tp["exact_transport_violations"],
           tp["largest_float_error_exponent"],
           tp["their_tolerance_over_the_largest_error"],
           tp["float_transport_violations_at_their_tolerance"]),
        "",
        "**Their synchronized reservoir toll: three clauses, all definitional.** "
        "Over **%d** synchronized edges the three asserted clauses — `c₃ ≥ 1`, "
        "`B ≥ c₃ − 1`, `n ≥ 3^{c₃−1}` — failed **%d**, **%d** and **%d** "
        "times. None of them can fail. `c₃ > 0` is the branch condition and "
        "`c₃` is an integer, so the first restates it; `c₃ = 1 + B − B′` makes "
        "the second exactly `B′ ≥ 0`, which a 3-adic valuation always is "
        "(**%d** negative in the whole population); and `3^B | n` with the "
        "second gives the third. Measured rather than asserted: over **%d** "
        "predicate comparisons, the depth clause disagreed with `B′ ≥ 0` "
        "**%d** times and the `c₃` clause disagreed with its own branch **%d** "
        "times. Largest synchronized `c₃` seen: **%d**."
        % (sy["sync_edges"], sy["c3_below_one"],
           sy["reservoir_depth_violations"], sy["quotient_floor_violations"],
           sy["output_ternary_valuation_negative"],
           sy["predicate_pairs_compared"],
           sy["reservoir_depth_disagreeing_with_a_nonneg_valuation"],
           sy["c3_at_least_one_disagreeing_with_the_branch"],
           sy["largest_sync_c3"]),
        "",
        "**The variation-transfer bound, implied term by term.** Their window "
        "check sums three lists and compares totals. By Theorem 3.1, "
        "`|ΔU| − |c₂ − βc₃|` is bounded by `|ε|` on each single edge by the "
        "reverse triangle inequality, so the summed form follows. Measured per "
        "term over **%d** edges: **%d** with negative slack. Over **%d** "
        "windows the aggregate failed **%d** times. The control — one edge's "
        "unit ratio replaced by an unrelated value — makes it fail on **%d of "
        "%d** windows, so the assertion has content that their construction "
        "cannot exercise."
        % (va["terms"], va["terms_with_negative_slack"], va["windows"],
           va["window_violations"], va["broken_window_failures"],
           va["broken_windows"]),
        "",
        "**Lemma 7.1, certified in exact rationals.** Their checker takes "
        "β's continued fraction from a 90-digit float. Here the terms come "
        "from the certified rational bracket: a term is emitted only while "
        "both endpoints agree on it, so every emitted term is a term of every "
        "number in the interval, hence of β. That yields **%d** certified "
        "partial quotients against the **%d** they publish, giving "
        "`M_β(D) = %d` and `Q_D = %d` at `D = 20000`, with the largest "
        "convergent denominator at or below `D` being **%d**. The separation "
        "`|a − βb| > 1/(Q_D b)` was then decided by integer "
        "cross-multiplication — no floating point anywhere — over **%d** "
        "values of `b`: **%d** violations and **%d** values the bracket could "
        "not decide. The bound is nearly attained: the tightest "
        "`|a − βb|·Q_D·b` is **%s**."
        % (cf["certified_partial_quotients"], cf["published_prefix_length"],
           cf["m_beta_at_D"], cf["q_local"],
           cf["largest_convergent_denominator_at_or_below_D"],
           cf["b_values_tested"], cf["separation_violations"],
           cf["b_values_the_bracket_could_not_decide"],
           cf["tightest_separation_ratio"]),
        "",
        "**Theorems 8.1 and 9.1, and two blocks counted twice.** The two CF "
        "master inequalities held over **%d** batches: **%d** and **%d** "
        "violations. They come from one block that increments **%d** "
        "counters. The monotone-run and coarea lemmas likewise share one "
        "block incrementing **%d** counters, and their assertions sit inside "
        "a guard the counters are outside: over **%d** trials the guard "
        "opened **%d** times. Violations: **%d** monotone-run, **%d** coarea "
        "identity, **%d** coarea crossing."
        % (ma["batches"], ma["gate_count_master_violations"],
           ma["workload_depth_master_violations"],
           ma["counters_their_block_increments"],
           ma["run_counters_their_block_increments"], ma["run_trials"],
           ma["run_guard_opened"], ma["monotone_run_violations"],
           ma["coarea_identity_violations"],
           ma["coarea_max_crossing_violations"]),
        "",
        "**Their exponent block asserts what its own guard already gives.** "
        "The code reads `if not (lhs >= 1 − 1e-12): assert lhs < 1 + 1e-12`. "
        "The branch condition is strictly stronger than the assertion, so the "
        "assertion cannot fail. Over **%d** trials, **%d** samples reached the "
        "assert and **%d** of them had it implied by the guard, with **%d** "
        "not implied. The round's real claim — that the master bound forces "
        "the half-space `α + χ + 2μ ≥ 1` — is scored separately on the **%d** "
        "samples inside it: **%d** violations."
        % (xp["trials"], xp["reached_the_assert"],
           xp["assert_implied_by_its_own_guard"], xp["assert_not_implied"],
           xp["samples_in_the_half_space"], xp["half_space_violations"]),
        "",
        "**The withdrawn exponent.** The round ships a provenance-repair note "
        "(**present: %d**) withdrawing `ρ★ = 4.1164`, and its frontier "
        "declares the value unused (**%d**). Checked: the numeral appears "
        "**%d** times in the frontier, **%d** in the checker report, and "
        "**%d** times in the paper outside its own NO-GO section — all in the "
        "discussion of the withdrawal, not as an input. The oscillation "
        "threshold is the stated one-half (**%d**), and β itself is **%s** "
        "against the certified bracket."
        % (cs["provenance_note_present"],
           cs["frontier_declares_the_exponent_unused"],
           cs["withdrawn_exponent_in_the_frontier"],
           cs["withdrawn_exponent_in_the_checker_report"],
           cs["withdrawn_exponent_in_the_paper_outside_its_no_go"],
           cs["oscillation_threshold_is_one_half"],
           cs["rows"][0]["verdict"] if cs["rows"] else "unchecked"),
        "",
        "**The published rows.** **%d** rows in **%d** groups recomputed from "
        "their own fields: **%d** quotient-identity failures, **%d** depth "
        "fields disagreeing, **%d** unit fields disagreeing, **%d** rows not "
        "actually synchronized."
        % (ex["rows"], ex["groups"], ex["quotient_identity_violations"],
           ex["depth_fields_disagreeing"], ex["unit_fields_disagreeing"],
           ex["class_not_synchronized"]),
        "",
        "**Their nine counters.** **%d** of the twelve compared figures "
        "reproduce exactly, including the three population totals they "
        "publish. **%d** are covered by a different population: their window "
        "sampler and their two doubled blocks. **%d** of their checks are "
        "covered by nothing here, and **%d** report zero."
        % (tc["counts_i_reproduce_exactly"],
           tc["checks_covered_by_a_different_population"],
           tc["checks_not_covered_at_all"],
           tc["checks_they_report_as_zero"]),
        "",
        "**The bundle as shipped, and one false attestation.** **%d** files, "
        "**%d** digests listed, **%d** mismatches, **%d** checksum lines "
        "naming a missing file, and %s with no digest anywhere — thirteen "
        "rounds without a digest in the validation record (**%d** per-file "
        "entries, **%d** with one). Its pass flag is the string `%s` under "
        "`%s`. **But the record attests `PASS` for a file the bundle does not "
        "contain**: %s. That file is absent from the directory and from "
        "`CHECKSUMS.sha256` too, so nothing in the bundle backs the "
        "attestation. It is reported in this gate's own `artifact_defects` "
        "field rather than as a failure, because `passed` has meant *the "
        "mathematics reproduces* for thirty-one reports and this defect is "
        "not in the mathematics. Against the paper, the ledger lists **%d** "
        "proved items to **%d**, **%d** open to **%d**, and **%d** no-go "
        "entries to the paper's **%d** headings (no no-go key at all: **%d**), "
        "with **%d** headings having no counterpart. The coverage heuristic "
        "passed both controls."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "no file",
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           af["validation_all_pass_flag"], af["validation_pass_flag_key"],
           ", ".join("`%s`" % n
                     for n in af["validation_names_a_file_not_in_the_bundle"])
           or "none",
           led["ledger_proved_items"], led["paper_proved_items"],
           led["ledger_open_items"], led["paper_open_items"],
           led["ledger_no_go_items"], led["paper_no_go_headings"],
           led["ledger_has_no_no_go_key"],
           len(led["no_go_headings_absent_from_the_ledger"])),
        "",
        "**The drill.** The instrument self-tests **%d** properties before the "
        "gate runs, **%d** of them failing. **%d** defects were planted one at "
        "a time: **%d** caught by the counter they attack, **%d** missed, "
        "**%d** malformed, %d caught only by another counter; %d of %d "
        "controls left the verdict unchanged. Six aim at non-vacuity entries "
        "and one at the artifact-defect field, which already reports a real "
        "defect — so that one has to make it report MORE, since from a known "
        "state only a rise is visible."
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
        print(json.dumps({"tool": "src73_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src73_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
