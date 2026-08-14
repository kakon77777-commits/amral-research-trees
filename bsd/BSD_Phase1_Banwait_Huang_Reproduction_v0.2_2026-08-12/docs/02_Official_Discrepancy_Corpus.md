# 02｜官方 discrepancy corpus

官方 repository 保存了一份專門的診斷報告，對四條曲線逐 predicate 解釋為什麼現行 Algorithm 1 拒絕它們：

$$
62a1,\quad66b1,\quad105a1,\quad141c1.
$$

四條共同通過 semistability、isogeny exclusion、ramification、optimality、rank-zero gate、$E'$ 的 $2$-descent gate與現行 $\operatorname{BSD}(E,2)$ gate。

共同失敗：

1. $\operatorname{ord}_2 L^{alg}=-2$，但 CLZ20 要求 $-1$；
2. $E'(\mathbb Q)_{\mathrm{tors}}$ 的 $2$-torsion structure 為 $(2,2)$，不符合所需 cyclic condition；
3. $f'(x_0)$ 是 rational square；
4. $\mathcal S$ nonempty gate失敗。

這份資料應被視為：

$$
\boxed{
\text{theorem-router adversarial regression corpus}.
}
$$

未來若某版本突然接受這四條，第一個標籤應是 `REGRESSION?`，不是 `NEW BSD BREAKTHROUGH!`。
