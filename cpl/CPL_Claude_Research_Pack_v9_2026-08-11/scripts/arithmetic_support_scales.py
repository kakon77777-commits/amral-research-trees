#!/usr/bin/env python3
"""
Compute arithmetic scales corresponding to CPL support targets.

If X=T^sigma, the near-diagonal off-diagonal prime-pair scale inferred from
T |log(n/m)| = O(1), n,m~X is H ~ X/T = T^(sigma-1).
In the prime-size X variable, H ~ X^(1-1/sigma).
"""
targets = {
    "P70":1.042628,
    "P80":1.257848,
    "P90":1.701455,
    "P95":2.260790,
    "P99":4.187215,
}
for name,s in targets.items():
    print(
        name,
        "sigma=",s,
        "H~T^",s-1,
        "H~X^",1-1/s,
        "strong-HL-alpha<2:",s<2
    )
