# BSD P5 v0.5: Cyclotomic IMC Closure and the Rank-2 Generalized Perrin--Riou Bridge

**Curve:** $E=389.a1$ over $\mathbb Q$  
**Prime:** $p=11$  
**Date:** 2026-08-14  
**Status:** theorem/reduction paper; not a proof of BSD

## Abstract

For the rank-$2$ elliptic curve

$$
E: y^2+y=x^3+x^2-2x
$$

and the prime $p=11$, the preceding project stage produced an exact Kurihara witness and a theorem-chain certificate

$$
\Sha(E/\mathbb Q)[11^\infty]=0.
$$

The purpose of the present stage is to isolate the remaining obstruction to the classical $11$-part of the Birch--Swinnerton-Dyer leading-term formula. The main new result of this audit is that the cyclotomic Iwasawa Main Conjecture is no longer an open gate for $(E,p)=(389.a1,11)$. The theorem of Burungale--Castella--Skinner applies, and its additional image condition is verified from maximal $11$-adic image by an explicit unipotent element. Combining this with the imported $11$-primary Shafarevich--Tate certificate closes the hypotheses needed for the Burns--Kurihara--Sano Iwasawa-to-Bockstein comparison.

Consequently, the remaining conceptual obstruction is not the Iwasawa main conjecture, not the $11$-primary Selmer structure, and not a global rationality assertion for the displayed real BSD quotient. It is the rank-$2$ Generalized Perrin--Riou comparison that changes derivative direction from a cyclotomic/Bockstein object to the complex rank-$2$ leading term and the Neron--Tate regulator. A second, finite computational gate is the nonvanishing of the $11$-adic Bockstein regulator; an exact SageMath replay is included.

## 1. Imported project state

The following are imported dependencies, not re-proved in this stage.

### 1.1 Exact one-prime Selmer certificate

The preceding stage constructed a Kurihara witness with

$$
n=397\cdot 991=393427
$$

and a nonzero residue on the relevant one-dimensional mod-$11$ plus Hecke eigenspace. Together with the Chan-Ho Kim Selmer structure theorem, the project certificate concludes

$$
\boxed{\Sha(E/\mathbb Q)[11^\infty]=0.}
$$

The machine-readable dependency is included as

```text
dependencies/389a1_p11_kurihara_certificate.json
```

This imported conclusion is only a statement about the $11$-primary part of $\Sha$. It is not the classical $11$-part leading-term formula and is not a proof of full BSD.

### 1.2 Curve data used in this stage

For $E=389.a1$, the exact database/certified-computation inputs used here are:

$$
N_E=389,
\qquad
\operatorname{rank}E(\mathbb Q)=2,
\qquad
E(\mathbb Q)_{\mathrm{tors}}=0,
$$

$$
\prod_\ell c_\ell=1,
\qquad
c_E^{\mathrm{Manin}}=1,
$$

and the $\ell$-adic Galois representation has maximal image for every prime $\ell$. The modular-form coefficient is

$$
a_{11}=-4.
$$

Since $11\nmid389$ and $11\nmid a_{11}$, the prime $11$ is a prime of good ordinary reduction.

## 2. The correct one-prime P5 target

The previous scalar formulation introduced

$$
\mathcal B_\infty(E)
=
\frac{L^{(2)}(E,1)/2!}
{\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)}.
$$

For a global strong-BSD identity, proving that this scalar belongs to a global algebraic field and then studying all of its local valuations is natural. For a single-prime closure, however, that is stronger than necessary.

Burns--Kurihara--Sano formulate the $p$-part as an equality of one-dimensional $\mathbb Z_p$-lattices inside a fixed $p$-adic realization. For the present curve, after using

$$
\#\Sha(E/\mathbb Q)[11^\infty]=1,
\qquad
\prod_\ell c_\ell=1,
\qquad
\#E(\mathbb Q)_{\mathrm{tors}}=1,
$$

the minimal classical target is

$$
\boxed{
L^*(E,1)\mathbb Z_{11}
=
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)\mathbb Z_{11}.
}
$$

Here

$$
L^*(E,1)=\frac{L^{(2)}(E,1)}{2!}.
$$

We denote this one-prime typed target by

$$
\boxed{\mathrm{P5\!\!-LAT}_{11}.}
$$

Thus the former gate $\mathrm{P5\!\!-RAT}$ is retained as a useful stronger global route, but it is no longer the minimal gate for the $11$-part.

## 3. Full cyclotomic Iwasawa Main Conjecture at $p=11$

### 3.1 External theorem

Burungale--Castella--Skinner prove the cyclotomic main conjecture for an elliptic curve over $\mathbb Q$ at a prime $p>3$ of good ordinary reduction under residual irreducibility. Their integral equality additionally uses the image condition

$$
(\mathrm{im}):
\quad
\exists\sigma\in G_{\mathbb Q}
\text{ fixing }\mathbb Q(\mu_{p^\infty})
\text{ such that }
T/(\sigma-1)T\simeq\mathbb Z_p.
$$

For $E=389.a1$ and $p=11$, good ordinarity and residual irreducibility are immediate from the curve data above. It remains to verify $(\mathrm{im})$.

### 3.2 Exact verification of condition $(\mathrm{im})$

Maximal $11$-adic image gives

$$
\rho_{E,11}(G_{\mathbb Q})=\operatorname{GL}_2(\mathbb Z_{11}).
$$

Choose

$$
u=
\begin{pmatrix}
1&1\\
0&1
\end{pmatrix}
\in\operatorname{SL}_2(\mathbb Z_{11}).
$$

Surjectivity gives an element $\sigma\in G_{\mathbb Q}$ with

$$
\rho_{E,11}(\sigma)=u.
$$

By the Weil pairing,

$$
\det\rho_{E,11}=\chi_{11},
$$

where $\chi_{11}$ is the $11$-adic cyclotomic character. Since

$$
\det u=1,
$$

we have

$$
\chi_{11}(\sigma)=1.
$$

Therefore $\sigma$ fixes the full cyclotomic extension $\mathbb Q(\mu_{11^\infty})$.

With respect to a basis $e_1,e_2$ of $T\simeq\mathbb Z_{11}^2$,

$$
(u-1)e_1=0,
\qquad
(u-1)e_2=e_1.
$$

Hence

$$
(u-1)T=\mathbb Z_{11}e_1
$$

and therefore

$$
T/(u-1)T\simeq\mathbb Z_{11}.
$$

This proves $(\mathrm{im})$.

### 3.3 Theorem-chain conclusion

The hypotheses of the Burungale--Castella--Skinner cyclotomic theorem are therefore satisfied for $(389.a1,11)$, and we may record

$$
\boxed{\mathrm{P5\!\!-IMC}_{11}=\mathrm{CLOSED}.}
$$

This is an external-theorem closure, not a numerical inference from the displayed Iwasawa invariants.

## 4. Burns--Kurihara--Sano hypotheses are closed

Burns--Kurihara--Sano work under a hypothesis package that, in the present elliptic-curve case, includes:

1. the appropriate cohomology group is $\mathbb Z_p$-free;
2. the algebraic rank is positive;
3. $\Sha(E/\mathbb Q)[p^\infty]$ is finite.

Residual irreducibility makes the first condition automatic in their setup. For the present pair,

$$
\operatorname{rank}E(\mathbb Q)=2>0
$$

and the imported project certificate gives

$$
\Sha(E/\mathbb Q)[11^\infty]=0.
$$

Hence the BKS standing hypotheses needed in the present route are closed.

We record

$$
\boxed{\mathrm{P5\!\!-BKS\!\!-HYP}_{11}=\mathrm{CLOSED}.}
$$

## 5. What full IMC now gives

The BKS Iwasawa-theoretic theorem compares the cyclotomic derivative of Kato's zeta element to the Bockstein regulator up to a $p$-adic unit under the full cyclotomic main conjecture and their standing hypotheses.

Thus, for $(E,p)=(389.a1,11)$, the combination

$$
\mathrm{P5\!\!-IMC}_{11}
+
\mathrm{P5\!\!-BKS\!\!-HYP}_{11}
$$

closes the algebraic Iwasawa-to-Bockstein relation up to $\mathbb Z_{11}^\times$.

We record this as

$$
\boxed{\mathrm{P5\!\!-ALG}_{11}=\mathrm{CLOSED\ UP\ TO\ UNIT}.}
$$

Likewise, the BKS corollary gives the corresponding $11$-adic BSD leading-term relation up to $\mathbb Z_{11}^\times$. This is a genuine theorem-level advance in the route, but it is not yet the classical complex BSD $11$-part.

## 6. The remaining derivative-direction bridge

### 6.1 Bockstein regulator

Let $x_1,\ldots,x_r$ be a basis of the free Mordell--Weil lattice, with $r=2$. BKS define a Bockstein regulator

$$
R_\omega^{\mathrm{Boc}}
$$

and identify the image of the BSD determinant element under the Bockstein map with

$$
\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}
R_\omega^{\mathrm{Boc}}.
$$

Their Generalized Perrin--Riou conjecture is equivalent to the equality

$$
\boxed{
\kappa_\infty
=
\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}
R_\omega^{\mathrm{Boc}}.
}
$$

This is the exact location where the complex higher derivative and the archimedean Neron--Tate regulator enter the cyclotomic derived object.

### 6.2 Two derivative directions must not be identified

The following objects live in different variation directions:

$$
D_{\mathrm{cyc}}^2L_{11}(E)
$$

and

$$
\left.\frac{d^2}{ds^2}L(E,s)\right|_{s=1}.
$$

The first varies a $p$-adic cyclotomic character. The second varies the complex spectral parameter. A nonzero Kurihara derivative, a Mazur--Tate augmentation coefficient, or an Iwasawa characteristic element does not by itself identify these two derivatives.

The Generalized Perrin--Riou comparison is precisely the missing direction-changing statement in this route.

Therefore

$$
\boxed{\mathrm{P5\!\!-GPR}_{11}=\mathrm{OPEN}.}
$$

This is now the principal conceptual obstruction.

## 7. Bockstein nonvanishing is a finite computational gate

BKS relate the Bockstein regulator to the $p$-adic height regulator $R_p$ by a formula of the form

$$
\langle x,R_\omega^{\mathrm{Boc}}\rangle_p
=
\log_\omega(x)R_p.
$$

Consequently, a rigorous certificate

$$
R_{11}\neq0
$$

implies

$$
R_\omega^{\mathrm{Boc}}\neq0.
$$

This does not solve GPR, but it removes the nonvanishing side condition in the BKS classical-$p$-part implication.

The present package therefore separates

$$
\boxed{\mathrm{P5\!\!-BOC\!\!-NZ}_{11}}
$$

as a finite local replay gate. A SageMath script is included at

```text
scripts/replay_padic_regulator_11.sage
```

The result is intentionally left as `PENDING_LOCAL_SAGE_REPLAY` in this package because SageMath is not available in the present execution environment. No numerical value is promoted to theorem status here.

## 8. Why the discrete routes do not finish the complex leading term

### 8.1 Kurihara and refined Tamagawa systems

Kim--Pollack prove a refined discrete Tamagawa/BSD-type formula in terms of Kolyvagin derivatives of modular-symbol $L$-values. This controls the rank and the exact module structure of the Bloch--Kato Selmer group and, at ordinary primes under large-image hypotheses, gives canonical nonvanishing of the Kurihara collection.

For the present project this strongly confirms that the Selmer/discrete side is closed. However, the discrete derivatives are not the same object as the complex $s$-derivative. The discrete theory is therefore an exact Selmer certificate, not a replacement for the GPR period comparison.

### 8.2 Mazur--Tate finite layers

Bullach--Honnor prove substantial $p$-parts of refined Mazur--Tate conjectures for semistable non-CM curves at $p\ge11$. Since $389.a1$ is semistable, non-CM, and $p=11$, these results apply to the relevant finite-layer order-of-vanishing and weak-main-conjecture components.

Their positive-rank discussion nevertheless leaves the finer rank-sensitive leading coefficient dependent on the same type of BSD/GPR or height-comparison input. Hence the finite-layer route closes rank detection but does not identify the complex rank-$2$ coefficient required by $\mathrm{P5\!\!-LAT}_{11}$.

### 8.3 Anticyclotomic/base-change escape

Sano's derived Bockstein formalism over imaginary quadratic fields proves strong arithmetic derived formulas from Heegner main conjectures. But the route back to the classical complex BSD leading term still requires an additional equality identifying the derived element with the complex leading term and archimedean regulator.

Thus quadratic base change does not remove the same comparison gate; it transports it.

## 9. Minimal closure theorem

The current route can now be stated as a precise conditional reduction.

### Theorem 9.1: one-prime rank-$2$ closure reduction

For $E=389.a1$ and $p=11$, assume the imported exact project certificate

$$
\Sha(E/\mathbb Q)[11^\infty]=0.
$$

Then:

1. the full cyclotomic Iwasawa Main Conjecture at $11$ is available by Burungale--Castella--Skinner;
2. the BKS standing hypotheses used in the rank-$2$ route are satisfied;
3. the algebraic Iwasawa-to-Bockstein relation is available up to a $11$-adic unit;
4. the $11$-adic BSD leading-term relation is available up to a $11$-adic unit;
5. if $R_\omega^{\mathrm{Boc}}\neq0$ and the rank-$2$ Generalized Perrin--Riou equality holds for $(E,11)$, then the classical $11$-part BSD lattice equality $\mathrm{P5\!\!-LAT}_{11}$ follows.

In the present curve, the classical target becomes

$$
\boxed{
L^*(E,1)\mathbb Z_{11}
=
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)\mathbb Z_{11}.
}
$$

Therefore the remaining route is

$$
\boxed{
\mathrm{P5\!\!-BOC\!\!-NZ}_{11}
+
\mathrm{P5\!\!-GPR}_{11}
\Longrightarrow
\mathrm{P5\!\!-LAT}_{11}.
}
$$

The first gate is finite/computational. The second is the remaining conceptual theorem gate.

## 10. Gate table

```text
P4-SHA11                 CLOSED (imported exact project certificate)
P5-GOOD-ORD11            CLOSED (curve data)
P5-RESIDUAL-IRR11        CLOSED (maximal 11-adic image)
P5-BCS-IM-CONDITION      CLOSED (explicit unipotent certificate)
P5-IMC11                 CLOSED (Burungale--Castella--Skinner)
P5-BKS-HYP11             CLOSED
P5-ALG11                 CLOSED UP TO Z_11^x
P5-PADIC-BSD11           CLOSED UP TO Z_11^x
P5-DISCRETE-SELMER11     CLOSED
P5-MAZUR-TATE-WEAK11     CLOSED AS EXTERNAL THEOREM INPUT
P5-BOC-NZ11              PENDING FINITE SAGEMATH REPLAY
P5-GPR11                 OPEN CONCEPTUAL GATE
P5-LAT11                 BLOCKED BY BOC-NZ11 + GPR11
FULL BSD                  NOT CLAIMED
```

## 11. Consequence for the research strategy

The next stage should not re-run:

- the Kurihara search at $p=11$;
- the $11$-primary Selmer-structure argument;
- generic searches for a cyclotomic main conjecture;
- global rational reconstruction of $\mathcal B_\infty(E)$ as the first gate.

The next stage should instead do exactly two things:

1. close $\mathrm{P5\!\!-BOC\!\!-NZ}_{11}$ by exact local SageMath computation and preserve the raw $11$-adic output as a certificate;
2. attack the rank-$2$ GPR equality, or prove a weaker one-prime lattice version sufficient for $\mathrm{P5\!\!-LAT}_{11}$.

If the second task cannot be proved from the current literature, the correct new frontier is not `BSD still open'. It is the much smaller statement

$$
\boxed{
\kappa_\infty
\stackrel{?}{=}
\frac{L_S^*(389.a1,1)}{\Omega_\xi R_\infty}
R_\omega^{\mathrm{Boc}}
\quad\text{at }p=11.
}
$$

This is the current irreducible rank-$2$ bridge in the chosen route.

## References

1. A. Burungale, F. Castella, C. Skinner, *Base change and Iwasawa Main Conjectures for GL2*, arXiv:2405.00270, current manuscript dated 2026-03-22.
2. D. Burns, M. Kurihara, T. Sano, *On derivatives of Kato's Euler system for elliptic curves*, arXiv:1910.07404.
3. C.-H. Kim, R. Pollack, *The refined Tamagawa number conjectures for GL2*, arXiv:2505.09121.
4. D. Bullach, M. H. L. Honnor, *On the refined Birch--Swinnerton-Dyer type conjectures of Mazur and Tate*, arXiv:2511.07203.
5. T. Sano, *Derived Bockstein regulators and anticyclotomic p-adic Birch and Swinnerton-Dyer conjectures*, arXiv:2308.08875.
6. LMFDB, elliptic curve $389.a1$.

## Claim discipline

This document does **not** claim a proof of BSD. It records a theorem-level closure of the cyclotomic Iwasawa gate for $(389.a1,11)$, imports an earlier exact $11$-primary $\Sha$ certificate, and reduces the remaining classical $11$-part leading-term problem to a finite Bockstein nonvanishing check plus the rank-$2$ Generalized Perrin--Riou comparison.
