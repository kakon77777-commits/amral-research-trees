# 05｜Non-Semistable Family Theorem Schema

## Candidate theorem（尚未證）

本文件不是定理宣稱，而是列出完整 proof obligations。

令：

$$
E/\mathbb Q
$$

為 optimal、analytic-rank-0 elliptic curve，不要求 semistable。

令：

$$
\mathcal D(E)
$$

是一個 squarefree twist parameter family，使 Banwait–Huang Theorem 2.14 的某一 branch成立。

則對：

$$
d\in\mathcal D(E)
$$

已知候選輸出：

$$
L(E_d,1)\ne0,
$$

$$
\operatorname{BSD}(E_d,2).
$$

若再能證：

$$
\forall p>2,
\quad
\operatorname{BSD}(E_d,p),
$$

則：

$$
\operatorname{BSD}(E_d)
$$

成立。

---

# Bridge hypotheses

對每個 odd $p$：

1. FW-H1/H2/H3 對 base $E$ 成立；
2. H1/H2在 quadratic twist下保持；
3. $d$ 的 splitting conditions使 H3 witness局部保持；
4. Fouquet–Wan Corollary的 period / Manin normalization與 Banwait BSD convention相容；
5. $L(E_d,1)\ne0$ 可直接供給 FW rank-zero corollary。

若上述全證：

$$
\boxed{
\forall d\in\mathcal D(E),
\quad
\mathrm{BSD}(E_d).
}
$$

---

# 目前最危險的兩個 gap

## Gap A

$$
\forall p>2
$$

尚未 finite-ized。

## Gap B

FW Corollary中的 modular-form period到 Néron period在小質數 $p$ 的 Manin constant處理需要乾淨拼接。

因此第一版最好：

- 用 FW 處理「large / generic odd primes」；
- 保留 Banwait 已有 small-prime theorems處理 $3,5,7$；
- 對 $p=2$ 保留 Theorem 2.14。

這可能形成更容易發表與驗證的 hybrid theorem。
