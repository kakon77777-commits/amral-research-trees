# RUN-047 — The derived theorem before and after the referee, compared

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`18_Provisional_Derived_Theorem`](../../../amral/public/bsd/phase2/files/18_Provisional_Derived_Theorem.md) against [`27_Revised_Derived_Theorem_Candidate`](../../../amral/public/bsd/phase2/files/27_Revised_Derived_Theorem_Candidate.md), with [`20_Adversarial_Referee_Verdict`](../../../amral/public/bsd/phase2/files/20_Adversarial_Referee_Verdict.md) between them
**Tools:** [`src49_provisional_vs_revised.py`](../code/src49_provisional_vs_revised.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src49-provisional-vs-revised.json`](../data/gate-logs/src49-provisional-vs-revised.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: **three definitions of `𝒫`, one set.** `18` and `27` define it by `q ≡ 1 (mod 24)`, `(q/29) = 1` and `f₂` irreducible mod `q`; this tree's `src16` test has been used since RUN-015; Referee A's five conditions were run at RUN-032. Enumerated below 4,000 all three pick out **the same 19 primes**, and below 5,000 the same 23. **One of the document's three conditions is implied by the other two** — `(q/29) = 1` follows from `q ≡ 1 (mod 24)` and inertness, which RUN-018 had already recorded as a drill control over a range fifty times larger; what is new is that the redundancy sits in the corpus's own stated definition. **Of the five items `18` hands to a referee, `27` answers one — its proof router *is* the citation chain `18` asked for — defers one to a novelty audit it names explicitly, and leaves three open**; two of those three are exactly what RUN-039 and RUN-040 went at, and neither is closed. **`27`'s six-branch router is a partition of every prime**, verified for the three smallest members over all 109 primes below 600: six branches used, zero unrouted, no prime in two. And **the witnesses `27` names were computed here independently** — the `3 ↔ 29` swap is RUN-033's leave-one-out and the nonsplit Steinberg witness 29 is RUN-037's `W₋`. The claim label is consistent across all three documents: `18` says *Provisional Derived Theorem*, `20` upgrades to *DERIVED THEOREM CANDIDATE* while refusing *NEW THEOREM*, and `27` carries the upgraded label and names *PREPRINT CANDIDATE* as the next rung.**

---

## Three definitions of the same set

| | conditions | members below 4,000 |
| --- | --- | ---: |
| `18` and `27` | `q ≡ 1 (mod 24)`, `(q/29) = 1`, `f₂` irreducible mod `q` | **19** |
| this tree (`src16`, since RUN-015) | its own membership test | **19** |
| Referee A (RUN-032) | squarefree, `gcd(q,696) = 1`, `q ≡ 1 (mod 4)`, `2/3/29` split in `Q(√q)`, `q` inert in the 2-division cubic | **19** |

`241, 313, 457, 673, 937, 1009, …` — the same list three times, enumerated rather
than argued. The translation is exact: `q ≡ 1 (mod 24)` is 2 and 3 splitting in
`Q(√q)`, `(q/29) = 1` is 29 splitting, irreducibility mod `q` is inertness in the
cubic, and a prime that is `1 mod 24` with `(q/29) = 1` is automatically
squarefree and coprime to 696.

RUN-032 checked Referee A's list against `𝒫` from the other side and found no
prime the membership test rejects passing all five. This round closes the loop
from the third side.

## One of the three conditions is implied by the other two

`18` and `27` state three conditions. The third is redundant:

* `q` inert in the cubic means `Frob_q` is a 3-cycle, hence in `A₃`, hence
  trivial on the quadratic resolvent `F₀ = Q(√−174)` — so `(−174/q) = 1`;
* `q ≡ 1 (mod 24)` forces `(−1/q) = (2/q) = (3/q) = 1`, hence `(−6/q) = 1`;
* `−174 = −6 × 29`, which leaves `(29/q) = 1`, and for `q ≡ 1 (mod 4)` that is
  `(q/29) = 1`.

Measured both ways below 4,000: of the 19 primes that are `1 mod 24` with the
cubic irreducible, **none** violates `(q/29) = 1`; and weakening `mod 24` to
`mod 4` breaks the implication immediately — **44 counterexamples**, the smallest
being 17, 37, 41, 113, 157. So the redundancy follows from the mod-24 condition
and is not an accident of the range.

**This arm already knew.** RUN-018 recorded exactly this as a drill control, with
a measurement far stronger than this round's: over every `q ≡ 1 (mod 24)` below
**200,000**, 760 have `f₂` irreducible and every one of them has `(q/29) = 1`,
with the opposite cell empty. What is new here is only where the redundancy sits
— **in the corpus's own stated definition of `𝒫`**, not just in this tree's
membership test. `18` and `27` state a condition their other two conditions
already give. Nothing is wrong with the set; a reader is told three things when
two suffice.

RUN-018 also drew the consequence that matters: this overlap **is** `e_E = 2`,
which is why the density is `1/24` and not `1/48`. RUN-044 computed the resolvent
that makes it work.

## `18`'s five referee items, and what `27` did with them

| item | `27` | status |
| --- | --- | --- |
| exact convention match between FW's modular representation and elliptic `E[p]` at the nonsplit multiplicative witness | names the witness per branch, not the convention | **OPEN** |
| period normalization for every twist `E_q` | not mentioned | **OPEN**, measured here |
| exact isogeny/optimality phrasing in the period comparison | not mentioned | **OPEN**, premise closed here |
| precise citation chain for all `p`-part results | **the proof router is this chain** | **ADDRESSED** |
| novelty search | deferred explicitly | **DEFERRED** |

**One addressed, one deferred, three open.** And the three open ones are not
idle:

* the **convention match** is the seam RUN-046 found the corpus disagreeing
  about — whether the divisibility criterion *is* H3;
* **period normalization** is RUN-039's `c_E = 1`, still open, with RUN-040
  checking `01`'s weaker sufficient condition on all 19 members instead;
* **optimality** had its premise closed at RUN-031 and its mod-`ℓ` images
  certified at RUN-036, and optimality itself remains cited.

So this arm has been working on `18`'s open list for eight rounds without having
read it. That is a coincidence worth naming rather than a result.

## `27`'s router is a partition

`27` replaces `18`'s prose with six branches, each naming its theorem:

| branch | theorem | witness |
| --- | --- | ---: |
| `p = 2` | Banwait–Huang 2.14 + Creutz–Miller | — |
| `p = q` | BSTW 9.21(c) + rank-zero descent | 29 |
| odd good ordinary | Skinner Theorem C | 29 |
| `p = 3` | Skinner Theorem C | 29 |
| `p = 29` | Skinner Theorem C | **3** |
| odd good supersingular | Fouquet–Wan 1.7 + Cor 1.10 | 29 |

Run for `q = 241, 313, 457` over all 109 primes below 600: **six branches used,
zero unrouted, every prime in exactly one.** `27` writes 所有 primes exhaustive
and this is that sentence executed.

## The witnesses were computed here, from the other end

| `27` says | this tree computed | |
| --- | --- | --- |
| `p = 3` takes 29, `p = 29` takes 3 | RUN-033's leave-one-out: `{3: 29, 29: 3}` | ✔ |
| nonsplit Steinberg witness 29 | RUN-037's `W₋ = {29}` | ✔ |

RUN-033 derived the swap from `00_GCD_Witness_Lemmas` without reading `27`, and
RUN-037 derived `W₋` from `09`. The router and the lemmas name the same primes
from opposite directions.

## The claim label holds across all three documents

* `18`: **Provisional Derived Theorem**, explicitly not *Established New Theorem*
  — and it says why: not a visible mathematical gap, but the stage where a
  referee must check citations and conventions line by line.
* `20`: upgrades to **DERIVED THEOREM CANDIDATE**, refusing **NEW THEOREM**
  because novelty is a separate gate.
* `27`: carries **DERIVED THEOREM CANDIDATE** and names **PREPRINT CANDIDATE** as
  what a novelty/citation referee could unlock.

Three documents, one ladder, no drift. That is worth checking precisely because
it is the kind of thing that quietly does drift.

## And a control caught a bound guard of mine

The gate's own control widens the enumeration bound from 4,000 to 5,000, and it
went **red**. The cause was mine: `in_P_per_18` carried a hardcoded `q < 4000`
guard on the root search, so every prime above it silently failed the document's
definition and the three definitions appeared to part company at 4201, 4297,
4441 and 4801. **A disagreement manufactured by a guard, not found in the
arithmetic.**

The guard is gone and the bound is now the caller's: at 5,000 the three
definitions agree on 23 primes. The failure mode is the one this line keeps
meeting — a scan whose range is written into the scan rather than into its
caller — and this time a control caught it before the round shipped.

## The drill

**192 defects, 192 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 37 controls undisturbed, over 76 checks.

The 4 planted for this gate, each turning `provisional-vs-revised` red and nothing else:

| planted defect | went red |
| --- | --- |
| 18's set definition drops the cubic-irreducibility condition | `provisional-vs-revised` |
| the router loses its p = q branch, so q goes unrouted | `provisional-vs-revised` |
| 18's open referee items are reported addressed | `provisional-vs-revised` |
| the router's witnesses are reported matching without comparing | `provisional-vs-revised` |


## What this round does not claim

* **The theorems in `27`'s router are cited, not verified.** Banwait–Huang,
  BSTW, Skinner and Fouquet–Wan are external; this round checks that the router
  covers every prime and names a witness this tree can confirm.
* **A partition is not a proof.** That every prime lands in exactly one branch
  says nothing about whether that branch's theorem applies to it.
* **The set agreement is over primes below 4,000.** Three definitions agreeing
  on 19 primes is strong evidence they are the same set and not a proof of it.
* **`18`'s open items are scored, not closed.** Three remain open and this round
  closes none of them.
* **Novelty is untouched.** `26_Novelty_Search_Log` is not a subject of any round
  in this tree, and whether the result is new is not a question this arm has
  looked at.
