# FELRA Analysis Report — What FELRA will not export, and why the general round is not solver-checkable

- Analysis ID: `refusal_on_symbolic_exponent`
- Type: `obligation_export`
- Execution success: `False`
- Summary: the claim cannot be rendered exactly: only a literal non-negative integer exponent can be rendered exactly; 3 ** y cannot
- Generated at: `2026-08-21T13:16:23.565481+00:00`

> Analysis outputs are finite-budget computational evidence and diagnostics.

## Metrics

```json
{
  "exported": false,
  "expression": "3 ** y <= 2 ** b",
  "refusal": "only a literal non-negative integer exponent can be rendered exactly; 3 ** y cannot",
  "cache_hit": false,
  "cache_fingerprint": "4cb4aefaa778b4f49c5dfee6ee129732423ee384257454f256699da8c19d37bc"
}
```

## Artifacts

- `analyses\refusal_on_symbolic_exponent\analysis_report.md`
- `analyses\refusal_on_symbolic_exponent\metrics.json`

## Warnings

- refused rather than approximated: an obligation that is nearly the claim is an obligation about a different claim
