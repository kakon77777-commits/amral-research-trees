# PC-002 handoff

`PC-002-relative-regulator.zip` contains one manuscript, frozen inputs, both producers, their complete results, and `MANIFEST.json`. The full computations use Python 3.11+ standard library only. No predecessor checkout, network, Sage, or installed mathematics package is needed.

Unzip to an empty directory. From inside that directory:

```powershell
python -B code/relative_regulator.py --inputs INPUTS.json --output result-local.json
python -B code/cup_normalization.py --inputs INPUTS.json --series result-local.json --output cup-result-local.json
```

The new files should match `result.json` and `cup-result.json` by SHA-256. The manifest names every shipped payload and its hash. Python outputs use UTF-8 with LF newlines.

The results are analytic series in pinned modular-symbol periods and the corresponding Gamma0 Farey-cup normalization. The actual BF class, LR adjoint-period ratio, weight-X trace jet, and s11 were not produced in this round. The manuscript proves the stated precision and cancellation claims and identifies each remaining comparison.

In the research checkout, rebuild the ZIP with `python -B code/pack_pc002.py` from the tree root.
