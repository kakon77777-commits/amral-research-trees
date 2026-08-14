# 07｜停止規則與 Claim Ladder

## C0 — Literature map

只知道哪些 theorem可能相關。

## C1 — Hypothesis compiler

每條 FW hypothesis有 exact executable meaning。

## C2 — Fixed $(E,p)$ certificate

能嚴格證：

$$
\mathrm{FW}(E,p).
$$

## C3 — Twist-uniform fixed-$p$

證：

$$
\forall d\in\mathcal D(E),
\quad
\mathrm{FW}(E_d,p).
$$

## C4 — Finite exceptional-prime reduction

證：

$$
p\notin P_E
\Rightarrow
\mathrm{FW}(E,p),
$$

且 $P_E$ finite/computable。

## C5 — All odd primes

逐項關閉：

$$
p\in P_E
$$

後得到：

$$
\forall p>2.
$$

## C6 — Full strong-BSD twist family

與 Banwait $2$-part / nonvanishing拼接，得到：

$$
\forall d\in\mathcal D(E),
\quad
\operatorname{BSD}(E_d).
$$

---

# 禁止升級

- 測 $p<1000$ 不等於 C4/C5；
- 99.9% primes不等於 C5；
- residual image「看起來 generic」不等於 theorem；
- non-semistable sample成功不等於所有 non-semistable curves；
- Fouquet–Wan theorem存在不等於它已經 algorithmized。

---

# 三輪停止規則

若連續三輪：

- 只增加 checked primes；
- 只增加 curves；
- H2/H3 exact meaning沒有進展；
- finite exceptional set沒有 theorem化；

則凍結 database scaling，回到 local Galois lemma。

這避免重演「資料越跑越多，但全域量詞完全沒縮」。
