# BSD period calibration

Independent continuation of the `bsd-verification-zhuiheng/` Attack 09–10 frontier, 2026-09-13, at Neo.K's direction. Current speaker identity: `unresolved`; historical resident names are not adopted.

The result of this round is a **derived cross-curve calibration identity**, accompanied by an exact level-19 modular-symbol computation providing a rank-zero calibration partner at p=11. The common Eisenstein comparison scalar cancels between two consistently projected classes. The genuine Beilinson–Flach class coordinates remain to be computed; no BSD conclusion is claimed.

- [Report and proof](reports/PC-001-CROSS-CURVE-CALIBRATION.md)
- [Exact calibrator producer](code/calibrator.py) and [output](data/calibrator-19a1.json)
- [Formal identity checks](code/verify_calibration.py) and [output](data/formal-calibration.json)
- [Sources and state](data/provenance.json)
- [Independent context's review](reports/PC-001-REVIEW.md)

Python 3.11+ standard library is sufficient. From this tree:

```powershell
python -B code/calibrator.py
python -B code/verify_calibration.py
```

Both scripts print deterministic JSON. `--output <new-path>` additionally saves it; the archived outputs were generated with that option. The arithmetic producer imports none of the predecessor's code. Its mathematical method is stated explicitly, including the same standard Manin/Heilbronn mathematics used by that verification line. Exact arithmetic is paired with a written proof of the abstract comparison; finite model checks are not substituted for arithmetic Galois classes.

The first next task is to construct one genuine, commonly normalized Beilinson–Flach calibration observable and the target class vector. The report distinguishes a safe quotient after Eisenstein specialization from a proposed earlier normalization whose remaining transport scalar has not been resolved.
