# BSD P5 v0.5 — IMC Closure and GPR Bridge

This bundle advances the $389.a1$, $p=11$ rank-$2$ BSD route.

Main update:

$$
\boxed{\mathrm{P5\!\!-IMC}_{11}=\mathrm{CLOSED}.}
$$

The remaining classical one-prime obstruction is reduced to:

$$
\mathrm{P5\!\!-BOC\!\!-NZ}_{11}
+
\mathrm{P5\!\!-GPR}_{11}.
$$

`P5-BOC-NZ11` is a finite SageMath replay gate. `P5-GPR11` is the conceptual rank-$2$ Generalized Perrin--Riou comparison.

Files:

- `BSD_P5_IMC_Closure_and_GPR_Bridge_v0.5.md`: theorem/reduction paper.
- `source/P5_v0.5_canonical_source.md`: canonical UTF-8 source; byte-identical to the main paper.
- `results/imc_hypothesis_certificate.json`: BCS hypothesis and condition-(im) certificate.
- `results/p5_gate_status_v0.5.json`: machine-readable route state.
- `results/route_no_go.json`: audited non-routes.
- `scripts/check_condition_im.py`: exact unipotent quotient replay.
- `scripts/check_gate_logic.py`: state-machine checker.
- `scripts/replay_padic_regulator_11.sage`: next finite local certificate.
- `scripts/validate_package.py`: canonical-source and JSON validation.
- `NEXT_HANDOFF.md`: next research launch state.
