"""Full twist-map completeness: for every stable curve, {d < 1000 : admissible} vs the map.
Writes a result file to the scratchpad; the gate ingests it if present."""
import json, math, pathlib, sys, time
sys.path.insert(0, r"D:\Ai\work together\amral-research-trees\bsd-verification-zhuiheng\code")
import src57_theorem_2_18_condition_map as c
import src10_phase2_density_and_base as ph2, src16_twist_family_lvalues as fam

OUT = pathlib.Path(__file__).with_name("full_completeness_result.json")
base = c.load_base(); new = c.load_new_map(); by = {r["curve_label"]: r for r in base}
primes_lt_1000 = c.anchor.sieve(999)
cands = [d for d in range(1, 1000) if d % 4 == 1 and c.squarefree(d)]   # D1, D3 once
pf = {d: (c.prime_factors(d) if d != 1 else []) for d in cands}

def admissible(r, d, ap_cache, pc_cache, cubic, cubic_cache):
    N = r["conductor"]; a = r["ainvs"]
    if math.gcd(d, 3 * N) != 1:
        return False
    ps = pf[d]
    for p in ps:
        if p not in ap_cache:
            pc = c.point_count(a, p); pc_cache[p] = pc; ap_cache[p] = p + 1 - pc
        if ap_cache[p] % p == 0:
            return False
    if r["source"] == "Zha16_no_2_tors":
        for p in ps:
            if p not in cubic_cache:
                cubic_cache[p] = ph2.cubic_root_count(cubic, p)
            if cubic_cache[p] != 0:
                return False
        if any(fam.kronecker(d, q) != 1 for q in r["conductor_primes"]):
            return False
        if r["discriminant"] > 0 and d < 0:
            return False
    else:
        if any(p % 4 != 1 for p in ps):
            return False
        if any(pc_cache[p] % 4 != 2 for p in ps):
            return False
        if d % 8 != 1:
            return False
        if any(fam.kronecker(d, q) != 1 for q in r["conductor_primes"] if q != 2):
            return False
    return True

t0 = time.time(); labels = sorted(new)
missing_total = extra_total = 0; curves_off = []; done = 0
for lab in labels:
    r = by[lab]; cubic = c.two_division_cubic(r["ainvs"])
    ap, pc, cc = {}, {}, {}
    adm = {d for d in cands if admissible(r, d, ap, pc, cubic, cc)}
    inmap = set(new[lab])
    m, e = adm - inmap, inmap - adm
    if m or e:
        curves_off.append({"curve": lab, "missing": sorted(m)[:10], "extra": sorted(e)[:10]})
    missing_total += len(m); extra_total += len(e); done += 1
    if done % 2000 == 0:
        print(f"  {done}/{len(labels)}  missing {missing_total} extra {extra_total}  {time.time()-t0:.0f}s", flush=True)
res = {"bound": "d < 1000 (04_Algorithm1_Environment_and_Gaps: twists up to 1000)",
       "curves": len(labels), "pairs_in_map": sum(len(v) for v in new.values()),
       "admissible_but_absent": missing_total, "present_but_inadmissible": extra_total,
       "curves_with_any_difference": len(curves_off), "examples": curves_off[:20],
       "exact": missing_total == 0 and extra_total == 0, "seconds": round(time.time() - t0)}
OUT.write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "examples"}, indent=1))
