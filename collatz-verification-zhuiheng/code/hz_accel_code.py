"""Round 03-A.1's accelerated exponent codes, implemented from the paper.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Hard-Zeta Phase I / Round 03-A.1: Small-Anchor Event
Arithmetic* (2026-08-11 16:13).

Round 03-A.1 changes coordinates. Instead of a parity word it uses the
**accelerated exact code**: for odd `x`, `S(x) = (3x+1)/2^κ` with
`κ = v₂(3x+1)`, so a start is described by `κ = (κ₁,…,κ_m)` and its cumulative
valuation `K_j = Σ_{i≤j} κ_i`.

The whole round then rests on one arithmetic fact: a code determines its source
**exactly**, modulo `2^{K_m+1}`, and extending the code can only *increase* the
canonical representative. This module is that arithmetic, written as the paper
writes it; `src10` confronts it with direct iteration.

Kept separate from `hz_chart_algebra.py` because it is a different coordinate on
the same object, and the two agreeing is worth more than one file agreeing with
itself.
"""

from __future__ import annotations


def floor_beta(j: int) -> int:
    """§4: floor(j·log₂3), exactly, as a bit length rather than a logarithm."""
    return (3 ** j).bit_length() - 1


def accel_code(n: int, m: int) -> tuple[int, ...]:
    """§1: the accelerated exact code of an odd start, by direct iteration."""
    if n % 2 == 0:
        raise ValueError(f"accel_code needs an odd start, got {n}")
    out, x = [], n
    for _ in range(m):
        y = 3 * x + 1
        k = (y & -y).bit_length() - 1      # v_2(y)
        out.append(k)
        x = y >> k
    return tuple(out)


def cumulative(kappa: tuple[int, ...]) -> list[int]:
    """§2: K_j for j = 0..m."""
    out, K = [0], 0
    for k in kappa:
        K += k
        out.append(K)
    return out


def is_subcritical(kappa: tuple[int, ...]) -> bool:
    """§3-§4: every odd endpoint still has coefficient > 1, i.e. K_j ≤ ⌊βj⌋."""
    K = 0
    for j, k in enumerate(kappa, start=1):
        K += k
        if K > floor_beta(j):
            return False
    return True


def offset(kappa: tuple[int, ...]) -> int:
    """§6: B_m, by the recurrence B_{m+1} = 3B_m + 2^{K_m}."""
    B, K = 0, 0
    for k in kappa:
        B = 3 * B + 2 ** K
        K += k
    return B


def endpoint(n: int, kappa: tuple[int, ...]) -> int:
    """§6: x_m = (3^m n + B_m) / 2^{K_m}, as a rational-free integer division."""
    K = cumulative(kappa)[-1]
    num = 3 ** len(kappa) * n + offset(kappa)
    if num % 2 ** K:
        raise ArithmeticError("§6's endpoint is not an integer for this start")
    return num // 2 ** K


def source_residue(kappa: tuple[int, ...]) -> int:
    """§8-§10: the canonical source, r_m = (2^{K_m} − B_m)·3^{−m} mod 2^{K_m+1}.

    The modulus is `2^{K_m+1}` and not `2^{K_m}` because §7's legality needs the
    endpoint ODD, not merely integral — one more binary digit of information.
    """
    m = len(kappa)
    K = cumulative(kappa)[-1]
    mod = 2 ** (K + 1)
    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod


def lift_digit(kappa: tuple[int, ...]) -> int:
    """§12: t_m, the digit by which the source lifts when the code is extended."""
    if not kappa:
        raise ValueError("the empty code has no lift digit")
    parent = kappa[:-1]
    r_prev = source_residue(parent) if parent else 1
    K_prev = cumulative(parent)[-1] if parent else 0
    if not parent:
        # the first code digit lifts from the odd residues mod 2
        return (source_residue(kappa) - 1) // 2
    return (source_residue(kappa) - r_prev) // 2 ** (K_prev + 1)


def residue_rate(kappa: tuple[int, ...]) -> float:
    """§18: ρ_m = log₂(r_m) / K_m."""
    r = source_residue(kappa)
    K = cumulative(kappa)[-1]
    return (r.bit_length() - 1) / K if K else 0.0


def mechanical_code(m: int) -> tuple[int, ...]:
    """§27-§28: κ*_j = ⌊βj⌋ − ⌊β(j−1)⌋, the maximal subcritical code."""
    return tuple(floor_beta(j) - floor_beta(j - 1) for j in range(1, m + 1))


def subcritical_codes(maxlen: int) -> dict[int, list[tuple[int, ...]]]:
    """Every subcritical code of each length up to maxlen."""
    out: dict[int, list[tuple[int, ...]]] = {}
    frontier = [((), 0)]
    for m in range(1, maxlen + 1):
        cap = floor_beta(m)
        nxt = [(kap + (k,), K + k)
               for kap, K in frontier
               for k in range(1, cap - K + 1)]
        out[m] = [kap for kap, _ in nxt]
        frontier = nxt
    return out


def minimum_anchor(maxlen: int, cap: int = 10 ** 7) -> list[dict]:
    """§35: a_m = min over subcritical codes of length m of the canonical source.

    §13 gives r_{m+1} >= r_m along any extension, so a partial code whose source
    already exceeds `cap` can never produce a smaller one later and is dropped.
    That prune is exact **provided the answer stays below `cap`**, which the
    caller must check — the returned rows carry `a_m` so it can. A prune assumed
    safe rather than shown safe would be exactly the kind of unfalsifiable step
    this tree refuses.
    """
    rows: list[dict] = []
    level: list[tuple[int, int]] = [(0, 0)]        # (K, B)
    for m in range(1, maxlen + 1):
        cap_K = floor_beta(m)
        nxt, best, kept = [], None, 0
        for K, B in level:
            for k in range(1, cap_K - K + 1):
                B2 = 3 * B + 2 ** K
                K2 = K + k
                mod = 2 ** (K2 + 1)
                r = ((2 ** K2 - B2) * pow(3, -m, mod)) % mod
                if best is None or r < best:
                    best = r
                if r <= cap:
                    nxt.append((K2, B2))
                    kept += 1
        if best is None:
            break
        rows.append({"m": m, "a_m": best, "codes_kept": kept,
                     "K_cap": cap_K, "prune_cap": cap})
        level = nxt
        if not level:
            break
    return rows
