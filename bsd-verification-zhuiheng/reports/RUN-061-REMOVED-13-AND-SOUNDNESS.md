# RUN-061 — `08`'s thirteen removed curves, row by row against the 500K census; and `03`'s six soundness gates, against what the package records

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`08_Removed_13_First_Failure_Closure`](../../../amral/public/bsd/phase1/files/08_Removed_13_First_Failure_Closure.md), [`03_Algorithm1_Soundness_Gates`](../../../amral/public/bsd/phase1/files/03_Algorithm1_Soundness_Gates.md)
**Tools:** [`src63_removed_13_and_soundness.py`](../code/src63_removed_13_and_soundness.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src63-removed-13-and-soundness.json`](../data/gate-logs/src63-removed-13-and-soundness.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: `08` closes the small fixture's 25 → 12 by giving each of the 13 removed curves a *first* failure — 9 × `P_ISOGENY_3`, 2 × `P_ISOGENY_5`, 1 × `P_ISOGENY_7`, 1 × `A3_ABS_3` — and notes that 26b1 also has `a₃ = −3` but the strict isogeny gate runs first. Every one of the thirteen is a row of the 500K removed census this line recomputed at RUN-055, so every cell is checkable. **13 of 13 agree** on first failure and on LMFDB label; **26b1 is the census's `BOTH` class** with `a₃ = −3` and a 7-isogeny, first failure `P_ISOGENY_7` exactly as `08` says; 142e1 has `|a₃| = 3` and no 3/5/7-isogeny. The fixture's 9/2/1/1 against 500K under the same first-failure ordering is **1,233 / 115 / 7 / 2,707** — the `a₃` share goes from one in thirteen to two in three — which is the extrapolation `11` §4 forbade, now measured. `03`'s six gates are a spec for the certificate pipeline; the package is an arithmetic census with no such pipeline, and says so, so **four of six are not applicable by scope**, S4 is the flag audit RUN-056 made, and **S6's seven provenance fields are 6 of 7 present** in the per-curve evidence — everything but a timestamp.**

---

## `08`'s table, every row

| curve | LMFDB, `08` | LMFDB, census | `08` says | census first failure | `a₃` | 500K class |
| --- | --- | --- | --- | --- | ---: | --- |
| 14a1 | 14.a6 | 14.a6 | `P_ISOGENY_3` | `P_ISOGENY_3` | −2 | `ISOGENY_ONLY` |
| 34a1 | 34.a4 | 34.a4 | `P_ISOGENY_3` | `P_ISOGENY_3` | −2 | `ISOGENY_ONLY` |
| 66c1 | 66.c3 | 66.c3 | `P_ISOGENY_5` | `P_ISOGENY_5` | 1 | `ISOGENY_ONLY` |
| 26a1 | 26.a2 | 26.a2 | `P_ISOGENY_3` | `P_ISOGENY_3` | 1 | `ISOGENY_ONLY` |
| **26b1** | 26.b2 | 26.b2 | `P_ISOGENY_7` | `P_ISOGENY_7` | **−3** | **`BOTH`** |
| 35a1 | 35.a3 | 35.a3 | `P_ISOGENY_3` | `P_ISOGENY_3` | 1 | `ISOGENY_ONLY` |
| 38a1 | 38.a3 | 38.a3 | `P_ISOGENY_3` | `P_ISOGENY_3` | 1 | `ISOGENY_ONLY` |
| 38b1 | 38.b2 | 38.b2 | `P_ISOGENY_5` | `P_ISOGENY_5` | −1 | `ISOGENY_ONLY` |
| 106a1 | 106.c2 | 106.c2 | `P_ISOGENY_3` | `P_ISOGENY_3` | −2 | `ISOGENY_ONLY` |
| 110c1 | 110.a1 | 110.a1 | `P_ISOGENY_3` | `P_ISOGENY_3` | 1 | `ISOGENY_ONLY` |
| 110b1 | 110.c1 | 110.c1 | `P_ISOGENY_3` | `P_ISOGENY_3` | 1 | `ISOGENY_ONLY` |
| **142e1** | 142.c1 | 142.c1 | `A3_ABS_3` | `A3_ABS_3` | **3** | `A3_ONLY` |
| 142d1 | 142.e2 | 142.e2 | `P_ISOGENY_3` | `P_ISOGENY_3` | 1 | `ISOGENY_ONLY` |

**13 of 13.** The "first failure" is computed here from the census columns
under `08`'s stated ordering — strict isogeny gate first, smallest prime first,
then `a₃` — and it reproduces `08`'s column without exception. 26b1's secondary
`a₃ = −3` is the census's `BOTH` class, one of only two such curves in 4,062.

## The fixture against 500K

| first failure | `<150` fixture | 500K |
| --- | ---: | ---: |
| `P_ISOGENY_3` | 9 | 1,233 |
| `P_ISOGENY_5` | 2 | 115 |
| `P_ISOGENY_7` | 1 | 7 |
| `A3_ABS_3` | 1 | 2,707 |
| `a₃` share | 1 / 13 ≈ 7.7 % | 2,707 / 4,062 ≈ **66.6 %** |

`08` is right about its thirteen curves and would have been wrong as a proxy
for the 4,062 — which is what `11` §4 said, before v0.5 could measure it.

## `03`'s six gates

| gate | state |
| --- | --- |
| S1 analytic Ш must not impersonate actual Ш | **N/A by scope** — no Ш is computed or recorded; no descent ran |
| S2 `dim Ш[2]` must not impersonate `ord₂ #Ш` | **N/A by scope** |
| S3 a timeout is `UNKNOWN`, not a failure | **N/A by scope** — no mwrank ran |
| S4 testing flags downgrade the whole run | **audited at RUN-056** — the flags appear only in archived source, never as recorded values |
| S5 the `𝒮 ≠ ∅` production gate is deterministic | **N/A by scope** — Algorithm 2's certificate machinery is not run |
| S6 every PASS carries seven provenance fields | **6 of 7** |

### S6, field by field

| field | in the per-curve evidence |
| --- | --- |
| predicate | ✔ `a3_computation.formula` |
| value | ✔ `a3` |
| evidence_type | ✔ `evidence.allcurves_line` + path |
| backend | ✔ `provenance.method` |
| semantic_version | ✔ `schema_version` |
| file/commit SHA | ✔ `ecdata_commit`, `current_algorithm_commit`, per-shard SHA-256 |
| **timestamp** | **✘** — none in the metadata; `run.log` carries a status line, not a time |

Scoring the four N/A gates as failures would hold the package to a pipeline it
says it does not contain — RUN-054's discipline on `05`, RUN-056's on `02` §6.
S6 is the one that binds, and it binds field by field.

## The drill

**260 defects, 260 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 52 controls undisturbed, over 90 checks.

The 4 planted for this gate, each turning `removed-13-and-soundness` red and nothing else:

| planted defect | went red |
| --- | --- |
| 08's ordering is applied a_3 first, so 26b1 becomes A3_ABS_3 | `removed-13-and-soundness` |
| 26b1 is reported ISOGENY_ONLY, losing the BOTH class | `removed-13-and-soundness` |
| S6's timestamp is reported present | `removed-13-and-soundness` |
| the fixture-vs-500K sum drops the BOTH class | `removed-13-and-soundness` |


## What this round does not claim

* **Nothing about the 25 → 12 fixture itself.** The 12 survivors and the
  `<150` twist fixture are not in the package; the 13 removed curves are
  checked because they are also 500K rows.
* **"First failure" is `08`'s ordering applied to the census's columns.** The
  census records failure *classes*, not an order; the order is `08`'s and is
  reproduced, not measured.
* **The missing timestamp is a fact about the metadata JSON.** The package's
  zip carries file dates; S6 asks for a field.
* **N/A by scope is the package's scope.** Whether an arithmetic census ought to
  carry a certificate pipeline is not this arm's question.
