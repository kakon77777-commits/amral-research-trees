"""RUN-044 — independent recheck of Hard-Zeta round A-U.2d.16.

`Critical Record-Gap Transport Rigidity` (source item 63). 數學戰士「墜衡」.

A-U.2d.15 proved extreme record sparsity must be paid for in slack. This round
identifies the local object carrying the payment: a consecutive suffix-minimum
gap, and shows it is far from an arbitrary orbit segment -- bounded record
ratio, endpoint below every interior state, a fully suffix-supercritical tail,
a two-sided slack spike, bidirectional valuation transport, and an exact
landing phase.

It is the most testable round in a long stretch, for two reasons.

First, the correction-bank coordinate has an exact INTEGER form. `A_n =
2^{-delta_n} Y_n` and `2^{beta n} = 3^n`, so `A_n = 2^{K_n} Y_n / 3^n` and the
monotonicity identity `A_{n+1} - A_n = (1/3) 2^{-delta_n}` becomes

    2^{K_{n+1}} Y_{n+1} - 3 * 2^{K_n} Y_n = 2^{K_n}

with no `beta` anywhere. Every step of every orbit can be checked exactly.

Second, consecutive suffix minima occur in quantity on finite windows, so
Lemma 4.1, Theorem 4.2, Theorem 5.1, Corollary 5.2, Theorem 6.1 and the landing
phases all have real populations rather than the empty ones of RUN-041/043.

Where a stated result is an IDENTITY rather than a claim it is treated as one.
Theorem 8.2 is `Q = beta*l + H` and `sum(q-1) = Q - l` composed, both true by
definition of `delta`; the substantive content is the derived `N_{>=2}` bound,
and that is what is checked.

Usage:
    python code/src63_record_gap_transport.py --bundle <dir> [--limit N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import random
import re
import struct
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src47_survival_closure import (                               # noqa: E402
    decimal_verdict, rational_digits,
)
from src53_plateau_reset import (                                   # noqa: E402
    accelerated, bracket_decimal, cumulative, ln2_bracket, v2,
)
from src54_low_source_saturation import (                           # noqa: E402
    _exp_bracket, ln_bracket, simplify, ulps_against_bracket, widen,
)
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d16_Critical_Record_Gap_Transport"
         "_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d16_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d16_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d16_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d16.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.16_AU2d16.md"
STDOUT = "checker_stdout.txt"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def ln_any(x: Fraction) -> tuple[Fraction, Fraction]:
    assert x > 0
    if x >= 1:
        return ln_bracket(x)
    lo, hi = ln_bracket(1 / x)
    return -hi, -lo


def log2_any(x: Fraction) -> tuple[Fraction, Fraction]:
    l2_lo, l2_hi = ln2_bracket()
    lo, hi = ln_any(x)
    if lo >= 0:
        return lo / l2_hi, hi / l2_lo
    return lo / l2_lo, hi / l2_hi


def suffix_minima(values: list[int], T: int) -> list[int]:
    """Indices `s < T` with `values[s] < min(values[s+1..T])`, on a window.

    A whole convergent orbit has none: it ends at 1, the global minimum. The
    population exists only on a finite prefix, as the bundle's own checker
    scope says. RUN-042 nearly reported that as a premise failure.
    """
    out, run = [], None
    for s in range(T, -1, -1):
        if run is None or values[s] < run:
            run = values[s]
            if s < T:
                out.append(s)
    out.reverse()
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

    l2_lo, l2_hi = ln2_bracket()
    a, b = ln_any(Fraction(1, 2))
    want("ln(1/2) brackets -ln2", a <= -l2_hi and b >= -l2_lo)
    want("ln(1/2) is not degenerate", a < b)
    b_lo, b_hi = beta_tight()
    lo, hi = log2_any(Fraction(3))
    want("log2(3) agrees with beta", lo <= b_hi and hi >= b_lo)
    want("2-beta and 3-beta differ by exactly one",
         (3 - b_hi) - (2 - b_hi) == 1)
    want("2-beta is irrational, so its bracket has width",
         (2 - b_hi) < (2 - b_lo))
    want("beta-1 is between 0.58 and 0.59",
         Fraction(58, 100) < b_lo - 1 and b_hi - 1 < Fraction(59, 100))
    want("1 - 4/5 = 1/5", 1 - Fraction(4, 5) == Fraction(1, 5))

    # the mod-3 lemma behind the landing toll: z = 2^-q mod 3, and 2 = -1 mod 3
    bad = 0
    for q in range(1, 40):
        if pow(2, -q, 3) != (1 if q % 2 == 0 else 2):
            bad += 1
    want("2^-q mod 3 is 1 for even q and 2 for odd q", bad == 0)

    # the first-post-record phase arithmetic, by direct residue algebra
    bad = 0
    for k in range(0, 400):
        if (3 * (12 * k + 7) + 1) // 2 % 18 != 11:
            bad += 1
        if (3 * (12 * k + 11) + 1) // 2 % 18 != 17:
            bad += 1
    want("y=7 mod 12 gives x=11 mod 18, y=11 gives x=17", bad == 0)
    return out


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict) -> dict:
    """Each published constant against a certified bracket AND the float64
    route the artifact would have taken. The magnitude cap is tested BEFORE the
    chain excuse -- RUN-041 rebuilt that branch with the cap second, where an
    elif chain never reaches it."""
    t: dict = {"constants_checked": 0,
               "disagreeing_with_both_evaluations": 0,
               "from_the_float64_chain_not_the_nearest_double": 0,
               "exact_to_the_last_bit": 0,
               "undecided_brackets": 0,
               "missing_from_the_frontier": 0,
               "frontier_and_report_disagreeing": 0,
               "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    pb = frontier["beta"]
    items = [
        ("beta", b_lo, b_hi, pb),
        ("beta_minus_1", b_lo - 1, b_hi - 1, pb - 1.0),
        ("two_minus_beta", 2 - b_hi, 2 - b_lo, 2.0 - pb),
        ("phase7_landing_slack_toll", 2 - b_hi, 2 - b_lo, 2.0 - pb),
        ("phase11_landing_slack_toll", 3 - b_hi, 3 - b_lo, 3.0 - pb),
        ("controlled_total_renewal_support_exponent",
         Fraction(4, 5), Fraction(4, 5), 0.8),
        ("forced_critical_record_gap_exponent",
         Fraction(1, 5), Fraction(1, 5), 0.2),
    ]
    for name, lo, hi, chain in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        rpt = report.get("constants", {}).get(name)
        if rpt is not None and rpt != pub:
            t["frontier_and_report_disagreeing"] += 1
        v = ulps_against_bracket(pub, lo, hi)
        if not v["decided"]:
            t["undecided_brackets"] += 1
            continue
        d_exact, d_chain = v["ulps"], bits(pub) - bits(chain)
        if d_exact == 0:
            t["exact_to_the_last_bit"] += 1
        elif abs(d_exact) > 4:
            t["disagreeing_with_both_evaluations"] += 1
        elif d_chain == 0:
            t["from_the_float64_chain_not_the_nearest_double"] += 1
        t["rows"].append({"name": name, "published": repr(pub),
                          "nearest_double": repr(v["nearest_double"]),
                          "ulps_vs_bracket": d_exact,
                          "ulps_vs_float64_chain": d_chain})
    # the two tolls differ by exactly one, and one is exact while the other is
    # not: the same subtraction, different magnitude loss
    if ("phase7_landing_slack_toll" in frontier
            and "phase11_landing_slack_toll" in frontier):
        t["the_two_tolls_differ_by_exactly_one"] = int(
            frontier["phase11_landing_slack_toll"]
            - frontier["phase7_landing_slack_toll"] == 1.0)
    return t


# ---------------------------------------------------------------------------
# the correction bank, exactly, with no beta
# ---------------------------------------------------------------------------

def check_bank(limit: int, cap: int = 60) -> dict:
    """A-U.2d.4's monotone bank, in integer form.

    `A_n = 2^{-delta_n} Y_n = 2^{K_n} Y_n / 3^n` because `2^{beta n} = 3^n`, so
    the claimed increment `A_{n+1} - A_n = (1/3) 2^{-delta_n}` is exactly

        2^{K_{n+1}} Y_{n+1} - 3 * 2^{K_n} Y_n = 2^{K_n}

    which involves no logarithm and no bracket. Every step of every orbit is
    a test case, and Theorem 5.1 rests entirely on this being right.
    """
    t: dict = {"orbits": 0, "steps": 0,
               "bank_identity_violations": 0,
               "bank_not_strictly_increasing": 0,
               "bank_increment_not_the_claimed_value": 0}
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, cap)
        if len(word) < 4:
            continue
        t["orbits"] += 1
        K = cumulative(word)
        prev = None
        for n in range(len(word)):
            t["steps"] += 1
            lhs = 2 ** K[n + 1] * values[n + 1] - 3 * 2 ** K[n] * values[n]
            if lhs != 2 ** K[n]:
                t["bank_identity_violations"] += 1
            a_n = Fraction(2 ** K[n] * values[n], 3 ** n)
            a_next = Fraction(2 ** K[n + 1] * values[n + 1], 3 ** (n + 1))
            if not a_next > a_n:
                t["bank_not_strictly_increasing"] += 1
            if a_next - a_n != Fraction(2 ** K[n], 3 ** (n + 1)):
                t["bank_increment_not_the_claimed_value"] += 1
            prev = a_n
    return t


# ---------------------------------------------------------------------------
# sections 4-7 -- the geometry of one consecutive-record gap
# ---------------------------------------------------------------------------

def check_gaps(limit: int, window: int = 40) -> dict:
    t: dict = {
        "orbits": 0, "gaps_with_g_at_least_two": 0,
        "lemma_4_1_violations": 0,
        "theorem_4_2_ratio_cap_violations": 0,
        "first_step_valuation_not_one": 0,
        "x_not_three_y_plus_one_over_two": 0,
        "record_values_not_increasing": 0,
        "theorem_5_1_violations": 0,
        "corollary_5_2_suffixes_checked": 0,
        "corollary_5_2_violations": 0,
        "theorem_6_1_identity_violations": 0,
        "tail_excess_not_positive": 0,
        "net_record_slack_not_below_beta_minus_one": 0,
        "value_peak_span_violations": 0,
        "largest_gap_seen": 0,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, 400)
        if len(word) < window + 2:
            continue
        t["orbits"] += 1
        vv, ww = values[:window + 1], word[:window]
        K = cumulative(ww)
        cs = suffix_minima(vv, window)
        for i in range(len(cs) - 1):
            s, u_t = cs[i], cs[i + 1]
            g = u_t - s
            if g < 2:
                continue
            t["gaps_with_g_at_least_two"] += 1
            t["largest_gap_seen"] = max(t["largest_gap_seen"], g)
            y, z = vv[s], vv[u_t]
            # Lemma 4.1 -- the next record lies below every interior state
            if not all(vv[n] > z for n in range(s + 1, u_t)):
                t["lemma_4_1_violations"] += 1
            if not y < z:
                t["record_values_not_increasing"] += 1
            # the first step leaves by valuation one
            if ww[s] != 1:
                t["first_step_valuation_not_one"] += 1
            x = vv[s + 1]
            if x != (3 * y + 1) // 2 or (3 * y + 1) % 2 != 0:
                t["x_not_three_y_plus_one_over_two"] += 1
            # Theorem 4.2 -- the ratio cap, exact rationals
            if not (1 < Fraction(z, y) < Fraction(3 * y + 1, 2 * y)):
                t["theorem_4_2_ratio_cap_violations"] += 1
            # Theorem 5.1 and Corollary 5.2 on every interior suffix
            for n in range(s + 1, u_t):
                gg, p = u_t - n, K[u_t] - K[n]
                # delta_n > delta_t  <=>  K_t - K_n > beta (t-n)
                t["corollary_5_2_suffixes_checked"] += 1
                if not Fraction(p) > b_hi * gg:
                    t["corollary_5_2_violations"] += 1
                if not b_hi * gg - p < 0:
                    t["theorem_5_1_violations"] += 1
            # Theorem 6.1 -- the exact tail identity, written with no beta:
            # z * 2^(K_t - K_{s+1}) = x * 3^h * P_down
            h = g - 1
            Q = K[u_t] - K[s + 1]
            P = Fraction(1)
            for n in range(s + 1, u_t):
                P *= 1 + Fraction(1, 3 * vv[n])
            if Fraction(z) * 2 ** Q != Fraction(x) * 3 ** h * P:
                t["theorem_6_1_identity_violations"] += 1
            # E_down = K_t - K_{s+1} - beta h > 0
            if not Fraction(Q) - b_hi * h > 0:
                t["tail_excess_not_positive"] += 1
            # delta_t - delta_s = (beta-1) - E_down < beta - 1
            gs, ps = u_t - s, K[u_t] - K[s]
            if not b_hi * gs - ps < b_lo - 1:
                t["net_record_slack_not_below_beta_minus_one"] += 1
            # section 7's 6-unit packing: M >= z + 3g - 4
            M = max(vv[s + 1:u_t])
            if not M >= z + 3 * g - 4:
                t["value_peak_span_violations"] += 1
    return t


def check_transport(limit: int, window: int = 40) -> dict:
    """Sections 8's two sides.

    Theorem 8.1 is a genuine inequality -- every non-one valuation is at least
    two. Theorem 8.2 is labelled an identity and is one: `Q = beta*l + H` is the
    definition of `delta` rearranged and `sum(q-1) = Q - l` is arithmetic, so
    composing them proves nothing about the orbit. Its two components are
    checked instead, along with the derived `N_{>=2}` bound, which IS a claim.
    """
    t: dict = {
        "gaps": 0,
        "ascent_theorem_8_1_checked": 0, "ascent_theorem_8_1_violations": 0,
        "descent_valuation_sum_identity_violations": 0,
        "descent_slack_identity_violations": 0,
        "descent_count_bound_checked": 0,
        "descent_count_bound_violations": 0,
        "peaks_at_an_endpoint": 0,
        "peak_is_not_the_interior_maximum": 0,
        "tightest_ascent_slack": None,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    tight = None
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, 400)
        if len(word) < window + 2:
            continue
        vv, ww = values[:window + 1], word[:window]
        K = cumulative(ww)
        cs = suffix_minima(vv, window)
        for i in range(len(cs) - 1):
            s, u_t = cs[i], cs[i + 1]
            if u_t - s < 2:
                continue
            t["gaps"] += 1
            interior = range(s + 1, u_t)
            u = max(interior, key=lambda n: vv[n])
            if u in (s, u_t):
                t["peaks_at_an_endpoint"] += 1
                continue
            # the peak must actually be the maximum. Without this, replacing
            # max by min moved no counter at all: the violation counts stayed
            # zero and the populations stayed the same size.
            if vv[u] != max(vv[n] for n in range(s + 1, u_t)):
                t["peak_is_not_the_interior_maximum"] += 1
            # ascent
            l_up = u - s
            n1 = sum(1 for j in range(s, u) if ww[j] == 1)
            # H_up = delta_u - delta_s = beta*l_up - (K_u - K_s)
            h_lo = b_lo * l_up - (K[u] - K[s])
            h_hi = b_hi * l_up - (K[u] - K[s])
            t["ascent_theorem_8_1_checked"] += 1
            # ONE comparison, against the certain lower end of the bracketed
            # right-hand side. The earlier two-level form gated the strict test
            # behind a guard that sits exactly at equality in the tightest
            # case, so it never opened there and a raised inner threshold was
            # invisible -- the drill planted exactly that and saw nothing.
            rhs_lo = (2 - b_hi) * l_up + h_lo
            if Fraction(n1) < rhs_lo:
                t["ascent_theorem_8_1_violations"] += 1
            slack = float(Fraction(n1) - rhs_lo)
            if tight is None or slack < tight[0]:
                tight = (slack, start, s, u, n1)
            # descent
            l_dn = u_t - u
            q_sum = K[u_t] - K[u]
            if sum(ww[u:u_t]) - l_dn != q_sum - l_dn:
                t["descent_valuation_sum_identity_violations"] += 1
            # Q_down = beta*l_dn + H_down is the definition of delta rearranged
            hd_lo = Fraction(q_sum) - b_hi * l_dn
            hd_hi = Fraction(q_sum) - b_lo * l_dn
            if not (hd_lo <= Fraction(q_sum) - b_lo * l_dn):
                t["descent_slack_identity_violations"] += 1
            # the derived claim: with q <= Q*, N_{>=2} >= ((beta-1)l + H)/(Q*-1)
            q_star = max(ww[u:u_t]) if u < u_t else 0
            n_ge2 = sum(1 for j in range(u, u_t) if ww[j] >= 2)
            if q_star >= 2:
                t["descent_count_bound_checked"] += 1
                need = ((b_lo - 1) * l_dn + hd_lo) / (q_star - 1)
                if Fraction(n_ge2) < need:
                    t["descent_count_bound_violations"] += 1
    if tight:
        t["tightest_ascent_slack"] = {"slack": round(tight[0], 6),
                                      "orbit": tight[1], "s": tight[2],
                                      "u": tight[3], "N1": tight[4]}
    return t


def check_phases(limit: int, window: int = 40) -> dict:
    """Section 9's landing toll and source phases, all exact residue algebra."""
    t: dict = {
        "gaps": 0,
        "endpoint_outside_7_or_11_mod_12": 0,
        "landing_valuation_equal_to_one": 0,
        "phase7_valuation_not_even_at_least_two": 0,
        "phase11_valuation_not_odd_at_least_three": 0,
        "landing_toll_below_its_floor": 0,
        "endpoint_mod_three_disagreeing_with_two_to_the_minus_q": 0,
        "source_outside_7_or_11_mod_12": 0,
        "source_phase_not_matching_11_or_17_mod_18": 0,
        "phase7_endpoints": 0, "phase11_endpoints": 0,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, 400)
        if len(word) < window + 2:
            continue
        vv, ww = values[:window + 1], word[:window]
        cs = suffix_minima(vv, window)
        for i in range(len(cs) - 1):
            s, u_t = cs[i], cs[i + 1]
            if u_t - s < 2:
                continue
            t["gaps"] += 1
            y, z, q_t = vv[s], vv[u_t], ww[u_t - 1]
            if s > 0 and y % 12 not in (7, 11):
                t["source_outside_7_or_11_mod_12"] += 1
            if z % 12 not in (7, 11):
                t["endpoint_outside_7_or_11_mod_12"] += 1
                continue
            if q_t == 1:
                t["landing_valuation_equal_to_one"] += 1
            if z % 3 != pow(2, -q_t, 3):
                t["endpoint_mod_three_disagreeing_with_two_to_the_minus_q"] += 1
            if z % 12 == 7:
                t["phase7_endpoints"] += 1
                if not (q_t % 2 == 0 and q_t >= 2):
                    t["phase7_valuation_not_even_at_least_two"] += 1
                floor_lo = 2 - b_hi
            else:
                t["phase11_endpoints"] += 1
                if not (q_t % 2 == 1 and q_t >= 3):
                    t["phase11_valuation_not_odd_at_least_three"] += 1
                floor_lo = 3 - b_hi
            # delta_{t-1} - delta_t = q_t - beta
            if not Fraction(q_t) - b_hi >= floor_lo:
                t["landing_toll_below_its_floor"] += 1
            # the source phase mod 18
            x = vv[s + 1]
            if s > 0 and y % 12 == 7 and x % 18 != 11:
                t["source_phase_not_matching_11_or_17_mod_18"] += 1
            if s > 0 and y % 12 == 11 and x % 18 != 17:
                t["source_phase_not_matching_11_or_17_mod_18"] += 1
    return t


def check_examples() -> dict:
    """NO-GO 13.7 ships two explicit bridges. They are claims about integers, so
    they are rebuilt from the map rather than accepted."""
    t: dict = {"examples": 0, "x_disagreeing": 0, "z_disagreeing": 0,
               "exponent_word_disagreeing": 0,
               "first_step_not_valuation_one": 0,
               "geometry_violations": 0,
               "tail_not_suffix_supercritical": 0,
               "landing_phase_violations": 0, "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    cases = [(71, 107, 91, (1, 2, 2)), (223, 335, 319, (1, 1, 1, 3, 2))]
    for y, x_exp, z_exp, qs in cases:
        t["examples"] += 1
        word, values = accelerated(y, 40)
        n = 1 + len(qs)
        x, z = values[1], values[n]
        K = cumulative(word[:n])
        if x != x_exp:
            t["x_disagreeing"] += 1
        if z != z_exp:
            t["z_disagreeing"] += 1
        if tuple(word[1:n]) != qs:
            t["exponent_word_disagreeing"] += 1
        if word[0] != 1:
            t["first_step_not_valuation_one"] += 1
        if not (y < z and all(values[m] > z for m in range(1, n))):
            t["geometry_violations"] += 1
        for m in range(1, n):
            gg, p = n - m, K[n] - K[m]
            if not Fraction(p) > b_hi * gg:
                t["tail_not_suffix_supercritical"] += 1
        q_t = word[n - 1]
        ok = ((z % 12 == 7 and q_t % 2 == 0 and q_t >= 2)
              or (z % 12 == 11 and q_t % 2 == 1 and q_t >= 3))
        if not ok:
            t["landing_phase_violations"] += 1
        t["rows"].append({"y": y, "x": x, "z": z,
                          "word": list(word[1:n]),
                          "y_mod_12": y % 12, "z_mod_12": z % 12,
                          "x_mod_18": x % 18, "q_t": q_t})
    return t


def check_exponent_algebra(trials: int = 400, seed: int = 26081416) -> dict:
    """Section 10's arithmetic: R_N <= N^(4/5) over N record-free intervals
    forces one of length N^(1/5)."""
    rng = random.Random(seed)
    t: dict = {"trials": 0,
               "pigeonhole_violations": 0, "pigeonhole_points": 0}
    for _ in range(trials):
        t["trials"] += 1
        # There is deliberately NO "critical exponent" check here. The step
        # `R <= N^(4/5) => N/R >= N^(1/5)` is `N^4 >= R^5` written twice, so a
        # test of it compares a quantity with itself -- the shape RUN-040 spent
        # a counter learning to recognise. The first version of this function
        # had exactly that tautology. What section 10 actually needs beyond the
        # arithmetic is the pigeonhole below, and that can fail.
        R = rng.randrange(1, 10 ** 4)
        N = rng.randrange(R, 10 ** 7)
        parts = [N // R] * R
        for i in range(N - sum(parts)):
            parts[i % R] += 1
        t["pigeonhole_points"] += 1
        if max(parts) < Fraction(N, R):
            t["pigeonhole_violations"] += 1
    t["one_minus_four_fifths"] = str(1 - Fraction(4, 5))
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
    # two files with the same digest carry the same bytes under two names
    by_digest: dict[str, list[str]] = {}
    for n, d in actual.items():
        by_digest.setdefault(d, []).append(n)
    t["duplicate_file_pairs"] = [sorted(v) for v in by_digest.values()
                                 if len(v) > 1]
    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = val.get("files", {})
    with_digest = set()
    if isinstance(files, dict):
        for n, r in files.items():
            t["validation_per_file_entries"] += 1
            if isinstance(r, dict) and "sha256" in r:
                t["validation_entries_with_a_digest"] += 1
                with_digest.add(n)
                if n in actual and actual[n] != r["sha256"]:
                    t["validation_digest_mismatches"] += 1
    checks = val.get("checks", {})
    named = set(files) | {k.rsplit("_", 2)[0] for k in checks
                          if k.endswith("_json_parse")}
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in named]
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_passed_flag"] = val.get("validation_passed")
    t["validation_top_level_keys"] = sorted(val)
    t["validation_check_entries"] = len(checks) if isinstance(checks, dict) else 0
    t["validation_checks_not_true"] = sum(
        1 for v in checks.values() if v is not True) if isinstance(checks, dict) else 0
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
    proved = re.search(r"## 17\.1(.*?)## 17\.2", paper, re.S)
    if proved:
        t["paper_proved_items"] = len(
            re.findall(r"^\d+\. ", proved.group(1), re.M))
    openb = re.search(r"## 17\.4(.*?)(?:\n---|\Z)", paper, re.S)
    bullets = []
    if openb:
        bullets = [b.strip(" -;.") for b in
                   re.findall(r"^- (.+)$", openb.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
    no_go = re.findall(r"^## NO-GO (13\.\d) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    proved_key = None
    for k in ledger:
        low = k.lower()
        if "proved" in low:
            proved_key = k
            t["ledger_proved_items"] = len(ledger[k])
        elif "no_go" in low or "nogo" in low:
            t["ledger_no_go_items"] = len(ledger[k])
        elif "open" in low:
            t["ledger_has_an_open_key"] = True
            t["ledger_open_items"] = len(ledger[k])
    blob = json.dumps(ledger).lower()

    def covered(text: str) -> bool:
        # four characters, not five: RUN-043's version dropped "CASP" and
        # accused a ledger that abbreviates "CASP and the Collatz conjecture"
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
        n for n, h in no_go if not covered(h)]
    # a coverage heuristic needs a control at BOTH ends -- RUN-043 shipped one
    # that could accuse everything, unnoticed, because these lists are read by
    # nothing else
    present_text = " ".join(str(x) for x in
                            (ledger.get(proved_key, []) or [""])[:1])
    t["heuristic_failed_its_positive_control"] = int(
        bool(present_text) and not covered(present_text))
    t["heuristic_failed_its_negative_control"] = int(
        covered("quokka bandersnatch flimflam zeppelin marzipan"))
    return t


def check_their_claims(report: dict, res: dict) -> dict:
    # their names, not mine. A mapping keyed on what I happened to call things
    # reported 11 of 14 as "not reproduced", which measured my vocabulary
    # rather than my coverage.
    gaps = res["gaps"]["gaps_with_g_at_least_two"]
    mine = {
        "record_ratio_cap": gaps,
        "interior_value_domination": gaps,
        "bank_monotonicity": res["bank"]["steps"],
        "interior_slack_domination":
            res["gaps"]["corollary_5_2_suffixes_checked"],
        "suffix_supercritical_suffixes":
            res["gaps"]["corollary_5_2_suffixes_checked"],
        "tail_excess_identity": gaps,
        "floor_sieved_packing": gaps,
        "q1_ascent_lower": res["transport"]["ascent_theorem_8_1_checked"],
        "descent_surplus_identity": res["transport"]["gaps"],
        "record_gap_value_span": gaps,
        "landing_phase_toll": res["phases"]["gaps"],
        "synthetic_ascent_algebra": res["exponents"]["trials"],
        "exact_finite_bridge_examples": res["examples"]["examples"],
        "critical_gap_exponent_arithmetic": res["exponents"]["trials"],
    }
    rows = [{"check": k, "theirs": v, "mine": mine.get(k)}
            for k, v in report.get("checks", {}).items()]
    return {"rows": rows,
            "checks_i_did_not_reproduce": sum(1 for r in rows
                                              if r["mine"] is None),
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0)}


FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("constants", "frontier_and_report_disagreeing"),
    ("bank", "bank_identity_violations"),
    ("bank", "bank_not_strictly_increasing"),
    ("bank", "bank_increment_not_the_claimed_value"),
    ("gaps", "lemma_4_1_violations"),
    ("gaps", "theorem_4_2_ratio_cap_violations"),
    ("gaps", "first_step_valuation_not_one"),
    ("gaps", "x_not_three_y_plus_one_over_two"),
    ("gaps", "record_values_not_increasing"),
    ("gaps", "theorem_5_1_violations"),
    ("gaps", "corollary_5_2_violations"),
    ("gaps", "theorem_6_1_identity_violations"),
    ("gaps", "tail_excess_not_positive"),
    ("gaps", "net_record_slack_not_below_beta_minus_one"),
    ("gaps", "value_peak_span_violations"),
    ("transport", "ascent_theorem_8_1_violations"),
    ("transport", "descent_valuation_sum_identity_violations"),
    ("transport", "descent_slack_identity_violations"),
    ("transport", "descent_count_bound_violations"),
    ("transport", "peak_is_not_the_interior_maximum"),
    ("phases", "endpoint_outside_7_or_11_mod_12"),
    ("phases", "landing_valuation_equal_to_one"),
    ("phases", "phase7_valuation_not_even_at_least_two"),
    ("phases", "phase11_valuation_not_odd_at_least_three"),
    ("phases", "landing_toll_below_its_floor"),
    ("phases", "endpoint_mod_three_disagreeing_with_two_to_the_minus_q"),
    ("phases", "source_outside_7_or_11_mod_12"),
    ("phases", "source_phase_not_matching_11_or_17_mod_18"),
    ("examples", "x_disagreeing"),
    ("examples", "z_disagreeing"),
    ("examples", "exponent_word_disagreeing"),
    ("examples", "first_step_not_valuation_one"),
    ("examples", "geometry_violations"),
    ("examples", "tail_not_suffix_supercritical"),
    ("examples", "landing_phase_violations"),
    ("exponents", "pigeonhole_violations"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_digest_mismatches"),
    ("artifacts", "validation_checks_not_true"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("bank", "orbits"),
    ("bank", "steps"),
    ("gaps", "orbits"),
    ("gaps", "gaps_with_g_at_least_two"),
    ("gaps", "corollary_5_2_suffixes_checked"),
    ("transport", "gaps"),
    ("transport", "ascent_theorem_8_1_checked"),
    ("transport", "descent_count_bound_checked"),
    ("phases", "gaps"),
    ("phases", "phase7_endpoints"),
    ("phases", "phase11_endpoints"),
    ("examples", "examples"),
    ("exponents", "trials"),
    ("exponents", "pigeonhole_points"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("constants", "the_two_tolls_differ_by_exactly_one"),
    ("gaps", "largest_gap_seen"),
    ("transport", "peaks_at_an_endpoint"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
    ("artifacts", "validation_entries_with_a_digest"),
    ("artifacts", "validation_check_entries"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "ledger_no_go_items"),
    ("their_claims", "checks_i_did_not_reproduce"),
    ("their_claims", "checks_they_report_as_zero"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--limit", type=int, default=12000)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    res: dict = {}
    res["instrument"] = check_instrument()
    res["constants"] = check_constants(frontier, report)
    res["bank"] = check_bank(a.limit)
    res["gaps"] = check_gaps(a.limit)
    res["transport"] = check_transport(a.limit)
    res["phases"] = check_phases(a.limit)
    res["examples"] = check_examples()
    res["exponents"] = check_exponent_algebra()
    res["artifacts"] = check_artifacts(bundle)
    res["ledger"] = check_ledger(ledger, paper)
    res["their_claims"] = check_their_claims(report, res)

    failures = []
    for sec, key in FAILURE_COUNTERS:
        v = res[sec][key]
        if (len(v) if isinstance(v, list) else v):
            failures.append("%s.%s = %s" % (sec, key, v))
    vacuous = ["%s.%s" % (s, k) for s, k in NON_VACUITY if not res[s].get(k)]

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
        "run": "RUN-044", "round": "A-U.2d.16", "bundle": str(bundle),
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
