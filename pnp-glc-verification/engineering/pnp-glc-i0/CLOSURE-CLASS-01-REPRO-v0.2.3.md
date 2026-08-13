# CLOSURE-CLASS-01：v0.2.2 反例與 v0.2.3 回歸

分類：Counterexample to frozen v0.2.2 interface consistency；不是 acceptance bypass，也不是 P/NP 結果。

## Frozen v0.2.2 反例

最小 artifact：

```json
{"artifact_envelope":{"spec_id":"urn:unsupported:closure:9"}}
```

frozen closure spec 要求完整 required-member shape/type 先驗，因此預期 `FAIL`；v0.2.2 實作在只檢查 `spec_id` 後先分派 unsupported，實際回傳 `UNKNOWN`。`UNKNOWN` 仍阻止 admission，所以沒有 record 被錯誤接受；不一致在分類介面本身。

三份獨立唯讀驗收：

- AI-1 report：`22D5ED76A24A0EC2C0C6E9E90EE4AF6CD863BDA557E2E29E4CC3C7F9CB5F5929`
- AI-2 report：`8D19F9E870FF7C28F2E9111C9497CEAF028A4A6B7C5918F28866C8C0093E7982`
- AI-3 report：`8F3CCFEA9D98D30BE5BC7966042CD9AFB51F4E95B331293803D38448C0036B75`
- AI-3 minimal regression：`408E4E2BA4C6EF61252009288D4EAA1FB94DDB5E6D21C94151B1F63FB1B5317D`

## v0.2.3 executable regression

執行：

```powershell
$env:PYTHONUTF8='1'
python scripts/reproduce_closure_class_v023.py .
```

本地觀察：exit 0；17 probes；unexpected `[]`。

- 14 個 malformed/empty/missing/ill-typed cases → `FAIL`；
- 2 個完整 unsupported cases → `UNKNOWN`；
- 1 個 pinned supported run-spec control → `PASS`。

另有兩個 valid-signature end-to-end record fixtures：`malformed-unsupported-envelope` 與 `shape-valid-unsupported-envelope`。兩者皆 structural valid、external semantic invalid、`record_accepted=false`。

reproducer SHA-256：`90AAECDD4214AC188A35F1DBF4894819CFE727C0D9E63A1A39E0D574335806F2`。

## 限定

這組測試只證明列出的分類案例與目前 executable interface 一致。它不是對所有 artifact graph 的 completeness proof，也不改變 robust I0 的 singleton deterministic 範圍；不得據此推論一般 SAT 或 P/NP。
