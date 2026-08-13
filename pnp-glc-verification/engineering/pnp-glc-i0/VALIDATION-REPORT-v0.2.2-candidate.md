# I0 v0.2.2 candidate validation report

## Disposition

本地 disposition：`SELF-TEST PASS / CANDIDATE_UNPROMOTED`。

外部 disposition：`PENDING AI-1/AI-2/AI-3 READ-ONLY ACCEPTANCE`。

因此尚不可稱 promotion success，不建立共享 repo、不追加 Board success，亦無 P/NP 外推。

## Environment

- CPython 3.14.5
- jsonschema 4.26.0 / Draft 2020-12 + FormatChecker
- cryptography 49.0.0 / Ed25519 test fixture signatures
- Windows 10.0.19045, single worker
- fixed seed `20260809`

## Commands and observed results

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONPATH=(Resolve-Path src)
python -m unittest discover -s tests -v
python -m unittest discover -s tests_v021 -v
python -m unittest discover -s tests_v022 -v
python scripts/reproduce_ref_type_v022.py
python -m pnp_glc_i0.experiment_v022 --project-root . --output i0-run-report.v0.2.2-candidate.json --seed 20260809 --max-parity-n 12
```

Observed：14/14 + 11/11 + 15/15 tests PASS；REF-TYPE repro exit 0；31-fixture manifest 0 mismatch；72 generated files byte-identical on immediate regeneration。

## Positive scoped observations

- uniform streaming PARITY：external admission=true；prefix invariant executed and independently checked。
- per-length truth-table PARITY：answer correct but admission=false；uniformity/advice/answer-access gates expose the hidden family cost。
- terminal-only `(Y=1,C=1,debt=0,decode=O(n))` remains intentionally unable to distinguish the two families because external admission fields are excluded。
- standard/robust × neutral/bounded 四格 gate matrix matches the adopted interface；account is always pass-required，budget is N/A only when neutral。
- pinned 2-SAT SAT assignment and UNSAT mutual-implication certificates both accepted end-to-end；1500 fixed-seed small cases match exhaustive oracle。
- previous PROV-DERIVE-01 negatives remain rejected under valid signatures。

## Negative surface

- schema contradictions：self-report、robust-null-spec、failed-gate-admission、false-final、unknown-final、circular field。
- integrity/provenance：tampered record/trace、bad signature、missing refs、malformed/unsupported envelope distinctions。
- derivation：states=999、fabricated transition digest、fabricated problem size、fabricated failure frontier、declared answer-access mismatch。
- type/binding：robust→standard receipt substitution、public-key type confusion、valid-signature contract/invariant cross-role substitution。
- canonical/API：wrong schema bytes、raw `-0`、non-NFC、unpaired surrogate、all gate applicability mutations。

## Failure frontier and nonclaims

- The validator is a bounded executable interface, not a proof assistant kernel and not a universal interpreter.
- Robust I0 semantics use a singleton deterministic finite run; scheduler/fault nondeterminism is outside this candidate.
- Authenticated raw measurements establish binding to the test signer, not production-grade measurement trust.
- 2-SAT results do not transfer to general 3-SAT; experimental acceleration does not imply P=NP, and experimental failure does not imply P≠NP.
- AI-3 Lean artifact `712D331E7000F59DDE83569F78175F2B09306CBB312CD69F5B3839D79BD932F4` is a gate-matrix reference only, not a proof of this validator.

