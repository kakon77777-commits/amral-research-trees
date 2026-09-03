"""Exact ERDOS-885 k=5 lift search over scaled public compact 4x6 packets.

For compact roots A (4) and B (6), the five positive integers
    N_j = c^2 (B_j^2 - B_0^2),  j=1..5,
have the four common factor differences 2c*A_i.  Every additional integer
common difference d corresponds exactly to the signed shift
    t = d^2 - (2c B_0)^2
which makes (2c B_j)^2+t square for all six j.  Enumerating factor pairs of
(2cB_1)^2-(2cB_0)^2 is therefore finite and complete, including negative t,
odd d, and d=0.
"""

from __future__ import annotations

import argparse
import math

from audit_public_4x6 import fetch_packets, is_square
from search_scaled_public_4x6 import all_divisors, merge_scaled_factors, small_factorization


def exact_signed_scaled_closure(
    right: tuple[int, ...], scale: int, base_factors: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int], ...], int]:
    roots = tuple(2 * scale * b for b in right)
    gap = roots[1] * roots[1] - roots[0] * roots[0]
    found: list[tuple[int, int]] = []
    factor_divisors = all_divisors(merge_scaled_factors(base_factors, scale))
    for u in factor_divisors:
        v = gap // u
        if u > v:
            break
        if (u ^ v) & 1:
            continue
        d = (v - u) // 2
        shift = d * d - roots[0] * roots[0]
        if all(is_square(root * root + shift) for root in roots[1:]):
            found.append((shift, d))
    return tuple(sorted(set(found))), len(factor_divisors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale-min", type=int, default=1)
    parser.add_argument("--scale-max", type=int, default=100)
    parser.add_argument("--packet-min", type=int, default=1)
    parser.add_argument("--packet-max", type=int, default=71)
    args = parser.parse_args()
    if not (1 <= args.scale_min <= args.scale_max):
        raise SystemExit("require 1 <= scale-min <= scale-max")
    if not (1 <= args.packet_min <= args.packet_max <= 71):
        raise SystemExit("require 1 <= packet-min <= packet-max <= 71")

    packets = fetch_packets()
    packet_multiplier_pairs = 0
    signed_candidates_tested = 0
    closure_entries = 0
    for packet_index in range(args.packet_min - 1, args.packet_max):
        left, right = packets[packet_index]
        a0 = left[0]
        # Base gap already includes the factor 4 from roots 2*B.
        base_gap = (2 * right[1]) ** 2 - (2 * right[0]) ** 2
        base_factors = small_factorization(base_gap)
        for scale in range(args.scale_min, args.scale_max + 1):
            packet_multiplier_pairs += 1
            closure, divisor_count = exact_signed_scaled_closure(right, scale, base_factors)
            # Number of tested factor-pair candidates is recorded conservatively
            # as the full divisor count; the actual parity/ordering sieve is lower.
            signed_candidates_tested += divisor_count
            closure_entries += len(closure)
            inherited_differences = {2 * scale * a for a in left}
            closure_differences = {d for _, d in closure}
            if not inherited_differences.issubset(closure_differences):
                raise AssertionError(
                    (packet_index + 1, scale, inherited_differences, closure)
                )
            new_differences = tuple(sorted(closure_differences - inherited_differences))
            if new_differences:
                rows = tuple(
                    scale * scale * (b * b - right[0] * right[0])
                    for b in right[1:]
                )
                differences = tuple(sorted(closure_differences))
                if not all(
                    is_square(d * d + 4 * n) for n in rows for d in differences
                ):
                    raise AssertionError((packet_index + 1, scale, rows, differences))
                print("STATUS=FOUND_ERDOS885_K5")
                print(f"SOURCE_PACKET_INDEX={packet_index + 1}")
                print(f"SCALE={scale}")
                print(f"ROWS={rows}")
                print(f"COMMON_DIFFERENCES={differences}")
                print(f"NEW_DIFFERENCES={new_differences}")
                return
        print(
            f"PROGRESS packet={packet_index + 1} scale_max={args.scale_max} "
            f"pairs={packet_multiplier_pairs}"
        )

    print("STATUS=NO_SIGNED_SCALAR_INDUCED_ERDOS885_K5_IN_RANGE")
    print(f"packet_range=[{args.packet_min},{args.packet_max}]")
    print(f"scale_range=[{args.scale_min},{args.scale_max}]")
    print(f"packet_multiplier_pairs={packet_multiplier_pairs}")
    print(f"factor_divisors_enumerated={signed_candidates_tested}")
    print(f"signed_closure_entries={closure_entries}")
    print(f"expected_inherited_entries={4 * packet_multiplier_pairs}")


if __name__ == "__main__":
    main()
