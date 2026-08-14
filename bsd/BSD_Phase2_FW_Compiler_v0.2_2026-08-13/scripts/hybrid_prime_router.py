#!/usr/bin/env python3
"""Phase 2 hybrid prime router skeleton.

No theorem claim is made when fixed-additive H1/H2 backends are UNKNOWN.
"""
from math import gcd
from functools import reduce

def gcd_list(xs):
    xs = [abs(int(x)) for x in xs if int(x) != 0]
    return reduce(gcd, xs) if xs else 0

def is_power_of_two(n):
    n = abs(int(n))
    return n > 0 and (n & (n - 1)) == 0

def fw_h3_witness(local_rows, p):
    for r in local_rows:
        ell = int(r["prime"])
        if ell == p:
            continue
        if int(r["conductor_exponent"]) != 1:
            continue
        if r["reduction"] != "nonsplit_multiplicative":
            continue
        if int(r["disc_valuation"]) % int(p) != 0:
            return ell
    return None

def uniform_fw_h3_certificate(local_rows):
    vals = [
        int(r["disc_valuation"])
        for r in local_rows
        if int(r["conductor_exponent"]) == 1
        and r["reduction"] == "nonsplit_multiplicative"
    ]
    g = gcd_list(vals)
    return {
        "nonsplit_witness_count": len(vals),
        "gcd_disc_valuations": g,
        "all_odd_prime_certificate": bool(vals) and is_power_of_two(g),
    }

def ordinary_ramification_certificate(local_rows):
    vals = [
        int(r["disc_valuation"])
        for r in local_rows
        if int(r["prime"]) % 2 == 1
        and int(r["conductor_exponent"]) == 1
        and r["reduction"] in ("split_multiplicative", "nonsplit_multiplicative")
    ]
    g = gcd_list(vals)
    return {
        "odd_multiplicative_witness_count": len(vals),
        "gcd_disc_valuations": g,
        "all_odd_good_prime_certificate": bool(vals) and is_power_of_two(g),
    }

def fw_h2_good_ordinary(a_p, p):
    """True means H2 passes in the good-ordinary shortcut."""
    return (int(a_p) * int(a_p) - 1) % int(p) != 0

def route_prime(reduction_type, divides_twist=False):
    if divides_twist:
        return "ADDITIVE_TWIST_EXISTING_THEOREM"
    if reduction_type == "good_ordinary":
        return "ORDINARY_EXISTING_THEOREM"
    if reduction_type == "good_supersingular":
        return "FW_SUPERSINGULAR"
    if reduction_type in ("split_multiplicative", "nonsplit_multiplicative"):
        return "FIXED_MULTIPLICATIVE_THEOREM"
    if reduction_type.startswith("additive"):
        return "FW_FIXED_ADDITIVE"
    return "UNKNOWN"
