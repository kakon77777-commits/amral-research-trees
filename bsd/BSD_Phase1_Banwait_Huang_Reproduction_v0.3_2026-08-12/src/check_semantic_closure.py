#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/"results"/"removed_13_cause_map.json").read_text(encoding="utf-8"))
t=json.loads((ROOT/"results"/"stable_twist_exact_match.json").read_text(encoding="utf-8"))
curves=m["curves"]
hist={}
for r in curves:
    hist[r["first_failure"]]=hist.get(r["first_failure"],0)+1
checks={
    "removed_exactly_13":len(curves)==13,
    "unique_removed_labels":len({r["cremona_label"] for r in curves})==13,
    "histogram_exact":hist=={"P_ISOGENY_3":9,"P_ISOGENY_5":2,"P_ISOGENY_7":1,"A3_ABS_3":1},
    "only_142e1_first_fails_a3":[r["cremona_label"] for r in curves if r["first_failure"]=="A3_ABS_3"]==["142e1"],
    "26b1_secondary_a3":next(r for r in curves if r["cremona_label"]=="26b1")["all_new_failures"]==["P_ISOGENY_7","A3_ABS_3"],
    "stable_twists_exact":t["all_stable_entries_exact_match"] is True,
    "stable_count_12":t["stable_base_curve_count"]==12,
}
out={"checks":checks,"pass":all(checks.values()),"computed_histogram":hist}
(ROOT/"results"/"semantic_closure_test.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
sys.exit(0 if out["pass"] else 1)
