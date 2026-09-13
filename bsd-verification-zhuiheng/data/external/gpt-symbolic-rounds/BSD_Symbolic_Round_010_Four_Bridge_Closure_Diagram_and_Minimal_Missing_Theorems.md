# BSD Symbolic Round 010
## Four-Bridge Closure Diagram and the Minimal Missing Theorems

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** architecture / proof-obligation synthesis；未做新的大型數值計算；未主張 BSD 已證明  
**承接：** BSD Symbolic Round 001--009  
**本輪目標：** 將前九輪壓縮成一張 proof-obligation DAG，區分 symbolic closure、finite computation certificate、theorem-level bridge；找出完整 BSD leading-term bridge 的最小阻斷集與可並行工作包。

---

# 1. 本輪不再創造新 object

Round 001--009 已經建立了足夠多的抽象結構：

1. cross-rank calibration；
2. determinant gauge degree；
3. anchored projective jet；
4. higher projective jet；
5. determinant lattice torsor；
6. rational descent與 finite-prime support；
7. determinant-of-cohomology；
8. self-dual fundamental-line exponent；
9. analytic leading-term line。

因此本輪的任務不是再增加新的 formalism，而是回答：

$$
\boxed{
\text{距離完整 BSD bridge，究竟還剩哪些真正不可被符號消元取代的義務？}
}
$$

---

# 2. 三種 obligation 類型

本輪使用三類標記。

## Type S: Symbolically Closed

只要其假設成立，結論已由 Round 001--009 的代數 / 線性代數 / determinant / jet 推導閉合。

這類工作不需要再提高計算精度。

## Type C: Computable / Finite Certificate

原理與 target 已明確，剩下的是：

- explicit class construction；
- finite-module length；
- local valuation；
- modular-symbol / Coleman / height computation；
- nonvanishing test；
- saturation test；
- support-set inspection。

這類最適合交給本地端。

## Type T: Theorem-Level Bridge

這類不是把 precision 從 $11^5$ 提高到 $11^{20}$ 就能補。

需要一個 genuine mathematical theorem，典型包括：

- global descent；
- comparison isomorphism；
- explicit reciprocity；
- self-dual fundamental-line identification；
- complex-to-$p$-adic leading-line comparison。

---

# 3. 四個主要 Bridge

整條 proof architecture壓成四個 bridge。

## Bridge A

$$
\boxed{
\text{BF / Kato deformation family}
\longrightarrow
\text{calibrated arithmetic determinant}
}
$$

## Bridge B

$$
\boxed{
\text{calibrated determinant}
\longrightarrow
\text{absolute arithmetic fundamental line}
}
$$

## Bridge C

$$
\boxed{
\text{arithmetic fundamental line}
\longrightarrow
\text{$p$-adic analytic leading line}
}
$$

## Bridge D

$$
\boxed{
\text{$p$-adic analytic leading line}
\longrightarrow
\text{complex analytic leading line}
}
$$

完整 classical BSD closure需要四個 bridge全部閉合，除非存在一條更直接的 theorem繞過某個 bridge。

---

# 4. DAG 的主要節點

定義以下節點。

### A0. Raw arithmetic family

$$
\widehat Z(X,t)
$$

或相應 BF/Kato family。

### A1. Common projected quotient

固定共同 Eisenstein quotient / period frame後的 family。

### A2. Projective arithmetic jet

$$
\mathcal P_m
\in
\operatorname{Sym}^m(T^\ast)
\otimes
\operatorname{Hom}(L,H/L).
$$

### A3. Calibrated determinant jet

$$
\mathcal A_m
\in
\operatorname{Sym}^m(T^\ast)
\otimes
\det H.
$$

### A4. Rational determinant

$$
\Delta_{\mathrm{cal}}
\in
D_{\mathbf Q}.
$$

### A5. Absolute determinant lattice position

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times.
$$

### A6. Derived arithmetic fundamental line

包含：

$$
\text{free determinant}
+
\text{finite Euler corrections}
+
\text{comparison cones}.
$$

### A7. Primal-dual regulator scalar

$$
\operatorname{Reg}_h
\cdot
q_{\mathrm{fin}}.
$$

### A8. $p$-adic analytic leading tensor

$$
\Theta_p
=
\operatorname{LT}_0(\mathcal L_p).
$$

### A9. Complex analytic leading tensor

$$
\Theta_{\mathbf C}
=
\operatorname{LT}_{s=1}(L_{\mathbf C}).
$$

### A10. Classical BSD leading-term equality

scalarized後 schematic：

$$
\boxed{
L_{\mathbf C}^{\ast}(E,1)
=
\Omega_E
\cdot
\operatorname{Reg}(E)
\cdot
q_{\mathrm{fin}}
}
$$

with all conventions fixed.

---

# 5. DAG 概觀

整體依賴關係可以寫成：

$$
A0
\longrightarrow
A1
\longrightarrow
A2
\longrightarrow
A3
\longrightarrow
A4
\longrightarrow
A5
\longrightarrow
A6
\longrightarrow
A7
\longrightarrow
A8
\longrightarrow
A9
\longrightarrow
A10.
$$

但其中若干箭頭內部還分成 symbolic layer與 theorem / computation layer。

更精確地：

$$
\boxed{
A0
\xrightarrow{T/C}
A1
\xrightarrow{S}
A2
\xrightarrow{S/C}
A3
\xrightarrow{T}
A4
\xrightarrow{T/C}
A5
\xrightarrow{T/C}
A6
\xrightarrow{T/C}
A7
\xrightarrow{T/C}
A8
\xrightarrow{T}
A9
\xrightarrow{S}
A10.
}
\tag{5.1}
$$

這只是 proof-obligation classification，不是聲稱 literature 中尚無相應 theorem。

---

# 6. Bridge A：BF / Kato family 到 calibrated determinant

Bridge A 包含四層。

## A-I. Common-factor structure

需要有 genuinely constructed projected family滿足 schematic：

$$
\widehat Z
=
C\,A\,Z
$$

或其 higher-order desingularized版本。

### 已閉合的 symbolic result

一旦 common factorization成立，Round 001 證明：

$$
\text{common scalar }C
$$

可由 matched calibrator消掉。

**類型：S**

### 尚需實際確認

common quotient transport是否真的 partner-independent。

**類型：T/C hybrid**

如果它來自既有比較 theorem，屬 T；

如果 theorem已固定、只差 actual normalization audit，屬 C。

---

# 7. Bridge A：projective jet layer

在 leading line

$$
L=K\kappa
$$

固定後，Round 003--004 已證：

$$
\mathcal P_m
$$

對 unit renormalization invariant。

並且：

$$
\mathcal A_m
$$

的 BF gauge weight恆為 $2$，與 jet order $m$ 無關。

### Symbolic closure

$$
\boxed{
\text{higher jet depth}
\neq
\text{higher determinant gauge degree}.
}
$$

**類型：S**

### 實際 arithmetic obligation

決定 actual first nonzero projective order

$$
m.
$$

以及證

$$
\mathcal P_m\neq0.
$$

**類型：C**

前提是 actual family與 quotient construction已存在。

---

# 8. Bridge A：Bockstein / derived companion

Round 003--004 已證：

若

$$
[D^{(m)}\kappa]
=
\tau_m
\quad
\text{in }H/L,
$$

則

$$
\mathcal A_m
=
\kappa\wedge D^{(m)}\kappa.
$$

完整 vector equality不是必要的。

### Symbolic implication

**類型：S**

### 真正缺口

actual arithmetic Bockstein / derived operator是否存在並滿足 quotient identity。

**類型：T/C hybrid**

operator existence與 comparison theorem通常屬 T；

在 theorem已知後，對特定 curve 的 quotient equality verification屬 C。

---

# 9. Bridge A：calibrator exponent

若 rank-$0$ calibrator observable是 weight one：

$$
b_0=C\,a_0k_0,
$$

則 determinant level永遠除：

$$
\boxed{
b_0^2
}
$$

primal-dual paired raw scalar永遠除：

$$
\boxed{
b_0^4.
}
$$

jet order不改變這些 exponent。

**類型：S**

這一點不再是 open problem。

---

# 10. Bridge A 的最小輸出

Bridge A 不必輸出完整 Mordell--Weil basis。

最小 sufficient output 是：

$$
\boxed{
\Delta_{\mathrm{cal}}
\text{ or its projective / determinant-jet representative}
}
$$

外加：

1. exact gauge degree；
2. period / quotient conventions；
3. arithmetic source provenance；
4. nonvanishing certificate。

---

# 11. Bridge B：rational descent

從 calibrated $p$-adic determinant到

$$
D_{\mathbf Q}
$$

需要 global descent。

Round 006 已證 no-go：

$$
\boxed{
\mathbf Q_p\text{-rational}
\not\Rightarrow
\mathbf Q\text{-rational}.
}
$$

而且：

$$
\boxed{
\text{arbitrarily high }p\text{-adic precision cannot replace global descent}.
}
$$

因此這一箭頭是真正 theorem-level blocker。

## Obligation T1

構造或套用 global descent theorem，使

$$
\Delta_{\mathrm{cal}}
\in
D_{\mathbf Q}.
$$

可接受 route包括：

- global Galois fixedness；
- rational functional；
- semilinear descent + rational anchor。

**類型：T**

---

# 12. Bridge B：absolute lattice position

一旦 rationality成立：

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times.
$$

Round 005 已證：

$$
a
$$

是 determinant lattice torsor coordinate。

若來自未飽和 sublattice，$a$ 就是 fractional saturation scalar。

### Local defects

$$
d_\ell=v_\ell(a).
$$

### Global reconstruction

$$
a
=
\pm
\prod_\ell
\ell^{d_\ell}.
$$

**symbolic part：S**

### 實際 local valuation

**類型：C**

---

# 13. Bridge B：support theorem

單純抽查 primes不夠。

必須先有 structural support control：

$$
v_\ell(a)=0
\qquad
(\ell\notin S)
$$

for explicit finite $S$。

Round 006 已證：

comparison map away from $S$ integral isomorphism

$$
\Longrightarrow
a\in\mathbf Z[S^{-1}]^\times.
$$

## Obligation T2

證明一個 global finite-support theorem。

**類型：T**

若 theorem已知、只差把 actual bad primes列出，後半屬 C。

---

# 14. Bridge B：finite local certificate

一旦 $S$ 已被 structural theorem固定，只需要：

$$
\{d_\ell\}_{\ell\in S}.
$$

local defect可由：

$$
v_\ell(a)
=
\operatorname{length}(L_\ell/I_\ell)
-
\operatorname{length}(L'_\ell/I_\ell)
$$

或 finite cokernel length求得。

**類型：C**

這就是本地端最適合做的 finite-prime工作。

---

# 15. Bridge B：derived determinant-of-cohomology

Round 007 把 finite cohomology壓成：

$$
\delta_\ell(C^\bullet)
=
\sum_i
(-1)^i
\operatorname{length}
H^i(C^\bullet)_{\mathrm{tor},\ell}.
$$

comparison map則由 cone：

$$
K^\bullet
=
\operatorname{Cone}(f)
$$

給：

$$
v_\ell(a_f)
=
\delta_\ell(K^\bullet).
$$

### Symbolic machinery

**類型：S**

### 真正 arithmetic identification

必須知道 actual Selmer / local-condition / comparison complexes，以及每個 finite group位於哪個 degree。

## Obligation T3

建立 actual arithmetic complex與 determinant-of-cohomology identification。

**類型：T**

specific finite lengths則屬 C。

---

# 16. Bridge B：primitive closure 與 derived closure不可混淆

Round 007 已證：

primitive closure：

$$
d_\ell=0.
$$

derived closure：

$$
d_\ell
=
\delta_\ell.
$$

兩者一般不同。

因此本地端報告必須分開標：

$$
\boxed{
\text{primitive lattice status}
}
$$

與

$$
\boxed{
\text{derived determinant status}.
}
$$

**類型：S**

---

# 17. Bridge B 到 A7：regulator line

Round 008 已證 regulator真正是：

$$
\det(h):
\det M
\otimes
\det N
\longrightarrow
K.
$$

regulator出現一次。

simultaneous basis scaling平方只是 bidegree $(1,1)$ 的結果。

### Symbolic exponent

**類型：S**

### Actual arithmetic height pairing

需要明確指定：

$$
h
$$

以及 primal / dual lattices。

specific regulator value或 local cokernel length：

**類型：C**

但 pairing本身與 final fundamental line的 compatibility可能需要 theorem。

---

# 18. Fundamental-line finite factor placement

Round 008 已證：

若 primal / dual finite scalars為

$$
q_+,
\qquad
q_-,
$$

則 final scalar是

$$
q_+q_-\operatorname{Reg}.
$$

self-duality alone不能決定 exponent。

odd-shift可 cancellation；

even-shift可同號；

one-sided placement給 exponent one。

## Obligation T4

確定 actual BSD arithmetic fundamental line：

1. primal line；
2. dual line；
3. duality shift；
4. local-condition placement；
5. finite correction placement。

**類型：T**

這是一個 genuine architecture theorem。

---

# 19. Bridge C：arithmetic fundamental line 到 $p$-adic analytic line

Round 009 的 abstract factorization是：

$$
\mathcal L_p
=
U\cdot E\cdot\lambda(Z_{\mathrm{tr}}).
$$

若：

$$
\operatorname{ord}(E)=e,
$$

$$
m=m_{\mathrm{proj}},
$$

且 first transverse jet不被 $\lambda$ annihilate，則

$$
r_p=e+m.
$$

### Symbolic order theorem

**類型：S**

### Actual explicit reciprocity

需要 genuine theorem，把 arithmetic determinant / jet送到 actual $p$-adic analytic family。

## Obligation T5

explicit reciprocity / leading-line comparison theorem。

**類型：T**

---

# 20. Bridge C：nonannihilation

即使 explicit reciprocity formula存在，也可能：

$$
\lambda(\tau_m)=0.
$$

那麼 analytic order上升。

因此需要：

$$
\boxed{
(\operatorname{id}\otimes\lambda)(\tau_m)\neq0.
}
$$

這個 obligation可能有兩種來源：

### route C1

由 theorem保證 nonannihilation。

**類型：T**

### route C2

對特定 curve explicit 計算驗證 nonzero。

**類型：C**

因此它不是必然 theorem-only blocker，但必須有 certificate。

---

# 21. Bridge C：hard order inequality

不論如何，在 factorization成立時：

$$
\boxed{
e+m\le r_p.
}
$$

若本地端得到：

$$
e+m>r_p,
$$

則至少一個假設錯。

這是一個 cheap consistency gate。

**類型：C**

但 underlying inequality是 **S**。

---

# 22. Bridge D：$p$-adic leading line 到 complex leading line

這是目前整條 architecture中最乾淨的一個 theorem-level分界。

即使已知：

$$
\Theta_p
=
\operatorname{Reg}_p
\cdot
q_p,
$$

仍不能直接推出：

$$
\Theta_{\mathbf C}
=
\Omega^{-1}
\operatorname{Reg}_{\mathbf C}
q_{\mathrm{fin}}.
$$

需要 explicit bridge：

$$
\boxed{
\mathscr F_p^{\mathrm{lead}}
\longrightarrow
\mathscr F_{\mathbf C}^{\mathrm{lead}}.
}
$$

## Obligation T6

complex-to-$p$-adic leading-line comparison theorem。

**類型：T**

若一條 direct complex theorem繞過 $p$-adic side，則可替代 T6。

---

# 23. Bridge D 不是 precision problem

即使：

$$
\Theta_p
$$

已知到無限 $p$-adic precision，

也不能由此純形式地恢復 complex number

$$
\Theta_{\mathbf C}.
$$

這與 Round 006 的 rationality no-go相同：

$$
\boxed{
\text{不同 completion 的 exact data不會自動產生 global comparison theorem。}
}
$$

所以 T6 不能被更大的本地算力替代。

---

# 24. A10 的 scalarization

假設 T1--T6 都已閉合，且所有 local certificates完成。

最後 scalar equality只是 line equality的 trivialization。

在 rank-$2$ classical side schematic 為：

$$
\boxed{
\frac{L''(E,1)}{2!}
=
\Omega_E
\cdot
\operatorname{Reg}(E)
\cdot
q_{\mathrm{fin}}
}
\tag{24.1}
$$

precise formula中的 torsion、Tamagawa、Sha、period conventions必須由 actual fundamental-line theorem決定。

本輪不重新指定它們。

---

# 25. Minimal theorem-level blockers

現在把 theorem-level obligations壓縮。

## T1. Global Rational Descent

$$
\Delta_{\mathrm{cal}}
\in
D_{\mathbf Q}.
$$

## T2. Finite Support / Integral Comparison

$$
a\in
\mathbf Z[S^{-1}]^\times
$$

for explicit finite $S$。

## T3. Arithmetic Complex Identification

把 actual finite arithmetic groups、local conditions、comparison cones放進正確 determinant degrees。

## T4. Self-Dual Fundamental-Line Assembly

固定：

$$
q_+,
\quad
q_-,
\quad
h,
\quad
\text{duality shift},
\quad
\text{period/local placements}.
$$

## T5. Explicit Reciprocity / $p$-adic Leading-Line Theorem

$$
\text{arithmetic determinant / jet}
\longrightarrow
\Theta_p.
$$

## T6. Complex-to-$p$-adic Leading-Line Comparison

$$
\Theta_p
\longrightarrow
\Theta_{\mathbf C}.
$$

這六個是目前 abstract architecture下的 theorem-level blockers。

---

# 26. 哪些 T 可能合併

這六個 obligation不是聲稱需要六篇完全獨立的新 theorem。

一個強 theorem可能一次閉合多個。

例如：

### Strong global determinant theorem

可能同時閉合：

$$
T1+T2+T3.
$$

### Strong main-conjecture / explicit-reciprocity theorem

可能同時閉合：

$$
T4+T5.
$$

### Strong leading-term BSD theorem

甚至可能直接閉合：

$$
T3+T4+T5+T6.
$$

因此真正的「最小 theorem 數」不是固定六個。

六個是 minimal logical obligations，不是 minimal paper count。

---

# 27. Minimal cut set

在目前四橋架構下，若沒有替代路線，任何完整 proof path都必須跨過以下四個 logical cuts：

## Cut I: Arithmetic descent cut

至少要有某個 mechanism把 local / coefficient-field determinant變成 global arithmetic determinant。

代表：

$$
T1.
$$

## Cut II: Absolute arithmetic cut

至少要知道它如何進入 integral / derived fundamental line。

代表：

$$
T2+T3+T4.
$$

## Cut III: Analytic reciprocity cut

至少要把 algebraic fundamental line送到某個 analytic leading line。

代表：

$$
T5.
$$

## Cut IV: Classical analytic cut

至少要到達 complex leading line。

代表：

$$
T6
$$

或 direct complex replacement。

所以 minimal logical cut set可以壓成：

$$
\boxed{
\{\text{Global Descent},
\text{Arithmetic Fundamental Line},
\text{Explicit Reciprocity},
\text{Complex Comparison}\}.
}
\tag{27.1}
$$

---

# 28. 本地端真正值得做的工作包

把 theorem-level blockers分離後，本地端可以高度並行。

## C1. Genuine BF / Kato target construction

產出 actual projected target data。

## C2. Projective order

求：

$$
m.
$$

## C3. Nonannihilation

檢查：

$$
\lambda(\tau_m)\neq0.
$$

## C4. Calibrator observables

產出 rank-$0$ calibrator的 matched observable。

## C5. Rational / integral candidate coordinates

若 global theorem提供 frame，計算 actual scalar coordinates。

## C6. Local saturation defects

對有限 $S$ 求：

$$
d_\ell.
$$

## C7. Complex / cone cohomology lengths

求：

$$
\delta_\ell.
$$

## C8. Height determinant

計算：

$$
\rho_\ell
=
v_\ell(\operatorname{Reg}).
$$

## C9. Analytic order

求：

$$
r_p,
\quad
e.
$$

## C10. Consistency triangles

包括：

$$
e+m\le r_p,
$$

以及 multi-calibrator cocycle。

這些都可以平行，不必等 theorem全部完成才做。

---

# 29. Symbolically closed invariants

以下結果在目前 abstraction中已不應再反覆重算證明。

## S1. Common scalar cancellation

matched cross-curve ratio消去 common $C$。

## S2. Determinant gauge degree

rank-$2$ determinant weight：

$$
2.
$$

## S3. Paired BF gauge degree

primal-dual paired raw scalar weight：

$$
4.
$$

## S4. Higher jet independence

jet order $m$ 不改變 determinant gauge degree。

## S5. Projective jet unit invariance

unit scalar contamination在 projectivization / anchored wedge中消失。

## S6. Bockstein quotient sufficiency

只需 modulo leading line equality。

## S7. Lattice regulator scale

index $n$ 對 regulator乘：

$$
n^2.
$$

## S8. Derived Euler additivity

mapping cone / exact triangle defects可相加。

## S9. Regulator multiplicity

final primal-dual determinant regulator只出現一次。

## S10. Analytic order lower bound

$$
e+m\le r_{\mathrm{an}}
$$

under factorization。

---

# 30. 目前不能靠計算解決的 no-go 列表

以下問題不應再靠增加 brute-force computation嘗試解決。

### N1

從 exact $\mathbf Q_{11}$ determinant推 global $\mathbf Q$-rationality。

不可能純靠 local precision。

### N2

從有限 prime sampling推 finite support。

需要 structural integrality theorem。

### N3

從 projective Galois invariance推 scalar descent。

一維 line中資訊不足。

### N4

從 self-duality三個字推出 finite factor exponent。

需要 shift與 line placement。

### N5

從 $p$-adic leading-term equality直接推出 complex BSD。

需要 cross-completion comparison。

### N6

從 determinant Euler balance推出 individual finite groups trivial。

alternating cancellation可能掩蓋非零 groups。

---

# 31. Proof-obligation matrix

| Obligation | Type | Can local compute finish it? | Output |
|---|---|---:|---|
| common-factor ratio algebra | S | yes, already symbolic | calibration identity |
| actual BF projected family | C/T | partially | genuine target classes |
| first projective order $m$ | C | yes | jet certificate |
| Bockstein quotient identity | C/T | partially | determinant companion |
| calibrator nonzero | C | yes | denominator certificate |
| global rational descent | T | no | $D_{\mathbf Q}$ element |
| finite-support theorem | T | no | explicit $S$ |
| local defects $d_\ell$ | C | yes | saturation vector |
| arithmetic complex identification | T | no | determinant-of-cohomology model |
| torsion / cone lengths | C | yes | Euler profile |
| fundamental-line placement | T | no | $q_+,q_-$ and duality shift |
| regulator value / valuation | C | yes | height determinant |
| explicit reciprocity | T | no | arithmetic-to-$p$-adic line map |
| nonannihilation | C/T | often yes | order equality certificate |
| $p$-adic analytic order | C | yes | $r_p$ |
| complex-to-$p$-adic comparison | T | no | complex leading line |
| final scalar equality | S/C | yes after bridges | BSD-shaped identity |

---

# 32. Theorem gaps與 computation gaps 的比例

這條 symbolic line到現在顯示一個重要現象：

很多原先看起來像「還差很多數值」的 gap，其實已經被壓成有限 certificate。

真正不可壓成 computation的 gap數量反而不多。

目前 abstract logical blockers只有四個 major cuts：

$$
\boxed{
\text{Global Descent}
}
$$

$$
\boxed{
\text{Arithmetic Fundamental Line}
}
$$

$$
\boxed{
\text{Explicit Reciprocity}
}
$$

$$
\boxed{
\text{Complex Comparison}
}
$$

其餘大多數工作都可以成為 local finite certificate。

---

# 33. 目前最值得優先攻的 theorem-level gap

若以「能否最大幅度縮小整張 DAG」衡量，最值得先攻的是：

$$
\boxed{
\text{T5: explicit reciprocity / leading-line comparison}.
}
$$

原因是它同時可以：

1. 固定 analytic observable；
2. 固定 scalar exceptional factor；
3. 決定 reciprocity functional；
4. 連結 projective jet與 analytic order；
5. 給 nonannihilation一個明確 target；
6. 讓本地端計算真正知道自己在驗證哪個 leading coefficient。

但這只是 architecture priority，不是聲稱 T5 比其他 theorem容易。

---

# 34. 第二優先：T1 + T2 的 global descent/support package

如果 calibrated determinant只停留在

$$
\mathbf Q_{11},
$$

再多 local computation都無法變成 global absolute statement。

因此第二個高價值 package 是：

$$
\boxed{
\text{global rational descent}
+
\text{finite support theorem}.
}
$$

若這兩個一起閉合，Round 005--007 的所有 local defect工作就真正變成有限 certificate。

---

# 35. 第三優先：fundamental-line placement

這一項負責防止最危險的 exponent錯誤。

需要固定：

$$
\text{free determinant},
$$

$$
\text{dual determinant},
$$

$$
\text{finite Euler line},
$$

$$
\text{height pairing},
$$

$$
\text{period line}.
$$

若 T4 未閉合，即使每個 finite group都算對，也可能在 final formula中：

- 多平方一次；
- 少一個 inverse；
- 把 one-sided correction放成 symmetric correction。

所以 T4 是 formula correctness blocker。

---

# 36. 第四優先：complex comparison

如果研究目標只是一個 $p$-adic BSD-shaped theorem，T6可以延後。

如果目標是 classical complex BSD，T6無法省略，除非用 direct complex bridge替代。

因此：

$$
\boxed{
T6
\text{ 的優先度取決於最終 claim 是 }p\text{-adic 還是 classical BSD。}
}
\tag{36.1}
$$

---

# 37. 一個更緊的 Stage-1 closure criterion

這條 web symbolic line的第一階段可以在以下條件達成時宣告 architecture closure：

1. 所有 normalization exponents已固定；
2. 所有 line objects已定義；
3. proof DAG無循環；
4. theorem-level gaps已壓到有限清單；
5. computation gaps都有 finite certificate target；
6. no-go routes已明確排除；
7. 不再存在「未知 scalar」沒有被分類。

Round 010 達到的正是這個層級。

這不等於 BSD proof closure。

它是：

$$
\boxed{
\text{BSD proof-architecture closure}.
}
$$

---

# 38. Stage-1 architecture closure statement

在 Round 001--010 的抽象假設下，現在所有曾出現的 unknown scalar可以分類成：

### Gauge scalar

可用 calibration消去。

### Coordinate scalar

由 jet tensor transformation law控制。

### Period scalar

屬 analytic / comparison trivialization。

### Lattice scalar

屬 rational determinant torsor。

### Finite Euler scalar

屬 determinant-of-cohomology。

### Height scalar

屬 pairing normalization。

### Reciprocity scalar

屬 analytic-algebraic comparison theorem。

因此：

$$
\boxed{
\text{目前不再需要一個未分類的「神秘常數」容器。}
}
\tag{38.1}
$$

每一個 scalar都已經有自己的 transformation law與 closure route。

---

# 39. 下一階段的策略選擇

Round 010 之後有兩條合理路線。

## Route I: theorem attack

選 T1--T6 中一個 theorem-level blocker，繼續純符號攻擊。

最值得優先的候選：

$$
T5
=
\text{explicit reciprocity leading-line theorem}.
$$

## Route II: architecture stress test

不新增 theorem，改用 hypothetical countermodels測試整張 DAG：

- period rescaling；
- wrong quotient transport；
- wrong duality shift；
- hidden prime-to-$11$ saturation；
- reciprocity annihilation；
- higher projective criticality。

目標是確認沒有漏掉第五種 major obstruction。

兩條都可行。

---

# 40. 若直接繼續純數學推演，我建議 Round 011

## BSD Symbolic Round 011

**題目：**

> Reciprocity Kernel, Nonannihilation, and the Minimal Leading-Term Theorem

理由：

目前 Bridge C 是最容易繼續用純符號往前推的一段。

下一輪可以不引用任何具體大 theorem，先抽象研究：

1. reciprocity map的 kernel到底需要多大才會破壞 order equality；
2. projective jet與 regulator determinant哪些部分可能落在 kernel；
3. 一個 minimal nonannihilation theorem最弱需要哪些假設；
4. 是否能用 dual pairing / determinant nondegeneracy把 nonannihilation降成一個 scalar determinant條件；
5. 是否能把

$$
\lambda(\tau_m)\neq0
$$

轉成已有 local nondegeneracy data的 consequence。

如果成功，T5 可能會從「一個很大的 explicit reciprocity theorem + nonannihilation」拆成：

$$
\boxed{
\text{comparison theorem}
+
\text{很小的 determinant nondegeneracy lemma}.
}
$$

這會進一步縮小真正 theorem-level gap。
