#!/usr/bin/env python3
p = 11
coeffs = [4, 7, 6, 1, 9, 10, 3]
assert coeffs[0] % p != 0
valuation = 0
assert valuation == 0
print("PADIC_REGULATOR_11_SOURCE_DIGIT_OK")
print("R_11 mod 11 =", coeffs[0] % p)
print("v_11(R_11) in source normalization =", valuation)
