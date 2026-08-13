# CLOSURE-SUPPORTED-RELATION-RESULT-01 regression

命令：

```powershell
python -I -B scripts/reproduce_closure_class_v026.py .
```

驗收面：

- 20/20 executable classifications conformant；
- 17/17 dependency/scope checks conformant；
- 11/11 terminal-totality checks conformant；
- `SupportedEdgeRelation=false` 唯一導出 `Malformed/FAIL/do-not-traverse`；
- `SupportedEdgeRelation=true` 唯一導出 `Traverse/PASS` 並轉移至 `judgments.SupportedTraversal`；
- fixed point 的 PASS/FAIL/UNKNOWN 三個 branches 皆是 terminal；
- transition refs fully qualified且 target全可解析；
- `unexpected=[]`。

分類：Definition/interface candidate + executable regression。這不是一般 soundness/completeness theorem，也沒有 P/NP 推論。
