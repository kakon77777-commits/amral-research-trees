"""Falsifiability drill: break the engine on purpose, confirm the gates notice.

數學戰士「墜衡」 / AMRAL Research Lab.

A passing check is only worth what it would have caught. This script takes the
real engine source, applies one deliberate defect at a time, rebuilds, and runs
the full gate suite against the broken build. Every defect must be caught by at
least one gate; every NULL control (a change that alters no behaviour) must be
caught by none.

A drill run where a defect survives all gates is a finding about the gates, and
is reported as `survived: true` rather than quietly dropped.

Gates
  self-test  the engine's own internal invariants (`--self-test`)
  reference  agreement with collatz_ref.py, an independent bigint Python walk
  anchors    agreement with the archived OEIS record sequences

Usage:  python code/mutation_drill.py
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "code" / "collatz_verify.rs"

REF_LO, REF_HI = 3, 300_000
ANCHOR_BOUND = 1_000_000

# (id, description, old_text, new_text, expected_to_be_caught)
MUTATIONS: list[tuple[str, str, str, str, bool]] = [
    (
        "M01-descent-3x+3",
        "descent iteration computes 3x+3 instead of 3x+1",
        "        x = if x & 1 == 0 { x >> 1 } else { (3 * x + 1) >> 1 };",
        "        x = if x & 1 == 0 { x >> 1 } else { (3 * x + 3) >> 1 };",
        True,
    ),
    (
        "M02-trajectory-halve-twice",
        "standard map halves twice on even values",
        "        x = if x & 1 == 0 { x >> 1 } else { 3 * x + 1 };",
        "        x = if x & 1 == 0 { x >> 2 } else { 3 * x + 1 };",
        True,
    ),
    (
        "M03-descent-not-strict",
        "descent accepts equality instead of strictly below n",
        "    while x >= bound {",
        "    while x > bound {",
        True,
    ),
    (
        "M04-table-shift",
        "k-step table shifts by 2 on odd steps",
        "                x = (3 * x + 1) >> 1;\n                a += 1;",
        "                x = (3 * x + 1) >> 2;\n                a += 1;",
        True,
    ),
    (
        "M05-table-pow2",
        "k-step table stores 2^a instead of 3^a",
        "        pow3[r] = 3u64.pow(a);",
        "        pow3[r] = 2u64.pow(a);",
        True,
    ),
    (
        "M06-guard-disabled",
        "the overflow guard can no longer trip",
        "        if x > VALUE_GUARD {\n            return Err(Failure::ValueGuard { n, at: x });\n        }\n        if steps >= STEP_GUARD {\n            return Err(Failure::StepGuard { n });\n        }\n        x = if x & 1 == 0 { x >> 1 } else { (3 * x + 1) >> 1 };",
        "        if steps >= STEP_GUARD {\n            return Err(Failure::StepGuard { n });\n        }\n        x = if x & 1 == 0 { x >> 1 } else { (3 * x + 1) >> 1 };",
        True,
    ),
    (
        "M07-delay-double-count",
        "standard-map step counter increments by 2",
        "        if x > peak {\n            peak = x;\n        }\n        steps += 1;\n    }\n    Ok((steps, peak))",
        "        if x > peak {\n            peak = x;\n        }\n        steps += 2;\n    }\n    Ok((steps, peak))",
        True,
    ),
    (
        "M08-verify-even-starts",
        "verification walks the even starts, which descend trivially",
        "    let mut n = if lo % 2 == 0 { lo + 1 } else { lo };",
        "    let mut n = if lo % 2 == 0 { lo } else { lo + 1 };",
        True,
    ),
    (
        "M09-skip-half-the-starts",
        "verification steps by 4, silently covering half the odd starts",
        "        n += 2;\n    }\n    Ok(st)",
        "        n += 4;\n    }\n    Ok(st)",
        True,
    ),
    (
        "M10-drop-peak-candidates",
        "record scan stops nominating peak candidates",
        "                                if d > bd || p > bp {",
        "                                if d > bd {",
        True,
    ),
    (
        "NULL-01-comment",
        "control: a comment is added and nothing else",
        "fn full_trajectory(n: u64) -> Result<(u64, u128), Failure> {",
        "// control mutation, no behavioural change\nfn full_trajectory(n: u64) -> Result<(u64, u128), Failure> {",
        False,
    ),
    (
        "NULL-02-chunk-size",
        "control: work is split into 8-wide chunks instead of 2^22-wide, which "
        "reorders how threads interleave and merge but must change nothing reported",
        "    let chunk: u64 = 1 << 22;",
        "    let chunk: u64 = 1 << 3;",
        False,
    ),
]


# A broken map can stop descending altogether, in which case the engine runs to
# its internal step guard on every start and returns no verdict for hours. A
# gate that cannot answer in bounded time has not passed, and the reason is
# recorded distinctly from an ordinary mismatch.
TIMEOUTS = {"self-test": 60, "reference": 90, "anchors": 120}


def run_bounded(cmd: list[str], timeout: int, env: dict | None = None
                ) -> tuple[int | None, str]:
    """Returns (returncode, stdout); returncode is None if it timed out."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout, env=env,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return proc.returncode, proc.stdout


def build(src: pathlib.Path, out: pathlib.Path) -> tuple[bool, str]:
    # rustc derives the crate name from the file stem, so the stem must be a
    # legal identifier. Mutation ids contain characters like '+'.
    proc = subprocess.run(
        ["rustc", "-O", "--edition", "2021", "--crate-name", "collatz_mutant",
         str(src), "-o", str(out)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return proc.returncode == 0, proc.stderr[-800:]


def gate_self_test(binary: pathlib.Path) -> str:
    """Returns 'pass', 'fail', or 'timeout'."""
    rc, out = run_bounded([str(binary), "--self-test"], TIMEOUTS["self-test"])
    if rc is None:
        return "timeout"
    return "pass" if rc == 0 and '"ok":true' in out else "fail"


def gate_reference(binary: pathlib.Path, expected: dict) -> str:
    rc, out = run_bounded(
        [str(binary), "--from", str(REF_LO), "--to", str(REF_HI),
         "--sieve", "20", "--threads", "4"],
        TIMEOUTS["reference"],
    )
    if rc is None:
        return "timeout"
    if rc != 0:
        return "fail"
    try:
        got = json.loads(out)
    except json.JSONDecodeError:
        return "fail"
    return "pass" if all(got.get(k) == v for k, v in expected.items()) else "fail"


def gate_anchors(binary: pathlib.Path) -> str:
    env = dict(os.environ, COLLATZ_BIN=str(binary))
    rc, _ = run_bounded(
        [sys.executable, str(ROOT / "code" / "anchors.py"), str(ANCHOR_BOUND)],
        TIMEOUTS["anchors"], env=env,
    )
    if rc is None:
        return "timeout"
    return "pass" if rc == 0 else "fail"


def main() -> int:
    sys.path.insert(0, str(ROOT / "code"))
    import collatz_ref

    print("computing the Python reference expectation once ...", file=sys.stderr)
    ref = collatz_ref.verify_descent(REF_LO, REF_HI)
    expected = {
        "odd_starts_checked": ref["odd_starts_checked"],
        "max_sigma": ref["max_sigma"],
        "max_sigma_at": ref["max_sigma_at"],
        "max_expansion_peak": ref["max_expansion_peak"],
        "max_expansion_at": ref["max_expansion_at"],
    }

    original = SOURCE.read_text(encoding="utf-8")
    results = []
    # ignore_cleanup_errors: a mutant killed by a gate timeout can still hold a
    # lock on its own .exe for a moment on Windows, and a failure to delete a
    # scratch file must not destroy the report that has already been earned.
    #
    # But "must not crash" is not the same as "may leak". Each run of this drill
    # builds a dozen binaries, so silently abandoning the directory left tens of
    # megabytes per run in the user's Temp. The retry sweep below waits for the
    # killed process to be reaped and then removes the directory properly;
    # ignore_cleanup_errors stays only as the last-resort backstop.
    leaked: str | None = None
    with tempfile.TemporaryDirectory(prefix="collatz-drill-",
                                     ignore_cleanup_errors=True) as tmp:
        tmpdir = pathlib.Path(tmp)

        # Baseline: the unmutated engine must pass every gate, otherwise the
        # whole drill is measuring a broken starting point.
        base_src = tmpdir / "baseline.rs"
        base_src.write_text(original, encoding="utf-8")
        base_bin = tmpdir / "baseline.exe"
        ok, err = build(base_src, base_bin)
        if not ok:
            print(json.dumps({"error": "baseline build failed", "stderr": err}))
            return 2
        baseline = {
            "self-test": gate_self_test(base_bin),
            "reference": gate_reference(base_bin, expected),
            "anchors": gate_anchors(base_bin),
        }
        if any(v != "pass" for v in baseline.values()):
            print(json.dumps({"error": "baseline failed a gate", "gates": baseline}))
            return 2
        print("baseline passes all gates", file=sys.stderr)

        for mid, desc, old, new, should_catch in MUTATIONS:
            occurrences = original.count(old)
            if occurrences != 1:
                results.append({
                    "id": mid, "description": desc,
                    "error": f"anchor text occurs {occurrences} times, expected exactly 1",
                })
                print(f"  {mid}: ANCHOR TEXT NOT UNIQUE", file=sys.stderr)
                continue

            stem = re.sub(r"[^A-Za-z0-9_]", "_", mid)
            src = tmpdir / f"{stem}.rs"
            src.write_text(original.replace(old, new), encoding="utf-8")
            binary = tmpdir / f"{stem}.exe"
            built, err = build(src, binary)
            if not built:
                # A defect the compiler rejects is still a caught defect. A
                # control that fails to compile is a broken control, not a pass.
                results.append({
                    "id": mid, "description": desc,
                    "expected_to_be_caught": should_catch,
                    "caught_by": ["compiler"],
                    "survived": False,
                    "control_disturbed": not should_catch,
                    "compiler_error": err.splitlines()[0] if err else "",
                })
                print(f"  {mid}: rejected by compiler", file=sys.stderr)
                continue

            gates = {
                "self-test": gate_self_test(binary),
                "reference": gate_reference(binary, expected),
                "anchors": gate_anchors(binary),
            }
            caught_by = [
                g if status == "fail" else f"{g} (timeout)"
                for g, status in gates.items() if status != "pass"
            ]
            survived = should_catch and not caught_by
            unexpected = (not should_catch) and bool(caught_by)
            results.append({
                "id": mid, "description": desc,
                "expected_to_be_caught": should_catch,
                "caught_by": caught_by,
                "survived": survived,
                "control_disturbed": unexpected,
            })
            verdict = "SURVIVED" if survived else ("DISTURBED" if unexpected
                                                  else ("caught by " + ",".join(caught_by)
                                                        if caught_by else "clean (control)"))
            print(f"  {mid}: {verdict}", file=sys.stderr)

    # Best-effort second pass at the scratch directory. A mutant killed by a
    # timeout releases its lock once the OS reaps it, which takes well under a
    # second; without this the directory is abandoned with a dozen binaries in it.
    import shutil
    import time

    if tmp and pathlib.Path(tmp).exists():
        for delay in (0.2, 0.5, 1.0, 2.0):
            time.sleep(delay)
            shutil.rmtree(tmp, ignore_errors=True)
            if not pathlib.Path(tmp).exists():
                break
        if pathlib.Path(tmp).exists():
            leaked = tmp

    defects = [r for r in results if r.get("expected_to_be_caught")]
    controls = [r for r in results if r.get("expected_to_be_caught") is False]
    report = {
        "tool": "mutation_drill.py",
        "reference_range": [REF_LO, REF_HI],
        "reference_expectation": expected,
        "anchor_bound": ANCHOR_BOUND,
        "baseline_gates": baseline,
        "mutations": results,
        "defects_planted": len(defects),
        "defects_caught": sum(1 for r in defects if not r.get("survived")),
        "defects_survived": [r["id"] for r in defects if r.get("survived")],
        "controls_planted": len(controls),
        "controls_disturbed": [r["id"] for r in controls if r.get("control_disturbed")],
        "errors": [r["id"] for r in results if "error" in r],
        "scratch_directory_leaked": leaked,
    }
    report["ok"] = (
        not report["defects_survived"]
        and not report["controls_disturbed"]
        and not report["errors"]
    )
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
