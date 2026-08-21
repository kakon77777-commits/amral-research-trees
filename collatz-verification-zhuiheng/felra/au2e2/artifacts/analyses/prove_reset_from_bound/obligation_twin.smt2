; FELRA proof obligation
; claim: reset_follows_from_the_correction_bound
; expression: not (b <= 405) or 3 * (243 * y + b) <= 243 * (3 * y + 5)
;
; The DOMAIN and the NEGATION of the claim are asserted, so `unsat` means
; no counterexample exists on that domain. `sat` is a counterexample.
; This is the DISCRIMINATING TWIN: the conclusion is flipped. A faithful export makes exactly one of the pair unsat.
(set-logic AUFNIRA)
(declare-const b Int)
(declare-const y Int)
(assert (and (>= b 0) (<= b 1000000)))
(assert (and (>= y 1) (<= y 1000000)))
(assert (or (not (<= b 405)) (<= (* 3 (+ (* 243 y) b)) (* 243 (+ (* 3 y) 5)))))
(check-sat)
