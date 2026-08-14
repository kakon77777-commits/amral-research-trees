# 12 — Arithmetic Realizability Bridge
## 從 $\sigma=1$ 的無條件 Prime Side 到 $P_{70}/P_{80}/P_{90}/P_{95}/P_{99}$ 的算術需求

**日期：** 2026-08-11  
**狀態：** source-grounded reconstruction + derived conditional schema  
**核心問題：**

$$
\boxed{
\text{Extremal side 已知道需要多少 support；
Arithmetic side 到底要提供什麼，才能合法實現它？}
}
$$

---

# 0. 已知邊界：為什麼 Claude 卡在 $\sigma=1$？

Claude Proposition 5.6 對 prime polynomial

$$
P_X
$$

的 quadratic mean 分解為：

$$
\mathcal M[P_X,P_X]
=
D+O_1+O_2.
$$

其中 diagonal：

$$
D
\sim
\frac{TL^3}{6\pi},
$$

而目前用 Montgomery–Vaughan generalized Hilbert inequality 控制：

$$
\boxed{
O_1\ll L^2X.
}
$$

若：

$$
X=(T/2\pi)^\sigma,
$$

忽略固定常數後：

$$
\frac{|O_1|}{D}
\ll
\frac{X}{TL}
\asymp
\frac{T^{\sigma-1}}{\log T}.
$$

所以：

### $\sigma<1$

$$
\frac{|O_1|}{D}\to0.
$$

### $\sigma=1$

$$
\frac{|O_1|}{D}
\ll
\frac1{\log T}
\to0.
$$

### 任意固定 $\sigma>1$

$$
\frac{|O_1|}{D}
\gg
\frac{T^{\sigma-1}}{\log T},
$$

目前的絕對值控制失效。

這不是「proof technique 不夠漂亮」而已，而是 off-diagonal 必須開始被**計算**，不能只被**壓掉**。

---

# 1. Off-diagonal 真正探測哪種 prime-pair scale？

Claude 的 $O_1$ 含有：

$$
\frac{1}{\log n-\log m}
$$

以及：

$$
(n/m)^{iT}
$$

類 oscillation。

對：

$$
n\sim m\sim X,
$$

令：

$$
h=n-m.
$$

當：

$$
|h|\ll X
$$

時：

$$
\log(n/m)
=
\log\left(1+\frac{h}{m}\right)
\approx
\frac{h}{X}.
$$

時間區間長度為 $T$，所以 off-diagonal 無法充分 oscillatory-cancel 的近對角區大致滿足：

$$
T|\log(n/m)|
\lesssim1.
$$

也就是：

$$
\boxed{
|h|
\lesssim
\frac XT.
}
$$

若：

$$
X=T^\sigma,
$$

則：

$$
\boxed{
H_\sigma
\asymp
T^{\sigma-1}.
}
$$

以 prime scale $X$ 表示：

$$
T=X^{1/\sigma},
$$

所以：

$$
\boxed{
H_\sigma
\asymp
X^{1-1/\sigma}.
}
$$

**這一段是從 Claude Proposition 5.6 的 explicit $O_1$ formula 推出的 scale inference，不是 Claude 原文直接列出的公式。**

---

# 2. CPL 各比例對應的 prime-pair shift scale

由 v8 generalized one-delta reconstruction：

| target | $\sigma$ | $H_\sigma$ in $T$ scale | $H_\sigma$ in prime scale $X$ |
|---|---:|---:|---:|
| $70\%$ | $1.042628$ | $T^{0.042628}$ | $X^{0.040885}$ |
| $80\%$ | $1.257848$ | $T^{0.257848}$ | $X^{0.204991}$ |
| $90\%$ | $1.701455$ | $T^{0.701455}$ | $X^{0.412268}$ |
| $95\%$ | $2.260790$ | $T^{1.260790}$ | $X^{0.557677}$ |
| $99\%$ | $4.187215$ | $T^{3.187215}$ | $X^{0.761178}$ |

這裡的物理意義不是「要知道所有 $h$ 到這裡」。

而是：

> 當 Dirichlet polynomial 長到 $X=T^\sigma$ 時，近對角 pair interaction 自然落在這個 additive-shift 尺度；若沒有足夠平均或逐-shift prime-pair 資訊，$O_1$ 無法得到所需主項／消去。

---

# 3. 一個經典的強 Hardy–Littlewood 輸入

Goldston 的 pair-correlation 筆記記錄 Montgomery 使用的強 prime-pair 假設：

$$
\boxed{
\sum_{n\le N}
\Lambda(n)\Lambda(n+k)
=
\mathfrak S(k)N
+
O_\varepsilon(N^{1/2+\varepsilon}),
}
$$

uniformly：

$$
0<k\le N.
$$

其中：

$$
\mathfrak S(k)
$$

是 prime-pair singular series。

Goldston 並記錄：這個強誤差版本足以導出 Strong Pair Correlation：

$$
F(\alpha,T)
=
1+o(1)
$$

到：

$$
\boxed{
1\le\alpha\le2-\varepsilon.
}
$$

---

# 4. 第一個重要分界：$90\%$ 與 $95\%$

我們重建：

$$
\sigma_{70}\approx1.043<2,
$$

$$
\sigma_{80}\approx1.258<2,
$$

$$
\sigma_{90}\approx1.701<2.
$$

因此在**經典 Montgomery arithmetic heuristic / Goldston 整理的強 HL framework** 裡：

$$
\boxed{
P_{70},P_{80},P_{90}
}
$$

全部仍落在：

$$
\alpha<2
$$

這個強 prime-pair 假設可以供應的區間。

但是：

$$
\sigma_{95}\approx2.261>2,
$$

$$
\sigma_{99}\approx4.187>2.
$$

所以：

$$
\boxed{
P_{95},P_{99}
}
$$

已經跨出「平方根誤差的逐-shift Hardy–Littlewood pair conjecture 已知可推出 SPC」的標準區域。

這是一個比單純 $q=90\%\to95\%$ 更實質的**算術 regime change**。

---

# 5. 第二個 arithmetic input：prime variance / short intervals

Goldston–Montgomery 的經典 equivalence（在原始文獻中以 RH 為背景）把 Strong Pair Correlation 與 primes-in-short-intervals 的二次矩連結：

$$
\int_1^X
\left(
\psi(x+h)-\psi(x)-h
\right)^2dx
\sim
hX\log\frac Xh.
$$

Goldston 的筆記特別指出：

> 逐-shift twin-prime conjecture 的平方根誤差只直接給 SPC 到 $\alpha<2$；  
> 但這個較弱、平均化的 short-interval second-moment hypothesis 可以供應 SPC 的完整固定 support range。

所以對 $P_{95},P_{99}$，較自然的 arithmetic hypothesis 不是要求每一個 shift 都有極強 pointwise Hardy–Littlewood error，而是要求：

$$
\boxed{
\text{足夠廣尺度的 prime short-interval variance asymptotic}.
}
$$

---

# 6. 我們定義三層 Arithmetic Bridge Hypotheses

為避免把「需要 HL」說得過於模糊，CPL 暫時分三層。

## ABH-1 — Direct Prime-Side Trace Hypothesis

對指定 support $\sigma$ 與 optimized one-delta family，假設 Claude 的 prime-side trace evaluation 可延伸，使：

$$
\frac{
(\operatorname{tr}\widetilde G)^2
}{
N\operatorname{tr}(\widetilde G^2)
}
\to
c(\sigma),
$$

其中：

$$
c(\sigma)
=
\frac{1}{2-q(\sigma)}.
$$

這是**最貼近 Claude proof pipeline**的假設。

它避免預先指定哪一個 prime conjecture必須負責。

---

## ABH-2 — Partial Strong Pair Correlation

假設：

$$
F(\alpha,T)=1+o(1)
$$

uniformly：

$$
1\le|\alpha|\le\sigma.
$$

連同已知的 $|\alpha|\le1$ 區域，便提供 generalized one-delta certificate 所需的 full pair data 到 $\sigma$。

這是 zero/pair-statistics 語言。

---

## ABH-3 — Arithmetic Realization

使用 prime-side sufficient conditions，例如：

### 對 $\sigma<2$

強 Hardy–Littlewood prime-pair：

$$
\sum_{n\le N}\Lambda(n)\Lambda(n+h)
=
\mathfrak S(h)N+O(N^{1/2+\varepsilon})
$$

的經典 framework。

### 對更大固定 $\sigma$

採：

$$
\int
(\psi(x+h)-\psi(x)-h)^2dx
$$

型的 short-interval variance asymptotic，或直接假設 full SPC / PCC 所需 arithmetic input。

---

# 7. Derived Conditional Theorem Schema

下面是**本研究根據 Claude 的 linear-algebra pipeline + v8 one-delta operator 重建出的條件式 schema，不是來源論文逐字定理。**

若對某固定：

$$
\sigma>1
$$

能把 Claude Proposition 5.6 / Theorem 5.8 的 prime-side second-trace evaluation 合法延伸到 optimized support-$\sigma$ one-delta test family，並保持所有 localisation / taper errors：

$$
o(N(T,2T)),
$$

使相應 trace ratio為：

$$
c(\sigma)
=
\frac1{2-q(\sigma)},
$$

則同一 zero-side inertia + rank–trace mechanism 應給：

$$
\boxed{
\liminf_{T\to\infty}
\frac{
N_0^s(T,2T)
}{
N(T,2T)
}
\ge
q(\sigma).
}
$$

所以：

### 若 arithmetic side 可實現 $\sigma=1.04263$

$$
P_{70}
$$

進入 conditional closure。

### 若可實現 $\sigma=1.25785$

$$
P_{80}.
$$

### 若可實現 $\sigma=1.70146$

$$
P_{90}.
$$

這把問題拆得非常乾淨：

$$
\boxed{
\text{比例門檻}
\rightarrow
\text{extremal support}
\rightarrow
\text{arithmetic realization}.
}
$$

---

# 8. $P_{70}$ 的最小算術問題現在可以怎麼問？

不再問：

> 「能不能證 $70\%$？」

而是問：

$$
\boxed{
\text{能不能把 prime-side second trace
從 }X\le T
\text{ 推到 }
X\le T^{1.04263}
\text{？}
}
$$

換成 additive shift：

$$
\boxed{
h
\lesssim
T^{0.04263}.
}
$$

或 prime scale：

$$
\boxed{
h
\lesssim
X^{0.04089}.
}
$$

這個尺度很小。

但真正的困難不是 exponent 小，而是：

$$
\boxed{
\text{它已經跨出 diagonal-only mean-value regime。}
}
$$

因此哪怕只從：

$$
1
\to
1.0001
$$

也已經是一個質變。

---

# 9. 一個值得注意的歷史對照

Goldston 筆記說，Montgomery 的 strong Hardy–Littlewood hypothesis 允許把 program 做到：

$$
x\le T\le x^{2-\varepsilon},
$$

也就是：

$$
\alpha<2.
$$

所以從歷史角度看：

$$
P_{90}
$$

所需的：

$$
\sigma\approx1.70
$$

仍然落在 Montgomery 當年 prime-pair heuristic 本來就預期可以處理的範圍內。

真正開始要求新的 arithmetic regime 的第一個 CPL 節點，反而是：

$$
\boxed{
P_{95}
}
$$

因為：

$$
\sigma_{95}\approx2.26.
$$

這一點在「比例 ladder」裡非常不直觀，但在「support ladder」裡一眼可見。

---

# 10. 下一輪最值得做什麼？

現在有三條。

## Route A — $P_{70}$ Weighted Prime-Pair Hypothesis

從 Claude Proposition 5.6 的實際：

$$
O_1
$$

公式出發，不假設完整 Hardy–Littlewood，而只抽取**足夠讓 optimized $\sigma=1.04263$ test 成立的 weighted prime-pair asymptotic**。

這可能比標準 pointwise HL 弱很多。

## Route B — Average-$h$ Hypothesis

因為 $O_1$ 本身對 $n,m$ 有 smooth weights，也許不需要：

$$
\forall h
$$

的 prime-pair asymptotic。

可研究：

$$
\sum_h W(h/H)
\left[
\sum_n\Lambda(n)\Lambda(n+h)-\mathfrak S(h)X
\right]
$$

只需：

$$
o(\text{main}).
$$

這會更接近現代「average Hardy–Littlewood」或 short-interval variance。

## Route C — Unconditional partial escape

搜尋是否存在目前已證、雖不足以得到：

$$
F(\alpha)\sim1
$$

但能對：

$$
1<\alpha<1+\delta
$$

提供 one-sided bound 的結果，並測試能否把 $67.25\%$ 往上推一點。

這可能不會到 $70\%$，但若能無條件突破：

$$
68.185\%
$$

那會是完全不同層級的結果。

---

# 11. 本輪結論

我們已經從：

$$
\text{「$\sigma>1$ 需要 prime pairs」}
$$

推進成：

$$
\boxed{
\text{Target proportion}
\rightarrow
\sigma_q
\rightarrow
X=T^{\sigma_q}
\rightarrow
h\sim X/T
\rightarrow
\text{需要的 arithmetic correlation scale}.
}
$$

這使 $P_{70}$ 的真正 QCI 變得可以操作：

$$
\boxed{
X:T\to T^{1.04263}
}
$$

就是第一道牆。
