# 11 — 重建 Claude 的 $1.04/1.26/1.70$ Support Ladder
## Generalized One-Delta Extremal Operator 與 $99\%$ 的第一個數值答案

**日期：** 2026-08-11  
**狀態：** 數學結構重建 + 數值 operator solve  
**重要區分：**
- Claude 論文明確寫出的 rough thresholds：$70\%\to1.04$、$80\%\to1.26$、$90\%\to1.70$。
- 本文件給出的更精細數值，以及 $95\%,99\%$，是我們依同一 one-delta extremal structure 做的數值重建／延伸，不是 Claude 論文明列的新定理。

---

# 0. 我們找到 $1.04/1.26/1.70$ 的生成機制

Claude Remark 1.1 寫：

$$
70\%\leadsto\sigma\approx1.04,
$$

$$
80\%\leadsto\sigma\approx1.26,
$$

$$
90\%\leadsto\sigma\approx1.70.
$$

前面只知道這三個數字是「roughly」。

現在可以重建它們來自什麼 extremal problem。

Claude §7.1 在 $\sigma=1$ 使用 Montgomery–Taylor / CCLM one-delta extremal：

$$
\min_R
M(R),
$$

其中：

$$
M(R)
=
\int_{\mathbb R}
R(x)
\left[
1-
\left(
\frac{\sin\pi x}{\pi x}
\right)^2
\right]dx,
$$

限制：

$$
R\ge0,
\qquad
R(0)\ge1,
\qquad
\operatorname{supp}\widehat R\subset[-1,1].
$$

CCLM 的 Corollary 14 給 $\sigma=1$ 的精確極值：

$$
M_{\min}(1)
=
0.3274992\ldots,
$$

所以 simple-zero certificate：

$$
q(1)
=
1-M_{\min}(1)
=
0.6725007\ldots.
$$

這就是 Montgomery–Taylor / Claude Theorem D 的 $67.25\%$。

---

# 1. 把 support 改成一般 $\sigma$

考慮：

$$
\operatorname{supp}\widehat R
\subset[-\sigma,\sigma].
$$

因為：

$$
R=|S|^2,
$$

可取 $\widehat S=f$ 支持在：

$$
I_\sigma
=
[-\sigma/2,\sigma/2].
$$

constraint：

$$
S(0)=1
$$

變成：

$$
\int_{I_\sigma}f(t)\,dt=1.
$$

又因 Fourier transform identity：

$$
\mathcal F
\left[
\left(
\frac{\sin\pi x}{\pi x}
\right)^2
\right](\xi)
=
(1-|\xi|)_+,
$$

Plancherel 給：

$$
M(R)
=
\langle f,A_\sigma f\rangle,
$$

其中：

$$
A_\sigma
=
I-T_\sigma,
$$

$$
(T_\sigma f)(t)
=
\int_{I_\sigma}
(1-|t-u|)_+
f(u)\,du.
$$

因此 generalized one-delta problem 是一個 quadratic minimisation：

$$
m(\sigma)
=
\min_{\int f=1}
\langle f,A_\sigma f\rangle.
$$

Lagrange multiplier / reproducing-kernel argument給：

$$
\boxed{
m(\sigma)
=
\frac{1}{
\langle
\mathbf 1,
A_\sigma^{-1}\mathbf1
\rangle
}.
}
$$

故同一 integrality certificate 的 simple proportion 是：

$$
\boxed{
q(\sigma)
=
1-m(\sigma)
=
1-
\frac{1}{
\langle
\mathbf1,
A_\sigma^{-1}\mathbf1
\rangle
}.
}
$$

這就是我們要找的 support ladder。

---

# 2. 為什麼 $\sigma\le1$ 有 Claude 的 cosine closed form？

若：

$$
\sigma\le1,
$$

則對 $t,u\in I_\sigma$ 永遠：

$$
|t-u|\le1.
$$

所以 kernel 不會被截斷：

$$
(1-|t-u|)_+
=
1-|t-u|.
$$

Euler equation 可降成二階 ODE；在 rescaled variable 上正是 Claude §7.1：

$$
v_\sigma^*(s)
=
\cos(\sqrt2\,\sigma s).
$$

因此 Claude 的：

$$
c_\sigma^*
=
\frac{
\sqrt2\tan(\sigma/\sqrt2)
}{
1+(\sigma/\sqrt2)\tan(\sigma/\sqrt2)
}
$$

與 operator formula 在 $\sigma\le1$ 完全一致。

---

# 3. 為什麼不能把這個 cosine 公式硬外推到 $\sigma>1$？

這正是我們前面第一次算 $90\%$ 時發現的坑。

當：

$$
\sigma>1,
$$

interval $I_\sigma$ 中開始存在：

$$
|t-u|>1.
$$

此時真正 kernel 是：

$$
\boxed{
(1-|t-u|)_+,
}
$$

不是：

$$
1-|t-u|.
$$

所以 operator 的結構發生變化。

若把 $\sigma\le1$ 的 cosine formula 盲目延伸，$70\%,80\%$ 附近誤差尚小，但到 $90\%$ 會嚴重錯誤。

真正的 support-extremal problem必須解 truncated triangular-kernel Fredholm equation。

這解釋了：

> 為什麼 paper 的 $90\%$ 是約 $1.70$，而不是把 §7.1 的 closed form 直接解下去所得的更大數字。

---

# 4. Numerical reconstruction

我們用 midpoint Nyström / sparse linear solve 計算：

$$
A_\sigma^{-1}\mathbf1
$$

再 root-find：

$$
q(\sigma)=q_{\rm target}.
$$

較高解析度的結果：

| target | $\sigma$ |
|---:|---:|
| $70\%$ | $\approx1.04263$ |
| $80\%$ | $\approx1.25785$ |
| $90\%$ | $\approx1.70146$ |
| $95\%$ | $\approx2.26079$ |
| $99\%$ | $\approx4.1872$ |

前三個與 Claude 的 rough：

$$
1.04,\quad1.26,\quad1.70
$$

幾乎逐一吻合。

因此我們可以很有把握地說：

$$
\boxed{
\text{Remark 1.1 的 support numbers 正是 generalized one-delta extremal ladder。}
}
$$

這是「數值重建機制」，不是從作者補充資料取得的明示公式。

---

# 5. $99\%$：第一個可回答的數字

Claude 論文沒有列：

$$
\sigma_{99}.
$$

我們現在沿同一 generalized one-delta operator 做數值延伸。

midpoint discretisation：

$$
n=1000:
\quad
\sigma_{99}\approx4.18714349,
$$

$$
n=1500:
\quad
\sigma_{99}\approx4.18719630,
$$

$$
n=2000:
\quad
\sigma_{99}\approx4.18721495.
$$

若假定主要離散誤差是 $O(h^2)$，簡單 Richardson heuristic 給：

$$
\sigma_{99}
\approx
4.18724.
$$

所以目前最適合的研究寫法是：

$$
\boxed{
\sigma_{99}
\approx4.19
\quad
\text{(numerical, same one-delta route)}.
}
$$

不要寫成精確 theorem constant。

---

# 6. 這個結果如何回答我們原來的「比例主義」？

現在 CPL ladder 可以改寫成：

$$
67.25\%
\leftrightarrow
\sigma=1,
$$

$$
70\%
\leftrightarrow
\sigma\approx1.043,
$$

$$
80\%
\leftrightarrow
\sigma\approx1.258,
$$

$$
90\%
\leftrightarrow
\sigma\approx1.701,
$$

$$
95\%
\leftrightarrow
\sigma\approx2.261,
$$

$$
99\%
\leftrightarrow
\sigma\approx4.19.
$$

這是一條真正的：

$$
\boxed{
\text{Proportion}
\longleftrightarrow
\text{Information Bandwidth}
}
$$

映射。

因此比例不再是「RH 完成度」，而是：

> 在此 one-delta / pair-correlation certificate class 裡，若 arithmetic side 能合法提供到 support $\sigma$，最多能把 simple-critical proportion certificate 推到哪裡？

---

# 7. 重要：這不是無條件結果

目前真正無條件可用的 arithmetic input 邊界仍是：

$$
\sigma\le1.
$$

Claude §7.5 明確說，超過 $1$ 時 prime-side off-diagonal sums 需要 Hardy–Littlewood-strength prime-pair information，等價地進入 Montgomery PCC 的 $\alpha>1$ 區域。

所以：

$$
\sigma_{70}\approx1.043
$$

不等於「只差 $4.3\%$ 算力」。

它代表：

$$
\boxed{
\text{必須跨過目前 arithmetic information 的結構邊界。}
}
$$

---

# 8. 與我們 Boundary-Spike toy 的關係

前面 toy model發現：

$$
\text{open band}
\quad
\Rightarrow
\quad
\text{adversarial boundary spike}.
$$

現在 generalized one-delta operator 給出真正 continuous support 版本：

$$
\sigma=1
\rightarrow
\sigma>1.
$$

兩者結構一致：

$$
\boxed{
\text{增加可觀測頻帶}
\Rightarrow
\text{縮小 adversarial configuration class}
\Rightarrow
q(\sigma)\uparrow.
}
$$

toy 的單一 $S(4)$ 是一個離散 probe；

Fredholm operator 才是接回真 pair-correlation support 的 continuum model。

---

# 9. 下一個問題

現在真正值得攻的已經不是「$99\%$ 到底要多少 support」。

那個數值問題我們已有第一答案：

$$
\sigma_{99}\approx4.19.
$$

更重要的是：

## Support Realizability Problem

Claude 的 arithmetic side目前只能嚴格做到：

$$
\sigma\le1.
$$

所以對每個 target：

$$
q\in\{0.70,0.80,0.90,0.99\},
$$

應拆成：

$$
\boxed{
\text{Extremal requirement }\sigma_q
}
$$

與：

$$
\boxed{
\text{Arithmetic realizability of }\sigma_q
}
$$

兩個完全不同的 proof obligations。

第一個現在已可數值重建。

第二個才是真正的數論牆。
