# 03｜Algorithm 1 Soundness Gates

## S1 — Analytic $\Sha$ 不得冒充 actual $\Sha$

`sha` 欄位可作 analytic prediction / gate input；certificate必須保存 descent來源。

## S2 — $\dim\Sha[2]$ 不得冒充 $\operatorname{ord}_2\#\Sha$

目前安全策略只在：

$$
v_2(\Sha_{\mathrm{an}})=0
$$

且 descent pins：

$$
\Sha[2]=0
$$

時接受 $\operatorname{BSD}(E,2)$。

正 valuation必須標 `OPEN / higher 2-power descent needed`。

## S3 — Timeout 是 UNKNOWN

mwrank timeout不是 theorem failure。

## S4 — Testing flag 污染

`skip_filter_S` 或 `skip_BSD_at_2_check` 開啟時，整個 run certificate自動降級。

## S5 — deterministic theorem gate

$\mathcal S\ne\varnothing$ production gate使用 deterministic criterion；bounded search只作 cross-check / witness。

## S6 — provenance

每條 PASS 保存：

```text
predicate
value
evidence_type
backend
semantic_version
file/commit SHA
timestamp
```
