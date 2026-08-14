# 07 — $N=4$ Continuous Toy PairCeiling 的 Exact-Rational Bernstein Certificate
## 從 numerical candidate 提升到可機器重算的嚴格下界

**日期：** 2026-08-11  
**狀態：** exact-rational finite certificate；尚未形式化到 Lean  
**作用域：** 本研究定義的 $N=4$ continuous-position toy marked-configuration class，不是 Riemann zeta theorem。

---

# 0. 結論

我們現在可以嚴格證明，在下列 toy configuration class：

- total multiplicity：

$$
N=4;
$$

- marks：

$$
m_i\in\{1,2\};
$$

- positions 任意位於 unit circle；
- configuration-wise open-band constraints只觀察：

$$
j=1,2,3;
$$

- CUE target：

$$
S(1)=\frac14,\qquad
S(2)=\frac12,\qquad
S(3)=\frac34,
$$

其 primal adversarial-law optimum 至少滿足：

$$
\boxed{
p_{\min}
\ge
0.6982110925.
}
$$

也就是：

$$
\boxed{
p_{\min}
\ge
69.82110925\%.
}
$$

這不是 numerical optimiser 給的下界，而來自一個 exact-rational dual certificate 加上 exact-rational Bernstein subdivision。

前一輪 numerical column generation 的 candidate floor 約：

$$
69.82311\%.
$$

因此目前 toy optimum 被夾在極窄區域附近：

$$
69.82110925\%
\le
p_{\min}
\approx
69.82311\%.
$$

右側仍是 numerical candidate，不是 rigorous upper bound；真正嚴格的是左側。

---

# 1. Dual certificate

取：

$$
c_0
=
\frac{99998}{100000}
=
0.99998,
$$

$$
y_1
=
-\frac{42763734}{10^8},
$$

$$
y_2
=
-\frac{25119857}{10^8},
$$

$$
y_3
=
-\frac{9234705}{10^8}.
$$

對任意 configuration $\mathcal C$，希望證明：

$$
c_0
+
y_1S_{\mathcal C}(1)
+
y_2S_{\mathcal C}(2)
+
y_3S_{\mathcal C}(3)
\le
p(\mathcal C).
$$

若成立，LP dual objective 給：

$$
L
=
c_0
+
\frac14y_1
+
\frac12y_2
+
\frac34y_3.
$$

exactly：

$$
\boxed{
L
=
\frac{279284437}{400000000}
=
0.6982110925.
}
$$

因此弱對偶直接給：

$$
p_{\min}\ge L.
$$

---

# 2. 為什麼只要檢查三種 multiplicity pattern？

對：

$$
N=4,
\qquad
m_i\in\{1,2\},
$$

所有 partition 只有：

$$
(1,1,1,1),
$$

$$
(2,1,1),
$$

$$
(2,2).
$$

位置則仍然是 continuous。

---

# 3. Pattern $(1,1,1,1)$

此時：

$$
p=1.
$$

而：

$$
S(j)\ge0,
$$

且：

$$
y_j<0.
$$

因此：

$$
c_0+\sum_{j=1}^3y_jS(j)
\le
c_0
=
0.99998
<
1=p.
$$

這一支不需要數值計算。

---

# 4. Pattern $(2,2)$

利用 translation symmetry，兩個 double points 可放在：

$$
0,\theta.
$$

令：

$$
q=\cos\theta\in[-1,1].
$$

則：

$$
S_j
=
2+2\cos(j\theta).
$$

reduced-cost polynomial 可精確化成：

$$
R_{22}(q)
=
\frac{
36938820q^3
+
50239714q^2
+
15059619q
+
1999439
}{
50000000
}.
$$

我們把：

$$
q=2Q-1,
\qquad
Q\in[0,1]
$$

轉成 degree-$3$ Bernstein basis。

全域 Bernstein coefficients 並非全部非負，因此做 midpoint subdivision。

Exact-rational subdivision結果：

- internal nodes：$3$；
- terminal boxes：$4$；
- maximum depth：$3$；
- 所有 terminal Bernstein coefficients 非負；
- 最小 terminal coefficient：

$$
\boxed{
\frac{120357}{25000000}
=
0.00481428.
}
$$

所以：

$$
R_{22}(q)>0
$$

對所有：

$$
q\in[-1,1].
$$

---

# 5. Pattern $(2,1,1)$

利用 translation symmetry，把 double point 放在 $0$，兩個 simple phases 為：

$$
\alpha,\beta.
$$

定義：

$$
u=\frac{\alpha+\beta}{2},
\qquad
v=\frac{\alpha-\beta}{2}.
$$

則：

$$
2+e^{ij\alpha}+e^{ij\beta}
=
2+2e^{iju}\cos(jv).
$$

所以：

$$
S_j
=
1+\cos^2(jv)+2\cos(jv)\cos(ju).
$$

再令：

$$
x=\cos u,\qquad
z=\cos v.
$$

由 Chebyshev polynomials：

$$
\cos(ju)=T_j(x),
\qquad
\cos(jv)=T_j(z),
$$

得到二變量 polynomial：

$$
R_{211}(x,z)
=
-\frac12+2\times10^{-5}
+
\sum_{j=1}^3
a_j
\left[
1+T_j(z)^2+2T_j(z)T_j(x)
\right],
$$

其中：

$$
a_1=\frac{42763734}{10^8},
$$

$$
a_2=\frac{25119857}{10^8},
$$

$$
a_3=\frac{9234705}{10^8}.
$$

而：

$$
(x,z)\in[-1,1]^2.
$$

將：

$$
x=2X-1,
\qquad
z=2Z-1
$$

搬到：

$$
[0,1]^2
$$

後，使用 exact-rational bivariate Bernstein coefficient subdivision。

結果：

- internal boxes：$77$；
- certified terminal boxes：$78$；
- maximum subdivision depth：$16$；
- 所有 terminal Bernstein coefficients 非負；
- 全部 terminal boxes 中最小 Bernstein coefficient為：

$$
\boxed{
\frac{
195858711475181
}{
34359738368000000000
}
}
$$

約：

$$
5.70023873225\times10^{-6}>0.
$$

因此：

$$
R_{211}(x,z)>0
$$

對整個：

$$
[-1,1]^2.
$$

---

# 6. 這已經證明什麼？

三個 pattern 全部通過，因此：

$$
\boxed{
c_0+\sum_{j=1}^3y_jS_{\mathcal C}(j)
\le
p(\mathcal C)
}
$$

對我們 $N=4$ 的完整 continuous toy configuration class 成立。

故對任意 probability law：

$$
\mathcal L=\{w_c,\mathcal C_c\},
$$

若：

$$
\mathbb E_{\mathcal L}[S(j)]
=
\frac j4,
\qquad
j=1,2,3,
$$

就有：

$$
\boxed{
\mathbb E_{\mathcal L}[p]
\ge
69.82110925\%.
}
$$

這是我們目前第一個 **certified small-$N$ PairCeiling analogue**。

---

# 7. 與 Anthropic ceiling 的關係

Anthropic $N=256$ exact-rational law 約：

$$
68.1828687\%.
$$

我們的 $N=4$ certified floor：

$$
69.82110925\%.
$$

兩者相差約：

$$
1.63824
$$

percentage points。

這不表示 $N\to\infty$ 必定收斂到 Anthropic 常數；但與前面的 numerical sequence：

$$
N=4,5,6,7
$$

往官方 law 下移的現象一致。

---

# 8. 為什麼 Bernstein 很適合這裡？

Bernstein basis 有一個非常重要的性質：

若 polynomial 在一個 box 上的所有 Bernstein coefficients 都非負，則：

$$
P(x)\ge0
$$

在整個 box 上。

若 global coefficients 尚不能證正，就對 domain 做 de Casteljau subdivision；每次 subdivision 仍保持 exact rational coefficients。

因此：

```text
numerical dual
→ rationalize with margin
→ derive exact polynomial
→ Bernstein subdivision
→ exact positivity certificate
```

是一條很自然的：

$$
\boxed{
\text{numerical discovery}
\rightarrow
\text{rigorous finite certificate}
}
$$

流程。

---

# 9. 下一個正式目標

我們現在應該把：

$$
N=4
$$

從 open-band certificate 進一步推到「最小 escape information」。

也就是新增一條 boundary / beyond-band constraint：

$$
S(4)\le B
$$

並找最弱的 $B$，使：

$$
p_{\min}\ge0.70.
$$

這就是 toy 版本的：

$$
I_{70}^*.
$$
