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


# ============================================================================
# Round 03-A.2 additions — the exact 2–3 bridge.
#
# Round 03-A.1 worked mod 2^{K_m+1}. Round 03-A.2 separates that into a COARSE
# residue mod 2^{K_m} (endpoint merely integral, §2) and one extra bit ε_m that
# makes the endpoint odd (§3), then shows that same bit also governs the ternary
# side: it is the endpoint's wrap count and the complement of its parity.
# ============================================================================


def canonical_endpoint(kappa: tuple[int, ...]) -> int:
    """§4: M_m ≡ 2^{−K_m}·B_m (mod 3^m), taken in 1 ≤ M_m ≤ 3^m."""
    m = len(kappa)
    K = cumulative(kappa)[-1]
    M = (pow(2, -K, 3 ** m) * offset(kappa)) % 3 ** m
    return 3 ** m if M == 0 else M


def coarse_source(kappa: tuple[int, ...]) -> int:
    """§5-§8: Q_m = (2^{K_m}·M_m − B_m)/3^m, which §7 places in (0, 2^{K_m}).

    This is the coarse residue of §2 — the start that only makes the endpoint an
    integer, without requiring it odd.
    """
    m = len(kappa)
    K = cumulative(kappa)[-1]
    num = 2 ** K * canonical_endpoint(kappa) - offset(kappa)
    if num % 3 ** m:
        raise ArithmeticError("§5's Q_m is not an integer for this code")
    return num // 3 ** m


def sync_bit(kappa: tuple[int, ...]) -> int:
    """§10: ε_m = 1 − (M_m mod 2)."""
    return 1 - (canonical_endpoint(kappa) % 2)


def exact_endpoint(kappa: tuple[int, ...]) -> int:
    """§9: Ŷ_m = M_m + ε_m·3^m, the endpoint the exact source actually reaches."""
    return canonical_endpoint(kappa) + sync_bit(kappa) * 3 ** len(kappa)


# ============================================================================
# Round 03-A.3 additions — endpoint 2-adic state and the zero-lift spine.
#
# Round 03-A.2 gave one bit per step. Round 03-A.3 collects all of them into a
# single 2-adic state Xi_m and shows the next exponent SELECTS a bit of it — and
# that exactly one choice of exponent keeps the source fixed. The tree of exact
# codes therefore carries a deterministic sub-object: the spine.
# ============================================================================

XI_PRECISION = 96      # bits of Xi_m kept; guarded against by the callers


def endpoint_state(kappa: tuple[int, ...], bits: int = XI_PRECISION) -> int:
    """§5: Xi_m = −(3·M_m + 1)·3^{−(m+1)} in Z_2, truncated to `bits` bits.

    A 2-adic integer has no finite representation, so this is a truncation and is
    named as one. Every caller must use fewer than `bits` low bits of it; the
    checks assert that rather than trusting it.
    """
    m = len(kappa)
    mod = 1 << bits
    return (-(3 * canonical_endpoint(kappa) + 1) * pow(3, -(m + 1), mod)) % mod


def coarse_lift_digit(kappa: tuple[int, ...], q: int) -> int:
    """§4-§5: c_{m+1} = [Xi_m]_q, the low q bits of the endpoint state."""
    return endpoint_state(kappa) & ((1 << q) - 1)


def zero_lift_exponent(kappa: tuple[int, ...]) -> int:
    """§19: q*_m = v_2(3·Ŷ_m + 1), the self-generated exponent.

    §19 also gives q* = v_2(Xi_m − eps_m); this route uses the exact endpoint
    directly, so it needs no 2-adic truncation at all and the two can be
    compared.
    """
    y = 3 * exact_endpoint(kappa) + 1
    return (y & -y).bit_length() - 1


def subcritical_budget(kappa: tuple[int, ...]) -> int:
    """§23: Q_m = ⌊β(m+1)⌋ − K_m, the room left for the next exponent."""
    return floor_beta(len(kappa) + 1) - cumulative(kappa)[-1]


def spine_survives(kappa: tuple[int, ...]) -> bool:
    """§24: the anchor-preserving move stays subcritical iff q* ≤ Q."""
    return zero_lift_exponent(kappa) <= subcritical_budget(kappa)


def trace_spine(kappa: tuple[int, ...], limit: int = 400) -> dict:
    """Follow the deterministic zero-lift spine until §24 ejects it.

    §20 makes this well defined: each node has at most one source-preserving
    child, so there is nothing to search — the continuation is forced.
    """
    steps = 0
    node = kappa
    while steps < limit:
        q, Q = zero_lift_exponent(node), subcritical_budget(node)
        if q > Q:
            return {"steps": steps, "end": node, "ejected_q": q, "budget": Q,
                    "hit_limit": False}
        node = node + (q,)
        steps += 1
    return {"steps": steps, "end": node, "ejected_q": None, "budget": None,
            "hit_limit": True}


def subcritical_lifetime(n: int, limit: int = 400) -> int:
    """How many odd steps an odd start stays inside the subcritical cone."""
    m = 0
    while m < limit and is_subcritical(accel_code(n, m + 1)):
        m += 1
    return m
