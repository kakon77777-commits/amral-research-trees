#!/usr/bin/env python3
"""Skeleton only: no theorem claims without exact H2/H3 implementations."""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class FWCertificate:
    curve: str
    prime: int
    H1: str = "UNKNOWN"
    H2: str = "UNKNOWN"
    H3: str = "UNKNOWN"
    witness_ell: Optional[int] = None

    @property
    def decision(self):
        vals = (self.H1, self.H2, self.H3)
        if all(v == "PASS" for v in vals):
            return "FW_APPLICABLE"
        if any(v == "FAIL" for v in vals):
            return "FW_NOT_APPLICABLE"
        return "UNKNOWN"

def check_H1(curve, p):
    # TODO: exact residual absolute-irreducibility certificate from Sage/LMFDB.
    return "UNKNOWN"

def check_H2(curve, p):
    # CRITICAL TODO:
    # derive the exact weight-2 elliptic-curve local criterion first.
    # Do not replace by a guessed a_p congruence.
    return "UNKNOWN"

def check_H3(curve, p):
    # CRITICAL TODO:
    # exact Fouquet-Wan auxiliary-prime local condition.
    # Return (status, witness_ell).
    return "UNKNOWN", None

def route(curve, p):
    h3, ell = check_H3(curve,p)
    c = FWCertificate(
        curve=str(curve),
        prime=int(p),
        H1=check_H1(curve,p),
        H2=check_H2(curve,p),
        H3=h3,
        witness_ell=ell,
    )
    return {**asdict(c), "decision": c.decision}
