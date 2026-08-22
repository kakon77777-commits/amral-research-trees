"""Can the item-43 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src43_renewal_rigidity.py` reports that A-U.2e.4's arithmetic holds and that one
inference in section 5 does not follow from its own premise. The second of those
is a claim ABOUT the round, so it had better be the case that this arm's checks
could have said otherwise.

Each check is broken in turn and the recheck must go red **for the reason named
for it**. A defect caught only by some other check is a miss.

Three of these guard non-vacuity rather than correctness, because this round's
checks are unusually easy to make hollow:

  D11 empties the determinant sample of unlocked pairs, so `Delta >= 1` would be
  tested only where it is automatic.
  D12 removes the negative half of the Farey-lock check.
  D13 empties every scale-separation hypothesis, which must be caught by the
  "no c inhabited" guard rather than by a violation count.

`GATE_TIMEOUT_SECONDS` is here from the start: on item 42 a planted defect made
the gate loop forever, which hung the drill so its restore never ran and left a
live defect in the gate on disk. Twice.

Usage:  python code/src43_drill.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src43_renewal_rigidity.py"
MAX_Q = "20000"
GATE_TIMEOUT_SECONDS = 120

DEFECTS = [
    # D1 first mutated the REPORTED STRING rather than the comparison, so the
    # verdict never moved. Aimed at `agrees` now, which is what feeds the result.
    ("D1_the_rho_closed_form_is_wrong",
     "        \"agrees\": (1 + root) / (2 * c) == 2,",
     "        \"agrees\": (1 - root) / (2 * c) == 2,",
     "rho_constants"),
    # D2 first replaced the test with `inside == inside`, which is a NO-OP: both
    # spellings evaluate True on the real value, so nothing moved. That miss did
    # find something real, though — the field was decorative, read by no verdict.
    # It is wired into `both_exact` now, and this defect makes it FALSE, which is
    # what demonstrates the wiring.
    ("D2_the_perfect_square_test_is_wrong",
     "        \"is_a_perfect_rational_square\": inside == root * root,",
     "        \"is_a_perfect_rational_square\": inside == root * root * 2,",
     "rho_constants"),
    ("D3_the_determinant_identity_is_transcribed_backwards",
     "            if pp * qm - pm * qp != qm * dp + qp * dm:",
     "            if pp * qm - pm * qp != qm * dm + qp * dp:",
     "determinant identity"),
    ("D4_the_lower_error_has_the_wrong_sign",
     "            dm = b * qm - pm",
     "            dm = pm - b * qm",
     "determinant identity"),
    ("D5_the_determinant_positivity_test_is_inverted",
     "            if delta < 1:",
     "            if delta > 1:",
     "determinant positive"),
    ("D6_the_cross_error_threshold_uses_the_wrong_denominator",
     "            threshold = Fraction(1, qm + qp)",
     "            threshold = Fraction(1, qm * qp)",
     "cross_error_barrier"),
    # D7 first weakened the threshold, which was invisible: on a Farey pair the
    # cheapest interior denominator always EQUALS q- + q+, so lowering the bar
    # moves no verdict. **To test a check that never fires, break its SUBJECT,
    # not its comparison.** This makes the interior search accept an endpoint,
    # which returns a denominator below the bound and the check must notice.
    ("D7_the_interior_search_accepts_an_endpoint",
     "            if r * h[1] < h[0] * s and r * l[1] > l[0] * s:",
     "            if r * h[1] <= h[0] * s and r * l[1] >= l[0] * s:",
     "farey_lock"),
    # D8 first loosened `1/q_next` to `1/1`, which no convergent error could ever
    # exceed — same class as D7. This uses the CURRENT denominator where the tax
    # uses the NEXT one, which is the whole substance of section 7.
    ("D8_the_cf_tax_uses_the_current_denominator_not_the_next",
     "        q_next = conv[i + 1][1]",
     "        q_next = conv[i][1]",
     "cf_tax"),
    ("D9_the_recycling_monotonicity_comparison_is_inverted",
     "            if prev is not None and val >= prev:",
     "            if prev is not None and val <= prev:",
     "recycling_no_go"),
    # D10 first disabled the premise check itself, which was invisible because
    # that check reports ZERO: turning `x != y` into `x != x` removes nothing when
    # nothing was being removed. Section 5's premise is about the MEDIANT
    # construction, so this breaks that, and the premise check must then fire.
    ("D10_the_descent_stops_taking_true_mediants",
     "        m = (lo[0] + hi[0], lo[1] + hi[1])\n        went_low = below_beta(*m)",
     "        m = (lo[0] + hi[0], lo[1] + hi[1] + 1)\n        went_low = below_beta(*m)",
     "section_5: the premise itself failed"),
    # --- non-vacuity guards ---
    ("D11_the_determinant_sample_keeps_only_locked_pairs",
     "            delta = pp * qm - pm * qp\n            if delta < 1:",
     "            delta = 1\n            if delta < 1:",
     "not discriminating"),
    ("D12_the_farey_negative_half_is_emptied",
     "            if d <= 1 or not below_beta(*l) or below_beta(*h):",
     "            if d <= 10 ** 9 or not below_beta(*l) or below_beta(*h):",
     "only the easy side"),
    ("D13_every_scale_separation_hypothesis_is_emptied",
     "            if dm_hi > c / qm:",
     "            if dm_hi > c / (qm * 10 ** 9):",
     "passed vacuously"),
    ("D14_the_barrier_is_never_approached",
     "                if best_lo < threshold * 2:\n                    tight += 1",
     "                if best_lo < threshold * 0:\n                    tight += 1",
     "not exercised"),
]

CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]


def run_gate() -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, str(GATE), "--max-q", MAX_Q],
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
