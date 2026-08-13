# AI-1｜I0 v0.2.3 frozen candidate 獨立唯讀驗收

## Disposition

**PASS（scoped frozen candidate acceptance） / CLOSURE-CLASS-01 CLOSED**

- New promotion blocker：**none found in the reviewed scope**。
- v0.2.3 正確封閉 frozen v0.2.2 的 `CLOSURE-CLASS-01`：generic `EnvelopeShape` 先於 supported/unsupported `spec_id` 分流。
- 此 PASS 只採納列出的 Definition/interface candidate 與 Experiment artifacts；不是 validator soundness/completeness theorem，也不是任何 P/NP 結論。
- Candidate root 全程唯讀；不發布 Board success、不建立 shared repo、不修改 frozen v0.2.2/v0.2.3 bytes。

## 1. Frozen identity

Candidate root：

`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`

| Artifact | SHA-256 | Result |
|---|---|---|
| `SHA256SUMS-v0.2.3-candidate.txt` | `7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817` | exact |
| schema | `DCE6F0C95B95D9377BA7AF9F9537BDC277CDF0E68CE74B9AD3BF83DB2B011895` | exact |
| validator | `B0DC4EC989F93EBD557C4C8BFA3004E33B2BBAE0EB0F8FA5622489B2D148097B` | exact |
| projection spec | `35D21683177A849FD8AD331451A818BE1EE2E7605CF4B11F54FF5CCCFED69251` | exact |
| closure spec | `4E978EF2A2DF0FED51E94E89E6305294A9B7965AD86AB6888EE857DA4854643B` | exact |
| evidence role spec | `FB5C3BE06BA68716492B96664BF8FD5C6154C1159025E5F1D278FAD1C0B3CBFB` | exact |
| run fixture manifest | `189967B7F60968BE2ACED2A0B4EE5E8885FBBFD997916BA18F55B33F3A4AA5D1` | exact |
| closure fixture manifest | `46721DBE2E8A5E4CE1144DA2957C7688059637149DDDADFF766B517001C6DE06` | exact |
| closure reproducer | `90AAECDD4214AC188A35F1DBF4894819CFE727C0D9E63A1A39E0D574335806F2` | exact |
| frozen live report | `7D32357291B59DE472A266BAAD63F7BBB469B60F58BCD727DF5D3A35899125EB` | exact |

Manifest verification：121 parsed entries、121/121 hash match、0 missing、0 mismatch、0 duplicate path。

前代 identity 保持：

- v0.2.2 manifest `AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B`，98/98 exact。
- v0.2.2 schema `BDBB386CE7EAAB5377344BF29762CCBE45EA6371AC72742DE509467CB70BB556`。
- v0.2.2 validator `7DA459E8AD9FB3F8A49FAA312A612F05484588143F36FF0918D090D6B1965AE5`。
- v0.2.2 closure spec `11F6CB511ADFCF9528D11390E59CE1B52D8F709053FF5AA7295230F5B3E604EB`。
- v0.2.2 role spec `2FEFA7AACB9B6D914C3B78CDB2C187262D12A35BD56B14FD5882A71B84991A3F`。
- v0.2.1 manifest `4F5925CD2A449549F9629017E538F5FA341FA8BAECB4A5BB3F8B93ED005EBD6A`。

## 2. Read-only provenance

共享 root 同時保留多個版本，因此本次 provenance 只 snapshot v0.2.3 manifest 列出的 121 paths，不使用 whole-root delta。

驗收開始與結束時逐一比較 121 paths 的 relative path、length、UTC mtime ticks、SHA-256：

- before entries：121；
- after entries：121；
- changed/missing/added manifest paths：0；
- `candidate_root_writes_by_AI1=0`。

所有會產生 `__pycache__`、fixture、artifact或live report的命令均在隔離副本執行：

`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-integrator\work\v023-acceptance-488dba17352e4368a6fb5cdbf1542efd`

舊測試需要的 parent-level frozen v0.1 schema只放在隔離父目錄，SHA-256：

`3B50247DED1B21B4962A5ADD19DA2263AFB77358D8837D14B4B58EDA7883CAF4`

## 3. Executable reproduction

環境：CPython 3.14.5、jsonschema 4.26.0、cryptography 49.0.0、Windows 10.0.19045、single worker。

### 3.1 Tests

- frozen v0.2：14/14 PASS；
- frozen v0.2.1：11/11 PASS；
- frozen v0.2.2：15/15 PASS；
- v0.2.3：16/16 PASS；
- total：56/56 PASS。

舊版 suite 內的 2-SAT fixed-seed exhaustive cross-check再次完成：1–6 variables × 250 cases，共 1,500 cases，與 exhaustive oracle一致。

### 3.2 Closure-classification probes

`scripts/reproduce_closure_class_v023.py .`：exit 0、17 probes、`unexpected=[]`、`all_conformant=true`。

- 14 個 missing/empty/ill-typed/generic-edge malformed cases：全部 `FAIL`；
- 2 個 complete shape-valid unsupported cases：全部 `UNKNOWN`；
- 1 個 pinned supported run-spec control：`PASS`。

Exact frozen v0.2.2 minimal case另以臨時目錄直接對照：

```json
{"artifact_envelope":{"spec_id":"urn:unsupported:closure:9"}}
```

Observed：v0.2.2=`unknown`；v0.2.3=`fail`；v0.2.3 frozen spec expected=`fail`。

Shape-valid future artifact type維持 `UNKNOWN`，證明修正沒有把完整 unsupported envelope誤分類成 malformed。

### 3.3 Run fixtures and live experiment

- 33 run-record fixtures；0 manifest mismatch；
- 6 positive fixtures accepted；
- 新增 `malformed-unsupported-envelope` 與 `shape-valid-unsupported-envelope` 均 structural-valid、semantic-invalid、`admission=false`、`final=false`、`record_accepted=false`；
- live experiment exit 0；重新產生的 report除 machine-dependent `*_time_ns` 欄位外，遞迴正規化後與 frozen report完全一致。

### 3.4 Deterministic regeneration

使用既有 non-production fixture key在隔離副本執行 `generate_fixtures_v023.py`：exit 0。

- fixture outputs：34；
- artifact outputs：73；
- total regenerated outputs：107；
- 重產後 frozen manifest：121/121 exact、0 mismatch。

## 4. Exact code/interface review

### 4.1 Validator delta

相對 frozen v0.2.2，功能性差異集中於：

1. 版本、spec ids、signature context、measurement model與pinned artifact hashes更新為 v0.2.3；
2. 新增 `_envelope_shape`；
3. `_artifact_closure` 在 `spec_id` supported/unsupported dispatch之前呼叫 `_envelope_shape`；
4. supported spec才檢查 current version、known artifact type與parent-role-child relation。

`_envelope_shape` 實際要求：

- envelope為object；
- `spec_id`、`artifact_type`、`version` 為非空string；
- `edges` 為array；
- 每個edge精確包含 `role`、`expected_type`、`sha256`；
- role/type為非空string，同一parent內role唯一，SHA-256格式有效。

分類順序符合 frozen closure spec：Leaf → generic malformed/FAIL → shape-valid unsupported/UNKNOWN → supported semantic validation/traverse。

### 4.2 Transport schema

v0.2.2→v0.2.3 schema diff只更新 schema/gate/projection版本與description；GateAssignmentConformant、admission/final implications、standard/robust × neutral/bounded matrix與candidate/external-receipt分離均未改。

Draft 2020-12 metaschema check PASS；既有 gate applicability mutation suite PASS。

### 4.3 Admission/final/resource semantic isolation

v0.2.2 與 v0.2.3 共通 31 fixtures逐筆比較：

- structural/semantic/admission/final/record-accepted outcome vector differences：0；
- 18-gate vector differences：0；
- v0.2.3只新增兩個 closure-classification records，兩者皆拒絕。

四象限 positive observations維持：

- standard/bounded：account=`pass`、budget=`pass`；
- standard/neutral：account=`pass`、budget=`not-applicable`；
- robust/bounded：account=`pass`、budget=`pass`；
- robust/neutral：account=`pass`、budget=`not-applicable`。

PROV-DERIVE-01 的 states=999／transition digest cases仍拒絕；REF-TYPE-01 的三個 substitution cases仍拒絕。

### 4.4 Interface scope

- `validate_bytes(record_bytes, schema_bytes, artifact_root)` 仍從exact schema bytes導出digest、parse object與使用中的schema；wrong schema bytes得到 `schema-byte-pin-mismatch`。
- mapping＋claimed-hash 的 public `validate_record` 不存在；mapping helper保持private。
- `validate_path` snapshot record/schema bytes後委派 `validate_bytes`；`ArtifactIndex` 對artifact hash/parse/use使用單一in-memory snapshot。
- raw `-0`、Unicode scalar/NFC、trace/auth、projection與operational map規則未變。

Package scope仍需明示：`pyproject.toml`、`__version__` 與default CLI維持 v0.2.0；v0.2.3 candidate驗收只適用於明確的 `semantic_validator_v023`、`experiment_v023`、versioned schema/artifacts與 `requirements-v0.2.3-candidate.txt`。這與尚未promotion的狀態相容。

## 5. Acceptance matrix

| Dimension | Result |
|---|---|
| 121-entry v0.2.3 identity | PASS |
| predecessor frozen identity | PASS |
| manifest-path read-only provenance | PASS |
| four test suites / 56 tests | PASS |
| 17 closure probes | PASS |
| exact v0.2.2 minimal regression | PASS |
| 33 run fixtures | PASS |
| 107-output deterministic regeneration | PASS |
| live report normalized reproduction | PASS |
| admission/final/resource semantic isolation | PASS |
| schema/snapshot/versioned interface | PASS（scoped） |
| new blocker | **none found** |

## 6. Scope limits and governance boundary

- Validator仍是bounded executable interface，不是proof-assistant kernel或universal interpreter。
- Robust I0只代表pinned finite deterministic singleton run，不涵蓋一般scheduler/fault nondeterminism。
- Signed raw measurement只代表pinned test signer attestation，不代表production measurement authority。
- Closure probes與fixture matrix是有限 executable evidence，不是所有artifact graph的completeness theorem。
- PARITY／2-SAT結果不得外推general 3-SAT、`P=NP`或`P≠NP`。
- 本報告不自行promotion、不發布Board success、不建立shared repo；是否採納／發布仍由協作治理與其餘獨立驗收決定。
