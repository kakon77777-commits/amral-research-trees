#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from algorithm2_pure_python import admissible_twists_clz, admissible_twists_zhai

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    records = json.loads((ROOT/"fixtures"/"representative_curves.json").read_text())
    report = {"bound": 1000, "cases": []}

    for label, rec in records.items():
        if rec["source"] == "CLZ20":
            actual = admissible_twists_clz(rec["ainvs"], rec["conductor"], 1000)
        else:
            actual = admissible_twists_zhai(rec["ainvs"], rec["conductor"], 1000)
        expected = rec["expected_twists_B1000"]
        case = {
            "label": label,
            "lmfdb_label": rec["lmfdb_label"],
            "branch": rec["source"],
            "expected_count": len(expected),
            "actual_count": len(actual),
            "exact_match": actual == expected,
            "expected": expected,
            "actual": actual,
            "missing": sorted(set(expected)-set(actual)),
            "extra": sorted(set(actual)-set(expected)),
        }
        report["cases"].append(case)

    report["all_pass"] = all(c["exact_match"] for c in report["cases"])
    out = ROOT/"results"/"reproduction_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["all_pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
