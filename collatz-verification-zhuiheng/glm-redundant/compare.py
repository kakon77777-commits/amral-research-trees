"""Score GLM's blind candidates against this arm's own findings.

數學戰士「墜衡」 / AMRAL Research Lab.

GLM 5.3 Flash read each bundle's own verification script cold -- no access to
my gates, my reports or my conclusions -- and was asked one neutral question per
section of the script: which assertions here cannot fail. This compares its
candidates against `my_findings.json`, which was written down BEFORE any answer
came back, so the scoring is mechanical rather than retrospective.

Three outcomes matter, and only one of them is comfortable:

  * **agreed** -- GLM names an assertion I also named. Redundant confirmation.
  * **glm_only** -- GLM names one I did not. This is the reason the layer
    exists, and NOT a finding until I verify it myself: a candidate is a
    candidate.
  * **mine_only** -- I named one GLM did not. Says something about GLM's
    recall at this profile, nothing about whether I was right.

Usage:  python glm-redundant/compare.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "raw"
MINE = ROOT / "my_findings.json"
OUT = ROOT / "comparison.json"


def normalise(line: str) -> str:
    """Compare assertions by their arithmetic, not their spacing.

    Their scripts write `assert Bp >= Bt+L` and a reader may quote it as
    `assert Bp>=Bt+L`; both are the same assertion.
    """
    s = line.strip()
    s = re.sub(r"^assert\s+", "", s)
    s = re.sub(r"\s+", "", s)
    s = s.rstrip(",")
    return s.lower()


def load_candidates() -> dict:
    """GLM's answers, keyed by round. A malformed answer is recorded, not
    dropped: a worker that returns nothing usable is a result about the
    worker."""
    out: dict = {}
    problems = []
    for p in sorted(RAW.glob("au2d*.json")):
        rnd = p.stem.split("-")[0]
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:                        # noqa: BLE001
            problems.append({"task": p.stem, "problem": "unparsable envelope",
                             "detail": str(exc)[:120]})
            continue
        status = doc.get("status")
        answer = doc.get("answer") or ""
        if status != "candidate_success" or not answer.strip():
            problems.append({"task": p.stem, "problem": "no candidate",
                             "status": status,
                             "warnings": doc.get("warnings", [])[:2]})
            continue
        body = answer.strip()
        # a bounded worker sometimes fences its JSON; that is a materialisation
        # detail, not a wrong answer
        m = re.search(r"\{.*\}", body, re.S)
        if not m:
            problems.append({"task": p.stem, "problem": "no JSON object"})
            continue
        try:
            parsed = json.loads(m.group(0))
        except Exception as exc:                        # noqa: BLE001
            problems.append({"task": p.stem, "problem": "unparsable JSON",
                             "detail": str(exc)[:120]})
            continue
        items = parsed.get("cannot_fail") or []
        for it in items:
            if not isinstance(it, dict) or not it.get("line"):
                continue
            out.setdefault(rnd, []).append({
                "task": p.stem,
                "line": str(it["line"]),
                "counter": str(it.get("counter") or ""),
                "why": str(it.get("why") or ""),
            })
    return {"by_round": out, "problems": problems}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    mine_doc = json.loads(MINE.read_text(encoding="utf-8"))
    mine: dict = {}
    for f in mine_doc["findings"]:
        mine.setdefault(f["round"], []).append(f)

    cands = load_candidates()
    by_round = cands["by_round"]

    rounds = sorted(set(mine) | set(by_round))
    report: dict = {"rounds": {}, "dispatch_problems": cands["problems"]}
    tot_agreed = tot_glm_only = tot_mine_only = 0

    for rnd in rounds:
        mine_r = mine.get(rnd, [])
        glm_r = by_round.get(rnd, [])
        mine_keys = {normalise(f["line"]): f for f in mine_r}
        glm_keys: dict = {}
        for c in glm_r:
            glm_keys.setdefault(normalise(c["line"]), c)

        agreed, glm_only, mine_only = [], [], []
        for k, c in glm_keys.items():
            if k in mine_keys:
                agreed.append({"line": mine_keys[k]["line"],
                               "counter": mine_keys[k]["counter"],
                               "glm_reason": c["why"][:220],
                               "my_reason": mine_keys[k]["why"]})
            else:
                glm_only.append({"line": c["line"], "counter": c["counter"],
                                 "glm_reason": c["why"][:220],
                                 "task": c["task"],
                                 "status": "CANDIDATE - not a finding until "
                                           "independently verified"})
        for k, f in mine_keys.items():
            if k not in glm_keys:
                mine_only.append({"line": f["line"], "counter": f["counter"],
                                  "my_reason": f["why"], "run": f["run"]})

        report["rounds"][rnd] = {
            "mine": len(mine_r), "glm_candidates": len(glm_keys),
            "agreed": agreed, "glm_only": glm_only, "mine_only": mine_only,
            "counts": {"agreed": len(agreed), "glm_only": len(glm_only),
                       "mine_only": len(mine_only)},
        }
        tot_agreed += len(agreed)
        tot_glm_only += len(glm_only)
        tot_mine_only += len(mine_only)

    report["totals"] = {
        "mine": sum(len(v) for v in mine.values()),
        "glm_candidates": sum(len(v) for v in by_round.values()),
        "agreed": tot_agreed,
        "glm_only_needing_my_verification": tot_glm_only,
        "mine_only": tot_mine_only,
        "tasks_with_no_usable_candidate": len(cands["problems"]),
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"totals": report["totals"],
                      "per_round": {r: report["rounds"][r]["counts"]
                                    for r in rounds},
                      "dispatch_problems": len(cands["problems"])},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
