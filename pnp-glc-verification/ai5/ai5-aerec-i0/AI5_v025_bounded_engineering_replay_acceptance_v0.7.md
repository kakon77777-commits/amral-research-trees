# AI-5｜v0.2.5 bounded engineering replay acceptance

日期：Asia/Taipei 2026-08-09  
候選狀態：`READ-ONLY / CANDIDATE_UNPROMOTED`  
驗收範圍：manifest identity、最小 advice 工程路徑、external derivation chain、acceptance packet portability 與 frozen live-report scope。  
非範圍：Board、shared repo、successor、完整 96-test suite、1500-case 重跑、P/NP 推論。

## Disposition

`FAIL / ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01 + FROZEN-LIVE-REPORT-SCOPE-01`

v0.2.5 的 typed advice 與既有 admission gates 在完整 live root 的定向重播符合預期；FAIL 僅針對本輪 bounded engineering acceptance packet。166-path frozen manifest 不是可執行、可解析證據閉合，且 frozen live report bytes 不包含 packet 所稱的 1500-case suite。

## 1. Exact identity 與零寫入

- frozen root：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- `SHA256SUMS-v0.2.5-candidate.txt`：166 entries，SHA-256 `9D759DB19360E9716E372B7791C251626F658E5C4A185A297EEF6EA01DE9531E`。
- 逐項驗證：166/166；malformed line 0、duplicate 0、outside-root 0、missing 0、reparse point 0、hash mismatch 0。
- manifest bytes 合計：1,188,108。
- 隔離快照恰含 166 files、1,188,108 bytes、extra files 0；未把 manifest 外路徑補入快照。
- candidate root 驗收前後均為 710 files、44 directories；觀察到的 `candidate_root_writes=0`。

前後指紋完全相同：

| 指紋 | SHA-256 |
|---|---|
| 全根內容（relative path + file SHA-256） | `B529740F5B9F7FEE121280F7D49396E00218F11C255329783BAF6152171D9C29` |
| 全根檔案 metadata | `A7B632DEDB05C5ACF11F4B97A6B6A1DAD399DF51F67AD7BFC27100C8EF2C0FAC` |
| 全根目錄 metadata | `0002D9F6DE32729F3EBBABA9796289AFBE689F0FC3242497AC0441FC020BBCC1` |

root `LastWriteTimeUtc` 前後同為 `2026-08-09T10:17:17.8610657Z`。所有 Python 重播均使用 `-B`／`PYTHONDONTWRITEBYTECODE=1`。

## 2. 最小工程路徑

完整 live root 上執行官方定向 CLI：

```powershell
python -B scripts/reproduce_advice_decl_ledger_v025.py .
```

結果：exit 0、`all_conformant=true`、4 negative probes、3 none-advice positive controls、1 coherent table-binding control、`unexpected=[]`。

| 路徑 | 結果 |
|---|---|
| 合法 PARITY `parity-stream`／`advice_mode=none` | structural PASS、semantic PASS、derived admission true、accepted |
| 合法 2-SAT `2sat-kosaraju`／`advice_mode=none` | structural PASS、semantic PASS、derived admission true、accepted |
| table mode + null generator + none access + zero ledger | schema FAIL、not accepted |
| none mode + table generator/access/positive ledger | schema FAIL、not accepted |
| stream mechanism + coherent table declaration | schema-valid；external `advice-declaration-ledger-binding` FAIL；not accepted |
| table mechanism + coherent none declaration | schema-valid；external `advice-declaration-ledger-binding` FAIL；not accepted |
| coherent table family binding (`cheat`) | direct advice match true、structural/semantic PASS；但 uniformity=FAIL、advice budget=FAIL，derived admission false、not accepted |

這些結果只證明 pinned I0 fixture/interface 的 bounded declaration consistency，不是 correctness bypass 或 P/NP 結果。

## 3. External validator 實際派生鏈

程式路徑不是只接受 candidate 自報：

1. `ExpectedAdviceDecl(family, mechanism)` 從 `(PARITY, parity-stream)`、`(2-SAT, 2sat-kosaraju)`、`(PARITY, parity-table-family)` 建立總映射。
2. `_advice_declaration_matches` 比對 typed mode、uniformity、program quantifier、pinned generator、declared/signed-observed access 與 advice-generation ledger fold。
3. `_expected_operational_reference_map` 從 family/mechanism/run mode 建立角色映射；再與 record 欄位、signed trace map、receipt map hash及 content-addressed artifact types比對。
4. validator 由輸入參數重算 transition、resource folds、applicable gates、Admission 與 Final postconditions。

另做 receipt-only 反向試驗：在合法 PARITY record 上只把 receipt 自報的 `builder_execution_pass` 改為 FAIL，並把 admission/final 改為 false；candidate projection 不變、signed trace projection 仍相等、trace authenticity 仍 PASS、schema 仍有效。validator 仍派生 builder=PASS、admission=true，並產生：

- `derived-gate-mismatch`
- `admission-postcondition-mismatch`
- `completion-postcondition-mismatch`

因此 live-root 的 external derivation chain 有實際執行證據，不是單純回讀 candidate 自報欄位。

## 4. Acceptance packet hash/count 核對

packet 的 11 個具名 pins 全部匹配 manifest bytes：schema、validator、projection spec、closure spec、role spec、fixture manifest、closure-classification manifest、closure reproducer、advice reproducer、retained-oracle reproducer、frozen live report。

- schema：`8A799A869CF6CDD17D1191A9D859AB25899FF9E651B454725814E4B458B92596`
- validator：`2571B418612414948A80967B868B910B3714D1FB63F3C79387BF77EC5CA71C5A`
- closure spec：`DFC5A11CF6296F4D83B054B7F4F903E509B0982F9C61D231D423E7F78B5FF71D`
- frozen live report：`1552B708D88D96365AF168D4A318DA2737EF4B06D5B700CEAA126BA27C6154F1`
- path counts：47 fixture + 102 artifact + 17 packet/code/doc = 166。

Hashes/counts 本身 PASS；command portability 不 PASS。

## 5. Blocker：ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01

在只含 166 manifest paths 的快照執行同一官方 CLI，exit 1：

```text
ImportError: cannot import name 'oracles' from 'pnp_glc_i0' (unknown location)
```

v0.2.5 manifest 的 `src/` 只含：

- `src/pnp_glc_i0/semantic_validator_v025.py`
- `src/pnp_glc_i0/experiment_v025.py`

但 validator 直接匯入、且把 bytes 當 operational evidence pin 的三個檔案都不在 manifest：

| 缺少路徑 | live-root SHA-256／validator pin |
|---|---|
| `src/pnp_glc_i0/oracles.py` | `C8C5F6A0C132B11C56FD7964B737C1EB4F0B6A8674C7DE8ADCDA50CA4B54EFCE` |
| `src/pnp_glc_i0/parity.py` | `BDFB4CD28A8730AA99B058DD6567027B98F0125FBF503A42E0FB895C686AEDEF` |
| `src/pnp_glc_i0/two_sat.py` | `ED1028C0263DC5A69864FB42D02ADA9756B40EE51149D9DD376DD206622A8971` |

`src/pnp_glc_i0/__init__.py` 亦未封裝；`experiment_v025.py` 依賴未封裝的 `experiment_v021.py`；`generate_fixtures_v025.py` 依賴未封裝的 `generate_fixtures_v021.py`。報告列出的舊 tests 目錄也不在本 manifest。

所以完整 live root 的 PASS 依賴 manifest 外 bytes；即使從外部環境注入 Python modules，manifest-bounded `ArtifactIndex` 仍無法解析上述 rule/oracle content hashes。這是 runtime 加 evidence closure 的 packet blocker，不是 advice 邏輯失敗。

## 6. Blocker：FROZEN-LIVE-REPORT-SCOPE-01

`CURRENT-v0.2.5-candidate.md` 與 `VALIDATION-REPORT-v0.2.5-candidate.md` 把「1500 fixed-seed 2-SAT exhaustive cases PASS」描述為 frozen live report 所保留的 scope；實際 frozen JSON：

- `two_sat.cases` 僅 2 筆：一個 SAT、一个 UNSAT 代表案例。
- 每筆只有 `exhaustive_crosscheck_pass=true`。
- 整份 live report 不含 literal `1500`、case-count 或 6×250 suite ledger。

1500-case loop 實際位於 full root 的 `tests/test_two_sat.py`（6 個 variable counts × 250），但該檔不在 v0.2.5 manifest，本輪也依指示沒有重跑。故不能把 1500-case 宣告歸因於 frozen live-report bytes；最多只能說 full-root 舊測試資料另有此宣告。

## 7. Bounded decision

- typed advice／declaration-ledger fix：live-root targeted replay PASS。
- coherent table binding 仍被既有 gates 阻擋：PASS。
- external independent derivation：targeted dynamic evidence PASS。
- exact manifest hashes/counts：PASS。
- manifest-bounded executable/evidence closure：FAIL。
- frozen live-report scope attribution：FAIL。
- candidate root writes：0。

因此 AI-5 在本輪 bounded engineering scope 回報 FAIL；不 promotion、不建立 successor、不發布 Board、不改 shared repo，也不提出任何 P/NP inference。完成此單一報告後返回待機。
