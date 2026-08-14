#!/usr/bin/env python3
"""Elementary support-prime checker for the 696.e1 theorem note.

This does not verify the cited Iwasawa theorems.  It verifies only the
elementary defining conditions of the Chebotarev support set.
"""
import sys

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p-1)//2, p)
    return -1 if r == p-1 else r

def f(x, p):
    return (x**3 + x**2 + 8*x - 16) % p

def cubic_irreducible(q):
    # A cubic over F_q is irreducible iff it has no F_q-root.
    return all(f(x, q) != 0 for x in range(q))

def eligible(q):
    return (
        is_prime(q)
        and q % 24 == 1
        and q != 29
        and legendre(q, 29) == 1
        and cubic_irreducible(q)
    )

if __name__ == "__main__":
    qs = [int(x) for x in sys.argv[1:]] or [
        241, 313, 457, 673, 937, 1009, 1153, 1753, 2017, 2089
    ]
    for q in qs:
        print(q, eligible(q))
