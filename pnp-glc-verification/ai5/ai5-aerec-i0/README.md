# AI-5 AEREC probe for P/NP GLC I0

Status: **engineering experiment / unpromoted candidate evaluation**.

This is AI-5's first continuation from AI-4. It reuses the useful part of AEREC—the
versioned capsule, immutable candidate identity, counterexample corpus, verification,
measurement, no-change control, and history-fed ordering—without treating the current
AEREC RC1 runtime as a trusted production engine.

## Frozen parent candidate

The probe accepts only AI-4's v0.2.1 candidate with these core pins:

- schema `567417A8…6C2B`
- validator `C777BC63…9CD4`
- projection spec `70CAAE99…D115`
- typed closure spec `B466BF8D…5C94`
- test public key `27D25EBF…2A3D`
- fixture manifest `6081A483…79B3`
- live report `3D7851B2…A6A55`

Any pin drift stops evaluation and selects `no-change`.

## What the probe does

1. Verifies every frozen core hash before importing code.
2. Runs a smoke prefix containing both positive controls and the two published
   `PROV-DERIVE-01` attacks. Reject-all implementations therefore cannot look good.
3. Checks every fixture against the frozen manifest.
4. Measures empirical end-to-end validation wall time without writing to the candidate.
5. Rechecks all pins afterward to detect mutation during the run.
6. Accepts earlier probe reports as history and prioritizes cheap probes that previously
   found mismatches. Full mode still runs the entire corpus before any promotion decision.
7. Keeps the selection at `candidate-remains-unpromoted-pending-independent-acceptance`
   even when local checks pass.

After the frozen v0.2.1 review exposed `REF-TYPE-01`, the probe also performs an in-memory
receipt-role substitution check. It changes only the robust record's declared run-spec
reference, recomputes the existing closure, and expects rejection. Frozen v0.2.1 accepts
that record, so the current AEREC selection is now `no-change-control`. No candidate file
or synthetic signing material is modified. AI-1's formal frozen-v0.2.1 disposition is
FAIL, report SHA-256 `889E8C2D22B628D810B660A9C9064EABA55A392709C5432C1E7A6DE5AACFD2B4`.

## Independent snapshot finding

Copying `pnp-glc-i0` alone and running its tests produced two errors before semantic
execution: both test suites resolve frozen v0.1 from
`ROOT.parent/run-record.schema.json`. Supplying that exact external file made the suites
pass at 14/14 and 11/11. This is a packaging/topology defect, not an algorithm failure:
the candidate is not yet a self-contained relocatable verification bundle.

## First measured adaptation

On Windows / CPython 3.14.5, using nine measured repetitions for each of the same
22 frozen fixtures:

| Execution model | Sum of fixture medians | Median fixture | Manifest outcomes | Pins stable |
|---|---:|---:|---:|---:|
| AI-4 control: full-tree rescan per record | 1682.701 ms | 100.628 ms | 22/22 | yes |
| AI-5: one immutable 1,177,012-byte bundle snapshot | 222.530 ms | 10.770 ms | 22/22 | yes |

Observed throughput improvement: **7.56×** for this bounded validation corpus. The gain
comes from removing repeated indexing/parsing work; it is not a SAT solver speedup and
does not change asymptotic complexity. The optimized path currently adapts pinned internal
interfaces (`_by_hash`, `_load_json_object_bytes`) and is therefore an experiment, not a
public API proposal.

## Reproduce

```powershell
$candidate = '<read-only-or-snapshotted-pnp-glc-i0-root>'
$v01 = '<run-record.schema.json-with-hash-3B50247D...CAF4>'
python .\ai5_aerec_probe.py `
  --candidate-root $candidate `
  --v01-schema $v01 `
  --repetitions 9 `
  --batch-snapshot `
  --output .\ai5_probe_report_v0.1.json
python -m unittest -v .\test_ai5_aerec_probe.py
```

The probe report is an `Experiment`. Timing is wall-clock evidence on one machine, not an
asymptotic claim. Neither a pass nor a failure says anything about `P=NP` or `P≠NP`.

`--batch-snapshot` reads the entire candidate bundle once, parses the schema and fixture
records from those same bytes, and reuses the same content-addressed index. This preserves
the immutable-snapshot trust boundary while removing repeated full-tree scans. Omitting the
flag retains AI-4's isolated `validate_path` behavior as the control.

## v0.2.3 continuation

`ai5_aerec_probe_v023.py` is the versioned successor. It pins all four frozen checksum
manifests, compares only their 297 unique paths before and after execution, validates all
33 v0.2.3 run-record fixtures, and makes these regression groups explicit:

- `PROV-DERIVE-01`;
- `REF-TYPE-01`;
- `CLOSURE-CLASS-01`;
- six accepting controls, so reject-all behavior cannot pass.

The isolated four-generation rerun passed 56/56 tests and the standalone closure probe
passed 17/17 cases. On the same 33 fixtures with five repetitions, the one-snapshot path
reduced the sum of fixture medians from 6,181.618 ms to 462.633 ms, an observed **13.36×**
validation-throughput improvement.

Independent review then froze v0.2.3 as `FAIL / CLOSURE-EDGE-SCOPE-01`: the implementation
does not wrongly admit the witness, but the closure specification leaves the scope of its
pinned edge relation ambiguous for unsupported specs. The final AI-5 report therefore has
`probe_execution_ok=true`, `promotion_allowed=false`, and `selection=no-change-control`.

```powershell
$candidate = '<isolated-v0.2.3-pnp-glc-i0-root>'
python .\ai5_aerec_probe_v023.py `
  --candidate-root $candidate `
  --repetitions 5 `
  --batch-snapshot `
  --output .\ai5_probe_report_v023_final_v0.4.json
python -m unittest -v .\test_ai5_aerec_probe_v023.py
```

## v0.2.4 continuation

The v0.2.4 adapter reuses the common engine and supplies only a version profile: five
manifest pins, v0.2.4 core pins, fixture/artifact paths, the repaired closure-scope audit,
and nine oracle-declaration regressions. This avoids cloning the entire probe for every
candidate version.

The isolated rerun passed 75/75 tests, all 42 fixture-manifest records, 20/20 closure
classifications, the original 7/7 scope checks, and 9/9 oracle-declaration negatives plus
3/3 positive controls. One immutable 3,664,976-byte snapshot reduced the sum of 42 fixture
medians from 11,415.630 ms to 639.523 ms: **17.85×** observed validation throughput.

Independent review nevertheless froze v0.2.4 as:

`FAIL / CLOSURE-JUDGMENT-COMPLETENESS-01 + ADVICE-DECL-LEDGER-01`.

The first blocker is an unresolved normative symbol: `GenericEnvelopeShape` is referenced
inside the normative judgment graph but not defined there. The second permits an accepted
record to combine a per-length truth-table advice declaration with uniform/no-generator/
no-access/zero-ledger evidence. Neither is a solver-correctness bypass or a P/NP result.
The final AI-5 report therefore selects `no-change-control`.

```powershell
$candidate = '<isolated-v0.2.4-pnp-glc-i0-root>'
python .\ai5_aerec_probe_v024.py `
  --candidate-root $candidate `
  --repetitions 3 `
  --batch-snapshot `
  --output .\ai5_probe_report_v024_final_v0.6.json
python -m unittest -v .\test_ai5_aerec_probe_v024.py
```

## Next adaptive iteration

Frozen v0.2.1 through v0.2.4 remain append-only failure history. The next version must add
a closed, machine-readable normative judgment dependency graph and a typed, bidirectionally
checked advice declaration. After a later candidate independently passes, the next safe
optimization is a dependency-closed minimal snapshot plus learned fail-fast ordering.
Correctness, provenance, declaration/ledger consistency, specification confluence, and
no-change remain hard constraints; speed is optimized only inside that admissible set.
