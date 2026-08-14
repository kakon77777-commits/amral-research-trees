#!/usr/bin/env python3
"""Independent finite regression checks for exact formulas used in the series.
These tests do not prove the global Collatz conjecture; they only test finite/algebraic claims.
"""
from fractions import Fraction
from math import comb, log, floor
import json, sys

def F_word(word,x,m=3,r=1):
    y=Fraction(x)
    for c in word:
        y = y/2 if c=='D' else (m*y+r)/2
    return y

def affine_data(word,m=3,r=1):
    b=0; u=0
    for j,c in enumerate(word):
        if c=='U': b=m*b+r*(2**j); u+=1
    return u,b

def residue(word,m=3,r=1):
    k=len(word); u,b=affine_data(word,m,r)
    return (-b*pow(m,-u,2**k))%(2**k)

def actual_word(n,k,m=3,r=1):
    out=[]; x=n
    for _ in range(k):
        if x%2==0: out.append('D'); x//=2
        else: out.append('U'); x=(m*x+r)//2
    return ''.join(out),x

def words(k):
    for i in range(2**k):
        yield ''.join('U' if (i>>(k-1-j))&1 else 'D' for j in range(k))

def test_p02_p03(maxk=9):
    checked=0
    for k in range(1,maxk+1):
        seen=set()
        for w in words(k):
            u,b=affine_data(w); r0=residue(w)
            assert r0 not in seen; seen.add(r0)
            # formal affine formula + admissible cylinder + transport
            for a in range(0,4):
                n=r0+(2**k)*a
                if n<=0: continue
                aw,y=actual_word(n,k)
                assert aw==w
                assert Fraction(y)==F_word(w,n)
                m0=F_word(w,r0)
                assert m0.denominator==1
                assert y==m0.numerator+(3**u)*a
                checked+=1
        assert len(seen)==2**k
    return checked

def test_p02_extrema(maxk=9):
    checked=0
    for k in range(1,maxk+1):
      for u in range(k+1):
        vals=[]
        for w in words(k):
          if w.count('U')==u: vals.append(affine_data(w)[1])
        if not vals: continue
        bmin=3**u-2**u
        bmax=(2**(k-u))*(3**u-2**u)
        assert min(vals)==bmin and max(vals)==bmax
        checked+=1
    return checked

def test_p05_counts():
    alpha=log(2)/log(3)
    expected={8:(5,219),12:(7,3302),16:(10,58651),20:(12,910596)}
    for k,(mexp,aexp) in expected.items():
        m=floor(alpha*k); A=sum(comb(k,u) for u in range(m+1))
        assert (m,A)==(mexp,aexp)
    D=alpha*log(alpha/0.5)+(1-alpha)*log((1-alpha)/0.5)
    assert abs(D-0.03468818523201744)<1e-14
    # Exact direct 16-block benchmark on 1 <= n < 2^20.
    k=16; N=2**20
    strict=eq=0
    for n in range(1,N):
        _,y=actual_word(n,k)
        if y<n: strict+=1
        elif y==n: eq+=1
    assert strict==938_413 and eq==2
    return {'alpha':alpha,'KL':D,'k16_strict':strict,'k16_equality':eq}

def accelerated_formula(kappas,n):
    x=n
    for kap in kappas:
        x=Fraction(3*x+1,2**kap)
    K=sum(kappas); m=len(kappas)
    B=sum((3**(m-i))*2**sum(kappas[:i-1]) for i in range(1,m+1))
    return x, Fraction((3**m)*n+B,2**K),B

def test_p06(maxm=5):
    checked=0
    from itertools import product
    for m in range(1,maxm+1):
      for ks in product(range(1,5), repeat=m):
        x,y,B=accelerated_formula(ks,1)
        assert x==y
        checked+=1
    return checked

def test_p07(maxk=7):
    checked=0
    for m in [1,3,5,7,9]:
      for r in [1,3,5]:
        for k in range(1,maxk+1):
          seen=set()
          for w in words(k):
            u,b=affine_data(w,m,r); rr=residue(w,m,r)
            assert rr not in seen; seen.add(rr)
            for a in range(0,3):
              n=rr+2**k*a
              if n<=0: continue
              aw,y=actual_word(n,k,m,r)
              assert aw==w
              assert Fraction(y)==F_word(w,n,m,r)
              base=F_word(w,rr,m,r)
              assert base.denominator==1 and y==base.numerator+(m**u)*a
              checked+=1
          assert len(seen)==2**k
    # m=1 special boundary
    for k in range(1,8):
      assert all(1**w.count('U')<2**k for w in words(k))
    return checked

def hard_height(word):
    vals=[]
    for j in range(1,len(word)+1):
      u,b=affine_data(word[:j]); delta=2**j-3**u
      if delta>0: vals.append(b//delta)
    return min(vals) if vals else None

def test_p09(maxk=9):
    checked=0
    for k in range(1,maxk+1):
      for w in words(k):
        h=hard_height(w); r0=residue(w)
        for a in range(0,8):
          n=r0+2**k*a
          if n<=0: continue
          aw,_=actual_word(n,k)
          assert aw==w
          hard=True; x=n
          for j in range(1,k+1):
            _,x=actual_word(n,j)
            if x<n: hard=False; break
          predicted=(True if h is None else n<=h)
          assert hard==predicted
          checked+=1
    return checked

def main():
    out={'status':'PASS','scope':'finite algebraic/regression checks only; not a global Collatz proof','tests':{}}
    out['tests']['p02_p03_affine_residue_transport']={'status':'PASS','cases':test_p02_p03()}
    out['tests']['p02_correction_extrema']={'status':'PASS','cases':test_p02_extrema()}
    out['tests']['p05_binomial_and_k16_benchmark']={'status':'PASS',**test_p05_counts()}
    out['tests']['p06_accelerated_affine_formula']={'status':'PASS','cases':test_p06()}
    out['tests']['p07_generalized_mxr']={'status':'PASS','cases':test_p07()}
    out['tests']['p09_hard_height']={'status':'PASS','cases':test_p09()}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
