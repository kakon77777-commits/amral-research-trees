; FELRA proof obligation
; claim: reset_is_equivalent_to_the_correction_bound
; expression: (not (b <= 405) or 3 * (243 * y + b) <= 243 * (3 * y + 5)) and (not (3 * (243 * y + b) <= 243 * (3 * y + 5)) or b <= 405)

;
; The DOMAIN and the NEGATION of the claim are asserted, so `unsat` means
; no counterexample exists on that domain. `sat` is a counterexample.
; This is the DISCRIMINATING TWIN: the conclusion is flipped. A faithful export makes exactly one of the pair unsat.
(set-logic AUFNIRA)
(declare-const b Int)
(declare-const y Int)
(assert (and (>= b 0) (<= b 1000000)))
(assert (and (>= y 1) (<= y 1000000)))
(assert (and (or (not (<= b 405)) (<= (* 3 (+ (* 243 y) b)) (* 243 (+ (* 3 y) 5)))) (or (not (<= (* 3 (+ (* 243 y) b)) (* 243 (+ (* 3 y) 5)))) (<= b 405))))
(check-sat)
