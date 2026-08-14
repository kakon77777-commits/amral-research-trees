# Valuation Language 與 Accelerated Collatz
## ——從奇偶字的 Run-Length Encoding、$v_2$ 精確漂移到 Valuation-Order Correction

**English Title:** *Valuation Language and the Accelerated Collatz Map: Exact $v_2$ Drift, Run-Length Encoding, and Valuation-Order Corrections*

**作者：** Neo.K  
**機構：** 一言諾科技有限公司（EveMissLab）  
**系列：** Collatz Operation Translation Series — Paper 06  
**版本：** v0.1  
**日期：** 2026-08-10

---

## 摘要

作者早期的 Collatz 系統論研究曾以「$2$ 的指數收縮最終壓過 $3$ 的放大」描述考拉茲軌跡的平均下降直覺。其主要問題在於：平均 $2$-進除法深度、負對數漂移與耗散類比只能提供統計／啟發式理由，不能排除 exceptional orbit，因此不能直接提升為 Collatz 全域證明。

本文利用前五篇建立的 finite-word affine atlas，把這條舊 heuristic 重新表述為一個精確的 **valuation language**。

對 positive odd integer $n$，定義：

$$
\boxed{
\kappa(n)=v_2(3n+1)\ge1
}
$$

以及 accelerated odd Collatz map：

$$
\boxed{
S(n)
=
\frac{3n+1}{2^{\kappa(n)}}.
}
$$

則：

$$
S(n)
$$

再次為 positive odd integer。

對一段長度 $m$ 的 odd-to-odd orbit：

$$
n_0
\to n_1
\to\cdots
\to n_m,
$$

定義 exact valuation word：

$$
\boxed{
\boldsymbol\kappa
=
(\kappa_1,\ldots,\kappa_m),
\qquad
\kappa_i=v_2(3n_{i-1}+1).
}
$$

以及 cumulative valuation：

$$
K_j=\sum_{i=1}^j\kappa_i,
\qquad
K_0=0,
$$

$$
K=K_m.
$$

本文證明：

$$
\boxed{
S^m(n_0)
=
\frac{
3^m n_0+B_{\boldsymbol\kappa}
}{
2^K
},
}
$$

其中：

$$
\boxed{
B_{\boldsymbol\kappa}
=
\sum_{i=1}^{m}
3^{m-i}2^{K_{i-1}}.
}
$$

所以 accelerated odd dynamics 再次具有：

$$
\boxed{
\text{multiplicative skeleton}
+
\text{order correction}.
}
$$

主 skeleton 只看：

$$
(m,K),
$$

而 valuation 的局部排列透過 prefix sums：

$$
K_{i-1}
$$

進入：

$$
B_{\boldsymbol\kappa}.
$$

因此 exact log drift 為：

$$
\boxed{
\ln\frac{S^m(n_0)}{n_0}
=
m\ln3
-
K\ln2
+
\ln\left(
1+\frac{B_{\boldsymbol\kappa}}{3^m n_0}
\right).
}
$$

這使舊「$2$ 的指數戰勝 $3$」得到精確版本：

$$
\boxed{
2^K>3^m
\iff
\frac Km>\log_2 3
}
$$

是 fixed valuation word 落在 contracting-skeleton side 的充要條件；若成立，存在 exact finite threshold：

$$
\boxed{
n_0>
\frac{
B_{\boldsymbol\kappa}
}{
2^K-3^m
}
}
$$

即可保證：

$$
S^m(n_0)<n_0.
$$

若：

$$
2^K<3^m,
$$

則：

$$
S^m(n_0)>n_0
$$

對該 fixed valuation itinerary 上所有 positive admissible inputs 成立。

本文同時證明 valuation language 與 modified-map parity language 之間具有自然 run-length correspondence。一次 odd-to-odd cycle：

$$
\kappa_i
$$

對應 modified parity block：

$$
\boxed{
UD^{\kappa_i-1}.
}
$$

因此一段 valuation word對應：

$$
\boxed{
UD^{\kappa_1-1}
UD^{\kappa_2-1}
\cdots
UD^{\kappa_m-1},
}
$$

其總 modified-map step length正是：

$$
K=\sum_i\kappa_i,
$$

而 $U$ 次數為：

$$
m.
$$

所以 Paper 05 的有限字收縮邊界：

$$
\frac{u}{k}<\frac{\ln2}{\ln3}
$$

在 valuation language 中精確等價為：

$$
\boxed{
\frac Km>\frac{\ln3}{\ln2}
=
\log_2 3.
}
$$

本文再證明一個單步 valuation-density law：對任意 $j\ge1$，在 positive odd integers 的自然密度意義下，

$$
\boxed{
\Pr_{\mathrm{res}}\bigl(v_2(3n+1)=j\bigr)
=
2^{-j}.
}
$$

更精確地說，在模 $2^{j+1}$ 的 $2^j$ 個 odd residue classes 中，恰有一個 residue class 滿足：

$$
v_2(3n+1)=j.
$$

因此：

$$
\boxed{
\sum_{j\ge1}j\,2^{-j}=2.
}
$$

即「平均 valuation 為 2」可被提升為一條 exact residue-density statement。

但本文特別強調：

$$
\boxed{
\text{one-step residue density}
\neq
\text{independent valuation process along an orbit}.
}
$$

所以：

$$
\ln3-2\ln2=\ln(3/4)<0
$$

只能描述 residue ensemble 的 skeleton mean drift；它本身仍不能推出每一條 orbit 收斂。Tao 對 Syracuse iteration 的 almost-all 結果使用遠比「獨立幾何分布」更強的 approximate-transport、renewal process 與 $3$-adic random-walk machinery，也正顯示此量詞鴻溝是真實存在的。

本文還證明 valuation order 對 correction 的精確影響。若 valuation word 中相鄰兩項：

$$
a,b
$$

互換，其餘不變，且該位置前 cumulative valuation 為 $P$，則 correction difference 為：

$$
\boxed{
B_{(\ldots,a,b,\ldots)}
-
B_{(\ldots,b,a,\ldots)}
=
3^{m-i-1}2^P(2^a-2^b).
}
$$

所以：

$$
a>b
$$

時，較大的 valuation 放在較前位置會提高 affine correction。對固定 valuation multiset：

$$
\boxed{
\text{ascending valuation order minimizes }B_{\boldsymbol\kappa},
}
$$

$$
\boxed{
\text{descending valuation order maximizes }B_{\boldsymbol\kappa}.
}
$$

這是 accelerated setting 中「counts determine drift; order determines finite correction」的精確版本。

最後，本文重新統一 inverse fibers。對 odd target $t$ 與 valuation $\kappa$：

$$
\boxed{
R_\kappa(t)
=
\frac{2^\kappa t-1}{3},
}
$$

只要：

$$
2^\kappa t\equiv1\pmod3
$$

就是合法 odd predecessor。對一個 reverse-admissible valuation word與 terminal odd state $t=n_m$，可精確還原：

$$
\boxed{
n_0
=
\frac{
2^K t-B_{\boldsymbol\kappa}
}{
3^m
}.
}
$$

因此 valuation language 同時支援 forward compression 與 exact inverse recovery。

本文不宣稱 valuation language 解決 Collatz 猜想。它完成的是更精確的工作：

$$
\boxed{
\text{舊的平均負漂移直覺}
\longrightarrow
\text{exact finite valuation-word drift}
+
\text{separate statistical layer}.
}
$$

**關鍵詞：** Collatz conjecture、accelerated Collatz、Syracuse map、$2$-adic valuation、valuation word、parity vector、log drift、inverse fiber、operation translation、exact recovery

---

# 1. 為什麼需要 Valuation Language？

在 modified Collatz map：

$$
T(n)
=
\begin{cases}
n/2,&n\text{ even},\\
(3n+1)/2,&n\text{ odd},
\end{cases}
$$

一個 odd state 經 $U$ 後，

可能需要：

$$
0,1,2,\ldots
$$

個額外 $D$ 才回到下一個 odd state。

例如：

$$
n\text{ odd},
$$

若：

$$
v_2(3n+1)=4,
$$

則 modified parity segment 是：

$$
\boxed{
UDDD.
}
$$

所以完整 parity word 對 odd-to-odd dynamics 存在大量重複的 $D$ runs。

valuation language 的目的就是把這些 run 無損壓縮。

---

# 2. Accelerated Odd Map

令：

$$
\mathcal O
=
\{1,3,5,\ldots\}.
$$

對：

$$
n\in\mathcal O,
$$

定義：

$$
\boxed{
\kappa(n)
=
v_2(3n+1).
}
$$

因 odd $n$：

$$
3n+1
$$

必 even，

所以：

$$
\kappa(n)\ge1.
$$

再定義：

$$
\boxed{
S(n)
=
\frac{3n+1}{2^{\kappa(n)}}.
}
$$

因已除掉全部 factor of 2，

所以：

$$
S(n)\in\mathcal O.
$$

因此：

$$
\boxed{
S:\mathcal O\to\mathcal O.
}
$$

---

# 3. Valuation Word

給定 actual odd orbit：

$$
n_0
\xrightarrow{S}
n_1
\xrightarrow{S}
\cdots
\xrightarrow{S}
n_m,
$$

定義：

$$
\boxed{
\kappa_i
=
v_2(3n_{i-1}+1).
}
$$

valuation word：

$$
\boxed{
\boldsymbol\kappa
=
(\kappa_1,\ldots,\kappa_m)
\in\mathbb Z_{\ge1}^m.
}
$$

---

# 4. Formal Valuation Word 與 Admissible Valuation Word

任意：

$$
(\kappa_1,\ldots,\kappa_m)
\in\mathbb Z_{\ge1}^m
$$

可以作為形式符號。

但只有當存在：

$$
n_0\in\mathcal O
$$

使：

$$
v_2(3n_{i-1}+1)=\kappa_i
$$

逐步成立時，

才稱其為對 $n_0$ 的 admissible valuation word。

所以再次需要：

$$
\boxed{
\text{formal language}
\neq
\text{dynamical legality}.
}
$$

---

# 5. Run-Length Expansion

對一個 valuation symbol：

$$
\kappa\ge1,
$$

定義其 modified parity expansion：

$$
\boxed{
E(\kappa)
=
UD^{\kappa-1}.
}
$$

例如：

$$
E(1)=U,
$$

$$
E(2)=UD,
$$

$$
E(4)=UDDD.
$$

對整個 valuation word：

$$
\boxed{
E(\boldsymbol\kappa)
=
UD^{\kappa_1-1}
UD^{\kappa_2-1}
\cdots
UD^{\kappa_m-1}.
}
$$

---

# 6. Run-Length Correspondence

對一段實際 odd-to-odd trajectory，

每個：

$$
\kappa_i
$$

恰等於：

> 從第 $i-1$ 個 odd state 到第 $i$ 個 odd state 所經歷的 modified Collatz steps 數。

因為：

- 第一步是 $U$，已除一次 2；
- 再有 $\kappa_i-1$ 次 $D$；
- 然後到下一個 odd state。

因此：

$$
\boxed{
|E(\boldsymbol\kappa)|
=
\sum_{i=1}^m\kappa_i.
}
$$

---

# 7. Cumulative Valuation

定義：

$$
\boxed{
K_j
=
\sum_{i=1}^j\kappa_i,
}
$$

$$
K_0=0.
$$

總 valuation：

$$
\boxed{
K=K_m.
}
$$

在 expanded parity word 中：

$$
\boxed{
k_{\mathrm{parity}}=K,
}
$$

$$
\boxed{
u_{\mathrm{parity}}=m.
}
$$

這建立 Paper 05 與 accelerated setting 的直接橋樑。

---

# 8. One-Cycle Formula

由：

$$
n_i
=
\frac{3n_{i-1}+1}{2^{\kappa_i}},
$$

重寫：

$$
\boxed{
2^{\kappa_i}n_i
=
3n_{i-1}+1.
}
$$

這是 valuation language 的基本 local equation。

---

# 9. Two-Cycle Example

兩步：

$$
n_1
=
\frac{3n_0+1}{2^{\kappa_1}},
$$

$$
n_2
=
\frac{3n_1+1}{2^{\kappa_2}}.
$$

代入：

$$
n_2
=
\frac{
3\frac{3n_0+1}{2^{\kappa_1}}+1
}{
2^{\kappa_2}
}
$$

$$
=
\frac{
9n_0+3+2^{\kappa_1}
}{
2^{\kappa_1+\kappa_2}
}.
$$

所以：

$$
\boxed{
B_{(\kappa_1,\kappa_2)}
=
3+2^{\kappa_1}.
}
$$

已經看出 correction 依賴 valuation order。

---

# 10. Accelerated Affine Closure Theorem

## 定理 10.1

對任意 actual admissible valuation word：

$$
\boldsymbol\kappa
=
(\kappa_1,\ldots,\kappa_m),
$$

有：

$$
\boxed{
S^m(n_0)
=
\frac{
3^mn_0+B_{\boldsymbol\kappa}
}{
2^K
},
}
$$

其中：

$$
\boxed{
B_{\boldsymbol\kappa}
=
\sum_{i=1}^{m}
3^{m-i}2^{K_{i-1}}.
}
$$

---

# 11. 歸納證明

定義：

$$
B_0=0.
$$

假設：

$$
n_{j-1}
=
\frac{
3^{j-1}n_0+B_{j-1}
}{
2^{K_{j-1}}
}.
$$

則：

$$
n_j
=
\frac{3n_{j-1}+1}{2^{\kappa_j}}
$$

$$
=
\frac{
3^j n_0
+
3B_{j-1}
+
2^{K_{j-1}}
}{
2^{K_j}
}.
$$

因此 recurrence：

$$
\boxed{
B_j
=
3B_{j-1}
+
2^{K_{j-1}}.
}
$$

展開即：

$$
\boxed{
B_j
=
\sum_{i=1}^{j}
3^{j-i}2^{K_{i-1}}.
}
$$

證畢。

---

# 12. Valuation Skeleton 與 Correction

定義：

$$
\boxed{
\Sigma(\boldsymbol\kappa)
=
(m,K).
}
$$

它決定 leading multiplier：

$$
\boxed{
\lambda_{\boldsymbol\kappa}
=
\frac{3^m}{2^K}.
}
$$

而：

$$
\boxed{
C(\boldsymbol\kappa)
=
B_{\boldsymbol\kappa}
}
$$

保存 valuation word 的 prefix-order information。

因此：

$$
\boxed{
S^m(n)
=
\lambda_{\boldsymbol\kappa}n
+
\frac{B_{\boldsymbol\kappa}}{2^K}.
}
$$

---

# 13. Counts Determine Drift；Valuation Order Determines Correction

兩個 valuation words 可以具有相同：

$$
m
$$

與：

$$
K,
$$

卻有不同：

$$
B_{\boldsymbol\kappa}.
$$

例如：

$$
(1,3)
$$

與：

$$
(3,1)
$$

都有：

$$
m=2,
\qquad
K=4.
$$

但：

$$
B_{(1,3)}
=
3+2
=
5,
$$

$$
B_{(3,1)}
=
3+8
=
11.
$$

所以：

$$
\boxed{
\text{same drift skeleton}
\not\Rightarrow
\text{same finite operator}.
}
$$

---

# 14. 與 Paper 02 的完全對應

expanded parity word：

$$
E(\boldsymbol\kappa)
$$

有：

$$
k=K,
$$

$$
u=m.
$$

因此 Paper 02：

$$
F_w(n)
=
\frac{3^un+b_w}{2^k}
$$

在 valuation form 中變成：

$$
\boxed{
S^m(n)
=
\frac{
3^mn+B_{\boldsymbol\kappa}
}{
2^K
}.
}
$$

所以：

$$
\boxed{
B_{\boldsymbol\kappa}
=
b_{E(\boldsymbol\kappa)}
}
$$

對實際 odd-to-odd segment 成立。

valuation language 不是另一套動力學，

而是 parity language 的 run-length compressed coordinate。

---

# 15. Exact Log Drift

對：

$$
n_0>0,
$$

有：

$$
S^m(n_0)
=
\frac{
3^mn_0+B_{\boldsymbol\kappa}
}{
2^K
}.
$$

取 log：

$$
\ln S^m(n_0)
=
m\ln3
-
K\ln2
+
\ln n_0
+
\ln\left(
1+
\frac{
B_{\boldsymbol\kappa}
}{
3^m n_0
}
\right).
$$

所以：

$$
\boxed{
\Delta_{\boldsymbol\kappa}L
=
m\ln3
-
K\ln2
+
C_{\boldsymbol\kappa}(n_0),
}
$$

其中：

$$
\boxed{
C_{\boldsymbol\kappa}(n)
=
\ln\left(
1+\frac{
B_{\boldsymbol\kappa}
}{
3^mn
}
\right).
}
$$

---

# 16. Correction 的性質

對：

$$
m\ge1,
$$

$$
B_{\boldsymbol\kappa}>0.
$$

所以：

$$
C_{\boldsymbol\kappa}(n)>0.
$$

且：

$$
\boxed{
C_{\boldsymbol\kappa}(n)\to0
\quad(n\to\infty)
}
$$

對 fixed valuation word 成立。

因此：

$$
\boxed{
m\ln3-K\ln2
}
$$

是 exact asymptotic skeleton drift。

---

# 17. Valuation Contraction Boundary

要求：

$$
3^m<2^K.
$$

取：

$$
\log_2:
$$

$$
m\log_2 3<K.
$$

即：

$$
\boxed{
\frac Km>\log_2 3.
}
$$

其中：

$$
\boxed{
\log_2 3
\approx1.5849625007.
}
$$

---

# 18. 與 Paper 05 的邊界等價

Paper 05：

$$
\frac uk
<
\frac{\ln2}{\ln3}.
$$

valuation expansion 給：

$$
u=m,
$$

$$
k=K.
$$

所以：

$$
\frac mK
<
\frac{\ln2}{\ln3}.
$$

取 reciprocal：

$$
\boxed{
\frac Km
>
\frac{\ln3}{\ln2}
=
\log_2 3.
}
$$

因此兩篇 contraction boundary 完全一致。

---

# 19. Exact Descent Criterion

由：

$$
S^m(n)
=
\frac{3^mn+B}{2^K},
$$

有：

$$
S^m(n)<n
$$

iff：

$$
\boxed{
B_{\boldsymbol\kappa}
<
(2^K-3^m)n.
}
$$

所以若：

$$
2^K>3^m,
$$

定義：

$$
\boxed{
\theta_{\boldsymbol\kappa}
=
\left\lfloor
\frac{
B_{\boldsymbol\kappa}
}{
2^K-3^m
}
\right\rfloor+1.
}
$$

則：

$$
n\ge\theta_{\boldsymbol\kappa}
$$

且 valuation word admissible，

即保證：

$$
\boxed{
S^m(n)<n.
}
$$

---

# 20. Uniform Expansion

若：

$$
2^K<3^m,
$$

則：

$$
(3^m-2^K)n>0,
$$

且：

$$
B_{\boldsymbol\kappa}>0.
$$

所以：

$$
\boxed{
S^m(n)>n
}
$$

對該 admissible valuation segment 上全部 positive $n$。

因此 valuation language 同樣具有 strict two-sided finite-word classification。

---

# 21. One-Step Valuation Residue Theorem

現在研究：

$$
\kappa(n)=v_2(3n+1)
$$

在 odd residue classes 中如何分布。

要求：

$$
v_2(3n+1)=j
$$

等價：

$$
3n+1
\equiv
2^j
\pmod{2^{j+1}}.
$$

所以：

$$
\boxed{
3n
\equiv
2^j-1
\pmod{2^{j+1}}.
}
$$

因：

$$
3
$$

在：

$$
\mathbb Z/2^{j+1}\mathbb Z
$$

為 unit，

恰有唯一 solution：

$$
\boxed{
n
\equiv
3^{-1}(2^j-1)
\pmod{2^{j+1}}.
}
$$

此 residue 自動為 odd。

---

# 22. Exact Residue Density

modulo：

$$
2^{j+1}
$$

共有：

$$
2^j
$$

個 odd residue classes。

其中恰好一個滿足：

$$
v_2(3n+1)=j.
$$

所以在 odd integers 中的 natural residue density：

$$
\boxed{
\delta_j
=
2^{-j}.
}
$$

因此：

$$
\boxed{
\sum_{j=1}^{\infty}\delta_j=1.
}
$$

這是一個 exact arithmetic density law。

---

# 23. Mean Valuation = 2

由：

$$
\delta_j=2^{-j},
$$

得到：

$$
\boxed{
\sum_{j=1}^\infty
j2^{-j}
=
2.
}
$$

所以：

$$
\boxed{
\mathbb E_{\mathrm{res}}[\kappa]=2.
}
$$

這裡的 expectation 指：

> 對 odd residue classes 的自然密度分布。

不是宣稱 actual orbit 上 $\kappa_i$ 是 independent random variables。

---

# 24. 舊「平均除 2 深度約為 2」的校正

所以舊研究的：

> $v_2(3n+1)$ 平均約為 2

可以改寫為精確版本：

$$
\boxed{
\text{one-step odd-residue valuation distribution is geometric with mass }2^{-j}.
}
$$

因此 mean exactly：

$$
2.
$$

這比 heuristic 說法更強、更清楚。

---

# 25. Ensemble Skeleton Drift

如果只對 one-step residue ensemble 平均 skeleton：

$$
\ln3-\kappa\ln2,
$$

則：

$$
\mathbb E_{\mathrm{res}}
[
\ln3-\kappa\ln2
]
$$

$$
=
\ln3
-
2\ln2.
$$

所以：

$$
\boxed{
\mathbb E_{\mathrm{res}}[\Delta L_{\mathrm{skeleton}}]
=
\ln\frac34
<0.
}
$$

這精確解釋了 Collatz 負漂移 heuristic 的來源。

---

# 26. 但 Correction 仍然是正的

單步 exact drift：

$$
\ln S(n)-\ln n
=
\ln3
-
\kappa(n)\ln2
+
\ln\left(
1+\frac1{3n}
\right).
$$

最後一項：

$$
\boxed{
\ln\left(
1+\frac1{3n}
\right)>0.
}
$$

但：

$$
\to0
$$

當：

$$
n\to\infty.
$$

所以「$3/4$」是 large-$n$ skeleton mean，

不是每個 finite $n$ 的 exact multiplier。

---

# 27. 最大的量詞警告：Residue Density ≠ Orbit Independence

即使：

$$
\Pr_{\mathrm{res}}(\kappa=j)=2^{-j},
$$

也不能直接假設同一條 orbit 上：

$$
\kappa_1,\kappa_2,\ldots
$$

是 independent geometric samples。

因為：

$$
n_{i+1}
=
S(n_i)
$$

由前一 state 決定。

因此 valuation sequence 具有 arithmetic dependence。

所以：

$$
\boxed{
\text{exact one-step marginal}
\not\Rightarrow
\text{i.i.d. orbit process}.
}
$$

---

# 28. 為什麼 Tao 的結果遠比「平均 = 2」深？

Tao 對 closely related Syracuse iteration 的 almost-all theorem 並不是簡單把 valuations 當作 independent geometric random variables。

其證明涉及：

- first-passage random variable；
- approximate transport；
- skew random walk；
- $3$-adic cyclic groups；
- Fourier decay；
- renewal process。

因此：

$$
\boxed{
\text{negative one-step ensemble drift}
}
$$

只是直覺入口，

不是 almost-all theorem 的替代品。

---

# 29. Valuation-Order Correction

對：

$$
\boldsymbol\kappa
=
(\kappa_1,\ldots,\kappa_m),
$$

$$
B_{\boldsymbol\kappa}
=
\sum_{i=1}^m
3^{m-i}2^{K_{i-1}}.
$$

固定：

$$
m,K,
$$

仍不足以決定：

$$
B_{\boldsymbol\kappa}.
$$

因為：

$$
K_{i-1}
$$

取決於 valuation order。

---

# 30. Adjacent Valuation Swap Theorem

假設在位置：

$$
i,i+1
$$

有：

$$
a,b,
$$

此前 cumulative valuation：

$$
P=K_{i-1}.
$$

比較：

$$
\boldsymbol\kappa
=
(\ldots,a,b,\ldots)
$$

及：

$$
\boldsymbol\kappa'
=
(\ldots,b,a,\ldots).
$$

兩者：

$$
m
$$

與：

$$
K
$$

完全相同。

因交換後 pair 的總 valuation：

$$
a+b
$$

不變，

所以所有 pair 之後的 prefix sums 相同。

唯一差別是 pair 中第二個 injection term。

因此：

$$
\boxed{
B_{\boldsymbol\kappa}
-
B_{\boldsymbol\kappa'}
=
3^{m-i-1}
2^P
(2^a-2^b).
}
$$

---

# 31. Ordering Corollary

若：

$$
a>b,
$$

則：

$$
2^a-2^b>0.
$$

所以：

$$
\boxed{
B_{(\ldots,a,b,\ldots)}
>
B_{(\ldots,b,a,\ldots)}.
}
$$

因此對 fixed valuation multiset：

$$
\boxed{
\kappa_1\le\kappa_2\le\cdots\le\kappa_m
}
$$

最小化 correction，

而：

$$
\boxed{
\kappa_1\ge\kappa_2\ge\cdots\ge\kappa_m
}
$$

最大化 correction。

---

# 32. 這個結果的意義

較大的 valuation 代表：

$$
3n+1
$$

後有更多 powers of 2 可除。

直覺上似乎「越早大 valuation 越有利下降」。

但對 fixed total：

$$
K,
$$

主 drift：

$$
3^m/2^K
$$

已固定。

較大的 valuation 越早出現，

反而會把後續 $+1$ injections 置於更大的 prefix power：

$$
2^{K_{i-1}},
$$

因此提高 affine correction：

$$
B_{\boldsymbol\kappa}.
$$

這不是說 early large valuation 整體有害，

而是說：

> 在固定 $(m,K)$ 的 comparison 中，order 只剩 finite correction effect，而 early concentration 使 correction 更大。

---

# 33. Skeleton vs Correction 再次分離

所以：

$$
\boxed{
(m,K)
}
$$

決定：

$$
\text{asymptotic side},
$$

而：

$$
\boxed{
(\kappa_1,\ldots,\kappa_m)
}
$$

的排列決定：

$$
\text{finite threshold}.
$$

這正好平行 Paper 02：

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

---

# 34. Exact Reverse Step

給定 odd target：

$$
t,
$$

和 valuation：

$$
\kappa\ge1,
$$

若：

$$
S(n)=t
$$

且：

$$
v_2(3n+1)=\kappa,
$$

則：

$$
3n+1
=
2^\kappa t.
$$

所以：

$$
\boxed{
n
=
R_\kappa(t)
=
\frac{2^\kappa t-1}{3}.
}
$$

---

# 35. Reverse Legality

$R_\kappa(t)$ 為 integer iff：

$$
\boxed{
2^\kappa t\equiv1\pmod3.
}
$$

若成立且：

$$
t>0
$$

odd，

則 numerator 是 odd，

故 predecessor 也是 odd。

因此它給 exact odd inverse fiber。

---

# 36. Multi-Step Reverse Recovery

若 valuation word：

$$
(\kappa_1,\ldots,\kappa_m)
$$

與 terminal odd state：

$$
t=n_m
$$

是 reverse-admissible，

則逐步：

$$
n_{m-1}=R_{\kappa_m}(n_m),
$$

$$
n_{m-2}=R_{\kappa_{m-1}}(n_{m-1}),
$$

直到：

$$
n_0.
$$

因每步 fixed $\kappa$，

inverse 是單值的。

---

# 37. Closed Reverse Formula

由 forward：

$$
2^K n_m
=
3^m n_0
+
B_{\boldsymbol\kappa},
$$

所以：

$$
\boxed{
n_0
=
\frac{
2^K n_m
-
B_{\boldsymbol\kappa}
}{
3^m}.
}
$$

因此對 reverse-admissible word：

$$
\boxed{
\text{valuation encoding is losslessly invertible}.
}
$$

---

# 38. 為什麼仍要保留 Recursive Legality？

只檢查 final closed fraction：

$$
\frac{
2^K t-B
}{
3^m}
$$

是 integer，

不應在未證明前自動等同於：

> 每個 intermediate reverse state 都滿足對應 valuation legality。

所以 rigorous inverse procedure 應保留：

$$
\boxed{
R_{\kappa_m},
R_{\kappa_{m-1}},
\ldots,
R_{\kappa_1}
}
$$

逐步 legality checks。

closed formula 是 recovery identity，

不是跳過 intermediate admissibility 的許可。

---

# 39. Terminal Fiber 再解釋

取：

$$
t=1
$$

與 single valuation：

$$
\kappa=2j.
$$

由：

$$
2^{2j}\equiv1\pmod3,
$$

得到：

$$
\boxed{
R_{2j}(1)
=
\frac{4^j-1}{3}.
}
$$

所以舊：

$$
M_j
$$

系列就是 terminal state 1 的 even-valuation inverse fiber。

這在 Paper 04 已建立，

本文則把它放進完整 valuation language 中。

---

# 40. Valuation-Labeled Odd Skeleton

accelerated odd inverse graph 可以記：

$$
n
\xrightarrow{\kappa}
t
$$

iff：

$$
\boxed{
3n+1=2^\kappa t.
}
$$

所以每條 edge 自帶：

$$
\boxed{
\kappa=v_2(3n+1)
}
$$

label。

一條 odd skeleton path：

$$
n_0\to n_1\to\cdots\to n_m
$$

因此自然對應：

$$
\boxed{
(\kappa_1,\ldots,\kappa_m).
}
$$

這就是 valuation language 的圖論版本。

---

# 41. 舊「耗散」語言應如何保留？

可以保留直覺：

$$
3
$$

是一次 odd update 的放大，

而：

$$
2^\kappa
$$

是其 valuation-controlled contraction。

但嚴格數學不再說：

> 「耗散必然戰勝輸入」。

而說：

$$
\boxed{
\text{for a fixed finite valuation word, the exact skeleton multiplier is }
\frac{3^m}{2^K}.
}
$$

其下降與否由：

$$
2^K\gtrless3^m
$$

精確決定。

---

# 42. 本文沒有證明什麼？

本文沒有證明：

$$
\frac{K_m}{m}>\log_2 3
$$

對每一條 sufficiently long ordinary positive-integer orbit 都最終成立。

沒有證明：

$$
\kappa_i
$$

沿 orbit 是 independent。

沒有從：

$$
\mathbb E_{\mathrm{res}}\kappa=2
$$

推出 universal convergence。

沒有排除 exceptional valuation words。

本文只把：

- finite valuation trajectory；
- one-step residue density；
- exact drift；
- exact correction；
- inverse recovery；

嚴格分層。

---

# 43. 本文主要定理總結

## Theorem A — Valuation Run-Length Encoding

$$
\boxed{
E(\boldsymbol\kappa)
=
UD^{\kappa_1-1}
\cdots
UD^{\kappa_m-1},
}
$$

且：

$$
|E|=K,\qquad u(E)=m.
$$

## Theorem B — Accelerated Affine Closure

$$
\boxed{
S^m(n)
=
\frac{
3^mn+B_{\boldsymbol\kappa}
}{
2^K}.
}
$$

## Theorem C — Correction Closed Form

$$
\boxed{
B_{\boldsymbol\kappa}
=
\sum_{i=1}^{m}
3^{m-i}2^{K_{i-1}}.
}
$$

## Theorem D — Exact Log Drift

$$
\boxed{
\Delta L
=
m\ln3-K\ln2
+
\ln\left(
1+\frac{B_{\boldsymbol\kappa}}{3^mn}
\right).
}
$$

## Theorem E — Valuation Contraction Boundary

$$
\boxed{
2^K>3^m
\iff
K/m>\log_2 3.
}
$$

## Theorem F — One-Step Valuation Density

$$
\boxed{
\delta(\kappa=j)=2^{-j},
\qquad
\mathbb E_{\mathrm{res}}\kappa=2.
}
$$

## Theorem G — Adjacent Valuation Swap

$$
\boxed{
\Delta B
=
3^{m-i-1}2^{K_{i-1}}
(2^a-2^b).
}
$$

## Theorem H — Exact Reverse Recovery

$$
\boxed{
n_0
=
\frac{
2^K n_m-B_{\boldsymbol\kappa}
}{
3^m}
}
$$

on reverse-admissible valuation words.

---

# 44. 結論

作者早期 Collatz 系統論的核心直覺是：

> 一次 $3n+1$ 的放大，會被隨後多次除以 2 的指數性收縮抵消。

本文將這句話拆成三個不同強度的數學層級。

第一層是完全 exact 的 finite-word theorem：

$$
\boxed{
S^m(n)
=
\frac{
3^mn+B_{\boldsymbol\kappa}
}{
2^K}.
}
$$

所以：

$$
\boxed{
K/m>\log_2 3
}
$$

精確決定 fixed valuation word 的 contracting skeleton side。

第二層是 exact one-step residue-density theorem：

$$
\boxed{
\Pr_{\mathrm{res}}(\kappa=j)=2^{-j},
}
$$

因此：

$$
\boxed{
\mathbb E_{\mathrm{res}}\kappa=2
}
$$

以及 skeleton ensemble mean：

$$
\boxed{
\ln3-2\ln2=\ln(3/4)<0.
}
$$

第三層才是未完成的 global orbit 問題：

> actual valuation itinerary 是否能以足夠強的方式被全稱控制？

這一層不能由前兩層直接推出。

因此本文真正完成的是：

$$
\boxed{
\text{heuristic negative drift}
\longrightarrow
\text{exact valuation-language dynamics}
+
\text{explicit statistical boundary}.
}
$$

同時，valuation order correction 顯示：

$$
\boxed{
(m,K)
\text{決定主漂移，}
}
$$

$$
\boxed{
(\kappa_1,\ldots,\kappa_m)
\text{的排列決定 finite correction}.
}
$$

所以 accelerated odd dynamics 與前五篇的 Local Affine Atlas 完全接合。

下一篇將把 Collatz 的數字 $3,1,2$ 換成一般 odd parameters，研究：

$$
C_{p,r}(n)
=
\begin{cases}
n/2,\\
(pn+r)/2,
\end{cases}
$$

並找出：

$$
\boxed{
\frac{u}{k}
<
\frac{\ln2}{\ln p}
}
$$

所形成的廣義 phase boundary，以及 $p=3$、$p\ge5$ 在 cylinder density 上的結構分流。

---

# 參考文獻

1. Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562; Forum of Mathematics, Pi 10 (2022).
2. Olivier Rozier, Claude Terracol, *Paradoxical behavior in Collatz sequences*, arXiv:2502.00948.
3. Tong Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, arXiv:2605.13886.
4. Olivier Rozier, *Parity sequences of the 3x+1 map on the 2-adic integers and Euclidean embedding*, arXiv:1805.00133.
5. Collatz Operation Translation Series — Paper 02, *Collatz Local Affine Atlas：有限奇偶字的精確仿射化*.
6. Collatz Operation Translation Series — Paper 03, *Parity Word、Residue Cylinder 與局部 Identity 化*.
7. Collatz Operation Translation Series — Paper 04, *雙向殘餘類轉譯：$2^k$ Cylinder 與 $3^u$ Progression*.
8. Collatz Operation Translation Series — Paper 05, *有限字收縮邊界與二項式 Cylinder Law*.

---

## 下一篇

**Paper 07 —《廣義 $mx+r$ 系統與 Residue-Class Operation Translation》**

核心任務：

1. 將 $3n+1$ 改為一般 odd $mn+r$；
2. 證明 finite-word affine closure；
3. 推導 generalized correction；
4. 建立 word–residue legality 的 unit 條件；
5. 推導：
   $$
   \frac uk<\frac{\ln2}{\ln m};
   $$
6. 比較 $m=1,3,5,7,\ldots$；
7. 建立 $m<4$ / $m>4$ 的典型 cylinder phase boundary；
8. 明確界定哪些結論是 Collatz-specific，哪些屬更一般 Residue-Class Operation Translation。
