"""Recheck of source item 32 — Phase II / Round A-U.2a, Lift-Occupation Coupling.

數學戰士「墜衡」 / AMRAL Research Lab.

A-U.1 left the anchor cocycle as the datum occupation theory cannot carry.
A-U.2a builds the algebra that couples it to the dynamics: an inverse-code
series for the source, a reading of the lift digit as a *block of the source's
binary expansion*, normalized pointed coordinates with exact recurrences, and a
flux balance tying mean lift to mean source height.

It then ends in a second no-go. Under the compact normalized coordinates every
positive-integer anchor collapses to `(X, Z, lambda) = (0,0,0)`, so the anchor
value is erased again — and the repair, an unbounded anchor height, is faithful
but noncompact.

Almost all of it is exact algebra, so almost all of it is checked exactly:
integers and Fractions, no floating point in any decision.

Usage:  python code/src16_hardzeta_au2a_recheck.py
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

BUNDLE = "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip"
AU2A = "Hard_Zeta_Phase_II_Round_AU2a_Lift_Occupation_Coupling_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.0_AU2a.md"

SPINES = [27, 103, 703, 1407, 10087, 15039, 35655]
DEPTH = 24
FLUX_M = 400          # the mechanical code is followed far enough to be stable
BETA = math.log2(3)


def read_sources() -> dict[str, str]:
    out = {}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                out[pathlib.PurePosixPath(n).name] = z.read(n).decode("utf-8")
    return out


def main() -> int:
    rep = {
        "tool": "src16_hardzeta_au2a_recheck.py",
        "subject": "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip (item 32) — Round "
                   "A-U.2a plus A_Line_ROUTE_MAP v1.0",
        "source_items": [32],
        "scope": "the inverse-code series and its functional equation, the Source "
                 "Block-Digit Theorem, the lift-endpoint amplification law, the "
                 "normalized pointed recurrences and their decoupling, the flux "
                 "balance and its zero-flux boundary, and the two completions "
                 "that share every finite datum with a genuine anchor",
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
    au2a, routemap = docs.get(AU2A, ""), docs.get(ROUTEMAP, "")
    codes = [A.accel_code(n, DEPTH) for n in SPINES] + [A.mechanical_code(DEPTH)]

    # ------------------------------------------- §1-§2: the inverse-code series
    def series_is_the_source():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH + 1):
                pre = kappa[:m]
                bits = A.cumulative(pre)[-1] + 1
                tested += 1
                if A.inverse_code_source(pre, bits) != A.source_residue(pre):
                    bad.append((pre[:4], m))
        return (not bad and tested > 0), {"prefixes": tested, "violations": bad[:5]}

    check("SRC16_the_inverse_code_series_converges_to_the_exact_source",
          series_is_the_source,
          "§1: B(q) = -sum_j 2^{K_j} 3^{-(j+1)}, summed to j = m inclusive because "
          "the j = m term is nonzero modulo 2^{K_m+1}")

    def functional_equation():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(2, DEPTH + 1):
                pre = kappa[:m]
                tail = A.shift_code(pre)
                q1 = pre[0]
                b_tail = A.cumulative(tail)[-1] + 1
                mod = 1 << (b_tail + q1)
                lhs = (3 * A.inverse_code_source(pre, b_tail + q1) + 1) % mod
                rhs = ((1 << q1) * A.inverse_code_source(tail, b_tail)) % mod
                tested += 1
                if lhs != rhs:
                    bad.append((pre[:4], m))
        return (not bad and tested > 0), {"prefixes": tested, "violations": bad[:5]}

    check("SRC16_the_source_satisfies_the_shift_functional_equation",
          functional_equation,
          "§2: 3 B(q) + 1 = 2^{q_1} B(sigma q), at the precision the shifted code "
          "actually determines")

    # ----------------------------------- §5: the Source Block-Digit Theorem
    def block_digits():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(DEPTH):
                tested += 1
                if A.block_digit(kappa, m) != A.lift_digit(kappa[:m + 1]):
                    bad.append((kappa[:4], m))
        return (not bad and tested > 0), {"digits": tested, "violations": bad[:5]}

    check("SRC16_the_lift_digit_is_a_binary_block_of_the_source", block_digits,
          "§5: t_{m+1} read off the source's bits at positions K_m+1..K_{m+1} "
          "equals the lift computed as a difference of canonical representatives")

    def source_is_its_lift_series():
        bad, tested = [], 0
        for kappa in codes:
            K = A.cumulative(kappa)
            for m in range(1, DEPTH + 1):
                want = 1 + sum(A.lift_digit(kappa[:i]) * 2 ** (K[i - 1] + 1)
                               for i in range(1, m + 1))
                tested += 1
                if A.source_residue(kappa[:m]) != want:
                    bad.append((kappa[:4], m))
        return (not bad and tested > 0), {"prefixes": tested, "violations": bad[:5]}

    check("SRC16_the_source_is_one_plus_the_weighted_lift_series",
          source_is_its_lift_series,
          "§5: R_m = 1 + sum_i t_i 2^{K_{i-1}+1}, with R_0 = 1")

    def adelic_dichotomy():
        # both branches must appear: a genuine integer stabilises, the mechanical
        # code does not, and its heights must actually be climbing
        rows, stable, climbing = [], 0, 0
        deep = 60
        for n in SPINES:
            k = A.accel_code(n, deep)
            R = [A.source_residue(k[:m]) for m in range(1, deep + 1)]
            if R[-1] == R[-2] == n:
                stable += 1
            rows.append({"start": n, "final_R": R[-1], "stabilised": R[-1] == n})
        mech = A.mechanical_code(deep)
        Rm = [A.source_residue(mech[:m]) for m in range(1, deep + 1)]
        climbing = sum(1 for i in range(len(Rm) - 1) if Rm[i + 1] > Rm[i])
        measured["adelic_dichotomy"] = {
            "integers": rows, "mechanical_final_bits": Rm[-1].bit_length(),
            "mechanical_strict_increases": climbing}
        return (stable == len(SPINES) and climbing > deep // 2), {
            "stabilised": stable, "of": len(SPINES),
            "mechanical_strict_increases": climbing,
            "_both_outcomes_seen": stable > 0 and climbing > 0}

    check("SRC16_the_adelic_lift_dichotomy_separates_the_two_branches",
          adelic_dichotomy,
          "§7-§8: finitely many nonzero lifts means R_m is eventually a positive "
          "odd integer; infinitely many means R_m -> +infinity")

    # ---------------------------------- §9-§11: endpoints and amplification
    def offset_closed_form():
        # E being a positive odd integer CANNOT detect an error in B_m, because
        # R_m is derived from B_m and the two errors cancel inside E. So B_m is
        # checked against its own closed form, independently of R.
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH + 1):
                pre = kappa[:m]
                K = A.cumulative(pre)
                want = sum(3 ** (m - i) * 2 ** K[i - 1] for i in range(1, m + 1))
                tested += 1
                if A.offset(pre) != want:
                    bad.append((kappa[:4], m))
        return (not bad and tested > 0), {"prefixes": tested, "violations": bad[:5]}

    check("SRC16_the_affine_offset_matches_its_closed_form", offset_closed_form,
          "§9: B_m = sum_i 3^{m-i} 2^{K_{i-1}}, checked against the recurrence "
          "the rest of the module uses")

    def endpoint_is_positive_odd():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH + 1):
                E = A.prefix_endpoint(kappa[:m])
                tested += 1
                if E <= 0 or E % 2 == 0:
                    bad.append((kappa[:4], m, E))
        return (not bad and tested > 0), {"endpoints": tested, "violations": bad[:5]}

    check("SRC16_the_canonical_prefix_endpoint_is_a_positive_odd_integer",
          endpoint_is_positive_odd, "§9: E_m = (3^m R_m + B_m)/2^{K_m}")

    def amplification():
        bad, tested, nonzero = [], 0, 0
        for kappa in codes:
            for m in range(1, DEPTH):
                E = A.prefix_endpoint(kappa[:m])
                E_tilde = A.endpoint(A.source_residue(kappa[:m + 1]), kappa[:m])
                t = A.lift_digit(kappa[:m + 1])
                tested += 1
                nonzero += t > 0
                if E_tilde - E != 2 * t * 3 ** m:
                    bad.append((kappa[:4], m))
        # a law about lifts is untested where every lift is zero
        return (not bad and nonzero > 0), {
            "pairs": tested, "violations": bad[:5], "with_a_nonzero_lift": nonzero,
            "_observable_nonempty": nonzero > 0}

    check("SRC16_a_source_lift_amplifies_to_twice_it_times_three_to_the_m",
          amplification,
          "§10-§11: E~_m - E_m = 2 t_{m+1} 3^m; guarded so it is not graded only "
          "where every lift is zero")

    # ------------------------- §12-§15: pointed coordinates and decoupling
    def x_recurrence():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH):
                q = kappa[m]
                lhs = A.x_coord(kappa[:m + 1])
                rhs = A.x_coord(kappa[:m]) / 2 ** q + A.lift_flux(kappa, m)
                tested += 1
                if lhs != rhs:
                    bad.append((kappa[:4], m))
        return (not bad and tested > 0), {"steps": tested, "violations": bad[:5]}

    check("SRC16_the_source_coordinate_follows_its_skew_product_recurrence",
          x_recurrence, "§13: X_{m+1} = 2^{-q} X_m + lambda_{m+1}, in Fractions")

    def z_recurrence():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH):
                q, t = kappa[m], A.lift_digit(kappa[:m + 1])
                lhs = A.z_coord(kappa[:m + 1])
                rhs = (A.z_coord(kappa[:m]) + 2 * t
                       + Fraction(1, 3 ** (m + 1))) / 2 ** q
                tested += 1
                if lhs != rhs:
                    bad.append((kappa[:4], m))
        return (not bad and tested > 0), {"steps": tested, "violations": bad[:5]}

    check("SRC16_the_endpoint_coordinate_follows_its_skew_product_recurrence",
          z_recurrence,
          "§13: Z_{m+1} = (Z_m + 2t + 3^{-(m+1)}) / 2^q, in Fractions")

    def correction_closed_form():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH + 1):
                pre = kappa[:m]
                K = A.cumulative(pre)[-1]
                want = Fraction(A.offset(pre), 2 ** K * 3 ** m)
                got = A.correction_coord(pre)
                tested += 1
                if got != want or got <= 0:
                    bad.append((kappa[:4], m))
        return (not bad and tested > 0), {"prefixes": tested, "violations": bad[:5]}

    check("SRC16_the_correction_coordinate_is_the_affine_offset_normalized",
          correction_closed_form, "§14: C_m = Z_m - 2 X_m = B_m / (2^{K_m} 3^m) > 0")

    def correction_recurrence():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH):
                q = kappa[m]
                lhs = A.correction_coord(kappa[:m + 1])
                rhs = (A.correction_coord(kappa[:m])
                       + Fraction(1, 3 ** (m + 1))) / 2 ** q
                tested += 1
                if lhs != rhs:
                    bad.append((kappa[:4], m))
        return (not bad and tested > 0), {"steps": tested, "violations": bad[:5]}

    check("SRC16_the_correction_recurrence_does_not_mention_the_lift",
          correction_recurrence,
          "§14: C_{m+1} = (C_m + 3^{-(m+1)})/2^{q_{m+1}} — the lift digit is absent")

    def decoupling_is_sharp():
        # The recurrence not *mentioning* t is weaker than C being independent of
        # it. Two genuinely different sources sharing a code prefix must give the
        # same C_m, and the lifts distinguishing them must actually differ.
        bad, tested, distinct = [], 0, 0
        for kappa in codes[:4]:
            for m in range(1, 10):
                pre = kappa[:m]
                base = A.correction_coord(pre)
                lifts = A.code_lifts(pre, 6)
                if len({x for x in lifts}) < 2:
                    continue
                distinct += 1
                K = A.cumulative(pre)[-1]
                for n in lifts:
                    # C computed from THIS source, not from the canonical one:
                    # E/3^m - 2n/2^{K+1} must come out the same for every member
                    # of the cylinder, because the n terms cancel
                    C = Fraction(A.endpoint(n, pre), 3 ** m) - Fraction(n, 2 ** K)
                    tested += 1
                    if C != base:
                        bad.append((pre[:4], m, n, str(C), str(base)))
        return (not bad and distinct > 0 and tested > 0), {
            "cylinders": distinct, "sources_tested": tested,
            "violations": bad[:5], "_observable_nonempty": distinct > 0}

    check("SRC16_the_correction_is_the_same_for_every_source_in_a_cylinder",
          decoupling_is_sharp,
          "§14 sharp form: C_m is a function of the exponent code alone, so the "
          "lift enters only X — checked across distinct sources of one cylinder")

    def correction_bound():
        bad, tested = [], 0
        for kappa in codes:
            for m in range(1, DEPTH + 1):
                C = A.correction_coord(kappa[:m])
                cap = Fraction(1, 2 ** m) * (1 - Fraction(2 ** m, 3 ** m))
                tested += 1
                if not (0 < C <= cap < Fraction(1, 2 ** m)):
                    bad.append((kappa[:4], m, str(C), str(cap)))
        return (not bad and tested > 0), {"prefixes": tested, "violations": bad[:3]}

    check("SRC16_the_correction_obeys_the_exponential_synchronization_bound",
          correction_bound,
          "§15: 0 < C_m <= 2^{-m}[1 - (2/3)^m] < 2^{-m}, so Z_m = 2 X_m + O(2^{-m})")

    # ------------------------------------------ §17-§21: flux and collapse
    def flux_balance():
        bad, tested = [], 0
        for kappa in codes:
            for M in (6, 12, 18, DEPTH - 1):
                # the sum telescopes over X_0..X_{M-1}, with X_0 = 1/2 from the
                # empty prefix, and the boundary term is X_M - X_0
                lhs = sum(A.lift_flux(kappa, m) for m in range(M)) / M
                rhs = (sum((1 - Fraction(1, 2 ** kappa[m])) * A.x_coord(kappa[:m])
                           for m in range(M)) / M
                       + (A.x_coord(kappa[:M]) - A.x_coord(())) / M)
                tested += 1
                if lhs != rhs:
                    bad.append((kappa[:4], M, str(lhs), str(rhs)))
        return (not bad and tested > 0), {"windows": tested, "violations": bad[:3]}

    check("SRC16_the_lift_flux_balance_is_an_exact_identity", flux_balance,
          "§17: mean lambda = mean (1 - 2^{-q}) X + boundary/M, in Fractions")

    def mean_equivalence():
        rows, bad = [], []
        for label, kappa in [("mechanical", A.mechanical_code(FLUX_M))] + \
                            [(str(n), A.accel_code(n, 60)) for n in (27, 35655)]:
            M = len(kappa) - 1
            xb = sum(A.x_coord(kappa[:m]) for m in range(M)) / M
            lb = sum(A.lift_flux(kappa, m) for m in range(M)) / M
            bdry = abs(A.x_coord(kappa[:M]) - A.x_coord(())) / M
            if not (xb / 2 - bdry <= lb <= xb + bdry):
                bad.append(label)
            rows.append({"code": label, "M": M, "X_bar": float(xb),
                         "lambda_bar": float(lb), "half_X_bar": float(xb) / 2})
        measured["mean_equivalence"] = rows
        return not bad, {"rows": rows, "violations": bad}

    check("SRC16_mean_lift_is_bracketed_by_mean_source_height", mean_equivalence,
          "§18: (1/2) Xbar <= lambdabar <= Xbar up to the boundary term")

    def compact_collapse():
        rows, bad = [], []
        for n in SPINES:
            k = A.accel_code(n, 60)
            X = [float(A.x_coord(k[:m])) for m in range(1, 61)]
            Z = [float(A.z_coord(k[:m])) for m in range(1, 61)]
            lam = [A.lift_flux(k, m) for m in range(59)]
            settled = all(x == 0 for x in lam[20:])
            if not (X[-1] < 1e-12 and Z[-1] < 1e-12 and settled):
                bad.append(n)
            rows.append({"n": n, "X_60": X[-1], "Z_60": Z[-1],
                         "lambda_zero_after_m20": settled})
        measured["compact_collapse"] = rows
        return not bad, {"rows": rows[:3], "violations": bad}

    check("SRC16_every_positive_anchor_collapses_to_the_same_boundary_point",
          compact_collapse,
          "§21-§22: X_m = n/2^{K_m+1} -> 0, lambda eventually 0, Z_m -> 0, so the "
          "anchor value n is erased in compact coordinates")

    def anchor_height_criterion():
        bad, bounded, unbounded = [], 0, 0
        for n in SPINES:
            k = A.accel_code(n, 60)
            Aq = [A.anchor_height(k[:m]) for m in range(1, 61)]
            if not all(Aq[i + 1] >= Aq[i] for i in range(len(Aq) - 1)):
                bad.append(("not monotone", n))
            if Aq[-1] == Aq[-2] == n:
                bounded += 1
        mech = A.mechanical_code(60)
        Am = [A.anchor_height(mech[:m]) for m in range(1, 61)]
        if not all(Am[i + 1] >= Am[i] for i in range(len(Am) - 1)):
            bad.append(("not monotone", "mechanical"))
        if Am[-1] > Am[0] * 2 ** 40:
            unbounded += 1
        return (not bad and bounded == len(SPINES) and unbounded == 1), {
            "monotone_violations": bad, "bounded": bounded, "unbounded": unbounded,
            "_both_outcomes_seen": bounded > 0 and unbounded > 0}

    check("SRC16_the_anchor_height_is_monotone_and_bounded_only_when_it_settles",
          anchor_height_criterion,
          "§23-§24: A_m = R_m is integer monotone, so bounded iff eventually "
          "constant iff the lifts stop — faithful, but noncompact")

    # ------------------------------------ §27-§29: the rival completions
    def negative_completion():
        bad, tested = [], 0
        for kappa in codes[:5]:
            for m in (3, 5, 7, 9):
                pre = kappa[:m]
                x = A.negative_completion(pre)
                if x >= 0:
                    bad.append(("not negative", pre[:4], m))
                    continue
                y, seen = x, []
                for _ in range(m):
                    y, q = A.accel_step_rational(y)
                    seen.append(q)
                tested += 1
                if tuple(seen) != pre:
                    bad.append(("code mismatch", pre[:4], m, tuple(seen)))
                elif y != Fraction(-1):
                    bad.append(("did not reach -1", pre[:4], m, str(y)))
        return (not bad and tested > 0), {"completions": tested, "violations": bad[:3]}

    check("SRC16_the_negative_completion_shares_the_whole_finite_code",
          negative_completion,
          "§27: x_- = -(2^{K_m} + B_m)/3^m runs the same m valuations and lands on "
          "the accelerated fixed point -1")

    def critical_completion():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            for m in range(2, min(life, 12) + 1):
                pre = A.accel_code(n, m)
                d = A.deficit(n, m)
                ext = A.critical_completion(pre, 30)
                K = A.cumulative(ext)
                tested += 1
                for j in range(1, 31):
                    if K[m + j] != A.floor_beta(m + j) - d:
                        bad.append((n, m, j))
                        break
                    if not (3 ** (m + j) > 2 ** K[m + j]):
                        bad.append(("not subcritical", n, m, j))
                        break
        return (not bad and tested > 0), {"prefixes": tested, "violations": bad[:3]}

    check("SRC16_every_subcritical_prefix_extends_to_a_critical_completion",
          critical_completion,
          "§28: K_{m+j} = floor(beta(m+j)) - d_m < beta(m+j), so the formal "
          "critical continuation always exists")

    def sparse_lift_bound():
        # §25's counting bound, checked as the inequality it is
        bad, rows = [], []
        mech = A.mechanical_code(FLUX_M)
        M = FLUX_M
        lb = sum(A.lift_flux(mech, m) for m in range(M)) / M
        qbar = Fraction(A.cumulative(mech)[-1], M)
        dens = Fraction(sum(1 for m in range(M)
                            if A.lift_digit(mech[:m + 1]) > 0), M)
        for R in (2, 3, 4, 6):
            cap = 2 ** R * lb + qbar / R
            if dens > cap:
                bad.append({"R": R, "density": float(dens), "cap": float(cap)})
            rows.append({"R": R, "bound": float(cap)})
        measured["sparse_lift"] = {"lift_density": float(dens),
                                   "lambda_bar": float(lb),
                                   "q_bar": float(qbar), "bounds": rows}
        return not bad, {"density": float(dens), "violations": bad}

    check("SRC16_the_sparse_lift_counting_bound_holds", sparse_lift_bound,
          "§25: #{t_m>0}/M <= 2^R lambdabar + qbar/R for every R")

    # --------------------------------------------------- ledger and bundle
    check("SRC16_the_paper_keeps_an_explicit_proved_and_unproved_ledger",
          lambda: ("## 已證" in au2a and "## 未證" in au2a, {}),
          "§33")

    def unproved_list():
        tail = au2a[au2a.find("## 未證"):] if "## 未證" in au2a else ""
        want = ["CASP", "CST", "Collatz"]
        missing = [w for w in want if w not in tail]
        return not missing, {"missing_from_the_unproved_list": missing}

    check("SRC16_the_paper_lists_casp_cst_and_collatz_as_unproved", unproved_list,
          "§33: a second no-go must not read as progress on the conjecture")

    def quantifier_gap_stated():
        flat = au2a.replace(" ", "").replace("\n", "")
        return ("liftdensity0" in flat and "notonlyfinitelymanylifts" in flat
                or "\\not\\Rightarrow" in au2a), {
            "gap_marked": "\\not\\Rightarrow" in au2a}

    check("SRC16_the_paper_marks_its_own_quantifier_gap", quantifier_gap_stated,
          "the abstract states that zero lift density does NOT give finitely many "
          "lifts; that gap is the whole reason A-U.2b exists")

    check("SRC16_the_route_map_and_the_paper_agree_on_the_next_routes",
          lambda: (all(s in routemap for s in ("Sparse Lift Rigidity",
                                               "Busemann", "Transducer"))
                   and "A-U.2b" in au2a,
                   {"routemap_len": len(routemap)}),
          "v1.0 names the same three successor routes the paper does")

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
                    "Hard_Zeta_Phase_II_Round_AU1_bundle.zip"):
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
        return (not edited and len(same) >= 2 and len(fresh) == 2), {
            "reshipped_identical": len(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh)}

    check("SRC16_the_bundle_reships_its_predecessors_unedited", bundle_faithful,
          "the closure and A-U.1 must be byte-identical to items 30 and 31")

    # ------------------------------------------------------ own measurement
    def countermodel_has_positive_flux():
        # A-U.1's countermodel defeated occupation theory. Does A-U.2a's flux
        # machinery reach it? §26 splits candidates by lift flux, so measure it.
        mech = A.mechanical_code(FLUX_M)
        rows = []
        for M in (40, 80, 150, 250, FLUX_M):
            lb = sum(A.lift_flux(mech, m) for m in range(M)) / M
            xb = sum(A.x_coord(mech[:m + 1]) for m in range(M)) / M
            dens = Fraction(sum(1 for m in range(M)
                                if A.lift_digit(mech[:m + 1]) > 0), M)
            rows.append({"M": M, "lambda_bar": float(lb), "X_bar": float(xb),
                         "lift_density": float(dens)})
        measured["countermodel_flux"] = {
            "rows": rows,
            "reading": ("the mechanical code sits in §26's POSITIVE-lift-flux "
                        "class, which the Zero-Flux Boundary Theorem excludes. It "
                        "is therefore not a witness for the sparse-lift class, "
                        "which is the one A-U.2b has to exclude."),
        }
        stable = all(r["lambda_bar"] > 0.25 for r in rows)
        return stable, {"rows": rows, "stays_above_quarter": stable}

    check("SRC16_the_au1_countermodel_has_positive_lift_flux",
          countermodel_has_positive_flux,
          "measurement: which of §26's three classes the mechanical code falls in")

    def integers_versus_countermodel():
        # X_m for the countermodel OSCILLATES — it dips to 0.065 at m = 60 — so
        # the separation is stated on the mean, which is the stable statistic and
        # the one the occupation theory is actually about. The pointwise values
        # are reported, not asserted on.
        mech = A.mechanical_code(60)
        rows = []
        for m in (8, 16, 24, 40, 60):
            rows.append({"m": m,
                         "X_27": float(A.x_coord(A.accel_code(27, m))),
                         "X_35655": float(A.x_coord(A.accel_code(35655, m))),
                         "X_mechanical": float(A.x_coord(mech[:m]))})
        means = {}
        for label, kappa in [("27", A.accel_code(27, 60)),
                             ("35655", A.accel_code(35655, 60)),
                             ("mechanical", mech)]:
            means[label] = float(sum(A.x_coord(kappa[:m]) for m in range(30, 60))
                                 / 30)
        measured["compact_separation"] = {
            "pointwise": rows, "mean_X_over_m30_to_m59": means,
            "note": "the countermodel's pointwise X oscillates; the mean does not"}
        return (means["27"] < 1e-6 and means["35655"] < 1e-4
                and means["mechanical"] > 0.1), {"means": means, "pointwise": rows}

    check("SRC16_the_compact_coordinate_separates_anchors_from_the_countermodel",
          integers_versus_countermodel,
          "measurement: X_m -> 0 exponentially for genuine anchors while the "
          "countermodel stays order one — the coordinate separates, but it also "
          "collapses every anchor to the same point")

    rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
    rep["counts"] = {"checks": len(checks),
                     "passed": sum(1 for v in checks.values() if v["pass"]),
                     "codes": len(codes), "depth": DEPTH, "flux_window": FLUX_M}
    rep["ok"] = not rep["failures"]
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
