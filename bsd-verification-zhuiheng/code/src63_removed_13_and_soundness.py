"""Gate 63 — `08`'s thirteen removed curves, row by row against the census; and `03`'s six soundness gates, against what the package records.

數學戰士「墜衡」 / AMRAL Research Lab.

`08_Removed_13_First_Failure_Closure` is the small-fixture story: 25 base curves
under the OLD rule, 12 under CURRENT, and the 13 removed ones each given a
FIRST failure — 9 × P_ISOGENY_3, 2 × P_ISOGENY_5, 1 × P_ISOGENY_7, 1 × A3_ABS_3
— with the note that 26b1 also has a_3 = −3 but the pipeline runs the strict
isogeny gate first, so its first failure is P_ISOGENY_7. Every one of those
thirteen curves is a row of the 500K removed census this line already
recomputed at RUN-055, so every cell of 08's table is checkable: does the named
prime isogeny exist, is |a_3| = 3 where claimed and only there, does the LMFDB
label match, and does the 500K census's own first-failure ordering agree.

`03_Algorithm1_Soundness_Gates` lists six rules for a PASS certificate. Four
concern descent, Sha and timeouts — the certificate machinery this tree does
not run and the package did not run either; they are recorded as not
applicable by scope, the discipline of RUN-054 and RUN-056. S4 (testing flags
downgrade the run) is the flag audit RUN-056 already made. S6 lists seven
provenance fields every PASS must carry; the package's per-curve evidence is
audited against them field by field.

Usage:  python code/src63_removed_13_and_soundness.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
OUT = LOGS / "src63-removed-13-and-soundness.json"

# 08's table, transcribed
TABLE_08 = (
    ("14a1", "14.a6", "P_ISOGENY_3"),
    ("34a1", "34.a4", "P_ISOGENY_3"),
    ("66c1", "66.c3", "P_ISOGENY_5"),
    ("26a1", "26.a2", "P_ISOGENY_3"),
    ("26b1", "26.b2", "P_ISOGENY_7"),
    ("35a1", "35.a3", "P_ISOGENY_3"),
    ("38a1", "38.a3", "P_ISOGENY_3"),
    ("38b1", "38.b2", "P_ISOGENY_5"),
    ("106a1", "106.c2", "P_ISOGENY_3"),
    ("110c1", "110.a1", "P_ISOGENY_3"),
    ("110b1", "110.c1", "P_ISOGENY_3"),
    ("142e1", "142.c1", "A3_ABS_3"),
    ("142d1", "142.e2", "P_ISOGENY_3"),
)

S6_FIELDS = ("predicate", "value", "evidence_type", "backend",
             "semantic_version", "file/commit SHA", "timestamp")


def _doc(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ------------------------------------------------------------------- 08

def first_failure_from_census(row: dict) -> str:
    """The census's own ordering, as 08 states it: strict isogeny gate first,
    smallest prime first; then a_3."""
    for p in (3, 5, 7):
        if row[f"has_isogeny_{p}"] == "True":
            return f"P_ISOGENY_{p}"
    if row["abs_a3_eq_3"] == "True":
        return "A3_ABS_3"
    return "NONE"


def table_08(removed: list[dict]) -> dict:
    by = {r["curve_label"]: r for r in removed}
    rows, mismatches = [], []
    for label, lmfdb, stated in TABLE_08:
        r = by.get(label)
        if r is None:
            rows.append({"curve": label, "in_removed_census": False})
            mismatches.append(label)
            continue
        first = first_failure_from_census(r)
        entry = {"curve": label, "lmfdb_stated": lmfdb,
                 "lmfdb_census": r["lmfdb_label"],
                 "lmfdb_agrees": r["lmfdb_label"] == lmfdb,
                 "stated": stated, "census_first_failure": first,
                 "agrees": first == stated,
                 "has_isogeny": {p: r[f"has_isogeny_{p}"] == "True" for p in (3, 5, 7)},
                 "a3": int(r["a3"]) if r["a3"] not in ("", None) else None,
                 "abs_a3_eq_3": r["abs_a3_eq_3"] == "True",
                 "failure_class_500k": r["failure_class"],
                 "source": r["source"]}
        if not (entry["agrees"] and entry["lmfdb_agrees"]):
            mismatches.append(label)
        rows.append(entry)
    hist = {}
    for e in rows:
        hist[e.get("stated")] = hist.get(e.get("stated"), 0) + 1
    r26 = by.get("26b1")
    return {"rows": rows, "count": len(rows), "mismatches": mismatches,
            "all_agree": not mismatches,
            "histogram_stated": {"P_ISOGENY_3": 9, "P_ISOGENY_5": 2,
                                 "P_ISOGENY_7": 1, "A3_ABS_3": 1},
            "histogram_from_table": hist,
            "26b1_secondary_a3": (int(r26["a3"]) if r26 and r26["a3"] not in ("", None)
                                  else None),
            "26b1_is_the_BOTH_class": bool(r26 and r26["failure_class"] == "BOTH"),
            "26b1_first_failure_is_isogeny_7": bool(r26 and r26["has_isogeny_7"] == "True"),
            "142e1_has_no_357_isogeny": bool(by.get("142e1")
                                             and all(by["142e1"][f"has_isogeny_{p}"] != "True"
                                                     for p in (3, 5, 7))),
            "all_thirteen_in_the_500k_removed_census": all(
                l in by for l, _, _ in TABLE_08)}


def fixture_versus_500k(removed: list[dict]) -> dict:
    """08's 9/2/1/1 against the 500K histogram — the extrapolation 11 forbade."""
    iso3 = sum(1 for r in removed if first_failure_from_census(r) == "P_ISOGENY_3")
    iso5 = sum(1 for r in removed if first_failure_from_census(r) == "P_ISOGENY_5")
    iso7 = sum(1 for r in removed if first_failure_from_census(r) == "P_ISOGENY_7")
    a3 = sum(1 for r in removed if first_failure_from_census(r) == "A3_ABS_3")
    return {"fixture": {"P_ISOGENY_3": 9, "P_ISOGENY_5": 2, "P_ISOGENY_7": 1, "A3_ABS_3": 1},
            "five_hundred_k_first_failure": {"P_ISOGENY_3": iso3, "P_ISOGENY_5": iso5,
                                             "P_ISOGENY_7": iso7, "A3_ABS_3": a3},
            "sum": iso3 + iso5 + iso7 + a3,
            "fixture_a3_share": round(1 / 13, 4),
            "five_hundred_k_a3_share": round(a3 / (iso3 + iso5 + iso7 + a3), 4),
            "reading": ("under first-failure ordering, the 500K a_3 share is "
                        "about two thirds against the fixture's one thirteenth. "
                        "11 §4 said not to extrapolate 9/2/1/1; 08's own table "
                        "is that 9/2/1/1, and it is right about its 13 curves "
                        "and wrong as a proxy for 4,062")}


# ------------------------------------------------------------------- 03

def soundness_03(removed_meta: dict) -> dict:
    rec = (removed_meta.get("records") or [{}])[0]
    prov = removed_meta.get("provenance") or {}
    present = {
        "predicate": "a3_computation" in rec and "formula" in rec.get("a3_computation", {}),
        "value": "a3" in rec,
        "evidence_type": "evidence" in rec and "allcurves_line" in rec.get("evidence", {}),
        "backend": "method" in prov,
        "semantic_version": "schema_version" in removed_meta,
        "file/commit SHA": "ecdata_commit" in prov and "current_algorithm_commit" in prov,
        "timestamp": False,
    }
    # a timestamp anywhere in the metadata?
    blob = json.dumps(removed_meta)[:200000]
    present["timestamp"] = ("timestamp" in blob) or ("generated_at" in blob) or ("created" in blob)
    gates = [
        {"gate": "S1 analytic Sha must not impersonate actual Sha",
         "state": "N/A BY SCOPE", "why": "no Sha is computed or recorded in the "
                                        "package; no descent ran"},
        {"gate": "S2 dim Sha[2] must not impersonate ord_2 #Sha",
         "state": "N/A BY SCOPE", "why": "same"},
        {"gate": "S3 a timeout is UNKNOWN, not a failure",
         "state": "N/A BY SCOPE", "why": "no mwrank ran"},
        {"gate": "S4 testing flags downgrade the whole run",
         "state": "AUDITED AT RUN-056", "why": "skip_filter_S / skip_BSD_at_2_check "
                                              "appear only in archived source, "
                                              "never as recorded values"},
        {"gate": "S5 the S != ∅ production gate is deterministic",
         "state": "N/A BY SCOPE", "why": "Algorithm 2's certificate machinery is "
                                        "not run by the package or this tree"},
        {"gate": "S6 every PASS carries seven provenance fields",
         "state": f"{sum(present.values())} of 7 present in the per-curve "
                  f"evidence", "why": present},
    ]
    return {"gates": gates,
            "s6_fields": list(S6_FIELDS),
            "s6_present": present,
            "s6_count": sum(present.values()),
            "s6_missing": [k for k, v in present.items() if not v],
            "not_applicable_by_scope": sum(1 for g in gates if g["state"] == "N/A BY SCOPE"),
            "reading": ("03 is a spec for the certificate pipeline. The package "
                        "is an arithmetic census with no certificate pipeline in "
                        "it, and says so; four of six gates have nothing to bind "
                        "to. S6 is the one that does bind, and it binds field by "
                        "field")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    removed = cmap.load_removed()
    removed_meta = json.loads(cmap.REMOVED_JSON.read_text(encoding="utf-8"))
    t08 = table_08(removed)
    fx = fixture_versus_500k(removed)
    s03 = soundness_03(removed_meta)
    docs = {n: bool(_doc(n)) for n in ("08_Removed_13_First_Failure_Closure.md",
                                       "03_Algorithm1_Soundness_Gates.md")}

    ok = (all(docs.values())
          and t08["count"] == 13 and t08["all_agree"]
          and t08["all_thirteen_in_the_500k_removed_census"]
          and t08["histogram_from_table"] == t08["histogram_stated"]
          and t08["26b1_secondary_a3"] == -3 and t08["26b1_is_the_BOTH_class"]
          and t08["26b1_first_failure_is_isogeny_7"]
          and t08["142e1_has_no_357_isogeny"]
          and fx["sum"] == 4062
          and s03["s6_count"] >= 5
          and s03["not_applicable_by_scope"] == 4)

    log = {
        "gate": "src63 — 08's thirteen and 03's six",
        "source": "08_Removed_13_First_Failure_Closure, 03_Algorithm1_Soundness_Gates",
        "documents_found": docs,
        "table_08": t08, "fixture_versus_500k": fx, "soundness_03": s03,
        "headline": (f"08's thirteen rows, each checked against the 500K removed "
                     f"census's own columns: {13 - len(t08['mismatches'])} of 13 "
                     f"agree on first failure and LMFDB label; 26b1 is the BOTH "
                     f"class with a_3 = {t08['26b1_secondary_a3']} and a 7-isogeny, "
                     f"first failure P_ISOGENY_7 as 08 says; 142e1 has no 3/5/7 "
                     f"isogeny and |a_3| = 3. 08's 9/2/1/1 against 500K's "
                     f"{fx['five_hundred_k_first_failure']}: a_3 share "
                     f"{fx['fixture_a3_share']} vs {fx['five_hundred_k_a3_share']}. "
                     f"03: four of six gates N/A by the package's scope, S4 "
                     f"audited at RUN-056, S6's seven fields {s03['s6_count']} of 7 "
                     f"present — missing {s03['s6_missing']}"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  08's table: {t08['count']} rows, all agree {t08['all_agree']}, "
          f"mismatches {t08['mismatches']}")
    for e in t08["rows"]:
        flag = "OK " if e.get("agrees") and e.get("lmfdb_agrees") else "!! "
        print(f"    {flag}{e['curve']:<7} {e.get('lmfdb_census','?'):<8} "
              f"stated {e.get('stated'):<12} census {e.get('census_first_failure'):<12} "
              f"a3={e.get('a3')} class={e.get('failure_class_500k')}")
    print(f"  26b1: a3 = {t08['26b1_secondary_a3']}, BOTH class "
          f"{t08['26b1_is_the_BOTH_class']}, first failure isogeny-7 "
          f"{t08['26b1_first_failure_is_isogeny_7']}")
    print(f"  fixture 9/2/1/1 vs 500K first-failure "
          f"{fx['five_hundred_k_first_failure']} (sum {fx['sum']:,})")
    print()
    print("  03's six gates")
    for g in s03["gates"]:
        print(f"    {g['state']:<28} {g['gate'][:60]}")
    print(f"    S6 fields present: {s03['s6_present']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
