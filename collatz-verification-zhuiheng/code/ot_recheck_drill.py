"""Falsifiability drill for ot_paper02_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The recheck passed every theorem of Paper 02. That is only worth something if
the recheck could have failed. Here each asserted formula is perturbed by one
term at a time and the run is required to report the *named* check as failing.

A mutation that leaves every check green means that check is not actually
testing the formula it is named after.

Note the asymmetry: `compose_affine` is the referee, derived from the operator
definitions alone. Perturbing it is expected to break many checks at once,
because everything is compared against it. Perturbing a single claimed formula
is expected to break exactly the check named for that formula.

Usage:  python code/ot_recheck_drill.py
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "code" / "ot_paper02_recheck.py"
DRILL_K = 8

# (id, description, old, new, checks expected to fail)
MUTATIONS = [
    ("D01-thmC-exponent", "Theorem C closed form uses 3^(u-t+1)",
     "return sum(2 ** (jt - 1) * 3 ** (u - t) for t, jt in enumerate(positions, start=1))",
     "return sum(2 ** (jt - 1) * 3 ** (u - t + 1) for t, jt in enumerate(positions, start=1))",
     ["ThmC_closed_form_of_b"]),
    ("D02-thmE-matrix-entry", "Theorem E uses M_U = [[3,2],[0,2]]",
     "    MU = [[3, 1], [0, 2]]",
     "    MU = [[3, 2], [0, 2]]",
     ["ThmE_matrix_representation"]),
    ("D03-thmB-recurrence", "Theorem B recurrence adds 2^k instead of 2^|w|",
     "                expect = bh if last == \"D\" else 3 * bh + 2 ** (k - 1)",
     "                expect = bh if last == \"D\" else 3 * bh + 2 ** k",
     ["ThmB_correction_recurrence"]),
    ("D04-thmD-wrong-power", "Theorem D concatenation uses 2^|v| instead of 2^|w|",
     "                    if b_wv != 3 ** v.count(\"U\") * b_table[w] + 2 ** kw * b_table[v]:",
     "                    if b_wv != 3 ** v.count(\"U\") * b_table[w] + 2 ** kv * b_table[v]:",
     ["ThmD_concatenation_law"]),
    ("D05-thmF-lower-bound", "Theorem F lower bound off by one",
     "            if lo != 3 ** u - 2 ** u or hi != 2 ** (k - u) * (3 ** u - 2 ** u):",
     "            if lo != 3 ** u - 2 ** u + 1 or hi != 2 ** (k - u) * (3 ** u - 2 ** u):",
     ["ThmF_order_extremal_bounds"]),
    ("D06-width-formula", "§25 width drops the -1",
     "            if hi - lo != (2 ** (k - u) - 1) * (3 ** u - 2 ** u):",
     "            if hi - lo != (2 ** (k - u)) * (3 ** u - 2 ** u):",
     ["S25_correction_width_formula"]),
    ("D07-extremes-swapped", "§21 argmin and argmax words swapped",
     "            if b_table[\"U\" * u + \"D\" * (k - u)] != lo:",
     "            if b_table[\"D\" * (k - u) + \"U\" * u] != lo:",
     ["S21_extremes_attained_at_stated_words"]),
    ("D08-residue-sign", "residue formula uses 3^{+u} instead of 3^{-u}",
     "            r = (-b * pow(3, -u, 2 ** k)) % 2 ** k",
     "            r = (-b * pow(3, u, 2 ** k)) % 2 ** k",
     ["P03_residue_cylinder_is_the_admissible_domain"]),
    ("D09-referee-broken", "the referee itself: U injects 2*Dn instead of Dn",
     "            A, B, Dn = 3 * A, 3 * B + Dn, 2 * Dn",
     "            A, B, Dn = 3 * A, 3 * B + 2 * Dn, 2 * Dn",
     ["ThmC_closed_form_of_b", "ThmE_matrix_representation"]),
    ("NULL-01", "control: a comment is added",
     "def closed_form_b(word: str) -> int:",
     "# control mutation, no behavioural change\ndef closed_form_b(word: str) -> int:",
     []),
]


def run(path: pathlib.Path) -> dict | None:
    import os
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, str(path), str(DRILL_K)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=600, env=env,
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    original = SOURCE.read_text(encoding="utf-8")
    results = []
    with tempfile.TemporaryDirectory(prefix="ot-drill-", ignore_cleanup_errors=True) as tmp:
        tmpdir = pathlib.Path(tmp)

        base = tmpdir / "baseline.py"
        base.write_text(original, encoding="utf-8")
        baseline = run(base)
        if baseline is None or not baseline["ok"]:
            print(json.dumps({"error": "baseline did not pass", "baseline": baseline}))
            return 2
        print(f"baseline passes all {len(baseline['checks'])} checks at k={DRILL_K}", file=sys.stderr)

        for mid, desc, old, new, expected in MUTATIONS:
            if original.count(old) != 1:
                results.append({"id": mid, "error": f"anchor occurs {original.count(old)} times"})
                print(f"  {mid}: ANCHOR NOT UNIQUE", file=sys.stderr)
                continue
            path = tmpdir / (re.sub(r"[^A-Za-z0-9_]", "_", mid) + ".py")
            path.write_text(original.replace(old, new), encoding="utf-8")
            out = run(path)
            if out is None:
                failed_checks = ["<crashed>"]
            else:
                failed_checks = [n for n, c in out["checks"].items() if not c["pass"]]

            if expected:
                caught = all(e in failed_checks for e in expected)
                verdict = "caught" if caught else "SURVIVED / WRONG CHECK"
            else:
                caught = not failed_checks
                verdict = "clean (control)" if caught else "CONTROL DISTURBED"

            results.append({
                "id": mid, "description": desc,
                "expected_failing_checks": expected,
                "observed_failing_checks": failed_checks,
                "as_expected": caught,
            })
            print(f"  {mid}: {verdict}  -> {failed_checks}", file=sys.stderr)

    # Defects and controls are counted separately. A single "as_expected" tally
    # across both makes the summary read as though more defects passed than were
    # planted.
    defects = [r for r in results if r.get("expected_failing_checks")]
    controls = [r for r in results if "expected_failing_checks" in r
                and not r["expected_failing_checks"]]
    report = {
        "tool": "ot_recheck_drill.py",
        "target": "code/ot_paper02_recheck.py",
        "drill_word_length": DRILL_K,
        "mutations": results,
        "defects_planted": len(defects),
        "defects_caught_by_the_named_check": len([r for r in defects if r["as_expected"]]),
        "controls_planted": len(controls),
        "controls_undisturbed": len([r for r in controls if r["as_expected"]]),
        "anomalies": [r["id"] for r in results if not r.get("as_expected", False)],
    }
    report["ok"] = not report["anomalies"] and not any("error" in r for r in results)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
