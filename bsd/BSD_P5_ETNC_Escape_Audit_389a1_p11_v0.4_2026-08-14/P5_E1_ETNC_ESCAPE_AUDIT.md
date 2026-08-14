# P5-E1 — ETNC / Determinant-Line Representation Escape Audit

**Date:** 2026-08-14  
**Curve:** $E=389.a1$  
**Prime:** $p=11$  
**Verdict:** `NO_DIRECT_ETNC_ESCAPE_FROM_DERIVED_ARCHIMEDEAN_GATE`

## 1. Why this route was tested

P5 has been reduced to the scalar

$$
\mathcal B_\infty(E)
=
\frac{L^{(2)}(E,1)/2!}
{\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)}.
$$

The first escape question is whether a proved equivariant Tamagawa number conjecture or determinant-line theorem can place this scalar in a rational lattice **without first assuming the classical rank-$2$ BSD leading-term formula**.

If yes, the numerical problem would become discrete and rational reconstruction could finish the curve.

## 2. What the ETNC machinery actually supplies

Fouquet's ETNC framework for modular motives constructs fundamental lines and zeta elements over Hecke/Iwasawa coefficient rings and proves broad cases of the corresponding ETNC under residual-representation hypotheses.

At classical non-derived fibers the framework has canonical $p$-adic and complex period maps and the zeta element computes critical $L$-values.

This is strong enough to justify the following classification:

```text
fundamental-line existence          THEOREM TECHNOLOGY AVAILABLE
integral zeta-element lattice       THEOREM TECHNOLOGY AVAILABLE
specialization in Hecke families    THEOREM TECHNOLOGY AVAILABLE
ordinary critical-value periods     THEOREM TECHNOLOGY AVAILABLE
```

## 3. Why rank $2$ at the trivial character is different

For $389.a1$ the central value vanishes to order $2$. The P5 target is not an ordinary nonzero fiber value. It is a **derived specialization** at the augmentation point.

The relevant comparison has the shape

$$
\partial^{(1)}\mathbf z_E
\longleftrightarrow
\frac{L^{(2)}(E,1)}{2!}
$$

on the analytic side and must simultaneously identify the derived determinant/Bockstein object with

$$
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)
$$

on the classical arithmetic side.

This is precisely the kind of extra datum encoded by the Generalized Perrin--Riou / derived-zeta formalism.

## 4. Circularity audit

Burns--Kurihara--Sano record that for general positive rank the cyclotomic Generalized Perrin--Riou conjecture follows, up to a $\mathbb Z_p^\times$ factor, from the relevant BSD statement together with a generalized Iwasawa main conjecture.

Their Mazur--Tate analysis also distinguishes an algebraic Generalized Perrin--Riou statement from the analytic one and states that the two become equivalent precisely when the classical BSD statement over $\mathbb Q$ is valid.

Therefore the following implication is **not** currently justified:

$$
\text{ETNC / Iwasawa main conjecture}
\Longrightarrow
\mathcal B_\infty(E)\in\mathbb Q^\times
$$

for the rank-$2$ trivial-character leading term without an additional derived archimedean comparison theorem.

The obstruction is not the absence of a fundamental line. It is the absence of a proved comparison between the **derived** $p$-adic/determinantal specialization and the **archimedean Néron--Tate leading-term normalization**.

## 5. Refined P5 gate

The previous gate

$$
\mathrm{P5\!\!\!-RAT}
$$

can now be sharpened to

$$
\boxed{
\mathrm{P5\!\!\!-DERPER}:
\text{derived determinant specialization}
\xrightarrow{\operatorname{per}_\infty}
\frac{L^{(2)}(E,1)}{2!}
\text{ with the Neron--Tate lattice identified}.
}
$$

A proof of `P5-DERPER` with an integral lattice immediately implies the required algebraicity/rationality gate and may also yield an effective denominator bound.

Current status:

```text
P5-ETNC-FUNDAMENTAL-LINE   AVAILABLE IN BROAD THEOREM FRAMEWORKS
P5-DERIVED-SPECIALIZATION  PARTIALLY AVAILABLE p-ADICALLY
P5-DERPER                  OPEN FOR THIS CLASSICAL RANK-2 TARGET
P5-RAT                     BLOCKED BY P5-DERPER
P5-VAL11                   BLOCKED BY P5-RAT
```

## 6. Consequence for the research route

The next literature search should no longer ask broadly for "ETNC for elliptic curves".

It should target exactly one of the following:

1. a derived archimedean period map at the augmentation ideal;
2. a Bockstein regulator theorem identifying the determinant lattice with the classical Néron--Tate regulator in rank $2$;
3. a theorem proving rationality plus an effective denominator for the normalized complex rank-$2$ leading term;
4. an independent comparison from a $p$-adic derived regulator to the classical Néron--Tate regulator that does not assume BSD.

Anything that only proves an Iwasawa characteristic-ideal equality or an ordinary critical-value interpolation theorem is upstream of the obstruction, not a solution to it.
