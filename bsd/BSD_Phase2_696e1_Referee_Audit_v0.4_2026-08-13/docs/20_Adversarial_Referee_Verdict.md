# 20｜Adversarial Referee Verdict

## Verdict

經逐 source audit，v0.3 的主要 proof router沒有被打死。

但 referee 確實抓出一個引用錯誤：

$$
\boxed{
\text{Miller ``most''}\neq\text{all conductor}<5000.
}
$$

這一點由 Creutz–Miller Theorem 1.1 修復。

目前沒有剩下已知的 mathematical branch gap。

因此 claim level 從：

```text
PROVISIONAL DERIVED FAMILY THEOREM
```

升到：

```text
DERIVED THEOREM CANDIDATE
```

但不升到：

```text
NEW THEOREM
```

因為 novelty 是另一個獨立 Gate。

---

# Referee principles

本輪強制區分：

1. theorem statement；
2. source-author remark；
3. our derived lemma；
4. LMFDB arithmetic certificate；
5. numerical sanity check；
6. novelty inference。

只要一項來源不支持，就不能用下一層替它補洞。
