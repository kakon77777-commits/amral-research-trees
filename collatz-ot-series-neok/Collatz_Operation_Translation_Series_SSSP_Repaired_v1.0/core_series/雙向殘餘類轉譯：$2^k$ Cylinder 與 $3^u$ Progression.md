# 雙向殘餘類轉譯：$2^k$ Cylinder 與 $3^u$ Progression
## ——從 Collatz Local Affine Atlas 到 Exact Inverse Fiber、Odd Skeleton 與雙螺旋重構

**English Title:** *Bidirectional Residue-Class Translation: From $2^k$ Cylinders to $3^u$ Progressions in the Collatz Local Affine Atlas*

**作者：** Neo.K  
**機構：** 一言諾科技有限公司（EveMissLab）  
**系列：** Collatz Operation Translation Series — Paper 04  
**版本：** v0.1  
**日期：** 2026-08-10

---

## 摘要

Paper 03 已證明，對 modified Collatz map

$$
T(n)=
\begin{cases}
n/2,&n\equiv0\pmod2,\\[2mm]
(3n+1)/2,&n\equiv1\pmod2,
\end{cases}
$$

每個長度 $k$ 的 admissible parity word $w$ 對應唯一 source residue cylinder

$$
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0},
$$

且若 $u=u(w)$、$m_w=T^k(r_w)$，則

$$
\boxed{
T^k(r_w+2^ka)
=
m_w+3^ua.
}
$$

本文將此單向公式提升為完整的**雙向精確殘餘類轉譯**。

在全整數仿射 extension 上，定義

$$
\mathcal C_w=r_w+2^k\mathbb Z,
$$

$$
\mathcal P_w=m_w+3^u\mathbb Z.
$$

本文證明：

$$
\boxed{
F_w:\mathcal C_w\overset{\sim}{\longrightarrow}\mathcal P_w
}
$$

為雙射，且其 inverse 為

$$
\boxed{
F_w^{-1}(y)
=
r_w
+
2^k\frac{y-m_w}{3^u},
\qquad
y\equiv m_w\pmod{3^u}.
}
$$

因此 fixed-word Collatz transport 可被理解為：

$$
\boxed{
r_w+2^k\mathbb Z
\;\longleftrightarrow\;
m_w+3^u\mathbb Z,
}
$$

而雙方共享同一個 exact quotient coordinate

$$
a.
$$

source 端以 $2^k$ 為 lattice spacing，target 端以 $3^u$ 為 lattice spacing；在 chart coordinate 中，forward 與 inverse 都只是

$$
a\leftrightarrow a.
$$

本文將此結構稱為 **Bidirectional Residue Transport**。

在正整數 Collatz domain 中，若取 canonical representative

$$
0\le r_w<2^k,
$$

則合法 quotient coordinate 下界為

$$
a_{\min}(w)
=
\begin{cases}
1,&r_w=0,\\
0,&r_w>0.
\end{cases}
$$

所以真正的 positive source/image 為

$$
\Omega_w
=
\{
r_w+2^ka:a\ge a_{\min}(w)
\},
$$

$$
\Gamma_w
=
\{
m_w+3^ua:a\ge a_{\min}(w)
\}.
$$

固定 chart 中的 inverse 因而仍是 exact、single-valued、lossless。

本文接著把作者早期「雙螺旋」研究重新整理為兩個互補層級：

1. **modified-map finite-word inverse transport**：由 $2^k$ source cylinder 與 $3^u$ target progression 構成；
2. **accelerated odd-map inverse fibers**：對
   $$
   S(n)=\frac{3n+1}{2^{v_2(3n+1)}}
   $$
   定義
   $$
   R_\kappa(t)=\frac{2^\kappa t-1}{3}.
   $$

若 $t$ 為正奇數，則 $R_\kappa(t)$ 是 $t$ 的合法 odd predecessor 當且僅當

$$
\boxed{
2^\kappa t\equiv1\pmod3.
}
$$

因此：

- 若 $t\equiv1\pmod3$，合法 $\kappa$ 必為偶數；
- 若 $t\equiv2\pmod3$，合法 $\kappa$ 必為奇數；
- 若 $3\mid t$，不存在 accelerated odd predecessor。

特別地，對 terminal state $t=1$：

$$
\kappa=2j
$$

給出

$$
\boxed{
R_{2j}(1)
=
\frac{4^j-1}{3}.
}
$$

因此作者舊研究中的

$$
M_j=\frac{4^j-1}{3}
$$

不再需要被解讀為獨立的「高速公路神秘級數」；它精確地就是 accelerated odd map 中 terminal state $1$ 的 valuation-labelled inverse fiber。數字 $5$ 則只是

$$
R_4(1)=5,
$$

而 $5\cdot2^q$ 是其在 ordinary Collatz inverse structure 中的 even $2$-ray。

本文亦重新整理 odd skeleton。任意正整數唯一表示為

$$
n=2^{v_2(n)}\operatorname{oddcore}(n),
$$

所以 ordinary Collatz inverse coverage 可拆為：

$$
\boxed{
\text{odd inverse skeleton}
+
\text{even }2\text{-rays}.
}
$$

在 accelerated odd map 上，所有節點均為 odd states；inverse fibers $R_\kappa(t)$ 直接描述 odd skeleton 的 edge labels。

本文特別強調三種不同的「反向」不能混淆：

- fixed-word local inverse；
- inverse-tree predecessor relation；
- global inverse coverage。

前兩者可以 exact；第三者仍然等價於 Collatz 全域問題。換言之：

$$
\boxed{
\text{local invertibility}
\not\Rightarrow
\text{global inverse-tree coverage}.
}
$$

本文因此把早期「雙螺旋」從視覺／圖論方法重新定義為一個嚴格的算術架構：

$$
\boxed{
\text{forward }2^k\text{-cylinder refinement}
\quad\leftrightarrow\quad
\text{backward }3^u\text{-progression / valuation fiber}.
}
$$

**關鍵詞：** Collatz conjecture、inverse iteration、residue class、$2$-adic cylinder、$3$-progression、accelerated Collatz、valuation fiber、odd skeleton、bidirectional transport、exact recovery

---

# 1. 問題：Paper 03 的 forward transport 能否真正反轉？

Paper 03 已得到：

$$
\boxed{
T^k(r_w+2^ka)
=
m_w+3^ua.
}
$$

這條式子已經暗示：

- source quotient label 是 $a$；
- target quotient label也是 $a$。

所以最自然的問題是：

> 若只知道 target $y$ 與 fixed chart $w$，是否能精確還原 source $n$？

答案是肯定的。

---

# 2. 全整數 Affine Extension

為避免正整數邊界干擾代數結構，先在：

$$
\mathbb Z
$$

上考慮 fixed-word affine map：

$$
F_w(x)
=
\frac{3^ux+b_w}{2^k}.
$$

定義 source cylinder：

$$
\boxed{
\mathcal C_w
=
r_w+2^k\mathbb Z.
}
$$

由 Paper 03：

$$
r_w
\equiv
-b_w3^{-u}
\pmod{2^k},
$$

所以對：

$$
x\in\mathcal C_w,
$$

$F_w(x)$ 必為整數。

---

# 3. Target Progression

令：

$$
m_w=F_w(r_w).
$$

對：

$$
x=r_w+2^ka,
$$

有：

$$
F_w(x)
=
m_w+3^ua.
$$

因此 image 精確為：

$$
\boxed{
\mathcal P_w
=
m_w+3^u\mathbb Z.
}
$$

所以：

$$
\boxed{
F_w(\mathcal C_w)=\mathcal P_w.
}
$$

---

# 4. Bidirectional Residue Transport Theorem

## 定理 4.1

對任意 finite parity word $w$：

$$
F_w:
\mathcal C_w
\to
\mathcal P_w
$$

為雙射。

其 inverse：

$$
\boxed{
F_w^{-1}(y)
=
r_w
+
2^k
\frac{y-m_w}{3^u}.
}
$$

### 證明

若：

$$
y\in\mathcal P_w,
$$

則唯一存在：

$$
a\in\mathbb Z
$$

使：

$$
y=m_w+3^ua.
$$

定義：

$$
x=r_w+2^ka.
$$

則：

$$
F_w(x)
=
m_w+3^ua
=
y.
$$

唯一性來自 $3^u\neq0$ 與 source coordinate $a$ 唯一。

證畢。

---

# 5. Inverse Legality Congruence

由：

$$
y=m_w+3^ua,
$$

可得：

$$
\boxed{
y\equiv m_w\pmod{3^u}.
}
$$

反之若：

$$
y\equiv m_w\pmod{3^u},
$$

則：

$$
a=\frac{y-m_w}{3^u}\in\mathbb Z
$$

並給出唯一 source：

$$
x=r_w+2^ka.
$$

因此 fixed-word inverse legality 恰好是：

$$
\boxed{
y\equiv m_w\pmod{3^u}.
}
$$

---

# 6. Source 與 Target 的雙殘餘類結構

source：

$$
\boxed{
x\equiv r_w\pmod{2^k}.
}
$$

target：

$$
\boxed{
y\equiv m_w\pmod{3^u}.
}
$$

所以一張 chart 同時具有：

$$
\boxed{
(2^k,r_w)
}
$$

與：

$$
\boxed{
(3^u,m_w)
}
$$

兩套 residual metadata。

可記成：

$$
\boxed{
\mathcal R(w)
=
(2^k,r_w;3^u,m_w).
}
$$

---

# 7. Quotient Coordinate 守恆

source coordinate：

$$
a
=
\frac{x-r_w}{2^k}.
$$

target coordinate：

$$
a
=
\frac{y-m_w}{3^u}.
$$

因此：

$$
\boxed{
\frac{x-r_w}{2^k}
=
\frac{y-m_w}{3^u}.
}
$$

這是 fixed-word transport 的核心守恆式。

它不是「數值 $x$ 不變」。

真正不變的是：

$$
\boxed{
\text{chart quotient label }a.
}
$$

---

# 8. Cross-Multiplied Exact Relation

上一式等價於：

$$
\boxed{
3^u(x-r_w)
=
2^k(y-m_w).
}
$$

此式完全不需要除法。

因此在 exact-integer backend 中可以直接作為：

$$
\boxed{
\text{transport certificate}.
}
$$

它也提供一種不依賴浮點數的雙向一致性檢查。

---

# 9. Positive-Integer Domain

Paper 03 的真正 Collatz domain 是：

$$
\Omega_w
=
\mathcal C_w\cap\mathbb Z_{>0}.
$$

取 canonical：

$$
0\le r_w<2^k.
$$

若：

$$
r_w>0,
$$

則：

$$
a\ge0
$$

就保證：

$$
r_w+2^ka>0.
$$

若：

$$
r_w=0,
$$

則必須：

$$
a\ge1.
$$

因此定義：

$$
\boxed{
a_{\min}(w)
=
\begin{cases}
1,&r_w=0,\\
0,&r_w>0.
\end{cases}
}
$$

---

# 10. Positive Source / Image Theorem

所以：

$$
\boxed{
\Omega_w
=
\{
r_w+2^ka:
a\ge a_{\min}(w)
\}.
}
$$

其正整數 image：

$$
\boxed{
\Gamma_w
=
\{
m_w+3^ua:
a\ge a_{\min}(w)
\}.
}
$$

並且：

$$
\boxed{
T^k:
\Omega_w
\overset{\sim}{\longrightarrow}
\Gamma_w
}
$$

仍是雙射。

因此 fixed chart 上：

$$
\boxed{
\text{positive-domain exact recovery}
}
$$

成立。

---

# 11. 例：$w=U$

由 Paper 03：

$$
r_U=1,
$$

$$
m_U=2,
$$

$$
k=1,
\qquad
u=1.
$$

因此：

$$
\boxed{
1+2a
\longleftrightarrow
2+3a.
}
$$

inverse：

$$
\boxed{
n
=
1+2\frac{y-2}{3}.
}
$$

合法 target：

$$
\boxed{
y\equiv2\pmod3.
}
$$

---

# 12. modified Collatz 的單步 inverse branches

由：

$$
T(n)=y.
$$

有兩種可能。

## even predecessor

若 $n$ even：

$$
n/2=y
$$

所以：

$$
\boxed{
n=2y.
}
$$

此 predecessor 對所有：

$$
y>0
$$

存在。

---

## odd predecessor

若 $n$ odd：

$$
\frac{3n+1}{2}=y.
$$

所以：

$$
\boxed{
n=\frac{2y-1}{3}.
}
$$

要成為整數：

$$
2y-1\equiv0\pmod3.
$$

即：

$$
\boxed{
y\equiv2\pmod3.
}
$$

此時：

$$
y=3q+2
$$

給：

$$
n=2q+1,
$$

自動為 odd。

因此 modified-map inverse relation：

$$
\boxed{
T^{-1}(y)
=
\{2y\}
\cup
\left\{
\frac{2y-1}{3}
:
y\equiv2\pmod3
\right\}.
}
$$

---

# 13. 與 original Collatz inverse branch 的關係

original map odd step：

$$
n\mapsto3n+1.
$$

給 target $y$ 的 odd predecessor：

$$
n=\frac{y-1}{3}.
$$

其合法條件為：

$$
\boxed{
y\equiv4\pmod6.
}
$$

modified map 把 odd step 後必然的一次除 2 合併，

所以 target 改成：

$$
y_{\mathrm{mod}}
=
\frac{y_{\mathrm{orig}}}{2}.
$$

因此：

$$
y_{\mathrm{orig}}\equiv4\pmod6
$$

正好等價於：

$$
y_{\mathrm{mod}}\equiv2\pmod3.
$$

所以兩種 inverse condition 只是不同時間取樣下的同一算術限制。

---

# 14. 早期「分支點」的重新定位

舊研究稱 original target：

$$
y\equiv4\pmod6
$$

為可產生 odd predecessor 的 branch point。

在 modified map 中更自然寫成：

$$
\boxed{
y\equiv2\pmod3.
}
$$

因此 branch sparsity 可以視為：

$$
\boxed{
\text{target-domain inverse legality}.
}
$$

這比「小數篩選」更精確，也完全不依賴十進制。

---

# 15. fixed-word inverse 與 inverse tree 的差異

fixed-word inverse：

$$
F_w^{-1}:
\mathcal P_w
\to
\mathcal C_w
$$

是單值的。

但 global Collatz inverse：

$$
T^{-1}(y)
$$

一般是：

- 一個 predecessor；
- 或兩個 predecessors。

所以：

$$
\boxed{
\text{fixed itinerary removes inverse branching}.
}
$$

這是一個重要的 local simplification。

---

# 16. 為什麼固定字後 inverse 會單值？

因為 global inverse branching 來自：

> 不知道 predecessor 的 branch history。

一旦 $w$ 固定，

branch history 已知，

所以所有 branching decision 被消除。

因此：

$$
\boxed{
\text{inverse ambiguity}
=
\text{itinerary uncertainty}.
}
$$

在 fixed-word chart 中 itinerary uncertainty 為零，

inverse 因而 exact single-valued。

---

# 17. Odd Core

任意：

$$
n\in\mathbb Z_{>0}
$$

唯一表示：

$$
\boxed{
n=2^{v_2(n)}m,
\qquad
m\text{ odd}.
}
$$

定義：

$$
\boxed{
\operatorname{oddcore}(n)
=
\frac{n}{2^{v_2(n)}}.
}
$$

因此所有正整數被分成 disjoint $2$-rays：

$$
\boxed{
\mathbb Z_{>0}
=
\bigsqcup_{m\text{ odd}}
\{2^qm:q\ge0\}.
}
$$

---

# 18. Inverse Tree 的 Odd Skeleton

若某個 odd state：

$$
m
$$

已在 inverse convergence tree 中，

則：

$$
m,2m,4m,8m,\ldots
$$

全部自動在 tree 中。

因此 global inverse coverage 等價於 odd coverage：

$$
\boxed{
\text{all positive integers covered}
\iff
\text{all positive odd integers covered}.
}
$$

所以 inverse tree 可分成：

$$
\boxed{
\text{odd skeleton}
+
\text{even }2\text{-rays}.
}
$$

這個舊研究觀察在本文中被保留。

---

# 19. Accelerated Odd Map

對 positive odd $n$ 定義：

$$
\boxed{
S(n)
=
\frac{3n+1}{2^{\kappa(n)}},
}
$$

其中：

$$
\boxed{
\kappa(n)
=
v_2(3n+1).
}
$$

因為：

$$
3n+1
$$

為 even，

所以：

$$
\kappa(n)\ge1.
$$

而：

$$
S(n)
$$

再次為 odd。

因此：

$$
S:
\mathbb Z_{>0}^{\mathrm{odd}}
\to
\mathbb Z_{>0}^{\mathrm{odd}}.
$$

---

# 20. Accelerated Inverse Fiber

給定 odd target：

$$
t,
$$

若：

$$
S(n)=t,
$$

則存在：

$$
\kappa\ge1
$$

使：

$$
3n+1
=
2^\kappa t.
$$

所以：

$$
\boxed{
n
=
R_\kappa(t)
=
\frac{2^\kappa t-1}{3}.
}
$$

這就是 valuation-labelled inverse candidate。

---

# 21. Inverse Fiber Legality Theorem

## 定理 21.1

對 positive odd $t$、$\kappa\ge1$，

$$
R_\kappa(t)
=
\frac{2^\kappa t-1}{3}
$$

是合法 positive odd predecessor 當且僅當：

$$
\boxed{
2^\kappa t\equiv1\pmod3.
}
$$

### 證明

若 congruence 成立，

numerator 可被 3 整除。

因：

$$
2^\kappa t
$$

為 even，

numerator：

$$
2^\kappa t-1
$$

為 odd。

除以 odd 3 後仍為 odd。

正性顯然。

反向立即成立。

證畢。

---

# 22. Modulo 3 的完整分類

因 $t$ 為 odd，

考慮：

$$
t\bmod3.
$$

### Case A

若：

$$
t\equiv1\pmod3,
$$

要求：

$$
2^\kappa\equiv1\pmod3.
$$

而：

$$
2^\kappa
\equiv
(-1)^\kappa
\pmod3.
$$

所以：

$$
\boxed{
\kappa\text{ 必須為偶數}.
}
$$

### Case B

若：

$$
t\equiv2\pmod3,
$$

要求：

$$
2^\kappa(-1)\equiv1\pmod3,
$$

所以：

$$
\boxed{
\kappa\text{ 必須為奇數}.
}
$$

### Case C

若：

$$
t\equiv0\pmod3,
$$

則：

$$
2^\kappa t\equiv0\pmod3
$$

不可能等於 1。

所以：

$$
\boxed{
3\mid t
\Rightarrow
S^{-1}(t)=\varnothing.
}
$$

---

# 23. Accelerated Map Image Avoids Multiples of 3

由上一節：

$$
\boxed{
S(n)\not\equiv0\pmod3
}
$$

對所有 odd $n$。

也可以直接看：

$$
3n+1\equiv1\pmod3,
$$

而除以：

$$
2^\kappa
$$

只乘上 mod 3 的 unit。

所以 accelerated odd skeleton 的 target states 永遠落在：

$$
\boxed{
1,2\pmod3.
}
$$

---

# 24. Terminal Fiber at $t=1$

取：

$$
t=1.
$$

因：

$$
1\equiv1\pmod3,
$$

合法 $\kappa$ 必為偶數：

$$
\kappa=2j,
\qquad
j\ge1.
$$

因此：

$$
R_{2j}(1)
=
\frac{2^{2j}-1}{3}.
$$

即：

$$
\boxed{
R_{2j}(1)
=
\frac{4^j-1}{3}.
}
$$

這正是舊研究的：

$$
\boxed{
M_j.
}
$$

---

# 25. 舊「高速公路」族的重新解釋

舊研究：

$$
M_j
=
\frac{4^j-1}{3}
=
1,5,21,85,341,\ldots.
$$

過去把它們視為快速進入 powers-of-two spine 的特殊族。

現在其本質可精確寫成：

$$
\boxed{
S(M_j)=1.
}
$$

而：

$$
\boxed{
v_2(3M_j+1)=2j.
}
$$

所以：

$$
M_j
$$

是 terminal odd state 1 的完整合法 even-valuation inverse fiber。

這比「高速公路」更結構化，也更一般。

---

# 26. 數字 5 的重新定位

$$
5
=
\frac{4^2-1}{3}
=
R_4(1).
$$

所以：

$$
\boxed{
5
\text{ 只是 }t=1,\kappa=4\text{ 的 inverse-fiber member}.
}
$$

其 ordinary Collatz 軌跡：

$$
5\to16\to8\to4\to2\to1.
$$

而：

$$
5\cdot2^q
$$

只是 odd node 5 上方的 even $2$-ray。

因此不需要額外假設「5 是超級吸引子」。

---

# 27. 任意 Target 的 Inverse Highway Family

對任何 positive odd：

$$
t\not\equiv0\pmod3,
$$

都有無限多個 parity-compatible $\kappa$：

若：

$$
t\equiv1\pmod3,
$$

則：

$$
\kappa=2,4,6,\ldots.
$$

若：

$$
t\equiv2\pmod3,
$$

則：

$$
\kappa=1,3,5,\ldots.
$$

因此：

$$
\boxed{
\mathcal R(t)
=
\left\{
\frac{2^\kappa t-1}{3}:
2^\kappa t\equiv1\pmod3
\right\}
}
$$

形成 target $t$ 的 accelerated inverse fiber。

所以早期「高速公路」不只存在於 1。

每個合法 odd target 都有自己的 valuation-labelled inverse family。

---

# 28. Odd Skeleton as Valuation-Labeled Graph

因此 accelerated inverse graph 可表示為：

節點：

$$
t\in\mathbb Z_{>0}^{\mathrm{odd}},
\qquad
3\nmid t
$$

及其 admissible predecessors。

edge label：

$$
\boxed{
\kappa=v_2(3n+1).
}
$$

edge relation：

$$
\boxed{
n
\xrightarrow{\;\kappa\;}
t
\iff
n=\frac{2^\kappa t-1}{3}.
}
$$

所以 odd skeleton 是一張 valuation-labelled directed graph。

---

# 29. 與早期雙螺旋的關係

舊「雙螺旋」主要把：

- forward orbit；
- backward convergence tree；

視為兩條相向路徑。

本文後，可改寫得更精確。

## Forward local strand

$$
\boxed{
r_w+2^k a
\to
m_w+3^u a.
}
$$

## Backward local strand

$$
\boxed{
m_w+3^u a
\to
r_w+2^k a.
}
$$

## Accelerated odd inverse strand

$$
\boxed{
t
\leftarrow
\frac{2^\kappa t-1}{3}.
}
$$

因此「雙螺旋」不再只是視覺圖，

而是：

$$
\boxed{
\text{two compatible exact coordinate directions}.
}
$$

---

# 30. 為什麼稱為 $2^k\leftrightarrow3^u$？

fixed finite word 中：

source spacing：

$$
2^k.
$$

target spacing：

$$
3^u.
$$

所以：

$$
\boxed{
2^k
}
$$

控制 admissible source residue resolution，

而：

$$
\boxed{
3^u
}
$$

控制 target progression resolution。

這兩個尺度的 quotient label：

$$
a
$$

完全相同。

---

# 31. 這不是說「2-adic = 3-adic」

必須避免過度詮釋。

本文只證明 fixed-word arithmetic progression transport：

$$
r_w+2^k\mathbb Z
\leftrightarrow
m_w+3^u\mathbb Z.
$$

它不自動建立：

$$
\mathbb Z_2\cong\mathbb Z_3.
$$

事實上：

$$
\mathbb Z_2
$$

與：

$$
\mathbb Z_3
$$

具有不同的 local-field / topological structure。

所以：

$$
\boxed{
\text{$2^k$/$3^u$ bidirectional residue transport}
}
$$

不是：

$$
\boxed{
\text{global $2$-adic/$3$-adic isomorphism}.
}
$$

---

# 32. Local Inverse ≠ Global Coverage

fixed $w$：

$$
F_w^{-1}
$$

存在且 exact。

但是 Collatz conjecture 需要：

$$
\forall n>0,
$$

其 forward orbit 最終進入 terminal cycle。

inverse formulation 等價要求：

$$
\boxed{
\text{inverse tree rooted at 1 covers all positive integers}.
}
$$

local inverse theorem 只回答：

> 若已知 itinerary / target congruence，怎麼精確反解？

它沒有回答：

> 每個整數是不是都出現在 terminal inverse tree？

所以：

$$
\boxed{
\text{local exact inversion}
\not\Rightarrow
\text{global inverse coverage}.
}
$$

---

# 33. Merge 與 Inversion 也不同

若不同 charts：

$$
w\neq v
$$

滿足：

$$
\Gamma_w\cap\Gamma_v\neq\varnothing,
$$

可能存在不同 sources 在固定步數後 merge 到同一 target。

這不違反 fixed-chart injectivity，

因為 injectivity 是：

$$
F_w|_{\mathcal C_w}
$$

內部的。

跨 chart：

$$
F_w(x)=F_v(z)
$$

完全可能。

因此：

$$
\boxed{
\text{local bijection}
\neq
\text{global one-to-one dynamics}.
}
$$

---

# 34. Fixed-Word Fiber Intersection

若：

$$
y\in\Gamma_w\cap\Gamma_v,
$$

則存在：

$$
a,b
$$

使：

$$
y=m_w+3^{u_w}a
$$

及：

$$
y=m_v+3^{u_v}b.
$$

這轉化為線性 Diophantine congruence：

$$
m_w-m_v
=
3^{u_v}b-3^{u_w}a.
$$

因此 target merge 問題本身也可被 reduction 成 arithmetic progression intersection。

這會在 Paper 09 finite certificate frontier 中重新出現。

---

# 35. 與 3x+1 Semigroup 的關係

既有 3x+1 semigroup 研究已用 rational multiplicative generators 編碼 backward iteration。

本文不宣稱「backward algebraic encoding」是新發現。

本文的特定工作是把 Paper 03 的 finite parity chart 寫成：

$$
\boxed{
\text{source residue class}
\overset{F_w}{\longleftrightarrow}
\text{target progression}
}
$$

並以同一 quotient coordinate提供 exact forward/inverse recovery。

這是 Operation Translation 系列的 atlas formulation。

---

# 36. 與 $2$-adic inverse parity transform 的關係

既有 $2$-adic Collatz 研究已研究：

$$
\text{$2$-adic integer}
\leftrightarrow
\text{infinite parity sequence}.
$$

本文只處理 finite word：

$$
w\in\{D,U\}^k
$$

與其：

$$
r_w\bmod2^k.
$$

因此 finite residue atlas 與 $2$-adic parity coding 相容，

但本文進一步附加：

$$
\boxed{
m_w\bmod3^u
}
$$

這個 target-side metadata，

用於精確 inverse recovery。

---

# 37. Bidirectional Chart Object

本文將 fixed word 的完整雙向資料記為：

$$
\boxed{
\mathcal B_w
=
(
w,
k,
u,
b_w,
r_w,
m_w,
\mathcal C_w,
\mathcal P_w,
\phi_w,
\psi_w
).
}
$$

其中：

$$
\phi_w(n)=\frac{n-r_w}{2^k},
$$

$$
\psi_w(y)=\frac{y-m_w}{3^u}.
$$

且：

$$
\boxed{
\psi_wF_w\phi_w^{-1}
=
\operatorname{id}.
}
$$

---

# 38. Bidirectional Certificate

給定：

$$
(x,y,w),
$$

可用三條 exact condition 驗證：

### Source legality

$$
\boxed{
x\equiv r_w\pmod{2^k}.
}
$$

### Target legality

$$
\boxed{
y\equiv m_w\pmod{3^u}.
}
$$

### Transport consistency

$$
\boxed{
3^u(x-r_w)
=
2^k(y-m_w).
}
$$

若三者成立並滿足 positive-domain quotient bound，

則 fixed-word transport 可機器精確驗證。

---

# 39. 這對有限驗證的意義

傳統 finite verification 常保存：

$$
n\to T(n)\to T^2(n)\to\cdots.
$$

本文顯示對已知 word：

$$
w
$$

可以只保存：

$$
\boxed{
(r_w,m_w,k,u,b_w).
}
$$

整個 cylinder 的所有 starting states 都可由 quotient label $a$ 批次描述。

因此：

$$
\boxed{
\text{trajectory storage}
\to
\text{chart certificate storage}.
}
$$

這將在 Paper 09 正式化。

---

# 40. 本文主要定理總結

## Theorem A — Bidirectional Residue Transport

$$
\boxed{
r_w+2^k\mathbb Z
\overset{\sim}{\longleftrightarrow}
m_w+3^u\mathbb Z.
}
$$

## Theorem B — Exact Inverse

$$
\boxed{
x
=
r_w+
2^k\frac{y-m_w}{3^u}.
}
$$

## Theorem C — Target Legality

$$
\boxed{
y\equiv m_w\pmod{3^u}.
}
$$

## Theorem D — Quotient Conservation

$$
\boxed{
\frac{x-r_w}{2^k}
=
\frac{y-m_w}{3^u}.
}
$$

## Theorem E — Accelerated Inverse Fiber

$$
\boxed{
R_\kappa(t)
=
\frac{2^\kappa t-1}{3}
}
$$

合法 iff：

$$
\boxed{
2^\kappa t\equiv1\pmod3.
}
$$

## Theorem F — Terminal Fiber

$$
\boxed{
R_{2j}(1)
=
\frac{4^j-1}{3}.
}
$$

---

# 41. 本文限制

第一，fixed-word inverse 依賴已知 chart $w$。

第二，target progressions 可跨 chart 重疊。

第三，本文不證明 inverse tree rooted at 1 覆蓋所有正整數。

第四，本文的 $2^k\leftrightarrow3^u$ 是 finite arithmetic progression transport，不是 $\mathbb Z_2$ 與 $\mathbb Z_3$ 的全域同構。

第五，accelerated inverse fibers 描述 odd skeleton edge candidates，但 global coverage 仍是未解問題。

---

# 42. 結論

Paper 03 證明：

$$
\text{parity word}
\longleftrightarrow
\text{unique }2^k\text{ source cylinder}.
$$

本文再證：

$$
\boxed{
\text{source }2^k\text{ cylinder}
\longleftrightarrow
\text{target }3^u\text{ progression}.
}
$$

兩側由同一 exact quotient coordinate：

$$
a
$$

連接。

因此 fixed-word Collatz dynamics 不只可 forward 壓縮，

也可以 exact inverse recovery。

這使作者早期「雙螺旋」研究得到一個更嚴格的新形式：

$$
\boxed{
\text{forward residue refinement}
+
\text{backward valuation / progression fibers}.
}
$$

另一方面，

舊研究中的：

$$
\frac{4^j-1}{3}
$$

也被重新定位為：

$$
\boxed{
\text{terminal state }1
\text{ 的 accelerated inverse fiber}.
}
$$

所以：

- powers of two；
- odd skeleton；
- $M_j$；
- 5；
- $5\cdot2^q$；

不再需要作為互相分離的「特殊結構」處理，而可統一進：

$$
\boxed{
\text{odd inverse skeleton}
+
\text{valuation-labelled fibers}
+
\text{even }2\text{-rays}.
}
$$

至此，早期雙螺旋框架完成了從圖像式方法到 exact residue transport 的重構。

下一篇將轉向另一個問題：

> 在所有 finite parity charts 中，哪些 charts 在充分大尺度上必然下降？

並建立：

$$
\boxed{
3^u<2^k
}
$$

的收縮邊界、word-order threshold，以及二項式 Cylinder Law。

---

# 參考文獻

1. David Applegate, Jeffrey C. Lagarias, *The 3x+1 Semigroup*, Journal of Number Theory 117 (2006), arXiv:math/0411140.
2. Olivier Rozier, *Parity sequences of the 3x+1 map on the 2-adic integers and Euclidean embedding*, arXiv:1805.00133.
3. Tong Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, arXiv:2605.13886.
4. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum of Mathematics, Pi 10 (2022), arXiv:1909.03562.
5. Collatz Operation Translation Series — Paper 01, *考拉茲猜想既有研究的重新分類與校正*.
6. Collatz Operation Translation Series — Paper 02, *Collatz Local Affine Atlas：有限奇偶字的精確仿射化*.
7. Collatz Operation Translation Series — Paper 03, *Parity Word、Residue Cylinder 與局部 Identity 化*.

---

## 下一篇

**Paper 05 —《有限字收縮邊界與二項式 Cylinder Law》**

核心任務：

1. 證明
   $$
   T_w(n)<n
   \iff
   b_w<(2^k-3^u)n;
   $$
2. 建立 $3^u<2^k$ 的 asymptotic contraction criterion；
3. 定義
   $$
   \alpha=\frac{\ln2}{\ln3};
   $$
4. 證明 fixed $k$ contracting word count：
   $$
   A_k=
   \sum_{u=0}^{\lfloor \alpha k\rfloor}\binom ku;
   $$
5. 純數學解釋 $k=16$ 的 $89.4943\%$；
6. 證明 contracting-cylinder density $P_k\to1$；
7. 嚴格指出 density-one 與 universal Collatz convergence 的鴻溝。
