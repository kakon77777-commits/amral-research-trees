"""RUN-047 mutation drill for `src66_carry_conjugacy.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" has four causes worth telling apart:
    unreachable, premise-empty, too weak, and mathematically identical to what
    it replaced (RUN-044's `2^-q` mod 3, RUN-045's modulus shrunk to a divisor);
  * from a GREEN baseline a defect must make a counter RISE. Deleting a check
    whose counter already reads zero is invisible, and so is LOOSENING one --
    RUN-045 produced four of the first kind, RUN-046 three of the second;
  * a defect that makes the gate RAISE is malformed too, and the fix belongs in
    the gate. RUN-046 made that general: every section reports through an
    `errors.<section>_raised` counter;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back.

Usage:
    python code/src66_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src66_carry_conjugacy.py"
LIMIT = "36000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the carry conjugacy, the round's whole point ---
    ("D1_the_carry_definition_uses_the_wrong_power_of_three",
     "    return [Fraction(3 ** ell * rev[ell], 1 << Qs[ell])",
     "    return [Fraction(3 ** (ell + 1) * rev[ell], 1 << Qs[ell])",
     "carry.carry_definition_violations"),
    ("D2_the_carry_denominator_is_read_one_level_early",
     "            if W[ell] != Fraction(3 ** ell * rev[ell], 1 << Qs[ell]):",
     "            if W[ell] != Fraction(3 ** ell * rev[ell], 1 << Qs[ell - 1]):",
     "carry.carry_definition_violations"),
    ("D3_the_carry_starts_at_the_source",
     "        if W[0] != Z:",
     "        if W[0] != X:",
     "carry.carry_start_not_the_endpoint"),
    ("D4_the_final_carry_forgets_its_phase",
     "        if W[h] != X / two_pow_eps(h):",
     "        if W[h] != X:",
     "carry.carry_end_not_the_phased_source"),
    ("D5_the_recurrence_decrement_uses_the_earlier_valuation_sum",
     "            if W[ell + 1] != W[ell] - Fraction(3 ** ell, 1 << Qs[ell + 1]):",
     "            if W[ell + 1] != W[ell] - Fraction(3 ** ell, 1 << Qs[ell]):",
     "carry.carry_recurrence_theorem_3_1_violations"),
    ("D6_the_recurrence_adds_where_it_must_subtract",
     "            if W[ell + 1] != W[ell] - Fraction(3 ** ell, 1 << Qs[ell + 1]):",
     "            if W[ell + 1] != W[ell] + Fraction(3 ** ell, 1 << Qs[ell + 1]):",
     "carry.carry_recurrence_theorem_3_1_violations"),
    ("D7_the_carry_is_required_to_increase",
     "            if not W[ell + 1] < W[ell]:",
     "            if not W[ell + 1] > W[ell]:",
     "carry.carry_not_strictly_decreasing"),
    ("D8_the_iterated_form_shifts_its_numerator",
     "            acc += Fraction(3 ** (ell - 1), 1 << Qs[ell])",
     "            acc += Fraction(3 ** ell, 1 << Qs[ell])",
     "carry.iterated_carry_form_violations"),
    ("D9_the_iterated_form_is_compared_to_the_wrong_side",
     "            if W[ell] != Z - acc:",
     "            if W[ell] != Z + acc:",
     "carry.iterated_carry_form_violations"),

    # --- the band and the windows ---
    ("D10_the_carry_band_floor_is_raised_to_the_endpoint",
     "            if not (Fraction(Z, 2) < W[ell] <= Z):",
     "            if not (Fraction(Z, 1) < W[ell] <= Z):",
     "carry.carry_band_theorem_4_1_violations"),
    ("D11_the_carry_band_ceiling_is_made_strict",
     "            if not (Fraction(Z, 2) < W[ell] <= Z):",
     "            if not (Fraction(Z, 2) < W[ell] < Z):",
     "carry.carry_band_theorem_4_1_violations"),
    ("D12_the_dyadic_window_is_narrowed_to_a_point",
     "            if not (p2(m - 1) * Z < v < p2(m + 1) * Z):",
     "            if not (p2(m) * Z < v < p2(m) * Z):",
     "carry.dyadic_window_corollary_4_2_violations"),
    ("D13_the_state_is_compared_to_the_unphased_carry",
     "            if Fraction(v) != p2(m) * two_pow_eps(ell) * W[ell]:",
     "            if Fraction(v) != p2(m) * W[ell]:",
     "carry.state_is_not_the_phased_carry"),
    ("D14_the_sharper_lower_end_uses_the_endpoint_not_the_source",
     "            lo = p2(m) * two_pow_eps(ell) / two_pow_eps(h) * X",
     "            lo = p2(m) * two_pow_eps(ell) / two_pow_eps(h) * X * 2",
     "carry.sharper_window_lower_violations"),
    ("D15_the_sharper_upper_end_is_halved",
     "            hi = p2(m) * two_pow_eps(ell) * Z",
     "            hi = p2(m) * two_pow_eps(ell) * Z / 2",
     "carry.sharper_window_upper_violations"),
    ("D16_the_suffix_sum_walks_the_word_forwards",
     "        run += word[h - ell]",
     "        run += word[ell - 1]",
     "carry.carry_recurrence_theorem_3_1_violations"),

    # --- mechanical neutrality ---
    ("D17_the_ceiling_table_stores_the_floor",
     "            _CEIL.append(p.bit_length())",
     "            _CEIL.append(p.bit_length() - 1)",
     "neutrality.telescoping_violations"),
    ("D18_the_mechanical_alphabet_is_required_to_be_one_or_three",
     "        if a not in (1, 2):",
     "        if a not in (1, 3):",
     "neutrality.mechanical_symbol_outside_one_or_two"),
    ("D19_two_consecutive_twos_are_called_forbidden",
     "        if j > 1 and a == 1 and tab[j - 1] - tab[j - 2] == 1:",
     "        if j > 1 and a == 2 and tab[j - 1] - tab[j - 2] == 2:",
     "neutrality.two_consecutive_mechanical_ones"),
    ("D20_the_neutrality_ratio_uses_the_wrong_interval_length",
     "        ratio = Fraction(1 << (tab[s] - tab[r]), 3 ** (s - r))",
     "        ratio = Fraction(1 << (tab[s] - tab[r]), 3 ** (s - r + 1))",
     "neutrality.band_violations"),
    ("D21_the_neutrality_band_is_narrowed_to_a_tenth",
     "        if not Fraction(1, 2) < ratio < 2:",
     "        if not Fraction(9, 10) < ratio < Fraction(11, 10):",
     "neutrality.band_violations"),
    ("D22_the_phase_form_inverts_its_ratio",
     "        if i % 100 == 0 and ratio != two_pow_eps(s) / two_pow_eps(r):",
     "        if i % 100 == 0 and ratio != two_pow_eps(r) / two_pow_eps(s):",
     "neutrality.phase_form_violations"),
    ("D23_the_mechanical_increment_skips_a_level",
     "        if i % 100 == 0:\n            t[\"telescoping_checks\"] += 1\n            if sum(mech_a(j) for j in range(r + 1, s + 1)) != tab[s] - tab[r]:",
     "        if i % 100 == 0:\n            t[\"telescoping_checks\"] += 1\n            if sum(mech_a(j) for j in range(r + 2, s + 1)) != tab[s] - tab[r]:",
     "neutrality.telescoping_violations"),

    # --- the nested endpoint tower ---
    ("D24_the_tower_sum_uses_the_wrong_power_of_three",
     "                s = (s + 3 ** (j - 1) * pow(1 << Qs[j], -1, mod)) % mod",
     "                s = (s + 3 ** j * pow(1 << Qs[j], -1, mod)) % mod",
     "tower.congruence_theorem_6_1_violations"),
    ("D25_the_tower_sum_drops_the_modular_inverse",
     "                s = (s + 3 ** (j - 1) * pow(1 << Qs[j], -1, mod)) % mod",
     "                s = (s + 3 ** (j - 1) * pow(1 << Qs[j], 1, mod)) % mod",
     "tower.congruence_theorem_6_1_violations"),
    ("D26_the_congruence_is_taken_at_the_wrong_modulus",
     "            if (Z - s) % mod:",
     "            if (Z - s) % (mod - 2):",
     "tower.congruence_theorem_6_1_violations"),
    ("D27_the_archimedean_form_shifts_its_numerator",
     "            if Z - acc_real != Fraction(3 ** ell * rev[ell], 1 << Qs[ell]):",
     "            if Z - acc_real != Fraction(3 ** ell * rev[ell], 1 << Qs[ell - 1]):",
     "tower.archimedean_carry_form_violations"),
    ("D28_the_stabilization_guard_opens_one_level_too_early",
     "            if 3 ** ell > Z:",
     "            if 3 ** (ell + 2) > Z:",
     "tower.stabilization_theorem_7_1_violations"),
    ("D29_the_stabilized_representative_is_compared_to_the_source",
     "                if r != Z:",
     "                if r != X:",
     "tower.stabilization_theorem_7_1_violations"),
    ("D30_the_shallow_representative_is_compared_without_reduction",
     "                if r % mod != Z % mod:",
     "                if r != Z:",
     "tower.representative_at_a_shallow_level_not_z_mod_three_to_the_l"),
    ("D31_the_stabilization_depth_is_computed_one_power_short",
     "    while p <= z:",
     "    while p <= z // 3:",
     "tower.k0_disagreeing_with_the_least_power"),
    ("D32_the_stabilization_depth_bracket_is_one_sided",
     "        if not (3 ** k0 > Z and 3 ** (k0 - 1) <= Z):",
     "        if not (3 ** k0 > Z and 3 ** (k0 - 1) <= Z // 9):",
     "tower.k0_disagreeing_with_the_least_power"),

    # --- valuation aliasing ---
    ("D33_the_alias_period_is_read_at_the_wrong_modulus",
     "        if pow(2, pk, modhi) != 1:",
     "        if pow(2, pk, modhi) != 2:",
     "aliasing.order_violations"),
    ("D34_the_aliasing_difference_is_tested_at_the_deeper_precision",
     "            if (b - a) % modk:",
     "            if (b - a) % modhi:",
     "aliasing.aliasing_theorem_8_1_violations"),
    ("D35_the_shifted_predecessor_uses_a_third_of_the_period",
     "            b = ((1 << (q + pk)) * v - 1) // 3",
     "            b = ((1 << (q + pk // 3)) * v - 1) // 3",
     "aliasing.aliasing_theorem_8_1_violations"),
    ("D36_the_shorter_period_test_accepts_the_full_period",
     "            c = ((1 << (q + pk // 3)) * v - 1) // 3 if (\n                (1 << (q + pk // 3)) * v - 1) % 3 == 0 else None",
     "            c = ((1 << (q + pk)) * v - 1) // 3 if (\n                (1 << (q + pk)) * v - 1) % 3 == 0 else None",
     "aliasing.aliasing_at_a_shorter_period"),
    ("D37_the_integrality_guard_accepts_a_non_multiple_of_three",
     "            if num % 3:",
     "            if num % 9:",
     "aliasing.predecessor_not_integral"),

    # --- their mesoscopic block ---
    ("D38_the_ceiling_is_replaced_by_a_floor",
     "        kcrit = math.ceil(math.log(target, 3))",
     "        kcrit = math.floor(math.log(target, 3))",
     "mesoscopic.ceiling_definition_violations"),
    ("D39_the_ceiling_definition_is_demanded_one_level_tighter",
     "        if not (3 ** kcrit >= target and (kcrit <= 0 or 3 ** (kcrit - 1) < target)):",
     "        if not (3 ** (kcrit - 1) >= target and (kcrit <= 0 or 3 ** (kcrit - 1) < target)):",
     "mesoscopic.ceiling_definition_violations"),
    ("D40_the_third_assertion_is_taken_above_the_critical_level",
     "        k = max(0, kcrit - 2)",
     "        k = kcrit + 2",
     "mesoscopic.third_assertion_not_implied_by_the_second"),

    # --- published examples ---
    ("D41_the_example_stabilization_depth_is_shifted",
     "        if k0_of(Z) != ex[\"stabilization_depth_k0\"]:",
     "        if k0_of(Z) + 1 != ex[\"stabilization_depth_k0\"]:",
     "examples.stabilization_depth_disagreeing"),
    ("D42_the_example_carry_is_rendered_upside_down",
     "        mine = \"%d/%d\" % (W[-1].numerator, W[-1].denominator)",
     "        mine = \"%d/%d\" % (W[-1].denominator, W[-1].numerator)",
     "examples.carry_final_disagreeing"),
    ("D43_the_example_word_drops_its_first_step",
     "        X, Z, w = vals[1], vals[-1], tuple(qs[1:])",
     "        X, Z, w = vals[1], vals[-1], tuple(qs[2:])",
     "examples.exponent_word_disagreeing"),

    # --- the constants layer, where this round's finding lives ---
    ("D44_the_report_constant_is_read_from_the_frontier",
     "        rpt = report.get(\"constants\", {}).get(name)",
     "        rpt = frontier.get(name)",
     "constants.disagreeing_with_both_evaluations"),
    ("D45_the_beta_bracket_is_widened_past_a_double",
     "    b_lo, b_hi = widen(*beta_tight(), 40)",
     "    b_lo, b_hi = widen(*beta_tight(), 2)",
     "constants.undecided_brackets"),

    # --- the artifact and ledger layers ---
    ("D46_the_checksum_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D47_the_validation_markdown_flag_is_read_inverted",
     "        if isinstance(rec, dict) and rec.get(\"ok\") is not True)",
     "        if isinstance(rec, dict) and rec.get(\"ok\") is True)",
     "artifacts.validation_file_ok_flags_not_true"),
    ("D48_the_validation_json_flag_is_read_inverted",
     "        if isinstance(rec, dict) and rec.get(\"parse_ok\") is not True)",
     "        if isinstance(rec, dict) and rec.get(\"parse_ok\") is True)",
     "artifacts.validation_json_parse_not_true"),
    ("D49_the_ledger_coverage_heuristic_accepts_anything",
     "        return hit >= max(1, len(words) // 2)",
     "        return hit >= 0",
     "ledger.heuristic_failed_its_negative_control"),
    ("D50_the_ledger_coverage_heuristic_accepts_nothing",
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
                        "mathematically identical -- and from green, deleting "
                        "or LOOSENING a check whose counter reads zero is "
                        "invisible too"}
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
