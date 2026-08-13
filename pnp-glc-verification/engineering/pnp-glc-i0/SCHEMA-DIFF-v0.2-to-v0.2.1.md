# v0.2 → v0.2.1 candidate diff

This is a versioned hardening candidate. Frozen v0.2 files and hashes are unchanged.

## Schema additions

- `receipt_version`, schema version and gate version advance to `0.2.1`.
- `validation_receipt` adds:
  - `trace_authenticity_ref`
  - `trace_public_key_ref`
  - `trace_signer_id`
  - `artifact_closure_spec_ref`
- `gates` adds four-valued:
  - `trace_authenticity_pass`
  - `transition_execution_pass`
  - `resource_derivation_pass`
- `admission_pass=true` implies all three new applicable gates are `pass`.
- Existing implications remain one-way; all constituent gates being `pass` does not force the aggregate field to true.
- Existing resource matrix remains: account completeness is always applicable; budget is applicable only when resource-bounded.

Schema SHA-256: `567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B`.

## External-validator additions

- Parse/hash/use of schema, record and artifacts uses a single byte snapshot.
- Canonical projection grammar explicitly maps newline spellings such as `\n` and `\u000a` to the unique output bytes `"\n"`; NFC and safe-integer restrictions remain fail-closed.
- Operational evidence uses a fixed-point typed-reference closure with cycle detection. Missing or malformed members fail; unknown envelope specifications derive `unknown`.
- Trace authenticity uses Ed25519, a pinned signer identity and a pinned public-key content hash. The producer string is checked as metadata but cannot establish authenticity.
- PARITY and 2-SAT transition execution recompute algorithm output and intermediate/final digests using pinned source hashes.
- Event states/counts, time and debt are recomputed. Raw space, description, admission-cost and precision observations require the authenticated I0 measurement trace.
- Correctness contracts require independent oracle success plus authenticated replay, transition execution, resource derivation and zero outstanding debt.

Validator SHA-256: `C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4`.

## Required negative fixtures

| Fixture | Layer that rejects it |
|---|---|
| `fabricated-states-999` | resource derivation; signature and structural replay deliberately remain valid |
| `fabricated-transition-digest` | transition execution; signature and structural replay deliberately remain valid |
| `bad-trace-signature` | Ed25519 trace authenticity |
| `missing-transitive-ref` | fixed-point typed-reference closure |
| `tampered-record` | projection/trace/result/oracle bindings |
| `tampered-trace` | signed trace-to-record replay |
| `canonicalization-variant` | NFC canonical domain |
| `self-report`, `robust-null-spec`, `failed-gate-admission`, `false-final-completion`, `unknown-final`, `circular-field` | JSON Schema implications/shape |

## Added positive coverage

- Standard/robust × neutral/bounded matrix records.
- Uniform PARITY and rejected nonuniform table family.
- End-to-end 2-SAT SAT and UNSAT records with independently verified certificates.
- Live report includes `robust-legit` and `unknown-final`.

## Trust boundary

The delivered public key verifies that the trace was signed by the fixture key. It does not prove OS isolation, honest hardware counters, or production custody of that key. The test private key is intentionally outside the deliverable tree. Production measurement authority remains an Open Problem.

