# BSD P5 v0.6 — uGPR Minimal Gate

This package advances the $(389.a1,p=11)$ route without re-running the closed Kurihara/Selmer or cyclotomic IMC stages.

New certified state:

$$
R_{11}\ne0,
$$

by the published Mazur--Stein--Tate computation, hence `P5-BOC-NZ11` is closed.

The main reduction is

$$
\mathrm{P5\!-LAT}_{11}
\iff
\mathrm{uGPR}_{11}
\iff
\mathrm{P5\!-INT}_{11}\land\mathrm{P5\!-PRIM}_{11}.
$$


No claim of BSD or of full GPR is made.

Run:

```bash
python scripts/check_padic_regulator_11.py
python scripts/check_gate_logic.py
python scripts/validate_package.py
```
