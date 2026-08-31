"""RUN-046 mutation drill for `src65_lift_cocycle.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" is malformed, and it has four causes worth
    telling apart: unreachable, premise-empty, too weak, and mathematically
    identical to what it replaced. RUN-044 planted `2^q` for `2^-q` mod 3;
    RUN-045 shrank a modulus to a divisor. Both left the statement true;
  * from a GREEN baseline a defect must make a counter RISE. Four of RUN-045's
    defects deleted a check whose counter already read zero and were invisible;
  * a defect that makes the gate RAISE is malformed too, and the fix belongs in
    the gate, which must report rather than crash;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back.

Usage:
    python code/src65_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src65_lift_cocycle.py"
LIMIT = "35000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the exact ceiling, which every integer statement rests on ---
    ("D1_the_exact_ceiling_returns_the_floor",
     "    return (3 ** ell).bit_length() if ell else 0",
     "    return (3 ** ell).bit_length() - 1 if ell else 0",
     "instrument.failed"),
    ("D2_the_mechanical_increment_skips_a_level",
     "    return ceil_beta(ell) - ceil_beta(ell - 1)",
     "    return ceil_beta(ell) - ceil_beta(ell - 2)",
     "errors.instrument_raised"),
    ("D3_the_phase_power_uses_the_wrong_base",
     "    return Fraction(1 << ceil_beta(ell), 3 ** ell)",
     "    return Fraction(1 << ceil_beta(ell), 2 ** ell)",
     "instrument.failed"),
    ("D4_the_fixed_point_bracket_is_read_at_the_wrong_precision",
     "        f_lo, f_hi = (ell * n_lo) >> prec, (ell * n_hi) >> prec",
     "        f_lo, f_hi = (ell * n_lo) >> prec, (ell * n_hi) >> (prec - 1)",
     "ceiling.fixed_point_undecided"),
    ("D5_the_fixed_point_route_returns_the_floor_not_the_ceiling",
     "        exact = f_lo + 1                      # ceil, since beta*ell is irrational",
     "        exact = f_lo                          # ceil, since beta*ell is irrational",
     "ceiling.float_ceiling_disagreements"),

    # --- the suffix lift profile ---
    ("D6_the_suffix_sum_walks_the_word_forwards",
     "        run += word[h - ell]",
     "        run += word[ell - 1]",
     "lift.lift_negative"),
    ("D7_the_lift_subtracts_the_wrong_ceiling",
     "        out.append(run - ceil_beta(ell))",
     "        out.append(run - ceil_beta(ell + 1))",
     "lift.lift_negative"),

    # --- Theorem 6.1 ---
    ("D8_the_rank_one_upper_bound_is_tightened_past_the_source",
     "        if not X < Fraction(3 * Z + 1, 2):",
     "        if not X < Fraction(Z + 1, 2):",
     "lift.rank_one_upper_violations"),
    ("D9_the_rank_one_ordering_is_reversed",
     "        if not Z < X:",
     "        if not Z > X:",
     "lift.rank_one_lower_violations"),
    ("D10_the_left_record_is_required_above_the_endpoint",
     "        if not y < Z:",
     "        if not y > Z:",
     "lift.left_record_not_below_the_endpoint"),
    ("D11_the_first_tail_state_is_computed_without_the_plus_one",
     "        if X != (3 * y + 1) // 2 or (3 * y + 1) % 2:",
     "        if X != (3 * y) // 2 or (3 * y + 1) % 2:",
     "lift.source_not_three_y_plus_one_over_two"),

    # --- Theorem 7.1 and 8.1 ---
    ("D12_the_lift_is_required_strictly_positive",
     "            if ms[ell] < 0:",
     "            if ms[ell] < 1:",
     "lift.lift_negative"),
    ("D13_the_supercriticality_cross_check_compares_the_wrong_power",
     "            if (ms[ell] >= 0) != ((1 << q_ell) > 3 ** ell):",
     "            if (ms[ell] >= 0) != ((1 << q_ell) > 3 ** (ell + 1)):",
     "lift.lift_nonnegative_disagreeing_with_supercriticality"),
    ("D14_the_slack_decomposition_drops_the_phase",
     "            rhs = p2(-ms[ell]) / two_pow_eps(ell)",
     "            rhs = p2(-ms[ell])",
     "lift.slack_decomposition_violations"),
    ("D15_the_recurrence_forgets_the_mechanical_increment",
     "            if ms[ell] - ms[ell - 1] != w[h - ell] - a:",
     "            if ms[ell] - ms[ell - 1] != w[h - ell]:",
     "lift.recurrence_theorem_8_1_violations"),
    ("D16_every_descent_is_called_a_descent_of_two",
     "                if ms[ell] < ms[ell - 1] - 1:",
     "                if ms[ell] < ms[ell - 1] + 1:",
     "lift.lift_descends_by_more_than_one"),
    ("D17_a_descent_is_required_at_a_mechanical_one",
     "                if a != 2:",
     "                if a != 1:",
     "lift.lift_descends_at_a_mechanical_one"),
    ("D18_the_total_lift_is_read_one_ceiling_out",
     "        if ms[h] != Q - ceil_beta(h):",
     "        if ms[h] != Q - ceil_beta(h) + 1:",
     "lift.total_lift_not_q_minus_ceil_beta_h"),

    # --- the Laplace budget ---
    ("D19_the_reindexing_is_compared_without_reversing",
     "        if old != list(reversed(new)):",
     "        if old != new:",
     "budget.reindexing_violations"),
    ("D20_the_laplace_right_side_loses_its_factor_of_three",
     "        if s_real != 3 * (Fraction(Z) - Fraction(3 ** h, 1 << Q) * X):",
     "        if s_real != (Fraction(Z) - Fraction(3 ** h, 1 << Q) * X):",
     "budget.laplace_identity_violations"),
    ("D21_the_budget_is_demanded_a_thousandfold",
     "        if not s_int < 6 * Z:",
     "        if not s_int < Fraction(6 * Z, 1000):",
     "budget.budget_theorem_9_1_violations"),
    ("D22_the_factor_two_sandwich_is_inverted",
     "        if not s_real < s_int < 2 * s_real:",
     "        if not s_int < s_real < 2 * s_int:",
     "budget.budget_is_not_within_a_factor_two_of_the_identity"),
    ("D23_the_quantile_bound_is_divided_by_a_million",
     "            if not cnt < 6 * Z * (1 << a):",
     "            if not cnt < Fraction(6 * Z * (1 << a), 10 ** 6):",
     "budget.quantile_violations"),
    ("D24_the_sharp_quantile_bound_loses_its_exponent",
     "            if not cnt < s_int * (1 << a):",
     "            if not cnt < s_int:",
     "budget.sharp_quantile_violations"),

    # --- the mechanical cocycle ---
    ("D25_the_reverse_recursion_drops_its_plus_one",
     "            if 3 * rev[ell + 1] + 1 != (1 << q) * rev[ell]:",
     "            if 3 * rev[ell + 1] != (1 << q) * rev[ell]:",
     "cocycle.reverse_recursion_violations"),
    ("D26_the_lifted_cocycle_exponent_forgets_the_lift_increment",
     "            if rev[ell + 1] != (p2(a + ms[ell + 1] - ms[ell]) * rev[ell]",
     "            if rev[ell + 1] != (p2(a) * rev[ell]",
     "cocycle.lifted_cocycle_theorem_12_1_violations"),
    ("D27_the_normalized_cocycle_subtracts_the_wrong_power",
     "                              - p2(-ms[ell + 1])) / 3:",
     "                              - p2(-ms[ell])) / 3:",
     "cocycle.normalized_cocycle_theorem_12_2_violations"),
    ("D28_the_closed_form_uses_the_wrong_leading_phase",
     "        if U[h] != eh * Z - acc / 3:",
     "        if U[h] != eh * Z - acc:",
     "cocycle.closed_form_violations"),
    ("D29_the_cocycle_weights_are_demanded_in_a_narrower_band",
     "            if not Fraction(1, 2) < wgt < 2:",
     "            if not Fraction(999, 1000) < wgt < Fraction(1001, 1000):",
     "cocycle.weight_outside_one_half_to_two"),
    ("D30_the_reversal_starts_at_the_source_not_the_endpoint",
     "        if U[0] != Z:",
     "        if U[0] != X:",
     "cocycle.u_zero_not_the_endpoint"),
    ("D31_the_zero_lift_boundary_is_taken_at_the_wrong_end",
     "            if U[h] != X:",
     "            if U[h] != Z:",
     "cocycle.u_h_not_the_source_on_a_zero_lift_bridge"),
    ("D32_the_residue_parity_is_shifted_by_one",
     "            if (a + ms[ell + 1] - ms[ell]) % 2 != pi:",
     "            if (a + ms[ell + 1] - ms[ell] + 1) % 2 != pi:",
     "cocycle.residue_parity_theorem_13_1_violations"),
    ("D33_the_valuation_parity_is_read_from_the_wrong_state",
     "            pi = 0 if rev[ell] % 3 == 1 else 1",
     "            pi = 0 if rev[ell + 1] % 3 == 1 else 1",
     "cocycle.residue_parity_theorem_13_1_violations"),
    ("D34_the_reverse_state_is_required_to_be_one_mod_three",
     "            if rev[ell] % 3 not in (1, 2):",
     "            if rev[ell] % 3 not in (1,):",
     "cocycle.reverse_state_outside_one_or_two_mod_three"),

    # --- the zero-lift class ---
    ("D35_the_excess_decomposition_drops_the_lift_factor",
     "        if Fraction(1 << Q, 3 ** h) != p2(ms[h]) * two_pow_eps(h):",
     "        if Fraction(1 << Q, 3 ** h) != two_pow_eps(h) / 2:",
     "zero_lift.excess_decomposition_violations"),
    ("D36_the_tail_product_uses_the_wrong_numerator",
     "        for v in tail[:-1]:\n            prod *= Fraction(3 * v + 1, 3 * v)\n        # the identity",
     "        for v in tail[:-1]:\n            prod *= Fraction(3 * v + 2, 3 * v)\n        # the identity",
     "zero_lift.product_identity_violations"),
    ("D37_the_product_identity_inverts_the_endpoint_ratio",
     "        if prod != Fraction(Z, X) * two_pow_eps(h):",
     "        if prod != Fraction(X, Z) * two_pow_eps(h):",
     "zero_lift.product_identity_violations"),
    ("D38_the_product_ceiling_is_lowered_below_one",
     "        if not prod < 2:",
     "        if not prod < 1:",
     "zero_lift.product_theorem_11_1_violations"),
    ("D39_the_reciprocal_mass_ceiling_is_divided_by_a_thousand",
     "        if not recip < 4 * l2_lo:",
     "        if not recip < 4 * l2_lo / 1000:",
     "zero_lift.reciprocal_mass_corollary_11_2_violations"),

    # --- Theorem 14.1's construction ---
    ("D40_the_rise_climbs_two_at_a_time",
     "        m[ell] = m[ell - 1] + 1",
     "        m[ell] = m[ell - 1] + 2",
     "abstract.valuation_outside_one_to_three"),
    ("D41_the_descent_fires_at_the_mechanical_ones",
     "        if a[ell] == 2 and cur > 0:",
     "        if a[ell] == 1 and cur > 0:",
     "abstract.lift_not_ending_at_zero"),
    ("D42_the_total_valuation_is_compared_to_the_wrong_ceiling",
     "        if sum(q) != ceil_beta(h):",
     "        if sum(q) != ceil_beta(h) + 1:",
     "abstract.total_valuation_not_the_ceiling"),
    ("D43_the_laplace_mass_ceiling_is_lowered_to_three",
     "        if not mass < 6:",
     "        if not mass < 3:",
     "abstract.laplace_mass_at_or_above_six"),
    ("D44_the_rise_component_bound_is_halved",
     "        if not rise < 1:",
     "        if not rise < Fraction(1, 2):",
     "abstract.rise_mass_at_or_above_one"),
    ("D45_the_plateau_component_bound_is_tightened_by_a_factor_h",
     "        if not plateau < Fraction(1, h):",
     "        if not plateau < Fraction(1, h * h):",
     "abstract.plateau_mass_at_or_above_one_over_h"),
    ("D46_the_descent_component_bound_is_halved",
     "        if not descent < 4:",
     "        if not descent < 2:",
     "abstract.descent_mass_at_or_above_four"),
    ("D47_a_height_may_be_held_only_once",
     "        if any(v > 2 for v in held.values()):",
     "        if any(v > 1 for v in held.values()):",
     "abstract.a_height_held_more_than_twice_in_the_descent"),

    # --- their two synthetic blocks ---
    ("D48_the_beta_cancellation_demonstration_evaluates_one_end_twice",
     "        at_hi = ((m + eps) - (b_hi - 1)) - (2 - b_hi)",
     "        at_hi = ((m + eps) - (b_hi - 1)) - (2 - b_lo)",
     "their_algebra.drop_difference_depends_on_beta"),

    # --- the artifact and ledger layers ---
    ("D49_the_checksum_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D50_the_validation_digests_are_compared_to_a_reversed_string",
     "                if n in actual and actual[n] != r[\"sha256\"]:",
     "                if n in actual and actual[n] != r[\"sha256\"][::-1]:",
     "artifacts.validation_digest_mismatches"),
    ("D51_the_ledger_coverage_heuristic_accepts_anything",
     "        return hit >= max(1, len(words) // 2)",
     "        return hit >= 0",
     "ledger.heuristic_failed_its_negative_control"),
    ("D52_the_ledger_coverage_heuristic_accepts_nothing",
     "        hit = sum(1 for w in words if w[:7] in blob)",
     "        hit = sum(1 for w in words if w[:7] == blob)",
     "ledger.heuristic_failed_its_positive_control"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
    ("N2_a_blank_line_is_not_a_defect", b"\n"),
]


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
    aim = {name: raw.count(old) for name, old, _n, _e in DEFECTS}
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
                "note": "unreachable, premise-empty, too weak, or "
                        "mathematically identical to what it replaced -- and "
                        "from a green baseline, deleting a check whose counter "
                        "already reads zero is invisible too"}
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
    tot = report["totals"]
    report["counts"] = {
        "planted": tot["defects"],
        "caught_by_their_own_check": tot["caught"],
        "missed": tot["missed"], "malformed": tot["malformed"],
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
