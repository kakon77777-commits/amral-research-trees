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
