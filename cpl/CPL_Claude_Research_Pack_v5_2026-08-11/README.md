# CPL / Claude PairCeiling Research Pack v5

**日期：** 2026-08-11

本包新增兩個關鍵進展。

## 1. 第一個 exact-rational small-N certificate

對 $N=4$ continuous-position toy marked-configuration class，建立 exact rational dual：

$$
L=0.6982110925
$$

因此嚴格得到：

$$
p_{min}\ge 69.82110925\%.
$$

$(2,2)$ 與 $(2,1,1)$ pattern 的 configuration-wise validity 使用 exact-rational Bernstein subdivision 驗證；$(1,1,1,1)$ 直接由 $S_j\ge0$ 驗證。

文件：

- `notes/07_N4_Exact_Rational_Bernstein_Certificate.md`
- `scripts/certify_N4_open_band_bernstein.py`
- `results/N4_exact_rational_certificate.json`

## 2. 第一個 $P_{70}$ minimal boundary-escape candidate

加入：

$$
\mathbb E[S(4)]\le B.
$$

continuous column-generation 顯示：

- $B=3.67$：candidate $69.9982\%$
- $B=3.65$：candidate $70.0596\%$

所以 numerical crossing 在 $B\approx3.6694$ 附近。

此外已 rationalize 一組 $B=3.65$ dual candidate，其 objective 仍為：

$$
70.0545516\%.
$$

但這組含 boundary price 的 certificate 尚未把 fully-simple 三自由度 pattern 做完 exact positivity certification，因此目前不能稱 theorem。

文件：

- `notes/08_N4_Minimal_Boundary_Escape_P70.md`
- `scripts/N4_boundary_P70_dual_candidate.py`
- `results/N4_boundary_escape_frontier_candidates.csv`
- `figures/N4_boundary_escape_near_70.png`

上一版完整包 `CPL_Claude_Research_Pack_v4_2026-08-11.zip` 已一併封存於本包。
