# 06｜Phase 1 Agent 實驗規格
## BSD Certificate Atlas + Strong-BSD Twist-Family Reproduction

## 0. 目標

不是：

> 對幾百萬條曲線計算一個 BSD 比值。

而是：

> 對完整有限域中的每個 isogeny class，生成 theorem-applicability、證書層級與未閉合項。

---

# 1. Benchmark domain

第一批：

$$
\boxed{
N_E<500{,}000
}
$$

的一個 isogeny-class representative。

理由：LMFDB 對此 conductor 範圍完整。

資料外的曲線可做 extension set，但必須標：

```text
database_completeness = partial
```

---

# 2. 工作流

## Step A — Ingest

抓取：

```text
LMFDB label
Cremona label
a-invariants
conductor
discriminant
rank
analytic rank
root number
torsion
regulator
Tamagawa factors
CM
semistable
Galois image metadata
Sha_an
```

## Step B — Evidence typing

每個欄位加：

```text
exact
rigorous_computation
numerical
BSD_inferred
unknown
```

## Step C — Theorem router

逐條檢查：

- Gross–Zagier–Kolyvagin；
- BSTW zeta-element hypotheses；
- Banwait–Huang algorithmic criteria；
- ordinary / supersingular main conjecture；
- Eisenstein-prime p-converse；
- CM-specific results；
- twist-family conditions。

每個判定輸出：

```json
{
  "theorem": "...",
  "applicable": true,
  "verified_hypotheses": [],
  "failed_hypotheses": [],
  "unknown_hypotheses": [],
  "source": "...",
  "claim_scope": "weak BSD / p-part / strong BSD family"
}
```

## Step D — Certificate level

依 `03_BSD_Certificate_Ladder.md` 標 C0–C10。

## Step E — Wall classification

未閉合原因只能選受控 vocabulary：

```text
analytic_rank_not_rigorous
algebraic_rank_upper_bound_open
generator_saturation_open
sha_finiteness_open
sha_p_part_open
all_prime_unification_open
local_hypothesis_failed
residual_representation_unknown
high_rank_bridge_missing
normalization_or_data_issue
```

---

# 3. 三組測試

## Group R0

rank $0$ curves。

目的：

- 測 weak BSD 已知 theorem；
- 測 strong BSD $p$-parts；
- 測 analytic $\Sha$ 與 actual proof分離。

## Group R1

rank $1$ curves。

目的：

- Heegner point / Kolyvagin applicability；
- regulator與 generator saturation；
- p-converse。

## Group R2+

rank $\ge2$ curves。

目的：

- 不求全面閉合；
- 找 theorem coverage突然下降的位置；
- 建 high-rank dependency DAG。

---

# 4. 第一個 rank-2 wall sample

$$
389.a1:
\quad
y^2+y=x^3+x^2-2x.
$$

LMFDB 給：

$$
r_{\mathrm{alg}}=r_{\mathrm{an}}=2,
$$

以及數值：

$$
\frac{L^{(2)}(E,1)}{2!}
\approx
0.7593165002884.
$$

右側使用：

$$
\Omega\approx4.9804251217,
$$

$$
\operatorname{Reg}\approx0.15246017794,
$$

$$
\prod c_p=1,
\qquad
\#E_{\mathrm{tors}}=1,
$$

得到同一數值。

Agent 的任務不是再算一次，而是回答：

1. rank $2$ equality 的證書來源是什麼？
2. generators 是否 saturated？
3. analytic rank是否 rigorous？
4. $\Sha_{\mathrm{an}}=1$ 是否 actual proof？
5. 哪些 $p$-parts已知？
6. 完整 strong BSD status到底是哪一級？

---

# 5. 第一個 family reproduction

以 Banwait–Huang 2026 為規格：

> 找出 conductor $\le500{,}000$ 中，哪些曲線符合已知 theorem，因而具有無限多 quadratic twists satisfying strong BSD。

要求：

1. 重建 paper algorithm；
2. 將每個 criterion翻成 predicate；
3. 以小樣本和作者結果比對；
4. 全域重跑；
5. 保存版本、程式、原始資料與 hash；
6. 對 discrepancy 做 adversarial audit。

---

# 6. 成功條件

Phase 1 不要求新 BSD theorem。

只要完成以下五項即成功：

1. 完整 schema；
2. 至少三類曲線的證書；
3. Banwait–Huang 算法可重現；
4. 每個結果能區分 evidence / theorem；
5. 找到高秩前三大共同瓶頸。

---

# 7. 失敗／凍結條件

若 Agent：

- 只抄 LMFDB；
- 只算數值比；
- 無法追溯 theorem hypotheses；
- 將 analytic $\Sha$ 當 actual $\Sha$；
- 無法分辨 weak / strong / p-part；

則本輪不算有效研究。
