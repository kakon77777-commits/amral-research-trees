# RUN-003 — auditing the audit: the rejection holds, and the corpus strengthened it later

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Phase 0 doc 05, *Neo.K 舊「格點秩收斂」路線審計* — the corpus's formal rejection of its own author's earlier idea
**Tools:** [`src02_rejected_route_recurrence.py`](../code/src02_rejected_route_recurrence.py) · [`src03_multiplicity_nogo.py`](../code/src03_multiplicity_nogo.py)
**Logs:** [`src02-rejected-route.json`](../data/gate-logs/src02-rejected-route.json) · [`src03-multiplicity-nogo.json`](../data/gate-logs/src03-multiplicity-nogo.json)

**Result: all four of the audit's objections hold. The verdict also held downstream — no document in the corpus claims any of the four salvage conditions is met, and the one P5 document that revisits the route re-derives the rejection independently and upgrades it from "the burden is unmet" to "FALSE IN GENERAL" with an explicit counterexample. That counterexample is correct, recomputed here in exact rationals. This round adds the half neither document states, and it is the half that says why the failure is not about precision.**

---

## Why audit an audit

Doc 05 is the most self-critical act in this corpus: a formal review of Neo.K's
own prior "lattice-point rank convergence" idea, ending

> Archive as exploratory analogy; do not use as Phase 1 proof route.

A rejection needs checking in both directions. It can be **too weak** — the
route survives and gets used anyway. It can be **too strong** — a workable idea
killed for a bad reason, which is the more expensive mistake because nobody goes
looking for it. And it can be **correct but unenforced**, which is the same as
absent.

## The four objections, read

| § | objection | verdict |
| --- | --- | --- |
| 1 | If the lattice relation `rank_a ≤ ord L_a` is assumed at each scale, where does that inequality come from? If its proof uses a classical BSD-type link, it is circular. | **Holds**, and correctly hedged — it states an unmet burden, not a proven circularity. |
| 2 | `rank E(Q)` is an integer-valued global arithmetic invariant; approximate point counts, matrix ranks and discrete homology ranks do not converge to it as `a → 0`. | **Holds.** Mordell–Weil rank is not determined by any archimedean approximation. |
| 3 | Even where `L_a → L`, `ord_{s=1} L_a` need not converge to `ord_{s=1} L`. | **Holds**, and is the sharpest of the four. See below. |
| 4 | `A_a → A` and `B_a → B` do not give `A = B` unless `A_a = B_a` legitimately for each `a` — and if `A_a = B_a` *is* lattice BSD, the difficulty has been moved into the lattice layer, not solved. | **Holds**, and is the best sentence in the document. |

One structural observation, offered as shape rather than as a defect. The four
salvage conditions map onto the objections unevenly: §1 and §4 both land on GR-4
(non-circular bridge), while **GR-1 (faithful discretisation) has no
corresponding objection section at all.** GR-1 is an additional requirement the
audit imposes without having argued for it in the body.

A second, and this one is a genuine gap in coverage rather than in reasoning:
**the audit accepts that a lattice L-function `L_a(E,s)` exists and attacks the
limit.** It never asks whether the object is definable — `L(E,s)` comes from an
Euler product and a modular form, and what a lattice analogue would be is a
prior question. Its absence does not weaken the verdict; if anything it means
"四項皆未完成" is a list of four things needed *given* the object exists.

## Did the verdict hold downstream?

A verdict nothing honours is a verdict in name only, so the whole corpus was
scanned for the rejected route's vocabulary.

| | |
| --- | ---: |
| documents scanned | 85 |
| route-signal hits | 61 |
| of those, inside the audit itself | 21 |
| documents outside the audit carrying route vocabulary | 8 |
| **salvage conditions GR-1…GR-4 claimed met, anywhere** | **0** |

Zero is the number that matters. Doc 05 says all four are unmet; nothing in the
corpus contradicts it.

Most of the eight documents are a **name collision the gate cannot resolve, and
does not pretend to**: "lattice" in this subject usually means an arithmetic
determinant lattice, a Mordell–Weil lattice, or an integral lattice — standard
vocabulary with no relation to the rejected route. The gate reports where to
look and refuses to call a hit a defect, because that judgement needs reading.

## What reading found instead

`p5/BSD_Rank_Uniform_Zeta_Primitivity_Reduction_v0.1` carries an entire
**§9 — Grid / continuum route 的 multiplicity no-go**, and its summary table
records:

> `grid convergence ⇒ multiplicity stabilization` — **FALSE IN GENERAL** — 有明確反例

So the route was not quietly reused. It was **independently re-derived and
sharpened**: doc 05's careful "the burden is unmet" became a general refutation
with a witness.

### The counterexample, recomputed

Lemma 9.1 offers `f_a(z) = z² + az = z(z+a)`. Recomputed in exact rational
arithmetic — no floating point anywhere, because the claim is about an
integer-valued order and a float would be answering a different question:

| `a` | ord at 0 | roots in \|z\|<1/100 | sup\|f_a−f_0\| on \|z\|≤1 |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 1 |
| 1/10 | 1 | 1 | 1/10 |
| 1/1000 | 1 | **2** | 1/1000 |
| 1/10⁶ | 1 | **2** | 1/10⁶ |
| 1/10¹² | 1 | **2** | 1/10¹² |
| −1/10⁶ | 1 | **2** | 1/10⁶ |

`ord_{z=0} f_0 = 2`. The order is **1 for every `a ≠ 0`** and **2 in the limit**,
while `sup|f_a − f_0| = |a|·R → 0`. The counterexample is correct and minimal.

### What this round adds

The point-order does not converge. **The zero count in a fixed neighbourhood
does.** `f_a` has roots at `0` and `−a`; once `|a| < r`, both lie inside
`|z| < r`, so that disc holds exactly **2** roots for every such `a` — the same
as the limit's order at the point. That is Hurwitz's theorem, and it is measured
in the table above: the count is 1 while `−a` is still outside the disc, and 2
from the moment it enters.

Neither doc 05 nor §9.1 states this, and it is the half that says what kind of
failure this is:

> The order jumps **while the neighbourhood count is stable**. So a method that
> measures the neighbourhood and reports the point is not imprecise — it is
> wrong at infinite precision.

It also explains a detail of doc 05 that would otherwise read as arbitrary. Its
remedy list asks first for *「在 $s=1$ 鄰域的解析控制」* — analytic control in a
**neighbourhood** of `s=1`, not at `s=1`. That is exactly the right thing to ask
for, and this is why.

## What this round does not claim

* **Nothing about BSD**, and nothing about whether any `L_a` behaves like `f_a`.
  A polynomial in one variable refutes the general inference, which is all
  either document claims of it.
* **It does not certify GR-1…GR-4 as unmet.** It measures that nothing in the
  corpus claims otherwise — a weaker statement, and the true one.
* **It does not audit the idea Neo.K originally had**, only the audit of it. The
  original draft is not in this corpus; doc 05's seven-step summary of it is the
  only version available here, and a rejection read only through the rejecter's
  paraphrase is a limit of this round worth stating.

## Credit where the corpus earned it

Rejecting its own author's idea in a numbered framework document, then
re-deriving that rejection independently in a later sub-line and strengthening
it with a witness, is the strongest discipline this arm has seen in the corpus
so far. Doc 05's hedging is also right: it says *if* the proof uses a classical
link *then* it is circular, rather than asserting circularity it had not shown.
