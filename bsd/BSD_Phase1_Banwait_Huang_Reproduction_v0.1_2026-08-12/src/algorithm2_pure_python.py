#!/usr/bin/env python3
"""Pure-Python mirror of the explicit arithmetic predicates in
Banwait–Huang Algorithm 2.

Scope:
- Assumes the base curve has already passed Algorithm 1.
- Reproduces the CLZ20 and Zha16 twist filters.
- Uses elementary finite-field point counting.
- Uses irreducibility of the cubic 2-division polynomial modulo p as the
  inertness test for unramified cubic primes.

This program is a reproducibility tool, not an independent proof of BSD.
"""

from __future__ import annotations
from math import gcd
from typing import Iterable

def prime_factors(n: int) -> list[int]:
    n = abs(int(n))
    out: list[int] = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out.append(n)
    return out

def is_squarefree(n: int) -> bool:
    n = abs(int(n))
    if n == 0:
        return False
    d = 2
    while d*d <= n:
        if n % (d*d) == 0:
            return False
        d += 1
    return True

def valuation_2(n: int) -> int:
    n = abs(int(n))
    if n == 0:
        raise ValueError("2-adic valuation of zero is not used here")
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v

def legendre_symbol(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p-1)//2, p)
    return -1 if value == p-1 else value

def kronecker_at_prime(D: int, p: int) -> int:
    if p == 2:
        if D % 2 == 0:
            return 0
        return 1 if D % 8 in (1, 7) else -1
    return legendre_symbol(D, p)

def discriminant(ainvs: Iterable[int]) -> int:
    a1,a2,a3,a4,a6 = map(int, ainvs)
    b2 = a1*a1 + 4*a2
    b4 = 2*a4 + a1*a3
    b6 = a3*a3 + 4*a6
    b8 = a1*a1*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3*a3 - a4*a4
    return -b2*b2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6

def point_count(ainvs: Iterable[int], p: int) -> int:
    a1,a2,a3,a4,a6 = map(int, ainvs)
    if p == 2:
        total = 1
        for x in range(p):
            rhs = (x**3 + a2*x*x + a4*x + a6) % p
            for y in range(p):
                if (y*y + a1*x*y + a3*y - rhs) % p == 0:
                    total += 1
        return total

    total = 1
    for x in range(p):
        B = (a1*x + a3) % p
        rhs = (x**3 + a2*x*x + a4*x + a6) % p
        disc = (B*B + 4*rhs) % p
        total += 1 + legendre_symbol(disc, p)
    return total

def a_p(ainvs: Iterable[int], p: int) -> int:
    return p + 1 - point_count(ainvs, p)

def two_division_polynomial(ainvs: Iterable[int]) -> list[int]:
    """Ascending coefficients of 4x^3+b2 x^2+2b4 x+b6."""
    a1,a2,a3,a4,a6 = map(int, ainvs)
    b2 = a1*a1 + 4*a2
    b4 = 2*a4 + a1*a3
    b6 = a3*a3 + 4*a6
    return [b6, 2*b4, b2, 4]

def poly_eval(coeffs: list[int], x: int, p: int) -> int:
    value = 0
    for c in reversed(coeffs):
        value = (value*x + c) % p
    return value

def cubic_is_irreducible_mod_p(coeffs: list[int], p: int) -> bool:
    if coeffs[-1] % p == 0:
        return False
    return all(poly_eval(coeffs, x, p) != 0 for x in range(p))

def fundamental_discriminant_of_squarefree(d: int) -> int:
    return d if d % 4 == 1 else 4*d

def admissible_twists_clz(
    ainvs: Iterable[int],
    conductor: int,
    bound: int = 1000
) -> list[int]:
    bad_primes = prime_factors(conductor)
    cache: dict[int,int] = {}
    out: list[int] = []

    for d in range(1, bound+1):
        if not is_squarefree(d) or gcd(d, 3*conductor) != 1:
            continue

        ok = True
        for p in prime_factors(d):
            ap = cache.setdefault(p, a_p(ainvs, p))
            if ap % p == 0:
                ok = False
                break
            if p % 4 != 1 or valuation_2(p+1-ap) != 1:
                ok = False
                break
        if not ok or d % 8 != 1:
            continue

        D = fundamental_discriminant_of_squarefree(d)
        if all(kronecker_at_prime(D, p) == 1 for p in bad_primes if p != 2):
            out.append(d)
    return out

def admissible_twists_zhai(
    ainvs: Iterable[int],
    conductor: int,
    bound: int = 1000
) -> list[int]:
    bad_primes = prime_factors(conductor)
    curve_disc = discriminant(ainvs)
    cubic = two_division_polynomial(ainvs)
    cache: dict[int,int] = {}
    out: list[int] = []

    for d in range(-bound, bound+1):
        if d == 0:
            continue
        if curve_disc > 0 and d < 0:
            continue
        if not is_squarefree(d) or gcd(d, 3*conductor) != 1:
            continue
        if d % 4 != 1:
            continue

        ok = True
        for p in prime_factors(d):
            ap = cache.setdefault(p, a_p(ainvs, p))
            if ap % p == 0:
                ok = False
                break
            if not cubic_is_irreducible_mod_p(cubic, p):
                ok = False
                break
        if not ok:
            continue

        D = fundamental_discriminant_of_squarefree(d)
        if all(kronecker_at_prime(D, p) == 1 for p in bad_primes):
            out.append(d)
    return out
