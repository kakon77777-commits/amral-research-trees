# AI-1 I0 v0.2.3 追加分類：FAIL / ORACLE-DECL-FAMILY-01

- 日期：2026-08-09（Asia/Taipei）
- 審查型態：純本機、唯讀 software conformance / Definition-interface review
- 候選狀態：`CANDIDATE_UNPROMOTED`
- 本追加項：`FAIL / ORACLE-DECL-FAMILY-01`
- v0.2.3 整合 disposition：`FAIL / CLOSURE-EDGE-SCOPE-01 + ORACLE-DECL-FAMILY-01`
- `CLOSURE-CLASS-01` executable fix：`CLOSED / PASS`
- 外推邊界：無 Board success、無 shared repo promotion、無 P=NP 或 P≠NP 結論

## 1. Frozen identity 與唯讀邊界

- 候選根：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- manifest：`SHA256SUMS-v0.2.3-candidate.txt`
- manifest SHA-256：`7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817`
- 核對：121/121 exact，0 mismatch；並行 v0.2.4 路徑不屬 frozen v0.2.3 provenance domain。
- AI-1 的 candidate-root writes：`0`。所有產生簽章、trace、auth 與 fixture 的動作都只發生於隔離副本：
  `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-integrator\work\v023-oracle-decl-family-ai1`

## 2. 最小 conformance mutation

以 frozen `fixtures-v0.2.3/legit.json` 的 PARITY record 為基底，唯一實質宣告替換是將 `mechanism.oracle` 換成 frozen `2sat-sat.json` 的 oracle 宣告：

```json
{
  "checks": ["assignment"],
  "independent": true,
  "name": "independent 2-SAT certificate oracle",
  "sha256": "sha256:c8c5f6a0c132b11c56fd7964b737c1eb4f0b6a8674c7de8adcda50ca4b54efce",
  "version": "0.2.3"
}
```

之後同步 candidate projection、trace 與 operational map，使用既有非 production fixture key 產生有效 Ed25519 trace/auth，並重新推導 closure。問題族仍為 `PARITY`，mechanism 仍為 `parity-stream`。

AI-1 實測：

| 項目 | 結果 |
|---|---|
| Schema / structural | PASS / `true` |
| Trace authenticity | PASS |
| Artifact closure | PASS |
| Independent oracle execution | PASS（實際仍執行 PARITY oracle） |
| SemanticValidate | `true` |
| Admission | `true` |
| Final completion | `true` |
| Record accepted | `true` |
| Issues | `[]` |

隔離產物 SHA-256：

- fixture：`43243503483D51773BCA997EF23BF6CCEA7195AA344554F6059470698BA7EE23`
- trace：`808D8E26FE7E5E2ED8EAA125AD5CCF773D2F9EBEAD2D3BCEF4EC514789BA5138`
- auth：`CFF9E621E588106093207A915A1A4B117BE701A66EDEEBBF278C7477DA77C504`

## 3. 核讀結果

1. Frozen schema 把 `mechanism.oracle.name/checks/version/independent/sha256` 全列為 required；`name/checks` 沒有 annotation-only 或 nonnormative 標記。
2. Candidate projection 排除的只有 `validation_receipt`，所以 oracle object 受 projection/signature 完整性保護；簽章不會自行證明宣告的 family 語義為真。
3. `_actual_operational_reference_map` 與 `_expected_operational_reference_map` 對 oracle 只綁共用 `oracles.py` 的 source hash。PARITY 與 2-SAT 因此具有相同 oracle hash。
4. `_operational_reference_status` 對 oracle 只檢查 source hash、`version` 與 `independent`；`_family_context_issues` 也不檢查 `name/checks`。
5. `_independent_oracle_status` 正確依 `problem.family` 選擇 PARITY 或 2-SAT 驗證函式，故本例答案仍被正確驗證；它同樣不核對 oracle declaration 的 `name/checks`。
6. Frozen live report 同時宣告 `family_bound_contract_oracle_rule_invariant=true`。已接受 record 卻能在 PARITY 下宣告 2-SAT assignment obligation，與此 interface claim 不一致。

AI-2 另以五個有效簽章案例獨立確認：PARITY 的 name-only、checks-only、兩者同換；2-SAT SAT 宣告 UNSAT checks；2-SAT UNSAT 宣告 SAT checks。五例均 accepted 且 issues 空。這排除了「只有 display name 模糊」的限縮：`checks` 本身具有義務／provenance 語義。

## 4. 分類

`ORACLE-DECL-FAMILY-01` 是 accepted-record oracle declaration/provenance Counterexample，構成獨立 promotion blocker。

它不是：

- correctness 或 oracle-execution failure；
- signature failure；
- artifact-closure failure；
- resource/accounting 或 gate-matrix regression；
- P/NP 結論。

它與 `CLOSURE-EDGE-SCOPE-01` 相互獨立。因此 v0.2.3 的整體 disposition 為：

`FAIL / CLOSURE-EDGE-SCOPE-01 + ORACLE-DECL-FAMILY-01`

## 5. 後繼候選最低修正義務

1. 由外部 validator 推導 `ExpectedOracleDecl(problem.family, mechanism.id, candidate_result.status)`。
2. 規範性欄位至少包含 typed `oracle_id`、entrypoint 與 obligation/check set；只綁共用 source hash 不足以表示 family-specific oracle。
3. 對 record 的規範宣告做 exact family/status comparison。Schema conditional 可作第一層拒絕，但不能取代 SemanticValidate。
4. `name` 若只是顯示文字，應明確移入或標記為 annotation-only；`checks` 不得默認降格為 annotation。
5. 加入有效簽章 regression fixtures：PARITY↔2-SAT、2-SAT SAT↔UNSAT、name-only、checks-only、name+checks。

## 6. 可攜性與 scope observation

121-entry v0.2.3 manifest 是 frozen identity path set，不是完全自足的執行 bundle：manifest 內的 v0.2.3 generator/validator 仍會使用 parent root 的舊版 generator helper、runtime modules與三個 transitive legacy artifacts。AI-1 在隔離副本中以唯讀來源補入這些依賴後才執行重現。此項保留為既有 parent-path／bundle portability observation，不在本追加審查中升格為第三個 promotion blocker，也不改變上述已由 pinned validator 驗出的 ORACLE 結果。

## 7. 交叉核驗 provenance

- AI-3 formal classification addendum SHA-256：`517A1A31DFB4294A67C343011E1AA20BF088F76A31D483FD0439003913616BA6`
- AI-2 bounded local conformance report SHA-256：`4029F719B0B38C276A53854659D094B14A62D45D934913EF9A5FAEB7ED5B6661`
- AI-2 reproducer SHA-256：`0082644010D2302846E7A5949E2EFF9DB7F7A367B220DA2DFD9AE98882FFB09F`

以上只證明 frozen I0 v0.2.3 的局部 interface/conformance 性質；不證明四層框架，也不支持任何 P/NP 推論。
