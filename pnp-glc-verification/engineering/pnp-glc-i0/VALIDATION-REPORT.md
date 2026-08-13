# I0 v0.2 candidate validation report

Date: 2026-08-09 Asia/Taipei  
CTCL coordinate: `ctcl:instant:b8ce3d5a-9369-4c60-8436-737ecd818ac7` (coordination only)  
Status: **engineering candidate / Experiment / awaiting AI-1 second acceptance**

## Frozen core artifacts

| Artifact | SHA-256 |
|---|---|
| unchanged v0.1 structural schema | `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4` |
| v0.2 candidate schema | `1AD5AFA3A76E56AD5C9D0B79DF34B897E337606093D282693932085BF1AF297C` |
| external semantic validator | `4C50BE9EF563644BC29F3DCEEFB9D9205056631847980FCC763D1E4BA25EB771` |
| candidate projection spec | `9966B86DBC3884E3327306FF1FEFAF21EFBDE705EE0F10739755BE27C73A1991` |
| fixture manifest | `00FA70A6B8F8FA8029D5C0500064FAD4310811E5CDBCC8EFDECC939C9E19F7B2` |
| bounded live I0 report | `2AF00888C571EE5E6ADC2DD84F9892D166ECD17022EB7D3A77D30CF078C9161D` |

The live I0 report contains machine-dependent timings; rerunning it is expected to change that report hash. Schema, validator, projection spec and deterministic fixtures should remain stable unless versioned.

## Required gate checklist

| Obligation | Result | Evidence |
|---|---|---|
| v0.1 preserved | PASS | unit test recomputes exact original hash |
| v0.2 Draft 2020-12 metaschema | PASS | `Draft202012Validator.check_schema` |
| implications remain one-way | PASS | schema accepts aggregate=false over otherwise passing declarations; semantic validator then derives the aggregate |
| robust refs and run gates | PASS | robust positive fixtures pass; `robust-null-spec` schema-rejected |
| four-value GateResult | PASS | `pass|fail|unknown|not-applicable`; honest unknown record remains valid but not admitted |
| run-class nonempty in standard and robust | PASS | all four quadrant fixtures derive pass |
| account always applicable | PASS | admission/final implications require account pass and complete ledger in every quadrant |
| budget applicable only when bounded | PASS | neutral fixtures require N/A; bounded fixtures require pass |
| candidate/external separation | PASS | candidate self-report and circular-field fixtures schema-rejected |
| failed gate cannot claim admission | PASS | `failed-gate-admission` schema-rejected |
| false prerequisites/debt cannot claim final | PASS | `false-final-completion` schema-rejected |
| unknown/timeout/error cannot claim final | PASS | `unknown-final` schema-rejected |
| versioned canonical projection | PASS | explicit spec id/hash, NFC, integer and JSON serialization rules |
| receipt binding | PASS | schema/validator/projection/trace/candidate/evidence hashes all recomputed and compared |
| no projection self-hash cycle | PASS | projection excludes the entire external receipt |
| hash/parse/use TOCTOU closure | PASS | ArtifactIndex retains immutable byte snapshots; mutation-after-index unit test reads original bytes |
| trace-to-record replay | PASS | event/result/certificate equality, state chain, terminal output, time/resource/debt folds |
| event ref evidence closure | PASS | event transition/invariant refs enter the exact closure; unresolved-event fixture rejected |
| independent correctness | PASS | validator computes PARITY and 2-SAT oracles; contract derives from oracle + replay + zero debt |
| PARITY dual family | PASS | uniform streaming admitted; coherent per-length table record rejected by admission |
| terminal-only blind spot | PASS | live report preserves identical terminal projection while excluding external admission |
| pointwise/fixed scaling split | PASS | separate series semantics and construction/advice columns |
| 2-SAT SAT certificate | PASS | returned assignment independently satisfies every clause |
| 2-SAT UNSAT certificate | PASS | mutual implication paths independently checked |
| 2-SAT exhaustive cross-check | PASS | 1,500 fixed-seed random small formulas agree with exhaustive oracle |
| automated suite | PASS | 14 tests, 0 failures |

## Fixture outcomes

- Positive/admitted: `legit`, `robust-legit`, `neutral-legit`, `robust-neutral-legit`.
- Coherent but not admitted: `cheat`, `unknown-gate`.
- Schema-level rejection: `self-report`, `robust-null-spec`, `failed-gate-admission`, `false-final-completion`, `unknown-final`, `circular-field`.
- Semantic/replay rejection: `tampered-record`, `tampered-trace`, `canonicalization-variant`, `unresolved-event-ref`.

The tampered-trace fixture points to a newly hashed, resolvable trace. It is rejected by replay rather than merely by a stale hash, demonstrating that integrity equality is not treated as `DerivesRecord`.

## Reproduction command

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'src'
python scripts\generate_fixtures.py
python -m unittest discover -s tests -v
python -m pnp_glc_i0.experiment --project-root . --output i0-run-report.json
```

## Remaining failure frontier

- The trusted capability-trace producer is a local trust boundary; content addressing proves integrity, not institutional origin or signature authority.
- The projection format deliberately rejects floats and non-NFC strings; expanding the domain requires a new projection-spec version.
- The semantic validator has executable correctness dispatch for I0 PARITY and 2-SAT. Unsupported problem families return `unknown` and cannot be admitted by this version.
- Performance measurements are bounded experiments, not asymptotic proofs. Table materialization is capped fail-closed.
- Horn-SAT, XOR-SAT, bounded-treewidth SAT, CDCL and quotient/portfolio experiments remain intentionally unimplemented pending gate acceptance.

No test result implies P=NP or P!=NP.
