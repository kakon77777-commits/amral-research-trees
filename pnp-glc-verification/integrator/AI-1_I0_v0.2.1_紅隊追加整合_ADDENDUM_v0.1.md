# AI-1｜I0 v0.2.1 紅隊追加整合 Addendum

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.1（2026-08-09，Asia/Taipei） |
| 附加對象 | `AI-1_I0_v0.2.1_二次唯讀驗收_FAIL_REF-TYPE-01_v0.1.md` |
| 原報告 SHA-256 | `889E8C2D22B628D810B660A9C9064EABA55A392709C5432C1E7A6DE5AACFD2B4` |
| 追加來源 | AI-2 bounded read-only red-team revalidation |
| Overall disposition | **維持 FAIL / REF-TYPE-01** |
| 數學狀態 | 工程／provenance gate；無 P/NP 推論 |

## 1. 來源與獨立重現

AI-1 重新計算：

| Artifact | SHA-256 | 結果 |
|---|---|---|
| AI-2 report | `6D0D88D76D7764D6FB764CCA804152B62736C45F59470C39ADFBE37EF0BACCB8` | PASS |
| AI-2 reproducer | `5B22DB0A9B77E3502281EABF351CEC2644F97D3659A54E38FBA69738F9AA1F73` | PASS |

AI-1 執行 `v021_bounded_redteam_revalidation.py` 的觀測：

```text
exit code                     0
candidate_root_writes         0
probe_count                   15
unexpected_probe_results      []
overall_disposition           FAIL / REF-TYPE-01
```

因此下列不是只轉述 AI-2，而是已在 AI-1 環境重現。

## 2. 主 blocker 的第三方一致性

AI-2 獨立重現兩個無需重簽的 `REF-TYPE-01`：

1. `robust-legit.run_spec_ref`：robust spec → standard spec；
2. `run_spec/maximal/fairness/sandbox` 四個 receipt-only refs 全改為 pinned Ed25519 public-key artifact。

兩案皆：

```text
signature=pass
closure=pass
structural=true
semantic=true
admission=true
final=true
accepted=true
issues=[]
```

這與 AI-1、AI-3 的獨立結果一致。v0.2.1 必須保持 frozen counterexample snapshot。

## 3. v0.2.2 新增強制驗收條件

### 3.1 `SCHEMA-BIND-API-01`

`validate_path` 正確地對同一份 schema bytes 做 read/hash/parse/use；但公開命名的：

```python
validate_record(record, schema_mapping, ..., schema_sha256=claimed_hash)
```

沒有證明 `schema_mapping` 是由 `claimed_hash` 對應 bytes 解析而來。AI-2 反例以 pinned schema 會拒絕的 receipt-only extra field，加上 `schema={}` 與 pinned hash，得到所有 aggregate true、issues=[]。

v0.2.2 必須二選一：

- 若這是 supported trust-boundary API：只接受 immutable schema snapshot／bytes，並在函式內由同一 bytes 導出 hash與 mapping；
- 若不是 public API：改成明確 private helper，文件與 exports 禁止把它當驗證入口，所有外部入口只能走 snapshot-binding path。

在完成其中一項前，AI-1 將它視為 successor acceptance blocker，而非可忽略的函式命名問題。

### 3.2 `CANON-NEGZERO-01`

projection spec 明文禁止 negative zero，但 raw JSON token `-0` 被 Python 預設 parser 轉為整數 `0`；因此與原 record 產生相同 projection hash，且在原有效簽章下被接受。

這不改變演算法答案，但違反 declared canonical input domain 並造成 raw-record malleability。v0.2.2 必須在 lexical information 消失前以 strict `parse_int` 或等價 tokenizer 拒絕 `-0`，並加入 unchanged-signature raw-token fixture。

### 3.3 `CLOSURE-CLASS-01`

closure spec 規定 envelope 缺 required member 為 `fail`；實作對缺 `spec_id` 回 `unknown`。兩者都阻擋 admission，所以不是 acceptance bypass，但 successor 必須先驗 required members，再區分「存在但未知的 spec id」。

### 3.4 Canonical surrogate diagnostic

unpaired surrogate 已間接 fail closed：`UnicodeEncodeError` 是 `ValueError`，projection hashing 路徑將其轉成 mismatch。下一版仍應在 canonical-domain walk 明確拒絕 non-scalar code points並產生專用 issue code。

### 3.5 Gate applicability schema boundary

schema-alone 在 `admission=false` 時允許 universally applicable gate=`not-applicable`；semantic validator 會拒絕。可選擇：

- schema 加入 AI-3 `GateAssignmentConformant`；或
- 明文聲明 applicability conformity 只由 semantic layer 保證。

不得再宣稱 schema-alone 已保證此性質。

## 4. 保留的 scoped positive evidence

AI-2 bounded probes另確認：

- `PROV-DERIVE-01` 兩案仍正確關閉；
- producer／signer／key／auth-receipt transplant 均拒絕；
- `validate_path` 與 `ArtifactIndex` snapshot TOCTOU probes 通過；
- missing child、known malformed envelope fail closed；fixed-point cycle終止；
- SAT/UNSAT oracle與 transition tamper均拒絕；
- 18 個 gate mutation與 final/applicability contradiction無 semantic bypass；
- NFD、float、超範圍整數拒絕；newline escape equivalence成立。

這些結果保持 scoped positive evidence；不抵銷 `REF-TYPE-01`，也不外推 production key custody、hardware measurement truth 或 P/NP。

## 5. 更新後 disposition

| Item | Disposition |
|---|---|
| v0.2.1 overall | **FAIL / REF-TYPE-01** |
| `SCHEMA-BIND-API-01` | v0.2.2 mandatory API-boundary repair |
| `CANON-NEGZERO-01` | v0.2.2 mandatory canonical conformance repair |
| `CLOSURE-CLASS-01` | fail-closed classification correction |
| surrogate diagnostic | hardening |
| shared repo / Board success | Deferred |
| P/NP conclusion | None |

**Disposition：下一版除了讓 evidence reference 帶角色，也必須讓 validator API 自己綁住它所用的 schema bytes，並在 JSON parser 還看得見 token 時拒絕 `-0`。**
