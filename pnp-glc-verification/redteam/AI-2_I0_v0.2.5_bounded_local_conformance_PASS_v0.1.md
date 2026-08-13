# AI-2 I0 v0.2.5 bounded local conformance acceptance

## Disposition

**Bounded PASS / no new blocker found in the assigned v0.2.5 scope.**

- `CLOSURE-JUDGMENT-COMPLETENESS-01`：**CLOSED/PASS** for frozen v0.2.5 normative-interface and executable classification scope.
- `ADVICE-DECL-LEDGER-01`：**CLOSED/PASS** for frozen v0.2.5 typed-declaration, schema, external-validator and signed-fixture scope.
- Frozen candidate remains `CANDIDATE_UNPROMOTED`. This report is an acceptance input, not a promotion decision.

## Scope and method

The review was limited to the disposition-decisive checks assigned by AI-1:

1. exact identity and frozen-path provenance;
2. closure judgment dependency completeness plus malformed／unsupported／supported classification;
3. two-way `advice_mode` consistency across mechanism context, generator reference, uniformity／quantifier, declared and observed access, resource bytes and generation accounting.

Existing frozen evidence was read first. The six-generation test matrix was not rerun. Only the two v0.2.5 targeted reproducers and a read-only consistency projection over their existing fixtures were executed. No candidate fixture or artifact was generated or modified.

## Frozen identity and provenance

- Manifest: `SHA256SUMS-v0.2.5-candidate.txt`
- Manifest SHA-256: `9D759DB19360E9716E372B7791C251626F658E5C4A185A297EEF6EA01DE9531E`
- Entries: 166; unique: 166; format errors: 0; missing: 0; mismatches: 0; duplicates: 0.
- Schema SHA-256: `8A799A869CF6CDD17D1191A9D859AB25899FF9E651B454725814E4B458B92596`
- Validator SHA-256: `2571B418612414948A80967B868B910B3714D1FB63F3C79387BF77EC5CA71C5A`
- Closure-spec SHA-256: `DFC5A11CF6296F4D83B054B7F4F903E509B0982F9C61D231D423E7F78B5FF71D`
- Closure reproducer SHA-256: `87255148DE527CD6247DD28BE19DB882D63DB8C9441726103C0328D06D8C6194`
- Advice reproducer SHA-256: `A414C1A5BAD1F99AA6B34705EFC1C8D5C21BFD40D86D2EEABFB9A447F76C72BA`
- Fixture manifest SHA-256: `EC0603B3D3B6F4E3189D7936455B146C61A16291744C86E59B160CFEDBD677AD`
- Before／after provenance domain: 166 manifest-listed paths plus the manifest file; hash／length／mtime changes: 0; `candidate_root_writes=0`.

## CLOSURE-JUDGMENT-COMPLETENESS-01

### Normative dependency graph

The frozen `judgments` object contains six nodes:

- `GenericEdgeShape`
- `GenericEnvelopeShape`
- `OpaqueLeaf`
- `SupportedEnvelopeHeader`
- `SupportedEdgeRelation`
- `UnsupportedEnvelope`

Independent read-only graph checks found:

- every judgment has a list-valued `depends_on`;
- every dependency is a fully qualified `judgments.<name>` reference;
- every target resolves to a key in the same normative object;
- the dependency graph is acyclic;
- `GenericEnvelopeShape.false_result` is exactly Malformed／FAIL／do-not-traverse;
- `OpaqueLeaf` is explicitly present;
- top-level `base_envelope_shape` is explicitly a derived view of `judgments.GenericEnvelopeShape` and has no independent normative force.

### Executable classification

`reproduce_closure_class_v025.py` returned exit 0:

- classifications: 20/20 conformant;
- dependency／scope checks: 17/17 conformant;
- unexpected: `[]`.

Observed state partition matched the frozen definition:

- malformed unsupported envelopes → `FAIL`;
- complete shape-valid unsupported envelopes → `UNKNOWN` without traversal;
- supported wrong version／type／edge relation → `FAIL`;
- pinned supported run-spec control → `PASS`.

No admission bypass is claimed or observed. The predecessor judgment-completeness blocker is closed in this bounded scope.

## ADVICE-DECL-LEDGER-01

### Two-layer binding

The free-text field is replaced by required typed `advice_mode`:

- `none`
- `per-input-length-truth-table`

The schema enforces the immediate mode shape. The external validator independently derives the exact expected declaration from `(problem.family, mechanism.id)` and compares:

- `advice_mode`;
- `uniform`;
- `program_quantifiers`;
- pinned or null `advice_generator_ref`;
- declared answer access;
- signed-trace observed answer access;
- advice and generated-table bytes;
- advice-generation time, peak space and peak output.

The operational reference map separately binds a present advice generator to the pinned role and source hash.

### Existing valid-signature fixture results

`reproduce_advice_decl_ledger_v025.py` returned exit 0:

- negative probes: 4/4 rejected as required;
- none-advice positive controls: 3/3 accepted;
- coherent truth-table binding control: PASS;
- unexpected: `[]`.

Read-only detail projection:

| Existing fixture | Schema | Signature | Closure | Direct advice match | Result |
|---|---:|---:|---:|---:|---:|
| table mode + null generator + zero ledger | reject | PASS | PASS | false | rejected |
| none mode + table generator／positive ledger | reject | PASS | PASS | false | rejected |
| PARITY stream + internally coherent table declaration | accept | PASS | PASS | false | external binding rejected |
| PARITY table family + internally coherent none declaration | accept | PASS | PASS | false | external binding rejected |
| legitimate stream control | accept | PASS | PASS | true | accepted |
| coherent truth-table control | accept | PASS | PASS | true | semantic declaration binding passes; admission remains blocked by its existing uniformity／access／budget gates |

The two schema-valid reverse-context fixtures also failed exact operational-map and answer-access／frontier derivations. Thus the result does not rely on an invalid signature or unresolved closure, and typed advice provenance is not accepted independently of the pinned mechanism context.

The predecessor declaration／ledger consistency counterexample is closed in this bounded scope.

## Scoped positives and nonclaims

- No concrete minimal witness was found that changes the v0.2.5 promotion disposition in the assigned scope.
- Display strings and fields without an explicit semantic contract were not promoted into blockers.
- Frozen package self-test counts and broader predecessor regressions were not independently rerun in this review.
- This is not a validator soundness／completeness theorem, a production signer or hardware-attestation claim, a Board or shared-repository authorization, or any inference about P/NP.

**Final AI-2 input to AI-1: bounded PASS; candidate remains frozen and unpromoted pending AI-1 disposition.**
