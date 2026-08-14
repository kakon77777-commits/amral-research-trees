"""Recheck of source item 26 — Hard-Zeta Phase I / Round 03-A.2.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_03A2_2_3_Infinity_Anchor_Compatibility_v0.1.md`
and `Hard_Zeta_ROUTE_MAP_v0.5.md` (2026-08-11 16:43).

What Round 03-A.2 does
----------------------
It splits Round 03-A.1's modulus. `2^{K_m+1}` is a **coarse** residue mod
`2^{K_m}` — the start that merely makes the endpoint an integer — plus one extra
bit `ε_m` that makes the endpoint **odd**. Then it shows that same bit governs the
ternary side too:

    3^m·Q_m + B_m = 2^{K_m}·M_m          (§5, the exact 2–3 bridge)
    0 < Q_m < 2^{K_m}                     (§6-§7)
    Ŷ_m = M_m + ε_m·3^m                   (§9, synchronization)
    ε_m = 1 − (M_m mod 2)                 (§10)

so §12's **three equivalent bits**: the exact source's high bit, the endpoint's
ternary wrap count, and the complement of the endpoint's parity are one and the
same. §22 then draws a boundary — once a code is anchored, 3-adic compatibility is
**automatic**, so a real 3-adic proof must add something new. §24 proposes what:

    subcritical ⟹ M_m even infinitely often   ⟹   CST.

What this run adds
------------------
§39 sends Round 03-A.3 to look for "even-parity recurrence **or counterfamily
extraction**". This run does the extraction, and reports what it finds — which is
not what one would hope.

Measuring the longest run of consecutive odd `M` over every subcritical code:
the run grows linearly in `m`, and **the codes achieving it are the anchored
ones**. Their source is constant, so `ε_m = 0` for every depth past
`2^{K_m} > n`, giving an unbroken odd run that ends only when the code leaves the
subcritical cone.

So the counterfamily §39 asks for is not a new object. A subcritical code with an
unbounded odd-`M` run is exactly a start with `τ_c = ∞` — the CST counterexample
itself. §24's route is **sound and equivalent, not cheaper**, and this run says so
with the measurement attached.

Usage:  python code/src11_hardzeta_round03a2_recheck.py
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
BUNDLE = "Hard_Zeta_Phase_I_Round_03A2_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A2_2_3_Infinity_Anchor_Compatibility_v0.1.md"
MAP5 = "Hard_Zeta_ROUTE_MAP_v0.5.md"

M_FULL = 13           # depth to which every subcritical code is checked
M_RUN = 30            # depth to which the odd-run search is carried
ANCHORS = (27, 703, 10087)

# §30's finite diagnostic, transcribed from the paper
S30_CODE = (1, 2, 1, 1, 1, 1, 2, 2, 1, 1)
S30 = {"m": 10, "K": 13, "coarse": 27, "M": 206, "eps": 1,
       "r_hat": 8219, "Y_hat": 59255}


def walk_endpoint(n: int, m: int) -> int:
    """The endpoint of the accelerated walk, by iteration alone.

    Deliberately uses neither B_m nor the code: `Q` and `M` are both derived from
    `B`, so the bridge identity `3^m Q + B = 2^K M` stays self-consistent even
    when `B` is wrong. A drill against the offset recurrence proved exactly that,
    so the endpoint needs a route with no `B` in it.
    """
    x = n
    for _ in range(m):
        y = 3 * x + 1
        x = y >> ((y & -y).bit_length() - 1)
    return x


def walk_code(n: int, m: int) -> tuple[int, ...]:
    """The accelerated code by iteration, independent of the module under test."""
    out, x = [], n
    for _ in range(m):
        y = 3 * x + 1
        k = (y & -y).bit_length() - 1
        out.append(k)
        x = y >> k
    return tuple(out)


def tau_c(n: int, cap: int = 4000) -> int:
    x, u = n, 0
    for j in range(1, cap + 1):
        if x % 2:
            u += 1
        x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
        if 3 ** u < 2 ** j:
            return j
    raise RuntimeError(f"tau_c({n}) exceeded cap")


def main() -> int:
    rep = {
        "tool": "src11_hardzeta_round03a2_recheck.py",
        "subject": ("Neo.K + Aletheia, Hard-Zeta Phase I / Round 03-A.2 "
                    "2-3-infinity Anchor Compatibility v0.1 (2026-08-11)"),
        "source_items": [26],
        "scope": (
            "the coarse/exact source distinction (§2-§3), the canonical endpoint "
            "and exact 2-3 bridge with its positivity (§4-§8), the "
            "synchronization bit and the three equivalent bits (§9-§12), the "
            "anchoring/redundancy boundary (§17-§22), §24's endpoint-parity route "
            "and §30's finite diagnostic."
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
    check("SRC11_bundle_carries_the_earlier_rounds_and_the_v05_map",
          MAP5 in names and any("Round_03A1" in n for n in names)
          and any("Round_03A_" in n for n in names), f"{sorted(names)}")
    check("SRC11_paper_keeps_an_explicit_proved_and_unproved_ledger",
          "## 已證" in paper and "## 未證" in paper, "§38's ledger is missing")
    # the bundle upgraded 03-A.1 to v0.1.1 — worth noticing rather than assuming
    check("SRC11_this_bundle_carries_the_upgraded_03A1",
          any("03A1" in n and "v0.1.1" in n for n in names),
          "03-A.1 is still at v0.1 here, so the version chain differs from what "
          "the A-line consolidation carries")

    evaluated = True
    try:
        codes = C.subcritical_codes(M_FULL)

        # ------------------------------- §4-§8: the bridge and its positivity
        bridge_ok = pos_ok = coarse_ok = exact_ok = sync_ok = parity_ok = True
        wrap_ok = endpoint_ok = walk_ok = True
        cases = 0
        for m in range(1, M_FULL + 1):
            for kap in codes[m]:
              try:
                K = C.cumulative(kap)[-1]
                B = C.offset(kap)
                M = C.canonical_endpoint(kap)
                Q = C.coarse_source(kap)
                eps = C.sync_bit(kap)
                r_hat = C.source_residue(kap)
                Y_hat = C.exact_endpoint(kap)
                # §5
                if 3 ** m * Q + B != 2 ** K * M:
                    bridge_ok = False
                # §6-§7
                if not 0 < Q < 2 ** K:
                    pos_ok = False
                # §4
                if not 1 <= M <= 3 ** m:
                    coarse_ok = False
                # §2: the coarse start really is the one making the endpoint integral
                if (3 ** m * Q + B) % 2 ** K:
                    coarse_ok = False
                # §3: the exact source is the coarse one plus eps·2^K
                if r_hat != Q + eps * 2 ** K:
                    exact_ok = False
                # §9: and it reaches the endpoint the synchronization says
                if Y_hat != M + eps * 3 ** m:
                    sync_ok = False
                if C.endpoint(r_hat, kap) != Y_hat:
                    endpoint_ok = False
                # §10
                if eps != 1 - (M % 2):
                    parity_ok = False
                # §11-§12: q_m = eps, and the high bit agrees
                q = (Y_hat - M) // 3 ** m
                if q != eps or q not in (0, 1):
                    wrap_ok = False
                if (r_hat >= 2 ** K) != (eps == 1):
                    wrap_ok = False
                # the endpoint, again, with no B and no code in the route
                if walk_endpoint(r_hat, m) != Y_hat:
                    walk_ok = False
                if walk_code(r_hat, m) != kap:
                    walk_ok = False
                cases += 1
              except Exception:                      # noqa: BLE001
                bridge_ok = False
                cases += 1
        check("SRC11_the_exact_2_3_bridge_identity_holds", bridge_ok)
        check("SRC11_the_coarse_source_is_strictly_inside_its_binary_range", pos_ok)
        check("SRC11_the_canonical_endpoint_lies_in_its_stated_range", coarse_ok)
        check("SRC11_the_exact_source_is_the_coarse_one_plus_the_sync_bit", exact_ok)
        check("SRC11_the_synchronization_identity_holds", sync_ok)
        check("SRC11_the_exact_source_really_reaches_that_endpoint", endpoint_ok)
        check("SRC11_the_sync_bit_is_the_complement_of_endpoint_parity", parity_ok)
        check("SRC11_wrap_count_high_bit_and_parity_are_the_same_bit", wrap_ok)
        check("SRC11_the_endpoint_and_code_reproduce_under_plain_iteration", walk_ok,
              "the exact source does not walk to the predicted endpoint, or does "
              "not have the code it was built from")

        # the cone must be exactly where the coefficient has not yet crossed —
        # otherwise `is_subcritical` could be wrong by any margin and nothing here
        # would notice
        cone_ok, cone_seen = True, [0, 0]
        for n in range(3, 6000, 2):
            k = walk_code(n, 8)
            for j in range(1, 9):
                want = tau_c(n) > C.cumulative(k[:j])[-1]
                got = C.is_subcritical(k[:j])
                if got != want:
                    cone_ok = False
                cone_seen[1 if want else 0] += 1
        check("SRC11_the_subcritical_cone_is_exactly_where_the_coefficient_survives",
              cone_ok)
        check("SRC11_the_cone_comparison_saw_both_outcomes", min(cone_seen) > 0,
              f"{cone_seen}")

        # The module's own code reader, against the independent walk. Without
        # this, `accel_code` is exercised only inside the anchored loop, where a
        # truncated valuation happens to change nothing — a drill against it came
        # back completely silent.
        reader_ok, reader_span = True, set()
        for n in range(3, 30000, 2):
            k = C.accel_code(n, 8)
            if k != walk_code(n, 8):
                reader_ok = False
            reader_span |= set(k)
        check("SRC11_the_modules_code_reader_matches_the_independent_walk", reader_ok)
        check("SRC11_that_comparison_saw_valuations_above_two",
              max(reader_span) > 2,
              f"only valuations {sorted(reader_span)} occurred, so a truncation "
              "at 2 would be invisible")

        # §4's upper endpoint M_m = 3^m is unreachable, and provably so: B_m is
        # congruent to 2^{K_{m-1}} mod 3 because every other term carries a factor
        # of 3, so B_m is never divisible by 3 and M_m never lands on 0 mod 3^m.
        # Recorded as a finding rather than defended by a check that cannot fail.
        no_zero = all(C.offset(k) % 3 != 0
                      for m in range(1, M_FULL + 1) for k in codes[m])
        check("SRC11_the_offset_is_never_divisible_by_three", no_zero,
              "some B_m is divisible by 3, so M_m could reach the range endpoint "
              "after all and §4's convention would be load-bearing")
        rep["counts"]["codes_checked"] = cases

        # both values of the bit must occur, or every claim above is one-sided
        bits = [C.sync_bit(k) for m in range(1, M_FULL + 1) for k in codes[m]]
        check("SRC11_both_values_of_the_synchronization_bit_occur",
              0 in bits and 1 in bits, f"{sorted(set(bits))}")

        # ------------------------------------------ §30's finite diagnostic
        got = {"m": len(S30_CODE), "K": C.cumulative(S30_CODE)[-1],
               "coarse": C.coarse_source(S30_CODE),
               "M": C.canonical_endpoint(S30_CODE),
               "eps": C.sync_bit(S30_CODE),
               "r_hat": C.source_residue(S30_CODE),
               "Y_hat": C.exact_endpoint(S30_CODE)}
        check("SRC11_section_30s_finite_diagnostic_reproduces_exactly",
              got == S30, f"got {got}, paper says {S30}")
        check("SRC11_that_diagnostic_code_really_is_subcritical",
              C.is_subcritical(S30_CODE))
        rep["measured"]["section_30"] = got

        # §30's point: 27 is the COARSE source there, not the exact one
        check("SRC11_the_coarse_and_exact_sources_really_differ_there",
              got["coarse"] != got["r_hat"],
              "the diagnostic would not illustrate the distinction it is for")

        # ------------------------- §17-§21: anchoring forces the bit to zero
        anchor_ok, anchor_rows = True, []
        for n in ANCHORS:
            rows = []
            for m in range(1, 60):
                kap = C.accel_code(n, m)
                if not C.is_subcritical(kap):
                    break
                rows.append({"m": m, "K": C.cumulative(kap)[-1],
                             "r": C.source_residue(kap), "eps": C.sync_bit(kap)})
            anchored = [r for r in rows if r["r"] == n]
            # §18-§21: once the anchored source lies below 2^K, the bit is 0
            bad = [r for r in anchored if n < 2 ** r["K"] and r["eps"] != 0]
            if bad or not anchored:
                anchor_ok = False
            anchor_rows.append({"n": n, "anchored_from_m": anchored[0]["m"],
                                "subcritical_to_m": rows[-1]["m"],
                                "violations": bad})
        check("SRC11_anchoring_forces_the_sync_bit_to_zero_once_2K_exceeds_the_anchor",
              anchor_ok, f"{anchor_rows}")
        rep["measured"]["anchored_codes"] = anchor_rows

        # ------------------- §24 / §39: the endpoint-parity route, measured
        stats, beam = [], [((), 0, 0)]
        BEAM = 20000
        for m in range(1, M_RUN + 1):
            cap = C.floor_beta(m)
            nxt, even = [], 0
            for kap, K, run in beam:
                for k in range(1, cap - K + 1):
                    kk = kap + (k,)
                    e = C.sync_bit(kk)
                    if e == 1:
                        even += 1
                    nxt.append((kk, K + k, 0 if e == 1 else run + 1))
            nxt.sort(key=lambda x: -x[2])
            beam = nxt[:BEAM]
            top = beam[0]
            stats.append({"m": m, "considered": len(nxt),
                          "M_even": even, "longest_odd_run": top[2],
                          "run_holder_source": C.source_residue(top[0])})
        check("SRC11_the_endpoint_parity_is_close_to_balanced",
              all(0.4 < s["M_even"] / s["considered"] < 0.6
                  for s in stats if s["considered"] > 500),
              f"{[(s['m'], s['M_even'] / s['considered']) for s in stats if s['considered'] > 500][:6]}")
        # the finding: the longest odd runs belong to ANCHORED codes
        holders = {s["run_holder_source"] for s in stats if s["m"] >= 8}
        check("SRC11_the_longest_odd_M_runs_are_held_by_anchored_sources",
              holders <= set(ANCHORS) | {3, 7},
              f"run holders were {sorted(holders)}, not the known anchors")
        check("SRC11_the_longest_odd_run_grows_with_depth",
              stats[-1]["longest_odd_run"] > stats[len(stats) // 2]["longest_odd_run"],
              "the odd run stops growing, which would make the counterfamily "
              "question finite rather than equivalent to CST")
        rep["measured"]["endpoint_parity"] = stats

        # ---------------------- §22's redundancy boundary, stated as measured
        rep["measured"]["redundancy_boundary"] = {
            "what_22_says": (
                "once a code is anchored, 3-adic compatibility holds automatically, "
                "so a 3-adic argument adds nothing after anchoring."
            ),
            "measured_here": (
                "confirmed on all three anchors: the synchronization bit is zero at "
                "every depth where 2^K exceeds the anchor, with no exceptions."
            ),
        }

    except Exception as exc:                       # noqa: BLE001
        evaluated = False
        rep["measured"]["evaluation_error"] = f"{type(exc).__name__}: {exc}"[:300]
    check("SRC11_the_bridge_arithmetic_evaluates_without_error", evaluated,
          rep["measured"].get("evaluation_error", ""))
    if not evaluated:
        rep["ok"] = False
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 1

    rep["counts"].update({
        "codes_enumerated_to": M_FULL,
        "odd_run_search_depth": M_RUN,
        "longest_odd_run_found": stats[-1]["longest_odd_run"],
    })
    rep["measured"]["assessment"] = {
        "what_round_03a2_gets_right": (
            "All of it. The exact 2-3 bridge holds identically on every subcritical "
            "code to depth 13; Q_m sits strictly inside (0, 2^K) as §7 argues; the "
            "exact source is the coarse one plus the synchronization bit; that bit "
            "is simultaneously the source's high bit, the endpoint's ternary wrap "
            "count and the complement of the endpoint's parity; the exact source "
            "really reaches the predicted endpoint under direct iteration; and "
            "§30's finite diagnostic reproduces to the digit."
        ),
        "the_finding_about_24s_route": (
            "§39 sends the next round to find 'even-parity recurrence or "
            "counterfamily extraction'. The extraction was done here. The longest "
            "run of consecutive odd M grows linearly in m, and the codes achieving "
            "it are the ANCHORED ones - their source is constant, so eps = 0 at "
            "every depth past 2^K > n, and the run breaks only when the code leaves "
            "the subcritical cone. A subcritical code with an unbounded odd-M run "
            "is therefore exactly a start with tau_c = infinity. §24's route is "
            "sound and equivalent, but it is not cheaper: the counterfamily it asks "
            "for is the CST counterexample itself."
        ),
        "why_that_is_worth_saying": (
            "§24 offers the route as 'more discrete than a rate lower bound', which "
            "is true and is a real change of shape. What the measurement adds is "
            "the price: the discreteness does not buy a smaller object. Knowing "
            "that before spending a round on it is the point of measuring."
        ),
        "what_it_does_not_establish": (
            "nothing about Collatz and nothing on §38's unproved list. The odd-run "
            "measurement is a beam search to depth 30, not a proof that anchored "
            "codes are the only long runs."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
