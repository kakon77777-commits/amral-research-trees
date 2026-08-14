# BSD P5 v1.3 package

This package advances the 389.a1, p=11 rank-2 BSD reduction from the norm-Selmer core vertex to an explicit finite determinant/Bockstein model.

Key exact output: `det(B_N) = 2 X_397 X_991` over F_11, while the inherited modular initial form is `6 X_397 X_991` in the deterministic normalization. The invariant result is equality of the generated mixed augmentation lines, not the scalar ratio 3.

Run:

```bash
python scripts/replay_finite_bockstein.py
```

Then inspect `GATE_STATE.json` and `NEXT_HANDOFF.md`.
