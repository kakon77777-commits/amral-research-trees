# 15 — Matrix Majorant–Inertia Problem（MMIP）
## 用 CGdL Tail-Sign SDP 與 Claude Off-Axis Signature 尋找無條件改進

**日期：** 2026-08-11  
**狀態：** literature audit + new research programme  
**不是結果宣稱：** 本文件沒有證明新的 $\zeta$ 零點比例，只定位一條可能避開 $\alpha>1$ asymptotic 的混合路線。

---

# 0. 為什麼重新看 CGdL？

Chirre–Gonçalves–de Laat（CGdL）在 RH 下將 Montgomery–Taylor 的 multiplicity constant：

$$
1.3275
$$

改進到：

$$
1.3208.
$$

因此 simple-zero lower proportion由：

$$
67.25\%
$$

提高到：

$$
67.92\%.
$$

它們並沒有取得 $F(\alpha)$ 在 $|\alpha|>1$ 的新 asymptotic。

核心技巧是放寬 bandlimited condition，允許：

$$
\widehat f(\alpha)\le0
\qquad
(|\alpha|\ge1).
$$

由於 pair form factor：

$$
F(\alpha,T)\ge0,
$$

未知 band 的積分：

$$
\int_{|\alpha|>1}
\widehat f(\alpha)F(\alpha,T)\,d\alpha
$$

對所需 upper bound只會有利，因此可以丟掉。

這是：

$$
\boxed{
\text{使用未知區域的 sign，而不是 value。}
}
$$

---

# 1. 2024/2026 後 prime-side sign 已經無條件

Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh 的 unconditional Montgomery theorem定義了不假設 RH 的 form factor，並證明：

$$
\boxed{
F(\alpha)\ \text{real, even, nonnegative}
}
$$

對所有 real $\alpha$，同時在：

$$
0\le\alpha\le1
$$

給出 Montgomery asymptotic。

所以 CGdL prime-side 的兩個原料：

1. known-band asymptotic；
2. outside-band nonnegativity；

現在都有無條件版本。

這會讓人第一眼猜：

> 能不能把 CGdL 的 $67.92\%$ 直接改成無條件？

答案目前是：不能直接如此推論。

---

# 2. 缺口在 zero side，不在 prime side

CGdL 的 scalar pair sum是：

$$
\sum_{\gamma,\gamma'}
g\!\left(
(\gamma-\gamma')
\frac{\log T}{2\pi}
\right)
w(\gamma-\gamma').
$$

在 RH 下：

- 每個 zero ordinate $\gamma$ 是 real；
- $g\ge0$；
- $w(\gamma-\gamma')>0$；
- 每個 off-diagonal scalar term非負。

所以它們可以直接得到：

$$
\boxed{
\text{pair sum}
\ge
g(0)\sum_\gamma m_\rho
}
$$

即其 equation (10)，從而下界 multiplicity sum。

但離開 RH 後，BGSTB 的 unconditional form factor使用：

$$
x^{\rho-\rho'}w(\rho-\rho')
$$

或等價的 functional-equation symmetrisation。

零點的 horizontal displacement 進入 complex arguments；CGdL 的 scalar nonnegative-kernel lower bound不再自動成立。

因此：

$$
\boxed{
\text{BGSTB prime-side positivity}
+
\text{CGdL scalar proof}
\not\Rightarrow
\text{unconditional }67.92\%.
}
$$

---

# 3. Claude 補上的正是另一種 zero-side機制

Claude 不要求整個 pair sum為正。

它把 finite compression寫成：

$$
\widetilde G=P+Q,
$$

其中：

- critical-line zeros貢獻：

$$
P\succeq0;
$$

- 每一個 off-axis functional-equation pair貢獻 signature：

$$
(1,1)
$$

的 indefinite block。

然後用 inertia + rank–trace inequality控制 positive index與 rank。

因此 Claude 解決 zero-side 的方式是：

$$
\boxed{
\text{block signature}
}
$$

而不是：

$$
\boxed{
\text{scalar termwise positivity}.
}
$$

---

# 4. 新問題：MMIP

我們定義：

## Matrix Majorant–Inertia Problem（MMIP）

尋找一個 test / finite compression，使以下三件事同時成立。

### M1 — Tail-sign prime control

Fourier side允許：

$$
\widehat f(\alpha)\le0
\qquad
(|\alpha|\ge1),
$$

並利用 unconditional：

$$
F(\alpha)\ge0
$$

丟掉 unknown tail，像 CGdL 一樣得到更好的 prime-side upper bound。

### M2 — Off-axis block control

zero side不能依賴 RH 下的 scalar nonnegative kernel，而必須保留 Claude 的：

$$
(1,1)
$$

off-axis block signature。

### M3 — Matrix certificate

建立新的 matrix inequality，把：

- prime-side tail-sign upper bound；
- critical-line PSD rank；
- off-axis positive-index budget；

轉成：

$$
N_0^s/N
$$

的 lower bound。

---

# 5. 為什麼這條路可能避開 $P_{70}$ 的 prime-pair牆？

generalized-support route要真正知道：

$$
F(\alpha)
$$

在：

$$
1<|\alpha|\le1.043
$$

的 weighted value。

MMIP 只想使用：

$$
F(\alpha)\ge0
$$

和：

$$
\widehat f(\alpha)\le0.
$$

所以它可能在完全不計算 $O_1$ beyond $\sigma=1$ 的情況下，改善 test-function constant。

這與前面 toy Boundary-Spike研究的語言一致：

> 不一定要完整觀測 boundary；也可以加入一個只限制其符號／方向的 dual price。

---

# 6. 常數目標

比較：

| Certificate | Effective $C$ | $2-C$ |
|---|---:|---:|
| Montgomery–Taylor / Claude D | $1.3274993$ | $67.2501\%$ |
| CGdL scalar SDP（RH） | $1.3208$ | $67.92\%$ |
| Bandwidth-one configuration-wise ceiling | $1.31815$ | $68.185\%$ |
| CGdL GRH comparison | $1.3155$ | $68.45\%$ |
| $P_{70}$ | $1.30$ | $70\%$ |

因此：

### 第一階段

只要 matrix-tail certificate取得：

$$
C<1.3274993,
$$

就是對 Claude $67.25\%$ 的無條件改善候選。

### 第二階段

要穿過：

$$
68.185\%
$$

需：

$$
C<1.31815.
$$

published CGdL RH constant：

$$
1.3208
$$

本身還不夠跨過該 ceiling。

### 第三階段

要達：

$$
70\%
$$

需：

$$
C\le1.30.
$$

只靠目前 CGdL-type tail sign是否可能做到，完全未知。

---

# 7. 一個可能的 SDP formulation

目前只給出研究骨架。

選一族 basis functions：

$$
\{f_1,\ldots,f_d\}.
$$

建立 Hermitian compression：

$$
G_{ij}=W(f_i,f_j).
$$

再引入一個 Fourier-side majorant matrix kernel：

$$
\widehat{\mathcal K}(\alpha).
$$

要求：

### Known band

$$
|\alpha|\le1
$$

時，prime-side trace / Frobenius quantities可由 unconditional Montgomery theorem計算。

### Unknown band

$$
|\alpha|>1
$$

時，要求適當 matrix ordering：

$$
\widehat{\mathcal K}(\alpha)\preceq0,
$$

使：

$$
F(\alpha)\ge0
$$

能提供 one-sided prime bound。

### Zero side

對 critical zero：

$$
B_{\rm crit}\succeq0.
$$

對 off-axis pair：

$$
B_{\rm off}
$$

保持可審計的 inertia budget，而不是被 scalar majorisation破壞。

---

# 8. 第一個 technical obstruction

scalar condition：

$$
\widehat f\le0
$$

不自動等於：

$$
\widehat{\mathcal K}\preceq0.
$$

而且一個有利於 prime-side tail的 matrix majorant，可能同時破壞 zero-side：

- rank-one critical contribution；
- off-axis hyperbolic block；
- Poisson–Gabor locality；
- Claude Lemma 3.2 所需 decomposition。

所以 MMIP 的核心不是「把 CGdL function 塞進 Claude」。

而是：

$$
\boxed{
\text{同時相容於 Fourier tail order 與 zero-side inertia 的 matrix cone。}
}
$$

---

# 9. 第一個可執行 MVP

不直接做完整 zeta theorem。

先做 finite configuration toy：

1. 取前面 $N=4$ marked configurations；
2. 在 open-band row constraints外，加入一個「tail nonnegative、dual coefficient nonpositive」的抽象 observable；
3. 允許 matrix block而不是 scalar certificate；
4. 用 SDP 求最小 simple fraction；
5. 看它是否超過 scalar bandwidth-one floor；
6. 再把可行 matrix inequality轉成 exact rational / Bernstein或SOS certificate。

這可以先回答：

> tail-sign + inertia在有限 toy world裡是否真的有協同增益？

若連 toy 都沒有增益，就不值得直接攻完整 zeta。

---

# 10. 本輪結論

direct arithmetic route目前遇到 short-interval range與精度障礙。

但 unconditional $F\ge0$ 又提供一條不同資訊：

$$
\boxed{
\text{不知道 unknown band 的值，
但知道它的方向。}
}
$$

CGdL 已在 RH scalar setting證明這種方向資訊可改善常數。

Claude則提供不依賴 RH 的 off-axis inertia bookkeeping。

因此 MMIP 是目前最具體的混合研究問題：

$$
\boxed{
\text{Tail sign}
+
\text{Matrix inertia}
\stackrel{?}{\Longrightarrow}
\text{unconditional improvement beyond }67.25\%.
}
$$
