# 14 — Claude Proposition 5.6 的 Exact $O_1$ Kernel
## Near-Diagonal Wedge、Selberg-Integral Barrier 與無條件結果審計

**日期：** 2026-08-11  
**狀態：** exact algebraic regrouping + asymptotic kernel extraction + literature audit  
**研究紀律：**
- exact symmetrisation 是 Proposition 5.6 公式的代數改寫；
- near-diagonal form 是在 $h/m\to0$ 下的 leading approximation；
- 現有無條件結果是否足夠，必須按其真正控制的 statistic 判斷，不能因為都叫「short intervals」就直接接上。

---

# 0. Claude 的原始 off-diagonal

Claude Proposition 5.6 定義：

$$
a_n=\frac{\Lambda(n)}{\sqrt n},
\qquad
y_n=\log n,
$$

以及：

$$
\alpha_n^+
=
\int_0^T\Phi(x)^2n^{ix}\,dx,
$$

$$
\alpha_n^-
=
\int_{-T}^0\Phi(x)^2n^{ix}\,dx.
$$

off-diagonal 為：

$$
O_1
=
\frac{1}{2\pi^2}
\Re
\sum_{n\ne m}
\frac{a_na_m}{i(y_n-y_m)}
\left[
\left(\frac nm\right)^{2iT}
(\alpha_m^++\alpha_n^-)
-
\left(\frac nm\right)^{iT}
(\alpha_n^++\alpha_m^-)
\right].
$$

Claude 目前只用 generalized Hilbert inequality 得：

$$
|O_1|\ll L^2X.
$$

與 diagonal：

$$
D\asymp TL^3
$$

比較，這正是：

$$
X\lesssim T
$$

即 support $\sigma\le1$ 的來源。

---

# 1. Exact unordered-pair symmetrisation

因為 $\Phi^2$ real and even：

$$
\alpha_n^-=\overline{\alpha_n^+}.
$$

寫：

$$
\alpha_n^+
=
G_T(y_n)+iH_T(y_n),
$$

其中：

$$
G_T(y)
=
\int_0^T\Phi(x)^2\cos(xy)\,dx,
$$

$$
H_T(y)
=
\int_0^T\Phi(x)^2\sin(xy)\,dx.
$$

對每一個 unordered pair：

$$
m<n,
$$

令：

$$
\vartheta=\log(n/m)>0,
\qquad
u=T\vartheta.
$$

把 ordered terms $(n,m)$ 與 $(m,n)$ 合併，exactly 得：

$$
\boxed{
\begin{aligned}
O_1
=
\frac1{\pi^2}
\sum_{m<n}
\frac{a_ma_n}{\vartheta}
\Big[
&
\big(G_T(y_m)+G_T(y_n)\big)
\big(\sin 2u-\sin u\big)
\\
&+
\big(H_T(y_m)-H_T(y_n)\big)
\big(\cos2u+\cos u\big)
\Big].
\end{aligned}
}
$$

這個等式不使用 prime-pair conjecture。

本包的 `o1_symmetrisation_check.json` 以 $1000$ 組隨機複數資料檢查原 ordered formula 與此 regrouping；最大 floating-point discrepancy 在機器誤差尺度。那只是程式檢查，exact proof 就是上述共軛配對代數。

---

# 2. $G_T$ 與 taper $g$

Claude 有 full Fourier identity：

$$
\int_{\mathbb R}
\Phi(x)^2e^{ixy}\,dx
=
2\pi g(y).
$$

因此：

$$
G_T(y)
=
\pi g(y)-E_T(y),
$$

其中：

$$
E_T(y)
=
\int_T^\infty
\Phi(x)^2\cos(xy)\,dx.
$$

所以 exact $O_1$ 可以拆成：

$$
O_1
=
O_{1,g}
+
O_{1,\mathrm{tail}}
+
O_{1,H}.
$$

其中 $O_{1,g}$ 是我們想與 weighted prime pairs 對接的 leading term；$E_T$ 與 $H_T$ 部分都是必須另外證明的 remainder obligations。

不能只因為 $g$ 看起來是主項，就默默刪掉 $H_T$。

---

# 3. 改寫成 additive shifts

令：

$$
n=m+h,
\qquad
h\ge1.
$$

leading $g$-kernel 是：

$$
\boxed{
K_g(m,h)
=
\frac{
g(\log m)+g(\log(m+h))
}{
\pi\sqrt{m(m+h)}\log(1+h/m)
}
\left[
\sin\!\left(2T\log(1+h/m)\right)
-
\sin\!\left(T\log(1+h/m)\right)
\right].
}
$$

因此：

$$
O_{1,g}
=
\sum_{h\ge1}
\sum_{m+h\le X}
\Lambda(m)\Lambda(m+h)K_g(m,h).
$$

這就是 WPPH 真正要控制的 weighted prime-pair sum。

---

# 4. Near-diagonal universal kernel

若：

$$
h=o(m),
$$

則：

$$
\log(1+h/m)
=
\frac hm+O(h^2/m^2),
$$

且：

$$
\frac1{
\sqrt{m(m+h)}\log(1+h/m)
}
=
\frac1h
\left(1+O(h/m)\right).
$$

再忽略 taper tail與 $g$ 的小變化，得到：

$$
K_g(m,h)
\approx
\frac{2g(\log m)}{\pi h}
\left[
\sin\left(\frac{2hT}{m}\right)
-
\sin\left(\frac{hT}{m}\right)
\right].
$$

令 local shift scale：

$$
H(m)=\frac mT,
$$

以及：

$$
u=\frac h{H(m)}=\frac{hT}{m}.
$$

則：

$$
\boxed{
K_g(m,h)
\approx
\frac{2Tg(\log m)}{\pi m}
\kappa(u),
}
$$

其中：

$$
\boxed{
\kappa(u)
=
\frac{\sin2u-\sin u}{u}
=
\frac{2\sin(u/2)\cos(3u/2)}{u}.
}
$$

並以連續延伸定義：

$$
\kappa(0)=1.
$$

這是一個 signed oscillatory kernel，而不是正的 averaging window。

因此只用 absolute-value mean-square bound，通常會丟失 WPPH 真正依靠的 cancellation。

---

# 5. 不是一個 shift，而是一個 wedge

令：

$$
X=T^\sigma,
$$

並按：

$$
m=T^\alpha
$$

分層。

真正跨出 diagonal-only regime 的部分是：

$$
1\le\alpha\le\sigma.
$$

local shift scale：

$$
H(m)=\frac mT=T^{\alpha-1}.
$$

所以 $P_{70}$ 的 arithmetic input 並不是只處理：

$$
h\sim X/T.
$$

而是處理一個 wedge：

$$
\boxed{
1
\lesssim h
\lesssim
T^{\sigma-1},
\qquad
m\in[T,T^\sigma].
}
$$

對 flat/Fejér-type taper：

$$
g(\log m)
\approx
(\sigma-\alpha)\log T.
$$

因此 wedge 頂端雖有最大的 shift，taper weight卻趨近零；真正權重分布不是 uniform。

作為簡單 diagnostic，flat taper diagonal weight落在 $m\ge T$ 的比例為：

$$
\boxed{
1-\frac3{\sigma^2}+\frac2{\sigma^3}.
}
$$

對：

$$
\sigma_{70}\approx1.042628,
$$

只有約：

$$
0.488\%.
$$

這和 v10 發現 optimizer 真正位於 $|\alpha|>1$ 的 Fourier mass只有約 $0.114\%$ 互相呼應：$P_{70}$ 只使用極薄的一層新資訊，但跨界本身仍是質變。

---

# 6. 現有無條件 Selberg integral 為什麼沒有直接解掉 WPPH？

Zaccagnini 的 survey 定義：

$$
J(x,\theta)
=
\int_x^{2x}
|\psi(t+\theta t)-\psi(t)-\theta t|^2dt.
$$

並記錄：

$$
J(x,\theta)=o(x^3\theta^2)
$$

可無條件取得於大致：

$$
\theta\ge x^{-5/6-\varepsilon(x)}.
$$

若：

$$
H=\theta x,
$$

就是：

$$
H\ge X^{1/6-o(1)}.
$$

但 $P_{70}$ wedge 最大 shift scale只有：

$$
H_{\max}
=
X^{1-1/\sigma_{70}}
\approx
X^{0.040885}.
$$

所以 range 本身已不相交：

$$
0.040885
<
\frac16.
$$

此外：

$$
J=o(XH^2)
$$

是「幾乎所有短區間具有 PNT」的尺度。

WPPH 要的是一個 signed weighted second-correlation constant，接近 conjectural：

$$
XH\log(X/H)
$$

型 variance，而不是只知道它比 $XH^2$ 小。

因此該 unconditional statement本身既不在所需 range，也不提供所需精細 constant。

---

# 7. 2026 higher-uniformity 結果是否幫忙？

Matomäki–Radziwiłł–Shao–Tao–Teräväinen 的 almost-all-interval result對 $\Lambda$ 可在：

$$
H\ge X^{1/3+\varepsilon}
$$

建立高階 uniformity / nilsequence discorrelation，並推出一類「一個變量做短平均」的 Hardy–Littlewood結果。

這是非常強的新進展，但對本問題仍有兩個不匹配：

1. range：

$$
\frac13
\gg
0.040885;
$$

2. statistic：它不是 Claude $O_1$ 所需的 weighted prime-pair second-trace asymptotic。

所以不能只看到「short-averaged Hardy–Littlewood」就宣布 WPPH 已成立。

---

# 8. 本輪無條件審計結論

目前查到的結果尚不足以由 Claude 的 $O_1$ pipeline 無條件證：

$$
P_{70}.
$$

更嚴格地說，它們也尚未給出一條清楚、已證的 implication：

$$
67.25\%
\longrightarrow
q>67.25\%
$$

沿 generalized-support route。

原因不是完全沒有短區間資訊，而是：

$$
\boxed{
\text{range}
+
\text{statistic}
+
\text{constant/sign}
}
$$

三者必須同時匹配。

---

# 9. 下一個較合理的問題

與其繼續拿一般 short-interval theorem 硬套 WPPH，更合理的是：

## Kernel-Matched Selberg Problem（KMSP）

對本文件的 exact kernel：

$$
K_g(m,h)
$$

建立專門的 weighted correlation bound：

$$
\sum_{h,m}
\Big(
\Lambda(m)\Lambda(m+h)-\mathfrak S(h)
\Big)
K_g(m,h).
$$

目標不是先證完整 prime-pair conjecture，而是利用：

- $\kappa(u)$ 的 sign oscillation；
- taper wedge；
- $H_T$ correction 的結構；
- $m$ 與 $h$ 的聯合 smoothness；

直接取得：

$$
o(TL^3)
$$

或一個足以改善 $67.25\%$ 的 one-sided bound。

這是目前 direct arithmetic route 最精確的 proof obligation。
