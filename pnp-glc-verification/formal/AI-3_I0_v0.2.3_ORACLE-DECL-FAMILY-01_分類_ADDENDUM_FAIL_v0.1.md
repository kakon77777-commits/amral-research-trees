# AI-3 v0.2.3 ORACLE-DECL-FAMILY-01 分類 addendum

- 審查者：AI-3 / Codex-GLC-Formalizer
- 日期：2026-08-09（Asia/Taipei）
- 對象：frozen v0.2.3 exact bytes；candidate root 未修改
- 分類：**FAIL / ORACLE-DECL-FAMILY-01**
- 身分：Counterexample to accepted-record declaration/provenance binding
- 非屬：correctness/oracle-execution bypass、signature bypass、closure bypass、P/NP 結論
- 與既有 blocker 關係：獨立於 `CLOSURE-EDGE-SCOPE-01`

## 1. 結論

AI-2 的隔離副本實驗顯示：將 accepted PARITY record 的 `mechanism.oracle` 宣告替換為 2-SAT SAT 宣告，並合法更新 candidate projection、trace、operational map、signature/auth 與 closure 後，frozen v0.2.3 validator 仍回傳：

```text
schema_valid = true
signature = pass
closure = pass
structural_ok = true
semantic_ok = true
admission_pass = true
final_completion = true
record_accepted = true
issues = []
```

AI-3 對 exact source/schema/artifacts 的靜態資料流核讀確認此接受路徑：validator 的 family-specific oracle execution 由 `problem.family` 選擇，因此仍實際執行 PARITY oracle；但 `mechanism.oracle.name/checks` 沒有進入任何 family/mechanism/result binding judgment。

所以本案例沒有讓錯誤答案通過；它讓一個已接受 record 同時聲稱「PARITY problem」與「oracle checks assignment」。這違反 frozen candidate 對 family-bound oracle provenance/declaration 的明示範圍。

## 2. 最小替換

基底：`fixtures-v0.2.3/legit.json`。

保留：

```text
problem.family = PARITY
mechanism.id = parity-stream
candidate_result.status = complete
oracle.sha256 = sha256:c8c5f6a0c132b11c56fd7964b737c1eb4f0b6a8674c7de8adcda50ca4b54efce
oracle.independent = true
oracle.version = 0.2.3
```

只在語義宣告上替換成 2-SAT SAT：

```json
{
  "name": "independent 2-SAT certificate oracle",
  "checks": ["assignment"],
  "independent": true,
  "version": "0.2.3",
  "sha256": "sha256:c8c5f6a0c132b11c56fd7964b737c1eb4f0b6a8674c7de8adcda50ca4b54efce"
}
```

兩族共用同一 `oracles.py` source hash，所以 hash-only operational role binding 無法識別被宣告的 family entrypoint／obligation。

## 3. 為何 `name/checks` 不是可默認忽略的自由 annotation

1. run-record schema 將 `name`、`checks`、`version`、`independent`、`sha256` 全列為 required；`name/checks` 沒有 nonnormative、display-only 或 annotation 標記。
2. `checks` 的值直接聲稱 oracle 驗證的義務；`assignment`、`mutual implication paths`、`answer/prefix invariant` 不是等價描述。
3. `mechanism.oracle` 位於 candidate projection，會被 projection hash／trace signature 覆蓋。簽章證明 bytes 完整，不能證明宣告為真。
4. frozen `i0-run-report.v0.2.3-candidate.json` 的 candidate scope 明列 `family_bound_contract_oracle_rule_invariant=true`。
5. 先前 frozen interface 文件亦將 contract/oracle/rule/invariant 描述為綁定 problem family／mechanism。

即使後繼版本決定把 `name` 明示為 display annotation，`checks` 仍是具有可驗證真值的語義宣告。本反例因此至少對 `checks` 構成實質 acceptance blocker；不能只以「name 可能是 metadata」降級。

## 4. Exact validator dependency audit

目前欄位使用如下：

| Judgment | 讀取 oracle 欄位 | 未讀取欄位 |
|---|---|---|
| schema consistency | name/checks 的存在、字串／陣列 shape | family-specific exact values |
| actual operational role map | `sha256` | name/checks |
| expected operational role map | 共用 pinned `oracles.py` hash | family entrypoint/name/checks |
| declaration checks | `version`、`independent` | name/checks |
| independent oracle execution | `sha256`；再由 `problem.family` 與 result status dispatch | name/checks |
| family context | problem size、failure frontier、answer access | name/checks |

因此對任一已接受 record `r`，若 `r'` 只改 oracle name/checks，並合法重建 projection/signature/closure：

```text
SchemaConsistency(r')          = SchemaConsistency(r)
OperationalHashBinding(r')     = OperationalHashBinding(r)
OracleExecution(r')            = OracleExecution(r)
FamilyContext(r')              = FamilyContext(r)
OracleDeclarationConform(r')    = unchecked
```

AI-2 的 valid-signature 實驗提供了這個存在性 witness。

## 5. 精確 epistemic classification

- **Counterexample**：對「accepted record 的 oracle declaration 已 family-bound」之 claim。
- **Acceptance blocker**：`semantic_ok=true` 與 `record_accepted=true` 仍可伴隨跨族 oracle declaration。
- **Not a correctness bypass**：PARITY 答案仍由 `parity_oracle` 依 `problem.family` 重算。
- **Not a signature bypass**：實驗使用合法 fixture signature；問題正是簽章後仍缺 semantic binding。
- **Not a schema-only defect**：schema 可以加速拒絕，但 external `SemanticValidate` 必須獨立導出並核對宣告。
- **No P/NP implication**：不改變任何 complexity-theoretic 結論。

## 6. 最小後繼修訂

首選是消除自由文字重複宣告，加入可導出的 typed oracle identity：

```text
OracleObligation :=
  parityAnswer
  | parityPrefixInvariant
  | twoSatAssignment
  | twoSatMutualImplicationPaths.

ExpectedOracleDecl(family, mechanism, resultStatus) :=
  (PARITY, parity-stream, complete)
    ↦ (oracleId=I0-PARITY,
       obligations={parityAnswer, parityPrefixInvariant})

  (2-SAT, 2sat-kosaraju, sat)
    ↦ (oracleId=I0-2SAT-SAT,
       obligations={twoSatAssignment})

  (2-SAT, 2sat-kosaraju, unsat)
    ↦ (oracleId=I0-2SAT-UNSAT,
       obligations={twoSatMutualImplicationPaths}).
```

外部 validator 應加入：

```text
OracleDeclarationConform(record) :=
  record.mechanism.oracle.oracle_id
    = ExpectedOracleDecl(context).oracleId
  ∧ record.mechanism.oracle.checks
    = ExpectedOracleDecl(context).obligations
  ∧ record.mechanism.oracle.entrypoint/source binding
    matches the dispatched executable oracle.
```

實作選項：

- 仍可共用單一 `oracles.py` source hash，但要另 pin `oracle_id`／entrypoint／obligation set；或
- 拆成 family-specific oracle artifacts／wrappers，使 operational role hash 自身即可區分 family；或
- 完全移除可導出的 `checks` 自報欄位，由 validator 產生 derived receipt。

若 `name` 要保留為 nonnormative display text，必須在新版本 schema/spec 明示並移入 annotation namespace；不得默默改變 frozen v0.2.3 的解讀。

## 7. 必加 negative fixtures

至少加入有效簽章且 projection/closure 全部一致的：

1. PARITY declaration → 2-SAT SAT name/checks；
2. PARITY declaration → 2-SAT UNSAT checks；
3. 2-SAT SAT → PARITY checks；
4. 2-SAT UNSAT → SAT assignment checks；
5. name-only swap；
6. checks-only swap；
7. correct source hash but wrong `oracle_id`／entrypoint。

每例應保持實際答案／certificate 正確，以隔離測得 declaration binding；預期為 structural-valid、signature PASS、oracle execution PASS，但 `SemanticValidate=false`、`record_accepted=false`，並產生專用 issue code，例如 `oracle-declaration-family-binding`。

## 8. 整合 disposition

Frozen v0.2.3 的目前 formal/interface blockers 至少包括：

```text
CLOSURE-EDGE-SCOPE-01
ORACLE-DECL-FAMILY-01
```

既有 executable、gate、resource、REF-TYPE、PROV-DERIVE 與 oracle correctness positives仍可保留為 scoped evidence；不能抵銷 accepted declaration mismatch。v0.2.3 應保持 frozen `CANDIDATE_UNPROMOTED`，修正另起後繼 exact bytes，再做 AI-1/AI-2/AI-3 唯讀驗收。
