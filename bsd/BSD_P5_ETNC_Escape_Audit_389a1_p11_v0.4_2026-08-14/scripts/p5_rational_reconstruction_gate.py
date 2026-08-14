#!/usr/bin/env python3
"""Finite rational-reconstruction gate for BSD P5.

This script does NOT prove rationality and does NOT turn ordinary floating-point
numbers into a proof. It only implements the final uniqueness implication:

If x is already proved rational with reduced denominator <= B, and a rigorous
interval [lo, hi] for x is contained in (1-1/(2B^2), 1+1/(2B^2)), then x=1.

All inputs are decimal strings so the interval arithmetic here is exact at the
level of the supplied rational decimals.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext

getcontext().prec = 120


def certify_one(lo: Decimal, hi: Decimal, B: int) -> dict:
    if B < 1:
        raise ValueError("B must be >= 1")
    if lo > hi:
        raise ValueError("lo must be <= hi")
    threshold = Decimal(1) / (Decimal(2) * Decimal(B) * Decimal(B))
    lower_target = Decimal(1) - threshold
    upper_target = Decimal(1) + threshold
    passed = lo > lower_target and hi < upper_target
    return {
        "lo": str(lo),
        "hi": str(hi),
        "denominator_bound": B,
        "half_separation_threshold": str(threshold),
        "target_interval": [str(lower_target), str(upper_target)],
        "uniqueness_gate_pass": passed,
        "conclusion_if_rationality_and_bound_are_proved": "x = 1" if passed else "NO_CONCLUSION"
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lo", required=True, help="rigorous lower bound for B_infty")
    parser.add_argument("--hi", required=True, help="rigorous upper bound for B_infty")
    parser.add_argument("--B", type=int, required=True, help="proved upper bound for reduced denominator")
    args = parser.parse_args()
    result = certify_one(Decimal(args.lo), Decimal(args.hi), args.B)
    import json
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
