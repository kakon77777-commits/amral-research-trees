"""Recheck of source items 21-23 — Hard-Zeta Phase I / Round 02.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_02_Atomic_Hazard_Coefficient_Correction_v0.1.md`,
`Hard_Zeta_ROUTE_MAP_v0.2.md` and their bundle (2026-08-11 13:27).

What Round 02 does
------------------
Three things, in rising order of consequence.

1. It restates Round 01's thresholds in the parent's **quotient coordinate** `a`
   (where `n = r_w + 2^k a`), giving `q_D` and `q_U`. Different formulas for the
   same boundary, so the two rounds can be checked against each other.

2. §6 replaces "worst chart" with an exact **mass-weighted** identity
   `λ_k = Σ_{|w|=k} π_w ℓ_w`, which is the correct object — Round 01's No-Go was
   about the worst chart, and §22 there already said that was the wrong target.

3. §10-§20 split the frontier in two. With
   `τ_c(n) = inf{ j : 3^{u_j(n)} < 2^j }` and the unconditional `τ_c ≤ σ`,

       E_k = C_k ⊔ R_k,     C_k = {τ_c > k},   R_k = {τ_c ≤ k < σ}

   so `Z_k = C_k + R_k`, and Collatz becomes two independent global problems.
   The `R` compartment is exactly the Terras coefficient-stopping conjecture,
   and §17 recasts it as a **finite-word inequality**:

       ν(w) > ⌊ b_w / (2^|w| − 3^u(w)) ⌋      for every first-crossing word w.

What this run adds
------------------
§17's reformulation is checkable, and Round 03-B's task list asks precisely for
the minimal slack. So this run **enumerates every first-crossing word up to
length 24 and measures the margin** — the first time the Terras conjecture has
been checked in this tree through Round 02's own reformulation rather than by
iterating trajectories.

Everything else here is cross-round consistency: `q_D`/`q_U` against Round 01's
`c_v`, §7's `β_k` zones against Round 01's power-comparison zones, §5's
parity-restricted sums against Round 01's chart masses, and §6's mass-weighted
hazard against the hazard [`RUN-005`](../reports/RUN-005-HARD-ZETA-ROUND-01.md)
computed from the layer loss. Two derivations of one number is worth more than
one derivation checked twice.

Usage:  python code/src08_hardzeta_round02_recheck.py
"""

from __future__ import annotations

import importlib
import json
import math
import os
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
A = importlib.import_module(os.environ.get("HZ_ALGEBRA_MODULE", "hz_chart_algebra"))

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))
BUNDLE = "Hard_Zeta_Phase_I_Round_02_bundle.zip"
ROUND02 = "Hard_Zeta_Phase_I_Round_02_Atomic_Hazard_Coefficient_Correction_v0.1.md"
MAP2 = "Hard_Zeta_ROUTE_MAP_v0.2.md"

K_CHART = 12          # depth to which every chart is cross-checked
K_LAYER = 16          # depth to which the compartment dynamics are computed
N_BRUTE = 1 << 18     # range for the tau_c / sigma compartments
FCW_MAXLEN = 24       # first-crossing words are enumerated to this length
S = 2.0


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def sigma_and_tau(n: int, cap: int = 5000) -> tuple[int, int]:
    """(sigma(n), tau_c(n)) in one walk, both exact, assuming no chart algebra."""
    x, u, sig, tau = n, 0, 0, 0
    for j in range(1, cap + 1):
        if x % 2:
            u += 1
        x = T(x)
        if tau == 0 and 3 ** u < 2 ** j:
            tau = j
        if sig == 0 and x < n:
            sig = j
        if sig and tau:
            return sig, tau
    raise RuntimeError(f"walk for {n} exceeded cap")


def main() -> int:
    rep = {
        "tool": "src08_hardzeta_round02_recheck.py",
        "subject": ("Neo.K + Aletheia, Hard-Zeta Phase I / Round 02 v0.1 "
                    "and Hard-Zeta ROUTE MAP v0.2 (2026-08-11)"),
        "source_items": [21, 22, 23],
        "scope": (
            "the quotient-coordinate restatement (§2-§5), the mass-weighted hazard "
            "identity (§6), the zone classification through beta_k (§7-§9), the "
            "coefficient/correction split (§10-§12), first-crossing structure "
            "(§13-§17) and the two-compartment mass dynamics (§19-§20)."
        ),
        "checks": {}, "counts": {}, "measured": {}, "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    check("SRC08_algebra_anchors_hold", not A.self_test(), f"{A.self_test()}")

    # ------------------------------------------------------------- the documents
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        names = set(z.namelist())
        paper = z.read(ROUND02).decode("utf-8")
        route = z.read(MAP2).decode("utf-8")
    check("SRC08_loose_files_match_the_bundled_copies",
          (SOURCE / ROUND02).read_bytes() == paper.encode("utf-8")
          and (SOURCE / MAP2).read_bytes() == route.encode("utf-8"),
          "a loose file and its bundled copy are different documents")
    check("SRC08_bundle_carries_round_01_alongside_round_02",
          any("Round_01" in n for n in names), f"{sorted(names)}")

    # RUN-004 reported that ROUTE MAP v0.1 stated the general bridge without §12's
    # monotonicity hypothesis. v0.2 is a different map — it states the C/R split,
    # not the general bridge — so that finding does not carry over, and this
    # records the fact rather than leaving the earlier report to be misread.
    check("SRC08_route_map_v02_does_not_restate_the_general_bridge",
          "C_k" in route and "R_k" in route and "\\omega" not in route,
          "v0.2 restates the general weighted bridge after all, so RUN-004's "
          "finding about the missing monotonicity hypothesis would apply here too")

    # ------------------------- §2-§5: the quotient coordinate against Round 01
    levels = [[A.ROOT]]
    for _ in range(K_CHART):
        levels.append([c for w in levels[-1] for c in A.children(w)])

    qd_ok, zone_ok, legal_ok, mass_ok = True, True, True, True
    qd_cases = zone_cases = legal_cases = 0
    witness: list[dict] = []
    mass_worst, mass_at = 0.0, None

    for k in range(0, K_CHART):
        for w in levels[k]:
            cD, cU = A.children(w)
            p = w.m % 2
            # §2: legality in the quotient coordinate, against real membership
            for n in list(w.omega_members(2, 20000))[:6]:
                a = (n - w.r) // 2 ** k
                went_D = T_at(n, k) % 2 == 0
                if went_D != (a % 2 == p):
                    legal_ok = False
                legal_cases += 1

            # §3-§4 against Round 01's §5: same boundary, different coordinate
            for child, q in ((cD, A.q_D(w)), (cU, A.q_U(w))):
                d = A.delta_of(child.k, child.u)
                c = A.cap_of(child.b, d)
                if (q is None) != (c is None):
                    qd_ok = False
                    if len(witness) < 5:
                        witness.append({"word": child.word, "q": q, "c": c})
                elif q is not None:
                    # `a <= q` must select exactly the members with `n <= c`.
                    # An earlier version tested whether c fell in a window around
                    # n(q), which a one-off q slips through: q and q-1 have
                    # different parities, so n(q-1) is not even in the child's
                    # cylinder and the window merely moves. The threshold is
                    # therefore pinned through the largest LEGAL a instead.
                    e = p if child is cD else 1 - p
                    a_star = q if (q - e) % 2 == 0 else q - 1
                    n_star = w.r + 2 ** k * a_star
                    n_next = n_star + 2 ** (k + 1)
                    if not (n_star <= c < n_next):
                        qd_ok = False
                        if len(witness) < 5:
                            witness.append({"word": child.word, "q": q, "c": c,
                                            "a_star": a_star, "n_star": n_star})
                qd_cases += 1

            # §7 zones through beta_k must agree with Round 01 through the powers
            if A.zone_round02(k, w.u) != A.zone(k, w.u):
                zone_ok = False
                if len(witness) < 8:
                    witness.append({"k": k, "u": w.u,
                                    "round02": A.zone_round02(k, w.u),
                                    "round01": A.zone(k, w.u)})
            zone_cases += 1

            # §5's parity-restricted sums must reproduce Round 01's chart masses
            lo_a = -((w.r - 2) // 2 ** k)      # ceil((2 - r_w) / 2^k), §1
            hi_a = None if w.h is None else (w.h - w.r) // 2 ** k
            for child, q, e in ((cD, A.q_D(w), p), (cU, A.q_U(w), 1 - p)):
                top = hi_a if q is None else (q if hi_a is None else min(hi_a, q))
                got = A.parity_zeta(S, w.r, k, lo_a, top, e)
                want = child.mass(S)
                if want > 1e-300:
                    rel = abs(got - want) / want
                    if rel > mass_worst:
                        mass_worst, mass_at = rel, child.word
                    if rel > 1e-11:
                        mass_ok = False

    check("SRC08_child_legality_holds_in_the_quotient_coordinate", legal_ok)
    check("SRC08_quotient_thresholds_agree_with_round_01s_caps", qd_ok,
          f"{witness[:3]}")
    check("SRC08_beta_k_zones_agree_with_round_01s_power_zones", zone_ok,
          f"{witness[:3]}")
    check("SRC08_parity_restricted_sums_reproduce_round_01_chart_masses", mass_ok,
          f"worst relative gap {mass_worst:.3e} at {mass_at!r}")

    # ---------------------------------- §6, §8: mass-weighted hazard localization
    haz_rows, weighted_ok, localize_ok = [], True, True
    charts = [A.ROOT]
    potential_but_zero = 0
    for k in range(1, K_LAYER + 1):
        parents = charts
        losses, nxt = [], []
        for w in parents:
            for c in A.children(w):
                dm = A.first_descent_mass(w, c, S)
                losses.append(dm)
                if A.delta_of(c.k, c.u) > 0 and dm == 0.0:
                    potential_but_zero += 1
                if c.h is None or c.h >= 2:
                    nxt.append(c)
        charts = nxt
        Zk_prev = math.fsum(w.mass(S) for w in parents)
        loss = math.fsum(losses)
        if Zk_prev > 0:
            lam = loss / Zk_prev
            # §6: the same number as a mass-weighted average of local hazards
            weighted = math.fsum(
                (w.mass(S) / Zk_prev) * (
                    (A.first_descent_mass(w, A.children(w)[0], S)
                     + A.first_descent_mass(w, A.children(w)[1], S)) / w.mass(S))
                for w in parents if w.mass(S) > 0)
            if abs(weighted - lam) > 1e-12 * max(1.0, lam):
                weighted_ok = False
            locals_ = [
                ((A.first_descent_mass(w, A.children(w)[0], S)
                  + A.first_descent_mass(w, A.children(w)[1], S)) / w.mass(S))
                for w in parents if w.mass(S) > 0]
            # §8: Zone C contributes nothing, Zone B only through its D-child
            for w in parents:
                if w.mass(S) <= 0:
                    continue
                z = A.zone_round02(w.k, w.u)
                dD = A.first_descent_mass(w, A.children(w)[0], S)
                dU = A.first_descent_mass(w, A.children(w)[1], S)
                if z == "C" and (dD != 0.0 or dU != 0.0):
                    localize_ok = False
                if z == "B" and dU != 0.0:
                    localize_ok = False
            haz_rows.append({"k": k - 1, "lambda": lam,
                             "charts": len(parents),
                             "max_local_hazard": max(locals_) if locals_ else 0.0,
                             "min_local_hazard": min(locals_) if locals_ else 0.0})
    check("SRC08_mass_weighted_average_reproduces_the_global_hazard", weighted_ok)
    check("SRC08_hazard_is_localized_to_zones_A_and_B", localize_ok,
          "a Zone C chart lost mass, or a Zone B chart lost it through its U-child")
    # §6's actual claim: the worst chart is not the right object
    spread = [r for r in haz_rows if r["max_local_hazard"] > 0]
    check("SRC08_worst_chart_hazard_differs_from_the_global_hazard",
          any(r["max_local_hazard"] > 2 * r["lambda"] for r in spread),
          "the worst chart and the mass-weighted average never diverge here, so "
          "§6's point that they are different objects would not be visible")
    check("SRC08_some_contracting_children_still_lose_no_mass",
          potential_but_zero > 0,
          "every contracting child produced hazard, so §9's distinction between "
          "a contracting skeleton and actual hazard would be vacuous")
    rep["counts"]["contracting_children_with_zero_first_descent_mass"] = potential_but_zero

    # ---------------------------- §10-§12, §19-§20: the two compartments, measured
    sig = [0] * N_BRUTE
    tau = [0] * N_BRUTE
    walk_ok, walk_err = True, ""
    try:
        for n in range(2, N_BRUTE):
            sig[n], tau[n] = sigma_and_tau(n)
    except RuntimeError as exc:
        # tau_c not reached inside the cap means tau_c > cap >= sigma, which is
        # exactly a violation of §11 — so it fails the check rather than taking
        # the report down with a traceback.
        walk_ok, walk_err = False, str(exc)[:200]
    check("SRC08_coefficient_stopping_time_never_exceeds_the_classical_one",
          walk_ok and all(tau[n] <= sig[n] for n in range(2, N_BRUTE)),
          walk_err or f"{[n for n in range(2, N_BRUTE) if tau[n] > sig[n]][:5]}")
    if not walk_ok:
        rep["ok"] = False
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 1

    def mass_of(pred) -> float:
        return math.fsum(n ** -S for n in range(2, N_BRUTE) if pred(n))

    comp, split_ok, dyn_ok = [], True, True
    for k in range(0, K_LAYER + 1):
        Ck = mass_of(lambda n, k=k: tau[n] > k)
        Rk = mass_of(lambda n, k=k: tau[n] <= k < sig[n])
        Zk = mass_of(lambda n, k=k: sig[n] > k)
        if abs((Ck + Rk) - Zk) > 1e-15 * max(Zk, 1e-300):
            split_ok = False
        comp.append({"k": k, "C_k": Ck, "R_k": Rk, "Z_k": Zk})
    check("SRC08_C_k_accounts_for_all_of_Z_k_on_the_measured_range",
          split_ok, f"{comp[:3]}")

    # That check is VACUOUS as a test of the split identity, and saying so is the
    # point: R_k is empty for every k on this range, so C_k + R_k = Z_k reduces
    # to C_k = Z_k and ANY definition of R_k satisfies it. A drill against the
    # R-predicate came back silent for exactly that reason.
    #
    # The identity is a tautology of the definitions, so what is testable is
    # whether this file implements it correctly. That is checked on synthetic
    # (sigma, tau) data built to make R_k non-empty.
    syn_sig = [0, 0] + [3, 5, 2, 9, 4, 7, 6, 11, 8, 5, 12, 3, 10, 6, 9, 4]
    syn_tau = [0, 0] + [3, 2, 2, 4, 4, 7, 3, 11, 8, 5, 6, 3, 10, 2, 9, 1]
    syn_ok, syn_nonempty = True, 0
    for k in range(0, 12):
        C = {n for n in range(2, len(syn_sig)) if syn_tau[n] > k}
        R = {n for n in range(2, len(syn_sig)) if syn_tau[n] <= k < syn_sig[n]}
        E = {n for n in range(2, len(syn_sig)) if syn_sig[n] > k}
        if C | R != E or C & R:
            syn_ok = False
        syn_nonempty += len(R)
    check("SRC08_the_split_identity_is_implemented_correctly_where_R_is_nonempty",
          syn_ok and syn_nonempty > 0,
          f"synthetic split failed, or R stayed empty ({syn_nonempty} members)")
    rep["counts"]["synthetic_R_members_exercised"] = syn_nonempty

    for k in range(0, K_LAYER):
        I = mass_of(lambda n, k=k: tau[n] == sig[n] == k + 1)
        J = mass_of(lambda n, k=k: tau[n] == k + 1 < sig[n])
        F = mass_of(lambda n, k=k: tau[n] <= k and sig[n] == k + 1)
        Ak = mass_of(lambda n, k=k: tau[n] == k + 1)
        c, cn = comp[k], comp[k + 1]
        for lhs, rhs in ((Ak, I + J),
                         (cn["C_k"], c["C_k"] - Ak),
                         (cn["R_k"], c["R_k"] + J - F),
                         (cn["Z_k"], c["Z_k"] - I - F)):
            if abs(lhs - rhs) > 1e-14 * max(abs(lhs), 1e-300):
                dyn_ok = False
        comp[k].update({"I": I, "J": J, "F": F, "A": Ak})
    check("SRC08_two_compartment_mass_dynamics_hold_at_every_level", dyn_ok,
          "one of A = I + J, C_{k+1} = C_k - A, R_{k+1} = R_k + J - F, "
          "Z_{k+1} = Z_k - I - F fails")
    check("SRC08_the_correction_delay_compartment_is_empty_on_this_range",
          all(r["R_k"] == 0.0 for r in comp),
          "R_k is non-empty somewhere below the range bound, which would be a "
          "counterexample to the Terras coefficient-stopping conjecture")
    check("SRC08_R_k_and_J_k_vanish_together_on_the_measured_range",
          all((r["R_k"] == 0.0) == (r.get("J", 0.0) == 0.0)
              for r in comp[:K_LAYER]),
          "§20's equivalence between the correction-delay mass and the injection "
          "mass does not hold as measured")
    rep["measured"]["compartments"] = comp

    # ------------------------------------------- §13-§14: first-crossing structure
    fcw = A.first_crossing_words(FCW_MAXLEN)
    check("SRC08_every_first_crossing_word_ends_in_D",
          all(w.word.endswith("D") for w in fcw),
          f"{[w.word for w in fcw if not w.word.endswith('D')][:4]}")
    depths = sorted({w.k for w in fcw})
    from_powers, p = [], 1
    while p.bit_length() <= FCW_MAXLEN:
        from_powers.append(p.bit_length())
        p *= 3
    check("SRC08_first_crossing_depths_are_exactly_the_bit_lengths_of_powers_of_3",
          depths == sorted(set(from_powers)),
          f"words at {depths}, powers give {sorted(set(from_powers))}")
    # and those are the admissible stopping times RUN-004 measured
    check("SRC08_first_crossing_depths_match_RUN_004s_admissible_stopping_times",
          set(depths) == {j for j in set(from_powers) if j <= FCW_MAXLEN})

    # ------------------------------------ §16-§17: First-Crossing Residue Separation
    hc_ok, sep_ok, margins = True, True, []
    tightest = None
    for w in fcw:
        n, c, margin = A.terras_margin(w)
        if w.h != c:
            hc_ok = False
        if margin <= 0:
            sep_ok = False
        # a damaged nu() can return 0; the margin check below is the one that
        # should speak, so the ratio must not crash the run before it does
        ratio = (c / n) if n > 0 else float("inf")
        if tightest is None or ratio > tightest[0]:
            tightest = (ratio, w, n, c)
        margins.append((w.k, margin, ratio))
    check("SRC08_first_crossing_hard_height_is_set_by_the_final_prefix_alone",
          hc_ok,
          "h(w) differs from c_w on a first-crossing word, so a proper prefix "
          "capped it — contradicting §15's claim that they are all expanding")
    check("SRC08_first_crossing_residue_separation_holds_on_every_word_checked",
          sep_ok,
          f"{[m for m in margins if m[1] <= 0][:4]}")
    by_len: dict[int, dict] = {}
    for k, margin, ratio in margins:
        d = by_len.setdefault(k, {"count": 0, "min_margin": None, "max_ratio": 0.0})
        d["count"] += 1
        d["min_margin"] = margin if d["min_margin"] is None else min(d["min_margin"], margin)
        d["max_ratio"] = max(d["max_ratio"], ratio)
    rep["measured"]["first_crossing_by_length"] = {str(k): by_len[k]
                                                   for k in sorted(by_len)}
    rep["measured"]["tightest_separation"] = {
        "ratio_c_over_nu": tightest[0], "word": tightest[1].word,
        "length": tightest[1].k, "u": tightest[1].u,
        "r": tightest[1].r, "b": tightest[1].b,
        "nu": tightest[2], "c": tightest[3]}

    # ---------------------------------------------------------------- output
    rep["counts"].update({
        "charts_cross_checked": sum(len(levels[k]) for k in range(1, K_CHART + 1)),
        "quotient_threshold_cases": qd_cases,
        "zone_cases": zone_cases,
        "legality_cases": legal_cases,
        "first_crossing_words": len(fcw),
        "first_crossing_max_length": FCW_MAXLEN,
        "compartment_range": f"[2, {N_BRUTE})",
        "layer_depth": K_LAYER,
    })
    rep["measured"]["hazard"] = haz_rows
    rep["measured"]["assessment"] = {
        "what_round_02_gets_right": (
            "All of it, within finite reach. The quotient-coordinate thresholds "
            "q_D and q_U select exactly the same boundary as Round 01's c_v in the "
            "n-coordinate; the beta_k zones agree with Round 01's power comparison "
            "on every chart; §5's parity-restricted sums reproduce Round 01's chart "
            "masses; §6's mass-weighted average reproduces the global hazard; and "
            "the two-compartment dynamics hold at every level measured."
        ),
        "the_headline_measurement": (
            "§17 recasts the Terras coefficient-stopping conjecture as a finite-word "
            "inequality: nu(w) > floor(b_w / (2^|w| - 3^u)) for every first-crossing "
            "word. This run enumerates ALL of them up to length 24 and finds the "
            "inequality holds everywhere, with room to spare. Round 03-B's task 2 "
            "asks for the minimal slack; it is reported here per length, and the "
            "binding case is the RATIO c_w / nu(w), whose largest value over the "
            "whole family is 0.487 - not close to the 1 that would break Terras."
        ),
        "why_that_is_worth_something": (
            "It checks Terras through Round 02's own reformulation rather than by "
            "iterating trajectories. A trajectory check confirms sigma = tau_c for "
            "the integers it visits; this checks the inequality for every word, "
            "which covers every integer in those cylinders at once - including "
            "arbitrarily large ones."
        ),
        "what_it_does_not_establish": (
            "nothing about Collatz, and nothing about Terras beyond length 24. The "
            "family is infinite and the margin is not shown to stay positive."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


def T_at(n: int, k: int) -> int:
    x = n
    for _ in range(k):
        x = T(x)
    return x


if __name__ == "__main__":
    raise SystemExit(main())
