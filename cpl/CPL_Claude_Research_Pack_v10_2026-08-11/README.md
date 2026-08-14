# CPL / Claude PairCeiling Research Pack v10

**日期：** 2026-08-11

本版把「$P_{70}$ 需要 Hardy–Littlewood」進一步縮小成 **test-specific weighted hypothesis**。

## 核心新概念

### WSPC$(\sigma)$

只要求 optimized one-delta test 的一個未知-strip weighted moment：

$$
\int_{1<|\alpha|\le\sigma}
\widehat R_\sigma^\star(\alpha)
(F(\alpha,T)-1)\,d\alpha
=o(1).
$$

而不是完整：

$$
F(\alpha,T)=1+o(1)
$$

uniformly on the whole interval。

### WPPH$(\sigma,\Phi)$

直接在 Claude Proposition 5.6 的 exact $O_1$ prime sum上要求：

$$
O_1-O_1^{HL-model}=o(TL^3).
$$

這是一個 test-specific weighted prime-pair assumption，比逐-shift strong Hardy–Littlewood 更貼近 proof 真正使用的資訊。

## 一個很意外的數值

對 $P_{70}$ optimizer：

$$
\sigma\approx1.04263,
$$

但 $\widehat R^\star$ 真正位於 $|\alpha|>1$ 的 Fourier mass只有約：

$$
0.114\%.
$$

因此第一道牆的難點是「跨出 support 1」，而不是需要大量未知頻帶。

若稍微取：

$$
\sigma=1.05,
$$

model certificate約為：

$$
70.44\%,
$$

所以可以容許約：

$$
0.44\%
$$

的 test-specific weighted pair error，仍維持 $70\%$。

## 新增

- `notes/13_Test_Specific_Weighted_Pair_Hypothesis.md`
- `scripts/weighted_pair_optimizer_diagnostics.py`
- `results/optimized_test_unknown_strip_mass.csv`
- `results/P70_weighted_moment_tolerance.csv`
- `figures/unknown_strip_mass_vs_target.png`
- `SOURCES.md`

上一版 v9 已封存在本包。

## 下一步

1. 從 Claude $O_1$ 抽出 rescaled leading kernel $K(m/X,hT/X)$。
2. 用該 kernel 對接已知 average prime-pair / Selberg-integral / short-interval variance results。
3. 先搜尋能否**無條件**推過 $67.25\%$ 或甚至 $68.185\%$，再談完整條件式 $70\%$。
