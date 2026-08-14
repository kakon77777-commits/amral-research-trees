# Collatz Local Affine Atlas：有限奇偶字的精確仿射化
## ——Finite-Word Affine Closure、Count/Order Decomposition 與字序修正

**English Title:** *Collatz Local Affine Atlas: Exact Affine Linearization of Finite Parity Words*

**作者：** Neo.K  
**機構：** 一言諾科技有限公司（EveMissLab）  
**系列：** Collatz Operation Translation Series — Paper 02  
**版本：** v0.1.1  
**日期：** 2026-08-10  
**修訂日期：** 2026-08-14

---

## 摘要

本文建立 Collatz Operation Translation Series 的第一個核心數學層：**有限 parity word 的精確仿射封閉性**。

採用 modified Collatz map

$$
T(n)=
\begin{cases}
\dfrac n2,&n\equiv0\pmod2,\\[2mm]
\dfrac{3n+1}{2},&n\equiv1\pmod2,
\end{cases}
$$

並定義兩個 branch operators

$$
D(x)=\frac x2,
\qquad
U(x)=\frac{3x+1}{2}.
$$

對任意長度 $k$ 的有限字

$$
w=\sigma_1\sigma_2\cdots\sigma_k,
\qquad
\sigma_j\in\{D,U\},
$$

令 $u(w)$ 為 $U$ 的總出現次數。本文證明存在唯一非負整數 $b_w$，使形式 composition 恆可寫為

$$
\boxed{
F_w(x)
=
\frac{3^{u(w)}x+b_w}{2^k}.
}
$$

若 $U$ 出現在位置

$$
1\le j_1<j_2<\cdots<j_u\le k,
$$

則

$$
\boxed{
b_w
=
\sum_{t=1}^{u}
2^{j_t-1}3^{u-t}.
}
$$

因此 finite Collatz word 的全部仿射資訊可精確分解為

$$
\boxed{
(k,u(w))
+
b_w.
}
$$

其中 $(k,u)$ 決定主斜率

$$
\lambda_w=\frac{3^u}{2^k},
$$

而 $b_w$ 保存 branch order 所造成的 affine offset。這提供本文最重要的結構性分解：

$$
\boxed{
\text{counts determine the multiplicative skeleton;}
}
$$

$$
\boxed{
\text{order determines the affine correction.}
}
$$

本文進一步建立遞迴律

$$
b_{wD}=b_w,
$$

$$
\boxed{
b_{wU}=3b_w+2^{|w|},
}
$$

以及字串 composition law。若先執行 $w$ 再執行 $v$，則

$$
\boxed{
b_{wv}
=
3^{u(v)}b_w
+
2^{|w|}b_v.
}
$$

因此三元組

$$
\Omega(w)=(|w|,u(w),b_w)
$$

在 concatenation 下具有精確半直積型結構。

同一結構亦可用 upper-triangular matrices 表示：

$$
M_D=
\begin{pmatrix}
1&0\\
0&2
\end{pmatrix},
\qquad
M_U=
\begin{pmatrix}
3&1\\
0&2
\end{pmatrix},
$$

以及

$$
\boxed{
M_w=
\begin{pmatrix}
3^{u(w)}&b_w\\
0&2^{|w|}
\end{pmatrix}.
}
$$

字的 composition 因此轉化為矩陣乘法。這一表示清楚揭示：標量主乘數 $3^u$ 與分母 $2^k$ 只依賴 branch counts；非交換的字序資訊則集中在右上角 correction term $b_w$。

本文同時嚴格區分兩個層次：

1. **Formal Word Operator**：任意 $w\in\{D,U\}^*$ 均定義一個 $\mathbb Q$ 上的仿射算子；
2. **Admissible Collatz Itinerary**：只有當輸入 $n$ 的實際 parity decisions 與 $w$ 一致時，才有
   $$
   T^k(n)=F_w(n).
   $$

因此 finite-word affine closure 並不等於任意 word 對任意正整數都是合法 Collatz trajectory。這個 domain restriction 將在 Paper 03 被進一步精確化為 parity word 與唯一 residue cylinder modulo $2^k$ 的對應。

本文還證明固定 $(k,u)$ 下，$b_w$ 的極值由字序決定：

$$
\boxed{
3^u-2^u
\le b_w
\le
2^{k-u}(3^u-2^u),
}
$$

其中最小值由

$$
U^uD^{k-u}
$$

取得，最大值由

$$
D^{k-u}U^u
$$

取得。這使「order correction」不只是一個概念，而具有明確可計算的有限範圍。

本文不聲稱 finite affine closure 本身解決 Collatz 猜想。相反地，本文的結論正是：

$$
\boxed{
\text{finite local arithmetic is exactly compressible;}
}
$$

而真正未閉合的問題將轉移到：

$$
\boxed{
\text{which affine chart is admissible at each stage?}
}
$$

亦即後續所稱的 global itinerary problem。

**關鍵詞：** Collatz conjecture、parity word、affine operator、operation translation、correction term、upper-triangular matrix、finite-word closure、local atlas、3n+1

---

# 1. 問題設定

傳統 Collatz map 為

$$
\operatorname{Col}(n)
=
\begin{cases}
n/2,&n\text{ even},\\
3n+1,&n\text{ odd}.
\end{cases}
$$

本文採用等價的 modified form：

$$
\boxed{
T(n)
=
\begin{cases}
n/2,&n\equiv0\pmod2,\\[2mm]
(3n+1)/2,&n\equiv1\pmod2.
\end{cases}
}
$$

之所以採此形式，是因為奇數經 $3n+1$ 後必為偶數，因此可把必然出現的一次除以 2 合併進 odd branch。

定義：

$$
D(x)=\frac{x}{2},
$$

$$
U(x)=\frac{3x+1}{2}.
$$

---

# 2. Formal Word 與 Admissible Itinerary 必須分開

令：

$$
\Sigma=\{D,U\}.
$$

有限字：

$$
w=\sigma_1\cdots\sigma_k
\in\Sigma^k.
$$

本文約定字由左至右執行：

$$
\sigma_1
\to
\sigma_2
\to\cdots\to
\sigma_k.
$$

因此形式算子：

$$
F_w
=
\sigma_k\circ\cdots\circ\sigma_2\circ\sigma_1.
$$

這個算子可以對所有：

$$
x\in\mathbb Q
$$

形式計算。

但對真正 Collatz trajectory，

必須有：

$$
\sigma_j
=
\begin{cases}
D,&T^{j-1}(n)\text{ even},\\
U,&T^{j-1}(n)\text{ odd}.
\end{cases}
$$

才稱 $w$ 對 $n$ **admissible**。

---

# 3. Admissible Domain

定義：

$$
\boxed{
\Omega_w
=
\{
n\in\mathbb Z_{>0}:
\text{the first }|w|
\text{ parity branches of }n
\text{ equal }w
\}.
}
$$

若：

$$
n\in\Omega_w,
$$

則：

$$
\boxed{
T^{|w|}(n)=F_w(n).
}
$$

若：

$$
n\notin\Omega_w,
$$

則 $F_w(n)$ 仍是一個合法有理數算式，

但它不代表 $n$ 的實際 Collatz itinerary。

這正是 Operation Translation 中的：

$$
\boxed{
\text{formal transform legality}
\neq
\text{dynamical-domain legality}.
}
$$

---

# 4. Finite-Word Affine Closure Theorem

## 定理 4.1

對任意：

$$
w\in\{D,U\}^k,
$$

令：

$$
u(w)
=
\#\{j:\sigma_j=U\}.
$$

則存在唯一：

$$
b_w\in\mathbb Z_{\ge0}
$$

使：

$$
\boxed{
F_w(x)
=
\frac{3^{u(w)}x+b_w}{2^k}
}
$$

對所有 $x\in\mathbb Q$ 成立。

---

# 5. 歸納證明

對空字：

$$
\varepsilon,
$$

有：

$$
F_\varepsilon(x)=x.
$$

所以：

$$
k=0,\qquad u=0,\qquad b_\varepsilon=0.
$$

假設長度 $k$ 的 $w$：

$$
F_w(x)
=
\frac{3^ux+b_w}{2^k}.
$$

---

## 5.1 加上一個 $D$

$$
F_{wD}(x)
=
D(F_w(x))
$$

$$
=
\frac{3^ux+b_w}{2^{k+1}}.
$$

所以：

$$
\boxed{
u(wD)=u(w),
}
$$

$$
\boxed{
b_{wD}=b_w.
}
$$

---

## 5.2 加上一個 $U$

$$
F_{wU}(x)
=
U(F_w(x))
$$

$$
=
\frac{
3\frac{3^ux+b_w}{2^k}+1
}{2}
$$

$$
=
\frac{
3^{u+1}x+3b_w+2^k
}{
2^{k+1}
}.
$$

因此：

$$
\boxed{
u(wU)=u(w)+1,
}
$$

$$
\boxed{
b_{wU}=3b_w+2^k.
}
$$

歸納完成。

---

# 6. Correction Recurrence

所以 $b_w$ 可以被看成一個字上的狀態量：

初始：

$$
b_\varepsilon=0.
$$

讀取符號：

$$
D:
\quad
b\mapsto b,
$$

$$
\boxed{
U:
\quad
b\mapsto3b+2^j,
}
$$

其中 $j$ 是加入該符號前的字長。

這不是 numerical error。

它是 exact structural correction。

---

# 7. Closed Form of the Order Correction

假設：

$$
U
$$

出現在位置：

$$
1\le j_1<j_2<\cdots<j_u\le k.
$$

第 $t$ 個 $U$ 在加入時產生：

$$
2^{j_t-1}.
$$

之後每遇到另一個 $U$，

既有 correction 乘以 3。

第 $t$ 個 $U$ 後面共有：

$$
u-t
$$

個 $U$。

因此：

$$
\boxed{
b_w
=
\sum_{t=1}^{u}
2^{j_t-1}3^{u-t}.
}
$$

---

# 8. 例一：$UD$

先：

$$
U(x)=\frac{3x+1}{2}.
$$

再 $D$：

$$
F_{UD}(x)
=
\frac{3x+1}{4}.
$$

所以：

$$
k=2,
\qquad
u=1,
\qquad
b_{UD}=1.
$$

closed form：

$$
j_1=1
$$

給：

$$
b=2^0=1.
$$

---

# 9. 例二：$DU$

先：

$$
D(x)=\frac x2.
$$

再 $U$：

$$
F_{DU}(x)
=
\frac{3x+2}{4}.
$$

所以：

$$
b_{DU}=2.
$$

兩個字：

$$
UD
$$

與：

$$
DU
$$

具有相同：

$$
k=2,\qquad u=1,
$$

因此相同主斜率：

$$
\frac34.
$$

但：

$$
\boxed{
b_{UD}\neq b_{DU}.
}
$$

所以：

$$
\boxed{
\text{branch counts do not determine the full operator}.
}
$$

---

# 10. Count/Order Decomposition

本文定義：

## Multiplicative Skeleton

$$
\boxed{
S(w)
=
(k,u(w)).
}
$$

它決定：

$$
\boxed{
\lambda_w
=
\frac{3^{u(w)}}{2^k}.
}
$$

## Order Correction

$$
\boxed{
C(w)=b_w.
}
$$

因此：

$$
\boxed{
F_w(x)
=
\lambda_wx+\frac{b_w}{2^k}.
}
$$

可讀作：

$$
\boxed{
\text{finite dynamics}
=
\text{order-insensitive multiplicative skeleton}
+
\text{order-sensitive affine correction}.
}
$$

---

# 11. 為什麼這不是普通的「線性化」？

因為：

$$
F_w(x)
$$

本身已是 affine。

本文真正做的是：

$$
\boxed{
\text{many branch-dependent steps}
\longrightarrow
\text{one exact affine operator}.
}
$$

原始流程：

$$
x
\to\sigma_1(x)
\to\sigma_2\sigma_1(x)
\to\cdots
\to F_w(x).
$$

轉譯後：

$$
\boxed{
x
\longmapsto
\frac{3^ux+b_w}{2^k}.
}
$$

這是 finite temporal composition 的 operator compression。

---

# 12. 三元組表示

定義：

$$
\boxed{
\Omega(w)
=
(k_w,u_w,b_w).
}
$$

若先執行：

$$
w
$$

再執行：

$$
v,
$$

則：

$$
F_{wv}
=
F_v\circ F_w.
$$

設：

$$
F_w(x)
=
\frac{3^{u_w}x+b_w}{2^{k_w}},
$$

$$
F_v(x)
=
\frac{3^{u_v}x+b_v}{2^{k_v}}.
$$

代入：

$$
F_v(F_w(x))
=
\frac{
3^{u_v}
\left(
\frac{3^{u_w}x+b_w}{2^{k_w}}
\right)
+b_v
}{
2^{k_v}
}.
$$

整理：

$$
=
\frac{
3^{u_v+u_w}x
+
3^{u_v}b_w
+
2^{k_w}b_v
}{
2^{k_v+k_w}
}.
$$

因此：

$$
\boxed{
\Omega(wv)
=
\left(
k_w+k_v,\,
u_w+u_v,\,
3^{u_v}b_w+2^{k_w}b_v
\right).
}
$$

---

# 13. 半直積型結構

前兩個分量：

$$
k_w+k_v,
$$

$$
u_w+u_v
$$

只做 ordinary addition。

第三分量：

$$
3^{u_v}b_w+2^{k_w}b_v
$$

則受前兩個分量作用。

因此可以把這個結構視作一種：

$$
\boxed{
\text{additive count monoid acting on an affine correction coordinate}.
}
$$

這是 finite parity words 的 operation-translation algebra。

---

# 14. Concatenation Order Defect

交換 $w,v$ 的執行次序。

有：

$$
b_{wv}
=
3^{u_v}b_w+2^{k_w}b_v,
$$

而：

$$
b_{vw}
=
3^{u_w}b_v+2^{k_v}b_w.
$$

所以：

$$
\boxed{
b_{wv}-b_{vw}
=
b_w(3^{u_v}-2^{k_v})
-
b_v(3^{u_w}-2^{k_w}).
}
$$

這是精確的 word-order defect。

注意：

$$
k_w+k_v
$$

與：

$$
u_w+u_v
$$

完全不變。

因此在標量 Collatz finite-word algebra 中：

$$
\boxed{
\text{noncommutativity is confined to the affine correction coordinate}.
}
$$

這個現象將在 Paper 08 與矩陣／非交換 algebra 對比；在真正 noncommutative multiplier 中，order dependence 會進入 leading linear part，而不再只停在 correction。

---

# 15. Upper-Triangular Matrix Representation

對映：

$$
F(x)=\frac{Ax+B}{D}
$$

到：

$$
M(F)
=
\begin{pmatrix}
A&B\\
0&D
\end{pmatrix}.
$$

其 action 為：

$$
x
\mapsto
\frac{Ax+B}{D}.
$$

對 Collatz branches：

$$
\boxed{
M_D
=
\begin{pmatrix}
1&0\\
0&2
\end{pmatrix},
}
$$

$$
\boxed{
M_U
=
\begin{pmatrix}
3&1\\
0&2
\end{pmatrix}.
}
$$

---

# 16. Word Matrix

若：

$$
w=\sigma_1\cdots\sigma_k,
$$

則：

$$
M_w
=
M_{\sigma_k}\cdots M_{\sigma_1}.
$$

由 affine closure：

$$
\boxed{
M_w
=
\begin{pmatrix}
3^{u(w)}&b_w\\
0&2^k
\end{pmatrix}.
}
$$

因此：

$$
\boxed{
\text{word concatenation}
\longrightarrow
\text{matrix multiplication}.
}
$$

---

# 17. Matrix Representation 的意義

這個表示把三種資訊分開：

左上：

$$
3^u
$$

表示 odd-branch multiplicative accumulation。

右下：

$$
2^k
$$

表示總 binary division depth。

右上：

$$
b_w
$$

表示所有 $+1$ injection 經後續 branch scaling 後留下的累積 correction。

因此：

$$
\boxed{
M_w
=
\begin{pmatrix}
\text{odd multiplier}&\text{order correction}\\
0&\text{division scale}
\end{pmatrix}.
}
$$

---

# 18. Correction 的物理式理解不是必要的

可以直觀說：

每次 $U$ 注入一個：

$$
+1
$$

項。

但不同時間注入的 $+1$，

會被後續：

$$
3
$$

multipliers 放大不同次數。

這正是：

$$
2^{j_t-1}3^{u-t}.
$$

出現的原因。

然而本文只把它當作精確代數結果，

不賦予額外物理本體論。

---

# 19. Fixed $(k,u)$ 的 Correction Range

對固定：

$$
k,\qquad u,
$$

不同字只改變：

$$
j_1,\ldots,j_u.
$$

由：

$$
b_w
=
\sum_t2^{j_t-1}3^{u-t},
$$

可以研究 order correction 的極值。

---

# 20. Adjacent Swap Lemma

考慮 word 中相鄰：

$$
UD
$$

與：

$$
DU.
$$

在相同 prefix state $x$ 下：

$$
UD(x)
=
\frac{3x+1}{4},
$$

$$
DU(x)
=
\frac{3x+2}{4}.
$$

所以：

$$
\boxed{
DU(x)-UD(x)=\frac14.
}
$$

若後面再接任意相同 suffix，

其差仍乘上一個正係數。

因此把某個 $U$ 向右越過一個 $D$，

會嚴格增大最終 correction $b_w$。

---

# 21. Order Extremal Theorem

因此對固定：

$$
(k,u),
$$

最小 correction 由所有 $U$ 放最左：

$$
\boxed{
w_{\min}
=
U^uD^{k-u}.
}
$$

最大 correction由所有 $U$ 放最右：

$$
\boxed{
w_{\max}
=
D^{k-u}U^u.
}
$$

---

# 22. 最小 correction

對：

$$
U^uD^{k-u},
$$

$U$ 位置：

$$
j_t=t.
$$

所以：

$$
b_{\min}
=
\sum_{t=1}^u
2^{t-1}3^{u-t}.
$$

利用有限幾何和：

$$
\boxed{
b_{\min}
=
3^u-2^u.
}
$$

---

# 23. 最大 correction

對：

$$
D^{k-u}U^u,
$$

位置：

$$
j_t=k-u+t.
$$

所以：

$$
b_{\max}
=
\sum_{t=1}^u
2^{k-u+t-1}3^{u-t}.
$$

抽出：

$$
2^{k-u},
$$

得到：

$$
\boxed{
b_{\max}
=
2^{k-u}(3^u-2^u).
}
$$

因此：

$$
\boxed{
3^u-2^u
\le
b_w
\le
2^{k-u}(3^u-2^u).
}
$$

---

# 24. 邊界案例

若：

$$
u=0,
$$

則：

$$
w=D^k,
$$

$$
b_w=0.
$$

上式亦給：

$$
3^0-2^0=0.
$$

若：

$$
u=k,
$$

則只有：

$$
w=U^k,
$$

上下界相同：

$$
b_w=3^k-2^k.
$$

例如：

$$
U^3:
$$

$$
b=27-8=19.
$$

因此：

$$
F_{UUU}(x)
=
\frac{27x+19}{8}.
$$

---

# 25. Order Correction Width

固定 $(k,u)$ 的 correction range 寬度：

$$
W_{k,u}
=
b_{\max}-b_{\min}.
$$

所以：

$$
\boxed{
W_{k,u}
=
(2^{k-u}-1)(3^u-2^u).
}
$$

這提供一個有限字次序敏感性的 exact measure。

當：

$$
k=u
$$

時：

$$
W_{k,u}=0
$$

因為只有一種排列。

當同時存在 $D,U$，

通常：

$$
W_{k,u}>0.
$$

---

# 26. Logarithmic Form

若：

$$
x>0,
$$

且：

$$
F_w(x)>0,
$$

則：

$$
\log F_w(x)
=
\log x
+
u\log3
-
k\log2
+
\log\left(
1+\frac{b_w}{3^ux}
\right).
$$

所以：

$$
\boxed{
\Delta_w L
=
u\log3-k\log2
+
C_w(x),
}
$$

其中：

$$
\boxed{
C_w(x)
=
\log\left(
1+\frac{b_w}{3^ux}
\right).
}
$$

---

# 27. Additive Core 與 Correction

因此 Series A 的 corrected linearization：

$$
T\mu=\nu T+C
$$

在 finite Collatz word 中出現一個非常標準的實例。

additive core：

$$
\boxed{
u\log3-k\log2.
}
$$

order-sensitive correction：

$$
\boxed{
C_w(x).
}
$$

且：

$$
C_w(x)\to0
$$

當：

$$
x\to\infty.
$$

所以對固定 word：

$$
\boxed{
\text{asymptotic drift is count-controlled}.
}
$$

這一結論將在 Paper 05 被用來建立 contraction boundary。

---

# 28. 但 Log 不是證明 certificate 的必要形式

因為 affine identity 已經 exact：

$$
F_w(n)
=
\frac{3^un+b_w}{2^k}.
$$

所以 descent 可以直接判斷：

$$
3^un+b_w<2^kn.
$$

因此後續 finite verification 應優先使用 exact integer inequality。

log-space 適合：

- interpretation；
- ordering；
- asymptotic classification；
- heuristic search。

但 exact certificate 不必依賴 floating logarithm。

---

# 29. 與既有 parity-vector 研究的關係

Collatz parity sequence / parity vector 與 $2$-adic 整數之間的一一對應是既有研究的重要部分。

因此本文不主張：

- parity vector 是新發現；
- finite itinerary 可被代數表達是完全未知；
- $2$-adic coding 由本文首次提出。

本文的作用是把 finite-word dynamics 按 Operation Translation 的語言重新整理為：

$$
\boxed{
\text{formal word}
\to
\text{affine operator}
\to
\text{multiplicative skeleton}
+
\text{order correction}.
}
$$

並明確準備後續 local atlas。

---

# 30. 為什麼 Paper 02 還不能直接談 residue bijection？

我們已經知道要使：

$$
F_w(n)
$$

代表真正的：

$$
T^k(n),
$$

必須：

$$
n\in\Omega_w.
$$

但本文尚未證明：

$$
\Omega_w
$$

究竟長什麼樣子。

Paper 03 將證明：

$$
\boxed{
\Omega_w
=
(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}
}
$$

其中 $r_w$ 取模 $2^k$ 的 canonical representative $0\le r_w<2^k$，

且：

$$
\boxed{
r_w
\equiv
-b_w3^{-u}
\pmod{2^k}.
}
$$

這才會把 formal affine operator 升級成 Local Affine Atlas。

---

# 31. 本文不證明什麼？

本文沒有證明：

$$
\forall n,\quad T^j(n)=1
$$

對某個 $j$。

沒有證明所有 infinite parity sequences 最終包含 descending prefix。

沒有證明所有 finite words 都是對所有 $n$ admissible。

沒有從：

$$
u/k
$$

的平均值推出 universal convergence。

本文只證明：

$$
\boxed{
\text{fixed finite word}
\Rightarrow
\text{exact finite affine operator}.
}
$$

---

# 32. 核心定理總結

## Theorem A — Finite-Word Affine Closure

$$
\boxed{
F_w(x)
=
\frac{3^{u(w)}x+b_w}{2^{|w|}}.
}
$$

## Theorem B — Correction Recurrence

$$
\boxed{
b_{wD}=b_w,
\qquad
b_{wU}=3b_w+2^{|w|}.
}
$$

## Theorem C — Closed Form

$$
\boxed{
b_w
=
\sum_{t=1}^{u}
2^{j_t-1}3^{u-t}.
}
$$

## Theorem D — Concatenation

$$
\boxed{
b_{wv}
=
3^{u(v)}b_w+2^{|w|}b_v.
}
$$

## Theorem E — Matrix Representation

$$
\boxed{
M_w
=
\begin{pmatrix}
3^{u(w)}&b_w\\
0&2^{|w|}
\end{pmatrix}.
}
$$

## Theorem F — Order Extremes

$$
\boxed{
3^u-2^u
\le b_w
\le
2^{k-u}(3^u-2^u).
}
$$

---

# 33. 新研究圖像

到這裡，一段長度 $k$ 的 Collatz dynamics 已不必看成：

$$
k
$$

個 if/else operations。

可以壓縮成：

$$
\boxed{
(k,u,b_w).
}
$$

或者：

$$
\boxed{
\begin{pmatrix}
3^u&b_w\\
0&2^k
\end{pmatrix}.
}
$$

因此：

$$
\boxed{
\text{temporal branch sequence}
\longrightarrow
\text{finite algebraic operator}.
}
$$

這就是 Collatz Local Affine Atlas 的 algebraic kernel。

---

# 34. 與 Series A 的銜接

Series A Paper 01：

$$
T(\mu(x,y))
=
\nu(Tx,Ty)+C_T(x,y).
$$

Series A Paper 03：

$$
\text{Linear Core}+\text{Correction}.
$$

Series A Paper 05：

$$
\text{Local Chart / Atlas}.
$$

本篇把三者移植到 Collatz：

$$
\boxed{
\text{finite itinerary}
\to
\text{affine core}
+
\text{word-order correction}.
}
$$

下一篇再把：

$$
\Omega_w
$$

精確識別成 residue cylinder。

---

# 35. 結論

考拉茲猜想的單步規則極為簡單，

但任意有限字的 branch composition 並不需要逐步保存。

它具有 exact affine closure：

$$
\boxed{
F_w(x)
=
\frac{3^ux+b_w}{2^k}.
}
$$

其中：

$$
\boxed{
(k,u)
}
$$

保存 branch-count skeleton，

而：

$$
\boxed{
b_w
}
$$

保存 branch order。

因此：

$$
\boxed{
\text{counts determine slope;}
}
$$

$$
\boxed{
\text{order determines offset.}
}
$$

這是本文最核心的結構性結論。

它同時說明一件更大的事：

Collatz 的有限局部算術其實可以被完整壓縮成低維 algebraic state。

真正困難不必再被描述為：

> 每一步 $3n+1$、除以 2 太亂。

更精確的描述是：

> 對固定有限 itinerary，算術完全可壓縮；未解問題在於每個起點究竟沿著哪些 itinerary 無限延伸，以及這些局部算子如何全域拼接。

Paper 03 將把這個結論再推一步：

$$
\boxed{
\text{parity word}
\longleftrightarrow
\text{unique residue cylinder modulo }2^k,
}
$$

並證明適當 source / destination charts 下：

$$
\boxed{
\psi_w\circ T^k\circ\phi_w^{-1}
=
\operatorname{id}.
}
$$

也就是 Collatz 局部 identity 化。

---

# 參考文獻

1. Olivier Rozier, *Parity sequences of the 3x+1 map on the 2-adic integers and Euclidean embedding*, arXiv:1805.00133.
2. Olivier Rozier, Claude Terracol, *Paradoxical behavior in Collatz sequences*, arXiv:2502.00948.
3. Tong Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, arXiv:2605.13886.
4. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum of Mathematics, Pi 10 (2022), arXiv:1909.03562.
5. David Applegate, Jeffrey C. Lagarias, *The 3x+1 Semigroup*, Journal of Number Theory 117 (2006), arXiv:math/0411140.
6. Tristan Stérin, Damien Woods, *The Collatz process embeds a base conversion algorithm*, arXiv:2007.06979.
7. Collatz Operation Translation Series — Paper 01, *考拉茲猜想既有研究的重新分類與校正*.

---

## 下一篇

**Paper 03 —《Parity Word、Residue Cylinder 與局部 Identity 化》**

核心任務：

1. 證明每個 finite parity word 對應唯一 residue $r_w\bmod2^k$；
2. 證明
   $$
   r_w\equiv-b_w3^{-u}\pmod{2^k};
   $$
3. 建立 exact cylinder map：
   $$
   T^k(r_w+2^ka)=m_w+3^ua;
   $$
4. 定義 source / destination charts；
5. 證明：
   $$
   \psi_wT^k\phi_w^{-1}=\operatorname{id};
   $$
6. 正式建立 Collatz Local Affine Atlas。
