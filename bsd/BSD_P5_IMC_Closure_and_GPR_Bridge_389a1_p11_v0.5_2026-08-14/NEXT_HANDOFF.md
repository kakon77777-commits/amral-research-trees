# NEXT HANDOFF — BSD P5 after v0.5

## Fixed state

Do not re-run the $p=11$ Kurihara search or the cyclotomic IMC literature audit.

Current fixed state for $E=389.a1$, $p=11$:

$$
\Sha(E/\mathbb Q)[11^\infty]=0.
$$

$$
\mathrm{P5\!\!-IMC}_{11}=\mathrm{CLOSED}.
$$

The full IMC closure uses Burungale--Castella--Skinner Theorem 1.1.2 and an explicit proof of condition $(\mathrm{im})$ from maximal $11$-adic image.

## Immediate task 1: finite replay

Run

```text
sage scripts/replay_padic_regulator_11.sage
```

Preserve full stdout. If the returned $11$-adic regulator is nonzero, promote

```text
P5-BOC-NZ11 = CLOSED_EXACT_LOCAL_REPLAY
```

using the BKS p-adic-height/Bockstein relation.

## Immediate task 2: conceptual frontier

Attack only

$$
\boxed{\mathrm{P5\!\!-GPR}_{11}}
$$

for the rank-$2$ curve $389.a1$.

The target comparison is

$$
\kappa_\infty
=
\frac{L_S^*(E,1)}{\Omega_\xi R_\infty}
R_\omega^{\mathrm{Boc}}.
$$

Priority order:

1. Search 2025--2026 follow-up papers for an actual rank-$2$ proof or a one-prime lattice form of Generalized Perrin--Riou.
2. Audit whether a theorem for this specific prime-conductor semistable curve is stronger than the general arbitrary-rank statement.
3. If no theorem exists, formulate the weakest local comparison sufficient for

$$
L^*(E,1)\mathbb Z_{11}
=
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)\mathbb Z_{11}.
$$

4. Keep cyclotomic derivatives, Kurihara derivatives, Mazur--Tate augmentation derivatives, and complex $s$-derivatives as distinct typed objects until a comparison theorem is supplied.

## No-go routes already audited

- Full cyclotomic IMC alone does not identify the complex rank-$2$ leading term.
- Discrete Kurihara/Mazur--Tate derivatives cannot be equated with $L^{(2)}(E,1)$ by analogy.
- Anticyclotomic/base-change derived formulas transport rather than remove the archimedean comparison gate.
- Global rationality of the displayed BSD scalar is a valid stronger route but is not the minimal one-prime target.

## Completion criterion for P5 at $p=11$

P5 is closed only when both are available:

```text
P5-BOC-NZ11 = CLOSED
P5-GPR11    = CLOSED
```

Then BKS gives

$$
\boxed{
L^*(E,1)\mathbb Z_{11}
=
\Omega_E\operatorname{Reg}^{\mathrm{NT}}(E)\mathbb Z_{11}.
}
$$

Do not call this full BSD; it is one-prime rank-$2$ leading-term closure.
