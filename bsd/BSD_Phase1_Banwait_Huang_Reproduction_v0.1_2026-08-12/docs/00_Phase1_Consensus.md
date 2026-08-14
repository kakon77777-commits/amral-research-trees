# 00｜Phase 1 共識裁決

## 裁決

$$
\boxed{
\text{PASS：Banwait–Huang 路線可工程化。}
}
$$

它不是只說「存在無限多 twists」，而是把 theorem hypotheses 分成：

1. base curve $E$ 的資格；
2. twist parameter $d$ 的資格；
3. $\operatorname{BSD}(E,2)$ 的獨立驗證；
4. branch-specific Chebotarev / splitting conditions。

這非常適合：

```text
Theorem
→ Predicate
→ Evidence source
→ Certificate
→ Pass / Fail / Open
```

---

# 本輪達成的最小重現

我們沒有在缺少 SageMath / LMFDB backend 的環境裡假裝重跑 500K 曲線。

相反地，先重現 Algorithm 2 最可隔離的兩條分支。

## CLZ20 branch

$$
46a1:
\quad
E=[1,-1,0,-10,-12],
\qquad
N=46.
$$

在：

$$
1\le d\le1000
$$

得到：

$$
[1,185,265,305,745,785,905].
$$

## Zha16 branch

$$
106d1:
\quad
E=[1,1,0,-27,-67],
\qquad
N=106.
$$

在：

$$
-1000\le d\le1000
$$

得到：

$$
[1,17,89,97,113,241,281,409,473,505,521,545,577,649,673,713,785,857,865,929,937].
$$

兩者均與官方 repository fixture 完全一致。

---

# 為什麼這不是 BSD 證明？

純 Python mirror 只驗證：

> 在假設 base curve 已通過 Algorithm 1 的前提下，$d$ 是否滿足 Theorem 2.18 所列的顯式算術條件。

真正的 theorem strength 仍來自：

- Cai–Li–Zhai；
- Zhai；
- Banwait–Huang 的組合定理；
- $\operatorname{BSD}(E,2)$ 的 descent certificate；
- base curve 的 analytic rank、optimality、ramification與 isogeny資料。

所以輸出應讀作：

```text
admissible according to theorem criteria
```

而不是：

```text
BSD independently proved from elementary computation
```

---

# 下一階段

Phase 1 v0.2 應在本地 Sage / LMFDB 環境中做：

1. 官方 conductor $<150$ 全曲線重跑；
2. Algorithm 1 每一 filter 的中間數量；
3. 2-descent pass/fail certificate；
4. 官方 12 曲線與 twist JSON 完整 diff；
5. 再擴到 conductor $<500000$。
