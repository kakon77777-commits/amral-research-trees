#!/usr/bin/env python3
# Exact finite-field certificate for E=389a1 at p=11.
# Pure Python + NumPy. No network, no floating point arithmetic in proof-critical steps.

import json, math, hashlib, sys
from fractions import Fraction
from pathlib import Path
import numpy as np

N = 389
P = 11
INF = N
A2 = -2
A3 = -2
A5 = -3
TARGET_HEC = {2:-2, 3:-2, 5:-3, 7:-5, 13:-3, 17:-6, 19:5}


def norm_pair(c, d):
    c %= N; d %= N
    if c == 0:
        if d == 0:
            raise ValueError('zero pair')
        return INF
    return (d * pow(c, -1, N)) % N


def pair_of(x):
    return (0, 1) if x == INF else (1, x)

S = np.array([[0,-1],[1,0]], dtype=object)
R = np.array([[0,-1],[1,-1]], dtype=object)


def act(x, M):
    c,d = pair_of(x)
    return norm_pair(c*int(M[0,0]) + d*int(M[1,0]),
                     c*int(M[0,1]) + d*int(M[1,1]))


def rref_mod(A, p=P):
    A = np.array(A, dtype=np.int64) % p
    m,n = A.shape
    pivots=[]; r=0
    for c in range(n):
        if r >= m: break
        nz = np.flatnonzero(A[r:,c] % p)
        if len(nz) == 0: continue
        i = r + int(nz[0])
        if i != r: A[[r,i]] = A[[i,r]]
        inv = pow(int(A[r,c]), -1, p)
        A[r] = (A[r] * inv) % p
        idx = np.flatnonzero(A[:,c] % p)
        idx = idx[idx != r]
        if len(idx):
            fac = A[idx,c].copy()
            A[idx] = (A[idx] - fac[:,None] * A[r]) % p
        pivots.append(c); r += 1
    return A, pivots


def nullspace_basis_from_rref(rr, pivots, p=P):
    n = rr.shape[1]
    pset=set(pivots)
    free=[j for j in range(n) if j not in pset]
    out=[]
    for f in free:
        v=np.zeros(n,dtype=np.int64); v[f]=1
        for row,pc in enumerate(pivots):
            v[pc]=(-int(rr[row,f]))%p
        out.append(v)
    return out, free


def ap_curve(q):
    # E: y^2 + y = x^3 + x^2 - 2x.
    if q == 2:
        cnt=1
        for x in range(q):
            rhs=(x**3+x**2-2*x)%q
            for y in range(q):
                if (y*y+y-rhs)%q == 0: cnt += 1
        return q+1-cnt
    s=0
    for x in range(q):
        rhs=(x**3+x**2-2*x)%q
        D=(1+4*rhs)%q
        if D==0: chi=0
        else:
            v=pow(D,(q-1)//2,q)
            chi=1 if v==1 else -1
        s += chi
    return -s


def cf_of(fr):
    if fr is None: raise ValueError('infinity has no CF')
    a,b=fr.numerator,fr.denominator
    out=[]
    while b:
        q=a//b
        out.append(q)
        a,b=b,a-q*b
    return out


def convergents(fr):
    cf=cf_of(fr)
    pm2,pm1=0,1; qm2,qm1=1,0
    out=[]
    for a in cf:
        p=a*pm1+pm2; q=a*qm1+qm2
        out.append((p,q))
        pm2,pm1=pm1,p; qm2,qm1=qm1,q
    return out


def raw_edge(alpha, beta):
    # alpha,beta are None (=infinity) or Fraction. Returns Manin generator index and sign.
    if alpha is None: p1,q1=1,0
    else: p1,q1=alpha.numerator,alpha.denominator
    if beta is None: p2,q2=1,0
    else: p2,q2=beta.numerator,beta.denominator
    det=p2*q1-p1*q2
    if det == 1:
        return norm_pair(q2,q1), 1
    if det == -1:
        return norm_pair(q1,q2), -1
    raise ValueError(f'not Farey adjacent: {alpha}, {beta}, det={det}')


def raw_m(fr):
    # {fr, infinity}; continued-fraction path and orientation.
    conv=convergents(fr)
    v=np.zeros(N+1,dtype=np.int64)
    prev=None
    for p,q in conv:
        cur=Fraction(p,q)
        idx,coef=raw_edge(prev,cur)
        v[idx]=(v[idx]+coef)%P
        prev=cur
    return (-v)%P


def m_raw_general(r):
    return np.zeros(N+1,dtype=np.int64) if r is None else raw_m(r)


def symbol_raw(r,s):
    return (m_raw_general(r)-m_raw_general(s))%P


def generator_endpoints(x):
    if x == INF: return Fraction(0), None
    if x == 0: return None, Fraction(0)
    return Fraction(-1,x), Fraction(0)


def mul_q(r,q): return None if r is None else r*q

def div_affine(r,i,q): return None if r is None else (r+i)/q


def hecke_raw_generator(x,q):
    r,s=generator_endpoints(x)
    v=symbol_raw(mul_q(r,q),mul_q(s,q))
    for i in range(q):
        v=(v+symbol_raw(div_affine(r,i,q),div_affine(s,i,q)))%P
    return v


def hecke_constraints(q,a):
    out=[]
    for x in range(N+1):
        v=hecke_raw_generator(x,q).copy()
        v[x]=(v[x]-a)%P
        out.append(v)
    return out


def build_certificate_line():
    rows=[]
    for x in range(N+1):
        row=np.zeros(N+1,dtype=np.int64)
        row[x]=(row[x]+1)%P; row[act(x,S)]=(row[act(x,S)]+1)%P
        rows.append(row)
        row=np.zeros(N+1,dtype=np.int64)
        y=act(x,R); z=act(y,R)
        row[x]=(row[x]+1)%P; row[y]=(row[y]+1)%P; row[z]=(row[z]+1)%P
        rows.append(row)
    rr_rel,piv_rel=rref_mod(rows)
    quotient_dim=(N+1)-len(piv_rel)

    rows_eig=list(rows)
    for q in (2,3,5):
        rows_eig.extend(hecke_constraints(q, ap_curve(q)))
    rr_eig,piv_eig=rref_mod(rows_eig)
    eig_nullity=(N+1)-len(piv_eig)

    rows_plus=list(rows_eig)
    for x in range(N+1):
        y=INF if x==INF else (-x)%N
        row=np.zeros(N+1,dtype=np.int64)
        row[y]=(row[y]+1)%P; row[x]=(row[x]-1)%P
        rows_plus.append(row)
    rr_plus,piv_plus=rref_mod(rows_plus)
    basis,free=nullspace_basis_from_rref(rr_plus,piv_plus)
    if len(basis)!=1:
        raise AssertionError(f'expected 1D plus Hecke eigenline, got {len(basis)}')
    lam=basis[0]
    # deterministic normalization: unique free coordinate is 1.
    return lam, {
        'manin_relation_rank_mod_11': len(piv_rel),
        'manin_quotient_dimension_mod_11': quotient_dim,
        'hecke_eigenspace_nullity_before_plus': eig_nullity,
        'plus_hecke_eigenspace_dimension': len(basis),
        'normalizing_free_index': int(free[0]),
        'lambda_nonzero_count': int(np.count_nonzero(lam%P)),
        'lambda_at_infinity': int(lam[INF]%P),
    }


def check_hecke_lambda(lam,q,a):
    bad=[]
    for x in range(N+1):
        v=hecke_raw_generator(x,q)%P
        lhs=int(np.dot(v,lam)%P)
        rhs=int((a*int(lam[x]))%P)
        if lhs!=rhs:
            bad.append((x,lhs,rhs))
            if len(bad)>=5: break
    return not bad, bad


def factor_int(n):
    f=[]; d=2
    while d*d<=n:
        if n%d==0:
            e=0
            while n%d==0: n//=d; e+=1
            f.append((d,e))
        d=3 if d==2 else d+2
    if n>1: f.append((n,1))
    return f


def is_primitive_root(g,l):
    if pow(g,l-1,l)!=1: return False
    for q,e in factor_int(l-1):
        if pow(g,(l-1)//q,l)==1: return False
    return True


def log_table(ell,g):
    if not is_primitive_root(g,ell): raise ValueError(f'{g} not primitive mod {ell}')
    logs=[0]*ell; x=1
    for e in range(ell-1):
        logs[x]=e%P; x=(x*g)%ell
    if x!=1: raise AssertionError('log cycle')
    return logs


def modular_symbol_positive_fast(lam,a,n):
    # evaluates Neron-scalar-ambiguous plus eigensymbol on {a/n, infinity}
    if not (0<a<n and math.gcd(a,n)==1):
        raise ValueError('requires reduced 0<a<n')
    num=a; den=n; cf=[]
    while den:
        q=num//den; cf.append(q); num,den=den,num-q*den
    pm2,pm1=0,1; qm2,qm1=1,0
    prev_p,prev_q=1,0
    total=0
    for A in cf:
        pp=A*pm1+pm2; qq=A*qm1+qm2
        det=pp*prev_q-prev_p*qq
        if det==1:
            idx=norm_pair(qq,prev_q); coef=1
        elif det==-1:
            idx=norm_pair(prev_q,qq); coef=-1
        else:
            raise AssertionError(f'bad det {det}')
        total = (total - coef*int(lam[idx]))%P
        prev_p,prev_q=pp,qq
        pm2,pm1=pm1,pp; qm2,qm1=qm1,qq
    return total%P


def delta_pair(lam,l1,l2,g1,g2):
    n=l1*l2
    L1=log_table(l1,g1); L2=log_table(l2,g2)
    total=0
    for a in range(1,n):
        if a%l1==0 or a%l2==0: continue
        ms=modular_symbol_positive_fast(lam,a,n)
        total=(total + ms*L1[a%l1]*L2[a%l2])%P
    return total


def is_kolyvagin_prime(ell):
    a=ap_curve(ell)
    return ((ell-1)%P==0 and (a-ell-1)%P==0), a


def main():
    lam, meta=build_certificate_line()
    ap={q:ap_curve(q) for q in sorted(TARGET_HEC)}
    for q,expected in TARGET_HEC.items():
        if ap[q]!=expected:
            raise AssertionError(f'a_{q}={ap[q]} != expected {expected}')
    hecke={}
    for q,a in ap.items():
        ok,bad=check_hecke_lambda(lam,q,a)
        hecke[str(q)]={'a_q':a,'pass':ok,'bad':bad}
        if not ok: raise AssertionError(f'Hecke T_{q} failed: {bad}')

    kol=[]
    for ell,g in ((397,5),(991,6),(1321,13)):
        ok,a=is_kolyvagin_prime(ell)
        kol.append({'ell':ell,'a_ell':a,'primitive_root':g,'condition_pass':ok,
                    'ell_minus_1_mod_11':(ell-1)%P,
                    'a_ell_minus_ell_minus_1_mod_11':(a-ell-1)%P})
        if not ok: raise AssertionError(f'{ell} not Kolyvagin')
        if not is_primitive_root(g,ell): raise AssertionError(f'bad primitive root {g} mod {ell}')

    d=delta_pair(lam,397,991,5,6)
    if d==0: raise AssertionError('target Kurihara witness unexpectedly zero')

    result={
      'schema_version':'0.2',
      'curve':{
        'lmfdb_label':'389.a1','cremona_label':'389a1',
        'equation':'y^2 + y = x^3 + x^2 - 2*x','conductor':389,
        'algebraic_rank_external':2,'torsion_order_external':1,
      },
      'prime':11,
      'finite_field':'F_11',
      'proof_critical_arithmetic':'exact_integer_and_finite_field_only',
      'manin_symbol_line':meta,
      'point_count_coefficients':{str(k):v for k,v in ap.items()},
      'hecke_validation':hecke,
      'kolyvagin_primes':kol,
      'witness':{
        'ell_1':397,'ell_2':991,'n':397*991,
        'primitive_roots':[5,6],
        'delta_lambda_mod_11':int(d),
        'invariant_nonzero':True,
        'normalization_note':'The exact residue depends on the nonzero scalar chosen for the one-dimensional plus Hecke eigenline and on primitive generators; vanishing/nonvanishing is invariant.'
      },
      'canonical_bridge':{
        'status':'closed_via_Kim_Corollary_1_6_plus_1D_eigenline',
        'reason':'Kim Corollary 1.6 gives nonvanishing of the canonical Kurihara collection at good ordinary p=11 under surjectivity and Manin p-unit hypotheses. Hence the canonical mod-11 plus modular-symbol vector is nonzero. The computed relevant plus Hecke eigenspace is one-dimensional, so the canonical vector differs from lambda by a unit in F_11.',
        'external_theorem_input':'Chan-Ho Kim, arXiv:2203.12159v6, Corollary 1.6 and Theorem 1.8'
      },
      'theorem_chain_conclusion':{
        'kim_order_upper_bound_from_witness':2,
        'mordell_weil_rank_lower_bound_external':2,
        'selmer_corank':2,
        'partial_2':0,
        'partial_infinity':0,
        'selmer_mod_div_length':0,
        'selmer_is_divisible_corank_2':True,
        'sha_specific_conditional_clause_used':False,
        'sha_11_infinity_finite':True,
        'sha_11_infinity_length':0,
        'sha_11_infinity_trivial':True,
        'scope':'one-prime p=11 Sha closure only; not full BSD and not by itself the p=11 leading-term identity'
      }
    }
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(text,encoding='utf-8',newline='\n')
    print(text,end='')

if __name__=='__main__': main()
