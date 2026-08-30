"""Emit RUN-042's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.
Usage:  python code/src61_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src61-au2d14.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src61-drill.json"
REPORT = ROOT / "reports" / "RUN-042-HARD-ZETA-AU2D14-SPARSE-SUPPORT.md"
FIGURES = ROOT / "data" / "gate-logs" / "src61-emitter-figures.json"
BEGIN = ("<!-- BEGIN GENERATED measured block: "
         "python code/src61_emit_report_block.py -->")
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    g = g.get("results", g)
    ex, ps, idn = g["exponents"], g["psi_identity"], g["identities"]
    suf, env, bl = g["suffix"], g["envelope"], g["backlog"]
    ce, cr, pr = g["counterexample"], g["criticality"], g["printed"]
    ar, led, tc = g["artifacts"], g["ledger"], g["their_claims"]

    out = [
        BEGIN, "",
        "**The constants, exact against the float64 route the artifact took.** "
        "Taking `rho* = 4.1164` as the decimal it is written as, every constant "
        "in this round is an exact rational.",
        "",
        "| constant | exact rational | published | vs exact | vs float64 chain |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in ex["rows"]:
        out.append("| `%s` | `%s` | %s | %s | %s |" % (
            r["name"], r["exact"], r["published"],
            "exact" if r["ulps_vs_exact"] == 0
            else "%+d ulp" % r["ulps_vs_exact"],
            "exact" if r["ulps_vs_float64_chain"] == 0
            else "%+d ulp" % r["ulps_vs_float64_chain"]))
    out += [
        "",
        "%d constants checked: **%d** disagree with both readings of their own "
        "formula, %d are the nearest double to the exact rational, and %d are "
        "what the same formula gives in float64 from an already-rounded parent. "
        "`chi` is the outlier again, for the reason RUN-041 named: `5 sigma - 4` "
        "collapses 4.18 to 0.18, a **%s-fold** loss of magnitude."
        % (ex["constants_checked"], ex["disagreeing_with_both_evaluations"],
           ex["exact_to_the_last_bit"],
           ex["from_the_float64_chain_not_the_exact_rational"],
           ex["cancellation_factor_in_five_sigma_minus_four"]),
        "",
        "**One quantity, two values, same object.** `psi(k) = "
        "(k-(1-theta*))/theta*` at `k = sigma*` is `theta*/(1+theta*)`, which is "
        "exactly `1 - sigma*`. The identity holds: **%s**. The frontier stores "
        "both under `at_old_sigma`, and they differ by **%d ulp** — `psi` is "
        "`%r` and `one_minus_sigma` is `%r`, while the exact value is `%s = "
        "%s`. Each reproduces its own float64 route bit-for-bit (%d of 2), so "
        "this is one number computed two ways and stored twice, not a wrong "
        "value."
        % (ps["identity_holds_exactly"],
           ps["ulps_between_the_two_published_values"],
           [r["published"] for r in ex["rows"]
            if r["name"] == "at_old_sigma.psi"][0].strip("'"),
           [r["published"] for r in ex["rows"]
            if r["name"] == "at_old_sigma.one_minus_sigma"][0].strip("'"),
           ps["exact_value"], ps["exact_decimal"][:20],
           ps["each_matches_its_own_float64_route"]),
        "",
        "**The exponent algebra, as identities in the symbols.** Over %d random "
        "rational parameter pairs: Theorem 4.1's step `rho/(rho+1) = 1-theta` "
        "**%d** violations; Theorem 9.1's `2k-1-chi(k) = zeta(k)` **%d**; "
        "section 10's inversion of the backlog bound for `psi` **%d**; and "
        "`chi(k) > 0` exactly above `4/5` **%d**. `chi(4/5) = %s` and "
        "`zeta(4/5) = %s`."
        % (idn["trials"], idn["rho_over_rho_plus_one_violations"],
           idn["trichotomy_exponent_identity_violations"],
           idn["psi_from_theorem_4_1_violations"],
           idn["chi_threshold_violations"], idn["chi_at_four_fifths"],
           idn["zeta_at_four_fifths"]),
        "",
        "**Section 3 has a real population, unlike last round's B-side.** A "
        "B source does not occur on a convergent orbit; a suffix minimum does. "
        "Across %d orbit windows, **%d** suffix minima were found and every one "
        "of them satisfies Theorem 3.1 (`q_{s+1} = 1`, **%d** violations) and "
        "Corollary 3.2 (`7, 11 mod 12`, **%d**). The equivalence the corollary "
        "rests on, `q = 1` iff `y = 3 mod 4` on an odd source, failed **%d** "
        "times; no source was divisible by 3 (**%d**); the ordinal floor "
        "`y^(j) >= 6j-1` failed **%d**; and the step the proof turns on, "
        "`Y_{s+1} > Y_s`, failed **%d**."
        % (suf["orbits"], suf["suffix_minima"],
           suf["theorem_3_1_violations"], suf["corollary_3_2_violations"],
           suf["q_one_not_equivalent_to_three_mod_four"],
           suf["sources_divisible_by_three"],
           suf["late_ordinal_floor_violations"],
           suf["successor_not_greater"]),
        "",
        "And a structural fact that explains RUN-041's zero: **all %d of them "
        "are A-renewals**, with **%d** having a delta crossing inside the "
        "window. A true suffix minimum with a first crossing would be a "
        "B-injection automatically — `Y_{e(s)} >= Y_s` by minimality, strict by "
        "injectivity — and there are **%d** of those. RUN-041 found 0 "
        "B-injections in 460,024 first-crossing intervals; this says why."
        % (suf["minima_that_are_A_renewals"],
           suf["minima_with_a_delta_crossing"],
           suf["B_injections_among_true_suffix_minima"]),
        "",
        "**The A envelope, sections 6 and 7, also on real orbits.** %d orbits "
        "carried two or more A-renewals (largest chain %d). `E_A = beta T - Q` "
        "disagreed with the direct `delta` difference **%d** times; the "
        "envelope was non-positive **%d** times; the exact product identity "
        "`z_A 2^Q = y_A 3^T prod(1+1/(3Y_j))` — written with no `beta` at all — "
        "failed **%d**; A-source values were non-increasing **%d** and their "
        "slacks **%d**; the `6j-1` floor **%d**. Theorem 7.1 in the form its "
        "proof gives, `6 A_N - 1 <= z_A`, was checked on all %d and failed "
        "**%d**."
        % (env["orbits_with_two_or_more_A_renewals"], env["largest_A_count"],
           env["E_A_disagreeing_with_beta_T_minus_Q"],
           env["A_envelope_not_positive"],
           env["envelope_product_identity_violations"],
           env["A_source_values_not_increasing"],
           env["delta_at_A_renewals_not_increasing"],
           env["theorem_7_1_floor_violations"],
           env["transfer_inequality_checked"],
           env["transfer_inequality_violations"]),
        "",
        "**The B-side theorems, as algebra.** Theorems 4.1 and 4.2 are "
        "conditional on a B source, so they were checked as implications "
        "between finite quantities at integer `rho`, where the root is exact "
        "and no bracket is needed. Over %d grid points: **%d** and **%d** "
        "violations, with the antecedent actually holding at %d and %d of "
        "them. Section 5's division and section 9's case split: **%d** and "
        "**%d** of %d."
        % (bl["grid_points"], bl["theorem_4_1_violations"],
           bl["theorem_4_2_violations"], bl["theorem_4_1_antecedent_holds"],
           bl["theorem_4_2_antecedent_holds"],
           bl["section_5_division_violations"],
           bl["trichotomy_case_split_violations"], bl["trichotomy_points"]),
        "",
        "**NO-GO 11.1, built rather than argued.** The claim is that a "
        "construction exists, so one was built: `t_j = 2^(j^2)`, records at "
        "those times, every intermediate above the next record. Enumerating "
        "the suffix minima of the result over %d levels — up to `log2 N = %d` "
        "— the record times disagreed with `t_j` **%d** times, the count "
        "disagreed with `sqrt(log2 N)` **%d**, the sequence failed to diverge "
        "**%d**, and an intermediate fell too low **%d**. At the largest `N` "
        "there are %d records."
        % (ce["levels"], ce["log2_of_the_largest_N"],
           ce["suffix_minimum_times_disagreeing_with_t_j"],
           ce["count_disagreeing_with_sqrt_log2_N"],
           ce["sequence_not_divergent"], ce["intermediate_value_too_small"],
           ce["count_at_the_largest_N"]),
        "",
        "**The criticality conversion, as the claim rather than the identity.** "
        "`delta_m/m = beta - K_m/m` is a rearrangement and testing it would "
        "measure nothing. What section 2.3 actually takes from the external "
        "input is that `liminf (m/K_m) = 1/beta` gives `limsup (K_m/m) = beta`. "
        "Over %d sequences that reciprocal relation failed **%d** times, the "
        "monotone conversion **%d**, and the CASP sign condition **%d**."
        % (cr["sequences"], cr["reciprocal_relation_violations"],
           cr["monotone_conversion_violations"], cr["casp_sign_violations"]),
        "",
        "**What the prose prints.** %d decimal instances across the paper and "
        "route map, **all %d followed by an ellipsis**. **%d** over-publish "
        "against the exact rational, %d are exact to every digit, %d is "
        "correctly rounded and %d truncated."
        % (pr["printed"], pr["printed_with_an_ellipsis"], pr["over_published"],
           pr["exact_to_every_digit"], pr["correctly_rounded"],
           pr["truncated"]),
        "",
        "**Artifacts — the three-round finding is fixed.** %d files, %d "
        "carrying a `CHECKSUMS` digest, **%d** mismatches, **%d** manifest "
        "lines naming a missing file. The source-validation record now carries "
        "**sha256 digests of its own**: %d entries, **%d with a digest**, and "
        "recomputing every one gives **%d** mismatches and **%d** naming a file "
        "that is not there. Its commit gate reports %s with **%d** entries not "
        "PASS. RUN-039, RUN-040 and RUN-041 each reported this record as "
        "digest-free; it no longer is. Files it does not list: %s — the first "
        "two cannot list themselves, and the third is covered by `CHECKSUMS`."
        % (ar["files_present"], ar["digests_listed"], ar["digest_mismatches"],
           ar["checksum_lines_naming_a_missing_file"],
           ar["validation_entries"], ar["validation_entries_with_a_digest"],
           ar["validation_digest_mismatches"],
           ar["validation_entries_naming_a_missing_file"],
           ar["validation_status"], ar["commit_gate_entries_not_pass"],
           ", ".join("`%s`" % n
                     for n in ar["files_absent_from_the_validation_record"])),
        "",
        "**Ledger coverage.** The paper lists %d proved items, %d explicitly "
        "open problems and %d numbered NO-GO heading; the ledger carries %d, "
        "%d and %d. It has an `open` key (%s). Open items with no trace in it: "
        "%s. NO-GO headings with no trace: %s."
        % (led["paper_proved_items"], led["paper_open_items"],
           led["paper_no_go_headings"], led["ledger_proved_items"],
           led["ledger_open_items"], led["ledger_no_go_items"],
           led["ledger_has_an_open_key"],
           json.dumps(led["open_items_absent_from_the_ledger"])
           if led["open_items_absent_from_the_ledger"] else "none",
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
        print(json.dumps({"tool": "src61_emit_report_block.py",
                          "mode": "check", "report_up_to_date": not stale,
                          "guard": guard, "ok": not stale},
                         indent=2, ensure_ascii=False))
        return 1 if stale else 0
    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src61_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard,
                      "ok": True}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
