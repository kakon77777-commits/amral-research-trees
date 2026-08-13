# I0 v0.2.5 candidate validation report

## Disposition

本地 disposition：`SELF-TEST PASS / CANDIDATE_UNPROMOTED`。

協作 disposition：`PENDING AI-1 MANAGED BOUNDED ACCEPTANCE`。

本報告不授權 promotion、successor、共享 repo、Board success 或 P/NP 結論。

## Environment

- CPython 3.14.5
- jsonschema 4.26.0 / Draft 2020-12 + FormatChecker
- cryptography 49.0.0 / Ed25519 test-fixture signatures
- Windows 10.0.19045；fixed seed `20260809`

## Commands

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONPATH=(Resolve-Path src)
python -m unittest discover -s tests
python -m unittest discover -s tests_v021
python -m unittest discover -s tests_v022
python -m unittest discover -s tests_v023
python -m unittest discover -s tests_v024
python -m unittest discover -s tests_v025
python scripts/reproduce_closure_class_v025.py .
python scripts/reproduce_advice_decl_ledger_v025.py .
python scripts/reproduce_oracle_decl_family_v025.py .
python -m pnp_glc_i0.experiment_v025 --project-root . --output i0-run-report.v0.2.5-candidate.json --seed 20260809 --max-parity-n 12
```

觀察：96/96 tests PASS；20/20 closure classifications；17/17 dependency/scope checks；4/4 advice negatives與3/3 none-advice controls符合；retained oracle 9/9 negatives與3/3 controls符合；46-fixture manifest 0 mismatch；149 fixture/artifact outputs立即重產 149/149 byte-identical；live report保留 2-SAT 1500 fixed-seed exhaustive cases PASS。

## CLOSURE-JUDGMENT-COMPLETENESS-01 result

- normative `judgments` 現含完整 generic envelope與opaque leaf分類；
- 所有 judgment以 structured `depends_on` 宣告依賴；
- refs必須 fully-qualified且 target存在；
- GenericEnvelope false明定 Malformed/FAIL/no traversal；
- 既有 malformed→FAIL、complete unsupported→UNKNOWN與supported relation分類不變。

## ADVICE-DECL-LEDGER-01 result

- free-text advice欄位不再被 schema接受；
- legitimate streaming PARITY與2-SAT均為 `advice_mode=none`，外部 binding PASS且 records accepted；
- table declaration配 null generator／none access／zero ledger由 schema拒絕；
- 即使把全部 table或none欄位改成內部一致但與 mechanism context相反，external validator仍以 `advice-declaration-ledger-binding`拒絕。

## 保留的核心回歸

CLOSURE-CLASS、CLOSURE-EDGE-SCOPE、ORACLE-DECL-FAMILY、PROV-DERIVE、REF-TYPE、schema snapshot、canonical/raw domain、trace authenticity、resource account、GateVal applicability與 Admission/Final implications持續通過本輪有界測試。

## 資源帳與失敗前沿

run record保存 time、space、construction、update、decode、lift、verify、restart、parallel、precision、description/advice/proof/output bytes、resource account、semantic-loss debt及failure-frontier axes；resource-neutral仍須完整記帳。

validator是 bounded executable interface，不是 proof-assistant kernel或 universal interpreter；robust只覆蓋 pinned finite deterministic singleton；test signer不等於 production measurement authority；2-SAT不代表 general 3-SAT/CDCL。實驗加速不等於P=NP，實驗失敗不等於P≠NP。live report含實測時間，因此只凍結本次 bytes，不宣稱跨執行 byte-identical。
