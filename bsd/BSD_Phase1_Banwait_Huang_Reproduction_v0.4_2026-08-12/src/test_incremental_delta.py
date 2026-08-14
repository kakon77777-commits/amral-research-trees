#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
inp=ROOT/"fixtures"/"delta_semantic_fixture.jsonl"
out=ROOT/"results"/"delta_semantic_fixture_output.json"
proc=subprocess.run(
    [sys.executable,str(ROOT/"src"/"incremental_algorithm1_delta.py"),str(inp),"--output",str(out)],
    capture_output=True,text=True
)
payload=json.loads(out.read_text())
expected={}
for line in inp.read_text().splitlines():
    r=json.loads(line); expected[r["cremona_label"]]=r["expected"]
actual={r["cremona_label"]:r["decision"] for r in payload["rows"]}
checks={
    "runner_returncode_zero":proc.returncode==0,
    "decisions_match":actual==expected,
    "46a1_survives":actual["46a1"]=="PASS",
    "106d1_survives":actual["106d1"]=="PASS",
    "34a1_dies_strict_3":next(r for r in payload["rows"] if r["cremona_label"]=="34a1")["first_failure"]=="P_ISOGENY_3",
    "38b1_dies_strict_5":next(r for r in payload["rows"] if r["cremona_label"]=="38b1")["first_failure"]=="P_ISOGENY_5",
    "26b1_order_is_7_then_a3":next(r for r in payload["rows"] if r["cremona_label"]=="26b1")["all_failures"]==["P_ISOGENY_7","A3_ABS_3"],
    "142e1_dies_a3":next(r for r in payload["rows"] if r["cremona_label"]=="142e1")["first_failure"]=="A3_ABS_3",
}
report={"checks":checks,"pass":all(checks.values()),"actual":actual}
(ROOT/"results"/"delta_semantic_fixture_test.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
sys.exit(0 if report["pass"] else 1)
