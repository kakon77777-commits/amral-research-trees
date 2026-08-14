#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
text_ext = {".md", ".py", ".json", ".txt"}
errors = []

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in text_ext:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"UTF8_FAIL {path}: {exc}")
        continue
    bad = [chr(92)+"[", chr(92)+"]", chr(92)+"(", chr(92)+")"]
    if any(token in text for token in bad):
        errors.append(f"NONCANONICAL_LATEX_DELIMITER {path}")

status_path = ROOT / "results" / "p5_gate_status.json"
try:
    status = json.loads(status_path.read_text(encoding="utf-8"))
    if status.get("overall_status") != "P5_REDUCED_TO_DERIVED_ARCHIMEDEAN_PERIOD_COMPARISON":
        errors.append("STATUS_MISMATCH")
except Exception as exc:
    errors.append(f"JSON_FAIL: {exc}")

if errors:
    print("VALIDATION_FAIL")
    for e in errors:
        print(e)
    sys.exit(1)
print("VALIDATION_OK")
