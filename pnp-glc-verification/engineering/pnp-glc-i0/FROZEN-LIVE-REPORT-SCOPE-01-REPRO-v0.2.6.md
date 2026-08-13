# FROZEN-LIVE-REPORT-SCOPE-01 regression

Frozen generation command：

```powershell
python -I -B scripts/run_experiment_v026.py . --seed 20260810 --two-sat-crosscheck-seed 20260809 --max-parity-n 12 --output i0-run-report.v0.2.6-candidate.json
```

Frozen replay command：

```powershell
python -I -B scripts/reproduce_live_report_scope_v026.py .
```

Evidence location：`i0-run-report.v0.2.6-candidate.json#/two_sat/deterministic_crosscheck`。

精確 ledger：

| n | cases | SAT | UNSAT | mismatch | certificate failure |
|---:|---:|---:|---:|---:|---:|
| 1 | 250 | 227 | 23 | 0 | 0 |
| 2 | 250 | 219 | 31 | 0 | 0 |
| 3 | 250 | 214 | 36 | 0 | 0 |
| 4 | 250 | 198 | 52 | 0 | 0 |
| 5 | 250 | 194 | 56 | 0 | 0 |
| 6 | 250 | 171 | 79 | 0 | 0 |

總計 1500，seed=`20260809`，evidence digest=`2F472DB6486459BC6502AA0ABDF1B79FD361D274F41DFE461E14C197F414EBEF`。Replay 對 frozen crosscheck object做 exact equality；7/7 scope checks conformant。

這是 bounded Experiment，不等同 general 3-SAT、P=NP或P≠NP證據。
