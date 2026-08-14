"""Reference Collatz implementation — deliberately naive, deliberately slow.

數學戰士「墜衡」 / AMRAL Research Lab.

This file exists to be *obviously* correct by reading, not to be fast. It uses
Python's arbitrary-precision integers, so it has no overflow behaviour at all,
which makes it a genuinely different arithmetic model from the u128 Rust
engine rather than a second copy of the same assumptions.

Nothing here is optimised. Nothing here has a sieve. If this file and
`collatz_verify.rs` ever disagree, this file is the one to be believed first.
"""

from __future__ import annotations


def standard_step(x: int) -> int:
    """C(x) = x/2 for even x, 3x+1 for odd x."""
    return x // 2 if x % 2 == 0 else 3 * x + 1


def shortcut_step(x: int) -> int:
    """T(x) = x/2 for even x, (3x+1)/2 for odd x."""
    return x // 2 if x % 2 == 0 else (3 * x + 1) // 2


def standard_trajectory(n: int) -> list[int]:
    """Full C-trajectory of n from n down to 1, inclusive. Loops forever on a
    counterexample; that is the honest behaviour for a reference."""
    if n < 1:
        raise ValueError("n must be positive")
    seq = [n]
    x = n
    while x != 1:
        x = standard_step(x)
        seq.append(x)
    return seq


def delay_and_peak(n: int) -> tuple[int, int]:
    """(number of C-steps to reach 1, largest value on the way)."""
    seq = standard_trajectory(n)
    return len(seq) - 1, max(seq)


def sigma_and_peak(n: int) -> tuple[int, int]:
    """(sigma(n), peak) where sigma(n) = min{ j >= 1 : T^j(n) < n } and peak is
    the largest T-value seen at steps 0..sigma(n), n itself included."""
    if n < 2:
        raise ValueError("sigma is only meaningful for n >= 2")
    x = n
    peak = n
    steps = 0
    while x >= n:
        x = shortcut_step(x)
        peak = max(peak, x)
        steps += 1
    return steps, peak


def verify_descent(lo: int, hi: int) -> dict:
    """Walk every odd n in [lo, hi] with no sieve and no shortcuts whatsoever."""
    checked = 0
    max_sigma = 0
    max_sigma_at = 0
    best_peak = 0
    best_at = 0
    n = lo if lo % 2 else lo + 1
    n = max(n, 3)
    while n <= hi:
        s, p = sigma_and_peak(n)
        checked += 1
        if s > max_sigma:
            max_sigma, max_sigma_at = s, n
        if best_at == 0 or p * best_at > best_peak * n:
            best_peak, best_at = p, n
        n += 2
    return {
        "odd_starts_checked": checked,
        "max_sigma": max_sigma,
        "max_sigma_at": max_sigma_at,
        "max_expansion_peak": best_peak,
        "max_expansion_at": best_at,
    }


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) >= 2 and sys.argv[1] == "constants":
        # Values the Rust self-test hard-codes. Printed here so that the
        # constants in the engine have a stated, reproducible origin instead of
        # being numbers someone remembered.
        out = {
            "standard_delay_and_peak": {
                str(n): list(delay_and_peak(n)) for n in (1, 2, 3, 6, 7, 27, 97, 871, 6171)
            },
            "shortcut_sigma_and_peak": {
                str(n): list(sigma_and_peak(n)) for n in (3, 7, 27, 703, 10087)
            },
        }
        print(json.dumps(out, indent=2))
    else:
        lo = int(sys.argv[1]) if len(sys.argv) > 1 else 3
        hi = int(sys.argv[2]) if len(sys.argv) > 2 else 300_000
        print(json.dumps({"lo": lo, "hi": hi, **verify_descent(lo, hi)}))
