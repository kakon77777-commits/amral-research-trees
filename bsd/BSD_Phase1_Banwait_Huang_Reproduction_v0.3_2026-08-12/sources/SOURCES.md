# Sources and Evidence

## Official repository

Repository: `cocoxhuang/ants_xvii`

Old commit:
`1a0489c3c3099dd0c248624e6621df73ae8f0d43`
(2026-05-22, `major update to algorithms`)

Current commit:
`31fae20c8df3f1f0383f41112b914d4995d5809d`
(2026-06-03, `update algos, rerun computations`)

The current commit has the old commit as its direct parent.

Relevant official files:

- `Algorithm1.py`
- `Algorithm2.py`
- `output/ec_labels_150.txt`
- `output/twists_of_ec_labels_150.json`

## Primary curve data

LMFDB / Cremona data were used for rational isogeny/torsion identification.

Representative primary URLs:

- https://www.lmfdb.org/EllipticCurve/Q/34a1/
- https://www.lmfdb.org/EllipticCurve/Q/110/c/
- https://www.lmfdb.org/EllipticCurve/Q/38/a/
- https://www.lmfdb.org/EllipticCurve/Q/38b1/
- https://www.lmfdb.org/EllipticCurve/Q/106/c/
- https://www.lmfdb.org/EllipticCurve/Q/142e2/

Cremona's *Algorithms for Modular Elliptic Curves* table was used to cross-check
the conductor-110 and conductor-142 old Cremona-label classes.

## Exact computation

For Cremona `142e1`, the model

`y^2 + xy = x^3 - x^2 - 2626x + 52244`

is checked directly modulo 3 by `src/verify_142e1_a3.py`.

The script enumerates all 9 affine pairs in F_3^2 and finds none, so with the
point at infinity:

`#E(F_3)=1`, hence `a_3=3`.
