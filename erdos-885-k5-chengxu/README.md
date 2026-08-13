# ERDOS-885 `k=5` — 數學戰士「澄序」

This is the durable research tree for 澄序's independent extra route on [ERDOS Problem 885](https://www.erdosproblems.com/885), produced on 2026-08-13 (Asia/Taipei) as MCDM Agent D. The work was performed independently from Agents A/B/C: their research trees were not edited and no unpublished material was sent to them.

## Status boundary

**The `k=5` problem is not solved here.** The duality reduction and displayed integer packets are exact. Every no-hit statement is exhaustive only over the stated finite domain and relative to the archived implementations. The rediscovered `K_(6,3)` precursor was already public; no literature novelty is claimed for it.

The central reduction is that an ERDOS-885 `K_(5,5)` witness transposes to a `K_(6,4)` factor-difference packet. The direct search found no `K_(6,4)` for canonical second difference `q <= 6000`. This yields a bounded necessary condition, not a global obstruction.

## Read in this order

1. [`reports/CHENGXU_DUALITY_ROUTE_REPORT.md`](./reports/CHENGXU_DUALITY_ROUTE_REPORT.md) — full mathematical narrative and claim boundaries; preserved byte-for-byte from the completed research run.
2. [`data/results.v1.json`](./data/results.v1.json) — machine-readable claims, bounds, counts, certificates, and provenance.
3. [`data/public-4x6-packets.v1.json`](./data/public-4x6-packets.v1.json) — the 71 public compact `4 x 6` packets used in the closure audit, snapshotted so replay does not depend on a mutable webpage.
4. [`code/`](./code/) — exact source plus offline and log-aggregation verifiers.
5. [`data/raw-logs/`](./data/raw-logs/) — original stdout/stderr captures, including completed, superseded, and interrupted chunks.

## Reproduce the compact checks

Observed environment: Windows 10 x64, Python 3.14.5, SymPy 1.14.0, and Rust 1.96.0. From this directory:

```powershell
python -m pip install -r .\code\requirements.txt
python .\code\verify_boundary_packets.py
python .\code\replay_public_4x6_snapshot.py
python .\code\verify_run_logs.py

$chengxuBuild = Join-Path $env:TEMP 'chengxu-erdos885-build'
New-Item -ItemType Directory -Force -Path $chengxuBuild | Out-Null
rustc -O .\code\search_dual_k64.rs -o (Join-Path $chengxuBuild 'search_dual_generic.exe')
& (Join-Path $chengxuBuild 'search_dual_generic.exe') --self-test
```

The full `q <= 6000` and multiplier searches are intentionally not part of the compact replay because they are expensive. Their disjoint raw runs and aggregate invariants are checked by `verify_run_logs.py`; rerun commands and bounds are in the report and source help text.

## Principal preserved hashes

| Artifact | SHA-256 |
|---|---|
| Original report | `76a17fefca115dda3f39be17faaa83ec3a27461ab391c1913db035324311b585` |
| Rust search source | `c16102ab05bd98a0b5c4768e4dbfb4b2b83741df1d3dee3340c5e2e5c3b9b379` |
| Boundary verifier | `fc06139c661042657d414c205c88b6a8f5fd3cc7b36b97328f1aa9a6adec340e` |
| Public-packet auditor | `f171b69f1ece22b6b879e0736ba55529cde8cf7710c7202897cd17f788061342` |
| Signed scaling search | `f98bffc79cb537586585bf845f86589789c8762e6c8edd0dcc099de46b26da2c` |
| Choudhry-family search | `4e97bcac4dc2f7255b289e36401e10801fca34f38b1cccefbf442d4d7cdf2acb` |

The Git commit containing this tree is the outer integrity and publication record. The original report's reference to a temporary directory describes where the independent run occurred; this tree is its subsequent public archive.
