# 00｜Phase 2 全局包圍共識

## 1. 先砍掉一條假主線

Banwait–Huang Remark 2.19 明確指出：

$$
\operatorname{ord}_2(\#\Sha_{\rm an}(E))=0
$$

對所有真正走到 Algorithm 1 最後 `check_BSD_at_2` 的 LMFDB curves成立。

所以：

$$
\boxed{
\text{positive }v_2(\Sha_{\rm an})
\text{ 沒有在 current 500K eligible frontier 出現。}
}
$$

higher $2$-descent雖然一般上重要，但目前不是增加 Banwait–Huang coverage 的 bottleneck。

**裁決：HOLD / TOOLBOX ONLY。**

---

# 2. 最大的結構性 restriction 是 semistability

Banwait–Huang Remark 2.10 直接稱：

> semistable condition is a strong restriction.

其作用主要在 odd-$p$ 部分：

1. additive twist case需要 ramified-prime hypothesis；
2. irreducible ordinary case需要 ramified-prime bridge；
3. supersingular case現有 BSTW corollary帶 squarefree-conductor restriction。

另一方面：

- multiplicative case的 underlying result 本身不需要 conductor restriction；
- reducible ordinary case已有 non-semistable results；
- Burungale–Castella–Skinner 也能處理一部分 non-semistable ordinary irreducible cases；
- Fouquet–Wan直接處理 arbitrary reduction type at $p$，但 residual hypotheses 尚未算法化。

因此：

$$
\boxed{
\text{真正值得攻的是 odd-}p\text{ theorem router。}
}
$$

---

# 3. 為什麼不是 full rational 2-torsion？

Banwait–Huang Remark 2.15 明確說，現有他們使用的 $2$-part 結果沒有 full rational $2$-torsion 對應版本。

2023 以後確實有 full-$2$-torsion twist / Selmer / $\Sha[2^\infty]$ 的新研究，但目前並沒有直接提供 Banwait–Huang 所需要的那種一般 strong-BSD infinite-family replacement theorem。

所以：

$$
\boxed{
\text{full }E(\mathbb Q)[2]\cong(\mathbb Z/2)^2
}
$$

是有價值的第二線，但 theorem gap 比 non-semistable odd-$p$ route 更大。

---

# 4. 為什麼不是 analytic rank 1？

Yan–Zhu 等結果已能處理 rank $\le1$ 的更多 good-ordinary $p$-part BSD cases。

但 Banwait–Huang Remark 2.11 自己指出，rank-1 algorithmic extension仍遇到 `(Im)` 類 residual-image condition難以算法判定。

而且 rank 1 family還需要重新設計 $2$-part twist theorem與 generator/regulator層。

所以：

$$
\boxed{
\text{rank 1 = YELLOW}
}
$$

不是第一個 Phase 2 工程。

---

# 5. Phase 2 主問題

我們把研究目標寫成：

> 給定一條 non-semistable、analytic-rank-0 的 optimal elliptic curve $E/\mathbb Q$，能否把 Fouquet–Wan 的 odd-$p$ hypotheses編譯成有限、可重播、base-curve-level 的 predicates，使 Banwait–Huang 的 $2$-part twist family與 odd-$p$ full-BSD closure重新拼起來？

形式上：

$$
\boxed{
\mathrm{BH2}(E,d)
+
\forall p>2\,\mathrm{FW}(E_d,p)
\Longrightarrow
\mathrm{BSD}(E_d).
}
$$

其中：

$$
\mathrm{BH2}(E,d)
$$

表示 Theorem 2.14 的 $2$-part / nonvanishing 條件。

---

# 6. 最大的未閉合量詞

真正的難題變成：

$$
\boxed{
\forall p>2.
}
$$

不能因為：

- 大多數 $p$ 好；
- 所有 $p\le B$ 好；
- residual representation generically surjective；

就偷偷換成完整 BSD。

Phase 2 必須找到：

$$
\boxed{
\text{finite exceptional-prime reduction}
}
$$

或者承認此 route只能給「固定 finite prime set的 p-part theorem」。

---

# 7. 當前 verdict

$$
\boxed{
\text{GO：Fouquet–Wan Hypothesis Compiler}
}
$$

$$
\boxed{
\text{STOP：直接 higher }2\text{-descent主線}
}
$$

$$
\boxed{
\text{HOLD：full rational 2-torsion / rank 1}
}
$$
