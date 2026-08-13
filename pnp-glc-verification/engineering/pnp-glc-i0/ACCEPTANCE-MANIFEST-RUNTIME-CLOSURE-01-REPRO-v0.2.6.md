# ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01 regression

Machine-readable source：`artifacts-v0.2.6/acceptance-runtime-closure.v0.2.6.json`。

Static closure：

- 209 required runtime/evidence/build-input paths；
- 20 AST-derived Python source paths；
- 29 local import edges；
- `oracles.py`、`parity.py`、`two_sat.py`、package `__init__.py`、validator、experiment、generator與全部 reproducer/build entrypoints均納入；
- operational evidence hashes由 validator pin重核；direct receipt maps及role-bearing fixed point再導出 content evidence paths，包含六個 legacy opaque artifacts；唯一 unresolved `f…f` hash明列為故意的 negative fixture；
- v0.2.6 generator 不再 import legacy generator，parent templates均列為 explicit build inputs；fixture signing key明列為 build-only excluded secret capability，不參與 acceptance commands。

官方隔離命令共六條：runtime self-check、closure、advice、oracle、live-report scope與 minimal CLI。

隔離方法：由 top-level manifest 逐項驗 hash後，只複製 manifest paths到全新 temporary snapshot；清除 `PYTHONHOME/PYTHONPATH/PYTHONSTARTUP/PYTHONUSERBASE`；設 no-bytecode/no-user-site；每條命令使用 `python -I -B`。guard 必須證明 isolated mode、no bytecode、無 `sitecustomize/usercustomize`、無 `PYTHONPATH`。執行前後 snapshot不得新增、刪除或修改任何 file，stdout/stderr不得含 original candidate root。

Frozen 結果以 `runtime-isolation-report.v0.2.6.json` 為權威：216 manifest entries，`all_pass=true`，六條命令全 exit 0；guard 全通過；snapshot extra/missing/changed皆空；required path omission與 original-root reference皆空。
