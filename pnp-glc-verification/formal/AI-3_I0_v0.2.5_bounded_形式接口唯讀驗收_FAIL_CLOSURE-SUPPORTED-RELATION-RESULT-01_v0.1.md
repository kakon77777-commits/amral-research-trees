# AI-3 I0 v0.2.5 bounded 形式／介面唯讀驗收

## Disposition

**FAIL / CLOSURE-SUPPORTED-RELATION-RESULT-01**

Frozen v0.2.5 已在本次 bounded scope 內封閉 v0.2.4 的兩項原 blocker：

- `CLOSURE-JUDGMENT-COMPLETENESS-01` 的未定義符號／依賴圖部分：**CLOSED/PASS**；六個 judgment 均存在，四條 symbolic dependency 全為 fully-qualified、全可解析，圖為有限 DAG。
- `ADVICE-DECL-LEDGER-01`：**CLOSED/PASS**；自由文字已換成 typed `advice_mode`，SchemaConsistency 與 SemanticValidate 分別封閉 record 內部一致性及 family/mechanism 對應。

但 frozen normative `judgments.SupportedEdgeRelation` 只有適用條件、依賴與 predicate，沒有 predicate=false 的 terminal result，也沒有 predicate=true 的 success／traversal transition。由於同一 spec 的 `normative_precedence` 明定完整規範分類圖就是 `judgments`，且頂層 `closure_algorithm`／`envelope_classification_order` 僅是無獨立規範力的 derived views，不能用頂層 prose 補入缺失結果。因此 supported-header 分支仍不是 total、唯一且終態封閉的形式 judgment。

這是 **Definition/interface terminal-totality blocker**，不是 executable acceptance bypass：bundled classifier 對 invalid supported relation 仍回 FAIL，對 valid supported relation 仍能繼續；FAIL disposition 不外推為 correctness、P/NP 或一般 soundness/completeness 結論。

## 1. Scope、版本與唯讀方法

- Role：AI-3 Formalizer
- Date：2026-08-09 Asia/Taipei
- Candidate status：`CANDIDATE_UNPROMOTED`
- Frozen root：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- Manifest：`SHA256SUMS-v0.2.5-candidate.txt`
- 本次只以 manifest 內 166 paths 作 identity／前後 snapshot；未以 shared root 全目錄差異作 provenance 判定。
- 未修改 candidate root；未重跑完整工程 tests、全 fixture regeneration 或 live report。
- disposition-decisive checks 僅包括：manifest/core identity、normative graph 靜態核讀、typed advice schema/validator 靜態核讀，以及兩支既有 bounded reproducer。

## 2. Exact-bytes identity — Observation

| 項目 | 唯讀核得值 | 結果 |
|---|---|---|
| manifest SHA256 | `9D759DB19360E9716E372B7791C251626F658E5C4A185A297EEF6EA01DE9531E` | exact |
| manifest entries | `166` | exact |
| format / missing / mismatch / duplicate | `0 / 0 / 0 / 0` | PASS |
| manifest-path-set 起始 snapshot | `805E50203A1B27D03DD567FBDEDE785A6FD33F62BEC8487A6F90D8833B77E184` | recorded |
| schema SHA256 | `8A799A869CF6CDD17D1191A9D859AB25899FF9E651B454725814E4B458B92596` | exact |
| validator SHA256 | `2571B418612414948A80967B868B910B3714D1FB63F3C79387BF77EC5CA71C5A` | exact |
| closure spec SHA256 | `DFC5A11CF6296F4D83B054B7F4F903E509B0982F9C61D231D423E7F78B5FF71D` | exact |

完成核讀後，以同一 manifest 順序及 `path|length|LastWriteTimeUtc ticks|SHA-256` material 重算，終止 snapshot 仍為 `805E50203A1B27D03DD567FBDEDE785A6FD33F62BEC8487A6F90D8833B77E184`；166 paths 的 content hash、length、mtime 均無變化，`candidate_root_writes_by_AI3=0`（限 manifest domain）。

Identity PASS 只證明本報告核讀的 bytes 與 freeze identity 相符，不等於介面 promotion PASS。

## 3. Normative classification graph

### 3.1 已封閉部分 — Definition/interface PASS

Frozen closure spec 的 `judgments` 恰含：

1. `judgments.GenericEdgeShape`
2. `judgments.GenericEnvelopeShape`
3. `judgments.OpaqueLeaf`
4. `judgments.SupportedEnvelopeHeader`
5. `judgments.SupportedEdgeRelation`
6. `judgments.UnsupportedEnvelope`

解析所得 dependency edges 為：

- `judgments.GenericEnvelopeShape → judgments.GenericEdgeShape`
- `judgments.SupportedEnvelopeHeader → judgments.GenericEnvelopeShape`
- `judgments.SupportedEdgeRelation → judgments.SupportedEnvelopeHeader`
- `judgments.UnsupportedEnvelope → judgments.GenericEnvelopeShape`

所有 symbolic dependency 都以 `judgments.<name>` fully qualified，皆解析到同一 `judgments` object；無 dangling reference、無 cycle。定義域／分支順序亦足以得到：

- 無 `artifact_envelope`：`OpaqueLeaf`，不 traverse；
- 有 envelope 且 generic shape 為 false：`Malformed / FAIL / do not traverse`；
- generic shape 為 true 且 `spec_id` unsupported：`Unsupported / UNKNOWN / do not traverse`；
- supported `spec_id`：先判 `SupportedEnvelopeHeader`；header=false 時明定 FAIL，header=true 時進入 `SupportedEdgeRelation`。

因此 v0.2.4 的 `GenericEnvelopeShape` 未定義問題，以及 generic malformed 與 opaque-leaf 的分支缺口，已在 exact frozen bytes 中修正。

### 3.2 新 blocker — Counterexample to terminal totality

`judgments.SupportedEdgeRelation` 的 frozen fields 只有：

- `applicable_iff`
- `depends_on`
- `not_applicable_when`
- `predicate`

它沒有 `false_result`／`failure_result`，也沒有 `true_result`／`success_result`／明確 traversal transition。

取任一 generic shape=true、supported header=true 的 envelope：

- 若 `EDGE_RELATIONS[artifact_type][role] = expected_type` 對某 edge 為 false，normative graph 可求得 predicate=false，卻求不出 `FAIL`、classification 或 no-traverse terminal；
- 若 predicate=true，normative graph亦未明定進入 `Traverse`／繼續 fixed-point closure，或直接得到何種 terminal status。

頂層 derived view 的「traverse only a supported well-typed envelope」可描述 executable 意圖，但 `normative_precedence` 同時明定該 view 沒有獨立規範力。故至少存在兩個未由 normative graph 唯一導出的狀態：

```text
SupportedEnvelopeHeader = true ∧ SupportedEdgeRelation = false → ?
SupportedEnvelopeHeader = true ∧ SupportedEdgeRelation = true  → ?
```

這使「完整 normative classification graph」的自我聲明與實際 outcome dependency closure 不一致，構成 promotion blocker `CLOSURE-SUPPORTED-RELATION-RESULT-01`。

既有 `reproduce_closure_class_v025.py` 的 bounded 執行仍為 20/20 classification、17/17 scope/dependency checks、`unexpected=[]`。它證明 executable 路徑仍 fail closed，也顯示既有 17 checks 只檢查節點／依賴／generic false 等，沒有檢查每個 decision predicate 的 true/false outcome totality。故此 blocker 與 executable CLOSURE-CLASS 修補並不矛盾。

### 3.3 最小規範義務（非 successor 工作授權）

要使本節 PASS，至少須在同一 normative `judgments.SupportedEdgeRelation` 節點明列：

- predicate=false → relation-invalid / `FAIL` / do not traverse；
- predicate=true → relation-valid / `Traverse`（並明示最終 closure 狀態仍依 descendants/fixed point）；
- regression 必須檢查每個可判定 predicate 的真假分支皆具有 terminal result 或唯一 next transition。

本報告只記錄義務，不建立、修改或驗收任何 successor。

## 4. Typed advice 與 ExpectedAdviceDecl

### 4.1 SchemaConsistency — PASS in bounded transport scope

Schema 已移除 free-text `mechanism.admissibility.advice`，改為 required enum：

- `none`
- `per-input-length-truth-table`

內部 conditional constraints 為雙向分型：

- `none` 要求 generator=null、declared access=`none`、uniform=true、量詞為 `exists-one-program-for-all-input-lengths`，且 advice/generated-table bytes 與 generation time/space/output 全為 0、observed access=`none`；
- `per-input-length-truth-table` 要求 non-null hash-shaped generator ref、declared/observed access=`truth-table`、uniform=false、量詞為 `for-all-lengths-exists-program`，且相關 ledger/generation quantities 為正值；exact pinned generator 身分留給 SemanticValidate 判定。

因此 record 自身把 mode 改成 table 卻留 null/zero，或改成 none 卻留 table/positive，均在 SchemaConsistency 層拒絕。

### 4.2 SemanticValidate — PASS over the stated supported I0 domain

`_expected_advice_declaration(family, mechanism_id)` 對 frozen validator 聲明支援的三個 context 是 deterministic/unique：

| family / mechanism | Expected mode | uniform / quantifier | generator / access | resource profile |
|---|---|---|---|---|
| PARITY / `parity-stream` | `none` | true / `∃ one program ∀ lengths` | null / none | zero |
| 2-SAT / `2sat-kosaraju` | `none` | true / `∃ one program ∀ lengths` | null / none | zero |
| PARITY / `parity-table-family` | `per-input-length-truth-table` | false / `∀ lengths ∃ program` | pinned rule hash / truth-table | materialized table |

其他 pair 回傳無 expected declaration，`_advice_declaration_matches` 因而 false，而不是任意採用某一模式；所以映射只在明列 supported I0 domain 上 total，在全字串 product 上是 fail-closed partial。這個適用域限制是清楚且沒有造成多值。

`_advice_declaration_matches` exact-compare mode、uniformity、quantifier、normalized generator ref、declared access、trace observed access；再依 profile exact/inequality 核 ledger：

- zero：advice bytes、generated tables、generation time/peak space/peak output 全等於 0；
- table：advice 與 generated-table bytes 等於從 input bits 導出的 truth-table bytes，generation time > 0、peak space ≥ table bytes、peak output = table bytes。

不符會形成 `advice-declaration-ledger-binding` issue 並 fail closed。這是 evidence-aware SemanticValidate，不只是 schema prose。

既有 `reproduce_advice_decl_ledger_v025.py` bounded 執行為 4 個 contradiction negatives 全拒、3 個 streaming controls 接受、table binding control 成立、`unexpected=[]`：兩個 record-internal 矛盾由 SchemaConsistency 擋下；兩個 schema-coherent 但 family/mechanism 錯配由 SemanticValidate 擋下。故 `ADVICE-DECL-LEDGER-01` 在本範圍 CLOSED/PASS。

## 5. Judgment-layer separation

| 層 | 本次判定 | 不可替代的義務 |
|---|---|---|
| Definition/interface completeness | **FAIL** | normative graph 本身必須對所有適用分支給唯一 result 或 next transition；executable 行為不能補寫缺少的 normative edge |
| SchemaConsistency(record) | PASS for typed advice internal constraints | 只封閉已寫入 record 的結構與條件式，不證 family/mechanism 語義 |
| SemanticValidate(evidence, record) | PASS for stated advice contexts and targeted witnesses | 以 trace、derived expected declaration、resource fold 判 constituent facts；不修復 closure spec 的定義缺口 |

所以 executable classifier fail closed、admission 未被繞過，仍不足以將一個自稱完整卻 outcome-partial 的 normative interface promotion 為 PASS。

## 6. Final bounded disposition

**FAIL / CLOSURE-SUPPORTED-RELATION-RESULT-01**

- New executable/admission blocker found：none in reviewed checks。
- New Definition/interface blocker：one，為 supported relation 的真假結果／轉移未規範化。
- v0.2.5 保持 frozen、read-only、`CANDIDATE_UNPROMOTED`。
- 本報告不宣稱完整工程驗收、一般 soundness/completeness、Board 採納、shared-repo promotion 或任何 P/NP 結論。
