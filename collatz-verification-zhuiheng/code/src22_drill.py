"""Can the item-40 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`src22_au2e1_reset_block.py` reports that every checkable claim in Round A-U.2e.1
holds. A run that confirms everything is exactly the run to distrust, because a
comparison that agrees is indistinguishable from a comparison that cannot
disagree. So each check is broken in turn and the recheck must go red **for the
reason named**.

Mutations are byte-level, restored under `try/finally`, and verified byte-equal
afterwards.

Usage:  python code/src22_drill.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
GATE = HERE / "code" / "src22_au2e1_reset_block.py"

# (name, old, new, substring that must appear in a reported problem)
DEFECTS = [
    ("D1_the_anchor_increment_gets_the_wrong_exponent",
     "if inc != Fraction(2 ** K_m, 3 ** (m + 1)):",
     "if inc != Fraction(2 ** K_m, 3 ** (m + 2)):",
     "renormalized anchor identity fails"),
    # D2 originally deleted a per-step comparison and was NOT caught, because that
    # comparison was implied by the increment check plus the telescoping check.
    # The redundant check has been removed from the gate; this defect now breaks
    # the one fact the surviving checks uniquely rest on, the anchor base A_0 = n.
    ("D2_the_anchor_base_is_wrong",
     "        out.append(Fraction(2 ** K * ys[m], 3 ** m))",
     "        out.append(Fraction(2 ** K * ys[m] + (1 if m == 0 else 0), 3 ** m))",
     "renormalized anchor identity fails"),
    ("D3_the_mod8_bridge_admits_a_wrong_residue",
     "    bridge_ok = (residues[5] == [3]\n"
     "                 and all(3 not in residues[r] for r in (1, 3, 7)))",
     "    residues[1] = [3]\n"
     "    bridge_ok = (residues[5] == [3]\n"
     "                 and all(3 not in residues[r] for r in (1, 3, 7)))",
     "mod-8 bridge"),
    ("D4_the_survival_comparison_is_inverted",
     'if Decimal(ratio.numerator) / Decimal(ratio.denominator) >= bound_route:\n'
     '                surv_route["violations"] += 1',
     'if Decimal(ratio.numerator) / Decimal(ratio.denominator) < bound_route:\n'
     '                surv_route["violations"] += 1',
     "relative-survival"),
    ("D5_the_depth_duration_comparison_is_inverted",
     "if Decimal(L) < D_route / (Decimal(R) - BETA):",
     "if Decimal(L) >= D_route / (Decimal(R) - BETA):",
     "depth-duration bound violated"),
    ("D6_the_packing_comparison_is_inverted",
     "if Decimal(lhs.numerator) / Decimal(lhs.denominator) >= rhs:",
     "if Decimal(lhs.numerator) / Decimal(lhs.denominator) < rhs:",
     "packing bound is violated"),
    ("D7_the_worked_example_arithmetic_is_wrong",
     "margin = EXAMPLE_RHO - Fraction(1, 2 ** EXAMPLE_D)",
     "margin = EXAMPLE_RHO - Fraction(1, 2 ** (EXAMPLE_D + 1))",
     "worked example does not recompute"),
    ("D8_delta_is_transcribed_wrongly",
     "        out.append(m * beta - K)",
     "        out.append(m * beta - 2 * K)",
     "transcription of delta is wrong"),
    ("D9_the_packing_hypothesis_is_violated_silently",
     "    D0, RHO = 3, Fraction(1, 4)",
     "    D0, RHO = 2, Fraction(1, 4)",
     "violate the theorem's own hypothesis"),
]


def run_gate() -> dict:
    p = subprocess.run([sys.executable, str(GATE)], cwd=str(HERE),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=3600)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"ok": None, "problems": ["gate produced no JSON"],
                "tail": (p.stdout + p.stderr)[-600:]}


def main() -> int:
    rep = {"tool": "src22_drill.py", "subject": GATE.name,
           "defects": {}, "controls": {}}

    base = run_gate()
    if not base.get("ok"):
        print(json.dumps({"error": "baseline recheck is not green; refusing to "
                                   "drill from a red baseline",
                          "problems": base.get("problems")},
                         indent=2, ensure_ascii=False))
        return 2
    rep["baseline"] = {"reset_blocks": base["orbits"]["reset_blocks_found"]}

    snapshot = GATE.read_bytes()
    for name, old, new, expect in DEFECTS:
        raw = GATE.read_bytes()
        text = raw.decode("utf-8")
        if text.count(old) != 1:
            rep["defects"][name] = {
                "caught": False,
                "note": "anchor matched %d times" % text.count(old)}
            continue
        try:
            GATE.write_bytes(text.replace(old, new, 1).encode("utf-8"))
            res = run_gate()
        finally:
            GATE.write_bytes(raw)
        if GATE.read_bytes() != raw:
            rep["defects"][name] = {"caught": False,
                                    "note": "gate not restored byte-exactly"}
            continue
        problems = " | ".join(res.get("problems", []))
        rep["defects"][name] = {
            "caught": (not res.get("ok")) and expect in problems,
            "expected_substring": expect,
            "reported": res.get("problems", [])[:3]}

    raw = GATE.read_bytes()
    try:
        GATE.write_bytes(raw + b"\n# a comment nothing reads\n")
        res = run_gate()
    finally:
        GATE.write_bytes(raw)
    rep["controls"]["N1_a_comment_is_not_a_problem"] = {
        "undisturbed": bool(res.get("ok")) and GATE.read_bytes() == raw}
    rep["controls"]["N2_the_gate_is_restored_byte_exactly"] = {
        "undisturbed": GATE.read_bytes() == snapshot}

    caught = sum(1 for v in rep["defects"].values() if v["caught"])
    rep["counts"] = {"defects_planted": len(DEFECTS), "caught": caught,
                     "controls": len(rep["controls"]),
                     "controls_undisturbed":
                         sum(1 for c in rep["controls"].values()
                             if c["undisturbed"])}
    rep["ok"] = (caught == len(DEFECTS)
                 and all(c["undisturbed"] for c in rep["controls"].values()))
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
