# RUN-022 — Hard-Zeta A-U.2e.1: the round holds, and the two things worth saying are about what a check is allowed to count as evidence

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `Hard_Zeta_Phase_II_Round_AU2e1_bundle.zip` (source item 40) — Reset-Block Arithmetic, with Aletheia as 協作整理
**Tools:** [`src22_au2e1_reset_block.py`](../code/src22_au2e1_reset_block.py) · [`src22_drill.py`](../code/src22_drill.py) · [`src22_emit_report_block.py`](../code/src22_emit_report_block.py)
**Logs:** [`src22-au2e1.json`](../data/gate-logs/src22-au2e1.json) · [`src22-drill.json`](../data/gate-logs/src22-drill.json)

**Result: every checkable claim in the round holds, on tens of thousands of real reset blocks. No defect found in the mathematics. Two findings, both about this arm's own instruments, and one correction to a misreading this run made and caught.**

---

## The sweep returns to Hard-Zeta

Items 38 and 39 were the crypto–semiotics compiler. Item 40 is
`A-U.2e.1`, which is exactly what [RUN-019](./RUN-019-HARD-ZETA-AU2E-MULTISCALE-RETURN.md)
named as the next successor in `ROUTE_MAP v1.5`. The two orderings agree, which is
worth a sentence only because they are independent: the sweep orders by file time,
the route map orders by mathematical dependency.

The round studies a **reset interval** `[a, b]` in the deficit
`δ_m = m·log₂3 − K_m`, and produces a depth–duration–tail triangle, a
relative-survival cost theorem, a disjoint-packing corollary, a bridge to an open
conjecture of Yolcu–Aaronson–Heule, and a renormalized anchor height.

## What is checkable, and what only looks checkable

The round's first identity is

> `Q_{a,b} = β·L_{a,b} + D_{a,b}`

and it is a **rearrangement of the definition of δ**. Substituting
`δ_m = m·β − K_m` turns it into `K_b − K_a = K_b − K_a`. Verifying it numerically
tests this arm's transcription of δ and nothing about the round, so it is recorded
as a transcription check and labelled as one. **A tautology dressed as a
verification is worse than no check**, because it inflates the count of things
that were confirmed.

The renormalized anchor identities are the opposite. They are theorems about the
accelerated map, not rearrangements:

> `A_m = 2^{−δ_m}·Y_m`,  `A_m = n + (1/3)·Σ_{i<m} 2^{−δ_i}`,  `A_{m+1} − A_m = (1/3)·2^{−δ_m}`

Since `δ_m = m·β − K_m` and `2^{−m·β} = 3^{−m}`, the first of these is exactly
`A_m = 2^{K_m}·Y_m / 3^m` — a **rational** quantity, with the irrational β
cancelled out. So the whole family is checked in exact rational arithmetic rather
than in floating point, and a float check here would have been a check of the
float library. Zero violations.

The **mod-8 bridge** is finite:

> for odd accelerated states, `q ≥ 3 ⟺ Y ≡ 5 (mod 8)`

That is exhaustive over the four odd residues, and it holds. The round then argues
that Yolcu–Aaronson–Heule Conjecture 4.12 — every nonconvergent trajectory contains
a value congruent to `5 mod 8` — implies `q ≥ 3` **infinitely often** in every CASP
candidate.

That step deserved suspicion, because "contains some value" is one occurrence and
"infinitely often" is not. **The round states the missing step itself**: any tail of
a nonconvergent trajectory is nonconvergent, so 4.12 applies to every tail. The
route map's summary omits it; the round does not. Reading the summary instead of the
source would have produced a false finding here.

## A correction this run made against itself

The relative-survival theorem is stated with a **free parameter** `h`: the
hypothesis is `δ_i > h` on the interior of the block, and the depth is `D = δ_a − h`.
The route map quotes the theorem with `D = δ_a − δ_b` instead.

The first reading here was that these are different quantities and the route map
substitutes one for the other. They are not different quantities — they are the
same theorem at two instantiations of its free parameter, and `h = δ_b` is
admissible exactly under the first-return condition and is the sharpest admissible
choice. **Reading a free parameter as a fixed one would have manufactured a gap
where the round has none.** Both instantiations are measured, and both hold on every
block: the weakest admissible `h`, and the route map's.

## The disjoint-packing bound, and a hypothesis worth stating

> for disjoint resets of depth at least `D₀` preserving ratio at least `ρ`,
> `Σ Y_{a_j} < N / (3(ρ − 2^{−D₀}))`

This is a corollary of the survival cost — each block costs `L_j > 3(ρ − 2^{−D₀})Y_{a_j}`,
and disjoint blocks in a window of length `N` have `Σ L_j ≤ N`. It holds on greedily
chosen maximal disjoint families, which is the shape the bound is about, rather than
on one hand-picked family.

Its hypothesis `ρ > 2^{−D₀}` is **strict**, and the first parameters this arm tried
sat exactly on the boundary, where the bound divides by zero. The gate now states
the hypothesis and refuses, which is the difference between a gate and a script: a
script crashes, a gate says which hypothesis was violated.

## Two findings, both about this arm's instruments

**A check that was implied by two others.** The first version of the gate compared
the anchor sequence against a running sum at every step, *and* compared the
increments against their closed form, *and* compared the final value. A planted
defect deleting the per-step comparison left the gate green — because given correct
increments and a correct final value, the per-step equality is implied, and the only
fact it added was the base `A_0 = n`. The redundant comparison is removed and the
base is asserted once, explicitly. **A check that cannot fail is not a weak check,
it is a claim about coverage that is false.**

**The drill found it, not review.** That is the second finding, and it is the reason
the drill exists. Nine defects are planted now, each of which must be reported *for
the reason named*, including one that violates the packing theorem's own hypothesis
and must be refused rather than crashed on.

## Measured

<!-- BEGIN GENERATED measured block: python code/src22_emit_report_block.py -->

| what | measured | value |
| --- | --- | --- |
| orbits walked | accelerated starts | `23` |
|  | steps per start | `60` |
|  | reset blocks found | `20923` |
|  | distinct accelerated valuations seen | `7` |
|  | steps with q ≥ 3 | `182` |
| renormalized anchor | violations, in exact rational arithmetic | `0` |
| relative survival | blocks checked at the weakest admissible h | `19581` |
|  | violations there | `0` |
|  | blocks checked at h = δ_b (the route map's form) | `20923` |
|  | violations there | `0` |
| depth–duration | blocks checked | `20923` |
|  | violations | `0` |
| disjoint packing | families checked | `12` |
|  | violations | `0` |
| the checks themselves | defects planted | `9` |
|  | caught, each for the reason named | `9` |
|  | null controls undisturbed | `2` |
|  | controls requiring the comparison to be able to reject | `5` |

**The mod-8 bridge, exhaustively.** Capping the accelerated valuation at `3`, the four odd residues give: `Y ≡ 1 (mod 8)` → `q ∈ [2]`, `Y ≡ 3 (mod 8)` → `q ∈ [1]`, `Y ≡ 5 (mod 8)` → `q ∈ [3]`, `Y ≡ 7 (mod 8)` → `q ∈ [1]`. So `q ≥ 3` holds for residue `5` and for no other, which is the biconditional the round needs. It is not vacuous on real orbits either: `182` of the steps walked here have `q ≥ 3`, and the valuations seen span `[1, 2, 3, 4, 5, 6, 7]`.

**The round's worked example recomputes.** With `D = 4` and `ρ = 1/2`, `ρ − 2^-D = 7/16` and the duration coefficient is `21/16` — the round states `7/16` and `21/16`.

Every figure above is emitted by `code/src22_emit_report_block.py` from the two gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

## What this run does **not** establish

- **Nothing about CASP.** The round compresses a hypothetical counterexample; it
  does not exclude one. The reset-mass split it ends with — shallow-reset dominated,
  infinitely deep-reset, giant-valuation-tail dominated — is a description of what a
  candidate must satisfy, not a proof that nothing does.
- **Nothing about Conjecture 4.12.** The bridge is an implication in one direction.
  This run checked the finite half of it, the mod-8 characterisation.
- **Nothing beyond the horizon walked.** Every inequality is verified on blocks
  drawn from a finite set of starts to a finite depth. Universally quantified claims
  are not settled by any of it; that is what the Lean arm is for, and none of this
  round is currently in it.

## Provenance

The archive was read from Neo's source folder and not modified. The orbits come from
this tree's own `hz_accel_code.py`, written from Round 03-A.1's prose, so the
enumerator and the engine are not the same code.

**Next:** item 41 is `Hard_Zeta_Phase_II_Round_AU2e2_bundle.zip` — the round's own
"Next" section names A-U.2e.2 (Reset Survival vs Positive Anchor) first, so the
sweep and the route map are expected to agree again. The first question is whether
the positive-anchor argument needs the anchor monotonicity proved here, which would
make this round a dependency rather than a sibling.
