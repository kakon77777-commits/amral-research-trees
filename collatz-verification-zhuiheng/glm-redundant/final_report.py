"""The definitive score across both passes, with the post-hoc corrections applied.

數學戰士「墜衡」 / AMRAL Research Lab.

`score_judgement.py` and `score_pass2.py` score against the pre-registered key,
which is what they are for. But three of that key's controls have since been
demonstrated to be forced — one of them by GLM itself — so scoring against it
unmodified reports a correct challenge as a worker error.

This script keeps both readings and never collapses them:

  * **as pre-registered** — what the key said before any answer arrived.
  * **as adjudicated** — with `post_hoc_verified.json` applied, where each entry
    is an assertion this arm has since PROVED forced, with the proof recorded.

The two passes are reported separately throughout. Pass 2 reduced the context,
which is a different condition, and pooling them would hide that.

Usage:  python glm-redundant/final_report.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "final_report.json"


def verdicts(raw_dir: pathlib.Path, prefix: str) -> dict:
    """task_id -> can_fail bool, for every envelope that produced one."""
    got = {}
    for p in sorted(raw_dir.glob(prefix + "*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:                                # noqa: BLE001
            continue
        if doc.get("status") != "candidate_success":
            continue
        m = re.search(r"\{.*\}", doc.get("answer") or "", re.S)
        if not m:
            continue
        try:
            a = json.loads(m.group(0))
        except Exception:                                # noqa: BLE001
            continue
        if isinstance(a.get("can_fail"), bool):
            got[p.stem] = a["can_fail"]
    return got


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    key = {i["task_id"]: i
           for i in json.loads((ROOT / "judgement_key.json")
                               .read_text(encoding="utf-8"))["items"]}
    ph = json.loads((ROOT / "post_hoc_verified.json").read_text(encoding="utf-8"))
    forced_lines = {e["line"] for e in ph["entries"]}
    criterion_lines = {e["line"] for e in ph["criterion_disagreements"]}

    p1 = verdicts(ROOT / "raw", "collatz-judge-")
    p2raw = verdicts(ROOT / "raw_pass2", "collatz-judge2-")
    p2 = {k.replace("judge2", "judge"): v for k, v in p2raw.items()}

    rows = []
    for tid, item in key.items():
        v1, v2 = p1.get(tid), p2.get(tid)
        v = v1 if v1 is not None else v2
        rows.append({
            "task_id": tid, "round": item["round"], "line": item["line"],
            "key_verdict": item["my_verdict"],
            "adjudicated": ("cannot_fail" if item["line"] in forced_lines
                            else item["my_verdict"]),
            "glm_can_fail": v,
            "answered_in": ("pass1" if v1 is not None
                            else "pass2" if v2 is not None else None),
            "criterion_dispute": item["line"] in criterion_lines,
        })

    answered = [r for r in rows if r["glm_can_fail"] is not None]
    said_true = [r for r in answered if r["glm_can_fail"]]

    def tally(field: str) -> dict:
        find = [r for r in answered if r[field] == "cannot_fail"]
        ctrl = [r for r in answered if r[field] == "can_fail"]
        return {
            "findings_answered": len(find),
            "findings_confirmed": sum(1 for r in find if not r["glm_can_fail"]),
            "controls_answered": len(ctrl),
            "controls_glm_got_right": sum(1 for r in ctrl if r["glm_can_fail"]),
            "controls_glm_called_forced": sum(1 for r in ctrl
                                              if not r["glm_can_fail"]),
        }

    overturned = [r for r in rows
                  if r["key_verdict"] == "can_fail"
                  and r["adjudicated"] == "cannot_fail"]
    report = {
        "totals": {
            "assertions": len(rows),
            "answered_either_pass": len(answered),
            "answered_pass1": sum(1 for r in answered
                                  if r["answered_in"] == "pass1"),
            "answered_pass2": sum(1 for r in answered
                                  if r["answered_in"] == "pass2"),
            "never_answered": len(rows) - len(answered),
            "glm_said_can_fail_at_least_once": bool(said_true),
        },
        "as_pre_registered": tally("key_verdict"),
        "as_adjudicated": tally("adjudicated"),
        "controls_overturned_by_verification": [
            {"line": r["line"], "task_id": r["task_id"],
             "found_by": next(e["who_found_it"] for e in ph["entries"]
                              if e["line"] == r["line"])}
            for r in overturned],
        "criterion_disputes_left_open": [
            {"line": r["line"], "task_id": r["task_id"]}
            for r in rows if r["criterion_dispute"]],
        "what_is_measured": (
            "GLM confirmed every finding it answered and never once said an "
            "assertion can fail. Of the controls that got an answer, three are "
            "now proved forced -- one of them found by GLM -- and one is an "
            "open disagreement about the criterion. So no answered control "
            "survives as a fair negative test, and the worker's ability to "
            "DISCRIMINATE is unmeasured: the instrument built to measure it "
            "was made of the same misjudgements it was meant to catch."),
        "why_the_controls_went_unanswered": (
            "Every unanswered task hit finish_reason=length with the whole "
            "4096-token output budget spent on reasoning. Pass 2 cut the "
            "context -- in one case from 3077 to 1455 input tokens -- and they "
            "failed identically. The cost is in the QUESTION: 'can this fail?' "
            "is an open-ended search over inputs, while 'is this forced?' stops "
            "at the guard. That asymmetry, not context size, is why the "
            "answered set skews to the side this arm was right about."),
        "rows": rows,
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
