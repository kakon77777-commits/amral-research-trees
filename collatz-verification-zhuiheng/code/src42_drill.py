"""Can the item-42 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src42_infinite_support.py` reports that everything it can reach in Round
A-U.2e.3 holds. Most of that round quantifies over surviving resets, of which
this sample contains none, so the file's real job is separating what it can check
from what it cannot — and a separation is exactly the kind of claim that can be
wrong quietly.

So each check is broken in turn and the recheck must go red **for the reason
named for it**. A defect caught only by some other check is a miss: the named
check is not aimed at what it claims to cover.

Two of these exist because of near-misses this round produced:

  D8/D9 guard the corrigendum measurement, whose whole value is that two
  independent routes agree. If the routes were secretly the same computation the
  agreement would be worth nothing, so one defect breaks each route separately.

  D10 guards the two-sided half of the correction-bank bound. `A_m <= n + m/3`
  is a CASP-candidate statement and MUST fail on a real orbit after the crossing;
  a version that never observed the failure would be testing only the easy half.

Mutations are byte-level, restored under `try/finally`, verified byte-equal.

Usage:  python code/src42_drill.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src42_infinite_support.py"
LIMIT = "2001"

# (name, old, new, the failure string that must be reported)
DEFECTS = [
    ("D1_the_bank_uses_the_wrong_power_of_three",
     "    return [Fraction((1 << Ks[m]) * ys[m], 3 ** m) for m in range(len(ys))]",
     "    return [Fraction((1 << Ks[m]) * ys[m], 3 ** (m + 1)) for m in range(len(ys))]",
     "correction_bank"),
    ("D2_the_increment_identity_loses_its_third",
     "            if A[m + 1] - A[m] != Fraction((1 << Ks[m]), 3 ** (m + 1)):",
     "            if A[m + 1] - A[m] != Fraction((1 << Ks[m]), 3 ** m):",
     "correction_bank"),
    # D3 has been re-aimed twice. Version 1 weakened the `A_m >= n` scan and was
    # not caught, because that bound is implied by the base plus positive
    # increments. Version 2 asserted the base and strict monotonicity separately
    # -- and BOTH of those were also uncatchable: `A_0 == n` is true by
    # construction of bank(), and monotonicity follows from the increment
    # identity that D2 already covers. Replacing one vacuous check with two more
    # vacuous ones taught the actual lesson: when a check cannot fail, look for a
    # SECOND independent expression of the same quantity rather than another
    # proxy for the same one. Section 2 supplies one, and these two defects break
    # each side of the comparison.
    ("D3_the_accumulated_expression_starts_from_the_wrong_place",
     "        acc = Fraction(n)",
     "        acc = Fraction(n + 1)",
     "correction_bank"),
    ("D3b_the_accumulated_increment_loses_its_third",
     "            acc += Fraction((1 << Ks[m]), 3 * 3 ** m)",
     "            acc += Fraction((1 << Ks[m]), 3 ** m)",
     "correction_bank"),
    ("D4_the_upper_bound_is_checked_past_the_crossing",
     "        for m in range(min(L, len(A))):\n"
     "            if A[m] > n + Fraction(m, 3):",
     "        for m in range(len(A)):\n"
     "            if A[m] > n + Fraction(m, 3):",
     "correction_bank"),
    ("D5_the_transcription_check_is_inverted_again",
     "                right = (Fraction(3 ** a * (1 << Ks[b]), 3 ** b * (1 << Ks[a]))",
     "                right = (Fraction(3 ** b * (1 << Ks[a]), 3 ** a * (1 << Ks[b]))",
     "bank_cost_identity"),
    # D6 originally inverted the comparison and was NOT caught, because the
    # intervals were contiguous and the product telescoped to an EQUALITY --
    # neither direction could fire. The gate now leaves gaps, so the inequality
    # is strict and the inversion is visible. D6b puts the contiguity back and
    # must be caught by the strictness guard rather than by the comparison.
    ("D6_the_telescoping_comparison_is_inverted",
     "            if prod > bound:\n                bad.append((n, stride))",
     "            if prod < bound:\n                bad.append((n, stride))",
     "telescoping"),
    ("D6b_the_intervals_go_back_to_being_contiguous",
     "                i += stride + 1",
     "                i += stride",
     "never strict"),
    ("D7_the_light_infinite_set_is_never_actually_light",
     "        mass = Fraction(1, 2 ** (J * s)) / (1 - Fraction(1, 2 ** s))\n"
     "        results.append({\"s\": s, \"epsilon\": str(eps), \"J\": J,",
     "        mass = Fraction(1, 2 ** s) / (1 - Fraction(1, 2 ** s))\n"
     "        results.append({\"s\": s, \"epsilon\": str(eps), \"J\": J,",
     "mass_no_go"),
    # --- the two routes behind the corrigendum measurement, broken separately ---
    # D8 has been re-aimed twice, and both misses were instructive.
    #
    # Version 1 changed `<` to `<=`, which is a NO-OP: 3^o is odd and 2^k is even,
    # so they are never equal and the two predicates coincide. A mutation that
    # changes nothing is not a defect that survived — it is a defect that was
    # never planted, and the drill reported a miss it had not earned.
    #
    # Version 2 counted two odd steps per odd step. That does not fail — it does
    # not TERMINATE: `3^o < 2^k` becomes `3^k < 2^k`, false forever. It hung the
    # drill mid-run, so the restore never ran and the gate was left on disk with a
    # live defect in it. `GATE_TIMEOUT_SECONDS` above exists because of that.
    #
    # This version offsets the step counter, which the closed-form comparison
    # depends on and which terminates.
    ("D8_the_walked_route_offsets_its_step_counter",
     "    x, k, o = n, 0, 0",
     "    x, k, o = n, 1, 0",
     "corrigendum_gap"),
    ("D9_the_closed_form_route_is_off_by_one",
     "        if k != floor_beta(L) + 1:",
     "        if k != floor_beta(L) + 2:",
     "corrigendum_gap"),
    ("D10_the_upper_bound_loses_its_negative_half",
     "        if any(A[m] > n + Fraction(m, 3) for m in range(len(A))):\n"
     "            upper_ok_after += 1",
     "        if any(A[m] > n + Fraction(m, 3) for m in range(0)):\n"
     "            upper_ok_after += 1",
     "negative half"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]


#: A planted defect can make the gate NOT TERMINATE, and one did: making the
#: walked route count two odd steps per odd step turns `3^o < 2^k` into
#: `3^k < 2^k`, which is never true, so the walk runs forever. Without a timeout
#: the drill itself hangs, the mutation is never restored, and the gate is left
#: on disk with a live defect in it — which is exactly what happened here, twice,
#: before this constant existed. A drill its own mutations can hang is not a
#: drill. The budget is generous against the ~1s the clean gate takes.
GATE_TIMEOUT_SECONDS = 60


def run_gate() -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--limit", LIMIT],
            capture_output=True, text=True, cwd=ROOT,
            timeout=GATE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        # A gate that cannot finish has not passed, and saying so is not the same
        # as saying the named check fired. Reported as its own outcome so that a
        # hang is never quietly counted as a catch.
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
                "note": "the anchor matches %d times, so this defect is aimed at "
                        "nothing; a stale anchor reports a pass it did not earn"
                        % hits}
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
