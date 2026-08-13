# I0 v0.2.5 candidate 狀態

目前狀態：`CANDIDATE_UNPROMOTED / pending AI-1 managed bounded acceptance`。

父版是 frozen v0.2.4，manifest SHA-256 `73ED3607EAD3F50502DCEFA3142DFFEE01AAC8576C045F05CA96DEB9669F77FE`、153 個路徑逐項不變。v0.2.4 的最終分類是 `FAIL / CLOSURE-JUDGMENT-COMPLETENESS-01 + ADVICE-DECL-LEDGER-01`；本版只處理這兩項，不建立 v0.2.6、不發布 Board success、不建立 shared repo，也不提出 P=NP 或 P≠NP 結論。

## 固定介面

- schema：`8A799A869CF6CDD17D1191A9D859AB25899FF9E651B454725814E4B458B92596`
- external validator：`2571B418612414948A80967B868B910B3714D1FB63F3C79387BF77EC5CA71C5A`
- candidate projection spec：`42348657BD0475442B266385D0C88E8685F21334D78A49ECB0CF64D2D3977E18`
- artifact closure spec：`DFC5A11CF6296F4D83B054B7F4F903E509B0982F9C61D231D423E7F78B5FF71D`
- evidence role spec：`6B49D3907209D5EDEED839FE698A25EA96451CDCF7534F2383125E9F3F98C088`
- fixture manifest：`EC0603B3D3B6F4E3189D7936455B146C61A16291744C86E59B160CFEDBD677AD`
- closure-classification fixture manifest：`09E9E6E4C0F1528C8239606DB6CC0A724B1031973F8D79F504FC22A2793A9159`
- closure reproducer：`87255148DE527CD6247DD28BE19DB882D63DB8C9441726103C0328D06D8C6194`
- advice reproducer：`A414C1A5BAD1F99AA6B34705EFC1C8D5C21BFD40D86D2EEABFB9A447F76C72BA`
- retained oracle reproducer：`50CE3893CD2A0C00F65D42370AD3E3DA1889622410D241D0F50EC3B94C2F07E1`
- frozen live experiment report：`1552B708D88D96365AF168D4A318DA2737EF4B06D5B700CEAA126BA27C6154F1`

完整 candidate checksum 在所有文件完成後產生；上述雜湊與本地自測不代表 promotion。

## 本輪兩項修補

1. closure 的 `judgments` 現明確包含 `OpaqueLeaf`、`GenericEdgeShape`、`GenericEnvelopeShape`、`SupportedEnvelopeHeader`、`SupportedEdgeRelation`、`UnsupportedEnvelope`。每個 judgment 有可機讀 `depends_on`；依賴必須是 fully-qualified `judgments.<name>` 且解析到同一物件中的 key。`GenericEnvelopeShape.false_result` 明定 `Malformed / FAIL / do not traverse`；頂層 shape 與 algorithm 文字明標 derived view。
2. `mechanism.admissibility.advice` 自由文字已移除，改成 typed `advice_mode = none | per-input-length-truth-table`。schema 封閉 record 內部矛盾；external validator 的 `ExpectedAdviceDecl(family, mechanism)` 再雙向比對 generator ref、uniformity／program quantifier、declared/observed answer access、advice/generated-table bytes與 generation time/space/output。

## 本地 Observation／Experiment

- 六代 tests：14 + 11 + 15 + 16 + 19 + 21 = 96/96 PASS。
- closure：20/20 executable classifications；17/17 scope/dependency checks；unexpected `[]`。
- advice：4/4 negatives拒絕；3/3合法 none-advice controls接受；table-binding control符合但因既有 uniformity/budget gates不准入。
- retained oracle：9/9 valid-signature negatives拒絕；3/3 controls接受。
- 46 個 run-record fixtures，0 manifest mismatch；6 個正向 records accepted。
- 47 fixture files + 102 artifact files = 149 outputs；立即重產 149/149 byte-identical。
- live report保留 fixed-seed 2-SAT 1500-case exhaustive cross-check。
- v0.2.4 frozen manifest：153/153；v0.2.3：121/121；v0.2.2：98/98。

robust 仍只涵蓋 pinned finite deterministic singleton I0 run。有限測試不是一般 soundness/completeness theorem，也不改變一般 SAT 或 P/NP 狀態。
