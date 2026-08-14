#!/usr/bin/env python3
"""
Continuous-position column generation for the small-N PairCeiling toy model.

Research code, not a proof artifact.

Primal:
    min sum_c w_c p_c
s.t.
    sum_c w_c = 1
    sum_c w_c S_c(j) = j/N,  j=1,...,N-1
    w_c >= 0

Dual:
    max y0 + sum_j (j/N) y_j
s.t.
    y0 + sum_j y_j S_c(j) <= p_c   for every configuration c

Set r_N(j/N) = N*y_j to obtain the discrete PairCeiling certificate form.

Pricing:
    minimize p(c) - y0 - sum_j y_j S_c(j)
over continuous marked configurations with marks in {1,2} and total
multiplicity N. Translation symmetry fixes the first point at x=0.

WARNING:
scipy.differential_evolution is numerical and does not certify a global
minimum. Use this to generate candidates; interval/SOS certification is a
separate research step.
"""
import argparse
import itertools
import numpy as np
from scipy.optimize import linprog, differential_evolution

def patterns(N):
    out=[]
    for twos in range(N//2 + 1):
        ones=N-2*twos
        out.append([2]*twos + [1]*ones)
    return out

def form_factor(marks, xs, N):
    marks=np.asarray(marks,float)
    xs=np.asarray(xs,float)
    return np.array([
        abs(np.sum(marks*np.exp(2j*np.pi*j*xs)))**2/N
        for j in range(1,N)
    ])

def simple_fraction(marks,N):
    return sum(m==1 for m in marks)/N

def pricing(marks, dual, N, seed=0, maxiter=500):
    p=simple_fraction(marks,N)
    if len(marks)==1:
        xs=np.array([0.0])
        S=form_factor(marks,xs,N)
        return p-(dual[0]+dual[1:]@S),xs,S
    def f(z):
        xs=np.r_[0.0,z]
        S=form_factor(marks,xs,N)
        return p-(dual[0]+dual[1:]@S)
    r=differential_evolution(
        f,[(0,1)]*(len(marks)-1),
        seed=seed,popsize=14,maxiter=maxiter,
        tol=1e-10,polish=True
    )
    xs=np.r_[0.0,r.x]
    return r.fun,xs,form_factor(marks,xs,N)

def solve_master(columns,N):
    c=np.array([col["p"] for col in columns])
    F=np.array([col["S"] for col in columns])
    Aeq=np.vstack([np.ones(len(columns)),F.T])
    beq=np.r_[1.0,np.arange(1,N)/N]
    return linprog(c,A_eq=Aeq,b_eq=beq,bounds=(0,None),method="highs")

def add_column(columns,marks,xs,N):
    columns.append({
        "marks":tuple(marks),
        "xs":tuple(float(x) for x in xs),
        "p":simple_fraction(marks,N),
        "S":form_factor(marks,xs,N)
    })

def regular_seed_columns(N):
    # A small heuristic seed set; for hard cases add more random/grid columns.
    cols=[]
    xs=np.arange(N)/N
    add_column(cols,[1]*N,xs,N)
    rng=np.random.default_rng(1)
    for pat in patterns(N):
        if pat==[1]*N: continue
        for _ in range(max(30,5*N)):
            z=np.sort(rng.random(len(pat)))
            z=(z-z[0])%1.0
            add_column(cols,pat,z,N)
    return cols

def run(N,outer=40,seeds=4):
    columns=regular_seed_columns(N)
    # seed pool may not be feasible; keep adding random columns until it is
    rng=np.random.default_rng(10)
    res=solve_master(columns,N)
    tries=0
    while not res.success and tries<50:
        for pat in patterns(N):
            z=np.sort(rng.random(len(pat)))
            z=(z-z[0])%1.0
            add_column(columns,pat,z,N)
        tries+=1
        res=solve_master(columns,N)
    if not res.success:
        raise RuntimeError("Initial restricted master is infeasible. Add a grid seed pool.")

    for it in range(outer):
        res=solve_master(columns,N)
        dual=res.eqlin.marginals
        best=None
        for pat in patterns(N):
            for s in range(seeds):
                rc,xs,S=pricing(pat,dual,N,seed=1000+97*it+17*s+len(pat))
                cand=(rc,pat,xs,S)
                if best is None or rc<best[0]:
                    best=cand
        print(it,"master",res.fun,"best reduced cost",best[0],"pattern",best[1])
        if best[0] >= -1e-7:
            break
        add_column(columns,best[1],best[2],N)

    res=solve_master(columns,N)
    print("candidate floor:",res.fun)
    print("dual:",res.eqlin.marginals)
    print("rescaled r samples:",N*res.eqlin.marginals[1:])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,default=4)
    ap.add_argument("--outer",type=int,default=30)
    ap.add_argument("--seeds",type=int,default=4)
    a=ap.parse_args()
    run(a.N,a.outer,a.seeds)
