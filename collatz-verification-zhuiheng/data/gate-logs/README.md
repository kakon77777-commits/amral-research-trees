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
| `hz-route-probe.json` | `code/hz_route_probe.py` — the first bridge to the Hard-Zeta route map: measures `tau_c` against `sigma` and splits `E_k` into `C_k` and `R_k`. |
| `ot-package-integrity.txt` | the subject package's *own* `tools/verify_series.py`, run against the copy archived at `../../../collatz-ot-series-neok/`. Not this arm's verifier — the author's, run on the committed bytes. |
| `ot-paper01-recheck.json` | `code/ot_paper01_recheck.py` — Paper 01's Claim Ledger arithmetic, plus external verification of the cited bibliography against arXiv and Crossref. |
| `ot-paper02-recheck.json` | `code/ot_paper02_recheck.py 16` — independent re-derivation of Paper 02 of Neo.K's Operation Translation Series |
| `ot-paper06-recheck.json` | `code/ot_paper06_recheck.py 20001` — the same for Paper 06, on real admissible orbits |
| `ot-paper03-recheck.json` | `code/ot_paper03_recheck.py 13` — Paper 03, with `r_w` derived twice: once by the closed congruence, once by refinement induction that never uses it. |
| `ot-paper04-recheck.json` | `code/ot_paper04_recheck.py 10` — Paper 04, bidirectional residue transport. The subject's suite has no Paper 04 test, so these are first checks. |
| `ot-paper05-kl-recheck.json` | `code/ot_paper05_kl_recheck.py` — the KL constant, at 60 digits and on exact binomial tails. Separates instrument soundness from subject findings. |
| `ot-paper07-recheck.json` | `code/ot_paper07_recheck.py 8 3000` — the same for Paper 07, over 24 (m, r) parameter pairs, including the floating-floor margin analysis |
| `ot-paper08-recheck.json` | `code/ot_paper08_recheck.py` — Paper 08's algebraic breakage ladder, one explicit witness per rung. |
| `ot-paper09-recheck.json` | `code/ot_paper09_recheck.py 11 20` — the same for Paper 09, including K(2^40) linked to the archived exhaustive run |
| `ot-recheck-drill.json` | `code/ot_recheck_drill.py` — the falsifiability drill for all nine rechecks |
| `ot-recheck-drill.progress.txt` | the same run's stderr, one line per planted defect |
| `ot-paper05-block-benchmark.json` | `collatz_verify.exe --block 16 --to 1048576` — independent reproduction of the series' Paper 05 `k=16` descent counts |

An earlier, narrower drill log pair (`ot-paper02-drill.json` and its progress
file) covered Paper 02 only and was superseded by `ot-recheck-drill.json` when
Paper 06 was added. It is not deleted history — it remains in the repository at
commit `aa0c02a`.

`build_results.py` reads these and refuses to write a summary if any of them is
missing or reports a failure. It does not re-run the gates, so it cannot turn a
failed gate into a passing line in the summary.
