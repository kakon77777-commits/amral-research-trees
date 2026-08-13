"""Deterministic implication-graph + SCC baseline for 2-SAT."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .oracles import assignment_satisfies_2sat, verify_unsat_certificate


Clause = tuple[int, int]


@dataclass(frozen=True)
class TwoSatResult:
    status: str
    assignment: Mapping[int, bool] | None
    unsat_variable: int | None
    positive_to_negative: tuple[int, ...]
    negative_to_positive: tuple[int, ...]


def _node(literal: int) -> int:
    variable = abs(literal) - 1
    return 2 * variable + (0 if literal > 0 else 1)


def _literal(node: int) -> int:
    variable = node // 2 + 1
    return variable if node % 2 == 0 else -variable


def _validate(variable_count: int, clauses: Iterable[Clause]) -> tuple[Clause, ...]:
    if variable_count < 0:
        raise ValueError("variable_count must be non-negative")
    normalized = tuple((int(left), int(right)) for left, right in clauses)
    for left, right in normalized:
        if left == 0 or right == 0:
            raise ValueError("literal 0 is invalid")
        if abs(left) > variable_count or abs(right) > variable_count:
            raise ValueError("literal exceeds variable_count")
    return normalized


def _path(graph: Sequence[Sequence[int]], start: int, target: int) -> tuple[int, ...]:
    queue = deque([start])
    previous: dict[int, int | None] = {start: None}
    while queue:
        current = queue.popleft()
        if current == target:
            break
        for neighbor in graph[current]:
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    if target not in previous:
        raise RuntimeError("SCC certificate path was not reconstructible")
    nodes: list[int] = []
    cursor: int | None = target
    while cursor is not None:
        nodes.append(cursor)
        cursor = previous[cursor]
    nodes.reverse()
    return tuple(_literal(node) for node in nodes)


def solve_2sat(variable_count: int, clauses: Iterable[Clause]) -> TwoSatResult:
    normalized = _validate(variable_count, clauses)
    node_count = 2 * variable_count
    graph: list[list[int]] = [[] for _ in range(node_count)]
    reverse: list[list[int]] = [[] for _ in range(node_count)]

    def add_edge(source_literal: int, target_literal: int) -> None:
        source = _node(source_literal)
        target = _node(target_literal)
        graph[source].append(target)
        reverse[target].append(source)

    for left, right in normalized:
        add_edge(-left, right)
        add_edge(-right, left)

    visited = [False] * node_count
    order: list[int] = []

    def first_pass(start: int) -> None:
        stack: list[tuple[int, int]] = [(start, 0)]
        visited[start] = True
        while stack:
            node, edge_index = stack[-1]
            if edge_index < len(graph[node]):
                neighbor = graph[node][edge_index]
                stack[-1] = (node, edge_index + 1)
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append((neighbor, 0))
            else:
                order.append(node)
                stack.pop()

    for node in range(node_count):
        if not visited[node]:
            first_pass(node)

    component = [-1] * node_count
    component_id = 0
    for start in reversed(order):
        if component[start] != -1:
            continue
        component[start] = component_id
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in reverse[node]:
                if component[neighbor] == -1:
                    component[neighbor] = component_id
                    stack.append(neighbor)
        component_id += 1

    for variable in range(1, variable_count + 1):
        positive = _node(variable)
        negative = _node(-variable)
        if component[positive] == component[negative]:
            positive_to_negative = _path(graph, positive, negative)
            negative_to_positive = _path(graph, negative, positive)
            result = TwoSatResult(
                status="unsat",
                assignment=None,
                unsat_variable=variable,
                positive_to_negative=positive_to_negative,
                negative_to_positive=negative_to_positive,
            )
            if not verify_unsat_certificate(
                normalized,
                variable,
                positive_to_negative,
                negative_to_positive,
            ):
                raise RuntimeError("internal UNSAT certificate verification failed")
            return result

    assignment = {
        variable: component[_node(variable)] > component[_node(-variable)]
        for variable in range(1, variable_count + 1)
    }
    if not assignment_satisfies_2sat(normalized, assignment):
        raise RuntimeError("internal SAT assignment verification failed")
    return TwoSatResult(
        status="sat",
        assignment=assignment,
        unsat_variable=None,
        positive_to_negative=(),
        negative_to_positive=(),
    )
