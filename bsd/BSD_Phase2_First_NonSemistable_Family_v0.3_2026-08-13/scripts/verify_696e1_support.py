#!/usr/bin/env python3
"""Elementary verifier for the explicit 696.e1 prime support conditions.

No Sage dependency. It verifies:
- q prime
- q ≡ 1 mod 24
- (q/29)=1
- 2-division cubic irreducible mod q
- a_q parity and ordinary status
"""
from math import isqrt
import sys

def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d=3
    while d*d <= n:
        if n%d == 0: return False
        d += 2
    return True

def legendre(a,p):
    a%=p
    if a==0:return 0
    r=pow(a,(p-1)//2,p)
    return -1 if r==p-1 else r

def f(x,p):
    return (x**3+x**2+8*x-16)%p

def inert_cubic(q):
    return all(f(x,q)!=0 for x in range(q))

def a_q(q):
    return -sum(legendre(f(x,q),q) for x in range(q))

def check(q):
    ap=a_q(q) if is_prime(q) and q not in (2,3,29) else None
    return {
        "q":q,
        "prime":is_prime(q),
        "q_mod_24":q%24,
        "split_2_3":q%24==1,
        "legendre_q_29":legendre(q,29) if q!=29 else 0,
        "inert_2division_cubic":inert_cubic(q) if is_prime(q) and q not in (2,3,29) else False,
        "a_q":ap,
        "a_q_odd":None if ap is None else bool(ap%2),
        "ordinary":None if ap is None else ap%q != 0,
    }

if __name__ == "__main__":
    for s in sys.argv[1:]:
        print(check(int(s)))
