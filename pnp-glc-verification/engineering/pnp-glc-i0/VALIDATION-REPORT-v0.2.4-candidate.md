# I0 v0.2.4 candidate validation report

## Disposition

本地 disposition：`SELF-TEST PASS / CANDIDATE_UNPROMOTED`。

協作 disposition：`PENDING AI-1/AI-2/AI-3 FROZEN READ-ONLY ACCEPTANCE`。

本報告不授權 promotion、共享 repo、Board success 或 P/NP 結論。

## Environment

- CPython 3.14.5
- jsonschema 4.26.0 / Draft 2020-12 + FormatChecker
- cryptography 49.0.0 / Ed25519 test-fixture signatures
- Windows 10.0.19045；single worker；fixed seed `20260809`

## Commands

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONPATH=(Resolve-Path src)
python -m unittest discover -s tests
python -m unittest discover -s tests_v021
python -m unittest discover -s tests_v022
python -m unittest discover -s tests_v023
python -m unittest discover -s tests_v024
python scripts/reproduce_closure_class_v024.py .
python scripts/reproduce_oracle_decl_family_v024.py .
python -m pnp_glc_i0.experiment_v024 --project-root . --output i0-run-report.v0.2.4-candidate.json --seed 20260809 --max-parity-n 12
```

觀察：75/75 tests PASS；20/20 closure classifications；7/7 scope checks；9/9 oracle-declaration negative probes與3/3 positive controls符合；42-fixture manifest 0 mismatch；2-SAT 1500 fixed-seed exhaustive cases PASS。137 fixture/artifact outputs立即重產後 137/137 byte-identical。

## CLOSURE-EDGE-SCOPE-01 result

- closure spec有單一 normative precedence；
- generic syntax judgment對所有 envelope 適用；
- supported header先封閉 current spec/version/artifact-type domain；
- current parent-role-child relation僅在 supported header成立時適用；
- complete unsupported envelope唯一為 UNKNOWN、不 traverse；
- future-type witness與三個 supported-header/relation controls形成對照。

## 保留的有限正向觀察

- uniform streaming PARITY 外部 admission=true，prefix invariant實際執行並核對；
- per-length truth-table PARITY答案可正確，但 uniformity/advice/answer-access gates使 admission=false；
- terminal-only projection不能單獨導出 acceptance；
- standard/robust × neutral/bounded gate matrix與 account/budget applicability不變；
- pinned 2-SAT SAT/UNSAT records皆 end-to-end accepted；
- PROV-DERIVE、REF-TYPE、schema snapshot、raw -0、Unicode scalar、trace/auth與operational-map negatives持續拒絕。

## ORACLE-DECL-FAMILY-01 result

- schema要求 `oracle_id/entrypoint/name/checks/obligations/version/independent/sha256`；
- validator從 family/mechanism/result status導出 exact typed declaration；
- 9 個 valid-signature declaration swaps 的 actual family oracle仍 PASS，但全部出現 `oracle-declaration-family-binding` 並拒絕 admission；
- 3 個 legitimate PARITY/2-SAT controls維持 accepted。

## 資源帳與失敗前沿

run record保存 time、space、construction、update、decode、lift、verify、restart、parallel、precision、description/advice/proof/output bytes、resource account、semantic-loss debt及failure-frontier axes。resource-neutral仍須完整記帳。

validator是bounded executable interface，不是proof-assistant kernel或universal interpreter；robust只覆蓋pinned finite deterministic singleton；test signer不等於production measurement authority；2-SAT不代表general 3-SAT/CDCL。實驗加速不等於P=NP，實驗失敗不等於P≠NP。live report含實測時間，因此只凍結本次bytes，不宣稱跨執行byte-identical。
