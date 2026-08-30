"""RUN-042 mutation drill for `src61_sparse_support_exhaustion.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" is malformed too, and so is a defect that
    LOOSENS what it attacks: RUN-041's first pass produced three of those and
    the harness was right to refuse them;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * a defect that makes the gate RAISE is malformed as well. RUN-041 found one,
    and the right response was to fix the gate so it reports instead;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back.

Usage:
    python code/src61_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src61_sparse_support_exhaustion.py"
LIMIT = "8000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the constants family ---
    ("D1_theta_star_uses_the_wrong_offset",
     "THETA_STAR = 1 / (RHO_STAR + 1)",
     "THETA_STAR = 1 / (RHO_STAR + 2)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D2_the_backbone_exponent_subtracts_where_it_should_add",
     "SIGMA_STAR = 1 / (1 + THETA_STAR)",
     "SIGMA_STAR = 1 / (1 - THETA_STAR)",
     "instrument."),
    ("D3_the_inherited_diophantine_exponent_is_mistyped",
     "RHO_STAR = Fraction(41164, 10000)",
     "RHO_STAR = Fraction(41165, 10000)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D4_a_constant_shifted_past_its_budget_that_the_chain_still_matches",
     "KAPPA_13 = (RHO_STAR + 1) / (RHO_STAR + 1 + THETA_STAR)",
     "KAPPA_13 = (RHO_STAR + 1) / (RHO_STAR + 1 + THETA_STAR)"
     " + Fraction(1, 10 ** 12)",
     "exponents.disagreeing_with_both_evaluations"),
    ("D5_the_pq_escape_exponent_is_shifted",
     "    return (5 * k - 4) / 3",
     "    return (5 * k - 3) / 3",
     "instrument."),
    ("D6_the_slack_spike_exponent_uses_the_wrong_offset",
     "    return (k + 1) / 3",
     "    return (k + 2) / 3",
     "instrument."),
    ("D7_the_active_slack_exponent_flips_a_sign",
     "    return (k - (1 - THETA_STAR)) / THETA_STAR",
     "    return (k + (1 - THETA_STAR)) / THETA_STAR",
     "instrument."),

    # --- the exponent identities ---
    ("D8_the_trichotomy_identity_drops_its_minus_one",
     "        if 2 * k - 1 - chi(k) != zeta(k):\n"
     "            t[\"trichotomy_exponent_identity_violations\"] += 1",
     "        if 2 * k - chi(k) != zeta(k):\n"
     "            t[\"trichotomy_exponent_identity_violations\"] += 1",
     "identities.trichotomy_exponent_identity_violations"),
    ("D9_theorem_4_1s_step_is_read_as_theta_not_one_minus_theta",
     "        if rho / (rho + 1) != 1 - th:",
     "        if rho / (rho + 1) != th:",
     "identities.rho_over_rho_plus_one_violations"),
    ("D10_the_psi_inversion_is_taken_at_the_wrong_power",
     "        if lhs * th + (1 - th) != k:",
     "        if lhs * th + (1 + th) != k:",
     "identities.psi_from_theorem_4_1_violations"),
    ("D11_the_chi_threshold_is_moved_off_four_fifths",
     "        if (chi(k) > 0) != (k > Fraction(4, 5)):",
     "        if (chi(k) > 0) != (k > Fraction(3, 5)):",
     "identities.chi_threshold_violations"),

    # --- suffix minima on real orbits ---
    ("D12_the_suffix_minimum_scan_collects_maxima",
     "        if run is None or values[s] < run:",
     "        if run is None or values[s] > run:",
     "suffix.theorem_3_1_violations"),
    ("D13_the_terminal_index_is_counted_as_a_suffix_minimum",
     "            if s < T:\n                out.append(s)",
     "            if s <= T:\n                out.append(s)",
     "suffix.terminal_index_returned_as_a_suffix_minimum"),
    ("D14_theorem_3_1_is_tested_inside_out",
     "            if ww[s] != 1:\n                t[\"theorem_3_1_violations\"] += 1",
     "            if ww[s] == 1:\n                t[\"theorem_3_1_violations\"] += 1",
     "suffix.theorem_3_1_violations"),
    ("D15_the_residue_classes_drop_one_of_the_two",
     "                if y % 12 not in (7, 11):",
     "                if y % 12 not in (7,):",
     "suffix.corollary_3_2_violations"),
    ("D16_the_valuation_one_equivalence_uses_the_wrong_residue",
     "            if (ww[s] == 1) != (y % 4 == 3):",
     "            if (ww[s] == 1) != (y % 4 == 1):",
     "suffix.q_one_not_equivalent_to_three_mod_four"),
    ("D17_the_late_ordinal_floor_is_taken_one_too_high",
     "            if y < 6 * j - 1:\n"
     "                t[\"late_ordinal_floor_violations\"] += 1",
     "            if y < 6 * j + 1:\n"
     "                t[\"late_ordinal_floor_violations\"] += 1",
     "suffix.late_ordinal_floor_violations"),
    ("D18_the_successor_test_is_reversed",
     "            if not vv[s + 1] > y:",
     "            if not vv[s + 1] < y:",
     "suffix.successor_not_greater"),

    # --- the A envelope ---
    ("D19_the_envelope_adds_the_valuation_instead_of_subtracting",
     "        e_lo, e_hi = b_lo * T - Q, b_hi * T - Q",
     "        e_lo, e_hi = b_lo * T + Q, b_hi * T + Q",
     "envelope.E_A_disagreeing_with_beta_T_minus_Q"),
    ("D20_the_envelope_product_identity_loses_a_factor_of_three",
     "        if Fraction(vv[cl]) * 2 ** Q != Fraction(vv[c1]) * 3 ** T * P:",
     "        if Fraction(vv[cl]) * 2 ** Q != Fraction(vv[c1]) * 3 ** (T - 1) * P:",
     "envelope.envelope_product_identity_violations"),
    ("D21_the_envelope_correction_omits_its_last_state",
     "        for j in range(c1, cl):\n"
     "            P *= 1 + Fraction(1, 3 * vv[j])",
     "        for j in range(c1, cl - 1):\n"
     "            P *= 1 + Fraction(1, 3 * vv[j])",
     "envelope.envelope_product_identity_violations"),
    ("D22_the_A_renewal_slack_is_required_to_fall",
     "            if not b_lo * g - p > 0:",
     "            if not b_lo * g - p < 0:",
     "envelope.delta_at_A_renewals_not_increasing"),
    ("D23_the_transfer_inequality_is_demanded_far_too_strongly",
     "        if not Fraction(6 * len(cs) - 1) <= Fraction(vv[cl]):",
     "        if not Fraction(6 * len(cs) - 1) <= Fraction(vv[cl]) / 10 ** 6:",
     "envelope.transfer_inequality_violations"),
    ("D24_the_A_renewal_test_is_inverted",
     "                if b_hi * g < p:\n                    cross = u\n"
     "                    break\n            if cross is None and s > 0:",
     "                if b_hi * g > p:\n                    cross = u\n"
     "                    break\n            if cross is None and s > 0:",
     "envelope."),

    # --- the conditional algebra ---
    ("D25_theorem_4_1_is_stated_with_the_wrong_power",
     "        if not delta > c * Fraction((r - 1) ** (rho + 1), N ** rho):",
     "        if not delta > c * Fraction((r - 1) ** (rho + 2), N ** rho):",
     "backlog.theorem_4_1_violations"),
    ("D26_theorem_4_2_loses_its_factor_of_N",
     "        if not Fraction((r - 1) ** 2) < Fraction(Qn * N) * d2:",
     "        if not Fraction((r - 1) ** 2) < Fraction(Qn) * d2:",
     "backlog.theorem_4_2_violations"),

    # --- the abstract counterexample ---
    ("D27_the_record_times_grow_only_geometrically",
     "    ts = [2 ** (j * j) for j in range(1, levels + 1)]",
     "    ts = [2 ** j for j in range(1, levels + 1)]",
     "counterexample.count_disagreeing_with_sqrt_log2_N"),
    ("D28_the_intermediate_values_are_set_below_the_next_record",
     "            x[n] = j + 2",
     "            x[n] = j - 1",
     "counterexample."),

    # --- criticality ---
    ("D29_the_reciprocal_relation_is_taken_at_the_wrong_end",
     "        if max(1 / d for d in ds) != 1 / min(ds):",
     "        if max(1 / d for d in ds) != 1 / max(ds):",
     "criticality.reciprocal_relation_violations"),

    # --- artifacts and the guards ---
    ("D30_a_checksum_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D31_the_validation_digest_comparison_is_inverted",
     "            elif actual[n] != r[\"sha256\"]:",
     "            elif actual[n] == r[\"sha256\"]:",
     "artifacts.validation_digest_mismatches"),
    ("D32_the_orbit_scan_is_reduced_to_a_single_source",
     "    for start in range(7, limit, 2):\n        if start % 3 == 0:\n"
     "            continue\n        word, values = accelerated(start, 400)\n"
     "        if len(word) < window + 2:\n            continue\n"
     "        t[\"orbits\"] += 1",
     "    for start in range(7, 9, 2):\n        if start % 3 == 0:\n"
     "            continue\n        word, values = accelerated(start, 400)\n"
     "        if len(word) < window + 2:\n            continue\n"
     "        t[\"orbits\"] += 1",
     "suffix."),
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
                        "defect is too weak -- or it LOOSENED what it attacked, "
                        "which is the same thing said differently"}
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
