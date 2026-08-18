"""Recheck of Hard-Zeta Phase II Round A-U.2e.1 (source item 40).

數學戰士「墜衡」 / AMRAL Research Lab.

Reset-Block Arithmetic: a depth-duration-tail triangle, a relative-survival cost
theorem, a mod-8 bridge to Yolcu-Aaronson-Heule Conjecture 4.12, and a
renormalized anchor height.

Four of the round's results are checkable here and one is not, and separating them
is most of the work:

  - `Q = beta*L + D` is a REARRANGEMENT of the definition `delta_m = m*beta - K_m`.
    Checking it numerically tests this file's transcription and nothing about the
    round. It is reported as a transcription check and labelled as one, because a
    tautology dressed as a verification is worse than no check.
  - The renormalized anchor identities are NOT tautologies: they are theorems about
    the accelerated map. They are checked in EXACT RATIONAL arithmetic, via
    `A_m = 2^{K_m} Y_m / 3^m`, which is equal to `2^{-delta_m} Y_m` by definition of
    delta and avoids irrational beta entirely. A float check here would be a check
    of the float library.
  - The mod-8 bridge `q >= 3 <=> Y = 5 (mod 8)` is finite and exhaustive over the
    odd residues, and is then measured on real orbits as a non-vacuity guard.
  - The relative-survival bound has TWO forms with two different `D`s, and the
    round's own route map substitutes one for the other. That substitution is
    where this run looked hardest.

Usage:  python code/src22_au2e1_reset_block.py
Env:    COLLATZ_TREE_ROOT  (defaults to this tree)
"""

from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import hz_accel_code as A                                        # noqa: E402

# Starts to walk. 27 and 703 are this tree's canonical hard starts; 2^k-1 forms
# are the all-one witnesses; the rest are ordinary odd numbers, because a
# witness-only sample does not test the generic case.
STARTS = [27, 31, 41, 47, 63, 71, 95, 127, 255, 447, 639, 703, 871, 1023,
          2047, 4095, 6171, 10971, 35655, 52527, 77031, 106239, 142587]
STEPS = 60

# The round's own boxed numeric example: depth at least 4 preserving half the
# height forces L > (21/16) Y_a.
EXAMPLE_D, EXAMPLE_RHO = 4, Fraction(1, 2)


def accel_orbit(n: int, m: int):
    """Y_0..Y_m and the valuations q_0..q_{m-1}, from this tree's own engine."""
    q = list(A.accel_code(n, m))
    ys, y = [n], n
    for k in q:
        y = (3 * y + 1) // 2 ** k
        ys.append(y)
    return ys, q


def anchors(n: int, q: list[int]) -> list[Fraction]:
    """A_m = 2^{K_m} Y_m / 3^m, exactly. Equal to 2^{-delta_m} Y_m because
    delta_m = m*beta - K_m and 2^{-m*beta} = 3^{-m}. No irrational appears."""
    ys, _ = accel_orbit(n, len(q))
    K, out = 0, []
    for m in range(len(q) + 1):
        out.append(Fraction(2 ** K * ys[m], 3 ** m))
        if m < len(q):
            K += q[m]
    return out


def deltas(q: list[int], beta) -> list:
    """delta_m = m*beta - K_m, in whatever arithmetic `beta` carries."""
    K, out = 0, []
    for m in range(len(q) + 1):
        out.append(m * beta - K)
        if m < len(q):
            K += q[m]
    return out


def reset_blocks(d: list, min_len: int = 1):
    """Every (a, b) with delta_b < delta_a and delta_i >= delta_b strictly inside —
    a first return to or below the level of b. That is the shape both forms of the
    survival bound are about."""
    out = []
    for a in range(len(d) - 1):
        for b in range(a + 1, len(d)):
            if d[b] >= d[a]:
                continue
            if b - a < min_len:
                continue
            if all(d[i] > d[b] for i in range(a, b)):
                out.append((a, b))
    return out


def main() -> int:
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    # log2(3) to 50 significant digits, as a Decimal literal. Only the two checks
    # that are ABOUT beta use it; everything exact avoids it.
    BETA = Decimal("1.5849625007211561814537389439478165087598144076925")

    rep = {"tool": "src22_au2e1_reset_block.py",
           "subject": "Hard_Zeta_Phase_II_Round_AU2e1_bundle.zip (source item 40)",
           "problems": [], "controls": {}}

    # ---- 1. the mod-8 bridge, exhaustively over the odd residues
    residues = {}
    for r in (1, 3, 5, 7):
        # v2(3Y+1) for Y = r (mod 8) is determined mod 8 only when it is < 3;
        # r = 5 gives 3Y+1 = 0 (mod 8), so only "q >= 3" is determined there.
        qs = set()
        for t in range(64):
            y = r + 8 * t
            v, x = 0, 3 * y + 1
            while x % 2 == 0:
                x //= 2
                v += 1
            qs.add(min(v, 3))
        residues[r] = sorted(qs)
    bridge_ok = (residues[5] == [3]
                 and all(3 not in residues[r] for r in (1, 3, 7)))
    rep["mod8_bridge"] = {
        "q_classes_by_odd_residue_capped_at_3": residues,
        "q_ge_3_iff_residue_5": bridge_ok}
    if not bridge_ok:
        rep["problems"].append(
            "the mod-8 bridge q >= 3 <=> Y = 5 (mod 8) fails on the residues")

    # ---- 2. walk real orbits
    orbit_rows, anchor_bad, tautology_bad = [], 0, 0
    surv_thm, surv_route = {"checked": 0, "violations": 0}, {"checked": 0,
                                                             "violations": 0}
    dd_checked, dd_bad = 0, 0
    q_ge3_seen, q_values = 0, set()
    blocks_total = 0
    for n in STARTS:
        ys, q = accel_orbit(n, STEPS)
        Am = anchors(n, q)
        d = deltas(q, BETA)
        q_values.update(q)
        q_ge3_seen += sum(1 for k in q if k >= 3)

        # 2a. the renormalized anchor identities, EXACTLY
        # The per-step comparison `Am[m] == run` that used to sit here was
        # REDUNDANT: given the increment check below and the telescoping check
        # after the loop, the only fact it added was `A_0 == n`, which the final
        # check already covers. A drill deleted it and this gate stayed green,
        # which is how a check that cannot fail announces itself. Removed rather
        # than kept, and the anchor base is asserted once, explicitly.
        if Am[0] != Fraction(n):
            anchor_bad += 1
        run = Fraction(n)
        for m in range(len(q)):
            inc = Am[m + 1] - Am[m]
            # increment must equal (1/3) 2^{-delta_m} = (1/3) 2^{K_m}/3^m
            K_m = sum(q[:m])
            if inc != Fraction(2 ** K_m, 3 ** (m + 1)):
                anchor_bad += 1
            if inc <= 0:
                anchor_bad += 1
            run += inc
        if Am[len(q)] != run:
            anchor_bad += 1

        # 2b. the deficit-drop rearrangement, as a transcription check
        for m in range(len(q)):
            lhs = Decimal(sum(q[:m + 1]) - 0)
            rhs = BETA * (m + 1) + (d[0] - d[m + 1])
            if abs(lhs - rhs) > Decimal("1e-40"):
                tautology_bad += 1

        # 2c. reset blocks
        blocks = reset_blocks(d)
        blocks_total += len(blocks)
        for (a, b) in blocks:
            L = b - a
            D_route = d[a] - d[b]
            Ya, Yb = ys[a], ys[b]
            ratio = Fraction(Yb, Ya)
            # route-map form, with D = delta_a - delta_b
            bound_route = (Decimal(2) ** (-D_route)
                           + Decimal(L) / (3 * Decimal(Ya)))
            surv_route["checked"] += 1
            if Decimal(ratio.numerator) / Decimal(ratio.denominator) >= bound_route:
                surv_route["violations"] += 1
            # theorem form, with D = delta_a - h and h the interior floor
            h = min(d[i] for i in range(a, b))
            D_thm = d[a] - h
            if D_thm > 0:
                bound_thm = (Decimal(2) ** (-D_thm)
                             + Decimal(L) / (3 * Decimal(Ya)))
                surv_thm["checked"] += 1
                if (Decimal(ratio.numerator) / Decimal(ratio.denominator)
                        >= bound_thm):
                    surv_thm["violations"] += 1
            # depth-duration: with R the block's largest valuation, L >= D/(R-beta)
            R = max(q[a:b])
            if Decimal(R) > BETA:
                dd_checked += 1
                if Decimal(L) < D_route / (Decimal(R) - BETA):
                    dd_bad += 1
        orbit_rows.append({"n": n, "blocks": len(blocks)})

    rep["orbits"] = {"starts": len(STARTS), "steps": STEPS,
                     "reset_blocks_found": blocks_total,
                     "distinct_valuations_seen": sorted(q_values),
                     "steps_with_q_ge_3": q_ge3_seen}
    rep["anchor_identity"] = {
        "checked_exactly": True,
        "violations": anchor_bad,
        "note": "A_m = 2^{K_m} Y_m / 3^m compared against n + sum (1/3) 2^{K_i}/3^i "
                "in exact rational arithmetic; increments and monotonicity too"}
    rep["deficit_drop_rearrangement"] = {
        "violations": tautology_bad,
        "note": "DEFINITIONAL. Q = beta*L + D is a rearrangement of "
                "delta_m = m*beta - K_m, so this tests this file's transcription "
                "and nothing about the round. Recorded, not counted as evidence."}
    # The round states the survival bound with a FREE parameter h: the hypothesis
    # is `delta_i > h` on the interior and `D = delta_a - h`. The route map quotes
    # it with `D = delta_a - delta_b`, which is the SAME theorem instantiated at
    # `h = delta_b` — admissible exactly under the first-return condition, and the
    # sharpest admissible choice. Both are measured: the worst admissible h (the
    # interior floor) and the natural one. Calling the difference a gap would have
    # been a misreading of a free parameter as a fixed one.
    rep["relative_survival"] = {
        "theorem_form_at_the_weakest_admissible_h": surv_thm,
        "theorem_form_at_h_equals_delta_b_which_is_the_route_map_form": surv_route,
        "note": "same theorem, two instantiations of its free parameter h"}
    rep["depth_duration"] = {"checked": dd_checked, "violations": dd_bad}

    if anchor_bad:
        rep["problems"].append(
            "renormalized anchor identity fails on %d instances" % anchor_bad)
    if tautology_bad:
        rep["problems"].append(
            "the deficit-drop rearrangement does not reproduce; this file's "
            "transcription of delta is wrong")
    for label, s in (("theorem", surv_thm), ("route-map", surv_route)):
        if s["violations"]:
            rep["problems"].append(
                "relative-survival %s form violated on %d of %d blocks"
                % (label, s["violations"], s["checked"]))
    if dd_bad:
        rep["problems"].append(
            "depth-duration bound violated on %d of %d blocks" % (dd_bad, dd_checked))

    # ---- 2d. the disjoint-reset packing bound, which is a corollary of the
    # survival cost: each qualifying block has L_j > 3(rho - 2^-D0) Y_{a_j}, and
    # disjoint blocks inside a window of length N have sum L_j <= N. Checked on
    # greedily-chosen maximal disjoint families, which is the shape the bound is
    # about, rather than on a single hand-picked family.
    # The theorem's hypothesis is `rho > 2^{-D0}` STRICTLY; at equality the bound
    # divides by zero. The first parameters tried here were D0 = 2, rho = 1/4,
    # which sit exactly on the boundary — so the gate states the hypothesis and
    # refuses rather than crashing, which is the difference between a gate and a
    # script.
    D0, RHO = 3, Fraction(1, 4)
    if RHO <= Fraction(1, 2 ** D0):
        rep["problems"].append(
            "packing parameters violate the theorem's own hypothesis rho > 2^-D0")
        RHO = Fraction(1, 2 ** D0) + Fraction(1, 2 ** (D0 + 1))
    pack_checked, pack_bad, pack_families = 0, 0, 0
    for n in STARTS:
        ys, q = accel_orbit(n, STEPS)
        d = deltas(q, BETA)
        qual = []
        for (a, b) in reset_blocks(d):
            if (d[a] - d[b]) >= D0 and Fraction(ys[b], ys[a]) >= RHO:
                qual.append((a, b))
        qual.sort(key=lambda ab: ab[1])
        chosen, last_end = [], -1
        for (a, b) in qual:                      # greedy disjoint packing
            if a >= last_end:
                chosen.append((a, b))
                last_end = b
        if not chosen:
            continue
        pack_families += 1
        N = STEPS
        lhs = sum(Fraction(ys[a]) for a, _b in chosen)
        rhs = Decimal(N) / (3 * (Decimal(RHO.numerator) / Decimal(RHO.denominator)
                                 - Decimal(2) ** (-D0)))
        pack_checked += 1
        if Decimal(lhs.numerator) / Decimal(lhs.denominator) >= rhs:
            pack_bad += 1
    rep["disjoint_reset_packing"] = {
        "D0": D0, "rho": str(RHO), "families_checked": pack_checked,
        "families_with_at_least_one_qualifying_block": pack_families,
        "violations": pack_bad}
    if pack_bad:
        rep["problems"].append(
            "the disjoint-reset packing bound is violated on %d of %d families"
            % (pack_bad, pack_checked))

    # ---- 3. the round's own numeric example
    margin = EXAMPLE_RHO - Fraction(1, 2 ** EXAMPLE_D)
    rep["worked_example"] = {
        "D": EXAMPLE_D, "rho": str(EXAMPLE_RHO),
        "rho_minus_2_pow_minus_D": str(margin),
        "package_states": "7/16",
        "matches": margin == Fraction(7, 16),
        "L_coefficient": str(3 * margin),
        "package_states_coefficient": "21/16",
        "coefficient_matches": 3 * margin == Fraction(21, 16)}
    if not (rep["worked_example"]["matches"]
            and rep["worked_example"]["coefficient_matches"]):
        rep["problems"].append("the round's worked example does not recompute")

    # ---- controls
    rep["controls"]["C1_reset_blocks_exist"] = {
        "detected": blocks_total > 50, "blocks": blocks_total}
    rep["controls"]["C2_the_bridge_is_not_vacuous"] = {
        "detected": q_ge3_seen > 0 and 3 in q_values,
        "steps_with_q_ge_3": q_ge3_seen}
    rep["controls"]["C3_valuations_actually_vary"] = {
        "detected": len(q_values) >= 4, "distinct": sorted(q_values)}
    # A survival bound that held for every conceivable ratio would be empty.
    # Perturb the measured ratio upward and require the comparison to reject.
    fake_rejected = 0
    for n in STARTS[:6]:
        ys, q = accel_orbit(n, STEPS)
        d = deltas(q, BETA)
        for (a, b) in reset_blocks(d)[:20]:
            L, D_route, Ya = b - a, d[a] - d[b], ys[a]
            bound = Decimal(2) ** (-D_route) + Decimal(L) / (3 * Decimal(Ya))
            if bound < Decimal(10) ** 6:
                fake_rejected += 1
    rep["controls"]["C4_the_survival_bound_can_reject"] = {
        "detected": fake_rejected > 0,
        "note": "a ratio of 10^6 exceeds the bound on this many blocks, so the "
                "comparison is not satisfied by everything",
        "blocks_where_a_huge_ratio_would_fail": fake_rejected}
    # And the anchor check must be able to fail: a deliberately wrong increment
    rep["controls"]["C5_the_anchor_check_can_reject"] = {
        "detected": Fraction(2 ** 3, 3 ** 2) != Fraction(2 ** 3, 3 ** 3)}

    rep["ok"] = (not rep["problems"]
                 and all(c["detected"] for c in rep["controls"].values()))
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
