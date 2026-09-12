"""Gate 78 — Attack 09 rewritten from this side: the auxiliary character of an Eisenstein degeneration for 389.a1 at p = 11. GPT-6's χ₈ has central value zero and a vanishing even first layer — root number, and an exact zero of L(E, χ₈ψ, 1) for the order-5 characters ψ of conductor 11 — the quadratic characters whose central value survives are listed with their twisted L-values as exact integers, and the mod-11 eigenline is cross-validated against those integers.

數學戰士「墜衡」 / AMRAL Research Lab.

GPT-6's Attack 09, as narrated on 2026-09-12 (the package itself never
arrived), runs a Loeffler–Rivero Eisenstein degeneration with the auxiliary
form E₂(1, χ₈), χ₈ the quadratic character mod 8, and reports "the extra
twisted 11-adic L-value ≡ 5 (mod 11), so nonzero", computed over forty cusp
paths (φ(88) = 40). This gate writes down what that input actually is for
389.a1 at 11, with its own arithmetic:

  * A weight-2 Eisenstein series E₂(1, χ) exists only for χ even, so χ₈ is
    (8/·), and the root number of E ⊗ χ₈ is χ₈(−389)·w(E) = (2/389) = −1
    since 389 ≡ 5 (mod 8): L(E, χ₈, 1) = 0 exactly. No normalisation moves a
    zero.
  * Beyond the sign: L(E, χ₈ψ, 1) = 0 for the four order-5 characters ψ of
    conductor 11 as well (one Galois orbit, so one event) — numerically to
    10⁻¹⁵ against controls of size 1, and mod 11 through RUN-068's plus
    eigenline, where every χ₈-twisted symbol [a/11]_{χ₈}⁺ is 0. The whole
    even part of the first cyclotomic layer of L₁₁(E ⊗ χ₈) vanishes. (The
    package, which arrived after this gate was written and is verified at
    src79 / RUN-077, uses instead the odd-branch value L₁₁(E ⊗ χ₈, x⁻¹) on
    the minus line, which is nonzero; §5's list below is for the
    central-value reading only.)
  * For every fundamental discriminant |D| ≤ 100 prime to 11: the root number
    of E ⊗ χ_D, the twisted sum S_D = Σ χ_D(b)[b/|D|]^± on the eigenline of
    the right sign, the level-11|D| sum and its Hecke identity
    Σ χ_D(c)[c/11|D|] = (a₁₁ − 2χ_D(11))·S_D, the first-layer total of the
    Mazur–Tate–Teitelbaum measure against (1 − χ_D(11)/α)²·S_D, and — for
    root number +1 — the archimedean value L(E, χ_D, 1)·√|D|/Ω^± from the
    a_n by the functional-equation series, which comes out an exact integer
    (4, 16, 36, or 0). One unit λ^± per sign carries the integers onto the
    mod-11 sums for all 27 twists, so the eigenline is now tied to the
    L-values themselves, not only to Hecke eigenvalues.
  * The smallest admissible even character is χ₅: root number +1,
    L(E, χ₅, 1)√5/Ω⁺ = 4, all five even tame branches nonzero mod 11, Euler
    factor (1 − 1/α)² a unit. The smallest odd one (weight-1 Eisenstein
    series, minus symbols) is χ₋₃. χ₆₅, χ₉₃ and χ₋₄₇ have root number +1 but
    a genuinely vanishing L-value and are unusable.

Not claimed: Loeffler–Rivero's comparison factor is not reproduced; nothing
about 𝔰₁₁, C, B₂, or BSD; the exact vanishing of L(E, χ₈ψ, 1) is a numerical
identification of an algebraic number of bounded denominator with 0, backed
by the independent mod-11 computation, not a proof.

Usage:  python code/src78_attack09_auxiliary_character.py
"""

from __future__ import annotations

import cmath
import json
import math
import pathlib
import sys
import time
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src15_phase2_anchor as anchor15                    # noqa: E402  Ω by AGM, cubic roots
import src70_kurihara_modular_symbols as kur              # noqa: E402  the eigenline, paths, a_q

LOGS = ROOT / "data" / "gate-logs"
OUT = LOGS / "src78-attack09-auxiliary-character.json"

P = 11
N = 389
AINVS = [0, 1, 1, -2, 0]                                  # 389.a1
D_LIMIT = 100                                             # fundamental discriminants with |D| ≤ D_LIMIT
BOUND = 15000                                             # a_n table
TAIL_EXPONENT = 45.0                                      # the series is cut where e^{−2πn/√M} < e^{−45}
DENOM_BOUND = 64                                          # a twisted L-value over the period is recognised as p/q, q ≤ this
ORDER5_ZERO = 1e-12                                       # |L(E, χ₈ψ, 1)| below this is a zero; controls sit above 0.05
ORDER5_CONTROL_MIN = 0.05
GPT6_D = 8                                                # the narrated auxiliary form E₂(1, χ₈)
GPT6_CLAIM = {"auxiliary_form": "E_2(1, chi_8)", "twisted_11adic_value_mod_11": 5, "cusp_paths": 40}

# --- the arithmetic the drill may disturb ---------------------------------------
KRONECKER_TWO_RULE = (1, 7)                               # (D/2) = +1 for D ≡ ±1 (mod 8), −1 for D ≡ ±3
ROOT_NUMBER_USES_CHI_MINUS_ONE = True                     # w(E ⊗ χ_D) = χ_D(−N)·w(E), not χ_D(N)·w(E)
EULER_EXPONENT = 2                                        # L_p(E, χ, 1) = (1 − χ(p)/α)^2 · L^alg(E, χ, 1)
HECKE_TWIST_CONSTANT = 2                                  # Σ_c χ(c)[c/pD] = (a_p − 2χ(p))·S_D
MEASURE_SECOND_TERM_SIGN = -1                             # μ(a + pZ_p) = α⁻¹[a/p] − α⁻²[a]
UNIT_ROOT_OVERRIDE = None                                 # None: the unit root of x² − a₁₁x + 11 mod 11
TWIST_LEVEL_EXPONENT = 2                                  # cond(E ⊗ χ_D) = N·|D|^2
SCALE_UNIT = 1                                            # the eigenline is only defined up to F₁₁^×; a control multiplies it

STATED = {"chi8_even": True, "root_number_chi8": -1, "cusp_paths_at_88": 40,
          "smallest_even_D": 5, "A_smallest_even": 4, "smallest_odd_D": -3, "A_smallest_odd": 4,
          "even_root_plus_but_L_zero": [65, 93], "odd_root_plus_but_L_zero": [-47],
          "a_11": -4, "unit_root": 7, "a_389": 1}

_CACHE: dict = {}


# ------------------------------------------------------------ characters

def legendre(x: int, p: int) -> int:
    x %= p
    if x == 0:
        return 0
    r = pow(x, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def kronecker(D: int, n: int) -> int:
    """(D/n) for n > 0: multiplicative in n, (D/2) by the mod-8 rule, Legendre at odd primes."""
    if n <= 0:
        raise ValueError("n must be positive")
    r = 1
    while n % 2 == 0:
        n //= 2
        if D % 2 == 0:
            return 0
        r *= 1 if D % 8 in KRONECKER_TWO_RULE else -1
    p = 3
    while p * p <= n:
        while n % p == 0:
            n //= p
            r *= legendre(D, p)
        p += 2
    if n > 1:
        r *= legendre(D, n)
    return r


def chi_minus_one(D: int) -> int:
    return 1 if D > 0 else -1


def _squarefree(m: int) -> bool:
    m = abs(m)
    k = 2
    while k * k <= m:
        if m % (k * k) == 0:
            return False
        k += 1
    return True


def is_fundamental(D: int) -> bool:
    if D in (0, 1):
        return False
    if D % 4 == 1:
        return _squarefree(D)
    if D % 4 == 0:
        m = D // 4
        return m % 4 in (2, 3) and _squarefree(m)
    return False


def fundamental_discriminants(limit: int = D_LIMIT) -> list[int]:
    """Fundamental D with 1 < |D| ≤ limit, prime to 11 and to 389."""
    return [D for D in range(-limit, limit + 1)
            if is_fundamental(D) and D % P != 0 and D % N != 0]


# ------------------------------------------------------------ the eigenline

def eigenline(sign: int) -> dict:
    """RUN-068's functional on Manin symbols mod 11, for the plus (+1) or minus (−1) condition."""
    old = kur.PLUS_SIGN
    kur.PLUS_SIGN = sign
    try:
        e = kur.eigenline()
    finally:
        kur.PLUS_SIGN = old
    lam = e["lambda"]
    ok = (lam is not None and e["dimension_after_relations"] == 65 and e["dimension_after_hecke"] == 2
          and e["dimension_after_plus"] == 1
          and all(v["agrees"] and v["is_eigenvector"] for v in e["eigenvalue_checks"].values()))
    return {"sign": sign, "lambda": [v * SCALE_UNIT % P for v in lam] if lam else None,
            "dimensions": [e["dimension_after_relations"], e["dimension_after_hecke"], e["dimension_after_plus"]],
            "first_nonzero_index": e["first_nonzero_index"], "ok": ok}


def symbol(lam: list[int], a: int, n: int) -> int:
    """[a/n] on the eigenline: the functional summed over the Manin symbols of {∞, a/n}."""
    return sum(lam[i] for i in kur.path_indices(a % n, n)) % P


def unit_root() -> dict:
    a11 = kur.a_q(P)
    roots = [x for x in range(P) if (x * x - a11 * x + P) % P == 0]
    alpha = UNIT_ROOT_OVERRIDE if UNIT_ROOT_OVERRIDE is not None else [x for x in roots if x][0]
    return {"a_11": a11, "roots_mod_11": roots, "alpha": alpha, "alpha_inv": pow(alpha, P - 2, P),
            "agrees": a11 == STATED["a_11"] and alpha == STATED["unit_root"]}


def a_389() -> int:
    if "a_389" not in _CACHE:
        _CACHE["a_389"] = N + 1 - kur.count_points_general(AINVS, N)   # counted on the node: +1, split
    return _CACHE["a_389"]


def root_number(D: int) -> dict:
    """w(E ⊗ χ_D) = χ_D(−N)·w(E) for D prime to N; w(E) = a_N for prime conductor."""
    w_e = a_389()
    chi_n = kronecker(D, N)
    sign = chi_minus_one(D) if ROOT_NUMBER_USES_CHI_MINUS_ONE else 1
    return {"D": D, "chi_D_of_minus_one": chi_minus_one(D), "chi_D_of_389": chi_n, "w_E": w_e,
            "w": sign * chi_n * w_e}


# ------------------------------------------------------------ twisted sums on the eigenline

def twisted_sums(D: int, lam: list[int], alpha: int) -> dict:
    """S_D, the level-11|D| sum, the Hecke identity, and the first-layer total of the MTT measure."""
    m = abs(D)
    units = [b for b in range(1, m) if math.gcd(b, m) == 1]
    S = sum(kronecker(D, b) * symbol(lam, b, m) for b in units) % P
    big = [c for c in range(1, P * m) if math.gcd(c, P * m) == 1]
    T = sum(kronecker(D, c) * symbol(lam, c, P * m) for c in big) % P
    chi11 = kronecker(D, P)
    a11 = kur.a_q(P)
    ainv = pow(alpha, P - 2, P)
    hecke_rhs = (a11 - HECKE_TWIST_CONSTANT * chi11) * S % P
    total = (ainv * T + MEASURE_SECOND_TERM_SIGN * (P - 1) * ainv * ainv * S) % P
    euler = pow(1 - chi11 * ainv, EULER_EXPONENT, P) * S % P
    return {"D": D, "phi": len(units), "paths_at_level_11D": len(big), "chi_D_of_11": chi11,
            "S_D": S, "level_11D_sum": T, "hecke_identity_rhs": hecke_rhs, "hecke_identity": T == hecke_rhs,
            "first_layer_total": total, "euler_factor_times_S": euler, "total_is_euler_times_S": total == euler,
            "euler_factor_mod_11": pow(1 - chi11 * ainv, EULER_EXPONENT, P)}


def tame_branches(D: int, lam: list[int], alpha: int) -> dict:
    """T_j = Σ_c χ_D(c)·c^j·[c/11|D|] over the units c mod 11|D|, j = 0..9: the ten tame branches
    of the χ_D-twisted first layer, ω^j(c) ≡ c^j (mod 11). Nonzero only where χ_D·ω^j has the
    eigenline's parity."""
    m = abs(D)
    big = [c for c in range(1, P * m) if math.gcd(c, P * m) == 1]
    syms = {c: symbol(lam, c, P * m) for c in big}
    T = [sum(kronecker(D, c) * pow(c % P, j, P) * syms[c] for c in big) % P for j in range(P - 1)]
    return {"D": D, "T_j": T, "nonzero_j": [j for j, t in enumerate(T) if t]}


def forty_paths(lam_plus: list[int], lam_minus: list[int], alpha: int) -> list[dict]:
    ainv = pow(alpha, P - 2, P)
    m = GPT6_D
    rows = []
    for c in range(1, P * m):
        if math.gcd(c, P * m) != 1:
            continue
        sp, sm = symbol(lam_plus, c, P * m), symbol(lam_minus, c, P * m)
        lp, lm = symbol(lam_plus, c, m), symbol(lam_minus, c, m)
        rows.append({"c": c, "chi_8": kronecker(m, c), "plus_88": sp, "plus_8": lp,
                     "measure_plus": (ainv * sp + MEASURE_SECOND_TERM_SIGN * ainv * ainv * lp) % P,
                     "minus_88": sm, "minus_8": lm,
                     "measure_minus": (ainv * sm + MEASURE_SECOND_TERM_SIGN * ainv * ainv * lm) % P})
    return rows


# ------------------------------------------------------------ the archimedean side

def _sieve(n: int) -> list[int]:
    f = bytearray([1]) * (n + 1)
    f[0] = f[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if f[i]:
            f[i * i::i] = bytearray(len(f[i * i::i]))
    return [i for i in range(n + 1) if f[i]]


def a_n_table() -> tuple[list[int], dict[int, int], list[int]]:
    """a_n for n ≤ BOUND: a_p by a Legendre-symbol count of (2y+1)² = 4f(x) + 1, then multiplicativity."""
    key = ("a_n", BOUND, tuple(AINVS))
    if key in _CACHE:
        return _CACHE[key]
    primes = _sieve(BOUND)
    ap = {}
    for p in primes:
        if p == 2:
            ap[p] = p + 1 - kur.count_points_general(AINVS, p)
            continue
        sq = bytearray(p)
        for y in range(p):
            sq[y * y % p] = 1
        s = 0
        for x in range(p):
            v = (4 * (x * x * x + x * x - 2 * x) + 1) % p
            if v:
                s += 1 if sq[v] else -1
        ap[p] = -s                                        # #E(F_p) = p + 1 + Σ χ_p(4f + 1)
    spf = list(range(BOUND + 1))
    for p in primes:
        for m in range(p, BOUND + 1, p):
            if spf[m] == m:
                spf[m] = p
    a = [0] * (BOUND + 1)
    a[1] = 1
    for n in range(2, BOUND + 1):
        p = spf[n]
        m, k = n, 0
        while m % p == 0:
            m //= p
            k += 1
        if p == N:
            apk = ap[p] ** k
        else:
            x0, x1 = 1, ap[p]
            for _ in range(k - 1):
                x0, x1 = x1, ap[p] * x1 - p * x0
            apk = x1
        a[n] = apk * a[m]
    _CACHE[key] = (a, ap, spf)
    return _CACHE[key]


def chi_table(D: int, nmax: int, spf: list[int]) -> list[int]:
    chi = [0] * (nmax + 1)
    chi[1] = 1
    at_prime = {}
    for n in range(2, nmax + 1):
        p = spf[n]
        if p not in at_prime:
            at_prime[p] = kronecker(D, p)
        chi[n] = at_prime[p] * chi[n // p]
    return chi


def periods() -> dict:
    b2, b4, b6, _b8, disc = anchor15.b_invariants(AINVS)
    e1, e2, e3 = anchor15.real_cubic_roots(b2, b4, b6)
    omega_plus = anchor15.real_period(AINVS)                                   # both components, Δ > 0
    omega_minus = math.pi / anchor15.agm(math.sqrt(e1 - e3), math.sqrt(e2 - e3))
    return {"discriminant": disc, "roots": [e1, e2, e3], "omega_plus": omega_plus, "omega_minus": omega_minus,
            "omega_plus_by_own_agm": 2 * math.pi / anchor15.agm(math.sqrt(e1 - e3), math.sqrt(e1 - e2))}


def twisted_l_value(D: int, w: int, per: dict) -> dict:
    """L(E, χ_D, 1) = (1 + w)·Σ a_n χ_D(n) e^{−2πn/√M}/n with M = N·|D|², then ·√|D|/Ω^±."""
    a, _ap, spf = a_n_table()
    m = abs(D)
    M = N * m ** TWIST_LEVEL_EXPONENT
    k = 2 * math.pi / math.sqrt(M)
    nmax = min(BOUND, int(TAIL_EXPONENT / k) + 1)
    chi = chi_table(D, nmax, spf)
    L = (1 + w) * sum(a[n] * chi[n] * math.exp(-k * n) / n for n in range(1, nmax + 1) if a[n] and chi[n])
    omega = per["omega_plus"] if D > 0 else per["omega_minus"]
    A = L * math.sqrt(m) / omega
    fr = Fraction(A).limit_denominator(DENOM_BOUND)
    err = abs(A - float(fr))
    recognised = err < 1e-9 * max(1.0, abs(A)) and fr.denominator % P != 0
    return {"D": D, "w": w, "terms": nmax, "tail": math.exp(-k * nmax), "L": L, "A": A,
            "A_rational": f"{fr.numerator}/{fr.denominator}", "A_numerator": fr.numerator,
            "A_denominator": fr.denominator, "recognition_error": err, "recognised": recognised,
            "A_mod_11": fr.numerator * pow(fr.denominator, P - 2, P) % P if recognised else None}


def _order5_characters() -> list[dict[int, complex]]:
    """The four characters ψ of (Z/11)^× of exact order 5, ψ(2) = e^{2πi t/5}, t = 1..4."""
    ind, x = {}, 1
    for e in range(P - 1):
        ind[x] = e
        x = x * 2 % P
    return [{n: cmath.exp(2j * math.pi * t * ind[n] / 5) for n in range(1, P)} for t in range(1, 5)]


def order_five_twists(D: int, per: dict) -> dict:
    """L(E, χ_D·ψ, 1) for the four order-5 characters ψ of conductor 11, by the functional-equation
    series of the newform f ⊗ χ_Dψ of level N·(11|D|)², root number w(E)·χ(N)·τ(χ)²/q."""
    a, _ap, spf = a_n_table()
    m = abs(D)
    q = P * m
    M = N * q ** TWIST_LEVEL_EXPONENT
    k = 2 * math.pi / math.sqrt(M)
    nmax = min(BOUND, int(TAIL_EXPONENT / k) + 1)
    base = chi_table(D, nmax, spf)
    omega = per["omega_plus"] if D > 0 else per["omega_minus"]
    out = []
    for t, psi in enumerate(_order5_characters(), start=1):
        def chi(n: int) -> complex:
            r = n % P
            return base[n] * psi[r] if r else 0
        tau = sum(kronecker(D, c) * psi[c % P] * cmath.exp(2j * math.pi * c / q)
                  for c in range(1, q) if c % P and math.gcd(c, m) == 1)
        w = a_389() * kronecker(D, N) * psi[N % P] * tau * tau / q
        s1 = sum(a[n] * chi(n) * math.exp(-k * n) / n for n in range(1, nmax + 1) if a[n] and base[n] and n % P)
        s2 = sum(a[n] * chi(n).conjugate() * math.exp(-k * n) / n for n in range(1, nmax + 1) if a[n] and base[n] and n % P)
        L = s1 + w * s2
        out.append({"t": t, "conductor": q, "terms": nmax, "gauss_norm_over_q": abs(tau) ** 2 / q,
                    "root_number": [w.real, w.imag], "L": [L.real, L.imag], "abs_L": abs(L),
                    "abs_algebraic_part": abs(L) * math.sqrt(q) / omega})
    return {"D": D, "values": out, "max_abs_L": max(v["abs_L"] for v in out),
            "min_abs_L": min(v["abs_L"] for v in out),
            "gauss_sums_primitive": all(abs(v["gauss_norm_over_q"] - 1) < 1e-9 for v in out)}


# ------------------------------------------------------------ the pieces

def parity_obstruction() -> dict:
    """GPT-6's E₂(1, χ₈): the weight-2 parity, the root number, and the whole even first layer."""
    ur = unit_root()
    alpha = ur["alpha"]
    plus, minus = eigenline(1), eigenline(-1)
    per = periods()
    even = chi_minus_one(GPT6_D) == 1
    rn = root_number(GPT6_D)
    ts_plus = twisted_sums(GPT6_D, plus["lambda"], alpha)
    tb_plus = tame_branches(GPT6_D, plus["lambda"], alpha)
    tb_minus = tame_branches(GPT6_D, minus["lambda"], alpha)
    o5 = order_five_twists(GPT6_D, per)
    ctrl = {str(D): order_five_twists(D, per) for D in (5, 13)}
    odd = -GPT6_D                                         # (−8/·): odd, so no weight-2 E₂(1, χ); minus symbols
    rn_odd = root_number(odd)
    ts_odd = twisted_sums(odd, minus["lambda"], alpha)
    paths = forty_paths(plus["lambda"], minus["lambda"], alpha)
    twisted_symbols_at_11 = {}
    for a_ in range(1, P):
        twisted_symbols_at_11[str(a_)] = sum(kronecker(GPT6_D, b) * symbol(plus["lambda"], (a_ * GPT6_D + P * b) % (P * GPT6_D), P * GPT6_D)
                                             for b in range(1, GPT6_D) if b % 2) % P
    agrees = (plus["ok"] and minus["ok"] and ur["agrees"] and even == STATED["chi8_even"]
              and rn["w"] == STATED["root_number_chi8"] and rn["chi_D_of_389"] == -1
              and ts_plus["S_D"] == 0 and ts_plus["first_layer_total"] == 0 and ts_plus["hecke_identity"]
              and ts_plus["paths_at_level_11D"] == STATED["cusp_paths_at_88"] and len(paths) == STATED["cusp_paths_at_88"]
              and all(t == 0 for t in tb_plus["T_j"]) and all(v == 0 for v in twisted_symbols_at_11.values())
              and any(t for t in tb_minus["T_j"])
              and o5["gauss_sums_primitive"] and o5["max_abs_L"] < ORDER5_ZERO
              and all(c["gauss_sums_primitive"] and c["min_abs_L"] > ORDER5_CONTROL_MIN for c in ctrl.values())
              and rn_odd["w"] == 1 and ts_odd["S_D"] != 0)
    return {"gpt6_claim": GPT6_CLAIM, "chi_8_is_even": even,
            "weight_2_eisenstein_series_E2_1_chi_exists": "only for chi even: (psi*phi)(-1) = (-1)^k",
            "root_number_of_E_twist_chi_8": rn, "389_mod_8": N % 8,
            "L_E_chi8_1_is_exactly_zero": rn["w"] == -1,
            "plus_line": ts_plus, "tame_branches_plus": tb_plus, "tame_branches_minus": tb_minus,
            "twisted_symbols_a_over_11_chi8_plus": twisted_symbols_at_11,
            "order_5_twists_chi8": o5, "order_5_controls": ctrl,
            "the_odd_character_minus_8": {"root_number": rn_odd, "minus_line": ts_odd,
                                          "note": "odd, so no weight-2 E_2(1, chi); it would need a weight-1 Eisenstein series"},
            "forty_paths": paths, "eigenlines": {"plus": plus, "minus": minus}, "unit_root": ur,
            "agrees": agrees}


def table() -> dict:
    """Every fundamental |D| ≤ 100 prime to 11: root number, twisted sums on the eigenline of the
    right sign, the two identities, the forced vanishing, and — for root number +1 — the
    archimedean value as an integer, with the unit λ^± tying the two sides."""
    ur = unit_root()
    alpha = ur["alpha"]
    lines = {1: eigenline(1), -1: eigenline(-1)}
    per = periods()
    rows = []
    for D in fundamental_discriminants():
        sign = chi_minus_one(D)
        rn = root_number(D)
        ts = twisted_sums(D, lines[sign]["lambda"], alpha)
        row = {"D": D, "sign": sign, "w": rn["w"], **{k: v for k, v in ts.items() if k != "D"}}
        if rn["w"] == 1:
            row["analytic"] = twisted_l_value(D, rn["w"], per)
        rows.append(row)
    forced = all(r["S_D"] == 0 for r in rows if r["w"] == -1)
    identities = all(r["hecke_identity"] and r["total_is_euler_times_S"] for r in rows)
    recognised = all(r["analytic"]["recognised"] for r in rows if "analytic" in r)
    cross = {}
    for sign in (1, -1):
        pairs = [(r["analytic"]["A_mod_11"], r["S_D"]) for r in rows if r["sign"] == sign and "analytic" in r]
        lam_unit = None
        usable = all(A_mod is not None for A_mod, _S in pairs)      # an unrecognised value has no residue
        for A_mod, S in pairs:
            if usable and A_mod:
                lam_unit = S * pow(A_mod, P - 2, P) % P
                break
        consistent = usable and lam_unit is not None and all((lam_unit * A_mod - S) % P == 0 for A_mod, S in pairs)
        nonzero = sum(1 for A_mod, _S in pairs if usable and A_mod)
        cross[str(sign)] = {"pairs_A_mod_11_S": pairs, "lambda_unit": lam_unit, "nonzero_pairs": nonzero,
                            "consistent": consistent and nonzero >= 3}
    even_zero = [r["D"] for r in rows if r["sign"] == 1 and r["w"] == 1 and r["analytic"]["A_numerator"] == 0]
    odd_zero = [r["D"] for r in rows if r["sign"] == -1 and r["w"] == 1 and r["analytic"]["A_numerator"] == 0]
    integers = sorted({r["analytic"]["A_rational"] for r in rows if "analytic" in r})
    return {"count": len(rows), "rows": rows, "forced_vanishing_holds": forced, "identities_hold": identities,
            "all_A_recognised": recognised, "A_values_seen": integers, "cross_check": cross,
            "even_root_plus_but_L_zero": even_zero, "odd_root_plus_but_L_zero": odd_zero,
            "periods": per, "eigenlines_ok": lines[1]["ok"] and lines[-1]["ok"],
            "agrees": (forced and identities and recognised and lines[1]["ok"] and lines[-1]["ok"]
                       and all(c["consistent"] for c in cross.values())
                       and even_zero == STATED["even_root_plus_but_L_zero"]
                       and odd_zero == STATED["odd_root_plus_but_L_zero"])}


def recommendation(tab: dict) -> dict:
    """The characters an Eisenstein degeneration at 389.a1, p = 11 can actually use."""
    ur = unit_root()
    alpha = ur["alpha"]
    plus = eigenline(1)["lambda"]
    by_size = sorted(tab["rows"], key=lambda r: abs(r["D"]))
    even = [r for r in by_size if r["sign"] == 1 and r["w"] == 1 and r["S_D"]]
    odd = [r for r in by_size if r["sign"] == -1 and r["w"] == 1 and r["S_D"]]
    if not even or not odd:                                  # nothing admissible on one side: red, not a crash
        return {"even_weight_2_route": [r["D"] for r in even], "odd_weight_1_route": [r["D"] for r in odd],
                "agrees": False}
    best_even, best_odd = even[0], odd[0]
    tb = tame_branches(best_even["D"], plus, alpha)
    return {"even_weight_2_route": [{"D": r["D"], "A": r["analytic"]["A_rational"], "chi_D_of_11": r["chi_D_of_11"],
                                     "euler_factor_mod_11": r["euler_factor_mod_11"]} for r in even],
            "odd_weight_1_route": [{"D": r["D"], "A": r["analytic"]["A_rational"], "chi_D_of_11": r["chi_D_of_11"],
                                    "euler_factor_mod_11": r["euler_factor_mod_11"]} for r in odd],
            "smallest_even": {"D": best_even["D"], "A": best_even["analytic"]["A_rational"],
                              "S_D_nonzero": bool(best_even["S_D"]), "tame_branches_plus": tb["T_j"],
                              "all_even_branches_nonzero": all(tb["T_j"][j] for j in range(0, P - 1, 2)),
                              "first_layer_total_nonzero": bool(best_even["first_layer_total"])},
            "smallest_odd": {"D": best_odd["D"], "A": best_odd["analytic"]["A_rational"]},
            "unusable_root_number_plus_one_but_L_zero": {"even": tab["even_root_plus_but_L_zero"],
                                                        "odd": tab["odd_root_plus_but_L_zero"]},
            "agrees": (best_even["D"] == STATED["smallest_even_D"]
                       and best_even["analytic"]["A_numerator"] == STATED["A_smallest_even"]
                       and best_even["analytic"]["A_denominator"] == 1
                       and best_odd["D"] == STATED["smallest_odd_D"]
                       and best_odd["analytic"]["A_numerator"] == STATED["A_smallest_odd"]
                       and best_odd["analytic"]["A_denominator"] == 1
                       and all(tb["T_j"][j] for j in range(0, P - 1, 2)))}


def labels() -> dict:
    return {"source": "GPT-6's Attack 09 progress narration, pasted by Neo on 2026-09-12; the package itself has not arrived",
            "the_claim_5_mod_11": "not a plus-line quantity (every first-layer value of chi_8 there is 0); identified and reproduced at RUN-077 as the minus-line value at x^-1",
            "loeffler_rivero_comparison_factor": "not reproduced; this gate fixes the arithmetic input any version of it consumes",
            "exact_vanishing_of_L_E_chi8_psi_1": "numerical to 1e-15 with the algebraic parts one Galois orbit of bounded denominator, and mod 11 by an independent computation; not a proof",
            "s11_C_B2": "untouched", "BSD_proved": False, "canonical_frontier_updated": False}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    t0 = time.time()
    po = parity_obstruction()
    rn = po["root_number_of_E_twist_chi_8"]
    print(f"  chi_8 even: {po['chi_8_is_even']}; w(E x chi_8) = {rn['w']} (chi_8(389) = {rn['chi_D_of_389']}, 389 = {N % 8} mod 8); "
          f"S_8+ = {po['plus_line']['S_D']}, first-layer total {po['plus_line']['first_layer_total']}, "
          f"paths {po['plus_line']['paths_at_level_11D']}")
    print(f"  tame branches, plus: {po['tame_branches_plus']['T_j']}; minus: {po['tame_branches_minus']['T_j']}")
    print(f"  twisted symbols [a/11]_chi8+ : {list(po['twisted_symbols_a_over_11_chi8_plus'].values())}")
    o5 = po["order_5_twists_chi8"]
    print(f"  L(E, chi_8 psi, 1), psi of order 5 mod 11: max |L| = {o5['max_abs_L']:.2e}; "
          f"controls min |L| = { {d: round(c['min_abs_L'], 4) for d, c in po['order_5_controls'].items()} }")
    tab = table()
    per = tab["periods"]
    print(f"  periods: Omega+ = {per['omega_plus']:.12f}, Omega- = {per['omega_minus']:.12f}")
    print(f"  {tab['count']} discriminants: forced vanishing {tab['forced_vanishing_holds']}, identities {tab['identities_hold']}, "
          f"A recognised {tab['all_A_recognised']} in {tab['A_values_seen']}; "
          f"lambda+ = {tab['cross_check']['1']['lambda_unit']} over {tab['cross_check']['1']['nonzero_pairs']} nonzero pairs, "
          f"lambda- = {tab['cross_check']['-1']['lambda_unit']} over {tab['cross_check']['-1']['nonzero_pairs']}")
    for r in tab["rows"]:
        an = r.get("analytic")
        print(f"    D={r['D']:4d} w={r['w']:+d} chi(11)={r['chi_D_of_11']:+d} S={r['S_D']:2d} T={r['level_11D_sum']:2d} "
              f"total={r['first_layer_total']:2d} euler*S={r['euler_factor_times_S']:2d}"
              + (f"  A={an['A_rational']} (err {an['recognition_error']:.1e}, {an['terms']} terms)" if an else ""))
    rec = recommendation(tab)
    print(f"  smallest even: D={rec['smallest_even']['D']}, A={rec['smallest_even']['A']}, tame branches {rec['smallest_even']['tame_branches_plus']}; "
          f"smallest odd: D={rec['smallest_odd']['D']}, A={rec['smallest_odd']['A']}; "
          f"unusable {rec['unusable_root_number_plus_one_but_L_zero']}")
    lab = labels()
    ok = po["agrees"] and tab["agrees"] and rec["agrees"]
    out = {"gate": "src78", "round": "RUN-076", "seconds": round(time.time() - t0, 2),
           "parity_obstruction": po, "table": tab, "recommendation": rec, "labels": lab, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"  agrees: {ok}  ({out['seconds']}s) -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
