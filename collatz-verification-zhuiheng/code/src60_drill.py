"""RUN-041 mutation drill for `src60_source_depth_collision.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one that matches zero or many places was aimed
    at nothing and is malformed, never a catch;
  * "the mutation changes nothing" is malformed too: the branch is unreachable
    on real data, or the defect is too weak, and a defect a correct check
    tolerates measures nothing;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back, because a killed drill leaves its defect
    behind.

Usage:
    python code/src60_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src60_source_depth_collision.py"
LIMIT = "1200"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the constants family, which is exact rational arithmetic ---
    ("D1_theta_star_uses_the_wrong_diophantine_offset",
     "THETA_STAR = 1 / (RHO_STAR + 1)",
     "THETA_STAR = 1 / (RHO_STAR + 2)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D2_the_backbone_exponent_subtracts_where_it_should_add",
     "SIGMA_STAR = 1 / (1 + THETA_STAR)",
     "SIGMA_STAR = 1 / (1 - THETA_STAR)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D3_the_support_exponent_loses_theta_from_its_denominator",
     "KAPPA_13 = (RHO_STAR + 1) / (RHO_STAR + 1 + THETA_STAR)",
     "KAPPA_13 = (RHO_STAR + 1) / (RHO_STAR + 1 - THETA_STAR)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D4_the_log_exponent_is_read_from_the_wrong_reciprocal",
     "LAMBDA_13 = 1 / (RHO_STAR + 1 + THETA_STAR)",
     "LAMBDA_13 = 1 / (RHO_STAR + 1 - THETA_STAR)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D5_the_pq_pressure_constant_is_shifted_by_one",
     "CHI_STAR = (5 * SIGMA_STAR - 4) / 3",
     "CHI_STAR = (5 * SIGMA_STAR - 3) / 3",
     "exponents.disagreeing_with_both_evaluations"),
    ("D6_the_inherited_diophantine_exponent_is_mistyped",
     "RHO_STAR = Fraction(41164, 10000)",
     "RHO_STAR = Fraction(41165, 10000)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D7_a_constant_shifted_past_its_budget_that_the_chain_still_matches",
     "CHI_STAR = (5 * SIGMA_STAR - 4) / 3",
     "CHI_STAR = (5 * SIGMA_STAR - 4) / 3 + Fraction(1, 10 ** 12)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D8_the_ulp_budget_is_taken_from_the_wrong_end",
     "            budget = 4 * int(math.ceil(cancel))",
     "            budget = 4",
     "exponents.disagreeing_with_both_evaluations"),

    # --- the exponent identities ---
    ("D9_the_section_7_identity_drops_a_term",
     "        if (1 + th) * (rho + 1) - th * rho != rho + 1 + th:",
     "        if (1 + th) * (rho + 1) - th * (rho + 1) != rho + 1 + th:",
     "identities.section_7_exponent_identity_violations"),
    ("D10_the_pq_exponent_is_derived_from_the_wrong_power",
     "        if (Fraction(5, 3) * kappa - Fraction(4, 3)",
     "        if (Fraction(5, 3) * kappa - Fraction(3, 4)",
     "identities.pq_exponent_from_inversion_violations"),
    ("D11_the_kappa_solution_cancels_the_wrong_factor",
     "        if (rho + 1) / (rho + 1 + th) * (rho + 1 + th) != rho + 1:",
     "        if (rho + 1) / (rho + 1 + th) * (rho + 1 - th) != rho + 1:",
     "identities.kappa_from_the_support_inequality_violations"),

    # --- the convexity steps ---
    ("D12_jensen_is_tested_in_the_wrong_direction",
     "            if lhs < rhs:\n                t[\"jensen_violations\"] += 1",
     "            if lhs > rhs:\n                t[\"jensen_violations\"] += 1",
     "means.jensen_violations"),
    ("D13_the_jensen_right_hand_side_uses_the_wrong_power",
     "            rhs = Fraction(n ** (rho + 1), S ** rho)",
     "            rhs = Fraction(n ** (rho + 2), S ** rho)",
     "means.jensen_violations"),
    ("D14_am_hm_is_tested_in_the_wrong_direction",
     "        if sum(Fraction(1, g) for g in gaps) < Fraction(n * n, S):",
     "        if sum(Fraction(1, g) for g in gaps) > Fraction(n * n, S):",
     "means.am_hm_violations"),
    ("D15_the_rho_star_power_is_taken_positive",
     "    return 1 / b[1], 1 / a[0]",
     "    return a[0], b[1]",
     "means."),

    # --- the overlap lemma ---
    ("D16_the_overlap_lemma_is_given_intervals_that_are_too_short",
     "        ends = [s + 4 * W + rng.randrange(0, 5 * W) for s in starts]",
     "        ends = [s + rng.randrange(1, max(2, W)) for s in starts]",
     "overlap.lemma_5_1_violations"),
    ("D17_the_common_point_is_taken_at_the_wrong_end",
     "        pt = max(starts)",
     "        pt = min(starts)",
     "overlap."),

    # --- the continued-fraction bound, the one arithmetic input ---
    ("D18_the_local_cf_scale_drops_its_plus_two",
     "        A = max(nexts) + 2",
     "        A = max(nexts)",
     "cf_local.local_cf_bound_violations"),
    ("D19_the_local_cf_scale_takes_the_smallest_partial_quotient",
     "        A = max(nexts) + 2\n",
     "        A = min(nexts) + 2\n",
     "cf_local.local_cf_bound_violations"),
    ("D20_the_floor_of_q_beta_is_taken_one_too_high",
     "    f = lo.numerator // lo.denominator",
     "    f = lo.numerator // lo.denominator + 1",
     "cf_local.undecided_brackets"),
    ("D21_the_convergents_stop_far_short_of_the_scale",
     "                 if q <= N and i + 1 < len(terms)]",
     "                 if q <= N // 1000 and i + 1 < len(terms)]",
     "cf_local.local_cf_bound_violations"),

    # --- the orbit identities ---
    ("D22_the_product_identity_loses_a_factor_of_three",
     "            if Fraction(z) * 2 ** Q != Fraction(y) * 3 ** L * P:",
     "            if Fraction(z) * 2 ** Q != Fraction(y) * 3 ** (L - 1) * P:",
     "orbits.exact_product_identity_violations"),
    ("D23_the_survival_equivalence_is_reversed",
     "            survives = Fraction(2) ** Q < Fraction(3) ** L * P",
     "            survives = Fraction(2) ** Q > Fraction(3) ** L * P",
     "orbits.survival_equivalence_violations"),
    ("D24_the_block_correction_omits_its_last_state",
     "            for j in range(s, u):\n                P *= 1 + Fraction(1, 3 * v[j])",
     "            for j in range(s, u - 1):\n                P *= 1 + Fraction(1, 3 * v[j])",
     "orbits.exact_product_identity_violations"),
    ("D25_the_slack_bracket_adds_beta_instead_of_subtracting",
     "            d_lo, d_hi = Fraction(Q) - b_hi * L, Fraction(Q) - b_lo * L",
     "            d_lo, d_hi = Fraction(Q) + b_hi * L, Fraction(Q) + b_lo * L",
     "orbits."),
    ("D26_the_unconditional_slack_floor_is_demanded_far_too_large",
     "                if d_lo <= Fraction(1, A_N * L):",
     "                if d_lo <= Fraction(1, A_N):",
     "orbits.local_cf_slack_violations"),
    ("D27_the_first_crossing_test_is_inverted",
     "            if b_hi * g < p:",
     "            if b_hi * g > p:",
     "orbits."),

    # --- the localized algebra ---
    ("D28_theorem_4_1_is_stated_with_the_wrong_power_of_L",
     "            if not Fraction(A * L * L) > 3 * y * l2_lo:",
     "            if not Fraction(A * L) > 3 * y * l2_lo:",
     "localization.theorem_4_1_violations"),
    ("D29_the_duration_floor_uses_the_wrong_exponent",
     "            if not Fraction(L) ** 5 > 3 * c * y * l2_lo:",
     "            if not Fraction(L) ** 3 > 3 * c * y * l2_lo:",
     "localization.duration_floor_violations"),
    ("D30_the_corridor_implication_forgets_to_subtract_one",
     "            if not (two_h - 1) * y1 < c2:",
     "            if not two_h * y1 < c2:",
     "localization.corridor_implication_violations"),

    # --- artifacts and the guards ---
    ("D31_a_digest_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D32_the_orbit_scan_is_reduced_to_a_single_source",
     "    for start in range(7, limit, 2):\n        if start % 3 == 0:\n"
     "            continue\n        t[\"starts\"] += 1",
     "    for start in range(7, 9, 2):\n        if start % 3 == 0:\n"
     "            continue\n        t[\"starts\"] += 1",
     "orbits."),
    ("D33_a_counter_is_added_that_no_list_classifies",
     "        \"constants_checked\": 0,\n"
     "        \"disagreeing_with_both_evaluations\": 0,",
     "        \"constants_checked\": 0, \"a_counter_nothing_reads\": 0,\n"
     "        \"disagreeing_with_both_evaluations\": 0,",
     "exponents.a_counter_nothing_reads"),
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
    """Three channels, all verdicts: a named failure, an emptied population,
    and a counter no list classifies."""
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
    tot = report["totals"]
    # the shape `suite_totals.py` already knows; it refuses an unlisted one, and
    # a rename once put seven drills outside the published figure for seven
    # rounds, so emit the shape rather than teach it a new one
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
