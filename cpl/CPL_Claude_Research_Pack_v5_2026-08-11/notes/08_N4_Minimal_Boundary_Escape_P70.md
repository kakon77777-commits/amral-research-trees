# 08 — Toy $P_{70}$ 的 Minimal Boundary-Escape Frontier
## $S(4)$ 多知道多少，才開始跨過 $70\%$？

**日期：** 2026-08-11  
**狀態：** numerical column-generation frontier；尚未 exact-rational certification  
**作用域：** $N=4$ continuous-position toy model

---

# 0. 問題

open-band toy 只知道：

$$
S(1),S(2),S(3).
$$

現在加入一條最小額外資訊：

$$
\boxed{
\mathbb E[S(4)]\le B.
}
$$

重新求：

$$
p_{\min}(B).
$$

目標是找：

$$
B^*_{70}
=
\sup\{
B:
p_{\min}(B)\ge0.70
\}.
$$

---

# 1. Continuous column-generation candidate

本輪重新求得：

$$
B=3.67
\quad\Longrightarrow\quad
p_{\min}^{cand}
=
69.9981973\%.
$$

而：

$$
B=3.65
\quad\Longrightarrow\quad
p_{\min}^{cand}
=
70.0595514\%.
$$

所以 numerical threshold 被夾在：

$$
\boxed{
3.65
<
B^*_{70}
<
3.67
}
$$

附近。

以這兩點做局部線性插值，得到探索性：

$$
B^*_{70}
\approx
3.66941.
$$

**此 $3.66941$ 不是 theorem。**

它只是下一個 exact certificate 要瞄準的位置。

---

# 2. 為什麼這有概念價值？

open-band optimum 本身的 boundary row 約：

$$
S(4)\approx3.73
$$

量級。

所以要把 $N=4$ floor 從約：

$$
69.82\%
$$

推過：

$$
70\%,
$$

不需要把 boundary row 強行壓到 CUE value：

$$
1.
$$

只需要排除最極端的一小部分 spike freedom。

也就是：

$$
\boxed{
\text{突破 $70\%$ 所需的資訊}
\ll
\text{完整知道 boundary row}.
}
$$

這正是「minimal escape information」概念想測的東西。

---

# 3. Dual price 的意義

在：

$$
S(4)\le B
$$

加入 master 後，boundary constraint 的 numerical dual price 約：

$$
-0.0307.
$$

這表示在當前局部 regime，稍微收緊 $B$，certificate floor 以大約：

$$
0.0307
$$

的比例提升。

直觀上：

> 原本 $S(4)$ 是免費藏資訊的方向；現在它開始有價格。

---

# 4. 下一個 certification target

對：

$$
B=3.65
$$

numerical dual candidate 約為：

$$
c_0\approx1.12274224,
$$

$$
y_1\approx-0.38437941,
$$

$$
y_2\approx-0.25114540,
$$

$$
y_3\approx-0.11796917,
$$

$$
\mu_4\approx-0.03068556.
$$

若把 $c_0$ 下調 $5\times10^{-5}$ 留 safety margin：

$$
c_0=1.12269224,
$$

則 dual objective 仍為：

$$
\boxed{
0.700545516
=
70.0545516\%.
}
$$

而 numerical global search 對三種 multiplicity patterns 的最小 reduced-cost 都約為：

$$
5\times10^{-5}>0.
$$

所以這是一個非常強的 **exact-certificate candidate**。

目前剩下的工作不是再找數字，而是把：

$$
(1,1,1,1)
$$

三位置自由度的 positivity 也轉成 exact polynomial / SOS / interval certificate。

一旦完成，就會得到 toy model 第一個真正的：

$$
\boxed{
P_{70}\text{ escape certificate}.
}
$$

---

# 5. 與真 Claude $1.04$ support 的關係

這裡：

$$
S(4)
$$

對 $N=4$ toy 恰好位在 normalized boundary：

$$
\alpha=1.
$$

真 zeta 問題中，Claude 論文估計 $70\%$ 約需要：

$$
\sigma\approx1.04.
$$

兩者不能數字對號。

但結構上很一致：

$$
\text{open-band ceiling}
\rightarrow
\text{開始看 boundary / beyond-band}
\rightarrow
\text{adversarial feasible set 收縮}.
$$

所以 $N=4$ toy 的角色不是預測：

$$
1.04,
$$

而是解剖：

> **為什麼一旦開始對 boundary-spike 收費，比例 floor 就會上升？**

---

# 6. 下一步的嚴格化工具

對三點自由度的 fully-simple pattern，最自然的下一層不是再增加 brute-force sampling，而是：

1. trigonometric polynomial positivity；
2. Fejér–Riesz / Hermitian-square；
3. SOS / SDP relaxation；
4. exact rational rounding；
5. proof-assistant replay。

這和既有的 exact SOHS / SDP positivity certification 技術完全相容。
