"""Gate 04 — recompute the arithmetic the Phase 1 census sits on.

數學戰士「墜衡」 / AMRAL Research Lab.

Phase 1's census is built on a curve-arithmetic table extracted from John
Cremona's `ecdata`: 40,749 base curves with a-invariants, conductor,
discriminant, discriminant valuations, rank and torsion order. Every count the
sub-line reports is downstream of that table being right.

The package's own README grades its headline figure `DIRECT_PRIMARY_SOURCE` —
taken from the official output and consistency-audited, **not independently
re-derived**, with only 2 curves and 28 twists recomputed. This gate takes the
other side of that: it recomputes, from the a-invariants alone, quantities the
table also states, and compares.

FOUR CHECKS, and each is exact integer arithmetic — no floating point anywhere,
because every quantity here is an integer and a float would be answering a
different question.

  1. **Discriminant from a-invariants.** Δ = −b₂²b₈ − 8b₄³ − 27b₆² + 9b₂b₄b₆,
     from (a₁,a₂,a₃,a₄,a₆) alone. The table's stored Δ is never read until the
     comparison.
  2. **Discriminant valuations.** v_p(Δ) recomputed by exact division, against
     the table's stored valuations.
  3. **Conductor primes ⊆ discriminant primes.** A prime of bad reduction
     divides the discriminant; the reverse can fail, so only one direction is a
     theorem and only that direction is checked.
  4. **Rank is constant on an isogeny class.** Phase 0 doc 01 §6 asserts it —
     "弱 BSD 的 rank 與 $L$-函數在 isogeny class 中保持一致". Cremona labels
     carry the class (`14a1` → conductor 14, class `a`), so it is directly
     measurable here rather than taken on trust.

WHAT A MISMATCH WOULD MEAN. Not that the mathematics is wrong — that the table
this sub-line reasons over disagrees with itself, which is a different and more
immediately actionable thing.

Usage:  python code/src04_curve_arithmetic_recompute.py
"""

from __future__ import annotations

import collections
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = (pathlib.Path("D:/我的研究/學術討論/論文/數學/BSD")
        / "BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12"
        / "inputs" / "metadata" / "old_base_curve_arithmetic.json")
OUT = ROOT / "data" / "gate-logs" / "src04-curve-arithmetic.json"

LABEL = re.compile(r"^(\d+)([a-z]+)(\d+)$")


def discriminant(a1: int, a2: int, a3: int, a4: int, a6: int) -> int:
    """Δ of the Weierstrass model, in exact integers."""
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6


def valuation(n: int, p: int) -> int:
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    if not DATA.exists():
        raise SystemExit(
            f"curve arithmetic table not found: {DATA}\n"
            "This gate recomputes a table it does not create; without it there "
            "is nothing to compare and a green result would mean nothing.")

    doc = json.loads(DATA.read_text(encoding="utf-8"))
    records = doc["records"]

    disc_mismatch, val_mismatch, cond_not_dividing = [], [], []
    unparsed_label, no_rank = [], []
    classes: dict[tuple[int, str], set[int]] = collections.defaultdict(set)
    class_members: dict[tuple[int, str], list[str]] = collections.defaultdict(list)
    checked_disc = checked_val = checked_cond = 0

    for rec in records:
        a1, a2, a3, a4, a6 = rec["ainvs"]
        mine = discriminant(a1, a2, a3, a4, a6)
        checked_disc += 1
        if mine != rec["discriminant"]:
            disc_mismatch.append({"label": rec["curve_label"],
                                  "ainvs": rec["ainvs"],
                                  "stored": rec["discriminant"],
                                  "recomputed": mine})
            continue                       # valuations below would be moot

        for p_s, v_stored in rec.get("discriminant_valuations", {}).items():
            p = int(p_s)
            checked_val += 1
            v_mine = valuation(abs(mine), p)
            if v_mine != v_stored:
                val_mismatch.append({"label": rec["curve_label"], "p": p,
                                     "stored": v_stored, "recomputed": v_mine})

        for p in rec.get("conductor_primes", []):
            checked_cond += 1
            if mine % p != 0:
                cond_not_dividing.append({"label": rec["curve_label"], "p": p,
                                          "discriminant": mine})

        m = LABEL.match(rec["curve_label"])
        if not m:
            unparsed_label.append(rec["curve_label"])
            continue
        line = rec.get("evidence", {}).get("allcurves_line", "").split()
        # conductor class number [ainvs] rank torsion
        if len(line) >= 6 and line[-2].lstrip("-").isdigit():
            classes[(int(m.group(1)), m.group(2))].add(int(line[-2]))
            class_members[(int(m.group(1)), m.group(2))].append(rec["curve_label"])
        else:
            no_rank.append(rec["curve_label"])

    split_classes = {f"{n}{c}": sorted(r) for (n, c), r in classes.items()
                     if len(r) > 1}

    # A class holding one curve cannot disagree with itself. Measure how many
    # classes could have failed check 4 before reporting that none did — this
    # table is the census's BASE curves, one representative per class, so the
    # answer is expected to be zero and the check is then VACUOUS, not passing.
    sizes = collections.Counter(len(members) for members in class_members.values())
    testable = sum(n for size, n in sizes.items() if size > 1)

    log = {
        "gate": "src04_curve_arithmetic_recompute",
        "source_table": str(DATA),
        "provenance_of_the_table": doc.get("provenance", {}).get("method"),
        "ecdata_commit": doc.get("provenance", {}).get("ecdata_commit"),
        "arithmetic": "exact integers throughout; no floating point",
        "counts": {
            "curves_in_table": len(records),
            "discriminants_recomputed": checked_disc,
            "discriminant_mismatches": len(disc_mismatch),
            "valuations_recomputed": checked_val,
            "valuation_mismatches": len(val_mismatch),
            "conductor_prime_divisibility_checks": checked_cond,
            "conductor_primes_not_dividing_the_discriminant": len(cond_not_dividing),
            "isogeny_classes_seen": len(classes),
            "isogeny_classes_with_more_than_one_rank": len(split_classes),
            "isogeny_classes_with_more_than_one_curve": testable,
            "labels_that_did_not_parse": len(unparsed_label),
            "records_with_no_readable_rank": len(no_rank),
        },
        "discriminant_mismatches": disc_mismatch[:20],
        "valuation_mismatches": val_mismatch[:20],
        "conductor_primes_not_dividing_the_discriminant": cond_not_dividing[:20],
        "isogeny_classes_with_more_than_one_rank": split_classes,
        "isogeny_class_size_distribution": {str(k): v for k, v in sorted(sizes.items())},
        "check_4_verdict": (
            "VACUOUS" if testable == 0 else "measured"),
        "why_check_4_is_vacuous_here": (
            "this table is the census's BASE curves — one representative per "
            "isogeny class, every label ending in 1 — so no class holds two "
            "curves and none could have disagreed. Zero split classes is "
            "therefore not evidence that rank is constant on a class; it is the "
            "shape of the table. Testing doc 01 §6 needs a table carrying the "
            "whole class." if testable == 0 else
            "classes carrying more than one curve are present and were compared"),
        "what_check_4_tests": (
            "Phase 0 doc 01 §6 asserts rank is constant across an isogeny "
            "class. Cremona labels carry the class, so this is measured on "
            "every class present rather than assumed."),
        "one_direction_only": (
            "check 3 tests that every conductor prime divides the "
            "discriminant, which is a theorem. The converse is false — a "
            "prime can divide Δ with good reduction after a change of model — "
            "so it is not checked and its absence is not a gap."),
        # check 4 contributes nothing to `ok` when it is vacuous: a check that
        # could not have failed must not be able to make the gate pass.
        "ok": (not disc_mismatch and not val_mismatch and not cond_not_dividing
               and not split_classes and not unparsed_label),
        "checks_that_carried_evidence": 3 if testable == 0 else 4,
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    c = log["counts"]
    print(f"  curves in table                    : {c['curves_in_table']:>8,}")
    print(f"  discriminants recomputed from ainvs: {c['discriminants_recomputed']:>8,}"
          f"   mismatches {c['discriminant_mismatches']}")
    print(f"  valuations recomputed              : {c['valuations_recomputed']:>8,}"
          f"   mismatches {c['valuation_mismatches']}")
    print(f"  conductor-prime divisibility checks: {c['conductor_prime_divisibility_checks']:>8,}"
          f"   failures   {c['conductor_primes_not_dividing_the_discriminant']}")
    print(f"  isogeny classes                    : {c['isogeny_classes_seen']:>8,}"
          f"   with >1 curve {c['isogeny_classes_with_more_than_one_curve']}")
    print(f"  check 4 (rank constant on a class) : {log['check_4_verdict']}")
    if log["check_4_verdict"] == "VACUOUS":
        print("      every class holds exactly one curve, so none could disagree;")
        print("      zero split classes is the table's shape, not evidence.")
    if split_classes:
        print()
        print("  classes whose curves disagree on rank:")
        for k, v in list(split_classes.items())[:20]:
            print(f"    {k}: {v}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
