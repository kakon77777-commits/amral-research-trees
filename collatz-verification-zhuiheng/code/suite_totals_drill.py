"""Drill for suite_totals.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The figure this script emits is quoted in the README and the charter, so the
question is not "does it add up" but "can it be wrong and still look right".
Its one real failure mode is silent undercounting: a drill log whose schema it
does not recognise contributes zero and the total stays plausible. That is not a
hypothetical — the first version of the script read only the `counts` shape and
reported 383 where the logs held 461, losing two whole drills without a murmur.

So the defects here are planted in the **logs**, not the script, because the logs
are what varies. Each must make the script exit non-zero.

A defect counts as caught only if `ok` goes false for the reason named.

Usage:  python code/suite_totals_drill.py
"""

from __future__ import annotations

import io
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE = ROOT / "code"
TOOL = CODE / "suite_totals.py"
LOGS = ROOT / "data" / "gate-logs"


def main() -> int:
    rep = {"tool": "suite_totals_drill.py",
           "subject": "code/suite_totals.py and the drill logs it reads",
           "defects": {}, "controls": {}}

    original = TOOL.read_text(encoding="utf-8")

    def run(logdir: pathlib.Path, tool: pathlib.Path) -> dict:
        src = tool.read_text(encoding="utf-8").replace(
            'LOGS = ROOT / "data" / "gate-logs"', f'LOGS = pathlib.Path(r"{logdir}")')
        f = CODE / "_st_mutant.py"
        try:
            f.write_text(src, encoding="utf-8")
            out = subprocess.run([sys.executable, str(f)], capture_output=True,
                                 text=True, encoding="utf-8", timeout=300,
                                 env={**__import__("os").environ, "PYTHONUTF8": "1"})
            try:
                return json.loads(out.stdout)
            except json.JSONDecodeError:
                return {"ok": False, "_crash": (out.stdout + out.stderr)[-300:]}
        finally:
            f.unlink(missing_ok=True)

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)

        def fresh(name: str) -> pathlib.Path:
            d = tmp / name
            shutil.copytree(LOGS, d)
            return d

        base = fresh("base")
        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline not green; drill is meaningless",
                              "baseline": baseline}, indent=2, ensure_ascii=False))
            return 2
        rep["baseline"] = {
            "drills": baseline["drills"],
            "defects_planted": baseline["defects_planted"],
            "controls": baseline["controls"]}

        def record(name, res, why, expect_key=None):
            hit = not res.get("ok")
            if expect_key:
                hit = hit and bool(res.get(expect_key))
            rep["defects"][name] = {"why": why, "caught": hit,
                                    "uninterpreted": res.get("uninterpreted"),
                                    "drills": res.get("drills"),
                                    "planted": res.get("defects_planted")}

        # D1 — a drill log in a shape the script does not know. This is the
        # undercount that actually happened, and it must not pass silently.
        d = fresh("unknown_shape")
        (d / "src99-drill.json").write_text(json.dumps(
            {"tool": "src99_drill.py", "ok": True,
             "tally": {"planted_defect_count": 12, "caught": 12}}),
            encoding="utf-8")
        record("D1_a_drill_log_in_an_unrecognised_shape", run(d, TOOL),
               "must land in `uninterpreted`, not contribute zero",
               expect_key="uninterpreted")

        # D2 — a drill that did not catch everything it planted
        d = fresh("survivor")
        p = d / "src21-drill.json"
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["counts"]["defects_caught_by_the_named_check"] -= 1
        p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        record("D2_a_planted_defect_survived", run(d, TOOL),
               "planted != caught must refuse")

        # D3 — a disturbed null control, in the list-shaped log
        d = fresh("control")
        p = d / "mutation-drill.json"
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["controls_disturbed"] = ["N01"]
        p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        record("D3_a_null_control_was_disturbed_in_the_list_shaped_log",
               run(d, TOOL), "the second control shape must be read, not ignored")

        # D4 — a drill log that is itself red
        d = fresh("red")
        p = d / "src20-drill.json"
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["ok"] = False
        p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        record("D4_a_drill_log_reports_itself_red", run(d, TOOL),
               "a red drill must not be totalled into a green summary")

        # D5 — the script stops reading the second tally shape. The total must
        # move, which is the whole point; a reader that cannot tell would have
        # published 383 for 461.
        anchor = '    for src in (doc.get("counts", {}), doc):'
        if anchor not in original:
            raise SystemExit(f"D5 anchor absent: {anchor!r}")
        f = CODE / "_st_narrow.py"
        try:
            f.write_text(
                original.replace(anchor, '    for src in (doc.get("counts", {}),):'),
                encoding="utf-8")
            res = run(base, f)
        finally:
            f.unlink(missing_ok=True)
        moved = res.get("defects_planted") != baseline["defects_planted"]
        rep["defects"]["D5_the_second_tally_shape_is_no_longer_read"] = {
            "why": "dropping a shape must change the total AND be refused",
            "caught": (not res.get("ok")) and moved,
            "planted": res.get("defects_planted"),
            "baseline_planted": baseline["defects_planted"],
            "uninterpreted": res.get("uninterpreted")}

        # D6 — a half-written log. This one is not hypothetical: a shell redirect
        # creates its target empty before the producing process writes anything,
        # so running this drill with `> gate-logs/suite-totals-drill.json` fed the
        # script a zero-byte file. It crashed instead of refusing.
        d = fresh("truncated")
        (d / "src18-drill.json").write_text("", encoding="utf-8")
        record("D6_a_half_written_log_is_refused_not_crashed_on", run(d, TOOL),
               "an empty file must land in `uninterpreted`",
               expect_key="uninterpreted")

        # N1 — an unrelated file beside the logs
        d = fresh("null")
        (d / "notes.txt").write_text("read by nothing\n", encoding="utf-8")
        res = run(d, TOOL)
        rep["controls"]["N01_unrelated_file_beside_the_logs"] = {
            "undisturbed": bool(res.get("ok"))
            and res.get("defects_planted") == baseline["defects_planted"]}

        # N2 — a NON-drill log added; it must not be picked up at all
        d = fresh("null2")
        (d / "src99-au9z-recheck.json").write_text(json.dumps(
            {"tool": "x", "ok": True, "counts": {"defects_planted": 999,
                                                 "defects_caught_by_the_named_check": 0}}),
            encoding="utf-8")
        res = run(d, TOOL)
        rep["controls"]["N02_a_recheck_log_is_not_mistaken_for_a_drill"] = {
            "undisturbed": bool(res.get("ok"))
            and res.get("defects_planted") == baseline["defects_planted"]}

    caught = sum(1 for v in rep["defects"].values() if v["caught"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {"defects_planted": len(rep["defects"]),
                     "defects_caught_by_the_named_check": caught,
                     "controls": len(rep["controls"]),
                     "controls_undisturbed": quiet}
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
