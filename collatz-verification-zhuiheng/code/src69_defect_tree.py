"""RUN-050 — independent recheck of Hard-Zeta round A-U.2d.22.

`Loop-Tree Defect Renormalization Rigidity` (source item 69). 數學戰士「墜衡」.

A-U.2d.21 left a semantic gap: an erased graph cycle need not be a contiguous
orbit interval, so the quotient-layer identity could not be applied to it. This
round closes the gap by changing the object. The general path defect

    d_M(P; r, s) := (B_P + 3^{L_P} r - 2^{Q_P} s) / M

is defined for arbitrary endpoints, its quotient-affine matrix
`[[3^L, d], [0, 2^Q]]` composes exactly, and chronological loop erasure --
retaining the CURRENT occurrence rather than the first -- produces a laminar
family of contiguous original-time return INTERVALS. The bare cycles were never
the right object.

Almost the whole round is exact integer arithmetic, and the shipped checker is
the strongest of this sweep: sixteen counters, none of them a synthetic block
that cannot fail. Four things this gate adds.

The composition test is checked for ORDER SENSITIVITY. RUN-049 found a
composition law tested only on inputs where its two coefficients swap into each
other; the matrix product here has the same hazard, so this gate verifies that
`R(R)R(P)` and `R(P)R(R)` actually differ on the tested population -- otherwise
"the product composes" would be blind to the order.

Two of the round's inequalities are guarded in float64 with a `1e-12` fudge.
Both are exact in integers: `m > Q + log2(M/Z0) - 1` is
`2^{m+1} Z0 > 2^Q M`, and `n > (2^{m-1} Z - M)/M` is `(n+1) M > 2^{m-1} Z`.
Both forms are computed and any disagreement is counted.

The sign law is stated with `beta L`, which the bundle evaluates in float64.
`Q <= beta L` is exactly `2^Q <= 3^L`, and the two routes are compared.

And the resonance claim carries `u >= 1`, which the bundle does not test.

Usage:
    python code/src69_defect_tree.py --bundle <dir> [--limit N]
"""

from __future__ import annotations

import argparse
from fractions import Fraction
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
from src65_lift_cocycle import lift_profile, local_bridges          # noqa: E402
from src67_return_loops import ord_two                              # noqa: E402
from src68_loop_defect import erase_cycles, split_runs              # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d22_Loop_Tree_Defect_Renormalization"
         "_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d22_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d22_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d22_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d22.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.22_AU2d22.md"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def v3(x: int) -> int | None:
    """`v_3(x)`, or None for zero -- a sentinel integer would sort into a
    minimum and silently win it."""
    if x == 0:
        return None
    x, a = abs(x), 0
    while x % 3 == 0:
        x //= 3
        a += 1
    return a


def path_defect(word: tuple[int, ...], r: int, s: int, m: int) -> int | None:
    """`d_M(P;r,s) = (B_P + 3^L r - 2^Q s)/M`, or None if it is not integral."""
    ell, q = len(word), sum(word)
    num = b_of(word) + 3 ** ell * r - (1 << q) * s
    return num // m if num % m == 0 else None


def matrix_of(word: tuple[int, ...], r: int, s: int, m: int):
    d = path_defect(word, r, s, m)
    return None if d is None else (3 ** len(word), d, 1 << sum(word))


def mat_comp(left, right):
    """The forward word is `left` then `right`, and the quotient matrix is
    `R(right) R(left)` -- the reversal is the point, not a typo."""
    a1, d1, e1 = left
    a2, d2, e2 = right
    return (a2 * a1, a2 * d1 + e1 * d2, e2 * e1)


def erasure_intervals(states: list[int], m: int):
    """Contiguous original-time return intervals from chronological erasure.

    The one line that makes this round work: on a repeat, the RETAINED
    occurrence is the current one (`stack_t[p] = i`), not the first. That is
    what makes a later parent interval contiguous and the family laminar --
    A-U.2d.21's bare cycles, which kept the first occurrence, were neither.
    """
    verts = [x % m for x in states]
    stack_v: list[int] = []
    stack_t: list[int] = []
    pos: dict[int, int] = {}
    out = []
    for i, v in enumerate(verts):
        if i == 0:
            stack_v, stack_t, pos = [v], [0], {v: 0}
            continue
        if v not in pos:
            stack_v.append(v)
            stack_t.append(i)
            pos[v] = len(stack_v) - 1
        else:
            p = pos[v]
            out.append((stack_t[p], i, v))
            for old in stack_v[p + 1:]:
                pos.pop(old, None)
            stack_v = stack_v[:p + 1]
            stack_t = stack_t[:p + 1]
            stack_t[p] = i
    return out


def erasure_intervals_retaining_first(states: list[int], m: int):
    """The same walker with A-U.2d.21's retention rule, for comparison only.

    Identical except that the retained time is NOT advanced to the current
    occurrence. Section 5's proof sketch derives contiguity and laminarity from
    the stack discipline; running both rules over the same orbits is what shows
    which conclusions actually depend on the update.
    """
    verts = [x % m for x in states]
    stack_v: list[int] = []
    stack_t: list[int] = []
    pos: dict[int, int] = {}
    out = []
    for i, v in enumerate(verts):
        if i == 0:
            stack_v, stack_t, pos = [v], [0], {v: 0}
            continue
        if v not in pos:
            stack_v.append(v)
            stack_t.append(i)
            pos[v] = len(stack_v) - 1
        else:
            p = pos[v]
            out.append((stack_t[p], i, v))
            for old in stack_v[p + 1:]:
                pos.pop(old, None)
            stack_v = stack_v[:p + 1]
            stack_t = stack_t[:p + 1]
    return out


def check_retention(bridges: list, depth: int = 5) -> dict:
    """What `stack_t[p] = i` is and is not responsible for.

    Both rules are run over the same orbits and scored on the three properties
    Theorem 5.1 claims. Whatever holds under both is not caused by the update.
    """
    t: dict = {"levels": 0, "levels_where_the_two_rules_differ": 0,
               "kept_intervals": 0, "kept_crossings": 0,
               "kept_non_contiguous": 0, "kept_misanchored": 0,
               "kept_nested_pairs": 0, "kept_shared_left_endpoint": 0,
               "kept_total_span": 0,
               "first_intervals": 0, "first_crossings": 0,
               "first_non_contiguous": 0, "first_misanchored": 0,
               "first_nested_pairs": 0, "first_shared_left_endpoint": 0,
               "first_total_span": 0,
               "reconstruction_failures_under_the_first_rule": 0}
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        for k in range(1, min(depth, h) + 1):
            t["levels"] += 1
            m = 3 ** k
            kept = erasure_intervals(states, m)
            first = erasure_intervals_retaining_first(states, m)
            if kept != first:
                t["levels_where_the_two_rules_differ"] += 1
            for tag, ints in (("kept", kept), ("first", first)):
                t["%s_intervals" % tag] += len(ints)
                for i, (a, b, r) in enumerate(ints):
                    t["%s_total_span" % tag] += b - a
                    if states[a] % m != r or states[b] % m != r:
                        t["%s_misanchored" % tag] += 1
                    if not a < b:
                        t["%s_non_contiguous" % tag] += 1
                    for c, d, _ in ints[i + 1:]:
                        if (a < c < b < d) or (c < a < d < b):
                            t["%s_crossings" % tag] += 1
                        elif (c <= a and b <= d) or (a <= c and d <= b):
                            t["%s_nested_pairs" % tag] += 1
                            if a == c:
                                t["%s_shared_left_endpoint" % tag] += 1
            children, root, _p = build_tree(first, h)
            memo: dict = {}
            got = node_matrix(root, first, children, root, states, w, m, memo)
            if got != matrix_of(w, states[0] % m, states[h] % m, m):
                t["reconstruction_failures_under_the_first_rule"] += 1
    return t


def build_tree(ints, h):
    n = len(ints)
    parent = [None] * n
    children: list[list[int]] = [[] for _ in range(n + 1)]
    root = n
    for i, (a, b, _r) in enumerate(ints):
        best, best_len = None, None
        for j, (c, d, _rr) in enumerate(ints):
            if j == i:
                continue
            if c <= a and b <= d and (c < a or b < d):
                if best is None or d - c < best_len:
                    best, best_len = j, d - c
        parent[i] = root if best is None else best
        children[parent[i]].append(i)
    for ch in children:
        ch.sort(key=lambda j: ints[j][0] if j < n else -1)
    return children, root, parent


def node_matrix(node, ints, children, root, states, word, m, memo):
    if node in memo:
        return memo[node]
    a, b = (0, len(word)) if node == root else ints[node][:2]
    cur, acc = a, None
    for ch in children[node]:
        ca, cb, _ = ints[ch]
        if cur < ca:
            mat = matrix_of(word[cur:ca], states[cur] % m, states[ca] % m, m)
            if mat is None:
                memo[node] = None
                return None
            acc = mat if acc is None else mat_comp(acc, mat)
        cmat = node_matrix(ch, ints, children, root, states, word, m, memo)
        if cmat is None:
            memo[node] = None
            return None
        acc = cmat if acc is None else mat_comp(acc, cmat)
        cur = cb
    if cur < b:
        mat = matrix_of(word[cur:b], states[cur] % m, states[b] % m, m)
        if mat is None:
            memo[node] = None
            return None
        acc = mat if acc is None else mat_comp(acc, mat)
    if acc is None:
        acc = (1, 0, 1)
    memo[node] = acc
    return acc


def zero_lift(limit: int, max_steps: int):
    out = []
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        ms = lift_profile(w)
        if ms[len(w)] != 0 or not w:
            continue
        out.append((y, X, Z, list(vals[1:]), w, ms))
    return out


def canonical_k(x: int, z: int) -> int:
    k, p = 1, 3
    while p <= max(x, z):
        k += 1
        p *= 3
    return k


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

    # v3 both ways: exact on powers of three, and None on zero rather than a
    # sentinel that would win a minimum
    bad = 0
    for a in range(0, 8):
        if v3(3 ** a) != a or v3(2 * 3 ** a) != a or v3(-(3 ** a)) != a:
            bad += 1
    want("v3 is exact on multiples of a power of three", bad == 0)
    want("v3 of zero is None, not a large integer", v3(0) is None)

    # the affine composition the whole matrix algebra rests on
    bad = 0
    for c, d in (((1, 2), (2, 1)), ((3,), (1, 1, 2)), ((2, 2, 1), (4,))):
        if b_of(c + d) != 3 ** len(d) * b_of(c) + (1 << sum(c)) * b_of(d):
            bad += 1
    want("B_{CD} = 3^{L_D} B_C + 2^{Q_C} B_D", bad == 0)

    # the matrix product must NOT commute, or "the product composes" would be
    # blind to the order -- RUN-049's lesson, applied before the fact
    u, v = (9, 5, 4), (27, 7, 8)
    want("the quotient-affine product does not commute",
         mat_comp(u, v) != mat_comp(v, u))
    want("the product is upper triangular with the right diagonal",
         mat_comp(u, v)[0] == u[0] * v[0] and mat_comp(u, v)[2] == u[2] * v[2])

    # the eraser: a hand case with a nested interval, so laminarity is
    # exercised rather than assumed empty
    got = erasure_intervals([1, 2, 4, 2, 1], 3)
    want("the eraser returns contiguous return intervals",
         all(a < b for a, b, _ in got))
    want("the eraser finds nothing when residues never repeat",
         erasure_intervals([1, 2], 9) == [])

    # the crossing test never fires on real data -- the stack truncation makes
    # a crossing unrepresentable -- so the predicate is exercised by hand here.
    # Without this, `crossing_pairs = 0` would be indistinguishable from a
    # broken test.
    def crosses(u, v):
        (a, b), (c, d) = u, v
        return (a < c < b < d) or (c < a < d < b)
    want("the crossing predicate fires on a crossing pair",
         crosses((0, 5), (3, 8)) and crosses((3, 8), (0, 5)))
    want("the crossing predicate is silent on nested and disjoint pairs",
         not crosses((0, 9), (3, 5)) and not crosses((0, 3), (5, 9))
         and not crosses((0, 5), (0, 9)))

    # the exact form of `Q <= beta L`
    bad = 0
    for ell in range(1, 40):
        for q in (ell, ell + 1, 2 * ell, 3 * ell):
            if ((1 << q) <= 3 ** ell) != (q <= ell * b_lo or
                                          (q <= ell * b_hi and
                                           (1 << q) <= 3 ** ell)):
                bad += 1
    want("2^Q <= 3^L decides Q <= beta L", bad == 0)
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
        ("faithful_loop_mass_constant", 2 - b_hi, 2 - b_lo, 2.0 - chain, 20,
         None),
    ]
    for name, lo, hi, ch, budget, rkey in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        rpt = rc.get(rkey) if rkey else None
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
# Theorems 3.2 and 4.1
# ---------------------------------------------------------------------------

def check_calculus(bridges: list, depth: int = 5) -> dict:
    """The quotient lift and the composition, on deterministic spans.

    Spans are enumerated rather than sampled, so the counts reproduce. The
    composition is also checked for ORDER SENSITIVITY: if the product happened
    to commute on this population, "the product composes" would be blind to the
    thing the theorem is about.
    """
    t: dict = {"bridges": 0, "levels": 0, "spans": 0, "compositions": 0,
               "defect_not_integral": 0,
               "quotient_lift_theorem_3_2_violations": 0,
               "composition_theorem_4_1_violations": 0,
               "matrix_form_disagreeing_with_the_defect_form": 0,
               "diagonal_not_multiplicative": 0,
               "compositions_where_the_two_orders_agree": 0,
               "order_sensitive_compositions": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        for k in range(1, min(depth, h) + 1):
            t["levels"] += 1
            m = 3 ** k
            # every span (a, b) with b - a in {1, 2, h}, deterministically
            spans = [(0, h)]
            spans += [(a, a + 1) for a in range(h)]
            spans += [(a, a + 2) for a in range(h - 1)]
            for a, b in spans:
                t["spans"] += 1
                r, s = states[a] % m, states[b] % m
                d = path_defect(w[a:b], r, s, m)
                if d is None:
                    t["defect_not_integral"] += 1
                    continue
                n, n2 = (states[a] - r) // m, (states[b] - s) // m
                ell, q = b - a, sum(w[a:b])
                if (1 << q) * n2 != 3 ** ell * n + d:
                    t["quotient_lift_theorem_3_2_violations"] += 1
            for a in range(h - 1):
                c, b = a + 1, min(a + 3, h)
                if b - c < 1:
                    continue
                t["compositions"] += 1
                r, s, u = states[a] % m, states[c] % m, states[b] % m
                left = matrix_of(w[a:c], r, s, m)
                right = matrix_of(w[c:b], s, u, m)
                whole = matrix_of(w[a:b], r, u, m)
                if None in (left, right, whole):
                    t["defect_not_integral"] += 1
                    continue
                comp = mat_comp(left, right)
                if comp != whole:
                    t["composition_theorem_4_1_violations"] += 1
                # the defect form, written out, must give the same middle entry
                if (3 ** (b - c) * left[1] + (1 << sum(w[a:c])) * right[1]
                        != whole[1]):
                    t["matrix_form_disagreeing_with_the_defect_form"] += 1
                if comp[0] != left[0] * right[0] or comp[2] != left[2] * right[2]:
                    t["diagonal_not_multiplicative"] += 1
                # order sensitivity
                if mat_comp(right, left) == comp:
                    t["compositions_where_the_two_orders_agree"] += 1
                else:
                    t["order_sensitive_compositions"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 5.1 and 6.1
# ---------------------------------------------------------------------------

def check_tree(bridges: list, depth: int = 5) -> dict:
    t: dict = {"bridges": 0, "levels": 0, "intervals": 0, "nodes": 0,
               "interval_endpoints_not_congruent": 0,
               "interval_not_contiguous": 0,
               "crossing_pairs": 0,
               "intervals_sharing_a_left_endpoint": 0,
               "nested_pairs": 0,
               "levels_with_a_nested_pair": 0,
               "tree_matrix_disagreeing_with_the_direct_one": 0,
               "node_span_defect_not_integral": 0,
               "node_matrix_disagreeing_with_its_span": 0,
               "root_matrix_disagreeing": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        for k in range(1, min(depth, h) + 1):
            t["levels"] += 1
            m = 3 ** k
            ints = erasure_intervals(states, m)
            nested_here = 0
            for i, (a, b, r) in enumerate(ints):
                t["intervals"] += 1
                if states[a] % m != r or states[b] % m != r:
                    t["interval_endpoints_not_congruent"] += 1
                if not a < b:
                    t["interval_not_contiguous"] += 1
                for c, d, _ in ints[i + 1:]:
                    if (a < c < b < d) or (c < a < d < b):
                        t["crossing_pairs"] += 1
                    elif (c <= a and b <= d) or (a <= c and d <= b):
                        t["nested_pairs"] += 1
                        # what `stack_t[p] = i` actually buys: siblings are
                        # disjoint, never a stack of prefixes off one point.
                        # Laminarity itself survives the other retention rule.
                        if a == c:
                            t["intervals_sharing_a_left_endpoint"] += 1
                        nested_here += 1
            if nested_here:
                t["levels_with_a_nested_pair"] += 1
            children, root, _parent = build_tree(ints, h)
            memo: dict = {}
            tree_mat = node_matrix(root, ints, children, root, states, w, m,
                                   memo)
            direct = matrix_of(w, states[0] % m, states[h] % m, m)
            if tree_mat is None or direct is None:
                t["node_span_defect_not_integral"] += 1
            elif tree_mat != direct:
                t["tree_matrix_disagreeing_with_the_direct_one"] += 1
                t["root_matrix_disagreeing"] += 1
            for node, mat in memo.items():
                if node == root:
                    continue
                t["nodes"] += 1
                if mat is None:
                    t["node_span_defect_not_integral"] += 1
                    continue
                a, b, _ = ints[node]
                if mat != matrix_of(w[a:b], states[a] % m, states[b] % m, m):
                    t["node_matrix_disagreeing_with_its_span"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 7.1, 7.2, 7.3 and 12.1
# ---------------------------------------------------------------------------

def check_root(bridges: list) -> dict:
    t: dict = {"bridges": 0, "partitions": 0, "cuts": 0,
               "root_defect_not_zero": 0,
               "canonical_modulus_not_above_both_endpoints": 0,
               "expansion_theorem_7_2_violations": 0,
               "expansion_block_not_integral": 0,
               "partitions_with_a_nonzero_block": 0,
               "ultrametric_minimum_not_paired": 0,
               "prefix_defect_not_the_coboundary": 0,
               "suffix_defect_not_the_coboundary": 0,
               "coboundary_sum_not_zero": 0}
    for y, X, Z, states, w, ms in bridges:
        t["bridges"] += 1
        h = len(w)
        k = canonical_k(X, Z)
        m = 3 ** k
        if not (m > X and m > Z and 3 ** (k - 1) <= max(X, Z)):
            t["canonical_modulus_not_above_both_endpoints"] += 1
        if path_defect(w, X, Z, m) != 0:
            t["root_defect_not_zero"] += 1
        # deterministic partitions rather than random ones
        for cuts in ({0, h, 1}, {0, h, h // 2}, {0, h, 1, h // 2, h - 1}):
            pts = sorted(x for x in cuts if 0 <= x <= h)
            if len(pts) < 2:
                continue
            t["partitions"] += 1
            terms, prefix_q = [], 0
            for j in range(len(pts) - 1):
                a, b = pts[j], pts[j + 1]
                sub = w[a:b]
                d = path_defect(sub, states[a] % m, states[b] % m, m)
                if d is None:
                    # a non-integral block is a finding, not a zero to drop in
                    t["expansion_block_not_integral"] += 1
                    d = 0
                terms.append(3 ** (h - b) * (1 << prefix_q) * d)
                prefix_q += sum(sub)
            if sum(terms) != 0:
                t["expansion_theorem_7_2_violations"] += 1
            nz = [v3(x) for x in terms if x != 0]
            if nz:
                t["partitions_with_a_nonzero_block"] += 1
                lo = min(nz)
                if sum(1 for x in nz if x == lo) < 2:
                    t["ultrametric_minimum_not_paired"] += 1
        for c in sorted({1, h // 2, max(1, h - 1)}):
            if not 0 < c < h:
                continue
            t["cuts"] += 1
            r = states[c] % m
            n = (states[c] - r) // m
            dp = path_defect(w[:c], X, r, m)
            ds = path_defect(w[c:], r, Z, m)
            qp, ls = sum(w[:c]), h - c
            if dp != (1 << qp) * n:
                t["prefix_defect_not_the_coboundary"] += 1
            if ds != -(3 ** ls) * n:
                t["suffix_defect_not_the_coboundary"] += 1
            if 3 ** ls * dp + (1 << qp) * ds != 0:
                t["coboundary_sum_not_zero"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorem 8.1
# ---------------------------------------------------------------------------

def check_depth(bridges: list, depth: int = 4, cap: int = 6) -> dict:
    """`v_3(d) >= a` iff the path lifts modulo `M 3^a`, in BOTH directions.

    The bundle caps the probe at `extra < 5`, so for a defect of high
    3-valuation the `extra > nu` half is never reached. That reach is counted
    here rather than left implicit.
    """
    t: dict = {"intervals": 0, "probes": 0,
               "depth_equivalence_violations": 0,
               "probes_at_or_below_the_valuation": 0,
               "probes_above_the_valuation": 0,
               "intervals_whose_upper_half_was_never_probed": 0,
               "intervals_the_bundle_cap_would_not_probe_above": 0,
               "largest_valuation_seen": 0}
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        for k in range(1, min(depth, h) + 1):
            m = 3 ** k
            for a, b, r in erasure_intervals(states, m):
                sub = w[a:b]
                d = path_defect(sub, r, r, m)
                if d is None or d == 0:
                    continue
                t["intervals"] += 1
                nu = v3(d)
                t["largest_valuation_seen"] = max(t["largest_valuation_seen"],
                                                  nu)
                ell, q = len(sub), sum(sub)
                # their loop is `range(0, min(nu+2, 5))`, so its largest probe
                # is `min(nu+1, 4)`; above `nu` only when `nu <= 3`
                if min(nu + 1, 4) <= nu:
                    t["intervals_the_bundle_cap_would_not_probe_above"] += 1
                reached_above = False
                for extra in range(0, min(nu + 2, cap)):
                    t["probes"] += 1
                    mod2 = m * 3 ** extra
                    lifts = (b_of(sub) + 3 ** ell * r - (1 << q) * r) % mod2 == 0
                    if lifts != (extra <= nu):
                        t["depth_equivalence_violations"] += 1
                    if extra <= nu:
                        t["probes_at_or_below_the_valuation"] += 1
                    else:
                        t["probes_above_the_valuation"] += 1
                        reached_above = True
                if not reached_above:
                    t["intervals_whose_upper_half_was_never_probed"] += 1
    return t


# ---------------------------------------------------------------------------
# Theorems 9.1, 10.1 and 11.1
# ---------------------------------------------------------------------------

def check_sign_and_resonance(bridges: list, depth: int = 5) -> dict:
    """The sign law in exact integers, and the resonance with `u >= 1`.

    `Q <= beta L` is exactly `2^Q <= 3^L`; the bundle evaluates `BETA*L` in
    float64. Both routes are computed and any disagreement is counted. The lift
    toll `m > Q + log2(M/Z0) - 1` is exactly `2^{m+1} Z0 > 2^Q M`, and the
    bundle guards it with a `1e-12` fudge; the two verdicts are compared.
    """
    t: dict = {"intervals": 0, "zero_defect_intervals": 0,
               "sign_law_violations": 0,
               "negative_defect_not_supercritical": 0,
               "float_sign_route_disagreeing_with_the_exact_one": 0,
               "zero_defect_not_supercritical": 0,
               "resonance_n_not_a_multiple": 0,
               "resonance_parameters_disagreeing": 0,
               "resonance_parameter_not_positive": 0,
               "smallest_resonance_parameter": None,
               "lift_toll_in_violations": 0,
               "lift_toll_out_violations": 0,
               "float_toll_route_disagreeing_with_the_exact_one": 0,
               "tolls_one_lift_bit_from_failing": 0,
               "smallest_toll_slack_bits": None,
               "tightest_toll_margin": None,
               "defects_that_are_negative": 0,
               "largest_absolute_defect_seen": 0}
    smallest_u = None
    slack: list = [None, None]
    beta_f = math.log2(3)
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        z0 = states[h]
        for k in range(1, min(depth, h) + 1):
            m = 3 ** k
            for a, b, r in erasure_intervals(states, m):
                sub = w[a:b]
                d = path_defect(sub, r, r, m)
                if d is None:
                    continue
                t["intervals"] += 1
                ell, q = len(sub), sum(sub)
                sub_critical = (1 << q) <= 3 ** ell          # Q <= beta L
                if sub_critical and not d > 0:
                    t["sign_law_violations"] += 1
                if d <= 0 and sub_critical:
                    t["negative_defect_not_supercritical"] += 1
                if sub_critical != (q <= beta_f * ell):
                    t["float_sign_route_disagreeing_with_the_exact_one"] += 1
                if d < 0:
                    t["defects_that_are_negative"] += 1
                t["largest_absolute_defect_seen"] = max(
                    t["largest_absolute_defect_seen"], abs(d))
                if d != 0:
                    continue
                t["zero_defect_intervals"] += 1
                if sub_critical:
                    t["zero_defect_not_supercritical"] += 1
                n = (states[a] - r) // m
                n2 = (states[b] - r) // m
                if n % (1 << q) or n2 % (3 ** ell):
                    t["resonance_n_not_a_multiple"] += 1
                    continue
                u1, u2 = n // (1 << q), n2 // (3 ** ell)
                if u1 != u2:
                    t["resonance_parameters_disagreeing"] += 1
                # the paper says u >= 1; the bundle does not test it
                if u1 < 1:
                    t["resonance_parameter_not_positive"] += 1
                if smallest_u is None or u1 < smallest_u:
                    smallest_u = u1
                m_in, m_out = ms[h - a], ms[h - b]
                # exact: 2^{m+1} Z0 > 2^Q M  and  2^{m+1} Z0 > 3^L M
                ok_in = (1 << (m_in + 1)) * z0 > (1 << q) * m
                ok_out = (1 << (m_out + 1)) * z0 > 3 ** ell * m
                if not ok_in:
                    t["lift_toll_in_violations"] += 1
                if not ok_out:
                    t["lift_toll_out_violations"] += 1
                f_in = m_in > q + math.log2(m / z0) - 1 - 1e-12
                f_out = m_out > beta_f * ell + math.log2(m / z0) - 1 - 1e-12
                if f_in != ok_in or f_out != ok_out:
                    t["float_toll_route_disagreeing_with_the_exact_one"] += 1
                # distance to the accident: would one fewer lift bit break it?
                if (not (1 << m_in) * z0 > (1 << q) * m
                        or not (1 << m_out) * z0 > 3 ** ell * m):
                    t["tolls_one_lift_bit_from_failing"] += 1
                # a bound that is never near failing is loose, not strong; the
                # margin is the honest report, not the zero above
                for lhs, rhs in (((1 << (m_in + 1)) * z0, (1 << q) * m),
                                 ((1 << (m_out + 1)) * z0, 3 ** ell * m)):
                    sl = lhs.bit_length() - rhs.bit_length()
                    if slack[0] is None or sl < slack[0]:
                        slack[0] = sl
                    rat = Fraction(lhs, rhs)
                    if slack[1] is None or rat < slack[1]:
                        slack[1] = rat
    t["smallest_resonance_parameter"] = smallest_u
    t["smallest_toll_slack_bits"] = slack[0]
    t["tightest_toll_margin"] = (None if slack[1] is None
                                 else round(float(slack[1]), 4))
    return t


# ---------------------------------------------------------------------------
# Theorem 13.1
# ---------------------------------------------------------------------------

def check_quotient_floor(bridges: list) -> dict:
    """`n_l >= (2^{m-1} Z - M)/M` in exact integers: `(n+1) M > 2^{m-1} Z`."""
    t: dict = {"positions": 0, "bridges": 0,
               "quotient_floor_violations": 0,
               "float_route_disagreeing_with_the_exact_one": 0,
               "positions_where_the_floor_is_positive": 0,
               "floors_within_a_factor_of_two_of_failing": 0,
               "smallest_floor_slack_bits": None,
               "tightest_floor_margin": None,
               "smallest_quotient_seen": None}
    small = None
    fslack: list = [None, None]
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        if h < 8:
            continue
        t["bridges"] += 1
        gamma, eta = 0.20, 0.45
        k = max(1, int(gamma * math.log2(h) / math.log2(3)))
        m = 3 ** k
        thr = (1 - eta) * math.log2(h)
        for ell in range(1, h):
            if ms[ell] < thr:
                continue
            t["positions"] += 1
            v = states[h - ell]
            r = v % m
            n = (v - r) // m
            lhs = (n + 1) * m
            rhs = (1 << (ms[ell] - 1)) * Z if ms[ell] >= 1 else 0
            if not lhs > rhs:
                t["quotient_floor_violations"] += 1
            if rhs > m:
                t["positions_where_the_floor_is_positive"] += 1
            # distance to the accident: does doubling the right side break it?
            if not lhs > 2 * rhs:
                t["floors_within_a_factor_of_two_of_failing"] += 1
            sl = lhs.bit_length() - rhs.bit_length()
            if fslack[0] is None or sl < fslack[0]:
                fslack[0] = sl
            rat = Fraction(lhs, rhs)
            if fslack[1] is None or rat < fslack[1]:
                fslack[1] = rat
            f = n > ((1 << (ms[ell] - 1)) * Z - m) / m - 1e-12
            if f != (lhs > rhs):
                t["float_route_disagreeing_with_the_exact_one"] += 1
            if small is None or n < small:
                small = n
    t["smallest_quotient_seen"] = small
    t["smallest_floor_slack_bits"] = fslack[0]
    t["tightest_floor_margin"] = (None if fslack[1] is None
                                  else round(float(fslack[1]), 4))
    return t


# ---------------------------------------------------------------------------
# Corollary 13.2 -- the only claim in the round with no counter behind it
# ---------------------------------------------------------------------------

def check_corollary_13_2(bridges: list) -> dict:
    """The faithful core and the polynomial floor, on the SAME vertices.

    The bundle's sixteen counters test Theorem 13.1 on all high-lift positions
    and inherit A-U.2d.21's mass bound separately. Corollary 13.2 conjoins
    them: the faithful core's RETAINED high-lift vertices are the ones claimed
    to sit on the floor. A conjunction is vacuous if its two sides never meet,
    so what is measured here is first whether that intersection is populated.

    The mass bound carries an `o(1)`, so a finite shortfall is not a failure --
    the ratio is reported, and only the floor half can fail.
    """
    t: dict = {"bridges": 0, "parameter_window_empty": 0,
               "retained_vertices": 0,
               "retained_high_lift_vertices": 0,
               "bridges_with_no_high_lift_retained_vertex": 0,
               "retained_high_lift_vertex_below_the_floor": 0,
               "levels_where_the_mass_ratio_is_below_the_constant": 0,
               "smallest_mass_ratio": None, "largest_mass_ratio": None,
               "bands": []}
    bands: dict = {}
    gamma, eta = 0.20, 0.45
    if not 0 < gamma < eta < 1 - gamma:
        t["parameter_window_empty"] = 1
        return t
    const = 2.0 - math.log2(3)
    lo = hi = None
    for y, X, Z, states, w, ms in bridges:
        h = len(w)
        if h < 8:
            continue
        t["bridges"] += 1
        k = max(1, int(gamma * math.log2(h) / math.log2(3)))
        m_low, s = 3 ** k, ord_two(k)
        thr = (1 - eta) * math.log2(h)
        bad = [q >= s for q in w]
        mass, retained = 0, set()
        for a, b in split_runs(w, bad):
            for _r, cyc, i0, i1, _c in erase_cycles(states[a:b + 1],
                                                    w[a:b], m_low):
                mass += len(cyc)
                retained.update(range(a + i0, a + i1 + 1))
        ratio = mass / h
        if lo is None or ratio < lo:
            lo = ratio
        if hi is None or ratio > hi:
            hi = ratio
        if ratio < const:
            t["levels_where_the_mass_ratio_is_below_the_constant"] += 1
        seen_high = False
        for idx in sorted(retained):
            ell = h - idx
            if not 1 <= ell < h:
                continue
            t["retained_vertices"] += 1
            if ms[ell] < thr:
                continue
            seen_high = True
            t["retained_high_lift_vertices"] += 1
            v = states[idx]
            r = v % m_low
            n = (v - r) // m_low
            if not (n + 1) * m_low > (1 << (ms[ell] - 1)) * Z:
                t["retained_high_lift_vertex_below_the_floor"] += 1
        if not seen_high:
            t["bridges_with_no_high_lift_retained_vertex"] += 1
        # an asymptotic claim is tested by its trend, so both deviations are
        # binned against bridge length rather than reported as one average
        row = bands.setdefault((h // 10) * 10, [0, 0.0, 0, 0])
        row[0] += 1
        row[1] += ratio
        row[2] += int(ratio < const)
        row[3] += int(not seen_high)
    t["bands"] = [
        {"h_from": b, "h_to": b + 9, "bridges": r[0],
         "mean_mass_ratio": round(r[1] / r[0], 4),
         "below_the_constant_pct": round(100.0 * r[2] / r[0], 1),
         "no_high_lift_retained_pct": round(100.0 * r[3] / r[0], 1)}
        for b, r in sorted(bands.items())]
    t["smallest_mass_ratio"] = None if lo is None else round(lo, 6)
    t["largest_mass_ratio"] = None if hi is None else round(hi, 6)
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"nonzero_nodes": 0, "zero_nodes": 0,
               "length_disagreeing": 0,
               "v3_disagreeing": 0, "defect_sign_wrong": 0,
               "zero_node_not_supercritical": 0,
               "zero_node_resonance_disagreeing": 0,
               "zero_node_defect_not_zero": 0,
               "zero_node_endpoints_not_congruent": 0,
               "zero_node_lift_identity_violations": 0,
               "rows": []}
    for ex in report.get("finite_nonzero_loop_nodes", []) or []:
        t["nonzero_nodes"] += 1
        a, b = ex["span"]
        if b - a != ex["length"]:
            t["length_disagreeing"] += 1
        if v3(ex["defect"]) != ex["v3_defect"]:
            t["v3_disagreeing"] += 1
        # the sign law applied to the published row
        if (1 << ex["Q"]) <= 3 ** ex["length"] and not ex["defect"] > 0:
            t["defect_sign_wrong"] += 1
        t["rows"].append({"M": ex["M"], "L": ex["length"], "Q": ex["Q"],
                          "r": ex["residue"], "defect": ex["defect"],
                          "v3": ex["v3_defect"]})
    for ex in report.get("finite_zero_defect_return_nodes", []) or []:
        t["zero_nodes"] += 1
        a, b = ex["span"]
        if b - a != ex["length"]:
            t["length_disagreeing"] += 1
        if ex["defect"] != 0:
            t["zero_node_defect_not_zero"] += 1
        if (1 << ex["Q"]) <= 3 ** ex["length"]:
            t["zero_node_not_supercritical"] += 1
        m, r = ex["M"], ex["residue"]
        if ex["start_state"] % m != r or ex["end_state"] % m != r:
            t["zero_node_endpoints_not_congruent"] += 1
        n = (ex["start_state"] - r) // m
        n2 = (ex["end_state"] - r) // m
        # a zero defect makes the quotient lift `2^Q n' = 3^L n` exactly;
        # recomputed from the published endpoints, not from their t
        if (1 << ex["Q"]) * n2 != 3 ** ex["length"] * n:
            t["zero_node_lift_identity_violations"] += 1
        if (n // (1 << ex["Q"]) != ex["quotient_parameter_t"]
                or n2 // (3 ** ex["length"]) != ex["quotient_parameter_t"]):
            t["zero_node_resonance_disagreeing"] += 1
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
    named = set(files) | set(val.get("json_parse", {}) or {})
    pc = val.get("python_compile")
    if isinstance(pc, dict) and "file" in pc:
        named.add(pc["file"])
    with_digest = set()
    for n, r in files.items():
        t["validation_per_file_entries"] += 1
        if isinstance(r, dict) and "sha256" in r:
            t["validation_entries_with_a_digest"] += 1
            with_digest.add(n)
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in named]
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_all_pass_flag"] = val.get("all_pass")
    t["validation_top_level_keys"] = sorted(val)
    t["validation_file_pass_flags_not_true"] = sum(
        1 for r in files.values()
        if isinstance(r, dict) and r.get("pass") is not True)
    t["validation_json_parse_not_true"] = sum(
        1 for r in (val.get("json_parse", {}) or {}).values()
        if isinstance(r, dict) and r.get("pass") is not True)
    t["validation_python_compile_not_true"] = int(
        isinstance(pc, dict) and pc.get("pass") is not True)
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
    proved = re.search(r"## 20\.1(.*?)## 20\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(
            re.findall(r"^\d+\. ", proved.group(1), re.M))
    openb = re.search(r"## 20\.4(.*?)(?:\n---|\Z)", paper, re.S)
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
    """Their counters beside mine, keyed on THEIR names.

    Five of their sixteen are drawn from a seeded RNG block, so no independent
    run can match the count. Those are not gaps: each is covered here by a
    deterministic enumeration, and the row names my counter and its size rather
    than leaving a blank that would read as "not reproduced".
    """
    tr, sr, rt = res["tree"], res["sign"], res["root"]
    ca, dp = res["calculus"], res["depth"]
    same = {
        "finite_local_bridges": res["population"]["bridges"],
        "zero_lift_bridges": res["population"]["zero_lift"],
        "contiguous_loop_tree_laminarity": tr["levels"],
        "tree_matrix_reconstruction": tr["levels"],
        "root_zero_defect_at_canonical_modulus": rt["bridges"],
        "prefix_suffix_coboundary": rt["cuts"],
        "return_defect_sign_law": sr["intervals"],
        "zero_defect_supercritical": sr["zero_defect_intervals"],
        "zero_defect_quotient_resonance": sr["zero_defect_intervals"],
        "zero_defect_lift_toll": sr["zero_defect_intervals"],
        "high_lift_quotient_floor": res["quotient_floor"]["positions"],
    }
    other = {
        "general_path_defect_integrality": ("calculus.spans", ca["spans"]),
        "general_defect_composition": ("calculus.compositions",
                                       ca["compositions"]),
        "weighted_defect_expansion": ("root.partitions", rt["partitions"]),
        "ultrametric_minimum_pairing": ("root.partitions_with_a_nonzero_block",
                                        rt["partitions_with_a_nonzero_block"]),
        "defect_extra_return_depth": ("depth.probes", dp["probes"]),
    }
    rows, exact, covered = [], 0, 0
    for k, v in report.get("checks", {}).items():
        if k in same:
            rows.append({"check": k, "theirs": v, "mine": same[k],
                         "basis": "same population"})
            exact += int(same[k] == v)
        elif k in other:
            nm, cnt = other[k]
            rows.append({"check": k, "theirs": v, "mine": cnt, "basis": nm})
            covered += 1
        else:
            rows.append({"check": k, "theirs": v, "mine": None,
                         "basis": "not covered"})
    return {"rows": rows,
            "checks_not_covered_at_all": sum(1 for r in rows
                                             if r["basis"] == "not covered"),
            "checks_covered_by_a_different_population": covered,
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "counts_i_reproduce_exactly": exact}


def check_population(all_b: list, zero_b: list) -> dict:
    return {"bridges": len(all_b), "zero_lift": len(zero_b),
            "positive_lift": len(all_b) - len(zero_b),
            "sources": len({r[0] for r in all_b}),
            "longest_tail": max((len(r[4]) for r in zero_b), default=0)}


SECTIONS = ("instrument", "constants", "population", "calculus", "tree",
            "root", "retention", "depth", "sign", "quotient_floor",
            "corollary",
            "examples",
            "artifacts", "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("calculus", "defect_not_integral"),
    ("calculus", "quotient_lift_theorem_3_2_violations"),
    ("calculus", "composition_theorem_4_1_violations"),
    ("calculus", "matrix_form_disagreeing_with_the_defect_form"),
    ("calculus", "diagonal_not_multiplicative"),
    ("tree", "interval_endpoints_not_congruent"),
    ("tree", "interval_not_contiguous"),
    ("tree", "crossing_pairs"),
    ("tree", "intervals_sharing_a_left_endpoint"),
    ("tree", "node_span_defect_not_integral"),
    ("retention", "kept_crossings"),
    ("retention", "kept_non_contiguous"),
    ("retention", "kept_misanchored"),
    ("retention", "kept_shared_left_endpoint"),
    ("tree", "tree_matrix_disagreeing_with_the_direct_one"),
    ("tree", "node_matrix_disagreeing_with_its_span"),
    ("root", "root_defect_not_zero"),
    ("root", "canonical_modulus_not_above_both_endpoints"),
    ("root", "expansion_theorem_7_2_violations"),
    ("root", "expansion_block_not_integral"),
    ("root", "ultrametric_minimum_not_paired"),
    ("root", "prefix_defect_not_the_coboundary"),
    ("root", "suffix_defect_not_the_coboundary"),
    ("root", "coboundary_sum_not_zero"),
    ("depth", "depth_equivalence_violations"),
    ("sign", "sign_law_violations"),
    ("sign", "negative_defect_not_supercritical"),
    ("sign", "float_sign_route_disagreeing_with_the_exact_one"),
    ("sign", "zero_defect_not_supercritical"),
    ("sign", "resonance_n_not_a_multiple"),
    ("sign", "resonance_parameters_disagreeing"),
    ("sign", "resonance_parameter_not_positive"),
    ("sign", "lift_toll_in_violations"),
    ("sign", "lift_toll_out_violations"),
    ("sign", "float_toll_route_disagreeing_with_the_exact_one"),
    ("quotient_floor", "quotient_floor_violations"),
    ("quotient_floor", "float_route_disagreeing_with_the_exact_one"),
    ("corollary", "parameter_window_empty"),
    ("corollary", "retained_high_lift_vertex_below_the_floor"),
    ("examples", "length_disagreeing"),
    ("examples", "v3_disagreeing"),
    ("examples", "defect_sign_wrong"),
    ("examples", "zero_node_not_supercritical"),
    ("examples", "zero_node_resonance_disagreeing"),
    ("examples", "zero_node_defect_not_zero"),
    ("examples", "zero_node_endpoints_not_congruent"),
    ("examples", "zero_node_lift_identity_violations"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_file_pass_flags_not_true"),
    ("artifacts", "validation_json_parse_not_true"),
    ("artifacts", "validation_python_compile_not_true"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("population", "bridges"),
    ("population", "sources"),
    ("calculus", "spans"),
    ("calculus", "compositions"),
    ("calculus", "order_sensitive_compositions"),
    ("tree", "levels"),
    ("tree", "intervals"),
    ("tree", "nodes"),
    ("tree", "nested_pairs"),
    ("tree", "levels_with_a_nested_pair"),
    ("root", "bridges"),
    ("root", "partitions"),
    ("root", "cuts"),
    ("root", "partitions_with_a_nonzero_block"),
    ("retention", "levels"),
    ("retention", "levels_where_the_two_rules_differ"),
    ("retention", "first_shared_left_endpoint"),
    ("depth", "intervals"),
    ("depth", "probes"),
    ("depth", "probes_at_or_below_the_valuation"),
    ("depth", "probes_above_the_valuation"),
    ("sign", "intervals"),
    ("sign", "zero_defect_intervals"),
    ("sign", "defects_that_are_negative"),
    ("quotient_floor", "positions"),
    ("quotient_floor", "positions_where_the_floor_is_positive"),
    ("corollary", "bridges"),
    ("corollary", "retained_vertices"),
    ("corollary", "retained_high_lift_vertices"),
    ("examples", "nonzero_nodes"),
    ("examples", "zero_nodes"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "frontier_and_report_disagreeing"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("population", "zero_lift"),
    ("population", "positive_lift"),
    ("population", "longest_tail"),
    ("calculus", "bridges"),
    ("calculus", "levels"),
    ("calculus", "compositions_where_the_two_orders_agree"),
    ("tree", "bridges"),
    ("tree", "root_matrix_disagreeing"),
    ("retention", "kept_intervals"),
    ("retention", "first_intervals"),
    ("retention", "kept_nested_pairs"),
    ("retention", "first_nested_pairs"),
    ("retention", "kept_total_span"),
    ("retention", "first_total_span"),
    ("retention", "first_crossings"),
    ("retention", "first_non_contiguous"),
    ("retention", "first_misanchored"),
    ("retention", "reconstruction_failures_under_the_first_rule"),
    ("depth", "largest_valuation_seen"),
    ("depth", "intervals_whose_upper_half_was_never_probed"),
    ("depth", "intervals_the_bundle_cap_would_not_probe_above"),
    ("sign", "largest_absolute_defect_seen"),
    ("sign", "smallest_resonance_parameter"),
    ("sign", "tolls_one_lift_bit_from_failing"),
    ("sign", "smallest_toll_slack_bits"),
    ("quotient_floor", "bridges"),
    ("quotient_floor", "floors_within_a_factor_of_two_of_failing"),
    ("quotient_floor", "smallest_floor_slack_bits"),
    ("quotient_floor", "smallest_quotient_seen"),
    ("corollary", "bridges_with_no_high_lift_retained_vertex"),
    ("corollary", "levels_where_the_mass_ratio_is_below_the_constant"),
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
    ("their_claims", "checks_not_covered_at_all"),
    ("their_claims", "checks_covered_by_a_different_population"),
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
    run("calculus", lambda: check_calculus(zero_b))
    run("tree", lambda: check_tree(zero_b))
    run("root", lambda: check_root(zero_b))
    run("retention", lambda: check_retention(zero_b))
    run("depth", lambda: check_depth(zero_b))
    run("sign", lambda: check_sign_and_resonance(zero_b))
    run("quotient_floor", lambda: check_quotient_floor(zero_b))
    run("corollary", lambda: check_corollary_13_2(zero_b))
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
        "run": "RUN-050", "round": "A-U.2d.22", "bundle": str(bundle),
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
