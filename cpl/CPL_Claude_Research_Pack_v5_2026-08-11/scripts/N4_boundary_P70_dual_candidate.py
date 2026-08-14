#!/usr/bin/env python3
"""
Numerical/exact-candidate data for the N=4 boundary escape P70 experiment.

This does NOT certify all configurations.
It records a rationalized dual candidate that still has >70% objective.
"""
from fractions import Fraction

B=Fraction(365,100)
c0=Fraction(112269224,10**8)
y1=Fraction(-38437941,10**8)
y2=Fraction(-25114540,10**8)
y3=Fraction(-11796917,10**8)
mu=Fraction(-3068556,10**8)

obj=c0+Fraction(1,4)*y1+Fraction(1,2)*y2+Fraction(3,4)*y3+B*mu

print("B =",float(B))
print("objective exact =",obj)
print("objective =",float(obj))
print("percent =",100*float(obj))
print("status: candidate only; configuration-wise positivity not yet fully exact-certified")
