#!/usr/bin/env python3
"""Produce a NEW ordinary cyclotomic distribution from the accepted eigenline.

Python 3.9+, standard library only. This does not revalidate the inherited
Hecke eigenspace or the canonical-period comparison. See BSD_Proof_Attack_04_Mu_Zero_Descent.md.
"""

import argparse
import hashlib
import json
from math import comb, gcd
from pathlib import Path


def projective(c, d, level):
    c, d = c % level, d % level
    if c == d == 0:
        raise ValueError("Farey edge has zero projective row")
    return d * pow(c, -1, level) % level if c else level


def symbol(a, b, vector, level, p):
    """Evaluate {infinity,a/b} by the inherited balanced Farey convention."""
    if b == 0:
        return 0
    if b < 0:
        a, b = -a, -b
    common = gcd(a, b)
    a, b = a // common, b // common
    a %= b
    value = vector[projective(1, 0, level)]
    while b > 1:
        inverse = pow(a, -1, b)
        sign, denominator = (1, inverse) if 2 * inverse <= b else (-1, b - inverse)
        numerator = (a * denominator - sign) // b
        if a * denominator - b * numerator != sign:
            raise ArithmeticError("Non-unimodular Farey edge")
        value += vector[projective(sign * b, denominator, level)]
        a, b = numerator % denominator, denominator
    return value % p


def produce(input_path):
    raw = input_path.read_bytes()
    data = json.loads(raw)
    p, level = data["p"], data["level"]
    vector = data["eigenvector"]
    if len(vector) != level + 1 or any(not 0 <= x < p for x in vector):
        raise ValueError("Input is not a projective-line vector over F_p")
    alpha = data["a_p"] % p
    if not alpha:
        raise ValueError("This producer requires good ordinary reduction")
    modulus = p * p
    inverse_alpha_2 = pow(alpha, -2, p)
    inverse_alpha_3 = pow(alpha, -3, p)
    coefficients = [0] * p
    terms = []
    for a in range(1, modulus):
        if a % p == 0:
            continue
        teich = pow(a, p, modulus)
        gamma_part = a * pow(teich, -1, modulus) % modulus
        if gamma_part % p != 1:
            raise ArithmeticError("Teichmuller projection did not land in 1+pZ")
        j = (gamma_part - 1) // p
        value_p2 = symbol(a, modulus, vector, level, p)
        value_p = symbol(a, p, vector, level, p)
        mass = (inverse_alpha_2 * value_p2 - inverse_alpha_3 * value_p) % p
        coefficients[j] = (coefficients[j] + mass) % p
        terms.append({"a": a, "gamma_exponent": j, "symbol_p2": value_p2,
                      "symbol_p": value_p, "mass": mass})
    t_coefficients = [
        sum(coefficients[j] * comb(j, i) for j in range(i, p)) % p
        for i in range(p)
    ]
    first_nonzero = next((i for i, a in enumerate(t_coefficients) if a), None)
    return {
        "curve": data["curve"], "p": p, "level": level,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "accepted_input": "Hecke eigenline and p-unit canonical-period comparison",
        "new_computation": "ordinary measure modulo (p,(1+t)^p-1)",
        "generator": "gamma=1+p, t=gamma-1; pushforward through Teichmuller quotient",
        "alpha_mod_p": alpha,
        "inverse_alpha_squared_mod_p": inverse_alpha_2,
        "inverse_alpha_cubed_mod_p": inverse_alpha_3,
        "group_basis_coefficients": coefficients,
        "t_basis_coefficients": t_coefficients,
        "summand_count": len(terms),
        "mu": 0 if first_nonzero is not None else None,
        "lambda": first_nonzero,
        "invariant_scope": "primitive ordinary p-adic L-function; conditional on accepted input",
        "canonical_leading_coefficient": "not determined; fixed-scale coefficient times an unknown F_p unit",
        "complex_analytic_rank": "not determined by this computation",
        "summands": terms,
    }


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=here / "eigenline_input.json")
    parser.add_argument("--output", type=Path, default=here / "cyclotomic_result.json")
    args = parser.parse_args()
    result = produce(args.input)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "summand_count", "group_basis_coefficients", "t_basis_coefficients", "mu", "lambda"
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
