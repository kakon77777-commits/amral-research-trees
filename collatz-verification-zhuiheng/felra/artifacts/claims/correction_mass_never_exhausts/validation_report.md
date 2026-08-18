# FELRA Validation Report

- Claim ID: `correction_mass_never_exhausts`
- Statement: On the all-ones spine the anchor gap 1 - (2/3)^m is positive at every m
- Declared domain: m in [1, 200] with 200 declared samples
- Result: **SUPPORTED IN DECLARED DOMAIN**
- Generated at: `2026-08-18T15:02:20.696719+00:00`

> This report records finite-budget machine validation. It is not a universal proof.

## Reproducibility metadata

- `expression`: `"m > 0"`
- `project_id`: `"collatz-anchor-representation"`
- `config_sha256`: `"f8b8b37d71145f14c144b47d67af5657ffc933e5f771e1c58e0e7c0621c5f523"`
- `seed`: `42`
- `analyses`: `[{"id": "anchor_gap_below_the_horizon", "type": "cross_backend", "success": true, "report": "analyses/anchor_gap_below_the_horizon/analysis_report.md"}, {"id": "anchor_gap_at_the_horizon", "type": "cross_backend", "success": false, "report": "analyses/anchor_gap_at_the_horizon/analysis_report.md"}, {"id": "decimal_still_sees_it", "type": "cross_backend", "success": true, "report": "analyses/decimal_still_sees_it/analysis_report.md"}, {"id": "anchor_precision_ladder", "type": "precision_ladder", "success": true, "report": "analyses/anchor_precision_ladder/analysis_report.md"}, {"id": "lean_whole_development_axiom_audit", "type": "formal_check", "success": true, "report": "analyses/lean_whole_development_axiom_audit/analysis_report.md"}]`

## Validation channels

### numerical

- Passed: `True`
- Summary: Claim held for all 200 evaluated points.
- Metrics: `{"tested_count": 200, "passed_count": 200, "failed_count": 0, "pass_rate": 1.0, "strategy": "declared_cartesian_grid", "exhaustive_declared_grid": true, "finite_domain": true}`
