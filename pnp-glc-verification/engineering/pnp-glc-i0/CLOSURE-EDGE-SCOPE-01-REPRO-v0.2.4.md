# CLOSURE-EDGE-SCOPE-01：v0.2.3 反例與 v0.2.4 回歸

分類：Counterexample to frozen v0.2.3 formal-interface uniqueness；不是 acceptance bypass、不是 executable regression、不是 P/NP 結果。

## Frozen v0.2.3 witness

`shape-valid-unsupported-future-type.json` 具有：

- unsupported `spec_id`；
- `artifact_type = future-artifact`；
- 非空 `future-edge`，`expected_type = opaque-content`；
- 目前 `EDGE_RELATIONS` 沒有 `future-artifact` parent mapping。

validator、source docstring、CURRENT 與 SCHEMA-DIFF 的 supported-only 讀法得到 `UNKNOWN`；但 frozen closure Definition 的 `edge_shape.expected_type` 無 scope 地要求符合 pinned relation，generic 讀法可得到 `FAIL/undefined`。兩者都阻止 admission，但 formal status 不唯一。

獨立驗收證據：

- AI-1 executable scoped PASS report：`C0B2E706A5CF3B0728A8BB83422323B88554127BDFF0BD7F84911A9C9CB2CC3E`
- AI-1 append-only correction：`3A1384611CBCDE6109288AE0C799A7E920395CD82AC52F65A3C4CBF68EDB69E7`
- AI-3 formal FAIL report：`79C4C8F0C54347217103BA58B035DA4D620B4BD0D5A7244DA8F9037BA2B135BC`

## v0.2.4 executable/interface regression

```powershell
$env:PYTHONUTF8='1'
python scripts/reproduce_closure_class_v024.py .
```

本地觀察：exit 0；20 classification probes + 7 scope checks；unexpected `[]`。

scope checks要求：normative precedence存在、generic relation明示不要求、supported header pins spec/version/type domain、supported relation iff header、unsupported relation N/A、unsupported result UNKNOWN、future parent確實不在 current relation domain。

reproducer SHA-256：`5F0FB64D1BB6DA17804088260FCA94A92F21DD4C2F5FAC1A9605F9F3BAD303DB`。

## 限定

此回歸只建立列出 judgment 與 executable interface 的一致性，不證明任意 artifact graph 的完整性；也不改變 robust singleton I0、一般 SAT 或 P/NP 的 epistemic 狀態。
