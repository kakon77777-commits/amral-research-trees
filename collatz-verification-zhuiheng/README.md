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

Across thirty-five source items and sixteen runs, **nothing in the source
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
18. [`data/results.v1.json`](./data/results.v1.json) — machine-readable claims,
   bounds, gate outcomes, and source digests. Generated from the archived gate
   logs by `code/build_results.py`, never typed by hand.
19. [`code/`](./code/) — the engine, the independent reference, and the gates.
20. [`data/gate-logs/`](./data/gate-logs/) and
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
