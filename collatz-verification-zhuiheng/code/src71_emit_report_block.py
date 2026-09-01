"""Emit RUN-052's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src71_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src71-au2d24.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src71-drill.json"
REPORT = ROOT / "reports" / "RUN-052-HARD-ZETA-AU2D24-COMPENSATION.md"
FIGURES = ROOT / "data" / "gate-logs" / "src71-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src71_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def ratio(n: int, d: int) -> str:
    if not d:
        return "n/a"
    from math import gcd
    g = gcd(n, d) or 1
    return "%d/%d" % (n // g, d // g)


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    bd, eq, al = g["bounds"], g["equivalence"], g["alignment"]
    pr, tr, te = g["primitive"], g["trichotomy"], g["telescoping"]
    sy, ex = g["synthetic"], g["examples"]
    af, led, tc = g["artifacts"], g["ledger"], g["their_claims"]
    tot = d["totals"]

    out = [
        BEGIN, "",
        "**The population.** Their enumeration is fully deterministic — four "
        "moduli, odd sources below 5000 not divisible by three, fourteen "
        "accelerated steps, windows of length at most six — so it reproduces "
        "exactly: **%d** quotient-active segments over **%d** moduli from "
        "**%d** distinct start states, **%d** malformed, longest segment "
        "**%d**."
        % (pop["segments"], pop["moduli"], pop["sources"],
           pop["malformed_segments"], pop["longest_segment"]),
        "",
        "**Theorem 4.1, which is attained.** The affine-correction bound "
        "`0 < B_P ≤ 2^{Q−L}(3^L − 2^L)` failed **%d** times below and **%d** "
        "above over **%d** segments, and the looser boxed form `< 2^{Q−L}3^L` "
        "failed **%d**. The upper bound is **reached on %d of %d segments "
        "(%s)** — a live, binding estimate."
        % (bd["affine_lower_bound_violations"],
           bd["affine_upper_bound_violations"], bd["segments"],
           bd["affine_loose_upper_bound_violations"],
           bd["affine_upper_bound_attained"], bd["segments"],
           pct(bd["affine_upper_bound_attained"], bd["segments"])),
        "",
        "**Theorem 5.1, which carries a spare factor of three.** The central "
        "barrier `|𝔡| < 2^Q 3^L` failed **%d** times — but the largest ratio "
        "`|𝔡|/(2^Q 3^L)` anywhere in the population is exactly **%s**. The "
        "sharp form `|𝔡| ≤ 2^Q 3^{L−1}` also holds, **%d** violations, and is "
        "**attained %d times**. The published inequality is loose by a factor "
        "of three and the tight one is reached; a drill defect that merely "
        "halved the bound was invisible and had to be taken to a twenty-seventh "
        "before it could bite."
        % (bd["barrier_violations"],
           ratio(bd["largest_barrier_numerator"],
                 bd["largest_barrier_denominator"]),
           bd["sharpened_barrier_violations"],
           bd["sharpened_barrier_attained"]),
        "",
        "**Theorem 6.1 and Corollary 6.2.** `𝔡 = 0 ⟺ c₂ = c₃ = 0` failed "
        "**%d** times over **%d** segments (**%d** zero-defect, **%d** "
        "nonzero), with **%d** zero defects carrying nonzero compensation and "
        "**%d** the other way. The no-double-deficit corollary failed **%d** "
        "times. The three nonzero classes are populated: **%d** synchronized, "
        "**%d** binary-exclusive, **%d** ternary-exclusive."
        % (eq["equivalence_violations"], eq["segments"], eq["zero_defect"],
           eq["nonzero_defect"],
           eq["zero_defect_with_nonzero_compensation"],
           eq["zero_compensation_with_nonzero_defect"],
           eq["double_deficit_violations"],
           eq["nonzero_with_both_positive"],
           eq["nonzero_with_c2_positive_only"],
           eq["nonzero_with_c3_positive_only"]),
        "",
        "**Theorems 7.1 and 7.2, which their report never counts.** The "
        "ultrametric alignment laws are asserted inside their validator and "
        "incremented nowhere, so they appear in no counter — on the two "
        "largest populations of the round. Measured here: binary alignment "
        "over **%d** segments with **%d** valuation and **%d** congruence "
        "failures; ternary alignment over **%d** with **%d** and **%d**. "
        "**%d** segments had a positive depth alongside a zero defect."
        % (al["binary_alignment_population"],
           al["binary_valuation_violations"],
           al["binary_congruence_violations"],
           al["ternary_alignment_population"],
           al["ternary_valuation_violations"],
           al["ternary_congruence_violations"],
           al["defect_zero_while_a_depth_is_positive"]),
        "",
        "**Theorems 8.1 and 9.1, and the same spare three.** Over **%d** "
        "synchronized events the primitive cylinder equation "
        "`2^{c₂}u' = 3^{c₃}u + ω` failed **%d** times, its two residue forms "
        "**%d** and **%d**, and the coprimality of `u`, `u'`, `ω` failed "
        "**%d** and **%d**. The CRT window failed **%d** times — and its "
        "largest ratio is exactly **%s**, the same spare factor the defect "
        "barrier carries. The sharp form `3|ω|2^{A'}3^{B} ≤ 2^{c₂}3^{c₃}` "
        "holds with **%d** violations and is **attained %d times**. **%d** "
        "windows sit within a factor of two of failing."
        % (pr["synchronized"], pr["cylinder_equation_violations"],
           pr["binary_residue_violations"], pr["ternary_residue_violations"],
           pr["u_not_coprime_to_six"], pr["omega_not_coprime_to_six"],
           pr["crt_window_violations"],
           ratio(pr["largest_window_numerator"],
                 pr["largest_window_denominator"]),
           pr["sharpened_window_violations"],
           pr["sharpened_window_attained"],
           pr["windows_within_a_factor_of_two_of_failing"]),
        "",
        "**Theorem 11.1, and two assertions that restate their hypotheses.** "
        "The exclusive branches gave **%d** binary-exclusive and **%d** "
        "ternary-exclusive events, **%d** and **%d** violations, and **%d** "
        "nonzero defects fell outside the trichotomy. But their validator's "
        "two exclusive assertions are their own hypotheses written out: by "
        "the definitions `c₃ = L + B − B'` and `c₂ = Q + A' − A`, `c₃ ≤ 0` IS "
        "`B' ≥ B + L` and `c₂ ≤ 0` IS `A − A' ≥ Q`. Evaluating both members of "
        "each pair separately on every segment — **%d** comparisons — they "
        "disagreed **%d** and **%d** times."
        % (tr["binary_exclusive"], tr["ternary_exclusive"],
           tr["ternary_overdrain_violations"],
           tr["binary_overdrain_violations"],
           tr["trichotomy_classes_unaccounted"],
           tr["predicate_pairs_compared"],
           tr["c3_nonpositive_disagreeing_with_B_prime_bound"],
           tr["c2_nonpositive_disagreeing_with_A_bound"]),
        "",
        "**Theorem 12.1, with its construction broken as a control.** Over "
        "**%d** partitions covering **%d** blocks the two telescoping sums "
        "failed **%d** and **%d** times, and **%d** zero blocks carried "
        "nonzero compensation. That is not evidence on its own: the identity "
        "holds because consecutive blocks share an endpoint, so `A'ᵢ` and "
        "`Aᵢ₊₁` are the same valuation of the same number, and their "
        "generator always builds it that way. Re-running with only that "
        "property broken — every block's start shifted by one — the same sums "
        "failed on **%d of %d** partitions (binary) and **%d** (ternary). The "
        "assertion has real content; no generated input can exercise it."
        % (te["partitions"], te["blocks"],
           te["binary_telescoping_violations"],
           te["ternary_telescoping_violations"],
           te["zero_block_with_nonzero_compensation"],
           te["broken_binary_telescoping_failures"], te["broken_partitions"],
           te["broken_ternary_telescoping_failures"]),
        "",
        "**Their two synthetic blocks, each with a control.** The random-word "
        "bound ran **%d** trials: **%d** below, **%d** above, **%d** with "
        "valuation under the length, and the upper bound **attained %d "
        "times**. The forbidden-quadrant block ran **%d** trials with **%d** "
        "divisibility and **%d** size violations (**%d** of them landing on a "
        "zero defect) — but in that quadrant both terms carry "
        "`2^{Q+A'} 3^{B+L}`, so the divisibility is a consequence of how the "
        "inputs are built. Dropping only the quadrant constraint and "
        "regenerating: **%d of %d** divisibility failures and **%d** size "
        "failures. The arithmetic is real and the generator cannot violate it."
        % (sy["word_trials"], sy["word_lower_bound_violations"],
           sy["word_upper_bound_violations"],
           sy["word_valuation_below_length"],
           sy["word_upper_bound_attained"], sy["quadrant_trials"],
           sy["quadrant_divisibility_violations"],
           sy["quadrant_size_violations"], sy["quadrant_zero_defects"],
           sy["free_quadrant_divisibility_failures"],
           sy["free_quadrant_trials"], sy["free_quadrant_size_failures"]),
        "",
        "**The published rows.** **%d** synchronized and **%d** exclusive "
        "rows recomputed from their own fields: **%d** depth fields "
        "disagreeing, **%d** quotient-identity failures, **%d** barrier "
        "failures, **%d** rows whose class disagrees with their own depths."
        % (ex["synchronized_rows"], ex["exclusive_rows"],
           ex["depth_fields_disagreeing"],
           ex["quotient_identity_violations"], ex["barrier_violations"],
           ex["class_disagreeing_with_the_depths"]),
        "",
        "**The constants.** **%d** checked, **%d** exact to the last bit, "
        "**%d** matching the float64 chain rather than the nearest double, "
        "**%d** disagreeing with both, **%d** undecided, **%d** missing, "
        "**%d** where frontier and report disagree. Cross-read, **%d** "
        "frontier constants are never computed by the checker: %s."
        % (cs["constants_checked"], cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["disagreeing_with_both_evaluations"], cs["undecided_brackets"],
           cs["missing_from_the_frontier"],
           cs["frontier_and_report_disagreeing"],
           len(cs["frontier_constants_the_checker_never_computes"]),
           ", ".join("`%s`" % n for n in
                     cs["frontier_constants_the_checker_never_computes"])
           or "none"),
        "",
        "**Their eleven counters.** **%d** reproduce exactly — the strongest "
        "reproduction of the sweep, because the whole enumeration is "
        "deterministic. **%d** is covered by a different population (their "
        "partitions are drawn inside the orbit loop, mine from a separate "
        "sampler). **%d** of their checks are covered by nothing here, and "
        "**%d** report zero. Two theorems — 7.1 and 7.2 — have no counter of "
        "theirs to compare against at all."
        % (tc["counts_i_reproduce_exactly"],
           tc["checks_covered_by_a_different_population"],
           tc["checks_not_covered_at_all"],
           tc["checks_they_report_as_zero"]),
        "",
        "**The bundle as shipped.** **%d** files — one more than every "
        "previous round, a `build_` script joining the verifier — **%d** "
        "digests listed, **%d** mismatches, **%d** checksum lines naming a "
        "missing file, and %s with no digest anywhere. The self-validation "
        "record changed shape for the eleventh round running: it now names "
        "files as a bare list rather than per-file results (**%d** per-file "
        "entries, **%d** with a digest), its `json_parse` and `python_compile` "
        "are plain booleans instead of records, and **it carries no overall "
        "pass flag at all** — `all_pass` and `overall_pass` are both gone. Its "
        "top-level booleans are all true (**%d** not true). %s absent from it "
        "entirely. Against the paper, the ledger lists **%d** proved items to "
        "the paper's **%d**, **%d** open to **%d**, and **%d** no-go entries "
        "to the paper's **%d** headings; **%d** open items and **%d** no-go "
        "headings have no ledger counterpart. The coverage heuristic passed "
        "both its controls."
        % (af["files_present"], af["digests_listed"],
           af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "no file",
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           af["validation_top_level_flags_not_true"],
           ", ".join("`%s`" % n
                     for n in af["files_absent_from_the_validation_record"])
           or "No file",
           led["ledger_proved_items"], led["paper_proved_items"],
           led["ledger_open_items"], led["paper_open_items"],
           led["ledger_no_go_items"], led["paper_no_go_headings"],
           len(led["open_items_absent_from_the_ledger"]),
           len(led["no_go_headings_absent_from_the_ledger"])),
        "",
        "**The drill.** The instrument self-tests **%d** properties before the "
        "gate runs, **%d** of them failing. **%d** defects were planted one at "
        "a time: **%d** caught by the counter they attack, **%d** missed, "
        "**%d** malformed, %d caught only by another counter; %d of %d "
        "controls left the gate undisturbed. Six aim at non-vacuity entries, "
        "two of them at this round's own controls — a control that stops "
        "firing proves nothing, so it is drilled like everything else."
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
        print(json.dumps({"tool": "src71_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src71_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
