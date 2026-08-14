# 09 — Exact $P_{70}$ Boundary-Escape Certificate
## $N=4$ continuous toy model 首次嚴格跨過 $70\%$

**日期：** 2026-08-11  
**狀態：** exact-rational finite certificate  
**重要限制：** 這是我們定義的 $N=4$ toy marked-configuration theorem，不是 Riemann zeta 零點的新定理。

---

# 0. 主結果

考慮 total multiplicity：

$$
N=4,
$$

marks：

$$
m_i\in\{1,2\},
$$

positions 可連續位於 unit circle。

令：

$$
S(j)
=
\frac14
\left|
\sum_i m_i e^{ij\theta_i}
\right|^2.
$$

對任意 probability law over configurations，假設：

$$
\mathbb E[S(1)]=\frac14,
$$

$$
\mathbb E[S(2)]=\frac12,
$$

$$
\mathbb E[S(3)]=\frac34,
$$

以及：

$$
\mathbb E[S(4)]\le B.
$$

我們現在可用 exact-rational dual + exact-rational Bernstein subdivision 嚴格證明：

$$
\boxed{
B
\le
\frac{11254781}{3068556}
}
$$

即：

$$
\boxed{
B\le3.667777612662112\ldots
}
$$

時必有：

$$
\boxed{
\mathbb E[p]\ge0.70.
}
$$

因此 toy minimal-escape threshold：

$$
B_{70}^*
=
\sup\{B:p_{\min}(B)\ge0.70\}
$$

至少滿足：

$$
\boxed{
B_{70}^*
\ge
3.667777612662112\ldots
}
$$

上一輪 numerical column generation 顯示 crossing 約在：

$$
3.6694
$$

附近；所以 exact certificate 已經逼得非常近，但 numerical side 尚不是 rigorous upper bound。

---

# 1. Exact dual

取：

$$
c_0
=
1.12269224,
$$

$$
y_1=-0.38437941,
$$

$$
y_2=-0.25114540,
$$

$$
y_3=-0.11796917,
$$

以及 boundary price：

$$
\mu=-0.03068556.
$$

configuration-wise 要證：

$$
c_0
+
y_1S(1)
+
y_2S(2)
+
y_3S(3)
+
\mu S(4)
\le
p.
$$

注意此不等式與 $B$ 無關；$B$ 只進入 dual objective。

open-band objective constant：

$$
A
=
c_0
+
\frac14y_1
+
\frac12y_2
+
\frac34y_3
=
0.81254781.
$$

所以：

$$
L(B)
=
A+\mu B.
$$

令：

$$
L(B)=0.70
$$

就得到 exact：

$$
\boxed{
B_{cert}
=
\frac{11254781}{3068556}
=
3.667777612662112\ldots.
}
$$

因為：

$$
\mu<0,
$$

所以所有：

$$
B\le B_{cert}
$$

都有：

$$
L(B)\ge0.70.
$$

---

# 2. Pattern $(2,2)$

固定位置：

$$
0,\theta,
$$

令：

$$
q=\cos\theta.
$$

reduced cost 變成 exact quartic：

$$
R_{22}(q)
=
\frac{
12274224q^4
+
23593834q^3
+
12840316q^2
+
1523595q
+
118679
}{
25000000
}.
$$

把：

$$
q=2Q-1,
\qquad
Q\in[0,1]
$$

轉成 Bernstein basis 後做 exact midpoint subdivision。

結果：

- internal nodes：$7$；
- terminal intervals：$8$；
- max depth：$7$；
- minimum terminal Bernstein coefficient：

$$
\boxed{
\frac{46501207}{1638400000000}
>
0.
}
$$

故：

$$
R_{22}(q)>0
$$

對全部：

$$
q\in[-1,1].
$$

---

# 3. Pattern $(2,1,1)$

固定 double point at $0$，另外兩個 simple points phases $\alpha,\beta$。

令：

$$
u=\frac{\alpha+\beta}{2},
\qquad
v=\frac{\alpha-\beta}{2},
$$

$$
x=\cos u,
\qquad
z=\cos v.
$$

則：

$$
S_j
=
1+T_j(z)^2+2T_j(z)T_j(x),
$$

其中 $T_j$ 是 Chebyshev polynomial。

加入 $j=4$ 後：

$$
R_{211}(x,z)
$$

成為 degree：

$$
(4,8)
$$

的 exact rational bivariate polynomial。

映射到：

$$
[0,1]^2
$$

後 exact Bernstein subdivision 得：

- internal nodes：$61$；
- terminal boxes：$62$；
- maximum depth：$12$；
- minimum terminal coefficient：

$$
\boxed{
\frac{
10973215641
}{
734003200000000
}
>
0.
}
$$

故整個 continuous $(2,1,1)$ configuration space 通過。

---

# 4. Pattern $(1,1,1,1)$：最關鍵的新步驟

這一支原本有三個連續 phase 自由度。

直接三角 subdivision 很笨重，因此改用 unit-circle root structure。

設四個 roots：

$$
z_1,z_2,z_3,z_4,
\qquad
|z_i|=1.
$$

因為 form factors：

$$
|p_j|^2
$$

在共同旋轉下不變，可以把 roots 同時旋轉，使：

$$
e_4=z_1z_2z_3z_4=1.
$$

令：

$$
A=e_1=x+iy,
$$

$$
B=e_2.
$$

unit-circle self-inversive relation給：

$$
e_3=\overline A,
$$

且：

$$
B\in\mathbb R.
$$

Newton identities給 power sums：

$$
p_1=A,
$$

$$
p_2=A^2-2B,
$$

$$
p_3=A^3-3AB+3\overline A,
$$

$$
p_4
=
A^4
-
4A^2B
+
4|A|^2
+
2B^2
-
4.
$$

而：

$$
S(j)=\frac{|p_j|^2}{4}.
$$

---

# 5. 降成三個實變量

定義：

$$
u=|A|^2,
$$

$$
v=\Re(A^2).
$$

由：

$$
|A|\le4
$$

得：

$$
0\le u\le16.
$$

而：

$$
|v|\le u,
$$

故可令：

$$
v=ut,
\qquad
-1\le t\le1.
$$

同時：

$$
B=e_2
$$

是六個 unit complex products 的和，因此粗略但充分地有：

$$
|B|\le6.
$$

所以所有真正 fully-simple root configurations 都落在：

$$
\boxed{
(u,t,B)
\in
[0,16]\times[-1,1]\times[-6,6].
}
$$

注意這是一個 **superset**；我們在更大的 domain 上證正，因此對真正 root configuration 自動成立。

---

# 6. Exact 3D Bernstein certificate

fully-simple reduced cost：

$$
R_{1111}
=
1-c_0
+
\sum_{j=1}^4
a_jS(j),
$$

其中：

$$
a_j=-y_j
$$

且：

$$
a_4=-\mu.
$$

代入 Newton identities、再改用 $(u,t,B)$ 後得到 exact rational polynomial：

$$
R_{1111}(u,t,B).
$$

映射：

$$
u=16U,
$$

$$
t=2T-1,
$$

$$
B=12C-6,
$$

到：

$$
(U,T,C)\in[0,1]^3.
$$

其 multidegree 是：

$$
(4,2,4).
$$

使用 exact rational Bernstein midpoint subdivision：

- internal boxes：$179$；
- terminal boxes：$180$；
- max depth：$13$；
- 所有 terminal Bernstein coefficients 非負；
- minimum terminal coefficient：

$$
\boxed{
\frac1{20000}
=
5\times10^{-5}.
}
$$

因此：

$$
\boxed{
R_{1111}\ge5\times10^{-5}>0
}
$$

甚至在那個比真 root data 更大的 box 上成立。

這完成了最後一個 multiplicity pattern。

---

# 7. 因而得到 toy $P_{70}$ theorem

三種 patterns：

$$
(2,2),
$$

$$
(2,1,1),
$$

$$
(1,1,1,1)
$$

全部 configuration-wise valid。

所以對任何 probability mixture，若：

$$
\mathbb E[S(1)]=\frac14,
$$

$$
\mathbb E[S(2)]=\frac12,
$$

$$
\mathbb E[S(3)]=\frac34,
$$

$$
\mathbb E[S(4)]\le
\frac{11254781}{3068556},
$$

就由弱對偶得到：

$$
\boxed{
\mathbb E[p]\ge70\%.
}
$$

---

# 8. 這個結果的研究意義

我們現在第一次真的完成：

$$
\text{open-band ceiling}
\rightarrow
\text{增加一條 boundary observable}
\rightarrow
\text{嚴格跨過 }70\%.
$$

所以 toy model 中的：

$$
\boxed{
\text{Minimal Escape Information}
}
$$

已不再只是 numerical intuition。

而且 boundary constraint 並不需要：

$$
S(4)\le1.
$$

只要：

$$
S(4)\lesssim3.66778
$$

就已足以保證 $70\%$。

這再次說明：

> 要突破 ceiling，未必需要完整掌握 boundary；只需足以排除最極端 adversarial spike 的少量新資訊。

---

# 9. 與 Claude 真實 $70\%$ 問題的關係

Claude 真實論文估計同一路線要從 Fourier support：

$$
1
$$

擴張到約：

$$
1.04
$$

才能達 $70\%$。

我們的 toy theorem不能推出：

$$
1.04.
$$

但它嚴格證明了對應的機制命題：

$$
\boxed{
\text{一旦新增能約束 boundary-spike 的 observable，
bandwidth-one ceiling 可以被穿越。}
}
$$

因此下一階段真正值得研究的是：

1. 把離散 $S(4)$ constraint 替換成小幅 continuous support extension；
2. 找 toy analogue：

$$
\delta^*_{70};
$$

3. 再研究它如何與 Claude 的：

$$
\sigma_{70}\approx1.04
$$

建立定量對照。

---

# 10. 下一步

下一個自然目標有兩個。

## A. Exact threshold refinement

目前 exact：

$$
B_{70}^*
\ge3.66777761266\ldots
$$

numerical crossing 約：

$$
3.6694.
$$

可以嘗試重新 optimize rational dual，把 certificate threshold 再往 numerical crossing 推。

## B. Support-strip replacement

不要只加入單一：

$$
S(4)
$$

而加入一小段：

$$
\alpha\in[1,1+\delta].
$$

研究：

$$
\delta_{70}^*
=
\inf\{\delta:p_{\min}\ge0.70\}.
$$

這會開始真正接回 Claude 的 $1.04$。
