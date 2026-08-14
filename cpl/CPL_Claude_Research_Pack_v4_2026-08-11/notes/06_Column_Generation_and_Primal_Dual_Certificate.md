# 06 — Column Generation、Continuous Pricing 與 PairCeiling 的 Primal/Dual 對偶
## 從 toy LP 正式接回 Anthropic 的 certificate language

**日期：** 2026-08-11  
**狀態：** 結構推導成立；數值 floors 為 exploratory candidates，尚非 certified global optima。

---

# 0. 本輪最重要的結果

前一輪我們只知道 small-$N$ toy LP「看起來很像」Anthropic 的 bandwidth-one adversarial law。

這一輪可以把兩者精確接起來。

Toy primal：

$$
\min_{w_c}
\sum_c w_c p_c
$$

subject to：

$$
\sum_cw_c=1,
$$

以及 open-band row constraints：

$$
\sum_cw_cS_c(j)=\frac{j}{N},
\qquad
j=1,\ldots,N-1.
$$

其 LP dual 為：

$$
\max_{y_0,y_1,\ldots,y_{N-1}}
\left[
y_0+\sum_{j=1}^{N-1}\frac{j}{N}y_j
\right]
$$

subject to對每一個 configuration $\mathcal C_c$：

$$
y_0+\sum_{j=1}^{N-1}y_jS_c(j)
\le p_c.
$$

現在定義：

$$
c_0:=y_0,
$$

以及離散 certificate samples：

$$
\boxed{
r_N(j/N):=Ny_j.
}
$$

因為 Anthropic 的 grid masses 是：

$$
s_j=\frac{S(j)}{N},
$$

dual constraint 就變成：

$$
\boxed{
c_0+\sum_{j=1}^{N-1}s_jr_N(j/N)\le p_c.
}
$$

這正是 `PairCeiling` 使用的 configuration-wise certificate inequality 的離散形式。

而 dual objective：

$$
y_0+\sum_{j=1}^{N-1}\frac{j}{N}y_j
$$

可以重寫：

$$
c_0+\sum_{j=1}^{N-1}
\frac{j}{N^2}r_N(j/N).
$$

當 $N\to\infty$，若 $r_N\to r$ 夠規則，Riemann sum 形式變成：

$$
\boxed{
c_0+\int_0^1 r(x)x\,dx.
}
$$

這又正是 Anthropic `PairCeiling` 的 continuum certificate value。

因此：

$$
\boxed{
\text{our primal/dual toy LP}
\longrightarrow
\text{Anthropic PairCeiling certificate}
}
$$

不是比喻，而是同一 convex-duality structure 的離散化。

---

# 1. Column generation 的意義也因此變得非常清楚

Master LP 只放一小部分 configurations。

解 master 後得到 dual：

$$
(c_0,y_1,\ldots,y_{N-1}).
$$

對任何新 configuration $\mathcal C$，reduced cost：

$$
RC(\mathcal C)
=
p(\mathcal C)
-
\left[
c_0+\sum_{j=1}^{N-1}y_jS_{\mathcal C}(j)
\right].
$$

用 certificate notation：

$$
RC(\mathcal C)
=
p(\mathcal C)
-
\left[
c_0+\sum_{j=1}^{N-1}
\frac{S_{\mathcal C}(j)}{N}
r_N(j/N)
\right].
$$

因此：

### 若

$$
RC(\mathcal C)<0,
$$

表示目前 dual certificate **不是 configuration-wise valid**。

我們找到了一個反例 configuration。

### 若

$$
RC(\mathcal C)\ge0
$$

對全部 configuration 都成立，

則 dual 就是整個 configuration class 上的有效 certificate。

所以 pricing problem 本身就是：

$$
\boxed{
\text{自動搜尋 certificate 的反例 configuration。}
}
$$

這其實與 Claude 研究流程中的「candidate theorem → adversarial referee / counterexample search」具有非常直接的工程對應。

---

# 2. Continuous-position pricing

前一輪 positions 只能在 $M$ 個 grid sites。

這輪不再枚舉所有 continuous configurations。

對每一種 multiplicity pattern，例如：

$$
(2,1,1,\ldots,1),
$$

固定 translation symmetry：

$$
x_1=0,
$$

然後對其餘：

$$
x_i\in[0,1)
$$

直接數值解：

$$
\min_{\mathbf x}
RC(\mathbf x).
$$

也就是 nonlinear configuration-pricing problem。

找到負 reduced cost column 後：

```text
solve master LP
→ read dual prices
→ continuous pricing
→ add most violating configuration
→ solve master again
→ repeat
```

這就是標準 column generation。

---

# 3. Numerical candidate floors

使用 multiple numerical global-search seeds 做 continuous pricing 後，目前取得：

| $N$ | candidate floor |
|---:|---:|
| $4$ | $69.82311\%$ |
| $5$ | $69.22046\%$ |
| $6$ | $68.89346\%$ |
| $7$ | $68.71442\%$ |

官方 $N=256$ exact-rational law：

$$
68.1828687\ldots\%.
$$

相對 gap：

| $N$ | 與官方 $N=256$ law 差距 |
|---:|---:|
| 4 | $1.6402$ percentage points |
| 5 | $1.0376$ |
| 6 | $0.7106$ |
| 7 | $0.5316$ |

這是一個很強的數值信號：

$$
\boxed{
\text{放開 continuous positions 後，toy primal 的 floor 確實快速向官方 law 靠近。}
}
$$

但不能宣稱：

$$
p_N\to0.681828687\ldots
$$

因為：

1. 只有 $N=4,\dots,7$；
2. continuous pricing 使用 numerical global optimiser；
3. 沒有 interval / exact-rational global optimality certificate；
4. configuration class 與官方生成器仍未證明完全相同。

---

# 4. 一個新的結構現象：one-double defect

在後期 pricing 中，最常持續找到負 reduced-cost 的 pattern 是：

$$
\boxed{
(2,1,1,\ldots,1).
}
$$

例如：

- $N=4$：$(2,1,1)$；
- $N=5$：$(2,1,1,1)$；
- $N=6$：$(2,1,1,1,1)$；
- $N=7$：大量後期 pricing 仍由 one-double pattern 主導，雖然中段亦找到 $(2,2,\ldots)$ columns。

one-double configuration 的 simple fraction 為：

$$
p_{\mathrm{1dbl}}
=
\frac{N-2}{N}.
$$

Primal law 並不是全部使用低-simple configuration；它把：

$$
\text{fully simple configurations}
$$

與：

$$
\text{collision-defect configurations}
$$

混合，利用位置自由度調整 Fourier rows，使平均 pair data 回到 CUE。

暫時可把它理解成：

> **以稀疏 multiplicity defects 換取大幅 pair-spectrum 可調性。**

這可能是官方 marked-configuration extremal law 的有限-$N$影子。

---

# 5. Dual certificate samples

數值 master duals：

## $N=4$

$$
(y_0,y_1,y_2,y_3)
\approx
(1,
-0.427637,
-0.251199,
-0.092347).
$$

## $N=5$

$$
(1,
-0.365810,
-0.257489,
-0.146837,
-0.054420).
$$

## $N=6$

$$
(1,
-0.316559,
-0.245610,
-0.167512,
-0.094591,
-0.035543).
$$

## $N=7$

$$
(0.998343,
-0.277556,
-0.227637,
-0.171470,
-0.114935,
-0.064905,
-0.024481).
$$

重縮放：

$$
r_N(j/N)=Ny_j
$$

後，不同 $N$ 的 samples 已開始落在相似的 smooth negative profile 上，並朝：

$$
r(1)=0
$$

靠近。

這個現象非常重要，因為它直接顯示：

$$
\boxed{
\text{finite LP dual}
\rightarrow
\text{continuum certificate function }r(x).
}
$$

圖見：

```text
figures/dual_certificate_rescaled_samples.png
```

目前不應猜測精確閉式函數；需要更大的 $N$ 與 certified pricing。

---

# 6. 為什麼這幫助研究 $70\%$？

官方 bandwidth-one law 已經告訴我們：

$$
p_{\min}\approx0.68183.
$$

要得到：

$$
P_{70},
$$

等價於需要讓 admissible primal laws 滿足：

$$
p_{\min}\ge0.70.
$$

所以現在可以把任何額外數學資訊 $\mathcal I$ 直接加成新的 primal constraints：

$$
\mathcal F_1
\rightarrow
\mathcal F_1\cap\mathcal I.
$$

然後重新求：

$$
p_{\min}(\mathcal I).
$$

如果：

$$
p_{\min}(\mathcal I)\ge0.70,
$$

我們就知道這個資訊在抽象 certificate 層已足以突破 bandwidth-one ceiling。

這使「需要什麼新資訊」變成可以實驗的 optimisation problem。

---

# 7. Minimal Escape Constraint Search

下一個正式問題：

$$
\boxed{
I_{70}^*
=
\arg\min_{\mathcal I}
Cost(\mathcal I)
\quad
\text{s.t.}
\quad
p_{\min}(\mathcal I)\ge0.70.
}
$$

候選 $\mathcal I$：

### A. Support

加入：

$$
S(\alpha)
$$

在：

$$
1<\alpha\le1+\delta
$$

的資訊。

### B. Boundary control

例如：

$$
S(1)\le B.
$$

### C. Higher moments

對 pair matrix / spectral law 增加：

$$
m_3,m_4,\ldots
$$

### D. Multi-point statistics

引入三點或更高 correlation。

### E. Zeta realizability

加入真正 zeta zeros 必須滿足、但 abstract marked configurations 不必滿足的 arithmetic / analytic conditions。

最後一條最可能繞過純 pair-correlation 的資訊障礙。

---

# 8. 與 Boundary-Spike Obstruction 的結合

前輪已觀察：

$$
S(256)\approx211.432
$$

而所有：

$$
j<256
$$

rows 幾乎完全 CUE-like。

現在 primal/dual 對偶說明其原因可以更精確表示：

> Dual certificate 在 open band 裡沒有價格可以懲罰未觀測 boundary spike。

也就是：

$$
y_N
$$

根本不存在於 bandwidth-one master。

所以 primal 可以利用：

$$
S(N)
$$

作為「免費方向」。

一旦新增 boundary / beyond-band observable，就等於給這個方向一個新的 dual price：

$$
y_N.
$$

這是 BSO 的 convex-optimization 解釋。

---

# 9. 下一輪：從 heuristic pricing 到 certificate pricing

現在最大的數學缺口不是 master LP。

Master LP 是線性的，可以精確求。

真正缺口是 pricing：

$$
\min_{\mathcal C}RC(\mathcal C)
$$

在 continuous marked-configuration space 上能否被 certified global solve。

下一步可分三級：

### Level 1 — multi-start numerical

目前已做。

### Level 2 — interval branch-and-bound

對 positions box：

$$
[0,1]^{k-1}
$$

建立 Fourier polynomial 的 interval lower bounds，證明：

$$
RC\ge-\epsilon.
$$

### Level 3 — exact algebraic / SDP relaxation

把 trigonometric pricing 改寫成：

- unit-circle polynomial；
- moment/SOS relaxation；
- semidefinite bound；
- rational certificate。

若 Level 2/3 做成，我們就會開始擁有自己的：

$$
\boxed{
\text{small-N certified PairCeiling results}.
}
$$

---

# 10. 本輪結論

目前最重要的不是 candidate floor 本身。

而是我們已經建立：

$$
\boxed{
\text{Primal adversarial law}
\;\Longleftrightarrow\;
\text{Dual certificate}
}
$$

以及：

$$
\boxed{
\text{Column pricing}
=
\text{certificate counterexample search}.
}
$$

這使整個 Claude bandwidth-one ceiling 可以被重新理解成一個可計算、可迭代、可增加資訊約束的 convex research programme。

下一個真正值得做的是：

$$
\boxed{
\text{certified pricing}
+
\text{minimal }I_{70}^*\text{ search}.
}
$$
