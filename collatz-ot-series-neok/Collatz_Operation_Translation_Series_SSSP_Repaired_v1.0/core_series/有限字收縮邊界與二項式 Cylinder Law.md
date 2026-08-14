# 有限字收縮邊界與二項式 Cylinder Law
## ——從 Exact Affine Drift、字序修正到 $89.4943\%$ 的純組合解釋

**English Title:** *Finite-Word Contraction Boundaries and the Binomial Cylinder Law in the Collatz Local Affine Atlas*

**作者：** Neo.K  
**機構：** 一言諾科技有限公司（EveMissLab）  
**系列：** Collatz Operation Translation Series — Paper 05  
**版本：** v0.1  
**日期：** 2026-08-10

---

## 摘要

Paper 02–04 已建立 modified Collatz map 的 finite-word affine closure、parity-word/residue-cylinder 對應與雙向精確殘餘類轉譯。對任意長度 $k$ 的 admissible parity word $w$，令 $u=u(w)$ 為 odd branch $U$ 的總次數，則在其唯一 source cylinder 上：

$$
\boxed{
T^k(n)
=
F_w(n)
=
\frac{3^u n+b_w}{2^k},
}
$$

其中：

$$
b_w\ge0
$$

是由字序決定的 exact affine correction。

本文回答下一個問題：

> 一張 fixed-word chart 在何種條件下，能保證 $k$ 步後下降到起點以下？

直接比較：

$$
F_w(n)<n
$$

得到：

$$
\boxed{
b_w<(2^k-3^u)n.
}
$$

因此有限字存在一條完全由主乘數決定的結構邊界：

$$
\boxed{
3^u<2^k
}
$$

與

$$
\boxed{
3^u>2^k.
}
$$

若：

$$
3^u<2^k,
$$

則 $w$ 稱為 **contracting word**，且存在 exact finite threshold

$$
\boxed{
\theta_w
=
\left\lfloor
\frac{b_w}{2^k-3^u}
\right\rfloor+1
}
$$

使所有 admissible：

$$
n\ge\theta_w
$$

都滿足：

$$
T^k(n)<n.
$$

若：

$$
3^u>2^k,
$$

則因 $b_w\ge0$，

$$
\boxed{
T^k(n)>n
}
$$

對該 chart 中每一個 positive admissible $n$ 都成立；此時不是「漸近上升」，而是整張 positive cylinder 都是 $k$-block expanding。

對任何非空有限字，不存在：

$$
3^u=2^k,
$$

因為 $2$ 與 $3$ 的質因數分解互斥。因此每一個 nonempty parity word 都嚴格落在 contracting 或 expanding 一側；唯一的 block equality 只能由 affine correction 抵消主收縮造成，即：

$$
T^k(n)=n
\iff
n=\frac{b_w}{2^k-3^u}
$$

且右側必須是 admissible positive integer。

定義：

$$
\alpha
=
\frac{\ln2}{\ln3}
\approx
0.6309297536.
$$

則：

$$
3^u<2^k
\iff
\frac uk<\alpha.
$$

由 $\alpha$ 無理，$\alpha k$ 對任何正整數 $k$ 皆非整數，所以 length-$k$ contracting words 的 exact count 為：

$$
\boxed{
A_k
=
\sum_{u=0}^{\lfloor\alpha k\rfloor}
\binom{k}{u}.
}
$$

由 Paper 03 的 word–residue bijection，這同時也是 modulo $2^k$ contracting residue cylinders 的數量。因此其 cylinder-class proportion：

$$
\boxed{
P_k
=
\frac{1}{2^k}
\sum_{u=0}^{\lfloor\alpha k\rfloor}
\binom{k}{u}.
}
$$

對：

$$
k=16,
$$

有：

$$
\lfloor16\alpha\rfloor=10,
$$

故：

$$
A_{16}
=
\sum_{u=0}^{10}\binom{16}{u}
=
58651
$$

以及：

$$
\boxed{
P_{16}
=
\frac{58651}{65536}
=
0.8949432373\ldots
}
$$

即：

$$
\boxed{
89.4943237\%.
}
$$

這從純數學解釋了先前 finite-verification prototype 中 $k=16$ 出現的約 $89.494\%$ cylinder pruning 現象。但本文進一步校正：**cylinder-class proportion 與特定有限區間內的 strict-descent certificate proportion 並不完全相同。**

在實驗域：

$$
1\le n<2^{20},
$$

$k=16$ 的 exact strict-descent certificate 數為：

$$
938413,
$$

比例：

$$
\boxed{
\frac{938413}{1048575}
=
89.4941229\%\ldots
}
$$

與 $P_{16}$ 的微小差異來自有限邊界與 block equality：residue $0$ 的 $n=0$ 不屬於 positive domain，而 $n=1,2$ 在 16 modified-Collatz steps 後回到自身，因此不滿足嚴格 $<$。所以先前 rounded benchmark 與 $89.4943\%$ 的高度一致，並非數值偶然，但「class density」與「finite strict certificate rate」必須精確區分。

由於：

$$
\alpha>\frac12
$$

（等價於 $3<4$），若令：

$$
X_k\sim\operatorname{Binomial}(k,1/2),
$$

則：

$$
P_k
=
\Pr(X_k\le\alpha k)
$$

在整數閾值意義下成立，因而由大數律：

$$
\boxed{
P_k\to1.
}
$$

甚至由 Chernoff large-deviation bound：

$$
1-P_k
\le
\exp\left(
-kD\!\left(\alpha\middle\|\frac12\right)
\right),
$$

其中：

$$
D\!\left(\alpha\middle\|\frac12\right)
=
\alpha\ln(2\alpha)
+
(1-\alpha)\ln(2(1-\alpha))
\approx
0.0346882.
$$

所以 expanding finite-word cylinders 的組合比例以 exponential rate 趨向 0。

然而本文最重要的量詞警告也由此變得更清楚：

$$
\boxed{
P_k\to1
\not\Rightarrow
\text{Collatz conjecture}.
}
$$

density-one 的 finite-word contraction 不能排除一條 ordinary positive-integer orbit 持續穿越稀有 expanding／correction-dominated prefixes。這正與既有 parity-vector、stopping-time、paradoxical-sequence 與 Tao 的 almost-all 結果形成清楚的邏輯邊界。

本文因此完成從「平均上 2 的除法會戰勝 3」的舊 heuristic，到以下 exact finite-word statement 的升級：

$$
\boxed{
\text{finite-word drift sign is determined exactly by }3^u\lessgtr2^k,
}
$$

而字序只影響 contracting side 上的有限 correction threshold，不改變 asymptotic side。

**關鍵詞：** Collatz conjecture、contraction boundary、parity word、binomial law、residue cylinder、stopping time、affine correction、large deviations、finite verification、operation translation

---

# 1. 從 Local Affine Atlas 到 Descent

Paper 03 對 fixed parity word：

$$
w\in\{D,U\}^k
$$

建立唯一 admissible residue cylinder：

$$
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}.
$$

Paper 02 給：

$$
\boxed{
T^k(n)
=
\frac{3^un+b_w}{2^k}
}
$$

對所有：

$$
n\in\Omega_w.
$$

因此 stopping-time 類問題在 fixed chart 中不再需要逐步分析。

只需比較一個 affine operator 與 identity。

---

# 2. Exact Descent Equation

考察：

$$
T^k(n)-n.
$$

有：

$$
T^k(n)-n
=
\frac{3^un+b_w}{2^k}-n
$$

$$
=
\boxed{
\frac{
(3^u-2^k)n+b_w
}{
2^k
}.
}
$$

因此：

$$
T^k(n)<n
$$

當且僅當：

$$
\boxed{
b_w<(2^k-3^u)n.
}
$$

這是本文所有收縮結果的母式。

---

# 3. Drift Gap

定義：

$$
\boxed{
\Delta_{k,u}
=
2^k-3^u.
}
$$

則：

$$
T^k(n)-n
=
\frac{
b_w-\Delta_{k,u}n
}{2^k}.
$$

所以 fixed-word behavior 可依：

$$
\operatorname{sgn}\Delta_{k,u}
$$

分類。

---

# 4. Contracting Word

若：

$$
\boxed{
\Delta_{k,u}>0
}
$$

即：

$$
\boxed{
3^u<2^k,
}
$$

則：

$$
T^k(n)<n
$$

等價於：

$$
n>\frac{b_w}{\Delta_{k,u}}.
$$

所以定義：

$$
\boxed{
\theta_w
=
\left\lfloor
\frac{b_w}{2^k-3^u}
\right\rfloor+1.
}
$$

得到：

## Theorem 4.1 — Exact Contracting Threshold

若：

$$
3^u<2^k,
$$

則對所有：

$$
n\in\Omega_w
$$

且：

$$
n\ge\theta_w,
$$

有：

$$
\boxed{
T^k(n)<n.
}
$$

---

# 5. Correction 只決定「何時開始下降」

對 contracting word：

主斜率：

$$
\lambda_w=\frac{3^u}{2^k}<1.
$$

但若：

$$
b_w>0,
$$

非常小的 $n$ 仍可能：

- 上升；
- 或恰好回到自身。

所以：

$$
\boxed{
3^u<2^k
}
$$

決定的是整張 cylinder 的最終方向，

而：

$$
\boxed{
b_w
}
$$

決定 finite-size threshold。

這正是：

$$
\boxed{
\text{multiplicative skeleton}
+
\text{order correction}
}
$$

在 descent problem 中的具體分工。

---

# 6. Expanding Word 比預期更強

若：

$$
3^u>2^k,
$$

則對任何：

$$
n>0,
$$

有：

$$
(3^u-2^k)n>0
$$

以及：

$$
b_w\ge0.
$$

所以：

$$
\boxed{
T^k(n)-n>0.
}
$$

因此：

## Theorem 6.1 — Uniform Block Expansion

若：

$$
\boxed{
3^u>2^k,
}
$$

則對所有 positive admissible：

$$
n\in\Omega_w,
$$

皆有：

$$
\boxed{
T^k(n)>n.
}
$$

所以 expanding word 不是只在 $n\to\infty$ 時上升。

整張 positive cylinder 在該 block 長度上都上升。

---

# 7. Nonempty Word 沒有 Neutral Slope

若：

$$
3^u=2^k,
$$

由唯一質因數分解，

必須：

$$
u=k=0.
$$

所以對：

$$
k\ge1,
$$

不可能有：

$$
3^u=2^k.
$$

因此：

$$
\boxed{
\text{every nonempty finite word is strictly on one side of the slope boundary}.
}
$$

即：

$$
\boxed{
3^u<2^k
\quad\text{or}\quad
3^u>2^k.
}
$$

---

# 8. Block Equality 仍然可能發生

雖然 slope 不可能等於 1，

contracting word 仍可能在某個特定 $n$：

$$
T^k(n)=n.
$$

由母式：

$$
(2^k-3^u)n=b_w.
$$

所以：

$$
\boxed{
n_w^\ast
=
\frac{b_w}{2^k-3^u}.
}
$$

若右側：

1. 為 positive integer；
2. 且屬於 $\Omega_w$；

則它是該 fixed-word block 的 periodic/fixed point。

所以：

$$
\boxed{
\text{slope contraction}
\neq
\text{strict descent at every finite point}.
}
$$

---

# 9. Collatz 平凡週期的 Block Equality

modified Collatz：

$$
1\to2\to1.
$$

因此任意偶數 block length：

$$
2q
$$

都有：

$$
T^{2q}(1)=1,
$$

$$
T^{2q}(2)=2.
$$

特別對：

$$
k=16,
$$

$n=1,2$ 均是：

$$
\boxed{
T^{16}(n)=n.
}
$$

所以即使其 16-step words 位於 contracting-slope side，

它們仍不是 strict-descent certificates。

---

# 10. Any Positive Cycle Must Live on Contracting-Slope Side

若某個 positive periodic orbit 有長度 $k$ parity word $w$，

則：

$$
T^k(n)=n.
$$

所以：

$$
(2^k-3^u)n=b_w.
$$

因：

$$
n>0,
\qquad
b_w\ge0,
$$

非平凡情況必須：

$$
\boxed{
2^k>3^u.
}
$$

亦即：

$$
\boxed{
\frac uk<
\frac{\ln2}{\ln3}.
}
$$

這是所有 positive periodic block 必須滿足的必要條件。

它不排除非平凡 Collatz cycles；

只把可能 cycle word 限制在 contracting-slope side。

---

# 11. Critical Odd-Step Fraction

定義：

$$
\boxed{
\alpha
=
\frac{\ln2}{\ln3}.
}
$$

數值：

$$
\boxed{
\alpha
\approx0.6309297535714574.
}
$$

則：

$$
3^u<2^k
$$

等價於：

$$
u\ln3<k\ln2,
$$

即：

$$
\boxed{
\frac uk<\alpha.
}
$$

---

# 12. $\alpha$ 是無理數

假設：

$$
\alpha=\frac pq
$$

為有理數。

則：

$$
\frac{\ln2}{\ln3}
=
\frac pq
$$

推出：

$$
q\ln2=p\ln3
$$

所以：

$$
2^q=3^p.
$$

由唯一質因數分解不可能。

因此：

$$
\boxed{
\alpha\notin\mathbb Q.
}
$$

故對任何：

$$
k\ge1,
$$

$$
\alpha k
$$

不是整數。

---

# 13. Exact Contracting Count

length-$k$ parity words 共：

$$
2^k
$$

個。

恰含：

$$
u
$$

個 $U$ 的字數：

$$
\boxed{
\binom ku.
}
$$

contracting 條件：

$$
u<\alpha k.
$$

因 $\alpha k$ 非整數，

等價：

$$
u\le\lfloor\alpha k\rfloor.
$$

所以：

## Theorem 13.1 — Binomial Cylinder Count

$$
\boxed{
A_k
=
\sum_{u=0}^{\lfloor\alpha k\rfloor}
\binom ku.
}
$$

---

# 14. 為什麼這同時是 Residue Cylinder Count？

Paper 03 已證：

$$
\boxed{
\{D,U\}^k
\longleftrightarrow
\mathbb Z/2^k\mathbb Z.
}
$$

所以每一個 parity word 恰對應一個 modulo $2^k$ cylinder。

因此：

$$
A_k
$$

不只是 contracting words 數量，

也是：

$$
\boxed{
\text{contracting residue cylinders modulo }2^k
}
$$

的 exact 數量。

---

# 15. Cylinder-Class Proportion

定義：

$$
\boxed{
P_k
=
\frac{A_k}{2^k}.
}
$$

所以：

$$
\boxed{
P_k
=
\frac1{2^k}
\sum_{u=0}^{\lfloor\alpha k\rfloor}
\binom ku.
}
$$

稱為 **Binomial Cylinder Law**。

---

# 16. $k=8$

$$
8\alpha
\approx5.047.
$$

所以：

$$
u\le5.
$$

$$
A_8
=
\sum_{u=0}^5\binom8u
=
219.
$$

因此：

$$
\boxed{
P_8
=
\frac{219}{256}
=
85.546875\%.
}
$$

---

# 17. $k=12$

$$
12\alpha
\approx7.571.
$$

所以：

$$
u\le7.
$$

$$
A_{12}=3302.
$$

所以：

$$
\boxed{
P_{12}
=
\frac{3302}{4096}
=
80.615234375\%.
}
$$

這比 $k=8$ 低。

因此：

$$
\boxed{
P_k
\text{ 對有限 }k\text{ 不必單調。}
}
$$

原因是 floor threshold 的離散跳躍。

---

# 18. $k=16$：$89.4943\%$ 的來源

$$
16\alpha
\approx10.094876.
$$

所以：

$$
u\le10.
$$

因此：

$$
A_{16}
=
\sum_{u=0}^{10}\binom{16}{u}.
$$

直接算：

$$
\boxed{
A_{16}=58651.
}
$$

故：

$$
\boxed{
P_{16}
=
\frac{58651}{65536}
=
0.8949432373046875.
}
$$

也就是：

$$
\boxed{
89.49432373046875\%.
}
$$

---

# 19. 這解釋了先前 benchmark，但不是完全同一個比例

先前 finite-verification prototype 在：

$$
1\le n<2^{20}
$$

使用：

$$
k=16
$$

得到：

$$
938413
$$

個 strict $16$-step descent certificates。

其比例：

$$
\boxed{
\frac{938413}{1048575}
\approx
89.4941229\%.
}
$$

它與：

$$
P_{16}
\approx89.4943237\%
$$

極接近，

但不是同一個數。

---

# 20. 差異一：$n=0$ 被排除

因：

$$
2^{20}=16\cdot2^{16},
$$

每個 modulo $2^{16}$ residue 在：

$$
0\le n<2^{20}
$$

中出現恰好 16 次。

如果把全部 contracting classes 都乘 16：

$$
58651\cdot16
=
938416.
$$

但 positive domain 排除：

$$
n=0.
$$

而 residue $0$ 本身是 contracting class。

所以先變成：

$$
938415.
$$

---

# 21. 差異二：$1,2$ 是 equality 而非 descent

如前所述：

$$
T^{16}(1)=1,
$$

$$
T^{16}(2)=2.
$$

所以還要扣除 2 個不是 strict descent 的 starting values：

$$
938415-2
=
\boxed{
938413.
}
$$

正好等於 benchmark 的 exact certificate count。

因此：

$$
\boxed{
\text{benchmark count}
=
\text{binomial class law}
+
\text{finite-domain boundary correction}.
}
$$

這是一個完整的理論—實驗對接。

---

# 22. $k=20$

$$
20\alpha
\approx12.6186.
$$

所以：

$$
u\le12.
$$

得到：

$$
A_{20}=910596.
$$

因此：

$$
\boxed{
P_{20}
=
\frac{910596}{1048576}
\approx86.8412\%.
}
$$

再次說明 finite-$k$ 比例有 staircase oscillation。

---

# 23. 大尺度趨勢

雖然：

$$
P_k
$$

有限時不單調，

其極限卻非常清楚。

令：

$$
X_k\sim\operatorname{Binomial}(k,1/2).
$$

則：

$$
\Pr(X_k=u)
=
\frac1{2^k}\binom ku.
$$

因此：

$$
\boxed{
P_k
=
\Pr(X_k<\alpha k).
}
$$

在整數化後等同前式。

---

# 24. 為什麼 $\alpha>1/2$？

$$
\alpha>\frac12
$$

等價：

$$
2\ln2>\ln3
$$

等價：

$$
\ln4>\ln3
$$

即：

$$
\boxed{
4>3.
}
$$

因此 binomial distribution 的平均 fraction：

$$
1/2
$$

位於 contraction threshold：

$$
\alpha
$$

左側。

---

# 25. Law of Large Numbers

由：

$$
\frac{X_k}{k}\to\frac12
$$

in probability，

以及：

$$
\frac12<\alpha,
$$

得到：

$$
\boxed{
\Pr\left(
\frac{X_k}{k}<\alpha
\right)\to1.
}
$$

所以：

## Theorem 25.1

$$
\boxed{
P_k\to1.
}
$$

即：

> length-$k$ parity cylinders 中，contracting-slope cylinders 的比例趨近 100%。

---

# 26. Large-Deviation Rate

更精確地，對：

$$
\alpha>\frac12,
$$

Chernoff bound 給：

$$
\Pr(X_k\ge\alpha k)
\le
\exp\left(
-kD\!\left(
\alpha\middle\|\frac12
\right)
\right).
$$

其中 binary relative entropy：

$$
\boxed{
D\!\left(
\alpha\middle\|\frac12
\right)
=
\alpha\ln(2\alpha)
+
(1-\alpha)\ln(2(1-\alpha)).
}
$$

對：

$$
\alpha=\frac{\ln2}{\ln3},
$$

數值約：

$$
\boxed{
D\approx0.0346882.
}
$$

所以 expanding-word fraction 具有 exponential upper bound。

---

# 27. 這不是一個隨機 Collatz 假設

這一點很重要。

本文並沒有假設：

> 真實 Collatz orbit 每一步像 independent fair coin。

我們只是對**全部 length-$k$ words 的有限集合**做均勻組合計數。

因 Paper 03 已證：

$$
\text{word}
\leftrightarrow
\text{residue class mod }2^k,
$$

所以：

$$
\frac{1}{2^k}\binom ku
$$

也是 residue-class 的 exact finite density。

因此：

$$
\boxed{
P_k
}
$$

是 deterministic combinatorial fact，

不是 stochastic orbit model。

---

# 28. 但從 Residue Density 到 Orbit Theorem 還有一道牆

雖然：

$$
P_k\to1,
$$

仍然可能存在極少數：

$$
1-P_k
$$

的 expanding cylinders。

一個特定 positive integer orbit 的後續 prefixes 是否：

- 反覆落入稀有 expanding cylinders；
- 或在 contracting cylinders 中停在 finite correction threshold 以下；

不是單靠 $P_k$ 能決定。

因此：

$$
\boxed{
\text{density of charts}
\neq
\text{itinerary theorem}.
}
$$

---

# 29. 與 Almost-All Results 的邏輯關係

Tao 的結果證明：

對任意：

$$
f(N)\to\infty,
$$

幾乎所有 $N$（logarithmic density）都有：

$$
\operatorname{Col}_{\min}(N)\le f(N).
$$

那是對 actual Collatz orbits 的深度 almost-all theorem。

本文的：

$$
P_k\to1
$$

只是 finite parity-cylinder combinatorics。

所以兩者不能混為同一結果。

本文的價值在於：

$$
\boxed{
\text{把 local affine slope distribution exact 化}.
}
$$

不是取代 Tao 的 global probabilistic/analytic machinery。

---

# 30. 與 Paradoxical Finite Prefix 的關係

近年的 parity-vector/stopping-time 研究會考察：

- odd-step proportion；
- finite prefix 的增長；
- slope 預測與實際 finite correction 的偏差；
- 所謂 paradoxical sequence behavior。

本文提供一個精確拆分：

$$
\boxed{
\text{slope effect}
=
\frac{3^u}{2^k},
}
$$

$$
\boxed{
\text{finite correction}
=
\frac{b_w}{2^k}.
}
$$

因此任何「主斜率預測下降，但 finite starting point 尚未下降」的情況，都可以定位為：

$$
\boxed{
b_w
\text{ 尚未被 }
(2^k-3^u)n
\text{ 壓過}.
}
$$

---

# 31. 字序如何影響 Threshold？

Paper 02 已證 fixed $(k,u)$：

$$
3^u-2^u
\le
b_w
\le
2^{k-u}(3^u-2^u).
$$

對 contracting：

$$
2^k>3^u,
$$

threshold：

$$
\theta_w
=
\left\lfloor
\frac{b_w}{2^k-3^u}
\right\rfloor+1.
$$

因此：

$$
b_w
$$

越大，

finite threshold 越高。

---

# 32. Order-Uniform Descent Threshold

用最壞：

$$
b_{\max}
=
2^{k-u}(3^u-2^u),
$$

定義：

$$
\boxed{
\Theta_{k,u}
=
\left\lfloor
\frac{
2^{k-u}(3^u-2^u)
}{
2^k-3^u
}
\right\rfloor
+1.
}
$$

只要：

$$
3^u<2^k,
$$

則對**所有** length-$k$、恰含 $u$ 個 $U$ 的 words：

$$
w,
$$

以及所有 admissible：

$$
n\ge\Theta_{k,u},
$$

都有：

$$
\boxed{
T^k(n)<n.
}
$$

---

# 33. 這把完整字壓成 $(k,u)$ Certificate

通常 exact threshold：

$$
\theta_w
$$

需要：

$$
b_w,
$$

所以需要完整 word-order data。

但若願意使用保守上界：

$$
\Theta_{k,u},
$$

則只需：

$$
\boxed{
(k,u)
}
$$

就能對整個 word family 給 universal finite threshold。

因此 operation translation 再次產生 information compression：

$$
\boxed{
w
\to
(k,u)
}
$$

但代價是 certificate 變保守。

---

# 34. Minimum Threshold Word

Paper 02：

$$
b_{\min}=3^u-2^u
$$

由：

$$
U^uD^{k-u}
$$

取得。

因此 fixed $(k,u)$ 最容易下降的排列是：

$$
\boxed{
U^uD^{k-u}.
}
$$

最晚開始 guaranteed descent 的排列則是：

$$
\boxed{
D^{k-u}U^u.
}
$$

所以 branch order 不改變 contraction side，

只改變 finite threshold 的位置。

---

# 35. Example：$UUDD$

$$
k=4,
\qquad
u=2.
$$

$$
3^u=9,
\qquad
2^k=16.
$$

所以 contracting。

Paper 02：

$$
b=5.
$$

因此：

$$
\theta_w
=
\left\lfloor
\frac5{7}
\right\rfloor+1
=
1.
$$

所以所有 positive admissible：

$$
n
$$

都：

$$
T^4(n)<n.
$$

例如 source cylinder：

$$
n=3+16a
$$

有：

$$
T^4(n)=2+9a<n.
$$

---

# 36. Example：$UUU$

$$
k=3,
\qquad
u=3.
$$

$$
3^3=27>8=2^3.
$$

所以 uniform expanding。

Paper 02：

$$
b=19.
$$

因此：

$$
T^3(n)
=
\frac{27n+19}{8}
>
n
$$

對其所有 positive admissible：

$$
n\equiv7\pmod8
$$

成立。

例如：

$$
7\to11\to17\to26.
$$

所以：

$$
26>7.
$$

---

# 37. Local Expansion 不代表 Global Escape

上例：

$$
7\to11\to17\to26
$$

三步上升。

但繼續：

$$
26\to13\to20\to10\to5\to\cdots
$$

仍回落。

所以：

$$
\boxed{
\text{expanding finite word}
\not\Rightarrow
\text{divergent infinite orbit}.
}
$$

這再次說明：

$$
\boxed{
\text{local chart classification}
\neq
\text{global itinerary classification}.
}
$$

---

# 38. Finite Cylinder Law 與舊負漂移直覺

舊研究用平均語言說：

> 約每個 odd step 伴隨足夠多的除 2，所以 $2$ 最終壓過 $3$。

本文改寫為完全有限且 exact 的命題：

$$
\boxed{
u/k<\ln2/\ln3
}
$$

時，fixed word 的 multiplicative skeleton 必然 contracting。

這不需要：

- 50/50 parity 假設；
- independence；
- random-walk 模型；
- expectation。

因此舊 heuristic 的局部核心已完成 exact 化。

---

# 39. 但全域 heuristic 的缺口仍保留

從：

$$
P_k\to1
$$

不能推出：

$$
\forall n,\exists k:
T^k(n)<n.
$$

因為後者把：

$$
k
$$

與：

$$
n
$$

沿 actual itinerary 關聯起來。

真正需要排除的是：

> 是否存在某個 positive integer，其每個 candidate descent prefix 都被稀有 itinerary structure 或 finite correction 阻擋？

這仍然是全域問題。

---

# 40. Paper 05 的核心邊界圖

對 nonempty word：

### Contracting-slope side

$$
\boxed{
u/k<\alpha.
}
$$

存在 finite strict-descent threshold。

### Expanding side

$$
\boxed{
u/k>\alpha.
}
$$

全 positive cylinder 在該 block 上 strictly expands。

### Neutral slope

$$
\boxed{
\varnothing.
}
$$

因：

$$
\alpha
$$

無理。

### Block equality

只能在 contracting side 的單一有限值：

$$
\boxed{
n=b_w/(2^k-3^u)
}
$$

若其為 admissible integer。

---

# 41. 與 Finite Verification 的直接銜接

對一張 contracting cylinder，

一旦：

$$
n\ge\theta_w,
$$

可直接輸出 certificate：

$$
\boxed{
T^k(n)<n.
}
$$

若採 strong induction finite verification：

所有小於 $n$ 的 starting values 已被 certified，

那麼：

$$
T^k(n)<n
$$

立即完成 $n$ 的 path-merge certificate。

所以 Paper 05 的數學正是先前 benchmark pruning 的理論基礎。

---

# 42. 本文沒有證明什麼？

本文沒有證明：

$$
\forall n,\exists k:T^k(n)<n.
$$

沒有證明：

$$
P_k\to1
$$

可排除所有 exceptional integer itineraries。

沒有證明所有 contracting words 對其最小 positive representative 都立即下降。

沒有排除非平凡周期。

本文只建立 finite-word contraction / expansion 的 exact classification 與 combinatorial density。

---

# 43. 主要定理總結

## Theorem A — Exact Descent Criterion

$$
\boxed{
T^k(n)<n
\iff
b_w<(2^k-3^u)n.
}
$$

## Theorem B — Contracting Threshold

若：

$$
3^u<2^k,
$$

則：

$$
\boxed{
n\ge\theta_w
\Rightarrow
T^k(n)<n.
}
$$

## Theorem C — Uniform Expansion

若：

$$
3^u>2^k,
$$

則：

$$
\boxed{
T^k(n)>n
}
$$

對全部 positive admissible $n$。

## Theorem D — Binomial Cylinder Law

$$
\boxed{
A_k
=
\sum_{u=0}^{\lfloor\alpha k\rfloor}
\binom ku,
\qquad
\alpha=\frac{\ln2}{\ln3}.
}
$$

## Theorem E — Cylinder Density

$$
\boxed{
P_k=\frac{A_k}{2^k}\to1.
}
$$

## Theorem F — Order-Uniform Threshold

$$
\boxed{
\Theta_{k,u}
=
\left\lfloor
\frac{
2^{k-u}(3^u-2^u)
}{
2^k-3^u
}
\right\rfloor+1.
}
$$

---

# 44. 結論

Paper 02 把 finite parity word 壓縮成 exact affine operator。

Paper 03 將其合法域識別為 unique residue cylinder。

Paper 04 建立 source/target 的雙向 exact transport。

本文則完成第四步：

$$
\boxed{
\text{each finite chart has an exact drift sign and, when contracting, an exact finite threshold}.
}
$$

其最核心的分工是：

$$
\boxed{
(k,u)
\text{ decides which side of the contraction boundary the word lies on},
}
$$

而：

$$
\boxed{
b_w
\text{ decides the finite correction threshold}.
}
$$

因此：

$$
\boxed{
\text{counts determine asymptotic direction;}
}
$$

$$
\boxed{
\text{order determines finite delay}.
}
$$

進一步，由 finite word–residue bijection：

$$
\boxed{
P_k
=
2^{-k}
\sum_{u\le\lfloor\alpha k\rfloor}
\binom ku
}
$$

精確描述 contracting cylinder fraction。

對 $k=16$：

$$
\boxed{
58651/65536
=
89.4943237\%.
}
$$

而先前 finite benchmark 的：

$$
938413/1048575
\approx89.4941229\%
$$

則是此 class law 經 positive-domain 與 strict-descent boundary correction 後的結果。

這使先前計算觀察第一次得到完整純數學解釋。

但：

$$
\boxed{
P_k\to1
}
$$

仍然只說明 finite chart space 中 expanding regions 的組合比例趨零。

Collatz conjecture 要求的是：

$$
\boxed{
\text{every actual positive-integer itinerary eventually acquires a descent certificate}.
}
$$

這是更強的全稱 itinerary 命題。

下一篇將把舊研究中的「平均除以 2 深度」改寫成精確 valuation language，使用 accelerated odd map 與：

$$
\kappa_i=v_2(3n_i+1)
$$

將 parity word 壓縮成 valuation word，並重新整理 $M_j=(4^j-1)/3$、inverse fibers 與 exact log drift。

---

# 參考文獻

1. Olivier Rozier, Claude Terracol, *Paradoxical behavior in Collatz sequences*, arXiv:2502.00948.
2. Tong Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, arXiv:2605.13886.
3. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum of Mathematics, Pi 10 (2022), arXiv:1909.03562.
4. Collatz Operation Translation Series — Paper 02, *Collatz Local Affine Atlas：有限奇偶字的精確仿射化*.
5. Collatz Operation Translation Series — Paper 03, *Parity Word、Residue Cylinder 與局部 Identity 化*.
6. Collatz Operation Translation Series — Paper 04, *雙向殘餘類轉譯：$2^k$ Cylinder 與 $3^u$ Progression*.

---

## 下一篇

**Paper 06 —《Valuation Language 與 Accelerated Collatz：從奇偶字到 $v_2$ 字》**

核心任務：

1. 定義 accelerated odd map；
2. 將 parity runs 無損壓縮為 valuation word
   $$
   (\kappa_1,\ldots,\kappa_m);
   $$
3. 推導
   $$
   S^m(n)=\frac{3^mn+B_\kappa}{2^{K}},
   \qquad
   K=\sum_i\kappa_i;
   $$
4. 建立 exact log drift
   $$
   m\ln3-K\ln2+C_\kappa(n);
   $$
5. 將舊「2 的指數戰勝 3」heuristic 校正成 finite exact statement；
6. 重新統一 terminal inverse fibers 與 $M_j=(4^j-1)/3$。
