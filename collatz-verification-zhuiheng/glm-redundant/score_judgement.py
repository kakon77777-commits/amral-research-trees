"""Score GLM's per-assertion judgements against this arm's own verdicts.

數學戰士「墜衡」 / AMRAL Research Lab.

Each task showed GLM one assertion from a bundle's own checker, with the whole
script as context, and asked a single question: can this assertion ever fail?
GLM saw no verdict of mine, and the 28 assertions were shuffled, so nothing in
the order says which is which.

**Eleven of them are controls** -- assertions this arm judges CAN fail, because
their truth depends on the paper's mathematics rather than on the code around
them. They are the reason this is a measurement and not a chorus: a worker that
answers "cannot fail" to everything agrees with all seventeen of my findings and
is worth nothing, and the controls are what makes that visible.

Reported four ways:

  * **confirmed**     -- I say cannot-fail, GLM says cannot-fail.
  * **control_held**  -- I say can-fail, GLM says can-fail. The negative control.
  * **glm_disputes**  -- I say cannot-fail, GLM says it can. Each one is a
    challenge to a published finding and gets re-derived by hand.
  * **glm_overcalls** -- I say can-fail, GLM says it cannot. Either a miss of
    mine or a false positive of GLM's; either way I verify before crediting.

Usage:  python glm-redundant/score_judgement.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "raw"
KEY = ROOT / "judgement_key.json"
OUT = ROOT / "judgement_result.json"


def extract(doc: dict):
    """GLM's verdict, or a reason it produced none."""
    if doc.get("status") != "candidate_success":
        meta = doc.get("provider_meta", {}) or {}
        return None, {"status": doc.get("status"),
                      "finish_reason": meta.get("finish_reason"),
                      "warnings": (doc.get("warnings") or [])[:1]}
    answer = (doc.get("answer") or "").strip()
    if not answer:
        return None, {"status": "empty answer"}
    m = re.search(r"\{.*\}", answer, re.S)
    if not m:
        return None, {"status": "no JSON object", "head": answer[:120]}
    try:
        parsed = json.loads(m.group(0))
    except Exception:                                    # noqa: BLE001
        return None, {"status": "unparsable JSON", "head": answer[:120]}
    if not isinstance(parsed.get("can_fail"), bool):
        return None, {"status": "no boolean can_fail", "head": answer[:120]}
    return ({"can_fail": parsed["can_fail"],
             "why": str(parsed.get("why") or "")[:240]}, None)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    key = json.loads(KEY.read_text(encoding="utf-8"))["items"]
    buckets: dict = {"confirmed": [], "control_held": [],
                     "glm_disputes": [], "glm_overcalls": [], "no_answer": []}
    usage = {"calls": 0, "answered": 0}
    for item in key:
        p = RAW / (item["task_id"] + ".json")
        if not p.exists():
            buckets["no_answer"].append({**item, "problem": "not dispatched"})
            continue
        usage["calls"] += 1
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:                         # noqa: BLE001
            buckets["no_answer"].append({**item,
                                         "problem": str(exc)[:100]})
            continue
        verdict, problem = extract(doc)
        if verdict is None:
            buckets["no_answer"].append({**item, "problem": problem})
            continue
        usage["answered"] += 1
        row = {"task_id": item["task_id"], "round": item["round"],
               "line": item["line"], "my_verdict": item["my_verdict"],
               "glm_can_fail": verdict["can_fail"], "glm_why": verdict["why"]}
        mine_cannot = item["my_verdict"] == "cannot_fail"
        if mine_cannot and not verdict["can_fail"]:
            buckets["confirmed"].append(row)
        elif mine_cannot and verdict["can_fail"]:
            buckets["glm_disputes"].append(row)
        elif not mine_cannot and verdict["can_fail"]:
            buckets["control_held"].append(row)
        else:
            buckets["glm_overcalls"].append(row)

    # a task that ran out of reasoning budget answers nothing, and if those
    # skew toward one side the agreement figure is measured on an easier set
    # than the one I put forward. Report the split rather than the total.
    unanswered_findings = sum(1 for r in buckets["no_answer"]
                              if r["my_verdict"] == "cannot_fail")
    unanswered_controls = sum(1 for r in buckets["no_answer"]
                              if r["my_verdict"] == "can_fail")
    n_mine = sum(1 for i in key if i["my_verdict"] == "cannot_fail")
    n_ctrl = len(key) - n_mine
    totals = {
        "assertions_put_to_glm": len(key),
        "answered": usage["answered"],
        "no_usable_answer": len(buckets["no_answer"]),
        "my_cannot_fail_findings": n_mine,
        "confirmed_by_glm": len(buckets["confirmed"]),
        "disputed_by_glm": len(buckets["glm_disputes"]),
        "controls": n_ctrl,
        "controls_glm_got_right": len(buckets["control_held"]),
        "controls_glm_called_cannot_fail": len(buckets["glm_overcalls"]),
        "findings_with_no_answer": unanswered_findings,
        "controls_with_no_answer": unanswered_controls,
    }
    answered_findings = totals["confirmed_by_glm"] + totals["disputed_by_glm"]
    answered_controls = (totals["controls_glm_got_right"]
                         + totals["controls_glm_called_cannot_fail"])
    totals["agreement_on_my_findings"] = (
        "%d/%d" % (totals["confirmed_by_glm"], answered_findings)
        if answered_findings else "n/a")
    totals["control_accuracy"] = (
        "%d/%d" % (totals["controls_glm_got_right"], answered_controls)
        if answered_controls else "n/a")
    # a worker that never says can_fail agrees with every finding for free
    totals["glm_said_cannot_fail_on_everything"] = bool(
        answered_controls and totals["controls_glm_got_right"] == 0)

    OUT.write_text(json.dumps({"totals": totals, **buckets}, indent=2,
                              ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps(totals, indent=2, ensure_ascii=False))
    if buckets["glm_disputes"]:
        print("\nGLM disputes these findings of mine "
              "(each re-derived by hand before anything is changed):")
        for r in buckets["glm_disputes"]:
            print("  [%s] %s\n      GLM: %s" % (r["round"], r["line"],
                                                r["glm_why"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
