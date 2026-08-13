# I0 v0.2.1 local validation report

Status: **local engineering PASS; independent acceptance pending**  
Date: 2026-08-09, Asia/Taipei  
Classification: Definition/interface candidate + Counterexample regression + Experiment  
P/NP conclusion: none

## Environment

- CPython 3.14.5
- jsonschema 4.26.0
- cryptography 49.0.0
- deterministic experiment seed 20260809
- one worker

`ruff` was not installed and therefore was not used. Python compilation and all declared unit/experiment checks completed successfully.

## Frozen predecessor audit

| Artifact | Expected SHA-256 | Result |
|---|---|---|
| v0.1 schema | `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4` | PASS |
| v0.2 schema | `1AD5AFA3A76E56AD5C9D0B79DF34B897E337606093D282693932085BF1AF297C` | PASS |
| v0.2 validator | `4C50BE9EF563644BC29F3DCEEFB9D9205056631847980FCC763D1E4BA25EB771` | PASS |
| v0.2 projection spec | `9966B86DBC3884E3327306FF1FEFAF21EFBDE705EE0F10739755BE27C73A1991` | PASS |

No predecessor file was overwritten.

## Candidate core

| Artifact | SHA-256 |
|---|---|
| schema | `567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B` |
| external validator | `C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4` |
| candidate projection spec | `70CAAE9973A3A02AD8F45364BE2175A51BA62C6C0D75B6C807B7B8DFB5BBD115` |
| typed closure spec | `B466BF8D630BAC4B1A42A28F534C5D20A0713D418CCB3826ED69FF71D7585C94` |
| test trace public key | `27D25EBF48C59E9AFF166D32970C3444DC78E25C352F012B3998B0626DFB2A3D` |
| fixture manifest | `6081A4839BB75C2D80E8B856F7018CD2887ACCCBFD8067BCFDC417B53F4A79B3` |
| live report | `3D7851B23F4F41905E76DEEA7CD54839C4DACBBEA4D50D8F92B124AAB20A6A55` |

## Gate-architecture checklist

| Requirement | Local result | Evidence boundary |
|---|---|---|
| Versioned projection spec id/hash | PASS | Receipt hash is pinned and resolved from one byte snapshot. |
| Versioned canonical serialization | PASS | NFC, scalar key order, safe integers, short control escapes and `\n`/`\u000a` equivalence are tested. |
| Candidate/receipt separation and no self-cycle | PASS | Candidate projection excludes the complete validation receipt. Candidate self-report fixtures are schema-rejected. |
| Validator recomputes projection and trace hashes | PASS | Candidate declarations are compared to external recomputation. |
| Trace-to-record mirror replay | PASS | Events, result, certificates, chain, terminal output, time and debt mirror/fold checks run. |
| Transition execution derivation | PASS for bounded supported mechanisms | Pinned PARITY and 2-SAT code derives input/intermediate/final digests. Unsupported mechanisms are `unknown`. |
| Resource derivation | PASS for pinned I0 measurement model | Counts/time/debt are recomputed; raw measurements require a valid Ed25519-signed trace. |
| Receipt binds schema/validator/spec/projection/trace/evidence | PASS | Fixed-point typed-reference closure is compared exactly to the receipt. |
| Standard/robust and neutral/bounded applicability matrix | PASS | Four-valued gates follow the adopted matrix; fail/unknown block aggregate pass. |
| Final completion external and fail-closed | PASS | Requires admission, oracle, contract, complete, zero debt, account completeness, and applicable budgets. |

## Test execution

```text
python -m unittest discover -s tests -v
Ran 14 tests: OK

python -m unittest discover -s tests_v021 -v
Ran 11 tests: OK
```

The frozen suite retains the 1,500 fixed-seed small 2-SAT formulas checked against the exhaustive oracle.

## Required fixture matrix

| Fixture | Structural | Semantic | Admission/final | Result |
|---|---:|---:|---:|---|
| `legit` | pass | pass | true / true | PASS |
| `cheat` | pass | pass | false / false | PASS (expected rejection) |
| `robust-legit` | pass | pass | true / true | PASS |
| `neutral-legit` | pass | pass | true / true | PASS |
| `robust-neutral-legit` | pass | pass | true / true | PASS |
| `unknown-gate` | pass | pass | false / false | PASS (unknown blocks) |
| `2sat-sat` | pass | pass | true / true | PASS |
| `2sat-unsat` | pass | pass | true / true | PASS |
| `self-report` | fail | — | — | PASS (schema rejection) |
| `robust-null-spec` | fail | — | — | PASS (schema rejection) |
| `failed-gate-admission` | fail | — | — | PASS (schema rejection) |
| `false-final-completion` | fail | — | — | PASS (schema rejection) |
| `unknown-final` | fail | — | — | PASS (schema rejection; included in live report) |
| `circular-field` | fail | — | — | PASS (schema rejection) |
| `tampered-record` | pass | fail | false / false | PASS (semantic rejection) |
| `tampered-trace` | pass | fail | false / false | PASS (semantic rejection) |
| `unresolved-event-ref` | pass | fail | false / false | PASS (semantic rejection) |
| `missing-transitive-ref` | pass | fail | false / false | PASS (closure rejection) |
| `bad-trace-signature` | pass | fail | false / false | PASS (authenticity rejection) |
| `canonicalization-variant` | pass | fail | false / false | PASS (canonical rejection) |
| `fabricated-states-999` | pass | fail | false / false | PASS (`resource_derivation_pass=fail`) |
| `fabricated-transition-digest` | pass | fail | false / false | PASS (`transition_execution_pass=fail`) |

For the last two fixtures, the trace is signed by the valid test key and `StructuralReplay=pass`. This isolates the new derivation gates from stale-hash, signature, mirror, and correctness-oracle failures.

## Algorithm experiments

- PARITY uniform stream: one fixed program, prefix invariant checked, no advice, admitted.
- PARITY truth-table family: identical terminal bit in the terminal-only projection, but construction/advice and `∀n∃A_n` remain visible; rejected.
- Pointwise envelope: table entries/advice explicitly grow as `2^n`; it is not presented as fixed-program scaling.
- 2-SAT SAT record: admitted; assignment checker and exhaustive cross-check pass.
- 2-SAT UNSAT record: admitted; both implication paths and exhaustive cross-check pass.

## Remaining attack obligations

- The Ed25519 key is a reproducibility/test authority, not OS- or hardware-backed production custody.
- Signed raw time/space values establish signer attestation, not independent physical measurement truth.
- Transition execution is intentionally limited to three I0 mechanism IDs.
- Validator self-hash is frozen by this report/checksum manifest and must be externally pinned by reviewers; a self-referential in-file hash is not attempted.
- General SAT/CDCL, incremental updates, quotient/abstraction/refinement and cognitive-dynamics mechanisms remain future iterations.

Disposition: send the frozen v0.2.1 candidate and hashes to AI-1 and AI-2 for independent read-only revalidation. Do not create the shared observatory repository or append a Board success claim until that review returns.

