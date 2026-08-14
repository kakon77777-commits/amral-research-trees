# 13 — Test-Specific Weighted Pair-Correlation Hypothesis
## $P_{70}$ 不需要完整 Hardy–Littlewood：只需要一個高槓桿 weighted moment

**日期：** 2026-08-11  
**狀態：** source-grounded derivation + new conditional schema  
**重要區分：**
- Claude Proposition 5.6 的 $O_1$ 公式、$\sigma>1$ 需要 prime-pair 資訊，是來源直接支持。
- Goldston 的強 Hardy–Littlewood假設與 SPC 關係，是經典來源直接支持。
- 本文的 `WSPC / WPPH` 定義與「只需一個 weighted moment」是本研究從這些公式抽出的**較弱 sufficient hypothesis schema**，不是來源原有命名或定理。

---

# 0. 為什麼「完整 Hardy–Littlewood」明顯太強？

Claude §7.5 說：

$$
\sigma>1
$$

時，Proposition 5.6 的 off-diagonal：

$$
O_1
$$

不再由 diagonal 控制，需要 Hardy–Littlewood-strength prime-pair資訊，等價地需要 Montgomery pair correlation 在：

$$
\alpha>1
$$

的資訊。

Goldston 的經典筆記中，Montgomery 所用的強 prime-pair 假設是：

$$
\sum_{n\le N}
\Lambda(n)\Lambda(n+h)
=
\mathfrak S(h)N
+
O_\varepsilon(N^{1/2+\varepsilon})
$$

uniformly：

$$
0<h\le N.
$$

這非常強：它要求**每一個 shift** 都有平方根級 error。

但我們要證：

$$
P_{70},
$$

並不需要知道所有 test functions，也不需要知道所有 shift。

---

# 1. Goldston 的公式已經暗示「一個 test = 一個 weighted moment」

Pair-correlation formula 的一般形式是：

$$
\sum_{\gamma,\gamma'}
R\!\left(
(\gamma-\gamma')
\frac{\log T}{2\pi}
\right)
w(\gamma-\gamma')
$$

對應 Fourier side：

$$
\int
\widehat R(\alpha)
F(\alpha,T)
\,d\alpha.
$$

因此，如果我們只準備使用**一個指定的 extremal test**：

$$
R_\sigma^\star,
$$

那麼要跑這個 certificate，真正需要的新 zero-pair input 只是：

$$
\boxed{
\int_{1<|\alpha|\le\sigma}
\widehat R_\sigma^\star(\alpha)
F(\alpha,T)
\,d\alpha
}
$$

的正確 asymptotic。

不需要先證：

$$
F(\alpha,T)=1+o(1)
$$

對每一個：

$$
1<\alpha\le\sigma
$$

逐點／uniformly成立。

---

# 2. 定義 WSPC — Weighted Strong Pair Correlation

令：

$$
R_\sigma^\star
$$

是 v8 重建的 generalized one-delta optimizer，normalize：

$$
R_\sigma^\star(0)=1,
$$

且：

$$
\operatorname{supp}\widehat R_\sigma^\star
\subset[-\sigma,\sigma].
$$

定義：

## WSPC$(\sigma)$

$$
\boxed{
\mathcal J_\sigma(T)
:=
\int_{1<|\alpha|\le\sigma}
\widehat R_\sigma^\star(\alpha)
\left[
F(\alpha,T)-1
\right]d\alpha
=
o(1).
}
$$

這是 **one-test weighted SPC**。

完整 SPC：

$$
F(\alpha,T)=1+o(1)
$$

uniformly on the interval，顯然會推出 WSPC。

但 WSPC 只限制一個線性泛函。

因此在資訊結構上：

$$
\boxed{
\mathrm{WSPC}(\sigma)
\ll
\mathrm{SPC}[1,\sigma].
}
$$

這裡的 $\ll$ 表示「要求的資訊維度遠低」，不是 Vinogradov notation。

---

# 3. 為什麼這一個 weighted moment 就夠？

對 optimizer，pair-correlation second-moment constant 可拆成：

$$
C_\sigma
=
\widehat R_\sigma^\star(0)
+
\int_{|\alpha|\le1}
|\alpha|
\widehat R_\sigma^\star(\alpha)\,d\alpha
+
\int_{1<|\alpha|\le\sigma}
\widehat R_\sigma^\star(\alpha)\,d\alpha.
$$

模型值滿足：

$$
C_\sigma
=
2-q(\sigma).
$$

如果未知 strip 的真實 $F$ 不是 $1$，修正量就是：

$$
\mathcal J_\sigma(T).
$$

所以 second-moment constant 變成：

$$
C_\sigma+\mathcal J_\sigma(T)+o(1).
$$

Claude 的同一 integrality / rank-trace mechanism 會把 proportion 改成：

$$
q(\sigma)-\mathcal J_\sigma(T)+o(1)
$$

（對正向 error 而言；若 $\mathcal J$ 為負則反而有利）。

因此：

$$
\boxed{
\mathcal J_\sigma(T)=o(1)
}
$$

就是跑同一 optimal certificate 的自然 test-specific 條件。

**此段是本研究的 conditional reconstruction；要把它正式升成 Claude paper 風格 theorem，仍需把 generalized-support prime-side trace 與其 localization errors完整寫出。**

---

# 4. $P_{70}$ 驚人的地方：未知 strip 的 test mass 其實極少

我們數值重建：

$$
\sigma_{70}
\approx
1.042628.
$$

對相應 optimizer：

$$
\int_{1<|\alpha|\le\sigma}
\widehat R_\sigma^\star(\alpha)\,d\alpha
\approx
0.00114.
$$

也就是整個 normalize Fourier mass 的：

$$
\boxed{
\approx0.114\%.
}
$$

因此 $P_{70}$ 從資訊量角度非常特殊：

- support 確實必須跨過 $1$；
- 但 optimal test 真正使用 unknown strip 的總 Fourier mass只有約千分之一。

這強化了一個重要觀察：

$$
\boxed{
\text{困難來自「跨界」，不是來自「需要大量新 band」。}
}
$$

---

# 5. 隨比例提高，unknown-band dependence 很快增加

同一數值診斷：

| target | $\sigma$ | optimizer Fourier mass in $|\alpha|>1$ |
|---:|---:|---:|
| $70\%$ | $1.04263$ | $\approx0.114\%$ |
| $80\%$ | $1.25785$ | $\approx2.89\%$ |
| $90\%$ | $1.70146$ | $\approx12.36\%$ |
| $95\%$ | $2.26079$ | $\approx24.32\%$ |
| $99\%$ | $4.18722$ | $\approx51.07\%$ |

所以：

$$
P_{70}
$$

與：

$$
P_{99}
$$

不是「同一件事多做幾次」。

到 $99\%$，optimal certificate 約一半的 Fourier mass 已依賴：

$$
|\alpha|>1
$$

的未知 pair-correlation區域。

---

# 6. 實用版本：不用正好卡在 $\sigma_{70}$

若正好取：

$$
\sigma=1.042628,
$$

model certificate 幾乎剛好：

$$
q=0.70.
$$

因此沒有 error slack。

更實用的是稍微多買一點 support。

例如：

## $\sigma=1.05$

數值：

$$
q(1.05)
\approx
0.70443.
$$

所以只要 weighted unknown-strip error滿足：

$$
\boxed{
|\mathcal J_{1.05}(T)|
\le
0.0044+o(1),
}
$$

就仍足以推出：

$$
P_{70}.
$$

而此時 unknown-strip Fourier mass也只有約：

$$
0.154\%.
$$

## $\sigma=1.06$

$$
q(1.06)
\approx
0.71031.
$$

允許：

$$
|\mathcal J_{1.06}(T)|
\lesssim
0.0103,
$$

而 unknown-strip mass約：

$$
0.217\%.
$$

所以會出現一個很自然的 tradeoff：

$$
\boxed{
\text{多擴一點 support}
\leftrightarrow
\text{降低 arithmetic accuracy requirement}.
}
$$

這可以視為 CPL 的第一條 **support–accuracy frontier**。

---

# 7. Prime side 的完全對應：WPPH

Claude Proposition 5.6 給 exact：

$$
O_1
=
\frac{1}{2\pi^2}
\Re
\sum_{n\ne m}
\frac{a_na_m}{i(\log n-\log m)}
\left[
\left(\frac nm\right)^{2iT}
(\alpha_m^++\alpha_n^-)
-
\left(\frac nm\right)^{iT}
(\alpha_n^++\alpha_m^-)
\right],
$$

其中：

$$
a_n
=
\frac{\Lambda(n)}{\sqrt n},
$$

$$
\alpha_n^+
=
\int_0^T
\Phi(x)^2n^{ix}\,dx,
$$

$$
\alpha_n^-
=
\int_{-T}^0
\Phi(x)^2n^{ix}\,dx.
$$

因此可以把：

$$
n=m+h
$$

分組，寫成：

$$
\boxed{
O_1
=
\sum_{h\ne0}
\sum_m
\Lambda(m)\Lambda(m+h)
K_{T,X,\Phi}(m,h),
}
$$

其中 $K$ 是由上面精確公式決定的 smooth / oscillatory weight，包含：

- $1/\sqrt{m(m+h)}$；
- $1/\log(1+h/m)$；
- endpoint oscillations；
- $\alpha_n^\pm$ window transforms。

---

# 8. 定義 WPPH — Weighted Prime-Pair Hypothesis

令：

$$
O_1^{HL}
$$

表示把：

$$
\Lambda(m)\Lambda(m+h)
$$

在上述**同一個 weight**中替換為 Hardy–Littlewood model：

$$
\mathfrak S(h)
$$

所得到的模型主項（連同適當的 local density / summation normalization）。

定義：

## WPPH$(\sigma,\Phi)$

$$
\boxed{
O_1(T,X,\Phi)
-
O_1^{HL}(T,X,\Phi)
=
o(TL^3),
\qquad
X=T^\sigma.
}
$$

這只要求 **Claude 實際使用的那一個 weighted double sum** 正確。

Pointwise Hardy–Littlewood with strong uniform error is一個 sufficient condition；

但 WPPH 允許：

- 不同 $h$ 的 errors 相互抵消；
- 不同 $m$ 區段抵消；
- 不要求每一個 shift都有 asymptotic；
- 不要求對任意 test weight都成立。

所以 WPPH 是我們目前能從 Claude $O_1$ 中抽出的更貼近實際 proof obligation 的假設。

---

# 9. $P_{70}$ 的 near-diagonal support

上一輪已推：

$$
X=T^\sigma,
$$

而 near-diagonal：

$$
h
\sim
\frac XT.
$$

對：

$$
\sigma=1.05,
$$

得到：

$$
h
\sim
T^{0.05}.
$$

在 prime scale：

$$
h
\sim
X^{1-1/1.05}
=
X^{0.047619\ldots}.
$$

因此 practical $P_{70}$ weighted prime-pair input主要聚焦在非常短的 relative shift scale。

但必須注意：

> exact $O_1$ weight仍有 oscillatory tails；「主要聚焦」不等於可以直接截斷所有較大 $h$ 而不證明 tail bound。

---

# 10. 與 Goldston 強 HL 的邏輯關係

Goldston 記錄的強 hypothesis要求：

$$
\forall h\le N:
\quad
\sum_{n\le N}
\Lambda(n)\Lambda(n+h)
=
\mathfrak S(h)N
+
O(N^{1/2+\varepsilon}).
$$

WPPH 則只要求：

$$
\sum_{h,m}
E(m,h)
K_{T,X,\Phi}(m,h)
=
o(TL^3),
$$

其中：

$$
E(m,h)
=
\Lambda(m)\Lambda(m+h)-\text{HL model}.
$$

所以可以把層級畫成：

$$
\boxed{
\text{Strong pointwise HL}
\Rightarrow
\text{full SPC (in its valid range)}
\Rightarrow
\text{WSPC for every chosen test}
}
$$

而在 Claude 的 prime-side formulation：

$$
\boxed{
\text{Strong HL}
\Rightarrow
\text{WPPH}
\Rightarrow
\text{test-specific trace evaluation}.
}
$$

反向都不能自動成立。

---

# 11. 新的 $P_{70}$ Conditional Target

我們現在不必把研究問題寫成：

> 證 Hardy–Littlewood。

可以改成：

## WPPH-$70$

選：

$$
\sigma=1.05
$$

及其 optimized one-delta window。

證明對 Claude Proposition 5.6 所產生的 exact weight：

$$
K_{T,T^{1.05},\Phi^\star_{1.05}}
$$

有：

$$
\boxed{
\left|
O_1-O_1^{model}
\right|
\le
(0.004+\!o(1))
\times
(\text{normalized second-moment scale}).
}
$$

一旦與 generalized trace normalization完整接合，這應已足以維持：

$$
q\ge0.70.
$$

這比「完整 HL」小得多，也比要求完整：

$$
F(\alpha)=1
$$

on $[1,1.05]$ 更接近真正 proof 使用的資訊。

---

# 12. 下一步

現在最值得做兩件事：

## A. Kernel extraction

把：

$$
K_{T,X,\Phi}(m,h)
$$

從 Proposition 5.6 進一步 simplify，找出其 leading near-diagonal kernel。

目標：

$$
K_{T,X,\Phi}(m,h)
\approx
W_\Phi(m/X,hT/X)
$$

或類似 rescaled form。

這會讓 WPPH 變成真正可和 average Hardy–Littlewood 文獻比較的式子。

## B. Existing theorem matching

搜尋現在已證的 average prime-pair / Selberg-integral / short-interval variance bounds，看看是否已有結果能控制：

$$
\sum_{h,m}E(m,h)K(m,h)
$$

到足以讓 $q>67.25\%$，即使還到不了 $70\%$。

若能無條件推過：

$$
68.185\%
$$

會比條件式 $70\%$ 更重要。
