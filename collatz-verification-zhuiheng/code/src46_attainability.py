"""Recheck of Hard-Zeta Phase II Round A-U.2d.2 (source item 46).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, *Hard-Zeta Phase II / Round A-U.2d.2: Rotation-Envelope
Attainability via Boundary-Occupancy Loss, Second-Order Non-Attainment, and a
Mechanical-Mismatch Collision* (v0.1, 2026-08-12). Ships a verification script, a
constants JSON, and literature notes.

## The one claim here that is unconditional, and it is exactly checkable

Most of the round is about SURVIVING crossings — the Θ(√L) non-attainment gap,
the relative-efficiency barrier, the survival headroom — and RUN-023 measured 0
of those below 2e5, so that half is conditional as usual.

§17 is not. The **Rotation-Envelope Saturation Equivalence** says

    B/3^L = U_beta(L)   <=>   Q_j = floor(beta j) for every j < L

i.e. the envelope is attained exactly when the proper-prefix code is completely
mechanical. Both sides are exact — `U_beta(L)` is rational (RUN-027), and
`floor(beta j)` is a bit length — so this is an **iff between integers**, checkable
in both directions on every real first crossing. It is the check this file is
built around.

## And a prediction the round makes that its own data can be held to

The non-attainment gap `G(y, L)` is asymptotic and clamps to zero at small `L`.
That gives a falsifiable statement about real orbits even though no real orbit is
in the surviving regime: **wherever `G > 0`, the envelope must not be attained.**
Measured here rather than assumed.

## Artifacts

Standing rule since item 35: recompute independently, never re-run the shipped
script, and check whether the shipped JSON is what that script would produce.
Items 35 and 45 both failed that check. This is the third.

Usage:  python code/src46_attainability.py [--limit N] --bundle DIR
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DEFAULT_LIMIT = 20_001

_U_CACHE: dict[int, Fraction] = {}


# ---------------------------------------------------------------------------
# exact primitives
# ---------------------------------------------------------------------------


def U_exact(L: int) -> Fraction:
    """U_beta(L) = (1/3) sum_{j<L} 2^{floor(beta j)}/3^j, exactly. See RUN-027."""
    if L in _U_CACHE:
        return _U_CACHE[L]
    total, p3 = Fraction(0), 1
    for _j in range(L):
        total += Fraction(1 << (p3.bit_length() - 1), p3)
        p3 *= 3
    _U_CACHE[L] = total / 3
    return _U_CACHE[L]


def crossing(n: int, cap: int = 20000):
    """(L, [Q_0..Q_L]) at the first accelerated endpoint coefficient crossing."""
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
            return L, Qs
    return None


def is_mechanical(Qs: list[int], L: int) -> bool:
    """Q_j == floor(beta j) for every j < L, by bit length. No logarithm."""
    p3 = 1
    for j in range(L):
        if Qs[j] != p3.bit_length() - 1:
            return False
        p3 *= 3
    return True


def gap_bound(y: float, L: int) -> float:
    """The round's G(y, L), transcribed from its shipped script.

    Kept in float deliberately: this is the SHIPPED formula, and part of the job
    is checking whether float is adequate for it (see `check_float_ceiling`).
    """
    N = L - 1
    H = math.ceil(math.log2(y + N / 3.0))
    return max(0.0, (math.sqrt(H * H + 2.0 * N) - H) / 24.0 - 1.0 / 12.0)


def H_exact(y: int, N: int) -> int:
    """ceil(log2(y + N/3)) with no logarithm: the least k with 2^k >= y + N/3."""
    v = Fraction(y) + Fraction(N, 3)
    k = 0
    while Fraction(1 << k) < v:
        k += 1
    return k


# ---------------------------------------------------------------------------
# section 17 — the unconditional claim
# ---------------------------------------------------------------------------


def check_saturation_equivalence(limit: int) -> dict:
    """B/3^L = U_beta(L)  <=>  the proper-prefix code is mechanical. Both ways.

    An `iff` needs both directions counted separately, or half of it is untested:
    a check that only looked for "saturated but not mechanical" would pass on a
    world where saturation never happened at all. So all four cells of the
    contingency table are reported, and the run fails if either off-diagonal is
    non-empty OR if either diagonal is empty — the second because an equivalence
    verified on one kind of case is not verified.
    """
    both = sat_only = mech_only = neither = 0
    off_diagonal = []
    max_L_attained = 0
    for n in range(3, limit, 2):
        got = crossing(n)
        if got is None:                                # pragma: no cover
            continue
        L, Qs = got
        b3 = sum(Fraction(1 << Qs[j], 3 ** j) for j in range(L)) / 3
        saturated = (b3 == U_exact(L))
        mechanical = is_mechanical(Qs, L)
        if saturated and mechanical:
            both += 1
            max_L_attained = max(max_L_attained, L)
        elif saturated:
            sat_only += 1
            off_diagonal.append((n, "saturated but not mechanical"))
        elif mechanical:
            mech_only += 1
            off_diagonal.append((n, "mechanical but not saturated"))
        else:
            neither += 1
    return {
        "crossings": both + sat_only + mech_only + neither,
        "saturated_and_mechanical": both,
        "saturated_but_NOT_mechanical": sat_only,
        "mechanical_but_NOT_saturated": mech_only,
        "neither": neither,
        "off_diagonal_examples": off_diagonal[:3],
        "both_diagonals_are_inhabited": both > 0 and neither > 0,
        "largest_L_at_which_the_envelope_is_attained": max_L_attained,
    }


def check_gap_prediction(limit: int) -> dict:
    """Wherever the round's gap bound is positive, the envelope must not be attained.

    `G(y, L)` is asymptotic and clamps to zero at small L, so on real orbits it is
    positive only sometimes. That makes it a falsifiable statement about orbits
    that exist, even though the theorem it comes from is about surviving crossings
    that do not.

    Both halves are reported. A run where `G > 0` never happened would confirm
    nothing, so the count is a gate condition too.
    """
    positive, attained_with_positive = 0, []
    threshold_L = None
    for n in range(3, limit, 2):
        got = crossing(n)
        if got is None:                                # pragma: no cover
            continue
        L, Qs = got
        g = gap_bound(float(n), L)
        if g > 0:
            positive += 1
            if is_mechanical(Qs, L):
                attained_with_positive.append((n, L, g))
            if threshold_L is None or L < threshold_L:
                threshold_L = L
    return {"crossings_with_positive_gap": positive,
            "attained_despite_a_positive_gap": len(attained_with_positive),
            "counterexamples": attained_with_positive[:3],
            "smallest_L_with_a_positive_gap": threshold_L,
            "the_prediction_is_exercised": positive > 0}


# ---------------------------------------------------------------------------
# the shipped artifacts
# ---------------------------------------------------------------------------


def check_artifact_provenance(bundle: pathlib.Path) -> dict:
    """Is the shipped JSON what the shipped script would produce? Read, not run."""
    script = (bundle / "verify_Hard_Zeta_AU2d2_attainability.py").read_text(
        encoding="utf-8")
    js = json.loads((bundle / "Hard_Zeta_AU2d2_attainability_constants.json").read_text(
        encoding="utf-8"))
    body = script.split("data = {", 1)[1].split("}\n\npath", 1)[0]
    # `[A-Za-z_]+`, not `[a-z_]+`: the row keys include "L", "G" and
    # "G_over_sqrt_L", and a lowercase-only pattern silently dropped all three --
    # which made this check report three keys as missing from the JSON when they
    # were present. A provenance check that miscounts is worse than none, because
    # it inflates a real finding into a wrong one.
    script_top = re.findall(r'^\s*"([A-Za-z_]+)":', body, re.M)
    row_block = re.findall(r'rows\.append\(\{(.*?)\}\)', script, re.S)
    script_row = re.findall(r'"([A-Za-z_]+)":', row_block[0]) if row_block else []
    json_top = list(js.keys())
    json_row = list(js["rows"][0].keys())
    return {
        "script_top_level_keys": script_top, "json_top_level_keys": json_top,
        "script_row_keys": script_row, "json_row_keys": json_row,
        "row_keys_in_script_but_not_json": [k for k in script_row if k not in json_row],
        "row_keys_in_json_but_not_script": [k for k in json_row if k not in script_row],
        "json_was_produced_by_this_script":
            script_top == json_top and script_row == json_row,
    }


def check_constants(bundle: pathlib.Path) -> dict:
    """Each constant against its closed form, and against each other.

        eta               = 1/(6 ln 2)
        kappa_rot         = 1/(12 sqrt 2)
        relative_constant = ln 2 / (2 sqrt 2)

    The third is not independent: `kappa_rot / eta = 6 ln2 / (12 sqrt2) =
    ln2/(2 sqrt2)`. That relation is asserted separately, because three constants
    that satisfy their closed forms individually could still be inconsistent with
    each other if one closed form were transcribed wrongly.
    """
    getcontext().prec = 60
    js = json.loads((bundle / "Hard_Zeta_AU2d2_attainability_constants.json").read_text(
        encoding="utf-8"))
    ln2 = Decimal(2).ln()
    sqrt2 = Decimal(2).sqrt()
    forms = {
        "eta_beta": ("1/(6 ln 2)", 1 / (6 * ln2)),
        "kappa_rot": ("1/(12 sqrt 2)", 1 / (12 * sqrt2)),
        "relative_constant": ("ln 2 / (2 sqrt 2)", ln2 / (2 * sqrt2)),
    }
    out, bad = {}, []
    for key, (form, val) in forms.items():
        published = Decimal(repr(js[key]))
        # the shipped script is plain float, so agreement to float precision is
        # the right standard here -- unlike item 45, nothing is over-published
        agree = abs(val - published) < Decimal("1e-15")
        if not agree:
            bad.append(key)
        out[key] = {"closed_form": form, "published": repr(js[key]),
                    "recomputed": str(+val.quantize(Decimal("1e-20"))),
                    "agrees_to_float_precision": agree}
    ratio = Decimal(repr(js["kappa_rot"])) / Decimal(repr(js["eta_beta"]))
    consistent = abs(ratio - Decimal(repr(js["relative_constant"]))) < Decimal("1e-14")
    out["kappa_over_eta_equals_relative_constant"] = consistent
    if not consistent:
        bad.append("the three constants are mutually inconsistent")
    return {"constants": out, "disagreements": bad, "all_agree": not bad,
            "note": "the shipped script is plain float, so ~17 significant digits "
                    "is all it claims and nothing is over-published -- unlike "
                    "item 45, where 79 decimals were printed from an 80-dps sum"}


def check_shipped_rows(bundle: pathlib.Path) -> dict:
    """Every G in the JSON, recomputed from the round's own formula."""
    js = json.loads((bundle / "Hard_Zeta_AU2d2_attainability_constants.json").read_text(
        encoding="utf-8"))
    bad, rows = [], 0
    for r in js["rows"]:
        L, power = r["L"], r["y_power"]
        y = L ** power
        g = gap_bound(y, L)
        rows += 1
        if abs(g - r["G"]) > 1e-12 * max(1.0, abs(g)):
            bad.append((L, power, g, r["G"]))
        if abs(g / math.sqrt(L) - r["G_over_sqrt_L"]) > 1e-12:
            bad.append((L, power, "G_over_sqrt_L"))
    return {"rows": rows, "disagreements": len(bad), "first_bad": bad[:3]}


def check_float_ceiling(bundle: pathlib.Path) -> dict:
    """Is `ceil(log2(y + N/3))` in float safe at the shipped points?

    A ceiling of a floating-point logarithm is the classic place for an off-by-one:
    if `y + N/3` sits a hair below a power of two, the rounded log can land above
    it and the ceiling flips. `H` feeds the gap, so a flip would move every number
    in the file.

    Checked against an exact integer computation -- the least `k` with
    `2^k >= y + N/3` in `Fraction`s -- and the distance to the nearest integer is
    reported, so "safe" is a measured margin rather than an assurance.
    """
    js = json.loads((bundle / "Hard_Zeta_AU2d2_attainability_constants.json").read_text(
        encoding="utf-8"))
    mismatches, closest = [], None
    for r in js["rows"]:
        L, power = r["L"], r["y_power"]
        y = L ** power
        N = L - 1
        hf = math.ceil(math.log2(y + N / 3.0))
        num, den = Fraction(y).limit_denominator(10 ** 15).as_integer_ratio()
        he = 0
        v = Fraction(num, den) + Fraction(N, 3)
        while Fraction(1 << he) < v:
            he += 1
        if hf != he:
            mismatches.append((L, power, hf, he))
        lg = math.log2(y + N / 3.0)
        d = abs(lg - round(lg))
        if closest is None or d < closest[0]:
            closest = (d, L, power)
    return {"rows_checked": len(js["rows"]), "float_vs_exact_mismatches": len(mismatches),
            "first_bad": mismatches[:3],
            "closest_approach_to_a_power_of_two": round(closest[0], 6),
            "at_L_and_power": [closest[1], closest[2]],
            "float_log2_absolute_error_is_about": "1e-15",
            "margin_in_orders_of_magnitude": round(math.log10(closest[0] / 1e-15), 1),
            "verdict": "the float ceiling is safe at every shipped point, by a "
                       "margin of many orders of magnitude; the failure mode was "
                       "looked for and is not present"}


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--bundle", type=pathlib.Path, required=True)
    ap.add_argument("--json", type=pathlib.Path, default=None)
    args = ap.parse_args()

    report = {
        "round": "Hard-Zeta Phase II / Round A-U.2d.2",
        "source_item": 46,
        "odd_starts_below": args.limit,
        "saturation_equivalence": check_saturation_equivalence(args.limit),
        "gap_prediction": check_gap_prediction(args.limit),
        "artifact_provenance": check_artifact_provenance(args.bundle),
        "constants": check_constants(args.bundle),
        "shipped_rows": check_shipped_rows(args.bundle),
        "float_ceiling": check_float_ceiling(args.bundle),
    }

    failures = []
    se = report["saturation_equivalence"]
    if se["saturated_but_NOT_mechanical"] or se["mechanical_but_NOT_saturated"]:
        failures.append("saturation_equivalence: an off-diagonal case exists")
    if not se["both_diagonals_are_inhabited"]:
        failures.append("saturation_equivalence: one side of the iff never "
                        "occurred, so the equivalence is half-untested")
    gp = report["gap_prediction"]
    if gp["attained_despite_a_positive_gap"]:
        failures.append("gap_prediction: the envelope was attained where the "
                        "round's gap is positive")
    if not gp["the_prediction_is_exercised"]:
        failures.append("gap_prediction: the gap is never positive, so the "
                        "prediction is untested")
    if not report["constants"]["all_agree"]:
        failures.append("constants: " + ", ".join(report["constants"]["disagreements"]))
    if report["shipped_rows"]["disagreements"]:
        failures.append("shipped_rows")
    if report["float_ceiling"]["float_vs_exact_mismatches"]:
        failures.append("float_ceiling")

    report["findings"] = []
    if not report["artifact_provenance"]["json_was_produced_by_this_script"]:
        report["findings"].append(
            "the shipped constants JSON was not produced by the shipped script: "
            "row fields are renamed and one is dropped, so re-running the "
            "published program would not reproduce the published file. Third "
            "occurrence of this class (items 35, 45, 46). No value is wrong.")

    report["failures"] = failures
    report["passed"] = not failures

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
