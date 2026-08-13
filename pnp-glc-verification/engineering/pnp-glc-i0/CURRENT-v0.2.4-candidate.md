# I0 v0.2.4 candidate 狀態

目前狀態：`CANDIDATE_UNPROMOTED / pending independent acceptance`。

v0.2.4 是 frozen v0.2.3 `FAIL / CLOSURE-EDGE-SCOPE-01 + ORACLE-DECL-FAMILY-01` 的版本化修補。v0.2.3 的 121 個 manifest 路徑不變；本候選不建立共享 repo、不發布 Board success，也不提出 P=NP 或 P≠NP 結論。

## 固定介面

- schema：`16EBCC7DE4196D0C46FC9C309F2060F856E321C0012C5B775390C04234F9DCC8`
- external validator：`B744C9C20C510FE39F132E0DFB4AAC50E6E3E573B48B7F1AE19494F5D5195FED`
- candidate projection spec：`CCF57716E63AD6B627F48688925054975254A88344E7F84ECBEC9CF0145B9D6D`
- artifact closure spec：`579B6F7DA8BE3712FE6130AD900CF0CBA189496100548CBF87655687A7690588`
- evidence role spec：`4EFC4C71C6275227B14429E58FCECC4E949459918315D27CC476765C7D24D850`
- fixture manifest：`5F79E8DC3EBAD4A9BA8C32C7092CDF52307220D08EF1D83EFD399B12B00B7AB1`
- closure-classification fixture manifest：`09E9E6E4C0F1528C8239606DB6CC0A724B1031973F8D79F504FC22A2793A9159`
- closure/scope reproducer：`5F0FB64D1BB6DA17804088260FCA94A92F21DD4C2F5FAC1A9605F9F3BAD303DB`
- oracle-declaration reproducer：`0A0EA8607D2E07E6189ACC52B698E781CF742C6523C4D46FF3F02330AF1B779B`
- frozen live experiment report：`FC25C0E04D44ACCC0F5232B4F852056B870D82059F7542D4307EC966C0EB9300`

完整 candidate checksum 在文件完成後另產生；上述雜湊本身不代表 promotion。

## Normative judgment 分層

closure spec 的 `judgments` 是分類的 normative source，其他 prose 與 fixtures 是 derived views：

1. `GenericEdgeShape`：對每個 envelope 的每個 edge、且在 spec-id dispatch 前適用。只要求 exact keys、非空 role/type、合法 SHA-256、同 parent role 唯一；明示不要求目前 `EDGE_RELATIONS` 有 parent/role mapping。
2. `SupportedEnvelopeHeader`：GenericEnvelopeShape 成立且 spec-id 為本版時才檢查；必須同時有本版 version 與目前已知 artifact type，否則先 `FAIL`。
3. `SupportedEdgeRelation`：`iff SupportedEnvelopeHeader holds` 才適用；此時才判 `EDGE_RELATIONS[parent][role] = expected_type`。
4. `UnsupportedEnvelope`：GenericEnvelopeShape 成立但 spec-id 不支援時，結果唯一為 `UNKNOWN`，不執行 SupportedEdgeRelation，也不 traverse。

因此 future-artifact + future-edge witness 只有一個本版判定：`UNKNOWN`。若把同一 future artifact type 放進本版 supported spec-id，則在 SupportedEnvelopeHeader 以 `FAIL` 結束。

## Oracle declaration family binding

schema 現要求 typed `oracle_id`、`entrypoint` 與 `obligations`。外部 validator 以 `(family, mechanism, result_status)` 導出 exact `oracle_id/entrypoint/name/checks/obligations`，不能只靠多族共用的 `oracles.py` hash。9 個 valid-signature swaps 覆蓋 PARITY↔2-SAT、2-SAT SAT↔UNSAT，以及 oracle-id／entrypoint／name／checks／obligations 單欄替換；實際 family-selected oracle 仍 PASS，但 declaration provenance 使 record admission=false。

其餘 GateVal、admission/final/resource matrix、ValidateBytes、canonical/raw domain、role closure、signed operational map、PARITY/2-SAT transition/correctness execution、PROV-DERIVE 與 REF-TYPE regressions未改。

## 本地 Observation／Experiment

- 五代 tests：14/14 + 11/11 + 15/15 + 16/16 + 19/19 PASS，共 75/75。
- closure classification：20/20；scope checks：7/7；unexpected `[]`。
- oracle declaration：9/9 negative probes拒絕；3/3 positive controls接受；actual family oracle均 PASS。
- 42 個 run-record fixtures，0 manifest mismatch；6 個正向 records accepted。
- 43 fixture files + 94 artifact files = 137 outputs；立即重產 137/137 byte-identical。
- 2-SAT fixed-seed exhaustive cross-check：6 個 variable-count × 250 = 1500 PASS。
- v0.2.3 frozen manifest：121/121；v0.2.2：98/98。

robust 仍只涵蓋 pinned finite deterministic singleton I0 run；通過有限測試不是一般 soundness/completeness theorem。
