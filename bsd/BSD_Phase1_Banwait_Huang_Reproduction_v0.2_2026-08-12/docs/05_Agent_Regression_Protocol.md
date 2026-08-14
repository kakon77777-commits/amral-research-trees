# 05｜Agent Regression Protocol

每個 Agent 修改 theorem router前，必須跑三層測試：

- Layer A：current 12 positive fixture；
- Layer B：old-only 13 historical regression；
- Layer C：official discrepancy four。

輸出格式：

```json
{
  "curve": "...",
  "decision": "PASS | FAIL | UNKNOWN",
  "first_failure": "...",
  "all_failures": [],
  "evidence": [],
  "code_version": "...",
  "semantic_version": "..."
}
```

認知防火牆：

- `analytic Sha = 1` 不等於 `Sha is trivial`；
- `rank = 0` 不自動等於 rigorous analytic rank $0$；
- 2-descent dimension與 analytic valuation數值相同，不自動等於 BSD$(E,2)$ 已證；
- timeout 必須是 `UNKNOWN`。

若新版本只改善 runtime/cache/batching/output formatting，標 `ENGINEERING ONLY`，不計為 BSD 數學進展。
