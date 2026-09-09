"""Gate 21 — the two-witness certificate (T1)–(T7) and its density formula, on 696.e1.

數學戰士「墜衡」 / AMRAL Research Lab.

`30_Two_Witness_Criterion_v0.1` generalises the 696.e1 result into a reusable
sufficient criterion: a finite certificate (T1)–(T7) on a non-semistable curve,
a Chebotarev support set 𝒫_E, and an explicit density

    δ(𝒫_E) = [L_E ∩ K_E : Q] / (3·[K_E : Q]),

where L_E is the Galois closure of the 2-division cubic and

    K_E = Q(ζ₈, √(ℓ*) : ℓ | N_E odd),   ℓ* = (−1)^{(ℓ−1)/2}·ℓ.

Corollary 5.1 instantiates it at 696.e1 with [K_E:Q] = 16, [L_E ∩ K_E : Q] = 2
and δ = 1/24.

WHAT IS EXACTLY COMPUTABLE HERE, AND IS. K_E is multiquadratic, so its degree is
2^r with r the F₂-rank of the exponent vectors of the squarefree parts — over the
"primes" {−1} ∪ {rational primes}. That is linear algebra over F₂, not an
estimate. The same rank decides whether the quadratic resolvent Q(√disc f_E) lies
inside K_E, which is what e_E measures. Both are done here in exact integer
arithmetic, and the density follows.

WHY THAT MATTERS BEYOND ONE NUMBER. RUN-015 found that 𝒫's stated congruence form
carries a redundant condition — (q/29) = 1 follows from the other two. This
criterion explains it: the 3-cycle condition already forces Frobenius trivial on
the quadratic resolvent, which sits inside K_E, so the two Chebotarev conditions
**overlap in a subgroup of index e_E**. The redundancy is not an oversight in the
theorem; it is exactly the factor e_E = 2 that makes the density 1/24 instead of
1/48. RUN-009 measured that factor, RUN-015 measured the redundancy, and this is
the statement that ties them together.

THE CONDITIONS THAT CAN BE CHECKED, AND THOSE THAT CANNOT. (T2)–(T5) are
arithmetic and are checked here against the earlier gates. (T1) is checked
except for the Manin constant and the cited BSD(E,2). (T6) and (T7) are checked
as far as X₀(n) reaches — degrees 2, 3, 5, 7 — and the remaining Mazur degrees
are named, not assumed.

Usage:  python code/src21_two_witness_certificate.py
"""

from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src21-two-witness.json"

CURVE = [0, 1, 0, 8, -16]                 # 696.e1
CONDUCTOR = 696
MAZUR_DEGREES = (2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163)
COVERED = (2, 3, 5, 7)


def squarefree_part(n: int) -> int:
    """The squarefree kernel of n, sign kept."""
    sign = -1 if n < 0 else 1
    n = abs(n)
    out, d = 1, 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e % 2:
            out *= d
        d += 1
    if n > 1:
        out *= n
    return sign * out


def exponent_vector(d: int, coords: list[int]) -> list[int]:
    """d, squarefree, as an F₂ vector over coords = [-1, p1, p2, …]."""
    vec = [0] * len(coords)
    m = d
    if m < 0:
        vec[0] = 1
        m = -m
    for i, p in enumerate(coords[1:], start=1):
        if m % p == 0:
            vec[i] = 1
            m //= p
    return vec if m == 1 else None


def f2_rank(vectors: list[list[int]]) -> int:
    rows = [v[:] for v in vectors]
    n = len(rows[0]) if rows else 0
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                rows[i] = [(a ^ b) for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def in_span(target: list[int], vectors: list[list[int]]) -> bool:
    return f2_rank(vectors + [target]) == f2_rank(vectors)


def star(ell: int) -> int:
    return ell if ell % 4 == 1 else -ell


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    b2, b4, b6, b8, disc = anchor.b_invariants(CURVE)
    cond_primes = [p for p in (2, 3, 29) if CONDUCTOR % p == 0]
    odd_bad = [p for p in cond_primes if p != 2]

    # ---- K_E and its degree, by F₂ rank -----------------------------------
    generators = [-1, 2] + [star(ell) for ell in odd_bad]   # ζ₈ gives √−1, √2
    coords = [-1] + sorted({p for g in generators
                            for p in _primes_of(abs(g))} | set(odd_bad) | {2})
    vectors = [exponent_vector(squarefree_part(g), coords) for g in generators]
    if any(v is None for v in vectors):
        raise SystemExit("a generator did not factor over the coordinate primes")
    rank = f2_rank(vectors)
    degree_K = 2 ** rank

    # ---- the quadratic resolvent, and e_E ---------------------------------
    cubic = [b6, 2 * b4, b2, 4]                 # 4x³ + b₂x² + 2b₄x + b₆
    d, c, bb, a = cubic
    disc_cubic = (18 * a * bb * c * d - 4 * bb ** 3 * d + bb * bb * c * c
                  - 4 * a * c ** 3 - 27 * a * a * d * d)
    resolvent = squarefree_part(disc_cubic)
    res_vec = exponent_vector(resolvent, coords)
    inside = res_vec is not None and in_span(res_vec, vectors)
    e_E = 2 if inside else 1
    density = Fraction(e_E, 3 * degree_K)

    # ---- the certificate conditions ---------------------------------------
    red = {p: tate.reduction_data(CURVE, p, want_c=True) for p in cond_primes}
    j = x0n.j_invariant(CURVE)
    fac = x0n.factorise(j.denominator) if j.denominator > 1 else {}
    isogeny = {n: x0n.rational_points(j, n, fac) for n in COVERED}

    torsion2 = bool(isogeny[2])
    conditions = {
        "T1 partial — E(Q)[2] = 0": not torsion2,
        "T1 partial — Δ_E < 0": disc < 0,
        "T1 partial — analytic rank 0": "verified in RUN-014 (w = +1, "
                                        "L(E,1) = 1.6317… ≠ 0)",
        "T1 partial — ord_2 L^alg(E,1) = 0": ("L/Ω = 1 exactly (RUN-014), and "
                                              "ord_2(1) = 0"),
        "T1 not checked": ["the Manin constant is odd", "BSD(E,2) is known — "
                           "cited from Creutz–Miller"],
        "T2 — f_E irreducible with Galois group S₃": {
            "disc_cubic": disc_cubic,
            "squarefree_resolvent": resolvent,
            "not_a_square": resolvent != 1,
            "verified_in": "RUN-009",
        },
        "T3 — the only additive prime is 2": {
            str(p): red[p]["kodaira"] for p in cond_primes},
        "T4 — 3 multiplicative with v₃(Δ) = 1": (
            red[3]["kodaira"].startswith("I") and not red[3]["kodaira"].endswith("*")
            and red[3]["v_disc"] == 1),
        "T5 — λ = 29 nonsplit multiplicative with v₂₉(Δ) = 1": (
            red[29].get("split_multiplicative") is False
            and red[29]["v_disc"] == 1),
        "T6/T7 — no rational isogeny, as far as X₀(n) reaches": {
            str(n): (None if isogeny[n] is None else bool(isogeny[n]))
            for n in COVERED},
        "T6/T7 degrees not covered": [n for n in MAZUR_DEGREES
                                      if n not in COVERED],
    }

    # ---- the congruence form, and where the redundancy comes from ---------
    members = [q for q in anchor.sieve(4000)
               if q % 24 == 1 and q != 29 and ph2.legendre(29, q) == 1
               and ph2.cubic_root_count(ph2.F2, q) == 0]
    without_29 = [q for q in anchor.sieve(4000)
                  if q % 24 == 1 and q != 29
                  and ph2.cubic_root_count(ph2.F2, q) == 0]

    log = {
        "gate": "src21_two_witness_certificate",
        "subject": ("30_Two_Witness_Criterion_v0.1 — the certificate (T1)–(T7), "
                    "the field K_E, and the density formula, at 696.e1"),
        "K_E": {
            "definition": "Q(ζ₈, √(ℓ*) : ℓ | N_E odd), ℓ* = (−1)^((ℓ−1)/2)·ℓ",
            "generators_as_square_roots": generators,
            "coordinate_primes": coords,
            "F2_rank": rank,
            "degree": degree_K,
            "document_states": 16,
            "agrees": degree_K == 16,
            "note": ("a multiquadratic field's degree is 2^r with r the F₂-rank "
                     "of the exponent vectors — exact linear algebra, not an "
                     "estimate"),
        },
        "quadratic_resolvent": {
            "disc_of_the_2_division_cubic": disc_cubic,
            "squarefree_part": resolvent,
            "lies_inside_K_E": inside,
            "e_E": e_E,
            "document_states": 2,
            "agrees": e_E == 2,
        },
        "density": {
            "formula": "e_E / (3·[K_E:Q])",
            "computed": str(density),
            "document_states": "1/24",
            "agrees": density == Fraction(1, 24),
            "measured_in_RUN_009": ("0.04162499 over primes below 2×10⁷, "
                                    "which is 0.99900 × 1/24"),
        },
        "why_RUN_015s_redundancy_is_this_e_E": {
            "finding": ("RUN-015 showed 𝒫's stated (q/29) = 1 follows from the "
                        "other two conditions"),
            "explanation": (
                "the 3-cycle condition forces Frobenius trivial on the quadratic "
                "resolvent Q(√%d), which lies inside K_E — so the two Chebotarev "
                "conditions overlap in a subgroup of index e_E. The redundancy "
                "IS the factor e_E = 2, and it is why the density is 1/24 rather "
                "than 1/48" % resolvent),
            "members_below_4000_with_the_condition": len(members),
            "members_below_4000_without_it": len(without_29),
            "same_set": members == without_29,
        },
        "certificate_conditions": conditions,
        "ok": (degree_K == 16 and e_E == 2 and density == Fraction(1, 24)
               and members == without_29
               and not torsion2 and disc < 0
               and red[2]["kodaira"] == "II*"
               and red[3]["v_disc"] == 1 and red[29]["v_disc"] == 1
               and red[29].get("split_multiplicative") is False
               and all(isogeny[n] is not None and not isogeny[n]
                       for n in COVERED)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    k = log["K_E"]
    print(f"  K_E = Q(√d : d ∈ {generators})")
    print(f"    F₂-rank {rank}  ⟹  [K_E:Q] = {degree_K}   document says "
          f"{k['document_states']}   agrees: {k['agrees']}")
    print(f"  quadratic resolvent Q(√{resolvent})  inside K_E: {inside}   "
          f"e_E = {e_E}   document says 2")
    print(f"  density = {e_E}/(3·{degree_K}) = {density}   document says 1/24   "
          f"agrees: {log['density']['agrees']}")
    print()
    print(f"  members of 𝒫 below 4,000 with the (q/29) condition   : "
          f"{len(members)}")
    print(f"  members of 𝒫 below 4,000 without it                  : "
          f"{len(without_29)}   same set: {members == without_29}")
    print()
    print("  certificate conditions:")
    print(f"    T1  E(Q)[2] = 0: {not torsion2}    Δ_E = {disc:,} < 0: "
          f"{disc < 0}")
    print(f"    T2  resolvent {resolvent} is not a square: {resolvent != 1}")
    print(f"    T3  reduction: " + "  ".join(
        f"{p}:{red[p]['kodaira']}" for p in cond_primes))
    print(f"    T4  v₃(Δ) = {red[3]['v_disc']}    T5  29 nonsplit: "
          f"{red[29].get('split_multiplicative') is False}, v₂₉(Δ) = "
          f"{red[29]['v_disc']}")
    print(f"    T6/T7 rational isogenies of degree 2,3,5,7: "
          f"{[bool(isogeny[n]) for n in COVERED]}   not covered: "
          f"{conditions['T6/T7 degrees not covered']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


def _primes_of(n: int):
    out, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
