# 16｜Phase 1 封頂與 Phase 2 接口

## Phase 1 已完成

已完成：

1. Theorem 2.18 predicate map；
2. Algorithm2 independent reproduction；
3. paper/current-code soundness audit；
4. `<150` version regression；
5. 13 removed curves first-failure closure；
6. 500K exact artifact census；
7. Algorithm1 4062 removal cause closure；
8. stable-domain OLD→CURRENT Algorithm2 semantic replay。

因此 Phase 1 可封頂：

$$
\boxed{
\text{Banwait–Huang Reproduction = COMPLETE}
}
$$

## 不值得再主攻

1,355 OLD-only curves的 historical twist reconstruction可做，但它們已不在 CURRENT Algorithm1 accepted universe。

除非目的轉為：
- repository history paper；
- proof-engineering case study；
- full historical reproducibility archive；

否則對 BSD 本身的邊際收益低。

## Phase 2 建議

### Route A — High-Rank Wall Atlas

從 rank $2+$ 曲線開始，逐 component建立：
- rigorous analytic rank；
- Mordell–Weil rank upper/lower；
- Selmer；
- $\Sha$ finiteness / p-parts；
- leading coefficient。

### Route B — Strong-BSD Coverage Expansion

問：
> 能否用 2024–2026 已知 theorem把 Banwait–Huang Algorithm1 的 eligible family再擴張，而不是只重現原算法？

這才開始可能產生新的外部數學結果。

### Route C — 2-primary unresolved frontier

目前 current code對 positive analytic $v_2(\Sha)$ 保守 reject。

可建立：
- higher 2-power descent可處理的曲線族；
- 哪些 reject只是 computation/certificate不足；
- 能否用現成 theorem / Magma/Sage exact descent擴大 certified set。

這是 Phase 1 最自然留下的新數學接口。
