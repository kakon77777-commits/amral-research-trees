#!/usr/bin/env python3
"""Rebuild v0.6 semantic partition from a v0.5 extracted directory."""
from pathlib import Path
from collections import Counter
import json, math, sys

def pf(n):
    n=abs(int(n)); out=[]; p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0: n//=p
        p=3 if p==2 else p+2
    if n>1: out.append(n)
    return out

def disc_ok(d, r):
    qs=[int(q) for q in r["conductor_primes"]]
    vals={int(q):int(v) for q,v in r["discriminant_valuations"].items()}
    return all(any(vals[q] % p != 0 for q in qs if q != p) for p in pf(d))

base=Path(sys.argv[1])
old=json.loads((base/"inputs/old/twists_of_ec_labels_500k.json").read_text())
new=json.loads((base/"inputs/new/twists_of_ec_labels_500k.json").read_text())
meta=json.loads((base/"inputs/metadata/old_base_curve_arithmetic.json").read_text())
md={r["curve_label"]:r for r in meta["records"]}

disc_fail=0
for E,ds in old.items():
    for d in ds:
        disc_fail += int(not disc_ok(d,md[E]))

cells=Counter()
mismatch=0
for E,curds in new.items():
    r=md[E]
    pred=set()
    for d in old[E]:
        D=disc_ok(d,r)
        G=math.gcd(abs(int(d)),3*int(r["conductor"]))==1
        cells[("D1" if D else "D0")+("_G1" if G else "_G0")]+=1
        if G: pred.add(d)
    mismatch += int(pred != set(curds))

print(json.dumps({
    "disc_fail_all_materialized":disc_fail,
    "stable_cells":dict(cells),
    "current_prediction_mismatch_curves":mismatch
},indent=2))
assert disc_fail == 0
assert cells == Counter({"D1_G1":247391,"D1_G0":21306})
assert mismatch == 0
