#!/usr/bin/env python3
"""Exact new norm computations and localization bookkeeping for Attack 08.

Python 3.9+, standard library only. Does not replay Attack 07's certificate.
Polynomial coefficients ascend in x. Function-field arithmetic uses
y^2+y=x^3+x^2-2x, and identities are checked by cross multiplication.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def padd(a, b):
    c = [0] * max(len(a), len(b))
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] += v
    return trim(c)


def pscale(a, c):
    return trim([c*v for v in a])


def psub(a, b):
    return padd(a, pscale(b, -1))


def pmul(a, b):
    c = [0] * (len(a)+len(b)-1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i+j] += u*v
    return trim(c)


def ppow(a, n):
    out = [1]
    for _ in range(n):
        out = pmul(out, a)
    return out


def check(actual, expected, label):
    if actual != expected:
        raise ArithmeticError(f"{label}: {actual!r} != {expected!r}")


Q = [0, -2, 1, 1]
ZERO = ([0], [0])
ONE = ([1], [0])


def radd(a, b):
    return padd(a[0], b[0]), padd(a[1], b[1])


def rneg(a):
    return pscale(a[0], -1), pscale(a[1], -1)


def rsub(a, b):
    return radd(a, rneg(b))


def rmul(a, b):
    bd = pmul(a[1], b[1])
    return padd(pmul(a[0], b[0]), pmul(bd, Q)), psub(padd(pmul(a[0], b[1]), pmul(a[1], b[0])), bd)


def rpow(a, n):
    out = ONE
    for _ in range(n):
        out = rmul(out, a)
    return out


def ring(a):
    if isinstance(a, int):
        return ([a], [0])
    return a


class FF:
    def __init__(self, numerator, denominator=ONE):
        self.n = ring(numerator)
        self.d = ring(denominator)
        if self.d == ZERO:
            raise ZeroDivisionError

    def __mul__(self, other):
        if not isinstance(other, FF):
            other = FF(other)
        return FF(rmul(self.n, other.n), rmul(self.d, other.d))

    def __truediv__(self, other):
        if not isinstance(other, FF):
            other = FF(other)
        return FF(rmul(self.n, other.d), rmul(self.d, other.n))

    def __pow__(self, n):
        if n < 0:
            return FF(rpow(self.d, -n), rpow(self.n, -n))
        return FF(rpow(self.n, n), rpow(self.d, n))

    def residual(self, other):
        if not isinstance(other, FF):
            other = FF(other)
        return rsub(rmul(self.n, other.d), rmul(other.n, self.d))


def norm_linear(a, b, trace, product):
    """Norm(a+b*z) for z with z+z'=trace and z*z'=product."""
    return padd(padd(ppow(a, 2), pmul(pmul(a, b), trace)), pmul(ppow(b, 2), product))


def divisor_sum(*terms):
    out = {}
    for k, div in terms:
        for point, n in div.items():
            out[point] = out.get(point, 0)+k*n
    return {point: n for point, n in out.items() if n}


def compute():
    # A07's curve is the off-diagonal ordered pair of roots of
    # X^3+X^2-2X-y^2-y. This turn computes new norms along its maps.
    trace = [-1, -1]
    product = [-2, 1, 1]
    norm_p1 = norm_linear([-3, 2], [3], trace, product)
    norm_p2 = norm_linear([-3, 3], [2], trace, product)
    # Under addition the output x is the third root; g=2*x1+3*x2-3
    # becomes 2*trace+x2-3.
    norm_add = norm_linear([-5, -2], [1], trace, product)
    check(norm_p1, [0, 0, 7], "norm along first projection")
    check(norm_p2, [7, -14, 7], "norm along second projection")
    check(norm_add, [28, 28, 7], "norm along addition")

    x = ([0, 1], [0])
    y = ([0], [1])
    xm1 = ([-1, 1], [0])
    xp2 = ([2, 1], [0])
    # Exact translations on E, reduced with the Weierstrass equation.
    translation_a_num = ([-2, 1, 1], [-1])
    translation_b_num = ([1, -2, -1], [1])
    raw_a_num = rsub(rpow(y, 2), rmul(xp2, rpow(xm1, 2)))
    raw_b_num = rsub(rpow(radd(y, ONE), 2), rmul(xp2, rpow(x, 2)))
    check(raw_a_num, translation_a_num, "x(T+Q) numerator")
    check(raw_b_num, translation_b_num, "x(T-P)-1 numerator")
    aa = FF(translation_a_num, rpow(xm1, 2))
    bb = FF(translation_b_num, rpow(x, 2))
    ratio_target = FF(rneg(rmul(xp2, rpow(xm1, 2))), rpow(y, 2))
    ratio_residual = (bb/aa).residual(ratio_target)
    check(ratio_residual, ZERO, "translation ratio, including its minus sign")

    miller = FF(xp2, y)
    full_addition_push = FF((norm_add, [0]))*(aa**-2)*(bb**2)*(FF(xm1)**-4)
    target_addition_push = FF(7)*(miller**4)
    push_residual = full_addition_push.residual(target_addition_push)
    check(push_residual, ZERO, "complete addition pushforward")
    p1_push = FF((norm_p1, [0]))*(FF(x)**-2)
    p2_push = FF((norm_p2, [0]))*(FF(xm1)**2)*(FF(xm1)**-4)
    check(p1_push.residual(7), ZERO, "complete first projection pushforward")
    check(p2_push.residual(7), ZERO, "complete second projection pushforward")

    # m_*Z_PQ=[P+Q]-[P]-[Q]+[O]. The Miller function has that divisor.
    div_xp2 = {"P+Q": 1, "-P-Q": 1, "O": -2}
    div_y = {"P": 1, "Q": 1, "-P-Q": 1, "O": -3}
    div_miller = divisor_sum((1, div_xp2), (-1, div_y))
    m_box = {"P+Q": 1, "P": -1, "Q": -1, "O": 1}
    check(div_miller, m_box, "Miller divisor")
    # Coordinate normalization subtracts two closed constant chains.
    normalized_addition_ratio = (target_addition_push/FF(49)).residual((miller**4)/FF(7))
    check(normalized_addition_ratio, ZERO, "normalized addition push is Miller^4/7")

    # A further closed correction survives both coordinate normalizations.
    # Theta_c=(Delta,c)-(E x O,c)-(O x E,c). On Delta, m=[2]
    # has degree 4, while each coordinate projection has degree 1.
    constant_push_degrees = {
        "diagonal": [1, 1, 4], "horizontal_axis": [1, 0, 1],
        "vertical_axis": [0, 1, 1]
    }
    theta_exponents = [
        constant_push_degrees["diagonal"][i]
        - constant_push_degrees["horizontal_axis"][i]
        - constant_push_degrees["vertical_axis"][i]
        for i in range(3)
    ]
    check(theta_exponents, [0, 0, 2], "Theta_c pushforward exponents")
    gamma0_constant_exponents = [Fraction(0), Fraction(0), Fraction(-1)]
    gamma1_constant_exponents = [
        old + Fraction(e, 2) for old, e in zip(gamma0_constant_exponents, theta_exponents)
    ]
    check(gamma1_constant_exponents, [0, 0, 0], "half Theta_7 removes 7 with coordinate norms fixed")

    # Localization suspension: div_{A1}(tau)=[0]; on G_m it is a unit.
    suspension_residues = {}
    for r in ("P", "Q"):
        residue = divisor_sum((1, {r: 1}), (-1, {"O": 1}))
        suspension_residues[r] = residue
        check(sum(residue.values()), 0, "degree-zero localization residue")
    return {
        "task": "BSD Proof Attack 08: norms, degree obstruction, and localization",
        "new_calculations_only": True,
        "norms_polynomials_ascending": {
            "projection_1": norm_p1, "projection_2": norm_p2, "addition": norm_add
        },
        "function_field": {"equation": "y^2+y=x^3+x^2-2*x", "representation": "a(x)+b(x)*y; cross-multiplied rational identities"},
        "translations": {
            "A=x(T+Q)": {"numerator": translation_a_num, "denominator": rpow(xm1, 2)},
            "B=x(T-P)-1": {"numerator": translation_b_num, "denominator": rpow(x, 2)},
            "B_over_A": "-(x+2)*(x-1)^2/y^2",
            "identity_residual": ratio_residual
        },
        "complete_pushforwards": {
            "pi1_Gamma": "7", "pi2_Gamma": "7", "m_Gamma": "7*((x+2)/y)^4",
            "m_identity_residual": push_residual,
            "Miller_divisor": div_miller,
            "geometric_constant": 7,
            "is_Kato_global_scalar": False
        },
        "coordinate_normalization": {
            "closed_correction": "(E x O,7)+(O x E,7)",
            "pi1_Gamma0": "1", "pi2_Gamma0": "1", "m_Gamma0": "((x+2)/y)^4/7",
            "interpretation": "The constant 7 moves under explicit closed-chain corrections."
        },
        "residual_closed_ambiguity": {
            "Theta_c": "(Delta,c)-(E x O,c)-(O x E,c)",
            "map_order": ["pi1", "pi2", "addition"],
            "map_degrees_on_support": constant_push_degrees,
            "Theta_c_push_exponents": theta_exponents,
            "rational_correction": "Gamma1=Gamma0+(1/2)*Theta_7",
            "Gamma1_pushes": ["1", "1", "((x+2)/y)^4"],
            "Gamma1_constant_7_exponents": [str(e) for e in gamma1_constant_exponents],
            "boundary": "4*Z_PQ, unchanged",
            "coefficient_convention": "Rational coefficients; pushforwards are in Q(E)^* tensor Q. No square root of 7 is adjoined."
        },
        "degrees": {
            "closed_input": "CH^2(E x E,1)=H_M^3(E x E,Q(2))",
            "direct_push_target": "CH^1(E,1)=H_M^1(E,Q(1))=Q^* tensor Q",
            "rational_point_target": "Pic^0(E)_Q subset CH^1(E,0)=H_M^2(E,Q(1))",
            "obstruction": "Ordinary algebraic correspondences preserve higher-Chow index; direct push lands one motivic cohomological degree too low after codimension adjustment."
        },
        "localization": {
            "space": "E x A^1_tau", "open": "E x G_m_tau",
            "class_P": "(P x G_m,tau)-(O x G_m,tau)",
            "class_Q": "(Q x G_m,tau)-(O x G_m,tau)",
            "residues": suspension_residues,
            "boundary_map": "CH^2(E x G_m,1) -> CH^1(E,0)",
            "formal_parameter_scaling": "tau -> c*tau leaves the residue unchanged; the difference is D x {c}",
            "is_Iwasawa_augmentation_parameter": False,
            "scope": "The code checks divisor bookkeeping. The localization theorem and regulator functoriality are mathematical input, cited in the manuscript."
        },
        "open": {
            "comparison_between_geometric_residue_and_cyclotomic_derivative": "not constructed",
            "rational_determinant_lift": "not proved",
            "s11": None,
            "complex_leading_term_comparison": "not proved",
            "BSD_proved": False,
            "canonical_frontier_updated": False
        }
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("attack08_result_local.json"))
    args = parser.parse_args()
    result = compute()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"norm_constant": 7, "addition_identity_residual": result["complete_pushforwards"]["m_identity_residual"], "localization_residues": result["localization"]["residues"], "Kato_comparison": "open", "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
