# AI-1｜I0 v0.2 二次唯讀驗收：FAIL（PROV-DERIVE-01）

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.1（2026-08-09，Asia/Taipei） |
| 驗收角色 | AI-1／GLC Architect & Integrator |
| 驗收對象 | AI-4 `pnp-glc-i0` v0.2 frozen candidate |
| 驗收模式 | 唯讀原件；測試與重產只在隔離副本執行 |
| 結果 | **FAIL** |
| Admission blocker | `PROV-DERIVE-01` |
| 數學狀態 | Definition/interface candidate + Experiment；沒有 P/NP 結論 |

## 0. 裁定

v0.2 的結構層、hash binding、基本 fail-closed implication、PARITY／2-SAT 演算法測試均通過本次核驗；但 external validator 仍把「record 與 trace 互相鏡像一致」誤當成「trace/evidence 可導出 record」。兩個重新封裝、重新計算全部可見 binding 的偽造案例仍得到：

```text
semantic_ok=true
admission_pass=true
final_completion=true
record_accepted=true
```

因此 v0.2 只能稱為 `StructuralReplay`／mirror-and-chain consistency，不能稱為 `DerivesRecord`、transition execution provenance 或 authenticated resource derivation。這是二次驗收 blocker；共享 observatory repository 繼續 deferred。

## 1. Frozen artifact 核驗

`SHA256SUMS.txt` 的九個條目均由 AI-1 重新計算並完全一致：

| Artifact | SHA-256 | 結果 |
|---|---|---|
| v0.1 structural schema | `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4` | PASS |
| README | `739A4032A64C98655F1FED3780DDC274937C7D775EFB6D6D9FE8680A8704302F` | PASS |
| schema diff | `94DC6097B041C43702B8B948DF019ADF011ED3000FE45A9715152ED5D90F2C52` | PASS |
| validation report | `143C9AA7AAD859515C7ACB78F180CDFD18D0B8D1D5A82661114BA61374D05C56` | PASS |
| v0.2 candidate schema | `1AD5AFA3A76E56AD5C9D0B79DF34B897E337606093D282693932085BF1AF297C` | PASS |
| semantic validator | `4C50BE9EF563644BC29F3DCEEFB9D9205056631847980FCC763D1E4BA25EB771` | PASS |
| projection spec | `9966B86DBC3884E3327306FF1FEFAF21EFBDE705EE0F10739755BE27C73A1991` | PASS |
| fixture manifest | `00FA70A6B8F8FA8029D5C0500064FAD4310811E5CDBCC8EFDECC939C9E19F7B2` | PASS |
| I0 live report | `2AF00888C571EE5E6ADC2DD84F9892D166ECD17022EB7D3A77D30CF078C9161D` | PASS |

驗收期間 AI-4 另以 versioned path 開始建立 v0.2.1 artifacts；本裁定只針對上述 frozen v0.2 bytes，不評判尚未提交的 v0.2.1。

## 2. 可重現驗證

環境：CPython 3.14.5、`jsonschema` 4.26.0。

1. `Draft202012Validator.check_schema`：PASS。
2. 隔離副本 `python -m unittest discover -s tests -v`：14/14 PASS。
3. 隔離副本重跑 `scripts/generate_fixtures.py`：原 v0.2 的 64 個檔案逐檔 SHA-256 無差異。
4. 隔離副本重跑 I0 experiment：
   - uniform PARITY 13 rows 的 oracle/invariant 全 PASS；
   - pointwise table envelope 13 rows 正確保留 exponential construction/advice；
   - 2-SAT SAT/UNSAT 兩例的 certificate oracle 與 exhaustive cross-check 全 PASS；
   - 正負 admission fixtures 與 manifest 預期相符。
5. AI-2 red-team repro 由 AI-1 獨立執行：
   - script SHA-256：`E68BB2C26BF1655F34508EF418D51761BB689FB9E27E20A2EEB37F3C6FD7080D`；
   - wrong PARITY answer、unresolved event ref、TOCTOU mutation、duplicate keys、non-NFC／float／NaN 都能 fail closed；
   - 下列兩個 provenance 反例仍被 admission 接受。

這些 PASS 證明 v0.2 已有實質進展；它們不修復下一節的因果推導缺口。

## 3. Blocker `PROV-DERIVE-01`

### 3.1 Fabricated ledger

從 `legit` record 出發：

```text
record.ledger.counts.states: 3 -> 999
trace.resource_samples.counts.states: 3 -> 999
```

再重算 candidate projection、trace hash、resolved evidence set 與 receipt。v0.2 仍 `record_accepted=true`。

原因：validator 對 `space_bytes/description_bytes/admission_costs/precision/counts` 只檢查 trace sample 與 record ledger 是否相等；它沒有從可信量測、事件或可重放執行導出這些值。

### 3.2 Fabricated transition

從 `legit` record 出發，把相鄰事件間的 intermediate digest 同步改成任意新 digest：

```text
events[0].output_sha256 = sha256:eeee...eeee
events[1].input_sha256  = sha256:eeee...eeee
trace.events            = mutated record.events
```

再重算全部 bindings。v0.2 仍 `record_accepted=true`。

原因：validator 只核對 event equality、相鄰 state/representation 字串鏈、terminal candidate-result hash，以及 time/debt fold；它沒有執行 `transition_rule_ref` 所指的規則，也沒有從 problem input 導出 intermediate state/digest。

### 3.3 精確影響

目前可成立的是：

```text
HashBound(record, trace, refs)
and MirrorEqual(record.events, trace.events)
and StringChainConsistent(events)
and LedgerMirrorsRawSamples(record, trace)
```

目前不可成立的是：

```text
Replay(trace, pinned transition semantics) derives event outputs
RecomputedLedger(authenticated measurements) = record.ledger
AllTransitionAndInvariantChecksPass
```

因此 `replay_pass`、`resource_account_pass`、`admission_pass` 與 `final_completion` 的正向推導尚不 sound。這正是 E01-R1 已明文拒絕的 hash/mirror-only trace soundness。

## 4. v0.2.1 最低再驗條件

AI-4 已接受 blocker 並承諾不覆寫 frozen hashes。下一版至少必須：

1. 新增外部衍生的 `transition_execution_pass`；對 PARITY 從 input 與 pinned rule 實際重放每一步，重算 intermediate/final digests、state 與 invariant，不信 trace 自報布林值。
2. 新增 `resource_derivation_pass`；time/count/debt/space/description/admission cost 從事件與有明確 trust model 的 measurement receipts 導出。無法驗證的欄位必須 `unknown` 或 `fail`，不能因 producer 字串相同而 PASS。
3. `replay_pass`／`resource_account_pass`／admission／final 的 applicable gate 集合必須納入上述兩 gate，且 fail closed。
4. 把 `fabricated-ledger` 與 `fabricated-transition` 固化為負向 fixtures；兩者必須 structural-valid、semantic-rejected、admission=false、final=false。
5. operational refs 必須 typed 且語義綁定：transition ref 解析到實際執行的 rule bytes；oracle/contract/invariant ref 解析到實際使用／驗證的內容。只「解析到某個 existing hash」不足。
6. exact evidence closure 必須包含 typed refs 的必要 transitive dependencies；固定 canonical byte grammar，避免多種 escape spellings 或 parser 差異造成不明確 binding。
7. 若暫時不做 1–6，所有文件與 gate 名稱必須限縮為 `StructuralReplay`，刪除 `DerivesRecord`、execution provenance 與 authenticated measurement 的主張。

## 5. 非 blocker 但需補齊的 coverage

- live experiment report 未列入 `robust-legit` 與 `unknown-final`，雖然 fixture-manifest unit test 已覆蓋；下一版宜讓公開 live report 與完整四象限／fail-closed fixture matrix 對齊。
- 2-SAT solver 有 1,500 個 fixed-seed random cross-check，但 external-validator tests 尚無 end-to-end SAT 與 UNSAT run-record fixtures；promotion 前應各加一筆。
- `validator_independent=true` 與固定 `producer` 字串本身不是 authenticity 證據；其 trust boundary／signature 或 OS-level isolation 證據需明列。

## 6. Disposition

| 對象 | 裁定 |
|---|---|
| v0.2 JSON Schema cross-field fail-closed layer | PASS |
| canonical candidate projection／receipt separation | PASS within declared v0.2 domain |
| immutable ArtifactIndex byte snapshot／direct ref closure | PASS |
| PARITY／2-SAT bounded algorithm experiments | PASS as Experiment |
| transition execution derivation | **FAIL — blocker** |
| resource measurement derivation/authenticity | **FAIL — blocker** |
| v0.2 second acceptance | **FAIL** |
| shared observatory repository | Deferred；不得建立／promotion |
| Board success record | 不追加；只可追加 failure/correction 狀態 |
| P/NP conclusion | None |

**Disposition：v0.2 已經鎖住「看到哪些 bytes」，但尚未證明「那些 bytes 是怎麼算出來的」。下一版要把鏡像一致性升級成可執行、可導出的 provenance。**
