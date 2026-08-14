# NEXT HANDOFF — BSD P5 v0.6

## Do not redo

Do not re-run:

- the rank-$2$ Kurihara witness search for $389.a1,p=11$;
- the project proof that $\Sha[11^\infty]=0$;
- the cyclotomic IMC applicability audit;
- the BCS condition-(im) unipotent certificate;
- the $11$-adic regulator nonvanishing search.

## Fixed state

$$
\Sha(389.a1/\mathbb Q)[11^\infty]=0,
$$

$$
\mathrm{P5\!-IMC}_{11}=\mathrm{CLOSED},
$$


and the published Mazur--Stein--Tate expansion gives

$$
R_{11}=4+7\cdot11+6\cdot11^2+11^3+9\cdot11^4+10\cdot11^5+3\cdot11^6+O(11^7),
$$

so

$$
\mathrm{P5\!-BOC\!-NZ}_{11}=\mathrm{CLOSED}.
$$


## New minimal target

Do not aim first at exact full GPR. Aim at

$$
\boxed{
\mathrm{uGPR}_{11}:
\mathbb Z_{11}b_{\mathrm{BSD}}=\Lambda_{11}.
}
$$

Equivalently attack the two gates

$$
\boxed{
\mathrm{P5\!-INT}_{11}:
 b_{\mathrm{BSD}}\in\Lambda_{11},
}
$$


and

$$
\boxed{
\mathrm{P5\!-PRIM}_{11}:
 b_{\mathrm{BSD}}\notin11\Lambda_{11}.
}
$$


The second gate is a one-dimensional mod-$11$ nonvanishing statement once the first gate is proved.

## Priority literature/construction query

Search only for results that can supply one of:

1. a **derived central specialization** of Fouquet/ETNC fundamental lines at a zero of order $2$;
2. a rank-$2$ Mazur--Tate/Kato derivative congruence modulo the exact augmentation power $I^3$ (or equivalent determinant quotient) without assuming BSD/GPR;
3. a comparison of Bockstein/derived $p$-adic height determinants with the complex Neron--Tate leading-term determinant, at least modulo $11$;
4. an effective rationality/denominator theorem for the normalized rank-$2$ complex leading term.

## No-go facts already audited

- Fouquet 2025 assumes the relevant $L(f,r)$ is nonzero at the pointwise TNC specializations.
- Bullach--Honnor 2025 explicitly leave the finer positive-rank congruence dependent on BSD/GPR or an extended height comparison.
- Perrin--Riou--Schneider high-rank $p$-adic BSD controls a $p$-adic $L$-function leading coefficient, not the complex $L^{(2)}(E,1)$ coefficient.

## Success condition for next stage

The next stage counts as a genuine closure only if it proves either

$$
\mathrm{P5\!-INT}_{11}
$$


or

$$
\mathrm{P5\!-PRIM}_{11}
$$


without inserting BSD, GPR, or the desired lattice equality as a hypothesis.
