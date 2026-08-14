#!/usr/bin/env python3
"""
Exact-rational certificate for the N=4 boundary-escape toy PairCeiling result.

Statement proved by this script's exact Bernstein certificates:

For every continuous-position marked configuration with total multiplicity N=4,
marks in {1,2}, and every probability law over such configurations satisfying

    E[S(1)] = 1/4,
    E[S(2)] = 1/2,
    E[S(3)] = 3/4,
    E[S(4)] <= B,

the expected simple-point fraction is >= 70% whenever

    B <= 11254781 / 3068556 = 3.667777612662...

This is a toy-model theorem, NOT a theorem about zeta zeros.

Dependencies: sympy (for exact symbolic expansion); final Bernstein arithmetic uses
Python Fraction only.
"""
from fractions import Fraction
import math
import sympy as sp

# Exact dual
c0 = sp.Rational(112269224, 10**8)
y1 = -sp.Rational(38437941, 10**8)
y2 = -sp.Rational(25114540, 10**8)
y3 = -sp.Rational(11796917, 10**8)
mu = -sp.Rational(3068556, 10**8)  # boundary-row dual price, <= 0
a1,a2,a3,a4 = -y1,-y2,-y3,-mu

base = sp.simplify(c0 + sp.Rational(1,4)*y1 + sp.Rational(1,2)*y2 + sp.Rational(3,4)*y3)
B70 = sp.simplify((base - sp.Rational(7,10))/(-mu))

def F(q):
    return Fraction(int(q.p), int(q.q))

def split_line_half(c):
    n=len(c)-1
    levels=[list(c)]
    for _ in range(n):
        p=levels[-1]
        levels.append([(p[i]+p[i+1])/2 for i in range(len(p)-1)])
    left=[levels[k][0] for k in range(n+1)]
    right=[levels[n-k][k] for k in range(n+1)]
    return left,right

def power_to_bernstein_1d(P,var,n):
    poly=sp.Poly(P,var)
    out=[]
    for i in range(n+1):
        s=sp.Rational(0)
        for k in range(i+1):
            s += poly.coeff_monomial(var**k)*sp.Rational(math.comb(i,k), math.comb(n,k))
        out.append(F(s))
    return out

def cert1(B,maxdepth=100):
    stack=[(0,B)]
    internal=leaves=maxd=0
    mint=None
    while stack:
        d,c=stack.pop()
        lb=min(c)
        if lb>=0:
            leaves+=1; maxd=max(maxd,d)
            mint=lb if mint is None or lb<mint else mint
            continue
        assert d<maxdepth
        L,R=split_line_half(c)
        stack += [(d+1,L),(d+1,R)]
        internal+=1
    return internal,leaves,maxd,mint

def power_to_bernstein_2d(P,X,Z,n,m):
    poly=sp.Poly(P,X,Z)
    out={}
    for i in range(n+1):
        for j in range(m+1):
            s=sp.Rational(0)
            for k in range(i+1):
                for l in range(j+1):
                    s += poly.coeff_monomial(X**k*Z**l) \
                        * sp.Rational(math.comb(i,k),math.comb(n,k)) \
                        * sp.Rational(math.comb(j,l),math.comb(m,l))
            out[(i,j)] = F(s)
    return out

def split2(B,degs,dim):
    n,m=degs; L={}; R={}
    if dim==0:
        for j in range(m+1):
            l,r=split_line_half([B[(i,j)] for i in range(n+1)])
            for i in range(n+1):
                L[(i,j)]=l[i]; R[(i,j)]=r[i]
    else:
        for i in range(n+1):
            l,r=split_line_half([B[(i,j)] for j in range(m+1)])
            for j in range(m+1):
                L[(i,j)]=l[j]; R[(i,j)]=r[j]
    return L,R

def cert2(B,degs,maxdepth=100):
    stack=[(0,B)]
    internal=leaves=maxd=0; mint=None
    while stack:
        d,c=stack.pop()
        lb=min(c.values())
        if lb>=0:
            leaves+=1; maxd=max(maxd,d)
            mint=lb if mint is None or lb<mint else mint
            continue
        assert d<maxdepth
        L,R=split2(c,degs,d%2)
        stack += [(d+1,L),(d+1,R)]
        internal+=1
    return internal,leaves,maxd,mint

def power_to_bernstein_3d(P,U,T,C,degs):
    n1,n2,n3=degs
    poly=sp.Poly(P,U,T,C)
    out={}
    for i in range(n1+1):
        for j in range(n2+1):
            for k in range(n3+1):
                s=sp.Rational(0)
                for a in range(i+1):
                    for b in range(j+1):
                        for c in range(k+1):
                            s += poly.coeff_monomial(U**a*T**b*C**c) \
                                * sp.Rational(math.comb(i,a),math.comb(n1,a)) \
                                * sp.Rational(math.comb(j,b),math.comb(n2,b)) \
                                * sp.Rational(math.comb(k,c),math.comb(n3,c))
                out[(i,j,k)] = F(s)
    return out

def split3(B,degs,dim):
    dims=list(degs); L={}; R={}
    others=[d for d in range(3) if d!=dim]
    ranges=[range(dims[d]+1) for d in others]
    import itertools
    for other in itertools.product(*ranges):
        line=[]
        for q in range(dims[dim]+1):
            idx=[0,0,0]; idx[dim]=q
            for od,val in zip(others,other): idx[od]=val
            line.append(B[tuple(idx)])
        l,r=split_line_half(line)
        for q in range(dims[dim]+1):
            idx=[0,0,0]; idx[dim]=q
            for od,val in zip(others,other): idx[od]=val
            L[tuple(idx)]=l[q]; R[tuple(idx)]=r[q]
    return L,R

def cert3(B,degs,maxdepth=100):
    stack=[(0,B)]
    internal=leaves=maxd=0; mint=None
    while stack:
        d,c=stack.pop()
        lb=min(c.values())
        if lb>=0:
            leaves+=1; maxd=max(maxd,d)
            mint=lb if mint is None or lb<mint else mint
            continue
        assert d<maxdepth
        L,R=split3(c,degs,d%3)
        stack += [(d+1,L),(d+1,R)]
        internal+=1
    return internal,leaves,maxd,mint

# ------------------------------------------------------------------
# Pattern (2,2): p=0, positions 0,theta, q=cos(theta)
# ------------------------------------------------------------------
q,Q = sp.symbols("q Q", real=True)
S22={}
for j in range(1,5):
    S22[j] = 2 + 2*sp.chebyshevt(j,q)
R22 = sp.expand(-c0 + sum([a1*S22[1],a2*S22[2],a3*S22[3],a4*S22[4]]))
P22 = sp.expand(R22.subs(q,2*Q-1))
B22 = power_to_bernstein_1d(P22,Q,4)
C22 = cert1(B22)

# ------------------------------------------------------------------
# Pattern (2,1,1): p=1/2.
# u=(alpha+beta)/2, v=(alpha-beta)/2,
# x=cos u, z=cos v.
# S_j=1+T_j(z)^2+2T_j(z)T_j(x).
# ------------------------------------------------------------------
x,z,X,Z = sp.symbols("x z X Z", real=True)
R211 = sp.Rational(1,2)-c0
for j,a in [(1,a1),(2,a2),(3,a3),(4,a4)]:
    tz=sp.chebyshevt(j,z); tx=sp.chebyshevt(j,x)
    R211 += a*(1+tz**2+2*tz*tx)
R211 = sp.expand(R211)
P211 = sp.Poly(sp.expand(R211.subs({x:2*X-1,z:2*Z-1})),X,Z)
B211 = power_to_bernstein_2d(P211.as_expr(),X,Z,P211.degree(X),P211.degree(Z))
C211 = cert2(B211,(P211.degree(X),P211.degree(Z)))

# ------------------------------------------------------------------
# Pattern (1,1,1,1): p=1.
#
# Rotate all roots so e4=1 (form factors are rotation-invariant).
# Let e1=A=x+iy, e2=B real, e3=conj(A).
# Newton identities:
# p1=A
# p2=A^2-2B
# p3=A^3-3AB+3conj(A)
# p4=A^4-4A^2B+4|A|^2+2B^2-4
#
# Introduce u=|A|^2 in [0,16], v=Re(A^2), |v|<=u, v=u*t,
# t in [-1,1], and |B|<=6.
# We certify on this larger box, which contains all feasible root data.
# ------------------------------------------------------------------
xr,yr,Br = sp.symbols("xr yr Br", real=True)
A = xr + sp.I*yr
Ac = xr - sp.I*yr
p1=A
p2=A**2-2*Br
p3=A**3-3*A*Br+3*Ac
p4=A**4-4*A**2*Br+4*(xr**2+yr**2)+2*Br**2-4
def abs2(w): return sp.expand(w*sp.conjugate(w))
R1111 = sp.expand(
    1-c0 +
    (a1*abs2(p1)+a2*abs2(p2)+a3*abs2(p3)+a4*abs2(p4))/4
)

XX,YY = sp.symbols("XX YY", nonnegative=True)
uv,t = sp.symbols("uv t", real=True)
exprXY = sp.Poly(R1111.subs({xr**2:XX,yr**2:YY}),XX,YY,Br).as_expr()
exprUV = sp.expand(exprXY.subs({XX:(uv+sp.Symbol("vv"))/2,YY:(uv-sp.Symbol("vv"))/2}))
vv=sp.Symbol("vv", real=True)
# redo cleanly because Symbol identity matters
exprUV = sp.expand(exprXY.subs({XX:(uv+vv)/2,YY:(uv-vv)/2}))
exprUTB = sp.expand(exprUV.subs(vv,uv*t))

U,T,C = sp.symbols("U T C", real=True)
cube = sp.Poly(sp.expand(exprUTB.subs({
    uv:16*U,
    t:2*T-1,
    Br:12*C-6
})),U,T,C)
degs=(cube.degree(U),cube.degree(T),cube.degree(C))
B1111=power_to_bernstein_3d(cube.as_expr(),U,T,C,degs)
C1111=cert3(B1111,degs)

print("=== exact boundary P70 toy certificate ===")
print("base objective without boundary term:", base)
print("mu =", mu)
print("certified B_70 threshold =", B70, "=", float(B70))
print("objective at B70 =", sp.simplify(base+B70*mu))
print()
print("(2,2) certificate:", C22)
print("(2,1,1) certificate:", C211)
print("(1,1,1,1) certificate:", C1111)
print()
print("Conclusion:")
print("For every B <= B70, dual objective >= 0.7 and all configuration patterns satisfy")
print("the exact rational configuration-wise inequality.")
print("Therefore p_min(B) >= 0.70 in this N=4 toy model.")

assert sp.simplify(base+B70*mu) == sp.Rational(7,10)
assert C22[3] > 0
assert C211[3] > 0
assert C1111[3] > 0
