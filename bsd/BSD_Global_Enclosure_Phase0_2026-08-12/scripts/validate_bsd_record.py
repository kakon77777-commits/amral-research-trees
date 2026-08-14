#!/usr/bin/env python3
"""Minimal validator for BSD certificate records.

Uses jsonschema when installed; otherwise performs structural checks.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

def fallback_validate(data: dict) -> list[str]:
    errors = []
    for key in ("schema_version", "identity", "rank", "strong_bsd", "certificate", "provenance"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    level = data.get("certificate", {}).get("level")
    if not isinstance(level, int) or not (0 <= level <= 10):
        errors.append("certificate.level must be integer 0..10")
    label = data.get("identity", {}).get("lmfdb_label")
    if not label:
        errors.append("missing identity.lmfdb_label")
    sha = data.get("strong_bsd", {}).get("sha", {})
    analytic = sha.get("analytic_prediction", {})
    proved = sha.get("proved_order", {})
    if analytic.get("evidence_type") == "BSD_inferred" and proved.get("status") == "proved":
        if proved.get("value") == analytic.get("value") and not proved.get("certificate_ref"):
            errors.append("proved Sha order cannot be copied from BSD-inferred value without certificate_ref")
    return errors

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_bsd_record.py RECORD.json")
        return 2
    record_path = Path(sys.argv[1])
    data = json.loads(record_path.read_text(encoding="utf-8"))
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "bsd_curve_certificate.schema.json"
    try:
        import jsonschema
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(data, schema)
        errors = fallback_validate(data)
    except ImportError:
        errors = fallback_validate(data)
    except Exception as exc:
        errors = [str(exc)]
    if errors:
        print("FAIL")
        for e in errors:
            print("-", e)
        return 1
    print("PASS:", data["identity"]["lmfdb_label"], "C" + str(data["certificate"]["level"]))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
