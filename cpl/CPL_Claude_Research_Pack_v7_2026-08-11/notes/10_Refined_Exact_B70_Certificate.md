# 10 — Refined Exact $B_{70}$ Certificate
## 將 safety margin 壓到 $8.0\times10^{-8}$ 後仍可 exact-certify

**日期：** 2026-08-11  
**作用域：** $N=4$ continuous-position toy marked-configuration model  
**狀態：** exact-rational finite certificate；非 Riemann zeta theorem

---

# 0. 新結果

前一版為了容易做 exact positivity，將 numerical dual 的 $c_0$ 下調：

$$
5\times10^{-5}.
$$

那給出：

$$
B_{70}^{cert}
=
3.667777612662112\ldots.
$$

本輪持續縮小 rationalization safety margin。

最終使用：

$$
\boxed{
\delta
=
\frac{25024291}{312500000000000}
=
8.00777312e-08
}
$$

也就是：

$$
\delta
=
8.00777312\times10^{-8}.
$$

取：

$$
c_0
=
1.12274224-\delta
=
\frac{350856924975709}{312500000000000}.
$$

其餘 dual coefficients 保持：

$$
y_1=-0.38437941,
$$

$$
y_2=-0.25114540,
$$

$$
y_3=-0.11796917,
$$

$$
\mu=-0.03068556.
$$

三種 multiplicity patterns 的 configuration-wise reduced cost 仍能以 exact-rational Bernstein subdivision 證明非負。

因此：

$$
\boxed{
B_{70}^{cert}
=
\frac{35186790600709}{9589237500000}
=
3.669404433950979\ldots
}
$$

對所有：

$$
B\le B_{70}^{cert}
$$

皆嚴格推出：

$$
\boxed{
p_{min}(B)\ge0.70.
}
$$

---

# 1. 與 numerical crossing 的距離

上一輪 continuous column-generation 的 crossing 約：

$$
B_{70}^{num}
\approx3.66941.
$$

現在 exact：

$$
B_{70}^{cert}
=
3.669404433950979.
$$

差約：

$$
3.66941-B_{70}^{cert}
\approx
5.56604902e-06.
$$

也就是大約：

$$
5.6\times10^{-6}
$$

的 $B$ 尺度。

因此 numerical discovery 與 exact certificate 在 toy model 中已經非常接近。

---

# 2. 為什麼 safety margin 不能直接取零？

原 numerical dual 經十進位 rationalization 後，並不恰好是精確 dual optimum。

例如 $(2,2)$ pattern 的 nominal exact-rational quartic 具有極小的負谷，數值約：

$$
-8.0077731\times10^{-8}.
$$

$(2,1,1)$ nominal polynomial 的最小負值約：

$$
-6.72\times10^{-8}.
$$

因此不是 Bernstein 方法「證不出來」，而是：

$$
\boxed{
\text{直接把 numerical decimals 當 exact dual，確實會有微小違例。}
}
$$

這正是 QCI 意義上的一個小型範例：

> 數值上看似有效的 certificate，在進入 exact arithmetic 後必須保留足夠 margin。

本輪選：

$$
\delta=8.00777312\times10^{-8}
$$

正是稍微越過最壞的 rationalization defect。

---

# 3. Exact certification complexity

在此極小 margin 下：

### $(2,2)$

exact univariate Bernstein subdivision 仍可終止。

### $(2,1,1)$

exact bivariate Bernstein subdivision：

- internal boxes：約 $131$；
- terminal boxes：約 $132$。

### $(1,1,1,1)$

沿用 Newton/self-inversive 降維後的三變量 superset proof：

- internal boxes：$179$；
- terminal boxes：$180$；
- max depth：$13$；
- 最小 terminal Bernstein coefficient即約為 safety margin：

$$
8.00777312\times10^{-8}>0.
$$

所以 fully-simple branch 並不是 threshold 的主要瓶頸；真正限制 safety margin 的是 rationalized dual 在 collision patterns 上的極小違例。

---

# 4. 現在可以怎麼描述 toy threshold？

嚴格可說：

$$
\boxed{
B_{70}^*
\ge
3.669404433950979\ldots
}
$$

其中：

$$
B_{70}^*
=
\sup\{
B:p_{min}(B)\ge0.70
}.
$$

numerical evidence則提示：

$$
B_{70}^*
\approx3.66941.
$$

但後者尚不是 upper-bound theorem。

---

# 5. 這一輪真正教我們的事

原本我們想問：

> 「Claude 的 $67.2\%$ 怎麼變 $70\%$？」

現在 toy model 已經演化成：

$$
\text{numerical dual}
\rightarrow
\text{rationalized dual}
\rightarrow
\text{find exact defect}
\rightarrow
\text{add minimal safety margin}
\rightarrow
\text{exact Bernstein proof}
\rightarrow
\text{certified escape threshold}.
$$

這是一個完整的「AI 數學候選結果如何進入 exact proof domain」的小型示範。

下一步應該不再繼續追 $B$ 的第七、第八位小數，而是把單一 boundary row：

$$
S(4)
$$

替換成真正的 **continuous support strip**：

$$
\alpha\in[1,1+\delta].
$$

如此才會開始和 Claude 真實的：

$$
\sigma_{70}\approx1.04
$$

進入同一種定量問題。
