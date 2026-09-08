# RUN-004 — 40,749 discriminants recomputed from scratch, and one check that could not have failed

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Phase 0 doc 01 §6, and the curve-arithmetic table Phase 1's census is built on
**Tools:** [`src04_curve_arithmetic_recompute.py`](../code/src04_curve_arithmetic_recompute.py)
**Logs:** [`src04-curve-arithmetic.json`](../data/gate-logs/src04-curve-arithmetic.json)

**Result: doc 01 is mathematically clean — the leading-term formula is stated correctly, including the two places it is usually mangled. The table Phase 1 sits on is clean too: 40,749 discriminants recomputed from a-invariants alone with zero mismatches, 135,787 valuations exact, 135,787 conductor-prime divisibilities holding. And the fourth check of this gate is vacuous: it tested whether rank is constant on an isogeny class, on a table where every class holds exactly one curve.**

---

## Part one: doc 01, read

The statement-and-quantifier audit. Checked line by line; the parts most often
got wrong are right here.

**§2.3, the leading-term formula.**

$$\frac{L^{(r)}(E,1)}{r!} = \frac{\#\Sha\,\Omega_E\,\operatorname{Reg}_E\,\prod_p c_p}{\#E(\mathbb Q)_{\mathrm{tors}}^2}$$

All five ingredients present, **torsion squared** in the denominator, `r!` in
place. Those are the two things routinely dropped, and neither is.

**§3, the global quantifier.** `∀E/Q, BSD-W ∧ BSD-F ∧ BSD-S`, with the exception
unit a single explicit curve — and the correct consequence: positive proportion,
low average rank, and "almost all twists" cannot absorb one real exception.

**§4.** Three counterexample shapes, and `weak BSD ⇏ strong BSD`. Correct: rank
equality alone does not give Ш finite outside the ranges where Kolyvagin
applies.

**§5.** `∀p` uniform control and a fixed-`p` theorem are different quantifiers.
Correct, and the distinction P5 spends ten documents inside.

**§6.** Rank and the L-function are constant on an isogeny class; the individual
ingredients of the strong formula can change between isogenous curves while the
prediction stays compatible. Both correct — the second is Cassels' isogeny
invariance of the BSD quotient.

**§7.** The analytic Ш as LMFDB reports it is §2.3 rearranged, and the document
says so, and forbids marking it as a proved `#Ш` without an independent descent.
The rearrangement checks out algebraically.

Nothing to report against doc 01. Stating that plainly is the finding.

## Part two: the table underneath Phase 1

Phase 1's census runs on a curve-arithmetic table extracted from John Cremona's
`ecdata` at commit `25cec5e`: 40,749 base curves. The package's own README
grades its headline figure `DIRECT_PRIMARY_SOURCE` — *"taken from the official
output and consistency-audited, not independently re-derived from scratch,"*
with **2 curves and 28 twists** recomputed.

This gate takes the other side, in exact integers, with no float anywhere —
every quantity here is an integer, and a float would be answering a different
question.

| check | scope | result |
| --- | ---: | ---: |
| Δ recomputed from `(a₁,a₂,a₃,a₄,a₆)` alone | 40,749 | **0 mismatches** |
| `v_p(Δ)` recomputed by exact division | 135,787 | **0 mismatches** |
| every conductor prime divides Δ | 135,787 | **0 failures** |

The discriminant is computed from `b₂ = a₁²+4a₂`, `b₄ = 2a₄+a₁a₃`,
`b₆ = a₃²+4a₆`, `b₈ = a₁²a₆+4a₂a₆−a₁a₃a₄+a₂a₃²−a₄²`, then
`Δ = −b₂²b₈ − 8b₄³ − 27b₆² + 9b₂b₄b₆`. The table's stored Δ is not read until
the comparison.

Only one direction of check 3 is a theorem — a prime of bad reduction divides
the discriminant, while a prime can divide Δ with good reduction after a change
of model. The converse is not checked, and its absence is not a gap.

## Part three: the check that could not have failed

The gate also tested doc 01 §6's assertion that **rank is constant on an isogeny
class**, using the class letter in the Cremona label. It reported:

> isogeny classes 40,749 · classes with more than one rank: **0**

40,749 classes for 40,749 curves. That ratio is the finding. Measured rather
than inferred:

| curves per class | classes |
| ---: | ---: |
| 1 | **40,749** |

Every label ends in `1`. This table is the census's **base curves** — one
representative per isogeny class, which is what "base curve" means in the
Banwait–Huang setting. **No class holds two curves, so no class could have
disagreed.**

Zero split classes is therefore not evidence that rank is constant on a class.
It is the shape of the table. The gate now reports check 4 as `VACUOUS` rather
than as a pass, records the class-size distribution beside it, and states that
three of its four checks carried evidence.

Testing doc 01 §6 needs a table that carries whole isogeny classes, not their
representatives. That is a later round, on different data — noted, not quietly
dropped.

**Why this is worth its own section.** The check was written, ran, returned
green, and would have appeared in this report as a fourth confirmation. What
stopped it was a number that looked too tidy: classes exactly equal to curves.
Nothing in the gate objected, because nothing was wrong — every comparison it
made was correct. There were simply no comparisons of the kind it claimed to be
making.

## What this round does not claim

* **Nothing about BSD.**
* **Not that the census's 36,687 / 247,391 is re-derived.** That figure is a
  count over twist pairs and admissibility conditions, and this round verified
  the arithmetic table beneath it, not the census built on top.
* **Not that `ecdata` is correct.** It verifies that this table is internally
  consistent and that its discriminants follow from its own a-invariants. If
  the a-invariants were wrong, every check here would still pass.
* **Nothing about isogeny classes**, per part three.
