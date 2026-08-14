# CPL / Claude PairCeiling Research Pack v11

**日期：** 2026-08-11

本版做了兩個核心推進。

## 1. Claude $O_1$ 的 exact kernel

將 Proposition 5.6 的 ordered double sum精確合併為 unordered prime pairs，得到：

$$
O_1
=
\frac1{\pi^2}
\sum_{m<n}
\frac{\Lambda(m)\Lambda(n)}{
\sqrt{mn}\log(n/m)
}
\left[
(G_m+G_n)(\sin2u-\sin u)
+
(H_m-H_n)(\cos2u+\cos u)
\right].
$$

near diagonal 的 leading universal kernel：

$$
\kappa(u)
=
\frac{\sin2u-\sin u}{u}.
$$

這顯示 WPPH 是一個 signed oscillatory weighted prime-pair problem，而不是普通 positive short-interval average。

## 2. 無條件路線審計

現有 unconditional Selberg-integral / short-interval結果同時有：

- range mismatch；
- statistic mismatch；
- constant/sign mismatch。

目前尚不能由它們直接推出 $q>67.25\%$。

但出現另一條混合線：

## Matrix Majorant–Inertia Problem（MMIP）

結合：

- BGSTB 的 unconditional $F(\alpha)\ge0$；
- CGdL 的 outside-band negative Fourier tail / SDP majorant；
- Claude 的 off-axis $(1,1)$ signature blocks。

目標是在不計算 $\alpha>1$ asymptotic 的情況下，利用 tail sign 改善 $67.25\%$。

## 新增

- `notes/14_Exact_O1_Kernel_and_Unconditional_Barrier.md`
- `notes/15_Matrix_Majorant_Inertia_Hybrid_Route.md`
- `scripts/o1_near_diagonal_kernel.py`
- `results/o1_symmetrisation_check.json`
- `results/near_diagonal_kernel_samples.csv`
- `results/unconditional_range_audit.csv`
- `results/unconditional_route_audit.csv`
- `results/majorant_inertia_constant_targets.csv`
- `figures/near_diagonal_universal_kernel.png`
- `figures/p70_short_interval_range_gap.png`
- `SOURCES.md`

上一版完整 v10 已封存在本包。

## 下一步

優先做 MMIP 的 finite toy SDP：

$$
\text{tail-sign observable}
+
\text{off-axis block inertia}
$$

是否能在 $N=4$ toy world中嚴格提高 scalar PairCeiling floor。

同時，direct arithmetic route可繼續研究 Kernel-Matched Selberg Problem（KMSP）。
