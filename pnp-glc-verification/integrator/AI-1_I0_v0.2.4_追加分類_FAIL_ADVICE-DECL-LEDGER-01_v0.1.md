# AI-1 I0 v0.2.4 追加分類：FAIL / ADVICE-DECL-LEDGER-01

## 更新後 disposition

- v0.2.4 整體：`FAIL / CLOSURE-JUDGMENT-COMPLETENESS-01 + ADVICE-DECL-LEDGER-01`
- 本追加項：accepted-record declaration/ledger Counterexample。
- 性質：admissibility declaration 與 uniformity、generator、answer-access及resource ledger不一致。
- 不是：實際 truth-table 使用、correctness/oracle-execution failure、signature/closure failure、production authority claim或 P/NP 結論。
- 前一份 AI-1 report 維持不變：SHA-256 `FE7609E89D67A76D10E0D92CCC9362E534C261F98D0EB13BC25EA327961278F7`。

## 最小有效簽章見證

在隔離副本以 frozen `fixtures-v0.2.4/legit.json` 為基底，只把：

```text
mechanism.admissibility.advice = "none"
```

改成：

```text
mechanism.admissibility.advice = "one truth table per n"
```

其餘實質狀態仍為：

- `problem.family = PARITY`
- `mechanism.id = parity-stream`
- `uniform = true`
- `program_quantifiers = exists-one-program-for-all-input-lengths`
- `advice_generator_ref = null`
- `declared_answer_access = none`
- `ledger.description_bytes.advice = 0`
- `ledger.description_bytes.generated_tables = 0`
- advice generation time / peak space / peak output 全為 0
- trace observation仍為 no answer access，實際執行仍為 legit streaming PARITY。

重新同步 candidate projection、trace、operational map，使用既有 non-production fixture key 有效簽章並重算 closure後，AI-1 實測：

| Check | Result |
|---|---|
| Schema / structural | PASS / true |
| Trace authenticity | PASS |
| Artifact closure | PASS |
| Actual family oracle | PASS |
| SemanticValidate | true |
| Admission | true |
| Final completion | true |
| Record accepted | true |
| Issues | `[]` |

隔離產物 SHA-256：

- fixture：`81D6048363716A3CA969046B45365AA4DD3844CB5F59CFBAE5FF4BCDE3DB3012`
- trace：`CAEC459ED076CF28F1DA5919CF8F97730043C57431F3E836A684C03EA1241306`
- auth：`63C15C176E2D017E79889E0EB515196D72959B559F899416AB101D02DEE9B07B`

所有寫入均只在 AI-1 隔離副本；frozen candidate 153 paths未修改。

## Frozen schema／validator核讀

1. `admissibility.advice` 位於 `mechanism.admissibility`，是 schema-required 欄位；schema只要求 string，沒有 annotation-only、nonnormative 或 family/mechanism conditional。
2. Candidate projection僅排除 `validation_receipt`，所以 advice declaration受簽章完整性保護；完整性不等於宣告語義為真。
3. `_uniformity_status` 只核 `uniform` 與 `program_quantifiers`。
4. `_advice_generation_status` 只在 `mechanism.id == parity-table-family` 時核 ledger table costs；對 `parity-stream` 直接回 `not-applicable`。
5. `advice_applicable` 只由 `advice_generator_ref`、ledger advice bytes及generated-table bytes推導；完全不讀 `admissibility.advice`。
6. Answer-access gate只比對 declared/observed access；resource derivation只驗 trace與ledger。故自由字串可與所有受驗證事實矛盾而不產生 issue。
7. Frozen研究介面把 advice、generator、description bytes、generation cost與answer access列為 admission/resource accounting 的實質項目；因此此欄不能在未標示的情況下被默認降格為顯示文字。

## 分類理由

這不是把未記帳的 truth table 偷渡進實際計算；trace、ledger與答案仍是 legit streaming PARITY。反例證明的是另一件事：一筆 `semantic_ok=true`、`admission=true`、`final=true` 的 accepted record，可以在必填 admissibility declaration中聲稱使用 per-length truth tables，同時由同一 record 的 generator、uniformity、answer-access與ledger證據證明沒有使用。

因此 `ADVICE-DECL-LEDGER-01` 是 accepted-record declaration/provenance consistency blocker，與純 formal 的 `CLOSURE-JUDGMENT-COMPLETENESS-01` 相互獨立。

## 最低後繼修正義務

1. 將自由字串改成規範性的 typed `advice_mode`，至少區分 `none` 與 `per-length-truth-table`；若保留自然語言，另置於明示的 annotation 欄。
2. 由 `ExpectedAdviceDecl(problem.family, mechanism.id)` 推導並 exact compare mode。
3. `none` 必須雙向一致於：`advice_generator_ref=null`、advice/generated-table bytes為0、generation account為0，以及對應的answer-access模式。
4. `per-length-truth-table` 必須一致於：nonuniform program quantifier、pinned generator ref、truth-table access、實際table/advice bytes與generation account。
5. Schema conditional可作第一層拒絕，但外部 SemanticValidate仍須從 family/mechanism、trace與ledger重新推導。
6. 新增有效簽章雙向 fixtures：宣告 table但ledger/generator為none；宣告 none但ledger/generator非零；逐欄同步但uniformity或answer-access不一致。

v0.2.4 應保持 frozen、`CANDIDATE_UNPROMOTED`；修正另起後繼版本。無 Board success、shared repo promotion或 P/NP 外推。
