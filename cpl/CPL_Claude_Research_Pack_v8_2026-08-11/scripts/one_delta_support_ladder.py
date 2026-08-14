#!/usr/bin/env python3
"""
Numerically reconstruct the generalized Montgomery–Taylor / CCLM one-delta
support ladder.

The model:
  I_sigma = [-sigma/2, sigma/2]
  (T_sigma f)(t) = ∫ (1-|t-u|)_+ f(u) du
  A_sigma = I - T_sigma

For the one-delta extremal problem,
  m(sigma) = 1 / <1, A_sigma^{-1} 1>
and the corresponding simple-zero integrality certificate is
  q(sigma) = 1 - m(sigma).

This script uses midpoint Nyström discretization and sparse solves.
It is numerical research code, not a proof certificate.
"""
import argparse, math
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from scipy.optimize import brentq

def q_sigma(sigma, n=1200):
    h=sigma/n
    maxlag=min(n-1,int(math.floor((1-1e-14)/h)))
    offsets=np.arange(-maxlag,maxlag+1)
    vals=[]
    for lag in offsets:
        kval=max(1-abs(lag)*h,0.0)
        a=np.full(n-abs(lag),-h*kval)
        if lag==0:
            a=a+1.0
        vals.append(a)
    A=diags(vals,offsets,shape=(n,n),format="csr")
    v=np.full(n,math.sqrt(h))
    sol=spsolve(A,v)
    K00=float(v@sol)
    return 1-1/K00

def threshold(target,n=1200):
    brackets={
        .70:(1,1.1),
        .80:(1.1,1.5),
        .90:(1.5,2.0),
        .95:(2,3),
        .99:(3,6),
    }
    a,b=brackets[target]
    return brentq(lambda s:q_sigma(s,n)-target,a,b,xtol=2e-9)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=1200)
    args=ap.parse_args()
    for t in [.70,.80,.90,.95,.99]:
        s=threshold(t,args.n)
        print(f"{100*t:.1f}%  sigma ~= {s:.10f}")
