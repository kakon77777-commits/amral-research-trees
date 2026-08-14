# An Explicit Non-Semistable Quadratic-Twist Family Satisfying the Strong Birch–Swinnerton–Dyer Conjecture

**Neo.K**

**Theorem-style research note — Version 1.0, 13 August 2026**

> **Status.** This note records an explicit derived consequence of the theorem statements cited below.  
> It does **not** assert priority over all published or unpublished literature, and it should be independently refereed before submission.

## Abstract

Let

\[
E/\mathbf Q:\qquad y^2=x^3+x^2+8x-16,
\]

the elliptic curve with LMFDB label \(696.e1\) (Cremona label \(696b1\)).  Its conductor is

\[
N_E=696=2^3\cdot 3\cdot 29,
\]

so \(E\) is not semistable.  Put

\[
f_2(x)=x^3+x^2+8x-16,
\]

and let \(\mathcal P\) be the set of rational primes \(q\) satisfying

\[
q\equiv1\pmod{24},\qquad
\left(\frac q{29}\right)=1,
\qquad
f_2(x)\ \text{irreducible in }\mathbf F_q[x].
\]

We show, by combining the \(2\)-primary quadratic-twist theorem collected by
Banwait--Huang with the ordinary and multiplicative \(p\)-part theorem of
Skinner, the additive-twist argument used by Banwait--Huang from
Burungale--Skinner--Tian--Wan, and the arbitrary-reduction Iwasawa theorem of
Fouquet--Wan, that every quadratic twist \(E^{(q)}\) with \(q\in\mathcal P\)
satisfies the strong Birch--Swinnerton--Dyer conjecture.  We also prove by
Chebotarev that \(\mathcal P\) has natural prime density \(1/24\).

The point of the example is that the base curve is non-semistable: the
additive reduction at \(2\) is bypassed by an explicit prime-by-prime routing
of the odd-primary BSD formula, with the nonsplit multiplicative prime \(29\)
serving as a uniform Fouquet--Wan auxiliary prime at good supersingular
primes.

---

## 1. Main theorem

For a squarefree integer \(d\), write \(E^{(d)}\) for the quadratic twist of
\(E\) by \(d\).

### Theorem 1.1

Let

\[
E:\quad y^2=x^3+x^2+8x-16
\]

and define

\[
\mathcal P
=
\left\{
q\text{ prime}:
q\equiv1\pmod{24},\
\left(\frac q{29}\right)=1,\
f_2\bmod q\text{ is irreducible}
\right\},
\]

where \(f_2(x)=x^3+x^2+8x-16\).  Then:

1. \(\mathcal P\) has natural density
   \[
   \delta(\mathcal P)=\frac1{24}
   \]
   in the set of rational primes;

2. for every \(q\in\mathcal P\),
   \[
   L(E^{(q)},1)\neq0;
   \]

3. for every \(q\in\mathcal P\), the strong Birch--Swinnerton--Dyer
   conjecture holds for \(E^{(q)}\):
   \[
   \boxed{\operatorname{BSD}(E^{(q)})}.
   \]

The proof occupies Sections 2--6.

### Remark 1.2

The theorem is a **derived theorem statement**: its proof is an explicit
synthesis of existing \(p\)-part theorems.  In particular, the present note
does not claim that the general synthesis mechanism, or this precise example,
has not appeared elsewhere.  The novelty question is logically separate from
the validity of the derivation.

---

## 2. Arithmetic of the base curve

We use the following arithmetic data for \(E\):

\[
[a_1,a_2,a_3,a_4,a_6]=[0,1,0,8,-16],
\]

\[
N_E=696=2^3\cdot3\cdot29,
\]

and

\[
\Delta_E=-178176=-2^{11}\cdot3\cdot29.
\]

The curve has analytic and algebraic rank \(0\), trivial rational torsion, a
singleton \(\mathbf Q\)-isogeny class, is \(\Gamma_0(N_E)\)-optimal, and has
Manin constant \(1\).  Its bad local data are

\[
\begin{array}{c|c|c|c}
\ell & \text{reduction} & \operatorname{ord}_{\ell}(N_E)
&\operatorname{ord}_{\ell}(\Delta_E)\\
\hline
2 & \text{additive }II^* & 3 & 11\\
3 & \text{split multiplicative }I_1 & 1 & 1\\
29& \text{nonsplit multiplicative }I_1 & 1 & 1.
\end{array}
\]

In particular \(E\) is not semistable.

LMFDB records maximal \(\ell\)-adic image for every prime \(\ell\); in
particular \(E[\ell]\) is absolutely irreducible for every odd prime
\(\ell\).  The full BSD formula is known for \(E\), since \(N_E<5000\) and
the analytic rank is \(0\), by the conductor-\(<5000\), rank-\(\le1\)
verification completed in Creutz--Miller and the works summarized there
[CM12].

A modular-symbol computation gives

\[
L^{(\mathrm{alg})}(E,1)
=
\frac{L(E,1)}{\Omega_E}
=1,
\]

hence

\[
\operatorname{ord}_2 L^{(\mathrm{alg})}(E,1)=0.
\]

The same arithmetic record is displayed in LMFDB [LMFDB].

The nontrivial \(2\)-torsion points have \(x\)-coordinates given by the roots
of

\[
f_2(x)=x^3+x^2+8x-16.
\]

The rational-root test shows that \(f_2\) is irreducible over \(\mathbf Q\),
and

\[
\operatorname{disc}(f_2)
=
-11136
=
-2^7\cdot3\cdot29.
\]

Thus the Galois closure \(L\) of the \(2\)-division cubic has

\[
\operatorname{Gal}(L/\mathbf Q)\simeq S_3,
\]

and its unique quadratic subfield is

\[
F_0=\mathbf Q(\sqrt{-174}).
\]

---

## 3. The support primes

We first isolate the two elementary facts that make the prime family useful.

### Lemma 3.1

If \(q\in\mathcal P\), then every prime dividing \(N_E\) splits in
\(\mathbf Q(\sqrt q)\).

#### Proof

Since \(q\equiv1\pmod{24}\),

\[
q\equiv1\pmod8
\quad\text{and}\quad
q\equiv1\pmod3.
\]

As \(q\equiv1\pmod4\), the quadratic field \(\mathbf Q(\sqrt q)\) has
fundamental discriminant \(q\).  The congruence \(q\equiv1\pmod8\) implies
that \(2\) splits, and \(q\equiv1\pmod3\) implies that \(3\) splits.  Finally

\[
\left(\frac q{29}\right)=1
\]

is precisely the splitting condition at \(29\).  Hence \(2,3,29\) all split.
\(\square\)

### Lemma 3.2

Every \(q\in\mathcal P\) is a prime of good ordinary reduction for \(E\).

#### Proof

The primes ramified in the \(2\)-division field divide
\(\operatorname{disc}(f_2)\), hence belong to \(\{2,3,29\}\), while every
\(q\in\mathcal P\) is different from these primes.  Since \(f_2\bmod q\) is
irreducible, the Frobenius element on \(E[2]\) is a \(3\)-cycle in

\[
\operatorname{GL}_2(\mathbf F_2)\simeq S_3.
\]

An element of order \(3\) in \(\operatorname{GL}_2(\mathbf F_2)\) has
characteristic polynomial \(X^2+X+1\), and therefore trace \(1\).  Hence

\[
a_q(E)\equiv1\pmod2.
\]

Thus \(a_q(E)\) is odd.  If \(E\) were supersingular at \(q\), then
\(q\mid a_q(E)\).  Since \(q\ge5\), the Hasse bound
\(|a_q(E)|\le2\sqrt q<q\) would force \(a_q(E)=0\), a contradiction.
Therefore \(q\) is ordinary.
\(\square\)

---

## 4. Density of the support primes

### Proposition 4.1

The set \(\mathcal P\) has natural prime density \(1/24\).

#### Proof

Let \(L\) be the Galois closure of \(f_2\), so

\[
\operatorname{Gal}(L/\mathbf Q)\simeq S_3,
\]

and let

\[
F_0=\mathbf Q(\sqrt{-174})
\]

be its unique quadratic subfield.

Set

\[
K=\mathbf Q(\zeta_{24},\sqrt{29}).
\]

Since \([\mathbf Q(\zeta_{24}):\mathbf Q]=8\) and
\(\sqrt{29}\notin\mathbf Q(\zeta_{24})\),

\[
[K:\mathbf Q]=16.
\]

Moreover \(\mathbf Q(\zeta_{24})\) contains \(\mathbf Q(\sqrt{-6})\), so

\[
\sqrt{-174}=\sqrt{-6}\sqrt{29}\in K.
\]

Thus \(F_0\subseteq L\cap K\).  Since \(K/\mathbf Q\) is abelian and the
only nontrivial proper normal subfield of the \(S_3\)-extension \(L/\mathbf Q\)
is \(F_0\), we have

\[
L\cap K=F_0.
\]

Consequently

\[
[LK:\mathbf Q]
=
\frac{[L:\mathbf Q][K:\mathbf Q]}{[F_0:\mathbf Q]}
=
\frac{6\cdot16}{2}
=
48.
\]

For an unramified prime \(q\), the conditions

\[
q\equiv1\pmod{24},
\qquad
\left(\frac q{29}\right)=1
\]

are equivalent to Frobenius acting trivially on \(K\).  The condition that
\(f_2\bmod q\) be irreducible is equivalent to the Frobenius class in
\(S_3\) being the class of \(3\)-cycles.  A \(3\)-cycle acts trivially on the
quadratic resolvent \(F_0\), so these two prescriptions agree on
\(L\cap K=F_0\) and therefore define a conjugacy class in
\(\operatorname{Gal}(LK/\mathbf Q)\).

There are exactly two \(3\)-cycles in \(S_3\), while the \(K\)-component is
fixed to be the identity.  Hence the relevant conjugacy class has size \(2\)
inside a group of order \(48\).  Chebotarev's density theorem gives

\[
\delta(\mathcal P)=\frac{2}{48}=\frac1{24}.
\]

\(\square\)

### Remark 4.2

The first elements of \(\mathcal P\) are

\[
241,313,457,673,937,1009,1153,1753,2017,2089,\ldots.
\]

These numerical examples are not used in the proof.

---

## 5. The \(2\)-primary part

### Proposition 5.1

For every \(q\in\mathcal P\),

\[
L(E^{(q)},1)\neq0
\]

and

\[
\operatorname{BSD}(E^{(q)},2)
\]

holds.

#### Proof

We apply Banwait--Huang [BH26, Theorem 2.14], in the branch where
\(E(\mathbf Q)[2]=0\) and \(\Delta_E<0\).

The base curve is optimal, has odd Manin constant, analytic rank \(0\), and
the \(2\)-part of BSD holds for \(E\).  Also

\[
E(\mathbf Q)[2]=0,\qquad \Delta_E<0,
\qquad
\operatorname{ord}_2 L^{(\mathrm{alg})}(E,1)=0.
\]

Let \(d=q\in\mathcal P\).  Then \(d\) is squarefree, coprime to \(N_E\), and

\[
d\equiv1\pmod4.
\]

By Lemma 3.1 every prime dividing \(N_E\) splits in
\(\mathbf Q(\sqrt d)\).  Finally, the irreducibility of \(f_2\bmod q\)
says precisely that the unique prime divisor \(q\mid d\) is inert in the
cubic \(2\)-division field.

All hypotheses of [BH26, Theorem 2.14(1)] are therefore satisfied.  Its
conclusion gives simultaneously

\[
L(E^{(q)},1)\neq0
\]

and

\[
\operatorname{BSD}(E^{(q)},2).
\]

\(\square\)

---

## 6. The odd-primary parts

Fix \(q\in\mathcal P\), and abbreviate

\[
A=E^{(q)}.
\]

By Proposition 5.1,

\[
L(A,1)\neq0.
\]

Because \(2,3,29\) split in \(\mathbf Q(\sqrt q)\), the local quadratic
character is trivial at these primes.  Thus \(A\) has the same local
reduction type as \(E\) at \(2,3,29\): additive at \(2\), split
multiplicative at \(3\), and nonsplit multiplicative at \(29\).  At the twist
prime \(q\), the curve \(A\) has additive reduction.  Every other odd prime is
a prime of good reduction.

We also use repeatedly the following observation.

### Lemma 6.1

For every odd prime \(p\), the representation \(A[p]\) is absolutely
irreducible.

#### Proof

The LMFDB Galois-image data for \(E\) give maximal mod-\(p\) image for every
odd \(p\), hence \(E[p]\) is absolutely irreducible.  Quadratic twisting
tensors the residual representation by a one-dimensional character:

\[
A[p]\simeq E[p]\otimes\chi_q.
\]

Tensoring by a character preserves invariant subspaces and absolute
irreducibility.
\(\square\)

### Lemma 6.2 — the additive twist prime

The \(q\)-part of BSD holds for \(A\):

\[
\operatorname{BSD}(A,q).
\]

#### Proof

By Lemma 3.2, \(q\ge5\) is a good ordinary prime for the base curve \(E\),
and Lemma 6.1 gives irreducibility of \(E[q]\).

The proof of Banwait--Huang [BH26, Proposition 2.9(1)] applies the
additive-twist clause of Burungale--Skinner--Tian--Wan
[BSTW24, Theorem 9.21(c)].  Banwait--Huang [BH26, Remark 2.10] explicitly
records that semistability is used in this case only to manufacture the
required ramified auxiliary prime; for a non-semistable base curve one may
impose that ramification condition directly.

We take the auxiliary prime to be

\[
\ell=29.
\]

The curve \(E\) has multiplicative reduction at \(29\) and

\[
v_{29}(\Delta_E)=1.
\]

For the residual representation modulo \(q\), the standard multiplicative
reduction criterion gives ramification at \(29\), because \(q\nmid1\).
Moreover \(29\nmid \operatorname{disc}(\mathbf Q(\sqrt q))=q\).
Hence the required ramified-prime hypothesis is satisfied.  The rank-zero
descent used in [BH26, Proposition 2.9(1)] then gives
\(\operatorname{BSD}(A,q)\).
\(\square\)

### Lemma 6.3 — good ordinary primes

Let \(p\) be an odd prime at which \(A\) has good ordinary reduction.  Then

\[
\operatorname{BSD}(A,p).
\]

#### Proof

By Lemma 6.1, \(A[p]\) is irreducible.  Since \(p\) is a good prime,
\(p\neq29\).  At \(29\), the curve \(A\) has multiplicative reduction and

\[
v_{29}(\Delta_A)=v_{29}(\Delta_E)=1.
\]

Hence \(A[p]\) is ramified at \(29\).  Skinner's Theorem C [Ski16] applies:
it allows every prime \(p\ge3\) of good ordinary or multiplicative reduction,
requires irreducibility of \(A[p]\), and requires a distinct multiplicative
prime at which \(A[p]\) is ramified.  Together with \(L(A,1)\neq0\), it yields

\[
\operatorname{BSD}(A,p).
\]

\(\square\)

### Lemma 6.4 — the fixed multiplicative primes

The \(3\)-part and the \(29\)-part of BSD hold for \(A\).

#### Proof

At \(p=3\), the curve \(A\) has split multiplicative reduction.  By Lemma 6.1
the representation \(A[3]\) is irreducible.  The prime \(29\neq3\) is
multiplicative and \(A[3]\) is ramified there because

\[
3\nmid v_{29}(\Delta_A)=1.
\]

Thus [Ski16, Theorem C] gives \(\operatorname{BSD}(A,3)\).

At \(p=29\), the curve \(A\) has nonsplit multiplicative reduction.
Again \(A[29]\) is irreducible.  This time use the distinct multiplicative
prime \(3\), where

\[
29\nmid v_3(\Delta_A)=1.
\]

Skinner's theorem gives \(\operatorname{BSD}(A,29)\).
\(\square\)

### Lemma 6.5 — good supersingular primes

Let \(p\) be an odd good supersingular prime for \(A\).  Then

\[
\operatorname{BSD}(A,p).
\]

#### Proof

Since \(3\) and \(29\) are bad primes for \(A\), and \(q\) is additive,
a good supersingular \(p\) is distinct from \(3,29,q\); in particular
\(p\ge5\).

We verify the hypotheses of Fouquet--Wan [FW21, Theorem 1.7] for the
weight-\(2\) modular form attached to \(A\).

First, \(A[p]\) is absolutely irreducible by Lemma 6.1.

Second, at a good supersingular prime \(p\ge5\), the restriction to
\(G_{\mathbf Q_p}\) is irreducible (equivalently, tame inertia acts through
the fundamental characters of level \(2\)).  Therefore its semisimplification
cannot be of the forbidden form

\[
\bar\chi\oplus\bar\chi_{\mathrm{cyc}}\bar\chi
\]

appearing in [FW21, Theorem 1.7].

Third, take again

\[
\ell=29.
\]

The curve \(A\) has nonsplit multiplicative reduction at \(29\).
For weight \(2\), Fouquet--Wan identify their auxiliary local hypothesis with
a ramified special Steinberg representation twisted by the nontrivial
unramified quadratic character.  Nonsplit multiplicative reduction gives
precisely this unramified quadratic splitting character, and

\[
p\nmid v_{29}(\Delta_A)=1
\]

ensures that the residual extension remains ramified.  Also \(29\parallel
N_A\).

Thus [FW21, Theorem 1.7] applies.  Since \(L(A,1)\neq0\), [FW21,
Corollary 1.10] gives the \(p\)-part of the BSD formula, initially with the
modular-form period.

It remains only to compare this period with the Néron period.  The curve \(E\)
has a singleton rational isogeny class, and quadratic twisting preserves
rational isogenies; hence \(A\) also has a singleton rational isogeny class
and is optimal.  By Česnavičius--Neururer--Saha [CNS24], prime divisors of
the Manin constant of an optimal elliptic curve are supported at additive
reduction primes.  For \(A\) the additive primes are \(2\) and \(q\), while
the present \(p\) is a good supersingular prime.  Therefore \(p\) does not
divide the Manin constant, so replacing the modular period by the Néron
period does not change the \(p\)-adic valuation.  Hence

\[
\operatorname{BSD}(A,p)
\]

holds.
\(\square\)

### Proposition 6.6

For every odd prime \(p\),

\[
\operatorname{BSD}(A,p)
\]

holds.

#### Proof

The odd primes are exhausted by the following mutually exclusive cases:

1. \(p=q\), handled by Lemma 6.2;
2. \(p=3\) or \(p=29\), handled by Lemma 6.4;
3. \(p\notin\{q,3,29\}\) and \(A\) has good ordinary reduction, handled by
   Lemma 6.3;
4. \(p\notin\{q,3,29\}\) and \(A\) has good supersingular reduction, handled
   by Lemma 6.5.

There are no other odd bad primes.
\(\square\)

---

## 7. Proof of the main theorem

#### Proof of Theorem 1.1

Proposition 4.1 gives

\[
\delta(\mathcal P)=\frac1{24}.
\]

For \(q\in\mathcal P\), Proposition 5.1 gives

\[
L(E^{(q)},1)\neq0
\]

and the \(2\)-part of BSD.  Proposition 6.6 gives the \(p\)-part of BSD for
every odd prime \(p\).

Since the analytic rank is therefore \(0\), the Gross--Zagier--Kolyvagin
rank-zero consequences give equality of analytic and algebraic rank and
finiteness of the Tate--Shafarevich group; equivalently one may invoke the
local-to-global formulation [BH26, Proposition 2.4 and Theorem 2.5].
The equality of the BSD formula at every finite prime, together with the real
place, yields the strong BSD formula.

Thus

\[
\operatorname{BSD}(E^{(q)})
\]

for every \(q\in\mathcal P\).
\(\square\)

---

## 8. Computational certificate and sanity check

The theorem itself uses only finite arithmetic data for the base curve and
the cited theorems.  For reproducibility, the accompanying checker verifies:

- the defining support congruences;
- the Legendre condition \((q/29)=1\);
- irreducibility of \(f_2\bmod q\);
- the first explicit support primes.

A separate sweep performed during preparation found \(27\,667\) support
primes below \(10^7\).  Since

\[
\pi(10^7)=664\,579,
\]

the observed proportion among primes is

\[
\frac{27667}{664579}\approx0.041630867,
\]

close to the Chebotarev density

\[
\frac1{24}\approx0.041666667.
\]

This numerical agreement is only a sanity check and is not used in the proof.

---

## 9. Concluding remarks

The example is structurally simple despite being non-semistable.  The entire
failure of semistability occurs at \(2\), while the two odd multiplicative
primes \(3\) and \(29\) provide complementary ramification certificates:

\[
3\longleftrightarrow29.
\]

The nonsplit multiplicative prime \(29\) additionally supplies the uniform
Steinberg auxiliary prime required by Fouquet--Wan at every good supersingular
prime.  Thus the strong BSD formula is obtained by a genuine prime-by-prime
hybrid:

\[
\boxed{
\text{\(2\)-part}
+
\text{additive twist prime}
+
\text{ordinary/multiplicative parts}
+
\text{supersingular part}.
}
\]

The construction suggests an algorithmic extension problem: search for
non-semistable rank-zero curves possessing two odd multiplicative
ramification reservoirs, at least one of them nonsplit, together with a
compatible \(2\)-primary twist family.  That broader classification is not
pursued here.

---

## References

**[BH26]** B. S. Banwait and X. Huang, *On the identification of elliptic
curves that admit infinitely many twists satisfying the
Birch--Swinnerton--Dyer conjecture*, arXiv:2601.16044v3, 2026; to appear in
ANTS XVII.

**[BSTW24]** A. A. Burungale, C. Skinner, Y. Tian and X. Wan,
*Zeta elements for elliptic curves and applications*,
arXiv:2409.01350v2, 2024.

**[CM12]** B. Creutz and R. L. Miller,
*Second isogeny descents and the Birch and Swinnerton--Dyer conjectural
formula*, J. Algebra **372** (2012), 673--701;
arXiv:1105.4018v2.

**[CNS24]** K. Česnavičius, M. Neururer and A. Saha,
*The Manin constant and the modular degree*,
J. Eur. Math. Soc. **26** (2024), 573--637;
arXiv:1911.09446.

**[FW21]** O. Fouquet and X. Wan,
*The Iwasawa Main Conjecture for universal families of modular motives*,
arXiv:2107.13726v3.

**[Ski16]** C. Skinner,
*Multiplicative reduction and the cyclotomic main conjecture for
\(\mathrm{GL}_2\)*, arXiv:1407.1093; published version 2016.

**[LMFDB]** The L-functions and Modular Forms Database,
elliptic curve \(696.e1\) (Cremona \(696b1\)); data accessed August 2026.

---

## Appendix A. Exact finite data to recheck before submission

A submission build should independently reproduce the following finite
certificate, preferably in both SageMath and Magma:

\[
\begin{aligned}
N_E&=696,\\
\Delta_E&=-178176=-2^{11}\cdot3\cdot29,\\
E(\mathbf Q)_{\mathrm{tors}}&=0,\\
\operatorname{rank}E(\mathbf Q)&=0,\\
L(E,1)/\Omega_E&=1,\\
c_E&=1,\\
v_3(\Delta_E)&=1,\\
v_{29}(\Delta_E)&=1,\\
a_3(E)&=1,\qquad a_{29}(E)=-1,
\end{aligned}
\]

together with maximal odd residual Galois image and the singleton
\(\mathbf Q\)-isogeny class.

The proof above is designed so that a failure of any one of these finite
inputs is localized to a single lemma rather than hidden in the global
argument.
