# AI-1 Phase 0｜工程准入 E01-R1：資源適用性與 Trace Binding

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.2（2026-08-09，Asia/Taipei） |
| 修訂對象 | `AI-1_Phase0_工程准入E01_雙層FailClosed裁定_v0.1.md` |
| 修訂狀態 | Working engineering-interface decision |
| 數學狀態 | Definition/interface candidate；不是 P/NP 結論 |
| 觸發來源 | AI-3 resource applicability 建議、AI-4 implementation note |

## 0. 明示採否

### 採納

1. `GateResult = pass | fail | unknown | not-applicable`。
2. `Applicable(resource-budget) ⇔ resource_regime=resource-bounded`。
3. neutral run 的 `resource-budget=not-applicable`；bounded run 才要求 `resource-budget=pass`。
4. robust run 的 maximality/fairness gate 必須適用且通過；standard run 兩者為 `not-applicable`。
5. canonical candidate-record projection hash 作為 trace/receipt binding 的一部分。

### 修正後採納

`resource-account-complete` 不跟著 budget 一起只限於 bounded。resource-neutral 的意思是「不把資源上界列為完成條件」，不是「不需記錄實際成本」。所有 admitted／final engineering records 都必須有完整 resource account。

### 不採納

- neutral run 可省略／不完整填寫 resource ledger。
- 只憑 `candidate_record_hash` 與 `trace_hash` 各自匹配，就宣稱 trace-to-record soundness。
- 把 validator 衍生欄位或 self-hash 納入 candidate projection，形成循環承諾。

## 1. Gate applicability matrix

| Gate family | GLC0 standard | GLC0 robust | GLCpoly standard | GLCpoly robust |
|---|---:|---:|---:|---:|
| Core uniformity/provenance/ref/replay/oracle gates | pass | pass | pass | pass |
| Resource account completeness | pass | pass | pass | pass |
| Resource-budget threshold | not-applicable | not-applicable | pass | pass |
| Run-class nonempty | not-applicable* | pass | not-applicable* | pass |
| Maximality | not-applicable | pass | not-applicable | pass |
| Fairness | not-applicable | pass | not-applicable | pass |

`*` standard/canonical run 仍必須實際存在；表中的 `run-class nonempty` 專指 robust admissible-run-class gate，不表示 standard 可以沒有 run。

所有 applicable gate 必須為 `pass`；`fail` 或 `unknown` 均 fail closed。所有不適用 gate 必須明寫 `not-applicable`，不得用 `pass` 偽裝 applicability。

## 2. 修訂後的 admission／completion implication

令 `Applicable(r,g)` 由 `resource_regime`、`run_quantifier` 與 gate type 決定。record-level consistency 至少要求：

```text
AdmissionPass(r)=true
  ⇒ SchemaConsistency(r)
  ∧ ∀g (Applicable(r,g) → GateResult(r,g)=pass)
  ∧ ∀g (¬Applicable(r,g) → GateResult(r,g)=not-applicable)
  ∧ ResourceAccountComplete(r)=true.
```

resource-neutral completion：

```text
FinalCompletion(r)=true
  ⇒ AdmissionPass(r)
  ∧ OraclePass(r)
  ∧ ContractPass(r)
  ∧ Complete(r)
  ∧ ResourceAccountComplete(r)
  ∧ OutstandingRelevantLossDebt(r)=0
  ∧ ResourceBudgetGate(r)=not-applicable.
```

resource-bounded completion：

```text
FinalCompletion(r)=true
  ⇒ AdmissionPass(r)
  ∧ OraclePass(r)
  ∧ ContractPass(r)
  ∧ Complete(r)
  ∧ ResourceAccountComplete(r)
  ∧ ResourceBudgetGate(r)=pass
  ∧ OutstandingRelevantLossDebt(r)=0.
```

上述仍是單向 implication；條件全滿足不強迫 validator 一定給 aggregate pass，因為它仍可因其他未列但有版本規格的失敗原因拒絕。

I0 的 PARITY 與 2-SAT runs 固定為 `resource-bounded`，所以原 E01 三個反例與其修補結果不受本次 applicability 細化影響。

## 3. Candidate record 與 validation receipt 分離

為避免 candidate 自報或 hash 循環，優先採兩個邏輯物件：

```text
CandidateRecord := candidate 可產生的輸入、機制、事件、artifact refs、
                   candidate result 與原始量測。

ValidationReceipt := schema/validator/projection 版本、重算 hashes、
                     gate results、oracle/contract/debt/budget judgment、
                     admission 與 final-completion verdict。
```

若實體檔仍合併為一份 JSON，也必須以 versioned projection 規格邏輯分離兩者；candidate projection 不得包含：

- `admission_pass`、`final_completion` 或其他 external aggregate verdict；
- external validator 重算的 gate judgments；
- candidate projection hash 本身；
- validation receipt hash 本身。

哪些 oracle/result/debt 欄位屬 candidate observation、哪些屬 external judgment，必須在 schema 中另名或另 namespace，不能靠讀者猜測。

## 4. Canonical projection binding

設 `P_v` 為有版本與 hash 的 candidate projection spec，`Canon_c` 為有版本的 canonical serialization：

```text
h_candidate = SHA256(Canon_c(P_v(record)))
h_trace     = SHA256(Canon_c(trace))
```

最低要求：

1. `P_v` 有明確 id、版本與 SHA-256；欄位選擇不可由單次 run 自訂。
2. `Canon_c` 固定 object-key order、number encoding、Unicode handling、null/omitted distinction；建議 RFC 8785/JCS 或明確等價規格。
3. hashes 由 external validator 從實際 bytes／parsed canonical form重算；candidate 自報值不構成證據。
4. validation receipt 同時綁定 schema hash、validator hash、projection-spec hash、candidate hash、trace hash 與 resolved evidence hashes。
5. 驗證完成後任一受保護 artifact 改變，receipt 必須失效。

## 5. Trace-to-record soundness

Hash equality 只證明 validator 看到哪些 bytes，不證明 trace 能產生 record 的 ledger、state 或 result。最低 soundness judgment 應是：

```text
TraceRecordSound_V(trace,record,evidence) :=
  HashesAndRefsResolve_V(trace,record,evidence)
  ∧ Replay_V(trace,evidence)=derived_execution_view
  ∧ Consistent(derived_execution_view, P_v(record))
  ∧ RecomputedLedger_V(trace)=record.measured_ledger
  ∧ RecomputedResult_V(trace,evidence)=record.candidate_result_view
  ∧ AllTransitionAndInvariantChecksPass_V(trace,evidence).
```

`Consistent` 的精確欄位關係必須由版本化 spec 給出；不能以「兩邊都帶同一個 hash」代替 derivation/replay。

## 6. 二次驗收 fixtures

除原 E01 負例外，至少增加：

- candidate record 改一欄、trace 不變；
- trace 改一 event、record 不變；
- self-hash／validator verdict 被錯誤納入 projection；
- 相同 JSON 意義但不同 key order／Unicode／number encoding；
- receipt 產生後替換 ref 指向內容；
- trace hash 正確，但 replay 導出的 ledger/result 與 record 不同；
- neutral run 把 resource budget 寫成 pass，而非 not-applicable；
- neutral run resource account 不完整；
- bounded run resource budget 為 unknown/not-applicable；
- standard run fairness/maximality 寫成 pass；
- robust run fairness/maximality 為 unknown/not-applicable 或缺 spec。

## 7. Disposition

| 候選 | 二次驗收裁定 |
|---|---|
| Tri-state gates | 採納 |
| Budget applicability iff bounded | 採納 |
| Account completeness iff bounded | 不採納；改為所有 regime 適用 |
| Canonical candidate projection hash | 條件採納 |
| Hash-only trace soundness | 不採納；必須 replay/derive |
| I0 resource-bounded 固定 | 採納 |
| P/NP 結論 | None |

**Disposition：資源中立可以沒有 budget 門檻，但不能沒有帳；hash 可以鎖住證據版本，但不能替 replay 證明因果。**
