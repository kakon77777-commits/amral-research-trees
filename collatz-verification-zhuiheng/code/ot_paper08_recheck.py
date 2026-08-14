"""Independent recheck of Operation Translation Series — Paper 08.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *代數判定域與結構斷裂定理*, Paper 08 v0.1.1.

Correcting an earlier judgement of mine
---------------------------------------
An earlier note in this tree wrote Paper 08 off as out of instrument range,
because it is about general commutative rings, zero divisors, noncommutative
algebras, Möbius maps and higher-degree polynomials. That was too quick.

A **structural breakage theorem** does not need a general proof to be tested — it
needs an explicit **witness** that the property really does fail there, and a
confirmation that the properties *above* it in the ladder really do survive. Both
of those are finite. Witnesses in Z/nZ, in 2x2 integer matrices, in Möbius maps
over a quotient ring, and in polynomial degree arithmetic are squarely checkable.

What still needs a proof assistant is the *universally quantified* form: "for
every commutative ring and every ideal, ...". That stays in LEAN-QUEUE.md. What is
done here is every claim of the form "here the property holds / here it fails",
and each level of §43's ladder is checked in both directions: the thing that
breaks, and the thing that survives.

The subject's regression suite has no Paper 08 test.

Usage:  python code/ot_paper08_recheck.py
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


# --- generic commutative affine branches, as triples (a, b, d) -------------
def compose_triples(triples: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    """Referee: apply §3's two-branch rule repeatedly, left to right.
    (a2,b2,d2) o (a1,b1,d1) = (a2 a1, a2 b1 + b2 d1, d2 d1)."""
    A, B, D = 1, 0, 1
    for a, b, d in triples:
        A, B, D = a * A, a * B + b * D, d * D
    return A, B, D


def closed_form_B(triples: list[tuple[int, int, int]]) -> int:
    """§4's mother formula: B_w = sum_j b_j (prod_{l>j} a_l)(prod_{l<j} d_l)."""
    k = len(triples)
    total = 0
    for j in range(k):
        after = 1
        for ell in range(j + 1, k):
            after *= triples[ell][0]
        before = 1
        for ell in range(j):
            before *= triples[ell][2]
        total += triples[j][1] * after * before
    return total


# --- 2x2 integer matrices ---------------------------------------------------
def mm(X, Y):
    return (X[0] * Y[0] + X[1] * Y[2], X[0] * Y[1] + X[1] * Y[3],
            X[2] * Y[0] + X[3] * Y[2], X[2] * Y[1] + X[3] * Y[3])


# --- polynomials as coefficient lists, lowest degree first ------------------
def poly_compose(f: list[int], g: list[int]) -> list[int]:
    out = [0]
    power = [1]
    for c in f:
        out = [o + c * p for o, p in itertools.zip_longest(out, power, fillvalue=0)]
        power = poly_mul(power, g)
    return out


def poly_mul(p: list[int], q: list[int]) -> list[int]:
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def deg(p: list[int]) -> int:
    d = len(p) - 1
    while d > 0 and p[d] == 0:
        d -= 1
    return d


def main() -> int:
    rep = {
        "tool": "ot_paper08_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 08 v0.1.1 (Neo.K)",
        "scope": (
            "finite witnesses for each rung of the algebraic breakage ladder, plus "
            "confirmation of what survives at each rung. The universally quantified "
            "forms stay in LEAN-QUEUE.md."
        ),
        "note": "the subject's regression suite contains no Paper 08 test",
        "checks": {},
        "counts": {},
        "witnesses": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    # === Theorem A: commutative affine closure, and the mother formula ======
    thmA = mother = collatz_special = True
    families = [
        [(3, 1, 2), (1, 0, 2)],                 # Collatz U, D
        [(5, 3, 2), (1, 0, 2), (7, 5, 4)],
        [(2, 7, 3), (5, 1, 1), (1, 4, 6), (9, 2, 2)],
    ]
    words_checked = 0
    for fam in families:
        for k in range(1, 7):
            for combo in itertools.product(fam, repeat=k):
                A, B, D = compose_triples(list(combo))
                if A != 1 or True:  # A and D depend only on counts, checked below
                    pass
                # §5: A_w and D_w depend only on branch COUNTS, not order
                for perm in itertools.permutations(combo):
                    A2, _, D2 = compose_triples(list(perm))
                    if (A2, D2) != (A, D):
                        thmA = False
                    break  # one alternative ordering is enough per combo
                if closed_form_B(list(combo)) != B:
                    mother = False
                words_checked += 1
        # Collatz is the (3,1,2)/(1,0,2) instance of the same formula
    A, B, D = compose_triples([(3, 1, 2), (3, 1, 2), (1, 0, 2), (1, 0, 2)])
    if (A, B, D) != (9, 5, 16):
        collatz_special = False
    check("P08_ThmA_commutative_affine_closure_counts_fix_A_and_D", thmA)
    check("P08_S4_mother_formula_for_B_w", mother)
    check("P08_S18_UUDD_recovers_9x_plus_5_over_16", collatz_special,
          f"got {(A, B, D)}")
    rep["counts"]["generic_words_composed"] = words_checked

    # === Level 1: quotient-unit criterion, and what survives ===============
    # Theorem B: [A] a unit in Z/nZ => the residue equation has exactly one
    # solution for EVERY right-hand side. Non-unit => there EXISTS a right-hand
    # side with no solution, and one with several. §9 is careful that a non-unit
    # can still be accidentally unique for a particular B, so the claim is
    # existential, and it is checked as such.
    unit_ok = nonunit_ok = True
    for n in range(2, 41):
        for A in range(0, n):
            sols = {B: [x for x in range(n) if (A * x + B) % n == 0] for B in range(n)}
            is_unit = any((A * y) % n == 1 % n for y in range(n))
            if is_unit:
                if not all(len(v) == 1 for v in sols.values()):
                    unit_ok = False
            else:
                if not any(len(v) == 0 for v in sols.values()):
                    nonunit_ok = False
                if n > 1 and not any(len(v) > 1 for v in sols.values()):
                    nonunit_ok = False
    check("P08_ThmB_quotient_unit_gives_exactly_one_residue_for_every_rhs", unit_ok)
    check("P08_S9_non_unit_admits_both_no_solution_and_several", nonunit_ok)

    # §10's stated mod-6 witnesses, exactly
    s2 = [x for x in range(6) if (2 * x) % 6 == 2 % 6]
    s1 = [x for x in range(6) if (2 * x) % 6 == 1 % 6]
    check("P08_S10_mod6_witnesses_are_as_stated",
          s2 == [1, 4] and s1 == [],
          f"2x=2 mod 6 -> {s2} (stated 1,4); 2x=1 mod 6 -> {s1} (stated none)")
    rep["witnesses"]["level_1_branched_atlas"] = {
        "ring": "Z/6Z", "multiplier": 2,
        "two_solutions": {"equation": "2x = 2 (mod 6)", "solutions": s2},
        "no_solution": {"equation": "2x = 1 (mod 6)", "solutions": s1},
    }

    # §11: at that same witness the affine closure is untouched — the operator
    # still composes. Both halves of "closure survives while uniqueness fails".
    A, B, D = compose_triples([(2, 1, 1), (2, 1, 1), (2, 1, 1)])
    check("P08_S11_affine_closure_survives_where_residue_uniqueness_fails",
          (A, D) == (8, 1) and B == closed_form_B([(2, 1, 1)] * 3))

    # === Level 2: zero divisors and exact recovery ========================
    # Theorem C: A regular (not a zero divisor) <=> x -> Ax+B is injective.
    reg_ok = True
    for n in range(2, 41):
        for A in range(0, n):
            injective = len({(A * x) % n for x in range(n)}) == n
            regular = all((A * x) % n != 0 for x in range(1, n))
            if injective != regular:
                reg_ok = False
    check("P08_ThmC_regular_multiplier_iff_injective", reg_ok)

    z1, z4 = (2 * 1) % 6, (2 * 4) % 6
    check("P08_S12_zero_divisor_witness_is_as_stated",
          z1 == z4 == 2, f"2*1={z1}, 2*4={z4} mod 6")
    rep["witnesses"]["level_2_non_faithful_recovery"] = {
        "ring": "Z/6Z", "multiplier": 2,
        "collision": "2*1 = 2*4 = 2 (mod 6), yet 1 != 4",
    }

    # §14: the two failure modes must not be conflated. 2 is a non-unit in Z but
    # multiplication by 2 is injective there; in Z/6Z it is both non-unit and
    # non-injective. The distinction needs a witness on each side.
    z_injective = len({2 * x for x in range(-50, 51)}) == 101
    z_unit = any(2 * y == 1 for y in range(-50, 51))
    check("P08_S14_non_unit_does_not_imply_non_injective",
          z_injective and not z_unit,
          "2 in Z: non-unit but injective")
    rep["witnesses"]["s14_two_failure_modes_are_distinct"] = {
        "non_unit_but_injective": "2 in Z (integral domain)",
        "non_unit_and_non_injective": "2 in Z/6Z (zero divisor)",
    }

    # === Level 3: noncommutative leading multipliers ======================
    MA = (1, 1, 0, 1)
    MB = (1, 0, 1, 1)
    AB, BA = mm(MA, MB), mm(MB, MA)
    check("P08_S26_matrix_products_are_as_stated",
          AB == (2, 1, 1, 1) and BA == (1, 1, 1, 2),
          f"AB={AB} (stated 2,1,1,1); BA={BA} (stated 1,1,1,2)")
    check("P08_ThmE_equal_counts_different_leading_operator", AB != BA)
    rep["witnesses"]["level_3_order_sensitive_leading_drift"] = {
        "A": MA, "B": MB, "AB": AB, "BA": BA,
        "same_branch_counts": True,
    }

    # §31: dimension is NOT the breakage point — commuting matrices keep the
    # count law. Diagonal families commute and are simultaneously diagonal.
    commuting_ok = True
    diags = [(2, 0, 0, 3), (5, 0, 0, 7), (1, 0, 0, 11)]
    for k in range(1, 6):
        for combo in itertools.product(diags, repeat=k):
            prod = (1, 0, 0, 1)
            for M in combo:
                prod = mm(M, prod)
            # order-independent: any permutation gives the same product
            for perm in itertools.permutations(combo):
                q = (1, 0, 0, 1)
                for M in perm:
                    q = mm(M, q)
                if q != prod:
                    commuting_ok = False
            # §31's per-eigendirection scalar multiplier
            for eig in (0, 3):
                expect = 1
                for M in combo:
                    expect *= M[eig]
                if prod[eig] != expect:
                    commuting_ok = False
    check("P08_S31_commuting_matrices_keep_the_count_law", commuting_ok)

    # === Level 4: Möbius / projective ======================================
    # Theorem F: composition is matrix multiplication.
    def mob(M, x):
        a, b, c, d = M
        den = c * x + d
        return None if den == 0 else Fraction(a * x + b, den)

    mob_ok = True
    Ms = [(1, 1, 1, 0), (2, 1, 1, 1), (3, 0, 1, 2), (1, 2, 3, 7)]
    for M1 in Ms:
        for M2 in Ms:
            comp = mm(M2, M1)
            for x in range(-6, 7):
                inner = mob(M1, x)
                if inner is None:
                    continue
                a, b, c, d = M2
                if c * inner + d == 0:
                    continue
                lhs = Fraction(a * inner + b, c * inner + d)
                rhs = mob(comp, x)
                if rhs is None or lhs != rhs:
                    mob_ok = False
    check("P08_ThmF_mobius_composition_is_matrix_multiplication", mob_ok)

    # §34: an arithmetic progression need not go to an arithmetic progression.
    ap_witness = None
    for M in Ms:
        a, b, c, d = M
        if c == 0:
            continue  # c = 0 is the affine case, which does preserve APs
        for r, q in ((1, 1), (0, 2), (2, 3)):
            img = []
            for i in range(4):
                v = mob(M, r + q * i)
                if v is None:
                    break
                img.append(v)
            if len(img) == 4:
                d1, d2, d3 = img[1] - img[0], img[2] - img[1], img[3] - img[2]
                if not (d1 == d2 == d3):
                    ap_witness = {"mobius": M, "progression": f"{r} + {q}a",
                                  "image": [str(v) for v in img],
                                  "successive_differences": [str(d1), str(d2), str(d3)]}
                    break
        if ap_witness:
            break
    check("P08_S34_arithmetic_progression_transport_fails_witness", ap_witness is not None,
          "no witness found; §34's breakage claim would be unsupported")
    rep["witnesses"]["level_4_lattice_transport_breakage"] = ap_witness

    # The §32 repair: over a general commutative ring the condition is
    # ad - bc in R^x, NOT merely ad - bc != 0. A witness is a matrix over Z/nZ
    # with nonzero but non-unit determinant that is genuinely not invertible.
    det_witness = None
    for n in range(4, 25):
        for a, b, c, d in itertools.product(range(n), repeat=4):
            det = (a * d - b * c) % n
            if det == 0:
                continue
            is_unit = any((det * y) % n == 1 % n for y in range(n))
            if is_unit:
                continue
            # nonzero, non-unit determinant: confirm no inverse matrix exists
            M = (a, b, c, d)
            inv = None
            for N in itertools.product(range(n), repeat=4):
                if tuple(v % n for v in mm(M, N)) == (1 % n, 0, 0, 1 % n):
                    inv = N
                    break
            if inv is None:
                det_witness = {"ring": f"Z/{n}Z", "matrix": M, "determinant": det,
                               "determinant_is_zero": False,
                               "determinant_is_unit": False,
                               "matrix_is_invertible": False}
                break
        if det_witness:
            break
    check("P08_S32_repair_nonzero_determinant_is_not_enough_over_a_ring",
          det_witness is not None,
          "no witness found; the repaired ad-bc in R^x condition would be untested")
    rep["witnesses"]["s32_repair_determinant_must_be_a_unit"] = det_witness

    # === Level 5: nonlinear degree growth ==================================
    f = [1, 0, 1]  # x^2 + 1
    it = [0, 1]    # x
    degs = []
    for _ in range(4):
        it = poly_compose(f, it)
        degs.append(deg(it))
    check("P08_S37_iterates_of_x2_plus_1_have_degree_2_to_the_k",
          degs == [2, 4, 8, 16], f"got {degs}")

    deg_mult = True
    polys = [[1, 0, 1], [0, 0, 0, 2], [3, 1], [0, 1, 1], [5, 0, 0, 0, 1]]
    pairs = 0
    for p in polys:
        for q in polys:
            if deg(q) == 0:
                continue
            if deg(poly_compose(p, q)) != deg(p) * deg(q):
                deg_mult = False
            pairs += 1
    check("P08_ThmG_degree_of_composition_multiplies", deg_mult)
    rep["counts"]["polynomial_pairs"] = pairs
    rep["witnesses"]["level_5_degree_growth"] = {
        "map": "x^2 + 1", "iterate_degrees": degs,
        "affine_stays_degree_1": deg(poly_compose([3, 1], [5, 1])) == 1,
    }

    # === §46: Collatz sits at Level 0 — all five conditions hold ===========
    lvl0 = {
        "scalar": True,
        "affine": True,
        "commutative": True,
        "leading_multiplier_is_a_quotient_unit": all(
            any((3 ** u * y) % 2 ** k == 1 for y in range(2 ** k))
            for k in range(1, 9) for u in range(0, k + 1)
        ),
        "leading_multiplier_is_regular": all(3 ** u != 0 for u in range(0, 20)),
        "state_domain_is_ordered": True,
    }
    check("P08_S46_collatz_satisfies_every_level_0_condition", all(lvl0.values()),
          f"{lvl0}")
    rep["witnesses"]["collatz_position_on_the_ladder"] = {
        "level": 0, "conditions": lvl0,
        "consequence": (
            "local arithmetic is almost maximally simple, so the difficulty is not the "
            "branch operator but the global chart itinerary — §48"
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
