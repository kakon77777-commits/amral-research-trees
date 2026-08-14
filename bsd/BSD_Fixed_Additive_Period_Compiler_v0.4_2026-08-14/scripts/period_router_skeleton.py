#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional

@dataclass
class PeriodEvidence:
    p: int
    additive: Optional[bool] = None
    kodaira_type: Optional[str] = None
    potentially_ordinary: Optional[bool] = None
    local_twist_trivial_uniform: Optional[bool] = None
    optimality_uniform: Optional[bool] = None
    exact_manin_constant: Optional[int] = None
    modular_degree: Optional[int] = None
    conductor_vp: Optional[int] = None
    cns_p3_aux_prime_exists: Optional[bool] = None
    rational_singularity_certificate: Optional[bool] = None

def decide_period(e: PeriodEvidence):
    p = int(e.p)

    # Family-uniform Edixhoven branch.
    if (
        p >= 11
        and e.additive is True
        and e.local_twist_trivial_uniform is True
        and e.optimality_uniform is True
        and e.potentially_ordinary is not None
    ):
        excluded = (
            e.potentially_ordinary is True
            and e.kodaira_type in {"II", "III", "IV"}
        )
        if not excluded:
            return "PERIOD_PASS_UNIFORM_FAMILY", ["EDIXHOVEN_LOCAL"]

    # Per-curve exact Manin constant.
    if e.exact_manin_constant is not None:
        if e.exact_manin_constant % p != 0:
            return "PERIOD_PASS_THIS_CURVE", ["DIRECT_MANIN"]
        return "PERIOD_FAIL", ["DIRECT_MANIN_P_DIVIDES_C"]

    # Per-curve modular-degree certificate.
    if e.modular_degree is not None:
        if p >= 5 and e.modular_degree % p != 0:
            return "PERIOD_PASS_THIS_CURVE", ["CNS_MODULAR_DEGREE"]

        if p == 3 and e.modular_degree % 3 != 0:
            good_geometry = (
                (e.conductor_vp is not None and e.conductor_vp <= 2)
                or e.cns_p3_aux_prime_exists is True
                or e.rational_singularity_certificate is True
            )
            if good_geometry:
                return "PERIOD_PASS_THIS_CURVE", ["CNS_MODULAR_DEGREE_P3"]

    return "PERIOD_UNKNOWN", ["NO_UNIFORM_OR_EXACT_PERIOD_CERTIFICATE"]
