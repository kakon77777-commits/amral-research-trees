# FELRA Analysis Report — Where float64 reports the correction mass as exhausted

- Analysis ID: `anchor_gap_at_the_horizon`
- Type: `cross_backend`
- Execution success: `False`
- Summary: 3 point(s) across float64, rational → inconsistent_somewhere
- Generated at: `2026-08-18T14:34:03.437318+00:00`

> Analysis outputs are finite-budget computational evidence and diagnostics.

## Metrics

```json
{
  "expression": "1 - (two / three) ** m",
  "backends": [
    "float64",
    "rational"
  ],
  "tolerance": 0.0,
  "decimal_prec": 50,
  "points_compared": 3,
  "difference_matrix": {
    "float64|rational": {
      "exact": 0,
      "within_tolerance": 0,
      "inconsistent": 3
    }
  },
  "points": [
    {
      "assignment": {
        "two": "2",
        "three": "3",
        "m": "92"
      },
      "values": {
        "float64": "9007199254740991/9007199254740992",
        "rational": "78551672112789406881262420173769446463876145/78551672112789411833022577315290546060373041"
      },
      "values_float": {
        "float64": 0.9999999999999999,
        "rational": 0.9999999999999999
      },
      "agreement": {
        "float64|rational": "inconsistent"
      }
    },
    {
      "assignment": {
        "two": "2",
        "three": "3",
        "m": "93"
      },
      "values": {
        "float64": "1/1",
        "rational": "235655016338368225595547417662829438988125331/235655016338368235499067731945871638181119123"
      },
      "values_float": {
        "float64": 1.0,
        "rational": 1.0
      },
      "agreement": {
        "float64|rational": "inconsistent"
      }
    },
    {
      "assignment": {
        "two": "2",
        "three": "3",
        "m": "150"
      },
      "values": {
        "float64": "1/1",
        "rational": "369988485035126972924700781024448951480513219331437004365689268919001625/369988485035126972924700782451696644186473100389722973815184405301748249"
      },
      "values_float": {
        "float64": 1.0,
        "rational": 1.0
      },
      "agreement": {
        "float64|rational": "inconsistent"
      }
    }
  ],
  "exactness": "inconsistent_somewhere",
  "any_input_was_float64": false,
  "errors": [],
  "note": "`exact` means the two ontologies produced the same rational number; `within_tolerance` means they did not. Only the first supports the evidence ladder's `exact_verified` rung.",
  "cache_hit": false,
  "cache_fingerprint": "b4e1991a273c5821b016d2c4a98f750c1e84d41cfb235d197bcd040bb4f81d22"
}
```

## Artifacts

- `analyses\anchor_gap_at_the_horizon\analysis_report.md`
- `analyses\anchor_gap_at_the_horizon\metrics.json`
