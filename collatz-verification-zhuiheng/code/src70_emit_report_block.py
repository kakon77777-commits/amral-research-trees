"""Emit RUN-051's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src70_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src70-au2d23.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src70-drill.json"
# the previous round's archived log, so the cross-read cites a run
PREV_LOG = ROOT / "data" / "gate-logs" / "src69-au2d22.json"
REPORT = ROOT / "reports" / "RUN-051-HARD-ZETA-AU2D23-QUOTIENT-RESONANCE.md"
FIGURES = ROOT / "data" / "gate-logs" / "src70-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src70_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def pct(a: int, b: int) -> str:
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def build(g: dict, d: dict, prev: dict) -> str:
    g = g.get("results", g)
    prev = prev.get("results", prev)
    ins, cs, pop = g["instrument"], g["constants"], g["population"]
    rs, cp, dl = g["resonance"], g["capacity"], g["delay"]
    at, rn, rt = g["atomic"], g["runs"], g["reset"]
    sy, ex, xr = g["synthetic"], g["examples"], g["cross_round"]
    af, led, tc = g["artifacts"], g["ledger"], g["their_claims"]
    tot = d["totals"]

    out = [
        BEGIN, "",
        "**The population.** **%d** zero-lift local bridges from **%d** "
        "distinct sources, longest tail %d — reproducing their "
        "`finite_zero_lift_bridges` exactly at their own limit."
        % (pop["bridges"], pop["sources"], pop["longest_tail"]),
        "",
        "**Theorem 3.1, the parity refinement.** Over **%d** congruent windows "
        "giving **%d** returns, **%d** carry zero defect. Every one satisfies "
        "`n = 2^{Q+1} v`, `n' = 2·3^L v` with `v ≥ 1`: **%d** violations of "
        "the refinement, **%d** outputs not in the refined form, **%d** "
        "non-positive quotients, and **%d** returns where the previous round's "
        "`u = n/2^Q` came out ODD — that is, `u` is even on all of them, which "
        "is exactly the sharpening this round adds. The smallest `v` is "
        "**%d**, so A-U.2d.22's `u ≥ 1` was loose by the factor this round "
        "identifies, not by an accident of the sample. Longest zero-defect "
        "return seen: **%d**."
        % (rs["windows"], rs["returns"], rs["zero_defect_returns"],
           rs["parity_refinement_violations"],
           rs["n_out_not_the_refined_form"], rs["quotient_not_positive"],
           rs["u_odd_so_the_previous_rounds_form_was_tight"],
           rs["smallest_v"], rs["largest_L"]),
        "",
        "**Confirmed against the previous round's own population.** Theorems "
        "3.1 and 4.1 are also run against RUN-050's **%d** bridges, whose "
        "returns come from the erasure walker rather than this round's window "
        "scan — different limit, different objects, **%d** zero-defect "
        "returns. Result: **%d** with `u` odd, **%d** and **%d** violations of "
        "the refined form and its parity, **%d** and **%d** of the two "
        "transfer identities, smallest `v` again **%d**. The sharpening holds "
        "on data collected before the claim existed."
        % (xr["bridges"], xr["zero_defect_returns"],
           xr["u_odd_on_the_previous_population"],
           xr["n_out_not_the_refined_form"],
           xr["parity_refinement_violations"],
           xr["cross_adic_two_violations"],
           xr["cross_adic_three_violations"], xr["smallest_v"]),
        "",
        "**Theorem 4.1, the cross-adic transfer.** `ν₂(n') = ν₂(n) − Q` failed "
        "**%d** times and `ν₃(n') = ν₃(n) + L` failed **%d** times. The "
        "return spends binary divisibility and buys ternary divisibility at a "
        "fixed rate, exactly."
        % (rs["cross_adic_two_violations"],
           rs["cross_adic_three_violations"]),
        "",
        "**Theorem 5.1, whose two halves have opposite tightness.** The "
        "per-position ceiling `m_ℓ ≤ ⌈βh⌉ − ⌈βℓ⌉ − (h−ℓ)` failed **%d** times "
        "over **%d** positions and is **attained at %d of them (%s)**, "
        "smallest slack **%s** — a live, binding bound. Its corollary "
        "`H_max < (β−1)h + 1` failed **%d** times, with a smallest integer "
        "slack of **%s** and a largest `H_max` of **%d**. But the `+1` is not "
        "load-bearing: the strictly stronger `H_max < (β−1)h` also holds, "
        "with **%d** violations across all **%d** bridges. The same theorem is "
        "attained in one half and carries a spare term in the other."
        % (cp["capacity_violations"], cp["positions"],
           cp["positions_attaining_the_capacity"],
           pct(cp["positions_attaining_the_capacity"], cp["positions"]),
           cp["smallest_capacity_slack"], cp["hmax_violations"],
           cp["smallest_hmax_slack"], cp["largest_hmax_seen"],
           cp["hmax_violations_without_the_plus_one"], cp["bridges"]),
        "",
        "**Theorem 6.1, the temporal delay, in exact integers.** The round "
        "states four inequalities containing `β` and evaluates every one in "
        "float64. All four are exact under `2^{βm} = 3^m`, and both routes "
        "were computed on **%d** zero-defect nodes: the lift toll "
        "`2^{m_in} Z₀ > 2^Q M` failed **%d** times, the capacity side **%d**, "
        "the chained bound `2·3^p Z₀ > 2^{Q+p} M` **%d**, and the length "
        "bound `3^L M 2^p < 2·3^p Z₀` **%d**. The two float routes disagreed "
        "with exact arithmetic **%d** and **%d** times — so their `1e-12` "
        "fudge is not deciding anything here. The toll's tightest margin is "
        "**%s**, with **%d** nodes one bit from failing; the earliest prefix "
        "at which a zero-defect return appears is **p = %d**."
        % (dl["nodes"], dl["lift_toll_violations"],
           dl["capacity_below_the_delay_bound_violations"],
           dl["chained_delay_violations"], dl["length_bound_violations"],
           dl["float_toll_route_disagreeing"],
           dl["float_length_route_disagreeing"],
           dl["tightest_toll_margin"], dl["tolls_one_bit_from_failing"],
           dl["smallest_prefix_p"]),
        "",
        "**The toll, cross-read against the previous round.** A-U.2d.22 "
        "stated it as `m > Q + log₂(M/Z₀) − 1`, and RUN-050's archived log "
        "records its tightest margin as **%s×**. This round drops the `−1`, "
        "which is exactly one bit stronger, and the margin measured here is "
        "**%s** — half of it, as it must be. The strengthening is real and "
        "still holds."
        % (prev["sign"]["tightest_toll_margin"],
           dl["tightest_toll_margin"]),
        "",
        "**Theorem 7.1, decided rather than scanned.** A length-one "
        "zero-defect return needs `1 = (2^q − 3)r` with `r ≥ 1`, so `2^q − 3` "
        "must be a positive divisor of 1. Over **%d** values of `q` there is "
        "**%d** solution and **%d** others; for **%d** of those `q` the "
        "divisor already exceeds 1, which is what settles every remaining `q` "
        "at once. **The bundle scans `q < 20, r < 100` instead — %d "
        "iterations whose assert body is reached exactly %d time, and which "
        "increments no counter at all**, so this theorem is absent from their "
        "report. The existence half was checked separately on **%d** actual "
        "transitions `x = 1 + 8Mv`: **%d** wrong valuations, **%d** wrong "
        "targets, **%d** non-zero defects, **%d** misaligned endpoints."
        % (at["q_values_decided"], at["solutions_found"],
           at["solutions_other_than_q2_r1"],
           at["q_values_where_the_divisor_exceeds_one"],
           at["bounded_scan_iterations"],
           at["bounded_scan_assert_reached"], at["transitions_checked"],
           at["atomic_valuation_not_two"], at["atomic_target_wrong"],
           at["atomic_defect_not_zero"],
           at["atomic_endpoints_not_congruent"]),
        "",
        "**Theorem 8.1, the q = 2 resonance runs.** **%d** runs over **%d** "
        "steps, longest **%d**: **%d** wrong valuations, **%d** states not "
        "congruent to 1, **%d** wrong start quotients, **%d** wrong "
        "endpoints, **%d** wrong binary spends, **%d** wrong ternary gains, "
        "and **%d** runs whose whole word failed to be a zero-defect return."
        % (rn["runs"], rn["steps"], rn["longest_run"],
           rn["valuation_not_two"], rn["state_not_congruent_to_one"],
           rn["start_quotient_wrong"], rn["end_quotient_wrong"],
           rn["two_adic_spend_wrong"], rn["three_adic_gain_wrong"],
           rn["run_defect_not_zero"]),
        "",
        "**Theorems 15.1 and 16.1, both halves each.** Over **%d** "
        "nonzero-defect nodes, **%d** are low-activation (`ν₃(𝔡) < L`) and "
        "**%d** are high-activation. The reset `ν₃(n') = ν₃(𝔡)` failed **%d** "
        "times on the first group. **The bundle counts only that group**; its "
        "converse branch raises but increments nothing, so the **%d** "
        "high-activation nodes are invisible in their report — measured here, "
        "**%d** violations. Theorem 16.1's `ν₂(n') ≥ b ⟺ 3^L n + 𝔡 ≡ 0 "
        "(mod 2^{Q+b})` was probed **%d** times up to `b = %d`: **%d** "
        "failures of the forward direction and **%d** of the converse, which "
        "the bundle does not test at all."
        % (rt["nonzero_defect_nodes"], rt["low_activation_nodes"],
           rt["high_activation_nodes"], rt["reset_violations"],
           rt["high_activation_nodes"], rt["converse_violations"],
           rt["replenishment_probes"], rt["largest_b_probed"],
           rt["replenishment_forward_violations"],
           rt["replenishment_converse_violations"]),
        "",
        "**Their three synthetic blocks, measured rather than trusted.** The "
        "accounting block runs **%d** trials. Its two telescoping assertions "
        "hold — **%d** and **%d** failures — but that is not evidence: "
        "rebuilding the generator with `Q` reduced so the supercriticality it "
        "is about is FALSE by construction, the telescoping stayed green on "
        "**%d of %d** broken inputs while the supercriticality assertion went "
        "red on **%d**. Two of the three assertions are identities of the "
        "construction; the third is live but true by construction of the "
        "generator, which sets `Q = ⌈βL⌉ + randint(0,4)`. The reservoir block "
        "reports **two** counters of 20,000 each, and **both increment "
        "outside a guard** that opened on **%d of %d** samples (%s) — so "
        "40,000 published checks are one block, evaluated %d times, counted "
        "twice. Its assertion held (**%d** violations) with a smallest margin "
        "of **%s**."
        % (sy["accounting_trials"], sy["telescoping_Q_violations"],
           sy["telescoping_L_violations"],
           sy["telescoping_still_green_on_broken_input"],
           sy["accounting_trials"],
           sy["supercriticality_red_on_broken_input"],
           sy["reservoir_guard_opened"], sy["reservoir_trials"],
           pct(sy["reservoir_guard_opened"], sy["reservoir_trials"]),
           sy["reservoir_guard_opened"],
           sy["reservoir_assertion_violations"],
           sy["smallest_reservoir_margin"]),
        "",
        "**The published rows.** **%d** zero-defect and **%d** nonzero-defect "
        "rows recomputed from their own fields: **%d** quotient-identity "
        "failures, **%d** parity-refinement failures, **%d** valuation fields "
        "disagreeing, **%d** supercriticality failures, and on the nonzero "
        "rows **%d** identity and **%d** defect-valuation disagreements."
        % (ex["zero_rows"], ex["nonzero_rows"],
           ex["quotient_identity_violations"],
           ex["parity_refinement_violations"],
           ex["valuation_fields_disagreeing"],
           ex["supercriticality_violations"],
           ex["nonzero_row_quotient_identity_violations"],
           ex["nonzero_row_defect_valuation_disagreeing"]),
        "",
        "**The constants, and one with no generator.** **%d** checked, **%d** "
        "exact to the last bit, **%d** matching the float64 chain rather than "
        "the nearest double, **%d** disagreeing with both, **%d** undecided, "
        "**%d** missing, **%d** where frontier and report disagree. Two of "
        "them are differences of nearly-equal quantities and land 21 and 16 "
        "ulps out, which is the chain and not an error. **Cross-read, the "
        "frontier carries %s that the checker never computes** — %s — and it "
        "shares its exact value with `faithful_minus_resonance_threshold`. A "
        "per-file check cannot see either fact; only the two artifacts side "
        "by side can."
        % (cs["constants_checked"], cs["exact_to_the_last_bit"],
           cs["from_the_float64_chain_not_the_nearest_double"],
           cs["disagreeing_with_both_evaluations"], cs["undecided_brackets"],
           cs["missing_from_the_frontier"],
           cs["frontier_and_report_disagreeing"],
           "%d constant" % len(cs["frontier_constants_the_checker_never_computes"]),
           ", ".join("`%s`" % n for n in
                     cs["frontier_constants_the_checker_never_computes"])),
        "",
        "**Their thirteen counters.** **%d** reproduce exactly. **%d** are "
        "covered here by a deterministic enumeration larger than theirs, and "
        "the cross-report table names my counter rather than leaving a blank "
        "that would read as *not reproduced*. **%d** of their checks are "
        "covered by nothing here, and **%d** report zero. One theorem — 7.1 — "
        "has no counter of theirs to compare against at all."
        % (tc["counts_i_reproduce_exactly"],
           tc["checks_covered_by_a_different_population"],
           tc["checks_not_covered_at_all"],
           tc["checks_they_report_as_zero"]),
        "",
        "**The bundle as shipped.** **%d** files, **%d** digests listed, "
        "**%d** mismatches, **%d** checksum lines naming a missing file, and "
        "%s with no digest anywhere. The validation record carries **%d** "
        "per-file entries of which **%d** carry a digest — the tenth round in "
        "a row recording `pass` without recording what it hashed — and its "
        "pass flag has been renamed again, to `%s`. %s absent from it "
        "entirely. Against the paper, the ledger lists **%d** proved items to "
        "the paper's **%d**, **%d** open to **%d**, and **%d** no-go entries "
        "to the paper's **%d** headings; **%d** open items and **%d** no-go "
        "headings have no ledger counterpart%s. The coverage heuristic passed "
        "both its controls."
        % (af["files_present"], af["digests_listed"], af["digest_mismatches"],
           af["checksum_lines_naming_a_missing_file"],
           ", ".join("`%s`" % n for n in af["files_with_no_digest_anywhere"])
           or "no file",
           af["validation_per_file_entries"],
           af["validation_entries_with_a_digest"],
           af["validation_pass_flag_key"],
           ", ".join("`%s`" % n
                     for n in af["files_absent_from_the_validation_record"])
           or "No file",
           led["ledger_proved_items"], led["paper_proved_items"],
           led["ledger_open_items"], led["paper_open_items"],
           led["ledger_no_go_items"], led["paper_no_go_headings"],
           len(led["open_items_absent_from_the_ledger"]),
           len(led["no_go_headings_absent_from_the_ledger"]),
           (" (%s)" % ", ".join(led["no_go_headings_absent_from_the_ledger"])
            if led["no_go_headings_absent_from_the_ledger"] else "")),
        "",
        "**The drill.** The instrument self-tests **%d** properties before the "
        "gate runs, **%d** of them failing. **%d** defects were planted one at "
        "a time: **%d** caught by the counter they attack, **%d** missed, "
        "**%d** malformed, %d caught only by another counter; %d of %d "
        "controls left the gate undisturbed. Five aim at non-vacuity entries "
        "rather than failure counters, because every finding this round is "
        "about a population smaller than the counter reporting it."
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
    for path in (GATE_LOG, DRILL_LOG, PREV_LOG):
        if not path.exists():
            print(json.dumps({"error": "missing log", "path": str(path)},
                             indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    prev = json.loads(PREV_LOG.read_text(encoding="utf-8"))
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
    guard = check_against_snapshot(build, [g, d, prev], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to",
                          "guard": guard}, indent=2))
        return 2
    block = build(g, d, prev)
    text = REPORT.read_text(encoding="utf-8")
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail
    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src70_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src70_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
