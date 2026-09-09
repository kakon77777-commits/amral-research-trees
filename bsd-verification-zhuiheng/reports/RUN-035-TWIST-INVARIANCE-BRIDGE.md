# RUN-035 — The twist-invariance bridge, and the one witness its split condition keeps alive

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`03_Quadratic_Twist_Invariance_Bridge`](../../../amral/public/bsd/phase2/files/03_Quadratic_Twist_Invariance_Bridge.md) — three candidate lemmas meant to push the Fouquet–Wan hypotheses from each twist back down to the base curve
**Tools:** [`src37_twist_invariance_bridge.py`](../code/src37_twist_invariance_bridge.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src37-twist-bridge.json`](../data/gate-logs/src37-twist-bridge.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: Lemma C is measured on both sides and it closes the question RUN-033 left open. On the split side, all 19 members of `𝒫` below 4,000 have 2, 3 and 29 split in `Q(√q)` and every local invariant of `E^(q)` at those primes — Kodaira type, `f`, `c`, `v_ℓ(Δ)`, the split flag — identical to the base's. On the inert side the same computation moves: `d = 5` makes 3 inert and flips its split flag, `d = 17` makes 29 inert and flips its. At `ℓ = 2` **nothing this tree computes can move** — 139 inert `d` were tried — because `q ≡ 1 (mod 4)` makes the twist unramified there, type `II*` has trivial component group so `c` is the constant 1, and additive reduction has no split flag; that prime is reported **untestable**, not passing. The consequence is the point: RUN-033 found the FW-H3 route holds a single witness, 29, the only nonsplit multiplicative prime. A twist by `d = 17` turns 29 **split** and the nonsplit set empties, so `𝒫`'s requirement that 29 split in `Q(√q)` is exactly what keeps that lone witness — verified on 19 of 19. Lemma A's computable shadow re-measured at 58/58 and 59/59 identical with 31 and 33 sign flips. **Lemma B is reported at the document's own status — a candidate derivation — so the bridge is NOT established.**

---

## What the bridge is for

Fouquet–Wan speaks about one `(E_d, p)`. Banwait–Huang needs one base curve to
license infinitely many `d`. `03` closes that gap with three lemmas and one
conclusion:

$$\mathrm{FW}(E,p)\Longrightarrow \mathrm{FW}(E_d,p)\quad\text{for all admissible }d,$$

which removes the `∀d` quantifier and leaves only `∀p > 2`. The document says so
itself in §6.

## The document marks its own middle lemma unfinished

Lemma B — that the FW-forbidden local semisimplification shape is preserved
under twisting — carries this line in the source:

> **狀態：標準表示論推導候選；正式文件需逐 theorem version 核對。**

A candidate derivation, needing per-theorem-version checking. The bridge is
`A ∧ B ∧ C`, so **with B open the bridge is not established**, and running the
two lemmas that are checkable does not change that. This round measures C,
re-measures A's computable shadow, and reports B where the document leaves it.

## Lemma C, both sides

`03` §4: if `ℓ | N` splits in `K_d = Q(√d)` then `χ_d` is trivial on `G_{Q_ℓ}`,
so `ρ̄_{E_d,p}|_{G_{Q_ℓ}} ≅ ρ̄_{E,p}|_{G_{Q_ℓ}}`. The computable content is that
every local invariant at `ℓ` must agree.

| | measured |
| --- | --- |
| every member has 2, 3, 29 split in `Q(√q)` | **19 of 19** |
| every local invariant preserved at all three | **19 of 19** |

And the direction that makes it a measurement rather than a tautology — at an
**inert** `ℓ` the character is nontrivial on `G_{Q_ℓ}` and the data must move:

| `ℓ` | an inert `d` | what changed |
| ---: | ---: | --- |
| 3 | 5 | `split_multiplicative` — **flipped** |
| 29 | 17 | `split_multiplicative` — **flipped** |
| 2 | — | **untestable**: 139 inert `d` tried, nothing moved |

`ℓ = 2` is reported as untestable rather than as a pass. Every member has
`q ≡ 1 (mod 4)`, so the twist is unramified at 2 and preserves the Kodaira type
and `v₂(Δ)`; the type is `II*`, whose component group is trivial, so the Tamagawa
number is the constant 1 for any curve carrying it; and 2 is additive, so there
is no split flag to flip. **The whole invariant set available is forced.** A
prime where the measurement cannot move is not a prime where the measurement
succeeded.

## The witness RUN-033 found has exactly one holder

That round measured something it could not then explain: the FW-H3 route
restricts to the **nonsplit** multiplicative primes, and of 696.e1's two
multiplicative primes only 29 is nonsplit. One witness, no spare — and the gcd
of an empty set being 0, an emptied nonsplit set makes **every** odd `p` fail.

Twisting at an inert prime flips split and nonsplit. So the question is whether
any member could turn 29 split, and the answer is measured:

* 29 is nonsplit for the base — **computed**;
* `d = 17` has 29 inert, and `E^(17)` has 29 **split** — the witness would be
  gone there;
* 29 stays nonsplit for **19 of 19** members.

`𝒫`'s condition that 2, 3 and 29 split in `Q(√q)` is what stands between this
family and an empty FW-H3 witness set. RUN-034 found the same condition doing the
same kind of work for `05`'s exact no-go. It is the third time a membership
condition that reads like bookkeeping has turned out to be load-bearing.

## Lemma A's computable shadow

Lemma A is representation theory — tensoring by a one-dimensional character is a
category auto-equivalence, so absolute irreducibility is invariant. That is not a
computation. What this tree can measure is the quantity the reducibility sieve
consumes, `a_ℓ² − 4ℓ`, invariant because `a_ℓ(E^{(d)}) = χ_d(ℓ)·a_ℓ(E)` squares
the sign away:

| `d` | good primes compared | identical | `a_ℓ` sign flips |
| ---: | ---: | ---: | ---: |
| 241 | 58 | **58** | 31 |
| 313 | 59 | **59** | 33 |

Roughly half the traces genuinely change and the discriminant does not, which is
what makes this a measurement rather than a restatement.

## The gate crashed rather than reported, and it was the same fault as RUN-030's

Planting "the local invariants drop the split flag" raised a `KeyError`: the
converse indexed `base["split_multiplicative"]` directly, and a stand-in that
removes the key is exactly what a drill is for. **A defect that produces a
traceback is not a defect a check caught** — RUN-020 recorded that when two
defects recursed instead of computing, and RUN-030 recorded it again when the
certificate indexed `red[2]` and 389.a1 had only one bad prime.

Seven direct indexes on that key are now reads that tolerate its absence, so a
missing split flag is reported — the flag did not flip — rather than thrown. The
check goes red either way; the difference is whether the drill measured the gate
or the interpreter.

## The drill

**144 defects, 144 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 24 controls undisturbed, over 64 checks.

The 4 planted for this gate, each turning `twist-bridge` red and nothing else:

| planted defect | went red |
| --- | --- |
| every prime is reported split, so the inert side never moves | `twist-bridge` |
| the local invariants drop the split flag, hiding the one thing that flips | `twist-bridge` |
| lemma B is reported as established | `twist-bridge` |
| the twist invariance is measured against the curve itself | `twist-bridge` |


## What this round does not claim

* **The bridge is not established.** C is measured, A's shadow holds, B is where
  the document left it, and `A ∧ B ∧ C` is what the conclusion needs.
* **Lemma A itself is not verified**, only its computable consequence. The
  category-equivalence argument is representation theory and is cited.
* **`ℓ = 2` is untestable here, not verified.** A finer invariant — the component
  group's Galois action for a type with a nontrivial component group, or the
  local representation itself — could test it, and this tree computes neither.
* **The inert side uses two `d` outside `𝒫`**, chosen because they are inert.
  They are counterexamples to invariance-without-the-split-condition, not family
  members.
* **The bound is 4,000**, the checklist's bound, as in RUN-032 and RUN-033.
