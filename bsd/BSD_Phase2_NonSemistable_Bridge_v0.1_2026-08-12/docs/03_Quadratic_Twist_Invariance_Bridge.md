# 03｜Quadratic-Twist Invariance Bridge

## 0. 目的

Fouquet–Wan theorem是對單一：

$$
E_d,\ p
$$

說的。

Banwait–Huang需要的是：

$$
\text{一個 base }E
\Longrightarrow
\text{無限多 }d.
$$

所以必須把 FW hypotheses從 twist層降回 base層。

---

# 1. Residual representation under quadratic twist

對 odd $p$：

$$
\bar\rho_{E_d,p}
\cong
\bar\rho_{E,p}\otimes\chi_d.
$$

其中：

$$
\chi_d:G_\mathbb Q\to\{\pm1\}\subset\mathbb F_p^\times.
$$

---

# 2. Candidate Lemma A — irreducibility invariance

tensor by a 1-dimensional character是 category auto-equivalence。

因此：

$$
\boxed{
\bar\rho_{E,p}\text{ absolutely irreducible}
\iff
\bar\rho_{E_d,p}\text{ absolutely irreducible}.
}
$$

這一項可完全 base-curve化。

---

# 3. Candidate Lemma B — local semisimplification degeneracy invariance

若 FW-H2 排除的是：

$$
\bar\rho|_{G_{\mathbb Q_p}}^{ss}
\cong
\bar\chi
\oplus
\bar\chi_{\rm cyc}\bar\chi
$$

型態，則 twist後：

$$
(\bar\rho\otimes\chi_d)^{ss}
\cong
(\bar\chi\chi_d)
\oplus
\bar\chi_{\rm cyc}(\bar\chi\chi_d).
$$

所以「存在某個 common character $\bar\chi$ 使其落入禁型」應保持不變。

若使用 FW simplified theorem還排除其他 equal-character case，同樣需逐項證 twist-invariance。

**狀態：標準表示論推導候選；正式文件需逐 theorem version核對。**

---

# 4. Candidate Lemma C — split-at-$\ell$ local preservation

Banwait twist條件要求 base conductor primes在：

$$
K_d=\mathbb Q(\sqrt d)
$$

中 split。

若：

$$
\ell\mid N
$$

split in $K_d$，則 quadratic character在：

$$
G_{\mathbb Q_\ell}
$$

上 trivial。

因此：

$$
\boxed{
\bar\rho_{E_d,p}|_{G_{\mathbb Q_\ell}}
\cong
\bar\rho_{E,p}|_{G_{\mathbb Q_\ell}}.
}
$$

所以任何以該 $\ell$ 作 witness 的 FW-H3 local certificate可以沿整個 admissible twist family保留。

---

# 5. Bridge 結果

若 A/B/C 全部形式化，則對固定 $p$：

$$
\boxed{
\mathrm{FW}(E,p)
\Longrightarrow
\mathrm{FW}(E_d,p)
}
$$

對所有滿足相應 splitting conditions 的 Banwait admissible twists成立。

這非常重要：

> 我們不必對無限多 $d$ 重跑 residual representation theorem。

只需對 base curve建立：

```text
FW certificate at p
```

---

# 6. 尚未解決

即使把 $d$ 量詞壓掉，仍有：

$$
\forall p>2.
$$

所以這個 bridge只解決：

$$
\forall d
$$

的一部分，沒有解決全部 prime quantifier。
