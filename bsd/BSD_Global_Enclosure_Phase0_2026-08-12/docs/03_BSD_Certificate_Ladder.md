# 03｜BSD Certificate Ladder

## 原則

每一條曲線都不能只存一個布林值：

```text
BSD true / false
```

而要存「哪一層已被什麼證書關閉」。

---

# C0 — Identity

- minimal Weierstrass model；
- $\mathbb Q$-isomorphism / isogeny label；
- conductor；
- discriminant；
- CM status；
- source provenance。

---

# C1 — Local arithmetic

- bad primes；
- reduction type；
- Tamagawa numbers；
- torsion；
- root number；
- Galois representation metadata。

---

# C2 — Numerical analytic rank

高精度計算顯示：

$$
r_{\mathrm{an}}=r.
$$

但未必有 rigorous zero-order certificate。

狀態：

```text
evidence
```

---

# C3 — Rigorous analytic rank

以可審計的 $L$-function 算法、interval arithmetic、Turing-type count 或 theorem證明：

$$
\operatorname{ord}_{s=1}L(E,s)=r.
$$

---

# C4 — Algebraic lower bound

找到 $r$ 個獨立 rational points：

$$
r_{\mathrm{alg}}\ge r.
$$

需保存：

- generators；
- canonical heights；
- height-pairing matrix；
- independence certificate。

---

# C5 — Algebraic upper bound

由 descent / Selmer：

$$
r_{\mathrm{alg}}\le r.
$$

需保存：

- $n$-Selmer group；
- local conditions；
- saturation；
- descent implementation。

此時：

$$
r_{\mathrm{alg}}=r.
$$

---

# C6 — Weak BSD certificate

同時有：

$$
r_{\mathrm{alg}}=r_{\mathrm{an}}.
$$

可以來自：

- rank $0/1$ theorem；
- 曲線級 analytic + algebraic certificates；
- family theorem。

---

# C7 — Single-prime strong BSD

對指定 $p$，證明首項公式的 $p$-part。

保存：

```text
p
reduction
Selmer structure
main-conjecture theorem
local factors
valuation equality
assumptions
```

---

# C8 — $\Sha$ finite and exact

獨立證明：

$$
\Sha(E/\mathbb Q)
$$

有限，並確定：

$$
\#\Sha.
$$

不能使用 BSD 反推值當作證明。

---

# C9 — Full strong BSD

所有 component 已閉合：

$$
\frac{L^{(r)}(E,1)}{r!}
=
\frac{
\#\Sha\Omega\operatorname{Reg}\prod c_p
}{
\#E_{\mathrm{tors}}^2
}.
$$

需明示：

- exact / certified numerical equality；
- convention；
- Manin constant / period normalization；
- all prime parts；
- no unproved assumptions。

---

# C10 — Family theorem

對一個無限 family：

$$
\{E_t\}_{t\in T}
$$

建立 uniform theorem。

要保存：

- parameter domain；
- exceptional set；
- local hypotheses；
- whether all or positive proportion；
- whether weak or strong BSD。

---

# 證書狀態字典

```text
unknown
numerical
conditional
theorem_applicable
proved_component
proved_curve
proved_family
refuted_data
```

---

# 絕對禁止

1. `analytic_sha` 寫成 `proved_sha`；
2. `rank()` 回傳一個整數就當成有完整 proof；
3. 某個 $p$-part 成立就標 full strong BSD；
4. rank $0/1$ theorem 套到 rank $2$；
5. LMFDB data completeness當成 BSD completeness。
