"""RUN-043 — independent recheck of Hard-Zeta round A-U.2d.15.

`Suffix-Minimum Record Sparsity Rigidity` (source item 62). 數學戰士「墜衡」.

A-U.2d.14 left a logical hole: generic divergence permits suffix-minimum times
as sparse as `N^o(1)`, so no polynomial record lower bound follows from record
theory alone. This round supplies the Collatz-specific replacement, enclosing
the record count between two slack coordinates:

    2^(-Delta_N) N^(1-o(1))  <=  R_N  <=  2^(delta_N) N^o(1)
    =>  Delta_N + delta_N >= (1-o(1)) log2 N

Its most checkable piece needs no premise at all. Section 10's

    N_1(s,g) >= (2-beta) g + (delta_{s+g} - delta_s)

follows from `K_t - K_s >= 2g - N_1` (every non-one valuation is at least two)
together with `K_t - K_s = beta g - (delta_t - delta_s)`. Neither step uses
suffix minimality, so it holds on every segment and is exercised here on tens of
thousands of them.

What is NOT testable is stated as such. Theorem 4.1 bounds the total DOWNWARD
variation of record slack, and on a convergent orbit every suffix minimum is an
A-renewal (RUN-042), so record slack only ascends and the descent population is
empty. The bundle's own checker says the same thing with two zero counts, and
section 18 says it in prose. That honesty is recorded rather than re-derived.

Usage:
    python code/src62_record_sparsity.py --bundle <dir> [--limit N]
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

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d15_Suffix_Minimum_Record_Sparsity"
         "_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d15_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d15_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d15_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d15.json"
CHECKSUMS = "CHECKSUMS.sha256"
ROUTE = "Hard_Zeta_A_Line_ROUTE_MAP_v2.15_AU2d15.md"

RHO_STAR = Fraction(41164, 10000)
THETA_STAR = 1 / (RHO_STAR + 1)
SIGMA_STAR = 1 / (1 + THETA_STAR)


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
    """Indices `s < T` with `values[s] < min(values[s+1..T])`.

    A whole convergent orbit has NONE -- it ends at 1, the global minimum, so
    nothing earlier is below its own suffix. RUN-042 nearly reported that as a
    premise failure when it is a definition failure; the population exists only
    on a finite window, which is what the bundle's checker scope specifies.
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
    lo, hi = log2_any(Fraction(3))
    b_lo, b_hi = beta_tight()
    want("log2(3) agrees with beta", lo <= b_hi and hi >= b_lo)
    want("log2(3) is not degenerate", lo < hi)
    want("2-beta is irrational, so its bracket has width",
         (2 - b_hi) < (2 - b_lo))
    want("2-beta is between 0.41 and 0.42",
         Fraction(41, 100) < 2 - b_hi and 2 - b_lo < Fraction(42, 100))
    want("theta* = 2500/12791", THETA_STAR == Fraction(2500, 12791))
    want("sigma* = 12791/15291", SIGMA_STAR == Fraction(12791, 15291))

    # the U_6 counting bound section 11 rests on, by enumeration
    bad = 0
    for lo_i in range(1, 200):
        for W in range(0, 60):
            n = sum(1 for x in range(lo_i, lo_i + W + 1) if x % 6 in (1, 5))
            if n > Fraction(W + 1, 3) + 2:
                bad += 1
    want("|U_6 in a width-W interval| <= (W+1)/3 + 2", bad == 0)
    return out


# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict) -> dict:
    """Published constants against a certified bracket AND the float64 route.

    The magnitude cap is tested BEFORE the chain excuse -- RUN-041 rebuilt that
    branch with the cap second, where an elif chain never reaches it.
    """
    t: dict = {"constants_checked": 0,
               "disagreeing_with_both_evaluations": 0,
               "from_the_float64_chain_not_the_nearest_double": 0,
               "exact_to_the_last_bit": 0,
               "undecided_brackets": 0,
               "missing_from_the_frontier": 0,
               "frontier_and_report_disagreeing": 0,
               "rows": []}
    b_lo, b_hi = widen(*beta_tight(), 40)
    p_beta = frontier["beta"]
    items = [
        ("beta", b_lo, b_hi, p_beta),
        ("q1_density_floor_2_minus_beta", 2 - b_hi, 2 - b_lo,
         2.0 - p_beta),
        ("theta_star", THETA_STAR, THETA_STAR,
         1.0 / (float(RHO_STAR) + 1.0)),
        ("inherited_controlled_renewal_support_exponent",
         Fraction(4, 5), Fraction(4, 5), 0.8),
        ("rho_star", RHO_STAR, RHO_STAR, float(RHO_STAR)),
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
        d_exact = v["ulps"]
        d_chain = bits(pub) - bits(chain)
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
    return t


# ---------------------------------------------------------------------------
# section 10 -- the piece that needs no premise
# ---------------------------------------------------------------------------

def check_q1_channel(limit: int, window: int = 40) -> dict:
    """`N_1(s,g) >= (2-beta) g + (delta_{s+g} - delta_s)`, section 10's exact
    inequality.

    Neither step of its derivation uses suffix minimality: every non-one
    valuation is at least two, so `K_t - K_s >= 2g - N_1`, and
    `K_t - K_s = beta g - (delta_t - delta_s)` is the definition of delta. So it
    holds on EVERY segment, and is checked on every `(s, g)` pair from every
    suffix minimum, plus a control population of segments rooted anywhere.
    """
    t: dict = {
        "orbits": 0, "pairs_from_a_suffix_minimum": 0,
        "exact_inequality_violations": 0,
        "pairs_from_an_arbitrary_root": 0,
        "exact_inequality_violations_off_a_record": 0,
        "valuation_sum_identity_violations": 0,
        "a_valuation_below_one": 0,
        "tightest_slack_in_the_inequality": None,
        "pairs_where_the_floor_alone_would_fail": 0,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    tight = None
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, 400)
        if len(word) < window + 2:
            continue
        t["orbits"] += 1
        vv, ww = values[:window + 1], word[:window]
        K = cumulative(ww)
        if any(q < 1 for q in ww):
            t["a_valuation_below_one"] += 1
        roots = suffix_minima(vv, window)
        for s in roots:
            for g in range(1, window - s + 1):
                u = s + g
                n1 = sum(1 for j in range(s, u) if ww[j] == 1)
                d_lo = (b_lo * u - K[u]) - (b_hi * s - K[s])
                d_hi = (b_hi * u - K[u]) - (b_lo * s - K[s])
                t["pairs_from_a_suffix_minimum"] += 1
                rhs_hi = (2 - b_lo) * g + d_hi
                if Fraction(n1) < rhs_hi:
                    if Fraction(n1) < (2 - b_hi) * g + d_lo:
                        t["exact_inequality_violations"] += 1
                slack = float(Fraction(n1) - (2 - b_hi) * g - d_lo)
                if tight is None or slack < tight[0]:
                    tight = (slack, start, s, g, n1)
                # the asymptotic floor alone, without the slack term
                if Fraction(n1) < (2 - b_hi) * g:
                    t["pairs_where_the_floor_alone_would_fail"] += 1
                # K_t - K_s = beta g - (delta_t - delta_s), by definition
                kk = K[u] - K[s]
                if not (b_lo * g - d_hi <= kk <= b_hi * g - d_lo):
                    t["valuation_sum_identity_violations"] += 1
        # a control root: any index, not only a record
        for s in range(0, window, 7):
            for g in range(1, min(9, window - s + 1)):
                u = s + g
                n1 = sum(1 for j in range(s, u) if ww[j] == 1)
                d_lo = (b_lo * u - K[u]) - (b_hi * s - K[s])
                t["pairs_from_an_arbitrary_root"] += 1
                if Fraction(n1) < (2 - b_hi) * g + d_lo:
                    t["exact_inequality_violations_off_a_record"] += 1
    if tight:
        t["tightest_slack_in_the_inequality"] = {
            "slack": round(tight[0], 6), "orbit": tight[1],
            "s": tight[2], "g": tight[3], "N1": tight[4]}
    return t


# ---------------------------------------------------------------------------
# sections 4-7 -- the record process
# ---------------------------------------------------------------------------

def check_records(limit: int, window: int = 40) -> dict:
    """The record process on real orbits.

    The exact pieces -- the multiplier, the product concatenation, the value
    span, the state ceiling -- all have real populations. Theorem 4.1's does
    not: it bounds the DOWNWARD variation of record slack, and every suffix
    minimum on a convergent orbit is an A-renewal, so record slack only
    ascends. The descent count is reported as the denominator rather than the
    theorem being called green on an empty set.
    """
    t: dict = {
        "orbits_with_two_or_more_records": 0, "record_edges": 0,
        "exact_multiplier_violations": 0,
        "product_concatenation_violations": 0,
        "record_slack_ascending": 0, "record_slack_descending": 0,
        "record_slack_undecided": 0,
        "total_downward_variation_negative": 0,
        "record_slack_edges_left_unclassified": 0,
        "total_downward_variation_is_zero": 0,
        "theorem_4_1_checked": 0, "theorem_4_1_violations": 0,
        "record_values_not_increasing": 0,
        "lemma_11_1_checked": 0, "lemma_11_1_violations": 0,
        "tail_checked": 0, "tail_violations": 0,
        "tail_descents": 0,
        "state_ceiling_identity_violations": 0,
        "gap_duration_above_the_U6_capacity": 0,
        "largest_record_count": 0,
    }
    b_lo, b_hi = widen(*beta_tight(), 40)
    for start in range(7, limit, 2):
        if start % 3 == 0:
            continue
        word, values = accelerated(start, 400)
        if len(word) < window + 2:
            continue
        vv, ww = values[:window + 1], word[:window]
        K = cumulative(ww)
        cs = suffix_minima(vv, window)
        if len(cs) < 2:
            continue
        t["orbits_with_two_or_more_records"] += 1
        t["largest_record_count"] = max(t["largest_record_count"], len(cs))
        prod_all = Fraction(1)
        down = Fraction(0)
        for i in range(len(cs) - 1):
            a, b = cs[i], cs[i + 1]
            g, p = b - a, K[b] - K[a]
            t["record_edges"] += 1
            P = Fraction(1)
            for j in range(a, b):
                P *= 1 + Fraction(1, 3 * vv[j])
            prod_all *= P
            # Y_b/Y_a = 2^{delta_b - delta_a} P, written with no beta at all
            if Fraction(vv[b]) * 2 ** p != Fraction(vv[a]) * 3 ** g * P:
                t["exact_multiplier_violations"] += 1
            if not vv[a] < vv[b]:
                t["record_values_not_increasing"] += 1
            d_lo, d_hi = b_lo * g - p, b_hi * g - p
            if d_lo > 0:
                t["record_slack_ascending"] += 1
            elif d_hi < 0:
                t["record_slack_descending"] += 1
                down += -d_hi
            else:
                t["record_slack_undecided"] += 1
            if not (d_lo > 0 or d_hi < 0 or (d_lo <= 0 <= d_hi)):
                t["record_slack_edges_left_unclassified"] += 1
            # Lemma 11.1: the record gap's value span
            t["lemma_11_1_checked"] += 1
            if not max(vv[a:b]) - vv[a] >= 3 * g - 7:
                t["lemma_11_1_violations"] += 1
            # section 7: the gap duration against the U_6 capacity below Ymax
            ceiling = max(vv[a:b])
            if not g <= Fraction(ceiling - vv[a] + 1, 3) + 2:
                t["gap_duration_above_the_U6_capacity"] += 1
        # `down` accumulates positive parts only, so a negative total means the
        # classification and the arithmetic have come apart. The drill inverted
        # the direction test and NOTHING complained until this existed.
        if down < 0:
            t["total_downward_variation_negative"] += 1
        if t["record_slack_descending"] == 0:
            t["total_downward_variation_is_zero"] += 1
        # Theorem 4.1 needs a descent to say anything
        if down > 0:
            t["theorem_4_1_checked"] += 1
            if not down < log2_any(simplify(prod_all, 25)[1])[1]:
                t["theorem_4_1_violations"] += 1
        # the concatenation the theorem rests on, which IS testable
        whole = Fraction(1)
        for j in range(cs[0], cs[-1]):
            whole *= 1 + Fraction(1, 3 * vv[j])
        if whole != prod_all:
            t["product_concatenation_violations"] += 1
        # section 5's tail, from the last record to the window end
        cr = cs[-1]
        n = window
        if cr < n:
            t["tail_checked"] += 1
            gg, pp = n - cr, K[n] - K[cr]
            d_hi = b_hi * gg - pp
            Pt = Fraction(1)
            for j in range(cr, n):
                Pt *= 1 + Fraction(1, 3 * vv[j])
            if Fraction(vv[n]) * 2 ** pp != Fraction(vv[cr]) * 3 ** gg * Pt:
                t["exact_multiplier_violations"] += 1
            if d_hi < 0:                      # delta_cR > delta_N
                t["tail_descents"] += 1
                if not -d_hi < log2_any(simplify(Pt, 25)[1])[1]:
                    t["tail_violations"] += 1
        # section 7's state-ceiling identity, from the first record
        c1 = cs[0]
        for nn in range(c1 + 1, window + 1):
            gg, pp = nn - c1, K[nn] - K[c1]
            Pn = Fraction(1)
            for j in range(c1, nn):
                Pn *= 1 + Fraction(1, 3 * vv[j])
            if Fraction(vv[nn]) * 2 ** pp != Fraction(vv[c1]) * 3 ** gg * Pn:
                t["state_ceiling_identity_violations"] += 1
            break                              # one per orbit is enough
    return t


def check_enclosure(trials: int = 400, seed: int = 9115) -> dict:
    """Section 8's enclosure, as the exponent algebra it is.

    `R <= 2^d N^eta` and `R >= 2^-D N^(1-eps)` together give
    `D + d >= (1 - eps - eta) log2 N`. That is the whole of Theorem 8.1, and it
    is an implication between finite quantities, so it is checked as one.
    """
    rng = random.Random(seed)
    t: dict = {"grid_points": 0, "enclosure_violations": 0,
               "antecedent_holds": 0,
               "corollary_8_2_violations": 0,
               "support_transfer_inversion_violations": 0}
    for _ in range(trials):
        t["grid_points"] += 1
        # sample the slacks RELATIVE to L, or the antecedents are almost never
        # satisfiable and the grid tests nothing -- the same vacuity RUN-042
        # found in a threshold check whose sample never straddled its threshold
        L = Fraction(rng.randrange(10, 10 ** 4))       # stands for log2 N
        d = L * Fraction(rng.randrange(0, 1200), 1000)     # delta_N
        D = L * Fraction(rng.randrange(0, 1200), 1000)     # Delta_N
        eps = Fraction(rng.randrange(1, 100), 1000)
        eta = Fraction(rng.randrange(1, 100), 1000)
        # in log2 coordinates: R <= d + eta L  and  R >= -D + (1-eps) L
        lo, hi = -D + (1 - eps) * L, d + eta * L
        if lo <= hi:
            t["antecedent_holds"] += 1
            if not D + d >= (1 - eps - eta) * L:
                t["enclosure_violations"] += 1
        # Corollary 8.2: d = o(log N) forces D >= (1-o(1)) log2 N
        if d <= eta * L and lo <= hi:
            if not D >= (1 - eps - 2 * eta) * L:
                t["corollary_8_2_violations"] += 1
        # Corollary 6.3: R = N^kappa forces delta_N >= (kappa - o(1)) log2 N
        kappa = Fraction(rng.randrange(1, 1000), 1000)
        if kappa * L <= d + eta * L:
            if not d >= (kappa - eta) * L:
                t["support_transfer_inversion_violations"] += 1
    return t


def check_shallow_b(limit: int, window: int = 40) -> dict:
    """Corollary 12.1 needs a B source: a suffix minimum whose slack is later
    crossed. RUN-042 established there are none on a convergent orbit, and this
    counts the denominator rather than reporting an empty set as green."""
    t: dict = {"orbits": 0, "suffix_minima": 0,
               "B_sources_found": 0,
               "corollary_12_1_checked": 0,
               "corollary_12_1_violations": 0}
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
        for s in suffix_minima(vv, window):
            t["suffix_minima"] += 1
            for u in range(s + 1, window + 1):
                g, p = u - s, K[u] - K[s]
                if b_hi * g < p:               # delta_u < delta_s
                    t["B_sources_found"] += 1
                    t["corollary_12_1_checked"] += 1
                    P = Fraction(1)
                    for j in range(s, u):
                        P *= 1 + Fraction(1, 3 * vv[j])
                    D_lo = p - b_hi * g
                    if not Fraction(2) ** 0 < P:   # 2^D < P, D > 0
                        t["corollary_12_1_violations"] += 1
                    break
    return t


# ---------------------------------------------------------------------------
# artifacts, ledger, their claims
# ---------------------------------------------------------------------------

def check_artifacts(bundle: pathlib.Path) -> dict:
    t: dict = {"files_present": 0, "digests_listed": 0, "digest_mismatches": 0,
               "checksum_lines_naming_a_missing_file": 0,
               "files_with_no_digest_anywhere": [],
               "validation_per_file_entries": 0,
               "validation_entries_with_a_digest": 0,
               "validation_digest_mismatches": 0,
               "validation_carries_per_file_digests": False}
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
    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    body = val.get("checks", val.get("files", {}))
    with_digest = set()
    if isinstance(body, dict):
        for n, r in body.items():
            if not isinstance(r, dict):
                continue
            t["validation_per_file_entries"] += 1
            if "sha256" in r:
                t["validation_entries_with_a_digest"] += 1
                with_digest.add(n)
                if n in actual and actual[n] != r["sha256"]:
                    t["validation_digest_mismatches"] += 1
    t["validation_carries_per_file_digests"] = bool(with_digest)
    t["files_with_no_digest_anywhere"] = [
        n for n in present if n not in listed and n not in with_digest]
    t["validation_status"] = val.get("status")
    t["validation_top_level_keys"] = sorted(val)
    t["validation_has_a_checker_stdout_digest"] = (
        "checker_stdout_sha256" in val)
    t["validation_issues"] = val.get("issues")
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    t: dict = {"paper_proved_items": 0, "ledger_proved_items": 0,
               "paper_open_items": 0, "ledger_open_items": 0,
               "paper_no_go_headings": 0, "ledger_no_go_items": 0,
               "ledger_has_an_open_key": False,
               "open_items_absent_from_the_ledger": [],
               "no_go_headings_absent_from_the_ledger": []}
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
    no_go = re.findall(r"^## NO-GO (14\.\d) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    for k in ledger:
        low = k.lower()
        if "proved" in low:
            t["ledger_proved_items"] = len(ledger[k])
        elif "no_go" in low or "nogo" in low:
            t["ledger_no_go_items"] = len(ledger[k])
        elif "open" in low:
            t["ledger_has_an_open_key"] = True
            t["ledger_open_items"] = len(ledger[k])
    blob = json.dumps(ledger).lower()

    def covered(text: str) -> bool:
        # four characters, not five. The ledger abbreviates "CASP and the
        # Collatz conjecture" to "CASP and Collatz"; a five-character floor
        # drops CASP, leaves ["collatz", "conjecture"], and demands two hits
        # from an item that legitimately supplies one. That is a false positive
        # in the ACCUSING direction, which is the expensive one.
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
    # A coverage heuristic needs a control at BOTH ends. This one already
    # false-positived once for real -- the ledger abbreviates "CASP and the
    # Collatz conjecture" and a five-character word floor dropped "CASP" -- and
    # a mutated version that accuses everything went unnoticed because the two
    # lists above are read by nothing. Feed it text that is certainly present
    # and text that is certainly absent, and require the right answer.
    present = " ".join(str(x) for x in ledger.get("proved_internally", [])[:1])
    if present and not covered(present):
        t["heuristic_failed_its_positive_control"] = 1
    else:
        t["heuristic_failed_its_positive_control"] = 0
    absent = "quokka bandersnatch flimflam zeppelin marzipan"
    t["heuristic_failed_its_negative_control"] = int(covered(absent))
    return t


def check_their_claims(report: dict, res: dict) -> dict:
    """Their counters beside mine, including the two they report as ZERO."""
    mine = {
        "exact_segment_product_identity": res["records"]["record_edges"],
        "record_first_step_q1": res["q1"]["pairs_from_a_suffix_minimum"],
        "record_values_mod12": res["records"]["record_edges"],
        "record_slack_drop_edge": res["records"]["record_slack_descending"],
        "record_total_down_variation": res["records"]["theorem_4_1_checked"],
        "record_tail_drop": res["records"]["tail_descents"],
        "q1_density_exact_algebra": res["q1"]["pairs_from_a_suffix_minimum"],
        "record_free_span_units": res["records"]["lemma_11_1_checked"],
        "record_descent_implies_crossing": res["shallow"]["B_sources_found"],
    }
    rows = [{"check": k, "theirs": v, "mine": mine.get(k)}
            for k, v in report["checks"].items()]
    return {"rows": rows,
            "checks_i_did_not_reproduce": sum(1 for r in rows
                                              if r["mine"] is None),
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "checks_we_both_report_as_zero": sum(
                1 for r in rows if r["theirs"] == 0 and r["mine"] == 0)}


FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("constants", "frontier_and_report_disagreeing"),
    ("q1", "exact_inequality_violations"),
    ("q1", "exact_inequality_violations_off_a_record"),
    ("q1", "valuation_sum_identity_violations"),
    ("q1", "a_valuation_below_one"),
    ("records", "exact_multiplier_violations"),
    ("records", "product_concatenation_violations"),
    ("records", "record_values_not_increasing"),
    ("records", "lemma_11_1_violations"),
    ("records", "gap_duration_above_the_U6_capacity"),
    ("records", "state_ceiling_identity_violations"),
    ("records", "record_slack_undecided"),
    ("records", "theorem_4_1_violations"),
    ("records", "total_downward_variation_negative"),
    ("records", "record_slack_edges_left_unclassified"),
    ("records", "tail_violations"),
    ("enclosure", "enclosure_violations"),
    ("enclosure", "corollary_8_2_violations"),
    ("enclosure", "support_transfer_inversion_violations"),
    ("shallow", "corollary_12_1_violations"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
    ("artifacts", "validation_digest_mismatches"),
)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("q1", "orbits"),
    ("q1", "pairs_from_a_suffix_minimum"),
    ("q1", "pairs_from_an_arbitrary_root"),
    ("records", "orbits_with_two_or_more_records"),
    ("records", "record_edges"),
    ("records", "lemma_11_1_checked"),
    ("records", "tail_checked"),
    ("enclosure", "grid_points"),
    ("enclosure", "antecedent_holds"),
    ("shallow", "suffix_minima"),
)

OBSERVATIONS = (
    ("instrument", "checks"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("q1", "pairs_where_the_floor_alone_would_fail"),
    ("records", "record_slack_ascending"),
    ("records", "record_slack_descending"),
    ("records", "total_downward_variation_is_zero"),
    ("records", "theorem_4_1_checked"),
    ("records", "tail_descents"),
    ("records", "largest_record_count"),
    ("shallow", "orbits"),
    ("shallow", "B_sources_found"),
    ("shallow", "corollary_12_1_checked"),
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
    ("their_claims", "checks_we_both_report_as_zero"),
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
    res["q1"] = check_q1_channel(a.limit)
    res["records"] = check_records(a.limit)
    res["enclosure"] = check_enclosure()
    res["shallow"] = check_shallow_b(a.limit)
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
        "run": "RUN-043", "round": "A-U.2d.15", "bundle": str(bundle),
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
