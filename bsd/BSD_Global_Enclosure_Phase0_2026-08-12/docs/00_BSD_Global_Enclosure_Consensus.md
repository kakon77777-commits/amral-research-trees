# 00｜BSD 全局包圍共識裁決

## 0. 一句話

BSD 確實比 RH 更「講人話」：

$$
\boxed{
\text{左邊：}L(E,s)\text{ 在 }s=1\text{ 的行為}
\quad\Longleftrightarrow\quad
\text{右邊：有理點、局部資料與 }\Sha
}
$$

術語門檻很高，但每個術語都是高價值、型別清楚、可計算或可證書化的數學物件。

這使 BSD 特別適合多 Agent 分工。

---

# 1. 本次全局裁決

$$
\boxed{
\text{GO：進入 Phase 1。}
}
$$

但不直接以「完整 BSD」作單一任務。

先限定：

$$
E/\mathbb Q.
$$

再把猜想拆成三層：

## BSD-W：弱 BSD／秩等式

$$
\boxed{
\operatorname{rank}E(\mathbb Q)
=
\operatorname{ord}_{s=1}L(E,s).
}
$$

## BSD-F：$\Sha$ 有限性

$$
\boxed{
\#\Sha(E/\mathbb Q)<\infty.
}
$$

## BSD-S：強 BSD 首項公式

若：

$$
r=\operatorname{rank}E(\mathbb Q),
$$

則：

$$
\boxed{
\frac{L^{(r)}(E,1)}{r!}
=
\frac{
\#\Sha(E/\mathbb Q)\,
\Omega_E\,
\operatorname{Reg}(E/\mathbb Q)\,
\prod_p c_p
}{
\#E(\mathbb Q)_{\mathrm{tors}}^2
}.
}
$$

不同正規化可能調整 period 等記號；研究資料必須保存所採 convention。

---

# 2. 為什麼現在值得做？

BSD 具有四個對 Agent 很有利的特徵。

## 2.1 Typed objects

```text
curve
conductor
local reduction
L-function
analytic rank
Mordell–Weil generators
Selmer group
Tamagawa numbers
regulator
torsion
Tate–Shafarevich group
```

每一項都可以有獨立 Agent、工具與驗證器。

## 2.2 低秩已有強閉包

解析秩 $0$、$1$ 的弱 BSD 已有 Gross–Zagier、Kolyvagin 與模性定理所建立的核心閉包。

這代表 Agent 不必從零發明整個理論；可以先學會辨認「哪個 theorem 套得上」。

## 2.3 可建立完整 benchmark

LMFDB 對 conductor 小於 $500{,}000$ 的 $E/\mathbb Q$ 資料是完整的，因此可建立有限、可重播的全量實驗域。

## 2.4 失敗仍可累積

即使無法證完整 BSD，仍可得到：

- theorem applicability atlas；
- 某些 $p$-part 的證書；
- twist-family 分類；
- 高秩 wall map；
- $\Sha$ prime-support 清單；
- 算法與資料品質反例；
- exact numerical certificate pipeline。

---

# 3. 真正的牆先標出來

## 3.1 高秩牆

對一般：

$$
r_{\mathrm{an}}\ge2,
$$

目前不存在一條像 rank $0/1$ 那樣普遍閉合的 Gross–Zagier–Kolyvagin 橋。

## 3.2 $\Sha$ 牆

數值 BSD 可以反推出：

$$
\#\Sha_{\mathrm{an}},
$$

但：

$$
\boxed{
\text{analytic predicted order}
\neq
\text{proved finite group order}.
}
$$

## 3.3 全 prime 統一牆

證明指定 $p$-part：

$$
\operatorname{ord}_p(\#\Sha)
$$

不等於證明所有質數的完整公式。

## 3.4 全曲線量詞牆

即使 conductor $\le500{,}000$ 全部處理，也只是有限 benchmark：

$$
\boxed{
\text{finite database closure}
\neq
\forall E/\mathbb Q.
}
$$

---

# 4. 第一主線

$$
\boxed{
\text{Strong-BSD Twist-Family Reproduction}
+
\text{BSD Certificate Atlas}
}
$$

以 2024 年 zeta-element / Iwasawa 工作與 2026 年 Banwait–Huang 算法化工作為外部基底。

第一階段不求新定理，先要求：

1. 能否重現其 hypotheses；
2. 能否在完整 conductor $\le500{,}000$ 域上再跑一次；
3. 每個判定能否輸出 machine-checkable applicability certificate；
4. 哪些 curves 被排除、原因為何；
5. 哪些條件反覆成為共同瓶頸。

---

# 5. 第二主線

$$
\boxed{
\text{High-Rank Wall Atlas}
}
$$

先以：

$$
389.a1
$$

這類 rank $2$ 曲線為樣本。

LMFDB 數值上給出完整 BSD identity，但我們必須逐項標示：

- 哪些量是 exact；
- 哪些量是 rigorous analytic computation；
- 哪些量只是 BSD 反推；
- 哪些 $\Sha$ 資訊已證；
- 哪個 theorem 不再適用。

這會比再產生一條漂亮數值等式更有研究價值。

---

# 6. 停止規則

任何路線若連續三輪只做到：

- 增加數值精度；
- 重述 BSD；
- 重新命名同一缺口；
- 在新曲線上重播相同公式；
- 以 analytic $\Sha$ 代替 actual $\Sha$；

而沒有：

- 新 theorem applicability；
- 新 exact certificate；
- 新排除域；
- 新 family；
- 新 barrier escape；

則凍結。

---

# 7. 本輪結論

BSD 不保證比 RH 更容易解。

但它更容易回答：

$$
\boxed{
\text{現在到底證到了哪一個 typed component？}
}
$$

因此它值得成為下一個正式 Agent 數學專案。
