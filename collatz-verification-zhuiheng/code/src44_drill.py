"""Can the item-44 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src44_source_freeze.py` reports that A-U.2d's arithmetic holds and that real
orbits sit on the *opposite* side of its §15 scale separation. Both are claims
that could be wrong quietly, so each check is broken in turn and the recheck must
go red **for the reason named for it**.

Two habits carried in from items 42 and 43, both learned by getting them wrong:

  - `GATE_TIMEOUT_SECONDS` from the start. A planted defect once made the gate
    loop forever, hanging the drill so its restore never ran and leaving a live
    defect in the gate on disk.
  - **Defects aim at SUBJECTS, not comparisons.** Weakening a comparison that
    never fires is undetectable; four misses in one run taught that. So the
    mutations here corrupt what is computed — the series, the horizon, the
    contraction, the bank — rather than loosening the tests that read them.

Usage:  python code/src44_drill.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src44_source_freeze.py"
LIMIT = "6001"
GATE_TIMEOUT_SECONDS = 120

DEFECTS = [
    # --- section 2, the 2-adic source series ---
    ("D1_the_source_series_loses_its_sign",
     "        b = (-acc) % mod",
     "        b = acc % mod",
     "shift_hereditary_source"),
    ("D2_the_source_series_uses_the_wrong_power_of_three",
     "            acc = (acc + pow(2, Qs[j], mod) * pow(inv3, j + 1, mod)) % mod",
     "            acc = (acc + pow(2, Qs[j], mod) * pow(inv3, j + 2, mod)) % mod",
     "shift_hereditary_source"),
    ("D3_the_local_valuations_are_not_local",
     "    Qs, ys, Q = [0], [y], 0",
     "    Qs, ys, Q = [0], [y], 1",
     "shift_hereditary_source"),
    ("D4_the_negative_control_compares_against_itself",
     "        other, _Q2, _y2 = accel_tail(n + 2, s, 30)",
     "        other, _Q2, _y2 = accel_tail(n, s, 30)",
     "the negative control never ran"),
    # --- sections 4, 8, 9, the horizons ---
    # D5 first used `Qs[m] - 3`, which raises on a negative shift: the gate died
    # instead of reporting, and "did not produce JSON" is not the named check
    # firing. A defect must break the result, not the interpreter.
    ("D5_the_freeze_threshold_is_far_too_strict",
     "        f2 = next((m for m in range(len(Qs)) if (1 << (Qs[m] + 1)) > n), None)",
     "        f2 = next((m for m in range(len(Qs)) if (1 << (Qs[m] + 1)) > n * n), None)",
     "horizons: freeze bound"),
    # D6 first replaced floor_log32 with floor_log2 and was NOT caught, because
    # the horizon bound used floor_log32 on BOTH sides -- the check compared the
    # mutated function against itself. The gate now asserts floor_log32's
    # DEFINING inequalities and the domination floor(log2 y) <= floor(log_{3/2} y)
    # separately, so this mutation has something independent to contradict.
    ("D6_floor_log32_is_computed_as_floor_log2",
     "    while 3 ** (k + 1) <= (1 << (k + 1)) * y:",
     "    while (1 << (k + 1)) <= y:",
     "horizons"),
    ("D7_the_bit_length_horizon_is_off_by_one",
     "    return y.bit_length() - 1",
     "    return y.bit_length() - 2",
     "horizons"),
    # --- the contraction behind endpoint exposure ---
    ("D8_the_contraction_step_forgets_to_divide",
     "        s = t >> ((t & -t).bit_length() - 1)\n        checked += 1",
     "        s = t\n        checked += 1",
     "contraction"),
    # --- sections 10, 11, the bank ---
    ("D9_the_accumulated_bank_increment_loses_its_three",
     "            acc += Fraction(1 << Qs[m], 3 ** (m + 1))",
     "            acc += Fraction(1 << Qs[m], 3 ** m)",
     "adelic_bank"),
    ("D10_the_closed_form_bank_uses_the_wrong_endpoint",
     "            closed = Fraction((1 << Qs[m]) * ys[m], 3 ** m)",
     "            closed = Fraction((1 << Qs[m]) * ys[0], 3 ** m)",
     "adelic_bank"),
    ("D11_the_two_adic_valuation_is_read_off_the_denominator",
     "            v2 = (num & -num).bit_length() - 1",
     "            v2 = (den & -den).bit_length() - 1",
     "adelic_bank"),
    ("D12_the_archimedean_negative_half_is_emptied",
     "            if any(Fraction((1 << Qs[m]) * ys[m], 3 ** m) > y_s + Fraction(m, 3)\n"
     "                   for m in range(len(Qs))):",
     "            if any(Fraction((1 << Qs[m]) * ys[m], 3 ** m) > y_s + Fraction(m, 3)\n"
     "                   for m in range(0)):",
     "no negative half"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]


def run_gate() -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--limit", LIMIT],
            capture_output=True, text=True, cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {"passed": False, "failures": ["__the gate did not terminate__"],
                "hung": True}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "failures": ["__the gate did not produce JSON__"],
                "stderr_tail": proc.stderr[-400:]}


def main() -> int:
    snapshot = GATE.read_bytes()
    base = run_gate()
    report: dict = {
        "gate": GATE.name,
        "baseline": {"passed": base.get("passed"), "failures": base.get("failures")},
        "defects": {}, "controls": {},
    }
    if not base.get("passed"):
        report["ok"] = False
        report["note"] = "the gate is not green before anything was planted"
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 2

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
            res = run_gate()
        finally:
            GATE.write_text(text, encoding="utf-8")
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
            res = run_gate()
        finally:
            GATE.write_bytes(raw)
        report["controls"][name] = {"undisturbed": bool(res.get("passed"))}
    report["controls"]["N2_the_gate_is_restored_byte_exactly"] = {
        "undisturbed": GATE.read_bytes() == snapshot}

    caught = sum(1 for v in report["defects"].values() if v.get("caught"))
    report["counts"] = {
        "planted": len(DEFECTS), "caught_by_their_own_check": caught,
        "missed": len(DEFECTS) - caught,
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
