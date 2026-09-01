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

Across <!-- COUNTS -->68 source items and 47 runs<!-- /COUNTS -->, **nothing in the source
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
35. [`reports/RUN-036-HARD-ZETA-AU2D8-LOW-SOURCE-SATURATION.md`](./reports/RUN-036-HARD-ZETA-AU2D8-LOW-SOURCE-SATURATION.md) —
    **a Gamma identity that needs no Gamma, a depth cap no real orbit can be
    tested against, and two rational constants published as their float64
    evaluations.** This round trades the additive slack machinery for a
    multiplicative one and the exchange is a good one: section 3's
    `z/y = (3^L/2^Q)·prod(1+1/(3Y_j))`, section 4's consecutive-odd envelope and
    section 5's Gamma representation are all statements about **rationals**, and
    all hold exactly on every segment swept. The Gamma identity especially: for
    integer `L` the quotient
    `Gamma(L+y/2+1/6)Gamma(y/2)/(Gamma(y/2+1/6)Gamma(L+y/2))` **is** the
    Pochhammer product `prod (y/2+k+1/6)/(y/2+k)`, which is the envelope's own
    definition — so where the shipped checker reports a worst error of
    `3.1e-10`, this run's error is **zero**, with no Gamma function evaluated
    anywhere. Section 4's premise is met by every segment tested; section 9.1's
    is met by **none**, because it needs `z_1 > y_r` and a first-crossing
    endpoint is precisely where the slack drops. So 9.1 was measured, not
    imposed — and since "0 violations of 0 subjects" is exactly what a vacuous
    filter produces, a drill defect deletes the premise gate and the run must go
    red. What *is* universal was checked on every chain: 9.1's two forms are one
    inequality. **Three findings.** `theta_star = 2500/12791` and
    `mu_star = 2209/63955` are exactly rational, and the published values are
    bit-for-bit what `1/(4.1164+1)` and `(6*theta-1)/5` give in float64 — 1 and
    2 ulps out, the second inheriting the first, while every genuinely
    transcendental constant is the exact nearest double. The theorem ledger
    under-reports the paper's own section 21 in three places of five, and the
    missing external input — identified by reading and by a distinctive-word
    test independently — is the irrationality-measure consequence for `log_2 3`
    through `rho_star`, the constant both new exponents come from. And, as an
    **improvement**: the new `CHECKSUMS.sha256` and the validation record agree
    on every digest, cover everything but one file, and that file is
    `CHECKSUMS.sha256` itself with the scope note saying so — the direct answer
    to what RUN-033 found at item 51. Section 15's floors recompute from
    **A-U.2d.7's Theorem 7.1**, verified in RUN-035, to within two ulps; the
    inversion is already sharper from depth 8, and the paper's `r >= 9` label
    belongs to that round's Corollary 7.2 rather than its Theorem 7.1. Three of
    this gate's own errors were caught before publication — a false 75 ulps from
    rendering a bracket to too few decimal places, a false 12 from measuring
    relative error under heavy cancellation, and a false 7,091 from applying 9.1
    without its premise. The drill's first pass exposed a **vacuous check** and
    an untested instrument; both are fixed, and the brackets now have an
    eight-part self-check of their own. Drill **25/25**.
36. [`reports/RUN-037-HARD-ZETA-AU2D9-ORBIT-PACKING-DEFICIT.md`](./reports/RUN-037-HARD-ZETA-AU2D9-ORBIT-PACKING-DEFICIT.md) —
    **one line of arithmetic closes the previous round's open problem, and for
    once the round's headline theorem has a premise real orbits actually meet.**
    A-U.2d.8 listed as open that a genuine orbit ought to beat the
    consecutive-odd packing envelope, with no quantitative theorem. The answer
    needs no machinery: `3n+1 = 1 (mod 3)`, so no accelerated image is ever
    divisible by three, the states pack into the integers coprime to 6 at mean
    spacing 3 rather than 2, and the local exponent moves `1/6 -> 1/9` with the
    ratio decaying like `L^(-1/18)`. Two residue refinements fall out of the same
    congruence — every post-entry state in `{1,5} mod 6`, every post-entry
    B-anchor in `{7,11} mod 12` — and all of it is decidable in integers. Zero
    disagreements across the sieve, the residue sets, the admissible positions,
    the envelope, and the two-progression Gamma form, which — as at RUN-036 — is
    a Pochhammer quotient at integer parameters, so this run's error is **zero**
    where the checker reports `2.0e-13`. **Section 11 is why this round is worth
    more than the last two.** Theorem 11.2 assumes first-crossing subcriticality,
    `sum q_j < beta m` — not a survival hypothesis but the defining property of a
    first-crossing interval, decidable as `2^Q < 3^m` — so unlike A-U.2d.8's
    section 9.1 it was tested on **every** prefix, and holds. Its `17/24` was
    enumerated rather than accepted: `q(n)=k` selects one class mod `2^(k+1)`,
    and among `W` consecutive integers the odd **3-free** ones in that class
    number at most `W/(3*2^k)+1`, which is where the `3` sieve enters; without it
    the same sum gives `17/16`. Lemma 7.1 needs `z_1 > y_r` and gets the
    A-U.2d.8 treatment — its combinatorial core enumerated over **499,149**
    residue sets with zero failures, its orbit half premise-gated. **Two
    findings.** A rounding chain with four links: `C_6` is exact, but
    `C_9 = C_6/6` is 1 ulp out, `c_9 = C_9^(-9/8)` another, and
    `mu9 = (9 theta-1)/8 = 9709/102328` is 3 — and every link reproduces exactly
    by redoing the arithmetic in float64 on the already-rounded parent. And one
    constant, `24(4-beta)/17`, is published with **two different values** in one
    bundle: the checker report and the paper both have the correctly rounded
    double, the constants frontier is 1 ulp off. The validation record has
    changed shape for the fifth time in six bundles — three purpose-named blocks
    with no `files` key — and one of those blocks carries a digest with no
    filename at all. Two of this gate's own errors were caught first: a false
    11,775 from applying a `mod 12` refinement to sources with `L = 1`, which its
    inherited result excludes, and three constants left undecided by a `beta`
    bracket `1e-6` wide where a double needs far tighter. Drill **31/31**.
37. [`reports/RUN-038-HARD-ZETA-AU2D10-VALUATION-HARMONIC-DEFICIT.md`](./reports/RUN-038-HARD-ZETA-AU2D10-VALUATION-HARMONIC-DEFICIT.md) —
    **the bridge the previous round refused to build, a countermodel that checks
    out against its own closed forms, and a ledger that is finer than its
    paper.** A-U.2d.9 declined to turn its diameter gain into a harmonic one and
    named the missing piece: a value-order bridge. It turns out to be the edge
    equation itself — `1/Y_j - 1/Y_{j+1} = (3-2^q)/(3Y_j) + 1/(3Y_jY_{j+1})` —
    which telescopes to `sum (2^q-3)/Y_j = -3/y + 3/z + C_cross` and couples each
    edge's valuation to the reciprocal weight of its source. The product exponent
    moves `1/9 -> 4/45` with a polynomial deficit `1/45`. Everything decidable
    holds: the identity on **70,810** edges, the telescope and both harmonic
    capacities on **68,311** segments, the mod-9 target-cost law on every edge
    with its table **rederived** from `2^q m = 4 or 7 (mod 9)` rather than
    trusted, and Theorem 15.1's span bound on all **27,345** prefixes meeting its
    premise — which, as at A-U.2d.9, is what a first-crossing interval already
    is. Three kinds of premise appear and the gate keeps them apart: the
    unconditional ones, the two that no real segment meets (Theorem 4.1 needs
    `z > y`; Lemma 5.1 needs every state including the endpoint above the
    source), and the one real orbits do meet. Where a theorem is untestable its
    *equivalence* to its premise is still checked, and Theorem 4.1's holds on all
    68,311. **The round bounds itself with a countermodel**, and that is checked
    as carefully as its claims: eliminating `t` between the construction's two
    closed forms leaves a relation between the round's own reported numbers,
    `avg_q -> 6|S_X|/X`, satisfied with a gap that shrinks `2.0e-3 -> 7.2e-4 ->
    1.8e-4` across three sizes, exactly as the `+o(X)` predicts. **Two
    observations.** The rounding chain recurs for a third round, now with the
    root drifting too — `C_10` +1 ulp, `C_10/6` +2, `c_10` -1, `mu10` +1 — every
    link reproducing in float64 from the already-rounded parent; but A-U.2d.9's
    span coefficient is quoted forward *correctly*, so that round's frontier
    error did not propagate. And for the first time the JSON ledger is **finer**
    than the paper rather than lossier: 18 entries to section 22.1's 17, because
    it splits one prose item into the two halves that item itself names, with no
    entry lacking a counterpart. Three of this gate's own errors were caught
    first — a false 352 from applying Lemma 5.1 without its premise, a comparison
    between two envelopes neither of which bounds the other, and a bracket too
    loose to identify what it judged. A fourth was speed, and the fix mattered:
    memoising a per-segment log series took the run from 88s to 26s at a
    **larger** limit, so the population guards were met rather than lowered.
    Drill **35/35**.
38. [`reports/RUN-039-HARD-ZETA-AU2D11-MULTISTEP-TRANSPORT.md`](./reports/RUN-039-HARD-ZETA-AU2D11-MULTISTEP-TRANSPORT.md) —
    **an exact rational certificate: the first headline number in this sweep
    that could be checked with no reference of my own.** Every previous round
    handed over a bound or a constant, and checking it meant computing a
    reference and then arguing mine was the better one — an argument always
    available to be wrong. This round's exponent `1373/25856` is instead the
    value of a **dual certificate**: a positive potential `a_r` on the units mod
    `3^h` and non-negative multipliers satisfying
    `-3a_r + 2^k a_T(r,k) + mu_(r,k) >= 1` for every `r` and every `k`, with the
    exponent read off by `alpha_h = (1/3) sum mu/(3^h 2^(k+1))`. Both halves are
    finite and rational, so there is nothing to calibrate. All three levels
    verify: **294** inequalities, **zero** violations, every potential positive,
    every multiplier non-negative, every transition landing back inside the unit
    group, and every `alpha` exactly the published rational. The tail is
    computed rather than accepted — past `K` with `2^K a_min - 3 a_max >= 1` the
    inequality holds from the transport term alone, and `K` comes out **4, 5, 7**
    for the three levels, exactly the `tail_k` each certificate declares.
    `eta11 = 4/45 - 1373/25856 = 41639/1163520` recomputes exactly. Section 3's
    transport identity holds on every unit residue of every segment; section 4's
    channel is one class mod `3^h 2^(k+1)` by CRT, enumerated. **Two findings,
    both about the machine-readable record.** The ledger has **no list of open
    problems at all** — its section is headed "Diagnostic / explicitly open" and
    the JSON key is `diagnostic_only`, holding the three diagnostics while the
    four genuinely open items, the Collatz conjecture among them, go unrecorded;
    the previous two rounds each carried an `open` list of six. And the bundle
    ships `build_AU2d11_artifacts.py`, the script that generated every other
    artifact and the largest file in the bundle — which `CHECKSUMS` does not
    list and the validation record covers with no digest at all, so the one file
    nothing pins is the tool the provenance chain hangs on. Against three rounds
    of over-published last digits, `C_11` is printed to **twenty** correct
    digits. One of this gate's own errors is worth recording: computing
    `x^(1373/25856)` by integer power and bisected root took **eight minutes**
    and could not reach a population meeting its own guards — and the available
    wrong fix was to lower the guard. The right one was `exp((p/q) ln x)`, which
    took it to twenty seconds. Drill **33/33**.
39. [`reports/RUN-040-HARD-ZETA-AU2D12-TRANSPORT-HIERARCHY.md`](./reports/RUN-040-HARD-ZETA-AU2D12-TRANSPORT-HIERARCHY.md) —
    **a hierarchy that reaches exponent zero, and constants that outrun it.**
    A-U.2d.11 asked whether its own finite-state exponents tend to zero; this
    round says three separate times that it does **not** answer that, and
    instead builds a different hierarchy from what the LP relaxation discards —
    that one trajectory must realise every overlapping exponent block at once.
    Almost all of it needs no logarithm: `floor(beta m)` is `(3**m).bit_length()
    - 1`, and `C_m^- = sum binom(Q-1,m-1)/(3 2^Q)`, `gamma_m = 2^(q_m+1)/3^m -
    1`, `alpha^_m = (1/3)(1+1/gamma_m)C_m^-` are exact rationals. All six
    published levels reproduce exactly, and so does the entire **150-level
    record set**, on every field — including the paper's own caution that the
    sequence is not monotone (`alpha^` rises at **93** of 150 levels). Lemma
    10.1 was re-derived by an exact convolution of the geometric law that never
    mentions the closed form (**zero** violations), and the closed form checked
    separately against brute-force composition counts. Both halves of the
    closure hold: Chernoff over 150 levels, tightest at `m = 2` where the truth
    is **0.558** of the bound, and the Diophantine floor `gamma_m >= (ln2)
    ||beta m||` over 400. Section 15 turns out to **derive** the source-floor
    formula `mu = (theta* - alpha)/(1 - alpha)` that RUN-039 could only fit, so
    the four inherited exponents and the six new ones are all checked against a
    quoted step. **Four findings, none a mathematical error.** Section 1 states
    the premise as every state *before* the endpoint being at least `y`, while
    section 4's sums run to `L` inclusive — under section 1's reading Theorem
    4.1 fails **221 of 999** times, under section 4's, none. The premise
    sections 7-8 need, `L >= y`, is met by **one** source in 66,665 (`y = 31`);
    mean excursion length is 6.3. The exponents fall but the explicit constants
    rise faster: `B_12 ~ 2.9e4`, `B_48 ~ 3.0e20`, so even giving A-U.2d.11 a
    constant of zero the `m = 12` certificate only overtakes it past
    `L/y ~ 10^334677` — their own report renders that ratio as `0.0`, a float64
    underflow, where the real slack is about **4227 powers of ten**. And
    `theta* = 1/(rho*+1)` is the exact rational `2500/12791`, but the shipped
    double is what `1/(1+float(4.1164))` evaluates to, one ulp higher, a single
    rounding inherited by all six source-floor exponents at **0 ulps** against
    the float64 chain. RUN-039's builder finding is **fixed** — the builder is
    in `CHECKSUMS` this time; its ledger finding is not, two rounds running.
    Drill **35/35**.
40. [`reports/RUN-041-HARD-ZETA-AU2D13-SOURCE-DEPTH-COLLISION.md`](./reports/RUN-041-HARD-ZETA-AU2D13-SOURCE-DEPTH-COLLISION.md) —
    **a collision assembled from five finite links, and a constants family with
    one parameter.** The first round in this stretch to prove a branch of the
    survivor space EMPTY rather than lower an exponent: positive-linear
    completed B-density is impossible, unconditionally, and section 14 says
    plainly that this still does not close CASP. The mechanism is a chain —
    support count → source height → duration floor → localized depth and span →
    large slack → source-corridor contradiction — and every arrow is finite, so
    each was checked on its own: the mod-12 source floor, two duration floors,
    the pigeonhole localization, Jensen and AM-HM on the origin gaps, and the
    corridor. **The one genuinely arithmetic input**, the local
    best-approximation bound `||q beta|| > 1/((M_beta(N)+2) q)`, was decided
    from the integer-comparison continued fraction of `log2 3` over **111,000**
    values of `q`: **zero** violations, and not slack — its tightest margin is
    **4.7%**, at the convergent denominator `q = 665`. Two things worth
    carrying forward. The constants family collapses to one rational parameter,
    with **`sigma* = 1/(1+theta*)`** and **`kappa13 = 1/(1+theta*^2)`** —
    closed forms the bundle never states, exact as `12791/15291` and
    `163609681/169859681`, which turns both headline exponents from numbers one
    approximates into numbers one decides. And `chi*` sits **27 ulps** from its
    exact value, not an error but a three-link rounding chain ending in a
    **22.9-fold** cancellation in `5 sigma - 4`; the gate's allowed budget for
    it is now derived from that factor rather than chosen. **The object of the
    round does not occur on a real orbit**: zero B-injections in **460,024**
    first-crossing intervals, closest ratio `z/y = 0.9761`, so the two
    conditional theorems are checked as algebra and their antecedent-free
    "zero violations" is never reported as coverage. Twelve of twenty-three
    printed decimals over-publish against the exact rationals, all twenty-three
    with an ellipsis. **RUN-039's ledger finding, still open at RUN-040, is
    fixed** — the `open` key is back with all four items, the Collatz
    conjecture among them; NO-GO 12.5 is the one heading still missing, and the
    validation record is digest-free for a third round. One of this gate's own
    errors is worth recording: RUN-040's fail-open lesson was written down and
    then rewritten into the code one round later with the clauses in the wrong
    order. Drill **33/33**.
41. [`reports/RUN-042-HARD-ZETA-AU2D14-SPARSE-SUPPORT.md`](./reports/RUN-042-HARD-ZETA-AU2D14-SPARSE-SUPPORT.md) —
    **the round whose central theorem a real orbit can actually be asked
    about.** A-U.2d.13 made completed B-support sparse; the obvious escape is
    to hide renewals in intervals that started but never finished, or in the
    complementary A family, and this round closes both — `B_st(N)=M_N+U_N`
    with the active backlog bounded twice, and `A_N <<_eps 2^(E_A(N)) N^eps`
    so a sublogarithmic envelope cannot carry polynomial A support. With
    envelope, slack and continued-fraction scales all subpolynomial the WHOLE
    renewal process obeys `R_N <= N^(4/5+o(1))`, and anything above `4/5` pays
    one of three named prices. **The change that matters for verification**:
    section 3 is about EVERY suffix minimum, not only B sources. RUN-041 could
    find zero B-injections in 460,024 intervals; this run finds **16,251**
    suffix minima and confirms Theorem 3.1 (`q=1`) and Corollary 3.2
    (`7, 11 mod 12`) on every one, zero violations — along with the `q=1` iff
    `y=3 mod 4` equivalence they rest on and the `6j-1` ordinal floor. The
    A-envelope side is equally testable: **1,885** orbits, `E_A = beta*T - Q`
    everywhere, and the exact product identity `z_A 2^Q = y_A 3^T
    prod(1+1/(3Y_j))` — written with no `beta` in it — holding on every
    segment. It also **retro-explains RUN-041's zero**: all 16,251 minima are
    A-renewals, and a true suffix minimum with a first crossing would be a
    B-injection by definition, since `Y_e(s) >= Y_s` by minimality and strict
    by injectivity. One measurement detail worth keeping: a whole convergent
    orbit has NO suffix minima at all, because it ends at 1; the population
    exists only on a finite window. **Two findings.** `psi(sigma*)` and
    `1-sigma*` are the same number, `2500/15291` exactly, and the frontier
    stores both one ulp apart, adjacent, under `at_old_sigma` — one quantity
    with two values in the same object, each reproducing its own float64
    route. And **the three-round finding is fixed**: the source-validation
    record now carries sha256 digests of its own, and recomputing all six
    gives zero mismatches. Drill **33/33** — its first pass again found two
    defects that LOOSENED what they attacked and one that made the gate raise
    instead of report, plus a threshold check whose sample never straddled its
    own threshold.
42. [`reports/RUN-043-HARD-ZETA-AU2D15-RECORD-SPARSITY.md`](./reports/RUN-043-HARD-ZETA-AU2D15-RECORD-SPARSITY.md) —
    **an inequality that needs no premise, and a checker report that publishes
    both its honest zeros and their vacuous twins.** A-U.2d.14 ended on a real
    obstruction — divergence alone permits suffix-minimum times as sparse as
    `N^o(1)`, so record theory gives no polynomial lower bound. This round
    supplies the Collatz-specific replacement, enclosing the record count
    between two slack coordinates, `2^(-Delta_N) N^(1-o(1)) <= R_N <=
    2^(delta_N) N^o(1)`, hence **`Delta_N + delta_N >= (1-o(1)) log2 N`**; and
    it collapses one of the previous round's three escapes, since every
    A-renewal is a suffix minimum and so `E_A(N) <= delta_N + o(log N)`.
    **The piece testable hardest needs no premise at all**: section 10's
    `N1(s,g) >= (2-beta)g + (delta_{s+g}-delta_s)` rests only on every non-one
    valuation being at least two and on the definition of `delta`, so it holds
    on every segment — **127,813** pairs rooted at suffix minima plus
    **59,130** rooted anywhere as a control, zero violations, and a tightest
    slack of exactly **0.0**, so the bound is attained and adding 1 to it turns
    the gate red. The record process is equally clean: **8,447** edges, exact
    multiplier with no `beta` in it, product concatenation, Lemma 11.1's
    `3g-7` span, the `U_6` capacity, the state-ceiling identity. **Three
    findings.** Their checker report carries the honest zeros
    `record_slack_drop_edge: 0` and `record_descent_implies_crossing: 0` —
    and section 18 says the same in prose, which is the right way to publish an
    empty population — but beside them sit `record_total_down_variation:
    23,018` and `record_tail_drop: 35,616`, which their own zero makes
    evaluations of `0 < log2 P`. The source-validation record has **lost the
    per-file digests it gained one round ago**, keeping a `checker_stdout_sha256`
    instead — provenance of the output, not the inputs. And `2-beta` is 2 ulps
    from its true value, 0 from `2.0 - published_beta`. **The drill found two
    genuine misses in this gate**, the first in several rounds: the record-slack
    classification had no failure counter at all, so inverting it flipped all
    8,447 edges silently; and the ledger-coverage lists were read by nothing, so
    a heuristic that accuses everything went unnoticed — while the honest
    version had already false-positived on "CASP and the Collatz conjecture",
    which the ledger abbreviates. Both fixed with invariants and two-sided
    controls, and the corrected heuristic re-verified against RUN-041's genuine
    absence. Drill **30/30**.
43. [`reports/RUN-044-HARD-ZETA-AU2D16-RECORD-GAP-TRANSPORT.md`](./reports/RUN-044-HARD-ZETA-AU2D16-RECORD-GAP-TRANSPORT.md) —
    **the round where the central coordinate turns out to be an integer
    identity.** A-U.2d.15 proved record sparsity must be paid for in slack;
    this round identifies the local object carrying the payment — a
    consecutive suffix-minimum gap — and shows it is nothing like an arbitrary
    segment: bounded record ratio `1 < z/y < (3y+1)/(2y)`, endpoint below every
    interior state, a fully suffix-supercritical tail, a two-sided slack spike,
    bidirectional valuation transport, and an exact landing phase. **The
    verification hinges on a coordinate change the paper does not spell out.**
    Section 5 rests on the correction bank `A_n = 2^(-delta_n) Y_n`, which
    needs `beta`; but `2^(beta n) = 3^n` exactly, so `A_n = 2^K_n Y_n / 3^n`
    and its monotonicity is the **integer** identity `2^K_{n+1} Y_{n+1} - 3 *
    2^K_n Y_n = 2^K_n`. Checked on **123,005** steps, zero violations, with no
    logarithm deciding anything — and Theorem 5.1 is proved THROUGH that
    coordinate, so it was the one place a bracket could have hidden an error.
    After three rounds of empty populations, this round's object is everywhere:
    **4,069** gaps and **11,305** tail suffixes, every claim clean, with
    Theorem 8.1's ascent bound **attained** (tightest slack exactly 0). The
    landing phases hold exactly on **3,057** `7 mod 12` and **1,012**
    `11 mod 12` endpoints, and **both bridges the paper ships in NO-GO 13.7
    rebuild from the map** — values, words, geometry, suffix-supercriticality,
    phases. **Three findings, all about the bundle.** `checker_stdout.txt` is
    **byte-identical** to the checker report beside it. The validation record
    names four files and digests none — its content has now varied across four
    consecutive rounds (absent, present, a stdout digest, neither), though
    `CHECKSUMS` still pins 10 of 11 files. And `3-beta` is published exact
    while `2-beta` is 2 ulps out: the same subtraction, magnitude loss 2.1x
    versus 4.8x. The drill found two real holes in this gate — an ascent check
    written as a two-level guard whose outer test sits exactly at equality and
    so never opened, and a transport section where nothing depended on WHICH
    interior point was the peak — plus one defect that was inert for genuine
    mathematics: `2 = -1 mod 3` has order two, so `2^-q` and `2^q` are the same
    residue. Drill **37/37**.
44. [`reports/RUN-045-HARD-ZETA-AU2D17-SMALL-ENDPOINT-CYLINDER.md`](./reports/RUN-045-HARD-ZETA-AU2D17-SMALL-ENDPOINT-CYLINDER.md) —
    **the round whose central identity turns out to be a definition, and whose
    content sits one line below it.** A-U.2d.17 puts the exact two-sided code
    cylinders on the bridge A-U.2d.16 produced. Its headline is the Exact
    Endpoint-Laplace Identity `sum_i 2^-H_i = 3(Z - 2^-E X)`; multiply by
    `2^Q` and it reads `sum_i 3^(h-i) 2^P_i = 3 B_w`, which is term by term
    the definition of `B_w` in section 3. The identity is true by
    construction. **The falsifiable content is the affine relation
    `2^Q Z = 3^h X + B_w` on real orbit data**, and that holds on all **874**
    bridges, along with the correction floor, the phase gap, Theorem 8.3, the
    double-canonical congruences, the weighted-area components and the
    first-hit slice. **Every population count the bundle reports — 874,
    3,038, 90 — is reproduced exactly from the definition.** Three additions
    the shipped checker does not make. `h(h+1)/2` is an integer, so
    `2^(sum H_i) = 2^A / 3^(h(h+1)/2)` and Jensen becomes
    `2^A S^h >= h^h 3^(h(h+1)/2)` — checked on every bridge, where the bundle
    checks Jensen only on synthetic random slack lists. The canonical
    congruences are checked on all 874 rather than the 90 that pass the
    smallness guard, so a congruence failing on a large bridge could not
    hide. And **all three of the shipped checker's assertion sites sit behind
    an `if` while its counters increment once per sample**: measured
    independently at its own parameters, its source-residue assertion runs on
    **10.0%** of samples, its endpoint assertion on **7.6%**, its Jensen
    assertion on **33.8%**, its quantile bound is non-trivial on **5.0%** —
    and passes wherever a guard opens. **Five findings.** Theorem 6.2 is
    vacuous on all **10,488** finite instances, while the sharper form its own
    proof gives — `S` in place of the `3Z` bounding it — is live on **136**.
    Theorem 7.2's finite content `2(A-M) >= (h+1)(Q-h)` is **exactly attained
    on 520 of 874**, so a strict test accuses 520 correct bridges. The
    integer-lift escape of Theorem 9.1 is **empty: `m_h = 0` on all 874**, so
    every finite bridge's excess IS its one-sided phase. Lemma 8.1's `X-Z>=4`
    is correct but nowhere near tight — smallest gap **16**, on both
    populations. And the validation record is the strongest yet: **7 per-file
    digests and 7 sizes, all matching**, `CHECKSUMS` pinning 10 of 11, though
    4 files appear in it nowhere and `CHECKER_STDOUT` is still the checker
    report, now plus one newline. Constants: `beta - e_beta` sits **26 ulps**
    out and is a rounding travelling down a cancelling subtraction from an
    already-2-ulp parent, so each constant now carries a budget of
    `4 x (operand/result)`, tested before the chain excuse. Drill **50/50**,
    and nine defects needed re-aiming — four probed a counter already reading
    zero, two loosened what they attacked, and one stayed TRUE after mutation
    because a congruence mod `m` implies the congruence mod every divisor.
45. [`reports/RUN-046-HARD-ZETA-AU2D18-LIFT-COCYCLE.md`](./reports/RUN-046-HARD-ZETA-AU2D18-LIFT-COCYCLE.md) —
    **the round that turns the slack profile into an integer, and the branch
    of its own dichotomy that has no finite instance.** A-U.2d.18 rereads
    A-U.2d.17's real suffix slack from the other end: `m_ell = Q_ell -
    ceil(beta ell)` with `H_(h-ell) = m_ell + eps_ell`, and full
    suffix-supercriticality is exactly `m_ell >= 0`. Because `ceil(beta ell) =
    (3^ell).bit_length()` and `2^eps_ell = 2^ceil(beta ell) / 3^ell`,
    **sections 7 through 14 are exact rational arithmetic with no logarithm
    anywhere** — including Theorem 11.1's `P_down < 2`, which the bundle
    floats, and Theorem 12.2's mechanical cocycle `U_(l+1) = (2^a U_l -
    2^-m_(l+1))/3`, the round's real contribution. **All twelve of the
    bundle's counters are reproduced exactly from the definition**: 1228
    bridges, 4337 recurrence steps, 125 collapse cases, six countermodels,
    both synthetic blocks. **Three findings.** Every one of the **1228**
    bridges has zero total lift, so the positive-lift branch of Theorem 15.1
    and the whole of Theorem 10.1's rarity bound have **no finite instance** —
    while the interior profile is far from flat, reaching a lift of **8**
    across **1044** descents, every one by exactly one unit at a mechanical
    `a=2` position. **Two of their twelve counters test a quantity against
    itself**: `near_linear_gap_algebra` asserts `N/(R+1) > 0` for `N >= 10^6`
    (smallest left side measured: 134,322), and `positive_lift_drop_algebra`
    asserts an inequality in which **beta cancels exactly**, leaving
    `m + eps >= 1` for an integer `m >= 1` — demonstrated by evaluating it at
    both ends of a certified bracket and getting the same answer 10,000 times.
    Twenty thousand assertion executions, no information. And the
    source-validation record has changed content for the **fifth consecutive
    round** — 7 per-file digests last round, 3 now, execution return code and
    counter cross-check gone. Their float64 `ceil(log2(3)*l)` is **safe and
    now measured**: no disagreement over 20,000 levels, closest approach
    `2.6e-5` at `l = 15601`, float64 error `7e-12`, a margin of **3.7 million
    to one**. Drill **52/52**; four defects made the gate RAISE, and the fix
    was general — every section now reports through an `errors.<section>_raised`
    counter, and `2^k` is written `p2(k)` so a negative lift is a finding
    rather than a crash four sections downstream.
46. [`reports/RUN-047-HARD-ZETA-AU2D19-CARRY-CONJUGACY.md`](./reports/RUN-047-HARD-ZETA-AU2D19-CARRY-CONJUGACY.md) —
    **the conjugacy that makes the real cocycle trivial, and the first
    constant the bundle contradicts itself on.** A-U.2d.18 left the mechanical
    affine cocycle `U_(l+1) = (2^a U_l - 2^-m_(l+1))/3` and pointed at
    `2^a/3` as the place to look for spectral contraction. Setting
    `W_l := 2^-eps_l U_l = 3^l V_l / 2^Q_l` removes the multiplier entirely:
    `W_(l+1) = W_l - 3^l/2^Q_(l+1)`, a strictly decreasing additive carry.
    Everything downstream is then exact rational or exact modular arithmetic —
    the band `Z/2 < W_l <= Z`, the dyadic window, mechanical neutrality
    `prod 2^a_j/3 = 2^(eps_s-eps_r)`, the nested endpoint tower
    `Z = sum 3^(j-1) 2^-Q_j mod 3^l` and its Archimedean twin, and valuation
    aliasing at period `2*3^k`. **All nine of the bundle's counters are
    reproduced exactly**: 1264 bridges, 4433 carry steps, 5697 window
    positions, 4433 tower levels, three synthetic blocks. **Three findings.**
    The constants frontier and the checker report **disagree on `beta`** —
    frontier `1.5849625007211563`, report `1.584962500721156`, one ulp apart,
    and the frontier matches neither the nearest double nor the float64 chain;
    `beta_minus_1` differs by two ulps the same way. First frontier/report
    disagreement of the sweep; trust the report. Section 4's "sharper exact
    window" is written with a strict `<` on its upper end and that end is
    **attained at l = 0** on all 1264 bridges, where `V_0 = Z` exactly —
    Corollary 4.2's phase-free version, which is what the bundle checks, is
    strict there and clean. And `mesoscopic_modulus_algebra` — 10,000
    assertion executions — asserts the defining property of a ceiling three
    times, its third assertion implied by its second; the closest
    `log_3(target)` comes to an integer is `4.6e-5` against a `1e-15` float
    error, a margin of 46 billion to one. Third round running with a large
    synthetic block that cannot fail. **Added here**: exact divisibility where
    the bundle floor-divides; the aliasing period checked sharp in BOTH
    directions (not shorter, not one level deeper); the mechanical alphabet
    over the whole range rather than on sampled intervals; the stabilization
    guard counted (it opens on 892 of 4433 levels, 20%); and both completions
    of Theorem 6.1's identity computed independently. Drill **50/50**, and
    **zero malformed on the first pass** — the RUN-046 section guards paying
    off, since the one defect that raised was reported rather than crashing.
47. [`reports/RUN-048-HARD-ZETA-AU2D20-RETURN-LOOPS.md`](./reports/RUN-048-HARD-ZETA-AU2D20-RETURN-LOOPS.md) —
    **the round whose central object is a loop, and the two things "loop"
    turns out to mean.** A-U.2d.19 showed a fixed ternary modulus has too
    little magnitude resolution; this round asks what a growing one can see
    and finds two structures with opposite characters — an `O(log h)` endpoint
    boundary layer that a near-full modulus resolves faithfully, and a bulk
    carrying linear mass of modular return loops with at most three valuation
    labels each. **All twelve of the bundle's counters are reproduced
    exactly**: 7136 bridges, 27,337 boundary levels, 29,282 transition pairs,
    3,826 loop-mass levels, 1,802 clean runs, three synthetic blocks. The
    sharpest object in the round is Theorem 11.1's loop certificate
    `(2^Q_C - 3^L_C) r_C = B_C mod M`, and **the bundle never checks it** —
    its loop block verifies mass lower bounds only. Built from the real
    orbits, the certificate holds on **all 34,970** loops, together with the
    exact integer identity it is a shadow of. **Three findings.** **"Return
    loop" names two objects and the period bounds one of them**: the erased
    cycle (0 violations, longest 13) and the orbit segment carrying the
    certificate, of which **14,539 of 34,970** exceed the period and **24,798**
    differ from their own cycle — my first version measured the wrong one and
    reported 973 violations of a theorem that was not being tested. **Theorem
    9.1's finite bound is positive on 4 of 3,826 levels**, so a comparison
    against it discriminates almost nothing — and I did not notice until the
    drill planted four defects in my own section and none of them moved a
    counter; the repair is three checks that are TOTAL (a clean run contains
    no low-lift vertex, no `q>=2M` edge, and loop erasure conserves edges).
    And **a fourth synthetic-block shape**: `fixed_power_high_lift_algebra`
    asserts one thing arranged by the line above it, one that is the same
    inequality restated, and one on a loop-invariant constant, while
    `boundary_alias_no_go_algebra` protects its assertion with a **repair
    branch that never fires** (0 of 10,000). **Added here**: Theorem 3.1 in
    its k-term form (the bundle checks the same value by a different
    sentence); both halves of Theorem 4.1 separately, both attained; the
    period checked SHARP in both directions, since uniqueness below `s_k`
    would also hold if the true period were three times longer. Drill
    **50/50**; the run also produced the sweep's first infrastructure
    failure — Windows returned `Errno 22` on a restore write mid-drill, the
    pristine sidecar recovered it and the gate was verified byte-identical,
    and every gate write now retries.
48. [`reports/RUN-049-HARD-ZETA-AU2D21-LOOP-DEFECT.md`](./reports/RUN-049-HARD-ZETA-AU2D21-LOOP-DEFECT.md) —
    **the round that names yesterday's finding, and a law that
    self-composition cannot see.** A-U.2d.21 removes A-U.2d.20's three-sheet
    ambiguity by cutting at the true unique-label threshold `q >= s_k` and
    paying out of the SURPLUS `sum(q-1)` rather than the full valuation sum,
    leaving `(2-beta)h` of fully faithful cycle mass; then it corrects its own
    programme, because the endpoint modulo `3^K` sees only the final `K`
    valuations and a polynomial modulus screens the linear-distance bulk.
    **Twelve of thirteen counters reproduced exactly** (7845 bridges, 18,603
    budget levels, 39,395 faithful cycles, 12,000 + 12,000 screening words,
    three synthetic blocks); the thirteenth differs only because I pool 157
    self-compositions where the bundle runs 20. **Two findings.** The bundle
    tests Theorem 11.1's defect semigroup law by composing each cycle with
    **itself**, with the comment "self-composition is enough to check
    algebra" — and it is not: at `D = C` the law is **symmetric in its two
    coefficients**, so the coefficient-swapped law gives the same answer.
    Measured: the swapped law agrees on **all 157** self-compositions and
    disagrees on **all 218** distinct pairs. And **three of thirteen counters
    — 30,000 executions — cannot fail**, in three shapes this sweep has
    already catalogued (arranged, restated, loop-invariant), fifth round
    running. **The round's NO-GO 12.1 is exactly RUN-048's Finding 1**,
    reached independently one round earlier by measurement — and the
    measurement is sharper than the prohibition: over 38,338 graph cycles the
    certificate holds on **every** one, while the quotient lift holds on
    **11,198 of 11,198 contiguous** cycles and fails on **27,140 of 27,140
    spliced** ones, with zero accidental survivals. **Added here**: screening
    checked for SHARPNESS in both directions (a change inside the horizon must
    move the residue, one outside must not); the surplus budget measured live
    and **attained** — binding on 15,022 of 18,603 levels where the previous
    round's bound managed 4 of 3,826. Drill **50/50**; three re-aims found
    real gaps in this gate, including one in my own headline finding, where I
    had guarded only half of a two-halved claim.
49. [`data/results.v1.json`](./data/results.v1.json) — machine-readable claims,
   bounds, gate outcomes, and source digests. Generated from the archived gate
   logs by `code/build_results.py`, never typed by hand.
50. [`code/`](./code/) — the engine, the independent reference, and the gates.
51. [`data/gate-logs/`](./data/gate-logs/) and
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
