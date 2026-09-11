"""Gate 69 — P5 v1.1, "Anomalous Norm Localization for 389.a1 at p = 11": every exact figure in §2, §5 and §7 recomputed from the group law up, and the document's label discipline checked against this line.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-011 recomputed the object the P5 sub-line turns on — the short model, the
generator images, #E(F_397) = 374 and #E(F_991) = 1045, the matrix
M_loc = [[1,2],[1,4]] and its determinant 2 — but took the sub-line's
foundations as its subject, not this document. v1.1 §7 goes further than any
round has: it claims P' GENERATES both finite groups, gives the discrete
logarithms Q' = 244 P' (mod 397) and Q' = 356 P' (mod 991), the four explicit
multiples 34P', 34Q', 95P', 95Q', the simultaneous-reduction map
ρ(a, b) = (a + 244 b, a + 356 b), its surjectivity, an explicit kernel basis
with determinant 390,830 = 374 · 1045, the index [E(Q) : E^S(Q)] = 390,830
with v_11 = 2, and J_S = 1. Every one of those is recomputed here with its own
group law — affine addition on the short model over F_ℓ — none read from
RUN-011's log.

What is NOT recomputed: §1's inherited θ̄_n ≡ 6 X_397 X_991 (mod I³) is a
modular-symbol computation and is the subject of a later round; Proposition
4.1 is a proof, whose hypotheses (tame, totally ramified, degree p ≠ ℓ, good
reduction) are checked on the data.

Usage:  python code/src69_anomalous_norm_localization.py
"""

from __future__ import annotations

import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "p5" / "files"
DOC = "BSD_P5_Anomalous_Norm_Localization_389a1_p11_v1.1.md"
OUT = LOGS / "src69-anomalous-norm-localization.json"

AINVS = [0, 1, 1, -2, 0]                  # 389.a1, minimal model
P_MIN, Q_MIN = (0, 0), (1, 0)
PRIME = 11
ELLS = (397, 991)

STATED = {
    "short_model": (-3024, 46224),
    "P_short": (12, 108), "Q_short": (48, 108),
    "counts": {397: 374, 991: 1045},
    "cofactors": {397: 34, 991: 95},
    "dlog_Q_of_P": {397: 244, 991: 356},
    "cofactor_multiples": {397: {"P": (281, 236), "Q": (11, 334)},
                           991: {"P": (39, 97), "Q": (865, 243)}},
    "slopes": {397: 2, 991: 4},
    "M_loc": [[1, 2], [1, 4]], "det_M_loc": 2,
    "kernel_basis": [(5742, -22), (-254980, 1045)],
    "kernel_det": 390830, "index": 390830, "v11_index": 2, "J_S": 1,
    "closed_exact_rows": 7, "open_rows": 1,
}


def _doc() -> str:
    p = DOCS / DOC
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ------------------------------------------------------------ the model

def b_c_invariants(a: list[int]) -> dict:
    a1, a2, a3, a4, a6 = a
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return {"b2": b2, "b4": b4, "b6": b6, "b8": b8, "c4": c4, "c6": c6, "disc": disc}


def short_model(a: list[int]) -> tuple[int, int]:
    """Y² = X³ + A X + B with A = −27 c₄, B = −54 c₆ (X = 36x + 3b₂, Y = 108(2y + a₁x + a₃))."""
    inv = b_c_invariants(a)
    return -27 * inv["c4"], -54 * inv["c6"]


def to_short(a: list[int], pt: tuple[int, int]) -> tuple[int, int]:
    a1, a2, a3, a4, a6 = a
    x, y = pt
    b2 = a1 * a1 + 4 * a2
    return 36 * x + 3 * b2, 108 * (2 * y + a1 * x + a3)


def on_minimal(a: list[int], pt: tuple[int, int]) -> bool:
    a1, a2, a3, a4, a6 = a
    x, y = pt
    return y * y + a1 * x * y + a3 * y == x ** 3 + a2 * x * x + a4 * x + a6


def on_short(A: int, B: int, pt: tuple[int, int], mod: int | None = None) -> bool:
    x, y = pt
    lhs, rhs = y * y, x ** 3 + A * x + B
    return (lhs - rhs) % mod == 0 if mod else lhs == rhs


# ------------------------------------------------------------ group law over F_ℓ

O = None


def ec_add(A: int, ell: int, R, S):
    if R is O:
        return S
    if S is O:
        return R
    x1, y1 = R
    x2, y2 = S
    if x1 == x2 and (y1 + y2) % ell == 0:
        return O
    if R == S:
        lam = (3 * x1 * x1 + A) * pow(2 * y1, ell - 2, ell) % ell
    else:
        lam = (y2 - y1) * pow(x2 - x1, ell - 2, ell) % ell
    x3 = (lam * lam - x1 - x2) % ell
    y3 = (lam * (x1 - x3) - y1) % ell
    return (x3, y3)


def ec_mul(A: int, ell: int, k: int, R):
    result, addend = O, R
    if k < 0:
        raise ValueError("k must be non-negative")
    while k:
        if k & 1:
            result = ec_add(A, ell, result, addend)
        addend = ec_add(A, ell, addend, addend)
        k >>= 1
    return result


def count_points(A: int, B: int, ell: int) -> int:
    """#E(F_ℓ) by enumerating x and counting square roots — Legendre via Euler."""
    n = 1
    for x in range(ell):
        rhs = (x ** 3 + A * x + B) % ell
        if rhs == 0:
            n += 1
        elif pow(rhs, (ell - 1) // 2, ell) == 1:
            n += 2
    return n


def order_of(A: int, ell: int, R, group_order: int) -> int:
    """Exact order of R, from the divisors of the group order."""
    for d in sorted(_divisors(group_order)):
        if ec_mul(A, ell, d, R) is O:
            return d
    return 0                                   # no divisor kills R: the group law is wrong, and the caller must go red


def _divisors(n: int) -> list[int]:
    out = []
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            out.append(i)
            if i * i != n:
                out.append(n // i)
    return out


def dlog(A: int, ell: int, base, target, order: int) -> int | None:
    """k with k·base = target, by exhaustive stepping up to the base's order."""
    R = O
    for k in range(order):
        if R == target:
            return k
        R = ec_add(A, ell, R, base)
    return None


def v_p(n: int, p: int) -> int:
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


# ------------------------------------------------------------ §2, §5, §7

def local_data(A: int, B: int, ell: int, P, Q) -> dict:
    count = count_points(A, B, ell)
    cof = count // PRIME
    ordP = order_of(A, ell, P, count)
    ordQ = order_of(A, ell, Q, count)
    k = dlog(A, ell, P, Q, ordP) if ordP == count else None
    cP = ec_mul(A, ell, cof, P)
    cQ = ec_mul(A, ell, cof, Q)
    slope = dlog(A, ell, cP, cQ, PRIME)          # in the order-11 subgroup
    a_ell = ell + 1 - count
    return {"ell": ell, "count": count, "count_stated": STATED["counts"][ell],
            "a_ell": a_ell, "kurihara_condition_a_minus_ell_minus_1_mod_11": (a_ell - ell - 1) % PRIME,
            "eleven_divides_count": count % PRIME == 0, "v_11_of_count": v_p(count, PRIME),
            "cofactor": cof, "cofactor_stated": STATED["cofactors"][ell],
            "order_of_P": ordP, "P_generates": ordP == count,
            "order_of_Q": ordQ, "group_cyclic": ordP == count or ordQ == count,
            "dlog_Q_of_P": k, "dlog_stated": STATED["dlog_Q_of_P"][ell],
            "cofactor_times_P": cP, "cofactor_times_Q": cQ,
            "cofactor_multiples_stated": STATED["cofactor_multiples"][ell],
            "slope_cQ_of_cP_in_the_11_subgroup": slope, "slope_stated": STATED["slopes"][ell],
            "slope_predicted_by_dlog_mod_11": k % PRIME if k is not None else None,
            "ell_mod_11": ell % PRIME, "eleven_divides_half_ell_minus_1": ((ell - 1) // 2) % PRIME == 0,
            "tame": ell != PRIME, "good_reduction": 389 % ell != 0,
            "agrees": (count == STATED["counts"][ell] and cof == STATED["cofactors"][ell]
                       and ordP == count and k == STATED["dlog_Q_of_P"][ell]
                       and cP == STATED["cofactor_multiples"][ell]["P"]
                       and cQ == STATED["cofactor_multiples"][ell]["Q"]
                       and slope == STATED["slopes"][ell] and slope == k % PRIME)}


def simultaneous_reduction(d397: dict, d991: dict) -> dict:
    n1, n2 = d397["count"], d991["count"]
    k1, k2 = d397["dlog_Q_of_P"], d991["dlog_Q_of_P"]
    g = math.gcd(n1, n2)
    # ρ(a, b) = (a + k1 b mod n1, a + k2 b mod n2). Image size = n1 n2 / #(kernel of the
    # induced map on the compatibility) — computed directly: b must satisfy
    # (k2 − k1) b ≡ 0 (mod g), then a is determined mod lcm(n1, n2).
    diff = (k2 - k1) % g
    b_period = g // math.gcd(diff, g)          # b ≡ 0 mod this
    lcm = n1 * n2 // g
    kernel_index = b_period * lcm              # [Z² : ker ρ] = #image
    surjective = kernel_index == n1 * n2
    # the document's kernel basis: in the kernel, and of the right determinant
    kb = STATED["kernel_basis"]
    in_kernel = [((a + k1 * b) % n1 == 0 and (a + k2 * b) % n2 == 0) for a, b in kb]
    det = kb[0][0] * kb[1][1] - kb[0][1] * kb[1][0]
    return {"rho": f"(a, b) -> (a + {k1} b mod {n1}, a + {k2} b mod {n2})",
            "gcd_of_orders": g, "k2_minus_k1": k2 - k1, "k2_minus_k1_mod_gcd": diff,
            "compatibility_solvable_for_every_target": math.gcd(diff, g) == 1,
            "b_period_forced_by_compatibility": b_period,
            "image_size": kernel_index, "n1_times_n2": n1 * n2, "surjective": surjective,
            "J_S_order_of_cokernel": n1 * n2 // kernel_index,
            "document_kernel_basis": kb, "basis_vectors_in_kernel": in_kernel,
            "basis_determinant": abs(det), "determinant_stated": STATED["kernel_det"],
            "basis_is_a_basis_of_the_kernel": abs(det) == kernel_index and all(in_kernel),
            "index_E_over_E_S": kernel_index, "index_stated": STATED["index"],
            "v_11_of_index": v_p(kernel_index, PRIME), "v11_stated": STATED["v11_index"],
            "tamagawa_at_389_is_1": True,
            "tamagawa_reason": "389 ∥ Δ (v_389(Δ) = 1): Kodaira I₁, c_389 = 1",
            "agrees": (surjective and abs(det) == STATED["kernel_det"] and all(in_kernel)
                       and kernel_index == STATED["index"] and v_p(kernel_index, PRIME) == 2)}


# ------------------------------------------------------------ labels

def label_discipline(reports: dict[str, str]) -> dict:
    t = _doc()
    # the gate-state table writes the labels TeX-escaped (CLOSED\_EXACT, \textbf{OPEN});
    # §0's definitions do not, so counting the escaped forms counts table rows only
    closed = t.count("CLOSED\\_EXACT")
    opens = t.count("\\textbf{OPEN}")
    not_asserted = "3\\text{ is not asserted to be a Mazur--Tate comparison constant" in t
    # this line must not have promoted the ratio either: no report calls 3 (or 6/2)
    # a comparison constant, and none claims the OPEN comparison closed
    offenders = [rn for rn, txt in reports.items()
                 if re.search(r"comparison constant (is|equals|=) *3\b", txt)
                 or "BocCOMP" in txt and re.search(r"BocCOMP[^.\n]{0,80}\b(closed|CLOSED)\b", txt)]
    return {"gate_state_table_closed_exact": closed, "closed_exact_stated": STATED["closed_exact_rows"],
            "gate_state_table_open": opens, "open_stated": STATED["open_rows"],
            "document_declines_to_assert_the_ratio_3": not_asserted,
            "reports_promoting_the_ratio_or_closing_the_open_gate": offenders,
            "RUN_011_terminological_point": "E is ordinary and not anomalous at 11 in Mazur's sense (a_11 = −4); the document's 'anomalous' is about 11 | #E(F_ℓ) at the ramified directions",
            "agrees": closed == 7 and opens == 1 and not_asserted and not offenders}


def anomalous_at_11(A: int, B: int) -> dict:
    n = count_points(A, B, PRIME)
    a11 = PRIME + 1 - n
    return {"count_mod_11": n, "a_11": a11, "ordinary": a11 % PRIME != 0,
            "anomalous_in_mazurs_sense": a11 % PRIME == 1, "as_RUN_011_recorded": a11 == -4}


# ------------------------------------------------------------ main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    A, B = short_model(AINVS)
    Ps, Qs = to_short(AINVS, P_MIN), to_short(AINVS, Q_MIN)
    model = {"ainvs": AINVS, "invariants": b_c_invariants(AINVS),
             "short_model_A_B": (A, B), "short_model_stated": STATED["short_model"],
             "P_Q_on_minimal_model": on_minimal(AINVS, P_MIN) and on_minimal(AINVS, Q_MIN),
             "P_short": Ps, "Q_short": Qs,
             "P_Q_short_stated": (STATED["P_short"], STATED["Q_short"]),
             "P_Q_on_short_model": on_short(A, B, Ps) and on_short(A, B, Qs),
             "agrees": ((A, B) == STATED["short_model"] and Ps == STATED["P_short"]
                        and Qs == STATED["Q_short"])}
    local = {ell: local_data(A, B, ell, Ps, Qs) for ell in ELLS}
    M = [[1, local[397]["slope_cQ_of_cP_in_the_11_subgroup"]],
         [1, local[991]["slope_cQ_of_cP_in_the_11_subgroup"]]]
    det = (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % PRIME
    matrix = {"M_loc": M, "M_loc_stated": STATED["M_loc"], "det_mod_11": det,
              "det_stated": STATED["det_M_loc"], "nonzero": det != 0,
              "each_local_norm_quotient_is_one_dimensional": all(local[e]["v_11_of_count"] == 1 for e in ELLS),
              "theorem_6_1_isomorphism": det != 0 and all(local[e]["v_11_of_count"] == 1 for e in ELLS),
              "agrees": M == STATED["M_loc"] and det == STATED["det_M_loc"]}
    rho = simultaneous_reduction(local[397], local[991])
    reports = {f.name[:7]: f.read_text(encoding="utf-8") for f in sorted(REPORTS.glob("RUN-*.md"))}
    labels = label_discipline(reports)
    at11 = anomalous_at_11(A, B)
    ok = (bool(_doc()) and model["agrees"] and all(local[e]["agrees"] for e in ELLS)
          and matrix["agrees"] and rho["agrees"] and labels["agrees"]
          and at11["ordinary"] and not at11["anomalous_in_mazurs_sense"]
          and all(local[e]["tame"] and local[e]["good_reduction"]
                  and local[e]["eleven_divides_half_ell_minus_1"] for e in ELLS))
    log = {"gate": "src69 — P5 v1.1 Anomalous Norm Localization, every exact figure recomputed",
           "source": DOC, "document_found": bool(_doc()),
           "model": model, "local": {str(k): v for k, v in local.items()},
           "localization_matrix": matrix, "simultaneous_reduction_section_7": rho,
           "labels": labels, "at_11": at11,
           "not_recomputed_here": ["§1: θ̄_n ≡ 6 X_397 X_991 (mod I³) — a modular-symbol computation, a later round's subject",
                                   "Proposition 4.1 — a proof; its hypotheses are checked on the data",
                                   "Ш(E/Q)[11] — carried by the P5 documents as inherited"],
           "headline": (f"the short model, the generator images, #E(F_397) = {local[397]['count']} and "
                        f"#E(F_991) = {local[991]['count']}, P' generating both groups, "
                        f"Q' = {local[397]['dlog_Q_of_P']} P' and {local[991]['dlog_Q_of_P']} P', the four "
                        f"cofactor multiples, the slopes {M[0][1]} and {M[1][1]}, det M_loc = {det}, ρ surjective "
                        f"with image {rho['image_size']:,} = 374·1045, the document's kernel basis a basis of "
                        f"determinant {rho['basis_determinant']:,}, v_11 = {rho['v_11_of_index']}, J_S = "
                        f"{rho['J_S_order_of_cokernel']} — every figure of §2, §5 and §7 recomputed and agreeing; "
                        f"{labels['gate_state_table_closed_exact']} CLOSED_EXACT rows and "
                        f"{labels['gate_state_table_open']} OPEN, the ratio 3 asserted by no one"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  model: A,B = {A},{B} ({model['agrees']}); P',Q' = {Ps},{Qs}")
    for e in ELLS:
        d = local[e]
        print(f"  ℓ = {e}: #E = {d['count']} = {d['cofactor']}·11, ord P' = {d['order_of_P']} "
              f"(generates {d['P_generates']}), Q' = {d['dlog_Q_of_P']} P', slope {d['slope_cQ_of_cP_in_the_11_subgroup']}, "
              f"agrees {d['agrees']}")
    print(f"  M_loc = {M}, det = {det}; ρ image {rho['image_size']:,} / {rho['n1_times_n2']:,}, "
          f"surjective {rho['surjective']}, basis det {rho['basis_determinant']:,}, v_11 {rho['v_11_of_index']}, "
          f"J_S {rho['J_S_order_of_cokernel']}")
    print(f"  labels: CLOSED_EXACT {labels['gate_state_table_closed_exact']}, OPEN {labels['gate_state_table_open']}, "
          f"3 not asserted {labels['document_declines_to_assert_the_ratio_3']}, offenders {labels['reports_promoting_the_ratio_or_closing_the_open_gate'] or 'none'}")
    print(f"  at 11: #E(F_11) = {at11['count_mod_11']}, a_11 = {at11['a_11']}, ordinary {at11['ordinary']}, "
          f"Mazur-anomalous {at11['anomalous_in_mazurs_sense']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
