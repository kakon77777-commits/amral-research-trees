# Schema/interface diff: v0.2.5 → v0.2.6

## Transport schema

`run-record.schema.v0.2.6-candidate.json` 只做版本化搬移，保留 v0.2.5 的 typed `advice_mode` 與雙向 record-internal conditionals。Schema 仍只驗 transport shape；evidence truth、family/mechanism binding、resource derivation與 admission/final postconditions由 external validator判定。

## Normative closure interface

- `GenericEnvelopeShape.true_result` 明列 supported/unsupported exact dispatch。
- `SupportedEnvelopeHeader` 具有 structured false terminal與 true next transition。
- `SupportedEdgeRelation` 具有 total false/true outcomes：false=`Malformed/FAIL/do-not-traverse`；true=`Traverse/PASS → judgments.SupportedTraversal`。
- `SupportedTraversal` 明列 child dispatch與 fixed-point terminal trichotomy：any FAIL→FAIL；無 FAIL 且有 UNKNOWN→UNKNOWN；queue empty且全 PASS→PASS。
- 所有 transition refs fully qualified 並解析至同一 judgments object。頂層 prose 仍是 derived-only，不能補寫 normative 結果。

## Runtime/evidence interface

`acceptance-runtime-closure.v0.2.6.json` 是 machine-readable closure：官方命令、entrypoints、AST-derived source closure、import edges、external distributions、operational evidence files、parent build inputs與 forbidden environment dependencies 均明列。Top-level manifest 必須涵蓋其全部 required paths。

## Frozen experiment scope

`experiment_v026.py` 不再匯入 legacy experiment。其 1500-case 2-SAT crosscheck完全由 v0.2.6 source、seed與 frozen report bytes定義；不引用未入 manifest 的舊 test 檔作證據。
