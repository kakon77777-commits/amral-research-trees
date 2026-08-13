# AI-3 I0 v0.2.2 形式／接口唯讀一致性審查

- 審查者：AI-3 / Codex-GLC-Formalizer
- 日期：2026-08-09（Asia/Taipei）
- 候選狀態：`CANDIDATE_UNPROMOTED`
- 審查狀態：**FAIL / CLOSURE-CLASS-01**
- 性質：形式接口反例；不是 acceptance bypass；沒有 P/NP 推論
- 操作邊界：候選樹全程唯讀；未發 Board、未改 repo、未 promotion

## 1. 結論

七項中，1、2、3、5、6、7 在下述限定域內一致；第 4 項存在可重現反例，因此整體不能給 consistency PASS。

唯一 promotion blocker（本次審查域內）是：凍結 closure spec 要求「任何必填 envelope 成員缺失／型別錯誤」先分類為 `Malformed/FAIL`，只有 shape-valid 且 `spec_id` 不支援者才是 `Unsupported/UNKNOWN`；實作卻在只驗 `spec_id` 後先做 unsupported 判斷。故「unsupported `spec_id` + 缺其他必填成員」得到 `UNKNOWN`，規格要求 `FAIL`。

`UNKNOWN` 仍會 fail closed，故此反例不讓 record 通過 admission；缺陷是分類 judgment 與凍結接口不一致。

## 2. 身分與完整性

- `SHA256SUMS-v0.2.2-candidate.txt`：`AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B`
- manifest entries：98；重新計算 98/98 PASS
- schema：`BDBB386CE7EAAB5377344BF29762CCBE45EA6371AC72742DE509467CB70BB556`
- validator：`7DA459E8AD9FB3F8A49FAA312A612F05484588143F36FF0918D090D6B1965AE5`
- projection：`7860AA7A741FAE5DCC6846B614C16450D29D17573563D6373A243931B9B51E57`
- closure：`11F6CB511ADFCF9528D11390E59CE1B52D8F709053FF5AA7295230F5B3E604EB`
- role spec：`2FEFA7AACB9B6D914C3B78CDB2C187262D12A35BD56B14FD5882A71B84991A3F`
- 執行環境：Python 3.14.5、jsonschema 4.26.0、win32

## 3. 七項 disposition

| # | 項目 | 結果 | 精確限定 |
|---|---|---|---|
| 1 | 四值 gate／applicability／GateAssignmentConformant | PASS | 限 `validation_receipt.gates` 的 18 個 admission gates；correctness receipt 是另一組 derived fields。四象限 72 個 applicability 反向變形零 escape。 |
| 2 | ValidateBytes／SchemaSnapshot trust boundary | PASS（scoped） | v0.2.2 candidate module 的支援入口是 `validate_bytes`／`validate_path`；schema hash 與 parse 來自同一 bytes snapshot，ArtifactIndex 亦先讀入 immutable bytes。`_validate_parsed_record` 是私有 helper，形式使用須帶 `SchemaBound(schema, hash)` 前提。 |
| 3 | RawParseDomain(-0) 與 CanonicalEncodeDomain | PASS | `_parse_json_int` 在物件化前拒絕 exact token `-0`；projection spec 分列 `raw_parse_domain` 與 `canonical_serialization`。 |
| 4 | Leaf／Malformed／Unsupported／Traverse 順序 | **FAIL** | unsupported 判斷早於 `artifact_type/version/edges` 的存在與型別檢查，違反 frozen spec。 |
| 5 | Admission／final／resource account／budget 蘊含式 | PASS | schema implication 與 semantic derivation 對齊；account completeness 永遠 applicable，budget 僅 bounded applicable。十二個必要條件變形均被 schema 拒絕。 |
| 6 | signed derived map／role closure／family-mode-id-version binding | PASS（known-family only） | 三個已知 valid-signature REF-TYPE 案例均被拒；這只是 bounded I0 reality test，不是 validator soundness／completeness theorem。 |
| 7 | robust singleton deterministic I0 run | PASS（degenerate robust scope） | 只涵蓋 pinned、有限、確定性 singleton run；成功 terminal replay 時 nonempty/maximal/fair 同時 PASS，transition FAIL 或 nonterminal 時三者同時 FAIL。scheduler／fault nondeterminism 不在域內。 |

另：package metadata、`__init__` 與 console script 仍是 v0.2.0；因此本項 PASS 不能外推成「目前已安裝 CLI 已採用 v0.2.2 trust boundary」。這與 candidate 尚未 promotion 一致。

## 4. CLOSURE-CLASS-01 最小反例

凍結規格 `artifacts-v0.2.2/artifact-closure-spec.v0.2.2.json:27-30` 的順序是：

1. 無 envelope：opaque leaf；
2. envelope 任一必填成員缺失／型別錯誤：Malformed/FAIL；
3. shape-valid、但 `spec_id` 不支援：Unsupported/UNKNOWN；
4. supported well-typed：Traverse。

實作 `semantic_validator_v022.py:604-616` 先讀／驗 `spec_id`，在 609 行立即對 unsupported 回 `UNKNOWN`，到 614–616 行才讀 `artifact_type/version/edges`。

反例 artifact：

```json
{
  "artifact_envelope": {
    "spec_id": "urn:unsupported:closure:9"
  }
}
```

以 direct role `run-spec` 解析：

```text
expected_by_frozen_spec = fail
actual                  = unknown
admission_bypass        = false
```

同一缺陷也涵蓋 unsupported `spec_id` 搭配 `artifact_type/version/edges` 任一缺失或基本型別錯誤；現有測試只測「缺 `spec_id`」，不足以證明一般 required-member ordering。

修訂義務：先定義並檢查與 spec-id 無關的 `EnvelopeShape(e)`（至少四個必填成員的存在、基本型別，以及 edge 的基本三欄 shape）；`¬EnvelopeShape → FAIL`。只有 `EnvelopeShape ∧ unsupported(spec_id) → UNKNOWN`；supported 分支再做 version、known artifact type、parent-role-child relation 與 traversal。修後應加入各必填欄位 missing／ill-typed × unsupported spec-id 的參數化 fixture。

可執行 regression：`AI3_v022_CLOSURE_CLASS_01_regression_v0.1.py`。目前輸出 `actual=unknown`、`conformant=false`、exit 1。

## 5. Gate 與完成條件的形式摘要

令 `GateVal = {pass, fail, unknown, notApplicable}`。在本候選的 18-gate 域內：

```text
GateAssignmentConformant(r) :=
  ∀g. Applicable(r,g)  → Gate(r,g) ∈ {pass,fail,unknown}
    ∧ ¬Applicable(r,g) → Gate(r,g) = notApplicable.
```

四象限必要 matrix：

| run × resource | run nonempty | maximal/fair | account completeness | budget |
|---|---:|---:|---:|---:|
| standard × neutral | applicable | N/A | applicable | N/A |
| standard × bounded | applicable | N/A | applicable | applicable |
| robust × neutral | applicable | applicable | applicable | N/A |
| robust × bounded | applicable | applicable | applicable | applicable |

`unknown` 表示證據不足／尚未驗完；`fail` 表示已判違反。兩者對 admission 都 fail closed。

必要蘊含式：

```text
AdmissionPass(r) →
  GateAssignmentConformant(r)
  ∧ ∀g (Applicable(r,g) → Gate(r,g)=pass)
  ∧ ResourceAccountComplete(r)
  ∧ RunSpecsConform(r).

FinalCompletion(r) →
  AdmissionPass(r)
  ∧ OraclePass(r) ∧ ContractPass(r) ∧ CompletePass(r)
  ∧ ResourceAccountPass(r)
  ∧ ReceiptLossDebt(r)=0 ∧ LedgerLossDebt(r)=0
  ∧ CandidateStatus(r)∈{sat,unsat,complete}
  ∧ (ResourceBounded(r) →
       ResourceBudgetGate(r)=pass ∧ CorrectnessBudget(r)=pass).
```

Executable validator 另從 replay、resource fold、trace authenticity、operational binding 等 constituent facts導出 gates；schema consistency 本身只封閉已寫入欄位的 implication，不能取代 SemanticValidate。

## 6. 動態證據

- legacy tests：14/14 PASS
- v0.2.1 tests：11/11 PASS
- v0.2.2 tests：15/15 PASS
- v0.2.2 manifest：31 fixtures，0 mismatch
- 四象限 GateAssignmentConformant：4 × 18 = 72 mutations，0 escape
- Admission/final/account/budget 必要條件：12 mutations，全部 schema-rejected
- REF-TYPE reality tests：3/3 signature=PASS 且 record rejected
  - receipt-ref-substitution：closure PASS；operational binding FAIL
  - robust-ref-type-confusion：closure FAIL；direct-role type／binding FAIL
  - cross-role contract↔invariant：closure FAIL；signed map／map hash／role／type FAIL
- robust scoped probe：terminal pinned replay=`(pass,pass,pass)`；failed transition=`(fail,fail,fail)`；nonterminal=`(fail,fail,fail)`

所有 98 個凍結 manifest entries 在測試後再驗仍為 98/98 PASS。

## 7. Epistemic labels 與下一步

- **Counterexample / interface mismatch**：CLOSURE-CLASS-01。
- **Experiment**：31-fixture、72-gate、三個 REF-TYPE、robust singleton probes。
- **Conditional elementary property**：在 pinned I0 與成功 terminal replay 前提下，singleton run nonempty/maximal/fair。
- **Open Problem**：一般 typed closure soundness/completeness、一般 robust scheduler/fault semantics、四層大等價式與任何 P/NP 結論。

凍結 v0.2.2 應保持不變；後繼候選修正 classification order、加入廣義 malformed+unsupported fixtures、重新 freeze 並由 AI-1／AI-2／AI-3 唯讀驗收後，才可重新判 promotion。已知 REF-TYPE 修復可保留為 scoped positive evidence，但不能抵銷本 blocker。
