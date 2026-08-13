# Canonical candidate-record projection／trace binding：bounded red-team v0.2

日期：2026-08-09（Asia/Taipei）  
角色：AI-2 Red Team  
範圍：工程 provenance admission gate；**不涉及、也不外推 P/NP**。

## 裁定

**FAIL — 新 admission blocker `PROV-DERIVE-01`。**

這不是否定整個 v0.2：凍結版已修掉 direct self-hash cycle、舊式 TOCTOU、直接 event ref 漏解，以及 PARITY 錯答只信 trace 的問題；14 個原生測試全數通過。失敗點較窄：現行 `DerivesRecord` replay 對部分 transition／ledger 欄位仍只驗「record 與 trace 互相鏡射且 hash chain 自洽」，尚未驗「確由 pinned transition 執行或可信量測導出」。

若 `artifact_root` 的「trusted」是額外、已證明的強前提——只有 capability sandbox 能寫入、trace origin 有可驗證 attestation、候選者不能提交同步偽造 trace——則本負例被該前提排除，狀態可降為 **Attack Obligation**。目前 validator 可見的是 content hash、producer 字串與 gate booleans；它們本身不證明 origin，因此 validator-alone 的 admission sufficiency 仍被反例擊中。

## 凍結 provenance

| Artifact | SHA-256 |
|---|---|
| schema | `1ad5afa3a76e56ad5c9d0b79df34b897e337606093d282693932085bf1af297c` |
| validator | `4c50be9ef563644bc29f3dceefb9d9205056631847980fcc763d1e4ba25eb771` |
| projection spec | `9966b86dbc3884e3327306ff1fefaf21efbde705ee0f10739755be27c73a1991` |
| fixture manifest | `00fa70a6b8f8fa8029d5c0500064fad4310811e5cdbcc8efdecc939c9e19f7b2` |
| AI-2 reproduction | `e68bb2c26bf1655f34508ef418d51761bb689fb9e27e20a2eeb37f3c6fd7080d` |

原生測試：`python -m unittest discover -s tests -v` → **14/14 PASS**。  
紅隊重現：`python candidate_projection_redteam_repro.py`。

## 六個攻擊面

| ID | 攻擊命題 | 最小負例／觀察 | 凍結版狀態 | 可修正性 |
|---|---|---|---|---|
| N1 | projection 不得含自己的 hash、trace hash 或 validator receipt | 改寫 `validation_receipt.candidate_projection_sha256` 前後，projection hash 必須不變 | **PASS**：整個 `validation_receipt` 被排除 | 保持 schema-first、closed root 與 field ownership；任何新 derived field 仍只能進 receipt |
| N2 | 「canonical JSON」必須跨實作產生唯一 bytes | `{"x":"\n"}` 與 `{"x":"\u000a"}` 是同一 JSON 值、不同 SHA-256；scalar ordering 也不同於 JCS UTF-16 ordering | **Attack Obligation**：目前 Python 實作固定，但規格文字仍未逐字節指定 control escape | 加 normative serializer 規則與 conformance vectors，或明確採用既有 canonicalization standard |
| N3 | validator-derived fields 不得混入 candidate projection | 只改 `final_completion` 等 receipt 欄位時 hash 必須不變 | **PASS**：derived fields 全在 excluded receipt；root 亦 `additionalProperties:false` | projection 前必須先驗 pinned schema；不要對任意 mapping 直接做 denylist projection |
| N4 | hash-match/replay 必須證明 ledger/result 由執行導出 | 下列 `F_state(v)`、`F_link(h)` 在同步 record/trace 並重算所有 hashes 後仍 admission | **FAIL — `PROV-DERIVE-01`** | 實際重放 pinned transitions；逐欄重算 ledger；或驗證 sandbox-origin attestation 與 raw measurement receipts |
| N5 | hash、parse、use 必須使用同一 bytes，不能驗後換檔 | 建索引後把 path 內容由 `trusted:true` 換成 `false` | **PASS**：load 仍解析原先 in-memory bytes snapshot | 維持一次讀取；後續 execution 亦須使用該 snapshot，而非再開 path |
| N6 | 所有 correctness-bearing content refs 必須閉合解析 | event 的 `transition_rule_ref` 換成不存在的合法 hash | **PASS（direct）**：以 `unresolved-ref` fail closed | 再明定 resolved artifact 內 typed refs 的遞迴 closure；區分 content-ref 與 digest-only commitment |

## 最小反例族 `PROV-DERIVE-01`

基底是凍結版 `legit` PARITY fixture；答案保持正確，故本反例不攻擊 oracle correctness。

### `F_state(v)`：ledger mirror，不是 derivation

對任意整數 `v`（實測 `v=999`）：

1. 將 `record.ledger.counts.states := v`；
2. 將 `trace.resource_samples.counts.states := v`；
3. 重算 candidate projection hash、trace hash、receipt evidence set；
4. 其他事件、答案與獨立 oracle 不變。

結果：`record_accepted=true`。因此 gate 對 `states` 只檢查 `trace.resource_samples == ledger`。同一 validator 對所有 `v` 都沒有可觀察的原始量測或 event fold 來判斷哪個值是執行所得。

### `F_link(h)`：hash chain，不是 transition execution

任取 64-hex digest `h`（實測 `e…e`）：

1. 將第一事件 `output_sha256 := h`；
2. 將下一事件 `input_sha256 := h`；
3. 將 trace events 同步為相同值；
4. 重算 projection／trace／receipt hashes；答案與 oracle 不變。

結果：`record_accepted=true`。validator 證明了相鄰 digest 相等，但沒有以 resolved `transition_rule_ref` 對 pinned input bytes 執行 transition 並重算 output digest。

### 被攻擊命題、最小前提與失敗條件

- 被攻擊命題：`record_accepted=true` 足以推出「events、ledger 與 candidate result 具有 pinned execution／measurement provenance」。
- 最小前提：呼叫端允許一組 content-addressed、彼此同步但 origin 未被 validator 驗證的 record 與 trace 進入 artifact root。
- 不攻擊的命題：凍結版會獨立拒絕錯誤 PARITY 答案；紅隊已重現此修補為 PASS。
- 反例失效條件：artifact root 的寫入者是已驗證的唯一 sandbox，且 trace origin、transition execution、raw resource measurements 均有 validator 可驗的 attestation／receipt。這些條件必須成為明示 admission premise，而不是 `trusted` 一字隱含。

## Canonicalization 最小負例與界線

凍結 validator 已做到：duplicate-key rejecting parser、NFC gate、float／NaN／Infinity 拒絕、安全整數範圍、receipt exclusion。仍需補規格的最小跨實作向量：

- control escape：short escape `\n` 還是 `\u000a`；兩者解析值相同但 bytes/hash 不同；
- key ordering：本規格採 Unicode scalar-value ordering，RFC 8785 JCS 採 UTF-16 code units；鍵 `U+E000` 與 `U+1F600` 的順序相反；
- normalization：本規格先拒絕 non-NFC；JCS 本身不做 normalization，而要求保留輸入字串；
- duplicate property：必須在 raw-byte parser 拒絕，不能先以 last-wins parser 折疊後再 hash。

RFC 8785 明定 duplicate names 禁止、NaN/Infinity 拒絕、UTF-16 排序與 UTF-8 輸出，可作為比較基線，但目前 v0.2 是自訂 scheme，不能只標作 JCS。[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html)

## 准入條件

1. **Acyclic ownership DAG**：`candidate projection → trace → external receipt`；projection 使用 exact allowlist，永不含 receipt、trace hash 或 validator verdict。
2. **Schema-before-projection**：只接受 pinned schema 驗過的 raw JSON bytes；mapping API 不得繞過 duplicate／Unicode／number-domain gates。
3. **Normative canonical bytes**：逐字節指定 escaping、integer spelling、scalar ordering、UTF-8、NFC reject policy，並提供跨語言 test vectors；建議加入 domain separator 與 spec hash。
4. **Trace authenticity**：validator 必須親自啟動 pinned sandbox，或驗證 trace 的簽章／attestation及 write-once origin；`producer` 字串與 content hash 只證 identity，不證 origin。
5. **Transition derivation**：每一 event 以 pinned `transition_rule_ref`、pinned input bytes 與明定環境實際重放；重算 output bytes/hash、state、representation 與 status。
6. **Ledger derivation**：`time_ns`、debt、counts 等可 fold 欄位由 events 重算；space／precision／admission costs 等不可 fold 欄位須由 content-addressed raw measurements 或可信 attestation 重算／驗簽。只比較 `resource_samples == ledger` 不足。
7. **Correctness separation**：保留獨立 oracle／contract checks；「答案正確」與「答案由申報機制算出」分成不同 gates。
8. **Reference closure**：direct event/certificate refs 必須解析；resolved artifacts 內明定為 `content-ref` 的欄位遞迴閉包解析。純 digest commitment 必須另有型別，不能假裝可解析 ref。
9. **Same-byte snapshot**：hash、parse、proof／program execution 與 replay 全用同一 immutable bytes snapshot；不得在 hash 後重開 pathname。
10. **Fail-closed claim scope**：在 4–6 未滿足時，可將目前結果命名為 `StructuralReplayPass`／`RecordTraceConsistencyPass`，不可升格為 execution provenance admission。

## 最終狀態

- **Counterexample-to-provenance-sufficiency**：`PROV-DERIVE-01`（適用於 validator-alone 或 origin 未驗證的 artifact root）。
- **PASS**：N1、N3、N5、N6 direct closure，以及錯誤 PARITY answer 的獨立拒絕。
- **Attack Obligation**：canonical escape 的唯一化、trace origin/authenticity、typed transitive ref closure。
- **修正後可重驗條件**：新增 transition/resource derivation 或明示且可驗的 sandbox attestation；把兩個負例加入 regression suite，預期皆 `record_accepted=false`。
