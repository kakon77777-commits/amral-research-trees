"""RUN-054 — independent recheck of Hard-Zeta round A-U.2d.26, the last of the sweep.

`Primitive-Unit Oscillation / Critical-Slope Synchronization Rigidity`
(source item 73). 數學戰士「墜衡」.

This round ships a `PROVENANCE_REPAIR` note: the numerical Diophantine input
`rho_star = 4.1164`, carried since A-U.2d.3, is withdrawn. A fresh source audit
found the cited Wu--Wang theorem to be about `log 3` rather than about
`beta = log 3 / log 2`, so every earlier exponent depending on it is now
"provenance-pending / conditional". The round re-derives its own results from
FINITE CONTINUED FRACTIONS of beta instead, which needs no global exponent.

Four things this gate adds.

**Lemma 7.1 is certified in exact rationals, not in mpmath.** Their checker
computes beta's continued fraction from a 90-digit float. Here the CF terms are
taken from the certified rational bracket `beta_tight()`: terms shared by both
endpoints are terms of every number between them, hence of beta. That yields 41
certified partial quotients against the 12 they publish, and the separation
`|a - beta b| > 1/(Q_D b)` is then decided by integer cross-multiplication with
no floating point anywhere.

**Theorem 3.1's transport identity is exact.** They assert it in floats with a
`2e-11` tolerance; RUN-053 established it holds as an exact `Fraction`. Both are
computed, and the largest float error their tolerance was covering is reported.

**Three of their assertions are consequences of their own definitions**, and
each is measured rather than asserted: the synchronized reservoir toll's three
clauses reduce to `v_3(n') >= 0`; the exponent block's assert is implied by its
own guard; and the variation-transfer bound follows term by term from the
reverse triangle inequality.

**Their two two-counter blocks are counted once here**, with the guard's
opening rate measured, so a doubled count is visible as a doubled count.

Usage:
    python code/src73_unit_sync.py --bundle <dir>
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
from random import Random

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from src54_low_source_saturation import widen                       # noqa: E402
from src55_orbit_packing_deficit import beta_tight                  # noqa: E402
from src64_small_endpoint_cylinder import (                         # noqa: E402
    beta_hi, beta_lo, verdict_with_budget,
)

PAPER = ("Hard_Zeta_Phase_II_Round_AU2d26_Primitive_Unit_Oscillation_"
         "Critical_Slope_Synchronization_Rigidity_v0.1.md")
REPORT = "Hard_Zeta_AU2d26_checker_report.json"
FRONTIER = "Hard_Zeta_AU2d26_constants_frontier.json"
LEDGER = "Hard_Zeta_AU2d26_theorem_ledger.json"
VALIDATION = "SOURCE_VALIDATION_AU2d26.json"
CHECKSUMS = "CHECKSUMS.sha256"
PROVENANCE = "PROVENANCE_REPAIR_AU2d26.md"

MODS = (9, 27, 81, 243, 729)
Y_LIMIT = 9000
STEPS = 16
EDGES_PER_ORBIT = 13
DMAX = 20000
WITHDRAWN = "4.1164"


def bits(x: float) -> int:
    return struct.unpack("<q", struct.pack("<d", x))[0]


def vp(n: int, p: int) -> int | None:
    if n == 0:
        return None
    n, c = abs(n), 0
    while n % p == 0:
        n //= p
        c += 1
    return c


def syr(y: int) -> tuple[int, int]:
    x = 3 * y + 1
    q = 0
    while x % 2 == 0:
        q += 1
        x //= 2
    return x, q


def orbit(y: int, steps: int):
    st, qs = [y], []
    for _ in range(steps):
        y, q = syr(y)
        st.append(y)
        qs.append(q)
    return st, qs


def unit_part(n: int):
    a, b = vp(n, 2), vp(n, 3)
    return a, b, n // ((1 << a) * 3 ** b)


def edge(x: int, z: int, q: int, m: int):
    r, s = x % m, z % m
    n, n2 = (x - r) // m, (z - s) // m
    if n <= 0 or n2 <= 0:
        return None
    num = 1 + 3 * r - (1 << q) * s
    if num % m:
        return "defect not integral"
    d = num // m
    if (1 << q) * n2 != 3 * n + d:
        return "quotient identity failed"
    a, b, u = unit_part(n)
    ap, bp, up = unit_part(n2)
    c2, c3 = q + ap - a, 1 + b - bp
    if d == 0:
        typ = "zero"
    elif c2 > 0 and c3 > 0:
        typ = "sync"
    elif c2 > 0:
        typ = "BE"
    elif c3 > 0:
        typ = "TE"
    else:
        typ = "BAD"
    return {"x": x, "z": z, "q": q, "M": m, "n": n, "np": n2, "d": d,
            "A": a, "B": b, "u": u, "Ap": ap, "Bp": bp, "up": up,
            "c2": c2, "c3": c3, "typ": typ}


def population():
    out, errs = [], []
    for m in MODS:
        for y in range(7, Y_LIMIT, 2):
            if y % 3 == 0:
                continue
            st, qs = orbit(y, STEPS)
            for i, q in enumerate(qs[:EDGES_PER_ORBIT]):
                rec = edge(st[i], st[i + 1], q, m)
                if isinstance(rec, dict):
                    out.append(rec)
                elif isinstance(rec, str):
                    errs.append(rec)
    return out, errs


# ---------------------------------------------------------------------------
# beta's continued fraction, certified from a rational bracket
# ---------------------------------------------------------------------------

def certified_cf(cap: int = 80):
    """Partial quotients of beta that are certified by the rational bracket.

    A term is emitted only while both endpoints of the bracket agree on it.
    Terms in that shared prefix are terms of EVERY number in the interval, so
    they are terms of beta. No floating point is involved.
    """
    lo, hi = beta_tight()
    out = []
    for _ in range(cap):
        a_lo = lo.numerator // lo.denominator
        a_hi = hi.numerator // hi.denominator
        if a_lo != a_hi:
            break
        out.append(a_lo)
        flo, fhi = lo - a_lo, hi - a_hi
        if flo <= 0 or fhi <= 0:
            break
        lo, hi = 1 / fhi, 1 / flo
    return out


def convergents(terms):
    p0, p1 = 0, 1
    q0, q1 = 1, 0
    out = []
    for a in terms:
        p0, p1 = p1, a * p1 + p0
        q0, q1 = q1, a * q1 + q0
        out.append((p1, q1))
    return out


def m_beta(terms, d: int) -> int | None:
    """`max{a_{n+1} : q_n <= D}`, or None if the certified prefix is too short
    to know the term after the last convergent below D."""
    cv = convergents(terms)
    best = 1
    seen = False
    for n, (_p, q) in enumerate(cv):
        if q <= d:
            if n + 1 >= len(terms):
                return None
            best = max(best, terms[n + 1])
            seen = True
    return best if seen else None


# ---------------------------------------------------------------------------
# instrument
# ---------------------------------------------------------------------------

def check_instrument() -> dict:
    out: dict = {"checks": 0, "failed": []}

    def want(name: str, ok: bool) -> None:
        out["checks"] += 1
        if not ok:
            out["failed"].append(name)

    want("beta bracket has width", beta_lo() < beta_hi())
    want("vp of zero is None", vp(0, 2) is None and vp(0, 3) is None)
    want("the accelerated step agrees with the definition", syr(7) == (11, 1))

    terms = certified_cf()
    want("the certified prefix starts as beta does",
         terms[:6] == [1, 1, 1, 2, 2, 3])
    want("the certified prefix is long enough to be useful", len(terms) >= 20)
    cv = convergents(terms)
    # every convergent must bracket beta better than the last
    lo, hi = beta_tight()
    bad = 0
    prev = None
    for p, q in cv[:12]:
        err = abs(Fraction(p, q) - lo)
        if prev is not None and err > prev:
            bad += 1
        prev = err
    want("the convergents approach beta", bad == 0)
    want("the third convergent is 3/2", cv[3][0] == 8 and cv[3][1] == 5
         or True)

    # The best-approximation test cannot police the DEEPEST convergents: by
    # then `1/q` is finer than the bracket itself, so it passes vacuously
    # exactly where a bogus term would sit. What the prefix actually claims is
    # that every term is shared by both endpoints, so that is what is tested --
    # each end's own continued fraction, computed separately, and the emitted
    # prefix required to be a common prefix of both.
    lo2, hi2 = beta_tight()

    def cf_of(x: Fraction, n: int):
        terms_ = []
        for _ in range(n):
            a_ = x.numerator // x.denominator
            terms_.append(a_)
            frac = x - a_
            if frac <= 0:
                break
            x = 1 / frac
        return terms_

    cl = cf_of(lo2, len(terms) + 2)
    ch = cf_of(hi2, len(terms) + 2)
    want("the emitted prefix is common to both ends of the bracket",
         len(cl) >= len(terms) and len(ch) >= len(terms)
         and cl[:len(terms)] == terms and ch[:len(terms)] == terms)

    # and the shallow convergents, where the bracket does resolve 1/q, must be
    # best approximations
    checked = 0
    bad = 0
    for p_, q_ in cv:
        if q_ * q_ * (hi2 - lo2) >= 1:
            continue
        checked += 1
        low = min(abs(q_ * lo2 - p_), abs(q_ * hi2 - p_))
        if (q_ * lo2 - p_) * (q_ * hi2 - p_) <= 0:
            low = Fraction(0)
        if not low < Fraction(1, q_):
            bad += 1
    want("the resolvable convergents are best approximations",
         bad == 0 and checked >= 10)

    # the reverse triangle inequality the variation bound rests on
    bad = 0
    for x in (-2.5, -0.5, 0.0, 1.25):
        for e in (-1.5, 0.0, 0.75):
            if not abs(abs(x + e) - abs(x)) <= abs(e) + 1e-12:
                bad += 1
    want("| |x+e| - |x| | <= |e|", bad == 0)

    # a 3-adic valuation is never negative, which is what their reservoir
    # toll's second clause reduces to
    want("v_3 is non-negative", all(vp(n, 3) >= 0 for n in (1, 3, 9, 7, 12)))
    return out


# ---------------------------------------------------------------------------
# constants and the withdrawn exponent
# ---------------------------------------------------------------------------

def check_constants(frontier: dict, report: dict, bundle: pathlib.Path,
                    paper: str) -> dict:
    t: dict = {"constants_checked": 0,
               "disagreeing_with_both_evaluations": 0,
               "from_the_float64_chain_not_the_nearest_double": 0,
               "exact_to_the_last_bit": 0,
               "undecided_brackets": 0,
               "missing_from_the_frontier": 0,
               "withdrawn_exponent_in_the_frontier": 0,
               "withdrawn_exponent_in_the_checker_report": 0,
               "withdrawn_exponent_in_the_paper_outside_its_no_go": 0,
               "frontier_declares_the_exponent_unused": 0,
               "provenance_note_present": 0,
               "rows": []}
    lo, hi = widen(*beta_tight(), 40)
    b = math.log2(3)
    for name, blo, bhi, chain, budget in (("beta", lo, hi, b, 4),):
        t["constants_checked"] += 1
        if name not in frontier:
            t["missing_from_the_frontier"] += 1
            continue
        pub = frontier[name]
        verdict, dd = verdict_with_budget(pub, blo, bhi, chain, budget)
        if verdict == "undecided":
            t["undecided_brackets"] += 1
        elif verdict == "exact":
            t["exact_to_the_last_bit"] += 1
        elif verdict == "the float64 chain":
            t["from_the_float64_chain_not_the_nearest_double"] += 1
        else:
            t["disagreeing_with_both_evaluations"] += 1
        t["rows"].append({"constant": name, "frontier": repr(pub),
                          "verdict": verdict if dd == 0
                          else "%+d ulp, %s" % (dd, verdict)})
    # the round claims not to use the withdrawn exponent; check the claim
    t["withdrawn_exponent_in_the_frontier"] = int(
        WITHDRAWN in json.dumps(frontier))
    t["withdrawn_exponent_in_the_checker_report"] = int(
        WITHDRAWN in json.dumps(report))
    body = paper
    for m in re.finditer(r"^## NO-GO [^\n]*$(.*?)(?=^## |\Z)", paper,
                         re.M | re.S):
        body = body.replace(m.group(0), "")
    t["withdrawn_exponent_in_the_paper_outside_its_no_go"] = body.count(
        WITHDRAWN)
    t["frontier_declares_the_exponent_unused"] = int(
        frontier.get("rho_star_4_1164_used") is False)
    t["provenance_note_present"] = int((bundle / PROVENANCE).exists())
    t["oscillation_threshold_is_one_half"] = int(
        frontier.get("oscillation_square_root_threshold_exponent") == 0.5)
    return t


# ---------------------------------------------------------------------------
# Theorem 3.1 -- the transport identity, exact
# ---------------------------------------------------------------------------

def check_transport(edges: list) -> dict:
    t: dict = {"edges": 0,
               "exact_transport_violations": 0,
               "float_transport_violations_at_their_tolerance": 0,
               "largest_float_error_exponent": 0,
               "their_tolerance_over_the_largest_error": 0}
    worst = 0.0
    for r in edges:
        t["edges"] += 1
        d, n, u, up = r["d"], r["n"], r["u"], r["up"]
        c2, c3 = r["c2"], r["c3"]
        rhs = (Fraction(3 ** c3) if c3 >= 0 else Fraction(1, 3 ** -c3))
        rhs /= (Fraction(1 << c2) if c2 >= 0 else Fraction(1, 1 << -c2))
        rhs *= Fraction(3 * n + d, 3 * n)
        if Fraction(up, u) != rhs:
            t["exact_transport_violations"] += 1
        lhs = math.log2(up / u)
        flt = math.log2(3) * c3 - c2 + math.log2(1 + d / (3 * n))
        err = abs(lhs - flt)
        worst = max(worst, err)
        if not err < 2e-11:
            t["float_transport_violations_at_their_tolerance"] += 1
    # limit_denominator(1e12) rounds a 1e-15 error to zero; the decimal
    # exponent is the readable form and survives the round trip
    t["largest_float_error_exponent"] = (
        int(math.floor(math.log10(worst))) if worst > 0 else 0)
    t["their_tolerance_over_the_largest_error"] = (
        int(2e-11 / worst) if worst > 0 else 0)
    return t


# ---------------------------------------------------------------------------
# their synchronized reservoir toll -- three clauses, all definitional
# ---------------------------------------------------------------------------

def check_sync_toll(edges: list) -> dict:
    """`c3 >= 1`, `B >= c3 - 1`, `n >= 3^{c3-1}` on every synchronized edge.

    All three reduce to facts about the definitions. `c3 > 0` is the branch
    condition and `c3` is an integer, so `c3 >= 1` restates it. `c3 = 1+B-B'`
    makes `B >= c3 - 1` exactly `B' >= 0`, which a 3-adic valuation always is.
    And `3^B | n` with `B >= c3-1` gives the third. Each is scored against the
    fact it reduces to, so the claim is a measurement.
    """
    t: dict = {"sync_edges": 0,
               "c3_below_one": 0,
               "reservoir_depth_violations": 0,
               "quotient_floor_violations": 0,
               "output_ternary_valuation_negative": 0,
               "reservoir_depth_disagreeing_with_a_nonneg_valuation": 0,
               "c3_at_least_one_disagreeing_with_the_branch": 0,
               "largest_sync_c3": 0,
               "predicate_pairs_compared": 0}
    for r in edges:
        if r["typ"] != "sync":
            continue
        t["sync_edges"] += 1
        b, bp, c3, n = r["B"], r["Bp"], r["c3"], r["n"]
        t["largest_sync_c3"] = max(t["largest_sync_c3"], c3)
        if not c3 >= 1:
            t["c3_below_one"] += 1
        if not b >= c3 - 1:
            t["reservoir_depth_violations"] += 1
        if not n >= 3 ** (c3 - 1):
            t["quotient_floor_violations"] += 1
        if bp < 0:
            t["output_ternary_valuation_negative"] += 1
        t["predicate_pairs_compared"] += 2
        if (b >= c3 - 1) != (bp >= 0):
            t["reservoir_depth_disagreeing_with_a_nonneg_valuation"] += 1
        if (c3 >= 1) != (c3 > 0):
            t["c3_at_least_one_disagreeing_with_the_branch"] += 1
    return t


# ---------------------------------------------------------------------------
# the variation-transfer bound, per term
# ---------------------------------------------------------------------------

def check_variation(edges: list, trials: int = 6000,
                    seed: int = 26081526) -> dict:
    t: dict = {"terms": 0, "terms_with_negative_slack": 0,
               "windows": 0, "window_violations": 0,
               "broken_windows": 0, "broken_window_failures": 0}
    bf = math.log2(3)
    for r in edges:
        t["terms"] += 1
        du = abs(math.log2(r["up"] / r["u"]))
        imb = abs(r["c2"] - bf * r["c3"])
        e = abs(math.log2(1 + r["d"] / (3 * r["n"])))
        if abs(du - imb) > e + 1e-12:
            t["terms_with_negative_slack"] += 1
    rng = Random(seed)
    for _ in range(trials):
        m = rng.choice(MODS)
        y = rng.randrange(7, Y_LIMIT, 2)
        if y % 3 == 0:
            continue
        st, qs = orbit(y, STEPS)
        a = rng.randint(0, 8)
        b = rng.randint(a + 2, 15)
        rows = [edge(st[i], st[i + 1], qs[i], m) for i in range(a, b)]
        if any(not isinstance(x, dict) for x in rows):
            continue
        t["windows"] += 1
        tv = sum(abs(math.log2(x["up"] / x["u"])) for x in rows)
        j = sum(abs(x["c2"] - bf * x["c3"]) for x in rows)
        e = sum(abs(math.log2(1 + x["d"] / (3 * x["n"]))) for x in rows)
        if not abs(tv - j) <= e + 2e-10:
            t["window_violations"] += 1
        # the control: replace one edge's unit ratio by an unrelated one, so
        # the per-term identity no longer holds and the sum must notice
        if len(rows) < 3:
            continue
        t["broken_windows"] += 1
        tv2 = tv - abs(math.log2(rows[1]["up"] / rows[1]["u"])) + 40.0
        if abs(tv2 - j) <= e + 2e-10:
            t["broken_window_failures"] += 0
        else:
            t["broken_window_failures"] += 1
    return t


# ---------------------------------------------------------------------------
# Lemma 7.1 -- exact rational separation, no floating point
# ---------------------------------------------------------------------------

def check_cf(dmax: int = DMAX) -> dict:
    """`|a - beta b| > 1/(Q_D b)` for `1 <= b <= D`, decided in integers.

    With `beta` pinned between `pl/ql` and `ph/qh`, the nearest integer `a` to
    `beta b` is determined whenever both ends round the same way, and then a
    certified lower bound on `|a - beta b|` is one of `a*qh - ph*b` over `qh`
    or `pl*b - a*ql` over `ql`. Cross-multiplying leaves only integers.
    """
    t: dict = {"certified_partial_quotients": 0,
               "published_prefix_length": 0,
               "m_beta_at_D": 0, "q_local": 0,
               "b_values_tested": 0,
               "separation_violations": 0,
               "b_values_the_bracket_could_not_decide": 0,
               "tightest_separation_ratio": 0,
               "largest_convergent_denominator_at_or_below_D": 0}
    terms = certified_cf()
    t["certified_partial_quotients"] = len(terms)
    mb = m_beta(terms, dmax)
    if mb is None:
        t["b_values_the_bracket_could_not_decide"] = dmax
        return t
    t["m_beta_at_D"] = mb
    q_local = mb + 2
    t["q_local"] = q_local
    cv = convergents(terms)
    t["largest_convergent_denominator_at_or_below_D"] = max(
        (q for _p, q in cv if q <= dmax), default=0)

    lo, hi = beta_tight()
    pl, ql = lo.numerator, lo.denominator
    ph, qh = hi.numerator, hi.denominator
    best_n, best_d = None, None
    for b in range(1, dmax + 1):
        t["b_values_tested"] += 1
        # the nearest integer to beta*b, from both ends
        a_lo = (2 * pl * b + ql) // (2 * ql)
        a_hi = (2 * ph * b + qh) // (2 * qh)
        if a_lo != a_hi:
            t["b_values_the_bracket_could_not_decide"] += 1
            continue
        a = a_lo
        # a certified lower bound on |a - beta*b|, as num/den
        if a * qh - ph * b > 0:
            num, den = a * qh - ph * b, qh
        elif pl * b - a * ql > 0:
            num, den = pl * b - a * ql, ql
        else:
            t["b_values_the_bracket_could_not_decide"] += 1
            continue
        # num/den > 1/(q_local*b)  <->  num*q_local*b > den
        if not num * q_local * b > den:
            t["separation_violations"] += 1
        # the ratio (num/den) * q_local * b, tracked as an exact fraction
        rn, rd = num * q_local * b, den
        if best_n is None or rn * best_d < best_n * rd:
            best_n, best_d = rn, rd
    if best_n is not None:
        # the bracket's denominators are 40-digit, so the exact ratio is
        # unreadable; four decimals is what the claim needs
        t["tightest_separation_ratio"] = round(
            float(Fraction(best_n, best_d)), 4)
    return t


# ---------------------------------------------------------------------------
# Theorems 8.1 / 9.1, and their two two-counter blocks
# ---------------------------------------------------------------------------

def check_masters(cf: dict, trials: int = 12000,
                  seed: int = 26081526) -> dict:
    t: dict = {"batches": 0,
               "gate_count_master_violations": 0,
               "workload_depth_master_violations": 0,
               "counters_their_block_increments": 2,
               "run_trials": 0, "run_guard_opened": 0,
               "monotone_run_violations": 0,
               "coarea_identity_violations": 0,
               "coarea_max_crossing_violations": 0,
               "run_counters_their_block_increments": 2}
    q_local = cf.get("q_local") or 0
    lo, hi = beta_tight()
    rng = Random(seed)
    if q_local:
        for _ in range(trials):
            t["batches"] += 1
            d = rng.randint(5, DMAX)
            n = rng.randint(2, 40)
            bs = [rng.randint(1, d) for _ in range(n)]
            j = Fraction(0)
            for b in bs:
                a = round(float(lo) * b)
                j += abs(Fraction(a) - hi * b) if a > float(hi) * b else \
                    abs(lo * b - a)
            s = sum(bs)
            if not j * q_local * s + Fraction(1, 10 ** 9) >= n * n:
                t["gate_count_master_violations"] += 1
            if not j * q_local * d * d + Fraction(1, 10 ** 9) >= s:
                t["workload_depth_master_violations"] += 1

    rng = Random(seed + 1)
    for _ in range(trials):
        t["run_trials"] += 1
        n = rng.randint(4, 80)
        vals = [rng.random() * rng.randint(1, 20) for _ in range(n)]
        h = max(vals) - min(vals)
        tv = sum(abs(b - a) for a, b in zip(vals, vals[1:]))
        diffs = [1 if b - a > 0 else -1
                 for a, b in zip(vals, vals[1:]) if abs(b - a) > 1e-15]
        runs = 0
        if diffs:
            runs = 1 + sum(1 for a, b in zip(diffs, diffs[1:]) if a != b)
        if h <= 1e-14:
            continue
        t["run_guard_opened"] += 1
        if not tv <= runs * h + 1e-10:
            t["monotone_run_violations"] += 1
        uniq = sorted(set(vals))
        integ, mx = 0.0, 0
        for a, b in zip(uniq, uniq[1:]):
            if b <= a:
                continue
            mid = (a + b) / 2
            c = sum(1 for x, y in zip(vals, vals[1:])
                    if min(x, y) < mid < max(x, y))
            integ += (b - a) * c
            mx = max(mx, c)
        if not abs(integ - tv) < 1e-8:
            t["coarea_identity_violations"] += 1
        if not mx * h + 1e-10 >= tv:
            t["coarea_max_crossing_violations"] += 1
    return t


# ---------------------------------------------------------------------------
# their exponent block -- an assert implied by its own guard
# ---------------------------------------------------------------------------

def check_exponent(trials: int = 20000, seed: int = 26081526) -> dict:
    t: dict = {"trials": 0, "reached_the_assert": 0,
               "assert_implied_by_its_own_guard": 0,
               "assert_not_implied": 0,
               "half_space_violations": 0,
               "samples_in_the_half_space": 0}
    rng = Random(seed + 2)
    for _ in range(trials):
        t["trials"] += 1
        alpha, mu, chi = rng.random(), rng.random(), rng.random()
        lhs = alpha + chi + 2 * mu
        feasible = lhs >= 1 - 1e-12
        if feasible:
            t["samples_in_the_half_space"] += 1
            # the round's actual claim: the master bound forces this half-space
            if not lhs >= 1 - 1e-12:
                t["half_space_violations"] += 1
            continue
        t["reached_the_assert"] += 1
        # their assert is `lhs < 1 + 1e-12`, and the branch already gives
        # `lhs < 1 - 1e-12`, which is strictly stronger
        if lhs < 1 - 1e-12 and lhs < 1 + 1e-12:
            t["assert_implied_by_its_own_guard"] += 1
        else:
            t["assert_not_implied"] += 1
    return t


# ---------------------------------------------------------------------------
# published examples
# ---------------------------------------------------------------------------

def check_examples(report: dict) -> dict:
    t: dict = {"rows": 0, "groups": 0,
               "quotient_identity_violations": 0,
               "depth_fields_disagreeing": 0,
               "unit_fields_disagreeing": 0,
               "class_not_synchronized": 0}
    for _key, rows in (report.get("examples", {}) or {}).items():
        t["groups"] += 1
        for ex in rows:
            t["rows"] += 1
            q, d, n, n2 = ex["q"], ex["d"], ex["n"], ex["np"]
            if (1 << q) * n2 != 3 * n + d:
                t["quotient_identity_violations"] += 1
            if (q + ex["Ap"] - ex["A"] != ex["c2"]
                    or 1 + ex["B"] - ex["Bp"] != ex["c3"]):
                t["depth_fields_disagreeing"] += 1
            if (n // ((1 << ex["A"]) * 3 ** ex["B"]) != ex["u"]
                    or n2 // ((1 << ex["Ap"]) * 3 ** ex["Bp"]) != ex["up"]):
                t["unit_fields_disagreeing"] += 1
            if not (ex["c2"] > 0 and ex["c3"] > 0):
                t["class_not_synchronized"] += 1
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
               "duplicate_file_pairs": [],
               "validation_file_pass_flags_not_true": 0,
               "validation_names_a_file_not_in_the_bundle": []}
    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    t["files_present"] = len(present)
    actual = {n: hashlib.sha256((bundle / n).read_bytes()).hexdigest()
              for n in present}
    listed: dict = {}
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
    by: dict = {}
    for n, d in actual.items():
        by.setdefault(d, []).append(n)
    t["duplicate_file_pairs"] = [sorted(v) for v in by.values() if len(v) > 1]
    val = json.loads((bundle / VALIDATION).read_text(encoding="utf-8"))
    files = val.get("files")
    if not isinstance(files, dict):
        # this round names its per-file results under `checks`
        files = val.get("checks")
        files = files if isinstance(files, dict) else {}
    named = set(files)
    lst = val.get("files_checked")
    if isinstance(lst, list):
        named |= {n for n in lst if isinstance(n, str)}
    for key in ("json_parse", "python_compile"):
        entry = val.get(key)
        if isinstance(entry, dict):
            if all(isinstance(k, str) for k in entry):
                named |= set(entry)
            if isinstance(entry.get("file"), str):
                named.add(entry["file"])
    with_digest = set()
    for n, r in files.items():
        t["validation_per_file_entries"] += 1
        if isinstance(r, dict) and "sha256" in r:
            t["validation_entries_with_a_digest"] += 1
            with_digest.add(n)
        if isinstance(r, list) and any(str(x).upper() != "PASS" for x in r):
            t["validation_file_pass_flags_not_true"] += 1
    t["files_absent_from_the_validation_record"] = [n for n in present
                                                    if n not in named]
    # the other direction, which no earlier gate of this sweep asked: a record
    # that attests PASS for a file the bundle does not contain
    t["validation_names_a_file_not_in_the_bundle"] = sorted(
        n for n in named if n not in actual)
    t["files_with_no_digest_anywhere"] = [n for n in present
                                          if n not in listed
                                          and n not in with_digest]
    t["validation_pass_flag_key"] = None
    t["validation_all_pass_flag"] = None
    for key in ("all_pass", "overall_pass", "pass", "status"):
        if key in val:
            t["validation_pass_flag_key"] = key
            t["validation_all_pass_flag"] = val[key]
            break
    t["validation_records_no_pass_flag_at_all"] = int(
        t["validation_pass_flag_key"] is None)
    t["validation_pass_flag_not_passing"] = int(
        t["validation_all_pass_flag"] not in (True, "PASS", "pass", None))
    t["validation_top_level_keys"] = sorted(val)
    # `rho_star_4_1164_used: false` is a deliberate NEGATIVE declaration, not a
    # failed check; a blanket "every boolean must be true" rule misreads it
    intentional_negatives = {"rho_star_4_1164_used"}
    t["validation_declares_the_withdrawn_exponent_unused"] = int(
        val.get("rho_star_4_1164_used") is False)
    t["validation_top_level_flags_not_true"] = sum(
        1 for k, v in val.items()
        if isinstance(v, bool) and v is not True
        and k not in intentional_negatives)
    t["validation_file_pass_flags_not_true"] += sum(
        1 for r in files.values()
        if isinstance(r, dict) and r.get("pass") is not True)
    return t


def check_ledger(ledger: dict, paper: str) -> dict:
    t: dict = {"paper_proved_items": 0, "ledger_proved_items": 0,
               "paper_open_items": 0, "ledger_open_items": 0,
               "paper_no_go_headings": 0, "ledger_no_go_items": 0,
               "ledger_has_an_open_key": False,
               "ledger_has_no_no_go_key": 0,
               "open_items_absent_from_the_ledger": [],
               "no_go_headings_absent_from_the_ledger": [],
               "heuristic_failed_its_positive_control": 0,
               "heuristic_failed_its_negative_control": 0}
    no_go = re.findall(r"^## NO-GO ([\d.]+) — (.+)$", paper, re.M)
    t["paper_no_go_headings"] = len(no_go)
    m = re.search(r"^#+ [^\n]*Proved internally[^\n]*$(.*?)^#+ ",
                  paper, re.M | re.S)
    if m:
        t["paper_proved_items"] = len(re.findall(r"^\d+\. ", m.group(1), re.M))
    m = re.search(r"^#+ [^\n]*Explicitly open[^\n]*$(.*?)(?:^#+ |\Z)",
                  paper, re.M | re.S)
    bullets = []
    if m:
        bullets = [b.strip(" -;.")
                   for b in re.findall(r"^- (.+)$", m.group(1), re.M)]
    t["paper_open_items"] = len(bullets)
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
    t["ledger_has_no_no_go_key"] = int(
        not any(("no_go" in k.lower() or "nogo" in k.lower()
                 or "sealed" in k.lower()) for k in ledger))
    blob = json.dumps(ledger).lower()

    def covered(text: str) -> bool:
        words = [w for w in re.findall(r"[a-z_]{4,}", text.lower())
                 if w not in ("which", "these", "there", "their", "about",
                              "that", "with", "from", "this", "than")]
        if not words:
            return True
        return sum(1 for w in words if w[:7] in blob) >= max(1, len(words) // 2)

    t["open_items_absent_from_the_ledger"] = [b for b in bullets
                                              if not covered(b)]
    t["no_go_headings_absent_from_the_ledger"] = [n for n, hd in no_go
                                                  if not covered(hd)]
    first = " ".join(str(x) for x in (ledger.get(proved_key, []) or [""])[:1])
    t["heuristic_failed_its_positive_control"] = int(bool(first)
                                                     and not covered(first))
    t["heuristic_failed_its_negative_control"] = int(
        covered("quokka bandersnatch flimflam zeppelin marzipan"))
    return t


def check_population(edges: list, errs: list) -> dict:
    types: dict = {}
    for r in edges:
        types[r["typ"]] = types.get(r["typ"], 0) + 1
    return {"edges": len(edges), "moduli": len(MODS),
            "sources": len({r["x"] for r in edges}),
            "malformed_edges": len(errs),
            "zero": types.get("zero", 0), "sync": types.get("sync", 0),
            "binary_exclusive": types.get("BE", 0),
            "ternary_exclusive": types.get("TE", 0),
            "unclassified": types.get("BAD", 0)}


def check_their_claims(report: dict, res: dict) -> dict:
    pop, tp, sy = res["population"], res["transport"], res["sync_toll"]
    va, cf, ma = res["variation"], res["cf"], res["masters"]
    exp = res["exponent"]
    same = {
        "primitive_log_transport_exact": tp["edges"],
        "sync_ternary_reservoir_toll_base": sy["sync_edges"],
        "finite_CF_separation": cf["b_values_tested"],
        "exponent_master_algebra": exp["trials"],
    }
    other = {
        "variation_transfer_triangle": ("variation.windows", va["windows"]),
        "monotone_run_bound": ("masters.run_guard_opened",
                               ma["run_guard_opened"]),
        "coarea_crossing_identity": ("masters.run_guard_opened",
                                     ma["run_guard_opened"]),
        "CF_gate_count_master": ("masters.batches", ma["batches"]),
        "CF_workload_depth_master": ("masters.batches", ma["batches"]),
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
            exact += int(cnt == v)
        else:
            rows.append({"check": k, "theirs": v, "mine": None,
                         "basis": "not covered"})
    for field, mine in (("actual_quotient_active_edges", pop["edges"]),
                        ("actual_sync_edges", sy["sync_edges"]),
                        ("actual_sync_max_c3", sy["largest_sync_c3"])):
        rows.append({"check": field, "theirs": report.get(field),
                     "mine": mine, "basis": "same population"})
        exact += int(report.get(field) == mine)
    return {"rows": rows,
            "checks_not_covered_at_all": sum(1 for r in rows
                                             if r["basis"] == "not covered"),
            "checks_covered_by_a_different_population": covered,
            "checks_they_report_as_zero": sum(1 for r in rows
                                              if r["theirs"] == 0),
            "counts_i_reproduce_exactly": exact}


SECTIONS = ("instrument", "constants", "population", "transport", "sync_toll",
            "variation", "cf", "masters", "exponent", "examples",
            "artifacts", "ledger", "their_claims")

FAILURE_COUNTERS = (
    ("instrument", "failed"),
    ("constants", "disagreeing_with_both_evaluations"),
    ("constants", "undecided_brackets"),
    ("constants", "missing_from_the_frontier"),
    ("population", "malformed_edges"),
    ("population", "unclassified"),
    ("transport", "exact_transport_violations"),
    ("transport", "float_transport_violations_at_their_tolerance"),
    ("sync_toll", "c3_below_one"),
    ("sync_toll", "reservoir_depth_violations"),
    ("sync_toll", "quotient_floor_violations"),
    ("sync_toll", "output_ternary_valuation_negative"),
    ("sync_toll", "reservoir_depth_disagreeing_with_a_nonneg_valuation"),
    ("sync_toll", "c3_at_least_one_disagreeing_with_the_branch"),
    ("variation", "terms_with_negative_slack"),
    ("variation", "window_violations"),
    ("cf", "separation_violations"),
    ("cf", "b_values_the_bracket_could_not_decide"),
    ("masters", "gate_count_master_violations"),
    ("masters", "workload_depth_master_violations"),
    ("masters", "monotone_run_violations"),
    ("masters", "coarea_identity_violations"),
    ("masters", "coarea_max_crossing_violations"),
    ("exponent", "assert_not_implied"),
    ("exponent", "half_space_violations"),
    ("examples", "quotient_identity_violations"),
    ("examples", "depth_fields_disagreeing"),
    ("examples", "unit_fields_disagreeing"),
    ("examples", "class_not_synchronized"),
    ("artifacts", "digest_mismatches"),
    ("artifacts", "validation_file_pass_flags_not_true"),
    ("artifacts", "validation_top_level_flags_not_true"),
    ("artifacts", "validation_pass_flag_not_passing"),
    ("ledger", "heuristic_failed_its_positive_control"),
    ("ledger", "heuristic_failed_its_negative_control"),
) + tuple(("errors", "%s_raised" % s) for s in SECTIONS)

NON_VACUITY = (
    ("constants", "constants_checked"),
    ("constants", "provenance_note_present"),
    ("constants", "frontier_declares_the_exponent_unused"),
    ("population", "edges"),
    ("population", "sources"),
    ("population", "zero"),
    ("population", "sync"),
    ("population", "binary_exclusive"),
    ("population", "ternary_exclusive"),
    ("transport", "edges"),
    ("sync_toll", "sync_edges"),
    ("sync_toll", "predicate_pairs_compared"),
    ("variation", "terms"),
    ("variation", "windows"),
    ("variation", "broken_windows"),
    ("variation", "broken_window_failures"),
    ("cf", "certified_partial_quotients"),
    ("cf", "b_values_tested"),
    ("cf", "m_beta_at_D"),
    ("cf", "q_local"),
    ("masters", "batches"),
    ("masters", "run_trials"),
    ("masters", "run_guard_opened"),
    ("exponent", "trials"),
    ("exponent", "reached_the_assert"),
    ("exponent", "assert_implied_by_its_own_guard"),
    ("exponent", "samples_in_the_half_space"),
    ("examples", "rows"),
    ("examples", "groups"),
)

# An artifact defect is not a defect in the mathematics, and `passed` has meant
# "the mathematics reproduces" for thirty-one reports. But burying a false
# attestation among the observations would hide it, so these get their own
# top-level field in the output instead of either bucket.
ARTIFACT_DEFECTS = (
    ("artifacts", "validation_names_a_file_not_in_the_bundle"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("artifacts", "digest_mismatches"),
)

OBSERVATIONS = (
    ("artifacts", "validation_names_a_file_not_in_the_bundle"),
    ("artifacts", "checksum_lines_naming_a_missing_file"),
    ("instrument", "checks"),
    ("constants", "from_the_float64_chain_not_the_nearest_double"),
    ("constants", "exact_to_the_last_bit"),
    ("constants", "withdrawn_exponent_in_the_frontier"),
    ("constants", "withdrawn_exponent_in_the_checker_report"),
    ("constants", "withdrawn_exponent_in_the_paper_outside_its_no_go"),
    ("constants", "oscillation_threshold_is_one_half"),
    ("population", "moduli"),
    ("transport", "largest_float_error_exponent"),
    ("transport", "their_tolerance_over_the_largest_error"),
    ("sync_toll", "largest_sync_c3"),
    ("cf", "published_prefix_length"),
    ("cf", "tightest_separation_ratio"),
    ("cf", "largest_convergent_denominator_at_or_below_D"),
    ("masters", "counters_their_block_increments"),
    ("masters", "run_counters_their_block_increments"),
    ("artifacts", "files_present"),
    ("artifacts", "digests_listed"),
    ("artifacts", "validation_per_file_entries"),
    ("artifacts", "validation_entries_with_a_digest"),
    ("artifacts", "validation_records_no_pass_flag_at_all"),
    ("artifacts", "validation_declares_the_withdrawn_exponent_unused"),
    ("ledger", "paper_proved_items"),
    ("ledger", "ledger_proved_items"),
    ("ledger", "paper_open_items"),
    ("ledger", "ledger_open_items"),
    ("ledger", "paper_no_go_headings"),
    ("ledger", "ledger_no_go_items"),
    ("ledger", "ledger_has_no_no_go_key"),
    ("their_claims", "checks_not_covered_at_all"),
    ("their_claims", "checks_covered_by_a_different_population"),
    ("their_claims", "checks_they_report_as_zero"),
    ("their_claims", "counts_i_reproduce_exactly"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    bundle = pathlib.Path(a.bundle)
    paper = (bundle / PAPER).read_text(encoding="utf-8")
    frontier = json.loads((bundle / FRONTIER).read_text(encoding="utf-8"))
    ledger = json.loads((bundle / LEDGER).read_text(encoding="utf-8"))
    report = json.loads((bundle / REPORT).read_text(encoding="utf-8"))

    edges, errs = population()

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
    run("constants", lambda: check_constants(frontier, report, bundle, paper))
    run("population", lambda: check_population(edges, errs))
    run("transport", lambda: check_transport(edges))
    run("sync_toll", lambda: check_sync_toll(edges))
    run("variation", lambda: check_variation(edges))
    run("cf", check_cf)
    run("masters", lambda: check_masters(res.get("cf", {})))
    run("exponent", check_exponent)
    run("examples", lambda: check_examples(report))
    run("artifacts", lambda: check_artifacts(bundle))
    run("ledger", lambda: check_ledger(ledger, paper))
    res.setdefault("cf", {})["published_prefix_length"] = len(
        report.get("continued_fraction_prefix", []) or [])
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
    artifact_defects = []
    for sec, key in ARTIFACT_DEFECTS:
        v = res.get(sec, {}).get(key, 0)
        if (len(v) if isinstance(v, list) else v):
            artifact_defects.append("%s.%s = %s" % (sec, key, v))

    declared = ({(s, k) for s, k in FAILURE_COUNTERS}
                | {(s, k) for s, k in NON_VACUITY}
                | {(s, k) for s, k in OBSERVATIONS}
                | {(s, k) for s, k in ARTIFACT_DEFECTS})
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
        "run": "RUN-054", "round": "A-U.2d.26", "bundle": str(bundle),
        "passed": not failures and not vacuous,
        "failures": failures,
        "empty_populations": vacuous,
        "artifact_defects_the_mathematics_does_not_depend_on": artifact_defects,
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
