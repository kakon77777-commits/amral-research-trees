# BSD Symbolic Round 001
## General Cross-Rank Projective Calibration

**日期：** 2026-09-13  
**路線：** 純數學／符號推演  
**狀態：** Conditional symbolic theorem；未做新的大型數值計算；未主張 BSD 已證明  
**對接前線：** `bsd-period-calibration` / PC-001 cross-curve calibration  
**原則：** 本輪只推導可由假設直接得到的代數關係。所有 genuine Beilinson--Flach、Kato、Coleman、period transport 與 regulator 的實際構造，留給本地端計算與獨立驗證。

---

# 1. 目的

目前的 rank-$2$ BSD 校準線中，核心退化關係可抽象寫成

$$
\widehat B_i(t)
=
C_\pi A_i(t)j(t)z_i(t),
$$

其中：

- $i$ 標記不同曲線或不同 arithmetic partner；
- $C_\pi$ 是固定 auxiliary family、Eisenstein quotient 與共同 frame 後出現的共同比較純量；
- $A_i(t)$ 是 partner-dependent、在中心通常非零的顯式因子；
- $j(t)$ 是共同 cyclotomic vanishing factor；
- $z_i(t)$ 是真正承載 arithmetic class 的部分。

PC-001 已展示 rank-$0$ calibrator 與 rank-$2$ target 的一個特例。本輪的目標是把它提升為任意消失階的抽象定理，並回答四個問題：

1. 何時可以完全消去共同純量 $C_\pi$？
2. quotient transport $q_{\mathbf f}$ 在什麼意義下只是 relative calibration 的 gauge？
3. 未知 auxiliary weight 消失階是否真的需要先被求出？
4. rank 不同的 partner 是否仍能形成一致的 calibration network？

---

# 2. 抽象設定

令 $K$ 為特徵零域；在當前應用中可取為有限擴張的 $p$-adic coefficient field。

對每個 index $i$，令 $M_i$ 為有限維 $K$-向量空間，並考慮形式冪級數

$$
\widehat B_i(t),z_i(t)\in M_i[[t]].
$$

假設存在一個與 $i$ 無關的純量

$$
C\in K^\times,
$$

以及

$$
A_i(t)\in K[[t]]^\times,
$$

與共同函數

$$
j(t)\in K[[t]]
$$

使得

$$
\boxed{
\widehat B_i(t)=C\,A_i(t)\,j(t)\,z_i(t).
}
\tag{2.1}
$$

不先假設 $j$ 只有一階零點。令

$$
j(t)=j_e t^e+O(t^{e+1}),
\qquad
j_e\neq 0,
\qquad
e\ge 1.
\tag{2.2}
$$

對每個 $i$，令

$$
z_i(t)=t^{d_i}\kappa_i+O(t^{d_i+1}),
\qquad
\kappa_i\neq 0,
\qquad
d_i\ge 0.
\tag{2.3}
$$

因此預期

$$
\operatorname{ord}_t\widehat B_i=e+d_i.
$$

記

$$
r_i:=e+d_i,
\qquad
B_i^{\mathrm{lead}}
:=
[t^{r_i}]\widehat B_i(t).
\tag{2.4}
$$

---

# 3. General Cross-Rank Leading-Term Lemma

## Lemma 3.1

在假設 (2.1)--(2.3) 下，

$$
\boxed{
B_i^{\mathrm{lead}}
=
C\,A_i(0)\,j_e\,\kappa_i.
}
\tag{3.1}
$$

特別地，

$$
\operatorname{ord}_t\widehat B_i=e+d_i.
\tag{3.2}
$$

## Proof

由

$$
A_i(t)=A_i(0)+O(t),
$$

以及

$$
j(t)=j_e t^e+O(t^{e+1}),
$$

和

$$
z_i(t)=t^{d_i}\kappa_i+O(t^{d_i+1}),
$$

相乘可得

$$
\widehat B_i(t)
=
C
\left(A_i(0)+O(t)\right)
\left(j_e t^e+O(t^{e+1})\right)
\left(t^{d_i}\kappa_i+O(t^{d_i+1})\right).
$$

最低次項唯一來自三個 leading terms，因此

$$
\widehat B_i(t)
=
C\,A_i(0)\,j_e\,
t^{e+d_i}\kappa_i
+
O(t^{e+d_i+1}),
$$

即得 (3.1) 與 (3.2)。證畢。

---

# 4. General Cross-Rank Projective Calibration Theorem

不同曲線的 class 位於不同的 $M_i$ 中，因此不能把兩個 vector 直接相除。正確做法是：只在 calibrator 一側取 scalar observable，而 target 仍保留為 vector。

令 $k$ 為 calibrator index，並取一個 $K$-線性泛函

$$
\lambda_k:M_k\to K
$$

滿足

$$
\lambda_k(\kappa_k)\neq 0.
\tag{4.1}
$$

定義 calibrator observable

$$
b_k
:=
\lambda_k\left(B_k^{\mathrm{lead}}\right).
\tag{4.2}
$$

由 Lemma 3.1，

$$
b_k
=
C\,A_k(0)\,j_e\,\lambda_k(\kappa_k).
\tag{4.3}
$$

因此 $b_k\neq 0$。

## Theorem 4.1

對任意 target $i$，

$$
\boxed{
\kappa_i
=
\frac{A_k(0)\lambda_k(\kappa_k)}
{A_i(0)}
\frac{B_i^{\mathrm{lead}}}{b_k}.
}
\tag{4.4}
$$

這個公式不需要單獨求出 $C$ 或 $j_e$。

## Proof

由 Lemma 3.1，

$$
B_i^{\mathrm{lead}}
=
C\,A_i(0)\,j_e\,\kappa_i.
$$

另一方面，

$$
b_k
=
C\,A_k(0)\,j_e\,\lambda_k(\kappa_k).
$$

因此

$$
\frac{B_i^{\mathrm{lead}}}{b_k}
=
\frac{A_i(0)}
{A_k(0)\lambda_k(\kappa_k)}
\kappa_i.
$$

整理即得 (4.4)。注意這裡只有 vector 除以 coefficient-field scalar；沒有跨不同 cohomology space 直接做 vector quotient。證畢。

---

# 5. PC-001 是 Theorem 4.1 的特例

在目前 BSD period calibration 的設定中，

$$
j(t)=\frac{\log(1+t)}{\log_{11}(12)}
=
\frac{1}{L}t+O(t^2),
$$

所以

$$
e=1,
\qquad
j_1=\frac1L.
$$

對 rank-$0$ calibrator $E_0$，

$$
d_0=0,
$$

故

$$
r_0=1.
$$

對 rank-$2$ target $E$，目前退化形式為

$$
z_E(t)=t\kappa_E+O(t^2),
$$

所以

$$
d_E=1,
\qquad
r_E=2.
$$

令

$$
B_{E,2}
=
[t^2]\widehat B_E(t),
$$

並令

$$
r_{0,1}
=
[t]\operatorname{Col}_0\left(\widehat B_0(t)\right).
$$

若

$$
\ell_0
=
\operatorname{Col}_0(z_0)(0)
=
\operatorname{Col}_0(\kappa_0),
$$

則 Theorem 4.1 直接給出

$$
\boxed{
\kappa_E
=
\frac{A_0(0)\ell_0}{A_E(0)}
\frac{B_{E,2}}{r_{0,1}}.
}
\tag{5.1}
$$

因此 PC-001 的 rank-$0\to2$ 公式不是孤立技巧，而是一般 cross-rank leading-term elimination 的第一個實例。

---

# 6. Projective interpretation：共同純量形成一個 gauge orbit

考慮同一 auxiliary setup 下的全部 leading data

$$
\left\{
B_i^{\mathrm{lead}}
\right\}_{i\in I}.
$$

由 Lemma 3.1，

$$
B_i^{\mathrm{lead}}
=
C\,
\left(A_i(0)j_e\kappa_i\right).
$$

若把共同 normalization 改成

$$
C\mapsto uC,
\qquad
u\in K^\times,
$$

則所有 leading classes 同時變為

$$
B_i^{\mathrm{lead}}
\mapsto
uB_i^{\mathrm{lead}}.
$$

因此 relative calibration 所真正看見的是共同 $K^\times$ 作用下的 orbit，而不是某一個指定的 absolute lift。

換句話說，relative data 自然生活在

$$
\left(
\prod_{i\in I} M_i^\times
\right)
/K^\times_{\mathrm{diag}},
\tag{6.1}
$$

其中 $K^\times_{\mathrm{diag}}$ 對每個 component 同時作同一倍數作用。

這給出一個精確的語言：

> 在只研究 cross-curve relative calibration 時，共同比較純量 $C$ 是 gauge parameter。

但這個結論有一個重要限制：

> 這不代表 $C$ 在 absolute BSD normalization 中必然無意義。

若最後必須把 $p$-adic class 與一個固定的 archimedean regulator、Neron period 或絕對 determinant trivialization 比較，那麼某個 absolute normalization 仍必須被固定。

因此本輪只得到：

$$
\boxed{
\text{relative calibration eliminates }C;
\quad
\text{absolute BSD may still require one absolute anchor.}
}
\tag{6.2}
$$

---

# 7. quotient transport $q_{\mathbf f}$ 的正確地位

假設較早的 full regulator 座標中出現

$$
R_i^{\mathrm{lead}}
=
q_{\mathbf f}\,
\frac{\operatorname{Col}_i(\widehat B_i)}{j},
$$

而

$$
C_\pi
=
\frac{c_{\mathrm{lead}}}{q_{\mathbf f}}.
$$

若同一 auxiliary family 與同一 Eisenstein quotient transport 被用於所有 partner，則 $q_{\mathbf f}$ 對所有 $i$ 是共同的。

此時任何只依賴兩個 consistently projected observables 的比值都會消去 $q_{\mathbf f}$。

例如若

$$
\rho_i
=
q_{\mathbf f}X_i,
\qquad
\rho_k
=
q_{\mathbf f}X_k,
$$

則

$$
\frac{\rho_i}{\rho_k}
=
\frac{X_i}{X_k}.
$$

因此：

$$
\boxed{
q_{\mathbf f}
\text{ 對 relative projected calibration 是 gauge-invisible。}
}
\tag{7.1}
$$

但不能因此推出

$$
q_{\mathbf f}=1.
$$

也不能推出它對 absolute comparison 不重要。

這正是「不需要算它」與「它等於 $1$」之間的差別。

---

# 8. auxiliary weight coordinate 的未知消失階

令 auxiliary weight variable 為 $X$，並假設共同 auxiliary factor 有

$$
c_{\mathbf f}(X)
=
c_nX^n+O(X^{n+1}),
\qquad
c_n\neq 0.
$$

考慮新的局部座標

$$
X'
=
sX+O(X^2),
\qquad
s\in K^\times.
$$

則

$$
X
=
s^{-1}X'+O(X'^2),
$$

所以

$$
c_{\mathbf f}
=
c_n s^{-n}X'^n+O(X'^{n+1}).
$$

leading coefficient 因而變成

$$
c_n'
=
s^{-n}c_n.
$$

只要所有 partner 使用同一 auxiliary family，這個 $s^{-n}$ 對全部 partner 是共同因子，因此在 cross-curve ratio 中消去。

故對 relative calibration 而言，不需要先知道 $n$ 的數值；真正需要的是：

$$
\boxed{
\text{所有 partner 確實共享同一個 auxiliary leading order }n.
}
\tag{8.1}
$$

這比「先證明 $n=1$」弱，也更符合目前資料。

---

# 9. cyclotomic coordinate 的情況不同

對 cyclotomic variable $t$，若改座標為

$$
t'
=
ut+O(t^2),
\qquad
u\in K^\times,
$$

則一個 $t^m$ 的 leading coefficient會帶上 $u^{-m}$。

由於不同 rank 的 partner 有不同的

$$
r_i=e+d_i,
$$

因此 cross-rank leading coefficients在 $t$ 重參數化下不會全部乘上相同次方。

這表示：

> auxiliary weight coordinate $X$ 的共同 reparametrization 可以在 ratio 中自動消去；但 cyclotomic coordinate $t$ 的 normalization 必須固定，或在公式中保留其 rank-dependent transformation law。

因此 Theorem 4.1 是在固定共同 cyclotomic coordinate 下成立的 calibration theorem。

這一點不能和 $X$-coordinate 的 gauge cancellation 混為一談。

---

# 10. Multi-calibrator consistency theorem

假設有兩個 calibrators $a,b$，各自具有非零泛函

$$
\lambda_a:M_a\to K,
\qquad
\lambda_b:M_b\to K,
$$

並定義

$$
b_a
=
\lambda_a(B_a^{\mathrm{lead}}),
\qquad
b_b
=
\lambda_b(B_b^{\mathrm{lead}}).
$$

由 (4.3)，

$$
\frac{b_a}
{A_a(0)\lambda_a(\kappa_a)}
=
Cj_e,
$$

以及

$$
\frac{b_b}
{A_b(0)\lambda_b(\kappa_b)}
=
Cj_e.
$$

所以必有：

## Theorem 10.1

$$
\boxed{
\frac{b_a}
{A_a(0)\lambda_a(\kappa_a)}
=
\frac{b_b}
{A_b(0)\lambda_b(\kappa_b)}.
}
\tag{10.1}
$$

這是一個非常適合交給本地端做獨立驗證的 consistency identity。

它的價值在於：即使不求 $C$，兩個 calibrators 也必須回推出同一個共同 product

$$
Cj_e.
$$

若未來取得多個 rank-$0$ 或 rank-$1$ calibrator，則可以形成 calibration network，而不是只依賴單一 partner。

---

# 11. Calibration cocycle

若每個 partner $i$ 都有 scalar observable

$$
b_i
=
\lambda_i(B_i^{\mathrm{lead}})
$$

與

$$
k_i
=
\lambda_i(\kappa_i)\neq 0,
$$

則

$$
b_i
=
C A_i(0)j_e k_i.
$$

定義從 $k$ 到 $i$ 的 relative calibration factor

$$
\Gamma_{i\leftarrow k}
:=
\frac{A_k(0)}{A_i(0)}
\frac{b_i}{b_k}.
$$

則

$$
\Gamma_{i\leftarrow k}
=
\frac{k_i}{k_k}.
$$

因此對任意 $i,j,k$，

$$
\boxed{
\Gamma_{i\leftarrow j}
\Gamma_{j\leftarrow k}
=
\Gamma_{i\leftarrow k}.
}
\tag{11.1}
$$

以及

$$
\boxed{
\Gamma_{i\leftarrow k}^{-1}
=
\Gamma_{k\leftarrow i}.
}
\tag{11.2}
$$

這使 calibration data 自然形成一個乘法 cocycle / groupoid-like structure。

對實驗而言，這表示三條曲線可以形成閉合三角：

$$
\Gamma_{i\leftarrow j}
\Gamma_{j\leftarrow k}
\Gamma_{k\leftarrow i}
=
1.
\tag{11.3}
$$

若本地端未來真的構造出三個 genuine projected BF observables，(11.3) 是一個不需要知道 $C$ 的強一致性測試。

---

# 12. Determinant-line extension

Theorem 4.1 並不要求 $M_i$ 是普通 cohomology coordinate space。

它只要求：

1. $M_i$ 是 $K$-向量空間；
2. leading factorization (2.1) 成立；
3. calibrator 有一個非零 scalar functional。

因此可以直接把

$$
M_E
$$

換成某個 determinant line，例如

$$
M_E
=
\det H^1_{\mathrm{Sel}}(E)
$$

或更具體地在 rank-$2$ 情形考慮

$$
M_E
=
\bigwedge^2 H^1_{\mathrm{Sel}}(E).
$$

若將來能建立 genuine arithmetic factorization

$$
\widehat\Delta_E(t)
=
C\,A_E(t)\,j(t)\,\Delta_E(t),
$$

其中 leading term

$$
\Delta_E(0)
$$

經 regulator map 送到

$$
\operatorname{Reg}_p(E),
$$

那麼同一套 cross-rank calibration theorem 可以直接作用於 determinant-line element，而不必先把 rank-$2$ 問題壓成某個單一向量座標。

這是下一輪值得優先研究的方向。

目前只能得到條件式結論：

$$
\boxed{
\text{若 BF/Kato leading class 可自然提升到 determinant line，}
\\
\text{則 relative calibration 機制原封不動保留。}
}
\tag{12.1}
$$

本輪沒有構造這個 determinant lift。

---

# 13. 本輪已證與未證

## 13.1 純符號上已證

在假設 (2.1)--(2.3) 下：

1. 任意 rank / 任意消失階的 leading coefficient 公式 (3.1)；
2. cross-rank calibrator elimination 公式 (4.4)；
3. PC-001 rank-$0\to2$ 公式是一般定理的特例；
4. 共同 $K^\times$ normalization 在 relative calibration 中消去；
5. 共同 quotient transport $q_{\mathbf f}$ 在 relative projected ratio 中消去；
6. auxiliary weight coordinate 的共同 leading rescaling 在 ratio 中消去；
7. multi-calibrator consistency identity (10.1)；
8. calibration cocycle identities (11.1)--(11.3)。

## 13.2 尚未證

本輪沒有證明：

1. 真實 Beilinson--Flach family 必然滿足 (2.1)；
2. 所有 partner 的 quotient transport 確實完全相同；
3. modular-symbol period 已與 Kato / Coleman / adjoint period 完全對齊；
4. genuine $B_{E,2}$ 已被構造；
5. genuine $r_{0,1}$ 已被構造；
6. $q_{\mathbf f}=1$；
7. absolute comparison scalar 不再需要；
8. determinant-line lift 已存在；
9. $p$-adic determinant 已與 archimedean regulator 比較；
10. BSD 猜想已被證明。

---

# 14. 給本地端的 oracle / verification checklist

本輪不計算，但若要驗證此路線，最小輸入可以壓成：

### O1. Common-factorization oracle

驗證至少兩個 partner 的 genuine projected BF objects 是否真的具有

$$
\widehat B_i
=
C A_i j z_i
$$

且 $C$ 為共同純量。

### O2. Leading-order oracle

獨立求

$$
\operatorname{ord}_t z_i=d_i
$$

與

$$
\operatorname{ord}_t\widehat B_i=e+d_i.
$$

### O3. Calibrator nonvanishing oracle

驗證

$$
\lambda_k(\kappa_k)\neq 0
$$

與

$$
b_k\neq 0.
$$

### O4. Period-transport oracle

確認 modular-symbol、Kato、Coleman、adjoint normalization 的 transport 沒有留下 partner-dependent unknown scalar。

### O5. Multi-calibrator consistency oracle

若有兩個 calibrator，測試

$$
\frac{b_a}
{A_a(0)\lambda_a(\kappa_a)}
=
\frac{b_b}
{A_b(0)\lambda_b(\kappa_b)}.
$$

### O6. Triangle oracle

若有三個 partner，測試

$$
\Gamma_{i\leftarrow j}
\Gamma_{j\leftarrow k}
\Gamma_{k\leftarrow i}
=
1.
$$

### O7. Absolute-anchor oracle

若目標是完整 BSD，而非 relative calibration，必須找出至少一個 absolute normalization anchor，使共同 $K^\times$ torsor 被真正固定。

---

# 15. 本輪核心結論

本輪最重要的觀念可以壓成一句：

$$
\boxed{
\text{BSD period calibration 的 relative 問題，
本質上不是求未知共同常數，
而是對共同 }K^\times\text{ gauge 取商。}
}
$$

在這個 quotient 之後，rank-$0$、rank-$1$、rank-$2$ 甚至更高消失階的 partner 都可以放進同一個 leading-term calibration network。

真正沒有被 relative quotient 消掉的，是：

$$
\boxed{
\text{partner-dependent arithmetic class、
period compatibility、
以及最後的 absolute BSD anchor。}
}
$$

因此下一步不應優先花力氣單獨計算 $C_\pi$ 或強迫 $q_{\mathbf f}=1$；更自然的方向是：

$$
\boxed{
\text{把 genuine BF/Kato leading data 推入 determinant line，
再研究 absolute anchor 如何固定最後一個 }K^\times\text{ 自由度。}
}
$$

---

# 16. 下一輪建議

**BSD Symbolic Round 002**

建議題目：

> **Determinant-Line Lift of Rank-2 Calibration**

目標不是計算 regulator，而是純符號回答：

1. rank-$2$ Selmer data 的自然 determinant object 應該是什麼；
2. BF/Kato leading class 需要哪一種 exterior / derived construction 才能進入該 line；
3. height pairing 如何在 determinant line 上變成單一 scalar morphism；
4. 哪些 normalization 在 determinant level 會自動消去；
5. 哪一個剩餘 scalar 才是真正的 absolute BSD obstruction。

