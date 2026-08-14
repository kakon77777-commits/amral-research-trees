# 17｜696.e1 All-Prime Router

令：

$$
q\in\mathcal P,
\qquad
d=q.
$$

由 Theorem 2.14：

$$
L(E_q,1)\neq0
$$

且：

$$
\operatorname{BSD}(E_q,2).
$$

現在只需 odd primes。

---

# Case A — $p=q$

$E$ 在 $q$：

- good；
- ordinary；
- $q\ge5$；
- residual irreducible。

取 witness：

$$
\ell=29.
$$

因：

$$
v_{29}(\Delta_E)=1,
$$

所以：

$$
q\nmid v_{29}(\Delta_E),
$$

 residual ramified。

又 $29$ split in $\mathbb Q(\sqrt q)$，所以 local twist在 $29$ trivial。

因此 additive-twist ordinary branch可套。

---

# Case B — $p\nmid q$, good ordinary

quadratic twist保留 residual irreducibility。

需要 direct ramified witness時：

- 若 $p=3$：此 case不發生，因 $3$ bad；
- 若 $p=29$：此 case不發生，因 $29$ bad；
- 其他 $p$：取 $29$。

因：

$$
p\nmid1=v_{29}(\Delta_E).
$$

所以 ramified-prime condition直接成立。

---

# Case C — fixed multiplicative primes

只有：

$$
p=3,\ 29.
$$

### $p=3$

residual irreducible。

取：

$$
q_0=29.
$$

### $p=29$

residual irreducible。

取：

$$
q_0=3.
$$

兩個 valuations都是：

$$
1.
$$

所以 residual ramification成立。

---

# Case D — good supersingular

這是 semistability原本真正卡住的 branch。

使用 Fouquet–Wan sufficient theorem interface。

## FW-H1

good supersingular local representation irreducible，故 global residual absolutely irreducible。

## FW-H2

local residual irreducible，因此不可能半單化成 FW 禁止的 character direct sums。

## FW-H3

取：

$$
\ell=29.
$$

$29$ 為 nonsplit multiplicative，且：

$$
v_{29}(\Delta)=1.
$$

任意 good supersingular odd $p$ 都：

$$
p\neq29,
\qquad
p\nmid1.
$$

所以 residual Steinberg extension ramified，且 nonsplit給 nontrivial unramified quadratic twist。

---

# Period / Manin issue

FW $p$-part corollary使用 modular period。

對 good supersingular $p$，$p$ 是 good reduction prime，因此：

$$
p\nmid N_{E_q}.
$$

Manin constant在這種 prime沒有 $p$-adic contribution（可使用已知 Manin-constant support結果）。

另外 base curve所有 mod-$\ell$ images maximal；twist保持 odd-$\ell$ irreducibility，$2$-torsion field不變，因此 $E_q$ 沒有 rational prime-degree isogeny。

這使 optimal/isogeny轉移問題保持乾淨。

---

# Exhaustion

odd $p$ 對 $E_q$ 只能是：

1. $p=q$ additive；
2. good ordinary；
3. multiplicative $3/29$；
4. good supersingular。

四類已覆蓋。

所以 prime router沒有遺漏 branch。
