"""Independent correctness checks for the I0 problem families."""

from __future__ import annotations

from itertools import product
from typing import Mapping, Sequence


def parity_oracle(bits: Sequence[int | bool], answer: int | bool) -> bool:
    expected = sum(int(bit) for bit in bits) & 1
    return int(answer) == expected


def assignment_satisfies_2sat(
    clauses: Sequence[tuple[int, int]], assignment: Mapping[int, bool]
) -> bool:
    def literal_value(literal: int) -> bool:
        value = bool(assignment[abs(literal)])
        return value if literal > 0 else not value

    return all(literal_value(left) or literal_value(right) for left, right in clauses)


def exhaustive_2sat(
    variable_count: int, clauses: Sequence[tuple[int, int]]
) -> dict[int, bool] | None:
    for values in product((False, True), repeat=variable_count):
        assignment = {index + 1: value for index, value in enumerate(values)}
        if assignment_satisfies_2sat(clauses, assignment):
            return assignment
    return None


def verify_implication_path(
    clauses: Sequence[tuple[int, int]], path: Sequence[int]
) -> bool:
    edges: set[tuple[int, int]] = set()
    for left, right in clauses:
        edges.add((-left, right))
        edges.add((-right, left))
    return bool(path) and all(edge in edges for edge in zip(path, path[1:]))


def verify_unsat_certificate(
    clauses: Sequence[tuple[int, int]],
    variable: int,
    positive_to_negative: Sequence[int],
    negative_to_positive: Sequence[int],
) -> bool:
    if variable <= 0:
        return False
    return (
        positive_to_negative[0] == variable
        and positive_to_negative[-1] == -variable
        and negative_to_positive[0] == -variable
        and negative_to_positive[-1] == variable
        and verify_implication_path(clauses, positive_to_negative)
        and verify_implication_path(clauses, negative_to_positive)
    )
