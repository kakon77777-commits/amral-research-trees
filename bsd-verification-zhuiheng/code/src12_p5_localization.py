"""Gate 12 — the P5 sub-line's foundations for 389.a1 at p = 11, recomputed.

數學戰士「墜衡」 / AMRAL Research Lab.

The P5 line hangs everything on one curve and one prime, and its v1.1 certificate
on one 2×2 matrix over F₁₁:

    M_loc = [[1, 2], [1, 4]],   det = 2 ∈ F₁₁^×,

the images of the Mordell–Weil generators P = (0,0), Q = (1,0) under localization
at two "ramified directions" ℓ = 397 and ℓ = 991. Nonzero determinant is the whole
point: it is what makes the localization injective on E(Q)/11E(Q).

**The matrix is not read here. It is recomputed.** For a prime ℓ of good
reduction and L_ℓ/Q_ℓ totally tamely ramified of degree 11 (ℓ ≠ 11), the norm
quotient is E(Q_ℓ)/N E(L_ℓ) ≅ E(F_ℓ)/11 E(F_ℓ), so the localization of a global
point is just its reduction mod ℓ read in that quotient. With 11 ‖ #E(F_ℓ) the
quotient is cyclic of order 11, and for R ∈ E(F_ℓ) the class of R is captured by
m·R with m = #E(F_ℓ)/11 — zero exactly when R ∈ 11·E(F_ℓ). Each row is then
determined up to a unit (the choice of generator), so the ratio within a row and
the vanishing of the determinant are both well defined.

WHAT ELSE IS CHECKABLE, AND WHAT IS NOT.

Checkable: that P and Q lie on the curve; that the short model
Y² = X³ − 3024X + 46224 and the images P' = (12,108), Q' = (48,108) are what the
transformation actually produces; that E(Q)_tors is trivial; that 11 is good and
ordinary; that 397 and 991 are ≡ 1 (mod 11), so the degree-11 real cyclotomic
subfields exist, and tame since neither is 11; that 11 divides #E(F_ℓ) **exactly
once** at both, which is what makes the norm quotient one-dimensional rather than
two; and that the Kurihara/Kolyvagin condition a_ℓ ≡ ℓ + 1 (mod 11) holds.

And how special the two directions are: this gate scans every prime below 20,000
for the same condition, so "397 and 991" can be reported as a measured fact about
the admissible set rather than an unexplained pair.

NOT checkable here, and not claimed: **Ш(E/Q)[11] = 0**, which the P5 documents
carry as an *inherited* dependency and label as such. Sel₁₁(E/Q) ≅ (Z/11)² follows
from rank 2, trivial torsion and that vanishing — this gate supplies the first
two and takes no position on the third. Nor does it touch the comparison the whole
sub-line names as OPEN: the analytic leading term against the algebraic regulator.

Usage:  python code/src12_p5_localization.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src12-p5-localization.json"

AINVS = [0, 1, 1, -2, 0]                  # 389.a1, the smallest rank-2 curve
CONDUCTOR = 389
P0, Q0 = (0, 0), (1, 0)                   # the Mordell-Weil generators used by P5
P = 11                                    # the working prime
DIRECTIONS = (397, 991)                   # the ramified directions v1.1 uses
SCAN = 20_000


def legendre(a: int, p: int) -> int:
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)


def is_prime(v: int) -> bool:
    if v < 2:
        return False
    d = 2
    while d * d <= v:
        if v % d == 0:
            return False
        d += 1
    return True


def factor(v: int) -> dict[int, int]:
    v, out, d = abs(v), {}, 2
    while d * d <= v:
        while v % d == 0:
            out[d] = out.get(d, 0) + 1
            v //= d
        d += 1
    if v > 1:
        out[v] = out.get(v, 0) + 1
    return out


def on_curve(pt, ainvs=AINVS) -> bool:
    a1, a2, a3, a4, a6 = ainvs
    x, y = pt
    return y * y + a1 * x * y + a3 * y == x ** 3 + a2 * x * x + a4 * x + a6


def npoints(ell: int) -> int:
    a1, a2, a3, a4, a6 = (c % ell for c in AINVS)
    total = 1
    for x in range(ell):
        d = ((a1 * x + a3) ** 2
             + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % ell
        total += 1 + legendre(d, ell)
    return total


# ------------------------------------------------- group law over F_ell

def ec_add(A, B, ell):
    a1, a2, a3, a4, _ = AINVS
    if A is None:
        return B
    if B is None:
        return A
    x1, y1 = A
    x2, y2 = B
    if x1 == x2 and (y1 + y2 + a1 * x2 + a3) % ell == 0:
        return None
    if A == B:
        num = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) % ell
        den = (2 * y1 + a1 * x1 + a3) % ell
    else:
        num = (y2 - y1) % ell
        den = (x2 - x1) % ell
    lam = num * pow(den, -1, ell) % ell
    nu = (y1 - lam * x1) % ell
    x3 = (lam * lam + a1 * lam - a2 - x1 - x2) % ell
    y3 = (-(lam + a1) * x3 - nu - a3) % ell
    return (x3, y3)


def ec_mul(k, A, ell):
    R, B = None, A
    while k:
        if k & 1:
            R = ec_add(R, B, ell)
        B = ec_add(B, B, ell)
        k >>= 1
    return R


def localization_row(ell: int) -> dict:
    """The image of (P, Q) in E(F_ell)/11·E(F_ell), normalised to (1, k)."""
    n = npoints(ell)
    m, v = n, 0
    while m % P == 0:
        m //= P
        v += 1
    row = {"ell": ell, "point_count": n,
           "point_count_factored": {str(a): b for a, b in factor(n).items()},
           "v_11_of_point_count": v, "cofactor": m}
    if v != 1:
        row["usable"] = False
        row["why"] = ("the norm quotient is one-dimensional only when 11 divides "
                      "#E(F_ell) exactly once")
        return row
    A = ec_mul(m, P0, ell)
    B = ec_mul(m, Q0, ell)
    row["m_times_P"] = A
    row["m_times_Q"] = B
    row["both_are_11_torsion"] = (ec_mul(P, A, ell) is None
                                  and ec_mul(P, B, ell) is None)
    if A is None:
        row["usable"] = False
        row["why"] = "P lands in 11·E(F_ell); the row cannot be normalised to 1"
        return row
    k = next((t for t in range(P) if ec_mul(t, A, ell) == B), None)
    row["k_with_mQ_equals_k_mP"] = k
    row["row_normalised"] = [1, k]
    row["usable"] = k is not None
    return row


def short_model() -> dict:
    """The short Weierstrass model and the images of P and Q, derived here."""
    a1, a2, a3, a4, a6 = AINVS
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    A, B = -27 * c4, -54 * c6
    images = {}
    for name, (x, y) in (("P", P0), ("Q", Q0)):
        X = 36 * x + 3 * b2
        Y = 216 * y + 108 * a1 * x + 108 * a3
        images[name] = {"minimal_model": [x, y], "short_model": [X, Y],
                        "satisfies_short_model":
                            Y * Y == X ** 3 + A * X + B}
    return {"b2": b2, "c4": c4, "c6": c6, "disc": disc, "A": A, "B": B,
            "images": images}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    sm = short_model()
    c4, c6, disc = sm["c4"], sm["c6"], sm["disc"]
    short = {"A": sm["A"], "B": sm["B"],
             "document_states": {"A": -3024, "B": 46224}}
    short["agrees"] = (short["A"] == -3024 and short["B"] == 46224)
    images = dict(sm["images"])
    images["document_states"] = {"P'": [12, 108], "Q'": [48, 108]}
    images["agrees"] = (images["P"]["short_model"] == [12, 108]
                        and images["Q"]["short_model"] == [48, 108])

    tors_gcd = 0
    for q in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        if q != CONDUCTOR:
            tors_gcd = math.gcd(tors_gcd, npoints(q))

    n11 = npoints(P)
    a11 = P + 1 - n11

    rows = {ell: localization_row(ell) for ell in DIRECTIONS}
    ks = [rows[e].get("k_with_mQ_equals_k_mP") for e in DIRECTIONS]
    det = None
    if all(k is not None for k in ks):
        det = (1 * ks[1] - ks[0] * 1) % P       # det [[1,k0],[1,k1]]

    admissible = []
    for ell in range(13, SCAN):
        if ell == CONDUCTOR or ell % P != 1 or not is_prime(ell):
            continue
        n = npoints(ell)
        if n % P != 0:
            continue
        v, m = 0, n
        while m % P == 0:
            m //= P
            v += 1
        admissible.append({"ell": ell, "point_count": n, "a_ell": ell + 1 - n,
                           "a_ell_mod_11": (ell + 1 - n) % P, "v_11": v})

    log = {
        "gate": "src12_p5_localization",
        "curve": {
            "label": "389.a1", "a_invariants": AINVS,
            "conductor_claimed": CONDUCTOR,
            "conductor_is_prime": is_prime(CONDUCTOR),
            "discriminant": disc, "c4": c4, "c6": c6,
            "P_on_curve": on_curve(P0), "Q_on_curve": on_curve(Q0),
            "torsion_gcd_of_point_counts": tors_gcd,
            "torsion_is_trivial": tors_gcd == 1,
        },
        "short_model": short,
        "generator_images": images,
        "working_prime": {
            "p": P, "good": P != CONDUCTOR,
            "point_count_over_F_p": n11, "a_p": a11,
            "ordinary": a11 % P != 0,
            "anomalous_in_the_Mazur_sense": a11 % P == 1,
            "note": ("E is ordinary but NOT anomalous at 11 in the classical "
                     "a_p ≡ 1 (mod p) sense. The corpus's 'anomalous' refers to "
                     "the ramified directions being anomalous for the "
                     "Mazur–Tate height setup, a different condition"),
        },
        "ramified_directions": {
            "criterion": (
                "ell ≡ 1 (mod 11) so the degree-11 real cyclotomic subfield "
                "exists — automatic once ell ≡ 1 (mod 11), since ell − 1 = 11k "
                "with k even — tame since ell ≠ 11, and 11 | #E(F_ell), which is "
                "the Kurihara/Kolyvagin condition a_ell ≡ ell + 1 (mod 11)"),
            "rows": rows,
            "checks": {
                str(e): {
                    "ell_is_1_mod_11": e % P == 1,
                    "tame": e != P,
                    "kurihara_condition_a_ell_equals_ell_plus_1_mod_11":
                        (rows[e]["point_count"]) % P == 0,
                    "eleven_divides_exactly_once": rows[e]["v_11_of_point_count"] == 1,
                } for e in DIRECTIONS},
        },
        "localization_matrix": {
            "recomputed_rows": [rows[e].get("row_normalised") for e in DIRECTIONS],
            "document_states": [[1, 2], [1, 4]],
            "agrees": [rows[e].get("row_normalised") for e in DIRECTIONS]
                      == [[1, 2], [1, 4]],
            "determinant_mod_11": det,
            "determinant_nonzero": det not in (None, 0),
            "consequence": (
                "a nonzero determinant makes localization injective on "
                "E(Q)/11E(Q); with trivial torsion that forces rank ≥ 2"),
        },
        "how_special_are_397_and_991": {
            "scanned_primes_below": SCAN,
            "admissible_count": len(admissible),
            "admissible": admissible,
            "the_two_used_are_the_smallest": (
                [e["ell"] for e in admissible][:2] == list(DIRECTIONS)),
        },
        "not_checked_here": {
            "Sha[11] = 0": ("carried by the P5 documents as an INHERITED "
                            "dependency and labelled as such; nothing in this "
                            "gate bears on it"),
            "Sel_11 ≅ (Z/11)^2": ("follows from rank 2, trivial torsion and that "
                                  "vanishing. This gate supplies the first two"),
            "the OPEN comparison": ("analytic leading term against algebraic "
                                    "regulator — the target the whole sub-line "
                                    "names as open in every package"),
        },
        "ok": (short["agrees"] and images["agrees"] and tors_gcd == 1
               and on_curve(P0) and on_curve(Q0)
               and det not in (None, 0)
               and all(rows[e]["v_11_of_point_count"] == 1 for e in DIRECTIONS)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    c = log["curve"]
    print(f"  389.a1 {AINVS}   Δ = {disc:,}   c4 = {c4}   c6 = {c6}")
    print(f"    conductor {CONDUCTOR} prime: {c['conductor_is_prime']}   "
          f"P=(0,0) on curve: {c['P_on_curve']}   Q=(1,0): {c['Q_on_curve']}")
    print(f"    torsion trivial (gcd of #E(F_p) = {tors_gcd}): "
          f"{c['torsion_is_trivial']}")
    print(f"    short model  Y² = X³ {short['A']:+,}X {short['B']:+,}   "
          f"matches document: {short['agrees']}")
    print(f"    P → {images['P']['short_model']}  Q → "
          f"{images['Q']['short_model']}   matches document: {images['agrees']}")
    print(f"    p = 11: #E(F_11) = {n11}  a_11 = {a11}  ordinary: "
          f"{log['working_prime']['ordinary']}  anomalous(a_p≡1): "
          f"{log['working_prime']['anomalous_in_the_Mazur_sense']}")
    print()
    for e in DIRECTIONS:
        r = rows[e]
        print(f"    ℓ = {e}:  #E(F_ℓ) = {r['point_count']:,} = "
              + "·".join(f"{a}^{b}" if b > 1 else str(a)
                         for a, b in sorted(factor(r['point_count']).items()))
              + f"   v₁₁ = {r['v_11_of_point_count']}")
        print(f"              cofactor {r['cofactor']}   m·P = {r['m_times_P']}"
              f"   m·Q = {r['m_times_Q']}   row = {r.get('row_normalised')}")
    lm = log["localization_matrix"]
    print()
    print(f"    localization matrix recomputed: {lm['recomputed_rows']}   "
          f"document: {lm['document_states']}   agrees: {lm['agrees']}")
    print(f"    det = {lm['determinant_mod_11']} in F₁₁   nonzero: "
          f"{lm['determinant_nonzero']}")
    print()
    hs = log["how_special_are_397_and_991"]
    print(f"    primes below {SCAN:,} meeting the same criterion: "
          f"{hs['admissible_count']}")
    print("      " + ", ".join(str(e["ell"]) for e in admissible))
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
