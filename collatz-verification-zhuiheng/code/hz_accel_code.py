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

from fractions import Fraction


_FLOOR_BETA: list[int] = [0]      # _FLOOR_BETA[k] = floor(k log2 3)
_POW3: list[int] = [1]            # _POW3[k] = 3^k, extended by multiplication


def floor_beta(j: int) -> int:
    """§4: floor(j·log₂3), exactly, as a bit length rather than a logarithm.

    Tabulated incrementally. Computing `(3 ** j).bit_length()` afresh raises 3 to
    a large power on every call, which is what made the A-U.2b.3 drill take half
    an hour: the queue DP asks for every j from 1 to 10000, twice each.
    """
    while len(_FLOOR_BETA) <= j:
        _POW3.append(_POW3[-1] * 3)
        _FLOOR_BETA.append(_POW3[-1].bit_length() - 1)
    return _FLOOR_BETA[j]


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


# ============================================================================
# Round 03-A.4 additions — the deficit queue and the spine excursion.
#
# Round 03-A.3 made the spine deterministic. Round 03-A.4 asks what it costs to
# stay on one: every step of valuation q spends q-1 units of a Sturmian credit
# budget, and the accumulated deficit turns out to BE the orbit's exponential
# growth rate.
# ============================================================================


def orbit_valuations(n: int, m: int) -> list[int]:
    """q_i = v_2(3·Y_{i-1} + 1) along the accelerated odd orbit of n."""
    return list(accel_code(n, m))


def orbit_endpoints(n: int, m: int) -> list[int]:
    """Y_0 = n, Y_1, ..., Y_m along the accelerated odd orbit."""
    out, x = [n], n
    for _ in range(m):
        y = 3 * x + 1
        x = y >> ((y & -y).bit_length() - 1)
        out.append(x)
    return out


def sturmian_credit(m: int) -> int:
    """§4: ⌊γm⌋ with γ = log₂3 − 1, by exact integer powers.

    ⌊γm⌋ = ⌊m·log₂3⌋ − m = (bits of 3^m) − 1 − m, no logarithm involved.
    """
    return floor_beta(m) - m


def deficit(n: int, m: int) -> int:
    """§3: d_m = ⌊βm⌋ − K_m. Subcritical means d_m ≥ 0 at every prefix."""
    return floor_beta(m) - cumulative(accel_code(n, m))[-1]


def credit_spent(n: int, m: int) -> int:
    """§5-§6: Σ_{i≤m} (q_i − 1), the excess valuation spent so far."""
    return sum(q - 1 for q in orbit_valuations(n, m))


def cylinder_residue(r: int) -> int:
    """§9: η_r = −3^{−1} mod 2^r — the single residue with v₂(3y+1) ≥ r."""
    return (-pow(3, -1, 1 << r)) % (1 << r)


def cylinder_visits(n: int, m: int, r: int) -> int:
    """§11: #{ 0 ≤ i < m : Y_i ∈ C_r }."""
    eta, mod = cylinder_residue(r), 1 << r
    return sum(1 for y in orbit_endpoints(n, m)[:m] if y % mod == eta)


def excursion_check(n: int, m: int) -> bool:
    """§18, as the exact integer statement it reduces to.

    `Y_m = 2^{δ_m}[n + (1/3)Σ 2^{−δ_i}]` is Paper 06's accelerated affine formula
    written in log coordinates: multiplying through by 2^{K_m} gives
    `Y_m·2^{K_m} = 3^m·n + Σ_i 3^{m−1−i}·2^{K_i}`, which is checkable in exact
    integers with no floating point at all. The NEW content of §18 is the
    reading — deficit as exponential growth rate — not the identity.
    """
    kappa = accel_code(n, m)
    K = cumulative(kappa)
    lhs = orbit_endpoints(n, m)[m] * 2 ** K[-1]
    rhs = 3 ** m * n + sum(3 ** (m - 1 - i) * 2 ** K[i] for i in range(m))
    return lhs == rhs


def beta_continued_fraction(terms: int) -> list[int]:
    """Partial quotients of β = log₂3, by exact rational comparison.

    No floating logarithm anywhere: the tail is carried as a pair of exact
    rationals (P, Q) standing for log_P(Q), and each quotient is found by
    multiplying P until it passes Q.

    **Cost warning.** Those rationals grow very fast — beta's tenth partial
    quotient is 23, and the exact tail after it is enormous. Asking for ~20 terms
    takes minutes; ~12 is instant. Callers should request only what they need,
    which for denominators up to a few dozen is about six terms.
    """
    from fractions import Fraction
    P, Q = Fraction(2), Fraction(3)
    out: list[int] = []
    for _ in range(terms):
        a, acc = 0, Fraction(1)
        while acc * P <= Q:
            acc *= P
            a += 1
        out.append(a)
        rem = Q / acc
        if rem == 1:
            break
        P, Q = rem, P
    return out


def beta_convergents(terms: int) -> list[tuple[int, int]]:
    """Convergents p/q of β = log₂3, from its partial quotients."""
    cf = beta_continued_fraction(terms)
    # h_{-2}, k_{-2}, h_{-1}, k_{-1} — an earlier version had the numerator and
    # denominator roles swapped, which printed 1/2 where beta's second
    # convergent is 2/1. The anchors below would not have caught that on their
    # own, so they check named values (19/12, 84/53) rather than a shape.
    p_prev, q_prev, p, q = 0, 1, 1, 0
    out: list[tuple[int, int]] = []
    for a in cf:
        p_prev, q_prev, p, q = p, q, a * p + p_prev, a * q + q_prev
        out.append((p, q))
    return out


def legendre_gate(n: int, m: int) -> bool:
    """§34: does δ_m < 1/(2m), so that Legendre makes K_m/m a convergent?

    δ_m = m·log₂3 − K_m is irrational, so the test is done by exact integer
    comparison instead: δ_m < 1/(2m) exactly when 3^{2m²} < 2^{2m·K_m + m}.
    """
    K = cumulative(accel_code(n, m))[-1]
    return 3 ** (2 * m * m) < 2 ** (2 * m * K + m)


# ---------------------------------------------------------------------------
# Round 03-A.5 — Exceptional Occupancy Rigidity.
# The finite-local no-go (§1-§6), the parity bridge that López-Stoll's density
# statement is applied through (§10-§16), and the occupancy / tail-leakage
# split that the closing dichotomy is stated in (§19-§26).
# ---------------------------------------------------------------------------


def all_ones_source(m: int) -> int:
    """§4: the canonical source of the all-one exponent code of length m."""
    return 2 ** (m + 1) - 1


def all_ones_offset(m: int) -> int:
    """§4: B_m for kappa = (1,...,1), claimed in closed form as 3^m - 2^m."""
    return 3 ** m - 2 ** m


def code_lifts(kappa: tuple[int, ...], count: int) -> list[int]:
    """§2: n = r_m + t 2^{K_m+1} for t = 0..count-1, the whole realization family."""
    r, step = source_residue(kappa), 1 << (cumulative(kappa)[-1] + 1)
    return [r + t * step for t in range(count)]


def occupancy_count(n: int, m: int, r: int) -> int:
    """§5, §21: N_{>=r}(m) = #{i <= m : q_i >= r}, counted on the valuations."""
    return sum(1 for q in orbit_valuations(n, m) if q >= r)


def excess(n: int, m: int) -> int:
    """§19: E_m = K_m - m = sum of (q_i - 1); the credit actually spent."""
    return cumulative(accel_code(n, m))[-1] - m


def truncated_occupancy(n: int, m: int, R: int) -> Fraction:
    """§22: G_R(m) = (1/m) sum min(q_i - 1, R - 1)."""
    return Fraction(sum(min(q - 1, R - 1) for q in orbit_valuations(n, m)), m)


def tail_leakage(n: int, m: int, R: int) -> Fraction:
    """§23: L_R(m) = (1/m) sum (q_i - R)_+, the credit escaping to giant q."""
    return Fraction(sum(max(q - R, 0) for q in orbit_valuations(n, m)), m)


def shortcut_parity(n: int, steps: int) -> str:
    """The parity word of the shortcut map T, U for odd and D for even.

    This is the unaccelerated coordinate the density statement is phrased in,
    so it is generated by iterating T directly rather than by expanding an
    accelerated code — the bridge in §12 is then a claim, not a construction.
    """
    out, x = [], n
    for _ in range(steps):
        if x % 2:
            out.append("U")
            x = (3 * x + 1) // 2
        else:
            out.append("D")
            x //= 2
    return "".join(out)


def u_count(word: str, ell: int) -> int:
    """h(l): the number of U symbols among the first l parity symbols."""
    return word[:ell].count("U")


# ---------------------------------------------------------------------------
# Phase II / Round A-U.1 — critical occupation and anchor erasure.
# The exponent-code conjugacy (§1-§5), the singular neighbourhoods the
# invariant-limit theorem is proved through (§7-§10), the two countermodels that
# make the Pure Occupation No-Go (§13-§17), and the anchor cocycle that
# occupation measures cannot see (§21-§26).
# ---------------------------------------------------------------------------


def shift_code(kappa: tuple[int, ...]) -> tuple[int, ...]:
    """The one-sided left shift sigma on exponent codes (§5)."""
    return kappa[1:]


def code_cylinder(kappa: tuple[int, ...]) -> tuple[int, int]:
    """§2: the clopen cylinder of a finite code, as (residue, modulus).

    Omega_hat = r_m + 2^{K_m+1} Z_2, so the modulus is the diameter's inverse.
    """
    return source_residue(kappa), 1 << (cumulative(kappa)[-1] + 1)


def anchor_cocycle(kappa: tuple[int, ...]) -> list[int]:
    """§21, §26: the lift digits t_1..t_m of a code, read along its prefixes.

    A positive integer anchor is exactly `t_m = 0 eventually` — once the modulus
    passes the integer, the canonical source *is* that integer and never lifts
    again. This is the datum §22 shows an occupation measure does not carry.
    """
    return [lift_digit(kappa[:j]) for j in range(1, len(kappa) + 1)]


def mechanical_valuation(m: int) -> int:
    """§15: q*_m = floor(beta m) - floor(beta (m-1)), stated directly."""
    return floor_beta(m) - floor_beta(m - 1)


def mechanical_two_frequency(m: int) -> Fraction:
    """§17: the density of the symbol 2 in the mechanical code's first m terms."""
    return Fraction(sum(1 for j in range(1, m + 1) if mechanical_valuation(j) == 2), m)


def bernoulli_mean_valuation(num: int, den: int) -> Fraction:
    """§13: mean of q under the product measure (1-p) delta_1 + p delta_2.

    Taken as an exact rational p = num/den so the identity mean = 1 + p is
    decided in Fractions rather than floating point.
    """
    p = Fraction(num, den)
    return 1 * (1 - p) + 2 * p


def singular_cylinder(r: int) -> tuple[int, int]:
    """§7: C_r = {x : q(x) >= r}, as (residue, modulus) — one clopen class."""
    return cylinder_residue(r), 1 << r


def in_singular_cylinder(y: int, r: int) -> bool:
    """Membership of C_r, decided by the residue rather than by computing q."""
    res, mod = singular_cylinder(r)
    return y % mod == res


# ---------------------------------------------------------------------------
# Phase II / Round A-U.2a — lift-occupation coupling.
# The accelerated inverse-code series (§1-§2), the block-digit reading of the
# lift (§5), the normalized pointed coordinates and their exact recurrences
# (§12-§15), and the two completions that share every finite datum with a
# genuine positive anchor (§27-§28).
# ---------------------------------------------------------------------------


def inverse_code_source(kappa: tuple[int, ...], bits: int) -> int:
    """§1: B(q) = -sum_j 2^{K_j} / 3^{j+1}, read modulo 2^bits.

    The series converges in the 2-adic metric because 2^{K_j} -> 0 there; the
    division by 3^{j+1} is a modular inverse, not a rational division.
    """
    mod = 1 << bits
    K = cumulative(kappa)
    total = 0
    # j runs to m INCLUSIVE: the j = m term is 2^{K_m}·3^{-(m+1)}, which is not
    # zero modulo 2^{K_m+1}. Only from j = m+1 on does 2^{K_j} vanish there,
    # because K_{m+1} >= K_m + 1. Dropping it costs exactly 2^{K_m}.
    for j in range(len(kappa) + 1):
        total += (1 << K[j]) * pow(3, -(j + 1), mod)
    return (-total) % mod


def source_bit(kappa: tuple[int, ...], j: int) -> int:
    """d_j, the j-th binary digit of the source, read from a long enough prefix."""
    K = cumulative(kappa)[-1]
    return (source_residue(kappa) >> j) & 1 if j <= K else -1


def block_digit(kappa: tuple[int, ...], m: int) -> int:
    """§5: t_{m+1} read as the source's binary block on positions K_m+1..K_{m+1}.

    Same quantity as `lift_digit(kappa[:m+1])`, obtained a different way — from
    the digits of the longer source rather than from a difference of two
    canonical representatives.
    """
    K = cumulative(kappa)
    r = source_residue(kappa[:m + 1])
    return sum(((r >> (K[m] + 1 + j)) & 1) << j for j in range(kappa[m]))


def prefix_endpoint(kappa: tuple[int, ...]) -> int:
    """§9: E_m = (3^m R_m + B_m) / 2^{K_m}, a positive odd integer."""
    return endpoint(source_residue(kappa), kappa)


def x_coord(kappa: tuple[int, ...]) -> Fraction:
    """§12: X_m = R_m / 2^{K_m+1}, the normalized source height in (0,1)."""
    return Fraction(source_residue(kappa), 1 << (cumulative(kappa)[-1] + 1))


def z_coord(kappa: tuple[int, ...]) -> Fraction:
    """§12: Z_m = E_m / 3^m, the normalized endpoint height."""
    return Fraction(prefix_endpoint(kappa), 3 ** len(kappa))


def lift_flux(kappa: tuple[int, ...], m: int) -> Fraction:
    """§12: lambda_{m+1} = t_{m+1} / 2^{q_{m+1}}."""
    return Fraction(lift_digit(kappa[:m + 1]), 1 << kappa[m])


def correction_coord(kappa: tuple[int, ...]) -> Fraction:
    """§14: C_m = Z_m - 2 X_m, claimed equal to B_m / (2^{K_m} 3^m).

    The claim that matters is §14's Decoupling: this depends on the exponent
    code alone, so two sources sharing a code prefix share C_m exactly.
    """
    return z_coord(kappa) - 2 * x_coord(kappa)


def anchor_height(kappa: tuple[int, ...]) -> int:
    """§23: A_m = 2^{K_m+1} X_m = R_m — faithful, monotone, and noncompact."""
    return source_residue(kappa)


def v2_rational(x: Fraction) -> int:
    """v_2 of a rational with odd denominator."""
    if x.denominator % 2 == 0:
        raise ValueError(f"{x} is not a 2-adic integer")
    n = x.numerator
    return (n & -n).bit_length() - 1


def accel_step_rational(x: Fraction) -> tuple[Fraction, int]:
    """One accelerated step on a rational 2-adic integer: (S(x), q)."""
    y = 3 * x + 1
    q = v2_rational(y)
    return y / 2 ** q, q


def negative_completion(kappa: tuple[int, ...]) -> Fraction:
    """§27: x_- = -(2^{K_m} + B_m) / 3^m, the source whose tail is all q = 1.

    -1 is the accelerated fixed point (S(-1) = -1 with q = 1), so continuing any
    finite code by ones lands on it. This negative rational shares every finite
    exact datum with the code's positive realizations.
    """
    K = cumulative(kappa)[-1]
    return Fraction(-(2 ** K + offset(kappa)), 3 ** len(kappa))


def critical_completion(kappa: tuple[int, ...], extra: int) -> tuple[int, ...]:
    """§28: continue a subcritical prefix by the mechanical code's increments."""
    m = len(kappa)
    return kappa + tuple(floor_beta(m + j) - floor_beta(m + j - 1)
                         for j in range(1, extra + 1))


# ---------------------------------------------------------------------------
# Phase II / Round A-U.2b — sparse lift rigidity.
# Return separation (§4-§6), factor complexity and the complexity-peak law
# (§7-§13), the thin-deficit block count that produces the entropy constant
# (§14-§20), and the two families the round eliminates outright (§30-§33).
# ---------------------------------------------------------------------------


def record_deficit(n: int, N: int) -> int:
    """§2: D_N = max over m <= N of d_m, the record deficit."""
    return max(deficit(n, m) for m in range(1, N + 1))


def factor_complexity(word: tuple[int, ...], r: int) -> int:
    """§7: p(r), the number of distinct length-r factors of an exponent word."""
    return len({word[j:j + r] for j in range(len(word) - r + 1)})


def block_excess(n: int, i: int, r: int) -> int:
    """§15: E_{i,r} = sum of (q-1) over positions i+1..i+r."""
    q = orbit_valuations(n, i + r)
    return sum(x - 1 for x in q[i:i + r])


def composition_count(r: int, E: int) -> int:
    """§17: the number of length-r sequences of nonnegative integers summing to E.

    Stated by the paper as C(r+E-1, E); `src17` confronts it with a direct
    enumeration at small r rather than trusting the binomial.
    """
    from math import comb
    return comb(r + E - 1, E)


def entropy_base(g: "Decimal") -> "Decimal":
    """§18: Lambda_g = (1+g)^{1+g} / g^g, evaluated at a Decimal g.

    Taken through logarithms because the exponents are irrational. The caller
    compares it against 3, which is what §20's entropy gap needs, so g must be
    the true gamma rather than a rational approximation to it — pass
    `gamma_decimal()`, not a fraction.
    """
    return ((1 + g) * (1 + g).ln() - g * g.ln()).exp()


def gamma_decimal(digits: int = 40) -> "Decimal":
    """gamma = log2(3) - 1, to `digits` places."""
    from decimal import Decimal, getcontext
    getcontext().prec = digits + 15
    return Decimal(3).ln() / Decimal(2).ln() - 1


def periodic_tail_source(v: tuple[int, ...]) -> Fraction:
    """§33: the source of a purely periodic exponent code, B_per / (2^Q - 3^p).

    Subcriticality forces 2^Q < 3^p, so the denominator is negative and the
    source cannot be a positive integer.
    """
    Q, pp = cumulative(v)[-1], len(v)
    return Fraction(offset(v), 2 ** Q - 3 ** pp)


def cycle_is_supercritical(v: tuple[int, ...]) -> bool:
    """§5: a positive accelerated cycle needs 2^Q > 3^p, i.e. Q > p*beta."""
    return 2 ** cumulative(v)[-1] > 3 ** len(v)


# ---------------------------------------------------------------------------
# Phase II / Round A-U.2b.1 — the sharp packing-entropy threshold.
# The per-block packing bound (§6) and its multi-occurrence sum (§10-§11), the
# composition entropy and its two exact derivative identities (§12, §23), and
# the variational problem whose supremum is the published constant (§20-§24).
# ---------------------------------------------------------------------------


def packing_entropy(z: "Decimal") -> "Decimal":
    """§12: H(z) = (1+z) log2(1+z) - z log2 z."""
    from decimal import Decimal
    ln2 = Decimal(2).ln()
    return ((1 + z) * (1 + z).ln() - z * z.ln()) / ln2


def packing_entropy_derivative(z: "Decimal") -> "Decimal":
    """§12: H'(z) = log2(1 + 1/z), which is positive, so H is increasing."""
    from decimal import Decimal
    return (1 + 1 / z).ln() / Decimal(2).ln()


_ROOT_CACHE: dict[int, "Decimal"] = {}


def entropy_root(digits: int = 60) -> "Decimal":
    """§20: the unique z* in (gamma, 1) with H(z*) = beta, by bisection.

    Deliberately a different method from the subject's own `mpmath.findroot`,
    and on the standard library rather than a third-party package, so agreement
    between the two is agreement between implementations and not a re-run.
    """
    from decimal import Decimal, getcontext
    if digits in _ROOT_CACHE:
        return _ROOT_CACHE[digits]
    getcontext().prec = digits + 25
    beta = Decimal(3).ln() / Decimal(2).ln()
    lo, hi = beta - 1, Decimal(1)
    for _ in range(8 * (digits + 10)):
        mid = (lo + hi) / 2
        if packing_entropy(mid) < beta:
            lo = mid
        else:
            hi = mid
    # cached: the variational scans in `src19` call this inside a bisection loop,
    # and recomputing a 560-step high-precision root each time is what made the
    # first version of that scan unrunnable
    _ROOT_CACHE[digits] = (lo + hi) / 2
    return _ROOT_CACHE[digits]


def packing_constant(digits: int = 60) -> "Decimal":
    """§22: c_pack = x*/beta with x* = z* - gamma."""
    from decimal import Decimal
    beta = Decimal(3).ln() / Decimal(2).ln()
    return (entropy_root(digits) - (beta - 1)) / beta


def variational_ratio(x: "Decimal") -> "Decimal":
    """§23-§24: F(x) = x / H(gamma + x), whose supremum is c_pack."""
    from decimal import Decimal
    beta = Decimal(3).ln() / Decimal(2).ln()
    return x / packing_entropy(beta - 1 + x)


def excess_bounds(r: int, D: int) -> tuple[int, int]:
    """§8: E_- = max(0, floor(gamma r) - D), E_+ = ceil(gamma r) + D."""
    lo_g = floor_beta(r) - r                       # floor(gamma r), exactly
    # gamma is irrational, so gamma*r is never an integer for r >= 1 and the
    # ceiling is always one above the floor. `src18` checks that rather than
    # assuming it, by confirming 2^{floor(beta r)} != 3^r over the tested range.
    return max(0, lo_g - D), lo_g + 1 + D


def block_count_A(r: int, D: int) -> int:
    """§10: A(r,D) = sum over the admissible excess range of C(r+E-1, E)."""
    from math import comb
    lo, hi = excess_bounds(r, D)
    return sum(comb(r + E - 1, E) for E in range(lo, hi + 1))


def block_count_B(r: int, D: int) -> Fraction:
    """§10: B(r,D) = sum of 2^{-E} C(r+E-1, E) over the same range."""
    from math import comb
    lo, hi = excess_bounds(r, D)
    return sum(Fraction(comb(r + E - 1, E), 2 ** E) for E in range(lo, hi + 1))


def occurrence_counts(n: int, N: int, r: int) -> dict:
    """How often each length-r exponent block starts in the first N positions."""
    q = accel_code(n, N)
    out: dict[tuple[int, ...], int] = {}
    for i in range(N - r + 1):
        blk = q[i:i + r]
        out[blk] = out.get(blk, 0) + 1
    return out


# ---------------------------------------------------------------------------
# Phase II / Round A-U.2b.2 — queue entropy and the second-order barrier.
# The exact deficit-corridor dynamic program (§30), the phase-resolved
# mechanical credits it runs on (§3), and the second-order constant that the
# Stirling prefactor buys (§17-§18).
# ---------------------------------------------------------------------------


_CREDIT_CACHE: dict[tuple[int, int], int] = {}


def phase_credit(j: int, phase: int = 0) -> int:
    """§3: b_j = floor(theta + gamma j) - floor(theta + gamma (j-1)), in {0,1}.

    Integer phases only, and the floors are taken exactly through `floor_beta`
    rather than by multiplying a float by j — the subject's own script uses the
    float form, and `src19` checks the two agree over the range it uses.
    """
    key = (j, phase)
    if key in _CREDIT_CACHE:
        return _CREDIT_CACHE[key]

    def fl(k: int) -> int:
        return floor_beta(k) - k if k else 0

    _CREDIT_CACHE[key] = fl(phase + j) - fl(phase + j - 1)
    return _CREDIT_CACHE[key]


_QUEUE_CACHE: dict[tuple[int, int, int], int] = {}


def queue_count(r: int, D: int, phase: int = 0) -> int:
    """§30: the number of queue-admissible blocks of length r in corridor [0, D].

    V_0(d) = 1 for 0 <= d <= D, then V_j(d') = sum over d >= max(0, d'-b_j) of
    V_{j-1}(d), and the answer is the sum of V_r. Accumulated here from the LOW
    end via prefix sums; the subject's script accumulates from the high end via
    suffix sums. Same recurrence, opposite direction.
    """
    key = (r, D, phase)
    if key in _QUEUE_CACHE:
        return _QUEUE_CACHE[key]
    vec = [1] * (D + 1)
    for j in range(1, r + 1):
        b = phase_credit(j, phase)
        total = sum(vec)
        pref = [0] * (D + 2)
        for i in range(D + 1):
            pref[i + 1] = pref[i] + vec[i]
        vec = [total - pref[max(0, t - b)] for t in range(D + 1)]
    # cached: `unpointed_queue_count` needs (r,D) and (r,D-1), and the diagnostic
    # check then asks for (r,D) again. Without this, a single drill run spent a
    # minute recomputing the same corridors.
    _QUEUE_CACHE[key] = sum(vec)
    return _QUEUE_CACHE[key]


def queue_count_bruteforce(r: int, D: int, phase: int = 0) -> int:
    """The same count by direct enumeration, for validating the DP at small r."""
    total = 0

    def walk(j: int, d: int) -> None:
        nonlocal total
        if j > r:
            total += 1
            return
        b = phase_credit(j, phase)
        for e in range(0, d + b + 1):
            nd = d + b - e
            if 0 <= nd <= D:
                walk(j + 1, nd)

    for start in range(D + 1):
        walk(1, start)
    return total


_HPRIME_CACHE: dict[int, "Decimal"] = {}


def entropy_derivative_at_root(digits: int = 60) -> "Decimal":
    """§17: h* = H'(z*) = log2(1 + 1/z*)."""
    from decimal import Decimal, getcontext
    if digits in _HPRIME_CACHE:
        return _HPRIME_CACHE[digits]
    getcontext().prec = digits + 25
    z = entropy_root(digits)
    _HPRIME_CACHE[digits] = (1 + 1 / z).ln() / Decimal(2).ln()
    return _HPRIME_CACHE[digits]


def second_order_constant(digits: int = 60) -> "Decimal":
    """§18: d_pack = 1 / (2 h*)."""
    return 1 / (2 * entropy_derivative_at_root(digits))


def block_scale_exponents(d: "Decimal", s: "Decimal",
                          digits: int = 60) -> tuple["Decimal", "Decimal"]:
    """§26: (P1, P2) for a block scale r = L/beta + s*l.

    Both must be negative for the contradiction, so the admissible d at a given
    s is the smaller of the two thresholds; `src19` scans s to confirm that
    s = 0 is where that minimum is largest.
    """
    from decimal import Decimal, getcontext
    getcontext().prec = digits + 25
    beta = Decimal(3).ln() / Decimal(2).ln()
    z = entropy_root(digits)
    x = z - (beta - 1)
    h = entropy_derivative_at_root(digits)
    p1 = h * d + s * (beta - h * x) - Decimal("0.5")
    p2 = h * (d - x * s) - Decimal("0.5")
    return p1, p2


# ---------------------------------------------------------------------------
# Phase II / Round A-U.2b.3 — the pointed / unpointed correction.
# Implemented from the PROSE DEFINITIONS (§1-§7), not from the shipped script:
# A-U.2b.2's DP turned out to count pointed paths where its own §4 defined an
# unpointed word set, and a reimplementation of the program cannot see that.
# ---------------------------------------------------------------------------


def word_range(word: tuple[int, ...], phase: int = 0) -> int:
    """§4: R(e) = max_j S_j - min_j S_j, with S_j = sum_{i<=j} (e_i - b_i).

    A word is admissible from starting deficit d_0 exactly when
    0 <= d_0 - S_j <= D for every j, i.e. max_j S_j <= d_0 <= D + min_j S_j.
    """
    S = 0
    lo = hi = 0
    for i, e in enumerate(word, start=1):
        S += e - phase_credit(i, phase)
        lo, hi = min(lo, S), max(hi, S)
    return hi - lo


def pointing_multiplicity(word: tuple[int, ...], D: int, phase: int = 0) -> int:
    """§4: the number of admissible starting deficits, D - R(e) + 1 or zero."""
    return max(0, D - word_range(word, phase) + 1)


def unpointed_words(r: int, D: int, phase: int = 0) -> list[tuple[int, ...]]:
    """§4's Q_{r,D} itself — the words with SOME admissible start, enumerated.

    Exponential, so only for small r; it exists so the identities below are
    checked against the definition rather than against a dynamic program.
    """
    out = []

    def walk(j: int, seq: list[int]) -> None:
        if j > r:
            if pointing_multiplicity(tuple(seq), D, phase) > 0:
                out.append(tuple(seq))
            return
        # e_j is bounded because the range can only grow
        for e in range(0, D + 2):
            seq.append(e)
            if word_range(tuple(seq), phase) <= D:
                walk(j + 1, seq)
            seq.pop()

    walk(1, [])
    return out


_BRIDGE_CACHE: dict[tuple[int, int, int], int] = {}


def bridge_count(r: int, D: int, phase: int = 0) -> int:
    """§27: paths from deficit D to deficit 0, the fixed-endpoint bridge.

    Cached, but NOT fused with the pointed pass. Fusing them was tried and made
    the run slower: `queue_count` is memoised, so a fused loop recomputes the
    pointed vector that the cache already holds. Measured 33s -> 47s.
    """
    key = (r, D, phase)
    if key in _BRIDGE_CACHE:
        return _BRIDGE_CACHE[key]
    vec = [0] * (D + 1)
    vec[D] = 1
    for j in range(1, r + 1):
        b = phase_credit(j, phase)
        total = sum(vec)
        pref = [0] * (D + 2)
        for i in range(D + 1):
            pref[i + 1] = pref[i] + vec[i]
        vec = [total - pref[max(0, tt - b)] for tt in range(D + 1)]
    _BRIDGE_CACHE[key] = vec[0]
    return _BRIDGE_CACHE[key]


def unpointed_queue_count(r: int, D: int, phase: int = 0) -> int:
    """§7: Q_{r,D} = P_{r,D} - P_{r,D-1}.

    The identity is verified against `unpointed_words` at small r by `src20`;
    beyond that it is the only tractable route, and the report says so.
    """
    return queue_count(r, D, phase) - (queue_count(r, D - 1, phase) if D else 0)


# ---------------------------------------------------------------------------
# Phase II / Round A-U.2e — multiscale return arithmetic.
# Deviation from the mechanical word (§abstract), the directional split of the
# deficit's total variation (§1), and the reset geometry (§3), whose affine
# identity reduces to an exact integer statement with no floating point at all.
# ---------------------------------------------------------------------------


def deviation_counts(n: int, N: int) -> dict:
    """§abstract, §1: J_N, V_N, U_N, W_N for a real orbit.

    J = positions where q differs from the mechanical word; V = the L1 deviation,
    which is also the deficit path's total variation; U and W its upward and
    downward halves.
    """
    q = accel_code(n, N)
    a = [mechanical_valuation(m) for m in range(1, N + 1)]
    J = sum(1 for i in range(N) if q[i] != a[i])
    V = sum(abs(q[i] - a[i]) for i in range(N))
    U = sum(max(a[i] - q[i], 0) for i in range(N))
    W = sum(max(q[i] - a[i], 0) for i in range(N))
    return {"J": J, "V": V, "U": U, "W": W}


def skipped_credit_positions(n: int, N: int) -> int:
    """§1: #{m <= N : a_m = 2 and q_m = 1}, claimed to equal U_N exactly."""
    q = accel_code(n, N)
    return sum(1 for m in range(1, N + 1)
               if mechanical_valuation(m) == 2 and q[m - 1] == 1)


def exponent_factor_complexity(n: int, N: int, r: int) -> int:
    """The number of distinct length-r factors among the first N exponents."""
    return factor_complexity(accel_code(n, N), r)


def reset_affine_holds(n: int, a: int, b: int) -> bool:
    """§3's Reset Affine Identity, cleared of every power of two and three.

    Y_b = 2^{delta_b - delta_a} Y_a + (2^{delta_b}/3) sum_{i=a}^{b-1} 2^{-delta_i}
    multiplied through by 3^b and 2^{-K_b} becomes

        Y_b 2^{K_b} = Y_a 2^{K_a} 3^{b-a} + sum_{i=a}^{b-1} 3^{b-1-i} 2^{K_i},

    which is an identity between integers. The paper's form is stated with the
    irrational slack delta_m = beta m - K_m; this one needs no float.
    """
    Y = orbit_endpoints(n, b)
    K = cumulative(accel_code(n, b))
    lhs = Y[b] * 2 ** K[b]
    rhs = (Y[a] * 2 ** K[a] * 3 ** (b - a)
           + sum(3 ** (b - 1 - i) * 2 ** K[i] for i in range(a, b)))
    return lhs == rhs


def slack_exceeds(n: int, m: int, h_num: int, h_den: int) -> bool:
    """Is delta_m = beta m - K_m greater than the rational h_num/h_den?

    delta_m > h  iff  3^{m h_den} > 2^{(K_m h_den + h_num)}, in exact integers.
    """
    K = cumulative(accel_code(n, m))[-1]
    return 3 ** (m * h_den) > 2 ** (K * h_den + h_num)


def first_return_below(n: int, a: int, h_num: int, h_den: int,
                       limit: int = 400) -> int | None:
    """§3: the first b > a with delta_b <= h, or None inside `limit` steps."""
    for b in range(a + 1, limit + 1):
        if not slack_exceeds(n, b, h_num, h_den):
            return b
    return None

