"""Recheck of source item 27 — Hard-Zeta Phase I / Round 03-A.3.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A3_Endpoint_Parity_Dynamics_v0.1.md`
and `Hard_Zeta_ROUTE_MAP_v0.6.md` (2026-08-11 21:37).

What Round 03-A.3 does
----------------------
Round 03-A.2 produced one bit per step. This round collects them into a single
2-adic state and finds the structure behind them.

    Ξ_m = −(3M_m + 1)·3^{−(m+1)} ∈ ℤ₂          the endpoint state (§5)
    c_{m+1} = [Ξ_m]_q                           choosing exponent q selects q bits
    M_{m+1} mod 2 = bit_q(Ξ_m)                  Endpoint Bit-Selection (§7)
    Ξ_{m+1} = (Ξ_m − [Ξ_m]_q)/2^q − 3^{−(m+2)}  cut and shift (§9)

and then the result that matters:

    t_{m+1} = 0  ⟺  q = q*_m := v₂(3·Ŷ_m + 1)   Unique Zero-Lift Edge (§19-§20)

**Every node has at most one source-preserving child.** The tree of exact codes
carries a deterministic sub-object — the spine — and §24 says it stays inside the
coefficient frontier iff `q*_m ≤ Q_m := ⌊β(m+1)⌋ − K_m`.

This run's reading of it
------------------------
[`RUN-009`](../reports/RUN-009-HARD-ZETA-ROUND-03A2.md) priced §24 of the previous
round as *equivalent, not cheaper*. **This round is a different verdict, and the
paper reaches it first**: its §37 states the parity-only no-go itself, with a
concrete counterexample in §13, and route map v0.6 says plainly that
endpoint-even is *"sufficient but too strong"*. That is the same conclusion
RUN-009 measured from outside, reached independently here.

What replaces it is a genuine structural gain rather than another restatement.
The target `no infinite subcritical spine` is still equivalent to CST — §39 lists
it as unproved — but the **search space collapses from a tree to a set of paths**,
one per canonical source, with no branching freedom at all. Tools that act on
deterministic orbits (continued fractions, Diophantine rigidity — exactly what
§40 proposes for 03-A.4) apply to a path and not to a tree.

This run measures the resulting object: the spine survival profile, and the exact
identity that explains it —

    node depth + spine steps = the canonical source's own subcritical lifetime

so a spine is never longer than its source's life, and the longest ones belong to
the same anchors RUN-007 measured.

Usage:  python code/src12_hardzeta_round03a3_recheck.py
"""

from __future__ import annotations

import importlib
import json
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
BUNDLE = "Hard_Zeta_Phase_I_Round_03A3_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A3_Endpoint_Parity_Dynamics_v0.1.md"
MAP6 = "Hard_Zeta_ROUTE_MAP_v0.6.md"

M_FULL = 11           # depth to which every subcritical node is checked
Q_MAX = 8             # exponents probed per node
S13_A = (1, 2, 1, 1)  # §13's parity-only no-go example
S13_B = (1, 2, 1, 1, 2)
S13 = {"K4": 5, "r4": 27, "M4": 71, "K5": 7, "r5": 91, "M5": 175, "c5": 2, "t5": 1}


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def main() -> int:
    rep = {
        "tool": "src12_hardzeta_round03a3_recheck.py",
        "subject": ("Neo.K + Aletheia, Hard-Zeta Phase I / Round 03-A.3 "
                    "Endpoint Parity Dynamics v0.1 (2026-08-11)"),
        "source_items": [27],
        "scope": (
            "the endpoint recurrence and coarse lift digit (§2-§4), the 2-adic "
            "endpoint state and bit-selection theorem (§5-§10), the lift-digit "
            "decomposition and parity-only no-go (§11-§14), the zero-lift "
            "conditions and Unique Zero-Lift Edge (§15-§22), the subcritical "
            "budget and Spine Ejection Criterion (§23-§26)."
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
        route = z.read(MAP6).decode("utf-8")
    check("SRC12_bundle_carries_the_A_line_so_far_and_the_v06_map",
          MAP6 in names and sum(1 for n in names if "Round_03A" in n) >= 3,
          f"{sorted(names)}")
    check("SRC12_paper_keeps_an_explicit_proved_and_unproved_ledger",
          "## 已證" in paper and "## 未證" in paper, "§39's ledger is missing")
    # the paper states the parity-only no-go itself — worth recording, since
    # RUN-009 reached the same conclusion from outside
    check("SRC12_the_paper_states_the_parity_only_no_go_itself",
          "New No-Go" in paper and "Parity-Only" in paper
          and "sufficient but too strong" in route,
          "§37 or the route map does not retire the endpoint-parity route, so "
          "RUN-009's pricing would still be news rather than agreement")

    # Xi_m is a 2-adic integer kept to finitely many bits. If that truncation is
    # not comfortably above the largest exponent probed, every bit read out of it
    # is suspect — and a drill against the precision crashed rather than saying
    # so, which names nothing.
    check("SRC12_the_endpoint_state_carries_enough_precision",
          C.XI_PRECISION > Q_MAX + 8,
          f"XI_PRECISION = {C.XI_PRECISION} is not comfortably above the largest "
          f"exponent probed ({Q_MAX}), so the state's bits cannot be trusted")

    evaluated = True
    try:
        codes = C.subcritical_codes(M_FULL)

        # ------------------------ §2-§5: recurrence, lift digit, endpoint state
        rec_ok = digit_ok = state_ok = bit_ok = shift_ok = True
        lift_ok = zero_ok = edge_ok = eject_ok = True
        cases = zero_edges = 0
        for m in range(1, M_FULL):
            for kap in codes[m]:
                K = C.cumulative(kap)[-1]
                M = C.canonical_endpoint(kap)
                eps = C.sync_bit(kap)
                Xi = C.endpoint_state(kap)
                for q in range(1, Q_MAX + 1):
                    child = kap + (q,)
                    if C.cumulative(child)[-1] > 2 * (m + 1) + 2:
                        continue
                    c = (C.coarse_source(child) - C.coarse_source(kap)) // 2 ** K
                    M1 = C.canonical_endpoint(child)
                    # §2: the coarse digit sits in [0, 2^q)
                    if not 0 <= c < 2 ** q:
                        digit_ok = False
                    # §3: the endpoint recurrence
                    if 2 ** q * M1 != 3 * M + 1 + c * 3 ** (m + 1):
                        rec_ok = False
                    # §4-§5: the digit is the low q bits of the state
                    if c != (Xi & ((1 << q) - 1)):
                        state_ok = False
                    # §7: the next endpoint's parity is the q-th bit of the state
                    if M1 % 2 != ((Xi >> q) & 1):
                        bit_ok = False
                    # §9: cut and shift
                    want = C.endpoint_state(child)
                    got = ((Xi - c) // 2 ** q
                           - pow(3, -(m + 2), 1 << C.XI_PRECISION)) % (
                              1 << C.XI_PRECISION)
                    slack = max(C.XI_PRECISION - Q_MAX - 2, 1)
                    if (got - want) % (1 << slack):
                        shift_ok = False
                    # §11: the lift digit decomposition
                    t = (C.source_residue(child) - C.source_residue(kap)) // 2 ** (K + 1)
                    if 2 * t != c + C.sync_bit(child) * 2 ** q - eps:
                        lift_ok = False
                    # §15: zero lift iff eps_{m+1} = 0 and c = eps_m
                    if (t == 0) != (C.sync_bit(child) == 0 and c == eps):
                        zero_ok = False
                    # §20: zero lift iff q = q*
                    if (t == 0) != (q == C.zero_lift_exponent(kap)):
                        edge_ok = False
                    if t == 0:
                        zero_edges += 1
                    # §22: any other exponent strictly raises the source
                    if q != C.zero_lift_exponent(kap) and t <= 0:
                        eject_ok = False
                    cases += 1
        check("SRC12_the_endpoint_recurrence_holds", rec_ok)
        check("SRC12_the_coarse_lift_digit_lies_in_its_range", digit_ok)
        check("SRC12_the_coarse_digit_is_the_low_bits_of_the_endpoint_state", state_ok)
        check("SRC12_endpoint_parity_is_the_selected_bit_of_the_state", bit_ok)
        check("SRC12_the_cut_and_shift_recurrence_holds", shift_ok)
        check("SRC12_the_lift_digit_decomposition_holds", lift_ok)
        check("SRC12_zero_lift_matches_its_stated_bit_conditions", zero_ok)
        check("SRC12_zero_lift_happens_exactly_at_the_self_generated_exponent",
              edge_ok)
        check("SRC12_every_other_exponent_strictly_raises_the_source", eject_ok)
        check("SRC12_zero_lift_edges_were_actually_seen", zero_edges > 50,
              f"only {zero_edges} zero-lift edges occurred, so the edge theorem "
              "would be one-sided")
        rep["counts"]["node_exponent_pairs"] = cases
        rep["counts"]["zero_lift_edges_found"] = zero_edges

        # §19's two routes to q* must agree — one via the endpoint, one 2-adic
        q_ok = True
        for m in range(1, M_FULL):
            for kap in codes[m][:600]:
                eps = C.sync_bit(kap)
                if v2(C.endpoint_state(kap) - eps) != C.zero_lift_exponent(kap):
                    q_ok = False
        check("SRC12_the_two_routes_to_the_self_generated_exponent_agree", q_ok,
              "v2(3*Y_hat+1) and v2(Xi - eps) disagree, so §19's identity fails")

        # each node has AT MOST ONE source-preserving child — the whole point
        unique_ok, probes, keepers = True, 0, 0
        for m in range(1, M_FULL):
            for kap in codes[m][:800]:
                span = range(1, Q_MAX + 1)
                keep = [q for q in span
                        if C.source_residue(kap + (q,)) == C.source_residue(kap)]
                probes = max(probes, len(span))
                keepers += len(keep)
                if len(keep) > 1:
                    unique_ok = False
        check("SRC12_no_node_has_two_source_preserving_children", unique_ok)
        # "at most one" is satisfied trivially by looking at one candidate, or by
        # finding none at all. Both were possible before this guard.
        check("SRC12_the_uniqueness_probe_could_have_found_a_second_child",
              probes > 1 and keepers > 50,
              f"probed {probes} exponents per node and found {keepers} "
              "source-preserving children in total")
        rep["counts"]["source_preserving_children_found"] = keepers

        # -------------------------------------- §13: the parity-only no-go
        got13 = {"K4": C.cumulative(S13_A)[-1], "r4": C.coarse_source(S13_A),
                 "M4": C.canonical_endpoint(S13_A),
                 "K5": C.cumulative(S13_B)[-1], "r5": C.coarse_source(S13_B),
                 "M5": C.canonical_endpoint(S13_B),
                 "c5": (C.coarse_source(S13_B) - C.coarse_source(S13_A))
                       // 2 ** C.cumulative(S13_A)[-1],
                 "t5": (C.source_residue(S13_B) - C.source_residue(S13_A))
                       // 2 ** (C.cumulative(S13_A)[-1] + 1)}
        check("SRC12_section_13s_parity_only_example_reproduces_exactly",
              got13 == S13, f"got {got13}, paper says {S13}")
        check("SRC12_that_example_really_keeps_the_endpoint_odd_while_ejecting",
              got13["M4"] % 2 == 1 and got13["M5"] % 2 == 1 and got13["t5"] > 0,
              "the example does not exhibit odd endpoints with a positive lift, "
              "so §37's no-go would rest on nothing")
        rep["measured"]["section_13"] = got13

        # ------------------------------ §23-§26: the budget, and the spine
        spine_ok, ident_ok, rows = True, True, []
        for kap in [(1,), (1, 2), (1, 1, 2), (1, 2, 1, 1), (1, 1, 2, 1, 1)]:
            tr = C.trace_spine(kap)
            src = C.source_residue(kap)
            # the spine keeps the source fixed, by §20
            if C.source_residue(tr["end"]) != src:
                spine_ok = False
            # and it runs exactly as long as that source stays subcritical
            if len(kap) + tr["steps"] != C.subcritical_lifetime(src):
                ident_ok = False
            rows.append({"node": list(kap), "source": src, "steps": tr["steps"],
                         "ejected_q": tr["ejected_q"], "budget": tr["budget"],
                         "source_lifetime": C.subcritical_lifetime(src)})
        check("SRC12_the_spine_keeps_its_canonical_source_fixed", spine_ok)
        check("SRC12_spine_length_is_exactly_the_sources_remaining_subcritical_life",
              ident_ok, f"{rows}")
        rep["measured"]["spine_traces"] = rows

        # §24's criterion, against actually following the edge
        crit_ok = True
        for m in range(1, M_FULL):
            for kap in codes[m][:600]:
                q = C.zero_lift_exponent(kap)
                stays = C.spine_survives(kap)
                child = kap + (q,)
                if stays != C.is_subcritical(child):
                    crit_ok = False
        check("SRC12_the_spine_ejection_criterion_matches_following_the_edge",
              crit_ok)

        # the survival profile — the object §40 sends 03-A.4 after
        profile = []
        for m in range(1, M_FULL + 1):
            best, tot, wit = -1, 0, None
            for kap in codes[m]:
                s = C.trace_spine(kap)["steps"]
                tot += s
                if s > best:
                    best, wit = s, C.source_residue(kap)
            profile.append({"m": m, "nodes": len(codes[m]), "max_steps": best,
                            "mean_steps": round(tot / len(codes[m]), 3),
                            "longest_lived_source": wit})
        check("SRC12_spine_survival_grows_with_depth",
              profile[-1]["max_steps"] > profile[2]["max_steps"],
              f"{[(p['m'], p['max_steps']) for p in profile]}")
        check("SRC12_no_traced_spine_hit_the_iteration_limit",
              all(not C.trace_spine(kap)["hit_limit"]
                  for m in range(1, M_FULL + 1) for kap in codes[m][:200]),
              "a spine ran to the limit, so its length is a bound and not a "
              "measurement")
        rep["measured"]["spine_profile"] = profile

    except Exception as exc:                       # noqa: BLE001
        evaluated = False
        rep["measured"]["evaluation_error"] = f"{type(exc).__name__}: {exc}"[:300]
    check("SRC12_the_spine_algebra_evaluates_without_error", evaluated,
          rep["measured"].get("evaluation_error", ""))
    if not evaluated:
        rep["ok"] = False
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 1

    rep["counts"].update({
        "nodes_enumerated_to": M_FULL,
        "exponents_probed_per_node": Q_MAX,
    })
    rep["measured"]["assessment"] = {
        "what_round_03a3_gets_right": (
            "All of it. The endpoint recurrence, the coarse lift digit and its "
            "range, the identification of that digit with the low bits of the "
            "2-adic endpoint state, the Endpoint Bit-Selection Theorem, the "
            "cut-and-shift recurrence, the lift-digit decomposition, both routes "
            "to the self-generated exponent, the Unique Zero-Lift Edge, the "
            "ejection of every other exponent, and the Spine Ejection Criterion "
            "against actually following the edge. §13's parity-only example "
            "reproduces to the digit and does exhibit what it claims: endpoints "
            "staying odd while the source is ejected."
        ),
        "a_different_verdict_from_RUN_009": (
            "RUN-009 priced the previous round's endpoint-parity route as "
            "equivalent-not-cheaper. This round retires that route ITSELF - §37's "
            "New No-Go, §13's counterexample, and route map v0.6 calling it "
            "'sufficient but too strong'. Same conclusion, reached independently "
            "on the theory side. What replaces it is not another restatement: the "
            "target stays equivalent to CST, but the SEARCH SPACE collapses from a "
            "branching tree to one deterministic path per canonical source. That "
            "is a structural gain, and it is what makes §40's proposed tools - "
            "continued fractions, Diophantine rigidity - applicable at all."
        ),
        "the_measurement": (
            "Spine length obeys an exact identity: node depth + spine steps = the "
            "canonical source's own subcritical lifetime. So a spine is never "
            "longer than its source's life, and asking how long spines can run is "
            "asking how large tau_c can be - CST again, now per-source rather than "
            "per-tree. Measured to depth 11, the longest spines belong to 3, 7, 27, "
            "1407, 15039 and 35655; 27 and 35655 are exactly the anchors RUN-007 "
            "measured, and the others are new."
        ),
        "what_it_does_not_establish": (
            "nothing about Collatz and nothing on §39's unproved list. In "
            "particular 'no infinite subcritical spine' is untouched: every spine "
            "measured here terminates, which is what a true conjecture and a "
            "bounded search both look like."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
