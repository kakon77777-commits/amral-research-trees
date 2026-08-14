# BSD Next Handoff — P5 Representation Escape

Date: 2026-08-14

## Fixed state

Keep the imported Phase-2 state fixed:

$$
\Sha(389.a1/\mathbb Q)[11^\infty]=0.
$$

Do not spend the next round recomputing the Kurihara witness unless auditing.

## New P5 reduction

Define

$$
\mathcal B_\infty(E)
=
\frac{L^{(2)}(E,1)/2!}{\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)}.
$$

The missing gates are

$$
\mathrm{P5\!\!\!-RAT}:
\mathcal B_\infty(E)\in\mathbb Q^\times
$$

followed by

$$
\mathrm{P5\!\!\!-VAL}_{11}:
 v_{11}(\mathcal B_\infty(E))=0.
$$

Do not write $v_{11}(\mathcal B_\infty(E))$ as a proved invariant before P5-RAT or an equivalent algebraic comparison is established.

## Priority

1. Audit ETNC/determinant-line literature for a theorem proving the required rationality or an algebraic leading-term class without assuming classical BSD.
2. Search for an effective denominator bound from congruence ideals, modular degree, integral zeta elements or determinant lattices.
3. In parallel, prepare a rigorous interval computation for the scalar, but keep it at evidence level until a discrete target set is proved.
4. Treat $p$-adic height/regulator formulas as a separate consistency branch; do not identify them with the real Neron--Tate regulator without an explicit comparison theorem.

## Stop rule

Any theorem whose hypotheses contain the classical rank-$2$ BSD leading-term formula, or a statement equivalent to it, is `CIRCULAR_WITH_BSD` for this target.


## Refined target after ETNC audit

Search directly for `P5-DERPER`: a derived determinant/Bockstein period comparison that identifies the rank-2 augmentation derivative with the classical Neron--Tate regulator lattice without assuming BSD. Broad ETNC or main-conjecture results alone are no longer sufficient search targets.
