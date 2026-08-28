#!/usr/bin/env python3
"""Recheck of Hard-Zeta Phase II Round A-U.2d.5 (source item 51).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Annular Farey-Residue Coupling* (v0.1, 2026-08-13).
Ships a checker, its report, a constants frontier, a source-validation record and
a stdout transcript.

## Two more results that need no hypothetical object

RUN-032 noted that A-U.2d.4 was the first round in this line whose core held on
orbits that exist. A-U.2d.5 adds two more of the same kind, and both are pure
integer arithmetic:

**Section 4 — exact exponent codes.** For a code `w = (a_1..a_k)` with
`Q = sum a_j` and `B_w = sum_j 3^(k-1-j) 2^(A_j)`, every realization from odd
source `x` to odd endpoint `z` satisfies `2^Q z = 3^k x + B_w`. Hence one code
selects one source class mod `2^(Q+1)` and one endpoint class mod `3^k`, and a
repeated code forces `|x-x'| >= 2^(Q+1)` and `|z-z'| >= 2*3^k`. No CASP
hypothesis appears anywhere in that.

**Section 6 — all B-sources are 3 mod 4.** If the first crossing has `L >= 2`
then `s+1` is a proper subcritical prefix, so `q_(s+1) < beta < 2`, so
`q_(s+1) = 1`, so `v2(3y+1) = 1`, so `y = 3 (mod 4)`. Again true of any orbit.

## Exactly, again

`delta_u < delta_s` is `3^(u-s) < 2^(K_u-K_s)`; `U_beta(L)` is rational because
`2^(-{beta j}) = 2^(floor(beta j))/3^j` (RUN-027); the annulus and determinant
quantities are `a*beta + b` for integers a, b (RUN-032). Nothing here needs a
floating-point number, and the shipped checker reports
`max_float_residual = 1.9e-12` for the same identities.

## Artifacts

Standing rule since item 35: recompute independently, never re-run the shipped
script, and check whether the shipped records are what they claim. This bundle's
constants are also compared against item 50's, because the two ship the same
quantities and RUN-032 measured item 50's drift.

Usage:
  python code/src51_annular_residue.py --bundle DIR [--limit N] [--codes N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import re
import sys
from fractions import Fraction

PAPER = "Hard_Zeta_Phase_II_Round_AU2d5_Annular_Farey_Residue_Coupling_v0.1.md"
CONSTANTS = "Hard_Zeta_AU2d5_constants_frontier.json"
CHECKER_REPORT = "Hard_Zeta_AU2d5_checker_report.json"
CHECKER_STDOUT = "checker_stdout.txt"
VALIDATION = "SOURCE_VALIDATION_AU2d5.json"

#: what RUN-032 measured in item 50's constants JSON, so the two can be compared
ITEM50_CONSTANTS = {
    "theta_star": 0.19544992572902825,
    "sigma_star": 0.8365051337388005,
    "dense_overlap_lower_exponent": 0.16349486626119947,
    "congestion_upper_power": 0.8045500742709718,
}


# ---------------------------------------------------------------------------
# orbit machinery, integers only
# ---------------------------------------------------------------------------

def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def accelerated(start: int, max_steps: int = 6000) -> tuple[list[int], list[int]]:
    y, word, values = start, [], [start]
    while y != 1 and len(word) < max_steps:
        t = 3 * y + 1
        k = v2(t)
        word.append(k)
        y = t >> k
        values.append(y)
    return word, values


def cumulative(word: list[int]) -> list[int]:
    out, run = [0], 0
    for q in word:
        run += q
        out.append(run)
    return out


def slack_is_smaller(K: list[int], u: int, s: int) -> bool:
    """delta_u < delta_s, as 3^(u-s) < 2^(K_u-K_s). Both signs handled."""
    return Fraction(3) ** (u - s) < Fraction(2) ** (K[u] - K[s])


def first_crossings(K: list[int], n: int) -> list[int | None]:
    out: list[int | None] = [None] * (n + 1)
    stack: list[int] = []
    for u in range(n + 1):
        while stack and slack_is_smaller(K, u, stack[-1]):
            out[stack.pop()] = u
        stack.append(u)
    return out


def u_beta(L: int) -> Fraction:
    """U_beta(L) = (1/3) sum_{j<L} 2^(-{beta j}), exactly (RUN-027).

    `2^(-{beta j}) = 2^(floor(beta j)) / 3^j`, and `floor(beta j)` is a bit
    length, so the whole sum is rational and no logarithm is evaluated.
    """
    total = Fraction(0)
    p3 = 1
    for j in range(L):
        total += Fraction(1 << (p3.bit_length() - 1), p3)
        p3 *= 3
    return total / 3


# ---------------------------------------------------------------------------
# section 4 — exact exponent codes
# ---------------------------------------------------------------------------

def b_of_code(code: tuple[int, ...]) -> tuple[int, int, int]:
    """(B_w, Q, k) for an accelerated exponent code."""
    k = len(code)
    partial = 0
    b = 0
    for j in range(k):
        b += 3 ** (k - 1 - j) * (1 << partial)
        partial += code[j]
    return b, partial, k


def run_code(x: int, k: int) -> tuple[tuple[int, ...], int]:
    """k accelerated steps from odd x; returns (code, endpoint)."""
    code, y = [], x
    for _ in range(k):
        t = 3 * y + 1
        a = v2(t)
        code.append(a)
        y = t >> a
    return tuple(code), y


def check_exact_codes(trials: int, seed: int) -> dict:
    rng = random.Random(seed)
    affine_bad = source_class_bad = endpoint_class_bad = 0
    reverse_bad = 0
    checked = 0
    reverse_checked = 0
    for _ in range(trials):
        x = 2 * rng.randrange(1, 5_000_000) + 1
        k = rng.randint(1, 9)
        code, z = run_code(x, k)
        b, q, kk = b_of_code(code)
        checked += 1
        if (1 << q) * z != 3 ** kk * x + b:
            affine_bad += 1
        modulus = 1 << (q + 1)
        want = (pow(3, -kk, modulus) * ((1 << q) - b)) % modulus
        if x % modulus != want:
            source_class_bad += 1
        mod3 = 3 ** kk
        if z % mod3 != (pow(2, -q, mod3) * b) % mod3:
            endpoint_class_bad += 1

        # the other direction: EVERY odd member of that class must realize w.
        # A class check that only looks at sources already known to realize the
        # code cannot distinguish "one class" from "some class".
        for step in range(1, 4):
            other = x + step * modulus
            if other % 2 == 0:
                continue
            reverse_checked += 1
            if run_code(other, kk)[0] != code:
                reverse_bad += 1
    return {
        "trials": checked,
        "affine_identity_violations": affine_bad,
        "source_class_violations": source_class_bad,
        "endpoint_class_violations": endpoint_class_bad,
        "class_members_checked_in_reverse": reverse_checked,
        "class_members_failing_to_realize_the_code": reverse_bad,
    }


def check_bi_exact_separation(trials: int, seed: int) -> dict:
    """Repeated code => source gap 2^(Q+1)m and endpoint gap 2*3^k m."""
    rng = random.Random(seed + 1)
    pairs = source_bad = endpoint_bad = ratio_bad = 0
    min_source_ratio = None
    for _ in range(trials):
        x = 2 * rng.randrange(1, 2_000_000) + 1
        k = rng.randint(1, 8)
        code, z = run_code(x, k)
        b, q, kk = b_of_code(code)
        modulus = 1 << (q + 1)
        m = rng.randint(1, 6)
        x2 = x + m * modulus
        code2, z2 = run_code(x2, kk)
        if code2 != code:
            continue
        pairs += 1
        if (x2 - x) % modulus != 0 or abs(x2 - x) < modulus:
            source_bad += 1
        if (z2 - z) != 2 * 3 ** kk * m:
            endpoint_bad += 1
        if abs(z2 - z) < 2 * 3 ** kk:
            ratio_bad += 1
        ratio = abs(x2 - x) // modulus
        min_source_ratio = ratio if min_source_ratio is None else min(min_source_ratio, ratio)
    return {
        "repeated_code_pairs": pairs,
        "source_gap_not_a_multiple_of_2^(Q+1)": source_bad,
        "endpoint_gap_not_2*3^k*m": endpoint_bad,
        "endpoint_gap_below_2*3^k": ratio_bad,
        "smallest_source_gap_in_units_of_2^(Q+1)": min_source_ratio,
    }


def check_shipped_examples(report: dict) -> dict:
    """The checker's own sample pairs, recomputed from the code alone."""
    rows, bad = [], []
    for ex in report.get("sample_bi_exact_examples", []):
        code = tuple(ex["code"])
        b, q, k = b_of_code(code)
        ok_q = q == ex["Q"]
        ok_k = k == ex["k"]
        c1, z1 = run_code(ex["source_1"], k)
        c2, z2 = run_code(ex["source_2"], k)
        ok_codes = c1 == code and c2 == code
        ok_end = z1 == ex["endpoint_1"] and z2 == ex["endpoint_2"]
        ok_sgap = ex["source_gap"] == ex["source_2"] - ex["source_1"]
        ok_egap = ex["endpoint_gap"] == ex["endpoint_2"] - ex["endpoint_1"]
        modulus = 1 << (q + 1)
        ok_sep = ex["source_gap"] % modulus == 0 and ex["endpoint_gap"] % (2 * 3 ** k) == 0
        entry = {"code": list(code), "Q_agrees": ok_q, "k_agrees": ok_k,
                 "both_sources_realize_the_code": ok_codes,
                 "endpoints_agree": ok_end,
                 "gaps_agree": ok_sgap and ok_egap,
                 "separation_multiples_hold": ok_sep}
        rows.append(entry)
        if not all(v for v in entry.values() if isinstance(v, bool)):
            bad.append(entry)
    return {"examples": rows, "examples_checked": len(rows), "disagreeing": bad}


# ---------------------------------------------------------------------------
# sections 5, 6 and the determinants, on real orbits
# ---------------------------------------------------------------------------

def lin(a: tuple[int, int], b: tuple[int, int], sign: int = 1) -> tuple[int, int]:
    return (a[0] + sign * b[0], a[1] + sign * b[1])


def delta(K: list[int], m: int) -> tuple[int, int]:
    return (m, -K[m])


def check_orbit_structure(limit: int) -> dict:
    totals = {
        "orbits": 0, "sources": 0, "L_equals_1": 0, "L_at_least_2": 0,
        "q_next_not_one": 0, "source_not_3_mod_4": 0,
        "laminarity_violations": 0, "nested_pairs": 0, "disjoint_pairs": 0,
        "renewal_edges": 0, "renewal_identity_errors": 0,
        "plateau_edges": 0, "drop_edges": 0,
        "plateau_determinant_not_a_positive_integer": 0,
        "drop_determinant_not_a_positive_integer": 0,
        "chains_with_increasing_sources": 0,
        "chains_inside_the_source_corridor": 0,
        "chains_outside_the_source_corridor": 0,
        "source_gap_below_4": 0,
        "depth_cap_violations": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e = first_crossings(K, n)
        totals["orbits"] += 1

        for s, end in enumerate(e):
            if end is None or s >= n:
                continue
            totals["sources"] += 1
            L = end - s
            if L == 1:
                totals["L_equals_1"] += 1
                continue
            totals["L_at_least_2"] += 1
            if word[s] != 1:
                totals["q_next_not_one"] += 1
            if values[s] % 4 != 3:
                totals["source_not_3_mod_4"] += 1

        intervals = [(s, u) for s, u in enumerate(e) if u is not None]
        if start <= 999:                     # laminarity is quadratic; sample it
            for i in range(len(intervals)):
                a, b = intervals[i]
                for j in range(i + 1, len(intervals)):
                    c, d = intervals[j]
                    if b <= c or d <= a:
                        totals["disjoint_pairs"] += 1
                    elif (a <= c and d <= b) or (c <= a and b <= d):
                        totals["nested_pairs"] += 1
                    else:
                        totals["laminarity_violations"] += 1

        for s_i, e_i in intervals:
            s_j = s_i + 1
            if s_j >= e_i or e[s_j] is None or e[s_j] > e_i:
                continue
            e_j = e[s_j]
            totals["renewal_edges"] += 1
            g_i, p_i = s_j - s_i, K[s_j] - K[s_i]
            h_i, r_i = e_i - e_j, K[e_i] - K[e_j]
            A = (g_i, -p_i)
            D_i = lin(delta(K, s_i), delta(K, e_i), -1)
            D_j = lin(delta(K, s_j), delta(K, e_j), -1)
            E = (-h_i, r_i)
            if lin(lin(A, D_i), lin(D_j, E), -1) != (0, 0):
                totals["renewal_identity_errors"] += 1
            if h_i == 0:
                totals["plateau_edges"] += 1
                # Pi_i = g_i D_{i+1} + L_{i+1} A_i, with L_{i+1} = e_j - s_j
                L_j = e_j - s_j
                combo = lin((g_i * D_j[0], g_i * D_j[1]), (L_j * A[0], L_j * A[1]))
                if combo[0] != 0 or combo[1] < 1:
                    totals["plateau_determinant_not_a_positive_integer"] += 1
            else:
                totals["drop_edges"] += 1
                combo = lin((g_i * E[0], g_i * E[1]), (h_i * A[0], h_i * A[1]))
                if combo[0] != 0 or combo[1] < 1:
                    totals["drop_determinant_not_a_positive_integer"] += 1

        # section 6's chain cap, on chains that satisfy its own premise
        for s0, e0 in intervals:
            chain, cur = [s0], s0
            while True:
                nxt = cur + 1
                if nxt >= e0 or e[nxt] is None or e[nxt] > e0:
                    break
                chain.append(nxt)
                cur = nxt
            ys = [values[i] for i in chain if e[i] is not None and e[i] - i >= 2]
            if len(ys) < 2 or any(b <= a for a, b in zip(ys, ys[1:])):
                continue                      # premise: distinct and INCREASING
            totals["chains_with_increasing_sources"] += 1
            if ys[-1] - ys[0] < 4 * (len(ys) - 1):
                totals["source_gap_below_4"] += 1
            r, L = len(ys), e0 - s0
            # Section 6 derives its cap from the SOURCE CORRIDOR
            #     4(r-1) < y_r - y_1 < U_beta(L),
            # and the right-hand bound is a B-survival property, not something a
            # real orbit owes anyone. Checking `r < 1 + U_beta(L)/4` without it
            # is imposing the conclusion on chains that never satisfied the
            # hypothesis -- which flagged 10214 of 10214, a rate that is a
            # statement about the check and not about the round.
            if ys[-1] - ys[0] < u_beta(L):
                totals["chains_inside_the_source_corridor"] += 1
                if not Fraction(r) < 1 + u_beta(L) / 4:
                    totals["depth_cap_violations"] += 1
            else:
                totals["chains_outside_the_source_corridor"] += 1
    return totals


# ---------------------------------------------------------------------------

def check_constants(constants: dict) -> dict:
    import struct

    rho = Fraction("4.1164")
    exact = {
        "rho_star": rho,
        "theta_star": 1 / (rho + 1),
        "congestion_power_rho_over_rho_plus_1": rho / (rho + 1),
        "disjoint_backbone_power": 1 / (1 + 1 / (rho + 1)),
        "dense_overlap_required_power": 1 - 1 / (1 + 1 / (rho + 1)),
    }
    published = constants["constants"]

    def bits(x: float) -> int:
        return struct.unpack("<q", struct.pack("<d", x))[0]

    rows, wrong = {}, []
    for name, value in exact.items():
        if name not in published:
            continue
        shown = published[name]
        nearest = float(value)
        rows[name] = {
            "exact": "%d/%d" % (value.numerator, value.denominator),
            "published": shown,
            "ulps_from_the_nearest_double": abs(bits(shown) - bits(nearest)),
            "relative_error": "%.2e" % float(abs(Fraction(shown) - value) / value),
        }
        if float(abs(Fraction(shown) - value) / value) >= 1e-15:
            wrong.append(name)

    # eta_beta is transcendental, not rational
    import mpmath as mp
    with mp.workdps(60):
        eta = 1 / (6 * mp.log(2))
        eta_drift = abs(bits(published["eta_beta"]) - bits(float(eta)))

    # the same quantities as item 50, which RUN-032 measured
    same = {
        "theta_star": ("theta_star", ITEM50_CONSTANTS["theta_star"]),
        "disjoint_backbone_power": ("sigma_star", ITEM50_CONSTANTS["sigma_star"]),
        "dense_overlap_required_power":
            ("dense_overlap_lower_exponent", ITEM50_CONSTANTS["dense_overlap_lower_exponent"]),
        "congestion_power_rho_over_rho_plus_1":
            ("congestion_upper_power", ITEM50_CONSTANTS["congestion_upper_power"]),
    }
    cross = {}
    for here, (there_name, there_value) in same.items():
        if here not in published:
            continue
        cross[here] = {
            "item_51": published[here],
            "item_50_as": there_name,
            "item_50": there_value,
            "agree": published[here] == there_value,
            "item_51_ulps": rows[here]["ulps_from_the_nearest_double"],
            "item_50_ulps": abs(bits(there_value) - bits(float(exact[here]))),
        }
    return {
        "rows": rows,
        "eta_beta_ulps_from_the_nearest_double": eta_drift,
        "exponents_wrong_beyond_15_digits": wrong,
        "exponents_off_by_at_least_one_ulp": sorted(
            k for k, v in rows.items() if v["ulps_from_the_nearest_double"] > 0),
        "against_item_50": cross,
        "quantities_that_moved_between_the_two_bundles": sorted(
            k for k, v in cross.items() if not v["agree"]),
    }


def check_artifacts(bundle: pathlib.Path) -> dict:
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    # Two shapes so far, enumerated rather than guessed: item 50 keys a dict by
    # filename, item 51 ships a list of records. A reader that knows one returns
    # ZERO for the other and reports a clean bundle -- which is precisely what
    # happened here, and only the "verified < 5" guard surfaced it. Anything
    # neither shape refuses instead of contributing nothing (RUN-028).
    if "artifact_sha256_before_manifest" in validation:
        listed = dict(validation["artifact_sha256_before_manifest"])
        shape = "dict keyed by filename (item 50)"
    elif isinstance(validation.get("files"), list):
        listed = {rec["file"]: rec for rec in validation["files"]}
        shape = "list of file records (item 51)"
    else:
        listed, shape = {}, "UNRECOGNISED"
    present = {p.name for p in bundle.iterdir() if p.is_file()}
    verified, mismatched, absent = 0, [], []
    for name, rec in sorted(listed.items()):
        path = bundle / name
        if not path.exists():
            absent.append(name)
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() == rec["sha256"] and len(raw) == rec["bytes"]:
            verified += 1
        else:
            mismatched.append(name)
    uncovered = sorted(present - set(listed))
    report = (bundle / CHECKER_REPORT).read_bytes()
    stdout = (bundle / CHECKER_STDOUT).read_bytes()
    upstream = validation.get("input_state_sha256", {})
    return {
        "validation_record_shape": shape,
        "files_in_the_bundle": len(present),
        "files_listed": len(listed),
        "verified": verified, "mismatched": mismatched, "listed_but_absent": absent,
        "present_but_not_covered": uncovered,
        "the_only_uncovered_file_is_the_record_itself": uncovered == [VALIDATION],
        "checker_report_and_stdout_are_byte_identical":
            hashlib.sha256(report).hexdigest() == hashlib.sha256(stdout).hexdigest(),
        "declared_input_state": upstream,
        "checker_gate_reported": {k: v for k, v in validation.items()
                                  if "checker" in k or "gate" in k},
    }


def check_their_claims(report: dict, results: dict) -> dict:
    """Each claim the shipped checker says it verified, against a check of mine."""
    st, ec, sep = results["orbit_structure"], results["exact_codes"], results["separation"]
    mapping = {
        "exact accelerated code has a unique realizing source class modulo 2^(Q+1)":
            ec["source_class_violations"] == 0
            and ec["class_members_failing_to_realize_the_code"] == 0,
        "repeated exact code gives source gap multiple 2^(Q+1)":
            sep["source_gap_not_a_multiple_of_2^(Q+1)"] == 0,
        "repeated exact code gives endpoint gap multiple 2*3^k":
            sep["endpoint_gap_not_2*3^k*m"] == 0,
        "next-strictly-smaller first-crossing intervals are laminar":
            st["laminarity_violations"] == 0,
        "renewal identity A_i + D_i = D_{i+1} + E_i":
            st["renewal_identity_errors"] == 0,
        "plateau determinant Pi_i = g_i D_{i+1} + L_{i+1} A_i is a positive integer":
            st["plateau_determinant_not_a_positive_integer"] == 0,
        "strict-drop determinant Delta_i = g_i E_i + h_i A_i is a positive integer":
            st["drop_determinant_not_a_positive_integer"] == 0,
    }
    stated = list(report.get("verified_claims", []))
    checked = {c: mapping[c] for c in stated if c in mapping}
    not_checked = [c for c in stated if c not in mapping]
    return {
        "claims_the_checker_states": len(stated),
        "independently_confirmed": sum(1 for v in checked.values() if v),
        "independently_contradicted": sorted(k for k, v in checked.items() if not v),
        "not_covered_by_this_run": not_checked,
    }


# ---------------------------------------------------------------------------

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True, type=pathlib.Path)
    ap.add_argument("--limit", type=int, default=4001)
    ap.add_argument("--codes", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260828)
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    bundle = args.bundle
    constants = json.loads((bundle / CONSTANTS).read_text(encoding="utf-8"))
    shipped = json.loads((bundle / CHECKER_REPORT).read_text(encoding="utf-8"))
    paper = (bundle / PAPER).read_text(encoding="utf-8")

    rep: dict = {
        "round": "Hard-Zeta Phase II / Round A-U.2d.5",
        "source_item": 51,
        "odd_starts_below": args.limit,
        "exact_codes": check_exact_codes(args.codes, args.seed),
        "separation": check_bi_exact_separation(args.codes, args.seed),
        "shipped_examples": check_shipped_examples(shipped),
        "orbit_structure": check_orbit_structure(args.limit),
        # the residual the shipped checker reports for the identities this run
        # computes exactly. It lives in the CHECKER REPORT, not the validation
        # record -- reading it from the latter returned the string "PASS", which
        # is a gate verdict and not a residual at all.
        "shipped_max_float_residual":
            shipped.get("counts", {}).get("max_float_residual"),
        "constants": check_constants(constants),
        "artifacts": check_artifacts(bundle),
    }
    rep["their_claims"] = check_their_claims(shipped, rep)
    rep["scope_discipline"] = {
        "paper refuses a full contradiction":
            "no full contradiction" in paper or "still no full contradiction" in paper,
        "constants carry the same status":
            "no full contradiction" in constants.get("status", ""),
        "the forbidden operation is restated":
            "do not telescope rotation headroom" in
            constants.get("forbidden_operation", "").lower(),
    }

    ec, sep, se = rep["exact_codes"], rep["separation"], rep["shipped_examples"]
    st, cs, ar = rep["orbit_structure"], rep["constants"], rep["artifacts"]
    tc, sd = rep["their_claims"], rep["scope_discipline"]

    failures = []
    if ec["affine_identity_violations"]:
        failures.append("the affine identity 2^Q z = 3^k x + B_w fails")
    if ec["source_class_violations"] or ec["endpoint_class_violations"]:
        failures.append("an exact-code residue class is wrong")
    if ec["class_members_failing_to_realize_the_code"]:
        failures.append("a member of the claimed source class does not realize the "
                        "code, so the class is not the right one")
    if ec["class_members_checked_in_reverse"] < ec["trials"]:
        failures.append("the class check was not exercised in both directions")
    if sep["repeated_code_pairs"] < 20:
        failures.append("too few repeated-code pairs to have tested separation")
    if (sep["source_gap_not_a_multiple_of_2^(Q+1)"]
            or sep["endpoint_gap_not_2*3^k*m"] or sep["endpoint_gap_below_2*3^k"]):
        failures.append("bi-exact separation fails")
    if se["disagreeing"]:
        failures.append("a shipped example does not recompute: %s" % se["disagreeing"])
    if se["examples_checked"] < 3:
        failures.append("too few shipped examples were checked")
    if st["q_next_not_one"] or st["source_not_3_mod_4"]:
        failures.append("section 6 fails: a source with L >= 2 is not 3 mod 4")
    if st["L_at_least_2"] < 1000:
        failures.append("too few L >= 2 sources to have tested section 6")
    if st["laminarity_violations"] or st["renewal_identity_errors"]:
        failures.append("laminarity or the renewal identity fails")
    if st["nested_pairs"] == 0 or st["disjoint_pairs"] == 0:
        failures.append("laminarity was not exercised in both branches")
    if (st["plateau_determinant_not_a_positive_integer"]
            or st["drop_determinant_not_a_positive_integer"]):
        failures.append("a determinant is not a positive integer")
    if st["plateau_edges"] == 0 or st["drop_edges"] == 0:
        failures.append("the plateau / strict-drop dichotomy was not exercised")
    if st["depth_cap_violations"] or st["source_gap_below_4"]:
        failures.append("section 6's chain cap or 4-gap fails on its own premise")
    if st["chains_with_increasing_sources"] < 50:
        failures.append("section 6's premise was never evaluated: too few chains "
                        "with distinct increasing sources")
    if cs["exponents_wrong_beyond_15_digits"]:
        failures.append("a published constant is wrong beyond float precision")
    if ar["validation_record_shape"] == "UNRECOGNISED":
        failures.append("the validation record is in a shape this run does not "
                        "know, so it was not read at all")
    if ar["mismatched"] or ar["listed_but_absent"] or ar["verified"] < 5:
        failures.append("the bundle's validation record does not match its files")
    if tc["independently_contradicted"]:
        failures.append("a claim the checker states is contradicted here: %s"
                        % tc["independently_contradicted"])
    if tc["independently_confirmed"] < 6:
        failures.append("too few of the checker's claims were independently checked")
    if not all(sd.values()):
        failures.append("the round's scope refusals are missing: %s"
                        % sorted(k for k, v in sd.items() if not v))

    findings = []
    residual = shipped.get("counts", {}).get("max_float_residual")
    if residual and st["renewal_identity_errors"] == 0:
        findings.append(
            "the renewal identity and both determinants are exact in beta-linear "
            "integers -- %d edges, %d errors -- while the shipped checker reports "
            "`max_float_residual = %s` for the same identities. Fourth round in "
            "this line where an exactly rational or exactly integral quantity was "
            "evaluated in floating point (RUN-027, RUN-029, RUN-032, here)."
            % (st["renewal_edges"], st["renewal_identity_errors"], residual))
    if ar["checker_report_and_stdout_are_byte_identical"]:
        findings.append(
            "`checker_stdout.txt` is byte-identical to the checker report again -- "
            "second bundle running (item 50, item 51). Two names, one file, and "
            "the validation record lists both with the same hash.")
    if st["chains_with_increasing_sources"] and not st["chains_inside_the_source_corridor"]:
        findings.append(
            "section 6 puts an unconditional corollary and a conditional cap in "
            "one section, and only the first is testable. `y = 3 (mod 4)` holds on "
            "%d real sources with L >= 2, with 0 violations. The depth cap "
            "`r < 1 + U_beta(L)/4` is derived from the source corridor "
            "`y_r - y_1 < U_beta(L)`, which is a B-survival property: **0 of %d** "
            "real chains with distinct increasing sources satisfy it, so the cap "
            "is vacuous on orbits that exist. Same shape as the surviving "
            "crossings RUN-023 measured 0 of."
            % (st["L_at_least_2"], st["chains_with_increasing_sources"]))
    if cs["quantities_that_moved_between_the_two_bundles"]:
        findings.append(
            "constants shared with item 50 changed value between the bundles: %s. "
            "They are exact rationals, so the two cannot both be the nearest "
            "double; item 50's drift was measured at RUN-032."
            % ", ".join(cs["quantities_that_moved_between_the_two_bundles"]))

    rep["findings"] = findings
    rep["failures"] = failures
    rep["passed"] = not failures

    text = json.dumps(rep, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
