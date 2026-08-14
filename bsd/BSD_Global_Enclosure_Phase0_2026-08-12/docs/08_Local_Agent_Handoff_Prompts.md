# 08｜本地多 Agent 交接提示

## Agent A — Statement Auditor

**任務：**  
只使用標準外部數學，建立 BSD-W、BSD-F、BSD-S 的 theorem dependency DAG。

**禁止：**

- 把 rank equality 等同 full BSD；
- 把 analytic $\Sha$ 等同 actual $\Sha$；
- 用 Wikipedia 作核心 theorem source。

**輸出：**

```text
theorem
statement
assumptions
claim_scope
what_it_does_not_prove
primary_source
```

---

## Agent B — Banwait–Huang Reproducer

**任務：**  
重現 arXiv:2601.16044 的 algorithm，先跑作者給出的樣本，再跑 conductor $\le500000$。

**輸出：**

- source code；
- environment lock；
- predicate list；
- result CSV/JSONL；
- discrepancies；
- exact count；
- hash。

**停止條件：**  
若 paper criterion有任何無法從 LMFDB / Sage / Magma exact 決定的欄位，標 `unknown`，不得猜測。

---

## Agent C — Certificate Schema Engineer

**任務：**  
實作 `bsd_curve_certificate.schema.json`，建立 importer與 validator。

**關鍵：**

```text
numeric evidence
rigorous computation
external theorem
conditional theorem
actual proof
```

必須分開。

---

## Agent D — Rank-2 Wall Analyst

**任務：**  
以 389.a1 為中心，逐項審計：

$$
r_{\mathrm{alg}},
r_{\mathrm{an}},
\Omega,
\operatorname{Reg},
c_p,
E_{\mathrm{tors}},
\Sha,
L^{(2)}(1)/2!.
$$

每項回答：

```text
value
how computed
rigorous?
theorem?
assumption?
missing certificate?
```

---

## Agent E — Adversarial Referee

**任務：**  
對所有輸出尋找：

- circular BSD assumption；
- numerical-to-proof leap；
- finite-to-global leap；
- p-part-to-full leap；
- rank0/1-to-high-rank leap；
- isogeny double counting；
- database incompleteness；
- normalization mismatch。

輸出必須是：

```text
PASS
FAIL
OPEN
```

不能只寫一般建議。

---

## Agent F — Internal Theory Quarantine

**任務：**  
審計 Neo.K 舊格點／PRC 稿與 BSD 的關係。

只允許輸出：

1. 可翻譯成標準 lemma 的部分；
2. 循環或未定義部分；
3. 需要的新 proof obligations。

禁止直接把內部公理帶進 external main proof。
