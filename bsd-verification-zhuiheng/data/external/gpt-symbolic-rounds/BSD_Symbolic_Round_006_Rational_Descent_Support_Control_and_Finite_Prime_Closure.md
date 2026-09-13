# BSD Symbolic Round 006
## Rational Descent, Support Control, and Finite-Prime Closure

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** conditional symbolic development；未做新的大型數值計算；未主張 BSD 已證明  
**承接：** BSD Symbolic Round 001--005  
**本輪目標：** 精確區分 local descent 與 global rational descent，建立 determinant scalar 的 $S$-unit support theorem、local length formula、comparison-chain support ledger，最後把 absolute BSD anchor 壓成有限 prime certificate。

---

# 1. 從 Round 005 出發

Round 005 把 absolute determinant anchor 寫成

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
$$

其中

$$
\Delta_\Lambda
$$

是 Mordell--Weil / Selmer integral determinant lattice 的 primitive generator，而理想情形希望證明

$$
a\in\mathbf Q^\times.
$$

一旦 rationality 成立，

$$
a
=
\pm
\prod_\ell
\ell^{v_\ell(a)}
$$

且只有有限多個 valuation 非零。

因此真正剩下兩個邏輯 gate：

$$
\boxed{
\text{Gate R: }a\in\mathbf Q^\times
}
$$

以及

$$
\boxed{
\text{Gate S: }v_\ell(a)=0\text{ for all but an explicit finite set }S.
}
$$

本輪先證明：這兩個 gate 必須分開。

---

# 2. Determinant line setup

令

$$
D_{\mathbf Q}
$$

為一維 $\mathbf Q$-向量空間，並令

$$
D_{\mathbf Z}
\subset
D_{\mathbf Q}
$$

為 rank-$1$ integral lattice。

取 primitive generator

$$
\Delta_\Lambda\in D_{\mathbf Z}.
$$

令 $K$ 為一個 coefficient field。

一個 calibrated determinant element為

$$
\Delta_K
\in
D_{\mathbf Q}\otimes_{\mathbf Q}K.
$$

由一維性，存在唯一

$$
a_K\in K
$$

使

$$
\boxed{
\Delta_K
=
a_K\Delta_\Lambda.
}
\tag{2.1}
$$

所有 rational descent 問題因此都化成：

$$
\boxed{
a_K
\text{ 是否其實落在 }\mathbf Q?
}
\tag{2.2}
$$

---

# 3. Local Galois descent theorem

先固定一個 prime $p$。

令

$$
K/\mathbf Q_p
$$

為有限 Galois extension，並假設

$$
\sigma(\Delta_K)
=
\Delta_K
$$

對所有

$$
\sigma\in\operatorname{Gal}(K/\mathbf Q_p).
$$

## Theorem 3.1

則

$$
\boxed{
\Delta_K
\in
D_{\mathbf Q}\otimes_{\mathbf Q}\mathbf Q_p.
}
\tag{3.1}
$$

等價地，

$$
\boxed{
a_K\in\mathbf Q_p.
}
\tag{3.2}
$$

## Proof

由

$$
\Delta_K=a_K\Delta_\Lambda
$$

且 $\Delta_\Lambda$ 為 rational fixed vector，

$$
\sigma(\Delta_K)
=
\sigma(a_K)\Delta_\Lambda.
$$

若 $\sigma(\Delta_K)=\Delta_K$，則

$$
\sigma(a_K)=a_K
$$

對所有 $\sigma$ 成立，所以

$$
a_K\in K^{\operatorname{Gal}(K/\mathbf Q_p)}
=
\mathbf Q_p.
$$

證畢。

---

# 4. Local descent 不等於 global rationality

Theorem 3.1 只能得到

$$
a_K\in\mathbf Q_p.
$$

不能得到

$$
a_K\in\mathbf Q.
$$

## No-Go 4.1

任取

$$
\alpha\in\mathbf Q_p\setminus\mathbf Q.
$$

則

$$
\Delta_p
=
\alpha\Delta_\Lambda
$$

已經是一個完全 $\mathbf Q_p$-rational 的 determinant element，但並不來自 $D_{\mathbf Q}$。

因此：

$$
\boxed{
\mathbf Q_p\text{-rational}
\not\Rightarrow
\mathbf Q\text{-rational}.
}
\tag{4.1}
$$

對目前 $p=11$ 的 BSD 路線而言：

$$
\boxed{
11\text{-adic descent 本身不能閉合 global rationality gate。}
}
\tag{4.2}
$$

---

# 5. Projective invariance 也不足以證明 rationality

在一維 determinant space中，任意非零 element 都張成同一條 projective line。

所以如果只知道

$$
[\Delta_K]
$$

在 projective sense Galois invariant，這幾乎沒有 scalar descent內容。

例如對任意

$$
\alpha\in K^\times,
$$

$$
[\alpha\Delta_\Lambda]
=
[\Delta_\Lambda].
$$

因此：

## No-Go 5.1

$$
\boxed{
\text{projective Galois invariance of a one-dimensional determinant line does not imply rationality of its generator.}
}
\tag{5.1}
$$

要證明 absolute determinant element rational，必須控制 scalar，不只是 line。

---

# 6. Global field descent theorem

令

$$
F/\mathbf Q
$$

為有限 Galois extension。

考慮

$$
\Delta_F
\in
D_{\mathbf Q}\otimes_{\mathbf Q}F.
$$

## Theorem 6.1

若

$$
\sigma(\Delta_F)
=
\Delta_F
$$

對所有

$$
\sigma\in\operatorname{Gal}(F/\mathbf Q),
$$

則

$$
\boxed{
\Delta_F\in D_{\mathbf Q}.
}
\tag{6.1}
$$

等價地，若

$$
\Delta_F=a_F\Delta_\Lambda,
$$

則

$$
\boxed{
a_F\in\mathbf Q.
}
\tag{6.2}
$$

證明與 Theorem 3.1 相同，只是 fixed field 改為 $\mathbf Q$。

這是 global rational descent 的標準 sufficient condition。

---

# 7. 一個 rational functional 就足以測試 rationality

因為

$$
\dim_{\mathbf Q}D_{\mathbf Q}=1,
$$

任取非零 rational functional

$$
\lambda
\in
D_{\mathbf Q}^\ast.
$$

令

$$
c_\Lambda
:=
\lambda(\Delta_\Lambda)
\in
\mathbf Q^\times.
$$

則對

$$
\Delta_K=a_K\Delta_\Lambda
$$

有

$$
\lambda(\Delta_K)
=
a_Kc_\Lambda.
$$

所以：

## Theorem 7.1

$$
\boxed{
\Delta_K\in D_{\mathbf Q}
\iff
\lambda(\Delta_K)\in\mathbf Q.
}
\tag{7.1}
$$

更明確地，

$$
\boxed{
a_K
=
\frac{\lambda(\Delta_K)}{c_\Lambda}.
}
\tag{7.2}
$$

這意味著 global rationality gate 在一維 determinant line上可以被壓成單一 scalar rationality test。

但 $\lambda$ 必須獨立地是 rationally normalized，不能由待證的 $\Delta_K$ 反向定義。

---

# 8. Trace 與 norm 本身不夠

若

$$
a_F\in F,
$$

則

$$
\operatorname{Tr}_{F/\mathbf Q}(a_F)
$$

與

$$
\operatorname{Norm}_{F/\mathbf Q}(a_F)
$$

本來就都在 $\mathbf Q$。

所以只知道 trace / norm rational，不足以推出

$$
a_F\in\mathbf Q.
$$

真正足夠的是：

$$
\boxed{
\sigma(a_F)=a_F
\text{ for every global Galois conjugation}
}
\tag{8.1}
$$

或其他等價地把 minimal polynomial 壓成 degree one 的條件。

---

# 9. Semilinear one-dimensional descent and Hilbert 90

現在考慮更一般的情形。

令

$$
F/\mathbf Q
$$

有限 Galois，$G=\operatorname{Gal}(F/\mathbf Q)$。

令 $L_F$ 為一維 $F$-向量空間，帶 semilinear $G$-action。

取 generator $e$，寫

$$
\sigma(e)
=
c_\sigma e,
\qquad
c_\sigma\in F^\times.
$$

semilinearity與 group law imply

$$
c_{\sigma\tau}
=
\sigma(c_\tau)c_\sigma.
\tag{9.1}
$$

所以

$$
(c_\sigma)
$$

是一個 multiplicative $1$-cocycle。

Hilbert 90 給出：

## Theorem 9.1

存在

$$
u\in F^\times
$$

使

$$
c_\sigma
=
\frac{u}{\sigma(u)}.
$$

因此

$$
e_0:=u^{-1}e
$$

滿足

$$
\sigma(e_0)=e_0.
$$

所以一維 semilinear descent obstruction 在 $H^1(G,F^\times)$ 層級消失。

---

# 10. Hilbert 90 解決的是 descent，不是 absolute normalization

Theorem 9.1 只保證存在 invariant generator。

若

$$
e_0
$$

是 invariant，則任意

$$
q\in\mathbf Q^\times
$$

都令

$$
qe_0
$$

仍 invariant。

所以：

$$
\boxed{
\text{Hilbert 90 kills the cocycle, but leaves a }\mathbf Q^\times\text{ torsor.}
}
\tag{10.1}
$$

這正好符合目前 BSD determinant 問題：

- Galois descent可以建立 rational determinant line / rational generator存在性；
- integral determinant lattice才固定最後的 rational scale。

兩個問題不能合併。

---

# 11. Localized determinant lattice

令 $S$ 為有限 prime set。

定義

$$
R_S
:=
\mathbf Z[S^{-1}].
$$

localized determinant lattice為

$$
D_{R_S}
:=
D_{\mathbf Z}\otimes_{\mathbf Z}R_S.
$$

若

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda
$$

且

$$
\Delta_{\mathrm{cal}}\in D_{R_S},
$$

則

$$
a\in R_S.
$$

這只控制 denominator support。

它並不能排除某個

$$
\ell\notin S
$$

整除 $a$。

---

# 12. Membership 與 primitiveness 必須分開

若

$$
a\in R_S,
$$

則對

$$
\ell\notin S
$$

只有

$$
v_\ell(a)\ge0.
$$

要進一步得到

$$
v_\ell(a)=0,
$$

需要 $\Delta_{\mathrm{cal}}$ 在 $\ell$-adic lattice中 primitive。

也就是：

$$
\Delta_{\mathrm{cal}}
\text{ generates }
D_{\mathbf Z_\ell}.
$$

因此：

$$
\boxed{
\text{integrality controls negative valuations;}
}
$$

$$
\boxed{
\text{primitiveness controls positive valuations.}
}
\tag{12.1}
$$

只有兩者一起才給

$$
v_\ell(a)=0.
$$

---

# 13. $S$-unit criterion

## Theorem 13.1

對 rational determinant

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times,
$$

以下等價：

1. 

$$
a\in R_S^\times;
$$

2. 對所有

$$
\ell\notin S,
$$

有

$$
v_\ell(a)=0;
$$

3. 對所有

$$
\ell\notin S,
$$

localized determinant lattices完全相同：

$$
\mathbf Z_\ell\Delta_{\mathrm{cal}}
=
\mathbf Z_\ell\Delta_\Lambda.
$$

因此：

$$
\boxed{
\text{away-from-}S\text{ local lattice equality}
\iff
a\text{ is an }S\text{-unit}.
}
\tag{13.1}
$$

---

# 14. Relative local length formula

令

$$
L_\ell
=
\mathbf Z_\ell\Delta_\Lambda,
$$

$$
L_\ell'
=
\mathbf Z_\ell\Delta_{\mathrm{cal}}
=
aL_\ell.
$$

令

$$
I_\ell
=
L_\ell\cap L_\ell'.
$$

## Theorem 14.1

$$
\boxed{
v_\ell(a)
=
\operatorname{length}_{\mathbf Z_\ell}
\left(
L_\ell/I_\ell
\right)
-
\operatorname{length}_{\mathbf Z_\ell}
\left(
L_\ell'/I_\ell
\right).
}
\tag{14.1}
$$

## Proof

寫

$$
a=\ell^du
$$

其中

$$
u\in\mathbf Z_\ell^\times.
$$

unit 不改變 lattice，所以只需考慮 $\ell^d$。

若 $d\ge0$，則

$$
L_\ell'\subset L_\ell,
$$

intersection 是 $L_\ell'$，第一個 length 為 $d$，第二個為 $0$。

若 $d<0$，情形反轉，得到負的 length difference。

證畢。

這提供了 lattice defect 的 intrinsic local公式。

---

# 15. Fitting ideal version

若有一個 injective map of free $\mathbf Z_\ell$-modules

$$
\phi_\ell:
M_\ell
\longrightarrow
N_\ell
$$

具有 finite cokernel，且兩者 rank 相同，則 determinant scalar滿足

$$
\boxed{
v_\ell(\det\phi_\ell)
=
\operatorname{length}_{\mathbf Z_\ell}
\operatorname{coker}(\phi_\ell).
}
\tag{15.1}
$$

等價地，

$$
\operatorname{Fitt}_0
(
\operatorname{coker}\phi_\ell
)
=
(\det\phi_\ell).
$$

因此 determinant support可由 comparison map 的 cokernel support控制。

這是把 abstract determinant scale轉成 finite module certificate 的標準方法。

---

# 16. Away-from-$S$ isomorphism theorem

令

$$
\phi:
M_{\mathbf Q}
\longrightarrow
N_{\mathbf Q}
$$

為同 rank rational vector spaces間的 isomorphism。

令

$$
M_{\mathbf Z},
\quad
N_{\mathbf Z}
$$

為 full lattices。

假設對所有

$$
\ell\notin S,
$$

localized map

$$
\phi_\ell:
M_{\mathbf Z_\ell}
\longrightarrow
N_{\mathbf Z_\ell}
$$

是 $\mathbf Z_\ell$-module isomorphism。

則：

## Theorem 16.1

relative determinant scalar

$$
a_\phi
$$

滿足

$$
\boxed{
a_\phi\in\mathbf Z[S^{-1}]^\times.
}
\tag{16.1}
$$

也就是

$$
v_\ell(a_\phi)=0
$$

對所有 $\ell\notin S$。

這是 finite support control 的核心 theorem。

---

# 17. Comparison chain support union theorem

真正 BSD bridge 通常不是單一 map，而是一條 chain：

$$
D_0
\xrightarrow{\phi_1}
D_1
\xrightarrow{\phi_2}
\cdots
\xrightarrow{\phi_m}
D_m.
$$

令每一步的 scalar factor為

$$
a_j.
$$

總 scalar為

$$
a
=
\prod_{j=1}^m a_j.
$$

若第 $j$ 步 away from finite set $S_j$ 是 integral isomorphism，則

$$
a_j
\in
\mathbf Z[S_j^{-1}]^\times.
$$

令

$$
S
=
\bigcup_{j=1}^mS_j.
$$

則：

## Theorem 17.1

$$
\boxed{
a
\in
\mathbf Z[S^{-1}]^\times.
}
\tag{17.1}
$$

因此整个 absolute normalization 的 bad-prime support 至多是各 comparison step bad support 的 union。

---

# 18. Valuation ledger is additive

對每個 prime $\ell$，

$$
d_\ell
:=
v_\ell(a).
$$

由

$$
a=\prod_ja_j,
$$

有

$$
\boxed{
d_\ell
=
\sum_j
v_\ell(a_j).
}
\tag{18.1}
$$

因此可以建立一張 purely symbolic support ledger：

| bridge step | scalar | possible bad-prime set |
|---|---|---|
| BF quotient / projection | $a_1$ | $S_1$ |
| period transport | $a_2$ | $S_2$ |
| Selmer comparison | $a_3$ | $S_3$ |
| Mordell--Weil lattice descent | $a_4$ | $S_4$ |
| height normalization | separate | separate |

總 determinant support只需檢查

$$
S_1\cup S_2\cup S_3\cup S_4.
$$

這讓「所有 primes」問題變成有限 support accounting。

---

# 19. 怎麼安全地選 $S$

本輪不直接宣稱實際 BSD route 的 $S$ 是哪一組 primes。

安全定義是：

$$
\boxed{
S
=
\{\ell:
\text{至少一個 comparison map 在 }\mathbf Z_\ell\text{ 上不是已證 integral isomorphism}\}.
}
\tag{19.1}
$$

然後再由 arithmetic theory把它縮小。

常見候選來源可能包括：

- bad reduction primes；
- chosen $p$；
- auxiliary levels / characters 的 primes；
- projector denominators；
- isogeny degrees；
- Tamagawa / torsion related denominators；
- comparison map 的 explicit denominators。

但除非實際 theorem 證明，不能把這些候選自動等同真正 support。

---

# 20. Finite-prime closure theorem

現在把 Rationality Gate 與 Support Gate 合併。

## Theorem 20.1

假設：

1. rational descent：

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times;
$$

2. finite support：

$$
a\in\mathbf Z[S^{-1}]^\times;
$$

3. 對每個

$$
\ell\in S,
$$

已求得

$$
d_\ell=v_\ell(a).
$$

則

$$
\boxed{
a
=
\pm
\prod_{\ell\in S}
\ell^{d_\ell}.
}
\tag{20.1}
$$

因此 absolute determinant anchor 已被完全閉合到 sign。

---

# 21. Primitive finite-prime closure

若 Theorem 20.1 的設定中進一步有

$$
d_\ell=0
\qquad
\text{for every }\ell\in S,
$$

則：

## Corollary 21.1

$$
\boxed{
a=\pm1.
}
\tag{21.1}
$$

所以

$$
\boxed{
\Delta_{\mathrm{cal}}
=
\pm\Delta_\Lambda.
}
\tag{21.2}
$$

且 quadratic regulator完全相等：

$$
\boxed{
\operatorname{Reg}(\Delta_{\mathrm{cal}})
=
\operatorname{Reg}(\Lambda).
}
\tag{21.3}
$$

這就是 global absolute determinant closure 的 finite-prime certificate 版本。

---

# 22. Regulator ratio theorem

若

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda
$$

且使用同一 height normalization，則

$$
\frac{
\operatorname{Reg}(\Delta_{\mathrm{cal}})
}{
\operatorname{Reg}(\Lambda)
}
=
a^2.
$$

在 Theorem 20.1 下，

$$
\boxed{
\frac{
\operatorname{Reg}(\Delta_{\mathrm{cal}})
}{
\operatorname{Reg}(\Lambda)
}
=
\prod_{\ell\in S}
\ell^{2d_\ell}.
}
\tag{22.1}
$$

所以 finite-prime determinant certificate 同時也是 regulator correction certificate。

---

# 23. Exact square 與 square class 不同

如果知道 exact rational number

$$
R=a^2,
$$

那麼 $a$ 在

$$
\mathbf Q^\times/\{\pm1\}
$$

中被唯一決定。

但如果只知道 $R$ 的 square class

$$
[R]
\in
\mathbf Q^\times/(\mathbf Q^\times)^2,
$$

那麼資訊遠遠不足。

因為任何 rational square都落在 trivial square class。

因此：

$$
\boxed{
\text{exact regulator ratio can determine the determinant class up to sign;}
}
$$

但

$$
\boxed{
\text{regulator square class alone cannot.}
}
\tag{23.1}
$$

這否定了把最後 absolute ambiguity僅僅降成 abstract square-class而不保留 valuations 的做法。

---

# 24. $p$-adic unit class 也不夠

同理，只知道

$$
a\in\mathbf Z_p^\times
$$

只告訴我們

$$
v_p(a)=0.
$$

它不記錄任何 prime-to-$p$ valuation。

所以：

$$
\boxed{
p\text{-adic unit class}
\neq
\text{global }S\text{-unit class}.
}
\tag{24.1}
$$

要 globalize 必須另有 finite support theorem。

---

# 25. Rationality Gate 的三條安全路線

本輪可以把 rational descent 的可接受 route分成三類。

## Route R1: global Galois fixedness

先構造

$$
\Delta_F
\in
D_{\mathbf Q}\otimes F
$$

再證

$$
\sigma(\Delta_F)=\Delta_F.
$$

則直接 descend。

## Route R2: rational functional

構造獨立 rational functional

$$
\lambda\in D_{\mathbf Q}^\ast
$$

並證

$$
\lambda(\Delta_K)\in\mathbf Q.
$$

由一維性推出 rationality。

## Route R3: semilinear descent + absolute rational normalization

先用 Hilbert 90 去掉 Galois cocycle，得到 rational line generator存在性，再用獨立 rational anchor固定剩餘 $\mathbf Q^\times$ scalar。

這三條都比單純的 $p$-adic fixedness強。

---

# 26. Support Gate 的兩條安全路線

## Route S1: local isomorphism

直接證對

$$
\ell\notin S,
$$

所有 comparison maps 都是 integral isomorphism。

則總 determinant scalar是 $S$-unit。

## Route S2: finite cokernel support

對每一步 comparison map證明其 kernel / cokernel只支撐在 $S$，再由 determinant / Fitting ideal公式推出 valuation outside $S$ 為零。

這兩條 route 可以混用。

---

# 27. 一個 abstract BSD finite-certificate template

現在可以把整條 absolute closure寫成：

### Step A: relative BF calibration

得到

$$
\Delta_{\mathrm{cal}}.
$$

### Step B: rational descent

證

$$
\Delta_{\mathrm{cal}}
\in
D_{\mathbf Q}.
$$

### Step C: support theorem

證

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Z[S^{-1}]^\times.
$$

### Step D: local defects

對每個

$$
\ell\in S
$$

求

$$
d_\ell=v_\ell(a).
$$

### Step E: closure

重建

$$
a
=
\pm
\prod_{\ell\in S}
\ell^{d_\ell}.
$$

若全部 $d_\ell=0$，則 determinant primitive。

這是一個真正 finite certificate。

---

# 28. 對目前 $p=11$ BSD 路線的含義

目前 web symbolic line 不需要立刻計算 $S$。

但本地端未來最有效率的任務不應只是：

> 再提高 $11$-adic precision。

更關鍵的是：

1. 找 global rationality mechanism；
2. 找 total comparison chain 的 bad-support union；
3. 證 away-from-$S$ integral isomorphism；
4. 只對有限 $S$ 做 local saturation。

這可能比無限提高單一 $11$-adic computation更接近 absolute closure。

---

# 29. 一個新的 no-go：無限精度也不能替代 global descent

即使知道

$$
a_{11}\in\mathbf Q_{11}
$$

到任意高精度，甚至 exact 地知道一個 $\mathbf Q_{11}$ element，也不會自動證明它來自 $\mathbf Q$。

因此：

## No-Go 29.1

$$
\boxed{
\text{arbitrarily high }11\text{-adic precision cannot by itself replace a global rational descent theorem.}
}
\tag{29.1}
$$

這不是計算能力問題，而是 information type 不同。

---

# 30. 一個新的 no-go：support theorem 不能由有限樣本猜出

即使前若干 primes都觀察到

$$
v_\ell(a)=0,
$$

也不能推出其他 primes一定為零。

finite support必須來自 structural integrality theorem，而不是 prime sampling。

因此：

$$
\boxed{
\text{finite-prime closure 的核心先是 support theorem，再是 local verification。}
}
\tag{30.1}
$$

順序不能顛倒。

---

# 31. 本輪已證

在一維 rational determinant line 的抽象設定下，本輪證明：

1. local Galois fixedness只推出 $\mathbf Q_p$-descent；
2. $\mathbf Q_p$-descent不推出 $\mathbf Q$-descent；
3. projective invariance不推出 scalar rationality；
4. global Galois fixedness推出 rational descent；
5. 一個 rational functional足以測試一維 determinant rationality；
6. Hilbert 90消去 semilinear one-dimensional cocycle，但保留 $\mathbf Q^\times$ torsor；
7. integrality與 primitiveness分別控制 negative / positive valuations；
8. away-from-$S$ local lattice equality等價於 determinant scalar為 $S$-unit；
9. relative local length formula；
10. finite cokernel的 determinant valuation等於 local length；
11. comparison chain 的 total support包含在 individual bad supports 的 union；
12. valuation ledger additive；
13. rationality + $S$-unit + finite local valuations完全決定 absolute determinant class到 sign；
14. exact regulator ratio可決定 rational determinant class到 sign；
15. square class、單一 $p$-adic unit class都不足以替代 full valuation data；
16. arbitrarily high $p$-adic precision不能替代 global descent；
17. finite support不能由有限 prime sampling推出。

---

# 32. 本輪沒有證明

本輪沒有證明：

1. actual BF/Kato calibrated determinant已 global rational；
2. actual global coefficient field與 Galois action已構造；
3. actual rational functional $\lambda$ 已找到；
4. actual comparison chain 在哪些 primes integral；
5. actual finite set $S$；
6. actual local defects $d_\ell$；
7. actual $11$-primary defect；
8. actual prime-to-$11$ saturation；
9. height normalization support；
10. BSD。

---

# 33. 給本地端的最小驗證清單

## V1. Global descent source

找出 calibrated determinant 的 global coefficient object，而不只是一個 $\mathbf Q_{11}$ 數值。

## V2. Galois / rational functional test

至少完成下列之一：

$$
\sigma(\Delta)=\Delta
$$

for all global conjugations，或

$$
\lambda(\Delta)\in\mathbf Q
$$

for an independently normalized rational functional。

## V3. Comparison-chain ledger

列出每一步 determinant comparison map及其 possible bad-support set。

## V4. Away-from-$S$ integrality

證明

$$
\phi_\ell
$$

對所有 $\ell\notin S$ 為 integral isomorphism。

## V5. Local lengths

對

$$
\ell\in S
$$

求 comparison cokernel length或 relative determinant lattice length。

## V6. Reconstruct global scalar

使用

$$
a
=
\pm
\prod_{\ell\in S}
\ell^{d_\ell}.
$$

## V7. Primitive closure

若所有 $d_\ell=0$，則標記 determinant primitive。

## V8. Keep height scale separate

height normalization scalar不可混入 determinant $S$-unit ledger，除非明確記錄它自己的 support與 exponent。

---

# 34. 本輪核心結論

absolute BSD anchor 現在可以被分成兩種不同型態的資訊：

$$
\boxed{
\text{global descent information}
}
$$

與

$$
\boxed{
\text{finite local valuation information}.
}
$$

單一 $p$-adic計算只提供第二類中的一個 local component，無法取代第一類。

若能證：

$$
\Delta_{\mathrm{cal}}
\in D_{\mathbf Q}
$$

以及

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Z[S^{-1}]^\times,
$$

那麼整個 absolute determinant問題就真正變成：

$$
\boxed{
\{v_\ell(a)\}_{\ell\in S}
}
$$

這一組有限整數。

這是目前純符號線到此為止最重要的壓縮：

$$
\boxed{
\text{global BSD absolute normalization}
\rightsquigarrow
\text{global descent theorem}
+
\text{finite-prime certificate}.
}
$$

---

# 35. 下一輪建議

## BSD Symbolic Round 007

**題目：**

> Derived Determinant Complex and Euler-Characteristic Closure

下一步可以不再只把 Mordell--Weil lattice當成單一 rank-$2$ module，而是把 Selmer complex整體放進 determinant formalism。

目標是研究：

1. perfect complex 的 determinant line如何同時編碼 $H^1$、$H^2$、torsion與 finite index；
2. saturation index、Sha、Tamagawa-type finite modules是否可統一成 Euler-characteristic determinant factor；
3. local defect $d_\ell$ 是否能表示成 cohomological length alternating sum；
4. BSD formula中的有限群因子是否其實正是 determinant-complex normalization的一部分；
5. absolute anchor是否能從「Mordell--Weil determinant + 若干 correction」提升成單一 determinant-of-cohomology identity。

如果這條線成立，Round 005--006 的 lattice index ledger可能會被進一步統一成一個 derived Euler-characteristic ledger。
