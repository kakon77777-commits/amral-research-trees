#!/usr/bin/env python3
"""Recheck of Hard-Zeta Phase II Round A-U.2d.4 (source item 50).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Renewal Congestion Rigidity: Laminar First-Crossing
Forests, Annular Farey Structure, and a Quantitative Congestion Envelope* (v0.1,
2026-08-13). Ships a checker, its report, a constants JSON, a source-validation
record and a stdout transcript.

## The first round in this line whose core needs no hypothetical object

Every A-U.2d round so far has had the same shape: a theorem about *surviving*
crossings, of which RUN-023 measured zero below 2e5. The conditional half was
always the interesting half, and it was never testable.

This round's core is different. Theorem 3.1 says

    e(s) = min{u > s : delta_u < delta_s}

and that is not a theorem about CASP candidates -- it is an identity about the
scalar sequence `delta_m = beta*m - K_m`, true of any orbit. Laminarity follows
from it for the same reason next-smaller-element intervals are laminar in any
sequence. The annulus identity and the determinant identity are algebra in the
slack values. **All of it applies to orbits this sweep can exhibit**, and all of
it is checkable in exact integers.

## Exactly, because these are beta-linear forms

`delta_u < delta_s` is `K_u - K_s > beta(u-s)`, i.e. `2^(K_u-K_s) > 3^(u-s)` --
integers. Every quantity the round defines (`A_i`, `D_i`, `E_i`) is `a*beta + b`
for integers `a, b`, so the annulus identity is exactly `(0, 0)` in that pair,
not a small residual. The shipped checker computes all of it in `float` and
reports a maximum identity error of `2.3e-14`; this file computes it in integers
and reports the error there.

That is not a defect in their result -- it is the RUN-027 situation again, where
the artifact reached for high precision to evaluate something that was exact.
What it does mean is that their next-smaller comparison is a float comparison of
quantities that can be arbitrarily close, so this run **measures the margin** by
which that comparison avoided being wrong.

## Artifacts

Standing rule since item 35: recompute independently, never re-run the shipped
script, and check whether the shipped records are what they claim. This bundle
ships a `SOURCE_VALIDATION` manifest whose `input_state_sha256` names the two
items RUN-030 and RUN-031 examined -- so the provenance chain can be closed
against this tree's own records.

Usage:
  python code/src50_congestion_rigidity.py --bundle DIR [--starts N,N,...]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from fractions import Fraction

import mpmath as mp

WORKING_DPS = 120

PAPER = "Hard_Zeta_Phase_II_Round_AU2d4_Renewal_Congestion_Rigidity_v0.1.md"
CONSTANTS = "Hard_Zeta_AU2d4_congestion_rigidity_constants.json"
CHECKER_REPORT = "Hard_Zeta_AU2d4_checker_report.json"
CHECKER_STDOUT = "checker_stdout.txt"
VALIDATION = "SOURCE_VALIDATION_AU2d4.json"

DEFAULT_STARTS = (27, 703, 6171, 837799)

#: what RUN-030 and RUN-031 recorded for the two upstream items, so the bundle's
#: declared input state can be closed against this tree rather than trusted
UPSTREAM = {
    "handoff_zip": "799fad5e0614c598157b4748e0b1033585f11194d80824051ac12e3a5730acdd",
    "collatz_ot_series_zip":
        "d7394cce7b6a877112446d5d4616339bf2b2eda4241f3d6a9010128c288f0d2d",
}


# ---------------------------------------------------------------------------
# the orbit, and slack comparison without a single floating-point operation
# ---------------------------------------------------------------------------

def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def accelerated_word(start: int, max_steps: int = 4000) -> list[int]:
    """The accelerated odd-to-odd valuation word, as integers."""
    y, word = start, []
    while y != 1 and len(word) < max_steps:
        t = 3 * y + 1
        k = v2(t)
        word.append(k)
        y = t >> k
    return word


def cumulative(word: list[int]) -> list[int]:
    out, run = [0], 0
    for q in word:
        run += q
        out.append(run)
    return out


def slack_is_smaller(K: list[int], u: int, s: int) -> bool:
    """delta_u < delta_s, decided exactly by comparing 3^(u-s) with 2^(K_u-K_s).

    No logarithm, no float. This is the comparison the shipped checker performs
    on doubles.

    Both exponents may be negative, and the first version returned False whenever
    `K_u < K_s` instead of handling it -- which made every reversed query answer
    "no", so the Theorem 3.1 prefix check (which asks `delta_s < delta_u`) marked
    every prefix a violation. **A comparison that silently answers one direction
    is worse than one that raises**: it produced 2757 violations of a theorem that
    holds. Rationals handle the signs.
    """
    d = u - s
    dk = K[u] - K[s]
    return Fraction(3) ** d < Fraction(2) ** dk


def first_crossings(K: list[int], n: int) -> list[int | None]:
    return [next((u for u in range(s + 1, n + 1) if slack_is_smaller(K, u, s)), None)
            for s in range(n + 1)]


def next_smaller_by_stack(K: list[int], n: int) -> list[int | None]:
    """The same thing by a monotone stack, which is a different algorithm.

    Two routes to one answer: a quadratic scan that asks the defining question at
    every pair, and a linear stack that assumes transitivity of the slack order.
    They must agree, and if they ever did not, the assumption would be the thing
    that broke.
    """
    out: list[int | None] = [None] * (n + 1)
    stack: list[int] = []
    for u in range(n + 1):
        while stack and slack_is_smaller(K, u, stack[-1]):
            out[stack.pop()] = u
        stack.append(u)
    return out


# ---------------------------------------------------------------------------
# beta-linear arithmetic: a quantity is (coefficient of beta, integer part)
# ---------------------------------------------------------------------------

def lin_sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] - b[0], a[1] - b[1])


def lin_add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def delta(K: list[int], m: int) -> tuple[int, int]:
    """delta_m = beta*m - K_m."""
    return (m, -K[m])


def lin_value(a: tuple[int, int], beta) -> object:
    return a[0] * beta + a[1]


# ---------------------------------------------------------------------------

def check_structure(starts: tuple[int, ...]) -> dict:
    """Theorem 3.1, laminarity, the annulus identity and the determinant -- exactly."""
    rows = []
    totals = {
        "orbits": 0, "intervals": 0,
        "next_smaller_disagreements": 0,
        "two_routes_disagreements": 0,
        "prefix_violations": 0,
        "laminarity_violations": 0,
        "nested_pairs": 0, "disjoint_pairs": 0,
        "annulus_edges": 0, "annulus_identity_errors": 0,
        "plateau_edges": 0, "strict_drop_edges": 0,
        "determinant_form_disagreements": 0,
        "determinants_below_one": 0,
    }
    for start in starts:
        word = accelerated_word(start)
        K = cumulative(word)
        n = len(word)
        e_scan = first_crossings(K, n)
        e_stack = next_smaller_by_stack(K, n)
        if e_scan != e_stack:
            totals["two_routes_disagreements"] += sum(
                1 for a, b in zip(e_scan, e_stack) if a != b)

        # Theorem 3.1: every proper prefix must have a STRICTLY larger slack
        prefix_bad = 0
        for s, e in enumerate(e_scan):
            if e is None:
                continue
            for u in range(s + 1, e):
                if slack_is_smaller(K, u, s) or not slack_is_smaller(K, s, u):
                    prefix_bad += 1
        totals["prefix_violations"] += prefix_bad

        intervals = [(s, e) for s, e in enumerate(e_scan) if e is not None]
        nested = disjoint = crossing = 0
        for i in range(len(intervals)):
            a, b = intervals[i]
            for j in range(i + 1, len(intervals)):
                c, d = intervals[j]
                if b <= c or d <= a:
                    disjoint += 1
                elif (a <= c and d <= b) or (c <= a and b <= d):
                    nested += 1
                else:
                    crossing += 1
        totals["nested_pairs"] += nested
        totals["disjoint_pairs"] += disjoint
        totals["laminarity_violations"] += crossing

        # consecutive nested origins: s_i < s_{i+1} < e_i with e_{i+1} <= e_i
        plateau = strict = ident_bad = det_bad = det_small = edges = 0
        for s_i, e_i in intervals:
            s_j = s_i + 1
            if s_j >= e_i or e_scan[s_j] is None:
                continue
            e_j = e_scan[s_j]
            if e_j > e_i:                                # not a nested edge
                continue
            edges += 1
            g_i, p_i = s_j - s_i, K[s_j] - K[s_i]
            h_i, r_i = e_i - e_j, K[e_i] - K[e_j]
            A = (g_i, -p_i)
            D_i = lin_sub(delta(K, s_i), delta(K, e_i))
            D_j = lin_sub(delta(K, s_j), delta(K, e_j))
            E = (-h_i, r_i)
            residual = lin_sub(lin_add(A, D_i), lin_add(D_j, E))
            if residual != (0, 0):
                ident_bad += 1
            if h_i == 0:
                plateau += 1
            else:
                strict += 1
                det = r_i * g_i - p_i * h_i
                combo = lin_add((g_i * E[0], g_i * E[1]), (h_i * A[0], h_i * A[1]))
                if combo != (0, det):
                    det_bad += 1
                if det < 1:
                    det_small += 1
        totals["annulus_edges"] += edges
        totals["annulus_identity_errors"] += ident_bad
        totals["plateau_edges"] += plateau
        totals["strict_drop_edges"] += strict
        totals["determinant_form_disagreements"] += det_bad
        totals["determinants_below_one"] += det_small
        totals["orbits"] += 1
        totals["intervals"] += len(intervals)

        depth, at, chain = 0, None, []
        for t in range(n + 1):
            live = [(a, b) for a, b in intervals if a <= t < b]
            if len(live) > depth:
                depth, at, chain = len(live), t, sorted(live)

        # The shipped report's `chain_*_edges` count the edges of THAT chain, not
        # every nested edge in the orbit: 13 + 3 = 16 = 17 - 1 for start 27. A
        # first version reported the orbit-wide counts under their field names
        # and called the disagreement theirs. Two different quantities wearing
        # one label is not a discrepancy, it is a mislabelling.
        chain_plateau = chain_strict = 0
        for (a1, b1), (a2, b2) in zip(chain, chain[1:]):
            if b1 == b2:
                chain_plateau += 1
            else:
                chain_strict += 1
        totals["chain_edges"] = totals.get("chain_edges", 0) + len(chain) - 1

        rows.append({"start": start, "accelerated_steps_to_1": n,
                     "intervals": len(intervals),
                     "max_completed_active_depth": depth, "depth_time": at,
                     "chain_plateau_edges": chain_plateau,
                     "chain_strict_drop_edges": chain_strict,
                     "orbit_wide_plateau_edges": plateau,
                     "orbit_wide_strict_drop_edges": strict})

    totals["rows"] = rows
    totals["exact_annulus_identity_error"] = 0 if not totals["annulus_identity_errors"] else None
    return totals


def check_float_margin(starts: tuple[int, ...]) -> dict:
    """How close did the shipped checker's float comparison come to being wrong?

    Their `next_strictly_smaller` compares doubles. The quantities compared are
    beta-linear forms and can be arbitrarily close. So: find the smallest gap
    the comparison actually had to resolve, and put it beside the spacing of a
    double at that magnitude. A margin is only reassuring once it is a number.
    """
    with mp.workdps(WORKING_DPS):
        beta = mp.log(3, 2)
        smallest = None
        where = None
        checked = 0
        for start in starts:
            K = cumulative(accelerated_word(start))
            n = len(K) - 1
            e = first_crossings(K, n)
            for s, end in enumerate(e):
                if end is None:
                    continue
                for u in range(s + 1, end + 1):
                    gap = abs(lin_value(lin_sub(delta(K, u), delta(K, s)), beta))
                    checked += 1
                    if smallest is None or gap < smallest:
                        smallest, where = gap, (start, s, u)
        biggest = max(abs(lin_value(delta(K, m), beta)) for m in range(len(K)))
        spacing = mp.mpf(2) ** -52 * max(biggest, mp.mpf(1))
        margin = smallest / spacing
    return {
        "comparisons_the_scan_had_to_decide": checked,
        "smallest_exact_gap": mp.nstr(smallest, 8),
        "at_start_s_u": list(where) if where else None,
        "double_spacing_at_that_magnitude": mp.nstr(spacing, 8),
        "margin_in_units_of_that_spacing": mp.nstr(margin, 8),
        "margin_in_orders_of_magnitude": round(float(mp.log(margin, 10)), 1),
        "the_float_comparison_had_room": bool(margin > 1000),
    }


#: how many times the bracket may fail before the run refuses. The exact
#: power of three is a correct answer and a quadratic one; using it for every
#: m is not a fallback, it is a ten-minute outage wearing a safety net.
FALLBACK_BUDGET = 64

#: the partial quotients of log_2 3 certified by integer comparison at RUN-029
BETA_CF = (1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1)


def beta_bracket() -> tuple[tuple[int, int], tuple[int, int]]:
    """Two consecutive convergents of log_2 3, which bracket it."""
    p_prev, p_cur, q_prev, q_cur = 0, 1, 1, 0
    conv = []
    for a in BETA_CF:
        p_prev, p_cur = p_cur, a * p_cur + p_prev
        q_prev, q_cur = q_cur, a * q_cur + q_prev
        conv.append((p_cur, q_cur))
    (p1, q1), (p2, q2) = conv[-2], conv[-1]
    return ((p1, q1), (p2, q2)) if p1 * q2 < p2 * q1 else ((p2, q2), (p1, q1))


def beta_floors(N: int) -> tuple[list[int], int]:
    """floor(m * log_2 3) for m = 0..N, exactly, and how often the fallback ran.

    Multiplying `p3 *= 3` up to `3^100000` is quadratic in the digits and took
    about ten minutes -- long enough to time the drill out. Two convergents
    bracket beta, so `floor(m*lo)` and `floor(m*hi)` pin the answer whenever they
    agree, which is integer arithmetic on numbers the size of `q`. When they do
    not agree the exact power decides it, and the number of times that happened
    is reported rather than assumed to be zero.
    """
    (p_lo, q_lo), (p_hi, q_hi) = beta_bracket()
    floors, fallbacks = [0], 0
    for m in range(1, N + 1):
        a = (m * p_lo) // q_lo
        b = (m * p_hi) // q_hi
        if a == b:
            floors.append(a)
        else:
            fallbacks += 1
            if fallbacks > FALLBACK_BUDGET:              # pragma: no cover
                return floors, fallbacks
            floors.append((3 ** m).bit_length() - 1)
    return floors, fallbacks


def check_mechanical(sizes: tuple[int, ...] = (100, 1000, 10000, 100000)) -> dict:
    """The mechanical word a_m = floor(beta m) - floor(beta (m-1))."""
    rows = []
    total_fallbacks = 0
    biggest = max(sizes)
    all_floors, total_fallbacks = beta_floors(biggest)
    if len(all_floors) <= biggest:
        # The budget stopped the fallback part-way. Returning a short list would
        # make the caller index off the end, and a check that dies is a check
        # that reports nothing -- so it comes back as an empty result the gate
        # can refuse, rather than as a traceback.
        return {"rows": [], "largest_N": biggest,
                "times_the_bracket_could_not_decide_and_the_exact_power_ran":
                    total_fallbacks,
                "the_floor_table_is_incomplete": True}
    for N in sizes:
        floors = all_floors[:N + 1]
        word = [floors[m] - floors[m - 1] for m in range(1, N + 1)]
        K = cumulative(word)
        e = next_smaller_by_stack(K, N)
        intervals = [(s, u) for s, u in enumerate(e) if u is not None]
        # A sweep, not a scan. Asking "which intervals are live at t" for every t
        # is quadratic, and at N = 100000 that was ten minutes -- long enough to
        # time the drill out and leave a planted defect on disk.
        depth, at, running = 0, None, 0
        # An interval (a, b) is live for a <= t < b, so at a position where one
        # ends and another begins the END is processed first. Sorting the other
        # way counted both and put every depth one too high -- caught only
        # because the shipped report says 6 and the sweep said 7.
        events = sorted([(a, 1) for a, _ in intervals] + [(b, -1) for _, b in intervals],
                        key=lambda ev: (ev[0], ev[1]))
        for pos, delta_ in events:
            running += delta_
            if running > depth:
                depth, at = running, pos
        chain = sorted(a for a, b in intervals if a <= at < b) if at is not None else []
        rows.append({"N": N, "alphabet": sorted(set(word)),
                     "max_completed_active_depth": depth, "depth_time": at,
                     "active_chain_first_start": chain[0] if chain else None,
                     "active_chain_last_start": chain[-1] if chain else None})
    return {"rows": rows,
            "largest_N": biggest,
            "times_the_bracket_could_not_decide_and_the_exact_power_ran":
                total_fallbacks}


def check_exponents(constants: dict) -> dict:
    """Every published exponent is an exact rational; measure the ulp drift."""
    import struct

    rho = Fraction("4.1164")
    exact = {
        "theta_star": 1 / (rho + 1),
        "sigma_star": 1 / (1 + 1 / (rho + 1)),
        "dense_overlap_lower_exponent": 1 - 1 / (1 + 1 / (rho + 1)),
        "chain_outer_length_power": 1 + 1 / rho,
        "chain_outer_log_denominator_power": 1 / rho,
        "congestion_upper_power": rho / (rho + 1),
        "congestion_upper_log_power": 1 / (rho + 1),
    }
    published = dict(constants["prior_inputs"])
    published.update(constants["new_derived_exponents"])

    def bits(x: float) -> int:
        return struct.unpack("<q", struct.pack("<d", x))[0]

    rows, missing, wrong = {}, [], []
    for name, value in exact.items():
        if name not in published:
            missing.append(name)
            continue
        shown = published[name]
        nearest = float(value)
        drift = abs(bits(shown) - bits(nearest))
        rel = float(abs(Fraction(shown) - value) / value)
        rows[name] = {"exact": "%d/%d" % (value.numerator, value.denominator),
                      "published": shown, "nearest_double": nearest,
                      "ulps_from_the_nearest_double": drift,
                      "relative_error": "%.2e" % rel,
                      "correct_to_15_significant_digits": rel < 1e-15}
        if rel >= 1e-15:
            wrong.append(name)

    # the round's own two self-consistency identities, exactly
    identities = {
        "theta_star + congestion_upper_power == 1":
            exact["theta_star"] + exact["congestion_upper_power"] == 1,
        "chain_outer_length_power * congestion_upper_power == 1":
            exact["chain_outer_length_power"] * exact["congestion_upper_power"] == 1,
    }
    return {
        "rows": rows, "exponents_not_published": missing,
        "exponents_wrong_beyond_15_digits": wrong,
        "exponents_off_by_at_least_one_ulp": sorted(
            k for k, v in rows.items() if v["ulps_from_the_nearest_double"] > 0),
        "largest_ulp_drift": max((v["ulps_from_the_nearest_double"]
                                  for v in rows.values()), default=0),
        "exact_identities": identities,
        "all_identities_hold_exactly": all(identities.values()),
    }


def check_artifacts(bundle: pathlib.Path) -> dict:
    """The bundle's own validation record, verified and measured for coverage."""
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    listed = validation["artifact_sha256_before_manifest"]
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

    upstream = {}
    for key, want in UPSTREAM.items():
        got = validation["input_state_sha256"].get(key)
        upstream[key] = {"declared_by_the_bundle": got,
                         "recorded_by_this_tree": want,
                         "agrees": got == want}

    report = (bundle / CHECKER_REPORT).read_bytes()
    stdout = (bundle / CHECKER_STDOUT).read_bytes()

    md = {}
    for name, rec in sorted(validation["markdown_checks"].items()):
        raw = (bundle / name).read_bytes()
        text = raw.decode("utf-8")
        md[name] = {
            "bytes_agree": len(raw) == rec["bytes"],
            "dollar_count_agrees": text.count("$") == rec["dollar_count"],
            "dollar_count": text.count("$"),
            "no_backslash_paren": ("\\(" in text) == rec["contains_backslash_paren_delimiters"],
            "no_backslash_bracket": ("\\[" in text) == rec["contains_backslash_bracket_delimiters"],
        }

    return {
        "files_in_the_bundle": len(present),
        "files_listed_by_the_validation_record": len(listed),
        "verified": verified, "mismatched": mismatched, "listed_but_absent": absent,
        "present_but_not_covered": uncovered,
        "the_only_uncovered_file_is_the_record_itself": uncovered == [VALIDATION],
        "upstream_state": upstream,
        "upstream_agrees_with_this_trees_records": all(v["agrees"] for v in upstream.values()),
        "checker_report_and_stdout_are_byte_identical":
            hashlib.sha256(report).hexdigest() == hashlib.sha256(stdout).hexdigest(),
        "markdown_checks": md,
        "markdown_checks_all_agree": all(all(v.values()) for v in md.values()),
        "checker_gate_reported": validation["checker_gate"],
    }


def check_scope_discipline(paper: str, constants: dict) -> dict:
    """The round's own refusals, which are as much a claim as its theorems."""
    checks = {
        "the paper's status line refuses Collatz / CST / CASP":
            bool(re.search(r"\*\*not\*\* a proof of Collatz, Terras CST, CASP", paper)),
        "the abstract says Highly Nested is not eliminated":
            "is **not eliminated**" in paper,
        "the headroom non-telescoping no-go is restated":
            "Headroom Non-Telescoping No-Go remains intact" in paper,
        "the constants JSON carries the same refusal":
            "no Collatz/CASP proof claim" in constants.get("status", ""),
        "the rotation-headroom telescope is still forbidden":
            constants["prior_inputs"].get("rotation_headroom_telescope_allowed") is False,
    }
    return {"checks": checks, "missing": sorted(k for k, v in checks.items() if not v),
            "ok": all(checks.values())}


# ---------------------------------------------------------------------------

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True, type=pathlib.Path)
    ap.add_argument("--starts", default=",".join(str(s) for s in DEFAULT_STARTS))
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    starts = tuple(int(x) for x in args.starts.split(",") if x.strip())
    bundle = args.bundle
    constants = json.loads((bundle / CONSTANTS).read_text(encoding="utf-8"))
    shipped = json.loads((bundle / CHECKER_REPORT).read_text(encoding="utf-8"))
    paper = (bundle / PAPER).read_text(encoding="utf-8")

    exact_prefix = [(3 ** m).bit_length() - 1 for m in range(0, 400)]
    fast_prefix, _ = beta_floors(399)
    rep = {
        "round": "Hard-Zeta Phase II / Round A-U.2d.4",
        "beta_floor_route_agrees_with_exact_powers_on_0_to_399":
            exact_prefix == fast_prefix,
        "source_item": 50,
        "starts": list(starts),
        "structure": check_structure(starts),
        "float_margin": check_float_margin(starts),
        "mechanical": check_mechanical(),
        "exponents": check_exponents(constants),
        "artifacts": check_artifacts(bundle),
        "scope_discipline": check_scope_discipline(paper, constants),
    }

    # every figure the shipped report states about these orbits, recomputed
    theirs = {r["start"]: r for r in shipped["accelerated_collatz_smoke_tests"]}
    mine = {r["start"]: r for r in rep["structure"]["rows"]}
    agree, differ = [], []
    for start in sorted(set(theirs) & set(mine)):
        fields = ("accelerated_steps_to_1", "max_completed_active_depth", "depth_time",
                  "chain_plateau_edges", "chain_strict_drop_edges")
        bad = {f: (theirs[start].get(f), mine[start].get(f))
               for f in fields if theirs[start].get(f) != mine[start].get(f)}
        (differ if bad else agree).append({"start": start, "fields": bad} if bad else start)
    rep["shipped_smoke_tests"] = {
        "starts_compared": len(set(theirs) & set(mine)),
        "agreeing": agree, "disagreeing": differ,
        "fields_per_start": 5,
    }

    theirs_mech = {r["N"]: r for r in shipped["mechanical_code_smoke_tests"]}
    mine_mech = {r["N"]: r for r in rep["mechanical"]["rows"]}
    mdiff = []
    for N in sorted(set(theirs_mech) & set(mine_mech)):
        fields = ("max_completed_active_depth", "depth_time",
                  "active_chain_first_start", "active_chain_last_start", "alphabet")
        bad = {f: (theirs_mech[N].get(f), mine_mech[N].get(f))
               for f in fields if theirs_mech[N].get(f) != mine_mech[N].get(f)}
        if bad:
            mdiff.append({"N": N, "fields": bad})
    rep["shipped_mechanical_tests"] = {
        "sizes_compared": len(set(theirs_mech) & set(mine_mech)),
        "disagreeing": mdiff,
    }

    st, fm, ex = rep["structure"], rep["float_margin"], rep["exponents"]
    ar, sd = rep["artifacts"], rep["scope_discipline"]

    failures = []
    if st["two_routes_disagreements"]:
        failures.append("the quadratic scan and the monotone stack disagree on the "
                        "next-smaller slack")
    if st["prefix_violations"]:
        failures.append("a proper prefix of a first-crossing interval does not have "
                        "a strictly larger slack, contradicting Theorem 3.1")
    if st["laminarity_violations"]:
        failures.append("two first-crossing intervals properly cross, contradicting "
                        "Theorem 4.1")
    if st["nested_pairs"] == 0 or st["disjoint_pairs"] == 0:
        failures.append("laminarity was not exercised: the sample contains no "
                        "nested pair or no disjoint pair")
    if st["annulus_identity_errors"]:
        failures.append("the annulus identity does not hold exactly")
    if st["annulus_edges"] < 10:
        failures.append("too few nested edges to have tested the annulus identity")
    if st["plateau_edges"] == 0 or st["strict_drop_edges"] == 0:
        failures.append("the plateau / strict-drop dichotomy was not exercised in "
                        "both branches")
    if st["determinant_form_disagreements"] or st["determinants_below_one"]:
        failures.append("the strict-drop determinant identity or its lower bound fails")
    if fm["comparisons_the_scan_had_to_decide"] < 5 * st["intervals"]:
        failures.append("the float-margin measurement decided almost nothing: %d "
                        "comparisons for %d intervals, so it looked at the first "
                        "step of each rather than the whole interval"
                        % (fm["comparisons_the_scan_had_to_decide"], st["intervals"]))
    if ex["exponents_wrong_beyond_15_digits"]:
        failures.append("a published exponent is wrong beyond float precision: %s"
                        % ex["exponents_wrong_beyond_15_digits"])
    if ex["exponents_not_published"] or not ex["all_identities_hold_exactly"]:
        failures.append("the exponent chain does not satisfy its own identities")
    if ar["mismatched"] or ar["listed_but_absent"]:
        failures.append("the bundle's own validation record does not match its files")
    if ar["verified"] < 5:
        failures.append("almost nothing in the validation record was verified")
    if not ar["markdown_checks_all_agree"]:
        failures.append("a markdown check in the validation record does not reproduce")
    if not ar["upstream_agrees_with_this_trees_records"]:
        failures.append("the declared input state disagrees with this tree's records")
    if rep["shipped_smoke_tests"]["disagreeing"]:
        failures.append("the shipped checker's orbit figures do not reproduce: %s"
                        % rep["shipped_smoke_tests"]["disagreeing"])
    if rep["shipped_smoke_tests"]["starts_compared"] < 3:
        failures.append("too few shipped smoke tests were compared")
    if rep["shipped_mechanical_tests"]["disagreeing"]:
        failures.append("the shipped checker's mechanical figures do not reproduce: %s"
                        % rep["shipped_mechanical_tests"]["disagreeing"])
    if not sd["ok"]:
        failures.append("the round's own scope refusals are missing: %s" % sd["missing"])
    if rep["mechanical"]["times_the_bracket_could_not_decide_and_the_exact_power_ran"]:
        failures.append("the floor bracket could not decide %d times, so the fast "
                        "path is not the exact one it is standing in for"
                        % rep["mechanical"]["times_the_bracket_could_not_decide_and_the_exact_power_ran"])
    if not rep["beta_floor_route_agrees_with_exact_powers_on_0_to_399"]:
        failures.append("the bracketed floor route disagrees with exact powers of "
                        "three, so the fast path is not the exact one")

    findings = []
    reported_err = ar["checker_gate_reported"].get("max_annulus_identity_error")
    if st["annulus_identity_errors"] == 0 and reported_err:
        findings.append(
            "the annulus identity `A_i + D_i = D_{i+1} + E_i` is exact in integers "
            "— every quantity in it is `a·β + b` for integers a, b, so the residual "
            "is the pair `(0, 0)` and not a small number. Recomputed that way over "
            "%d nested edges the error is **0**; the shipped validation record "
            "reports `max_annulus_identity_error = %s` because the checker "
            "evaluates it in `float`. Third time in this line that an exactly "
            "rational or exactly integral quantity was reached for with floating "
            "point (RUN-027, RUN-029, here)."
            % (st["annulus_edges"], reported_err))
    if ex["exponents_off_by_at_least_one_ulp"]:
        findings.append(
            "%d of the %d published exponents differ from the nearest double of "
            "their exact rational by 1 to %d ulps — they are chained float "
            "arithmetic where an exact rational was available. Every one is right "
            "to 15 significant digits and nothing in the round turns on it, so "
            "this is a note rather than a defect."
            % (len(ex["exponents_off_by_at_least_one_ulp"]), len(ex["rows"]),
               ex["largest_ulp_drift"]))
    if ar["checker_report_and_stdout_are_byte_identical"]:
        findings.append(
            "`checker_stdout.txt` is byte-identical to `Hard_Zeta_AU2d4_checker_"
            "report.json`. The README describes them as different artifacts — "
            "\"deterministic checker output\" and \"human-readable checker run "
            "output\" — and the bundle's own validation record lists both, with "
            "the same hash. Two names, one file.")

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
