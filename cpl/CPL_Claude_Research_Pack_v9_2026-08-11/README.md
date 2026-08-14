# CPL / Claude PairCeiling Research Pack v9

**日期：** 2026-08-11

本版從 `Support Escape` 進到真正的 `Arithmetic Realizability`。

## 核心結論

Claude prime-side目前：

$$
O_1\ll L^2X,
\qquad
D\asymp TL^3.
$$

若：

$$
X=T^\sigma,
$$

則現有 absolute bound 的 normalized size：

$$
\frac{|O_1|}{D}
\ll
\frac{T^{\sigma-1}}{\log T}.
$$

所以 $\sigma=1$ 是 diagonal-only regime 的結構邊界。

對 $n,m\sim X$，近對角 additive shift：

$$
h\sim \frac XT
=
T^{\sigma-1}
=
X^{1-1/\sigma}.
$$

### CPL arithmetic scales

- $P_{70}$: $\sigma\approx1.04263$, $h\sim T^{0.04263}$
- $P_{80}$: $\sigma\approx1.25785$, $h\sim T^{0.25785}$
- $P_{90}$: $\sigma\approx1.70146$, $h\sim T^{0.70146}$
- $P_{95}$: $\sigma\approx2.26079$
- $P_{99}$: $\sigma\approx4.18722$

Goldston 的 strong Hardy–Littlewood pair hypothesis（平方根級誤差）經典上足以供應 SPC 到 $\alpha<2$，因此 $P_{70},P_{80},P_{90}$ 落在同一 conjectural arithmetic regime；$P_{95},P_{99}$ 則已跨過它。

## 新增

- `notes/12_Arithmetic_Realizability_Bridge.md`
- `results/arithmetic_realizability_targets.csv`
- `scripts/arithmetic_support_scales.py`
- `SOURCES.md`

上一版 v8 已封存在本包。

## 下一步

優先研究 `Route A`：

> 從 Claude Proposition 5.6 的實際 $O_1$，抽出只足以完成 $\sigma=1.04263$ 的 **weighted prime-pair hypothesis**，而不是直接假設完整 Hardy–Littlewood。
