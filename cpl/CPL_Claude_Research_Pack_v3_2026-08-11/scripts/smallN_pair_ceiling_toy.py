#!/usr/bin/env python3
"""
Small-N toy LP for the bandwidth-one ceiling mechanism.

NOT the Anthropic N=256 exact-rational LP.

Toy configuration class:
  - M equally spaced circle sites
  - occupancy n_k in {0,1,2}
  - sum n_k = N
  - simple fraction = # {k:n_k=1} / N
  - S(j)=|Σ n_k exp(2π i j k/M)|²/N

The LP mixes configurations and minimizes expected simple fraction subject to
open-band CUE rows E[S(j)] = j/N, j=1,...,N-1.

Optional:
  --edge-cap B  adds E[S(N)] <= B
  --max-row J   enforces E[S(j)] = min(j/N,1) for j<=J

Use small N first. Brute-force enumeration grows quickly.
"""
import argparse
import numpy as np
from scipy.optimize import linprog

def configs(N,M):
    out=[]; cur=[0]*M
    def rec(i,rem):
        if i==M:
            if rem==0: out.append(tuple(cur))
            return
        for v in range(min(2,rem)+1):
            cur[i]=v; rec(i+1,rem-v)
        cur[i]=0
    rec(0,N)
    return out

def solve(N,M,max_row=None,edge_cap=None):
    if max_row is None: max_row=N-1
    rows=list(range(1,max_row+1))
    C=configs(N,M)
    k=np.arange(M)
    F=np.empty((len(C),len(rows))); p=np.empty(len(C)); edge=np.empty(len(C))
    roots={j:np.exp(2j*np.pi*j*k/M) for j in set(rows+[N])}
    for i,c in enumerate(C):
        occ=np.asarray(c,float)
        p[i]=np.count_nonzero(occ==1)/N
        for t,j in enumerate(rows):
            F[i,t]=abs(np.dot(occ,roots[j]))**2/N
        edge[i]=abs(np.dot(occ,roots[N]))**2/N
    Aeq=np.vstack([np.ones(len(C)),F.T])
    beq=np.r_[1.0,[min(j/N,1.0) for j in rows]]
    kw={}
    if edge_cap is not None:
        kw["A_ub"]=np.array([edge]); kw["b_ub"]=np.array([edge_cap])
    r=linprog(p,A_eq=Aeq,b_eq=beq,bounds=(0,None),method="highs",**kw)
    return r

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,default=4)
    ap.add_argument("--M",type=int,default=24)
    ap.add_argument("--max-row",type=int,default=None)
    ap.add_argument("--edge-cap",type=float,default=None)
    a=ap.parse_args()
    r=solve(a.N,a.M,a.max_row,a.edge_cap)
    print("success:",r.success)
    if r.success:
        print("min simple fraction:",r.fun)
        print("percent:",100*r.fun)
