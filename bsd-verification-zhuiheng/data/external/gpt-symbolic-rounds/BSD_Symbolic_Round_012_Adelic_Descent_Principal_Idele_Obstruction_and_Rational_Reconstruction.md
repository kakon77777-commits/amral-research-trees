# BSD Symbolic Round 012
## Adelic Descent, Principal-Idele Obstruction, and Rational Reconstruction

**Date:** 2026-09-13  
**Route:** pure mathematics / symbolic derivation  
**Status:** conditional symbolic development; no new large-scale numerical computation; no claim that BSD is proved  
**Depends on:** BSD Symbolic Round 001--011  
**Goal:** refine the global rational-descent blocker by separating projective-line descent, determinant-lattice descent, and exact-element descent; identify the principal-idele obstruction; prove what finite valuations can reconstruct over $\mathbf Q$; and isolate the part that still cannot be replaced by local precision.

---

# 1. The descent problem has three different levels

Let

$$
D_{\mathbf Q}
$$

be a one-dimensional rational determinant space with primitive arithmetic lattice

$$
D_{\mathbf Z}
=
\mathbf Z\Delta_\Lambda.
$$

For every place $v$ of $\mathbf Q$, set

$$
D_v
=
D_{\mathbf Q}\otimes_{\mathbf Q}\mathbf Q_v.
$$

A local nonzero determinant element can be written

$$
\Delta_v
=
a_v\Delta_\Lambda,
\qquad
a_v\in\mathbf Q_v^\times.
\tag{1.1}
$$

There are three logically distinct descent questions.

### Level P: projective-line descent

Does $\Delta_v$ lie on the same one-dimensional line?

In a one-dimensional space this is almost vacuous.

### Level L: lattice-class descent

What is the local position of

$$
\mathbf Z_v\Delta_v
$$

relative to

$$
\mathbf Z_v\Delta_\Lambda?
$$

At a finite prime $p$, this only sees

$$
v_p(a_p).
$$

### Level E: exact-element descent

Does there exist

$$
a\in\mathbf Q^\times
$$

such that

$$
a_v=a
$$

inside every completion?

This is the genuine principal-idele problem.

These three levels must not be conflated.

---

# 2. Finite local lattice classes are only valuations

For every finite prime $p$,

$$
\mathbf Q_p^\times
\simeq
p^{\mathbf Z}
\times
\mathbf Z_p^\times.
$$

Therefore

$$
\boxed{
\mathbf Q_p^\times/\mathbf Z_p^\times
\simeq
\mathbf Z
}
\tag{2.1}
$$

by the valuation map.

Hence the local determinant-lattice class of $\Delta_p$ is completely determined by

$$
d_p
:=
v_p(a_p).
\tag{2.2}
$$

The local unit part of $a_p$ is invisible at lattice level.

---

# 3. Global determinant torsor over $\mathbf Q$

The prime-factorization theorem gives

$$
\boxed{
\mathbf Q^\times/\{\pm1\}
\simeq
\bigoplus_p \mathbf Z,
}
\tag{3.1}
$$

where the map is

$$
[a]
\longmapsto
\left(
v_p(a)
\right)_p.
$$

Only finitely many entries are nonzero.

Therefore:

## Theorem 3.1

Every finite-support valuation vector

$$
(d_p)_p
\in
\bigoplus_p\mathbf Z
$$

determines a unique global determinant torsor class

$$
[a]\in
\mathbf Q^\times/\{\pm1\}.
$$

Explicitly,

$$
\boxed{
a_0
=
\prod_p
p^{d_p}
}
\tag{3.2}
$$

is the unique positive representative.

This is stronger than the generic number-field situation because $\mathbf Q$ has trivial ideal class group.

---

# 4. Lattice-class globalization over $\mathbf Q$

Suppose one has genuine local determinant-lattice defects

$$
d_p
$$

with finite support.

Then Theorem 3.1 produces a unique global rational lattice-scale class

$$
[a_0].
$$

Thus:

$$
\boxed{
\text{finite-support local lattice classes always globalize over }\mathbf Q.
}
\tag{4.1}
$$

No additional ideal-class obstruction exists.

This gives a first refinement of Round 010's T1:

> at the level of determinant lattices modulo local units, global rational reconstruction is automatic once the local valuations are genuine and finitely supported.

But this does not yet descend exact local elements.

---

# 5. Exact local elements form an idele

Let

$$
\mathbf A_{\mathbf Q}^\times
$$

be the idele group of $\mathbf Q$.

An exact compatible family

$$
a=(a_v)_v
$$

with

$$
a_p\in\mathbf Q_p^\times
$$

and almost all

$$
a_p\in\mathbf Z_p^\times
$$

is an idele.

Exact global descent asks whether

$$
a
$$

lies in the diagonal image

$$
\mathbf Q^\times
\hookrightarrow
\mathbf A_{\mathbf Q}^\times.
$$

Equivalently:

$$
\boxed{
[a]=1
\quad
\text{in }
\mathbf A_{\mathbf Q}^\times/\mathbf Q^\times.
}
\tag{5.1}
$$

This is the principal-idele criterion.

---

# 6. Normalize the valuation part

Given an idele

$$
a=(a_\infty,(a_p)_p),
$$

define

$$
d_p=v_p(a_p)
$$

and

$$
q_0
:=
\prod_p
p^{d_p}
\in
\mathbf Q_{>0}^\times.
\tag{6.1}
$$

Then for every finite prime,

$$
u_p
:=
a_p/q_0
\in
\mathbf Z_p^\times.
\tag{6.2}
$$

At the real place define

$$
u_\infty
:=
a_\infty/q_0
\in
\mathbf R^\times.
\tag{6.3}
$$

So every idele splits into

$$
\boxed{
a
=
q_0\cdot u,
}
\tag{6.4}
$$

where

$$
u
\in
\mathbf R^\times
\times
\widehat{\mathbf Z}^{\,\times}.
$$

The rational number $q_0$ absorbs all finite valuations.

The remaining obstruction is entirely in the unit idele $u$.

---

# 7. Principal-idele criterion over $\mathbf Q$

## Theorem 7.1

The idele $a$ is principal if and only if there exists

$$
\epsilon\in\{+1,-1\}
$$

such that

$$
\boxed{
u_\infty=\epsilon
}
\tag{7.1}
$$

and

$$
\boxed{
u_p=\epsilon
\quad
\text{inside }\mathbf Q_p^\times
\text{ for every }p.
}
\tag{7.2}
$$

In that case

$$
\boxed{
a
=
\epsilon q_0
}
\tag{7.3}
$$

diagonally at every place.

## Proof

If $a$ is principal, write

$$
a=q
$$

for some $q\in\mathbf Q^\times$.

Its finite valuations are $d_p$, so

$$
q
=
\epsilon q_0
$$

for a unique sign $\epsilon$.

Hence every normalized component is the same diagonal unit $\epsilon$.

Conversely, if all normalized components equal the same sign $\epsilon$, then $a$ is the diagonal image of $\epsilon q_0$. QED.

---

# 8. The residual compact unit obstruction

After removing all valuations, exact descent still has to kill the finite-unit tuple

$$
(u_p)_p
\in
\widehat{\mathbf Z}^{\,\times}.
$$

Modulo the diagonal rational units

$$
\{\pm1\},
$$

the residual obstruction lives in

$$
\boxed{
\widehat{\mathbf Z}^{\,\times}/\{\pm1\}.
}
\tag{8.1}
$$

Therefore the vanishing of all local valuation defects does not imply exact global descent.

One can have

$$
d_p=0
\quad
\text{for every }p,
$$

while

$$
(u_p)_p
$$

is not the diagonal unit $+1$ or $-1$.

This is the exact-element obstruction that lattice data cannot see.

---

# 9. Product formula is necessary but not sufficient

Define the idele norm

$$
\|a\|
=
|a_\infty|
\prod_p
|a_p|_p.
\tag{9.1}
$$

Every principal idele satisfies

$$
\boxed{
\|a\|=1.
}
\tag{9.2}
$$

In terms of $q_0$,

$$
\|a\|
=
\frac{|a_\infty|}{q_0}.
\tag{9.3}
$$

Thus the product formula forces

$$
|a_\infty|
=
q_0.
$$

But it says nothing about the finite unit tuple $(u_p)_p$.

Therefore:

## No-Go 9.1

$$
\boxed{
\text{product formula}
+
\text{all finite valuations}
\not\Rightarrow
\text{principal idele}.
}
\tag{9.4}
$$

A compact finite-unit obstruction remains.

---

# 10. Lattice descent and element descent are genuinely different

At lattice level, the unit tuple disappears because

$$
\mathbf Z_p^\times
$$

acts trivially on the local lattice class.

Therefore:

$$
\boxed{
\text{Level L descent only needs }(d_p)_p.
}
$$

At exact-element level, one must also control

$$
(u_p)_p.
$$

Hence:

$$
\boxed{
\text{lattice globalization over }\mathbf Q
\text{ is easy;}
}
$$

$$
\boxed{
\text{exact element globalization still requires principalization.}
}
\tag{10.1}
$$

This is the main structural distinction of Round 012.

---

# 11. Refined T1 decomposition

Round 010 used one blocker:

$$
T1
=
\text{Global Rational Descent}.
$$

Round 012 refines it into two parts.

## T1L. Lattice-class globalization

Input:

$$
(d_p)_p
$$

with finite support.

Output:

$$
[a_0]
\in
\mathbf Q^\times/\{\pm1\}.
$$

Over $\mathbf Q$, this is symbolically automatic by prime factorization.

**Type: S**, once the local defects are genuine.

## T1E. Exact-element principalization

Input:

$$
(a_v)_v
\in
\mathbf A_{\mathbf Q}^\times.
$$

Output:

$$
a\in\mathbf Q^\times
$$

with all local components equal to $a$.

This requires triviality of the residual unit idele.

**Type: T/C hybrid**, depending on how the local exact elements are produced.

Thus the theorem-level burden of T1 is smaller than before, but not eliminated.

---

# 12. What the regulator actually needs

If the final global regulator correction only depends on the determinant torsor class

$$
[a]
\in
\mathbf Q^\times/\{\pm1\},
$$

then valuations determine

$$
a^2
$$

exactly:

$$
\boxed{
a^2
=
\prod_p
p^{2d_p}.
}
\tag{12.1}
$$

So at the level of a purely rational lattice-index correction, exact local unit principalization may be unnecessary.

But if one needs to identify a specific calibrated determinant element across:

- $p$-adic comparison;
- rational cohomology;
- archimedean period line;

then exact element descent matters.

Therefore:

$$
\boxed{
\text{whether T1E is necessary depends on the target claim.}
}
\tag{12.2}
$$

---

# 13. A safe lattice-level reconstruction theorem

## Theorem 13.1

Suppose a global arithmetic argument independently guarantees that the desired unknown is a rational determinant torsor class

$$
[a]
\in
\mathbf Q^\times/\{\pm1\}.
$$

If local calculations determine all nonzero valuations

$$
d_p=v_p(a),
$$

then

$$
\boxed{
[a]
=
\left[
\prod_p p^{d_p}
\right].
}
\tag{13.1}
$$

No local unit computation is needed.

This is the strongest safe form of rational reconstruction from valuation data.

The global rational-torsor hypothesis is essential.

---

# 14. An even stronger $S$-unit version

Suppose a theorem gives

$$
a
\in
\mathbf Z[S^{-1}]^\times.
$$

Then

$$
v_p(a)=0
$$

for every

$$
p\notin S.
$$

Therefore:

## Corollary 14.1

The finite vector

$$
\left(
v_\ell(a)
\right)_{\ell\in S}
$$

determines $a$ up to sign:

$$
\boxed{
a
=
\pm
\prod_{\ell\in S}
\ell^{v_\ell(a)}.
}
\tag{14.1}
$$

One real sign normalization then determines $a$ exactly.

This is the finite-prime reconstruction mechanism anticipated in Round 006.

---

# 15. Archimedean sign is enough once $S$-unit rationality is known

Assume

$$
a\in\mathbf Q^\times
$$

and all finite valuations are known.

Then the only remaining ambiguity is

$$
\pm1.
$$

Thus a single archimedean orientation or positivity convention fixes the sign.

For a regulator ratio, the sign is irrelevant because

$$
a^2
$$

is used.

So:

$$
\boxed{
\text{for quadratic regulator correction, finite valuations are enough once rationality is known.}
}
\tag{15.1}
$$

---

# 16. Exact local unit data can be gauge rather than arithmetic

Suppose the local determinant generator itself is only defined up to

$$
\mathbf Z_p^\times.
$$

Then replacing

$$
a_p
\mapsto
u_pa_p,
\qquad
u_p\in\mathbf Z_p^\times,
$$

does not change the local determinant lattice.

In that situation, demanding exact principalization of the tuple $(a_p)_p$ is artificial: the unit parts are trivialization gauge.

Therefore before declaring a residual unit idele to be an obstruction, one must ask:

$$
\boxed{
\text{are the local unit coordinates canonical arithmetic data,
or only local frame choices?}
}
\tag{16.1}
$$

If they are only frame choices, Level L is the correct descent problem.

If they are canonical comparison scalars, Level E is required.

---

# 17. Gauge quotient before principal-idele testing

Let the allowed local frame group be

$$
G_{\mathrm{loc}}
\subset
\prod_p\mathbf Z_p^\times.
$$

Then exact local coordinates should first be quotiented by $G_{\mathrm{loc}}$.

Only the residual class

$$
[(u_p)_p]
$$

after this gauge quotient can be interpreted as arithmetic obstruction.

Hence:

$$
\boxed{
\text{principal-idele obstruction must be computed after all declared local gauge symmetries are removed.}
}
\tag{17.1}
$$

Otherwise one can mistake a basis artifact for a global descent failure.

---

# 18. Finite local exact checks cannot prove principality by themselves

Fix a finite set of places $S$.

One may verify exact equalities

$$
a_v=q
$$

for all

$$
v\in S.
$$

But without structural control outside $S$, this does not imply the entire idele is principal.

At an untested prime $p\notin S$, one can alter the unit component

$$
a_p
$$

inside $\mathbf Z_p^\times$ without changing any tested data or any valuation.

Therefore:

## No-Go 18.1

$$
\boxed{
\text{finitely many exact local equalities do not prove principal-idele descent
without an outside-}S\text{ compatibility theorem.}
}
\tag{18.1}
$$

This is the exact-element analogue of Round 006's finite-support no-go.

---

# 19. Restricted principalization theorem

Assume a theorem gives:

1. finite support of valuations in $S$;
2. for every $p\notin S$, the normalized local unit is canonically

$$
u_p=1;
$$

3. at every $\ell\in S$, exact unit coordinates are known;
4. the real normalized coordinate is known.

Then principalization reduces to a finite check.

## Theorem 19.1

Under the assumptions above, the idele is principal if and only if there exists

$$
\epsilon\in\{\pm1\}
$$

such that

$$
u_\ell=\epsilon
\quad
\text{for every }\ell\in S,
$$

and

$$
u_\infty=\epsilon.
$$

Thus an outside-$S$ exact compatibility theorem converts exact element descent into a finite certificate.

---

# 20. Principal-idele defect ledger

After valuation normalization, define the finite-unit defect

$$
\mathfrak u(a)
=
[(u_p)_p]
\in
\widehat{\mathbf Z}^{\,\times}/\{\pm1\}.
\tag{20.1}
$$

Define the norm defect

$$
\mathfrak n(a)
=
\frac{|a_\infty|}{q_0}
\in
\mathbf R_{>0}.
\tag{20.2}
$$

Then every principal idele satisfies

$$
\mathfrak n(a)=1
$$

and

$$
\mathfrak u(a)=1.
$$

A final sign compatibility condition identifies the same diagonal sign at the real and finite places.

This gives a three-part exact descent ledger:

$$
\boxed{
\text{valuation class}
+
\text{norm defect}
+
\text{finite-unit defect}.
}
\tag{20.3}
$$

---

# 21. Rational reconstruction from one $p$-adic value requires a prior height bound

There is another practical route.

Suppose one already knows

$$
a
=
\frac{m}{n}
\in\mathbf Q,
$$

with

$$
|m|\le M,
\qquad
1\le n\le N,
\qquad
p\nmid n.
$$

If a $p$-adic computation determines $a$ modulo sufficiently high

$$
p^k,
$$

then standard rational reconstruction can recover the unique fraction $m/n$ satisfying the bounds once $p^k$ is large enough relative to $MN$.

The exact numerical threshold depends on the chosen reconstruction theorem, but the logical structure is:

$$
\boxed{
\text{rationality}
+
\text{height bound}
+
\text{sufficient }p\text{-adic precision}
\Longrightarrow
\text{finite reconstruction}.
}
\tag{21.1}
$$

Without the rationality and height assumptions, increasing precision alone does not prove global descent.

---

# 22. S-unit reconstruction is stronger than generic rational reconstruction

If one knows

$$
a\in\mathbf Z[S^{-1}]^\times,
$$

no numerator-height bound is needed.

The valuations at $S$ already determine the exact absolute value of $a$ up to sign.

Thus:

$$
\boxed{
S\text{-unit theorem}
+
\text{local valuations}
}
$$

is much stronger than generic p-adic rational reconstruction.

For the BSD determinant problem, structural $S$-unit control is therefore a better target than merely increasing p-adic precision.

---

# 23. Compatible local lines can reconstruct the global lattice class

Suppose for every prime $p$ we have a local determinant lattice

$$
L_p
\subset D_p
$$

such that

$$
L_p=D_{\mathbf Z_p}
$$

for almost all $p$.

Write

$$
L_p
=
p^{d_p}D_{\mathbf Z_p}.
$$

Then the restricted product

$$
\prod_p L_p
$$

determines a unique global fractional determinant lattice

$$
\boxed{
D'
=
a_0D_{\mathbf Z}
}
\tag{23.1}
$$

with

$$
a_0
=
\prod_p p^{d_p}.
$$

Thus:

## Theorem 23.1

Over $\mathbf Q$, compatible local determinant lattices with finite support reconstruct a unique global fractional determinant lattice up to sign.

This is a lattice-level local-to-global theorem requiring no exact unit data.

---

# 24. But compatible local lines do not reconstruct a global element

Choose arbitrary units

$$
u_p\in\mathbf Z_p^\times.
$$

Then

$$
a_p
=
u_p a_0
$$

all generate the same local lattices as $a_0$.

But unless the unit tuple is diagonal $\pm1$, the exact family

$$
(a_p)_p
$$

does not come from a rational number.

Therefore:

$$
\boxed{
\text{local lattice reconstruction}
\not\Rightarrow
\text{exact local-element reconstruction}.
}
\tag{24.1}
$$

This is the key no-go of the round.

---

# 25. Consequence for the BSD absolute anchor

The Round 005--006 scalar

$$
a
$$

must now be interpreted carefully.

There are two possible targets.

### Target A: lattice-scale anchor

One only needs

$$
[a]
\in
\mathbf Q^\times/\{\pm1\}.
$$

Then local valuations plus finite support are enough.

### Target B: exact cross-completion determinant element

One needs an actual

$$
a\in\mathbf Q^\times
$$

whose images agree with canonical local comparison scalars.

Then principal-idele triviality is required.

Thus the global descent theorem needed by BSD depends on whether the final fundamental-line comparison is lattice-valued or element-valued.

---

# 26. A refined proof-obligation split

The previous theorem-level blocker

$$
T1
=
\text{Global Rational Descent}
$$

should now be replaced by:

## T1L: global fractional determinant lattice

Given local valuation defects with finite support, reconstruct

$$
[a].
$$

Over $\mathbf Q$, this is symbolically closed.

## T1U: local unit compatibility

Determine whether local units are:

- gauge;
- canonical arithmetic data;
- or partially canonical after quotient.

## T1E: exact principalization

If canonical exact local units remain, prove the normalized idele is diagonal $\pm1$.

Only T1E is a genuine exact-element descent obstruction.

This is a substantial reduction.

---

# 27. What can now be delegated to local computation

If a structural theorem already gives finite support $S$ and declares local units gauge outside $S$, the local machines only need:

1. compute

$$
d_\ell
\quad
(\ell\in S);
$$

2. compute any residual canonical unit

$$
u_\ell;
$$

3. test whether the surviving unit defects agree with the required diagonal sign;
4. optionally verify the real sign / orientation.

This is finite.

---

# 28. What still cannot be delegated to brute force

The following remain theorem-type issues.

### A. Are local unit parts gauge or arithmetic?

This is a comparison-functor question.

### B. Why are outside-$S$ canonical unit defects trivial?

This needs a structural compatibility theorem.

### C. Why do all local exact realizations belong to one adelic object?

This needs a global comparison framework.

### D. Why is the resulting idele principal?

This is the principalization theorem if exact element descent is required.

No amount of isolated $11$-adic precision answers these questions.

---

# 29. A practical hierarchy for the current $p=11$ route

For the current target, the cheapest logically sound workflow is:

### Stage 1

Determine whether the desired final claim only needs determinant lattice class.

If yes, avoid exact unit descent entirely.

### Stage 2

Prove or assume a finite support theorem.

### Stage 3

Compute only the local valuations in $S$.

### Stage 4

Reconstruct

$$
[a]
=
\left[
\prod_{\ell\in S}
\ell^{d_\ell}
\right].
$$

### Stage 5

Only if the final line comparison requires exact canonical elements, reopen the finite-unit idele problem.

This ordering prevents unnecessary p-adic unit computations.

---

# 30. A principal-idele red flag

Suppose one claims exact global descent from:

- all local valuations;
- the product formula;
- one real normalization.

This is insufficient unless local unit parts have already been shown gauge or diagonal.

The missing object is

$$
\boxed{
\mathfrak u(a)
\in
\widehat{\mathbf Z}^{\,\times}/\{\pm1\}.
}
$$

Any proof that never addresses this unit class but claims exact idele principalization has a gap.

---

# 31. A lattice-level green flag

Conversely, if the target is only the rational determinant torsor class

$$
[a]
\in
\mathbf Q^\times/\{\pm1\},
$$

then the finite-unit idele is irrelevant.

In that case a proof that tracks only the valuation vector is not incomplete.

It is exactly the correct invariant.

Thus:

$$
\boxed{
\text{whether units matter is determined by the target category.}
}
\tag{31.1}
$$

This distinction should be explicit in every later proof obligation.

---

# 32. Interaction with the regulator

If

$$
[a]
$$

is known from valuations, then the regulator scaling correction is

$$
\boxed{
a^2
=
\prod_p
p^{2d_p}.
}
\tag{32.1}
$$

The sign disappears.

Any local unit ambiguity that does not change the rational lattice class also does not change this lattice-index regulator factor.

But local units can still matter elsewhere, such as:

- period comparison;
- p-adic height normalization;
- reciprocity scalar;
- exact cross-completion identification.

So they are irrelevant only to the lattice-index piece, not automatically to the whole BSD formula.

---

# 33. Interaction with Round 008 fundamental lines

Round 008 showed the final scalar is assembled from separate lines.

Therefore the correct strategy is to ask, line by line:

$$
\boxed{
\text{Does this line need a lattice class or an exact element?}
}
$$

Examples:

- a free integral determinant lattice may only need valuation data;
- a period comparison isomorphism may require exact scalar units;
- a reciprocity map may require a canonical local normalization;
- a quadratic regulator correction may only need the rational lattice-scale class.

This line-wise classification can shrink the principal-idele burden further.

---

# 34. Stage-2 update of the major cuts

Round 010 listed four major logical cuts:

$$
\{
\text{Global Descent},
\text{Arithmetic Fundamental Line},
\text{Explicit Reciprocity},
\text{Complex Comparison}
\}.
$$

Round 012 refines the first to:

$$
\boxed{
\text{Global Descent}
=
\text{Lattice Globalization}
+
\text{Residual Unit Principalization}.
}
\tag{34.1}
$$

Over $\mathbf Q$:

$$
\boxed{
\text{Lattice Globalization is symbolically closed from valuations.}
}
$$

The only remaining exact-descent difficulty is the residual unit idele, and only for those lines that genuinely require exact elements.

---

# 35. The minimal exact-descent theorem

A minimal theorem sufficient for exact element descent would have the form:

> The canonically normalized local determinant realizations define an idele whose normalized finite-unit component is diagonal and whose real component has the same sign.

Equivalently:

$$
\boxed{
\mathfrak u(a)=1
}
$$

plus norm and sign compatibility.

This is much smaller than an unspecified "global rational descent theorem."

---

# 36. Proved in this round

In the one-dimensional determinant setting over $\mathbf Q$, this round proves:

1. local determinant-lattice classes are valuations;
2. finite-support valuation vectors classify $\mathbf Q^\times/\{\pm1\}$;
3. local determinant lattices reconstruct a unique global fractional determinant lattice up to sign;
4. exact local elements define an idele;
5. exact global descent is equivalent to principality of that idele;
6. removing valuations leaves a finite-unit idele obstruction;
7. product formula is necessary but not sufficient for principality;
8. lattice descent and exact-element descent are different;
9. $S$-unit rationality plus local valuations reconstructs the global scalar up to sign;
10. one real sign fixes the remaining sign;
11. exact unit coordinates may be gauge rather than arithmetic;
12. principal-idele testing must occur after quotienting declared local gauge;
13. finitely many exact local checks do not prove principality without outside-$S$ control;
14. compatible local determinant lattices do not reconstruct compatible exact local elements;
15. the global-descent blocker splits into lattice globalization and residual unit principalization.

---

# 37. Not proved

This round does not prove:

1. that the actual calibrated BSD determinant has canonical local realizations at all places;
2. that those local realizations form one idele;
3. that the actual local unit parts are gauge;
4. that the actual normalized unit idele is diagonal;
5. an outside-$S$ exact compatibility theorem;
6. an actual finite support set $S$;
7. actual local defects for $389.a1$;
8. actual principalization of the BSD determinant;
9. the complex-to-$p$-adic comparison;
10. BSD.

---

# 38. Minimal local verification checklist

## V1. Decide target category

Is the required output:

$$
[a]\in\mathbf Q^\times/\{\pm1\},
$$

or an exact

$$
a\in\mathbf Q^\times?
$$

## V2. Compute lattice defects

For the finite support set $S$, compute

$$
d_\ell.
$$

## V3. Reconstruct lattice scale

Form

$$
a_0
=
\prod_{\ell\in S}
\ell^{d_\ell}.
$$

## V4. Identify unit gauge

Record which local units are removable by frame changes.

## V5. Compute residual canonical units only

For the units that survive gauge, compute

$$
u_\ell.
$$

## V6. Test principalization only if needed

Check whether the surviving normalized units are the same diagonal sign.

## V7. Keep product formula separate

Use it only as a norm consistency test, not as a proof of principality.

---

# 39. Main conclusion

The global-descent problem is smaller than Round 006 first suggested.

At the determinant-lattice level over $\mathbf Q$,

$$
\boxed{
\text{finite-support valuations already determine the global rational torsor class.}
}
$$

The genuine residual obstruction is not another valuation.

It is:

$$
\boxed{
\text{the finite-unit idele class after all local gauge has been removed.}
}
$$

Therefore the exact role of T1 is now:

$$
\boxed{
\text{decide whether exact unit principalization is actually needed for each fundamental line.}
}
$$

If a line only depends on lattice scale, T1 is already closed there.

If a line depends on a canonically normalized element, the remaining obstruction is the principal-idele unit class.

---

# 40. Proposed next round

## BSD Symbolic Round 013

**Title:**

> Line-by-Line Descent Audit and Elimination of Unnecessary Exact Scalars

The next round should use the Round 008--012 architecture and inspect each fundamental-line component separately:

1. free Mordell--Weil determinant;
2. dual determinant;
3. height regulator map;
4. finite Euler line;
5. BF comparison line;
6. reciprocity line;
7. $p$-adic analytic line;
8. complex period line.

For each component, classify whether it needs:

$$
\text{projective data},
$$

$$
\text{lattice-class data},
$$

or

$$
\text{exact scalar data}.
$$

The goal is to prove that some of the remaining exact-normalization obligations are artificial and can be quotiented away.

If successful, the principal-idele obstruction may survive only on a very small subset of the final BSD bridge rather than on the entire determinant architecture.
