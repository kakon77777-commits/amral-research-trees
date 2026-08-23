"""Recheck of Hard-Zeta Phase II Round A-U.2d.1 (source item 45).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Hard-Zeta Phase II / Round A-U.2d.1: Bi-Exact
Source–Endpoint Rigidity via an Irrational-Rotation Correction Cap, Endpoint-Gap
Quantization, and an Improved Diophantine Survival Gate* (v0.1, 2026-08-12),
shipped with a verification script, a constants JSON, and literature notes.

## The round sharpens something this arm already verified

RUN-023 checked A-U.2e.2's First-Crossing Correction Bound, which in the form
used here reads `B/3^L <= L/3`. This round replaces the universal constant `1/3`
with

    U_beta(L) := (1/3) * sum_{j<L} 2^{-{beta j}},     U_beta(L)/L -> 1/(6 ln 2),

because `Q_j` is an integer below `beta j`, hence at most `floor(beta j)`, hence
`delta_j >= {beta j}` termwise. The universal linear efficiency drops from
`0.3333...` to `0.2404...`.

## The observation that makes this checkable in integers

`U_beta(L)` looks like it needs high-precision reals, and the shipped script
computes it with `mpmath` at 80 digits. It does not need them:

    2^{-{beta j}} = 2^{floor(beta j) - beta j} = 2^{floor(beta j)} / 3^j,

since `2^{beta j} = 3^j`, and `floor(beta j)` is exactly `(3**j).bit_length()-1`.
So **`U_beta(L)` is a rational number**, and the whole Irrational-Rotation
Correction Cap is an exact inequality between rationals:

    B/3^L = (1/3) sum_{j<L} 2^{Q_j}/3^j   <=   (1/3) sum_{j<L} 2^{floor(beta j)}/3^j

which is termwise, from `Q_j <= floor(beta j)`. Nothing here is approximated, and
the check is stronger than the one the round ships.

## Artifacts are checked as artifacts

The bundle ships `verify_Hard_Zeta_AU2d1_rotation_correction.py` and
`Hard_Zeta_AU2d1_rotation_constants.json`. Standing rule in this tree since item
35: recompute independently, never re-run theirs, and check whether the shipped
JSON is what the shipped script would produce. Item 35 is why — there the two did
not match. See `check_artifact_provenance`.

Usage:  python code/src45_rotation_cap.py [--limit N] [--bundle DIR]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DEFAULT_LIMIT = 20_001
DIGITS = 80


# ---------------------------------------------------------------------------
# exact primitives
# ---------------------------------------------------------------------------


def floor_beta(j: int, p3: int | None = None) -> int:
    """floor(j * log2 3), exactly, as a bit length."""
    return (3 ** j).bit_length() - 1 if p3 is None else p3.bit_length() - 1


_U_CACHE: dict[int, Fraction] = {}


def U_exact(L: int) -> Fraction:
    """U_beta(L) = (1/3) sum_{j<L} 2^{-{beta j}}, as an EXACT rational.

    `2^{-{beta j}} = 2^{floor(beta j)} / 3^j`, so no logarithm and no
    floating-point number appears. The shipped script computes this in mpmath at
    80 digits; this route agrees with it (see `check_shipped_U`) and is exact.

    Only usable for MODERATE L: the denominator is 3^L, so at the largest
    convergent denominator this round checks (190537) it would be a 90000-digit
    rational and every addition a gcd on it. `U_high_precision` below carries
    those, and the two are compared where both are feasible.
    """
    if L in _U_CACHE:
        return _U_CACHE[L]
    total, p3 = Fraction(0), 1
    for _j in range(L):
        total += Fraction(1 << (p3.bit_length() - 1), p3)
        p3 *= 3
    _U_CACHE[L] = total / 3
    return _U_CACHE[L]


def U_high_precision(L: int, prec: int = 140) -> tuple[Decimal, int]:
    """U_beta(L) at high precision, by an exact-ratio recurrence.

    `t_j = 2^{-{beta j}}` satisfies `t_j = t_{j-1} * 2^{-gamma} * 2^[wrapped]`
    with `gamma = beta - 1`, and `2^{-gamma} = 2/3` exactly since `2^beta = 3`.
    So each step multiplies by **2/3 or 4/3** — both rational — and the only thing
    needing precision is the wrap decision `{beta(j-1)} + gamma >= 1`.

    A wrap decision closer to the boundary than the accumulated error is NOT
    guessed: it is counted and returned, so an unreliable run says so instead of
    producing a number. Returns (sum, undecidable_count).
    """
    ctx = getcontext()
    old_prec = ctx.prec
    ctx.prec = prec
    try:
        gamma = Decimal(3).ln() / Decimal(2).ln() - 1
        guard = Decimal(1).scaleb(-(prec - 30))       # generous error allowance
        frac = Decimal(0)
        t = Decimal(1)                                # t_0 = 2^{-0} = 1
        total = Decimal(0)
        undecidable = 0
        for _j in range(L):
            total += t
            nxt = frac + gamma
            if abs(nxt - 1) < guard:
                undecidable += 1
            if nxt >= 1:
                frac = nxt - 1
                t = t * 4 / 3
            else:
                frac = nxt
                t = t * 2 / 3
        return +(total / 3), undecidable
    finally:
        ctx.prec = old_prec


def first_crossing(n: int, cap: int = 20000):
    """(L, Q_L, [Q_0..Q_L], Y_{a+L}) at the first accelerated endpoint crossing."""
    y, Q, L, p3, Qs = n, 0, 0, 1, [0]
    while L < cap:
        L += 1
        t = 3 * y + 1
        v = (t & -t).bit_length() - 1
        Q += v
        p3 *= 3
        y = t >> v
        Qs.append(Q)
        if (1 << Q) > p3:
            return L, Q, Qs, y
    return None


def stern_brocot_convergents(max_q: int) -> list[int]:
    """Convergent denominators of log2(3), by exact integer mediant descent.

    `p/q < log2 3` is `2^p < 3^q`. A convergent ends a run of same-side mediants.
    Shares no code and no arithmetic with the shipped script's floating-point
    continued fraction, which is the point of computing it here at all.
    """
    lo, hi, rows = (1, 1), (2, 1), []
    while lo[1] + hi[1] <= max_q:
        m = (lo[0] + hi[0], lo[1] + hi[1])
        side = (1 << m[0]) < 3 ** m[1]
        rows.append((m, side))
        lo, hi = (m, hi) if side else (lo, m)
    out = []
    for i, (m, side) in enumerate(rows):
        if i + 1 < len(rows) and rows[i + 1][1] != side:
            out.append(m[1])
    return out


# ---------------------------------------------------------------------------
# the shipped artifacts, checked as artifacts
# ---------------------------------------------------------------------------


def check_artifact_provenance(bundle: pathlib.Path) -> dict:
    """Is the shipped JSON what the shipped script would produce?

    Not run — READ. The script's `out = {...}` literal names its top-level keys
    and its row keys; those are compared against the JSON's. A mismatch means the
    published numbers did not come from the published program, so re-running the
    program would not reproduce them.

    This exact class was found at item 35 (RUN-017), where a shipped JSON had a
    different row count and renamed fields from its shipped script while every
    number in it was correct. The numbers being right is not the same as the
    artifact being reproducible.
    """
    script = (bundle / "verify_Hard_Zeta_AU2d1_rotation_correction.py").read_text(
        encoding="utf-8")
    js = json.loads((bundle / "Hard_Zeta_AU2d1_rotation_constants.json").read_text(
        encoding="utf-8"))

    # keys the script's output literal assigns, read off the source
    import re
    body = script.split("out = {", 1)[1].split("}\n\npath", 1)[0]
    script_top = re.findall(r'^\s*"([a-z_]+)":', body, re.M)
    row_sample = re.findall(r'rows\.append\(\{(.*?)\}\)', script, re.S)
    row_cf = re.findall(r'cf_rows\.append\(\{(.*?)\}\)', script, re.S)
    script_sample_keys = re.findall(r'"([a-z_]+)":', row_sample[0]) if row_sample else []
    script_cf_keys = re.findall(r'"([a-z_]+)":', row_cf[0]) if row_cf else []

    json_top = list(js.keys())
    json_sample_keys = list(js["sample_rotation_sums"][0].keys())
    json_cf_keys = list(js.get("cf_denominator_checks", js.get(
        "continued_fraction_denominators", [{}]))[0].keys())

    missing_top = [k for k in script_top if k not in json_top]
    extra_top = [k for k in json_top if k not in script_top]
    return {
        "script_top_level_keys": script_top,
        "json_top_level_keys": json_top,
        "in_script_but_not_json": missing_top,
        "in_json_but_not_script": extra_top,
        "script_sample_row_keys": script_sample_keys,
        "json_sample_row_keys": json_sample_keys,
        "script_cf_row_keys": script_cf_keys,
        "json_cf_row_keys": json_cf_keys,
        "json_was_produced_by_this_script": (
            not missing_top and not extra_top
            and script_sample_keys == json_sample_keys
            and script_cf_keys == json_cf_keys),
        "note": "a mismatch is about provenance, not arithmetic: it means the "
                "shipped program is not what produced the shipped file, so "
                "re-running it would not reproduce it",
    }


def check_constants(bundle: pathlib.Path) -> dict:
    """Every constant in the JSON, recomputed to more digits than it publishes.

    Each has a closed form the round states, and each is recomputed from that form
    rather than copied:

        beta                     = log2 3
        eta_beta                 = 1/(6 ln 2)        (from (1/3) int_0^1 2^-x dx)
        six_ln2                  = 6 ln 2
        improved_sqrt_y_constant = sqrt(3) * ln 2

    `1/(6 (ln 2)^2)`, stated in the round's section 4 but not shipped in the JSON,
    is recomputed too so that the paper's printed digits have a check as well.
    """
    getcontext().prec = DIGITS + 40
    js = json.loads((bundle / "Hard_Zeta_AU2d1_rotation_constants.json").read_text(
        encoding="utf-8"))
    ln2 = Decimal(2).ln()
    ln3 = Decimal(3).ln()
    beta = ln3 / ln2
    forms = {
        "beta_log2_3": ("log2 3", beta),
        "eta_beta": ("1/(6 ln 2)", 1 / (6 * ln2)),
        "six_ln2": ("6 ln 2", 6 * ln2),
        "improved_sqrt_y_constant": ("sqrt(3) * ln 2", Decimal(3).sqrt() * ln2),
    }
    out, bad = {}, []
    for key, (form, val) in forms.items():
        published = js[key]
        n = len(published.split(".")[1])
        mine = str(+val.quantize(Decimal(1).scaleb(-n)))
        agree = mine == published
        if not agree:
            bad.append(key)
        out[key] = {"closed_form": form, "published_decimals": n,
                    "agrees_to_every_published_digit": agree,
                    "recomputed_head": mine[:24], "published_head": published[:24]}
    # the round prints this one in section 4 but does not ship it
    printed = Decimal("0.34689483016760")
    mine = 1 / (6 * ln2 * ln2)
    out["one_over_6_ln2_squared"] = {
        "closed_form": "1/(6 (ln 2)^2)", "printed_in_section_4": str(printed),
        "recomputed_head": str(+mine.quantize(Decimal(1).scaleb(-14))),
        "agrees_to_printed_digits":
            str(+mine.quantize(Decimal(1).scaleb(-14))) == str(printed),
        "shipped_in_json": False,
    }
    if not out["one_over_6_ln2_squared"]["agrees_to_printed_digits"]:
        bad.append("one_over_6_ln2_squared")
    return {"constants": out, "disagreements": bad, "all_agree": not bad}


def check_shipped_U(bundle: pathlib.Path) -> dict:
    """Every U in the JSON, against the EXACT rational value.

    The shipped script computes U in mpmath at 80 digits. This computes it as a
    rational and compares every published digit. Two routes, and only one of them
    can be wrong by rounding.
    """
    getcontext().prec = DIGITS + 60
    js = json.loads((bundle / "Hard_Zeta_AU2d1_rotation_constants.json").read_text(
        encoding="utf-8"))
    rows, over_published, materially_wrong = [], [], []
    for row in js["sample_rotation_sums"]:
        L = row["L"]
        exact = U_exact(L)
        pub = row["U"]
        n = len(pub.split(".")[1])
        mine = str(+(Decimal(exact.numerator) / Decimal(exact.denominator)
                     ).quantize(Decimal(1).scaleb(-n)))
        k = next((i for i, (a, b) in enumerate(zip(pub, mine)) if a != b), None)
        if k is None:
            correct = n
        else:
            # characters before the decimal point are not decimals
            correct = k - (pub.index(".") + 1)
            over_published.append(L)
            if correct < 20:
                materially_wrong.append(L)
        rows.append({"L": L, "published_decimals": n,
                     "decimals_actually_correct": correct,
                     "over_published_by": n - correct})
    return {"rows": rows,
            "values_with_incorrect_trailing_decimals": over_published,
            "values_wrong_in_the_first_20_decimals": materially_wrong,
            "all_agree": not over_published,
            "cause": "the shipped script computes these in mpmath at 80 dps and "
                     "the JSON prints up to 79 decimals; summing L terms at fixed "
                     "precision costs about log10(L) digits, so the tail of the "
                     "larger values is not supported by the computation that "
                     "produced it",
            "note": "recomputed here as an EXACT rational, so this side has no "
                    "rounding at all"}


def check_convergent_denominators(bundle: pathlib.Path) -> dict:
    """The JSON's q list, against an exact integer mediant descent.

    The shipped script derives them from a floating-point continued fraction of
    `beta - 1`. This derives them from `2^p < 3^q` comparisons. Agreement between
    two routes that share no arithmetic is the only reason to believe either.
    """
    js = json.loads((bundle / "Hard_Zeta_AU2d1_rotation_constants.json").read_text(
        encoding="utf-8"))
    published = [r["q"] for r in js["cf_denominator_checks"]]
    # The descent must run PAST the largest published denominator, or that
    # denominator's own run of same-side mediants is still open when the walk is
    # cut off and it is not recognised as a convergent. Same edge case as item
    # 43's convergent detection; the cure is to overshoot and then filter.
    mine = [q for q in stern_brocot_convergents(max(published) * 3)
            if 2 <= q <= max(published)]
    return {"published": published, "recomputed_exactly": mine,
            "agree": published == mine,
            "count": len(published)}


def check_denjoy_koksma(bundle: pathlib.Path) -> dict:
    """|U(q) - q*eta| <= Var(f) at every convergent denominator, TWO-SIDED.

    `f(x) = (1/3) 2^{-x}` extended 1-periodically. Its total variation over a
    period is NOT `(1/3)(1 - 1/2) = 1/6`: the periodic extension JUMPS at the
    integers, from `1/2` back up to `1`, so the variation is
    `(1/3)[(1 - 1/2) + (1 - 1/2)] = 1/3`. The shipped script uses `1/3` and is
    right; the factor-of-two trap is recorded here because getting it wrong in
    the tightening direction would have produced a check that fails on correct
    data.

    The shipped check is one-sided (`verified_upper`). This does both sides,
    which is strictly more.
    """
    getcontext().prec = DIGITS + 60
    js = json.loads((bundle / "Hard_Zeta_AU2d1_rotation_constants.json").read_text(
        encoding="utf-8"))
    ln2 = Decimal(2).ln()
    eta = 1 / (6 * ln2)
    # THE VARIATION, FROM ITS DEFINITION.
    #
    # f(x) = (1/3) 2^-x on [0,1), extended 1-periodically. Over one period it
    # decreases from 1/3 to 1/6, then JUMPS back up to 1/3 at the integer. Total
    # variation = (1/3 - 1/6) + (1/3 - 1/6) = 1/3.
    #
    # Asserting this matters more than it looks. The drill replaced 1/3 with 1/6
    # -- dropping the jump, which is the mistake I nearly made -- and THE GATE
    # STAYED GREEN, because the largest deviation over the shipped convergents is
    # about 0.139, below 1/6 = 0.1667. This data cannot catch that error, so the
    # constant is checked against its definition rather than against the data.
    # In FRACTIONS, not Decimals: `(1/3 - 1/6)*2` differs from `1/3` by an ulp at
    # any finite decimal precision, and an exact statement about a rational should
    # not be decided by rounding. The first version of this check compared
    # Decimals and reported the correct value as wrong.
    f0 = Fraction(1, 3)                       # f(0)
    f1 = Fraction(1, 6)                       # limit as x -> 1^-
    variation_exact = (f0 - f1) + (f0 - f1)   # descent + jump
    variation_from_definition_is_one_third = (variation_exact == Fraction(1, 3))
    variation = Decimal(variation_exact.numerator) / Decimal(
        variation_exact.denominator)
    upper_bad, lower_bad, rows = [], [], []
    worst = Decimal(0)
    cross_checked, cross_bad, undecided_total = 0, [], 0
    for r in js["cf_denominator_checks"]:
        q = r["q"]
        u, undecided = U_high_precision(q)
        undecided_total += undecided
        if q <= 400:
            # Both routes are feasible here, so run both and compare. Wrapped in
            # a guard because a BROKEN recurrence can return an absurd magnitude
            # and `quantize` then raises -- the drill found exactly that, and a
            # check that dies is not a check that failed. A disagreement so large
            # it cannot be quantised is still a disagreement.
            exact = U_exact(q)
            ex = +(Decimal(exact.numerator) / Decimal(exact.denominator)
                   ).quantize(Decimal(1).scaleb(-40))
            try:
                same = +u.quantize(Decimal(1).scaleb(-40)) == ex
            except Exception:
                same = False
            if not same:
                cross_bad.append(q)
            else:
                cross_checked += 1
        dev = u - q * eta
        if dev > variation:
            upper_bad.append(q)
        if dev < -variation:
            lower_bad.append(q)
        if abs(dev) > worst:
            worst = abs(dev)
        rows.append({"q": q, "deviation_head": str(dev)[:12]})
    return {"convergents_checked": len(rows),
            "exact_vs_high_precision_cross_checked": cross_checked,
            "exact_vs_high_precision_disagreements": len(cross_bad),
            "undecidable_wrap_decisions": undecided_total,
            "upper_violations": len(upper_bad), "lower_violations": len(lower_bad),
            "max_abs_deviation": str(worst)[:18],
            "variation_bound": str(variation)[:18],
            "two_sided": True,
            "variation_from_its_definition_is_one_third":
                variation_from_definition_is_one_third,
            "the_jump_is_half_the_variation": True,
            "this_data_cannot_catch_a_missing_jump":
                str(worst) < "0.1667",
            "margin_head": str(variation - worst)[:18],
            # How much of the allowance is actually used. The round cites a
            # SHARPNESS reference for Denjoy-Koksma; that result is metric (almost
            # every alpha) while this is one specific alpha, so tightness here is
            # a thing to measure rather than inherit.
            "fraction_of_the_bound_used": _safe_ratio(worst, variation)}


def _safe_ratio(worst: Decimal, variation: Decimal) -> str:
    """worst/variation, or a plain statement that it is off the scale.

    A broken recurrence produces a magnitude `quantize` cannot represent, and the
    drill found that twice: the gate DIED instead of reporting. A ratio too large
    to render is still information -- it is reported as such rather than raised.
    """
    try:
        return str(+(worst / variation).quantize(Decimal("0.0001")))
    except Exception:
        return ("off-scale: the deviation is too large to render, which is itself "
                "a failure of the bound")


# ---------------------------------------------------------------------------
# the round's core inequality, on real orbits
# ---------------------------------------------------------------------------


def check_rotation_cap(limit: int) -> dict:
    """B/3^L <= U_beta(L) at every real first crossing, exactly, and termwise.

    Both sides are rationals:
        B/3^L    = (1/3) sum_{j<L} 2^{Q_j}   / 3^j
        U_beta(L)= (1/3) sum_{j<L} 2^{floor(beta j)} / 3^j
    and the cap is termwise from `Q_j <= floor(beta j)`, which is the round's own
    argument. Both the aggregate inequality and the termwise one are checked, so
    a cap that held only by cancellation would show up.

    The improvement over the previous bound `L/3` is measured rather than
    asserted, and attainment is reported: a bound never reached would be a weaker
    claim than this one is.
    """
    cap_bad, term_bad = [], []
    attained = 0
    worst = Fraction(0)
    worst_n = None
    sum_ratio, count = Fraction(0), 0
    improvement = {}
    for n in range(3, limit, 2):
        got = first_crossing(n)
        if got is None:                                # pragma: no cover
            continue
        L, _Q, Qs, _z = got
        p3 = 1
        ok = True
        for j in range(L):
            if Qs[j] > p3.bit_length() - 1:
                term_bad.append((n, j))
                ok = False
                break
            p3 *= 3
        b3 = sum(Fraction(1 << Qs[j], 3 ** j) for j in range(L)) / 3
        u = U_exact(L)
        if b3 > u:
            cap_bad.append(n)
        r = b3 / u
        if r == 1:
            attained += 1
        if r > worst:
            worst, worst_n = r, n
        sum_ratio += r
        count += 1
        if L not in improvement:
            improvement[L] = float(u / Fraction(L, 3))
    shown = {str(L): round(improvement[L], 6)
             for L in sorted(improvement)[:1] + [k for k in (5, 10, 34, 100)
                                                 if k in improvement]}
    return {"crossings": count,
            "cap_violations": len(cap_bad), "first_bad": cap_bad[:3],
            "termwise_violations": len(term_bad), "first_termwise_bad": term_bad[:3],
            "max_B3_over_U": float(worst), "at_n": worst_n,
            "mean_B3_over_U": round(float(sum_ratio / count), 6) if count else None,
            "crossings_where_the_cap_is_ATTAINED": attained,
            "cap_is_attained": attained > 0,
            "U_over_L_third_by_L": shown,
            "asymptotic_improvement_factor": "1/(2 ln 2) = 0.7213...",
            }


def check_endpoint_gap(limit: int) -> dict:
    """B/3^L = (2^D - 1) y + 2^{D+1} h, with z - y = 2h, exactly.

    From `2^Q z = 3^L y + B` and `2^Q = 3^L 2^D`: `B/3^L = 2^D z - y`, and
    substituting `z = y + 2h` gives the quantized form. Cleared of the irrational
    `D` by writing `2^D = 2^Q/3^L`, so the whole identity is between rationals.

    `h >= 1` is asserted only where the round's hypothesis holds — `z > y` — and
    the count of real crossings where `z < y` is reported beside it, because on
    real orbits the endpoint usually DROPS and the round's setting does not apply.
    """
    bad, h_negative, h_at_least_one = [], 0, 0
    count = 0
    for n in range(3, min(limit, 20001), 2):
        got = first_crossing(n)
        if got is None:                                # pragma: no cover
            continue
        L, Q, Qs, z = got
        count += 1
        B = sum(3 ** (L - 1 - j) * (1 << Qs[j]) for j in range(L))
        b3 = Fraction(B, 3 ** L)
        two_d = Fraction(1 << Q, 3 ** L)
        if b3 != two_d * z - n:
            bad.append((n, "B/3^L != 2^D z - y"))
            continue
        h2 = z - n                                     # = 2h
        if h2 % 2 != 0:
            bad.append((n, "z - y is odd"))
            continue
        h = h2 // 2
        if b3 != (two_d - 1) * n + 2 * two_d * h:
            bad.append((n, "quantized form disagrees"))
            continue
        if h < 0:
            h_negative += 1
        elif h >= 1:
            h_at_least_one += 1
    return {"crossings": count, "violations": len(bad), "first_bad": bad[:3],
            "crossings_with_h_negative_endpoint_dropped": h_negative,
            "crossings_with_h_at_least_1": h_at_least_one,
            "note": "the round's h >= 1 needs z > y, which is the surviving case; "
                    "on real orbits the endpoint usually drops, and that count is "
                    "reported rather than filtered away"}


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--bundle", type=pathlib.Path, required=True,
                    help="directory holding the shipped script and constants JSON")
    ap.add_argument("--json", type=pathlib.Path, default=None)
    args = ap.parse_args()

    report = {
        "round": "Hard-Zeta Phase II / Round A-U.2d.1",
        "source_item": 45,
        "odd_starts_below": args.limit,
        "artifact_provenance": check_artifact_provenance(args.bundle),
        "constants": check_constants(args.bundle),
        "shipped_U_values": check_shipped_U(args.bundle),
        "convergent_denominators": check_convergent_denominators(args.bundle),
        "denjoy_koksma": check_denjoy_koksma(args.bundle),
        "rotation_cap": check_rotation_cap(args.limit),
        "endpoint_gap": check_endpoint_gap(args.limit),
    }

    failures = []
    if not report["constants"]["all_agree"]:
        failures.append("constants: " + ", ".join(report["constants"]["disagreements"]))
    if report["shipped_U_values"]["values_wrong_in_the_first_20_decimals"]:
        failures.append("shipped_U_values: a published value is wrong in its "
                        "leading decimals")
    if not report["convergent_denominators"]["agree"]:
        failures.append("convergent_denominators")
    dk = report["denjoy_koksma"]
    if dk["upper_violations"] or dk["lower_violations"]:
        failures.append("denjoy_koksma")
    if not dk["variation_from_its_definition_is_one_third"]:
        failures.append("denjoy_koksma: the variation does not match its own "
                        "definition")
    if dk["exact_vs_high_precision_disagreements"] or dk["undecidable_wrap_decisions"]:
        failures.append("denjoy_koksma: the two routes disagree, or a wrap "
                        "decision was too close to call")
    if not dk["exact_vs_high_precision_cross_checked"]:
        failures.append("denjoy_koksma: the high-precision route was never "
                        "compared against the exact one")
    rc = report["rotation_cap"]
    if rc["cap_violations"] or rc["termwise_violations"]:
        failures.append("rotation_cap")
    if not rc["cap_is_attained"]:
        failures.append("rotation_cap: never attained, so its tightness is unmeasured")
    if report["endpoint_gap"]["violations"]:
        failures.append("endpoint_gap")
    # provenance is a FINDING, not a gate failure: no number is wrong.
    report["findings"] = []
    su = report["shipped_U_values"]
    if su["values_with_incorrect_trailing_decimals"]:
        report["findings"].append(
            "the shipped JSON publishes more decimals than its own computation "
            "supports: the U values at L = %s have incorrect trailing decimals, "
            "by up to %d places. Every leading digit is right; the tail is "
            "accumulated rounding from summing L terms at 80 dps."
            % (", ".join(str(L) for L in su["values_with_incorrect_trailing_decimals"]),
               max(r["over_published_by"] for r in su["rows"])))
    if not report["artifact_provenance"]["json_was_produced_by_this_script"]:
        report["findings"].append(
            "the shipped constants JSON was not produced by the shipped script: "
            "fields are renamed and one top-level key is dropped, so re-running "
            "the published program would not reproduce the published file. This "
            "is about PROVENANCE and is separate from the precision finding "
            "above -- no value is wrong in any digit the computation supports")

    report["failures"] = failures
    report["passed"] = not failures

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
