"""Can the item-54 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src54_low_source_saturation.py` reports that section 3's exact multiplicative
identity holds on every real segment, that section 4's consecutive-odd envelope
holds wherever its premise does -- which here is everywhere -- that section 5's
Gamma representation is an identity between two rationals and needs no Gamma
evaluated at all, that section 9.1 is untestable on real orbits because its
endpoint-gap premise is met by none of them, and that this round's floors
recompute from A-U.2d.7's Theorem 7.1.

D9 is the positive control on the premise gate, carried over from RUN-035 and
more important here. Theorem 9.1's premise is met by ZERO real chains, so
"0 violations of 0 subjects" is exactly the reading a vacuous filter would
produce. D9 deletes the gate; thousands of violations must appear and the run
must go RED. Without that, the empty denominator proves nothing.

D15 replants this run's own instrument error. Comparing a published double
against a rational bracket rendered to a fixed number of decimal places measured
the truncation rather than the artifact: `c_H` came out 75 ulps and
`log2 Y_ver` 78929, both pure fiction. Rounding is monotone, so the bracket
itself decides -- or admits it cannot.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), robustness properties (45), a pre-flight naming
malformed mutations (46), byte-exact restore (47), a failure for every empty
locator (48), a pristine sidecar against a killed drill (50), premise before
conclusion (51), a guard on the largest case reached (52), and enumerating
counters rather than matching their names (53).

Usage:  python code/src54_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src54_low_source_saturation.py"
LIMIT = "2500"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- section 3, the exact multiplicative identity ---
    ("D1_the_identity_swaps_its_two_bases",
     "            first = Fraction(3) ** L / Fraction(2) ** Q * script_p",
     "            first = Fraction(2) ** L / Fraction(3) ** Q * script_p",
     "segments.product_identity_violations"),
    ("D2_the_correction_factor_uses_two_where_the_map_uses_three",
     "                script_p *= 1 + Fraction(1, 3 * values[j])",
     "                script_p *= 1 + Fraction(1, 2 * values[j])",
     "segments.product_identity_violations"),
    ("D3_the_two_printed_forms_stop_being_compared",
     "            if first != Fraction(3, 2) ** 0 * Fraction(3 ** L, 2 ** Q) * script_p:",
     "            if first != Fraction(3, 2) ** 0 * Fraction(3 ** L, 2 ** Q) * script_p * 2:",
     "segments.two_forms_of_the_identity_disagree"),
    # --- section 4, the packing envelope ---
    ("D4_the_envelope_factor_overshoots_by_one",
     "        out *= Fraction(d + 1, d)",
     "        out *= Fraction(d + 2, d)",
     "segments.gamma_form_disagrees_with_the_product"),
    ("D5_the_envelope_spaces_its_odds_four_apart",
     "        d = 3 * (y + 2 * k)",
     "        d = 3 * (y + 4 * k)",
     "segments.packing_envelope_violations"),
    ("D6_the_sorted_state_bound_uses_the_wrong_spacing",
     "                if v < y + 2 * k:",
     "                if v < y + 3 * k:",
     "segments.sorted_state_below_y_plus_2k"),
    # --- section 5, the Gamma representation ---
    ("D7_the_pochhammer_shift_is_one_fifth",
     "    a, b = Fraction(y, 2) + Fraction(1, 6), Fraction(y, 2)",
     "    a, b = Fraction(y, 2) + Fraction(1, 5), Fraction(y, 2)",
     "segments.gamma_form_disagrees_with_the_product"),
    ("D8_the_lgamma_combination_flips_a_sign",
     "        approx = terms[0] + terms[1] - terms[2] - terms[3]",
     "        approx = terms[0] - terms[1] - terms[2] - terms[3]",
     "gamma.lgamma_disagreements_beyond_cancellation"),
    # --- section 9.1 ---
    ("D9_the_caps_are_applied_without_their_premise",
     "            if not (packing and gap):\n                continue",
     "            if False:\n                continue",
     "harmonic_depth.theorem_9_1_violations"),
    ("D10_the_two_forms_of_9_1_are_compared_at_different_scales",
     "            right = Fraction(r) < Fraction(1, 2) + Fraction(y1, 4) * (P - 1)",
     "            right = Fraction(r) < Fraction(1, 2) + Fraction(y1, 8) * (P - 1)",
     "harmonic_depth.the_two_forms_of_9_1_are_not_equivalent"),
    # --- the envelopes on a grid ---
    ("D11_the_harmonic_envelope_halves_its_logarithmic_term",
     "            if not R_lo <= a_hi / (3 * y) + l_hi * a_hi / 6:",
     "            if not R_lo <= a_hi / (3 * y) + l_hi * a_hi / 12:",
     "grids.harmonic_envelope_violations"),
    ("D12_the_coarse_envelope_is_ten_times_too_tight",
     "            if not R_lo < Fraction(L) * a_hi / (3 * y):",
     "            if not R_lo < Fraction(L) * a_hi / (30 * y):",
     "grids.coarse_envelope_violations"),
    ("D13_the_sixth_root_cap_loses_an_order_of_magnitude",
     "            sixth_cap_lo = Fraction(1, 2) + CH_lo * root_lo",
     "            sixth_cap_lo = Fraction(1, 2) + CH_lo * root_lo / 10",
     "grids.sixth_root_cap_violations"),
    ("D14_mu_star_is_defined_over_six_instead_of_five",
     "    mu = (6 * theta - 1) / 5\n    old = theta / (1 + theta)\n"
     "    if mu != (6 * theta - 1) / 5:",
     "    mu = (6 * theta - 1) / 6\n    old = theta / (1 + theta)\n"
     "    if mu != (6 * theta - 1) / 5:",
     "grids.mu_star_not_six_theta_minus_one_over_five"),
    ("D15_the_log_series_is_truncated_after_four_terms",
     "def ln_bracket(x: Fraction, terms: int = 80)",
     "def ln_bracket(x: Fraction, terms: int = 4)",
     "the bracket could not decide"),
    # --- the A-U.2d.7 carryover ---
    ("D16_the_verification_floor_is_off_by_a_power_of_two",
     "    Y = 2075 * 2 ** 60",
     "    Y = 2075 * 2 ** 61",
     "au2d7_carryover: 2075*2^60 is not the published floor"),
    ("D17_the_log_range_reduction_divides_by_three",
     "    while x >= 2:\n        x /= 2",
     "    while x >= 2:\n        x /= 3",
     "instrument.ln_of_four_is_not_twice_ln_two"),
    # --- the two manifests ---
    ("D18_the_checksum_comparison_is_negated",
     "        \"CHECKSUMS_mismatches\": sorted(n for n, d in cs.items()\n"
     "                                       if actual.get(n) != d),",
     "        \"CHECKSUMS_mismatches\": sorted(n for n, d in cs.items()\n"
     "                                       if actual.get(n) == d),",
     "artifacts.CHECKSUMS_mismatches"),
    ("D19_the_cross_manifest_comparison_is_negated",
     "            sorted(n for n in set(cs) & set(sv) if cs[n] != sv[n]),",
     "            sorted(n for n in set(cs) & set(sv) if cs[n] == sv[n]),",
     "artifacts.digests_disagreeing_between_the_two_manifests"),
    ("D20_the_item_54_validation_shape_is_not_recognised",
     "    if isinstance(files, list):",
     "    if False:",
     "the validation record shape is unrecognised"),
    # --- empty locators must be refused, not passed ---
    ("D21_the_paper_ledger_anchor_no_longer_matches",
     '    prose = re.findall(r"^(\\d+)\\. ", block("## 21.1 Proved internally",',
     '    prose = re.findall(r"^(\\d+)\\) ", block("## 21.1 Proved internally",',
     "the paper's own ledger sections parsed empty"),
    ("D22_only_a_key_this_report_does_not_use_is_read",
     '    stated = list(report.get("checks", {}))',
     '    stated = list(report.get("verified_statements", {}))',
     "checker entries were read"),
    # A two-term exponential bracket is WIDE, not wrong: it still contains the
    # true value, so no containment check can catch it and the self-check
    # correctly stays silent. What a bracket too wide to be useful breaks is
    # decidability, and that is where this is caught.
    ("D23_the_exponential_series_stops_after_two_terms",
     "def _exp_bracket(x: Fraction, terms: int = 120)",
     "def _exp_bracket(x: Fraction, terms: int = 2)",
     "the bracket could not decide"),
    # --- robustness ---
    ("D24_the_scope_note_echo_is_dropped",
     '        "scope_note": validation.get("scope_note"),',
     '        "scope_note": None,',
     "__robustness: the manifest verdict stands without the echo__"),

    ("D25_the_nth_root_loses_its_upper_bound",
     "    return _nth_root_lo(x, n, digits) + Fraction(1, 10 ** digits)",
     "    return _nth_root_lo(x, n, digits) - Fraction(1, 10 ** digits)",
     "instrument.cube_root_of_eight_does_not_contain_two"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D24_the_scope_note_echo_is_dropped": None,
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
