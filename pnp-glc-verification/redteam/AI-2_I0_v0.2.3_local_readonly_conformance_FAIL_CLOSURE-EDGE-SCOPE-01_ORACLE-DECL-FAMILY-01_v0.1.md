# AI-2 I0 v0.2.3 本機唯讀 conformance 驗收

## Disposition

**FAIL / CLOSURE-EDGE-SCOPE-01 + ORACLE-DECL-FAMILY-01**

- `CLOSURE-CLASS-01` 的 executable 修補：**CLOSED / PASS**。
- `CLOSURE-EDGE-SCOPE-01`：frozen Definition/interface 的 edge-relation scope 不唯一；promotion blocker。
- `ORACLE-DECL-FAMILY-01`：外部 validator 接受與 family/result 不一致的 oracle `name/checks` 宣告；independent accepted-record provenance/declaration blocker。
- v0.2.3 保持 `CANDIDATE_UNPROMOTED`；未修改 candidate root，不授權 Board success 或 shared repo，也不作任何 P/NP 外推。

兩個 blocker 均不表示錯誤答案通過：第一項的 `FAIL` 與 `UNKNOWN` 都阻止 admission；第二項仍由 validator 按 `problem.family` 執行正確的獨立 oracle。問題分別是規範判定不唯一，以及 accepted record 的宣告／provenance 不真。

## Scope 與方法

- 僅做本機、唯讀的 record-validator conformance review；未連網。
- frozen root：`pnp-glc-i0` v0.2.3 exact bytes。
- 先一次讀取並核對 v0.2.3 manifest 的 121 個 paths，再於 temporary directory 建立版本限定的 runtime snapshot；所有欄位替換、有效測試簽章與重產均只發生於 temporary snapshot。
- v0.2.3 manifest 是版本增量而非 standalone runtime closure，故隔離副本包含未變的 predecessor/core runtime context；並行的 v0.2.4 paths 明確排除。
- 寫入監測域嚴格限定為 121 個 v0.2.3 manifest paths，另監測 manifest 本身；以 length、mtime_ns、SHA-256 前後比對。
- 使用的 Ed25519 key 是既有 non-production fixture key；有效簽章只證明 test signer attestation，不代表 production measurement authority。

## Frozen identity

| Artifact | SHA-256 / result |
|---|---|
| v0.2.3 manifest | `7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817` |
| v0.2.3 entries | 121/121 exact；0 missing、0 mismatch |
| schema | `DCE6F0C95B95D9377BA7AF9F9537BDC277CDF0E68CE74B9AD3BF83DB2B011895` |
| validator | `B0DC4EC989F93EBD557C4C8BFA3004E33B2BBAE0EB0F8FA5622489B2D148097B` |
| closure spec | `4E978EF2A2DF0FED51E94E89E6305294A9B7965AD86AB6888EE857DA4854643B` |
| role spec | `FB5C3BE06BA68716492B96664BF8FD5C6154C1159025E5F1D278FAD1C0B3CBFB` |
| fixture manifest | `189967B7F60968BE2ACED2A0B4EE5E8885FBBFD997916BA18F55B33F3A4AA5D1` |
| closure fixture manifest | `46721DBE2E8A5E4CE1144DA2957C7688059637149DDDADFF766B517001C6DE06` |
| bundled reproducer | `90AAECDD4214AC188A35F1DBF4894819CFE727C0D9E63A1A39E0D574335806F2` |
| frozen live report | `7D32357291B59DE472A266BAAD63F7BBB469B60F58BCD727DF5D3A35899125EB` |
| v0.2.2 predecessor manifest | `AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B`；98/98 exact |
| candidate writes in monitored domain | 0 |

## Blocker 1：CLOSURE-EDGE-SCOPE-01

### 被檢查的命題

Frozen v0.2.3 Definition/interface 對「完整 generic edge、但 unsupported `spec_id`」能唯一決定 `FAIL` 或 `UNKNOWN`。

### 最小 witness

Frozen positive fixture `shape-valid-unsupported-future-type`：

```json
{
  "artifact_envelope": {
    "artifact_type": "future-artifact",
    "edges": [
      {
        "expected_type": "opaque-content",
        "role": "future-edge",
        "sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
      }
    ],
    "spec_id": "urn:unsupported:closure:9",
    "version": "9.0.0"
  }
}
```

觀察：

- `_envelope_shape(...)` 通過，generic shape=true。
- `EDGE_RELATIONS.get("future-artifact")` 為 `None`。
- validator 與 fixture expected status 都是 `UNKNOWN`。
- source docstring、`CURRENT-v0.2.3-candidate.md`、`SCHEMA-DIFF-v0.2.2-to-v0.2.3.md` 均明確採 supported-only relation checking。
- 但 frozen `artifact-closure-spec.v0.2.3.json` 的 `edge_shape.expected_type` 無條件寫成 `must equal the pinned parent-type/role relation`，沒有 `scope` 或 precedence 欄位；該 artifact 自標 `Definition-interface-candidate`。

因此有兩個合理形式化：

1. `edge_shape.expected_type` 屬 generic `EnvelopeShape`：parent relation 未定義／不相等，得 `FAIL`（或 judgment undefined）。
2. relation checking 僅在 supported dispatch 後適用：得 `UNKNOWN`，與 executable 一致。

兩者都 admission-blocking，故不是 erroneous acceptance；但 frozen normative status 不唯一，阻止 interface promotion。

### 可修正性

後繼版應以 normative fields 明確拆分：

- `GenericEdgeShape`：適用所有 envelope，只規定 keys、非空字串、hash syntax、同 parent role 唯一。
- `SupportedEdgeRelation`：`scope = supported spec_id only`，才要求 `EDGE_RELATIONS[parent][role] == expected_type`。
- 明示 classification precedence。

## Blocker 2：ORACLE-DECL-FAMILY-01

### 被檢查的命題

Accepted run record 的 oracle declaration 已綁定 exact problem family、mechanism 與 result obligation。

最低前提不是自行加出的：

- schema 把 oracle `name`、`checks`、`version`、`independent`、`sha256` 全列為 required，沒有 nonnormative／annotation 標記。
- candidate projection 與有效 trace signature 覆蓋完整 oracle object；這提供完整性，但不自行提供宣告真實性。
- frozen live report 的 `candidate_scope.family_bound_contract_oracle_rule_invariant` 為 `true`。
- predecessor `CURRENT-v0.2.2-candidate.md` 明列 contract/oracle/rule/invariant 綁定 exact problem family 與 mechanism；v0.2.3 聲明該語義未改。

### 最小可重現族

以合法 PARITY 或 2-SAT fixture 為基底，只變更 oracle declaration 的 `name`／`checks`；共同 `sha256` 不變，因兩族使用同一 pinned `oracles.py` source hash：

`sha256:c8c5f6a0c132b11c56fd7964b737c1eb4f0b6a8674c7de8adcda50ca4b54efce`

每個 case 都同步 candidate projection、trace 與 operational map，以既有 fixture key 產生有效 Ed25519 trace/auth，再重算 closure：

| Variant | Actual |
|---|---|
| PARITY，只把 `name` 換成 2-SAT oracle name | schema valid、signature PASS、closure PASS、accepted=true、issues=[] |
| PARITY，只把 `checks` 換成 `["assignment"]` | 同上 |
| PARITY，同時換 `name` 與 `checks` | 同上 |
| 2-SAT SAT record 宣告 UNSAT `checks=["mutual implication paths"]` | 同上 |
| 2-SAT UNSAT record 宣告 SAT `checks=["assignment"]` | 同上 |

成因：

- actual/expected operational map 對 oracle 只比較共用 source hash。
- `_operational_reference_status` 只核 version、independent、hash；不核 name/checks。
- `_independent_oracle_status` 正確地按 `problem.family` 與 actual result 執行 oracle，但忽略 name/checks。
- `_family_context_issues` 也不核 oracle declaration。

因此它不是 correctness、oracle-execution、signature 或 closure bypass；答案仍由正確 oracle 重算。反例是 `SemanticValidate` 將假的義務／provenance 宣告判為 `semantic_ok=true` 並接受。即使 `name` 日後改定義為 display annotation，`checks` 仍明確表達驗證義務，故 blocker 不消失。

### 可修正性

- 由外部 validator 導出 `ExpectedOracleDecl(family, mechanism, result_status)`。
- 精確核對 typed `oracle_id`、entrypoint 與 obligation set；2-SAT SAT/UNSAT 的 obligations 亦須分開。
- 若 `name` 非規範，應明示移入 annotation，不應再把它當作 executed oracle identity。
- 加入 PARITY↔2-SAT、2-SAT SAT↔UNSAT、name-only、checks-only 的 valid-signature negative fixtures。
- JSON Schema conditional 可提供早期拒絕，但不能取代 external semantic derivation。

## Scoped positive evidence retained

| Probe | Result |
|---|---|
| 四代 unit suites | 14/14 + 11/11 + 15/15 + 16/16 PASS |
| bundled closure reproducer | exit 0；17/17 conformant；unexpected=[] |
| v0.2.3 fixture manifest | 33 records；0 mismatch |
| independent generic envelope matrix | 57 cases；53 expected FAIL、4 expected UNKNOWN；0 mismatch |
| exact v0.2.2 minimal witness | v0.2.3 actual `FAIL`；`CLOSURE-CLASS-01` executable fix closed |
| supported edge relations | supported control PASS；wrong relation、missing child、child type mismatch、duplicate role 均 FAIL |
| valid-signature refs/maps | 7 schema-valid cases全部 rejected：run、sandbox、contract、invariant、rule、map omission、extra role |
| trace/signature pairing | valid-signature trace/auth transplant 與三個 built-in negative fixtures全部 rejected |
| schema/raw domain | wrong schema bytes、raw `-0`、duplicate key、unpaired surrogate fail closed；canonical newline spellings一致 |
| derived mirrors | size、frontier、answer-access、states、transition digest 五類均 rejected，所需 issue code 存在 |
| resource mirrors | record/trace mismatch rejected；matching signed raw measurement accepted，僅證明 signer attestation |
| gate applicability | 8 profiles × 18 gates = 144 mutations；schema acceptance=0 |
| isolated regeneration | schema byte-identical；34 fixtures + 73 artifacts = 107 outputs byte-identical |
| provenance | 15/15 probe groups得到預期觀察；unexpected=[]；frozen monitored writes=0 |

以上是 bounded I0 evidence，不是 validator soundness/completeness theorem。Robust 仍只覆蓋 pinned finite deterministic singleton；共享 oracle source hash 不等於 declaration family binding；test signer 不等於 production authority。

## Reproducer

- `v023_conformance_revalidation.py`
- SHA-256：`0082644010D2302846E7A5949E2EFF9DB7F7A367B220DA2DFD9AE98882FFB09F`
- Final run：exit 0；`probe_groups=15`；`unexpected_results=[]`；`candidate_root_writes=0`；overall disposition 如本報告。

## Final classification

- `CLOSURE-CLASS-01`：closed executable regression。
- `CLOSURE-EDGE-SCOPE-01`：Definition ambiguity / unconditional promotion blocker for frozen v0.2.3 interface。
- `ORACLE-DECL-FAMILY-01`：accepted-record semantic provenance/declaration Counterexample / unconditional promotion blocker。
- 其餘本報告的成功 probes：bounded Observations / Experiments，不升格為一般定理。
