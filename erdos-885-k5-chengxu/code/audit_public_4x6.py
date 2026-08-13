"""Audit every public 2019 compact 4x6 square-sum packet for a 5x5 lift.

For compact root sets A (four roots) and B (six roots), the condition is
    a^2 + b^2 - a0^2 is square for every a in A and b in B,
where a0 is the shared least root.  Dropping one b leaves five roots.  We
enumerate every positive shift compatible with those five roots.  A fourth
positive shift, in addition to zero, would lift that subset to a 5x5 packet.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import math
import re
import subprocess
from functools import lru_cache

from sympy import divisors


URL = "https://www.thomas-egense.dk/math/constructing_magic_squares_of_squares_from_mols.html"


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


@lru_cache(maxsize=None)
def pair_shift_candidates(y0: int, y1: int) -> tuple[int, ...]:
    """All positive shifts taking both y0^2 and y1^2 to squares."""
    gap = y1 * y1 - y0 * y0
    found: list[int] = []
    for u in divisors(gap):
        v = gap // u
        if u >= v or (u ^ v) & 1:
            continue
        x0 = (v - u) // 2
        if x0 <= y0:
            continue
        found.append(x0 * x0 - y0 * y0)
    return tuple(sorted(set(found)))


def exact_positive_shift_closure(roots: tuple[int, ...]) -> tuple[int, ...]:
    roots = tuple(sorted(roots))
    return tuple(
        shift
        for shift in pair_shift_candidates(roots[0], roots[1])
        if all(is_square(y * y + shift) for y in roots[2:])
    )


def exact_positive_root_closure(shifts: tuple[int, ...]) -> tuple[int, ...]:
    """All positive roots compatible with zero and every positive shift."""
    shifts = tuple(sorted(shifts))
    gap = shifts[1] - shifts[0]
    found: set[int] = set()
    for u in divisors(gap):
        v = gap // u
        if u >= v or (u ^ v) & 1:
            continue
        first_shift_root = (v - u) // 2
        root_sq = first_shift_root * first_shift_root - shifts[0]
        if root_sq <= 0 or not is_square(root_sq):
            continue
        root = math.isqrt(root_sq)
        if all(is_square(root * root + shift) for shift in shifts):
            found.add(root)
    return tuple(sorted(found))


def exact_signed_shift_closure(roots: tuple[int, ...]) -> tuple[int, ...]:
    """All integer shifts (negative, zero, positive) square on every root.

    The equality case u=v is retained: it gives first shifted root zero and
    therefore covers the possible common factor difference d=0.
    """
    roots = tuple(sorted(roots))
    y0, y1 = roots[:2]
    gap = y1 * y1 - y0 * y0
    found: set[int] = set()
    for u in divisors(gap):
        v = gap // u
        if u > v or (u ^ v) & 1:
            continue
        x0 = (v - u) // 2
        shift = x0 * x0 - y0 * y0
        if all(is_square(y * y + shift) for y in roots):
            found.add(shift)
    return tuple(sorted(found))


def fetch_packets() -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    proc = subprocess.run(
        ["curl.exe", "-L", "-s", "-A", "Codex-Research", URL],
        check=True,
        capture_output=True,
    )
    html = proc.stdout.decode("utf-8", errors="replace")
    rows = re.findall(
        r"<tr><td>(\[[0-9, ]+\])</td><td>(\[[0-9, ]+\])</td><td>.*?</td></tr>",
        html,
        flags=re.DOTALL,
    )
    packets = []
    for left_text, right_text in rows:
        left = tuple(ast.literal_eval(left_text))
        right = tuple(ast.literal_eval(right_text))
        if len(left) == 4 and len(right) == 6:
            packets.append((left, right))
    if len(packets) != 71:
        raise AssertionError(f"expected 71 public packets, parsed {len(packets)}")
    return tuple(packets)


def main() -> None:
    packets = fetch_packets()
    best = -1
    best_records = []
    subset_closures = 0
    full_closed = 0
    reverse_closed = 0
    largest_reverse_closure = 0
    signed_factor_packets_closed = 0
    signed_five_subsets_checked = 0
    largest_signed_five_subset_closure = 0
    for index, (left, right) in enumerate(packets, start=1):
        if left[0] != right[0] or len(set(left)) != 4 or len(set(right)) != 6:
            raise AssertionError((index, left, right))
        a0 = left[0]
        if any(not is_square(a * a + b * b - a0 * a0) for a in left for b in right):
            raise AssertionError((index, left, right))
        expected = tuple(sorted(a * a - a0 * a0 for a in left[1:]))
        full_closure = exact_positive_shift_closure(right)
        if not set(expected).issubset(full_closure):
            raise AssertionError((index, expected, full_closure))
        if full_closure == expected:
            full_closed += 1
        reverse_closure = exact_positive_root_closure(expected)
        if not set(right).issubset(reverse_closure):
            raise AssertionError((index, right, reverse_closure))
        if reverse_closure == right:
            reverse_closed += 1
        largest_reverse_closure = max(largest_reverse_closure, len(reverse_closure))

        # In factor-difference coordinates the five rows are
        # right[j]^2-right[0]^2 (j>0), and existing differences are 2*left[i].
        # Searching signed shifts on 2*right covers every integer difference,
        # including odd values and d=0, on either side of the current minimum.
        inherited_signed = tuple(sorted(4 * (a * a - a0 * a0) for a in left))
        signed_full = exact_signed_shift_closure(tuple(2 * b for b in right))
        if not set(inherited_signed).issubset(signed_full):
            raise AssertionError((index, inherited_signed, signed_full))
        if signed_full == inherited_signed:
            signed_factor_packets_closed += 1
        if len(signed_full) >= 5:
            print("STATUS=FOUND_ERDOS885_K5_IN_PUBLIC_PACKET")
            print(f"PACKET={index} LEFT={left} RIGHT={right}")
            print(f"SIGNED_SHIFT_CLOSURE={signed_full}")
            return

        for dropped in range(6):
            roots = right[:dropped] + right[dropped + 1 :]
            closure = exact_positive_shift_closure(roots)
            subset_closures += 1
            if not set(expected).issubset(closure):
                raise AssertionError((index, dropped, expected, closure))
            if len(closure) > best:
                best = len(closure)
                best_records = [(index, right[dropped], roots, closure)]
                print(f"RECORD positive_shifts={best} packet={index} dropped={right[dropped]}")
                print(f"ROOTS={roots}")
                print(f"EXACT_POSITIVE_SHIFT_CLOSURE={closure}")
            elif len(closure) == best:
                best_records.append((index, right[dropped], roots, closure))
            if len(closure) >= 4:
                print("STATUS=FOUND_5x5_CANDIDATE")
                print(f"SOURCE_LEFT={left}")
                print(f"SOURCE_RIGHT={right}")
                return
            signed_subset = exact_signed_shift_closure(tuple(2 * b for b in roots))
            signed_five_subsets_checked += 1
            largest_signed_five_subset_closure = max(
                largest_signed_five_subset_closure, len(signed_subset)
            )
            if not set(inherited_signed).issubset(signed_subset):
                raise AssertionError((index, dropped, inherited_signed, signed_subset))
            if len(signed_subset) >= 5:
                print("STATUS=FOUND_5x5_SQUARE_SUM_IN_PUBLIC_SUBSET")
                print(f"PACKET={index} DROPPED={right[dropped]}")
                print(f"ROOTS={roots}")
                print(f"SIGNED_SHIFT_CLOSURE={signed_subset}")
                return

    digest = hashlib.sha256(repr(packets).encode()).hexdigest()
    print("STATUS=NO_5x5_LIFT_IN_PUBLIC_4x6_FIVE_SUBSETS")
    print(f"public_packets={len(packets)}")
    print(f"five_root_subsets_checked={subset_closures}")
    print(f"full_six_root_packets_exactly_closed={full_closed}")
    print(f"reverse_three_shift_packets_exactly_closed={reverse_closed}")
    print(f"largest_reverse_root_closure={largest_reverse_closure}")
    print(f"signed_factor_packets_exactly_closed={signed_factor_packets_closed}")
    print(f"signed_five_root_subsets_checked={signed_five_subsets_checked}")
    print(f"largest_signed_five_subset_closure={largest_signed_five_subset_closure}")
    print(f"best_positive_shift_closure={best}")
    print(f"best_record_count={len(best_records)}")
    print(f"public_packet_dataset_sha256={digest}")


if __name__ == "__main__":
    main()
