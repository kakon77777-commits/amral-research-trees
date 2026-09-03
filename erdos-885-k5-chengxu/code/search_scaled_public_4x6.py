"""Search scalar-induced closure jumps in the 71 public compact 4x6 packets.

Scaling compact roots by c can add new divisor factorizations even though the
old shifts merely scale by c^2.  A new shift supported by all six roots gives
the normalized 6x5 square-sum packet equivalent to ERDOS-885 k=5.  Support on
exactly five roots gives the adjacent (still open) 5x5 square-sum problem, not
ERDOS-885 itself.
"""

from __future__ import annotations

import argparse
import math
from functools import lru_cache

from sympy import factorint

from audit_public_4x6 import fetch_packets, is_square


@lru_cache(maxsize=None)
def small_factorization(n: int) -> tuple[tuple[int, int], ...]:
    return tuple(sorted((int(p), int(e)) for p, e in factorint(n).items()))


def merge_scaled_factors(
    base: tuple[tuple[int, int], ...], scale: int
) -> tuple[tuple[int, int], ...]:
    factors = dict(base)
    for p, e in small_factorization(scale):
        factors[p] = factors.get(p, 0) + 2 * e
    return tuple(sorted(factors.items()))


def all_divisors(factors: tuple[tuple[int, int], ...]) -> list[int]:
    result = [1]
    for p, exponent in factors:
        old = tuple(result)
        power = 1
        for _ in range(exponent):
            power *= p
            result.extend(d * power for d in old)
    result.sort()
    return result


def scaled_pair_shift_candidates(
    y0: int,
    y1: int,
    scale: int,
    base_factors: tuple[tuple[int, int], ...],
) -> set[int]:
    cy0 = scale * y0
    gap = scale * scale * (y1 * y1 - y0 * y0)
    found: set[int] = set()
    for u in all_divisors(merge_scaled_factors(base_factors, scale)):
        v = gap // u
        if u >= v:
            break
        if (u ^ v) & 1:
            continue
        x0 = (v - u) // 2
        if x0 > cy0:
            found.add(x0 * x0 - cy0 * cy0)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale-min", type=int, default=2)
    parser.add_argument("--scale-max", type=int, default=100)
    parser.add_argument("--packet-min", type=int, default=1)
    parser.add_argument("--packet-max", type=int, default=71)
    parser.add_argument("--min-support", type=int, choices=(5, 6), default=5)
    args = parser.parse_args()
    if not (2 <= args.scale_min <= args.scale_max):
        raise SystemExit("require 2 <= scale-min <= scale-max")
    if not (1 <= args.packet_min <= args.packet_max <= 71):
        raise SystemExit("require 1 <= packet-min <= packet-max <= 71")

    packets = fetch_packets()
    multipliers = 0
    candidate_shifts = 0
    support_at_least_five = 0
    support_all_six = 0
    best_new_support = 0
    best_new = None
    for packet_index in range(args.packet_min - 1, args.packet_max):
        left, right = packets[packet_index]
        a0 = left[0]
        # If all six roots are required, every candidate contains roots 0 and 1.
        # If five suffice, at most one of roots 0,1,2 can be absent, so all three
        # pair anchors are required for completeness.
        base_pairs = ((0, 1),) if args.min_support == 6 else ((0, 1), (0, 2), (1, 2))
        base_factorizations = {
            pair: small_factorization(right[pair[1]] ** 2 - right[pair[0]] ** 2)
            for pair in base_pairs
        }
        for scale in range(args.scale_min, args.scale_max + 1):
            multipliers += 1
            roots = tuple(scale * y for y in right)
            inherited = {
                scale * scale * (a * a - a0 * a0)
                for a in left[1:]
            }
            candidates: set[int] = set()
            for i, j in base_pairs:
                candidates |= scaled_pair_shift_candidates(
                    right[i], right[j], scale, base_factorizations[(i, j)]
                )
            candidate_shifts += len(candidates)
            for shift in candidates:
                support = tuple(i for i, y in enumerate(roots) if is_square(y * y + shift))
                if len(support) < args.min_support:
                    continue
                support_at_least_five += 1
                if len(support) == 6:
                    support_all_six += 1
                if shift in inherited:
                    continue
                if len(support) > best_new_support:
                    best_new_support = len(support)
                    best_new = (packet_index + 1, scale, roots, shift, support)
                    print(
                        f"RECORD_NEW_SUPPORT support={len(support)} packet={packet_index + 1} "
                        f"scale={scale} shift={shift} roots={roots} supported_indices={support}"
                    )
                shifts = tuple(sorted(inherited | {shift}))
                if len(support) == 6 and all(
                    is_square(y * y + t) for y in roots for t in shifts
                ):
                    print("STATUS=FOUND_ERDOS885_K5_NORMALIZED_6x5")
                    print(f"SOURCE_PACKET_INDEX={packet_index + 1}")
                    print(f"SCALE={scale}")
                    print(f"ROOTS={roots}")
                    print(f"POSITIVE_SHIFTS={shifts}")
                    return
                kept = tuple(roots[i] for i in support)
                if len(kept) == 5 and all(
                    is_square(y * y + t) for y in kept for t in shifts
                ):
                    print("STATUS=FOUND_5x5_SQUARE_SUM_INTERMEDIATE")
                    print(f"SOURCE_PACKET_INDEX={packet_index + 1}")
                    print(f"SCALE={scale}")
                    print(f"ROOTS={kept}")
                    print(f"POSITIVE_SHIFTS={shifts}")
                    return
        print(
            f"PROGRESS packet={packet_index + 1} scale_max={args.scale_max} "
            f"multipliers={multipliers}"
        )

    if args.min_support == 6:
        print("STATUS=NO_SCALAR_INDUCED_ERDOS885_K5_IN_RANGE")
    else:
        print("STATUS=NO_SCALAR_INDUCED_5x5_SQUARE_SUM_IN_RANGE")
    print(f"packet_range=[{args.packet_min},{args.packet_max}]")
    print(f"scale_range=[{args.scale_min},{args.scale_max}]")
    print(f"minimum_support={args.min_support}")
    print(f"packet_multiplier_pairs={multipliers}")
    print(f"candidate_shifts_tested={candidate_shifts}")
    print(f"shifts_with_support_at_least_five={support_at_least_five}")
    print(f"shifts_with_support_all_six={support_all_six}")
    print(f"best_new_support={best_new_support}")
    print(f"best_new_record={best_new}")


if __name__ == "__main__":
    main()
