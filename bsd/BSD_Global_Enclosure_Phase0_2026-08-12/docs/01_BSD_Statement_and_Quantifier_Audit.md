# 01｜BSD 命題、量詞與例外忠實性審計

## 1. 基本對象

取一條定義於 $\mathbb Q$ 的橢圓曲線：

$$
E:\quad y^2+a_1xy+a_3y=x^3+a_2x^2+a_4x+a_6.
$$

Mordell–Weil 定理給：

$$
E(\mathbb Q)
\cong
E(\mathbb Q)_{\mathrm{tors}}
\oplus
\mathbb Z^{r_{\mathrm{alg}}}.
$$

其中：

$$
r_{\mathrm{alg}}
=
\operatorname{rank}E(\mathbb Q).
$$

相應 $L$-函數在 $s=1$ 的消失階：

$$
r_{\mathrm{an}}
=
\operatorname{ord}_{s=1}L(E,s)
$$

稱為解析秩。

---

# 2. 三層主張不能混寫

## 2.1 弱式

$$
r_{\mathrm{alg}}=r_{\mathrm{an}}.
$$

## 2.2 有限性

$$
\Sha(E/\mathbb Q)
$$

有限。

## 2.3 首項公式

$$
\frac{L^{(r)}(E,1)}{r!}
=
\frac{
\#\Sha\,
\Omega_E\,
\operatorname{Reg}_E\,
\prod_pc_p
}{
\#E(\mathbb Q)_{\mathrm{tors}}^2
}.
$$

可能發生：

- 秩等式已證；
- $\Sha$ 有限性只有部分質數；
- 數值首項吻合；
- 完整強式仍未證。

所以資料庫不能只有一個：

```json
{"bsd": true}
```

---

# 3. 全域量詞

完整 BSD over $\mathbb Q$ 是：

$$
\boxed{
\forall E/\mathbb Q,\quad
\mathrm{BSD\text{-}W}(E)
\land
\mathrm{BSD\text{-}F}(E)
\land
\mathrm{BSD\text{-}S}(E).
}
$$

其例外單位是一條具體曲線。

任何「正比例曲線成立」「平均 rank 低」「幾乎所有 twist 成立」都不能吞掉一條真正例外。

---

# 4. 三種反例型態

## 4.1 Rank mismatch

$$
r_{\mathrm{alg}}\ne r_{\mathrm{an}}.
$$

## 4.2 Infinite $\Sha$

即使 rank equality 成立，仍可能：

$$
\#\Sha=\infty.
$$

## 4.3 Leading coefficient mismatch

即使 rank equality 與有限性成立，仍可能首項公式不符。

因此：

$$
\boxed{
\text{弱 BSD 成立}
\not\Rightarrow
\text{強 BSD 成立}.
}
$$

---

# 5. $p$-part 與完整公式

對某質數 $p$ 證明強 BSD 的 $p$-part，通常表示首項公式兩側的 $p$-adic valuation 相符，連同相應 Selmer / Iwasawa 控制。

但：

$$
\boxed{
\forall p\text{ 的統一控制}
}
$$

與：

$$
\boxed{
\text{固定 }p\text{ 的 theorem}
}
$$

是不同量詞。

Agent 必須保存：

```text
prime p
reduction type
ordinary / supersingular
Eisenstein / non-Eisenstein
local hypotheses
main-conjecture status
p-converse status
```

---

# 6. Isogeny-class 層級

弱 BSD 的 rank 與 $L$-函數在 isogeny class 中保持一致。

強 BSD 公式的各項可能在 isogenous curves 間改變，但整體預言具有相容性。

因此 Phase 1：

- theorem routing 以 isogeny class 為主；
- local invariant / exact formula 以 curve 為主；
- 不應把同一 isogeny class 的多條曲線當成獨立全域樣本。

---

# 7. 數值證據的正確地位

LMFDB 顯示的：

$$
\Sha_{\mathrm{an}}
=
\frac{
L^{(r)}(E,1)
\#E(\mathbb Q)_{\mathrm{tors}}^2
}{
r!\,
\Omega_E
\operatorname{Reg}_E
\prod_pc_p
}
$$

是由 BSD 公式反推出的 analytic prediction。

它可以用於：

- 偵測資料異常；
- 尋找非平凡 $\Sha$ 候選；
- 測試算法；
- family statistics。

但不能在沒有獨立 descent / cohomological proof 時，標成：

$$
\#\Sha(E/\mathbb Q)\text{ 已證}.
$$

---

# 8. 全局審計結論

BSD 比 RH 比例路線更適合 Faithful Globalizer，因為每條曲線都是明確原子。

但仍要避免：

$$
\boxed{
\text{大資料庫全部吻合}
\to
\text{所有曲線成立}.
}
$$

Phase 1 的 global object應衡量「認證前沿」，而不是偽裝成真值前沿。
