# Collatz — verification and computation arm, 數學戰士「墜衡」

Durable research tree for the local verification role on the Collatz
conjecture (3x+1 problem), opened 2026-08-14 (Asia/Taipei) by 數學戰士「墜衡」
(Zhuì Héng), Claude Opus 5, working under Neo.K / AMRAL Research Lab.

Neo.K set the target and assigned this agent the local verification and
computation role. This tree is therefore an **instrument**, not an argument. It
answers bounded, decidable questions about the map exactly, states how far each
answer reaches, and is built to be able to return "no".

## Status boundary

**The Collatz conjecture is not solved here, and nothing here is evidence for
it.** No novelty of any kind is claimed.

What exists is a bounded exhaustive verification and the gate suite that makes
it worth believing:

- every `n` with `1 ≤ n ≤ 2^40` reaches 1, relative to the archived
  implementation;
- as a free corollary at the same bound, no nontrivial cycle has all of its
  elements `≤ 2^40`.

`2^40` is far below the published frontier, which stands at **all `n` below
`2075 × 2^60 ≈ 2^71.02`** (Barina, *Improved verification limit for the
convergence of the Collatz conjecture*, The Journal of Supercomputing **81**:810,
2025), with the project page reporting progress beyond it. This arm did not re-run
that verification. It did verify, while rechecking Paper 01, that the DOI resolves
to the stated journal, volume and article, and that the project page states that
figure.

*Correction:* until 2026-08-14 this section said `2^68`, citing Barina 2021. That
understated the frontier by three doublings and cited a superseded milestone. It
was found by verifying Neo.K's own reference audit, which had the current figure. A local run is never a record attempt; a bound this arm
can finish and fully archive is preferred over one that sounds impressive.

A finite verification to any `N`, however large, says something about `[1, N]`
and nothing else. It is not support for the conjecture, and this tree will not
describe it that way.

## Where mathematics and computation do not align

Neo.K's standing position, which this tree now records with its evidence: going
from formal language to mathematical language to programming language, **the
choice of underlying symbol space is not fully identical** — it can be, and it
can fail to be. A body of mathematics can be highly complete *as mathematics* and
still not reduce cleanly to a machine, and where it fails to reduce, the first
hypothesis should not be that the theory is wrong.

Across <!-- COUNTS -->53 source items and thirty-three runs<!-- /COUNTS -->, **nothing in the source
mathematics failed a check**. The defects clustered in the *realizations* — two
in the subject's own computational apparatus, considerably more in this arm's
code, which is what the 304-defect mutation suite exists to catch. But the
non-alignment is real, and it has at least four distinct shapes: fully alignable,
alignable in shadow only, structurally unreachable, and **scale-invisible** — a
check that is green, exact and drilled while reporting nothing about what the
theorem is actually for.

It also runs in both directions. In Rounds A-U.1 and A-U.2a the machine holds
exactly what the standard formalism provably discards. Neither symbol space
contains the other.

[`reports/CHARTER.md`](./reports/CHARTER.md) states this in full, with the
instance behind each band.

## Read in this order

1. [`reports/CHARTER.md`](./reports/CHARTER.md) — what this arm answers, what it
   will never certify, and how it keeps itself falsifiable. Read this before any
   number.
2. [`reports/RUN-001-T40.md`](./reports/RUN-001-T40.md) — the `[3, 2^40]` run:
   method, numbers, all five gates, the three defects found in the harness, and
   the weaknesses that remain.
3. [`reports/RUN-002-OT-SERIES.md`](./reports/RUN-002-OT-SERIES.md) — independent
   re-derivation of the finite claims of Neo.K's *Collatz Operation Translation
   Series*: package integrity (and the defect that stops its own verifier on the
   author's platform), Paper 05's `k=16` benchmark reproduced, and every theorem
   of **all nine core papers** rechecked against referees that assume none of
   them, including Paper 01's bibliography verified against arXiv and Crossref.
   Includes the §14 bridge tying two papers' correction terms together, and
   `K(2^40) = 550` — Paper 09's frontier function evaluated at the scale the
   engine actually measured.
4. [`reports/RUN-003-PROVENANCE-CHAIN.md`](./reports/RUN-003-PROVENANCE-CHAIN.md) —
   a different question, asked of the draft chain that preceded the series:
   **is the repair's account of itself complete?** Every one of the ten published
   diffs applies to its published original under an applier that demands exact
   context, and reproduces the repaired file byte for byte — 276 hunks — so no
   edit escapes the correction ledger. The pre-repair text is attested by drafts
   archived three days earlier. Includes the two checks of my own that turned out
   to be vacuous, and how the drill found them.
5. [`reports/RUN-004-HARD-ZETA-ORIGIN.md`](./reports/RUN-004-HARD-ZETA-ORIGIN.md) —
   the origin of the Hard-Zeta line, and the first **measured** values of its
   central quantity `Z_k(s)`, on `[2, 2^32)` with rigorous two-sided bounds. Also
   a result rather than a reproduction: `sigma(n) = 3` is impossible for every
   `n`, so `E_2 = E_3` exactly and the `L = 1` form of the route's uniform decay
   obligation is **false**. Plus a hypothesis its ROUTE MAP drops, a defect in my
   own measurer, and a claim of mine the drill deleted.
6. [`reports/RUN-005-HARD-ZETA-ROUND-01.md`](./reports/RUN-005-HARD-ZETA-ROUND-01.md) —
   Round 01's exact refinement algebra, rendered executable and confronted with
   direct iteration: the child recursion, the recursive hard height, the four-way
   identity, exact mass conservation, the trichotomy and the `U^k` closed form all
   hold. The algebra computes `Z_k(s)` **exactly**, and it lands inside RUN-004's
   independently measured bracket at every depth — two routes, no shared code.
   Adds a **hazard budget**: fifty levels share 1.12 nats while `n = 27` stays
   hard. Includes three real gaps the drill found in my own checks.
7. [`reports/RUN-006-HARD-ZETA-ROUND-02.md`](./reports/RUN-006-HARD-ZETA-ROUND-02.md) —
   Round 02's two-compartment split `Z_k = C_k + R_k`, checked against Round 01
   throughout. Two results: the **mass-weighted** hazard is the right object, and
   by up to 94× — at depth 12 the worst chart loses 99.75% while the global rate
   is 2.5%; and the Terras conjecture, in Round 02's own finite-word form, holds
   on **all 81,119 first-crossing words up to length 24**, worst case at 49% of
   its bound. Also a check made vacuous by the very emptiness it measures.
8. [`reports/RUN-007-HARD-ZETA-ROUND-03A.md`](./reports/RUN-007-HARD-ZETA-ROUND-03A.md) —
   Round 03-A compresses the coefficient frontier to a single unproved quantity,
   the minimum surviving anchor `m_k`. This run **measures it**: 23 values from a
   `τ_c` record scan of `[2, 2^32)`, rising to 2,788,008,987, each converted by
   the paper's own §28 into a rigorous upper bound on the true infinite `C_k(s)`
   — `C_447(2) ≤ 2.3e-10`. Escaping 23 times is not evidence of escaping forever,
   and the report says so. Also a circular check and a tautological one, found by
   the drill in my own work.
9. [`reports/RUN-008-HARD-ZETA-ROUND-03A1.md`](./reports/RUN-008-HARD-ZETA-ROUND-03A1.md) —
   Round 03-A.1 re-coordinates the frontier by accelerated exponent codes. Its
   §34 diagnostic table reproduces exactly and is **extended from m = 8 to
   m = 60** under a prune that validates itself. And the anchor sequence it
   defines turns out to be RUN-007's, switching at exactly `k = K_m` — two
   coordinate systems, two independent computations, one sequence. Measured
   agreement, not the theorem, which the paper is right to withhold.
10. [`reports/RUN-009-HARD-ZETA-ROUND-03A2.md`](./reports/RUN-009-HARD-ZETA-ROUND-03A2.md) —
    Round 03-A.2's exact 2–3 bridge, which holds everywhere checked, §30's
    diagnostic reproduced to the digit, and a **priced route**: §39 asks the next
    round to extract a counterfamily for §24's endpoint-parity target, and the
    extraction shows the longest odd-`M` runs belong to the **anchored** codes.
    So that counterfamily is the CST counterexample itself — the route is
    equivalent, not cheaper. Worth knowing before spending a round on it.
11. [`reports/RUN-010-HARD-ZETA-ROUND-03A3.md`](./reports/RUN-010-HARD-ZETA-ROUND-03A3.md) —
    Round 03-A.3 finds a **unique zero-lift edge**: every node has at most one
    source-preserving child, so the tree of exact codes collapses to one
    deterministic path per canonical source. Verified over 13,929 node/exponent
    pairs. Unlike RUN-009's verdict this is a real structural gain — the target
    stays equivalent to CST, but the *object* is genuinely smaller. Measured: a
    spine is exactly as long as its source's remaining subcritical life.
12. [`reports/RUN-011-HARD-ZETA-ROUND-03A4.md`](./reports/RUN-011-HARD-ZETA-ROUND-03A4.md) —
    Round 03-A.4 prices the spine: every unit of extra 2-adic valuation is paid
    from a Sturmian budget of density `γ ≈ 0.585`, while a Haar-typical orbit
    would spend **1** per step. Ledger verified throughout. Two measurements: the
    Haar gap is real on every spine tested, and §34's **Legendre gate opens on 2
    of 168 depths** — so continued-fraction tools have rigorous purchase on
    almost none of the spine, which makes the paper's own No-Go 3 the normal case.
13. [`reports/RUN-012-HARD-ZETA-A-LINE-CLOSURE.md`](./reports/RUN-012-HARD-ZETA-A-LINE-CLOSURE.md) —
    the B-line handoff and the **A-line closure**. Read as a scope claim first:
    the closure says *reduction programme complete*, explicitly not that Terras
    or Collatz is proved, and leaves CASP open — and it is checked that way, with
    seven planted edits that would make it claim more. Its one external
    dependency (López–Stoll, arXiv:2101.12747) was fetched, and the liminf
    equality it is used for appears verbatim in that abstract. Three
    measurements: the B line's ratio supremum is attained at a **length-8** word
    and nothing to length 24 comes within a factor of ten; the finite-local
    no-go's own witness `2^{m+1}−1` is up to **5 × 10⁹** times larger than the
    cheapest start with the same subcritical reach; and spines die having spent
    **93–98%** of the Sturmian budget, so the near-saturation A.5 requires of a
    counterexample is the ordinary end state rather than an exotic one. Also
    corrects a truncated table in RUN-011. And the bundle is checked as a
    bundle: its seven re-shipped rounds are **byte-identical** to the standalone
    ones already verified as items 19-28, so those runs carry over.
14. [`reports/RUN-013-HARD-ZETA-AU1-ANCHOR-ERASURE.md`](./reports/RUN-013-HARD-ZETA-AU1-ANCHOR-ERASURE.md) —
    Phase II opens, and Round A-U.1's main result is that its own programme does
    not work: invariance, uniform integrability and the critical mean are
    **mutually consistent**, so no contradiction comes from them alone. Both
    countermodels verified exactly — the Bernoulli critical measure, and the
    mechanical code, whose closed formula agrees with the implementation RUN-008
    wrote from a different round's description. What survives is the anchor
    cocycle, and this run **measures** it: every genuine integer's lift digits
    settle by `m = 11`, while the countermodel is still lifting at `m = 59` with
    its source grown from 13 to 93 bits. So the datum the no-go calls
    load-bearing is cheaply available in the coordinate an occupation measure
    discards.
15. [`reports/RUN-014-HARD-ZETA-AU2A-LIFT-COUPLING.md`](./reports/RUN-014-HARD-ZETA-AU2A-LIFT-COUPLING.md) —
    Round A-U.2a's lift-occupation algebra, almost all of it exact and all of it
    holding: a lift digit turns out to **be** a binary block of the source, one
    such digit is amplified to `2t·3^m` at the endpoint, and the normalized
    correction is identical for *every* source in a cylinder. It ends in a second
    no-go — compact coordinates collapse every anchor to the same point. Measured:
    **the countermodel that defeated A-U.1 has positive lift flux**, so A-U.2a's
    own machinery already excludes it, and the class left open has no exhibited
    inhabitant. Also: why a mutation that makes a check *vacuous* is invisible to
    a drill.
16. [`reports/RUN-015-HARD-ZETA-AU2B-SPARSE-LIFT-RIGIDITY.md`](./reports/RUN-015-HARD-ZETA-AU2B-SPARSE-LIFT-RIGIDITY.md) —
    the first round of Phase II that **eliminates** rather than blocks. Its whole
    result turns on one constant being below another — `Λ_γ = 2.8395137304… < 3`,
    checked at 60 digits — and on two explicit inequalities that clear by
    `1.0e-4` and `6.0e-4`, each drilled by a perturbation smaller than its own
    margin. It also settles RUN-014's open question by a second route: the
    mechanical code has `d_m ≡ 0`, so the barrier excludes it directly.
    Measured: **the same proof scheme supports `0.0150`, not just the published
    `0.01`** — where the cheap gains stop, which is what the next round asks.
17. [`reports/RUN-016-HARD-ZETA-AU2B1-PACKING-THRESHOLD.md`](./reports/RUN-016-HARD-ZETA-AU2B1-PACKING-THRESHOLD.md) —
    the first round to ship a numerical artifact of its own, so it is checked as
    one: its 80-digit constants are **recomputed from scratch** by `decimal`
    bisection against the subject's `mpmath` root-finder, and agree to **80-83
    digits**. `c_pack = 0.03586` is **2.388×** the ceiling RUN-015 measured for
    the previous round's scheme — reached, as predicted, by a new argument
    (multi-occurrence packing) rather than by tuning. Both entropy identities
    hold, the variational supremum is the published constant, and §27's
    optimality is checked as two exhibited failures rather than an assertion.
18. [`reports/RUN-017-HARD-ZETA-AU2B2-QUEUE-ENTROPY.md`](./reports/RUN-017-HARD-ZETA-AU2B2-QUEUE-ENTROPY.md) —
    the first of the previous round's five levers is pulled, and **returns zero
    at first order**: queue legality does not change the entropy, and the gain
    comes instead from the Stirling prefactor, which was not on the list. Their
    queue DP is checked by **reimplementation** — opposite accumulation
    direction, exact integer credits, validated against brute force first — and
    all nine rows reproduce. Also a provenance finding: **the shipped JSON was
    not produced by the shipped script** (nine rows against eight, renamed
    fields), although every number in it is correct. A realization defect with
    the mathematics intact — the band this tree named a day earlier.
19. [`reports/RUN-018-HARD-ZETA-AU2B3-PREFACTOR-SATURATION.md`](./reports/RUN-018-HARD-ZETA-AU2B3-PREFACTOR-SATURATION.md) —
    **the subject corrected a defect this arm reproduced faithfully and did not
    notice.** The previous round's queue DP counted *pointed* paths where its own
    §4 defined an *unpointed* word set; RUN-017 verified the program against a
    brute force written from the program's reading, so both shared the
    misreading. Everything here is implemented from the **prose definitions**
    instead. Cost to RUN-017: the label, not the conclusion — the rate moves by
    `1.4e-4` at `r = 5000`. All nine diagnostic rows reproduce with worst
    deviation **exactly 0**, and the pointing ratio settles at 1.638, which is
    why the correction cannot move the exponential rate. The packing branch is
    declared closed.
20. [`reports/RUN-019-HARD-ZETA-AU2E-MULTISCALE-RETURN.md`](./reports/RUN-019-HARD-ZETA-AU2E-MULTISCALE-RETURN.md) —
    **every exact identity holds, and the round's two inequalities turn out to be
    the same line.** The Reset Affine Identity clears to a statement between
    integers and holds at 1,554 windows with no floating point. But the
    contamination bound says something only when `J_N < (N−2r)/r`, which *is* the
    packing theorem's floor — verified row by row with **0 disagreements** — and
    every computable spine sits far on the vacuous side: `J_N/N` runs 0.55–0.69
    against a floor of 0.08–1.50, so the barrier pins **3.1 %–6.7 %** of the
    mismatches present and cannot fail at these sizes. The reset geometry, by
    contrast, binds — `Y_b` reaches 0.203–0.938 of its cap across 190
    first-return windows — though its affine correction is never what makes the
    bound true.
21. [`reports/RUN-020-HARD-ZETA-AU2B3-PREFACTOR-SATURATION.md`](./reports/RUN-020-HARD-ZETA-AU2B3-PREFACTOR-SATURATION.md),
    [`RUN-021-CRYPTO-SEMIOTICS-V09.md`](./reports/RUN-021-CRYPTO-SEMIOTICS-V09.md) and
    [`RUN-022-HARD-ZETA-AU2E1-RESET-BLOCK.md`](./reports/RUN-022-HARD-ZETA-AU2E1-RESET-BLOCK.md)
    — source items 38–40. These three sat outside this index for three rounds
    while the index itself said "sixteen runs"; the count below is now emitted
    from the report files rather than typed, which is the only fix that does not
    go stale again.
22. [`reports/RUN-023-HARD-ZETA-AU2E2-FIRST-CROSSING-SURVIVAL.md`](./reports/RUN-023-HARD-ZETA-AU2E2-FIRST-CROSSING-SURVIVAL.md) —
    **the round holds, and its two headline inequalities are one inequality.**
    Substituting the closed form into the First-Crossing Reset Inequality cancels
    the `Y_a` terms identically, leaving the First-Crossing Correction Bound: the
    reset inequality says nothing about the starting height, and its slack is
    exactly `3·(L·3^(L−1) − B_L)` at every crossing. The Duration–Diophantine
    Dichotomy is likewise a **partition** on `D` against `1/(2L)` rather than a
    choice between escape routes — the cap forces the duration branch on one side
    and Legendre covers the other, so "satisfies neither" is impossible rather
    than unobserved. Everything conditional on a *surviving* crossing is checked
    as algebra, because a survivor would refute the Terras coefficient-stopping
    conjecture and there are **0 in 99,999 starts**. What is not vacuous: near
    misses land on the Stern–Brocot path to `log₂3` at **66.3 %** against a
    population base rate of **12.9 %**, with the furthest 1,000 at **0.0 %**.
23. [`reports/RUN-024-HARD-ZETA-AU2E3-INFINITE-SUPPORT.md`](./reports/RUN-024-HARD-ZETA-AU2E3-INFINITE-SUPPORT.md) —
    **the round's headline is a negative result and a correct one**, and its own
    corrigendum turns out to be measurable. A-U.2e.3 declines an available
    shortcut: `Σ_{n∈S} n^(−s) ≤ ζ(s)` for *any* `S`, so infinite obstruction
    support cannot be killed by cardinality — checked here by **constructing**
    infinite sets whose mass is below a target, in exact rationals. The new
    content is the conversion the corrigendum asks for and does not supply: the
    accelerated block endpoint sits at modified step `Q_L` while the true first
    crossing is at `⌊L·log₂3⌋+1`, and measured by **two routes sharing no code**
    the two coincide **49.84 %** of the time, mean gap `1.0032`, max `14`. So
    "do not conflate them" bites on half the population. Also: §8's suffix-minimum
    characterisation is **structurally untestable on any terminating orbit** —
    both characterisations degenerate to the final index, and their perfect
    agreement is a statement about two singletons, which this run nearly reported
    as a finding. Drill 12/12; three of its defects were re-aimed after misses,
    one of which hung the gate forever and left a live defect on disk, which is
    why `src42_drill.py` now has a subprocess timeout.
24. [`reports/RUN-025-HARD-ZETA-AU2E4-RENEWAL-RIGIDITY.md`](./reports/RUN-025-HARD-ZETA-AU2E4-RENEWAL-RIGIDITY.md) —
    **the arithmetic holds, and one inference does not follow from its own
    premise.** A-U.2e.4 is the most checkable round in a while: its determinant
    barrier, Farey lock, scale separation, CF tax and both recycling no-gos are
    statements about *any* pair of rationals bracketing `log₂3`, needing no orbit.
    All verified exactly on 272 real bracketing pairs. Both stated constants are
    **exact algebraic identities** — `ρ(2/5) = 2` is a rational, provable with no
    square root evaluated; `ρ(1/4) = 2+√3` exactly. **The finding:** §5's premise
    (a Farey-locked bracket's next denominator is at least `q₋+q₊`) holds at every
    step with 0 violations, but the conclusion drawn from it — Fibonacci growth,
    hence `O(log N)` record updates — **does not follow**, and `log₂3` is its own
    counterexample. Its continued fraction has a partial quotient of 23, and the
    convergent `1054/665` sits frozen for 23 consecutive steps while denominators
    walk in arithmetic progression with difference 665. Every one of those
    brackets is Farey-locked, so the hypothesis holds perfectly and the inference
    still fails: **33 of 45 steps** violate the Fibonacci recursion, while the
    convergents violate it 0 times. The claim is true for convergents; the
    Farey-lock condition admits semiconvergents. Drill 14/14 after five misses,
    four of the same class — *to test a check that never fires, break its subject,
    not its comparison.*
25. [`reports/RUN-026-HARD-ZETA-AU2D-SOURCE-FREEZE.md`](./reports/RUN-026-HARD-ZETA-AU2D-SOURCE-FREEZE.md) —
    **the round is a negative result about proof architecture and is right about
    it.** A-U.2d proves why transducer rationality alone cannot close CASP: once a
    positive source freezes its lift tail is `0^∞` for *every* positive source, so
    no source-only statistic distinguishes a convergent orbit from a CASP
    candidate. Everything checkable holds exactly, including §2's 2-adic
    shift-hereditary identity `𝓑(σ^s q) = Y_s` — **verified with a negative
    control**, 380 of which correctly failed. **Finding 1:** §15 concludes the
    source is frozen before a large B-atom crosses; asked of starts that exist the
    ordering is **reversed on 99.07 %** of them, because §15's hypothesis is the
    surviving-crossing one and RUN-023 found zero of those. The bi-exact regime is
    a true localisation pointing at a place nothing exhibitable is in when it
    matters. **Finding 2, about provenance:** all four cited arXiv references were
    fetched and checked; three are live and say what the notes say, and
    **arXiv:2605.13886 (Niu) is WITHDRAWN** as of 2026-05-20 while listed as a
    primary reference. Not load-bearing — both rounds explicitly decline to use it
    as a theorem — and the withdrawal points at a paper the notes already cite.
    Drill 12/12; a byte-restore control fired once and its cause was **not pinned
    down**, which the report says rather than explaining away.
26. [`reports/RUN-027-HARD-ZETA-AU2D1-ROTATION-CAP.md`](./reports/RUN-027-HARD-ZETA-AU2D1-ROTATION-CAP.md) —
    **the rotation cap holds, is attained, and is exactly rational.** A-U.2d.1
    sharpens the bound RUN-023 verified — `B/3^L ≤ L/3` becomes `≤ U_β(L)`, with
    the universal efficiency dropping from `0.3333` to `1/(6 ln 2) = 0.2404`.
    Verified termwise on **9,999** real first crossings with **0** violations, and
    **attained 7,137 times**. A methodological note that made this possible:
    `2^(−{βj}) = 2^(⌊βj⌋)/3^j`, so `U_β(L)` is a **rational number** and the whole
    inequality is exact — the shipped script computes it in `mpmath` at 80 digits
    and does not need to. **Three findings, all in the shipped artifacts and none
    in the mathematics:** the constants JSON over-publishes its own precision (the
    last 2–3 decimals of four `U` values are wrong, tracking `log₁₀L` exactly as
    fixed-precision summation costs); the JSON is **not what the shipped script
    produces** (renamed and dropped fields — the item-35 class, second occurrence);
    and the **withdrawn** Niu citation recurs for a second bundle. Drill 16/16
    after three passes; the most useful thing in the run is that a wrong
    Denjoy–Koksma variation constant would have **passed on this data**, so the
    constant is now asserted against its definition rather than against the data.
27. [`reports/RUN-028-HARD-ZETA-AU2D2-ATTAINABILITY.md`](./reports/RUN-028-HARD-ZETA-AU2D2-ATTAINABILITY.md) —
    **the saturation equivalence is an exact iff, and it holds both ways.**
    A-U.2d.2's one unconditional theorem — the rotation envelope is attained
    exactly when the proper-prefix code is completely mechanical
    (`B/3^L = U_β(L) ⟺ Q_j = ⌊βj⌋ ∀ j<L`) — verified on **9,999** real first
    crossings with **both off-diagonals empty and both diagonals inhabited**, so
    it is exercised in both directions rather than only where it is easy. The
    round's asymptotic `Θ(√L)` non-attainment gap also makes a falsifiable
    prediction about orbits that exist: **75** crossings have `G > 0` and **0** of
    them attain the envelope. Two failure modes were looked for and **not** found
    — the shipped script drops from 80-digit `mpmath` to plain `float`, and its
    `ceil(log2(y+N/3))` matches an exact integer route on all **15** rows with
    **13.4 orders of magnitude** of margin. **Three findings, none in the
    mathematics:** the JSON is again not what the shipped script produces (the
    item-35 class, third occurrence); the **withdrawn** Niu citation recurs for a
    third bundle, this time under a heading asserting the references were
    *rechecked*; and — in my own tooling — the guard certifying that these reports'
    figures are generated rather than typed **could not fail**, in three published
    runs. It is replaced, the replacement is shown failing on the real logs, and
    all four reports regenerate byte-identically. **A fourth finding, also mine:**
    the suite-wide defect total had been *refusing to compute* since item 22 —
    two drill logs renamed their tally keys, the aggregator did exactly what it
    was built to do and exited non-zero, and nobody read it, so **seven drills
    and 91 defects** sat outside the published figure for seven rounds (now
    **27 drills, 560/560**). Drill 12/12, with a new pre-flight that names a
    malformed mutation instead of blaming the check.
28. [`reports/RUN-029-HARD-ZETA-AU2D3-SURVIVAL-CLOSURE.md`](./reports/RUN-029-HARD-ZETA-AU2D3-SURVIVAL-CLOSURE.md) —
    **the most checkable round the sweep has met, and its one load-bearing
    citation names a different paper.** A-U.2d.3 takes exactly one external input,
    a Diophantine exponent `ρ★ = 4.1164` for `log2/log3`, and derives everything
    from it — and because `4.1164` is a terminating decimal, `θ★ = 2500/12791`
    and `σ★ = 12791/15291` are **exact rationals**, right to all **100** published
    digits. Two things this run could do that earlier ones could not. The round's
    two **second-order expansion coefficients** were tested by a probe that
    vanishes for the round's values (`1.7e-7`, `3.0e-8` at `10¹²`) and converges
    to a nonzero constant for values **1% away** — testing the expansion rather
    than confirming the symbols. And the continued fraction of `log₂3` was
    recomputed **with no logarithm evaluated anywhere**, every partial quotient
    decided by comparing `2^A` against `3^B`: **16 terms certified, to denominator
    10,781,274**, with the cutoff reported rather than crossed silently, and the
    integer comparisons counted so the independence is measured. **Three findings,
    none in the mathematics:** one digit of `η_β` is over-published, and the
    per-row `p − βq` is published to 100 significant digits where **83–100** are
    supported — the shortfall predicted by `log₁₀(β·q·q⁺)` to within **2.0**
    digits at every row; the Wu–Wang citation gives the title as *log₂ 3* when
    Crossref says *log 3* and reverses the authors, which matters because that is
    exactly the substitution that would make the citation self-justifying; and the
    **withdrawn** Niu paper recurs for a **fourth** bundle, beside the very paper
    its withdrawal notice defers to. The item-35 artifact class **does not** recur.
    Drill **20/20**, and its byte-exact restore control caught a real defect in my
    own harness after six quiet items.
29. [`reports/RUN-030-HARD-ZETA-HANDOFF-FIDELITY.md`](./reports/RUN-030-HARD-ZETA-HANDOFF-FIDELITY.md) —
    **132 documents reshipped 27 times without a byte of drift, and one lemma
    compressed into a stronger one than the round proves.** Item 48 is not a
    round: it is the handoff a *new conversation* is bootstrapped from, so it
    asserts what the other documents say rather than asserting mathematics, and
    an error in it is inherited by every round written afterwards. Checked for
    fidelity instead: every number must trace to a round document, every
    reshipped document must be byte-identical, every status disclaimer must
    survive the compression, and the **intermediate lemmas** must be the round's
    lemmas rather than stronger ones that imply the same conclusion. Three things
    could have gone wrong and did not — **132** distinct markdown documents, **27**
    of them shipped in more than one bundle and one shipped **8** times, each
    resolving to exactly **one** hash; **13** constants all traced (10 verbatim,
    3 as correct roundings); and all **6** required disclaimers intact. **Two
    findings.** The handoff states the occupancy lemma as `𝒪_L ≳ √L` where the
    round proves `(√(H²+2N) − H)/2 − 1`, which tends to `√L/√2` — so the
    handoff's own first two lines give `κ_rot = 1/12` while its third prints the
    round's `1/(12√2)`, contradicting each other by exactly **√2**; the
    conclusion was copied and the step that produced it was rounded off. And the
    **withdrawn** Niu paper appears a **fifth** time, now in the standing
    bibliography a new conversation is told to work from, with no note — in a
    list that annotates elsewhere. Drill **16/16**; six of its defects break a
    *locator* rather than a comparison, because a locator that finds nothing
    reports its subject as clean.
30. [`reports/RUN-031-CONSOLIDATED-ARCHIVE-INTEGRITY.md`](./reports/RUN-031-CONSOLIDATED-ARCHIVE-INTEGRITY.md) —
    **964 files open at nine nesting levels, nothing has drifted, and a checksum
    manifest certifies only the half that cannot change.** Item 49 is a third kind
    of object: a 17.5 MB consolidated archive of the source folder, which asserts
    no mathematics and makes no claim about other documents — it is a *container*,
    so the failure modes are drift, omission, content reachable only from inside,
    a nested structure that will not open, and an integrity claim aimed at the
    wrong half. **The archive is faithful:** of **50** entries, **47** have a
    standalone counterpart and every one is **byte-identical** to the item this
    sweep verified — checked against both the recorded hash and the file on disk
    — with **0** drifted, and all **964** files reachable through **49** nested
    archives open cleanly. **Three findings, none about the Collatz work.** Two
    entries ship their own `SHA256SUMS.txt`; all **16** listed hashes verify, and
    they list the **8** third-party PDFs — the files that by construction cannot
    change. Between two shipped versions of the same pack **3** files differ (two
    notes/scripts added, the README changed) and the manifest covers **none** of
    them, being **byte-identical across both versions**: an integrity claim that
    only ever certifies the immutable files is a checksum on the part nobody
    would doubt. A sibling pack nests its own predecessor **9 levels deep** with
    **no manifest at any level**. **50.0%** of the archive by volume is
    Riemann-zeta material existing nowhere else in the folder — reachable only by
    opening this item, and explicitly *not* verified here. And the archive omits
    one source item **33 seconds** older than itself: the bootstrap handoff of
    RUN-030. Drill **14/14**; six of its defects aim at the non-vacuity guards,
    because an archive check's defect branches are ones no real input reaches.
31. [`reports/RUN-032-HARD-ZETA-AU2D4-CONGESTION-RIGIDITY.md`](./reports/RUN-032-HARD-ZETA-AU2D4-CONGESTION-RIGIDITY.md) —
    **the first round in this line whose core holds on orbits that exist.** Every
    A-U.2d round so far proved something about *surviving* crossings, of which
    RUN-023 measured **0** below `2·10⁵`. Theorem 3.1 is different: `e(s) = min{u
    > s : δ_u < δ_s}` is an identity about the scalar sequence `δ_m = βm − K_m`,
    true of any orbit, and laminarity follows for the reason next-smaller
    intervals are laminar in any sequence at all. So the structural core was
    tested on four real Collatz orbits — **in exact integers, with no floating
    point anywhere**, since `δ_u < δ_s` is `3^(u−s) < 2^(K_u−K_s)`. Theorem 3.1:
    **0** violations over **394** intervals. Laminarity: **0** crossing pairs,
    with **2757** nested and **23429** disjoint so both branches are exercised.
    The annulus identity `A+D = D′+E` is not a small residual but the **pair
    (0,0)** in β-linear integers — **0** errors over **229** nested edges — and
    the strict-drop determinant `Δ = rg−ph = gE+hA` is exact on all **106** of
    them. All **8** of the shipped checker's smoke-test figures reproduce
    independently, field for field. **Three findings, none mathematical:** the
    bundle's own validation record reports `max_annulus_identity_error =
    2.3e-14`, because its checker evaluates in `float` an identity that is
    exactly integral — the **third** time in this line an exact quantity was
    reached for with higher precision instead (RUN-027, RUN-029, here), though
    the float route's margin is measured at **11.8 orders of magnitude** and was
    never at risk; `checker_stdout.txt` is **byte-identical** to the checker
    report it is described as differing from; and six of seven exponents drift
    1–6 ulps from their exact rationals, which is a note and not a defect. **What
    the bundle gets right is worth saying:** unlike item 49's manifest, its
    `SOURCE_VALIDATION` covers 8 of 9 files and the one it omits is itself, all 8
    verify, and its declared `input_state_sha256` **closes against RUN-030 and
    RUN-031**. Drill **18/18** — and a killed drill left a planted defect live on
    disk, so drills now keep a pristine sidecar and restore from it.
32. [`reports/RUN-033-HARD-ZETA-AU2D5-ANNULAR-RESIDUE.md`](./reports/RUN-033-HARD-ZETA-AU2D5-ANNULAR-RESIDUE.md) —
    **the exact-code separation holds in both directions, every B-source really is
    3 mod 4, and one section mixes an unconditional corollary with a cap that is
    vacuous on real orbits.** A-U.2d.5 adds two more results needing no
    hypothetical object. §4: for a code `w`, `2^Q z = 3^k x + B_w`, so one code
    selects one source class mod `2^(Q+1)` and one endpoint class mod `3^k`, and
    a repeated code forces `|x−x′| ≥ 2^(Q+1)` and `|z−z′| ≥ 2·3^k` — all pure
    integer arithmetic, **0** violations over **400** codes. Crucially it is
    checked in **both** directions: **1,200** members drawn from the claimed class
    *at which the code was never observed* each realize it, **0** failures —
    without that half the check would pass on a class ten times too large. §6:
    `L ≥ 2` forces `q_(s+1) = 1` hence `y ≡ 3 (mod 4)`, verified on **27,556**
    real sources with **0** violations. **Four findings, none mathematical.**
    §6's own depth cap `r < 1 + U_β(L)/4` rests on the source corridor, a
    B-survival property: **0 of 10,214** real chains satisfy it, so the cap is
    vacuous on orbits that exist — one section carrying a result testable on every
    orbit and one testable on none. The renewal identity and both determinants are
    the **pair (0,0)** in β-linear integers over **27,556** edges where the
    shipped checker reports `max_float_residual = 1.93e-12` — **fourth** round in
    this line reaching for precision where exactness was available. `checker_stdout.txt`
    is byte-identical to the checker report for the **second** bundle running, and
    two constants shared with item 50 **moved** between the bundles (item 51's are
    the exact doubles). And item 51's validation record is a **list** where item
    50's was a dict, so my reader saw **zero** files and only a non-vacuity guard
    surfaced it — RUN-028's finding landing on my own code. Drill **18/18**.
33. [`reports/RUN-034-HARD-ZETA-AU2D6-FAREY-ENTROPY.md`](./reports/RUN-034-HARD-ZETA-AU2D6-FAREY-ENTROPY.md) —
    **a closed-form count checked against brute-force enumeration, and the extra
    bit of section 6 is really there.** Most of this sweep compares one
    computation against another and has to argue the reference is better. §5 does
    not: `#W_{p,g} = binom(p−1,g−1)/g = binom(p,g)/p` is a closed form for a set
    that can simply be **enumerated**, so formula-versus-enumeration is decidable
    with no tolerance and no sampling. **34** coprime pairs with `p/g < β`, up to
    `(20,13)` with **3,876** members, **0** disagreements — and all **5** shipped
    capacity examples recompute, including the 129-digit one at `(485,306)`. §3's
    binary bridge `C(d(w)) = B_w`, its concatenation law, and the rational
    normalized correction are exact over **800** codes. §6 sharpens item 51's
    separation by **one bit**, `2^(p+1) → 2^(p+2)` and `2·3^g → 4·3^g`, using
    item 51's own `3 (mod 4)` result — checked in **both** directions, with
    **1,128** members drawn from the claimed class *where the code was never
    observed* each required to realize it and land on a `3 (mod 4)` destination,
    **0** failures; without that half the check passes on a class twice too
    large, which is exactly the size of the claim. The carryover was re-verified,
    not assumed: **12,419** real sources, **0** violations. **Two findings,
    neither mathematical:** `checker_stdout.txt` is the checker report plus a
    single trailing newline — third bundle shipping one content under two names,
    and the first where they are *not* byte-identical; and the inherited
    exponents are the **exact** nearest doubles, as item 51's were and item 50's
    were not. A published continued fraction that looked one term short turned
    out to be correct — the round defines `θ = β − 1`, and reading that stopped a
    finding against right arithmetic. Four of the checker's nine claims are
    independently confirmed and the other five are **named**, not implied. Drill
    **19/19 on the first pass** — the first in this sweep needing no re-aiming.
34. [`reports/RUN-035-HARD-ZETA-AU2D7-PLATEAU-RESET.md`](./reports/RUN-035-HARD-ZETA-AU2D7-PLATEAU-RESET.md) —
    **the crossing slope moves by whole numbers, the caps above it rest on a
    premise almost no real chain meets, and the round's new machine-readable
    ledger under-reports its own paper.** Section 3 is the cleanest decidable
    core this sweep has been handed: `xi_i = Q_i/L_i - beta`, and in the
    difference `xi_{i+1} - xi_i = J_i/(L_i L_{i+1})` the `beta` cancels, so the
    jump law, the quantization, the plateau form `J_i = Pi_i >= 1`, the
    strict-drop form, and the characterization of a genuine reset as exactly
    `J_i < 0` are all settled in integers with no logarithm anywhere. Verified
    over six figures of renewal edges from real orbits, together with Theorem
    4.4, Lemma 5.1 and all of section 11, with **zero** disagreements. Sections
    4.3 to 9 are a different kind of claim: each descends from B-survival
    inputs, and **one** chain in tens of thousands meets all three, so this run
    measures the premises and checks the **derivations** on a grid rather than
    imposing caps on orbits that never agreed to them — the mistake RUN-032 made
    on 10,214 chains. A drill defect deletes that premise filter and the gate
    goes red, which is what proves the filter is load-bearing rather than merely
    exclusive. Section 9's literal hypothesis is common on real chains and its
    conclusions fail there; the companion survival bound it also needs is
    declared a section earlier, and this run names that instead of reporting a
    counterexample. **Three findings, none mathematical:** the new theorem
    ledger renders the paper's own section 22 lossily — 19 numbered results
    become 16, seven `NO-GO` headings become six, with `NO-GO 18.2` identified
    as the gap by reading and by keyword test independently — and it disagrees
    with the constants frontier on the round's `status`; the frontier's
    `1/(3 ln2)` is one ulp off while the **paper's** printed value is the
    correctly rounded double, so the two artifacts disagree at the last bit; and
    the source-validation record has changed schema for the third time in four
    bundles. Every bracket is certified in the file that uses it — `ln 2` from
    its series with an exact tail bound, `log_2 3` from a bit length — after a
    hard-coded "lower bound" for `beta` turned out to sit above it. The drill's
    first pass returned **26/27**, and the miss was a hole in this gate, not an
    escaped defect: derivation failures were collected by matching key-name
    suffixes, and one counter's name matched none of them, so it could increment
    unread. Enumerating the counters fixed the instance; making the gate refuse
    an integer in that block it was never told about fixes the class. Drill
    **27/27** after that. Running the tree's standing guards then turned up an
    older one: `audit_drill_anchors.py` knew only the `src07`–`src21` defect-list
    shape, so it had been reading **zero anchors for 16 of 31 drills** — the
    whole current sweep — while reporting `ok`. It now discovers shapes, names
    the 103 defects that are not string replacements, and refuses on an
    unexplained zero; coverage went from **277** anchors to **502**, none of the
    225 newly visible ones stale.
35. [`data/results.v1.json`](./data/results.v1.json) — machine-readable claims,
   bounds, gate outcomes, and source digests. Generated from the archived gate
   logs by `code/build_results.py`, never typed by hand.
36. [`code/`](./code/) — the engine, the independent reference, and the gates.
37. [`data/gate-logs/`](./data/gate-logs/) and
   [`data/raw-logs/`](./data/raw-logs/) — the evidence the above is built from.

How to cite this tree, and its CTCL timestamp, are in
[`CITATION.md`](./CITATION.md). States are timestamped by appended CTCL instants — most recently
[`06f0de0a`](https://commoninstant.org/i/06f0de0a-a6ed-4383-9dfa-5447e30ed099) —
each Ed25519-signed, with the git commit carried in the instant's own metadata — so the timestamp is checkable against the repository rather than
asserted beside it. It timestamps *when this state existed*; it does not review
whether any of it is correct.

Held separately: [`reports/LEAN-QUEUE.md`](./reports/LEAN-QUEUE.md) — the claims
this arm structurally cannot settle, because they are `forall`-quantified over
infinite or non-integer domains rather than finite. Collected, scoped and ordered,
and deliberately **not started**: a mathlib-backed development is heavy on CPU and
disk, and that hardware comes later.

This tree is portable across drives. Nothing hardcodes an absolute path, the one
path input defaults to the tree's own location, and every archived log is
relative — so moving it does not require re-running anything.

The subject series itself is archived separately as its own tree at
[`../collatz-ot-series-neok/`](../collatz-ot-series-neok/), under Neo.K's
authorship. Its presence beside this one is not agreement between the two.

## Keeping the drills aimed

A mutation drill plants its defects by exact string replacement, so a refactor of
the code under test can **unaim** it without anything going red — the anchors
simply stop matching, and the drill says so only when next run. That happened
here: one performance change to `floor_beta` broke eight anchors across six
drills in a single edit.

[`code/audit_drill_anchors.py`](./code/audit_drill_anchors.py) is the standing
guard. It requires every anchor to match its source **exactly once** and every
target check name to still exist — currently 277 anchors across 17 drills. It is
itself drilled: a whitespace-only edit to one anchored line turns it red. Run it
after any change to a shared module, including changes that provably preserve
behaviour.

## Counting the suite

How many defects the suite has planted and caught is **not typed into this file.**
[`code/suite_totals.py`](./code/suite_totals.py) reads the archived gate logs and
emits it to
[`data/gate-logs/suite-totals.json`](./data/gate-logs/suite-totals.json):

```bash
python code/suite_totals.py
```

Its only real failure mode is silent undercounting — drill logs have used four
different key shapes, and a reader that knows one returns zero for the others
while the total still looks plausible. The first version did exactly that,
reporting 383 where the logs held 461. So it classifies every log explicitly and
refuses anything it cannot interpret, including a zero-byte file, rather than
counting it as nothing. [`code/suite_totals_drill.py`](./code/suite_totals_drill.py)
plants that failure and seven others in the **logs** and requires each to turn the
totalling red.

**The refusal worked and went unread.** `src22` renamed one tally key and `src41`
renamed both, after which this script exited non-zero on every run while the
archived summary still said `drills: 20 … ok: true`. Seven drills and 91 defects
sat outside the published figure for seven rounds, until RUN-028 went looking.
The shapes are now enumerated with the run that introduced each, every row
reports which shape it used so the next rename is visible in the output rather
than only in an exit code, and the drill removes the newest shape again to prove
that branch is load-bearing.

## How the evidence is arranged

The engine verifies intervals; a statement about `[3, N]` exists only once
`code/verify_run_logs.py` confirms the archived chunk logs tile `[3, N]` with no
gap and no overlap, every chunk exited clean, and each chunk's count of odd
starts matches what its interval actually contains. That aggregator reads only
the logs — it never re-runs the engine, so it cannot launder a missing chunk
into a covered one. It has been shown refusing a deleted chunk and a tampered
count (`data/gate-logs/coverage-refusal-drill.json`).

Four gates guard the engine itself, chosen to be of different kinds because
gates of the same kind fail together: the engine's internal self-test, an
independent arbitrary-precision Python implementation, exact two-sided
agreement with archived OEIS record sequences computed by other people, and a
mutation drill that plants defects to confirm the other three can still fail.

## Reproduce

Observed environment: Windows 10 x64, 16 logical CPUs, rustc 1.96.0
(ac68faa20 2026-05-25), Python 3.14.5. No third-party crates, no Python
packages — `code/requirements.txt` is empty on purpose.

```bash
rustc -O --edition 2021 code/collatz_verify.rs -o build/collatz_verify.exe
./build/collatz_verify.exe --self-test
python code/reference_crosscheck.py 3 300000
python code/anchors.py 100000000
python code/mutation_drill.py
```

The four commands above are the compact replay and take a few minutes, apart
from the mutation drill, which rebuilds the engine twelve times. The full
`[3, 2^40]` verification is deliberately not part of the compact replay because
it takes about 16 minutes of wall clock on 16 threads:

```bash
bash code/run_verification.sh 1099511627776 16 20 16 t40
python code/verify_run_logs.py --tag t40 --expect-to 1099511627776
```

## Next

This arm is available to the theory side. Claim types it can take are listed in
`reports/CHARTER.md` (V1 bounded convergence, V2 bounded cycle exclusion, V3
single trajectory, V4 candidate adjudication, V5 extremal statistics). Handing
it a specific claim to check is more useful than raising `N`.
