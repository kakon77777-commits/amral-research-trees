# 11｜Exact Census Gate Definitions

## G0 — Rank-zero object gate

Required in the strict first pool:

\[
r_{\rm alg}=r_{\rm an}=0.
\]

LMFDB fields:

```text
ec_curvedata.rank
ec_curvedata.analytic_rank
```

## G1 — No-rational-2-torsion cheap branch

Strict first pool uses:

```text
torsion = 1
```

This is stronger than necessary, but gives the cleanest Banwait–Huang branch.

## G2 — Numeric \(2\)-part parity prefilter

Require:

```text
sha_an = 1
Tamagawa product odd
torsion = 1
```

This makes the stored analytic quotient have odd \(2\)-adic parity.

It is **not** a proof of:

\[
\operatorname{BSD}(E,2).
\]

Therefore every row exits SQL with:

```text
base_bsd2_status = PENDING
```

unless an independent certificate is later attached.

## G3 — Family-uniform odd-additive period gate

For the strict first theorem pool:

```text
every odd additive p >= 11
kodaira_symbol not in (2,3,4)
```

This is a conservative Edixhoven-safe subclass.

The LMFDB local-data coding is used directly; do not translate it by memory
inside the SQL.

## G4 — Fixed multiplicative leave-one-out graph

For every odd multiplicative bad prime \(p\), require:

\[
\exists \ell\neq p,\quad
\ell\text{ multiplicative},\quad
p\nmid v_\ell(\Delta_E).
\]

This is a theorem gate, not a heuristic.

## G5 — Nonsplit FW-H3 reservoir

Require at least one odd nonsplit multiplicative prime.

For every fixed odd additive \(p\), require a nonsplit witness \(\ell\) with:

\[
p\nmid v_\ell(\Delta_E).
\]

The postprocessor also computes:

\[
g_-=\gcd_{\ell\in\mathcal M^-}v_\ell(\Delta_E)
\]

and the finite exceptional set \(R_-\).

## G6 — Clean residual image

The strict first pool excludes odd `nonmax_primes`.

This is deliberately stronger than the final theorem needs.

Reason:

- it removes rational odd-isogeny/Eisenstein branches from the first census;
- it does **not** solve local FW-H2 at an additive prime.

## G7 — Local additive H2

Always:

```text
PENDING
```

until certified by the v0.3 local p-isogeny compiler.

## G8 — Final theorem gate

Only promote to `PROVED_FAMILY` after:

```text
BSD(E,2) PROVED
all fixed additive H2 PASS
all finite R_mult exceptions routed
all finite R_minus exceptions routed
Chebotarev support compatibility proved
```

No SQL row alone proves a family theorem.
