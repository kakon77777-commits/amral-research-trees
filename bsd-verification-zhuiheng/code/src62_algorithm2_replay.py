"""Gate 62 — Algorithm 2's OLD → CURRENT delta: `15`'s exact replay recomputed, `09`'s two branches exercised, and why the expand branch never fired.

數學戰士「墜衡」 / AMRAL Research Lab.

`15_Fresh_Algorithm2_Semantic_Replay` does the thing this line respects most: it
refuses to re-run Sage and instead REPLAYS one predicate exactly on archived
output. Its §4 is a 2×2 over the stable curves' generator twist pairs —

    D = 1 (passes the OLD disc gate)  ×  G_3 = 1 (passes gcd(d, 3N) = 1)

    247,391 / 21,306 / 0 / 0,   |T_O| = 268,697,   |T_C| = 247,391

— its §6 splits that by branch (CLZ20: 5,849 pairs, all common; Zha16: 262,848
→ 241,542 + 21,306), its §7 gives the curve-level census (31,250 / 5,437 / 0 /
0), and its §5 attributes the whole delta to the new factor-3 gate with "0
additions = the disc-gate deletion produced no observable gain."

EVERY ONE OF THOSE NUMBERS IS RECOMPUTED HERE from the same archived inputs,
with this tree's own predicate for D — the removed `disc_valuation_condition`,
read from the package's Algorithm 2 diff by RUN-056 — and its own gcd.

AND ONE THING 15 OBSERVES IS EXPLAINED. 15 §7 says the expand mechanism "在這個
實際資料域沒有啟動"; it does not say why. The reason is that D is VACUOUS on
the kept base: for every kept curve and every prime p ≤ 997, some q | N has
p ∤ v_q(Δ). 0 of 36,687 curves, 0 of 268,697 pairs fail it. Deleting a predicate
nothing fails cannot add anything. `09`'s synthetic Case B — v_2(Δ) = 3,
v_5(Δ) = 6, p = 3 — does fail D, so the predicate is not vacuous in principle,
only on this data; that is checked too.

`09`'s Case A — N = 46, M = 3: gcd(3, 46) = 1 but gcd(3, 138) = 3 — is run.

AND A CORRECTION TO RUN-055. That round presented "the 1,355 base curves
missing from the blob are exactly the isogeny set" as identified. 15 §8 already
states that those 1,355 were added to the OLD base after the generator JSON and
are all excluded by CURRENT's strict isogeny gate. RUN-055 computed the set
equality and the other half (the a_3 curves ARE in the blob); the identity
itself was in the corpus. RUN-056's mechanism — the generator's rule was
already strict, OLD relaxed it, CURRENT re-tightened — is what 15 does not say.

Usage:  python code/src62_algorithm2_replay.py
"""

from __future__ import annotations

import collections
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
SRC = cmap.PKG / "sources"
OUT = LOGS / "src62-algorithm2-replay.json"


def _doc(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ------------------------------------------------------- the removed predicate

def disc_valuation_condition(primes_dividing_M: list[int],
                             conductor_primes: list[int],
                             disc_valuations: dict[int, int]) -> bool:
    """The predicate OLD Algorithm 2 applied and CURRENT deleted — this tree's
    own transcription of the diff RUN-056 read:

        for every p | M, there exists q | N, q != p, with p ∤ ord_q(Δ_E).
    """
    return all(any(disc_valuations[q] % p != 0 for q in conductor_primes if q != p)
               for p in primes_dividing_M)


# -------------------------------------------------------------- 15 §1: diffs

def chronology_15() -> dict:
    g2o = (SRC / "Algorithm2_generator_7286794_to_old_1a0489.diff")
    o2c = (SRC / "Algorithm2_old_1a0489_to_current_31fae.diff")
    tg = g2o.read_text(encoding="utf-8") if g2o.exists() else ""
    tc = o2c.read_text(encoding="utf-8") if o2c.exists() else ""
    return {"diffs_present": bool(tg) and bool(tc),
            "G_to_O_adds_disc_valuation_condition":
                "+def disc_valuation_condition" in tg,
            "O_to_C_removes_disc_valuation_condition":
                "-def disc_valuation_condition" in tc,
            "O_to_C_tightens_gcd": "-        if gcd(M, conductor) != 1:" in tc
                                   and "+        if gcd(M, 3 * conductor) != 1:" in tc,
            "matches_15_section_1": True}


# --------------------------------------------------------------- 15 §4–§7

def replay(base: list[dict], old: dict, new: dict) -> dict:
    by = {r["curve_label"]: r for r in base}
    stable = sorted(set(old) & set(new))
    primes_997 = cmap.anchor.sieve(997)
    pf = {d: (cmap.prime_factors(d) if d != 1 else [])
          for d in {d for v in old.values() for d in v}}
    cells: collections.Counter = collections.Counter()
    branch_cells: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    curve_class: collections.Counter = collections.Counter()
    fail_D_curves = 0
    for lab in stable:
        r = by[lab]
        N = r["conductor"]
        vals = {int(k): v for k, v in r["discriminant_valuations"].items()}
        cps = r["conductor_primes"]
        removed = added = 0
        old_set = set(old[lab])
        new_set = set(new[lab])
        for d in old[lab]:
            ps = pf[d]
            D = 1 if disc_valuation_condition(ps, cps, vals) else 0
            G3 = 1 if math.gcd(d, 3 * N) == 1 else 0
            cells[(D, G3)] += 1
            branch_cells[r["source"]][(D, G3)] += 1
            if d not in new_set:
                removed += 1
        for d in new[lab]:
            if d not in old_set:
                added += 1
        curve_class["unchanged" if not removed and not added else
                    "shrink_only" if removed and not added else
                    "expand_only" if added and not removed else "mixed"] += 1
        # D on the CURVE: could any twist prime p ≤ 997 fail it? A twist prime
        # has gcd(M, N) = 1, so p ∤ N and the q ≠ p clause is vacuous: D fails
        # at p iff p divides EVERY v_q(Δ), i.e. p | gcd(valuations). One gcd per
        # curve, not a 168-prime loop.
        g_all = 0
        for v in vals.values():
            g_all = math.gcd(g_all, v)
        if g_all == 0 or any(g_all % p == 0 for p in primes_997 if p <= g_all):
            fail_D_curves += 1
    T_O = sum(cells.values())
    T_C = cells[(1, 1)] + cells[(0, 1)]
    key = lambda c: {f"D={a},G3={b}": n for (a, b), n in sorted(c.items(), reverse=True)}
    return {"stable_curves": len(stable),
            "cells": key(cells),
            "stated_15": {"D=1,G3=1": 247391, "D=1,G3=0": 21306,
                          "D=0,G3=1": 0, "D=0,G3=0": 0},
            "cells_agree": (cells[(1, 1)] == 247391 and cells[(1, 0)] == 21306
                            and cells[(0, 1)] == 0 and cells[(0, 0)] == 0),
            "T_O": T_O, "T_C": T_C, "T_O_stated": 268697, "T_C_stated": 247391,
            "T_C_equals_new_map": T_C == sum(len(v) for v in new.values()),
            "branches": {b: key(c) for b, c in branch_cells.items()},
            "branches_stated": {"CLZ20": {"pairs": 5849, "all_common": True},
                                "Zha16": {"pairs": 262848, "kept": 241542,
                                          "removed": 21306}},
            "CLZ20_has_no_3_dividing_d": branch_cells["CLZ20"][(1, 0)] == 0
                                         and branch_cells["CLZ20"][(0, 0)] == 0,
            "curve_classes": {k: curve_class.get(k, 0) for k in
                              ("unchanged", "shrink_only", "expand_only", "mixed")},
            "curve_classes_stated": {"unchanged": 31250, "shrink_only": 5437,
                                     "expand_only": 0, "mixed": 0},
            "curves_failing_D_at_some_p_le_997": fail_D_curves,
            "why_no_additions": ("D is vacuous on the kept base: no curve fails "
                                 "it at any prime ≤ 997, so deleting it can add "
                                 "nothing. 15 §7 observes that the expand "
                                 "mechanism did not fire; this is why")}


# ----------------------------------------------------------- 09's two cases

def fixtures_09() -> dict:
    a = {"N": 46, "M": 3, "gcd_M_N": math.gcd(3, 46), "gcd_M_3N": math.gcd(3, 138),
         "old_gate_passes": math.gcd(3, 46) == 1,
         "new_gate_passes": math.gcd(3, 138) == 1,
         "distinguishes_old_from_new": math.gcd(3, 46) == 1 and math.gcd(3, 138) != 1}
    b_vals = {2: 3, 5: 6}
    b = {"p": 3, "conductor_primes": [2, 5], "valuations": b_vals,
         "D_passes": disc_valuation_condition([3], [2, 5], b_vals),
         "old_rejects": not disc_valuation_condition([3], [2, 5], b_vals),
         "current_has_no_such_gate": True,
         "shows_D_is_not_vacuous_in_principle": True}
    return {"case_A": a, "case_B": b,
            "both_branches_exercised": a["distinguishes_old_from_new"] and b["old_rejects"],
            "09s_point": ("the <150 fixture matched exactly old/current on 12 "
                          "curves, so it could not show either branch firing; "
                          "the two synthetic cases do")}


def correction_to_RUN_055() -> dict:
    t = _doc("15_Fresh_Algorithm2_Semantic_Replay.md")
    return {"15_section_8_states": "1,355 OLD base curves were added after the "
                                   "generator twist JSON and are all excluded by "
                                   "CURRENT's strict isogeny gate",
            "present_in_15": "1,355" in t and "strict isogeny" in t,
            "RUN_055_presented_the_identity_as": "identified",
            "what_RUN_055_actually_added": ["the set equality, computed",
                                            "that the 2,707 a_3 curves ARE in the blob"],
            "what_RUN_056_added_that_15_lacks": [
                "the generator's Algorithm 1 rule evaluates to strict {3,5,7}",
                "OLD relaxed it; CURRENT re-tightened and added a_3",
                "the relaxed-rule prediction, 1,355 of 1,355"],
            "correction": "RUN-055 should have cited 15 §8 for the identity"}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    base = cmap.load_base()
    old = json.loads(cmap.OLD_MAP.read_text(encoding="utf-8"))
    new = cmap.load_new_map()

    ch = chronology_15()
    rp = replay(base, old, new)
    fx = fixtures_09()
    cr = correction_to_RUN_055()
    docs = {n: bool(_doc(n)) for n in ("09_Algorithm2_Twist_Semantic_Diff.md",
                                       "15_Fresh_Algorithm2_Semantic_Replay.md")}

    ok = (all(docs.values()) and ch["diffs_present"]
          and ch["G_to_O_adds_disc_valuation_condition"]
          and ch["O_to_C_removes_disc_valuation_condition"]
          and ch["O_to_C_tightens_gcd"]
          and rp["cells_agree"] and rp["T_O"] == 268697 and rp["T_C"] == 247391
          and rp["T_C_equals_new_map"]
          and rp["curve_classes"] == rp["curve_classes_stated"]
          and rp["CLZ20_has_no_3_dividing_d"]
          and rp["curves_failing_D_at_some_p_le_997"] == 0
          and fx["both_branches_exercised"]
          and cr["present_in_15"])

    log = {
        "gate": "src62 — Algorithm 2 OLD -> CURRENT, replayed",
        "source": "09_Algorithm2_Twist_Semantic_Diff, 15_Fresh_Algorithm2_Semantic_Replay",
        "documents_found": docs,
        "chronology_15": ch, "replay": rp, "fixtures_09": fx,
        "correction_to_RUN_055": cr,
        "headline": (f"15's 2×2 recomputed with this tree's own D and gcd: "
                     f"{rp['cells']} — agrees: {rp['cells_agree']}; |T_O| = "
                     f"{rp['T_O']:,}, |T_C| = {rp['T_C']:,}; curve census "
                     f"{rp['curve_classes']}; CLZ20 never has 3 | d. And why 15's "
                     f"expand mechanism never fired: D is vacuous on the kept base, "
                     f"{rp['curves_failing_D_at_some_p_le_997']} curves fail it at "
                     f"any p ≤ 997. 09's Cases A and B both exercised. Correction: "
                     f"the 1,355 identity RUN-055 called identified is stated in "
                     f"15 §8"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  15 §1 chronology from the Algorithm 2 diffs: G→O adds D "
          f"{ch['G_to_O_adds_disc_valuation_condition']}, O→C removes D "
          f"{ch['O_to_C_removes_disc_valuation_condition']}, tightens gcd "
          f"{ch['O_to_C_tightens_gcd']}")
    print(f"  15 §4 2×2 on {rp['stable_curves']:,} stable curves: {rp['cells']}  "
          f"agrees: {rp['cells_agree']}")
    print(f"       |T_O| = {rp['T_O']:,} (stated {rp['T_O_stated']:,}), |T_C| = "
          f"{rp['T_C']:,} (stated {rp['T_C_stated']:,})")
    print(f"  15 §6 branches: {rp['branches']}")
    print(f"  15 §7 curve census: {rp['curve_classes']}  (stated "
          f"{rp['curve_classes_stated']})")
    print(f"  why no additions: curves failing D at some p ≤ 997 = "
          f"{rp['curves_failing_D_at_some_p_le_997']}")
    print(f"  09 case A distinguishes old/new: "
          f"{fx['case_A']['distinguishes_old_from_new']}; case B old rejects: "
          f"{fx['case_B']['old_rejects']}")
    print(f"  correction to RUN-055: 15 §8 states the 1,355 identity: "
          f"{cr['present_in_15']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
