# RUN-024 — Hard-Zeta A-U.2e.3: the round holds, its own corrigendum turns out to be measurable, and one of its sections cannot be tested on any orbit that ends

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `Hard_Zeta_Phase_II_Round_AU2e3_bundle.zip` (source item 42) — Infinite-Support Degeneration, shipped with a Terminology Corrigendum v0.1.1 to A-U.2e.2
**Tools:** [`src42_infinite_support.py`](../code/src42_infinite_support.py) · [`src42_drill.py`](../code/src42_drill.py) · [`src42_emit_report_block.py`](../code/src42_emit_report_block.py)
**Logs:** [`src42-au2e3.json`](../data/gate-logs/src42-au2e3.json) · [`src42-drill.json`](../data/gate-logs/src42-drill.json)

**Result: everything this arm can reach holds, exactly. No defect found in the mathematics. The round's headline is a negative result and a correctly stated one. The new content here is a measurement its own corrigendum makes possible and does not supply — plus one section that turns out to be untestable on any terminating orbit, which this run nearly reported as confirmed.**

---

## The round is honest about being negative

A-U.2e.2 proved that a CASP counterexample multiplies into infinitely many A- or
B-type obstruction atoms. The natural next move is to kill that with Hard-Zeta
mass. This round says plainly that **you cannot**:

> `Σ_{n∈S} n^(−s) ≤ ζ(s) < ∞` for **any** `S`, and an infinite `S` can be sparse
> enough to make that sum as small as you like.

So cardinality alone finishes nothing, and what has to be preserved is
`atom + renewal type + duration + depth`. That is a round declining an available
shortcut, and §13 states the same thing a second way: distinct odd
`y_1 < y_2 < …` satisfy `y_j ≥ y_1 + 2(j−1)`, so the mass converges no matter
what.

Checked here **by construction rather than by assertion** — for a target `ε`, an
explicit infinite set is built and its mass shown below `ε` in exact rationals. A
claim that infinite sets can be arbitrarily light is worth something only if one
can be produced.

## Where the line falls, and it moved since last round

| | |
| --- | --- |
| **Unconditional**, checkable on real orbits | the correction bank's increment identity, and its **two expressions for `A_m` agreeing**; the telescoping step behind the Depth Budget; the Mass No-Go |
| **A transcription check**, labelled not counted | §3's `A_b/A_a = 2^D · Y_b/Y_a` |
| **Conditional** on a surviving reset | the Reset Bank-Cost *inequality*, the Depth Budget, Fixed-Depth Sparsity, the Weighted B-Injection Budget |
| **Structurally untestable here** | §8's suffix-minimum characterisation |

A surviving reset (`Y_b ≥ Y_a` across a coefficient contraction) is a
counterexample to the Terras coefficient-stopping conjecture. RUN-023 measured
**0** below `2·10⁵`; this run repeats the census on its own sample and the count
is in the generated block below. So the third row is a set that is empty as far as anyone has looked, and
this arm checks none of it.

**The useful decomposition is in the second-to-last row.** §4's Depth Budget has
two halves: multiply `A_{b_j}/A_{a_j}` over disjoint ordered intervals and bound
the product by `A_{b_R}/A_{a_1}`; then substitute `A_b/A_a ≥ 2^D`. **Only the
substitution needs survival.** The telescoping needs a monotone bank and disjoint
intervals and nothing else, so it is checked here on real orbits with intervals
chosen without regard to whether anything survives.

## Finding 1 — the corrigendum is measurable, and the answer is "half the time"

The corrigendum separates two indices and warns against conflating them:

- the **accelerated odd-endpoint** crossing, at block `L` with `2^Q_L > 3^L` — the
  one A-U.2e.2 indexes by, and the one RUN-023 measured;
- the **modified-step** first crossing at depth `k`, which can land *earlier*,
  inside that final accelerated block.

It says the two are equivalent in finiteness, that their time indices need not
agree, and that the B line must not identify them without explicit conversion. It
does not say how far apart they are.

One accelerated block is `v` modified steps of which exactly **one** is odd, so
after `L` blocks the modified index is `Q_L` and the odd count is `L`. The
crossing condition `3^{o(k)} < 2^k` therefore first fires at
`k = ⌊L·log₂3⌋ + 1`, and the gap the corrigendum warns about is `Q_L − k`.

Measured exactly, by **two routes sharing no code** — one walking `T` and testing
`3^o < 2^k` at every step, the other computing `⌊L·log₂3⌋` from a bit length. The
distribution is in the generated block below. The short version: **they coincide
on about half of all starts, and on the rest the endpoint lags by a
geometrically-distributed number of modified steps.** The warning is not
theoretical bookkeeping; it bites on half the population.

## Finding 2 — §8 cannot be tested on any orbit that ends, and the degenerate version looks like a result

§8 characterises A-renewal atoms as the strict suffix minima of `δ_m`, and notes
that because the bank is strictly increasing these are automatically suffix minima
of `Y_m`. That is a clean statement and RUN-023's A/B classification was built on
`Y` suffix minima, so checking whether the two characterisations pick the same
positions looked like the obvious job.

They agree on every orbit tested. **And that agreement is worth nothing**, because every
orbit here terminates at `Y = 1`: nothing before the final position can be a
strict suffix minimum of anything, so both sets are the single last index on
every single orbit. "The two characterisations agree on every orbit" is a
statement about two singletons, and the set sizes are reported beside it below.

Suffix minima are a notion about a **divergent** orbit, which is what a CASP
candidate is and what no known integer has. The check is kept in the gate,
reporting the set sizes beside the agreement, precisely so the agreement cannot be
read as content — and it reports `testable_here: false` rather than a pass.

I nearly wrote the agreement up as a finding. It is in this report because
catching it is the only thing about it worth recording.

## Finding 3 — `A_m ≤ n + m/3` is a CASP-candidate statement, not an orbit statement

The round states the correction bank under the hypothesis `δ_m > 0`, and the
upper bound needs exactly that: every increment is `(1/3)·2^(−δ_m)`, which is at
most `1/3` only while `δ_m ≥ 0`. A real orbit **crosses**, `δ` goes negative, the
increments exceed `1/3`, and the bound must fail.

The round is right and this is not a correction to it — it is a note about where
the hypothesis bites, and it makes the check two-sided. The gate asserts the bound
holds at every position **before** the crossing and requires it to be observed
**failing** after one; a version that only checked the easy half would pass with
the hypothesis silently doing all the work.

---

<!-- BEGIN GENERATED measured block: python code/src42_emit_report_block.py -->

| what | measured | value |
| --- | --- | --- |
| odd starts walked | both crossing indices computed for each | `29999` |
| **the two routes disagree on** | direct walk of T against ⌊L·log₂3⌋+1 from a bit length | `0` |
| odd-step count ≠ L | one odd step per accelerated block | `0` |
| **gap `Q_L − k` is zero** | the two indices coincide | `49.84%` |
| mean gap | modified steps | `1.0032` |
| largest gap seen | modified steps | `14` |
| bank increment-identity violations | A_{m+1}−A_m = (1/3)·2^(−δ_m), exact | `0` |
| the two expressions for `A_m` disagree on | `2^(−δ_m)·Y_m` against `n + (1/3)Σ 2^(−δ_i)`, accumulated independently | `0` |
| upper-bound violations before the crossing | A_m ≤ n + m/3 while δ ≥ 0 | `0` |
| starts where that bound fails after the crossing | the negative half, without which the test is one-sided | `9980` |
| telescoping violations | gapped disjoint intervals, exact | `0` |
| …of which the inequality is **strict** | with contiguous intervals it is an equality and cannot fire | `7624` |
| §3 transcription-check violations | labelled, not counted as a result | `0` |
| **surviving resets** | Y_b ≥ Y_a; a survivor would refute Terras | `0` |
| defects planted / caught by their own check | `code/src42_drill.py` | `12 / 12` |

**The corrigendum's gap, distributed.** `Q_L − k` in modified steps, where `Q_L` is the accelerated block endpoint A-U.2e.2 indexes by and `k` is the true modified first crossing:

| gap | starts | share |
| --- | --- | --- |
| 0 | 14951 | 49.84% |
| 1 | 7543 | 25.14% |
| 2 | 3727 | 12.42% |
| 3 | 1910 | 6.37% |
| 4 | 932 | 3.11% |
| 5 | 463 | 1.54% |
| 6 | 236 | 0.79% |
| 7 | 116 | 0.39% |
| 8 | 55 | 0.18% |
| > 8 | 66 | 0.22% |

**The Mass No-Go, by construction.** For each target the set is infinite and its mass is an exact rational: `s=2`, target `1/1000000` → `{2^j : j >= 11}, infinite` with mass `3.18e-07`; `s=2`, target `1/1000000000000` → `{2^j : j >= 21}, infinite` with mass `3.03e-13`; `s=3`, target `1/100000000000000000000` → `{2^j : j >= 23}, infinite` with mass `1.94e-21`.

**§8, and why the agreement is not evidence.** Over `1999` orbits the δ-characterisation and the Y-characterisation pick the same positions every time — and every set has size `1`, the final index alone. Reported as `testable_here: false`.

Every figure above is emitted by `code/src42_emit_report_block.py` from the two gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument, and the bug it caught in itself

`src42_drill.py` plants defects and requires each to be caught **by the check
named for it**. Its first pass reported **three misses, and all three were real
holes in this arm's checks** — in every case the gate stayed fully green with the
defect in place.

- **A check that could not fail — and my first fix could not fail either.** The
  bound `A_m ≥ n` was scanned for at every position; weakening it to `A_m ≥ 0`
  changed nothing, because `A_m ≥ n` is *implied* by `A_0 = n` plus positive
  increments. I replaced it with explicit assertions of the base and of strict
  monotonicity — and **the drill caught both of those too**: `A_0 = n` is true by
  construction of `bank()` (`2^0·n/3^0`), and monotonicity follows from the
  increment identity that another defect already covers. Replacing one vacuous
  check with two more taught the actual lesson: **when a check cannot fail, the
  fix is a second independent expression of the same quantity, not another proxy
  for the same one.** §2 supplies one — `A_m = n + (1/3)Σ_{i<m} 2^(−δ_i)` — which
  is accumulated separately and compared against `2^(−δ_m)·Y_m`. That comparison
  is a statement about the exact excursion identity, and both sides of it are now
  drilled. Fourth appearance of this class in this tree (RUN-022's redundant
  per-step anchor comparison, RUN-023's cap equivalence, and §8 above).
- **An inequality that was secretly an equality.** The telescoping check used
  *contiguous* intervals, so the product telescoped exactly to `A_last/A_first`
  and neither `>` nor `<` could ever fire. Inverting the comparison left the gate
  green because there was nothing to compare. The intervals now leave gaps, which
  is where the theorem has content — skipping stretches can only lose mass — and
  the gate additionally refuses unless the inequality is observed **strict**.
- **A mutation that was not a defect.** D8 changed `3^o < 2^k` to `3^o ≤ 2^k`.
  That is a no-op: `3^o` is odd and `2^k` is even, so they are never equal and the
  two predicates coincide. The drill had reported a miss it had not earned —
  **a planted defect that changes nothing is not a defect that survived.**
  Re-aimed at the odd-step count, which that route genuinely depends on.

D8/D9 exist as a pair on purpose: they break the corrigendum measurement's two
routes *separately*, because the whole value of that measurement is that two
independent computations agree, and a "agreement" between two spellings of one
computation would be worth nothing.

Before any of that, the gate caught a defect in itself. §3's identity check failed
on **94,388 of 94,388** pairs — I had written `2^(−D)` where the round has `2^D`.
**A check that fails on everything is reporting its own defect, not the
subject's**, and the 100% rate is the signature. Fixed, and then relabelled: since
`A_m` is *defined* as `2^(−δ_m)·Y_m`, that identity is a rearrangement of the
definition. It tests this file's `bank()`, not the round, and it is now reported
as a transcription check rather than counted among the results.

## Route map

`ROUTE_MAP v1.8` names three successors: **A-U.2d** (Transducer Rationality),
**A-L** (Giant Valuation Tail), and **A-U.2e.4** (Renewal Diophantine Rigidity).
The sweep's file ordering puts item 43 next; the two orderings have agreed four
times running and this is the first round where the route map offers a branch
rather than a single successor.

Relevant to whichever comes next: Finding 1 gives the conversion the corrigendum
asks for. If the B line imports A-U.2e.2's correction cap, the duration in
modified steps is `⌊L·log₂3⌋ + 1`, not `L` and not `Q_L`, and the difference from
`Q_L` is zero only about half the time.

## What this run does not claim

1. That a surviving reset exists. None was found; finding one would refute the
   Terras coefficient-stopping conjecture.
2. That the Depth Budget, Fixed-Depth Sparsity, or the Weighted B-Injection Budget
   hold. Each quantifies over surviving resets and none is checked here.
3. That §8 is true or false. It is untestable on terminating orbits, which is a
   statement about this arm's reach, not about the section.
4. That the Infinite-Support Degeneration Frontier is established. Its ingredients
   above the survival line are checked; the frontier itself rests on a CASP orbit.
