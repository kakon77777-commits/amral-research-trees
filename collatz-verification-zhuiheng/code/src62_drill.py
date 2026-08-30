"""RUN-043 mutation drill for `src62_record_sparsity.py`.

Plant one defect at a time, run the gate, restore the file byte for byte, and
record whether the gate complained about the RIGHT thing.

The discipline, each clause bought by a run that got it wrong:

  * anchors are pre-flighted -- one matching zero or many places was aimed at
    nothing and is malformed, never a catch;
  * "the mutation changes nothing" is malformed too, and a defect that LOOSENS
    what it attacks is the same thing said differently. RUN-041 produced three
    of those and RUN-042 two; every one was correctly refused;
  * a defect that makes the gate RAISE is malformed as well, and the right
    response is to fix the gate so it reports instead. RUN-041 and RUN-042 each
    found one;
  * a guard is a verdict -- an emptied population and an unclassified counter
    both count, and both are read here;
  * the pristine sidecar is written before anything is planted and removed only
    when the file is provably back.

Usage:
    python code/src62_drill.py --bundle <dir>
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src62_record_sparsity.py"
LIMIT = "4000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the constants ---
    ("D1_the_valuation_one_floor_is_read_as_beta_minus_two",
     "        (\"q1_density_floor_2_minus_beta\", 2 - b_hi, 2 - b_lo,\n"
     "         2.0 - p_beta),",
     "        (\"q1_density_floor_2_minus_beta\", b_hi - 2, b_lo - 2,\n"
     "         p_beta - 2.0),",
     "constants."),
    ("D2_the_inherited_diophantine_exponent_is_mistyped",
     "RHO_STAR = Fraction(41164, 10000)",
     "RHO_STAR = Fraction(41165, 10000)",
     "constants.disagreeing_with_both_evaluations"),
    ("D3_the_controlled_support_exponent_is_moved",
     "        (\"inherited_controlled_renewal_support_exponent\",\n"
     "         Fraction(4, 5), Fraction(4, 5), 0.8),",
     "        (\"inherited_controlled_renewal_support_exponent\",\n"
     "         Fraction(3, 5), Fraction(3, 5), 0.6),",
     "constants.disagreeing_with_both_evaluations"),
    ("D4_a_constant_shifted_past_its_cap_whose_chain_still_matches",
     "        (\"theta_star\", THETA_STAR, THETA_STAR,",
     "        (\"theta_star\", THETA_STAR + Fraction(1, 10 ** 12),\n"
     "         THETA_STAR + Fraction(1, 10 ** 12),",
     "constants.disagreeing_with_both_evaluations"),

    # --- section 10, the premise-free inequality ---
    ("D5_the_q1_floor_uses_the_wrong_multiplier",
     "                    if Fraction(n1) < (2 - b_hi) * g + d_lo:\n"
     "                        t[\"exact_inequality_violations\"] += 1",
     "                    if Fraction(n1) < (3 - b_hi) * g + d_lo:\n"
     "                        t[\"exact_inequality_violations\"] += 1",
     "q1.exact_inequality_violations"),
    ("D6_the_q1_bound_is_raised_by_one",
     "                    if Fraction(n1) < (2 - b_hi) * g + d_lo:\n"
     "                        t[\"exact_inequality_violations\"] += 1",
     "                    if Fraction(n1) < (2 - b_hi) * g + d_lo + 1:\n"
     "                        t[\"exact_inequality_violations\"] += 1",
     "q1.exact_inequality_violations"),
    ("D7_the_off_record_control_drops_its_slack_term",
     "                if Fraction(n1) < (2 - b_hi) * g + d_lo:\n"
     "                    t[\"exact_inequality_violations_off_a_record\"] += 1",
     "                if Fraction(n1) < (2 - b_hi) * g + 10 * d_lo + 1:\n"
     "                    t[\"exact_inequality_violations_off_a_record\"] += 1",
     "q1.exact_inequality_violations_off_a_record"),
    ("D8_the_valuation_sum_identity_is_stated_with_a_flipped_delta",
     "                if not (b_lo * g - d_hi <= kk <= b_hi * g - d_lo):",
     "                if not (b_lo * g + d_lo <= kk <= b_hi * g + d_hi):",
     "q1.valuation_sum_identity_violations"),
    ("D9_the_valuation_one_count_counts_the_wrong_valuation",
     "                n1 = sum(1 for j in range(s, u) if ww[j] == 1)\n"
     "                d_lo = (b_lo * u - K[u]) - (b_hi * s - K[s])\n"
     "                d_hi = (b_hi * u - K[u]) - (b_lo * s - K[s])",
     "                n1 = sum(1 for j in range(s, u) if ww[j] == 2)\n"
     "                d_lo = (b_lo * u - K[u]) - (b_hi * s - K[s])\n"
     "                d_hi = (b_hi * u - K[u]) - (b_lo * s - K[s])",
     "q1.exact_inequality_violations"),

    # --- the record process ---
    ("D10_the_suffix_minimum_scan_collects_maxima",
     "        if run is None or values[s] < run:",
     "        if run is None or values[s] > run:",
     "records."),
    ("D11_the_exact_multiplier_loses_a_factor_of_three",
     "            if Fraction(vv[b]) * 2 ** p != Fraction(vv[a]) * 3 ** g * P:",
     "            if Fraction(vv[b]) * 2 ** p != Fraction(vv[a]) * 3 ** (g - 1) * P:",
     "records.exact_multiplier_violations"),
    ("D12_the_record_gap_product_omits_its_last_state",
     "            P = Fraction(1)\n            for j in range(a, b):\n"
     "                P *= 1 + Fraction(1, 3 * vv[j])",
     "            P = Fraction(1)\n            for j in range(a, b - 1):\n"
     "                P *= 1 + Fraction(1, 3 * vv[j])",
     "records.exact_multiplier_violations"),
    ("D13_the_concatenated_product_spans_the_wrong_range",
     "        for j in range(cs[0], cs[-1]):\n"
     "            whole *= 1 + Fraction(1, 3 * vv[j])",
     "        for j in range(cs[0], cs[-1] - 1):\n"
     "            whole *= 1 + Fraction(1, 3 * vv[j])",
     "records.product_concatenation_violations"),
    ("D14_lemma_11_1_is_stated_with_the_wrong_offset",
     "            if not max(vv[a:b]) - vv[a] >= 3 * g - 7:",
     "            if not max(vv[a:b]) - vv[a] >= 3 * g + 7:",
     "records.lemma_11_1_violations"),
    ("D15_the_U6_capacity_drops_its_slack_term",
     "            if not g <= Fraction(ceiling - vv[a] + 1, 3) + 2:",
     "            if not g <= Fraction(ceiling - vv[a] + 1, 3):",
     "records.gap_duration_above_the_U6_capacity"),
    ("D16_the_record_slack_direction_is_inverted",
     "            if d_lo > 0:\n"
     "                t[\"record_slack_ascending\"] += 1\n"
     "            elif d_hi < 0:",
     "            if d_lo < 0:\n"
     "                t[\"record_slack_ascending\"] += 1\n"
     "            elif d_hi > 0:",
     "records.total_downward_variation_negative"),
    ("D17_record_values_are_required_to_fall",
     "            if not vv[a] < vv[b]:",
     "            if not vv[a] > vv[b]:",
     "records.record_values_not_increasing"),
    ("D18_the_state_ceiling_identity_loses_its_power_of_two",
     "            if Fraction(vv[nn]) * 2 ** pp != Fraction(vv[c1]) * 3 ** gg * Pn:",
     "            if Fraction(vv[nn]) * 2 ** (pp - 1) != Fraction(vv[c1]) * 3 ** gg * Pn:",
     "records.state_ceiling_identity_violations"),
    ("D19_the_tail_identity_loses_a_factor_of_three",
     "            if Fraction(vv[n]) * 2 ** pp != Fraction(vv[cr]) * 3 ** gg * Pt:",
     "            if Fraction(vv[n]) * 2 ** pp != Fraction(vv[cr]) * 3 ** (gg - 1) * Pt:",
     "records.exact_multiplier_violations"),

    # --- the U_6 counting bound in the instrument ---
    ("D20_the_U6_counting_bound_is_asserted_too_tightly",
     "            if n > Fraction(W + 1, 3) + 2:",
     "            if n > Fraction(W + 1, 3):",
     "instrument."),
    ("D21_the_U6_count_admits_every_residue",
     "            n = sum(1 for x in range(lo_i, lo_i + W + 1) if x % 6 in (1, 5))",
     "            n = sum(1 for x in range(lo_i, lo_i + W + 1) if x % 6 in (0, 1, 2, 3, 4, 5))",
     "instrument."),

    # --- the enclosure algebra ---
    ("D22_the_enclosure_drops_one_of_its_error_terms",
     "            if not D + d >= (1 - eps - eta) * L:",
     "            if not D + d >= (1 + eps + eta) * L:",
     "enclosure.enclosure_violations"),
    ("D23_corollary_8_2_is_stated_without_its_slack",
     "            if not D >= (1 - eps - 2 * eta) * L:",
     "            if not D >= (1 + eps) * L:",
     "enclosure.corollary_8_2_violations"),
    ("D24_the_support_inversion_forgets_to_subtract_eta",
     "            if not d >= (kappa - eta) * L:",
     "            if not d >= (kappa + eta) * L:",
     "enclosure.support_transfer_inversion_violations"),

    # --- artifacts ---
    ("D25_a_checksum_comparison_is_inverted",
     "        elif actual[n] != d:",
     "        elif actual[n] == d:",
     "artifacts.digest_mismatches"),
    ("D26_the_ledger_coverage_heuristic_covers_everything",
     "        return hit >= max(1, len(words) // 2)",
     "        return True",
     "ledger.heuristic_failed_its_negative_control"),

    # --- the guards ---
    ("D27_the_q1_scan_is_reduced_to_a_single_source",
     "    for start in range(7, limit, 2):\n        if start % 3 == 0:\n"
     "            continue\n        word, values = accelerated(start, 400)\n"
     "        if len(word) < window + 2:\n            continue\n"
     "        t[\"orbits\"] += 1\n        vv, ww = values[:window + 1], word[:window]\n"
     "        K = cumulative(ww)\n        if any(q < 1 for q in ww):",
     "    for start in range(7, 9, 2):\n        if start % 3 == 0:\n"
     "            continue\n        word, values = accelerated(start, 400)\n"
     "        if len(word) < window + 2:\n            continue\n"
     "        t[\"orbits\"] += 1\n        vv, ww = values[:window + 1], word[:window]\n"
     "        K = cumulative(ww)\n        if any(q < 1 for q in ww):",
     "q1."),
    ("D28_the_enclosure_grid_never_satisfies_its_antecedent",
     "        if lo <= hi:\n            t[\"antecedent_holds\"] += 1",
     "        if lo <= hi - 10 ** 9:\n            t[\"antecedent_holds\"] += 1",
     "enclosure.antecedent_holds"),
    ("D29_a_counter_is_added_that_no_list_classifies",
     "    t: dict = {\"constants_checked\": 0,\n"
     "               \"disagreeing_with_both_evaluations\": 0,",
     "    t: dict = {\"constants_checked\": 0, \"a_counter_nothing_reads\": 0,\n"
     "               \"disagreeing_with_both_evaluations\": 0,",
     "constants.a_counter_nothing_reads"),
    ("D30_the_ledger_coverage_heuristic_accuses_everything",
     "        return hit >= max(1, len(words) // 2)",
     "        return hit >= len(words) * 100",
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
