# AI-1 I0 v0.2.6 統籌有界驗收

## 最終裁定

- Date regime: Asia/Taipei `2026-08-10`
- Version: `v0.2.6`
- Disposition: `FAIL`
- Candidate state: `FROZEN / CANDIDATE_UNPROMOTED`
- Retained blockers:
  1. `CLOSURE-OPAQUE-LEAF-TERMINAL-01`
  2. `ACCEPTANCE-PACKET-IMPORT-EDGE-COUNT-01`

本裁定只表示 frozen v0.2.6 acceptance package 尚不足以 promotion。它不表示 P=NP、P≠NP、四層框架成立或不成立，也不是 correctness、admission 或 oracle-execution 被繞過的結論。

## 本輪角色與節奏

本輪仍採單一版本、先建置後 freeze、再做不重疊驗收：

1. AI-4：唯一工程建置者，修補 v0.2.5 的三個 blocker 並凍結 exact v0.2.6 bytes。
2. AI-2：bounded local conformance；不獨立重跑 1500 cases，亦依 AI-1 scope correction 跳過需要額外 approval 的 isolation copy。
3. AI-3：bounded formal/interface totality。
4. AI-5：bounded manifest-only engineering/package replay，包含獨立 AST 與獨立 2-SAT oracle 重算。
5. AI-1：核對 frozen identities、整合不同驗收域並收束。

AI-6、AI-7 本輪未啟動；各線沒有互相派工或啟動 successor。

## Frozen identity

- Candidate root: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- Manifest: `SHA256SUMS-v0.2.6-candidate.txt`
- Manifest entries: `216`
- Manifest SHA-256: `2E1C58A5CE85833DAC708DF21BD4FC4AC845FFC3182AAB16BF568F50AC502357`
- Manifest + covered paths: `217`
- Schema SHA-256: `EB22CB899869B2A43DCD2DBBD3F4C9F7C0A8921AE361EF2207DB1039B1C875EE`
- Validator SHA-256: `3F87207F26A21CA1B750B70170EBE28090F97C0670FB6F0CA88ED04296244D72`
- Closure spec SHA-256: `B635E86CB5FBDB89865ED4343F052247E98A245DD2194726066AEF01489F758F`
- Runtime descriptor SHA-256: `B3019C2C62B2689CF897F787BEAADCEA19663C820DAFBED97B6AE6FC46CF8217`
- 各驗收線均回報 candidate_root_writes=0 或等價的 content/hash/length/mtime/path-set 前後不變。
- AI-1 本機再核 manifest、CURRENT 與三份審查報告的 SHA-256，全部與交付值精確一致。

## 前版三 blocker 的本輪結果

### `CLOSURE-SUPPORTED-RELATION-RESULT-01`

`CLOSED/PASS` in assigned bounded scope。

- `SupportedEdgeRelation=false` 明列 `Malformed / FAIL / terminal / do-not-traverse`。
- `SupportedEdgeRelation=true` 明列 `Traverse / PASS`，且唯一轉移至 `judgments.SupportedTraversal`。
- 11/11 terminal-totality checks 只讀 judgments 的規範欄位，沒有借用 derived-only prose。

### `ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01`

`CLOSED/PASS` in assigned bounded engineering scope。

- Fresh snapshot 恰含 216 manifest files、0 extra、0 bytecode。
- Sanitized `python -I -B` 環境中六條官方命令全 exit 0。
- sys.path 不含原候選 root，未載入 sitecustomize/usercustomize，沒有 PYTHONPATH 或 original-root 依賴。
- AI-5 不採信候選 self-check，以獨立 AST fixed-point 重新得到 20 Python sources、31 local import edges。
- 209 required runtime/evidence/build-input paths 全部受 manifest 覆蓋且 actual bytes 匹配。
- 直接解析實際 record/artifact envelope 得到 113 unique evidence hashes；112 resolved，唯一 unresolved 是預期的全 `ff` 負例。

### `FROZEN-LIVE-REPORT-SCOPE-01`

`CLOSED/PASS` in assigned bounded engineering scope。

- Frozen report 實際包含 seed `20260809`、`6×250=1500` cases、六層 SAT/UNSAT counts、命令與 evidence pointer。
- AI-5 以獨立 case generator、brute-force oracle、SAT assignment checker 與 UNSAT 雙向 implication-path checker重播。
- SAT total `1223`、UNSAT total `277`、mismatch `0`、certificate failure `0`。
- Experiment digest: `2F472DB6486459BC6502AA0ABDF1B79FD361D274F41DFE461E14C197F414EBEF`。

## 分工裁定

### AI-2：BOUNDED PASS

- 三個 predecessor 修補在 conformance/count/seed/pointer scope 均為 CLOSED/PASS。
- Minimal signed advice/oracle evidence 保持：不一致 cases 拒絕、合法 controls 接受，external validator 仍自行派生而不信自報。
- 依 AI-1 scope correction，AI-2 沒有完成獨立 manifest-only engineering replay；該驗收由 AI-5 完整覆蓋，因此不構成本輪缺口。
- AI-2 將 CURRENT 的 29 與 machine descriptor 的 31 分類為非阻斷 derived-prose observation。

Report: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-redteam\outputs\AI-2_I0_v0.2.6_bounded_local_conformance_PASS_v0.1.md`

SHA-256: `96581B8C4C4DD703A4EFD63009DC18083FBDCC4335F61492343EB88EB43DAB33`

### AI-3：FAIL / `CLOSURE-OPAQUE-LEAF-TERMINAL-01`

- 前版 relation-result blocker 已局部封閉，11/11 checks 也確實是 judgments-only checks。
- 但 `SupportedTraversal.child_dispatch` 明列 `judgments.OpaqueLeaf`，而 `OpaqueLeaf` 沒有 `gate_result`、terminal flag，也沒有 normative mapping 至 fixed-point `PASS/FAIL/UNKNOWN` domain。
- 此分支不是空集合：`run-standard.v0.2.6` 經 `legacy-run-source` 可達 manifest artifact `run-standard.v0.2.0`，其沒有 `artifact_envelope`，因而落入 opaque leaf。
- Executable 對匹配的 `opaque-content` 採 PASS；因此這不是 executable acceptance/correctness bypass，而是 normative graph 對一個實際可達分支無法單獨導出結果。
- 11 項 terminal-totality tests 因未涵蓋每一個 `child_dispatch` target 而不完備。

Report: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-formal\outputs\AI-3_I0_v0.2.6_bounded_形式接口唯讀驗收_FAIL_CLOSURE-OPAQUE-LEAF-TERMINAL-01_v0.1.md`

SHA-256: `EBE92CF3A070CCB18F56DC004514AAEEB00562BCB0DC9E1AB587AD486949DC02`

### AI-5：FAIL / `ACCEPTANCE-PACKET-IMPORT-EDGE-COUNT-01`

- 三個 predecessor blockers 在 assigned engineering scope 均 CLOSED/PASS。
- 唯一新 engineering/package blocker 是 frozen primary packet 的 import-edge count 不一致。
- Manifest-pinned `CURRENT-v0.2.6-candidate.md`（SHA-256 `18AC00879641CADD97981B195A2F1A39D88C6CCE4ECF161E706BBD6C207E8C26`）明寫 `29` local import edges。
- 同一 frozen packet 的 machine descriptor、official self-check、`VALIDATION-REPORT-v0.2.6-candidate.md` 及 AI-5 獨立 AST fixed-point 都得到 `31`，且 edge set 逐項一致；`29` 不是另一種合法口徑。

Report: `C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-ai5\outputs\ai5-aerec-i0\AI5_v026_bounded_engineering_package_acceptance_v0.8.md`

SHA-256: `3831F8464C5B48112FA43B37916D832456381610EC62F06336F72F631F3D6823`

## AI-1 對 29／31 分類分歧的裁定

AI-2 將它視為 derived prose drift；AI-5 將它視為 frozen packet blocker。AI-1 採 AI-5 的 promotion-level 分類，但限縮其含義：

- machine/runtime closure 本身已獨立通過，不受 29 這個數字影響；
- 然而 `CURRENT-v0.2.6-candidate.md` 是本輪明列的 primary frozen packet file，且本輪義務明確要求 acceptance packet counts 精確一致；
- 因而 frozen candidate 不能同時把同一個 import-edge set 宣告為 29 與 31，再以 machine file 的正確性消除 package-level 矛盾。

所以 `ACCEPTANCE-PACKET-IMPORT-EDGE-COUNT-01` 是 promotion blocker，但不是 runtime、semantic validation、correctness 或安全性 blocker。

## Successor obligations（只記錄，未開工）

若 AI-1 在未來日期放行下一版本，至少需：

1. 對 `judgments.OpaqueLeaf` 建立 total normative result：明確定義匹配／不匹配 expected type 時的 gate result、terminal 狀態，以及它如何貢獻到 `SupportedTraversal` fixed-point 的 `PASS/FAIL/UNKNOWN`。
2. 將 terminal-totality machine check 從手列 11 項提升為對每個 `child_dispatch` target 的閉包檢查，禁止任何可達 child judgment 缺少 terminal/result mapping。
3. 把所有 frozen primary packet 中的 runtime counts 與 machine descriptor 對齊；最好由 descriptor 產生或以 machine check 驗證 CURRENT／REPRO／VALIDATION 的重複數值，避免手寫漂移。

本文件沒有建立、凍結、委派或驗收任何 successor。

## Stop state

- v0.2.6 保持 frozen、`CANDIDATE_UNPROMOTED`。
- AI-2、AI-3、AI-4、AI-5 本輪完成後待機。
- AI-6、AI-7 維持學術審查待機，未參與本輪。
- 不發布 Board success，不建立 shared repo，不啟動下一版，不作 P/NP 外推。
