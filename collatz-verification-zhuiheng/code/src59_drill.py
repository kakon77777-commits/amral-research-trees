"""RUN-040 mutation drill for `src59_block_hierarchy.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The accumulated discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- a defect whose anchor matches zero or many
    places was aimed at nothing and is reported as malformed, never as a catch;
  * "the mutation changes nothing" is malformed too. It says the branch is
    unreachable on real data, or the defect is too weak to matter, and a defect
    a correct check tolerates measures nothing at all;
  * a guard is a verdict. A defect that empties a population is caught by the
    non-vacuity list, and one that adds an unread counter by the classification
    guard -- both count, and both are read here;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back. A killed drill leaves its defect behind, so
    the next run restores from the sidecar first and says that it did.

Usage:
    python code/src59_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src59_block_hierarchy.py"
LIMIT = "600"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the exact hierarchy: integer arithmetic, so every defect must bite ---
    ("D1_the_floor_of_beta_m_is_off_by_one",
     "    k = (3 ** m).bit_length() - 1\n"
     "    assert 2 ** k <= 3 ** m < 2 ** (k + 1), \"bit_length is not the floor\"",
     "    k = (3 ** m).bit_length()\n"
     "    assert k >= 0, \"bit_length is not the floor\"",
     "hierarchy.q_floor_disagreeing_with_floor_beta_m"),
    ("D2_the_negative_block_count_uses_the_wrong_binomial",
     "    return sum((Fraction(comb(Q - 1, m - 1), 3 * 2 ** Q)",
     "    return sum((Fraction(comb(Q - 1, m), 3 * 2 ** Q)",
     "hierarchy.C_minus_disagreeing_with_the_binomial_sum"),
    ("D3_the_positive_block_gap_loses_its_extra_power_of_two",
     "    return Fraction(2 ** (q + 1), 3 ** m) - 1",
     "    return Fraction(2 ** q, 3 ** m) - 1",
     "hierarchy.gamma_disagreeing_with_its_definition"),
    ("D4_the_block_exponent_divides_by_two_instead_of_three",
     "    return (1 + 1 / gamma_m(m, q)) * c_minus(m, q) / 3",
     "    return (1 + 1 / gamma_m(m, q)) * c_minus(m, q) / 2",
     "hierarchy.alpha_hat_disagreeing_with_corollary_8_2"),
    ("D5_the_finance_factor_subtracts_where_it_should_add",
     "    return (1 + 1 / gamma_m(m, q)) * c_minus(m, q) / 3\n",
     "    return (1 - 1 / gamma_m(m, q)) * c_minus(m, q) / 3\n",
     "hierarchy.alpha_hat_disagreeing_with_corollary_8_2"),
    ("D6_the_source_floor_formula_flips_a_sign",
     "    return (theta - alpha) / (1 - alpha)",
     "    return (theta + alpha) / (1 - alpha)",
     "hierarchy.mu_dense_disagreeing_with_the_section_15_formula"),
    ("D7_the_word_total_runs_one_past_the_subcritical_range",
     "    return sum(comb(Q - 1, m - 1) for Q in range(m, q + 1))",
     "    return sum(comb(Q - 1, m - 1) for Q in range(m, q + 2))",
     "hierarchy.B_star_outside_its_bracket"),
    ("D8_the_two_over_seven_term_loses_its_two_CRT_phases",
     "    lo = hi = Fraction(2 * n_minus(m, q), 7)",
     "    lo = hi = Fraction(n_minus(m, q), 7)",
     "hierarchy.B_star_outside_its_bracket"),
    ("D9_the_additive_constant_drops_its_terminal_positions",
     "    return widen(f * k_lo + s_lo / g + Fraction(m - 1, 7),\n"
     "                 f * k_hi + s_hi / g + Fraction(m - 1, 7), 20)",
     "    return widen(f * k_lo + s_lo / g, f * k_hi + s_hi / g, 20)",
     "hierarchy.B_star_outside_its_bracket"),
    ("D10_the_published_exponent_float_is_compared_against_a_doubled_value",
     "        d_ulps = bits(row[\"alpha_hat_float\"]) - bits(float(ah))",
     "        d_ulps = bits(row[\"alpha_hat_float\"]) - bits(float(ah) * 2)",
     "hierarchy.alpha_hat_float_not_the_nearest_double"),
    ("D11_theta_star_is_built_from_the_wrong_diophantine_exponent",
     "    i_lo, i_hi = i_beta_bracket()\n    theta = 1 / (RHO_STAR + 1)",
     "    i_lo, i_hi = i_beta_bracket()\n    theta = 1 / (RHO_STAR + 2)",
     "hierarchy.mu_dense_disagreeing_with_the_section_15_formula"),

    # --- the record set ---
    ("D12_a_running_minimum_admits_values_that_are_not_records",
     "        if best is None or a < best:",
     "        if best is None or a < best * 2:",
     "records.record_set_disagreeing_with_the_report"),

    # --- the generating identity ---
    ("D13_each_level_is_truncated_at_its_own_q_m",
     "            for k in range(1, ceiling - a + 1):",
     "            for k in range(1, q + 2 - a):",
     "generating.lemma_10_1_violations"),
    ("D14_the_composition_count_is_taken_at_the_wrong_argument",
     "            if compositions(Q, m) != comb(Q - 1, m - 1):",
     "            if compositions(Q, m) != comb(Q - 1, m):",
     "generating.N_m_Q_disagreeing_with_composition_enumeration"),

    # --- the Chernoff half ---
    ("D15_the_capacity_bound_is_tightened_a_hundredfold",
     "        rhs_lo = lo / 3",
     "        rhs_lo = lo / 300",
     "chernoff.chernoff_capacity_violations"),
    ("D16_the_chernoff_optimum_uses_the_wrong_sign_on_log_two",
     "    ts_lo = lb_lo - l2_hi - lm_hi          # t* = ln beta - ln2 - ln(beta-1)",
     "    ts_lo = lb_lo + l2_hi - lm_hi          # t* = ln beta - ln2 - ln(beta-1)",
     "chernoff.optimum_identity_violations"),
    ("D17_the_rate_function_comes_out_half_its_size",
     "    return widen(lo, hi, 40)",
     "    return widen(lo / 2, hi / 2, 40)",
     "constants.I_beta_outside_its_bracket"),

    # --- the Diophantine half ---
    ("D18_the_convexity_step_is_demanded_a_hundred_times_over",
     "        if p_lo - 1 < l2_hi * x and p_hi - 1 < l2_lo * x:",
     "        if p_lo - 1 < l2_hi * x * 100 and p_hi - 1 < l2_lo * x * 100:",
     "diophantine.convexity_violations"),
    ("D19_the_phase_gap_is_required_to_beat_a_thousand_log_twos",
     "        if g < l2_lo * ep_lo:",
     "        if g < l2_lo * ep_lo * 1000:",
     "diophantine.gamma_below_log2_times_epsilon_plus"),
    ("D20_the_one_sided_phase_is_read_from_the_wrong_side",
     "        ep_lo, ep_hi = (q + 1) - b_hi * m, (q + 1) - b_lo * m",
     "        ep_lo, ep_hi = b_lo * m - q, b_hi * m - q",
     "diophantine.gamma_below_log2_times_epsilon_plus"),
    ("D35_the_one_sided_phase_is_taken_a_whole_step_too_high",
     "        ep_lo, ep_hi = (q + 1) - b_hi * m, (q + 1) - b_lo * m",
     "        ep_lo, ep_hi = (q + 2) - b_hi * m, (q + 2) - b_lo * m",
     "diophantine.epsilon_plus_outside_the_unit_interval"),

    # --- the cross-round formula ---
    ("D21_an_inherited_exponent_is_quoted_wrongly",
     "    inherited = [Fraction(1, 6), Fraction(1, 9), Fraction(4, 45), ALPHA_27]",
     "    inherited = [Fraction(1, 5), Fraction(1, 9), Fraction(4, 45), ALPHA_27]",
     "inherited.disagreeing_with_the_formula"),

    # --- the orbit theorems ---
    ("D22_the_block_total_valuation_is_one_exponent_short",
     "        Q = sum(w[j:j + m])",
     "        Q = sum(w[j:j + m - 1])",
     "orbits.theorem_3_1_violations"),
    ("D23_the_block_correction_omits_its_last_factor",
     "        for t in range(j, j + m):\n            P *= 1 + Fraction(1, 3 * v[t])",
     "        for t in range(j, j + m - 1):\n            P *= 1 + Fraction(1, 3 * v[t])",
     "orbits.theorem_3_1_violations"),
    ("D24_the_boundary_error_bound_is_made_negative",
     "    return Fraction(m, y) + Fraction(3 * m, 14 * y) * e",
     "    return Fraction(-10 ** 6) + Fraction(0, 14 * y) * e",
     "orbits.theorem_4_1_violations"),
    ("D25_the_suffix_minimum_premise_stops_being_enforced",
     "    while L + 1 < len(values) and values[L + 1] >= y:",
     "    while L + 1 < len(values) and values[L + 1] > 0:",
     "orbits.theorem_4_1_violations"),
    ("D26_the_finance_inequality_is_scaled_past_its_slack",
     "            if gamma_m(m, q_m) * s_pos > s_neg + e_bound(m, y):",
     "            if gamma_m(m, q_m) * s_pos * 1000 > s_neg + e_bound(m, y):",
     "orbits.theorem_5_1_violations"),
    ("D27_the_exact_word_capacity_loses_four_powers_of_two",
     "                       + ln_any(1 + Fraction(3 * 2 ** (Q + 1) * L, y))[1]",
     "                       + ln_any(1 + Fraction(3 * 2 ** (Q + 1) * L, y * 10 ** 9))[1]",
     "orbits.theorem_6_1_violations"),
    ("D28_injectivity_is_reported_inside_out",
     "        \"distinct\": len(set(strict)) == len(strict),",
     "        \"distinct\": len(set(strict)) != len(strict),",
     "orbits.segments_with_a_repeated_state"),
    ("D29_the_source_cylinder_is_read_at_too_fine_a_modulus",
     "            if len({x % (2 ** (Q + 1)) for x in xs}) > 1:",
     "            if len({x % (2 ** (Q + 2)) for x in xs}) > 1:",
     "cylinders.words_spanning_more_than_one_class_mod_2Qplus1"),
    ("D30_the_three_sieve_phase_count_is_read_at_too_fine_a_modulus",
     "            if len({x % (3 * 2 ** (Q + 1)) for x in xs}) > 2:",
     "            if len({x % (9 * 2 ** (Q + 2)) for x in xs}) > 2:",
     "cylinders.words_spanning_more_than_two_classes_mod_3_2Qplus1"),

    # --- artifacts ---
    ("D31_a_digest_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),

    # --- the guards themselves ---
    ("D32_a_population_the_theorems_depend_on_is_emptied",
     "            if L >= y and L >= m:",
     "            if L >= y and L >= 10 ** 9:",
     "orbits.theorem_7_1_checked"),
    ("D33_the_orbit_scan_is_reduced_to_a_single_source",
     "    for y in range(7, limit, 2):\n        if y % 3 == 0:\n"
     "            continue                       # post-entry sources are 3-free",
     "    for y in range(7, 9, 2):\n        if y % 3 == 0:\n"
     "            continue                       # post-entry sources are 3-free",
     "orbits."),
    ("D34_a_counter_is_added_that_no_list_classifies",
     "        \"levels\": 0,\n        \"q_floor_disagreeing_with_floor_beta_m\": 0,",
     "        \"levels\": 0, \"a_counter_nothing_reads\": 0,\n"
     "        \"q_floor_disagreeing_with_floor_beta_m\": 0,",
     "hierarchy.a_counter_nothing_reads"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
    ("N2_a_blank_line_is_not_a_defect", b"\n"),
]

# defects whose whole point is that the gate should REFUSE rather than answer
FINDING_ROBUSTNESS: dict[str, str | None] = {}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle),
             "--limit", LIMIT],
            capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
    except subprocess.TimeoutExpired:
        return {"passed": False,
                "failures": ["__the gate did not terminate__"], "hung": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False,
                "failures": ["__the gate did not produce JSON__"],
                "stderr_tail": (proc.stderr or "")[-400:]}


def _complaints(res: dict) -> list[str]:
    """Three channels, all of them verdicts: a named failure, an emptied
    population, and a counter no list classifies."""
    return (list(res.get("failures", []))
            + list(res.get("empty_populations", []))
            + list(res.get("counters_not_in_the_failure_or_population_lists",
                           [])))


def _same_verdict(a: dict, b: dict) -> bool:
    def strip(d: dict) -> dict:
        return {k: v for k, v in d.items() if k not in ("bundle",)}
    return (json.dumps(strip(a), sort_keys=True, default=str)
            == json.dumps(strip(b), sort_keys=True, default=str))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=pathlib.Path, required=True)
    args = ap.parse_args()

    backup = GATE.with_suffix(GATE.suffix + ".pristine")
    interrupted = False
    if backup.exists():
        GATE.write_bytes(backup.read_bytes())
        interrupted = True
    snapshot = GATE.read_bytes()
    backup.write_bytes(snapshot)

    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name, "limit": LIMIT,
        "a_previous_run_was_interrupted_and_the_gate_was_restored": interrupted,
        "baseline": {"passed": base.get("passed"),
                     "failures": base.get("failures"),
                     "empty_populations": base.get("empty_populations")},
        "defects": {}, "controls": {},
    }
    if not base.get("passed"):
        report["ok"] = False
        report["note"] = "the gate is not green before anything was planted"
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 2

    raw = snapshot.decode("utf-8")

    # pre-flight: every anchor must name exactly one place BEFORE anything runs
    aim = {name: raw.count(old) for name, old, _new, _e in DEFECTS}
    report["anchors_matching_once"] = sum(1 for v in aim.values() if v == 1)
    report["anchors_not_unique"] = {k: v for k, v in aim.items() if v != 1}

    for name, old, new, expected in DEFECTS:
        if aim[name] != 1:
            report["defects"][name] = {
                "caught": False, "anchor_matches": aim[name],
                "malformed": "the anchor names %d places, so nothing was "
                             "planted" % aim[name]}
            continue
        try:
            GATE.write_bytes(raw.replace(old, new).encode("utf-8"))
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(snapshot)

        if res.get("hung"):
            report["defects"][name] = {
                "caught": False, "malformed": "the gate did not terminate"}
            continue
        if "__the gate did not produce JSON__" in res.get("failures", []):
            report["defects"][name] = {
                "caught": False, "malformed": "the gate raised",
                "stderr_tail": res.get("stderr_tail", "")[-200:]}
            continue
        if _same_verdict(base, res):
            report["defects"][name] = {
                "caught": False,
                "malformed": "the mutation changes nothing",
                "note": "either the branch is unreachable on real data or the "
                        "defect is too weak to matter; a defect a correct "
                        "check tolerates is no evidence about the check"}
            continue
        said = _complaints(res)
        report["defects"][name] = {
            "caught": any(expected in c for c in said),
            "expected_named": expected,
            "reported": said[:4],
            "caught_by_something_else_only": (bool(said) and
                                              not any(expected in c
                                                      for c in said)),
        }

    for name, addition in CONTROLS:
        try:
            GATE.write_bytes(snapshot + addition)
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(snapshot)
        report["controls"][name] = {
            "undisturbed": bool(res.get("passed")) and not _complaints(res),
            "reported": _complaints(res)[:4],
        }

    caught = sum(1 for v in report["defects"].values() if v.get("caught"))
    malformed = sum(1 for v in report["defects"].values() if v.get("malformed"))
    report["totals"] = {
        "defects": len(DEFECTS), "caught": caught, "malformed": malformed,
        "missed": len(DEFECTS) - caught - malformed,
        "caught_but_by_another_counter": sum(
            1 for v in report["defects"].values()
            if v.get("caught_by_something_else_only")),
        "controls": len(report["controls"]),
        "controls_undisturbed": sum(1 for c in report["controls"].values()
                                    if c["undisturbed"]),
    }
    # `suite_totals.py` reads a drill log through an enumerated list of key
    # shapes and REFUSES an unlisted one, because a rename once put seven drills
    # outside the published figure for seven rounds. So emit the shape it
    # already knows rather than adding another for it to learn.
    tot = report["totals"]
    report["counts"] = {
        "planted": tot["defects"],
        "caught_by_their_own_check": tot["caught"],
        "missed": tot["missed"],
        "malformed": tot["malformed"],
        "controls": tot["controls"],
        "controls_undisturbed": tot["controls_undisturbed"],
    }
    report["ok"] = (caught == len(DEFECTS)
                    and all(c["undisturbed"]
                            for c in report["controls"].values()))
    if GATE.read_bytes() == snapshot:
        backup.unlink()
    else:
        report["ok"] = False
        report["note"] = "the gate did not come back byte-identical"
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
