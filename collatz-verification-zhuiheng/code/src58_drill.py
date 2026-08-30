"""Can the item-58 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src58_multistep_transport.py` reports that all three shipped transport dual
certificates satisfy their defining inequalities exactly -- 294 of them, with the
tail settled by a computed monotonicity bound rather than an assumed one -- that
each level's `alpha` is exactly what Corollary 5.3's formula gives, that section
3's residue transport identity holds on every residue class of every segment,
and that the mod-27 uniform envelope holds on every low-source segment.

The certificate defects are the ones that matter. A dual certificate is only
worth anything if a WRONG one would be rejected, so D1-D8 break the inequality,
the transition map, the tail bound, the sign conventions and the exponent
formula in turn. D9 is the positive control on the premise gate: Theorem 5.2
needs `z > y`, met by no real segment, so the gate could be excluding everything
-- deleting it must turn the run red.

D22 replants this run's own performance error, which was also a correctness
hazard: computing `x^(1373/25856)` by integer power and bisected root raises to
the 1373rd power and bisects a 25856-th root of a thousand-digit number. Eight
minutes, and the honest fix was the logarithm, not a smaller population.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), robustness properties (45), a pre-flight naming
malformed mutations (46), byte-exact restore (47), a failure for every empty
locator (48), a pristine sidecar (50), premise before conclusion (51), a guard on
the largest case reached (52), enumerated counters (53), a named failure rather
than an assert (54), a bracket tight enough to pin what it judges (55, 57), and a
defect decisive enough that a correct check must refuse it (57).

Usage:  python code/src58_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src58_multistep_transport.py"
LIMIT = "3000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- the certificates ---
    ("D1_the_certificate_inequality_is_reversed",
     "                if lhs < 1:",
     "                if lhs > 1:",
     "certificates.certificate_inequality_violations"),
    ("D2_the_certificate_drops_its_source_potential",
     "                lhs = (-3 * a[r] + 2 ** k * a[transition(r, k, M)]",
     "                lhs = (-4 * a[r] + 2 ** k * a[transition(r, k, M)]",
     "certificates.certificate_inequality_violations"),
    ("D3_the_transition_forgets_to_invert_the_power_of_two",
     "    return ((3 * r + 1) * pow(pow(2, k, M), -1, M)) % M",
     "    return ((3 * r + 1) * pow(2, k, M)) % M",
     "certificates.certificate_inequality_violations"),
    ("D4_the_transition_uses_the_wrong_affine_map",
     "    return ((3 * r + 1) * pow(pow(2, k, M), -1, M)) % M\n\n\n# ----",
     "    return ((3 * r + 2) * pow(pow(2, k, M), -1, M)) % M\n\n\n# ----",
     "certificates."),
    ("D5_the_tail_bound_demands_a_million",
     "        while 2 ** K * a_min - 3 * a_max < 1:",
     "        while 2 ** K * a_min - 3 * a_max < 10 ** 6:",
     "certificates.levels_where_the_computed_tail_exceeds_the_declared_one"),
    ("D6_the_exponent_formula_loses_its_third",
     "        alpha = sum(v / (M * 2 ** (k + 1)) for (_r, k), v in mu.items()) / 3",
     "        alpha = sum(v / (M * 2 ** (k + 1)) for (_r, k), v in mu.items())",
     "certificates.alpha_disagreeing_with_corollary_5_3"),
    ("D7_the_exponent_formula_takes_the_wrong_power_of_two",
     "        alpha = sum(v / (M * 2 ** (k + 1)) for (_r, k), v in mu.items()) / 3\n"
     "        pub_alpha",
     "        alpha = sum(v / (M * 2 ** k) for (_r, k), v in mu.items()) / 3\n"
     "        pub_alpha",
     "certificates.alpha_disagreeing_with_corollary_5_3"),
    ("D8_A_is_not_required_to_be_three_times_alpha",
     "        if pub_A != 3 * alpha:",
     "        if pub_A != 4 * alpha:",
     "certificates.A_not_three_times_alpha"),
    ("D9_the_potentials_are_required_to_exceed_one",
     '        t["potentials_not_positive"] += sum(1 for v in a.values() if v <= 0)',
     '        t["potentials_not_positive"] += sum(1 for v in a.values() if v <= 1)',
     "certificates.potentials_not_positive"),
    ("D10_the_strongest_alpha_takes_the_largest",
     '    best = min((Fraction(c["product_exponent_alpha"]) for c in certs.values()),',
     '    best = max((Fraction(c["product_exponent_alpha"]) for c in certs.values()),',
     "certificates: the report's strongest alpha disagrees"),
    ("D11_eta11_is_measured_against_the_wrong_predecessor",
     "    eta = Fraction(4, 45) - best if best else None",
     "    eta = Fraction(1, 9) - best if best else None",
     "certificates: eta11 does not match the reported float"),
    # --- section 3, the transport identity ---
    ("D12_the_transport_identity_drops_its_factor_of_three",
     "                lhs = 3 * S_b.get(b, Fraction(0)) - sum(",
     "                lhs = 2 * S_b.get(b, Fraction(0)) - sum(",
     "transport.transport_identity_violations"),
    ("D13_the_transport_sum_forgets_its_weight",
     "                    2 ** k * v for (r, k), v in S_rk.items()",
     "                    v for (r, k), v in S_rk.items()",
     "transport.transport_identity_violations"),
    ("D14_the_boundary_terms_are_swapped",
     "                rhs = (Fraction(3, y) if y % M == b else Fraction(0)) \\\n"
     "                    - (Fraction(3, z) if z % M == b else Fraction(0)) \\",
     "                rhs = (Fraction(3, z) if z % M == b else Fraction(0)) \\\n"
     "                    - (Fraction(3, y) if y % M == b else Fraction(0)) \\",
     "transport.transport_identity_violations"),
    ("D15_the_cross_term_is_added_where_it_is_subtracted",
     "                    - C_b.get(b, Fraction(0))",
     "                    + C_b.get(b, Fraction(0))",
     "transport.transport_identity_violations"),
    # --- section 4, the channel ---
    ("D16_the_channel_modulus_forgets_the_three_adic_part",
     "            D = M * 2 ** (k + 1)\n            for r in range(M):",
     "            D = 2 ** (k + 1)\n            for r in range(M):",
     "channel."),
    ("D17_the_channel_modulus_is_off_by_a_power_of_two",
     "            if D != 3 ** h * 2 ** (k + 1):",
     "            if D != 3 ** h * 2 ** k:",
     "channel.modulus_disagreeing_with_3h_2k1"),
    ("D18_the_channel_capacity_drops_its_leading_term",
     "                bound = Fraction(1, y) + ln_cached(1 + Fraction(D * L, y))[1] / D",
     "                bound = ln_cached(1 + Fraction(D * L, y))[1] / (D * 1000)",
     "channel.capacity_violations"),
    # --- sections 5 and 8 ---
    # Neither half fires alone: with the gate in place the block is
    # premise-empty, and with only the gate removed the bound has enough
    # slack that no segment violates it. Both together are decisive.
    ("D19_the_mass_bound_loses_both_its_premise_and_its_slack",
     '            if z <= y:\n                continue\n            t["segments_meeting_the_endpoint_premise"] += 1\n            t["theorem_5_2_checked"] += 1\n            Stot = sum(Fraction(1, values[j]) for j in range(s, end))\n            rhs = Fraction(51, 14) * a_max / y\n            for (r, k), v in mu.items():\n                D = M * 2 ** (k + 1)\n                rhs += v * (Fraction(1, y)\n                            + ln_cached(1 + Fraction(D * L, y))[1] / D)\n            if Stot > rhs:',
     '            if False:\n                continue\n            t["segments_meeting_the_endpoint_premise"] += 1\n            t["theorem_5_2_checked"] += 1\n            Stot = sum(Fraction(1, values[j]) for j in range(s, end))\n            rhs = Fraction(51, 14) * a_max / y\n            for (r, k), v in mu.items():\n                D = M * 2 ** (k + 1)\n                rhs += v * (Fraction(1, y)\n                            + ln_cached(1 + Fraction(D * L, y))[1] / D)\n            if Stot > rhs / 10 ** 6:',
     "mass_and_product.theorem_5_2_violations"),
    ("D20_the_multiplier_support_check_shifts_its_cutoff",
     '            1 for (_r, k) in mu if k > tail)',
     '            1 for (_r, k) in mu if k > tail - 3)',
     "certificates.multipliers_beyond_the_declared_tail"),
    ("D21_the_uniform_envelope_is_a_thousand_times_too_tight",
     "                if script > C11_hi * ratio_hi:",
     "                if script > C11_hi * ratio_hi / 1000:",
     "mass_and_product.uniform_envelope_violations"),
    ("D22_the_reciprocal_branch_forgets_to_flip_the_bracket_end",
     "        return 1 / pow_frac(1 / x, p, q, not hi)",
     "        return 1 / pow_frac(1 / x, p, q, hi)",
     "instrument.pow_frac_returns_an_inverted_bracket_below_one"),
    # --- section 12, the diagnostics ---
    ("D23_the_hierarchy_exponent_relation_is_wrong",
     '        if abs(row["reciprocal_coeff"] / 3 - row["product_exponent"]) > 1e-15:',
     '        if abs(row["reciprocal_coeff"] / 2 - row["product_exponent"]) > 1e-15:',
     "hierarchy.rows_where_the_exponent_is_not_the_coefficient_over_three"),
    ("D24_the_hierarchy_is_required_to_increase",
     '        if prev is not None and row["product_exponent"] >= prev:',
     '        if prev is not None and row["product_exponent"] <= prev:',
     "hierarchy.rows_not_decreasing_in_h"),
    ("D25_the_certified_levels_are_not_compared_to_the_diagnostic",
     '            if abs(float(exact) - row["product_exponent"]) > 1e-12:',
     '            if abs(float(exact) * 2 - row["product_exponent"]) > 1e-12:',
     "hierarchy.certified_levels_disagreeing_with_the_diagnostic"),
    # --- the constants ---
    ("D26_the_exact_rational_string_check_is_defeated",
     '        "alpha_mod27_exact": str(alpha) == pub.get("alpha_mod27_exact"),',
     '        "alpha_mod27_exact": str(2 * alpha) == pub.get("alpha_mod27_exact"),',
     "constants: alpha_mod27_exact does not reproduce"),
    ("D27_the_relative_deficit_constant_uses_the_wrong_roots",
     "    den_lo = _nth_root_lo(Fraction(6), 15, 40) * _nth_root_lo(Fraction(12), 45, 40)",
     "    den_lo = _nth_root_lo(Fraction(6), 45, 40) * _nth_root_lo(Fraction(12), 15, 40)",
     "matches no reference"),
    # --- the manifests ---
    ("D28_the_checksum_comparison_is_negated",
     '        "CHECKSUMS_mismatches": sorted(n for n, d in cs.items()\n'
     '                                       if actual.get(n) != d),',
     '        "CHECKSUMS_mismatches": sorted(n for n, d in cs.items()\n'
     '                                       if actual.get(n) == d),',
     "artifacts.CHECKSUMS_mismatches"),
    ("D29_only_a_key_this_report_does_not_use_is_read",
     '    stated = list(report.get("checks", {}))',
     '    stated = list(report.get("verified_statements", {}))',
     "checker entries were read"),
    ("D30_the_paper_ledger_anchor_no_longer_matches",
     '            len(re.findall(r"^(\\d+)\\. ", block("## 17.1 Proved internally",',
     '            len(re.findall(r"^(\\d+)\\) ", block("## 17.1 Proved internally",',
     "the paper's own ledger sections parsed empty"),
    # --- the instrument ---
    ("D31_the_modular_inverse_self_check_is_defeated",
     '    if pow(2, -1, 27) != 14 or (2 * 14) % 27 != 1:',
     '    if pow(2, -1, 27) != 15 or (2 * 15) % 27 != 1:',
     "instrument.the_modular_inverse_is_wrong"),
    ("D32_the_coarse_beta_bracket_is_used_instead_of_the_tight_one",
     "    beta_lo, beta_hi = beta_tight()",
     "    beta_lo, beta_hi = beta_bracket()",
     "instrument.the_beta_bracket_is_too_wide_to_pin_a_double"),
    # --- robustness ---
    ("D33_the_validation_field_echo_is_dropped",
     '        "validation_record_fields": sorted(\n'
     '            next(iter(files.values()))) if sv_names else [],',
     '        "validation_record_fields": [],',
     "__robustness: the manifest verdict stands without the echo__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D33_the_validation_field_echo_is_dropped": None,
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
    the non-vacuity guard, not by a failure."""
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
