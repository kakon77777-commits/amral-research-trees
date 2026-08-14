#!/usr/bin/env python3
"""Reproduce the scalar quotient from the decimals displayed by LMFDB.

The output is NUMERICAL EVIDENCE ONLY. The displayed inputs are rounded and
must never be treated as rigorous interval endpoints.
"""
from decimal import Decimal, getcontext
import json

getcontext().prec = 90
L2_over_2 = Decimal("0.75931650028842677023019260790")
omega = Decimal("4.9804251217101101506427155839")
reg = Decimal("0.15246017794314375162432475705")
product = omega * reg
ratio = L2_over_2 / product
out = {
    "L2_over_2_displayed": str(L2_over_2),
    "omega_displayed": str(omega),
    "regulator_displayed": str(reg),
    "omega_times_regulator": str(product),
    "displayed_scalar_ratio": str(ratio),
    "displayed_ratio_minus_one": str(ratio - Decimal(1)),
    "status": "NUMERICAL_ONLY_ROUNDED_INPUTS"
}
print(json.dumps(out, indent=2, sort_keys=True))
