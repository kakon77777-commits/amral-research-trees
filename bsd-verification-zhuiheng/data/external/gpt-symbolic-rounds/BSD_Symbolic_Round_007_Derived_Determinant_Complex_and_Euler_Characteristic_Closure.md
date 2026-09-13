# BSD Symbolic Round 007
## Derived Determinant Complex and Euler-Characteristic Closure

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** conditional symbolic development；未做新的大型數值計算；未主張 BSD 已證明  
**承接：** BSD Symbolic Round 001--006  
**本輪目標：** 用 determinant-of-cohomology 統一 free lattice、saturation、finite cokernel 與 torsion cohomology 的 valuation bookkeeping；建立 mapping-cone Euler defect；並說明 derived determinant closure 能證明什麼、不能證明什麼。

---

# 1. 為什麼要從單一 lattice 升到 complex

Round 005--006 已把 absolute determinant anchor 壓成

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times,
$$

以及有限個 local defects

$$
d_\ell=v_\ell(a).
$$

但真正的 BSD arithmetic 不只包含 free Mordell--Weil lattice。

它還可能同時包含：

- free Selmer / Mordell--Weil part；
- torsion cohomology；
- finite kernel / cokernel；
- local condition correction；
- saturation defect；
- comparison-map defect。

這些物件若分開記，容易把 normalization exponent 混掉。

determinant-of-cohomology 的目的就是把它們放進同一條一維 line。

---

# 2. Determinant convention

令 $R$ 為 DVR，fraction field 為 $K$，uniformizer 為 $\varpi$。

令

$$
C^\bullet
$$

為 bounded perfect complex of finite free $R$-modules。

定義 determinant line

$$
\det_R(C^\bullet)
:=
\bigotimes_i
\det_R(C^i)^{(-1)^i},
\tag{2.1}
$$

其中對一維 line $L$，

$$
L^{-1}:=L^\ast.
$$

本輪為了讓 degree-$1$ free cohomology直接出現在正向 determinant line，定義 arithmetic-oriented line

$$
\boxed{
\mathscr A_R(C^\bullet)
:=
\det_R(C^\bullet)^{-1}.
}
\tag{2.2}
$$

這個 convention 很重要。

若改用 $\det(C^\bullet)$ 而不是其 inverse，以下所有 local Euler exponent 都會整體反號。

---

# 3. Cohomological determinant isomorphism

determinant functor 給出 canonical isomorphism

$$
\det_R(C^\bullet)
\simeq
\bigotimes_i
\det_R(H^i(C^\bullet))^{(-1)^i},
\tag{3.1}
$$

其中 finite torsion modules 的 determinant透過 finite projective resolution解釋。

等價地，

$$
\mathscr A_R(C^\bullet)
\simeq
\bigotimes_i
\det_R(H^i(C^\bullet))^{(-1)^{i+1}}.
\tag{3.2}
$$

在 tensor 到 $K$ 後，所有 finite torsion cohomology消失，只留下 free cohomology determinant。

因此 integral arithmetic line 與 rational free determinant line 的差異，正是 torsion Euler data。

---

# 4. Sign calibration model

先固定最容易出錯的正負號。

考慮 complex

$$
C_n:
\qquad
R
\xrightarrow{\varpi^n}
R
$$

放在 degrees $1$ 與 $2$。

則

$$
H^1(C_n)=0,
$$

$$
H^2(C_n)
=
R/\varpi^nR.
$$

在 generic fiber 上 complex acyclic。

依 convention (2.2)，其 arithmetic determinant lattice在 canonical generic trivialization中對應

$$
\varpi^nR.
$$

所以 degree-$2$ finite cohomology length $n$ 對 $\mathscr A$ 貢獻

$$
+n.
$$

相反地，若同一 complex放在 degrees $0$ 與 $1$，使 torsion出現在 $H^1$，則對 $\mathscr A$ 的 contribution 是

$$
-n.
$$

這固定了後面的 Euler sign。

---

# 5. Local Euler defect

假設

$$
C^\bullet\otimes_RK
$$

在 torsion directions 上已 generic-acyclic。

定義 local torsion Euler defect

$$
\boxed{
\delta_R(C^\bullet)
:=
\sum_i
(-1)^i
\operatorname{length}_R
H^i(C^\bullet)_{\mathrm{tor}}.
}
\tag{5.1}
$$

如果所有 generic cohomology 都為零，則 $\mathscr A_R(C^\bullet)$ 在 canonical $K$-trivialization 中就是 fractional ideal

$$
\boxed{
\varpi^{\delta_R(C^\bullet)}R.
}
\tag{5.2}
$$

---

# 6. Euler-ideal theorem

## Theorem 6.1

若 $C^\bullet$ 是 perfect，且 $C^\bullet\otimes_RK$ acyclic，則

$$
\boxed{
\mathscr A_R(C^\bullet)
=
\varpi^{\delta_R(C^\bullet)}R
}
\tag{6.1}
$$

在 canonical generic trivialization 下成立。

## Proof sketch

對 finite-length cohomology做 devissage。

每個 cyclic summand

$$
R/\varpi^nR
$$

可由 elementary two-term complex

$$
R\xrightarrow{\varpi^n}R
$$

表示。

Section 4 已固定其 determinant contribution。

direct sum令 determinant tensor product，length相加，因此所有 cyclic factors相乘後得到 exponent

$$
\sum_i(-1)^i\operatorname{length}H^i.
$$

證畢。

---

# 7. Free rank-$2$ plus finite cohomology

現在考慮最接近目前 BSD target 的 abstract model：

$$
H^1(C^\bullet)
=
\Lambda\oplus T_1,
$$

其中

$$
\Lambda
$$

是 rank-$2$ free $R$-module，

$$
T_1
$$

有限；

並假設

$$
H^2(C^\bullet)
=
T_2
$$

有限，

其他 cohomology 為零。

令

$$
D_\Lambda
=
\det_R\Lambda.
$$

則 generic arithmetic line為

$$
\mathscr A_K(C^\bullet)
\simeq
\det_K(\Lambda\otimes_RK).
$$

而 integral line為：

## Theorem 7.1

$$
\boxed{
\mathscr A_R(C^\bullet)
=
\varpi^{
\operatorname{length}(T_2)
-
\operatorname{length}(T_1)
}
D_\Lambda.
}
\tag{7.1}
$$

這是 free determinant 與 finite cohomology 的第一個統一公式。

---

# 8. Global finite Euler factor

若回到 global rational setting，對每個 prime $\ell$ 定義

$$
\delta_\ell(C^\bullet)
=
\sum_i
(-1)^i
\operatorname{length}_{\mathbf Z_\ell}
H^i(C^\bullet)_{\mathrm{tor},\ell}.
$$

定義 multiplicative finite Euler factor

$$
\boxed{
q(C^\bullet)
:=
\prod_\ell
\ell^{\delta_\ell(C^\bullet)}.
}
\tag{8.1}
$$

只有有限多個 prime有非零 exponent。

在 Section 7 的 two-degree model 中，

$$
\boxed{
q(C^\bullet)
=
\frac{|T_2|}{|T_1|}.
}
\tag{8.2}
$$

並且 global arithmetic line在 rational determinant space中對應

$$
\boxed{
\mathscr A(C^\bullet)
=
q(C^\bullet)\,
D_\Lambda.
}
\tag{8.3}
$$

這個 $q(C^\bullet)$ 是 derived Euler scalar。

它不是 regulator，也不是 saturation index。

---

# 9. Saturation 與 finite cohomology 同時存在

令

$$
\Lambda'
\subset\Lambda
$$

為 full-rank sublattice，index

$$
n=[\Lambda:\Lambda'].
$$

則

$$
D_{\Lambda'}
=
nD_\Lambda.
$$

由 (8.3)，

$$
\mathscr A(C^\bullet)
=
q(C^\bullet)D_\Lambda
=
\frac{q(C^\bullet)}{n}
D_{\Lambda'}.
\tag{9.1}
$$

因此如果實際 arithmetic construction先給出未飽和 lattice $\Lambda'$，那麼 derived determinant correction不是單獨的 $n$，也不是單獨的 $q$，而是 ratio

$$
\boxed{
\frac{q(C^\bullet)}{n}.
}
\tag{9.2}
$$

這是 Round 005 的 lattice index與本輪 finite Euler factor的第一次合流。

---

# 10. Calibrated determinant relative to derived arithmetic line

假設

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times.
$$

derived arithmetic line generator相對於 $\Delta_\Lambda$ 的 scalar是

$$
q(C^\bullet).
$$

因此 calibrated determinant相對 derived line的 scalar為

$$
\boxed{
b
=
\frac{a}{q(C^\bullet)}.
}
\tag{10.1}
$$

對每個 prime $\ell$，

$$
\boxed{
v_\ell(b)
=
d_\ell
-
\delta_\ell(C^\bullet),
}
\tag{10.2}
$$

其中

$$
d_\ell=v_\ell(a).
$$

定義：

$$
\boxed{
\varepsilon_\ell
:=
d_\ell
-
\delta_\ell(C^\bullet).
}
\tag{10.3}
$$

稱為 derived relative defect。

---

# 11. Derived closure 不等於 primitive lattice closure

如果

$$
\varepsilon_\ell=0,
$$

只代表 calibrated determinant與 derived arithmetic line在 $\ell$-adic scale上匹配。

它不代表：

$$
d_\ell=0.
$$

也不代表：

$$
\delta_\ell(C^\bullet)=0.
$$

例如若

$$
d_\ell=1
$$

且

$$
\delta_\ell(C^\bullet)=1,
$$

仍有

$$
\varepsilon_\ell=0.
$$

因此：

## No-Go 11.1

$$
\boxed{
\text{derived determinant closure does not imply saturated Mordell--Weil lattice.}
}
\tag{11.1}
$$

finite cohomology defect可以和 lattice defect在 determinant line中抵消。

---

# 12. Euler cancellation ambiguity

更強地說，even if

$$
\delta_\ell(C^\bullet)=0,
$$

也不能推出所有 torsion cohomology都消失。

例如

$$
\operatorname{length}(T_1)
=
\operatorname{length}(T_2)
=
1
$$

時，

$$
\delta_\ell
=
-1+1
=
0,
$$

但

$$
T_1\neq0,
\qquad
T_2\neq0.
$$

因此：

## No-Go 12.1

$$
\boxed{
\delta_\ell=0
\not\Rightarrow
H^i(C^\bullet)_{\mathrm{tor},\ell}=0
\text{ for every }i.
}
\tag{12.1}
$$

determinant line只看 alternating Euler sum，不看完整 torsion profile。

---

# 13. Refined local profile

因此每個 prime應保留兩層資料。

### Coarse determinant defect

$$
\delta_\ell
=
\sum_i
(-1)^i
\ell_i,
$$

其中

$$
\ell_i
:=
\operatorname{length}
H^i(C^\bullet)_{\mathrm{tor},\ell}.
$$

### Refined cohomology profile

$$
\boxed{
\mathbf L_\ell
=
(\ell_i)_i.
}
\tag{13.1}
$$

derived determinant closure只需要 coarse scalar $\delta_\ell$。

若要進一步分辨 Sha-type、torsion-type、local-condition-type finite groups，必須保留 refined profile $\mathbf L_\ell$。

---

# 14. Exact triangle additivity

令

$$
A^\bullet
\longrightarrow
B^\bullet
\longrightarrow
C^\bullet
\longrightarrow
A^\bullet[1]
$$

為 exact triangle of perfect complexes。

determinant functor給出

$$
\det(B^\bullet)
\simeq
\det(A^\bullet)
\otimes
\det(C^\bullet).
$$

因此 arithmetic-oriented lines滿足

$$
\boxed{
\mathscr A(B^\bullet)
\simeq
\mathscr A(A^\bullet)
\otimes
\mathscr A(C^\bullet).
}
\tag{14.1}
$$

在 finite torsion local setting：

## Theorem 14.1

$$
\boxed{
\delta_R(B^\bullet)
=
\delta_R(A^\bullet)
+
\delta_R(C^\bullet).
}
\tag{14.2}
$$

這是 derived Euler ledger 的 additivity law。

---

# 15. Mapping-cone comparison theorem

令

$$
f:
C^\bullet
\longrightarrow
D^\bullet
$$

為 morphism of perfect $R$-complexes，並假設

$$
f\otimes_RK
$$

是 quasi-isomorphism。

則

$$
\operatorname{Cone}(f)\otimes_RK
$$

acyclic。

exact triangle

$$
C^\bullet
\longrightarrow
D^\bullet
\longrightarrow
\operatorname{Cone}(f)
\longrightarrow
C^\bullet[1]
$$

給出：

## Theorem 15.1

relative arithmetic determinant lattice滿足

$$
\boxed{
\mathscr A_R(D^\bullet)
=
\varpi^{
\delta_R(\operatorname{Cone}(f))
}
\mathscr A_R(C^\bullet)
}
\tag{15.1}
$$

在 generic determinant line的自然識別下成立。

其中

$$
\boxed{
\delta_R(\operatorname{Cone}(f))
=
\sum_i
(-1)^i
\operatorname{length}_R
H^i(\operatorname{Cone}(f)).
}
\tag{15.2}
$$

這是 Round 006 finite-cokernel determinant formula 的 derived generalization。

---

# 16. Same-rank lattice inclusion 是特例

令

$$
M\hookrightarrow N
$$

為同 rank free $R$-modules，finite cokernel length為 $c$。

把 $M,N$ 放在 degree $1$。

則 cone的唯一 finite cohomology是

$$
H^1(\operatorname{Cone}(f))
=
N/M,
$$

所以

$$
\delta(\operatorname{Cone}(f))
=
-c.
$$

因此

$$
\mathscr A(N)
=
\varpi^{-c}
\mathscr A(M).
$$

因為 degree-$1$ arithmetic line正是正向 determinant，

$$
\det N
=
\varpi^{-c}\det M.
$$

等價地，

$$
\det M
=
\varpi^c\det N.
$$

這與 Round 005 的 saturation formula完全一致。

---

# 17. Derived support theorem

對 global comparison

$$
f:
C^\bullet
\longrightarrow
D^\bullet,
$$

假設 generic fiber是 quasi-isomorphism。

定義 bad support

$$
S_f
:=
\{
\ell:
H^\ast(\operatorname{Cone}(f))_\ell\neq0
\}.
$$

若 $S_f$ finite，則 relative determinant scalar是 $S_f$-unit。

更精確地：

## Theorem 17.1

對

$$
\ell\notin S_f,
$$

有

$$
\delta_\ell(\operatorname{Cone}(f))=0,
$$

因此 local determinant lattices相同。

所以：

$$
\boxed{
\text{support of the relative determinant scalar}
\subseteq
\text{support of cone cohomology}.
}
\tag{17.1}
$$

這把 Round 006 的 away-from-$S$ integral isomorphism重新表達成 cone acyclicity。

---

# 18. Comparison-chain ledger 變成 cone Euler sum

考慮 chain

$$
C_0^\bullet
\xrightarrow{f_1}
C_1^\bullet
\xrightarrow{f_2}
\cdots
\xrightarrow{f_m}
C_m^\bullet.
$$

令

$$
K_j^\bullet
=
\operatorname{Cone}(f_j).
$$

則總 relative defect在 prime $\ell$ 為

$$
\boxed{
\varepsilon_\ell^{\mathrm{chain}}
=
\sum_{j=1}^m
\delta_\ell(K_j^\bullet).
}
\tag{18.1}
$$

所以 Round 006 的 scalar valuation ledger，現在被提升成：

$$
\boxed{
\text{valuation ledger}
=
\text{alternating sum of cone cohomology lengths}.
}
$$

---

# 19. Local conditions 可以用 exact triangle加入

典型 Selmer construction會有 global complex與 local-condition complex。

抽象地，若有 exact triangle

$$
C_{\mathrm{Sel}}
\longrightarrow
C_{\mathrm{glob}}
\longrightarrow
C_{\mathrm{loc}}
\longrightarrow
C_{\mathrm{Sel}}[1],
$$

則

$$
\delta(C_{\mathrm{glob}})
=
\delta(C_{\mathrm{Sel}})
+
\delta(C_{\mathrm{loc}}).
$$

所以

$$
\boxed{
\delta(C_{\mathrm{Sel}})
=
\delta(C_{\mathrm{glob}})
-
\delta(C_{\mathrm{loc}}).
}
\tag{19.1}
$$

這表示 local correction 不必手動乘進去。

如果 actual Selmer complex與 local complexes定義清楚，determinant functor會自動決定 exponent sign。

但本輪不把任何具體 Tamagawa factor直接等同某個 $\delta$；那需要實際 complex identification。

---

# 20. Sha、torsion、Tamagawa 不能只靠名稱塞進公式

derived determinant framework可以統一 finite modules，但有一個嚴格限制：

> 必須先證明某個具體 finite arithmetic group真的出現在所選 complex 的哪一個 cohomological degree，或哪一個 mapping cone。

例如不能只因為一個有限群「看起來像 Sha correction」就把它乘進 $q(C^\bullet)$。

所以：

$$
\boxed{
\text{group identification}
\longrightarrow
\text{cohomological degree}
\longrightarrow
\text{determinant exponent}
}
\tag{20.1}
$$

順序不能反過來。

---

# 21. Free regulator 與 finite Euler factor 必須分層

這裡出現一個非常重要的 normalization warning。

在 Section 8，

$$
\mathscr A(C^\bullet)
=
q(C^\bullet)D_\Lambda.
$$

但 height regulator是定義在 free determinant上：

$$
\mathcal R_h:
D_\Lambda^{\otimes2}
\longrightarrow
K.
$$

若錯誤地把整個 derived line element

$$
q(C^\bullet)\Delta_\Lambda
$$

直接丟進 quadratic regulator，會得到

$$
q(C^\bullet)^2
\operatorname{Reg}(\Lambda).
$$

然而 determinant-of-cohomology 本身只告訴我們 finite Euler scalar在線性 determinant line上出現一次。

因此：

## Warning 21.1

$$
\boxed{
\text{不能在沒有固定 full fundamental-line duality convention 前，
把 finite Euler factor 自動平方。}
}
\tag{21.1}
$$

free regulator與 finite cohomology correction必須先分層，再由完整 BSD fundamental-line pairing決定如何組合。

---

# 22. 這修正了「把所有東西塞進同一 determinant 再平方」的誘惑

Round 002--004 的 quadratic regulator argument適用於：

$$
\text{free rank-$2$ determinant direction}.
$$

本輪顯示：

$$
\boxed{
\text{finite torsion determinant factor不應在未檢查 duality convention時
直接和 free determinant一起做 quadratic self-pairing。}
}
\tag{22.1}
$$

否則有限群 correction可能被 double-count。

所以更安全的架構是：

$$
\boxed{
\text{free determinant layer}
+
\text{finite Euler layer}
+
\text{duality / fundamental-line assembly}.
}
\tag{22.2}
$$

---

# 23. A two-layer BSD symbolic object

因此對 rank-$2$ target，先定義兩層資料。

### Free determinant datum

$$
\Delta_{\mathrm{free}}
\in
D_\Lambda.
$$

其 height regulator為

$$
\operatorname{Reg}_h(\Delta_{\mathrm{free}}).
$$

### Finite Euler datum

$$
q(C^\bullet)
=
\prod_\ell
\ell^{\delta_\ell(C^\bullet)}.
$$

在未固定完整 fundamental-line convention前，不先決定最終 scalar是

$$
q\operatorname{Reg}
$$

還是其他 duality-adjusted combination。

真正下一步是把這兩層放入同一個 self-dual fundamental line。

---

# 24. Derived relative closure theorem

令 calibrated free determinant為

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda.
$$

令 arithmetic complex Euler scalar為

$$
q=q(C^\bullet).
$$

若要比較 calibrated determinant與 arithmetic-oriented determinant line，relative scalar是

$$
b=\frac{a}{q}.
$$

## Theorem 24.1

global derived determinant closure到 sign等價於

$$
\boxed{
b=\pm1.
}
\tag{24.1}
$$

即

$$
\boxed{
a=\pm q.
}
\tag{24.2}
$$

local 等價條件為

$$
\boxed{
d_\ell
=
\delta_\ell(C^\bullet)
\quad
\text{for every }\ell.
}
\tag{24.3}
$$

這是 Round 005--006 lattice defect與本輪 Euler defect的統一 closure equation。

---

# 25. Primitive closure 與 derived closure 是兩個不同命題

### Primitive lattice closure

$$
d_\ell=0
\quad
\text{for every }\ell.
$$

等價於

$$
a=\pm1.
$$

### Derived determinant closure

$$
d_\ell
=
\delta_\ell(C^\bullet)
\quad
\text{for every }\ell.
$$

等價於

$$
a=\pm q.
$$

兩者只有在

$$
\delta_\ell(C^\bullet)=0
$$

對所有 $\ell$ 時才相同。

所以：

$$
\boxed{
\text{primitive closure}
\neq
\text{derived closure}
}
\tag{25.1}
$$

一般而言。

---

# 26. Determinant equality 不能單獨證明 Sha-type group trivial

即使 derived closure完全成立，

$$
a=\pm q,
$$

也只證明 total determinant balance。

因為 Section 12 的 Euler cancellation可能存在，所以不能因此推出：

$$
T_1=0,
$$

$$
T_2=0,
$$

或任何具名 finite group individually trivial。

因此：

## No-Go 26.1

$$
\boxed{
\text{determinant-of-cohomology equality proves Euler product data,
not the individual finite-group decomposition.}
}
\tag{26.1}
$$

如果 strong BSD proof需要某一個 finite group的 exact order，而不是只要總 product，就必須保留 refined cohomology information。

---

# 27. Derived finite-prime certificate

假設只有有限 set $S$ 可能出現：

- lattice defects $d_\ell$；
- torsion Euler defects $\delta_\ell$；
- comparison-cone defects。

則對

$$
\ell\notin S
$$

所有 derived defects都為零。

對每個

$$
\ell\in S
$$

計算

$$
\varepsilon_\ell
=
d_\ell
-
\delta_\ell(C^\bullet)
-
\sum_j
\delta_\ell(K_j^\bullet),
$$

其中 $K_j^\bullet$ 是尚未 absorbed into $C^\bullet$ 的 comparison cones。

若

$$
\varepsilon_\ell=0
$$

對所有 $\ell\in S$，則 global derived relative scalar為 unit到 sign。

這是一個真正 finite-prime derived certificate。

---

# 28. Additive valuation form

乘法 scalar bookkeeping經 valuation後全部變成加法。

如果總 scalar schematic 地為

$$
a_{\mathrm{tot}}
=
a_{\mathrm{lat}}
\cdot
a_{\mathrm{coh}}
\cdot
a_{\mathrm{cmp}},
$$

則

$$
v_\ell(a_{\mathrm{tot}})
=
v_\ell(a_{\mathrm{lat}})
+
v_\ell(a_{\mathrm{coh}})
+
v_\ell(a_{\mathrm{cmp}}).
$$

在 derived language 中：

$$
\boxed{
v_\ell(a_{\mathrm{coh}})
=
\delta_\ell(C^\bullet),
}
$$

$$
\boxed{
v_\ell(a_{\mathrm{cmp}})
=
\sum_j
\delta_\ell(K_j^\bullet).
}
$$

所以 local valuation ledger本質上就是 Euler-characteristic ledger。

---

# 29. Support theorem becomes a cohomology-support theorem

Round 006 需要一個 structural theorem：

$$
\ell\notin S
\Longrightarrow
\text{integral comparison isomorphism}.
$$

本輪可以更 invariant 地寫成：

$$
\boxed{
\ell\notin S
\Longrightarrow
H^\ast(K_j^\bullet)_\ell=0
\text{ for every comparison cone }K_j^\bullet.
}
\tag{29.1}
$$

也就是：

$$
\boxed{
\text{support control}
=
\text{torsion cohomology support control}.
}
$$

這比逐一追 scalar denominator更接近 derived arithmetic本身。

---

# 30. 一個重要 compression

如果 local comparison map 很複雜，但其 cone cohomology容易理解，那麼根本不必直接計算 determinant scalar。

只需知道：

$$
\operatorname{length}
H^i(\operatorname{Cone}(f))
$$

就得到 relative determinant valuation。

所以：

$$
\boxed{
\text{scalar computation}
\rightsquigarrow
\text{finite cohomology length computation}.
}
\tag{30.1}
$$

這正適合交給本地端後置驗證。

---

# 31. 對目前 $389.a1$ symbolic line 的含義

目前 web symbolic line應把後續問題拆成：

### Layer A: free determinant

延續 Round 003--005：

$$
\Delta_{\mathrm{cal}}
\in
\det H^1_{\mathrm{free}}.
$$

### Layer B: finite cohomology

找出 actual Selmer / comparison complexes的 finite cohomology groups與 degrees。

### Layer C: comparison cones

每一個 period / local-condition / descent map若 generic 是 iso，建立其 cone並讀 length。

### Layer D: fundamental-line assembly

最後才決定 free regulator、finite Euler factor、archimedean period如何在完整 BSD line中組合。

這比直接把所有 scalar乘成一個 $C$ 更安全。

---

# 32. 本輪已證

在 perfect-complex determinant formalism與明確 convention下，本輪證明：

1. arithmetic-oriented determinant line $\mathscr A=\det(C)^{-1}$ 的 sign convention；
2. finite torsion cohomology對 local determinant lattice的 Euler exponent

$$
\delta
=
\sum_i(-1)^i\operatorname{length}H^i_{\mathrm{tor}};
$$

3. rank-$2$ free $H^1$ 加 finite $T_1,T_2$ 時

$$
\mathscr A
=
\varpi^{\operatorname{length}T_2-\operatorname{length}T_1}
D_\Lambda;
$$

4. global finite Euler factor

$$
q(C)=\prod_\ell\ell^{\delta_\ell};
$$

5. saturation index與 finite Euler factor合成為 $q/n$；
6. calibrated determinant相對 derived line的 local defect

$$
\varepsilon_\ell=d_\ell-\delta_\ell;
$$

7. exact triangle下 Euler defect additivity；
8. mapping cone comparison formula；
9. same-rank lattice inclusion是 mapping-cone theorem特例；
10. comparison-chain scalar valuation等於 cone Euler defects之和；
11. support control等價於 cone torsion support control；
12. derived closure與 primitive lattice closure不同；
13. determinant equality不能推出 individual finite groups trivial；
14. finite Euler factor不能在未固定 full duality convention前直接平方進 regulator。

---

# 33. 本輪沒有證明

本輪沒有證明：

1. actual BSD Selmer complex採用哪一個 precise degree convention；
2. actual $H^1,H^2$ 與 Mordell--Weil、Sha、torsion的 exact identification；
3. actual local-condition triangles；
4. actual Tamagawa factors在哪一個 cone / degree出現；
5. actual finite Euler scalar $q(C)$；
6. actual comparison-cone cohomology；
7. actual derived relative defects $\varepsilon_\ell$；
8. full self-dual BSD fundamental line；
9. finite Euler factor在 final BSD leading-term formula中的 precise exponent；
10. BSD。

---

# 34. 給本地端的最小驗證清單

## V1. Fix the actual complex

明確指定 Selmer / arithmetic complex

$$
C^\bullet
$$

以及 cohomological degrees。

## V2. Identify free and torsion cohomology

分解

$$
H^i(C^\bullet)
$$

的 free part與 finite part。

## V3. Compute local Euler profiles

對 relevant primes $\ell$，記錄

$$
\mathbf L_\ell
=
(
\operatorname{length}H^i_{\mathrm{tor},\ell}
)_i.
$$

不要只記 alternating sum。

## V4. Compute coarse Euler defect

$$
\delta_\ell
=
\sum_i(-1)^iL_{\ell,i}.
$$

## V5. Build comparison cones

每個 generic quasi-isomorphism都建立

$$
K_j^\bullet
=
\operatorname{Cone}(f_j).
$$

## V6. Read determinant valuations from lengths

使用

$$
v_\ell(a_j)
=
\delta_\ell(K_j^\bullet).
$$

## V7. Keep saturation separate

獨立記錄 free lattice defect

$$
d_\ell.
$$

## V8. Compare derived defects

檢查

$$
\varepsilon_\ell
=
d_\ell-\delta_\ell-\sum_j\delta_\ell(K_j).
$$

## V9. Do not square finite factors prematurely

在 full duality / fundamental-line convention未固定前，finite Euler scalar不要直接帶入 quadratic height regulator。

---

# 35. 本輪核心結論

Round 005--006 的 lattice ledger現在被提升為：

$$
\boxed{
\text{derived Euler-characteristic ledger}.
}
$$

free lattice defect給

$$
d_\ell,
$$

finite cohomology給

$$
\delta_\ell(C^\bullet),
$$

comparison maps給

$$
\delta_\ell(\operatorname{Cone}(f)).
$$

所有 multiplicative normalization經 valuation後都變成有限 cohomology length的加法。

因此 absolute determinant closure不再只是：

$$
\text{saturation index}=1,
$$

而可以更一般地寫成：

$$
\boxed{
\text{free lattice defect}
=
\text{finite Euler defect}
+
\text{comparison-cone defect}.
}
$$

但這也帶來一個重要警告：

$$
\boxed{
\text{Euler balance 可以成立，而 individual finite groups仍然非零。}
}
$$

所以 determinant-of-cohomology 是強力的 global product closure工具，但不是 individual-group triviality oracle。

---

# 36. 下一輪建議

## BSD Symbolic Round 008

**題目：**

> Self-Dual Fundamental Line and the Correct Regulator Exponent

現在最大的符號問題變成：

> free determinant 的 quadratic height regulator，與 derived finite Euler line，究竟如何在完整 self-dual BSD fundamental line中組合？

下一輪應該研究：

1. primal Selmer complex與 dual Selmer complex的 determinant pairing；
2. self-duality shift如何改變 determinant exponent；
3. 為什麼 free rank-$2$ regulator是 quadratic，而 finite Euler factors不一定被平方；
4. torsion square、dual torsion、Sha-type self-duality如何改變 exponent；
5. 如何避免把 finite correction double-count；
6. 是否能抽象推出一個 BSD-shaped scalar：

$$
\text{period}^{-1}
\times
\text{regulator}
\times
\text{finite Euler product},
$$

而不是錯誤的

$$
\text{period}^{-1}
\times
\text{regulator}
\times
(\text{finite Euler product})^2.
$$

若 Round 008 能把這個 exponent structure定死，整條 web symbolic line就會第一次接近「完整 leading-term architecture」，而不只是 determinant subproblem。
