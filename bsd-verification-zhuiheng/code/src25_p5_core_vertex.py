"""Gate 25 — P5's norm-Selmer core vertex: the cube, and how special 397 and 991 are.

數學戰士「墜衡」 / AMRAL Research Lab.

`BSD_P5_Norm_Selmer_Core_Vertex_389a1_p11_v1.2` turns the localization matrix of
v1.1 into a Selmer-structure theorem. Its boxed conclusions are

    Sel^{N_397}   = F_11 (Q - 2P),      Sel^{N_991}   = F_11 (Q - 4P),
    Sel^{N_397,991} = 0,
    dimensions   2 -> 1,  2 -> 1,  1 ∩ 1 -> 0,
    cardinalities  121 -> 11 -> 1,

and §5 adds that the two rank-1 faces are transverse.

ALL OF THAT IS ONE DETERMINANT, AND THE GATE SAYS SO. Each localization row is
normalised to (1, k_ℓ), so for two directions the matrix is

    [[1, k_1], [1, k_2]]   with determinant   k_2 - k_1.

`det M_loc = 2` is `k_991 - k_397 = 4 - 2`. The vanishing of the doubly-modified
Selmer group, the transversality of the two faces, and `det(𝓑_N) ≠ 0` in
`v1.3` §3 are therefore **the same fact three times**, and none of the three is
independent evidence for either other. That is worth stating rather than letting
three boxed statements read as three confirmations.

HOW SPECIAL IS THE CHOSEN PAIR — measured rather than assumed. RUN-011 listed
the admissible directions below 20,000 and noted 397 and 991 are the two
smallest. It did not compute the pairwise matrices. A row can in principle have
shape (1, k), (0, 1) or (0, 0); over this range every surviving row turns out to
be (1, k) — measured, not assumed — and for two such rows the pair gives a core
vertex **exactly when k_ℓ ≠ k_ℓ'**. So the distribution of k decides every pair,
and it is reported alongside the count.

Usage:  python code/src25_p5_core_vertex.py
"""

from __future__ import annotations

import collections
import itertools
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src12_p5_localization as p5                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src25-p5-core-vertex.json"

P11 = 11
SCAN = 20_000


# --------------------------------------------------------------------------
# the Selmer cube, as exact linear algebra over F_11
# --------------------------------------------------------------------------

def kernel_line(row):
    """The kernel of one localization row acting on (a, b) ↦ a·r0 + b·r1.

    Returned as the pair (a, b) spanning it, normalised so that the entry the
    document writes as the coefficient of Q is 1 when it can be.
    """
    r0, r1 = row[0] % P11, row[1] % P11
    if r0 == 0 and r1 == 0:
        return None                                   # the whole plane
    if r0 == 0:
        return (1, 0)                                 # b = 0, spanned by P
    # a·r0 + b·r1 = 0 with r0 ≠ 0 → a = −b·r1/r0; take b = 1
    a = (-pow(r0, -1, P11) * r1) % P11
    return (a, 1)


def selmer_cube(rows: dict) -> dict:
    """dim Sel with no condition, with each one, and with both."""
    labels = sorted(rows)
    lines = {ell: kernel_line(rows[ell]) for ell in labels}
    r1, r2 = rows[labels[0]], rows[labels[1]]
    det = (r1[0] * r2[1] - r1[1] * r2[0]) % P11
    dims = {"empty": 2,
            str(labels[0]): 2 - (1 if any(x % P11 for x in r1) else 0),
            str(labels[1]): 2 - (1 if any(x % P11 for x in r2) else 0),
            "both": 0 if det else 1}
    return {
        "rows": {str(k): list(v) for k, v in rows.items()},
        "kernel_lines_as_(a,b)_in_aP_plus_bQ": {str(k): list(v) if v else None
                                                for k, v in lines.items()},
        "kernel_lines_as_written_by_the_document":
            {str(k): (f"Q - {(-v[0]) % P11}P" if v and v[1] == 1 else "P")
             for k, v in lines.items()},
        "determinant": det,
        "dimensions": dims,
        "cardinalities": [P11 ** dims["empty"], P11 ** dims[str(labels[0])],
                          P11 ** dims["both"]],
        "document_says": {
            "Sel_397": "F_11 (Q - 2P)", "Sel_991": "F_11 (Q - 4P)",
            "Sel_both": 0, "dimension_cube": "2 -> 1, 2 -> 1, 1 ∩ 1 -> 0",
            "cardinalities": "121 -> 11 -> 1", "det": 2,
        },
        "agrees": (det == 2 and dims == {"empty": 2, "397": 1, "991": 1, "both": 0}),
    }


def the_three_statements_are_one(rows: dict) -> dict:
    """§3's `Sel = 0`, §5's transversality, and v1.3 §3's `det(𝓑_N) ≠ 0`.

    All three are `det M_loc ≠ 0`, and with rows normalised to (1, k) that is
    `k_991 ≠ k_397`. Three boxed statements, one fact — recorded so that their
    agreement is not read as three confirmations.
    """
    labels = sorted(rows)
    ks = {ell: rows[ell][1] % P11 for ell in labels}
    normalised = all(rows[ell][0] % P11 == 1 for ell in labels)
    r1, r2 = rows[labels[0]], rows[labels[1]]
    det = (r1[0] * r2[1] - r1[1] * r2[0]) % P11
    # transversality: the two kernel lines are distinct
    l1, l2 = kernel_line(r1), kernel_line(r2)
    transverse = (l1[0] * l2[1] - l1[1] * l2[0]) % P11 != 0
    return {
        "rows_are_normalised_to_(1,k)": normalised,
        "k": {str(k): v for k, v in ks.items()},
        "det_equals_k_difference": det == (ks[labels[1]] - ks[labels[0]]) % P11,
        "selmer_both_vanishes": det != 0,
        "faces_are_transverse": transverse,
        "bockstein_determinant_nonzero_v1_3": det != 0,
        "all_three_agree": (det != 0) == transverse,
        "reading": ("the three are the same determinant. Their agreement is "
                    "arithmetic, not evidence — a gate that reported them as "
                    "three independent confirmations would be counting one "
                    "fact three times"),
    }


# --------------------------------------------------------------------------
# how special the chosen pair is
# --------------------------------------------------------------------------

def admissible_valuation(v: int) -> bool:
    """`11` must divide `#E(F_ℓ)` **exactly once**, not merely divide it.

    `v = 0` and `v ≥ 2` both fail, and for different reasons: at `v = 0` there
    is no 11-torsion to localise into, and at `v ≥ 2` the norm quotient is no
    longer one-dimensional so a single residue `k` does not describe the row.
    Split out as a predicate because it is otherwise untestable in practice —
    **19867 is the only prime below 20,000 with `v ≥ 2`**, so any drill fixture
    cheap enough to run per defect never reaches the branch.
    """
    return v == 1


def admissible_rows(scan: int = SCAN) -> dict:
    """Every admissible direction below `scan`, with its row — computed here.

    Admissible is v1.1's condition, recomputed rather than read: ℓ ≡ 1 (mod 11)
    so the degree-11 real cyclotomic subfield exists, ℓ ≠ 11 so the extension is
    tame, and 11 divides #E(F_ℓ) **exactly once** so the norm quotient is
    one-dimensional.

    TWO NOTES ON RUN-011, both about its own gate rather than about the corpus.

    First, its `usable` flag means "the row normalises to (1, k)", not "a row
    exists", and the three possible shapes are (1, k), (0, 1) and (0, 0). The
    exclusion it makes at ℓ = 19009 is **right in effect and incomplete in its
    stated reason**: its message stops at "P lands in 11·E(F_ℓ)", which alone
    would leave the row (0, 1) — a perfectly good condition — while what is
    actually true there is that **Q dies as well**, so the row is (0, 0) and the
    direction imposes no condition at all. Its `both_are_11_torsion: true` for
    that prime is likewise vacuous: the identity is 11-torsion. The shapes are
    therefore counted here rather than assumed away, so that "every row is
    (1, k)" is reported as a measurement over this range and not as a theorem.

    Second, RUN-011's `admissible` list counted 25 directions while its own row
    computation rejects one of them: ℓ = 19867 has v₁₁(#E(F_ℓ)) = 3, and the
    list's stated criterion asks only that 11 divide the order, not that it
    divide it once. The list and the row computation used different criteria.

    Rows are therefore computed here from `ec_mul` directly.
    """
    rows, skipped, kinds = {}, [], collections.Counter()
    for ell in range(2, scan):
        if ell % 11 != 1 or not p5.is_prime(ell):
            continue
        n = p5.npoints(ell)
        m, v = n, 0
        while m % P11 == 0:
            m //= P11
            v += 1
        if not admissible_valuation(v):
            skipped.append({"ell": ell, "why": f"v_11(#E(F_l)) = {v}, not 1"})
            continue
        A = p5.ec_mul(m, p5.P0, ell)
        B = p5.ec_mul(m, p5.Q0, ell)
        if A is not None:
            k = next((t for t in range(P11) if p5.ec_mul(t, A, ell) == B), None)
            if k is None:                              # pragma: no cover
                skipped.append({"ell": ell, "why": "m*Q is not a multiple of m*P"})
                continue
            rows[ell] = (1, k)
            kinds["(1, k)"] += 1
        elif B is not None:
            rows[ell] = (0, 1)                         # P dies, Q survives
            kinds["(0, 1)"] += 1
        else:
            skipped.append({"ell": ell,
                            "why": "both generators land in 11·E(F_l); the "
                                   "direction imposes no condition"})
            kinds["(0, 0)"] += 1
    return {"rows": rows, "skipped": skipped,
            "row_shapes": dict(kinds),
            "rows_not_normalisable_to_(1,k)": [e for e, r in rows.items()
                                               if r[0] % P11 == 0]}


def pair_scan(rows: dict) -> dict:
    """Every pair of admissible directions, and whether it is a core vertex.

    With rows normalised to (1, k) the determinant is k' − k, so a pair works
    exactly when the two directions give different k. The distribution of k is
    therefore the whole answer, and it is reported alongside the pair counts.
    """
    labels = sorted(rows)
    normalisable = [e for e in labels if rows[e][0] % P11 != 0]
    ks = {ell: rows[ell][1] % P11 for ell in normalisable}
    dist = collections.Counter(ks.values())
    good, bad, examples = 0, [], []
    for a, b in itertools.combinations(labels, 2):
        (r0, r1), (s0, s1) = rows[a], rows[b]
        det = (r0 * s1 - r1 * s0) % P11
        if det:
            good += 1
            if len(examples) < 5:
                examples.append({"pair": [a, b], "rows": [list(rows[a]),
                                                          list(rows[b])],
                                 "det": det})
        else:
            bad.append({"pair": [a, b], "rows": [list(rows[a]), list(rows[b])]})
    total = good + len(bad)
    return {
        "admissible_directions": len(labels),
        "directions": labels,
        "directions_with_a_(0,1)_row": [e for e in labels
                                        if rows[e][0] % P11 == 0],
        "k_per_direction": {str(k): v for k, v in ks.items()},
        "distribution_of_k": {str(k): v for k, v in sorted(dist.items())},
        "distinct_k_values": len(dist),
        "pairs_total": total,
        "pairs_giving_a_core_vertex": good,
        "pairs_that_degenerate": len(bad),
        "degenerate_pairs": bad[:10],
        "fraction_usable": good / total if total else None,
        "chosen_pair_397_991": {"k": [ks.get(397), ks.get(991)],
                                "det": ((ks.get(991, 0) - ks.get(397, 0)) % P11)},
        "reading": ("among rows of the form (1, k) a pair degenerates exactly "
                    "when the two k agree; a (0, 1) row pairs non-degenerately "
                    "with every (1, k) row, since that determinant is 1. So the "
                    "distribution of k over the normalisable directions decides "
                    "everything. 397 and 991 are the two smallest admissible "
                    "primes and they happen to differ; whether that is typical "
                    "is what the distribution answers"),
        "expected_degenerate_if_k_were_uniform": (
            len(list(itertools.combinations(normalisable, 2))) / P11
            if normalisable else None),
        "examples": examples,
    }


def main() -> int:
    rows_397_991 = {ell: tuple(p5.localization_row(ell)["row_normalised"])
                    for ell in (397, 991)}
    cube = selmer_cube(rows_397_991)
    one = the_three_statements_are_one(rows_397_991)
    adm = admissible_rows()
    scan = pair_scan(adm["rows"])

    log = {
        "gate": "src25 — P5 norm-Selmer core vertex",
        "selmer_cube": cube,
        "three_statements_one_determinant": one,
        "how_special_is_the_chosen_pair": scan,
        # The overwhelming majority of skips are v_11 = 0 — primes that are
        # 1 mod 11 but whose point count is not divisible by 11 at all. Those
        # are summarised; anything else is kept in full, because a skip for any
        # other reason is a fact about the structure rather than about density.
        "directions_skipped": {
            "by_reason": dict(collections.Counter(
                "v_11 = 0" if s["why"].startswith("v_11(#E(F_l)) = 0")
                else s["why"] for s in adm["skipped"])),
            "not_merely_v_11_zero": [s for s in adm["skipped"]
                                     if not s["why"].startswith("v_11(#E(F_l)) = 0")],
        },
        "row_shapes": adm["row_shapes"],
        "corrections_to_RUN_011": {
            "usable_flag": ("src12's `usable` means the row normalises to "
                            "(1, k), not that a row exists. Its exclusion at "
                            "l = 19009 is right in effect but its stated reason "
                            "stops at P: what makes that direction vacuous is "
                            "that Q dies too, so the row is (0, 0) and no "
                            "condition is imposed. Its both_are_11_torsion flag "
                            "is vacuously true there, the identity being "
                            "11-torsion"),
            "admissible_count": ("RUN-011's log reports 25 admissible "
                                 "directions while its own row computation "
                                 "rejects l = 19867, where v_11(#E(F_l)) = 3. "
                                 "The list's criterion asks only that 11 divide "
                                 "the order; the row computation asks that it "
                                 "divide it once. This gate uses the second"),
            "corrected_count": len(adm["rows"]),
        },
        "ok": (cube["agrees"] and one["all_three_agree"]
               and one["det_equals_k_difference"]
               and scan["pairs_giving_a_core_vertex"] > 0),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print(f"  rows: {cube['rows']}   det = {cube['determinant']}")
    print(f"  kernel lines: {cube['kernel_lines_as_written_by_the_document']}")
    print(f"  dimensions {cube['dimensions']}   cardinalities "
          f"{cube['cardinalities']}   agrees: {cube['agrees']}")
    print()
    print(f"  det = k_991 - k_397: {one['det_equals_k_difference']}   "
          f"k = {one['k']}")
    print(f"    Sel_both = 0: {one['selmer_both_vanishes']}, faces transverse: "
          f"{one['faces_are_transverse']}, det(B_N) != 0: "
          f"{one['bockstein_determinant_nonzero_v1_3']} — one determinant, "
          f"three statements")
    print()
    print(f"  admissible directions below {SCAN:,}: "
          f"{scan['admissible_directions']}   row shapes {adm['row_shapes']}")
    if scan["directions_with_a_(0,1)_row"]:
        print(f"    rows NOT of the form (1, k): "
              f"{scan['directions_with_a_(0,1)_row']} — RUN-011's `usable` flag "
              f"drops these")
    print(f"    k distribution: {scan['distribution_of_k']}  "
          f"({scan['distinct_k_values']} distinct values)")
    print(f"    pairs: {scan['pairs_giving_a_core_vertex']}/{scan['pairs_total']} "
          f"give a core vertex ({scan['fraction_usable']:.1%}), "
          f"{scan['pairs_that_degenerate']} degenerate "
          f"(uniform k would give {scan['expected_degenerate_if_k_were_uniform']:.1f})")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
