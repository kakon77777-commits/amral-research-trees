# BSD P5 v1.2 — Norm-Selmer Core-Vertex Certificate for $389.a1$ at $p=11$

**Date:** 2026-08-14  
**Curve:** $E=389.a1$  
**Prime:** $p=11$  
**Dependency:** the inherited theorem-chain closure $\Sha(E/\mathbb Q)[11]=0$ and the exact v1.1 anomalous norm-localization certificate.  
**Status:** exact finite Selmer-structure theorem under the stated inherited dependency; not a proof of the full BSD conjecture and not yet the anomalous Mazur--Tate/Bockstein comparison.

## 0. Input from v1.1

Let

$$
L_{397}/\mathbb Q_{397},
\qquad
L_{991}/\mathbb Q_{991}
$$

be the tame totally ramified degree-$11$ local extensions obtained from the degree-$11$ real cyclotomic subfields at $397$ and $991$.

Version 1.1 proved

$$
E(\mathbb Q_{397})/N E(L_{397})\simeq\mathbb F_{11},
$$

$$
E(\mathbb Q_{991})/N E(L_{991})\simeq\mathbb F_{11},
$$

and, relative to the Mordell--Weil basis

$$
P=(0,0),\qquad Q=(1,0),
$$

the localization matrix is

$$
\boxed{
M_{\rm loc}
=
\begin{pmatrix}
1&2\\
1&4
\end{pmatrix}.
}
$$

Hence

$$
\det M_{\rm loc}=2\in\mathbb F_{11}^{\times}.
$$

## 1. From Mordell--Weil to the mod-$11$ Selmer group

The Kummer exact sequence gives

$$
0\longrightarrow
E(\mathbb Q)/11E(\mathbb Q)
\longrightarrow
\operatorname{Sel}_{11}(E/\mathbb Q)
\longrightarrow
\Sha(E/\mathbb Q)[11]
\longrightarrow0.
$$

Using the inherited closure

$$
\Sha(E/\mathbb Q)[11]=0,
$$

we obtain

$$
\boxed{
\operatorname{Sel}_{11}(E/\mathbb Q)
\simeq
E(\mathbb Q)/11E(\mathbb Q)
\simeq
\mathbb F_{11}^2.
}
$$

Thus every mod-$11$ Selmer class is represented by a global Mordell--Weil point modulo $11$.

## 2. Norm local-condition maps

For

$$
\ell\in\{397,991\},
$$

one has

$$
11E(\mathbb Q_\ell)
\subseteq
N_{L_\ell/\mathbb Q_\ell}E(L_\ell),
$$

because a point already defined over $\mathbb Q_\ell$ has norm equal to its $11$-fold multiple.

Therefore the quotient map

$$
E(\mathbb Q_\ell)/11E(\mathbb Q_\ell)
\longrightarrow
E(\mathbb Q_\ell)/N E(L_\ell)
$$

is well-defined. Composing localization of Selmer classes with this quotient gives

$$
\lambda_\ell:
\operatorname{Sel}_{11}(E/\mathbb Q)
\longrightarrow
E(\mathbb Q_\ell)/N E(L_\ell).
$$

Relative to the basis $P,Q$ and the local bases fixed in v1.1,

$$
\lambda_{397}(aP+bQ)=a+2b,
$$

and

$$
\lambda_{991}(aP+bQ)=a+4b
$$

in $\mathbb F_{11}$.

## 3. Modified norm-Selmer groups

For any subset

$$
T\subseteq\{397,991\},
$$

define

$$
\operatorname{Sel}^{N_T}_{11}(E/\mathbb Q)
:=
\bigcap_{\ell\in T}\ker(\lambda_\ell).
$$

This is the subgroup of mod-$11$ Selmer classes satisfying the norm local condition at every prime in $T$.

For $T=\varnothing$,

$$
\dim_{\mathbb F_{11}}
\operatorname{Sel}^{N_\varnothing}_{11}(E/\mathbb Q)=2.
$$

At $397$,

$$
a+2b=0,
$$

so

$$
\boxed{
\operatorname{Sel}^{N_{397}}_{11}(E/\mathbb Q)
=
\mathbb F_{11}(Q-2P),
}
$$

and therefore

$$
\dim_{\mathbb F_{11}}
\operatorname{Sel}^{N_{397}}_{11}(E/\mathbb Q)=1.
$$

At $991$,

$$
a+4b=0,
$$

so

$$
\boxed{
\operatorname{Sel}^{N_{991}}_{11}(E/\mathbb Q)
=
\mathbb F_{11}(Q-4P),
}
$$

and

$$
\dim_{\mathbb F_{11}}
\operatorname{Sel}^{N_{991}}_{11}(E/\mathbb Q)=1.
$$

Imposing both norm conditions gives

$$
\begin{pmatrix}
1&2\\
1&4
\end{pmatrix}
\begin{pmatrix}
a\\b
\end{pmatrix}
=0.
$$

Since the determinant is $2\ne0$ in $\mathbb F_{11}$,

$$
\boxed{
\operatorname{Sel}^{N_{397,991}}_{11}(E/\mathbb Q)=0.
}
$$

Hence the exact dimension cube is

$$
\boxed{
2\longrightarrow1,
\qquad
2\longrightarrow1,
\qquad
1\cap1\longrightarrow0.
}
$$

Equivalently, by cardinality,

$$
\boxed{
121\longrightarrow11\longrightarrow1.
}
$$

## 4. Core-vertex localization theorem

The combined map

$$
\lambda_{397}\oplus\lambda_{991}:
\operatorname{Sel}_{11}(E/\mathbb Q)
\longrightarrow
E(\mathbb Q_{397})/N E(L_{397})
\oplus
E(\mathbb Q_{991})/N E(L_{991})
$$

has matrix $M_{\rm loc}$ and is therefore an isomorphism.

### Theorem 4.1

Under the inherited closure $\Sha(E/\mathbb Q)[11]=0$,

$$
\boxed{
\operatorname{Sel}_{11}(E/\mathbb Q)
\xrightarrow{\sim}
E(\mathbb Q_{397})/N E(L_{397})
\oplus
E(\mathbb Q_{991})/N E(L_{991}).
}
$$

In particular, the two norm local conditions form a complete rank-$2$ killing set for the mod-$11$ Selmer group.

This is the finite Selmer skeleton that the v1.1 arithmetic localization determinant was detecting.

## 5. Transversality of the two rank-$1$ faces

The two one-dimensional norm-Selmer faces are

$$
K_{397}=\mathbb F_{11}(Q-2P),
$$

and

$$
K_{991}=\mathbb F_{11}(Q-4P).
$$

Their coordinate columns relative to $P,Q$ are

$$
\begin{pmatrix}-2\\1\end{pmatrix},
\qquad
\begin{pmatrix}-4\\1\end{pmatrix}.
$$

The wedge coefficient is

$$
(-2)(1)-(-4)(1)=2.
$$

Thus

$$
\boxed{
(Q-2P)\wedge(Q-4P)
=2(P\wedge Q)
\quad\text{in }
\bigwedge^2(E(\mathbb Q)/11E(\mathbb Q)).
}
$$

Since $2\in\mathbb F_{11}^{\times}$, the two rank-$1$ faces are primitive and transverse:

$$
K_{397}\cap K_{991}=0,
$$

$$
K_{397}+K_{991}=\operatorname{Sel}_{11}(E/\mathbb Q).
$$

## 6. Relation to the v1.0 finite Mazur--Tate class

The modular-symbol side has the exact primitive mixed class

$$
[\overline\theta_{397\cdot991}]_2
=
6X_{397}X_{991}
$$

in the deterministic replay normalization.

The arithmetic norm-Selmer skeleton has the primitive determinant

$$
\det M_{\rm loc}=2.
$$

Thus both sides now possess nonzero rank-$2$ determinant data over $\mathbb F_{11}$.

However,

$$
\boxed{
\text{no equality between the scalars }6\text{ and }2\text{ is asserted.}
}
$$

A comparison map is still required to place the two determinants in the same canonical line.

## 7. New precise frontier

Version 1.1 introduced the open gate

$$
\mathrm{P5\! - \!ANOM\! - \!BocCOMP}_{11}^{(2)}.
$$

Version 1.2 closes the purely finite Selmer prerequisite for that gate:

$$
\boxed{
\mathrm{P5\! - \!NORM\! - \!COREVERTEX}_{11}^{(2)}
=
\mathrm{CLOSED\_EXACT}.
}
$$

The remaining task is no longer to discover whether the two anomalous directions detect the rank-$2$ arithmetic space. They do, and they do so isomorphically.

The remaining task is to construct the correct anomalous Bockstein/extended-height comparison map and prove that it transports this primitive Selmer determinant to the finite Mazur--Tate initial form in $I^2/I^3$.

Schematically,

$$
\boxed{
\begin{array}{ccc}
\operatorname{Sel}_{11}(E/\mathbb Q)
&\xrightarrow{\sim}&
L_{397}\oplus L_{991}\\
\downarrow\det&&\downarrow\det\\
\text{arithmetic determinant line}
&\dashrightarrow&
I^2/I^3
\end{array}
}
$$

where

$$
L_\ell:=E(\mathbb Q_\ell)/N E(L_\ell)\simeq\mathbb F_{11}.
$$

The dashed arrow is precisely the unproved anomalous Bockstein comparison.

## 8. Gate state after v1.2

$$
\boxed{
\begin{aligned}
\Sha(E/\mathbb Q)[11]&=0 && \text{INHERITED\_CLOSED},\\
\dim\operatorname{Sel}_{11}(E/\mathbb Q)&=2 && \text{CLOSED},\\
\dim\operatorname{Sel}^{N_{397}}_{11}&=1 && \text{CLOSED\_EXACT},\\
\dim\operatorname{Sel}^{N_{991}}_{11}&=1 && \text{CLOSED\_EXACT},\\
\operatorname{Sel}^{N_{397,991}}_{11}&=0 && \text{CLOSED\_EXACT},\\
\det M_{\rm loc}&=2\ne0 && \text{CLOSED\_EXACT},\\
\mathrm{P5\! - \!NORM\! - \!COREVERTEX}_{11}^{(2)}& && \text{CLOSED\_EXACT},\\
\mathrm{P5\! - \!ANOM\! - \!BocCOMP}_{11}^{(2)}& && \mathbf{OPEN}.
\end{aligned}
}
$$

## 9. Reproducibility

Run

```text
python scripts/replay_norm_selmer_cube.py
```

Expected output:

```text
NORM_SELMER_CORE_VERTEX_EXACT
dims = 2, 1, 1, 0
K_397 = <Q-2P>
K_991 = <Q-4P>
wedge coefficient mod 11 = 2
```
