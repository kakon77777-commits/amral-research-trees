"""Gate 82 — PC-001 (the local GPT-6 line's cross-curve calibration): the rank-0 calibrator 19.a1 rebuilt over Q from the Manin relations at level 19 — the 3-dimensional space, the plus and minus rational eigenlines (identical to the line's primitive vectors), five Hecke checks against point counts, the first-layer ordinary and χ₈-twisted measures at 11 and every stated residue; the calibration identity read as RUN-079's (4.4); and a supplement the line lists as not done — the archimedean alignment of both modular-symbol periods with the Néron period, one unit per sign.

數學戰士「墜衡」 / AMRAL Research Lab.

PC-001 (branch agent/bsd-period-calibration, commit 002e5d5) chooses the
calibrator E₀ = 19.a1: y² + y = x³ + x² − 769x − 8470, rank 0, a₁₁ = 3
(ordinary at 11), builds its modular symbols over Q from the twenty Manin
generators of P¹(F₁₉), separates the cusp form from the Eisenstein T₂
eigenvalue 3, and computes at the first layer: α₀ ≡ 3, the ordinary
measures, L₁₁(E₀, 1) ≡ 9, the χ₈-twisted x⁻¹ value L₁₁(E₀ ⊗ χ₈, x⁻¹) ≡ 4
from the cusp sums (4,4,0,2,9,2,9,0,7,7), the smoothing 26 ≡ 4, the
adjoint multiplier 7, and the product of the three nonzero factors 1.

Recomputed here with an independent rational Manin engine (dense exact
elimination over Q, its own continued fractions, its own point counts):
the dimension 3, the T₂ eigenvalues 0 (cusp, twice) and 3 (Eisenstein),
the primitive integer plus vector (2, 0, 6, 6, 3, −3, −6, 0, 0, −6, −6, 0,
0, −6, −3, 3, 6, 6, 0, −2) and minus vector (0,0,0,0,1,1,0,…,0,−1,−1,0,0,0,0)
— identical — the Hecke eigenvalues −2, 3, −1, 3, −4 at 3, 5, 7, 11, 13
against point counts, and every residue in the line's table, with the
distribution relation at level 121 for both measures. The level-17
remark: a₁₁(17.a1) = 0, supersingular, as the line says.

The supplement. The line writes that its modular-symbol periods "must still
be matched to the Kato/adjoint conventions" and does not identify them with
Néron periods. The archimedean half of that is done here as at RUN-076:
for every even fundamental D ≤ 100 prime to 11·19 with root number
χ_D(−19) = +1, L(E₀, χ_D, 1)·√D/Ω⁺(E₀) is computed from the a_n and comes
out an exact rational; one unit λ₀⁺ carries these residues onto the
plus-line twisted sums at the line's normalisation (coordinate 0 ↦ 1).
For the odd D (root number +1) the minus-line sums are matched, through
ratios that cancel the imaginary period, by one unit λ₀⁻. So both of the
line's normalisations are Néron normalisations up to a unit at 11, and
"nonzero mod 11" in its table is nonzero at the Néron scale.

Read, not verified: Loeffler–Rivero C1.9–C1.13 and the common quotient
transport; the identification of B_{E,2} and r_{0,1} with genuine
Beilinson–Flach data (the line says these are not constructed); the
Kato/Coleman/adjoint alignment beyond the archimedean one.

Usage:  python code/src82_pc001_calibrator_19a1.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src15_phase2_anchor as anchor15                    # noqa: E402  Ω by AGM
import src78_attack09_auxiliary_character as atk78        # noqa: E402  kronecker, fundamental discriminants

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-local-period-calibration"
DOC = EXT / "reports" / "PC-001-CROSS-CURVE-CALIBRATION.md"
REVIEW = EXT / "reports" / "PC-001-REVIEW.md"
THEIRS = EXT / "data" / "calibrator-19a1.json"
OUT = LOGS / "src82-pc001-calibrator-19a1.json"

P = 11
N0 = 19
AINVS0 = [0, 1, 1, -769, -8470]                            # 19.a1 (LMFDB) = 19a2 (Cremona)
AINVS17 = [1, -1, 1, -1, -14]                              # 17.a1, the partner the line rejected
CHI8 = {1: 1, 3: -1, 5: -1, 7: 1}
D_LIMIT = 100
BOUND = 4000
TAIL_EXPONENT = 45.0

# --- the arithmetic the drill may disturb ---------------------------------------
HECKE_PRIMES = (3, 5, 7, 11, 13)
PLUS_NORMALISATION_INDEX = 0                               # the line: plus coordinate 0 ↦ 1 (primitive has 2)
MINUS_NORMALISATION_INDEX = 4                              # the line: minus coordinate 4 ↦ 1
TWIST_SIGN = -1                                            # α_F = χ₈(11)·α₀ = −α₀
CHARACTER_EXPONENT = -1                                    # the moment against x⁻¹
SMOOTHING_D = 5
MEASURE_SECOND_TERM_SIGN = -1
EISENSTEIN_T2 = 3                                          # 1 + 2

STATED = {"dimension": 3, "traces": {2: 0, 3: -2, 5: 3, 7: -1, 11: 3, 13: -4},
          "plus_primitive": [2, 0, 6, 6, 3, -3, -6, 0, 0, -6, -6, 0, 0, -6, -3, 3, 6, 6, 0, -2],
          "minus_primitive": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
          "plus_mod11": [1, 0, 3, 3, 7, 4, 8, 0, 0, 8, 8, 0, 0, 8, 4, 7, 3, 3, 0, 10],
          "minus_mod11": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 0, 0, 0, 0],
          "alpha": 3, "alpha_twist": 8, "plus_at_zero": 1,
          "ordinary_measures": [10, 6, 3, 10, 3, 3, 10, 3, 6, 10], "ordinary_central": 9,
          "twisted_sums": [4, 4, 0, 2, 9, 2, 9, 0, 7, 7], "twisted_weighted": 10, "twisted_x_inverse": 4,
          "wrong_x_moment": 8, "smoothing_mod11": 4, "adjoint": 7, "product": 1, "a11_of_17a1": 0}


def their_json() -> dict:
    return json.loads(THEIRS.read_text(encoding="utf-8"))


# ------------------------------------------------------------ a rational Manin engine at prime level N

class Manin:
    """Manin symbols (c:d) ∈ P¹(F_N), generators (1:t), t < N, and (0:1) at index N; relations
    x + Sx = 0 and x + Rx + R²x = 0 with S(c,d) = (d, −c), R(c,d) = (d, −c−d); Hecke by Merel's
    matrices acting on the bottom row; ι(c:d) = (−c:d). Exact linear algebra over Q."""

    def __init__(self, N: int):
        self.N = N

    def index(self, c: int, d: int) -> int:
        N = self.N
        c %= N
        d %= N
        if c:
            return d * pow(c, N - 2, N) % N
        if d == 0:
            raise ValueError("(0:0)")
        return N

    def rep(self, i: int) -> tuple[int, int]:
        return (1, i) if i < self.N else (0, 1)

    def relation_rows(self) -> list[dict[int, int]]:
        rows = []
        for i in range(self.N + 1):
            c, d = self.rep(i)
            s: dict[int, int] = {}
            for j in (i, self.index(d, -c)):
                s[j] = s.get(j, 0) + 1
            rows.append(s)
            r: dict[int, int] = {}
            for j in (i, self.index(d, -c - d), self.index(-c - d, c)):
                r[j] = r.get(j, 0) + 1
            rows.append(r)
        return rows

    @staticmethod
    def merel(q: int) -> list[tuple[int, int, int, int]]:
        out = []
        for a in range(1, q + 1):
            for b in range(0, a):
                for c in range(0, q + 1):
                    num = q + b * c
                    if num % a:
                        continue
                    d = num // a
                    if d > c:
                        out.append((a, b, c, d))
        return out

    def hecke_rows(self, q: int) -> list[dict[int, int]]:
        ms = self.merel(q)
        rows = []
        for i in range(self.N + 1):
            c, d = self.rep(i)
            r: dict[int, int] = {}
            for a, b, cc, dd in ms:
                j = self.index(c * a + d * cc, c * b + d * dd)
                r[j] = r.get(j, 0) + 1
            rows.append(r)
        return rows

    def iota(self, i: int) -> int:
        c, d = self.rep(i)
        return self.index(-c, d)

    @staticmethod
    def apply(rows: list[dict[int, int]], v: list[Fraction]) -> list[Fraction]:
        return [sum(coef * v[j] for j, coef in r.items()) for r in rows]

    @staticmethod
    def nullspace_q(rows: list[list[Fraction]], ncols: int) -> list[list[Fraction]]:
        """Basis of {v : row·v = 0 for every row}, exact over Q."""
        m = [list(r) for r in rows]
        piv_cols = []
        r = 0
        for c in range(ncols):
            pr = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
            if pr is None:
                continue
            m[r], m[pr] = m[pr], m[r]
            inv = 1 / m[r][c]
            m[r] = [x * inv for x in m[r]]
            for i in range(len(m)):
                if i != r and m[i][c] != 0:
                    f = m[i][c]
                    m[i] = [x - f * y for x, y in zip(m[i], m[r])]
            piv_cols.append(c)
            r += 1
            if r == len(m):
                break
        free = [c for c in range(ncols) if c not in piv_cols]
        basis = []
        for f in free:
            v = [Fraction(0)] * ncols
            v[f] = Fraction(1)
            for i, c in enumerate(piv_cols):
                v[c] = -m[i][f]
            basis.append(v)
        return basis

    def dual_space(self) -> list[list[Fraction]]:
        """Functionals on the generators vanishing on the relations."""
        rows = []
        for rel in self.relation_rows():
            row = [Fraction(0)] * (self.N + 1)
            for j, v in rel.items():
                row[j] += v
            rows.append(row)
        return self.nullspace_q(rows, self.N + 1)

    def eigenspace(self, basis: list[list[Fraction]], hecke: list[dict[int, int]], a: int) -> list[list[Fraction]]:
        """Vectors in span(basis) with T_q v = a·v, in the generator coordinates."""
        images = [self.apply(hecke, b) for b in basis]
        rows = []
        for i in range(self.N + 1):
            rows.append([images[k][i] - a * basis[k][i] for k in range(len(basis))])
        coords = self.nullspace_q(rows, len(basis))
        return [[sum(mu[k] * basis[k][i] for k in range(len(basis))) for i in range(self.N + 1)] for mu in coords]

    def sign_space(self, basis: list[list[Fraction]], sign: int) -> list[list[Fraction]]:
        rows = []
        for i in range(self.N + 1):
            j = self.iota(i)
            if j == i:
                continue
            rows.append([basis[k][i] - sign * basis[k][j] for k in range(len(basis))])
        coords = self.nullspace_q(rows, len(basis))
        return [[sum(mu[k] * basis[k][i] for k in range(len(basis))) for i in range(self.N + 1)] for mu in coords]

    def path_indices(self, a: int, n: int) -> list[int]:
        out = [self.index(1, 0)]
        num, den = a, n
        a0 = num // den
        num -= a0 * den
        p_prev2, q_prev2 = 1, 0
        p_prev, q_prev = a0, 1
        i = 1
        while num:
            k, r = divmod(den, num)
            p_new, q_new = k * p_prev + p_prev2, k * q_prev + q_prev2
            out.append(self.index(q_new, (1 if (i - 1) % 2 == 0 else -1) * q_prev))
            p_prev2, q_prev2, p_prev, q_prev = p_prev, q_prev, p_new, q_new
            den, num = num, r
            i += 1
        return out

    def symbol(self, lam: list, a: int, n: int, mod: int | None = None):
        val = sum(lam[i] for i in self.path_indices(a % n, n))
        return val % mod if mod else val


def primitive(v: list[Fraction]) -> list[int]:
    den = 1
    for x in v:
        den = den * x.denominator // math.gcd(den, x.denominator)
    ints = [int(x * den) for x in v]
    g = 0
    for x in ints:
        g = math.gcd(g, abs(x))
    ints = [x // g for x in ints]
    first = next(x for x in ints if x)
    return ints if first > 0 else [-x for x in ints]


# ------------------------------------------------------------ the curve

def b_invariants(a: list[int]) -> tuple[int, int, int, int]:
    a1, a2, a3, a4, a6 = a
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return b2, b4, b6, b8


def a_p(a: list[int], p: int) -> int:
    """p + 1 − #E(F_p) by the Legendre symbol of 4x³ + b₂x² + 2b₄x + b₆ (p odd), direct count at 2."""
    if p == 2:
        a1, a2, a3, a4, a6 = (c % 2 for c in a)
        n = 1
        for x in range(2):
            for y in range(2):
                if (y * y + a1 * x * y + a3 * y - (x ** 3 + a2 * x * x + a4 * x + a6)) % 2 == 0:
                    n += 1
        return 3 - n
    b2, b4, b6, _b8 = b_invariants(a)
    sq = bytearray(p)
    for y in range(p):
        sq[y * y % p] = 1
    s = 0
    for x in range(p):
        v = (4 * x ** 3 + b2 * x * x + 2 * b4 * x + b6) % p
        if v:
            s += 1 if sq[v] else -1
    return -s


def a_n_table(a: list[int], bound: int, bad: int) -> list[int]:
    primes = [q for q in range(2, bound + 1) if all(q % r for r in range(2, int(q ** 0.5) + 1))]
    ap = {q: a_p(a, q) for q in primes}
    spf = list(range(bound + 1))
    for q in primes:
        for m in range(q, bound + 1, q):
            if spf[m] == m:
                spf[m] = q
    an = [0] * (bound + 1)
    an[1] = 1
    for n in range(2, bound + 1):
        q = spf[n]
        m, k = n, 0
        while m % q == 0:
            m //= q
            k += 1
        if q == bad:
            aq = ap[q] ** k
        else:
            x0, x1 = 1, ap[q]
            for _ in range(k - 1):
                x0, x1 = x1, ap[q] * x1 - q * x0
            aq = x1
        an[n] = aq * an[m]
    return an


# ------------------------------------------------------------ the calibrator's modular symbols

def calibrator_lines() -> dict:
    M = Manin(N0)
    dual = M.dual_space()
    traces = {q: a_p(AINVS0, q) for q in (2,) + HECKE_PRIMES}
    h2 = M.hecke_rows(2)
    cusp = M.eigenspace(dual, h2, traces[2])
    eis = M.eigenspace(dual, h2, EISENSTEIN_T2)
    plus = M.sign_space(cusp, 1)
    minus = M.sign_space(cusp, -1)
    out = {"dimension": len(dual), "genus": 1, "traces": traces, "cusp_dimension": len(cusp),
           "eisenstein_dimension": len(eis), "plus_dimension": len(plus), "minus_dimension": len(minus)}
    if len(plus) != 1 or len(minus) != 1:
        out["agrees"] = False
        return out
    pv, mv = primitive(plus[0]), primitive(minus[0])
    hecke_ok = {}
    for q in HECKE_PRIMES:
        H = M.hecke_rows(q)
        hecke_ok[q] = (M.apply(H, [Fraction(x) for x in pv]) == [Fraction(traces[q] * x) for x in pv]
                       and M.apply(H, [Fraction(x) for x in mv]) == [Fraction(traces[q] * x) for x in mv])
    pm = [x * pow(pv[PLUS_NORMALISATION_INDEX], -1, P) % P for x in pv]
    mm = [x * pow(mv[MINUS_NORMALISATION_INDEX], -1, P) % P for x in mv]
    th = their_json()
    out.update({"plus_primitive": pv, "minus_primitive": mv, "plus_mod11": pm, "minus_mod11": mm,
                "hecke_checks": hecke_ok,
                "plus_identical_to_theirs": pv == th["plus_line"]["primitive_integer_vector"],
                "minus_identical_to_theirs": mv == th["minus_line"]["primitive_integer_vector"],
                "plus_mod11_identical": pm == th["plus_line"]["mod11_vector"],
                "minus_mod11_identical": mm == th["minus_line"]["mod11_vector"],
                "agrees": (len(dual) == STATED["dimension"] and len(cusp) == 2 and len(eis) == 1
                           and traces == STATED["traces"] and all(hecke_ok.values())
                           and pv == STATED["plus_primitive"] and mv == STATED["minus_primitive"]
                           and pm == STATED["plus_mod11"] and mm == STATED["minus_mod11"])})
    return out


def measures(lines: dict | None = None) -> dict:
    if lines is None:
        lines = calibrator_lines()
    M = Manin(N0)
    pm, mm = lines["plus_mod11"], lines["minus_mod11"]
    a11 = lines["traces"][11]
    roots = [x for x in range(P) if (x * x - a11 * x + P) % P == 0]
    alpha = [x for x in roots if x][0]
    ainv = pow(alpha, P - 2, P)
    alpha_t = (TWIST_SIGN * alpha) % P
    atinv = pow(alpha_t, P - 2, P)
    plus_zero = M.symbol(pm, 0, 1, P)
    ordinary = [(ainv * M.symbol(pm, a, P, P) + MEASURE_SECOND_TERM_SIGN * ainv * ainv * plus_zero) % P for a in range(1, P)]
    central = sum(ordinary) % P
    euler_central = pow(1 - ainv, 2, P) * plus_zero % P

    def phi_chi(num: int, den: int) -> int:                # Φ_χ₈(num/den) = Σ_b χ₈(b) Φ⁻(num/den + b/8)
        return sum(CHI8[b] * M.symbol(mm, (num * 8 + b * den) % (den * 8), den * 8, P) for b in CHI8) % P

    twisted_sums = [phi_chi(a, P) for a in range(1, P)]
    phi_zero = phi_chi(0, 1)
    weight = {a: (pow(a, P - 2, P) if CHARACTER_EXPONENT == -1 else pow(a, CHARACTER_EXPONENT % (P - 1), P)) for a in range(1, P)}
    weighted = sum(weight[a] * s for a, s in zip(range(1, P), twisted_sums)) % P
    x_inverse_value = atinv * weighted % P
    wrong = atinv * sum(a * s for a, s in zip(range(1, P), twisted_sums)) % P
    # distribution relation at level 121 for both measures
    residuals = []
    for a in range(1, P):
        fine_ord = sum((ainv * ainv * M.symbol(pm, a + P * b, P * P, P) + MEASURE_SECOND_TERM_SIGN * ainv ** 3 * M.symbol(pm, a + P * b, P, P))
                       for b in range(P)) % P
        fine_tw = sum((atinv * atinv * phi_chi(a + P * b, P * P) + MEASURE_SECOND_TERM_SIGN * atinv ** 3 * phi_chi(a + P * b, P))
                      for b in range(P)) % P
        coarse_tw = (atinv * twisted_sums[a - 1] + MEASURE_SECOND_TERM_SIGN * atinv * atinv * phi_zero) % P
        residuals.append([(fine_ord - ordinary[a - 1]) % P, (fine_tw - coarse_tw) % P])
    smoothing = SMOOTHING_D * SMOOTHING_D - CHI8.get(SMOOTHING_D % 8, 0)
    adjoint = (1 - ainv * ainv) % P                        # (1 − 11α⁻²)(1 − α⁻²) mod 11
    product = central * x_inverse_value * (smoothing % P) % P
    return {"a_11": a11, "alpha": alpha, "alpha_twist": alpha_t, "plus_at_zero": plus_zero,
            "ordinary_first_layer_measures": ordinary, "ordinary_central_value": central,
            "central_by_euler_factor": euler_central, "twisted_cusp_sums": twisted_sums, "twisted_symbol_at_zero": phi_zero,
            "twisted_weighted_sum": weighted, "twisted_x_inverse_value": x_inverse_value, "wrong_x_moment": wrong,
            "distribution_residuals": residuals, "smoothing": smoothing, "smoothing_mod11": smoothing % P,
            "adjoint_euler_multiplier": adjoint, "nonvanishing_product": product,
            "agrees": (alpha == STATED["alpha"] and alpha_t == STATED["alpha_twist"] and plus_zero == STATED["plus_at_zero"]
                       and ordinary == STATED["ordinary_measures"] and central == STATED["ordinary_central"]
                       and central == euler_central and twisted_sums == STATED["twisted_sums"] and phi_zero == 0
                       and weighted == STATED["twisted_weighted"] and x_inverse_value == STATED["twisted_x_inverse"]
                       and wrong == STATED["wrong_x_moment"] and all(r == [0, 0] for r in residuals)
                       and smoothing % P == STATED["smoothing_mod11"] and adjoint == STATED["adjoint"]
                       and product == STATED["product"])}


def level_17_remark() -> dict:
    a11 = a_p(AINVS17, 11)
    return {"a_11_of_17a1": a11, "supersingular_at_11": a11 == 0, "agrees": a11 == STATED["a11_of_17a1"]}


# ------------------------------------------------------------ the supplement: archimedean alignment

def periods() -> dict:
    b2, b4, b6, _b8 = b_invariants(AINVS0)
    disc = -b2 * b2 * _b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return {"discriminant": disc, "omega_plus": anchor15.real_period(AINVS0)}


def archimedean_alignment(lines: dict | None = None) -> dict:
    """Even D: A_D = L(E₀, χ_D, 1)√D/Ω⁺ rational, one unit λ₀⁺ onto the plus sums (line's scale).
    Odd D: ratios L(χ_D)√|D| / L(χ_{D₀})√|D₀| (the period cancels) against the minus sums, one unit."""
    if lines is None:
        lines = calibrator_lines()
    M = Manin(N0)
    pm, mm = lines["plus_mod11"], lines["minus_mod11"]
    an = a_n_table(AINVS0, BOUND, N0)
    per = periods()
    rows = []
    for D in [1] + [d for d in atk78.fundamental_discriminants(D_LIMIT) if d % N0 != 0]:
        m = abs(D)
        w = (1 if D > 0 else -1) * (atk78.kronecker(D, N0) if D != 1 else 1)
        if w != 1:
            continue
        k = 2 * math.pi / math.sqrt(N0 * m * m)
        nmax = min(BOUND, int(TAIL_EXPONENT / k) + 1)
        chi = [0] + [(atk78.kronecker(D, n) if D != 1 else 1) for n in range(1, nmax + 1)]
        L = 2 * sum(an[n] * chi[n] * math.exp(-k * n) / n for n in range(1, nmax + 1) if an[n] and chi[n])
        lam = pm if D > 0 else mm
        S = sum((atk78.kronecker(D, b) if D != 1 else 1) * M.symbol(lam, b, m, P) for b in range(1, m + 1) if math.gcd(b, m) == 1) % P if m > 1 else M.symbol(pm, 0, 1, P)
        rows.append({"D": D, "w": w, "terms": nmax, "L": L, "L_sqrtD": L * math.sqrt(m), "S": S})
    # plus: A_D = L√D/Ω⁺ recognised as rationals
    unit_plus, plus_ok, plus_pairs = None, True, []
    for r in rows:
        if r["D"] > 0:
            A = r["L_sqrtD"] / per["omega_plus"]
            fr = Fraction(A).limit_denominator(64)
            rec = abs(A - float(fr)) < 1e-9 * max(1.0, abs(A)) and fr.denominator % P != 0
            r["A"] = A
            r["A_rational"] = f"{fr.numerator}/{fr.denominator}"
            r["recognised"] = rec
            plus_ok &= rec
            A_mod = fr.numerator * pow(fr.denominator, -1, P) % P if rec else None
            plus_pairs.append((r["D"], A_mod, r["S"]))
    for D, A_mod, S in plus_pairs:
        if A_mod:
            unit_plus = S * pow(A_mod, -1, P) % P
            break
    plus_ok &= unit_plus is not None and all(A_mod is not None and (unit_plus * A_mod - S) % P == 0 for _D, A_mod, S in plus_pairs)
    # minus: ratios against the smallest odd D with a nonzero value
    minus_rows = [r for r in rows if r["D"] < 0]
    ref = next((r for r in minus_rows if abs(r["L_sqrtD"]) > 1e-9 and r["S"]), None)
    unit_minus_ok, minus_pairs = ref is not None, []
    if ref is not None:
        for r in minus_rows:
            rho = r["L_sqrtD"] / ref["L_sqrtD"]
            fr = Fraction(rho).limit_denominator(64)
            rec = abs(rho - float(fr)) < 1e-9 * max(1.0, abs(rho)) and fr.denominator % P != 0
            r["ratio_to_reference"] = f"{fr.numerator}/{fr.denominator}"
            r["recognised"] = rec
            rho_mod = fr.numerator * pow(fr.denominator, -1, P) % P if rec else None
            minus_pairs.append((r["D"], rho_mod, r["S"]))
            unit_minus_ok &= rec and rho_mod is not None and (r["S"] - rho_mod * ref["S"]) % P == 0
    return {"omega_plus": per["omega_plus"], "discriminant": per["discriminant"], "rows": rows,
            "plus_unit": unit_plus, "plus_pairs": plus_pairs, "plus_consistent": plus_ok,
            "minus_reference_D": ref["D"] if ref else None, "minus_pairs": minus_pairs, "minus_consistent": unit_minus_ok,
            "nonzero_plus": sum(1 for _D, A, _S in plus_pairs if A), "nonzero_minus": sum(1 for _D, r, _S in minus_pairs if r),
            "agrees": plus_ok and unit_minus_ok and sum(1 for _D, A, _S in plus_pairs if A) >= 3
            and sum(1 for _D, r, _S in minus_pairs if r) >= 3}


# ------------------------------------------------------------ labels

def labels() -> dict:
    text = DOC.read_text(encoding="utf-8")
    review = REVIEW.read_text(encoding="utf-8")
    th = their_json()
    phrases = {"no_bsd": "沒有得到 BSD 的完整證明" in text,
               "bf_not_constructed": "它們仍要求真正構造" in text,
               "not_identified_with_neron": "這不是對某一 isogenous curve 的 Neron period 數值作未聲明的換算" in text,
               "alignment_still_needed": "Kato/Coleman/adjoint 規範必須與這兩條模符號 period 對齊" in text,
               "review_concur_challenge": "CONCUR" in review and "CHALLENGE" in review,
               "not_circular": "本輪沒有以式 (1) 反向定義這兩個輸入" in text}
    js = {"bf_false": th["actual_BF_family_computed"] is False, "C_false": th["C_computed"] is False,
          "s11_false": th["s11_computed"] is False, "bsd_false": th["BSD_proved"] is False}
    return {"text": phrases, "json": js, "agrees": all(phrases.values()) and all(js.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    lines = calibrator_lines()
    print(f"  level 19 over Q: dim {lines['dimension']}, cusp {lines.get('cusp_dimension')}, Eisenstein {lines.get('eisenstein_dimension')}, "
          f"traces {lines['traces']}; plus identical {lines.get('plus_identical_to_theirs')}, minus identical {lines.get('minus_identical_to_theirs')}; "
          f"Hecke {lines.get('hecke_checks')}")
    ms = measures(lines)
    print(f"  measures: alpha {ms['alpha']}, twist {ms['alpha_twist']}, [0]+ = {ms['plus_at_zero']}, ordinary {ms['ordinary_first_layer_measures']} sum {ms['ordinary_central_value']} "
          f"(Euler {ms['central_by_euler_factor']}); twisted sums {ms['twisted_cusp_sums']} weighted {ms['twisted_weighted_sum']} -> {ms['twisted_x_inverse_value']}; "
          f"wrong-x {ms['wrong_x_moment']}; residuals zero {all(r == [0, 0] for r in ms['distribution_residuals'])}; smoothing {ms['smoothing_mod11']}, adjoint {ms['adjoint_euler_multiplier']}, product {ms['nonvanishing_product']}")
    l17 = level_17_remark()
    print(f"  17.a1: a_11 = {l17['a_11_of_17a1']}")
    aa = archimedean_alignment(lines)
    print(f"  archimedean: Omega+ = {aa['omega_plus']:.12f} (disc {aa['discriminant']}); plus unit {aa['plus_unit']} over {aa['nonzero_plus']} nonzero pairs, consistent {aa['plus_consistent']}; "
          f"minus reference D = {aa['minus_reference_D']}, {aa['nonzero_minus']} nonzero pairs, consistent {aa['minus_consistent']}")
    for r in aa["rows"]:
        extra = f"A = {r.get('A_rational')}" if r["D"] > 0 else f"ratio = {r.get('ratio_to_reference')}"
        print(f"    D={r['D']:4d} S={r['S']:2d} L={r['L']:.10f} {extra}")
    lab = labels()
    ok = lines["agrees"] and ms["agrees"] and l17["agrees"] and aa["agrees"] and lab["agrees"]
    out = {"gate": "src82", "round": "RUN-080", "lines": lines, "measures": ms, "level_17": l17, "archimedean": aa,
           "labels": lab, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
