# I0 v0.2.3 candidate 狀態

目前狀態：`CANDIDATE_UNPROMOTED / pending independent acceptance`。

v0.2.3 是針對 frozen v0.2.2 `FAIL / CLOSURE-CLASS-01` 的窄版後繼。v0.2.2 的 98 個 manifest 路徑與 checksum 不變；本候選不建立共享 repo、不發布 Board success，也不提出 P=NP 或 P≠NP 結論。

## 固定介面

- schema：`DCE6F0C95B95D9377BA7AF9F9537BDC277CDF0E68CE74B9AD3BF83DB2B011895`
- external validator：`B0DC4EC989F93EBD557C4C8BFA3004E33B2BBAE0EB0F8FA5622489B2D148097B`
- candidate projection spec：`35D21683177A849FD8AD331451A818BE1EE2E7605CF4B11F54FF5CCCFED69251`
- artifact closure spec：`4E978EF2A2DF0FED51E94E89E6305294A9B7965AD86AB6888EE857DA4854643B`
- evidence role spec：`FB5C3BE06BA68716492B96664BF8FD5C6154C1159025E5F1D278FAD1C0B3CBFB`
- fixture manifest：`189967B7F60968BE2ACED2A0B4EE5E8885FBBFD997916BA18F55B33F3A4AA5D1`
- closure-classification fixture manifest：`46721DBE2E8A5E4CE1144DA2957C7688059637149DDDADFF766B517001C6DE06`
- frozen live experiment report：`7D32357291B59DE472A266BAAD63F7BBB469B60F58BCD727DF5D3A35899125EB`

上述雜湊先記錄本地 candidate 身分；完整 frozen manifest 會在文件完成後另產生，因此本頁本身不宣稱 promotion。

## 唯一功能性修補

`EnvelopeShape` 現在於 spec-id 分流前驗證：

1. `spec_id`、`artifact_type`、`version` 必須是非空字串；`edges` 必須是陣列。
2. 每個 edge 必須具有且只具有 `role`、`expected_type`、`sha256`；角色與型別為非空字串、角色不重複、雜湊格式有效。
3. 缺欄、空值、錯型或通用 edge 形狀錯誤一律 `Malformed/FAIL`。
4. 只有完整通過通用形狀、但 `spec_id` 不支援的 envelope 才是 `Unsupported/UNKNOWN`。
5. 支援的 spec 才進一步驗 version、artifact type 與 parent-role-child relation，通過後 traverse。

unsupported artifact 的 `artifact_type` 不必是目前已知型別；它只須為非空字串。這是明示的前向相容政策。`UNKNOWN` 與 `FAIL` 都阻止 admission。

## 保留的範圍

- GateVal 仍是 `pass | fail | unknown | not-applicable`；applicable gate 的 fail/unknown 均 fail closed。
- resource-account 對所有 regime 適用；resource-budget 只在 resource-bounded 適用。
- standard/robust 與 neutral/bounded 四象限規則未變；robust 仍僅指 pinned finite deterministic singleton I0 run。
- `ValidateBytes(recordBytes, schemaBytes, artifactSnapshot)`、raw `-0` 拒絕、Unicode scalar/NFC、role-bearing closure、signed operational map、transition execution、resource derivation及 PARITY/2-SAT oracle 路徑未改。
- REF-TYPE-01 與 PROV-DERIVE-01 的既有負例保留為回歸；通過這些有限測試不是一般 soundness/completeness 定理。

## 本地自測觀察

- frozen v0.2：14/14 PASS；frozen v0.2.1：11/11 PASS；frozen v0.2.2：15/15 PASS。
- v0.2.3：16/16 PASS；33 個 run-record fixtures，0 manifest mismatch。
- CLOSURE-CLASS-01：16 個 artifact cases 加 1 個 supported control，共 17/17 conformant。
- 2-SAT fixed-seed exhaustive cross-check：6 個 variable-count × 250 cases = 1500 PASS。
- fixture producer 的 107 個 artifact/fixture outputs 立即重產 byte-identical；live report 含實測時間，因此只凍結本次 bytes，不宣稱跨執行 byte-identical。
- v0.2.2 frozen manifest：98/98，0 mismatch。

以上全部標記為 Observation/Experiment。下一步是 AI-1/AI-2/AI-3 對 frozen v0.2.3 bytes 的唯讀驗收。
