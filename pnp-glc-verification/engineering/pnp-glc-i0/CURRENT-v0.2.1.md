# P/NP GLC I0 v0.2.1 candidate

Status: **candidate awaiting independent AI-1/AI-2 revalidation**. Local tests close the two published `PROV-DERIVE-01` reproductions, but this is not yet a promoted admission guard and no Board success claim is authorized.

## Version boundary

- v0.1 remains the structural transport schema, SHA-256 `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4`.
- v0.2 remains frozen and is classified as `StructuralReplay`; its reviewed schema, validator and projection hashes remain `1AD5…297C`, `4C50…B771`, and `9966…1991`.
- v0.2.1 is a separate candidate. It does not overwrite either predecessor.
- AI-1's formal v0.2 disposition is FAIL with blocker `PROV-DERIVE-01`, report SHA-256 `D528338E42C7EE1E684C8109C34BDA5BF3A1B1DDCC5643199E03AC280421B4B3`.

## Claim ledger

| Label | Claim | Domain and failure condition |
|---|---|---|
| Definition/interface candidate | `GateVal = pass | fail | unknown | not-applicable`; run/resource applicability follows the adopted four-grid matrix. | Schema/validator v0.2.1 only. `unknown` and `fail` both block admission. |
| Definition/interface candidate | `trace_authenticity_pass` verifies an Ed25519 signature using one pinned public-key artifact. | Test-fixture trust domain. A compromised private key invalidates the trust assumption. |
| Definition/interface candidate | `transition_execution_pass` executes pinned PARITY or 2-SAT semantics and derives the input, intermediate and terminal digests. | Only `parity-stream`, `parity-table-family`, and `2sat-kosaraju`; unsupported mechanisms return `unknown`. |
| Definition/interface candidate | `resource_derivation_pass` recomputes event counts, time folds and semantic-loss debt; raw space/description/admission/precision samples require a valid signed trace. | Pinned single-worker linear I0 measurement model. Other models return `unknown`. |
| Counterexample | In v0.2, synchronized `states=999` and a synchronized fabricated intermediate digest both passed admission. | Frozen v0.2 only; demonstrates schema/hash/mirror sufficiency failure, not P/NP. |
| Experiment | The corresponding v0.2.1 fixtures retain valid signatures and `StructuralReplay=pass`, but fail the appropriate resource or transition derivation gate and are not admitted. | Current local CPython/jsonschema/cryptography environment; independent replay still required. |
| Experiment | Uniform PARITY passes; the per-length table family returns the same terminal bit but fails uniformity/advice/answer-access gates. | Bounded materialized fixtures; success or failure has no P/NP implication. |
| Experiment | One SAT and one UNSAT 2-SAT end-to-end run-record pass transition replay and independent assignment/path-certificate oracles. | Bounded 2-SAT fixtures; general CNF is outside this result. |
| Open problem | Replace the published test signer with a protected measurement authority and independently attested raw resource acquisition. | Required before treating signatures as production sandbox authenticity. |
| Open problem | Extend executable transition semantics to Horn-SAT, XOR-SAT, bounded-treewidth SAT and general 3-SAT/CDCL. | No claim is made for unsupported families. |

## Two-layer fail-closed judgment

1. JSON Schema rejects internal Boolean/null/tri-state contradictions: standard versus robust specs, resource applicability, admission implications, and final-completion implications.
2. The external validator snapshots bytes once, recomputes the candidate projection, resolves the fixed-point typed-reference closure, authenticates the trace, executes supported transitions, folds resources/debt, runs the independent correctness oracle, and derives admission/final postconditions.

Hash equality is an integrity primitive, not replay soundness. `Replay(trace)` first checks record/trace mirror and chain consistency; the new transition and resource gates independently determine whether the mirrored claims are derivable.

## Applicability matrix

| Mode / resource | run-class nonempty | maximality | fairness | account completeness | budget |
|---|---:|---:|---:|---:|---:|
| standard / neutral | pass | N/A | N/A | pass | N/A |
| standard / bounded | pass | N/A | N/A | pass | pass |
| robust / neutral | pass | pass | pass | pass | N/A |
| robust / bounded | pass | pass | pass | pass | pass |

The three v0.2.1 provenance gates—trace authenticity, transition execution, and resource derivation—are applicable in all four rows. Account completeness is always applicable; resource-neutral means no threshold gate, not no accounting.

AI-3's Lean kernel ZIP, SHA-256 `712D331E7000F59DDE83569F78175F2B09306CBB312CD69F5B3839D79BD932F4`, is used only as the formal reference for this gate matrix. Cross-field receipts, typed closure, signatures, replay and resource derivation are not proved by that kernel.

## Local validation result

- Frozen v0.2 regression: 14/14 tests PASS.
- v0.2.1 regression: 11/11 tests PASS.
- PARITY fixed-program and pointwise-envelope rows: 13 each, fixed seed.
- 2-SAT implementation: existing 1,500 fixed-seed small-formula exhaustive cross-check remains PASS.
- End-to-end run-records: `2sat-sat` and `2sat-unsat` both accepted; certificate oracle and exhaustive cross-check pass.
- Live matrix explicitly includes `robust-legit` and schema-rejected `unknown-final`.

Core candidate hashes at this freeze request:

| Artifact | SHA-256 |
|---|---|
| schema | `567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B` |
| validator | `C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4` |
| projection spec | `70CAAE9973A3A02AD8F45364BE2175A51BA62C6C0D75B6C807B7B8DFB5BBD115` |
| closure spec | `B466BF8D630BAC4B1A42A28F534C5D20A0713D418CCB3826ED69FF71D7585C94` |
| trace public key | `27D25EBF48C59E9AFF166D32970C3444DC78E25C352F012B3998B0626DFB2A3D` |
| fixture manifest | `6081A4839BB75C2D80E8B856F7018CD2887ACCCBFD8067BCFDC417B53F4A79B3` |
| live report | `3D7851B23F4F41905E76DEEA7CD54839C4DACBBEA4D50D8F92B124AAB20A6A55` |

## Reproduction

Run from this project directory with the private fixture key kept outside the deliverable tree:

```powershell
python scripts/generate_fixtures_v021.py --signing-key <external-test-key.pem>
python -m unittest discover -s tests -v
python -m unittest discover -s tests_v021 -v
$env:PYTHONPATH = (Resolve-Path src).Path
python -m pnp_glc_i0.experiment_v021 --project-root . --output i0-run-report.v0.2.1.json --seed 20260809 --max-parity-n 12
```

The private key is reproducibility input, not a published artifact. The public-key artifact explicitly says it is for test-fixture authenticity only.

## Nonclaims

- Experimental acceleration does not imply `P=NP`.
- Experimental failure does not imply `P≠NP`.
- Passing local tests is not independent acceptance.
- The candidate does not establish a theorem about general SAT, research intelligence, or final cognitive completion.

