"""Independent exact checks for the Chengxu E885 boundary route.

This script deliberately uses direct divisor enumeration and integer square
tests instead of the Rust pair-fiber searcher's data structures.
"""

from math import isqrt

from sympy import divisors


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


def positive_shifts_for_roots(roots: list[int]) -> list[int]:
    roots = sorted(roots)
    gap = roots[1] ** 2 - roots[0] ** 2
    shifts: set[int] = set()
    for u in divisors(gap):
        v = gap // u
        if u >= v or (u + v) % 2:
            continue
        y0 = (v - u) // 2
        if y0 <= roots[0]:
            continue
        shift = y0 * y0 - roots[0] ** 2
        if shift > 0 and all(is_square(z * z + shift) for z in roots):
            shifts.add(shift)
    return sorted(shifts)


def positive_roots_for_shifts(shifts: list[int]) -> list[int]:
    shifts = sorted(shifts)
    gap = shifts[1] - shifts[0]
    roots: set[int] = set()
    for u in divisors(gap):
        v = gap // u
        if u >= v or (u + v) % 2:
            continue
        y0 = (v - u) // 2
        z2 = y0 * y0 - shifts[0]
        if z2 <= 0 or not is_square(z2):
            continue
        z = isqrt(z2)
        if all(is_square(z * z + shift) for shift in shifts):
            roots.add(z)
    return sorted(roots)


def verify_square_sum_packet(roots: list[int], shifts: list[int]) -> None:
    assert len(roots) == len(set(roots))
    assert len(shifts) == len(set(shifts))
    assert all(is_square(z * z + shift) for z in roots for shift in shifts)


def factor_differences(n: int) -> set[int]:
    return {n // a - a for a in divisors(n) if a <= n // a}


def common_factor_differences(rows: list[int]) -> list[int]:
    common = factor_differences(rows[0])
    for n in rows[1:]:
        common &= factor_differences(n)
    return sorted(common)


def b_set(delta: int) -> set[int]:
    return {
        delta // a - a
        for a in divisors(delta)
        if a <= delta // a and (a + delta // a) % 2 == 0 and delta // a - a > 0
    }


def main() -> None:
    pinned_roots = [330, 870, 2445, 4155, 10482]
    pinned_shifts = [756000, 15971200, 45130176]
    chengxu_roots = [120, 1380, 5080, 9228, 15420]
    chengxu_shifts = [1389825, 26611200, 247104000]
    obstruction_roots = [18, 66, 186]
    obstruction_shifts = [1885, 3040, 25920, 110565]
    chengxu_rows = [472500, 6448000, 21285396, 59440500]
    chengxu_differences = [120, 1185, 5160, 15720]
    k53_rows = [299700, 673920, 5567380]
    k53_differences = [216, 567, 1128, 1848, 5496]
    k63_rows = [4148640, 34418880, 300736800]
    k63_differences = [2988, 4356, 5787, 11164, 17046, 23948]
    transposed_k45_rows = [10046592, 24561225, 115706752, 281637972, 564578560]
    transposed_k45_differences = [5976, 10104, 24216, 69624]
    transposed_k45_scaled2_rows = [4 * n for n in transposed_k45_rows]
    transposed_k45_scaled2_differences = [2 * d for d in transposed_k45_differences]
    same_parity_sextuple = [744, 912, 1104, 1808, 2928, 6932]
    sextuple_deltas = [
        (s * s - same_parity_sextuple[0] ** 2) // 4
        for s in same_parity_sextuple[1:]
    ]

    for roots, shifts in (
        (pinned_roots, pinned_shifts),
        (chengxu_roots, chengxu_shifts),
        (obstruction_roots, obstruction_shifts),
    ):
        verify_square_sum_packet(roots, shifts)

    assert positive_shifts_for_roots(pinned_roots) == pinned_shifts
    assert positive_shifts_for_roots(chengxu_roots) == chengxu_shifts
    assert positive_roots_for_shifts(pinned_shifts) == pinned_roots
    assert positive_roots_for_shifts(chengxu_shifts) == chengxu_roots
    assert positive_shifts_for_roots(obstruction_roots) == obstruction_shifts
    assert positive_roots_for_shifts(obstruction_shifts) == obstruction_roots
    assert common_factor_differences(chengxu_rows) == chengxu_differences
    assert common_factor_differences(k53_rows) == k53_differences
    assert common_factor_differences(k63_rows) == k63_differences
    assert common_factor_differences(transposed_k45_rows) == transposed_k45_differences
    assert (
        common_factor_differences(transposed_k45_scaled2_rows)
        == transposed_k45_scaled2_differences
    )
    pair_spectrum = b_set(sextuple_deltas[0]) & b_set(sextuple_deltas[1])
    full_spectrum = set.intersection(*(b_set(delta) for delta in sextuple_deltas))
    assert sorted(pair_spectrum) == [24, 366, 536, 744, 1896]
    assert sorted(full_spectrum) == [24, 744, 1896]

    print("BOUNDARY_PACKET_VERIFICATION=PASS")
    print(f"PINNED_EXACT_POSITIVE_SHIFTS={pinned_shifts}")
    print(f"PINNED_EXACT_POSITIVE_ROOTS={pinned_roots}")
    print(f"CHENGXU_EXACT_POSITIVE_SHIFTS={chengxu_shifts}")
    print(f"CHENGXU_EXACT_POSITIVE_ROOTS={chengxu_roots}")
    print(f"OBSTRUCTION_EXACT_POSITIVE_SHIFTS={obstruction_shifts}")
    print(f"OBSTRUCTION_EXACT_POSITIVE_ROOTS={obstruction_roots}")
    print(f"CHENGXU_EXACT_COMMON_FACTOR_DIFFERENCES={chengxu_differences}")
    print(f"K53_EXACT_COMMON_FACTOR_DIFFERENCES={k53_differences}")
    print(f"K63_EXACT_COMMON_FACTOR_DIFFERENCES={k63_differences}")
    print(f"TRANSPOSED_K45_EXACT_COMMON_FACTOR_DIFFERENCES={transposed_k45_differences}")
    print(
        "TRANSPOSED_K45_SCALED2_EXACT_COMMON_FACTOR_DIFFERENCES="
        f"{transposed_k45_scaled2_differences}"
    )
    print(f"SEXTUPLE_PAIR_SPECTRUM={sorted(pair_spectrum)}")
    print(f"SEXTUPLE_FULL_SPECTRUM={sorted(full_spectrum)}")


if __name__ == "__main__":
    main()
