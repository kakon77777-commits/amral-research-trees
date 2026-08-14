---
title: "BSD RUGZPB P2/P4 Update: exact 11-primary Sha closure for 389.a1"
version: "v0.2"
date: "2026-08-14"
author: "Neo.K / EveMissLab"
status: "theorem-chain update + exact finite computation"
epistemic_status: "P4 closed for the 11-primary Sha component of 389.a1, relative only to cited published/current theorem inputs; NOT full BSD and NOT a proof of the p=11 leading-term formula."
---

# BSD RUGZPB P2/P4 Update

## 0. Scope

This note continues `BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1.md` at the declared proof obligations P1--P7. It does not repeat the rank-$0$ family census.

The two targets addressed here are:

- P2: audit whether RUGZPB is merely ETNC in different notation;
- P4: close one favorable odd prime for the rank-$2$ wall curve $389.a1$.

The main new result is a computer-assisted exact finite-field certificate at

$$
E=389.a1,
\qquad
p=11.
$$

The result proved by the theorem chain in this note is

$$
\boxed{
\Sha(E/\mathbb Q)[11^\infty]=0.
}
$$

This statement is strictly weaker than full strong BSD and does not by itself prove

$$
\operatorname{BSD}(E,11)
$$

in the leading-coefficient sense.

---

# 1. External theorem inputs

## 1.1 Curve data

For

$$
E: y^2+y=x^3+x^2-2x,
$$

the LMFDB record for $389.a1$ gives:

- conductor $N=389$;
- Mordell--Weil rank $2$;
- trivial rational torsion;
- Tamagawa product $1$;
- Manin constant $1$;
- non-CM;
- maximal mod-$\ell$ image for every prime $\ell$;
- $a_{11}=-4$.

Thus $11\nmid N$, the mod-$11$ representation is surjective, and $p=11$ is a good ordinary prime because

$$
a_{11}\not\equiv0\pmod{11}.
$$

## 1.2 Kim's structural theorem

We use Chan-Ho Kim, `The structure of Selmer groups and the Iwasawa main conjecture for elliptic curves`, arXiv:2203.12159v6, Theorem 1.8 and Corollary 1.6.

For $p\ge5$, surjective residual representation and Manin constant prime to $p$, Kim defines the Kurihara collection

$$
\widetilde{\boldsymbol\delta}
=
\{\widetilde\delta_n\}_{n\in\mathcal N_1}
$$

and its order

$$
\operatorname{ord}(\widetilde{\boldsymbol\delta})
=
\min\{\nu(n):\widetilde\delta_n\ne0\}.
$$

If this order is finite, Theorem 1.8 gives

$$
\operatorname{cork}_{\mathbb Z_p}
\operatorname{Sel}(\mathbb Q,E[p^\infty])
=
\operatorname{ord}(\widetilde{\boldsymbol\delta}).
$$

It also gives

$$
\operatorname{length}_{\mathbb Z_p}
\left(
\operatorname{Sel}(\mathbb Q,E[p^\infty])_{/\mathrm{div}}
\right)
=
\partial^{(\operatorname{ord}(\widetilde{\boldsymbol\delta}))}
-
\partial^{(\infty)}.
$$

Once $\Sha(E/\mathbb Q)[p^\infty]$ is known finite, the same theorem identifies its length by the same difference.

Kim's Corollary 1.6 further states, under the same residual and Manin hypotheses, that the canonical Kurihara collection is nonzero in the good ordinary case.

No conjectural BSD identity is inserted into the finite computation below.

---

# 2. Exact modular-symbol computation over $\mathbf F_{11}$

The proof-critical computation uses only integer arithmetic and finite-field arithmetic. No floating-point number enters the certificate.

## 2.1 Manin-symbol quotient

For prime level

$$
N=389,
$$

we construct the Manin-symbol module on

$$
\mathbf P^1(\mathbf F_{389})
$$

and impose the standard $S$ and $R$ relations.

The exact row reduction over $\mathbf F_{11}$ gives:

$$
\operatorname{rank}(\text{relation matrix})=325,
$$

hence

$$
390-325=65.
$$

This agrees with the expected dimension

$$
2g(X_0(389))+1=65.
$$

## 2.2 Hecke isolation

Point counting on

$$
E: y^2+y=x^3+x^2-2x
$$

gives

$$
a_2=-2,
\quad
a_3=-2,
\quad
a_5=-3.
$$

Adding the exact Hecke constraints

$$
(T_q-a_q)\lambda=0,
\qquad q\in\{2,3,5\},
$$

leaves a $2$-dimensional mod-$11$ eigenspace before imposing the plus involution.

After imposing the plus relation, the target space has dimension exactly

$$
\boxed{1}.
$$

A deterministic normalization selects a vector

$$
\lambda\in\mathbf F_{11}^{390}.
$$

The script independently verifies that this same vector has the correct Hecke eigenvalues for

$$
q=2,3,5,7,13,17,19,
$$

namely

$$
(-2,-2,-3,-5,-3,-6,5).
$$

This validation is not used as a probabilistic argument; every equality is checked exactly in $\mathbf F_{11}$.

---

# 3. Exact Kurihara witness

Take

$$
\ell_1=397,
\qquad
\ell_2=991.
$$

Exact point counting gives

$$
a_{397}=24,
\qquad
a_{991}=-53.
$$

Both satisfy the mod-$11$ Kolyvagin-prime conditions

$$
\ell\equiv1\pmod{11},
$$

and

$$
a_\ell-\ell-1\equiv0\pmod{11}.
$$

Using primitive roots

$$
5\pmod{397},
\qquad
6\pmod{991},
$$

and

$$
n=397\cdot991=393427,
$$

the exact finite sum corresponding to Kim's mod-$p$ Kurihara quantity, evaluated on the deterministic eigenline normalization $\lambda$, is

$$
\boxed{
\delta_{393427}^{(\lambda)}=6\in\mathbf F_{11}.
}
$$

The residue $6$ itself is normalization-dependent. The invariant statement is

$$
\boxed{
\delta_{393427}^{(\lambda)}\ne0.
}
$$

Changing the nonzero eigenline scalar or the chosen primitive roots multiplies the quantity by a unit and cannot turn a nonzero value into zero.

---

# 4. Canonical-normalization bridge

Kim's canonical modular symbols are normalized by the Néron period. Their mod-$11$ plus modular-symbol vector is a Hecke eigenvector with the same newform eigenvalues.

By the exact computation above, the relevant plus Hecke eigenspace is one-dimensional over $\mathbf F_{11}$.

Kim's good-ordinary nonvanishing result implies that the canonical Kurihara collection for $(389.a1,11)$ is not identically zero. Therefore the canonical mod-$11$ plus modular-symbol vector cannot be the zero vector.

Hence there exists

$$
u\in\mathbf F_{11}^{\times}
$$

such that

$$
\lambda_{\mathrm{can}}=u\lambda.
$$

The Kurihara sum is linear in the modular-symbol vector, so

$$
\widetilde\delta_{393427}^{\mathrm{can}}
=
u\delta_{393427}^{(\lambda)}.
$$

Since

$$
\delta_{393427}^{(\lambda)}=6\ne0,
$$

we obtain the canonical statement

$$
\boxed{
\widetilde\delta_{393427}^{\mathrm{can}}\ne0\pmod{11}.
}
$$

Thus an external Sage/eclib normalization replay is useful as an independent audit, but it is not logically necessary for nonvanishing.

---

# 5. P4 theorem: exact $11$-primary Sha closure

## Theorem 5.1

For the elliptic curve

$$
E=389.a1
$$

and $p=11$, accepting Kim's Theorem 1.8 and good-ordinary nonvanishing theorem as external theorem inputs, the exact finite computation in this package proves

$$
\boxed{
\Sha(E/\mathbb Q)[11^\infty]=0.
}
$$

## Proof

The witness above has

$$
\nu(393427)=2
$$

and

$$
\widetilde\delta_{393427}\ne0.
$$

Therefore

$$
\operatorname{ord}(\widetilde{\boldsymbol\delta})\le2.
$$

Kim's Theorem 1.8 gives

$$
\operatorname{cork}_{\mathbb Z_{11}}
\operatorname{Sel}(\mathbb Q,E[11^\infty])
=
\operatorname{ord}(\widetilde{\boldsymbol\delta}).
$$

The standard Selmer exact sequence contains

$$
E(\mathbb Q)\otimes\mathbb Q_{11}/\mathbb Z_{11}
$$

as a subgroup of the Selmer group. Since the Mordell--Weil rank is exactly $2$,

$$
\operatorname{cork}_{\mathbb Z_{11}}
\operatorname{Sel}(\mathbb Q,E[11^\infty])\ge2.
$$

Hence

$$
\boxed{
\operatorname{ord}(\widetilde{\boldsymbol\delta})=2
}
$$

and

$$
\boxed{
\operatorname{cork}_{\mathbb Z_{11}}
\operatorname{Sel}(\mathbb Q,E[11^\infty])=2.
}
$$

Because our $\nu(n)=2$ witness is nonzero modulo $11$,

$$
\partial^{(2)}(\widetilde{\boldsymbol\delta})=0.
$$

All $\partial^{(i)}$ are nonnegative, hence

$$
\partial^{(\infty)}(\widetilde{\boldsymbol\delta})=0.
$$

Now use the unconditional Selmer-structure clause of Kim's Theorem 1.8:

$$
\operatorname{length}_{\mathbb Z_{11}}
\left(
\operatorname{Sel}(\mathbb Q,E[11^\infty])_{/\mathrm{div}}
\right)
=
\partial^{(2)}-\partial^{(\infty)}
=0.
$$

Therefore

$$
\operatorname{Sel}(\mathbb Q,E[11^\infty])
=
\operatorname{Sel}(\mathbb Q,E[11^\infty])_{\mathrm{div}}
\simeq
(\mathbb Q_{11}/\mathbb Z_{11})^2.
$$

The standard exact sequence is

$$
0
\to
E(\mathbb Q)\otimes\mathbb Q_{11}/\mathbb Z_{11}
\to
\operatorname{Sel}(\mathbb Q,E[11^\infty])
\to
\Sha(E/\mathbb Q)[11^\infty]
\to0.
$$

Since $\operatorname{rank}E(\mathbb Q)=2$ and the rational torsion is trivial,

$$
E(\mathbb Q)\otimes\mathbb Q_{11}/\mathbb Z_{11}
\simeq
(\mathbb Q_{11}/\mathbb Z_{11})^2.
$$

Its injection into the Selmer group is therefore an injection between divisible $11$-primary groups of the same finite corank $2$. The quotient is divisible and has corank $0$, hence it is trivial. Consequently

$$
\boxed{
\Sha(389.a1/\mathbb Q)[11^\infty]=0.
}
$$

This conclusion uses only clauses (1)--(3) of Kim's Theorem 1.8; the later clauses that assume $\Sha[p^\infty]$ finite are not needed.

$\square$

---

# 6. Circularity audit

The proof above does not assume the desired $11$-primary finiteness of $\Sha$.

The logical order is:

$$
\text{exact canonical Kurihara nonvanishing at }\nu(n)=2
\Longrightarrow
\operatorname{ord}(\widetilde{\boldsymbol\delta})=2
\Longrightarrow
\operatorname{Sel}\simeq(\mathbb Q_{11}/\mathbb Z_{11})^2
\Longrightarrow
\Sha[11^\infty]=0.
$$

The proof uses the unconditional Selmer statements (1)--(3) of Kim's Theorem 1.8. It does not invoke the later $\Sha$-specific statements whose formulation assumes $\Sha[p^\infty]$ finite.

---

# 7. P2: RUGZPB versus ETNC audit

## 7.1 Verdict

The current RUGZPB package must not be described as simply "ETNC with renamed variables".

A more accurate decomposition is

$$
\boxed{
\mathrm{RUGZPB}
=
\text{fixed-$(E,p)$ determinant / $p$-TNC core}
+
\text{rank-exact bridge}
+
\text{noncircular $\Sha$ recovery}
+
\text{archimedean comparison}
+
\text{all-prime gluing}
+
\text{rank-uniform architecture}.
}
$$

The determinant-line content of R4, parts of R6, and the zeta/leading-term philosophy of R7 live in the same conceptual territory as Bloch--Kato Tamagawa-number conjectures, Kato's zeta isomorphism, and ETNC-type formulations.

However, the currently cited positive-rank derivative literature does not itself discharge every RUGZPB obligation noncircularly.

## 7.2 Concrete obstruction to naive equivalence

Burns--Kurihara--Sano, `On derivatives of Kato's Euler system for elliptic curves`, arXiv:1910.07404v2, explicitly sets

$$
r=\operatorname{rank}E(\mathbb Q)
$$

and, in its positive-rank setup, assumes the $p$-primary Tate--Shafarevich group finite before defining the BSD element used in the generalized Perrin--Riou framework.

Its arbitrary-rank order-of-vanishing theorem also lists finiteness of the relevant $p$-primary Tate--Shafarevich groups among its hypotheses, while its integrality discussion states that the desired containment follows when the $p$-part of BSD is already known.

Consequently this route cannot, by itself, be substituted for R5 as a noncircular proof of $\Sha$ finiteness in arbitrary positive rank.

The P2 status is therefore:

```text
P2 = RESOLVED_COMPONENTWISE
NOT: RUGZPB == ETNC (proved equivalence)
NOT: RUGZPB independent of ETNC philosophy
YES: determinant core overlaps strongly with p-TNC / zeta-isomorphism structures
YES: explicit rank, Sha-recovery, global gluing, and rank-uniform obligations remain separately typed
```

A formal implication/equivalence theorem would require fixing one precise ETNC formulation and one exact realization functor for the RUGZPB determinant line. That theorem has not been proved here.

---

# 8. P1 minimality consequences

The P4 computation also improves the minimality audit.

At a fixed prime $p$, an R5-like local finiteness clause is not always independent. If a sufficiently strong R4-type theorem determines the Selmer corank and R2 independently fixes the Mordell--Weil rank, then

$$
\operatorname{cork}\operatorname{Sel}
=
\operatorname{rank}E(\mathbb Q)
$$

forces

$$
\Sha[p^\infty]
$$

to be finite.

Thus a minimal fixed-$p$ interface can replace

$$
\text{R4 + independent local R5}
$$

by a stronger exact Selmer-structure primitive.

This does not eliminate global R5. To obtain

$$
\#\Sha(E/\mathbb Q)<\infty,
$$

one still needs a global theorem ensuring that only finitely many primary components can contribute, together with finiteness of each contributing primary component.

Hence:

```text
P1 = PARTIAL_RESOLVED
local R5 can be derived from strong Selmer structure + exact MW rank;
global R5 remains a separate all-prime/global-finiteness obligation.
```

---

# 9. Updated P1--P7 status

| Obligation | New status | Meaning |
|---|---|---|
| P1 Minimality audit | PARTIAL_RESOLVED | local R5 is derivable from exact Selmer structure plus exact MW rank; global R5 remains |
| P2 ETNC equivalence audit | RESOLVED_COMPONENTWISE | determinant core overlaps with $p$-TNC/ETNC; no proved wholesale equivalence |
| P3 Rank-$2$ object choice | RESOLVED_FOR_SHA_CONTROL | Kurihara/Kato modular-symbol route works for fixed-prime Selmer/$\Sha$ control |
| P4 One-prime rank-$2$ closure | CLOSED_AT_P11_FOR_SHA | $\Sha(389.a1/\mathbb Q)[11^\infty]=0$ |
| P5 Analytic-to-regulator | OPEN | still need rank-$2$ complex leading-term/regulator bridge |
| P6 Global primitivity/all-$p$ gluing | OPEN | fixed-prime closure does not globalize automatically |
| P7 Rank-$2$ wall atlas | OPEN | must test the mechanism across multiple rank-$2$ curves |

The important boundary is

$$
\boxed{
\text{P4 Sha-control closed at }p=11
\quad\not\Rightarrow\quad
\text{strong BSD for }389.a1.
}
$$

---

# 10. New irreducible frontier

For the wall curve $389.a1$, the immediate obstruction is no longer

$$
\text{Can one prove any exact positive-rank primary Sha statement?}
$$

because the $11$-primary statement is now closed.

The next frontier is P5:

$$
\boxed{
\frac{L^{(2)}(E,1)}{2!}
\longleftrightarrow
\Omega_E\operatorname{Reg}(E/\mathbb Q)
\times
\text{integral arithmetic index}
}
$$

without inserting the strong BSD formula as an assumption.

The Burns--Kurihara--Sano generalized Perrin--Riou route is relevant here, but its positive-rank formulation must be audited for circular use of $\Sha$ finiteness and $\operatorname{BSD}_p(E)$. The present P4 result is useful precisely because it can now supply the $p=11$ finiteness input independently for $389.a1$.

This changes the role of the BKS route at $p=11$: one of its former hypotheses has become an independently certified fact for the chosen wall curve.

---

# 11. Reproducibility

The package contains:

- `scripts/compute_389a1_kurihara_mod11.py`: pure Python + NumPy exact finite-field certificate;
- `scripts/replay_389a1_kurihara_sage.sage`: independent Sage/eclib canonical-normalization replay;
- `results/389a1_p11_kurihara_certificate.json`: machine-readable certificate;
- `validate_source.py`: UTF-8 and canonical-math-delimiter validation;
- `SHA256SUMS.json`: hashes of committed artifacts;
- `source/BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1.md`: input theorem/reduction state.

The proof-critical Python computation can be replayed with

```text
python scripts/compute_389a1_kurihara_mod11.py results/389a1_p11_kurihara_certificate.replay.json
```

The independent Sage replay is not required by the theorem chain above, but provides a direct check against eclib's Néron-normalized modular-symbol implementation.

---

# References

1. Chan-Ho Kim, `The structure of Selmer groups and the Iwasawa main conjecture for elliptic curves`, arXiv:2203.12159v6, final version, Theorem 1.8 and Corollary 1.6.
2. Francesc Castella and Takamichi Sano, `On refined nonvanishing conjectures by Kurihara and Kolyvagin`, arXiv:2601.14504, 2026. This is corroborating current literature; it is not necessary for the core P4 proof once Kim's good-ordinary nonvanishing is used.
3. David Burns, Masato Kurihara and Takamichi Sano, `On derivatives of Kato's Euler system for elliptic curves`, arXiv:1910.07404v2.
4. LMFDB, elliptic curve $389.a1$ / Cremona $389a1$.
5. Alexandru Ghitza and Chan-Ho Kim, `kurihara_numbers` reference implementation, GitHub.
