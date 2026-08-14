# v0.5 Exact Census Report

**Status:** `v0.5 EXACT ARTIFACT CENSUS COMPLETE`  
**Repository:** `https://github.com/cocoxhuang/ants_xvii.git`  
**OLD:** `1a0489c3c3099dd0c248624e6621df73ae8f0d43`  
**CURRENT:** `31fae20c8df3f1f0383f41112b914d4995d5809d`

## Provenance finding: OLD base and OLD twist JSON are asynchronous

Git blob history shows that the OLD twist JSON was last changed at
`72867942accf94b9513857a2c0bae3895af8e9bc`.  It contains `39394` keys, exactly the
same label set as that commit's base file.  The selected OLD commit later contains
`40749` base labels but retains the same twist JSON blob, leaving
`1355` base labels without a materialized twist entry.
The OLD commit also changed `Algorithm2.py` after that JSON was generated (including
adding `disc_valuation_condition`) without changing the JSON blob.  Consequently,
the OLD twist map is an archived output artifact, not evidence of a fresh
end-to-end execution of the OLD source tree.

Those `1355` labels are listed in
`old_base_curves_missing_from_old_twist_map.csv`; they are exactly the curves added
after the twist file's last change and exactly the removed curves hitting a
3/5/7-isogeny gate.  There are no orphan OLD twist keys, and every stable base curve
has entries in both twist maps.  All counts below are therefore exact for the four
archived giant outputs.  They do not impute hypothetical results for missing entries.

## Q1 — Base-curve exact delta

```text
old    = 40749
new    = 36687
removed= 4062
added  = 0
stable = 36687
```

Both base partitions and the membership equation are exact PASS.

## Q2 — Algorithm 1 failure census

```text
ISOGENY_ONLY = 1353
A3_ONLY      = 2707
BOTH         = 2
UNEXPLAINED  = 0
```

Individual counts (overlap allowed): 3-isogeny `1233`, 5-isogeny `115`, 7-isogeny `7`.

Combination histogram:

```json
{
  "NONE": 2707,
  "{3}": 1233,
  "{5}": 115,
  "{7}": 7
}
```

The isogeny data comes from John Cremona's `ecdata` commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f`.  The coefficient `a3` was recomputed directly from each minimal model over `F_3`; all good-reduction values agree with the independent `aplist` data.

## Q3 — Unexplained removed curves

`0`.  The complete file is `algorithm1_unexplained_removed.csv` (header only when zero).

## Q4 — Upstream Algorithm 1 twist removals

`R_upstream = 24785` twist pairs.

These are isolated in `twists_removed_by_upstream_base_deletion.csv` and are not counted as Algorithm 2 removals.
This is the exact number present in the archived OLD twist JSON.  The
`1355` OLD base curves absent from that JSON contribute no
materialized pairs; the report does not pretend that Algorithm2 was rerun for them.

## Q5 — Stable-base Algorithm 2 delta

```text
stable removed = 21306
stable added   = 0
net delta      = -21306
```

Every stable curve is present in both maps.  Moreover, the CURRENT stable map is
exactly the OLD stable map with twists divisible by 3 removed; mismatch count
`0`.  This is an observed set identity, not merely
an inference from source-code text.

## Q6 — Stable-curve classes

```text
UNCHANGED   = 31250
SHRINK_ONLY = 5437
EXPAND_ONLY = 0
MIXED       = 0
```

## Q7 — MIXED curves

There are `0` MIXED curves.  The complete list is `algorithm2_mixed_curves.csv`.

_None._

## Q8 — Descriptive concentration of additions

By source:

_None._

Conductor-band counts are in `algorithm2_additions_by_conductor_band.csv`.  These are descriptive statistics only; no arithmetic cause is inferred from concentration.

## Q9 — Global accounting identity

```text
old_total_twist_pairs = 293482
new_total_twist_pairs = 247391
lhs                    = 46091
upstream_removed       = 24785
stable_removed         = 21306
stable_added           = 0
newbase_added          = 0
rhs                    = 46091
accounting identity    = PASS
```

## Priority cases

### Top 10 shrink

| curve | removed | added | net |
|---|---|---|---|
| 66166b1 | 16 | 0 | -16 |
| 104474a1 | 15 | 0 | -15 |
| 156854b1 | 15 | 0 | -15 |
| 302606a1 | 15 | 0 | -15 |
| 10349a1 | 14 | 0 | -14 |
| 39731a1 | 14 | 0 | -14 |
| 41869a1 | 14 | 0 | -14 |
| 62102a1 | 14 | 0 | -14 |
| 69074a1 | 14 | 0 | -14 |
| 77579b1 | 14 | 0 | -14 |

### Top 10 expand

_None._

Full top-50 lists are supplied as CSV.

## Completion gate

```json
{
  "algorithm1_all_removed_explained": true,
  "algorithm1_metadata_exact_coverage": true,
  "base_membership_equation": true,
  "base_new_partition": true,
  "base_old_partition": true,
  "current_commit_recorded": true,
  "four_raw_inputs_materialized": true,
  "four_raw_sha256_recorded": true,
  "new_base_labels_unique_and_parsed": true,
  "new_twist_keys_equal_base_set": true,
  "new_twist_schema_valid": true,
  "newbase_twists_isolated": true,
  "old_base_labels_unique_and_parsed": true,
  "old_commit_recorded": true,
  "old_missing_twist_keys_exactly_isogeny_gate_removed": true,
  "old_missing_twist_keys_exactly_post_generator_base_additions": true,
  "old_twist_keys_equal_last_generator_base_set": true,
  "old_twist_keys_subset_old_base_set": true,
  "old_twist_map_has_no_orphan_keys": true,
  "old_twist_schema_valid": true,
  "raw_git_blob_ids_exact": true,
  "stable_current_map_equals_old_map_filtered_by_3": true,
  "stable_curve_class_partition": true,
  "stable_domain_has_complete_old_and_new_twist_maps": true,
  "stable_removed_twists_all_divisible_by_3": true,
  "twist_accounting_identity": true,
  "upstream_twist_removals_isolated": true
}
```

This is an exact archived-output census of a theorem-producing computation.  It is
not a fresh end-to-end rerun of every OLD curve, and it is not a proof of the
Birch–Swinnerton-Dyer conjecture for all elliptic curves.
