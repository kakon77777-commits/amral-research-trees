# AI-2 I0 v0.2.1 bounded red-team revalidation

**Disposition:** `FAIL / REF-TYPE-01`

**Classification:** engineering/provenance admission blocker for the frozen v0.2.1 candidate. This is not a P/NP result and does not invalidate the narrower positive matrix results.

**Method:** read-only inspection plus independently written adversarial probes. The candidate tree was not modified. Temporary files were used only outside the candidate tree for raw-JSON and snapshot tests.

## Frozen identity and baseline

The supplied core hashes matched exactly:

- schema: `567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B`
- validator: `C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4`
- projection spec: `70CAAE9973A3A02AD8F45364BE2175A51BA62C6C0D75B6C807B7B8DFB5BBD115`
- closure spec: `B466BF8D630BAC4B1A42A28F534C5D20A0713D418CCB3826ED69FF71D7585C94`
- public key: `27D25EBF48C59E9AFF166D32970C3444DC78E25C352F012B3998B0626DFB2A3D`
- fixture manifest: `6081A4839BB75C2D80E8B856F7018CD2887ACCCBFD8067BCFDC417B53F4A79B3`
- checksum manifest: `4F5925CD2A449549F9629017E538F5FA341FA8BAECB4A5BB3F8B93ED005EBD6A`

`SHA256SUMS-v0.2.1.txt` verified `69/69`. The old suite passed `14/14`; the v0.2.1 suite passed `11/11`. Six positive records (`legit`, `robust-legit`, both neutral variants, `2sat-sat`, and `2sat-unsat`) were independently accepted before mutation.

These facts establish frozen identity and the tested matrix only. They do not establish type-safe evidence closure.

## Attack matrix

| ID | Attacked claim | Minimal probe | Observed result | Disposition |
|---|---|---|---|---|
| `PROV-DERIVE-01` | Signed mirror/replay is insufficient unless transition and resources derive | Revalidate the two published, valid-signature fabricated fixtures | `states=999` fails resource derivation; fabricated transition digest fails transition execution; both are rejected | Closed regression |
| `SIG-TRANSPLANT-01` | Producer string, signer label, key, or authenticity receipt can substitute for signature binding | Producer-only bad signature; cross-record authenticity receipt; wrong key role; wrong signer | All rejected | Closed bounded surface |
| `TOCTOU-01` | Hash, parse, and use reopen paths | One-read schema/record objects; replace a temporary artifact after index construction | One read each; old artifact bytes remain pinned and are used for parse | Closed for `validate_path` and `ArtifactIndex` |
| `CLOSURE-FIXPOINT-01` | Fixed-point traversal misses cycles, malformed envelopes, or missing transitive refs | Synthetic two-node cycle; missing child; malformed known envelope; unknown spec | Cycle terminates with two refs; missing/malformed fail; unknown spec is unknown | Closed bounded algorithm surface |
| `REF-TYPE-01` | Transitive hash closure proves role/type-correct operational evidence | Valid signed robust record; change only receipt refs; recompute closure; no re-sign | Signature and closure pass; semantic/admission/final/accepted all true; no issues | **Counterexample / blocker** |
| `CANON-CORE-01` | Escape, NFC, and numeric canonical domain are enforced | `\n` versus `\u000a`, NFD, float, oversized integer, raw `-0`, unpaired surrogate | Core cases close; raw `-0` is accepted; surrogate is indirectly rejected | One conformance counterexample plus hardening |
| `ORACLE-CONTRACT-01` | SAT/UNSAT result is trusted rather than recomputed | Empty SAT assignment and broken UNSAT paths | Independent oracle and transition execution both fail | Closed bounded recomputation surface |
| `GATE-BYPASS-01` | Gate/applicability/final completion fields can self-authorize | Mutate all 18 gates; use contradictory admission/final fixtures; robust null specs | No semantic acceptance bypass found | Closed bounded surface |

## Blocking counterexample: REF-TYPE-01

The attacked claim is that a passing fixed-point artifact closure plus a valid trace signature establishes role-correct operational evidence for robust execution.

Minimal premises:

1. Start from the valid signed `robust-legit` record.
2. Change only fields inside `validation_receipt`, which the candidate projection and trace signature exclude.
3. Recompute `resolved_evidence_hashes` exactly from the validator's own closure algorithm.
4. Do not alter or re-sign the trace.

Two independent variants reproduced:

- Replace only `run_spec_ref` from the robust-run artifact to the standard-run artifact.
- Replace `run_spec_ref`, `maximal_run_spec_ref`, `fairness_spec_ref`, and `capability_sandbox_ref` with the pinned Ed25519 public-key artifact reference.

For both variants the frozen validator returned:

```text
trace_authenticity = pass
artifact_closure    = pass
structural_ok       = true
semantic_ok         = true
admission_pass      = true
final_completion    = true
record_accepted     = true
issues              = []
```

The accepted construction is therefore only an **envelope-aware transitive hash closure**, not a role/type-safe evidence closure. The existential counterexample is sufficient to refute v0.2.1 closure sufficiency within this engineering interface; it has no P/NP implication.

Required repair obligation for a successor version:

- Define a versioned field-role to expected artifact type, semantic id, version, and mode map.
- Encode role-bearing edges, not merely unlabelled `typed_refs`.
- Bind the operational-reference map by the signed candidate projection or derive it uniquely in the external validator.
- Give legacy leaf specs typed envelopes or an externally pinned typed registry.
- Bind family, contract, oracle, transition rule, invariant, robust-run, fairness, maximality, and sandbox roles coherently.
- Add valid-signature cross-role substitutions as mandatory negative fixtures.

## Narrow additional findings

### SCHEMA-BIND-API-01 — conditional interface blocker

`validate_path` correctly hashes and parses one schema-byte snapshot. The lower-level, publicly named `validate_record(record, schema, ..., schema_sha256=...)` does not bind the supplied schema mapping to the supplied digest string.

Counterexample:

1. Add an extra receipt-only field to `legit`; the pinned schema rejects it and the signed candidate projection is unchanged.
2. Call `validate_record` with the empty schema object `{}` but claim the pinned schema SHA-256.
3. The frozen function returns structural/semantic/admission/final/accepted all true with no issues.

This is a blocker if `validate_record` is a supported trust-boundary entrypoint. The shipped tests and v0.2.1 experiment use `validate_path`, so it is otherwise an interface-hardening correction: make the helper private, accept schema bytes and hash the same bytes internally, or pass an immutable schema-snapshot object whose digest is derived inside the validator.

### CANON-NEGZERO-01 — canonical-spec conformance counterexample

The pinned projection spec says negative zero is forbidden. Replacing one raw candidate-projected `"seed": 0` token with `"seed": -0` produces the identical Python integer value, identical canonical projection, and an accepted record under the existing signature. This does not change the semantic answer, but it defeats the declared raw-domain uniqueness and permits record malleability.

Repair: reject the exact integer token `-0` in the raw JSON parser (for example through a strict `parse_int` hook) before lexical information is lost.

### CLOSURE-CLASS-01 — fail-closed classification correction

The closure spec says that an envelope missing any required member is malformed and must be `fail`. The implementation returns `unknown` when `spec_id` is missing, because it checks for an unknown spec before checking required members. Admission is still blocked, so this is not an acceptance bypass. Check required-member presence/type first, then distinguish an actually present but unknown `spec_id`.

### CANON-SURROGATE-01 — fail-closed diagnostic hardening

An unpaired surrogate makes the canonical serializer raise `UnicodeEncodeError`. Because that exception is a `ValueError`, `validate_path` catches it at projection hashing, substitutes an empty expected hash, and rejects the record through `candidate-projection-mismatch`; it does not crash or accept. A successor should reject surrogates explicitly in the canonical-domain walk and return a specific issue rather than relying on downstream encoding failure.

### GATE-SCHEMA-NA-01 — two-layer Observation

The JSON Schema alone accepts `not-applicable` on a universally applicable gate when `admission_pass=false`. The external semantic validator derives the correct applicability and rejects it. This is not a full-interface bypass, but schema-only consumers do not obtain `GateAssignmentConformant`; either tighten the conditional schema or document that this property belongs exclusively to semantic validation.

## Positive scoped findings retained

- Both published `PROV-DERIVE-01` regressions are genuinely closed under valid signatures.
- Producer-string-only, signer/public-key, and authenticity-receipt transplant probes are rejected.
- `validate_path` and `ArtifactIndex` use single immutable byte snapshots in the probed path/artifact cases.
- Missing transitive refs fail closed; known malformed envelopes fail; unknown envelope specs block as unknown; cycle detection terminates in the synthetic fixed-point model.
- `\n` and `\u000a` canonicalize identically; NFD, floats, and out-of-range integers are rejected.
- The fixed SAT and UNSAT records validate end to end; tampered answers fail both independent oracle and transition execution.
- All 18 direct gate mutations and the tested admission/final/applicability contradictions are rejected by schema and/or semantic validation.

These findings retain their narrow scope: Ed25519 test-key authenticity means signer attestation, and signed raw measurements remain attestations rather than independently reconstructed measurements.

## Reproduction

Run:

```powershell
$env:PYTHONUTF8='1'
python .\outputs\v021_bounded_redteam_revalidation.py
```

Expected script result: exit code `0`, `probe_count=15`, `unexpected_probe_results=[]`, and overall disposition `FAIL / REF-TYPE-01`.

Probe script SHA-256:

```text
5B22DB0A9B77E3502281EABF351CEC2644F97D3659A54E38FBA69738F9AA1F73
```

## Limits

- The cycle probe uses an abstract content store to test traversal termination. Constructing a real mutually self-referential SHA-256 artifact pair would require a cryptographic fixed point and is not claimed.
- This audit does not validate a later candidate version and does not authorize promotion, repository success, or Board success.
- No statement in this report is evidence for either `P=NP` or `P≠NP`.
