# BSD P5 v0.8 — Explicit Local-Unit Cancellation for $389.a1$ at $p=11$

**Date:** 2026-08-14  
**Curve:** $E=389.a1$ (Cremona $389a1$)  
**Prime:** $p=11$  
**Status:** exact local-arithmetic reduction; **not** a proof of BSD and **not** a proof of $\mathrm{P5\!-DESC}_{11}$.

---

## 1. Purpose

The v0.7 frontier was reduced to the local-descent and valuation gates

$$
\mathrm{P5\!-DESC}_{11}:
\quad c_{11}\in\mathbb Q_{11},
$$

and

$$
\mathrm{P5\!-VAL0}_{11}:
\quad v_{11}(c_{11})=0.
$$

The goal of v0.8 is to isolate every explicitly computable $11$-local factor in the rank-$2$ Burns--Kurihara--Sano BSD element and determine whether any hidden $11$-denominator survives.

The answer for $389.a1$ is:

$$
\boxed{
\text{the $11$-Euler denominator is cancelled exactly by the $11$-adic logarithm.}
}
$$

The resulting local factor is a $11$-adic unit.

---

## 2. Exact curve data

Use the minimal model

$$
E:\quad y^2+y=x^3+x^2-2x.
$$

The standard invariants give

$$
\Delta_E=389.
$$

Hence $11$ is a prime of good reduction. Direct point counting gives

$$
\#E(\mathbb F_{11})=16,
$$

so

$$
a_{11}=11+1-16=-4.
$$

At the unique bad prime $389$, the minimal discriminant has valuation one. The split-multiplicative criterion gives split reduction, hence the local Euler factor at $389$ is

$$
L_{389}(E,s)=\left(1-389^{-s}\right)^{-1}.
$$

Take the minimal admissible set

$$
S_0=\{\infty,11,389\}.
$$

---

## 3. Exact truncation factor

At the good prime $11$,

$$
L_{11}(E,s)
=
\left(1-a_{11}11^{-s}+11^{1-2s}\right)^{-1}.
$$

Therefore

$$
L_{11}(E,1)^{-1}
=
1-\frac{a_{11}}{11}+\frac1{11}
=
\frac{16}{11}.
$$

At the split multiplicative prime $389$,

$$
L_{389}(E,1)^{-1}
=
1-\frac1{389}
=
\frac{388}{389}.
$$

Since the omitted local factors are nonzero at $s=1$, the order-$2$ leading coefficient satisfies

$$
L_{S_0}^{*}(E,1)
=
L^{*}(E,1)
\frac{16}{11}
\frac{388}{389}.
$$

The $11$-valuation of the rational truncation factor is

$$
v_{11}\left(\frac{16}{11}\frac{388}{389}\right)=-1.
$$

Thus an apparent single $11$-denominator occurs before the logarithmic factor is inserted.

---

## 4. Mordell--Weil basis and the logarithmic factor

Use the Mordell--Weil generator

$$
P=(0,0).
$$

For exact computation pass to

$$
E':\quad Y^2=X^3-3024X+46224
$$

by

$$
X=36x+12,
\qquad
Y=216y+108.
$$

Then

$$
P'=(12,108).
$$

If

$$
\omega=\frac{dx}{2y+1}
$$

is the Neron differential on the minimal model and

$$
\omega'=\frac{dX}{2Y}
$$

on the short model, then

$$
\omega'=\frac{1}{6}\omega.
$$

Hence

$$
\log_{\omega}(P)=6\log_{\omega'}(P').
$$

Since

$$
\#E(\mathbb F_{11})=16,
$$

the point $16P'$ lies in the formal group at $11$. With the standard formal parameter

$$
t=-\frac{X}{Y},
$$

exact rational group-law computation gives

$$
\boxed{
v_{11}\bigl(t(16P')\bigr)=1
}
$$

and

$$
\boxed{
\frac{t(16P')}{11}\equiv7\pmod{11}.
}
$$

For the good-reduction formal group over $\mathbb Z_{11}$, the formal logarithm is an analytic isomorphism on the first formal neighbourhood and, for $t\in11\mathbb Z_{11}$, satisfies

$$
\log_{\omega'}(t)\equiv t\pmod{11^2}.
$$

Therefore

$$
\frac{\log_{\omega'}(16P')}{11}
\equiv7\pmod{11}.
$$

Using

$$
\log_{\omega'}(16P')=16\log_{\omega'}(P'),
$$

and

$$
16^{-1}\equiv9\pmod{11},
$$

one gets

$$
\frac{\log_{\omega'}(P')}{11}
\equiv7\cdot9
\equiv8
\pmod{11}.
$$

Multiplying by the differential-change factor $6$ gives

$$
\boxed{
v_{11}\bigl(\log_{\omega}(P)\bigr)=1
}
$$

and

$$
\boxed{
\frac{\log_{\omega}(P)}{11}
\equiv4\pmod{11}.
}
$$

Thus the logarithmic factor contributes exactly one positive power of $11$.

---

## 5. Exact local cancellation theorem

Define

$$
u_{\mathrm{loc}}
:=
\frac{16}{11}
\frac{388}{389}
\log_{\omega}(P).
$$

Then

$$
v_{11}(u_{\mathrm{loc}})
=
-1+0+1
=0.
$$

Moreover,

$$
16\frac{388}{389}
\equiv1\pmod{11},
$$

and therefore

$$
\boxed{
u_{\mathrm{loc}}\equiv4\pmod{11}.
}
$$

In particular,

$$
\boxed{
u_{\mathrm{loc}}\in\mathbb Z_{11}^{\times}.
}
$$

This is an exact finite certificate. No numerical $L$-value or numerical BSD identity is used in this local-unit computation.

---

## 6. Consequence for the BKS rank-$2$ coefficient

Burns--Kurihara--Sano define the positive-rank BSD element using the complex leading coefficient and a $p$-adic logarithmic factor. In rank $2$, after choosing a Mordell--Weil basis whose first vector is $P$, the coefficient has the schematic form

$$
\frac{L_{S_0}^{*}(E,1)}{\Omega_{\xi}R_{\infty}}
\log_{\omega}(P),
$$

up to the already-fixed algebraic line/basis identifications of v0.7.

Define the remaining normalized complex scalar

$$
\beta_{\xi}
:=
\frac{L^{*}(E,1)}{\Omega_{\xi}R_{\infty}}.
$$

Using the exact truncation identity gives

$$
\frac{L_{S_0}^{*}(E,1)}{\Omega_{\xi}R_{\infty}}
\log_{\omega}(P)
=
\beta_{\xi}\,u_{\mathrm{loc}}.
$$

Since

$$
u_{\mathrm{loc}}\in\mathbb Z_{11}^{\times}
\subset\mathbb Q_{11}^{\times},
$$

multiplication by $u_{\mathrm{loc}}$ neither changes the field-of-definition gate nor the $11$-valuation.

Therefore, for this explicitly normalized rank-$2$ coefficient,

$$
\boxed{
\beta_{\xi}u_{\mathrm{loc}}\in\mathbb Q_{11}
\iff
\beta_{\xi}\in\mathbb Q_{11}.
}
$$

Once descent holds,

$$
\boxed{
v_{11}(\beta_{\xi}u_{\mathrm{loc}})
=
v_{11}(\beta_{\xi}).
}
$$

Hence the local $11$-arithmetic contributes **no residual valuation obstruction**.

---

## 7. Refined P5 frontier

The v0.7 local-descent gate can now be sharpened to the normalized complex scalar itself:

$$
\boxed{
\mathrm{P5\!-DESC}^{\mathrm{red}}_{11}:
\quad
\beta_{\xi}
=
\frac{L^{*}(E,1)}{\Omega_{\xi}R_{\infty}}
\in\mathbb Q_{11}.
}
$$

The unit-level valuation target becomes

$$
\boxed{
\mathrm{P5\!-VAL0}^{\mathrm{red}}_{11}:
\quad
v_{11}(\beta_{\xi})=0.
}
$$

Under the inherited v0.5--v0.7 line identifications and BKS coefficient normalization,

$$
\boxed{
\mathrm{P5\!-LAT}_{11}
\iff
\left(
\mathrm{P5\!-DESC}^{\mathrm{red}}_{11}
\land
\mathrm{P5\!-VAL0}^{\mathrm{red}}_{11}
\right).
}
$$

The important point is negative as well as positive:

$$
\boxed{
\text{there is no hidden $11$-local denominator left to explain.}
}
$$

The remaining wall is genuinely the descent/unit property of the normalized complex rank-$2$ leading scalar.

---

## 8. What this does not prove

This package does **not** prove

$$
\beta_{\xi}\in\mathbb Q_{11},
$$

and does **not** prove

$$
v_{11}(\beta_{\xi})=0.
$$

It also does not identify a numerical approximation of $\beta_{\xi}$ with an exact rational number.

The exact result is only that every explicitly visible $11$-local factor multiplying $\beta_{\xi}$ in the minimal-$S$ BKS rank-$2$ coefficient is a $11$-adic unit, with residue $4$ modulo $11$.

---

## 9. Next target

The next step should attack only

$$
\boxed{
\frac{L^{*}(389.a1,1)}{\Omega_{\xi}R_{\infty}}
\in\mathbb Q_{11}.
}
$$

The highest-value routes are now:

1. derived $p$-TNC rationality at an order-$2$ zero;
2. a motivic/Beilinson rationality theorem for the rank-$2$ normalized leading coefficient;
3. a rank-sensitive finite-layer congruence that determines the same coefficient in a $\mathbb Q_{11}$ determinant line;
4. a representation/base-change escape that factors the rank-$2$ coefficient into already-proved lower-rank leading terms.

The local logarithm, good Euler factor, bad Euler factor, and their $11$-valuation interaction should not be recomputed in the next round.

---

## References

1. D. Burns, M. Kurihara, T. Sano, *On derivatives of Kato's Euler system for elliptic curves*, arXiv:1910.07404.
2. LMFDB, elliptic curve $389.a1$, used as an external cross-check for the standard curve labels and Mordell--Weil generators; the local-unit replay itself recomputes the required $a_{11}$ and discriminant data exactly.
3. Parent project artifact: *BSD P5 v0.7 — GPR(ii) Local-Descent Decomposition for $389.a1$ at $p=11$*.
