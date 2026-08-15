"""Recheck of source item 34 — Phase II / Round A-U.2b.1, Sharp Packing Threshold.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-015 measured that A-U.2b's proof scheme tops out at `eps = 0.01502`, and said
that anything past it needs a different argument rather than better tuning. This
round supplies the different argument — **multi-occurrence packing**, which bounds
how often a block can recur rather than merely that it must — and reaches

    c_pack = x*/beta = 0.03585676003404866...

where `x*` is the unique positive root of `H(gamma + x) = beta`.

This is also the first round to ship its own numerical artifact: a script and a
JSON of constants to 80 digits. That is checked as an artifact — recomputed here
by **bisection in the standard library's `decimal`**, against the subject's
`mpmath.findroot`. Two libraries, two root-finding methods; agreement is a
cross-implementation result and not a re-run. (This tree has no third-party
packages, so running the subject's script was never an option.)

Usage:  python code/src18_hardzeta_au2b1_recheck.py
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

BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b1_bundle.zip"
AU2B1 = "Hard_Zeta_Phase_II_Round_AU2b1_Sharp_Packing_Entropy_Threshold_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.2_AU2b1.md"
CONSTANTS = "Hard_Zeta_AU2b1_packing_entropy_constants.json"
SCRIPT = "verify_Hard_Zeta_AU2b1_packing_entropy.py"
PRED = "Hard_Zeta_Phase_II_Round_AU2b_Sparse_Lift_Rigidity_v0.1.md"

SPINES = [27, 103, 703, 1407, 10087, 15039, 35655]
DIGITS = 60

getcontext().prec = DIGITS + 30
LN2 = Decimal(2).ln()
BETA_D = Decimal(3).ln() / LN2
GAMMA_D = BETA_D - 1
# RUN-015's measured ceiling for the PREVIOUS round's scheme
AU2B_SCHEME_CEILING = Decimal("0.015018214488925716")


def read_sources() -> dict[str, bytes]:
    out = {}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                out[pathlib.PurePosixPath(n).name] = z.read(n)
    return out


def main() -> int:
    rep = {
        "tool": "src18_hardzeta_au2b1_recheck.py",
        "subject": "Hard_Zeta_Phase_II_Round_AU2b1_bundle.zip (item 34) — Round "
                   "A-U.2b.1, its constants JSON and verification script, plus "
                   "A_Line_ROUTE_MAP v1.2",
        "source_items": [34],
        "scope": "the per-block packing bound and its multi-occurrence sum, the "
                 "composition entropy with its two exact derivative identities, "
                 "the variational problem whose supremum is the published "
                 "constant, and the bundled numerical artifact",
        "checks": {}, "counts": {}, "measured": {}, "failures": [],
    }
    checks, measured = rep["checks"], rep["measured"]

    def check(name, fn, note=""):
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        checks[name] = {"pass": bool(ok), "detail": detail, "note": note}

    raw = read_sources()
    au2b1 = raw.get(AU2B1, b"").decode("utf-8")
    routemap = raw.get(ROUTEMAP, b"").decode("utf-8")
    consts = json.loads(raw.get(CONSTANTS, b"{}").decode("utf-8"))

    # ------------------------------------------- §3-§8: blocks and excess
    def block_excess_identity():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            K = A.cumulative(A.accel_code(n, life))
            for r in range(1, 6):
                for i in range(0, life - r):
                    Q = K[i + r] - K[i]
                    E = Q - r
                    want = (A.sturmian_credit(i + r) - A.sturmian_credit(i)
                            + A.deficit(n, i) - A.deficit(n, i + r)) if i else None
                    if want is None:
                        continue
                    tested += 1
                    if E != want:
                        bad.append((n, i, r, E, want))
        return (not bad and tested > 0), {"blocks": tested, "violations": bad[:5]}

    check("SRC18_the_block_excess_identity_holds", block_excess_identity,
          "§7: E_i = floor(gamma(i+r)) - floor(gamma i) + d_i - d_{i+r}")

    def gamma_is_never_integral():
        # §8's range has width 1 because ceil(gamma r) = floor(gamma r) + 1, which
        # needs gamma*r to be non-integral. Checked rather than assumed.
        bad = [r for r in range(1, 200) if 2 ** A.floor_beta(r) == 3 ** r]
        return not bad, {"r_range": "1..199", "integral_at": bad}

    check("SRC18_gamma_times_r_is_never_an_integer", gamma_is_never_integral,
          "§8: so the floor/ceil window is exactly one wide")

    def excess_stays_in_range():
        bad, tested, spread = [], 0, []
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            D = A.record_deficit(n, life)
            K = A.cumulative(A.accel_code(n, life))
            for r in range(2, 6):
                lo, hi = A.excess_bounds(r, D)
                for i in range(0, life - r):
                    E = K[i + r] - K[i] - r
                    spread.append(E)
                    tested += 1
                    if not (lo <= E <= hi):
                        bad.append((n, i, r, E, lo, hi))
        return (not bad and tested > 0 and max(spread) - min(spread) >= 2), {
            "blocks": tested, "violations": bad[:5],
            "excess_spread": max(spread) - min(spread) if spread else 0}

    check("SRC18_the_block_excess_stays_inside_its_range", excess_stays_in_range,
          "§8: E_- <= E_i <= E_+; guarded so a degenerate sample cannot pass")

    # --------------------------------------- §5-§6, §11: the packing bound
    def per_block_packing():
        bad, tested, multi = [], 0, 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            Y = A.orbit_endpoints(n, N)
            M_N = max(Y[:N])
            for r in range(1, 5):
                counts = A.occurrence_counts(n, N, r)
                K = A.cumulative(A.accel_code(n, N))
                for blk, occ in counts.items():
                    Q = sum(blk)
                    tested += 1
                    if occ > 1:
                        multi += 1
                    if occ > 1 + Fraction(M_N, 2 ** (Q + 1)):
                        bad.append((n, r, blk, occ, M_N, Q))
        return (not bad and multi > 0), {
            "blocks": tested, "violations": bad[:5],
            "blocks_occurring_more_than_once": multi,
            "_observable_nonempty": multi > 0}

    check("SRC18_no_block_recurs_more_often_than_packing_allows", per_block_packing,
          "§6: occ_N(v) <= 1 + M_N/2^{Q+1}; guarded so it is not graded where "
          "every block occurs once")

    def multi_occurrence_inequality():
        # The inequality has enormous slack at any size this arm can compute, so
        # asserting it alone is close to vacuous. The guard is that the FIRST
        # term must be insufficient somewhere, so the multi-occurrence term is
        # actually exercised rather than carried along unused.
        bad, tested, b_needed, slack = [], 0, 0, []
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            Y = A.orbit_endpoints(n, N)
            M_N = max(Y[:N])
            D = A.record_deficit(n, N)
            for r in range(2, 6):
                lhs = N - r + 1
                a_term = A.block_count_A(r, D)
                rhs = a_term + Fraction(M_N, 2 ** (r + 1)) * A.block_count_B(r, D)
                tested += 1
                if a_term < lhs:
                    b_needed += 1
                slack.append(float(rhs) / lhs)
                if not (lhs <= rhs):
                    bad.append((n, r, lhs, float(rhs)))
        measured["packing_slack"] = {
            "windows": tested, "where_the_A_term_alone_is_insufficient": b_needed,
            "min_slack_ratio": min(slack), "max_slack_ratio": max(slack),
            "reading": ("the right side exceeds the left by up to eight orders of "
                        "magnitude at these sizes, so this check would not notice "
                        "a small error in either term — only a gross one. The "
                        "asymptotic content of the multi-occurrence refinement is "
                        "not visible on orbits this short.")}
        return (not bad and tested > 0 and b_needed > 0), {
            "windows": tested, "violations": bad[:5],
            "A_term_alone_insufficient_at": b_needed,
            "min_slack_ratio": min(slack) if slack else None,
            "_B_term_is_exercised": b_needed > 0}

    check("SRC18_the_multi_occurrence_packing_inequality_holds",
          multi_occurrence_inequality,
          "§11: N - r + 1 <= A(r,D) + (M_N/2^{r+1}) B(r,D), in exact rationals")

    def packing_sums_match_enumeration():
        # §9-§10: A and B as sums of binomials, confronted with a direct
        # enumeration of the blocks they claim to count.
        bad = []
        for r in range(1, 6):
            for D in (0, 1, 2):
                lo, hi = A.excess_bounds(r, D)
                brute_A, brute_B = 0, Fraction(0)

                def walk(k, left, chosen):
                    nonlocal brute_A, brute_B
                    if k == 0:
                        if left == 0:
                            brute_A += 1
                            brute_B += Fraction(1, 2 ** sum(chosen))
                        return
                    for x in range(left + 1):
                        walk(k - 1, left - x, chosen + [x])

                for E in range(lo, hi + 1):
                    walk(r, E, [])
                if A.block_count_A(r, D) != brute_A or A.block_count_B(r, D) != brute_B:
                    bad.append((r, D, A.block_count_A(r, D), brute_A))
        return not bad, {"shapes": 15, "violations": bad[:5]}

    check("SRC18_the_packing_sums_match_a_direct_enumeration",
          packing_sums_match_enumeration,
          "§9-§10: A and B counted by binomials against the blocks themselves")

    # ------------------------------- §12, §23: the two entropy identities
    def entropy_derivative_identity():
        bad = []
        h = Decimal(1) / Decimal(10 ** 25)
        for z in ("0.2", "0.5", "0.58496", "0.7", "0.95"):
            z = Decimal(z)
            num = (A.packing_entropy(z + h) - A.packing_entropy(z - h)) / (2 * h)
            claimed = A.packing_entropy_derivative(z)
            if abs(num - claimed) > Decimal(1) / Decimal(10 ** 20):
                bad.append((str(z), str(num)[:20], str(claimed)[:20]))
            if claimed <= 0:
                bad.append(("not positive", str(z)))
        return not bad, {"points": 5, "violations": bad}

    check("SRC18_the_entropy_derivative_is_log_of_one_plus_reciprocal",
          entropy_derivative_identity,
          "§12: H'(z) = log2(1 + 1/z) > 0, against a central difference")

    def variational_identity():
        # §23: H(z) - z H'(z) = log2(1+z), the identity that makes F increasing
        bad = []
        for z in ("0.1", "0.4", "0.58496", "0.64179", "0.9"):
            z = Decimal(z)
            lhs = A.packing_entropy(z) - z * A.packing_entropy_derivative(z)
            rhs = (1 + z).ln() / LN2
            if abs(lhs - rhs) > Decimal(1) / Decimal(10 ** 40):
                bad.append((str(z), str(lhs)[:24], str(rhs)[:24]))
        return not bad, {"points": 5, "violations": bad}

    check("SRC18_the_entropy_minus_z_times_its_derivative_is_log_of_one_plus_z",
          variational_identity,
          "§23: H(z) - z H'(z) = log2(1+z), which is what forces F' > 0")

    def variational_ratio_increases():
        bad, prev = [], None
        xs = [Decimal(k) / 1000 for k in range(1, 57)]
        for x in xs:
            f = A.variational_ratio(x)
            if prev is not None and f <= prev:
                bad.append(str(x))
            prev = f
        return (not bad and len(xs) > 10), {"points": len(xs), "decreases_at": bad[:5]}

    check("SRC18_the_variational_ratio_is_strictly_increasing",
          variational_ratio_increases, "§23: F(x) = x/H(gamma+x) has F' > 0")

    # -------------------------------------- §20-§25: the root and constant
    def root_bracket():
        h_gamma = A.packing_entropy(GAMMA_D)
        h_one = A.packing_entropy(Decimal(1))
        return (h_gamma < BETA_D < h_one
                and str(h_gamma).startswith("1.5056438879")
                and abs(h_one - 2) < Decimal(1) / Decimal(10 ** 40)), {
            "H_gamma": str(h_gamma)[:22], "beta": str(BETA_D)[:22],
            "H_one": str(h_one)[:22]}

    check("SRC18_the_entropy_root_is_bracketed_by_gamma_and_one", root_bracket,
          "§20: H(gamma) = 1.5056438879... < beta < 2 = H(1), so a unique root "
          "exists in between")

    def constants_reproduce():
        # the bundled JSON was produced by mpmath.findroot; this is bisection in
        # the standard library's decimal — different library, different method
        z = A.entropy_root(DIGITS)
        x = z - GAMMA_D
        c = A.packing_constant(DIGITS)
        agree, mismatched = {}, []
        for key, mine in (("beta_log2_3", BETA_D), ("gamma_beta_minus_1", GAMMA_D),
                          ("z_star", z), ("x_star", x), ("c_pack", c)):
            theirs = consts.get(key, "")
            a, b = str(+mine), theirs
            n = 0
            while n < min(len(a), len(b)) and a[n] == b[n]:
                n += 1
            agree[key] = n
            if n < 50:
                mismatched.append((key, a[:30], b[:30]))
        measured["constants"] = {"digits_agreeing": agree,
                                 "c_pack": str(+c)[:34],
                                 "method": "decimal bisection vs mpmath findroot"}
        return (not mismatched and min(agree.values()) >= 50), {
            "digits_agreeing": agree, "mismatched": mismatched}

    check("SRC18_the_bundled_constants_reproduce_under_a_different_method",
          constants_reproduce,
          "the artifact is checked as an artifact: recomputed independently to "
          "at least 50 digits, not re-run")

    def root_signs_match():
        lo, hi = (Decimal(s) for s in consts["root_bracket"])
        s_lo = A.packing_entropy(GAMMA_D + lo) - BETA_D
        s_hi = A.packing_entropy(GAMMA_D + hi) - BETA_D
        want_lo, want_hi = (Decimal(s) for s in consts["root_signs"])
        return (s_lo < 0 < s_hi
                and abs(s_lo - want_lo) < Decimal(1) / Decimal(10 ** 40)
                and abs(s_hi - want_hi) < Decimal(1) / Decimal(10 ** 40)), {
            "sign_low": str(s_lo)[:24], "sign_high": str(s_hi)[:24],
            "straddles": bool(s_lo < 0 < s_hi)}

    check("SRC18_the_published_root_bracket_really_straddles_the_root",
          root_signs_match,
          "the JSON records both sign values; they must be reproducible and of "
          "opposite sign")

    def safe_constant_witness():
        c = Decimal(consts["safe_constant"])
        x = Decimal(consts["safe_x"])
        a = c / x
        h = A.packing_entropy(GAMMA_D + x)
        return (h < BETA_D and a * h < 1 and c < A.packing_constant(DIGITS)
                and str(a) == consts["safe_a"]), {
            "a": str(a), "H_at_safe_x": str(h)[:20],
            "a_times_H": str(a * h)[:20], "below_c_pack": True}

    check("SRC18_the_explicit_safe_constant_satisfies_both_criteria",
          safe_constant_witness,
          "§26: c = 0.035, x = 0.056, a = 0.625 with H(gamma+x) < beta and aH < 1")

    def supremum_is_the_constant():
        # §24: F increasing on (0, x*) means sup F = F(x*) = x*/H(z*) = x*/beta
        x_star = A.entropy_root(DIGITS) - GAMMA_D
        f_at = A.variational_ratio(x_star)
        c = A.packing_constant(DIGITS)
        below = A.variational_ratio(x_star * Decimal("0.999"))
        return (abs(f_at - c) < Decimal(1) / Decimal(10 ** 40) and below < c), {
            "F_at_x_star": str(f_at)[:24], "c_pack": str(c)[:24],
            "F_just_below": str(below)[:24]}

    check("SRC18_the_variational_supremum_equals_the_published_constant",
          supremum_is_the_constant,
          "§24: sup over the feasible interval is F(x*) = x*/beta = c_pack")

    def optimality_boundary():
        # §27: past x* the second term cannot be o(N); at or above F(x) the first
        # cannot. Both failure modes must be exhibited, not asserted.
        x_star = A.entropy_root(DIGITS) - GAMMA_D
        above = x_star * Decimal("1.01")
        second_fails = A.packing_entropy(GAMMA_D + above) >= BETA_D
        x = x_star / 2
        c_too_big = A.variational_ratio(x) * Decimal("1.01")
        a = c_too_big / x
        first_fails = a * A.packing_entropy(GAMMA_D + x) >= 1
        return (second_fails and first_fails), {
            "x_above_star_breaks_second_term": second_fails,
            "c_above_F_breaks_first_term": first_fails}

    check("SRC18_both_sides_of_the_optimality_boundary_really_fail",
          optimality_boundary,
          "§27: the envelope is maximal because each side of x* kills a different "
          "packing term")

    # ----------------------------------------------- ledger and provenance
    def unproved_list():
        tail = au2b1[au2b1.find("## 未證"):] if "## 未證" in au2b1 else ""
        want = ["CASP", "Terras", "Collatz"]
        missing = [w for w in want if w not in tail]
        return (bool(tail) and not missing), {"missing": missing}

    check("SRC18_the_paper_lists_casp_terras_and_collatz_as_unproved",
          unproved_list, "§35")

    check("SRC18_the_route_map_carries_the_same_constant",
          lambda: (("0.03585676003404866" in routemap
                    and "0.03585676003404866" in au2b1
                    and "0.035" in routemap),
                   {"routemap_len": len(routemap)}),
          "v1.2 must publish the same c_pack and the same safe constant")

    check("SRC18_the_paper_states_the_method_boundary",
          lambda: (("Method optimality" in au2b1 or "Method-Optimality" in au2b1
                    or "Method Optimality" in au2b1)
                   and "Method boundary" in routemap,
                   {}),
          "§27-§28: a sharp constant must say what would be needed to beat it")

    def script_matches_its_output():
        # the bundled script and JSON must agree about what was computed; this
        # does NOT run the script, it reads what it claims to write
        src = raw.get(SCRIPT, b"").decode("utf-8")
        keys = ["z_star", "x_star", "c_pack", "safe_constant", "root_bracket",
                "root_signs"]
        missing = [k for k in keys if f'"{k}"' not in src]
        return (bool(src) and not missing and set(keys) <= set(consts)), {
            "keys_absent_from_the_script": missing,
            "script_bytes": len(src)}

    check("SRC18_the_bundled_script_and_json_describe_the_same_quantities",
          script_matches_its_output,
          "the artifact ships a generator and its output; they must at least "
          "name the same fields")

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
        for pat in ("Hard_Zeta_Phase_II_Round_AU1_bundle.zip",
                    "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip",
                    "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip"):
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
        return (not edited and len(same) == 3 and len(fresh) == 6), {
            "reshipped_identical": len(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh)}

    check("SRC18_the_bundle_reships_its_predecessors_unedited", bundle_faithful,
          "the three predecessor rounds must be byte-identical; SIX files are "
          "new — the paper, the route map, the verification script, the "
          "constants JSON and two figures")

    # ------------------------------------------------------ own measurement
    def scheme_comparison():
        # RUN-015 measured A-U.2b's ceiling and said tuning stops there. This
        # round changed the argument. By how much, and is the new constant itself
        # at its own ceiling or below it?
        c = A.packing_constant(DIGITS)
        safe = Decimal(consts["safe_constant"])
        rows = {
            "au2b_published": 0.01,
            "au2b_scheme_ceiling_measured_in_run_015": float(AU2B_SCHEME_CEILING),
            "au2b1_published_c_pack": float(c),
            "au2b1_safe_constant": float(safe),
            "gain_over_the_old_ceiling": float(c / AU2B_SCHEME_CEILING),
            "au2b_published_as_fraction_of_its_ceiling":
                float(Decimal("0.01") / AU2B_SCHEME_CEILING),
            "au2b1_safe_as_fraction_of_its_ceiling": float(safe / c),
        }
        measured["scheme_comparison"] = {
            "rows": rows,
            "reading": ("RUN-015 measured the previous scheme's ceiling at "
                        "0.01502 and said passing it needed a different argument, "
                        "not tuning. Multi-occurrence packing is that argument, "
                        "and it reaches 2.39x the old ceiling. Note also the "
                        "tightness: A-U.2b published 67% of what its own scheme "
                        "allowed, while A-U.2b.1 publishes the supremum itself "
                        "and rounds down only for the explicit witness.")}
        return (c > AU2B_SCHEME_CEILING and float(c / AU2B_SCHEME_CEILING) > 2
                and safe / c > Decimal("0.95")), {"rows": rows}

    check("SRC18_the_new_argument_passes_the_previous_schemes_measured_ceiling",
          scheme_comparison,
          "measurement: RUN-015's ceiling against this round's constant, and how "
          "tightly each round publishes against its own limit")

    rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
    rep["counts"] = {"checks": len(checks),
                     "passed": sum(1 for v in checks.values() if v["pass"]),
                     "spines": len(SPINES), "digits": DIGITS}
    rep["ok"] = not rep["failures"]
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
