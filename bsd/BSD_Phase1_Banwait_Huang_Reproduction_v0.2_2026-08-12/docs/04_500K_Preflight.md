# 04｜500K Preflight

本 runtime 沒有獨立重算 500K 官方輸出。

放大前依序：

1. 鎖 Sage / LMFDB / Git SHA / descent backend；
2. current `<150` exact replay；
3. old-only 13條 first-failure replay；
4. discrepancy four exact rejection replay；
5. 才跑 conductor `<500000`。

500K run必須輸出：

```text
passed.csv
failed.csv
unknown.csv
predicate_trace.jsonl
descent_certificates/
run_manifest.json
hashes.txt
```

`unknown.csv` 不能丟掉，否則 timeout / backend failure會被誤讀成數學拒絕。

成功判定不是「最後 count 很接近」，而是：

$$
\boxed{
\text{final set exact}
+
\text{stage counts reproducible}
+
\text{adversarial corpus stable}
+
\text{certificate semantics stable}.
}
$$
