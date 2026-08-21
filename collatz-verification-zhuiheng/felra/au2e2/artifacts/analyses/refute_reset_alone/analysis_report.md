# FELRA Analysis Report — Export the unguarded inequality — a counterexample is the correct outcome

- Analysis ID: `refute_reset_alone`
- Type: `obligation_export`
- Execution success: `True`
- Summary: z3 → refuted (expected refuted): the solver found a counterexample; the twin is satisfiable too, so the claim holds at some points of the domain and fails at others
- Generated at: `2026-08-21T13:16:23.431768+00:00`

> Analysis outputs are finite-budget computational evidence and diagnostics.

## Metrics

```json
{
  "exported": true,
  "expression": "3 * (243 * y + b) <= 243 * (3 * y + 5)",
  "parameters": {
    "y": {
      "type": "int",
      "range": [
        1,
        1000000
      ]
    },
    "b": {
      "type": "int",
      "range": [
        0,
        1000000
      ]
    }
  },
  "obligation_file": "felra\\au2e2\\artifacts\\analyses\\refute_reset_alone\\obligation.smt2",
  "twin_file": "felra\\au2e2\\artifacts\\analyses\\refute_reset_alone\\obligation_twin.smt2",
  "obligation_sha256": "d10946e15233bc1f133b71be550c5af577db2f8b9cff4964029451207e5462d2",
  "twin_sha256": "8cc44c149fdc1eeb0c5b345d14d073ca48af1ce3705dc30ccf5c7efb6b90ab75",
  "format": "smt-lib2",
  "note": "the obligation asserts the domain and the NEGATION of the claim, so `unsat` is a proof over that domain and `sat` is a counterexample",
  "primary": {
    "formal_status": "refuted",
    "checker": {
      "backend": "z3",
      "available": true,
      "command": [
        "D:\\Ai\\work together\\tools\\z3-5.1.0-x64-win\\bin\\z3.exe"
      ],
      "executable_path": "D:\\Ai\\work together\\tools\\z3-5.1.0-x64-win\\bin\\z3.exe",
      "executable_sha256": "c638e6b8d066a5ad6ea2712dcd5e2eff5c57eba501b98e7fa8487f7daf0e863d",
      "version_string": "Z3 version 5.1.0 - 64 bit",
      "note": null
    },
    "obligation": {
      "path": "D:\\Ai\\work together\\amral-research-trees\\collatz-verification-zhuiheng\\felra\\au2e2\\artifacts\\analyses\\refute_reset_alone\\obligation.smt2",
      "sha256": "c0b6810c24e269dc786acfd6a1409e7e5293aaa329c558dc9cd7fc555ae00d04",
      "bytes": 497
    },
    "exit_code": 0,
    "duration_seconds": 0.024,
    "detail": "z3 reported sat, so a counter-model exists",
    "stdout_tail": "sat\n",
    "assumptions": [],
    "limitations": [
      "a formal verdict is relative to the obligation as written; it says nothing about whether the obligation states the intended claim"
    ],
    "theorems_audited": null,
    "axioms_seen": null
  },
  "twin": {
    "formal_status": "refuted",
    "checker": {
      "backend": "z3",
      "available": true,
      "command": [
        "D:\\Ai\\work together\\tools\\z3-5.1.0-x64-win\\bin\\z3.exe"
      ],
      "executable_path": "D:\\Ai\\work together\\tools\\z3-5.1.0-x64-win\\bin\\z3.exe",
      "executable_sha256": "c638e6b8d066a5ad6ea2712dcd5e2eff5c57eba501b98e7fa8487f7daf0e863d",
      "version_string": "Z3 version 5.1.0 - 64 bit",
      "note": null
    },
    "obligation": {
      "path": "D:\\Ai\\work together\\amral-research-trees\\collatz-verification-zhuiheng\\felra\\au2e2\\artifacts\\analyses\\refute_reset_alone\\obligation_twin.smt2",
      "sha256": "ac2fe1dd5e24a8d11ccc38a0a6fe947bb4f58823577645a7653788b18158f763",
      "bytes": 609
    },
    "exit_code": 0,
    "duration_seconds": 0.024,
    "detail": "z3 reported sat, so a counter-model exists",
    "stdout_tail": "sat\n",
    "assumptions": [],
    "limitations": [
      "a formal verdict is relative to the obligation as written; it says nothing about whether the obligation states the intended claim"
    ],
    "theorems_audited": null,
    "axioms_seen": null
  },
  "formal_status": "refuted",
  "detail": "the solver found a counterexample; the twin is satisfiable too, so the claim holds at some points of the domain and fails at others",
  "domain_is_nonempty": true,
  "discriminates": true,
  "cache_hit": false,
  "cache_fingerprint": "6c40f7166bedee9c82198f3467bdb0f04f1ed0ef9de0c094326732cdc355093c"
}
```

## Artifacts

- `analyses\refute_reset_alone\analysis_report.md`
- `analyses\refute_reset_alone\metrics.json`
