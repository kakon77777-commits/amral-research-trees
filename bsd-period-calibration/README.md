# BSD period calibration

Independent continuation of the `bsd-verification-zhuiheng/` Attack 09–10 frontier, 2026-09-13, at Neo.K's direction. Current speaker identity: `unresolved`; historical resident names are not adopted.

Latest round: **PC-002** computes the relative analytic regulator modulo `(11,t^121)` and a Farey-cup normalization invariant under the four eigensymbol unit rescalings. Its leading coefficients are respectively 7 and 10 at degree 2. The full class vectors and the LR adjoint-period transport remain open.

- [PC-002 report and proofs](reports/PC-002-RELATIVE-REGULATOR.md)
- [Frozen inputs](data/pc002-inputs.json), [relative series and summands](data/pc002-relative-regulator.json), [cup matrices and normalized series](data/pc002-cup-normalization.json)
- [PC-002 handoff ZIP](handoff/PC-002-relative-regulator.zip) and [instructions](handoff/README.md)

PC-001 established a **derived cross-curve calibration identity**, accompanied by an exact level-19 modular-symbol computation providing a rank-zero calibration partner at p=11. The common Eisenstein comparison scalar cancels between two consistently projected classes. The genuine Beilinson–Flach class coordinates remain to be computed; no BSD conclusion is claimed.

- [Report and proof](reports/PC-001-CROSS-CURVE-CALIBRATION.md)
- [Exact calibrator producer](code/calibrator.py) and [output](data/calibrator-19a1.json)
- [Formal identity checks](code/verify_calibration.py) and [output](data/formal-calibration.json)
- [Sources and state](data/provenance.json)
- [Independent context's review](reports/PC-001-REVIEW.md)

Python 3.11+ standard library is sufficient. From this tree:

```powershell
python -B code/calibrator.py
python -B code/verify_calibration.py
python -B code/relative_regulator.py
python -B code/cup_normalization.py
```

The scripts print deterministic JSON results or summaries. `--output <new-path>` additionally saves the full result; the archived outputs were generated with that option. The arithmetic producers import none of the predecessor verification line's code. Their mathematical methods and accepted inputs are stated explicitly. Exact arithmetic is paired with written proofs of the comparison and precision statements; finite model checks are not substituted for arithmetic Galois classes.

The next scalar task is to match the Gamma0 cup normalization to LR's adjoint-period/Petersson convention. Genuine commonly normalized Beilinson–Flach class data are still required for the rank-two comparison. Each report records the boundary reached in its round.
