# BSD P5 v0.6 — Unit-Level Generalized Perrin--Riou Minimal Gate for $389.a1$ at $p=11$

**Date:** 2026-08-14  
**Curve:** $E=389.a1$ over $\mathbb Q$  
**Prime:** $p=11$  
**Status:** theorem/reduction package; **not** a proof of BSD  
**Parent state:** P4 and P5 v0.5

---

## Abstract

For the rank-$2$ elliptic curve $E=389.a1$ at the good ordinary prime $p=11$, the previous project stages closed the $11$-primary Selmer/Shafarevich--Tate gate and the cyclotomic Iwasawa Main Conjecture gate, and reduced the classical $11$-part of the Birch--Swinnerton-Dyer leading-term formula to a Bockstein nonvanishing check plus the rank-$2$ Generalized Perrin--Riou comparison.

This stage makes two further reductions.

First, a published computation of Mazur--Stein--Tate gives the cyclotomic $11$-adic regulator of the rank-$2$ curve $389A$ with nonzero constant $11$-adic digit. Hence the regulator is nonzero; in the published normalization it is an $11$-adic unit. This closes the finite nonvanishing gate required in the Bockstein branch. We use only nonvanishing, which is invariant under any nonzero change of normalization.

Second, the full Generalized Perrin--Riou equality is stronger than is needed for a single-prime BSD statement. Once the v0.5 Iwasawa/Bockstein hypotheses are fixed, the remaining $11$-part target is equivalent to equality of two rank-one $\mathbb Z_{11}$-lattices. We therefore introduce the **unit-level Generalized Perrin--Riou gate** $\mathrm{uGPR}_{11}$ and prove formally that it is equivalent to the remaining lattice target. Over the discrete valuation ring $\mathbb Z_{11}$, this unit-level gate splits into two minimal conditions: integrality and primitiveness modulo $11$.

Fresh literature auditing also rules out three apparent shortcuts. Fouquet's 2025 Hecke-algebra ETNC paper explicitly works at specializations with $L(f,r)\ne0$ and therefore does not directly cover the central rank-$2$ zero. The recent refined Mazur--Tate results of Bullach--Honnor prove substantial finite-layer statements, but explicitly state that the finer positive-rank congruence still requires BSD, the generalized Perrin--Riou conjecture, or an extension of a height-comparison theorem. Finally, classical Perrin--Riou--Schneider higher-rank $p$-adic BSD formulas determine the leading term of a $p$-adic $L$-function, not the complex derivative $L^{(2)}(E,1)/2!$.

Thus the project frontier is no longer ``rank-$2$ BSD'' in bulk. For $(389.a1,11)$ it is the two-bit lattice problem

$$
\boxed{
\mathrm{P5\!-INT}_{11}
\quad+\quad
\mathrm{P5\!-PRIM}_{11}.
}
$$


---

## 1. Fixed inherited data

The following are imported as project-certified inputs and are not recomputed here:

$$
\operatorname{rank}E(\mathbb Q)=2,
$$

$$
\Sha(E/\mathbb Q)[11^\infty]=0,
$$

$$
\prod_{\ell}c_\ell(E)=1,
\qquad
\#E(\mathbb Q)_{\mathrm{tors}}=1,
$$

and

$$
\boxed{
\mathrm{P5\!-IMC}_{11}=\mathrm{CLOSED}.
}
$$


The v0.5 reduction also supplies the BKS Iwasawa-to-Bockstein comparison up to multiplication by an element of $\mathbb Z_{11}^{\times}$, under its recorded standing hypotheses.

The remaining classical one-prime target is

$$
\boxed{
\mathrm{P5\!-LAT}_{11}:
\quad
L^*(E,1)\mathbb Z_{11}
=
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)\mathbb Z_{11},
}
$$


where

$$
L^*(E,1)=\frac{L^{(2)}(E,1)}{2!}.
$$

Local Tamagawa, torsion, and $11$-primary Shafarevich--Tate factors are absent from this displayed target because their $11$-primary contributions have already been certified to be trivial in the imported state.

---

## 2. Published $11$-adic regulator certificate

Mazur, Stein, and Tate computed $p$-adic regulators for the first rank-$2$ elliptic curve, $389A$ of conductor $389$. Their table gives at $p=11$

$$
R_{11}
=
4+7\cdot 11+6\cdot 11^2+11^3+9\cdot 11^4+10\cdot 11^5+3\cdot 11^6+O(11^7).
$$

Therefore

$$
R_{11}\equiv 4\pmod{11},
$$

and hence

$$
\boxed{
R_{11}\ne0.
}
$$

In the normalization of that computation one has the stronger statement

$$
\boxed{
v_{11}(R_{11})=0.
}
$$

The present proof route uses only nonvanishing. A change between standard cyclotomic $p$-adic-height normalizations can rescale the regulator by a nonzero scalar, but cannot turn a nonzero regulator into zero. Consequently the finite gate from v0.5 may be promoted to

$$
\boxed{
\mathrm{P5\!-BOC\!-NZ}_{11}
=
\mathrm{CLOSED\_BY\_PUBLISHED\_COMPUTATION}.
}
$$


This closure does **not** identify the complex leading term and does **not** prove the classical $11$-part of BSD.

---

## 3. The one-dimensional comparison line

Let $\mathcal L_{11}$ denote the one-dimensional $\mathbb Q_{11}$-comparison line used in the BKS determinant formalism after the v0.5 specializations, and let

$$
\Lambda_{11}\subset\mathcal L_{11}
$$

be its distinguished integral $\mathbb Z_{11}$-lattice.

The closed IMC/BKS branch supplies a primitive generator, denoted

$$
\kappa_\infty\in\Lambda_{11},
\qquad
\Lambda_{11}=\mathbb Z_{11}\kappa_\infty,
$$

up to multiplication of $\kappa_\infty$ by a unit.

On the classical BSD side, define the BKS-normalized vector

$$
b_{\mathrm{BSD}}
:=
\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}
R_\omega^{\mathrm{Boc}}
\in
\mathcal L_{11}\otimes_{\mathbb Q_{11}}\mathbb C_{11},
$$

with the same period, local Euler factor, Bockstein-regulator, and comparison conventions as in BKS. The full Generalized Perrin--Riou conjecture asserts the element equality

$$
\kappa_\infty=b_{\mathrm{BSD}}.
$$

For a one-prime valuation statement this is more than necessary.

---

## 4. Definition of the unit-level GPR gate

### Definition 4.1

The **unit-level Generalized Perrin--Riou gate at $11$** is

$$
\boxed{
\mathrm{uGPR}_{11}:
\quad
b_{\mathrm{BSD}}
\in
\mathbb Z_{11}^{\times}\kappa_\infty.
}
$$

Equivalently,

$$
\boxed{
\mathbb Z_{11}b_{\mathrm{BSD}}
=
\mathbb Z_{11}\kappa_\infty
=
\Lambda_{11}.
}
$$

This statement forgets the exact unit relating the two vectors. Therefore

$$
\mathrm{GPR}_{11}
\Longrightarrow
\mathrm{uGPR}_{11},
$$

whereas the converse need not hold.

---

## 5. Minimal-gate theorem

### Theorem 5.1 — one-prime minimality

Assume all imported v0.5 hypotheses for $(E,p)=(389.a1,11)$ and the closure

$$
R_{11}\ne0.
$$

Then, within the BKS-normalized determinant line,

$$
\boxed{
\mathrm{P5\!-LAT}_{11}
\iff
\mathrm{uGPR}_{11}.
}
$$


#### Proof

The v0.5 IMC/BKS branch identifies the arithmetic determinant lattice with the lattice generated by $\kappa_\infty$, up to a unit. The nonvanishing of $R_{11}$ removes the degeneracy obstruction in the Bockstein regulator branch. Under the imported local normalizations and the already-trivial $11$-primary Tamagawa, torsion, and Shafarevich--Tate factors, the classical $11$-part of the BSD leading-term formula is precisely the assertion that the BSD determinant vector spans this same integral lattice. Thus

$$
\mathrm{P5\!-LAT}_{11}
\iff
\mathbb Z_{11}b_{\mathrm{BSD}}=\Lambda_{11}.
$$


By Definition 4.1 the right-hand statement is exactly $\mathrm{uGPR}_{11}$. This proves the equivalence. $\square$

### Remark 5.2

The theorem is a **reduction theorem**, not a proof of the remaining lattice equality. Its role is to remove unnecessary information: the exact scalar required by full GPR is not needed for the $11$-part.

---

## 6. DVR decomposition: integrality plus one mod-$11$ bit

Because $\Lambda_{11}$ is a free rank-one module over the discrete valuation ring $\mathbb Z_{11}$, unit-level GPR has an elementary two-stage decomposition.

### Definition 6.1

Set

$$
\mathrm{P5\!-INT}_{11}:
\quad
b_{\mathrm{BSD}}\in\Lambda_{11},
$$


and

$$
\mathrm{P5\!-PRIM}_{11}:
\quad
b_{\mathrm{BSD}}\notin11\Lambda_{11}.
$$


Equivalently, once integrality is known,

$$
\overline{b}_{\mathrm{BSD}}\ne0
\quad\text{in}\quad
\Lambda_{11}/11\Lambda_{11}.
$$

### Proposition 6.2

One has

$$
\boxed{
\mathrm{uGPR}_{11}
\iff
\mathrm{P5\!-INT}_{11}
\land
\mathrm{P5\!-PRIM}_{11}.
}
$$


#### Proof

Choose the primitive basis $\kappa_\infty$ of $\Lambda_{11}$. If $b_{\mathrm{BSD}}\in\Lambda_{11}$, then there is a unique $a\in\mathbb Z_{11}$ such that

$$
b_{\mathrm{BSD}}=a\kappa_\infty.
$$

The condition $b_{\mathrm{BSD}}\notin11\Lambda_{11}$ is equivalent to $a\notin11\mathbb Z_{11}$, hence to $a\in\mathbb Z_{11}^{\times}$. This is exactly $\mathrm{uGPR}_{11}$. $\square$

Thus the final conceptual wall for this one-prime route is literally reduced to

$$
\boxed{
\text{integrality}
+
\text{one nonzero residue class mod }11.
}
$$

This does not make the missing theorem easy: the hard part is constructing the correct comparison map that assigns a canonical integral meaning to the complex leading coefficient inside the $11$-adic determinant line.

---

## 7. Why the main apparent escape routes do not close the two-bit gate

### 7.1 Fouquet Hecke-algebra ETNC

Fouquet's 2025 formulation and main specialization results are stated in a framework in which the relevant special value $L(f,r)$ is assumed nonzero. The resulting pointwise Tamagawa-number-conjecture statement therefore applies to nonvanishing critical specializations, not directly to the central rank-$2$ specialization of $389.a1$, where

$$
L(E,1)=0.
$$

Consequently this theorem cannot be substituted for $\mathrm{P5\!-INT}_{11}$ or $\mathrm{P5\!-PRIM}_{11}$ at the rank-$2$ central point without an additional derived specialization theorem.


### 7.2 Refined Mazur--Tate theory

Bullach--Honnor prove the $p$-parts of the order-of-vanishing, weak main, and their stated leading-term components for semistable non-CM curves at $p\ge11$. However, they explicitly distinguish these statements from the finer positive-rank congruence modulo the rank-sensitive augmentation power. For positive rank, they state that the finer congruence would follow up to a unit if BSD holds, without ambiguity under the generalized Perrin--Riou conjecture, and in broader settings requires an extension of a height-pairing comparison.

Therefore the currently proved finite-layer theorem does not supply the missing rank-$2$ residue

$$
\overline{b}_{\mathrm{BSD}}\in\Lambda_{11}/11\Lambda_{11}.
$$

### 7.3 Classical higher-rank $p$-adic BSD

Perrin--Riou--Schneider formulas, and computational implementations based on them, control the order and leading coefficient of the **cyclotomic $p$-adic $L$-function** in terms of the $p$-adic regulator and $p$-primary Selmer data. They are extremely useful for proving statements such as

$$
\Sha(E/\mathbb Q)[p]=0
$$

in high rank. Their analytic object is nevertheless a $p$-adic cyclotomic leading coefficient, not

$$
\frac{L^{(2)}(E,1)}{2!}.
$$

The change of derivative direction is exactly the comparison still encoded by $\mathrm{uGPR}_{11}$.

### 7.4 Curve-specific computational BSD

For $389a$, rigorous algebraic rank calculations and many $p$-primary Shafarevich--Tate bounds are available. Standard computational documentation nevertheless treats the analytic strong-BSD quotient in rank $2$ as a floating-point prediction and explicitly warns that its rationality is not proved in general. Such computations therefore provide consistency checks, not $\mathrm{P5\!-LAT}_{11}$.


---

## 8. Current gate state

The project state after this stage is

```text
P4 / Sha[11^infinity]      CLOSED_IN_PROJECT_THEOREM_CHAIN
P5-IMC11                   CLOSED
P5-BKS-HYP                 CLOSED
P5-IWASAWA-TO-BOC11        CLOSED_UP_TO_UNIT
P5-BOC-NZ11                CLOSED_BY_PUBLISHED_COMPUTATION
P5-FULL-GPR11              OPEN_STRONGER_THAN_NEEDED
P5-uGPR11                  OPEN_MINIMAL_CONCEPTUAL_GATE
P5-INT11                   OPEN
P5-PRIM11                  OPEN
P5-LAT11                   EQUIVALENT_TO_uGPR11
```

The main conceptual reduction is

$$
\boxed{
\mathrm{P5\!-LAT}_{11}
\iff
\mathrm{uGPR}_{11}
\iff
\mathrm{P5\!-INT}_{11}
\land
\mathrm{P5\!-PRIM}_{11}.
}
$$


---

## 9. Next attack surface

The next research stage should **not** repeat IMC, Kurihara, or $p$-adic-regulator calculations. It should attack one of the following strictly smaller targets.

### Route A — derived integrality

Construct a central rank-$2$ derived specialization map from a Hecke/Iwasawa fundamental line and prove

$$
b_{\mathrm{BSD}}\in\Lambda_{11}.
$$

This is $\mathrm{P5\!-INT}_{11}$.


### Route B — mod-$11$ primitive comparison

Assuming integrality, prove only

$$
\overline b_{\mathrm{BSD}}\ne0
\quad\text{in}\quad
\Lambda_{11}/11\Lambda_{11}.
$$

A rank-sensitive Mazur--Tate/Kato derivative congruence at precisely the required augmentation order would be sufficient. Full element equality is unnecessary.

### Route C — rational reconstruction escape

Independently prove a rationality and effective denominator theorem for

$$
\mathcal B_\infty(E)
=
\frac{L^{(2)}(E,1)/2!}
{\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)}.
$$

Then a rigorous real interval smaller than the rational-separation bound can identify the scalar exactly. This route remains open because no effective rank-$2$ denominator theorem has been supplied.

---

## 10. Claim discipline

This package proves a reduction, not BSD. In particular it does **not** claim

$$
\mathcal B_\infty(E)=1,
$$

it does **not** claim

$$
\mathrm{uGPR}_{11},
$$

and it does **not** claim the classical $11$-part of the BSD leading-term formula.

What is newly certified is:

1. the $11$-adic Bockstein nonvanishing side condition is closed by a published $p$-adic regulator computation;
2. full rank-$2$ GPR is stronger than necessary for the one-prime target;
3. the remaining one-prime target is equivalent to a unit-level lattice comparison;
4. over $\mathbb Z_{11}$ that comparison is equivalent to integrality plus a single nonzero mod-$11$ residue;
5. the principal current ETNC/Mazur--Tate/$p$-adic-BSD shortcuts do not supply this missing residue without a derived comparison input.

---

## References

1. B. Mazur, W. Stein, J. Tate, *Computation of p-adic heights and log convergence*, Documenta Mathematica, Extra Volume Coates, 577--614, DOI 10.4171/DMS/4/17.
2. D. Burns, M. Kurihara, T. Sano, *On derivatives of Kato's Euler system for elliptic curves*, Journal of the Mathematical Society of Japan 76 (2024), arXiv:1910.07404.
3. O. Fouquet, *The Equivariant Tamagawa Number Conjectures for modular motives with coefficients in Hecke algebra*, Tunisian Journal of Mathematics 7 (2025), 791--829, arXiv:2501.07105.
4. D. Bullach, M. H. L. Honnor, *On the refined `Birch--Swinnerton-Dyer type' conjectures of Mazur and Tate*, arXiv:2511.07203.
5. SageMath documentation, elliptic-curve BSD and Shafarevich--Tate functionality, consulted 2026-08-14.

---

## Final status

$$
\boxed{
\text{For }(389.a1,11),\quad
\text{all current algebraic/Iwasawa/nondegeneracy gates are closed,}
}
$$

while

$$
\boxed{
\text{the remaining classical one-prime obstruction is }
\mathrm{P5\!-\mathrm{uGPR}}_{11}
=
\mathrm{P5\!-INT}_{11}+\mathrm{P5\!-PRIM}_{11}.
}
$$
