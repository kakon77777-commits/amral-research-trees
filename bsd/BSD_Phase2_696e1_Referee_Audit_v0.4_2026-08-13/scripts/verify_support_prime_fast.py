#!/usr/bin/env python3
"""Fast support-prime verifier for the 696.e1 derived-family candidate."""
import sys

def legendre(a,p):
    a%=p
    if a==0:return 0
    r=pow(a,(p-1)//2,p)
    return -1 if r==p-1 else r

def pmul(A,B,p):
    t=[0]*5
    for i,a in enumerate(A):
        for j,b in enumerate(B):
            t[i+j]=(t[i+j]+a*b)%p
    for k in (4,3):
        c=t[k]%p
        if c:
            t[k]=0
            t[k-1]=(t[k-1]-c)%p
            t[k-2]=(t[k-2]-8*c)%p
            t[k-3]=(t[k-3]+16*c)%p
    return t[:3]

def ppow_x(n,p):
    r=[1,0,0]; b=[0,1,0]
    while n:
        if n&1:r=pmul(r,b,p)
        b=pmul(b,b,p); n//=2
    return r

def deg(a,p):
    for i in range(len(a)-1,-1,-1):
        if a[i]%p:return i
    return -1

def pmod(a,b,p):
    a=[x%p for x in a]; b=[x%p for x in b]
    db=deg(b,p)
    while deg(a,p)>=db:
        da=deg(a,p)
        c=a[da]*pow(b[db],p-2,p)%p
        s=da-db
        for i in range(db+1):
            a[i+s]=(a[i+s]-c*b[i])%p
        while a and a[-1]%p==0:a.pop()
    return a or [0]

def pgcd(a,b,p):
    while deg(b,p)>=0:
        r=pmod(a,b,p); a,b=b,r
        if deg(b,p)<0:break
    return a

def irreducible(q):
    xq=ppow_x(q,q)
    h=[xq[0],(xq[1]-1)%q,xq[2]]
    f=[-16%q,8%q,1,1]
    return deg(pgcd(f,h,q),q)==0

def eligible(q):
    return q%24==1 and q!=29 and legendre(q,29)==1 and irreducible(q)

for s in sys.argv[1:]:
    q=int(s)
    print(q, eligible(q))
