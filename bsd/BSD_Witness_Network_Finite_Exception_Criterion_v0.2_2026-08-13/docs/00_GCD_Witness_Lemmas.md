# 00 | GCD Witness Lemmas

For multiplicative bad primes \(\ell\), let
\[
n_\ell=v_\ell(\Delta_E).
\]

## Generic witness

For an odd prime \(p\) not itself in the multiplicative witness set:
\[
\exists\ell:\ p\nmid n_\ell
\iff
p\nmid\gcd_\ell n_\ell.
\]

Hence the only failures are the finitely many odd prime divisors of the gcd.

## Fixed multiplicative prime

For \(p\) itself multiplicative, the witness must be distinct:
\[
\exists\ell\neq p:\ p\nmid n_\ell.
\]

This is a finite leave-one-out check.

## Nonsplit FW witness

The same gcd lemma applies after restricting to nonsplit multiplicative
primes.  Its odd gcd divisors are the only primes at which the standard FW-H3
witness can fail.

This is the exact algebraic reason the all-prime witness problem is finite.
