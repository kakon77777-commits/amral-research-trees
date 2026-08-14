# 02｜論文 pseudocode 與目前官方程式審計

## 0. 結論

目前 GitHub 實作不是單純照抄 paper pseudocode。

它已加入數個重要的證書強度修正，尤其是：

$$
\boxed{
\operatorname{BSD}(E,2)\text{ 的防過度宣稱 gate}.
}
$$

---

# 1. $2$-descent 到底能證什麼？

2-descent直接控制的是：

$$
\dim_{\mathbb F_2}\Sha(E)[2],
$$

不是一般情況下的：

$$
\operatorname{ord}_2\#\Sha(E).
$$

因為即使：

$$
\dim_{\mathbb F_2}\Sha[2]=2,
$$

仍可能有：

$$
\Sha[2^\infty]\cong(\mathbb Z/4\mathbb Z)^2,
$$

此時：

$$
\operatorname{ord}_2\#\Sha=4.
$$

因此目前官方 `check_BSD_at_2` 採取：

```text
sha_an_ord_2 != 0
→ reject / False
```

只有在：

$$
\operatorname{ord}_2\#\Sha_{\mathrm{an}}=0
$$

且 descent 嚴格得到：

$$
\Sha[2]=0
$$

時，才接受：

$$
\operatorname{BSD}(E,2).
$$

這與 paper Remark 2.19 的警告一致：

> 正 analytic 2-adic valuation時需要更高 $2$-power descent。

---

# 2. $E'$ 的條件也被硬化

CLZ20 branch 要求：

$$
\Sha(E')[2]=0.
$$

目前程式雖然會讀取：

$$
\Sha_{\mathrm{an}}(E'),
$$

但只把它當 descent gate 的輸入。

真正接受的條件是：

$$
\operatorname{ord}_2\Sha_{\mathrm{an}}(E')=0
$$

且 2-descent pins：

$$
\dim\Sha(E')[2]=0.
$$

因此 analytic value沒有被直接冒充 actual group order。

---

# 3. Descent backend

目前程式依序嘗試：

1. PARI 2-descent；
2. mwrank；
3. Sage native 2-isogeny descent。

mwrank 因可能卡住，被放入 forked process並設 wall-clock timeout。

這不是數學內容，但對大規模可重現性非常重要。

---

# 4. $\mathcal S\ne\varnothing$ 的 deterministic criterion

論文 Proposition 2.16 給一個代數判準。

目前程式預設使用 deterministic filter，而不是只搜尋：

$$
q\le10000
$$

的 witness。

bounded prime search仍保留作交叉驗證／測試，但不再是主證書。

---

# 5. Soundness-sensitive flags

目前程式明確將以下選項標為 testing only：

```text
skip_filter_S
skip_BSD_at_2_check
```

啟用後的輸出不能再稱作完整 theorem-qualified curves。

本地 Agent 必須把這些 flags 寫入 metadata，不能只保存結果清單。

---

# 6. Paper / repository 格式漂移

論文文字與 repository 當前輸出格式略有演化，例如 twist output 目前為 JSON。

這不影響 theorem，但重現工作必須鎖定：

```text
paper version
repository commit / file SHA
Sage version
LMFDB release
runtime flags
```

---

# 7. 一個仍需 Phase 1 v0.2 審計的點

Theorem 2.18 的條件是：

$$
\text{analytic rank}=0.
$$

Algorithm 1 程式初始 dataframe 使用 LMFDB `rank` 欄位，再透過非零 special value與 $L^{alg}$ 條件實際排除中心消失。

完整重現時仍應顯式保存：

```text
algebraic rank field
analytic rank field
special value nonvanishing
proof/evidence type
```

避免把兩種 rank 靜默混為同一欄。
