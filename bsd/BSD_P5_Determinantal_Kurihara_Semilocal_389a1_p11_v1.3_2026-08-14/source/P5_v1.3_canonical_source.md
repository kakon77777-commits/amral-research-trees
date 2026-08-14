# BSD P5 v1.3 — Determinantal Kurihara–Semilocal Closure for $389.a1$ at $p=11$

**Date:** 2026-08-14  
**Curve:** $E=389.a1$  
**Prime:** $p=11$  
**Squarefree Kurihara level:** $n=397\cdot991$  
**Status:** exact finite determinant theorem plus external theorem alignment. This document does not prove the rank-$2$ complex BSD leading-term formula.

## 0. Inherited exact state

From v1.2,

$$
\operatorname{Sel}_{11}(E/\mathbb Q)
=\mathbb F_{11}P\oplus\mathbb F_{11}Q,
$$

with

$$
P=(0,0),\qquad Q=(1,0),
$$

and norm/semi-local rows

$$
\lambda_{397}=(1,2),\qquad
\lambda_{991}=(1,4).
$$

Thus the combined localization matrix is

$$
M_{\rm loc}
=
\begin{pmatrix}
1&2\\
1&4
\end{pmatrix},
\qquad
\det(M_{\rm loc})=2\in\mathbb F_{11}^{\times}.
$$

The inherited Mazur--Tate/Kurihara computation gives, in the deterministic modular-symbol normalization,

$$
[\bar\theta_n]_2
=6X_{397}X_{991}
\quad\text{in }I^2/I^3,
$$

and canonically at least

$$
[\bar\theta_n]_2\ne0.
$$

The exact scalar $6$ is normalization-dependent; nonvanishing and augmentation order are not.

## 1. External theorem alignment

Chan-Ho Kim's semi-local theorem for Kurihara numbers states, under the standard residual-surjectivity, Manin-constant, local-$p$-torsion, and Tamagawa hypotheses, that a minimal-order nonzero mod-$p$ Kurihara witness gives an isomorphism

$$
\operatorname{Sel}(\mathbb Q,E[p])
\longrightarrow
\bigoplus_{\ell\mid n}
E(\mathbb F_\ell)\otimes\mathbb F_p.
$$

For the present curve, the inherited certificates verify the required hypotheses at $p=11$, and the witness $n=397\cdot991$ has

$$
\nu(n)=2
$$

with nonzero Kurihara number. Hence the v1.2 semi-local isomorphism is not merely an isolated finite computation; it is exactly the phenomenon predicted and proved by refined Iwasawa/Kolyvagin-system theory.

Castella--Sano's 2026 refined nonvanishing theorem further proves the refined Kurihara conjecture in the good ordinary case by reformulating the relevant Iwasawa Main Conjecture in determinant-of-Selmer-complex form. For $389.a1$ at $11$, this closes the refined Kurihara divisibility/nonvanishing side independently of the complex rank-$2$ BSD leading-term problem.

## 2. The finite anomalous norm-Bockstein operator

Put

$$
k=\mathbb F_{11},
$$

$$
V=kP\oplus kQ,
$$

and

$$
W=ke_{397}\oplus ke_{991}.
$$

Let

$$
G=G_{397}\times G_{991}
\simeq C_{11}\times C_{11},
$$

and let

$$
A=k[G],
$$

with augmentation ideal $I$.

Choose generators $\gamma_{397}$ and $\gamma_{991}$ and set

$$
X_{397}=\gamma_{397}-1,
\qquad
X_{991}=\gamma_{991}-1.
$$

Define the finite norm-Bockstein operator

$$
\mathcal B_N:
V\longrightarrow
W\otimes_k I/I^2
$$

by

$$
\mathcal B_N(v)
=
\lambda_{397}(v)e_{397}\otimes X_{397}
+
\lambda_{991}(v)e_{991}\otimes X_{991}.
$$

Relative to $P,Q$ and $e_{397},e_{991}$, this is the matrix

$$
\begin{pmatrix}
X_{397}&2X_{397}\\
X_{991}&4X_{991}
\end{pmatrix}.
$$

## 3. Exact rank-$2$ determinant

Using exterior multiplication in $W$ together with

$$
(I/I^2)\otimes(I/I^2)
\longrightarrow
I^2/I^3,
$$

the rank-$2$ determinant satisfies

$$
\det(\mathcal B_N)(P\wedge Q)
=
\det(M_{\rm loc})
(e_{397}\wedge e_{991})
\otimes X_{397}X_{991}.
$$

Since

$$
\det(M_{\rm loc})=2,
$$

we obtain the exact finite certificate

$$
\boxed{
\det(\mathcal B_N)(P\wedge Q)
=
2(e_{397}\wedge e_{991})\otimes X_{397}X_{991}.
}
$$

In particular,

$$
\boxed{
\det(\mathcal B_N)\ne0.
}
$$

Thus the finite arithmetic determinant is primitive in the mixed augmentation direction.

## 4. Mixed-line coincidence with the modular element

The modular side has

$$
[\bar\theta_n]_2
=6X_{397}X_{991}
$$

in the deterministic replay normalization, while the arithmetic finite Bockstein determinant has coefficient $2$.

Therefore both generate the same prime-labelled mixed line

$$
\boxed{
\mathscr L_{397,991}
:=
\mathbb F_{11}\cdot X_{397}X_{991}
\subset I^2/I^3.
}
$$

Equivalently,

$$
\boxed{
\mathbb F_{11}\cdot[\bar\theta_n]_2
=
\mathbb F_{11}\cdot
\operatorname{coeff}_{e_{397}\wedge e_{991}}
\det(\mathcal B_N)
=
\mathscr L_{397,991}.
}
$$

In the fixed deterministic bases,

$$
6=3\cdot2\pmod{11}.
$$

Hence the scalar ratio is

$$
3\in\mathbb F_{11}^{\times}.
$$

This scalar is **not** promoted to a canonical invariant: changing a primitive root, a generator of either $C_{11}$ factor, a local quotient basis, or a determinant basis rescales these coefficients by units. The invariant statement is the equality of the generated mixed lines and their nonvanishing.

## 5. What is now closed

The following finite rank-$2$ facts are closed:

$$
\boxed{
\mathrm{P5\!-KUR\!-
SEMILOC}_{11}^{(2)}
=
\mathrm{CLOSED}.
}
$$

That is, the minimal two-prime Kurihara witness and the semi-local rank-$2$ Selmer detection agree at theorem level.

Also,

$$
\boxed{
\mathrm{P5\!-FIN\!-
BocDET}_{11}^{(2)}
=
\mathrm{CLOSED\_EXACT}.
}
$$

The finite anomalous norm-Bockstein determinant is explicitly

$$
2X_{397}X_{991}
$$

up to the determinant-line basis.

Finally,

$$
\boxed{
\mathrm{P5\!-MIXEDLINE}_{11}^{(2)}
=
\mathrm{CLOSED\_UP\_TO\_UNITS}.
}
$$

Both the modular initial form and the finite arithmetic determinant occupy the same primitive mixed augmentation line.

## 6. What is not closed

This document does **not** prove that the finite operator $\mathcal B_N$ constructed above is identical, as a canonically normalized element, to the Bockstein regulator appearing in Burns--Kurihara--Sano or in a Nekov\'a\v r Selmer-complex determinant formalism.

Thus the following comparison remains open:

$$
\boxed{
\mathrm{P5\!-CANON\!-
BocID}_{11}^{(2)}.
}
$$

More importantly, even a canonical finite Bockstein identification does not by itself prove the complex rank-$2$ BSD leading coefficient. The remaining analytic comparison is still

$$
\boxed{
\mathrm{P5\!-CPLX\!-
GPR}_{11}^{(2)}:
\text{derived arithmetic determinant}
\longleftrightarrow
\frac{L^{(2)}(E,1)/2!}{\Omega_E^+\operatorname{Reg}_\infty(E)}.
}
$$

Burns--Kurihara--Sano explicitly formulate the Generalized Perrin--Riou conjecture as the bridge between a Darmon-type derivative of Kato's zeta element and the appropriate higher complex derivative. Their arbitrary-rank order-of-vanishing results do not by themselves supply this full leading-coefficient comparison.

## 7. Updated frontier

The rank-$2$, $p=11$ route for $389.a1$ is now:

$$
\begin{aligned}
\Sha(E/\mathbb Q)[11^\infty]&=0 &&\checkmark\\
\mathrm{IMC}_{11}& &&\checkmark\\
\widetilde\delta_{397\cdot991}\ne0& &&\checkmark\\
\operatorname{ord}_I(\bar\theta_{397\cdot991})&=2 &&\checkmark\\
\text{semi-local Selmer map isomorphism}& &&\checkmark\\
\det(M_{\rm loc})=2\ne0& &&\checkmark\\
\det(\mathcal B_N)&\in\mathbb F_{11}^{\times}X_{397}X_{991} &&\checkmark\\
[\bar\theta_n]_2&\in\mathbb F_{11}^{\times}X_{397}X_{991} &&\checkmark\\
\mathrm{P5\!-CANON\!-
BocID}_{11}^{(2)}& &&\mathbf{OPEN}\\
\mathrm{P5\!-CPLX\!-
GPR}_{11}^{(2)}& &&\mathbf{OPEN}.
\end{aligned}
$$

The arithmetic side is therefore no longer a vague high-rank obstruction. At finite mod-$11$ level it is completely rank-detecting, primitive, and supported in the same mixed augmentation direction as the modular element.

## 8. Next research target

Do not recompute the finite group law or Kurihara sum.

The next step is to trace the **canonical determinant map** through one of the following theorem interfaces:

1. Kim's proof of the semi-local theorem, keeping determinant bases instead of only invertibility;
2. Castella--Sano's determinant-of-Selmer-complex reformulation of the refined Kurihara conjecture;
3. Macias Castillo--Sano's canonical determinant-to-Stark-system isomorphism for Selmer complexes.

The precise target is to construct a commutative diagram whose bottom map is

$$
\det(\mathcal B_N):
\bigwedge^2\operatorname{Sel}_{11}(E/\mathbb Q)
\longrightarrow
\mathscr L_{397,991}
$$

and whose top map is a canonical Selmer-complex/Bockstein determinant specialization.

Only after that identification should one return to the complex comparison

$$
\frac{L^{(2)}(389.a1,1)/2!}{\Omega_E^+\operatorname{Reg}_\infty(E)}.
$$

## References

1. C.-H. Kim, *The structure of Selmer groups and the Iwasawa main conjecture for elliptic curves*, arXiv:2203.12159, final manuscript.
2. F. Castella and T. Sano, *On refined nonvanishing conjectures by Kurihara and Kolyvagin*, arXiv:2601.14504, 2026.
3. D. Macias Castillo and T. Sano, *On Selmer complexes, Stark systems and derived $p$-adic heights*, arXiv:2603.23978, 2026.
4. D. Burns, M. Kurihara and T. Sano, *On derivatives of Kato's Euler system for elliptic curves*, arXiv:1910.07404; J. Math. Soc. Japan 76 (2024), 855--919.
