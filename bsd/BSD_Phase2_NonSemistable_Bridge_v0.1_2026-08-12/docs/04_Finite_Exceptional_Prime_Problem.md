# 04｜Finite Exceptional Prime Problem

## Mother problem

對 fixed non-CM elliptic curve $E/\mathbb Q$：

$$
\boxed{
\forall p>2,\quad \mathrm{FW}(E,p)
}
$$

如何變成 finite certificate？

---

# 1. H1 的 finite nature

absolute reducibility：

$$
\bar\rho_{E,p}\text{ reducible}
$$

對 $E/\mathbb Q$ 等價於存在 rational $p$-isogeny類型的 residual stable line。

這只會發生在有限質數。

對實際 pipeline，應由：

- LMFDB isogeny/Galois-image metadata；
- Sage isogeny class；
- 已知 rational isogeny theorem；

產生 finite set：

$$
P_{\rm red}(E).
$$

---

# 2. H3 的 finite-exception heuristic

若某 multiplicative：

$$
\ell\parallel N
$$

可作 witness，residual ramification常與：

$$
p\nmid v_\ell(\Delta_E)
$$

相關。

因此 fixed $\ell$ 只會被：

$$
p\mid v_\ell(\Delta_E)
$$

的有限質數破壞。

若有多個 $\ell$ candidates，可形成：

$$
P_{\rm ram}(E)
=
\bigcap_{\ell\in W(E)}
\{p:p\mid v_\ell(\Delta_E)\}
$$

類型的 finite obstruction set。

**注意：Fouquet–Wan H3比 ramification alone更細；此式只能作 compiler heuristic，不能直接當 theorem。**

---

# 3. H2 是目前最不清楚的部分

local degeneracy at $p$ 的 failure是否可化成：

- congruence on $a_p$；
- local reduction type；
- finite exceptional set；

需要正式推導。

所以 Phase 2 第一個真正 algebraic task：

$$
\boxed{
\text{derive FW-H2 for weight-2 elliptic curves in explicit local terms}.
}
$$

---

# 4. 成功標準

找到一個 theorem：

$$
p\notin
P_{\rm red}(E)
\cup
P_{\rm loc}(E)
\cup
P_{\rm ram}(E)
\Longrightarrow
\mathrm{FW}(E,p),
$$

其中右側三個集合都：

- finite；
- effectively computable；
- certificate-producing。

此時 full odd-prime part變成有限驗證。

---

# 5. 失敗標準

若 FW-H2 / H3 的 exact condition需要對無限多 $p$ 做不可壓縮 local Galois computation，且無 generic-large-$p$ theorem：

$$
\boxed{
\text{route remains a per-prime theorem, not full-BSD family closure}.
}
$$

此時必須降級，不得用「tested up to $B$」替代全稱量詞。
