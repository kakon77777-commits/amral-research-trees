# CPL / Claude PairCeiling Research Pack v7

本版把 $N=4$ toy $P_{70}$ 的 exact boundary threshold 從：

$$
3.667777612662112\ldots
$$

推到：

$$
\boxed{
3.669404433950979\ldots
}.
$$

使用的 exact rational safety margin只有：

$$
8.00777312\times10^{-8}.
$$

三種 multiplicity patterns 仍以 exact-rational Bernstein 證正。

這已非常接近上一輪 numerical crossing：

$$
3.66941.
$$

## 新增

- `notes/10_Refined_Exact_B70_Certificate.md`
- `results/N4_refined_exact_B70_certificate.json`

上一版完整研究包 `CPL_Claude_Research_Pack_v6_2026-08-11.zip` 已一併封存。

下一階段不再追 boundary scalar 的更多小數位，而轉向 continuous support-strip escape，開始逼近 Claude 真實的 $\sigma_{70}\approx1.04$ 問題。
