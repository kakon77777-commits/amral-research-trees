"""RUN-045 — independent recheck of Hard-Zeta round A-U.2d.17.

`Small-Endpoint Critical Bridge Cylinder Rigidity` (source item 64). 數學戰士「墜衡」.

A-U.2d.16 produced a local object -- the consecutive-record bridge. This round
puts the exact two-sided code cylinders on it. As at RUN-044, the round is
checkable because `2^{beta m} = 3^m` turns every headline statement into exact
rational arithmetic. Three separate places, all with no logarithm deciding
anything:

  * `2^{-H_i} = 3^{h-i} / 2^{Q-P_i}`, so Theorem 5.1 is rational -- the bundle
    says this too. Multiplying by `2^Q` shows it is TERM BY TERM the definition
    of `B_w`, so the identity carries no information on its own. The content is
    the affine relation `2^Q Z = 3^h X + B_w` on real orbit data, and that is
    what this gate checks.
  * `2^E = 2^Q / 3^h`, so Theorem 8.3's `E >= log2(1 + (5-(2/3)^h)/Z)` is the
    rational inequality `2^Q/3^h >= 1 + (5-(2/3)^h)/Z`. The bundle checks it in
    float64 with a `1e-12` fudge.
  * `2^{sum_i H_i} = 2^{sum_k k q_k} / 3^{h(h+1)/2}`, because `h(h+1)/2` is an
    integer. So Theorem 6.1's Jensen bound `avg H >= log2(h/S)` is the integer
    inequality `2^A * S^h >= h^h * 3^{h(h+1)/2}`. The bundle checks Jensen only
    on synthetic random `H` lists, never on a bridge.

Where a stated result is an IDENTITY it is treated as one. Theorem 7.1 is
`sum_i H_i = sum_k k(q_k - beta)`: both sides reduce to `A - beta*h(h+1)/2`, so
comparing them numerically compares a quantity with itself. Its content is the
combinatorial rearrangement `sum_{i<h} (Q - P_i) = sum_k k q_k`, and that is
checked in integers. Section 9's `E = m_h + eps^+` is true by the definition of
`m_h`; the content is `m_h >= 0`.

Usage:
    python code/src64_small_endpoint_cylinder.py --bundle <dir> [--limit N]
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
    ln_bracket, simplify, ulps_against_bracket, widen,
)
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d17_Small_Endpoint_Critical_Bridge"
         "_Cylinder_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d17_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d17_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d17_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d17.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.17_AU2d17.md"
STDOUT = "CHECKER_STDOUT_AU2d17.txt"


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


def log2_int(c: int) -> tuple[Fraction, Fraction]:
    """`log2` of a positive integer, range-reduced by ONE bit shift.

    `log2_any` halves a Fraction until it is below two, which for a binomial
    coefficient of five thousand bits is five thousand divisions of a rational
    with a five-thousand-bit numerator. The exponent is already sitting in the
    bit length.
    """
    assert c > 0
    k = c.bit_length() - 1
    # The shift leaves an argument in [1,2) but its NUMERATOR is still the
    # whole coefficient, and the series raises `(x-1)/(x+1)` to the 161st
    # power -- a quarter of a million digits. Replace it by a simple rational
    # bracket first; that only ever widens the answer.
    x_lo, x_hi = simplify(Fraction(c, 1 << k), 30)
    lo, _ = log2_any(x_lo)
    _, hi = log2_any(x_hi)
    return k + lo, k + hi


def h2_bracket(r: Fraction) -> tuple[Fraction, Fraction]:
    """Binary entropy of an exact rational `r` in (0,1), as a bracket.

    `h2(r) = -r log2 r - (1-r) log2(1-r)`. Both logarithms are negative, so
    each product is bracketed by swapping the ends.
    """
    assert 0 < r < 1
    a_lo, a_hi = widen(*log2_any(r), 50)
    b_lo, b_hi = widen(*log2_any(1 - r), 50)
    lo = -r * a_hi - (1 - r) * b_hi
    hi = -r * a_lo - (1 - r) * b_lo
    return lo, hi


def entropy_bracket() -> tuple[Fraction, Fraction]:
    """`e_beta = beta * h2(1/beta)`.

    `h2` is strictly decreasing on (1/2, 1) and `1/beta = 0.63... > 1/2`, so a
    bracket for `1/beta` maps to a bracket for `h2` with the ends swapped. Both
    factors are positive, so the product bracket is endpoint-wise.
    """
    b_lo, b_hi = widen(*beta_tight(), 45)
    p_lo, p_hi = 1 / b_hi, 1 / b_lo
    assert Fraction(1, 2) < p_lo <= p_hi < 1
    h_lo, _ = h2_bracket(p_hi)
    _, h_hi = h2_bracket(p_lo)
    return b_lo * h_lo, b_hi * h_hi


def step(n: int) -> tuple[int, int]:
    t = 3 * n + 1
    k = v2(t)
    return t >> k, k


def prefix_sums(word: tuple[int, ...]) -> list[int]:
    out, run = [0], 0
    for q in word:
        run += q
        out.append(run)
    return out


def suffix_supercritical(word: tuple[int, ...]) -> bool:
    """`H_i > 0` for every `i`, decided by `2^{Q-P_i} > 3^{h-i}`.

    Integers only. `H_i > 0` is `sum_{k>i} q_k > beta (h-i)`, and raising two
    to both sides turns `beta` into an exponent of three.
    """
    h, run = len(word), 0
    for j in range(h - 1, -1, -1):
        run += word[j]
        if not (1 << run) > 3 ** (h - j):
            return False
    return True


def b_of(word: tuple[int, ...]) -> int:
    """`B_w = sum_{i<h} 3^{h-1-i} 2^{P_i}`, from the definition."""
    h, run, out = len(word), 0, 0
    for j, q in enumerate(word):
        out += 3 ** (h - 1 - j) * (1 << run)
        run += q
    return out


def local_bridges(limit_y: int, max_steps: int = 36
                  ) -> list[tuple[int, int, int, tuple[int, ...], int]]:
    """The bundle's finite-bridge population, rebuilt from its definition.

    An odd `y` with `y = 7 or 11 mod 12`, a first accelerated step of valuation
    one, and any later state `Z > y` in the same residue classes lying below
    every interior state, whose tail word is fully suffix-supercritical.

    This is NOT "consecutive suffix-minimum records": one `y` can contribute
    several, and `y = 155` contributes both `Z = 175` (h=1) and `Z = 167`
    (h=6), of which at most one can be the next record. Section 12 of the paper
    says so -- these are local cylinder witnesses, not orbit records. The
    stricter population is built separately by `record_gaps`.
    """
    out = []
    for y in range(7, limit_y + 1, 2):
        if y % 3 == 0 or y % 12 not in (7, 11):
            continue
        vals, qs, seen, cur = [y], [], {y}, y
        for s in range(1, max_steps + 1):
            cur, q = step(cur)
            if cur in seen:
                break
            seen.add(cur)
            vals.append(cur)
            qs.append(q)
            if s >= 2 and cur > y and cur % 12 in (7, 11):
                inter = vals[1:-1]
                if inter and cur < min(inter) and qs[0] == 1:
                    tail = tuple(qs[1:])
                    if tail and suffix_supercritical(tail):
                        out.append((y, vals[1], cur, tail, s))
            if cur == 1:
                break
    return out


def record_gaps(limit_y: int, window: int = 40
                ) -> list[tuple[int, int, int, tuple[int, ...]]]:
    """CONSECUTIVE suffix-minimum gaps, the RUN-044 object.

    A whole convergent orbit has no suffix minima -- it ends at its global
    minimum -- so the population lives on a finite window, exactly as at
    RUN-042/043/044.
    """
    out = []
    for y0 in range(7, limit_y + 1, 2):
        if y0 % 3 == 0:
            continue
        word, values = accelerated(y0, max_steps=window)
        if len(values) <= window:
            continue
        vals = values[:window + 1]
        run, mins = None, []
        for s in range(window, -1, -1):
            if run is None or vals[s] < run:
                run = vals[s]
                if s < window:
                    mins.append(s)
        mins.reverse()
        for a, b in zip(mins, mins[1:]):
            if b - a < 2 or word[a] != 1:
                continue
            out.append((vals[a], vals[a + 1], vals[b],
                        tuple(word[a + 1:b])))
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

    b_lo, b_hi = beta_tight()
    lo, hi = log2_any(Fraction(3))
    want("log2(3) agrees with beta", lo <= b_hi and hi >= b_lo)
    want("beta bracket is not degenerate", b_lo < b_hi)
    want("beta-1 is between 0.58 and 0.59",
         Fraction(58, 100) < b_lo - 1 and b_hi - 1 < Fraction(59, 100))

    # h2(1/2) = 1 exactly is the one value of binary entropy known in closed
    # form; a bracket that does not contain it has a broken sign somewhere.
    lo, hi = h2_bracket(Fraction(1, 2))
    want("h2(1/2) brackets 1", lo <= 1 <= hi)
    want("h2 is symmetric at 1/4 and 3/4",
         h2_bracket(Fraction(1, 4))[0] <= h2_bracket(Fraction(3, 4))[1]
         and h2_bracket(Fraction(3, 4))[0] <= h2_bracket(Fraction(1, 4))[1])
    # decreasing on (1/2,1) is the fact `entropy_bracket` relies on to swap ends
    want("h2 decreases on (1/2,1)",
         h2_bracket(Fraction(6, 10))[0] > h2_bracket(Fraction(7, 10))[1])

    # ceil(beta h) with no logarithm. beta*h is never an integer for h >= 1, so
    # the ceiling is the bit length of 3^h rather than that minus one.
    bad = 0
    for h in range(1, 400):
        if (3 ** h).bit_length() - 1 != math.floor(h * math.log2(3)):
            bad += 1
    want("floor(beta h) is the bit length of 3^h minus one", bad == 0)

    # the phase-gap enumeration, done exhaustively rather than by the mod-6
    # shortcut the paper's proof sketch uses
    xs = {r for r in range(36) if r % 18 in (11, 17)}
    zs = {r for r in range(36) if r % 12 in (7, 11)}
    want("X-Z=2 is impossible on the combined classes mod 36",
         not any((z + 2) % 36 in xs for z in zs))
    want("X-Z=4 IS possible on the combined classes mod 36",
         any((z + 4) % 36 in xs for z in zs))

    # The substitution the whole round rests on. It cannot be written as
    # `2**(m*b_lo) < 3**m`: a Fraction exponent sends Python to float64, which
    # is exactly what the check exists to rule out. The bracket form is
    # `m*b_lo <= log2(3^m) <= m*b_hi`, and the width must be nonzero or the
    # test would pass for a bracket that had collapsed.
    bad, degenerate = 0, 0
    for m in (1, 2, 5, 17, 60):
        lo, hi = log2_any(Fraction(3 ** m))
        if not (m * b_lo <= hi and lo <= m * b_hi):
            bad += 1
        if not m * b_lo < m * b_hi:
            degenerate += 1
    want("log2(3^m) lies in [m*beta_lo, m*beta_hi]", bad == 0)
    want("the beta bracket has width at every m", degenerate == 0)

    # the exponent arithmetic those brackets stand in for, in integers: the
    # suffix test `2^{Q-P} > 3^{h-i}` is what `H_i > 0` becomes
    want("2^2 > 3^1 but 2^3 < 3^2", (1 << 2) > 3 and not (1 << 3) > 3 ** 2)

    # log2_int strips the exponent with a bit shift, so a power of two must
    # come back exactly and a nearby integer must NOT -- one test alone would
    # pass for a function that always returned the bit length.
    bad, flat = 0, 0
    for k in (1, 10, 300, 4000):
        lo, hi = log2_int(1 << k)
        if not lo <= k <= hi:
            bad += 1
        lo, hi = log2_int((1 << k) + (1 << (k - 1)))
        if not k < lo:
            flat += 1
    want("log2_int is exact on powers of two", bad == 0)
    want("log2_int is strictly above the bit length off a power of two",
         flat == 0)
    return out


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

def _entropy_chain() -> float:
    """`beta * h2(1/beta)` down the float64 route the shipped checker takes."""
    b = math.log2(3)
    p = 1 / b
    return b * -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def verdict_with_budget(pub: float, lo: Fraction, hi: Fraction,
                        chain: float | None, budget: int) -> tuple[str, int]:
    """Exact, within-budget-and-matching-the-chain, or disagreeing.

    The ORDER is the bound. RUN-040 shipped an excuse with no magnitude cap and
    RUN-041 rebuilt it with the cap in an unreachable elif; the cap has to be
    tested BEFORE the chain, and it has to be sized to what the explanation can
    actually produce -- here, the ulps a cancelling subtraction or a logarithm
    near one can lose.
    """
    v = ulps_against_bracket(pub, lo, hi)
    if not v["decided"]:
        return "undecided", 0
    d = v["ulps"]
    if d == 0:
        return "exact", 0
    if abs(d) > budget:
        return "beyond the cancellation budget of %d ulp" % budget, d
    if chain is not None and bits(pub) == bits(chain):
        return "the float64 chain", d
    return "within budget but matching no evaluation", d


def check_constants(frontier: dict, report: dict) -> dict:
    """Each published constant against a certified bracket AND the float64
    route the artifact would have taken. The magnitude cap is tested BEFORE the
    chain excuse: RUN-041 rebuilt this branch with the cap second, in an elif
    that could never be reached."""
    t: dict = {"constants_checked": 0,
               "disagreeing_with_both_evaluations": 0,
               "from_the_float64_chain_not_the_nearest_double": 0,
               "exact_to_the_last_bit": 0,
               "undecided_brackets": 0,
               "missing_from_the_frontier": 0,
               "frontier_and_report_disagreeing": 0,
               "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    e_lo, e_hi = widen(*entropy_bracket(), 40)
    pb = frontier["beta"]
    ec = _entropy_chain()
    # budget = 4 * (largest operand / result), the factor by which a formula
    # magnifies one ulp of its inputs. 4 for anything that does not cancel.
    items = [
        ("beta", b_lo, b_hi, pb, 4),
        ("beta_minus_one", b_lo - 1, b_hi - 1, pb - 1.0, 12),
        ("critical_gap_exponent", Fraction(1, 5), Fraction(1, 5), 0.2, 4),
        ("inverse_beta_minus_one", 1 / (b_hi - 1), 1 / (b_lo - 1),
         1.0 / (pb - 1.0), 12),
        ("first_hit_single_cylinder_exponent_limit",
         1 / (5 * (b_hi - 1)), 1 / (5 * (b_lo - 1)), 1.0 / (5 * (pb - 1.0)),
         12),
        ("first_hit_joint_cylinder_exponent_limit",
         2 / (5 * (b_hi - 1)), 2 / (5 * (b_lo - 1)),
         2 * (1.0 / (5 * (pb - 1.0))), 12),
        ("raw_nearcritical_composition_entropy_bits_per_h", e_lo, e_hi, ec, 12),
        ("source_modulus_bits_per_h", b_lo, b_hi, pb, 4),
        # beta - e_beta: 1.585 and 1.506 giving 0.0793, a magnification of 20,
        # on top of a parent already two ulps out
        ("source_entropy_rate_gap_bits_per_h", b_lo - e_hi, b_hi - e_lo,
         math.log2(3) - ec, 80),
        ("double_cylinder_modulus_bits_per_h", 2 * b_lo, 2 * b_hi, 2 * pb, 4),
    ]
    for name, lo, hi, chain, budget in items:
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        rpt = report.get("constants", {}).get(name)
        if rpt is not None and rpt != pub:
            t["frontier_and_report_disagreeing"] += 1
        row = {"constant": name, "published": repr(pub), "budget": budget}
        # ORDER MATTERS, and it lives inside verdict_with_budget: the magnitude
        # cap is tested BEFORE the chain excuse, because an excuse licenses
        # only discrepancies the size its explanation can produce.
        verdict, d = verdict_with_budget(pub, lo, hi, chain, budget)
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
# the bridge population and the exact identities on it
# ---------------------------------------------------------------------------

def check_bridges(limit: int, max_steps: int = 36) -> dict:
    t: dict = {"bridges": 0, "sources": 0, "longest_tail": 0,
               "suffixes_checked": 0,
               "affine_identity_violations": 0,
               "b_w_not_matching_the_closed_form": 0,
               "laplace_identity_violations": 0,
               "laplace_sum_not_positive": 0,
               "suffix_not_supercritical": 0,
               "correction_floor_violations": 0,
               "excess_floor_theorem_8_3_violations": 0,
               "excess_floor_decided_by_the_float64_fudge": 0,
               "phase_gap_violations": 0,
               "source_outside_11_or_17_mod_18": 0,
               "endpoint_outside_7_or_11_mod_12": 0,
               "endpoint_not_below_the_source": 0,
               "integer_lift_negative": 0,
               "one_sided_phase_outside_the_unit_interval": 0,
               "smallest_phase_gap_seen": None,
               "smallest_excess_floor_slack": None,
               "integer_lift_zero": 0}
    bridges = local_bridges(limit, max_steps)
    t["bridges"] = len(bridges)
    t["sources"] = len({y for y, *_ in bridges})
    tightest = None
    for y, X, Z, w, _ in bridges:
        h, Q = len(w), sum(w)
        t["longest_tail"] = max(t["longest_tail"], h)
        P = prefix_sums(w)

        # (1) the affine relation. THIS is the content of section 5; the
        # Laplace identity below is the same statement divided by 2^Q.
        B = b_of(w)
        if (1 << Q) * Z != 3 ** h * X + B:
            t["affine_identity_violations"] += 1
        if B != sum(3 ** (h - 1 - i) * (1 << P[i]) for i in range(h)):
            t["b_w_not_matching_the_closed_form"] += 1

        # (2) the published rational form, as its own route through Fractions
        lhs = sum(Fraction(3 ** (h - i), 1 << (Q - P[i])) for i in range(h))
        rhs = 3 * (Fraction(Z) - Fraction(3 ** h, 1 << Q) * X)
        if lhs != rhs:
            t["laplace_identity_violations"] += 1
        if not lhs > 0:
            t["laplace_sum_not_positive"] += 1

        # (3) every suffix supercritical, in integers
        for i in range(h):
            t["suffixes_checked"] += 1
            if not (1 << (Q - P[i])) > 3 ** (h - i):
                t["suffix_not_supercritical"] += 1

        # (4) Lemma 8.2, exact
        if not Fraction(B, 3 ** h) >= 1 - Fraction(2, 3) ** h:
            t["correction_floor_violations"] += 1

        # (5) Theorem 8.3, exact. 2^E = 2^Q/3^h, so no logarithm decides it.
        floor = 1 + (5 - Fraction(2, 3) ** h) / Z
        slack = Fraction(1 << Q, 3 ** h) - floor
        if slack < 0:
            t["excess_floor_theorem_8_3_violations"] += 1
        if tightest is None or slack < tightest:
            tightest = slack
        # would the bundle's float64 form with its 1e-12 fudge have agreed?
        e_f = Q - h * math.log2(3)
        f_f = math.log2(1 + (5 - (2 / 3) ** h) / Z)
        if (e_f + 1e-12 >= f_f) != (slack >= 0):
            t["excess_floor_decided_by_the_float64_fudge"] += 1

        # (6) Lemma 8.1 and the phases it rests on
        if X % 18 not in (11, 17):
            t["source_outside_11_or_17_mod_18"] += 1
        if Z % 12 not in (7, 11):
            t["endpoint_outside_7_or_11_mod_12"] += 1
        if not X > Z:
            t["endpoint_not_below_the_source"] += 1
        gap = X - Z
        if gap < 4:
            t["phase_gap_violations"] += 1
        if t["smallest_phase_gap_seen"] is None or gap < t["smallest_phase_gap_seen"]:
            t["smallest_phase_gap_seen"] = gap

        # (7) section 9. `E = m_h + eps^+` is true by the definition of m_h;
        # the content is that the lift is nonnegative and the phase is in (0,1).
        m_h = Q - (3 ** h).bit_length()
        if m_h < 0:
            t["integer_lift_negative"] += 1
        if m_h == 0:
            t["integer_lift_zero"] += 1
        # eps = ceil(beta h) - beta h in (0,1). Lower end from the UPPER beta,
        # upper end from the LOWER: an OR of two one-sided tests would pass on
        # a bracket that had collapsed the wrong way.
        ceil_v = Fraction((3 ** h).bit_length())
        if not (ceil_v - Fraction(h) * beta_hi() > 0
                and ceil_v - 1 < Fraction(h) * beta_lo()):
            t["one_sided_phase_outside_the_unit_interval"] += 1
    t["smallest_excess_floor_slack"] = (None if tightest is None
                                        else float(tightest))
    return t


_BETA_CACHE: list = []


def beta_lo() -> Fraction:
    if not _BETA_CACHE:
        _BETA_CACHE.extend(widen(*beta_tight(), 40))
    return _BETA_CACHE[0]


def beta_hi() -> Fraction:
    if not _BETA_CACHE:
        _BETA_CACHE.extend(widen(*beta_tight(), 40))
    return _BETA_CACHE[1]


# ---------------------------------------------------------------------------
# double-canonical collapse
# ---------------------------------------------------------------------------

def check_canonical(limit: int, max_steps: int = 36) -> dict:
    """Theorem 4.1 has two halves and the bundle only tests one of them.

    The congruences `X = r_2(w) mod 2^{Q+1}` and `Z = r_3(w) mod 3^h` hold for
    EVERY word; the collapse to equality needs the smallness. The shipped
    checker guards both with `if X < 2**(Q+1) and Z < 3**h`, so a congruence
    that failed on a large bridge would never be seen. Here the congruence is
    checked on all of them and the collapse on the ones inside the moduli, with
    the two smallness conditions counted separately.
    """
    t: dict = {"bridges": 0,
               "source_congruence_violations": 0,
               "endpoint_congruence_violations": 0,
               "source_inside_its_modulus": 0,
               "endpoint_inside_its_modulus": 0,
               "both_inside_their_moduli": 0,
               "collapse_violations": 0,
               "collapse_asserted_outside_the_moduli": 0,
               "representative_does_not_satisfy_its_congruence": 0}
    for y, X, Z, w, _ in local_bridges(limit, max_steps):
        t["bridges"] += 1
        h, Q = len(w), sum(w)
        B = b_of(w)
        m2, m3 = 1 << (Q + 1), 3 ** h
        r2 = ((1 << Q) - B) * pow(3 ** h, -1, m2) % m2
        r3 = B * pow(1 << Q, -1, m3) % m3
        # `0 <= r < m` holds by construction of `%`, so testing it names no
        # failing world. What can be wrong is the modular inverse, so check
        # that each representative satisfies the congruence that defines it.
        if (r2 * 3 ** h - ((1 << Q) - B)) % m2 or not 0 <= r2 < m2:
            t["representative_does_not_satisfy_its_congruence"] += 1
        if (r3 * (1 << Q) - B) % m3 or not 0 <= r3 < m3:
            t["representative_does_not_satisfy_its_congruence"] += 1
        if (X - r2) % m2:
            t["source_congruence_violations"] += 1
        if (Z - r3) % m3:
            t["endpoint_congruence_violations"] += 1
        a, b = X < m2, Z < m3
        t["source_inside_its_modulus"] += int(a)
        t["endpoint_inside_its_modulus"] += int(b)
        if a and b:
            t["both_inside_their_moduli"] += 1
            if r2 != X or r3 != Z:
                t["collapse_violations"] += 1
        else:
            # the theorem is NOT claimed here; assert only that it would be
            # wrong to claim it, so a defect that drops the guard is caught
            if (not a and r2 == X and X >= m2) or (not b and r3 == Z and Z >= m3):
                t["collapse_asserted_outside_the_moduli"] += 1
    return t


# ---------------------------------------------------------------------------
# Jensen and the quantile bound, on real bridges
# ---------------------------------------------------------------------------

def check_plateau(limit: int, max_steps: int = 36) -> dict:
    """Theorems 6.1 and 6.2 on actual bridges rather than synthetic slack.

    Jensen becomes an integer inequality. `sum_i H_i = A - beta*M` with
    `A = sum_k k q_k` and `M = h(h+1)/2`, and `M` is an integer, so

        2^{sum H_i} = 2^A / 3^M

    and `avg H >= log2(h/S)` is `2^A * S^h >= h^h * 3^M`. No logarithm.
    """
    t: dict = {"bridges": 0,
               "jensen_theorem_6_1_violations": 0,
               "jensen_with_the_published_weaker_bound_violations": 0,
               "jensen_weaker_bound_with_a_positive_right_side": 0,
               "quantile_instances": 0,
               "quantile_theorem_6_2_violations": 0,
               "quantile_instances_that_are_not_vacuous": 0,
               "sharp_quantile_instances_that_are_not_vacuous": 0,
               "sharp_quantile_violations": 0,
               "laplace_sum_not_below_three_z": 0,
               "laplace_sum_not_below_h": 0}
    for y, X, Z, w, _ in local_bridges(limit, max_steps):
        t["bridges"] += 1
        h, Q = len(w), sum(w)
        P = prefix_sums(w)
        S = sum(Fraction(3 ** (h - i), 1 << (Q - P[i])) for i in range(h))
        A = sum((k + 1) * w[k] for k in range(h))
        M = h * (h + 1) // 2

        # Corollary 5.2 and the elementary bound the plateau argument needs
        if not S < 3 * Z:
            t["laplace_sum_not_below_three_z"] += 1
        if not S < h:
            t["laplace_sum_not_below_h"] += 1

        # Theorem 6.1, exact and integer
        if not (1 << A) * S ** h >= Fraction(h ** h) * 3 ** M:
            t["jensen_theorem_6_1_violations"] += 1
        # the weaker published form, with its own positivity counter: its right
        # side `log2(h/(3Z))` is negative whenever `3Z >= h`, and then the
        # statement says nothing at all
        if h > 3 * Z:
            t["jensen_weaker_bound_with_a_positive_right_side"] += 1
            if not (1 << A) * Fraction(3 * Z) ** h >= Fraction(h ** h) * 3 ** M:
                t["jensen_with_the_published_weaker_bound_violations"] += 1

        # Theorem 6.2 on an integer grid of A, with the vacuity counted
        for a in range(1, 13):
            t["quantile_instances"] += 1
            cnt = sum(1 for i in range(h)
                      if Fraction(1 << (Q - P[i]), 3 ** (h - i)) < (1 << a))
            if not cnt < 3 * Z * (1 << a):
                t["quantile_theorem_6_2_violations"] += 1
            if 3 * Z * (1 << a) < h:
                t["quantile_instances_that_are_not_vacuous"] += 1
            # the sharp form uses S rather than the 3Z it is bounded by
            if S * (1 << a) < h:
                t["sharp_quantile_instances_that_are_not_vacuous"] += 1
            if not cnt < S * (1 << a):
                t["sharp_quantile_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# the weighted area and the centre of mass
# ---------------------------------------------------------------------------

def check_area(limit: int, max_steps: int = 36) -> dict:
    """Theorem 7.1 is an identity, so its COMPONENTS are what get checked.

    `sum_i H_i` and `sum_k k(q_k - beta)` both reduce to `A - beta*h(h+1)/2`.
    Comparing them numerically -- which is what the shipped checker does, in
    float64 with a 1e-10 tolerance -- compares a quantity with itself. The two
    pieces that can actually be wrong are the combinatorial rearrangement and
    the triangular sum, and both are integer statements.

    Theorem 7.2's finite content is that the centre of mass of the `q-1`
    surplus lies past the midpoint, and that is `2(A - M) > (h+1)(Q - h)` --
    integers, no beta.
    """
    t: dict = {"bridges": 0,
               "rearrangement_violations": 0,
               "triangular_sum_violations": 0,
               "centre_of_mass_before_the_midpoint": 0,
               "centre_of_mass_exactly_at_the_midpoint": 0,
               "centre_of_mass_past_the_midpoint": 0,
               "surplus_total_not_q_minus_h": 0,
               "centre_of_mass_undefined": 0,
               "largest_midpoint_excess_seen": None}
    best = None
    for y, X, Z, w, _ in local_bridges(limit, max_steps):
        t["bridges"] += 1
        h, Q = len(w), sum(w)
        P = prefix_sums(w)
        A = sum((k + 1) * w[k] for k in range(h))
        M = h * (h + 1) // 2
        if sum(Q - P[i] for i in range(h)) != A:
            t["rearrangement_violations"] += 1
        if sum(h - i for i in range(h)) != M:
            t["triangular_sum_violations"] += 1
        R = Q - h
        if sum(q - 1 for q in w) != R:
            t["surplus_total_not_q_minus_h"] += 1
        if R == 0:
            t["centre_of_mass_undefined"] += 1
            continue
        excess = Fraction(2 * (A - M) - (h + 1) * R, 2 * R)
        # `>=`, not `>`. At h=1 the only position is k=1 and (h+1)/2 = 1, so
        # equality is forced and a strict test would accuse 520 correct
        # single-step bridges. The strict cases are counted separately.
        if 2 * (A - M) < (h + 1) * R:
            t["centre_of_mass_before_the_midpoint"] += 1
        elif 2 * (A - M) == (h + 1) * R:
            t["centre_of_mass_exactly_at_the_midpoint"] += 1
        else:
            t["centre_of_mass_past_the_midpoint"] += 1
        if best is None or excess > best:
            best = excess
    t["largest_midpoint_excess_seen"] = None if best is None else float(best)
    return t


# ---------------------------------------------------------------------------
# the first-hit slice of section 10
# ---------------------------------------------------------------------------

def check_first_hit(limit: int, window: int = 60,
                    lam: Fraction = Fraction(1, 10)) -> dict:
    """Section 10, with `2^{delta_v - delta_s} = 3^{v-s} / 2^{K_v - K_s}`.

    Every inequality becomes a comparison of integers after raising both sides
    to the denominator of `lambda`. The published `ell >= lambda/(beta-1) log2 N
    + O(1)` needs no additive constant: it reduces to `K_v - K_s >= v - s`.
    """
    a, b = lam.numerator, lam.denominator
    t: dict = {"orbits": 0, "first_hits": 0,
               "first_hit_below_the_threshold": 0,
               "first_hit_not_minimal": 0,
               "overshoot_above_one_step": 0,
               "length_bound_violations": 0,
               "length_bound_attained_with_no_additive_constant": 0,
               "slack_step_ratio_violations": 0,
               "prefix_valuation_below_the_length": 0,
               "prefix_valuation_not_matching_the_cumulative_sum": 0,
               "source_inside_its_cylinder": 0,
               "source_outside_its_cylinder": 0,
               "endpoint_inside_its_cylinder": 0,
               "endpoint_outside_its_cylinder": 0,
               "largest_n_with_the_source_outside": None}
    for y0 in range(7, limit + 1, 2):
        if y0 % 3 == 0:
            continue
        word, values = accelerated(y0, max_steps=window)
        if len(word) < 3:
            continue
        t["orbits"] += 1
        K = cumulative(word)
        N = y0
        # `2^{delta_v - delta_s} >= N^lambda` with lambda = a/b becomes
        # `(3^v / 2^{K_v})^b >= N^a` -- integers on both sides, no logarithm.
        thresh = Fraction(N ** a)
        for v in range(1, len(word) + 1):
            if Fraction(3 ** v, 1 << K[v]) ** b >= thresh:
                break
        else:
            continue
        t["first_hits"] += 1
        ell, dK = v, K[v]
        cur = Fraction(3 ** ell, 1 << dK)
        if not cur ** b >= thresh:
            t["first_hit_below_the_threshold"] += 1
        # minimality is its OWN failure: one step earlier the threshold was not
        # yet reached. Folding it into the overshoot counter would let either
        # defect hide behind the other.
        if ell >= 1 and Fraction(3 ** (ell - 1), 1 << K[ell - 1]) ** b >= thresh:
            t["first_hit_not_minimal"] += 1
        # the overshoot is at most one step's slack gain, beta-1, i.e. 2^{beta-1}
        # = 3/2 -- again rational
        if not cur ** b < Fraction(3, 2) ** b * thresh:
            t["overshoot_above_one_step"] += 1
        # `ell >= lambda log2 N / (beta-1)` needs no additive constant at all:
        # it reduces to `K_v - K_s >= v - s`, which holds because every
        # valuation is at least one. The paper writes `+ O(1)`.
        if not dK >= ell:
            t["length_bound_violations"] += 1
        if dK == ell:
            t["length_bound_attained_with_no_additive_constant"] += 1
        # `delta_{n+1} - delta_n = beta - q` exponentiates to
        # `2^{delta_{n+1}}/2^{delta_n} = 3 / 2^q`, and 2^{delta_n} = 3^n/2^{K_n}.
        # Testing `q >= 1` instead would name no failing world; this catches a
        # wrong index into K.
        for n in range(ell):
            a1 = Fraction(3 ** (n + 1), 1 << K[n + 1])
            a0 = Fraction(3 ** n, 1 << K[n])
            if a1 / a0 != Fraction(3, 1 << word[n]):
                t["slack_step_ratio_violations"] += 1
        # section 10's `P >= ell`. Computed from the WORD, not from the
        # cumulative array, so that this and the length bound above are two
        # tests rather than one statement wearing two counters -- and so a
        # broken cumulative sum shows up here.
        P = sum(word[:ell])
        if P != dK:
            t["prefix_valuation_not_matching_the_cumulative_sum"] += 1
        if not P >= ell:
            t["prefix_valuation_below_the_length"] += 1
        # Theorem 10.1's containment is asymptotic in N. At these N it holds
        # for a minority, which is a fact about the SCALE, not a violation --
        # so it is counted both ways and neither way is a failure.
        if values[0] < (1 << (dK + 1)):
            t["source_inside_its_cylinder"] += 1
        else:
            t["source_outside_its_cylinder"] += 1
            t["largest_n_with_the_source_outside"] = max(
                t["largest_n_with_the_source_outside"] or 0, N)
        if values[ell] < 3 ** ell:
            t["endpoint_inside_its_cylinder"] += 1
        else:
            t["endpoint_outside_its_cylinder"] += 1
    return t


# ---------------------------------------------------------------------------
# their own guarded assertions, measured independently
# ---------------------------------------------------------------------------

def check_their_guards(trials: int = 40000, seed: int = 26081417) -> dict:
    """How often do the shipped checker's three guarded assertions actually run?

    Its counters increment once per SAMPLE, not once per assertion, and all
    three assertions sit behind `if` guards. This reimplements the sampling
    scheme from its stated parameters and measures the guard rates. The numbers
    are an independent estimate of the rate, not a replay of their stream.
    """
    rng = random.Random(seed)
    t: dict = {"residue_samples": 0,
               "residue_source_assert_fired": 0,
               "residue_endpoint_assert_fired": 0,
               "residue_source_violations": 0,
               "residue_endpoint_violations": 0,
               "quantile_samples": 0,
               "quantile_jensen_guard_open": 0,
               "quantile_bound_not_vacuous": 0,
               "quantile_jensen_violations": 0,
               "quantile_markov_violations": 0}
    for _ in range(trials):
        n = rng.randrange(1, 2_000_000) | 1
        if n % 3 == 0:
            continue
        t["residue_samples"] += 1
        cur, w = n, []
        for _ in range(rng.randint(1, 9)):
            cur, q = step(cur)
            w.append(q)
        h, Q = len(w), sum(w)
        B = b_of(tuple(w))
        if n < 1 << (Q + 1):
            t["residue_source_assert_fired"] += 1
            m2 = 1 << (Q + 1)
            if ((1 << Q) - B) * pow(3 ** h, -1, m2) % m2 != n:
                t["residue_source_violations"] += 1
        if cur < 3 ** h:
            t["residue_endpoint_assert_fired"] += 1
            m3 = 3 ** h
            if B * pow(1 << Q, -1, m3) % m3 != cur:
                t["residue_endpoint_violations"] += 1
    for _ in range(trials // 4):
        t["quantile_samples"] += 1
        h = rng.randint(10, 1000)
        Z = rng.randint(1, 500)
        H = [rng.random() * 8 for _ in range(h)]
        s = sum(2.0 ** (-x) for x in H)
        if s > 3 * Z:
            shift = math.log2(s / (3 * Z)) + 1e-9
            H = [x + shift for x in H]
            s = sum(2.0 ** (-x) for x in H)
        if h > 3 * Z:
            t["quantile_jensen_guard_open"] += 1
            if not sum(H) / h + 1e-9 >= math.log2(h / (3 * Z)):
                t["quantile_jensen_violations"] += 1
        a = rng.random() * 10
        cnt = sum(1 for x in H if x < a)
        if 3 * Z * 2.0 ** a < h:
            t["quantile_bound_not_vacuous"] += 1
        if not cnt <= 3 * Z * 2.0 ** a + 1e-7:
            t["quantile_markov_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# published finite examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"examples": 0, "x_disagreeing": 0, "z_disagreeing": 0,
               "exponent_word_disagreeing": 0, "h_disagreeing": 0,
               "first_step_not_valuation_one": 0,
               "laplace_sum_disagreeing": 0,
               "excess_decimal_disagreeing": 0,
               "phase_floor_disagreeing": 0,
               "tail_not_suffix_supercritical": 0,
               "geometry_violations": 0,
               "sources_appearing_more_than_once": 0,
               "excess_verdicts": [], "phase_floor_verdicts": [],
               "rows": []}
    seen: dict[int, int] = {}
    for ex in report.get("finite_examples", []):
        t["examples"] += 1
        y = ex["y"]
        seen[y] = seen.get(y, 0) + 1
        vals, qs, cur = [y], [], y
        for _ in range(40):
            cur, q = step(cur)
            vals.append(cur)
            qs.append(q)
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
        if qs[0] != 1:
            t["first_step_not_valuation_one"] += 1
        if not suffix_supercritical(w):
            t["tail_not_suffix_supercritical"] += 1
        inter = vals[1:-1]
        if not (Z > y and inter and Z < min(inter)):
            t["geometry_violations"] += 1
        h, Q = len(w), sum(w)
        P = prefix_sums(w)
        S = sum(Fraction(3 ** (h - i), 1 << (Q - P[i])) for i in range(h))
        if float(S) != ex["laplace_sum"]:
            t["laplace_sum_disagreeing"] += 1
        # E = Q - beta*h. The subtraction cancels: the operands are of size
        # beta*h and the answer of size E, so the relative error is magnified
        # by beta*h/E and the ulp budget must be sized to that, not fixed.
        lo, hi = Q - Fraction(h) * beta_hi(), Q - Fraction(h) * beta_lo()
        budget = max(4, int(4 * float(Fraction(h) * beta_hi() / lo)))
        v, d = verdict_with_budget(ex["E"], lo, hi,
                                   Q - h * math.log2(3), budget)
        if v.startswith("beyond") or v.startswith("within budget"):
            t["excess_decimal_disagreeing"] += 1
        t["excess_verdicts"].append({"y": y, "h": h, "verdict": v,
                                     "ulps": d, "budget": budget})
        # log2(1+x) for small x loses about log2(1/x) bits the same way
        arg = 1 + (5 - Fraction(2, 3) ** h) / Z
        f_lo, f_hi = log2_any(arg)
        budget = max(4, int(4 / float(arg - 1)))
        chain = math.log2(1 + (5 - (2 / 3) ** h) / Z)
        v, d = verdict_with_budget(ex["phase_floor"], f_lo, f_hi, chain, budget)
        if v.startswith("beyond") or v.startswith("within budget"):
            t["phase_floor_disagreeing"] += 1
        t["phase_floor_verdicts"].append({"y": y, "h": h, "verdict": v,
                                          "ulps": d, "budget": budget})
        t["rows"].append({"y": y, "X": X, "Z": Z, "h": h,
                          "word": list(w), "laplace_sum": str(S),
                          "X_minus_Z": X - Z})
    t["sources_appearing_more_than_once"] = sum(1 for v in seen.values() if v > 1)
    return t


# ---------------------------------------------------------------------------
# the record-gap population, where the phase hypotheses actually apply
# ---------------------------------------------------------------------------

def check_records(limit: int, window: int = 40) -> dict:
    """The same claims on genuine consecutive suffix-minimum gaps.

    The bundle's population is looser -- one source can contribute several
    bridges, and section 12 says they are not asserted to be records. The phase
    claims are the ones that need the record structure: `Z = 3 mod 4` comes
    from the mandatory valuation-one step out of `Z`, not from the word.
    """
    t: dict = {"gaps": 0, "sources": 0,
               "affine_identity_violations": 0,
               "laplace_identity_violations": 0,
               "phase_gap_violations": 0,
               "endpoint_outside_7_or_11_mod_12": 0,
               "endpoint_not_three_mod_four": 0,
               "suffix_not_supercritical": 0,
               "suffixes_checked": 0,
               "smallest_phase_gap_seen": None}
    gaps = record_gaps(limit, window)
    t["gaps"] = len(gaps)
    t["sources"] = len({y for y, *_ in gaps})
    for y, X, Z, w in gaps:
        h, Q = len(w), sum(w)
        P = prefix_sums(w)
        if (1 << Q) * Z != 3 ** h * X + b_of(w):
            t["affine_identity_violations"] += 1
        lhs = sum(Fraction(3 ** (h - i), 1 << (Q - P[i])) for i in range(h))
        if lhs != 3 * (Fraction(Z) - Fraction(3 ** h, 1 << Q) * X):
            t["laplace_identity_violations"] += 1
        if Z % 12 not in (7, 11):
            t["endpoint_outside_7_or_11_mod_12"] += 1
        if Z % 4 != 3:
            t["endpoint_not_three_mod_four"] += 1
        if X - Z < 4:
            t["phase_gap_violations"] += 1
        g = X - Z
        if t["smallest_phase_gap_seen"] is None or g < t["smallest_phase_gap_seen"]:
            t["smallest_phase_gap_seen"] = g
        for i in range(h):
            t["suffixes_checked"] += 1
            if not (1 << (Q - P[i])) > 3 ** (h - i):
                t["suffix_not_supercritical"] += 1
    return t


# ---------------------------------------------------------------------------
# NO-GO 11.1's entropy rate
# ---------------------------------------------------------------------------

def check_entropy(levels: tuple[int, ...] = (50, 200, 800, 3200)) -> dict:
    """`log2 C(Q-1,h-1) / h -> e_beta` at `Q = ceil(beta h)`.

    Checked by watching the gap shrink, not by asserting a limit at one h. A
    single level cannot distinguish a convergent sequence from a wrong one.
    """
    t: dict = {"levels": 0, "gap_not_shrinking": 0, "rows": [],
               "entropy_rate_above_beta": 0}
    e_lo, e_hi = widen(*entropy_bracket(), 40)
    prev = None
    for h in levels:
        t["levels"] += 1
        Q = (3 ** h).bit_length()
        c = math.comb(Q - 1, h - 1)
        lo, hi = log2_int(c)
        rate_lo, rate_hi = lo / h, hi / h
        gap = max(abs(rate_hi - e_lo), abs(e_hi - rate_lo))
        if prev is not None and gap >= prev:
            t["gap_not_shrinking"] += 1
        prev = gap
        if rate_lo > beta_hi():
            t["entropy_rate_above_beta"] += 1
        t["rows"].append({"h": h, "Q": Q,
                          "rate": bracket_decimal(rate_lo, rate_hi, 6),
                          "gap_to_e_beta": float(gap)})
    return t


# ---------------------------------------------------------------------------
# artifacts
# ---------------------------------------------------------------------------

def check_artifacts(bundle: pathlib.Path) -> dict:
    t: dict = {"files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
               "checksum_lines_naming_a_missing_file": 0,
               "files_with_no_digest_anywhere": [],
               "validation_per_file_entries": 0,
               "validation_entries_with_a_digest": 0,
               "validation_digest_mismatches": 0,
               "validation_size_mismatches": 0,
               "files_absent_from_the_validation_record": [],
               "duplicate_file_pairs": [],
               "stdout_is_the_report_plus_trailing_bytes": False,
               "stdout_extra_bytes": None}
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
    # RUN-044 found these two byte-identical. They are no longer -- measure the
    # difference rather than restating last round's finding.
    a = (bundle / STDOUT).read_bytes()
    b = (bundle / REPORT).read_bytes()
    if a[:len(b)] == b:
        t["stdout_is_the_report_plus_trailing_bytes"] = True
        t["stdout_extra_bytes"] = repr(a[len(b):])

    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = val.get("source_files", val.get("files", {}))
    with_digest = set()
    if isinstance(files, dict):
        for n, r in files.items():
            t["validation_per_file_entries"] += 1
            if isinstance(r, dict) and "sha256" in r:
                t["validation_entries_with_a_digest"] += 1
                with_digest.add(n)
                if n in actual and actual[n] != r["sha256"]:
                    t["validation_digest_mismatches"] += 1
            if isinstance(r, dict) and "size_bytes" in r and n in present:
                if (bundle / n).stat().st_size != r["size_bytes"]:
                    t["validation_size_mismatches"] += 1
    t["files_absent_from_the_validation_record"] = [
        n for n in present if n not in files]
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_all_ok_flag"] = val.get("all_ok", val.get("validation_passed"))
    t["validation_top_level_keys"] = sorted(val)
    t["validation_issue_entries"] = len(val.get("issues", []))
    t["validation_compile_returncode"] = (
        val.get("checker_compile", {}) or {}).get("returncode")
    t["validation_execution_returncode"] = (
        val.get("checker_execution", {}) or {}).get("returncode")
    t["validation_counts_disagreeing_with_the_report"] = sum(
        1 for k, v in (val.get("checker_counts", {}) or {}).items()
        if v != json.loads((bundle / REPORT).read_text(
            encoding="utf-8")).get("checks", {}).get(k))
    return t


# ---------------------------------------------------------------------------
# ledger
# ---------------------------------------------------------------------------

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
    no_go = re.findall(r"^## NO-GO (14\.\d) — (.+)$", paper, re.M)
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
    present_text = " ".join(str(x) for x in
                            (ledger.get(proved_key, []) or [""])[:1])
    t["heuristic_failed_its_positive_control"] = int(
        bool(present_text) and not covered(present_text))
    t["heuristic_failed_its_negative_control"] = int(
        covered("quokka bandersnatch flimflam zeppelin marzipan"))
    return t


def check_their_claims(report: dict, res: dict) -> dict:
    # THEIR names are the key. A mapping keyed on mine reported 11 of 14 as
    # "not reproduced" at RUN-044, which measured my vocabulary, not my
    # coverage -- and under-claiming is the false negative nobody questions.
    br = res["bridges"]["bridges"]
    mine = {
        "finite_local_bridges": br,
        "laplace_identities_exact": br,
        "canonical_rep_collapses_finite":
            res["canonical"]["both_inside_their_moduli"],
        "phase_gap_checks": br,
        "correction_floor_checks": br,
        "suffix_supercritical_suffixes": res["bridges"]["suffixes_checked"],
        "weighted_area_identities": res["area"]["bridges"],
        "random_exact_residue_checks":
            res["their_guards"]["residue_samples"],
        "quantile_jensen_tests": res["their_guards"]["quantile_samples"],
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


FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("constants", "frontier_and_report_disagreeing"),
    ("bridges", "affine_identity_violations"),
    ("bridges", "b_w_not_matching_the_closed_form"),
    ("bridges", "laplace_identity_violations"),
    ("bridges", "laplace_sum_not_positive"),
    ("bridges", "suffix_not_supercritical"),
    ("bridges", "correction_floor_violations"),
    ("bridges", "excess_floor_theorem_8_3_violations"),
    ("bridges", "phase_gap_violations"),
    ("bridges", "source_outside_11_or_17_mod_18"),
    ("bridges", "endpoint_outside_7_or_11_mod_12"),
    ("bridges", "endpoint_not_below_the_source"),
    ("bridges", "integer_lift_negative"),
    ("bridges", "one_sided_phase_outside_the_unit_interval"),
    ("canonical", "source_congruence_violations"),
    ("canonical", "endpoint_congruence_violations"),
    ("canonical", "collapse_violations"),
    ("canonical", "collapse_asserted_outside_the_moduli"),
    ("canonical", "representative_does_not_satisfy_its_congruence"),
    ("plateau", "jensen_theorem_6_1_violations"),
    ("plateau", "jensen_with_the_published_weaker_bound_violations"),
    ("plateau", "quantile_theorem_6_2_violations"),
    ("plateau", "sharp_quantile_violations"),
    ("plateau", "laplace_sum_not_below_three_z"),
    ("plateau", "laplace_sum_not_below_h"),
    ("area", "rearrangement_violations"),
    ("area", "triangular_sum_violations"),
    ("area", "centre_of_mass_before_the_midpoint"),
    ("area", "surplus_total_not_q_minus_h"),
    ("first_hit", "first_hit_below_the_threshold"),
    ("first_hit", "first_hit_not_minimal"),
    ("first_hit", "overshoot_above_one_step"),
    ("first_hit", "length_bound_violations"),
    ("first_hit", "slack_step_ratio_violations"),
    ("first_hit", "prefix_valuation_below_the_length"),
    ("first_hit", "prefix_valuation_not_matching_the_cumulative_sum"),
    ("their_guards", "residue_source_violations"),
    ("their_guards", "residue_endpoint_violations"),
    ("their_guards", "quantile_jensen_violations"),
    ("their_guards", "quantile_markov_violations"),
    ("examples", "x_disagreeing"),
    ("examples", "z_disagreeing"),
    ("examples", "exponent_word_disagreeing"),
    ("examples", "h_disagreeing"),
    ("examples", "first_step_not_valuation_one"),
    ("examples", "laplace_sum_disagreeing"),
    ("examples", "excess_decimal_disagreeing"),
    ("examples", "phase_floor_disagreeing"),
    ("examples", "tail_not_suffix_supercritical"),
    ("examples", "geometry_violations"),
    ("records", "affine_identity_violations"),
    ("records", "laplace_identity_violations"),
    ("records", "phase_gap_violations"),
    ("records", "endpoint_outside_7_or_11_mod_12"),
    ("records", "endpoint_not_three_mod_four"),
    ("records", "suffix_not_supercritical"),
    ("entropy", "gap_not_shrinking"),
    ("entropy", "entropy_rate_above_beta"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "validation_digest_mismatches"),
    ("artifacts", "validation_size_mismatches"),
    ("artifacts", "validation_issue_entries"),
    ("artifacts", "validation_counts_disagreeing_with_the_report"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("bridges", "bridges"),
    ("bridges", "sources"),
    ("bridges", "suffixes_checked"),
    ("canonical", "bridges"),
    ("canonical", "both_inside_their_moduli"),
    ("canonical", "source_inside_its_modulus"),
    ("canonical", "endpoint_inside_its_modulus"),
    ("plateau", "bridges"),
    ("plateau", "quantile_instances"),
    ("area", "bridges"),
    ("area", "centre_of_mass_past_the_midpoint"),
    ("first_hit", "orbits"),
    ("first_hit", "first_hits"),
    ("their_guards", "residue_samples"),
    ("their_guards", "residue_endpoint_assert_fired"),
    ("their_guards", "quantile_samples"),
    ("their_guards", "quantile_jensen_guard_open"),
    ("examples", "examples"),
    ("records", "gaps"),
    ("records", "suffixes_checked"),
    ("entropy", "levels"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("bridges", "longest_tail"),
    ("bridges", "smallest_phase_gap_seen"),
    ("bridges", "integer_lift_zero"),
    ("bridges", "excess_floor_decided_by_the_float64_fudge"),
    ("canonical", "collapse_asserted_outside_the_moduli"),
    ("plateau", "jensen_weaker_bound_with_a_positive_right_side"),
    ("plateau", "quantile_instances_that_are_not_vacuous"),
    ("plateau", "sharp_quantile_instances_that_are_not_vacuous"),
    ("area", "centre_of_mass_undefined"),
    ("area", "centre_of_mass_exactly_at_the_midpoint"),
    ("first_hit", "length_bound_attained_with_no_additive_constant"),
    ("first_hit", "largest_n_with_the_source_outside"),
    ("first_hit", "source_inside_its_cylinder"),
    ("first_hit", "source_outside_its_cylinder"),
    ("first_hit", "endpoint_inside_its_cylinder"),
    ("first_hit", "endpoint_outside_its_cylinder"),
    ("their_guards", "residue_source_assert_fired"),
    ("their_guards", "quantile_bound_not_vacuous"),
    ("examples", "sources_appearing_more_than_once"),
    ("records", "sources"),
    ("records", "smallest_phase_gap_seen"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
    ("artifacts", "validation_entries_with_a_digest"),
    ("artifacts", "validation_compile_returncode"),
    ("artifacts", "validation_execution_returncode"),
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
    ap.add_argument("--limit", type=int, default=25000)
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
    res["bridges"] = check_bridges(a.limit)
    res["canonical"] = check_canonical(a.limit)
    res["plateau"] = check_plateau(a.limit)
    res["area"] = check_area(a.limit)
    res["first_hit"] = check_first_hit(min(a.limit, 4000))
    res["their_guards"] = check_their_guards()
    res["examples"] = check_examples(report)
    res["records"] = check_records(min(a.limit, 12000))
    res["entropy"] = check_entropy()
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
        "run": "RUN-045", "round": "A-U.2d.17", "bundle": str(bundle),
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
