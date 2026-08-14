# External Reference Audit — 2026-08-14

This audit spot-checks time-sensitive or structurally load-bearing external references used by the series. It is not a complete bibliography review.

## Paper 01 / Paper 09 — computational verification frontier

- David Barina, *Improved verification limit for the convergence of the Collatz conjecture*, Journal of Supercomputing 81, 810 (2025), reports complete convergence verification below $2^{71}$.
  - https://doi.org/10.1007/s11227-025-07337-0
- Barina's project page, generated 2026-07-28, still records 2025-01-15 as the date the $2^{71}$ milestone was completed.
  - https://pcbarina.fit.vut.cz/

Result: the manuscripts' $2^{71}$ calibration remains supported as of this audit.

## Paper 01 — Tao almost-all result

- Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562 / Forum of Mathematics, Pi (2022).
  - https://arxiv.org/abs/1909.03562

Result: the manuscript correctly distinguishes logarithmic-density almost-all control from a universal Collatz proof.

## Paper 09 — Angeltveit 2026

- Vigleik Angeltveit, *An improved algorithm for checking the Collatz conjecture for all n < 2^N*, arXiv:2602.10466 (2026).
  - https://arxiv.org/abs/2602.10466

The paper states that the $2^{N+1}$ verification takes less than twice the $2^N$ time, uses recursive least-significant-bit refinement, and discusses Descent, mod-9 Preimage, Path-Merging, and Odd-Even-Even sieves. It also explicitly notes that the fraction of integers requiring explicit checking tends to zero while the number still tends to infinity.

Result: the series' finite-frontier / quantifier-gap comparison is consistent with the cited source.

## Paper 07 — generalized Collatz condition

- Felipe Gonçalves, Rachel Greenfeld, Jose Madrid, *Generalized Collatz Maps with Almost Bounded Orbits*, arXiv:2111.06170.
  - https://arxiv.org/abs/2111.06170

Theorem 1.3 includes coprimality, the condition $q<p^{p/(p-1)}$, and the residue compatibility condition. For $p=2$, the displayed threshold becomes $q<4$.

Result: Paper 07's use of $m<4$ as a structural consistency comparison is supported, provided it remains distinguished from the stronger analytic theorem—which the manuscript explicitly does.

## Parity / 2-adic context

- Olivier Rozier, *Parity sequences of the 3x+1 map on the 2-adic integers and Euclidean embedding*, arXiv:1805.00133.
  - https://arxiv.org/abs/1805.00133
- Tong Niu, *Parity vectors and paradoxical sequences in the accelerated Collatz map*, arXiv:2605.13886 (2026).
  - https://arxiv.org/abs/2605.13886

Result: the cited parity-vector / $2$-adic context is a genuine active research line; no global-proof claim is inferred from it.
