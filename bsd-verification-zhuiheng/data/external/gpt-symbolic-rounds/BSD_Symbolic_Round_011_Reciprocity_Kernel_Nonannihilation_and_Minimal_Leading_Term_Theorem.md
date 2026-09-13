# BSD Symbolic Round 011
## Reciprocity Kernel, Nonannihilation, and the Minimal Leading-Term Theorem

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** conditional symbolic development；未做新的大型數值計算；未主張 BSD 已證明  
**承接：** BSD Symbolic Round 001--010  
**本輪目標：** 將 explicit reciprocity 中的 nonannihilation burden 壓縮到最小；利用 rank-$2$ transverse quotient 的一維性證明 reciprocity kernel 的二分律；區分 reciprocity annihilation 與 directional criticality；建立 determinant nondegeneracy criterion 與 cross-curve nonvanishing transfer。

---

# 1. Round 010 留下的 T5

Round 010 將其中一個主要 theorem-level blocker記為

$$
T5
=
\text{explicit reciprocity / $p$-adic leading-line theorem}.
$$

Round 009 的 order-matching theorem使用 factorization

$$
\mathcal L
=
U\cdot E\cdot\lambda(Z_{\mathrm{tr}}),
$$

並要求 first transverse jet不被

$$
\lambda
$$

annihilate。

當時保留了條件

$$
(\operatorname{id}\otimes\lambda)(\tau_m)\neq0.
\tag{1.1}
$$

本輪的核心問題是：

> 在 rank-$2$ target 中，(1.1) 到底是不是一個真正獨立的大條件？

答案是：在最自然的一維 transverse quotient setup 中，幾乎不是。

---

# 2. Rank-$2$ transverse quotient 是一維

令

$$
H
$$

為二維 $K$-向量空間。

令

$$
L=K\kappa
$$

為 leading line。

定義 transverse quotient

$$
Q
:=
H/L.
\tag{2.1}
$$

則

$$
\boxed{
\dim_K Q=1.
}
\tag{2.2}
$$

令 analytic target fiber也是一維 line

$$
A.
$$

reciprocity map為

$$
\lambda:
Q\longrightarrow A.
\tag{2.3}
$$

因為 domain與codomain都一維，$\lambda$ 的線性代數只有兩種可能：

$$
\lambda=0
$$

或

$$
\lambda\text{ is an isomorphism}.
$$

---

# 3. Reciprocity kernel dichotomy

## Theorem 3.1

若

$$
\dim Q
=
\dim A
=
1,
$$

則：

$$
\boxed{
\ker\lambda
=
Q
\iff
\lambda=0,
}
\tag{3.1}
$$

而若

$$
\lambda\neq0,
$$

則

$$
\boxed{
\ker\lambda=0.
}
\tag{3.2}
$$

因此不存在 proper nonzero reciprocity kernel。

這表示在 rank-$2$ transverse quotient上，不存在：

> first jet剛好落進一個非平凡 proper kernel

這種中間情形。

要嘛 reciprocity map整條 transverse line都殺掉；

要嘛任何 nonzero transverse vector都 survive。

---

# 4. Tensor nonannihilation theorem

令

$$
V
$$

為任意 finite-dimensional $K$-向量空間。

若

$$
\lambda:Q\to A
$$

是 nonzero line map，則它是 injective。

因此

$$
\operatorname{id}_V\otimes\lambda:
V\otimes Q
\longrightarrow
V\otimes A
$$

也是 injective。

## Theorem 4.1

對任意 nonzero

$$
\tau\in V\otimes Q,
$$

若

$$
\lambda\neq0,
$$

則

$$
\boxed{
(\operatorname{id}_V\otimes\lambda)(\tau)\neq0.
}
\tag{4.1}
$$

取

$$
V=\operatorname{Sym}^m(T^\ast),
$$

立即得到：

## Corollary 4.2

若

$$
\tau_m
\in
\operatorname{Sym}^m(T^\ast)\otimes Q
$$

是 first nonzero projective jet，且

$$
\lambda\neq0,
$$

則

$$
\boxed{
(\operatorname{id}\otimes\lambda)(\tau_m)\neq0.
}
\tag{4.2}
$$

所以 global tensor-level nonannihilation不再需要 target-specific額外檢查。

---

# 5. Minimal global order-matching theorem

假設：

1. scalar exceptional factor $E$ 有 order

$$
e;
$$

2. arithmetic projective family first nonzero order是

$$
m;
$$

3. first transverse jet

$$
\tau_m\neq0;
$$

4. reciprocity map

$$
\lambda:Q\to A
$$

非零；

5. analytic unit

$$
U(0)\neq0;
$$

6. analytic section factorizes as

$$
\mathcal L
=
U\cdot E\cdot\lambda(Z_{\mathrm{tr}}).
$$

## Theorem 5.1

在 $\mathfrak m$-adic multivariable order下，

$$
\boxed{
\operatorname{ord}_{\mathfrak m}\mathcal L
=
e+m.
}
\tag{5.1}
$$

不再需要額外假設

$$
\lambda(\tau_m)\neq0.
$$

因為它已由

$$
\tau_m\neq0
$$

與

$$
\lambda\neq0
$$

自動推出。

這將 Round 009 的 nonannihilation burden壓縮成：

$$
\boxed{
\lambda\neq0.
}
\tag{5.2}
$$

---

# 6. T5 因此可以拆成兩部分

原本：

$$
T5
=
\text{explicit reciprocity}
+
\text{nonannihilation}.
$$

本輪顯示在 rank-$2$ line-quotient setup中，可以改寫成：

## T5a. Reciprocity existence / compatibility

構造

$$
\lambda:Q\to A
$$

並證明 analytic factorization。

這仍是 theorem-level。

## T5b. Reciprocity line nonzero

只需證明：

$$
\boxed{
\lambda\neq0.
}
$$

這可能只是一個 scalar nonvanishing certificate。

所以：

$$
\boxed{
T5
\rightsquigarrow
T5a
+
\text{one-dimensional nonzero test}.
}
\tag{6.1}
$$

---

# 7. Nonzero line map只需一個 witness

因為 $Q$ 一維，只要取任意

$$
q\in Q^\times,
$$

則：

## Theorem 7.1

$$
\boxed{
\lambda\neq0
\iff
\lambda(q)\neq0.
}
\tag{7.1}
$$

所以不需要掃很多 classes。

只需找到一個 nonzero transverse witness。

這個 witness可以是：

- 一個 local class；
- 一個 calibrator image；
- 一個 quotient generator；
- 一個 independently normalized Coleman / regulator value。

---

# 8. Lifted functional criterion

reciprocity functional也可以寫在 $H$ 上。

令

$$
\pi:H\to Q
$$

為 quotient map。

定義

$$
\widetilde\lambda
=
\lambda\circ\pi:
H\to A.
\tag{8.1}
$$

則

$$
L
\subset
\ker\widetilde\lambda.
$$

因為 $\dim H=2$：

## Theorem 8.1

$$
\boxed{
\lambda\neq0
\iff
\ker\widetilde\lambda=L.
}
\tag{8.2}
$$

如果 $\lambda=0$，則

$$
\ker\widetilde\lambda=H.
$$

所以 reciprocity nonzero可以被重新表達成：

$$
\boxed{
\text{the lifted analytic functional kills exactly the leading line, not all of }H.
}
\tag{8.3}
$$

---

# 9. Adapted-basis scalar test

取 basis

$$
(\kappa,q)
$$

of $H$，其中

$$
q\notin L.
$$

因為

$$
\widetilde\lambda(\kappa)=0,
$$

有

$$
\widetilde\lambda
=
(0,c)
$$

在該 basis 下。

此時：

$$
\boxed{
\lambda\neq0
\iff
c\neq0.
}
\tag{9.1}
$$

若更換 transverse lift：

$$
q'
=
uq+a\kappa,
\qquad
u\in K^\times,
$$

則

$$
c'
=
u c.
$$

所以：

$$
\boxed{
c\neq0
}
$$

是 basis-independent statement。

absolute value $c$ 依 normalization變動；

nonvanishing不變。

---

# 10. Pairing realization

假設有 perfect pairing

$$
\beta:
H\times H^\vee
\longrightarrow
K.
$$

leading line的 annihilator定義為

$$
L^\perp
=
\{
\eta\in H^\vee:
\beta(\kappa,\eta)=0
\}.
$$

因為 $H$ 二維且 pairing perfect，

$$
\dim L^\perp=1.
$$

任取

$$
\eta\in L^\perp\setminus\{0\}.
$$

定義

$$
\widetilde\lambda_\eta(x)
=
\beta(x,\eta).
$$

則它 annihilate $L$，所以 descend 成

$$
\lambda_\eta:
Q\to K.
$$

## Theorem 10.1

$$
\boxed{
\eta\neq0
\Longrightarrow
\lambda_\eta\neq0.
}
\tag{10.1}
$$

## Proof

若 $\lambda_\eta=0$，則

$$
\beta(x,\eta)=0
$$

對所有 $x\in H$，與 pairing perfect及 $\eta\neq0$ 矛盾。證畢。

因此在 pairing realization下，reciprocity nonannihilation可以被降成：

$$
\boxed{
\text{dual annihilator line中取到一個 nonzero vector。}
}
\tag{10.2}
$$

---

# 11. Determinant nondegeneracy criterion

考慮另一個二維空間

$$
W
$$

與 line

$$
L_W\subset W.
$$

令

$$
\Phi:
H\longrightarrow W
$$

滿足

$$
\Phi(L)\subset L_W.
\tag{11.1}
$$

所以有 induced quotient map

$$
\overline\Phi:
H/L
\longrightarrow
W/L_W.
\tag{11.2}
$$

假設

$$
\Phi|_L\neq0.
$$

## Theorem 11.1

以下等價：

$$
\boxed{
\det\Phi\neq0,
}
\tag{11.3}
$$

$$
\boxed{
\overline\Phi\neq0,
}
\tag{11.4}
$$

$$
\boxed{
\overline\Phi
\text{ is an isomorphism}.
}
\tag{11.5}
$$

## Proof

取 adapted bases使 $L$ 與 $L_W$ 都由第一個 basis vector張成。

由 (11.1)，matrix為 upper triangular：

$$
\Phi
=
\begin{pmatrix}
a&b\\
0&d
\end{pmatrix}.
$$

$\Phi|_L\neq0$ 給

$$
a\neq0.
$$

而 induced quotient map就是 multiplication by $d$。

因此

$$
\det\Phi=ad\neq0
$$

等價於

$$
d\neq0.
$$

證畢。

---

# 12. 這提供 local determinant certificate

若 actual reciprocity map可以 factor through一個二維 localization / Coleman / regulator map

$$
H
\xrightarrow{\Phi}
W
\longrightarrow
W/L_W
\xrightarrow{\mu}
A,
$$

其中：

1. $\Phi(L)\subset L_W$；
2. $\Phi|_L\neq0$；
3. $\det\Phi\neq0$；
4. $\mu\neq0$；

則：

$$
\overline\Phi\neq0
$$

而

$$
\mu\circ\overline\Phi
$$

是 nonzero line map。

因此：

## Corollary 12.1

$$
\boxed{
\det\Phi\neq0
+
\mu\neq0
\Longrightarrow
\lambda\neq0.
}
\tag{12.1}
$$

這正是將 reciprocity nonannihilation降成 determinant nondegeneracy的形式。

---

# 13. Existing local nondegeneracy data 的可能角色

如果一條既有 BSD verification line已經獨立證明某個 localization matrix

$$
M_{\mathrm{loc}}
$$

nondegenerate，

那麼這個事實不能自動被宣稱為 actual reciprocity nonannihilation。

還必須證明：

1. $M_{\mathrm{loc}}$ 就是 relevant $\Phi$；
2. leading line確實映到 distinguished $L_W$；
3. analytic reciprocity functional確實 factor through induced quotient；
4. endpoint line map非零。

因此：

$$
\boxed{
\text{local determinant nonzero 是 potential certificate，
不是 automatic identification theorem。}
}
\tag{13.1}
$$

這避免把已知 local matrix硬接到錯的 analytic map。

---

# 14. Directional criticality 是另一個問題

目前的 nonannihilation theorem是 tensor-level：

$$
\tau_m\neq0
\Longrightarrow
(\operatorname{id}\otimes\lambda)(\tau_m)\neq0.
$$

但若 deformation base有 dimension大於一，actual analytic family可能只沿某個 distinguished tangent direction

$$
\xi\in T
$$

觀察。

此時 relevant scalar是

$$
\tau_m(\xi^{\otimes m})
\in
Q.
$$

即使

$$
\tau_m\neq0,
$$

仍可能有

$$
\tau_m(\xi^{\otimes m})=0.
$$

所以：

$$
\boxed{
\text{reciprocity nonannihilation}
\neq
\text{directional noncriticality}.
}
\tag{14.1}
$$

---

# 15. Directional order theorem

假設：

$$
\lambda\neq0.
$$

取一個一維 formal path

$$
\gamma:
\operatorname{Spf}K[[t]]
\longrightarrow
S
$$

tangent direction為

$$
\xi.
$$

令 first global projective jet order是 $m$。

若

$$
\tau_m(\xi^{\otimes m})\neq0,
$$

則沿 $\gamma$ 的 projective order仍為 $m$。

因此 analytic order沿該 path為：

$$
\boxed{
r_\gamma
=
e_\gamma+m.
}
\tag{15.1}
$$

若

$$
\tau_m(\xi^{\otimes m})=0,
$$

則沿該 path 的 arithmetic projective order嚴格大於 $m$。

所以真正要檢查的是：

$$
\boxed{
\text{direction avoids the exceptional divisor}.
}
\tag{15.2}
$$

---

# 16. Exceptional divisor replaces reciprocity kernel

Round 004 已定義：

$$
\mathcal Z_m
=
\{
[\xi]\in\mathbf P(T):
\tau_m(\xi^{\otimes m})=0
\}.
$$

本輪顯示在

$$
\lambda\neq0
$$

之後，analytic first-order failure完全由

$$
[\xi]\in\mathcal Z_m
$$

控制。

也就是：

$$
\boxed{
\text{proper reciprocity kernel obstruction消失，
剩下的是 source-direction exceptional divisor。}
}
\tag{16.1}
$$

這是 T5 的重要簡化。

---

# 17. 一維 deformation base 的最強簡化

若一開始

$$
\dim T=1,
$$

那麼

$$
\operatorname{Sym}^m(T^\ast)
$$

也是一維。

first nonzero jet

$$
\tau_m\neq0
$$

自動在唯一 nonzero tangent direction上 nonzero。

因此：

## Theorem 17.1

在一維 deformation base上，只要

$$
\tau_m\neq0
$$

與

$$
\lambda\neq0,
$$

就必有 exact order equality

$$
\boxed{
r=e+m.
}
\tag{17.1}
$$

沒有 directional exceptional divisor。

這是 rank-$2$ + one-variable setup 的 minimal leading-term theorem。

---

# 18. Multivariable directional certificate

若

$$
\dim T>1,
$$

則本地端真正需要計算的不是 target-specific reciprocity kernel。

而是：

$$
\boxed{
P_m(\xi)
:=
\tau_m(\xi^{\otimes m})
}
$$

是否非零。

因為 $Q$ 一維，選 generator後 $P_m$ 可視為 homogeneous polynomial。

所以 directional noncriticality只是一個 polynomial nonvanishing certificate。

**類型：C**

這比重新計算一個高維 reciprocity kernel便宜。

---

# 19. Cross-curve reciprocity transport

現在考慮多個 partner $i$。

令

$$
Q_i
$$

與

$$
A_i
$$

都是一維 lines。

假設存在 common reference lines

$$
Q_\ast,
\qquad
A_\ast,
$$

以及 isomorphisms

$$
\phi_i:
Q_i\longrightarrow Q_\ast,
$$

$$
\psi_i:
A_i\longrightarrow A_\ast,
$$

使 reciprocity maps滿足

$$
\boxed{
\psi_i\circ\lambda_i
=
u_i
\lambda_\ast
\circ
\phi_i,
}
\tag{19.1}
$$

其中

$$
u_i\in K^\times.
$$

## Theorem 19.1

若某一個 partner $k$ 有

$$
\lambda_k\neq0,
$$

則

$$
\boxed{
\lambda_i\neq0
\quad
\text{for every }i.
}
\tag{19.2}
$$

## Proof

由 (19.1) 與 $\phi_i,\psi_i,u_i$ 全部可逆，

$$
\lambda_i=0
\iff
\lambda_\ast=0.
$$

一個 partner nonzero即推出 common map nonzero，再推出全部 nonzero。證畢。

---

# 20. Calibrator 可以成為 reciprocity nonzero witness

假設 rank-$0$ calibrator observable具有

$$
b_0
=
\lambda_0(q_0)
$$

up to explicitly nonzero factors，且

$$
b_0\neq0.
$$

則：

$$
\lambda_0\neq0.
$$

若 Cross-curve transport theorem (19.1) 成立，則：

$$
\boxed{
\text{calibrator nonzero}
\Longrightarrow
\text{target reciprocity map nonzero}.
}
\tag{20.1}
$$

這表示 rank-$0$ calibrator可能同時做兩件事：

1. 消去 common normalization scalar；
2. 證明整個 transported reciprocity line不是 zero map。

這是 calibrator 的第二種用途。

---

# 21. 但 calibrator不能自動證 direction noncritical

即使 (20.1) 成立，target-specific multivariable direction仍可能落在

$$
\mathcal Z_m.
$$

因此：

$$
\boxed{
\text{calibrator can transfer reciprocity nonzero,
but cannot automatically transfer directional noncriticality.}
}
\tag{21.1}
$$

後者仍要檢查 target jet polynomial at chosen direction。

---

# 22. Minimal nonannihilation package

對 rank-$2$ target，若 analytic deformation path已固定，真正最小 package現在是：

### M1. Arithmetic jet nonzero

$$
\tau_m\neq0.
$$

### M2. Reciprocity line nonzero

$$
\lambda\neq0.
$$

### M3. Directional noncriticality

若 base multivariable，則

$$
\tau_m(\xi^{\otimes m})\neq0.
$$

在 one-variable case，M3 automatic。

這三個條件取代了模糊的：

> explicit reciprocity nonannihilation。

---

# 23. Minimal leading-term theorem

## Theorem 23.1

令：

- $Q,A$ 為一維 $K$-spaces；
- $\lambda:Q\to A$ nonzero；
- arithmetic first nonzero projective jet為

$$
\tau_m
\in
\operatorname{Sym}^m(T^\ast)\otimes Q;
$$

- scalar exceptional factor order為 $e$；
- analytic unit $U(0)\neq0$；
- analytic path tangent為 $\xi$；
- reciprocity factorization成立。

若

$$
\tau_m(\xi^{\otimes m})\neq0,
$$

則：

$$
\boxed{
r_\xi=e_\xi+m.
}
\tag{23.1}
$$

leading coefficient由：

$$
\boxed{
U(0)
\cdot
E_e(\xi^{\otimes e})
\cdot
\lambda(
\tau_m(\xi^{\otimes m})
)
}
\tag{23.2}
$$

決定，乘上 chosen analytic line / period trivialization。

這是本輪的 minimal leading-term theorem。

---

# 24. 若 base one-dimensional

若

$$
\dim T=1,
$$

Theorem 23.1 簡化成：

## Corollary 24.1

只要：

$$
\tau_m\neq0,
$$

$$
\lambda\neq0,
$$

就有

$$
\boxed{
r=e+m.
}
\tag{24.1}
$$

因此 rank-$2$ one-variable setting中的 nonannihilation burden真正只有：

$$
\boxed{
\lambda\neq0.
}
$$

---

# 25. Kernel dimension diagnostic for higher-rank generalization

本輪的簡化強烈依賴：

$$
\dim Q=1.
$$

若未來 rank更高，

$$
\dim Q>1,
$$

則 nonzero $\lambda$ 仍可能有 nontrivial kernel。

例如：

$$
\dim Q=2,
\qquad
\dim A=1,
$$

任何 nonzero functional都有一維 kernel。

此時 first jet確實可能「剛好被殺掉」。

所以：

$$
\boxed{
\text{reciprocity kernel dichotomy 是 rank-$2$ transverse quotient 的特殊優勢。}
}
\tag{25.1}
$$

不能直接推廣到所有 rank。

---

# 26. A determinant criterion for higher target dimension

若未來

$$
\dim Q=d>1,
$$

則可以選 $d$ 個 independent analytic functionals

$$
\lambda_1,\ldots,\lambda_d
$$

組成

$$
\Lambda:
Q\to A_1\oplus\cdots\oplus A_d.
$$

若

$$
\det\Lambda\neq0,
$$

則 $\Lambda$ injective，所有 nonzero transverse jets都 survive somewhere。

這顯示 rank-$2$ 的 line-map nonzero criterion是 higher-rank determinant criterion的 $d=1$ 特例。

---

# 27. T5 的新狀態

Round 010 中 T5看起來像一個大型 obligation：

$$
\text{explicit reciprocity}
+
\text{nonannihilation}.
$$

Round 011 後可重分類為：

## T5a: Reciprocity comparison theorem

建立 actual line map與 analytic factorization。

**類型：T**

## C5b: Reciprocity line nonzero

只需一個 scalar witness或 determinant nonzero。

**類型：C 或小型 T**

## C5c: Directional noncriticality

multivariable時檢查

$$
\tau_m(\xi^{\otimes m})\neq0.
$$

**類型：C**

所以 T5 的 theorem burden確實縮小了。

---

# 28. Proof-obligation reduction

原 Round 010 major cuts：

$$
\{
\text{Global Descent},
\text{Arithmetic Fundamental Line},
\text{Explicit Reciprocity},
\text{Complex Comparison}
\}.
$$

本輪顯示第三個 cut更精確地是：

$$
\boxed{
\text{Reciprocity Comparison Theorem}
}
$$

而不是

$$
\text{Reciprocity Comparison + mysterious nonannihilation theorem}.
$$

nonannihilation的大部分已降成：

$$
\boxed{
\text{line map nonzero}
+
\text{direction polynomial nonzero}.
}
$$

---

# 29. 本地端最小 verification target

本地端針對 Bridge C 不必再廣泛搜尋。

只需要：

## V1. Produce one transverse quotient generator

$$
q\in Q^\times.
$$

## V2. Evaluate reciprocity once

$$
\lambda(q).
$$

若非零，整條 $Q$ survives。

## V3. If factorized through a $2\times2$ map

檢查：

$$
\det\Phi\neq0.
$$

## V4. If multivariable

計算：

$$
P_m(\xi)
=
\tau_m(\xi^{\otimes m}).
$$

## V5. Order check

驗證：

$$
r_\xi=e_\xi+m.
$$

若 V1--V4成立但 V5失敗，則 factorization / scalar-zero bookkeeping有問題。

---

# 30. 一個強 consistency triangle

在 minimal theorem hypotheses下，以下三件事形成 consistency triangle：

$$
\lambda\neq0,
$$

$$
\tau_m(\xi^{\otimes m})\neq0,
$$

$$
r_\xi=e_\xi+m.
$$

其中前兩者推出第三者。

若已知第三者與其中一個，也能對另一個形成限制。

例如若：

$$
r_\xi=e_\xi+m
$$

且

$$
\tau_m(\xi^{\otimes m})\neq0,
$$

則 factorization下必有

$$
\lambda\neq0.
$$

所以 analytic order equality可以反過來當 reciprocity nonzero evidence。

---

# 31. Reciprocity zero 的 observable consequence

若

$$
\lambda=0,
$$

則整個 first transverse quotient被殺掉。

如果 analytic observable完全依賴這條 reciprocity map，則所有 transverse orders都不會由該 map被看見。

這通常會導致：

- analytic section identically zero in that channel；
- 或必須由另一個 higher / different functional接手。

因此：

$$
\boxed{
\lambda=0
}
$$

不是一個「多一階 vanishing」的小現象，而是整條 chosen reciprocity channel失效。

這進一步說明為什麼在一維 quotient中只需證 nonzero map。

---

# 32. Directional zero 才是 higher-order vanishing的自然來源

相反地，

$$
\lambda\neq0
$$

但

$$
\tau_m(\xi^{\otimes m})=0
$$

時，只表示 chosen path在 first homogeneous projective jet的 zero locus上。

此時：

$$
r_\xi>e_\xi+m
$$

完全自然。

所以 higher analytic vanishing應優先區分：

$$
\boxed{
\text{channel zero}
}
$$

versus

$$
\boxed{
\text{directional criticality}.
}
$$

兩者的修復方法不同。

---

# 33. 本輪已證

在 rank-$2$ transverse quotient與 line-valued reciprocity setup下，本輪證明：

1. reciprocity kernel dichotomy；
2. nonzero line map自動 injective；
3. tensor product後 nonzero projective jet不能被 nonzero line map annihilate；
4. global multivariable order equality只需 $\lambda\neq0$；
5. lifted functional nonzero等價於 kernel exactly equal to leading line；
6. adapted-basis scalar nonvanishing criterion；
7. perfect pairing realization下 nonzero annihilator vector自動給 nonzero quotient functional；
8. $2\times2$ determinant nondegeneracy等價於 induced quotient map nonzero；
9. reciprocity nonannihilation與 directional criticality不同；
10. one-variable deformation時 directional issue automatic消失；
11. cross-curve transported line maps可由一個 calibrator witness transfer nonzero；
12. calibrator nonzero不能自動 transfer directional noncriticality；
13. minimal leading-term theorem；
14. higher-rank時一維 kernel dichotomy一般失效。

---

# 34. 本輪沒有證明

本輪沒有證明：

1. actual BSD reciprocity map的 domain確實就是所定義的 $Q=H/L$；
2. actual analytic target fiber是一維 line in the required sense；
3. actual reciprocity map存在；
4. actual reciprocity map非零；
5. actual localization / Coleman matrix就是 Theorem 11.1 的 $\Phi$；
6. actual cross-curve transport law (19.1)；
7. actual calibrator observable直接等於 reciprocity witness；
8. actual cyclotomic direction是否避開 exceptional divisor；
9. actual explicit reciprocity theorem；
10. BSD。

---

# 35. 給本地端的最小驗證清單

## V1. Dimension check

確認 target transverse quotient真的滿足：

$$
\dim Q=1.
$$

## V2. Reciprocity endpoint check

確認 analytic target為一維 line。

## V3. One-witness nonzero

取

$$
q\neq0
$$

並檢查

$$
\lambda(q)\neq0.
$$

## V4. Determinant alternative

若 reciprocity factor through二維 map，檢查：

$$
\det\Phi\neq0
$$

以及 leading-line compatibility。

## V5. Directional polynomial

若 deformation multivariable，檢查：

$$
P_m(\xi)\neq0.
$$

## V6. Cross-curve transport

若想用 calibrator transfer target nonzero，驗證 conjugacy relation (19.1)。

## V7. Order equality

最終核對：

$$
r_\xi=e_\xi+m.
$$

---

# 36. 本輪核心結論

Round 009 保留的 nonannihilation condition原本看起來像一個難以控制的 analytic-arithmetic coincidence。

Round 011 顯示，在 rank-$2$ target中：

$$
\boxed{
H/L
\text{ 是一維。}
}
$$

因此：

$$
\boxed{
\lambda\neq0
\Longrightarrow
\text{任何 nonzero transverse jet都不會被 reciprocity kernel殺掉。}
}
$$

所以真正剩下的只有兩個可分離問題：

$$
\boxed{
\text{reciprocity channel是否 nonzero？}
}
$$

與

$$
\boxed{
\text{chosen deformation direction是否落在 exceptional divisor？}
}
$$

前者可降成 one-scalar / one-determinant nonvanishing。

後者可降成 homogeneous jet polynomial evaluation。

這使 T5 從一個「大 comparison theorem + mysterious nonannihilation」縮成：

$$
\boxed{
\text{comparison theorem}
+
\text{small nonzero certificates}.
}
$$

---

# 37. 下一輪建議

## BSD Symbolic Round 012

**題目：**

> Global Descent by Compatible Local Lines and Rational Reconstruction

現在 T5 已明顯縮小。

下一個最值得攻的是 T1：

$$
\text{global rational descent}.
$$

下一輪可以研究一個比 Round 006 更積極的問題：

> 若同一 determinant class在多個 completions 中都有 compatible local realizations，而且 ratios obey rational transition laws，什麼最弱條件可以迫使它來自 $\mathbf Q$？

重點可以包括：

1. adelic determinant line；
2. compatible local scalars $a_v$；
3. product formula；
4. restricted product lattice；
5. diagonal embedding

$$
\mathbf Q^\times
\hookrightarrow
\mathbf A_{\mathbf Q}^\times;
$$

6. 何時 local data + finite support + one archimedean normalization足以 reconstruct a unique rational scalar；
7. 哪些 compatibility仍然只是 idelic class，而不是真正 rational principal idele。

如果這條線成功，T1 可能從「需要一個抽象 global descent theorem」進一步降成：

$$
\boxed{
\text{principal-idele criterion}
+
\text{finite local certificate}.
}
$$
