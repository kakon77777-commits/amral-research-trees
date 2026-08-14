# 19｜Independent Referee / Local Agent Handoff

## Goal

不要再搜尋更多 curves。

先嘗試推翻：

> `696.e1` family theorem.

---

# Referee A — Theorem 2.14

對：

$$
E=[0,1,0,8,-16]
$$

逐項確認：

```text
optimal
odd Manin
analytic rank 0
BSD(E,2) rigorous source
E(Q)[2]=0
Delta<0
v2(Lalg)=0
```

再對 symbolic $q\in\mathcal P$ 驗：

```text
squarefree
gcd(q,696)=1
q mod 4 = 1
2,3,29 split in Q(sqrt(q))
q inert in 2-division cubic
```

輸出 PASS/FAIL。

---

# Referee B — Odd ordinary/additive branches

只使用 Banwait–Huang Remark 2.10明確允許的 non-semistable replacement：

```text
semistability used only to manufacture ramified witness
```

逐 branch確認 witness $3$ / $29$ 的 theorem hypotheses。

---

# Referee C — Fouquet–Wan

優先使用 FW Theorem 1.1 的 stronger but simpler sufficient hypotheses，而不是自行改寫最一般 Theorem 1.7。

對 arbitrary good supersingular $p$ 驗：

```text
absolute irreducibility
local forbidden semisimplifications impossible
ell=29
ell||N(E_q)
dim E_q[p]^I_29 = 1
dim E_q[p]^G_Q29 = 0
```

尤其檢查：

```text
nonsplit multiplicative
<=>
FW nontrivial unramified quadratic Steinberg twist
```

---

# Referee D — Period

證明對 FW 使用的 good supersingular $p$：

```text
p does not divide Manin-period discrepancy
```

優先引用 published Manin-constant results，不依賴 unpublished Edixhoven remark。

---

# Referee E — Chebotarev

獨立重算：

```text
disc(f2) = -11136
Gal = S3
quadratic resolvent = Q(sqrt(-174))
K = Q(zeta_24, sqrt(29))
L intersect K = Q(sqrt(-174))
[LK:Q] = 48
class size = 2
density = 1/24
```

---

# Referee F — Search for counterexample prime

寫程式至少掃：

$$
q<10^7
$$

所有 $\mathcal P$ primes。

對每個：

```text
a_q odd
ordinary
all splitting predicates
f2 irreducible
```

任何 mismatch都立即 FAIL。

數值 sweep不是 theorem proof，只是找 implementation/case bug。

---

# Stop rule

若 Referee A–E 全 PASS：

```text
upgrade to DERIVED THEOREM / PREPRINT CANDIDATE
```

若任何一項 FAIL：

```text
freeze scaling
return to exact failed lemma
```
