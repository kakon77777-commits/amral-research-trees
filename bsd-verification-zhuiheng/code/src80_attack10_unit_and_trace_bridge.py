"""Gate 80 — GPT-6's Attack 10: the circular unit in Z[ζ₈], its 11-adic logarithm to 11¹⁰, the Leopoldt value L₁₁(1, χ₈) ≡ 5, the filtered-Frobenius entry q_bot ≡ 9, the Bernoulli cross-check B_{10,χ₈}, and the first-order trace algebra on 676 pairs — every finite statement recomputed; the 1-motive, the Selmer identification and the family-level inputs read.

數學戰士「墜衡」 / AMRAL Research Lab.

Attack 10 builds two objects around Attack 09's unknown period C: a
norm-one 1-motive [Z → Res¹_{Q(√2)/Q} G_m], 1 ↦ 17 − 12√2, whose 11-adic
filtered Frobenius matrix it calibrates exactly, and a trace-reconstruction
formula with an explicit null-homotopy of the cup product b_ε ∪ β in a
weight family. Its finite content, recomputed here with its own arithmetic:

  * in Z[ζ₈]/(ζ₈⁴ + 1), r = ζ₈ − ζ₈³ has r² = 2; (1 − ζ₈)(1 − ζ₈⁷) = 2 − r,
    (1 − ζ₈³)(1 − ζ₈⁵) = 2 + r, so u₈ = 3 − 2r = ε⁻², ε = 1 + r; u_bot = u₈² =
    17 − 12r = ε⁻⁴; N(ε) = −1, N(u₈) = N(u_bot) = 1; G(χ₈) = 2r;
  * L(1, χ₈) = log(1 + √2)/√2 = 0.6232252401… three ways (the Gauss-sum log
    formula, the Dirichlet series in blocks of 8, the class-number formula);
  * u_bot⁶ = 768398401 − 543339720√2, w = u_bot⁶ − 1 ∈ 11·O, log(u_bot⁶) =
    Σ_{m≤19} (−1)^{m+1} w^m/m exactly in Q(√2), the omitted terms of valuation
    ≥ 19: L_bot ≡ 8662686351, L_ε ≡ 17287396863 (mod 11¹⁰), v₁₁(L_ε) = 1,
    L_ε/11 ≡ 1571581533, L₁₁^std(1, χ₈) = (12/11)L_ε ≡ 2353344559,
    q_bot = −(12/11)L_bot ≡ 2339535163 (mod 11⁹); L₁₁^std ≡ 5, q_bot ≡ 9
    (mod 11); q_bot = 4·L₁₁^std; and L_ε ≡ 55 (mod 121) — Attack 09's
    log₁₁ ε ≡ 55√2, read from the other end of the same series;
  * B_{10,χ₈} = 28730410, −B₁₀/10 ≡ 5 (mod 11), the Kubota–Leopoldt value
    L₁₁(−9, χ₈) mod 11 agreeing with L₁₁(1, χ₈) mod 11 as it must;
  * the framed Frobenius matrix [[−1/11, q],[0, 1]] with q = −(12/11)L_bot,
    from φ = diag(−1/11, 1) and Fil⁰ = ⟨d₀ + L_bot d_χ⟩;
  * the model ρ(a), ρ(b), ρ(J) over Q[X]/(X²), the 26 reduced words of length
    ≤ 2 in Free(a, b) ∗ C₂, and on all 676 pairs: a_g = (T(g) − T(Jg))/2,
    Q(g, h) = b_ε(g)v(h), b_ε ∪ β = −δF, the two cocycle relations, rank ≤ 1,
    Q(a,a) = 15, Q(a,b) = 21, v(a) = 5 and v(b) = 7 from either pivot; the
    variant with lower entries 8X, 9X giving Q(a,a) = 24, Q(a,b) = 27 — the
    package's 676-row table matched row by row.

Read, not verified: the Tate realisation of the 1-motive and its extension
class, D_cris(T) and the Bloch–Kato logarithm convention, the Selmer space
H¹_f(Q, T) being spanned by Kum(ε), the reducibility ideal (X) and
Loeffler–Rivero §A5–A6, the J-eigenbasis argument. The package computes no
Coleman trace jet, no n, no C, no B₂, no 𝔰₁₁, and says so.

Usage:  python code/src80_attack10_unit_and_trace_bridge.py
"""

from __future__ import annotations

import itertools
import json
import math
import pathlib
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "10"
DOC = EXT / "BSD_Proof_Attack_10_Unit_and_Trace_Bridge.md"
THEIR_RESULT = EXT / "attack10_result.json"
OUT = LOGS / "src80-attack10-unit-and-trace-bridge.json"

P = 11
PRECISION = 10                                             # log to 11^PRECISION
CHI8 = {1: 1, 3: -1, 5: -1, 7: 1}

# --- the arithmetic the drill may disturb ---------------------------------------
ROOT2_IN_ZETA8 = (0, 1, 0, -1)                              # r = ζ − ζ³
CIRCLE_EXPONENTS = ((1, 7), (3, 5))                         # numerator (1−ζ^1)(1−ζ^7), denominator (1−ζ^3)(1−ζ^5)
BOTTOM_NORM_EXPONENT = 2                                    # 1 − χ₈(11) = 2
BOTTOM_POWER = 6                                            # u_bot⁶ ≡ 1 (mod 11)
LOG_TERMS = 2 * PRECISION - 1                               # the series to m = 19
FROBENIUS_SUB_EIGENVALUE = Fraction(-1, 11)                 # φ on d_χ
EULER_TWELVE_ELEVENTHS = Fraction(12, 11)                   # (1 + 1/11) in Leopoldt's formula
BERNOULLI_N = 10
MODEL_LOWER = (5, 7)                                        # the X-coefficients of the lower-left entries of ρ(a), ρ(b)
SERIES_BLOCKS = 100_000

STATED = {"u8": (3, -2), "u_bot": (17, -12), "gauss": (0, 2, 0, -2), "norms": (-1, 1, 1),
          "kummer_multiple": -4, "L1_chi8": 0.6232252401402305,
          "bottom_power_6": (768398401, -543339720), "L_bot": 8662686351, "L_eps": 17287396863,
          "L_eps_valuation": 1, "L_eps_over_11": 1571581533, "Lp_std_1": 2353344559, "q_bot": 2339535163,
          "Lp_std_mod_11": 5, "q_bot_mod_11": 9, "L_eps_mod_121": 55,
          "B10": 28730410, "minus_B10_over_10": -2873041, "Lp_minus_9_mod_11": 5,
          "Q_aa": 15, "Q_ab": 21, "v_a": 5, "v_b": 7, "alt_Q_aa": 24, "alt_Q_ab": 27, "words": 26, "pairs": 676}


def their_result() -> dict:
    return json.loads(THEIR_RESULT.read_text(encoding="utf-8"))


# ------------------------------------------------------------ Z[ζ₈]

def cmul(x, y):
    """Product in Z[ζ]/(ζ⁴ + 1), coefficients of 1, ζ, ζ², ζ³."""
    out = [0] * 4
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            k = i + j
            if k >= 4:
                out[k - 4] -= a * b
            else:
                out[k] += a * b
    return tuple(out)


def cpow(x, k):
    r = (1, 0, 0, 0)
    for _ in range(k):
        r = cmul(r, x)
    return r


ZETA = (0, 1, 0, 0)


def one_minus_zeta_power(k: int):
    z = cpow(ZETA, k)
    return (1 - z[0], -z[1], -z[2], -z[3])


def zmul(x, y):                                            # in Z[√2]
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def zpow(x, k):
    r = (1, 0)
    for _ in range(k):
        r = zmul(r, x)
    return r


def znorm(x):
    return x[0] * x[0] - 2 * x[1] * x[1]


def embed(x):                                              # a + b√2 ↦ a + b·r in Z[ζ₈]
    r = ROOT2_IN_ZETA8
    return tuple(x[0] * (1 if i == 0 else 0) + x[1] * r[i] for i in range(4))


def circular_unit() -> dict:
    r = ROOT2_IN_ZETA8
    r2 = cmul(r, r)
    num = cmul(one_minus_zeta_power(CIRCLE_EXPONENTS[0][0]), one_minus_zeta_power(CIRCLE_EXPONENTS[0][1]))
    den = cmul(one_minus_zeta_power(CIRCLE_EXPONENTS[1][0]), one_minus_zeta_power(CIRCLE_EXPONENTS[1][1]))
    u8 = (3, -2)
    quotient_ok = cmul(embed(u8), den) == num                # u₈·den = num, i.e. u₈ = num/den
    eps = (1, 1)
    eps2 = zmul(eps, eps)
    u8_is_eps_minus_2 = zmul(u8, eps2) == (1, 0)
    ubot = zpow(u8, BOTTOM_NORM_EXPONENT)
    ubot_is_eps_minus_4 = zmul(ubot, zpow(eps, 4)) == (1, 0)
    gauss = tuple(sum(CHI8[a] * cpow(ZETA, a)[i] for a in CHI8) for i in range(4))
    gauss_is_2r = gauss == tuple(2 * c for c in r)
    norms = (znorm(eps), znorm(u8), znorm(ubot))
    return {"r_squared": r2, "numerator": num, "denominator": den, "numerator_is_2_minus_r": num == embed((2, -1)),
            "denominator_is_2_plus_r": den == embed((2, 1)), "u8": u8, "u8_is_num_over_den": quotient_ok,
            "u8_is_epsilon_minus_2": u8_is_eps_minus_2, "u_bot": ubot, "u_bot_is_epsilon_minus_4": ubot_is_eps_minus_4,
            "kummer_multiple_of_epsilon": -2 * BOTTOM_NORM_EXPONENT, "gauss_sum": gauss, "gauss_is_2r": gauss_is_2r,
            "norms_epsilon_u8_ubot": norms,
            "agrees": (r2 == (2, 0, 0, 0) and quotient_ok and u8 == STATED["u8"] and u8_is_eps_minus_2
                       and ubot == STATED["u_bot"] and ubot_is_eps_minus_4 and gauss == STATED["gauss"]
                       and norms == STATED["norms"] and -2 * BOTTOM_NORM_EXPONENT == STATED["kummer_multiple"])}


# ------------------------------------------------------------ the real regulator

def real_regulator() -> dict:
    r = math.sqrt(2)
    by_class_number = math.log(1 + r) / r
    by_gauss = -sum(CHI8[a] * math.log(abs(1 - complex(math.cos(2 * math.pi * a / 8), math.sin(2 * math.pi * a / 8))))
                    for a in CHI8) / (2 * r)
    series = 0.0
    for k in range(SERIES_BLOCKS):
        series += sum(CHI8[a] / (8 * k + a) for a in CHI8)   # blocks of 8: Σ χ₈(a)·a = 0, so the tail is O(1/K²)
    reg_ratio = -4 * math.log(1 + r) / r                     # log|u_bot|/r = −4 log(1+r)/r, (7)
    return {"by_class_number_formula": by_class_number, "by_gauss_sum_logs": by_gauss, "by_series": series,
            "series_blocks": SERIES_BLOCKS, "log_u_bot_over_r": reg_ratio,
            "equals_minus_4_L": abs(reg_ratio + 4 * by_class_number) < 1e-12,
            "agrees": (abs(by_gauss - by_class_number) < 1e-12 and abs(series - by_class_number) < 1e-8
                       and abs(by_class_number - STATED["L1_chi8"]) < 1e-12)}


# ------------------------------------------------------------ the 11-adic logarithm

def red(fr: Fraction, mod: int) -> int:
    if fr.denominator % P == 0:
        raise ValueError("not 11-integral")
    return fr.numerator * pow(fr.denominator, -1, mod) % mod


def padic_log() -> dict:
    modN = P ** PRECISION
    modN1 = P ** (PRECISION - 1)
    ubot = circular_unit()["u_bot"]
    u6 = zpow(ubot, BOTTOM_POWER)
    w = (Fraction(u6[0] - 1), Fraction(u6[1]))
    in_11O = (u6[0] - 1) % P == 0 and u6[1] % P == 0
    if not in_11O:                                           # the series does not converge: red, not a crash
        return {"u_bot_power_6": u6, "w_in_11O": False, "series_terms": [], "L_bot": None, "L_eps": None,
                "L_eps_valuation": None, "L_eps_over_11": None, "Lp_std_1_chi8": None, "q_bot": None,
                "q_bot_is_4_Lp": False, "Lp_mod_11": None, "q_bot_mod_11": None, "L_eps_mod_121": None, "agrees": False}
    total = (Fraction(0), Fraction(0))
    upow = (Fraction(1), Fraction(0))
    terms = []
    for m in range(1, LOG_TERMS + 1):
        upow = zmul(upow, w)
        sign = 1 if m % 2 else -1
        term = (sign * upow[0] / m, sign * upow[1] / m)
        total = (total[0] + term[0], total[1] + term[1])
        terms.append({"m": m, "residues": (red(term[0], modN), red(term[1], modN))})
    log6 = (red(total[0], modN), red(total[1], modN))
    # log(u_bot) = log(u_bot⁶)/6; L_bot = log(u_bot)/√2 is the √2-coordinate
    inv6 = pow(BOTTOM_POWER, -1, modN)
    log_bot = (log6[0] * inv6 % modN, log6[1] * inv6 % modN)
    L_bot = log_bot[1]
    L_eps = (-L_bot * pow(4, -1, modN)) % modN               # L_bot = −4 L_ε
    val = 0
    x = L_eps
    while x % P == 0 and x:
        x //= P
        val += 1
    L_eps_over_11 = (L_eps // P) % modN1 if L_eps % P == 0 else None
    Lp = None if L_eps_over_11 is None else (EULER_TWELVE_ELEVENTHS.numerator * L_eps_over_11) % modN1
    q_bot = None if L_bot % P else (-EULER_TWELVE_ELEVENTHS.numerator * (L_bot // P)) % modN1
    four_Lp = None if Lp is None else 4 * Lp % modN1
    tail_ok = all(m - (1 if m % P == 0 else 0) >= PRECISION for m in range(LOG_TERMS + 1, LOG_TERMS + 200))
    return {"u_bot_power_6": u6, "w_in_11O": in_11O, "terms_used": LOG_TERMS, "first_omitted": LOG_TERMS + 1,
            "tail_valuation_bound_holds": tail_ok, "log_u_bot_6_mod_11N": log6,
            "log_u_bot_first_coordinate_zero": log_bot[0] == 0, "L_bot": L_bot, "L_eps": L_eps,
            "L_eps_valuation": val, "L_eps_over_11": L_eps_over_11, "Lp_std_1_chi8": Lp, "q_bot": q_bot,
            "q_bot_is_4_Lp": q_bot == four_Lp, "Lp_mod_11": None if Lp is None else Lp % P,
            "q_bot_mod_11": None if q_bot is None else q_bot % P, "L_eps_mod_121": L_eps % 121,
            "series_terms": terms,
            "agrees": (u6 == STATED["bottom_power_6"] and in_11O and tail_ok and log_bot[0] == 0
                       and L_bot == STATED["L_bot"] and L_eps == STATED["L_eps"] and val == STATED["L_eps_valuation"]
                       and L_eps_over_11 == STATED["L_eps_over_11"] and Lp == STATED["Lp_std_1"]
                       and q_bot == STATED["q_bot"] and q_bot == four_Lp and Lp % P == STATED["Lp_std_mod_11"]
                       and q_bot % P == STATED["q_bot_mod_11"] and L_eps % 121 == STATED["L_eps_mod_121"])}


# ------------------------------------------------------------ Bernoulli

def bernoulli_numbers(n: int) -> list[Fraction]:
    B = [Fraction(0)] * (n + 1)
    B[0] = Fraction(1)
    for m in range(1, n + 1):
        B[m] = -sum(math.comb(m + 1, k) * B[k] for k in range(m)) / (m + 1)
    return B


def bernoulli_polynomial(n: int, x: Fraction, B: list[Fraction]) -> Fraction:
    return sum(math.comb(n, k) * B[k] * x ** (n - k) for k in range(n + 1))


def bernoulli_check() -> dict:
    n = BERNOULLI_N
    B = bernoulli_numbers(n)
    f = 8
    Bn = f ** (n - 1) * sum(CHI8.get(a, 0) * bernoulli_polynomial(n, Fraction(a, f), B) for a in range(1, f + 1))
    B2 = f * sum(CHI8.get(a, 0) * bernoulli_polynomial(2, Fraction(a, f), B) for a in range(1, f + 1))
    minus_over_n = -Bn / n
    euler = 1 + P ** (n - 1)                                 # (1 − χ₈(11)·11^{n−1}), χ₈(11) = −1
    lp = red(Fraction(euler) * minus_over_n, P)
    return {"n": n, "B_n_chi8": str(Bn), "B_2_chi8": str(B2), "minus_B_n_over_n": str(minus_over_n),
            "euler_factor": euler, "Lp_1_minus_n_mod_11": lp, "B_1_is_minus_half": B[1] == Fraction(-1, 2),
            "agrees": (Bn == STATED["B10"] and minus_over_n == STATED["minus_B10_over_10"]
                       and lp == STATED["Lp_minus_9_mod_11"] and B2 == 2)}


# ------------------------------------------------------------ the Frobenius matrix

def frobenius_matrix(L_bot_value: Fraction = Fraction(8662686351)) -> dict:
    """φ = diag(λ, 1) in (d_χ, d₀), Fil⁰ = ⟨h⟩, h = d₀ + L d_χ; in (d_χ, h): φ(h) = d₀ + Lλ d_χ = h + (λ − 1)L d_χ."""
    lam = FROBENIUS_SUB_EIGENVALUE
    L = L_bot_value
    q = (lam - 1) * L
    stated_q = -Fraction(12, 11) * L
    eigen_minus_one = lam - 1
    return {"phi_sub": str(lam), "q": str(q), "q_is_minus_12_over_11_L": q == stated_q,
            "phi_minus_1_on_subline": str(eigen_minus_one), "invertible": eigen_minus_one != 0,
            "agrees": q == stated_q and eigen_minus_one != 0}


# ------------------------------------------------------------ the trace algebra over Q[X]/(X²)

class D2:
    """2×2 matrices over Q[X]/(X²): (M0, M1) with M = M0 + X·M1."""

    def __init__(self, m0, m1):
        self.m0 = [[Fraction(v) for v in row] for row in m0]
        self.m1 = [[Fraction(v) for v in row] for row in m1]

    @staticmethod
    def _mm(a, b):
        return [[a[i][0] * b[0][j] + a[i][1] * b[1][j] for j in range(2)] for i in range(2)]

    @staticmethod
    def _add(a, b):
        return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]

    def __mul__(self, o):
        return D2(self._mm(self.m0, o.m0), self._add(self._mm(self.m0, o.m1), self._mm(self.m1, o.m0)))

    def inverse(self):
        a, b, c, d = self.m0[0][0], self.m0[0][1], self.m0[1][0], self.m0[1][1]
        det = a * d - b * c
        inv0 = [[d / det, -b / det], [-c / det, a / det]]
        inv1 = [[-v for v in row] for row in self._mm(self._mm(inv0, self.m1), inv0)]
        return D2(inv0, inv1)

    def trace(self):
        return (self.m0[0][0] + self.m0[1][1], self.m1[0][0] + self.m1[1][1])


def model(lower=None) -> dict[str, D2]:
    if lower is None:
        lower = MODEL_LOWER
    a = D2([[2, 3], [0, 1]], [[7, 13], [lower[0], 11]])
    b = D2([[3, 2], [0, 1]], [[17, 19], [lower[1], 23]])
    j = D2([[-1, 0], [0, 1]], [[0, 0], [0, 0]])
    return {"a": a, "A": a.inverse(), "b": b, "B": b.inverse(), "j": j}


def words() -> list[str]:
    gens = ["a", "A", "b", "B", "j"]
    inv = {"a": "A", "A": "a", "b": "B", "B": "b", "j": "j"}
    out = ["1"] + gens
    for g, h in itertools.product(gens, gens):
        if inv[g] != h:
            out.append(g + h)
    return out


def evaluate(word: str, gens: dict[str, D2]) -> D2:
    m = D2([[1, 0], [0, 1]], [[0, 0], [0, 0]])
    for ch in word:
        if ch != "1":
            m = m * gens[ch]
    return m


def trace_algebra(lower=None) -> dict:
    gens = model(MODEL_LOWER if lower is None else lower)
    W = words()
    rho = {w: evaluate(w, gens) for w in W}
    xi = {w: rho[w].m0[0][0] for w in W}
    A_ = {w: rho[w].m1[0][0] for w in W}
    b_eps = {w: rho[w].m0[0][1] for w in W}
    v = {w: rho[w].m1[1][0] for w in W}
    beta = {w: v[w] / xi[w] for w in W}
    F = {w: A_[w] / xi[w] for w in W}
    structure_ok = all(rho[w].m0[1][0] == 0 and rho[w].m0[1][1] == 1 for w in W)   # lower-left ≡ 0 mod X, d_g(0) = 1
    # (21): a_g(X) = (T(g) − T(Jg))/2
    t21 = 0
    for w in W:
        tg, tjg = rho[w].trace(), (gens["j"] * rho[w]).trace()
        t21 += ((tg[0] - tjg[0]) / 2 == xi[w]) and ((tg[1] - tjg[1]) / 2 == A_[w])
    rows, ok22, ok24, cocycle_b, cocycle_v = [], 0, 0, 0, 0
    Qmat = []
    for g in W:
        row = []
        for h in W:
            gh = rho[g] * rho[h]
            A_gh, b_gh, v_gh = gh.m1[0][0], gh.m0[0][1], gh.m1[1][0]
            Q = A_gh - xi[g] * A_[h] - xi[h] * A_[g]
            cup = b_eps[g] / xi[g] * beta[h]
            F_gh = A_gh / (xi[g] * xi[h])
            minus_delta_F = -(F[h] - F_gh + F[g])
            ok22 += Q == b_eps[g] * v[h]
            ok24 += cup == minus_delta_F
            cocycle_b += b_gh == b_eps[g] + xi[g] * b_eps[h]
            cocycle_v += v_gh == v[g] * xi[h] + v[h]
            rows.append({"g": g, "h": h, "Q": str(Q), "cup": str(cup), "minus_delta_F": str(minus_delta_F)})
            row.append(Q)
        Qmat.append(row)
    # rank ≤ 1: every 2×2 minor vanishes
    n = len(W)
    rank_le_1 = all(Qmat[i][j] * Qmat[k][l] - Qmat[i][l] * Qmat[k][j] == 0
                    for i in range(n) for k in range(i + 1, n) for j in range(n) for l in range(j + 1, n))
    # reconstruction (23) from the pivots a and b
    recon = {}
    for pivot in ("a", "b"):
        recon[pivot] = {h: (A_[pivot + h] if pivot + h in rho else (rho[pivot] * rho[h]).m1[0][0]) for h in W}
        recon[pivot] = {h: ((rho[pivot] * rho[h]).m1[0][0] - xi[pivot] * A_[h] - xi[h] * A_[pivot]) / (b_eps[pivot] * xi[h])
                        for h in W}
    recon_ok = all(recon["a"][h] == beta[h] and recon["b"][h] == beta[h] for h in W)
    Q_aa = Qmat[W.index("a")][W.index("a")]
    Q_ab = Qmat[W.index("a")][W.index("b")]
    return {"words": len(W), "pairs": len(rows), "structure": structure_ok, "identity_21": t21 == len(W),
            "identity_22": ok22 == len(rows), "identity_24": ok24 == len(rows),
            "cocycle_b": cocycle_b == len(rows), "cocycle_v": cocycle_v == len(rows), "rank_le_1": rank_le_1,
            "reconstruction_from_both_pivots": recon_ok, "Q_aa": str(Q_aa), "Q_ab": str(Q_ab),
            "v_a": str(v["a"]), "v_b": str(v["b"]), "b_eps_a": str(b_eps["a"]), "b_eps_b": str(b_eps["b"]),
            "rows": rows, "beta": {w: str(beta[w]) for w in W}, "A_over_xi": {w: str(F[w]) for w in W},
            "agrees": (len(W) == STATED["words"] and len(rows) == STATED["pairs"] and structure_ok and t21 == len(W)
                       and ok22 == len(rows) and ok24 == len(rows) and cocycle_b == len(rows) and cocycle_v == len(rows)
                       and rank_le_1 and recon_ok)}


# ------------------------------------------------------------ labels and comparison

def labels() -> dict:
    text = DOC.read_text(encoding="utf-8")
    th = their_result()
    phrases = {"no_trace_jet_no_C": "尚未計算真實 Coleman 族的 trace jet 或 meromorphic Eichler–Shimura 常數" in text,
               "model_is_not_galois_data": "模型不是 Galois 數據" in text,
               "period_not_identified_with_C": "尚未被識別為 Attack 09 的族插值常數" in text,
               "shortcut_rejected": "把式 (14) 的 unit 稱為 $C$，會跳過上表第二個比較箭頭，因此不成立" in text,
               "bsd_not_proved": "BSD 尚未證明；canonical frontier 不更新" in text}
    st = th["status"]
    json_labels = {"trace_jets_null": st["actual_Coleman_trace_jets"] is None, "n_null": st["meromorphic_ES_order_n"] is None,
                   "C_null": st["period_C"] is None, "B2_null": st["Beilinson_Flach_B2_coordinates"] is None,
                   "s11_null": st["s11"] is None, "BSD_proved_false": st["BSD_proved"] is False,
                   "frontier_false": st["canonical_frontier_updated"] is False,
                   "period_C_computed_false": th["local_crystalline_calibration"]["period_C_computed"] is False,
                   "model_labelled": "EXACT ALGEBRA MODEL" in th["first_order_trace_algebra"]["data_kind"]}
    return {"text": phrases, "json": json_labels, "agrees": all(phrases.values()) and all(json_labels.values())}


def compare_with_theirs(cu: dict, pl: dict, bc: dict, ta: dict, alt: dict) -> dict:
    th = their_result()
    c = th["circular_unit"]
    lc = th["local_crystalline_calibration"]
    fo = th["first_order_trace_algebra"]
    theirs_rows = {(r["g"], r["h"]): r for r in fo["trace_tensor_rows"]}
    mine_rows = {(r["g"], r["h"]): r for r in ta["rows"]}
    rows_match = (set(theirs_rows) == set(mine_rows)
                  and all(Fraction(theirs_rows[k]["Q"]) == Fraction(mine_rows[k]["Q"])
                          and Fraction(theirs_rows[k]["cup"]) == Fraction(mine_rows[k]["cup"])
                          and Fraction(theirs_rows[k]["minus_delta_F"]) == Fraction(mine_rows[k]["minus_delta_F"])
                          for k in theirs_rows))
    recon_match = all(Fraction(e["beta"]) == Fraction(ta["beta"][e["word"]]) and Fraction(e["A_over_xi"]) == Fraction(ta["A_over_xi"][e["word"]])
                      and Fraction(e["v_from_a"]) == Fraction(e["v_from_b"]) for e in fo["opposite_reconstruction"])
    my_terms = {t["m"]: t["residues"] for t in pl["series_terms"]}
    terms_match = all(tuple(t["term_residues"]) == my_terms.get(t["m"]) for t in lc["series_terms"])
    checks = {"unit_quotient": tuple(c["unit_quotient"]) == embed(cu["u8"]), "u_chi": tuple(c["u_chi_in_Z_sqrt2"]) == cu["u8"],
              "bottom": tuple(c["bottom_unit_in_Z_sqrt2"]) == cu["u_bot"], "gauss": tuple(c["gauss_sum"]) == cu["gauss_sum"],
              "kummer_multiple": c["bottom_Kummer_multiple_of_epsilon"] == cu["kummer_multiple_of_epsilon"],
              "norms": (c["norms"]["epsilon"], c["norms"]["u_chi"], c["norms"]["bottom"]) == cu["norms_epsilon_u8_ubot"],
              "bottom_power_6": tuple(lc["bottom_power_6"]) == pl["u_bot_power_6"], "series_terms_19": terms_match,
              "L_bot": lc["L_bottom_mod_pN"] == pl["L_bot"], "L_eps": lc["L_epsilon_mod_pN"] == pl["L_eps"],
              "valuation": lc["L_epsilon_exact_valuation"] == pl["L_eps_valuation"],
              "L_eps_over_11": lc["L_epsilon_div_p_mod"] == pl["L_eps_over_11"],
              "Lp": lc["Leopoldt_Lp_1_chi_mod"] == pl["Lp_std_1_chi8"], "q_bot": lc["phi_offdiag_bottom_mod"] == pl["q_bot"],
              "q_bot_mod_11": lc["phi_offdiag_bottom_mod_p"] == pl["q_bot_mod_11"], "Lp_mod_11": lc["Leopoldt_Lp_mod_p"] == pl["Lp_mod_11"],
              "B10": Fraction(th["new_Bernoulli_normalization_check"]["B_n_chi"]) == Fraction(bc["B_n_chi8"]),
              "Lp_minus_9": th["new_Bernoulli_normalization_check"]["Lp_1_minus_n_mod_p"] == bc["Lp_1_minus_n_mod_11"],
              "words_pairs": (fo["word_count"], fo["pair_count"]) == (ta["words"], ta["pairs"]),
              "Q_aa_ab": (Fraction(fo["Q_a_a"]), Fraction(fo["Q_a_b"])) == (Fraction(ta["Q_aa"]), Fraction(ta["Q_ab"])),
              "all_676_rows": rows_match, "reconstruction_26": recon_match,
              "alternative_model": (Fraction(th["alternative_algebra_model"]["Q_a_a"]), Fraction(th["alternative_algebra_model"]["Q_a_b"]))
              == (Fraction(alt["Q_aa"]), Fraction(alt["Q_ab"]))}
    return {"checks": checks, "agrees": all(checks.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    cu = circular_unit()
    print(f"  Z[zeta8]: r^2 = {cu['r_squared']}, num = 2 - r: {cu['numerator_is_2_minus_r']}, den = 2 + r: {cu['denominator_is_2_plus_r']}, "
          f"u8 = {cu['u8']} = eps^-2: {cu['u8_is_epsilon_minus_2']}, u_bot = {cu['u_bot']} = eps^-4: {cu['u_bot_is_epsilon_minus_4']}, "
          f"G(chi8) = 2r: {cu['gauss_is_2r']}, norms {cu['norms_epsilon_u8_ubot']}")
    rr = real_regulator()
    print(f"  L(1, chi8): class number {rr['by_class_number_formula']:.15f}, Gauss logs {rr['by_gauss_sum_logs']:.15f}, series {rr['by_series']:.12f}")
    pl = padic_log()
    print(f"  11-adic: u_bot^6 = {pl['u_bot_power_6']}, L_bot = {pl['L_bot']}, L_eps = {pl['L_eps']} (v = {pl['L_eps_valuation']}), "
          f"L_eps/11 = {pl['L_eps_over_11']}, Lp(1,chi8) = {pl['Lp_std_1_chi8']} (= {pl['Lp_mod_11']} mod 11), "
          f"q_bot = {pl['q_bot']} (= {pl['q_bot_mod_11']} mod 11), q_bot = 4 Lp: {pl['q_bot_is_4_Lp']}, L_eps mod 121 = {pl['L_eps_mod_121']}")
    bc = bernoulli_check()
    print(f"  Bernoulli: B_10,chi8 = {bc['B_n_chi8']}, -B/10 = {bc['minus_B_n_over_n']}, Lp(-9) mod 11 = {bc['Lp_1_minus_n_mod_11']}; B_2,chi8 = {bc['B_2_chi8']}")
    fm = frobenius_matrix()
    print(f"  Frobenius: q = (lambda - 1) L = -12/11 L: {fm['q_is_minus_12_over_11_L']}")
    ta = trace_algebra()
    alt = trace_algebra((8, 9))
    print(f"  trace algebra: {ta['words']} words, {ta['pairs']} pairs; (21) {ta['identity_21']}, (22) {ta['identity_22']}, (24) {ta['identity_24']}, "
          f"cocycles {ta['cocycle_b']}/{ta['cocycle_v']}, rank<=1 {ta['rank_le_1']}, both pivots {ta['reconstruction_from_both_pivots']}; "
          f"Q(a,a) = {ta['Q_aa']}, Q(a,b) = {ta['Q_ab']}, v(a) = {ta['v_a']}, v(b) = {ta['v_b']}; alternative Q(a,a) = {alt['Q_aa']}, Q(a,b) = {alt['Q_ab']}")
    lab = labels()
    cmp_ = compare_with_theirs(cu, pl, bc, ta, alt)
    print(f"  comparison: {cmp_['checks']}")
    ok = (cu["agrees"] and rr["agrees"] and pl["agrees"] and bc["agrees"] and fm["agrees"] and ta["agrees"]
          and Fraction(alt["Q_aa"]) == STATED["alt_Q_aa"] and Fraction(alt["Q_ab"]) == STATED["alt_Q_ab"]
          and Fraction(ta["Q_aa"]) == STATED["Q_aa"] and Fraction(ta["Q_ab"]) == STATED["Q_ab"]
          and Fraction(ta["v_a"]) == STATED["v_a"] and Fraction(ta["v_b"]) == STATED["v_b"]
          and lab["agrees"] and cmp_["agrees"])
    out = {"gate": "src80", "round": "RUN-078", "circular_unit": cu, "real_regulator": rr, "padic_log": pl,
           "bernoulli": bc, "frobenius": fm, "trace_algebra": {k: v for k, v in ta.items() if k != "rows"},
           "alternative_model": {k: v for k, v in alt.items() if k not in ("rows", "beta", "A_over_xi")},
           "labels": lab, "comparison": cmp_, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
