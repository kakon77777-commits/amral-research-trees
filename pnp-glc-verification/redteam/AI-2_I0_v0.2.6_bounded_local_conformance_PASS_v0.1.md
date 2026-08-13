# AI-2 I0 v0.2.6 bounded local conformance acceptance

## 裁定

- 日期：Asia/Taipei `2026-08-10`
- 版本：frozen `v0.2.6 candidate`
- Disposition：`BOUNDED PASS / assigned scope 無 promotion blocker`
- Candidate state：`READ-ONLY / CANDIDATE_UNPROMOTED`
- 證據分類：frozen-byte identity、Definition/interface conformance Observation、既有 signed-fixture Experiment；不是一般 soundness/completeness theorem。

本裁定只涵蓋 AI-1 指派的三項 predecessor conformance judgments、最小 typed-advice/oracle retention，以及 v0.2.6 新增欄位的具體交叉一致性核讀。它不構成 promotion，也不外推至 P/NP。

## Frozen identity 與唯讀 provenance

- Root：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- Manifest：`SHA256SUMS-v0.2.6-candidate.txt`
- Manifest SHA-256：`2E1C58A5CE85833DAC708DF21BD4FC4AC845FFC3182AAB16BF568F50AC502357`
- Manifest entries：`216/216` 可解析、唯一、存在且內容 SHA-256 精確一致；missing/mismatch/duplicate 均為 `0`。
- Schema SHA-256：`EB22CB899869B2A43DCD2DBBD3F4C9F7C0A8921AE361EF2207DB1039B1C875EE`
- Validator SHA-256：`3F87207F26A21CA1B750B70170EBE28090F97C0670FB6F0CA88ED04296244D72`
- Closure spec SHA-256：`B635E86CB5FBDB89865ED4343F052247E98A245DD2194726066AEF01489F758F`
- Runtime descriptor SHA-256：`B3019C2C62B2689CF897F787BEAADCEA19663C820DAFBED97B6AE6FC46CF8217`
- Frozen live report SHA-256：`0812D561EE31C8F1C7B6B73DD6D73DACF70CF1E981600B551655597642B363DB`
- Frozen isolation report SHA-256：`0A911965CD262B0B2205605F4834D39779A4DFFFC4E58F26AD8DFE360EEEB902`
- 首次與末次內容核對均為 `216/216 exact`；末次 manifest-path-set 前後 SHA-256／length／mtime 比較為 `0` changes。
- `candidate_root_writes=0`。

依 AI-1 scope correction，AI-2 未建立可供本次驗收採用的 isolation snapshot，也未完成或採用 manifest-only command replay；該工程重跑屬 AI-5 範圍。此項未重跑不是本 conformance scope 的 blocker。本報告只寫入 AI-2 自有 outputs folder，未修改 candidate root。

## 三項 predecessor judgments

### 1. CLOSURE-SUPPORTED-RELATION-RESULT-01

Disposition：`CLOSED/PASS`（Definition/interface bounded scope）。

Frozen `judgments` graph 現已明列：

- `SupportedEdgeRelation.false_result` = `Malformed / FAIL / terminal=true / do not traverse`；
- `SupportedEdgeRelation.true_result` = `Traverse / PASS / terminal=false / next_transition=judgments.SupportedTraversal`；
- relation totality 對每個 applicable envelope 唯一選出 false 或 true；
- `SupportedTraversal.fixed_point_results` 對 reachable FAIL、reachable UNKNOWN、queue-empty all-PASS 給出互斥的 `FAIL/UNKNOWN/PASS` terminal trichotomy；
- dependency 與 transition refs 使用 fully-qualified `judgments.<name>`，所引 symbols 均存在。

Frozen live report 的 `closure_supported_relation_totality` 三項檢查皆為 true，`all_conformant=true`。未見 predecessor 的 false/true branch 缺口復現。

### 2. ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01

Disposition：`CLOSED/PASS`（declared closure-shape conformance；不主張 AI-2 獨立 isolation replay）。

Machine-readable runtime descriptor 交叉核讀結果：

- `required_paths=209`，全部位於 216-entry top-level manifest，missing=`0`；
- `python_source_closure=20`；
- `local_import_edges=31`；
- 六條 official acceptance commands 的 target 均在 source closure 與 required paths；
- build inputs、resolved-content evidence、operational evidence 與 AST-derived sources 均包含於 required paths；
- schema、closure spec、live report與 runtime descriptor本身均受 required-path/manifest domain 覆蓋。

既有 frozen `runtime-isolation-report.v0.2.6.json` 記錄 `all_pass=true`、216 manifest paths、required-path omission=`0`、snapshot extra/missing/changed=`0`、`candidate_root_source_dependency=false`。AI-2 只把它當 frozen evidence 讀取，不把它升格為自己重跑所得的普遍結論。

非阻斷 Observation `OBS-RUNTIME-EDGE-COUNT-DOC-01`：`CURRENT-v0.2.6-candidate.md` 與 `ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01-REPRO-v0.2.6.md` 的 prose 摘要仍寫 `29 local import edges`；machine descriptor 與 `VALIDATION-REPORT-v0.2.6-candidate.md` 均為 `31`，且 31 條為 AST-derived exact set。這是 derived prose count drift，不改變 machine closure、required-path coverage 或本次 disposition；後續文件可 append-only 更正。

### 3. FROZEN-LIVE-REPORT-SCOPE-01

Disposition：`CLOSED/PASS`（count/seed/pointer coherence only）。

Frozen live report 內部一致性如下：

- JSON pointer：`/two_sat/deterministic_crosscheck`；
- generation command、report location與 replay command 均明列；
- seed=`20260809`，與 `parameters.two_sat_crosscheck_seed` 及 generation command 一致；
- variable counts=`[1,2,3,4,5,6]`，每層 `250` cases，總數 `1500`；
- strata 彙總 `SAT=1223`、`UNSAT=277`，合計 `1500`；
- mismatch=`0`、certificate failure=`0`；
- declared evidence digest=`2F472DB6486459BC6502AA0ABDF1B79FD361D274F41DFE461E14C197F414EBEF`。

依本輪限制，AI-2 沒有重算 1500 cases；上述裁定只確認 frozen bytes 的 count/seed/pointer/ledger coherence，並保留既有 replay output 的 provenance，不聲稱本輪獨立演算法重驗。

## Typed advice、oracle 與 external derivation retention

採最小既有 signed-fixture evidence：

- `advice-table-with-null-generator-zero-ledger`：trace authenticity=`pass`，direct advice match=false，structural=false，accepted=false；
- `advice-none-with-table-generator-ledger`：trace authenticity=`pass`，direct advice match=false，structural=false，accepted=false；
- `parity-stream-with-coherent-table-advice` 與 `parity-table-with-coherent-none-advice`：structural=true，但 family/mechanism declaration binding 不符，accepted=false；
- `parity-with-2sat-oracle-checks-only` 與 `2sat-with-parity-oracle-declaration`：實際 family oracle 仍為 `pass`，錯誤 declaration 仍 accepted=false；
- 合法 controls `legit` 與 `2sat-sat` 均 structural/semantic/admission/final/accepted=true。

Validator frozen source仍自行導出 `expected_gates`、`expected_admission`、`expected_correctness` 與 `expected_completion`，再逐欄比較 receipt；不以 candidate/receipt boolean 代替外部派生。v0.2.5→v0.2.6 transport schema 的功能差異限於版本 constants/description，validator 的功能差異限於版本 pins、IDs 與對應診斷文字；未見 typed-advice/oracle binding 被新欄位削弱。

## Cross-field review 與最小反例門檻

- 未發現能使不一致 record 由 `record_accepted=false` 變為 true，或使三項 predecessor conformance judgment 重新失敗的最小 witness。
- 唯一新差異為 `OBS-RUNTIME-EDGE-COUNT-DOC-01` 的 29/31 prose 計數漂移；依 machine source precedence 與 assigned rule，列 Observation，不列 blocker。
- 本次沒有新增 mutation、沒有重跑完整六代 matrix、沒有重跑 1500 cases。

## Nonclaims / stop state

- 本報告不代表 v0.2.6 已 promotion；候選仍為 `CANDIDATE_UNPROMOTED`。
- 本報告不是 validator completeness、一般 artifact closure soundness、演算法正確性或複雜度定理。
- 不發布 Board success、不建立 shared repo、不建立 successor、不作 P=NP 或 P≠NP 推論。
- 回傳 AI-1 後，AI-2 立即待機，不聯絡其他 AI。
