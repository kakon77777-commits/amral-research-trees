#!/usr/bin/env python3
"""Backend-neutral Fouquet-Wan local H2 router.

This file contains only theorem logic.  It intentionally does not invent
Sage/Magma API calls for local p-isogeny computations.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class LocalEvidence:
    p: int
    profile: str = "FW17_EXACT"
    global_abs_irreducible: Optional[bool] = None
    potentially_multiplicative: Optional[bool] = None
    local_reducible_Fp: Optional[bool] = None
    phi_kernel_linear_Qp: Optional[bool] = None
    dual_kernel_linear_Qp: Optional[bool] = None
    equal_constituent_characters: Optional[bool] = None

def decide_h2(e: LocalEvidence):
    reasons = []

    if e.global_abs_irreducible is False:
        return "FAIL", ["GLOBAL_H1_FAIL"]

    if e.potentially_multiplicative is True:
        return "FAIL", ["POTENTIALLY_MULTIPLICATIVE_FORBIDDEN"]

    if e.local_reducible_Fp is False:
        # Local representation is irreducible over the coefficient field F_p,
        # hence cannot be a direct sum of F_p-valued characters.
        return "PASS", ["LOCAL_IRREDUCIBLE"]

    if e.local_reducible_Fp is None:
        return "UNKNOWN", ["INSUFFICIENT_LOCAL_DATA"]

    # Reducible branch.
    if e.p == 3:
        return "FAIL", ["P3_REDUCIBLE_FORBIDDEN"]

    if e.phi_kernel_linear_Qp is None or e.dual_kernel_linear_Qp is None:
        return "UNKNOWN", ["INSUFFICIENT_LOCAL_DATA"]

    if e.phi_kernel_linear_Qp:
        reasons.append("PHI_KERNEL_QUADRATIC")
    if e.dual_kernel_linear_Qp:
        reasons.append("DUAL_KERNEL_QUADRATIC")

    if reasons:
        return "FAIL", reasons

    if e.profile == "FW11_SIMPLE":
        if e.equal_constituent_characters is None:
            return "UNKNOWN", ["INSUFFICIENT_LOCAL_DATA"]
        if e.equal_constituent_characters:
            return "FAIL", ["FW11_EQUAL_CHARACTERS"]

    return "PASS", ["KERNEL_CHARACTER_TEST_PASS"]

if __name__ == "__main__":
    fixtures = [
        LocalEvidence(p=3, local_reducible_Fp=True),
        LocalEvidence(p=5, potentially_multiplicative=True),
        LocalEvidence(p=5, local_reducible_Fp=True,
                      phi_kernel_linear_Qp=True,
                      dual_kernel_linear_Qp=False),
        LocalEvidence(p=5, local_reducible_Fp=True,
                      phi_kernel_linear_Qp=False,
                      dual_kernel_linear_Qp=False),
        LocalEvidence(p=7, local_reducible_Fp=False),
    ]
    for x in fixtures:
        print(x, "=>", decide_h2(x))
