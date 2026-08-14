#!/usr/bin/env python3
"""Incremental verifier for the 2026-06-03 Algorithm1 semantic change.

Input JSONL rows:
{
  "cremona_label": "...",
  "a3": integer,
  "isogeny_degrees": [integers...]
}

Assumption:
Each row already passed the 2026-05-22 Algorithm1. Since the only
Algorithm1 theorem-predicate change in the next commit is:
  1) always exclude rational 3/5/7-isogenies;
  2) independently require a3 != +/-3,
the new membership decision is exactly determined by these fields.

This script does NOT prove that the input rows passed the old algorithm.
It verifies only the one-commit delta.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

STRICT_PRIMES = {3,5,7}

def prime_isogeny_degrees(values):
    # For this delta, only 3/5/7 matter. LMFDB isogeny_degrees may include
    # composite degrees; filtering by membership in STRICT_PRIMES is exact.
    return sorted({int(x) for x in values if int(x) in STRICT_PRIMES})

def decide(row):
    hits = prime_isogeny_degrees(row.get("isogeny_degrees", []))
    a3 = int(row["a3"])
    failures = []
    # Current production order: strict p-isogeny gate before a3 gate.
    for p in hits:
        failures.append(f"P_ISOGENY_{p}")
    if abs(a3) == 3:
        failures.append("A3_ABS_3")
    return {
        "cremona_label": row["cremona_label"],
        "decision": "PASS" if not failures else "FAIL",
        "first_failure": failures[0] if failures else None,
        "all_failures": failures,
        "a3": a3,
        "isogeny_degrees": row.get("isogeny_degrees", []),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input_jsonl")
    ap.add_argument("--output", default=None)
    args=ap.parse_args()
    rows=[]
    for line in Path(args.input_jsonl).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    out=[decide(r) for r in rows]
    payload={
        "input_count":len(rows),
        "pass_count":sum(x["decision"]=="PASS" for x in out),
        "fail_count":sum(x["decision"]=="FAIL" for x in out),
        "rows":out
    }
    text=json.dumps(payload,indent=2)
    if args.output:
        Path(args.output).write_text(text,encoding="utf-8")
    print(text)

if __name__=="__main__":
    main()
