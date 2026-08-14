# Source provenance

## Banwait–Huang computation repository

Repository: <https://github.com/cocoxhuang/ants_xvii>

```text
OLD       1a0489c3c3099dd0c248624e6621df73ae8f0d43
CURRENT   31fae20c8df3f1f0383f41112b914d4995d5809d
OLD twist JSON last-change commit
          72867942accf94b9513857a2c0bae3895af8e9bc
```

Exact tracked blob IDs:

```text
OLD ec_labels_500k.txt                 46ee5b24c93f4ceffc602f7a941f37003d3c5def
OLD twists_of_ec_labels_500k.json      67809e1210d95d13e69b731bcb458a711602e456
CURRENT ec_labels_500k.txt             6f2cce03973009223a7679fecad3c0c5b141ca52
CURRENT twists_of_ec_labels_500k.json  2135e1dd979fbcfb643923e5a11e0bf7e50fd244
72867942 ec_labels_500k.txt             6c68bce8973fbe80e37c26beef13ce7f122ec3cc
72867942 Algorithm2.py                 3a83d05a6b2e3cc72c6bf68311356d422e8201ec
OLD Algorithm2.py                      162d8bb6bc373334a66f8b42383481f2018d9b95
```

`scripts/extract_exact_git_blobs.py` uses `git cat-file blob`, bypassing Windows
checkout newline conversion. `results/raw_file_manifest.json` independently records
and checks Git blob SHA-1 plus SHA-256 for the materialized files.

The source snapshots and exact diffs are under:

```text
sources/generator_7286794/
sources/old/
sources/new/
sources/Algorithm1_generator_7286794_to_old_1a0489.diff
sources/Algorithm1_old_1a0489_to_current_31fae.diff
sources/Algorithm2_generator_7286794_to_old_1a0489.diff
sources/Algorithm2_old_1a0489_to_current_31fae.diff
sources/Algorithm2_generator_7286794_to_current_31fae.diff
```

The Git history establishes that OLD base and OLD `Algorithm2.py` changed after the
OLD twist JSON's last-change commit, while the JSON blob stayed identical. This is why
the report deliberately says **exact artifact census**, not fresh OLD-source replay.

## Elliptic-curve arithmetic data

Repository: <https://github.com/JohnCremona/ecdata>

```text
commit 25cec5ecfec8b9f016eb1631ac633194c2bed39f
```

Used data families:

```text
allcurves  exact minimal Weierstrass coefficients
allisog    isogeny-class matrices and model ordering
alllabels  Cremona-to-LMFDB label mapping
aplist     independent good-reduction a_p cross-checks
```

`inputs/metadata/algorithm1_removed_metadata.json` records the exact ecdata commit,
method, every source shard's SHA-256, exact source lines for each curve, direct
projective point counts over `F_3`, and validation checks. No live web value is used
as an unpinned arithmetic input.

The upstream `LICENSE`, `README.md`, and `docs/file-format.txt` are bundled under
`sources/ecdata_25cec5e/` for format and licensing context.

## Scope boundary

The four giant output files and their parsed sets are the authoritative inputs for
v0.5 accounting. Missing OLD JSON keys are reported, explained by history, and never
silently synthesized. Recomputing hypothetical OLD outputs for those absent keys
would be a separate Sage/LMFDB replay task and is intentionally not represented as
completed here.
