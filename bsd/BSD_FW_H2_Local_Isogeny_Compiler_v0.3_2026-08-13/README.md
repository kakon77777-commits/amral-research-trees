# BSD Phase 2 — Fouquet–Wan H2 Local Isogeny Compiler v0.3

**日期：** 2026-08-13  
**定位：** fixed odd additive prime 的 exact local compiler  
**狀態：** representation-level H2 compiler CLOSED；local \(p\)-isogeny computation backend 尚待本地 Sage/Magma 接入。

---

## 0. 本輪最重要的修正

Fouquet–Wan 有兩個容易被混淆的 theorem profile。

### `FW11_SIMPLE`

Theorem 1.1 的 local residual hypothesis排除兩種型態：

\[
\bar\rho_p^{ss}\not\simeq \chi\oplus\chi,
\]

以及

\[
\bar\rho_p^{ss}\not\simeq
\chi\oplus\bar\chi_{\rm cyc}\chi.
\]

### `FW17_EXACT`

Theorem 1.7 的 exact local hypothesis只排除：

\[
\boxed{
\bar\rho_p^{ss}\not\simeq
\chi\oplus\bar\chi_{\rm cyc}\chi.
}
\]

但其 auxiliary-prime hypothesis更具體：需要指定的 ramified
nonsplit-Steinberg residual extension。

我們的 witness-network 本來就使用 nonsplit multiplicative prime作
Fouquet–Wan auxiliary witness，所以預設：

```text
profile = FW17_EXACT
```

這比誤把 Theorem 1.1 的較強 H2 也強加上去更準確。

---

# 1. Exact elliptic-curve translation

令

\[
V=E[p]|_{G_{\mathbf Q_p}},
\qquad
\omega=\bar\chi_{\rm cyc}.
\]

對 elliptic curve：

\[
\det V=\omega.
\]

如果 \(V\) 在 \(\mathbf F_p\) 上 irreducible，則
`FW17_H2 = PASS`。

若 \(V\) reducible，選一條 \(G_{\mathbf Q_p}\)-stable line，其 character為
\(\lambda\)。則

\[
V^{ss}\simeq
\lambda\oplus\mu,
\qquad
\mu=\omega\lambda^{-1}.
\]

FW17 禁型成立 iff 存在 \(\chi\)：

\[
\{\lambda,\mu\}
=
\{\chi,\omega\chi\}.
\]

比較 determinant：

\[
\omega
=
\chi^2\omega,
\]

所以：

\[
\chi^2=1.
\]

因此得到 exact lemma：

\[
\boxed{
\mathrm{FW17\text{-}H2\ FAIL}
\iff
\lambda^2=1
\ \lor\
\mu^2=1.
}
\]

也就是：

> **FW17-H2 失敗 iff local Jordan–Hölder constituents 中至少有一個 quadratic（含 trivial）character。**

這不是 heuristic，而是 theorem hypothesis 的直接代數改寫。

---

# 2. Local \(p\)-isogeny kernel criterion

一條 local stable line：

\[
C\subset E[p]
\]

等價於一條在 \(\mathbf Q_p\) 上定義的 cyclic \(p\)-isogeny：

\[
\phi:E\to E'.
\]

令 \(\lambda\) 是 \(\ker\phi\) 的 Galois character。

對 generator：

\[
P\in\ker\phi,
\]

因 \(p\) odd：

\[
x(P)\in\mathbf Q_p
\iff
\sigma(P)=\pm P
\quad
\forall\sigma\in G_{\mathbf Q_p}.
\]

因此：

\[
\boxed{
x(P)\in\mathbf Q_p
\iff
\lambda^2=1.
}
\]

而 quotient character：

\[
\mu=\omega\lambda^{-1}
\]

正是 dual isogeny：

\[
\widehat\phi:E'\to E
\]

的 kernel character。

所以：

\[
\boxed{
\mathrm{FW17\text{-}H2\ FAIL}
}
\]

iff：

- \(\ker\phi\) 的 generator 有 \(\mathbf Q_p\)-rational \(x\)-coordinate；
- **或** \(\ker\widehat\phi\) 的 generator 有 \(\mathbf Q_p\)-rational \(x\)-coordinate。

等價地：

> \(\phi\) 或 \(\widehat\phi\) 的 kernel polynomial 在 \(\mathbf Q_p\) 上有 linear factor。

這提供一個不需要顯式 local Galois matrices 的 exact backend。

---

# 3. Production algorithm

對 fixed odd additive prime \(p\)：

```text
Input:
    E / Q
    p odd additive bad prime
    profile = FW17_EXACT

Step A:
    certify global E[p] absolute irreducibility.
    FAIL -> Fouquet–Wan theorem unavailable.

Step B:
    decide local reducibility of E[p]|G_Qp over F_p.

    IRREDUCIBLE:
        FW17-H2 = PASS.

    REDUCIBLE:
        construct one local p-isogeny phi:E->E'
        and its dual phihat:E'->E.

Step C:
    test kernel polynomial(phi) for Q_p-linear factor.
    test kernel polynomial(phihat) for Q_p-linear factor.

    either YES:
        FW17-H2 = FAIL.

    both NO:
        FW17-H2 = PASS.
```

注意：

- 不需要所有 local \(p\)-isogenies；
- 一條 \(\phi\) 與它的 dual 已經同時看到兩個 Jordan–Hölder constituents；
- 若 original extension nonsplit，dual kernel仍代表 quotient constituent；
- 若 representation split，兩者就是兩條 constituent lines。

---

# 4. Cheap exact gates

## 4.1 \(p=3\)

因：

\[
\mathbf F_3^\times=\{\pm1\},
\]

任何 \(\mathbf F_3^\times\)-valued character都滿足：

\[
\lambda^2=1.
\]

所以：

\[
\boxed{
p=3:
\quad
\mathrm{FW17\text{-}H2\ PASS}
\iff
E[3]|_{G_{\mathbf Q_3}}
\text{ irreducible over }\mathbf F_3.
}
\]

local reducible ⇒ automatic FAIL。

---

## 4.2 potentially multiplicative additive reduction

potentially multiplicative curve在 quadratic splitting character \(\psi\) twist後成為 Tate/multiplicative curve。

因此 residual semisimplification是：

\[
\psi
\oplus
\psi\omega.
\]

其中：

\[
\psi^2=1.
\]

這**正是** FW17 禁型。

所以：

\[
\boxed{
\text{fixed additive potentially multiplicative at }p
\Rightarrow
\mathrm{FW17\text{-}H2=FAIL}.
}
\]

這一類不能用 FW17 當 additive repair route。

---

## 4.3 local rational \(p\)-torsion

若：

\[
E(\mathbf Q_p)[p]\neq0,
\]

則 local representation有 trivial constituent：

\[
\lambda=1.
\]

因此：

\[
\boxed{
E(\mathbf Q_p)[p]\neq0
\Rightarrow
\mathrm{FW17\text{-}H2=FAIL}.
}
\]

Pannekoek 的 additive-\(p\)-torsion theorem可作 cheap local filter，
但它只偵測 trivial constituent；**沒有 local rational \(p\)-torsion不等於 H2 PASS**，
因為還可能有 nontrivial quadratic constituent。

---

# 5. Kodaira type 的正確角色

本輪正式撤回：

```text
potentially supersingular => H2 PASS
```

這種簡化。

對 fixed additive \(p\)，Kodaira / potential-reduction type本身不能決定：

\[
\lambda^2=1
\quad\text{or}\quad
\mu^2=1.
\]

同一 potential-reduction 類中仍可能有不同 residual reducibility /
isogeny-character行為。

所以 Kodaira table只當：

```text
PREFILTER
```

不能當：

```text
H2 PROOF.
```

唯一乾淨的 reduction-type no-go shortcut是 potentially multiplicative，
因它的 semisimplification本身就是 FW17 禁型。

---

# 6. Theorem 1.1 profile

若未來某 route選用較強但較簡單的 `FW11_SIMPLE`，
除了 FW17 的 quadratic-constituent test外，還必須額外排除：

\[
V^{ss}\simeq\chi\oplus\chi.
\]

在 reducible notation：

\[
V^{ss}=\lambda\oplus\mu,
\]

這等價於：

\[
\boxed{\lambda=\mu.}
\]

由 determinant：

\[
\lambda\mu=\omega,
\]

亦即：

\[
\lambda^2=\omega.
\]

因此：

```text
FW11_SIMPLE PASS
=
FW17 quadratic test PASS
AND
lambda != mu.
```

這個額外條件**不是** rational-x kernel test。

所以 production schema必須記：

```text
theorem_profile
```

避免把 FW11 與 FW17 hypotheses混在一起。

---

# 7. Witness-network integration

上一版 fixed odd additive certificate：

```text
A1 global absolute irreducibility
A2 FW-H2
A3 nonsplit H3 witness
A4 period
```

現在 A2 已經具體化：

```text
A2a local reducibility
A2b local p-isogeny phi
A2c dual phihat
A2d phi kernel Qp-linear-root?
A2e dual kernel Qp-linear-root?
```

對 `FW17_EXACT`：

```text
both root tests NO
=> A2 PASS.
```

因此 witness-network 現在剩下兩類未閉合工程：

1. **backend**：
   本地 Sage/Magma如何 certified construct local p-isogeny / kernel polynomial；
2. **period**：
   fixed additive prime的 modular/Néron period compatibility。

第一類是計算實作，不再是數學定義缺口。

---

# 8. Gate status

```text
FW17 exact hypothesis statement               CLOSED
elliptic determinant reduction                CLOSED
Jordan-Hölder quadratic-character criterion   CLOSED
local p-isogeny equivalence                    CLOSED
kernel rational-x criterion                    CLOSED
p=3 shortcut                                   CLOSED
potentially multiplicative no-go               CLOSED
Kodaira-only compiler                          FORMALLY REJECTED
local Sage/Magma backend                       OPEN / ENGINEERING
fixed-additive period compiler                 OPEN / MATH+ENGINEERING
```

這輪已經改變 Gate status：

\[
\boxed{
\text{fixed additive H2}
:
\text{theoretical UNKNOWN}
\longrightarrow
\text{finite exact local certificate}.
}
\]

下一輪主數學問題因此不再是 H2，而是：

\[
\boxed{
\text{fixed additive period compiler}.
}
\]
