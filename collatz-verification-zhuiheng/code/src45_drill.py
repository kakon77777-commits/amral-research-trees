"""Can the item-45 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src45_rotation_cap.py` reports that A-U.2d.1's arithmetic holds, that the shipped
JSON over-publishes its own precision, and that the shipped JSON is not what the
shipped script produces. The last two are claims **about the subject's artifacts**,
so they had better be claims this arm could have got wrong.

Habits carried in and all of them earned:

  - `GATE_TIMEOUT_SECONDS` from the start (item 42: a defect hung the gate and left
    a live mutation on disk).
  - Defects aim at **subjects, not comparisons** (item 43: weakening a check that
    never fires is undetectable).
  - Defects must break the **result, not the interpreter** (item 44: a crash is not
    the named check firing).

Usage:  python code/src45_drill.py --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src45_rotation_cap.py"
LIMIT = "2001"
GATE_TIMEOUT_SECONDS = 300

DEFECTS = [
    # --- the exact rational route for U ---
    ("D1_U_uses_the_wrong_floor",
     "        total += Fraction(1 << (p3.bit_length() - 1), p3)",
     "        total += Fraction(1 << p3.bit_length(), p3)",
     "shipped_U_values"),
    ("D2_U_forgets_its_third",
     "    _U_CACHE[L] = total / 3\n    return _U_CACHE[L]",
     "    _U_CACHE[L] = total\n    return _U_CACHE[L]",
     "shipped_U_values"),
    # --- the high-precision recurrence, and its guard ---
    ("D3_the_recurrence_uses_the_wrong_wrapped_ratio",
     "                t = t * 4 / 3",
     "                t = t * 5 / 3",
     "denjoy_koksma: the two routes disagree"),
    ("D4_the_unwrapped_ratio_is_wrong",
     "                t = t * 2 / 3",
     "                t = t * 3 / 4",
     "denjoy_koksma: the two routes disagree"),
    ("D5_the_overlap_cross_check_never_runs",
     "        if q <= 400:",
     "        if q <= 1:",
     "never compared against the exact one"),
    # --- constants ---
    ("D6_eta_is_not_one_over_six_ln2",
     '        "eta_beta": ("1/(6 ln 2)", 1 / (6 * ln2)),',
     '        "eta_beta": ("1/(6 ln 2)", 1 / (5 * ln2)),',
     "constants"),
    ("D7_the_sqrt_constant_uses_the_wrong_root",
     '        "improved_sqrt_y_constant": ("sqrt(3) * ln 2", Decimal(3).sqrt() * ln2),',
     '        "improved_sqrt_y_constant": ("sqrt(3) * ln 2", Decimal(2).sqrt() * ln2),',
     "constants"),
    # --- the convergent denominators, by the independent route ---
    # D8 first reversed the descent, which never converges: the walk stopped
    # bracketing and the gate HUNG. The timeout caught it, but a timeout is not
    # the named check firing. This breaks the convergent DETECTION instead, which
    # gives a wrong list and terminates.
    ("D8_convergents_are_detected_at_the_wrong_step",
     "        if i + 1 < len(rows) and rows[i + 1][1] != side:",
     "        if i + 1 < len(rows) and rows[i + 1][1] == side:",
     "convergent_denominators"),
    ("D9_the_descent_stops_at_the_largest_published_q",
     "    mine = [q for q in stern_brocot_convergents(max(published) * 3)",
     "    mine = [q for q in stern_brocot_convergents(max(published) * 1)",
     "convergent_denominators"),
    # --- Denjoy-Koksma ---
    # D10 first replaced the constant `1/3` with `1/6` and was NOT caught: the
    # largest deviation over the shipped convergents is about 0.139, comfortably
    # below 1/6, so THIS DATA CANNOT SEE THAT ERROR. It is the mistake I nearly
    # made myself. The cure was to assert the variation against its DEFINITION
    # rather than against the data, and this defect now drops the jump term from
    # that derivation — which is exactly the way the error would be made.
    ("D10_the_variation_forgets_the_jump",
     "    variation_exact = (f0 - f1) + (f0 - f1)   # descent + jump",
     "    variation_exact = (f0 - f1)   # descent + jump",
     "denjoy_koksma: the variation does not match its own definition"),
    # --- the round's core inequality, on real orbits ---
    ("D11_the_cap_comparison_is_inverted",
     "        if b3 > u:\n            cap_bad.append(n)",
     "        if b3 < u:\n            cap_bad.append(n)",
     "rotation_cap"),
    # D12 first LOOSENED the termwise bound, which is undetectable: `Q_j <=
    # floor(beta j)` always holds, so allowing one more never fires. Tightening it
    # does fire, precisely because the bound is ATTAINED -- the attainment
    # measured in this run is what gives this defect something to hit.
    ("D12_the_termwise_bound_is_one_too_strict",
     "            if Qs[j] > p3.bit_length() - 1:",
     "            if Qs[j] > p3.bit_length() - 2:",
     "rotation_cap"),
    ("D13_B_over_3L_is_built_from_the_wrong_exponent",
     "        b3 = sum(Fraction(1 << Qs[j], 3 ** j) for j in range(L)) / 3",
     "        b3 = sum(Fraction(1 << Qs[j], 3 ** (j + 1)) for j in range(L)) / 3",
     "rotation_cap"),
    # --- endpoint-gap quantization ---
    ("D14_the_quantized_form_drops_its_factor_of_two",
     "        if b3 != (two_d - 1) * n + 2 * two_d * h:",
     "        if b3 != (two_d - 1) * n + two_d * h:",
     "endpoint_gap"),
    # --- the two artifact findings, which are claims ABOUT the subject ---
    # N3 below, not a defect: see FINDING_ROBUSTNESS.
    ("N3_one_broken_signal_must_NOT_remove_the_provenance_finding",
     '    missing_top = [k for k in script_top if k not in json_top]',
     '    missing_top = [k for k in json_top if k not in json_top]',
     "__the finding must survive__"),
    ("D16_the_precision_finding_never_fires",
     "        k = next((i for i, (a, b) in enumerate(zip(pub, mine)) if a != b), None)",
     "        k = next((i for i, (a, b) in enumerate(zip(pub, pub)) if a != b), None)",
     "__precision finding disappears__"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]

#: Two of the defects break a FINDING rather than a gate check. A finding that
#: cannot disappear is not a finding — it is a sentence. These are verified by
#: watching the finding vanish from the report, not by watching `failures` grow.
FINDING_DEFECTS = {
    "D16_the_precision_finding_never_fires": "more decimals than its own computation",
}

#: NOT a defect — a robustness property, and it started life as a failed defect.
#:
#: The provenance finding rests on FOUR independent signals: keys the script
#: writes that the JSON lacks, keys the JSON has that the script does not write,
#: and the two row-key comparisons. Breaking one was supposed to make the finding
#: vanish; it did not, because three still fired. That is the check being robust,
#: not the drill missing. So the expectation is inverted and pinned: **one broken
#: signal must NOT remove the finding.** If a future refactor collapses those four
#: into one, this goes red.
FINDING_ROBUSTNESS = {
    "N3_one_broken_signal_must_NOT_remove_the_provenance_finding":
        "not produced by the shipped script",
}


def run_gate(bundle: pathlib.Path) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--limit", LIMIT, "--bundle", str(bundle)],
            capture_output=True, text=True, cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {"passed": False, "failures": ["__the gate did not terminate__"],
                "findings": [], "hung": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "failures": ["__the gate did not produce JSON__"],
                "findings": [], "stderr_tail": proc.stderr[-400:]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", type=pathlib.Path, required=True)
    args = ap.parse_args()

    snapshot = GATE.read_bytes()
    base = run_gate(args.bundle)
    report: dict = {
        "gate": GATE.name,
        "baseline": {"passed": base.get("passed"), "failures": base.get("failures"),
                     "findings": base.get("findings")},
        "defects": {}, "controls": {},
    }
    if not base.get("passed"):
        report["ok"] = False
        report["note"] = "the gate is not green before anything was planted"
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 2
    baseline_findings = base.get("findings", [])

    text = GATE.read_text(encoding="utf-8")
    for name, old, new, expected in DEFECTS:
        hits = text.count(old)
        if hits != 1:
            report["defects"][name] = {
                "caught": False, "anchor_matches": hits,
                "note": "anchor matches %d times; aimed at nothing" % hits}
            continue
        try:
            GATE.write_text(text.replace(old, new), encoding="utf-8")
            res = run_gate(args.bundle)
        finally:
            GATE.write_text(text, encoding="utf-8")

        if name in FINDING_ROBUSTNESS:
            needle = FINDING_ROBUSTNESS[name]
            was = any(needle in f for f in baseline_findings)
            now = any(needle in f for f in res.get("findings", []))
            report["defects"][name] = {
                "caught": was and now,        # SURVIVING is the pass condition
                "kind": "robustness: the finding must SURVIVE one broken signal",
                "finding_present_at_baseline": was,
                "finding_survived_the_break": now,
            }
            continue
        if name in FINDING_DEFECTS:
            needle = FINDING_DEFECTS[name]
            was = any(needle in f for f in baseline_findings)
            now = any(needle in f for f in res.get("findings", []))
            report["defects"][name] = {
                "caught": was and not now,
                "kind": "breaks a FINDING, not a gate check",
                "finding_present_at_baseline": was,
                "finding_present_with_defect": now,
            }
            continue

        failures = res.get("failures", [])
        by_own = any(expected in f for f in failures)
        report["defects"][name] = {
            "caught": by_own, "expected_failure_named": expected,
            "reported": failures[:4],
            "caught_by_something_else_only": bool(failures) and not by_own,
            "hung": bool(res.get("hung")),
        }

    for name, suffix in CONTROLS:
        raw = GATE.read_bytes()
        try:
            GATE.write_bytes(raw + suffix)
            res = run_gate(args.bundle)
        finally:
            GATE.write_bytes(raw)
        report["controls"][name] = {"undisturbed": bool(res.get("passed"))}
    report["controls"]["N2_the_gate_is_restored_byte_exactly"] = {
        "undisturbed": GATE.read_bytes() == snapshot}

    caught = sum(1 for v in report["defects"].values() if v.get("caught"))
    report["counts"] = {
        "planted": len(DEFECTS), "caught_by_their_own_check": caught,
        "missed": len(DEFECTS) - caught,
        "finding_defects": len(FINDING_DEFECTS),
        "finding_robustness_properties": len(FINDING_ROBUSTNESS),
        "hung": sum(1 for v in report["defects"].values() if v.get("hung")),
        "controls": len(report["controls"]),
        "controls_undisturbed": sum(1 for c in report["controls"].values()
                                    if c["undisturbed"]),
    }
    report["ok"] = (caught == len(DEFECTS)
                    and all(c["undisturbed"] for c in report["controls"].values()))
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
