# BSD Symbolic Round 004
## Higher Projective Jets and the First Nonzero Determinant Order

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** conditional symbolic development；未做新的大型數值計算；未主張 BSD 已證明  
**承接：** BSD Symbolic Round 001--003  
**本輪目標：** 定義第一次非零 higher projective jet，證明其 scalar normalization law，分離 scalar vanishing order、projective jet order 與 determinant gauge weight，並建立 higher Bockstein bridge。

---

# 1. 問題

Round 003 處理了一階 projective derivative

$$
\operatorname{KS}_Z:
T\longrightarrow \operatorname{Hom}(L,H/L),
$$

其中

$$
L=K\kappa,
\qquad
\kappa=Z(0)\neq0.
$$

若

$$
\operatorname{KS}_Z\neq0,
$$

則一個 projectively transverse direction 已足以產生 rank-$2$ determinant direction。

現在處理真正困難的分支：

$$
\operatorname{KS}_Z=0.
$$

這不代表 determinant route 失敗。它只表示 projective family 在原點 first-order critical。

本輪證明：

$$
\boxed{
\text{higher projective jet order 可以任意提高，但 rank-$2$ determinant 的 gauge weight 始終是 }2.
}
$$

因此 scalar regulator 的 gauge weight 始終是 $4$，而不會隨 jet order 增加。

---

# 2. 基本設定

令

$$
R=K[[x_1,\ldots,x_d]]
$$

為形式冪級數環，

$$
\mathfrak m=(x_1,\ldots,x_d)
$$

為其 maximal ideal。

令 $H$ 為二維 $K$-向量空間，並取

$$
Z\in H\widehat\otimes_KR
$$

滿足

$$
Z(0)=\kappa\neq0.
\tag{2.1}
$$

定義

$$
L:=K\kappa,
$$

以及 quotient

$$
Q:=H/L.
$$

令

$$
\pi:H\longrightarrow Q
$$

為自然投影。

因為

$$
\pi(\kappa)=0,
$$

所以

$$
\pi(Z)\in Q\widehat\otimes\mathfrak m.
$$

---

# 3. Projective vanishing order

## Definition 3.1

若

$$
\pi(Z)\neq0,
$$

定義 projective vanishing order

$$
m_{\mathrm{proj}}(Z)
:=
\operatorname{ord}_{\mathfrak m}\pi(Z),
$$

即唯一整數 $m\ge1$ 使

$$
\pi(Z)
\in
Q\otimes\mathfrak m^m
$$

但

$$
\pi(Z)
\notin
Q\otimes\mathfrak m^{m+1}.
$$

若

$$
\pi(Z)=0,
$$

則 family 在整個 formal germ 中都停留在固定 line $L$，此時記

$$
m_{\mathrm{proj}}(Z)=+\infty.
$$

因此：

- $m_{\mathrm{proj}}=1$ 對應 Round 003 的非零 first projective derivative；
- $m_{\mathrm{proj}}>1$ 對應 first-order critical；
- $m_{\mathrm{proj}}=+\infty$ 表示沒有任何 transverse projective variation。

---

# 4. First nonzero transverse jet

設

$$
m:=m_{\mathrm{proj}}(Z)<+\infty.
$$

則 $\pi(Z)$ 在

$$
Q\otimes
\mathfrak m^m/\mathfrak m^{m+1}
$$

中有非零 leading class。

由標準識別

$$
\mathfrak m^m/\mathfrak m^{m+1}
\simeq
\operatorname{Sym}^m(T^\ast),
$$

其中

$$
T:=(\mathfrak m/\mathfrak m^2)^\ast,
$$

得到

$$
\tau_m(Z)
\in
\operatorname{Sym}^m(T^\ast)\otimes Q,
\qquad
\tau_m(Z)\neq0.
\tag{4.1}
$$

這是第一個非零 transverse vector-valued jet。

---

# 5. Intrinsic projective jet

$\tau_m(Z)$ 仍然使用了 generator $\kappa$ 所決定的 representative $Z$。

真正 invariant 的物件應該記錄 line $L$ 本身。

## Definition 5.1

定義 intrinsic first nonzero projective jet

$$
\mathcal P_m(Z)
\in
\operatorname{Sym}^m(T^\ast)
\otimes
\operatorname{Hom}(L,Q)
$$

如下。

對

$$
\ell=c\kappa\in L,
$$

令

$$
\mathcal P_m(Z)(\ell)
:=
c\,\tau_m(Z).
\tag{5.1}
$$

這個定義看似使用 $\kappa$，但下一節證明它其實不依賴 scalar trivialization。

---

# 6. Unit-renormalization invariance

令

$$
g\in R^\times
$$

為任意 formal unit，並設

$$
\widetilde Z=gZ.
$$

令

$$
g_0:=g(0)\in K^\times.
$$

則

$$
\widetilde Z(0)=g_0\kappa,
$$

所以 $\widetilde Z$ 與 $Z$ 決定同一條 line $L$。

## Theorem 6.1

有

$$
\boxed{
m_{\mathrm{proj}}(\widetilde Z)
=
m_{\mathrm{proj}}(Z).
}
\tag{6.1}
$$

而且

$$
\boxed{
\tau_m(\widetilde Z)
=
g_0\,\tau_m(Z).
}
\tag{6.2}
$$

最後，

$$
\boxed{
\mathcal P_m(\widetilde Z)
=
\mathcal P_m(Z).
}
\tag{6.3}
$$

## Proof

因為

$$
\pi(\widetilde Z)
=
g\,\pi(Z),
$$

而 $g$ 是 unit，所以 multiplication by $g$ 不改變 $\mathfrak m$-adic order，得到 (6.1)。

在 associated graded 的 degree-$m$ 部分，只有 $g$ 的 constant term 會作用，因此得到

$$
\tau_m(\widetilde Z)
=
g_0\tau_m(Z).
$$

現在令

$$
\widetilde\kappa=g_0\kappa.
$$

對同一個

$$
\ell=c\kappa
=
\frac{c}{g_0}\widetilde\kappa,
$$

有

$$
\mathcal P_m(\widetilde Z)(\ell)
=
\frac{c}{g_0}
\tau_m(\widetilde Z)
=
c\tau_m(Z)
=
\mathcal P_m(Z)(\ell).
$$

故得 (6.3)。證畢。

---

# 7. 第一個關鍵結論

Theorem 6.1 告訴我們：

$$
\boxed{
\text{first nonzero projective jet order 與 intrinsic projective jet 都完全不依賴 scalar normalization。}
}
$$

也就是說，若 BF/Kato family 被任意 unit

$$
g(x_1,\ldots,x_d)
$$

重新 normalize，所有 higher-order scalar contamination 都不會改變

$$
m_{\mathrm{proj}}
$$

或

$$
\mathcal P_m.
$$

這比 Round 003 的一階 shear cancellation 更強，因為現在是所有低於 first transverse order 的 scalar mixing 一次消掉。

---

# 8. Anchored higher determinant tensor

由

$$
\det H
\simeq
L\otimes Q
$$

以及

$$
\operatorname{Hom}(L,Q)
\simeq
L^\ast\otimes Q,
$$

可得

$$
L^{\otimes2}
\otimes
\operatorname{Hom}(L,Q)
\simeq
\det H.
$$

選擇 generator

$$
\kappa\in L,
$$

定義 anchored higher determinant tensor

$$
\mathcal A_m(Z)
\in
\operatorname{Sym}^m(T^\ast)
\otimes
\det H
$$

為

$$
\boxed{
\mathcal A_m(Z)
:=
\kappa^{\otimes2}
\otimes
\mathcal P_m(Z).
}
\tag{8.1}
$$

在 concrete representative 中，它就是

$$
\boxed{
\mathcal A_m(Z)
=
\kappa\wedge\tau_m(Z).
}
\tag{8.2}
$$

這裡 (8.2) 的意思是對每個 homogeneous tangent monomial，把 $\tau_m$ 的 $Q$-class 任取 lift 到 $H$，再與 $\kappa$ wedge；結果與 lift 無關。

---

# 9. Gauge weight 與 jet order 分離

令

$$
\widetilde Z=gZ,
\qquad
g_0=g(0).
$$

由 Theorem 6.1，

$$
\mathcal P_m(\widetilde Z)
=
\mathcal P_m(Z),
$$

而 leading generator 變成

$$
\widetilde\kappa=g_0\kappa.
$$

所以

$$
\mathcal A_m(\widetilde Z)
=
g_0^2
\mathcal A_m(Z).
$$

因此：

## Theorem 9.1

對所有有限 projective jet order $m$，

$$
\boxed{
\mathcal A_m
\text{ 的 scalar gauge weight 永遠是 }2.
}
\tag{9.1}
$$

這個 weight 與 $m$ 無關。

換句話說：

$$
\boxed{
\text{jet order 描述 deformation 的消失深度；exterior degree 決定 gauge weight。}
}
\tag{9.2}
$$

這正是 Round 003 所提出猜想的證明。

---

# 10. Rank-$2$ scalar regulator 的 weight 也與 jet order 無關

令 height determinant tensor 為

$$
\mathcal R_h
\in
(\det H^\ast)^{\otimes2}.
$$

把 $\mathcal A_m$ 自配對後，

$$
\mathcal R_h(
\mathcal A_m\otimes\mathcal A_m
)
$$

的 gauge weight 為

$$
2+2=4.
$$

因此：

## Corollary 10.1

不論

$$
m_{\mathrm{proj}}=1,2,3,\ldots,
$$

rank-$2$ self-paired regulator scalar 的 common normalization weight 永遠是

$$
\boxed{
4.
}
\tag{10.1}
$$

所以只要 rank-$0$ calibrator $b_0$ 是 weight one，

$$
b_0^2
$$

永遠足以校準 determinant level，

而

$$
b_0^4
$$

永遠足以校準 scalar regulator level。

不需要因為 higher jet order 增加 calibration power。

---

# 11. Source coordinate change

現在考慮 formal reparametrization

$$
\varphi:
(R,\mathfrak m)
\longrightarrow
(R',\mathfrak m')
$$

其 linear tangent map

$$
d\varphi_0:
T'\longrightarrow T
$$

可逆。

令

$$
Z':=\varphi^\ast Z.
$$

## Theorem 11.1

有

$$
\boxed{
m_{\mathrm{proj}}(Z')
=
m_{\mathrm{proj}}(Z).
}
\tag{11.1}
$$

而 first nonzero projective jet 依 symmetric covariant law 變換：

$$
\boxed{
\mathcal P_m(Z')
=
\mathcal P_m(Z)
\circ
\operatorname{Sym}^m(d\varphi_0).
}
\tag{11.2}
$$

因此 $\mathcal P_m$ 本身是 coordinate-free tensor，而 coordinate components 具有 degree-$m$ transformation law。

這表示：

$$
\boxed{
\text{gauge weight 與 coordinate weight 是兩個不同概念。}
}
$$

gauge weight 固定為 determinant degree；

coordinate weight 會記住 jet order $m$。

---

# 12. 一維 distinguished direction

若 arithmetic theory 給出 canonical tangent line

$$
T_{\mathrm{cyc}}\subset T,
$$

取非零

$$
\xi\in T_{\mathrm{cyc}}.
$$

則可評估

$$
\mathcal P_m(Z)(\xi^{\otimes m})
\in
\operatorname{Hom}(L,Q).
$$

若改變 tangent vector normalization

$$
\xi\mapsto c\xi,
$$

則

$$
\mathcal P_m(Z)((c\xi)^{\otimes m})
=
c^m
\mathcal P_m(Z)(\xi^{\otimes m}).
$$

所以：

$$
\boxed{
\text{沿 distinguished line 的 absolute higher jet 具有 coordinate weight }m.
}
\tag{12.1}
$$

但 anchored determinant 對 BF scalar normalization 的 gauge weight仍是 $2$。

這兩個 exponent 不應混為一談。

---

# 13. Scalar vanishing order 與 projective jet order

現在加入一個可能具有真正零點的 scalar factor。

令

$$
F\in R
$$

非零，且

$$
e:=\operatorname{ord}_{\mathfrak m}F.
$$

考慮

$$
B:=FZ.
\tag{13.1}
$$

因為 $Z(0)=\kappa\neq0$，

$$
\operatorname{ord}_{\mathfrak m}B=e.
$$

但 transverse quotient 為

$$
\pi(B)
=
F\pi(Z).
$$

若

$$
m=m_{\mathrm{proj}}(Z)<+\infty,
$$

則 associated graded ring

$$
\operatorname{gr}_{\mathfrak m}R
\simeq
K[x_1,\ldots,x_d]
$$

是 integral domain，所以兩個 nonzero initial forms 的 product 不會消失。

因此：

## Theorem 13.1

$$
\boxed{
\operatorname{ord}_{\mathfrak m}\pi(B)
=
e+m.
}
\tag{13.2}
$$

這是一個 order-additivity theorem。

---

# 14. 三種 order 必須分開

現在至少有三個不同概念：

### 14.1 Scalar vanishing order

$$
e
=
\operatorname{ord}_{\mathfrak m}F.
$$

它描述 common exceptional / Euler / Eisenstein scalar factor 的消失階。

### 14.2 Projective transverse order

$$
m
=
m_{\mathrm{proj}}(Z).
$$

它描述 arithmetic line 第一次真正離開 $L$ 的階數。

### 14.3 Determinant gauge degree

rank-$2$ 時固定為

$$
2.
$$

它只由 exterior degree 決定。

因此：

$$
\boxed{
e,\quad m,\quad 2
}
$$

是三個不同的不變量。

它們可以在 raw formula 中同時出現，但不能彼此代換。

---

# 15. 一維情形的 raw transverse order

若只有一個 formal variable $t$，令

$$
F(t)
=
f_et^e+O(t^{e+1}),
\qquad
f_e\neq0,
$$

而

$$
\pi(Z(t))
=
q_mt^m+O(t^{m+1}),
\qquad
q_m\neq0.
$$

則

$$
\pi(B(t))
=
f_eq_mt^{e+m}
+
O(t^{e+m+1}).
$$

因此 observable 的第一次 transverse term 出現在

$$
\boxed{
e+m.
}
\tag{15.1}
$$

這提供一個非常簡單的 bookkeeping rule：

$$
\boxed{
\text{raw transverse vanishing}
=
\text{scalar vanishing}
+
\text{projective transverse vanishing}.
}
$$

---

# 16. 與 analytic rank 的關係不能自動推出

即使某個 $p$-adic $L$-function 或 regulator observable 的零點階數是 $r$，本輪也不能直接推出

$$
r=e+m.
$$

需要額外的 explicit reciprocity law，確認：

1. 該 scalar observable 真正讀取 $\pi(B)$ 的 first nonzero transverse component；
2. 沒有額外 local factor；
3. 使用的 functional 不會 annihilate first nonzero transverse jet；
4. coordinate normalization 已固定；
5. 沒有另一個 independent exceptional zero。

只有在這些條件成立時，才可能得到條件式關係

$$
r=e+m.
$$

因此本輪只提供 order decomposition framework，不把它直接等同 analytic rank。

---

# 17. Higher Bockstein bridge

設

$$
m=m_{\mathrm{proj}}(Z).
$$

考慮某個 homogeneous degree-$m$ derived operator

$$
D^{(m)}
$$

其作用在 leading line 上產生一個 quotient class

$$
[D^{(m)}\kappa]
\in
\operatorname{Sym}^m(T^\ast)\otimes Q.
$$

不要求它在 $H$ 中逐字等於 raw $m$-th derivative。

只要求

$$
\boxed{
[D^{(m)}\kappa]
=
\tau_m(Z)
\quad
\text{in }
\operatorname{Sym}^m(T^\ast)\otimes Q.
}
\tag{17.1}
$$

則立即得到：

## Theorem 17.1

$$
\boxed{
\mathcal A_m(Z)
=
\kappa\wedge D^{(m)}\kappa
}
\tag{17.2}
$$

其中右側理解為 degree-$m$ symmetric tangent tensor with values in $\det H$。

任何落在 $L$ 中的 lower-order correction 或 normalization contamination 都在 wedge 中消失。

---

# 18. Higher Bockstein ambiguity

若另一個 derived operator 滿足

$$
\widetilde D^{(m)}\kappa
=
uD^{(m)}\kappa
+
\Lambda_m\kappa,
$$

其中

$$
u\in K^\times
$$

而

$$
\Lambda_m
\in
\operatorname{Sym}^m(T^\ast),
$$

則

$$
\kappa\wedge
\widetilde D^{(m)}\kappa
=
u
\kappa\wedge
D^{(m)}\kappa.
$$

所以 projective determinant direction 只看 transverse quotient class。

這是 Round 003 affine ambiguity principle 的 higher-order 版本。

---

# 19. 二維 deformation base 的新現象

現在令

$$
\dim T=2.
$$

因為

$$
\dim\operatorname{Hom}(L,Q)=1,
$$

所以在選定 target line trivialization 後，

$$
\mathcal P_m
$$

等價於一個 nonzero binary homogeneous form of degree $m$。

也就是某個

$$
P_m(X,Y)
$$

的 projective class。

若 $m=1$，其 zero locus 在

$$
\mathbf P(T)
$$

中只有一個 null direction。

這正是 Round 003 的 canonical null line。

但若

$$
m>1,
$$

zero locus 是 degree-$m$ divisor。

因此：

## Theorem 19.1

higher-order projective criticality 一般不再給出唯一 null line。

相反地，存在一個 canonical projective divisor

$$
\boxed{
\mathcal Z_m
=
\{
[\xi]\in\mathbf P(T):
\mathcal P_m(\xi^{\otimes m})=0
\}.
}
\tag{19.1}
$$

在代數閉包上，它最多包含 $m$ 個方向，計入 multiplicity。

這是從 first-order 到 higher-order 的一個真正結構變化。

---

# 20. Transverse direction 的 higher-order 定義

對

$$
[\xi]\in\mathbf P(T),
$$

若

$$
\mathcal P_m(\xi^{\otimes m})\neq0,
$$

則稱 $\xi$ 為 first-order-$m$ transverse direction。

沿這個 direction，

$$
\mathcal A_m(\xi^{\otimes m})
\neq0.
$$

因此即使整個 family 的一階 projective derivative消失，只要存在一個方向避開 $\mathcal Z_m$，仍然可以得到非零 rank-$2$ determinant direction。

因為 $P_m$ 非零，所以在無限域 $K$ 上必存在這種 direction。

---

# 21. Polarization

$\mathcal P_m$ 不只可以在單一 direction 上評估。

它是一個 symmetric $m$-linear tensor，因此可以 polarization 成

$$
\mathcal P_m(
\xi_1,\ldots,\xi_m
).
$$

這意味著 mixed weight/cyclotomic information 不必被壓成一條 diagonal path。

可以保留真正 mixed jet：

$$
\mathcal P_m(
\partial_X^{\otimes a},
\partial_t^{\otimes(m-a)}
),
$$

其中

$$
0\le a\le m.
$$

這比沿

$$
X=t
$$

之類的 diagonal substitution 安全，因為它不會預先把不同 deformation directions 混在一起。

---

# 22. 對目前 BSD 路線的直接含義

假設在抽去 common scalar vanishing factor後，target family 的 first projective derivative其實為零。

以前可能會把這視為：

> 需要再找另一條 completely different arithmetic class。

本輪顯示不必立刻如此。

更自然的流程是：

1. 先計算或理論判定

$$
m=m_{\mathrm{proj}}(Z);
$$

2. 取 first nonzero projective jet

$$
\mathcal P_m;
$$

3. 選一個不在 $\mathcal Z_m$ 的 arithmetic direction；
4. 形成

$$
\mathcal A_m;
$$

5. 用 calibrator square 消去 common BF normalization。

所以 higher degeneracy 增加的是 jet depth，不是 determinant degree。

---

# 23. Calibration theorem at arbitrary projective order

假設 target projected/desingularized family 滿足

$$
\widehat Z_E
=
C_0A_EZ_E
$$

在 relevant special-fiber normalization level，其中 $C_0,A_E\in K^\times$。

令

$$
m=m_{\mathrm{proj}}(Z_E).
$$

則

$$
\mathcal A_m(\widehat Z_E)
=
C_0^2A_E^2
\mathcal A_m(Z_E).
$$

若 rank-$0$ calibrator 滿足

$$
b_0=C_0a_0k_0,
$$

則：

## Theorem 23.1

$$
\boxed{
\mathcal A_m(Z_E)
=
\frac{a_0^2k_0^2}{A_E^2}
\frac{
\mathcal A_m(\widehat Z_E)
}{
b_0^2
}.
}
\tag{23.1}
$$

這個公式對所有

$$
m=1,2,3,\ldots
$$

完全相同。

jet order 沒有進入 calibrator exponent。

---

# 24. Regulator theorem at arbitrary projective order

同理，

$$
\mathcal R_h(
\mathcal A_m(Z_E)
\otimes
\mathcal A_m(Z_E)
)
$$

滿足

$$
\boxed{
\operatorname{Reg}_{m,E}
=
\frac{a_0^4k_0^4}{A_E^4}
\frac{
\mathcal R_h(
\mathcal A_m(\widehat Z_E)
\otimes
\mathcal A_m(\widehat Z_E)
)
}{
b_0^4
}.
}
\tag{24.1}
$$

其中 $\operatorname{Reg}_{m,E}$ 只是符號上對 first nonzero projective determinant jet 的 height determinant evaluation。

是否等於 classical BSD regulator仍需要 absolute determinant comparison。

---

# 25. 一個新的 normalization diagnostic

任何 proposed formula 若同時出現：

- projective jet order $m$；
- rank-$2$ determinant；
- common BF scalar $C$；

則 calibration power 應由 rank-$2$ exterior degree決定，而不是由 $m$ 決定。

所以以下型態一般是可疑的：

$$
\frac{\mathcal A_m}{b_0^m}
$$

除非

$$
m=2
$$

剛好偶然相等。

正確的 common gauge cancellation 是

$$
\boxed{
\frac{\mathcal A_m}{b_0^2}.
}
$$

同理 scalar regulator 是

$$
\boxed{
\frac{\mathcal R_h(\mathcal A_m^{\otimes2})}{b_0^4}.
}
$$

這提供一個完全不需要計算的 exponent sanity check。

---

# 26. 本輪已證

在形式冪級數與二維 target space 的抽象設定下，本輪證明：

1. projective vanishing order $m_{\mathrm{proj}}$ 的定義與 unit invariance；
2. first nonzero transverse jet $\tau_m$ 的 transformation law；
3. intrinsic projective jet $\mathcal P_m$ 的 scalar-normalization invariance；
4. anchored higher determinant tensor $\mathcal A_m$ 的 gauge weight恆為 $2$；
5. self-paired regulator scalar 的 gauge weight恆為 $4$；
6. source reparametrization下的 degree-$m$ symmetric tensor law；
7. scalar vanishing order與 projective order 的 additive law

$$
e+m;
$$

8. higher Bockstein quotient criterion；
9. higher Bockstein longitudinal ambiguity cancellation；
10. 二維 deformation base 在 $m>1$ 時出現 canonical degree-$m$ exceptional-direction divisor；
11. mixed jets 可用 polarization 保留，而不必 diagonal substitution；
12. calibrator square / fourth-power law 對所有 projective jet order不變。

---

# 27. 本輪沒有證明

本輪沒有證明：

1. genuine BF/Kato family 的 actual projective order是多少；
2. target 是否 first-order critical；
3. 若 first-order critical，第一次非零 order 是否為 $2$ 或更高；
4. projective order 與 analytic rank 有直接等式；
5. higher Bockstein operator 已被 arithmetic construction 實現；
6.某個 canonical arithmetic direction 一定避開 $\mathcal Z_m$；
7. calibrated higher determinant 已與 Mordell--Weil determinant lattice 對齊；
8. higher jet height evaluation 已等於 classical BSD regulator；
9. BSD。

---

# 28. 給本地端的最小驗證清單

## V1. Projective order

在抽掉明確 scalar vanishing factor後，決定

$$
m_{\mathrm{proj}}(Z_E).
$$

## V2. First nonzero transverse jet

構造

$$
\tau_m(Z_E)
$$

或至少證明它非零。

## V3. Unit-invariance drill

對 family 乘任意測試 unit

$$
g=1+\text{higher terms}
$$

確認 $m_{\mathrm{proj}}$ 與 projective jet 不變。

## V4. Gauge-degree drill

對 constant rescaling

$$
Z\mapsto cZ
$$

確認 anchored determinant乘

$$
c^2
$$

而不是 $c^m$。

## V5. Scalar/projective order separation

若 raw family 有 scalar zero order $e$，檢查 first transverse raw order 是否為

$$
e+m.
$$

## V6. Exceptional-direction divisor

若 deformation base 是二維且 $m>1$，求 binary form $P_m$ 的 zero directions，而不是硬找唯一 null line。

## V7. Higher Bockstein quotient test

只驗證

$$
[D^{(m)}\kappa]
=
\tau_m
\quad
\text{in }Q,
$$

不要求完整 lift equality。

## V8. Calibrator exponent test

不論 $m$ 多大，determinant level 都測試

$$
\frac{\mathcal A_m}{b_0^2},
$$

scalar regulator level都測試

$$
\frac{\mathcal R_h(\mathcal A_m^{\otimes2})}{b_0^4}.
$$

---

# 29. 本輪核心結論

本輪把三個容易混淆的數字徹底拆開：

$$
\boxed{
e
=
\text{scalar vanishing order},
}
$$

$$
\boxed{
m
=
\text{projective transverse jet order},
}
$$

以及

$$
\boxed{
2
=
\text{rank-$2$ determinant gauge degree}.
}
$$

raw transverse observable 的 order 可以是

$$
e+m,
$$

但 determinant calibration 的 common scalar exponent仍然只是

$$
2.
$$

因此：

$$
\boxed{
\text{高階退化不會讓 rank-$2$ calibration 從平方變成立方、四次方或 }m\text{ 次方。}
}
$$

它只把真正 transverse arithmetic information 推到更高 jet。

---

# 30. 下一輪建議

## BSD Symbolic Round 005

**題目：**

> Determinant Lattice Torsor and the Absolute BSD Anchor

現在 relative BF normalization 已被壓得相當乾淨。

下一個真正 obstruction 應該轉向：

$$
\boxed{
\text{calibrated determinant line}
\longleftrightarrow
\text{absolute Mordell--Weil / Selmer lattice determinant}.
}
$$

下一輪應研究：

1. calibrated determinant element 到底還剩什麼 $K^\times$ torsor；
2. integral lattice / rational lattice 如何固定它；
3. saturation index 如何進入 determinant；
4. basis change、isogeny、period scaling 對 absolute anchor 的 transformation law；
5. 是否能把最後的 unknown scalar壓成一個 square class、rational unit class 或 finite index；
6. classical regulator 是否其實只需要 determinant lattice 的 quadratic class，而不需要完整 oriented generator。

如果成功，BSD bridge 的最後 unknown 就可能從「神秘 period constant」降成一個可明確描述的 arithmetic lattice index problem。
