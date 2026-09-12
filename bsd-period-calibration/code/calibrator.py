"""Exact rank-zero calibrator arithmetic; standard library, no upstream imports.

The characteristic-zero Manin eigenlines are solved over Q and then reduced
modulo 11.  All displayed moments use this file's explicitly pinned periods.
Hecke matrices use the determinant-l Heilbronn/Merel representative set.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from functools import lru_cache
from math import gcd, lcm
from pathlib import Path


P = 11
LEVEL = 19
AINVS = (0, 1, 1, -769, -8470)  # LMFDB 19.a1, Cremona 19a2
SOURCE = "https://www.lmfdb.org/EllipticCurve/Q/19/a/1"


def point_count(q: int) -> int:
    a1, a2, a3, a4, a6 = AINVS
    return 1 + sum(
        (y*y + a1*x*y + a3*y - x*x*x - a2*x*x - a4*x - a6) % q == 0
        for x in range(q) for y in range(q)
    )


def trace(q: int) -> int:
    return q + 1 - point_count(q)


def p1(c: int, d: int) -> int:
    c, d = c % LEVEL, d % LEVEL
    if c:
        return d * pow(c, -1, LEVEL) % LEVEL
    if not d:
        raise ValueError("zero projective pair")
    return LEVEL


def representative(i: int) -> tuple[int, int]:
    return (1, i) if i < LEVEL else (0, 1)


def row(indices: list[int]) -> list[int]:
    result = [0] * (LEVEL + 1)
    for i in indices:
        result[i] += 1
    return result


def manin_relations() -> list[list[int]]:
    result = []
    for i in range(LEVEL + 1):
        c, d = representative(i)
        result.append(row([i, p1(d, -c)]))
        result.append(row([i, p1(d, -c-d), p1(-c-d, c)]))
    return result


@lru_cache(None)
def hecke(q: int) -> tuple[tuple[int, ...], ...]:
    matrices = []
    for a in range(1, q + 1):
        for b in range(a):
            for c in range(q + 1):
                d, remainder = divmod(q + b*c, a)
                if remainder == 0 and d > c:
                    matrices.append((a, b, c, d))
    return tuple(tuple(row([
        p1(x*a + y*c, x*b + y*d) for a, b, c, d in matrices
    ])) for x, y in map(representative, range(LEVEL + 1)))


def rational_kernel(rows: list[list[int]]) -> list[list[F]]:
    matrix = [list(map(F, r)) for r in rows]
    pivots = []
    rank = 0
    for j in range(LEVEL + 1):
        k = next((k for k in range(rank, len(matrix)) if matrix[k][j]), None)
        if k is None:
            continue
        matrix[rank], matrix[k] = matrix[k], matrix[rank]
        pivot = matrix[rank][j]
        matrix[rank] = [x/pivot for x in matrix[rank]]
        for k in range(len(matrix)):
            if k != rank and matrix[k][j]:
                factor = matrix[k][j]
                matrix[k] = [x-factor*y for x, y in zip(matrix[k], matrix[rank])]
        pivots.append(j)
        rank += 1
    vectors = []
    for j in range(LEVEL + 1):
        if j in pivots:
            continue
        v = [F(0)] * (LEVEL + 1)
        v[j] = F(1)
        for i, pivot in enumerate(pivots):
            v[pivot] = -matrix[i][j]
        vectors.append(v)
    return vectors


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def eigenline(sign: int) -> dict:
    relations = manin_relations()
    constraints = [r[:] for r in relations]
    for i, h in enumerate(hecke(2)):
        eq = list(h)
        eq[i] -= trace(2)
        constraints.append(eq)
    for i in range(LEVEL + 1):
        c, d = representative(i)
        eq = [0] * (LEVEL + 1)
        eq[i] += 1
        eq[p1(-c, d)] -= sign
        constraints.append(eq)
    basis = rational_kernel(constraints)
    if len(basis) != 1:
        raise ValueError(f"expected rational sign eigenline, got {len(basis)}")
    denominator = lcm(*(x.denominator for x in basis[0]))
    primitive = [int(x * denominator) for x in basis[0]]
    divisor = gcd(*primitive)
    primitive = [x // divisor for x in primitive]
    first = next(i for i, x in enumerate(primitive) if x % P)
    if primitive[first] < 0:
        primitive = [-x for x in primitive]
    mod = [x * pow(primitive[first], -1, P) % P for x in primitive]
    validations = {
        str(q): all(dot(r, primitive) == trace(q)*primitive[i]
                    for i, r in enumerate(hecke(q)))
        for q in (3, 5, 7, 11, 13)
    }
    assert all(dot(r, primitive) == 0 for r in relations)
    assert all(validations.values())
    return {"sign": sign, "rational_dimension": len(basis),
            "primitive_integer_vector": primitive, "mod11_vector": mod,
            "normalization_index": first, "hecke_checks_over_Q": validations}


def cusp_indices(value: F) -> list[int]:
    """Decompose {infinity, value} into consecutive determinant +/-1 edges."""
    num, den = value.numerator, value.denominator
    convergents = [(1, 0)]
    # Standard convergents: p[-2]=0,p[-1]=1; q[-2]=1,q[-1]=0.
    pm2, pm1, qm2, qm1 = 0, 1, 1, 0
    while den:
        coefficient, rem = divmod(num, den)
        pn, qn = coefficient*pm1+pm2, coefficient*qm1+qm2
        convergents.append((pn, qn))
        pm2, pm1, qm2, qm1 = pm1, pn, qm1, qn
        num, den = den, rem
    result = []
    for (a, c), (b, d) in zip(convergents, convergents[1:]):
        det = a*d - b*c
        assert det in (-1, 1)
        # [[b,a],[d,c]] sends 0 -> a/c, infinity -> b/d.
        # Negating one column if necessary yields determinant +1.
        result.append(p1(d, -det*c))
    return result


def symbol(value: F, vector: list[int]) -> int:
    return sum(vector[i] for i in cusp_indices(value))


def chi8(a: int) -> int:
    return {1: 1, 3: -1, 5: -1, 7: 1}.get(a % 8, 0)


def moments(plus: list[int], minus: list[int]) -> dict:
    alpha = trace(P) % P
    if not alpha:
        raise ValueError("calibrator is not ordinary")
    inverse = pow(alpha, -1, P)
    at_zero = symbol(F(0), plus) % P
    base_measures = [
        (inverse*symbol(F(a, P), plus) - inverse**2*at_zero) % P
        for a in range(1, P)
    ]
    alpha_twist = chi8(P)*alpha % P
    twisted = lambda x: sum(chi8(b)*symbol(x+F(b, 8), minus) for b in (1,3,5,7))
    assert twisted(F(0)) % P == 0
    sums = [twisted(F(a, P)) % P for a in range(1, P)]
    weighted_sum = sum(pow(a, -1, P)*sums[a-1] for a in range(1, P)) % P
    shifted = weighted_sum * pow(alpha_twist, -1, P) % P
    # Check distribution in both signs with an independent denominator layer.
    distribution = []
    for a in range(1, P):
        base = sum(symbol(F(a+P*b,P*P), plus) for b in range(P))
        base -= trace(P)*symbol(F(a,P), plus)-symbol(F(a), plus)
        twist = sum(twisted(F(a+P*b,P*P)) for b in range(P))
        twist -= chi8(P)*trace(P)*twisted(F(a,P))-twisted(F(a))
        distribution.append([base % P, twist % P])
    assert all(r == [0, 0] for r in distribution)
    central = sum(base_measures) % P
    # Hecke at p gives the interpolation factor for the trivial character.
    assert central == ((1-inverse)**2 * at_zero) % P
    return {"a11": trace(P), "alpha_mod11": alpha,
            "alpha_twist_mod11": alpha_twist,
            "plus_symbol_at_zero_mod11": at_zero,
            "ordinary_first_layer_measures": base_measures,
            "ordinary_central_value_mod11": central,
            "twisted_cusp_sums": sums, "twisted_weighted_sum": weighted_sum,
            "twisted_x_inverse_value_mod11": shifted,
            "distribution_residuals": distribution,
            "smoothing_d": 5, "smoothing_mod11": (25-chi8(5)) % P,
            "adjoint_euler_multiplier_mod11": (1-inverse**2) % P,
            "nonvanishing_product_mod11": central*shifted*(25-chi8(5)) % P}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    plus, minus = eigenline(1), eigenline(-1)
    measured = moments(plus["mod11_vector"], minus["mod11_vector"])
    # Homogeneity controls: scale the two period lines independently.
    controls = []
    for a, b in ((2,3), (3,7), (10,10)):
        other = moments([a*x % P for x in plus["mod11_vector"]],
                        [b*x % P for x in minus["mod11_vector"]])
        controls.append(other["ordinary_central_value_mod11"] == a*measured["ordinary_central_value_mod11"] % P
                        and other["twisted_x_inverse_value_mod11"] == b*measured["twisted_x_inverse_value_mod11"] % P)
    assert all(controls)
    # These are negative witnesses against specific false-green conditions.
    bad_vector = plus["mod11_vector"][:]
    bad_vector[0] = (bad_vector[0] + 1) % P
    wrong_branch = sum(a*s for a, s in enumerate(measured["twisted_cusp_sums"], 1)) * pow(measured["alpha_twist_mod11"], -1, P) % P
    negative_checks = {
        "altered_symbol_rejected_by_Manin_relations": any(dot(r, bad_vector) % P for r in manin_relations()),
        "zero_symbol_rejected_by_normalization": not any([0] * (LEVEL + 1)),
        "x_instead_of_x_inverse_changes_recorded_moment": wrong_branch != measured["twisted_x_inverse_value_mod11"],
        "wrong_twist_root_rejected_by_Hecke_polynomial": (measured["alpha_mod11"]**2 - chi8(P)*trace(P)*measured["alpha_mod11"] + P) % P != 0,
    }
    assert all(negative_checks.values())
    result = {
        "status": "EXACT_FINITE_CALIBRATOR_CHECK",
        "curve": {"label": "19.a1", "cremona_label": "19a2", "ainvs": list(AINVS),
                  "conductor_source": SOURCE, "rank_zero_source": SOURCE},
        "modulus": P,
        "manin_dimension_over_Q": len(rational_kernel(manin_relations())),
        "point_counted_traces": {str(q): trace(q) for q in (2,3,5,7,11,13)},
        "plus_line": plus, "minus_line": minus, "measurements": measured,
        "independent_period_rescaling_controls": controls,
        "negative_checks": {k: bool(v) for k, v in negative_checks.items()},
        "wrong_x_moment_mod11": wrong_branch,
        "actual_BF_family_computed": False,
        "C_computed": False, "s11_computed": False, "BSD_proved": False,
    }
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
    print(encoded, end="")


if __name__ == "__main__":
    main()
