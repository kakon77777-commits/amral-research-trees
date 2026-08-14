# 廣義 $mx+r$ 系統與 Residue-Class Operation Translation
## ——從 Collatz 特例到交換標量仿射動力、相變邊界與一般化局部圖冊

**English Title:** *Generalized $mx+r$ Systems and Residue-Class Operation Translation: Affine Word Closure, Local Atlases, and a Cylinder Phase Boundary*

**作者：** Neo.K  
**機構：** 一言諾科技有限公司（EveMissLab）  
**系列：** Collatz Operation Translation Series — Paper 07  
**版本：** v0.1.1  
**日期：** 2026-08-10  
**修訂日期：** 2026-08-14

---

## 摘要

前六篇以 modified Collatz map

$$
T(n)=
\begin{cases}
n/2,&n\text{ even},\\[2mm]
(3n+1)/2,&n\text{ odd}
\end{cases}
$$

建立 finite-word affine closure、parity-word/residue-cylinder 對應、局部 identity 化、雙向 $2^k\leftrightarrow3^u$ 殘餘類轉譯、有限字收縮邊界與 valuation language。

本文拔除 Collatz 特有的 $3,1$，考察正奇整數參數

$$
m\ge1,\qquad r\ge1,\qquad m,r\text{ odd}
$$

所定義的 parity-preserving generalized system

$$
\boxed{
T_{m,r}(n)
=
\begin{cases}
\dfrac n2,&n\equiv0\pmod2,\\[2mm]
\dfrac{mn+r}{2},&n\equiv1\pmod2.
\end{cases}
}
$$

令

$$
D(x)=\frac x2,
\qquad
U_{m,r}(x)=\frac{mx+r}{2}.
$$

本文證明，對任意長度 $k$ 的 finite parity word $w\in\{D,U\}^k$，若 $u=u(w)$，則形式 composition 恆有 exact affine closure：

$$
\boxed{
F_w^{(m,r)}(x)
=
\frac{m^u x+b_w^{(m,r)}}{2^k},
}
$$

其中

$$
\boxed{
b_w^{(m,r)}
=
r\sum_{t=1}^{u}
2^{j_t-1}m^{u-t},
}
$$

而 $j_t$ 是第 $t$ 個 $U$ 的位置。

因此 generalized system 保留：

$$
\boxed{
\text{branch counts determine the multiplicative skeleton;}
}
$$

$$
\boxed{
\text{branch order determines the affine correction.}
}
$$

更重要的是，因 $m$ 為奇數，

$$
\gcd(m^u,2^k)=1,
$$

所以每個 finite parity word 仍對應唯一 residue cylinder modulo $2^k$：

$$
\boxed{
\Omega_w^{(m,r)}
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0},
}
$$

且

$$
\boxed{
r_w
\equiv
-b_w^{(m,r)}m^{-u}
\pmod{2^k}.
}
$$

若

$$
s_w
=
F_w^{(m,r)}(r_w),
$$

則：

$$
\boxed{
T_{m,r}^k(r_w+2^ka)
=
s_w+m^ua.
}
$$

因此 source $2^k$-cylinder 被 exact 送往 target $m^u$-progression：

$$
\boxed{
r_w+2^k\mathbb Z
\longleftrightarrow
s_w+m^u\mathbb Z,
}
$$

並在 source/target quotient coordinates 中再次 identity 化：

$$
\boxed{
\psi_w
\circ
T_{m,r}^k
\circ
\phi_w^{-1}
=
\operatorname{id}.
}
$$

這證明前六篇最核心的 local-affine/identity structure 並非 $3x+1$ 特有，而屬於更廣泛的 odd-$m$, odd-$r$ residue-class affine family。

對固定 $(k,u)$，當 $r>0$ 時，order correction 有 exact bounds：

$$
\boxed{
r\,\frac{m^u-2^u}{m-2}
\le
b_w^{(m,r)}
\le
r\,2^{k-u}\frac{m^u-2^u}{m-2}
}
$$

（$m\neq2$，而本文 $m$ 為 odd）。最小值由

$$
U^uD^{k-u}
$$

取得，最大值由

$$
D^{k-u}U^u
$$

取得。

finite-word drift 則由：

$$
\boxed{
m^u\lessgtr2^k
}
$$

完全決定其 skeleton side。若

$$
m^u<2^k,
$$

存在 finite threshold 使整個 chart 最終 strict descent；若

$$
m^u>2^k,
$$

則整張 positive admissible cylinder 在該 $k$-block 上 strict expansion。

對 $m>1$，定義：

$$
\boxed{
\alpha_m
=
\frac{\ln2}{\ln m}.
}
$$

則 contracting condition 為：

$$
\boxed{
\frac uk<\alpha_m.
}
$$

因 odd $m>1$ 不可能是 2 的冪，$\alpha_m$ 無理，所以 length-$k$ contracting cylinder count 為：

$$
\boxed{
A_k(m)
=
\sum_{u=0}^{\lfloor\alpha_m k\rfloor}
\binom ku.
}
$$

比例：

$$
\boxed{
P_k(m)
=
\frac{A_k(m)}{2^k}.
}
$$

這導致一條 generalized cylinder phase theorem：

- $m=1$：所有 nonempty finite words 均位於 contracting-skeleton side；
- $m=3$：$\alpha_3>1/2$，故
  $$
  \boxed{P_k(3)\to1;}
  $$
- odd $m\ge5$：$\alpha_m<1/2$，故
  $$
  \boxed{P_k(m)\to0.}
  $$

連續參數意義下的臨界值恰為：

$$
\boxed{
m_c=4.
}
$$

這個臨界來自：

$$
\frac{\ln2}{\ln m}
=
\frac12
\iff
m=4.
$$

值得注意的是，Gonçalves–Greenfeld–Madrid 對更一般 $p,q,r$ Collatz-like maps 的 almost-all theorem 使用條件：

$$
q<p^{p/(p-1)}.
$$

當 $p=2$ 時恰為：

$$
\boxed{
q<4.
}
$$

因此本文由 finite-word/residue-cylinder 組合計數得到的 parity-family phase boundary，與既有更深 almost-all analytic theory 在 $p=2$ 截面上出現同一臨界常數。本文不把兩者視為同一定理：前者是 deterministic finite chart density，後者是 actual orbit 的 logarithmic-density theorem；其吻合應被理解為一個重要的結構交叉驗證。

本文亦證明 additive parameter $r$ 不改變 asymptotic skeleton boundary：

$$
m^u\lessgtr2^k
$$

只依賴 $m,k,u$。$r$ 線性縮放 correction，因而主要控制 finite-size threshold、fixed-point位置與局部 orbit geometry，而不移動 cylinder-density phase boundary。

本文最後把這一類結構定義為 **Residue-Class Operation Translation (RCOT) parity kernel**：只要 branch maps 為交換標量仿射算子，且 odd multiplier 對 binary denominator 為 unit，則 finite-word closure、unique residue chart、local identityization、exact recovery 與 count/order decomposition 全部成立。

下一篇將進一步把係數所在代數逐層擴張至有零因子的交換環、無序域、矩陣／非交換代數、Möbius transformation 與高次 polynomial dynamics，以確定 RCOT 的真正代數判定域與第一個結構斷裂點。

**關鍵詞：** generalized Collatz、$mx+r$、residue-class affine map、operation translation、local affine atlas、phase boundary、parity word、binomial cylinder law、exact recovery

---

# 1. 從 Collatz 特例拔除 $3,1$

Collatz modified branches：

$$
D(x)=\frac x2,
\qquad
U(x)=\frac{3x+1}{2}.
$$

其中真正使用到的局部代數條件其實是：

1. $D,U$ 都是 affine；
2. odd branch 的 multiplier 為 odd；
3. translation term 也是 odd，使 odd input 映到 integer；
4. denominator 為 2；
5. scalar coefficients commute。

所以考慮：

$$
\boxed{
D(x)=\frac x2,
}
$$

$$
\boxed{
U_{m,r}(x)=\frac{mx+r}{2},
}
$$

其中：

$$
m,r\in2\mathbb Z+1,
\qquad
m,r>0.
$$

---

# 2. 為什麼 $m,r$ 必須 odd？

若：

$$
n\text{ odd},
$$

且：

$$
m,r\text{ odd},
$$

則：

$$
mn+r
=
\text{odd}+\text{odd}
=
\text{even}.
$$

所以：

$$
U_{m,r}(n)
=
\frac{mn+r}{2}
\in\mathbb Z.
$$

因此：

$$
\boxed{
\text{odd branch legality is automatic on odd inputs}.
}
$$

---

# 3. Formal Word

取：

$$
w=\sigma_1\cdots\sigma_k,
\qquad
\sigma_i\in\{D,U\}.
$$

令：

$$
u(w)=u
$$

為 $U$ 次數。

形式 composition：

$$
F_w^{(m,r)}
=
\sigma_k\circ\cdots\circ\sigma_1.
$$

與 Collatz 一樣：

$$
F_w^{(m,r)}
$$

可在 $\mathbb Q$ 上形式計算；

真正 dynamics 還需 branch admissibility。

---

# 4. Generalized Finite-Word Affine Closure

## Theorem 4.1

對任意：

$$
w\in\{D,U\}^k,
$$

存在唯一：

$$
b_w^{(m,r)}\in\mathbb Z_{\ge0}
$$

使：

$$
\boxed{
F_w^{(m,r)}(x)
=
\frac{m^u x+b_w^{(m,r)}}{2^k}.
}
$$

---

# 5. Correction Recurrence

空字：

$$
b_\varepsilon=0.
$$

若 append $D$：

$$
\boxed{
b_{wD}=b_w.
}
$$

若 append $U$：

$$
U\left(
\frac{m^u x+b_w}{2^k}
\right)
=
\frac{
m^{u+1}x
+
m b_w
+
r2^k
}{
2^{k+1}
}.
$$

所以：

$$
\boxed{
b_{wU}
=
m b_w+r2^k.
}
$$

---

# 6. Closed Form

若 $U$ 出現在：

$$
1\le j_1<\cdots<j_u\le k,
$$

則第 $t$ 個 $U$ 注入：

$$
r2^{j_t-1},
$$

且後面剩：

$$
u-t
$$

個 $U$，每個再乘 $m$。

因此：

$$
\boxed{
b_w^{(m,r)}
=
r\sum_{t=1}^{u}
2^{j_t-1}m^{u-t}.
}
$$

Collatz：

$$
(m,r)=(3,1)
$$

立即恢復 Paper 02。

---

# 7. Count/Order Decomposition survives

固定：

$$
k,u,
$$

leading multiplier 永遠：

$$
\boxed{
\lambda_w
=
\frac{m^u}{2^k}.
}
$$

不依賴 $U,D$ 排列。

全部 order information 進入：

$$
\boxed{
b_w^{(m,r)}.
}
$$

所以：

$$
\boxed{
\text{counts determine slope;}
}
$$

$$
\boxed{
\text{order determines offset.}
}
$$

不是 $3x+1$ 特例。

---

# 8. Matrix Representation

定義：

$$
\boxed{
M_D
=
\begin{pmatrix}
1&0\\
0&2
\end{pmatrix},
}
$$

$$
\boxed{
M_U
=
\begin{pmatrix}
m&r\\
0&2
\end{pmatrix}.
}
$$

則：

$$
\boxed{
M_w
=
\begin{pmatrix}
m^u&b_w^{(m,r)}\\
0&2^k
\end{pmatrix}.
}
$$

finite-word composition 仍轉為 upper-triangular matrix multiplication。

---

# 9. Concatenation Law

若先執行 $w$，再執行 $v$，則：

$$
\boxed{
b_{wv}
=
m^{u(v)}b_w
+
2^{|w|}b_v.
}
$$

所以：

$$
\Omega(w)
=
(k,u,b)
$$

的 generalized composition：

$$
\boxed{
(k_w,u_w,b_w)
\circ
(k_v,u_v,b_v)
}
$$

仍具有 semidirect-type structure。

---

# 10. Residue Cylinder 仍然唯一

真正的關鍵不是 $m=3$。

而是：

$$
\boxed{
m\text{ odd}.
}
$$

所以：

$$
\gcd(m^u,2^k)=1.
$$

因此：

$$
m^u
$$

在：

$$
\mathbb Z/2^k\mathbb Z
$$

中為 unit。

---

# 11. Closed Residue Formula

若 $w$ admissible，

必須：

$$
m^u n+b_w
\equiv0
\pmod{2^k}.
$$

所以唯一：

$$
\boxed{
r_w
\equiv
-b_wm^{-u}
\pmod{2^k}.
}
$$

---

# 12. Word–Residue Bijection survives

更嚴格地，和 Paper 03 一樣用 induction：

假設：

$$
n=r_w+2^ka.
$$

則：

$$
T_{m,r}^k(n)
=
s_w+m^ua.
$$

因：

$$
m^u
$$

為 odd，

所以：

$$
T_{m,r}^k(n)\pmod2
=
s_w+a\pmod2.
$$

因此下一個 $D/U$ branch 再次只由：

$$
a\bmod2
$$

決定。

每個 parent cylinder 唯一分裂成兩個 modulo $2^{k+1}$ child cylinders。

所以：

$$
\boxed{
\{D,U\}^k
\longleftrightarrow
\mathbb Z/2^k\mathbb Z
}
$$

仍成立。

---

# 13. Generalized Local Atlas

定義：

$$
\Omega_w^{(m,r)}
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}.
$$

令：

$$
s_w
=
F_w^{(m,r)}(r_w).
$$

則：

$$
\boxed{
T_{m,r}^k(r_w+2^ka)
=
s_w+m^ua.
}
$$

所以：

$$
\boxed{
r_w+2^k\mathbb Z
\longleftrightarrow
s_w+m^u\mathbb Z.
}
$$

---

# 14. Generalized Identityization

source chart：

$$
\phi_w(n)
=
\frac{n-r_w}{2^k}.
$$

target chart：

$$
\psi_w(y)
=
\frac{y-s_w}{m^u}.
$$

則：

$$
\boxed{
\psi_w
\circ
T_{m,r}^k
\circ
\phi_w^{-1}
=
\operatorname{id}.
}
$$

所以：

$$
\boxed{
\text{local identity trivialization survives for all positive odd }m,r.
}
$$

---

# 15. Exact Recovery survives

若：

$$
y\equiv s_w\pmod{m^u},
$$

則：

$$
a=
\frac{y-s_w}{m^u}.
$$

所以：

$$
\boxed{
n
=
r_w
+
2^k
\frac{y-s_w}{m^u}.
}
$$

因此 fixed chart transport 仍然 lossless。

---

# 16. Fixed $(k,u)$ Order Extremes

對：

$$
r>0,
$$

把某個 $U$ 向右交換過一個 $D$：

$$
UD(x)
=
\frac{mx+r}{4},
$$

而：

$$
DU(x)
=
\frac{mx+2r}{4}.
$$

所以：

$$
DU(x)-UD(x)
=
\frac r4>0.
$$

因此 moving $U$ right increases correction。

---

# 17. Minimum Correction

所有 $U$ 最左：

$$
U^uD^{k-u}.
$$

其 correction：

$$
b_{\min}
=
r
\sum_{t=1}^{u}
2^{t-1}m^{u-t}.
$$

有限等比和：

$$
\boxed{
b_{\min}
=
r\frac{m^u-2^u}{m-2}.
}
$$

---

# 18. Maximum Correction

所有 $U$ 最右：

$$
D^{k-u}U^u.
$$

所以：

$$
\boxed{
b_{\max}
=
r\,2^{k-u}
\frac{m^u-2^u}{m-2}.
}
$$

因此：

$$
\boxed{
r\frac{m^u-2^u}{m-2}
\le
b_w
\le
r2^{k-u}\frac{m^u-2^u}{m-2}.
}
$$

---

# 19. $m=1$ 需要單獨理解

當：

$$
m=1,
$$

公式：

$$
\frac{m^u-2^u}{m-2}
$$

仍可直接代入：

$$
\frac{1-2^u}{-1}
=
2^u-1.
$$

所以：

$$
b_{\min}
=
r(2^u-1).
$$

沒有奇點。

只是此時 skeleton：

$$
\lambda_w=\frac1{2^k}
$$

與 $u$ 無關。

---

# 20. Exact Descent Criterion

由：

$$
T_{m,r}^k(n)
=
\frac{m^un+b_w}{2^k},
$$

有：

$$
T_{m,r}^k(n)<n
$$

iff：

$$
\boxed{
b_w<(2^k-m^u)n.
}
$$

---

# 21. Contracting Skeleton

若：

$$
\boxed{
m^u<2^k,
}
$$

則存在 finite threshold：

$$
\boxed{
\theta_w
=
\left\lfloor
\frac{b_w}{2^k-m^u}
\right\rfloor+1
}
$$

使：

$$
n\ge\theta_w
$$

時：

$$
\boxed{
T_{m,r}^k(n)<n.
}
$$

---

# 22. Uniform Expansion

若：

$$
m^u>2^k,
$$

因：

$$
b_w\ge0,
$$

對任何 positive admissible：

$$
n,
$$

都有：

$$
\boxed{
T_{m,r}^k(n)>n.
}
$$

因此 generalized family 仍有 strict finite-word two-sided classification。

---

# 23. $r$ 不移動 Skeleton Boundary

注意：

$$
m^u\lessgtr2^k
$$

完全沒有：

$$
r.
$$

所以：

$$
\boxed{
r
\text{ controls correction and finite thresholds, not the asymptotic skeleton side}.
}
$$

這是 generalized family 很重要的參數分工。

---

# 24. Generalized Critical Fraction

對：

$$
m>1,
$$

定義：

$$
\boxed{
\alpha_m
=
\frac{\ln2}{\ln m}.
}
$$

則：

$$
m^u<2^k
$$

iff：

$$
\boxed{
\frac uk<\alpha_m.
}
$$

---

# 25. $\alpha_m$ 的無理性

若 odd：

$$
m>1
$$

且：

$$
\alpha_m=\frac pq
\in\mathbb Q,
$$

則：

$$
m^p=2^q.
$$

左側為 odd，

右側為 even，

矛盾。

因此：

$$
\boxed{
\alpha_m\notin\mathbb Q
}
$$

對所有 odd $m>1$。

所以不存在 nonempty neutral-slope word。

---

# 26. Generalized Binomial Cylinder Law

length-$k$ words 中，

恰含 $u$ 個 $U$ 的數量：

$$
\binom ku.
$$

所以 contracting cylinder count：

$$
\boxed{
A_k(m)
=
\sum_{u=0}^{\lfloor\alpha_mk\rfloor}
\binom ku.
}
$$

比例：

$$
\boxed{
P_k(m)
=
\frac{A_k(m)}{2^k}.
}
$$

---

# 27. $m=1$：完全 Contracting Skeleton

若：

$$
m=1,
$$

則對任意 nonempty word：

$$
1=m^u<2^k.
$$

所以：

$$
\boxed{
P_k(1)=1
}
$$

對所有：

$$
k\ge1.
$$

注意這只說 finite-word skeleton。

不同 $r$ 仍可造成 finite correction、cycles 或其他 global structure。

---

# 28. $m=3$：Collatz Regime

$$
\alpha_3
=
\frac{\ln2}{\ln3}
\approx0.63093
>
\frac12.
$$

因此由二項分布大數律：

$$
\boxed{
P_k(3)\to1.
}
$$

這就是 Paper 05 的 Collatz cylinder law。

---

# 29. $m=5$

$$
\alpha_5
=
\frac{\ln2}{\ln5}
\approx0.43068
<
\frac12.
$$

所以：

$$
\boxed{
P_k(5)\to0.
}
$$

也就是 length-$k$ words 中，contracting-skeleton cylinders 的比例反而趨零。

---

# 30. odd $m\ge5$

對：

$$
m\ge5,
$$

有：

$$
\ln m>\ln4=2\ln2.
$$

所以：

$$
\frac{\ln2}{\ln m}
<
\frac12.
$$

故：

$$
\boxed{
P_k(m)\to0
}
$$

對所有 odd：

$$
m\ge5.
$$

---

# 31. Continuous Phase Boundary

考察：

$$
\alpha_m=\frac12.
$$

解：

$$
\frac{\ln2}{\ln m}
=
\frac12.
$$

所以：

$$
\ln m=2\ln2=\ln4.
$$

得到：

$$
\boxed{
m_c=4.
}
$$

因此：

$$
\boxed{
m<4
\Rightarrow
\text{typical word lies on contracting side},
}
$$

$$
\boxed{
m>4
\Rightarrow
\text{typical word lies on expanding side}.
}
$$

在 odd integer family 中：

- $m=3$ 位於 contraction regime；
- 下一個 $m=5$ 已跨到 expansion regime。

---

# 32. 為什麼 $3$ 特別？

這不需要神秘化。

binomial center：

$$
u/k\approx1/2.
$$

典型 skeleton multiplier：

$$
\left(
\frac{\sqrt m}{2}
\right)^k.
$$

所以：

$$
\boxed{
\frac{\sqrt m}{2}<1
\iff
m<4.
}
$$

對：

$$
m=3,
$$

典型 factor：

$$
\frac{\sqrt3}{2}<1.
$$

對：

$$
m=5,
$$

$$
\frac{\sqrt5}{2}>1.
$$

所以 $3$ 恰好是 odd multipliers 中最後一個落在典型 contraction side 的非平凡值。

---

# 33. $r$ 只改 Finite Geometry

對 fixed：

$$
m,k,u,w,
$$

correction：

$$
b_w^{(m,r)}
$$

對 $r$ 線性：

$$
\boxed{
b_w^{(m,r)}
=
r\,b_w^{(m,1)}.
}
$$

所以 threshold：

$$
\theta_w
$$

大致隨 $r$ 線性移動。

但：

$$
\alpha_m
$$

完全不變。

因此：

$$
\boxed{
m=\text{phase parameter},
\qquad
r=\text{finite correction parameter}.
}
$$

---

# 34. Generalized Log Drift

對：

$$
n>0,
$$

$$
T_{m,r}^k(n)
=
\frac{m^un+b_w}{2^k}.
$$

取 log：

$$
\boxed{
\ln\frac{T_{m,r}^k(n)}{n}
=
u\ln m
-
k\ln2
+
\ln\left(
1+\frac{b_w}{m^un}
\right).
}
$$

所以：

$$
\boxed{
\text{additive core}=u\ln m-k\ln2,
}
$$

$$
\boxed{
\text{correction}
=
\ln\left(
1+\frac{b_w}{m^un}
\right).
}
$$

Series A 的 corrected additivization 在 generalized Collatz family 中仍完整成立。

---

# 35. Accelerated $mx+r$ Map

對 odd $n$ 可定義：

$$
\boxed{
S_{m,r}(n)
=
\frac{mn+r}
{2^{v_2(mn+r)}}.
}
$$

因 $m,r,n$ 都 odd，

numerator even。

因此 generalized valuation language 亦自然存在：

$$
\kappa_i
=
v_2(mn_{i-1}+r).
$$

---

# 36. Generalized Valuation Skeleton

經 $q$ 個 odd-to-odd cycles，

leading multiplier 變成：

$$
\boxed{
\frac{m^q}{2^K}.
}
$$

所以 valuation boundary：

$$
\boxed{
K/q>\log_2 m.
}
$$

這是 Paper 06：

$$
K/q>\log_2 3
$$

的直接一般化。

---

# 37. One-Step Valuation Density 仍有幾何結構

因 odd $m$ 在：

$$
\mathbb Z/2^{j+1}\mathbb Z
$$

中是 unit。

要求：

$$
v_2(mn+r)=j
$$

等價於一條唯一 odd residue congruence modulo：

$$
2^{j+1}.
$$

所以在 odd residue classes 中仍有：

$$
\boxed{
\delta(\kappa=j)=2^{-j}.
}
$$

因此 one-step residue mean：

$$
\boxed{
\mathbb E_{\mathrm{res}}\kappa=2
}
$$

與 $m,r$ 無關，只要二者 odd。

---

# 38. 因而 Generalized Skeleton Mean

one-step accelerated skeleton：

$$
\ln m-\kappa\ln2.
$$

residue ensemble mean：

$$
\boxed{
\ln m-2\ln2
=
\ln\frac m4.
}
$$

所以平均 skeleton sign 也在：

$$
\boxed{
m=4
}
$$

翻轉。

這與 binomial cylinder phase boundary 完全一致。

---

# 39. 兩條不同推導得到同一臨界

### Finite parity-word combinatorics：

$$
u/k\approx1/2
$$

導致：

$$
\frac{\sqrt m}{2}\lessgtr1.
$$

### Accelerated valuation residue mean：

$$
\mathbb E\kappa=2
$$

導致：

$$
\frac m4\lessgtr1.
$$

兩者都給：

$$
\boxed{
m_c=4.
}
$$

這是一個內部交叉驗證。

---

# 40. 與更一般 $p,q,r$ 文獻的交叉

Gonçalves–Greenfeld–Madrid 研究一類更一般的 Collatz-like maps：

- divisible by $p$ 時除以 $p$；
- 其他 residue classes 使用 $qN+r(j)$；
- 再研究其 Syracuse acceleration。

其 almost-all theorem 的重要條件之一：

$$
\boxed{
q<p^{p/(p-1)}.
}
$$

對 parity case：

$$
p=2,
$$

變成：

$$
\boxed{
q<4.
}
$$

若把本文：

$$
q=m,
$$

則恰好得到同一臨界：

$$
\boxed{
m<4.
}
$$

---

# 41. 但兩個 $m<4$ 不是同一定理

本文證：

$$
\boxed{
P_k(m)\to1
}
$$

只是一個 finite-word / residue-cylinder combinatorial theorem。

Gonçalves–Greenfeld–Madrid 的 theorem 則處理 actual generalized Collatz orbits 的 almost-bounded behavior，並需要更深 analytic/probabilistic machinery。

所以：

$$
\boxed{
\text{same critical constant}
\neq
\text{same mathematical result}.
}
$$

其吻合應視為 structural consistency check。

---

# 42. 更廣 Collatz-like Maps 的危險

一般 Collatz-like map 可寫：

$$
T(N)=a_NN+b_N
$$

其中：

$$
a_N,b_N
$$

週期性依賴 residue class。

既有文獻還指出，Conway 的 FRACTRAN 與這類系統相關，足夠一般的 Collatz-like family 可以模擬通用計算，因此某些全域 orbit questions 甚至是不可判定的。

所以：

$$
\boxed{
\text{不能期待 RCOT 的局部簡化自動產生所有 Collatz-like systems 的 global classification}.
}
$$

這也再次說明本文必須限制在特定 affine parity kernel。

---

# 43. RCOT Parity Kernel

本文把以下條件稱為 **RCOT parity kernel**：

1. state domain 為 positive integers；
2. branch domain由 parity 決定；
3. branch maps 為 scalar affine maps；
4. common denominator 為 2；
5. odd multiplier $m$ 是 modulo $2^k$ 的 unit；
6. translation $r$ 保持 odd branch integer-valued；
7. scalar coefficient multiplication commutative。

在此 domain 中，以下全部成立：

$$
\boxed{
\text{finite affine closure},
}
$$

$$
\boxed{
\text{count/order decomposition},
}
$$

$$
\boxed{
\text{unique residue cylinder},
}
$$

$$
\boxed{
\text{local identityization},
}
$$

$$
\boxed{
\text{exact inverse recovery},
}
$$

$$
\boxed{
\text{binomial cylinder law}.
}
$$

---

# 44. 哪些是 Collatz-specific？

Collatz-specific：

$$
m=3,\qquad r=1.
$$

因此具體：

$$
\alpha=\frac{\ln2}{\ln3},
$$

$$
2^k\leftrightarrow3^u,
$$

$$
R_\kappa(t)=\frac{2^\kappa t-1}{3},
$$

以及：

$$
\frac{4^j-1}{3}
$$

等 family。

---

# 45. 哪些不是 Collatz-specific？

以下全部其實屬於 generalized odd-$m,r$ RCOT：

- finite-word affine closure；
- upper-triangular matrix representation；
- word/residue bijection mod $2^k$；
- source cylinder ↔ target $m^u$-progression；
- quotient-label identityization；
- exact recovery；
- branch-order correction；
- $m^u\lessgtr2^k$ finite-word phase boundary；
- generalized binomial cylinder law；
- valuation run-length compression。

所以前六篇其實揭示了一個比 Collatz 更大的局部算術類別。

---

# 46. Generalized Order Correction Width

由：

$$
b_{\max}
=
2^{k-u}b_{\min},
$$

有：

$$
\boxed{
W_{k,u}^{(m,r)}
=
r
\left(2^{k-u}-1\right)
\frac{m^u-2^u}{m-2}.
}
$$

所以 branch-order sensitivity：

- 隨 $r$ 線性放大；
- 隨 $k-u$ 增長；
- 受 $m^u-2^u$ 控制。

這提供 generalized affine correction 的 exact finite width。

---

# 47. Order-Uniform Threshold

contracting：

$$
m^u<2^k.
$$

使用最大 correction：

$$
b_{\max}
=
r2^{k-u}\frac{m^u-2^u}{m-2},
$$

得到：

$$
\boxed{
\Theta_{k,u}^{(m,r)}
=
\left\lfloor
\frac{
r2^{k-u}(m^u-2^u)
}{
(m-2)(2^k-m^u)
}
\right\rfloor+1.
}
$$

則所有 fixed $(k,u)$ words：

$$
n\ge\Theta_{k,u}^{(m,r)}
$$

時都 strict descent。

所以 generalized family 同樣可以把完整 word 壓成 conservative $(k,u)$ certificate。

---

# 48. $m=3$ 為何是特殊但不是神秘

在 odd multiplier family：

$$
1,3,5,7,\ldots,
$$

$m=1$ 是近乎純 contraction 的退化情況。

真正第一個具有 multiplicative growth 的 nontrivial odd multiplier：

$$
m=3
$$

仍位於：

$$
m<4.
$$

下一個：

$$
m=5
$$

已跨越 phase boundary。

所以 Collatz 的 $3$ 位於一個非常窄的參數窗口：

$$
\boxed{
\text{nontrivial growth}
+
\text{typical finite-word contraction}.
}
$$

這可能是 $3x+1$ 系統既簡單又長期呈現下降傾向的重要結構原因之一。

---

# 49. 但 $m=3$ 的 Cylinder Density 仍不是 Convergence

即使：

$$
P_k(3)\to1,
$$

仍然不能推出所有 $3x+r$ systems global bounded。

不同 $r$ 可以改變：

- periodic points；
- cycles；
- finite thresholds；
- chart transitions；
- orbit merging pattern。

因此：

$$
\boxed{
\text{skeleton phase}
\neq
\text{complete global dynamics}.
}
$$

---

# 50. 本文主要定理總結

## Theorem A — Generalized Affine Closure

$$
\boxed{
F_w^{(m,r)}(x)
=
\frac{m^ux+b_w^{(m,r)}}{2^k}.
}
$$

## Theorem B — Correction Closed Form

$$
\boxed{
b_w^{(m,r)}
=
r\sum_{t=1}^{u}
2^{j_t-1}m^{u-t}.
}
$$

## Theorem C — Unique Residue Cylinder

$$
\boxed{
r_w
\equiv
-b_wm^{-u}
\pmod{2^k}.
}
$$

## Theorem D — Local Identityization

$$
\boxed{
T_{m,r}^k(r_w+2^ka)
=
s_w+m^ua,
}
$$

hence：

$$
\boxed{
\psi_wT_{m,r}^k\phi_w^{-1}
=
\operatorname{id}.
}
$$

## Theorem E — Generalized Contraction Boundary

對 odd $m>1$：

$$
\boxed{
m^u<2^k
\iff
u/k<\ln2/\ln m.
}
$$

對 $m=1$，任意 nonempty word 都滿足 $m^u=1<2^k$，須獨立處理而不能代入 $\ln m$ 分母。

## Theorem F — Generalized Binomial Cylinder Law

對 odd $m>1$：

$$
\boxed{
P_k(m)
=
2^{-k}
\sum_{u=0}^{\lfloor k\ln2/\ln m\rfloor}
\binom ku.
}
$$

而：

$$
\boxed{P_k(1)=1.}
$$

## Theorem G — Cylinder Phase Classification

$$
\boxed{
P_k(3)\to1,
}
$$

而對 odd：

$$
\boxed{
m\ge5
\Rightarrow
P_k(m)\to0.
}
$$

## Theorem H — Critical Parameter

$$
\boxed{
m_c=4.
}
$$

---

# 51. 結論

前六篇從 Collatz 出發建立：

$$
\text{finite word}
\to
\text{affine operator}
\to
\text{residue cylinder}
\to
\text{identity chart}
\to
\text{contraction law}
\to
\text{valuation language}.
$$

本文顯示這條鏈的核心部分並不依賴：

$$
3,\qquad1.
$$

只要：

$$
m,r
$$

為正奇整數，

整個 local RCOT structure 仍然成立：

$$
\boxed{
T_{m,r}^k(r_w+2^ka)
=
s_w+m^ua.
}
$$

因此：

$$
\boxed{
\text{Collatz is one member of a larger residue-class affine translation family}.
}
$$

而真正由 $m$ 控制的 phase boundary：

$$
\boxed{
m_c=4
}
$$

在三種不同層次中同時出現：

1. binomial parity-cylinder majority；
2. accelerated one-step valuation mean；
3. 更一般 $p,q,r$ almost-all theory 在 $p=2$ 時的已知 analytic condition。

這種一致性不等於全域證明，但清楚指出：

$$
\boxed{
m=3
}
$$

位於 generalized family 中一個特殊的 subcritical regime。

下一篇將不再只換數字。

我們將真正換**代數**：

$$
\mathbb Z
\to
\text{commutative rings}
\to
\text{zero divisors}
\to
\text{unordered fields}
\to
\text{matrices / noncommutative algebras}
\to
\text{Möbius maps}
\to
\text{nonlinear polynomials}.
$$

目標是回答：

> RCOT 的定理究竟在哪一層第一次斷裂？斷的是 residue uniqueness、exact recovery、count/order decomposition，還是 finite-dimensional closure 本身？

---

# 參考文獻

1. Felipe Gonçalves, Rachel Greenfeld, Jose Madrid, *Generalized Collatz Maps with Almost Bounded Orbits*, arXiv:2111.06170.
2. Alec Edgington, *The autoconjugacy of a generalized Collatz map*, arXiv:1206.0553.
3. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562; Forum of Mathematics, Pi 10 (2022).
4. John H. Conway, work on generalized Collatz-like iterations and FRACTRAN, as discussed in the generalized Collatz literature.
5. Matthews & Watts, generalized Syracuse / residue-class-wise affine mappings, as discussed in Gonçalves–Greenfeld–Madrid.
6. Collatz Operation Translation Series — Papers 02–06.

---

## 下一篇

**Paper 08 —《代數判定域與結構斷裂定理》**

核心任務：

1. 從 $\mathbb Z/\mathbb Q$ 推到一般交換整域；
2. 檢查 multiplier 非 unit 時 residue uniqueness 如何分裂；
3. 檢查 zero divisor 如何破壞 exact inverse recovery；
4. 檢查 $\mathbb C$、$p$-adic domain 中「下降」語義如何改變；
5. 進入 matrix / noncommutative algebra，證明 order dependence 進入 leading operator；
6. 推到 Möbius transformations，辨認 finite-dimensional closure 尚存但 progression transport 消失；
7. 推到 degree $>1$ polynomial maps，辨認 fixed-dimensional affine closure 的斷裂。
