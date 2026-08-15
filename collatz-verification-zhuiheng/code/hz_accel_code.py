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

