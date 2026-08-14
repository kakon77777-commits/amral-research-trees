#!/usr/bin/env python3
import math

def H(lam):
    return 2.0 - 1.0/lam - lam/3.0

def Hd(lam):
    return (1.0 + H(lam))/2.0

def F(lam):
    return lam/(1.0 + lam*lam/3.0)

def cstar(lam):
    theta=lam/math.sqrt(2.0)
    return math.sqrt(2.0)*math.tan(theta)/(1.0 + theta*math.tan(theta))

def p_mt(lam):
    return 2.0 - 1.0/cstar(lam)

if __name__=='__main__':
    lam=1.0
    print(f'H(1)       = {H(lam):.12f}   [2/3 = {2/3:.12f}]')
    print(f'Hd(1)      = {Hd(lam):.12f}   [5/6 = {5/6:.12f}]')
    print(f'F(1)       = {F(lam):.12f}   [3/4 = {3/4:.12f}]')
    print(f'c*_1       = {cstar(lam):.12f}')
    print(f'1/c*_1     = {1/cstar(lam):.12f}')
    print(f'P_MT       = {p_mt(lam):.12f}')
    print(f'P_MT (%)   = {100*p_mt(lam):.9f}')
    print('\nC-targets from 2-C=q:')
    for q in (0.70,0.80,0.90,0.99,1.0):
        print(f'  q={q:.2f} -> C <= {2-q:.2f}')
    print('\nPaper-stated rough support targets:')
    print('  70% -> ~1.04')
    print('  80% -> ~1.26')
    print('  90% -> ~1.70')
    print('  99% -> NOT STATED; do not extrapolate')
