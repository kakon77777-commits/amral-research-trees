# AI-1｜I0 v0.2.3 驗收分類更正（append-only addendum）

## Corrected integrated disposition

**FAIL / CLOSURE-EDGE-SCOPE-01**

本 addendum 不覆寫先前報告：

`AI-1_I0_v0.2.3_獨立唯讀驗收_PASS_v0.1.md`

原報告 SHA-256：

`C0B2E706A5CF3B0728A8BB83422323B88554127BDFF0BD7F84911A9C9CB2CC3E`

原報告的 `PASS` 現限縮為 executable/code conformance reviewed scope；其中的 identity、tests、fixtures、regeneration、minimal regression、admission/final/resource isolation與read-only provenance證據全部保留。整體 formal-interface promotion disposition由本 addendum更正為 `FAIL / CLOSURE-EDGE-SCOPE-01`。

此更正不是 executable regression、不是record錯誤接受，也不影響 `CLOSURE-CLASS-01` 已由程式封閉的事實。`FAIL` 與 `UNKNOWN` 都阻止admission；blocker在frozen interface對edge-relation規則的scope不唯一。

## 1. Frozen witness

Closure spec：

`artifacts-v0.2.3/artifact-closure-spec.v0.2.3.json`

SHA-256：

`4E978EF2A2DF0FED51E94E89E6305294A9B7965AD86AB6888EE857DA4854643B`

Positive unsupported fixture：

`artifacts-v0.2.3/closure-classification/shape-valid-unsupported-future-type.json`

SHA-256：

`5B315F430543309C0BEC9CD48E011520074A065EED2B923F170491B6DA275342`

核心內容：

```json
{
  "artifact_envelope": {
    "spec_id": "urn:unsupported:closure:9",
    "artifact_type": "future-artifact",
    "version": "9.0.0",
    "edges": [
      {
        "role": "future-edge",
        "expected_type": "opaque-content",
        "sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
      }
    ]
  }
}
```

Observed executable facts：

- `EDGE_RELATIONS.get("future-artifact") = None`；
- validator `_envelope_shape` 只檢查generic syntax；
- unsupported `spec_id` 在generic shape通過後得到 `UNKNOWN`；
- frozen fixture與reproducer也把此case預期為 `UNKNOWN`。

## 2. Ambiguous frozen rule

Frozen closure spec的 `edge_shape.expected_type` 寫道：

`must equal the pinned parent-type/role relation`

該句本身沒有scope欄位，也沒有寫明只在supported `spec_id` dispatch之後適用。另一方面：

- `base_envelope_shape`、source docstring、`CURRENT-v0.2.3-candidate.md` 與 `SCHEMA-DIFF-v0.2.2-to-v0.2.3.md` 將pre-dispatch規則描述為generic edge syntax；
- source只對supported spec執行parent-role-child relation；
- candidate明示unsupported `artifact_type` 只需nonempty，不需是目前known type。

因此至少存在兩個合理形式化：

1. **Generic-relation reading**：`edge_shape.expected_type` 對所有EnvelopeShape適用。`future-artifact/future-edge` 沒有pinned relation，因此case應為 `FAIL`。
2. **Supported-only reading**：generic階段只驗keys/nonempty/hash/unique role；pinned relation只在supported spec內適用，因此case為 `UNKNOWN`。

兩種形式化都符合frozen package中的部分文字，卻產生不同status。雖然兩者都admission-blocking，但Definition/interface candidate無法給出唯一判斷，故阻止formal-interface promotion。

## 3. Preserved scoped positives

以下AI-1獨立證據保持有效：

- v0.2.3 manifest `7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817`，121/121 exact；
- manifest-path before/after changes=0，`candidate_root_writes_by_AI1=0`；
- tests `14/14 + 11/11 + 15/15 + 16/16`；
- executable closure probes 17/17 conformant to their stated expected statuses；
- exact v0.2.2 minimalcase在v0.2.3由`UNKNOWN`改為`FAIL`；
- 33 run fixtures 0 mismatch；
- 107 outputs隔離重產byte-identical；
- live report除machine timing外一致；
- v0.2.2/v0.2.3共通31 fixtures outcome/gate vectors無差異；
- REF-TYPE與PROV-DERIVE既有cases仍拒絕；
- schema snapshot、admission/final/resource四象限與versioned explicit interface在reviewed scope內一致。

上述只證明executable/code與列出cases的一致性，不能消除frozen normative scope ambiguity。

## 4. v0.2.4 minimum correction

後繼版本應在normative closure spec中明確拆分：

### `generic_edge_shape`

- scope：所有帶`artifact_envelope`的artifact，在supported/unsupported dispatch之前；
- exact keys：`role`、`expected_type`、`sha256`；
- role/expected_type為nonempty strings；
- hash格式有效；
- one parent內role唯一；
- 不要求目前已知parent relation。

### `supported_edge_relation`

- scope：**iff** `spec_id == ARTIFACT_CLOSURE_SPEC_ID`；
- parent `artifact_type` 必須是known supported type；
- `EDGE_RELATIONS[parent][role] == expected_type`；
- resolved child type依既有規則驗證並traverse。

並應明列normative precedence：

1. no envelope → Leaf；
2. generic envelope/edge malformed → `FAIL`；
3. generic-valid unsupported spec → `UNKNOWN`，不套用supported relation；
4. supported spec → supported type/version/relation/traversal checks。

Regression需同時保留future-artifact＋nonempty generic edge=`UNKNOWN`與supported wrong relation=`FAIL`，以及v0.2.3全部既有identity/tests/fixtures/regeneration evidence。

## 5. Governance boundary

- v0.2.3全部121 frozen entries保持不動。
- v0.2.3維持`CANDIDATE_UNPROMOTED`。
- 修正另起v0.2.4，不覆寫v0.2.3。
- 不發布Board success、不建立shared repo、不作P/NP外推。
