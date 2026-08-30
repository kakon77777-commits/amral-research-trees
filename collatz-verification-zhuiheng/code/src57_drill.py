"""Can the item-57 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src57_valuation_harmonic_deficit.py` reports that the reciprocal-flow identity
and its telescope hold exactly on every edge and segment, that the q=1 and q=2
harmonic capacities and the total reciprocal-mass bound hold on every segment,
that the mod-9 target-cost table follows from the valuation arithmetic and every
edge respects it, that Theorem 15.1's span bound holds on every prefix meeting
first-crossing subcriticality, and that section 16's countermodel diagnostics are
internally consistent with their own closed forms.

D5 and D8 are the premise controls. Theorem 4.1 is the telescope plus `z > y`;
Lemma 5.1 needs every state INCLUDING the endpoint above the source. Neither is
met by any real segment, so both gates could be excluding everything and proving
nothing -- D5 and D8 delete them and the run must go RED. Without that the empty
denominators are worthless.

D9 replants this run's own error, twice over: applying Lemma 5.1 without its
premise flagged 352 segments of a lemma that holds, and comparing `P_RF` against
`P_6` treated two envelopes as if one dominated when the round takes their
minimum.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), robustness properties (45), a pre-flight naming
malformed mutations (46), byte-exact restore (47), a failure for every empty
locator (48), a pristine sidecar against a killed drill (50), premise before
conclusion (51), a guard on the largest case reached (52), enumerating counters
rather than matching their names (53), a named failure rather than an assert (54),
and a bracket tight enough to pin what it judges (55, 57).

Usage:  python code/src57_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src57_valuation_harmonic_deficit.py"
LIMIT = "5000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- section 3, the reciprocal flow ---
    ("D1_the_identity_drops_its_cross_term",
     "            rhs = Fraction(3 - 2 ** q, 3 * Yj) + Fraction(1, 3 * Yj * Yn)",
     "            rhs = Fraction(3 - 2 ** q, 3 * Yj)",
     "reciprocal_flow.identity_violations"),
    ("D2_the_identity_uses_the_target_where_it_needs_the_source",
     "            lhs = Fraction(1, Yj) - Fraction(1, Yn)",
     "            lhs = Fraction(1, Yn) - Fraction(1, Yj)",
     "reciprocal_flow.identity_violations"),
    ("D3_the_telescope_takes_the_wrong_endpoint_sign",
     "            if flow != -Fraction(3, y) + Fraction(3, z) + cross:",
     "            if flow != Fraction(3, y) - Fraction(3, z) + cross:",
     "reciprocal_flow.telescope_violations"),
    ("D4_the_flow_weight_subtracts_two_instead_of_three",
     "            flow = sum(Fraction(2 ** word[j] - 3, values[j])",
     "            flow = sum(Fraction(2 ** word[j] - 2, values[j])",
     "reciprocal_flow.telescope_violations"),
    # --- the two premise gates ---
    ("D5_theorem_4_1_is_applied_without_its_endpoint_premise",
     "            premise = z > y",
     "            premise = True",
     "reciprocal_flow.theorem_4_1_violations"),
    ("D6_the_balance_and_the_premise_are_required_to_differ",
     "            if balance != premise:",
     "            if balance == premise:",
     "reciprocal_flow.the_balance_is_not_equivalent_to_the_endpoint_premise"),
    ("D7_the_high_valuation_weight_is_wrong",
     "            high = sum((2 ** k - 3) * v for k, v in S.items() if k >= 2)",
     "            high = sum((2 ** k - 4) * v for k, v in S.items() if k >= 2)",
     "reciprocal_flow.the_balance_is_not_equivalent_to_the_endpoint_premise"),
    ("D8_lemma_5_1_is_applied_without_its_premise",
     "            if all(v >= y for v in span) and len(set(span)) == len(span):",
     "            if True:",
     "reciprocal_flow.cross_term_above_one_over_y_squared_plus_one_over_two_y"),
    ("D9_the_premise_span_excludes_the_endpoint",
     "            span = values[s:end + 1]",
     "            span = values[s:end]",
     "reciprocal_flow.cross_term_above_one_over_y_squared_plus_one_over_two_y"),
    # --- sections 6 and 7 ---
    ("D10_the_q1_capacity_halves_its_logarithmic_term",
     "            if S1 > Fraction(2, y) + l6 / 6:",
     "            if S1 > Fraction(2, y) + l6 / 600:",
     "capacities.q1_capacity_violations"),
    ("D11_the_q2_capacity_uses_the_q1_logarithm",
     "            if S2 > Fraction(2, y) + l12 / 12:",
     "            if S2 > Fraction(2, y) + l12 / 1200:",
     "capacities.q2_capacity_violations"),
    ("D12_the_total_reciprocal_bound_halves_its_leading_term",
     "            if Stot >= l6 / 5 + l12 / 15 + Fraction(289, 70 * y):",
     "            if Stot >= l6 / 500 + l12 / 1500 + Fraction(289, 70 * y):",
     "capacities.theorem_7_1_violations"),
    ("D13_the_289_over_70_decomposition_is_mis_stated",
     "    if (Fraction(6, 5) * 2 + Fraction(4, 5) * 2 + Fraction(1, 5) * Fraction(9, 14)\n"
     "            != Fraction(289, 70)):",
     "    if (Fraction(6, 5) * 2 + Fraction(4, 5) * 2 + Fraction(1, 5) * Fraction(9, 15)\n"
     "            != Fraction(289, 70)):",
     "capacities.the_289_over_70_constant_does_not_decompose"),
    # --- sections 8 and 9 ---
    # `(L/y)^(1/450)` is still about 1 and `C_10` is 1.47, which every real
    # product stays under -- so that mutation was never planted. Divide the
    # bound instead: nothing with a positive product can pass it.
    ("D14_the_uniform_bound_is_a_thousand_times_too_tight",
     "            if script > C10_hi * ratio_hi:",
     "            if script > C10_hi * ratio_hi / 1000:",
     "product.corollary_9_1_violations"),
    # Likewise: the low-source segments have `L/y` near one, so raising the
    # decay exponent moved the factor barely at all.
    ("D15_the_deficit_bound_is_a_thousand_times_too_tight",
     "            if script * dec_hi > Crel_hi * P6:",
     "            if script * dec_hi > Crel_hi * P6 / 1000:",
     "product.theorem_9_2_violations"),
    ("D16_the_p6_floor_uses_the_wrong_constant",
     "            floor_lo = _pow_bracket(Fraction(63 * L, 25 * y), 1, 9)",
     "            floor_lo = _pow_bracket(Fraction(630 * L, 25 * y), 1, 9)",
     "product.p6_lower_bound_violations"),
    ("D17_the_admissible_upper_placement_is_one_too_tight",
     "            if any(a[k] > y + 3 * k + 1 for k in range(L)):",
     "            if any(a[k] > y + 3 * k for k in range(L)):",
     "product.admissible_upper_placement_violations"),
    ("D18_the_rf_exponent_is_compared_against_one_ninth",
     "            if prev is not None and abs(erf - 4 / 45) > abs(prev - 4 / 45) + 1e-9:",
     "            if prev is not None and abs(erf - 1 / 45) > abs(prev - 1 / 45) + 1e-9:",
     "exponents.rf_exponent_not_approaching_four_forty_fifths"),
    # --- sections 14 and 15 ---
    ("D19_the_target_residue_set_is_wrong",
     "            if (2 ** word[j] * target) % 9 not in (4, 7):",
     "            if (2 ** word[j] * target) % 9 not in (4, 5):",
     "mod9.targets_not_4_or_7_mod_9"),
    ("D20_the_cost_table_is_transcribed_wrongly",
     "TARGET_COST = {1: 2, 2: 1, 4: 2, 5: 3, 7: 4, 8: 1}",
     "TARGET_COST = {1: 2, 2: 1, 4: 2, 5: 3, 7: 4, 8: 2}",
     "mod9.cost_table_entries_disagreeing_with_the_valuation_arithmetic"),
    ("D21_the_class_capacity_drops_its_slack",
     "                if counts[c] > Fraction(W, 9) + 2:",
     "                if counts[c] > Fraction(W, 18):",
     "mod9.windows_where_a_cost_class_exceeds_W_over_9_plus_2"),
    ("D22_the_valuation_floor_charges_the_wrong_baseline",
     "            if not Fraction(Q) >= 3 * m - Fraction(W, 3) - 6:",
     "            if not Fraction(Q) >= 10 * m - Fraction(W, 3) - 6:",
     "mod9.valuation_floor_violations"),
    ("D23_the_span_bound_loses_its_constant",
     "            if not Fraction(W) > 3 * (3 - beta_lo) * m - 18:",
     "            if not Fraction(W) > 3 * (3 - beta_lo) * m + 18:",
     "mod9.theorem_15_1_violations"),
    ("D24_the_subcriticality_premise_is_inverted",
     "            if 2 ** Q >= 3 ** m:",
     "            if 2 ** Q < 3 ** m:",
     "theorem 15.1 was applied to"),
    # --- section 16, the round's own countermodel ---
    ("D25_the_class_density_is_off_by_a_factor",
     "        if abs(Fraction(hits, X) - Fraction(1, 3 * (1 << k))) > Fraction(1, 300):",
     "        if abs(Fraction(hits, X) - Fraction(1, 6 * (1 << k))) > Fraction(1, 300):",
     "countermodel.class_densities_off"),
    ("D26_the_density_closed_form_drops_its_three",
     "        if abs(d_sum - 1 / (3 * (2 - tt))) > Fraction(1, 10 ** 30):",
     "        if abs(d_sum - 1 / (2 - tt)) > Fraction(1, 10 ** 30):",
     "countermodel.density_series_disagrees_with_its_closed_form"),
    ("D27_the_average_closed_form_takes_the_wrong_numerator",
     "        if abs(a_sum / d_sum - 2 / (2 - tt)) > Fraction(1, 10 ** 30):",
     "        if abs(a_sum / d_sum - 3 / (2 - tt)) > Fraction(1, 10 ** 30):",
     "countermodel.average_series_disagrees_with_its_closed_form"),
    ("D28_the_reported_average_is_compared_against_the_wrong_density",
     "        implied = 6 * count / X          # eliminating t between the two forms",
     "        implied = 3 * count / X          # eliminating t between the two forms",
     "countermodel.the_gap_to_the_closed_form_does_not_shrink"),
    # --- the instrument and the manifests ---
    ("D29_the_coarse_beta_bracket_is_used_instead_of_the_tight_one",
     "    beta_lo, beta_hi = beta_tight()",
     "    beta_lo, beta_hi = beta_bracket()",
     "instrument.the_beta_bracket_is_too_wide_to_pin_a_double"),
    ("D30_the_checksum_comparison_is_negated",
     "        \"CHECKSUMS_mismatches\": sorted(n for n, d in cs.items()\n"
     "                                       if actual.get(n) != d),",
     "        \"CHECKSUMS_mismatches\": sorted(n for n, d in cs.items()\n"
     "                                       if actual.get(n) == d),",
     "artifacts.CHECKSUMS_mismatches"),
    ("D31_the_validation_dict_shape_is_not_recognised",
     "    elif isinstance(files, dict):",
     "    elif False:",
     "the validation record shape is unrecognised"),
    ("D32_the_paper_ledger_anchor_no_longer_matches",
     '    prose = re.findall(r"^(\\d+)\\. ", block("## 22.1 Proved internally",',
     '    prose = re.findall(r"^(\\d+)\\) ", block("## 22.1 Proved internally",',
     "the paper's own ledger sections parsed empty"),
    ("D33_only_a_key_this_report_does_not_use_is_read",
     '    stated = list(report.get("checks", {}))',
     '    stated = list(report.get("verified_statements", {}))',
     "checker entries were read"),
    ("D34_the_roots_fall_back_to_the_loose_default",
     "        e_lo * _nth_root_lo(Fraction(7), 15, 40) * _nth_root_lo(Fraction(13), 45, 40),",
     "        e_lo * _nth_root_lo(Fraction(7), 15, 3) * _nth_root_lo(Fraction(13), 45, 3),",
     "matches no reference"),
    # --- robustness ---
    ("D35_the_validation_key_echo_is_dropped",
     '        "validation_record_top_level_keys": sorted(validation),',
     '        "validation_record_top_level_keys": [],',
     "__robustness: the manifest verdict stands without the echo__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D35_the_validation_key_echo_is_dropped": None,
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle), "--limit", LIMIT],
            capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
    except subprocess.TimeoutExpired:
        return {"passed": False, "failures": ["__the gate did not terminate__"],
                "non_vacuity_guards": [], "hung": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "failures": ["__the gate did not produce JSON__"],
                "non_vacuity_guards": [], "stderr_tail": (proc.stderr or "")[-400:]}


def _complaints(res: dict) -> list[str]:
    """A guard is a verdict too. A defect that empties a population is caught by
    the non-vacuity guard, not by a failure, and refusing to look there would
    leave every such defect scored as missed."""
    return list(res.get("failures", [])) + list(res.get("non_vacuity_guards", []))


def _same_verdict(a: dict, b: dict) -> bool:
    def strip(d):
        return {k: v for k, v in d.items() if k not in ("round", "orbit_limit")}
    return json.dumps(strip(a), sort_keys=True) == json.dumps(strip(b), sort_keys=True)


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
                     "non_vacuity_guards": base.get("non_vacuity_guards")},
        "defects": {}, "controls": {},
    }
    if not base.get("passed"):
        report["ok"] = False
        report["note"] = "the gate is not green before anything was planted"
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 2

    raw_text = snapshot.decode("utf-8")
    for name, old, new, expected in DEFECTS:
        hits = raw_text.count(old)
        if hits != 1:
            report["defects"][name] = {
                "caught": False, "anchor_matches": hits,
                "note": "anchor matches %d times; aimed at nothing" % hits}
            continue
        try:
            GATE.write_bytes(raw_text.replace(old, new).encode("utf-8"))
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(snapshot)

        if name not in FINDING_ROBUSTNESS:
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
                    "caught": False, "malformed": "the mutation changes nothing",
                    "note": "the branch is unreachable on real data, so this was "
                            "never planted; it is not the check missing it"}
                continue
            report["defects"][name] = {
                "caught": any(expected in c for c in _complaints(res)),
                "expected_named": expected,
                "reported": _complaints(res)[:4],
                "caught_by_something_else_only": bool(_complaints(res))
                and not any(expected in c for c in _complaints(res))}
            continue

        report["defects"][name] = {
            "caught": bool(res.get("passed")),
            "kind": "robustness: the gate must stay green",
            "gate_still_green": bool(res.get("passed")),
            "complaints_seen": _complaints(res)[:3]}

    for name, suffix in CONTROLS:
        try:
            GATE.write_bytes(snapshot + suffix)
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(snapshot)
        report["controls"][name] = {"undisturbed": bool(res.get("passed"))}
    report["controls"]["N2_the_gate_is_restored_byte_exactly"] = {
        "undisturbed": GATE.read_bytes() == snapshot}

    caught = sum(1 for v in report["defects"].values() if v.get("caught"))
    report["counts"] = {
        "planted": len(DEFECTS), "caught_by_their_own_check": caught,
        "missed": len(DEFECTS) - caught,
        "robustness_properties": len(FINDING_ROBUSTNESS),
        "malformed": sum(1 for v in report["defects"].values() if v.get("malformed")),
        "hung": sum(1 for v in report["defects"].values() if v.get("hung")),
        "controls": len(report["controls"]),
        "controls_undisturbed": sum(1 for c in report["controls"].values()
                                    if c["undisturbed"])}
    report["ok"] = (caught == len(DEFECTS)
                    and all(c["undisturbed"] for c in report["controls"].values()))
    if GATE.read_bytes() == snapshot:
        backup.unlink()
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
