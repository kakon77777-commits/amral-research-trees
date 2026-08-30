"""RUN-044 mutation drill for `src63_record_gap_transport.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" is malformed, and a defect that LOOSENS what
    it attacks is the same verdict said differently. RUN-041 produced three,
    RUN-042 two, RUN-043 five; every one was correctly refused;
  * a defect that makes the gate RAISE is malformed too, and the fix belongs in
    the gate, which must report rather than crash;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * every group of observation counters needs an invariant somewhere, or a
    defect can move all of them at once in silence (RUN-043 missed exactly
    that);
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back. RUN-043's first attempt was killed by a
    timeout mid-plant and the sidecar is what recovered it.

Usage:
    python code/src63_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src63_record_gap_transport.py"
LIMIT = "6000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the correction bank, pure integer arithmetic ---
    ("D1_the_bank_identity_loses_its_factor_of_three",
     "            lhs = 2 ** K[n + 1] * values[n + 1] - 3 * 2 ** K[n] * values[n]",
     "            lhs = 2 ** K[n + 1] * values[n + 1] - 2 ** K[n] * values[n]",
     "bank.bank_identity_violations"),
    ("D2_the_bank_increment_is_expected_one_power_too_high",
     "            if lhs != 2 ** K[n]:",
     "            if lhs != 2 ** (K[n] + 1):",
     "bank.bank_identity_violations"),
    ("D3_the_bank_is_required_to_fall",
     "            if not a_next > a_n:",
     "            if not a_next < a_n:",
     "bank.bank_not_strictly_increasing"),
    ("D4_the_bank_increment_denominator_is_off_by_one_power",
     "            if a_next - a_n != Fraction(2 ** K[n], 3 ** (n + 1)):",
     "            if a_next - a_n != Fraction(2 ** K[n], 3 ** n):",
     "bank.bank_increment_not_the_claimed_value"),
    ("D5_the_bank_coordinate_uses_the_wrong_power_of_three",
     "            a_n = Fraction(2 ** K[n] * values[n], 3 ** n)",
     "            a_n = Fraction(2 ** K[n] * values[n], 3 ** (n + 1))",
     "bank."),

    # --- the gap geometry ---
    ("D6_lemma_4_1_is_tested_inside_out",
     "            if not all(vv[n] > z for n in range(s + 1, u_t)):",
     "            if not all(vv[n] < z for n in range(s + 1, u_t)):",
     "gaps.lemma_4_1_violations"),
    ("D7_the_ratio_cap_upper_end_is_tightened",
     "            if not (1 < Fraction(z, y) < Fraction(3 * y + 1, 2 * y)):",
     "            if not (1 < Fraction(z, y) < Fraction(3 * y + 1, 3 * y)):",
     "gaps.theorem_4_2_ratio_cap_violations"),
    ("D8_the_ratio_cap_lower_end_is_raised",
     "            if not (1 < Fraction(z, y) < Fraction(3 * y + 1, 2 * y)):\n",
     "            if not (2 < Fraction(z, y) < Fraction(3 * y + 1, 2 * y)):\n",
     "gaps.theorem_4_2_ratio_cap_violations"),
    ("D9_the_first_step_valuation_test_is_inverted",
     "            if ww[s] != 1:\n                t[\"first_step_valuation_not_one\"] += 1",
     "            if ww[s] == 1:\n                t[\"first_step_valuation_not_one\"] += 1",
     "gaps.first_step_valuation_not_one"),
    ("D10_the_post_record_state_is_taken_one_too_high",
     "            if x != (3 * y + 1) // 2 or (3 * y + 1) % 2 != 0:",
     "            if x != (3 * y + 1) // 2 + 1 or (3 * y + 1) % 2 != 0:",
     "gaps.x_not_three_y_plus_one_over_two"),
    ("D11_record_values_are_required_to_fall",
     "            if not y < z:",
     "            if not y > z:",
     "gaps.record_values_not_increasing"),
    ("D12_interior_slack_domination_is_reversed",
     "                if not b_hi * gg - p < 0:",
     "                if not b_hi * gg - p > 0:",
     "gaps.theorem_5_1_violations"),
    ("D13_the_suffix_supercritical_test_is_reversed",
     "                if not Fraction(p) > b_hi * gg:",
     "                if not Fraction(p) < b_lo * gg:",
     "gaps.corollary_5_2_violations"),
    ("D14_the_tail_identity_loses_a_factor_of_three",
     "            if Fraction(z) * 2 ** Q != Fraction(x) * 3 ** h * P:",
     "            if Fraction(z) * 2 ** Q != Fraction(x) * 3 ** (h - 1) * P:",
     "gaps.theorem_6_1_identity_violations"),
    ("D15_the_tail_product_omits_its_last_state",
     "            for n in range(s + 1, u_t):\n"
     "                P *= 1 + Fraction(1, 3 * vv[n])",
     "            for n in range(s + 1, u_t - 1):\n"
     "                P *= 1 + Fraction(1, 3 * vv[n])",
     "gaps.theorem_6_1_identity_violations"),
    ("D16_the_tail_excess_is_required_negative",
     "            if not Fraction(Q) - b_hi * h > 0:",
     "            if not Fraction(Q) - b_hi * h < 0:",
     "gaps.tail_excess_not_positive"),
    ("D17_the_net_record_slack_bound_is_reversed",
     "            if not b_hi * gs - ps < b_lo - 1:",
     "            if not b_hi * gs - ps > b_lo - 1:",
     "gaps.net_record_slack_not_below_beta_minus_one"),
    ("D18_the_value_peak_span_is_demanded_a_hundredfold",
     "            if not M >= z + 3 * g - 4:",
     "            if not M >= 100 * z + 3 * g:",
     "gaps.value_peak_span_violations"),

    # --- bidirectional transport ---
    ("D19_the_ascent_bound_is_raised_by_one",
     "            rhs_lo = (2 - b_hi) * l_up + h_lo",
     "            rhs_lo = (2 - b_hi) * l_up + h_lo + 1",
     "transport.ascent_theorem_8_1_violations"),
    ("D20_the_ascent_counts_the_wrong_valuation",
     "            n1 = sum(1 for j in range(s, u) if ww[j] == 1)",
     "            n1 = sum(1 for j in range(s, u) if ww[j] == 2)",
     "transport.ascent_theorem_8_1_violations"),
    ("D21_the_descent_valuation_sum_is_taken_at_the_wrong_length",
     "            if sum(ww[u:u_t]) - l_dn != q_sum - l_dn:",
     "            if sum(ww[u:u_t]) - l_dn != q_sum - l_dn - 1:",
     "transport.descent_valuation_sum_identity_violations"),
    ("D22_the_descent_count_bound_drops_its_divisor",
     "                need = ((b_lo - 1) * l_dn + hd_lo) / (q_star - 1)",
     "                need = ((b_lo - 1) * l_dn + hd_lo) * (q_star - 1)",
     "transport.descent_count_bound_violations"),
    ("D23_the_peak_is_taken_at_the_minimum",
     "            u = max(interior, key=lambda n: vv[n])",
     "            u = min(interior, key=lambda n: vv[n])",
     "transport.peak_is_not_the_interior_maximum"),

    # --- the landing phases ---
    ("D24_the_endpoint_residue_classes_drop_one",
     "            if z % 12 not in (7, 11):",
     "            if z % 12 not in (7,):",
     "phases.endpoint_outside_7_or_11_mod_12"),
    ("D25_the_phase_seven_valuation_is_required_odd",
     "                if not (q_t % 2 == 0 and q_t >= 2):",
     "                if not (q_t % 2 == 1 and q_t >= 2):",
     "phases.phase7_valuation_not_even_at_least_two"),
    ("D26_the_phase_eleven_valuation_floor_is_raised",
     "                if not (q_t % 2 == 1 and q_t >= 3):",
     "                if not (q_t % 2 == 1 and q_t >= 5):",
     "phases.phase11_valuation_not_odd_at_least_three"),
    ("D27_the_endpoint_mod_three_lemma_shifts_its_parity",
     "            if z % 3 != pow(2, -q_t, 3):",
     "            if z % 3 != pow(2, -q_t - 1, 3):",
     "phases.endpoint_mod_three_disagreeing_with_two_to_the_minus_q"),
    ("D28_the_source_phase_mod_eighteen_is_swapped",
     "            if s > 0 and y % 12 == 7 and x % 18 != 11:",
     "            if s > 0 and y % 12 == 7 and x % 18 != 17:",
     "phases.source_phase_not_matching_11_or_17_mod_18"),
    ("D29_the_landing_toll_floor_is_taken_from_the_wrong_phase",
     "                floor_lo = 2 - b_hi",
     "                floor_lo = 4 - b_hi",
     "phases.landing_toll_below_its_floor"),

    # --- the shipped examples ---
    ("D30_a_shipped_example_endpoint_is_mistyped",
     "    cases = [(71, 107, 91, (1, 2, 2)), (223, 335, 319, (1, 1, 1, 3, 2))]",
     "    cases = [(71, 107, 92, (1, 2, 2)), (223, 335, 319, (1, 1, 1, 3, 2))]",
     "examples.z_disagreeing"),
    ("D31_a_shipped_example_word_is_mistyped",
     "    cases = [(71, 107, 91, (1, 2, 2)), (223, 335, 319, (1, 1, 1, 3, 2))]\n",
     "    cases = [(71, 107, 91, (1, 2, 3)), (223, 335, 319, (1, 1, 1, 3, 2))]\n",
     "examples.exponent_word_disagreeing"),

    # --- the pigeonhole ---
    ("D32_the_pigeonhole_is_tested_in_the_wrong_direction",
     "        if max(parts) < Fraction(N, R):",
     "        if max(parts) > Fraction(N, R):",
     "exponents.pigeonhole_violations"),

    # --- artifacts and guards ---
    ("D33_a_checksum_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D34_the_ledger_heuristic_accuses_everything",
     "        return hit >= max(1, len(words) // 2)",
     "        return hit >= len(words) * 100",
     "ledger.heuristic_failed_its_positive_control"),
    ("D35_the_ledger_heuristic_covers_everything",
     "        return hit >= max(1, len(words) // 2)\n",
     "        return True\n",
     "ledger.heuristic_failed_its_negative_control"),
    ("D36_the_gap_scan_is_reduced_to_a_single_source",
     "    for start in range(7, limit, 2):\n        if start % 3 == 0:\n"
     "            continue\n        word, values = accelerated(start, 400)\n"
     "        if len(word) < window + 2:\n            continue\n"
     "        t[\"orbits\"] += 1\n"
     "        vv, ww = values[:window + 1], word[:window]\n"
     "        K = cumulative(ww)\n        cs = suffix_minima(vv, window)\n"
     "        for i in range(len(cs) - 1):\n            s, u_t = cs[i], cs[i + 1]\n"
     "            g = u_t - s",
     "    for start in range(7, 9, 2):\n        if start % 3 == 0:\n"
     "            continue\n        word, values = accelerated(start, 400)\n"
     "        if len(word) < window + 2:\n            continue\n"
     "        t[\"orbits\"] += 1\n"
     "        vv, ww = values[:window + 1], word[:window]\n"
     "        K = cumulative(ww)\n        cs = suffix_minima(vv, window)\n"
     "        for i in range(len(cs) - 1):\n            s, u_t = cs[i], cs[i + 1]\n"
     "            g = u_t - s",
     "gaps."),
    ("D37_a_counter_is_added_that_no_list_classifies",
     "    t: dict = {\"orbits\": 0, \"steps\": 0,",
     "    t: dict = {\"orbits\": 0, \"steps\": 0, \"a_counter_nothing_reads\": 0,",
     "bank.a_counter_nothing_reads"),
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
                "note": "unreachable on real data, too weak, or it LOOSENED "
                        "what it attacked -- all the same verdict"}
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
