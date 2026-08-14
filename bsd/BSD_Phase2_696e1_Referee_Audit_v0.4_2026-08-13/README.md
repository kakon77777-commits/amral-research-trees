# BSD Phase 2 — 696.e1 Adversarial Referee Audit v0.4

**日期：** 2026-08-13  
**曲線：** `696.e1` / `696b1`  
**裁決：**

$$
\boxed{\text{DERIVED THEOREM CANDIDATE}}
$$

這一版不是增加更多 candidate curves，而是專門嘗試推翻 v0.3 的 `696.e1` family。

## 敵對審查找到並修掉的一個真錯誤

v0.3 曾把「conductor <5000、rank 0/1」的既有 BSD 驗證歸得太快。

Banwait–Huang 回顧的是 Miller 驗證 **most** curves，不是 all。

真正正確的 full anchor 是：

**Creutz–Miller, Theorem 1.1**：

> 對所有 $E/\mathbf Q$，若 conductor $N<5000$ 且 analytic rank $\le1$，則 full BSD 成立。

因此 `696.e1` 的 base BSD(E,2) 仍然成立，但引用鏈已修正。

## 其餘高風險 gates

- Skinner Theorem C：明確 $p\ge3$，所以 multiplicative $p=3$ PASS。
- $p=q$ additive twist：BH Proposition 2.9 明確用 BSTW 9.21(c)；Remark 2.10 說 non-semistable 時只需顯式補 `(ramK)`。`ell=29` PASS。
- good ordinary：直接用 Skinner Theorem C，`ell=29` PASS。
- good supersingular：FW H1/H2/H3 PASS；H3 用 FW 原文對 Steinberg 的等價描述，不靠自訂 convention。
- period：FW prime 是 good supersingular；Manin constant只可能由 additive primes支撐，因此 $p$ 不整除 period discrepancy。
- Chebotarev：重新審計仍得 density $1/24$。

## 數值 sanity sweep

掃描：

$$
q<10^7
$$

得到 support primes：

$$
27,667.
$$

相對全部 primes 的比例：

$$
0.041631,
$$

理論值：

$$
1/24\approx 0.041667.
$$

這只是 implementation sanity check，不是 Chebotarev proof。

## 現在可以說什麼？

可以說：

> 現有公開 theorem 的一個具體 derived corollary candidate 是：對下述正密度 prime family 的每個 $q$，`696.e1` 的 quadratic twist by $q$ 滿足 full BSD。

目前仍**不要說「新定理」**，因 novelty search 尚未達到可發表優先權等級。

下一步應是 theorem-style paper + 獨立 referee，而不是繼續掃 curve。
