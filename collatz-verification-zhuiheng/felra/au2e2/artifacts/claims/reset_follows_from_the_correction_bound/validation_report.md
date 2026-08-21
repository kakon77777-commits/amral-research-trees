# FELRA Validation Report

- Claim ID: `reset_follows_from_the_correction_bound`
- Statement: At L=5, the correction bound b <= 405 implies the reset inequality, for every start y in the declared range.

- Declared domain: y in [1, 1000000] with 25 declared samples; b in [0, 1000000] with 25 declared samples
- Result: **SUPPORTED IN DECLARED DOMAIN**
- Generated at: `2026-08-21T13:16:23.128591+00:00`

> This report records finite-budget machine validation. It is not a universal proof.

## Reproducibility metadata

- `expression`: `"not (b <= 405) or 3 * (243 * y + b) <= 243 * (3 * y + 5)"`
- `project_id`: `"au2e2-first-crossing-reset"`
- `config_sha256`: `"3f0168cc2245df7ee2a746e22ca4bd64e51c73d8eaba98fe1c86ce0721895a79"`
- `seed`: `42`
- `analyses`: `[{"id": "prove_reset_from_bound", "type": "obligation_export", "success": true, "report": "analyses/prove_reset_from_bound/analysis_report.md"}]`

## Validation channels

### numerical

- Passed: `True`
- Summary: Claim held for all 625 evaluated points.
- Metrics: `{"tested_count": 625, "passed_count": 625, "failed_count": 0, "pass_rate": 1.0, "strategy": "declared_cartesian_grid", "exhaustive_declared_grid": true, "finite_domain": true}`
