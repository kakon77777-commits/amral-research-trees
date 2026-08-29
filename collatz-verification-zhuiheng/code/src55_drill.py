"""Can the item-55 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src55_orbit_packing_deficit.py` reports that the Syracuse image sieve holds on
every odd integer tested, that the residue refinements it buys hold on every
post-entry source with `L >= 2`, that the 6-sieved envelope and its
two-progression Gamma form are exact, that Lemma 7.1's combinatorial core
survives half a million enumerated residue sets, and that Theorem 11.2 -- the
one theorem in this round whose premise real orbits actually meet -- holds on
every prefix tested.

D4 is the positive control on the premise gate, and it is the sharpest one this
sweep has had. Corollary 3.3 refines A-U.2d.5's `3 (mod 4)`, and THAT result
needs `L >= 2`. Applied to every first-crossing source instead, 11,775 of them
"violate" it -- a number about the check, not the round. D4 deletes the `L == 1`
branch and the run must go RED, which is what proves the premise gate is
load-bearing rather than merely exclusive.

D18 is its mirror. Theorem 11.2's premise is met by EVERY prefix, so unlike
A-U.2d.8's section 9.1 the theorem is genuinely tested -- and a defect that
inverts the subcriticality test empties the population, which the guard must
catch rather than read as a clean pass.

Habits carried in, each paid for by an earlier item: subprocess timeout (42),
defects aimed at subjects not comparisons (43), defects must break the result not
the interpreter (44, 45), robustness properties (45), a pre-flight naming
malformed mutations (46), byte-exact restore (47), a failure for every empty
locator (48), a pristine sidecar against a killed drill (50), premise before
conclusion (51), a guard on the largest case reached (52), enumerating counters
rather than matching their names (53), and a named failure rather than an assert
so a broken instrument reports instead of crashing (54).

Usage:  python code/src55_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src55_orbit_packing_deficit.py"
LIMIT = "2000"
TRIALS = "20000"
GATE_TIMEOUT_SECONDS = 600

DEFECTS = [
    # --- section 3, the sieve and what it buys ---
    ("D1_the_syracuse_map_adds_three_instead_of_one",
     "    t = 3 * n + 1\n    return t >> v2(t)",
     "    t = 3 * n + 3\n    return t >> v2(t)",
     "sieve.images_divisible_by_three"),
    ("D2_the_post_entry_residue_set_is_wrong",
     "            if values[j] % 6 not in (1, 5):",
     "            if values[j] % 6 not in (1, 3):",
     "sieve.states_not_1_or_5_mod_6"),
    ("D3_the_anchor_residue_set_is_wrong",
     "            if y % 12 not in (7, 11):\n                t[\"sources_not_7_or_11_mod_12\"] += 1",
     "            if y % 12 not in (7, 5):\n                t[\"sources_not_7_or_11_mod_12\"] += 1",
     "sieve.sources_not_7_or_11_mod_12"),
    ("D4_the_L_at_least_2_premise_is_removed",
     "            if L == 1:\n                t[\"sources_with_L_equal_1\"] += 1",
     "            if False:\n                t[\"sources_with_L_equal_1\"] += 1",
     "sieve.sources_not_7_or_11_mod_12"),
    # --- section 4, the sieved packing ---
    ("D5_the_admissible_set_forgets_the_three_sieve",
     "        if n % 2 and n % 3:",
     "        if n % 2:",
     "packing.explicit_admissible_position_errors"),
    ("D6_the_sieved_factor_uses_two_where_the_map_uses_three",
     "        out *= 1 + Fraction(1, 3 * a)",
     "        out *= 1 + Fraction(1, 2 * a)",
     "packing.two_progression_form_disagrees_with_the_product"),
    ("D7_the_uniform_lower_bound_claims_four_apart",
     "                if a[k] < y + 3 * k - 1:",
     "                if a[k] < y + 4 * k - 1:",
     "packing.uniform_lower_bound_a_k_below_y_plus_3k_minus_1"),
    ("D8_the_odd_envelope_is_spaced_three_apart",
     "        out *= 1 + Fraction(1, 3 * (y + 2 * k))",
     "        out *= 1 + Fraction(1, 3 * (y + 3 * k))",
     "packing.sieved_envelope_above_the_odd_envelope"),
    # --- section 5, the two-progression Gamma form ---
    ("D9_the_pochhammer_shift_is_one_seventeenth",
     "    a = Fraction(y + c, 6) + Fraction(1, 18)",
     "    a = Fraction(y + c, 6) + Fraction(1, 17)",
     "packing.two_progression_form_disagrees_with_the_product"),
    ("D10_the_second_progression_takes_the_wrong_offset",
     "    c = 4 if y % 6 == 1 else 2\n    out = gamma_progression(y, 0, n)",
     "    c = 2 if y % 6 == 1 else 4\n    out = gamma_progression(y, 0, n)",
     "packing.two_progression_form_disagrees_with_the_product"),
    ("D11_the_lgamma_combination_flips_a_sign",
     "            approx += four[0] + four[1] - four[2] - four[3]",
     "            approx += four[0] - four[1] - four[2] - four[3]",
     "gamma.lgamma_disagreements_beyond_cancellation"),
    ("D12_the_deficit_is_required_to_be_positive",
     "            if p6 - po >= 0:",
     "            if p6 - po <= 0:",
     "exponents.deficit_exponent_not_negative"),
    # --- section 7, the anchor gap ---
    ("D13_the_enumerated_span_bound_drops_its_phase_slack",
     "            if span < 6 * (r - 1) - 2:",
     "            if span < 6 * (r - 1):",
     "anchor_gap.spans_below_six_r_minus_eight"),
    ("D14_the_tight_phase_rule_expects_seven_mod_twelve",
     "            if combo[-1] % 12 != 11:",
     "            if combo[-1] % 12 != 7:",
     "anchor_gap.tight_sets_whose_last_anchor_is_not_11_mod_12"),
    # --- section 11, the valuation classes ---
    ("D15_a_valuation_is_expected_to_select_two_classes",
     "        if len(classes) != 1:",
     "        if len(classes) != 2:",
     "qclass.valuation_classes_not_exactly_one_mod_2_to_k_plus_1"),
    ("D16_the_interval_capacity_halves_its_allowance",
     "                if counts[k] > Fraction(W, 3 * (1 << k)) + 1:",
     "                if counts[k] > Fraction(W, 6 * (1 << k)):",
     "qclass.windows_where_N_k_exceeds_W_over_three_two_to_k_plus_one"),
    ("D17_the_weighted_capacity_uses_forty_eight_not_twenty_four",
     "            if weighted > Fraction(17 * W, 24) + 12:",
     "            if weighted > Fraction(17 * W, 48):",
     "qclass.windows_where_the_weighted_capacity_exceeds_17W_over_24_plus_12"),
    ("D18_the_subcriticality_premise_is_inverted",
     "            if 2 ** Q < 3 ** m:",
     "            if 2 ** Q > 3 ** m:",
     "theorem 11.2 was applied to"),
    ("D19_the_span_bound_adds_where_it_subtracts",
     "            bound_hi = Fraction(24, 17) * ((4 - beta_lo) * m - 12)",
     "            bound_hi = Fraction(24, 17) * ((4 - beta_lo) * m + 12)",
     "qclass.theorem_11_2_violations"),
    # --- sections 6 and 8, on a grid ---
    ("D20_the_harmonic_envelope_halves_its_logarithmic_term",
     "                                           + l_hi / 9):",
     "                                           + l_hi / 18):",
     "grids.theorem_6_1_violations"),
    ("D21_the_uniform_power_form_loses_a_factor_of_two",
     "            if not P_hi <= C6_hi * ratio_hi:",
     "            if not P_hi <= C6_hi * ratio_hi / 2:",
     "grids.corollary_6_2_violations"),
    ("D22_the_uniform_constant_takes_an_eighteenth_root",
     "    C6_lo, C6_hi = widen(e_lo * _nth_root_lo(Fraction(4), 9),\n"
     "                         e_hi * _nth_root_hi(Fraction(4), 9))\n"
     "    C9_lo, C9_hi = C6_lo / 6, C6_hi / 6\n\n    for y in",
     "    C6_lo, C6_hi = widen(e_lo * _nth_root_lo(Fraction(4), 18),\n"
     "                         e_hi * _nth_root_hi(Fraction(4), 18))\n"
     "    C9_lo, C9_hi = C6_lo / 6, C6_hi / 6\n\n    for y in",
     # `C6` is Corollary 6.2's constant, so shrinking it breaks 6.2 first --
     # the check that owns it, and upstream of 8.2, which only ever sees
     # `C9 = C6/6`. Naming 8.2 here scored a working guard as a miss.
     "grids.corollary_6_2_violations"),
    ("D31_the_depth_constant_divides_by_sixty",
     "    C9_lo, C9_hi = C6_lo / 6, C6_hi / 6\n\n    for y in",
     "    C9_lo, C9_hi = C6_lo / 60, C6_hi / 60\n\n    for y in",
     "grids.corollary_8_2_not_implied_by_8_1"),
    # --- the instrument ---
    ("D23_the_tight_beta_inverts_its_quotient",
     "    return l3_lo / l2_hi, l3_hi / l2_lo",
     "    return l2_lo / l3_hi, l2_hi / l3_lo",
     "instrument.the_tight_beta_disagrees_with_the_certified_coarse_one"),
    # Aimed so the self-check FIRES. Making the comparison tautologically false
    # would leave the verdict identical, which the pre-flight would rightly call
    # "the mutation changes nothing" rather than a caught defect.
    ("D24_the_admissible_hand_list_is_wrong",
     "    if admissible(7, 4) != [7, 11, 13, 17]:",
     "    if admissible(7, 4) != [7, 11, 13, 19]:",
     "instrument.the_admissible_positions_disagree_with_a_hand_list"),
    # --- the manifests ---
    ("D25_the_checksum_comparison_is_negated",
     "        \"CHECKSUMS_mismatches\": sorted(n for n, d in cs.items()\n"
     "                                       if actual.get(n) != d),",
     "        \"CHECKSUMS_mismatches\": sorted(n for n, d in cs.items()\n"
     "                                       if actual.get(n) == d),",
     "artifacts.CHECKSUMS_mismatches"),
    ("D26_the_anonymous_digest_is_never_resolved",
     "        name = by_digest.get(rec[\"sha256\"])",
     "        name = by_digest.get(\"\")",
     "matches no file"),
    ("D27_the_item_55_validation_shape_is_not_recognised",
     "    elif blocks:",
     "    elif False:",
     "the validation record shape is unrecognised"),
    ("D28_the_paper_ledger_anchor_no_longer_matches",
     '    prose = re.findall(r"^(\\d+)\\. ", block("## 18.1 Proved internally",',
     '    prose = re.findall(r"^(\\d+)\\) ", block("## 18.1 Proved internally",',
     "the paper's own ledger sections parsed empty"),
    ("D29_only_a_key_this_report_does_not_use_is_read",
     '    stated = list(report.get("checks", {}))',
     '    stated = list(report.get("verified_statements", {}))',
     "checker entries were read"),
    # --- robustness ---
    ("D30_the_record_s_own_notes_echo_is_dropped",
     '        "the_record_s_own_notes": validation.get("notes", []),',
     '        "the_record_s_own_notes": [],',
     "__robustness: the manifest verdict stands without the echo__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

FINDING_ROBUSTNESS: dict[str, str | None] = {
    "D30_the_record_s_own_notes_echo_is_dropped": None,
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--bundle", str(bundle),
             "--limit", LIMIT, "--trials", TRIALS],
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
        "gate": GATE.name, "limit": LIMIT, "trials": TRIALS,
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
