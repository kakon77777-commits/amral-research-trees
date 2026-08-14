# CPL / Claude PairCeiling Research Pack v4

本包延續 v3，新增：

- `notes/06_Column_Generation_and_Primal_Dual_Certificate.md`
- `scripts/continuous_column_generation.py`
- `results/continuous_column_generation_summary.csv`
- `results/dual_certificate_samples.csv`
- `results/representative_active_columns_N4.csv`
- `figures/column_generation_candidate_trend.png`
- `figures/dual_certificate_rescaled_samples.png`

## v4 核心

本輪證明了結構上的離散/連續對應：

$$
\text{toy LP dual}
\longrightarrow
\text{PairCeiling certificate}.
$$

令：

$$
r_N(j/N)=Ny_j,
$$

則 LP dual constraint：

$$
y_0+\sum_j y_jS(j)\le p
$$

直接等價於：

$$
c_0+\sum_j \frac{S(j)}{N}r_N(j/N)\le p.
$$

而 dual objective 趨向：

$$
c_0+\int_0^1r(x)x\,dx.
$$

Continuous-position column generation 的數值候選 floors：

$$
N=4:\ 69.8231\%,
$$

$$
N=5:\ 69.2205\%,
$$

$$
N=6:\ 68.8935\%,
$$

$$
N=7:\ 68.7144\%.
$$

官方 Anthropic $N=256$ exact-rational law：

$$
68.1828687\ldots\%.
$$

目前數值 pricing 尚未形成 rigorous global certificate，因此這些是 candidate floors，不是新定理。

## 下一步

1. interval branch-and-bound pricing；
2. trigonometric polynomial / SOS / SDP pricing relaxation；
3. minimal escape information $I^*_{70}$；
4. support / higher-moment / zeta-specific realizability 三線比較。

`CPL_Claude_Research_Pack_v3_2026-08-11.zip` 已一起放在本包根目錄，保留前一階段完整資料。
