#!/usr/bin/env python3
from fractions import Fraction
import json

p = 11
A = Fraction(-3024)
B = Fraction(46224)
O = None

def add(P,Q):
    if P is None: return Q
    if Q is None: return P
    x1,y1=P; x2,y2=Q
    if x1 == x2 and y1 == -y2:
        return None
    if P == Q:
        if y1 == 0: return None
        m = (3*x1*x1 + A)/(2*y1)
    else:
        m = (y2-y1)/(x2-x1)
    x3 = m*m - x1 - x2
    y3 = m*(x1-x3) - y1
    return x3,y3

def mul(n,P):
    R=None; Q=P
    while n:
        if n & 1: R=add(R,Q)
        Q=add(Q,Q); n//=2
    return R

def vp(q,p):
    if q == 0: return 10**9
    n=abs(q.numerator); d=abs(q.denominator); v=0
    while n % p == 0: n//=p; v+=1
    while d % p == 0: d//=p; v-=1
    return v

def mod_fraction(q,p):
    return (q.numerator % p) * pow(q.denominator % p,-1,p) % p

# Original minimal model: y^2 + y = x^3 + x^2 - 2x.
a1,a2,a3,a4,a6 = 0,1,1,-2,0
b2 = a1*a1 + 4*a2
b4 = 2*a4 + a1*a3
b6 = a3*a3 + 4*a6
b8 = 4*a2*a6 - a1*a3*a4 + a2*a3*a3 - a4*a4
Delta = -b2*b2*b8 - 8*b4**3 - 27*b6*b6 + 9*b2*b4*b6
c6 = -b2**3 + 36*b2*b4 - 216*b6
assert Delta == 389
assert pow((-c6) % 389, (389-1)//2, 389) == 1  # split multiplicative criterion

# Exact point count modulo 11.
count = 1  # point at infinity
for x in range(p):
    rhs = (x**3 + x**2 - 2*x) % p
    for y in range(p):
        if (y*y + y - rhs) % p == 0:
            count += 1
assert count == 16
a11 = p + 1 - count
assert a11 == -4

# Short model transformation X=36x+12, Y=216y+108.
Pshort = (Fraction(12), Fraction(108))
assert Pshort[1]**2 == Pshort[0]**3 + A*Pshort[0] + B
R16 = mul(16,Pshort)
x16,y16 = R16
t = -x16/y16
assert vp(t,11) == 1
assert t.numerator % 11 == 0
u_t = mod_fraction(Fraction(t.numerator//11,t.denominator),11)
assert u_t == 7

# Formal-log theorem at good odd p: log(t)=t+O(t^2).
# Hence log_short(16P)/11 mod 11 equals t/11 mod 11.
log_short_P_over_11_mod11 = (u_t * pow(16,-1,11)) % 11
assert log_short_P_over_11_mod11 == 8

# omega_short = omega_minimal / 6, so log_minimal = 6*log_short.
log_minimal_P_over_11_mod11 = (6 * log_short_P_over_11_mod11) % 11
assert log_minimal_P_over_11_mod11 == 4

# Minimal-S Euler truncation factors at 11 and 389.
e11 = Fraction(16,11)
e389 = Fraction(388,389)
assert vp(e11,11) == -1
assert vp(e389,11) == 0
# After extracting the one 11 from log(P), the remaining rational factor is a unit.
rational_unit = Fraction(16*388,389)
rational_unit_mod11 = mod_fraction(rational_unit,11)
assert rational_unit_mod11 == 1
local_unit_mod11 = rational_unit_mod11 * log_minimal_P_over_11_mod11 % 11
assert local_unit_mod11 == 4

out = {
  'curve': '389.a1',
  'prime': 11,
  'minimal_discriminant': Delta,
  'point_count_mod_11': count,
  'a_11': a11,
  'split_multiplicative_at_389': True,
  'short_model_P': [str(Pshort[0]), str(Pshort[1])],
  'P16_short_x': str(x16),
  'P16_short_y': str(y16),
  'formal_parameter_t': str(t),
  'v11_t': vp(t,11),
  't_over_11_mod_11': u_t,
  'log_short_P_over_11_mod_11': log_short_P_over_11_mod11,
  'log_minimal_P_over_11_mod_11': log_minimal_P_over_11_mod11,
  'v11_log_minimal_P': 1,
  'euler_11': str(e11),
  'euler_389': str(e389),
  'v11_euler_product': -1,
  'local_unit_mod_11': local_unit_mod11,
  'local_unit_v11': 0,
  'status': 'LOCAL_UNIT_CANCELLATION_EXACT'
}
print(json.dumps(out,indent=2))
print('LOCAL_UNIT_CANCELLATION_EXACT')
