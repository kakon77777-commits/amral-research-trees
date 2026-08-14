# A Finite-Exception Witness-Network Criterion for Strong BSD in Non-Semistable Quadratic-Twist Families

**Neo.K**

**Derived theorem framework — Version 0.2, 13 August 2026**

> **Status.** This note strengthens the preceding Two-Witness Criterion by replacing
> valuation-one hypotheses with a finite witness network. It also isolates a rigorous,
> finite interface for allowing odd additive bad primes. No novelty or priority claim is made.

---

## Abstract

Let \(E/\mathbf Q\) be an analytic-rank-zero elliptic curve to which a
Banwait--Huang \(2\)-primary quadratic-twist theorem applies.  Write
\(\mathcal M(E)\) for the odd multiplicative bad primes of \(E\) and
\(\mathcal M^-(E)\subseteq\mathcal M(E)\) for the nonsplit multiplicative
ones.  For \(\ell\in\mathcal M(E)\), put
\[
n_\ell=v_\ell(\Delta_E).
\]

The earlier Two-Witness Criterion imposed \(n_\ell=1\) at two distinguished
primes.  Here we show that the relevant obstruction is instead controlled by
the finite integers
\[
g_{\mathrm{mult}}(E)
=
\gcd_{\ell\in\mathcal M(E)} n_\ell,
\qquad
g_-(E)
=
\gcd_{\ell\in\mathcal M^-(E)} n_\ell,
\]
together with finitely many leave-one-out witness tests at the fixed
multiplicative primes.

Odd prime divisors of these gcds do not destroy the route.  They create only
a finite exceptional-prime set.  Generic primes are handled automatically by
multiplicative ramification witnesses, while the exceptional primes are
routed individually.  This yields a genuine finite-exception compression of
the all-prime BSD problem.

We also show how fixed odd additive bad primes can be incorporated through
Fouquet--Wan, provided their residual local hypotheses and period
normalization are certified.  For a useful published period-safe subclass,
an additive prime \(p\ge11\) is harmless for the Manin-period comparison when
the local reduction is not additive potentially ordinary of Kodaira type
II, III, or IV.

---

# 1. Witness sets

Let

\[
\mathcal M
=
\{\ell>2:\ E\text{ has multiplicative reduction at }\ell\},
\]

and

\[
\mathcal M^-
=
\{\ell\in\mathcal M:\ E\text{ has nonsplit multiplicative reduction at }\ell\}.
\]

For each \(\ell\in\mathcal M\), define

\[
n_\ell=v_\ell(\Delta_E)>0.
\]

Assume throughout that

\[
\mathcal M\neq\varnothing,
\qquad
\mathcal M^-\neq\varnothing.
\]

Define

\[
g_{\mathrm{mult}}
=
\gcd_{\ell\in\mathcal M} n_\ell,
\]

and

\[
g_-
=
\gcd_{\ell\in\mathcal M^-} n_\ell.
\]

Let

\[
R_{\mathrm{mult}}
=
\{r\text{ odd prime}:r\mid g_{\mathrm{mult}}\},
\]

and

\[
R_-
=
\{r\text{ odd prime}:r\mid g_-\}.
\]

These are finite.

For a fixed multiplicative prime \(p\in\mathcal M\), define the
leave-one-out condition

\[
\mathrm{LOO}(p):
\quad
\exists\ell\in\mathcal M,\ \ell\neq p,\ 
p\nmid n_\ell.
\]

Equivalently, when \(\mathcal M\setminus\{p\}\neq\varnothing\),

\[
\mathrm{LOO}(p)
\iff
p\nmid
\gcd_{\ell\in\mathcal M\setminus\{p\}} n_\ell.
\]

---

# 2. Elementary witness compression

## Lemma 2.1 — generic multiplicative witness

Let \(p\) be an odd prime with \(p\notin\mathcal M\).  Then

\[
\exists\ell\in\mathcal M:
p\nmid n_\ell
\]

if and only if

\[
p\notin R_{\mathrm{mult}}.
\]

### Proof

The failure of every witness means exactly

\[
p\mid n_\ell
\qquad
\forall\ell\in\mathcal M,
\]

which is equivalent to

\[
p\mid g_{\mathrm{mult}}.
\]
\(\square\)

## Lemma 2.2 — generic nonsplit Fouquet--Wan witness

Let \(p\) be an odd prime with \(p\notin\mathcal M^-\).  Then

\[
\exists\ell\in\mathcal M^-:
p\nmid n_\ell
\]

if and only if

\[
p\notin R_-.
\]

The proof is identical.

---

# 3. Why odd gcd factors are not a global obstruction

The previous criterion required

\[
g_{\mathrm{mult}}=2^a,
\qquad
g_-=2^b.
\]

This is sufficient, but unnecessarily strong.

The correct interpretation is:

\[
\boxed{
R_{\mathrm{mult}}\cup R_-
\text{ is a finite exceptional-prime set.}
}
\]

For every odd prime outside this set, the relevant ramification witness exists
automatically.

Thus the infinite quantifier

\[
\forall p>2
\]

is reduced to:

1. a generic theorem for
   \[
   p\notin R_{\mathrm{mult}}\cup R_-;
   \]
2. exact routing of finitely many primes in
   \[
   R_{\mathrm{mult}}\cup R_-;
   \]
3. exact routing of the finitely many bad primes of \(E\).

This is strictly stronger than requiring both gcds to be powers of \(2\).

---

# 4. Chebotarev support with finite exclusions

Let \(L_E\) be the Galois closure of the irreducible \(2\)-division cubic
and assume

\[
\operatorname{Gal}(L_E/\mathbf Q)\simeq S_3.
\]

Let

\[
K_E
=
\mathbf Q\left(
\zeta_8,\,
\sqrt{\ell^*}:\ell\mid N_E,\ \ell\text{ odd}
\right),
\qquad
\ell^*=(-1)^{(\ell-1)/2}\ell.
\]

Define \(\mathcal P_E\) as the primes \(q\) such that:

\[
\operatorname{Frob}_q|_{K_E}=1,
\]

and

\[
\operatorname{Frob}_q|_{L_E}
\text{ is a }3\text{-cycle}.
\]

As before,

\[
\delta(\mathcal P_E)
=
\frac{[L_E\cap K_E:\mathbf Q]}
{3[K_E:\mathbf Q]}
>0.
\]

Now remove the finite set

\[
R_{\mathrm{mult}}
\cup
R_-
\cup
\{\text{ramified primes of }L_EK_E\}.
\]

Call the remaining support set

\[
\mathcal P_E^\circ.
\]

Finite deletion does not change natural prime density:

\[
\boxed{
\delta(\mathcal P_E^\circ)
=
\delta(\mathcal P_E)>0.
}
\]

Every \(q\in\mathcal P_E^\circ\) is:

- coprime to \(N_E\);
- \(1\bmod 8\);
- inert in the cubic \(2\)-division field;
- good ordinary for \(E\);
- equipped with at least one multiplicative ramification witness, because
  \(q\notin R_{\mathrm{mult}}\).

---

# 5. Squarefree products, not only prime twists

Let

\[
d>1
\]

be any positive squarefree integer supported on \(\mathcal P_E^\circ\).

Because every support prime is \(1\bmod8\),

\[
d\equiv1\pmod8,
\]

hence in particular \(d\equiv1\pmod4\).

For every \(\ell\mid N_E\), each prime factor \(q\mid d\) has

\[
\left(\frac q\ell\right)=1,
\]

so

\[
\left(\frac d\ell\right)=1.
\]

Therefore every conductor prime splits in

\[
\mathbf Q(\sqrt d).
\]

Every \(q\mid d\) is inert in the cubic \(2\)-division field and ordinary for
\(E\).

Thus the Chebotarev construction automatically supports the full
squarefree-product family required by the \(2\)-primary theorem, rather than
only prime twists.

---

# 6. Prime router with a witness network

Fix such a squarefree \(d\) and put

\[
A=E^{(d)}.
\]

Assume the \(2\)-primary Banwait--Huang anchor gives

\[
L(A,1)\neq0
\]

and

\[
\operatorname{BSD}(A,2).
\]

Assume also, for simplicity of the reusable criterion, that

\[
E[p]
\]

is absolutely irreducible for every odd prime \(p\).  Quadratic twisting
preserves this property.

We route all odd primes as follows.

---

## Route Q — primes \(p\mid d\)

Such a prime is a good ordinary prime of the base curve.  Since

\[
p\notin R_{\mathrm{mult}},
\]

Lemma 2.1 supplies a multiplicative prime

\[
\ell\in\mathcal M
\]

with

\[
p\nmid n_\ell.
\]

The support splitting condition makes the quadratic character locally
trivial at \(\ell\).  Hence \(\ell\) supplies the explicit ramified-prime
condition in the additive-twist theorem used by Banwait--Huang.

So

\[
\operatorname{BSD}(A,p)
\]

holds for every \(p\mid d\).

---

## Route O — good ordinary primes \(p\nmid d\)

If

\[
p\notin R_{\mathrm{mult}},
\]

Lemma 2.1 supplies a direct Skinner ramified multiplicative witness, and the
ordinary \(p\)-part follows.

If

\[
p\in R_{\mathrm{mult}},
\]

then \(p\) belongs to a finite set.  It is routed by an explicit
**ordinary-exception certificate**.

One published option for \(p>3\) is the
Burungale--Castella--Skinner good-ordinary theorem, whose rank-zero BSD
corollary removes the old multiplicative-ramification hypothesis under its
residual image condition `(im)`.

Thus the condition
\[
g_{\mathrm{mult}}=2^a
\]
may be replaced by finitely many ordinary-exception checks.

---

## Route M — fixed multiplicative bad primes

Let

\[
p\in\mathcal M.
\]

Require the finite leave-one-out certificate

\[
\mathrm{LOO}(p).
\]

Then there exists

\[
\ell\in\mathcal M,\qquad
\ell\neq p,
\qquad
p\nmid n_\ell.
\]

Skinner's multiplicative theorem gives

\[
\operatorname{BSD}(A,p).
\]

Hence the fixed multiplicative branch is entirely finite.

---

## Route S — good supersingular primes

Let \(p\) be an odd good supersingular prime.

If

\[
p\notin R_-,
\]

Lemma 2.2 gives a nonsplit multiplicative prime

\[
\ell\in\mathcal M^-
\]

with

\[
p\nmid n_\ell.
\]

The good supersingular local residual representation excludes the forbidden
Fouquet--Wan semisimplification, while \(\ell\) provides the required
ramified nonsplit Steinberg auxiliary prime.

Thus Fouquet--Wan gives

\[
\operatorname{BSD}(A,p).
\]

If

\[
p\in R_-,
\]

the prime belongs to a finite set.  Therefore one may replace the old strong
condition

\[
g_-=2^b
\]

by the finite check:

\[
\boxed{
\text{every }p\in R_-
\text{ is either not good supersingular, or has an alternative certified route.}
}
\]

This is the exact finite-exception version of the nonsplit-witness
requirement.

---

# 7. Fixed odd additive primes

Let

\[
\mathcal A
=
\{p>2:\ E\text{ has additive reduction at }p\}.
\]

For any \(p\in\mathcal A\), the support construction makes every prime
dividing \(N_E\) split in \(\mathbf Q(\sqrt d)\).  Hence the twist character
is locally trivial at \(p\), and

\[
A[p]|_{G_{\mathbf Q_p}}
\simeq
E[p]|_{G_{\mathbf Q_p}}.
\]

Therefore all Fouquet--Wan residual conditions at \(p\) can be checked once
on the base curve.

For each \(p\in\mathcal A\), require the finite certificate:

### (A1) absolute irreducibility
\[
E[p]\text{ is absolutely irreducible};
\]

### (A2) local Fouquet--Wan nondegeneracy
there is no character \(\chi\) with
\[
E[p]|_{G_{\mathbf Q_p}}^{ss}
\simeq
\chi\oplus\chi_{\mathrm{cyc}}\chi;
\]

### (A3) nonsplit auxiliary witness
\[
p\notin R_-;
\]

### (A4) period compatibility
the modular period in Fouquet--Wan has the same \(p\)-adic valuation as the
Néron period of \(A\).

Under (A1)--(A4), Fouquet--Wan gives

\[
\operatorname{BSD}(A,p).
\]

Thus odd additive bad primes do **not** reopen an infinite quantifier:
they create only a finite table of local certificates.

---

# 8. A published period-safe additive subclass

Condition (A4) is the delicate part.

For optimal elliptic curves, the Manin constant is supported at additive
reduction primes, so good supersingular primes were automatically period
safe.  At a fixed additive prime \(p\), this is no longer automatic.

A useful published sufficient condition is available for many large additive
primes.  As reviewed by Česnavičius--Neururer--Saha from Edixhoven's theorem:

> if \(p\ge11\) is an additive prime and the reduction is not additive
> potentially ordinary of Kodaira type II, III, or IV, then \(p\) does not
> divide the Manin constant of an optimal parametrization.

Because our support forces the quadratic twist to be locally trivial at the
fixed bad prime \(p\), its local Kodaira type is unchanged.

Consequently, if the twist remains optimal—for example, under a singleton
rational isogeny-class hypothesis—then (A4) is automatically satisfied for
every fixed odd additive prime belonging to this published period-safe
subclass.

This gives a rigorous first extension beyond the “additive only at \(2\)”
criterion.

For additive primes \(3,5,7\), or for the excluded potentially ordinary
Kodaira types, period compatibility remains an explicit finite certificate;
it must not be silently assumed.

---

# 9. Finite-Exception Witness-Network Criterion

## Theorem Schema 9.1

Let \(E/\mathbf Q\) be an analytic-rank-zero optimal elliptic curve satisfying
a Banwait--Huang \(2\)-primary twist anchor, with irreducible \(S_3\)
\(2\)-division cubic and absolutely irreducible odd residual
representations.

Assume:

1. \(\mathcal M\neq\varnothing\) and
   \(\mathcal M^-\neq\varnothing\);

2. every fixed multiplicative prime
   \[
   p\in\mathcal M
   \]
   satisfies \(\mathrm{LOO}(p)\);

3. every prime in the finite ordinary-exception set
   \[
   R_{\mathrm{mult}}
   \]
   that actually occurs as a good ordinary prime has a certified ordinary
   route;

4. every prime in
   \[
   R_-
   \]
   that actually occurs as a good supersingular prime has a certified
   alternative supersingular route;

5. every fixed odd additive prime satisfies the finite
   Fouquet--Wan certificate (A1)--(A4);

6. the rational isogeny/optimality hypotheses needed for period comparison
   are stable under the twists.

Then every positive squarefree \(d\) supported on
\(\mathcal P_E^\circ\) satisfies

\[
\boxed{
\operatorname{BSD}(E^{(d)}).
}
\]

Moreover

\[
\mathcal P_E^\circ
\]

has the same positive Chebotarev prime density as \(\mathcal P_E\).

---

# 10. What has actually been gained

The progression is now:

\[
\text{valuation-one witnesses}
\]

\[
\Downarrow
\]

\[
\text{power-of-two gcd witnesses}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{arbitrary witness gcds + finite exceptional-prime routing}.
}
\]

The strongest step is the last one.

An odd prime divisor of a witness gcd no longer means “reject the curve.”
It means only:

\[
\boxed{
\text{put this prime into the finite exception table.}
}
\]

Likewise, an odd additive bad prime no longer means “reject the curve.”
It means:

\[
\boxed{
\text{run one finite FW local/period certificate at that prime.}
}
\]

This converts the non-semistable extension problem into a genuinely finite
certificate problem.

---

# 11. Remaining frontier

The next high-value tasks are now sharply localized.

### F1 — exact additive H2 backend

Specialize
\[
E[p]|_{G_{\mathbf Q_p}}^{ss}
\]
for fixed additive Kodaira types and turn Fouquet--Wan (A2) into an explicit
Tate-algorithm/Galois predicate.

### F2 — period-safe additive classification

Extend the published period-safe subclass, or replace (A4) by an exact
modular-degree certificate.

### F3 — ordinary finite exceptions

Compile the Burungale--Castella--Skinner `(im)` condition for the finite set
\(R_{\mathrm{mult}}\).

### F4 — database census

Only after F1--F3 should one scan the non-semistable analytic-rank-zero
database.

The mathematical bottleneck is no longer an infinite prime quantifier.  It is
a finite local-certificate compiler.
