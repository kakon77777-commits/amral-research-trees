# BSD Phase 2 — LMFDB Exact Census Compiler v0.5

**日期：** 2026-08-14  
**狀態：** `READY FOR LOCAL SQL EXECUTION`  
**目的：** 停止逐 curve 手工搜尋；將 Phase 2 non-semistable BSD family criterion 編譯成 LMFDB 全庫 exact census。

---

## 一句話

這一版不宣稱「找到多少條曲線」。

它做的是更重要的事：

\[
\boxed{
\text{theorem gates}
\longrightarrow
\text{SQL universe}
\longrightarrow
\text{exact witness graph}
\longrightarrow
\text{finite pending certificates}.
}
\]

本包故意把不能由 LMFDB 靜態資料直接證明的項目保留成：

```text
BSD2_BASE_PENDING
FIXED_ADDITIVE_H2_PENDING
FINITE_ORDINARY_EXCEPTION_PENDING
```

而不是用 analytic/numerical data冒充 theorem certificate。

---

# 1. LMFDB access

LMFDB 官方提供 read-only PostgreSQL mirror：

```text
host     = devmirror.lmfdb.xyz
port     = 5432
dbname   = lmfdb
user     = lmfdb
password = lmfdb
```

本 census 使用：

```text
ec_curvedata
ec_mwbsd
ec_localdata
```

必要時後續加入：

```text
ec_galrep
```

---

# 2. Cheap gate order

第一層 SQL 只做低成本高殺傷力條件：

```text
analytic rank = 0
algebraic rank = 0
torsion = 1
optimality = 1
non-semistable
analytic Sha = 1
Tamagawa product odd
Manin constant odd
```

這些條件的用途是建立：

```text
NUMERIC_2PART_PARITY_PASS
```

不是：

```text
BSD(E,2) PROVED.
```

---

# 3. Edixhoven-safe odd additive gate

第一個 theorem-ready census pool要求：

```text
at least one odd additive prime
all odd additive primes p >= 11
kodaira_symbol NOT IN (2,3,4)
```

在 LMFDB `ec_localdata` 對 \(p\ge5\) 的編碼中：

```text
2 = II
3 = III
4 = IV
-1 = I0*
```

因此這是一個保守、可機器判定的 Edixhoven-safe pool。

---

# 4. Multiplicative witness graph

對每個 fixed odd multiplicative prime \(p\)，要求存在另一個 odd multiplicative prime \(\ell\neq p\)：

\[
p\nmid v_\ell(\Delta_E).
\]

這是 leave-one-out witness gate：

\[
\boxed{\mathrm{LOO}(p)}.
\]

另外要求至少一個 nonsplit multiplicative prime，供 Fouquet–Wan H3。

第一個最乾淨 pool還可額外要求：

```text
exists nonsplit multiplicative ell with v_ell(Delta)=1
```

這會自動消除 generic supersingular H3 exceptional primes。

---

# 5. Residual image discipline

`ec_curvedata.nonmax_primes` 可用來建立 clean pool：

```text
no odd nonmaximal primes
```

但這只是 global residual-image clean filter。

它**不能**替代 fixed additive prime 的 local FW-H2 compiler：

```text
global absolute irreducible != local irreducible.
```

因此每個 odd additive prime仍輸出：

```text
FIXED_ADDITIVE_H2_PENDING
```

等待上一版 local p-isogeny backend。

---

# 6. Base BSD(E,2) discipline

即使：

```text
rank 0
torsion trivial
sha_an = 1
Tamagawa odd
```

可以推出 analytic quotient的 \(2\)-adic parity漂亮，

仍不得輸出：

```text
BSD(E,2) PROVED
```

除非有：

- 已知 full BSD verification；
- exact descent certificate；
- theorem applicability certificate；
- 其他 rigorous source。

因此 census中的主要狀態是：

```text
STRUCTURAL_FAMILY_CANDIDATE
```

而不是：

```text
PROVED_FAMILY.
```

---

# 7. Expected local workflow

```bash
psql \
  -h devmirror.lmfdb.xyz \
  -p 5432 \
  -U lmfdb \
  -d lmfdb \
  -f sql/00_candidate_universe.sql \
  --csv > results/00_candidate_universe.csv

psql ... \
  -f sql/01_edixhoven_safe_structural_pool.sql \
  --csv > results/01_structural_pool.csv

psql ... \
  -f sql/02_local_rows_for_structural_pool.sql \
  --csv > results/02_local_rows.csv

python scripts/postprocess_witness_network.py \
  --base results/01_structural_pool.csv \
  --local results/02_local_rows.csv \
  --outdir results/final
```

---

# 8. Completion outputs

本地執行後至少應產生：

```text
candidate_census.csv
structural_pass.csv
witness_graph_fail.csv
fw_h3_fail.csv
finite_exception_pending.csv
additive_h2_pending.csv
bsd2_pending.csv
summary.json
CENSUS_REPORT.md
```

每條 curve都必須有 failure reason。

---

# 9. Completion gate

只有以下全部成立，才能稱：

```text
LMFDB EXACT CENSUS COMPLETE
```

```text
[ ] SQL mirror release / timestamp recorded
[ ] raw query SHA256 recorded
[ ] row counts recorded
[ ] all local rows materialized
[ ] Tamagawa parity exact
[ ] all odd additive primes classified
[ ] multiplicative leave-one-out graph exact
[ ] nonsplit FW-H3 reservoirs exact
[ ] gcd exceptional-prime sets exact
[ ] nonmax-prime clean flag exact
[ ] UNKNOWN/PENDING rows preserved
[ ] no analytic Sha -> actual Sha inference
[ ] no numeric Lalg parity -> BSD(E,2) inference
```

---

## Recommended interpretation

如果 strict structural pool最後是空的，這本身就是 theorem-coverage information。

如果不空，下一步只對剩下的少量 rows做：

1. rigorous `BSD(E,2)` anchor；
2. fixed additive FW-H2 local-isogeny certificate；
3. finite ordinary/supersingular exception routing。

不再掃全庫做 expensive math。
