#!/usr/bin/env python3
"""
Utilities for CPL v11:
1. Verify the exact unordered-pair symmetrisation of Claude Proposition 5.6.
2. Sample the universal near-diagonal kernel kappa(u).
3. Print the P70/P80/P90/P95/P99 arithmetic scale audit.

Research utility, not a proof assistant artifact.
"""
import math
import numpy as np

def pairing_check(seed=20260811, trials=1000):
    rng=np.random.default_rng(seed)
    err=0.0
    for _ in range(trials):
        theta=float(rng.uniform(.03,2))
        u=float(rng.uniform(-8,8))
        Am=complex(rng.normal(),rng.normal())
        An=complex(rng.normal(),rng.normal())
        am=float(rng.uniform(.1,3)); an=float(rng.uniform(.1,3))
        tnm=(an*am/(1j*theta))*(
            np.exp(2j*u)*(Am+np.conj(An))
            -np.exp(1j*u)*(An+np.conj(Am))
        )
        tmn=(am*an/(-1j*theta))*(
            np.exp(-2j*u)*(An+np.conj(Am))
            -np.exp(-1j*u)*(Am+np.conj(An))
        )
        lhs=np.real(tnm+tmn)/(2*np.pi**2)
        rhs=(an*am/(np.pi**2*theta))*(
            (Am.real+An.real)*(np.sin(2*u)-np.sin(u))
            +(Am.imag-An.imag)*(np.cos(2*u)+np.cos(u))
        )
        err=max(err,abs(lhs-rhs))
    return err

def kappa(u):
    if abs(u)<1e-12:
        return 1.0
    return (math.sin(2*u)-math.sin(u))/u

if __name__=="__main__":
    print("max pairing error:",pairing_check())
    targets={
        "P70":1.042628,
        "P80":1.257848,
        "P90":1.701455,
        "P95":2.260790,
        "P99":4.187215,
    }
    for name,s in targets.items():
        print(
            name,
            "sigma",s,
            "H~T^",s-1,
            "H~X^",1-1/s,
            "flat diagonal tail",1-3/s**2+2/s**3
        )
    for u in [0,.25,.5,1,2,3,5,10]:
        print("kappa",u,kappa(u))
