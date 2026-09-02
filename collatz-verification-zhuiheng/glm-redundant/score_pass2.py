"""Score pass 2 — the same questions, less context — SEPARATELY from pass 1.

數學戰士「墜衡」 / AMRAL Research Lab.

Pass 1 sent each question with the whole ~8 KB script. Nine of twenty-eight
returned nothing: the model spent its entire 4096-token output budget reasoning
and stopped. Six of those nine were controls, which left the control arm at 3
answers — and all three were the two documented-borderline cases plus one
criterion disagreement. That is far too thin to decide whether the worker can
distinguish at all.

Pass 2 re-asks only the unanswered ones with the context cut to the module
helpers plus the single enclosing block. **It is a different condition** and is
never pooled with pass 1: the same worker given an easier read of the same
question is not the same experiment. What it can settle is narrow and worth
settling — whether GLM ever says `can_fail: true` when the reasoning fits.

Usage:  python glm-redundant/score_pass2.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
RAW2 = ROOT / "raw_pass2"
KEY2 = ROOT / "pass2_key.json"
OUT = ROOT / "pass2_result.json"


def extract(doc: dict):
    if doc.get("status") != "candidate_success":
        meta = doc.get("provider_meta", {}) or {}
        return None, str(meta.get("finish_reason") or doc.get("status"))
    answer = (doc.get("answer") or "").strip()
    m = re.search(r"\{.*\}", answer, re.S)
    if not m:
        return None, "no JSON object"
    try:
        parsed = json.loads(m.group(0))
    except Exception:                                    # noqa: BLE001
        return None, "unparsable JSON"
    if not isinstance(parsed.get("can_fail"), bool):
        return None, "no boolean can_fail"
    return ({"can_fail": parsed["can_fail"],
             "why": str(parsed.get("why") or "")[:240]}, None)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    key = json.loads(KEY2.read_text(encoding="utf-8"))["items"]
    rows, unanswered = [], []
    for item in key:
        p = RAW2 / (item["task_id"] + ".json")
        if not p.exists():
            unanswered.append({**item, "problem": "not dispatched"})
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:                                # noqa: BLE001
            unanswered.append({**item, "problem": "decode crash"})
            continue
        verdict, problem = extract(doc)
        if verdict is None:
            unanswered.append({**item, "problem": problem})
            continue
        rows.append({**item, "glm_can_fail": verdict["can_fail"],
                     "glm_why": verdict["why"],
                     "correct": (verdict["can_fail"]
                                 == (item["my_verdict"] == "can_fail"))})

    ctrl = [r for r in rows if r["my_verdict"] == "can_fail"]
    find = [r for r in rows if r["my_verdict"] == "cannot_fail"]
    ever_true = any(r["glm_can_fail"] for r in rows)
    totals = {
        "dispatched": len(key),
        "answered": len(rows),
        "no_usable_answer": len(unanswered),
        "controls_answered": len(ctrl),
        "controls_correct": sum(1 for r in ctrl if r["correct"]),
        "findings_answered": len(find),
        "findings_confirmed": sum(1 for r in find if r["correct"]),
        "glm_ever_said_can_fail": ever_true,
    }
    # the only question pass 2 exists to settle
    totals["verdict"] = (
        "the worker CAN distinguish once the reasoning fits"
        if ever_true else
        "the worker said cannot-fail to every question in both passes; its "
        "agreement carries no information")
    OUT.write_text(json.dumps({"totals": totals, "rows": rows,
                               "unanswered": unanswered}, indent=2,
                              ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps(totals, indent=2, ensure_ascii=False))
    for r in ctrl:
        print("\n  CONTROL %s  glm_can_fail=%s  %s" %
              (r["task_id"], r["glm_can_fail"],
               "correct" if r["correct"] else "WRONG"))
        print("    %s" % r["line"])
        print("    %s" % r["glm_why"][:200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
