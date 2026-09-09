"""Gate 23 — P5's explicit local-unit cancellation at 389.a1, p = 11, recomputed.

數學戰士「墜衡」 / AMRAL Research Lab.

`BSD_P5_Explicit_Local_Unit_Cancellation_389a1_p11_v0.8` isolates every
explicitly computable 11-local factor in the rank-2 Burns–Kurihara–Sano BSD
element and asks whether a hidden 11-denominator survives. Its answer is a
chain of boxed exact statements ending in

    u_loc := (16/11)(388/389) log_ω(P),   v_11(u_loc) = 0,   u_loc ≡ 4 (mod 11).

Every link in that chain is a finite exact computation over Q, and none of it
had been recomputed. This gate does that, independently: the minimal model's
invariants, the local Euler factors at 11 and 389, the short-model change of
coordinates and its effect on the Néron differential, the point 16P′ in the
formal group at 11, and the two residues the document boxes.

WHAT MAKES THIS WORTH A ROUND RATHER THAN A SPOT CHECK.

**The formal-group computation is the document's own load-bearing step**, and it
is the one an author cannot check by inspection: 16P′ has enormous height, the
statement is about v_11 of a rational number with hundreds of digits, and the
residue mod 11 that follows is what makes the cancellation exact rather than
approximate. It is recomputed here from the group law up, in exact rational
arithmetic, with no floating point anywhere.

**The rank is 2 and the document uses one generator.** v0.8 fixes "a
Mordell–Weil basis whose first vector is P", so the boxed residue is a statement
about a *chosen* basis vector, not about the curve. Whether the second basis
vector behaves the same way is not stated, and it decides whether "the
logarithmic factor contributes exactly one positive power of 11" is a fact about
the formal group at 11 or an artefact of the choice. That is measured here.

**The truncation factor has a closed form the document does not use.** At a good
prime, L_p(E,1)^{-1} = 1 - a_p/p + 1/p = #E(F_p)/p exactly. The document computes
16/11 and separately records #E(F_11) = 16; the identity says those are the same
number, so the two are not independent evidence. Recorded rather than presented
as agreement.

Usage:  python code/src23_p5_local_units.py
"""

from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src18_tate_algorithm as tate                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src23-p5-local-units.json"

# 389.a1 in its minimal model, y^2 + y = x^3 + x^2 - 2x.
AINVS = [0, 1, 1, -2, 0]
P_MIN = (Fraction(0), Fraction(0))
P11 = 11


# --------------------------------------------------------------------------
# invariants
# --------------------------------------------------------------------------

def b_invariants(a):
    a1, a2, a3, a4, a6 = a
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = (a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4
          + a2 * a3 * a3 - a4 * a4)
    disc = (-b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6)
    return b2, b4, b6, b8, disc


def c_invariants(a):
    b2, b4, b6, _b8, _d = b_invariants(a)
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    return c4, c6


# --------------------------------------------------------------------------
# exact group law on the short model Y^2 = X^3 + A X + B
# --------------------------------------------------------------------------

def short_add(A, Pt, Qt):
    """P + Q on Y^2 = X^3 + A X + B, exact over Q. None is the point at infinity."""
    if Pt is None:
        return Qt
    if Qt is None:
        return Pt
    x1, y1 = Pt
    x2, y2 = Qt
    if x1 == x2:
        if y1 != y2 or y1 == 0:
            return None
        lam = (3 * x1 * x1 + A) / (2 * y1)
    else:
        lam = (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    y3 = lam * (x1 - x3) - y1
    return (x3, y3)


def short_mul(A, n, Pt):
    """n·P by double-and-add, exact."""
    if n < 0:
        R = short_mul(A, -n, Pt)
        return None if R is None else (R[0], -R[1])
    out, base = None, Pt
    while n:
        if n & 1:
            out = short_add(A, out, base)
        base = short_add(A, base, base)
        n >>= 1
    return out


def valuation(q: Fraction, p: int):
    """v_p of a non-zero rational, and its p-free unit part."""
    if q == 0:
        raise ZeroDivisionError("valuation of zero")
    n, d, v = q.numerator, q.denominator, 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v, Fraction(n, d)


def unit_residue(q: Fraction, p: int) -> int:
    """The residue mod p of a rational whose v_p is 0."""
    v, u = valuation(q, p)
    if v != 0:
        raise ValueError(f"v_{p} = {v}, not a unit")
    return (u.numerator * pow(u.denominator, -1, p)) % p


# --------------------------------------------------------------------------
# the minimal model, and point counting
# --------------------------------------------------------------------------

def point_count(a, p: int) -> int:
    """#E(F_p) including the point at infinity, by brute force over F_p."""
    a1, a2, a3, a4, a6 = (x % p for x in a)
    n = 1
    for x in range(p):
        rhs = (x * x * x + a2 * x * x + a4 * x + a6) % p
        for y in range(p):
            if (y * y + a1 * x * y + a3 * y - rhs) % p == 0:
                n += 1
    return n


def minimal_to_short(a, pt):
    """The standard (X, Y) = (36x + 3b2, 108(2y + a1 x + a3)) change of model.

    It sends y^2 + a1 xy + a3 y = x^3 + a2 x^2 + a4 x + a6 to
    Y^2 = X^3 - 27 c4 X - 54 c6, and dX/(2Y) = (1/6) dx/(2y + a1 x + a3), so the
    Néron differential scales by exactly 6. Both facts are asserted by v0.8 and
    both are checked below rather than taken from it.
    """
    a1, _a2, a3, _a4, _a6 = a
    b2, *_ = b_invariants(a)
    c4, c6 = c_invariants(a)
    A, B = -27 * c4, -54 * c6
    x, y = pt
    X = 36 * x + 3 * b2
    Y = 108 * (2 * y + a1 * x + a3)
    return A, B, (X, Y)


# --------------------------------------------------------------------------
# the checks
# --------------------------------------------------------------------------

def analyse() -> dict:
    log: dict = {"gate": "src23 — P5 explicit local-unit cancellation, 389.a1 at p = 11"}

    # ---- section 2: exact curve data -------------------------------------
    b2, b4, b6, b8, disc = b_invariants(AINVS)
    c4, c6 = c_invariants(AINVS)
    n11 = point_count(AINVS, 11)
    a11 = 11 + 1 - n11
    red389 = tate.reduction_data(AINVS, 389, want_c=True)
    v389 = 0
    m = abs(disc)
    while m % 389 == 0:
        m //= 389
        v389 += 1
    log["section_2_exact_curve_data"] = {
        "minimal_model": "y^2 + y = x^3 + x^2 - 2x",
        "a_invariants": AINVS,
        "b_invariants": [b2, b4, b6, b8],
        "c_invariants": [c4, c6],
        "discriminant": disc,
        "discriminant_is_389": disc == 389,
        "11_is_good": disc % 11 != 0,
        "point_count_at_11": n11,
        "a_11": a11,
        "document_says": {"Delta_E": 389, "#E(F_11)": 16, "a_11": -4},
        "agrees": disc == 389 and n11 == 16 and a11 == -4,
        "reduction_at_389": {
            "kodaira": red389["kodaira"], "f": red389["f"],
            "c_p": red389["c"],
            "v_389_of_discriminant": v389,
            "split": red389["kodaira"].startswith("I") and red389["c"] == v389,
        },
    }

    # ---- section 3: the truncation factor --------------------------------
    # L_p(E,1)^{-1} = 1 - a_p/p + p^{-1}. At a good prime that is #E(F_p)/p
    # exactly, so the document's 16/11 and its #E(F_11) = 16 are ONE fact.
    euler11 = Fraction(1) - Fraction(a11, 11) + Fraction(1, 11)
    euler389 = Fraction(1) - Fraction(1, 389)
    trunc = euler11 * euler389
    v_trunc, _ = valuation(trunc, 11)
    log["section_3_truncation_factor"] = {
        "L_11(E,1)^-1": str(euler11),
        "L_389(E,1)^-1": str(euler389),
        "product": str(trunc),
        "v_11_of_the_product": v_trunc,
        "document_says": {"L_11": "16/11", "L_389": "388/389", "v_11": -1},
        "agrees": (euler11 == Fraction(16, 11) and euler389 == Fraction(388, 389)
                   and v_trunc == -1),
        "not_independent_evidence": {
            "identity": "1 - a_p/p + 1/p = (p + 1 - a_p)/p = #E(F_p)/p",
            "holds": euler11 == Fraction(n11, 11),
            "reading": ("the document's 16/11 and its separately stated "
                        "#E(F_11) = 16 are the same computation. Their "
                        "agreement confirms nothing"),
        },
    }

    # ---- section 4: short model, differential, and 16P' -------------------
    A, B, Pshort = minimal_to_short(AINVS, P_MIN)
    on_curve = Pshort[1] ** 2 == Pshort[0] ** 3 + A * Pshort[0] + B
    # dX = 36 dx and 2Y = 216(2y + a1 x + a3), so omega' = omega/6.
    diff_ratio = Fraction(36, 216)
    P16 = short_mul(A, n11, Pshort)
    t16 = -Fraction(P16[0], 1) / Fraction(P16[1], 1)
    v_t, _ = valuation(t16, 11)
    res_t = unit_residue(t16 / 11, 11) if v_t == 1 else None
    log["section_4_formal_group"] = {
        "short_model": f"Y^2 = X^3 + {A} X + {B}",
        "document_says_short_model": "Y^2 = X^3 - 3024 X + 46224",
        "short_model_agrees": (A, B) == (-3024, 46224),
        "P_on_short_model": [str(Pshort[0]), str(Pshort[1])],
        "document_says_P_prime": [12, 108],
        "P_prime_agrees": Pshort == (Fraction(12), Fraction(108)),
        "P_prime_is_on_the_curve": on_curve,
        "omega_prime_over_omega": str(diff_ratio),
        "document_says_omega_ratio": "1/6",
        "omega_ratio_agrees": diff_ratio == Fraction(1, 6),
        "multiplier_used": n11,
        "digits_in_x_of_16P": len(str(P16[0].numerator)),
        "v_11_of_t_of_16P": v_t,
        "t_of_16P_over_11_mod_11": res_t,
        "document_says": {"v_11": 1, "residue": 7},
        "agrees": v_t == 1 and res_t == 7,
    }

    # ---- the formal logarithm, and whether t is enough --------------------
    # log(t) = t + sum_{n>=2} c_n t^n / n with c_n in Z_11 for good reduction,
    # so for v(t) = 1 every term past the first has v >= 2 UNLESS n kills it:
    # the term t^n/n has valuation n - v_11(n), which is >= 2 for all n >= 2.
    bad_n = [n for n in range(2, 200) if n - _v11_int(n) < 2]
    log["formal_logarithm_truncation"] = {
        "claim": "log_{omega'}(t) ≡ t (mod 11^2) for t in 11 Z_11",
        "argument": ("the n-th term of the formal logarithm is c_n t^n / n with "
                     "c_n integral at a prime of good reduction, so its "
                     "valuation is at least n - v_11(n)"),
        "n_with_valuation_below_2": bad_n,
        "holds": not bad_n,
        "checked_to_n": 199,
    }

    # ---- section 4/5: the residues the document boxes --------------------
    inv16 = pow(n11 % 11, -1, 11)
    res_logPprime = (res_t * inv16) % 11 if res_t is not None else None
    res_logP = (res_logPprime * 6) % 11 if res_logPprime is not None else None
    v_uloc = v_trunc + 1
    trunc_unit_res = unit_residue(trunc * 11, 11)
    res_uloc = (trunc_unit_res * res_logP) % 11 if res_logP is not None else None
    log["section_5_local_cancellation"] = {
        "16_inverse_mod_11": inv16,
        "log_omega'(P')_over_11_mod_11": res_logPprime,
        "document_says": 8,
        "log_omega(P)_over_11_mod_11": res_logP,
        "document_says_after_the_factor_6": 4,
        "v_11(log_omega(P))": 1,
        "(16/11)(388/389)·11 as a unit, mod 11": trunc_unit_res,
        "document_says_16·388/389_mod_11": 1,
        "v_11(u_loc)": v_uloc,
        "u_loc_mod_11": res_uloc,
        "document_says_u_loc": {"v_11": 0, "residue": 4},
        "agrees": (res_logPprime == 8 and res_logP == 4 and v_uloc == 0
                   and trunc_unit_res == 1 and res_uloc == 4),
    }

    # ---- the rank is 2, and the document uses one generator --------------
    log["the_second_basis_vector"] = second_generator(A, B, n11)
    log["the_residue_is_a_homomorphism"] = residue_homomorphism(A, n11)
    log["chain_inputs_v0_5_section_1_2"] = imported_curve_data()
    log["regulator_is_basis_invariant"] = regulator_is_basis_invariant(A)

    log["ok"] = all([
        log["section_2_exact_curve_data"]["agrees"],
        log["section_3_truncation_factor"]["agrees"],
        log["section_4_formal_group"]["short_model_agrees"],
        log["section_4_formal_group"]["P_prime_agrees"],
        log["section_4_formal_group"]["omega_ratio_agrees"],
        log["section_4_formal_group"]["agrees"],
        log["formal_logarithm_truncation"]["holds"],
        log["section_5_local_cancellation"]["agrees"],
        log["the_second_basis_vector"]["searched"],
        log["the_residue_is_a_homomorphism"]["is_a_homomorphism"],
        log["the_residue_is_a_homomorphism"]["generators_are_on_the_curve"],
        log["the_residue_is_a_homomorphism"]["phi_matches_the_documents_boxed_residue"],
        log["chain_inputs_v0_5_section_1_2"]["conductor_agrees"],
        log["chain_inputs_v0_5_section_1_2"]["prod_c_agrees"],
        log["chain_inputs_v0_5_section_1_2"]["torsion_agrees"],
        log["regulator_is_basis_invariant"]["agree"],
        log["regulator_is_basis_invariant"]["is_on_the_curve"],
    ])
    return log


def _v11_int(n: int) -> int:
    v = 0
    while n % 11 == 0:
        n //= 11
        v += 1
    return v


def short_to_minimal(pt):
    """Inverse of minimal_to_short for 389.a1 (a1 = 0, a3 = 1, b2 = 4)."""
    X, Y = pt
    return ((X - 12) / 36, (Y / 108 - 1) / 2)


def regulator_is_basis_invariant(A, depth: int = 8) -> dict:
    """The regulator does not move between the two bases — and that is a test.

    Reg is det of the height pairing, so a change of basis by U ∈ GL_2(Z)
    multiplies it by det(U)^2 = 1. That is a theorem, not a measurement. What
    the measurement tests is the *other* direction: if {3P + Q, P} were an
    index-k subgroup rather than a basis, the regulator would come out k^2 times
    larger — a factor of 4 or 9, impossible to miss at any depth. So agreeing to
    the method's own precision confirms index 1 independently of the determinant
    computation, and it is the reason this arm can say "basis" rather than
    "generating set".

    It also isolates what the round is claiming: Reg is basis-invariant, u_loc
    is not, so their product cannot be a basis-invariant quantity.
    """
    import src20_bsd_consistency as bsd20
    Ps = minimal_to_short(AINVS, (Fraction(0), Fraction(0)))[2]
    Qs = minimal_to_short(AINVS, (Fraction(1), Fraction(0)))[2]
    R = short_to_minimal(short_add(A, short_mul(A, 3, Ps), Qs))
    on_curve = (R[1] ** 2 + R[1] == R[0] ** 3 + R[0] ** 2 - 2 * R[0])
    P = (Fraction(0), Fraction(0))
    bases = {"{P, Q}": [[Fraction(0), Fraction(0)], [Fraction(1), Fraction(0)]],
             "{3P+Q, P}": [[R[0], R[1]], [P[0], P[1]]]}
    regs = {k: bsd20.regulator(AINVS, v, depth=depth)["regulator"]
            for k, v in bases.items()}
    vals = list(regs.values())
    spread = abs(vals[0] - vals[1])
    # An index k > 1 would show as a factor k^2 >= 4. The tolerance is set to
    # what doubling depth 8 actually delivers, not to what would look tidy.
    return {
        "3P+Q_on_the_minimal_model": [str(R[0]), str(R[1])],
        "is_on_the_curve": on_curve,
        "depth": depth,
        "regulators": {k: v for k, v in regs.items()},
        "absolute_spread": spread,
        "tolerance": 1e-3,
        "agree": spread < 1e-3,
        "smallest_index_that_would_show": 2,
        "ratio_if_index_2_were_true": 4.0,
        "reading": ("agreement to the method's precision rules out every index "
                    "k > 1, since the regulator of an index-k subgroup is k^2 "
                    "times larger. {3P + Q, P} is a basis"),
    }


def imported_curve_data() -> dict:
    """`IMC_Closure_and_GPR_Bridge_v0.5` §1.2 — the chain's declared inputs.

    The document lists these as "exact database/certified-computation inputs"
    and every later stage stands on them. Most are recomputable here, and the
    ones that are not are named as cited rather than left in the same list as
    the ones that are. That distinction is the point: a reader of §1.2 cannot
    tell which entries are arithmetic and which are imports.
    """
    b2, b4, b6, b8, disc = b_invariants(AINVS)
    bad = [p for p in (2, 3, 5, 7, 11, 13, 389) if disc % p == 0]
    red = {p: tate.reduction_data(AINVS, p, want_c=True) for p in bad}
    cond = 1
    for p, d in red.items():
        cond *= p ** d["f"]
    prod_c = 1
    for d in red.values():
        prod_c *= d["c"]
    n11 = point_count(AINVS, 11)
    a11 = 11 + 1 - n11
    # torsion: E(Q)_tors injects into E(F_p) for every good p, so the gcd over
    # several good primes bounds it. 389.a1 is claimed to have trivial torsion.
    counts = {p: point_count(AINVS, p) for p in (5, 7, 11, 13, 17, 19)}
    tors_bound = 0
    for c in counts.values():
        tors_bound = c if tors_bound == 0 else _gcd(tors_bound, c)
    return {
        "conductor": cond,
        "document_says_N": 389,
        "conductor_agrees": cond == 389,
        "bad_primes": bad,
        "reduction": {str(p): {"kodaira": d["kodaira"], "f": d["f"], "c": d["c"]}
                      for p, d in red.items()},
        "product_of_tamagawa_numbers": prod_c,
        "document_says_prod_c": 1,
        "prod_c_agrees": prod_c == 1,
        "point_counts_at_good_primes": counts,
        "torsion_order_divides": tors_bound,
        "document_says_torsion": "trivial",
        "torsion_agrees": tors_bound == 1,
        "a_11": a11,
        "document_says_a_11": -4,
        "good_ordinary_at_11": disc % 11 != 0 and a11 % 11 != 0,
        "still_cited_not_checked": [
            "rank E(Q) = 2 — this gate does not compute a rank; RUN-017 "
            "computed Reg(389.a1) from two given generators, which assumes it",
            "the Manin constant c_E = 1",
            "maximal l-adic image for EVERY prime l. RUN-007's X_0(n) method "
            "rules out a rational isogeny of degree 2, 3, 5 and 7, which gives "
            "irreducibility at those four primes and nothing about the other "
            "eight of Mazur's twelve, nor about surjectivity",
            "the Chan-Ho Kim Selmer structure theorem and the Kurihara witness "
            "that together give Sha[11^inf] = 0",
        ],
    }


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def residue_homomorphism(A, n11) -> dict:
    """R ↦ [t(16R)/11] is a HOMOMORPHISM E(Q) → Z/11, and it has a kernel.

    16 = #E(F_11), so 16R always lands in the formal group E_1(Q_11); its class
    in E_1/E_2 ≅ F_11 is what the residue records. Both maps are homomorphisms,
    so the composite is one, and a surjective homomorphism onto Z/11 has an
    index-11 kernel. On that kernel v_11(log) ≥ 2 rather than = 1.

    This is the part v0.8 does not say. Its §4 concludes "the logarithmic factor
    contributes exactly one positive power of 11" from a computation at the
    single point P = (0,0); §6 then fixes "a Mordell–Weil basis whose first
    vector is P". The homomorphism shows the conclusion is a fact about that
    vector and not about the curve — and the kernel is computed explicitly here
    rather than argued.
    """
    P = (Fraction(0), Fraction(0))                 # 389.a1's standard generators
    Q = (Fraction(1), Fraction(0))
    on_curve = all(y * y + y == x ** 3 + x * x - 2 * x for x, y in (P, Q))
    Ps = minimal_to_short(AINVS, P)[2]
    Qs = minimal_to_short(AINVS, Q)[2]

    def val_res(R):
        if R is None:
            return None, None
        S = short_mul(A, n11, R)
        if S is None:
            return None, None
        t = -Fraction(S[0]) / Fraction(S[1])
        v, _ = valuation(t, 11)
        return v, (unit_residue(t / 11, 11) if v == 1 else None)

    def comb(a, b):
        return short_add(A, short_mul(A, a, Ps), short_mul(A, b, Qs))

    phi_P = val_res(Ps)[1]
    phi_Q = val_res(Qs)[1]
    rows, mismatches = [], []
    for a in range(-3, 4):
        for b in range(-3, 4):
            if a == 0 and b == 0:
                continue
            v, res = val_res(comb(a, b))
            pred = (phi_P * a + phi_Q * b) % 11
            ok = (res == pred) if pred else (v is not None and v >= 2)
            rows.append({"a": a, "b": b, "v_11": v, "residue": res,
                         "predicted": pred, "agrees": ok})
            if not ok:
                mismatches.append({"a": a, "b": b, "v_11": v,
                                   "residue": res, "predicted": pred})
    kernel = [(r["a"], r["b"]) for r in rows if r["predicted"] == 0]
    # {3P + Q, P} has determinant -1, so it is a genuine Z-basis of E(Q) whose
    # FIRST vector lies in the kernel.
    alt_v = val_res(comb(3, 1))[0]
    return {
        "generators_used": {"P": ["0", "0"], "Q": ["1", "0"]},
        "generators_are_on_the_curve": on_curve,
        "phi(P)": phi_P,
        "phi(Q)": phi_Q,
        "phi_matches_the_documents_boxed_residue": phi_P == 7,
        "homomorphism_law": f"phi(aP + bQ) = {phi_P}a + {phi_Q}b (mod 11)",
        "combinations_tested": len(rows),
        "mismatches": mismatches,
        "is_a_homomorphism": not mismatches,
        "surjective": phi_Q % 11 != 0,
        "kernel": f"{{aP + bQ : {phi_P}a + {phi_Q}b ≡ 0 (mod 11)}} — index 11",
        "kernel_members_found": [f"{a}P + {b}Q" for a, b in kernel],
        "an_alternative_Z_basis": {
            "basis": "{3P + Q, P}",
            "determinant": 3 * 0 - 1 * 1,
            "is_a_basis": abs(3 * 0 - 1 * 1) == 1,
            "v_11_of_the_first_vector": alt_v,
        },
        "what_this_does_and_does_not_touch": {
            "survives": ("§6's boxed equivalence β_ξ u_loc ∈ Q_11 ⟺ β_ξ ∈ Q_11. "
                         "It needs only u_loc ≠ 0, which holds for every basis "
                         "vector R with 16R ≠ O"),
            "does_not_survive": ("§6's parenthetical that multiplication by "
                                 "u_loc 'neither changes the field-of-definition "
                                 "gate nor the 11-valuation'. In the basis "
                                 "{3P + Q, P} the first vector has v_11(log) = 2, "
                                 "so v_11(u_loc) = 1 and multiplication by it "
                                 "does change the 11-valuation"),
            "reading": ("the rationality half of §6 is basis-robust and the "
                        "valuation half is not, and the document does not "
                        "separate them"),
        },
    }


def second_generator(A, B, n11, x_bound=40) -> dict:
    """389.a1 has rank 2. v0.8 fixes a basis whose FIRST vector is P = (0,0).

    Whether "the logarithmic factor contributes exactly one positive power of
    11" is a fact about the formal group or about that choice is decided by the
    other basis vector, and the document does not say. Small integral points on
    the minimal model are enumerated, each is pushed through the same
    computation, and the valuations are compared.
    """
    pts = []
    for x in range(-x_bound, x_bound + 1):
        # y^2 + y = x^3 + x^2 - 2x  ⟺  (2y+1)^2 = 4x^3 + 4x^2 - 8x + 1
        rhs = 4 * x ** 3 + 4 * x * x - 8 * x + 1
        if rhs < 0:
            continue
        r = _isqrt(rhs)
        if r * r != rhs or (r - 1) % 2:
            continue
        for s in ({r, -r} if r else {0}):
            y = (s - 1) // 2 if (s - 1) % 2 == 0 else None
            if y is None:
                continue
            pts.append((Fraction(x), Fraction(y)))
    rows = []
    for pt in pts:
        _A2, _B2, sp = minimal_to_short(AINVS, pt)
        R = short_mul(A, n11, sp)
        if R is None:
            rows.append({"point": [str(pt[0]), str(pt[1])], "note": "torsion-like: 16·P = O"})
            continue
        t = -Fraction(R[0]) / Fraction(R[1])
        v, _ = valuation(t, 11)
        rows.append({"point": [str(pt[0]), str(pt[1])],
                     "v_11_of_t": v,
                     "residue_of_t/11": unit_residue(t / 11, 11) if v == 1 else None})
    vals = sorted({r["v_11_of_t"] for r in rows if "v_11_of_t" in r})
    return {
        "searched": bool(rows),
        "x_bound": x_bound,
        "integral_points_found": len(pts),
        "rows": rows,
        "distinct_valuations": vals,
        "reading": (
            "if every small point gives valuation 1 then 'exactly one positive "
            "power of 11' is a property of the formal group at 11 — 16P lands in "
            "the first formal neighbourhood and no deeper — and not of the basis "
            "choice. A point with valuation 2 or more would mean the document's "
            "boxed statement depends on which vector is called P, which it does "
            "not say"),
    }


def _isqrt(n: int) -> int:
    if n < 0:
        raise ValueError
    x = int(n ** 0.5) + 2
    while x * x > n:
        x -= 1
    while (x + 1) * (x + 1) <= n:
        x += 1
    return x


def main() -> int:
    log = analyse()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    s2 = log["section_2_exact_curve_data"]
    print(f"  Δ = {s2['discriminant']}, #E(F_11) = {s2['point_count_at_11']}, "
          f"a_11 = {s2['a_11']}   agrees: {s2['agrees']}")
    r = s2["reduction_at_389"]
    print(f"  389: {r['kodaira']}, f = {r['f']}, c = {r['c_p']}, "
          f"v_389(Δ) = {r['v_389_of_discriminant']}")
    s3 = log["section_3_truncation_factor"]
    print(f"  truncation {s3['product']}, v_11 = {s3['v_11_of_the_product']}   "
          f"agrees: {s3['agrees']}")
    print(f"    and 16/11 IS #E(F_11)/11: "
          f"{s3['not_independent_evidence']['holds']} — not independent evidence")
    s4 = log["section_4_formal_group"]
    print(f"  short model {s4['short_model']}   agrees: {s4['short_model_agrees']}")
    print(f"  ω'/ω = {s4['omega_prime_over_omega']}   "
          f"agrees: {s4['omega_ratio_agrees']}")
    print(f"  16P′: x has a {s4['digits_in_x_of_16P']}-digit numerator; "
          f"v_11(t) = {s4['v_11_of_t_of_16P']}, "
          f"t/11 ≡ {s4['t_of_16P_over_11_mod_11']} (mod 11)   "
          f"agrees: {s4['agrees']}")
    fl = log["formal_logarithm_truncation"]
    print(f"  log(t) ≡ t mod 11²: {fl['holds']} (no n ≤ 199 with valuation < 2)")
    s5 = log["section_5_local_cancellation"]
    print(f"  log_ω(P)/11 ≡ {s5['log_omega(P)_over_11_mod_11']} (mod 11), "
          f"v_11(u_loc) = {s5['v_11(u_loc)']}, u_loc ≡ {s5['u_loc_mod_11']}   "
          f"agrees: {s5['agrees']}")
    g = log["the_second_basis_vector"]
    print(f"  small integral points: {g['integral_points_found']}, "
          f"distinct v_11(t(16·)): {g['distinct_valuations']}")
    h = log["the_residue_is_a_homomorphism"]
    print(f"  the residue is a homomorphism: {h['is_a_homomorphism']} over "
          f"{h['combinations_tested']} combinations   {h['homomorphism_law']}")
    print(f"    kernel {h['kernel']}, e.g. {', '.join(h['kernel_members_found'][:4])}")
    ab = h["an_alternative_Z_basis"]
    print(f"    {ab['basis']} is a Z-basis (det {ab['determinant']}) whose first "
          f"vector has v_11(log) = {ab['v_11_of_the_first_vector']}")
    ci = log["chain_inputs_v0_5_section_1_2"]
    print(f"  chain inputs (v0.5 §1.2): N = {ci['conductor']}, ∏c_ℓ = "
          f"{ci['product_of_tamagawa_numbers']}, torsion divides "
          f"{ci['torsion_order_divides']}, good ordinary at 11: "
          f"{ci['good_ordinary_at_11']}")
    print(f"    still cited, not checked here: {len(ci['still_cited_not_checked'])} items")
    bi = log["regulator_is_basis_invariant"]
    regs = "  ".join(f"{k} = {v:.9f}" for k, v in bi["regulators"].items())
    print(f"  regulator across the two bases (depth {bi['depth']}): {regs}")
    print(f"    spread {bi['absolute_spread']:.2e} — an index 2 subgroup would "
          f"show a factor 4, so {{3P+Q, P}} is a basis")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
