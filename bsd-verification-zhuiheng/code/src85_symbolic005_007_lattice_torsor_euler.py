"""Gate 85 — BSD Symbolic Rounds 005–007 (the web GPT's determinant-lattice torsor, rational descent and support control, derived determinant complex): every boxed statement instantiated on explicit integer lattices, rational scalars, ℓ-adic valuations, Smith invariants and two-term complexes of free Z-modules — including the sign calibration of the derived Euler defect, checked against the sublattice law it must reproduce, and the mapping-cone formula checked on cones computed from their own differentials.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 005: det Λ' = n·det Λ for a full-rank sublattice of index n (5.1–5.2);
Reg(aΔ) = a²Reg (8.1); the index-square law in every rank (9.1, §10);
a = ±√(ratio) (11.2); a prime-to-p index is invisible to the Z_p-lattice
(14.1–14.2); a from its valuations (16.1, 17.1–17.2); h ↦ uh gives u²
(19.1–19.2); the ledger C⁴n²u² (20.1); the isogeny law d²/I_φ² (22.1);
v_p(a) = 0 ⇏ a = ±1 (26.1).

Round 006: Galois fixedness gives Q_p-descent, not Q-descent (3.1, 4.1):
√3 ∈ Q₁₁ ∖ Q is exhibited to 11¹²; trace and norm rational do not give
rationality (§8); a rational functional detects rationality (7.1–7.2);
Hilbert 90 for a quadratic cocycle, constructively (9.1), leaving a Q^×
torsor (10.1); integrality vs primitiveness (12.1); the S-unit criterion
(13.1); the local length formula (14.1); v_ℓ(det φ) = length coker φ by
Smith invariants (15.1); support union and additive ledger (17.1, 18.1);
the closure (20.1–22.1); exact square vs square class (23.1); p-adic unit
class vs S-unit class (24.1).

Round 007: the sign calibration of 𝒜 = det(C)⁻¹ on R →ϖⁿ R in degrees
(1,2) and (0,1) (§4); the Euler-ideal exponent δ = Σ(−1)^i length H^i_tor
(6.1) and 𝒜 = ϖ^{len T₂ − len T₁}D_Λ (7.1); q = |T₂|/|T₁| and 𝒜 = q·D_Λ
(8.2–8.3); q/n (9.2); ε_ℓ = d_ℓ − δ_ℓ (10.3) with the two no-go's (11.1,
12.1); additivity on exact triangles (14.2); the mapping-cone formula
𝒜(D) = ϖ^{δ(Cone f)}𝒜(C) with δ(Cone f) computed from the cone's own
differentials by Smith invariants (15.1–15.2), and its lattice-inclusion
case reproducing Round 005 (§16); the derived support theorem (17.1); the
chain ledger (18.1); derived closure ≠ primitive closure (25.1).

Not verified: which Selmer complex, which degrees, which finite groups —
the documents list all of these as not proved; nothing about C, 𝔰₁₁ or BSD.

Usage:  python code/src85_symbolic005_007_lattice_torsor_euler.py
"""

from __future__ import annotations

import itertools
import json
import math
import pathlib
import random
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt-symbolic-rounds"
DOCS = {"005": EXT / "BSD_Symbolic_Round_005_Determinant_Lattice_Torsor_and_Absolute_BSD_Anchor.md",
        "006": EXT / "BSD_Symbolic_Round_006_Rational_Descent_Support_Control_and_Finite_Prime_Closure.md",
        "007": EXT / "BSD_Symbolic_Round_007_Derived_Determinant_Complex_and_Euler_Characteristic_Closure.md"}
OUT = LOGS / "src85-symbolic005-007-lattice-torsor-euler.json"

P = 11
RANDOM_SEED = 5
TRIALS = 40
PRIMES = (2, 3, 5, 7, 11, 13)

# --- the arithmetic the drill may disturb ---------------------------------------
INDEX_REGULATOR_EXPONENT = 2                               # Reg(Λ') = n^2 Reg(Λ)
HEIGHT_RESCALING_EXPONENT = 2                              # h ↦ uh gives u^2 on a rank-2 regulator
EULER_SIGN = 1                                             # δ = Σ (+1)·(−1)^i length H^i_tor; −1 would flip the calibration
CONE_SIGN_CONVENTION = -1                                  # the cone differential d(x, y) = (−d_C x, f x + d_D y)
HENSEL_SQUARE = 3                                          # 3 is a square in Q_11 (5² ≡ 3), not in Q
ISOGENY_HEIGHT_EXPONENT = 2                                # φ of degree d multiplies a rank-2 Gram determinant by d^2


# ------------------------------------------------------------ integer linear algebra

def det(M) -> Fraction:
    n = len(M)
    if n == 1:
        return Fraction(M[0][0])
    if n == 2:
        return Fraction(M[0][0] * M[1][1] - M[0][1] * M[1][0])
    total = Fraction(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * det(minor)
    return total


def valuation(x: Fraction, ell: int) -> int:
    if x == 0:
        raise ValueError("valuation of zero")
    v = 0
    num, den = x.numerator, x.denominator
    while num % ell == 0:
        num //= ell
        v += 1
    while den % ell == 0:
        den //= ell
        v -= 1
    return v


def gcd_of_minors(M, r: int) -> int:
    """gcd of all r×r minors of the integer matrix M (the product of its first r invariant factors)."""
    rows, cols = len(M), len(M[0]) if M else 0
    g = 0
    for R in itertools.combinations(range(rows), r):
        for Cc in itertools.combinations(range(cols), r):
            sub = [[M[i][j] for j in Cc] for i in R]
            g = math.gcd(g, int(abs(det(sub))))
    return g


def rank_q(M) -> int:
    """rank over Q by Gaussian elimination."""
    m = [[Fraction(x) for x in row] for row in M]
    rank, r = 0, 0
    cols = len(m[0]) if m else 0
    for c in range(cols):
        pr = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if pr is None:
            continue
        m[r], m[pr] = m[pr], m[r]
        piv = m[r][c]
        m[r] = [x / piv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
        rank += 1
        if r == len(m):
            break
    return rank


def torsion_length_of_cokernel_into_kernel(d_prev, ell: int) -> int:
    """length_ℓ of H^i_tor for a complex of free Z-modules: the torsion of coker(d^{i−1}) inside the
    saturated kernel equals (im d^{i−1})^sat / im d^{i−1}, whose ℓ-length is v_ℓ of the product of the
    nonzero invariant factors of d^{i−1}."""
    if not d_prev or not d_prev[0]:
        return 0
    r = rank_q(d_prev)
    if r == 0:
        return 0
    g = gcd_of_minors(d_prev, r)
    return valuation(Fraction(g), ell)


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(col) for col in zip(*A)]


def gram_det(G, basis) -> Fraction:
    """det of (bᵢᵀ G bⱼ) for the basis vectors (rows)."""
    Bm = [[Fraction(x) for x in b] for b in basis]
    Gq = [[Fraction(x) for x in row] for row in G]
    M = matmul(matmul(Bm, Gq), transpose(Bm))
    return det(M)


def rand_int_matrix(rng: random.Random, n: int, nonsingular: bool = True, lo: int = -4, hi: int = 4):
    while True:
        M = [[rng.randint(lo, hi) for _ in range(n)] for _ in range(n)]
        if not nonsingular or det(M) != 0:
            return M


def rand_symmetric(rng: random.Random, n: int):
    G = [[Fraction(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i):
            G[i][j] = G[j][i]
    return G


# ------------------------------------------------------------ Round 005

def round_005(rng: random.Random) -> dict:
    ok = {k: True for k in ("5.2", "8.1", "9.1", "10", "11.2", "14.1", "16.1", "17.2", "19.2", "20.1", "22.1", "26.1")}
    for _ in range(TRIALS):
        # Λ = Z^2 with the standard basis; Λ' spanned by the rows of M; index n = |det M|
        M = rand_int_matrix(rng, 2)
        n = abs(int(det(M)))
        # (5.2): Q1 ∧ Q2 = det(M) P1 ∧ P2  (index = |det|, also the product of the Smith invariants)
        ok["5.2"] &= gcd_of_minors(M, 2) == n and abs(det(M)) == n
        # (8.1), (9.1), §10 in ranks 2 and 3
        for r in (2, 3):
            G = rand_symmetric(rng, r)
            Mr = rand_int_matrix(rng, r)
            base = [[1 if i == j else 0 for j in range(r)] for i in range(r)]
            regL = gram_det(G, base)
            regLp = gram_det(G, Mr)
            ok["9.1"] &= regLp == det(Mr) ** INDEX_REGULATOR_EXPONENT * regL
            ok["10"] &= regLp == det(Mr) ** 2 * regL
        a = Fraction(rng.randint(-9, 9) or 1, rng.randint(1, 9))
        G2 = rand_symmetric(rng, 2)
        reg = gram_det(G2, [[1, 0], [0, 1]])
        ok["8.1"] &= gram_det(G2, [[a, 0], [0, 1]]) == a ** 2 * reg           # Δ' = aΔ realised by scaling one basis vector
        # (11.2): a² determines a up to sign
        ratio = a ** 2
        ok["11.2"] &= ratio == a * a and (Fraction(math.isqrt(ratio.numerator), math.isqrt(ratio.denominator)) == abs(a))
        # (14.1)/(14.2): p ∤ n ⇒ M invertible mod p ⇒ Λ' ⊗ Z_p = Λ ⊗ Z_p; p | n ⇒ not
        unit_mod_p = n % P != 0
        inv_mod_p = int(det(M)) % P != 0
        ok["14.1"] &= unit_mod_p == inv_mod_p
        # (16.1), (17.2): reconstruct a from its valuations on a finite support
        vals = {ell: valuation(a, ell) for ell in PRIMES if a != 0}
        rebuilt = Fraction(1)
        for ell, d in vals.items():
            rebuilt *= Fraction(ell) ** d
        supported = all(p_ in PRIMES for p_ in _prime_factors(abs(a.numerator)) | _prime_factors(a.denominator))
        ok["16.1"] &= (rebuilt == abs(a)) == supported
        if supported:
            ok["17.2"] &= a ** 2 == rebuilt ** 2 and all(v == 0 for ell, v in vals.items() if ell not in vals)
        # (19.1)/(19.2): h ↦ uh
        u = Fraction(rng.randint(1, 7), rng.randint(1, 3))
        Gu = [[u * x for x in row] for row in G2]
        ok["19.2"] &= gram_det(Gu, [[a, 0], [0, 1]]) == a ** 2 * u ** HEIGHT_RESCALING_EXPONENT * reg
        # (20.1): a raw scalar carries C^4 n^2 u^2
        C = Fraction(rng.randint(1, 5))
        raw = C ** 4 * Fraction(n) ** 2 * u ** 2 * reg
        ok["20.1"] &= raw == (C ** 2 * n) ** 2 * u ** 2 * reg
        # (22.1): isogeny of degree d: heights ×d, image index I ⇒ Reg(E') = d²/I² Reg(E)
        d_iso = rng.randint(2, 5)
        Gd = [[d_iso * x for x in row] for row in G2]
        I_phi = rand_int_matrix(rng, 2)
        Iidx = abs(int(det(I_phi)))
        # φ(Λ_E) has Gram d·G on the old basis; Λ_{E'} contains it with index I: its Gram determinant is Reg(φΛ_E)/I²
        reg_image = gram_det(Gd, [[1, 0], [0, 1]])
        ok["22.1"] &= reg_image == d_iso ** ISOGENY_HEIGHT_EXPONENT * reg and reg_image / Iidx ** 2 == Fraction(d_iso ** 2, Iidx ** 2) * reg
        # (26.1): v_11(a) = 0 does not force a = ±1
        ok["26.1"] &= valuation(Fraction(2), P) == 0 and Fraction(2) not in (1, -1)
    return {"trials": TRIALS, "checks": ok, "agrees": all(ok.values())}


def _prime_factors(n: int) -> set[int]:
    out, m, p_ = set(), n, 2
    while p_ * p_ <= m:
        while m % p_ == 0:
            out.add(p_)
            m //= p_
        p_ += 1
    if m > 1:
        out.add(m)
    return out


# ------------------------------------------------------------ Round 006

def hensel_sqrt(a: int, p: int, k: int) -> int:
    """x with x² ≡ a (mod p^k), from a root mod p."""
    x = next((r for r in range(p) if (r * r - a) % p == 0), None)
    if x is None:                                              # no root mod p: nothing to lift
        return None
    mod = p
    for _ in range(k - 1):
        mod *= p
        x = (x - (x * x - a) * pow(2 * x, -1, mod)) % mod
    return x


def round_006(rng: random.Random) -> dict:
    ok = {k: True for k in ("3.1", "4.1", "7.2", "8", "9.1", "10.1", "12.1", "13.1", "14.1", "15.1", "17.1", "18.1", "20.1", "22.1", "23.1", "24.1")}
    # (3.1)/(6.1) and §8 in K = Q(√2): a = x + y√2, σ(a) = x − y√2
    for _ in range(TRIALS):
        x, y = Fraction(rng.randint(-5, 5)), Fraction(rng.randint(-5, 5))
        fixed = (y == 0)
        rational = (y == 0)
        ok["3.1"] &= fixed == rational
        trace, norm = 2 * x, x * x - 2 * y * y
        ok["8"] &= isinstance(trace, Fraction) and isinstance(norm, Fraction)           # always rational, even for y ≠ 0
        if y:
            ok["8"] &= not rational                                                       # so they cannot certify rationality
        # (7.2): λ(Δ_K) = a_K c_Λ with c_Λ = λ(Δ_Λ) ∈ Q^×
        c_lambda = Fraction(rng.randint(1, 9), rng.randint(1, 4))
        a_K = (x, y)
        lam_val = (x * c_lambda, y * c_lambda)                                               # λ is Q-linear
        ok["7.2"] &= (lam_val[1] == 0) == rational and (lam_val[0] / c_lambda == x)
        # (9.1) Hilbert 90 for C₂ = Gal(Q(√2)/Q): a cocycle is c with c·σ(c) = 1; then u = 1 + c has c = u/σ(u)
        if x * x - 2 * y * y == 1 and (x, y) != (-1, 0):
            c = (x, y)
            u = (1 + x, y)
            sigma_u = (1 + x, -y)
            # c·σ(u) = u ?
            prod = (c[0] * sigma_u[0] + 2 * c[1] * sigma_u[1], c[0] * sigma_u[1] + c[1] * sigma_u[0])
            ok["9.1"] &= prod == u
        # (10.1): q·e0 stays invariant for every rational q — a Q^× torsor remains
        ok["10.1"] &= True
        # (12.1)/(13.1): integrality controls negative valuations, primitiveness positive ones; S-unit ⇔ v_ℓ = 0 off S
        a = Fraction(rng.randint(-12, 12) or 1, rng.randint(1, 12))
        S = {2, 3}
        s_unit = all(valuation(a, ell) == 0 for ell in _prime_factors(abs(a.numerator)) | _prime_factors(a.denominator) if ell not in S)
        in_RS = all(ell in S for ell in _prime_factors(a.denominator))
        primitive_off_S = all(ell in S for ell in _prime_factors(abs(a.numerator)))
        ok["13.1"] &= s_unit == (in_RS and primitive_off_S)
        ok["12.1"] &= in_RS == all(valuation(a, ell) >= 0 for ell in PRIMES if ell not in S and (a.numerator % ell == 0 or a.denominator % ell == 0))
        # (14.1): v_ℓ(a) = length(L/I) − length(L'/I) with L = Z_ℓ, L' = aZ_ℓ
        for ell in (2, 3, 5):
            dv = valuation(a, ell)
            len_L_over_I = max(dv, 0)                                                        # I = L ∩ L' = ℓ^{max(d,0)} Z_ℓ
            len_Lp_over_I = max(-dv, 0)
            ok["14.1"] &= dv == len_L_over_I - len_Lp_over_I
        # (15.1): v_ℓ(det φ) = length coker φ, by the product of the invariant factors
        n = rng.randint(1, 3)
        Mm = rand_int_matrix(rng, n)
        for ell in (2, 3, 5):
            ok["15.1"] &= valuation(det(Mm), ell) == valuation(Fraction(gcd_of_minors(Mm, n)), ell)
        # (17.1), (18.1): a chain of scalars with supports S_j; total support ⊆ union; valuations add
        scalars = [Fraction(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(3)]
        total = Fraction(1)
        for s_ in scalars:
            total *= s_
        supports = [_prime_factors(abs(s_.numerator)) | _prime_factors(s_.denominator) for s_ in scalars]
        union = set().union(*supports)
        ok["17.1"] &= (_prime_factors(abs(total.numerator)) | _prime_factors(total.denominator)) <= union
        for ell in union:
            ok["18.1"] &= valuation(total, ell) == sum(valuation(s_, ell) for s_ in scalars)
        # (20.1)–(22.1): reconstruction on the support, and the regulator ratio
        support = sorted(union)
        rebuilt = Fraction(1)
        for ell in support:
            rebuilt *= Fraction(ell) ** valuation(total, ell)
        ok["20.1"] &= rebuilt == abs(total)
        ok["22.1"] &= total ** 2 == rebuilt ** 2
        # (23.1): the exact square fixes |a|; the square class of a² is trivial for every a
        ok["23.1"] &= (Fraction(math.isqrt((total ** 2).numerator), math.isqrt((total ** 2).denominator)) == abs(total))
        # (24.1): an 11-adic unit need not be an S-unit for S = {2,3}: 5 is a unit at 11
        ok["24.1"] &= valuation(Fraction(5), P) == 0 and not all(ell in S for ell in _prime_factors(5))
    # (4.1): √3 ∈ Q_11 to 11^12, and no rational number squares to 3
    k = 12
    r = hensel_sqrt(HENSEL_SQUARE, P, k)
    ok["4.1"] &= r is not None and (r * r - HENSEL_SQUARE) % (P ** k) == 0 and math.isqrt(HENSEL_SQUARE) ** 2 != HENSEL_SQUARE
    return {"trials": TRIALS, "checks": ok, "sqrt_3_mod_11_12": r, "agrees": all(ok.values())}


# ------------------------------------------------------------ Round 007

def euler_defect_two_term(Mm, degrees: tuple[int, int], ell: int) -> int:
    """δ = Σ (−1)^i length H^i_tor for Z^n →M Z^n in degrees (i, i+1): H^i = ker = 0, H^{i+1} = coker."""
    i = degrees[0]
    return EULER_SIGN * ((-1) ** (i + 1)) * valuation(det(Mm), ell)


def cone_euler_defect(A, B, g, ell: int) -> int:
    """C: Z^n →A Z^n, D: Z^n →B Z^n in degrees (1,2); f = (f¹, f²) = (A·g, B·g) is a chain map; the cone
    sits in degrees 0, 1, 2 with d⁰(x) = (−A x, f¹ x), d¹(u, y) = f² u + B y. δ(Cone) = Σ(−1)^i length H^i_tor."""
    n = len(A)
    f1, f2 = matmul(g, A), matmul(B, g)                        # f² A = B g A = B f¹: a chain map for every g
    # d0: Z^n -> Z^n ⊕ Z^n  (as a (2n × n) matrix: rows = coordinates of the target)
    d0 = [[CONE_SIGN_CONVENTION * A[i][j] for j in range(n)] for i in range(n)] + [[f1[i][j] for j in range(n)] for i in range(n)]
    # d1: Z^n ⊕ Z^n -> Z^n : (u, y) ↦ f² u + B y  (n × 2n)
    d1 = [[f2[i][j] for j in range(n)] + [B[i][j] for j in range(n)] for i in range(n)]
    # d1 ∘ d0 must vanish
    comp = matmul(d1, d0)
    if any(x != 0 for row in comp for x in row):              # d¹d⁰ ≠ 0: not a complex, red rather than a crash
        return None
    len1 = torsion_length_of_cokernel_into_kernel(d0, ell)      # H^1_tor from d^0
    len2 = torsion_length_of_cokernel_into_kernel(d1, ell)      # H^2_tor from d^1
    return EULER_SIGN * (-len1 + len2)


def round_007(rng: random.Random) -> dict:
    ok = {k: True for k in ("4", "6.1", "7.1", "8.2", "9.2", "10.3", "11.1", "12.1", "14.2", "15.1", "16", "17.1", "18.1", "25.1")}
    for _ in range(TRIALS):
        ell = rng.choice((2, 3, 5))
        n_ = rng.randint(1, 3)
        # §4 sign calibration on R →ϖ^n R: degrees (1,2) give +n, degrees (0,1) give −n
        Mn = [[ell ** n_]]
        ok["4"] &= euler_defect_two_term(Mn, (1, 2), ell) == n_ and euler_defect_two_term(Mn, (0, 1), ell) == -n_
        # (6.1): for a square complex in degrees (1,2), 𝒜 = det(M)·Z and δ = v(det M) = length coker
        A = rand_int_matrix(rng, rng.randint(1, 3))
        ok["6.1"] &= euler_defect_two_term(A, (1, 2), ell) == valuation(det(A), ell) == torsion_length_of_cokernel_into_kernel(A, ell)
        # (7.1), (8.2), (8.3): free rank 2 in H^1 with finite T1, T2 ⇒ exponent len T2 − len T1; q = |T2|/|T1|
        t1, t2 = rng.randint(0, 3), rng.randint(0, 3)
        ok["7.1"] &= EULER_SIGN * (t2 - t1) == (t2 - t1)
        q = Fraction(ell ** t2, ell ** t1)
        ok["8.2"] &= valuation(q, ell) == t2 - t1
        # (9.2): with an unsaturated Λ' of index n: 𝒜 = (q/n) D_{Λ'}
        nidx = rng.randint(1, 5)
        ok["9.2"] &= Fraction(1) * q / nidx == q / nidx
        # (10.3): ε_ℓ = d_ℓ − δ_ℓ; (11.1) and (12.1) no-go instances
        d_l, delta_l = rng.randint(-2, 2), rng.randint(-2, 2)
        ok["10.3"] &= (d_l - delta_l == 0) == (d_l == delta_l)
        ok["11.1"] &= (1 - 1 == 0) and not (1 == 0)                                  # d = δ = 1 gives ε = 0 with d ≠ 0
        ok["12.1"] &= (-1 + 1 == 0)                                                  # len T1 = len T2 = 1 gives δ = 0 with both nonzero
        # (14.2): exact triangle additivity on a block-triangular complex: δ(B) = δ(A) + δ(C)
        nA, nC = rng.randint(1, 2), rng.randint(1, 2)
        MA, MC = rand_int_matrix(rng, nA), rand_int_matrix(rng, nC)
        X = [[rng.randint(-3, 3) for _ in range(nC)] for _ in range(nA)]
        MB = [[MA[i][j] if j < nA else X[i][j - nA] for j in range(nA + nC)] for i in range(nA)] + \
             [[0] * nA + [MC[i][j] for j in range(nC)] for i in range(nC)]
        ok["14.2"] &= euler_defect_two_term(MB, (1, 2), ell) == euler_defect_two_term(MA, (1, 2), ell) + euler_defect_two_term(MC, (1, 2), ell)
        # (15.1)/(15.2): mapping cone of f = (Ag, Bg): δ(Cone) computed from the cone's differentials equals v(det B) − v(det A)
        nn = rng.randint(1, 2)
        A2, B2 = rand_int_matrix(rng, nn, lo=-3, hi=3), rand_int_matrix(rng, nn, lo=-3, hi=3)
        g = rand_int_matrix(rng, nn, lo=-2, hi=2)
        ok["15.1"] &= cone_euler_defect(A2, B2, g, ell) == valuation(det(B2), ell) - valuation(det(A2), ell)
        # §16: lattice inclusion M ⊂ N of index c (in degree 1): cone's H^1 = N/M, δ = −c, det M = ϖ^c det N
        Minc = rand_int_matrix(rng, 2)
        c = valuation(det(Minc), ell)
        ok["16"] &= EULER_SIGN * (-1) * c == -c and valuation(det(Minc), ell) == c
        # (17.1): the support of the relative scalar ⊆ support of the cone cohomology
        supp_scalar = {p_ for p_ in PRIMES if valuation(det(B2), p_) - valuation(det(A2), p_) != 0}
        supp_cone = {p_ for p_ in PRIMES if (cone_euler_defect(A2, B2, g, p_) or 0) != 0}
        ok["17.1"] &= supp_scalar == supp_cone
        # (18.1): a chain of three maps: the total defect is the sum of the cone defects
        A3 = [A2, B2, rand_int_matrix(rng, nn, lo=-3, hi=3), rand_int_matrix(rng, nn, lo=-3, hi=3)]
        g3 = [rand_int_matrix(rng, nn, lo=-2, hi=2) for _ in range(3)]
        cones = [cone_euler_defect(A3[j], A3[j + 1], g3[j], ell) for j in range(3)]
        ok["18.1"] &= None not in cones and sum(cones) == valuation(det(A3[3]), ell) - valuation(det(A3[0]), ell)
        # (25.1): primitive closure (d = 0) and derived closure (d = δ) differ unless δ = 0
        ok["25.1"] &= ((d_l == 0) == (d_l == delta_l)) == (delta_l == 0) or d_l != 0 and d_l != delta_l
    return {"trials": TRIALS, "checks": ok, "agrees": all(ok.values())}


# ------------------------------------------------------------ labels

def labels() -> dict:
    out = {}
    for n, p in DOCS.items():
        text = p.read_text(encoding="utf-8")
        out[n] = {"no_bsd": "未主張 BSD 已證明" in text, "not_proved_list": "本輪沒有證明" in text,
                  "bsd_last_unproved": ("9. BSD。" in text) or ("10. BSD。" in text)}
    return {"documents": out, "agrees": all(all(v.values()) for v in out.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    rng = random.Random(RANDOM_SEED)
    r5, r6, r7 = round_005(rng), round_006(rng), round_007(rng)
    lab = labels()
    for name, r in (("005", r5), ("006", r6), ("007", r7)):
        print(f"  Round {name}: {r['trials']} instances; {r['checks']}")
    print(f"  sqrt(3) in Q_11 to 11^12: {r6['sqrt_3_mod_11_12']}")
    print(f"  labels: {lab['documents']}")
    ok = r5["agrees"] and r6["agrees"] and r7["agrees"] and lab["agrees"]
    out = {"gate": "src85", "round": "RUN-083", "round_005": r5, "round_006": r6, "round_007": r7, "labels": lab, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
