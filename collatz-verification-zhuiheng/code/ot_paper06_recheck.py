"""Independent recheck of Operation Translation Series — Paper 06.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *Valuation Language 與 Accelerated Collatz*, Paper 06 v0.1.

Independence
------------
The referee is direct iteration of the accelerated odd map
S(n) = (3n+1)/2^{v_2(3n+1)} on genuine odd integers. It assumes no theorem of
the paper. Every claimed formula is compared against it.

This matters more here than in Paper 02. The subject's own suite
(`test_p06`) checks only that the closed affine form agrees with iterated
Fraction arithmetic, for formal valuation tuples, with m <= 5, kappa in 1..4,
and **only at n = 1**. It never checks admissibility — that a valuation word is
actually realised by some odd n — and it never touches Theorems D through H,
the section 19 descent threshold, or the section 14 bridge back to Paper 02.

Scope: exact finite arithmetic and exact residue counting. Nothing here bears
on the Collatz conjecture, and the paper does not claim otherwise.

Usage:  python code/ot_paper06_recheck.py [odd_limit]
"""

from __future__ import annotations

import itertools
import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ot_paper02_recheck import compose_affine  # the Paper 02 referee route

ODD_LIMIT_DEFAULT = 20001


def v2(x: int) -> int:
    k = 0
    while x % 2 == 0:
        x //= 2
        k += 1
    return k


# --- referee: no theorem assumed ------------------------------------------
def S(n: int) -> tuple[int, int]:
    """One accelerated odd step. Returns (S(n), kappa)."""
    k = v2(3 * n + 1)
    return (3 * n + 1) // 2 ** k, k


def orbit(n0: int, m: int) -> tuple[list[int], list[int]]:
    """m accelerated steps from odd n0. Returns (states, valuation word)."""
    states, kappas = [n0], []
    x = n0
    for _ in range(m):
        x, k = S(x)
        states.append(x)
        kappas.append(k)
    return states, kappas


# --- claimed formulas ------------------------------------------------------
def B_closed(kappas: list[int]) -> int:
    """Theorem C: B = sum_i 3^{m-i} 2^{K_{i-1}}."""
    m = len(kappas)
    total = 0
    Kprev = 0
    for i in range(1, m + 1):
        total += 3 ** (m - i) * 2 ** Kprev
        Kprev += kappas[i - 1]
    return total


def B_recurrence(kappas: list[int]) -> int:
    """Section 11: B_j = 3 B_{j-1} + 2^{K_{j-1}}."""
    B, K = 0, 0
    for k in kappas:
        B = 3 * B + 2 ** K
        K += k
    return B


def expand(kappas: list[int]) -> str:
    """Theorem A: E(kappa) = U D^{kappa-1} concatenated."""
    return "".join("U" + "D" * (k - 1) for k in kappas)


def R(kappa: int, t: int) -> Fraction:
    """Section 34: the exact reverse step."""
    return Fraction(2 ** kappa * t - 1, 3)


def check(rep: dict, name: str, ok: bool, detail: str = "") -> None:
    rep["checks"][name] = {"pass": bool(ok), **({"detail": detail} if detail else {})}
    if not ok:
        rep["failures"].append(name + (f": {detail}" if detail else ""))


def main() -> int:
    odd_limit = int(sys.argv[1]) if len(sys.argv) > 1 else ODD_LIMIT_DEFAULT
    rep = {
        "tool": "ot_paper06_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 06 v0.1 (Neo.K)",
        "scope": "exact finite arithmetic and exact residue counting; not a Collatz proof",
        "odd_starts_upper_limit": odd_limit,
        "checks": {},
        "counts": {},
        "failures": [],
    }

    MAX_M = 12
    thmA = thmBC = thmC_rec = bridge = thmD = thm19 = thm20 = True
    orbits = 0
    contracting = expanding = 0

    for n0 in range(1, odd_limit, 2):
        states, kappas = orbit(n0, MAX_M)
        for m in range(1, MAX_M + 1):
            ks = kappas[:m]
            K = sum(ks)
            B = B_closed(ks)

            # Theorem A: the run-length expansion is the genuine parity word,
            # with |E| = K and u(E) = m.
            E = expand(ks)
            if len(E) != K or E.count("U") != m:
                thmA = False
            x, ok_word = n0, True
            for c in E:
                if (c == "U") != (x % 2 == 1):
                    ok_word = False
                    break
                x = (3 * x + 1) // 2 if x % 2 else x // 2
            if not ok_word or x != states[m]:
                thmA = False

            # Theorems B and C, on a genuine admissible orbit rather than a
            # formal tuple: iteration must equal the closed affine form.
            if Fraction(3 ** m * n0 + B, 2 ** K) != states[m]:
                thmBC = False
            if B_recurrence(ks) != B:
                thmC_rec = False

            # Section 14: the accelerated correction is exactly the Paper 02
            # correction of the expanded parity word. Cross-paper consistency.
            _, b_w, _ = compose_affine(E)
            if b_w != B:
                bridge = False

            # Theorem D, checked as the equivalent exact rational identity so
            # that no floating logarithm is involved.
            if Fraction(states[m], n0) != Fraction(3 ** m, 2 ** K) * (
                1 + Fraction(B, 3 ** m * n0)
            ):
                thmD = False

            # Sections 19 and 20: exact two-sided finite classification.
            if 2 ** K > 3 ** m:
                contracting += 1
                theta = B // (2 ** K - 3 ** m) + 1
                descends = states[m] < n0
                if descends != (n0 >= theta):
                    thm19 = False
            elif 2 ** K < 3 ** m:
                expanding += 1
                if not states[m] > n0:
                    thm20 = False
            orbits += 1

    check(rep, "P06_ThmA_run_length_expansion_is_the_parity_word", thmA)
    check(rep, "P06_ThmBC_accelerated_affine_closure_on_real_orbits", thmBC)
    check(rep, "P06_ThmC_recurrence_matches_closed_form", thmC_rec)
    check(rep, "P06_S14_bridge_B_kappa_equals_b_of_expanded_word", bridge)
    check(rep, "P06_ThmD_exact_log_drift_as_rational_identity", thmD)
    check(rep, "P06_S19_descent_threshold_theta_is_exact_iff", thm19)
    check(rep, "P06_S20_uniform_expansion_when_2K_lt_3m", thm20)
    rep["counts"]["orbit_prefixes_checked"] = orbits
    rep["counts"]["contracting_skeleton_cases"] = contracting
    rep["counts"]["expanding_skeleton_cases"] = expanding

    # --- Theorem F: exact one-step valuation density -----------------------
    thmF = thmF_repr = True
    for j in range(1, 21):
        mod = 2 ** (j + 1)
        hits = [r for r in range(1, mod, 2) if v2(3 * r + 1) == j]
        if len(hits) != 1:
            thmF = False
        if hits and hits[0] != pow(3, -1, mod) * (2 ** j - 1) % mod:
            thmF_repr = False
    check(rep, "P06_ThmF_exactly_one_odd_residue_class_per_valuation", thmF)
    check(rep, "P06_ThmF_stated_representative_is_correct", thmF_repr)

    # The two series, as exact rationals with their closed partial sums, so
    # "= 1" and "= 2" are verified rather than eyeballed from a decimal.
    J = 64
    s1 = sum(Fraction(1, 2 ** j) for j in range(1, J + 1))
    s2 = sum(Fraction(j, 2 ** j) for j in range(1, J + 1))
    check(rep, "P06_ThmF_density_partial_sum_closed_form",
          s1 == 1 - Fraction(1, 2 ** J))
    check(rep, "P06_ThmF_mean_valuation_partial_sum_closed_form",
          s2 == 2 - Fraction(J + 2, 2 ** J))
    rep["counts"]["series_terms"] = J

    # --- Theorem G and section 31: valuation order --------------------------
    thmG = order_min = order_max = True
    swaps = perms = 0
    for m in range(2, 7):
        for ks in itertools.product(range(1, 5), repeat=m):
            ks = list(ks)
            for i in range(m - 1):
                a, b = ks[i], ks[i + 1]
                swapped = ks[:i] + [b, a] + ks[i + 2:]
                P = sum(ks[:i])
                lhs = B_closed(ks) - B_closed(swapped)
                if lhs != 3 ** (m - i - 2) * 2 ** P * (2 ** a - 2 ** b):
                    thmG = False
                swaps += 1
    for m in range(2, 7):
        for ks in itertools.combinations_with_replacement(range(1, 6), m):
            vals = [B_closed(list(p)) for p in set(itertools.permutations(ks))]
            if B_closed(sorted(ks)) != min(vals):
                order_min = False
            if B_closed(sorted(ks, reverse=True)) != max(vals):
                order_max = False
            perms += 1
    check(rep, "P06_ThmG_adjacent_valuation_swap_formula", thmG)
    check(rep, "P06_S31_ascending_order_minimises_correction", order_min)
    check(rep, "P06_S31_descending_order_maximises_correction", order_max)
    rep["counts"]["adjacent_swaps"] = swaps
    rep["counts"]["valuation_multisets"] = perms

    # --- Theorems H, sections 35, 38, 39: reverse recovery ------------------
    thmH = legality = terminal = True
    recoveries = 0
    for n0 in range(1, min(odd_limit, 4001), 2):
        for m in range(1, 9):
            states, kappas = orbit(n0, m)
            K = sum(kappas)
            B = B_closed(kappas)
            # closed reverse formula
            if Fraction(2 ** K * states[m] - B, 3 ** m) != n0:
                thmH = False
            # section 38: stepwise legality, not just the closed fraction
            t = states[m]
            for kappa in reversed(kappas):
                if (2 ** kappa * t) % 3 != 1:
                    legality = False
                    break
                prev = R(kappa, t)
                if prev.denominator != 1 or prev.numerator % 2 == 0:
                    legality = False
                    break
                t = prev.numerator
            if t != n0:
                legality = False
            recoveries += 1
    for j in range(1, 25):
        # section 39: R_{2j}(1) = (4^j - 1)/3, and it is an odd integer
        r = R(2 * j, 1)
        if r != Fraction(4 ** j - 1, 3) or r.denominator != 1 or r.numerator % 2 == 0:
            terminal = False
    check(rep, "P06_ThmH_closed_reverse_recovery", thmH)
    check(rep, "P06_S35_S38_stepwise_reverse_legality", legality)
    check(rep, "P06_S39_terminal_fiber_of_1", terminal)
    rep["counts"]["reverse_recoveries"] = recoveries

    # --- Theorem E, and where a floating comparison would betray it --------
    # 2^K > 3^m iff K/m > log2 3 is exact. Deciding it with a float log2(3)
    # is not, because K/m runs through the convergents of log2 3. The exact
    # integer test is the reference; the float test is recorded as a hazard.
    import math
    from decimal import Decimal, getcontext

    getcontext().prec = 80
    # log2(3) to 80 significant digits, computed here rather than taken from a
    # float, so this route does not inherit double-precision error.
    log2_3_hp = Decimal(3).ln() / Decimal(2).ln()
    log2_3_float = math.log2(3)

    thmE = True
    float_disagreements = []
    hp_disagreements = []
    closest = None
    pairs = 0
    for m in range(1, 401):
        for K in range(max(1, int(m * log2_3_float) - 1), int(m * log2_3_float) + 3):
            exact = 2 ** K > 3 ** m          # the integer statement
            hp = Decimal(K) / Decimal(m) > log2_3_hp   # the real-number statement
            approx = (K / m) > log2_3_float            # what a naive float test says
            if exact != hp:
                hp_disagreements.append({"m": m, "K": K})
                thmE = False
            if exact != approx:
                float_disagreements.append({"m": m, "K": K})
            gap = abs(Fraction(K, m) - Fraction(log2_3_hp))
            if closest is None or gap < closest[0]:
                closest = (gap, m, K)
            pairs += 1

    # A high-precision route is only a witness if it is actually precise enough
    # for the closest ratio in range. Recorded, not assumed.
    margin = abs(Fraction(closest[2], closest[1]) - Fraction(log2_3_hp))
    check(rep, "P06_ThmE_integer_form_matches_the_real_inequality", thmE,
          f"high-precision disagreements at {hp_disagreements[:5]}" if hp_disagreements else "")
    check(rep, "P06_ThmE_float_log2_3_test_agrees_on_tested_range",
          not float_disagreements,
          f"naive float verdict differs at {float_disagreements[:5]}"
          if float_disagreements else "")
    rep["counts"]["thmE_pairs_tested"] = pairs
    rep["counts"]["closest_ratio_to_log2_3"] = f"K/m = {closest[2]}/{closest[1]}"
    rep["counts"]["closest_ratio_margin_exceeds_float_epsilon"] = bool(
        margin > Fraction(1, 2 ** 52)
    )

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
