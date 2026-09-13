# BSD Symbolic Round 002
## Determinant-Line Lift of Rank-2 Calibration

**Date:** 2026-09-13  
**Route:** pure mathematics / symbolic derivation  
**Status:** conditional symbolic development; no new large-scale numerical computation; no claim that BSD is proved  
**Depends on:** BSD Symbolic Round 001, PC-001 cross-curve calibration  
**Target:** identify the precise determinant object needed for a rank-$2$ BSD bridge, prove what can and cannot be obtained from one leading class, and determine the normalization weight of a determinant-level calibration.

---

# 1. Why the vector language is not yet enough

Round 001 established the relative calibration identity

$$
\widehat B_i(t)=C\,A_i(t)\,j(t)\,z_i(t),
$$

with leading term

$$
B_i^{\mathrm{lead}}=C\,A_i(0)\,j_e\,\kappa_i.
$$

For a rank-$2$ target, this removes the common scalar $C$ at vector level. But the BSD regulator is not naturally attached to one vector.

Let $H$ be a two-dimensional Selmer-type space over a field $K$, and let

$$
h:H\times H\longrightarrow K
$$

be a symmetric height pairing. For a basis $P_1,P_2$,

$$
\operatorname{Reg}_h(P_1,P_2)
=
\det
\begin{pmatrix}
h(P_1,P_1) & h(P_1,P_2)\\
h(P_2,P_1) & h(P_2,P_2)
\end{pmatrix}.
$$

Thus the natural arithmetic carrier is

$$
\det H:=\bigwedge^2H.
$$

The first structural question is whether one nonzero BF/Kato leading vector can canonically determine a nonzero element of $\det H$.

The answer is no without extra structure.

---

# 2. No-go theorem for a single vector

Suppose a rule assigns to each nonzero $v\in H$ an element

$$
F(v)\in\det H
$$

and is natural under every basis change:

$$
F(gv)=\det(g)\,F(v)
\qquad
\text{for all }g\in\operatorname{GL}(H).
\tag{2.1}
$$

## Theorem 2.1

Any rule satisfying (2.1) is identically zero.

## Proof

Choose a basis $e_1,e_2$ and take $v=e_1$. For any $b\in K^\times$, let

$$
g_b=
\begin{pmatrix}
1&0\\
0&b
\end{pmatrix}.
$$

Then

$$
g_be_1=e_1,
$$

while

$$
\det(g_b)=b.
$$

Hence

$$
F(e_1)=F(g_be_1)=bF(e_1).
$$

Choosing $b\neq1$ forces

$$
F(e_1)=0.
$$

Every nonzero vector is carried to $e_1$ by some element of $\operatorname{GL}(H)$, so $F$ vanishes identically. QED.

---

# 3. Consequence for the current BSD route

Theorem 2.1 gives a sharp obstruction:

$$
\boxed{
\text{one rank-$2$ leading vector cannot by itself canonically produce the rank-$2$ determinant line.}
}
\tag{3.1}
$$

Therefore a relation such as

$$
\kappa_E=16s_{11}\operatorname{adj}(H)\ell
$$

may encode important rank-$2$ information, but a single vector $\kappa_E$ does not automatically identify

$$
P_1\wedge P_2\in\det H.
$$

At least one extra structure is required:

1. a second independent arithmetic class;
2. a two-dimensional source whose determinant maps into $\det H$;
3. an operator producing an independent derived companion;
4. a dual determinant line together with a determinant pairing;
5. an equivalent derived construction at the Selmer-complex level.

This is a structural necessity, not a numerical deficiency.

---

# 4. The clean determinant object

Let $U$ and $H$ both be two-dimensional $K$-vector spaces and let

$$
\Phi:U\longrightarrow H
$$

be linear.

The canonical determinant-level object is

$$
\det(\Phi):\det U\longrightarrow\det H.
\tag{4.1}
$$

If $\Phi$ has rank two, then $\det(\Phi)$ is nonzero.

Only after choosing

$$
\omega_U\in\det U
$$

does one obtain a target element

$$
\Delta_\Phi:=\det(\Phi)(\omega_U)\in\det H.
\tag{4.2}
$$

Thus the determinant morphism is canonical before any choice of a source-volume generator.

---

# 5. Two-class determinant lift

Assume two independent arithmetic classes

$$
\kappa_1,\kappa_2\in H
$$

and define

$$
\Delta_H:=\kappa_1\wedge\kappa_2.
\tag{5.1}
$$

Suppose their projected realizations satisfy

$$
\widehat\kappa_1=C\,a_1\,\kappa_1,
$$

$$
\widehat\kappa_2=C\,a_2\,\kappa_2,
$$

with the same common comparison scalar $C$.

Then

$$
\widehat\Delta_H
:=
\widehat\kappa_1\wedge\widehat\kappa_2
$$

satisfies

$$
\boxed{
\widehat\Delta_H=C^2a_1a_2\Delta_H.
}
\tag{5.2}
$$

The common normalization appears with degree two at determinant level.

---

# 6. Gauge weight

## Definition 6.1

An object $X$ has gauge weight $w$ if under

$$
C\mapsto uC
$$

it transforms as

$$
X\mapsto u^wX.
$$

A projected class has weight one.

A wedge of two projected classes has weight two.

More generally,

$$
\widehat\kappa_1\wedge\cdots\wedge\widehat\kappa_r
$$

has weight $r$.

---

# 7. Gauge-balance theorem

Let $X_j$ have gauge weight $w_j$. Consider

$$
\mathcal I=\prod_{j=1}^mX_j^{n_j},
$$

whenever the algebraic operations are defined.

## Theorem 7.1

The expression $\mathcal I$ is gauge-invariant exactly when

$$
\boxed{
\sum_{j=1}^mn_jw_j=0.
}
\tag{7.1}
$$

## Proof

Under $C\mapsto uC$,

$$
\mathcal I
\mapsto
u^{\sum_jn_jw_j}\mathcal I.
$$

The exponent must vanish for invariance under every $u\in K^\times$. QED.

---

# 8. Determinant calibration theorem

Let the rank-$2$ target provide two independent classes

$$
\kappa_{E,1},\kappa_{E,2}\in H_E
$$

with

$$
\widehat\kappa_{E,1}
=
C\,a_{E,1}\kappa_{E,1},
$$

$$
\widehat\kappa_{E,2}
=
C\,a_{E,2}\kappa_{E,2}.
$$

Set

$$
\Delta_E
=
\kappa_{E,1}\wedge\kappa_{E,2},
$$

$$
\widehat\Delta_E
=
\widehat\kappa_{E,1}\wedge\widehat\kappa_{E,2}.
$$

Then

$$
\widehat\Delta_E
=
C^2a_{E,1}a_{E,2}\Delta_E.
\tag{8.1}
$$

Let a rank-$0$ calibrator provide

$$
b_0
=
C\,a_0\,k_0,
\qquad
a_0k_0\neq0.
\tag{8.2}
$$

## Theorem 8.1

$$
\boxed{
\Delta_E
=
\frac{a_0^2k_0^2}{a_{E,1}a_{E,2}}
\frac{\widehat\Delta_E}{b_0^2}.
}
\tag{8.3}
$$

## Proof

Square (8.2):

$$
b_0^2=C^2a_0^2k_0^2.
$$

Divide (8.1) by this scalar and rearrange. QED.

Hence

$$
\boxed{
\text{rank-$2$ determinant data must be calibrated against a weight-two quantity.}
}
\tag{8.4}
$$

A single power of a weight-one calibrator does not have the correct normalization degree.

---

# 9. General rank-$r$ determinant calibration

Suppose $H_E$ has dimension $r$ with independent classes

$$
\kappa_{E,1},\ldots,\kappa_{E,r},
$$

and

$$
\widehat\kappa_{E,j}
=
C\,a_{E,j}\kappa_{E,j}.
$$

Define

$$
\Delta_E
=
\bigwedge_{j=1}^r\kappa_{E,j},
$$

$$
\widehat\Delta_E
=
\bigwedge_{j=1}^r\widehat\kappa_{E,j}.
$$

Then

$$
\widehat\Delta_E
=
C^r
\left(
\prod_{j=1}^ra_{E,j}
\right)
\Delta_E.
$$

If

$$
b_0=Ca_0k_0,
$$

then

$$
\boxed{
\Delta_E
=
\frac{a_0^rk_0^r}
{\prod_{j=1}^ra_{E,j}}
\frac{\widehat\Delta_E}{b_0^r}.
}
\tag{9.1}
$$

Thus

$$
\boxed{
\text{rank }r\text{ determinant data has gauge weight }r.
}
\tag{9.2}
$$

---

# 10. The regulator as a determinant tensor

Let

$$
h:H\times H\longrightarrow K
$$

be symmetric. It induces

$$
h^\sharp:H\longrightarrow H^\ast
$$

by

$$
h^\sharp(x)(y)=h(x,y).
$$

Taking determinants gives

$$
\det(h^\sharp):
\det H\longrightarrow\det H^\ast.
$$

Using

$$
\det H^\ast\simeq(\det H)^\ast,
$$

the height determinant is canonically a tensor

$$
\boxed{
\mathcal R_h
\in
(\det H^\ast)^{\otimes2}.
}
\tag{10.1}
$$

For

$$
\Delta=P_1\wedge P_2,
$$

one has

$$
\boxed{
\mathcal R_h(\Delta\otimes\Delta)
=
\det
\begin{pmatrix}
h(P_1,P_1)&h(P_1,P_2)\\
h(P_2,P_1)&h(P_2,P_2)
\end{pmatrix}.
}
\tag{10.2}
$$

So the regulator is naturally a quadratic evaluation on the determinant line, not a linear functional on one Selmer vector.

---

# 11. Gauge weight of the raw scalar regulator

From

$$
\widehat\Delta_E
=
C^2a_{E,1}a_{E,2}\Delta_E
$$

we get

$$
\widehat\Delta_E\otimes\widehat\Delta_E
=
C^4(a_{E,1}a_{E,2})^2
(\Delta_E\otimes\Delta_E).
$$

Therefore

$$
\mathcal R_h(
\widehat\Delta_E\otimes\widehat\Delta_E
)
=
C^4(a_{E,1}a_{E,2})^2
\mathcal R_h(
\Delta_E\otimes\Delta_E
).
$$

Hence

$$
\boxed{
\text{the raw self-paired rank-$2$ regulator scalar has gauge weight }4.
}
\tag{11.1}
$$

This implies that a weight-one calibrator must occur to the fourth power at scalar regulator level.

---

# 12. Calibrated regulator formula

Using Theorem 8.1,

$$
\Delta_E
=
\frac{a_0^2k_0^2}{a_{E,1}a_{E,2}}
\frac{\widehat\Delta_E}{b_0^2}.
$$

Applying the regulator tensor gives

$$
\boxed{
\operatorname{Reg}_h(\Delta_E)
=
\frac{a_0^4k_0^4}
{a_{E,1}^2a_{E,2}^2}
\frac{
\mathcal R_h(
\widehat\Delta_E\otimes\widehat\Delta_E
)
}
{b_0^4}.
}
\tag{12.1}
$$

Thus the common comparison scalar can still be eliminated at determinant and regulator level without solving for it directly, provided the calibration power matches the gauge degree.

---

# 13. Bilinear Selmer/dual-Selmer version

Let $H$ and $H^\vee$ be two-dimensional spaces with perfect pairing

$$
h:H\times H^\vee\longrightarrow K.
$$

Then

$$
\det(h):
\det H\otimes\det H^\vee
\longrightarrow K.
\tag{13.1}
$$

This is linear in each determinant factor separately.

If both determinant classes have gauge weight two, then

$$
\det(h)(
\widehat\Delta_H\otimes\widehat\Delta_{H^\vee}
)
$$

has weight four.

This is the bilinear form of the same degree law.

---

# 14. Candidate mechanism A: two independent derived classes

The direct route is to construct

$$
\kappa_{E,1},\kappa_{E,2}\in H_E
$$

with

$$
\kappa_{E,1}\wedge\kappa_{E,2}\neq0.
$$

Then Sections 5--13 apply immediately.

The difficult step is arithmetic, not exterior algebra:

$$
\boxed{
\text{construct two genuine independent classes with matched normalization.}
}
\tag{14.1}
$$

A scalar regulator ratio cannot manufacture the missing second class.

---

# 15. Candidate mechanism B: a two-dimensional deformation source

Suppose the arithmetic construction depends on two deformation directions, schematically $(X,t)$, and after the correct specialization and quotient operations yields a map

$$
\Phi_E:U_E\longrightarrow H_E,
$$

where

$$
\dim_KU_E=2.
$$

The invariant object is

$$
\det(\Phi_E):
\det U_E
\longrightarrow
\det H_E.
\tag{15.1}
$$

If

$$
\operatorname{rank}\Phi_E=2,
$$

then the determinant map is nonzero.

This is cleaner than selecting two named partial derivatives too early. Coordinate changes act on $\det U_E$, while the line map itself remains canonical.

Thus a promising target is:

$$
\boxed{
\text{identify the correct two-dimensional graded deformation source }U_E.
}
\tag{15.2}
$$

---

# 16. Candidate mechanism C: one class plus a derived companion operator

Suppose

$$
D:H\longrightarrow H
$$

and

$$
\kappa\in H
$$

satisfy

$$
\kappa\wedge D\kappa\neq0.
$$

Define

$$
\Delta_D(\kappa)
=
\kappa\wedge D\kappa.
\tag{16.1}
$$

If

$$
D'
=
uD+a\,\operatorname{Id}_H,
\qquad
u\in K^\times,
$$

then

$$
\kappa\wedge D'\kappa
=
u(\kappa\wedge D\kappa).
$$

Hence

$$
\boxed{
[
\kappa\wedge D\kappa
]
\in
\mathbf P(\det H)
}
\tag{16.2}
$$

is invariant under the affine ambiguity

$$
D\mapsto uD+a\operatorname{Id}_H.
$$

This is the kind of projective robustness desirable from a Bockstein-like or derivative-like companion construction.

This round does not claim that the actual arithmetic Bockstein has exactly this target or transformation law.

---

# 17. Candidate mechanism D: jets of one formal class

Let

$$
z(t)
=
t\kappa_0+t^2\kappa_1+O(t^3),
$$

with

$$
\kappa_0\wedge\kappa_1\neq0.
$$

Let

$$
t'
=
ut+at^2+O(t^3),
\qquad
u\in K^\times.
$$

Then

$$
\kappa_0'
=
u^{-1}\kappa_0,
$$

and

$$
\kappa_1'
=
u^{-2}\kappa_1-au^{-3}\kappa_0.
$$

Therefore

$$
\boxed{
\kappa_0'\wedge\kappa_1'
=
u^{-3}
\kappa_0\wedge\kappa_1.
}
\tag{17.1}
$$

The nonlinear shear term disappears in the wedge.

Hence the projective determinant line generated by the first two independent jets survives nonlinear reparametrization, although the absolute scale carries a known coordinate weight.

The current target data, however, only fixes the first leading vector. A second independent jet is not yet established.

---

# 18. Determinant degree of quotient transport

Suppose the common quotient transport rescales every weight-one projected class by

$$
q_{\mathbf f}^{-1}.
$$

Then a two-class determinant is rescaled by

$$
q_{\mathbf f}^{-2},
$$

and its self-paired regulator scalar by

$$
q_{\mathbf f}^{-4}.
$$

If the rank-$0$ calibrator has the same weight-one transport, then

$$
b_0^2
$$

cancels the determinant transport and

$$
b_0^4
$$

cancels the regulator transport.

Therefore the correct goal is not

$$
q_{\mathbf f}=1.
$$

It is degree-matched cancellation.

---

# 19. Relative and absolute determinant data

There are three layers.

## 19.1 Projective determinant direction

One may know only

$$
[\Delta_E]\in\mathbf P(\det H_E).
$$

## 19.2 Calibrated determinant element

One may construct

$$
\Delta_E^{\mathrm{cal}}
\sim
\frac{\widehat\Delta_E}{b_0^2},
$$

with the explicit arithmetic factors restored by Theorem 8.1.

This removes the common BF gauge.

## 19.3 Absolute BSD determinant

To compare with the classical BSD regulator, one still needs an identification between the calibrated determinant line and the determinant of the actual Mordell--Weil lattice, or the correct Selmer-complex analogue.

Thus

$$
\boxed{
\text{the final obstruction is not necessarily the BF comparison scalar.}
}
$$

A sharper statement is

$$
\boxed{
\text{the remaining structural problem is the absolute arithmetic determinant identification.}
}
\tag{19.1}
$$

---

# 20. The lattice determinant

Let

$$
\Lambda\subset H
$$

be a rank-$2$ lattice with basis $P_1,P_2$. Define

$$
\Delta_\Lambda=P_1\wedge P_2.
$$

Changing the integral basis by

$$
G\in\operatorname{GL}_2(\mathbf Z)
$$

changes $\Delta_\Lambda$ by

$$
\det(G)\in\{1,-1\}.
$$

The regulator uses

$$
\mathcal R_h(
\Delta_\Lambda\otimes\Delta_\Lambda
),
$$

so this sign disappears.

Therefore the main absolute issue is not orientation. It is the scale needed to identify the $K$-normalized BF determinant with the integral or rational Mordell--Weil determinant lattice.

---

# 21. Conditional determinant bridge template

Assume:

1. a rank-$2$ arithmetic space $H_E$;
2. a two-dimensional derived source $U_E$;
3. a rank-two map

$$
\Phi_E:U_E\longrightarrow H_E;
$$

4. a projected realization carrying the same weight-one comparison factor on each source direction;
5. a rank-$0$ calibrator

$$
b_0=Ca_0k_0;
$$

6. an arithmetic determinant comparison with the Mordell--Weil or Selmer determinant line;
7. a height determinant tensor.

Then determinant formation produces a weight-two projected object, and the common scalar is removed by $b_0^2$.

After the arithmetic determinant identification, the scalar regulator is obtained by applying the determinant height tensor, with gauge cancellation occurring through $b_0^4$.

This factorizes the final BSD bridge into:

$$
\boxed{
\text{BF normalization problem}
}
$$

and

$$
\boxed{
\text{absolute arithmetic determinant identification problem}.
}
$$

Round 001 weakens the first. This round isolates the second.

---

# 22. Main new obstruction and diagnostic

The combined result of Sections 2 and 5--12 is:

$$
\boxed{
\text{a single calibrated rank-$2$ vector is insufficient for a canonical rank-$2$ regulator bridge.}
}
\tag{22.1}
$$

A valid route must produce determinant degree two.

Moreover:

$$
\boxed{
\text{rank-$2$ determinant level requires gauge weight two,}
}
$$

while

$$
\boxed{
\text{self-paired regulator level requires gauge weight four.}
}
$$

This yields an immediate symbolic red-flag test:

> If a proposed rank-$2$ determinant bridge cancels a common weight-one BF normalization using only one power of a rank-$0$ calibrator, the normalization degrees do not match.

No numerical computation is required to detect this failure.

---

# 23. Proved in this round

Under the stated linear-algebraic hypotheses, this round proves:

1. the single-vector no-go theorem;
2. the two-class determinant scaling law;
3. the gauge-balance criterion;
4. the determinant calibration formula;
5. the general rank-$r$ determinant calibration law;
6. the determinant-tensor formulation of the height regulator;
7. the weight-four law for a self-paired rank-$2$ regulator scalar;
8. the calibrated regulator formula;
9. projective invariance of $\kappa\wedge D\kappa$ under

$$
D\mapsto uD+a\operatorname{Id};
$$

10. the first nontrivial jet-wedge transformation law;
11. the separation between BF gauge removal and absolute lattice determinant identification.

---

# 24. Not proved

This round does not prove:

1. that the actual Beilinson--Flach family supplies two independent target classes;
2. that the correct two-dimensional arithmetic source $U_E$ has been constructed;
3. that an arithmetic Bockstein operator has the properties assumed in Section 16;
4. that a second cyclotomic jet is independent;
5. that the projected determinant is nonzero;
6. that Kato, Coleman, adjoint and modular-symbol period transports agree at determinant level;
7. that the calibrated determinant equals the Mordell--Weil lattice determinant;
8. lattice saturation;
9. equality of the relevant $p$-adic determinant with the archimedean BSD regulator;
10. BSD.

---

# 25. Local verification checklist

The local machines should attack the arithmetic hypotheses rather than the exterior-algebra identities.

## V1. Second-class test

Construct or detect two target classes and verify

$$
\kappa_{E,1}\wedge\kappa_{E,2}\neq0.
$$

## V2. Two-dimensional source test

If the mixed deformation source is used, identify the exact graded source $U_E$ and verify

$$
\operatorname{rank}\Phi_E=2.
$$

## V3. Gauge-degree test

Track the common comparison factor through:

- class level: degree one;
- determinant level: degree two;
- self-paired regulator level: degree four.

## V4. Quotient-transport degree test

Track $q_{\mathbf f}$ through the same three levels.

## V5. Calibrator-square test

Test stability of

$$
\frac{\widehat\Delta_E}{b_0^2}
$$

under any implemented common projected-quotient rescaling.

## V6. Determinant-lattice comparison test

Identify the map from the calibrated determinant line to

$$
K\otimes\det E(\mathbf Q)_{\mathrm{free}}
$$

or the appropriate Selmer determinant line.

## V7. Regulator-fourth-power test

If a raw scalar regulator observable is constructed from the BF determinant, test whether division by

$$
b_0^4
$$

removes the common weight-one normalization.

---

# 26. Main conclusion

The symbolic structure now separates into three normalization levels:

$$
\text{weight-one projected classes},
$$

$$
\text{weight-two determinant class},
$$

and

$$
\text{weight-four self-paired regulator scalar}.
$$

The rank-$0$ calibrator can remove the common comparison scalar at every level, but only with the correct power.

For the rank-$2$ determinant:

$$
\boxed{
\Delta_E
\propto
\frac{\widehat\Delta_E}{b_0^2}.
}
$$

For the self-paired regulator:

$$
\boxed{
\operatorname{Reg}_E
\propto
\frac{
\mathcal R_h(
\widehat\Delta_E\otimes\widehat\Delta_E
)
}{b_0^4}.
}
$$

The unresolved problem is therefore:

$$
\boxed{
\text{construct a genuine degree-two arithmetic determinant object and identify it with the absolute Mordell--Weil or Selmer determinant line.}
}
$$

The common BF comparison scalar is no longer the conceptual center of the problem.

---

# 27. Proposed next round

## BSD Symbolic Round 003

**Title:**

> Two-Variable Jet Determinant and Bockstein Bridge

The next task should compare three plausible determinant-producing mechanisms:

1. two independent BF/Kato classes;
2. the mixed $(X,t)$ deformation source and its determinant map;
3. one leading class plus a Bockstein or derived companion operator.

The target is an equivalence criterion, or an exact obstruction theorem, for relations of the schematic form

$$
\det(\Phi_E)
\sim
\kappa_E\wedge D\kappa_E
\sim
\text{mixed-jet determinant},
$$

up to explicitly controlled gauge and coordinate factors.

If such a theorem holds, the search for an arbitrary second class can be replaced by the search for one canonical derived operator or one canonical two-dimensional deformation source.
