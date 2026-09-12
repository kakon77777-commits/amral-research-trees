"""Gate 74 — GPT-6's Attack 05: the one new computation, the 11-adic formal logarithm of P and Q on 389.a1, recomputed with exact rational arithmetic; the Euler-factor constant; the labels.

數學戰士「墜衡」 / AMRAL Research Lab.

Attack 05 computes ℓ(R) = log_ω(R)/11 mod 11 for R = P = (0,0), Q = (1,0):
since #E(F₁₁) = 16, [16]R lies in the formal group; with s = −x/y its formal
parameter, log_ω(s) ≡ s (mod 11²) for s ∈ 11Z₁₁, so ℓ(R) ≡ s([16]R)/(16·11)
(mod 11). The document reports s([16]P) ≡ 99, s([16]Q) ≡ 66 (mod 121), both
of valuation 1, hence (ℓ̄(P), ℓ̄(Q)) = (4, 10) and ker ℓ̄ = k·(P + 4Q). It also
gives the exact coordinates of [16]P and [16]Q. All of it is recomputed here
with the gate's own group law over Q (Fractions), and the exact coordinates
are compared to the document's to the last digit.

Also checked: #E(F₁₁) = 16 by enumeration; a₁₁ = −4 ≢ 1 (non-anomalous);
the premise n − v₁₁(n) ≥ 2 for n ≥ 2 behind "log ≡ s mod 121"; the
Euler-factor constant 374·1045/(397·991) = 11²·3230/393427 with 3230/393427
≡ 7 (mod 11). The Selmer-complex derivations (det H_γ a unit, L₁₁ = t²U,
the torsion Z/11, the index 11²) are read, not computed — they rest on
Kato's bound and Kataoka's Coleman map as cited.

Usage:  python code/src74_attack05_local_log.py
"""

from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src70_kurihara_modular_symbols as kur              # noqa: E402

LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external" / "gpt6-proof-attacks" / "extracted" / "05"
DOC = EXT / "BSD_Proof_Attack_05_Rank_Two_Regulator.md"
THEIR_RESULT = EXT / "local_log_result.json"
OUT = LOGS / "src74-attack05-local-log.json"

P = 11
AINVS = (0, 1, 1, -2, 0)                                  # y² + y = x³ + x² − 2x
EULER_PAIRS = ((374, 397), (1045, 991))                   # #E(F_ℓ)/ℓ for the two auxiliary primes
PREMISE_START = 2                                          # n − v₁₁(n) ≥ 2 is checked from this n on
STATED = {"s_P_mod_121": 99, "s_Q_mod_121": 66, "v11": 1, "ell_P": 4, "ell_Q": 10, "count_F11": 16}


# ------------------------------------------------------------ exact group law over Q

def on_curve(pt) -> bool:
    if pt is None:
        return True
    a1, a2, a3, a4, a6 = AINVS
    x, y = pt
    return y * y + a1 * x * y + a3 * y == x ** 3 + a2 * x * x + a4 * x + a6


def neg(pt):
    if pt is None:
        return None
    a1, a2, a3, a4, a6 = AINVS
    x, y = pt
    return (x, -y - a1 * x - a3)


def add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    a1, a2, a3, a4, a6 = AINVS
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        if y1 + y2 + a1 * x2 + a3 == 0:
            return None
        lam = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) / (2 * y1 + a1 * x1 + a3)
        nu = (-x1 ** 3 + a4 * x1 + 2 * a6 - a3 * y1) / (2 * y1 + a1 * x1 + a3)
    else:
        lam = (y2 - y1) / (x2 - x1)
        nu = (y1 * x2 - y2 * x1) / (x2 - x1)
    x3 = lam * lam + a1 * lam - a2 - x1 - x2
    y3 = -(lam + a1) * x3 - nu - a3
    return (x3, y3)


def mul(k: int, pt):
    result, addend = None, pt
    while k:
        if k & 1:
            result = add(result, addend)
        addend = add(addend, addend)
        k >>= 1
    return result


def v_p(q: Fraction, p: int = P) -> int:
    n, d = q.numerator, q.denominator
    v = 0
    while n and n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def residue(q: Fraction, mod: int):
    """q mod `mod` for an 11-integral rational; None when q is not 11-integral (a gate must go red, not raise)."""
    if q.denominator % P == 0:
        return None
    return q.numerator * pow(q.denominator, -1, mod) % mod


def formal_parameter(x: Fraction, y: Fraction) -> Fraction:
    """z = −x/y, the formal-group parameter of a Weierstrass model at O."""
    return -x / y


def reduction_group_order() -> int:
    return kur.count_points_general(list(AINVS), P)


def normalise(s: Fraction, n: int) -> Fraction:
    """ℓ(R) = log_ω(R)/11 ≡ s([n]R)/(n·11) (mod 11) for s ∈ 11Z₁₁."""
    return s / (n * P)


# ------------------------------------------------------------ the computation

def local_log(label: str, pt) -> dict:
    n = reduction_group_order()                          # 16
    R = mul(n, pt)
    assert on_curve(R)
    x, y = R
    s = formal_parameter(x, y)
    v = v_p(s)
    s121 = residue(s, 121)
    ell = residue(normalise(s, n), P)
    return {"point": label, "input": [int(pt[0]), int(pt[1])], "multiple": n, "point16": [str(x), str(y)],
            "formal_parameter_s_exact": str(s), "v11_of_s": v, "s_mod_121": s121,
            "log_over_11_mod_11": ell,
            "x_is_11_adically_large": v_p(x) < 0, "v11_x": v_p(x), "v11_y": v_p(y)}


def premises() -> dict:
    n11 = kur.count_points_general(list(AINVS), P)
    a11 = P + 1 - n11
    log_premise = all(n - _v(n) >= 2 for n in range(PREMISE_START, 400))
    prod = Fraction(EULER_PAIRS[0][0] * EULER_PAIRS[1][0], EULER_PAIRS[0][1] * EULER_PAIRS[1][1])
    v2 = v_p(prod)
    unit = prod / P ** v2
    return {"count_F11": n11, "a_11": a11, "non_anomalous_a11_not_1_mod_11": a11 % P != 1,
            "n_minus_v11_n_at_least_2_for_n_2_to_399": log_premise,
            "euler_constant_374_1045_over_397_991": str(prod), "its_v11": v2,
            "unit_part": str(unit), "unit_part_mod_11": residue(unit, P) if v2 >= 0 else None,
            "three_two_three_zero_check": 374 * 1045 == 121 * 3230,
            "agrees": n11 == 16 and a11 == -4 and log_premise and v2 == 2 and residue(unit, P) == 7}


def compare_with_theirs(mine: dict) -> dict:
    if not THEIR_RESULT.exists():
        return {"present": False}
    t = json.loads(THEIR_RESULT.read_text(encoding="utf-8"))
    out = {"present": True}
    ok = True
    for lab in ("P", "Q"):
        th = t["points"][lab]
        me = mine[lab]
        same16 = [str(Fraction(v)) for v in th["point16"]] == me["point16"]
        same_s = str(Fraction(th["formal_t_exact"])) == me["formal_parameter_s_exact"]
        out[lab] = {"point16_identical": same16, "formal_parameter_identical": same_s,
                    "their_s_mod_121": th["formal_t_mod121"], "their_ell": th["log_over_11_mod11"]}
        ok = ok and same16 and same_s and th["formal_t_mod121"] == me["s_mod_121"] and th["log_over_11_mod11"] == me["log_over_11_mod_11"]
    out["agrees"] = ok
    return out


def labels() -> dict:
    t = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
    return {"document_found": bool(t),
            "says_no_full_BSD": "沒有宣稱完整 BSD" in t,
            "says_unreviewed": "尚未經獨立審查" in t,
            "height_matrix_entries_not_computed": "沒有聲稱已數值算出高度矩陣每個 entry" in t,
            "rests_on_cited_theorems": "Kim–Lee–Ponsinet" in t and "Kataoka" in t,
            "agrees": bool(t) and "沒有宣稱完整 BSD" in t and "尚未經獨立審查" in t}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    Pt, Qt = (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))
    assert on_curve(Pt) and on_curve(Qt)
    res = {"P": local_log("P", Pt), "Q": local_log("Q", Qt)}
    ker = (res["P"]["log_over_11_mod_11"] + 4 * res["Q"]["log_over_11_mod_11"]) % P
    pre = premises()
    cmp_ = compare_with_theirs(res)
    lab = labels()
    stated_ok = (res["P"]["s_mod_121"] == STATED["s_P_mod_121"] and res["Q"]["s_mod_121"] == STATED["s_Q_mod_121"]
                 and res["P"]["v11_of_s"] == 1 and res["Q"]["v11_of_s"] == 1
                 and res["P"]["log_over_11_mod_11"] == STATED["ell_P"] and res["Q"]["log_over_11_mod_11"] == STATED["ell_Q"])
    ok = stated_ok and ker == 0 and pre["agrees"] and cmp_.get("agrees", False) and lab["agrees"]
    log = {"gate": "src74 — Attack 05's local logarithm, exact",
           "source": str(DOC.relative_to(ROOT)).replace("\\", "/"),
           "local_log": res, "ell_of_P_plus_4Q_mod_11": ker, "kernel_is_P_plus_4Q": ker == 0,
           "premises": pre, "comparison_with_the_documents_output": cmp_, "labels": lab, "stated": STATED,
           "not_computed_here": ["det H_γ ∈ O^× and L₁₁(E,t) = t²U(t) — derived from Kato's one-sided bound and the Coleman map, read",
                                 "H²(G_{Q,Σ},T) ≅ O ⊕ O/11 and the index 11² — Selmer-complex derivations, read",
                                 "Theorem 6.1 (κ_prim = u₀·adj(H_γ)ℓ) — read"],
           "headline": (f"[16]P and [16]Q computed exactly and identical to the document's coordinates; "
                        f"s([16]P) ≡ {res['P']['s_mod_121']}, s([16]Q) ≡ {res['Q']['s_mod_121']} (mod 121), both of "
                        f"valuation 1; ℓ̄ = ({res['P']['log_over_11_mod_11']}, {res['Q']['log_over_11_mod_11']}), "
                        f"ker ℓ̄ ∋ P + 4Q; #E(F₁₁) = {pre['count_F11']}; the Euler constant is 11² times a unit ≡ "
                        f"{pre['unit_part_mod_11']}"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    for lab_ in ("P", "Q"):
        r = res[lab_]
        print(f"  {lab_}: [16]{lab_} x-denominator digits {len(str(Fraction(r['point16'][0]).denominator))}, "
              f"s ≡ {r['s_mod_121']} (mod 121), v₁₁ = {r['v11_of_s']}, ℓ̄ = {r['log_over_11_mod_11']}")
    print(f"  ℓ̄(P + 4Q) = {ker}; premises {pre['agrees']}; identical to their output {cmp_.get('agrees')}; labels {lab['agrees']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


def _v(n: int) -> int:
    v = 0
    while n % P == 0:
        n //= P
        v += 1
    return v


if __name__ == "__main__":
    raise SystemExit(main())
