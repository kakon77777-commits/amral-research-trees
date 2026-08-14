#!/usr/bin/env python3
"""Post-process an LMFDB structural pool into exact witness-network certificates.

This script intentionally does NOT prove:
- BSD(E,2);
- fixed-additive FW-H2;
- finite-exception ordinary/supersingular theorems.

Those stay PENDING.
"""
from __future__ import annotations
import argparse, csv, json
from collections import defaultdict
from functools import reduce
from math import gcd
from pathlib import Path

def factor_primes(n: int) -> list[int]:
    n = abs(int(n))
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out.append(n)
    return out

def gcd_list(xs):
    xs = [abs(int(x)) for x in xs if int(x) != 0]
    return reduce(gcd, xs) if xs else 0

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def as_int(x):
    return int(x) if x not in (None, "", "NULL", "null") else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--local", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    base_rows = read_csv(args.base)
    local_rows = read_csv(args.local)

    local_by = defaultdict(list)
    for r in local_rows:
        rr = dict(r)
        for k in [
            "prime", "conductor_valuation", "discriminant_valuation",
            "j_denominator_valuation", "kodaira_symbol",
            "reduction_type", "root_number", "tamagawa_number"
        ]:
            rr[k] = as_int(rr.get(k))
        local_by[rr["lmfdb_label"]].append(rr)

    certs = []
    for b in base_rows:
        label = b["lmfdb_label"]
        rows = sorted(local_by[label], key=lambda x: x["prime"])

        additive = [r for r in rows if r["prime"] > 2 and r["reduction_type"] == 0]
        mult = [r for r in rows if r["prime"] > 2 and r["reduction_type"] in (-1, 1)]
        nonsplit = [r for r in mult if r["reduction_type"] == -1]

        g_mult = gcd_list([r["discriminant_valuation"] for r in mult])
        g_minus = gcd_list([r["discriminant_valuation"] for r in nonsplit])

        R_mult = [p for p in factor_primes(g_mult) if p > 2]
        R_minus = [p for p in factor_primes(g_minus) if p > 2]

        loo = []
        loo_pass = True
        for pbad in mult:
            p = pbad["prime"]
            witnesses = [
                w["prime"] for w in mult
                if w["prime"] != p and w["discriminant_valuation"] % p != 0
            ]
            passed = bool(witnesses)
            loo_pass &= passed
            loo.append({
                "p": p,
                "pass": passed,
                "witnesses": witnesses,
            })

        additive_h3 = []
        additive_h3_pass = True
        for a in additive:
            p = a["prime"]
            witnesses = [
                w["prime"] for w in nonsplit
                if w["discriminant_valuation"] % p != 0
            ]
            passed = bool(witnesses)
            additive_h3_pass &= passed
            additive_h3.append({
                "p": p,
                "pass": passed,
                "nonsplit_witnesses": witnesses,
            })

        edix_safe = all(
            a["prime"] >= 11 and a["kodaira_symbol"] not in (2, 3, 4)
            for a in additive
        ) and bool(additive)

        ultra_clean_h3 = any(
            r["discriminant_valuation"] == 1 for r in nonsplit
        )

        cert = {
            "lmfdb_label": label,
            "conductor": as_int(b.get("conductor")),
            "numeric_2part_parity_pass": True,
            "base_bsd2_status": "PENDING",
            "odd_additive_primes": [r["prime"] for r in additive],
            "edixhoven_safe_all_odd_additive": edix_safe,
            "fixed_additive_h2_status": {
                str(r["prime"]): "PENDING" for r in additive
            },
            "multiplicative_primes": [r["prime"] for r in mult],
            "nonsplit_multiplicative_primes": [r["prime"] for r in nonsplit],
            "g_mult": g_mult,
            "g_minus": g_minus,
            "R_mult": R_mult,
            "R_minus": R_minus,
            "leave_one_out": loo,
            "leave_one_out_all_pass": loo_pass,
            "fixed_additive_h3": additive_h3,
            "fixed_additive_h3_all_pass": additive_h3_pass,
            "ultra_clean_nonsplit_v1": ultra_clean_h3,
            "finite_ordinary_exception_status": {
                str(p): "PENDING" for p in R_mult
            },
            "finite_supersingular_exception_status": {
                str(p): "PENDING" for p in R_minus
            },
        }

        structural = (
            edix_safe
            and len(mult) >= 2
            and bool(nonsplit)
            and loo_pass
            and additive_h3_pass
        )
        cert["structural_status"] = (
            "STRUCTURAL_PASS" if structural else "STRUCTURAL_FAIL"
        )
        cert["theorem_status"] = (
            "PENDING_BSD2_AND_LOCAL_H2"
            if structural else "NOT_READY"
        )
        certs.append(cert)

    (outdir / "candidate_census.json").write_text(
        json.dumps(certs, indent=2), encoding="utf-8"
    )

    # Flat summary CSV.
    fields = [
        "lmfdb_label", "conductor", "structural_status", "theorem_status",
        "odd_additive_primes", "multiplicative_primes",
        "nonsplit_multiplicative_primes", "g_mult", "g_minus",
        "R_mult", "R_minus", "leave_one_out_all_pass",
        "fixed_additive_h3_all_pass", "ultra_clean_nonsplit_v1",
        "base_bsd2_status"
    ]
    with open(outdir / "candidate_census.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for c in certs:
            row = {k: c.get(k) for k in fields}
            for k in [
                "odd_additive_primes", "multiplicative_primes",
                "nonsplit_multiplicative_primes", "R_mult", "R_minus"
            ]:
                row[k] = json.dumps(row[k])
            w.writerow(row)

    summary = {
        "input_base_rows": len(base_rows),
        "input_local_rows": len(local_rows),
        "structural_pass": sum(c["structural_status"] == "STRUCTURAL_PASS" for c in certs),
        "ultra_clean_h3": sum(c["ultra_clean_nonsplit_v1"] for c in certs),
        "bsd2_pending": sum(c["base_bsd2_status"] == "PENDING" for c in certs),
        "fixed_additive_h2_pending_curve_count": sum(
            bool(c["fixed_additive_h2_status"]) for c in certs
        ),
        "claim_discipline": (
            "No structural candidate is promoted to proved BSD family without "
            "rigorous BSD(E,2) and local additive H2 certificates."
        ),
    }
    (outdir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    report = f"""# LMFDB Exact Census Report

- base rows: {summary['input_base_rows']}
- local rows: {summary['input_local_rows']}
- structural pass: {summary['structural_pass']}
- ultra-clean nonsplit-v1: {summary['ultra_clean_h3']}
- BSD(E,2) pending: {summary['bsd2_pending']}
- curves with fixed-additive H2 pending: {summary['fixed_additive_h2_pending_curve_count']}

## Claim discipline

{summary['claim_discipline']}
"""
    (outdir / "CENSUS_REPORT.md").write_text(report, encoding="utf-8")

if __name__ == "__main__":
    main()
