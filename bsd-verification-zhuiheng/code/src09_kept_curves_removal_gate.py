"""Gate 09 — the curves the census KEPT, and the base's own selection criterion.

數學戰士「墜衡」 / AMRAL Research Lab.

Every gate in this line so far has audited the 4,062 curves the census REMOVED.
That is the half where evidence exists: each removed curve carries a row saying
why. RUN-007 named the other half and left it:

    an error in that direction is the one the census's own
    `algorithm1_all_removed_explained` check can never see: a missed isogeny
    wrongly *keeps* a curve, and a keep leaves no evidence to audit.

Algorithm 1 removes a base curve when it has a rational 3-, 5- or 7-isogeny, or
when |a₃| = 3 on its minimal model. 4,062 removals split 2,707 A3_ONLY / 1,353
ISOGENY_ONLY / 2 BOTH, with 0 unexplained. The contrapositive is a claim about
every surviving curve:

    **kept ⟹ no rational 3-, 5- or 7-isogeny, AND |a₃| ≠ 3.**

36,687 curves, 110,061 isogeny determinations, and not one of them has a row in
any results file. This gate checks all of them, on the whole removal criterion
rather than the isogeny half.

FOUR THINGS ARE MEASURED RATHER THAN READ.

1. The partition. kept ⊔ removed = the old base, recomputed here from the label
   files and the census CSV, not taken from the package's own `checks` block.

2. The discriminant factorisations. j's denominator reaches **48 digits** among
   the kept curves — past what Pollard rho reaches in reasonable time. It does
   not need to: den(j) divides Δ, and for a minimal model the primes of Δ are
   the primes of the conductor, which the package supplies as
   `discriminant_valuations`. So the factorisation is handed over — and this
   gate reconstructs ∏ p^{v_p} and compares it to the Δ it computes from the
   a-invariants itself, refusing the shortcut on any curve where the two differ.
   A supplied factorisation that has been checked is data; one that has not is
   an assumption wearing a number's clothes.

3. The isogenies, by RUN-007's X₀(n) criterion — complete, so a curve is decided
   yes or no rather than merely surviving a sieve.

4. a₃, straight off the minimal model.

A hit here is not a disagreement about bookkeeping. It is a curve the census's
own stated criterion should have removed and did not.

AND ONE CLAIM THAT IS NOT THE CENSUS'S AT ALL. The base is not "the curves of
conductor below 500,000" — it is 37,002 curves sourced `Zha16_no_2_tors` plus
3,747 sourced `CLZ20`. The first label is itself a testable assertion: a rational
2-isogeny is exactly a rational 2-torsion point, X₀(2) has the same shape as the
others (`j = (t+256)³/t²`, and `N(0) = 2²⁴` is again a pure power of n), and E[2]
is unchanged by a quadratic twist because χ_d lands in {±1} and −1 = +1 in F₂. So
the same machine decides it, over the whole 40,749 rather than the kept part,
reported per source. Verifying a census against a base means knowing what the
base is.

Usage:  python code/src09_kept_curves_removal_gate.py
"""

from __future__ import annotations

import collections
import csv
import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEPT_LABELS = x0n.PKG / "inputs" / "new" / "ec_labels_500k.txt"
OUT = ROOT / "data" / "gate-logs" / "src09-kept-curves.json"
LABEL_HEADER_LINES = 6
NS = (3, 5, 7)


def discriminant(ainvs: list[int]) -> int:
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6


def verify_discriminant_valuations(rec: dict) -> tuple[bool, int, list[int]]:
    """Does ∏ p^{v_p} reproduce the Δ computed from this record's a-invariants?

    Returns (agrees, rebuilt, usable_primes). On disagreement the prime list
    comes back empty: an unverified factorisation must not be used as one.
    """
    disc = discriminant(rec["ainvs"])
    vals = rec.get("discriminant_valuations") or {}
    rebuilt = 1
    for p, e in vals.items():
        rebuilt *= int(p) ** int(e)
    agrees = rebuilt == abs(disc)
    return agrees, rebuilt, ([int(p) for p in vals] if agrees else [])


def verify_partition(kept: set, removed: set, old: set) -> dict:
    """kept ⊔ removed = old base, recomputed rather than read."""
    return {
        "kept": len(kept),
        "removed": len(removed),
        "old_base": len(old),
        "overlap": len(kept & removed),
        "union_equals_old_base": (kept | removed) == old,
        "arithmetic_present_for_every_kept_curve": kept <= old,
        "ok": (not (kept & removed)) and (kept | removed) == old and kept <= old,
    }


def read_kept_labels() -> list[str]:
    out = []
    with KEPT_LABELS.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            if i < LABEL_HEADER_LINES:
                continue
            s = line.split(",")[0].strip()
            if s:
                out.append(s)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (KEPT_LABELS, x0n.CENSUS, x0n.ARITH):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")

    checks = x0n.self_check()
    print(f"  self-check: {len(checks)} known answers reproduced, 0 wrong")

    kept_list = read_kept_labels()
    kept = set(kept_list)
    removed = {r["curve_label"]
               for r in csv.DictReader(x0n.CENSUS.open(encoding="utf-8"))}
    recs = json.loads(x0n.ARITH.read_text(encoding="utf-8"))["records"]
    old = {r["curve_label"]: r for r in recs}

    partition = verify_partition(kept, removed, set(old))
    partition["kept_labels_read"] = len(kept_list)
    partition["kept_labels_unique"] = len(kept) == len(kept_list)
    if not (partition["ok"] and partition["kept_labels_unique"]):
        raise SystemExit(f"partition is not what the package describes: "
                         f"{json.dumps(partition, indent=2)}")
    print(f"  partition: {len(kept):,} kept ⊔ {len(removed):,} removed = "
          f"{len(old):,} old base, no overlap")

    found = {n: [] for n in NS}
    undecided = {n: [] for n in NS}
    special_j, a3_hits = [], []
    disc_val_ok = disc_val_bad = 0
    disc_val_disagreements = []
    fell_back_to_search = 0

    # The base's own selection criterion, which is a different claim from the
    # removal gate: 37,002 of the 40,749 carry source "Zha16_no_2_tors". A
    # rational 2-isogeny is exactly a rational 2-torsion point, so X₀(2) tests
    # that label directly — over the whole base, kept and removed alike.
    tors2 = {"by_source": collections.defaultdict(
        lambda: {"curves": 0, "has_2_torsion": 0, "undecided": 0}),
        "hits": []}

    for idx, label in enumerate(sorted(old)):
        if idx and idx % 2000 == 0:
            print(f"    … {idx:,}/{len(old):,}", file=sys.stderr)
        rec = old[label]
        inv = rec["ainvs"]
        is_kept = label in kept

        if is_kept and abs(inv[2]) == 3:
            a3_hits.append({"label": label, "a3": inv[2]})

        agrees, rebuilt, primes = verify_discriminant_valuations(rec)
        if agrees:
            disc_val_ok += 1
        else:
            disc_val_bad += 1
            if len(disc_val_disagreements) < 20:
                disc_val_disagreements.append(
                    {"label": label,
                     "computed_abs_disc": str(abs(discriminant(inv))),
                     "rebuilt_from_valuations": str(rebuilt)})

        j = x0n.j_invariant(inv)
        if j is None:
            continue
        if j in (Fraction(0), Fraction(1728)):
            special_j.append({"label": label, "j": str(j), "kept": is_kept})
            continue

        den = j.denominator
        fac = {} if den == 1 else (x0n.factorise_over(den, primes)
                                   if primes else None)
        if fac is None:
            fac = x0n.factorise(den)          # verified set did not cover it
            fell_back_to_search += 1

        src = rec.get("source") or "?"
        bucket = tors2["by_source"][src]
        bucket["curves"] += 1
        pts2 = x0n.rational_points(j, 2, fac)
        if pts2 is None:
            bucket["undecided"] += 1
        elif pts2:
            bucket["has_2_torsion"] += 1
            if len(tors2["hits"]) < 20:
                tors2["hits"].append({"label": label, "source": src,
                                      "kept": is_kept, "j": str(j)})

        if not is_kept:
            continue                # the removal gate is a claim about keeps

        for n in NS:
            pts = x0n.rational_points(j, n, fac)
            if pts is None:
                undecided[n].append(label)
            elif pts:
                found[n].append({"label": label, "j": str(j),
                                 "t": [str(x) for x in pts[:4]]})

    special_kept = [e for e in special_j if e["kept"]]
    decided = {n: len(kept) - len(undecided[n]) - len(special_kept)
               for n in NS}
    tors2["by_source"] = {k: dict(v) for k, v in tors2["by_source"].items()}
    zha = tors2["by_source"].get("Zha16_no_2_tors", {})
    counts = {
        "kept_curves": len(kept),
        "isogeny_determinations_attempted": 3 * len(kept),
        "KEPT_BUT_HAS_A_RATIONAL_ISOGENY": {f"n={n}": len(found[n]) for n in NS},
        "confirmed_no_isogeny": {f"n={n}": decided[n] - len(found[n])
                                 for n in NS},
        "undecided_search_cut": {f"n={n}": len(undecided[n]) for n in NS},
        "set_aside_j_is_0_or_1728": len(special_kept),
        "KEPT_BUT_ABS_A3_IS_3": len(a3_hits),
    }

    log = {
        "gate": "src09_kept_curves_removal_gate",
        "claim_under_test": (
            "Algorithm 1 removes a base curve for a rational 3/5/7-isogeny or "
            "for |a₃| = 3, and reports 0 unexplained removals — so every one of "
            "the 36,687 curves it KEPT must fail both conditions"),
        "why_this_direction_matters": (
            "the removed curves carry rows saying why; the kept ones carry "
            "nothing. A missed isogeny wrongly keeps a curve, and the package's "
            "own algorithm1_all_removed_explained check is structurally blind "
            "to it — it audits only what was removed"),
        "partition_recomputed_here": partition,
        "discriminant_valuations_cross_check": {
            "policy": (
                "den(j) divides Δ and for a minimal model Δ's primes are the "
                "conductor's, so the package's discriminant_valuations makes a "
                "48-digit denominator factorable without any search — but only "
                "after ∏p^v is reconstructed and compared to the Δ this gate "
                "computes from the a-invariants itself"),
            "agree": disc_val_ok,
            "disagree": disc_val_bad,
            "disagreements": disc_val_disagreements,
            "curves_needing_a_general_factorisation_instead": fell_back_to_search,
        },
        "self_check": {"results": checks},
        "counts": counts,
        "kept_but_has_isogeny": {f"n={n}": found[n][:20] for n in NS},
        "undecided": {f"n={n}": undecided[n][:20] for n in NS},
        "set_aside": special_j[:20],
        "base_selection_criterion_no_2_torsion": {
            "claim": (
                "37,002 of the 40,749 base curves carry source "
                "\"Zha16_no_2_tors\". A rational 2-isogeny is exactly a "
                "rational 2-torsion point, and X₀(2) decides it by the same "
                "complete method — so the label is testable, over the whole "
                "base rather than only the kept part"),
            "by_source": tors2["by_source"],
            "hits": tors2["hits"],
        },
        "kept_but_abs_a3_is_3": a3_hits[:20],
        "ok": ((not any(found[n] for n in NS)) and not a3_hits
               and not disc_val_bad
               and zha.get("has_2_torsion", 0) == 0
               and zha.get("undecided", 0) == 0),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print()
    print(f"  discriminant valuations: {disc_val_ok:,} agree, "
          f"{disc_val_bad:,} disagree   "
          f"(general factorisation needed on {fell_back_to_search:,})")
    print()
    for n in NS:
        print(f"  n = {n}   KEPT BUT HAS A RATIONAL ISOGENY : "
              f"{len(found[n]):>7,}")
        print(f"           confirmed no isogeny            : "
              f"{decided[n] - len(found[n]):>7,}")
        print(f"           undecided                       : "
              f"{len(undecided[n]):>7,}")
    print()
    print(f"  set aside (j = 0 or 1728)  : {len(special_kept):>7,}")
    print(f"  KEPT BUT |a₃| = 3          : {len(a3_hits):>7,}")
    print()
    print("  base selection criterion — rational 2-torsion, by source:")
    for src, v in sorted(tors2["by_source"].items()):
        print(f"    {src:22s} {v['curves']:>7,} curves   "
              f"has 2-torsion: {v['has_2_torsion']:>6,}   "
              f"undecided: {v['undecided']:,}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
