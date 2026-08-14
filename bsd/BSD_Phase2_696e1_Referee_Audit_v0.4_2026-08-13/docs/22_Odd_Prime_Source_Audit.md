# 22｜Odd Prime Source Audit

令 $d=q$ 為 support prime。

## A. $p=q$：additive twist

Banwait–Huang Proposition 2.9 Item 1直接把此 case歸到 BSTW Theorem 9.21(c)。

其 proof列出：

- $p\ge5$；
- $p\nmid6N$；
- $p$ good ordinary for base $E$；
- $\bar\rho_{E,p}$ irreducible；
- `(ramK)`：存在 $\ell\parallel N$，$\ell\nmid D_K$，residual ramified。

對 `696.e1`：

- $q\equiv1\pmod{24}$；
- $q\neq29$；
- support inertness推出 ordinary；
- base mod-$q$ image maximal，故 absolutely/ordinary residual irreducible；
- 取 $\ell=29$；
- $v_{29}(\Delta)=1$，所以 $q\nmid1$；
- $29\nmid D_K=q$。

所以 PASS。

Banwait Remark 2.10明說 semistability在 Item 1只用來自動產生 ramified witness；
non-semistable 時把 witness當 hypothesis即可。

---

## B. good ordinary $p$

直接用 Skinner Theorem C：

- $p\ge3$；
- good ordinary；
- $E_q[p]$ irreducible；
- 存在另一 multiplicative $\ell$ residual ramified；
- $L(E_q,1)\ne0$。

取：

$$
\ell=29.
$$

good ordinary $p$ 不等於 $29$，且 $p\nmid v_{29}(\Delta)=1$。

PASS。

---

## C. multiplicative $p=3$

Skinner Theorem C **明確寫 $p\ge3$**。

取 witness：

$$
\ell=29.
$$

PASS。

---

## D. multiplicative $p=29$

取 witness：

$$
\ell=3.
$$

因：

$$
v_3(\Delta)=1.
$$

PASS。

---

# Important simplification

由於 base curve mod-$\ell$ image對所有 $\ell$ maximal，
quadratic twist只 tensor一個 scalar character，故 irreducibility保持。

因此 ordinary branch無需再拆 reducible/irreducible subcases。
