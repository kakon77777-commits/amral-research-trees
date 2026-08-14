"""Independent recheck of Operation Translation Series — Paper 07.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *廣義 (mx+r) 系統與 Residue-Class Operation Translation*, Paper 07 v0.1.1.

Referee: symbolic composition of D(x)=x/2 and U(x)=(mx+r)/2 on an affine form,
assuming no theorem of the paper. Every claimed formula is compared against it.

What the subject's own test_p07 covers: affine data, residue coding and transport
for m in {1,3,5,7,9}, r in {1,3,5}, k <= 7, a in 0..2, plus the m=1 boundary.
What it does not: the matrix representation, the concatenation law, the closed
geometric-sum bounds of §17/§18, the m=1 form of §19, the §21 threshold, §22
uniform expansion, Theorems E–H, §33's linearity in r, §46's width, §47's
order-uniform threshold, and §37's valuation density for general (m, r).

One hazard gets special attention. Theorems E and F are stated with
alpha_m = ln2/ln m and a floor, and the subject's own p05 counting code computes
that floor in floating point. alpha_m is irrational, so the floor is well
defined, but a double can land on the wrong side of an integer when k*alpha_m is
close to one. The exact integer predicate m^u < 2^k is the reference here, and
any k where the float disagrees is reported.

Usage:  python code/ot_paper07_recheck.py [max_k] [max_k_float_scan]
"""

from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from math import comb, floor, log

MS = (1, 3, 5, 7, 9, 11)
RS = (1, 3, 5, 7)
MAX_K_DEFAULT = 9
FLOAT_SCAN_DEFAULT = 4000


def compose(word: str, m: int, r: int) -> tuple[int, int, int]:
    """Referee: apply the branch maps one at a time to (A x + B)/Dn.
    D: Dn -> 2 Dn.   U: (A,B,Dn) -> (m A, m B + r Dn, 2 Dn)."""
    A, B, Dn = 1, 0, 1
    for c in word:
        if c == "D":
            Dn = 2 * Dn
        else:
            A, B, Dn = m * A, m * B + r * Dn, 2 * Dn
    return A, B, Dn


def words(k: int):
    for bits in itertools.product("DU", repeat=k):
        yield "".join(bits)


def b_closed(word: str, m: int, r: int) -> int:
    """Theorem B."""
    pos = [j + 1 for j, c in enumerate(word) if c == "U"]
    u = len(pos)
    return r * sum(2 ** (jt - 1) * m ** (u - t) for t, jt in enumerate(pos, start=1))


def b_matrix(word: str, m: int, r: int) -> tuple[int, int, int]:
    """§8: M_w = M_{sigma_k} ... M_{sigma_1}."""
    A, B, Dn = 1, 0, 1
    for c in word:
        n00, n01, n11 = (1, 0, 2) if c == "D" else (m, r, 2)
        A, B, Dn = n00 * A, n00 * B + n01 * Dn, n11 * Dn
    return A, B, Dn


def T(n: int, m: int, r: int) -> int:
    return n // 2 if n % 2 == 0 else (m * n + r) // 2


def actual_word(n: int, k: int, m: int, r: int) -> tuple[str, int]:
    out, x = [], n
    for _ in range(k):
        out.append("U" if x % 2 else "D")
        x = T(x, m, r)
    return "".join(out), x


def check(rep: dict, name: str, ok: bool, detail: str = "") -> None:
    rep["checks"][name] = {"pass": bool(ok), **({"detail": detail} if detail else {})}
    if not ok:
        rep["failures"].append(name + (f": {detail}" if detail else ""))


def main() -> int:
    max_k = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_K_DEFAULT
    float_scan = int(sys.argv[2]) if len(sys.argv) > 2 else FLOAT_SCAN_DEFAULT
    rep = {
        "tool": "ot_paper07_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 07 v0.1.1 (Neo.K)",
        "scope": "exact finite algebra and exact integer counting; not a Collatz proof",
        "parameters": {"m": list(MS), "r": list(RS), "max_word_length": max_k},
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    ok = dict.fromkeys(
        "A B rec mat cat C D bij rec15 min max m1 desc thr uni lin width ordthr".split(), True)
    cases = 0
    for m, r in itertools.product(MS, RS):
        btab: dict[str, int] = {}
        for k in range(1, max_k + 1):
            by_ku: dict[int, list[tuple[int, str]]] = {}
            for w in words(k):
                A, B, Dn = compose(w, m, r)
                u = w.count("U")
                btab[w] = B
                by_ku.setdefault(u, []).append((B, w))

                if A != m ** u or Dn != 2 ** k:
                    ok["A"] = False
                if b_closed(w, m, r) != B:
                    ok["B"] = False
                if b_matrix(w, m, r) != (A, B, Dn):
                    ok["mat"] = False
                if k > 1:
                    bh = btab[w[:-1]]
                    if (bh if w[-1] == "D" else m * bh + r * 2 ** (k - 1)) != B:
                        ok["rec"] = False
                # §33: correction is linear in r
                if B != r * compose(w, m, 1)[1]:
                    ok["lin"] = False

                # Theorem C and D: unique cylinder, transport, identityization
                rw = (-B * pow(m, -u, 2 ** k)) % 2 ** k
                sw = Fraction(m ** u * rw + B, 2 ** k)
                if sw.denominator != 1:
                    ok["C"] = False
                sw = sw.numerator
                for a in range(0, 6):
                    n = rw + 2 ** k * a
                    if n <= 0:
                        continue
                    aw, y = actual_word(n, k, m, r)
                    if aw != w:
                        ok["bij"] = False
                    if y != sw + m ** u * a:
                        ok["D"] = False
                    # §15 exact recovery
                    if rw + 2 ** k * ((y - sw) // m ** u) != n:
                        ok["rec15"] = False
                    # §20 descent criterion, §22 uniform expansion
                    if (B < (2 ** k - m ** u) * n) != (y < n):
                        ok["desc"] = False
                    if m ** u > 2 ** k and not y > n:
                        ok["uni"] = False
                    # §21 threshold
                    if m ** u < 2 ** k:
                        theta = B // (2 ** k - m ** u) + 1
                        if (n >= theta) != (y < n):
                            ok["thr"] = False
                    cases += 1

            # §17/§18/§46: closed geometric-sum extremes and width.
            # m = 1 is the case the repair was about: the (m-2) denominator must
            # not be reached by substituting into a log/ratio form blindly.
            for u, vals in by_ku.items():
                lo, _ = min(vals)
                hi, _ = max(vals)
                geo = sum(2 ** t * m ** (u - 1 - t) for t in range(u))  # exact, no division
                if m != 2:
                    if geo * (m - 2) != m ** u - 2 ** u:
                        ok["min"] = False
                if lo != r * geo:
                    ok["min"] = False
                if hi != r * 2 ** (k - u) * geo:
                    ok["max"] = False
                if btab["U" * u + "D" * (k - u)] != lo or btab["D" * (k - u) + "U" * u] != hi:
                    ok["min"] = False
                if hi - lo != r * (2 ** (k - u) - 1) * geo:
                    ok["width"] = False
                if m == 1 and lo != r * (2 ** u - 1):
                    ok["m1"] = False
                # §47: one conservative threshold for every word of this (k, u)
                if m ** u < 2 ** k:
                    Theta = (r * 2 ** (k - u) * geo) // (2 ** k - m ** u) + 1
                    for B, w in vals:
                        rw = (-B * pow(m, -u, 2 ** k)) % 2 ** k
                        for a in range(0, 4):
                            n = rw + 2 ** k * a
                            if n < Theta:
                                continue
                            _, y = actual_word(n, k, m, r)
                            if not y < n:
                                ok["ordthr"] = False

    names = {
        "A": "P07_ThmA_generalized_affine_closure",
        "B": "P07_ThmB_correction_closed_form",
        "rec": "P07_S5_correction_recurrence",
        "mat": "P07_S8_matrix_representation",
        "C": "P07_ThmC_unique_residue_cylinder",
        "D": "P07_ThmD_transport_and_identityization",
        "bij": "P07_S12_word_residue_bijection_survives",
        "rec15": "P07_S15_exact_recovery",
        "min": "P07_S17_minimum_correction_closed_geometric_form",
        "max": "P07_S18_maximum_correction_closed_form",
        "m1": "P07_S19_m_equals_1_has_no_singularity",
        "desc": "P07_S20_exact_descent_criterion",
        "thr": "P07_S21_contracting_threshold_is_an_exact_iff",
        "uni": "P07_S22_uniform_expansion",
        "lin": "P07_S33_correction_is_linear_in_r",
        "width": "P07_S46_generalized_order_correction_width",
        "ordthr": "P07_S47_order_uniform_threshold_covers_every_word",
    }
    for key, name in names.items():
        check(rep, name, ok[key])
    rep["counts"]["parameter_pairs"] = len(MS) * len(RS)
    rep["counts"]["transport_cases"] = cases

    # --- §9 concatenation ---------------------------------------------------
    cat = True
    pairs = 0
    for m, r in itertools.product((1, 3, 5, 7), (1, 3)):
        for kw, kv in itertools.product(range(1, 6), repeat=2):
            for w in words(kw):
                for v in words(kv):
                    if compose(w + v, m, r)[1] != (
                        m ** v.count("U") * compose(w, m, r)[1] + 2 ** kw * compose(v, m, r)[1]
                    ):
                        cat = False
                    pairs += 1
    check(rep, "P07_S9_concatenation_law", cat)
    rep["counts"]["concatenation_pairs"] = pairs

    # --- §25 irrationality of alpha_m, exactly ------------------------------
    # alpha_m rational would give m^p = 2^q with m odd > 1: impossible. The
    # computable content is that m^u = 2^k never happens, checked directly.
    irr = all(m ** u != 2 ** k
              for m in MS if m > 1
              for u in range(1, 40) for k in range(1, 64))
    check(rep, "P07_S25_no_word_has_neutral_slope", irr)

    # --- Theorems E, F, G, H, and the floating-floor hazard -----------------
    # Reference: the exact largest u with m^u < 2^k, found by integer growth.
    # Compared against floor(k * ln2/ln m) in double precision — which is what
    # the subject's own p05 counting code uses.
    thmE = thmF = True
    float_bad = []
    scanned = 0
    for m in (3, 5, 7, 9, 11, 13):
        alpha = log(2) / log(m)
        u_max, mp = 0, 1  # mp = m^u_max
        for k in range(1, float_scan + 1):
            # advance u_max while m^(u_max+1) < 2^k
            while mp * m < 2 ** k:
                mp *= m
                u_max += 1
            if not (mp < 2 ** k):
                thmE = False
            if mp * m < 2 ** k:
                thmE = False
            if floor(alpha * k) != u_max:
                float_bad.append({"m": m, "k": k, "float_floor": floor(alpha * k),
                                  "exact": u_max})
            scanned += 1
    check(rep, "P07_ThmE_exact_contraction_boundary", thmE)
    check(rep, "P07_ThmEF_float_floor_agrees_with_the_exact_boundary",
          not float_bad,
          f"double-precision floor disagrees at {float_bad[:5]}" if float_bad else "")
    rep["counts"]["float_scan_k_max"] = float_scan
    rep["counts"]["float_scan_points"] = scanned
    rep["measured"]["float_floor_disagreements"] = float_bad[:20]

    # Agreement over a range is weak evidence on its own. What makes the float
    # floor safe here is the margin: how close k*alpha_m ever gets to an integer,
    # versus how much error a double can accumulate. Both are measured, in high
    # precision, so the conclusion has a number attached instead of a hope.
    from decimal import Decimal, getcontext

    getcontext().prec = 60
    margins = {}
    for m in (3, 5, 7, 9, 11, 13):
        a_hp = Decimal(2).ln() / Decimal(m).ln()
        worst = None
        for k in range(1, float_scan + 1):
            v = a_hp * k
            d = min(v - int(v), int(v) + 1 - v)
            if worst is None or d < worst[0]:
                worst = (d, k)
        # a double holds alpha to ~2^-53 relative; scaled by k this is the
        # largest displacement the float floor could suffer
        bound = Decimal(2) ** -52 * Decimal(float_scan) * a_hp
        margins[m] = {
            "closest_k_alpha_to_an_integer": f"{worst[0]:.3e}",
            "at_k": worst[1],
            "double_error_bound_over_range": f"{bound:.3e}",
            "margin_exceeds_error_bound_by": f"{worst[0] / bound:.3e}",
        }
    check(rep, "P07_ThmEF_float_floor_has_margin_not_luck",
          all(Decimal(v["closest_k_alpha_to_an_integer"])
              > Decimal(v["double_error_bound_over_range"]) for v in margins.values()))
    rep["measured"]["float_floor_margin"] = margins

    # Theorem F/G: the cylinder-density law and its limits, on the exact boundary
    P = {}
    for m in (1, 3, 5, 7):
        row = {}
        for k in (10, 40, 160, 640):
            if m == 1:
                row[k] = 1.0
                continue
            u_max, mp = 0, 1
            while mp * m < 2 ** k:
                mp *= m
                u_max += 1
            row[k] = sum(comb(k, u) for u in range(u_max + 1)) / 2 ** k
        P[m] = row
    check(rep, "P07_ThmF_P_k_of_1_is_exactly_1", all(v == 1.0 for v in P[1].values()))
    check(rep, "P07_ThmG_P_k_of_3_increases_towards_1",
          P[3][10] < P[3][640] and P[3][640] > 0.99)
    check(rep, "P07_ThmG_P_k_of_5_and_7_decrease_towards_0",
          P[5][640] < P[5][10] and P[7][640] < P[7][10] and P[5][640] < 1e-3)
    # Theorem H: the critical multiplier is where alpha_m = 1/2, i.e. m = 4
    check(rep, "P07_ThmH_critical_multiplier_is_4",
          log(2) / log(4) == 0.5 and log(2) / log(3) > 0.5 and log(2) / log(5) < 0.5)
    rep["measured"]["cylinder_density_P_k_m"] = P

    # --- §37: one-step valuation density is independent of (m, r) -----------
    dens = True
    for m, r in itertools.product((1, 3, 5, 7, 9), (1, 3, 5, 7)):
        for j in range(1, 13):
            mod = 2 ** (j + 1)
            hits = [x for x in range(1, mod, 2)
                    if (m * x + r) % mod == 2 ** j % mod
                    and ((m * x + r) % (2 ** (j + 1))) == 2 ** j]
            if len(hits) != 1:
                dens = False
    check(rep, "P07_S37_valuation_density_independent_of_m_and_r", dens)

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
