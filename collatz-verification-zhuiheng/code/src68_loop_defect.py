"""RUN-049 — independent recheck of Hard-Zeta round A-U.2d.21.

`Faithful Return-Loop / Boundary-Layer Coupling Rigidity` (source item 68).
數學戰士「墜衡」.

A-U.2d.20 extracted a linear mass of return cycles carrying three valuation
sheets. This round removes the ambiguity by deleting at the true unique-label
threshold `q >= s_k` and paying for it out of the SURPLUS `sum(q-1)` rather
than the full valuation sum, which leaves `(2-beta-o(1))h` of fully faithful
cycle mass. It then shows the coupling that was hoped for cannot work: the
endpoint modulo `3^K` depends only on the final `K` valuations, so a
polynomial modulus screens everything a linear distance inside the bridge.

The round's new object is the **loop defect**

    d_M(C; r) := (B_C - (2^{Q_C} - 3^{L_C}) r) / M,

an integer by the cycle certificate, with the exact semigroup law
`d(CD) = 3^{L_D} d(C) + 2^{Q_C} d(D)` and a quotient-layer lift
`2^{Q_C} n' = 3^{L_C} n + d_M(C;r)` that holds only for a CONTIGUOUS orbit
realization -- the bundle's own NO-GO 12.1.

Three things this gate does that the shipped checker does not.

First, the semigroup law is tested on **distinct pairs**. The bundle composes
each cycle with ITSELF (`compose_defect(r, w, w, M)`, twenty times, with the
comment "self-composition is enough to check algebra"). It is not: at `D = C`
the law reads `d(CC) = (3^{L} + 2^{Q}) d(C)`, which is symmetric in its two
coefficients, so the WRONG law with the coefficients swapped gives the same
answer. This gate plants that swapped law and shows self-composition accepts
it while a genuine `C != D` composition rejects it.

Second, NO-GO 12.1 is measured rather than asserted. The erasure is run with
contiguity tracking; the certificate is checked on every graph cycle,
contiguous or spliced, and the quotient-layer lift is checked on the
contiguous ones and MEASURED on the spliced ones, where it is not licensed.

Third, endpoint and source screening are checked on real orbit words as well
as synthetic ones, and for SHARPNESS: a change inside the horizon must be able
to move the residue, or the horizon claim bounds nothing.

Usage:
    python code/src68_loop_defect.py --bundle <dir> [--limit N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import re
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src54_low_source_saturation import widen                       # noqa: E402
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    b_of, beta_hi, beta_lo, verdict_with_budget,
)
from src65_lift_cocycle import (                                    # noqa: E402
    ceil_beta, lift_profile, local_bridges,
)
from src67_return_loops import forward_target, ord_two              # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d21_Faithful_Return_Loop_Boundary"
         "_Layer_Coupling_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d21_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d21_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d21_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d21.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.21_AU2d21.md"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def defect(word: tuple[int, ...], r: int, m: int) -> int | None:
    """`d_M(C;r) = (B_C - (2^Q - 3^L) r) / M`, or None if it is not integral.

    Integrality is the CONTENT of the cycle certificate, so it is returned
    rather than asserted -- a caller that gets None has found a violation.
    """
    q, ell = sum(word), len(word)
    num = b_of(word) - ((1 << q) - 3 ** ell) * r
    return num // m if num % m == 0 else None


def erase_cycles(states: list[int], word: tuple[int, ...], m: int,
                 cap: int = 200):
    """Chronological loop erasure, tracking CONTIGUITY.

    Returns `(residue, cycle_word, first_index, last_index, contiguous)`.
    A cycle is contiguous when the orbit positions it is built from are
    consecutive -- which is exactly when Theorem 10.2's quotient-layer lift is
    licensed. After a nested erasure they need not be, which is NO-GO 12.1.
    """
    out = []
    stack_v: list[int] = []      # residues
    stack_i: list[int] = []      # original orbit indices
    stack_e: list[int] = []      # labels between stack vertices
    pos: dict[int, int] = {}
    for idx, s in enumerate(states):
        v = s % m
        if idx == 0:
            stack_v, stack_i, pos = [v], [0], {v: 0}
            continue
        q = word[idx - 1]
        if v not in pos:
            stack_e.append(q)
            stack_v.append(v)
            stack_i.append(idx)
            pos[v] = len(stack_v) - 1
        else:
            p = pos[v]
            cyc = tuple(stack_e[p:] + [q])
            idxs = stack_i[p:] + [idx]
            contiguous = all(b == a + 1 for a, b in zip(idxs, idxs[1:]))
            out.append((stack_v[p], cyc, stack_i[p], idx, contiguous))
            for old in stack_v[p + 1:]:
                pos.pop(old, None)
            stack_v = stack_v[:p + 1]
            stack_i = stack_i[:p + 1]
            stack_e = stack_e[:p]
            if len(out) >= cap:
                break
    return out


def split_runs(word: tuple[int, ...], bad: list[bool]) -> list[tuple[int, int]]:
    h, runs, j = len(word), [], 0
    while j < h:
        while j < h and bad[j]:
            j += 1
        if j >= h:
            break
        a = j
        while j < h and not bad[j]:
            j += 1
        runs.append((a, j))
    return runs


def endpoint_mod(word: tuple[int, ...], k: int) -> int:
    """The endpoint representative of the whole word, reduced mod `3^k`."""
    m = 3 ** k
    return b_of(word) % m * pow(pow(2, sum(word), m), -1, m) % m


def endpoint_from_suffix(word: tuple[int, ...], k: int) -> int:
    """The k-term tower sum -- only the final `k` valuations enter."""
    m, total, run = 3 ** k, 0, 0
    for j in range(1, k + 1):
        run += word[len(word) - j]
        total = (total + 3 ** (j - 1) * pow(pow(2, run, m), -1, m)) % m
    return total


def source_rep(word: tuple[int, ...]) -> int:
    ell, q = len(word), sum(word)
    mod = 1 << (q + 1)
    r = ((1 << q) - b_of(word)) % mod * pow(pow(3, ell, mod), -1, mod) % mod
    return r or mod


def zero_lift(limit: int, max_steps: int):
    out = []
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        ms = lift_profile(w)
        if ms[len(w)] != 0:
            continue
        out.append((y, X, Z, list(vals[1:]), w, ms))
    return out


# ---------------------------------------------------------------------------
# instrument
# ---------------------------------------------------------------------------

def check_instrument() -> dict:
    out: dict = {"checks": 0, "failed": []}

    def want(name: str, ok: bool) -> None:
        out["checks"] += 1
        if not ok:
            out["failed"].append(name)

    b_lo, b_hi = beta_lo(), beta_hi()
    want("beta bracket has width", b_lo < b_hi)
    bad, flat = 0, 0
    for ell in (1, 2, 7, 41, 306, 1000):
        c = ceil_beta(ell)
        if not (c - 1 < ell * b_lo and ell * b_hi < c):
            bad += 1
        if c == (3 ** ell).bit_length() - 1:
            flat += 1
    want("ceil(beta l) brackets beta*l on both sides", bad == 0)
    want("ceil(beta l) is not the floor", flat == 0)

    bad, loose = 0, 0
    for k in range(1, 9):
        m, s = 3 ** k, ord_two(k)
        if pow(2, s, m) != 1:
            bad += 1
        if k >= 2 and (pow(2, s // 3, m) == 1 or pow(2, s // 2, m) == 1):
            loose += 1
    want("2^{2*3^{k-1}} = 1 mod 3^k", bad == 0)
    want("no maximal proper divisor of the order works", loose == 0)

    # the composition law for the affine correction, which is the whole
    # algebraic backbone of the defect semigroup
    bad = 0
    for c, d in (((1, 2), (2, 1)), ((3,), (1, 1, 2)), ((2, 2, 1), (4,))):
        lhs = b_of(c + d)
        rhs = 3 ** len(d) * b_of(c) + (1 << sum(c)) * b_of(d)
        if lhs != rhs:
            bad += 1
    want("B_{CD} = 3^{L_D} B_C + 2^{Q_C} B_D", bad == 0)
    # and that it is NOT symmetric, or the semigroup test below proves nothing
    c, d = (1, 2), (2, 1, 3)
    want("the composition law is not symmetric in C and D",
         3 ** len(d) * b_of(c) + (1 << sum(c)) * b_of(d)
         != 3 ** len(c) * b_of(d) + (1 << sum(d)) * b_of(c))

    # the eraser: a contiguous case and a spliced one, so contiguity tracking
    # is exercised in both directions
    got = erase_cycles([1, 2, 4], (1, 1), 3)
    want("the eraser finds a contiguous cycle",
         len(got) == 1 and got[0][4] is True)
    want("the eraser finds nothing when residues never repeat",
         erase_cycles([1, 2], (1,), 9) == [])
    return out


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict) -> dict:
    t: dict = {"constants_checked": 0,
               "disagreeing_with_both_evaluations": 0,
               "from_the_float64_chain_not_the_nearest_double": 0,
               "exact_to_the_last_bit": 0,
               "undecided_brackets": 0,
               "missing_from_the_frontier": 0,
               "frontier_and_report_disagreeing": 0,
               "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    chain = math.log2(3)
    rc = report.get("constants", {})
    items = [
        ("beta", b_lo, b_hi, chain, 4, "beta"),
        ("fully_faithful_loop_mass_constant", 2 - b_hi, 2 - b_lo,
         2.0 - chain, 20, "fully_faithful_loop_mass_constant_decimal"),
        ("fully_faithful_loop_count_coefficient",
         (3 - 3 * b_hi / 2), (3 - 3 * b_lo / 2), 1.5 * (2.0 - chain), 20,
         "faithful_loop_count_coefficient_vs_h_over_M"),
        ("previous_three_sheet_loop_mass_constant", 1 - b_hi / 3, 1 - b_lo / 3,
         1 - chain / 3, 12, "previous_three_sheet_mass_constant"),
    ]
    for name, lo, hi, ch, budget, rkey in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub, rpt = frontier[name], rc.get(rkey)
        row = {"constant": name, "frontier": repr(pub), "report": repr(rpt),
               "budget": budget}
        if rpt is not None and rpt != pub:
            t["frontier_and_report_disagreeing"] += 1
            row["frontier_minus_report_ulps"] = bits(pub) - bits(rpt)
        verdict, d = verdict_with_budget(pub, lo, hi, ch, budget)
        if verdict == "undecided":
            t["undecided_brackets"] += 1
        elif verdict == "exact":
            t["exact_to_the_last_bit"] += 1
        elif verdict == "the float64 chain":
            t["from_the_float64_chain_not_the_nearest_double"] += 1
        else:
            t["disagreeing_with_both_evaluations"] += 1
        row["verdict"] = verdict if d == 0 else "%+d ulp, %s" % (d, verdict)
        row["nearest_double"] = repr(float(lo))
        t["rows"].append(row)
    return t


# ---------------------------------------------------------------------------
# Theorem 3.1
# ---------------------------------------------------------------------------

def check_surplus(bridges: list, depth: int = 5) -> dict:
    """The surplus identity and the alias budget it pays for."""
    t: dict = {"bridges": 0, "levels": 0,
               "surplus_identity_violations": 0,
               "budget_theorem_3_1_violations": 0,
               "levels_with_an_alias_large_edge": 0,
               "levels_where_the_budget_binds": 0,
               "largest_alias_count_seen": 0,
               "smallest_budget_slack_seen": None}
    slack = None
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h, q_total = len(w), sum(w)
        surplus = q_total - h
        if sum(q - 1 for q in w) != surplus or q_total != ceil_beta(h):
            t["surplus_identity_violations"] += 1
        for k in range(1, min(depth, h) + 1):
            t["levels"] += 1
            s = ord_two(k)
            a_k = sum(1 for q in w if q >= s)
            if a_k * max(1, s - 1) > surplus:
                t["budget_theorem_3_1_violations"] += 1
            if a_k:
                t["levels_with_an_alias_large_edge"] += 1
                t["largest_alias_count_seen"] = max(
                    t["largest_alias_count_seen"], a_k)
            # a budget that never binds bounds nothing: count the levels where
            # one more alias edge would have broken it
            if (a_k + 1) * max(1, s - 1) > surplus:
                t["levels_where_the_budget_binds"] += 1
            d = surplus - a_k * max(1, s - 1)
            if slack is None or d < slack:
                slack = d
    t["smallest_budget_slack_seen"] = slack
    return t


# ---------------------------------------------------------------------------
# Theorem 4.1's faithful core
# ---------------------------------------------------------------------------

def check_faithful_core(bridges: list, depth: int = 5,
                        unique_depth: int = 4) -> dict:
    t: dict = {"bridges": 0, "levels": 0, "cycles": 0, "edges": 0,
               "retained_edge_at_or_above_the_period": 0,
               "label_not_unique_in_the_faithful_range": 0,
               "uniqueness_checks": 0,
               "mass_below_the_finite_bound": 0,
               "levels_where_the_bound_is_positive": 0,
               "high_lift_mass_below_its_bound": 0,
               "cycle_longer_than_the_period": 0,
               "total_faithful_mass": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        for k in range(1, min(depth, h) + 1):
            t["levels"] += 1
            m, s = 3 ** k, ord_two(k)
            bad = [q >= s for q in w]
            a_k = sum(bad)
            mass = 0
            for a, b in split_runs(w, bad):
                sub = states[a:b + 1]
                for r, cyc, i0, i1, _cont in erase_cycles(sub, w[a:b], m):
                    t["cycles"] += 1
                    mass += len(cyc)
                    if len(cyc) > s:
                        t["cycle_longer_than_the_period"] += 1
                    cur = r
                    for q in cyc:
                        t["edges"] += 1
                        if q >= s:
                            t["retained_edge_at_or_above_the_period"] += 1
                        nxt = forward_target(cur, q, m)
                        # the faithfulness claim: below the period the label is
                        # the ONLY one carrying this transition
                        if k <= unique_depth:
                            t["uniqueness_checks"] += 1
                            if [p for p in range(1, s)
                                    if forward_target(cur, p, m) == nxt] != [q]:
                                t["label_not_unique_in_the_faithful_range"] += 1
                        cur = nxt
            lower = h + 1 - (a_k + 1) * s
            if mass < max(0, lower):
                t["mass_below_the_finite_bound"] += 1
            if lower > 0:
                t["levels_where_the_bound_is_positive"] += 1
            t["total_faithful_mass"] += mass

            # the high-lift refinement, with its own bound
            thr = max(1.0, 0.5 * math.log2(max(h, 2)))
            low = [ms[h - j] < thr for j in range(h + 1)]
            n_low = sum(low)
            bad2 = [bad[j] or low[j] or low[j + 1] for j in range(h)]
            mass2 = 0
            for a, b in split_runs(w, bad2):
                for _r, cyc, _i0, _i1, _c in erase_cycles(
                        states[a:b + 1], w[a:b], m):
                    mass2 += len(cyc)
            if mass2 < max(0, h + 1 - (a_k + 2 * n_low + 1) * s):
                t["high_lift_mass_below_its_bound"] += 1
    return t


# ---------------------------------------------------------------------------
# the certificate, the defect, and NO-GO 12.1
# ---------------------------------------------------------------------------

def check_defects(bridges: list, depth: int = 4) -> dict:
    """Theorem 9.1 on every graph cycle; Theorem 10.2 only where licensed.

    The quotient-layer lift needs a CONTIGUOUS orbit realization. Applying it
    to a spliced cycle is exactly what NO-GO 12.1 forbids, so the failure rate
    there is measured rather than the prohibition restated.
    """
    t: dict = {"bridges": 0, "levels": 0, "cycles": 0,
               "contiguous_cycles": 0, "spliced_cycles": 0,
               "cycle_does_not_return_to_its_residue": 0,
               "certificate_theorem_9_1_violations": 0,
               "defect_not_integral": 0,
               "quotient_lift_violations_on_contiguous_cycles": 0,
               "quotient_lift_violations_on_spliced_cycles": 0,
               "quotient_lift_holds_anyway_on_a_spliced_cycle": 0,
               "endpoints_not_congruent_to_the_residue": 0,
               "largest_absolute_defect_seen": 0,
               "defects_that_are_zero": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        if h < 3:
            continue
        for k in range(1, min(depth, max(1, h // 3)) + 1):
            t["levels"] += 1
            m = 3 ** k
            for r, cyc, i0, i1, cont in erase_cycles(states, w, m):
                t["cycles"] += 1
                cur = r
                for q in cyc:
                    cur = forward_target(cur, q, m)
                if cur != r:
                    t["cycle_does_not_return_to_its_residue"] += 1
                q_c, l_c = sum(cyc), len(cyc)
                # Theorem 9.1, on EVERY graph cycle
                if (((1 << q_c) - 3 ** l_c) * r - b_of(cyc)) % m:
                    t["certificate_theorem_9_1_violations"] += 1
                dm = defect(cyc, r, m)
                if dm is None:
                    t["defect_not_integral"] += 1
                    continue
                if dm == 0:
                    t["defects_that_are_zero"] += 1
                t["largest_absolute_defect_seen"] = max(
                    t["largest_absolute_defect_seen"], abs(dm))
                x, z = states[i0], states[i1]
                if x % m != r or z % m != r:
                    t["endpoints_not_congruent_to_the_residue"] += 1
                    continue
                n, n2 = (x - r) // m, (z - r) // m
                holds = (1 << q_c) * n2 == 3 ** l_c * n + dm
                if cont:
                    t["contiguous_cycles"] += 1
                    if not holds:
                        t["quotient_lift_violations_on_contiguous_cycles"] += 1
                else:
                    t["spliced_cycles"] += 1
                    if not holds:
                        t["quotient_lift_violations_on_spliced_cycles"] += 1
                    else:
                        t["quotient_lift_holds_anyway_on_a_spliced_cycle"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 11.1, on distinct pairs
# ---------------------------------------------------------------------------

def check_semigroup(bridges: list, depth: int = 4, cap: int = 4000) -> dict:
    """The defect composition law, and what self-composition cannot see.

    At `D = C` the law reads `d(CC) = (3^L + 2^Q) d(C)`, which is symmetric in
    its two coefficients. So the WRONG law with them swapped agrees with the
    right one on every self-composition, and the bundle's twenty
    self-compositions cannot distinguish them. Both are evaluated here, on
    self-compositions and on distinct pairs, and the difference is the finding.
    """
    t: dict = {"residue_classes": 0, "self_compositions": 0,
               "distinct_pairs": 0,
               "true_law_violations_on_self": 0,
               "true_law_violations_on_distinct_pairs": 0,
               "swapped_law_disagreeing_on_self": 0,
               "swapped_law_agreeing_on_distinct_pairs": 0,
               "swapped_law_disagreeing_on_distinct_pairs": 0,
               "pair_words_identical": 0,
               "composite_defect_not_integral": 0,
               "composed_cycle_does_not_return": 0}
    pool: dict[tuple[int, int], list[tuple[int, ...]]] = {}
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        if h < 3:
            continue
        for k in range(1, min(depth, max(1, h // 3)) + 1):
            m = 3 ** k
            for r, cyc, _i0, _i1, _c in erase_cycles(states, w, m):
                bucket = pool.setdefault((m, r), [])
                if len(bucket) < 4 and cyc not in bucket:
                    bucket.append(cyc)
        if sum(len(v) for v in pool.values()) > cap:
            break

    def law(c, d, m, r):
        dc, dd = defect(c, r, m), defect(d, r, m)
        dcd = defect(tuple(c) + tuple(d), r, m)
        if dc is None or dd is None or dcd is None:
            return None
        true_rhs = 3 ** len(d) * dc + (1 << sum(c)) * dd
        swapped = (1 << sum(d)) * dc + 3 ** len(c) * dd
        return dcd, true_rhs, swapped

    for (m, r), words in pool.items():
        if not words:
            continue
        t["residue_classes"] += 1
        for c in words:
            res = law(c, c, m, r)
            if res is None:
                t["composite_defect_not_integral"] += 1
                continue
            t["self_compositions"] += 1
            got, true_rhs, swapped = res
            if got != true_rhs:
                t["true_law_violations_on_self"] += 1
            if got != swapped:
                t["swapped_law_disagreeing_on_self"] += 1
        for i, c in enumerate(words):
            for d in words[i + 1:]:
                res = law(c, d, m, r)
                if res is None:
                    t["composite_defect_not_integral"] += 1
                    continue
                t["distinct_pairs"] += 1
                got, true_rhs, swapped = res
                if got != true_rhs:
                    t["true_law_violations_on_distinct_pairs"] += 1
                if got == swapped:
                    t["swapped_law_agreeing_on_distinct_pairs"] += 1
                else:
                    # the half that carries the finding: SOME distinct pair
                    # must separate the true law from the swapped one, or
                    # "distinct pairs can tell them apart" is empty
                    t["swapped_law_disagreeing_on_distinct_pairs"] += 1
                if tuple(c) == tuple(d):
                    t["pair_words_identical"] += 1
                cur = r
                for q in tuple(c) + tuple(d):
                    cur = forward_target(cur, q, m)
                if cur != r:
                    t["composed_cycle_does_not_return"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 6.1 and 7.1
# ---------------------------------------------------------------------------

def check_screening(bridges: list, trials: int = 12000) -> dict:
    """Endpoint and source screening, on real orbit words and synthetic ones,
    and for SHARPNESS.

    "Depends only on the final K valuations" is half a statement. The other
    half is that something inside the horizon CAN move the residue -- without
    it the horizon bounds nothing, and a residue that never moved would satisfy
    the theorem trivially.
    """
    t: dict = {"real_words": 0, "synthetic_words": 0,
               "synthetic_source_words": 0,
               "endpoint_screening_violations": 0,
               "endpoint_suffix_formula_violations": 0,
               "source_screening_violations": 0,
               "sharpness_probes": 0,
               "changes_inside_the_horizon_that_moved_nothing": 0,
               "changes_outside_the_horizon_that_moved_something": 0}
    for y, X, Z, states, w, ms in bridges[:400]:
        h = len(w)
        if h < 4:
            continue
        t["real_words"] += 1
        for k in range(1, min(4, h - 1) + 1):
            # a different prefix, same final k valuations
            alt = tuple([w[0] + 1] + list(w[1:]))
            if endpoint_mod(w, k) != endpoint_mod(alt, k) and h - 1 >= k:
                t["endpoint_screening_violations"] += 1
            if endpoint_mod(w, k) != endpoint_from_suffix(w, k):
                t["endpoint_suffix_formula_violations"] += 1
            # source side: the full representative reduces to the prefix one
            pref = w[:k]
            mod = 1 << (sum(pref) + 1)
            if source_rep(w) % mod != source_rep(pref) % mod:
                t["source_screening_violations"] += 1
            # sharpness: changing the LAST valuation is inside every horizon
            t["sharpness_probes"] += 1
            inside = tuple(list(w[:-1]) + [w[-1] + 1])
            if endpoint_mod(inside, k) == endpoint_mod(w, k):
                t["changes_inside_the_horizon_that_moved_nothing"] += 1
            # and a change strictly outside it must move nothing
            if h - 1 > k:
                outside = tuple([w[0] + 2] + list(w[1:]))
                if endpoint_mod(outside, k) != endpoint_mod(w, k):
                    t["changes_outside_the_horizon_that_moved_something"] += 1
    # their synthetic ranges, rebuilt
    for i in range(trials):
        h = 3 + (i * 7919) % 16
        k = 1 + (i * 104729) % (h - 1)
        suffix = [1 + (i * 31 + j * 17) % 5 for j in range(k)]
        p1 = [1 + (i * 13 + j * 7) % 5 for j in range(h - k)]
        p2 = [1 + (i * 29 + j * 11) % 7 for j in range(h - k)]
        w1, w2 = tuple(p1 + suffix), tuple(p2 + suffix)
        t["synthetic_words"] += 1
        a, b, c = (endpoint_mod(w1, k), endpoint_mod(w2, k),
                   endpoint_from_suffix(w1, k))
        if not a == b == c:
            t["endpoint_screening_violations"] += 1
    # and their synthetic source block, rebuilt from its stated ranges
    for i in range(trials):
        h = 3 + (i * 104729) % 12
        r = 1 + (i * 7919) % (h - 1)
        prefix = [1 + (i * 19 + j * 5) % 5 for j in range(r)]
        s1 = [1 + (i * 23 + j * 3) % 5 for j in range(h - r)]
        s2 = [1 + (i * 37 + j * 13) % 7 for j in range(h - r)]
        t["synthetic_source_words"] += 1
        mod = 1 << (sum(prefix) + 1)
        pref = source_rep(tuple(prefix))
        for tail in (s1, s2):
            if source_rep(tuple(prefix + tail)) % mod != pref % mod:
                t["source_screening_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# their three cannot-fail blocks
# ---------------------------------------------------------------------------

def check_their_algebra(trials: int = 10000) -> dict:
    """Three of the bundle's thirteen counters, 30,000 executions, none of
    which can fail. Fifth round, and the shapes are all catalogued ones."""
    t: dict = {"faithful_core_samples": 0,
               "faithful_core_gamma_not_below_eta": 0,
               "faithful_core_second_assertion_differing_from_the_first": 0,
               "faithful_core_constant_varying_across_the_loop": 0,
               "horizon_samples": 0, "horizon_could_have_failed": 0,
               "horizon_smallest_margin": None,
               "near_full_samples": 0, "near_full_could_have_failed": 0,
               "near_full_smallest_margin": None}
    c_faith = 2 - math.log2(3)
    for i in range(trials):
        t["faithful_core_samples"] += 1
        gamma = 0.03 + 0.8 * ((i * 7919) % 10007) / 10007.0
        eta = gamma + (1 - gamma) * 0.5 * ((i * 104729) % 9973) / 9973.0
        eta = min(0.99, max(gamma + 1e-3, eta))
        if not gamma < eta:
            t["faithful_core_gamma_not_below_eta"] += 1
        if (1 - eta + gamma < 1) != (gamma < eta):
            t["faithful_core_second_assertion_differing_from_the_first"] += 1
        if 2 - math.log2(3) != c_faith:
            t["faithful_core_constant_varying_across_the_loop"] += 1
    worst = None
    for i in range(trials):
        t["horizon_samples"] += 1
        c = 0.05 + 5 * ((i * 31337) % 10007) / 10007.0
        theta = 0.05 + 0.9 * ((i * 65537) % 9973) / 9973.0
        logh = 100 + 900 * ((i * 2654435761) % 9967) / 9967.0
        val = math.log(c * logh) - math.log(theta) - logh
        if not val < 0:
            t["horizon_could_have_failed"] += 1
        if worst is None or -val < worst:
            worst = -val
    t["horizon_smallest_margin"] = worst
    worst = None
    for i in range(trials):
        t["near_full_samples"] += 1
        a = 0.05 + 0.9 * ((i * 7919) % 10007) / 10007.0
        logh = 100 + 1000 * ((i * 104729) % 9973) / 9973.0
        ratio = 1 / (logh ** a)
        if not ratio < 1:
            t["near_full_could_have_failed"] += 1
        if worst is None or 1 - ratio < worst:
            worst = 1 - ratio
    t["near_full_smallest_margin"] = worst
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"examples": 0, "length_disagreeing": 0,
               "valuation_sum_disagreeing": 0,
               "defect_disagreeing": 0,
               "cycle_does_not_return": 0,
               "certificate_violations": 0,
               "label_at_or_above_the_period": 0,
               "rows": []}
    for ex in report.get("finite_graph_cycle_examples", []) or []:
        t["examples"] += 1
        m, r, w = ex["M"], ex["r"], tuple(ex["word"])
        if len(w) != ex["length"]:
            t["length_disagreeing"] += 1
        if sum(w) != ex["Q"]:
            t["valuation_sum_disagreeing"] += 1
        s = ord_two(round(math.log(m, 3)))
        if any(q >= s for q in w):
            t["label_at_or_above_the_period"] += 1
        cur = r
        for q in w:
            cur = forward_target(cur, q, m)
        if cur != r:
            t["cycle_does_not_return"] += 1
        if (((1 << sum(w)) - 3 ** len(w)) * r - b_of(w)) % m:
            t["certificate_violations"] += 1
        dm = defect(w, r, m)
        if dm != ex["defect"]:
            t["defect_disagreeing"] += 1
        t["rows"].append({"M": m, "r": r, "word": list(w), "L": len(w),
                          "Q": sum(w), "defect": dm})
    return t


# ---------------------------------------------------------------------------
# artifacts and ledger
# ---------------------------------------------------------------------------

def check_artifacts(bundle: pathlib.Path) -> dict:
    t: dict = {"files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
               "checksum_lines_naming_a_missing_file": 0,
               "files_with_no_digest_anywhere": [],
               "validation_files_named": 0,
               "validation_entries_with_a_digest": 0,
               "files_absent_from_the_validation_record": [],
               "duplicate_file_pairs": []}
    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    t["files_present"] = len(present)
    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()
              for n in present}
    listed: dict[str, str] = {}
    for line in (bundle / CHECKSUMS).read_text(encoding="utf-8").splitlines():
        if line.strip():
            d, n = line.split(None, 1)
            listed[n.strip()] = d
    t["digests_listed"] = len(listed)
    for n, d in listed.items():
        if n not in actual:
            t["checksum_lines_naming_a_missing_file"] += 1
        elif actual[n] != d:
            t["digest_mismatches"] += 1
    by_digest: dict[str, list[str]] = {}
    for n, d in actual.items():
        by_digest.setdefault(d, []).append(n)
    t["duplicate_file_pairs"] = [sorted(v) for v in by_digest.values()
                                 if len(v) > 1]
    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    named = set(val.get("utf8_checked_files", []) or [])
    t["validation_files_named"] = len(named)
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in named]
    t["files_with_no_digest_anywhere"] = [n for n in present if n not in listed]
    t["validation_status"] = val.get("status")
    t["validation_top_level_keys"] = sorted(val)
    t["validation_issue_entries"] = len(val.get("issues", []) or [])
    t["validation_flags_not_true"] = sum(
        1 for k in ("lf_only", "control_characters_clear",
                    "canonical_math_delimiters_only")
        if val.get(k) is not True)
    t["validation_counts_disagreeing_with_the_report"] = sum(
        1 for k, v in (val.get("checker_checks", {}) or {}).items()
        if v != json.loads((bundle / REPORT).read_text(
            encoding="utf-8")).get("checks", {}).get(k))
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    t: dict = {"paper_proved_items": 0, "ledger_proved_items": 0,
               "paper_open_items": 0, "ledger_open_items": 0,
               "paper_no_go_headings": 0, "ledger_no_go_items": 0,
               "ledger_has_an_open_key": False,
               "open_items_absent_from_the_ledger": [],
               "no_go_headings_absent_from_the_ledger": [],
               "heuristic_failed_its_positive_control": 0,
               "heuristic_failed_its_negative_control": 0}
    proved = re.search(r"## 19\.1(.*?)## 19\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(
            re.findall(r"^\d+\. ", proved.group(1), re.M))
    openb = re.search(r"## 19\.4(.*?)(?:\n---|\Z)", paper, re.S)
    bullets = []
    if openb:
        bullets = [b.strip(" -;.") for b in
                   re.findall(r"^- (.+)$", openb.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    proved_key = None
    for k in ledger:
        low = k.lower()
        if "proved" in low:
            proved_key = k
            t["ledger_proved_items"] = len(ledger[k])
        elif "no_go" in low or "nogo" in low or "sealed" in low:
            t["ledger_no_go_items"] = len(ledger[k])
        elif "open" in low:
            t["ledger_has_an_open_key"] = True
            t["ledger_open_items"] = len(ledger[k])
    blob = json.dumps(ledger).lower()

    def covered(text: str) -> bool:
        words = [w for w in re.findall(r"[a-z_]{4,}", text.lower())
                 if w not in ("which", "these", "there", "their", "about",
                              "that", "with", "from", "this", "than")]
        if not words:
            return True
        hit = sum(1 for w in words if w[:7] in blob)
        return hit >= max(1, len(words) // 2)

    t["open_items_absent_from_the_ledger"] = [b for b in bullets
                                              if not covered(b)]
    t["no_go_headings_absent_from_the_ledger"] = [
        n for n, hd in no_go if not covered(hd)]
    present_text = " ".join(str(x) for x in
                            (ledger.get(proved_key, []) or [""])[:1])
    t["heuristic_failed_its_positive_control"] = int(
        bool(present_text) and not covered(present_text))
    t["heuristic_failed_its_negative_control"] = int(
        covered("quokka bandersnatch flimflam zeppelin marzipan"))
    return t


def check_their_claims(report: dict, res: dict) -> dict:
    sp, fc, df = res["surplus"], res["faithful_core"], res["defects"]
    mine = {
        "finite_local_bridges": res["population"]["bridges"],
        "zero_lift_bridges": res["population"]["zero_lift"],
        "faithful_surplus_alias_budget": sp["levels"],
        "finite_fully_faithful_loop_mass": fc["levels"],
        "finite_high_lift_faithful_loop_mass": fc["levels"],
        "fully_faithful_graph_cycles": fc["cycles"],
        "graph_cycle_certificates": fc["cycles"],
        "defect_semigroup_self_composition":
            res["semigroup"]["self_compositions"],
        "endpoint_temporal_screening": res["screening"]["synthetic_words"],
        "source_temporal_screening": res["screening"]["synthetic_source_words"],
        "polynomial_precision_horizon_algebra":
            res["their_algebra"]["horizon_samples"],
        "near_full_almost_total_loop_algebra":
            res["their_algebra"]["near_full_samples"],
        "faithful_core_asymptotic_algebra":
            res["their_algebra"]["faithful_core_samples"],
    }
    rows = [{"check": k, "theirs": v, "mine": mine.get(k)}
            for k, v in report.get("checks", {}).items()]
    return {"rows": rows,
            "checks_i_did_not_reproduce": sum(1 for r in rows
                                              if r["mine"] is None),
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "counts_i_reproduce_exactly": sum(
                1 for r in rows if r["mine"] is not None
                and r["mine"] == r["theirs"])}


def check_population(all_b: list, zero_b: list) -> dict:
    return {"bridges": len(all_b), "zero_lift": len(zero_b),
            "positive_lift": len(all_b) - len(zero_b),
            "sources": len({r[0] for r in all_b}),
            "longest_tail": max((len(r[4]) for r in zero_b), default=0)}


SECTIONS = ("instrument", "constants", "population", "surplus",
            "faithful_core", "defects", "semigroup", "screening",
            "their_algebra", "examples", "artifacts", "ledger",
            "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("surplus", "surplus_identity_violations"),
    ("surplus", "budget_theorem_3_1_violations"),
    ("faithful_core", "retained_edge_at_or_above_the_period"),
    ("faithful_core", "label_not_unique_in_the_faithful_range"),
    ("faithful_core", "mass_below_the_finite_bound"),
    ("faithful_core", "high_lift_mass_below_its_bound"),
    ("faithful_core", "cycle_longer_than_the_period"),
    ("defects", "cycle_does_not_return_to_its_residue"),
    ("defects", "certificate_theorem_9_1_violations"),
    ("defects", "defect_not_integral"),
    ("defects", "quotient_lift_violations_on_contiguous_cycles"),
    ("defects", "endpoints_not_congruent_to_the_residue"),
    ("semigroup", "true_law_violations_on_self"),
    ("semigroup", "true_law_violations_on_distinct_pairs"),
    ("semigroup", "swapped_law_disagreeing_on_self"),
    ("semigroup", "pair_words_identical"),
    ("semigroup", "composite_defect_not_integral"),
    ("semigroup", "composed_cycle_does_not_return"),
    ("screening", "endpoint_screening_violations"),
    ("screening", "endpoint_suffix_formula_violations"),
    ("screening", "source_screening_violations"),
    ("screening", "changes_inside_the_horizon_that_moved_nothing"),
    ("screening", "changes_outside_the_horizon_that_moved_something"),
    ("their_algebra", "faithful_core_gamma_not_below_eta"),
    ("their_algebra", "faithful_core_second_assertion_differing_from_the_first"),
    ("their_algebra", "faithful_core_constant_varying_across_the_loop"),
    ("their_algebra", "horizon_could_have_failed"),
    ("their_algebra", "near_full_could_have_failed"),
    ("examples", "length_disagreeing"),
    ("examples", "valuation_sum_disagreeing"),
    ("examples", "defect_disagreeing"),
    ("examples", "cycle_does_not_return"),
    ("examples", "certificate_violations"),
    ("examples", "label_at_or_above_the_period"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_issue_entries"),
    ("artifacts", "validation_flags_not_true"),
    ("artifacts", "validation_counts_disagreeing_with_the_report"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("population", "bridges"),
    ("population", "sources"),
    ("surplus", "levels"),
    ("surplus", "levels_with_an_alias_large_edge"),
    ("faithful_core", "levels"),
    ("faithful_core", "cycles"),
    ("faithful_core", "edges"),
    ("faithful_core", "uniqueness_checks"),
    ("faithful_core", "total_faithful_mass"),
    ("defects", "cycles"),
    ("defects", "contiguous_cycles"),
    ("defects", "spliced_cycles"),
    ("semigroup", "residue_classes"),
    ("semigroup", "self_compositions"),
    ("semigroup", "distinct_pairs"),
    ("semigroup", "swapped_law_disagreeing_on_distinct_pairs"),
    ("screening", "real_words"),
    ("screening", "synthetic_words"),
    ("screening", "synthetic_source_words"),
    ("screening", "sharpness_probes"),
    ("their_algebra", "faithful_core_samples"),
    ("their_algebra", "horizon_samples"),
    ("their_algebra", "near_full_samples"),
    ("examples", "examples"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "frontier_and_report_disagreeing"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("population", "zero_lift"),
    ("population", "positive_lift"),
    ("population", "longest_tail"),
    ("surplus", "bridges"),
    ("surplus", "levels_where_the_budget_binds"),
    ("surplus", "largest_alias_count_seen"),
    ("surplus", "smallest_budget_slack_seen"),
    ("faithful_core", "bridges"),
    ("faithful_core", "levels_where_the_bound_is_positive"),
    ("defects", "bridges"),
    ("defects", "levels"),
    ("defects", "quotient_lift_violations_on_spliced_cycles"),
    ("defects", "quotient_lift_holds_anyway_on_a_spliced_cycle"),
    ("defects", "largest_absolute_defect_seen"),
    ("defects", "defects_that_are_zero"),
    ("semigroup", "swapped_law_agreeing_on_distinct_pairs"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_files_named"),
    ("artifacts", "validation_entries_with_a_digest"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "ledger_no_go_items"),
    ("their_claims", "checks_i_did_not_reproduce"),
    ("their_claims", "checks_they_report_as_zero"),
    ("their_claims", "counts_i_reproduce_exactly"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=220000)
    ap.add_argument("--max-steps", type=int, default=110)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    all_b = local_bridges(a.limit, a.max_steps)
    zero_b = zero_lift(a.limit, a.max_steps)

    res: dict = {}
    errors: dict = {"%s_raised" % s: 0 for s in SECTIONS}
    errors["messages"] = []

    def run(name: str, fn):
        try:
            res[name] = fn()
        except Exception as exc:                        # noqa: BLE001
            res[name] = {}
            errors["%s_raised" % name] = 1
            errors["messages"].append("%s: %s: %s"
                                      % (name, type(exc).__name__, exc))

    run("instrument", check_instrument)
    run("constants", lambda: check_constants(frontier, report))
    run("population", lambda: check_population(all_b, zero_b))
    run("surplus", lambda: check_surplus(zero_b))
    run("faithful_core", lambda: check_faithful_core(zero_b))
    run("defects", lambda: check_defects(zero_b))
    run("semigroup", lambda: check_semigroup(zero_b))
    run("screening", lambda: check_screening(zero_b))
    run("their_algebra", check_their_algebra)
    run("examples", lambda: check_examples(report))
    run("artifacts", lambda: check_artifacts(bundle))
    run("ledger", lambda: check_ledger(ledger, paper))
    run("their_claims", lambda: check_their_claims(report, res))
    res["errors"] = errors

    failures = []
    for sec, key in FAILURE_COUNTERS:
        v = res.get(sec, {}).get(key, 0)
        if (len(v) if isinstance(v, list) else v):
            failures.append("%s.%s = %s" % (sec, key, v))
    if errors["messages"]:
        failures.append("errors.messages = %s" % errors["messages"][:3])
    vacuous = ["%s.%s" % (s, k) for s, k in NON_VACUITY
               if not res.get(s, {}).get(k)]

    declared = ({(s, k) for s, k in FAILURE_COUNTERS}
                | {(s, k) for s, k in NON_VACUITY}
                | {(s, k) for s, k in OBSERVATIONS})
    unread = []
    for sec, body in res.items():
        if not isinstance(body, dict):
            continue
        for k, v in body.items():
            if isinstance(v, bool) or not isinstance(v, int):
                continue
            if (sec, k) in declared:
                continue
            unread.append("%s.%s" % (sec, k))

    out = {
        "run": "RUN-049", "round": "A-U.2d.21", "bundle": str(bundle),
        "passed": not failures and not vacuous,
        "failures": failures,
        "empty_populations": vacuous,
        "counters_not_in_the_failure_or_population_lists": sorted(unread),
        "results": res,
    }
    text = json.dumps(out, indent=2, ensure_ascii=False, default=str)
    if a.out:
        pathlib.Path(a.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
