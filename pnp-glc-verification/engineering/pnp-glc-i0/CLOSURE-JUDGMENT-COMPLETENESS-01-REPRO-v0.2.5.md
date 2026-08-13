# CLOSURE-JUDGMENT-COMPLETENESS-01：v0.2.4 反例與 v0.2.5 回歸

分類：Counterexample to frozen v0.2.4 Definition/interface completeness；不是 admission bypass、correctness failure或 P/NP 結果。

## Frozen v0.2.4 缺口

v0.2.4 closure spec 的 `normative_precedence` 指定 `judgments` 是 classification 的規範來源，但 `judgments` 沒有 `GenericEnvelopeShape`，而 `SupportedEnvelopeHeader` 與 `UnsupportedEnvelope` 都直接引用它。完整 required-member/type constraints只在 judgments外的 prose-like `base_envelope_shape`，也沒有 normative generic-fail→Malformed/FAIL或 OpaqueLeaf judgment。因此嚴格 judgments-only 讀法的依賴圖未閉合；code仍 fail closed，所以不是錯誤接受。

AI-1 formal acceptance report SHA-256：`FE7609E89D67A76D10E0D92CCC9362E534C261F98D0EB13BC25EA327961278F7`。AI-3 formal/interface report SHA-256：`EC42899B9CC5E375CF756A76EE34F970D7E52B2BEF755D8BFC9136B9BE39CE00`。

## v0.2.5 executable/interface regression

```powershell
$env:PYTHONUTF8='1'
python scripts/reproduce_closure_class_v025.py .
```

本地觀察：exit 0；20 classification probes + 17 scope/dependency checks；unexpected `[]`。dependency checks要求每個 judgment有 list-valued `depends_on`、每個 ref fully-qualified、每個 target解析成功，並核對 GenericEnvelope／OpaqueLeaf、Malformed/FAIL及 derived-view precedence。reproducer SHA-256：`87255148DE527CD6247DD28BE19DB882D63DB8C9441726103C0328D06D8C6194`。

這只證明 pinned v0.2.5 artifact 的 dependency graph與 executable classifier在本次有限介面上一致，不是任意 artifact graph 的完整性定理。
