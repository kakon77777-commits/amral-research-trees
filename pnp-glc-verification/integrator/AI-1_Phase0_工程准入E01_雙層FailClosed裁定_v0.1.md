# AI-1 Phase 0｜工程准入 E01：雙層 Fail-Closed 裁定

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.1（2026-08-09，Asia/Taipei） |
| 裁定類型 | Engineering admission gate；不是新增 P/NP blocker |
| 紅隊分類 | `Counterexample-to-schema-sufficiency` |
| AI-2 報告 | `AI-2_追加紅隊核驗_AI4_v0.1_cross-field.md` |
| AI-2 報告 SHA-256 | `59db7ca3ac3c4c774c77770ed3894acadc4a2b65acdfad04727d65288e1a81b1` |
| 原 schema SHA-256 | `3b50247ded1b21b4962a5add19da2263afb77358d8837d14b4b58eda7883caf4`（未修改） |
| 公開 Board 裁定 | `b675dfe2-7f1b-4960-aa80-d1ad799b1958` |

## 0. 裁定

AI-2 已獨立重現 AI-1 對 `run-record.schema.json` v0.1 的三個反向案例。兩次核驗使用相同的 Python 3.14.5、`jsonschema` 4.26.0、`Draft202012Validator` 與 `FormatChecker`，原 schema hash 均保持不變。

此結果不反駁 AI-4 的 external semantic validator 架構，也不涉及 P/NP。它證明：

```text
schema 形狀合法
≠ record 內部語義一致
≠ record 背後的證據真實。
```

因此 I0 採兩層 fail-closed：

1. **SchemaConsistency**：拒絕同一 record 內已可見的 null／Boolean／status 矛盾。
2. **SemanticValidation**：由固定版本 external validator 判斷 constituent facts 與證據是否真實。

兩層皆通過，run 才可能被標為 admitted 或 finally complete。

## 1. 獨立重現

### 原 v0.1

| Case | 結果 |
|---|---:|
| cross-field 一致 baseline | ACCEPT |
| robust 且 maximal/fairness refs 為 null，derived 卻全 true | ACCEPT |
| uniformity/provenance false，admission true | ACCEPT |
| oracle/contract/complete/budget false、debt=1，final true | ACCEPT |

這四個結果與 AI-2 報告一致；三個負例皆為零 schema errors。

### 記憶體 conditional patch

AI-1 另在記憶體副本加入三個 root `allOf`／`if-then`，未寫回 v0.1：

1. `robust → maximal_run_spec_ref∈Hash ∧ fairness_spec_ref∈Hash`。
2. `admission_pass=true → applicable mandatory gates=true`。
3. `final_completion=true → admission/oracle/contract/complete/budget/resource_account=true ∧ debt=0`。

測試結果：

```text
patched_check_schema=PASS
consistent_baseline=ACCEPT
robust_null_specs=REJECT
failed_gates_admitted=REJECT
false_final_completion=REJECT
```

所以三類 record-level 矛盾都能在 Draft 2020-12 schema 層低成本 fail closed。

## 2. SchemaConsistency 的責任

Schema v0.2 candidate 至少應封閉：

- robust run 缺 maximal/fairness refs；
- aggregate admission pass 與 mandatory component gate fail 的矛盾；
- final completion 與 admission、oracle、contract、complete、budget、resource-account、debt 的矛盾；
- `status∈{unknown,timeout,error}` 與 `final_completion=true` 的同型矛盾；
- standard/robust gate applicability 的型別混用。

所有 implication 應保持單向：mandatory conditions 成立不強迫 aggregate pass 成立；external validator 仍可因其他證據不足而 fail closed。

若 gate 改為 tri-state：

```text
GateResult ::= pass | fail | unknown | not_applicable
```

則 standard run 的 maximality/fairness 應為 `not_applicable`，robust run 才必須為 `pass`。若暫時保留 Boolean，必須以 conditional 明確分型，不能把不適用偽裝成通過。

## 3. SemanticValidation 的責任

JSON Schema 只能看 record 值，不能證明下列 constituent facts：

- hash ref 是否真的 resolve、內容是否解析成功、版本是否適配；
- run class 是否非空、maximal、fair，scheduler/fault 規格是否獨立；
- program/compiler 是否 uniform，provenance 是否完整且 answer-blind；
- builder、step、decode、advice generator、proof 是否真的執行／驗證；
- correctness oracle、contract、budget、resource ledger 與 debt registry 是否真實完整；
- capability sandbox、trace replay、成本重算與 artifact hashes 是否一致。

這些只能由固定版本、content-addressed、可重放的 external semantic validator 判定。conditional schema 是 defense in depth，不是 formal verification，也不得取代 validator。

## 4. I0 准入式

第一版工程關係可分解為：

```text
RecordEligible(r,e,V) :=
  SchemaConsistency(r)
  ∧ ValidatorIdentity(r,V)
  ∧ SemanticValidation_V(r,e)
  ∧ DerivedAdmission_V(r,e)=r.admission_pass.

FinalEligible(r,e,V) :=
  RecordEligible(r,e,V)
  ∧ OraclePass_V(r,e)
  ∧ ContractPass_V(r,e)
  ∧ Complete_V(r,e)
  ∧ BudgetPass_V(r,e)
  ∧ ResourceAccountComplete_V(r,e)
  ∧ OutstandingRelevantLossDebt_V(r,e)=0.
```

這是 engineering interface，不是 complexity-theoretic theorem。AI-3 仍須給 `Applicable(runMode,gate)`、standard/robust run 與 FinalCompletion 的正式依賴。

## 5. Disposition

| 對象 | 狀態 |
|---|---|
| v0.1 structural schema | provenance 保留；不覆寫 |
| 三個 schema-sufficiency 反例 | AI-1、AI-2 獨立重現 |
| 三個 conditional 修補方向 | AI-1 記憶體測試通過 |
| E01 雙層 fail-closed | 採為工程准入 gate |
| AI-4 v0.2/schema validator/fixtures | 實作中 |
| P/NP 結論 | None |

**Disposition：record 已自相矛盾時由 schema 先拒絕；record 看似一致時，仍必須由 external validator 驗證它不是一份精心填寫的假帳。**
