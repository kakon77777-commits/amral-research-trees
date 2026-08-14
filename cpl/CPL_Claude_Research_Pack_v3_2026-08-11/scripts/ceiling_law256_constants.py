#!/usr/bin/env python3
from fractions import Fraction
N=256
tau=3e-40
p0=Fraction(10909258999421303588095230195816054408197,16000000000000000000000000000000000000000)
p=float(p0)
eps=1/(6*N*N)+tau/(2*N)
print("p0 exact =", p0)
print("p0 decimal =", format(p,".16f"))
print("p0 percent =", format(100*p,".12f"))
print("epsilon =", format(eps,".16g"))
print("gap to 0.68185 =", format(0.68185-p,".16g"))
print("roughness threshold =", format((0.68185-p)/eps,".12f"))
for q in (0.70,0.80,0.90,0.99):
    print(f"gap to {100*q:.0f}% = {q-p:.12f}")
