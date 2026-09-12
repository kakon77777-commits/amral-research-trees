# Code

`calibrator.py` solves the rational Manin-symbol equations at prime level 19, isolates both signs using T2, checks five further Hecke eigenvalues against direct point counts, and evaluates ordinary and chi8-twisted measures modulo 11. Period conventions and the full rational vectors are emitted.

`verify_calibration.py` checks the coefficient identity with exact fractions over varied shared constants, vanishing orders and coordinates. Named falsifying witnesses distinguish an independent rescaling, a missing factorial, a wrong prefactor and a hidden quotient transport from valid common rescaling. Its inputs are formal examples, not computed BF classes.
