"""Recheck of source item 31 — Phase II / Round A-U.1, Anchor Erasure.

數學戰士「墜衡」 / AMRAL Research Lab.

A-U.1 is a **negative** round. It opens the first horn of Round 03-A.5's
dichotomy, proves that a critical A-U candidate must produce an invariant
measure with mean valuation exactly β — and then proves that this cannot
finish, by exhibiting two countermodels:

  §13  a Bernoulli measure on {1,2} with Pr(2) = γ, invariant, mean β, UI free;
  §15  the mechanical code q*_m = ⌊βm⌋ − ⌊β(m−1)⌋, subcritical at every prefix.

Both are checkable exactly, and both are checked here. What survives is the
anchor cocycle `r̂_{m+1} = r̂_m + t_{m+1}·2^{K_m+1}`, which an occupation measure
does not carry — so this run measures the thing the no-go says is load-bearing:
whether the lift digits actually distinguish a genuine integer from the
mechanical code.

Everything decidable is decided in exact integers or Fractions.

Usage:  python code/src15_hardzeta_au1_recheck.py
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
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))

A = importlib.import_module(os.environ.get("HZ_ACCEL_MODULE", "hz_accel_code"))

BUNDLE = "Hard_Zeta_Phase_II_Round_AU1_bundle.zip"
AU1 = "Hard_Zeta_Phase_II_Round_AU1_Critical_Occupation_Anchor_Erasure_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v0.9_AU1.md"

SPINES = [27, 103, 703, 1407, 10087, 15039, 35655]
DEPTH = 60                 # anchor-cocycle depth; the mechanical source is huge
BETA = math.log2(3)


def read_sources() -> dict[str, str]:
    out = {}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        for n in z.namelist():
            if n.endswith("/"):
                continue
            out[pathlib.PurePosixPath(n).name] = z.read(n).decode("utf-8")
    return out


def main() -> int:
    rep = {
        "tool": "src15_hardzeta_au1_recheck.py",
        "subject": "Hard_Zeta_Phase_II_Round_AU1_bundle.zip (item 31) — Round "
                   "A-U.1 plus A_Line_ROUTE_MAP v0.9",
        "source_items": [31],
        "scope": "the exponent-code conjugacy, the singular neighbourhoods the "
                 "invariant-limit theorem runs through, the two countermodels "
                 "behind the Pure Occupation No-Go, and the anchor cocycle the "
                 "Anchor-Erasure No-Go says is load-bearing",
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
    au1, routemap = docs.get(AU1, ""), docs.get(ROUTEMAP, "")

    # ------------------------------------------------ §1-§5: the conjugacy
    def cylinder_is_exact():
        bad, tested = [], 0
        for kappa in [(1,), (2, 1), (1, 2, 1), (3, 1, 1, 2), (1, 1, 1, 1, 1),
                      (2, 3, 1, 1, 2)]:
            r, mod = A.code_cylinder(kappa)
            for t in range(8):                       # inside the cylinder
                n = r + t * mod
                tested += 1
                if n % 2 == 0 or A.accel_code(n, len(kappa)) != kappa:
                    bad.append(("in", kappa, n))
            outside = 0                              # and just outside it
            for off in range(1, 6):
                n = r + off * (mod // 2)
                if n % 2 == 0 or n == r:
                    continue
                tested += 1
                if A.accel_code(n, len(kappa)) != kappa:
                    outside += 1
            if outside == 0:
                bad.append(("no_outside_witness", kappa, None))
        return (not bad and tested > 0), {"starts_tested": tested,
                                          "violations": bad[:5]}

    check("SRC15_a_finite_code_is_exactly_one_clopen_cylinder", cylinder_is_exact,
          "§2: Omega_hat = r_m + 2^{K_m+1} Z_2 — membership must be sufficient "
          "AND the complement must contain non-members")

    def cylinders_nest():
        bad, tested = [], 0
        for n in SPINES:
            kappa = A.accel_code(n, 24)
            for m in range(1, 24):
                r_m, mod_m = A.code_cylinder(kappa[:m])
                r_next, mod_next = A.code_cylinder(kappa[:m + 1])
                tested += 1
                if r_next % mod_m != r_m or mod_next <= mod_m:
                    bad.append((n, m))
        return (not bad and tested > 0), {"nestings": tested, "violations": bad[:5]}

    check("SRC15_exact_cylinders_nest_as_the_code_extends", cylinders_nest,
          "§3: extending a code shrinks its cylinder inside the parent, and the "
          "diameter 2^{-(K_m+1)} strictly decreases")

    def intertwines():
        bad, tested = [], 0
        for n in SPINES + [15, 31, 63, 12345, 999999]:
            kappa = A.accel_code(n, 20)
            y = n
            for m in range(1, 12):
                q = kappa[m - 1]
                y = (3 * y + 1) >> q                 # one accelerated step
                tested += 1
                if A.accel_code(y, 8) != A.shift_code(kappa[m - 1:])[:8]:
                    bad.append((n, m))
        return (not bad and tested > 0), {"steps": tested, "violations": bad[:5]}

    check("SRC15_the_code_map_intertwines_with_the_shift", intertwines,
          "§5: E(Sx) = sigma E(x), checked by iterating S on integers")

    def arbitrary_codes_realized():
        bad, tested = [], 0
        # deliberately NOT subcritical, and with large valuations, because §4
        # claims every element of N_{>=1}^N is realized, not merely legal ones
        for kappa in [(7,), (1, 9), (12, 1, 5), (2, 2, 11, 1), (5, 5, 5),
                      (1, 1, 20), (17, 3)]:
            r, _ = A.code_cylinder(kappa)
            tested += 1
            if r % 2 == 0 or A.accel_code(r, len(kappa)) != kappa:
                bad.append(kappa)
        return (not bad and tested > 0), {"codes": tested, "violations": bad}

    check("SRC15_every_finite_code_including_large_valuations_is_realized",
          arbitrary_codes_realized,
          "§4: the alphabet is all of N_{>=1}, so unbounded and supercritical "
          "codes must be realized too")

    # -------------------------------------- §7-§10: singular neighbourhoods
    def singular_cylinders():
        bad, hi, lo = [], 0, 0
        for y in range(1, 30000, 2):
            q = A.accel_code(y, 1)[0]
            for r in range(2, 9):
                member = A.in_singular_cylinder(y, r)
                if member != (q >= r):
                    bad.append((y, r))
                hi += member
                lo += not member
        nest = all(A.singular_cylinder(r + 1)[0] % (1 << r)
                   == A.singular_cylinder(r)[0] for r in range(2, 20))
        return (not bad and nest and hi > 0 and lo > 0), {
            "violations": bad[:5], "cylinders_nest": nest,
            "in_C_r": hi, "outside_C_r": lo, "_both_outcomes_seen": hi > 0 and lo > 0}

    check("SRC15_the_singular_cylinders_nest_and_are_exactly_high_valuation",
          singular_cylinders,
          "§7: C_r is one clopen class, C_{r+1} inside C_r, membership iff q >= r")

    def truncated_observable():
        bad, tested = [], 0
        for y in range(1, 20000, 2):
            q = A.accel_code(y, 1)[0]
            for R in range(2, 10):
                g = sum(1 for r in range(2, R + 1) if A.in_singular_cylinder(y, r))
                tested += 1
                if g != min(q - 1, R - 1):
                    bad.append((y, R))
        return (not bad and tested > 0), {"points": tested, "violations": bad[:5]}

    check("SRC15_the_truncated_observable_is_the_clipped_valuation",
          truncated_observable,
          "§10: g_R = sum of indicators of C_2..C_R equals min(q-1, R-1), which "
          "is what makes it bounded continuous")

    def singular_mass_bound():
        gamma = BETA - 1
        rows, bad = [], []
        for n in SPINES:
            m = A.subcritical_lifetime(n)
            qs = A.orbit_valuations(n, m)
            for R in range(2, 8):
                share = Fraction(sum(1 for q in qs if q >= R), m)
                bound = Fraction(A.excess(n, m), m) / (R - 1)
                if share > bound:
                    bad.append({"n": n, "R": R, "share": str(share),
                                "bound": str(bound)})
                if R == 3:
                    rows.append({"n": n, "m": m, "nu_m_C3": float(share),
                                 "bound": float(bound),
                                 "gamma_over_R_minus_1": gamma / (R - 1)})
        measured["singular_mass"] = rows
        return not bad, {"violations": bad[:5], "sample": rows[:3]}

    check("SRC15_the_singular_mass_bound_holds_on_real_spines",
          singular_mass_bound,
          "§8: nu_m(C_R) <= (1/m)sum(q_i-1)/(R-1); checked against the run's own "
          "measured excess rather than against gamma, which is only the limit")

    # ------------------------------ §13-§17: the two occupation countermodels
    def bernoulli_mean():
        # gamma is irrational, so the identity mean = 1 + p is checked on exact
        # rationals bracketing it, plus the general identity at many p.
        bad = []
        for num, den in [(3, 5), (7, 12), (12, 19), (53, 84), (1, 2), (0, 1), (1, 1)]:
            got = A.bernoulli_mean_valuation(num, den)
            if got != 1 + Fraction(num, den):
                bad.append((num, den, str(got)))
        # gamma is irrational so p = gamma is not a Fraction; the identity is
        # pinned instead by rationals that bracket it from both sides
        lo = A.bernoulli_mean_valuation(53, 91)     # 53/91 = 0.5824 < gamma
        hi = A.bernoulli_mean_valuation(12, 19)     # 12/19 = 0.6316 > gamma
        brackets = float(lo) < BETA < float(hi)
        return (not bad and brackets), {
            "identity_violations": bad,
            "mean_at_p_below_gamma": float(lo), "beta": BETA,
            "mean_at_p_above_gamma": float(hi),
            "note": "q <= 2 makes uniform integrability automatic, as §13 says"}

    check("SRC15_the_bernoulli_critical_measure_has_mean_beta", bernoulli_mean,
          "§13: mean of (1-p)delta_1 + p delta_2 is 1 + p, so p = gamma gives beta")

    def mechanical_matches_formula():
        # RUN-008 implemented this code from Round 03-A.1; A-U.1 §15 states it
        # independently. The two must be the same sequence.
        a = A.mechanical_code(300)
        b = tuple(A.mechanical_valuation(j) for j in range(1, 301))
        return a == b, {"terms_compared": 300, "first_disagreement":
                        next((j for j in range(300) if a[j] != b[j]), None)}

    check("SRC15_the_mechanical_code_matches_its_stated_formula",
          mechanical_matches_formula,
          "cross-check: Round 03-A.1's implementation against A-U.1 §15's formula")

    def mechanical_telescopes():
        bad = [m for m in range(1, 301)
               if A.cumulative(A.mechanical_code(m))[-1] != A.floor_beta(m)]
        return not bad, {"m_range": "1..300", "violations": bad[:5]}

    check("SRC15_the_mechanical_cumulative_telescopes_to_floor_beta",
          mechanical_telescopes, "§15: K*_m = floor(beta m)")

    def mechanical_subcritical():
        # 3^m < 2^{K+1} is exactly K = floor(beta m) >= beta m - 1 < beta m, done
        # in integers so no float decides it
        bad = [m for m in range(1, 301)
               if not (3 ** m > 2 ** A.cumulative(A.mechanical_code(m))[-1])]
        return not bad, {"m_range": "1..300", "violations": bad[:5]}

    check("SRC15_the_mechanical_code_is_subcritical_at_every_prefix",
          mechanical_subcritical, "§15: K*_m < beta m for every m, i.e. 2^{K*_m} < 3^m")

    def mechanical_alphabet():
        vals = {A.mechanical_valuation(j) for j in range(1, 2001)}
        return vals == {1, 2}, {"symbols_seen": sorted(vals)}

    check("SRC15_the_mechanical_code_uses_only_the_two_symbol_alphabet",
          mechanical_alphabet, "§15: 1 < beta < 2 forces q* in {1,2}")

    def mechanical_frequency():
        gamma = BETA - 1
        rows = [{"m": m, "two_frequency": float(A.mechanical_two_frequency(m)),
                 "gap_from_gamma": abs(float(A.mechanical_two_frequency(m)) - gamma)}
                for m in (100, 500, 2000, 8000)]
        measured["mechanical_two_frequency"] = rows
        shrinking = all(rows[i + 1]["gap_from_gamma"] <= rows[i]["gap_from_gamma"] + 1e-9
                        for i in range(len(rows) - 1))
        return (rows[-1]["gap_from_gamma"] < 1e-3 and shrinking), {
            "rows": rows, "gamma": gamma}

    check("SRC15_the_mechanical_two_frequency_converges_to_gamma",
          mechanical_frequency,
          "§17: the mechanical code's 2-density is gamma, so its mean exponent "
          "is beta and it pulls back to a critical invariant measure")

    # ------------------------------------- §18-§23: anchor blindness
    def dense_but_not_closed():
        # "every odd residue class contains a positive odd integer" is a
        # TAUTOLOGY — r is odd, 2^k is even, so r + t·2^k is odd for every t. It
        # cannot fail and was replaced. §18's content is the second sentence:
        # N_odd is dense but NOT closed. The mechanical code witnesses exactly
        # that — its canonical sources are positive odd integers, 2-adically
        # Cauchy (each is the next one's residue), and unbounded in R.
        mech = A.mechanical_code(DEPTH)
        rs = [A.source_residue(mech[:m]) for m in range(1, DEPTH + 1)]
        Ks = [A.cumulative(mech[:m])[-1] for m in range(1, DEPTH + 1)]
        all_odd = all(r % 2 == 1 for r in rs)
        cauchy = all(rs[m] % (1 << (Ks[m - 1] + 1)) == rs[m - 1]
                     for m in range(1, DEPTH))
        unbounded = rs[-1] > rs[0] * 2 ** 80
        return (all_odd and cauchy and unbounded), {
            "all_positive_odd_integers": all_odd,
            "two_adically_cauchy": cauchy, "diverges_in_the_reals": unbounded,
            "first_source": rs[0], "bits_at_depth": rs[-1].bit_length()}

    check("SRC15_the_positive_integers_are_dense_but_not_closed", dense_but_not_closed,
          "§18: a 2-adically convergent sequence of positive integers whose real "
          "size diverges is what makes the limit escape N_odd")

    def cylinders_hold_integers():
        bad = []
        for kappa in [(1, 2, 1), (2, 1, 3), (1, 1, 1, 1), (3, 2, 1, 1)]:
            lifts = A.code_lifts(kappa, 25)
            if len(lifts) != 25 or any(
                    A.accel_code(n, len(kappa)) != kappa for n in lifts):
                bad.append(kappa)
        return not bad, {"codes": 4, "lifts_each": 25, "violations": bad}

    check("SRC15_every_finite_cylinder_holds_infinitely_many_positive_integers",
          cylinders_hold_integers,
          "§19: so no finite-prefix observable can decide anchoring")

    def cocycle_recursion():
        bad, tested = [], 0
        for kappa in [A.accel_code(n, 20) for n in SPINES] + [A.mechanical_code(20)]:
            for m in range(1, 20):
                r_m = A.source_residue(kappa[:m])
                r_next = A.source_residue(kappa[:m + 1])
                t = A.lift_digit(kappa[:m + 1])
                K_m = A.cumulative(kappa[:m])[-1]
                tested += 1
                if r_next != r_m + t * 2 ** (K_m + 1):
                    bad.append((kappa[:3], m))
        return (not bad and tested > 0), {"lifts": tested, "violations": bad[:5]}

    check("SRC15_the_anchor_cocycle_recursion_is_exact", cocycle_recursion,
          "§21, §26: r_{m+1} = r_m + t_{m+1} 2^{K_m+1}, in exact integers")

    def anchor_is_eventually_zero():
        # both directions, and both outcomes must appear: a genuine integer must
        # settle to t = 0, and the code must show nonzero lifts before it does
        bad, rows, saw_zero, saw_nonzero = [], [], 0, 0
        for n in SPINES:
            kappa = A.accel_code(n, DEPTH)
            t = A.anchor_cocycle(kappa)
            settle = next((j for j in range(len(t))
                           if all(x == 0 for x in t[j:])), None)
            if settle is None:
                bad.append({"n": n, "never_settled": True})
                continue
            saw_zero += 1
            saw_nonzero += any(x != 0 for x in t[:settle])
            # once settled, the canonical source must BE the integer — and the
            # settling point must be SHARP, or the index is unpinned and a
            # one-place shift in the cocycle passes unnoticed
            if A.source_residue(kappa[:settle + 1]) != n:
                bad.append({"n": n, "source_is_not_the_integer": True})
            # sharpness: the source must already be n AT the settling point, not
            # merely one step later. Without this a cocycle shifted by one place
            # still passes, because r_{s+1} = r_s = n on a settled orbit.
            if settle > 0 and A.source_residue(kappa[:settle]) != n:
                bad.append({"n": n, "settling_point_is_not_sharp": True})
            rows.append({"n": n, "lift_settles_at_m": settle,
                         "nonzero_lifts_before": sum(1 for x in t[:settle] if x)})
        measured["integer_anchors"] = rows
        return (not bad and saw_zero > 0 and saw_nonzero > 0), {
            "spines": len(rows), "violations": bad[:3],
            "settled": saw_zero, "had_nonzero_lifts_first": saw_nonzero,
            "_both_outcomes_seen": saw_zero > 0 and saw_nonzero > 0}

    check("SRC15_a_positive_integer_anchor_is_exactly_an_eventually_zero_lift",
          anchor_is_eventually_zero,
          "§21: t_m = 0 eventually, and once it settles the canonical source is "
          "the integer itself")

    # --------------------------------------------------- ledger and bundle
    check("SRC15_the_paper_keeps_an_explicit_proved_and_unproved_ledger",
          lambda: ("## 已證" in au1 and "## 未證" in au1,
                   {"has_both": "## 已證" in au1 and "## 未證" in au1}),
          "§32")

    def unproved_list():
        tail = au1[au1.find("## 未證"):] if "## 未證" in au1 else ""
        want = ["Pointed Critical Occupation Rigidity", "CASP exclusion",
                "Terras", "Collatz"]
        missing = [w for w in want if w not in tail]
        return not missing, {"missing_from_the_unproved_list": missing}

    check("SRC15_the_paper_lists_terras_and_collatz_as_unproved", unproved_list,
          "§32: the no-go must not be allowed to read as progress on the "
          "conjecture itself")

    check("SRC15_the_route_map_and_the_paper_agree_on_the_no_go",
          lambda: (("Pure occupation no-go" in routemap
                    and "Anchor-Erasure No-Go" in au1
                    and "t_m=0" in routemap.replace(" ", "")),
                   {"routemap_len": len(routemap)}),
          "v0.9 must carry the same verdict and the same missing condition")

    def bundle_faithful():
        def members(path):
            out = {}
            with zipfile.ZipFile(path) as z:
                for n in z.namelist():
                    if n.endswith("/"):
                        continue
                    out[pathlib.PurePosixPath(n).name] = hashlib.sha256(
                        z.read(n)).hexdigest()
            return out

        big = members(SOURCE / BUNDLE)
        earlier = {p.name: members(p) for p in sorted(
            SOURCE.glob("Hard_Zeta_*Rounds_01_03A5*.zip"))}
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
        return (not edited and len(same) >= 2 and len(fresh) == 2), {
            "reshipped_identical": len(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh)}

    check("SRC15_the_bundle_reships_phase_i_unedited", bundle_faithful,
          "item 31 re-ships the closure and 03A5 already verified as item 30; "
          "they must be byte-identical, and exactly two files new")

    # ------------------------------------------------------ own measurement
    def cocycle_separates():
        # §16 declines to decide whether the mechanical point is an ordinary
        # positive integer, calling it the anchor-sensitive question. This does
        # not decide it either — it measures how far the anchor cocycle gets.
        mech = A.mechanical_code(DEPTH)
        t_mech = A.anchor_cocycle(mech)
        nonzero = [j + 1 for j, x in enumerate(t_mech) if x]
        tail_nonzero = [j for j in nonzero if j > 12]
        rows = []
        for m in (8, 16, 24, 40, DEPTH):
            r = A.source_residue(mech[:m])
            rows.append({"m": m, "source_bits": r.bit_length(),
                         "K_m": A.cumulative(mech[:m])[-1],
                         "source": r if r < 10 ** 12 else None})
        measured["mechanical_anchor"] = {
            "depth": DEPTH,
            "lift_digits": t_mech,
            "nonzero_lifts": len(nonzero),
            "last_nonzero_at_m": nonzero[-1] if nonzero else None,
            "source_growth": rows,
            "reading": ("no positive integer below 2^{K_m+1} realizes the "
                        "mechanical code to this depth; that is not a proof that "
                        "none exists, and §16 is right to leave it open"),
        }
        # a genuine integer settles; the mechanical code must still be lifting
        # deep into the tail, or the separation this run reports is not there
        return (bool(tail_nonzero) and len(nonzero) > DEPTH // 3), {
            "nonzero_lifts": len(nonzero), "of_depth": DEPTH,
            "still_lifting_past_m12": len(tail_nonzero),
            "integer_spines_settle_by": max(
                r["lift_settles_at_m"] for r in measured.get("integer_anchors", [])
                or [{"lift_settles_at_m": -1}])}

    check("SRC15_the_anchor_cocycle_separates_the_mechanical_code_from_integers",
          cocycle_separates,
          "measurement: the datum §22 says occupation measures do not carry, "
          "evaluated on both a genuine integer and the countermodel")

    def mechanical_source_grows():
        mech = A.mechanical_code(DEPTH)
        bits = [A.source_residue(mech[:m]).bit_length() for m in range(1, DEPTH + 1)]
        rising = sum(1 for i in range(len(bits) - 1) if bits[i + 1] >= bits[i])
        measured["mechanical_source_bits"] = {
            "at_m": {str(m): bits[m - 1] for m in (8, 16, 24, 32, 40, 48, DEPTH)},
            "monotone_steps": rising, "of": len(bits) - 1}
        return (bits[-1] > 4 * bits[7] and rising == len(bits) - 1), {
            "bits_at_m8": bits[7], "bits_at_depth": bits[-1],
            "monotone_nondecreasing": rising == len(bits) - 1}

    check("SRC15_the_mechanical_source_grows_without_settling",
          mechanical_source_grows,
          "measurement: RUN-008 saw this source pass 29 million by m=16; here it "
          "is followed to the anchor-cocycle depth")

    rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
    rep["counts"] = {"checks": len(checks),
                     "passed": sum(1 for v in checks.values() if v["pass"]),
                     "spines": len(SPINES), "anchor_depth": DEPTH}
    rep["ok"] = not rep["failures"]
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
