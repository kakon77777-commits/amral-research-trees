"""Can the item-41 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src41_first_crossing_survival.py` reports that every checkable claim in Round
A-U.2e.2 holds. A run that confirms everything is exactly the run to distrust,
because a comparison that agrees is indistinguishable from a comparison that
cannot disagree — and this round is unusually exposed to that, since its most
striking claims are conditional on a set the run measures to be EMPTY.

So each check is broken in turn, and the recheck must go red **for the reason
named for it**. A defect caught by some other check is recorded as a miss: it
means the named check is not aimed at what it claims to cover.

Two defects (D9, D10) exist specifically because the empty-set problem bit once
already: the cap-equivalence check on real orbits compares False against False
for every start, so it passes no matter what the cap computes. Its true branch
lives in the synthetic configurations, and D9/D10 break each side of that branch
separately, because breaking only one would leave a rule that always answers the
same way looking correct.

Mutations are byte-level, restored under `try/finally`, and verified byte-equal
afterwards.

Usage:  python code/src41_drill.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE = ROOT / "code" / "src41_first_crossing_survival.py"
LIMIT = "6001"          # small: the drill runs the gate a dozen times

# (name, old, new, the failure string that must be reported)
DEFECTS = [
    ("D1_the_correction_bound_comparison_is_inverted",
     "        if B > limit:\n            bad.append(n)",
     "        if B <= limit:\n            bad.append(n)",
     "correction_bound"),
    ("D2_the_correction_bound_uses_the_wrong_power",
     "        limit = L * (p3 // 3)",
     "        limit = L * (p3 // 9)",
     "correction_bound"),
    ("D3_the_reset_inequality_drops_the_duration_term",
     "        rhs = p3 * (3 * n + L)",
     "        rhs = p3 * (3 * n)",
     "reset_inequality"),
    ("D4_the_reset_inequality_comparison_is_inverted",
     "        if lhs > rhs:\n            bad.append(n)",
     "        if lhs <= rhs:\n            bad.append(n)",
     "reset_inequality"),
    # D5 originally expected `cap_equivalence` and was NOT caught: on real orbits
    # that check compares False against False at every start, so the cap's
    # denominator could be anything at all and the run stayed green. The gate now
    # probes each real crossing's cap from both sides in `cap_threshold`, and that
    # is the check this defect is aimed at.
    ("D5_the_cap_denominator_is_wrong",
     "        denom = (1 << Q) - p3",
     "        denom = (1 << Q) + p3",
     "cap_threshold"),
    ("D5b_the_cap_threshold_probes_only_one_side",
     "        z = y_star + 1\n"
     "        if not (p3 * z + B) < z * (1 << Q):",
     "        z = y_star\n"
     "        if not (p3 * z + B) < z * (1 << Q):",
     "cap_threshold"),
    ("D5c_the_reset_slack_identity_loses_its_factor_of_three",
     "        if rhs - lhs != 3 * (L * (p3 // 3) - B):",
     "        if rhs - lhs != (L * (p3 // 3) - B):",
     "reset_inequality"),
    ("D6_the_constant_is_recomputed_from_the_wrong_expression",
     "    val_lo = (Decimal(3) * lo / 2).sqrt()",
     "    val_lo = (Decimal(2) * lo / 3).sqrt()",
     "constant"),
    ("D7_the_approximation_set_admits_every_fraction",
     "        out.add(Fraction(*m))",
     "        out.add(Fraction(*m))\n        out.add(Fraction(17, 11))",
     "approximation set accepts a non-member"),
    ("D8_the_approximation_descent_goes_the_wrong_way",
     "        lo, hi = (m, hi) if below_beta(*m) else (lo, m)\n\n\ndef beta_bounds",
     "        lo, hi = (lo, m) if below_beta(*m) else (m, hi)\n\n\ndef beta_bounds",
     "approximation set misses a classical convergent"),
    # --- the two halves of the branch that real orbits cannot exercise ---
    ("D9_at_or_below_the_cap_is_allowed_to_descend",
     "        if not (p3 * y + B) >= y * (1 << Q):\n            below_fail.append((y, L, Q))",
     "        if not (p3 * y + B) > y * (1 << Q) * 2:\n            below_fail.append((y, L, Q))",
     "cap_equivalence_branches"),
    ("D10_just_above_the_cap_is_allowed_not_to_descend",
     "        if not (p3 * z + B) < z * (1 << Q):\n            above_fail.append((z, L, Q))",
     "        if not (p3 * z + B) < z * (1 << Q) // 2:\n            above_fail.append((z, L, Q))",
     "cap_equivalence_branches"),
    ("D11_the_survival_cost_loses_its_factor_of_three",
     "        if not 3 * ((1 << Q) - p3) * y <= L * p3:",
     "        if not 9 * ((1 << Q) - p3) * y <= L * p3:",
     "survival_cost"),
    ("D12_the_log_form_of_the_survival_cost_is_wrong",
     "        if not 3 * y * (1 << Q) <= p3 * (3 * y + L):",
     "        if not 3 * y * (1 << Q) <= p3 * (3 * y):",
     "survival_cost"),
    ("D13_the_duration_branch_is_evaluated_against_the_wrong_threshold",
     "        duration = 2 * L * L >= 3 * LN2_HI * y",
     "        duration = L >= 3 * LN2_HI * y",
     "legendre_gate"),
    ("D14_the_clustering_control_is_the_sample_itself",
     "    bottom_ids = {r[1] for r in ordered[-1000:]}",
     "    bottom_ids = {r[1] for r in ordered[:1000]}",
     "clustering control overlaps the sample it controls for"),
]

# Defects that must NOT change the verdict.
CONTROLS = [
    ("N1_a_trailing_comment_is_not_a_defect", b"\n# a comment nothing reads\n"),
]


def run_gate() -> dict:
    proc = subprocess.run(
        [sys.executable, str(GATE), "--limit", LIMIT],
        capture_output=True, text=True, cwd=ROOT,
    )
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
        "defects": {},
        "controls": {},
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
                "note": "the anchor matches %d times, so this defect is not aimed "
                        "at anything; a drill with a stale anchor reports a pass "
                        "it did not earn" % hits}
            continue
        try:
            GATE.write_text(text.replace(old, new), encoding="utf-8")
            res = run_gate()
        finally:
            GATE.write_text(text, encoding="utf-8")
        failures = res.get("failures", [])
        by_its_own_check = any(expected in f for f in failures)
        report["defects"][name] = {
            "caught": by_its_own_check,
            "expected_failure_named": expected,
            "reported": failures[:4],
            "caught_by_something_else_only":
                bool(failures) and not by_its_own_check,
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
        "controls_undisturbed": sum(1 for c in report["controls"].values()
                                    if c["undisturbed"]),
        "controls": len(report["controls"]),
    }
    report["ok"] = (caught == len(DEFECTS)
                    and all(c["undisturbed"] for c in report["controls"].values()))
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
