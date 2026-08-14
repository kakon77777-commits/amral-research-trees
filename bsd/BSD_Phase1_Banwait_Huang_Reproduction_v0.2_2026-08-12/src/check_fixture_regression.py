#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
ROOT = Path(__file__).resolve().parents[1]
def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {r["cremona_label"]: r for r in csv.DictReader(f)}
old = load(ROOT/"fixtures"/"ec_labels_150_old_2026-05-22.csv")
cur = load(ROOT/"fixtures"/"ec_labels_150_current_2026-06-03.csv")
expected_removed = {
    "14a1","34a1","66c1","26a1","26b1","35a1","38a1","38b1",
    "106a1","110c1","110b1","142e1","142d1"
}
removed = set(old)-set(cur)
added = set(cur)-set(old)
checks = {
    "old_count_25": len(old)==25,
    "current_count_12": len(cur)==12,
    "current_subset_of_old": set(cur).issubset(old),
    "removed_exactly_13": len(removed)==13,
    "removed_set_exact": removed==expected_removed,
    "no_added_curves": added==set(),
}
report = {"checks":checks,"pass":all(checks.values()),"removed":sorted(removed),"added":sorted(added)}
(ROOT/"results"/"fixture_regression_test.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
sys.exit(0 if report["pass"] else 1)
