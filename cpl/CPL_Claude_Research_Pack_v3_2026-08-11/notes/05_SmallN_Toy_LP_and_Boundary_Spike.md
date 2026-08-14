# 05 — Small-$N$ Primal Toy LP 與 Boundary-Spike Escape
## 第一次自行重現 bandwidth-one adversarial-law 機制

**日期：** 2026-08-11  
**狀態：** Exploratory / toy-model result  
**限制：** 不是 Anthropic $N=256$ exact-rational LP 的重現；本模型將 positions 限制在離散圓格點。

---

## 1. Toy primal

配置：

$$
n_k\in\{0,1,2\},
\qquad
\sum_{k=0}^{M-1}n_k=N.
$$

simple fraction：

$$
p(\mathcal C)
=
\frac{\#\{k:n_k=1\}}{N}.
$$

form factor：

$$
S_{\mathcal C}(j)
=
\frac1N
\left|
\sum_{k=0}^{M-1}n_ke^{2\pi ijk/M}
\right|^2.
$$

對配置 law $w_c$ 解：

$$
\min_{w_c}\sum_cw_cp_c
$$

subject to：

$$
w_c\ge0,\qquad\sum_cw_c=1,
$$

以及：

$$
\sum_cw_cS_c(j)=\frac jN,
\qquad j=1,\ldots,N-1.
$$

---

## 2. Open-band 結果

我們已自行解出的代表值：

| $N$ | $M$ | $p_{\min}$ |
|---:|---:|---:|
| 4 | 8 | 71.3388% |
| 4 | 12 | 70.8333% |
| 4 | 16 | 70.4798% |
| 4 | 24 | 70.1828% |
| 5 | 10 | 70.9443% |
| 5 | 15 | 70.3565% |
| 5 | 20 | 70.0460% |
| 6 | 18 | 70.0966% |
| 7 | 14 | 70.6078% |
| 8 | 16 | 70.5267% |

因此，即使在比官方窄很多的 toy configuration class 裡，也已出現：

$$
\boxed{
\text{open-band pair rows 完全匹配 CUE}
\not\Rightarrow
\text{simple fraction 接近 }1.
}
$$

我們的 toy floor 約在 $70\%$ 附近；官方更寬的 rational-position configuration law 可壓至約 $68.18\%$。

---

## 3. $N=4,M=24$ 的顯式 mixture

LP 的極值只需四個 support configurations；詳細資料見：

```text
results/toy_optimal_law_N4_M24.csv
```

其混合後：

$$
\bar S(1)=\frac14,\qquad
\bar S(2)=\frac12,\qquad
\bar S(3)=\frac34,
$$

但：

$$
\bar p
=
0.7018283569\ldots.
$$

未被限制的 closed-band row 卻是：

$$
\bar S(4)
\approx3.68563.
$$

---

## 4. 官方 $N=256$ 的 boundary spike

Anthropic `LawN256.lean` 給：

$$
|256S(j)-j|
\le3\times10^{-40},
\qquad
1\le j<256.
$$

但最後一個 row enclosure 配上：

$$
K=2^{140}
$$

可算出：

$$
\boxed{
S(256)\approx211.432009142486.
}
$$

也就是：

```text
open band j<256:
幾乎完美 CUE ramp

closed row j=256:
巨大 spike
```

若把前 $255$ rows 暫視為 exact $j/256$，則：

$$
D(1)
=
\frac1{256}\sum_{j=1}^{256}S(j)-\frac12
\approx
\frac{S(256)-1/2}{256}
\approx0.82395316,
$$

與官方 kernel-checked：

$$
|D(1)|\le0.82395317
$$

吻合。

這是一個相當強的線索：低 simple-fraction extremal law 把大量可區分資訊推入 open-band 之外／邊界的 channel。

---

## 5. Boundary-row cap experiment

保持所有 $j<N$ rows 完全不變，只加入：

$$
\mathbb E[S(N)]\le B.
$$

對 $N=4,M=24$：

| $B$ | $p_{\min}$ |
|---:|---:|
| unconstrained $\approx3.686$ | 70.18% |
| 3.5 | 70.65% |
| 3.0 | 72.49% |
| 2.5 | 74.85% |
| 2.0 | 77.20% |
| 1.5 | 79.55% |
| 1.25 | 80.73% |
| 1.0 | 81.91% |

$N=5,6$ 顯示同樣方向。

所以 toy model 已實際驗證：

$$
\boxed{
\text{只增加一個 boundary observable，
就能顯著提高 adversarial simple-fraction floor。}
}
$$

---

## 6. Support extension experiment

強制：

$$
S(j)=\min(j/N,1)
$$

到更高 rows。

對 $N=4,M=24$：

$$
j\le3
\Rightarrow70.18\%,
$$

$$
j\le4
\Rightarrow81.91\%,
$$

$$
j\le5
\Rightarrow88.85\%,
$$

$$
j\le6
\Rightarrow92.46\%.
$$

其他 $N$ 也有同樣定性趨勢。

**這些百分比不能與 Claude 的真實 support thresholds $1.04,1.26,1.70$ 對號入座。**
toy grid 太窄，而且 row sampling 過於粗糙。

但它已經重現「support expansion 排除 adversarial laws」的機制。

---

## 7. Boundary-Spike Obstruction（BSO）

暫定義：

> 在只固定 open-band pair-correlation observables 時，低 simple-fraction configuration law 可以將區分 multiplicity/collision structure 的大量訊息轉移到 $\alpha\approx1$ 或更外側的未觀測頻帶，使其在 open band 中與理想 CUE 資料幾乎不可辨識。

形式上：

$$
\mathcal O_{<1}(\mathcal L_{\mathrm{bad}})
\approx
\mathcal O_{<1}(\mathcal L_{\mathrm{CUE}}),
$$

但：

$$
p(\mathcal L_{\mathrm{bad}})
\ll1,
$$

且：

$$
\mathcal O_{\ge1}(\mathcal L_{\mathrm{bad}})
$$

出現強烈偏離。

這個概念目前由：

1. Anthropic exact $N=256$ law 的 $S(256)\approx211.43$；
2. 我們 small-$N$ toy LP 的 boundary spikes；

共同支持。

---

## 8. 對 $70\%$ 的新解讀

Claude 的論文說 same-route 要達：

$$
70\%
$$

約需 pair-correlation support：

$$
1.04.
$$

本輪給出一個更具體的機制猜想：

$$
\boxed{
\text{$1.04$ 的作用可能正是開始看到足以排除 boundary-spike extremal laws 的資料。}
}
$$

這還不是定理，需要下一輪重建 Claude 用來估 $1.04$ 的 extremal law。

---

## 9. 下一輪

### Route A — Continuous-position column generation

目前 brute-force toy grid：

$$
M/N
$$

增加時 floor 下降，但成本爆炸。

下一步改成：

```text
Restricted Master LP
        ↓
dual prices
        ↓
configuration pricing problem
        ↓
nonlinear / discrete search
        ↓
new adverse column
        ↓
repeat
```

目標：不枚舉所有 configurations，逐步逼近官方 continuous rational-position primal。

### Route B — Minimal Escape Information

定義：

$$
I^*_{70}
=
\inf\{
\text{extra observable strength}:
p_{\min}\ge0.70
\}.
$$

分別測：

- boundary-row inequality；
- small support extension；
- higher spectral moment；
- zeta-specific realizability constraint。

這會把「$70\%$」真正轉成一個 optimisation problem。
