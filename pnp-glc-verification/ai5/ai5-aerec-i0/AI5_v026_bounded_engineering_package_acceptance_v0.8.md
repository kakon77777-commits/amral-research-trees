# AI-5｜v0.2.6 bounded engineering/package acceptance

日期：Asia/Taipei 2026-08-10  
候選狀態：`READ-ONLY / CANDIDATE_UNPROMOTED`  
Frozen root：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`  
非範圍：Board、shared repo、successor、歷史完整測試、一般 SAT、P/NP 推論。

## Disposition

`FAIL / ACCEPTANCE-PACKET-IMPORT-EDGE-COUNT-01`

三個既定 blocker 在本輪 assigned bounded scope 均重播通過：

- `CLOSURE-SUPPORTED-RELATION-RESULT-01`：CLOSED/PASS。
- `ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01`：CLOSED/PASS。
- `FROZEN-LIVE-REPORT-SCOPE-01`：CLOSED/PASS。

整體仍為 FAIL，唯一原因是 frozen acceptance packet 的 import-edge count 自相矛盾：`CURRENT-v0.2.6-candidate.md` 宣告 29，machine descriptor、官方 self-check、validation report及獨立 AST 固定點均為 31。本輪任務明確要求核對 packet counts/hashes，故不能把該差異忽略為非驗收 prose。

## 1. Frozen identity、快照與零寫入

- manifest：`SHA256SUMS-v0.2.6-candidate.txt`
- entries：216
- manifest SHA-256：`2E1C58A5CE85833DAC708DF21BD4FC4AC845FFC3182AAB16BF568F50AC502357`
- 逐項驗證：216/216
- malformed、duplicate、outside-root、missing、reparse、hash mismatch：全部 0
- manifest paths bytes 合計：1,487,312

委派核心 pins 全部匹配實際 bytes：

| Artifact | SHA-256 |
|---|---|
| schema | `EB22CB899869B2A43DCD2DBBD3F4C9F7C0A8921AE361EF2207DB1039B1C875EE` |
| validator | `3F87207F26A21CA1B750B70170EBE28090F97C0670FB6F0CA88ED04296244D72` |
| closure spec | `B635E86CB5FBDB89865ED4343F052247E98A245DD2194726066AEF01489F758F` |
| runtime descriptor | `B3019C2C62B2689CF897F787BEAADCEA19663C820DAFBED97B6AE6FC46CF8217` |

新快照只複製 manifest paths：216 files、14 directories、1,487,312 bytes、extra 0、missing 0、`.pyc/__pycache__` 0。命令與獨立 replay 前後：

- snapshot content digest：`8F095F9D72BE5CCF8B7F3B1F685FF2C8086D9CB5B6AE59D4419B88424F370F90`，不變。
- snapshot file-metadata digest：`BD9DF71F841ABF3F3754C228003D12A27486505311DEDED03CA9224B8EE92742`，不變。
- snapshot file count與root LastWriteTime均不變。

Candidate root 前後同為 887 files／50 directories：

| 指紋 | SHA-256 |
|---|---|
| content | `205AA6E00910D992B61FEF123206784ECB20A9BC2241CBF3907E79EEE832F648` |
| file metadata | `2D035A9D39DE8968BC4F18B6F8EC8CA5E1ED89DF55FDF12732E67B65BBECFE5E` |
| directory metadata | `11BB8FD9BDB6B9F5B0A40639A15C125D8F52E264A0FBF43CBE3A7D41015C3574` |

root LastWriteTimeUtc 前後同為 `2026-08-10T02:59:56.9733935Z`；本驗收觀察 `candidate_root_writes=0`。

## 2. Sanitized isolated execution

六條命令只在 216-path snapshot 中執行。執行前清除 21 個 Python influence variables；descriptor 指定的 `PYTHONHOME`、`PYTHONPATH`、`PYTHONSTARTUP`、`PYTHONUSERBASE` 均確認不存在。環境值沒有 original candidate root。

`python -I -B` preflight：

- `isolated=1`
- `dont_write_bytecode=true`
- `no_user_site=1`
- `sitecustomize_loaded=false`
- `usercustomize_loaded=false`
- `sys.path` 只有 Python installation／system site-packages；沒有 candidate original root、snapshot src或外部研究路徑
- external distributions：`cryptography=49.0.0`、`jsonschema=4.26.0`

## 3. 六條 descriptor commands

| Command | Exit | Disposition-decisive output |
|---|---:|---|
| runtime-closure-self-check | 0 | 209 required、20 sources、31 edges、6 commands；`all_conformant=true` |
| closure-reproducer | 0 | 20 classifications + 17 scope/dependency + 11 terminal-totality；`unexpected=[]` |
| advice-reproducer | 0 | 4 negatives、3 legal controls、table-binding control全符合 |
| oracle-reproducer | 0 | 9 negatives、3 controls全符合 |
| live-report-scope-reproducer | 0 | exact frozen object；1500 replay；7/7 checks |
| minimal-cli-legit | 0 | structural/semantic/admission/final PASS；record accepted |

六條命令全 exit 0；執行後 snapshot沒有新增、刪除或改變任何 file。

## 4. Runtime descriptor 獨立核對

獨立 checker沒有呼叫候選 `verify_runtime_closure_v026.py`，而是直接解析 manifest、Python AST及實際 JSON envelope bytes。

### Required paths

- descriptor required paths：209，unique。
- 209/209 均在216-entry top-level manifest。
- 209/209 均存在於snapshot且實際 SHA-256 等於manifest。
- 由 Python fixed-point、build inputs、content evidence、全部 v0.2.6 artifacts/fixtures、schema/live report/requirements重新做 union，結果恰等於同一209-path set。
- manifest多出的7 paths都是 packet docs／runtime isolation report，沒有 required omission。
- frozen isolation report的 manifest path-set digest獨立重算為 `2BC452701854A3FB46818B9969D49AB24CADBAB165CABAF706D94D554157C94D`，一致。

### Python source/import fixed point

- 14 entrypoints。
- 獨立 AST resolver得到20 source paths。
- 固定點得到31 unique local import edges。
- source set及edge set逐項等於descriptor。
- 20/20 sources均在required set、manifest及snapshot，bytes全部受pin。

### Direct/fixed-point evidence closure

獨立從run-record欄位導出direct hashes，再直接沿actual `artifact_envelope.edges`做fixed-point；沒有呼叫validator的direct-map或closure helper。

- direct-reference observations：661（跨fixture可重複）。
- unique fixed-point references：113。
- resolved hashes：112。
- unresolved hashes：1，恰為故意負例 `ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff`。
- descriptor的112個evidence paths一對一映射到112個resolved hashes，無缺少或重複代表。
- reference-set digest：`7F1C1B2D1BFE27BD286E30EA016B3B1C8A1FC55E7249E3B92DED8FF3FBCFB8C0`。
- oracle、PARITY transition、2-SAT transition、schema、closure spec的actual bytes均等於validator literal pins。

因此 `ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01` 在本輪 bounded package scope為PASS。

## 5. Frozen 1500-case evidence獨立重播

Frozen report：`i0-run-report.v0.2.6-candidate.json`  
SHA-256：`0812D561EE31C8F1C7B6B73DD6D73DACF70CF1E981600B551655597642B363DB`

獨立 replay沒有呼叫candidate experiment helper或其 exhaustive oracle：只載入manifest-pinned `two_sat.py` solver；case生成、最多64 assignments的brute-force oracle、SAT assignment checker及UNSAT雙向implication-path checker均由AI-5獨立實作。

- JSON pointer：`/two_sat/deterministic_crosscheck`，精確解析到frozen object。
- generation command逐字符合 frozen scope。
- seed：20260809。
- strata：variable counts 1至6，每層250 cases。
- total：1500。
- mismatch：0。
- certificate failure：0。
- frozen object與replay object逐欄完全相等。
- evidence digest：`2F472DB6486459BC6502AA0ABDF1B79FD361D274F41DFE461E14C197F414EBEF`。

| Variables | Cases | SAT | UNSAT | Mismatch | Certificate failures |
|---:|---:|---:|---:|---:|---:|
| 1 | 250 | 227 | 23 | 0 | 0 |
| 2 | 250 | 219 | 31 | 0 | 0 |
| 3 | 250 | 214 | 36 | 0 | 0 |
| 4 | 250 | 198 | 52 | 0 | 0 |
| 5 | 250 | 194 | 56 | 0 | 0 |
| 6 | 250 | 171 | 79 | 0 | 0 |

因此 `FROZEN-LIVE-REPORT-SCOPE-01` 在本輪 bounded evidence scope為PASS。

## 6. Blocker：ACCEPTANCE-PACKET-IMPORT-EDGE-COUNT-01

Frozen `CURRENT-v0.2.6-candidate.md`（SHA-256 `18AC00879641CADD97981B195A2F1A39D88C6CCE4ECF161E706BBD6C207E8C26`）宣告：

> 20 個 Python source paths 與 29 條 local import edges

但同一216-entry frozen packet內：

- machine descriptor：31 edges。
- descriptor官方 self-check：31 derived edges。
- `VALIDATION-REPORT-v0.2.6-candidate.md`：31 import edges。
- AI-5獨立 AST fixed-point：31 edges，且逐項等於descriptor。

所以29不是另一種合法計數口徑，也不是未凍結草稿；它是manifest-pinned CURRENT與其machine evidence之間的count inconsistency。Executable runtime closure仍PASS，但acceptance packet counts不具雙向一致性。

## 7. Bounded decision

- exact identity／216-path snapshot：PASS。
- six isolated descriptor commands：PASS。
- 209 required paths：PASS。
- 20 Python sources／31 import edges：PASS。
- 112 resolved + 1 intentional unresolved evidence closure：PASS。
- frozen 1500-case replay、pointer與digest：PASS。
- closure supported relation result：PASS。
- packet count consistency：FAIL（CURRENT 29 vs authoritative/derived 31）。
- candidate root writes：0。

因此AI-5回報單一 bounded FAIL，不promotion、不建立successor、不發布Board、不修改shared repo，也不提出P/NP inference。完成此報告後返回待機。
