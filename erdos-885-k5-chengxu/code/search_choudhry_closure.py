"""Exact closure search in Choudhry's seven-parameter (5,3) family.

For every generated five-root/three-shift square sumset, translate the least
shift to zero and enumerate *all* positive shifts compatible with the five
roots.  Enumeration is finite: for the two smallest roots y0 < y1, any added
shift gives X1^2-X0^2 = y1^2-y0^2, hence a factor pair of that fixed integer.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
from functools import lru_cache

from sympy import divisors


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def euler_entries(p: int, q: int, r: int, s: int) -> tuple[int, ...]:
    """Unsigned roots of the nine squared entries, in row-major order."""
    return (
        p * p + q * q - r * r - s * s,
        2 * q * r + 2 * p * s,
        2 * q * s - 2 * p * r,
        2 * q * r - 2 * p * s,
        p * p - q * q + r * r - s * s,
        2 * p * q + 2 * r * s,
        2 * q * s + 2 * p * r,
        2 * r * s - 2 * p * q,
        p * p - q * q - r * r + s * s,
    )


def generated_packet(params: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    f, g, m, u1, u2, v1, v2 = params
    e = g * m * v1 * v2
    h = f * m * u1 * u2
    p1, p2 = e * u1 + f * u2, e * u1 - f * u2
    q1, q2 = e * u2 + f * u1, e * u2 - f * u1
    r1, r2 = g * v1 + h * v2, g * v1 - h * v2
    s1, s2 = g * v2 + h * v1, g * v2 - h * v1
    E = euler_entries(p1, q1, r1, s1)
    F = euler_entries(p2, q2, r2, s2)

    # Lemma 2 / Theorem 2: a1=e13^2, a2=e31^2, a3=e22^2,
    # a4=f13^2, a5=f31^2; b2=e21^2-e13^2, b3=e11^2-e22^2.
    A = (E[2] ** 2, E[6] ** 2, E[4] ** 2, F[2] ** 2, F[6] ** 2)
    B = (0, E[3] ** 2 - E[2] ** 2, E[0] ** 2 - E[4] ** 2)
    if len(set(A)) != 5 or len(set(B)) != 3:
        return None
    if any(not is_square(a + b) for a in A for b in B):
        raise AssertionError((params, A, B))

    b0 = min(B)
    roots = tuple(sorted(math.isqrt(a + b0) for a in A))
    shifts = tuple(sorted(b - b0 for b in B))
    if roots[0] <= 0 or len(set(roots)) != 5 or shifts[0] != 0:
        return None
    return roots, shifts


@lru_cache(maxsize=None)
def exact_positive_shift_closure(roots: tuple[int, ...]) -> tuple[int, ...]:
    y0, y1 = roots[:2]
    gap = y1 * y1 - y0 * y0
    found: list[int] = []
    for a in divisors(gap):
        b = gap // a
        if a >= b or (a ^ b) & 1:
            continue
        x0 = (b - a) // 2
        if x0 <= y0:
            continue
        shift = x0 * x0 - y0 * y0
        if all(is_square(y * y + shift) for y in roots):
            found.append(shift)
    return tuple(sorted(set(found)))


def primitive_key(roots: tuple[int, ...], shifts: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    # Exact coordinates are the conservative deduplication key.  We avoid
    # quotienting by scale here so no arithmetic class is accidentally merged.
    return roots, shifts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=4)
    parser.add_argument("--signed", action="store_true")
    args = parser.parse_args()
    values = tuple(range(-args.bound, args.bound + 1)) if args.signed else tuple(range(1, args.bound + 1))
    if args.signed:
        values = tuple(x for x in values if x)

    total = valid = unique = 0
    best = -1
    seen: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    records: list[tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]] = []
    for params in itertools.product(values, repeat=7):
        total += 1
        packet = generated_packet(params)
        if packet is None:
            continue
        valid += 1
        roots, base_shifts = packet
        key = primitive_key(roots, base_shifts)
        if key in seen:
            continue
        seen.add(key)
        unique += 1
        closure = exact_positive_shift_closure(roots)
        if not set(base_shifts[1:]).issubset(closure):
            raise AssertionError((params, roots, base_shifts, closure))
        if len(closure) > best:
            best = len(closure)
            print(f"RECORD closure={best} params={params}")
            print(f"ROOTS={roots}")
            print(f"BASE_SHIFTS={base_shifts}")
            print(f"EXACT_POSITIVE_SHIFT_CLOSURE={closure}")
        if len(closure) >= 3:
            records.append((len(closure), params, roots, base_shifts, closure))
        if len(closure) >= 4:
            print("STATUS=FOUND_5x5_CANDIDATE")
            return

    digest = hashlib.sha256(repr(sorted(seen)).encode()).hexdigest()
    print("STATUS=NO_5x5_CANDIDATE_IN_PARAMETER_BOX")
    print(f"bound={args.bound} signed={args.signed}")
    print(f"total_parameter_tuples={total}")
    print(f"valid_packets={valid}")
    print(f"unique_exact_packets={unique}")
    print(f"best_positive_shift_closure={best}")
    print(f"packets_with_at_least_3_positive_shifts={len(records)}")
    print(f"exact_packet_digest_sha256={digest}")
    for record in sorted(records, reverse=True)[:20]:
        print(f"NEAR={record}")


if __name__ == "__main__":
    main()
