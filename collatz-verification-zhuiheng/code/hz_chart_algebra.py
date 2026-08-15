"""The Hard-Zeta chart algebra of Phase I / Round 01, implemented from the paper.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Hard-Zeta Exact Refinement Algebra — Phase I /
Round 01* (2026-08-11 13:12).

Round 01 replaces "scan every prefix" with a **recursion**: each chart `w` in
`{D,U}^k` carries `(r_w, u_w, b_w, m_w, h(w))`, and a child's data is a closed
formula in the parent's. This module implements those formulas exactly as the
paper writes them — integer arithmetic throughout, nothing rearranged — so that
`src07` can confront them with direct iteration.

Nothing here is derived independently. That is deliberate: this file is the
paper's claim rendered executable, and the checking happens elsewhere against a
brute-force walk that assumes none of it.

Hurwitz zeta is needed for §10-§11 and is computed by Euler-Maclaurin, anchored
against closed forms the paper does not supply (pi^2/6, Apery, the half-integer
reflection).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

# ---------------------------------------------------------------- Hurwitz zeta

_BERNOULLI = [Fraction(1, 6), Fraction(-1, 30), Fraction(1, 42),
              Fraction(-1, 30), Fraction(5, 66), Fraction(-691, 2730),
              Fraction(7, 6)]


def hurwitz_zeta(s: float, a: float, terms: int = 24, corrections: int = 7) -> float:
    """zeta(s, a) for s > 1, a > 0, by Euler-Maclaurin.

    Accuracy is checked in `self_test()` against three closed forms rather than
    assumed from the formula.
    """
    if a <= 0:
        raise ValueError(f"hurwitz_zeta needs a > 0, got {a}")
    total = math.fsum((n + a) ** -s for n in range(terms))
    x = terms + a
    total += x ** (1 - s) / (s - 1)
    total += 0.5 * x ** -s
    rising = s
    for j in range(1, corrections + 1):
        b = float(_BERNOULLI[j - 1]) / math.factorial(2 * j)
        total += b * rising * x ** (-(s + 2 * j - 1))
        rising *= (s + 2 * j - 1) * (s + 2 * j)
    return total


def ap_dirichlet_mass(s: float, q: int, r: int, lo: int, hi: int | None) -> float:
    """§10: sum of n^{-s} over n >= 1, n = r (mod q), lo <= n <= hi.

    `hi = None` is the paper's U = infinity. Written to follow §10 step for step,
    including its `a_pos` guard against the n = 0 term when r = 0.
    """
    a_pos = 1 if r == 0 else 0
    A = max(a_pos, -((r - lo) // q))          # ceil((lo - r) / q)
    if hi is None:
        return q ** -s * hurwitz_zeta(s, A + r / q)
    B = (hi - r) // q
    if B < A:
        return 0.0
    return q ** -s * (hurwitz_zeta(s, A + r / q)
                      - hurwitz_zeta(s, B + 1 + r / q))


# --------------------------------------------------------------- chart algebra

@dataclass(frozen=True)
class Chart:
    """One hard chart, carrying exactly the data Round 01 §1 assigns to a word."""
    word: str
    k: int
    r: int                  # canonical residue, 0 <= r < 2^k
    u: int                  # count of U steps
    b: int                  # affine offset: F_w(n) = (3^u n + b) / 2^k
    m: int                  # m_w = F_w(r_w)
    h: int | None           # hard height; None means +infinity

    # ---- §1
    def F(self, n: int) -> Fraction:
        return Fraction(3 ** self.u * n + self.b, 2 ** self.k)

    def omega_members(self, lo: int, hi: int):
        """Omega_w intersect [lo, hi], as the paper's positive-integer cylinder."""
        q = 2 ** self.k
        start = self.r if self.r >= max(lo, 1) else self.r + q * (
            -((self.r - max(lo, 1)) // q))
        return range(start, hi + 1, q)

    def hard_members(self, lo: int, hi: int):
        """H~_w intersect [lo, hi], via the hard height rather than by scanning."""
        top = hi if self.h is None else min(hi, self.h)
        if top < lo:
            return range(0)
        return self.omega_members(max(lo, 2), top)

    # ---- §11
    def mass(self, s: float) -> float:
        return ap_dirichlet_mass(s, 2 ** self.k, self.r, 2, self.h)


ROOT = Chart(word="", k=0, r=0, u=0, b=0, m=0, h=None)


def children(w: Chart) -> tuple[Chart, Chart]:
    """§2, §3, §4, §5, §6 — the whole child recursion, in the paper's order."""
    k, q = w.k, 2 ** w.k
    p = w.m % 2                                              # §2

    r_D = w.r + q * p                                        # §2 D-child
    r_U = w.r + q * (1 - p)                                  # §2 U-child

    u_D, b_D = w.u, w.b                                      # §3
    u_U, b_U = w.u + 1, 3 * w.b + q                          # §3

    # §3 target bases. Both are stated as fractions in the paper and are
    # integers; the assertion is a claim about the algebra, not a formatting
    # convenience, so it is checked rather than assumed away by // division.
    num_D = w.m + 3 ** w.u * p
    num_U = 3 * (w.m + 3 ** w.u * (1 - p)) + 1
    if num_D % 2 or num_U % 2:
        raise ArithmeticError(
            f"§3 target base is not an integer at word {w.word!r}: "
            f"D numerator {num_D}, U numerator {num_U}")
    m_D, m_U = num_D // 2, num_U // 2

    out = []
    for word, r, u, b, m in (("D", r_D, u_D, b_D, m_D), ("U", r_U, u_U, b_U, m_U)):
        delta = 2 ** (k + 1) - 3 ** u                         # §4
        if delta == 0:
            raise ArithmeticError("§4 says delta is never 0, but it is")
        if delta > 0:                                         # §5
            c = b // delta
            h = c if w.h is None else min(w.h, c)             # §6
        else:
            h = w.h                                           # c = +infinity
        out.append(Chart(word=w.word + word, k=k + 1, r=r, u=u, b=b, m=m, h=h))
    return out[0], out[1]


def delta_of(k: int, u: int) -> int:
    """§4 drift gap for a (k)-length word with u up-steps: 2^k - 3^u."""
    return 2 ** k - 3 ** u


def cap_of(b: int, delta: int) -> int | None:
    """§5 new-prefix hard cap; None for the paper's c_v = +infinity."""
    return b // delta if delta > 0 else None


def first_descent_stratum(parent: Chart, child: Chart, lo: int, hi: int):
    """§8: values hard through the parent that first descend at the child's step."""
    delta = delta_of(child.k, child.u)
    if delta < 0:
        return range(0)                                       # D_v = empty
    c = cap_of(child.b, delta)
    top = hi if parent.h is None else min(hi, parent.h)
    bottom = max(2, c + 1, lo)
    if top < bottom:
        return range(0)
    return child.omega_members(bottom, top)


def first_descent_mass(parent: Chart, child: Chart, s: float) -> float:
    """§11 D_v(s), by the paper's arithmetic-progression formula."""
    delta = delta_of(child.k, child.u)
    if delta < 0:
        return 0.0
    c = cap_of(child.b, delta)
    return ap_dirichlet_mass(s, 2 ** child.k, child.r, max(2, c + 1), parent.h)


def level(k: int) -> list[Chart]:
    """Every chart of depth k, built by repeated refinement from the root."""
    charts = [ROOT]
    for _ in range(k):
        nxt = []
        for w in charts:
            nxt.extend(children(w))
        charts = nxt
    return charts


def zone(k: int, u: int) -> str:
    """§19 trichotomy for the children of a depth-k word with u up-steps."""
    if 3 ** (u + 1) < 2 ** (k + 1):
        return "A"                      # both children contracting
    if 3 ** u < 2 ** (k + 1) < 3 ** (u + 1):
        return "B"                      # D contracting, U expanding
    if 2 ** (k + 1) < 3 ** u:
        return "C"                      # both expanding
    raise ArithmeticError(f"§19 claims a trichotomy but k={k}, u={u} fits none")


# ------------------------------------------------------------------- self-test

def self_test() -> list[str]:
    """Anchors for the numerics this module supplies. Returns failure strings."""
    bad = []
    # Hurwitz zeta against closed forms the paper does not provide
    if abs(hurwitz_zeta(2, 1) - math.pi ** 2 / 6) > 1e-13:
        bad.append(f"zeta(2,1) = {hurwitz_zeta(2, 1)!r}, expected pi^2/6")
    if abs(hurwitz_zeta(3, 1) - 1.2020569031595942854) > 1e-13:
        bad.append(f"zeta(3,1) = {hurwitz_zeta(3, 1)!r}, expected Apery")
    for s in (1.5, 2.0, 3.0, 4.0):
        want = (2 ** s - 1) * hurwitz_zeta(s, 1)
        got = hurwitz_zeta(s, 0.5)
        if abs(got - want) / want > 1e-12:
            bad.append(f"zeta({s},1/2) = {got!r}, reflection expects {want!r}")
        want2 = hurwitz_zeta(s, 1) - 1
        got2 = hurwitz_zeta(s, 2)
        if abs(got2 - want2) / abs(want2) > 1e-12:
            bad.append(f"zeta({s},2) = {got2!r}, expected zeta({s}) - 1")
    # the AP mass against brute-force summation on a finite window
    for q, r in ((8, 3), (16, 0), (5, 1)):
        for s in (2.0, 3.5):
            want = math.fsum(n ** -s for n in range(2, 5000)
                             if n % q == r % q)
            got = ap_dirichlet_mass(s, q, r, 2, 4999)
            if abs(got - want) / want > 1e-12:
                bad.append(f"AP mass q={q} r={r} s={s}: {got!r} vs {want!r}")
    # §10's a_pos guard keeps the n = 0 term out when r = 0. Every caller in this
    # tree passes lo >= 2, which forces A >= 1 on its own, so the guard is dead
    # code from their point of view and a drill against it came back silent.
    # This anchor calls with lo = 0 so the guard is actually load-bearing
    # somewhere, rather than being a claim nothing can test.
    for s in (2.0, 3.0):
        want = math.fsum(n ** -s for n in range(1, 4000) if n % 16 == 0)
        try:
            got = ap_dirichlet_mass(s, 16, 0, 0, 3999)
        except (ZeroDivisionError, OverflowError, ValueError) as exc:
            bad.append(f"AP mass with lo=0, r=0, s={s} raised {exc!r}")
            continue
        if not math.isfinite(got) or abs(got - want) / want > 1e-12:
            bad.append(f"AP mass lo=0 r=0 s={s}: {got!r} vs {want!r}")
    return bad


if __name__ == "__main__":
    failures = self_test()
    print("\n".join(failures) if failures
          else "hz_chart_algebra self-test ok (14 anchors)")
    raise SystemExit(1 if failures else 0)


# ============================================================================
# Round 02 additions — the quotient-coordinate form, and first-crossing words.
#
# Round 02 restates Round 01's thresholds in the parent's quotient coordinate
# `a` (where n = r_w + 2^k a) rather than in n. The two must agree, and
# `src08` checks that they do rather than taking it on the paper's word.
# ============================================================================


def q_D(w: "Chart") -> int | None:
    """§3: the D-child survivor cap in the parent's quotient coordinate."""
    delta = 2 ** (w.k + 1) - 3 ** w.u
    if delta <= 0:
        return None                      # uniformly expanding: q = +infinity
    return (w.m - 2 * w.r) // delta


def q_U(w: "Chart") -> int | None:
    """§4: the U-child survivor cap in the parent's quotient coordinate."""
    delta = 2 ** (w.k + 1) - 3 ** (w.u + 1)
    if delta <= 0:
        return None
    return (3 * w.m + 1 - 2 * w.r) // delta


def parity_zeta(s: float, r: int, k: int, A_lo: int, B_hi: int | None,
                e: int) -> float:
    """§5: sum of (r + 2^k a)^{-s} over A <= a <= B with a = e (mod 2).

    Those a form an arithmetic progression of step 2, so the n they produce form
    one modulo 2^(k+1) — which is what makes this the child cylinder's mass.
    """
    first = A_lo if (A_lo - e) % 2 == 0 else A_lo + 1
    n_lo = r + 2 ** k * first
    n_hi = None if B_hi is None else r + 2 ** k * B_hi
    if n_hi is not None and n_hi < n_lo:
        return 0.0
    return ap_dirichlet_mass(s, 2 ** (k + 1), n_lo % 2 ** (k + 1), n_lo, n_hi)


def beta(k: int) -> int:
    """§7: floor((k+1) * ln2/ln3), by integer powers rather than a logarithm.

    beta_k is the largest u with 3^u < 2^(k+1), which is exactly
    (2^(k+1)).bit_length() read through powers of 3 — no rounding involved.
    """
    u, p = 0, 1
    while p * 3 < 2 ** (k + 1):
        p *= 3
        u += 1
    return u


def zone_round02(k: int, u: int) -> str:
    """§7's trichotomy, stated through beta_k instead of through the powers."""
    b = beta(k)
    if u <= b - 1:
        return "A"
    if u == b:
        return "B"
    return "C"


def nu(w: "Chart") -> int:
    """§16: the least member of Omega_w that lies in the Hard-Zeta domain."""
    return w.r if w.r >= 2 else w.r + 2 ** w.k


def is_first_crossing(w: "Chart") -> bool:
    """§15: every proper prefix expanding, and this one contracting."""
    return 3 ** w.u < 2 ** w.k


def first_crossing_words(maxlen: int) -> list["Chart"]:
    """§15's set W_fc, up to a given length.

    Pruned by the defining condition itself: a word is only extended while it is
    still uniformly expanding, so the search never enters a subtree that cannot
    contain a first-crossing word.
    """
    out, stack = [], [ROOT]
    while stack:
        w = stack.pop()
        for c in children(w):
            if 3 ** c.u < 2 ** c.k:
                out.append(c)
            elif 3 ** c.u > 2 ** c.k and c.k < maxlen:
                stack.append(c)
    return out


def terras_margin(w: "Chart") -> tuple[int, int, int]:
    """§16-§17: (nu(w), c_w, nu(w) - c_w) for a first-crossing word.

    The First-Crossing Residue Separation form of the Terras conjecture says the
    third entry is positive for every w in W_fc.
    """
    delta = 2 ** w.k - 3 ** w.u
    c = w.b // delta
    n = nu(w)
    return n, c, n - c


# ============================================================================
# Round 03-A additions — the coefficient survivor tree.
#
# S_k = { w : 3^(u_j(w)) > 2^j for all j <= k } is the irrational ballot tree of
# Round 03-A §1. Note the contrast with `first_crossing_words`: there every
# PROPER prefix expands and the last contracts; here every prefix including the
# last expands.
# ============================================================================


def crossing_depth(u: int) -> int:
    """§7: K_u, the least j with 3^u < 2^j. Exact — a bit length, not a log."""
    return (3 ** u).bit_length()


def survives(k: int, u: int) -> bool:
    """§1: is a depth-k word with u up-steps still a coefficient survivor?"""
    return 3 ** u > 2 ** k


def survivor_words(maxlen: int) -> dict[int, list["Chart"]]:
    """S_k for k = 1..maxlen, as charts, by breadth-first refinement.

    Pruned by the survival condition itself, so no dead subtree is ever built.
    """
    out: dict[int, list[Chart]] = {}
    frontier = [ROOT]
    for k in range(1, maxlen + 1):
        nxt = [c for w in frontier for c in children(w) if survives(c.k, c.u)]
        out[k] = nxt
        frontier = nxt
    return out


def survivor_dp(maxlen: int) -> dict[tuple[int, int], int]:
    """§3: a_{k,u}, the survivor count by depth and up-count, from the recursion."""
    a = {(0, 0): 1}
    for k in range(1, maxlen + 1):
        for u in range(0, k + 1):
            if not survives(k, u):
                continue
            a[(k, u)] = a.get((k - 1, u), 0) + a.get((k - 1, u - 1), 0)
    return a


def normalized_residue(w: "Chart") -> float:
    """§12: x_w = r_w / 2^k, in (0, 1)."""
    return w.r / 2 ** w.k


def chi_D(x: float, p: int) -> float:
    """§18: which binary lift the D-child receives."""
    return x / 2 if p == 0 else (x + 1) / 2


def rho_D(x: float, p: int, s: float) -> float:
    """§18: the exact fraction of a boundary parent's mass a D-crossing removes."""
    return 2 ** -s * hurwitz_zeta(s, chi_D(x, p)) / hurwitz_zeta(s, x)


def coefficient_mass(k: int, s: float, words: list["Chart"]) -> float:
    """§13: C_k(s) = 2^{-ks} * sum over survivors of zeta(s, x_w).

    Exact — an infinite sum per cylinder, closed by the Hurwitz zeta, not a
    truncation.
    """
    return 2 ** (-k * s) * math.fsum(
        hurwitz_zeta(s, normalized_residue(w)) for w in words)


def head_mass(words: list["Chart"], s: float) -> float:
    """§25: H_k(s), the mass of the canonical heads alone."""
    return math.fsum(w.r ** -s for w in words)


# ---------------------------------------------------------------------------
# B-Line Handoff v0.1 — the correction-delay frontier, in its own coordinates.
# The handoff restates Round 02's first-crossing test as an integer slack, which
# is the form it asks to be machine-checked in (§13).
# ---------------------------------------------------------------------------


def correction_slack(w: "Chart") -> int:
    """B-Line §4, §13: Lambda(w) = Delta_w * nu(w) - b_w, an exact integer.

    Trichotomy: > 0 immediate descent, = 0 boundary, < 0 correction delay.
    Terras equality on W_fc is exactly Lambda(w) >= 1 for every first-crossing
    word, so the conjecture has an integer lower bound as its finite form.
    """
    return delta_of(w.k, w.u) * nu(w) - w.b


def normalized_correction_ratio(w: "Chart") -> Fraction:
    """B-Line §12: R(w) = b_w / ((2^k - 3^u) nu(w)); delay exactly when R > 1.

    Kept as a Fraction: R(w) = 1 is one of the three cases and a float compare
    could not tell it from either neighbour.
    """
    return Fraction(w.b, delta_of(w.k, w.u) * nu(w))


def word_chart(word: str) -> "Chart":
    """The chart of an explicit U/D word, walked down the child recursion."""
    w = ROOT
    for ch in word:
        d, u = children(w)
        w = u if ch == "U" else d
    return w


def b_extremals(k: int, u: int) -> dict:
    """B-Line §11: the claimed argmin and argmax of b_w at fixed (k, u).

    min at U^u D^{k-u} with b = 3^u - 2^u; max at D^{k-u} U^u with b =
    2^{k-u} (3^u - 2^u). Returned with the words so a caller can confront the
    closed forms with an enumeration rather than trusting them.
    """
    lo, hi = word_chart("U" * u + "D" * (k - u)), word_chart("D" * (k - u) + "U" * u)
    return {"min_word": lo.word, "b_min": lo.b, "b_min_closed": 3 ** u - 2 ** u,
            "max_word": hi.word, "b_max": hi.b,
            "b_max_closed": 2 ** (k - u) * (3 ** u - 2 ** u)}


def words_of_shape(k: int, u: int) -> list["Chart"]:
    """Every chart of length k with exactly u up-steps."""
    out, stack = [], [ROOT]
    while stack:
        w = stack.pop()
        if w.k == k:
            if w.u == u:
                out.append(w)
            continue
        if w.u > u or (u - w.u) > (k - w.k):
            continue
        stack.extend(children(w))
    return out

