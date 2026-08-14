# 02｜已知定理閉包圖

## 0. 作用

本文件不是完整文獻綜述，而是回答：

> 每一條現有理論，究竟關閉 BSD 的哪一個 component？

---

# 1. 基礎解析層：已關閉

對 $E/\mathbb Q$，模性定理提供相應 weight-$2$ modular form，從而給 $L(E,s)$ 的解析延拓與泛函方程。

所以本專案不把「$L$-函數是否存在」當前線。

---

# 2. 解析秩 $0$、$1$：弱 BSD 核心閉包

Gross–Zagier 與 Kolyvagin 的工作，結合模性定理，建立：

若：

$$
r_{\mathrm{an}}=0
\quad\text{或}\quad
r_{\mathrm{an}}=1,
$$

則：

$$
r_{\mathrm{alg}}=r_{\mathrm{an}},
$$

並給出相應 $\Sha$ 有限性控制。

這是 BSD 最重要的低秩閉包。

但它不能被外推為：

$$
r_{\mathrm{an}}\ge2.
$$

---

# 3. 強 BSD 的 $p$-part：快速推進區

近年的 Iwasawa theory、Euler systems、Kato classes、Heegner points 與 $p$-adic $L$-functions，已在大量條件下證明：

- rank $0/1$ 的 $p$-part BSD；
- ordinary / supersingular primes 的 main conjecture；
- p-converse；
- 非 CM 曲線的無限 twist families satisfying strong BSD。

這一層非常適合 theorem-applicability engine。

但每個結果通常有明確條件：

```text
semistable?
p divides conductor?
ordinary/supersingular?
split in an imaginary quadratic field?
residual representation?
Eisenstein prime?
local Tamagawa divisibility?
```

---

# 4. 高秩：結構進展，但無一般閉包

rank $2$ 及以上已有：

- generalized Kato classes；
- higher Gross–Zagier formula；
- Selmer structure results；
- derived classes；
- higher-rank Iwasawa theory。

但目前不能整理成：

$$
\forall E/\mathbb Q,\quad
r_{\mathrm{an}}\ge2
\Rightarrow
r_{\mathrm{alg}}=r_{\mathrm{an}}.
$$

所以高秩仍是 BSD-W 的主要牆。

---

# 5. 強式的 $\Sha$ 與首項公式

完整 BSD-S 不只需要 rank。

還要：

1. actual $\Sha$ finite；
2. actual order；
3. regulator exact enough and based on a saturated Mordell–Weil basis；
4. local Tamagawa factors；
5. torsion；
6. period convention；
7. exact leading term。

有限案例可以 exact verify；一般曲線族則需要更深的 descent / Iwasawa / Euler system。

---

# 6. 計算驗證的學術地位

Keller–Stoll 類工作顯示，完整強 BSD 可以在明確有限集合上被無條件、精確地驗證，甚至對 dimension $2$ 的 absolutely simple modular abelian varieties。

這提供一個重要工程教訓：

$$
\boxed{
\text{完整 BSD 證書是可工程化的，
但每個 component 都必須獨立閉合。}
}
$$

---

# 7. 算術統計

Selmer group average、rank distribution、twist families 與 Goldfeld-type 結果可以：

- 預測大多數曲線落在 rank $0/1$；
- 找高價值 families；
- 測試 $\Sha$ 分布；
- 決定 Agent 預算。

但：

$$
\boxed{
\text{正密度／平均結果}
\neq
\forall E.
}
$$

它們是 research routing，不是 global closure。

---

# 8. 閉包表

| 層級 | 狀態 | 主要方法 | 全域缺口 |
|---|---|---|---|
| 模性與解析延拓 | 已關閉 | modularity theorem | 無 |
| analytic rank $0/1$ 的弱 BSD | 核心已關閉 | Gross–Zagier, Kolyvagin | 高秩 |
| rank $0/1$ 的若干 $p$-part | 大量新閉包 | Iwasawa, zeta elements | 條件與全 prime 統一 |
| 無限 strong-BSD twist families | 已存在 | zeta elements + algorithmic criteria | 不覆蓋所有 curves |
| rank $\ge2$ 弱 BSD | 開放 | higher classes | 非消失與 rank bridge |
| $\Sha$ 一般有限性 | 開放 | Selmer / Euler systems | 高秩與全 prime |
| 完整 leading coefficient | 開放 | strong BSD machinery | 全部 components |
| 所有 $E/\mathbb Q$ | 開放 | 無單一路線 | 全域 uniformity |
