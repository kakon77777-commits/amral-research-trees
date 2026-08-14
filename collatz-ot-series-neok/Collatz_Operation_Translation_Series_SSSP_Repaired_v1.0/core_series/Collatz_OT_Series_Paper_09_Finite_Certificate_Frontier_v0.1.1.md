# Finite Certificate Frontier：Collatz 有限精確覆蓋與全域鴻溝
## ——從 Local Affine Atlas、Descent Sieve 到 Integer-Anchored Hard Branch 的系列封頂

**English Title:** *Finite Certificate Frontiers for the Collatz Map: Exact Finite Coverage, Hard Prefix Domains, and the Remaining Global Quantifier Gap*

**作者：** Neo.K  
**機構：** 一言諾科技有限公司（EveMissLab）  
**系列：** Collatz Operation Translation Series — Paper 09  
**版本：** v0.1.1  
**日期：** 2026-08-11  
**修訂日期：** 2026-08-14

---

## 摘要

本系列前八篇已將 modified Collatz map

$$
T(n)=
\begin{cases}
n/2,&n\equiv0\pmod2,\\[2mm]
(3n+1)/2,&n\equiv1\pmod2
\end{cases}
$$

的有限局部動力分解為：

$$
\boxed{
\text{finite parity word}
\longleftrightarrow
\text{unique residue cylinder}
\longrightarrow
\text{exact affine operator}
\longrightarrow
\text{local identity chart}
}
$$

並建立：

$$
T^k(r_w+2^ka)=m_w+3^{u(w)}a,
$$

$$
T^k(n)<n
\iff
b_w<(2^k-3^{u(w)})n,
$$

以及 exact inverse recovery、valuation language、generalized $mx+r$ 與 RCOT algebraic boundary。

本文完成最後一步：將上述局部結構整理為**有限精確證書系統**，並明確標示 finite verification 與 Collatz 全域猜想之間最後不能被跨越的量詞鴻溝。

本文首先採用 coefficient stopping-time 形式。對 $n>1$，定義：

$$
\boxed{
\sigma(n)
=
\inf\{j\ge1:T^j(n)<n\}.
}
$$

若所有 $n>1$ 都有有限 $\sigma(n)$，則由 strong induction 可推出所有正整數最終進入 $1\leftrightarrow2$ cycle。因此：

$$
\boxed{
\text{Collatz conjecture}
\iff
\forall n>1,\ \sigma(n)<\infty.
}
$$

對 finite parity word

$$
w=w_1\cdots w_k
$$

及其每個 prefix $w_{\le j}$，令：

$$
u_j=u(w_{\le j}),
\qquad
b_j=b_{w_{\le j}},
\qquad
\Delta_j=2^j-3^{u_j}.
$$

由前文 exact affine formula：

$$
T^j(n)-n
=
\frac{b_j-\Delta_jn}{2^j}.
$$

因此一個輸入在前 $k$ 步內**尚未下降**的條件可以完全 exact 化。定義 hard-prefix domain：

$$
\boxed{
H_w
=
\left\{
n\in\Omega_w:
T^j(n)\ge n,\ 1\le j\le k
\right\}.
}
$$

若 prefix $w_{\le j}$ 為 expanding-skeleton：

$$
\Delta_j<0,
$$

則 $T^j(n)>n$ 對所有 positive admissible $n$ 自動成立，不對 hard domain 加任何上界。

若：

$$
\Delta_j>0,
$$

則：

$$
T^j(n)\ge n
\iff
n\le
\left\lfloor
\frac{b_j}{\Delta_j}
\right\rfloor.
$$

因此：

$$
\boxed{
H_w
=
\Omega_w
\cap
[1,h(w)]
}
$$

其中：

$$
\boxed{
h(w)
=
\min_{
1\le j\le k,\ \Delta_j>0
}
\left\lfloor
\frac{b_j}{\Delta_j}
\right\rfloor
}
$$

若沒有 contracting prefix，定義：

$$
h(w)=+\infty.
$$

這是本文的第一個核心結果：**一個有限 parity prefix 的「尚未下降集合」不是模糊的動力集合，而是 unique residue cylinder 與一個 exact integer height bound 的交集。**

接著對有限驗證域：

$$
I_N=[2,N]\cap\mathbb Z
$$

定義 depth-$k$ hard frontier：

$$
\boxed{
\mathfrak F_k(N)
=
\{
w\in\{D,U\}^k:
H_w\cap I_N\neq\varnothing
\}.
}
$$

本文證明：

$$
\boxed{
\mathfrak F_k(N)=\varnothing
}
$$

當且僅當：

$$
\boxed{
\sigma(n)\le k
\quad
\forall\,2\le n\le N.
}
$$

因此，對固定有限 $N$，Collatz verification 可完全重寫為：

> 持續 refine residue cylinders，直到 finite hard frontier 為空。

這使 finite verification 成為一個 exact set-cover / frontier-extinction problem，而不必把每個完整 trajectory 當作獨立 proof object。

本文定義五類 finite certificates：

1. **Terminal Certificate**：直接到達 $1$ 或 $2$；
2. **Descent Certificate**：某 finite prefix 滿足 $T^j(n)<n$；
3. **Cylinder Threshold Certificate**：一整個 residue cylinder 在某 exact threshold 以上都下降；
4. **Merge Certificate**：軌跡在有限時間與一個已由較小起點證明的 trajectory 合流；
5. **Inverse/Preimage Certificate**：利用 exact inverse fiber 證明某 state 位於已證明較小起點的 path 上。

一個 finite certificate family：

$$
\boxed{
\mathcal C_N
}
$$

稱為 coverage-complete，若：

$$
\boxed{
I_N
\subseteq
\bigcup_{\gamma\in\mathcal C_N}D_\gamma
}
$$

且每個 certificate 都可由有限整數算術、有限 word recurrence、congruence、transport identity 或明確 dependency graph 檢查。

在最簡 strong-induction 版本中，只需 descent / terminal certificates。若：

$$
T^j(n)<n,
$$

則 $T^j(n)$ 已由較小起點假設證明收斂，所以 $n$ 收斂。Merge / preimage certificates 則進一步允許：

$$
T^j(n)=T^\ell(n_0),
\qquad
n_0<n,
$$

即使共同 merge state 本身未小於 $n$，仍可由 $n_0$ 的已知軌跡繼承收斂。

本文把早期 BCCP 修正成：

$$
\boxed{
\text{finite bidirectional coverage-complete certification}.
}
$$

其合理目標不是直接宣稱「全體自然數已被雙向構造覆蓋」，而是對每個有限 $N$ 建立一個 exact proof-object family：

$$
\mathcal C_N.
$$

本文亦將先前實驗中的 residue threshold compiler 納入純數學框架。對：

$$
n=r+2^ka,
$$

若：

$$
T^k(n)=m_r+3^ua,
$$

則：

$$
T^k(n)<n
$$

等價於：

$$
\boxed{
(2^k-3^u)a>m_r-r.
}
$$

所以每張 contracting chart 可預先編譯成 exact integer quotient threshold：

$$
\boxed{
a>
\frac{m_r-r}{2^k-3^u}.
}
$$

這就是 earlier $k=16$ threshold certificates 的數學本體。先前對 $1\le n<2^{20}$ 的 prototype 中，$k=16$ 直接 strict-descent certificate 數為：

$$
938413,
$$

並可由 Paper 05 的 $58651$ 個 contracting residue classes 加 finite boundary corrections 完整解釋。

本文進一步處理最容易被誤用的「無限 hard tree」。對每個 formal infinite parity sequence，其 nested residues：

$$
r_k\bmod2^k
$$

自然定義一個 $2$-adic integer；但該 $2$-adic integer 不一定是 ordinary positive integer。因此：

$$
\boxed{
\text{infinite formal hard branch}
\not\Rightarrow
\text{positive-integer Collatz counterexample}.
}
$$

為了精確對應普通正整數，本文定義 **integer-anchored branch**。若一條 nested branch 的 canonical residues：

$$
0\le r_k<2^k
$$

存在某個固定：

$$
n\in\mathbb Z_{>0}
$$

使：

$$
\boxed{
r_k=n
}
$$

對所有 sufficiently large $k$ 成立，則稱該 branch anchored at $n$。這一 eventual stabilization 條件恰好刻畫 ordinary positive integer embedded in $\mathbb Z_2$。

本文證明：

$$
\boxed{
\sigma(n)=\infty
}
$$

當且僅當 $n$ 的 parity-prefix chain 構成一條 anchored hard branch，亦即：

$$
\boxed{
n\in H_{w_{\le k}(n)}
\quad
\forall k.
}
$$

因此：

$$
\boxed{
\text{Collatz conjecture}
\iff
\text{there exists no integer-anchored infinite hard branch for }n>1.
}
$$

這個表述比「hard-prefix tree well-founded」更精確。若要求**所有 formal $2$-adic hard branches** 都消失，則會得到一個過強條件；Collatz 只需排除由 ordinary positive integer anchor 的無限 obstruction。

本文同時得到另一個 exact 全域形式：

$$
\boxed{
\forall N\ge2,\ \exists K(N)<\infty:
\mathfrak F_{K(N)}(N)=\varnothing.
}
$$

這與：

$$
\forall n>1,\ \sigma(n)<\infty
$$

等價，但不能一般交換成：

$$
\boxed{
\exists K\ \forall N:
\mathfrak F_K(N)=\varnothing.
}
$$

後者等價於所有 stopping times 有一個全域 uniform bound，遠強於 Collatz，而且與已知／觀察到的 unbounded stopping-time behavior 不相容。

這正是本系列最後的量詞邊界：

$$
\boxed{
\forall N\,\exists K(N)
\not\Rightarrow
\exists K\,\forall N.
}
$$

2026 年 Angeltveit 的 finite verification algorithm 與本文的 certificate viewpoint 高度一致：其演算法按最低 $k$ bits 遞迴分裂，使用 descent sieve、preimage sieve 與 path-merging sieve，且明確指出需要 explicit checking 的比例可趨近 0，但實際待檢整數數量仍趨向無限。Barina 的公開驗證則已將完整 verification frontier 推進至 $2^{71}$。這些成果都支持本文最後的定位：**有限 residue-class pruning 可以極強，甚至讓 survivor density 趨零，但 finite computational completeness 與 infinite universal proof 仍是不同命題。**

本文因此以以下句子封頂整個九篇系列：

$$
\boxed{
\textbf{Collatz dynamics is locally affine-trivializable,
finitely certificate-compressible,
but globally itinerary-unresolved.}
}
$$

中文：

> **考拉茲動力在固定有限判定域內可被精確仿射化甚至局部平凡化；任意有限範圍可被組織成可機器檢查的有限證書覆蓋問題；但全域猜想仍等價於排除所有普通正整數所錨定的無限未下降 itinerary。**

本文不宣稱完成 Collatz 猜想。它完成的是：把本系列可以 exact 化的部分全部 exact 化，並把不能由這些局部定理自動推出的最後全稱義務明確隔離。

**關鍵詞：** Collatz conjecture、finite certificate、stopping time、residue cylinder、descent sieve、path merging、hard frontier、2-adic parity、strong induction、operation translation

---

# 1. 系列最後的 Proof Obligation

Collatz 猜想可以寫成：

$$
\forall n>0,\quad
T^j(n)\in\{1,2\}
$$

對某個 $j$。

但對 strong induction，更方便使用 stopping-time form。

---

# 2. Coefficient Stopping Time

對：

$$
n>1,
$$

定義：

$$
\boxed{
\sigma(n)
=
\inf\{j\ge1:T^j(n)<n\}.
}
$$

若不存在，令：

$$
\sigma(n)=\infty.
$$

注意：

$$
\sigma(1)
$$

不需要定義成 finite，因 $1$ 是 induction base / terminal cycle 成員。

---

# 3. Finite Stopping Time $\Rightarrow$ Collatz

## Theorem 3.1

若：

$$
\boxed{
\sigma(n)<\infty
\quad
\forall n>1,
}
$$

則 Collatz conjecture 成立。

### 證明

對 $n$ strong induction。

base：

$$
1
$$

已在 terminal cycle。

對：

$$
n>1,
$$

存在：

$$
j
$$

使：

$$
T^j(n)<n.
$$

由 induction hypothesis：

$$
T^j(n)
$$

最終到 1。

故 $n$ 亦最終到 1。

證畢。

---

# 4. Collatz $\Rightarrow$ Finite Stopping Time

若 $n>1$ 最終到：

$$
1<n,
$$

則沿途第一次落到 $n$ 以下即給：

$$
\sigma(n)<\infty.
$$

所以：

## Theorem 4.1

$$
\boxed{
\text{Collatz}
\iff
\forall n>1,\ \sigma(n)<\infty.
}
$$

這是本文 global equivalence 的基礎。

---

# 5. Prefix Affine Data

對 length-$k$ word：

$$
w=w_1\cdots w_k,
$$

令 prefix：

$$
w_{\le j}=w_1\cdots w_j.
$$

記：

$$
u_j=u(w_{\le j}),
$$

$$
b_j=b_{w_{\le j}}.
$$

則 Paper 02：

$$
\boxed{
T^j(n)
=
\frac{3^{u_j}n+b_j}{2^j}
}
$$

對：

$$
n\in\Omega_w
$$

及：

$$
1\le j\le k
$$

成立。

---

# 6. Prefix Drift Gap

定義：

$$
\boxed{
\Delta_j
=
2^j-3^{u_j}.
}
$$

所以：

$$
\boxed{
T^j(n)-n
=
\frac{b_j-\Delta_jn}{2^j}.
}
$$

每個 prefix 是否已經 strict descent 因而是一個 exact linear inequality。

---

# 7. Hard Prefix Domain

## Definition 7.1

$$
\boxed{
H_w
=
\left\{
n\in\Omega_w:
T^j(n)\ge n
\quad
\forall\,1\le j\le k
\right\}.
}
$$

也就是：

> 所有具有 prefix $w$，但到 depth $k$ 仍沒有取得 strong-induction descent certificate 的正整數。

---

# 8. Expanding Prefix 對 Hard Domain 不加限制

若：

$$
\Delta_j<0,
$$

即：

$$
3^{u_j}>2^j,
$$

則：

$$
b_j-\Delta_jn
=
b_j+(3^{u_j}-2^j)n>0.
$$

所以：

$$
\boxed{
T^j(n)>n
}
$$

對所有 positive admissible $n$。

因此此 prefix 不可能提供 descent certificate。

---

# 9. Contracting Prefix 給 Hard Height

若：

$$
\Delta_j>0,
$$

則：

$$
T^j(n)\ge n
$$

iff：

$$
b_j\ge\Delta_jn.
$$

所以：

$$
\boxed{
n
\le
\left\lfloor
\frac{b_j}{\Delta_j}
\right\rfloor.
}
$$

因此 contracting prefix 對仍未下降者產生一個 exact upper bound。

---

# 10. Hard Height Theorem

定義：

$$
\boxed{
h(w)
=
\min_{
j\le k,\ \Delta_j>0
}
\left\lfloor
\frac{b_j}{\Delta_j}
\right\rfloor
}
$$

若沒有：

$$
\Delta_j>0,
$$

令：

$$
h(w)=+\infty.
$$

則：

## Theorem 10.1

$$
\boxed{
H_w
=
\Omega_w
\cap
[1,h(w)].
}
$$

若：

$$
h(w)=+\infty,
$$

即：

$$
H_w=\Omega_w.
$$

---

# 11. 證明

$n\in H_w$ iff 對所有 prefix：

$$
T^j(n)\ge n.
$$

expanding prefix 自動成立。

contracting prefix 要求：

$$
n\le
\left\lfloor b_j/\Delta_j\right\rfloor.
$$

所以全部條件的交集就是最小 upper bound。

證畢。

---

# 12. 這個結果的重要性

一個 hard domain 不需要保存：

$$
T(n),T^2(n),\ldots,T^k(n)
$$

的整條 numerical path。

只需保存：

$$
\boxed{
(r_w,2^k,h(w)).
}
$$

即：

$$
\boxed{
\text{one residue cylinder}
\cap
\text{one height cap}.
}
$$

這是 finite obstruction 的高度壓縮形式。

---

# 13. Hard Domain 可能是有限的，也可能是無限的

若 word 到目前為止至少出現一個 contracting prefix：

$$
h(w)<\infty,
$$

則：

$$
H_w
$$

是 finite set。

若所有 prefixes 都在 expanding-skeleton side：

$$
h(w)=\infty,
$$

則：

$$
H_w=\Omega_w
$$

仍是一個 infinite arithmetic progression。

所以 hard-prefix analysis 同時區分：

- finite correction obstruction；
- pure skeleton obstruction。

---

# 14. Finite Verification Interval

固定：

$$
N\ge2.
$$

定義：

$$
\boxed{
I_N
=
\{2,3,\ldots,N\}.
}
$$

我們只問：

> $I_N$ 內每個 starting value 是否已取得 finite stopping-time certificate？

---

# 15. Depth-$k$ Hard Frontier

定義：

$$
\boxed{
\mathfrak F_k(N)
=
\left\{
w\in\{D,U\}^k:
H_w\cap I_N\neq\varnothing
\right\}.
}
$$

每個 element 是：

> 到 depth $k$ 仍至少含一個未下降 starting value 的 parity cylinder。

---

# 16. Frontier Extinction Theorem

## Theorem 16.1

$$
\boxed{
\mathfrak F_k(N)=\varnothing
}
$$

iff：

$$
\boxed{
\sigma(n)\le k
\quad
\forall n\in I_N.
}
$$

### 證明

如果 frontier 為空，則任意 $n\le N$ 的 length-$k$ parity word $w_k(n)$ 不含 $n$ 於 $H_w$，所以存在 $j\le k$：

$$
T^j(n)<n.
$$

反之，若所有 $n\le N$ 在 $k$ 步內下降，則沒有任何 hard domain 能和 $I_N$ 相交。

證畢。

---

# 17. Finite Verification 的 Frontier Form

所以對 fixed $N$：

$$
\boxed{
\text{verify Collatz on }[2,N]
}
$$

等價於：

$$
\boxed{
\text{refine hard cylinders until }\mathfrak F_k(N)=\varnothing.
}
$$

這不是 heuristic。

是 exact finite equivalence。

---

# 18. Finite Certificate 的基本定義

一個 finite certificate：

$$
\gamma
$$

包含：

1. source domain $D_\gamma$；
2. finite word / affine data；
3. claim type；
4. exact target relation；
5. 若需要，dependency on previously certified objects。

並要求：

$$
\boxed{
\text{all checks terminate in finite exact arithmetic}.
}
$$

---

# 19. Terminal Certificate

若：

$$
T^j(n)\in\{1,2\},
$$

則：

$$
\boxed{
\gamma_T(n,j)
}
$$

直接證明收斂。

其 dependency rank 為 0。

---

# 20. Descent Certificate

若：

$$
T^j(n)<n,
$$

則：

$$
\boxed{
\gamma_D(n,j)
}
$$

透過 strong induction 證明 $n$ 收斂。

這是最基本 finite certificate。

---

# 21. Cylinder Threshold Certificate

對 word $w$：

$$
T^k(n)
=
\frac{3^un+b_w}{2^k}.
$$

若：

$$
3^u<2^k,
$$

定義：

$$
\theta_w
=
\left\lfloor
\frac{b_w}{2^k-3^u}
\right\rfloor+1.
$$

則：

$$
\boxed{
D_{\gamma_w}
=
\{
n\in\Omega_w:n\ge\theta_w
\}
}
$$

中的全部 starting values 共享同一 descent proof。

所以一個 certificate 可以覆蓋 infinite arithmetic subset。

---

# 22. Quotient-Threshold Compiler

寫：

$$
n=r_w+2^ka,
$$

以及：

$$
T^k(n)=m_w+3^ua.
$$

則：

$$
T^k(n)<n
$$

iff：

$$
m_w+3^ua
<
r_w+2^ka.
$$

所以：

$$
\boxed{
(2^k-3^u)a
>
m_w-r_w.
}
$$

若：

$$
2^k>3^u,
$$

可以預先編譯：

$$
\boxed{
a
>
\frac{m_w-r_w}{2^k-3^u}.
}
$$

這是 integer hot-loop certificate，而不是 floating log approximation。

---

# 23. Exact Quotient Threshold

可定義：

$$
\boxed{
q_w
=
\left\lfloor
\frac{m_w-r_w}
{2^k-3^u}
\right\rfloor+1.
}
$$

則：

$$
\boxed{
a\ge q_w
\Rightarrow
T^k(r_w+2^ka)
<
r_w+2^ka.
}
$$

所以 certificate payload 可縮成：

$$
\boxed{
(r_w,k,u,m_w,q_w).
}
$$

---

# 24. 與 Earlier $k=16$ Prototype 的對接

先前 prototype 對：

$$
1\le n<2^{20}
$$

使用：

$$
k=16.
$$

Paper 05 已證 length-16 contracting residue classes：

$$
\boxed{
58651
}
$$

個。

經 finite positive-domain 與 strict-equality corrections，

實際 direct strict-descent certificate：

$$
\boxed{
938413
}
$$

個 starting values。

因此早期 benchmark 的「pruning」可以完全重新解讀為：

$$
\boxed{
\text{finite certificate coverage ratio}.
}
$$

---

# 25. Merge Certificate

descent 不是唯一可用 strong-induction information。

若：

$$
T^j(n)
=
T^\ell(n_0)
$$

且：

$$
n_0<n,
$$

則由 induction hypothesis：

$$
n_0
$$

收斂。

因此其後續 state：

$$
T^\ell(n_0)
$$

收斂。

所以 $n$ 也收斂。

定義：

$$
\boxed{
\gamma_M
=
(n,n_0,j,\ell)
}
$$

為 merge certificate。

---

# 26. Path Merging 不要求 Merge State 小於 $n$

重要的是：

$$
n_0<n,
$$

而不是：

$$
T^j(n)<n.
$$

所以 merge sieve 可以比單純 descent sieve 排除更多 starting values。

這和 2026 年 Angeltveit 的 path-merging sieve 完全相容。

---

# 27. Preimage / Inverse-Fiber Certificate

如果可證：

$$
n=T^\ell(n_0)
$$

對某：

$$
n_0<n,
$$

則 $n$ 本身位於已證明較小 starting value 的 trajectory 上。

例如 modified inverse：

$$
n\equiv2\pmod3
$$

時：

$$
n=T\left(\frac{2n-1}{3}\right).
$$

若：

$$
\frac{2n-1}{3}<n,
$$

則可直接排除 $n$ 作為新 starting case。

這是 preimage certificate。

---

# 28. Paper 04 的 Inverse Fiber 進入 Certificate System

accelerated odd map：

$$
R_\kappa(t)
=
\frac{2^\kappa t-1}{3}.
$$

若：

$$
2^\kappa t\equiv1\pmod3,
$$

則 $R_\kappa(t)$ 是 $t$ 的 exact odd predecessor。

所以 inverse-fiber data 可以作：

- merge proof；
- preimage sieve；
- known terminal basin certificate。

---

# 29. Certificate Dependency Graph

若只用 descent certificates，

strong induction 本身提供 dependency：

$$
n\to m<n.
$$

如果加入 merge / preimage，

可建立 directed dependency graph：

$$
\gamma_i\to\gamma_j.
$$

要求存在 rank：

$$
\rho:\mathcal C_N\to\mathbb N
$$

使每條 dependency edge：

$$
\boxed{
\rho(\gamma_j)<\rho(\gamma_i).
}
$$

則 finite dependency graph 無 cycle，

所有 certificates 最終落到 terminal objects。

---

# 30. Coverage-Complete Certificate Family

## Definition 30.1

對：

$$
I_N=[2,N],
$$

finite family：

$$
\mathcal C_N
$$

若滿足：

$$
\boxed{
I_N
\subseteq
\bigcup_{\gamma\in\mathcal C_N}D_\gamma
}
$$

且所有 certificate claims / dependencies 都 exact-valid，

則稱：

$$
\boxed{
\mathcal C_N
\text{ coverage-complete}.
}
$$

---

# 31. Finite Certificate Completeness Theorem

若：

$$
\mathcal C_N
$$

coverage-complete，

且 dependency graph well-ranked to terminal cases，

則：

$$
\boxed{
\text{Collatz is verified for every }2\le n\le N.
}
$$

這是 finite theorem。

---

# 32. BCCP 的正式修正版

舊 BCCP：

$$
\text{Forward}
+
\text{Backward}
+
\text{Coverage}.
$$

現在可以重寫為：

### Forward certificate

finite word / affine descent。

### Backward certificate

preimage / inverse fiber / merge。

### Coverage completeness

$$
I_N
\subseteq
\cup D_\gamma.
$$

所以：

$$
\boxed{
\text{BCCP}_{\mathrm{finite}}
=
\text{bidirectional finite proof-object coverage}.
}
$$

---

# 33. 為什麼 Finite BCCP 是嚴格的？

因為對固定：

$$
N,
$$

所有：

- source values；
- words；
- congruences；
- inequalities；
- dependency graph；

都是 finite。

因此可以由 independent checker 重算。

不需要：

- probabilistic extrapolation；
- decimal digit heuristic；
- infinite tree assertion。

---

# 34. Machine-Checkable Certificate Schema

概念上，一個 chart certificate 可以保存：

$$
\boxed{
\gamma=
(
\text{type},
w,k,u,b,r,m,
L,U,
\theta,
\text{dependencies}
).
}
$$

其中：

- $w$：parity word；
- $k$：depth；
- $u$：odd-step count；
- $b$：affine correction；
- $r$：source residue；
- $m$：target base；
- $[L,U]$：有限 coverage range；
- $\theta$：descent threshold；
- dependencies：merge/preimage reference。

checker 只需驗：

$$
F_w(x)
=
\frac{3^ux+b}{2^k},
$$

$$
r\equiv-b3^{-u}\pmod{2^k},
$$

及對應 inequality / merge identity。

---

# 35. Proof Object 與 Trajectory Log 的差異

trajectory log 保存：

$$
n,T(n),T^2(n),\ldots.
$$

certificate 保存：

$$
\boxed{
\text{an entire congruence family plus a finite proof rule}.
}
$$

所以：

$$
\boxed{
\text{trajectory enumeration}
\to
\text{structural proof compression}.
}
$$

這是 operation translation 對 finite verification 的核心價值。

---

# 36. 與 Angeltveit 2026 Algorithm 的對照

Angeltveit 的 2026 verification algorithm：

1. 按 least significant bits recursive split；
2. 對同 residue family 同時處理；
3. 使用 descent sieve；
4. 使用 mod-$9$ preimage sieve；
5. 使用 path-merging sieve；
6. 對剩餘 survivors 再 explicit iterate。

這與本文：

$$
\boxed{
\text{residue frontier}
+
\text{descent certificates}
+
\text{inverse/merge certificates}
}
$$

高度一致。

---

# 37. 但本文不是宣稱該 Verification Idea 是新發現

low-bit parity grouping、lookup-table sieve、descent sieve、preimage sieve 都有既有 computational Collatz 傳統。

Angeltveit 亦明確說明其中多項 sieve 是 standard ideas，而其新點主要在遞迴加 bits 與整體 algorithmic scaling。

本文的工作是：

$$
\boxed{
\text{把前八篇 local algebra 統一成 certificate semantics}.
}
$$

---

# 38. Finite Frontier 的 Current Computational Context

Barina 已公開報告：

$$
\boxed{
n<2^{71}
}
$$

的完整 convergence verification。

Angeltveit 2026 則提出：

> 從 $2^N$ 擴張到 $2^{N+1}$ 所需時間成長可壓到小於 factor 2，

並估計其方法可能用近似資源推到更高範圍。

這些都是：

$$
\boxed{
\text{finite certificate / computation frontier}
}
$$

的進展，

而非 infinite proof。

---

# 39. Survivor Fraction $\to0$ 仍不等於 Proof

Angeltveit 指出：

隨：

$$
N\to\infty,
$$

需要 explicit checking 的 fraction 可趨近：

$$
0.
$$

但他同時明確指出：

$$
\boxed{
\text{the number of integers to check still goes to infinity}.
}
$$

這一句幾乎就是本文 global quantifier gap 的 computational version。

---

# 40. 為什麼不能從「比例趨零」推全稱？

因為：

$$
\boxed{
\frac{|E_N|}{N}\to0
}
$$

不代表：

$$
\boxed{
E_N=\varnothing
}
$$

對 sufficiently large $N$。

甚至可能：

$$
|E_N|\to\infty
$$

同時：

$$
|E_N|/N\to0.
$$

所以：

$$
\boxed{
\text{density-zero survivors}
\neq
\text{no survivors}.
}
$$

這和 Paper 05：

$$
P_k\to1
$$

的量詞警告完全一致。

---

# 41. Infinite Hard Branch 的誘惑

自然會想：

> 如果 hard-prefix tree 沒有 infinite branch，不就證明 Collatz？

作為 sufficient condition 是對的。

但若把它當成 equivalent condition，會過強。

原因在 $2$-adic completion。

---

# 42. Infinite Parity Prefix Defines a $2$-adic Integer

Paper 03：

每個 finite parity prefix對應：

$$
r_k\bmod2^k.
$$

nested prefixes：

$$
r_{k+1}\equiv r_k\pmod{2^k}.
$$

所以：

$$
(r_k)
$$

定義一個 inverse-limit point：

$$
\boxed{
x\in\mathbb Z_2.
}
$$

但：

$$
x
$$

未必在：

$$
\mathbb Z_{>0}.
$$

---

# 43. Formal Infinite Branch 不是普通整數反例

因此可能存在：

$$
\boxed{
\text{an infinite formal parity/hard branch}
}
$$

但其 $2$-adic limit：

$$
x
$$

是：

- negative integer；
- nonordinary $2$-adic integer；
- 或其他不在 positive naturals 的點。

所以：

$$
\boxed{
\text{formal branch existence}
\not\Rightarrow
\text{positive-integer counterexample}.
}
$$

---

# 44. Canonical Residues

每個 modulo：

$$
2^k
$$

class 選 canonical representative：

$$
\boxed{
0\le r_k<2^k.
}
$$

若 branch 來自固定普通正整數 $n$，

則當：

$$
2^k>n,
$$

有：

$$
\boxed{
r_k=n.
}
$$

所以 canonical residues 會 eventually stabilize。

---

# 45. Integer-Anchored Branch

## Definition 45.1

一條 infinite nested parity branch：

$$
w_1\prec w_2\prec\cdots
$$

稱為 anchored at：

$$
n\in\mathbb Z_{>0}
$$

若存在：

$$
K
$$

使：

$$
\boxed{
r_{w_k}=n
\quad
\forall k\ge K.
}
$$

這等價於其 $2$-adic point正好是 ordinary positive integer $n$。

---

# 46. Anchored Hard Branch

若進一步：

$$
\boxed{
n\in H_{w_k}
\quad
\forall k,
}
$$

則稱為：

$$
\boxed{
\text{integer-anchored infinite hard branch}.
}
$$

也就是：

> 同一個 ordinary positive integer $n$ 在所有 finite depths 都沒有取得 descent certificate。

---

# 47. Counterexample Equivalence Theorem

## Theorem 47.1

對：

$$
n>1,
$$

以下等價：

1. $\sigma(n)=\infty$；
2. 對所有 $k$：
   $$
   T^j(n)\ge n
   \quad
   1\le j\le k;
   $$
3. $n$ 的 parity-prefix chain 是 integer-anchored infinite hard branch。

### 證明

(1)$\Rightarrow$(2)：stopping time infinite 的定義。

(2)$\Rightarrow$(3)：$n$ 的 canonical residue 在 $2^k>n$ 後等於 $n$，且每個 prefix hard。

(3)$\Rightarrow$(1)：若某 finite $j$ descent，則所有更長 prefix 不再 hard，矛盾。

證畢。

---

# 48. Global Collatz 的最小 Obstruction Form

所以：

## Theorem 48.1

$$
\boxed{
\text{Collatz conjecture}
}
$$

等價於：

$$
\boxed{
\text{不存在 anchored at }n>1
\text{ 的 infinite hard branch}.
}
$$

這是本文認為最乾淨的 global remainder statement。

---

# 49. 為什麼不是「整棵 Hard Tree Well-Founded」？

如果要求：

$$
\boxed{
\text{no infinite formal hard branch in }\mathbb Z_2,
}
$$

那會排除所有 nonordinary $2$-adic obstruction。

Collatz 猜想本身沒有要求這一點。

因此：

$$
\boxed{
\text{2-adic global well-foundedness}
}
$$

是更強命題。

本文只保留：

$$
\boxed{
\text{positive-integer anchored well-foundedness}.
}
$$

---

# 50. Finite Frontier Function

若 Collatz 對：

$$
[2,N]
$$

已驗證，

定義：

$$
\boxed{
K(N)
=
\min
\{
k:
\mathfrak F_k(N)=\varnothing
\}.
}
$$

它就是：

$$
\boxed{
K(N)=\max_{2\le n\le N}\sigma(n)
}
$$

在 strict stopping-time 定義下。

因此 finite certificate depth 是一個自然的 frontier complexity statistic。

---

# 51. Global Conjecture 的 Quantifier Form

Collatz 等價：

$$
\boxed{
\forall N\ge2,\ \exists K(N)<\infty:
\mathfrak F_{K(N)}(N)=\varnothing.
}
$$

注意量詞順序：

$$
\boxed{
\forall N\,\exists K(N).
}
$$

---

# 52. 不可偷換成 Uniform Depth

更強命題：

$$
\exists K\ \forall N:
\mathfrak F_K(N)=\varnothing.
$$

等價於：

$$
\boxed{
\sigma(n)\le K
\quad
\forall n>1.
}
$$

即所有 stopping times 有 uniform global bound。

Collatz 不需要這件事。

所以：

$$
\boxed{
\forall N\,\exists K(N)
\not\equiv
\exists K\,\forall N.
}
$$

---

# 53. 這就是本系列最後的量詞鴻溝

前八篇可以：

- 對 fixed $w$ exact；
- 對 fixed $k$ exact；
- 對 fixed $N$ exact；
- 對 finite family exact。

但 Collatz 是：

$$
\boxed{
\forall n
}
$$

的無界 statement。

因此任何 finite certificate framework 若沒有額外 theorem 控制：

$$
K(N)
$$

或 anchored hard branches，

都不能單靠「對每個已測 $N$ 成功」升級成 global proof。

---

# 54. Finite Certificate Frontier

本文最終把：

$$
\boxed{
\mathfrak F_k(N)
}
$$

稱為 **Finite Certificate Frontier** 的 hard side。

相對地，已被：

- descent；
- merge；
- preimage；
- terminal；

certified 的 domains 構成 certified side。

因此：

$$
I_N
=
\boxed{
\text{Certified Region}
\sqcup
\text{Hard Frontier}.
}
$$

---

# 55. Frontier Refinement

從 depth：

$$
k
$$

到：

$$
k+1,
$$

只需展開：

$$
\mathfrak F_k(N)
$$

中的 cylinders。

已 certified charts 不需再展開。

所以 algorithmic search tree 是：

$$
\boxed{
\text{expand only surviving proof obligations}.
}
$$

這是 certificate-oriented computation 的自然形式。

---

# 56. Hard Frontier 的 Monotonicity

對 fixed $N$，考慮未證明 starting-value set：

$$
E_k(N)
=
\{
n\in I_N:
\sigma(n)>k
\}.
$$

則：

$$
\boxed{
E_{k+1}(N)\subseteq E_k(N).
}
$$

而：

$$
\mathfrak F_k(N)
$$

只是 $E_k(N)$ 在 level-$k$ residue atlas 中的 compressed representation。

所以：

$$
\boxed{
\text{frontier refinement is monotone in obligations}.
}
$$

---

# 57. Certificate Compression Ratio

可定義：

$$
\boxed{
\eta_k(N)
=
1-
\frac{|E_k(N)|}{N-1}.
}
$$

表示 depth-$k$ 已取得 descent certificate 的 starting-value fraction。

也可定義 chart-level：

$$
\boxed{
\eta_k^{\mathrm{chart}}
=
1-
\frac{|\mathfrak F_k(N)|}{2^k}
}
$$

但兩者不應混淆。

Paper 05 已展示：

$$
\boxed{
\text{chart density}
\neq
\text{finite strict certificate density}
}
$$

在 finite boundary 下會有小差異。

---

# 58. Certificate Minimality 不是必要條件

一個 finite range 可能有很多不同 certificate families：

$$
\mathcal C_N.
$$

可以追求：

- minimum certificate count；
- minimum total word length；
- minimum verifier work；
- maximum cylinder coverage；
- maximum merge reuse。

但這些是 proof compression optimization，

不影響 logical validity。

---

# 59. Proof Complexity 與 Truth 分離

Collatz 對：

$$
[2,N]
$$

為真，

只代表存在某種 finite brute-force proof。

RCOT certificate framework 關心的是：

$$
\boxed{
\text{能否用更結構化、更小、更可重用的 proof objects 表達}.
}
$$

因此：

$$
\boxed{
\text{verification complexity}
\neq
\text{mathematical truth}.
}
$$

---

# 60. 本系列最終結構圖

Paper 01：

$$
\text{舊研究證據校正}.
$$

Paper 02：

$$
\text{finite word}\to\text{affine operator}.
$$

Paper 03：

$$
\text{word}\leftrightarrow2^k\text{ cylinder}\to\text{identity chart}.
$$

Paper 04：

$$
2^k\text{ source}\leftrightarrow3^u\text{ target}.
$$

Paper 05：

$$
\text{exact contraction boundary}.
$$

Paper 06：

$$
\text{valuation-language compression}.
$$

Paper 07：

$$
mx+r\text{ generalization}.
$$

Paper 08：

$$
\text{algebraic domain / breakage ladder}.
$$

Paper 09：

$$
\boxed{
\text{all local results}
\to
\text{finite proof-object frontier}
\to
\text{global quantifier boundary}.
}
$$

---

# 61. 本文主要定理總結

## Theorem A — Collatz / Finite Stopping-Time Equivalence

$$
\boxed{
\text{Collatz}
\iff
\forall n>1,\sigma(n)<\infty.
}
$$

## Theorem B — Hard Height Formula

$$
\boxed{
H_w
=
\Omega_w\cap[1,h(w)].
}
$$

## Theorem C — Frontier Extinction

$$
\boxed{
\mathfrak F_k(N)=\varnothing
\iff
\sigma(n)\le k
\quad\forall2\le n\le N.
}
$$

## Theorem D — Cylinder Quotient Certificate

$$
\boxed{
(2^k-3^u)a>m_w-r_w
\Rightarrow
T^k(n)<n.
}
$$

## Theorem E — Finite Coverage Completeness

$$
\boxed{
I_N
\subseteq
\bigcup_{\gamma\in\mathcal C_N}D_\gamma
}
$$

plus valid ranked dependencies implies convergence for all $n\le N$.

## Theorem F — Anchored Hard Branch Equivalence

$$
\boxed{
\sigma(n)=\infty
\iff
n\text{ anchors an infinite hard branch}.
}
$$

## Theorem G — Global Frontier Form

$$
\boxed{
\text{Collatz}
\iff
\forall N\ge2,\exists K(N):
\mathfrak F_{K(N)}(N)=\varnothing.
}
$$

---

# 62. 本文不證明什麼？

本文沒有證明：

$$
\mathfrak F_k(N)
$$

對所有 $N$ 具有 uniform extinction depth。

沒有證明：

$$
K(N)
$$

的 closed asymptotic upper bound。

沒有排除 integer-anchored infinite hard branch。

沒有把：

$$
P_k\to1
$$

或 survivor density $\to0$ 轉換成 emptiness。

沒有因為 finite verification 已達 $2^{71}$ 就推斷 infinite domain。

因此本文不是 Collatz proof。

---

# 63. 系列最終結論

經九篇後，可以非常精確地說：

### 已完成

$$
\boxed{
\text{finite-word arithmetic}
}
$$

可 exact affine compression。

$$
\boxed{
\text{finite itinerary legality}
}
$$

可 exact residue coding。

$$
\boxed{
\text{fixed-chart dynamics}
}
$$

可 identity trivialization。

$$
\boxed{
\text{forward / inverse local transport}
}
$$

可 exact recovery。

$$
\boxed{
\text{finite contraction}
}
$$

有 exact threshold。

$$
\boxed{
\text{finite range verification}
}
$$

可重寫成 certificate coverage / frontier extinction。

### 尚未完成

$$
\boxed{
\text{all ordinary positive-integer itineraries}
}
$$

是否都在有限時間取得 descent / merge / terminal certificate。

---

# 64. 最終母句

本系列最終核心句為：

$$
\boxed{
\textbf{Collatz dynamics is locally affine-trivializable,
finitely certificate-compressible,
but globally itinerary-unresolved.}
}
$$

中文：

> **考拉茲動力在有限合法判定域內可以被精確仿射化甚至局部平凡化；任意有限驗證域可以被壓縮成可機器檢查的證書覆蓋問題；但全域猜想仍要求排除所有由普通正整數錨定的無限未下降 itinerary。**

因此真正未解的不是：

$$
\boxed{
\text{how to compute one finite Collatz block}.
}
$$

而是：

$$
\boxed{
\text{whether every positive-integer anchored itinerary eventually leaves the hard frontier}.
}
$$

至此，本系列封頂。

---

# 參考文獻

1. Vigleik Angeltveit, *An improved algorithm for checking the Collatz conjecture for all $n<2^N$*, arXiv:2602.10466 (2026).
2. David Barina, *Improved verification limit for the convergence of the Collatz conjecture*, The Journal of Supercomputing 81, 810 (2025).
3. David Barina, *Convergence verification of the Collatz problem*, The Journal of Supercomputing 77 (2021).
4. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum of Mathematics, Pi 10 (2022), arXiv:1909.03562.
5. Olivier Rozier, Claude Terracol, *Paradoxical behavior in Collatz sequences*, arXiv:2502.00948.
6. Tong Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, arXiv:2605.13886.
7. Mike Winkler, *Deterministic Structures in the Stopping Time Dynamics of the $3x+1$ Problem* (2026 preprint).
8. Collatz Operation Translation Series — Papers 01–08.
9. Operation Translation Series A — Papers 01–07.

---

# 系列封頂聲明

**Collatz Operation Translation Series — Papers 01–09：完成。**

後續若繼續研究，應另立新系列，而不再無限制擴張本系列。

可延伸但未納入本系列的方向包括：

- hard-frontier asymptotics；
- certificate minimization complexity；
- formal proof assistant verification；
- accelerated valuation-code frontier；
- generalized $mx+r$ certificate phase diagrams；
- RCOT in noncommutative/state-machine systems。

上述皆屬新系列，而非本文未完成章節。
