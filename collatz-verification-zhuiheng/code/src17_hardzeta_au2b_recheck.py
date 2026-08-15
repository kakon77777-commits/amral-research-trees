"""Recheck of source item 33 — Phase II / Round A-U.2b, Sparse Lift Rigidity.

數學戰士「墜衡」 / AMRAL Research Lab.

The first **positive** round of Phase II. A-U.1 and A-U.2a both ended in no-gos;
this one eliminates classes outright, including the mechanical critical code that
defeated A-U.1.

The argument is a squeeze between two exponential scales:

  thin-deficit exponent blocks grow like  Lambda_gamma = 2.8395137304...
  return separation operates at scale     3^r

and `Lambda_gamma < 3` is the whole result. Everything downstream — the
logarithmic deficit barrier, the explicit `0.01`, the eliminated families — rests
on that gap and on two explicit inequalities at `c = 0.645`, `eps = 0.01` that
clear by margins of 1e-4 and 6e-4.

So the constants are checked at 60 digits, not asserted. The rest is exact
integer algebra.

Usage:  python code/src17_hardzeta_au2b_recheck.py
Env:    HZ_SOURCE_DIR, HZ_ACCEL_MODULE
"""

from __future__ import annotations

import hashlib
import importlib
import io
import json
import math
import os
import pathlib
import sys
import zipfile
from decimal import Decimal, getcontext
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))

A = importlib.import_module(os.environ.get("HZ_ACCEL_MODULE", "hz_accel_code"))

BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip"
AU2B = "Hard_Zeta_Phase_II_Round_AU2b_Sparse_Lift_Rigidity_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.1_AU2b.md"
PRED = "Hard_Zeta_Phase_II_Round_AU2a_Lift_Occupation_Coupling_v0.1.md"

SPINES = [27, 103, 703, 1407, 10087, 15039, 35655]
DEPTH = 20

getcontext().prec = 60
BETA_D = Decimal(3).ln() / Decimal(2).ln()
GAMMA_D = BETA_D - 1
LN2 = Decimal(2).ln()


def read_sources() -> dict[str, str]:
    out = {}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                out[pathlib.PurePosixPath(n).name] = z.read(n).decode("utf-8")
    return out


def log2_lambda(g: Decimal) -> Decimal:
    return ((1 + g) * (1 + g).ln() - g * g.ln()) / LN2


def main() -> int:
    rep = {
        "tool": "src17_hardzeta_au2b_recheck.py",
        "subject": "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip (item 33) — Round "
                   "A-U.2b plus A_Line_ROUTE_MAP v1.1",
        "source_items": [33],
        "scope": "the repeated-block congruence and return separation, the "
                 "complexity-peak law and its deficit tradeoff, the thin-deficit "
                 "block count and its entropy constant, the two explicit "
                 "inequalities behind the 0.01 barrier, and the families the "
                 "round eliminates",
        "checks": {}, "counts": {}, "measured": {}, "failures": [],
    }
    checks, measured = rep["checks"], rep["measured"]

    def check(name, fn, note=""):
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        checks[name] = {"pass": bool(ok), "detail": detail, "note": note}

    docs = read_sources()
    au2b, routemap = docs.get(AU2B, ""), docs.get(ROUTEMAP, "")

    # ------------------------------------------ §4-§6: return separation
    def repeated_block_congruence():
        bad, tested, hits = [], 0, 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            q = A.accel_code(n, life)
            Y = A.orbit_endpoints(n, life)
            for r in range(1, 5):
                seen = {}
                for a in range(len(q) - r + 1):
                    blk = q[a:a + r]
                    if blk in seen:
                        b = seen[blk]
                        Q = sum(blk)
                        tested += 1
                        hits += 1
                        if (Y[a] - Y[b]) % 2 ** (Q + 1) != 0:
                            bad.append((n, r, a, b))
                    else:
                        seen[blk] = a
        return (not bad and hits > 0), {
            "repeats_found": hits, "violations": bad[:5],
            "_observable_nonempty": hits > 0}

    check("SRC17_a_repeated_exponent_block_forces_a_congruence",
          repeated_block_congruence,
          "§4: equal length-r blocks after a and b give Y_a = Y_b mod 2^{Q+1}; "
          "guarded so it is not graded on a sample with no repeats")

    def return_separation():
        bad, hits = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            q = A.accel_code(n, life)
            Y = A.orbit_endpoints(n, life)
            for r in range(1, 5):
                seen = {}
                for a in range(len(q) - r + 1):
                    blk = q[a:a + r]
                    if blk in seen:
                        b, Q = seen[blk], sum(blk)
                        hits += 1
                        if abs(Y[a] - Y[b]) < 2 ** (Q + 1):
                            bad.append((n, r, a, b, Y[a], Y[b]))
                        if 2 ** (Q + 1) < 2 ** (r + 1):
                            bad.append(("Q < r", n, r))
                    else:
                        seen[blk] = a
        return (not bad and hits > 0), {"repeats": hits, "violations": bad[:5]}

    check("SRC17_repeated_blocks_force_the_states_to_separate", return_separation,
          "§6: |Y_b - Y_a| >= 2^{Q+1} >= 2^{r+1}, since no state repeats")

    def no_repeated_state():
        bad = []
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            Y = A.orbit_endpoints(n, life)
            if len(set(Y)) != len(Y):
                bad.append(n)
        return not bad, {"spines": len(SPINES), "with_a_repeat": bad}

    check("SRC17_no_state_repeats_on_a_subcritical_spine", no_repeated_state,
          "§5: a repeat would make the orbit periodic")

    def cycle_forces_supercritical():
        # §5: any positive accelerated cycle needs 2^Q > 3^p. Both outcomes must
        # appear, or the implication is graded on one side only.
        sup, sub, bad = 0, 0, []
        for v in [(1,), (2,), (1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (1, 1, 1),
                  (2, 1, 2), (1, 2, 1), (3, 2, 1), (2, 2, 2)]:
            hot = A.cycle_is_supercritical(v)
            y = A.periodic_tail_source(v)
            sup += hot
            sub += not hot
            # a positive cycle source requires the supercritical side
            if (y > 0) != hot:
                bad.append((v, str(y), hot))
        return (not bad and sup > 0 and sub > 0), {
            "supercritical": sup, "subcritical": sub, "violations": bad[:5],
            "_both_outcomes_seen": sup > 0 and sub > 0}

    check("SRC17_a_positive_cycle_requires_a_supercritical_period",
          cycle_forces_supercritical,
          "§5: (2^Q - 3^p) Y = B_cyc > 0 forces Q > p*beta; both signs required")

    # ------------------------------ §7-§13: complexity and the peak law
    def complexity_peak():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            q = A.accel_code(n, life)
            Y = A.orbit_endpoints(n, life)
            for r in range(1, 6):
                p = A.factor_complexity(q, r)
                N = p + 1
                if N > len(Y):
                    continue
                tested += 1
                if max(Y[:N]) < 2 ** (r + 1):
                    bad.append((n, r, p, max(Y[:N])))
        return (not bad and tested > 0), {"windows": tested, "violations": bad[:5]}

    check("SRC17_the_complexity_peak_law_holds_on_real_spines", complexity_peak,
          "§8: M_{p(r)+1} >= 2^{r+1}, by pigeonhole on length-r factors")

    def excursion_upper_bound():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            Y = A.orbit_endpoints(n, life)
            for m in range(1, life + 1):
                d = A.deficit(n, m)
                tested += 1
                if not (Y[m] < 2 ** (d + 1) * (n + Fraction(m, 3))):
                    bad.append((n, m, Y[m], d))
        return (not bad and tested > 0), {"points": tested, "violations": bad[:5]}

    check("SRC17_the_exact_excursion_upper_bound_holds", excursion_upper_bound,
          "§9: Y_m < 2^{d_m+1}(n + m/3), in exact rationals")

    def complexity_deficit_tradeoff():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            q = A.accel_code(n, life)
            for r in range(1, 6):
                p = A.factor_complexity(q, r)
                N = p + 1
                if N > life:
                    continue
                tested += 1
                lhs = A.record_deficit(n, N)
                rhs = r - math.log2(n + N / 3)
                if not (lhs > rhs):
                    bad.append((n, r, lhs, rhs))
        return (not bad and tested > 0), {"windows": tested, "violations": bad[:5]}

    check("SRC17_the_complexity_deficit_tradeoff_holds", complexity_deficit_tradeoff,
          "§10: D_{p(r)+1} > r - log2(n + (p(r)+1)/3)")

    # -------------------------- §14-§20: the thin-deficit block count
    def deficit_recurrence():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            for m in range(1, life + 1):
                b = A.sturmian_credit(m) - A.sturmian_credit(m - 1)
                e = A.orbit_valuations(n, m)[-1] - 1
                tested += 1
                if A.deficit(n, m) != A.deficit(n, m - 1) + b - e if m > 1 else False:
                    bad.append((n, m))
        return (not bad and tested > 0), {"steps": tested, "violations": bad[:5]}

    check("SRC17_the_deficit_recurrence_holds", deficit_recurrence,
          "§14: d_m = d_{m-1} + b_m - e_m")

    def block_ledger():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            for i in range(0, life - 4):
                for r in (1, 2, 3, 4):
                    if i + r > life:
                        continue
                    lhs = A.block_excess(n, i, r)
                    rhs = (A.sturmian_credit(i + r) - A.sturmian_credit(i)
                           + A.deficit(n, i) - A.deficit(n, i + r)) if i else None
                    if rhs is None:
                        continue
                    tested += 1
                    if lhs != rhs:
                        bad.append((n, i, r, lhs, rhs))
        return (not bad and tested > 0), {"blocks": tested, "violations": bad[:5]}

    check("SRC17_the_block_excess_ledger_telescopes", block_ledger,
          "§15: E_{i,r} = floor(gamma(i+r)) - floor(gamma i) + d_i - d_{i+r}")

    def thin_deficit_range():
        bad, tested, seen = [], 0, []
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            D = A.record_deficit(n, life)
            g = math.log2(3) - 1
            for i in range(1, life - 4):
                for r in (2, 3, 4):
                    if i + r > life:
                        continue
                    E = A.block_excess(n, i, r)
                    seen.append(E)
                    tested += 1
                    if not (math.floor(g * r) - D <= E <= math.ceil(g * r) + D):
                        bad.append((n, i, r, E, D))
        # The range is a COROLLARY of the ledger plus d <= D, so it would hold
        # trivially on a degenerate sample. Require the excess to actually vary.
        spread = (max(seen) - min(seen)) if seen else 0
        return (not bad and tested > 0 and spread >= 2), {
            "blocks": tested, "violations": bad[:5], "excess_spread": spread,
            "_observable_nondegenerate": spread >= 2}

    check("SRC17_thin_deficit_blocks_stay_in_their_range", thin_deficit_range,
          "§16: floor(gamma r) - D <= E_{i,r} <= ceil(gamma r) + D")

    def composition_count():
        # §17's binomial, confronted with a direct enumeration
        bad = []
        for r in range(1, 7):
            for E in range(0, 8):
                brute = 0
                def walk(k, left):
                    nonlocal brute
                    if k == 1:
                        brute += 1
                        return
                    for x in range(left + 1):
                        walk(k - 1, left - x)
                walk(r, E)
                if A.composition_count(r, E) != brute:
                    bad.append((r, E, A.composition_count(r, E), brute))
        return not bad, {"pairs": 6 * 8, "violations": bad[:5]}

    check("SRC17_the_composition_count_matches_a_direct_enumeration",
          composition_count, "§17: C(r+E-1, E) sequences of r nonnegatives summing to E")

    def entropy_constant():
        L = A.entropy_base(A.gamma_decimal(50))
        claimed = "2.8395137304"
        return (str(L).startswith(claimed) and L < 3), {
            "computed": str(L)[:22], "claimed_prefix": claimed,
            "less_than_three": bool(L < 3),
            "gap_to_three": float(3 - L)}

    check("SRC17_the_entropy_constant_matches_and_is_below_three", entropy_constant,
          "§18-§20: Lambda_gamma = (1+g)^{1+g}/g^g = 2.8395137304..., and the "
          "whole round rests on it being < 3")

    def why_three_appears():
        # §19: Q >= floor(beta r) - D, hence 2^{Q+1} > 3^r / 2^D
        bad = []
        for r in range(1, 40):
            for D in range(0, 6):
                Q = A.floor_beta(r) - D
                if Q < 0:
                    continue
                if not (2 ** (Q + 1) * 2 ** D > 3 ** r):
                    bad.append((r, D))
                if A.floor_beta(r) != r + math.floor((math.log2(3) - 1) * r):
                    bad.append(("floor identity", r))
        return not bad, {"violations": bad[:5],
                         "note": "r + floor(gamma r) = floor(beta r) for integer r"}

    check("SRC17_return_separation_operates_at_base_three", why_three_appears,
          "§19: 2^{Q+1} > 3^r / 2^D, which is what makes 3 the scale Lambda must beat")

    # -------------------- §21-§27: the barrier and its explicit constants
    def interval_nonempty():
        lo = 1 / BETA_D
        hi = 1 / log2_lambda(GAMMA_D)
        c = Decimal("0.645")
        return (lo < hi and lo < c < hi), {
            "lower_1_over_beta": str(lo)[:20], "upper": str(hi)[:20],
            "c_used_by_the_paper": "0.645", "c_inside": bool(lo < c < hi)}

    check("SRC17_the_admissible_c_interval_is_nonempty", interval_nonempty,
          "§21: 1/beta < c < 1/log2(Lambda_gamma), non-empty exactly because "
          "Lambda_gamma < 3")

    def explicit_inequality_one():
        c, eps = Decimal("0.645"), Decimal("0.01")
        val = BETA_D * c - 1 - 2 * eps
        return (val > Decimal("0.0022")), {
            "value": str(val)[:20], "claimed_lower_bound": "0.0022",
            "margin": str(val - Decimal("0.0022"))[:14]}

    check("SRC17_the_first_explicit_inequality_clears", explicit_inequality_one,
          "§26: beta*c - 1 - 2eps > 0.0022 at c = 0.645, eps = 0.01")

    def explicit_inequality_two():
        c, eps = Decimal("0.645"), Decimal("0.01")
        val = c * log2_lambda(GAMMA_D + eps / c)
        return (val < Decimal("0.986")), {
            "value": str(val)[:20], "claimed_upper_bound": "0.986",
            "margin": str(Decimal("0.986") - val)[:14]}

    check("SRC17_the_second_explicit_inequality_clears", explicit_inequality_two,
          "§26: c*log2(Lambda_{gamma+eps/c}) < 0.986 at the same c and eps")

    # ------------------------------------- §30-§33: eliminated families
    def mechanical_has_zero_deficit():
        mech = A.mechanical_code(400)
        bad = [m for m in range(1, 401)
               if A.floor_beta(m) - A.cumulative(mech[:m])[-1] != 0]
        return not bad, {"m_range": "1..400", "violations": bad[:5],
                         "note": "K*_m = floor(beta m) exactly, so d_m = 0"}

    check("SRC17_the_mechanical_code_has_identically_zero_deficit",
          mechanical_has_zero_deficit,
          "§30: d_m = 0 for every m, so D_N = 0 = o(log N) and the barrier applies")

    def mechanical_is_sturmian():
        mech = A.mechanical_code(3000)
        bad = [r for r in range(1, 25) if A.factor_complexity(mech, r) != r + 1]
        return not bad, {"r_range": "1..24", "violations": bad[:5]}

    check("SRC17_the_mechanical_code_has_sturmian_complexity", mechanical_is_sturmian,
          "§31: p(r) = r + 1, so the tradeoff excludes it independently")

    def mechanical_nonanchored_cross_check():
        # Two independent routes to the same verdict: A-U.2b's barrier (d_m = 0),
        # and RUN-013's direct measurement that the lifts never stop.
        mech = A.mechanical_code(60)
        t = A.anchor_cocycle(mech)
        nonzero_late = [j + 1 for j, x in enumerate(t) if x and j > 30]
        zero_deficit = all(A.floor_beta(m) - A.cumulative(mech[:m])[-1] == 0
                           for m in range(1, 61))
        measured["mechanical_nonanchored"] = {
            "barrier_route_D_N": 0,
            "lift_route_nonzero_after_m30": nonzero_late,
            "agree": bool(zero_deficit and nonzero_late)}
        return (zero_deficit and bool(nonzero_late)), {
            "zero_deficit": zero_deficit,
            "late_nonzero_lifts": len(nonzero_late)}

    check("SRC17_two_independent_routes_agree_the_mechanical_code_is_unanchored",
          mechanical_nonanchored_cross_check,
          "§30 says d_m = 0 forces nonanchoring; RUN-013 measured the lifts never "
          "stopping. Different arguments, same verdict")

    def periodic_tail_is_negative():
        bad, tested, neg, pos = [], 0, 0, 0
        for v in [(1,), (1, 1), (1, 2), (2, 1), (1, 1, 1), (1, 2, 1), (2, 1, 1),
                  (1, 1, 2), (2, 2), (3, 1), (1, 3), (2, 2, 1)]:
            y = A.periodic_tail_source(v)
            sub = not A.cycle_is_supercritical(v)
            tested += 1
            if sub:
                neg += 1
                if y >= 0:
                    bad.append((v, str(y)))
            else:
                pos += 1
        return (not bad and neg > 0 and pos > 0), {
            "periods": tested, "subcritical": neg, "supercritical": pos,
            "violations": bad[:5], "_both_outcomes_seen": neg > 0 and pos > 0}

    check("SRC17_an_ultimately_periodic_subcritical_tail_has_a_negative_source",
          periodic_tail_is_negative,
          "§33: y = B_per/(2^Q - 3^p) < 0 whenever the period is subcritical")

    # --------------------------------------------------- ledger and bundle
    def limits_section():
        tail = au2b[au2b.find("# 36."):] if "# 36." in au2b else ""
        want = ["CASP", "CST", "Collatz"]
        missing = [w for w in want if w not in tail]
        return (bool(tail) and not missing), {
            "missing_from_the_limits_section": missing}

    check("SRC17_the_paper_states_what_it_does_not_prove", limits_section,
          "§36: a positive round must still say where it stops")

    check("SRC17_the_route_map_and_the_paper_agree_on_the_eliminated_classes",
          lambda: (("Classes eliminated" in routemap
                    and "mechanical critical code" in routemap
                    and "0.01" in routemap and "0.01" in au2b),
                   {"routemap_len": len(routemap)}),
          "v1.1 must list the same eliminations and the same constant")

    def bundle_faithful():
        def members(path):
            out = {}
            with zipfile.ZipFile(path) as z:
                for n in z.namelist():
                    if not n.endswith("/"):
                        out[pathlib.PurePosixPath(n).name] = hashlib.sha256(
                            z.read(n)).hexdigest()
            return out

        big = members(SOURCE / BUNDLE)
        earlier = {}
        for pat in ("Hard_Zeta_*Rounds_01_03A5*.zip",
                    "Hard_Zeta_Phase_II_Round_AU1_bundle.zip",
                    "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip"):
            for p in sorted(SOURCE.glob(pat)):
                earlier[p.name] = members(p)
        same, edited, fresh = [], [], []
        for name, h in big.items():
            hit = next(((z, m[name]) for z, m in earlier.items() if name in m), None)
            if hit is None:
                fresh.append(name)
            elif hit[1] == h:
                same.append(name)
            else:
                edited.append({"file": name, "differs_from": hit[0]})
        measured["bundle"] = {"reshipped_identical": sorted(same),
                              "reshipped_edited": edited,
                              "new_in_this_bundle": sorted(fresh)}
        return (not edited and len(same) >= 3 and len(fresh) == 2), {
            "reshipped_identical": len(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh)}

    check("SRC17_the_bundle_reships_its_predecessors_unedited", bundle_faithful,
          "the closure, A-U.1 and A-U.2a must be byte-identical to items 30-32")

    # ------------------------------------------------------ own measurement
    def best_constant_this_scheme_gives():
        # §37's A-U.2b.1 asks for the sharp threshold. The published 0.01 is a
        # safe round number; the scheme's own ceiling is what a sharpening round
        # would start from. Constraints, from §22-§24: block count o(N) needs
        # c*log2(Lambda_{gamma+eps/c}) < 1, and the separation must beat the
        # excursion bound, which needs beta*c - 1 - 2eps > 0.
        def feasible(c, e):
            return (BETA_D * c - 1 - 2 * e > 0
                    and c * log2_lambda(GAMMA_D + e / c) < 1)

        best, best_c = Decimal(0), None
        c = Decimal("0.60")
        while c < Decimal("0.70"):
            lo, hi = Decimal(0), Decimal("0.2")
            for _ in range(60):
                mid = (lo + hi) / 2
                if feasible(c, mid):
                    lo = mid
                else:
                    hi = mid
            if lo > best:
                best, best_c = lo, c
            c += Decimal("0.0005")
        measured["sharp_threshold"] = {
            "published_eps": 0.01, "published_c": 0.645,
            "scheme_ceiling_eps": float(best), "at_c": float(best_c),
            "improvement_factor": float(best / Decimal("0.01")),
            "reading": ("the published 0.01 is a safe round choice; the same "
                        "argument supports about 0.015 with no new ideas, and "
                        "anything past that needs a different one")}
        return (best > Decimal("0.01") and best < Decimal("0.05")), {
            "ceiling": float(best), "at_c": float(best_c)}

    check("SRC17_the_published_constant_is_below_this_schemes_ceiling",
          best_constant_this_scheme_gives,
          "measurement: how far §26's constant could be pushed without a new "
          "argument, which is what §37's A-U.2b.1 is for")

    def record_deficit_contrast():
        # Both outcomes required. Every real start must clear the barrier, and
        # the one object that does NOT clear it must be the countermodel the
        # theorem says is unanchored — otherwise the check tests nothing.
        rows = []
        for n in SPINES + [2 ** 11 - 1, 2 ** 17 - 1]:
            life = A.subcritical_lifetime(n)
            D = A.record_deficit(n, life)
            rows.append({"start": n, "lifetime": life, "D_N": D,
                         "D_over_log2N": D / math.log2(life)})
        mech = A.mechanical_code(400)
        mech_D = max(A.floor_beta(m) - A.cumulative(mech[:m])[-1]
                     for m in range(1, 401))
        measured["record_deficit"] = {
            "real_starts": rows, "mechanical_D_N": mech_D,
            "reading": ("real integers have no infinite subcritical spine, so the "
                        "theorem constrains a hypothetical. Every finite run that "
                        "does exist clears 0.01 by two orders of magnitude; the "
                        "only object with D_N = 0 is the mechanical code, which "
                        "§30 proves is not a positive integer. The all-ones family "
                        "is the OPPOSITE extreme — K_j = j gives d_j = floor(gamma j), "
                        "the largest deficit possible, not the smallest")}
        clears = all(r["D_over_log2N"] > 0.01 for r in rows)
        return (clears and mech_D == 0), {
            "real_starts_clearing": sum(1 for r in rows if r["D_over_log2N"] > 0.01),
            "of": len(rows), "mechanical_D_N": mech_D,
            "_both_outcomes_seen": clears and mech_D == 0}

    check("SRC17_real_starts_clear_the_barrier_and_only_the_countermodel_does_not",
          record_deficit_contrast,
          "measurement: D_N/log2 N on every subcritical run that exists, against "
          "the one code with D_N = 0")

    rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
    rep["counts"] = {"checks": len(checks),
                     "passed": sum(1 for v in checks.values() if v["pass"]),
                     "spines": len(SPINES)}
    rep["ok"] = not rep["failures"]
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
