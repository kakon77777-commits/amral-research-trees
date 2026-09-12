#!/usr/bin/env python3
"""Exact new algebra for BSD Attack 06; Python 3.9+, standard library only.

This computes local-factor cancellation and polynomial identities.
It does not compute the canonical global scalar or prove the motivic bridge.
"""

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


class Quadratic:
    """Q[A]/(A^2 + 4*A + 11), stored as constant + linear*A."""

    def __init__(self, constant=0, linear=0):
        self.constant, self.linear = F(constant), F(linear)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Quadratic) else Quadratic(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Quadratic(self.constant + other.constant, self.linear + other.linear)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.constant, -self.linear)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        a, b, c, d = self.constant, self.linear, other.constant, other.linear
        return Quadratic(a*c - 11*b*d, a*d + b*c - 4*b*d)

    __rmul__ = __mul__

    def inverse(self):
        a, b = self.constant, self.linear
        norm = a*a - 4*a*b + 11*b*b
        if not norm:
            raise ZeroDivisionError("Zero element in quadratic field")
        return Quadratic((a-4*b)/norm, -b/norm)

    def __truediv__(self, other):
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def as_json(self):
        return {"constant": str(self.constant), "coefficient_of_A": str(self.linear)}


VARIABLES = ("a", "b", "d", "c", "x", "y")
ZERO_EXP = (0,) * len(VARIABLES)


def constant(value):
    return {} if value == 0 else {ZERO_EXP: F(value)}


def variable(name):
    exp = list(ZERO_EXP)
    exp[VARIABLES.index(name)] = 1
    return {tuple(exp): F(1)}


def add(left, right):
    out = dict(left)
    for exp, value in right.items():
        out[exp] = out.get(exp, F(0)) + value
        if not out[exp]:
            del out[exp]
    return out


def scale(value, polynomial):
    return {exp: F(value)*coefficient for exp, coefficient in polynomial.items()
            if value*coefficient}


def subtract(left, right):
    return add(left, scale(-1, right))


def multiply(left, right):
    out = {}
    for exp1, value1 in left.items():
        for exp2, value2 in right.items():
            exp = tuple(x+y for x, y in zip(exp1, exp2))
            out[exp] = out.get(exp, F(0)) + value1*value2
    return {exp: value for exp, value in out.items() if value}


def power(polynomial, exponent):
    out = constant(1)
    for _ in range(exponent):
        out = multiply(out, polynomial)
    return out


def polynomial_json(polynomial):
    return [{"coefficient": str(value), "exponents": list(exp)}
            for exp, value in sorted(polynomial.items())]


def hensel_ordinary_root(digits):
    root, modulus = 7, 11
    for _ in range(1, digits):
        correction = (-(root*root + 4*root + 11)//modulus
                      * pow((2*root+4) % 11, -1, 11)) % 11
        root += correction*modulus
        modulus *= 11
    if (root*root + 4*root + 11) % modulus:
        raise ArithmeticError("Hensel lift failed")
    return root


def integral_residue(value, modulus):
    return value.numerator*pow(value.denominator, -1, modulus) % modulus


def produce():
    alpha = Quadratic(0, 1)
    beta = 11/alpha
    euler = (1 - 1/alpha)*(1 - 1/alpha)
    coleman_log = (1 - 1/alpha)/(1 - 1/beta)
    theta = coleman_log/11
    cancellation = euler/theta
    if cancellation.constant != 16 or cancellation.linear != 0:
        raise ArithmeticError("Local cancellation identity failed")

    a, b, d, c, x, y = (variable(name) for name in VARIABLES)
    hc11 = add(a, multiply(c, power(x, 2)))
    hc12 = add(b, multiply(c, multiply(x, y)))
    hc22 = add(d, multiply(c, power(y, 2)))
    original_vector = [subtract(multiply(d, x), multiply(b, y)),
                       subtract(multiply(a, y), multiply(b, x))]
    changed_vector = [subtract(multiply(hc22, x), multiply(hc12, y)),
                      subtract(multiply(hc11, y), multiply(hc12, x))]
    vector_residual = [subtract(new, old)
                       for new, old in zip(changed_vector, original_vector)]
    det_original = subtract(multiply(a, d), power(b, 2))
    det_changed = subtract(multiply(hc11, hc22), power(hc12, 2))
    contraction = add(multiply(x, original_vector[0]), multiply(y, original_vector[1]))
    det_residual = subtract(subtract(det_changed, det_original), multiply(c, contraction))
    if any(vector_residual) or det_residual:
        raise ArithmeticError("Symbolic rank-one update identity failed")

    # Formal exp(c*epsilon) * exp(-c*epsilon), through epsilon^4.
    plus, minus = [], []
    factorial = 1
    for n in range(5):
        if n:
            factorial *= n
        plus.append(scale(F(1, factorial), power(c, n)))
        minus.append(scale(F((-1)**n, factorial), power(c, n)))
    balanced = []
    for n in range(5):
        coefficient = {}
        for i in range(n+1):
            coefficient = add(coefficient, multiply(plus[i], minus[n-i]))
        balanced.append(coefficient)
    if balanced != [constant(1), {}, {}, {}, {}]:
        raise ArithmeticError("Balanced truncated character identity failed")

    digits = 8
    alpha_lift = hensel_ordinary_root(digits+2)
    modulus = 11**digits
    def evaluate(value):
        return integral_residue(value.constant + value.linear*alpha_lift, modulus)

    return {
        "package": "BSD Proof Attack 06",
        "arithmetic": "Exact rational and multivariate polynomial arithmetic",
        "quadratic_relation": "A^2+4*A+11=0; ordinary embedding A=7 mod 11",
        "euler_e11": euler.as_json(),
        "coleman_log_c_alpha": coleman_log.as_json(),
        "theta_c_alpha_over_11": theta.as_json(),
        "e11_over_theta_exact": cancellation.as_json(),
        "local_multiplier": 16,
        "ordinary_residues": {
            "modulus": modulus,
            "alpha": alpha_lift % modulus,
            "e11": evaluate(euler),
            "theta": evaluate(theta),
            "e11_mod11": evaluate(euler) % 11,
            "theta_mod11": evaluate(theta) % 11,
        },
        "symbolic_variables": list(VARIABLES),
        "adjugate_rank_one_update_residual": [polynomial_json(p) for p in vector_residual],
        "determinant_rank_one_update_residual": polynomial_json(det_residual),
        "balanced_character_product_coefficients_through_epsilon4": [polynomial_json(p) for p in balanced],
        "normalized_first_jet_Sen_matrix": [[0, 1], [0, 0]],
        "Sen_matrix_characteristic_polynomial": "X^2",
        "Sen_matrix_minimal_polynomial": "X^2",
        "canonical_global_scalar_s11": None,
        "motivic_bridge_BD6": "Not constructed or proved",
        "scope": "Local algebra only. The Hodge-Tate inference uses the cited Sen theorem; no global proof is machine-verified here."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent / "attack06_result.json")
    args = parser.parse_args()
    result = produce()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({
        "local_multiplier": result["local_multiplier"],
        "e11_mod11": result["ordinary_residues"]["e11_mod11"],
        "theta_mod11": result["ordinary_residues"]["theta_mod11"],
        "adjugate_residual": result["adjugate_rank_one_update_residual"],
        "determinant_residual": result["determinant_rank_one_update_residual"],
        "canonical_global_scalar_s11": None,
        "motivic_bridge_BD6": result["motivic_bridge_BD6"],
    }, indent=2))


if __name__ == "__main__":
    main()
