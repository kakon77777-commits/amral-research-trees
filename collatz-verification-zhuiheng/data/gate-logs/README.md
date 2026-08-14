# `data/gate-logs/` — archived gate output

The exact stdout of each gate, kept so that `results.v1.json` can be rebuilt
from evidence rather than retyped, and so a later reader can see what the gates
said at the time rather than only that they were said to pass.

| File | Produced by |
|---|---|
| `self-test.json` | `collatz_verify.exe --self-test` |
| `reference-crosscheck.json` | `code/reference_crosscheck.py` |
| `anchors.json` | `code/anchors.py` |
| `mutation-drill.json` | `code/mutation_drill.py` |
| `mutation-drill.progress.txt` | the same run's stderr, one line per mutation as it was decided |
| `coverage.json` | `code/verify_run_logs.py` |
| `coverage-refusal-drill.json` | a manual drill showing the aggregator refusing a run with a deleted chunk, and a run with one chunk's count reduced by one; the tampered log was restored byte-identical afterwards |

`build_results.py` reads these and refuses to write a summary if any of them is
missing or reports a failure. It does not re-run the gates, so it cannot turn a
failed gate into a passing line in the summary.
