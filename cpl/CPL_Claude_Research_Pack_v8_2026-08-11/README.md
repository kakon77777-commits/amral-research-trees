# CPL / Claude PairCeiling Research Pack v8

**日期：** 2026-08-11

本版正式從 toy boundary scalar 進入 continuum Support Escape。

## 核心突破

我們重建了 Claude Remark 1.1 的：

$$
70\%\to1.04,\qquad
80\%\to1.26,\qquad
90\%\to1.70
$$

背後的數值機制。

對 generalized one-delta problem，令：

$$
A_\sigma
=
I-T_\sigma,
$$

$$
(T_\sigma f)(t)
=
\int_{-\sigma/2}^{\sigma/2}
(1-|t-u|)_+ f(u)\,du.
$$

則：

$$
q(\sigma)
=
1-
\frac1{
\langle1,A_\sigma^{-1}1\rangle
}.
$$

數值 root solving 得：

- $70\%$: $\sigma\approx1.04263$
- $80\%$: $\sigma\approx1.25785$
- $90\%$: $\sigma\approx1.70146$

精準重現 Claude 的 rough values。

我們並首次沿同一路線數值延伸：

- $95\%$: $\sigma\approx2.26079$
- $99\%$: $\sigma\approx4.19$

其中 $99\%$ 不是 Claude 論文明列結果，而是本研究的 numerical extension。

## 新增

- `notes/11_Reconstructing_Claude_Support_Ladder.md`
- `scripts/one_delta_support_ladder.py`
- `results/one_delta_support_thresholds.csv`
- `results/support_99_convergence.csv`
- `results/one_delta_support_curve.csv`
- `figures/one_delta_support_ladder.png`
- `SOURCES.md`
- `papers/` 內附 Claude 主論文（若本地來源存在）

上一版完整 v7 已封存在本包。
