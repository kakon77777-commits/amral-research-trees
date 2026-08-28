"""Can the item-53 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src53_plateau_reset.py` reports that section 3's crossing-slope jump law holds
exactly on real orbits, that section 4.4, Lemma 5.1 and section 11 hold with it,
that the survival-conditioned caps of sections 4.3 to 9 are met by essentially no
real chain and so were measured rather than imposed, and that the bundle's new
theorem ledger under-reports its own paper.

Two defects here matter more than the rest.

D1 replants THIS run's own error. Building the chain from the records of `delta`
instead of from the stalk at a common point looks equivalent and is not: records
only force `delta` to increase, so two record intervals can be disjoint and
`h_i = e_i - e_{i+1}` goes negative. That produced 33052 edges with a determinant
below one, out of 86539, and would have been published as a violation of a boxed
claim that holds everywhere.

D26 is a positive control on the premise gating itself. RUN-032 imposed a cap on
10214 chains that never met its corridor hypothesis and flagged all 10214. This
gate applies the caps only where the premise holds -- and D26 removes that guard,
which must turn the gate RED. A premise filter that excluded everything and
proved nothing would stay green under D26; this one does not.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), robustness properties (45), a pre-flight naming
malformed mutations (46), byte-exact restore (47), a failure for every empty
locator (48), a pristine sidecar against a killed drill (50), premise before
conclusion (51), and a guard on the largest case reached (52).

Usage:  python code/src53_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src53_plateau_reset.py"
LIMIT = "2200"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the chain itself: this run's own error, replanted ---
    ("D1_the_chain_is_built_from_delta_records_instead_of_the_stalk",
     "        ch = tuple(s for s in st if e[s] is not None)",
     "        ch = tuple(s for s in range(st[0], st[-1] + 1) if e[s] is not None)",
     "slope_quantization.endpoints_not_nested_h_negative"),
    # --- section 3, the jump law ---
    ("D2_the_jump_numerator_pairs_each_length_with_its_own_exponent",
     "                J = Qb * La - Qa * Lb\n"
     "                if Fraction(Qb, Lb) - Fraction(Qa, La)",
     "                J = Qa * La - Qb * Lb\n"
     "                if Fraction(Qb, Lb) - Fraction(Qa, La)",
     "slope_quantization.jump_law_violations"),
    ("D3_the_quantization_test_admits_equality",
     "                    if abs(Fraction(J, La * Lb)) < Fraction(1, La * Lb):",
     "                    if abs(Fraction(J, La * Lb)) <= Fraction(1, La * Lb):",
     "slope_quantization.quantization_violations"),
    ("D4_the_plateau_determinant_adds_where_it_subtracts",
     "                    Pi = Qb * g - p * Lb",
     "                    Pi = Qb * g + p * Lb",
     "slope_quantization.plateau_J_not_equal_to_Pi"),
    ("D5_the_plateau_determinant_second_form_uses_the_parent_length",
     "                    two = (g * Dj[0] + Lb * A[0], g * Dj[1] + Lb * A[1])",
     "                    two = (g * Dj[0] + La * A[0], g * Dj[1] + La * A[1])",
     "slope_quantization.plateau_Pi_two_forms_disagree"),
    ("D6_the_strict_determinant_is_off_by_one",
     "                    Delta = r * g - p * h",
     "                    Delta = r * g - p * h - 1",
     "slope_quantization.strict_determinant_below_one"),
    ("D7_the_strict_jump_formula_subtracts_the_endpoint_drop",
     "                    form = ((g + h) * Dj[0] - Lb * (E[0] - A[0]),",
     "                    form = ((g - h) * Dj[0] - Lb * (E[0] - A[0]),",
     "slope_quantization.strict_J_formula_violations"),
    ("D8_the_renewal_identity_adds_the_endpoint_slack",
     "                if (A[0] + Di[0] - Dj[0] - E[0],",
     "                if (A[0] + Di[0] - Dj[0] + E[0],",
     "slope_quantization.renewal_identity_violations"),
    ("D9_theorem_4_4_is_tested_with_its_two_sides_swapped",
     "                        if not beta_linear_exceeds(E[0] - A[0], E[1] - A[1],",
     "                        if not beta_linear_exceeds(A[0] - E[0], A[1] - E[1],",
     "slope_quantization.theorem_4_4_violations"),
    ("D10_the_beta_sign_test_is_inverted",
     "    return (v > 1) - (v < 1)",
     "    return (v < 1) - (v > 1)",
     "slope_quantization.A_not_positive"),
    ("D11_the_lemma_5_1_mass_uses_the_parent_length_squared",
     "                    plateau_mass += g * Lb",
     "                    plateau_mass += g * La * La",
     "slope_quantization.lemma_5_1_violations"),
    # --- section 11 ---
    ("D12_the_reset_orientation_looks_for_the_lower_mediant",
     "                    if not beta_cmp(p + r, g + h) > 0:",
     "                    if not beta_cmp(p + r, g + h) < 0:",
     "orientation.reset_mediant_not_above_beta"),
    ("D13_the_child_denominator_bound_uses_the_wrong_coefficient",
     "                    if child.denominator < 2 * g + h:",
     "                    if child.denominator < 3 * g + h:",
     "orientation.child_denominator_below_2g_plus_h"),
    ("D14_the_child_slope_is_required_above_its_own_mediant",
     "                    if not (beta_cmp(Qb, Lb) > 0 and child < mu):",
     "                    if not (beta_cmp(Qb, Lb) > 0 and child > mu):",
     "orientation.reset_child_slope_not_between_beta_and_mediant"),
    ("D15_the_farey_neighbour_identity_expects_the_wrong_determinant",
     "                if (p + r) * g - p * (g + h) != 1:",
     "                if (p + r) * g - p * (g + h) != 2:",
     "orientation.farey_neighbour_identity_violations"),
    # --- premises and the corridor ---
    ("D16_u_beta_uses_one_bit_too_many",
     "        total += Fraction(1 << (p3.bit_length() - 1), p3)",
     "        total += Fraction(1 << p3.bit_length(), p3)",
     "premises.u_beta_above_L_over_3"),
    ("D17_the_slope_separation_threshold_is_not_squared",
     "                    if y - x < Fraction(1, L * L):",
     "                    if y - x < Fraction(1, L):",
     "premises.distinct_slopes_closer_than_one_over_L_squared"),
    ("D26_the_caps_are_applied_without_their_premise",
     "            if origin_ok and endpoint_ok and survives:",
     "            if True:",
     "premises.theorem_4_3_violations"),
    # --- the derivations ---
    ("D18_the_algebraic_constant_loses_its_factor_of_three",
     "    two_b2_over_a_hi = (12 + 8 * r2_hi) / 3",
     "    two_b2_over_a_hi = (12 + 8 * r2_hi) / 2",
     "2b^2/a is not below 8"),
    ("D19_corollary_6_2_is_compared_the_wrong_way_round",
     "                if master_hi > explicit_lo:",
     "                if master_hi < explicit_lo:",
     "derivations.cor_6_2_not_implied_by_thm_6_1"),
    ("D20_the_depth_root_takes_the_wrong_branch",
     "                X_lo = (disc_lo - b_hi) / (2 * a_hi)",
     "                X_lo = (disc_lo + b_hi) / (2 * a_hi)",
     "derivations.X_r_not_a_root_of_a_x2_plus_b_x"),
    # --- the artifacts ---
    ("D21_the_digest_comparison_is_negated",
     "        (verified if got == want else mismatched).append(",
     "        (verified if got != want else mismatched).append(",
     "sha256 mismatches"),
    ("D22_the_item_53_validation_shape_is_not_recognised",
     '    elif isinstance(validation.get("files"), dict):',
     "    elif False:",
     "the validation record shape is unrecognised"),
    ("D23_a_shipped_example_is_recomputed_with_the_wrong_sign",
     '            "J_recomputes": Qj * Li - Qi * Lj == ex["J"],',
     '            "J_recomputes": Qj * Li + Qi * Lj == ex["J"],',
     "a unit-reset example fails a clause"),
    ("D24_only_the_old_report_key_is_read",
     '    stated = list(report.get("verified_statements", '
     'report.get("verified_claims", [])))',
     '    stated = list(report.get("verified_claims", []))',
     "the report key may have been renamed again"),
    ("D25_the_paper_ledger_anchor_no_longer_matches",
     '    prose_items = re.findall(r"^(\\d+)\\. ", paper[prose_start:prose_end], re.M)',
     '    prose_items = re.findall(r"^(\\d+)\\) ", paper[prose_start:prose_end], re.M)',
     "the paper's own ledger section was not parsed"),
    # --- robustness ---
    ("D27_the_no_go_heading_echo_is_dropped",
     '        "no_go_headings_in_the_paper": [h for h, _ in no_go_headings],',
     '        "no_go_headings_in_the_paper": [],',
     "__robustness: the shortfall count stands without the echo__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D27_the_no_go_heading_echo_is_dropped": None,
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
