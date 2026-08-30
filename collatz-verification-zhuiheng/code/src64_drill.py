"""RUN-045 mutation drill for `src64_small_endpoint_cylinder.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" is malformed, and it has FOUR causes worth
    telling apart: unreachable, premise-empty, too weak, and mathematically
    identical to what it replaced. RUN-044 planted `2^q` for `2^-q` mod 3 and
    got the same test back, because 2 has order two there;
  * a defect that makes the gate RAISE is malformed too, and the fix belongs in
    the gate, which must report rather than crash;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * every group of observation counters needs an invariant somewhere, or a
    defect can move all of them at once in silence;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back.

Usage:
    python code/src64_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src64_small_endpoint_cylinder.py"
LIMIT = "25000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the affine identity, which is the actual content of section 5 ---
    ("D1_the_affine_identity_loses_the_endpoint_power",
     "        if (1 << Q) * Z != 3 ** h * X + B:",
     "        if (1 << Q) * Z != 3 ** (h - 1) * X + B:",
     "bridges.affine_identity_violations"),
    ("D2_the_running_exponent_inside_b_of_advances_too_fast",
     "        out += 3 ** (h - 1 - j) * (1 << run)\n        run += q",
     "        out += 3 ** (h - 1 - j) * (1 << run)\n        run += q + 1",
     "bridges.affine_identity_violations"),
    ("D3_the_closed_form_for_b_w_shifts_its_power_of_three",
     "        out += 3 ** (h - 1 - j) * (1 << run)",
     "        out += 3 ** (h - j) * (1 << run)",
     "bridges.b_w_not_matching_the_closed_form"),
    ("D4_the_laplace_numerator_uses_the_wrong_suffix_length",
     "        lhs = sum(Fraction(3 ** (h - i), 1 << (Q - P[i])) for i in range(h))\n        rhs",
     "        lhs = sum(Fraction(3 ** (h - i - 1), 1 << (Q - P[i])) for i in range(h))\n        rhs",
     "bridges.laplace_identity_violations"),
    ("D5_the_laplace_right_side_forgets_its_factor_of_three",
     "        rhs = 3 * (Fraction(Z) - Fraction(3 ** h, 1 << Q) * X)",
     "        rhs = (Fraction(Z) - Fraction(3 ** h, 1 << Q) * X)",
     "bridges.laplace_identity_violations"),
    ("D6_the_laplace_sum_is_allowed_to_vanish",
     "        if not lhs > 0:",
     "        if not lhs > 3 * Z:",
     "bridges.laplace_sum_not_positive"),

    # --- suffix supercriticality, in integers ---
    ("D7_the_suffix_test_compares_against_the_wrong_power",
     "            if not (1 << (Q - P[i])) > 3 ** (h - i):\n                t[\"suffix_not_supercritical\"] += 1\n\n        # (4)",
     "            if not (1 << (Q - P[i])) > 3 ** (h - i + 1):\n                t[\"suffix_not_supercritical\"] += 1\n\n        # (4)",
     "bridges.suffix_not_supercritical"),
    ("D8_the_population_filter_admits_nothing_at_all",
     "        if not (1 << run) > 3 ** (h - j):",
     "        if not (1 << run) > 3 ** (h - j) * 10 ** 6:",
     "bridges.bridges"),

    # --- Lemma 8.2 and Theorem 8.3, exact ---
    ("D9_the_correction_floor_is_demanded_a_hundredfold",
     "        if not Fraction(B, 3 ** h) >= 1 - Fraction(2, 3) ** h:",
     "        if not Fraction(B, 3 ** h) >= 100 - Fraction(2, 3) ** h:",
     "bridges.correction_floor_violations"),
    ("D10_the_excess_floor_uses_the_wrong_power_of_two",
     "        slack = Fraction(1 << Q, 3 ** h) - floor",
     "        slack = Fraction(1 << (Q - 1), 3 ** h) - floor",
     "bridges.excess_floor_theorem_8_3_violations"),
    ("D11_the_excess_floor_numerator_is_five_hundred_not_five",
     "        floor = 1 + (5 - Fraction(2, 3) ** h) / Z",
     "        floor = 1 + (500 - Fraction(2, 3) ** h) / Z",
     "bridges.excess_floor_theorem_8_3_violations"),

    # --- the phases ---
    ("D12_the_source_phase_admits_the_wrong_residues",
     "        if X % 18 not in (11, 17):",
     "        if X % 18 not in (7, 13):",
     "bridges.source_outside_11_or_17_mod_18"),
    ("D13_the_endpoint_phase_admits_the_wrong_residues",
     "        if Z % 12 not in (7, 11):\n            t[\"endpoint_outside_7_or_11_mod_12\"] += 1\n        if not X > Z:",
     "        if Z % 12 not in (1, 5):\n            t[\"endpoint_outside_7_or_11_mod_12\"] += 1\n        if not X > Z:",
     "bridges.endpoint_outside_7_or_11_mod_12"),
    ("D14_the_phase_gap_floor_is_raised_past_what_is_observed",
     "        if gap < 4:",
     "        if gap < 400:",
     "bridges.phase_gap_violations"),
    ("D15_the_ordering_of_source_and_endpoint_is_reversed",
     "        if not X > Z:",
     "        if not X < Z:",
     "bridges.endpoint_not_below_the_source"),

    # --- section 9 ---
    ("D16_the_integer_lift_uses_the_floor_instead_of_the_ceiling",
     "        m_h = Q - (3 ** h).bit_length()",
     "        m_h = Q - (3 ** h).bit_length() - 3",
     "bridges.integer_lift_negative"),
    ("D17_the_one_sided_phase_is_required_above_one",
     "        if not (ceil_v - Fraction(h) * beta_hi() > 0\n                and ceil_v - 1 < Fraction(h) * beta_lo()):",
     "        if not (ceil_v - Fraction(h) * beta_hi() > 1\n                and ceil_v - 1 < Fraction(h) * beta_lo()):",
     "bridges.one_sided_phase_outside_the_unit_interval"),

    # --- the canonical representatives ---
    ("D18_the_source_representative_drops_its_inverse",
     "        r2 = ((1 << Q) - B) * pow(3 ** h, -1, m2) % m2",
     "        r2 = ((1 << Q) - B) * pow(3 ** h, 1, m2) % m2",
     "canonical.representative_does_not_satisfy_its_congruence"),
    ("D19_the_endpoint_representative_uses_the_wrong_modulus",
     "        r3 = B * pow(1 << Q, -1, m3) % m3",
     "        r3 = B * pow(1 << Q, -1, m3) % (m3 - 2)",
     "canonical.representative_does_not_satisfy_its_congruence"),
    ("D20_the_source_modulus_gains_a_factor_the_congruence_cannot_carry",
     "        m2, m3 = 1 << (Q + 1), 3 ** h",
     "        m2, m3 = 5 << (Q + 1), 3 ** h",
     "canonical.source_congruence_violations"),
    ("D21_the_collapse_is_asserted_for_the_wrong_value",
     "            if r2 != X or r3 != Z:",
     "            if r2 != Z or r3 != X:",
     "canonical.collapse_violations"),
    ("D22_the_smallness_guard_is_dropped_and_the_collapse_claimed_everywhere",
     "        a, b = X < m2, Z < m3",
     "        a, b = True, True",
     "canonical.collapse_violations"),

    # --- Jensen and the quantile bound ---
    ("D23_the_jensen_exponent_is_off_by_one",
     "        if not (1 << A) * S ** h >= Fraction(h ** h) * 3 ** M:",
     "        if not (1 << A) * S ** h >= Fraction(h ** (h + 1)) * 3 ** M:",
     "plateau.jensen_theorem_6_1_violations"),
    ("D24_the_jensen_triangular_exponent_is_wrong",
     "        M = h * (h + 1) // 2\n\n        # Corollary 5.2",
     "        M = h * (h + 3) // 2\n\n        # Corollary 5.2",
     "plateau.jensen_theorem_6_1_violations"),
    ("D25_corollary_5_2_is_demanded_a_hundredfold",
     "        if not S < 3 * Z:",
     "        if not S < Fraction(1, 1000):",
     "plateau.laplace_sum_not_below_three_z"),
    ("D26_the_elementary_bound_on_the_laplace_sum_is_tightened",
     "        if not S < h:",
     "        if not S < Fraction(h, 100):",
     "plateau.laplace_sum_not_below_h"),
    ("D27_the_quantile_count_is_taken_the_wrong_way_round",
     "            cnt = sum(1 for i in range(h)\n                      if Fraction(1 << (Q - P[i]), 3 ** (h - i)) < (1 << a))",
     "            cnt = sum(1 for i in range(h)\n                      if Fraction(1 << (Q - P[i]), 3 ** (h - i)) > (1 << a))",
     "plateau.sharp_quantile_violations"),
    ("D28_the_sharp_quantile_bound_is_divided_by_a_thousand",
     "            if not cnt < S * (1 << a):",
     "            if not cnt < S * (1 << a) / 1000:",
     "plateau.sharp_quantile_violations"),

    # --- the weighted area and the centre of mass ---
    ("D29_the_rearrangement_sums_the_wrong_prefix",
     "        if sum(Q - P[i] for i in range(h)) != A:",
     "        if sum(Q - P[i] for i in range(1, h)) != A:",
     "area.rearrangement_violations"),
    ("D30_the_triangular_sum_is_off_by_one_term",
     "        if sum(h - i for i in range(h)) != M:",
     "        if sum(h - i for i in range(h - 1)) != M:",
     "area.triangular_sum_violations"),
    ("D31_the_surplus_total_forgets_the_baseline",
     "        if sum(q - 1 for q in w) != R:",
     "        if sum(q for q in w) != R:",
     "area.surplus_total_not_q_minus_h"),
    ("D32_the_centre_of_mass_is_demanded_ten_times_the_midpoint",
     "        if 2 * (A - M) < (h + 1) * R:",
     "        if 2 * (A - M) < 10 * (h + 1) * R:",
     "area.centre_of_mass_before_the_midpoint"),

    # --- the first-hit slice ---
    ("D33_the_first_hit_threshold_is_lowered_after_the_search",
     "        if not cur ** b >= thresh:",
     "        if not cur ** b >= thresh * 1000:",
     "first_hit.first_hit_below_the_threshold"),
    ("D34_the_first_hit_search_starts_one_step_late",
     "        for v in range(1, len(word) + 1):\n            if Fraction(3 ** v, 1 << K[v]) ** b >= thresh:",
     "        for v in range(2, len(word) + 1):\n            if Fraction(3 ** v, 1 << K[v]) ** b >= thresh:",
     "first_hit.first_hit_not_minimal"),
    ("D35_the_overshoot_is_bounded_by_less_than_one_step",
     "        if not cur ** b < Fraction(3, 2) ** b * thresh:",
     "        if not cur ** b < Fraction(11, 10) ** b * thresh:",
     "first_hit.overshoot_above_one_step"),
    ("D36_the_slack_step_ratio_uses_the_previous_valuation",
     "            if a1 / a0 != Fraction(3, 1 << word[n]):",
     "            if a1 / a0 != Fraction(3, 1 << word[n - 1]):",
     "first_hit.slack_step_ratio_violations"),
    ("D37_the_prefix_valuation_is_read_off_by_one_step",
     "        P = sum(word[:ell])",
     "        P = sum(word[:ell - 1])",
     "first_hit.prefix_valuation_not_matching_the_cumulative_sum"),

    # --- the record-gap population, where the phase hypotheses apply ---
    ("D38_the_record_affine_identity_loses_its_correction",
     "        if (1 << Q) * Z != 3 ** h * X + b_of(w):",
     "        if (1 << Q) * Z != 3 ** h * X:",
     "records.affine_identity_violations"),
    ("D39_the_record_endpoint_is_required_one_mod_four",
     "        if Z % 4 != 3:",
     "        if Z % 4 != 1:",
     "records.endpoint_not_three_mod_four"),

    # --- their guards, measured independently ---
    ("D40_the_source_residue_guard_is_widened_past_the_modulus",
     "        if n < 1 << (Q + 1):",
     "        if n < 1 << (Q + 8):",
     "their_guards.residue_source_violations"),
    ("D41_the_endpoint_residue_guard_is_widened_past_the_modulus",
     "        if cur < 3 ** h:",
     "        if cur < 3 ** (h + 4):",
     "their_guards.residue_endpoint_violations"),

    # --- the entropy diagnostic ---
    ("D42_the_composition_count_uses_the_wrong_binomial",
     "        c = math.comb(Q - 1, h - 1)",
     "        c = math.comb(Q + 40, h - 1)",
     "entropy.entropy_rate_above_beta"),
    ("D42b_the_convergence_test_forgets_the_previous_gap",
     "        prev = gap",
     "        prev = gap * 0",
     "entropy.gap_not_shrinking"),
    ("D43_the_entropy_rate_forgets_to_divide_by_h",
     "        rate_lo, rate_hi = lo / h, hi / h",
     "        rate_lo, rate_hi = lo, hi",
     "entropy.entropy_rate_above_beta"),

    # --- the instrument itself ---
    ("D44_log2_int_returns_the_bit_length_and_nothing_else",
     "    x_lo, x_hi = simplify(Fraction(c, 1 << k), 30)",
     "    x_lo, x_hi = simplify(Fraction(1, 1), 30)",
     "instrument.failed"),
    ("D45_binary_entropy_adds_the_term_it_must_subtract",
     "    lo = -r * a_hi - (1 - r) * b_hi",
     "    lo = -r * a_hi + (1 - r) * b_hi",
     "instrument.failed"),

    # --- the artifact and ledger layers ---
    ("D46_the_checksum_comparison_is_made_against_itself",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D47_the_validation_digests_are_compared_to_the_wrong_file",
     "                if n in actual and actual[n] != r[\"sha256\"]:",
     "                if n in actual and actual[n] != r.get(\"sha256\", \"\")[::-1]:",
     "artifacts.validation_digest_mismatches"),
    ("D48_the_ledger_coverage_heuristic_accepts_anything",
     "        return hit >= max(1, len(words) // 2)",
     "        return hit >= 0",
     "ledger.heuristic_failed_its_negative_control"),
    ("D49_the_ledger_coverage_heuristic_accepts_nothing",
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
                        "mathematically identical to what it replaced -- read "
                        "which before re-aiming; two of the four are facts "
                        "about the subject"}
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
