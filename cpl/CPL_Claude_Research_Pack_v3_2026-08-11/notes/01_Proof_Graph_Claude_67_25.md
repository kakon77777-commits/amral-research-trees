# 01 — Claude 67.25%：證明鏈模組化重建

## 1. 目標命題

研究核心是：

$$
\liminf_{T\to\infty}
\frac{N_0^s(T,2T)}{N(T,2T)}
\ge0.672500\ldots.
$$

這不是逐顆零點驗證，而是 asymptotic proportion certificate。

---

## 2. 模組 Z：Zero Side

把 Weil Hermitian form 限制到有限維 test family $V$，得到 Hermitian compression $\widetilde G$。

由 functional equation 對稱：

- critical-line distinct point 提供 rank-one nonnegative contribution；
- off-line pair $\{\rho,1-\bar\rho\}$ 在適當基底中產生 hyperbolic block：

$$
\begin{pmatrix}
0&m\\
m&0
\end{pmatrix},
$$

其 signature 為：

$$
(1,1).
$$

因此可分解：

$$
\widetilde G=P+Q,
$$

其中 $P\succeq0$，而 $Q$ 的 positive index 由 off-line pairs 控制。

---

## 3. 模組 L：Linear Algebra

Claude Lemma 3.2：若 $P,Q$ Hermitian，且

$$
P\succeq0,\qquad \operatorname{rank}P\le r,\qquad n_+(Q)\le b,
$$

則對 $c>0$：

$$
\|P+Q\|_F^2
\ge
c\operatorname{tr}P
-
\frac{c^2}{4}r
+
2c\operatorname{tr}Q
-
c^2b.
$$

取 $c=2$：

$$
r
\ge
2\operatorname{tr}P
+4\operatorname{tr}Q
-4b
-\|P+Q\|_F^2.
$$

此處用 von Neumann trace inequality 控制 positive/negative spectral parts 的最壞耦合。

---

## 4. 模組 P：Prime Side

利用 explicit formula，把 compression 的 traces 化成 prime-power / archimedean integrals。

對 $0<\lambda\le1$，無條件得到主項：

$$
\operatorname{tr}\widetilde G\sim N,
$$

$$
\operatorname{tr}\widetilde G^2
\sim
\left(\frac1\lambda+\frac\lambda3\right)N.
$$

關鍵結構邊界：

$$
\lambda\le1.
$$

若超過 $1$，off-diagonal prime sums 不再由 diagonal 自動壓制，需 prime-pair / Hardy--Littlewood 或等價的更強 pair-correlation 輸入。

---

## 5. Flat window：$2/3$

把 Z、P、L 合起來得到：

$$
H(\lambda)
=
2-
\frac1\lambda
-
\frac\lambda3.
$$

在允許區間 $0<\lambda\le1$ 上，最佳點為：

$$
\lambda=1,
$$

所以：

$$
H(1)=2-1-\frac13=\frac23.
$$

---

## 6. Window optimisation：$67.25\%$

§7.1 對 window density $v$ 最佳化 scale-free functional：

$$
c_\lambda(v)
=
\frac{
\lambda\left(\int v\right)^2
}{
\int v^2
+
\lambda^2
\iint |s-s'|v(s)v(s')\,ds\,ds'
}.
$$

Euler / extremal problem 給：

$$
v_\lambda^*(s)=\cos(\sqrt2\lambda s),
$$

以及：

$$
c_\lambda^*
=
\frac{\sqrt2\tan\theta}{1+\theta\tan\theta},
\qquad
\theta=\frac\lambda{\sqrt2}.
$$

於 $\lambda=1$：

$$
c_1^*=0.753296\ldots,
$$

所以：

$$
P_{MT}
=
2-
\frac1{c_1^*}
=
0.672500\ldots.
$$

CCLM17 的 one-delta extremal result 被 Claude 用來說明：在「只使用 Montgomery $F(\alpha)$ 於 $[-1,1]$ 的值」且保持 §7.1 這類 window extremisation 時，Montgomery--Taylor kernel 已是 extremal；因此此子框架不能只靠換 window 再提高。

---

## 7. Higher moments

現有 unconditional 主證明只真正使用低階 moments。Claude §7.5 將 sharp positive-eigenvalue lower bound 連到 one-sided Chebyshev--Markov--Stieltjes / Christoffel function。

如果 normalized moments 到 $2m$ 階可知，則可改善 $n_+$ certificate。

對 conditional $HL^*(4,\lambda)$，在 $\lambda\to1$：

$$
m_1=1,\qquad
m_2=\frac43,\qquad
m_3=2,\qquad
m_4=\frac{13}{4}.
$$

論文得到：

$$
\Lambda_2(0;1)=\frac5{36},
$$

以及：

$$
\frac{N_0^s}{N}
\ge
\frac{13}{18}
\approx72.22\%.
$$

因此 $P_{70}$ 存在一條非常具體的 conditional moment route。

---

## 8. 第一批 Proof Obligations

### PO-01
獨立證明 Lemma 3.2，逐項追 equality condition。

### PO-02
從 functional-equation pair 明確導出 $(1,1)$ block，而不是只接受敘述。

### PO-03
重新做 normalization，確定：

$$
\operatorname{tr}\widetilde G\sim N,
\qquad
\operatorname{tr}\widetilde G^2\sim\left(\frac1\lambda+\frac\lambda3\right)N.
$$

### PO-04
獨立解 $c_\lambda(v)$ extremal problem。

### PO-05
追查 $0.68185$ 的 configuration extremal law；目前只確認主論文 Remark 1.1 的結論，尚未在正文中定位完整 derivation。
