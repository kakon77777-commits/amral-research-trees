# Run-record v0.1 -> v0.2 candidate semantic-hardening diff

Epistemic status: **Definition/interface candidate**. v0.1 remains valid as a Draft 2020-12 structural transport schema. The counterexamples below target schema-alone sufficiency, not that structural validity.

## Preserved

- v0.1 is not overwritten; canonical SHA-256 remains `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4`.
- Source/provenance, claim labels, problem family, mechanism, event stream, full cost ledger, semantic-loss debt and failure-frontier records remain.
- JSON Schema and external semantic validation remain different judgments.

## Structural changes

1. Schema/version id moves to candidate `0.2.0`.
2. `result` becomes `candidate_result`; it cannot contain `admission_pass`, `final_completion` or the validation receipt.
3. `admission_validation` and `completion_validation` are replaced by one external `validation_receipt`.
4. Receipt bindings include schema, validator, projection spec, candidate projection, trace and exact resolved-evidence hashes.
5. Boolean component gates become `GateResult = pass | fail | unknown | not-applicable`.
6. `PARITY` is an explicit problem family and program quantifiers use a controlled enum.
7. Certificate and event rule/invariant refs are content-addressed hashes.

## One-way schema implications

- robust -> maximal/fairness refs are non-null hashes; standard -> refs null and gates N/A;
- resource-neutral -> budget gate/check N/A; resource-bounded -> applicable gate/check;
- admission true -> every applicable run/provenance/resource gate passes, with resource account complete in every quadrant;
- final true -> admission, oracle, contract, completeness and resource-account pass; zero ledger/receipt debt; terminal status is `sat|unsat|complete`; bounded additionally requires budget pass;
- advice/proof gates may be N/A only when their generators/artifacts are absent.

No inverse implication is present. In particular, declarations that all gates pass do not force schema-level admission or completion. The external validator derives and compares both aggregates.

## External validator obligations added

- strict duplicate-key parsing and a versioned canonical projection domain;
- actual SHA-256 recomputation and content resolution;
- exact receipt evidence-set binding;
- trace/run/gate/projection binding;
- replay of events, terminal output, certificates, resource folds and debt folds;
- applicable-gate derivation with `unknown` distinct from `fail`;
- independent PARITY and 2-SAT correctness checks;
- exact admission and final-completion postcondition comparison.

## Counterexample-to-obligation mapping

| Counterexample / fixture | v0.2 enforcement |
|---|---|
| candidate self-report | candidate-result `additionalProperties=false` |
| robust null specs | schema robust conditional |
| failed component gate + admission true | schema admission conditional |
| false correctness/budget/account/debt + final true | schema final conditional |
| unknown/timeout/error + final true | schema terminal-status conditional |
| tampered record | projection recomputation + replay |
| tampered trace with a resolvable new hash | DerivesRecord replay mismatch |
| circular validation field | candidate/receipt separation |
| Unicode canonicalization variant | projection-spec NFC check |

These are engineering counterexamples and tests, not P/NP results.
