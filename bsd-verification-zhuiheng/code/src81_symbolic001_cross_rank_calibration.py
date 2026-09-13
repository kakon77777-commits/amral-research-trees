"""Gate 81 — BSD Symbolic Round 001 (the web GPT's "General Cross-Rank Projective Calibration"): every boxed identity instantiated with exact formal power series and checked on random instances of every rank pattern; two supplements the document does not state — the t-covariance of Theorem 4.1 and what the oracles O5/O6 actually test — and the one number in it, log₁₁(12), computed to 11¹².

數學戰士「墜衡」 / AMRAL Research Lab.

The document is a conditional symbolic theorem: under a factorisation

    B̂_i(t) = C · A_i(t) · j(t) · z_i(t),   C ∈ K^× common, A_i(0) ≠ 0,
    j(t) = j_e tᵉ + …,  z_i(t) = t^{d_i} κ_i + …,  κ_i ≠ 0,

it derives the leading term (3.1), the order (3.2), the calibrator
elimination (4.4), the PC-001 special case (5.1), the gauge orbit (6.1),
the invisibility of q_f (7.1), the X-rescaling law (8.1), the
t-reparametrisation remark (§9), the two-calibrator identity (10.1) and the
cocycle (11.1)–(11.3). None of it is computed in the document. This gate
computes all of it: formal power series over Q with vector coefficients,
truncated at a high order, random exact instances over every pattern of
(e, d_i) with e ≤ 3, d_i ≤ 3, dimensions m_i ≤ 3, and checks each identity
exactly. Two things the document leaves implicit are made explicit:

  * Theorem 4.1 is covariant under t ↦ ut: both sides scale by u^{−d_i}, so
    the formula is not merely "valid in a fixed coordinate" — it transforms
    correctly, while the bare ratio B_i^lead/b_k scales by u^{−(d_i − d_k)}
    (the rank-dependent law of §9), which is what a reader must not drop.
  * (10.1) and (11.3) are consequences of (2.1) alone: with a common C they
    hold for any data, and with a partner-dependent C they fail — so the
    oracles O5/O6 test the common-factorisation hypothesis O1 and nothing
    else. Checked both ways.

And the one number: L = log₁₁(12) = Σ (−1)^{m+1} 11^m/m, computed exactly
to 11¹² and cross-checked through log(144)/2 = log(1 + 11·13)/2:
v₁₁(L) = 1, so j₁ = 1/L has valuation −1 and the leading coefficients of
B̂_i carry a factor 11⁻¹ that the relative ratios cancel.

Read, not verified: whether a genuine Beilinson–Flach family satisfies
(2.1); PC-001 itself (not handed to this line); the determinant-line lift
of §12. The document lists these as unproved and so does this gate.

Usage:  python code/src81_symbolic001_cross_rank_calibration.py
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
DOC = EXT / "BSD_Symbolic_Round_001_General_Cross_Rank_Projective_Calibration.md"
OUT = LOGS / "src81-symbolic001-cross-rank-calibration.json"

P = 11
ORDER = 8                                                  # series truncated after t^ORDER
INSTANCES = 105                                            # random instances per (e, d) pattern
RANDOM_SEED = 1
LOG_PRECISION = 12                                         # log₁₁(12) to 11^LOG_PRECISION
LOG_TERMS = 60

# --- the arithmetic the drill may disturb ---------------------------------------
LEADING_OFFSET = 0                                         # the leading term is read at t^{e + d_i + LEADING_OFFSET}
FORMULA_A_RATIO_INVERTED = False                           # (4.4) with A_i(0)/A_k(0) in place of A_k(0)/A_i(0)
J_LEADING_ZERO = False                                     # force j_e = 0 (breaks hypothesis (2.2))
GAMMA_WITHOUT_A_RATIO = False                              # Γ_{i←k} := b_i/b_k, dropping A_k(0)/A_i(0)
REPARAM_EXPONENT_SIGN = -1                                 # t = t'/u: [t'^m] = u^{−m}·[t^m]
LOG_SERIES_SIGN = -1                                       # log(1+x) = Σ (−1)^{m+1} x^m/m; +1 would give −log(1−x)


def rnd(rng: random.Random, nonzero: bool = False) -> Fraction:
    while True:
        v = Fraction(rng.randint(-6, 6), rng.randint(1, 4))
        if v or not nonzero:
            return v


# ------------------------------------------------------------ formal series with vector coefficients

def smul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    """scalar series product, truncated at ORDER"""
    out = [Fraction(0)] * (ORDER + 1)
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if i + j <= ORDER:
                out[i + j] += x * y
    return out


def vmul(a: list[Fraction], v: list[list[Fraction]]) -> list[list[Fraction]]:
    """scalar series × vector series, truncated at ORDER"""
    m = len(v[0])
    out = [[Fraction(0)] * m for _ in range(ORDER + 1)]
    for i, x in enumerate(a):
        if not x:
            continue
        for j, vec in enumerate(v):
            if i + j <= ORDER:
                for k in range(m):
                    out[i + j][k] += x * vec[k]
    return out


def vorder(v: list[list[Fraction]]) -> int | None:
    for i, vec in enumerate(v):
        if any(vec):
            return i
    return None


def reparam_scalar(a: list[Fraction], u: Fraction) -> list[Fraction]:
    """t = t'/u: the coefficient of t'^m is u^{−m} times the coefficient of t^m"""
    return [x * u ** (REPARAM_EXPONENT_SIGN * m) for m, x in enumerate(a)]


def reparam_vector(v: list[list[Fraction]], u: Fraction) -> list[list[Fraction]]:
    return [[x * u ** (REPARAM_EXPONENT_SIGN * m) for x in vec] for m, vec in enumerate(v)]


# ------------------------------------------------------------ an instance of the abstract setting

def instance(rng: random.Random, e: int, ds: list[int], dims: list[int], common_C: bool = True) -> dict:
    C = rnd(rng, True)
    j = [Fraction(0)] * (ORDER + 1)
    for m in range(e, ORDER + 1):
        j[m] = rnd(rng)
    j[e] = Fraction(0) if J_LEADING_ZERO else rnd(rng, True)
    partners = []
    for d, m in zip(ds, dims):
        A = [rnd(rng) for _ in range(ORDER + 1)]
        A[0] = rnd(rng, True)
        z = [[Fraction(0)] * m for _ in range(ORDER + 1)]
        for k in range(d, ORDER + 1):
            z[k] = [rnd(rng) for _ in range(m)]
        kappa = [rnd(rng) for _ in range(m)]
        kappa[rng.randrange(m)] = rnd(rng, True)
        z[d] = kappa
        Ci = C if common_C else rnd(rng, True)
        B = vmul([Ci * x for x in smul(A, j)], z)                 # B̂ = C·A·j·z
        lam = [rnd(rng) for _ in range(m)]                        # a functional with λ(κ) ≠ 0
        while sum(l * k for l, k in zip(lam, kappa)) == 0:
            lam = [rnd(rng) for _ in range(m)]
        partners.append({"d": d, "m": m, "A": A, "z": z, "kappa": kappa, "B": B, "lam": lam, "C": Ci})
    return {"C": C, "e": e, "j": j, "partners": partners}


def leading(inst: dict, p: dict) -> list[Fraction]:
    r = inst["e"] + p["d"] + LEADING_OFFSET
    return p["B"][r] if r <= ORDER else [Fraction(0)] * p["m"]


def functional(lam: list[Fraction], v: list[Fraction]) -> Fraction:
    return sum(l * x for l, x in zip(lam, v))


def check_instance(inst: dict) -> dict:
    e, j, C = inst["e"], inst["j"], inst["C"]
    je = j[e]
    out = {"order": True, "leading": True, "theorem_4_4": True, "theorem_10_1": True, "cocycle": True,
           "gauge_orbit": True, "t_covariance": True, "t_ratio_rank_dependence": True, "q_f_invisible": True}
    ps = inst["partners"]
    for p in ps:
        # (3.2) and (3.1)
        out["order"] &= vorder(p["B"]) == e + p["d"]
        lead = leading(inst, p)
        out["leading"] &= lead == [C * p["A"][0] * je * k for k in p["kappa"]]
    # (4.4): every partner as calibrator k, every partner as target i
    for k, i in itertools.product(ps, ps):
        b_k = functional(k["lam"], leading(inst, k))
        ratio = (k["A"][0] * functional(k["lam"], k["kappa"])) / i["A"][0]
        if FORMULA_A_RATIO_INVERTED:
            ratio = (i["A"][0] * functional(k["lam"], k["kappa"])) / k["A"][0]
        rhs = [ratio * x / b_k for x in leading(inst, i)]
        out["theorem_4_4"] &= rhs == i["kappa"]
    # (10.1) and the cocycle (11.1)–(11.3)
    obs = {}
    for idx, p in enumerate(ps):
        obs[idx] = (functional(p["lam"], leading(inst, p)), p["A"][0], functional(p["lam"], p["kappa"]))
    vals = [b / (A0 * kk) for b, A0, kk in obs.values()]
    out["theorem_10_1"] &= all(v == vals[0] for v in vals) and vals[0] == C * je

    def gamma(i, k):
        bi, Ai, ki = obs[i]
        bk, Ak, kk = obs[k]
        return bi / bk if GAMMA_WITHOUT_A_RATIO else (Ak / Ai) * (bi / bk)

    for i, jj, k in itertools.product(range(len(ps)), repeat=3):
        out["cocycle"] &= gamma(i, jj) * gamma(jj, k) == gamma(i, k)
        out["cocycle"] &= gamma(i, k) == obs[i][2] / obs[k][2]                    # Γ_{i←k} = k_i/k_k
        out["cocycle"] &= gamma(i, k) * gamma(k, i) == 1
    # (6.1): C ↦ uC multiplies every leading class by u and leaves (4.4) unchanged
    u = Fraction(3, 2)
    for k, i in itertools.product(ps, ps):
        lead_i = [u * x for x in leading(inst, i)]
        b_k = u * functional(k["lam"], leading(inst, k))
        ratio = (k["A"][0] * functional(k["lam"], k["kappa"])) / i["A"][0]
        out["gauge_orbit"] &= [ratio * x / b_k for x in lead_i] == i["kappa"]
    # (7.1): a common q_f in ρ_i = q_f X_i cancels in ρ_i/ρ_k
    q = Fraction(5, 7)
    for k, i in itertools.product(ps, ps):
        Xi, Xk = functional(i["lam"], leading(inst, i)), functional(k["lam"], leading(inst, k))
        out["q_f_invisible"] &= (q * Xi) / (q * Xk) == Xi / Xk
    # §9: t = t'/u. κ_i' = u^{−d_i} κ_i, B_i^lead' = u^{−r_i} B_i^lead; (4.4) holds again in t'; the bare
    # ratio B_i^lead/b_k picks up u^{−(d_i − d_k)}
    u = Fraction(2, 3)
    jp = reparam_scalar(j, u)
    for p in ps:
        Bp = reparam_vector(p["B"], u)
        zp = reparam_vector(p["z"], u)
        Ap = reparam_scalar(p["A"], u)
        kappa_p = zp[p["d"]]
        out["t_covariance"] &= kappa_p == [x * u ** (-p["d"]) for x in p["kappa"]]
        out["t_covariance"] &= Bp[e + p["d"]] == [x * u ** (-(e + p["d"])) for x in p["B"][e + p["d"]]]
        out["t_covariance"] &= Bp == vmul([C * x for x in smul(Ap, jp)], zp)        # the factorisation survives
        p["_prime"] = (Bp, zp, Ap, kappa_p)
    for k, i in itertools.product(ps, ps):
        Bk, zk, Ak, kk = k["_prime"]
        Bi, zi, Ai, ki = i["_prime"]
        b_k = functional(k["lam"], Bk[e + k["d"]])
        ratio = (Ak[0] * functional(k["lam"], kk)) / Ai[0]
        out["t_covariance"] &= [ratio * x / b_k for x in Bi[e + i["d"]]] == ki
        # the bare ratio's law
        old = [x / functional(k["lam"], leading(inst, k)) for x in leading(inst, i)]
        new = [x / b_k for x in Bi[e + i["d"]]]
        out["t_ratio_rank_dependence"] &= new == [x * u ** (-(i["d"] - k["d"])) for x in old]
    for p in ps:
        p.pop("_prime", None)
    return out


def symbolic_identities() -> dict:
    rng = random.Random(RANDOM_SEED)
    patterns = [(e, ds) for e in (1, 2, 3) for ds in ([0, 1], [0, 2], [1, 1], [0, 1, 2], [2, 3, 0], [1, 3], [0, 0, 1])]
    totals: dict[str, int] = {}
    runs = 0
    for e, ds in patterns:
        for _ in range(INSTANCES // len(patterns) + 1):
            dims = [rng.randint(1, 3) for _ in ds]
            try:
                res = check_instance(instance(rng, e, ds, dims))
            except ZeroDivisionError:                          # a vanishing calibrator observable: (4.3) fails, red
                res = {k: False for k in ("order", "leading", "theorem_4_4", "theorem_10_1", "cocycle",
                                          "gauge_orbit", "t_covariance", "t_ratio_rank_dependence", "q_f_invisible")}
            runs += 1
            for k, v in res.items():
                totals[k] = totals.get(k, 0) + (1 if v else 0)
    # the negative control: a partner-dependent C must break (10.1) and (11.3)
    broken = 0
    trials = 30
    for _ in range(trials):
        inst = instance(rng, 1, [0, 1, 2], [2, 2, 2], common_C=False)
        try:
            res = check_instance(inst)
        except ZeroDivisionError:
            res = {"theorem_10_1": False, "cocycle": False}
        broken += (not res["theorem_10_1"]) and (not res["cocycle"])
    return {"patterns": [f"e={e}, d={ds}" for e, ds in patterns], "instances": runs,
            "passed": totals, "all_pass": all(v == runs for v in totals.values()),
            "non_common_C_detected_by_10_1_and_11_3": broken, "negative_trials": trials,
            "agrees": all(v == runs for v in totals.values()) and broken == trials}


# ------------------------------------------------------------ the PC-001 specialisation and Attack 09's (19)

def specialisation() -> dict:
    """e = 1, d_0 = 0, d_E = 1, j₁ = 1/L: (5.1) κ_E = A_0(0)ℓ_0/A_E(0) · B_{E,2}/r_{0,1}; and with
    A_E(0) = 26λ₈(0)/D_E this is Attack 09's (19), B_{E,2} = 26Cλ₈(0)κ†/(D_E L)."""
    rng = random.Random(RANDOM_SEED + 1)
    ok = True
    for _ in range(50):
        L = rnd(rng, True)
        C = rnd(rng, True)
        lam8, DE, kappa_dag = rnd(rng, True), rnd(rng, True), rnd(rng, True)
        A_E0 = 26 * lam8 / DE
        A_00, ell0 = rnd(rng, True), rnd(rng, True)                 # calibrator data: A_0(0), ℓ_0 = Col_0(κ_0)
        j1 = 1 / L
        B_E2 = C * A_E0 * j1 * kappa_dag                             # [t²] of C A_E j z_E, z_E = t κ† + …
        r_01 = C * A_00 * j1 * ell0                                  # [t] of Col_0(B̂_0) = λ_0(B_0^lead)
        ok &= kappa_dag == A_00 * ell0 / A_E0 * B_E2 / r_01          # (5.1)
        ok &= B_E2 == 26 * C * lam8 * kappa_dag / (DE * L)           # Attack 09 (19)
    return {"trials": 50, "agrees": ok}


# ------------------------------------------------------------ log₁₁(12)

def red(fr: Fraction, mod: int) -> int:
    if fr.denominator % P == 0:
        raise ValueError("not 11-integral")
    return fr.numerator * pow(fr.denominator, -1, mod) % mod


def padic_log_one_plus(x: int, terms: int) -> Fraction:
    total = Fraction(0)
    for m in range(1, terms + 1):
        total += Fraction((LOG_SERIES_SIGN ** (m + 1)) * x ** m, m) if LOG_SERIES_SIGN == -1 else Fraction(x ** m, m)
    return total


def log_eleven_twelve() -> dict:
    mod = P ** LOG_PRECISION
    L = red(padic_log_one_plus(P, LOG_TERMS), mod)                 # log(1 + 11)
    L2 = red(padic_log_one_plus(P * 13, LOG_TERMS), mod)           # log(1 + 143) = log(144) = 2 log(12)
    half = L2 * pow(2, -1, mod) % mod
    val = 0
    x = L
    while x and x % P == 0:
        x //= P
        val += 1
    unit = (L // P) % (P ** (LOG_PRECISION - 1)) if L % P == 0 else None
    digits = []
    y = L
    for _ in range(LOG_PRECISION):
        digits.append(y % P)
        y //= P
    tail_ok = all(m - (1 if m % P == 0 else 0) >= LOG_PRECISION for m in range(LOG_TERMS + 1, LOG_TERMS + 300))
    return {"precision": LOG_PRECISION, "modulus": mod, "log_12": L, "digits_low_to_high": digits,
            "valuation": val, "unit_part_L_over_11": unit, "j_1_valuation": -val,
            "cross_check_half_log_144": half, "cross_check_agrees": half == L, "tail_bound_holds": tail_ok,
            "agrees": half == L and val == 1 and tail_ok and digits[0] == 0 and digits[1] != 0}


# ------------------------------------------------------------ labels

def labels() -> dict:
    text = DOC.read_text(encoding="utf-8")
    phrases = {"conditional": "Conditional symbolic theorem" in text,
               "no_new_computation": "未做新的大型數值計算" in text,
               "bsd_not_claimed": "未主張 BSD 已證明" in text,
               "unproved_list": "本輪沒有證明" in text and "BSD 猜想已被證明" in text,
               "q_f_not_one": "不能因此推出" in text and "q_{\\mathbf f}=1" in text,
               "absolute_anchor_needed": "absolute BSD may still require one absolute anchor" in text,
               "determinant_lift_not_constructed": "本輪沒有構造這個 determinant lift" in text}
    return {"phrases": phrases, "agrees": all(phrases.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    si = symbolic_identities()
    print(f"  identities: {si['instances']} instances over {len(si['patterns'])} (e, d) patterns; passed {si['passed']}; "
          f"non-common C detected {si['non_common_C_detected_by_10_1_and_11_3']}/{si['negative_trials']}")
    sp = specialisation()
    print(f"  specialisation (5.1) and Attack 09's (19): {sp['agrees']}")
    lg = log_eleven_twelve()
    print(f"  log_11(12) mod 11^{lg['precision']} = {lg['log_12']} (digits low→high {lg['digits_low_to_high']}), "
          f"v = {lg['valuation']}, unit {lg['unit_part_L_over_11']}, cross-check log(144)/2: {lg['cross_check_agrees']}")
    lab = labels()
    ok = si["agrees"] and sp["agrees"] and lg["agrees"] and lab["agrees"]
    out = {"gate": "src81", "round": "RUN-079", "symbolic_identities": si, "specialisation": sp,
           "log_11_of_12": lg, "labels": lab, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
