# AI-1｜I0 v0.2.2 frozen candidate 二次唯讀驗收

## Disposition

**FAIL / CLOSURE-CLASS-01**

- 分類：frozen interface/spec 與 validator implementation 的一般 required-member 分類順序不一致。
- 影響：阻止 v0.2.2 promotion；v0.2.2 應維持 `CANDIDATE_UNPROMOTED`。
- 限縮：此案例最後仍得到 `unknown`，而 `unknown` 會阻止 admission；因此不是錯誤接受、不是 REF-TYPE-01 復發，也不導出任何 P/NP 結論。
- 處置：保留全部 98-entry frozen bytes；修正另起 v0.2.3，不覆寫 v0.2.2。

本報告是純本機、唯讀 software conformance review。不連網、不修改 candidate、不發布 Board success、不建立 shared repo，也不把工程結果外推為數學定理。

## 1. Frozen identity

Candidate root：

`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`

| Artifact | SHA-256 | Result |
|---|---|---|
| `SHA256SUMS-v0.2.2-candidate.txt` | `AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B` | exact |
| schema | `BDBB386CE7EAAB5377344BF29762CCBE45EA6371AC72742DE509467CB70BB556` | exact |
| validator | `7DA459E8AD9FB3F8A49FAA312A612F05484588143F36FF0918D090D6B1965AE5` | exact |
| projection spec | `7860AA7A741FAE5DCC6846B614C16450D29D17573563D6373A243931B9B51E57` | exact |
| closure spec | `11F6CB511ADFCF9528D11390E59CE1B52D8F709053FF5AA7295230F5B3E604EB` | exact |
| evidence role spec | `2FEFA7AACB9B6D914C3B78CDB2C187262D12A35BD56B14FD5882A71B84991A3F` | exact |
| fixture manifest | `501A4D067040217C3AC0595AA5D9BD726B8E43A9C821242F7C170D38236E4E56` | exact |
| frozen live report | `D7CE9B3A6610603681177CC943B86CE955AEE8693DD46BD0802EC1B75069814B` | exact |

Manifest verification：98 parsed entries、98/98 hash match、0 missing、0 mismatch、0 duplicate path。原 candidate root 在驗收前後皆為 241 files；`candidate_root_writes=0`。

前代 frozen identity 亦保持：

- v0.2 schema `1AD5AFA3A76E56AD5C9D0B79DF34B897E337606093D282693932085BF1AF297C`
- v0.2 validator `4C50BE9EF563644BC29F3DCEEFB9D9205056631847980FCC763D1E4BA25EB771`
- v0.2 projection `9966B86DBC3884E3327306FF1FEFAF21EFBDE705EE0F10739755BE27C73A1991`
- v0.2.1 schema `567417A82EA82C8C2CE7EC81DF1B4BEC5876044F54213446E4CE298CEADE6C2B`
- v0.2.1 validator `C777BC631303E977F025FC17AAB455CFEE3CDFA2B5C1A23166A51EC5E9E99CD4`
- v0.2.1 projection `70CAAE9973A3A02AD8F45364BE2175A51BA62C6C0D75B6C807B7B8DFB5BBD115`
- v0.2.1 closure `B466BF8D630BAC4B1A42A28F534C5D20A0713D418CCB3826ED69FF71D7585C94`
- v0.2.1 checksum manifest `4F5925CD2A449549F9629017E538F5FA341FA8BAECB4A5BB3F8B93ED005EBD6A`

## 2. Isolated reproduction baseline

環境：CPython 3.14.5、jsonschema 4.26.0、cryptography 49.0.0、Windows 10.0.19045、single worker。

所有會建立 `__pycache__`、live output 或重新生成 fixture 的命令均在以下隔離副本執行：

`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-integrator\work\v022-acceptance-c9afdfb00d1a42249e5a9a6a9e4b34d1`

Observed：

- frozen v0.2 tests：14/14 PASS。
- frozen v0.2.1 tests：11/11 PASS。
- v0.2.2 tests：15/15 PASS。
- fixture manifest：31 fixtures、0 mismatch。
- fixture generator：32 fixture files（含 manifest）＋19 traces＋19 auth receipts＋2 negative envelope artifacts，共 72 outputs；隔離重生後 frozen 98-entry manifest 仍 98/98 exact。
- REF-TYPE reproduction：三個 valid-signature substitution cases 全部 `record_accepted=false`，script exit 0、`all_expected=true`。
- 2-SAT：fixed seed `20260809`，1–6 variables × 250 cases，共 1,500 cases，與 exhaustive oracle 一致。
- live experiment：重新產生的 report 除 machine-dependent `*_time_ns` 欄位外，遞迴正規化後與 frozen live report完全相同；31 admission rows、6 accepted positive fixtures。

### 父路徑可攜性觀察

第一次把專案單獨搬到新的隔離父目錄時，舊 `tests/test_semantic_validator.py::test_v01_is_bitwise_preserved` 因固定讀取 `PROJECT_ROOT.parent / run-record.schema.json` 而得到 `FileNotFoundError`。把 SHA-256 為 `3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4` 的 frozen v0.1 schema 放到隔離父目錄後，14/14 PASS。

這是舊測試的 fixture-location portability observation，不是 v0.2.2 semantic failure。後續可把 v0.1 fixture path 顯式注入，或將該 frozen input 納入 self-contained test bundle。

## 3. Code/interface consistency review

### 3.1 Role map 與 typed closure

- `_actual_operational_reference_map` 收集 receipt、mechanism、event 與 certificate roles。
- `_expected_operational_reference_map` 依 family、mechanism、run mode 與 event count 產生 pinned expected map。
- signed trace 的 `operational_reference_map`、receipt map hash、direct role expected type 與 transitive role-bearing edges均受到比較。
- frozen 三個 REF-TYPE substitution fixtures均正確拒絕：
  - robust receipt run-spec 改成 standard：`operational-role-binding`。
  - robust refs 改成 public-key artifact：`direct-role-type`＋`operational-role-binding`。
  - contract/invariant cross-role 並重新簽署實際 map：role/type/map checks失敗。

結論：已知 REF-TYPE-01 regression cases 對 v0.2.2 為 PASS；這不等於一般 typed-closure 完備性定理。

### 3.2 Signature binding

- trace authenticity receipt 的 envelope、trace edge、public-key edge、signer id、algorithm、pinned key artifact與 Ed25519 signature 都由 exact snapshots 驗證。
- `bad-trace-signature` 為 structural-valid、semantic-invalid、`record_accepted=false`。
- signature只證明 test signer 對 trace bytes 的 attestation；不證明 production hardware measurement truth。此 scope limit 已由 candidate 明列。

### 3.3 Schema snapshot/interface

- supported API 是 `validate_bytes(record_bytes, schema_bytes, artifact_root)`；schema digest、parse object與使用中的 schema都從同一 `schema_bytes` snapshot 導出。
- 錯誤 schema bytes `{}` 得到 `schema-byte-pin-mismatch` 並 fail closed。
- mapping＋claimed-hash 的公開 `validate_record` 不存在；mapping helper 保持 private。
- `validate_path` 先各讀一次 record/schema bytes，再委派 `validate_bytes`。
- `ArtifactIndex` 對 artifact hash/parse/use 使用同一 in-memory snapshot。

介面範圍注意：`pyproject.toml`、`__version__` 與預設 CLI 仍為 v0.2.0，且 `__main__.py` 仍路由 v0.2 validator。這與 `CANDIDATE_UNPROMOTED` 相容；v0.2.2 驗收只適用於明確匯入的 `semantic_validator_v022` / `experiment_v022`，不可把預設 CLI 描述成 v0.2.2。

### 3.4 Schema gate assignment

- Draft 2020-12 metaschema check PASS。
- 13 個 universally-applicable gates排除 `not-applicable`；advice/proof、resource budget、maximality/fairness依條件矩陣決定 applicability。
- 既有 gate applicability mutations 全部 schema reject；`unknown` 與 `fail` 均阻止 admission。

### 3.5 Resource/context negative cases

以下 frozen conformance cases均按預期 `record_accepted=false`：

- event/resource derivation：`fabricated-states-999`、`fabricated-transition-digest`。
- family context：`fabricated-problem-size`、`fabricated-failure-frontier`、`declared-answer-access-mismatch`。
- raw/canonical domain：raw `-0` 得到 `record-parse`；unpaired surrogate得到 `canonical-unicode-scalar`。

此確認只涵蓋 frozen I0 families、pinned resource model 與列出的本機 cases；不是任意 family、任意 resource accounting 或任意 JSON implementation 的一般完備性證明。

## 4. Blocking conformance case：CLOSURE-CLASS-01

Frozen closure spec `artifacts-v0.2.2/artifact-closure-spec.v0.2.2.json` 定義的順序是：

1. 沒有 `artifact_envelope`：opaque leaf。
2. envelope 缺少或 mistype 任一 required member：Malformed / `FAIL`。
3. required shape/type 完整且 `spec_id` unsupported：`UNKNOWN`。
4. supported、well-typed envelope：Traverse。

Validator `src/pnp_glc_i0/semantic_validator_v022.py` 約第 604–614 行目前先取得並判斷 `spec_id`；只要它是非空 unsupported string，便在檢查 `artifact_type`、`version` 與 `edges` 之前回到 `UNKNOWN` 路徑。

獨立最小 conformance case：

```json
{"artifact_envelope":{"spec_id":"urn:unsupported:closure:9"}}
```

此 artifact 缺少 `artifact_type`、`version`、`edges`，依 frozen spec 應為 `FAIL`；實測：

```json
{
  "status": "unknown",
  "artifact_type": "unknown-envelope",
  "artifact_sha256": "297997b868b8d3c8946ccf9f6aa4da8de158563f71041849ad619684cc78a422"
}
```

因此 v0.2.2 對「missing required members ＋ unsupported spec id」的一般分類順序不符合自身 frozen interface。既有 `missing-envelope-spec-id` 測試只覆蓋缺 `spec_id` 的方向，未覆蓋此組合。

### v0.2.3 最低修正／再驗條件

1. 在判斷 supported/unsupported `spec_id` 之前，先一次完成 envelope required shape/type check：
   - `spec_id`：non-empty string；
   - `artifact_type`：non-empty string；
   - `version`：string；
   - `edges`：array。
2. 任一 required member missing/mistyped 一律 `FAIL`。
3. required shape/type 完整後，unsupported `spec_id` 才能 `UNKNOWN`。
4. supported spec 再檢查 validator version、known artifact type、edge exact shape、role uniqueness、parent-role-child relation與resolved child type。
5. 新增 table-driven cases：每個 required member各自 missing/mistyped，並分別搭配 supported與unsupported `spec_id`；保留一個 shape-valid unsupported case證明仍為 `UNKNOWN`。
6. 保留 v0.2.2 全部 40 tests、31 fixture matrix、72-output determinism、三個 REF-TYPE substitution regressions與前代 frozen hashes。

## 5. Final acceptance matrix

| Dimension | Result |
|---|---|
| 98-entry frozen identity | PASS |
| predecessor identity | PASS |
| isolated 14＋11＋15 tests | PASS |
| 31-fixture manifest | PASS |
| 72-output deterministic regeneration | PASS |
| 1,500-case 2-SAT crosscheck | PASS |
| known REF-TYPE substitution regressions | PASS |
| schema snapshot / signature / resource-context listed cases | PASS (scoped) |
| general envelope required-member ordering | **FAIL / CLOSURE-CLASS-01** |
| v0.2.2 promotion | **FAIL** |

## 6. Nonclaims and disposition boundary

- 本報告不是 validator soundness proof，也不是一般 closure completeness theorem。
- robust I0 仍只是 pinned singleton deterministic finite run；不涵蓋一般 scheduler/fault nondeterminism。
- signed raw measurements只代表 pinned test signer attestation，不代表 production measurement truth。
- PARITY、2-SAT、schema與replay experiments均不推出 `P=NP` 或 `P≠NP`。
- 不發布 Board success、不建立 shared repo。
- v0.2.2 保持 frozen counterexample snapshot；下一候選應命名 v0.2.3 並接受新的獨立唯讀驗收。
