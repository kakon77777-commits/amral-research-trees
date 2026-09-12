#!/usr/bin/env python3
"""New exact local-log calculation for E389a1 at 11; standard library only.

The formal logarithm satisfies log_omega(t) = t mod 11^2 on 11 Z_11.
Since #E(F_11)=16, log_omega(R)/11 = t([16]R)/(16*11) mod 11.
This program computes those formal parameters with rational arithmetic.
It does not compute a p-adic height matrix or prove a global theorem.
"""

import argparse
import json
from fractions import Fraction
from pathlib import Path


def add(left, right):
    if left is None:
        return right
    if right is None:
        return left
    x, y = left
    u, v = right
    if x == u and y + v + 1 == 0:
        return None
    slope = ((3*x*x + 2*x - 2) / (2*y + 1)
             if left == right else (v-y)/(u-x))
    intercept = y - slope*x
    new_x = slope*slope - 1 - x - u
    return new_x, -slope*new_x - intercept - 1


def multiply(n, point):
    result = None
    while n:
        if n & 1:
            result = add(result, point)
        n //= 2
        if n:
            point = add(point, point)
    return result


def valuation_integer(n, p):
    if n == 0:
        raise ValueError("The zero integer has no finite valuation")
    order = 0
    while n % p == 0:
        order += 1
        n //= p
    return order


def residue(value, modulus):
    return value.numerator * pow(value.denominator, -1, modulus) % modulus


def produce():
    p = 11
    result = {
        "curve": "389a1",
        "equation": "y^2+y=x^3+x^2-2*x",
        "differential": "omega=dx/(2*y+1)",
        "p": p,
        "accepted_reduction_group_order": 16,
        "method": "Exact rational multiplication; formal logarithm modulo p^2",
        "points": {},
    }
    for name, coordinates in [("P", (0, 0)), ("Q", (1, 0))]:
        point = tuple(Fraction(a) for a in coordinates)
        multiple = multiply(16, point)
        if multiple is None:
            raise ArithmeticError("Unexpected torsion point")
        x, y = multiple
        if y*y+y != x*x*x+x*x-2*x:
            raise ArithmeticError("Computed multiple is not on the given curve")
        formal_t = -x/y
        order = (valuation_integer(formal_t.numerator, p)
                 - valuation_integer(formal_t.denominator, p))
        if order < 1:
            raise ArithmeticError("The multiple is not in the formal group")
        result["points"][name] = {
            "input": list(coordinates),
            "point16": [str(x), str(y)],
            "formal_t_exact": str(formal_t),
            "formal_t_mod121": residue(formal_t, p*p),
            "v11_formal_t": order,
            "log_over_11_mod11": residue(formal_t/(16*p), p),
        }
    values = [result["points"][name]["log_over_11_mod11"] for name in ("P", "Q")]
    result["normalized_log_vector_mod11"] = values
    result["normalized_log_is_surjective"] = any(values)
    result["height_matrix"] = "Not computed; see proof for determinant nonvanishing"
    result["global_torsion"] = "Not inferred by code; proved using Selmer triangles in the manuscript"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent / "local_log_result.json")
    args = parser.parse_args()
    result = produce()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"formal_t_mod121": {
        name: item["formal_t_mod121"] for name, item in result["points"].items()},
        "normalized_log_vector_mod11": result["normalized_log_vector_mod11"],
        "normalized_log_is_surjective": result["normalized_log_is_surjective"]}, indent=2))


if __name__ == "__main__":
    main()
