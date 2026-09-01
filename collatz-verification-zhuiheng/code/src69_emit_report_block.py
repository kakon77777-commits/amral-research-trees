"""Emit RUN-050's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src69_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src69-au2d22.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src69-drill.json"
REPORT = ROOT / "reports" / "RUN-050-HARD-ZETA-AU2D22-DEFECT-TREE.md"
FIGURES = ROOT / "data" / "gate-logs" / "src69-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src69_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    ca, tr, rt = g["calculus"], g["tree"], g["root"]
    dp, sg, qf = g["depth"], g["sign"], g["quotient_floor"]
    rn = g["retention"]
    co, ex = g["corollary"], g["examples"]
    af, led, tc = g["artifacts"], g["ledger"], g["their_claims"]
    tot = d["totals"]

    out = [
        BEGIN, "",
        "**The population.** **%d** bridges from **%d** distinct sources "
        "(longest tail %d), of which **%d** have zero total lift and **%d** do "
        "not — the sixth round running in which the positive-lift branch has "
        "no finite instance. Their checker publishes `finite_local_bridges` "
        "and `zero_lift_bridges` as separate counters; both read **%d**, "
        "because a local bridge has minimal `Q` by definition and its total "
        "lift is therefore zero. The second counter filters nothing."
        % (pop["bridges"], pop["sources"], pop["longest_tail"],
           pop["zero_lift"], pop["positive_lift"], pop["bridges"]),
        "",
        "**Theorem 3.2, the quotient lift.** `2^Q n' = 3^L n + d` was checked "
        "on **%d** deterministically enumerated spans across **%d** "
        "bridge-precision levels: **%d** violations, and **%d** spans where "
        "the defect failed to be an integer."
        % (ca["spans"], ca["levels"],
           ca["quotient_lift_theorem_3_2_violations"],
           ca["defect_not_integral"]),
        "",
        "**Theorem 4.1, and the order it is about.** The composition held on "
        "**%d** matrix products, with **%d** disagreements between the matrix "
        "form and the written-out defect form and **%d** products whose "
        "diagonal was not multiplicative. The previous round's headline was a "
        "bilinear law tested only where its two coefficients swap into each "
        "other, so the population is measured for order sensitivity here "
        "before the law is believed: `R(R)R(P)` differs from `R(P)R(R)` on "
        "**%d of %d** products (%s), and coincides on **%d**. The law is "
        "being tested where it can distinguish itself from its reverse."
        % (ca["compositions"],
           ca["matrix_form_disagreeing_with_the_defect_form"],
           ca["diagonal_not_multiplicative"],
           ca["order_sensitive_compositions"], ca["compositions"],
           pct(ca["order_sensitive_compositions"], ca["compositions"]),
           ca["compositions_where_the_two_orders_agree"]),
        "",
        "**Theorem 5.1, and what the retention rule actually buys.** **%d** "
        "erasure intervals over **%d** levels: **%d** with endpoints not "
        "congruent, **%d** not contiguous, **%d** crossing pairs, and **%d** "
        "nested pairs on **%d** levels, so the laminar family is populated "
        "rather than trivially empty. But `crossing_pairs` **cannot rise**. "
        "The stack truncation makes a crossing structurally unrepresentable — "
        "planting the opposite retention rule leaves it at zero, and a "
        "variant that keeps a removed residue reachable raises `IndexError` "
        "instead of producing one. The predicate is therefore exercised by "
        "hand in the instrument, or a zero here would be indistinguishable "
        "from a broken test. Their `contiguous_loop_tree_laminarity` counter "
        "has the same property."
        % (tr["intervals"], tr["levels"],
           tr["interval_endpoints_not_congruent"],
           tr["interval_not_contiguous"], tr["crossing_pairs"],
           tr["nested_pairs"], tr["levels_with_a_nested_pair"]),
        "",
        "**What the paper attributes to `stack_t[p] = i`, measured.** Section "
        "5's proof sketch derives contiguity and laminarity from the stack "
        "discipline. Running both retention rules over the same orbits: they "
        "produce **different** interval families on **%d of %d** levels (%s), "
        "and *both* give **%d**/**%d** crossings, **%d**/**%d** "
        "non-contiguous intervals and **%d**/**%d** misanchored endpoints — "
        "and Theorem 6.1 still reconstructs under the wrong rule, **%d** "
        "failures. The update is not what makes the family laminar. What it "
        "controls is the tree's shape: nested pairs go from **%d** to **%d**, "
        "of which **%d** share a left endpoint under the wrong rule and "
        "**%d** under the paper's, and the total interval span goes from "
        "**%d** to **%d**. The renormalization is a partition because of that "
        "line; laminarity would have survived without it."
        % (rn["levels_where_the_two_rules_differ"], rn["levels"],
           pct(rn["levels_where_the_two_rules_differ"], rn["levels"]),
           rn["kept_crossings"], rn["first_crossings"],
           rn["kept_non_contiguous"], rn["first_non_contiguous"],
           rn["kept_misanchored"], rn["first_misanchored"],
           rn["reconstruction_failures_under_the_first_rule"],
           rn["kept_nested_pairs"], rn["first_nested_pairs"],
           rn["first_shared_left_endpoint"],
           rn["kept_shared_left_endpoint"],
           rn["kept_total_span"], rn["first_total_span"]),
        "",
        "**Theorem 6.1, the tree reconstruction.** Rebuilding each bridge's "
        "matrix from its interval tree and comparing against the direct "
        "product: **%d** disagreements at the root and **%d** at the **%d** "
        "interior nodes, with **%d** node spans whose defect was not an "
        "integer."
        % (tr["tree_matrix_disagreeing_with_the_direct_one"],
           tr["node_matrix_disagreeing_with_its_span"], tr["nodes"],
           tr["node_span_defect_not_integral"]),
        "",
        "**Theorems 7.1–7.3 and 12.1.** The root defect vanished at the "
        "canonical modulus on all **%d** bridges, with **%d** moduli failing "
        "to exceed both endpoints. The ordered weighted expansion summed to "
        "zero on **%d** partitions (**%d** non-integral blocks), of which "
        "**%d** (%s) carry a nonzero block and so can exercise Corollary "
        "7.3 — the other %s are all-zero and test nothing. The ultrametric "
        "minimum was unpaired **%d** times. The prefix/suffix coboundary held "
        "at **%d** cuts: **%d**, **%d** and **%d** failures of its three "
        "forms."
        % (rt["bridges"], rt["canonical_modulus_not_above_both_endpoints"],
           rt["partitions"], rt["expansion_block_not_integral"],
           rt["partitions_with_a_nonzero_block"],
           pct(rt["partitions_with_a_nonzero_block"], rt["partitions"]),
           pct(rt["partitions"] - rt["partitions_with_a_nonzero_block"],
               rt["partitions"]),
           rt["ultrametric_minimum_not_paired"], rt["cuts"],
           rt["prefix_defect_not_the_coboundary"],
           rt["suffix_defect_not_the_coboundary"],
           rt["coboundary_sum_not_zero"]),
        "",
        "**Theorem 8.1, both directions.** **%d** probes over **%d** "
        "intervals, **%d** violations. The equivalence has an `only if` half "
        "that is only reached when the probe goes above the defect's "
        "valuation: **%d** probes did (%s), **%d** did not, and **%d** "
        "intervals never had their upper half probed at all. Their loop caps "
        "the probe at `min(nu+2, 5)`, whose largest step is `min(nu+1, 4)` — "
        "above `nu` only when `nu <= 3`. On this population that costs them "
        "the upper half on **%d** intervals, the largest valuation seen being "
        "**%d**. A small gap, and worth stating as a number rather than left "
        "implicit."
        % (dp["probes"], dp["intervals"], dp["depth_equivalence_violations"],
           dp["probes_above_the_valuation"],
           pct(dp["probes_above_the_valuation"], dp["probes"]),
           dp["probes_at_or_below_the_valuation"],
           dp["intervals_whose_upper_half_was_never_probed"],
           dp["intervals_the_bundle_cap_would_not_probe_above"],
           dp["largest_valuation_seen"]),
        "",
        "**Theorem 9.1 in exact integers.** `Q <= beta L` is exactly "
        "`2^Q <= 3^L`, and the bundle evaluates `BETA*L` in float64. Over "
        "**%d** return intervals the sign law failed **%d** times, a "
        "nonpositive defect was non-supercritical **%d** times, and the two "
        "routes disagreed **%d** times — so on this population their float "
        "evaluation decides every case the way exact arithmetic does. "
        "**%d** defects were negative, the largest in absolute value running "
        "to %d bits, so the law's contrapositive has a real population."
        % (sg["intervals"], sg["sign_law_violations"],
           sg["negative_defect_not_supercritical"],
           sg["float_sign_route_disagreeing_with_the_exact_one"],
           sg["defects_that_are_negative"],
           int(sg["largest_absolute_defect_seen"]).bit_length()),
        "",
        "**Theorems 10.1 and 11.1.** **%d** zero-defect intervals, all "
        "supercritical (**%d** exceptions). The resonance `n = 2^Q u`, "
        "`n' = 3^L u` held with **%d** divisibility failures and **%d** "
        "disagreeing parameters. The paper also asserts `u >= 1`, which their "
        "checker does not test: **%d** violations, and the smallest `u` seen "
        "is **%d**, so the claim is satisfied with room rather than at its "
        "boundary. The lift toll is guarded in float64 with a `1e-12` fudge "
        "and is exactly `2^{m+1} Z0 > 2^Q M` in integers: **%d** and **%d** "
        "violations of its two forms, **%d** disagreements between the two "
        "routes, and **%d** tolls that one fewer lift bit would break. Its "
        "tightest margin over the whole population is a factor of **%s**."
        % (sg["zero_defect_intervals"], sg["zero_defect_not_supercritical"],
           sg["resonance_n_not_a_multiple"],
           sg["resonance_parameters_disagreeing"],
           sg["resonance_parameter_not_positive"],
           sg["smallest_resonance_parameter"],
           sg["lift_toll_in_violations"], sg["lift_toll_out_violations"],
           sg["float_toll_route_disagreeing_with_the_exact_one"],
           sg["tolls_one_lift_bit_from_failing"],
           sg["tightest_toll_margin"]),
        "",
        "**Theorem 13.1, and how close it runs.** `n > (2^{m-1} Z - M)/M` is "
        "exactly `(n+1) M > 2^{m-1} Z`: **%d** violations over **%d** "
        "high-lift positions on **%d** bridges, **%d** disagreements with "
        "their float route, and the floor was nontrivial (right side above "
        "the modulus) at **%d** of them. **%d** positions sit within a factor "
        "of two of failing, and the tightest margin anywhere is **%s** — "
        "so this bound is nearly attained rather than comfortably loose, "
        "which is what makes it worth stating. The smallest quotient seen is "
        "**%d**."
        % (qf["quotient_floor_violations"], qf["positions"], qf["bridges"],
           qf["float_route_disagreeing_with_the_exact_one"],
           qf["positions_where_the_floor_is_positive"],
           qf["floors_within_a_factor_of_two_of_failing"],
           qf["tightest_floor_margin"],
           qf["smallest_quotient_seen"]),
        "",
        "**Corollary 13.2, which has no counter of its own.** The round's "
        "sixteen checks cover every numbered theorem and skip the corollary "
        "that names the frontier constant. Its content is a *conjunction* the "
        "bundle only tests as two separate statements: the faithful core's "
        "retained high-lift vertices are the ones claimed to sit on Theorem "
        "13.1's floor. Measured over **%d** bridges: **%d** retained "
        "vertices, **%d** of them high-lift (%s), and **%d** below the floor. "
        "The conjunction is real — but it is **empty on %d bridges** (%s), "
        "which have no high-lift retained vertex for the corollary to speak "
        "about. The mass half carries an `o(1)`, so a finite shortfall cannot "
        "be a failure: the ratio ranges over **%s to %s** and falls below "
        "`2 - beta = 0.4150` on **%d of %d**."
        % (co["bridges"], co["retained_vertices"],
           co["retained_high_lift_vertices"],
           pct(co["retained_high_lift_vertices"], co["retained_vertices"]),
           co["retained_high_lift_vertex_below_the_floor"],
           co["bridges_with_no_high_lift_retained_vertex"],
           pct(co["bridges_with_no_high_lift_retained_vertex"],
               co["bridges"]),
           co["smallest_mass_ratio"], co["largest_mass_ratio"],
           co["levels_where_the_mass_ratio_is_below_the_constant"],
           co["bridges"]),
        "",
        "**Both halves of the corollary converge.** An asymptotic claim is "
        "tested by its trend, not by a finite count, so both deviations were "
        "binned against bridge length:",
        "",
        "| `h` | bridges | mean mass/`h` | below 0.4150 | no high-lift retained |",
        "| --- | ---: | ---: | ---: | ---: |",
    ] + [
        "| %d–%d | %d | %.4f | %.1f%% | %.1f%% |"
        % (b["h_from"], b["h_to"], b["bridges"], b["mean_mass_ratio"],
           b["below_the_constant_pct"], b["no_high_lift_retained_pct"])
        for b in co["bands"]
    ] + [
        "",
        "The mean sits above the constant in every band, the shortfall falls "
        "away with `h`, and the vacuity of the second conjunct disappears "
        "entirely by `h >= 30`. The `o(1)` is doing honest work. The tail is "
        "thin — **%d** bridges above `h = 50` — so the trend is clear and the "
        "last rows are not on their own evidence."
        % sum(b["bridges"] for b in co["bands"] if b["h_from"] >= 50),
        "",
        "**The published rows.** **%d** nonzero and **%d** zero-defect nodes "
        "recomputed: **%d** length disagreements, **%d** valuations, **%d** "
        "sign-law failures, **%d** zero nodes that were not supercritical, "
        "**%d** whose endpoints were not congruent to the published residue, "
        "**%d** failing the lift identity `2^Q n' = 3^L n` recomputed from the "
        "published endpoints, and **%d** resonance parameters disagreeing."
        % (ex["nonzero_nodes"], ex["zero_nodes"], ex["length_disagreeing"],
           ex["v3_disagreeing"], ex["defect_sign_wrong"],
           ex["zero_node_not_supercritical"],
           ex["zero_node_endpoints_not_congruent"],
           ex["zero_node_lift_identity_violations"],
           ex["zero_node_resonance_disagreeing"]),
        "",
        "**The constants.** **%d** checked, **%d** exact to the last bit, "
        "**%d** matching the float64 chain rather than the nearest double, "
        "**%d** disagreeing with both, **%d** undecided, **%d** missing from "
        "the frontier, and **%d** where the frontier and the report "
        "disagree. The mass constant is republished from the previous round "
        "under a shorter name (`fully_faithful_loop_mass_constant` → "
        "`faithful_loop_mass_constant`) with **identical digits** and the "
        "same +2 ulp offset — cross-read across the two rounds, there is no "
        "drift."
        % (cs["constants_checked"], cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["disagreeing_with_both_evaluations"], cs["undecided_brackets"],
           cs["missing_from_the_frontier"],
           cs["frontier_and_report_disagreeing"]),
        "",
        "**Their sixteen counters.** **%d** reproduce exactly on the same "
        "population. The other **%d** are drawn from their seeded RNG block, "
        "so no independent run can match the integer; each is covered here by "
        "a deterministic enumeration that is larger than theirs, and the "
        "cross-report table names my counter rather than leaving a blank that "
        "would read as *not reproduced*. **%d** of their checks are covered "
        "by nothing here, and **%d** of them report zero."
        % (tc["counts_i_reproduce_exactly"],
           tc["checks_covered_by_a_different_population"],
           tc["checks_not_covered_at_all"],
           tc["checks_they_report_as_zero"]),
        "",
        "**The bundle as shipped.** **%d** files, **%d** digests listed, "
        "**%d** mismatches, **%d** checksum lines naming a file that is not "
        "there, and %s with no digest anywhere. The validation record carries "
        "**%d** per-file entries of which **%d** carry a digest — the ninth "
        "round in a row whose self-validation records `pass` without "
        "recording what it hashed. %s absent from it entirely. Against the "
        "paper, the ledger lists **%d** proved items to the paper's **%d**, "
        "**%d** open to **%d**, and **%d** no-go entries to the paper's "
        "**%d** headings; **%d** open items and **%d** no-go headings have no "
        "ledger counterpart, and the coverage heuristic passed both its "
        "controls."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "no file",
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           ", ".join("`%s`" % n
                     for n in af["files_absent_from_the_validation_record"])
           or "No file",
           led["ledger_proved_items"], led["paper_proved_items"],
           led["ledger_open_items"], led["paper_open_items"],
           led["ledger_no_go_items"], led["paper_no_go_headings"],
           len(led["open_items_absent_from_the_ledger"]),
           len(led["no_go_headings_absent_from_the_ledger"])),
        "",
        "**The drill.** The instrument self-tests **%d** properties before "
        "the gate runs, **%d** of them failing. **%d** defects were planted "
        "one at a time: **%d** caught by the counter they attack, **%d** "
        "missed, **%d** malformed, %d caught only by another counter; %d of "
        "%d controls left the gate undisturbed. Two defects aim at "
        "non-vacuity entries rather than failure counters, because last "
        "round's headline was a law whose second half was only an "
        "observation."
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
        print(json.dumps({"tool": "src69_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src69_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
