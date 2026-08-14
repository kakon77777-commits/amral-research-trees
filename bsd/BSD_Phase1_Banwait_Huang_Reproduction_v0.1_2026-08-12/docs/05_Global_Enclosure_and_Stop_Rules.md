# 05｜全局包圍與停止規則

## 這條路即使完全成功，能證什麼？

Banwait–Huang Algorithm 1 成功時，證明：

> 該 base curve有一個明確、可有效枚舉的無限 quadratic-twist subfamily，其成員由既有定理保證 strong BSD。

它不證明：

1. base curve的所有 twists都滿足 BSD；
2. 未通過 Algorithm 1 的 base curve沒有 strong-BSD twists；
3. 所有 elliptic curves都有這種 family；
4. 完整 BSD 對所有 $E/\mathbb Q$ 成立。

因此本路線屬於：

$$
\boxed{
\text{Uniform infinite-family theorem}
}
$$

而不是：

$$
\boxed{
\forall E/\mathbb Q.
}
$$

---

# Phase 1 的全球價值

即使不解完整 BSD，它仍能產生：

- theorem applicability atlas；
- curve family certificates；
- descent soundness audit；
- data / theorem separation；
- twist generator；
- external result reproduction。

這屬於高累積性工作。

---

# 停止規則

若連續三輪只做到：

- 增加 twist bound；
- 多列一些 $d$；
- 重算同一批 curves；
- 只調整 runtime；
- 沒有新 theorem predicate或 certificate；

則凍結。

只有以下變化可延長主線：

1. 新 theorem family；
2. 新 descent certificate；
3. 新 eligibility criterion；
4. discrepancy / bug with mathematical consequence；
5. 對作者結果的獨立全域重現；
6. 將 family coverage真正擴到新類型曲線。
