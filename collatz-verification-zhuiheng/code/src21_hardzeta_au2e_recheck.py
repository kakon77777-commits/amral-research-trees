"""Recheck of source item 37 — Phase II / Round A-U.2e, Multiscale Return Arithmetic.

數學戰士「墜衡」 / AMRAL Research Lab.

With the packing branch closed, this round stops counting and asks instead how
far a genuine positive-integer spine must *deviate from the mechanical critical
word*. The chain is short and almost entirely exact:

  d_m - d_{m-1} = a_m - q_m            deviation is the deficit's variation
  p_N(r) <= (r+1) + r J_N              each mismatch contaminates r windows
  N - r + 1 <= p_N(r)   when 2^{r+1} > M_N    return separation
  =>  J_N >= (N - 2r)/r

and a reset geometry whose affine identity, stated in the paper with the
irrational slack `delta_m = beta m - K_m`, clears to an identity between
integers — which is how it is checked here, with no floating point at all.

Usage:  python code/src21_hardzeta_au2e_recheck.py
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

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))

A = importlib.import_module(os.environ.get("HZ_ACCEL_MODULE", "hz_accel_code"))

BUNDLE = "Hard_Zeta_Phase_II_Round_AU2e_bundle.zip"
AU2E = "Hard_Zeta_Phase_II_Round_AU2e_Multiscale_Return_Arithmetic_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.5_AU2e.md"
PRED = "Hard_Zeta_Phase_II_Round_AU2b3_Queue_Prefactor_Saturation_v0.1.md"
PREV_BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b3_bundle.zip"

SPINES = [27, 103, 703, 1407, 10087, 15039, 35655]


def read_sources() -> dict[str, bytes]:
    out = {}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                out[pathlib.PurePosixPath(n).name] = z.read(n)
    return out


def main() -> int:
    rep = {
        "tool": "src21_hardzeta_au2e_recheck.py",
        "subject": "Hard_Zeta_Phase_II_Round_AU2e_bundle.zip (item 37) — Round "
                   "A-U.2e plus A_Line_ROUTE_MAP v1.5",
        "source_items": [37],
        "scope": "the mechanical deviation identity and its directional split, "
                 "the contamination bound and the mismatch barrier built on it, "
                 "the reset geometry cleared to exact integers, and the "
                 "one-sided deficit dichotomy",
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
    au2e = raw.get(AU2E, b"").decode("utf-8")
    routemap = raw.get(ROUTEMAP, b"").decode("utf-8")

    # ------------------------------- abstract: the deviation identity
    def deviation_identity():
        bad, tested = [], 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            q = A.accel_code(n, N)
            for m in range(1, N + 1):
                lhs = A.deficit(n, m) - (A.deficit(n, m - 1) if m > 1 else 0)
                rhs = A.mechanical_valuation(m) - q[m - 1]
                tested += 1
                if lhs != rhs:
                    bad.append((n, m, lhs, rhs))
        return (not bad and tested > 0), {"steps": tested, "violations": bad[:5]}

    check("SRC21_the_deficit_increment_is_the_mechanical_deviation",
          deviation_identity,
          "abstract: d_m - d_{m-1} = a_m - q_m, so the L1 deviation from the "
          "mechanical word IS the deficit path's total variation")

    def variation_equals_deviation():
        bad = []
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            c = A.deviation_counts(n, N)
            path = sum(abs(A.deficit(n, m) - (A.deficit(n, m - 1) if m > 1 else 0))
                       for m in range(1, N + 1))
            if c["V"] != path or c["J"] > c["V"]:
                bad.append((n, c["V"], path, c["J"]))
        return not bad, {"spines": len(SPINES), "violations": bad}

    check("SRC21_the_deviation_is_the_deficit_paths_total_variation",
          variation_equals_deviation, "V_N = sum |d_m - d_{m-1}|, and J_N <= V_N")

    # --------------------------------- §1: the directional split
    def directional_split():
        bad = []
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            c = A.deviation_counts(n, N)
            if (c["U"] - c["W"] != A.deficit(n, N)
                    or c["U"] + c["W"] != c["V"]):
                bad.append((n, c, A.deficit(n, N)))
        return not bad, {"spines": len(SPINES), "violations": bad}

    check("SRC21_the_two_directions_reconstruct_the_deficit_and_its_variation",
          directional_split, "§1: U - W = d_N and U + W = V_N")

    def skipped_credit_identity():
        # §1: a positive increment can only happen at a_m = 2, q_m = 1, and is
        # exactly 1 there. Both outcomes must occur or the identity is graded on
        # a sample with no upward steps at all.
        bad, ups, downs = [], 0, 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            c = A.deviation_counts(n, N)
            ups += c["U"]
            downs += c["W"]
            if c["U"] != A.skipped_credit_positions(n, N):
                bad.append((n, c["U"], A.skipped_credit_positions(n, N)))
            if c["W"] != sum(max(A.accel_code(n, N)[m - 1]
                                 - A.mechanical_valuation(m), 0)
                             for m in range(1, N + 1)):
                bad.append(("W", n))
        return (not bad and ups > 0 and downs > 0), {
            "violations": bad[:5], "upward_steps": ups, "downward_steps": downs,
            "_both_directions_seen": ups > 0 and downs > 0}

    check("SRC21_the_upward_variation_counts_exactly_the_skipped_credits",
          skipped_credit_identity,
          "§1: U_N = #{a_m = 2, q_m = 1}, and W_N = sum (q_m - a_m)_+")

    # ------------------- abstract: contamination and the mismatch barrier
    def contamination_bound():
        # A word of length N has at most N-r+1 factors of length r no matter what
        # it is, so the bound only says anything where cap < N-r+1. That column is
        # recorded per row, and the check below turns it into a statement.
        bad, rows = [], []
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            J = A.deviation_counts(n, N)["J"]
            for r in (1, 2, 3, 4, 5, 6):
                p = A.exponent_factor_complexity(n, N, r)
                cap = (r + 1) + r * J
                trivial_ceiling = N - r + 1
                rows.append({"n": n, "N": N, "J": J, "r": r, "p": p, "cap": cap,
                             "trivial_ceiling": trivial_ceiling,
                             "informative": cap < trivial_ceiling,
                             "slack": cap / p if p else None})
                if p > cap:
                    bad.append((n, r, p, cap))
        measured["contamination"] = rows
        return (not bad and len(rows) > 10), {"windows": len(rows),
                                              "violations": bad[:5]}

    check("SRC21_the_factor_complexity_obeys_the_contamination_bound",
          contamination_bound,
          "abstract: p_N(r) <= (r+1) + r J_N, because the mechanical word has "
          "complexity r+1 and each mismatch spoils at most r windows")

    def one_line_seen_from_two_sides():
        # The contamination bound is informative exactly when
        #   (r+1) + r J < N - r + 1   <=>   J < (N - 2r)/r,
        # and the right-hand side IS the packing theorem's floor. So the round's
        # two inequalities are one line: contamination constrains the word only
        # below the floor that return separation forbids. Checked row by row, and
        # required to be non-trivial — both outcomes must occur, or the
        # equivalence is being graded on rows that all fall the same way.
        rows = measured.get("contamination", [])
        dis = [(r["n"], r["r"]) for r in rows
               if r["informative"] != (r["J"] < (r["N"] - 2 * r["r"]) / r["r"])]
        yes = [r for r in rows if r["informative"]]
        no = [r for r in rows if not r["informative"]]
        measured["informative_window"] = {
            "rows": len(rows), "informative": len(yes), "vacuous": len(no),
            "informative_r": sorted({r["r"] for r in yes}),
            "vacuous_r": sorted({r["r"] for r in no})}
        return (not dis and yes and no), {
            "disagreements": dis[:5], "informative_rows": len(yes),
            "vacuous_rows": len(no),
            "_both_outcomes_seen": bool(yes) and bool(no)}

    check("SRC21_the_contamination_bound_and_the_packing_floor_are_one_line",
          one_line_seen_from_two_sides,
          "the two inequalities of this round are the same threshold from two "
          "sides: contamination says something only when J < (N-2r)/r, which is "
          "exactly what the packing theorem forbids")

    def mechanical_word_is_sturmian():
        # the bound's first term is the mechanical word's own complexity; if that
        # were not r+1 the whole estimate would be built on sand
        mech = A.mechanical_code(3000)
        bad = [r for r in range(1, 25) if A.factor_complexity(mech, r) != r + 1]
        return not bad, {"r_range": "1..24", "violations": bad}

    check("SRC21_the_mechanical_word_has_complexity_r_plus_one",
          mechanical_word_is_sturmian,
          "the (r+1) term: the mechanical word is Sturmian")

    def mismatch_packing():
        bad, rows = [], []
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            Y = A.orbit_endpoints(n, N)
            M_N = max(Y[:N + 1])
            J = A.deviation_counts(n, N)["J"]
            r_N = math.ceil(math.log2(M_N))
            # the theorem applies only where separation forces distinctness
            if not 2 ** (r_N + 1) > M_N:
                bad.append(("separation precondition fails", n))
                continue
            lo = max(0, (N - 2 * r_N) / r_N)
            rows.append({"n": n, "N": N, "r_N": r_N, "J": J, "lower_bound": lo,
                         "N_over_r": N / r_N,
                         # the smallest J that would still satisfy the bound; the
                         # ratio to the measured J says how much of the mismatch
                         # count this check is actually pinning down
                         "min_J_that_passes": math.ceil(lo),
                         "fraction_pinned": math.ceil(lo) / J if J else None,
                         "slack": J / lo if lo > 0 else None})
            if J < lo:
                bad.append((n, J, lo))
        measured["mismatch_packing"] = rows
        return (not bad and len(rows) == len(SPINES)), {"spines": len(rows),
                                                        "violations": bad[:5]}

    check("SRC21_the_mismatch_packing_bound_holds_on_real_spines",
          mismatch_packing,
          "abstract: J_N >= (N - 2 r_N)/r_N with r_N = ceil(log2 M_N). Passing "
          "this is WEAK evidence and the row's fraction_pinned says how weak: the "
          "floor is near 1 while J_N is in the tens. The falsifiable statement "
          "here is not the inequality but the quantity — see "
          "SRC21_the_rounds_three_inequalities_have_different_finite_quality.")

    def peak_exponent_bound():
        # r_N <= D_N + log2 N + O_n(1); checked with the constant made explicit
        bad, rows = [], []
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            Y = A.orbit_endpoints(n, N)
            M_N = max(Y[:N + 1])
            r_N = math.ceil(math.log2(M_N))
            D_N = A.record_deficit(n, N)
            # from M_N < 2^{D_N+1}(n + N/3)
            cap = D_N + 1 + math.log2(n + N / 3)
            rows.append({"n": n, "r_N": r_N, "D_N": D_N, "cap": cap})
            if not (r_N <= cap + 1):
                bad.append((n, r_N, cap))
        measured["peak_exponent"] = rows
        return (not bad and rows), {"spines": len(rows), "violations": bad}

    check("SRC21_the_peak_exponent_is_bounded_by_the_deficit_record_and_log_n",
          peak_exponent_bound,
          "r_N <= D_N + log2 N + O_n(1), from Round 03-A.4's excursion bound")

    # ------------------------------------- §2: the one-sided dichotomy
    def monotone_stretch_behaviour():
        # §2: where the deficit is nondecreasing, every mismatch is a skipped
        # credit and the mismatch count over that stretch equals the deficit gain
        bad, rows = [], []
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            q = A.accel_code(n, N)
            best = (0, 0, 0)
            i = 1
            while i <= N:
                j = i
                while (j < N and A.deficit(n, j + 1) >= A.deficit(n, j)):
                    j += 1
                if j - i > best[1] - best[0]:
                    best = (i, j, 0)
                i = j + 1
            a, b, _ = best
            if b > a:
                gain = A.deficit(n, b) - A.deficit(n, a)
                mism = sum(1 for m in range(a + 1, b + 1)
                           if q[m - 1] != A.mechanical_valuation(m))
                skipped = sum(1 for m in range(a + 1, b + 1)
                              if A.mechanical_valuation(m) == 2 and q[m - 1] == 1)
                rows.append({"n": n, "from": a, "to": b, "gain": gain,
                             "mismatches": mism, "skipped": skipped})
                if mism != skipped or gain != skipped:
                    bad.append((n, a, b, gain, mism, skipped))
        measured["monotone_stretches"] = rows
        return (not bad and len(rows) >= 5), {"stretches": len(rows),
                                              "violations": bad[:5]}

    check("SRC21_on_a_nondecreasing_stretch_every_mismatch_is_a_skipped_credit",
          monotone_stretch_behaviour,
          "§2: q_m <= a_m there, so mismatches are exactly a_m=2 q_m=1 and their "
          "count is the deficit gain")

    def nonincreasing_means_constant():
        # §2: a nonnegative integer sequence that is eventually nonincreasing is
        # eventually constant — so that branch collapses to bounded deficit,
        # which A-U.2b excluded. Checked as the arithmetic fact it is.
        bad = []
        for seq in ([5, 4, 4, 3, 3, 3], [2, 2, 1, 1, 1, 1], [0, 0, 0]):
            n = len(seq)
            if any(seq[i + 1] > seq[i] for i in range(n - 1)):
                continue
            if seq[-1] != min(seq) or seq[-1] < 0:
                bad.append(seq)
        # and the real content: no spine's deficit is nonincreasing throughout,
        # which is what makes the branch non-vacuous to talk about
        rising = 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            if any(A.deficit(n, m + 1) > A.deficit(n, m) for m in range(1, N)):
                rising += 1
        return (not bad and rising == len(SPINES)), {
            "spines_with_a_rising_step": rising, "of": len(SPINES)}

    check("SRC21_a_nonincreasing_nonnegative_integer_deficit_would_be_constant",
          nonincreasing_means_constant,
          "§2: which is why that branch reduces to bounded deficit and is already "
          "excluded; every real spine does have rising steps")

    # -------------------------------------- §3: the reset geometry
    def reset_affine_identity():
        bad, tested = [], 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            for a in range(0, min(N, 12)):
                for b in range(a + 1, min(N, 24) + 1):
                    tested += 1
                    if not A.reset_affine_holds(n, a, b):
                        bad.append((n, a, b))
        return (not bad and tested > 0), {"windows": tested, "violations": bad[:5]}

    check("SRC21_the_reset_affine_identity_holds_in_exact_integers",
          reset_affine_identity,
          "§3: cleared of 2^{-K_b} and 3^b, Y_b 2^{K_b} = Y_a 2^{K_a} 3^{b-a} + "
          "sum 3^{b-1-i} 2^{K_i} — no floating point anywhere")

    def slope_identity():
        # §3: 3^{b-a} / 2^{K_b-K_a} = 2^{delta_b - delta_a}. Both sides are
        # exactly 3^{b-a} 2^{-(K_b-K_a)} by substituting delta = beta m - K_m, so
        # what is checked is the CONSEQUENCE that matters: a deficit drop is
        # exactly a locally contracting block.
        bad, contracting, expanding = [], 0, 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            K = A.cumulative(A.accel_code(n, N))
            for a in range(0, N - 2):
                for b in range(a + 1, min(a + 6, N) + 1):
                    drop = A.deficit(n, b) < A.deficit(n, a) if a else None
                    if drop is None:
                        continue
                    contracts = 3 ** (b - a) < 2 ** (K[b] - K[a])
                    if drop and not contracts:
                        bad.append((n, a, b))
                    contracting += contracts
                    expanding += not contracts
        return (not bad and contracting > 0 and expanding > 0), {
            "violations": bad[:5], "contracting": contracting,
            "expanding": expanding,
            "_both_outcomes_seen": contracting > 0 and expanding > 0}

    check("SRC21_a_deficit_drop_is_exactly_a_locally_contracting_block",
          slope_identity,
          "§3: the slope identity's content — delta falling means 3^{b-a} < "
          "2^{K_b-K_a}; both outcomes required")

    def first_return_reset_bound():
        # §3: if b is the first return with delta_b <= h while delta_i > h for
        # a <= i < b, then Y_b < 2^{h-delta_a} Y_a + (b-a)/3. For integer h this
        # clears to 3^{a+1} Y_b < 3 * 2^{h+K_a} Y_a + 3^a (b-a) — exact integers.
        bad, rows, multi = [], [], 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            for h in (1, 2, 3):
                for a in range(1, min(N - 1, 20)):
                    if not A.slack_exceeds(n, a, h, 1):
                        continue            # the hypothesis delta_a > h fails
                    b = A.first_return_below(n, a, h, 1, limit=N)
                    if b is None or b > N:
                        continue
                    # the premise delta_i > h for a <= i < b is what
                    # first_return_below constructs; assert it rather than trust it
                    if any(not A.slack_exceeds(n, i, h, 1) for i in range(a, b)):
                        bad.append(("premise violated", n, h, a, b))
                        continue
                    Y = A.orbit_endpoints(n, b)
                    K = A.cumulative(A.accel_code(n, b))
                    lhs = 3 ** (a + 1) * Y[b]
                    contraction = 3 * 2 ** (h + K[a]) * Y[a]
                    rhs = contraction + 3 ** a * (b - a)
                    multi += (b - a > 1)
                    rows.append({"n": n, "h": h, "a": a, "b": b, "gap": b - a,
                                 "ratio": lhs / rhs,
                                 "ratio_contraction_only": lhs / contraction,
                                 "correction_needed": lhs >= contraction})
                    if lhs >= rhs:
                        bad.append((n, h, a, b, lhs, rhs))
        measured["first_return"] = {
            "windows": len(rows),
            "windows_longer_than_one_step": multi,
            "ratio_min": min(r["ratio"] for r in rows) if rows else None,
            "ratio_max": max(r["ratio"] for r in rows) if rows else None,
            "longest_gap": max((r["gap"] for r in rows), default=0),
            "windows_where_the_correction_is_needed":
                sum(r["correction_needed"] for r in rows)}
        # a bound checked only on one-step returns would be nearly content-free
        return (not bad and multi >= 5), {"windows": len(rows),
                                          "multi_step_windows": multi,
                                          "violations": bad[:5]}

    check("SRC21_the_first_return_reset_bound_holds_in_exact_integers",
          first_return_reset_bound,
          "§3: Y_b < 2^{h-delta_a} Y_a + (b-a)/3, cleared to integers for integer "
          "h; requires genuine multi-step returns, not just b = a+1")

    def correction_never_carries_the_bound():
        # §3 reads the first-return bound as contraction PLUS an affine
        # correction that accumulates linearly over the reset interval. On these
        # spines the correction never does any work: the contraction term alone
        # already dominates Y_b at every window, and adding (b-a)/3 moves the
        # ratio in the fourth decimal. So the reset is pure contraction here, and
        # the paper's second term is an asymptotic provision, not a live one.
        rows = measured.get("first_return", {})
        # recomputed independently rather than read off the rows above
        bad, worst, worst_full, n_needed, tested = [], 0.0, 0.0, 0, 0
        for n in SPINES:
            N = A.subcritical_lifetime(n)
            for h in (1, 2, 3):
                for a in range(1, min(N - 1, 20)):
                    if not A.slack_exceeds(n, a, h, 1):
                        continue
                    b = A.first_return_below(n, a, h, 1, limit=N)
                    if b is None or b > N:
                        continue
                    Y = A.orbit_endpoints(n, b)
                    K = A.cumulative(A.accel_code(n, b))
                    lhs = 3 ** (a + 1) * Y[b]
                    contraction = 3 * 2 ** (h + K[a]) * Y[a]
                    tested += 1
                    worst = max(worst, lhs / contraction)
                    worst_full = max(worst_full, lhs / (contraction + 3 ** a * (b - a)))
                    if lhs >= contraction:
                        n_needed += 1
                        bad.append((n, h, a, b))
        measured["correction_weight"] = {
            "windows": tested,
            "worst_ratio_contraction_only": worst,
            "worst_ratio_with_correction": worst_full,
            "windows_where_the_correction_is_needed": n_needed,
            "reading": ("the affine correction moves the worst case by "
                        f"{worst - worst_full:.2e}; it is never what makes the "
                        "bound true at these sizes")}
        return (not bad and tested == rows.get("windows")), {
            "windows": tested, "windows_needing_the_correction": n_needed,
            "worst_ratio_contraction_only": worst}

    check("SRC21_the_affine_correction_never_carries_the_first_return_bound",
          correction_never_carries_the_bound,
          "§3: the contraction term alone bounds Y_b at every window here, so "
          "the +(b-a)/3 provision is asymptotic rather than live. This is also "
          "why removing that term from the bound is a no-op in the drill.")

    # --------------------------------------------- ledger and provenance
    def unproved_list():
        tail = au2e[au2e.find("### 未證"):] if "### 未證" in au2e else ""
        want = ["CASP", "Terras", "Collatz"]
        missing = [w for w in want if w not in tail]
        return (bool(tail) and not missing), {"missing": missing}

    check("SRC21_the_paper_lists_casp_terras_and_collatz_as_unproved",
          unproved_list, "§6")

    def regimes_named():
        return (("Regime M" in au2e and "Regime R" in au2e
                 and "One-Sided Deficit Dichotomy" in au2e), {})

    check("SRC21_the_paper_states_its_dichotomy_as_two_named_regimes",
          regimes_named,
          "§4: a candidate must pay either monotone buildup or reset domination")

    def routemap_agrees():
        want = ["A-U.2e.1", "A-L", "A-U.2d"]
        missing = [w for w in want if w not in routemap]
        return (not missing and len(routemap) > 500), {"missing": missing,
                                                       "routemap_len": len(routemap)}

    check("SRC21_the_route_map_carries_the_same_three_successors",
          routemap_agrees,
          "v1.5: Reset-Block Arithmetic, the giant-valuation tail, and transducer "
          "rationality")

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
        prev = members(SOURCE / PREV_BUNDLE)
        same = [n for n, h in big.items() if prev.get(n) == h]
        edited = [n for n, h in big.items() if n in prev and prev[n] != h]
        fresh = [n for n in big if n not in prev]
        measured["bundle"] = {"reshipped_identical": sorted(same),
                              "reshipped_edited": edited,
                              "new_in_this_bundle": sorted(fresh),
                              "note": ("this bundle is TRIMMED: it drops AU1, "
                                       "AU2a and AU2b, which earlier bundles "
                                       "carried. Dropping is not editing, so the "
                                       "check requires only that what IS "
                                       "re-shipped is byte-identical.")}
        return (not edited and len(same) == 3 and len(fresh) == 2), {
            "reshipped_identical": len(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh)}

    check("SRC21_whatever_the_trimmed_bundle_reships_is_unedited", bundle_faithful,
          "three predecessors byte-identical, two files new; the bundle drops "
          "three earlier papers, which is a trim rather than an edit")

    # ------------------------------------------------------ own measurement
    def which_half_binds():
        # This round asserts three inequalities. Measure how close each comes to
        # binding, so the report can say which ones a bounded computation can see
        # and which are asymptotic statements that no finite spine will test.
        cont = measured.get("contamination", [])
        pack = measured.get("mismatch_packing", [])
        fr = measured.get("first_return", {})
        cont_slack = [r["slack"] for r in cont if r["slack"]]
        pack_slack = [r["slack"] for r in pack if r["slack"]]
        pinned = [r["fraction_pinned"] for r in pack if r["fraction_pinned"]]
        nor = [r["N_over_r"] for r in pack]

        def rng(v, p=2):
            return f"{min(v):.{p}f} to {max(v):.{p}f}"

        # every number in the reading is computed from the rows above; none is
        # typed, so the sentence cannot drift away from the measurement
        measured["which_half_binds"] = {
            "reset_geometry_saturation": [fr.get("ratio_min"), fr.get("ratio_max")],
            "contamination_slack": [min(cont_slack), max(cont_slack)],
            "packing_slack": [min(pack_slack), max(pack_slack)],
            "packing_fraction_pinned": [min(pinned), max(pinned)],
            "N_over_r_N": [min(nor), max(nor)],
            "reading": (
                f"This round asserts three inequalities whose finite qualities "
                f"differ by a factor of "
                f"{max(fr.get('ratio_max', 0), 1e-9) / min(pinned):.0f}.\n"
                f"(1) The reset geometry of §3 nearly saturates: across "
                f"{fr.get('windows')} first-return windows the true Y_b reaches "
                f"{fr.get('ratio_min'):.2f} to {fr.get('ratio_max'):.2f} of its "
                f"cap, so that bound is doing real work at this scale.\n"
                f"(2) The contamination bound is informative at r = "
                f"{measured['informative_window']['informative_r']} and vacuous "
                f"at r = {measured['informative_window']['vacuous_r']}: for the "
                f"larger windows its cap exceeds N-r+1, which every word of "
                f"length N satisfies for free. Where it does bite it exceeds the "
                f"true complexity by {rng(cont_slack)}.\n"
                f"(3) The mismatch barrier is not visible at all. Its floor is "
                f"N/r_N - 2, and on real spines N/r_N runs {rng(nor)}, so the "
                f"floor lands at {min(r['lower_bound'] for r in pack):.2f} to "
                f"{max(r['lower_bound'] for r in pack):.2f} against a measured "
                f"J_N of {min(r['J'] for r in pack)} to "
                f"{max(r['J'] for r in pack)}. It pins only "
                f"{min(pinned):.1%} to {max(pinned):.1%} of the mismatches that "
                f"are actually there, so it would still be satisfied if all but "
                f"one or two of them vanished. Passing it is not evidence.\n"
                f"(2) and (3) are the same threshold from two sides — "
                f"contamination constrains the word only below J = (N-2r)/r, "
                f"which is exactly the floor return separation forbids — and at "
                f"these sizes real spines sit far on the vacuous side of that "
                f"line, with J_N/N running "
                f"{rng([r['J'] / r['N'] for r in pack])}. The round's exact "
                f"identities are "
                f"checkable and check out; its asymptotic content is what this "
                f"computation cannot see.")}
        return (max(cont_slack) < 15 and min(pack_slack) > 5
                and max(pinned) < 0.25 and fr.get("ratio_max", 0) > 0.5), {
            "reset_geometry_saturation": [fr.get("ratio_min"), fr.get("ratio_max")],
            "contamination_slack": [min(cont_slack), max(cont_slack)],
            "packing_slack": [min(pack_slack), max(pack_slack)],
            "packing_fraction_pinned": [min(pinned), max(pinned)]}

    check("SRC21_the_rounds_three_inequalities_have_different_finite_quality",
          which_half_binds,
          "measurement: which of this round's inequalities a bounded computation "
          "can actually see, and which is asymptotic only")

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
