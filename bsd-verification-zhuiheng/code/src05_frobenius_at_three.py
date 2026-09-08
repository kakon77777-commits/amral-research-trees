"""Gate 05 — recount every removed curve over F_3, and re-derive the census's accounting.

數學戰士「墜衡」 / AMRAL Research Lab.

The Banwait–Huang census removes 4,062 of 40,749 base curves, and explains each
removal by one of two mechanisms: the trace of Frobenius at 3, or a rational
3/5/7-isogeny. The package publishes the accounting in `results/summary.json`
and the per-curve evidence in `results/algorithm1_removed_census.csv`.

This gate recomputes the arithmetic half of that from the a-invariants alone.

WHAT `a3` MEANS HERE, because the name is a trap. It is **not** the Weierstrass
coefficient a₃. It is the trace of Frobenius at p = 3:

    a_3 = 3 + 1 - #E(F_3)

The CSV's own columns settle it: curve `14a1` records `a3 = -2` beside
`projective_point_count_at_3 = 6`, and 4 - 6 = -2. A gate that read the column
name and compared against the Weierstrass a₃ would report 4,062 mismatches
against correct data.

FIVE CHECKS, all exact — F_3 arithmetic and integer counting, no float:

  1. **Projective point count over F_3**, recounted by exhaustive search over
     F_3 x F_3 plus the point at infinity, against the stored count.
  2. **The nonsingular count**, recounted by excluding singular points, against
     its own stored column.
  3. **a_3 = 4 - #E(F_3)** where the curve has good reduction at 3, against the
     stored `a3` and against ecdata's own aplist token.
  4. **The a3 histogram**, rebuilt from the recomputed values, against
     `summary.json`.
  5. **The removal accounting**: a3_only + isogeny_only + both = removed, and
     base_old - removed + added = base_new.

The histogram is the interesting one. `summary.json` publishes keys
{-3,-2,-1,1,3} — and by Hasse |a_3| <= 2*sqrt(3) < 4, so the possible values are
{-3,...,3}. **Zero and two are absent.** Whether that is a fact about the removed
population or a gap in the histogram is exactly what recomputing settles.

Usage:  python code/src05_frobenius_at_three.py
"""

from __future__ import annotations

import collections
import csv
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = (pathlib.Path("D:/我的研究/學術討論/論文/數學/BSD")
       / "BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12")
CENSUS = PKG / "results" / "algorithm1_removed_census.csv"
SUMMARY = PKG / "results" / "summary.json"
ARITH = PKG / "inputs" / "metadata" / "old_base_curve_arithmetic.json"
OUT = ROOT / "data" / "gate-logs" / "src05-frobenius-at-three.json"

P = 3


def point_counts(a1: int, a2: int, a3: int, a4: int, a6: int) -> tuple[int, int]:
    """(projective points over F_3, nonsingular projective points over F_3).

    Exhaustive over the 9 affine pairs plus the point at infinity, which is
    always nonsingular on a Weierstrass model. A point is singular where both
    partial derivatives of F = y^2 + a1 x y + a3 y - x^3 - a2 x^2 - a4 x - a6
    vanish together with F itself.
    """
    a1, a2, a3, a4, a6 = (c % P for c in (a1, a2, a3, a4, a6))
    total = 1                      # the point at infinity
    nonsingular = 1
    for x in range(P):
        for y in range(P):
            f = (y * y + a1 * x * y + a3 * y
                 - (x ** 3 + a2 * x * x + a4 * x + a6)) % P
            if f:
                continue
            total += 1
            df_dx = (a1 * y - (3 * x * x + 2 * a2 * x + a4)) % P
            df_dy = (2 * y + a1 * x + a3) % P
            if df_dx or df_dy:
                nonsingular += 1
    return total, nonsingular


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (CENSUS, SUMMARY, ARITH):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")

    ainvs = {r["curve_label"]: r["ainvs"]
             for r in json.loads(ARITH.read_text(encoding="utf-8"))["records"]}
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    rows = list(csv.DictReader(CENSUS.open(encoding="utf-8")))
    count_mismatch, nonsing_mismatch, a3_mismatch, aplist_mismatch = [], [], [], []
    missing_ainvs = []
    hist = collections.Counter()
    bad_reduction_types = collections.Counter()
    unclassified_bad, bad_a3_mismatch = [], []
    aplist_nonnumeric = collections.Counter()
    good_reduction = 0
    failure_classes = collections.Counter()

    for r in rows:
        label = r["curve_label"]
        failure_classes[r["failure_class"]] += 1
        inv = ainvs.get(label)
        if inv is None:
            missing_ainvs.append(label)
            continue
        total, nonsing = point_counts(*inv)

        if int(r["projective_point_count_at_3"]) != total:
            count_mismatch.append({"label": label, "stored": r["projective_point_count_at_3"],
                                   "recomputed": total})
        if int(r["nonsingular_projective_point_count_at_3"]) != nonsing:
            nonsing_mismatch.append({"label": label,
                                     "stored": r["nonsingular_projective_point_count_at_3"],
                                     "recomputed": nonsing})

        good = r["good_reduction_at_3"].strip().lower() == "true"
        if good:
            good_reduction += 1
            mine = P + 1 - total
        else:
            # Bad reduction still has a well-defined a_p, fixed by the reduction
            # type: split multiplicative +1, non-split -1, additive 0. The type
            # is read off the NONSINGULAR count, which is p-1, p+1 and p
            # respectively — already computed above, so nothing new is assumed
            # and no convention is taken on the package's behalf.
            bad_reduction_types[nonsing] += 1
            mine = {P - 1: 1, P + 1: -1, P: 0}.get(nonsing)
            if mine is None:
                unclassified_bad.append({"label": label, "nonsingular": nonsing})
                continue

        hist[mine] += 1
        stored = r["a3"].strip()
        if stored not in ("", "None") and int(stored) != mine:
            (a3_mismatch if good else bad_a3_mismatch).append(
                {"label": label, "stored": stored, "recomputed": mine,
                 "good_reduction_at_3": good, "nonsingular_count": nonsing})
        # ecdata writes a placeholder rather than an integer at some primes.
        # Counted, not silently skipped: a comparison that quietly declines to
        # run on part of its population is the shape this arm catalogues.
        tok = r.get("ecdata_aplist_a3_token", "").strip()
        try:
            tok_val = int(tok)
        except ValueError:
            aplist_nonnumeric[tok or "(empty)"] += 1
        else:
            if tok_val != mine:
                aplist_mismatch.append({"label": label, "ecdata": tok,
                                        "recomputed": mine,
                                        "good_reduction_at_3": good})

    stored_hist = {int(k): v for k, v in
                   summary.get("algorithm1", {}).get("a3_histogram", {}).items()}
    hist_diff = {str(k): {"stored": stored_hist.get(k, 0), "recomputed": hist.get(k, 0)}
                 for k in sorted(set(stored_hist) | set(hist))
                 if stored_hist.get(k, 0) != hist.get(k, 0)}

    a1 = summary.get("algorithm1", {})
    base = summary.get("base", {})
    accounting = {
        "a3_only + isogeny_only + both == removed": (
            a1.get("a3_only", 0) + a1.get("isogeny_only", 0) + a1.get("both", 0)
            == base.get("removed")),
        "old - removed + added == new": (
            base.get("old", 0) - base.get("removed", 0) + base.get("added", 0)
            == base.get("new")),
        "individual_isogeny_counts == isogeny_only + both": (
            sum(a1.get("individual_isogeny_counts", {}).values())
            == a1.get("isogeny_only", 0) + a1.get("both", 0)),
        "isogeny_combination_counts.NONE == a3_only": (
            a1.get("isogeny_combination_counts", {}).get("NONE")
            == a1.get("a3_only")),
        "unexplained == 0": a1.get("unexplained") == 0,
    }

    hasse = [v for v in hist if abs(v) > 3]
    log = {
        "gate": "src05_frobenius_at_three",
        "what_a3_is": ("the trace of Frobenius at p=3, NOT the Weierstrass "
                       "coefficient a_3. Settled from the package's own columns: "
                       "14a1 records a3=-2 beside projective_point_count_at_3=6, "
                       "and 3+1-6 = -2"),
        "arithmetic": "exhaustive counting over F_3 and exact integers; no float",
        "counts": {
            "removed_curves_in_census": len(rows),
            "a_invariants_found": len(rows) - len(missing_ainvs),
            "projective_counts_recomputed": len(rows) - len(missing_ainvs),
            "projective_count_mismatches": len(count_mismatch),
            "nonsingular_count_mismatches": len(nonsing_mismatch),
            "curves_with_good_reduction_at_3": good_reduction,
            "a3_mismatches": len(a3_mismatch),
            "ecdata_aplist_disagreements": len(aplist_mismatch),
            "histogram_buckets_disagreeing": len(hist_diff),
            "values_outside_the_hasse_range": len(hasse),
            "curves_with_bad_reduction_at_3": len(rows) - good_reduction,
            "bad_reduction_a3_mismatches": len(bad_a3_mismatch),
            "bad_reduction_unclassified": len(unclassified_bad),
            "ecdata_tokens_not_numeric": sum(aplist_nonnumeric.values()),
            "ecdata_tokens_compared": len(rows) - sum(aplist_nonnumeric.values()),
        },
        "recomputed_a3_histogram": {str(k): hist[k] for k in sorted(hist)},
        "stored_a3_histogram": {str(k): stored_hist[k] for k in sorted(stored_hist)},
        "histogram_disagreements": hist_diff,
        "failure_class_distribution": dict(failure_classes),
        "bad_reduction_at_3_by_nonsingular_count": {
            str(k): v for k, v in sorted(bad_reduction_types.items())},
        "reduction_type_key": {"2": "split multiplicative, a_3 = +1",
                               "3": "additive, a_3 = 0",
                               "4": "non-split multiplicative, a_3 = -1"},
        "ecdata_nonnumeric_tokens_seen": dict(aplist_nonnumeric),
        "bad_reduction_a3_mismatches": bad_a3_mismatch[:20],
        "bad_reduction_unclassified": unclassified_bad[:20],
        "accounting_identities": accounting,
        "projective_count_mismatches": count_mismatch[:20],
        "nonsingular_count_mismatches": nonsing_mismatch[:20],
        "a3_mismatches": a3_mismatch[:20],
        "ecdata_aplist_disagreements": aplist_mismatch[:20],
        "curves_with_no_a_invariants": missing_ainvs[:20],
        "hasse_note": (
            "|a_3| <= 2*sqrt(3) < 4, so a_3 lies in {-3..3}. Any recomputed "
            "value outside that range would be an error in this gate, not a "
            "finding about the data."),
        "ok": (not count_mismatch and not nonsing_mismatch and not a3_mismatch
               and not aplist_mismatch and not hist_diff and not missing_ainvs
               and not hasse and not bad_a3_mismatch and not unclassified_bad
               and all(accounting.values())),
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    c = log["counts"]
    print(f"  removed curves                     : {c['removed_curves_in_census']:>7,}")
    print(f"  F_3 projective counts recomputed   : {c['projective_counts_recomputed']:>7,}"
          f"   mismatches {c['projective_count_mismatches']}")
    print(f"  nonsingular counts recomputed      : {c['projective_counts_recomputed']:>7,}"
          f"   mismatches {c['nonsingular_count_mismatches']}")
    print(f"  good reduction at 3                : {c['curves_with_good_reduction_at_3']:>7,}")
    print(f"  bad reduction at 3                 : {c['curves_with_bad_reduction_at_3']:>7,}"
          f"   a_3 mismatches {c['bad_reduction_a3_mismatches']}"
          f"   unclassified {c['bad_reduction_unclassified']}")
    print(f"  a_3 = 4 - #E(F_3) vs stored        : {'':>7}   mismatches {c['a3_mismatches']}")
    print(f"  vs ecdata's own aplist token       : {'':>7}   disagreements {c['ecdata_aplist_disagreements']}")
    print()
    print("  a_3 histogram")
    for k in sorted(set(stored_hist) | set(hist)):
        s, m = stored_hist.get(k, 0), hist.get(k, 0)
        flag = "  <-- DIFFERS" if s != m else ""
        print(f"    a_3 = {k:>2} : stored {s:>5,}   recomputed {m:>5,}{flag}")
    print()
    for k, v in accounting.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
