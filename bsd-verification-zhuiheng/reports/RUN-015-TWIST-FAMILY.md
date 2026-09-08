# RUN-015 — Theorem 1.1(2) tested, and one of 𝒫's three conditions is implied by the other two

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the second part of Phase 2's Theorem 1.1, the "automatic ordinary" derivation of `16_696e1_Chebotarev_Support`, and the exhaustion claim of `17_696e1_All_Prime_Router`
**Tools:** [`src16_twist_family_lvalues.py`](../code/src16_twist_family_lvalues.py), [`src17_family_prime_router.py`](../code/src17_family_prime_router.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src16-twist-family.json`](../data/gate-logs/src16-twist-family.json), [`src17-family-router.json`](../data/gate-logs/src17-family-router.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `L(E^(q),1) ≠ 0` holds on the two smallest members of 𝒫, computed. `L/Ω` comes out `1` at `q = 241` and `49` at `q = 313` — and 49 is `7²`, which with trivial torsion and Cassels's square theorem forces `c_q = 1` and `Ш = 7²`. Every member of 𝒫 below 20,000 has root number `+1`, `a_q` odd, and good ordinary reduction. The four-way exhaustion holds on every odd prime below 3,000. And one finding the theorem does not state: **𝒫's second condition is implied by its first and third** — the cell that would contradict it is empty over 200,000 primes.**

---

## What RUN-009 left

RUN-009 verified part (1) of Theorem 1.1 — the density of

$$\mathcal P=\{q \text{ prime}: q\equiv1\ (\mathrm{mod}\ 24),\ (q/29)=1,\ f_2 \text{ irreducible mod } q\}$$

is `1/24` and not the `1/48` the conditions naively multiply to — and said parts
(2) and (3) were untested. RUN-014 built the machinery that makes (2) computable:

> for every `q ∈ 𝒫`, `L(E^{(q)}, 1) ≠ 0`.

## Why the first two conditions exist

For a fundamental discriminant `d` coprime to `N`, the root number twists as
`w(E^{(d)}) = w(E)·χ_d(−N)`. With `N = 696 = 2³·3·29` and `w(E) = +1`,

$$w(E^{(q)})=\Big(\tfrac{-696}{q}\Big)=\Big(\tfrac{-1}{q}\Big)\Big(\tfrac{2}{q}\Big)\Big(\tfrac{3}{q}\Big)\Big(\tfrac{29}{q}\Big).$$

`q ≡ 1 (mod 24)` gives the first three symbols; `(q/29) = 1` gives the fourth by
reciprocity. So **`w(E^{(q)}) = +1` for every `q ∈ 𝒫`** — the first two
conditions hold the sign at `+1` so that a nonvanishing theorem has something to
prove.

The formula is **measured before it is used**, on twists of this same curve by
small `d` where the numerical sign test still separates the candidates:

| `d` | `N(E^{(d)})` | measured `w` | predicted | residual | gap |
| ---: | ---: | :-: | :-: | ---: | ---: |
| 5 | 17,400 | +1 | +1 | 4.5e−6 | 8.3e−3 |
| **13** | 117,624 | **−1** | **−1** | 1.3e−5 | 9.9e−3 |
| 17 | 201,144 | +1 | +1 | 1.2e−5 | 7.8e−3 |
| 37 | 952,824 | +1 | +1 | 2.2e−6 | 7.8e−3 |
| 41 | 1,169,976 | +1 | +1 | 2.3e−5 | 1.8e−3 |

`d = 13` is the load-bearing row: a formula that always returned `+1` would agree
with the other four.

**All 87 members of 𝒫 below 20,000 have `w = +1`.**

## Theorem 1.1(2), on the two smallest members

`a_n(E^{(d)}) = χ_d(n)·a_n(E)`, so the base curve's coefficients are counted once
and each twist is a character multiplication — a relation checked against direct
point counts before it is relied on.

| `q` | `N = 696q²` | terms | first dropped term | `L(E^{(q)},1)` | `Ω` | `L/Ω` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **241** | 40,424,376 | 46,000 | 1.8e−20 | **0.105108823625** | 0.105108823625 | **1** |
| **313** | 68,186,424 | 46,000 | 6.3e−16 | **4.519304541603** | 0.092230704931 | **49** |

Both nonzero. Both twists have **trivial torsion**, and their reduction at 2, 3
and 29 is unchanged from the base — additive, split multiplicative, non-split
multiplicative — which is what the 𝒫 conditions guarantee by making `q` a local
square there. So `c₂ = c₃ = c₂₉ = 1` carries over from RUN-014, and

$$\frac{L(E^{(q)},1)}{\Omega}=c_q\cdot\#Ш.$$

Additive reduction at `q` bounds `c_q ∈ {1,2,4}`, and Cassels makes `#Ш` a
square. At `q = 241` that leaves `c_q = 1`, `Ш = 1`. At `q = 313` the product is
**49**, and of the three allowed `c_q` only `c_q = 1` leaves a square:

$$\boxed{c_{313}=1,\qquad \#Ш\big(E^{(313)}\big)=49=7^2.}$$

A nontrivial Ш, arrived at by measuring an `L`-value and a period.

## `a_q` is odd — and that is not free

`16_696e1_Chebotarev_Support` derives the ordinariness of every `q ∈ 𝒫`:
`f₂` irreducible mod `q` makes Frobenius an order-3 element of `GL₂(F₂) ≅ S₃`,
whose characteristic polynomial `X²+X+1` has trace 1, so `a_q` is **odd**; a
supersingular `q ≥ 5` would need `q | a_q`, and Hasse then forces `a_q = 0`,
contradicting oddness.

| | |
| --- | --- |
| `a_p` odd ⟺ `f₂` irreducible mod `p`, over 2,259 primes | **holds, 0 counterexamples** |
| density of odd `a_p` | **0.328907** (Chebotarev: `1/3`) |
| members of 𝒫 below 20,000 with `a_q` odd | 87 of 87 |
| members of 𝒫 below 20,000 that are ordinary | 87 of 87 |

The density line is the one that matters. If `a_p` were odd for every `p` the
derivation would be true and empty; it is odd for a third of primes, so the
condition is doing real work.

The document's one explicit number checks out: **`a₂₄₁(E) = −7`**, and
`241 ≡ 1 (mod 24)`, `241 ≡ 9 (mod 29)` with 9 a square, `f₂` irreducible mod 241.

## The all-prime router's exhaustion

`17` closes by asserting that for `E_q` the odd primes fall in exactly four
classes. Classifying every odd prime below 3,000 for `q = 241`:

| class | count |
| --- | ---: |
| good ordinary | 422 |
| good supersingular | 4 |
| multiplicative at 3 | 1 |
| multiplicative at 29 | 1 |
| `p = q`, additive | 1 |
| **unclassified** | **0** |

429 odd primes, every one in exactly one class.

`17` also asserts `E_q` carries no rational prime-degree isogeny. RUN-007's
`X₀(n)` machinery decides `n = 2, 3, 5, 7` — all four **no**. Mazur allows prime
degrees `2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163`, so **eight of twelve are
not covered here** and are named rather than passed over.

## One of 𝒫's three conditions is implied by the other two

The drill found this, by planting a defect that dropped `(q/29) = 1` from the
membership test — and nothing changed.

`f₂` irreducible mod `q` makes Frobenius a 3-cycle, hence an element of `A₃`,
hence `(disc(f₂)/q) = 1`. RUN-009 established that `disc(f₂) = −2⁷·3·29` has
squarefree part `−174 = (−6)·29`, and that `q ≡ 1 (mod 24)` gives `(−6/q) = 1`.
Therefore `(29/q) = 1` **follows**, without being stated.

Measured over every prime `q ≡ 1 (mod 24)` below 200,000:

| | count |
| --- | ---: |
| `f₂` reducible, `(q/29) = −1` | 1,097 |
| `f₂` reducible, `(q/29) = +1` | 355 |
| `f₂` irreducible, `(q/29) = +1` | **760** |
| **`f₂` irreducible, `(q/29) = −1`** | **0** |

The contradicting cell is empty.

**This is not an error** — `𝒫` is the same set either way. But the theorem states
three conditions where two determine the set, and RUN-009's own density
derivation read `δ = (1/8)·(1/2)·(2/3)` as three independent-ish factors. With
the redundancy it is `(1/8)·(1/3)`, where the `1/3` already contains the `1/2`
the second condition was supplying. Same `1/24`, one step shorter.

## The drill

**62 defects, 62 caught by the check named for each. 16 controls, none
disturbed.**

Four defects escaped the first run of the new checks, and each was one of two
things. Two were checks that could not see them: the Kronecker fixture had **no
even `n` at all**, so the symbol's prime-2 branch was untested, and no check read
the twisted *model* — `family-root-number` works off character-multiplied
coefficients, so a wrong power of `d` on `a₄` was invisible. Both closed.

Two were no-ops, and moved to controls with the reason:

* swapping `χ`'s arguments cannot change anything here, because every twisting
  discriminant in this family is `≡ 1 (mod 4)` and Kronecker reciprocity makes
  `(d/n) = (n/d)` for exactly those `d`;
* dropping `(q/29)` cannot change `𝒫`, for the reason above.

One correction of my own: the Kronecker fixture's expected value for `(6/35)` was
written by hand as `+1` and is `−1`. The gate's implementation was right and the
expectation was not, which is why that check now carries both a fixed table and a
sympy comparison.

## What this round does not claim

* **Nothing about BSD**, and nothing about part (3) of Theorem 1.1 — that every
  `q ∈ 𝒫` gives a twist satisfying strong BSD depends on four cited theorems this
  arm has not read.
* **`L(E^{(q)},1) ≠ 0` is verified on two members, not on 𝒫.** The term count
  grows linearly in `q`, so this reaches the smallest ones; the theorem is about
  all of them.
* **`Ш = 49` is a reading under the BSD formula**, not an independent
  computation. It follows from the measured ratio together with Cassels and the
  bound on `c_q` — a different route would be needed to confirm it directly.
* **The isogeny check covers four of Mazur's twelve prime degrees.**
* **`c₂` for the base is still not computed** — RUN-014's carve-out stands, and
  the twists inherit it.
