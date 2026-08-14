#!/usr/bin/env python3
"""
Exact-rational Bernstein certificate for the N=4 open-band PairCeiling toy.

Requires sympy only.
All final Bernstein arithmetic is exact rational arithmetic.
"""
from fractions import Fraction
import math
import sympy as sp

c0 = sp.Rational(99998,100000)
y1 = -sp.Rational(42763734,10**8)
y2 = -sp.Rational(25119857,10**8)
y3 = -sp.Rational(9234705,10**8)
a1,a2,a3 = -y1,-y2,-y3

objective = c0 + sp.Rational(1,4)*y1 + sp.Rational(1,2)*y2 + sp.Rational(3,4)*y3

def to_frac(q):
    return Fraction(int(q.p),int(q.q))

def split1(c):
    n=len(c)-1
    levels=[list(c)]
    for _ in range(n):
        prev=levels[-1]
        levels.append([(prev[i]+prev[i+1])/2 for i in range(len(prev)-1)])
    left=[levels[k][0] for k in range(n+1)]
    right=[levels[n-k][k] for k in range(n+1)]
    return left,right

def certify_1d(B):
    stack=[(0,B)]
    internal=leaves=maxdepth=0
    min_terminal=None
    while stack:
        d,cfs=stack.pop()
        lb=min(cfs)
        if lb>=0:
            leaves+=1
            maxdepth=max(maxdepth,d)
            min_terminal=lb if min_terminal is None or lb<min_terminal else min_terminal
            continue
        L,R=split1(cfs)
        stack.append((d+1,L)); stack.append((d+1,R))
        internal+=1
    return internal,leaves,maxdepth,min_terminal

def split_x(M):
    nr,nc=len(M),len(M[0])
    L=[[Fraction(0) for _ in range(nc)] for __ in range(nr)]
    R=[[Fraction(0) for _ in range(nc)] for __ in range(nr)]
    for j in range(nc):
        l,r=split1([M[i][j] for i in range(nr)])
        for i in range(nr):
            L[i][j]=l[i]; R[i][j]=r[i]
    return L,R

def split_z(M):
    nr,nc=len(M),len(M[0])
    L=[[Fraction(0) for _ in range(nc)] for __ in range(nr)]
    R=[[Fraction(0) for _ in range(nc)] for __ in range(nr)]
    for i in range(nr):
        l,r=split1(M[i])
        L[i]=l; R[i]=r
    return L,R

def certify_2d(B):
    stack=[(0,0,B)]
    internal=leaves=maxdepth=0
    min_terminal=None
    while stack:
        dx,dz,M=stack.pop()
        lb=min(v for row in M for v in row)
        if lb>=0:
            leaves+=1
            maxdepth=max(maxdepth,dx+dz)
            min_terminal=lb if min_terminal is None or lb<min_terminal else min_terminal
            continue
        if dx<=dz:
            parts=split_x(M); nd=(dx+1,dz)
        else:
            parts=split_z(M); nd=(dx,dz+1)
        for Q in parts:
            stack.append((nd[0],nd[1],Q))
        internal+=1
    return internal,leaves,maxdepth,min_terminal

def power_to_bernstein_1d(P,var,n):
    poly=sp.Poly(P,var)
    aa=[poly.coeff_monomial(var**k) for k in range(n+1)]
    B=[]
    for i in range(n+1):
        s=sp.Rational(0)
        for k in range(i+1):
            s += aa[k]*sp.Rational(math.comb(i,k),math.comb(n,k))
        B.append(to_frac(s))
    return B

def power_to_bernstein_2d(P,X,Z,n,m):
    poly=sp.Poly(P,X,Z)
    aa={(k,l):poly.coeff_monomial(X**k*Z**l) for k in range(n+1) for l in range(m+1)}
    B=[]
    for i in range(n+1):
        row=[]
        for j in range(m+1):
            s=sp.Rational(0)
            for k in range(i+1):
                for l in range(j+1):
                    s += aa[(k,l)]*sp.Rational(math.comb(i,k),math.comb(n,k))*sp.Rational(math.comb(j,l),math.comb(m,l))
            row.append(to_frac(s))
        B.append(row)
    return B

# (2,2)
q,Q=sp.symbols("q Q", real=True)
S1=2+2*q
S2=2+2*(2*q**2-1)
S3=2+2*(4*q**3-3*q)
R22=sp.expand(-c0+a1*S1+a2*S2+a3*S3)
P22=sp.expand(R22.subs(q,2*Q-1))
B22=power_to_bernstein_1d(P22,Q,3)
C22=certify_1d(B22)

# (2,1,1)
x,z,X,Z=sp.symbols("x z X Z", real=True)
T={1:lambda q:q,2:lambda q:2*q**2-1,3:lambda q:4*q**3-3*q}
R211=sp.Rational(1,2)-c0
for j,a in [(1,a1),(2,a2),(3,a3)]:
    cv=T[j](z); cu=T[j](x)
    R211 += a*(1+cv**2+2*cv*cu)
P211=sp.expand(R211.subs({x:2*X-1,z:2*Z-1}))
B211=power_to_bernstein_2d(P211,X,Z,3,6)
C211=certify_2d(B211)

print("dual objective exact:", objective)
print("dual objective decimal:", float(objective))
print("percent:",100*float(objective))
print("(1,1,1,1): trivial valid")
print("(2,2):",C22)
print("(2,1,1):",C211)

assert C22[3] == Fraction(120357,25000000)
assert C211[3] == Fraction(195858711475181,34359738368000000000)
assert C22[3] > 0 and C211[3] > 0
