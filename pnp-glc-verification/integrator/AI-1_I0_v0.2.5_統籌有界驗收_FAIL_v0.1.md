# AI-1 I0 v0.2.5 統籌有界驗收

## 最終裁定

- Version: `v0.2.5`
- Date regime: Asia/Taipei `2026-08-09`，使用者明確放行的一次額外流程測試
- Disposition: `FAIL`
- Candidate state: `FROZEN / CANDIDATE_UNPROMOTED`
- Retained blockers:
  1. `CLOSURE-SUPPORTED-RELATION-RESULT-01`
  2. `ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01`
  3. `FROZEN-LIVE-REPORT-SCOPE-01`

本裁定不代表 P=NP、P≠NP、四層框架成立或不成立，也不代表演算法正確性被突破。它只裁定 frozen v0.2.5 acceptance package 尚不足以 promotion。

## 本輪流程與角色

本輪採單一建置者、freeze 後三個不重疊驗收面的順序：

1. AI-4 由 frozen v0.2.4 建置並凍結 v0.2.5。
2. AI-2 僅做 local conformance 與既定反例矩陣。
3. AI-3 僅做 formal/interface totality 與定義閉合。
4. AI-5 僅做 manifest-bounded engineering replay 與交付封裝核驗。
5. AI-1 統一核對身分、整合 disposition 並停止本輪。

AI-6、AI-7 本輪未啟動；各審查線沒有互相派工或啟動 successor。

## Frozen identity

- Candidate root: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- Manifest: `SHA256SUMS-v0.2.5-candidate.txt`
- Manifest entries: `166`
- Manifest SHA-256: `9D759DB19360E9716E372B7791C251626F658E5C4A185A297EEF6EA01DE9531E`
- AI-1 本機核對：manifest 與三份獨立報告的 SHA-256 均與交付值精確一致。
- 各線均回報 candidate manifest domain `candidate_root_writes=0` 或等價的前後 hash/length/mtime 不變證據。

## 分工結果

### AI-4：建置者 self-test

`SELF-TEST PASS / CANDIDATE_UNPROMOTED`。

- 六代 tests: `96/96 PASS`
- closure: `20/20` classifications + `17/17` scope/dependency checks
- advice: `4/4` negatives rejected、`3/3` legal none controls accepted、1 table-binding control 符合預期
- retained oracle: `9/9` negatives rejected + `3/3` controls accepted
- deterministic regeneration: `149/149` byte-identical

這些結果是候選建置證據，不單獨構成 promotion。

### AI-2：bounded local conformance

Disposition: `bounded PASS / assigned scope 無新 blocker`。

- `CLOSURE-JUDGMENT-COMPLETENESS-01`: `CLOSED/PASS`
- `ADVICE-DECL-LEDGER-01`: `CLOSED/PASS`
- 六個 normative judgment symbol 的 dependency target 可解析且無循環。
- advice 的直接 shape 矛盾由 schema 拒絕；schema-valid 的 family/mechanism 反向錯置由 external semantic binding 拒絕。
- 沒有重跑已充分確認的完整六代測試。

Report: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-redteam\outputs\AI-2_I0_v0.2.5_bounded_local_conformance_PASS_v0.1.md`

SHA-256: `B6751A9A6615D063FDD7BDD0AE6442CB9AF8DE7185A0D026291B03207FBF586F`

### AI-3：bounded formal/interface acceptance

Disposition: `FAIL / CLOSURE-SUPPORTED-RELATION-RESULT-01`。

- v0.2.4 的 undefined `GenericEnvelopeShape` / dependency defect 已關閉。
- typed advice 的雙向義務在指定 I0 domain 已關閉。
- 新殘餘問題：`judgments.SupportedEdgeRelation` 只有 applicability 與 predicate，沒有在 normative judgment 內明列 false/failure terminal，也沒有 true/success 的 `Traverse` transition。
- `normative_precedence` 又宣告 judgments graph 完整，並把頂層 algorithm/order 降為 derived-only；因此 supported-header=true 分支不能只從 normative graph 得到唯一、total 的結果。
- executable closure tests 全綠不消除這項 Definition/interface 缺口。

Report: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-formal\outputs\AI-3_I0_v0.2.5_bounded_形式接口唯讀驗收_FAIL_CLOSURE-SUPPORTED-RELATION-RESULT-01_v0.1.md`

SHA-256: `420E5C1FA78E3428F359629DA5EEFA319F652CB543DDB00070065EB56FB6E407`

### AI-5：bounded engineering replay acceptance

Disposition: `FAIL / ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01 + FROZEN-LIVE-REPORT-SCOPE-01`。

正面結果：

- 在完整 live root，五條要求的語義路徑皆符合預期。
- receipt-only mutation 顯示 validator 會自行派生 builder/admission 結果，而非信任 receipt 自報。
- 合法 PARITY streaming 與合法 2-SAT none-advice accepted；不一致 advice cases 按預期拒絕；coherent table binding 仍被既有 gates 阻止 admission。

Blocker 1：manifest-bounded runtime closure 不成立。

- 只含 166 個 manifest paths 的隔離 snapshot 執行官方 advice reproducer 時，因缺少 `oracles.py` 而 `ImportError`。
- manifest 收錄 `semantic_validator_v025.py` 與 `experiment_v025.py`，卻未收錄它們直接匯入且被當作 operational evidence pins 的 `oracles.py`、`parity.py`、`two_sat.py`，亦缺部分 package/script dependencies。
- 因而 live-root PASS 依賴 manifest 外 bytes；freeze manifest 不是可獨立執行的 runtime/evidence closure。

Blocker 2：frozen live-report scope 與 acceptance packet 敘述不一致。

- frozen live report 的 `two_sat.cases=2`，其 bytes 沒有 1500 case count 或 6×250 ledger。
- 1500-case loop 位於未納入 v0.2.5 manifest 的舊 `tests/test_two_sat.py`。
- 因此不能把 1500-case cross-check 歸因於 frozen live report；本輪 AI-5 也依有界規則沒有重跑該實驗。

Report: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-ai5\outputs\ai5-aerec-i0\AI5_v025_bounded_engineering_replay_acceptance_v0.7.md`

SHA-256: `15BD4596BA6AA87A99F531B5A7CCD5088354CDBC5F7E170FB57340CD617C4F6C`

## 整合判斷

AI-2 的 PASS 與 AI-3／AI-5 的 FAIL 並不矛盾：三者驗收域不同。AI-2 證明既定 conformance fixtures 在完整候選環境中符合指定規則；AI-3 指出 normative result graph 仍非 total；AI-5 指出 frozen package 無法在 manifest domain 內自行執行，且一項 live-report 證據歸屬超出 frozen bytes。

因此整體只能是 `FAIL`，但以下兩個本輪目標可保留為 bounded positive evidence：

- `CLOSURE-JUDGMENT-COMPLETENESS-01`: symbol/dependency closure `CLOSED/PASS`，但不包含新發現的 relation-result totality。
- `ADVICE-DECL-LEDGER-01`: supported I0 typed declaration/ledger binding `CLOSED/PASS`。

## Successor obligations（只記錄，未開工）

下一版本號若由 AI-1 日後放行，至少需：

1. 對 `SupportedEdgeRelation` 在 normative judgment 內明列 total 結果：false 的 failure terminal／no-traverse，以及 true 的 success／`Traverse` transition，並用機器檢查覆蓋 terminal-totality。
2. 由同一 manifest 收錄 validator、experiment、oracle、solver、package initialization、generator/reproducer 所需的完整 transitive runtime/evidence closure；在只複製 manifest paths 的隔離 snapshot 中執行官方命令。
3. 讓 frozen live report、manifest evidence 與 acceptance packet 的 case count／scope 精確一致；若沒有凍結 1500-case evidence，就刪除該歸因，若要主張則把可重現輸出與依賴納入 freeze。

本文件沒有建立、凍結、委派或驗收任何 successor。

## Stop state

- v0.2.5 保持 frozen、`CANDIDATE_UNPROMOTED`。
- AI-2、AI-3、AI-4、AI-5 本輪完成後待機。
- AI-6、AI-7 維持學術審查待機，未參與本輪。
- 不發布 Board success，不建立 shared repo，不啟動下一版，不作 P/NP 外推。
