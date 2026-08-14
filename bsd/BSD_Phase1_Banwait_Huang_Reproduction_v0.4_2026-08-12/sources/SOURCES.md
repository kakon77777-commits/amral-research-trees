# Sources

## Current paper

Banwait–Huang, arXiv:2601.16044.

Current paper reports:

- total conductor `<500000` curves: `3,064,705`;
- analytic rank 0: `1,170,876`;
- semistable analytic-rank-0: `274,888`;
- after optimal/composite-conductor restriction: `178,364`;
- Algorithm 1 accepted: `36,687`.

## GitHub one-commit comparison

Old:
`1a0489c3c3099dd0c248624e6621df73ae8f0d43`

Current:
`31fae20c8df3f1f0383f41112b914d4995d5809d`

Commit distance: 1.

Relevant file diff stats:

- `Algorithm1.py`: `+10/-12`
- `Algorithm2.py`: `+6/-51`
- `ec_labels_500k.txt`: `+2/-4064`
- `twists_of_ec_labels_500k.json`: `+1899/-53404`

Current `ec_labels_500k.txt` SHA:
`6f2cce03973009223a7679fecad3c0c5b141ca52`

Old `ec_labels_500k.txt` SHA:
`46ee5b24c93f4ceffc602f7a941f37003d3c5def`

## Limitation

GitHub connector exposes metadata/commit diffs but did not materialize the huge
old/current 500K output contents into this runtime. Full entry-level JSON/CSV
set differences remain a local-agent task.
