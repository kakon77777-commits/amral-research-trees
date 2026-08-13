# AI-2 I0 v0.2.2 本機唯讀 conformance review

**Disposition：`FAIL / CLOSURE-CLASS-01`**

這是 frozen v0.2.2 record validator 的軟體規格一致性核驗。全程僅使用本機檔案、記憶體物件與隔離暫存副本；未連網，candidate root 實測 `0 writes`。結論不涉及外部系統，也不構成任何 P/NP 推論。

## Frozen identity

下列 SHA-256 全部精確相符：

- `SHA256SUMS-v0.2.2-candidate.txt`：`AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B`
- schema：`BDBB386CE7EAAB5377344BF29762CCBE45EA6371AC72742DE509467CB70BB556`
- validator：`7DA459E8AD9FB3F8A49FAA312A612F05484588143F36FF0918D090D6B1965AE5`
- projection spec：`7860AA7A741FAE5DCC6846B614C16450D29D17573563D6373A243931B9B51E57`
- closure spec：`11F6CB511ADFCF9528D11390E59CE1B52D8F709053FF5AA7295230F5B3E604EB`
- evidence-role spec：`2FEFA7AACB9B6D914C3B78CDB2C187262D12A35BD56B14FD5882A71B84991A3F`

Checksum manifest 為 `98/98`、零 missing、零 mismatch。

## 唯一 blocker：CLOSURE-CLASS-01

Frozen closure spec 的分類順序是：

1. 沒有 `artifact_envelope`：Leaf。
2. envelope 任一 required member 缺失或型別錯誤：Malformed／`fail`。
3. required shape 完整，但 `spec_id` 不支援：Unsupported／`unknown`。
4. 支援且 shape 正確：Traverse。

最小反例：

```json
{"artifact_envelope":{"spec_id":"urn:unsupported:closure:9"}}
```

此 envelope 具有不支援的 `spec_id`，但同時缺少 required `artifact_type`、`version`、`edges`。依 frozen spec 必須先分類為 Malformed／`fail`；實測：

```text
frozen spec expected = fail
validator actual      = unknown
```

原因位於 frozen validator 第 604–616 行：實作先讀取並分派 `spec_id`，遇到不支援值便在第 609–613 行回傳 `unknown`；`artifact_type/version/edges` 的 shape validation 到第 614 行以後才執行。

`unknown` 仍會阻止 admission，因此這不是 record 錯誤接受，也不是 `REF-TYPE-01` 回歸；但它違反 frozen interface 的 required-member ordering，足以阻止 v0.2.2 promotion。

後繼版本的最小修正義務：

- 先執行 generic `EnvelopeShape`，完整檢查 `spec_id/artifact_type/version/edges` 的存在與型別。
- 只有 shape-valid envelope 才依 `spec_id` 分成 supported 或 unsupported。
- 加入 `unsupported spec_id × missing/ill-typed required member` 的參數化 fixtures。
- Frozen v0.2.2 bytes 保持不變，修正另起新版本。

## 已通過的 scoped conformance evidence

### 內建驗證

- 前代測試：`14/14 PASS`。
- v0.2.1 測試：`11/11 PASS`。
- v0.2.2 測試：`15/15 PASS`。
- `scripts/reproduce_ref_type_v022.py`：exit `0`，三個既有 valid-signature REF-TYPE negative fixtures 全部拒絕。
- v0.2.2 manifest：`31` fixtures、`0` result mismatch。

上述測試沒有包含本報告的最小 `unsupported + missing required members` 組合，因此與 blocker 並不矛盾。

### Schema-valid reference substitutions

以下四組在隔離副本中重新建立自洽 trace、使用 matching non-production fixture signature，且 mutated record 均通過 JSON Schema；external validator 全部回傳 `record_accepted=false`：

| 欄位替換 | signature | closure | 結果 | 主要判定 |
|---|---:|---:|---:|---|
| robust `run_spec_ref` → standard run spec | pass | pass | rejected | exact operational role/map mismatch |
| sandbox ref → run-spec artifact | pass | fail | rejected | direct role/type 與 exact map mismatch |
| PARITY contract → 2-SAT contract | pass | pass | rejected | exact role map及 contract-family binding |
| invariant/certificate/event invariant → contract artifact | pass | fail | rejected | direct role/type 與 exact map mismatch |

Signed operational map 少一個 role、多一個 role，以及 receipt map hash 單獨變更，亦全為 schema-valid 且全部拒絕。將另一個 record 的完整 trace/auth receipt pair 指入 `legit` 時，簽章與 closure 仍為 pass，但 run/projection/replay/operational binding 使最終結果拒絕。

這些結果僅支持目前四個欄位族與 bounded I0 fixtures，不能升格為所有未來 artifact family 的 completeness theorem。

### Raw JSON、schema bytes 與 envelope 分類

- raw integer token `-0`：在轉成 Python integer 前回 `record-parse`，符合 v0.2.2 `RawParseDomain(-0)=reject`。
- 錯誤 schema bytes `{}`：先回 `schema-byte-pin-mismatch`；supported API 由同一份 bytes 內部導出 hash 與 parsed schema。
- unpaired surrogate：回明確 `canonical-unicode-scalar` 並拒絕。
- `\n` 與 `\u000a`：產生相同 canonical bytes。
- missing `spec_id`：`fail`。
- shape-valid unsupported `spec_id`：`unknown`。
- wrong edge type、duplicate edge role、missing child 與 synthetic typed relation cycle：全部 `fail`。

唯一不一致即本報告的「unsupported `spec_id` 與其他 required members 同時缺失」ordering case。

### Derived mirrors、resources 與 gates

- fabricated problem size：以 `problem-size-derivation` 拒絕。
- fabricated failure-frontier axis：以 `failure-frontier-derivation` 拒絕。
- declared/observed answer-access 不一致：以 `answer-access-family-binding` 拒絕。
- states count 與 transition digest 的既有負向 fixtures：均拒絕。
- record 與 trace 的 raw resource sample 不一致：以 `replay-resource-fold` 拒絕。
- record 與有效簽章 trace 的 raw space measurement 一致時可接受；其意義僅為 signer attestation/binding，不是獨立重建量測。
- 對八種 fixture profiles 執行 `8 × 18 = 144` 個 gate applicability 變體：JSON Schema 接受數為 `0`。

## Candidate-root read-only proof

獨立 reproducer 在開始與結束時，對 candidate root 每個檔案比較：

- relative path set
- byte length
- `mtime_ns`
- SHA-256

結果：

```text
candidate_root_writes = 0
changed_paths         = []
```

隔離簽章與 trace/artifact 檔案只存在於系統暫存副本，結束後由 temporary-directory cleanup 移除。

## Reproduction

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONUTF8='1'
python .\outputs\v022_conformance_revalidation.py
```

預期結果：

```text
exit                     = 0
overall_disposition      = FAIL / CLOSURE-CLASS-01
promotion_blockers       = [CLOSURE-CLASS-01]
probe_count              = 12
unexpected_results       = []
candidate_root_writes    = 0
```

Reproducer SHA-256：

```text
45F904D34DADAA17562FC0A227E461684EFBFF24E5EB9DAC2897C1EA3C43A4AC
```

## Scope and nonclaims

- 本報告只適用於列出的 frozen v0.2.2 hashes 與 bounded I0 interface。
- robust 結果只適用於 pinned finite deterministic singleton run family。
- Raw authenticated measurements 只證明 test signer attestation。
- v0.2.2 應保持 `CANDIDATE_UNPROMOTED`；本報告不宣告 Board success 或 shared-repository adoption。
- 無任何 `P=NP` 或 `P≠NP` 推論。
