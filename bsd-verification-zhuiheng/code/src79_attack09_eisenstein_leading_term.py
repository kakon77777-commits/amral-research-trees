"""Gate 79 — GPT-6's Attack 09, the package: the minus eigenline, the forty cusp paths and λ₈(0) = L₁₁(E ⊗ χ₈, x⁻¹) ≡ 5 (mod 11) reproduced coordinate for coordinate; the Eisenstein data, the Kummer unit's 11-adic logarithm, the smoothing and adjoint factors and the formal leading-term extraction recomputed; the theorem read; and what the package settles about RUN-076.

數學戰士「墜衡」 / AMRAL Research Lab.

Attack 09's one new number is not the central value. It is

    λ₈(0) = L₁₁(F, x⁻¹),   F = f_E ⊗ χ₈,

the ordinary 11-adic L-function of the twist evaluated at the full character
x ↦ x⁻¹ of Z₁₁^× — the odd Teichmüller branch ω⁻¹ at s = 0, a non-critical
point — which the package computes mod 11 from the first layer:
S_a = Σ_{b odd} χ₈(b)·Φ_E⁻((8a + 11b)/88), μ_F(a + 11Z₁₁) = α_F⁻¹·S_a with
α_F = χ₈(11)·α_E ≡ 4, and λ₈(0) ≡ Σ_a a⁻¹·μ_F(a + 11Z₁₁) = 4⁻¹·9 ≡ 5. The
symbols are the MINUS modular symbol (v(c,d) + v(−c,d) = 0), normalised at
its first nonzero coordinate, index 3 — the line RUN-068's machinery also
builds. This gate rebuilds that line from the Manin relations, walks the
same forty paths with its own continued fractions, and finds the package's
390-coordinate vector, all forty index sequences, all forty symbol values,
the ten S_a, the ten measures, the weighted sum 9 and the value 5 —
identical.

RUN-076, written from the narration before the package arrived, analysed a
different quantity: the central value L(E, χ₈, 1) and the even (plus-line)
first layer, which vanish. The package does not use them and says so
("not the central complex L-value"). Both computations are right about
their own objects; RUN-076's replacement characters are for the
central-value reading only. This gate records the relation between the two
(RUN-076's T₉⁻ is −8⁹ times the package's weighted sum) and evaluates the
package's own criterion, λ_D(0) ≢ 0, for every even D ≤ 100.

Also recomputed: B_{2,χ₈} = 2 and the constant term −1/2 of E₂(1, χ₈); its
q-coefficients a_n = Σ_{d|n} χ₈(d)d and the slope-1 refinement f_β with
U₁₁ f_β = −11 f_β (32 coefficients, 12 residuals); the Hecke polynomial
U² + 10U − 11 = (U − 1)(U + 11); ε = 1 + √2 with norm −1, ε^σ = −ε⁻¹,
ε²⁴ = 768398401 + 543339720√2 ≡ 1 + 110√2 (mod 121), log₁₁ ε ≡ 55√2
(mod 121), log₁₁ ε/(11√2) ≡ 5 (mod 11), the tail bound; 𝒮₅(0) = 26; the
adjoint Euler multiplier ≡ 3; A₀·D_E ≡ 9; the leading-term coefficients
[t²] = A₀Cκ₀, [t³] = A₀Cκ₁ + A₁Cκ₀ − ½A₀Cκ₀, Coleman [t³] = A₀Ca₂; and the
algebra behind (20), including 416 = 16·26.

Read, not verified: Loeffler–Rivero's Proposition C1.12 / Theorem C1.13 and
the identification of the extra factor with L₁₁(F, σ_t x⁻¹); decency and
non-criticality as cited; the Bellaïche–Dasgupta remark. Nothing about C,
n, B₂ or 𝔰₁₁: the package leaves them null and so does this gate.

Usage:  python code/src79_attack09_eisenstein_leading_term.py
"""

from __future__ import annotations

import json
import math
import pathlib
import random
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src70_kurihara_modular_symbols as kur              # noqa: E402
import src78_attack09_auxiliary_character as atk78        # noqa: E402  kronecker and the discriminant list only

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "09"
DOC = EXT / "BSD_Proof_Attack_09_Eisenstein_Leading_Term.md"
THEIR_RESULT = EXT / "attack09_result.json"
OUT = LOGS / "src79-attack09-eisenstein-leading-term.json"

P = 11
N = 389
AINVS = [0, 1, 1, -2, 0]

# --- the arithmetic the drill may disturb ---------------------------------------
CHI8 = {1: 1, 3: -1, 5: -1, 7: 1}                          # (8/·) on the odd residues mod 8
TWIST_DENOMINATOR = 8                                      # Φ_F(r) = Σ_b χ₈(b) Φ⁻(r + b/8)
ALPHA_TWIST_SIGN = -1                                      # α_F = χ₈(11)·α_E = −α_E
CHARACTER_EXPONENT = -1                                    # x ↦ x⁻¹ on a + 11Z₁₁ is a⁻¹
EISENSTEIN_REFINEMENT = -11                                # f_β = f − f(q¹¹), U₁₁-eigenvalue −11
UNIT = (1, 1)                                              # ε = 1 + 1·√2
UNIT_POWER = 24                                            # ε²⁴ ≡ 1 (mod 11) in O_{K_11}
SMOOTHING_D = 5                                            # 𝒮_d(0) = d² − χ₈(d)⁻¹
LOG_TERMS = 3                                              # log series to this order, exact, before reducing mod 121
RANDOM_SEED = 9

STATED = {"lambda8": 5, "weighted_sum": 9, "alpha_F": 4,
          "S_a": [4, 9, 3, 4, 3, 8, 7, 8, 2, 7], "mu": [1, 5, 9, 1, 9, 2, 10, 2, 6, 10],
          "twisted_symbol_at_zero": 0, "paths": 40, "minus_normalisation_index": 3,
          "B2_chi8": Fraction(2), "constant_term": Fraction(-1, 2), "hecke_roots": [1, -11],
          "epsilon_power_exact": (768398401, 543339720), "epsilon_power_mod_121": (1, 110),
          "log_epsilon_mod_121": (0, 55), "log_over_11_sqrt2_mod_11": 5,
          "smoothing": 26, "adjoint_euler_mod_11": 3, "A0_times_DE_mod_11": 9,
          "class_degree_2": {("A0", "C", "kappa0"): Fraction(1)},
          "class_degree_3": {("A0", "C", "kappa0"): Fraction(-1, 2), ("A0", "C", "kappa1"): Fraction(1),
                             ("A1", "C", "kappa0"): Fraction(1)},
          "regulator_degree_3": {("A0", "C", "a2"): Fraction(1)}, "constant_416": 416}


def their_result() -> dict:
    return json.loads(THEIR_RESULT.read_text(encoding="utf-8"))


def eigenline(sign: int) -> dict:
    """RUN-068's functional for the plus (+1) or minus (−1) condition, normalised at its first nonzero
    coordinate — the package's own normalisation for the minus line (index 3 ↦ 1). Independent of
    src78's scale unit on purpose: the package's numbers are at this scale."""
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
    return {"sign": sign, "lambda": lam, "first_nonzero_index": e["first_nonzero_index"],
            "dimensions": [e["dimension_after_relations"], e["dimension_after_hecke"], e["dimension_after_plus"]], "ok": ok}


def symbol(lam: list[int], a: int, n: int) -> int:
    return sum(lam[i] for i in kur.path_indices(a % n, n)) % P


def unit_root() -> dict:
    a11 = kur.a_q(P)
    roots = [x for x in range(P) if (x * x - a11 * x + P) % P == 0]
    alpha = [x for x in roots if x][0]
    return {"a_11": a11, "roots_mod_11": roots, "alpha": alpha, "agrees": a11 == -4 and alpha == 7}


def kron8(n: int) -> int:
    return CHI8.get(n % 8, 0) if n % 2 else 0


# ------------------------------------------------------------ the minus line and the forty paths

def minus_line() -> dict:
    e = eigenline(-1)
    theirs = their_result()["new_minus_line"]
    same = e["lambda"] == theirs["vector_mod_11"]
    return {"dimensions": e["dimensions"], "first_nonzero_index": e["first_nonzero_index"],
            "nonzero_coordinates": sum(1 for v in e["lambda"] if v), "identical_to_theirs": same,
            "their_normalisation": [theirs["normalization_index"], theirs["normalization_value"]],
            "agrees": e["ok"] and same and e["first_nonzero_index"] == STATED["minus_normalisation_index"]}


def alpha_twist() -> dict:
    ur = unit_root()
    a_f = (ALPHA_TWIST_SIGN * ur["alpha"]) % P
    return {"alpha_E": ur["alpha"], "chi8_of_11": CHI8.get(P % TWIST_DENOMINATOR, 0), "alpha_F": a_f,
            "alpha_F_inv": pow(a_f, P - 2, P), "a_11_F": (ALPHA_TWIST_SIGN * ur["a_11"]) % P,
            "agrees": a_f == STATED["alpha_F"] and ur["agrees"]}


def forty_paths(lam: list[int] | None = None) -> dict:
    """S_a, μ_F(a + 11Z₁₁), the x⁻¹-weighted sum and λ₈(0), path by path, against the package's table."""
    if lam is None:
        lam = eigenline(-1)["lambda"]
    at = alpha_twist()
    ainv = at["alpha_F_inv"]
    m = TWIST_DENOMINATOR
    theirs = {r["a"]: r for r in their_result()["shifted_twisted_moment"]["residue_terms"]}
    rows, same_paths, same_syms, total = [], 0, 0, 0
    for a in range(1, P):
        summands, S = [], 0
        for b in sorted(CHI8):
            num = a * m + P * b                                # a/11 + b/8 = (8a + 11b)/88
            den = P * m
            idx = kur.path_indices(num % den, den)
            val = sum(lam[i] for i in idx) % P
            S += CHI8[b] * val
            th = next((s for s in theirs[a]["summands"] if s["b"] == b), None) if a in theirs else None
            same_paths += bool(th and th["path_indices"] == idx)
            same_syms += bool(th and th["minus_symbol"] == val)
            summands.append({"b": b, "chi8": CHI8[b], "numerator": num, "indices": idx, "symbol": val})
        S %= P
        mu = ainv * S % P
        weight = pow(a, P - 2, P) if CHARACTER_EXPONENT == -1 else pow(a, CHARACTER_EXPONENT % (P - 1), P)
        rows.append({"a": a, "S_a": S, "mu": mu, "weight": weight, "weighted": weight * mu % P, "summands": summands})
        total += weight * S
    total %= P
    lam8 = ainv * total % P
    phi_f_zero = sum(CHI8[b] * symbol(lam, b, m) for b in CHI8) % P
    # the relation to RUN-076's tame branch T₉⁻ = Σ_c χ₈(c) c⁹ [c/88]⁻ over the units c mod 88
    t9 = sum(kron8(c) * pow(c % P, 9, P) * symbol(lam, c, P * m)
             for c in range(1, P * m) if math.gcd(c, P * m) == 1) % P
    relation = (t9 + pow(m % P, 9, P) * total) % P == 0       # T₉⁻ = −8⁹·Σ a⁻¹S_a, since c ≡ 8a and χ₈(c) = −χ₈(b)
    return {"rows": rows, "S_a": [r["S_a"] for r in rows], "mu": [r["mu"] for r in rows],
            "weighted_sum": total, "lambda8_at_zero": lam8, "twisted_symbol_at_zero": phi_f_zero,
            "paths": sum(len(r["summands"]) for r in rows), "paths_identical_to_theirs": same_paths,
            "symbols_identical_to_theirs": same_syms,
            "run076_T9_minus": t9, "T9_equals_minus_8_pow_9_times_sum": relation,
            "agrees": ([r["S_a"] for r in rows] == STATED["S_a"] and [r["mu"] for r in rows] == STATED["mu"]
                       and total == STATED["weighted_sum"] and lam8 == STATED["lambda8"]
                       and phi_f_zero == STATED["twisted_symbol_at_zero"]
                       and same_paths == STATED["paths"] and same_syms == STATED["paths"] and relation)}


def hecke_measure_relation(lam: list[int] | None = None) -> dict:
    """Σ_{b=0}^{10} Φ_F((a + 11b)/121) = a₁₁(F)·Φ_F(a/11) − Φ_F(a), for every a — the relation the
    package's measure (11) rests on, checked on the twisted symbols at level 121·8."""
    if lam is None:
        lam = eigenline(-1)["lambda"]
    m = TWIST_DENOMINATOR
    a11f = alpha_twist()["a_11_F"]

    def phi_f(num: int, den: int) -> int:                    # Φ_F(num/den) = Σ_b χ₈(b) Φ⁻(num/den + b/8)
        return sum(CHI8[b] * symbol(lam, (num * m + b * den) % (den * m), den * m) for b in CHI8) % P

    bad = 0
    for a in range(1, P):
        lhs = sum(phi_f(a + P * b, P * P) for b in range(P)) % P
        rhs = (a11f * phi_f(a, P) - phi_f(a, 1)) % P
        bad += lhs != rhs
    return {"a_11_F": a11f, "failures": bad, "agrees": bad == 0}


# ------------------------------------------------------------ the Eisenstein series

def bernoulli_polynomial(n: int, x: Fraction) -> Fraction:
    table = {0: [Fraction(1)], 1: [Fraction(-1, 2), Fraction(1)], 2: [Fraction(1, 6), Fraction(-1), Fraction(1)]}
    if n not in table:
        raise ValueError(n)
    return sum(c * x ** k for k, c in enumerate(table[n]))


def eisenstein_data() -> dict:
    f = 8
    b2 = f * sum(CHI8.get(a, 0) * bernoulli_polynomial(2, Fraction(a, f)) for a in range(1, f + 1))
    b2_theirs = 8 * sum(CHI8.get(a, 0) * (Fraction(a * a, 64) - Fraction(a, 8) + Fraction(1, 6)) for a in range(1, 9))
    const = -b2 / 4
    bound = 12 * P
    a_f = [0] + [sum(CHI8.get(d % 8, 0) * d for d in range(1, n + 1) if n % d == 0) for n in range(1, bound + 1)]
    a_beta = [0] + [a_f[n] - (a_f[n // P] if n % P == 0 else 0) for n in range(1, bound + 1)]
    a11 = a_f[P]
    hecke = (1, a11, CHI8.get(P % 8, 0) * P)                 # U² − a₁₁U + χ₈(11)·11
    roots = sorted(x for x in range(-P, P + 1) if x * x - a11 * x + CHI8.get(P % 8, 0) * P == 0)
    residuals = [a_beta[P * n] - EISENSTEIN_REFINEMENT * a_beta[n] for n in range(1, 13)]
    th = their_result()["eisenstein"]
    return {"B2_chi8": str(b2), "B2_by_their_formula": str(b2_theirs), "constant_term": str(const),
            "a_11": a11, "hecke_polynomial_coefficients": hecke, "hecke_roots": roots,
            "f_beta_coefficients_1_to_32": a_beta[1:33], "U11_residuals_1_to_12": residuals,
            "theirs_coefficients_match": a_beta[1:33] == th["critical_q_coefficients_n_1_to_32"],
            "theirs_residuals_match": residuals == th["U11_residuals_n_1_to_12"],
            "decency_data": {"chi8_even": CHI8[7] == 1 and CHI8[1] == 1, "chi8_nontrivial": -1 in CHI8.values(),
                             "chi8_of_11": CHI8.get(P % 8, 0), "conductor": f},
            "agrees": (b2 == STATED["B2_chi8"] and b2_theirs == b2 and const == STATED["constant_term"]
                       and roots == sorted(STATED["hecke_roots"]) and all(r == 0 for r in residuals)
                       and a_beta[1:33] == th["critical_q_coefficients_n_1_to_32"]
                       and CHI8.get(P % 8, 0) == -1)}


# ------------------------------------------------------------ the Kummer unit in Z[√2]

def zmul(x, y):                                            # (a + b√2)(c + d√2)
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def zpow(x, k):
    r = (1, 0)
    for _ in range(k):
        r = zmul(r, x)
    return r


def kummer_unit() -> dict:
    eps = UNIT
    norm = eps[0] ** 2 - 2 * eps[1] ** 2
    conj = (eps[0], -eps[1])
    sigma_relation = zmul(eps, conj) == (-1, 0)              # ε·ε^σ = −1, i.e. ε^σ = −ε⁻¹
    e24 = zpow(eps, UNIT_POWER)
    mod121 = (e24[0] % 121, e24[1] % 121)
    u = (Fraction(e24[0] - 1), Fraction(e24[1]))              # ε²⁴ − 1, exact
    in_11O = e24[0] % P == 1 and e24[1] % P == 0
    # log(1 + u) = u − u²/2 + u³/3 − …, exact in Q(√2) to LOG_TERMS terms, then the tail bound
    log24 = (Fraction(0), Fraction(0))
    upow = (Fraction(1), Fraction(0))
    for m in range(1, LOG_TERMS + 1):
        upow = zmul(upow, u)
        sign = 1 if m % 2 else -1
        log24 = (log24[0] + sign * upow[0] / m, log24[1] + sign * upow[1] / m)

    def red(fr: Fraction, mod: int) -> int:
        if fr.denominator % P == 0:
            raise ValueError("not 11-integral")
        return fr.numerator * pow(fr.denominator, -1, mod) % mod

    log24_mod = (red(log24[0], 121), red(log24[1], 121))
    higher_terms_vanish_mod_121 = all(red(Fraction(x), 121) == 0 for x in
                                      (zmul(u, u)[0] / 2, zmul(u, u)[1] / 2))
    inv24 = pow(UNIT_POWER, -1, 121)
    log_eps = (log24_mod[0] * inv24 % 121, log24_mod[1] * inv24 % 121)
    over = log_eps[1] // P % P if log_eps[1] % P == 0 and log_eps[0] == 0 else None   # log ε/(11√2) mod 11
    two_nonsquare = pow(2, (P - 1) // 2, P) == P - 1
    return {"epsilon": eps, "norm": norm, "sigma_is_minus_inverse": sigma_relation,
            "epsilon_power_exact": e24, "epsilon_power_mod_121": mod121, "power_minus_one_in_11O": in_11O,
            "log_terms_used": LOG_TERMS, "higher_terms_vanish_mod_121": higher_terms_vanish_mod_121,
            "log_epsilon_mod_121": log_eps, "log_over_11_sqrt2_mod_11": over, "two_is_a_nonsquare_mod_11": two_nonsquare,
            "agrees": (norm == -1 and sigma_relation and e24 == STATED["epsilon_power_exact"]
                       and mod121 == STATED["epsilon_power_mod_121"] and in_11O and higher_terms_vanish_mod_121
                       and log_eps == STATED["log_epsilon_mod_121"] and over == STATED["log_over_11_sqrt2_mod_11"]
                       and two_nonsquare)}


# ------------------------------------------------------------ the other factors and the formal algebra

def factors(lam8: int) -> dict:
    d = SMOOTHING_D
    chi_d = CHI8.get(d % 8, 0)
    smoothing = d * d - (chi_d if chi_d else 0)               # χ₈(d)⁻¹ = χ₈(d) for a quadratic character
    coprime = math.gcd(d, 6 * 8 * N * P) == 1
    alpha = unit_root()["alpha"]
    ainv = pow(alpha, P - 2, P)
    adjoint = (1 - 0) * (1 - ainv * ainv) % P                 # (1 − β/α)(1 − β/(11α)) with β = 11/α: (1 − 11α⁻²)(1 − α⁻²)
    a0_de = smoothing * lam8 % P
    return {"smoothing_d": d, "chi8_of_d": chi_d, "smoothing_factor": smoothing, "d_coprime": coprime,
            "adjoint_euler_mod_11": adjoint, "A0_times_DE_mod_11": a0_de,
            "agrees": (smoothing == STATED["smoothing"] and coprime and adjoint == STATED["adjoint_euler_mod_11"]
                       and a0_de == STATED["A0_times_DE_mod_11"])}


def _pmul(f: dict, g: dict) -> dict:
    out: dict = {}
    for (m1, d1), c1 in f.items():
        for (m2, d2), c2 in g.items():
            key = (tuple(sorted(m1 + m2)), d1 + d2)
            out[key] = out.get(key, Fraction(0)) + c1 * c2
    return {k: v for k, v in out.items() if v}


def formal_algebra() -> dict:
    """scaled_B = C·A(t)·log(1+t)·z(t) with A = A0 + A1 t, z = κ0 t + κ1 t², log(1+t) = t − t²/2 + t³/3;
    Col = C·A(t)·log(1+t)·(a2 t²). Keys are (sorted monomial, t-degree)."""
    C = {(("C",), 0): Fraction(1)}
    A = {(("A0",), 0): Fraction(1), (("A1",), 1): Fraction(1)}
    LOG = {((), 1): Fraction(1), ((), 2): Fraction(-1, 2), ((), 3): Fraction(1, 3)}
    Z = {(("kappa0",), 1): Fraction(1), (("kappa1",), 2): Fraction(1)}
    COL = {(("a2",), 2): Fraction(1)}
    cls = _pmul(_pmul(_pmul(C, A), LOG), Z)
    col = _pmul(_pmul(_pmul(C, A), LOG), COL)

    def degree(poly: dict, d: int) -> dict:
        return {m: c for (m, dd), c in poly.items() if dd == d}

    lowest_cls = min(dd for (_m, dd) in cls)
    lowest_col = min(dd for (_m, dd) in col)
    d2, d3, r3 = degree(cls, 2), degree(cls, 3), degree(col, 3)
    return {"class_lowest_degree": lowest_cls, "class_degree_2": {"*".join(m): str(c) for m, c in d2.items()},
            "class_degree_3": {"*".join(m): str(c) for m, c in d3.items()},
            "regulator_lowest_degree": lowest_col, "regulator_degree_3": {"*".join(m): str(c) for m, c in r3.items()},
            "agrees": (lowest_cls == 2 and lowest_col == 3 and d2 == STATED["class_degree_2"]
                       and d3 == STATED["class_degree_3"] and r3 == STATED["regulator_degree_3"])}


def scale_identities(trials: int = 200) -> dict:
    """(19) ⇒ (1) is a rearrangement; (20) needs h(x, adj(H)ℓ) = det(H)·ℓ(x) for h(x, y) = xᵀHy, and 416 = 16·26."""
    rng = random.Random(RANDOM_SEED)
    bad = 0
    for _ in range(trials):
        h11, h12, h22 = (Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(3))
        det = h11 * h22 - h12 * h12
        if det == 0:
            continue
        ell = [Fraction(rng.randint(-9, 9)) for _ in range(2)]
        x = [Fraction(rng.randint(-9, 9)) for _ in range(2)]
        adj_ell = [h22 * ell[0] - h12 * ell[1], -h12 * ell[0] + h11 * ell[1]]
        h_adj = [h11 * adj_ell[0] + h12 * adj_ell[1], h12 * adj_ell[0] + h22 * adj_ell[1]]
        lhs = x[0] * h_adj[0] + x[1] * h_adj[1]
        rhs = det * (x[0] * ell[0] + x[1] * ell[1])
        bad += lhs != rhs
        # (19) → (1) → (20) with random nonzero scalars
        C_, lam8, DE, log12, s11, kappa = (Fraction(rng.randint(1, 9)) for _ in range(6))
        B2 = 26 * C_ * lam8 * kappa / (DE * log12)              # (19), scalar shadow
        bad += kappa != log12 * DE * B2 / (26 * C_ * lam8)      # (1)
        # (3): κ† = 16·s₁₁·adj(H)ℓ, so h(x, κ†) = 16 s₁₁ det(H) ℓ(x); with κ† ∝ B₂ by (19):
        h_x_B2 = B2 / kappa * (16 * s11 * det * (x[0] * ell[0] + x[1] * ell[1]))
        recovered = log12 * DE / (416 * C_ * lam8) * h_x_B2 / (det * (x[0] * ell[0] + x[1] * ell[1])) if (x[0] * ell[0] + x[1] * ell[1]) else s11
        bad += recovered != s11
    return {"trials": trials, "failures": bad, "constant_416": 16 * 26,
            "agrees": bad == 0 and 16 * 26 == STATED["constant_416"]}


# ------------------------------------------------------------ the package's criterion on other characters

def lambda_D_at_zero(D: int, lam_minus: list[int], lam_plus: list[int]) -> dict:
    """L₁₁(E ⊗ χ_D, x⁻¹) mod 11 the package's way: Φ_F(r) = Σ_b χ_D(b)Φ^∓(r + b/|D|) on the line of
    parity opposite to χ_D (x⁻¹ is odd), α_F = χ_D(11)·α_E, λ_D(0) ≡ α_F⁻¹ Σ_a a⁻¹ Φ_F(a/11)."""
    m = abs(D)
    lam = lam_minus if D > 0 else lam_plus
    alpha = unit_root()["alpha"]
    chi11 = atk78.kronecker(D, P)
    a_f = chi11 * alpha % P
    ainv = pow(a_f, P - 2, P)
    total = 0
    for a in range(1, P):
        phi = sum(atk78.kronecker(D, b) * symbol(lam, (a * m + P * b) % (P * m), P * m)
                  for b in range(1, m) if math.gcd(b, m) == 1) % P
        total += pow(a, P - 2, P) * phi
    return {"D": D, "chi_D_of_11": chi11, "alpha_F": a_f, "lambda_D_at_zero": ainv * total % P}


def package_criterion() -> dict:
    lm = eigenline(-1)["lambda"]
    lp = eigenline(1)["lambda"]
    rows = [lambda_D_at_zero(D, lm, lp) for D in atk78.fundamental_discriminants() if D > 0]
    rows.insert(0, lambda_D_at_zero(8, lm, lp)) if not any(r["D"] == 8 for r in rows) else None
    nonzero = [r["D"] for r in rows if r["lambda_D_at_zero"]]
    zero = [r["D"] for r in rows if not r["lambda_D_at_zero"]]
    at8 = next(r for r in rows if r["D"] == 8)
    at5 = next(r for r in rows if r["D"] == 5)
    return {"rows": rows, "nonzero_D": nonzero, "zero_D": zero, "chi8": at8, "chi5": at5,
            "agrees": at8["lambda_D_at_zero"] == STATED["lambda8"]}


# ------------------------------------------------------------ labels and comparison

def labels() -> dict:
    text = DOC.read_text(encoding="utf-8")
    th = their_result()
    phrases = {"not_the_central_value": "不能把式 (8) 改成平凡分支的中心值，也不能把它等同於複數" in text,
               "bsd_not_proved": "BSD 尚未證明" in text, "frontier_unchanged": "canonical frontier 不更新" in text,
               "C_B2_s11_uncomputed": "尚未完成" in text and "尚未計算的量" in text,
               "theorem_cited_not_proved": "使用已發表的退化定理，並非本輪程式已算出" in text}
    out = th["open"]
    json_labels = {"C_value_null": out["C_value"] is None, "n_value_null": out["n_value"] is None,
                   "B2_null": out["B2_coordinates"] is None, "s11_null": out["s11"] is None,
                   "BSD_proved_false": out["BSD_proved"] is False,
                   "frontier_false": out["canonical_frontier_updated"] is False,
                   "scope_noncritical": "not the central complex L-value" in th["shifted_twisted_moment"]["scope"]}
    return {"text": phrases, "json": json_labels, "agrees": all(phrases.values()) and all(json_labels.values())}


def compare_with_theirs(fp: dict, ed: dict, ku: dict, fa: dict, fo: dict) -> dict:
    th = their_result()
    m = th["shifted_twisted_moment"]
    checks = {"lambda8": m["lambda8_at_zero_mod11"] == fp["lambda8_at_zero"],
              "weighted_sum": m["weighted_unstabilized_sum_mod11"] == fp["weighted_sum"],
              "alpha_twist": m["alpha_twist_mod11"] == alpha_twist()["alpha_F"],
              "twisted_symbol_at_zero": m["twisted_symbol_at_zero"] == fp["twisted_symbol_at_zero"],
              "path_count": m["new_cusp_path_count"] == fp["paths"],
              "paths": fp["paths_identical_to_theirs"] == 40, "symbols": fp["symbols_identical_to_theirs"] == 40,
              "B2": Fraction(th["eisenstein"]["B2_chi8"]) == Fraction(ed["B2_chi8"]),
              "constant_term": Fraction(th["eisenstein"]["constant_term"]) == Fraction(ed["constant_term"]),
              "U11": th["eisenstein"]["critical_U11"] == EISENSTEIN_REFINEMENT,
              "coefficients": ed["theirs_coefficients_match"], "residuals": ed["theirs_residuals_match"],
              "epsilon_power": tuple(th["unit_anchor"]["epsilon_power_exact"]) == ku["epsilon_power_exact"],
              "epsilon_mod_121": tuple(th["unit_anchor"]["epsilon_power_mod_121"]) == ku["epsilon_power_mod_121"],
              "log_mod_121": tuple(th["unit_anchor"]["log_epsilon_mod_121"]) == ku["log_epsilon_mod_121"],
              "log_over_11_sqrt2": th["unit_anchor"]["log_epsilon_over_11_sqrt2_mod_11"] == ku["log_over_11_sqrt2_mod_11"],
              "smoothing": th["invertible_factors"]["C5_at_zero"] == fa["smoothing_factor"],
              "adjoint": th["invertible_factors"]["adjoint_Euler_factor_mod11"] == fa["adjoint_euler_mod_11"],
              "A0DE": th["invertible_factors"]["A0_times_D_E_mod11"] == fa["A0_times_DE_mod_11"],
              "formal": (th["formal_leading_calculation"]["class_first_coefficient_degree"] == fo["class_lowest_degree"]
                         and th["formal_leading_calculation"]["regulator_first_coefficient_degree"] == fo["regulator_lowest_degree"]
                         and {"*".join(sorted(e["monomial"])): Fraction(e["coefficient"]) for e in th["formal_leading_calculation"]["class_degree_3"]}
                         == {k: Fraction(v) for k, v in fo["class_degree_3"].items()})}
    return {"checks": checks, "agrees": all(checks.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    ml = minus_line()
    print(f"  minus line: dims {ml['dimensions']}, first nonzero {ml['first_nonzero_index']}, identical to theirs: {ml['identical_to_theirs']}")
    fp = forty_paths()
    print(f"  forty paths: S_a {fp['S_a']}, mu {fp['mu']}, sum {fp['weighted_sum']}, lambda8(0) = {fp['lambda8_at_zero']}, "
          f"Phi_F(0) = {fp['twisted_symbol_at_zero']}; paths identical {fp['paths_identical_to_theirs']}/40, "
          f"symbols {fp['symbols_identical_to_theirs']}/40; RUN-076 T9- = {fp['run076_T9_minus']} = -8^9*sum: {fp['T9_equals_minus_8_pow_9_times_sum']}")
    hm = hecke_measure_relation()
    print(f"  Hecke relation at level 121 for the twisted symbols: a_11(F) = {hm['a_11_F']}, failures {hm['failures']}")
    ed = eisenstein_data()
    print(f"  Eisenstein: B2 = {ed['B2_chi8']}, constant {ed['constant_term']}, Hecke {ed['hecke_polynomial_coefficients']} roots {ed['hecke_roots']}, "
          f"coefficients match {ed['theirs_coefficients_match']}, residuals {ed['U11_residuals_1_to_12']}")
    ku = kummer_unit()
    print(f"  unit: norm {ku['norm']}, eps^24 = {ku['epsilon_power_exact']} = {ku['epsilon_power_mod_121']} mod 121, "
          f"log eps = {ku['log_epsilon_mod_121']} mod 121, /(11 sqrt2) = {ku['log_over_11_sqrt2_mod_11']} mod 11")
    fa = factors(fp["lambda8_at_zero"])
    print(f"  factors: smoothing {fa['smoothing_factor']}, adjoint Euler {fa['adjoint_euler_mod_11']}, A0*D_E {fa['A0_times_DE_mod_11']}")
    fo = formal_algebra()
    print(f"  formal: class degrees {fo['class_lowest_degree']}: {fo['class_degree_2']} / {fo['class_degree_3']}; regulator {fo['regulator_lowest_degree']}: {fo['regulator_degree_3']}")
    si = scale_identities()
    pc = package_criterion()
    print(f"  the package's criterion lambda_D(0) != 0 on the even D: nonzero {pc['nonzero_D']}; zero {pc['zero_D']}; chi_5: {pc['chi5']['lambda_D_at_zero']}")
    lab = labels()
    cmp_ = compare_with_theirs(fp, ed, ku, fa, fo)
    ok = all(x["agrees"] for x in (ml, fp, hm, ed, ku, fa, fo, si, pc, lab, cmp_)) and alpha_twist()["agrees"]
    out = {"gate": "src79", "round": "RUN-077", "minus_line": ml, "alpha_twist": alpha_twist(), "forty_paths": fp,
           "hecke_measure_relation": hm, "eisenstein": ed, "kummer_unit": ku, "factors": fa, "formal_algebra": fo,
           "scale_identities": si, "package_criterion": pc, "labels": lab, "comparison": cmp_, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  comparison: {cmp_['checks']}")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
