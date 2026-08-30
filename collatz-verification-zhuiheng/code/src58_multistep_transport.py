"""RUN-039 — independent recheck of Hard-Zeta round A-U.2d.11.

`Multi-Step Reciprocal-Transport Rigidity` (source item 58). 數學戰士「墜衡」.

This is the most checkable round the sweep has been given, because its headline
number is backed by an **exact rational dual certificate** rather than by an
estimate. A level-`h` certificate is a positive potential `a_r` on the units mod
`3^h` and non-negative multipliers `mu_{r,k}` satisfying

    -3 a_r + 2^k a_{T(r,k)} + mu_{r,k} >= 1      for every r and every k >= 1,

with `T_h(r,k) = ((3r+1) 2^-k) mod 3^h`, and then Corollary 5.3 gives the product
exponent in closed form:

    alpha_h = (1/3) sum_{r,k} mu_{r,k} / (3^h 2^(k+1)).

Both halves are finite and rational. There is no tolerance to argue about, no
sampling, and no reference computation of my own that could be the wrong one --
the certificate either satisfies its inequalities or it does not, and `alpha`
either equals the published rational or it does not. That is checked here for
all three shipped levels, including the tail: beyond some `K` the inequality
holds for free because `2^K a_min - 3 a_max >= 1`, and `K` is computed rather
than assumed.

Section 3's transport identity and section 4's channel capacity are likewise
exact and are checked on real orbits. Theorem 5.2 needs `z > y`, which no real
segment satisfies, so it is measured and premise-gated as at RUN-037/038.

Brackets come from `src53`, `src54` and `src55`, certified there.

Usage:
    python code/src58_multistep_transport.py --bundle <dir> [--limit N] [--out F]
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
from src55_orbit_packing_deficit import beta_tight, syracuse, v2    # noqa: E402

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d11_Multi_Step_Reciprocal_Transport"
         "_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d11_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d11_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d11_theorem_ledger.json"
CERTS = "Hard_Zeta_AU2d11_transport_certificates.json"
VALIDATION = "SOURCE_VALIDATION_AU2d11.json"
CHECKSUMS = "CHECKSUMS.sha256"
BUILDER = "build_AU2d11_artifacts.py"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


_LN: dict[Fraction, tuple[Fraction, Fraction]] = {}


def ln_cached(x: Fraction) -> tuple[Fraction, Fraction]:
    """`ln_bracket` memoised. RUN-038 spent 85 of 88 seconds on an eighty-term
    series called once per segment; here it is called eighteen times per
    segment, once per certificate multiplier."""
    if x not in _LN:
        _LN[x] = ln_bracket(x)
    return _LN[x]


def pow_frac(x: Fraction, p: int, q: int, hi: bool = False) -> Fraction:
    """`x^(p/q)` for `x >= 1`, via `exp((p/q) ln x)`, rigorously bracketed.

    NOT by integer power and root: this round's exponents are `1373/25856` and
    `25856/24483`, and `_pow_bracket` would raise to the 1373rd power and then
    bisect a 25856-th root of a number with a thousand digits. That is what put
    this gate past eight minutes. Through the logarithm both brackets stay
    small, and both halves are already certified.
    """
    if x < 1:
        # `ln_bracket` and `_exp_bracket` both want non-negative arguments, so
        # take the reciprocal and flip which end of the bracket is wanted.
        return 1 / pow_frac(1 / x, p, q, not hi)
    l_lo, l_hi = ln_cached(x)
    e = Fraction(p, q)
    return _exp_bracket(e * l_hi)[1] if hi else _exp_bracket(e * l_lo)[0]


def transition(r: int, k: int, M: int) -> int:
    """`T_h(r,k) = ((3r+1) 2^-k) mod M`, exactly."""
    return ((3 * r + 1) * pow(pow(2, k, M), -1, M)) % M


# ---------------------------------------------------------------------------
# the certificates -- the round's headline, and entirely decidable
# ---------------------------------------------------------------------------

def check_certificates(certs: dict, report: dict) -> dict:
    t = {
        "levels": 0, "inequalities_checked": 0,
        "certificate_inequality_violations": 0,
        "potentials_not_positive": 0,
        "multipliers_negative": 0,
        "residues_with_no_potential": 0,
        "transitions_leaving_the_unit_group": 0,
        "multipliers_beyond_the_declared_tail": 0,
        "levels_where_the_computed_tail_exceeds_the_declared_one": 0,
        "alpha_disagreeing_with_corollary_5_3": 0,
        "A_not_three_times_alpha": 0,
        "report_disagreeing_with_the_certificate_file": 0,
        "rows": [],
    }
    for level in sorted(certs, key=int):
        c = certs[level]
        M = c["modulus"]
        a = {int(r): Fraction(v) for r, v in c["potential_a"].items()}
        mu = {tuple(int(x) for x in key.split(",")): Fraction(v)
              for key, v in c["mu_nonzero"].items()}
        tail = c["tail_k"]
        units = [r for r in range(M) if r % 3]
        t["levels"] += 1

        t["residues_with_no_potential"] += sum(1 for r in units if r not in a)
        t["potentials_not_positive"] += sum(1 for v in a.values() if v <= 0)
        t["multipliers_negative"] += sum(1 for v in mu.values() if v < 0)
        t["multipliers_beyond_the_declared_tail"] += sum(
            1 for (_r, k) in mu if k > tail)
        if any(r not in a for r in units):
            continue

        # `T` must land back in the unit group, or the transport is not closed
        for r in units:
            for k in range(1, 40):
                if transition(r, k, M) % 3 == 0:
                    t["transitions_leaving_the_unit_group"] += 1

        # the tail: past K the inequality holds from `2^k a_T` alone
        a_min, a_max = min(a.values()), max(a.values())
        K = 1
        while 2 ** K * a_min - 3 * a_max < 1:
            K += 1
        if K > tail:
            t["levels_where_the_computed_tail_exceeds_the_declared_one"] += 1

        upper = max(K, tail) + 5
        viol = 0
        for r in units:
            for k in range(1, upper + 1):
                lhs = (-3 * a[r] + 2 ** k * a[transition(r, k, M)]
                       + mu.get((r, k), Fraction(0)))
                t["inequalities_checked"] += 1
                if lhs < 1:
                    viol += 1
        t["certificate_inequality_violations"] += viol

        alpha = sum(v / (M * 2 ** (k + 1)) for (_r, k), v in mu.items()) / 3
        pub_alpha = Fraction(c["product_exponent_alpha"])
        pub_A = Fraction(c["reciprocal_log_coefficient_A"])
        if alpha != pub_alpha:
            t["alpha_disagreeing_with_corollary_5_3"] += 1
        if pub_A != 3 * alpha:
            t["A_not_three_times_alpha"] += 1
        rc = report.get("exact_certificates", {}).get(level, {})
        if (rc.get("alpha") and Fraction(rc["alpha"]) != pub_alpha) or \
                (rc.get("A") and Fraction(rc["A"]) != pub_A) or \
                (rc.get("modulus") not in (None, M)) or \
                (rc.get("tail_k") not in (None, tail)):
            t["report_disagreeing_with_the_certificate_file"] += 1
        t["rows"].append({
            "level": int(level), "modulus": M, "units": len(units),
            "multipliers": len(mu), "declared_tail_k": tail,
            "tail_settles_from_k": K,
            "inequalities": len(units) * upper,
            "violations": viol,
            "alpha": "%d/%d" % (alpha.numerator, alpha.denominator),
            "alpha_float": float(alpha)})
    # the strongest certified alpha, and the gain over A-U.2d.10
    best = min((Fraction(c["product_exponent_alpha"]) for c in certs.values()),
               default=None)
    t["strongest_certified_alpha"] = ("%d/%d" % (best.numerator, best.denominator)
                                      if best else None)
    t["the_report_agrees_on_the_strongest"] = (
        best is not None
        and Fraction(report.get("strongest_certified_alpha", "0")) == best)
    eta = Fraction(4, 45) - best if best else None
    t["eta11_recomputed"] = ("%d/%d" % (eta.numerator, eta.denominator)
                             if eta else None)
    t["eta11_matches_the_reported_float"] = (
        eta is not None
        and float(eta) == report.get("additional_deficit_vs_alpha10"))
    t["the_certified_exponents_decrease_with_level"] = [
        r["alpha"] for r in t["rows"]] == sorted(
        (r["alpha"] for r in t["rows"]),
        key=lambda s: -Fraction(s)) if t["rows"] else None
    return t


# ---------------------------------------------------------------------------
# section 3 -- exact finite-state reciprocal transport, on real orbits
# ---------------------------------------------------------------------------

def check_transport(limit: int, M: int) -> dict:
    t = {"orbits": 0, "segments": 0, "max_L": 0,
         "residue_identities_checked": 0,
         "transport_identity_violations": 0,
         "segments_meeting_the_endpoint_premise_z_above_y": 0,
         "states_outside_the_unit_group": 0}
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        t["orbits"] += 1
        for s in range(1, n):
            end = e[s]
            if end is None or end <= s:
                continue
            L, y, z = end - s, values[s], values[end]
            t["segments"] += 1
            t["max_L"] = max(t["max_L"], L)
            if z > y:
                t["segments_meeting_the_endpoint_premise_z_above_y"] += 1
            for j in range(s, end + 1):
                if values[j] % 3 == 0:
                    t["states_outside_the_unit_group"] += 1
            # S_b over sources, S_{r,k} over channels, C_b over targets
            S_b: dict[int, Fraction] = {}
            S_rk: dict[tuple[int, int], Fraction] = {}
            C_b: dict[int, Fraction] = {}
            for j in range(s, end):
                r, k = values[j] % M, word[j]
                S_b[r] = S_b.get(r, Fraction(0)) + Fraction(1, values[j])
                S_rk[(r, k)] = S_rk.get((r, k), Fraction(0)) + Fraction(1, values[j])
                tb = values[j + 1] % M
                C_b[tb] = C_b.get(tb, Fraction(0)) + Fraction(
                    1, values[j] * values[j + 1])
            for b in range(M):
                if b % 3 == 0:
                    continue
                t["residue_identities_checked"] += 1
                lhs = 3 * S_b.get(b, Fraction(0)) - sum(
                    2 ** k * v for (r, k), v in S_rk.items()
                    if transition(r, k, M) == b)
                rhs = (Fraction(3, y) if y % M == b else Fraction(0)) \
                    - (Fraction(3, z) if z % M == b else Fraction(0)) \
                    - C_b.get(b, Fraction(0))
                if lhs != rhs:
                    t["transport_identity_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# section 4 -- the channel is one residue class modulo 3^h 2^(k+1)
# ---------------------------------------------------------------------------

def check_channel(levels: tuple[int, ...] = (1, 2, 3)) -> dict:
    t = {"channels_checked": 0,
         "channels_not_selecting_exactly_one_class": 0,
         "modulus_disagreeing_with_3h_2k1": 0,
         "capacity_windows": 0, "capacity_violations": 0}
    for h in levels:
        M = 3 ** h
        for k in range(1, 7):
            t["channels_checked"] += 1
            D = M * 2 ** (k + 1)
            for r in range(M):
                if r % 3 == 0:
                    continue
                cls = {n % D for n in range(1, 8 * D, 2)
                       if n % M == r and v2(3 * n + 1) == k}
                if len(cls) != 1:
                    t["channels_not_selecting_exactly_one_class"] += 1
                    break
            if D != 3 ** h * 2 ** (k + 1):
                t["modulus_disagreeing_with_3h_2k1"] += 1
            # members of one class, all >= y, have reciprocal mass under H
            for y in (7, 25, 121):
                t["capacity_windows"] += 1
                base = next(n for n in range(y, y + 8 * D, 2)
                            if n % M != 0 and n % M % 3 and v2(3 * n + 1) == k
                            and n % 3) if True else y
                members = [base + i * D for i in range(min(60, 4000 // 1))][:60]
                mass = sum(Fraction(1, m) for m in members)
                L = len(members)
                bound = Fraction(1, y) + ln_cached(1 + Fraction(D * L, y))[1] / D
                if mass > bound:
                    t["capacity_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# sections 5 and 8 -- the certified mass bound and the uniform envelope
# ---------------------------------------------------------------------------

def check_mass_and_product(limit: int, certs: dict,
                           C11_lo: Fraction, C11_hi: Fraction) -> dict:
    c = certs["3"]
    M = c["modulus"]
    a = {int(r): Fraction(v) for r, v in c["potential_a"].items()}
    mu = {tuple(int(x) for x in key.split(",")): Fraction(v)
          for key, v in c["mu_nonzero"].items()}
    a_max = max(a.values())
    alpha = Fraction(c["product_exponent_alpha"])

    t = {"segments": 0, "low_source_segments_7_le_y_le_L": 0,
         "segments_meeting_the_endpoint_premise": 0,
         "theorem_5_2_checked": 0, "theorem_5_2_violations": 0,
         "uniform_envelope_violations": 0,
         "max_L": 0}
    for start in range(3, limit + 1, 2):
        word, values = accelerated(start)
        K = cumulative(word)
        n = len(word)
        e, _ = crossings_and_stalks(K, n)
        for s in range(1, n):
            end = e[s]
            if end is None or end <= s:
                continue
            L, y, z = end - s, values[s], values[end]
            t["segments"] += 1
            t["max_L"] = max(t["max_L"], L)
            script = Fraction(1)
            for j in range(s, end):
                script *= 1 + Fraction(1, 3 * values[j])
            if 7 <= y <= L:
                t["low_source_segments_7_le_y_le_L"] += 1
                ratio_hi = pow_frac(Fraction(L, y), alpha.numerator,
                                    alpha.denominator, hi=True)
                if script > C11_hi * ratio_hi:
                    t["uniform_envelope_violations"] += 1
            if z <= y:
                continue
            t["segments_meeting_the_endpoint_premise"] += 1
            t["theorem_5_2_checked"] += 1
            Stot = sum(Fraction(1, values[j]) for j in range(s, end))
            rhs = Fraction(51, 14) * a_max / y
            for (r, k), v in mu.items():
                D = M * 2 ** (k + 1)
                rhs += v * (Fraction(1, y)
                            + ln_cached(1 + Fraction(D * L, y))[1] / D)
            if Stot > rhs:
                t["theorem_5_2_violations"] += 1
    return t


def check_hierarchy(report: dict, certs: dict) -> dict:
    """Section 12's floating hierarchy is a DIAGNOSTIC and says so."""
    t = {"rows_checked": 0,
         "rows_where_the_exponent_is_not_the_coefficient_over_three": 0,
         "rows_not_decreasing_in_h": 0,
         "certified_levels_disagreeing_with_the_diagnostic": 0,
         "the_report_labels_them_diagnostics_only": False}
    diag = report.get("diagnostics", {}).get(
        "floating_lp_hierarchy_not_proof", {})
    prev = None
    for h in sorted(diag, key=int):
        row = diag[h]
        t["rows_checked"] += 1
        if abs(row["reciprocal_coeff"] / 3 - row["product_exponent"]) > 1e-15:
            t["rows_where_the_exponent_is_not_the_coefficient_over_three"] += 1
        if prev is not None and row["product_exponent"] >= prev:
            t["rows_not_decreasing_in_h"] += 1
        prev = row["product_exponent"]
        if h in certs:
            exact = Fraction(certs[h]["product_exponent_alpha"])
            if abs(float(exact) - row["product_exponent"]) > 1e-12:
                t["certified_levels_disagreeing_with_the_diagnostic"] += 1
            if row["modulus"] != certs[h]["modulus"]:
                t["certified_levels_disagreeing_with_the_diagnostic"] += 1
    warn = report.get("scope_warning", "").lower()
    t["the_report_labels_them_diagnostics_only"] = (
        "diagnostic" in warn and "not proof" in
        " ".join(report.get("diagnostics", {}).keys()).lower().replace("_", " "))
    return t


# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict, paper: str, certs: dict,
                    beta_lo: Fraction, beta_hi: Fraction) -> dict:
    c = certs["3"]
    M = c["modulus"]
    a = {int(r): Fraction(v) for r, v in c["potential_a"].items()}
    mu = {tuple(int(x) for x in key.split(",")): Fraction(v)
          for key, v in c["mu_nonzero"].items()}
    a_max, sum_mu = max(a.values()), sum(mu.values())
    alpha = Fraction(c["product_exponent_alpha"])
    theta = 1 / (Fraction("4.1164") + 1)
    mu11 = (theta - alpha) / (1 - alpha)

    # C11 = exp( ( (sum mu)/7 + sum mu ln(1+D)/D + 51 a_max/98 ) / 3 )
    inner_lo = sum_mu / 7 + Fraction(51, 98) * a_max
    inner_hi = Fraction(inner_lo)
    for (_r, k), v in mu.items():
        D = M * 2 ** (k + 1)
        lo, hi = ln_bracket(Fraction(1 + D))
        inner_lo += v * lo / D
        inner_hi += v * hi / D
    C11_lo, C11_hi = widen(*_exp_bracket_pair(inner_lo / 3, inner_hi / 3))
    C11r_lo, C11r_hi = C11_lo / 6, C11_hi / 6
    c11_lo = pow_frac(1 / C11r_hi, 25856, 24483)
    c11_hi = pow_frac(1 / C11r_lo, 25856, 24483, hi=True)

    pub = dict(frontier)
    rows = {}
    for name, lo, hi, form in (
        ("C11_uniform_product", C11_lo, C11_hi,
         "exp(((sum mu)/7 + sum mu ln(1+D)/D + 51 a_max/98)/3)"),
        ("C11_depth", C11r_lo, C11r_hi, "C11/6"),
        ("c11_source_inversion", c11_lo, c11_hi, "(C11/6)^(-25856/24483)"),
    ):
        if name in pub:
            rows[name] = dict(ulps_against_bracket(pub[name], lo, hi),
                              published=pub[name], closed_form=form,
                              recomputed=bracket_decimal(lo, hi, 20))
    for name, exact, form in (
        ("theta_star", theta, "1/(rho+1)"),
        ("alpha_mod3", Fraction(certs["1"]["product_exponent_alpha"]), "7/80"),
        ("alpha_mod9", Fraction(certs["2"]["product_exponent_alpha"]), "99/1472"),
        ("alpha_mod27", alpha, "1373/25856"),
        ("alpha10", Fraction(4, 45), "4/45"),
        ("eta11", Fraction(4, 45) - alpha, "4/45 - alpha_27"),
        ("dense_root_source_floor_exponent_mu11", mu11,
         "(theta-alpha)/(1-alpha) = %d/%d" % (mu11.numerator, mu11.denominator)),
    ):
        if name in pub:
            rows[name] = {"published": pub[name], "closed_form": form,
                          "decided": True, "nearest_double": float(exact),
                          "ulps": bits(pub[name]) - bits(float(exact)),
                          "recomputed": None}
    drifted = sorted(k for k, v in rows.items() if v.get("ulps"))
    exact_strings = {
        "alpha_mod27_exact": str(alpha) == pub.get("alpha_mod27_exact"),
        "A_mod27_exact": str(3 * alpha) == pub.get("A_mod27_exact"),
        "eta11_exact": str(Fraction(4, 45) - alpha) == pub.get("eta11_exact"),
    }
    af = float(alpha)
    chain = {
        "C11_depth_is_the_published_C11_over_six_as_doubles":
            pub.get("C11_uniform_product", 0) / 6 == pub.get("C11_depth"),
        "c11_is_the_published_C11_depth_to_the_minus_25856_over_24483":
            pub.get("C11_depth", 1) ** (-25856 / 24483)
            == pub.get("c11_source_inversion"),
        "mu11_is_the_float64_theta_and_alpha_put_through_the_formula":
            (1 / (4.1164 + 1) - af) / (1 - af)
            == pub.get("dense_root_source_floor_exponent_mu11"),
    }
    # `P_RF >= 6^(1/15) 12^(1/45) (L/y)^(4/45)`, so the relative deficit
    # constant is `C11 / (6^(1/15) 12^(1/45))`.
    den_lo = _nth_root_lo(Fraction(6), 15, 40) * _nth_root_lo(Fraction(12), 45, 40)
    den_hi = _nth_root_hi(Fraction(6), 15, 40) * _nth_root_hi(Fraction(12), 45, 40)
    crel_lo, crel_hi = C11_lo / den_hi, C11_hi / den_lo
    mus = {"mu8_from_AU2d8": Fraction(1, 6), "mu9_from_AU2d9": Fraction(1, 9),
           "mu10_from_AU2d10": Fraction(4, 45)}
    refs = {"C11_uniform_product": (C11_lo, C11_hi),
            "relative_deficit_vs_P_RF": (crel_lo, crel_hi),
            "alpha_mod3": (Fraction(certs["1"]["product_exponent_alpha"]),) * 2,
            "alpha_mod9": (Fraction(certs["2"]["product_exponent_alpha"]),) * 2,
            "alpha10": (Fraction(4, 45), Fraction(4, 45)),
            **{n: ((theta - al) / (1 - al),) * 2 for n, al in mus.items()},
            "C11_depth": (C11r_lo, C11r_hi),
            "c11_source_inversion": (c11_lo, c11_hi),
            "alpha_mod27": (Fraction(alpha), Fraction(alpha)),
            "eta11": (Fraction(4, 45) - alpha, Fraction(4, 45) - alpha),
            "mu11": (Fraction(mu11), Fraction(mu11)),
            "theta_star": (Fraction(theta), Fraction(theta)),
            "beta": (beta_lo, beta_hi)}
    inline, unidentified = {}, []
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
        v = dict(decimal_verdict(shown, ref), published=shown)
        rank = {"exact to every published digit": 0,
                "correctly rounded at the last digit": 1,
                "truncated rather than rounded at the last digit": 2,
                "OVER-PUBLISHED": 3}
        if name not in inline or rank.get(v["verdict"], 3) > rank.get(
                inline[name]["verdict"], 3):
            inline[name] = v
    return {
        "rows": rows, "off_by_at_least_one_ulp": drifted,
        "exact_rational_strings_reproduce": exact_strings,
        "the_derivation_chain_in_float64": chain,
        "inline_decimals_in_the_paper": inline,
        "published_decimals_this_run_could_not_identify": unidentified,
        "relative_deficit_vs_P_RF_recomputed": bracket_decimal(crel_lo, crel_hi, 16),
        "_C11": (C11_lo, C11_hi),
    }


def _exp_bracket_pair(lo: Fraction, hi: Fraction) -> tuple[Fraction, Fraction]:
    return _exp_bracket(lo)[0], _exp_bracket(hi)[1]


def check_ledger(ledger: dict, paper: str) -> dict:
    """The paper's section 17 against the JSON ledger, by NAMED keys.

    The first version matched section labels to ledger keys by substring, which
    is the kind of guess that turns a naming choice into a reported shortfall.
    Each section is paired with its key explicitly, and any key the earlier
    rounds carried but this one does not is reported as absent rather than
    silently skipped -- that is the finding here, not a count.
    """
    def block(a: str, b: str) -> str:
        return paper[paper.index(a):paper.index(b)]

    counts = {
        "17.1 proved internally": (
            len(re.findall(r"^(\d+)\. ", block("## 17.1 Proved internally",
                                              "## 17.2 Inherited"), re.M)),
            "proved_internal"),
        "17.2 inherited": (
            len(re.findall(r"^- ", block("## 17.2 Inherited",
                                         "## 17.3 External"), re.M)),
            "inherited_internal"),
        "17.3 external grounding": (
            len(re.findall(r"^- ", block("## 17.3 External",
                                         "## 17.4 Diagnostic"), re.M)),
            "external_grounding"),
        "17.4 diagnostic / explicitly open": (
            len(re.findall(r"^- ", block("## 17.4 Diagnostic",
                                         "# 18. Checker scope"), re.M)),
            "diagnostic_only"),
    }
    table, differ = [], []
    for label, (n, key) in counts.items():
        got = len(ledger[key]) if isinstance(ledger.get(key), list) else None
        table.append({"paper_section": label, "paper_items": n,
                      "ledger_key": key, "ledger_items": got,
                      "shortfall": (n - got) if got is not None else None})
        if got is not None and got != n:
            differ.append(label)

    # Every earlier round's ledger carried a list of open problems. This one
    # names its section "Diagnostic / explicitly open" and ships only the
    # diagnostics, so the open items -- the Collatz conjecture among them --
    # have no machine-readable record at all.
    expected_keys = ("proved_internal", "inherited_internal",
                     "external_grounding", "diagnostic_only", "no_go")
    open_like = [k for k in ledger if "open" in k.lower()]
    no_go = re.findall(r"^## NO-GO (\d+\.\d+) — (.+)$", paper, re.M)
    return {
        "table": table, "sections_where_the_counts_differ": differ,
        "ledger_keys": sorted(k for k in ledger if isinstance(ledger[k], list)),
        "expected_keys_absent": [k for k in expected_keys if k not in ledger],
        "the_ledger_carries_a_list_of_open_problems": bool(open_like),
        "paper_no_go_headings": len(no_go),
        "ledger_no_go_entries": len(ledger.get("no_go", [])),
        "no_go_shortfall": len(no_go) - len(ledger.get("no_go", [])),
        "no_go_headings_in_the_paper": [n for n, _ in no_go],
    }


def check_artifacts(bundle: pathlib.Path) -> dict:
    validation = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = validation.get("files", {})
    sv_names = sorted(files) if isinstance(files, dict) else []
    sv_digests = {n: r["sha256"] for n, r in files.items()
                  if isinstance(r, dict) and "sha256" in r} \
        if isinstance(files, dict) else {}
    cs = {}
    for line in (bundle / CHECKSUMS).read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            cs[name.strip()] = digest
    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()
              for n in present}
    return {
        "files_in_the_bundle": len(present),
        "listed_in_CHECKSUMS": len(cs),
        "listed_in_the_validation_record": len(sv_names),
        "validation_records_carrying_a_digest": len(sv_digests),
        "validation_record_fields": sorted(
            next(iter(files.values()))) if sv_names else [],
        "CHECKSUMS_mismatches": sorted(n for n, d in cs.items()
                                       if actual.get(n) != d),
        "validation_record_mismatches": sorted(n for n, d in sv_digests.items()
                                               if actual.get(n) != d),
        "in_the_validation_record_but_not_CHECKSUMS":
            sorted(set(sv_names) - set(cs)),
        "files_with_no_digest_anywhere":
            sorted(n for n in present if n not in cs and n not in sv_digests),
        "the_builder_is_shipped": BUILDER in present,
        "the_builder_has_a_digest": BUILDER in cs or BUILDER in sv_digests,
        "the_record_says_all_pass": validation.get("all_pass"),
        "a_stdout_transcript_is_shipped": any(
            p.endswith(".txt") and "stdout" in p for p in present),
    }


def check_their_claims(report: dict, res: dict) -> dict:
    ce, tr, ch = res["certificates"], res["transport"], res["channel"]
    mapping = {
        "dual_inequalities_exact":
            ce["certificate_inequality_violations"] == 0
            and ce["inequalities_checked"] > 0,
        "residue_transport_equalities_exact":
            tr["transport_identity_violations"] == 0
            and tr["residue_identities_checked"] > 0,
        "harmonic_capacity_tests":
            ch["capacity_violations"] == 0
            and ch["channels_not_selecting_exactly_one_class"] == 0,
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
    if transition(1, 1, 3) != ((3 * 1 + 1) * pow(2, -1, 3)) % 3:
        failed.append("the_transition_disagrees_with_its_own_definition")
    if pow(2, -1, 27) != 14 or (2 * 14) % 27 != 1:
        failed.append("the_modular_inverse_is_wrong")
    if syracuse(7) != 11 or v2(24) != 3:
        failed.append("a_hand_computed_value_disagrees")
    if _pow_bracket(Fraction(8), 1, 3) > 2 or _pow_bracket(
            Fraction(8), 1, 3, hi=True) < 2:
        failed.append("the_cube_root_of_eight_does_not_contain_two")
    # `pow_frac`'s reciprocal branch is only reached for `x < 1`, which the
    # subject never supplies, so without this it is never exercised at all.
    #
    # The test value must have an IRRATIONAL answer. The first version asked
    # for `(1/4)^(1/2) = 1/2`, which is exactly representable at the widening
    # denominator, so both ends of the bracket collapsed onto it and swapping
    # them was undetectable. `(1/2)^(1/2)` is irrational, so the two ends are
    # genuinely distinct and an orientation bug shows up.
    q_lo = pow_frac(Fraction(1, 2), 1, 2)
    q_hi = pow_frac(Fraction(1, 2), 1, 2, hi=True)
    if not q_lo < q_hi:
        failed.append("pow_frac_returns_an_inverted_bracket_below_one")
    if not q_lo ** 2 <= Fraction(1, 2) <= q_hi ** 2:
        failed.append("pow_frac_of_a_half_does_not_bracket_its_own_square")
    return {"checks": 10, "failed": failed}


# ---------------------------------------------------------------------------

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
    certs = json.loads((bundle / CERTS).read_text(encoding="utf-8"))

    ln2_lo, ln2_hi = ln2_bracket()
    beta_lo, beta_hi = beta_tight()

    res: dict = {
        "tool": "src58_multistep_transport.py",
        "round": report.get("round"),
        "orbit_limit": args.limit,
        "instrument": {"brackets_from": "src53, src54 and src55, certified there"},
    }
    res["instrument_selfcheck"] = check_instrument(beta_lo, beta_hi, ln2_lo, ln2_hi)
    res["certificates"] = check_certificates(certs, report)
    res["constants"] = check_constants(frontier, report, paper, certs,
                                       beta_lo, beta_hi)
    C11_lo, C11_hi = res["constants"].pop("_C11")
    res["transport"] = check_transport(args.limit, 27)
    res["channel"] = check_channel()
    res["mass_and_product"] = check_mass_and_product(args.limit, certs,
                                                     C11_lo, C11_hi)
    res["hierarchy"] = check_hierarchy(report, certs)
    res["ledger"] = check_ledger(ledger, paper)
    res["artifacts"] = check_artifacts(bundle)
    res["their_claims"] = check_their_claims(report, res)

    ce, tr, ch = res["certificates"], res["transport"], res["channel"]
    mp, hi, art = res["mass_and_product"], res["hierarchy"], res["artifacts"]
    failures = ["instrument.%s" % n
                for n in res["instrument_selfcheck"]["failed"]]
    for key in ("certificate_inequality_violations", "potentials_not_positive",
                "multipliers_negative", "residues_with_no_potential",
                "transitions_leaving_the_unit_group",
                "multipliers_beyond_the_declared_tail",
                "levels_where_the_computed_tail_exceeds_the_declared_one",
                "alpha_disagreeing_with_corollary_5_3",
                "A_not_three_times_alpha",
                "report_disagreeing_with_the_certificate_file"):
        if ce[key]:
            failures.append("certificates.%s = %d" % (key, ce[key]))
    if not ce["the_report_agrees_on_the_strongest"]:
        failures.append("certificates: the report's strongest alpha disagrees")
    if not ce["eta11_matches_the_reported_float"]:
        failures.append("certificates: eta11 does not match the reported float")
    for key in ("transport_identity_violations", "states_outside_the_unit_group"):
        if tr[key]:
            failures.append("transport.%s = %d" % (key, tr[key]))
    for key in ("channels_not_selecting_exactly_one_class",
                "modulus_disagreeing_with_3h_2k1", "capacity_violations"):
        if ch[key]:
            failures.append("channel.%s = %d" % (key, ch[key]))
    for key in ("theorem_5_2_violations", "uniform_envelope_violations"):
        if mp[key]:
            failures.append("mass_and_product.%s = %d" % (key, mp[key]))
    for key in ("rows_where_the_exponent_is_not_the_coefficient_over_three",
                "rows_not_decreasing_in_h",
                "certified_levels_disagreeing_with_the_diagnostic"):
        if hi[key]:
            failures.append("hierarchy.%s = %d" % (key, hi[key]))
    for key, ok in res["constants"]["exact_rational_strings_reproduce"].items():
        if not ok:
            failures.append("constants: %s does not reproduce" % key)
    for key in ("CHECKSUMS_mismatches", "validation_record_mismatches"):
        if art[key]:
            failures.append("artifacts.%s = %s" % (key, art[key]))
    if res["their_claims"]["independently_contradicted"]:
        failures.append("their_claims: %s"
                        % res["their_claims"]["independently_contradicted"])

    guards = []
    if ce["levels"] < 3:
        guards.append("only %d certificate levels read" % ce["levels"])
    if ce["inequalities_checked"] < 200:
        guards.append("only %d certificate inequalities checked"
                      % ce["inequalities_checked"])
    if tr["residue_identities_checked"] < 20000:
        guards.append("only %d residue transport identities checked"
                      % tr["residue_identities_checked"])
    if tr["segments"] < 5000:
        guards.append("too few segments: %d" % tr["segments"])
    if ch["channels_checked"] < 12:
        guards.append("only %d channels checked" % ch["channels_checked"])
    if mp["low_source_segments_7_le_y_le_L"] < 100:
        guards.append("the low-source regime is barely attained: %d"
                      % mp["low_source_segments_7_le_y_le_L"])
    if 0 < mp["theorem_5_2_checked"] < 200:
        guards.append("theorem 5.2 was applied to %d segments: too few to have "
                      "tested it, too many to call it untested"
                      % mp["theorem_5_2_checked"])
    if hi["rows_checked"] < 5:
        guards.append("only %d hierarchy rows read" % hi["rows_checked"])
    if not hi["the_report_labels_them_diagnostics_only"]:
        guards.append("the floating hierarchy is not labelled diagnostic-only")
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
    empty = [r["paper_section"] for r in res["ledger"]["table"]
             if r["paper_items"] < 1]
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
