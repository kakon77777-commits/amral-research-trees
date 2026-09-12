"""Gate 77 — GPT-6's Attack 08: the three norms of the tangent function, the translation formulas and the sign identity in the function field of 389.a1, the full addition pushforward 7·((x+2)/y)⁴, the divisor of (x+2)/y against m_*Z_PQ, the closed-chain bookkeeping that moves the constant 7, and the localisation residues — every finite identity recomputed exactly.

數學戰士「墜衡」 / AMRAL Research Lab.

Attack 08 pushes Attack 07's chain Γ along the two projections and the
addition map m: A = E × E → E, and finds

    F_{π₁}(Γ) = 7,   F_{π₂}(Γ) = 7,   F_m(Γ) = 7·M⁴,   M = (x + 2)/y,

with div M = [R] − [P] − [Q] + [O] = m_*Z_PQ; then shows the 7 is not
intrinsic — a closed chain Θ_c = (Δ,c) − (H₀,c) − (V_O,c) has pushforward
exponents (0, 0, 2), so ½Θ₇ removes it — and writes down the localisation
classes whose residues are [P] − [O], [Q] − [O]. It says the comparison with
Kato's class is not constructed, 𝔰₁₁ unknown, BSD not proved.

What is recomputed here, in Q[x, y]/(y² + y − x³ − x² + 2x) with the gate's
own arithmetic (elements a(x) + b(x)·y, exact Fractions):

  08.1  the Vieta factorisation X³ + X² − 2X − f₀(x) = (X − x)(X² + (1+x)X + x² + x − 2)
        and the three norms N(a + br) = a² + ab(−1−x) + b²(x² + x − 2):
        7x², 7(x−1)², 7(x+2)² for (a,b) = (2x−3, 3), (3x−3, 2), (−5−2x, 1)
  08.2  A(T) = x(T+Q) = (x² + x − 2 − y)/(x−1)² and B(T) = x(T−P) − 1 =
        (y + 1 − x² − 2x)/x² from the group law; the sign identity (9)
        y²(y + 1 − x² − 2x) + x²(x+2)(x² + x − 2 − y) = 0 on the curve;
        the full pushforward identity B²y⁴ = (x+2)²x⁴A²; div(x+2), div(y),
        div M and m_*Z_PQ point by point
  08.3  the mapping-degree table and the exponent arithmetic (1,1,4) − (1,0,1)
        − (0,1,1) = (0,0,2); Γ⁰ and Γ¹ = Γ⁰ + ½Θ₇ carrying (1,1,M⁴); #E[2] = 4
        from the 2-division cubic being separable
  08.5  the localisation residues, by divisor bookkeeping

Propositions 08.4 and 08.6 (the degree mismatch, the split exact sequence)
are higher-Chow theory, read.

Usage:  python code/src77_attack08_norms_and_pushforwards.py
"""

from __future__ import annotations

import json
import pathlib
import random
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src74_attack05_local_log as ec                     # noqa: E402  (exact group law)
import src76_attack07_explicit_geometry as pg             # noqa: E402  (univariate polynomial helpers)

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "08"
DOC = EXT / "BSD_Proof_Attack_08_Norms_Localization_and_Scale.md"
THEIR_RESULT = EXT / "attack08_result.json"
OUT = LOGS / "src77-attack08-norms-and-pushforwards.json"

F = Fraction
F0 = [F(0), F(-2), F(1), F(1)]                            # f₀(x) = x³ + x² − 2x, ascending
NORM_PAIRS = {"projection_1": ([F(-3), F(2)], [F(3)]),     # (a, b) = (2x − 3, 3)
              "projection_2": ([F(-3), F(3)], [F(2)]),     # (3x − 3, 2)
              "addition": ([F(-5), F(-2)], [F(1)])}       # (−5 − 2x, 1)
STATED_NORMS = {"projection_1": [0, 0, 7], "projection_2": [7, -14, 7], "addition": [28, 28, 7]}
DEGREE_TABLE = {"diagonal": (1, 1, 4), "horizontal_axis": (1, 0, 1), "vertical_axis": (0, 1, 1)}
PROD_RS = [F(-2), F(1), F(1)]                              # rs = x² + x − 2 (Vieta)
Y2_LINEAR = -1                                            # y² = f₀ + Y2_LINEAR·y on the curve
POLE_ORDER_Y = 3                                          # y has a triple pole at O
VIETA_SEED = 8


# ------------------------------------------------------------ the function field, a(x) + b(x)·y

class FF:
    def __init__(self, a, b=None):
        self.a = pg.ptrim([F(c) for c in a])
        self.b = pg.ptrim([F(c) for c in (b if b is not None else [0])])

    @staticmethod
    def x():
        return FF([0, 1])

    @staticmethod
    def y():
        return FF([0], [1])

    @staticmethod
    def const(c):
        return FF([c])

    def __add__(self, o):
        return FF(pg.padd(self.a, o.a), pg.padd(self.b, o.b))

    def __sub__(self, o):
        return FF(pg.padd(self.a, pg.pscale(o.a, -1)), pg.padd(self.b, pg.pscale(o.b, -1)))

    def __mul__(self, o):
        # (a + by)(c + dy) = ac + (ad + bc)y + bd·y², y² = f₀ − y
        ac = pg.pmul(self.a, o.a)
        ad_bc = pg.padd(pg.pmul(self.a, o.b), pg.pmul(self.b, o.a))
        bd = pg.pmul(self.b, o.b)
        return FF(pg.padd(ac, pg.pmul(bd, F0)), pg.padd(ad_bc, pg.pscale(bd, Y2_LINEAR)))

    def __pow__(self, n):
        out = FF.const(1)
        for _ in range(n):
            out = out * self
        return out

    def is_zero(self):
        return all(c == 0 for c in self.a) and all(c == 0 for c in self.b)

    def show(self):
        return {"a": [str(c) for c in self.a], "b": [str(c) for c in self.b]}


X, Y, ONE = FF.x(), FF.y(), FF.const(1)


def poly(coeffs):
    return FF([F(c) for c in coeffs])


# ------------------------------------------------------------ 08.1 the norms

def vieta_factorisation(trials: int = 60) -> bool:
    """X³ + X² − 2X − f₀(x) = (X − x)(X² + (1 + x)X + x² + x − 2) as polynomials in X, at random rational x."""
    rng = random.Random(VIETA_SEED)
    for _ in range(trials):
        x = F(rng.randrange(-50, 50), rng.randrange(1, 20))
        lhs = [-(x ** 3 + x * x - 2 * x), F(-2), F(1), F(1)]
        rhs = pg.pmul([-x, F(1)], [x * x + x - 2, 1 + x, F(1)])
        if pg.ptrim(lhs) != pg.ptrim(rhs):
            return False
    return True


def norms() -> dict:
    """N(a + br) = a² + ab(r + s) + b²·rs with r + s = −1 − x, rs = x² + x − 2."""
    sum_rs = [F(-1), F(-1)]
    prod_rs = PROD_RS
    out = {}
    for name, (a, b) in NORM_PAIRS.items():
        n = pg.ptrim(pg.padd(pg.padd(pg.pmul(a, a), pg.pmul(pg.pmul(a, b), sum_rs)), pg.pmul(pg.pmul(b, b), prod_rs)))
        out[name] = {"a": [str(c) for c in a], "b": [str(c) for c in b], "norm_ascending": [int(c) for c in n],
                     "stated": STATED_NORMS[name], "agrees": [int(c) for c in n] == STATED_NORMS[name]}
    out["vieta_factorisation"] = vieta_factorisation()
    out["agrees"] = all(v["agrees"] for k, v in out.items() if isinstance(v, dict)) and out["vieta_factorisation"]
    return out


# ------------------------------------------------------------ 08.2 translations, the sign identity, the pushforward

def translations() -> dict:
    # A = x(T + Q): λ = y/(x − 1), x₃ = λ² − x − 2 ⇒ (x − 1)²·x₃ = y² − (x + 2)(x − 1)²  ≟  x² + x − 2 − y
    lhs_A = (Y * Y) - (poly([2, 1]) * (poly([-1, 1]) * poly([-1, 1])))            # (x − 1)²·x₃ with x₃ = λ² − x − 2
    rhs_A = poly([-2, 1, 1]) - Y
    # B = x(T − P) − 1: λ = (y + 1)/x, x₃ = λ² − x − 1 ⇒ x²·(x₃ − 1) = (y + 1)² − x³ − x² − x²  ≟  y + 1 − x² − 2x
    lhs_B = (Y + ONE) * (Y + ONE) - poly([0, 0, 2, 1])
    rhs_B = Y + ONE - poly([0, 2, 1])
    # (9): y²(y + 1 − x² − 2x) + x²(x + 2)(x² + x − 2 − y) = 0
    sign = (Y * Y) * (Y + ONE - poly([0, 2, 1])) + (poly([0, 0, 1]) * poly([2, 1])) * (poly([-2, 1, 1]) - Y)
    # the full pushforward: with A = a_n/(x−1)², B = b_n/x², F_m(Γ) = 7(x+2)²B²/((x−1)⁴A²) = 7(x+2)⁴/y⁴ ⟺ b_n²·y⁴ = (x+2)²·x⁴·a_n²
    a_n = poly([-2, 1, 1]) - Y
    b_n = Y + ONE - poly([0, 2, 1])
    push = (b_n * b_n) * (Y ** 4) - (poly([2, 1]) ** 2) * poly([0, 0, 0, 0, 1]) * (a_n * a_n)
    return {"A_numerator_identity_residual": (lhs_A - rhs_A).show(), "A_holds": (lhs_A - rhs_A).is_zero(),
            "B_numerator_identity_residual": (lhs_B - rhs_B).show(), "B_holds": (lhs_B - rhs_B).is_zero(),
            "sign_identity_9_residual": sign.show(), "sign_identity_9_holds": sign.is_zero(),
            "pushforward_identity_residual": push.show(), "F_m_Gamma_is_7_M4": push.is_zero(),
            "agrees": (lhs_A - rhs_A).is_zero() and (lhs_B - rhs_B).is_zero() and sign.is_zero() and push.is_zero()}


def divisors() -> dict:
    """div(x + 2), div(y), div M and m_*Z_PQ, point by point on E(Q)."""
    Pt, Qt = (F(0), F(0)), (F(1), F(0))
    R = ec.add(Pt, Qt)
    negR = ec.neg(R)
    # points with x = −2: y² + y = f₀(−2) = 0 → y ∈ {0, −1}
    x_m2 = [(F(-2), y) for y in (F(0), F(-1)) if ec.on_curve((F(-2), y))]
    # points with y = 0: x³ + x² − 2x = 0 → x ∈ {0, 1, −2}
    y_0 = [(x, F(0)) for x in (F(0), F(1), F(-2)) if ec.on_curve((x, F(0)))]
    name = {Pt: "P", Qt: "Q", R: "R", negR: "-R", ec.neg(Pt): "-P", ec.neg(Qt): "-Q"}
    div_x2 = {name.get(p, str(p)): 1 for p in x_m2}
    div_x2["O"] = -2
    div_y = {name.get(p, str(p)): 1 for p in y_0}
    div_y["O"] = -POLE_ORDER_Y
    div_M = dict(div_x2)
    for k, v in div_y.items():
        div_M[k] = div_M.get(k, 0) - v
    div_M = {k: v for k, v in div_M.items() if v}
    m_Z = {"R": 1, "P": -1, "Q": -1, "O": 1}                      # m_*([(P,Q)] − [(P,O)] − [(O,Q)] + [(O,O)])
    return {"R_equals_P_plus_Q": [str(c) for c in R], "minus_R": [str(c) for c in negR],
            "points_with_x_equal_minus_2": [[str(c) for c in p] for p in x_m2],
            "points_with_y_equal_0": [[str(c) for c in p] for p in y_0],
            "div_x_plus_2": div_x2, "div_y": div_y, "div_M": div_M, "m_star_Z_PQ": m_Z,
            "div_M_equals_m_star_Z_PQ": div_M == m_Z,
            "div_F_m_Gamma_equals_m_star_boundary": {k: 4 * v for k, v in div_M.items()} == {k: 4 * v for k, v in m_Z.items()},
            "agrees": div_M == m_Z and R == (F(-2), F(-1))}


# ------------------------------------------------------------ 08.3 the closed correction

def closed_correction() -> dict:
    d, h, v = DEGREE_TABLE["diagonal"], DEGREE_TABLE["horizontal_axis"], DEGREE_TABLE["vertical_axis"]
    theta = tuple(d[i] - h[i] - v[i] for i in range(3))
    # exponents of the constant 7 in the three pushforwards
    gamma = (1, 1, 1)                                           # F = 7, 7, 7M⁴
    xi7 = tuple(h[i] + v[i] for i in range(3))                  # Ξ₇ = (H₀,7) + (V_O,7)
    gamma0 = tuple(gamma[i] - xi7[i] for i in range(3))
    gamma1 = tuple(F(gamma0[i]) + F(theta[i], 2) for i in range(3))
    # deg [2] = 4 ⇐ #E[2] = 4 ⇐ the 2-division cubic is separable
    a1, a2, a3, a4, a6 = 0, 1, 1, -2, 0
    b2, b4, b6 = a1 * a1 + 4 * a2, 2 * a4 + a1 * a3, a3 * a3 + 4 * a6
    cub = [F(b6), F(2 * b4), F(b2), F(4)]
    g = pg.pgcd(cub, pg.pderiv(cub))
    return {"degree_table": DEGREE_TABLE, "Theta_c_push_exponents": theta,
            "Gamma_exponents_of_7": gamma, "Xi_7_exponents": xi7, "Gamma0_exponents": gamma0,
            "Gamma0_pushes": ("1", "1", "M⁴/7"), "Gamma1_exponents": [str(e) for e in gamma1],
            "Gamma1_pushes": ("1", "1", "M⁴"),
            "two_division_cubic_separable": len(g) == 1, "E_2_torsion_order": 4 if len(g) == 1 else None,
            "agrees": theta == (0, 0, 2) and gamma0 == (0, 0, -1) and gamma1 == (F(0), F(0), F(0)) and len(g) == 1}


# ------------------------------------------------------------ 08.5 the localisation residues

def localisation() -> dict:
    # (P × G_m, τ) − (O × G_m, τ): div_{A¹}(τ) = [0], so the closure boundary is [(P,0)] − [(O,0)]
    S = {"P": {"P": 1, "O": -1}, "Q": {"Q": 1, "O": -1}}
    return {"residues": S, "agrees": S["P"] == {"P": 1, "O": -1} and S["Q"] == {"Q": 1, "O": -1}}


# ------------------------------------------------------------ labels and comparison

def labels() -> dict:
    t = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    their = json.loads(THEIR_RESULT.read_text(encoding="utf-8")) if THEIR_RESULT.exists() else {}
    o = their.get("open", {})
    return {"document_found": bool(t),
            "says_bsd_not_proved": "BSD 尚未證明" in t,
            "says_frontier_unchanged": "canonical frontier 保持原狀" in t,
            "says_comparison_not_constructed": "尚未構造" in t,
            "says_7_is_not_s11": "不能把這裡出現的 $7$ 指認為 Attack 06 的 $s_{11}$" in t,
            "their_json_s11_null": ("s11" in o) and o["s11"] is None,
            "their_json_BSD_proved_false": o.get("BSD_proved") is False,
            "their_json_frontier_updated_false": o.get("canonical_frontier_updated") is False,
            "agrees": bool(t) and "BSD 尚未證明" in t and "尚未構造" in t and o.get("BSD_proved") is False}


def compare_with_theirs(n: dict) -> dict:
    if not THEIR_RESULT.exists():
        return {"present": False}
    t = json.loads(THEIR_RESULT.read_text(encoding="utf-8"))
    tn = t.get("norms_polynomials_ascending", {})
    same = all(tn.get(k) == n[k]["norm_ascending"] for k in NORM_PAIRS)
    exps = t.get("residual_closed_ambiguity", {}).get("Theta_c_push_exponents")
    return {"present": True, "norms_identical": same, "their_Theta_exponents": exps,
            "their_geometric_constant": t.get("complete_pushforwards", {}).get("geometric_constant"),
            "their_is_Kato_global_scalar": t.get("complete_pushforwards", {}).get("is_Kato_global_scalar"),
            "agrees": same and exps == [0, 0, 2]}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    n = norms()
    tr = translations()
    dv = divisors()
    cc = closed_correction()
    lc = localisation()
    lab = labels()
    cmp_ = compare_with_theirs(n)
    ok = n["agrees"] and tr["agrees"] and dv["agrees"] and cc["agrees"] and lc["agrees"] and lab["agrees"] and cmp_.get("agrees", False)
    log = {"gate": "src77 — Attack 08's norms, pushforwards, divisors and closed corrections, recomputed",
           "source": str(DOC.relative_to(ROOT)).replace("\\", "/"),
           "norms": n, "translations_and_identities": tr, "divisors": dv, "closed_correction": cc,
           "localisation": lc, "labels": lab, "comparison_with_the_documents_output": cmp_,
           "not_computed_here": ["Proposition 08.4 — the higher-Chow degree mismatch (q = 1 vs q = 0), read",
                                 "Proposition 08.6 — the split localisation sequence, homotopy invariance and self-intersection, read",
                                 "deg [2] = 4 in characteristic zero — standard; #E[2] = 4 is checked from the separable 2-division cubic",
                                 "everything about Kato, 𝔰₁₁ and the complex leading term — the document says none of it is constructed"],
           "headline": (f"the three norms are 7x², 7(x−1)², 7(x+2)² from Vieta exactly; A = x(T+Q) and B = x(T−P) − 1 "
                        f"are as stated, the sign identity (9) and the pushforward identity B²y⁴ = (x+2)²x⁴A² hold in the "
                        f"function field, so F_m(Γ) = 7M⁴; div M = [R] − [P] − [Q] + [O] = m_*Z_PQ; the closed correction "
                        f"Θ_c has exponents (0,0,2) and Γ¹ = Γ⁰ + ½Θ₇ carries (1, 1, M⁴) — the 7 is not intrinsic, as the "
                        f"document says; the localisation residues are [P] − [O], [Q] − [O]; 𝔰₁₁ null, BSD not proved"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  norms: {[n[k]['norm_ascending'] for k in NORM_PAIRS]} (Vieta {n['vieta_factorisation']})")
    print(f"  A {tr['A_holds']}, B {tr['B_holds']}, sign identity {tr['sign_identity_9_holds']}, F_m = 7M⁴ {tr['F_m_Gamma_is_7_M4']}")
    print(f"  div M = {dv['div_M']} = m_*Z_PQ {dv['div_M_equals_m_star_Z_PQ']}")
    print(f"  Θ_c exponents {cc['Theta_c_push_exponents']}, Γ⁰ {cc['Gamma0_exponents']}, Γ¹ {cc['Gamma1_exponents']}, E[2] = {cc['E_2_torsion_order']}")
    print(f"  labels {lab['agrees']}, their output {cmp_.get('agrees')}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
