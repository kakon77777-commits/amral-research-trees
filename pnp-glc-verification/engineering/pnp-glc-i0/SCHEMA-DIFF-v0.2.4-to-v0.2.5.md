# Schema／validator／closure-spec diff：v0.2.4 → v0.2.5

分類：Definition/interface candidate + Experiment；不是 theorem adoption。

## Transport schema

v0.2.5 從 frozen v0.2.4 transport schema 版本化。唯一語義欄位變更是移除 required free-text `mechanism.admissibility.advice`，改為 required enum `advice_mode`：

- `none`：schema要求 single uniform program、null advice generator、declared access none、advice/generated-table bytes為0、generation time/space/output為0、receipt observed access none。
- `per-input-length-truth-table`：schema要求 nonuniform per-length program量詞、非 null generator、declared/observed access truth-table，以及正的 advice/generation resource entries。

JSON Schema只封閉 record 已自相矛盾；跨欄相等、family/mechanism 語義與 trace observation仍由 external validator判定。

## External validator

`ExpectedAdviceDecl(family, mechanism)` 對三個 supported I0 context形成總映射：uniform streaming PARITY與2-SAT均為 `none`；PARITY table family為 `per-input-length-truth-table`。`_advice_declaration_matches` 同時核對 typed mode、uniformity、program quantifier、pinned generator ref、declared/observed access與 ledger fold；不符產生 `advice-declaration-ledger-binding` 並 fail closed。

既有 oracle family binding、transition execution、resource derivation、role-bearing closure、trace authenticity、GateVal applicability與 Admission/Final implications未改。

## Normative closure spec

v0.2.5 把完整 classification dependency graph收進 normative `judgments`：

- `OpaqueLeaf`：沒有 artifact envelope；不 traverse。
- `GenericEdgeShape`：通用 edge syntax。
- `GenericEnvelopeShape`：required members／nonempty strings／edge list；依賴 `judgments.GenericEdgeShape`；false時明定 Malformed/FAIL。
- `SupportedEnvelopeHeader` 與 `UnsupportedEnvelope`：都以 fully-qualified dependency指向 `judgments.GenericEnvelopeShape`。
- `SupportedEdgeRelation`：依賴 `judgments.SupportedEnvelopeHeader`。

`normative_precedence` 明定所有 symbolic dependencies必須解析於同一 judgments object；頂層 prose objects只作 derived views。

## 適用域與失敗前沿

修補只涵蓋目前 artifact-envelope 與 advice declaration interface。一般 3-SAT/CDCL、任意 nondeterministic scheduler/fault、production measurement authority、完整 validator proof與通用 oracle framework不在主張內。不得外推 P=NP 或 P≠NP。
