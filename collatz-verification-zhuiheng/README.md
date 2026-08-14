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

`2^40` is far below the published frontier, which stands at **at least `2^68`**
(Barina, *Convergence verification of the Collatz problem*, The Journal of
Supercomputing, 2021), with distributed work reporting further progress since.
That literature claim was not independently checked here and is not restated as
this arm's own result. A local run is never a record attempt; a bound this arm
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
   of Papers 02, 06, 07 and 09 rechecked against referees that assume none of them.
   Includes the §14 bridge tying two papers' correction terms together, and
   `K(2^40) = 550` — Paper 09's frontier function evaluated at the scale the
   engine actually measured.
4. [`data/results.v1.json`](./data/results.v1.json) — machine-readable claims,
   bounds, gate outcomes, and source digests. Generated from the archived gate
   logs by `code/build_results.py`, never typed by hand.
5. [`code/`](./code/) — the engine, the independent reference, and the gates.
6. [`data/gate-logs/`](./data/gate-logs/) and
   [`data/raw-logs/`](./data/raw-logs/) — the evidence the above is built from.

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
