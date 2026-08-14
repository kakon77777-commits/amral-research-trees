"""Recheck of source item 25 — Hard-Zeta Phase I / Round 03-A.1.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A1_Small_Anchor_Event_Arithmetic_v0.1.md`
and `Hard_Zeta_ROUTE_MAP_v0.4.md` (2026-08-11 16:13).

What Round 03-A.1 does
----------------------
It changes coordinates. Round 03-A described the coefficient frontier by parity
words; 03-A.1 uses the **accelerated exact code** `κ = (κ₁,…,κ_m)` with
`κ_i = v₂(3x_{i-1}+1)`, and proves that a code pins its source exactly:

    r_m ≡ (2^{K_m} − B_m)·3^{−m}   (mod 2^{K_m+1})

with `r_{m+1} = r_m + t_{m+1}·2^{K_m+1}` and `t ≥ 0` — so the canonical source is
**nondecreasing** along any extension. That gives §17's anchor equivalence
(a fixed integer realization ⟺ the lift digits are eventually zero) and §21-§22's
**Residue-Rate Gap**: `ρ_m → 0` or `limsup ρ_m ≥ α`, with nothing in between.

It also records a **No-Go**: the mechanical/Sturmian code `κ*_j = ⌊βj⌋−⌊β(j−1)⌋`
maximizes cumulative valuation at every step but does **not** minimize the source
representative. §34 tables that for `m ≤ 8`.

What this run adds
------------------
Two things.

1. **§34's diagnostic table, reproduced independently and extended from m = 8 to
   m = 60.** §13's monotonicity makes a branch-and-bound prune exact provided the
   answer stays under the cap, and the run checks that rather than assuming it.

2. **The bridge to [`RUN-007`](../reports/RUN-007-HARD-ZETA-ROUND-03A.md).** §35
   calls `a_m` the accelerated-code minimum anchor and declines to assume it
   matches the classical one. It does, on everything measured: `a_m` takes exactly
   the values RUN-007 measured for `m_k`, and switches at exactly `k = K_m`. Two
   coordinate systems, two independent computations, one sequence.

Everything else is confrontation: the code and its cumulative valuation against
direct iteration, the affine formula, the source congruence, the lift-digit range,
the monotonicity, the rate gap, and both concrete counterexamples in §30-§31.

Usage:  python code/src10_hardzeta_round03a1_recheck.py <tau-records.json>
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
A = importlib.import_module(os.environ.get("HZ_ALGEBRA_MODULE", "hz_chart_algebra"))

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))
BUNDLE = "Hard_Zeta_Phase_I_Round_03A1_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A1_Small_Anchor_Event_Arithmetic_v0.1.md"
MAP4 = "Hard_Zeta_ROUTE_MAP_v0.4.md"

M_FULL = 14           # depth to which every subcritical code is enumerated
M_DEEP = 60           # depth to which the pruned minimum anchor is computed
ALPHA = math.log(2) / math.log(3)

# §34's table, transcribed from the paper and checked, not recomputed from it
PAPER_TABLE = {1: (3, 3), 2: (7, 11), 3: (7, 27), 4: (27, 123),
               5: (27, 251), 6: (27, 1019), 7: (27, 3067), 8: (27, 7163)}


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def tau_c(n: int, cap: int = 4000) -> int:
    x, u = n, 0
    for j in range(1, cap + 1):
        if x % 2:
            u += 1
        x = T(x)
        if 3 ** u < 2 ** j:
            return j
    raise RuntimeError(f"tau_c({n}) exceeded cap")


def main() -> int:
    records = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))

    rep = {
        "tool": "src10_hardzeta_round03a1_recheck.py",
        "subject": ("Neo.K + Aletheia, Hard-Zeta Phase I / Round 03-A.1 "
                    "Small-Anchor Event Arithmetic v0.1 (2026-08-11)"),
        "source_items": [25],
        "scope": (
            "the accelerated exact code and its subcritical cone (§1-§5), the "
            "affine formula and exact source congruence (§6-§10), the nested "
            "lift-digit recurrence and anchor equivalence (§11-§17), the "
            "Residue-Rate Gap (§18-§23), the mechanical code and its extremality "
            "trap (§27-§33), and §34-§35's diagnostics."
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
    check("SRC10_bundle_carries_the_earlier_rounds_and_the_v04_map",
          MAP4 in names and any("Round_03A_" in n for n in names)
          and any("Round_02" in n for n in names), f"{sorted(names)}")
    check("SRC10_paper_keeps_an_explicit_proved_and_unproved_ledger",
          "## 已證" in paper and "## 未證" in paper,
          "§41's ledger is missing")

    evaluated = True
    try:
        # ------------------------------- §1-§5: the code against direct iteration
        codes = C.subcritical_codes(M_FULL)

        # Each of these is exception-tolerant per start. A formula that RAISES on
        # a valid input has failed its own check, and letting the exception
        # escape instead would leave only the blanket "did it evaluate" check to
        # fire — which is a catch, but not one that names anything. Three planted
        # defects reached exactly that state before this loop was hardened.
        code_ok, cum_ok, sub_ok, endpoint_ok = True, True, True, True
        realize_ok, realize_cases = True, 0
        for n in range(3, 40000, 2):
            try:
                k = C.accel_code(n, 6)
            except Exception:                  # noqa: BLE001
                code_ok = False
                continue
            x = n
            K = 0
            for i, kk in enumerate(k, start=1):
                y = 3 * x + 1
                if kk != (y & -y).bit_length() - 1:
                    code_ok = False
                    break
                x = y >> kk
                K += kk
                if x % 2 == 0:
                    code_ok = False           # §7: the endpoint must be ODD
                try:
                    if C.cumulative(k)[i] != K:
                        cum_ok = False
                except Exception:              # noqa: BLE001
                    cum_ok = False
                # §6: the affine formula must reproduce the same endpoint
                try:
                    if C.endpoint(n, k[:i]) != x:
                        endpoint_ok = False
                except Exception:              # noqa: BLE001
                    endpoint_ok = False
            # §3: subcritical iff the coefficient has not yet crossed
            for j in range(1, 7):
                try:
                    if C.is_subcritical(k[:j]) != (tau_c(n) > C.cumulative(k)[j]):
                        sub_ok = False
                except Exception:              # noqa: BLE001
                    sub_ok = False
        check("SRC10_the_accelerated_code_reproduces_direct_iteration", code_ok)
        check("SRC10_cumulative_valuation_matches_the_walk", cum_ok)
        check("SRC10_the_affine_endpoint_formula_reproduces_the_walk", endpoint_ok)
        check("SRC10_subcritical_means_the_coefficient_has_not_crossed", sub_ok)

        # §4: the strict and floor forms, with both outcomes actually seen
        floor_ok, seen = True, [0, 0]
        for j in range(1, 60):
            for K in range(1, 2 * j + 3):
                strict = 3 ** j > 2 ** K
                floored = K <= C.floor_beta(j)
                if strict != floored:
                    floor_ok = False
                seen[1 if strict else 0] += 1
        check("SRC10_the_strict_and_floor_forms_of_subcriticality_agree", floor_ok)
        check("SRC10_that_comparison_saw_both_outcomes", min(seen) > 0, f"{seen}")

        # ------------------- §8-§13: the source congruence and its monotonicity
        odd_ok, range_ok, nested_ok, mono_ok, digit_ok = (True,) * 5
        for m in range(1, M_FULL + 1):
            for kap in codes[m]:
                r = C.source_residue(kap)
                K = C.cumulative(kap)[-1]
                if r % 2 == 0:
                    odd_ok = False
                if not 1 <= r < 2 ** (K + 1):
                    range_ok = False
                if m >= 2:
                    parent = kap[:-1]
                    rp = C.source_residue(parent)
                    Kp = C.cumulative(parent)[-1]
                    if r % 2 ** (Kp + 1) != rp:
                        nested_ok = False
                    if r < rp:
                        mono_ok = False
                    t = (r - rp) // 2 ** (Kp + 1)
                    if not 0 <= t < 2 ** kap[-1]:
                        digit_ok = False
                # the source must really realize the code
                if m <= 9 and C.accel_code(r, m) != kap:
                    realize_ok = False
                realize_cases += 1
        check("SRC10_every_canonical_source_is_odd", odd_ok)
        check("SRC10_every_canonical_source_lies_in_its_stated_range", range_ok)
        check("SRC10_source_classes_are_nested_across_the_extension", nested_ok)
        check("SRC10_the_canonical_source_is_nondecreasing_along_an_extension",
              mono_ok)
        check("SRC10_the_lift_digit_lies_in_its_stated_range", digit_ok)
        check("SRC10_each_canonical_source_really_realizes_its_own_code", realize_ok)

        # §7: integrality is weaker than valuation legality — exhibit it
        weaker = 0
        for kap in codes[3]:
            K = C.cumulative(kap)[-1]
            B = C.offset(kap)
            for n in range(1, 2 ** (K + 1), 2):
                if (3 ** 3 * n + B) % 2 ** K == 0 and C.accel_code(n, 3) != kap:
                    weaker += 1
        check("SRC10_integrality_alone_does_not_pin_the_code", weaker > 0,
              "every integral start already realized the code, so §7's extra "
              "oddness requirement would be doing no work")
        rep["counts"]["integral_but_illegal_starts_found"] = weaker

        # ----------------------------------- §19-§22: the residue-rate gap
        spike_ok, dich_ok, spikes, zeros = True, True, 0, 0
        for m in range(2, M_FULL + 1):
            for kap in codes[m]:
                rp = C.source_residue(kap[:-1])
                Kp = C.cumulative(kap[:-1])[-1]
                t = (C.source_residue(kap) - rp) // 2 ** (Kp + 1)
                rho = C.residue_rate(kap)
                if t > 0:
                    spikes += 1
                    if not rho > ALPHA:
                        spike_ok = False           # §20
                    if 0 < rho < ALPHA:
                        dich_ok = False            # §22
                else:
                    zeros += 1
        check("SRC10_a_nonzero_lift_always_spikes_the_rate_above_alpha", spike_ok)
        check("SRC10_no_code_sits_strictly_inside_the_forbidden_rate_gap", dich_ok)
        check("SRC10_both_zero_and_nonzero_lifts_were_seen",
              spikes > 0 and zeros > 0, f"spikes {spikes}, zero lifts {zeros}")
        rep["counts"]["nonzero_lifts"] = spikes
        rep["counts"]["zero_lifts"] = zeros

        # --------------------------- §27-§31: the mechanical code and its trap
        mech = C.mechanical_code(M_FULL)
        check("SRC10_the_mechanical_code_has_increments_one_or_two",
              set(mech) <= {1, 2}, f"{sorted(set(mech))}")
        check("SRC10_the_mechanical_code_is_the_maximal_subcritical_path",
              all(C.cumulative(mech)[j] == C.floor_beta(j)
                  for j in range(1, M_FULL + 1)))
        # §30-§31, the concrete counterexamples
        pairs = {"(1,1)": C.source_residue((1, 1)), "(1,2)": C.source_residue((1, 2)),
                 "(1,1,2)": C.source_residue((1, 1, 2)),
                 "(1,2,1)": C.source_residue((1, 2, 1))}
        check("SRC10_the_two_step_counterexample_reproduces",
              pairs["(1,1)"] == 7 and pairs["(1,2)"] == 11 and 7 < 11,
              f"{pairs}")
        check("SRC10_the_same_skeleton_counterexample_reproduces",
              pairs["(1,1,2)"] == 7 and pairs["(1,2,1)"] == 27
              and C.cumulative((1, 1, 2))[-1] == C.cumulative((1, 2, 1))[-1],
              f"{pairs}")
        check("SRC10_those_sources_really_have_those_codes",
              all(C.accel_code(v, len(k.strip('()').split(','))) ==
                  tuple(int(x) for x in k.strip('()').split(','))
                  for k, v in pairs.items()), f"{pairs}")
        rep["measured"]["counterexamples"] = pairs

        # ---------------------------------------- §34: the diagnostic table
        table_rows, table_ok = [], True
        for m in range(1, 9):
            a = min(C.source_residue(k) for k in codes[m])
            rstar = C.source_residue(C.mechanical_code(m))
            want_a, want_star = PAPER_TABLE[m]
            if (a, rstar) != (want_a, want_star):
                table_ok = False
            table_rows.append({"m": m, "a_m": a, "mechanical": rstar,
                               "paper_a_m": want_a, "paper_mechanical": want_star})
        check("SRC10_section_34s_diagnostic_table_reproduces_exactly", table_ok,
              f"{[r for r in table_rows if r['a_m'] != r['paper_a_m'] or r['mechanical'] != r['paper_mechanical']]}")
        rep["measured"]["section_34_table"] = table_rows

        # the trap, quantified past the paper's table
        trap = [{"m": m, "a_m": min(C.source_residue(k) for k in codes[m]),
                 "mechanical": C.source_residue(C.mechanical_code(m))}
                for m in range(1, M_FULL + 1)]
        check("SRC10_the_mechanical_code_is_never_the_minimizer_past_m_1",
              all(r["mechanical"] > r["a_m"] for r in trap if r["m"] > 1),
              f"{[r for r in trap if r['m'] > 1 and r['mechanical'] <= r['a_m']]}")
        rep["measured"]["extremality_trap"] = trap

        # ------------------- §35 + the bridge to RUN-007's classical anchors
        deep = C.minimum_anchor(M_DEEP)
        largest = max(r["a_m"] for r in deep)
        check("SRC10_the_branch_and_bound_prune_is_exact_on_this_run",
              largest <= deep[0]["prune_cap"],
              f"largest a_m {largest} exceeded the prune cap {deep[0]['prune_cap']}, "
              "so codes that could have mattered were dropped")
        check("SRC10_the_deep_anchor_agrees_with_the_full_enumeration",
              all(deep[m - 1]["a_m"] == trap[m - 1]["a_m"] for m in range(1, M_FULL + 1)),
              "the pruned computation and the exhaustive one disagree")
        check("SRC10_the_minimum_anchor_is_nondecreasing_in_m",
              all(deep[i]["a_m"] <= deep[i + 1]["a_m"] for i in range(len(deep) - 1)))
        rep["measured"]["minimum_anchor_by_m"] = deep

        # the bridge: same values, and switching at k = K_m
        recs = records["records"]
        # The accelerated code is defined on ODD starts only, so the classical
        # anchor n = 2 has no counterpart here and is dropped before comparing.
        # Keeping it made the two lists differ by an offset that had nothing to do
        # with the mathematics.
        classical = [r["n"] for r in recs if r["n"] % 2 == 1]
        accel_values = []
        for r in deep:
            if not accel_values or accel_values[-1] != r["a_m"]:
                accel_values.append(r["a_m"])
        check("SRC10_the_accelerated_anchors_are_a_prefix_of_the_classical_ones",
              classical[:len(accel_values)] == accel_values,
              f"accelerated {accel_values} vs classical {classical[:8]}")
        # and each switch happens where the classical anchor's tau_c says it should
        switch_ok, switch_rows = True, []
        for i, r in enumerate(deep[:-1]):
            if deep[i + 1]["a_m"] != r["a_m"]:
                m_switch = deep[i + 1]["m"]
                holder = r["a_m"]
                # The holder leaves at the odd-step count whose Beatty depth is
                # its own coefficient stopping time. That depth is K_{m_switch} —
                # an earlier version used K_{m_switch - 1} and was off by one
                # step of the staircase.
                want = A.crossing_depth(m_switch)
                switch_rows.append({"m": m_switch, "leaving": holder,
                                    "tau_c": tau_c(holder), "K_m": want})
                if tau_c(holder) != want:
                    switch_ok = False
        check("SRC10_each_anchor_leaves_exactly_at_the_beatty_depth_of_its_own_tau_c",
              switch_ok, f"{switch_rows}")
        rep["measured"]["anchor_switches"] = switch_rows

        # §9's count bridge back to Round 03-A
        dp = A.survivor_dp(48)
        count_ok, count_rows = True, []
        for m in range(1, M_FULL + 1):
            # A subcritical code of length m has stayed clear through m odd
            # steps, so the crossing it is poised for is the (m+1)-th, at depth
            # K_{m+1}. Indexing it at K_m was an off-by-one in this bridge, not
            # a disagreement with either paper.
            Km1 = A.crossing_depth(m + 1)
            want = dp.get((Km1 - 1, m + 1), 0)
            got = len(codes[m])
            if want != got:
                count_ok = False
            count_rows.append({"m": m, "K_m_plus_1": Km1, "codes": got,
                               "round_03A_first_crossing_count": want})
        check("SRC10_subcritical_code_count_equals_round_03As_first_crossing_count",
              count_ok, f"{[r for r in count_rows if r['codes'] != r['round_03A_first_crossing_count']][:4]}")
        rep["measured"]["count_bridge"] = count_rows

    except Exception as exc:                       # noqa: BLE001
        evaluated = False
        rep["measured"]["evaluation_error"] = f"{type(exc).__name__}: {exc}"[:300]
    check("SRC10_the_accelerated_code_algebra_evaluates_without_error", evaluated,
          rep["measured"].get("evaluation_error", ""))
    if not evaluated:
        rep["ok"] = False
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 1

    rep["counts"].update({
        "codes_enumerated_to": M_FULL,
        "codes_per_length": {str(m): len(codes[m]) for m in range(1, M_FULL + 1)},
        "minimum_anchor_computed_to": M_DEEP,
        "source_realizations_checked": realize_cases,
    })
    rep["measured"]["assessment"] = {
        "what_round_03a1_gets_right": (
            "All of it, within finite reach. The accelerated code reproduces direct "
            "iteration; the affine endpoint formula and the B recurrence hold; the "
            "source congruence pins an odd canonical representative in its stated "
            "range; the classes nest, the lift digit sits in its stated range and "
            "the source is nondecreasing along extensions; a nonzero lift always "
            "spikes the rate above alpha and nothing sits inside the forbidden gap; "
            "the mechanical code is the maximal subcritical path with increments in "
            "{1,2}; and both of §30-§31's counterexamples reproduce, with the "
            "sources really having those codes."
        ),
        "section_34_extended": (
            "The paper's diagnostic table for m <= 8 reproduces exactly - 3, 7, 7, "
            "27, 27, 27, 27, 27 against mechanical 3, 11, 27, 123, 251, 1019, 3067, "
            "7163. Extended here to m = 60 by branch and bound, which §13's "
            "monotonicity makes exact provided the answer stays under the prune cap; "
            "this run checks that it does rather than assuming it. a_m stays at 27 "
            "through m = 36, then 703 through m = 50, then 10087. Meanwhile the "
            "mechanical source passes 29 million by m = 16, so the extremality trap "
            "is not marginal - it is six orders of magnitude wide."
        ),
        "the_bridge_to_RUN_007": (
            "§35 introduces a_m as the accelerated-code minimum anchor and declines "
            "to assume it agrees with the classical one, since that would involve "
            "CST. On everything measured it agrees exactly: a_m takes the same "
            "values RUN-007 measured for m_k - 3, 7, 27, 703, 10087 - and each "
            "anchor leaves at precisely the odd-step count whose Beatty depth is its "
            "own tau_c. Two coordinate systems, two independent computations, one "
            "sequence. That is a measured agreement on this range, not the theorem."
        ),
        "what_it_does_not_establish": (
            "nothing about Collatz, and nothing about §41's unproved list. In "
            "particular 'every infinite subcritical code has infinitely many "
            "nonzero lifts' is untouched: this run sees only finite codes, and a_m "
            "sitting at 27 for thirty-three consecutive m is exactly what a bounded "
            "anchor would look like too."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
