# RUN-033 — The GCD witness lemmas, run, and the empty set they do not survive

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`00_GCD_Witness_Lemmas`](../../../amral/public/bsd/phase2/files/00_GCD_Witness_Lemmas.md) — the four-paragraph algebraic floor under [`12_Hybrid_Odd_Prime_Router`](../../../amral/public/bsd/phase2/files/12_Hybrid_Odd_Prime_Router.md) and [`17_696e1_All_Prime_Router`](../../../amral/public/bsd/phase2/files/17_696e1_All_Prime_Router.md)
**Tools:** [`src35_gcd_witness_lemmas.py`](../code/src35_gcd_witness_lemmas.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src35-gcd-witness.json`](../data/gate-logs/src35-gcd-witness.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: all three witness lemmas now have computed inputs. 696.e1's bad primes, found from `Δ = −2¹¹·3·29` rather than assumed: 2 additive (`II*`), 3 **split** multiplicative, 29 **nonsplit** multiplicative, both with `n_ℓ = 1`. Lemma 1's `gcd n_ℓ = 1`, so the generic witness exists for every odd non-multiplicative `p` and the failure set is empty. Lemma 2's leave-one-out returns `3 ↦ 29` and `29 ↦ 3` — exactly the swap `17`'s Case C performs, now derived instead of asserted. Lemma 3 restricts to the nonsplit primes and **2 of 2 becomes 1 of 2**: the FW-H3 route has one witness and no spare. And the direction the document's phrasing hides — the gcd of an empty set is 0, and every prime divides 0, so an emptied set means **every** odd `p` fails rather than none — is exhibited on a curve found by search, `[0,−1,0,−6,−2]`, whose single multiplicative prime 71 is split: lemma 1 passes there with gcd 1 while lemma 3's gcd is 0. Across all 19 members of `𝒫` below 4,000 the twist keeps its multiplicative primes at exactly `{3, 29}` with `n = 1`, `q` additive for its own twist, and both gcds equal to 1.**

---

## What the lemmas are for

Every witness `17_696e1_All_Prime_Router` picks is an instance of one of them.
Case A takes `ℓ = 29`; Case B takes `ℓ = 29` for all `p` outside `{3, 29}`;
Case C swaps `3 ↔ 29`; FW-H3 takes `ℓ = 29` again. The router justifies each
choice with the same sentence — `v₂₉(Δ_E) = 1`, so `p ∤ v₂₉(Δ_E)` — and
`00_GCD_Witness_Lemmas` is where that sentence is turned into a finite
statement:

> \[\exists\ell:\ p\nmid n_\ell \iff p\nmid \gcd_\ell n_\ell.\]
> Hence the only failures are the finitely many odd prime divisors of the gcd.
> … This is the exact algebraic reason the all-prime witness problem is finite.

Nothing in the corpus computes the gcd.

## The inputs, found rather than assumed

`Δ = −178176 = −2¹¹ · 3 · 29`, and the bad primes are read off that
factorisation and then classified by Tate's algorithm rather than by the
document:

| `p` | reduction | Kodaira | `v_p(Δ)` | |
| --- | --- | --- | ---: | --- |
| 2 | additive | `II*` | 11 | not a multiplicative witness |
| 3 | multiplicative | `I₁` | 1 | **split** |
| 29 | multiplicative | `I₁` | 1 | **nonsplit** |

`17` asserts "29 為 nonsplit multiplicative" and never computes it. It is
correct, and 29 is the **only** nonsplit prime available.

## The three lemmas, run

| | | |
| --- | --- | --- |
| **generic witness** | `gcd(n₃, n₂₉) = gcd(1, 1) = 1` | failure set **empty** |
| **leave-one-out** | `p = 3 → ℓ = 29 (n = 1)`; `p = 29 → ℓ = 3 (n = 1)` | both distinct |
| **nonsplit FW witness** | nonsplit `= {29}`, **1 of 2 survived**, gcd `= 1` | failure set **empty** |

The middle row is Case C, computed. The bottom row is the one worth reading
twice: the restriction to nonsplit primes halves the witness set, and what
survives is a singleton. The FW-H3 route is not failing — it also has nothing
in reserve.

## The empty set, and why "gcd = 1" on its own means nothing

The lemma says the failures are the odd prime divisors of the gcd. If the set
being intersected is empty the gcd is 0, and **every** prime divides 0 — so the
lemma then says every odd prime is a failure, not that there are none. That is
the opposite of how an empty case usually reads, and the third lemma is exactly
the one that can empty its set, because it throws away the split primes.

Reporting `gcd = 1` for 696.e1 without ever showing the other outcome would be
reporting an accident. So the gate searches for it, over 31 nonsingular models:

| curve | multiplicative | lemma 1 | lemma 3 |
| --- | --- | --- | --- |
| `[0, −1, 0, −4, −1]` | none | **gcd 0** → every odd prime fails | — |
| `[0, −1, 0, −6, −2]` | `{71}`, split | gcd 1 → no failures | **gcd 0** → every odd prime fails |

The second row is the sharp one: **on one curve lemma 1 passes and lemma 3
fails.** A gcd of 1 for one of these lemmas says nothing whatever about the
other, and 696.e1 clears both only because it has a nonsplit prime to spare —
one.

## The family

`17`'s Case C asserts the twist's multiplicative primes are still exactly 3 and
29 with both valuations 1. Run on every member of `𝒫` below 4,000:

* **19 of 19** keep multiplicative primes exactly `{3, 29}` with `n = 1`;
* **19 of 19** have `q` itself additive for `E^(q)` — type `I₀*`, which is what
  puts Case A's `p = q` in the additive branch;
* **19 of 19** have lemma 1's and lemma 3's gcds both equal to 1.

So the witness problem is not merely finite for the family, it is empty: there
is no odd prime at which any of the three witnesses fails, for any member.

## The drill

**136 defects, 136 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 22 controls undisturbed, over 62 checks.

The 4 planted for this gate, each turning `gcd-witness-lemmas` red and nothing else:

| planted defect | went red |
| --- | --- |
| the gcd of an empty set reports no failures instead of all of them | `gcd-witness-lemmas` |
| every multiplicative prime is reported split, emptying the nonsplit set | `gcd-witness-lemmas` |
| the empty-set search is given nothing to search | `gcd-witness-lemmas` |
| the leave-one-out lets a prime be its own witness | `gcd-witness-lemmas` |


## What this round does not claim

* **A witness is not a theorem.** These lemmas say a suitable `ℓ` exists. Whether
  the ordinary/multiplicative/FW theorem that consumes it applies is Referee B's
  and C's territory and is untouched here.
* **The single nonsplit witness is reported as measured, not as a defect.** One
  is enough. It is also all there is, and that is worth saying only because the
  same computation shows what an empty set would mean.
* **The two empty-set curves are search results with no arithmetic relation to
  696.e1.** They exist to make the lemma testable, and they carry nothing about
  the family.
* **The family bound is 4,000**, the same as RUN-032's, and it is the checklist's
  bound rather than the family's — RUN-009 ran the density to 2×10⁷.
* **Valuations are taken through Tate's algorithm on each model**, which is what
  detects a non-minimal one; they are not read from the raw discriminant
  factorisation.
