# 01｜Theorem 2.18 條件圖

## A. Base curve $E/\mathbb Q$

令 conductor 為 $N$。

### E1 — Semistable

$$
E\text{ semistable}.
$$

### E2 — Small prime trace

$$
a_3(E)\in\{-2,-1,0,1,2\}.
$$

等價於排除：

$$
a_3(E)=\pm3.
$$

### E3 — Rational-isogeny exclusion

$$
E\text{ 無 rational }p\text{-isogeny},
\qquad
p\in\{3,5,7\}.
$$

### E4 — Ramification at multiplicative primes

對每個：

$$
p\mid N,
$$

存在另一個 multiplicative prime：

$$
q\mid N,\qquad q\ne p,
$$

使：

$$
E[p]
$$

在 $q$ ramified。

對 semistable curve，論文 Algorithm 1 將其轉成 minimal discriminant valuation 條件。

### E5 — Optimality

$$
E
$$

是 isogeny class 的 $\Gamma_0(N)$-optimal representative。

### E6 — Analytic rank zero

$$
\operatorname{ord}_{s=1}L(E,s)=0.
$$

### E7 — 2-part of BSD

$$
\operatorname{BSD}(E,2)
$$

已被無條件驗證。

---

# B. Branch 8a：無 rational 2-torsion

$$
E(\mathbb Q)[2]=0,
$$

$$
\operatorname{ord}_2 L^{(\mathrm{alg})}(E,1)=0.
$$

此分支由 Zhai 類結果處理。

---

# C. Branch 8b：恰有一個 rational 2-torsion

$$
E(\mathbb Q)[2]\cong\mathbb Z/2\mathbb Z,
$$

$$
\operatorname{ord}_2 L^{(\mathrm{alg})}(E,1)=-1.
$$

寫：

$$
E:y^2=f(x),
$$

且 rational 2-torsion 為：

$$
(x_0,0).
$$

要求：

$$
f'(x_0),\quad -f'(x_0),\quad -\Delta_E
$$

均不是 $\mathbb Q$ 中平方。

令：

$$
E'=E/E(\mathbb Q)[2].
$$

再要求：

$$
\Sha(E')[2]=0,
$$

並在 paper algorithm 中同時檢查：

$$
E'(\mathbb Q)[2]\cong\mathbb Z/2\mathbb Z.
$$

---

# D. Twist $d$ 的共同條件

$$
d\text{ squarefree},
$$

$$
(d,3N)=1,
$$

$$
d\equiv1\pmod4,
$$

且對所有：

$$
p\mid d,
$$

$E$ 在 $p$ ordinary。

對 good prime：

$$
\#E(\mathbb F_p)=p+1-a_p(E),
$$

而官方程式使用：

$$
p\nmid a_p(E)
$$

作 ordinary test。

---

# E. Zha16 branch 的 twist 條件

若：

$$
E(\mathbb Q)[2]=0,
$$

則：

1. 每個 $p\mid d$ 在 cubic 2-division field
   $$
   \mathbb Q[x]/(f_2(x))
   $$
   中 inert；
2. 每個 $p\mid N$ 在
   $$
   \mathbb Q(\sqrt d)
   $$
   中 split；
3. 若：
   $$
   \Delta_E>0,
   $$
   則：
   $$
   d>0.
   $$

---

# F. CLZ20 branch 的 twist 條件

若：

$$
E(\mathbb Q)[2]\cong\mathbb Z/2\mathbb Z,
$$

則對每個 $p\mid d$：

$$
p\equiv1\pmod4,
$$

$$
\operatorname{ord}_2\#E(\mathbb F_p)=1.
$$

並要求：

$$
d\equiv1\pmod8,
$$

以及每個 odd：

$$
p\mid N
$$

在：

$$
\mathbb Q(\sqrt d)
$$

中 split。

---

# G. 輸出語義

Algorithm 2 回傳的不是「所有滿足 BSD 的 twists」。

它只枚舉一個 theorem-guaranteed subfamily：

$$
\boxed{
\text{admissible}
\Rightarrow
\text{BSD follows from cited theorems}.
}
$$

反方向不成立：

$$
\boxed{
\text{not admissible}
\not\Rightarrow
\text{BSD false}.
}
$$
