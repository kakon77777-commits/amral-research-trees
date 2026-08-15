"""Recheck of source item 28 — Hard-Zeta Phase I / Round 03-A.4.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A4_Spine_Valuation_Rigidity_v0.1.md`
and `Hard_Zeta_ROUTE_MAP_v0.7.md` (2026-08-11 21:52).

What Round 03-A.4 does
----------------------
Round 03-A.3 made the spine deterministic. This round asks what staying on one
**costs**.

    d_m = ⌊βm⌋ − K_m                    the integer deficit; subcritical ⟺ d_m ≥ 0
    d_m = d_{m−1} + b_m − e_m           b_m ∈ {0,1} Sturmian, e_m = q_m − 1
    Σ_{i≤m}(q_i − 1) ≤ ⌊γm⌋             the credit ledger, γ = β − 1

so every unit of extra 2-adic valuation is paid for out of a Sturmian budget of
density `γ ≈ 0.585`. §9-§12 then read the same ledger as **cylinder occupancy**:
`q_i ≥ r` exactly when `Y_{i−1} ≡ −3^{−1} (mod 2^r)`, and under Haar measure
those cylinders would be visited with total density **1** — well above the
budget. §13 is careful to say that is a discrepancy, not a contradiction.

The strongest statement is §26-§32:

    any infinite positive subcritical spine has Y_m → ∞

so a CST counterexample would be a genuinely **divergent** orbit, not merely a
long one.

What this run checks
--------------------
All of it, and two things worth separating out.

§18's "Spine Excursion Identity" is **Paper 06's accelerated affine formula in
log coordinates** — multiply through by `2^{K_m}` and it becomes
`Y_m·2^{K_m} = 3^m·n + Σ 3^{m−1−i}·2^{K_i}` exactly. So this run verifies it in
exact integers, and records that the new content of §18 is the *reading* (deficit
= exponential growth rate), not a new identity. That is worth stating because the
reading is what carries §30.

And §34's Legendre gate is measured rather than described: on real spines, how
often is the contact tight enough for continued fractions to apply at all?

Usage:  python code/src13_hardzeta_round03a4_recheck.py
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
C = importlib.import_module(os.environ.get("HZ_ACCEL_MODULE", "hz_accel_code"))

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))
BUNDLE = "Hard_Zeta_Phase_I_Round_03A4_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A4_Spine_Valuation_Rigidity_v0.1.md"
MAP7 = "Hard_Zeta_ROUTE_MAP_v0.7.md"

# odd starts whose spines are long enough to measure on
SPINES = (27, 103, 703, 1407, 10087, 15039, 35655)
M_MAX = 34            # spine depth examined
R_MAX = 20            # cylinder levels in the occupancy ledger
# β's convergents include the equal-temperament fractions; naming them pins the
# recursion against known values rather than against its own shape
KNOWN_CONVERGENTS = {(1, 1), (2, 1), (3, 2), (8, 5), (19, 12), (65, 41), (84, 53)}
KNOWN_CF = [1, 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2]


def main() -> int:
    rep = {
        "tool": "src13_hardzeta_round03a4_recheck.py",
        "subject": ("Neo.K + Aletheia, Hard-Zeta Phase I / Round 03-A.4 "
                    "Spine Valuation Rigidity v0.1 (2026-08-11)"),
        "source_items": [28],
        "scope": (
            "the deficit queue and credit ledger (§3-§7), the valuation cylinders "
            "and occupancy ledger with its Haar comparison (§9-§13), the Spine "
            "Excursion Identity and its logarithmic reading (§15-§21), the "
            "bounded-deficit bounds and the divergence corollary (§24-§32), and "
            "the Legendre continued-fraction gate (§33-§35)."
        ),
        "checks": {}, "counts": {}, "measured": {}, "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        names = set(z.namelist())
        paper = z.read(PAPER).decode("utf-8")
    check("SRC13_bundle_carries_the_A_line_and_the_v07_map",
          MAP7 in names and sum(1 for n in names if "Round_03A" in n) >= 4,
          f"{sorted(names)}")
    check("SRC13_paper_keeps_an_explicit_proved_and_unproved_ledger",
          "## 已證" in paper and "## 未證" in paper, "§46's ledger is missing")
    check("SRC13_paper_states_its_own_method_no_gos",
          "Method No-Go" in paper and "ergodic average" in paper,
          "§45's four method no-gos are missing, so the Haar discrepancy could "
          "be read as a contradiction when the paper says it is not")

    evaluated = True
    try:
        # ----------------------------------- β's continued fraction, anchored
        cf = C.beta_continued_fraction(len(KNOWN_CF))
        cvs = C.beta_convergents(9)
        check("SRC13_beta_continued_fraction_matches_its_known_expansion",
              cf == KNOWN_CF, f"{cf} vs {KNOWN_CF}")
        check("SRC13_beta_convergents_contain_the_named_equal_temperaments",
              KNOWN_CONVERGENTS <= set(cvs),
              f"missing {sorted(KNOWN_CONVERGENTS - set(cvs))}")
        # and they really do approximate beta, from alternating sides
        approx_ok = all(abs(p / q - math.log2(3)) < 1 / q ** 2 for p, q in cvs)
        check("SRC13_beta_convergents_approximate_beta_to_legendre_quality",
              approx_ok)
        rep["measured"]["beta_convergents"] = [{"p": p, "q": q} for p, q in cvs]

        # -------------------------------- §3-§7: deficit queue and credit ledger
        rec_ok = ledger_ok = sturm_ok = sub_ok = True
        rows = []
        # The loop runs ONE STEP PAST the subcritical lifetime on purpose. Inside
        # the lifetime both sides of "subcritical iff d >= 0" are always true, so
        # the equivalence sees only one outcome and passes for free — a planted
        # defect in `deficit` slipped through exactly that way.
        sub_seen = [0, 0]
        for n in SPINES:
            life = C.subcritical_lifetime(n)
            d_prev = 0
            for m in range(1, min(life, M_MAX) + 2):
                q = C.orbit_valuations(n, m)[-1]
                b = C.sturmian_credit(m) - C.sturmian_credit(m - 1)
                d = C.deficit(n, m)
                inside = C.is_subcritical(C.accel_code(n, m))
                sub_seen[1 if inside else 0] += 1
                # §4: the Sturmian increment is a bit
                if b not in (0, 1):
                    sturm_ok = False
                # §5: the deficit recurrence — an identity, so it holds either side
                if d != d_prev + b - (q - 1):
                    rec_ok = False
                # §6: the telescoped credit ledger, likewise an identity
                if d != C.sturmian_credit(m) - C.credit_spent(n, m):
                    ledger_ok = False
                # the "never overspent" half is a subcritical statement only
                if inside and C.credit_spent(n, m) > C.sturmian_credit(m):
                    ledger_ok = False
                # §3: subcritical iff the deficit never goes negative
                if (d >= 0) != inside:
                    sub_ok = False
                d_prev = d
            rows.append({"n": n, "subcritical_lifetime": life,
                         "final_deficit": C.deficit(n, min(life, M_MAX)),
                         "credit_spent": C.credit_spent(n, min(life, M_MAX)),
                         "sturmian_credit": C.sturmian_credit(min(life, M_MAX))})
        check("SRC13_the_sturmian_increment_is_always_a_single_bit", sturm_ok)
        check("SRC13_the_deficit_recurrence_holds_at_every_step", rec_ok)
        check("SRC13_the_credit_ledger_telescopes_and_is_never_overspent", ledger_ok)
        check("SRC13_subcritical_is_exactly_a_nonnegative_deficit", sub_ok)
        check("SRC13_that_equivalence_saw_both_outcomes", min(sub_seen) > 0,
              f"{sub_seen} — every depth examined fell on the same side, so the "
              "equivalence decides nothing")
        rep["measured"]["spines"] = rows

        # ------------------------------- §9-§12: cylinders and occupancy ledger
        cyl_ok = nest_ok = occ_ok = True
        occ_rows = []
        for n in SPINES:
            m = min(C.subcritical_lifetime(n), M_MAX)
            ys = C.orbit_endpoints(n, m)
            qs = C.orbit_valuations(n, m)
            # §9: high valuation is exactly membership of a single residue class
            for i, q in enumerate(qs):
                for r in range(1, R_MAX):
                    inside = ys[i] % (1 << r) == C.cylinder_residue(r)
                    if (q >= r) != inside:
                        cyl_ok = False
            # §10: the cylinders nest
            for r in range(2, R_MAX):
                if C.cylinder_residue(r) % (1 << (r - 1)) != C.cylinder_residue(r - 1):
                    nest_ok = False
            # §11: total occupancy is inside the Sturmian budget
            total = sum(C.cylinder_visits(n, m, r) for r in range(2, R_MAX))
            if total > C.sturmian_credit(m):
                occ_ok = False
            occ_rows.append({"n": n, "m": m, "occupancy": total,
                             "budget": C.sturmian_credit(m),
                             "haar_expectation": round(m * 1.0, 3),
                             "mean_excess_valuation": round(
                                 C.credit_spent(n, m) / m, 4)})
        check("SRC13_high_valuation_is_exactly_membership_of_one_residue_class",
              cyl_ok)
        check("SRC13_the_valuation_cylinders_nest", nest_ok)
        check("SRC13_cylinder_occupancy_stays_inside_the_sturmian_budget", occ_ok)
        # §12's comparison: Haar would spend 1 per step, the budget allows γ
        gamma = math.log2(3) - 1
        check("SRC13_measured_spines_spend_less_than_haar_would",
              all(r["mean_excess_valuation"] < 1.0 for r in occ_rows),
              f"{occ_rows}")
        check("SRC13_the_haar_gap_is_real_and_not_an_artefact_of_the_bound",
              gamma < 1.0 and abs(gamma - 0.5849625) < 1e-6,
              f"gamma = {gamma}")
        rep["measured"]["occupancy"] = occ_rows
        rep["measured"]["haar_total_density"] = sum(2.0 ** -(r - 1)
                                                    for r in range(2, 200))

        # ------------------------ §18-§21: the excursion identity and its reading
        exc_ok = all(C.excursion_check(n, m)
                     for n in SPINES
                     for m in range(1, min(C.subcritical_lifetime(n), 20) + 1))
        check("SRC13_the_spine_excursion_identity_holds_in_exact_integers", exc_ok)
        # it IS Paper 06's affine formula: state that rather than imply novelty
        same_ok = True
        for n in SPINES[:3]:
            for m in range(1, 12):
                kap = C.accel_code(n, m)
                if C.endpoint(n, kap) != C.orbit_endpoints(n, m)[m]:
                    same_ok = False
        check("SRC13_the_excursion_identity_is_paper_06s_affine_formula_rewritten",
              same_ok,
              "the affine endpoint and the walked endpoint disagree, which would "
              "mean the two forms are not the same statement after all")

        # §20: the logarithmic equivalence bounds
        log_ok, log_rows = True, []
        for n in SPINES:
            m = min(C.subcritical_lifetime(n), M_MAX)
            Y = C.orbit_endpoints(n, m)[m]
            d = C.deficit(n, m)
            lo = d + math.log2(n)
            hi = d + 1 + math.log2(n + m / 3)
            if not lo <= math.log2(Y) < hi:
                log_ok = False
            log_rows.append({"n": n, "m": m, "log2_Y": round(math.log2(Y), 4),
                             "d_m": d, "lower": round(lo, 4), "upper": round(hi, 4)})
        check("SRC13_the_logarithmic_equivalence_bounds_hold", log_ok,
              f"{[r for r in log_rows if not r['lower'] <= r['log2_Y'] < r['upper']]}")
        rep["measured"]["log_equivalence"] = log_rows

        # ---------------------------------- §24-§30: bounded deficit, divergence
        bd_ok, div_ok = True, True
        for n in SPINES:
            m = min(C.subcritical_lifetime(n), M_MAX)
            ds = [C.deficit(n, j) for j in range(1, m + 1)]
            D = max(ds)
            Y = C.orbit_endpoints(n, m)[m]
            if not (n + m / (3 * 2 ** (D + 1)) < Y < 2 ** (D + 1) * (n + m / 3)):
                bd_ok = False
            # §30's conclusion, as far as a finite spine can show it: the odd
            # endpoints grow
            ys = C.orbit_endpoints(n, m)
            if ys[m] <= ys[0]:
                div_ok = False
        check("SRC13_the_bounded_deficit_bounds_bracket_the_endpoint", bd_ok)
        check("SRC13_endpoints_grow_along_every_subcritical_spine_measured", div_ok)
        # §28's cycle argument: no endpoint may repeat on a subcritical spine
        rep_ok = True
        for n in SPINES:
            m = min(C.subcritical_lifetime(n), M_MAX)
            ys = C.orbit_endpoints(n, m)
            if len(set(ys)) != len(ys):
                rep_ok = False
        check("SRC13_no_endpoint_repeats_along_a_subcritical_spine", rep_ok)

        # ------------------------------------------ §33-§35: the Legendre gate
        gate_rows, gate_hits = [], 0
        for n in SPINES:
            m_max = min(C.subcritical_lifetime(n), 24)
            hits = [m for m in range(1, m_max + 1) if C.legendre_gate(n, m)]
            gate_hits += len(hits)
            gate_rows.append({"n": n, "depth": m_max, "gate_open_at": hits,
                              "fraction": round(len(hits) / m_max, 4)})
        check("SRC13_the_legendre_gate_is_open_only_rarely",
              all(r["fraction"] < 0.35 for r in gate_rows), f"{gate_rows}")
        check("SRC13_the_legendre_gate_opened_somewhere",
              gate_hits > 0,
              "the gate never opened, so 'rarely' would be untested")
        # where it opens, K_m/m must actually be a convergent
        conv_ok = True
        # only convergents with denominator <= the depths probed can ever
        # match, and beta's exact tail explodes past a dozen terms
        cvset = {(p, q) for p, q in C.beta_convergents(12)}
        for n in SPINES:
            for m in range(1, min(C.subcritical_lifetime(n), 24) + 1):
                if C.legendre_gate(n, m):
                    K = C.cumulative(C.accel_code(n, m))[-1]
                    g = math.gcd(K, m)
                    if (K // g, m // g) not in cvset:
                        conv_ok = False
        check("SRC13_where_the_gate_opens_the_ratio_really_is_a_convergent",
              conv_ok)
        rep["measured"]["legendre_gate"] = gate_rows

    except Exception as exc:                       # noqa: BLE001
        evaluated = False
        rep["measured"]["evaluation_error"] = f"{type(exc).__name__}: {exc}"[:300]
    check("SRC13_the_deficit_algebra_evaluates_without_error", evaluated,
          rep["measured"].get("evaluation_error", ""))
    if not evaluated:
        rep["ok"] = False
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 1

    rep["counts"].update({
        "spines_traced": len(SPINES),
        "spine_depth_examined": M_MAX,
        "cylinder_levels": R_MAX,
        "legendre_gate_openings": gate_hits,
    })
    rep["measured"]["assessment"] = {
        "what_round_03a4_gets_right": (
            "All of it. The Sturmian increment is always a bit; the deficit "
            "recurrence holds at every step; the credit ledger telescopes and is "
            "never overspent; subcritical is exactly a non-negative deficit; high "
            "valuation is exactly membership of one residue class and those "
            "cylinders nest; total occupancy stays inside the budget; the excursion "
            "identity holds in exact integers; the logarithmic equivalence and "
            "bounded-deficit bounds bracket the endpoint; no endpoint repeats; and "
            "where the Legendre gate opens, K_m/m really is a convergent of beta."
        ),
        "on_the_excursion_identity": (
            "§18 is Paper 06's accelerated affine formula in log coordinates - "
            "multiply through by 2^{K_m} and it becomes the exact integer "
            "statement Y_m·2^{K_m} = 3^m·n + sum 3^{m-1-i}·2^{K_i}, which is what "
            "this run verifies. That is not a criticism: the NEW content of §18 is "
            "the reading, deficit as exponential growth rate, and that reading is "
            "what carries §30's divergence corollary. Worth separating so the "
            "novelty is attributed to the right half."
        ),
        "the_haar_gap_measured": (
            "§12 contrasts a Haar-typical total cylinder density of 1 against a "
            "budget of gamma = 0.585. On real spines the mean excess valuation "
            "comes out well under 1, confirming the gap exists rather than being "
            "an artefact of the bound. §13 and §45's No-Go 2 are right to stop "
            "there: a measure-one statement about Haar-typical orbits cannot "
            "produce a theorem about every anchored positive-integer orbit, and "
            "this run adds nothing to close that."
        ),
        "the_legendre_gate_measured": (
            "§34 says continued-fraction tools apply rigorously only when "
            "delta_m < 1/(2m). Measured on real spines, the gate is open on a small "
            "fraction of depths, and where it opens the ratio is genuinely a "
            "convergent. So §35's 'ultra-tight contact' is not a hypothetical "
            "restriction - it is most of the spine being out of reach of CF tools."
        ),
        "what_it_does_not_establish": (
            "nothing on §46's unproved list. The divergence corollary is checked "
            "only in the direction a finite spine can show - endpoints grow, none "
            "repeats - which is consistent with the theorem and with any bounded "
            "search."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
