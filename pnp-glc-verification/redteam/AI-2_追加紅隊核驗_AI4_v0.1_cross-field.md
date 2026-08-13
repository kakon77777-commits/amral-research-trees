# AI-2 追加紅隊核驗｜AI-4 v0.1 cross-field contradictions

| 欄位 | 結果 |
|---|---|
| 分類 | **Counterexample-to-schema-sufficiency** |
| 適用域 | AI-4 `run-record.schema.json` v0.1 的 Draft 2020-12 schema-only acceptance |
| 不適用域 | 不反駁 external semantic validator 架構；不涉及、更不外推 P/NP |
| 原始 schema SHA-256 | `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4` |
| 原始檔處置 | 唯讀；未修改；核驗前後 hash 相同 |
| 重現環境 | Python 3.14.5；`jsonschema` 4.26.0；`Draft202012Validator` + `FormatChecker` |
| 重現腳本 SHA-256 | `b7b8dde5e48b3d7d452ee1193b3db955b9c33ac857d0e889635abf911535227a` |

## 裁定

AI-1 的三項反向測試全部獨立重現。原 v0.1 schema 通過 metaschema check；一筆 cross-field 一致的 baseline 被接受。對 baseline 只作指定欄位變更後，三筆矛盾 record 仍全部得到零個 schema error。

這構成對下列命題的反例：

> 「通過 v0.1 JSON Schema 足以排除文件已明定的 cross-field 矛盾。」

它**不是**對完整工程架構的反例，因為 AI-4 章程已明說 JSON Schema 只驗形狀，跨欄一致性由 external semantic validator 執行。真正的新裁定是：三種表面矛盾皆能、也應以低成本 Draft 2020-12 conditionals 在 schema 層 fail closed；underlying evidence 的真實性仍只能由 external validator 判定。

## 重現結果

| Case | 相對於合法 baseline 的唯一關鍵變更 | 原 v0.1 | 記錄層矛盾 |
|---|---|---:|---|
| baseline | `robust` refs 非 null；所有 mandatory gate true；final components true、debt=0 | ACCEPT | 無 |
| (a) robust missing specs | `maximal_run_spec_ref=null`、`fairness_spec_ref=null`；derived 仍全 true | **ACCEPT** | robust run 缺 maximal/fairness spec |
| (b) failed gates admitted | `uniformity_pass=false`、`provenance_pass=false`；`admission_pass=true` | **ACCEPT** | aggregate pass 與 constituent gates 衝突 |
| (c) failed result completed | oracle/contract/complete/budget 均 false、debt=1；`final_completion=true` | **ACCEPT** | final completion 與其明定必要條件衝突 |

另外在記憶體中的 schema 副本加入三個候選 `if/then` 後重新驗證：baseline 仍 ACCEPT；(a)、(b)、(c) 全部 REJECT。這證明三項**記錄內部矛盾**都可由 Draft 2020-12 表達，不必把這部分留到 semantic validator 才第一次發現。

## 分工判斷

| Case | JSON Schema conditional 應拒絕 | External semantic validator 才能判斷 |
|---|---|---|
| (a) | 若 `mechanism.run_quantifier="robust"`，則 `maximal_run_spec_ref`、`fairness_spec_ref` 必須符合 non-null hash schema | hash 是否能 resolve；內容是否真的定義非空 admissible maximal fair runs；scheduler/fault class 是否獨立且公平 |
| (b) | 若 `derived.admission_pass=true`，所有列為 mandatory 的 derived gates 必須為 true。只要求單向 implication；全 true 不強迫 admission 一定 true | uniformity、provenance、builder、proof、answer access、resource、replay 等 gate 的實際證據是否成立 |
| (c) | 若 `result.final_completion=true`，至少要求 external `admission_pass=true`，且 oracle/contract/complete/budget 均 true、`outstanding_loss_debt=0` | 答案是否真確、contract 是否真滿足、成本是否真在 budget、debt registry 是否完整且證據有效 |

因此，三個 case 沒有任何一個必須「只能」留給 semantic validator 才拒絕；只能留給 validator 的是 constituent facts 的實質判定，而不是已寫入同一 record 的 Boolean／null 自相矛盾。

## 建議的 fail-closed 方向

1. Root `allOf`：`if mechanism.run_quantifier == robust`，`then` 把兩個 nullable refs 收窄為 `$defs.hash`。
2. Root `allOf`：`if admission_validation.derived.admission_pass == true`，`then` mandatory derived gates 全為 `const: true`。
3. Root `allOf`：`if result.final_completion == true`，`then` 跨 `admission_validation` 與 `result` 強制已公布的必要條件。
4. 保持單向 implication：schema 不應因所有 gate 都是 true 就強迫 admission/final completion 為 true；external validator 仍可因未列原因 fail closed。
5. `unknown`、`timeout`、`error` 與 `final_completion=true` 的衝突也是同型、可 schema 化的相鄰 hardening，但不影響本次三例裁定。

## 失敗條件與界線

- 若未來允許某種 `robust` 子型不使用 scheduler fairness，則不能以 null+pass 表示；應增加明確 applicability/submode，而不是放寬上述 implication。
- content-addressed ref 的 non-null 只證明有一個形狀合法的 hash，不證明內容正確；resolve、解析、執行與語義適配仍需 validator。
- JSON Schema conditional 是 defense in depth，不得被稱為 formal verification，也不得取代 replay、sandbox、proof check 或資源重算。

**追加核驗 disposition：完成；Counterexample-to-schema-sufficiency；原 v0.1 provenance 保留。**
