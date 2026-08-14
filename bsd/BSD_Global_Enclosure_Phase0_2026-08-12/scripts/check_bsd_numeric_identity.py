#!/usr/bin/env python3
"""Check the numerical BSD identity in a record.

This verifies arithmetic consistency of stored decimal values only.
It does NOT prove BSD or the actual order of Sha.
"""
from __future__ import annotations
from decimal import Decimal, getcontext
import json
import sys
from pathlib import Path

getcontext().prec = 60

def D(v):
    return Decimal(str(v))

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_bsd_numeric_identity.py RECORD.json")
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    bsd = data["strong_bsd"]
    lhs = D(bsd["special_value"]["value"])
    sha = D(bsd["sha"]["analytic_prediction"]["value"])
    omega = D(bsd["real_period"]["value"])
    reg = D(bsd["regulator"]["value"])
    tam = D(bsd["tamagawa_product"]["value"])
    tor = D(bsd["torsion_order"]["value"])
    rhs = sha * omega * reg * tam / (tor * tor)
    err = abs(lhs - rhs)
    rel = err / max(abs(lhs), Decimal("1e-100"))
    print("curve:", data["identity"]["lmfdb_label"])
    print("LHS:", lhs)
    print("RHS using analytic Sha prediction:", rhs)
    print("absolute error:", err)
    print("relative error:", rel)
    print("WARNING: numerical consistency is not a proof of actual Sha or strong BSD.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
