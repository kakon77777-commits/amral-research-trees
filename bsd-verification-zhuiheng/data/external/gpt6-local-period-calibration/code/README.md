# Code

`calibrator.py` solves the rational Manin-symbol equations at prime level 19, isolates both signs using T2, checks five further Hecke eigenvalues against direct point counts, and evaluates ordinary and chi8-twisted measures modulo 11. Period conventions and the full rational vectors are emitted.

`verify_calibration.py` checks the coefficient identity with exact fractions over varied shared constants, vanishing orders and coordinates. Named falsifying witnesses distinguish an independent rescaling, a missing factorial, a wrong prefactor and a hidden quotient transport from valid common rescaling. Its inputs are formal examples, not computed BF classes.

`relative_regulator.py` builds new cusp measures from the pinned PC-002 vectors, computes the four analytic series and their quotient to degree below 121 modulo 11, and checks all coarse cells against one deeper measure layer.

`cup_normalization.py` computes the Farey cup pairing on the entire Manin cocycle space, checks its cusp radical, and forms the quotient invariant under four independent eigensymbol unit rescalings. It checks the supplied cocycles and binds its inputs to the relative-series receipt.

`pack_pc002.py` builds a deterministic self-contained handoff ZIP with a member hash manifest.
