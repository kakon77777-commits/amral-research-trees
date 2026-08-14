# BSD P5 v1.1 — Anomalous Norm Localization for $389.a1$ at $p=11$

**Date:** 2026-08-14  
**Curve:** $E=389.a1$  
**Prime:** $p=11$  
**Ramified directions:** $397$ and $991$  
**Status:** exact arithmetic theorem/certificate plus a corrected comparison interface; not a proof of the full Birch--Swinnerton-Dyer conjecture and not a proof of the rank-$2$ Mazur--Tate leading-term formula.

## 0. Claim discipline

This version continues v1.0 and uses the following labels.

- `CLOSED_EXACT`: proved by exact finite computation and elementary arithmetic.
- `EXTERNAL_THEOREM`: a published theorem or definition used as input.
- `REDUCTION`: an exact logical consequence of stated hypotheses.
- `NO_GO`: a previously tempting route whose hypotheses fail here.
- `OPEN`: a comparison theorem that remains unavailable.

In particular, this document does **not** identify the determinant computed from local norm-obstruction lines with the classical Mazur--Tate biextension regulator. The two objects are only compared after an appropriate anomalous Bockstein/height theorem is supplied.

## 1. Inherited left-hand-side certificate

The inherited v1.0 exact certificate uses

$$
n=397\cdot991.
$$

After projection to the $11$-Sylow quotient

$$
G_{11}\simeq C_{11}\times C_{11}
$$

and writing

$$
X_{397}=\gamma_{397}-1,
\qquad
X_{991}=\gamma_{991}-1,
$$

one has, in the deterministic replay normalization,

$$
\overline\theta_n
\equiv
6X_{397}X_{991}
\pmod{I^3}.
$$

Hence

$$
\boxed{
\overline\theta_n\in I^2\setminus I^3
}
$$

and its initial form is a nonzero mixed rank-$2$ class. The scalar $6$ depends on the choice of a nonzero scalar on the one-dimensional mod-$11$ eigenline and on generator choices, whereas the statements

$$
\operatorname{ord}_I(\overline\theta_n)=2
$$

and

$$
[\overline\theta_n]_2\in
\mathbb F_{11}^{\times}X_{397}X_{991}
$$

are invariant under the permitted unit changes.

## 2. The anomalous collision is structural

For the short Weierstrass model

$$
Y^2=X^3-3024X+46224,
$$

the rational generators

$$
P=(0,0),\qquad Q=(1,0)
$$

of the original minimal model map to

$$
P'=(12,108),\qquad Q'=(48,108).
$$

Exact point counting gives

$$
\#E(\mathbb F_{397})=374=34\cdot11,
$$

and

$$
\#E(\mathbb F_{991})=1045=95\cdot11.
$$

Thus

$$
\boxed{
11\mid\#E(\mathbb F_{397}),
\qquad
11\mid\#E(\mathbb F_{991}).
}
$$

This is not accidental. The Kurihara/Kolyvagin condition at a prime $\ell$ is

$$
a_\ell-\ell-1\equiv0\pmod{11},
$$

which is equivalent to

$$
\#E(\mathbb F_\ell)
=\ell+1-a_\ell
\equiv0\pmod{11}.
$$

Therefore the same primes that make the discrete derivative certificate available are automatically anomalous for the classical non-anomalous finite Mazur--Tate height setup.

### External-theorem boundary

Burns--Kurihara--Sano impose, in their Hypothesis 2.2(iii), the condition that the chosen prime $p$ not divide the relevant reduction orders. Under that condition their restricted lattice $E^S(\mathbb Q)$ becomes the full $p$-adic Mordell--Weil lattice and the classical Mazur--Tate pairing may be viewed as a symmetric pairing on that full lattice.

For the present data,

$$
p=11,
\qquad
m=397\cdot991,
$$

and the displayed divisibilities show that this hypothesis fails.

Hence the implication

$$
\text{``classical non-anomalous pairing formula''}
\Longrightarrow
\text{``plug in }397,991\text{''}
$$

is a `NO_GO`.

The computational framework of Bley--Macias Castillo is also not something that can simply be re-run with $p=11$: their published implementation is restricted to $p=3$, and more importantly the arithmetic hypotheses used by the corresponding non-anomalous setup are not automatically satisfied by the present ramified Kolyvagin primes.

## 3. The degree-$11$ ramified local fields

For each

$$
\ell\in\{397,991\},
$$

let $F_\ell$ denote the unique degree-$11$ subfield of the maximal real cyclotomic field

$$
\mathbb Q(\zeta_\ell)^+.
$$

Since

$$
11\mid\frac{\ell-1}{2},
$$

such a field exists and is unique. Its completion at the unique prime above $\ell$ is a tame totally ramified cyclic extension

$$
L_\ell/\mathbb Q_\ell
$$

of degree $11$.

The curve has good reduction at both $397$ and $991$.

## 4. Local norm lemma

### Proposition 4.1 — tame good-reduction norm quotient

Let $K$ be a finite extension of $\mathbb Q_\ell$, let $L/K$ be a tame totally ramified cyclic extension of degree $p$, where $p\ne\ell$, and let $E/K$ have good reduction. Then

$$
\boxed{
E(K)/N_{L/K}E(L)
\simeq
\widetilde E(k)/p\widetilde E(k),
}
$$

where $k$ is the common residue field.

### Proof

Good reduction gives exact reduction sequences

$$
0\to E_1(K)\to E(K)\to\widetilde E(k)\to0
$$

and

$$
0\to E_1(L)\to E(L)\to\widetilde E(k)\to0.
$$

Because $L/K$ is totally ramified, every Galois conjugate of a point has the same reduction. Hence reduction sends the group norm to multiplication by $p$:

$$
\widetilde{N_{L/K}R}=p\widetilde R.
$$

On the formal group, the formal logarithm identifies the norm with the field trace. Since the extension is tame and totally ramified,

$$
\operatorname{Tr}_{L/K}(\mathfrak m_L)=\mathfrak m_K,
$$

so

$$
N_{L/K}:E_1(L)\to E_1(K)
$$

is surjective. Taking the quotient of the two reduction sequences by the norm therefore gives

$$
E(K)/N_{L/K}E(L)
\simeq
\widetilde E(k)/p\widetilde E(k).
$$

This proves the proposition.

## 5. Specialization to $397$ and $991$

Since

$$
v_{11}\bigl(\#E(\mathbb F_{397})\bigr)
=
v_{11}\bigl(\#E(\mathbb F_{991})\bigr)
=1,
$$

each local norm quotient is one-dimensional over $\mathbb F_{11}$:

$$
E(\mathbb Q_{397})/N E(L_{397})
\simeq\mathbb F_{11},
$$

$$
E(\mathbb Q_{991})/N E(L_{991})
\simeq\mathbb F_{11}.
$$

The exact finite-field replay gives, at $397$,

$$
34P'=(281,236),
$$

$$
34Q'=(11,334),
$$

and

$$
\boxed{
34Q'=2(34P').
}
$$

At $991$ it gives

$$
95P'=(39,97),
$$

$$
95Q'=(865,243),
$$

and

$$
\boxed{
95Q'=4(95P').
}
$$

Thus, after choosing the image of $P$ as the basis of each local norm-obstruction line, the localizations of the global basis $P,Q$ are encoded by

$$
\boxed{
M_{\mathrm{loc}}
=
\begin{pmatrix}
1&2\\
1&4
\end{pmatrix}
\in M_2(\mathbb F_{11}).
}
$$

Its determinant is

$$
\boxed{
\det M_{\mathrm{loc}}=2\in\mathbb F_{11}^{\times}.
}
$$

## 6. Rank-$2$ local norm localization theorem

Since

$$
E(\mathbb Q)\simeq\mathbb ZP\oplus\mathbb ZQ
$$

and the torsion subgroup is trivial,

$$
E(\mathbb Q)/11E(\mathbb Q)
\simeq\mathbb F_{11}^2.
$$

The target

$$
E(\mathbb Q_{397})/N E(L_{397})
\oplus
E(\mathbb Q_{991})/N E(L_{991})
$$

is also two-dimensional over $\mathbb F_{11}$. Its localization matrix is $M_{\rm loc}$ and its determinant is nonzero. Therefore:

### Theorem 6.1

$$
\boxed{
E(\mathbb Q)/11E(\mathbb Q)
\xrightarrow{\sim}
E(\mathbb Q_{397})/N E(L_{397})
\oplus
E(\mathbb Q_{991})/N E(L_{991}).
}
$$

This is an exact arithmetic closure, independent of any conjectural complex leading-term comparison.

Equivalently, the two anomalous ramified directions together separate the full rank-$2$ Mordell--Weil lattice modulo $11$.

## 7. Full simultaneous reduction is surjective

The replay also proves that $P'$ generates both finite groups:

$$
\operatorname{ord}_{397}(P')=374,
$$

$$
\operatorname{ord}_{991}(P')=1045.
$$

Moreover,

$$
\boxed{
Q'=244P'
\quad\text{in }E(\mathbb F_{397}),
}
$$

and

$$
\boxed{
Q'=356P'
\quad\text{in }E(\mathbb F_{991}).
}
$$

Hence, in cyclic coordinates, the simultaneous reduction map is

$$
\rho:
\mathbb Z^2
\longrightarrow
\mathbb Z/374\mathbb Z
\oplus
\mathbb Z/1045\mathbb Z,
$$

$$
(a,b)
\longmapsto
(a+244b,\ a+356b).
$$

Since

$$
\gcd(374,1045)=11
$$

and

$$
356-244=112\equiv2\pmod{11},
$$

the compatibility condition in the Chinese remainder problem can be solved for every target pair. Thus $\rho$ is surjective.

An explicit basis of its kernel is

$$
(5742,-22),
$$

$$
(-254980,1045).
$$

Its determinant is

$$
\boxed{
390830
=374\cdot1045.
}
$$

Therefore

$$
\boxed{
[E(\mathbb Q):E^S(\mathbb Q)]=390830,
}
$$

for the subgroup cut out by reduction to zero at $397$ and $991$; the bad-prime component at $389$ contributes no further index because the Tamagawa number is $1$.

In particular,

$$
v_{11}([E(\mathbb Q):E^S(\mathbb Q)])=2.
$$

Under the standard Mazur--Tate/Darmon definition in which $J_S$ is the order of the cokernel of this reduction map, the exact surjectivity gives

$$
\boxed{J_S=1.}
$$

This last statement concerns the original restricted-lattice setup; it must not be confused with the symmetric regulator on the full $11$-adic Mordell--Weil lattice that BKS obtain only under their non-anomalous hypothesis.

## 8. What has and has not been proved on the regulator side

The v1.0 left-hand-side initial class is

$$
[\overline\theta_n]_2
=
6X_{397}X_{991}
$$

in the deterministic modular-symbol normalization.

The v1.1 right-hand-side localization determinant is

$$
\det M_{\rm loc}=2.
$$

Both are nonzero mod $11$. Their quotient in the displayed normalizations is

$$
6/2=3\in\mathbb F_{11}^{\times}.
$$

However,

$$
\boxed{
3\text{ is not asserted to be a Mazur--Tate comparison constant.}
}
$$

The two quantities live in different constructions until an anomalous Bockstein/height comparison identifies the correct arithmetic determinant class with the augmentation-graded Mazur--Tate class.

What is now proved is the stronger structural statement that the arithmetic localization core is primitive:

$$
\boxed{
\det M_{\rm loc}\ne0\pmod{11}.
}
$$

Thus any future comparison failure cannot be blamed on collapse of the two rank directions in local norm space.

## 9. Corrected frontier

The old naive target

$$
\text{``compute the classical symmetric }R_F\text{ at }397,991\text{''}
$$

is removed.

The correct remaining interface is:

$$
\boxed{
\mathrm{P5\! - \!ANOM\! - \!BocCOMP}_{11}^{(2)}
}
$$

with the following meaning.

Construct an integral anomalous finite Bockstein/extended-height regulator for the rank-$2$ Mordell--Weil lattice and the ramification set

$$
\{397,991\},
$$

in a Selmer-complex formalism that remains valid when

$$
11\mid\#E(\mathbb F_\ell),
$$

and prove that its image in

$$
I^2/I^3
$$

matches the exact Mazur--Tate class

$$
[\overline\theta_n]_2
\in
\mathbb F_{11}^{\times}X_{397}X_{991}
$$

at least up to an $11$-adic unit.

The 2026 work of Macias Castillo--Sano shows that determinants of Selmer complexes admit canonical Stark-system interpretations and that two important derived $p$-adic height constructions coincide. This makes a Selmer-complex/Bockstein extension a natural research direction, but their theorem is not asserted here to already prove the present finite tame anomalous comparison.

## 10. Gate state after v1.1

The current state is

$$
\boxed{
\begin{aligned}
\operatorname{ord}_I(\overline\theta_n)&=2 && \text{CLOSED\_EXACT},\\
[\overline\theta_n]_2&\ne0 && \text{CLOSED\_EXACT},\\
11\mid\#E(\mathbb F_{397})& && \text{CLOSED\_EXACT},\\
11\mid\#E(\mathbb F_{991})& && \text{CLOSED\_EXACT},\\
\det M_{\rm loc}&=2\ne0 && \text{CLOSED\_EXACT},\\
E(\mathbb Q)/11E(\mathbb Q)&\xrightarrow{\sim}\bigoplus_{\ell=397,991}E(\mathbb Q_\ell)/NE(L_\ell) && \text{CLOSED\_EXACT},\\
J_S&=1 && \text{CLOSED\_EXACT},\\
\mathrm{P5\! - \!ANOM\! - \!BocCOMP}_{11}^{(2)}& && \textbf{OPEN}.
\end{aligned}
}
$$

The project has therefore isolated a very specific phenomenon:

$$
\boxed{
\text{double Kolyvagin anomaly}
+
\text{nondegenerate rank-2 norm localization}
+
\text{nonzero mixed Mazur--Tate derivative}.
}
$$

The missing theorem is no longer an unspecified high-rank BSD statement. It is a comparison between two already nondegenerate rank-$2$ objects in an anomalous ramified setting.

## 11. External references and their roles

1. D. Burns, M. Kurihara, T. Sano, *On derivatives of Kato's Euler system and the Mazur--Tate Conjecture*, arXiv:2103.11535.  
   Role: classical Mazur--Tate pairing, restricted lattice $E^S(\mathbb Q)$, Bockstein reinterpretation, and the non-anomalous Hypothesis 2.2 used by their main comparison theorem.

2. W. Bley, D. Macias Castillo, *Congruences for critical values of higher derivatives of twisted Hasse--Weil L-functions, III*, arXiv:1912.11260.  
   Role: explicit computation of Galois-valued height pairings through generalized Selmer groups and local Tate/Hilbert-symbol methods; implementation restrictions are not to be confused with theorem-level generality.

3. D. Bullach, M. H. L. Honnor, *On the refined `Birch--Swinnerton-Dyer type' conjectures of Mazur and Tate*, arXiv:2511.07203.  
   Role: modern Selmer/Fitting/eTNC framework with broader local hypotheses, including anomalous cases in its stated range; it does not by itself supply the rank-$2$ anomalous comparison asserted as open above.

4. D. Macias Castillo, T. Sano, *On Selmer complexes, Stark systems and derived $p$-adic heights*, arXiv:2603.23978.  
   Role: canonical determinant-line/Stark-system structure and comparison of derived $p$-adic height constructions; used as a route indicator, not as a completed proof of the finite tame anomalous gate.

## 12. Reproducibility

Run

```text
python scripts/replay_anomalous_norm_localization.py
```

The expected terminal output is

```text
ANOMALOUS_NORM_LOCALIZATION_EXACT
M_loc = [[1, 2], [1, 4]]
det(M_loc) mod 11 = 2
J_S = 1
[E(Q):E^S(Q)] = 390830
```

The script independently recounts the finite fields, verifies the group orders and discrete logarithms, reconstructs the local norm-obstruction slopes, checks the localization determinant, and proves simultaneous reduction surjectivity by exact integer congruence data.
