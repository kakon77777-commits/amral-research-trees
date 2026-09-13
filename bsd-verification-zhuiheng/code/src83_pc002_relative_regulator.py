"""Gate 83 — PC-002 (the local GPT-6 line's relative regulator germ and Farey cup normalisation): the four ordinary/twisted 11-adic L-series of 389.a1 and 19.a1 recomputed to t¹²⁰ from the level-1331 layer with this line's own eigenlines and paths — 2420 summand rows, all four series, the quotient Q(t) = L_Eλ_E/(L_0λ_0), its 121 coefficients, μ = 0, λ = 2 — identical; the finite-layer lemma exercised by refinement; the Farey cup pairing rebuilt on the cocycle spaces (ranks 64 and 2, radicals the cusp gauge, J_E ≡ 1, J_0 ≡ 3) and the four-line-invariant Q_∪; the comparison theorem read.

數學戰士「墜衡」 / AMRAL Research Lab.

PC-002 (branch agent/bsd-period-calibration, commit 85cf079) defines, for
E = 389.a1 and E₀ = 19.a1 at p = 11 with the pinned eigenlines of PC-001
and this line, the ordinary series L_i(t) = L₁₁(E_i, σ_t) and the twisted
odd-branch series λ_i(t) = L₁₁(E_i ⊗ χ₈, x⁻¹σ_t), σ_t(12) = 1 + t, and
computes Q(t) = L_Eλ_E/(L_0λ_0) mod (11, t¹²¹) from the 11³ layer:

    Q = 7t² + 10t³ + 9t⁴ + 7t⁵ + 6t⁶ + 7t⁹ + t¹⁰ + …

with the finite-layer lemma (5) certifying 121 coefficients from 1210
residue balls per curve; then the Farey cup pairing
J_N(u, v) = (1/6)Σ_i (u_i v_{Ri} − v_i u_{Ri}) on closed edge cochains,
J_E ≡ 1, J_0 ≡ 3, and Q_∪ = (J_0/J_E)Q, invariant under the four eigenline
rescalings.

Recomputed here: the two 389 eigenlines from the Manin relations (RUN-068's
engine) and the two 19 eigenlines over Q (gate 82's engine), all four equal
to the frozen inputs; the cyclotomic exponents e_u = log⟨u⟩/log 12 mod 121
by discrete logarithm; for each of the 2420 units u mod 1331 the plus
symbols at u/1331 and u/121, the eight twisted minus symbols, the ordinary
and twisted measures and the x⁻¹-weighted term — every row identical to
the line's; the group-basis and t-basis coefficients of all four series
(121 each) identical; Q's 121 coefficients identical, Weierstrass degree 2,
leading coefficient 7; the level-121 layer agreeing to width 11 and the
121 → 1331 distribution relation on 220 cells (the 1331 → 14641 relation on
2420 cells when run as a script); the cup pairing on the 65- and
3-dimensional cocycle spaces with rank 64 and 2, the cusp gauge
−e₀ + e_N a cocycle spanning each radical, J_E = 1, J_0 = 3, Q_∪'s
coefficients identical, and the invariance under a random four-line
rescaling.

Read, not verified: Loeffler–Rivero C1.9–C1.11 and (4) — that Q is
(D_E/D_0)·(R_E/R_0)|_{X=0}; the identification of the Γ₀ cup with the
adjoint-period/Petersson convention (the line says it is not done, and
that 3/1 is not D_0/D_E); the torsion-free-cover proof of the cup formula
as a statement about H¹ of the compactified curve — what is checked is the
formula's algebra on these cochains.

Usage:  python code/src83_pc002_relative_regulator.py [--deep]
"""

from __future__ import annotations

import json
import math
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src70_kurihara_modular_symbols as kur              # noqa: E402  the 389 engine
import src79_attack09_eisenstein_leading_term as atk79    # noqa: E402  eigenline(sign) at 389
import src82_pc001_calibrator_19a1 as pc1                 # noqa: E402  the 19 engine

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-local-period-calibration"
DOC = EXT / "reports" / "PC-002-RELATIVE-REGULATOR.md"
INPUTS = EXT / "data" / "pc002-inputs.json"
REG = EXT / "data" / "pc002-relative-regulator.json"
CUP = EXT / "data" / "pc002-cup-normalization.json"
OUT = LOGS / "src83-pc002-relative-regulator.json"

P = 11
GAMMA = 12
WIDTH = 121                                                # coefficients certified by the 11³ layer
CHI8 = {1: 1, 3: -1, 5: -1, 7: 1}

# --- the arithmetic the drill may disturb ---------------------------------------
LAYER = 3                                                  # the production layer 11^LAYER
TWIST_SIGN = -1                                            # α_χ = χ₈(11)·α
CHARACTER_EXPONENT = -1                                    # λ integrates x⁻¹
TEICHMULLER_POWER = 120                                    # ⟨u⟩ = u^{−120} mod 1331 (ω(u) = u^{121})
CUP_DENOMINATOR = 6
R_MAP = "d,-c-d"                                           # R(c,d) = (d, −c−d); the drill may swap the orientation
MEASURE_SECOND_TERM_SIGN = -1
RESCALING_SEED = 3

STATED = {"Q_first_11": [0, 0, 7, 10, 9, 7, 6, 0, 0, 7, 1], "Q_cup_first_11": [0, 0, 10, 8, 5, 10, 7, 0, 0, 10, 3],
          "L_E_first_11": [0, 0, 2, 2, 2, 0, 5, 6, 10, 7, 0], "lambda_E_first_11": [5, 9, 10, 6, 6, 2, 0, 8, 8, 9, 10],
          "L_0_first_11": [9, 3, 10, 3, 1, 6, 9, 6, 2, 0, 6], "lambda_0_first_11": [4, 3, 10, 9, 4, 10, 2, 7, 3, 8, 3],
          "J_E": 1, "J_0": 3, "cup_ranks": (64, 2), "cocycle_dims": (65, 3), "leading": 7, "t_order": 2,
          "denominator_constant": 3}


def their(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ------------------------------------------------------------ F₁₁[t]/(t^WIDTH)

def smul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * WIDTH
    for i, x in enumerate(a):
        if x:
            for j in range(WIDTH - i):
                if b[j]:
                    out[i + j] = (out[i + j] + x * b[j]) % P
    return out


def sinv(a: list[int]) -> list[int]:
    if a[0] % P == 0:
        raise ZeroDivisionError("series not invertible")
    inv0 = pow(a[0], P - 2, P)
    out = [0] * WIDTH
    out[0] = inv0
    for n in range(1, WIDTH):
        s = sum(a[k] * out[n - k] for k in range(1, n + 1) if a[k]) % P
        out[n] = (-inv0 * s) % P
    return out


def one_plus_t_power(e: int) -> list[int]:
    return [math.comb(e, k) % P if k <= e else 0 for k in range(WIDTH)]


# ------------------------------------------------------------ the two curves' symbols

class Curve:
    def __init__(self, label: str, N: int, plus: list[int], minus: list[int], a11: int, symbol):
        self.label, self.N, self.plus, self.minus, self.a11, self.symbol = label, N, plus, minus, a11, symbol
        roots = [x for x in range(P) if (x * x - a11 * x + P) % P == 0]
        self.alpha = [x for x in roots if x][0]
        self.alpha_t = (TWIST_SIGN * self.alpha) % P

    def phi_plus(self, num: int, den: int) -> int:
        return self.symbol(self.plus, num % den, den)

    def phi_chi(self, num: int, den: int) -> int:
        return sum(CHI8[b] * self.symbol(self.minus, (num * 8 + b * den) % (den * 8), den * 8) for b in CHI8) % P

    def measures(self, layer: int) -> dict:
        """ordinary μ(u + 11^layer Z) and twisted μ_χ(u + 11^layer Z) for the units u mod 11^layer, with the
        symbol values that enter them."""
        mod, parent = P ** layer, P ** (layer - 1)
        ainv, atinv = pow(self.alpha, P - 2, P), pow(self.alpha_t, P - 2, P)
        rows = {}
        for u in range(1, mod):
            if u % P == 0:
                continue
            p_mod, p_par = self.phi_plus(u, mod), self.phi_plus(u, parent)
            c_mod = [self.symbol(self.minus, (u * 8 + b * mod) % (mod * 8), mod * 8) for b in sorted(CHI8)]
            c_par = [self.symbol(self.minus, (u * 8 + b * parent) % (parent * 8), parent * 8) for b in sorted(CHI8)]
            chi_mod = sum(CHI8[b] * c for b, c in zip(sorted(CHI8), c_mod)) % P
            chi_par = sum(CHI8[b] * c for b, c in zip(sorted(CHI8), c_par)) % P
            ordinary = (pow(ainv, layer, P) * p_mod + MEASURE_SECOND_TERM_SIGN * pow(ainv, layer + 1, P) * p_par) % P
            twisted = (pow(atinv, layer, P) * chi_mod + MEASURE_SECOND_TERM_SIGN * pow(atinv, layer + 1, P) * chi_par) % P
            weight = pow(u % P, P - 2, P) if CHARACTER_EXPONENT == -1 else pow(u % P, CHARACTER_EXPONENT % (P - 1), P)
            rows[u] = {"plus_mod": p_mod, "plus_par": p_par, "cusps_mod": c_mod, "cusps_par": c_par,
                       "ordinary": ordinary, "twisted": twisted, "weighted": weight * twisted % P}
        return rows


def gamma_exponent(u: int, layer: int) -> int:
    """e(u) = log⟨u⟩/log(12) mod 11^{layer−1}: the discrete logarithm of ⟨u⟩ = u·ω(u)⁻¹ base 12 in 1 + 11Z/11^layer."""
    mod = P ** layer
    target = pow(u, -TEICHMULLER_POWER, mod)              # u^{−(11^{layer−1}−1)}... for layer 3: u^{−120}
    x, k, order = 1, 0, P ** (layer - 1)
    while k < order:
        if x == target:
            return k
        x = x * GAMMA % mod
        k += 1
    return None                                            # ⟨u⟩ not a power of 12: the exponent is undefined, red not a crash


def series_from_layer(curve: Curve, layer: int) -> dict:
    rows = curve.measures(layer)
    width = P ** (layer - 1)
    groupL, groupl = [0] * width, [0] * width
    unresolved = 0
    for u, r in rows.items():
        e = gamma_exponent(u, layer)
        r["e"] = e
        if e is None:
            unresolved += 1
            continue
        groupL[e] = (groupL[e] + r["ordinary"]) % P
        groupl[e] = (groupl[e] + r["weighted"]) % P
    L = [0] * WIDTH
    lam = [0] * WIDTH
    for e in range(width):
        if groupL[e] or groupl[e]:
            pw = one_plus_t_power(e)
            for k in range(WIDTH):
                if pw[k]:
                    L[k] = (L[k] + groupL[e] * pw[k]) % P
                    lam[k] = (lam[k] + groupl[e] * pw[k]) % P
    return {"rows": rows, "group_L": groupL, "group_lambda": groupl, "L": L, "lambda": lam, "units": len(rows),
            "unresolved_exponents": unresolved}


def refinement(curve: Curve, coarse: dict, fine: dict, layer: int) -> dict:
    """Σ over the 11 refinements of each coarse ball equals the coarse measure, both measures."""
    mod = P ** layer
    bad = 0
    for u, r in coarse["rows"].items():
        so = sum(fine["rows"][u + j * mod]["ordinary"] for j in range(P)) % P
        st = sum(fine["rows"][u + j * mod]["twisted"] for j in range(P)) % P
        bad += (so != r["ordinary"]) + (st != r["twisted"])
    return {"cells": len(coarse["rows"]), "failed": bad, "agrees": bad == 0}


# ------------------------------------------------------------ the cup pairing

def R_index(M_index, c: int, d: int) -> int:
    if R_MAP == "d,-c-d":
        return M_index(d, -c - d)
    return M_index(-c - d, c)                              # the other orientation


def cup(N: int, u: list[int], v: list[int]) -> int:
    """J_N(u, v) = (1/6) Σ_i (u_i v_{Ri} − v_i u_{Ri}) mod 11 over the darts i ∈ P¹(F_N)."""
    M = pc1.Manin(N)
    total = 0
    for i in range(N + 1):
        c, d = M.rep(i)
        j = R_index(M.index, c, d)
        total += u[i] * v[j] - v[i] * u[j]
    return total * pow(CUP_DENOMINATOR, P - 2, P) % P


def is_cocycle(N: int, w: list[int]) -> bool:
    M = pc1.Manin(N)
    for rel in M.relation_rows():
        if sum(v * w[j] for j, v in rel.items()) % P:
            return False
    return True


def cup_structure(N: int, basis: list[list[int]]) -> dict:
    n = len(basis)
    mat = [[cup(N, basis[i], basis[j]) for j in range(n)] for i in range(n)]
    alternating = all(mat[i][i] == 0 and (mat[i][j] + mat[j][i]) % P == 0 for i in range(n) for j in range(n))
    # rank mod 11
    m = [row[:] for row in mat]
    rank, r = 0, 0
    for c in range(n):
        pr = next((i for i in range(r, n) if m[i][c]), None)
        if pr is None:
            continue
        m[r], m[pr] = m[pr], m[r]
        inv = pow(m[r][c], P - 2, P)
        m[r] = [x * inv % P for x in m[r]]
        for i in range(n):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(x - f * y) % P for x, y in zip(m[i], m[r])]
        r += 1
        rank += 1
    gauge = [0] * (N + 1)
    gauge[0], gauge[N] = (-1) % P, 1
    gauge_cocycle = is_cocycle(N, gauge)
    gauge_radical = all(cup(N, gauge, b) == 0 for b in basis)
    return {"dimension": n, "rank": rank, "radical_dimension": n - rank, "alternating": alternating,
            "gauge_is_cocycle": gauge_cocycle, "gauge_in_radical": gauge_radical}


# ------------------------------------------------------------ assembling the round

def curves() -> dict:
    e_plus, e_minus = atk79.eigenline(1), atk79.eigenline(-1)
    lines19 = pc1.calibrator_lines()
    inp = their(INPUTS)
    target = Curve("389.a1", 389, e_plus["lambda"], e_minus["lambda"], kur.a_q(11),
                   lambda lam, a, n: sum(lam[i] for i in kur.path_indices(a % n, n)) % P)
    M19 = pc1.Manin(19)
    calib = Curve("19.a1", 19, lines19["plus_mod11"], lines19["minus_mod11"], lines19["traces"][11],
                  lambda lam, a, n: M19.symbol(lam, a, n, P))
    inputs_ok = {"target_plus": e_plus["lambda"] == inp["target"]["plus"], "target_minus": e_minus["lambda"] == inp["target"]["minus"],
                 "calibrator_plus": lines19["plus_mod11"] == inp["calibrator"]["plus"],
                 "calibrator_minus": lines19["minus_mod11"] == inp["calibrator"]["minus"],
                 "normalisations": (inp["target"]["normalization"] == {"plus_index": 5, "minus_index": 3}
                                    and inp["calibrator"]["normalization"] == {"plus_index": 0, "minus_index": 4}
                                    and e_plus["first_nonzero_index"] == 5 and e_minus["first_nonzero_index"] == 3)}
    return {"target": target, "calibrator": calib, "inputs_ok": inputs_ok, "eigenlines_ok": e_plus["ok"] and e_minus["ok"] and lines19["agrees"]}


def compare_rows(mine: dict, theirs: list) -> dict:
    same, total = 0, 0
    for row in theirs:
        a, e, pm, pp, cm, cp, om, tm, wm = row
        r = mine["rows"].get(a)
        total += 1
        same += bool(r and r["e"] == e and r["plus_mod"] == pm and r["plus_par"] == pp and r["cusps_mod"] == cm
                     and r["cusps_par"] == cp and r["ordinary"] == om and r["twisted"] == tm and r["weighted"] == wm)
    return {"rows": total, "identical": same}


def relative_regulator(cv: dict | None = None) -> dict:
    if cv is None:
        cv = curves()
    reg = their(REG)
    out = {"inputs_ok": cv["inputs_ok"], "eigenlines_ok": cv["eigenlines_ok"], "curves": {}}
    series = {}
    for key, name in (("target", "target"), ("calibrator", "calibrator")):
        c = cv[key]
        s3 = series_from_layer(c, LAYER)
        s2 = series_from_layer(c, LAYER - 1)
        th = reg["production_layers"][name]
        th2 = reg["first_layers"][name]
        rows_cmp = compare_rows(s3, th["summands"])
        ref = refinement(c, s2, s3, LAYER - 1)
        series[key] = s3
        out["curves"][key] = {
            "units": s3["units"], "alpha": c.alpha, "alpha_twist": c.alpha_t,
            "group_L_identical": s3["group_L"] == th["L_group_coefficients"],
            "group_lambda_identical": s3["group_lambda"] == th["lambda_group_coefficients"],
            "L_identical": s3["L"] == th["L_coefficients"], "lambda_identical": s3["lambda"] == th["lambda_coefficients"],
            "L_first_11": s3["L"][:11], "lambda_first_11": s3["lambda"][:11],
            "layer2_agrees_to_width_11": s3["L"][:11] == s2["L"][:11] and s3["lambda"][:11] == s2["lambda"][:11],
            "layer2_identical_to_theirs": s2["L"][:11] == th2["L_coefficients"] and s2["lambda"][:11] == th2["lambda_coefficients"],
            "summand_rows": rows_cmp, "refinement_121_to_1331": ref, "unresolved_exponents": s3["unresolved_exponents"]}
    num = smul(series["target"]["L"], series["target"]["lambda"])
    den = smul(series["calibrator"]["L"], series["calibrator"]["lambda"])
    Q = smul(num, sinv(den))
    order = next((k for k, x in enumerate(Q) if x), None)
    out.update({"numerator_first_11": num[:11], "denominator_first_11": den[:11], "denominator_constant": den[0],
                "Q": Q, "Q_first_11": Q[:11], "Q_t_order": order, "Q_leading": Q[order] if order is not None else None,
                "Q_identical_to_theirs": Q == reg["quotient_coefficients"],
                "numerator_identical": num == reg["numerator_coefficients"], "denominator_identical": den == reg["denominator_coefficients"],
                "mu": 0 if any(Q) else None, "lambda_invariant": order})
    t, c = out["curves"]["target"], out["curves"]["calibrator"]
    out["agrees"] = (all(cv["inputs_ok"].values()) and cv["eigenlines_ok"]
                     and all(x["group_L_identical"] and x["group_lambda_identical"] and x["L_identical"] and x["lambda_identical"]
                             and x["layer2_agrees_to_width_11"] and x["layer2_identical_to_theirs"]
                             and x["summand_rows"]["identical"] == x["summand_rows"]["rows"] == 1210
                             and x["refinement_121_to_1331"]["agrees"] and x["unresolved_exponents"] == 0 for x in (t, c))
                     and t["L_first_11"] == STATED["L_E_first_11"] and t["lambda_first_11"] == STATED["lambda_E_first_11"]
                     and c["L_first_11"] == STATED["L_0_first_11"] and c["lambda_first_11"] == STATED["lambda_0_first_11"]
                     and Q[:11] == STATED["Q_first_11"] and out["Q_identical_to_theirs"] and order == STATED["t_order"]
                     and Q[order] == STATED["leading"] and den[0] == STATED["denominator_constant"])
    out["_series"] = series
    return out


def cup_normalisation(cv: dict | None = None, rr: dict | None = None) -> dict:
    if cv is None:
        cv = curves()
    if rr is None:
        rr = relative_regulator(cv)
    cp = their(CUP)
    t, c = cv["target"], cv["calibrator"]
    J_E, J_0 = cup(389, t.plus, t.minus), cup(19, c.plus, c.minus)
    basis389 = kur.nullspace(kur.relation_rows(), 390)
    M19 = pc1.Manin(19)
    basis19 = [[int(x * 1) % P if x.denominator == 1 else (x.numerator * pow(x.denominator, -1, P)) % P for x in v] for v in M19.dual_space()]
    s389, s19 = cup_structure(389, basis389), cup_structure(19, basis19)
    cocycles = {"plus_E": is_cocycle(389, t.plus), "minus_E": is_cocycle(389, t.minus),
                "plus_0": is_cocycle(19, c.plus), "minus_0": is_cocycle(19, c.minus)}
    ratio = J_0 * pow(J_E, P - 2, P) % P
    Q_cup = [x * ratio % P for x in rr["Q"]]
    # four-line rescaling: plus_E·a, minus_E·b, plus_0·c, minus_0·d
    rng = random.Random(RESCALING_SEED)
    a, b, cc, d = (rng.randint(2, P - 1) for _ in range(4))
    Q_scaled = [x * a * b * pow(cc * d, P - 2, P) % P for x in rr["Q"]]
    J_E_scaled = cup(389, [x * a % P for x in t.plus], [x * b % P for x in t.minus])
    J_0_scaled = cup(19, [x * cc % P for x in c.plus], [x * d % P for x in c.minus])
    invariant = (J_E_scaled == a * b * J_E % P and J_0_scaled == cc * d * J_0 % P
                 and [x * J_0_scaled * pow(J_E_scaled, P - 2, P) % P for x in Q_scaled] == Q_cup)
    return {"J_E": J_E, "J_0": J_0, "ratio": ratio, "cocycles": cocycles, "structure_389": s389, "structure_19": s19,
            "Q_cup_first_11": Q_cup[:11], "Q_cup_identical_to_theirs": Q_cup == cp["cup_normalized_quotient_coefficients"],
            "rescaling": {"a": a, "b": b, "c": cc, "d": d, "invariant": invariant},
            "agrees": (J_E == STATED["J_E"] and J_0 == STATED["J_0"] and all(cocycles.values())
                       and (s389["rank"], s19["rank"]) == STATED["cup_ranks"] and (s389["dimension"], s19["dimension"]) == STATED["cocycle_dims"]
                       and s389["radical_dimension"] == 1 and s19["radical_dimension"] == 1
                       and s389["gauge_is_cocycle"] and s389["gauge_in_radical"] and s19["gauge_is_cocycle"] and s19["gauge_in_radical"]
                       and s389["alternating"] and s19["alternating"]
                       and Q_cup[:11] == STATED["Q_cup_first_11"] and Q_cup == cp["cup_normalized_quotient_coefficients"] and invariant
                       and cp["cup_ratio_mod11"] == ratio and cp["target"]["eigensymbol_pairing_mod11"] == J_E
                       and cp["calibrator"]["eigensymbol_pairing_mod11"] == J_0)}


def labels() -> dict:
    text = DOC.read_text(encoding="utf-8")
    reg, cp = their(REG), their(CUP)
    phrases = {"not_measured_regulator": "不是由原始 BF 類座標測量出的 regulator" in text,
               "three_over_one_not_D_ratio": "不能直接把 \\(3/1\\) 當成 \\(D_0/D_E\\)" in text,
               "weierstrass_degree_only": "單憑 mod 11 展開，不能推出 characteristic-zero 的常數及一次項恰為零" in text,
               "invariance_scope": "不是任意更換 cochain 代表時所有解析函數都不變" in text,
               "still_need_bf": "再往後仍需真正的 BF leading class" in text}
    js = {"bf_regulator_false": reg["claims"]["actual_BF_regulator_measured"] is False,
          "C_false": reg["claims"]["C_computed"] is False, "s11_false": reg["claims"]["s11_computed"] is False,
          "bsd_false": reg["claims"]["BSD_proved"] is False, "cup_not_matched": cp["claims"]["matched_to_LR_adjoint_periods"] is False}
    return {"text": phrases, "json": js, "agrees": all(phrases.values()) and all(js.values())}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    deep = "--deep" in sys.argv
    cv = curves()
    print(f"  inputs: {cv['inputs_ok']}; eigenlines ok {cv['eigenlines_ok']}")
    rr = relative_regulator(cv)
    for key in ("target", "calibrator"):
        x = rr["curves"][key]
        print(f"  {key}: {x['units']} units, alpha {x['alpha']}, twist {x['alpha_twist']}; rows identical {x['summand_rows']['identical']}/{x['summand_rows']['rows']}; "
              f"group/t coefficients identical {x['group_L_identical']}/{x['group_lambda_identical']}/{x['L_identical']}/{x['lambda_identical']}; "
              f"layer-2 width-11 agreement {x['layer2_agrees_to_width_11']}; refinement 121->1331 failed {x['refinement_121_to_1331']['failed']}")
        print(f"    L    {x['L_first_11']}\n    lam  {x['lambda_first_11']}")
    print(f"  Q first 11: {rr['Q_first_11']} (order {rr['Q_t_order']}, leading {rr['Q_leading']}); identical to theirs {rr['Q_identical_to_theirs']}; denominator constant {rr['denominator_constant']}")
    cn = cup_normalisation(cv, rr)
    print(f"  cup: J_E = {cn['J_E']}, J_0 = {cn['J_0']}, ratio {cn['ratio']}; 389: dim {cn['structure_389']['dimension']} rank {cn['structure_389']['rank']} radical {cn['structure_389']['radical_dimension']} gauge {cn['structure_389']['gauge_in_radical']}; "
          f"19: dim {cn['structure_19']['dimension']} rank {cn['structure_19']['rank']} radical {cn['structure_19']['radical_dimension']} gauge {cn['structure_19']['gauge_in_radical']}; "
          f"Q_cup first 11 {cn['Q_cup_first_11']} identical {cn['Q_cup_identical_to_theirs']}; rescaling invariant {cn['rescaling']['invariant']}")
    extra = {}
    if deep:
        for key in ("target", "calibrator"):
            c = cv[key]
            s4 = series_from_layer(c, LAYER + 1)
            ref = refinement(c, rr["_series"][key], s4, LAYER)
            extra[key] = {"units_at_14641": s4["units"], "refinement_1331_to_14641": ref,
                          "series_agree_to_width_121": s4["L"][:WIDTH] == rr["_series"][key]["L"] and s4["lambda"][:WIDTH] == rr["_series"][key]["lambda"]}
            print(f"  deep {key}: 1331->14641 refinement failed {ref['failed']} of {ref['cells']}; width-121 agreement {extra[key]['series_agree_to_width_121']}")
    lab = labels()
    ok = rr["agrees"] and cn["agrees"] and lab["agrees"] and all(v["refinement_1331_to_14641"]["agrees"] and v["series_agree_to_width_121"] for v in extra.values())
    rr.pop("_series", None)
    out = {"gate": "src83", "round": "RUN-081", "relative_regulator": rr, "cup": cn, "deep": extra, "labels": lab, "agrees": ok}
    LOGS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"  agrees: {ok} -> {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
