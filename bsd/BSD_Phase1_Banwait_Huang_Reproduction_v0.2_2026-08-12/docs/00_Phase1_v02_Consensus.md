# 00｜Phase 1 v0.2 收斂裁決

## 本輪結論

$$
\boxed{
\text{Phase 1 小樣本已從「結果重現」升級為「版本化證書回歸」。}
}
$$

v0.1 已獨立重現 Algorithm 2 的兩個代表分支。

v0.2 新增：

1. 5 月 22 日舊 fixture 與 6 月 3 日現行 fixture 的完整差分；
2. 官方 discrepancy report 的獨立 adversarial corpus；
3. false-positive / unknown / timeout / testing-only 的受控失敗字典；
4. 500K 重跑的 soundness preflight；
5. 「版本回歸不等於數學拒絕原因」的資料分層；
6. 可執行 regression test。

舊 fixture 有 $25$ 條，現行 fixture有 $12$ 條；現行集合是舊集合的子集，沒有新增，正好移除 $13$ 條。

這說明 theorem-producing code不能只保存最終成功清單，而必須保存數學語義的版本歷史。

## 兩個 adversarial corpus

### Corpus A — Version Regression

只回答：

> 哪些曲線曾被舊版官方 pipeline 放行，但現行版不再放行？

它只證明 membership change，不能自動推斷每條的數學拒絕原因。

### Corpus B — Explicit Discrepancy

官方 `discrepancy_report.txt` 對四條曲線逐 predicate列出現行拒絕理由。

這才是 theorem-level adversarial corpus。

## 新 Gate

進 500K 前必須同時通過：

$$
\boxed{
\text{Current positive fixture}
+
\text{Historical regression}
+
\text{Explicit discrepancy corpus}.
}
$$
