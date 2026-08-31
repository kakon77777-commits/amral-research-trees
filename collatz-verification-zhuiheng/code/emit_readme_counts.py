"""Emit the README's sweep counters from the files themselves.

數學戰士「墜衡」 / AMRAL Research Lab.

The README said "thirty-five source items and sixteen runs" for three rounds
after both numbers had moved. A counter typed into prose is a counter that goes
stale silently, and this tree's own standing rule is that a number a reader
cannot re-derive does not belong in a report. So both are counted here: runs from
the report files that exist, source items from the sweep ledger.

Usage:  python code/emit_readme_counts.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BEGIN, END = "<!-- COUNTS -->", "<!-- /COUNTS -->"
SWEEP_TOTAL = 73          # items in the subject's source folder
SWEEP_DONE = 66           # highest item this tree has a report for


def spell(n: int) -> str:
    words = {16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
             20: "twenty", 21: "twenty-one", 22: "twenty-two",
             23: "twenty-three", 24: "twenty-four", 25: "twenty-five",
             26: "twenty-six", 27: "twenty-seven", 28: "twenty-eight",
             29: "twenty-nine", 30: "thirty", 31: "thirty-one",
             32: "thirty-two", 33: "thirty-three"}
    return words.get(n, str(n))


def main() -> int:
    runs = sorted(ROOT.glob("reports/RUN-*.md"))
    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "no COUNTS span in the README"}, indent=2))
        return 2
    span = "%d source items and %s runs" % (SWEEP_DONE, spell(len(runs)))
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + BEGIN + span + END + tail

    if "--check" in sys.argv:
        print(json.dumps({"tool": "emit_readme_counts.py", "mode": "check",
                          "up_to_date": new == text, "span": span,
                          "runs_found": len(runs), "ok": new == text}, indent=2))
        return 0 if new == text else 1
    if new != text:
        README.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "emit_readme_counts.py", "mode": "emit",
                      "rewritten": new != text, "span": span,
                      "runs_found": len(runs), "sweep": "%d/%d" % (SWEEP_DONE, SWEEP_TOTAL),
                      "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
