#!/usr/bin/env python3
"""Exact algebra for a new rational-equivalence construction on 389a1 squared.

Python 3.9+, standard library only. This is not a BSD or Kato-regulator check.
Polynomial arrays are in ascending order. No input from prior certificates.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return trim(c)


def scale(a, c):
    return trim([c * x for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def power(a, n):
    c = [1]
    for _ in range(n):
        c = mul(c, a)
    return c


def evaluate(a, x):
    c = F(0)
    for y in reversed(a):
        c = c * x + y
    return c


def derivative(a):
    return trim([i * a[i] for i in range(1, len(a))])


def modpoly(a, p):
    return trim([x % p for x in a])


def divmodp(a, b, p):
    a, b = modpoly(a, p), modpoly(b, p)
    if b == [0]:
        raise ZeroDivisionError
    q = [0] * max(1, len(a) - len(b) + 1)
    while a != [0] and len(a) >= len(b):
        j = len(a) - len(b)
        k = a[-1] * pow(b[-1], -1, p) % p
        q[j] = (q[j] + k) % p
        a = modpoly(sub(a, [0] * j + scale(b, k)), p)
    return trim(q), a


def xgcdp(a, b, p):
    r0, r1 = modpoly(a, p), modpoly(b, p)
    s0, s1, t0, t1 = [1], [0], [0], [1]
    while r1 != [0]:
        q, r2 = divmodp(r0, r1, p)
        r0, r1 = r1, r2
        s0, s1 = s1, modpoly(sub(s0, mul(q, s1)), p)
        t0, t1 = t1, modpoly(sub(t0, mul(q, t1)), p)
    k = pow(r0[-1], -1, p)
    return tuple(modpoly(scale(a, k), p) for a in (r0, s0, t0))


def sum_poly(*items):
    ans = [0]
    for a in items:
        ans = add(ans, a)
    return ans


def require_equal(actual, expected, step):
    if actual != expected:
        raise ArithmeticError(f"{step}: {actual!r} != {expected!r}")


def cycle(*terms):
    ans = {}
    for a, b, n in terms:
        key = (a, b)
        ans[key] = ans.get(key, 0) + n
    return {k: v for k, v in ans.items() if v}


def cycle_sum(*terms):
    ans = {}
    for multiplier, a in terms:
        for key, n in a.items():
            ans[key] = ans.get(key, 0) + multiplier * n
    return {k: v for k, v in ans.items() if v}


def encode_cycle(a):
    return [{"point": list(k), "coefficient": v} for k, v in sorted(a.items())]


def box(a, b):
    return cycle((a, b, 1), (a, "O", -1), ("O", b, -1), ("O", "O", 1))


def diagonal_chain_boundary(r):
    nr = "-" + r
    diagonal = cycle((r, r, 1), (nr, nr, 1), ("O", "O", -2))
    horizontal = cycle((r, nr, 1), (nr, nr, 1), ("O", nr, -2))
    vertical = cycle((r, r, 1), (r, nr, 1), (r, "O", -2))
    origin_vertical = cycle(("O", r, 1), ("O", nr, 1), ("O", "O", -2))
    return cycle_sum((1, diagonal), (-1, horizontal), (1, vertical), (-2, origin_vertical))


def add_distinct_points(p, q):
    x, y = p
    u, v = q
    if x == u:
        raise ValueError("Only distinct x-coordinates are used in this construction")
    slope = (v-y)/(u-x)
    intercept = y-slope*x
    X = slope*slope-1-x-u
    return X, -slope*X-intercept-1


def compute():
    d, n, m, linear = [1, 1, 1], [-2, -3], [1, -1, -2], [2, 3]
    # x1=n/d, x2=m/d. F is the off-diagonal conic.
    conic = sum_poly(power(n, 2), mul(n, m), power(m, 2), mul(n, d), mul(m, d), scale(power(d, 2), -2))
    require_equal(conic, [0], "conic parametrization")
    f_num = sum_poly(power(d, 3), scale(power(n, 3), 4), scale(mul(power(n, 2), d), 4), scale(mul(n, power(d, 2)), -8))
    f_num_second = sum_poly(power(d, 3), scale(power(m, 3), 4), scale(mul(power(m, 2), d), 4), scale(mul(m, power(d, 2)), -8))
    require_equal(f_num, f_num_second, "same ordinate for the two maps to E")
    f8 = mul(d, f_num)
    tangent = sum_poly(scale(n, 2), scale(m, 3), scale(d, -3))
    require_equal(tangent, scale(power(linear, 2), -1), "tangent function numerator")

    squarefree_gcd, bezout_s, bezout_t = xgcdp(f8, derivative(f8), 11)
    require_equal(squarefree_gcd, [1], "squarefree hyperelliptic polynomial modulo 11")
    bezout_residual = modpoly(sum_poly(mul(bezout_s, f8), mul(bezout_t, derivative(f8)), [-1]), 11)
    require_equal(bezout_residual, [0], "Bezout witness")
    require_equal(len(f8) - 1, 8, "hyperelliptic degree")
    require_equal(f8[-1], 1, "two rational points at parameter infinity")

    s0 = -F(2, 3)
    d0 = evaluate(d, s0)
    x1, x2 = evaluate(n, s0) / d0, evaluate(m, s0) / d0
    require_equal((x1, x2, d0), (F(0), F(1), F(7, 9)), "target fibre")
    require_equal(evaluate(f8, s0), d0**4, "unramified target fibre W=plus/minus d^2")
    pole_numerator = divmodp(f_num, d, 11)[1]
    pole_gcd = xgcdp(d, f_num, 11)[0]
    require_equal(pole_gcd, [1], "simple branch points over d=0")
    require_equal(xgcdp(d, linear, 11)[0], [1], "no cancellation in tangent function")
    # Exact rational point checks on the elliptic curve.
    points = {"P": [0, 0], "-P": [0, -1], "Q": [1, 0], "-Q": [1, -1]}
    for name, (x, y) in points.items():
        require_equal(y*y+y-x*x*x-x*x+2*x, 0, f"E point {name}")

    # Divisor of g: zero order 2 at each of the two unramified points;
    # pole order 2 at the two ramified points above d=0, both mapping to (O,O).
    div_c = cycle(("P", "Q", 2), ("-P", "-Q", 2), ("O", "O", -4))
    div_h = cycle(("P", "-Q", 1), ("-P", "-Q", 1), ("O", "-Q", -2))
    div_v = cycle(("P", "Q", 1), ("P", "-Q", 1), ("P", "O", -2))
    div_v0 = cycle(("O", "Q", 1), ("O", "-Q", 1), ("O", "O", -2))
    boundary = cycle_sum((1, div_c), (-2, div_h), (2, div_v), (-4, div_v0))
    target = cycle_sum((4, box("P", "Q")))
    require_equal(boundary, target, "boundary Gamma_PQ=4 box(P,Q)")
    residual = cycle_sum((1, boundary), (-1, target))
    diagonal_results = {}
    for r in ("P", "Q"):
        actual = diagonal_chain_boundary(r)
        require_equal(actual, cycle_sum((2, box(r, r))), f"diagonal boundary {r}")
        diagonal_results[r] = encode_cycle(actual)
    swapped = {(b, a): k for (a, b), k in boundary.items()}
    require_equal(swapped, cycle_sum((4, box("Q", "P"))), "swapped cross boundary")

    # Fresh finite input for the Tate/biextension part: disjoint representatives.
    point_p, point_q = (F(0), F(0)), (F(1), F(0))
    r = add_distinct_points(point_p, point_q)
    p_plus_r, q_plus_r = add_distinct_points(point_p, r), add_distinct_points(point_q, r)
    require_equal(r, (F(-2), F(-1)), "translation R")
    require_equal(p_plus_r, (F(5, 4), F(-13, 8)), "P+R")
    require_equal(q_plus_r, (F(1, 9), F(-19, 27)), "Q+R")
    for name, a in (("R", r), ("P+R", p_plus_r), ("Q+R", q_plus_r)):
        x, y = a
        require_equal(y*y+y-x*x*x-x*x+2*x, 0, "shifted E point " + name)
    require_equal(set((r, p_plus_r, q_plus_r)) & set((point_p, point_q)), set(), "disjoint divisor supports")

    # Full tensor basis: e1e1,e1e2,e2e1,e2e2.
    alternating_tensor = [F(0), F(1), F(-1), F(0)]
    transpose_tensor = [alternating_tensor[i] for i in (0, 2, 1, 3)]
    symmetric_projection = [(a+b)/2 for a, b in zip(alternating_tensor, transpose_tensor)]
    weil_value = alternating_tensor[1]-alternating_tensor[2]
    require_equal(symmetric_projection, [0, 0, 0, 0], "symmetric quotient kills alternating line")
    require_equal(weil_value, 2, "Weil pairing does not factor through symmetric quotient")

    return {
        "task": "BSD Proof Attack 07: explicit relative cycle construction",
        "arithmetic": "exact integers, fractions and F_11 polynomials; standard library only",
        "curve": {"ainvs": [0, 1, 1, -2, 0], "points": points},
        "polynomials_ascending": {"d": d, "n": n, "m": m, "F6": f_num, "F8": f8},
        "identities": {"conic_numerator": conic, "same_ordinate_residual": sub(f_num, f_num_second), "tangent_numerator": tangent},
        "smoothness_certificate_mod_11": {"gcd": squarefree_gcd, "bezout_s": bezout_s, "bezout_t": bezout_t, "residual_sF8_plus_tF8prime_minus_1": bezout_residual, "genus": 3},
        "divisor_geometry": {
            "zero_parameter": str(s0), "d_at_zero": str(d0), "W_at_zero": [str(d0*d0), str(-d0*d0)],
            "zero_images": [["P", "Q"], ["-P", "-Q"]], "zero_orders": [2, 2],
            "pole_locus": "d(s)=0, a degree-two closed point with residue field Q(sqrt(-3))",
            "F6_mod_d_mod11": pole_numerator, "gcd_d_F6_mod11": pole_gcd,
            "valuation_at_each_geometric_pole": {"d": 2, "W": 1, "x1": -2, "x2": -2, "2y+1": -3, "g": -2},
            "pole_images": [["O", "O"], ["O", "O"]],
            "parameter_infinity_g_value": -9,
            "scope": "Orders follow from the local-parameter proof in the manuscript; code verifies its polynomial hypotheses."
        },
        "four_chain_boundaries": {"C_g": encode_cycle(div_c), "H_x": encode_cycle(div_h), "V_x_minus_1": encode_cycle(div_v), "V0_x_minus_1": encode_cycle(div_v0)},
        "chain_coefficients": [1, -2, 2, -4],
        "Gamma_PQ_boundary": encode_cycle(boundary), "four_box_target": encode_cycle(target), "boundary_residual": encode_cycle(residual),
        "diagonal_chain_boundaries": diagonal_results,
        "relative_chain_denominators": {"PQ": 4, "QP": 4, "PP": 2, "QQ": 2, "all_units_at_11": True},
        "biextension_input": {
            "R": list(map(str, r)), "P_plus_R": list(map(str, p_plus_r)), "Q_plus_R": list(map(str, q_plus_r)),
            "shifted_divisors": {"D_P_prime": "[P+R]-[R]", "D_Q_prime": "[Q+R]-[R]"},
            "supports_disjoint_from_O_P_Q": True,
            "one_motive": "[Z^2 -> G_P x_E G_Q], with G_j attached to O(D_j_prime) rigidified at O",
            "height_entries_computed": False
        },
        "Tate_projection_obstruction": {
            "alternating_tensor": [int(x) for x in alternating_tensor],
            "symmetric_projection": [int(x) for x in symmetric_projection], "Weil_value": int(weil_value),
            "conclusion": "The Weil contraction cannot be recovered from the symmetric quotient alone."
        },
        "claims": {
            "explicit_boundary_4_box_PQ": "proved by divisor calculation, with exact algebra reproduced here",
            "minimal_torsion_order_of_box_PQ": None,
            "full_Albanese_kernel_triviality": "not asserted",
            "closed_higher_Chow_class_from_Gamma_alone": False,
            "Kato_compatible_secondary_realization": "not constructed or proved",
            "canonical_global_scalar_s11": None,
            "archimedean_L_second_derivative_comparison": "not constructed or proved",
            "BSD_proved": False,
            "old_certificates_replayed": False
        }
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("attack07_result_local.json"))
    args = parser.parse_args()
    result = compute()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"genus": 3, "smooth_mod_11": True, "boundary_residual": result["boundary_residual"], "boundary_multiplier": 4, "s11": None, "Kato_comparison": "open", "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
