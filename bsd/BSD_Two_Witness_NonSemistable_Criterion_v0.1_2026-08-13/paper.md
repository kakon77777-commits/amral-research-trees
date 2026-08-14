# A Two-Witness Criterion for Strong BSD in Positive-Density Non-Semistable Quadratic-Twist Families

**Neo.K**

**Derived theorem note — Version 0.1, 13 August 2026**

> **Status.** This paper formulates and proves a reusable sufficient criterion obtained by
> combining existing \(2\)-primary, ordinary/multiplicative, additive-twist, and
> supersingular \(p\)-part results.  It does not assert novelty or priority.

## Abstract

We isolate a finite certificate on a non-semistable elliptic curve
\(E/\mathbf Q\) that produces a positive-density set of quadratic twists
satisfying the strong Birch--Swinnerton--Dyer conjecture.  The criterion is
designed for curves whose only additive reduction occurs at \(2\).  Two odd
multiplicative primes play complementary roles: the prime \(3\) and a second
nonsplit multiplicative prime \(\lambda\), both with minimal-discriminant
valuation one.  These primes provide all ramification witnesses required by
the ordinary, multiplicative, additive-twist, and supersingular Iwasawa
theorems.

The twist support is defined by requiring primes to split completely in a
finite abelian \(2\)-extension controlling all bad-prime splitting, while
having Frobenius a \(3\)-cycle in the Galois closure of the \(2\)-division
cubic.  The support set has explicit positive Chebotarev density
\[
\frac{[L_E\cap K_E:\mathbf Q]}{3[K_E:\mathbf Q]}.
\]
The curve \(696.e1\) is recovered as a concrete corollary, with density
\(1/24\).

---

## 1. Setup

Let \(E/\mathbf Q\) be an elliptic curve with conductor \(N_E\), minimal
discriminant \(\Delta_E\), and no rational \(2\)-torsion.  Let
\[
f_E(x)
\]
denote the cubic whose roots are the \(x\)-coordinates of the nonzero points
of \(E[2]\), and let \(L_E\) be its Galois closure.

For an odd prime \(\ell\), put
\[
\ell^*=(-1)^{(\ell-1)/2}\ell.
\]
Define the finite abelian extension
\[
K_E
=
\mathbf Q\left(
\zeta_8,\,
\sqrt{\ell^*}\ :\ \ell\mid N_E,\ \ell\text{ odd}
\right).
\]

We write \(E^{(q)}\) for the quadratic twist by a positive prime \(q\).

---

## 2. The finite two-witness certificate

### Definition 2.1

We say that \(E\) satisfies the **two-witness BSD certificate** if the
following conditions hold.

**(T1) \(2\)-primary anchor.**
The curve \(E\) is optimal of analytic rank \(0\), its Manin constant is odd,
\[
E(\mathbf Q)[2]=0,\qquad
\Delta_E<0,\qquad
\operatorname{ord}_2L^{(\mathrm{alg})}(E,1)=0,
\]
and
\[
\operatorname{BSD}(E,2)
\]
is known.

**(T2) \(S_3\) two-division field.**
The polynomial \(f_E\) is irreducible and
\[
\operatorname{Gal}(L_E/\mathbf Q)\simeq S_3.
\]

**(T3) controlled non-semistability.**
The only prime at which \(E\) has additive reduction is \(2\).
Every odd bad prime is multiplicative.

**(T4) first ramification witness.**
The prime \(3\) is multiplicative and
\[
v_3(\Delta_E)=1.
\]

**(T5) nonsplit Fouquet--Wan witness.**
There exists an odd prime
\[
\lambda\neq3
\]
such that \(E\) has nonsplit multiplicative reduction at \(\lambda\) and
\[
v_\lambda(\Delta_E)=1.
\]

**(T6) residual irreducibility.**
For every odd prime \(p\),
\[
E[p]
\]
is absolutely irreducible.

**(T7) optimality after twisting.**
The rational isogeny class of \(E\) is a singleton.

The last condition is included explicitly to keep the period comparison
independent of any auxiliary isogeny argument.

---

## 3. The Chebotarev support set

Let \(C_3\subset S_3\) be the conjugacy class of \(3\)-cycles.

### Definition 3.1

Let \(\mathcal P_E\) be the set of rational primes \(q\), unramified in
\(L_EK_E\), such that
\[
\operatorname{Frob}_q|_{K_E}=1
\]
and
\[
\operatorname{Frob}_q|_{L_E}\in C_3.
\]

### Lemma 3.2

If \(q\in\mathcal P_E\), then:

1. \(q\equiv1\pmod8\);
2. every prime \(\ell\mid N_E\) splits in \(\mathbf Q(\sqrt q)\);
3. \(f_E\bmod q\) is irreducible;
4. \(q\) is a prime of good ordinary reduction for \(E\).

#### Proof

The trivial Frobenius condition on \(\mathbf Q(\zeta_8)\subset K_E\) gives
\(q\equiv1\pmod8\).  For an odd \(\ell\mid N_E\), trivial Frobenius on
\(\mathbf Q(\sqrt{\ell^*})\) gives
\[
\left(\frac{\ell^*}{q}\right)=1.
\]
Since \(q\equiv1\pmod4\), quadratic reciprocity rewrites this as
\[
\left(\frac q\ell\right)=1,
\]
which is exactly the splitting condition for \(\ell\) in
\(\mathbf Q(\sqrt q)\).  The condition at \(2\) follows from
\(q\equiv1\pmod8\).

The \(3\)-cycle condition is equivalent to irreducibility of the
\(2\)-division cubic modulo \(q\).  On \(E[2]\),
\[
\operatorname{GL}_2(\mathbf F_2)\simeq S_3,
\]
and a \(3\)-cycle has trace \(1\).  Thus
\[
a_q(E)\equiv1\pmod2.
\]
Hence \(a_q(E)\) is odd.  Because \(q\equiv1\pmod8\), we have \(q\ge17\).
If \(E\) were supersingular at \(q\), then \(q\mid a_q(E)\), and the Hasse
bound would force \(a_q(E)=0\), contradiction.  Thus \(q\) is ordinary.
\(\square\)

### Proposition 3.3 — positive density

Let
\[
e_E=[L_E\cap K_E:\mathbf Q].
\]
Then
\[
e_E\in\{1,2\}
\]
and
\[
\boxed{
\delta(\mathcal P_E)
=
\frac{e_E}{3[K_E:\mathbf Q]}.
}
\]

In particular \(\mathcal P_E\) has positive natural prime density.

#### Proof

Since \(K_E/\mathbf Q\) is abelian, \(L_E\cap K_E\) is an abelian Galois
subextension of the \(S_3\)-extension \(L_E/\mathbf Q\).  The only
possibilities are \(\mathbf Q\) and the unique quadratic resolvent of
\(L_E\).  Hence \(e_E\in\{1,2\}\).

A \(3\)-cycle acts trivially on the quadratic resolvent.  Therefore the
condition “identity on \(K_E\)” is compatible with either of the two
\(3\)-cycles in \(L_E\).  The compositum has degree
\[
[L_EK_E:\mathbf Q]
=
\frac{6[K_E:\mathbf Q]}{e_E}.
\]
Exactly two elements of its Galois group have identity \(K_E\)-component and
\(3\)-cycle \(L_E\)-component.  Chebotarev gives
\[
\delta(\mathcal P_E)
=
\frac{2}{6[K_E:\mathbf Q]/e_E}
=
\frac{e_E}{3[K_E:\mathbf Q]}.
\]
\(\square\)

---

## 4. Main criterion

### Theorem 4.1 — Two-Witness Non-Semistable Criterion

Assume that \(E/\mathbf Q\) satisfies the two-witness BSD certificate
(T1)--(T7).  Then for every
\[
q\in\mathcal P_E
\]
the strong Birch--Swinnerton--Dyer conjecture holds for the quadratic twist
\(E^{(q)}\):
\[
\boxed{
\operatorname{BSD}(E^{(q)}).
}
\]

Moreover the set of such primes has natural density
\[
\boxed{
\delta(\mathcal P_E)
=
\frac{[L_E\cap K_E:\mathbf Q]}
     {3[K_E:\mathbf Q]}
>0.
}
\]

#### Proof

Fix \(q\in\mathcal P_E\) and write
\[
A=E^{(q)}.
\]

### Step 1: the \(2\)-part

By Lemma 3.2,
\[
q\equiv1\pmod4,
\]
every prime dividing \(N_E\) splits in \(\mathbf Q(\sqrt q)\), and the unique
prime \(q\mid d=q\) is inert in the cubic \(2\)-division field.  Thus the
no-rational-\(2\)-torsion branch of Banwait--Huang's \(2\)-primary twist
theorem applies using (T1), and gives
\[
L(A,1)\neq0
\]
and
\[
\operatorname{BSD}(A,2).
\]

### Step 2: residual irreducibility after twisting

For odd \(p\),
\[
A[p]\simeq E[p]\otimes\chi_q.
\]
Tensoring by a one-dimensional character preserves absolute irreducibility.
Hence (T6) gives absolute irreducibility of \(A[p]\) for every odd \(p\).

### Step 3: the additive twist prime \(p=q\)

Lemma 3.2 shows that \(q\ge5\) is good ordinary for the base curve \(E\).
The additive-twist theorem used in Banwait--Huang's proof of their odd-prime
router therefore applies once the ramified auxiliary prime is supplied
explicitly.

Take
\[
\ell=\lambda.
\]
By (T5),
\[
v_\lambda(\Delta_E)=1,
\]
so \(E[q]\) is residually ramified at \(\lambda\).  Since
\(q\in\mathcal P_E\), the prime \(\lambda\) splits in
\(\mathbf Q(\sqrt q)\), and \(q\neq\lambda\).  This supplies the required
ramification hypothesis and yields
\[
\operatorname{BSD}(A,q).
\]

### Step 4: odd good ordinary primes

Let \(p\) be an odd good ordinary prime for \(A\).  Then \(p\neq\lambda\).
The curve \(A\) has multiplicative reduction at \(\lambda\), and local
splitting of \(q\) at \(\lambda\) means that the twist does not alter that
local representation.  Since
\[
v_\lambda(\Delta_A)=1,
\]
the representation \(A[p]\) is ramified at \(\lambda\).  Skinner's
ordinary/multiplicative theorem applies and gives
\[
\operatorname{BSD}(A,p).
\]

### Step 5: fixed odd multiplicative primes

Let \(p\mid N_E\) be odd.  By (T3), \(A\) remains multiplicative at \(p\).

If
\[
p\neq\lambda,
\]
use \(\lambda\) as the distinct ramified multiplicative witness; the
valuation-one condition in (T5) works for every odd \(p\neq\lambda\).

If
\[
p=\lambda,
\]
use the prime \(3\).  By (T4),
\[
v_3(\Delta_A)=1,
\]
so \(A[\lambda]\) is ramified at \(3\).

Skinner's theorem therefore gives
\[
\operatorname{BSD}(A,p)
\]
for every odd multiplicative bad prime \(p\).

### Step 6: odd good supersingular primes

Let \(p\) be an odd good supersingular prime for \(A\).  Since \(3\) is bad
multiplicative by (T4), we have \(p\neq3\); hence \(p\ge5\).

Apply Fouquet--Wan.  Absolute irreducibility is supplied by Step 2.
At a good supersingular prime \(p\ge5\), the local residual representation is
irreducible, so its semisimplification cannot be one of the forbidden
one-dimensional character sums.

For the auxiliary Steinberg prime take again
\[
\ell=\lambda.
\]
By (T5), \(E\), hence also \(A\), is nonsplit multiplicative at \(\lambda\);
the support condition makes the local quadratic twist trivial there.  The
condition
\[
v_\lambda(\Delta_A)=1
\]
implies residual ramification for every odd good \(p\neq\lambda\).  Thus the
Fouquet--Wan residual hypotheses hold and their rank-zero \(p\)-part BSD
consequence applies.

For the period comparison, (T7) and twisting imply that \(A\) is the unique
curve in its rational isogeny class and hence optimal.  Prime divisors of the
Manin constant are supported at additive reduction primes.  The additive
primes of \(A\) are \(2\) and \(q\), whereas the present \(p\) is good.
Thus the modular and Néron periods have the same \(p\)-adic valuation, and
\[
\operatorname{BSD}(A,p)
\]
holds.

### Step 7: exhaustion

The curve \(A\) has:

- additive reduction at \(2\) and \(q\);
- multiplicative reduction at the odd primes dividing \(N_E\);
- good reduction at every other prime.

The \(2\)-part is handled in Step 1; \(p=q\) in Step 3; all odd
multiplicative primes in Step 5; and all other odd primes are good ordinary
or good supersingular, handled in Steps 4 and 6.

Thus the BSD formula holds at every finite prime.  Since \(L(A,1)\neq0\),
the rank-zero Gross--Zagier--Kolyvagin consequences give rank equality and
finiteness of \(\Sha(A)\), and the local-to-global formulation of the strong
BSD formula yields
\[
\operatorname{BSD}(A).
\]
\(\square\)

---

## 5. The explicit curve \(696.e1\)

### Corollary 5.1

Let
\[
E:\quad y^2=x^3+x^2+8x-16
\]
be the curve \(696.e1\).  Then \(E\) satisfies the two-witness certificate
with
\[
3
\quad\text{and}\quad
\lambda=29.
\]

Moreover
\[
[K_E:\mathbf Q]=16,
\qquad
[L_E\cap K_E:\mathbf Q]=2.
\]
Hence
\[
\delta(\mathcal P_E)
=
\frac{2}{3\cdot16}
=
\frac1{24}.
\]

In concrete congruence form,
\[
\mathcal P_E
=
\left\{
q:
q\equiv1\pmod{24},\
\left(\frac q{29}\right)=1,\
x^3+x^2+8x-16
\text{ irreducible mod }q
\right\},
\]
and every \(q\in\mathcal P_E\) satisfies
\[
\operatorname{BSD}(E^{(q)}).
\]

#### Proof

The arithmetic certificate is:
\[
N_E=2^3\cdot3\cdot29,\qquad
\Delta_E=-2^{11}\cdot3\cdot29,
\]
with additive reduction only at \(2\), split multiplicative reduction at
\(3\), nonsplit multiplicative reduction at \(29\), and
\[
v_3(\Delta_E)=v_{29}(\Delta_E)=1.
\]
The remaining conditions (T1), (T2), (T6), and (T7) are exactly the finite
data isolated in the explicit \(696.e1\) theorem note.

The \(2\)-division Galois closure has quadratic resolvent
\[
\mathbf Q(\sqrt{-174}),
\]
which lies in
\[
K_E=\mathbf Q(\zeta_{24},\sqrt{29}),
\]
so the intersection has degree \(2\), giving density \(1/24\).
\(\square\)

---

## 6. What the criterion does and does not say

Theorem 4.1 is intentionally a **sufficient criterion**, not a
classification.

The assumptions
\[
v_3(\Delta_E)=v_\lambda(\Delta_E)=1
\]
are stronger than necessary.  They are chosen because they make the
ramification witnesses uniform for every odd prime without an exceptional
prime audit.  A more general version should replace valuation one by suitable
gcd conditions.

Likewise, the assumption that the only additive prime is \(2\) avoids the
finite but nontrivial Fouquet--Wan local checks at fixed odd additive primes.
Removing this hypothesis is the next natural extension.

Thus there are two immediate generalizations:

1. **gcd-witness criterion:** replace valuation-one witnesses by a finite set
   of multiplicative primes whose discriminant valuations have odd-prime-free
   gcd;

2. **odd-additive extension:** permit finitely many odd additive primes and
   verify Fouquet--Wan's local residual hypotheses at those fixed primes.

These extensions preserve the same global architecture:
\[
\boxed{
\text{finite base certificate}
\longrightarrow
\text{positive-density Chebotarev support}
\longrightarrow
\text{all-prime BSD routing}.
}
\]

---

## References

- B. S. Banwait and X. Huang,
  *On the identification of elliptic curves that admit infinitely many twists
  satisfying the Birch--Swinnerton--Dyer conjecture*,
  arXiv:2601.16044v3 (2026).
- A. A. Burungale, C. Skinner, Y. Tian and X. Wan,
  *Zeta elements for elliptic curves and applications*,
  arXiv:2409.01350.
- C. Skinner,
  *Multiplicative reduction and the cyclotomic main conjecture for
  \(\mathrm{GL}_2\)*,
  arXiv:1407.1093.
- O. Fouquet and X. Wan,
  *The Iwasawa Main Conjecture for universal families of modular motives*,
  arXiv:2107.13726.
- K. Česnavičius, M. Neururer and A. Saha,
  *The Manin constant and the modular degree*,
  JEMS 26 (2024).
- B. Creutz and R. L. Miller,
  *Second isogeny descents and the Birch and Swinnerton--Dyer conjectural
  formula*,
  J. Algebra 372 (2012).
