# P/NP GLC Observatory I0

Status: **engineering candidate / Experiment**. This project implements a bounded admission-reality slice; it does not adopt a theorem and makes no P=NP or P!=NP claim.

## Delivered boundary

- The unchanged v0.1 file remains the structural transport schema at `../run-record.schema.json`, SHA-256 `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4`.
- `schemas/run-record.schema.v0.2.0-candidate.json` adds one-way, fail-closed conditionals to reduce record misuse. It still does **not** establish that evidence is true.
- `src/pnp_glc_i0/semantic_validator.py` is the versioned external validator. It resolves content, checks canonical projection and receipt bindings, replays trace events, folds ledger/debt, derives gate results and independently checks supported correctness oracles.
- Candidate-controlled output is `candidate_result`. Admission and final completion exist only in the separate external `validation_receipt`.

## Gate matrix

`GateResult = pass | fail | unknown | not-applicable`. Both `fail` and `unknown` block admission.

| Run/resource quadrant | run class | maximality/fairness | resource account | resource budget |
|---|---|---|---|---|
| standard / neutral | pass | N/A | pass | N/A |
| standard / bounded | pass | N/A | pass | pass |
| robust / neutral | pass | pass + non-null specs | pass | N/A |
| robust / bounded | pass | pass + non-null specs | pass | pass |

The schema encodes implications only in the safe direction: `admission_pass=true` or `final_completion=true` constrains prerequisites. It does not infer either aggregate merely because declared gates are `pass`. The external validator recomputes the aggregates.

## Trace-to-record soundness implemented in I0

The validation receipt binds the schema hash, validator hash, projection-spec id/hash, candidate-projection hash, trace hash and the exact resolved operational-evidence hash set. The trace is bound to the run, gate version and projection.

Hash equality is only an integrity check. Replay additionally:

- requires the trace event stream and candidate output to reproduce the record;
- verifies contiguous event sequence, state/representation chain and terminal output hash;
- sums event time accounts into the ledger and checks raw space/description/admission/precision/count samples;
- folds debt additions/retirements into registered, peak-open and outstanding debt;
- resolves certificate refs and checks the candidate result against an independent PARITY or 2-SAT oracle when supported.

The canonical candidate projection excludes `validation_receipt`, avoiding self-hash and derived-field cycles. Its exact Unicode, integer and JSON rules are in `artifacts/candidate-projection-spec.v0.2.0.json`.

## I0 mechanisms

### PARITY admission reality test

- `parity.stream_parity`: one uniform program, state `(i,b)`, update `b <- b XOR x_i`, with a locally checked prefix invariant.
- `parity.TruthTableFamily`: one materialized table for each `n`; decode is linear in the input width while construction/advice is `2^n`. Materialization is bounded and fails closed above the configured limit.
- Terminal-only projection intentionally gives both families the same `Y`, correctness, zero-debt and `O(n)` decode fields. External admission accepts the streaming record and rejects the table family.
- Fixed-program scaling and pointwise envelope are separate report series.

### 2-SAT baseline

- deterministic implication graph + Kosaraju SCC;
- SAT oracle checks every clause under the returned assignment;
- UNSAT certificate supplies paths `x -> not x` and `not x -> x` inside the implication graph;
- randomized small cases are cross-checked against exhaustive enumeration.

Failure frontier: clauses wider than two, free general-CNF conversion, and incremental-update bounds are outside this baseline.

## Fixtures

| Fixture | Expected outcome |
|---|---|
| `legit` | structurally and semantically valid; admission/final true |
| `robust-legit` | robust specs resolve; all applicable gates pass |
| `neutral-legit` | standard/neutral: account pass, budget N/A |
| `robust-neutral-legit` | robust/neutral: run gates/account pass, budget N/A |
| `cheat` | coherent rejected Experiment; record valid, admission false |
| `unknown-gate` | insufficient provenance remains `unknown`; admission false |
| `self-report` | schema rejects candidate `admission_pass` |
| `robust-null-spec` | schema rejects null maximal/fairness specs |
| `failed-gate-admission` | schema rejects aggregate true over failed gates |
| `false-final-completion` | schema rejects false prerequisites/debt with final true |
| `unknown-final` | schema rejects unknown terminal status with final true |
| `tampered-record` | semantic validator rejects projection/replay mismatch |
| `tampered-trace` | semantic validator rejects even though the new trace hash resolves |
| `unresolved-event-ref` | semantic validator closes event rule/invariant refs and rejects |
| `circular-field` | schema rejects external derived field in candidate output |
| `canonicalization-variant` | semantic validator rejects non-NFC projection variant |

## Reproduce

From this directory in PowerShell:

```powershell
$env:PYTHONPATH = 'src'
python scripts\generate_fixtures.py
python -m unittest discover -s tests -v
python -m pnp_glc_i0 validate fixtures\legit.json fixtures\cheat.json `
  --schema schemas\run-record.schema.v0.2.0-candidate.json --artifacts .
python -m pnp_glc_i0.experiment --project-root . --output i0-run-report.json
```

Fixture regeneration is deterministic except for no timing values: fixture ledgers use fixed test measurements. `i0-run-report.json` is a live bounded Experiment and therefore records machine-dependent nanosecond observations.
