# 02｜Fouquet–Wan Hypothesis Compiler

## 0. 目標

Fouquet–Wan 對 modular motives證明 arbitrary-reduction Iwasawa Main Conjecture，並在 weight $2$ / elliptic-curve情形給出 $p$-part BSD corollary。

Banwait–Huang 已指出這可以用於 non-semistable extension，但：

> it is not immediately apparent how to algorithmically verify these conditions.

所以本文件把它變成正式 compiler 問題。

---

# 1. Compiler Level 0：使用較強但較易實作的 sufficient theorem interface

先以 Fouquet–Wan Introduction 的 sufficient hypothesis package為目標，而不是第一輪就編譯最一般 deformation-theoretic版本。

對每個 odd prime $p$，保存：

## FW-H1 — Absolute irreducibility

$$
\bar\rho_{E,p}
$$

絕對不可約。

對 $E/\mathbb Q$：

- reducible $\bar\rho_{E,p}$ 與 rational $p$-isogeny 密切相關；
- production implementation應使用 Sage/LMFDB Galois-image/isogeny metadata，而不是自己用少量 Frobenius traces猜。

狀態：

```text
EXACT / THEOREM
```

---

## FW-H2 — Local residual non-degeneracy at $p$

需要排除 Fouquet–Wan theorem中指定的 local semisimplification degeneracy。

資料介面：

```text
p
reduction_type_at_p
a_p
local_residual_representation
semisimplification_type
fw_local_degenerate
```

第一輪**不得**用：

```text
a_p != something
```

自行猜等價條件。

必須：

1. 從 theorem / local representation formalism推導；
2. 再編譯成 finite-field/local-Galois predicate。

這是 compiler 的第一個真正數學子問題。

---

## FW-H3 — Auxiliary multiplicative prime $\ell$

需要存在：

$$
\ell\ne p,\qquad \ell\parallel N
$$

且 residual local representation滿足 theorem指定的 ramified-extension / fixed-space條件。

推薦先建立：

```text
ell
ord_ell(N)
ord_ell(Delta_min)
split_multiplicative?
nonsplit_multiplicative?
rho_bar_ramified?
dim_inertia_invariants
dim_local_invariants
```

Banwait 的 semistable路線用：

$$
p\nmid\operatorname{ord}_\ell(\Delta_E)
$$

作 residual ramification criterion。

但 Fouquet–Wan 的 exact local condition更細，不能直接把這一條當完整 H3。

---

# 2. Compiler Level 1：base curve → prime certificate

每個 $(E,p)$ 輸出：

```json
{
  "curve": "...",
  "p": 5,
  "H1_absolute_irreducible": "PASS|FAIL|UNKNOWN",
  "H2_local_nondegenerate": "PASS|FAIL|UNKNOWN",
  "H3_auxiliary_prime": "PASS|FAIL|UNKNOWN",
  "witness_ell": null,
  "claim": "FW_APPLICABLE|FW_NOT_APPLICABLE|UNKNOWN"
}
```

---

# 3. Compiler Level 2：prime quantifier compression

對 fixed $E$，目標不是掃 $p<1000$ 然後說完成。

需要建立：

```text
generic_large_prime theorem
+
finite exceptional prime list
```

形式：

$$
\exists P_E\text{ finite}:
\quad
p\notin P_E
\Longrightarrow
\mathrm{FW}(E,p).
$$

再對：

$$
p\in P_E
$$

逐項 exact check。

如果做不到，就只能輸出：

```text
FW verified for tested primes
```

不能升級 full BSD。

---

# 4. 最有價值的第一個 compiler theorem

理想成果不是一百萬曲線 count，而是一個標準語言 lemma：

> 對某一明確 elliptic-curve class，FW-H1/H2/H3 對所有 odd primes except a computable finite set自動成立。

然後：

$$
\boxed{
\text{infinite prime quantifier}
\to
\text{finite certificate}.
}
$$

這才是真正的 Phase 2 數學推進。
