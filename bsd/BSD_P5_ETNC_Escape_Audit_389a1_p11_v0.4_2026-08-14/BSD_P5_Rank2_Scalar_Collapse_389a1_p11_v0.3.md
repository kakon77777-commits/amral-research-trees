# BSD Phase 3 — P5 Rank-2 Scalar Collapse and Archimedean Comparison Boundary

**Version:** v0.3  
**Date:** 2026-08-14  
**Curve:** $E=389.a1$  
**Prime:** $p=11$  
**Status:** `P5_REDUCED_TO_ARCHIMEDEAN_RANK2_PERIOD_COMPARISON`

## 0. Claim discipline

This note does **not** claim the Birch--Swinnerton-Dyer conjecture for $389.a1$ and does not promote numerical agreement to proof.

It imports one project-level theorem-chain state from Phase 2:

$$
\Sha(E/\mathbb Q)[11^\infty]=0.
$$

The imported certificate is stored in `dependencies/389a1_p11_kurihara_certificate.json`.

The goal here is narrower: identify the minimal remaining obstruction to the $11$-primary **leading-term** formula in rank $2$ and compile that obstruction into finite theorem gates.

---

## 1. Fixed arithmetic data

For $E=389.a1$, LMFDB records

$$
\operatorname{rank}E(\mathbb Q)=2,
\qquad
E(\mathbb Q)_{\mathrm{tors}}=0,
$$

and

$$
\prod_{\ell}c_\ell=1.
$$

It also records

$$
\operatorname{Reg}^{\mathrm{NT}}(E)
\approx
0.15246017794314375162432475705,
$$

$$
\Omega_E
\approx
4.9804251217101101506427155839,
$$

and

$$
\frac{L^{(2)}(E,1)}{2!}
\approx
0.75931650028842677023019260790.
$$

The last three quantities are used below only as numerical evidence unless an independent rigorous interval certificate is attached.

---

## 2. Scalar collapse

Define the archimedean BSD quotient

$$
\mathcal B_\infty(E)
:=
\frac{L^{(2)}(E,1)/2!}
{\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)}.
$$

For a rank-$2$ elliptic curve the strong BSD leading-term formula predicts

$$
\mathcal B_\infty(E)
=
\frac{\#\Sha(E/\mathbb Q)\prod_\ell c_\ell}
{\#E(\mathbb Q)_{\mathrm{tors}}^2}.
$$

For $389.a1$, the exact torsion and Tamagawa factors are both $11$-adic units, and the imported Phase-2 result gives

$$
\Sha(E/\mathbb Q)[11^\infty]=0.
$$

Hence the arithmetic side of the $11$-primary leading-term formula has valuation

$$
0.
$$

This yields the following reduction.

### Proposition 2.1 — $11$-primary scalar reduction

Assume that $\mathcal B_\infty(E)$ is given a canonical rational realization

$$
\mathcal B_\infty(E)\in\mathbb Q^\times.
$$

Then, for $E=389.a1$, the $11$-primary valuation statement in the strong BSD leading-term formula is equivalent to

$$
\boxed{
 v_{11}(\mathcal B_\infty(E))=0.
}
$$

### Proof

The arithmetic factor is

$$
\frac{\#\Sha(E/\mathbb Q)\prod_\ell c_\ell}
{\#E(\mathbb Q)_{\mathrm{tors}}^2}.
$$

Its $11$-primary contribution is trivial because

$$
\Sha(E/\mathbb Q)[11^\infty]=0,
\qquad
\prod_\ell c_\ell=1,
\qquad
\#E(\mathbb Q)_{\mathrm{tors}}=1.
$$

Therefore its $11$-adic valuation is zero. Once $\mathcal B_\infty(E)$ is canonically rational, equality of the $11$-primary valuations is exactly the displayed condition. $\square$

---

## 3. The rationality gate comes before the valuation gate

The expression

$$
\mathcal B_\infty(E)
$$

is initially a real number obtained from a complex $L$-value derivative, a real period and a Néron--Tate regulator.

For a generic real number there is no canonical operation

$$
v_{11}:\mathbb R^\times\to\mathbb Z.
$$

Thus the statement

$$
v_{11}(\mathcal B_\infty(E))=0
$$

is not even well-typed until a comparison theorem places the normalized leading term in an algebraic field with a specified embedding at $11$; in the classical BSD normalization the desired target is $\mathbb Q^\times$.

Accordingly P5 separates into two gates:

$$
\boxed{
\mathrm{P5\!\!\!-RAT}:
\mathcal B_\infty(E)\in\mathbb Q^\times
}
$$

and, only after that,

$$
\boxed{
\mathrm{P5\!\!\!-VAL}_{11}:
 v_{11}(\mathcal B_\infty(E))=0.
}
$$

For the present curve, `P5-VAL11` is arithmetically predetermined by the Phase-2 $\Sha[11^\infty]$ certificate, but logically blocked by `P5-RAT`.

---

## 4. Literature-route audit

### 4.1 Burns--Kurihara--Sano / Generalized Perrin--Riou

The Generalized Perrin--Riou framework is extremely close to the desired bridge: it connects higher Darmon derivatives of Kato zeta elements with higher derivatives of the complex $L$-function.

However, the arbitrary-rank **leading-term** comparison is not currently an unconditional theorem that can be inserted here as a non-circular proof of BSD.

The later Mazur--Tate paper explicitly records that in general rank the relevant Generalized Perrin--Riou statement follows, up to a $\mathbb Z_p^\times$ factor, from the relevant BSD statement together with a generalized Iwasawa main conjecture. Its main Mazur--Tate theorem also assumes BSD over $\mathbb Q$ when proving the leading-term component.

Classification for P5:

```text
order-of-vanishing machinery       EXTERNAL_THEOREM_INPUT
higher-rank leading-term bridge    CIRCULAR_WITH_BSD for present goal
archimedean rank-2 comparison      NOT_CLOSED
```

### 4.2 Castella--Hsieh rank-$2$ generalized Kato classes

Castella--Hsieh prove rank-$2$ nonvanishing results for generalized Kato classes and obtain a leading-term formula for an **anticyclotomic $p$-adic $L$-function** in terms of a derived $p$-adic height and an enhanced $p$-adic regulator.

This closes important $p$-adic height/Selmer geometry, but it is not the required identity

$$
\frac{L^{(2)}(E,1)}{2!}
\leftrightarrow
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E).
$$

Classification:

```text
generalized Kato class technology  EXTERNAL_THEOREM_INPUT
rank-2 p-adic height bridge         EXTERNAL_THEOREM_INPUT
complex-to-Neron-Tate bridge        TYPE_MISMATCH / NOT_CLOSED
```

### 4.3 Chan-Ho Kim: higher Gross--Zagier / Selmer structure

Kim's higher Gross--Zagier framework removes low-rank restrictions from structural comparisons between Kolyvagin systems, modular symbols, Heegner systems and Selmer structure.

This is precisely why the Phase-2 Kurihara route can control the $11$-primary Selmer quotient. But the structural formula does not provide the missing rank-$2$ complex leading coefficient against the classical Néron--Tate regulator over $\mathbb Q$.

Classification:

```text
Selmer structure                    CLOSED_ENOUGH_FOR_P4
Kurihara/Kolyvagin comparison       CLOSED_ENOUGH_FOR_P4
archimedean leading coefficient     NOT_PROVIDED
```

### 4.4 Kim--Pollack refined Tamagawa number conjectures

Kim--Pollack give a refined BSD-type description of Bloch--Kato Selmer groups using Kolyvagin derivatives of $L$-values, under the Iwasawa main conjecture localized at the augmentation ideal. This is a powerful **discrete** analogue of Beilinson--Bloch--Kato and determines exact Selmer rank/module structure.

Its strength is also the reason it does not by itself solve P5: the construction deliberately accesses the Selmer side through discrete Kolyvagin derivatives rather than supplying the missing archimedean comparison

$$
L^{(2)}(E,1)/2!
\longleftrightarrow
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E).
$$

Classification:

```text
discrete Selmer determinant         EXTERNAL_THEOREM_INPUT
rank/module structure               EXTERNAL_THEOREM_INPUT
archimedean period comparison       NOT_PROVIDED
```

---

## 5. P5 verdict

After the Phase-2 $11$-primary $\Sha$ closure, the strongest audited routes no longer leave a diffuse rank-$2$ Selmer obstruction.

They leave one sharply typed missing map:

$$
\boxed{
\text{complex higher derivative}
\longrightarrow
\text{classical Neron--Tate determinant with algebraic normalization}.
}
$$

Equivalently:

$$
\boxed{
\mathrm{P5}
\rightsquigarrow
\mathrm{P5\!\!\!-RAT}
+
\mathrm{P5\!\!\!-VAL}_{11}.
}
$$

Current status:

```text
P5-RAT      OPEN / ARCHIMEDEAN RANK-2 PERIOD COMPARISON
P5-VAL11    ARITHMETIC TARGET = 0, BUT BLOCKED BY P5-RAT
P5 OVERALL  REDUCED, NOT PROVED
```

This is a genuine reduction: the remaining wall is not ``prove more Selmer finiteness'' and not ``compute another numerical BSD quotient.''

---

## 6. Numerical scalar witness

Using the displayed LMFDB decimals,

$$
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)
\approx
0.759316500288426770230192607899779387254353517170616391495,
$$

so the displayed-data quotient is

$$
\mathcal B_\infty^{\mathrm{disp}}(E)
\approx
1.000000000000000000000000000000290541224328304419\ldots.
$$

Thus the natural candidate is

$$
\boxed{\mathcal B_\infty(E)=1.}
$$

But this is **not** a proof. The inputs are rounded real approximations, and no theorem in the present package proves that $\mathcal B_\infty(E)$ lies in a discrete rational set.

This demonstrates the exact verification obstruction:

$$
\text{arbitrarily strong real approximation}
\not\Rightarrow
\text{exact equality}
$$

without a discreteness/rationality theorem.

---

## 7. Rational-reconstruction escape

The obstruction immediately suggests a finite escape route.

### Lemma 7.1 — denominator-bound reconstruction

Suppose a theorem establishes

$$
\mathcal B_\infty(E)=\frac{a}{b}\in\mathbb Q,
\qquad
\gcd(a,b)=1,
\qquad
1\le b\le B.
$$

Any two distinct reduced rationals whose denominators are at most $B$ differ by at least

$$
\frac{1}{B^2}.
$$

Therefore, if a rigorous interval computation proves

$$
\left|\mathcal B_\infty(E)-1\right|<\frac{1}{2B^2},
$$

then necessarily

$$
\boxed{\mathcal B_\infty(E)=1.}
$$

### Consequence

A future theorem need not necessarily hand us the full equality directly. It would already be enough to provide both:

1. rationality of the normalized rank-$2$ leading term;
2. an explicit denominator bound $B$.

Then a rigorous ball/interval computation of the complex $L$-derivative, real period and Néron--Tate regulator can close the equality by finite rational reconstruction.

The included script `scripts/p5_rational_reconstruction_gate.py` implements this final finite gate once a **rigorous** interval and a proved denominator bound are supplied.

---

## 8. Proof-enclosure interpretation

The present rank-$2$ example exhibits a strong form of proof-space collapse:

$$
\text{large BSD statement}
\to
\text{prime-local Selmer certificate}
\to
\text{exact }\Sha[11^\infty]\text{ control}
\to
\text{one normalized real scalar}.
$$

The verification space is therefore small, but it is not yet discrete.

The missing mathematical operation is a **discretizer**:

$$
\mathbb R\text{-valued leading term}
\longrightarrow
\mathbb Q\text{- or algebraic-valued normalized invariant}.
$$

Once such a map is proved with effective denominators, numerical verification becomes finite and exact.

This is the precise sense in which the current obstruction is a **space-domain proof-enclosure boundary**, rather than a lack of additional raw computation.

---

## 9. Next research route

Do **not** proceed to all-prime gluing as though P5 were closed. The next high-value route is a representation escape focused on the missing discretizer.

Priority order:

```text
P5-E1  Audit ETNC/determinant-line formulations for an unconditional
       rationality statement weaker than full BSD.

P5-E2  Search congruence-ideal / modular-degree / integral determinant
       techniques for an explicit denominator bound on the normalized
       rank-2 archimedean leading term.

P5-E3  Build a rigorous Arb/Dokchitser interval certificate for
       L^(2)(E,1), Omega_E and Reg(E), but keep it as evidence until
       P5-E1/P5-E2 supplies discreteness.

P5-E4  Independently compute the cyclotomic p-adic height/regulator and
       p-adic L-leading term at p=11 as a consistency certificate.
       This does not substitute for P5-RAT.
```

Stop rule:

> Any route that requires the classical rank-$2$ BSD leading-term formula, or a conjecture equivalent to it, must be labeled `CIRCULAR_WITH_BSD` and may not be promoted to proof.

---

## 10. External primary references audited

- D. Burns, M. Kurihara, T. Sano, *On derivatives of Kato's Euler system for elliptic curves*, arXiv:1910.07404.
- D. Burns, M. Kurihara, T. Sano, *On derivatives of Kato's Euler system and the Mazur--Tate Conjecture*, arXiv:2103.11535.
- F. Castella, M.-L. Hsieh, *On the non-vanishing of generalized Kato classes for elliptic curves of rank 2*, arXiv:1809.09066, current arXiv version dated 2026-03-22.
- C.-H. Kim, *A higher Gross--Zagier formula and the structure of Selmer groups*, arXiv:2203.12161, current arXiv version dated 2026-03-22.
- C.-H. Kim, R. Pollack, *The refined Tamagawa number conjectures for GL2*, arXiv:2505.09121.
- LMFDB, elliptic curve $389.a1$ data page.

