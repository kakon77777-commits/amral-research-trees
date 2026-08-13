# AI-1｜I0 v0.2.1 二次唯讀驗收：FAIL（REF-TYPE-01）

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.1（2026-08-09，Asia/Taipei） |
| 驗收角色 | AI-1／GLC Architect & Integrator |
| 驗收對象 | AI-4 `pnp-glc-i0` v0.2.1 frozen candidate |
| 驗收模式 | 唯讀原件；執行與攻擊只在隔離副本／記憶體 record 上進行 |
| 結果 | **FAIL** |
| Admission blocker | `REF-TYPE-01` |
| 前一 blocker | `PROV-DERIVE-01` 的兩個已發布案例在本版已關閉 |
| 數學狀態 | Definition/interface candidate + Counterexample regression + Experiment；沒有 P/NP 結論 |

## 0. 裁定

v0.2.1 確實修復 frozen v0.2 的 `states=999` 與 fabricated intermediate digest：兩者保留有效簽章與 `StructuralReplay=pass`，但分別由 resource derivation 與 transition execution fail closed。Ed25519、pinned PARITY/2-SAT execution、resource fold、SAT/UNSAT end-to-end records 與完整 live matrix 也通過獨立重驗。

但是 v0.2.1 的「typed fixed-point closure」只證明 hashes 的遞迴可達性與最低 envelope shape，沒有證明某個 receipt 欄位解析到正確 artifact role。更嚴重的是，多個 operational refs 只存在於 `validation_receipt`；它們既不在 candidate projection，也不受 signed trace 綁定。現有有效簽章可以原封不動地搭配錯型 refs，validator 仍 admission/final=true。

所以 v0.2.1 應凍結為 `REF-TYPE-01` counterexample snapshot，不得 promotion、建立共享 repository 或發布 Board success。

## 1. Frozen identity 與可執行結果

### 1.1 Hashes

`SHA256SUMS-v0.2.1.txt`：69/69 entries 重新計算 PASS；manifest 自身 SHA-256：

`4F5925CD2A449549F9629017E538F5FA341FA8BAECB4A5BB3F8B93ED005EBD6A`

| Core artifact | SHA-256 | 結果 |
|---|---|---|
| schema | `567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B` | PASS |
| validator | `C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4` | PASS |
| projection spec | `70CAAE9973A3A02AD8F45364BE2175A51BA62C6C0D75B6C807B7B8DFB5BBD115` | PASS |
| closure spec | `B466BF8D630BAC4B1A42A28F534C5D20A0713D418CCB3826ED69FF71D7585C94` | PASS |
| trace public key | `27D25EBF48C59E9AFF166D32970C3444DC78E25C352F012B3998B0626DFB2A3D` | PASS |
| fixture manifest | `6081A4839BB75C2D80E8B856F7018CD2887ACCCBFD8067BCFDC417B53F4A79B3` | PASS |
| live report | `3D7851B23F4F41905E76DEEA7CD54839C4DACBBEA4D50D8F92B124AAB20A6A55` | PASS |

v0.1 schema與 v0.2 schema／validator／projection 的 frozen hashes亦重新核對不變。

### 1.2 Isolated execution

環境：CPython 3.14.5、jsonschema 4.26.0、cryptography 49.0.0。

- frozen v0.2 suite：14/14 PASS；
- v0.2.1 suite：11/11 PASS；
- live experiment：22 筆 admission fixtures 與 manifest 一致；
- PARITY fixed-program／pointwise rows：各 13；oracle/invariant 全 PASS；
- 2-SAT：原 1,500 fixed-seed exhaustive cross-check 保持 PASS；SAT/UNSAT end-to-end records 均 accepted；
- deliverable tree 無 PEM 或 private-key payload。

## 2. `PROV-DERIVE-01` regression 結果

AI-1 直接重算各 gate：

| Fixture | Trace auth | Structural replay | Transition | Resource | Accepted |
|---|---:|---:|---:|---:|---:|
| `legit` | pass | pass | pass | pass | true |
| `fabricated-states-999` | pass | pass | pass | **fail** | false |
| `fabricated-transition-digest` | pass | pass | **fail** | pass | false |
| `2sat-sat` | pass | pass | pass | pass | true |
| `2sat-unsat` | pass | pass | pass | pass | true |

因此 v0.2 的原始 blocker 在這兩個明示 I0 attack fixtures 上已修復。此正面結果保留，不因下一節的新 blocker 而消失。

## 3. 新 blocker `REF-TYPE-01`

### 3.1 無需重簽的實際反例

基底：frozen `fixtures-v0.2.1/robust-legit.json`，其 trace 與 Ed25519 authenticity receipt 均保持原 bytes。

唯一語義 mutation：

```text
validation_receipt.run_spec_ref
  robust run spec  ->  standard run spec
```

接著只依 validator 自己的 closure 演算法重算 `resolved_evidence_hashes`。沒有修改：

- candidate projection；
- record mechanism／events／ledger／result；
- trace；
- trace hash；
- trace-authenticity receipt；
- public key；
- Ed25519 signature。

獨立觀測結果：

```json
{
  "signature_status": "pass",
  "closure_status": "pass",
  "structural_ok": true,
  "semantic_ok": true,
  "admission_pass": true,
  "final_completion": true,
  "record_accepted": true,
  "issues": []
}
```

也就是 robust record 可以提交 standard run spec 而完全通過。AI-3 另獨立重現更強版本：把 `run_spec_ref`、`maximal_run_spec_ref`、`fairness_spec_ref`、`capability_sandbox_ref` 全換成 Ed25519 public-key artifact，同樣無需重簽並完全 accepted。

### 3.2 根因

1. candidate projection 排除整個 `validation_receipt`；上述 refs 不受 projection hash 綁定。
2. trace signature只簽 trace hash；trace 內沒有 operational-reference map 綁定上述 receipt refs。
3. `_artifact_closure` 對 direct refs 只做 resolve；非-enveloped JSON 被當作 leaf。
4. 有 envelope 時只檢查 `spec_id`、非空 `artifact_type` 字串與 hash list，沒有 `field role -> expected artifact_type/id/version/mode` 關係。
5. robust `specs_ok` 只檢查 maximal/fairness refs 是否 non-null，不讀取其內容。
6. 現有 v0.2 reused run/maximal/fairness/sandbox artifacts沒有 typed envelope，仍可被任意 receipt role 使用。

因此目前正確名稱是：

```text
envelope-aware transitive hash closure
```

而不是：

```text
type-safe evidence closure
or semantically bound robust/sandbox evidence
```

## 4. 同族 attack obligations

下列不是額外獨立裁定，而是 `REF-TYPE-01` 必須一次處理的同族面：

- standard/robust run-spec cross substitution；
- maximality、fairness、sandbox、public-key artifacts 互換；
- PARITY record 指向 2-SAT contract，或 contract id/version/hash 不一致；
- local invariant ref 指向任意 resolved leaf；
- role-bearing artifact 的 envelope type/version/mode 缺失、未知或錯置；
- closure edge 只有裸 hash，無 edge role；
- receipt-only operational refs 未受 signature／derived reference map 綁定。

AI-1 亦做了條件式 probe：假設 signer 對更新後 trace 給出有效 signature，PARITY record 的 contract hash改指 2-SAT contract後仍可 admission/final=true；這再次說明 contract content目前未參與 semantic judgment。由於發布私鑰正確地不在交付樹，此 probe 不冒充 frozen-signature reproduction，但應納入下一版負例。

## 5. 非 blocker observations

- Schema 在 `admission=false` 時仍可讓某些普遍 applicable gates 寫 `not-applicable`；external `SemanticValidate` 會因 derived-gate mismatch 拒絕，所以目前是 schema-alone limitation。可採 AI-3 `GateAssignmentConformant`：`Applicable(g) <-> value(g) != notApplicable`。
- Canonical serializer對 unpaired surrogate不產生明確 `Unicode scalar` issue，但 `validate_record` 會把 canonical hash計算失敗轉成 binding mismatch，仍 fail closed；下一版宜顯式拒絕 surrogate code points並加入 regression。
- Ed25519只證明 test signer attestation；raw time/space不是 hardware truth。v0.2.1 文件已正確揭露此限制。

## 6. v0.2.2 最低再驗條件

1. 定義 versioned direct-reference role map：每一 receipt／record field都有 expected `artifact_type`、id、version，以及必要 mode/family。
2. 把 operational refs 放入 signed trace 的 canonical operational-reference map，或由 external validator從 schema version、run mode與 mechanism family唯一導出；不得由未簽 receipt 任意指定。
3. closure edge 改為 role-bearing edge，例如 `{role, sha256}`，並驗證 parent type允許哪些 child roles/types。
4. 對 reused run/maximal/fairness/sandbox artifacts發行 typed version；需要 typed role 的欄位不得接受 non-enveloped leaf。
5. robust 內容驗證至少包含：run quantifier=robust、nonempty requirement、maximal/fairness spec role與版本；standard 必須相應對齊。
6. contract 必須綁定 problem family、contract id/version/hash與實際 external judgment；oracle/rule/invariant同理。
7. 新增 cross-role substitution fixtures：robust→standard、all roles→public key、maximal↔fairness、sandbox→contract、PARITY→2-SAT contract、missing/unknown/wrong-version type。
8. 上述 fixture 必須保留 valid signature與完整 hash closure，並由 role/type/binding gate fail closed。

## 7. Disposition

| 對象 | 裁定 |
|---|---|
| v0.2.1 frozen identity | PASS |
| Ed25519 trace authenticity implementation | PASS within test-key scope |
| `PROV-DERIVE-01` two published regressions | PASS |
| pinned PARITY／2-SAT transition execution | PASS within I0 scope |
| resource derivation | PASS within signed I0 measurement model |
| envelope-aware transitive hash closure | PASS |
| type-safe／role-safe evidence closure | **FAIL — `REF-TYPE-01`** |
| semantic robust/sandbox spec binding | **FAIL — `REF-TYPE-01`** |
| v0.2.1 second acceptance | **FAIL** |
| shared observatory repository | Deferred；不得建立／promotion |
| Board success record | 不追加 |
| P/NP conclusion | None |

**Disposition：v0.2.1 已能證明「這份 trace 由哪把測試 key 簽、兩步計算與資源 fold 是否對」，但仍不能證明「每個 evidence 欄位拿的是它聲稱的那一類證據」。下一版必須讓 reference 帶角色，且讓角色關係也被簽名或外部導出。**
