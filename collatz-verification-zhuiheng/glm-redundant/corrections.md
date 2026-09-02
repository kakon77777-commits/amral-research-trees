# A correction to RUN-052, found while building this layer

**Date:** 2026-09-03
**Affects:** [`RUN-052`](../reports/RUN-052-HARD-ZETA-AU2D24-COMPENSATION.md), round A-U.2d.24

## What RUN-052 said

Finding 1 of that report was that Theorems 7.1 and 7.2 — the ultrametric
alignment laws — are asserted inside the bundle's validator and incremented by
no counter, so they appear nowhere in its report. That much is correct, and it
still stands.

The report then said, of the four clauses:

> Measured here: binary alignment over **219,440** segments with **0**
> valuation and **0** congruence failures; ternary alignment over **217,771**
> with **0** and **0**.

Those numbers are right. The reading of them was not.

## What is actually true

All four clauses are forced by the definitions, and cannot fail on any input.

From the quotient identity alone, `𝔡 = 2^Q n′ − 3^L n`:

* `ν₂(3^L n) = A` and `ν₂(2^Q n′) = Q + A′`. The hypothesis `c₂ > 0` **is**
  `Q + A′ > A`, so the two valuations differ and the ultrametric law gives
  `ν₂(𝔡) = A`.
* Dividing by `2^A`: `𝔡/2^A + 3^L(n/2^A) = 2^{c₂}·odd`, so the binary
  congruence is `0 mod 2^{c₂}`.
* `ν₃(2^Q n′) = B′` and `ν₃(3^L n) = L + B`. The hypothesis `c₃ > 0` **is**
  `L + B > B′`, so `ν₃(𝔡) = B′`.
* Dividing by `3^{B′}`: `𝔡/3^{B′} − 2^Q(n′/3^{B′}) = −3^{c₃}·(…)`, so the
  ternary congruence is `0 mod 3^{c₃}`.

Measured: 219,440 and 217,771 segments, 0 violations, and the premise
`Q + A′ > A` holds on 219,440 of 219,440 — because it is the branch condition
written differently.

So the two largest populations in that round are not evidence about the paper's
mathematics. They are the ultrametric law applied to a difference whose two
terms have known, unequal valuations.

## What this changes, and what it does not

The **paper is not wrong.** It calls these "exact valuation identities, not
statistical conditions", which is consistent with their being consequences. The
error is mine: I verified four statements, got zero violations, and reported the
population sizes as though the zeros were informative.

RUN-052's Finding 1 — that the alignment laws carry no counter — is unaffected.
What changes is the significance: a counter for them would have been a counter
for a restatement, which makes their absence less of a gap than the report
implied.

## How it was found

Not by GLM. By auditing my own eleven controls for the redundant layer before
dispatching them: `assert vp(d,2)==A` had been filed as an assertion that *can*
fail, and checking why exposed that it cannot. `judgement_key.json` records the
correction and the fact that `raw/collatz-judge-024.json` did not yet exist when
it was made — the batch had reached 004.

The pre-registered `my_findings.json` is deliberately **left unedited** at its
original seventeen entries, so the record of what this arm claimed before the
layer ran stays intact. This file is the correction.

## The lesson, stated plainly

Six shapes of cannot-fail check were catalogued across the sweep, and this is a
seventh instance of one of them — an assertion whose hypothesis is its own
conclusion in different variables — that I walked past twice: once when writing
the RUN-052 gate, and once when writing the RUN-052 report. What caught it was
being made to sort my own findings into *can* and *cannot* fail and defend each
side. Building the negative control for someone else's benefit is what audited
my own work.

## The same shape carries into A-U.2d.25 (RUN-053)

Checked after the above, on that round's own population: its synchronized
branch asserts `vp(d,2)==A`, `vp(d,3)==Bp`, and `gcd(omega,6)==1` on **131,639**
edges. All three are forced the same way — for a single edge `𝔡 = 2^q n′ − 3n`,
so `ν₂(3n) = A` against `ν₂(2^q n′) = q + A′`, and the branch condition `c₂ > 0`
**is** `q + A′ > A`; likewise `c₃ > 0` **is** `1 + B > B′`, giving `ν₃(𝔡) = B′`.
Both premises hold on 131,639 of 131,639, for the same reason as before. And
`gcd(ω, 6) = 1` then follows from dividing out exactly those two valuations, so
it is forced too.

RUN-053 did not make a headline of these, but its gate counts them among the
checks that hold, and the same caution applies: those zeros describe the
construction.

## Scope of the correction

| round | clauses forced | population | reported as |
| --- | --- | ---: | --- |
| A-U.2d.24 (RUN-052) | `ν₂(𝔡)=A`, binary congruence | 219,440 | verified, headline finding |
| A-U.2d.24 (RUN-052) | `ν₃(𝔡)=B′`, ternary congruence | 217,771 | verified, headline finding |
| A-U.2d.25 (RUN-053) | `ν₂(𝔡)=A`, `ν₃(𝔡)=B′`, `gcd(ω,6)=1` | 131,639 | verified, in passing |

None of it changes a theorem. What it changes is which numbers in two of my
reports carry evidential weight, and the answer for these is: none of them do.

## A second, larger one: Theorem 5.1 of A-U.2d.25 (RUN-053)

Found the same way, auditing the remaining controls before their answers came
back (`raw/collatz-judge-020.json` did not exist; the batch was at 014).

RUN-053 called the primitive-unit transport law

> `u′/u = 2^{−c₂} 3^{c₃} (1 + 𝔡/(3n))`

"the round's real content", and verified it as an exact `Fraction` on all
**187,769** edges. It is an **algebraic rearrangement of its own definitions**:

with `n = 2^A 3^B u`, `n′ = 2^{A′} 3^{B′} u′` and `𝔡 := 2^q n′ − 3n`,

> `u′/u = (n′/n)·2^{A−A′}3^{B−B′} = ((3n+𝔡)/(2^q n))·2^{A−A′}3^{B−B′}`
> `= (1 + 𝔡/(3n))·3^{1+B−B′}/2^{q+A′−A} = (1 + 𝔡/(3n))·3^{c₃}/2^{c₂}`.

Tested on **200,000 arbitrary triples** `(n, n′, q)` with `𝔡` defined by the
quotient identity and no Collatz orbit anywhere in the construction: **0
violations**. It holds for any such triple.

**This does not empty the round.** The paper's content is the *reading* — that
`c₂ − βc₃` is the negative primitive-unit log drift up to an exact
relative-defect correction — and the identity being definitional is precisely
why that reading is exact rather than approximate. What is wrong is my report
presenting 187,769 verified edges as evidence for it. No input could have
produced anything else.

The float form of the same identity in A-U.2d.26, `assert abs(lhs-rhs)<2e-11`,
is **deliberately left classified as a control**: its mathematical content is
equally forced, but as written it also tests float accuracy, which has a genuine
if remote failure mode. Per this arm's own rule, a doubtful case is omitted
rather than claimed.

## Running tally of this audit

| what | round | population reported as evidence | actually |
| --- | --- | ---: | --- |
| Theorem 7.1 both clauses | A-U.2d.24 | 219,440 | forced |
| Theorem 7.2 both clauses | A-U.2d.24 | 217,771 | forced |
| sync alignment, three clauses | A-U.2d.25 | 131,639 | forced |
| Theorem 5.1 transport identity | A-U.2d.25 | 187,769 | forced |

Four corrections, none of them a defect in the papers, all of them mine —
found by building the negative control for a second reader, before that reader
answered any of them.

## A weaker category, recorded but NOT corrected in the key

Two more controls turn out to be algebra on the assertions immediately above
them, rather than on a guard or a definition:

* A-U.2d.25, ternary-exclusive branch: `assert up == (2**(A-1))*(3**(B+1))*u + 1`
  follows from the preceding `d==2`, `q==1`, `Ap==0 and Bp==0` plus
  `n = 2^A 3^B u` — 200,000 arbitrary `(A, B, u)`, 0 violations.
* A-U.2d.25, binary-exclusive branch: `assert xi>=1 and xi%2==1` follows from
  `v2(d)=A` (itself forced) and the divisibility asserted on the line above —
  200,000 constructed cases, 0 violations.

These are a **different and weaker case** than the four corrections above. There,
the assertion restated its own guard or its own definition, so the whole check
was empty. Here the assertions that precede them in the same block *do* carry
content — the classification `d==2, q==1, A′=B′=0` is a real theorem — and only
the trailing algebra is redundant. The counter increments once per block, so the
counter is not inflated; a reader counting *assertions* would over-count.

They are **deliberately left as controls in `judgement_key.json`.** Two entries
were already corrected before their answers arrived; continuing to move entries
as I discover them starts to look like fitting the key to the result, even
though none of these had answered either. The pre-registered classification
stands, this note records the finding, and any score involving these two should
be read with it.

## Completing the audit of the remaining controls

For the record, the other seven were checked too and stand as controls:

* `assert abs(d) < (2**Q)*(3**L)` (A-U.2d.24) — a real estimate; RUN-052
  measured it loose by exactly a factor of three, which a forced identity would
  not be.
* `assert (d==0) == (c2==0 and c3==0)` (A-U.2d.24) — the reverse direction is
  genuine: equal valuations on both sides do not by themselves force the odd
  unit parts to agree.
* `assert -(2**q) < d < 3` (A-U.2d.25) — RUN-053 measured both ends nearly
  attained, which a definitional bound would not be.
* `assert TV<=runs*H+1e-10` and `assert J*QD*S+1e-10>=N*N` (A-U.2d.26) — real
  lemmas about arbitrary sequences and Cauchy–Schwarz, tested on random inputs
  rather than constructed ones.
* `assert abs(lhs-rhs)<2e-11` (A-U.2d.26) — kept as a control for the reason
  given above.

One is **half-forced** and worth naming rather than leaving implicit:
`assert 0 < Bcode <= bound` (A-U.2d.24). The lower half is trivially true —
`B_P` is a sum of positive terms — while the upper half is a genuine estimate
using only `q_j >= 1`. A single `assert` carrying one forced clause and one real
one is its own small hazard: it cannot be scored either way without splitting it.

**The criterion used throughout**, stated so the scoring is interpretable: an
assertion cannot fail if it is a restatement or algebraic consequence of its own
guard, its own definitions, or the code preceding it — *not* merely if it is a
true theorem about validly constructed inputs. Without that line every true
theorem checked on valid data would count, and the category would mean nothing.

---

# Correction 5 — found by GLM, not by me

**This one overturns a control I had audited twice and kept.**

`assert -(2**q) < d < 3` is A-U.2d.25's Theorem 3.1, the "sharp one-step defect
strip". RUN-053 made it the round's headline: *"a bound that is finally sharp"*,
attained at `d = 2` on 9,169 edges and reaching 126/128 at the lower end, in
explicit contrast to the previous round's spare factor of three.

GLM, shown only the script and asked whether the assertion can fail, returned:

> Since `r = x%M ∈ [0,M)` and `s = z%M ∈ [0,M)` with `M ≥ 1`, and
> `d = (1+3r−2^q·s)/M` exactly, we get `1+3r−2^q·s ≤ 1+3(M−1) = 3M−2 < 3M` so
> `d < 3`, and `1+3r−2^q·s+2^q·M = 1+3r+2^q(M−s) ≥ 1+2^q > 0` so `d > −2^q`,
> making the strip condition true for every constructible input.

That is a complete proof, and it is correct. Verified on **33,281** integral
cases built from arbitrary `(M, q, r, s)` with no Collatz orbit anywhere: 0
violations at either end.

**The strip is forced by the residue ranges.** It is sharp because `0 ≤ r,s < M`
is sharp — not because the accelerated dynamics make it so. The attainment I
measured and praised is measuring how close the residues get to their own
extremes.

The theorem remains true and remains useful downstream; what is wrong is
RUN-053 presenting 187,769 verified edges as evidence for it, and contrasting
its "sharpness" with A-U.2d.24's loose bounds as though the two were the same
kind of claim. They are not: the loose ones were estimates, this one is a range
computation.

## What this does to the verdict on the layer

The earlier framing in `README.md` — that almost all the value arrived before
the second reader answered — **was wrong, and is corrected there.**

It also means the pass-1 headline cannot be read as I first read it. GLM
answered `can_fail: false` to every question in both passes, which looked like a
worker that never disagrees. But of the four controls that ever got an answer,
it was **right on three** (`up == …`, `xi>=1 and xi%2==1`, and this one) and had
a defensible criterion disagreement on the fourth (`TV <= runs*H`).

So the constancy is not evidence of a yes-to-everything worker. It is evidence
that **my control set was contaminated** — I had built it from assertions I
believed tested the mathematics, and a majority of the ones that got answered
did not. The control arm failed as an instrument because I built it wrong, not
because the worker is a mirror.

The honest conclusion is therefore narrower and less comfortable than either of
the ones I drafted while waiting: **this layer produced one finding I had missed
after auditing the same set twice, and its discrimination remains unmeasured**,
because the instrument that was supposed to measure it was made of the same
misjudgements it was meant to catch.

