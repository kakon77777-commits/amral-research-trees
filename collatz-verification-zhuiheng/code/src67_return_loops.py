"""RUN-048 — independent recheck of Hard-Zeta round A-U.2d.20.

`Mesoscopic Ternary Return Discrepancy Rigidity` (source item 67). 數學戰士「墜衡」.

A-U.2d.19 reduced the survivor to a zero-lift bridge and showed a FIXED ternary
modulus has too little magnitude resolution. This round asks what a GROWING one
can see, and the answer has two halves with opposite characters:

  * the endpoint is `3^k`-determined by its last `k` valuations alone, so at
    polynomial precision the canonical endpoint is an `O(log h)` boundary
    layer;
  * the bulk carries a LINEAR mass of modular return loops, each with at most
    three possible valuation labels, and each carrying the exact certificate
    `(2^{Q_C} - 3^{L_C}) r_C = B_C mod M`.

Almost all of it is exact integer or exact modular arithmetic. The round's
central new object is the return loop, and the loop certificate is the sharpest
thing in it -- so this gate builds the loops and checks the certificate, which
the shipped checker does not: its loop block verifies mass lower bounds only.

Three more things this gate does that the shipped checker does not.

Theorem 3.1's boxed statement is the k-TERM truncated sum
`Z = sum_{j=1}^{k} 3^{j-1} 2^{-Q_j} mod 3^k`. The bundle checks the full
endpoint representative of the k-suffix against `Z mod 3^k`, which is the same
value but not the same sentence: what makes the theorem "boundary locality" is
that the terms beyond `j = k` contribute nothing, and that is checked here
separately.

Theorem 5.1's period `s_k = ord_M(2)` and Corollary 5.2's three sheets are
checked SHARP: the bundle verifies uniqueness below `s_k` and at most three
labels below `2M`; it does not verify that a collision actually occurs at
`s_k`, nor that three sheets are attained. An upper bound with no attained case
is compatible with a period three times too long.

And `fixed_power_high_lift_algebra`, ten thousand iterations, contains three
assertions: one arranged by the line above it, one that is the same inequality
restated, and one on a constant computed outside the loop.

Usage:
    python code/src67_return_loops.py --bundle <dir> [--limit N]
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
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src53_plateau_reset import ln2_bracket, v2                     # noqa: E402
from src54_low_source_saturation import widen                       # noqa: E402
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    b_of, beta_hi, beta_lo, verdict_with_budget,
)
from src65_lift_cocycle import (                                    # noqa: E402
    ceil_beta, lift_profile, local_bridges, mech_a,
)
from src66_carry_conjugacy import suffix_sums                       # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d20_Mesoscopic_Ternary_Return"
         "_Discrepancy_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d20_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d20_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d20_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d20.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.20_AU2d20.md"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def ord_two(k: int) -> int:
    """`ord_{3^k}(2) = 2 * 3^{k-1}`, since 2 is a primitive root mod 3^k."""
    return 2 * 3 ** (k - 1)


def forward_target(r: int, q: int, m: int) -> int:
    """The accelerated map read on residues: `r' = (3r+1) 2^{-q} mod M`."""
    return (3 * r + 1) * pow(pow(2, q, m), -1, m) % m


def zero_lift_bridges(limit: int, max_steps: int):
    """The bundle's population, restricted to the zero-lift class."""
    out = []
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        ms = lift_profile(w)
        if ms[len(w)] != 0:
            continue
        out.append((y, X, Z, list(vals[1:]), w, ms))
    return out


def return_loops(states: list[int], word: tuple[int, ...], m: int,
                 cap: int = 400) -> list[tuple[int, int, int]]:
    """Chronological modular return loops, as `(i, j, cycle_length)`.

    `states[i] = states[j] mod m`, so the ORBIT SEGMENT `i..j` carries an exact
    affine identity and hence Theorem 11.1's certificate. Its length is `j - i`.

    The loop-erased CYCLE is a different object: the vertices still on the
    stack from the first occurrence onwards, all carrying distinct unit
    residues. Its length is the stack-depth difference, and it is that one
    Corollary 10.2 bounds by `s_k = 2M/3`, because there are only that many
    units to be distinct in.

    The two coincide only when nothing was erased inside the segment. Both are
    returned, because applying either bound to the other object is wrong in a
    way that reads as a violation.
    """
    out: list[tuple[int, int]] = []
    stack: list[int] = []          # positions, residues all distinct
    pos: dict[int, int] = {}       # residue -> index into `stack`
    for j, s in enumerate(states):
        r = s % m
        if r in pos:
            p = pos[r]
            out.append((stack[p], j, len(stack) - p))
            # everything after the first occurrence is inside the emitted loop
            # and must leave the stack, or a later "loop" would span it
            for old in stack[p + 1:]:
                pos.pop(states[old] % m, None)
            stack = stack[:p + 1]
            if len(out) >= cap:
                break
        else:
            pos[r] = len(stack)
            stack.append(j)
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

    # the order of 2 modulo 3^k, both ways round
    bad, loose = 0, 0
    for k in range(1, 9):
        m = 3 ** k
        if pow(2, ord_two(k), m) != 1:
            bad += 1
        # an upper bound on the order is not the order: no maximal proper
        # divisor may work either
        s = ord_two(k)
        if k >= 2 and (pow(2, s // 3, m) == 1 or pow(2, s // 2, m) == 1):
            loose += 1
    want("2^{2*3^{k-1}} = 1 mod 3^k", bad == 0)
    want("no maximal proper divisor of the order works", loose == 0)

    # The first version of this asserted that `r -> (3r+1) 2^-q` is injective
    # on units. It is not -- `3r mod 3^k` is THREE-to-one, collapsing residues
    # that agree mod 3^{k-1} -- and the check caught the claim, which is what a
    # check is for. The variable the round actually reads is the other one:
    # for a FIXED source residue, `q -> r'` has period exactly ord_M(2), and
    # that is what makes a transition pair determine q.
    bad, degenerate = 0, 0
    for k in (1, 2, 3):
        m = 3 ** k
        s = ord_two(k)
        for r in (1, 2, m - 1):
            if r % 3 == 0:
                continue
            if forward_target(r, s, m) != forward_target(r, 0, m):
                bad += 1
            # and no shorter period, or "determines q modulo s" would be wrong
            if s > 1 and forward_target(r, s // 2 or 1, m) == forward_target(r, 0, m) \
                    and (s // 2 or 1) != s:
                degenerate += 1
    want("q -> r' has period ord_M(2) for a fixed source residue", bad == 0)
    want("and no half-period works", degenerate == 0)
    # the collapsing direction, stated correctly so it is on the record
    m = 27
    want("r -> 3r+1 is three-to-one mod 3^k",
         len({(3 * r + 1) % m for r in range(m) if r % 3}) == len(
             [r for r in range(m) if r % 3]) // 3)

    # a_j <= 2 is what turns the source budget into 2r
    want("every mechanical increment is at most two",
         all(mech_a(j) <= 2 for j in range(1, 500)))

    # loop extraction on a hand case: residues 1,2,1 give exactly one loop (0,2)
    want("the loop walker finds the obvious loop with both lengths",
         return_loops([1, 2, 4], (1, 1), 3) == [(0, 2, 2)])
    want("the loop walker finds none when residues never repeat",
         return_loops([1, 2], (1,), 9) == [])
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
               "duplicate_keys_carrying_the_same_value": 0,
               "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    chain = math.log2(3)
    items = [
        ("beta", b_lo, b_hi, chain, 4, "beta"),
        ("linear_return_loop_mass_constant", 1 - b_hi / 3, 1 - b_lo / 3,
         1 - chain / 3, 12, "linear_clean_loop_mass_constant"),
        ("linear_return_loop_count_coefficient", (3 - b_hi) / 2, (3 - b_lo) / 2,
         (3 - chain) / 2, 12, "clean_loop_count_coefficient_vs_h_over_M"),
    ]
    rc = report.get("constants", {})
    for name, lo, hi, ch, budget, rkey in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        rpt = rc.get(rkey)
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
    # RUN-047 found the frontier and the report disagreeing on beta. Two keys
    # in this report carry the same value under different names, which is the
    # opposite failure and worth its own count.
    vals: dict = {}
    for k, v in rc.items():
        if isinstance(v, float):
            vals.setdefault(v, []).append(k)
    t["duplicate_keys_carrying_the_same_value"] = sum(
        1 for names in vals.values() if len(names) > 1)
    t["duplicate_key_groups"] = [sorted(n) for n in vals.values() if len(n) > 1]
    return t


# ---------------------------------------------------------------------------
# Theorem 3.1, in the form it is stated in
# ---------------------------------------------------------------------------

def check_locality(bridges: list) -> dict:
    """The boxed statement is a k-TERM sum, and its content is that the terms
    beyond `k` contribute nothing modulo `3^k`.

    The bundle compares the k-suffix's full endpoint representative against
    `Z mod 3^k`. Same value, different sentence -- it verifies that the suffix
    determines the residue, not that only the FIRST k terms of the sum do.
    Three things are checked here: the truncated sum, the full sum, and their
    agreement.
    """
    t: dict = {"bridges": 0, "levels": 0,
               "truncated_sum_violations": 0,
               "full_sum_violations": 0,
               "truncation_changes_the_residue": 0,
               "tail_term_not_divisible_by_the_modulus": 0,
               "suffix_representative_violations": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        Qs = suffix_sums(w)
        for k in range(1, h + 1):
            t["levels"] += 1
            mod = 3 ** k
            trunc = sum(3 ** (j - 1) * pow(pow(2, Qs[j], mod), -1, mod)
                        for j in range(1, k + 1)) % mod
            full = sum(3 ** (j - 1) * pow(pow(2, Qs[j], mod), -1, mod)
                       for j in range(1, h + 1)) % mod
            if (Z - trunc) % mod:
                t["truncated_sum_violations"] += 1
            if (Z - full) % mod:
                t["full_sum_violations"] += 1
            if trunc != full:
                t["truncation_changes_the_residue"] += 1
            # the reason: every term past j = k carries 3^{j-1} with j-1 >= k
            for j in range(k + 1, min(h, k + 3) + 1):
                if 3 ** (j - 1) % mod:
                    t["tail_term_not_divisible_by_the_modulus"] += 1
            # and the bundle's own form, so the comparison is like for like
            suf = w[h - k:]
            b, qq = b_of(suf), sum(suf)
            r = b * pow(pow(2, qq, mod), -1, mod) % mod
            if (Z - r) % mod:
                t["suffix_representative_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 4.1
# ---------------------------------------------------------------------------

def check_source_budget(bridges: list) -> dict:
    """`P_r <= ceil(beta h) - ceil(beta(h-r)) <= 2r`, two halves with different
    proofs and therefore two counters.

    The left inequality is zero total lift plus suffix supercriticality; the
    right is `a_j <= 2` summed. The bundle asserts them in one chained
    expression, so a failure of either reads the same.
    """
    t: dict = {"bridges": 0, "prefixes": 0,
               "left_inequality_violations": 0,
               "right_inequality_violations": 0,
               "left_inequality_attained": 0,
               "right_inequality_attained": 0,
               "largest_prefix_over_r_seen": None,
               "single_valuation_above_two_r": 0}
    worst = None
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        for r in range(1, h + 1):
            t["prefixes"] += 1
            pr = sum(w[:r])
            mid = ceil_beta(h) - ceil_beta(h - r)
            if pr > mid:
                t["left_inequality_violations"] += 1
            elif pr == mid:
                t["left_inequality_attained"] += 1
            if mid > 2 * r:
                t["right_inequality_violations"] += 1
            elif mid == 2 * r:
                t["right_inequality_attained"] += 1
            if max(w[:r]) > 2 * r:
                t["single_valuation_above_two_r"] += 1
            f = Fraction(pr, r)
            if worst is None or f > worst:
                worst = f
    t["largest_prefix_over_r_seen"] = None if worst is None else float(worst)
    return t


# ---------------------------------------------------------------------------
# Theorem 5.1 and Corollary 5.2, checked SHARP
# ---------------------------------------------------------------------------

def check_labels(depth: int = 5) -> dict:
    """Label uniqueness below `s_k`, three sheets below `2M`, and both bounds
    checked for ATTAINMENT.

    An upper bound with no attained case is compatible with a period three
    times too long: `q < s_k` unique would also hold if the true period were
    `3 s_k`. So the collision AT `s_k` and a residue actually carrying three
    labels are separate counters.
    """
    t: dict = {"levels": 0, "pairs": 0, "sheet_checks": 0,
               "label_collisions_below_the_period": 0,
               "no_collision_at_the_period": 0,
               "more_than_three_sheets": 0,
               "three_sheets_never_attained": 0,
               "period_disagreeing_with_two_thirds_m": 0,
               "residues_with_exactly_three_sheets": 0}
    for k in range(1, depth + 1):
        t["levels"] += 1
        m = 3 ** k
        s = ord_two(k)
        if s != 2 * m // 3:
            t["period_disagreeing_with_two_thirds_m"] += 1
        units = [r for r in range(m) if r % 3]
        three_seen = False
        for r in units:
            seen: dict[int, int] = {}
            for q in range(1, s):
                tgt = forward_target(r, q, m)
                t["pairs"] += 1
                if tgt in seen:
                    t["label_collisions_below_the_period"] += 1
                seen[tgt] = q
            # sharpness: q = s must return to the q = 0 label, i.e. the period
            # is attained rather than merely an upper bound
            if forward_target(r, s, m) != forward_target(r, 0, m):
                t["no_collision_at_the_period"] += 1
            mult: dict[int, int] = {}
            for q in range(1, 2 * m):
                mult[forward_target(r, q, m)] = mult.get(
                    forward_target(r, q, m), 0) + 1
            t["sheet_checks"] += 1
            top = max(mult.values())
            if top > 3:
                t["more_than_three_sheets"] += 1
            if top == 3:
                three_seen = True
                t["residues_with_exactly_three_sheets"] += 1
        if not three_seen:
            t["three_sheets_never_attained"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 6.1
# ---------------------------------------------------------------------------

def check_alias_budget(bridges: list, depth: int = 5) -> dict:
    t: dict = {"bridges": 0, "levels": 0,
               "budget_theorem_6_1_violations": 0,
               "large_edge_budget_violations": 0,
               "total_valuation_not_the_ceiling": 0,
               "levels_with_an_alias_large_edge": 0,
               "largest_alias_count_seen": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h, q_total = len(w), sum(w)
        if q_total != ceil_beta(h):
            t["total_valuation_not_the_ceiling"] += 1
        for k in range(1, min(depth, h) + 1):
            t["levels"] += 1
            m, s = 3 ** k, ord_two(k)
            b = sum(1 for q in w if q >= s)
            if b * s > q_total:
                t["budget_theorem_6_1_violations"] += 1
            b2 = sum(1 for q in w if q >= 2 * m)
            if b2 * 2 * m > q_total:
                t["large_edge_budget_violations"] += 1
            if b:
                t["levels_with_an_alias_large_edge"] += 1
            t["largest_alias_count_seen"] = max(
                t["largest_alias_count_seen"], b)
    return t


# ---------------------------------------------------------------------------
# the return loops and their certificate
# ---------------------------------------------------------------------------

def check_loops(bridges: list, depth: int = 4) -> dict:
    """Theorem 11.1's certificate, on loops built from the real orbits.

    `(2^{Q_C} - 3^{L_C}) r_C = B_C mod M`. The shipped checker builds the same
    loop-erasure but verifies only the mass lower bound; the certificate is the
    sharpest object the round produces and it is exact modular arithmetic, so
    it is checked here on every loop found.

    The certificate follows from the exact INTEGER affine identity on the
    segment, so that is checked too and the derivation is not assumed.
    """
    t: dict = {"bridges": 0, "levels": 0, "loops": 0,
               "loop_endpoints_not_congruent": 0,
               "segment_affine_identity_violations": 0,
               "certificate_theorem_11_1_violations": 0,
               "erased_cycle_longer_than_the_period": 0,
               "segment_longer_than_the_period": 0,
               "segment_longer_than_its_erased_cycle": 0,
               "longest_erased_cycle_seen": 0,
               "loop_of_zero_length": 0,
               "certificate_trivially_zero": 0,
               "longest_loop_seen": 0,
               "total_loop_edge_mass": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        if h < 3:
            continue
        for k in range(1, min(depth, max(1, h // 3)) + 1):
            t["levels"] += 1
            m, s = 3 ** k, ord_two(k)
            for i, j, cyc in return_loops(states, w, m):
                t["loops"] += 1
                lc, qc = j - i, sum(w[i:j])
                rc = states[i] % m
                bc = b_of(tuple(w[i:j]))
                if lc <= 0:
                    t["loop_of_zero_length"] += 1
                    continue
                if states[j] % m != rc:
                    t["loop_endpoints_not_congruent"] += 1
                # the exact integer identity the certificate is a shadow of
                if (1 << qc) * states[j] != 3 ** lc * states[i] + bc:
                    t["segment_affine_identity_violations"] += 1
                if ((1 << qc) - 3 ** lc) * rc % m != bc % m:
                    t["certificate_theorem_11_1_violations"] += 1
                # the period bounds the ERASED CYCLE, whose vertices carry
                # distinct unit residues and so cannot exceed 2M/3 of them
                if cyc > s:
                    t["erased_cycle_longer_than_the_period"] += 1
                # the ORBIT SEGMENT carrying the certificate is a different
                # object and is not bounded by the period: it can enclose
                # previously erased loops. Counted, not called a violation.
                if lc > s:
                    t["segment_longer_than_the_period"] += 1
                if lc != cyc:
                    t["segment_longer_than_its_erased_cycle"] += 1
                t["longest_erased_cycle_seen"] = max(
                    t["longest_erased_cycle_seen"], cyc)
                # a certificate whose two sides are both zero mod M says
                # nothing; count them rather than let them pad the total
                if ((1 << qc) - 3 ** lc) % m == 0 and bc % m == 0:
                    t["certificate_trivially_zero"] += 1
                t["longest_loop_seen"] = max(t["longest_loop_seen"], lc)
                t["total_loop_edge_mass"] += lc
    return t


def clean_runs(states: list[int], word: tuple[int, ...], ms: list[int],
               thr: float, qthr: int) -> tuple[int, list[tuple[int, int]]]:
    """The bundle's edge deletion: drop every edge with `q >= 2M` and every
    edge touching a vertex whose reverse lift is below the threshold.

    The chronological vertex `j` carries the reverse lift `m_{h-j}`, which is
    the one index flip in the whole construction and the obvious place to get
    it wrong.
    """
    h = len(word)
    low = [ms[h - j] < thr for j in range(h + 1)]
    bad = [word[j] >= qthr or low[j] or low[j + 1] for j in range(h)]
    runs, j = [], 0
    while j < h:
        while j < h and bad[j]:
            j += 1
        if j >= h:
            break
        a = j
        while j < h and not bad[j]:
            j += 1
        runs.append((a, j))
    return sum(low), runs


def erased_mass(residues: list[int]) -> tuple[int, int]:
    """Loop-erase one run; return the erased edge mass and the residual simple
    path length. The mass is counted in STACK depth, which is what makes the
    residual path shorter than the number of unit residues."""
    stack: list[int] = []
    pos: dict[int, int] = {}
    erased = 0
    for v in residues:
        if v in pos:
            p = pos[v]
            erased += len(stack) - p
            for old in stack[p + 1:]:
                pos.pop(old, None)
            stack = stack[:p + 1]
        else:
            pos[v] = len(stack)
            stack.append(v)
    return erased, len(stack)


def check_clean_mass(bridges: list) -> dict:
    """Theorem 9.1's finite lower bound `mass >= h + 1 - (b + 2L + 1) s_k`.

    Rebuilt from the construction rather than accepted, and with the slack
    measured: a lower bound that is never approached says less than a bound
    that is, and 0 violations alone cannot tell the two apart.
    """
    t: dict = {"bridges": 0, "levels": 0, "runs": 0,
               "mass_below_the_finite_bound": 0,
               "residual_path_longer_than_the_period": 0,
               "non_unit_residue_in_a_clean_run": 0,
               "low_lift_vertex_inside_a_clean_run": 0,
               "large_edge_inside_a_clean_run": 0,
               "erasure_accounting_violations": 0,
               "levels_where_the_bound_is_positive": 0,
               "levels_where_the_bound_is_attained": 0,
               "float_depth_disagreeing_with_the_integer_one": 0,
               "smallest_mass_minus_bound_seen": None,
               "total_clean_mass": 0}
    slack = None
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        if h < 3:
            continue
        t["bridges"] += 1
        thr = max(1.0, 0.5 * math.log2(max(h, 2)))
        # their loop bound uses a float logarithm; the integer one is the
        # number of ternary digits. A disagreement would silently change the
        # population, so it is counted rather than assumed away.
        depth_f = min(4, int(math.log(max(h, 3), 3)) + 1)
        # the exact one: the largest e with 3^e <= h, by multiplication
        e, p = 0, 1
        while p * 3 <= max(h, 3):
            e += 1
            p *= 3
        depth_i = min(4, e + 1)
        if depth_f != depth_i:
            t["float_depth_disagreeing_with_the_integer_one"] += 1
        # their loop is `range(1, depth)`, which is EXCLUSIVE of depth
        for k in range(1, depth_f):
            t["levels"] += 1
            m, s = 3 ** k, ord_two(k)
            qthr = 2 * m
            b = sum(1 for q in w if q >= qthr)
            low_count, runs = clean_runs(states, w, ms, thr, qthr)
            mass = 0
            for a, bb in runs:
                t["runs"] += 1
                res = [states[j] % m for j in range(a, bb + 1)]
                if any(r % 3 == 0 for r in res):
                    t["non_unit_residue_in_a_clean_run"] += 1
                # what "clean" MEANS, asserted directly. The mass comparison
                # below is vacuous on all but a handful of levels, so without
                # these two the deletion rule itself is untested.
                for j in range(a, bb + 1):
                    if ms[h - j] < thr:
                        t["low_lift_vertex_inside_a_clean_run"] += 1
                for j in range(a, bb):
                    if w[j] >= qthr:
                        t["large_edge_inside_a_clean_run"] += 1
                em, rest = erased_mass(res)
                if rest > s:
                    t["residual_path_longer_than_the_period"] += 1
                # loop erasure conserves edges: every edge of the run is either
                # inside an erased loop or on the residual simple path. This is
                # total -- it holds at every level, vacuous bound or not.
                if em + rest - 1 != bb - a:
                    t["erasure_accounting_violations"] += 1
                mass += em
            lower = h + 1 - (b + 2 * low_count + 1) * s
            if mass < max(0, lower):
                t["mass_below_the_finite_bound"] += 1
            if lower > 0:
                t["levels_where_the_bound_is_positive"] += 1
                if mass == lower:
                    t["levels_where_the_bound_is_attained"] += 1
                d = mass - lower
                if slack is None or d < slack:
                    slack = d
            t["total_clean_mass"] += mass
    t["smallest_mass_minus_bound_seen"] = slack
    return t


# ---------------------------------------------------------------------------
# their two synthetic blocks
# ---------------------------------------------------------------------------

def check_their_algebra(trials: int = 10000) -> dict:
    """`fixed_power_high_lift_algebra` has three assertions and none can fail.

        eta = min(0.98, max(gamma+0.01, eta))
        assert gamma < eta          # arranged by the line above
        err_exp = 1-eta+gamma
        assert err_exp < 1          # the SAME inequality, restated
        assert C_LOOP > 0           # a constant computed outside the loop

    `boundary_alias_no_go_algebra` is a fourth shape: the assertion is preceded
    by a REPAIR branch that fixes any input that would have failed it.

        if lhs_log <= 0:
            hlog = max(hlog, 10/(1-gamma)); lhs_log = ...
        assert lhs_log > 0

    So the measurable question is how often the repair fires, and what the
    assertion would have said without it.
    """
    t: dict = {"high_lift_samples": 0,
               "high_lift_gamma_not_below_eta": 0,
               "high_lift_second_assertion_differing_from_the_first": 0,
               "high_lift_constant_varying_across_the_loop": 0,
               "alias_samples": 0,
               "alias_repair_fired": 0,
               "alias_would_have_failed_without_the_repair": 0,
               "alias_assertion_failed_after_the_repair": 0,
               "alias_smallest_left_side_before_the_repair": None,
               "alias_smallest_left_side_after_the_repair": None}
    c_loop = 1 - math.log2(3) / 3
    for i in range(trials):
        t["high_lift_samples"] += 1
        gamma = 0.05 + 0.55 * ((i * 7919) % 10007) / 10007.0
        eta = gamma + (0.05 + (0.95 - gamma) * ((i * 104729) % 9973) / 9973.0) * (1 - gamma)
        eta = min(0.98, max(gamma + 0.01, eta))
        if not gamma < eta:
            t["high_lift_gamma_not_below_eta"] += 1
        # the two assertions are the same inequality; if they ever disagreed
        # the claim in the docstring would be wrong
        if (1 - eta + gamma < 1) != (gamma < eta):
            t["high_lift_second_assertion_differing_from_the_first"] += 1
        if 1 - math.log2(3) / 3 != c_loop:
            t["high_lift_constant_varying_across_the_loop"] += 1

    before, after = None, None
    for i in range(trials):
        t["alias_samples"] += 1
        gamma = 0.05 + 0.9 * ((i * 31337) % 10007) / 10007.0
        hlog = 100 + 500 * ((i * 65537) % 9973) / 9973.0
        lhs0 = (1 - gamma) * hlog - math.log(hlog)
        if before is None or lhs0 < before:
            before = lhs0
        if lhs0 <= 0:
            t["alias_would_have_failed_without_the_repair"] += 1
            t["alias_repair_fired"] += 1
            hlog = max(hlog, 10 / (1 - gamma))
            lhs = (1 - gamma) * hlog - math.log(hlog)
        else:
            lhs = lhs0
        if not lhs > 0:
            t["alias_assertion_failed_after_the_repair"] += 1
        if after is None or lhs < after:
            after = lhs
    t["alias_smallest_left_side_before_the_repair"] = before
    t["alias_smallest_left_side_after_the_repair"] = after
    return t


# ---------------------------------------------------------------------------
# their near-full diagnostic rows
# ---------------------------------------------------------------------------

def check_near_full(report: dict) -> dict:
    t: dict = {"rows_published": 0, "rows_i_rebuilt": 0,
               "k_disagreeing": 0, "alias_bound_disagreeing": 0,
               "faithful_run_disagreeing": 0,
               "modulus_bracket_violations": 0,
               "alias_fraction_not_decreasing_end_to_end": 0,
               "faithful_run_not_increasing_end_to_end": 0,
               "rows": []}
    rows = report.get("near_full_diagnostics", []) or []
    t["rows_published"] = len(rows)
    mine = []
    for row in rows:
        power = row["h_power10"]
        h = 10 ** power
        target = h / (math.log(h) ** 0.5)
        k = max(1, math.floor(math.log(target, 3)))
        m = 3 ** k
        if not m <= target < 3 * m:
            t["modulus_bracket_violations"] += 1
        q = math.ceil(math.log2(3) * h)
        b = q // ord_two(k)
        run = max(0, math.ceil((k - b) / (b + 1))) if b < k else 0
        t["rows_i_rebuilt"] += 1
        if k != row["k"]:
            t["k_disagreeing"] += 1
        if b != row["alias_bound"]:
            t["alias_bound_disagreeing"] += 1
        if run != row["faithful_run_lower_bound"]:
            t["faithful_run_disagreeing"] += 1
        mine.append((power, k, b, run, b / k))
        t["rows"].append({"h_power10": power, "k": k, "alias_bound": b,
                          "alias_fraction": b / k, "faithful_run": run})
    if len(mine) >= 2:
        if not mine[-1][4] < mine[0][4]:
            t["alias_fraction_not_decreasing_end_to_end"] += 1
        if not mine[-1][3] > mine[0][3]:
            t["faithful_run_not_increasing_end_to_end"] += 1
    return t


def check_examples(report: dict, bridges: list) -> dict:
    t: dict = {"examples": 0, "example_not_found_in_my_population": 0,
               "x_disagreeing": 0, "z_disagreeing": 0,
               "h_disagreeing": 0, "modulus_disagreeing": 0,
               "phi_disagreeing": 0,
               "low_vertex_count_disagreeing": 0,
               "large_edge_count_disagreeing": 0,
               "lower_bound_disagreeing": 0,
               "mass_below_their_lower_bound": 0,
               "rows": []}
    # keyed on (y, Z), not on y: one source can contribute several bridges,
    # and keying on y alone silently compared the wrong one
    by_key: dict[tuple, tuple] = {}
    for rec in bridges:
        by_key.setdefault((rec[0], rec[2]), rec)
    for ex in report.get("finite_loop_examples", []) or []:
        t["examples"] += 1
        rec = by_key.get((ex["y"], ex["Z"]))
        if rec is None:
            t["example_not_found_in_my_population"] += 1
            continue
        y, X, Z, states, w, ms = rec
        h = len(w)
        if X != ex["X"]:
            t["x_disagreeing"] += 1
        if Z != ex["Z"]:
            t["z_disagreeing"] += 1
        if h != ex["h"]:
            t["h_disagreeing"] += 1
        m = ex["modulus"]
        k = round(math.log(m, 3))
        if 3 ** k != m:
            t["modulus_disagreeing"] += 1
        if ord_two(k) != ex["phi"]:
            t["phi_disagreeing"] += 1
        thr = ex["lift_threshold"]
        low = sum(1 for x in ms if x < thr)
        if low != ex["low_vertices"]:
            t["low_vertex_count_disagreeing"] += 1
        big = sum(1 for q in w if q >= 2 * m)
        if big != ex["q_ge_2M_edges"]:
            t["large_edge_count_disagreeing"] += 1
        lower = max(0, h + 1 - (big + 2 * low + 1) * ord_two(k))
        if lower != ex["exact_lower_bound"]:
            t["lower_bound_disagreeing"] += 1
        if ex["clean_loop_edge_mass"] < ex["exact_lower_bound"]:
            t["mass_below_their_lower_bound"] += 1
        t["rows"].append({"y": y, "X": X, "Z": Z, "h": h, "M": m,
                          "phi": ord_two(k), "low_vertices": low,
                          "q_ge_2M": big, "their_mass": ex["clean_loop_edge_mass"],
                          "their_lower_bound": ex["exact_lower_bound"]})
    return t


# ---------------------------------------------------------------------------
# artifacts and ledger
# ---------------------------------------------------------------------------

def check_artifacts(bundle: pathlib.Path) -> dict:
    t: dict = {"files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
               "checksum_lines_naming_a_missing_file": 0,
               "files_with_no_digest_anywhere": [],
               "validation_per_file_entries": 0,
               "validation_entries_with_a_digest": 0,
               "validation_digest_mismatches": 0,
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
    files = val.get("files", {}) or {}
    with_digest = set()
    for n, r in files.items():
        t["validation_per_file_entries"] += 1
        if isinstance(r, dict) and "sha256" in r:
            t["validation_entries_with_a_digest"] += 1
            with_digest.add(n)
            if n in actual and actual[n] != r["sha256"]:
                t["validation_digest_mismatches"] += 1
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in files]
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_status"] = val.get("status")
    t["validation_top_level_keys"] = sorted(val)
    t["validation_issue_entries"] = len(val.get("issues", []) or [])
    t["validation_json_parse_ok"] = val.get("json_parse_ok")
    t["validation_python_compile_ok"] = val.get("python_compile_ok")
    t["validation_flags_not_true"] = sum(
        1 for r in files.values() if isinstance(r, dict)
        and not (r.get("utf8") and r.get("lf_only")
                 and r.get("control_chars") == 0
                 and r.get("forbidden_math_delimiters") is False
                 and r.get("double_dollar_even")))
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
    proved = re.search(r"## 18\.1(.*?)## 18\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(
            re.findall(r"^\d+\. ", proved.group(1), re.M))
    openb = re.search(r"## 18\.4(.*?)(?:\n---|\Z)", paper, re.S)
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
    lo, sb, la = res["locality"], res["source_budget"], res["labels"]
    mine = {
        "finite_local_bridges": res["population"]["bridges"],
        "zero_lift_bridges": res["population"]["zero_lift"],
        "endpoint_boundary_locality": lo["levels"],
        "source_boundary_valuation_budget": sb["prefixes"],
        "transition_label_faithfulness": la["pairs"],
        "three_sheet_bound": la["sheet_checks"],
        "alias_budget_actual": res["alias"]["levels"],
        "clean_loop_mass_finite": res["clean_mass"]["levels"],
        "clean_loop_cycles": res["clean_mass"]["runs"],
        "near_full_boundary_algebra": res["near_full"]["rows_i_rebuilt"],
        "fixed_power_high_lift_algebra": res["their_algebra"]["high_lift_samples"],
        "boundary_alias_no_go_algebra": res["their_algebra"]["alias_samples"],
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


def check_population(bridges_all: list, bridges: list) -> dict:
    return {"bridges": len(bridges_all), "zero_lift": len(bridges),
            "positive_lift": len(bridges_all) - len(bridges),
            "sources": len({r[0] for r in bridges_all}),
            "longest_tail": max((len(r[4]) for r in bridges), default=0)}


SECTIONS = ("instrument", "constants", "population", "locality",
            "source_budget", "labels", "alias", "loops", "clean_mass",
            "their_algebra",
            "near_full", "examples", "artifacts", "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("locality", "truncated_sum_violations"),
    ("locality", "full_sum_violations"),
    ("locality", "truncation_changes_the_residue"),
    ("locality", "tail_term_not_divisible_by_the_modulus"),
    ("locality", "suffix_representative_violations"),
    ("source_budget", "left_inequality_violations"),
    ("source_budget", "right_inequality_violations"),
    ("source_budget", "single_valuation_above_two_r"),
    ("labels", "label_collisions_below_the_period"),
    ("labels", "no_collision_at_the_period"),
    ("labels", "more_than_three_sheets"),
    ("labels", "three_sheets_never_attained"),
    ("labels", "period_disagreeing_with_two_thirds_m"),
    ("alias", "budget_theorem_6_1_violations"),
    ("alias", "large_edge_budget_violations"),
    ("alias", "total_valuation_not_the_ceiling"),
    ("loops", "loop_endpoints_not_congruent"),
    ("loops", "segment_affine_identity_violations"),
    ("loops", "certificate_theorem_11_1_violations"),
    ("loops", "erased_cycle_longer_than_the_period"),
    ("loops", "loop_of_zero_length"),
    ("clean_mass", "mass_below_the_finite_bound"),
    ("clean_mass", "residual_path_longer_than_the_period"),
    ("clean_mass", "non_unit_residue_in_a_clean_run"),
    ("clean_mass", "low_lift_vertex_inside_a_clean_run"),
    ("clean_mass", "large_edge_inside_a_clean_run"),
    ("clean_mass", "erasure_accounting_violations"),
    ("clean_mass", "float_depth_disagreeing_with_the_integer_one"),
    ("their_algebra", "high_lift_gamma_not_below_eta"),
    ("their_algebra", "high_lift_second_assertion_differing_from_the_first"),
    ("their_algebra", "high_lift_constant_varying_across_the_loop"),
    ("their_algebra", "alias_assertion_failed_after_the_repair"),
    ("near_full", "k_disagreeing"),
    ("near_full", "alias_bound_disagreeing"),
    ("near_full", "faithful_run_disagreeing"),
    ("near_full", "modulus_bracket_violations"),
    ("near_full", "alias_fraction_not_decreasing_end_to_end"),
    ("near_full", "faithful_run_not_increasing_end_to_end"),
    ("examples", "example_not_found_in_my_population"),
    ("examples", "x_disagreeing"),
    ("examples", "z_disagreeing"),
    ("examples", "h_disagreeing"),
    ("examples", "modulus_disagreeing"),
    ("examples", "phi_disagreeing"),
    ("examples", "low_vertex_count_disagreeing"),
    ("examples", "large_edge_count_disagreeing"),
    ("examples", "lower_bound_disagreeing"),
    ("examples", "mass_below_their_lower_bound"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_digest_mismatches"),
    ("artifacts", "validation_issue_entries"),
    ("artifacts", "validation_flags_not_true"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("population", "bridges"),
    ("population", "sources"),
    ("locality", "bridges"),
    ("locality", "levels"),
    ("source_budget", "prefixes"),
    ("source_budget", "left_inequality_attained"),
    ("labels", "levels"),
    ("labels", "pairs"),
    ("labels", "sheet_checks"),
    ("labels", "residues_with_exactly_three_sheets"),
    ("alias", "levels"),
    ("alias", "levels_with_an_alias_large_edge"),
    ("loops", "levels"),
    ("loops", "loops"),
    ("loops", "total_loop_edge_mass"),
    ("clean_mass", "bridges"),
    ("clean_mass", "levels"),
    ("clean_mass", "runs"),
    ("clean_mass", "total_clean_mass"),
    ("clean_mass", "levels_where_the_bound_is_positive"),
    ("their_algebra", "high_lift_samples"),
    ("their_algebra", "alias_samples"),
    ("near_full", "rows_i_rebuilt"),
    ("examples", "examples"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "frontier_and_report_disagreeing"),
    ("constants", "duplicate_keys_carrying_the_same_value"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("population", "zero_lift"),
    ("population", "positive_lift"),
    ("population", "longest_tail"),
    ("source_budget", "bridges"),
    ("source_budget", "right_inequality_attained"),
    ("alias", "bridges"),
    ("alias", "largest_alias_count_seen"),
    ("loops", "bridges"),
    ("loops", "longest_loop_seen"),
    ("loops", "longest_erased_cycle_seen"),
    ("loops", "segment_longer_than_the_period"),
    ("loops", "segment_longer_than_its_erased_cycle"),
    ("loops", "certificate_trivially_zero"),
    ("clean_mass", "levels_where_the_bound_is_attained"),
    ("clean_mass", "smallest_mass_minus_bound_seen"),
    ("their_algebra", "alias_repair_fired"),
    ("their_algebra", "alias_would_have_failed_without_the_repair"),
    ("near_full", "rows_published"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
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
    ap.add_argument("--limit", type=int, default=200000)
    ap.add_argument("--max-steps", type=int, default=100)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    all_b = local_bridges(a.limit, a.max_steps)
    zero = [(y, X, Z, list(vals[1:]), w, lift_profile(w))
            for y, X, Z, vals, w in all_b
            if lift_profile(w)[len(w)] == 0]

    res: dict = {}
    errors: dict = {"%s_raised" % s: 0 for s in SECTIONS}
    errors["messages"] = []

    def run(name: str, fn):
        """A section that raises has no verdict -- RUN-046's lesson, kept."""
        try:
            res[name] = fn()
        except Exception as exc:                        # noqa: BLE001
            res[name] = {}
            errors["%s_raised" % name] = 1
            errors["messages"].append("%s: %s: %s"
                                      % (name, type(exc).__name__, exc))

    run("instrument", check_instrument)
    run("constants", lambda: check_constants(frontier, report))
    run("population", lambda: check_population(all_b, zero))
    run("locality", lambda: check_locality(zero))
    run("source_budget", lambda: check_source_budget(zero))
    run("labels", check_labels)
    run("alias", lambda: check_alias_budget(zero))
    run("loops", lambda: check_loops(zero))
    run("clean_mass", lambda: check_clean_mass(zero))
    run("their_algebra", check_their_algebra)
    run("near_full", lambda: check_near_full(report))
    run("examples", lambda: check_examples(report, zero))
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
        "run": "RUN-048", "round": "A-U.2d.20", "bundle": str(bundle),
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
