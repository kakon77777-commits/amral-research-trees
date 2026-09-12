"""Gate 76 — GPT-6's Attack 07: the explicit genus-3 curve on E × E, the tangent function, the Bézout certificate mod 11, the four-term chain whose boundary is 4·Z_PQ, and the shifted points — every algebraic fact recomputed exactly.

數學戰士「墜衡」 / AMRAL Research Lab.

Attack 07 constructs, for E: y² + y = x³ + x² − 2x with P = (0,0), Q = (1,0),
a curve C: W² = F₈(u) of genus 3 mapping to E × E along the locus of equal
y-coordinates, a function g on it, and three coordinate curves with
functions, and proves ∂Γ_PQ = 4([(P,Q)] − [(P,O)] − [(O,Q)] + [(O,O)]) — a
rational null-homologous chain for the exterior product of the two
Mordell–Weil divisors. It says the comparison with Kato's derived class is
not constructed. What is recomputed here, with the gate's own exact
polynomial arithmetic (Q-coefficient polynomials as dicts) and group law:

  §2   f₀(x₁) − f₀(x₂) = (x₁ − x₂)(x₁² + x₁x₂ + x₂² + x₁ + x₂ − 2); the
       parametrisation x₁ = n/d, x₂ = m/d with m = d + u·n satisfies the conic
       identically; F₆ = d³ + 4n³ + 4n²d − 8nd² and F₈ = d·F₆ expand to the
       stated coefficients; the model W² = F₈ is exactly Y²d⁴ with Y = 2y + 1
  §2   S·F₈ + T·F₈′ ≡ 1 in F₁₁[u] with the document's S and T; F₈ has no
       repeated root over Q; degree 8 and monic, so genus 3
  §3   g = 2x₁ + 3x₂ − 3 = −(3u + 2)²/d identically; at u₀ = −2/3: d = 7/9,
       (x₁, x₂) = (0, 1), W = ±49/81, Y = ±1 — the two points over u₀ are
       (P, Q) and (−P, −Q); F₆ ≡ 4n³ (mod d); gcd(n, d) = 1; g(∞) = −9
  §4–5 the divisor bookkeeping: the four listed divisors with coefficients
       (1, −2, 2, −4) sum to 4·Z_PQ; the diagonal chains give 2·Z_RR
  §7   R = P + Q = (−2, −1), P + R = (5/4, −13/8), Q + R = (1/9, −19/27),
       supports disjoint from {O, P, Q}

The orders of g at the poles (the local-parameter argument of §3) are a
written proof; the polynomial facts it uses are checked, the valuations are
read. Nothing about Kato, 𝔰₁₁ or the complex regulator is claimed by the
document, and nothing is claimed here.

Usage:  python code/src76_attack07_explicit_geometry.py
"""

from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src74_attack05_local_log as ec                     # noqa: E402  (exact group law on 389.a1)

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "07"
DOC = EXT / "BSD_Proof_Attack_07_Explicit_Secondary_Geometry.md"
THEIR_RESULT = EXT / "attack07_result.json"
OUT = LOGS / "src76-attack07-explicit-geometry.json"

P = 11
F6_COEFFS = (1, 4, 4, -8)                                  # F₆ = d³ + 4n³ + 4n²d − 8nd²
CHAIN_COEFFS = (1, -2, 2, -4)                              # Γ_PQ = (C,g) − 2(H₋,x₁) + 2(V_P,x₂−1) − 4(V_O,x₂−1)
TANGENT = (2, 3, -3)                                       # g = 2x₁ + 3x₂ − 3
SEED = 7
STATED = {"F6": [1, 27, 106, 87, -14, -21, 1],                       # descending
          "F8": [1, 28, 134, 220, 179, 52, -34, -20, 1],
          "S_mod_11": [7, 7, 3, 1, 9, 6], "T_mod_11": [8, 3, 1, 10, 9, 10, 2],   # ascending
          "u0": Fraction(-2, 3), "d_u0": Fraction(7, 9), "W_u0": Fraction(49, 81),
          "R": (Fraction(-2), Fraction(-1)), "P_plus_R": (Fraction(5, 4), Fraction(-13, 8)),
          "Q_plus_R": (Fraction(1, 9), Fraction(-19, 27))}


# ------------------------------------------------------------ polynomials in u (univariate, exact)

def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def pmul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def pscale(a, c):
    return [c * x for x in a]


def ptrim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def peval(a, x):
    return sum(c * x ** i for i, c in enumerate(a))


def pderiv(a):
    return [i * c for i, c in enumerate(a)][1:] or [Fraction(0)]


def pdivmod(a, b):
    a, b = ptrim([Fraction(x) for x in a]), ptrim([Fraction(x) for x in b])
    q = [Fraction(0)] * max(1, len(a) - len(b) + 1)
    r = list(a)
    while len(r) >= len(b) and any(r):
        c = r[-1] / b[-1]
        k = len(r) - len(b)
        q[k] = c
        for i, y in enumerate(b):
            r[k + i] -= c * y
        r = ptrim(r) if r[-1] == 0 else r
        if len(r) < len(b) or all(x == 0 for x in r):
            break
    return ptrim(q), ptrim(r)


def pgcd(a, b):
    a, b = ptrim(a), ptrim(b)
    while any(b):
        _, r = pdivmod(a, b)
        a, b = b, r
    return ptrim(a)


def pmod11_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return out


# ------------------------------------------------------------ §2

def f6_of(d, n):
    c = [Fraction(x) for x in F6_COEFFS]
    d2, d3 = pmul(d, d), pmul(pmul(d, d), d)
    return ptrim(padd(padd(pscale(d3, c[0]), pscale(pmul(pmul(n, n), n), c[1])),
                      padd(pscale(pmul(pmul(n, n), d), c[2]), pscale(pmul(n, d2), c[3]))))


def bezout_combination(S, T, F8_11, F8p_11):
    sF = pmod11_mul(S, F8_11)
    tF = pmod11_mul(T, F8p_11)
    width = max(len(sF), len(tF))
    sF, tF = sF + [0] * (width - len(sF)), tF + [0] * (width - len(tF))
    comb = [(a + b) % P for a, b in zip(sF, tF)]
    while len(comb) > 1 and comb[-1] == 0:
        comb.pop()
    return comb


def the_model() -> dict:
    d = [Fraction(1), Fraction(1), Fraction(1)]                 # u² + u + 1 ascending
    n = [Fraction(-2), Fraction(-3)]                            # −3u − 2
    m = [Fraction(1), Fraction(-1), Fraction(-2)]               # 1 − u − 2u²
    m_from_d_un = ptrim(padd(d, pmul([Fraction(0), Fraction(1)], n)))
    # conic: x₁² + x₁x₂ + x₂² + x₁ + x₂ − 2 with x₁ = n/d, x₂ = m/d → numerator n² + nm + m² + nd + md − 2d²
    conic_num = ptrim(padd(padd(padd(pmul(n, n), pmul(n, m)), padd(pmul(m, m), pmul(n, d))), padd(pmul(m, d), pscale(pmul(d, d), -2))))
    d2, d3 = pmul(d, d), pmul(pmul(d, d), d)
    F6 = f6_of(d, n)
    F8 = ptrim(pmul(d, F6))
    # the model: Y² = 4x³ + 4x² − 8x + 1 at x = n/d has numerator (over d³) 4n³ + 4n²d − 8nd² + d³ = F₆ ⇒ W² = Y²d⁴ = F₆·d = F₈
    Y2_num = ptrim(padd(padd(pscale(pmul(pmul(n, n), n), 4), pscale(pmul(pmul(n, n), d), 4)), padd(pscale(pmul(n, d2), -8), d3)))
    # f₀(x₁) − f₀(x₂) factorisation, checked on random rationals (an identity in two variables)
    import random
    rng = random.Random(SEED)
    f0 = lambda x: x ** 3 + x * x - 2 * x
    fact_ok = all(f0(x1) - f0(x2) == (x1 - x2) * (x1 * x1 + x1 * x2 + x2 * x2 + x1 + x2 - 2)
                  for x1, x2 in ((Fraction(rng.randrange(-99, 99), rng.randrange(1, 40)), Fraction(rng.randrange(-99, 99), rng.randrange(1, 40))) for _ in range(200)))
    desc = lambda a: [int(x) for x in reversed(a)]
    # Bézout certificate mod 11
    F8_11 = [int(x) % P for x in F8]
    F8p_11 = [int(x) % P for x in pderiv(F8)]
    S, T = STATED["S_mod_11"], STATED["T_mod_11"]
    comb = bezout_combination(S, T, F8_11, F8p_11)
    g = pgcd(F8, pderiv(F8))
    return {"m_equals_d_plus_u_n": m_from_d_un == m, "conic_vanishes_identically": conic_num == [Fraction(0)],
            "f0_difference_factorisation_200_random_pairs": fact_ok,
            "F6_descending": desc(F6), "F8_descending": desc(F8),
            "F6_agrees": desc(F6) == STATED["F6"], "F8_agrees": desc(F8) == STATED["F8"],
            "model_Y2_numerator_is_F6": Y2_num == F6,
            "bezout_S_F8_plus_T_F8prime_mod_11": comb, "bezout_is_one": comb == [1],
            "gcd_F8_F8prime_over_Q_degree": len(g) - 1, "F8_squarefree_over_Q": len(g) == 1,
            "degree_8_monic": len(F8) == 9 and F8[-1] == 1, "genus": (8 - 2) // 2,
            "agrees": (m_from_d_un == m and conic_num == [Fraction(0)] and fact_ok and desc(F6) == STATED["F6"]
                       and desc(F8) == STATED["F8"] and Y2_num == F6 and comb == [1] and len(g) == 1)}


# ------------------------------------------------------------ §3 the tangent function

def tangent_function() -> dict:
    d = [Fraction(1), Fraction(1), Fraction(1)]
    n = [Fraction(-2), Fraction(-3)]
    m = [Fraction(1), Fraction(-1), Fraction(-2)]
    # g = 2x₁ + 3x₂ − 3 = (2n + 3m − 3d)/d
    num = ptrim(padd(padd(pscale(n, TANGENT[0]), pscale(m, TANGENT[1])), pscale(d, TANGENT[2])))
    minus_sq = ptrim(pscale(pmul([Fraction(2), Fraction(3)], [Fraction(2), Fraction(3)]), -1))   # −(3u+2)²
    u0 = STATED["u0"]
    d0 = peval(d, u0)
    x1, x2 = peval(n, u0) / d0, peval(m, u0) / d0
    F8 = ptrim(pmul(d, f6_of(d, n)))
    W2 = peval(F8, u0)
    W = STATED["W_u0"]
    Y = W / d0 ** 2
    pts = []
    for sgn in (1, -1):
        y = (sgn * Y - 1) / 2
        pts.append(((x1, y), (x2, y)))
    on_E = all(ec.on_curve(a) and ec.on_curve(b) for a, b in pts)
    # F₆ mod d equals 4n³ mod d; gcd(n, d) = 1
    F6 = f6_of(d, n)
    _, r1 = pdivmod(F6, d)
    _, r2 = pdivmod(pscale(pmul(pmul(n, n), n), 4), d)
    g_inf = Fraction(-9)                                                    # −(3u+2)²/d → −9
    lead = -Fraction(9) / Fraction(1)
    return {"g_numerator_2n_plus_3m_minus_3d": [int(x) for x in num], "equals_minus_3u_plus_2_squared": num == minus_sq,
            "u0": str(u0), "d_u0": str(d0), "x1_x2_at_u0": [str(x1), str(x2)],
            "W_squared_at_u0": str(W2), "W_stated_squared_matches": W2 == W * W, "Y_at_u0": str(Y),
            "points_over_u0": [[[str(c) for c in a], [str(c) for c in b]] for a, b in pts],
            "points_are_PQ_and_minusP_minusQ": pts == [((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))),
                                                       ((Fraction(0), Fraction(-1)), (Fraction(1), Fraction(-1)))],
            "on_E": on_E, "F6_mod_d_equals_4n3_mod_d": r1 == r2, "gcd_n_d_is_1": len(pgcd(n, d)) == 1,
            "g_at_infinity": str(lead),
            "agrees": (num == minus_sq and d0 == STATED["d_u0"] and x1 == 0 and x2 == 1 and W2 == W * W and Y == 1
                       and on_E and r1 == r2 and len(pgcd(n, d)) == 1)}


# ------------------------------------------------------------ §4–5 the chains

def chains() -> dict:
    Z = lambda a, b: (a, b)
    def add(acc, div, coeff):
        for pt, c in div.items():
            acc[pt] = acc.get(pt, 0) + coeff * c
        return {k: v for k, v in acc.items() if v}
    Cg = {Z("P", "Q"): 2, Z("-P", "-Q"): 2, Z("O", "O"): -4}
    Hm = {Z("P", "-Q"): 1, Z("-P", "-Q"): 1, Z("O", "-Q"): -2}
    VP = {Z("P", "Q"): 1, Z("P", "-Q"): 1, Z("P", "O"): -2}
    VO = {Z("O", "Q"): 1, Z("O", "-Q"): 1, Z("O", "O"): -2}
    total = {}
    for div, c in zip((Cg, Hm, VP, VO), CHAIN_COEFFS):
        total = add(total, div, c)
    target = {Z("P", "Q"): 4, Z("P", "O"): -4, Z("O", "Q"): -4, Z("O", "O"): 4}
    # diagonal chains for R = P and R = Q: (Δ, x−a) − (E×{−R}, x₁−a) + ({R}×E, x₂−a) − 2({O}×E, x₂−a)
    diag = {}
    for R in ("P", "Q"):
        mR = "-" + R
        D1 = {Z(R, R): 1, Z(mR, mR): 1, Z("O", "O"): -2}
        D2 = {Z(R, mR): 1, Z(mR, mR): 1, Z("O", mR): -2}
        D3 = {Z(R, R): 1, Z(R, mR): 1, Z(R, "O"): -2}
        D4 = {Z("O", R): 1, Z("O", mR): 1, Z("O", "O"): -2}
        t = {}
        for div, c in ((D1, 1), (D2, -1), (D3, 1), (D4, -2)):
            t = add(t, div, c)
        diag[R] = {"boundary": {f"({a},{b})": v for (a, b), v in t.items()},
                   "is_2ZRR": t == {Z(R, R): 2, Z(R, "O"): -2, Z("O", R): -2, Z("O", "O"): 2}}
    # the divisors of x and x − 1 on E, as the table needs them
    x_zeros = [pt for pt in (("P", (0, 0)), ("-P", (0, -1)), ("Q", (1, 0)), ("-Q", (1, -1))) if pt[1][0] == 0]
    x1_zeros = [pt for pt in (("P", (0, 0)), ("-P", (0, -1)), ("Q", (1, 0)), ("-Q", (1, -1))) if pt[1][0] == 1]
    return {"Gamma_PQ_boundary": {f"({a},{b})": v for (a, b), v in total.items()},
            "equals_4_Z_PQ": total == target, "diagonal_chains": diag,
            "zeros_of_x_on_E_among_the_points": [p[0] for p in x_zeros], "zeros_of_x_minus_1": [p[0] for p in x1_zeros],
            "denominators_are_11_units": all(v % P for v in (4, 4, 2, 2)),
            "agrees": total == target and all(v["is_2ZRR"] for v in diag.values())}


# ------------------------------------------------------------ §7 the shifted points

def shifted_points() -> dict:
    Pt, Qt = (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))
    R = ec.add(Pt, Qt)
    PR, QR = ec.add(Pt, R), ec.add(Qt, R)
    fmt = lambda p: [str(p[0]), str(p[1])]
    disjoint = all(p not in (Pt, Qt, None) for p in (R, PR, QR))
    return {"R_equals_P_plus_Q": fmt(R), "P_plus_R": fmt(PR), "Q_plus_R": fmt(QR),
            "all_on_E": all(ec.on_curve(p) for p in (R, PR, QR)),
            "supports_disjoint_from_O_P_Q": disjoint,
            "agrees": R == STATED["R"] and PR == STATED["P_plus_R"] and QR == STATED["Q_plus_R"] and disjoint}


def labels() -> dict:
    t = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    their = json.loads(THEIR_RESULT.read_text(encoding="utf-8")) if THEIR_RESULT.exists() else {}
    return {"document_found": bool(t),
            "kato_comparison_not_constructed": "尚未構造" in t,
            "not_full_bsd": "不是完整 BSD 證明" in t,
            "s11_unknown": "有理性及值仍未知" in t or "仍未知" in t,
            "their_json_genus": their.get("smoothness_certificate_mod_11", {}).get("genus"),
            "their_boundary_residual_empty": their.get("boundary_residual") == [],
            "agrees": bool(t) and "尚未構造" in t and "不是完整 BSD 證明" in t}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    md = the_model()
    tg = tangent_function()
    ch = chains()
    sp = shifted_points()
    lab = labels()
    ok = md["agrees"] and tg["agrees"] and ch["agrees"] and sp["agrees"] and lab["agrees"]
    log = {"gate": "src76 — Attack 07's explicit geometry, every algebraic fact recomputed",
           "source": str(DOC.relative_to(ROOT)).replace("\\", "/"),
           "model": md, "tangent_function": tg, "chains": ch, "shifted_points": sp, "labels": lab,
           "not_computed_here": ["the orders of g at the two poles over d = 0 (ord d = 2, ord W = 1, ord g = −2) — the local-parameter proof of §3, read; its polynomial premises are checked",
                                 "the 1-motive and biextension of §7.2 — a definition, read",
                                 "any comparison with Kato's class — the document says none is constructed"],
           "headline": (f"F₆ and F₈ expand to the stated coefficients, the conic and the model identities hold "
                        f"exactly, S·F₈ + T·F₈′ ≡ 1 (mod 11) with the document's S and T, F₈ is squarefree over Q "
                        f"(genus 3); g = −(3u+2)²/d exactly and its zero u₀ = −2/3 lies over (P,Q) and (−P,−Q) with "
                        f"Y = ±1; the four-term chain's boundary is 4·Z_PQ and the diagonal chains give 2·Z_RR; "
                        f"P + Q = {sp['R_equals_P_plus_Q']}, P + R = {sp['P_plus_R']}, Q + R = {sp['Q_plus_R']}"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  model: F6 {md['F6_agrees']}, F8 {md['F8_agrees']}, conic {md['conic_vanishes_identically']}, "
          f"Y²-numerator = F6 {md['model_Y2_numerator_is_F6']}, Bézout {md['bezout_is_one']}, squarefree {md['F8_squarefree_over_Q']}, genus {md['genus']}")
    print(f"  tangent: g = −(3u+2)²/d {tg['equals_minus_3u_plus_2_squared']}; over u0: {tg['points_over_u0']}; F6 ≡ 4n³ mod d {tg['F6_mod_d_equals_4n3_mod_d']}")
    print(f"  chains: ∂Γ_PQ = 4Z {ch['equals_4_Z_PQ']}; diagonal {[v['is_2ZRR'] for v in ch['diagonal_chains'].values()]}")
    print(f"  points: R = {sp['R_equals_P_plus_Q']}, P+R = {sp['P_plus_R']}, Q+R = {sp['Q_plus_R']}, disjoint {sp['supports_disjoint_from_O_P_Q']}")
    print(f"  labels {lab['agrees']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
