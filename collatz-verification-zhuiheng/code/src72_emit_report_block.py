"""Emit RUN-053's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src72_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src72-au2d25.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src72-drill.json"
REPORT = ROOT / "reports" / "RUN-053-HARD-ZETA-AU2D25-PRIMITIVE-UNIT.md"
FIGURES = ROOT / "data" / "gate-logs" / "src72-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src72_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def ratio(n: int, d: int) -> str:
    if not d:
        return "n/a"
    from math import gcd
    g = gcd(n, d) or 1
    return "%d/%d" % (n // g, d // g)


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    st, ga, tp = g["strip"], g["gates"], g["transport"]
    wi, sy, ex = g["windows"], g["synthetic"], g["examples"]
    af, led, tc = g["artifacts"], g["ledger"], g["their_claims"]
    tot = d["totals"]

    out = [
        BEGIN, "",
        "**The population.** Their enumeration is deterministic — five moduli, "
        "odd sources below 12000 not divisible by three, eleven edges per "
        "orbit — so it reproduces exactly: **%d** quotient-active edges from "
        "**%d** distinct start states over **%d** moduli, **%d** malformed."
        % (pop["edges"], pop["sources"], pop["moduli"],
           pop["malformed_edges"]),
        "",
        "**Theorem 3.1, sharp at both ends.** The one-step strip "
        "`-2^q < d < 3` failed **%d** times above and **%d** below over **%d** "
        "edges, and `d > 0 ⟹ d ∈ {1,2}` failed **%d** times on **%d** positive "
        "defects. Both ends are close: the upper end is **attained %d times** "
        "at `d = 2`, and the largest `-d/2^q` anywhere is **%s**. Against the "
        "previous round's block bound specialised to one edge, **%d** "
        "violations. **%d** defects are negative and **%d** are zero."
        % (st["strip_upper_violations"], st["strip_lower_violations"],
           st["edges"], st["positive_defect_not_one_or_two"],
           st["positive_defects"], st["upper_end_attained"],
           ratio(st["largest_lower_ratio_numerator"],
                 st["largest_lower_ratio_denominator"]),
           st["block_bound_from_the_previous_round_violations"],
           st["negative_defects"], st["zero_defects"]),
        "",
        "**The compensation gates, all four populated.** **%d** zero, **%d** "
        "synchronized (**%d** positive, **%d** negative), **%d** "
        "binary-exclusive, **%d** ternary-exclusive, **%d** unclassified. "
        "Theorem 4.1's atomic reset: **%d** defects not 2, **%d** valuations "
        "not 1, **%d** wrong output depths, **%d** outputs not coprime to "
        "six, **%d** unit-formula failures, **%d** units not increasing. "
        "Theorem 4.2's pump: **%d** non-negative defects, **%d** valuations "
        "below two, **%d** ternary depths not deeper, **%d** wrong defect "
        "valuations, **%d** bad `ξ`, **%d** unit-formula failures, **%d** "
        "units not decreasing. Theorem 4.3's normal forms: **%d** wrong "
        "valuations, **%d** non-coprime `ω`, **%d** cylinder failures, **%d** "
        "positive normal-form failures, **%d** non-negative `ω` on the "
        "negative side."
        % (ga["zero"], ga["sync"], ga["sync_positive"], ga["sync_negative"],
           ga["binary_exclusive"], ga["ternary_exclusive"],
           ga["unclassified"],
           ga["te_defect_not_two"], ga["te_valuation_not_one"],
           ga["te_depths_wrong"], ga["te_output_not_coprime"],
           ga["te_unit_formula_violations"], ga["te_unit_not_increasing"],
           ga["be_defect_not_negative"], ga["be_valuation_below_two"],
           ga["be_ternary_not_deeper"], ga["be_defect_valuation_wrong"],
           ga["be_xi_not_odd_positive"], ga["be_unit_formula_violations"],
           ga["be_unit_not_decreasing"],
           ga["sync_defect_valuations_wrong"], ga["sync_omega_not_coprime"],
           ga["sync_cylinder_violations"],
           ga["sync_positive_normal_form_violations"],
           ga["sync_negative_omega_not_negative"]),
        "",
        "**Two float-guarded reservoir bounds, in exact integers.** Their "
        "checker writes `A + BETA*(B+1) < q + 1e-12` and "
        "`A + BETA*Bp < q + 1e-12`; under `2^{βm} = 3^m` these are "
        "`2^A 3^{B+1} < 2^q` and `2^A 3^{Bp} < 2^q`. Over **%d** reservoir "
        "tests the exact forms failed **%d** and **%d** times, and the two "
        "routes disagreed **%d** times — so their `1e-12` fudge decides "
        "nothing here."
        % (ga["reservoir_tests"], ga["be_reservoir_bound_violations"],
           ga["sync_negative_reservoir_violations"],
           ga["float_reservoir_route_disagreeing"]),
        "",
        "**Theorem 5.1, exact in rationals.** "
        "`u'/u = 2^{-c₂}3^{c₃}(1 + d/(3n))` was checked as an exact "
        "`Fraction` on all **%d** edges: **%d** violations. Corollary 5.2 "
        "(zero defect preserves the unit) failed **%d** times, and Corollary "
        "5.3's seesaw — the unit rises on every ternary-exclusive edge and "
        "falls on every binary-exclusive one — failed **%d** times over **%d** "
        "exclusive edges."
        % (tp["edges"], tp["transport_violations"],
           tp["zero_defect_transport_not_trivial"],
           tp["exclusive_seesaw_violations"], tp["seesaw_population"]),
        "",
        "**Theorem 6.1's window products, with the chain broken as a "
        "control.** Over **%d** windows covering **%d** edges the quotient "
        "correction product failed **%d** times and the unit transport "
        "**%d**. Both hold because consecutive edges chain, and their "
        "generator always builds them that way — so each was re-run with one "
        "interior edge dropped: **%d of %d** broken windows failed the "
        "correction product and **%d** failed the unit transport. The "
        "assertions have content; no generated input can exercise them."
        % (wi["windows"], wi["edges_in_windows"],
           wi["correction_product_violations"],
           wi["unit_window_transport_violations"],
           wi["broken_correction_product_failures"], wi["broken_windows"],
           wi["broken_unit_transport_failures"]),
        "",
        "**Their triangle bound is implied edge by edge.** The window "
        "assertion sums three lists and compares the totals — but by Theorem "
        "5.1, `|c₂ − βc₃|` is `|log₂(u'/u) − ε|`, so each term already "
        "satisfies `|ΔU| + |ε| ≥ |c₂ − βc₃|`. Measured per term over **%d** "
        "edges: **%d** with negative slack, and **%d** aggregate violations. "
        "A sum of non-negative terms cannot go negative however it is "
        "grouped, so the summed form adds nothing to the per-edge one."
        % (wi["triangle_terms"], wi["triangle_terms_with_negative_slack"],
           wi["triangle_bound_violations"]),
        "",
        "**Their three synthetic blocks, each with its construction broken.** "
        "The synchronized block draws **%d** times and keeps **%d** "
        "constructions, whose equation failed **%d** times — but `u'` is "
        "*defined* as `num // 2^{c₂}` under a divisibility test, so the "
        "assertion restates integer division. Dropping only that test: **%d** "
        "failures. The ternary-exclusive block ran **%d** trials with **%d** "
        "failures, where `u'` is built as a multiple of `u` plus one; "
        "removing the multiplier: **%d** failures. The binary-exclusive block "
        "ran **%d** trials with **%d** failures, where `u` is built as `ξ` "
        "plus a multiple of `u'`; removing the pump: **%d** failures. All "
        "three assertions restate the line above them."
        % (sy["sync_attempts"], sy["sync_constructions"],
           sy["sync_equation_violations"],
           sy["sync_equation_violations_when_the_divisibility_is_dropped"],
           sy["te_trials"], sy["te_not_increasing"],
           sy["te_not_increasing_when_the_offset_is_removed"],
           sy["be_trials"], sy["be_not_decreasing"],
           sy["be_not_decreasing_when_the_pump_is_removed"]),
        "",
        "**The published rows.** **%d** rows across **%d** example groups "
        "recomputed from their own fields: **%d** quotient-identity failures, "
        "**%d** depth fields disagreeing, **%d** unit fields disagreeing, "
        "**%d** strip violations, **%d** rows whose group name disagrees with "
        "their own defect sign."
        % (ex["rows"], ex["groups"], ex["quotient_identity_violations"],
           ex["depth_fields_disagreeing"], ex["unit_fields_disagreeing"],
           ex["strip_violations"],
           ex["class_disagreeing_with_the_defect_sign"]),
        "",
        "**The constants.** **%d** checked, **%d** exact to the last bit, "
        "**%d** matching the float64 chain rather than the nearest double, "
        "**%d** disagreeing with both, **%d** undecided, **%d** missing, "
        "**%d** where frontier and report disagree. **%d** frontier value has "
        "no closed form to check against here — %s, carried as a four-decimal "
        "literal inherited from an earlier round."
        % (cs["constants_checked"], cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["disagreeing_with_both_evaluations"], cs["undecided_brackets"],
           cs["missing_from_the_frontier"],
           cs["frontier_and_report_disagreeing"],
           len(cs["frontier_constants_with_no_closed_form_here"]),
           ", ".join("`%s`" % n for n in
                     cs["frontier_constants_with_no_closed_form_here"])
           or "none"),
        "",
        "**Their sixteen counters.** **%d** reproduce exactly. **%d** are "
        "covered by a different population — their three window counters come "
        "from partitions drawn inside the orbit loop, and their synchronized "
        "synthetic block draws from an RNG stream shared with that loop, so "
        "no standalone reimplementation can match those integers. **%d** of "
        "their checks are covered by nothing here, and **%d** report zero."
        % (tc["counts_i_reproduce_exactly"],
           tc["checks_covered_by_a_different_population"],
           tc["checks_not_covered_at_all"],
           tc["checks_they_report_as_zero"]),
        "",
        "**The bundle as shipped.** **%d** files, **%d** digests listed, "
        "**%d** mismatches, **%d** checksum lines naming a missing file, and "
        "%s with no digest anywhere. The self-validation record changed shape "
        "for the twelfth round running: its pass flag is now the STRING `%s` "
        "under the key `%s`, it lists **%d** problems, and it names **no "
        "files at all** — so nothing records which files were validated "
        "(**%d** per-file entries, **%d** with a digest). Against the paper, "
        "the ledger lists **%d** proved items to the paper's **%d** and "
        "**%d** open to **%d**, but **carries no no-go key at all** against "
        "the paper's **%d** NO-GO headings, **%d** of which have no textual "
        "counterpart anywhere in it. The coverage heuristic passed both its "
        "controls."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "no file",
           af["validation_all_pass_flag"], af["validation_pass_flag_key"],
           af["validation_problems_listed"],
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           led["ledger_proved_items"], led["paper_proved_items"],
           led["ledger_open_items"], led["paper_open_items"],
           led["paper_no_go_headings"],
           len(led["no_go_headings_absent_from_the_ledger"])),
        "",
        "**The drill.** The instrument self-tests **%d** properties before "
        "the gate runs, **%d** of them failing. **%d** defects were planted "
        "one at a time: **%d** caught by the counter they attack, **%d** "
        "missed, **%d** malformed, %d caught only by another counter; %d of "
        "%d controls left the gate undisturbed. Seven aim at non-vacuity "
        "entries, five of them at this round's own controls."
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
        print(json.dumps({"tool": "src72_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src72_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
