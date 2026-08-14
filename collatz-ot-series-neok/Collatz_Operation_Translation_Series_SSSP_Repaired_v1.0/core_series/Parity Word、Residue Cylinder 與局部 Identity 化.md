# Parity Word、Residue Cylinder 與局部 Identity 化
## ——Collatz Local Affine Atlas 的精確判定域、雙進位分裂與局部平凡化

**English Title:** *Parity Words, Residue Cylinders, and Local Identity Trivialization in the Collatz Local Affine Atlas*

**作者：** Neo.K  
**機構：** 一言諾科技有限公司（EveMissLab）  
**系列：** Collatz Operation Translation Series — Paper 03  
**版本：** v0.1.1  
**日期：** 2026-08-10  
**修訂日期：** 2026-08-14

---

## 摘要

Paper 02 已證明：對 modified Collatz map

$$
T(n)=
\begin{cases}
\dfrac n2,&n\equiv0\pmod2,\\[2mm]
\dfrac{3n+1}{2},&n\equiv1\pmod2,
\end{cases}
$$

任意有限 parity word

$$
w\in\{D,U\}^k
$$

均對應一個形式仿射算子

$$
F_w(x)
=
\frac{3^{u(w)}x+b_w}{2^k}.
$$

但 Paper 02 尚未回答最重要的判定域問題：

> 哪些正整數真的以 $w$ 作為其前 $k$ 步 Collatz itinerary？

本文證明，對每一個長度 $k$ 的 parity word $w$，存在唯一 residue

$$
r_w\in\mathbb Z/2^k\mathbb Z
$$

使其 admissible domain 精確為

$$
\boxed{
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}.
}
$$

因此長度 $k$ 的 parity words 與 modulo $2^k$ residue classes 形成一一對應：

$$
\boxed{
\{D,U\}^k
\longleftrightarrow
\mathbb Z/2^k\mathbb Z.
}
$$

本文並給出其 closed congruence：

$$
\boxed{
r_w
\equiv
-b_w\,3^{-u(w)}
\pmod{2^k},
}
$$

其中 $3^{-u(w)}$ 表示 $3^{u(w)}$ 在模 $2^k$ 下的乘法逆元。

更重要的是，令

$$
m_w=T^k(r_w)
=
\frac{3^{u(w)}r_w+b_w}{2^k},
$$

則對任意整數 quotient coordinate $a$，只要

$$
n=r_w+2^k a>0,
$$

就有 exact cylinder transport：

$$
\boxed{
T^k(r_w+2^ka)
=
m_w+3^{u(w)}a.
}
$$

因此 source cylinder

$$
r_w+2^k\mathbb Z
$$

被 $T^k$ 精確送到 target arithmetic progression

$$
m_w+3^{u(w)}\mathbb Z.
$$

定義 source chart

$$
\phi_w(n)
=
\frac{n-r_w}{2^k},
$$

以及 target chart

$$
\psi_w(y)
=
\frac{y-m_w}{3^{u(w)}},
$$

則在合法 domain 上：

$$
\boxed{
\psi_w\circ T^k\circ\phi_w^{-1}
=
\operatorname{id}.
}
$$

也就是說：**固定有限 parity word 的 Collatz dynamics 不只是仿射化，而可在適當 source/target coordinates 中精確平凡化成 identity map。**

本文將這組資料

$$
\mathcal A_w
=
(\Omega_w,\Gamma_w,\phi_w,\psi_w,F_w)
$$

稱為一個 **Collatz Local Affine Chart**。所有長度 $k$ 的 charts 共同形成 level-$k$ atlas：

$$
\boxed{
\mathfrak A_k
=
\{\mathcal A_w:w\in\{D,U\}^k\}.
}
$$

其 source domains 恰好對正整數形成互不重疊的 partition。進一步，從長度 $k$ 到 $k+1$ 時，每個 cylinder 會依 quotient coordinate 的一個 parity bit 唯一分裂成兩個子 cylinder；因此 atlas refinement 等價於 binary residue refinement。

本文最終得到一個核心結論：

$$
\boxed{
\text{finite Collatz dynamics is locally identity-trivializable}.
}
$$

但本文同時強調：

$$
\boxed{
\text{local identity trivialization}
\not\Rightarrow
\text{global Collatz convergence}.
}
$$

因為真正未決的問題已轉移為：當軌跡離開一張有限 chart 後，下一張 chart 如何被選擇，以及無限 chart itinerary 是否對每個起點必然進入 descending / certified region。

**關鍵詞：** Collatz conjecture、parity word、residue cylinder、2-adic coding、local affine atlas、identity conjugacy、operation translation、exact recovery、3n+1

---

# 1. Paper 02 留下的判定域缺口

Paper 02 對任意形式字

$$
w=\sigma_1\cdots\sigma_k,
\qquad
\sigma_j\in\{D,U\},
$$

定義：

$$
D(x)=\frac{x}{2},
$$

$$
U(x)=\frac{3x+1}{2},
$$

並證明：

$$
\boxed{
F_w(x)
=
\frac{3^{u(w)}x+b_w}{2^k}.
}
$$

但：

$$
F_w(n)
$$

只是形式 composition。

要使：

$$
T^k(n)=F_w(n),
$$

必須 $n$ 的前 $k$ 次 parity decisions 真正等於 $w$。

因此必須找出：

$$
\boxed{
\Omega_w
=
\{n>0:w\text{ is the first }k\text{-step parity word of }n\}.
}
$$

---

# 2. 主要定理預告

本文將證明：

$$
\boxed{
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}
}
$$

且 $r_w$ 唯一。

所以「finite word 的合法域」不是任意稀疏集合，而是一個完整 residue cylinder。

---

# 3. Base Case：長度 1

有兩個字：

$$
D,\qquad U.
$$

其中：

$$
\Omega_D
=
2\mathbb Z_{>0}
=
(0+2\mathbb Z)\cap\mathbb Z_{>0},
$$

以及：

$$
\Omega_U
=
(1+2\mathbb Z)\cap\mathbb Z_{>0}.
$$

所以：

$$
r_D=0\pmod2,
$$

$$
r_U=1\pmod2.
$$

長度 1 的 word ↔ residue 對應成立。

---

# 4. Inductive Cylinder Hypothesis

假設對某個長度 $k$ 的字 $w$，

已存在唯一 residue class：

$$
r_w\pmod{2^k},
$$

並取其 canonical representative：

$$
0\le r_w<2^k.
$$

使：

$$
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}.
$$

令：

$$
u=u(w),
$$

並定義：

$$
m_w
=
F_w(r_w)
=
\frac{3^ur_w+b_w}{2^k}.
$$

由 cylinder hypothesis，無論 $r_w$ 是否為 $0$，都有：

$$
r_w+2^k\in\Omega_w.
$$

因此 $F_w$ 在這個正整數 admissible input 上等於真正的 $T^k$，故：

$$
F_w(r_w+2^k)
=
m_w+3^u
\in\mathbb Z.
$$

因 $3^u\in\mathbb Z$，遂得：

$$
m_w\in\mathbb Z.
$$

---

# 5. Cylinder Quotient Coordinate

任意：

$$
n\in\Omega_w
$$

唯一寫為：

$$
\boxed{
n=r_w+2^ka,
\qquad
a\in\mathbb Z,
}
$$

並滿足 $n>0$。

Paper 02 的 affine formula 給：

$$
T^k(n)
=
\frac{3^u(r_w+2^ka)+b_w}{2^k}.
$$

因此：

$$
\boxed{
T^k(n)
=
m_w+3^ua.
}
$$

由於：

$$
3^u
$$

為奇數，

所以：

$$
T^k(n)\pmod2
=
m_w+a\pmod2.
$$

這個簡單式子就是 atlas refinement 的核心。

---

# 6. Append-$D$ 子 Cylinder

字：

$$
wD
$$

合法的條件是：

$$
T^k(n)\equiv0\pmod2.
$$

所以：

$$
m_w+a\equiv0\pmod2.
$$

等價：

$$
\boxed{
a\equiv m_w\pmod2.
}
$$

令：

$$
a=m_w+2q
$$

在模 2 意義下。

代回：

$$
n
=
r_w+2^k a.
$$

所以 modulo $2^{k+1}$：

$$
\boxed{
r_{wD}
\equiv
r_w+2^k(m_w\bmod2)
\pmod{2^{k+1}}.
}
$$

因此 $wD$ 對應唯一 modulo $2^{k+1}$ residue。

---

# 7. Append-$U$ 子 Cylinder

同理，

$$
wU
$$

合法要求：

$$
T^k(n)\equiv1\pmod2.
$$

所以：

$$
m_w+a\equiv1\pmod2.
$$

即：

$$
\boxed{
a\equiv1-m_w\pmod2.
}
$$

因此：

$$
\boxed{
r_{wU}
\equiv
r_w
+
2^k(1-m_w\bmod2)
\pmod{2^{k+1}}.
}
$$

更直觀地：

$$
\{r_{wD},r_{wU}\}
=
\{r_w,r_w+2^k\}
\pmod{2^{k+1}}.
$$

兩者恰好是 parent cylinder 的兩個 binary refinements。

---

# 8. Word–Residue Bijection Theorem

## 定理 8.1

對每個：

$$
w\in\{D,U\}^k,
$$

存在唯一：

$$
r_w\in\mathbb Z/2^k\mathbb Z
$$

使：

$$
\boxed{
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}.
}
$$

此外：

$$
w\neq v
\Longrightarrow
r_w\not\equiv r_v\pmod{2^k}.
$$

因此：

$$
\boxed{
\{D,U\}^k
\cong
\mathbb Z/2^k\mathbb Z
}
$$

作為有限集合。

### 證明

Base case 已成立。

若 length-$k$ 每個 cylinder 唯一，

則上節證明每個 cylinder 恰分裂成 $wD,wU$ 兩個互斥且完備的 modulo $2^{k+1}$ 子 cylinder。

因此由 induction，所有 $k$ 成立。

證畢。

---

# 9. Partition Theorem

因 modulo $2^k$ residue classes 恰好 partition $\mathbb Z$，

所以：

$$
\boxed{
\mathbb Z_{>0}
=
\bigsqcup_{w\in\{D,U\}^k}
\Omega_w.
}
$$

其中：

$$
\bigsqcup
$$

表示 disjoint union。

所以每個正整數在任意固定 depth $k$ 都屬於恰好一張 parity chart。

這個結論非常重要：

$$
\boxed{
\text{the level-}k\text{ atlas is globally source-complete}.
}
$$

但只是對「前 $k$ 步分類」的 source coverage 完備，不是 Collatz convergence 完備。

---

# 10. Closed Congruence Formula

Paper 02：

$$
F_w(n)
=
\frac{3^un+b_w}{2^k}.
$$

若：

$$
n\in\Omega_w,
$$

則 $F_w(n)$ 必為整數。

所以：

$$
3^un+b_w
\equiv0
\pmod{2^k}.
$$

由：

$$
\gcd(3^u,2^k)=1,
$$

$3^u$ 在：

$$
\mathbb Z/2^k\mathbb Z
$$

中為 unit。

因此：

$$
\boxed{
n
\equiv
-b_w3^{-u}
\pmod{2^k}.
}
$$

由 word–residue uniqueness，

這個唯一解必然就是：

$$
\boxed{
r_w
\equiv
-b_w3^{-u}
\pmod{2^k}.
}
$$

---

# 11. 為什麼不應只靠這條 congruence 證 admissibility？

單獨看到：

$$
3^un+b_w\equiv0\pmod{2^k}
$$

只明確保證形式算子的最終分母消失。

若沒有另外證明 finite parity coding 的唯一性，

直接從「最終整數」跳到「每個 intermediate parity branch 都正確」會留下論證缺口。

本文因此先用逐層 cylinder refinement 證：

$$
\boxed{
\text{word}\leftrightarrow\text{residue}
}
$$

再把 closed congruence 當作該 residue 的 closed formula。

這是 proof order 上的重要校正。

---

# 12. Exact Cylinder Transport Theorem

## 定理 12.1

令：

$$
w\in\{D,U\}^k,
$$

$$
u=u(w),
$$

$$
r=r_w,
$$

並：

$$
m_w=T^k(r_w).
$$

則對任何：

$$
a\in\mathbb Z
$$

只要：

$$
n=r+2^ka>0,
$$

都有：

$$
\boxed{
T^k(n)
=
m_w+3^ua.
}
$$

### 證明

因：

$$
n\equiv r_w\pmod{2^k},
$$

由 Theorem 8.1：

$$
n\in\Omega_w.
$$

所以：

$$
T^k(n)=F_w(n).
$$

代入 Paper 02 affine form：

$$
T^k(n)
=
\frac{3^u(r+2^ka)+b_w}{2^k}
$$

$$
=
\frac{3^ur+b_w}{2^k}
+
3^ua
$$

$$
=
m_w+3^ua.
$$

證畢。

---

# 13. Source Cylinder 與 Target Progression

定義：

$$
\boxed{
\mathcal C_w
=
r_w+2^k\mathbb Z
}
$$

及：

$$
\boxed{
\mathcal P_w
=
m_w+3^u\mathbb Z.
}
$$

則形式上：

$$
\boxed{
F_w(\mathcal C_w)
=
\mathcal P_w.
}
$$

在正整數 Collatz domain 中，

取：

$$
\Omega_w=\mathcal C_w\cap\mathbb Z_{>0},
$$

其 image：

$$
\Gamma_w=T^k(\Omega_w)
$$

是：

$$
\mathcal P_w
$$

中對應相同 quotient coordinates 且由正 source 產生的部分。

若只在全整數仿射 extension 上研究，

則 cylinder/progression 之間為完整雙向 bijection。

---

# 14. Source Chart

定義：

$$
\boxed{
\phi_w:
\mathcal C_w\to\mathbb Z,
}
$$

$$
\boxed{
\phi_w(n)
=
\frac{n-r_w}{2^k}.
}
$$

逆映射：

$$
\boxed{
\phi_w^{-1}(a)
=
r_w+2^ka.
}
$$

所以 source cylinder 在 chart coordinate 中就是 ordinary integer line：

$$
a\in\mathbb Z.
$$

---

# 15. Target Chart

定義：

$$
\boxed{
\psi_w:
\mathcal P_w\to\mathbb Z,
}
$$

$$
\boxed{
\psi_w(y)
=
\frac{y-m_w}{3^u}.
}
$$

逆：

$$
\boxed{
\psi_w^{-1}(a)
=
m_w+3^ua.
}
$$

---

# 16. Local Identity Trivialization Theorem

## 定理 16.1

在：

$$
\mathcal C_w
$$

上，

形式算子：

$$
F_w
$$

滿足：

$$
\boxed{
\psi_w
\circ
F_w
\circ
\phi_w^{-1}
=
\operatorname{id}_{\mathbb Z}.
}
$$

在正整數 admissible domain：

$$
\Omega_w
$$

上，

相應限制滿足：

$$
\boxed{
\psi_w
\circ
T^k
\circ
\phi_w^{-1}
=
\operatorname{id}
}
$$

在其合法 quotient-coordinate subset 上成立。

### 證明

取任意 $a$：

$$
\phi_w^{-1}(a)
=
r_w+2^ka.
$$

由 cylinder transport：

$$
F_w(\phi_w^{-1}(a))
=
m_w+3^ua.
$$

所以：

$$
\psi_w(m_w+3^ua)
=
a.
$$

證畢。

---

# 17. 這比「線性化」更強

Paper 02 得到：

$$
T^k(n)
=
\frac{3^un+b_w}{2^k}.
$$

這只是 affine compression。

Paper 03 再利用 source/target lattices：

$$
2^k\mathbb Z
$$

與：

$$
3^u\mathbb Z,
$$

把它化成：

$$
\boxed{
a\mapsto a.
}
$$

所以：

$$
\boxed{
\text{affine linearization}
\to
\text{local identity trivialization}.
}
$$

這是 Operation Translation 的極端簡化案例。

---

# 18. Exact Recovery

若知道：

$$
w,\quad r_w,\quad m_w,\quad k,\quad u,
$$

以及 target：

$$
y\in\mathcal P_w,
$$

則：

$$
a
=
\frac{y-m_w}{3^u}
$$

精確為整數。

因此 source 可 exact recover：

$$
\boxed{
n
=
r_w
+
2^k
\frac{y-m_w}{3^u}.
}
$$

所以在 fixed-chart domain：

$$
\boxed{
\text{forward transport is lossless}.
}
$$

---

# 19. Faithfulness

如果：

$$
n_1,n_2\in\mathcal C_w
$$

且：

$$
F_w(n_1)=F_w(n_2),
$$

則：

$$
\frac{3^u(n_1-n_2)}{2^k}=0.
$$

在 $\mathbb Z/\mathbb Q$ 中：

$$
n_1=n_2.
$$

因此 fixed-word affine transform 是 injective。

所以局部 identityization 不存在 information loss。

---

# 20. 例一：$w=D$

$$
r_D=0\pmod2.
$$

取 representative：

$$
r_D=0.
$$

$$
m_D=T(0)=0
$$

在整數 affine extension。

cylinder：

$$
2\mathbb Z.
$$

target：

$$
\mathbb Z.
$$

source chart：

$$
a=n/2.
$$

target chart：

$$
a=y.
$$

因此：

$$
D(2a)=a.
$$

這是最簡單 identity chart。

對正整數 domain，

只取：

$$
a\ge1.
$$

---

# 21. 例二：$w=U$

$$
r_U=1\pmod2.
$$

取：

$$
r_U=1.
$$

$$
m_U=T(1)=2.
$$

所以：

$$
\boxed{
T(1+2a)
=
2+3a.
}
$$

source：

$$
1+2\mathbb Z,
$$

target：

$$
2+3\mathbb Z.
$$

charts：

$$
\phi_U(n)=\frac{n-1}{2},
$$

$$
\psi_U(y)=\frac{y-2}{3}.
$$

則：

$$
\boxed{
\psi_UT\phi_U^{-1}(a)=a.
}
$$

---

# 22. 例三：$w=UD$

Paper 02：

$$
F_{UD}(n)
=
\frac{3n+1}{4}.
$$

所以：

$$
u=1,
\qquad
b=1.
$$

residue：

$$
3n+1\equiv0\pmod4.
$$

因：

$$
3^{-1}\equiv3\pmod4,
$$

$$
r_{UD}
\equiv
-3
\equiv1
\pmod4.
$$

所以：

$$
\Omega_{UD}
=
(1+4\mathbb Z)\cap\mathbb Z_{>0}.
$$

取：

$$
r=1.
$$

$$
m=T^2(1)=1.
$$

因此：

$$
\boxed{
T^2(1+4a)
=
1+3a.
}
$$

---

# 23. 例四：$w=DU$

Paper 02：

$$
F_{DU}(n)
=
\frac{3n+2}{4}.
$$

所以：

$$
u=1,
\qquad
b=2.
$$

解：

$$
3n+2\equiv0\pmod4.
$$

得：

$$
r_{DU}=2.
$$

$$
m=T^2(2)=2.
$$

所以：

$$
\boxed{
T^2(2+4a)
=
2+3a.
}
$$

注意 $UD$ 和 $DU$：

- $k$ 相同；
- $u$ 相同；
- target step size 都是 $3$；

但：

$$
r_w,\quad m_w
$$

不同。

這正是 Paper 02 order correction 的 domain-level manifestation。

---

# 24. 例五：$w=UUDD$

Paper 02：

$$
F_w(n)
=
\frac{9n+5}{16}.
$$

所以：

$$
k=4,\qquad u=2,\qquad b=5.
$$

解：

$$
9n+5\equiv0\pmod{16}.
$$

因：

$$
9^{-1}\equiv9\pmod{16},
$$

$$
r_w
\equiv
-45
\equiv3
\pmod{16}.
$$

取：

$$
r_w=3.
$$

直接：

$$
3\to5\to8\to4\to2.
$$

所以：

$$
m_w=2.
$$

因此整個 cylinder：

$$
\boxed{
3+16a
\longmapsto
2+9a.
}
$$

charts：

$$
\phi_w(n)
=
\frac{n-3}{16},
$$

$$
\psi_w(y)
=
\frac{y-2}{9}.
$$

所以：

$$
\boxed{
a\mapsto a.
}
$$

---

# 25. Level-$k$ Collatz Atlas

定義每個 word chart：

$$
\boxed{
\mathcal A_w
=
(
\Omega_w,
\Gamma_w,
\phi_w,
\psi_w,
T^k|_{\Omega_w}
).
}
$$

所有長度 $k$ words：

$$
\boxed{
\mathfrak A_k
=
\{
\mathcal A_w:
w\in\{D,U\}^k
\}.
}
$$

稱為 **level-$k$ Collatz Local Affine Atlas**。

---

# 26. Source-Complete Atlas

由 Partition Theorem：

$$
\boxed{
\mathbb Z_{>0}
=
\bigsqcup_{w\in\{D,U\}^k}
\Omega_w.
}
$$

因此對任意正整數 $n$，

在 level $k$ 恰有一張 chart：

$$
\mathcal A_w
$$

負責描述其前 $k$ 步 dynamics。

所以：

$$
\boxed{
\mathfrak A_k
\text{ is source-complete}.
}
$$

---

# 27. 但 Target Charts 可以重疊

不同：

$$
w\neq v
$$

的 target images：

$$
\Gamma_w,\Gamma_v
$$

不一定互斥。

這是因為不同起點可在 $k$ 步後 merge 到同一 state 或同一 progression intersection。

因此：

$$
\boxed{
\text{source partition}
\neq
\text{target partition}.
}
$$

這一點將在 finite certificate / path-merging 中變得重要。

---

# 28. Atlas Refinement

每個：

$$
\Omega_w
$$

在下一層分裂為：

$$
\boxed{
\Omega_w
=
\Omega_{wD}
\bigsqcup
\Omega_{wU}.
}
$$

而 modulo：

$$
2^{k+1},
$$

這兩個 child residues 就是：

$$
r_w
$$

與：

$$
r_w+2^k.
$$

哪一個對應 $D$、哪一個對應 $U$，

由：

$$
m_w
$$

的 parity 決定。

---

# 29. Quotient Bit Interpretation

寫：

$$
n=r_w+2^ka.
$$

則下一步 parity：

$$
T^k(n)\pmod2
=
m_w+a\pmod2.
$$

所以在 fixed chart 中，

下一個 Collatz branch 不再需要重新看巨大整數 $n$。

只需看 quotient coordinate：

$$
\boxed{
a\bmod2
}
$$

再加一個固定 chart bit：

$$
m_w\bmod2.
$$

這是非常重要的 computational / symbolic simplification。

---

# 30. Atlas Refinement 就是 Binary Decision

因此從 level $k$ 到 $k+1$：

$$
\boxed{
\text{one new itinerary symbol}
\leftrightarrow
\text{one new quotient bit}.
}
$$

Collatz parity tree 與 binary residue refinement 因此不是單純類比，

而是精確同一個有限 combinatorial refinement structure。

---

# 31. 與 $2$-adic parity coding 的關係

既有 Collatz 研究已知：

$2$-adic integers 與其 infinite parity sequences 可建立一一對應，且 modified Collatz map 與 $2$-adic shift 之間存在 conjugacy structure。

本文並不重新宣稱此一結果為新發現。

本文的 finite contribution 是把 finite prefix 明確組織為：

$$
\boxed{
\text{word}
\leftrightarrow
\text{mod }2^k\text{ cylinder}
\leftrightarrow
\text{exact affine transport}
\leftrightarrow
\text{local identity chart}.
}
$$

因此它更接近 Operation Translation 的有限局部 atlas formulation。

---

# 32. Finite Atlas 與 Infinite 2-adic Coding

若：

$$
w_1\prec w_2\prec w_3\prec\cdots
$$

是一條一致的無限 parity-prefix chain，

對應 residues：

$$
r_1\bmod2,
$$

$$
r_2\bmod2^2,
$$

$$
r_3\bmod2^3,
$$

並滿足：

$$
r_{k+1}
\equiv
r_k
\pmod{2^k}.
$$

這形成 inverse system，

其極限自然對應一個：

$$
\mathbb Z_2
$$

中的 $2$-adic integer。

因此 finite atlas refinement 與 classical $2$-adic parity coding 相容。

---

# 33. 但正整數問題仍不同

一條任意 infinite parity sequence 對應某個：

$$
2\text{-adic integer},
$$

不代表該 $2$-adic integer 是 ordinary positive integer。

因此：

$$
\boxed{
\text{$2$-adic itinerary existence}
\not\Rightarrow
\text{positive-integer orbit existence}.
}
$$

這也是為什麼 $2$-adic conjugacy 本身不直接解 Collatz conjecture。

---

# 34. 局部 Identity 並沒有消滅 Global Dynamics

這一點必須特別強調。

對 fixed $w$：

$$
\psi_wT^k\phi_w^{-1}
=
\operatorname{id}.
$$

可能讓人錯誤以為：

> Collatz 已經被變成 identity，所以問題解掉了。

不對。

因為每個 chart 只負責：

$$
k
$$

個步驟。

跨出 target：

$$
\Gamma_w
$$

後，

若要繼續下一個 block，

必須重新判定下一張 admissible chart。

因此真正 global system 是：

$$
\boxed{
\mathcal A_{w_0}
\to
\mathcal A_{w_1}
\to
\mathcal A_{w_2}
\to\cdots.
}
$$

---

# 35. Global Itinerary Problem

這使 Collatz 全域困難可以重新表述為：

> 對每個正整數起點，其無限 chart itinerary 是否必然在有限時刻進入已知 descending / terminal certificate domain？

所以：

$$
\boxed{
\text{local operator complexity}
}
$$

已被大幅消除，

剩餘的是：

$$
\boxed{
\text{global chart-selection complexity}.
}
$$

這就是本系列的核心分工。

---

# 36. Source Coordinate 與 Target Coordinate 的尺度不同

source spacing：

$$
2^k.
$$

target spacing：

$$
3^u.
$$

所以 identityization 並不是在原數軸上說：

$$
T^k(n)=n.
$$

而是：

$$
\boxed{
\text{the quotient label }a\text{ is preserved}.
}
$$

原值改變：

$$
r_w+2^ka
\to
m_w+3^ua,
$$

但 chart coordinate：

$$
a
$$

不變。

這是「local identity」的正確語義。

---

# 37. Exact Recovery 與 Series A

Series A 強調：

$$
\text{approximate coordinate}
\to
\text{exact decision}
$$

以及：

$$
\text{faithful transform}.
$$

本篇的情況甚至更強：

coordinate：

$$
a
$$

本身是 exact integer。

所以：

$$
\boxed{
\text{encoding}
\to
\text{identity transport}
\to
\text{exact decoding}
}
$$

完全沒有 numerical approximation。

這是一個純離散 exact model。

---

# 38. Paper 03 的核心分類

對 fixed finite word：

### Domain legality

$$
n\in\Omega_w
\iff
n\equiv r_w\pmod{2^k}.
$$

### Exact operator

$$
T^k(n)
=
\frac{3^un+b_w}{2^k}.
$$

### Cylinder transport

$$
r_w+2^ka
\to
m_w+3^ua.
$$

### Local coordinate law

$$
a\to a.
$$

### Recovery

$$
n
=
r_w
+
2^k\frac{y-m_w}{3^u}.
$$

五層全部 exact。

---

# 39. 本文限制

第一，本文只處理 finite word / finite depth。

第二，本文沒有證明任意 infinite positive-integer itinerary 收斂。

第三，本文不把 known $2$-adic parity conjugacy 宣稱為新發現。

第四，source residue partition 完備不等於 target convergence coverage 完備。

第五，local identityization 依賴 word-specific source/target charts，並不是單一 global coordinate transform。

---

# 40. 主要定理總結

## Theorem A — Unique Residue Cylinder

$$
\boxed{
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}.
}
$$

## Theorem B — Word–Residue Bijection

$$
\boxed{
\{D,U\}^k
\longleftrightarrow
\mathbb Z/2^k\mathbb Z.
}
$$

## Theorem C — Closed Residue Formula

$$
\boxed{
r_w
\equiv
-b_w3^{-u}
\pmod{2^k}.
}
$$

## Theorem D — Exact Cylinder Transport

$$
\boxed{
T^k(r_w+2^ka)
=
m_w+3^ua.
}
$$

## Theorem E — Local Identity Trivialization

$$
\boxed{
\psi_wT^k\phi_w^{-1}
=
\operatorname{id}.
}
$$

## Theorem F — Exact Recovery

$$
\boxed{
n
=
r_w+
2^k\frac{y-m_w}{3^u}.
}
$$

---

# 41. 結論

Paper 02 已經證明：

$$
\text{finite parity word}
\to
\text{exact affine operator}.
$$

本文再證：

$$
\text{finite parity word}
\to
\text{unique residue cylinder}.
$$

因此兩者結合得到：

$$
\boxed{
\text{word}
\longleftrightarrow
\text{source cylinder}
\longrightarrow
\text{target progression}.
}
$$

而在 quotient coordinates 中：

$$
\boxed{
a\longmapsto a.
}
$$

所以 Collatz 的前 $k$ 步 dynamics，

在每張合法 chart 中可以被完全平凡化。

這正是本文標題中：

$$
\boxed{
\text{Collatz Local Affine Atlas}
}
$$

的核心意義。

真正還沒有被平凡化的是：

$$
\boxed{
\text{which chart comes next?}
}
$$

因此：

$$
\boxed{
\textbf{Collatz dynamics is locally identity-trivializable,
but globally itinerary-nontrivial.}
}
$$

在本文後已不再只是方法論口號，

而有了第一個完整的有限域定理版本。

Paper 04 將沿著本文的 exact cylinder transport：

$$
r_w+2^k a
\longmapsto
m_w+3^u a
$$

研究其反向形式，

並把作者早期「雙螺旋」概念重構為：

$$
\boxed{
2^k\text{-source cylinder}
\leftrightarrow
3^u\text{-target progression}.
}
$$

---

# 參考文獻

1. Olivier Rozier, *Parity sequences of the 3x+1 map on the 2-adic integers and Euclidean embedding*, arXiv:1805.00133.
2. Jonathan Yazinski, *Pseudoperiodicity and the 3x+1 Conjugacy Function*, arXiv:1102.5547.
3. Olivier Rozier, Claude Terracol, *Paradoxical behavior in Collatz sequences*, arXiv:2502.00948.
4. Tong Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, arXiv:2605.13886.
5. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum of Mathematics, Pi 10 (2022), arXiv:1909.03562.
6. David Applegate, Jeffrey C. Lagarias, *The 3x+1 Semigroup*, Journal of Number Theory 117 (2006), arXiv:math/0411140.
7. Collatz Operation Translation Series — Paper 02, *Collatz Local Affine Atlas：有限奇偶字的精確仿射化*.

---

## 下一篇

**Paper 04 —《雙向殘餘類轉譯：$2^k$ Cylinder 與 $3^u$ Progression》**

核心任務：

1. 將
   $$
   r_w+2^ka\mapsto m_w+3^ua
   $$
   寫成完整雙向算術 transport；
2. 建立 exact inverse legality；
3. 重新整理 inverse tree / odd skeleton；
4. 把 $(4^j-1)/3$ 等舊「高速公路」族放回 inverse-fiber 架構；
5. 明確區分 local bijection、global merge 與 inverse-tree coverage。
