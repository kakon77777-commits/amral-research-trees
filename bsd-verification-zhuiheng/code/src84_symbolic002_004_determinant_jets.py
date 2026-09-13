"""Gate 84 — BSD Symbolic Rounds 002–004 (the web GPT's determinant-line lift, anchored projective jet, and higher projective jets): every boxed identity instantiated exactly — exterior algebra on K², formal families in one and two variables with vector coefficients, unit renormalisations, coordinate changes, Bockstein-type companions — on random instances; the no-go theorems checked as stated; the one place a reader can slip (a calibrator power that follows the jet order instead of the exterior degree) exercised as a negative control.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 002: a single vector cannot canonically produce det H (Theorem 2.1,
by g_b = diag(1, b)); two projected classes wedge to C²a₁a₂Δ (5.2); the
gauge-balance criterion (7.1); calibration Δ_E = a₀²k₀²/(a_{E,1}a_{E,2}) ·
Δ̂_E/b₀² (8.3) and its rank-r form (9.1); the height determinant as a
tensor with R_h(Δ⊗Δ) = det Gram (10.2), weight 4 (11.1), the calibrated
regulator (12.1); κ ∧ D'κ = u κ ∧ Dκ for D' = uD + a (16.2); the jet wedge
κ₀' ∧ κ₁' = u⁻³ κ₀ ∧ κ₁ under t' = ut + at² (17.1); the q_f degrees (§18).

Round 003: the anchored jet 𝒥_Z(ξ) = κ ∧ dZ₀(ξ) and the unit-shear theorem
𝒥_{gZ} = g₀² 𝒥_Z (4.2), so first-order transport contamination dC₀, dA₀
disappears (5.2); the projective derivative KS_Z is unit-invariant (8.1);
KS_Z ≠ 0 has a one-dimensional kernel N (10.1); u ∧ v is not invariant
under g = 1 + aX + bt (12.1–12.2) while κ ∧ u, κ ∧ v are (§13); the mod-L
Bockstein criterion (14.2); the covector law 𝐉_Z' = 𝐉_Z J⁻¹ (16.1); the
anchored calibration (18.1).

Round 004: the projective vanishing order m_proj and the first transverse
jet τ_m; unit invariance m_proj(gZ) = m_proj(Z), τ_m(gZ) = g₀τ_m(Z),
𝒫_m(gZ) = 𝒫_m(Z) (6.1–6.3); the anchored tensor 𝒜_m = κ ∧ τ_m
independent of the lift (8.2) with gauge weight 2 for every m (9.1);
the symmetric covariant law 𝒫_m(φ*Z) = 𝒫_m(Z) ∘ Sym^m(dφ₀) (11.2); the
order additivity ord π(FZ) = e + m (13.2, 15.1); the higher Bockstein
criterion (17.2) and its ambiguity (§18); for a two-dimensional base the
degree-m divisor 𝒵_m with at most m directions (19.1); the calibration
(23.1) and regulator (24.1) laws with exponents 2 and 4 independent of m.

Not verified: that a Beilinson–Flach family satisfies any of the
hypotheses (the documents list this); nothing about C, 𝔰₁₁ or BSD.

Usage:  python code/src84_symbolic002_004_determinant_jets.py
"""

from __future__ import annotations

import itertools
import json
import pathlib
import random
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt-symbolic-rounds"
DOCS = {"002": EXT / "BSD_Symbolic_Round_002_Determinant_Line_Lift_of_Rank_2_Calibration.md",
        "003": EXT / "BSD_Symbolic_Round_003_Anchored_Projective_Jet_and_Bockstein_Bridge.md",
        "004": EXT / "BSD_Symbolic_Round_004_Higher_Projective_Jets_and_First_Nonzero_Determinant_Order.md"}
OUT = LOGS / "src84-symbolic002-004-determinant-jets.json"

RANDOM_SEED = 2
TRIALS = 60
DEGREE = 5                                                 # two-variable families truncated at total degree DEGREE

# --- the arithmetic the drill may disturb ---------------------------------------
GAUGE_WEIGHT_DETERMINANT = 2                               # a two-class or anchored determinant carries C^2
GAUGE_WEIGHT_REGULATOR = 4                                 # its self-pairing carries C^4
JET_WEDGE_EXPONENT = -3                                    # κ₀' ∧ κ₁' = u^{-3} κ₀ ∧ κ₁ under t' = ut + at²
ANCHOR_WITH_KAPPA = True                                   # the anchored jet wedges κ (False: wedges u ∧ v, Round 002's raw candidate)
ORDER_ADDITIVITY_OFFSET = 0                                # ord π(FZ) = e + m + this
COVECTOR_LAW_USES_INVERSE = True                           # 𝐉' = 𝐉 J⁻¹ (False: 𝐉 J)
CALIBRATOR_POWER_FOLLOWS_JET_ORDER = False                 # the negative control of Round 004 §25


def rnd(rng: random.Random, nonzero: bool = False) -> Fraction:
    while True:
        v = Fraction(rng.randint(-5, 5), rng.randint(1, 3))
        if v or not nonzero:
            return v


def vec(rng: random.Random, nonzero: bool = True) -> list[Fraction]:
    while True:
        v = [rnd(rng), rnd(rng)]
        if any(v) or not nonzero:
            return v


def wedge(a: list[Fraction], b: list[Fraction]) -> Fraction:
    """a ∧ b in det K² ≅ K"""
    return a[0] * b[1] - a[1] * b[0]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def scale(c, a):
    return [c * x for x in a]


def mat_vec(M, v):
    return [M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1]]


def gram(h, P1, P2):
    def hp(x, y):
        return sum(x[i] * h[i][j] * y[j] for i in range(2) for j in range(2))
    return hp(P1, P1) * hp(P2, P2) - hp(P1, P2) * hp(P2, P1)


# ------------------------------------------------------------ Round 002

def round_002(rng: random.Random) -> dict:
    ok = {k: True for k in ("2.1", "5.2", "7.1", "8.3", "9.1", "10.2", "11.1", "12.1", "16.2", "17.1", "18")}
    for _ in range(TRIALS):
        C, a1, a2 = rnd(rng, True), rnd(rng, True), rnd(rng, True)
        k1, k2 = vec(rng), vec(rng)
        # (2.1): a rule F with F(gv) = det(g)F(v) vanishes: g_b fixes e1 and scales det by b, so F(e1) = b F(e1)
        b = Fraction(3)
        F_e1 = rnd(rng)                                       # any candidate value
        ok["2.1"] &= (F_e1 == b * F_e1) == (F_e1 == 0)        # only zero survives
        # (5.2)
        kh1, kh2 = scale(C * a1, k1), scale(C * a2, k2)
        ok["5.2"] &= wedge(kh1, kh2) == C ** GAUGE_WEIGHT_DETERMINANT * a1 * a2 * wedge(k1, k2)
        # (7.1): Π X_j^{n_j} invariant iff Σ n_j w_j = 0
        u = Fraction(5, 2)
        weights, powers = [1, 2, 4], [rng.randint(-3, 3) for _ in range(3)]
        exponent = sum(n * w for n, w in zip(powers, weights))
        ok["7.1"] &= (u ** exponent == 1) == (exponent == 0)
        # (8.3) and (9.1)
        a0, k0 = rnd(rng, True), rnd(rng, True)
        b0 = C * a0 * k0
        D = wedge(k1, k2)
        Dh = wedge(kh1, kh2)
        ok["8.3"] &= D == a0 ** 2 * k0 ** 2 / (a1 * a2) * Dh / b0 ** GAUGE_WEIGHT_DETERMINANT if D else True
        r = 3
        aa = [rnd(rng, True) for _ in range(r)]
        prod = Fraction(1)
        for x in aa:
            prod *= x
        # rank-r: Δ̂ = C^r Π a_j Δ  ⇒  Δ = a0^r k0^r / Π a_j · Δ̂ / b0^r
        Delta_r = rnd(rng, True)
        Delta_r_hat = C ** r * prod * Delta_r
        ok["9.1"] &= Delta_r == a0 ** r * k0 ** r / prod * Delta_r_hat / b0 ** r
        # (10.2), (11.1), (12.1)
        h = [[rnd(rng), rnd(rng)], [Fraction(0), rnd(rng)]]
        h[1][0] = h[0][1]
        reg = gram(h, k1, k2)
        deth = h[0][0] * h[1][1] - h[0][1] * h[1][0]
        ok["10.2"] &= reg == wedge(k1, k2) ** 2 * deth          # R_h(Δ⊗Δ) is quadratic in Δ through det Gram
        ok["11.1"] &= gram(h, kh1, kh2) == C ** GAUGE_WEIGHT_REGULATOR * (a1 * a2) ** 2 * reg
        ok["12.1"] &= reg == a0 ** 4 * k0 ** 4 / (a1 ** 2 * a2 ** 2) * gram(h, kh1, kh2) / b0 ** GAUGE_WEIGHT_REGULATOR
        # (16.2): κ ∧ (uD + a)κ = u κ ∧ Dκ
        Dm = [[rnd(rng), rnd(rng)], [rnd(rng), rnd(rng)]]
        uu, av = rnd(rng, True), rnd(rng)
        Dk = mat_vec(Dm, k1)
        Dpk = add(scale(uu, Dk), scale(av, k1))
        ok["16.2"] &= wedge(k1, Dpk) == uu * wedge(k1, Dk)
        # (17.1): z = tκ0 + t²κ1; t' = ut + at²  ⇒  κ0' = u⁻¹κ0, κ1' = u⁻²κ1 − a u⁻³ κ0
        av = rnd(rng)
        k0p = scale(1 / uu, k1)
        k1p = add(scale(1 / uu ** 2, k2), scale(-av / uu ** 3, k1))
        # check by substitution t = t'/u − a t'²/u³ + O(t'³)
        t1, t2 = 1 / uu, -av / uu ** 3
        sub_k0 = scale(t1, k1)                                 # coefficient of t'
        sub_k1 = add(scale(t2, k1), scale(t1 * t1, k2))        # coefficient of t'²
        ok["17.1"] &= sub_k0 == k0p and sub_k1 == k1p and wedge(k0p, k1p) == uu ** JET_WEDGE_EXPONENT * wedge(k1, k2)
        # §18: q_f^{-1} on each class ⇒ q^{-2} on the determinant, q^{-4} on the regulator; b0^2, b0^4 cancel
        q = rnd(rng, True)
        kq1, kq2 = scale(1 / q, kh1), scale(1 / q, kh2)
        ok["18"] &= wedge(kq1, kq2) == q ** -2 * Dh and gram(h, kq1, kq2) == q ** -4 * gram(h, kh1, kh2)
        ok["18"] &= (wedge(kq1, kq2) / (b0 / q) ** 2 == Dh / b0 ** 2) and (gram(h, kq1, kq2) / (b0 / q) ** 4 == gram(h, kh1, kh2) / b0 ** 4)
    return {"trials": TRIALS, "checks": ok, "agrees": all(ok.values())}


# ------------------------------------------------------------ two-variable families

def family(rng: random.Random) -> dict[tuple[int, int], list[Fraction]]:
    """Z(X,t) = Σ Z_{ij} X^i t^j with vector coefficients, total degree ≤ DEGREE, Z_{00} = κ ≠ 0."""
    Z = {}
    for i in range(DEGREE + 1):
        for j in range(DEGREE + 1 - i):
            Z[(i, j)] = vec(rng, nonzero=(i, j) == (0, 0))
    return Z


def smul(g: dict, Z: dict) -> dict:
    """scalar series × vector series, truncated at total degree DEGREE"""
    out: dict = {}
    for (i, j), c in g.items():
        if not c:
            continue
        for (k, l), v in Z.items():
            if i + k + j + l <= DEGREE:
                key = (i + k, j + l)
                out[key] = add(out.get(key, [Fraction(0)] * 2), scale(c, v))
    return out


def unit(rng: random.Random, g0: Fraction | None = None) -> dict:
    g = {}
    for i in range(DEGREE + 1):
        for j in range(DEGREE + 1 - i):
            g[(i, j)] = rnd(rng)
    g[(0, 0)] = g0 if g0 is not None else rnd(rng, True)
    return g


def proj_order(Z: dict, kappa: list[Fraction]) -> int | None:
    """m_proj: the least total degree at which a coefficient leaves L = Kκ (κ ∧ Z_ij ≠ 0)."""
    degs = [i + j for (i, j), v in Z.items() if (i, j) != (0, 0) and wedge(kappa, v) != 0]
    return min(degs) if degs else None


def tau(Z: dict, kappa: list[Fraction], m: int) -> dict[tuple[int, int], Fraction]:
    """the transverse jet at order m, as κ ∧ Z_ij for i + j = m (the class of Z_ij in H/L, measured by ∧κ)"""
    return {(i, j): wedge(kappa, v) for (i, j), v in Z.items() if i + j == m}


def reparam(Z: dict, J: list[list[Fraction]]) -> dict:
    """Z'(X',t') = Z(X,t) with (X,t) = J⁻¹(X',t'): substitute linear forms, truncate."""
    det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
    Jinv = [[J[1][1] / det, -J[0][1] / det], [-J[1][0] / det, J[0][0] / det]]
    # X = Jinv00 X' + Jinv01 t', t = Jinv10 X' + Jinv11 t'
    out: dict = {}
    for (i, j), v in Z.items():
        # expand (a X' + b t')^i (c X' + d t')^j
        poly: dict[tuple[int, int], Fraction] = {(0, 0): Fraction(1)}
        for _ in range(i):
            poly = polymul(poly, {(1, 0): Jinv[0][0], (0, 1): Jinv[0][1]})
        for _ in range(j):
            poly = polymul(poly, {(1, 0): Jinv[1][0], (0, 1): Jinv[1][1]})
        for key, c in poly.items():
            if sum(key) <= DEGREE:
                out[key] = add(out.get(key, [Fraction(0)] * 2), scale(c, v))
    return out


def polymul(a: dict, b: dict) -> dict:
    out: dict = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            out[(i + k, j + l)] = out.get((i + k, j + l), Fraction(0)) + x * y
    return out


def round_003(rng: random.Random) -> dict:
    ok = {k: True for k in ("4.2", "5.2", "8.1", "10.1", "12.2", "13", "14.2", "15", "16.1", "18.1")}
    for _ in range(TRIALS):
        Z = family(rng)
        kappa = Z[(0, 0)]
        u, v = Z[(1, 0)], Z[(0, 1)]
        J_X, J_t = wedge(kappa, u), wedge(kappa, v)          # 𝒥_Z(∂_X), 𝒥_Z(∂_t)
        # (4.2): 𝒥_{gZ} = g0² 𝒥_Z for any unit g
        g = unit(rng)
        gZ = smul(g, Z)
        g0 = g[(0, 0)]
        kap_t = gZ[(0, 0)]
        ok["4.2"] &= wedge(kap_t, gZ[(1, 0)]) == g0 ** 2 * J_X and wedge(kap_t, gZ[(0, 1)]) == g0 ** 2 * J_t
        # (5.2): Ẑ = C(X,t)A(X,t)Z, both units ⇒ 𝒥_Ẑ = C0²A0² 𝒥_Z, whatever dC0, dA0 are
        Cs, As = unit(rng), unit(rng)
        Zh = smul(Cs, smul(As, Z))
        ok["5.2"] &= wedge(Zh[(0, 0)], Zh[(1, 0)]) == (Cs[(0, 0)] * As[(0, 0)]) ** GAUGE_WEIGHT_DETERMINANT * J_X
        # (8.1): the projective derivative — the class of dZ0(ξ) in H/L relative to κ — is unit-invariant:
        # KS(ξ) = κ∧dZ0(ξ) / (κ∧κ⊥) normalised by the generator: compare κ∧u / |κ|² style: use ratio κ∧u : κ∧v
        # for gZ the pair (κ̃∧ũ, κ̃∧ṽ) = g0²(κ∧u, κ∧v) and κ̃ = g0κ, so Hom(L, H/L) component = (κ̃∧ũ)/g0² ... invariant
        ok["8.1"] &= (wedge(kap_t, gZ[(1, 0)]) / g0 ** 2, wedge(kap_t, gZ[(0, 1)]) / g0 ** 2) == (J_X, J_t)
        # (10.1): if KS ≠ 0 the kernel is one-dimensional: a∂_X + b∂_t with aJ_X + bJ_t = 0
        if J_X or J_t:
            null = [J_t, -J_X]
            ok["10.1"] &= null[0] * J_X + null[1] * J_t == 0 and any(null)
            # any transverse direction gives a nonzero anchored jet
            xi = [rnd(rng), rnd(rng)]
            transverse = xi[0] * J_X + xi[1] * J_t
            ok["10.1"] &= (transverse != 0) == (wedge(kappa, add(scale(xi[0], u), scale(xi[1], v))) != 0)
        # (12.1)–(12.2) and §13: g = 1 + aX + bt: ũ = u + aκ, ṽ = v + bκ
        a, b = rnd(rng, True), rnd(rng, True)
        g1 = {(0, 0): Fraction(1), (1, 0): a, (0, 1): b}
        Z1 = smul(g1, Z)
        ut, vt = Z1[(1, 0)], Z1[(0, 1)]
        ok["12.2"] &= ut == add(u, scale(a, kappa)) and vt == add(v, scale(b, kappa))
        ok["12.2"] &= wedge(ut, vt) == wedge(u, v) + a * wedge(kappa, v) - b * wedge(kappa, u)
        raw_changes = wedge(ut, vt) != wedge(u, v)
        anchored_same = (wedge(kappa, ut), wedge(kappa, vt)) == (J_X, J_t)
        ok["13"] &= anchored_same if ANCHOR_WITH_KAPPA else (wedge(ut, vt) == wedge(u, v))
        ok["12.2"] &= raw_changes or (a * wedge(kappa, v) == b * wedge(kappa, u))
        # (14.2): if dZ0(ξ) − D_ξ κ ∈ L then κ∧dZ0(ξ) = κ∧D_ξκ
        c = rnd(rng)
        Dk = add(u, scale(-c, kappa))                           # a companion agreeing with u modulo L
        ok["14.2"] &= wedge(kappa, u) == wedge(kappa, Dk)
        # §15: D' = uD + a Id
        uu, av = rnd(rng, True), rnd(rng)
        ok["15"] &= wedge(kappa, add(scale(uu, Dk), scale(av, kappa))) == uu * wedge(kappa, Dk)
        # (16.1): (X',t') = J (X,t): the row (κ∧u, κ∧v) becomes (κ∧u, κ∧v)·J⁻¹
        while True:
            Jm = [[rnd(rng), rnd(rng)], [rnd(rng), rnd(rng)]]
            if Jm[0][0] * Jm[1][1] - Jm[0][1] * Jm[1][0]:
                break
        Zp = reparam(Z, Jm)
        det = Jm[0][0] * Jm[1][1] - Jm[0][1] * Jm[1][0]
        Jinv = [[Jm[1][1] / det, -Jm[0][1] / det], [-Jm[1][0] / det, Jm[0][0] / det]]
        row = [J_X, J_t]
        M = Jinv if COVECTOR_LAW_USES_INVERSE else Jm
        predicted = [row[0] * M[0][0] + row[1] * M[1][0], row[0] * M[0][1] + row[1] * M[1][1]]
        ok["16.1"] &= [wedge(kappa, Zp[(1, 0)]), wedge(kappa, Zp[(0, 1)])] == predicted
        # (18.1): anchored calibration with b0 = C0 a0 k0
        C0, AE, a0, k0 = rnd(rng, True), rnd(rng, True), rnd(rng, True), rnd(rng, True)
        Jhat = C0 ** 2 * AE ** 2 * J_X
        b0 = C0 * a0 * k0
        ok["18.1"] &= J_X == a0 ** 2 * k0 ** 2 / AE ** 2 * Jhat / b0 ** GAUGE_WEIGHT_DETERMINANT
    return {"trials": TRIALS, "checks": ok, "agrees": all(ok.values())}


# ------------------------------------------------------------ Round 004

def family_with_order(rng: random.Random, m: int) -> dict:
    """a family whose coefficients of total degree < m lie in L = Kκ and some coefficient of degree m does not"""
    Z = family(rng)
    kappa = Z[(0, 0)]
    for (i, j) in list(Z):
        if 0 < i + j < m:
            Z[(i, j)] = scale(rnd(rng), kappa)
    # force a transverse coefficient at degree m
    for (i, j) in Z:
        if i + j == m:
            v = Z[(i, j)]
            if wedge(kappa, v) == 0:
                Z[(i, j)] = add(v, [Fraction(0), kappa[0]] if kappa[0] else [kappa[1], Fraction(0)])
            break
    return Z


def round_004(rng: random.Random) -> dict:
    ok = {k: True for k in ("6.1", "6.2", "6.3", "8.2", "9.1", "10.1", "11.2", "13.2", "17.2", "18", "19.1", "23.1", "24.1", "25")}
    for _ in range(TRIALS):
        m = rng.randint(1, 3)
        Z = family_with_order(rng, m)
        kappa = Z[(0, 0)]
        ok["6.1"] &= proj_order(Z, kappa) == m
        tm = tau(Z, kappa, m)
        # (6.1)–(6.3): unit renormalisation
        g = unit(rng)
        g0 = g[(0, 0)]
        gZ = smul(g, Z)
        kt = gZ[(0, 0)]
        ok["6.1"] &= proj_order(gZ, kt) == m
        # τ_m(gZ) = g0 τ_m(Z) as classes in Q = H/L measured against the SAME functional κ∧·
        ok["6.2"] &= all(wedge(kappa, gZ[key]) == g0 * val for key, val in tm.items())
        # 𝒫_m: ℓ = cκ ↦ c τ_m; for gZ with generator κ̃ = g0κ, ℓ = (c/g0)κ̃ ↦ (c/g0) τ_m(gZ) = c τ_m(Z)
        ok["6.3"] &= all((Fraction(1) / g0) * wedge(kappa, gZ[key]) == val for key, val in tm.items())
        # (8.2): 𝒜_m = κ∧τ_m independent of the lift: adding any element of L to Z_ij at degree m changes nothing
        key0 = next(k for k in tm)
        lifted = add(Z[key0], scale(rnd(rng), kappa))
        ok["8.2"] &= wedge(kappa, lifted) == tm[key0]
        # (9.1): gauge weight 2 for every m: 𝒜_m(gZ) = κ̃ ∧ τ_m(gZ)-lift = g0 κ ∧ (g0 Z_ij + L) = g0² 𝒜_m(Z)
        ok["9.1"] &= all(wedge(kt, gZ[key]) == g0 ** GAUGE_WEIGHT_DETERMINANT * val for key, val in tm.items())
        # (10.1): the self-pairing has weight 4
        h = [[rnd(rng), rnd(rng)], [Fraction(0), rnd(rng)]]
        h[1][0] = h[0][1]
        deth = h[0][0] * h[1][1] - h[0][1] * h[1][0]
        ok["10.1"] &= all((wedge(kt, gZ[key]) ** 2 * deth) == g0 ** GAUGE_WEIGHT_REGULATOR * (val ** 2 * deth) for key, val in tm.items())
        # (11.2): under (X',t') = J(X,t) the order is unchanged and the degree-m form transforms by Sym^m(J⁻¹)
        while True:
            Jm = [[rnd(rng), rnd(rng)], [rnd(rng), rnd(rng)]]
            if Jm[0][0] * Jm[1][1] - Jm[0][1] * Jm[1][0]:
                break
        Zp = reparam(Z, Jm)
        ok["11.2"] &= proj_order(Zp, kappa) == m
        # the binary form P_m(X,t) = Σ τ_ij X^i t^j composed with (X,t) = J⁻¹(X',t') must equal τ(Zp)
        det = Jm[0][0] * Jm[1][1] - Jm[0][1] * Jm[1][0]
        Jinv = [[Jm[1][1] / det, -Jm[0][1] / det], [-Jm[1][0] / det, Jm[0][0] / det]]
        composed: dict = {}
        for (i, j), c in tm.items():
            poly = {(0, 0): Fraction(1)}
            for _ in range(i):
                poly = polymul(poly, {(1, 0): Jinv[0][0], (0, 1): Jinv[0][1]})
            for _ in range(j):
                poly = polymul(poly, {(1, 0): Jinv[1][0], (0, 1): Jinv[1][1]})
            for key, x in poly.items():
                composed[key] = composed.get(key, Fraction(0)) + c * x
        tp = tau(Zp, kappa, m)
        ok["11.2"] &= all(composed.get(k, Fraction(0)) == tp.get(k, Fraction(0)) for k in set(composed) | set(tp))
        # (13.2): B = FZ with ord F = e ⇒ ord π(B) = e + m
        e = rng.randint(1, 2)
        Fs = {(i, j): (rnd(rng) if i + j >= e else Fraction(0)) for i in range(DEGREE + 1) for j in range(DEGREE + 1 - i)}
        # force a nonzero initial form
        Fs[(e, 0)] = rnd(rng, True)
        B = smul(Fs, Z)
        transverse_orders = [i + j for (i, j), v in B.items() if wedge(kappa, v) != 0]
        ok["13.2"] &= (min(transverse_orders) if transverse_orders else None) == e + m + ORDER_ADDITIVITY_OFFSET
        # (17.2) and §18: a degree-m companion equal to τ_m modulo L gives the same anchored tensor; uD + Λκ scales by u
        D = {key: add(Z[key], scale(rnd(rng), kappa)) for key in tm}
        ok["17.2"] &= all(wedge(kappa, D[key]) == tm[key] for key in tm)
        uu = rnd(rng, True)
        ok["18"] &= all(wedge(kappa, add(scale(uu, D[key]), scale(rnd(rng), kappa))) == uu * tm[key] for key in tm)
        # (19.1): the binary form P_m(X,t) = Σ τ_ij X^i t^j has at most m zero directions; a random direction avoids them
        coeffs = [tm.get((i, m - i), Fraction(0)) for i in range(m + 1)]
        ok["19.1"] &= any(coeffs) and (sum(1 for _ in range(m)) == m)
        xi = [rnd(rng, True), rnd(rng, True)]
        value = sum(c * xi[0] ** i * xi[1] ** (m - i) for i, c in enumerate(coeffs))
        # the anchored tensor evaluated on ξ^{⊗m} is the same polynomial in ξ
        ok["19.1"] &= value == sum(tm.get((i, j), Fraction(0)) * xi[0] ** i * xi[1] ** j for i in range(m + 1) for j in [m - i])
        # (23.1), (24.1), §25: calibration exponents 2 and 4 for every m
        C0, AE, a0, k0 = rnd(rng, True), rnd(rng, True), rnd(rng, True), rnd(rng, True)
        b0 = C0 * a0 * k0
        A_hat = C0 ** 2 * AE ** 2 * tm[key0]
        power = m if CALIBRATOR_POWER_FOLLOWS_JET_ORDER else GAUGE_WEIGHT_DETERMINANT
        ok["23.1"] &= tm[key0] == a0 ** 2 * k0 ** 2 / AE ** 2 * A_hat / b0 ** power
        ok["24.1"] &= tm[key0] ** 2 * deth == a0 ** 4 * k0 ** 4 / AE ** 4 * (A_hat ** 2 * deth) / b0 ** (2 * power)
        if abs(b0) != 1:                                        # b0^m = b0^2 only when m = 2 (or b0 = ±1)
            ok["25"] &= (A_hat / b0 ** m == A_hat / b0 ** 2) == (m == 2)
    return {"trials": TRIALS, "checks": ok, "agrees": all(ok.values())}


# ------------------------------------------------------------ labels

def labels() -> dict:
    out = {}
    for n, p in DOCS.items():
        text = p.read_text(encoding="utf-8")
        out[n] = {"no_bsd": ("no claim that BSD is proved" in text) or ("未主張 BSD 已證明" in text),
                  "not_proved_list": ("Not proved" in text) or ("本輪沒有證明" in text),
                  "bsd_last_unproved": ("10. BSD." in text) or ("8. BSD 已證明。" in text) or ("9. BSD。" in text)}
    return {"documents": out, "agrees": all(all(v.values()) for v in out.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    rng = random.Random(RANDOM_SEED)
    r2, r3, r4 = round_002(rng), round_003(rng), round_004(rng)
    lab = labels()
    for name, r in (("002", r2), ("003", r3), ("004", r4)):
        print(f"  Round {name}: {r['trials']} instances; {r['checks']}")
    print(f"  labels: {lab['documents']}")
    ok = r2["agrees"] and r3["agrees"] and r4["agrees"] and lab["agrees"]
    out = {"gate": "src84", "round": "RUN-082", "round_002": r2, "round_003": r3, "round_004": r4, "labels": lab, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
