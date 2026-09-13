# BSD Symbolic Round 003
## Anchored Projective Jet and Bockstein Bridge

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** conditional symbolic development；未做新的大型數值計算；未主張 BSD 已證明  
**承接：** BSD Symbolic Round 001--002  
**本輪主題：** 比較 mixed $(X,t)$ deformation、projective jet、Bockstein companion 與 determinant lift，並判定哪些候選 determinant 物件其實不具 normalization invariance。

---

# 1. 本輪的核心修正

Round 002 提出三種可能的 rank-$2$ determinant 來源：

1. 兩個獨立 arithmetic classes；
2. mixed $(X,t)$ deformation 的二維 source；
3. 一個 leading class 加上一個 Bockstein / derived companion。

本輪得到一個重要修正：

> 直接取兩個一階偏導數的 wedge，通常不是 canonical 的。

真正穩定的物件是：

$$
\boxed{
\kappa\wedge dZ_0(\xi),
}
$$

也就是以 leading class $\kappa$ 作為 anchor，再 wedge 一個 deformation derivative。

更 invariant 地說，真正的 gauge-free 物件不是一個已經 trivialized 的 determinant element，而是 projective derivative

$$
\boxed{
d[Z]_0:
T_0S
\longrightarrow
\operatorname{Hom}(L,H/L),
}
$$

其中

$$
L=K\kappa.
$$

Bockstein bridge 應該與這個 projective derivative 對接，而不是直接和 raw mixed derivative wedge 對接。

---

# 2. 基本設定

令 $K$ 為特徵零域，$H$ 為二維 $K$-向量空間。

令

$$
S=\operatorname{Spf}K[[X,t]]
$$

表示形式二維 deformation base，其原點 maximal ideal 為

$$
\mathfrak m=(X,t).
$$

切空間記為

$$
T
:=
(\mathfrak m/\mathfrak m^2)^\ast.
$$

考慮一個非零 formal arithmetic family

$$
Z(X,t)\in H[[X,t]]
$$

滿足

$$
Z(0,0)=\kappa\neq0.
\tag{2.1}
$$

令

$$
L:=K\kappa\subset H.
\tag{2.2}
$$

一階展開寫成

$$
Z(X,t)
=
\kappa
+
Xu
+
tv
+
O(\mathfrak m^2),
\tag{2.3}
$$

其中

$$
u,v\in H.
$$

---

# 3. Anchored jet determinant tensor

對任意 tangent vector

$$
\xi\in T,
$$

定義 directional derivative

$$
dZ_0(\xi)\in H.
$$

## Definition 3.1

定義 anchored jet determinant tensor

$$
\mathcal J_Z:
T
\longrightarrow
\det H
$$

為

$$
\boxed{
\mathcal J_Z(\xi)
=
\kappa\wedge dZ_0(\xi).
}
\tag{3.1}
$$

等價地，

$$
\mathcal J_Z
\in
T^\ast\otimes\det H.
\tag{3.2}
$$

在座標基底 $\partial_X,\partial_t$ 下，

$$
\mathcal J_Z(\partial_X)
=
\kappa\wedge u,
$$

$$
\mathcal J_Z(\partial_t)
=
\kappa\wedge v.
$$

這個 tensor 同時保留兩個 deformation direction，但不要求 $u$ 與 $v$ 本身 canonical。

---

# 4. Unit-shear cancellation theorem

現在考慮 family 的一般 scalar renormalization。

令

$$
g(X,t)\in K[[X,t]]^\times
$$

為一個 formal unit，並令

$$
\widetilde Z(X,t)
=
g(X,t)Z(X,t).
\tag{4.1}
$$

記

$$
g_0:=g(0,0)\in K^\times.
$$

## Theorem 4.1

有

$$
\boxed{
\mathcal J_{\widetilde Z}
=
g_0^2\mathcal J_Z.
}
\tag{4.2}
$$

特別地，$dg_0$ 的所有一階變化完全消失。

## Proof

首先

$$
\widetilde Z(0,0)
=
g_0\kappa.
$$

對任意 $\xi\in T$，

$$
d\widetilde Z_0(\xi)
=
dg_0(\xi)\kappa
+
g_0dZ_0(\xi).
$$

因此

$$
\mathcal J_{\widetilde Z}(\xi)
=
(g_0\kappa)
\wedge
\left(
dg_0(\xi)\kappa
+
g_0dZ_0(\xi)
\right).
$$

由於

$$
\kappa\wedge\kappa=0,
$$

所以

$$
\mathcal J_{\widetilde Z}(\xi)
=
g_0^2
\kappa\wedge dZ_0(\xi).
$$

即得 (4.2)。證畢。

---

# 5. 這個定理對 BSD normalization 的意義

假設 projected BF/Kato family 不是單純乘上一個常數，而是

$$
\widehat Z(X,t)
=
C(X,t)A(X,t)Z(X,t),
\tag{5.1}
$$

其中在已經抽掉必要 vanishing monomial 後，

$$
C(X,t),A(X,t)\in K[[X,t]]^\times.
$$

令

$$
C_0=C(0,0),
\qquad
A_0=A(0,0).
$$

由 Theorem 4.1，

$$
\boxed{
\mathcal J_{\widehat Z}
=
C_0^2A_0^2
\mathcal J_Z.
}
\tag{5.2}
$$

注意：

$$
dC_0,
\qquad
dA_0
$$

都不出現在結果中。

因此 anchored determinant level 有一個很強的穩定性：

$$
\boxed{
\text{任何一階 scalar transport contamination 都只產生 }\kappa\text{-方向 shear，最後在 wedge 中自動消失。}
}
\tag{5.3}
$$

這比單純假設 comparison scalar 在 deformation space 上完全常數更弱。

---

# 6. Gauge weight 再次出現

若共同 normalization 只看 special-fiber value

$$
C_0\mapsto aC_0,
$$

則

$$
\mathcal J_{\widehat Z}
\mapsto
a^2
\mathcal J_{\widehat Z}.
$$

因此 anchored jet determinant 的 gauge weight 是

$$
\boxed{
2.
}
\tag{6.1}
$$

這與 Round 002 的 rank-$2$ determinant degree 完全一致。

所以 rank-$0$ calibrator

$$
b_0
=
C_0a_0k_0
$$

仍然必須平方：

$$
\boxed{
\mathcal J_Z
\propto
\frac{\mathcal J_{\widehat Z}}{b_0^2}.
}
\tag{6.2}
$$

---

# 7. Projective derivative 是真正 gauge-free 的物件

family $Z$ 在原點定義一條 line

$$
L=K\kappa.
$$

因此 $Z$ 也定義一個 projective map

$$
[Z]:
S
\longrightarrow
\mathbf P(H).
$$

其 differential 為

$$
d[Z]_0:
T
\longrightarrow
T_{[L]}\mathbf P(H).
$$

標準識別給出

$$
T_{[L]}\mathbf P(H)
\simeq
\operatorname{Hom}(L,H/L).
$$

所以得到

$$
\boxed{
\operatorname{KS}_Z
:=
d[Z]_0
\in
T^\ast
\otimes
\operatorname{Hom}(L,H/L).
}
\tag{7.1}
$$

這裡 $\operatorname{KS}_Z$ 可以視為 projective Kodaira--Spencer 型的一階變形資料。

---

# 8. Projective invariance theorem

## Theorem 8.1

對任意 unit

$$
g(X,t)\in K[[X,t]]^\times,
$$

若

$$
\widetilde Z=gZ,
$$

則

$$
\boxed{
\operatorname{KS}_{\widetilde Z}
=
\operatorname{KS}_Z.
}
\tag{8.1}
$$

## Proof

$Z$ 與 $gZ$ 在每一點張成同一條 projective line，因此

$$
[\widetilde Z]=[Z].
$$

對原點微分即得。證畢。

這表示：

$$
\boxed{
\operatorname{KS}_Z
\text{ 完全不依賴 scalar trivialization。}
}
\tag{8.2}
$$

---

# 9. Anchored determinant 與 projective derivative 的關係

projective derivative 的 target 是

$$
\operatorname{Hom}(L,H/L)
\simeq
L^\ast\otimes(H/L).
$$

另一方面，

$$
\det H
\simeq
L\otimes(H/L).
$$

因此

$$
L^{\otimes2}
\otimes
\operatorname{Hom}(L,H/L)
\simeq
\det H.
\tag{9.1}
$$

這正好解釋為什麼從 projective derivative 轉成 determinant element 會出現 normalization weight two。

若選擇 generator

$$
\kappa\in L,
$$

則

$$
\kappa^{\otimes2}
\otimes
\operatorname{KS}_Z(\xi)
$$

對應到

$$
\kappa\wedge dZ_0(\xi).
$$

因此 anchored tensor $\mathcal J_Z$ 可以理解為：

$$
\boxed{
\text{projective derivative}
+
\text{一個 }L^{\otimes2}\text{ trivialization}.
}
\tag{9.2}
$$

這使 Round 002 的 gauge weight two 不再只是計數現象，而有幾何來源。

---

# 10. 第一個真正的結構簡化

因為

$$
\dim H=2,
$$

所以

$$
\dim(H/L)=1.
$$

因此

$$
\dim
\operatorname{Hom}(L,H/L)
=
1.
$$

故若

$$
\operatorname{KS}_Z\neq0,
$$

則它的 rank 必定為一。

所以

$$
\ker(\operatorname{KS}_Z)
\subset T
$$

是一條 canonical tangent line。

## Theorem 10.1

若 $\operatorname{KS}_Z\neq0$，則存在 canonical exact sequence

$$
0
\longrightarrow
N
\longrightarrow
T
\longrightarrow
\operatorname{Hom}(L,H/L)
\longrightarrow
0,
\tag{10.1}
$$

其中

$$
N:=\ker(\operatorname{KS}_Z)
$$

是一維。

因此真正需要的不是「兩個獨立 deformation derivatives」。

真正需要的是：

$$
\boxed{
\text{一個 leading line }L
+
\text{一個 transverse deformation direction }T/N.
}
\tag{10.2}
$$

這已經足以生成 rank-$2$ determinant direction。

---

# 11. Two-variable geometry 的正確讀法

在座標 $(X,t)$ 下，

$$
T
=
K\partial_X
\oplus
K\partial_t.
$$

若

$$
\operatorname{KS}_Z
\neq0,
$$

則存在某個非零線性組合

$$
\xi_{\mathrm{null}}
=
a\partial_X+b\partial_t
$$

滿足

$$
\operatorname{KS}_Z(\xi_{\mathrm{null}})=0.
$$

也就是

$$
dZ_0(\xi_{\mathrm{null}})
\in
L.
\tag{11.1}
$$

任何不在 $N$ 裡的 transverse direction

$$
\xi_{\mathrm{tr}}
$$

都滿足

$$
\kappa\wedge dZ_0(\xi_{\mathrm{tr}})
\neq0.
\tag{11.2}
$$

因此 mixed $(X,t)$ deformation 的真正任務不是提供兩個 independent target vectors，而是找出：

$$
\boxed{
N
=
\text{first-order projectively trivial direction},
}
$$

以及其 transverse quotient。

---

# 12. Raw mixed derivative wedge 不是 canonical

現在檢查 Round 002 原先候選的

$$
u\wedge v.
$$

令

$$
Z(X,t)
=
\kappa+Xu+tv+O(\mathfrak m^2).
$$

考慮一個 constant-one unit renormalization

$$
g(X,t)
=
1+aX+bt+O(\mathfrak m^2).
$$

令

$$
\widetilde Z=gZ.
$$

則

$$
\widetilde u
=
u+a\kappa,
$$

$$
\widetilde v
=
v+b\kappa.
$$

所以

$$
\widetilde u\wedge\widetilde v
=
u\wedge v
+
a\kappa\wedge v
-
b\kappa\wedge u.
\tag{12.1}
$$

一般而言，

$$
\widetilde u\wedge\widetilde v
\neq
u\wedge v.
$$

因此：

## Theorem 12.1

$$
\boxed{
u\wedge v
\text{ 不 invariant under unit renormalization with }g(0)=1.
}
\tag{12.2}
$$

所以 raw mixed first-derivative determinant 不能直接當作 canonical BSD determinant bridge。

這是本輪對 Round 002 候選機制 B 的實質修正。

---

# 13. Anchored jet 為什麼避開這個問題

同樣的 transformation 下，

$$
\kappa\wedge\widetilde u
=
\kappa\wedge(u+a\kappa)
=
\kappa\wedge u,
$$

以及

$$
\kappa\wedge\widetilde v
=
\kappa\wedge(v+b\kappa)
=
\kappa\wedge v.
$$

所以當

$$
g(0)=1,
$$

anchored jet 完全不變。

更一般地，若

$$
g(0)=g_0,
$$

只剩

$$
g_0^2
$$

這個預期中的 determinant gauge weight。

因此 anchored jet 正好去除了 raw mixed wedge 的 longitudinal contamination。

---

# 14. Bockstein bridge criterion

現在令

$$
D_\xi:H\longrightarrow H
$$

表示與 tangent direction $\xi$ 對應的一個 derived / Bockstein-type operator。

不要求

$$
dZ_0(\xi)
=
D_\xi\kappa
$$

逐字相等。

只要求它們在 quotient 中相等：

$$
dZ_0(\xi)
-
D_\xi\kappa
\in
L.
\tag{14.1}
$$

## Theorem 14.1

若 (14.1) 成立，則

$$
\boxed{
\kappa\wedge dZ_0(\xi)
=
\kappa\wedge D_\xi\kappa.
}
\tag{14.2}
$$

## Proof

由 (14.1)，存在 $c_\xi\in K$ 使

$$
dZ_0(\xi)
=
D_\xi\kappa
+
c_\xi\kappa.
$$

因此

$$
\kappa\wedge dZ_0(\xi)
=
\kappa\wedge D_\xi\kappa
+
c_\xi\kappa\wedge\kappa,
$$

而第二項為零。證畢。

這個 theorem 告訴我們：

$$
\boxed{
\text{Bockstein bridge 只需要 modulo }L\text{ 的 equality。}
}
\tag{14.3}
$$

不需要 rigid 地匹配整個 vector。

---

# 15. Affine ambiguity 自動消失

假設 Bockstein operator 有 ambiguity

$$
D_\xi'
=
uD_\xi
+
a\operatorname{Id}_H,
$$

其中

$$
u\in K^\times.
$$

則

$$
\kappa\wedge D_\xi'\kappa
=
u
\kappa\wedge D_\xi\kappa.
$$

因此 projective determinant line

$$
[
\kappa\wedge D_\xi\kappa
]
$$

不受

$$
D_\xi\mapsto D_\xi+a\operatorname{Id}
$$

影響，而只對 overall scale $u$ 有一維縮放。

這與 projective derivative 的結構完全一致。

---

# 16. Coordinate change law

令新的 deformation coordinates $(X',t')$ 滿足

$$
\begin{pmatrix}
X'\\
t'
\end{pmatrix}
=
J
\begin{pmatrix}
X\\
t
\end{pmatrix}
+
O(\mathfrak m^2),
$$

其中

$$
J\in\operatorname{GL}_2(K).
$$

切空間因而由 Jacobian 線性變換。

因為 $\mathcal J_Z$ 是一個 element of

$$
T^\ast\otimes\det H,
$$

其 components 依 covector law 變換。

若把

$$
\mathbf J_Z
=
\begin{pmatrix}
\kappa\wedge u &
\kappa\wedge v
\end{pmatrix}
$$

視為 row vector，則

$$
\boxed{
\mathbf J_Z'
=
\mathbf J_ZJ^{-1}.
}
\tag{16.1}
$$

所以 individual $X$-或 $t$-component 依賴座標，但整個 tensor $\mathcal J_Z$ 不依賴座標。

---

# 17. Distinguished cyclotomic direction 的必要性

如果最終 arithmetic theory 本身給出 canonical cyclotomic tangent line

$$
T_{\mathrm{cyc}}
\subset T,
$$

那麼可以選

$$
\xi_{\mathrm{cyc}}\in T_{\mathrm{cyc}}
$$

並考慮

$$
\mathcal J_Z(\xi_{\mathrm{cyc}}).
$$

但它的 absolute scale 仍取決於 cyclotomic coordinate normalization。

因此需要區分：

$$
\boxed{
\text{canonical tangent line}
}
$$

與

$$
\boxed{
\text{canonical tangent vector}.
}
$$

前者給出 projective determinant direction；後者才給出 absolute determinant element。

這與 Round 001 對 cyclotomic reparametrization 的警告一致。

---

# 18. Calibrator cancellation at anchored-jet level

假設 target projected family 滿足

$$
\widehat Z_E
=
C_0A_EZ_E
$$

於 special fiber 的 normalization level，其中 $A_E\neq0$。

則

$$
\mathcal J_{\widehat Z_E}
=
C_0^2A_E^2
\mathcal J_{Z_E}.
$$

rank-$0$ calibrator 給

$$
b_0
=
C_0a_0k_0.
$$

因此

$$
\boxed{
\mathcal J_{Z_E}
=
\frac{a_0^2k_0^2}{A_E^2}
\frac{\mathcal J_{\widehat Z_E}}{b_0^2}.
}
\tag{18.1}
$$

這是 Round 002 determinant calibration 的 anchored-jet 版本。

它不需要先選出第二個 named arithmetic class。

只需要：

1. leading line $L_E$；
2. 非零 projective derivative；
3. calibrator normalization。

---

# 19. 一個更弱但更實用的 arithmetic target

因此，對本地端而言，未必要立刻構造兩個完整 classes

$$
\kappa_{E,1},
\kappa_{E,2}.
$$

一個更弱的 target 是：

$$
\boxed{
\operatorname{KS}_{Z_E}\neq0.
}
\tag{19.1}
$$

或者更具體：

找一個 arithmetic direction $\xi$ 使

$$
dZ_{E,0}(\xi)
\notin
K\kappa_E.
\tag{19.2}
$$

只要 (19.2) 成立，

$$
\kappa_E
\wedge
dZ_{E,0}(\xi)
\neq0,
$$

rank-$2$ determinant direction 就已經出現。

這可能比直接找第二個全球 arithmetic class 容易。

---

# 20. Bockstein equivalence 的最小條件

若本地端已有 Bockstein-type construction $D_\xi$，那麼不需要驗證完整 equality。

只需要驗證 quotient equality：

$$
\boxed{
[dZ_0(\xi)]
=
[D_\xi\kappa]
\quad
\text{in }
H/L.
}
\tag{20.1}
$$

一旦 (20.1) 成立，就自動得到 determinant equality

$$
\boxed{
\mathcal J_Z(\xi)
=
\kappa\wedge D_\xi\kappa.
}
\tag{20.2}
$$

因此 Bockstein bridge 的 verification burden 可以從二維 vector equality 降到一維 quotient equality。

---

# 21. Projective criticality

如果

$$
\operatorname{KS}_Z=0,
$$

則所有一階 derivatives 都滿足

$$
dZ_0(\xi)\in L.
$$

此時一階 deformation 沒有產生新的 determinant direction。

這表示原點對 projective family 是 first-order critical。

那麼就必須進入 higher jet。

定義最小整數

$$
m\ge1
$$

使得第 $m$ 階 projective jet 首次非零。

這會形成下一個自然分支：

$$
\boxed{
\operatorname{KS}_Z\neq0
\quad\text{or}\quad
\operatorname{KS}_Z=0\text{ and use higher projective jet}.
}
\tag{21.1}
$$

因此「找不到一階 companion」不等於 determinant route 失敗，只代表 deformation order 更高。

---

# 22. Higher-order shear principle

Theorem 4.1 的精神可以延伸：

如果 family 被 unit $g$ 重新 normalize，所有由 $dg$ 造成的 first-order contamination 都落在 leading line $L$。

因此只要 determinant construction 每次都 wedge leading direction $\kappa$，這些 longitudinal shear 就會消失。

這提供一個一般設計原則：

$$
\boxed{
\text{先 quotient 掉 leading line，再研究 transverse jet。}
}
\tag{22.1}
$$

而不是直接在 $H$ 中比較 raw derivatives。

---

# 23. 本輪對三條候選路徑的判定

## Route A: 兩個獨立 global classes

仍然有效。

如果真的能構造

$$
\kappa_1\wedge\kappa_2\neq0,
$$

則直接得到 determinant。

但它可能比必要條件更強。

## Route B: raw mixed derivative determinant

原候選

$$
u\wedge v
$$

一般不 canonical。

其問題來自 unit renormalization 造成的

$$
u\mapsto u+a\kappa,
\qquad
v\mapsto v+b\kappa.
$$

所以此 route 必須改寫。

## Route B prime: anchored projective jet

正確物件是

$$
\mathcal J_Z
\in
T^\ast\otimes\det H.
$$

這一條通過 unit-shear invariance。

## Route C: Bockstein companion

若

$$
D_\xi\kappa
\equiv
dZ_0(\xi)
\pmod L,
$$

則與 anchored jet 完全一致。

因此 Route B prime 與 Route C 在 quotient criterion 下可以真正合流。

---

# 24. 本輪主要定理鏈

本輪可以壓成以下邏輯：

$$
Z(0)=\kappa
$$

先決定 leading line

$$
L=K\kappa.
$$

接著 projectivize：

$$
[Z]:
S\to\mathbf P(H).
$$

微分得到 gauge-free object

$$
\operatorname{KS}_Z:
T\to\operatorname{Hom}(L,H/L).
$$

若

$$
\operatorname{KS}_Z\neq0,
$$

則存在 canonical null line

$$
N=\ker\operatorname{KS}_Z
$$

與 transverse quotient

$$
T/N.
$$

選擇一個 transverse direction $\xi$ 後，

$$
\kappa\wedge dZ_0(\xi)
$$

產生 determinant element。

若 Bockstein operator 滿足 quotient equality，則

$$
\kappa\wedge dZ_0(\xi)
=
\kappa\wedge D_\xi\kappa.
$$

最後用 rank-$0$ calibrator 的平方消去 common BF gauge。

---

# 25. 本輪最重要的新結論

第一個結論：

$$
\boxed{
\text{rank-$2$ determinant 不需要先找到兩個獨立 global classes。}
}
$$

一個 leading class 加上一個 projectively transverse derivative 已經足夠。

第二個結論：

$$
\boxed{
\text{raw two-variable derivative wedge }u\wedge v\text{ 一般不是 canonical。}
}
$$

第三個結論：

$$
\boxed{
\text{真正 gauge-free 的一階資料是 projective derivative }
\operatorname{KS}_Z.
}
$$

第四個結論：

$$
\boxed{
\text{Bockstein bridge 只需要在 }H/L\text{ 中比對，不需要完整 vector equality。}
}
$$

第五個結論：

$$
\boxed{
\text{scalar normalization 的一階導數在 anchored wedge 中自動消失。}
}
$$

這最後一點可能直接降低 period transport / quotient transport 的 verification burden。

---

# 26. 本輪沒有證明的事

本輪沒有證明：

1. genuine BF/Kato family 已經給出一個符合設定的二變量 $Z(X,t)$；
2. target 的 $\operatorname{KS}_Z$ 非零；
3. canonical cyclotomic 或 weight tangent vector 已被 absolute normalize；
4. arithmetic Bockstein operator 已存在並滿足 quotient equality；
5. higher-order projective jet 在 first-order critical 情形下非零；
6. calibrator period 已完全與 target determinant normalization 對齊；
7. calibrated anchored determinant 已等於 Mordell--Weil determinant lattice；
8. BSD 已證明。

---

# 27. 給本地端的最小驗證清單

## V1. Projective nonvanishing

計算或構造一個 direction $\xi$，檢查

$$
dZ_0(\xi)
\notin
K\kappa.
$$

等價地，

$$
\mathcal J_Z(\xi)\neq0.
$$

## V2. Null-line detection

若 base 是 $(X,t)$ 二維，找

$$
N=\ker\operatorname{KS}_Z.
$$

確認 $N$ 是否真為一維。

## V3. Unit-rescaling test

對 family 人為乘上一個

$$
g(X,t)=1+aX+bt+\cdots
$$

確認 raw $u\wedge v$ 會變，但

$$
\kappa\wedge u,
\qquad
\kappa\wedge v
$$

不變。

## V4. Bockstein quotient test

若已有 $D_\xi$，只檢查

$$
dZ_0(\xi)-D_\xi\kappa
\in
K\kappa.
$$

不必先要求完整 equality。

## V5. Gauge-degree test

確認 projected anchored jet 的 common factor 是

$$
C_0^2
$$

而不是 $C_0$。

## V6. Calibrator-square test

確認

$$
\frac{\mathcal J_{\widehat Z_E}}{b_0^2}
$$

對 common rescaling invariant。

## V7. First-order criticality test

若所有 anchored first jets 都為零，明確標記

$$
\operatorname{KS}_Z=0
$$

並轉入 higher projective jet，而不是把 route 誤判為失敗。

---

# 28. 下一輪建議

## BSD Symbolic Round 004

**題目：**

> Higher Projective Jets and the First Nonzero Determinant Order

下一輪應處理：

1. 若 $\operatorname{KS}_Z=0$，如何定義 coordinate-covariant higher projective jet；
2. 第一次非零 transverse jet 的 order 是否與 analytic rank / exceptional-zero order 有結構關係；
3. unit renormalization 在 higher jet 中造成的 longitudinal contamination如何系統性 quotient 掉；
4. 如何把 first nonzero projective jet 轉成 determinant line element；
5. calibration exponent 是否仍然只由 determinant degree決定，而不由 jet order 改變。

最值得先證的一個猜想是：

$$
\boxed{
\text{jet order 決定 deformation vanishing degree，但 determinant gauge weight 仍只由 exterior degree 決定。}
}
$$

若這成立，則 rank-$2$ target 即使 first-order critical，也仍然只需要 calibrator square，而不是因為 higher jet order 而提高 calibration power。
