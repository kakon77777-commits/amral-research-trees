# FELRA Validation Report

- Claim ID: `reset_needs_the_correction_bound`
- Statement: The reset inequality does NOT hold on its own. FALSE on this domain, and a solver should hand back a counterexample rather than a proof.

- Declared domain: y in [1, 1000000] with 25 declared samples; b in [0, 1000000] with 25 declared samples
- Result: **NOT SUPPORTED**
- Generated at: `2026-08-21T13:16:23.134448+00:00`

> This report records finite-budget machine validation. It is not a universal proof.

## Reproducibility metadata

- `expression`: `"3 * (243 * y + b) <= 243 * (3 * y + 5)"`
- `project_id`: `"au2e2-first-crossing-reset"`
- `config_sha256`: `"3f0168cc2245df7ee2a746e22ca4bd64e51c73d8eaba98fe1c86ce0721895a79"`
- `seed`: `42`
- `analyses`: `[{"id": "refute_reset_alone", "type": "obligation_export", "success": true, "report": "analyses/refute_reset_alone/analysis_report.md"}]`

## Validation channels

### numerical

- Passed: `False`
- Summary: Claim failed at 600 of 625 evaluated points.
- Metrics: `{"tested_count": 625, "passed_count": 25, "failed_count": 600, "pass_rate": 0.04, "strategy": "declared_cartesian_grid", "exhaustive_declared_grid": true, "finite_domain": true}`

Counterexamples:

- `{"index": 1, "inputs": {"y": 1, "b": 41667}, "outcome": false}`
- `{"index": 2, "inputs": {"y": 1, "b": 83333}, "outcome": false}`
- `{"index": 3, "inputs": {"y": 1, "b": 125000}, "outcome": false}`
- `{"index": 4, "inputs": {"y": 1, "b": 166667}, "outcome": false}`
- `{"index": 5, "inputs": {"y": 1, "b": 208333}, "outcome": false}`
- `{"index": 6, "inputs": {"y": 1, "b": 250000}, "outcome": false}`
- `{"index": 7, "inputs": {"y": 1, "b": 291667}, "outcome": false}`
- `{"index": 8, "inputs": {"y": 1, "b": 333333}, "outcome": false}`
- `{"index": 9, "inputs": {"y": 1, "b": 375000}, "outcome": false}`
- `{"index": 10, "inputs": {"y": 1, "b": 416667}, "outcome": false}`
- `{"index": 11, "inputs": {"y": 1, "b": 458333}, "outcome": false}`
- `{"index": 12, "inputs": {"y": 1, "b": 500000}, "outcome": false}`
- `{"index": 13, "inputs": {"y": 1, "b": 541667}, "outcome": false}`
- `{"index": 14, "inputs": {"y": 1, "b": 583333}, "outcome": false}`
- `{"index": 15, "inputs": {"y": 1, "b": 625000}, "outcome": false}`
- `{"index": 16, "inputs": {"y": 1, "b": 666667}, "outcome": false}`
- `{"index": 17, "inputs": {"y": 1, "b": 708333}, "outcome": false}`
- `{"index": 18, "inputs": {"y": 1, "b": 750000}, "outcome": false}`
- `{"index": 19, "inputs": {"y": 1, "b": 791667}, "outcome": false}`
- `{"index": 20, "inputs": {"y": 1, "b": 833333}, "outcome": false}`
