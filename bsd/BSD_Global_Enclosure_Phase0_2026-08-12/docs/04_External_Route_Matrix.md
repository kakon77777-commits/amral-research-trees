# 04｜外部研究路線矩陣

| 路線 | 最強自然輸出 | 累積性 | 共同瓶頸 | Phase 1 裁決 |
|---|---|---:|---|---|
| Gross–Zagier–Kolyvagin | rank $0/1$ 弱 BSD | 高 | 不跨高秩 | 基線 |
| p-adic zeta / Iwasawa | $p$-part、rank $0/1$ 強式 | 高 | local hypotheses、全 prime | 綠燈 |
| Strong-BSD twist families | 無限 family theorem | 很高 | applicability criteria | **首選** |
| p-converse | Selmer rank $\Rightarrow$ analytic rank | 高 | residual/local conditions | 綠燈 |
| generalized Kato / higher GZ | 高秩 bridge | 中高 | non-vanishing、uniformity | 黃燈 |
| exact computational BSD | 有限集合 full proof | 很高 | saturation、$\Sha$ exactness | 綠燈 |
| Selmer arithmetic statistics | rank/family distribution | 高 | 不保全稱例外 | 輔助 |
| numerical BSD atlas | evidence / anomaly detection | 高 | 不等於 proof | 僅作資料層 |
| 格點秩收斂 | 理論上想連 rank 與 zero order | 低 | 隱藏 equality、離散量不連續 | 紅燈 |
| Faithful certificate frontier | 全域研究控制 | 高 | 不提供 BSD theorem | 控制層 |

---

# 1. 首選：Twist-family reproduction

理由：

1. 2024 外部 theorem 已有；
2. 2026 已有算法化 paper；
3. LMFDB conductor $\le500{,}000$ 域完整；
4. 結果可逐條重播；
5. Agent 能把 hypotheses 編譯成 predicates；
6. 成功或失敗都能建立 applicability atlas。

---

# 2. 高秩線

不立即要求「證 rank $2$ BSD」。

先問：

- 哪個 higher Kato class 必須非零？
- 哪個 Selmer rank equality 已知？
- 哪個 $p$-converse 可用？
- rank $2$ 的 regulator、points、descent 哪些已 exact？
- $\Sha$ 的哪個 prime part仍未知？

輸出是一張 dependency DAG，而不是一篇假裝閉合的證明。

---

# 3. Representation Escape

對每個候選 BSD bottleneck，至少測試：

- complex $L$-function；
- $p$-adic $L$-function；
- Selmer group；
- Euler system；
- Heegner / Kato classes；
- descent；
- Iwasawa main conjecture；
- twist family；
- explicit computation。

若某個「困難」只在單一表示中存在，不能稱全域瓶頸。

---

# 4. MCDM 初評

$$
\mathfrak D_{\mathrm{BSD}/\mathbb Q}
\approx
(G5,U3,X2\text{--}X3,P4\text{--}P5).
$$

其中：

- $G5$：多條主方法回到高秩、$\Sha$、全 prime；
- $U3$：沒有完整全域閉合路徑；
- $X2$–$X3$：曲線例外可忠實列舉，但 theorem coverage仍常是 family/statistical；
- $P4$–$P5$：證書、資料與 theorem applicability高度可累積。

這是研究路由評估，不是數學定理。
