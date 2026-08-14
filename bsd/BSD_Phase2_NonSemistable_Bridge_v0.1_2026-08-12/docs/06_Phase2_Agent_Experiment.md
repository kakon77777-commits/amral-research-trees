# 06｜Phase 2 第一個 Agent 實驗

## Experiment name

`FW-Hypothesis-Compiler / Weight-2 Elliptic Curves`

---

# Step 1 — 不掃全庫

先挑：

```text
20 semistable known-pass curves
20 non-semistable analytic-rank-0 curves
20 deliberately bad/control curves
```

只為 compiler correctness，不為統計。

---

# Step 2 — 每條曲線建立 local prime table

先取：

$$
p\in\{3,5,7,11,13,17,19,23,29,31,37\}
$$

加上：

- rational isogeny primes；
- bad reduction primes；
- prime divisors of all $v_\ell(\Delta_E)$。

這只是測試集，不是 full quantifier closure。

輸出：

```text
curve
p
reduction_type
a_p
residual_irreducible
local_ss_type
FW_H2
candidate_ell
FW_H3
evidence
```

---

# Step 3 — H2 symbolic derivation

單獨 Agent：

> 將 Fouquet–Wan local semisimplification prohibition specialised to weight-2 elliptic curves，分 good ordinary / supersingular / multiplicative / additive reduction，推成可計算的 local criteria。

輸出不是 code先，而是：

```text
lemma
proof
allowed assumptions
counterexamples
Sage predicate
```

---

# Step 4 — H3 symbolic derivation

單獨 Agent：

> 將 Fouquet–Wan auxiliary $\ell$ condition specialised to elliptic curves and compare with Banwait's residual-ramification criterion $p\nmid v_\ell(\Delta_E)$.

目標：

```text
exact equivalence
or
strict implication
or
not equivalent
```

不得默認相同。

---

# Step 5 — twist invariance proof

形式化三個 bridge lemmas：

```text
absolute irreducibility invariant
FW-H2 bad type invariant
split-local FW-H3 witness invariant
```

最好可以 Lean / theorem-style prose雙輸出。

---

# Step 6 — finite exceptional prime theorem search

Agent 搜索／證明：

```text
for fixed E, which p can fail H1?
which p can fail H2?
which p can fail H3?
```

輸出：

$$
P_E^{\rm candidate}
$$

但若無 theorem保證完整，不得標 complete。

---

# Step 7 — only then database census

Compiler通過後才掃：

$$
895{,}988
$$

左右的 non-semistable analytic-rank-0 search pool。

第一個 database輸出應是：

```text
FW_COMPILER_PASS
FW_COMPILER_FAIL
FW_COMPILER_UNKNOWN
```

UNKNOWN不可吞掉。

---

# 成功 Gate

Phase 2 v0.1 成功不需要找到新 curve。

只要：

1. H2 exact specialisation完成；
2. H3 exact specialisation完成；
3. twist-invariance lemmas完成；
4. finite-prime reduction至少在一個 nontrivial curve class成立。

這已經是新的標準語言數學結果。
