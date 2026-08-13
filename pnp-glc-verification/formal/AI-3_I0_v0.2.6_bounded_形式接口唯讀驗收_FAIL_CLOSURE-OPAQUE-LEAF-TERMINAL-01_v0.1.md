# AI-3 I0 v0.2.6 bounded 形式／介面唯讀驗收

## Disposition

**FAIL / CLOSURE-OPAQUE-LEAF-TERMINAL-01**

在本次指定範圍內：

- `CLOSURE-SUPPORTED-RELATION-RESULT-01`：**CLOSED/PASS（local normative branch）**。`SupportedEdgeRelation` 現有明確 applicability、false terminal、true transition 與 exactly-one totality；true branch 唯一進入 `judgments.SupportedTraversal`。
- v0.2.5 `GenericEnvelopeShape` dependency closure：**retained PASS**。
- v0.2.5 typed advice／`ExpectedAdviceDecl`：**retained PASS**。
- 新發現 `CLOSURE-OPAQUE-LEAF-TERMINAL-01`：**Definition/interface blocker**。`SupportedTraversal.child_dispatch` 規範性地指向 `judgments.OpaqueLeaf`，但 `OpaqueLeaf` 沒有 `gate_result`、`terminal` 或其他把其結果送入 fixed-point PASS/FAIL/UNKNOWN 三分支的規範映射。因此 relation=true 後的 traversal graph 仍不是 outcome-total。

Executable 仍會把符合 `opaque-content` 預期型別的 opaque leaf 視為成功並繼續，既有 closure reproducer 也為全綠；所以本 FAIL 是 normative graph 與 executable 意圖之間的介面缺口，不是 admission bypass、correctness counterexample 或 P/NP 結論。

## 1. Scope 與方法

- Role：AI-3 Formalizer
- Date：2026-08-10 Asia/Taipei
- Candidate：v0.2.6 frozen `CANDIDATE_UNPROMOTED`
- Frozen root：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- Identity domain：只含 `SHA256SUMS-v0.2.6-candidate.txt` 的 216 paths。
- 未修改 candidate；未重跑完整工程 tests、fixture regeneration、runtime closure 或 live-report replay。
- 唯一 executable check：既有 `python -I -B scripts\reproduce_closure_class_v026.py .`；其餘為 exact-byte hash、JSON judgment graph、check source、schema 與 validator 的唯讀核讀。

本報告區分：

1. **Definition/interface completeness**：規範圖自身是否對每個 reachable state 導出唯一 terminal status 或唯一 next transition。
2. **Executable behavior**：validator 在 frozen fixtures 上實際回傳何值。
3. **SchemaConsistency / SemanticValidate**：transport record 內部條件式與 evidence-aware 外部判定；兩者都不能補寫 closure normative graph 缺少的 judgment outcome。

## 2. Exact-bytes identity — PASS

| 項目 | AI-3 唯讀核得值 | 結果 |
|---|---|---|
| manifest SHA256 | `2E1C58A5CE85833DAC708DF21BD4FC4AC845FFC3182AAB16BF568F50AC502357` | exact |
| entries | `216` | exact |
| format / missing / mismatch / duplicate | `0 / 0 / 0 / 0` | PASS |
| schema | `EB22CB899869B2A43DCD2DBBD3F4C9F7C0A8921AE361EF2207DB1039B1C875EE` | exact |
| validator | `3F87207F26A21CA1B750B70170EBE28090F97C0670FB6F0CA88ED04296244D72` | exact |
| closure spec | `B635E86CB5FBDB89865ED4343F052247E98A245DD2194726066AEF01489F758F` | exact |
| runtime descriptor `artifacts-v0.2.6/acceptance-runtime-closure.v0.2.6.json` | `B3019C2C62B2689CF897F787BEAADCEA19663C820DAFBED97B6AE6FC46CF8217` | exact |
| manifest-path-set 起始 snapshot | `11ED2E3D6597C62CF32FA716DDD06EAF109840E05E16349528F19B442778A39D` | recorded |

完成核讀與 bounded reproducer 後，以同一 manifest 順序及 `path|length|LastWriteTimeUtc ticks|SHA-256` material 重算，終止 snapshot 仍為 `11ED2E3D6597C62CF32FA716DDD06EAF109840E05E16349528F19B442778A39D`；216 paths 的 content hash、length、mtime 均無變化，`candidate_root_writes_by_AI3=0`（限 manifest domain）。

Identity PASS 只固定本報告所核讀的 bytes；不等於 formal/interface promotion PASS。

## 3. Normative graph reconstruction

令「outcome-total」表示每個 reachable judgment state 恰有下列之一：

- 一個結構化 terminal result，其 closure status 屬 `{PASS, FAIL, UNKNOWN}`；或
- 一個由 predicate／dispatch rule 唯一決定、fully-qualified 且可解析的 next transition。

### 3.1 Fully-qualified graph

Frozen `judgments` 有七個節點：

1. `judgments.GenericEdgeShape`
2. `judgments.GenericEnvelopeShape`
3. `judgments.OpaqueLeaf`
4. `judgments.SupportedEnvelopeHeader`
5. `judgments.SupportedEdgeRelation`
6. `judgments.SupportedTraversal`
7. `judgments.UnsupportedEnvelope`

五條 `depends_on` 與六條 transition／child-dispatch reference 全以 `judgments.<name>` fully qualified，全部解析到同一 object，沒有 dangling target。核心路徑為：

```text
GenericEnvelopeShape
  ├─ unsupported spec_id → UnsupportedEnvelope → UNKNOWN / no traverse
  └─ supported spec_id   → SupportedEnvelopeHeader
                              ├─ false → Malformed / FAIL / terminal
                              └─ true  → SupportedEdgeRelation
                                           ├─ false → Malformed / FAIL / terminal
                                           └─ true  → SupportedTraversal
```

`normative_precedence` 明定完整規範分類圖就是 `judgments` 內的 structured results、child dispatch 與 fixed-point branches；頂層 `base_envelope_shape`、`closure_algorithm`、`edge_shape`、`envelope_classification_order` 都是無獨立規範力的 derived views。

### 3.2 SupportedEdgeRelation — local totality PASS

`judgments.SupportedEdgeRelation` 的 exact obligations 已形成單值分支：

- `applicable_iff = judgments.SupportedEnvelopeHeader holds`；
- `depends_on = [judgments.SupportedEnvelopeHeader]`；
- predicate=false → `Malformed / FAIL / invalid / terminal=true / do not traverse`；
- predicate=true → `Traverse / PASS / valid / terminal=false / next_transition=judgments.SupportedTraversal`；
- `totality` 明列每個 applicable envelope 恰選 `false_result` 或 `true_result` 之一。

`SupportedEnvelopeHeader` 自身也有 false terminal 與 true unique transition。因此 v0.2.5 的 `CLOSURE-SUPPORTED-RELATION-RESULT-01` 在這個 local branch 已被 exact frozen bytes 封閉。

### 3.3 SupportedTraversal fixed-point skeleton — locally coherent

`SupportedTraversal`：

- `applicable_iff = judgments.SupportedEdgeRelation holds`；
- `depends_on = [judgments.SupportedEdgeRelation]`；
- child dispatch 為 `[judgments.OpaqueLeaf, judgments.GenericEnvelopeShape]`；
- fixed-point terminal branches 恰列：
  - `any_reachable_fail → FAIL`；
  - `no_fail_and_any_reachable_unknown → UNKNOWN`；
  - `queue_empty_all_reachable_pass → PASS`；
- 三者都標 `terminal=true`。

在「每個 child 都先有唯一 PASS/FAIL/UNKNOWN outcome」這個前提下，三分支以 FAIL 優先、再 UNKNOWN、其餘全 PASS 的語義互斥且可覆蓋終止佇列。

### 3.4 Counterexample to global traversal totality

上述前提在 frozen normative graph 中不成立：

```json
"OpaqueLeaf": {
  "applicable_when": "an artifact object does not contain artifact_envelope",
  "depends_on": [],
  "result": "opaque leaf; envelope classification is not applied",
  "traversal": "do not traverse"
}
```

此節點沒有：

- `gate_result`；
- `terminal`；
- 或一條把 opaque resolution 明確映成 fixed-point `PASS`（以及 expected-type mismatch 映成 `FAIL`）的 next transition／typed child rule。

這不是抽象不可達狀態。Frozen `artifacts-v0.2.6/run-standard.v0.2.6.json` 有 relation-valid edge：

```text
role = legacy-run-source
expected_type = opaque-content
sha256 = d587ac4f...a15b7a4
```

該 hash 精確解析到 manifest path `artifacts/run-standard.v0.2.0.json`；此 JSON 沒有 `artifact_envelope`，故 `SupportedTraversal.child_dispatch` 必選 `judgments.OpaqueLeaf`。從 normative graph 只能得到「不 traverse」，不能得到 reachable PASS/FAIL/UNKNOWN；因而不能推出 `queue_empty_all_reachable_pass`，也不能推出另外兩個 terminal branch。

Executable `semantic_validator_v026.py` 會把這種 child 記成 `opaque-content`，在 incoming expected type 為 `opaque-content` 時保持 PASS；這個行為沒有被規範性 `OpaqueLeaf` outcome 表達。頂層 derived-only prose 也不能依 `normative_precedence` 補上該結果。

所以存在 exact frozen reachable state：

```text
SupportedEdgeRelation=true
→ SupportedTraversal
→ child_dispatch=OpaqueLeaf
→ normative closure status = undefined
```

這構成 promotion blocker `CLOSURE-OPAQUE-LEAF-TERMINAL-01`。它不是 executable regression：同一 `supported-run-standard` probe 實際回 PASS。

## 4. The 11 terminal-totality checks

AI-3 唯讀執行既有 reproducer，結果：

- executable classifications：`20/20`；
- dependency/scope checks：`17/17`；
- terminal-totality checks：`11/11`；
- `unexpected=[]`，exit `0`。

11 checks 的資料來源都在 normative `judgments` object，沒有以 derived-only `closure_algorithm` 或 `envelope_classification_order` 補值。其對應如下：

| Check | 對應 frozen normative obligation | 判定 |
|---|---|---|
| generic-valid-dispatch-is-total | Generic true 的 exact supported/unsupported dispatch | genuine local check |
| supported-header-false-terminal | Header false 的 FAIL terminal | genuine local check |
| supported-header-true-unique-transition | Header true → Relation | genuine local check |
| supported-relation-false-terminal | Relation false 的 FAIL terminal | genuine local check |
| supported-relation-true-unique-transition | Relation true → Traversal | genuine local check |
| supported-relation-declares-totality | Relation exactly-one declaration | genuine declaration check |
| supported-traversal-depends-relation | Traversal dependency | genuine local check |
| supported-traversal-child-dispatch-total | child target list 恰為 Opaque/Generic | **名稱過強：只檢查 target list，不檢查 target outcomes** |
| fixed-point-terminal-trichotomy | 三個 branch key、三種 gate value、terminal flags | genuine branch-shape check；不證 child domain 已封閉 |
| transition-refs-fully-qualified | transition reference syntax | genuine local check |
| transition-targets-resolve | transition targets 存在 | genuine local check |

因此 `11/11` 是真實的局部 regression result，但不能推出整張 traversal graph outcome-total：check 8 只驗 `[OpaqueLeaf, GenericEnvelopeShape]` 這個列表，沒有要求 `OpaqueLeaf` 產生一個 terminal gate status；check 9 只驗 aggregation branches 的形狀，沒有證明每個 dispatched child 都落入其輸入 domain。

## 5. Retained v0.2.5 definitions

### 5.1 GenericEnvelopeShape dependency closure — PASS

v0.2.5 與 v0.2.6 的 `GenericEnvelopeShape`：

- 節點均存在；
- `depends_on` 均精確為 `[judgments.GenericEdgeShape]`；
- predicate 相同；
- false classification 均為 `Malformed / FAIL`；
- v0.2.6 另明列 `terminal=true` 及 true exact dispatch；
- v0.2.6 全部 dependency refs fully qualified 且可解析。

未發現 `CLOSURE-JUDGMENT-COMPLETENESS-01` 回歸。

### 5.2 Typed advice / ExpectedAdviceDecl — PASS in retained bounded scope

唯讀 canonical subtree comparison：

- schema `mechanism.admissibility` subtree v0.2.5 = v0.2.6；canonical subtree SHA256 均為 `8E51154896B4B17F850C8E8E64444D4BF70FE561D91B01F8FBA6ED93BA9982EA`；
- root advice-mode/ledger conditionals 均為兩條且內容相同；canonical rules SHA256 均為 `F3B6F7D3FA32B4931996560716F0926898F4E949FE6DAABD8441758F9E710D24`；
- validator `_expected_advice_declaration` 至 `_advice_declaration_matches` source region v0.2.5 = v0.2.6；region SHA256 均為 `7512936B8C9730FB67CD4FBAE77E634BE84FA1678514B0373558DB9BB36DB88C`。

故 typed `none | per-input-length-truth-table`、family/mechanism expected mapping、generator／quantifier／uniformity／answer-access／ledger binding 在本次靜態 exact comparison 中沒有回歸。本輪沒有重跑 advice executable matrix；此 PASS 是 retained Definition/SchemaConsistency/SemanticValidate interface 判定，不擴張為一般 soundness theorem。

## 6. Minimum formal obligation（非 successor 授權）

要封閉本 blocker，normative graph 至少必須：

1. 對 `OpaqueLeaf` 給出 structured terminal outcome；incoming expected type 為 `opaque-content`（或明列允許的 top-level情形）時導出 `PASS / terminal=true / do not traverse`；
2. 對 incoming expected type 不相容、hash 無法解析或 child type mismatch 的情形，於 normative traversal/child rule 明確導出 `FAIL`；
3. 將 `supported-traversal-child-dispatch-total` regression 擴成「每個 child target 的每個適用分支都有 terminal gate result 或唯一 next transition」，而不只比對 target 名單。

本報告只記錄義務，不建立、修改或啟動任何 successor。

## 7. Final bounded disposition

**FAIL / CLOSURE-OPAQUE-LEAF-TERMINAL-01**

- `CLOSURE-SUPPORTED-RELATION-RESULT-01`：CLOSED/PASS in local normative scope。
- `CLOSURE-JUDGMENT-COMPLETENESS-01`：retained CLOSED/PASS for GenericEnvelope dependency closure。
- `ADVICE-DECL-LEDGER-01`：retained CLOSED/PASS in stated typed interface scope。
- New executable/admission bypass：none found in assigned checks。
- New Definition/interface blocker：one，為 reachable OpaqueLeaf 缺少 fixed-point 可消費的 terminal gate result。
- Candidate 保持 frozen、read-only、`CANDIDATE_UNPROMOTED`。
- 無 Board、shared-repo、successor、完整工程驗收、一般 soundness/completeness 或 P/NP 外推。
