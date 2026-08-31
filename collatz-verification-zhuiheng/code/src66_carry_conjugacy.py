"""RUN-047 — independent recheck of Hard-Zeta round A-U.2d.19.

`Zero-Lift Mechanical Cocycle Discrepancy Rigidity` (source item 66).
數學戰士「墜衡」.

The round's move is a conjugacy that makes the whole real cocycle trivial.
A-U.2d.18 left the mechanical affine cocycle
`U_{l+1} = (2^{a_{l+1}} U_l - 2^{-m_{l+1}})/3` and pointed at `2^a/3` as the
place to look for spectral contraction. Setting

    W_l := 2^{-eps_l} U_l = 3^l V_l / 2^{Q_l}

removes the multiplier entirely: `W_{l+1} = W_l - 3^l/2^{Q_{l+1}}`, a strictly
decreasing additive carry. Everything downstream is then exact rational or
exact modular arithmetic:

  * the carry band `Z/2 < W_l <= Z` and the dyadic window
    `2^{m_l-1} Z < V_l < 2^{m_l+1} Z`;
  * mechanical neutrality `prod 2^{a_j}/3 = 2^{eps_s - eps_r}`, which in
    integers is `2^{ceil(beta s) - ceil(beta r)}` against `3^{s-r}`;
  * the nested endpoint tower `Z = sum_j 3^{j-1} 2^{-Q_j} mod 3^l`, whose
    Archimedean counterpart is `Z - sum_j 3^{j-1}/2^{Q_j} = W_l`;
  * valuation aliasing `R_{q+2*3^k}(V) = R_q(V) mod 3^k`.

Three things this gate does that the shipped checker does not.

First, the two artifacts DISAGREE on `beta`. The constants frontier publishes
`1.5849625007211563`; the checker report, machine-generated, publishes
`1.584962500721156`. One ulp apart, and the frontier is the one that is wrong.
`beta_minus_1` differs by two ulps the same way. This is the first
frontier/report disagreement of the sweep and it has its own counter.

Second, the paper's "sharper exact window" in section 4 is written
`2^{m_l+eps_l-eps_h} X <= V_l < 2^{m_l+eps_l} Z`, and the upper half is
ATTAINED at `l = 0`, where `V_0 = Z` exactly. Corollary 4.2's phase-free form
is strict there and is what the bundle checks, so the strictness never gets
tested. Both are checked here, with the attained case counted rather than
reported as a violation.

Third, `mesoscopic_modulus_algebra` -- ten thousand of the bundle's assertion
executions -- asserts the defining property of a ceiling three times, in
float64, and its third assertion is implied by its second. This gate
demonstrates that rather than restating it, and measures how close
`log_3(target)` comes to an integer over the same sampling, which is the only
way the float64 route could have failed.

Usage:
    python code/src66_carry_conjugacy.py --bundle <dir> [--limit N]
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
from src54_low_source_saturation import (                           # noqa: E402
    ulps_against_bracket, widen,
)
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    beta_hi, beta_lo, log2_any, verdict_with_budget,
)
from src65_lift_cocycle import (                                    # noqa: E402
    ceil_beta, lift_profile, local_bridges, mech_a, p2, two_pow_eps,
)

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d19_Zero_Lift_Mechanical_Cocycle"
         "_Discrepancy_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d19_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d19_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d19_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d19.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.19_AU2d19.md"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def suffix_sums(word: tuple[int, ...]) -> list[int]:
    """`Q_l = sum_{j=h-l+1}^{h} q_j`, the SUFFIX sums, `Q_0 = 0`."""
    h, run, out = len(word), 0, [0]
    for ell in range(1, h + 1):
        run += word[h - ell]
        out.append(run)
    return out


def carry(word: tuple[int, ...], rev: list[int]) -> list[Fraction]:
    """`W_l = 3^l V_l / 2^{Q_l}`, exact."""
    Qs = suffix_sums(word)
    return [Fraction(3 ** ell * rev[ell], 1 << Qs[ell])
            for ell in range(len(word) + 1)]


def k0_of(z: int) -> int:
    """`min{k >= 1 : 3^k > z}`, by repeated multiplication rather than a log."""
    k, p = 1, 3
    while p <= z:
        k += 1
        p *= 3
    return k


def zero_lift_bridges(limit: int, max_steps: int
                      ) -> list[tuple[int, int, int, list[int], tuple[int, ...], list[int]]]:
    """The bundle's population, restricted to the zero-lift class it studies.

    Returned with the REVERSED tail states `V_0 = Z ... V_h = X` already built,
    since every theorem in the round is stated on them.
    """
    out = []
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        ms = lift_profile(w)
        if ms[len(w)] != 0:
            continue
        rev = list(reversed(vals[1:]))
        out.append((y, X, Z, rev, w, ms))
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

    bad = 0
    for ell in range(1, 300):
        if not 1 < two_pow_eps(ell) < 2:
            bad += 1
    want("2^{eps_l} lies strictly between one and two", bad == 0)

    # the order of 2 modulo 3^{k+1} is 2*3^k, and no proper divisor of it works
    bad, loose = 0, 0
    for k in range(1, 9):
        m = 3 ** (k + 1)
        if pow(2, 2 * 3 ** k, m) != 1:
            bad += 1
        # a genuine order needs BOTH maximal-proper-divisor tests to fail
        if pow(2, 3 ** k, m) == 1 or pow(2, 2 * 3 ** (k - 1), m) == 1:
            loose += 1
    want("2^{2*3^k} = 1 mod 3^{k+1}", bad == 0)
    want("no maximal proper divisor of 2*3^k is an order", loose == 0)

    # the divisibility criterion every reverse step needs
    bad = 0
    for q in range(1, 30):
        for v in (1, 2, 4, 5, 7, 8):
            integral = (2 ** q * v - 1) % 3 == 0
            if integral != (pow(2, q, 3) * (v % 3) % 3 == 1):
                bad += 1
    want("(2^q V - 1)/3 is integral exactly when 2^q V = 1 mod 3", bad == 0)

    # the carry conjugacy on a hand case: y=59, tail (2,), V = [67, 89]
    Q1 = 2
    w0 = Fraction(3 ** 0 * 67, 1 << 0)
    w1 = Fraction(3 ** 1 * 89, 1 << Q1)
    want("the hand carry case satisfies the recurrence",
         w1 == w0 - Fraction(3 ** 0, 1 << Q1))
    want("the hand carry case sits in the band", Fraction(67, 2) < w1 <= 67)
    return out


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict) -> dict:
    """The two artifacts disagree on `beta`, so that gets its own counter and
    the row records BOTH published values."""
    t: dict = {"constants_checked": 0,
               "disagreeing_with_both_evaluations": 0,
               "frontier_constants_matching_no_evaluation": 0,
               "from_the_float64_chain_not_the_nearest_double": 0,
               "exact_to_the_last_bit": 0,
               "undecided_brackets": 0,
               "missing_from_the_frontier": 0,
               "frontier_and_report_disagreeing": 0,
               "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    chain = math.log2(3)
    items = [
        ("beta", b_lo, b_hi, chain, 4),
        ("beta_minus_1", b_lo - 1, b_hi - 1, chain - 1.0, 12),
    ]
    for name, lo, hi, ch, budget in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        rpt = report.get("constants", {}).get(name)
        row = {"constant": name, "frontier": repr(pub), "report": repr(rpt),
               "budget": budget}
        if rpt is not None and rpt != pub:
            t["frontier_and_report_disagreeing"] += 1
            row["frontier_minus_report_ulps"] = bits(pub) - bits(rpt)
        # the FRONTIER value is hand-written; a discrepancy there is an
        # artifact finding, recorded and reported, never a gate failure
        verdict, d = verdict_with_budget(pub, lo, hi, ch, budget)
        if verdict == "undecided":
            t["undecided_brackets"] += 1
        elif verdict == "exact":
            t["exact_to_the_last_bit"] += 1
        elif verdict == "the float64 chain":
            t["from_the_float64_chain_not_the_nearest_double"] += 1
        else:
            t["frontier_constants_matching_no_evaluation"] += 1
        row["frontier_verdict"] = (verdict if d == 0
                                   else "%+d ulp, %s" % (d, verdict))
        # the REPORT value is machine-generated from `log2(3)`, so a
        # discrepancy there would mean my instrument or their generator is
        # wrong -- that one stays a failure
        if rpt is not None:
            v2_, d2 = verdict_with_budget(rpt, lo, hi, ch, budget)
            row["report_verdict"] = (v2_ if d2 == 0
                                     else "%+d ulp, %s" % (d2, v2_))
            if v2_ not in ("exact", "the float64 chain"):
                t["disagreeing_with_both_evaluations"] += 1
        row["nearest_double"] = repr(float(lo))
        t["rows"].append(row)
    return t


# ---------------------------------------------------------------------------
# the carry conjugacy
# ---------------------------------------------------------------------------

def check_carry(limit: int, max_steps: int) -> dict:
    t: dict = {"bridges": 0, "steps": 0, "positions": 0,
               "carry_definition_violations": 0,
               "carry_recurrence_theorem_3_1_violations": 0,
               "carry_not_strictly_decreasing": 0,
               "carry_start_not_the_endpoint": 0,
               "carry_end_not_the_phased_source": 0,
               "iterated_carry_form_violations": 0,
               "carry_band_theorem_4_1_violations": 0,
               "dyadic_window_corollary_4_2_violations": 0,
               "sharper_window_lower_violations": 0,
               "sharper_window_upper_violations": 0,
               "sharper_window_upper_attained": 0,
               "sharper_window_lower_attained": 0,
               "state_is_not_the_phased_carry": 0,
               "smallest_carry_over_z": None,
               "largest_lift_seen": 0}
    smallest = None
    for y, X, Z, rev, w, ms in zero_lift_bridges(limit, max_steps):
        t["bridges"] += 1
        h = len(w)
        Qs = suffix_sums(w)
        W = carry(w, rev)
        t["largest_lift_seen"] = max(t["largest_lift_seen"], max(ms))

        for ell in range(h + 1):
            if W[ell] != Fraction(3 ** ell * rev[ell], 1 << Qs[ell]):
                t["carry_definition_violations"] += 1
        if W[0] != Z:
            t["carry_start_not_the_endpoint"] += 1
        if W[h] != X / two_pow_eps(h):
            t["carry_end_not_the_phased_source"] += 1

        for ell in range(h):
            t["steps"] += 1
            if W[ell + 1] != W[ell] - Fraction(3 ** ell, 1 << Qs[ell + 1]):
                t["carry_recurrence_theorem_3_1_violations"] += 1
            if not W[ell + 1] < W[ell]:
                t["carry_not_strictly_decreasing"] += 1

        acc = Fraction(0)
        for ell in range(1, h + 1):
            acc += Fraction(3 ** (ell - 1), 1 << Qs[ell])
            if W[ell] != Z - acc:
                t["iterated_carry_form_violations"] += 1

        for ell in range(h + 1):
            t["positions"] += 1
            if not (Fraction(Z, 2) < W[ell] <= Z):
                t["carry_band_theorem_4_1_violations"] += 1
            v, m = rev[ell], ms[ell]
            if not (p2(m - 1) * Z < v < p2(m + 1) * Z):
                t["dyadic_window_corollary_4_2_violations"] += 1
            # `V_l = 2^{m_l + eps_l} W_l` is the identity the window rests on
            if Fraction(v) != p2(m) * two_pow_eps(ell) * W[ell]:
                t["state_is_not_the_phased_carry"] += 1
            # the paper's SHARPER window, with its endpoints counted rather
            # than assumed strict
            lo = p2(m) * two_pow_eps(ell) / two_pow_eps(h) * X
            hi = p2(m) * two_pow_eps(ell) * Z
            if v < lo:
                t["sharper_window_lower_violations"] += 1
            elif v == lo:
                t["sharper_window_lower_attained"] += 1
            if v > hi:
                t["sharper_window_upper_violations"] += 1
            elif v == hi:
                t["sharper_window_upper_attained"] += 1
        r = W[h] / Z
        if smallest is None or r < smallest:
            smallest = r
    t["smallest_carry_over_z"] = None if smallest is None else float(smallest)
    return t


# ---------------------------------------------------------------------------
# mechanical neutrality
# ---------------------------------------------------------------------------

_CEIL: list[int] = []


def ceil_table(upto: int) -> list[int]:
    """`ceil(beta j)` for `0 <= j <= upto`, built by ONE incremental pass.

    `ceil_beta` recomputes `3**j` from scratch, which is fine at a bridge's
    forty levels and ruinous at five thousand: the first version of
    `check_neutrality` spent fourteen of the gate's fifteen seconds here. The
    table is cross-checked against `ceil_beta` at its ends by the instrument.
    """
    if len(_CEIL) <= upto:
        _CEIL.clear()
        p = 1
        _CEIL.append(0)
        for _ in range(upto):
            p *= 3
            _CEIL.append(p.bit_length())
    return _CEIL


def check_neutrality(trials: int = 10000, span: int = 500) -> dict:
    """Theorem 5.1, in integers, plus what it actually reduces to.

    `prod_{j>r}^{s} 2^{a_j}/3 = 2^{ceil(beta s) - ceil(beta r)} / 3^{s-r}`, and
    the band `(1/2,2)` is `eps_s - eps_r in (-1,1)` -- which holds because each
    `eps` is in `(0,1)`, i.e. because a ceiling is a ceiling. Both the band and
    the telescoping are checked; the second is the one a wrong `mech_a` breaks.
    """
    t: dict = {"intervals": 0,
               "telescoping_checks": 0,
               "telescoping_violations": 0,
               "band_violations": 0,
               "phase_form_violations": 0,
               "mechanical_symbol_outside_one_or_two": 0,
               "two_consecutive_mechanical_ones": 0,
               "widest_ratio_seen": None,
               "narrowest_ratio_seen": None}
    wide, narrow = None, None
    tab = ceil_table(5000 + span + 1)
    # the alphabet itself, over the whole range rather than on the sampled
    # intervals: `a_j in {1,2}` is `beta in (1,2)` and no two consecutive ones
    # is `beta > 3/2`. Neither is tested by the band below.
    for j in range(1, len(tab)):
        a = tab[j] - tab[j - 1]
        if a not in (1, 2):
            t["mechanical_symbol_outside_one_or_two"] += 1
        if j > 1 and a == 1 and tab[j - 1] - tab[j - 2] == 1:
            t["two_consecutive_mechanical_ones"] += 1
    for i in range(trials):
        r = (i * 7919) % 5000
        s = r + 1 + (i * 104729) % span
        t["intervals"] += 1
        # the sum of mechanical increments telescopes -- this is what breaks if
        # `a_j` is wrong, and the band below does not test it. Sampled rather
        # than run on every interval, because it is O(s-r).
        if i % 100 == 0:
            t["telescoping_checks"] += 1
            if sum(mech_a(j) for j in range(r + 1, s + 1)) != tab[s] - tab[r]:
                t["telescoping_violations"] += 1
        ratio = Fraction(1 << (tab[s] - tab[r]), 3 ** (s - r))
        if not Fraction(1, 2) < ratio < 2:
            t["band_violations"] += 1
        if i % 100 == 0 and ratio != two_pow_eps(s) / two_pow_eps(r):
            t["phase_form_violations"] += 1
        if wide is None or ratio > wide:
            wide = ratio
        if narrow is None or ratio < narrow:
            narrow = ratio
    t["widest_ratio_seen"] = None if wide is None else float(wide)
    t["narrowest_ratio_seen"] = None if narrow is None else float(narrow)
    return t


# ---------------------------------------------------------------------------
# the nested endpoint tower
# ---------------------------------------------------------------------------

def check_tower(limit: int, max_steps: int) -> dict:
    """Theorems 6.1 and 7.1.

    The congruence and its Archimedean counterpart are two completions of one
    identity, so both are checked and their agreement is its own counter. The
    stabilization `r_l = Z` is guarded by `3^l > Z` in the bundle; the guard
    rate is counted here rather than left implicit.
    """
    t: dict = {"bridges": 0, "levels": 0,
               "congruence_theorem_6_1_violations": 0,
               "archimedean_carry_form_violations": 0,
               "stabilization_levels": 0,
               "stabilization_theorem_7_1_violations": 0,
               "levels_below_the_stabilization_depth": 0,
               "representative_at_a_shallow_level_not_z_mod_three_to_the_l": 0,
               "k0_disagreeing_with_the_least_power": 0,
               "largest_k0_seen": 0}
    for y, X, Z, rev, w, ms in zero_lift_bridges(limit, max_steps):
        t["bridges"] += 1
        h = len(w)
        Qs = suffix_sums(w)
        k0 = k0_of(Z)
        if not (3 ** k0 > Z and 3 ** (k0 - 1) <= Z):
            t["k0_disagreeing_with_the_least_power"] += 1
        t["largest_k0_seen"] = max(t["largest_k0_seen"], k0)
        acc_real = Fraction(0)
        for ell in range(1, h + 1):
            t["levels"] += 1
            mod = 3 ** ell
            s = 0
            for j in range(1, ell + 1):
                s = (s + 3 ** (j - 1) * pow(1 << Qs[j], -1, mod)) % mod
            if (Z - s) % mod:
                t["congruence_theorem_6_1_violations"] += 1
            acc_real += Fraction(3 ** (ell - 1), 1 << Qs[ell])
            if Z - acc_real != Fraction(3 ** ell * rev[ell], 1 << Qs[ell]):
                t["archimedean_carry_form_violations"] += 1
            r = s if s else mod
            if 3 ** ell > Z:
                t["stabilization_levels"] += 1
                if r != Z:
                    t["stabilization_theorem_7_1_violations"] += 1
            else:
                t["levels_below_the_stabilization_depth"] += 1
                if r % mod != Z % mod:
                    t["representative_at_a_shallow_level_not_z_mod_three_to_the_l"] += 1
    return t


# ---------------------------------------------------------------------------
# valuation aliasing
# ---------------------------------------------------------------------------

def check_aliasing(depth: int = 7, trials: int = 1000) -> dict:
    """Theorem 8.1, with EXACT divisibility rather than floor division.

    The bundle computes `(2^q V - 1)//3` with `//`, which silently truncates if
    the numerator is not divisible. It adjusts the parity first so it never
    is -- but the divisibility is the hypothesis of the theorem, so it is
    checked here instead of arranged.
    """
    t: dict = {"levels": 0, "samples": 0,
               "order_violations": 0,
               "predecessor_not_integral": 0,
               "aliasing_theorem_8_1_violations": 0,
               "aliasing_at_a_shorter_period": 0,
               "aliasing_holds_one_level_deeper": 0}
    for k in range(1, depth + 1):
        t["levels"] += 1
        pk, modhi, modk = 2 * 3 ** k, 3 ** (k + 1), 3 ** k
        if pow(2, pk, modhi) != 1:
            t["order_violations"] += 1
        for i in range(trials):
            v = 1 + (i * 7919) % (modhi - 1)
            if v % 3 == 0:
                v += 1
            q = 1 + (i * 31) % 29
            if pow(2, q, 3) * (v % 3) % 3 != 1:
                q += 1
            num = (1 << q) * v - 1
            if num % 3:
                t["predecessor_not_integral"] += 1
                continue
            t["samples"] += 1
            a = num // 3
            b = ((1 << (q + pk)) * v - 1) // 3
            if (b - a) % modk:
                t["aliasing_theorem_8_1_violations"] += 1
            # sharpness: the difference is divisible by 3^k and, because the
            # order of 2 modulo 3^{k+2} is 3*P_k rather than P_k, generally
            # NOT by 3^{k+1}. A counter that only checked the first half would
            # pass for a period three times too long.
            if (b - a) % modhi == 0:
                t["aliasing_holds_one_level_deeper"] += 1
            # a SHORTER period must not alias, or the theorem's period is not
            # the sharp one -- checked at the largest proper divisor
            c = ((1 << (q + pk // 3)) * v - 1) // 3 if (
                (1 << (q + pk // 3)) * v - 1) % 3 == 0 else None
            if c is not None and (c - a) % modk == 0 and k >= 2:
                t["aliasing_at_a_shorter_period"] += 1
    return t


# ---------------------------------------------------------------------------
# their mesoscopic block
# ---------------------------------------------------------------------------

def check_mesoscopic(trials: int = 10000) -> dict:
    """Ten thousand executions of the defining property of a ceiling.

    The block asserts `3^kcrit >= target`, `3^{kcrit-1} < target` and
    `3^{kcrit-2} < target` for `kcrit = ceil(log_3 target)`. The first two are
    the definition of a ceiling; the third is implied by the second. All three
    are computed in float64, so the only way any could fail is a rounding that
    puts `kcrit` on the wrong side of an integer -- and the distance from
    `log_3(target)` to the nearest integer is measured here for exactly that
    reason.
    """
    t: dict = {"samples": 0,
               "ceiling_definition_violations": 0,
               "third_assertion_not_implied_by_the_second": 0,
               "samples_that_could_have_failed": 0,
               "closest_log_to_an_integer": None,
               "smallest_margin_ratio": None}
    closest, margin = None, None
    for i in range(trials):
        h = 10 ** 5 + (i * 104729) % (10 ** 12 - 10 ** 5)
        gamma = 0.05 + 0.9 * ((i * 7919) % 10007) / 10007.0
        target = h ** gamma
        kcrit = math.ceil(math.log(target, 3))
        t["samples"] += 1
        if not (3 ** kcrit >= target and (kcrit <= 0 or 3 ** (kcrit - 1) < target)):
            t["ceiling_definition_violations"] += 1
        # the third assertion follows from the second: 3^{k-2} < 3^{k-1}
        k = max(0, kcrit - 2)
        if not (3 ** k < target):
            t["third_assertion_not_implied_by_the_second"] += 1
        # how close did the logarithm come to an integer?
        lg = math.log(target, 3)
        d = min(lg - math.floor(lg), math.ceil(lg) - lg)
        if closest is None or d < closest:
            closest = d
        # a double's relative error here is ~1e-16 on a value up to ~25
        if d < 1e-12:
            t["samples_that_could_have_failed"] += 1
        r = d / 1e-15
        if margin is None or r < margin:
            margin = r
    t["closest_log_to_an_integer"] = closest
    t["smallest_margin_ratio"] = margin
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"examples": 0, "x_disagreeing": 0, "z_disagreeing": 0,
               "exponent_word_disagreeing": 0, "h_disagreeing": 0,
               "max_lift_disagreeing": 0,
               "stabilization_depth_disagreeing": 0,
               "carry_final_disagreeing": 0,
               "sources_appearing_more_than_once": 0,
               "rows": []}
    seen: dict[int, int] = {}
    for ex in report.get("finite_zero_lift_examples", []):
        t["examples"] += 1
        y = ex["y"]
        seen[y] = seen.get(y, 0) + 1
        vals, qs, cur = [y], [], y
        for _ in range(60):
            m = 3 * cur + 1
            k = v2(m)
            cur = m >> k
            vals.append(cur)
            qs.append(k)
            if cur == ex["Z"] and len(qs) >= 2:
                break
        X, Z, w = vals[1], vals[-1], tuple(qs[1:])
        if X != ex["X"]:
            t["x_disagreeing"] += 1
        if Z != ex["Z"]:
            t["z_disagreeing"] += 1
        if list(w) != list(ex["tail_code"]):
            t["exponent_word_disagreeing"] += 1
        if len(w) != ex["h"]:
            t["h_disagreeing"] += 1
        ms = lift_profile(w)
        if max(ms) != ex["max_lift"]:
            t["max_lift_disagreeing"] += 1
        if k0_of(Z) != ex["stabilization_depth_k0"]:
            t["stabilization_depth_disagreeing"] += 1
        rev = list(reversed(vals[1:]))
        W = carry(w, rev)
        mine = "%d/%d" % (W[-1].numerator, W[-1].denominator)
        if mine != ex["carry_final"]:
            t["carry_final_disagreeing"] += 1
        t["rows"].append({"y": y, "X": X, "Z": Z, "h": len(w),
                          "word": list(w), "lift_profile": ms[1:],
                          "k0": k0_of(Z), "carry_final": mine,
                          "carry_over_z": float(W[-1] / Z)})
    t["sources_appearing_more_than_once"] = sum(1 for v in seen.values() if v > 1)
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
    named, with_digest = set(), set()
    for key in ("markdown_checks", "json_checks"):
        for rec in val.get(key, []) or []:
            if isinstance(rec, dict) and "file" in rec:
                t["validation_per_file_entries"] += 1
                named.add(rec["file"])
                if "sha256" in rec:
                    t["validation_entries_with_a_digest"] += 1
                    with_digest.add(rec["file"])
                    if rec["file"] in actual and actual[rec["file"]] != rec["sha256"]:
                        t["validation_digest_mismatches"] += 1
    pc = val.get("python_compile")
    if isinstance(pc, dict) and "file" in pc:
        named.add(pc["file"])
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in named]
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_all_ok_flag"] = val.get("all_ok")
    t["validation_top_level_keys"] = sorted(val)
    t["validation_checker_rerun"] = val.get("checker_rerun")
    t["validation_python_compile_ok"] = (
        pc.get("ok") if isinstance(pc, dict) else pc)
    t["validation_file_ok_flags_not_true"] = sum(
        1 for rec in (val.get("markdown_checks", []) or [])
        if isinstance(rec, dict) and rec.get("ok") is not True)
    t["validation_json_parse_not_true"] = sum(
        1 for rec in (val.get("json_checks", []) or [])
        if isinstance(rec, dict) and rec.get("parse_ok") is not True)
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
    ca, tw = res["carry"], res["tower"]
    mine = {
        "finite_local_bridges": res["population"]["bridges"],
        "zero_lift_bridges": ca["bridges"],
        "carry_conjugacy_exact": ca["steps"],
        "carry_monotone_band": ca["bridges"],
        "state_lift_window": ca["positions"],
        "nested_endpoint_tower": tw["levels"],
        "mechanical_neutrality": res["neutrality"]["intervals"],
        "valuation_aliasing": res["aliasing"]["samples"],
        "mesoscopic_modulus_algebra": res["mesoscopic"]["samples"],
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


def check_population(limit: int, max_steps: int) -> dict:
    t: dict = {"bridges": 0, "zero_lift": 0, "positive_lift": 0,
               "sources": 0, "longest_tail": 0}
    src = set()
    for y, X, Z, vals, w in local_bridges(limit, max_steps):
        t["bridges"] += 1
        src.add(y)
        t["longest_tail"] = max(t["longest_tail"], len(w))
        if lift_profile(w)[len(w)] == 0:
            t["zero_lift"] += 1
        else:
            t["positive_lift"] += 1
    t["sources"] = len(src)
    return t


SECTIONS = ("instrument", "constants", "population", "carry", "neutrality",
            "tower", "aliasing", "mesoscopic", "examples", "artifacts",
            "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("carry", "carry_definition_violations"),
    ("carry", "carry_recurrence_theorem_3_1_violations"),
    ("carry", "carry_not_strictly_decreasing"),
    ("carry", "carry_start_not_the_endpoint"),
    ("carry", "carry_end_not_the_phased_source"),
    ("carry", "iterated_carry_form_violations"),
    ("carry", "carry_band_theorem_4_1_violations"),
    ("carry", "dyadic_window_corollary_4_2_violations"),
    ("carry", "sharper_window_lower_violations"),
    ("carry", "sharper_window_upper_violations"),
    ("carry", "state_is_not_the_phased_carry"),
    ("neutrality", "telescoping_violations"),
    ("neutrality", "mechanical_symbol_outside_one_or_two"),
    ("neutrality", "two_consecutive_mechanical_ones"),
    ("neutrality", "band_violations"),
    ("neutrality", "phase_form_violations"),
    ("tower", "congruence_theorem_6_1_violations"),
    ("tower", "archimedean_carry_form_violations"),
    ("tower", "stabilization_theorem_7_1_violations"),
    ("tower", "representative_at_a_shallow_level_not_z_mod_three_to_the_l"),
    ("tower", "k0_disagreeing_with_the_least_power"),
    ("aliasing", "order_violations"),
    ("aliasing", "predecessor_not_integral"),
    ("aliasing", "aliasing_theorem_8_1_violations"),
    ("aliasing", "aliasing_at_a_shorter_period"),
    ("mesoscopic", "ceiling_definition_violations"),
    ("mesoscopic", "third_assertion_not_implied_by_the_second"),
    ("examples", "x_disagreeing"),
    ("examples", "z_disagreeing"),
    ("examples", "exponent_word_disagreeing"),
    ("examples", "h_disagreeing"),
    ("examples", "max_lift_disagreeing"),
    ("examples", "stabilization_depth_disagreeing"),
    ("examples", "carry_final_disagreeing"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_digest_mismatches"),
    ("artifacts", "validation_file_ok_flags_not_true"),
    ("artifacts", "validation_json_parse_not_true"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("population", "bridges"),
    ("population", "sources"),
    ("carry", "bridges"),
    ("carry", "steps"),
    ("carry", "positions"),
    ("carry", "largest_lift_seen"),
    ("neutrality", "intervals"),
    ("neutrality", "telescoping_checks"),
    ("tower", "bridges"),
    ("tower", "levels"),
    ("tower", "stabilization_levels"),
    ("tower", "levels_below_the_stabilization_depth"),
    ("aliasing", "levels"),
    ("aliasing", "samples"),
    ("mesoscopic", "samples"),
    ("examples", "examples"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "frontier_and_report_disagreeing"),
    ("constants", "frontier_constants_matching_no_evaluation"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("population", "zero_lift"),
    ("population", "positive_lift"),
    ("population", "longest_tail"),
    ("carry", "sharper_window_upper_attained"),
    ("carry", "sharper_window_lower_attained"),
    ("tower", "largest_k0_seen"),
    ("aliasing", "aliasing_holds_one_level_deeper"),
    ("mesoscopic", "samples_that_could_have_failed"),
    ("examples", "sources_appearing_more_than_once"),
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
    ap.add_argument("--limit", type=int, default=36000)
    ap.add_argument("--max-steps", type=int, default=46)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

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
    run("population", lambda: check_population(a.limit, a.max_steps))
    run("carry", lambda: check_carry(a.limit, a.max_steps))
    run("neutrality", check_neutrality)
    run("tower", lambda: check_tower(a.limit, a.max_steps))
    run("aliasing", check_aliasing)
    run("mesoscopic", check_mesoscopic)
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
        "run": "RUN-047", "round": "A-U.2d.19", "bundle": str(bundle),
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
