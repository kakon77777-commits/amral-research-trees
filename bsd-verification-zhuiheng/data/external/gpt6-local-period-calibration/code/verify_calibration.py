"""Exact tests of the proved formal calibration identity, not arithmetic BF data."""

from fractions import Fraction as F
from itertools import product
import argparse
import json
from pathlib import Path


def multiply(a, b, cap=6):
    out = [F(0)] * (cap+1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i+j <= cap:
                out[i+j] += x*y
    return out


def divide(a, b):
    if not b[0]:
        raise ZeroDivisionError("denominator must be a unit after removing its proved order")
    out = [F(0)] * len(a)
    for n, value in enumerate(a):
        out[n] = (value-sum(b[j]*out[n-j] for j in range(1,min(n+1,len(b))))) / b[0]
    return out


def formal_cases():
    count = 0
    log12 = F(7, 3)  # Exact model parameter, never presented as a p-adic log.
    jt = [F(0)] + [F((-1)**(j+1), j)/log12 for j in range(1,7)]
    kappa = [F(2,3), F(-5,7)]
    for n, C, A, A0, l0, s in product(range(6), (F(1),F(11),F(1,11)),
                                      (F(3),F(-2)), (F(5),F(1,3)),
                                      (F(9),F(-4)), (F(1),F(2))):
        # Weight-coordinate replacement X'=sX multiplies both leading
        # coefficients by s^-n. Retain that factor rather than assume n=1.
        shared = C / s**n
        target = [multiply(multiply([shared], [A,F(2)]), multiply(jt,[F(0),k,F(4)]))
                  for k in kappa]
        cal_reg = multiply(multiply([shared], [A0,F(-3)]), multiply(jt,[l0,F(8)]))
        observed = [A0*l0/A * component[2]/cal_reg[1] for component in target]
        assert observed == kappa
        count += 1
    return count


def falsifiers():
    # Residual transport is independent data: modifying only one line
    # scales the reconstructed class and must be visible.
    C, A, A0, l0, log12, kappa = map(F,(3,5,7,9,2,11))
    numerator = C*A*kappa/log12
    denominator = C*A0*l0/log12
    recover = lambda num, den: A0*l0/A * num/den
    tests = {
        "shared_frame_control": recover(13*numerator,13*denominator) == kappa,
        "independent_frame_error_detected": recover(2*numerator,denominator) != kappa,
        "second_derivative_without_factorial_error_detected": recover(2*numerator,denominator) == 2*kappa,
        "omit_A_ratio_error_detected": numerator/denominator != kappa,
    }
    try:
        divide([F(0),F(2)], [F(0),F(1)])
        tests["zero_denominator_rejected"] = False
    except ZeroDivisionError:
        tests["zero_denominator_rejected"] = True
    # Explicit hidden transport scalar: raw pre-leading normalization
    # can retain q_f, whereas the ratio of two projected classes cancels it.
    qf = F(17)
    tests["hidden_quotient_transport_detected"] = recover(qf*numerator, denominator) != kappa
    tests["common_quotient_transport_cancels"] = recover(qf*numerator,qf*denominator) == kappa
    # X^n(t^2 v + Xw): replacing X with t creates an earlier term.
    bivariate = {(3, 2): F(5), (4, 0): F(7)}
    first_weight = min(i for i, j in bivariate)
    sequential = {j: v for (i, j), v in bivariate.items() if i == first_weight}
    diagonal = {}
    for (i, j), v in bivariate.items():
        diagonal[i+j] = diagonal.get(i+j, F(0)) + v
    tests["diagonal_contamination_detected"] = (
        sequential == {2: F(5)} and diagonal == {5: F(5), 4: F(7)}
        and min(diagonal) < first_weight + min(sequential))
    assert all(tests.values())
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    result = {"status":"PASS", "exact_formal_cases":formal_cases(),
              "named_tests":falsifiers(), "arithmetic_BF_data":False,
              "proof_kind":"Formal identity proved in report; tests are finite witnesses only",
              "BSD_proved":False}
    encoded = json.dumps(result,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(encoded,encoding="utf-8",newline="\n")
    print(encoded,end="")


if __name__ == "__main__":
    main()
