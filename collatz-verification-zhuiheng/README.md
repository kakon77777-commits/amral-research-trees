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
8. [`data/results.v1.json`](./data/results.v1.json) — machine-readable claims,
   bounds, gate outcomes, and source digests. Generated from the archived gate
   logs by `code/build_results.py`, never typed by hand.
9. [`code/`](./code/) — the engine, the independent reference, and the gates.
10. [`data/gate-logs/`](./data/gate-logs/) and
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
