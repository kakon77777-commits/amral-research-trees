# BSD P5 Rank-2 Scalar Collapse v0.3

This package advances the $389.a1$, $p=11$ BSD project from a broad rank-$2$ leading-term problem to two explicitly typed gates:

- `P5-RAT`: rational/algebraic archimedean leading-term comparison;
- `P5-VAL11`: the $11$-adic valuation target, arithmetically forced to be zero once `P5-RAT` exists.

The package does not claim BSD. It records the exact circularity boundary in current higher-rank Kato/Gross--Zagier/Tamagawa routes and supplies a finite rational-reconstruction gate for any future rationality-plus-denominator theorem.

Run:

```bash
python scripts/compute_displayed_scalar.py
python scripts/validate_package.py
```

The rational reconstruction script requires a rigorous interval and a proved denominator bound:

```bash
python scripts/p5_rational_reconstruction_gate.py --lo 0.9999 --hi 1.0001 --B 10
```


## v0.4 ETNC escape audit

The ETNC route has been further typed. Fundamental-line and family-specialization technology exists, but the rank-2 trivial-character target requires a derived archimedean specialization (`P5-DERPER`). No non-circular theorem closing this gate was identified in the audited primary literature.
