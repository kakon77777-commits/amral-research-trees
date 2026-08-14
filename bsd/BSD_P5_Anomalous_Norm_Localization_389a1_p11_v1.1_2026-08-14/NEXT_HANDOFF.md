# BSD next handoff after P5 v1.1

Do not recompute the Kurihara witness, the v1.0 augmentation coefficients, the $11$-primary Sha closure, the cyclotomic IMC gate, or the local-unit cancellation.

## Exact inherited state

$$
[\overline\theta_{397\cdot991}]_2
\in
\mathbb F_{11}^{\times}X_{397}X_{991},
$$

with deterministic replay coefficient $6$.

New v1.1 arithmetic closure:

$$
M_{\rm loc}=
\begin{pmatrix}
1&2\\
1&4
\end{pmatrix},
\qquad
\det M_{\rm loc}=2\ne0\pmod{11}.
$$

Thus

$$
E(\mathbb Q)/11E(\mathbb Q)
\xrightarrow{\sim}
E(\mathbb Q_{397})/NE(L_{397})
\oplus
E(\mathbb Q_{991})/NE(L_{991}).
$$

Full reduction data:

$$
Q=244P\text{ in }E(\mathbb F_{397}),
\qquad
Q=356P\text{ in }E(\mathbb F_{991}),
$$

and the simultaneous reduction map is surjective. Hence the relevant reduction cokernel is trivial:

$$
J_S=1.
$$

## Structural obstruction

The Kolyvagin conditions imply

$$
11\mid\#E(\mathbb F_{397}),
\qquad
11\mid\#E(\mathbb F_{991}),
$$

so BKS Hypothesis 2.2(iii) fails for this finite ramification set. Do not use their full-lattice symmetric $R_F$ formula as though the hypothesis held.

## Next target

Construct the correct anomalous finite Bockstein/extended-height determinant and compare it to the exact finite Mazur--Tate class:

$$
\boxed{
\mathrm{P5\! - \!ANOM\! - \!BocCOMP}_{11}^{(2)}.
}
$$

Priority routes:

1. Start from the BKS finite Bockstein map, which is defined before Hypothesis 2.2 is imposed, and identify precisely which later step uses the non-anomalous full-lattice replacement.
2. Replace the full lattice by the restricted lattice $E^S(\mathbb Q)$ or by an extended Selmer-complex determinant that retains the two local norm-obstruction lines.
3. Use the exact localization isomorphism from v1.1 to simplify the local correction complex: both rank directions are already separated mod $11$.
4. Audit Macias Castillo--Sano 2026 for a determinant/Stark-system formulation that can be specialized to a finite tame ramified quotient; do not assume their cyclotomic derived-height comparison automatically gives this finite result.
5. Only after a canonical comparison map exists should one compare its mixed coefficient with the v1.0 class $6X_{397}X_{991}$.
