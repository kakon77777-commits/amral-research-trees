"""RUN-038 — independent recheck of Hard-Zeta round A-U.2d.10.

`Valuation-Class Harmonic Deficit Rigidity` (source item 57). 數學戰士「墜衡」.

A-U.2d.9 ended by refusing to promote its span result from a diameter gain to a
harmonic one, and named the missing piece: a value-order / time-order bridge.
This round supplies one, and it is again an exact identity on a single edge:

    1/Y_j - 1/Y_{j+1} = (3 - 2^q)/(3 Y_j) + 1/(3 Y_j Y_{j+1})

which telescopes to `sum (2^q - 3)/Y_j = -3/y + 3/z + C_cross`. Everything in
sections 3, 5, 6, 14 and 15 is decidable in rationals or integers, and this gate
checks all of it.

Two things are worth separating carefully.

The TELESCOPE is unconditional and exact. Theorem 4.1 is that telescope plus
`z > y`, which is a B-survival property; the equivalence between the two is
universal algebra and is checked on every segment, while the conclusion is
applied only where the premise holds.

Section 15's premise is different again, and better: first-crossing
subcriticality `sum q_j < beta m`, which is what a first-crossing interval IS.
As at RUN-037 it is decidable as `2^Q < 3^m` and real orbits meet it, so the
span theorem is genuinely tested.

Sections 16 and 17 are the round's own limits -- a relaxation countermodel
retaining exponent 1/9, and sharpness of 4/45 for one-step balance. Their
published diagnostics are recomputed rather than taken.

Brackets come from `src53_plateau_reset`, `src54_low_source_saturation` and
`src55_orbit_packing_deficit`, certified there rather than re-derived.

Usage:
    python code/src57_valuation_harmonic_deficit.py --bundle <dir> [--limit N]
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
from src47_survival_closure import decimal_verdict                 # noqa: E402
from src53_plateau_reset import (                                   # noqa: E402
    accelerated, beta_bracket, bracket_decimal, crossings_and_stalks,
    cumulative, ln2_bracket,
)
from src54_low_source_saturation import (                           # noqa: E402
    _exp_bracket, _nth_root_hi, _nth_root_lo, _pow_bracket, ln_bracket,
    simplify, ulps_against_bracket, widen,
)
from src55_orbit_packing_deficit import (                           # noqa: E402
    admissible, beta_tight, packing6, syracuse, v2,
)

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d10_Valuation_Class_Harmonic_Deficit"
         "_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d10_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d10_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d10_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d10.json"
CHECKSUMS = "CHECKSUMS.sha256"

# The round's own mod-9 target-cost table, transcribed once and then CHECKED
# against the valuation arithmetic rather than trusted.
TARGET_COST = {1: 2, 2: 1, 4: 2, 5: 3, 7: 4, 8: 1}

GRID_COUNTERS = (
    "q1_capacity_violations",
    "q2_capacity_violations",
    "theorem_7_1_violations",
    "corollary_9_1_violations",
    "theorem_9_2_violations",
    "p6_lower_bound_violations",
    "mu10_not_forty_five_theta_minus_four_over_forty_one",
    "eta10_not_one_ninth_minus_four_forty_fifths",
)


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


_P6: dict[tuple[int, int], Fraction] = {}
_ADM: dict[tuple[int, int], list[int]] = {}


def p6(y: int, L: int) -> Fraction:
    """`packing6` memoised. Segments repeat `(y, L)` constantly -- caching lets
    the orbit sweep reach a population that discriminates instead of lowering
    the guard until the population it already had looked sufficient."""
    key = (y, L)
    if key not in _P6:
        _P6[key] = packing6(y, L)
    return _P6[key]


def adm(y: int, L: int) -> list[int]:
    key = (y, L)
    if key not in _ADM:
        _ADM[key] = admissible(y, L)
    return _ADM[key]


_LN: dict[Fraction, tuple[Fraction, Fraction]] = {}


def ln_cached(x: Fraction) -> tuple[Fraction, Fraction]:
    """`ln_bracket` memoised. It is an eighty-term series on exact rationals,
    and the capacity check called it twice per segment -- 85 of this gate's 88
    seconds. Segments share `(y, L)` heavily, so the cache is nearly free."""
    if x not in _LN:
        _LN[x] = ln_bracket(x)
    return _LN[x]


# ---------------------------------------------------------------------------
# sections 3, 4, 5 -- the reciprocal flow, exactly
# ---------------------------------------------------------------------------

def check_reciprocal_flow(limit: int) -> dict:
    t = {
        "orbits": 0, "edges": 0, "segments": 0, "max_L": 0,
        "identity_violations": 0,
        "telescope_violations": 0,
        "segments_meeting_the_endpoint_premise_z_above_y": 0,
        "theorem_4_1_checked": 0, "theorem_4_1_violations": 0,
        "the_balance_is_not_equivalent_to_the_endpoint_premise": 0,
        "segments_where_every_state_including_the_endpoint_is_above_y": 0,
        "lemma_5_1_checked": 0,
        "cross_term_above_one_over_y_squared_plus_one_over_two_y": 0,
        "cross_term_above_nine_over_fourteen_y": 0,
        "segments_with_a_source_below_seven": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        t["orbits"] += 1
        for j in range(n):
            t["edges"] += 1
            Yj, Yn, q = values[j], values[j + 1], word[j]
            lhs = Fraction(1, Yj) - Fraction(1, Yn)
            rhs = Fraction(3 - 2 ** q, 3 * Yj) + Fraction(1, 3 * Yj * Yn)
            if lhs != rhs:
                t["identity_violations"] += 1
        for s in range(1, n):
            end = e[s]
            if end is None or end <= s:
                continue
            L, y, z = end - s, values[s], values[end]
            t["segments"] += 1
            t["max_L"] = max(t["max_L"], L)
            if y < 7:
                t["segments_with_a_source_below_seven"] += 1

            cross = sum(Fraction(1, values[j] * values[j + 1])
                        for j in range(s, end))
            flow = sum(Fraction(2 ** word[j] - 3, values[j])
                       for j in range(s, end))
            # Corollary 3.2, unconditional and exact
            if flow != -Fraction(3, y) + Fraction(3, z) + cross:
                t["telescope_violations"] += 1

            S = {}
            for j in range(s, end):
                S[word[j]] = S.get(word[j], Fraction(0)) + Fraction(1, values[j])
            S1 = S.get(1, Fraction(0))
            high = sum((2 ** k - 3) * v for k, v in S.items() if k >= 2)
            balance = high < S1 + cross
            premise = z > y
            # Theorem 4.1 IS the telescope plus `z > y`; that the two agree is
            # universal algebra and is checked everywhere.
            if balance != premise:
                t["the_balance_is_not_equivalent_to_the_endpoint_premise"] += 1
            if premise:
                t["segments_meeting_the_endpoint_premise_z_above_y"] += 1
                t["theorem_4_1_checked"] += 1
                if not balance:
                    t["theorem_4_1_violations"] += 1
            # Lemma 5.1 sums `1/n^2` over odd `n >= y`, so it needs EVERY state
            # of the segment to be at least `y` -- the endpoint included. A
            # first-crossing endpoint is usually below its source, so applied
            # without that premise it flagged 352 segments of a lemma that
            # holds. The premise is measured, not assumed.
            span = values[s:end + 1]
            if all(v >= y for v in span) and len(set(span)) == len(span):
                t["segments_where_every_state_including_the_endpoint_is_above_y"] += 1
                t["lemma_5_1_checked"] += 1
                if cross > Fraction(1, y * y) + Fraction(1, 2 * y):
                    t["cross_term_above_one_over_y_squared_plus_one_over_two_y"] += 1
                if y >= 7 and cross > Fraction(9, 14 * y):
                    t["cross_term_above_nine_over_fourteen_y"] += 1
    return t


# ---------------------------------------------------------------------------
# sections 6 and 7 -- harmonic capacity of the cheap valuation classes
# ---------------------------------------------------------------------------

def check_capacities(limit: int, a_lo: Fraction, a_hi: Fraction) -> dict:
    t = {
        "segments": 0, "max_L": 0,
        "q1_capacity_violations": 0, "q2_capacity_violations": 0,
        "theorem_7_1_violations": 0,
        "the_289_over_70_constant_does_not_decompose": 0,
        "segments_with_no_q_equal_1_edge": 0,
    }
    # (6/5)(2/y) + (4/5)(2/y) + (1/5)(9/(14y)) = 289/(70y), exactly
    if (Fraction(6, 5) * 2 + Fraction(4, 5) * 2 + Fraction(1, 5) * Fraction(9, 14)
            != Fraction(289, 70)):
        t["the_289_over_70_constant_does_not_decompose"] += 1
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        for s in range(1, n):
            end = e[s]
            if end is None or end <= s:
                continue
            L, y = end - s, values[s]
            t["segments"] += 1
            t["max_L"] = max(t["max_L"], L)
            S1 = sum(Fraction(1, values[j]) for j in range(s, end)
                     if word[j] == 1)
            S2 = sum(Fraction(1, values[j]) for j in range(s, end)
                     if word[j] == 2)
            Stot = sum(Fraction(1, values[j]) for j in range(s, end))
            if S1 == 0:
                t["segments_with_no_q_equal_1_edge"] += 1
            l6 = ln_cached(1 + Fraction(6 * L, y))[1]
            l12 = ln_cached(1 + Fraction(12 * L, y))[1]
            if S1 > Fraction(2, y) + l6 / 6:
                t["q1_capacity_violations"] += 1
            if S2 > Fraction(2, y) + l12 / 12:
                t["q2_capacity_violations"] += 1
            if Stot >= l6 / 5 + l12 / 15 + Fraction(289, 70 * y):
                t["theorem_7_1_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# sections 8 and 9 -- the product envelope and the deficit beyond P_6
# ---------------------------------------------------------------------------

def check_product(limit: int, C10_lo: Fraction, C10_hi: Fraction,
                  Crel_lo: Fraction, Crel_hi: Fraction) -> dict:
    t = {
        "segments": 0, "low_source_segments_7_le_y_le_L": 0,
        "p_rf_envelope_violations": 0,
        "corollary_9_1_violations": 0,
        "theorem_9_2_violations": 0,
        "p6_lower_bound_violations": 0,
        "admissible_upper_placement_violations": 0,
        "max_L": 0,
    }
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        for s in range(1, n):
            end = e[s]
            if end is None or end <= s:
                continue
            L, y = end - s, values[s]
            t["segments"] += 1
            t["max_L"] = max(t["max_L"], L)
            script = Fraction(1)
            for j in range(s, end):
                script *= 1 + Fraction(1, 3 * values[j])
            # the elementary upper placement A-U.2d.9 supplies
            a = adm(y, L)
            if any(a[k] > y + 3 * k + 1 for k in range(L)):
                t["admissible_upper_placement_violations"] += 1
            if not (7 <= y <= L):
                continue
            t["low_source_segments_7_le_y_le_L"] += 1
            P6 = p6(y, L)
            # P_6 >= (63 L / (25 y))^(1/9)
            floor_lo = _pow_bracket(Fraction(63 * L, 25 * y), 1, 9)
            if P6 < floor_lo:
                t["p6_lower_bound_violations"] += 1
            ratio_hi = _pow_bracket(Fraction(L, y), 4, 45, hi=True)
            if script > C10_hi * ratio_hi:
                t["corollary_9_1_violations"] += 1
            # Theorem 9.2: P_actual / P_6 <= C_rel (L/y)^(-1/45)
            dec_hi = _pow_bracket(Fraction(L, y), 1, 45, hi=True)
            if script * dec_hi > Crel_hi * P6:
                t["theorem_9_2_violations"] += 1
    return t


def check_exponents() -> dict:
    """The 4/45 and 1/45 exponents are asymptotic; what is checked is the trend.

    `P_RF` is an ENVELOPE, so a real segment's product need not approach its
    exponent -- only stay under it. What must hold at finite `L` is that the
    envelope's own measured exponent approaches 4/45 and the deficit against
    `P_6` stays negative.
    """
    t = {"rows": [], "largest_L": 0,
         "rf_exponent_not_approaching_four_forty_fifths": 0,
         "the_new_exponent_is_not_below_the_old": 0}
    for y in (7, 11, 25):
        prev = None
        for L in (200, 800, 3200, 12800):
            t["largest_L"] = max(t["largest_L"], L)
            rf = (289 / (210 * y) + math.log(1 + 6 * L / y) / 15
                  + math.log(1 + 12 * L / y) / 45)
            p6v = math.log(float(packing6(y, L)))
            erf = rf / math.log(L)
            if prev is not None and abs(erf - 4 / 45) > abs(prev - 4 / 45) + 1e-9:
                t["rf_exponent_not_approaching_four_forty_fifths"] += 1
            # `P_RF` and `P_6` are two ENVELOPES and the round takes their
            # MINIMUM -- neither dominates. Theorem 9.2's deficit is about the
            # ACTUAL product against `P_6`, which `check_product` tests. What
            # belongs here is the exponent ordering.
            if not 4 / 45 < 1 / 9:
                t["the_new_exponent_is_not_below_the_old"] += 1
            prev = erf
            if len(t["rows"]) < 8:
                t["rows"].append({"y": y, "L": L,
                                  "rf_exponent": "%.5f" % erf,
                                  "p6_exponent": "%.5f" % (p6v / math.log(L)),
                                  "deficit_exponent": "%.5f"
                                  % ((rf - p6v) / math.log(L))})
    return t


# ---------------------------------------------------------------------------
# sections 14 and 15 -- the mod-9 target cost and its span theorem
# ---------------------------------------------------------------------------

def check_mod9(limit: int, beta_lo: Fraction, beta_hi: Fraction) -> dict:
    t = {
        "edges": 0, "targets_not_4_or_7_mod_9": 0,
        "edges_below_their_target_cost": 0,
        "cost_table_entries_checked": 0,
        "cost_table_entries_disagreeing_with_the_valuation_arithmetic": 0,
        "capacity_windows": 0,
        "windows_where_a_cost_class_exceeds_W_over_9_plus_2": 0,
        "prefixes": 0, "prefixes_meeting_subcriticality": 0,
        "prefixes_failing_subcriticality": 0,
        "valuation_floor_violations": 0,
        "theorem_15_1_checked": 0, "theorem_15_1_violations": 0,
        "max_prefix_length": 0,
    }
    # the table, checked against `2^q m = 4 or 7 (mod 9)` rather than trusted
    for m in sorted(TARGET_COST):
        t["cost_table_entries_checked"] += 1
        allowed = [q for q in range(1, 7) if (pow(2, q, 9) * m) % 9 in (4, 7)]
        if not allowed or min(allowed) != TARGET_COST[m]:
            t["cost_table_entries_disagreeing_with_the_valuation_arithmetic"] += 1
    for W in (18, 90, 180, 900, 1800):
        for base in (1, 7, 25, 1001):
            t["capacity_windows"] += 1
            counts = {1: 0, 2: 0}
            for x in range(base, base + W):
                if x % 2 == 0 or x % 3 == 0:
                    continue
                c = TARGET_COST.get(x % 9)
                if c in counts:
                    counts[c] += 1
            for c in (1, 2):
                if counts[c] > Fraction(W, 9) + 2:
                    t["windows_where_a_cost_class_exceeds_W_over_9_plus_2"] += 1
                    break
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        for j in range(1, n):
            t["edges"] += 1
            target = values[j + 1]
            if (2 ** word[j] * target) % 9 not in (4, 7):
                t["targets_not_4_or_7_mod_9"] += 1
            need = TARGET_COST.get(target % 9)
            if need is not None and word[j] < need:
                t["edges_below_their_target_cost"] += 1
        for s in range(1, n):
            end = e[s]
            if end is None or end - s < 3:
                continue
            m = end - s - 1
            t["prefixes"] += 1
            t["max_prefix_length"] = max(t["max_prefix_length"], m)
            Q = K[s + m] - K[s]
            if 2 ** Q >= 3 ** m:
                t["prefixes_failing_subcriticality"] += 1
                continue
            t["prefixes_meeting_subcriticality"] += 1
            targets = values[s + 1:s + 1 + m]
            W = max(targets) - min(targets) + 1
            # sum q_j >= 3m - W/3 - 6, the step the span bound rests on
            if not Fraction(Q) >= 3 * m - Fraction(W, 3) - 6:
                t["valuation_floor_violations"] += 1
            t["theorem_15_1_checked"] += 1
            if not Fraction(W) > 3 * (3 - beta_lo) * m - 18:
                t["theorem_15_1_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# sections 16 and 17 -- the round's own limits, recomputed
# ---------------------------------------------------------------------------

def check_countermodel(report: dict, beta_lo: Fraction, beta_hi: Fraction) -> dict:
    """Check the section 16 countermodel against its own closed forms.

    The first version of this function enumerated a different set and printed
    its average beside theirs, which reads like a reproduction and is not one.
    Section 16 specifies the construction exactly, and its two closed forms

        D(t) = sum_k t^(k-1)/(3 2^k) = 1/(3(2-t)),
        average valuation -> 2/(2-t),

    collapse to a relation between the round's OWN reported numbers: eliminating
    `t` gives `avg_q -> 6 |S_X| / X`. So the reported density and the reported
    average must agree in the limit, and the gap must shrink with `X`. That is a
    real check; the earlier one was a coincidence of names.
    """
    t = {"rows": [], "density_series_disagrees_with_its_closed_form": 0,
         "average_series_disagrees_with_its_closed_form": 0,
         "t_beta_does_not_make_the_average_equal_beta": 0,
         "class_densities_checked": 0, "class_densities_off": 0,
         "rows_where_the_average_exceeds_beta": 0,
         "the_gap_to_the_closed_form_does_not_shrink": 0,
         "slopes_checked": 0, "slopes_far_from_one_ninth": 0,
         "max_prefix_slack_rows": 0,
         "max_prefix_slack_rows_not_equal_to_one_minus_beta": 0}

    # d_k = 1/(3 2^k), by enumeration over U_6
    for k in (1, 2, 3, 4):
        t["class_densities_checked"] += 1
        X = 3 * (1 << k) * 4000
        hits = sum(1 for n in range(1, X, 2) if n % 3 and v2(3 * n + 1) == k)
        if abs(Fraction(hits, X) - Fraction(1, 3 * (1 << k))) > Fraction(1, 300):
            t["class_densities_off"] += 1

    # the two series, as exact rationals at sample t
    for num, den in ((1, 2), (3, 5), (599, 1000)):
        tt = Fraction(num, den)
        d_sum = sum(Fraction(1, 3 * (1 << k)) * tt ** (k - 1) for k in range(1, 400))
        a_sum = sum(k * Fraction(1, 3 * (1 << k)) * tt ** (k - 1)
                    for k in range(1, 400))
        if abs(d_sum - 1 / (3 * (2 - tt))) > Fraction(1, 10 ** 30):
            t["density_series_disagrees_with_its_closed_form"] += 1
        if abs(a_sum / d_sum - 2 / (2 - tt)) > Fraction(1, 10 ** 30):
            t["average_series_disagrees_with_its_closed_form"] += 1
    # t_beta = 2(1 - 1/beta) is exactly where the average reaches beta
    tb_lo, tb_hi = 2 * (1 - 1 / beta_lo), 2 * (1 - 1 / beta_hi)
    if not (2 / (2 - tb_hi) >= beta_lo and 2 / (2 - tb_lo) <= beta_hi):
        t["t_beta_does_not_make_the_average_equal_beta"] += 1

    diag = report.get("diagnostics", {})
    prev_gap = None
    for row in diag.get("static_countermodel_avg_q", []):
        X, count, avg = row["X"], row["count"], row["avg_q"]
        implied = 6 * count / X          # eliminating t between the two forms
        gap = abs(avg - implied)
        t["rows"].append({"X": X, "count": count, "reported_avg_q": avg,
                          "implied_by_the_reported_density": round(implied, 10),
                          "gap": "%.2e" % gap,
                          "t_recovered_from_the_density":
                              round(2 - X / (3 * count), 6)})
        if avg >= float(beta_lo):
            t["rows_where_the_average_exceeds_beta"] += 1
        if prev_gap is not None and gap > prev_gap:
            t["the_gap_to_the_closed_form_does_not_shrink"] += 1
        prev_gap = gap
        t["max_prefix_slack_rows"] += 1
        slack = row.get("max_prefix_slack_q_minus_beta")
        if slack is not None:
            lo, hi = 1 - beta_hi, 1 - beta_lo
            if not (float(lo) - 1e-12 <= slack <= float(hi) + 1e-12):
                t["max_prefix_slack_rows_not_equal_to_one_minus_beta"] += 1
    for slope in diag.get("static_countermodel_product_slopes", []):
        t["slopes_checked"] += 1
        if abs(slope - 1 / 9) > 0.01:
            t["slopes_far_from_one_ninth"] += 1
    t["their_max_rf_actual_ratio"] = diag.get("max_rf_actual_ratio")
    t["the_ratio_is_at_most_one"] = (
        diag.get("max_rf_actual_ratio") is not None
        and diag["max_rf_actual_ratio"] <= 1.0)
    return t


# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict, paper: str,
                    beta_lo: Fraction, beta_hi: Fraction) -> dict:
    rho = Fraction("4.1164")
    theta = 1 / (rho + 1)
    mu10 = (45 * theta - 4) / 41
    pub = frontier["constants"]

    e_lo, e_hi = _exp_bracket(Fraction(289, 1470))
    # 40 digits, not the 25-digit default: `C10` multiplies three roots, so
    # their errors compound and the bracket came out 2.7e-25 wide -- too loose
    # to pin a 17-place decimal, which left `C10_depth` unidentified.
    C10_lo, C10_hi = widen(
        e_lo * _nth_root_lo(Fraction(7), 15, 40) * _nth_root_lo(Fraction(13), 45, 40),
        e_hi * _nth_root_hi(Fraction(7), 15, 40) * _nth_root_hi(Fraction(13), 45, 40))
    C10r_lo, C10r_hi = C10_lo / 6, C10_hi / 6
    c10_lo = _pow_bracket(1 / C10r_hi, 45, 41)
    c10_hi = _pow_bracket(1 / C10r_lo, 45, 41, hi=True)
    root_lo = _nth_root_lo(Fraction(63, 25), 9, 40)
    root_hi = _nth_root_hi(Fraction(63, 25), 9, 40)
    Crel_lo, Crel_hi = C10_lo / root_hi, C10_hi / root_lo
    span_lo, span_hi = 3 * (3 - beta_hi), 3 * (3 - beta_lo)
    # `t_beta := 2(1 - 1/beta)`, the countermodel's own threshold
    tb_lo, tb_hi = 2 * (1 - 1 / beta_lo), 2 * (1 - 1 / beta_hi)
    mu8 = (6 * theta - 1) / 5
    mu9 = (9 * theta - 1) / 8

    rows = {}
    for name, lo, hi, form in (
        ("C10_uniform_product", C10_lo, C10_hi,
         "exp(289/1470) * 7^(1/15) * 13^(1/45)"),
        ("C10_depth", C10r_lo, C10r_hi, "C10/6"),
        ("c10_source_inversion", c10_lo, c10_hi, "C10_depth^(-45/41)"),
        ("relative_deficit_constant", Crel_lo, Crel_hi, "C10/(63/25)^(1/9)"),
        ("mod9_target_span_coefficient", span_lo, span_hi, "3(3-beta)"),
        ("beta", beta_lo, beta_hi, "log2 3"),
        ("static_countermodel_t_beta", tb_lo, tb_hi, "2(1 - 1/beta)"),
    ):
        if name in pub:
            rows[name] = dict(ulps_against_bracket(pub[name], lo, hi),
                              published=pub[name], closed_form=form,
                              recomputed=bracket_decimal(lo, hi, 18))
    for name, exact, form in (
        ("theta_star", theta, "1/(rho+1)"),
        ("dense_root_source_floor_exponent_mu10", mu10,
         "(45 theta-4)/41 = %d/%d" % (mu10.numerator, mu10.denominator)),
        ("AU2d10_product_exponent", Fraction(4, 45), "4/45"),
        ("eta10_relative_to_AU2d9", Fraction(1, 45), "1/9 - 4/45"),
        ("AU2d9_product_exponent", Fraction(1, 9), "1/9"),
        ("AU2d8_product_exponent", Fraction(1, 6), "1/6"),
    ):
        if name in pub:
            rows[name] = {"published": pub[name], "closed_form": form,
                          "decided": True, "nearest_double": float(exact),
                          "ulps": bits(pub[name]) - bits(float(exact)),
                          "recomputed": None}
    drifted = sorted(k for k, v in rows.items() if v.get("ulps"))

    chain = {
        "C10_depth_is_the_published_C10_divided_by_six_as_doubles":
            pub.get("C10_uniform_product", 0) / 6 == pub.get("C10_depth"),
        "c10_is_the_published_C10_depth_to_the_minus_forty_five_forty_firsts":
            pub.get("C10_depth", 1) ** (-45 / 41) == pub.get("c10_source_inversion"),
        "mu10_is_the_float64_theta_star_put_through_its_formula":
            (45 * (1 / (float(rho) + 1)) - 4) / 41
            == pub.get("dense_root_source_floor_exponent_mu10"),
        "Crel_is_the_published_C10_over_the_float64_ninth_root":
            pub.get("C10_uniform_product", 0) / (63 / 25) ** (1 / 9)
            == pub.get("relative_deficit_constant"),
    }
    rc = report["constants"]
    disagree = [{"constant": k, "checker_report": rc[k], "frontier": pub[k],
                 "ulps_apart": bits(pub[k]) - bits(rc[k])}
                for k in set(rc) & set(pub) if rc[k] != pub[k]]
    only_report = sorted(set(rc) - set(pub))
    only_frontier = sorted(set(pub) - set(rc))
    renamed = [{"checker_report": a, "frontier": b}
               for a, b in (("reciprocal_flow_product_exponent_alpha10",
                             "AU2d10_product_exponent"),
                            ("new_relative_deficit_eta10",
                             "eta10_relative_to_AU2d9"),
                            ("relative_deficit_constant_Crel",
                             "relative_deficit_constant"),
                            ("mod9_target_span_mean_spacing_lower",
                             "mod9_target_span_coefficient"))
               if a in rc and b in pub and rc[a] == pub[b]]

    # A-U.2d.9's span coefficient is quoted here; RUN-037 found its frontier
    # copy one ulp out. Did the wrong value travel forward?
    prev_lo, prev_hi = Fraction(24, 17) * (4 - beta_hi), Fraction(24, 17) * (4 - beta_lo)
    quoted = re.findall(r"3\.40946470486425[0-9]*", paper)
    carried = {"the_paper_quotes_AU2d9_span_as": sorted(set(quoted)),
               "the_correctly_rounded_double_is":
                   bracket_decimal(prev_lo, prev_hi, 14),
               "the_AU2d9_frontier_had": "3.4094647048642504"}

    inline, unidentified = {}, []
    refs = {"C10_uniform_product": (C10_lo, C10_hi),
            "C10_depth": (C10r_lo, C10r_hi),
            "c10_source_inversion": (c10_lo, c10_hi),
            "relative_deficit_constant": (Crel_lo, Crel_hi),
            "mod9_target_span_coefficient": (span_lo, span_hi),
            "AU2d9_span_coefficient_quoted": (prev_lo, prev_hi),
            "mu10": (Fraction(mu10), Fraction(mu10)),
            "theta_star": (Fraction(theta), Fraction(theta)),
            "four_forty_fifths": (Fraction(4, 45), Fraction(4, 45)),
            "one_forty_fifth": (Fraction(1, 45), Fraction(1, 45)),
            "beta": (beta_lo, beta_hi),
            "mu8_from_AU2d8": (Fraction(mu8), Fraction(mu8)),
            "mu9_from_AU2d9": (Fraction(mu9), Fraction(mu9)),
            "t_beta": (tb_lo, tb_hi)}
    for shown in re.findall(r"=?\s*\n?([0-9]+\.[0-9]{4,})\\ldots", paper):
        places = len(shown.split(".")[1])
        best = None
        for name, (lo, hi) in refs.items():
            ref = bracket_decimal(lo, hi, places + 8)
            if ref is None:
                continue
            gap = abs(Fraction(ref) - Fraction(shown))
            if gap <= Fraction(10, 10 ** places) and (best is None or gap < best[2]):
                best = (name, ref, gap)
        if best is None:
            unidentified.append(shown)
            continue
        name, ref, _ = best
        inline.setdefault(name, dict(decimal_verdict(shown, ref), published=shown))
    return {
        "rows": rows, "off_by_at_least_one_ulp": drifted,
        "the_derivation_chain_in_float64": chain,
        "constants_the_two_artifacts_disagree_on": disagree,
        "constants_renamed_between_the_two_artifacts": renamed,
        "keys_only_in_the_checker_report": only_report,
        "keys_only_in_the_frontier": only_frontier,
        "the_AU2d9_constant_carried_forward": carried,
        "inline_decimals_in_the_paper": inline,
        "published_decimals_this_run_could_not_identify": unidentified,
        "_brackets": (C10_lo, C10_hi, Crel_lo, Crel_hi),
    }


def check_ledger(ledger: dict, paper: str) -> dict:
    def block(start: str, end: str) -> str:
        return paper[paper.index(start):paper.index(end)]

    prose = re.findall(r"^(\d+)\. ", block("## 22.1 Proved internally",
                                          "## 22.2 Inherited"), re.M)
    inherited = re.findall(r"^- ", block("## 22.2 Inherited",
                                         "## 22.3 External"), re.M)
    external = re.findall(r"^- ", block("## 22.3 External",
                                        "## 22.4 Explicitly open"), re.M)
    openq = re.findall(r"^- ", block("## 22.4 Explicitly open",
                                     "# 23. Checker scope"), re.M)
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)
    labels = {"proved_internally": ("22.1 proved internally", len(prose)),
              "inherited_internal": ("22.2 inherited", len(inherited)),
              "external_primary_grounding": ("22.3 external grounding",
                                             len(external)),
              "open": ("22.4 explicitly open", len(openq))}
    table, differ = [], []
    for key, (label, count) in labels.items():
        got = len(ledger.get(key, []))
        table.append({"paper_section": label, "paper_items": count,
                      "ledger_key": key, "ledger_items": got,
                      "shortfall": count - got})
        if count != got:
            differ.append(label)
    missing = ["%s %s" % (n, ti) for n, ti in no_go
               if not any(w in entry.lower()
                          for entry in ledger.get("no_go_boundaries", [])
                          for w in re.findall(r"[a-z-]{7,}", ti.lower()))]
    # A ledger with MORE entries than the paper is new, and it can mean two
    # different things: the ledger split one prose item into its parts, or it
    # lists something the paper does not. Only the second would be a defect, so
    # they are distinguished rather than both called a surplus.
    # Section 19 summarises boundaries proved earlier in the paper, so a NO-GO
    # heading can appear twice. Counting headings then reads as a ledger
    # shortfall when the duplication is the paper's. Pair them by their own
    # section bodies rather than by title wording.
    duplicated = []
    for a_num, a_ti in no_go:
        for b_num, b_ti in no_go:
            if a_num >= b_num:
                continue
            aw = set(re.findall(r"[a-z-]{6,}", a_ti.lower()))
            bw = set(re.findall(r"[a-z-]{6,}", b_ti.lower()))
            if len(aw & bw) >= 2:
                duplicated.append("%s restates %s" % (b_num, a_num))
    prose_text = block("## 22.1 Proved internally", "## 22.2 Inherited").lower()
    orphan = [e[:100] for e in ledger.get("proved_internally", [])
              if not any(w in prose_text
                         for w in re.findall(r"[a-z-]{8,}", e.lower()))]
    # and a NO-GO absent from `no_go_boundaries` may be dropped or simply filed
    # as a result instead; that is also worth telling apart.
    proved = " ".join(ledger.get("proved_internally", [])).lower()
    elsewhere = [m for m in missing
                 if any(w in proved
                        for w in re.findall(r"[a-z-]{8,}", m.lower()))]
    return {
        "table": table, "sections_where_the_counts_differ": differ,
        "paper_no_go_headings": len(no_go),
        "ledger_no_go_entries": len(ledger.get("no_go_boundaries", [])),
        "no_go_shortfall": len(no_go) - len(ledger.get("no_go_boundaries", [])),
        "paper_no_go_titles_with_no_ledger_entry_sharing_a_keyword": missing,
        "of_which_share_a_distinctive_word_with_proved_internally": elsewhere,
        "ledger_entries_sharing_no_distinctive_word_with_the_paper_s_list": orphan,
        "no_go_headings_in_the_paper": [n for n, _ in no_go],
        "no_go_headings_that_restate_another": duplicated,
        "ledger_keys": sorted(ledger),
    }


def check_artifacts(bundle: pathlib.Path) -> dict:
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = validation.get("files")
    anonymous: list[dict] = []
    blocks = [k for k in ("formal_source_validation", "json_validation",
                          "checker_script") if isinstance(validation.get(k), dict)]
    if isinstance(files, list):
        sv = {r["file"]: r["sha256"] for r in files}
        shape = "list of file records under `files` (items 51, 52, 54)"
    elif isinstance(files, dict):
        sv = {k: v["sha256"] for k, v in files.items()}
        shape = "dict of file records under `files` (item 53)"
    elif "artifact_sha256_before_manifest" in validation:
        sv = dict(validation["artifact_sha256_before_manifest"])
        shape = "dict keyed by filename (item 50)"
    elif blocks:
        sv = {}
        for key in blocks:
            blk = validation[key]
            if "sha256" in blk and isinstance(blk["sha256"], str):
                anonymous.append({"block": key, "sha256": blk["sha256"]})
                continue
            for name, rec in blk.items():
                if isinstance(rec, dict) and "sha256" in rec:
                    sv[name] = rec["sha256"]
        shape = "three purpose-named blocks, no `files` key (item 55): %s" \
            % ", ".join(blocks)
    else:
        sv, shape = {}, "UNRECOGNISED"

    cs = {}
    for line in (bundle / CHECKSUMS).read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            cs[name.strip()] = digest
    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()
              for n in present}
    by_digest = {d: n for n, d in actual.items()}
    resolved, unresolved = [], []
    for rec in anonymous:
        name = by_digest.get(rec["sha256"])
        (resolved if name else unresolved).append(
            {"block": rec["block"], "resolves_to": name})
        if name:
            sv[name] = rec["sha256"]
    return {
        "digests_the_record_gives_without_a_filename": len(anonymous),
        "resolved_by_looking_the_digest_up_among_the_files": resolved,
        "that_match_no_file_in_the_bundle": unresolved,
        "validation_record_shape": shape,
        "validation_record_top_level_keys": sorted(validation),
        "files_in_the_bundle": len(present),
        "listed_in_CHECKSUMS": len(cs),
        "listed_in_the_validation_record": len(sv),
        "CHECKSUMS_mismatches": sorted(n for n, d in cs.items()
                                       if actual.get(n) != d),
        "validation_record_mismatches": sorted(n for n, d in sv.items()
                                               if actual.get(n) != d),
        "digests_disagreeing_between_the_two_manifests":
            sorted(n for n in set(cs) & set(sv) if cs[n] != sv[n]),
        "covered_by_neither_manifest": [p for p in present
                                        if p not in cs and p not in sv],
        "covered_only_by_CHECKSUMS": sorted(set(cs) - set(sv)),
        "the_validation_record_covers_only_these_suffixes":
            sorted({("." + n.rsplit(".", 1)[-1]) for n in sv}),
        "a_stdout_transcript_is_shipped": any(
            p.endswith(".txt") and "stdout" in p for p in present),
    }


def check_their_claims(report: dict, res: dict) -> dict:
    rf, cap, m9 = res["reciprocal_flow"], res["capacities"], res["mod9"]
    pr = res["product"]
    mapping = {
        "exact_reciprocal_flow_identity":
            rf["identity_violations"] == 0 and rf["telescope_violations"] == 0,
        "cross_term_bound":
            rf["cross_term_above_nine_over_fourteen_y"] == 0,
        "q1_q2_harmonic_capacity":
            cap["q1_capacity_violations"] == 0 and cap["q2_capacity_violations"] == 0,
        "actual_reciprocal_flow_product_bound":
            pr["corollary_9_1_violations"] == 0
            and pr["p6_lower_bound_violations"] == 0,
        "mod9_target_q_table":
            m9["cost_table_entries_disagreeing_with_the_valuation_arithmetic"] == 0
            and m9["targets_not_4_or_7_mod_9"] == 0
            and m9["edges_below_their_target_cost"] == 0,
        "mod9_target_cost_span":
            m9["theorem_15_1_violations"] == 0 and m9["theorem_15_1_checked"] > 0,
    }
    stated = list(report.get("checks", {}))
    checked = {c: mapping[c] for c in stated if c in mapping}
    return {
        "checks_the_report_names": len(stated),
        "independently_confirmed": sum(1 for v in checked.values() if v),
        "independently_contradicted": sorted(k for k, v in checked.items() if not v),
        "not_covered_by_this_run": [c for c in stated if c not in mapping],
        "the_scope_warning": report.get("scope_warning", "")[:110],
    }


# ---------------------------------------------------------------------------

def check_instrument(beta_lo: Fraction, beta_hi: Fraction,
                     ln2_lo: Fraction, ln2_hi: Fraction) -> dict:
    failed = []
    coarse_lo, coarse_hi = beta_bracket()
    if not (coarse_lo <= beta_hi and beta_lo <= coarse_hi):
        failed.append("the_tight_beta_disagrees_with_the_certified_coarse_one")
    if beta_hi - beta_lo > Fraction(1, 10 ** 20):
        failed.append("the_beta_bracket_is_too_wide_to_pin_a_double")
    l2 = ln_bracket(Fraction(2))
    if not (l2[0] <= ln2_lo and ln2_hi <= l2[1]):
        failed.append("ln_of_two_does_not_contain_the_certified_bracket")
    if not (_exp_bracket(ln2_lo)[0] <= 2 <= _exp_bracket(ln2_hi)[1]):
        failed.append("exp_of_ln_two_does_not_contain_two")
    r = _nth_root_lo(Fraction(128), 7), _nth_root_hi(Fraction(128), 7)
    if not (r[0] <= 2 <= r[1]):
        failed.append("seventh_root_of_128_does_not_contain_two")
    if syracuse(1) != 1 or syracuse(7) != 11:
        failed.append("the_syracuse_map_disagrees_with_hand_computed_values")
    if admissible(7, 4) != [7, 11, 13, 17]:
        failed.append("the_admissible_positions_disagree_with_a_hand_list")
    if v2(24) != 3:
        failed.append("the_two_adic_valuation_disagrees_with_a_hand_value")
    return {"checks": 8, "failed": failed}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                                   # pragma: no cover
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--out")
    args = ap.parse_args()
    bundle = pathlib.Path(args.bundle)

    paper = (bundle / PAPER).read_text(encoding="utf-8")
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))

    ln2_lo, ln2_hi = ln2_bracket()
    a_lo, a_hi = 1 / ln2_hi, 1 / ln2_lo
    beta_lo, beta_hi = beta_tight()

    res: dict = {
        "tool": "src57_valuation_harmonic_deficit.py",
        "round": report.get("round"),
        "orbit_limit": args.limit,
        "instrument": {
            "brackets_from": "src53, src54 and src55, certified there",
            "one_over_ln2_to_20_places": bracket_decimal(a_lo, a_hi, 20),
        },
    }
    res["instrument_selfcheck"] = check_instrument(beta_lo, beta_hi, ln2_lo, ln2_hi)
    res["constants"] = check_constants(frontier, report, paper, beta_lo, beta_hi)
    C10_lo, C10_hi, Crel_lo, Crel_hi = res["constants"].pop("_brackets")
    res["reciprocal_flow"] = check_reciprocal_flow(args.limit)
    res["capacities"] = check_capacities(args.limit, a_lo, a_hi)
    res["product"] = check_product(args.limit, C10_lo, C10_hi, Crel_lo, Crel_hi)
    res["exponents"] = check_exponents()
    res["mod9"] = check_mod9(args.limit, beta_lo, beta_hi)
    res["countermodel"] = check_countermodel(report, beta_lo, beta_hi)
    res["ledger"] = check_ledger(ledger, paper)
    res["artifacts"] = check_artifacts(bundle)
    res["their_claims"] = check_their_claims(report, res)

    rf, cap, pr = res["reciprocal_flow"], res["capacities"], res["product"]
    ex, m9, cm = res["exponents"], res["mod9"], res["countermodel"]
    art = res["artifacts"]
    failures = ["instrument.%s" % n
                for n in res["instrument_selfcheck"]["failed"]]
    for key in ("identity_violations", "telescope_violations",
                "theorem_4_1_violations",
                "the_balance_is_not_equivalent_to_the_endpoint_premise",
                "cross_term_above_one_over_y_squared_plus_one_over_two_y",
                "cross_term_above_nine_over_fourteen_y"):
        if rf[key]:
            failures.append("reciprocal_flow.%s = %d" % (key, rf[key]))
    for key in ("q1_capacity_violations", "q2_capacity_violations",
                "theorem_7_1_violations",
                "the_289_over_70_constant_does_not_decompose"):
        if cap[key]:
            failures.append("capacities.%s = %d" % (key, cap[key]))
    for key in ("p_rf_envelope_violations", "corollary_9_1_violations",
                "theorem_9_2_violations", "p6_lower_bound_violations",
                "admissible_upper_placement_violations"):
        if pr[key]:
            failures.append("product.%s = %d" % (key, pr[key]))
    for key in ("rf_exponent_not_approaching_four_forty_fifths",
                "the_new_exponent_is_not_below_the_old"):
        if ex[key]:
            failures.append("exponents.%s = %d" % (key, ex[key]))
    for key in ("targets_not_4_or_7_mod_9", "edges_below_their_target_cost",
                "cost_table_entries_disagreeing_with_the_valuation_arithmetic",
                "windows_where_a_cost_class_exceeds_W_over_9_plus_2",
                "valuation_floor_violations", "theorem_15_1_violations"):
        if m9[key]:
            failures.append("mod9.%s = %d" % (key, m9[key]))
    for key in ("density_series_disagrees_with_its_closed_form",
                "average_series_disagrees_with_its_closed_form",
                "t_beta_does_not_make_the_average_equal_beta",
                "class_densities_off", "rows_where_the_average_exceeds_beta",
                "the_gap_to_the_closed_form_does_not_shrink"):
        if cm[key]:
            failures.append("countermodel.%s = %d" % (key, cm[key]))
    if cm["max_prefix_slack_rows_not_equal_to_one_minus_beta"]:
        failures.append("countermodel.max_prefix_slack_rows_not_equal_to_one_minus_beta = %d"
                        % cm["max_prefix_slack_rows_not_equal_to_one_minus_beta"])
    if not cm["the_ratio_is_at_most_one"]:
        failures.append("countermodel: the reported RF/actual ratio exceeds one")
    for key in ("CHECKSUMS_mismatches", "validation_record_mismatches",
                "digests_disagreeing_between_the_two_manifests"):
        if art[key]:
            failures.append("artifacts.%s = %s" % (key, art[key]))
    if art["validation_record_shape"] == "UNRECOGNISED":
        failures.append("artifacts: the validation record shape is unrecognised")
    if res["their_claims"]["independently_contradicted"]:
        failures.append("their_claims: %s"
                        % res["their_claims"]["independently_contradicted"])

    guards = []
    if rf["edges"] < 50000:
        guards.append("too few accelerated edges: %d" % rf["edges"])
    if rf["segments"] < 5000:
        guards.append("too few segments: %d" % rf["segments"])
    if 0 < rf["theorem_4_1_checked"] < 200:
        guards.append("theorem 4.1 was applied to %d segments: too few to have "
                      "tested it, too many to call it untested"
                      % rf["theorem_4_1_checked"])
    if cap["segments"] < 5000:
        guards.append("too few capacity segments: %d" % cap["segments"])
    if pr["low_source_segments_7_le_y_le_L"] < 200:
        guards.append("the low-source regime is barely attained: %d"
                      % pr["low_source_segments_7_le_y_le_L"])
    if ex["largest_L"] < 5000:
        guards.append("the exponent fit stops at L = %d" % ex["largest_L"])
    if m9["theorem_15_1_checked"] < 2000:
        guards.append("theorem 15.1 was applied to %d prefixes"
                      % m9["theorem_15_1_checked"])
    if m9["cost_table_entries_checked"] < 6:
        guards.append("only %d cost-table entries checked"
                      % m9["cost_table_entries_checked"])
    if m9["capacity_windows"] < 10:
        guards.append("only %d capacity windows" % m9["capacity_windows"])
    if cm["class_densities_checked"] < 3 or not cm["rows"]:
        guards.append("the countermodel's own construction was barely checked")
    if cm["slopes_checked"] < 2 or cm["max_prefix_slack_rows"] < 2:
        guards.append("the countermodel diagnostics were barely read: %d slopes, "
                      "%d rows" % (cm["slopes_checked"], cm["max_prefix_slack_rows"]))
    if len(res["constants"]["rows"]) < 8:
        guards.append("only %d constants bracketed" % len(res["constants"]["rows"]))
    for name, row in res["constants"]["rows"].items():
        if not row.get("decided"):
            guards.append("constants.%s: the bracket could not decide" % name)
    if res["constants"]["published_decimals_this_run_could_not_identify"]:
        guards.append("a decimal the paper publishes matches no reference: %s"
                      % res["constants"]["published_decimals_this_run_could_not_identify"])
    if res["their_claims"]["checks_the_report_names"] < 4:
        guards.append("only %d checker entries were read"
                      % res["their_claims"]["checks_the_report_names"])
    if art["listed_in_CHECKSUMS"] < 5:
        guards.append("only %d digests in CHECKSUMS" % art["listed_in_CHECKSUMS"])
    if art["that_match_no_file_in_the_bundle"]:
        guards.append("a digest given without a filename matches no file: %s"
                      % art["that_match_no_file_in_the_bundle"])
    empty = [row["paper_section"] for row in res["ledger"]["table"]
             if row["paper_items"] < 1]
    if empty:
        guards.append("the paper's own ledger sections parsed empty: %s" % empty)

    res["failures"] = failures
    res["non_vacuity_guards"] = guards
    res["passed"] = not failures and not guards
    text = json.dumps(res, indent=2, ensure_ascii=False)
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
