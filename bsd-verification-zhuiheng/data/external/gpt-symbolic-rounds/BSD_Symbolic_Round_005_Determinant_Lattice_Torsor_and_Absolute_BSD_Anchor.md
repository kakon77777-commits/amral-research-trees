# BSD Symbolic Round 005
## Determinant Lattice Torsor and the Absolute BSD Anchor

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** conditional symbolic development；未做新的大型數值計算；未主張 BSD 已證明  
**承接：** BSD Symbolic Round 001--004  
**本輪目標：** 把 calibrated determinant 與 Mordell--Weil / Selmer integral determinant lattice 之間的剩餘 ambiguity 精確化，證明 saturation index、local valuation、height normalization 與 regulator scaling 的關係。

---

# 1. 問題已經轉移

Round 001--004 已經把 common BF normalization 的 relative 問題壓成：

$$
\text{projected class}
\longrightarrow
\text{projective jet}
\longrightarrow
\text{calibrated determinant}.
$$

對 rank-$2$ target，若記 calibrated determinant 為

$$
\Delta_{\mathrm{cal}},
$$

則 common BF gauge 已可藉由 rank-$0$ calibrator 的平方消去。

因此剩下的 absolute 問題不是：

$$
\text{如何求 }C_\pi?
$$

而是：

$$
\boxed{
\Delta_{\mathrm{cal}}
\text{ 在真正 arithmetic determinant lattice 中位於哪裡？}
}
\tag{1.1}
$$

本輪要把這個問題寫成一個一維 lattice torsor problem。

---

# 2. Global determinant lattice

令

$$
\Lambda
=
E(\mathbf Q)/E(\mathbf Q)_{\mathrm{tors}}
$$

為 rank-$2$ Mordell--Weil lattice。

令

$$
H_{\mathbf Q}
=
\Lambda\otimes_{\mathbf Z}\mathbf Q.
$$

定義一維 rational determinant space

$$
D_{\mathbf Q}
:=
\det_{\mathbf Q}H_{\mathbf Q}
=
\bigwedge_{\mathbf Q}^2H_{\mathbf Q}.
\tag{2.1}
$$

integral determinant lattice 為

$$
D_{\mathbf Z}
:=
\det_{\mathbf Z}\Lambda
=
\bigwedge_{\mathbf Z}^2\Lambda
\subset
D_{\mathbf Q}.
\tag{2.2}
$$

因為 $\Lambda$ 是 rank-$2$ free abelian group，所以 $D_{\mathbf Z}$ 是 rank-$1$ free $\mathbf Z$-module。

選一個 basis

$$
P_1,P_2
$$

後，

$$
\Delta_\Lambda
:=
P_1\wedge P_2
$$

生成 $D_{\mathbf Z}$。

換一個 integral basis 只會令

$$
\Delta_\Lambda
\mapsto
\pm\Delta_\Lambda.
$$

因此 integral determinant lattice 本身 canonical，而 generator 只差 sign。

---

# 3. Global determinant torsor

任意非零 rational determinant element

$$
\Delta\in D_{\mathbf Q}^\times
$$

都唯一寫成

$$
\Delta
=
a\,\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times,
\tag{3.1}
$$

一旦選定 orientation。

若不選 orientation，$a$ 只在

$$
\mathbf Q^\times/\{\pm1\}
$$

中有意義。

因此：

## Definition 3.1

absolute determinant class 定義為

$$
\boxed{
[\Delta]_\Lambda
\in
\mathbf Q^\times/\{\pm1\}.
}
\tag{3.2}
$$

這正是 calibrated rational determinant 相對於 arithmetic lattice 的 global torsor coordinate。

---

# 4. Rationality gate

如果

$$
\Delta_{\mathrm{cal}}
$$

只知道屬於

$$
D_{\mathbf Q}\otimes_{\mathbf Q}K
$$

而不知道它是否來自 $D_{\mathbf Q}$，那麼還不能談 rational saturation index。

因此 absolute anchor 的第一個邏輯 gate 是：

$$
\boxed{
\Delta_{\mathrm{cal}}
\in
D_{\mathbf Q}^\times.
}
\tag{4.1}
$$

更一般地，只要能證明

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda
$$

中的 $a$ 落在一個具體 number field 或 rational subfield，也可以開始做 arithmetic denominator analysis。

本輪以下主要討論最乾淨的 rational case

$$
a\in\mathbf Q^\times.
$$

---

# 5. Sublattice determinant theorem

令

$$
\Lambda'
\subset\Lambda
$$

為 rank-$2$ finite-index sublattice。

令

$$
n
:=
[\Lambda:\Lambda'].
$$

選 $\Lambda$ basis $P_1,P_2$，並選 $\Lambda'$ basis $Q_1,Q_2$。

存在

$$
M\in M_2(\mathbf Z)
$$

使

$$
\begin{pmatrix}
Q_1\\
Q_2
\end{pmatrix}
=
M
\begin{pmatrix}
P_1\\
P_2
\end{pmatrix},
$$

且

$$
|\det M|
=
n.
$$

所以：

## Theorem 5.1

$$
\boxed{
Q_1\wedge Q_2
=
\pm n\,
P_1\wedge P_2.
}
\tag{5.1}
$$

即

$$
\boxed{
\det_{\mathbf Z}\Lambda'
=
n\,\det_{\mathbf Z}\Lambda
}
\tag{5.2}
$$

作為 $D_{\mathbf Q}$ 中的 sublattice，忽略 orientation sign。

---

# 6. Saturation index 直接等於 determinant scale

若 calibrated determinant 實際由兩個 rational points

$$
Q_1,Q_2
$$

產生，而

$$
\Lambda'
=
\mathbf ZQ_1+\mathbf ZQ_2
$$

在 $\Lambda$ 中 index 為 $n$，則

$$
\Delta_{\mathrm{cal}}
=
Q_1\wedge Q_2
=
\pm n\Delta_\Lambda.
$$

因此 absolute scalar

$$
a
$$

不是神秘 period constant，而是：

$$
\boxed{
a=\pm[\Lambda:\Lambda'].
}
\tag{6.1}
$$

在這種情形，最後 absolute determinant problem 就是 saturation problem。

---

# 7. Fractional determinant class

更一般地，$\Delta_{\mathrm{cal}}$ 不一定由 integral points 直接生成。

若

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times,
$$

寫

$$
a
=
\pm
\frac{m}{n}
$$

其中

$$
m,n\in\mathbf Z_{>0},
\qquad
\gcd(m,n)=1.
$$

則正 valuation 表示 calibrated determinant 相對 integral lattice 更深，

負 valuation 表示它位於 fractional over-lattice。

因此：

$$
\boxed{
a
\text{ 是一個 fractional saturation coordinate。}
}
\tag{7.1}
$$

若額外證明

$$
\Delta_{\mathrm{cal}}\in D_{\mathbf Z},
$$

則

$$
a\in\mathbf Z.
$$

若再證明 $\Delta_{\mathrm{cal}}$ primitive，則

$$
a=\pm1.
$$

---

# 8. Regulator scaling theorem

令

$$
h:H_{\mathbf Q}\times H_{\mathbf Q}\longrightarrow\mathbf R
$$

或任意 coefficient field中的 symmetric bilinear height pairing。

對

$$
\Delta=P_1\wedge P_2,
$$

定義

$$
\operatorname{Reg}_h(\Delta)
=
\det
\begin{pmatrix}
h(P_1,P_1)&h(P_1,P_2)\\
h(P_2,P_1)&h(P_2,P_2)
\end{pmatrix}.
$$

若

$$
\Delta'=a\Delta,
$$

則：

## Theorem 8.1

$$
\boxed{
\operatorname{Reg}_h(\Delta')
=
a^2
\operatorname{Reg}_h(\Delta).
}
\tag{8.1}
$$

## Proof

若 $\Delta'=a\Delta$，在 determinant line 上 regulator 是 quadratic functional，因此 scalar rescaling平方。亦可由 basis-change determinant formula直接得到。證畢。

---

# 9. Saturation index 的 regulator law

由 Theorem 5.1 與 Theorem 8.1：

## Corollary 9.1

若

$$
\Lambda'\subset\Lambda,
\qquad
[\Lambda:\Lambda']=n,
$$

則

$$
\boxed{
\operatorname{Reg}_h(\Lambda')
=
n^2
\operatorname{Reg}_h(\Lambda).
}
\tag{9.1}
$$

這個平方不是 rank-$2$ 特例。

對任意 rank $r$，若 full-rank sublattice index 是 $n$，Gram determinant仍然乘上

$$
n^2.
$$

也就是：

$$
\boxed{
\text{saturation index 對 regulator 的 exponent 永遠是 }2,
}
\tag{9.2}
$$

與 rank 無關。

---

# 10. 為什麼 index exponent 與 rank 無關

令 rank 為 $r$。

basis-change matrix 為

$$
M\in M_r(\mathbf Z),
$$

且

$$
|\det M|=n.
$$

Gram matrix 變換為

$$
G'
=
M^TGM.
$$

因此

$$
\det G'
=
\det(M)^2\det G
=
n^2\det G.
$$

rank 只改變 matrix size，不改變 index 進入 regulator 的 exponent。

這和 BF gauge 不同。

BF projected class若每一個 basis direction帶 weight one，rank-$r$ determinant的 BF gauge weight是 $r$；

但 lattice index進入 determinant element本身只是一個 scalar $n$，regulator再平方成 $n^2$。

這兩種 exponent 必須分開。

---

# 11. Global regulator map 消去 orientation

global determinant class只定義到

$$
a\sim-a.
$$

但 regulator只看

$$
a^2.
$$

所以 map

$$
\mathbf Q^\times/\{\pm1\}
\longrightarrow
\mathbf Q_{>0},
\qquad
[a]\longmapsto a^2
\tag{11.1}
$$

是 injective，image 是正 rational squares。

因此：

## Theorem 11.1

若

$$
\frac{
\operatorname{Reg}_h(\Delta_{\mathrm{cal}})
}{
\operatorname{Reg}_h(\Lambda)
}
$$

已知為 exact rational number，且確實來自 rational determinant class，則 absolute determinant torsor coordinate由 regulator ratio唯一決定到 sign：

$$
\boxed{
a
=
\pm
\sqrt{
\frac{
\operatorname{Reg}_h(\Delta_{\mathrm{cal}})
}{
\operatorname{Reg}_h(\Lambda)
}
}.
}
\tag{11.2}
$$

因此 sign 不是 classical regulator 的 obstruction。

---

# 12. Local determinant lattices

對每個 prime $\ell$，令

$$
\Lambda_\ell
=
\Lambda\otimes_{\mathbf Z}\mathbf Z_\ell,
$$

$$
H_\ell
=
H_{\mathbf Q}\otimes_{\mathbf Q}\mathbf Q_\ell,
$$

$$
D_\ell
=
\det_{\mathbf Q_\ell}H_\ell.
$$

local determinant lattice 為

$$
D_{\mathbf Z_\ell}
=
\det_{\mathbf Z_\ell}\Lambda_\ell.
$$

任意 generator 可差一個

$$
u_\ell\in\mathbf Z_\ell^\times.
$$

因此 local determinant lattice 只 canonical 地記錄

$$
\mathbf Q_\ell^\times/\mathbf Z_\ell^\times.
$$

標準 valuation 給出

$$
\boxed{
\mathbf Q_\ell^\times/\mathbf Z_\ell^\times
\simeq
\mathbf Z.
}
\tag{12.1}
$$

所以 local lattice class 的真正 invariant 只有 valuation。

---

# 13. Local defect

若 global rational determinant

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times,
$$

定義

$$
d_\ell
:=
v_\ell(a).
\tag{13.1}
$$

則：

- $d_\ell>0$：determinant 在 $\ell$-adic lattice 中過深；
- $d_\ell=0$：local primitive；
- $d_\ell<0$：determinant 具有 $\ell$-adic denominator。

因此：

$$
\boxed{
d_\ell
\text{ 是 absolute determinant 的 local lattice defect。}
}
\tag{13.2}
$$

---

# 14. Prime-to-$p$ saturation invisibility theorem

現在固定 BSD period-calibration 使用的 prime

$$
p=11.
$$

令

$$
\Lambda'\subset\Lambda
$$

index 為

$$
n.
$$

若

$$
p\nmid n,
$$

則 $n$ 在 $\mathbf Z_p$ 中是 unit。

因此：

## Theorem 14.1

若

$$
p\nmid[\Lambda:\Lambda'],
$$

則

$$
\boxed{
\Lambda'\otimes\mathbf Z_p
=
\Lambda\otimes\mathbf Z_p.
}
\tag{14.1}
$$

且

$$
\boxed{
\det\Lambda'_p
=
\det\Lambda_p.
}
\tag{14.2}
$$

作為 $\mathbf Z_p$-lattice。

也就是說：

$$
\boxed{
\text{單一 }p\text{-adic determinant lattice 無法看見 prime-to-}p\text{ saturation index。}
}
\tag{14.3}
$$

這是 absolute BSD anchor 的一個重要限制。

---

# 15. 對目前 $p=11$ 路線的直接含義

即使本地端完全閉合

$$
11\text{-adic determinant comparison},
$$

最多直接確定

$$
v_{11}(a).
$$

它不能僅靠 local lattice position 排除例如

$$
a=2,
\quad
a=3,
\quad
a=5,
\quad
a=7,
$$

因為這些都是 $11$-adic units。

所以：

$$
\boxed{
\text{11-adic primitive}
\not\Rightarrow
\text{globally primitive}.
}
\tag{15.1}
$$

要從 local $p$-adic anchor 升到 global absolute anchor，還需要 rationality 加上 global support control，或其他 primes 的 saturation information。

---

# 16. Global-local reconstruction

若

$$
a\in\mathbf Q^\times,
$$

則

$$
a
=
\pm
\prod_{\ell}
\ell^{v_\ell(a)},
$$

只有有限多個 valuation 非零。

因此：

## Theorem 16.1

global determinant class

$$
[a]_\Lambda
\in
\mathbf Q^\times/\{\pm1\}
$$

由全部 local defects

$$
\{d_\ell\}_\ell
$$

唯一決定。

而 regulator ratio為

$$
\boxed{
a^2
=
\prod_\ell
\ell^{2d_\ell}.
}
\tag{16.1}
$$

所以 absolute anchor 本質上可以被拆成一組 finite-support local valuation data。

---

# 17. Finite-support closure theorem

實際上不需要檢查所有 primes。

假設已由 global arithmetic 證明：

$$
v_\ell(a)=0
\qquad
\text{for all }\ell\notin S,
$$

其中 $S$ 是有限 prime set。

則：

## Theorem 17.1

只要知道

$$
d_\ell=v_\ell(a)
\qquad
(\ell\in S),
$$

就已完全決定 absolute determinant class到 sign：

$$
\boxed{
a
=
\pm
\prod_{\ell\in S}
\ell^{d_\ell}.
}
\tag{17.1}
$$

而 classical regulator ratio完全決定：

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
\tag{17.2}
$$

這把 global anchor 問題轉成有限個 local saturation checks。

---

# 18. Primitive closure criterion

如果能證明：

1. rationality：

$$
\Delta_{\mathrm{cal}}\in D_{\mathbf Q}^\times;
$$

2. integrality：

$$
\Delta_{\mathrm{cal}}\in D_{\mathbf Z};
$$

3. 對所有可能 divisibility primes $\ell$，

$$
d_\ell=0;
$$

則：

## Corollary 18.1

$$
\boxed{
\Delta_{\mathrm{cal}}
=
\pm\Delta_\Lambda.
}
\tag{18.1}
$$

因此

$$
\boxed{
\operatorname{Reg}(\Delta_{\mathrm{cal}})
=
\operatorname{Reg}(\Lambda).
}
\tag{18.2}
$$

這就是 determinant lattice absolute anchor 的最乾淨 closure condition。

---

# 19. Height normalization 是另一個獨立 torsor

到目前為止固定了 height pairing $h$。

若改成

$$
h'
=
u\,h,
\qquad
u\in K^\times,
$$

rank-$2$ Gram matrix 的每個 entry 都乘 $u$，所以：

## Theorem 19.1

$$
\boxed{
\operatorname{Reg}_{h'}(\Lambda)
=
u^2
\operatorname{Reg}_h(\Lambda).
}
\tag{19.1}
$$

因此 absolute BSD scalar comparison至少有兩種不同 normalization：

1. determinant element scale；
2. height pairing scale。

若

$$
\Delta\mapsto a\Delta
$$

同時

$$
h\mapsto uh,
$$

則 rank-$2$ regulator總體變成

$$
\boxed{
\operatorname{Reg}
\mapsto
a^2u^2
\operatorname{Reg}.
}
\tag{19.2}
$$

這兩個 $2$ 的來源不同，不能合併成同一個 gauge。

---

# 20. BF gauge、lattice index、height scale 三者分離

現在可以把目前所有 normalization exponent 分成三層。

### 20.1 BF gauge

每個 projected class帶 common factor $C$。

rank-$2$ determinant：

$$
C^2.
$$

self-paired scalar：

$$
C^4.
$$

### 20.2 Lattice index

determinant element若對 integral lattice差 index $n$：

$$
n.
$$

regulator：

$$
n^2.
$$

### 20.3 Height normalization

若

$$
h\mapsto uh,
$$

rank-$2$ regulator：

$$
u^2.
$$

因此一個 raw scalar可能同時帶

$$
\boxed{
C^4n^2u^2.
}
\tag{20.1}
$$

校準時必須知道每個 exponent 的來源。

---

# 21. 一個 normalization ledger

對 rank-$2$ target，可建立以下符號帳本：

| quantity | BF gauge | lattice scale | height scale |
|---|---:|---:|---:|
| projected class | $1$ | -- | -- |
| determinant class | $2$ | $1$ | -- |
| self-paired regulator scalar | $4$ | $2$ | $2$ |

這張表提供一個快速 sanity check。

如果某個 proposed bridge 把 lattice index寫成四次方，或把 BF common scalar在 determinant level只寫一次，符號 degree 就已不一致。

---

# 22. Isogeny transformation law

令

$$
\varphi:E\longrightarrow E'
$$

為 degree

$$
d
$$

的 isogeny。

在 free Mordell--Weil lattices上，

$$
\varphi(\Lambda_E)
\subset
\Lambda_{E'}.
$$

令

$$
I_\varphi
:=
[\Lambda_{E'}:\varphi(\Lambda_E)].
$$

canonical height滿足

$$
h_{E'}(\varphi P,\varphi Q)
=
d\,h_E(P,Q).
$$

因此 image basis的 Gram determinant乘

$$
d^2.
$$

另一方面 image sublattice相對 $\Lambda_{E'}$ index為 $I_\varphi$，所以 regulator又差

$$
I_\varphi^2.
$$

因此：

## Theorem 22.1

在 rank-$2$ 情形，

$$
\boxed{
\operatorname{Reg}(E')
=
\frac{d^2}{I_\varphi^2}
\operatorname{Reg}(E),
}
\tag{22.1}
$$

只要兩邊使用相容 canonical height normalization。

這說明 isogeny transport 的 absolute regulator correction本質上仍是：

$$
\text{height degree}
+
\text{lattice index}.
$$

---

# 23. 為什麼 local unit 不等於 global irrelevance

在 $p$-adic determinant lattice中，

$$
a
$$

與

$$
ua,
\qquad
u\in\mathbf Z_p^\times,
$$

定義同一 local lattice position。

但如果 $a,u$ 都來自 rational numbers，$u$ 可能含有其他 primes 的 global index information。

例如對 $p=11$，

$$
2,\ 3,\ 5,\ 7
$$

全是 $\mathbf Z_{11}^\times$。

所以：

$$
\boxed{
\text{local unit ambiguity 可能承載 global prime-to-}p\text{ arithmetic information。}
}
\tag{23.1}
$$

不能因為它在 $\mathbf Z_{11}^\times$ 中可逆，就把它在 global BSD normalization 中丟掉。

---

# 24. Rationality + support control 才能把 local data globalize

因此一條安全的 absolute-anchor 路線是：

### Gate A: rationality

證明

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times.
$$

### Gate B: support theorem

證明

$$
v_\ell(a)=0
$$

除了一個有限 set $S$。

### Gate C: local saturation

對每個

$$
\ell\in S
$$

求

$$
d_\ell=v_\ell(a).
$$

### Gate D: primitive closure

若所有

$$
d_\ell=0,
$$

則

$$
a=\pm1.
$$

這四個 gate 合起來才真正固定 global determinant lattice。

---

# 25. 對目前 $389.a1$ 路線的最小符號要求

本輪不計算實際 $S$。

但對目前 target，如果將來 calibrated determinant 已構造，最小 arithmetic questions應該改寫成：

1. 它是否 rational？
2. 它是否 integral？
3. 哪些 primes 可能整除它的 lattice index？
4. $11$-primary defect 是否為零？
5. prime-to-$11$ defects 是否能由其他 global structure 排除？
6. 若不能，是否需要其他 $\ell$-adic comparison或直接 saturation theorem？

這比問「最後那個 period constant是多少」更精確。

---

# 26. 一個重要 no-go statement

假設只知道：

$$
\Delta_{\mathrm{cal},p}
\in
D_{\mathbf Q_p}
$$

相對 local lattice primitive，即

$$
v_p(a)=0.
$$

沒有 rationality theorem，也沒有 global support control。

則不能推出：

$$
a=\pm1.
$$

甚至不能推出 $a$ 是 rational number。

所以：

## Theorem 26.1

$$
\boxed{
\text{單一 }p\text{-adic primitive determinant 本身不足以閉合 global absolute BSD anchor。}
}
\tag{26.1}
$$

必須另有 global descent / rationality / saturation input。

這是本輪最重要的限制之一。

---

# 27. Regulator ratio 可作為 saturation certificate，但不能循環使用

若 classical regulator已經獨立計算並 rigorously fixed，而 calibrated determinant regulator也獨立取得，則

$$
\frac{
\operatorname{Reg}(\Delta_{\mathrm{cal}})
}{
\operatorname{Reg}(\Lambda)
}
=
a^2
$$

可反推出 $a$ 到 sign。

但是若 calibrated determinant本身就是使用 classical regulator定義出來，這個 ratio沒有新的證據價值。

因此必須維持：

$$
\boxed{
\text{determinant construction}
\quad\text{與}\quad
\text{regulator comparison}
}
$$

的來源獨立性。

不能把 regulator ratio拿來定義 determinant scale，再用同一 ratio證明 scale正確。

---

# 28. Absolute anchor 的最小資料結構

現在可把 absolute anchor 壓成三個物件：

$$
\boxed{
(\Delta_{\mathrm{cal}},\ D_{\mathbf Z},\ h).
}
$$

其中：

- $\Delta_{\mathrm{cal}}$：已經去除 common BF gauge 的 determinant element；
- $D_{\mathbf Z}$：Mordell--Weil / Selmer integral determinant lattice；
- $h$：固定 normalization 的 height pairing。

真正需要求的是：

$$
a
\quad\text{such that}\quad
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda.
$$

然後：

$$
\operatorname{Reg}_{\mathrm{cal}}
=
a^2
\operatorname{Reg}_{\Lambda}.
$$

所以 absolute BSD anchor 已縮成一維 arithmetic scale problem。

---

# 29. 本輪已證

在抽象 determinant-lattice 設定下，本輪證明：

1. global determinant torsor為

$$
\mathbf Q^\times/\{\pm1\};
$$

2. full-rank sublattice determinant乘其 index；
3. saturation index $n$ 令 regulator乘 $n^2$；
4. index-square law與 rank 無關；
5. global regulator quadratic map消去 orientation sign；
6. local determinant lattice class只記錄 valuation；
7. prime-to-$p$ saturation對單一 $p$-adic lattice position不可見；
8. global determinant class由全部 local valuations重建；
9. finite-support theorem把 global anchor化成有限 local checks；
10. integrality + local primitiveness推出 absolute determinant generator到 sign；
11. rank-$2$ height rescaling $h\mapsto uh$ 令 regulator乘 $u^2$；
12. BF gauge、lattice scale、height scale有不同 exponent bookkeeping；
13. rank-$2$ isogeny regulator transformation可分解成 degree與 lattice index；
14. 單一 $p$-adic primitive determinant不足以推出 global primitiveness。

---

# 30. 本輪沒有證明

本輪沒有證明：

1. actual calibrated BF/Kato determinant 已 rational；
2. actual determinant 已 integral；
3. actual possible defect prime set $S$；
4. $v_{11}(a)=0$；
5. prime-to-$11$ saturation defects不存在；
6. Mordell--Weil lattice 已 fully saturated；
7. p-adic height normalization 已與 archimedean canonical height normalization比較；
8. actual absolute determinant anchor 已閉合；
9. BSD。

---

# 31. 給本地端的最小驗證清單

## V1. Rationality

檢查 calibrated determinant是否落在

$$
D_{\mathbf Q}.
$$

## V2. Integrality

檢查

$$
\Delta_{\mathrm{cal}}\in D_{\mathbf Z}
$$

或至少找出 denominator support。

## V3. $11$-primary saturation

求

$$
d_{11}=v_{11}(a).
$$

## V4. Support bound

找一個有限 set $S$，證明

$$
v_\ell(a)=0
$$

對所有 $\ell\notin S$。

## V5. Prime-to-$11$ saturation

對

$$
\ell\in S\setminus\{11\}
$$

做獨立 local 或 global saturation check。

## V6. Primitive closure

若所有

$$
d_\ell=0,
$$

標記

$$
a=\pm1.
$$

## V7. Height scale

獨立確認 p-adic / algebraic height normalization factor，不把它混入 lattice index。

## V8. Regulator ratio independence

若使用

$$
a^2
=
\operatorname{Reg}_{\mathrm{cal}}/
\operatorname{Reg}_{\Lambda},
$$

確認 numerator與 denominator來源獨立，避免循環。

---

# 32. 本輪核心結論

absolute BSD anchor現在被壓成：

$$
\boxed{
\text{一個 rank-$1$ determinant lattice torsor。}
}
$$

如果 rationality成立，

$$
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Q^\times,
$$

那麼最後的 arithmetic ambiguity不是任意 transcendental constant，而是：

$$
\boxed{
a
=
\pm
\prod_\ell\ell^{d_\ell}.
}
$$

若 calibrated determinant來自未飽和 sublattice，$a$ 就是 saturation index。

其 regulator effect永遠只是：

$$
\boxed{
a^2.
}
$$

最重要的是：

$$
\boxed{
11\text{-adic closure 只能直接看見 }11\text{-primary defect，不能自動排除 prime-to-}11\text{ saturation。}
}
$$

因此真正的 global absolute closure需要：

$$
\boxed{
\text{rationality}
+
\text{finite support control}
+
\text{local saturation at the remaining primes}.
}
$$

---

# 33. 下一輪建議

## BSD Symbolic Round 006

**題目：**

> Rational Descent, Support Control, and Finite-Prime Closure

下一輪應該研究：

1. 什麼 abstract hypotheses 足以把 a priori $p$-adic calibrated determinant descend 到 rational determinant line；
2. Galois equivariance / comparison-map compatibility如何逼出 rationality；
3. denominator support能否只落在一個有限 explicit set；
4. Tamagawa primes、bad reduction primes、auxiliary primes、$p$ 本身如何進入 support bookkeeping；
5. 若 rationality + $S$-unit property成立，如何把 absolute BSD anchor徹底變成有限 prime certificate；
6. 是否能證明某些 prime defects因 Selmer/Kolyvagin/Kurihara structure 自動為零。

最理想的結論會是：

$$
\boxed{
\Delta_{\mathrm{cal}}
=
a\Delta_\Lambda,
\qquad
a\in\mathbf Z[S^{-1}]^\times,
}
$$

然後 global BSD anchor只剩有限個

$$
v_\ell(a),
\qquad
\ell\in S.
$$
