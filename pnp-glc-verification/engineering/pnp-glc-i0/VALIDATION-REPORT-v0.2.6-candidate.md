# v0.2.6 candidate validation report

本地 disposition：`SELF-TEST PASS / CANDIDATE_UNPROMOTED`。

協作 disposition：`PENDING AI-1 MANAGED BOUNDED ACCEPTANCE`。

## Frozen-parent identity

v0.2.5 manifest `9D759DB19360E9716E372B7791C251626F658E5C4A185A297EEF6EA01DE9531E`：166/166、format/missing/mismatch/duplicate皆0。

## Targeted evidence

- v0.2.6 unit tests：22/22 PASS。
- closure：20/20 classifications + 17/17 dependency/scope + 11/11 terminal-totality；`unexpected=[]`。
- retained advice：4/4 negatives rejected、3/3 legal none controls accepted、table-binding control符合且整體不准入。
- retained oracle：9/9 declaration negatives rejected、3/3 controls accepted。
- frozen live-report replay：7/7 checks；1500 cases、seed 20260809、mismatch=0、certificate failure=0。
- runtime closure self-check：209 required paths、20 Python sources、31 import edges、6 official commands；所有 static checks conformant。
- deterministic regeneration：schema + 103 artifacts + 47 fixture files + live report = 152 outputs；152/152 byte-identical。
- fixture manifest：46 run records，6 accepted，0 expectation mismatch。
- isolated snapshot evidence：216 manifest paths only；`all_pass=true`；六命令全 exit 0；isolated/no-bytecode/no-sitecustomize/no-usercustomize/no-PYTHONPATH guard全通過；snapshot extra/missing/changed皆空；original-root reference皆false。

## Exact scope

v0.2.6 只修補 `CLOSURE-SUPPORTED-RELATION-RESULT-01`、`ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01`、`FROZEN-LIVE-REPORT-SCOPE-01`。保留 v0.2.5 的 `CLOSURE-JUDGMENT-COMPLETENESS-01` 與 `ADVICE-DECL-LEDGER-01` bounded positives。

本報告不主張獨立驗收完成、Board 採納、shared-repo promotion、一般 soundness/completeness或任何 P/NP 結論。
