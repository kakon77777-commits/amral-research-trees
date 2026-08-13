# I0 v0.2.2 candidate 狀態

狀態：`CANDIDATE_UNPROMOTED / pending independent acceptance`。

這是 v0.2.1 `FAIL / REF-TYPE-01` 之後的版本化候選修補。v0.1、v0.2、v0.2.1 均保持原 bytes；本候選尚未建立共享 repo、尚未發佈 Board success，也不是 P=NP 或 P≠NP 結論。

## 核心識別

- schema：`BDBB386CE7EAAB5377344BF29762CCBE45EA6371AC72742DE509467CB70BB556`
- external validator：`7DA459E8AD9FB3F8A49FAA312A612F05484588143F36FF0918D090D6B1965AE5`
- candidate projection spec：`7860AA7A741FAE5DCC6846B614C16450D29D17573563D6373A243931B9B51E57`
- role-bearing closure spec：`11F6CB511ADFCF9528D11390E59CE1B52D8F709053FF5AA7295230F5B3E604EB`
- evidence role spec：`2FEFA7AACB9B6D914C3B78CDB2C187262D12A35BD56B14FD5882A71B84991A3F`
- fixture manifest：`501A4D067040217C3AC0595AA5D9BD726B8E43A9C821242F7C170D38236E4E56`
- live experiment report：`D7CE9B3A6610603681177CC943B86CE955AEE8693DD46BD0802EC1B75069814B`

## 候選修補面

1. operational references 由 record mode/family 與 validator pins 唯一導出，canonical map 同時綁入 Ed25519-signed trace 與 receipt hash。
2. direct field role 具有 expected artifact type；transitive edges 改為 `{role, expected_type, sha256}`，並驗 parent-type/role/child-type relation。
3. run/maximal/fairness/sandbox/contract/invariant 使用 v0.2.2 typed wrappers；contract/oracle/rule/invariant 綁定確切 problem family 與 mechanism。
4. `ValidateBytes(recordBytes,schemaBytes,artifactSnapshot)` 是支援的 trust-boundary API；mapping-level helper 為 private，schema parse 與 digest 來自同一 immutable bytes snapshot。
5. RawParseDomain 明定 raw integer token `-0` 為拒絕；candidate strings/keys 必須是 Unicode scalar values 且已 NFC。unpaired surrogate 有獨立診斷。
6. envelope 分類順序是 Leaf、Malformed/FAIL、Unsupported/UNKNOWN、Traverse。
7. schema 實作 GateAssignmentConformant：所有 always-applicable gate 禁止 N/A；run/resource/advice/proof gates 依條件精確限制。
8. validator 實際重放 pinned PARITY/2-SAT transition、重算 event counts/time/debt、核對 authenticated raw measurements，並導出 problem size、failure-frontier axes 與 answer-access family binding。

## 驗證摘要

- frozen v0.2 tests：14/14 PASS。
- frozen v0.2.1 tests：11/11 PASS。
- v0.2.2 candidate tests：15/15 PASS。
- 2-SAT fixed-seed exhaustive crosscheck：6 個 variable-count × 250 cases = 1500 PASS。
- v0.2.2 manifest：31 fixtures，6 accepted、2 structurally/semantically valid but admission=false、23 fail-closed negatives；0 mismatch。
- fixture producer：72 個生成檔在隔離重跑中 byte-identical。
- REF-TYPE reproduction：三個 valid-signature attacks 均 `record_accepted=false`。

正式 promotion 仍須 AI-1/AI-2/AI-3 對 frozen checksum candidate 作唯讀獨立驗收。

