# BSD next handoff after P5 v1.2

Do not recompute v1.0 augmentation coefficients or v1.1 finite-field/local-norm data.

## Exact finite Selmer state

Using inherited $\Sha[11]=0$:

$$
\operatorname{Sel}_{11}(E/\mathbb Q)=\mathbb F_{11}P\oplus\mathbb F_{11}Q.
$$

Norm-localization rows:

$$
\lambda_{397}=(1,2),
\qquad
\lambda_{991}=(1,4).
$$

Single-prime norm-Selmer lines:

$$
K_{397}=\mathbb F_{11}(Q-2P),
$$

$$
K_{991}=\mathbb F_{11}(Q-4P).
$$

Double norm condition:

$$
K_{397}\cap K_{991}=0.
$$

Primitive wedge:

$$
(Q-2P)\wedge(Q-4P)=2(P\wedge Q).
$$

## Left modular element

Inherited v1.0:

$$
[\overline\theta_{397\cdot991}]_2
\in
\mathbb F_{11}^{\times}X_{397}X_{991},
$$

with deterministic coefficient $6$.

## Next gate

$$
\boxed{
\mathrm{P5\! - \!ANOM\! - \!BocCOMP}_{11}^{(2)}.
}
$$

The next proof attempt should not ask whether the two local directions detect the rank. That is closed. It should construct a canonical determinant/Bockstein map from the norm-modified Selmer complex to the augmentation-graded group ring and identify its image with the v1.0 finite Mazur--Tate class, at least up to $\mathbb F_{11}^{\times}$.

Suggested route:

1. Encode the two norm local conditions as a mapping-cone modification of the standard mod-$11$ Selmer complex.
2. Because the localization map is an isomorphism, simplify the resulting determinant line explicitly.
3. Compare this finite determinant construction with the BKS finite Bockstein map, which exists before their non-anomalous full-lattice replacement.
4. Audit whether the 2026 determinant-to-Stark-system theorem of Macias Castillo--Sano extends to this finite local-condition complex without extra hypotheses.
5. Only after a canonical line map is defined should the scalar relation to the modular coefficient $6$ be studied.
