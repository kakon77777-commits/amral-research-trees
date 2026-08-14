#!/usr/bin/env python3
"""
Diagnostics for the generalized one-delta optimizer:
- q(sigma)
- Fourier autocorrelation mass in |alpha|>1
- P70 support/error slack.

Numerical research utility, not a proof certificate.
"""
import math
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def metrics(sigma,n=1600):
    h=sigma/n
    maxlag=min(n-1,int(math.floor((1-1e-14)/h)))
    offs=np.arange(-maxlag,maxlag+1)
    vals=[]
    for lag in offs:
        k=max(1-abs(lag)*h,0.0)
        a=np.full(n-abs(lag),-h*k)
        if lag==0:
            a+=1
        vals.append(a)
    A=diags(vals,offs,shape=(n,n),format="csr")
    one=np.ones(n)
    g=spsolve(A,one)
    K=h*g.sum()
    f=g/K
    corr=np.correlate(f,f,mode="full")*h
    lags=np.arange(-(n-1),n)*h
    f2=h*np.sum(f*f)
    inside=np.abs(lags)<=1
    outside=np.abs(lags)>1
    inside_alpha=h*np.sum(np.abs(lags[inside])*corr[inside])
    outside_mass=h*np.sum(corr[outside])
    C=f2+inside_alpha+outside_mass
    q=2-C
    return q,outside_mass

if __name__=="__main__":
    for s in [1.042628,1.05,1.06,1.257848,1.701455,2.26079,4.187215]:
        q,m=metrics(s)
        print(
            f"sigma={s:.6f} q={q:.8f} "
            f"unknown-strip-mass={m:.8f} ({100*m:.4f}%)"
        )
