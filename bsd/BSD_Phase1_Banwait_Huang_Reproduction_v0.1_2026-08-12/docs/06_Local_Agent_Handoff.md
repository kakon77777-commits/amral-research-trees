# 06｜本地 Agent 交接

## Agent A — Sage Environment Builder

建立：

```text
Sage version
LMFDB release
database connection
Python dependencies
PARI / mwrank status
```

先跑 conductor $<150$。

---

## Agent B — Algorithm 1 Reproducer

輸出每個 filter 後的 row count：

```text
initial
semistable/optimal/composite conductor
a3
p-isogeny
ramification
rank/L-value
CLZ branch
Zhai branch
BSD(E,2)
```

每個 curve保存 pass/fail原因。

---

## Agent C — 2-Descent Referee

對 `check_BSD_at_2`：

- 確認 analytic Sha valuation；
- 保存每個 backend的 bounds；
- 驗證 `sha_an_ord_2 != 0 -> False`；
- 檢查 timeout是否造成 false negative；
- 不允許把 $\dim\Sha[2]$ 當 $\operatorname{ord}_2\#\Sha$。

---

## Agent D — Algorithm 2 Cross-Checker

同時跑：

1. 官方 Sage code；
2. 本包 pure-Python mirror。

對每個 discrepancy分類：

```text
number-field index issue
Kronecker convention
negative twist convention
finite-field point count
source-branch mismatch
official code drift
```

---

## Agent E — Paper/Code Version Auditor

固定：

- arXiv version；
- GitHub file SHA；
- LMFDB release；
- runtime flags。

輸出 paper pseudocode與 current code的 semantic diff。

---

## Agent F — Global Enclosure Referee

每輪只回答：

```text
這一輪擴大了 theorem coverage嗎？
增加了證書強度嗎？
還是只增加枚舉量？
```

若只是枚舉量，連續三輪後停止。
