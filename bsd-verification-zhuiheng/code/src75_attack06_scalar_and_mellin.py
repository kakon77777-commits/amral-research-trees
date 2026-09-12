"""Gate 75 — GPT-6's Attack 06: the local multiplier 16 recomputed in Q(α), the adjugate identities checked, the Sen matrix, and — the substantive part — its complex-side Mellin formula for L''(E,1)/2 evaluated numerically with this tree's own a_n and compared with the corpus's value.

數學戰士「墜衡」 / AMRAL Research Lab.

Attack 06 fixes normalisations and proves (under listed inputs) that the
derived Kato class is κ† = 16·𝔰₁₁·adj(H)ℓ with 𝔰₁₁ ∈ Z₁₁^× unknown, shows a
direct motivic lift of the cyclotomic first jet fails at the Hodge–Tate
condition (Sen operator nilpotent), and writes the complex target as

    L''(E,1)/2 = (2π/√389) ∫₁^∞ f_E(iy/√389) (log y)² dy,

leaving the bridge BD6 unproved. What is computed here:

  §2   in Q(α), α² + 4α + 11 = 0: e₁₁ = (1 − α⁻¹)², c_α = (1 − α⁻¹)/(1 − β⁻¹)
       with β = 11/α, θ = c_α/11, and e₁₁/θ = 11 − a₁₁ + 1 = 16 exactly; the
       11-adic residues of α, e₁₁, θ to 11⁸ by Hensel lifting (e₁₁ ≡ 5, θ ≡ 1)
  §3   adj(H + c·llᵀ)l = adj(H)l and det(H + c·llᵀ) = det H + c·lᵀadj(H)l —
       tested on 500 random integer instances (Schwartz–Zippel)
  §4   Θ_J = [[0,1],[0,0]]: nonzero, square zero — not semisimple
  §6   det(AᵀHA) = (det A)² det H on random instances (the invariance claim's algebra)
  §7   the Mellin formula: with a_n from point counts (a₃₈₉ = +1 counted on the
       node), L(E,1) ≈ 0 by the same series, and L''(E,1)/2 evaluated to
       compare with 0.759316500288426770 — the value the corpus stated at
       RUN-023 and this tree had never computed

Usage:  python code/src75_attack06_scalar_and_mellin.py
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

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "06"
DOC = EXT / "BSD_Proof_Attack_06_Balanced_Determinant_Descent.md"
THEIR_RESULT = EXT / "attack06_result.json"
OUT = LOGS / "src75-attack06-scalar-and-mellin.json"

P = 11
N = 389
AINVS = [0, 1, 1, -2, 0]
REL = (-4, -11)                                           # A² = REL[0]·A + REL[1]: the minimal polynomial A² + 4A + 11
CUT = 60.0                                                # the Mellin integrals are cut at y = 1 + CUT/c
SIMPSON_EPS = 1e-15
DOC_L2 = 0.759316500288426770                             # the corpus's L''(E,1)/2!, as RUN-023 took it
STATED = {"local_multiplier": 16, "e11_mod_11": 5, "theta_mod_11": 1,
          "e11": ("214/121", "26/121"), "c_alpha": ("107/88", "13/88"), "theta": ("107/968", "13/968")}


# ------------------------------------------------------------ §2 Q(α)

class QA:
    """u + v·A in Q[A]/(A² + 4A + 11)."""
    def __init__(self, u, v=0):
        self.u, self.v = Fraction(u), Fraction(v)

    def __add__(self, o): return QA(self.u + o.u, self.v + o.v)
    def __sub__(self, o): return QA(self.u - o.u, self.v - o.v)

    def __mul__(self, o):
        # (u + vA)(u' + v'A) = uu' + (uv' + vu')A + vv'A², A² = −4A − 11
        vv = self.v * o.v
        return QA(self.u * o.u + REL[1] * vv, self.u * o.v + self.v * o.u + REL[0] * vv)

    def inv(self):
        # conjugate: A ↦ −4 − A; norm = (u + vA)(u + v(−4 − A)) = u² − 4uv − 11v²... computed via the product
        conj = QA(self.u + REL[0] * self.v, -self.v)
        n = (self * conj)
        assert n.v == 0 and n.u != 0
        return QA(conj.u / n.u, conj.v / n.u)

    def __truediv__(self, o): return self * o.inv()
    def pair(self): return (str(self.u), str(self.v))


def beta_of(alpha: "QA") -> "QA":
    """β = 11/α, the other root."""
    return QA(11) / alpha


def a_prime_power(p: int, k: int, ap: int, prev: int, prev2: int) -> int:
    """a_{p^k} = a_p·a_{p^{k−1}} − p·a_{p^{k−2}} at a good prime; a_p^k at the bad prime."""
    if p == N:
        return ap ** k
    return ap * prev - p * prev2


def local_multiplier() -> dict:
    a11 = kur.a_q(11)
    alpha = QA(0, 1)
    beta = beta_of(alpha)
    one = QA(1)
    e11 = (one - alpha.inv()) * (one - alpha.inv())
    c_alpha = (one - alpha.inv()) / (one - beta.inv())
    theta = c_alpha / QA(11)
    ratio = e11 / theta
    # Hensel: α mod 11^8 with α ≡ 7 (mod 11), f(x) = x² + 4x + 11
    mod = P ** 8
    a = 7
    for _ in range(8):
        f = (a * a + 4 * a + 11) % mod
        fp = (2 * a + 4) % mod
        a = (a - f * pow(fp, -1, mod)) % mod
    assert (a * a + 4 * a + 11) % mod == 0
    ainv = pow(a, -1, mod)
    e11_res = (1 - ainv) ** 2 % mod
    b = 11 * ainv % mod                                   # β = 11/α, not a unit — c_α needs care: (1 − β⁻¹) = (β − 1)/β
    # c_α = (1 − α⁻¹)·β/(β − 1); θ = c_α/11 = (1 − α⁻¹)·α⁻¹/(β − 1) since β/11 = α⁻¹
    theta_res = (1 - ainv) * ainv % mod * pow((b - 1) % mod, -1, mod) % mod
    return {"a_11": a11, "alpha_plus_beta": (alpha + beta).pair(), "alpha_times_beta": (alpha * beta).pair(),
            "e11": e11.pair(), "c_alpha": c_alpha.pair(), "theta": theta.pair(), "e11_over_theta": ratio.pair(),
            "eleven_minus_a11_plus_1": 11 - a11 + 1,
            "hensel_alpha_mod_11_8": a, "e11_mod_11_8": e11_res, "theta_mod_11_8": theta_res,
            "e11_mod_11": e11_res % P, "theta_mod_11": theta_res % P,
            "agrees": (ratio.pair() == ("16", "0") and 11 - a11 + 1 == 16 and e11.pair() == STATED["e11"]
                       and c_alpha.pair() == STATED["c_alpha"] and theta.pair() == STATED["theta"]
                       and e11_res % P == 5 and theta_res % P == 1)}


# ------------------------------------------------------------ §3, §6 identities

def adj2(m):
    (a, b), (c, d) = m
    return [[d, -b], [-c, a]]


def det2(m):
    (a, b), (c, d) = m
    return a * d - b * c


def identities(trials: int = 500) -> dict:
    rng = random.Random(6)
    R = lambda: rng.randrange(-10 ** 6, 10 ** 6)
    bad_adj = bad_det = bad_basis = 0
    for _ in range(trials):
        a, b, d, c, x, y = (R() for _ in range(6))
        H = [[a, b], [b, d]]
        l = [x, y]
        Hc = [[a + c * x * x, b + c * x * y], [b + c * x * y, d + c * y * y]]
        lhs = [sum(adj2(Hc)[i][j] * l[j] for j in range(2)) for i in range(2)]
        rhs = [sum(adj2(H)[i][j] * l[j] for j in range(2)) for i in range(2)]
        if lhs != rhs:
            bad_adj += 1
        quad = sum(l[i] * rhs[i] for i in range(2))       # lᵀ adj(H) l
        if det2(Hc) != det2(H) + c * quad:
            bad_det += 1
        A = [[R(), R()], [R(), R()]]
        At = [[A[0][0], A[1][0]], [A[0][1], A[1][1]]]
        AtH = [[sum(At[i][k] * H[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        AtHA = [[sum(AtH[i][k] * A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        if det2(AtHA) != det2(A) ** 2 * det2(H):
            bad_basis += 1
    sen = [[0, 1], [0, 0]]
    sen2 = [[sum(sen[i][k] * sen[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return {"trials": trials, "adjugate_rank_one_update_failures": bad_adj,
            "determinant_rank_one_update_failures": bad_det, "basis_change_det_failures": bad_basis,
            "sen_matrix": sen, "sen_nonzero": any(any(r) for r in sen), "sen_squared_zero": not any(any(r) for r in sen2),
            "agrees": bad_adj == 0 and bad_det == 0 and bad_basis == 0 and not any(any(r) for r in sen2)}


# ------------------------------------------------------------ §7 the Mellin formula

def a_n_table(bound: int) -> list[int]:
    a = [0] * (bound + 1)
    a[1] = 1
    primes = [p for p in range(2, bound + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    ap = {p: p + 1 - kur.count_points_general(AINVS, p) for p in primes}
    if N not in ap:                                         # the bad prime, counted on the node: a_389 = 389 + 1 − #E(F_389)
        ap[N] = N + 1 - kur.count_points_general(AINVS, N)
    for p in primes:
        # prime powers
        pk, k = p, 1
        powers = {}
        while pk <= bound:
            if k == 1:
                powers[pk] = ap[p]
            else:
                powers[pk] = a_prime_power(p, k, ap[p], powers[pk // p], powers[pk // (p * p)] if k >= 3 else 1)
            pk *= p
            k += 1
        for q, val in powers.items():
            a[q] = val
    # multiplicativity
    for n in range(2, bound + 1):
        if a[n] == 0 and n not in (0,):
            # factor n
            m, f = n, {}
            for p in primes:
                if p * p > m:
                    break
                while m % p == 0:
                    f[p] = f.get(p, 0) + 1
                    m //= p
            if m > 1:
                f[m] = f.get(m, 0) + 1
            if len(f) > 1:
                val = 1
                for p, e in f.items():
                    val *= a[p ** e]
                a[n] = val
    return a, ap


def simpson_adaptive(f, lo, hi, eps=None, depth=0, whole=None):
    if eps is None:
        eps = SIMPSON_EPS
    mid = (lo + hi) / 2
    if whole is None:
        whole = (hi - lo) / 6 * (f(lo) + 4 * f(mid) + f(hi))
    left = (mid - lo) / 6 * (f(lo) + 4 * f((lo + mid) / 2) + f(mid))
    right = (hi - mid) / 6 * (f(mid) + 4 * f((mid + hi) / 2) + f(hi))
    if depth > 40 or abs(left + right - whole) <= 15 * eps:
        return left + right + (left + right - whole) / 15
    return (simpson_adaptive(f, lo, mid, eps / 2, depth + 1, left)
            + simpson_adaptive(f, mid, hi, eps / 2, depth + 1, right))


def integral_log2(c: float) -> float:
    """∫₁^∞ e^{−cy} (log y)² dy, split at a few points for the adaptive rule."""
    f = lambda y: math.exp(-c * y) * math.log(y) ** 2
    cut = 1.0 + CUT / c
    total = 0.0
    a = 1.0
    for b in (1.5, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0):
        if b >= cut:
            break
        total += simpson_adaptive(f, a, b)
        a = b
    total += simpson_adaptive(f, a, cut)
    return total


def mellin() -> dict:
    bound = 220
    a, ap = a_n_table(bound)
    k = 2 * math.pi / math.sqrt(N)
    # L(E,1) = (2π/√N)·Λ(1), Λ(1) = 2 Σ a_n e^{−kn}/(kn)
    L1 = k * 2 * sum(a[n] * math.exp(-k * n) / (k * n) for n in range(1, bound + 1))
    terms = []
    total = 0.0
    for n in range(1, bound + 1):
        if a[n] == 0:
            continue
        val = a[n] * integral_log2(k * n)
        terms.append(val)
        total += val
    L2_half = k * total
    tail = abs(terms[-1]) if terms else 0.0
    return {"bound": bound, "a_p_first": {str(p): ap[p] for p in sorted(ap)[:12]}, "a_389": ap[N],
            "a_389_is_plus_1_split_multiplicative": ap[N] == 1,
            "constant_2pi_over_sqrtN": k, "L_at_1": L1, "L_at_1_is_zero_to": abs(L1),
            "L2_over_2_by_the_mellin_formula": L2_half, "corpus_value": DOC_L2,
            "difference": L2_half - DOC_L2, "relative_difference": abs(L2_half - DOC_L2) / DOC_L2,
            "last_term_magnitude": tail,
            "agrees": abs(L1) < 1e-9 and abs(L2_half - DOC_L2) / DOC_L2 < 1e-9}


def labels() -> dict:
    t = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    return {"document_found": bool(t),
            "s11_not_computed": "本輪沒有解出 $\\mathfrak s_{11}$" in t or "沒有解出" in t,
            "BD6_unproved": "BD6 未證" in t or "BD6（未證）" in t,
            "not_full_bsd": "並非完整 BSD 證明" in t,
            "agrees": bool(t) and "沒有解出" in t and "BD6" in t and "並非完整 BSD 證明" in t}


def compare_with_theirs(lm: dict) -> dict:
    if not THEIR_RESULT.exists():
        return {"present": False}
    t = json.loads(THEIR_RESULT.read_text(encoding="utf-8"))
    r = t.get("ordinary_residues", {})
    same = (t.get("local_multiplier") == 16 and r.get("alpha") == lm["hensel_alpha_mod_11_8"]
            and r.get("e11") == lm["e11_mod_11_8"] and r.get("theta") == lm["theta_mod_11_8"]
            and r.get("modulus") == P ** 8)
    return {"present": True, "their_alpha_mod_11_8": r.get("alpha"), "their_e11": r.get("e11"), "their_theta": r.get("theta"),
            "s11_left_null": t.get("canonical_global_scalar_s11", "missing") is None, "agrees": same}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    lm = local_multiplier()
    ids = identities()
    mel = mellin()
    cmp_ = compare_with_theirs(lm)
    lab = labels()
    ok = lm["agrees"] and ids["agrees"] and mel["agrees"] and cmp_.get("agrees", False) and lab["agrees"]
    log = {"gate": "src75 — Attack 06: the multiplier 16, the identities, the Mellin formula for L''(E,1)/2",
           "source": str(DOC.relative_to(ROOT)).replace("\\", "/"),
           "local_multiplier": lm, "identities": ids, "mellin": mel,
           "comparison_with_the_documents_output": cmp_, "labels": lab,
           "not_computed_here": ["Proposition 2.1 (h(x, κ†) = θ⁻¹a₂ℓ(x)) — Rubin's formula as cited in BKS I, read",
                                 "Proposition 4.1's Hodge–Tate inference — the Sen matrix is checked, the theorem is cited",
                                 "BD6 — the document says it is unproved; 𝔰₁₁ is left unknown, as the document leaves it"],
           "headline": (f"e₁₁/θ = 16 = 11 − a₁₁ + 1 exactly in Q(α), residues e₁₁ ≡ 5, θ ≡ 1 to 11⁸ as the document's; "
                        f"both rank-one-update identities and the basis-change law hold on 500 random instances; "
                        f"the Sen matrix is nilpotent and nonzero; and the Mellin formula, evaluated with this tree's "
                        f"a_n (a₃₈₉ = {mel['a_389']}), gives L(E,1) = {mel['L_at_1']:.2e} and L''(E,1)/2 = "
                        f"{mel['L2_over_2_by_the_mellin_formula']:.15f} against the corpus's {DOC_L2:.15f} "
                        f"(relative difference {mel['relative_difference']:.1e}) — the first computation of that "
                        f"value in this tree"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  Q(α): e11 = {lm['e11']}, c_α = {lm['c_alpha']}, θ = {lm['theta']}, e11/θ = {lm['e11_over_theta']}; "
          f"residues mod 11: e11 {lm['e11_mod_11']}, θ {lm['theta_mod_11']}; α mod 11^8 = {lm['hensel_alpha_mod_11_8']}")
    print(f"  identities: adj {ids['adjugate_rank_one_update_failures']}, det {ids['determinant_rank_one_update_failures']}, "
          f"basis {ids['basis_change_det_failures']} failures of {ids['trials']}; Sen² = 0 {ids['sen_squared_zero']}")
    print(f"  Mellin: a_389 = {mel['a_389']}, L(1) = {mel['L_at_1']:.3e}, L''(1)/2 = {mel['L2_over_2_by_the_mellin_formula']:.18f} "
          f"vs {DOC_L2:.18f}, rel diff {mel['relative_difference']:.2e}")
    print(f"  their residues identical {cmp_.get('agrees')}; labels {lab['agrees']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
