"""Recheck of source item 35 — Phase II / Round A-U.2b.2, Queue-Entropy Barrier.

數學戰士「墜衡」 / AMRAL Research Lab.

A-U.2b.1 §28 listed five levers that could beat its constant. This round pulls
the first — **queue entropy** — and the result is one negative and one positive:

  Prefix-Constraint First-Order No-Gain   all-prefix queue legality does not
                                          change H(gamma + x), so c_pack stands
  Second-Order Packing Barrier            the Stirling prefactor does buy a
                                          second-order term, d_pack = 1/(2 h*)

The subject ships an exact deficit-corridor dynamic program and a table of its
output. That table is the strongest thing here to check, so it is checked by a
**reimplemented DP** — accumulating from the low end via prefix sums where the
subject accumulates from the high end via suffix sums, with credits taken from
exact integer `floor_beta` where the subject multiplies a float — and the
reimplementation is itself validated against brute-force enumeration first.

Usage:  python code/src19_hardzeta_au2b2_recheck.py
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
from decimal import Decimal, getcontext

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))

A = importlib.import_module(os.environ.get("HZ_ACCEL_MODULE", "hz_accel_code"))

BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b2_bundle.zip"
AU2B2 = "Hard_Zeta_Phase_II_Round_AU2b2_Queue_Entropy_Second_Order_Barrier_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.3_AU2b2.md"
CONSTANTS = "Hard_Zeta_AU2b2_constants_and_queue.json"
SCRIPT = "verify_Hard_Zeta_AU2b2_queue_second_order.py"
PRED = "Hard_Zeta_Phase_II_Round_AU2b1_Sharp_Packing_Entropy_Threshold_v0.1.md"

DIGITS = 60
getcontext().prec = DIGITS + 30
LN2 = Decimal(2).ln()
BETA_D = Decimal(3).ln() / LN2
GAMMA_D = BETA_D - 1


def read_sources() -> dict[str, bytes]:
    out = {}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                out[pathlib.PurePosixPath(n).name] = z.read(n)
    return out


def main() -> int:
    rep = {
        "tool": "src19_hardzeta_au2b2_recheck.py",
        "subject": "Hard_Zeta_Phase_II_Round_AU2b2_bundle.zip (item 35) — Round "
                   "A-U.2b.2, its queue-DP script and constants JSON, three "
                   "figures, plus A_Line_ROUTE_MAP v1.3",
        "source_items": [35],
        "scope": "the exact queue dynamic program and its entropy saturation, "
                 "the second-order constant from the Stirling prefactor, the "
                 "block-scale optimality that makes it maximal, and the bundled "
                 "numerical artifact",
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
    au2b2 = raw.get(AU2B2, b"").decode("utf-8")
    routemap = raw.get(ROUTEMAP, b"").decode("utf-8")
    script = raw.get(SCRIPT, b"").decode("utf-8")
    consts = json.loads(raw.get(CONSTANTS, b"{}").decode("utf-8"))

    # ------------------------------------------------ §3: the credit word
    def credits_are_bits():
        bad, ones, zeros = [], 0, 0
        for phase in (0, 1, 5, 17):
            for j in range(1, 400):
                b = A.phase_credit(j, phase)
                if b not in (0, 1):
                    bad.append((phase, j, b))
                ones += b == 1
                zeros += b == 0
        return (not bad and ones > 0 and zeros > 0), {
            "violations": bad[:5], "ones": ones, "zeros": zeros,
            "_both_symbols_seen": ones > 0 and zeros > 0}

    check("SRC19_the_phase_resolved_credit_is_always_a_single_bit",
          credits_are_bits, "§3: b_j in {0,1} for every phase and index")

    def credit_prefix_tracks_gamma():
        # §3: |B_s - gamma s| < 1
        bad = []
        g = float(GAMMA_D)
        for phase in (0, 3, 11):
            B = 0
            for s in range(1, 600):
                B += A.phase_credit(s, phase)
                if not abs(B - g * s) < 1:
                    bad.append((phase, s, B, g * s))
        return not bad, {"violations": bad[:5]}

    check("SRC19_the_credit_prefix_stays_within_one_of_gamma_s",
          credit_prefix_tracks_gamma, "§3: |B_s - gamma s| < 1")

    def float_floor_matches_exact():
        # the subject's script computes floor(gamma*j) with a FLOAT gamma; this
        # arm uses exact integer arithmetic. Over the range the script uses they
        # must agree, or its whole table is built on a different credit word.
        g = float(GAMMA_D)
        bad = [j for j in range(1, 20001)
               if math.floor(g * j) != A.floor_beta(j) - j]
        measured["float_floor_agreement"] = {"j_range": 20000,
                                             "disagreements": len(bad)}
        return not bad, {"j_range": "1..20000", "disagreements": bad[:5]}

    check("SRC19_the_subjects_float_floor_agrees_with_exact_arithmetic",
          float_floor_matches_exact,
          "the script's credits come from math.floor(gamma*j) on a float; this "
          "would silently change the credit word if it ever slipped")

    # ------------------------------------ §4, §30: the queue dynamic program
    def dp_matches_bruteforce():
        bad = []
        for r, D in ((3, 1), (4, 2), (5, 1), (6, 2), (7, 3), (8, 2), (9, 1)):
            if A.queue_count(r, D) != A.queue_count_bruteforce(r, D):
                bad.append((r, D, A.queue_count(r, D),
                            A.queue_count_bruteforce(r, D)))
        return not bad, {"shapes": 7, "violations": bad}

    check("SRC19_the_queue_dp_matches_a_direct_enumeration", dp_matches_bruteforce,
          "§30: the DP is validated before it is used to grade anything")

    def dp_reproduces_the_table():
        bad, rows = [], []
        beta_f = float(BETA_D)
        for row in consts.get("queue_dp", []):
            r, D = row["r"], row["D"]
            count = A.queue_count(r, D)
            lg = math.log2(count)
            rate = lg / r
            gap = beta_f * r - lg - 0.5 * math.log2(r)
            drate = abs(rate - row["rate"])
            dgap = abs(gap - row["centered_gap"])
            rows.append({"r": r, "D": D, "rate": rate, "their_rate": row["rate"],
                         "gap": gap, "their_gap": row["centered_gap"]})
            if drate > 1e-12 or dgap > 1e-9:
                bad.append((r, drate, dgap))
        measured["queue_table"] = rows
        return (not bad and len(rows) > 4), {"rows_checked": len(rows),
                                             "violations": bad[:5]}

    check("SRC19_every_published_queue_row_reproduces_under_an_independent_dp",
          dp_reproduces_the_table,
          "§31: the shipped table, recomputed by a DP that accumulates from the "
          "other end and takes its credits from exact integers")

    def D_follows_the_stated_rule():
        # each row's D must be floor(x_star * r); a row with a different D would
        # be measuring a different corridor
        x = float(A.entropy_root(DIGITS) - GAMMA_D)
        bad = [(row["r"], row["D"], math.floor(x * row["r"]))
               for row in consts.get("queue_dp", [])
               if row["D"] != math.floor(x * row["r"])]
        return not bad, {"violations": bad}

    check("SRC19_each_published_row_uses_the_corridor_its_length_implies",
          D_follows_the_stated_rule, "D = floor(x* r) for every row")

    # -------------------------------------- §5, §11-§12: entropy saturation
    def excess_identity():
        # §5: E_r = B_r + d_0 - d_r, so E_r <= gamma r + D + O(1)
        bad, tested = [], 0
        for phase in (0, 4):
            for r in (10, 25, 60):
                for D in (2, 5):
                    B = sum(A.phase_credit(j, phase) for j in range(1, r + 1))
                    # walk one admissible path explicitly and check the identity
                    d = D
                    E = 0
                    for j in range(1, r + 1):
                        b = A.phase_credit(j, phase)
                        e = min(d + b, 1)
                        d = d + b - e
                        E += e
                    tested += 1
                    if E != B + D - d:
                        bad.append((phase, r, D, E, B + D - d))
        return (not bad and tested > 0), {"paths": tested, "violations": bad[:5]}

    check("SRC19_the_block_excess_equals_the_credit_prefix_plus_the_queue_drop",
          excess_identity, "§5: E_r = B_r + d_0 - d_r")

    def entropy_saturates():
        # §11: the rate rises toward H(gamma + x) = beta when x = x*. Checked as
        # a monotone approach with a shrinking gap, not as an attained limit.
        rows = measured.get("queue_table", [])
        if len(rows) < 5:
            return False, {"reason": "table not computed"}
        beta_f = float(BETA_D)
        gaps = [beta_f - r["rate"] for r in rows]
        shrinking = all(gaps[i + 1] < gaps[i] for i in range(len(gaps) - 1))
        measured["entropy_saturation"] = {
            "beta": beta_f, "rate_at_smallest_r": rows[0]["rate"],
            "rate_at_largest_r": rows[-1]["rate"],
            "gap_at_largest_r": gaps[-1],
            "monotone_approach": shrinking}
        return (shrinking and gaps[-1] < 0.01 and gaps[0] > 0.1), {
            "first_gap": gaps[0], "last_gap": gaps[-1], "monotone": shrinking}

    check("SRC19_the_queue_entropy_rate_climbs_toward_beta", entropy_saturates,
          "§11: with D/r -> x*, the rate tends to H(gamma+x*) = beta, so the "
          "queue constraint costs nothing at first order")

    def composition_ratios():
        # §13-§14: C_{E-1}/C_E = E/(r+E-1) and W_{E-1}/W_E = 2E/(r+E-1), both
        # below 1 in the relevant range, so each sum is controlled by its endpoint
        from math import comb
        bad = []
        for r in (50, 200, 1000):
            for E in (int(0.6 * r), int(0.64 * r)):
                lhs = comb(r + E - 2, E - 1) / comb(r + E - 1, E)
                if abs(lhs - E / (r + E - 1)) > 1e-12:
                    bad.append(("C", r, E))
                if not (E / (r + E - 1) < 1 and 2 * E / (r + E - 1) < 1):
                    bad.append(("not below one", r, E))
        return not bad, {"shapes": 6, "violations": bad}

    check("SRC19_the_composition_ratios_are_below_one_in_the_relevant_range",
          composition_ratios,
          "§13-§14: the adjacent-term ratios, so both packing sums are controlled "
          "by their endpoint term")

    # ------------------------------- §17-§18, §26: the second-order constant
    def second_order_constants():
        h = A.entropy_derivative_at_root(DIGITS)
        d = A.second_order_constant(DIGITS)
        margin = Decimal("0.5") - h * Decimal("0.36")
        agree, bad = {}, []
        for key, mine in (("H_prime_z_star", h), ("d_pack", d),
                          ("safe_margin_half_minus_Hprime_d", margin),
                          ("c_pack", A.packing_constant(DIGITS)),
                          ("z_star", A.entropy_root(DIGITS))):
            theirs = consts.get(key, "")
            a = str(+mine)
            n = 0
            while n < min(len(a), len(theirs)) and a[n] == theirs[n]:
                n += 1
            agree[key] = n
            if n < 50:
                bad.append((key, a[:30], theirs[:30]))
        measured["constants"] = {"digits_agreeing": agree,
                                 "d_pack": str(+d)[:32],
                                 "h_star": str(+h)[:32]}
        return (not bad and min(agree.values()) >= 50), {
            "digits_agreeing": agree, "mismatched": bad}

    check("SRC19_the_second_order_constants_reproduce_independently",
          second_order_constants,
          "§17-§18: h* = log2(1+1/z*) and d_pack = 1/(2h*), recomputed here")

    def safe_constant_is_admissible():
        # "0.36 clears the criterion" is satisfied MORE easily by a larger d_pack,
        # so on its own it survives a completely wrong root — a flipped bisection
        # lands on z = 1, giving h = 1 and d = 0.5, and 0.36 still clears. The
        # check therefore pins the root as well: z* must actually solve H(z) = beta.
        h = A.entropy_derivative_at_root(DIGITS)
        d = A.second_order_constant(DIGITS)
        z = A.entropy_root(DIGITS)
        root_holds = abs(A.packing_entropy(z) - BETA_D) < Decimal(1) / Decimal(10 ** 40)
        safe = Decimal(consts["safe_second_order_constant"])
        return (root_holds and h * safe < Decimal("0.5") and safe < d), {
            "h_times_safe": str(h * safe)[:20], "d_pack": str(+d)[:20],
            "safe": str(safe), "root_solves_H_equals_beta": bool(root_holds)}

    check("SRC19_the_safe_second_order_constant_clears_its_criterion",
          safe_constant_is_admissible,
          "§19, §24: the contradiction needs h* d < 1/2, and 0.36 must be below "
          "d_pack")

    def block_scale_optimum():
        # §26: scan s; the admissible d is min over the two exponents, and its
        # maximum must sit at s = 0 with value d_pack.
        best, best_s = Decimal(-1), None
        s = Decimal("-0.5")
        step = Decimal("0.002")
        while s <= Decimal("0.5"):
            lo, hi = Decimal(0), Decimal(2)
            for _ in range(60):
                mid = (lo + hi) / 2
                p1, p2 = A.block_scale_exponents(mid, s, DIGITS)
                if p1 < 0 and p2 < 0:
                    lo = mid
                else:
                    hi = mid
            if lo > best:
                best, best_s = lo, s
            s += step
        d = A.second_order_constant(DIGITS)
        measured["block_scale"] = {"best_d": float(best), "at_s": float(best_s),
                                   "d_pack": float(d),
                                   "reading": ("s = 0 is optimal, so d_pack is the "
                                               "ceiling of this envelope too — the "
                                               "third consecutive round published "
                                               "at its own supremum")}
        return (abs(best_s) <= step and abs(best - d) < Decimal("0.001")), {
            "best_d": str(+best)[:20], "at_s": str(+best_s),
            "d_pack": str(+d)[:20]}

    check("SRC19_the_block_scale_optimum_sits_at_the_published_constant",
          block_scale_optimum,
          "§26: maximising d over the block scale s, subject to both exponents "
          "being negative")

    def both_exponents_bite():
        # the optimum is a corner between two constraints; each must be the
        # binding one somewhere, or the "optimum" is one-sided
        d = A.second_order_constant(DIGITS)
        # STRICTLY positive: at d = d_pack the undamaged exponents are exactly
        # zero at s = 0, so a defect that deletes the s-dependence leaves them at
        # zero and a `>= 0` test passes for the wrong reason.
        p1_pos = A.block_scale_exponents(d, Decimal("0.05"), DIGITS)[0] > 0
        p2_pos = A.block_scale_exponents(d, Decimal("-0.05"), DIGITS)[1] > 0
        return (p1_pos and p2_pos), {
            "first_exponent_fails_above_s_zero": p1_pos,
            "second_exponent_fails_below_s_zero": p2_pos}

    check("SRC19_each_block_scale_exponent_binds_on_its_own_side",
          both_exponents_bite,
          "§26: moving s either way breaks one of the two, which is what makes "
          "s = 0 a genuine corner rather than an arbitrary choice")

    # ------------------------------------------------ artifact provenance
    def json_is_consistent_with_its_script():
        # The shipped script emits rows for a fixed list of r and names its
        # fields one way; the shipped JSON has a different row set and different
        # names. That is recorded as a finding. What is CHECKED is that nothing
        # in the JSON contradicts the script: every r the script would emit
        # appears in the JSON, and every such row reproduces under this arm's DP.
        script_rs = []
        for line in script.splitlines():
            if "for r in [" in line:
                script_rs = [int(x) for x in
                             line.split("[", 1)[1].split("]", 1)[0].split(",")]
        json_rs = [row["r"] for row in consts.get("queue_dp", [])]
        script_keys = {"log2_count_over_r", "beta_minus_rate", "centered_gap"}
        json_keys = set(consts["queue_dp"][0]) if consts.get("queue_dp") else set()
        measured["artifact_pairing"] = {
            "script_row_count": len(script_rs), "json_row_count": len(json_rs),
            "rows_only_in_json": sorted(set(json_rs) - set(script_rs)),
            "script_row_keys": sorted(script_keys),
            "json_row_keys": sorted(json_keys),
            "finding": ("the shipped JSON was not produced by the shipped script "
                        "revision: it carries an extra row, renames "
                        "log2_count_over_r to rate, and drops beta_minus_rate. "
                        "Every value in it is nevertheless correct under an "
                        "independent DP, so this is a stale generator/output "
                        "pairing, not a wrong number.")}
        subset = set(script_rs) <= set(json_rs)
        return (bool(script_rs) and subset), {
            "script_rows": script_rs, "json_rows": json_rs,
            "script_rows_all_present_in_json": subset}

    check("SRC19_the_json_covers_everything_the_script_would_emit",
          json_is_consistent_with_its_script,
          "the artifact pairing is stale — recorded in `measured` — but the JSON "
          "must at least not contradict its generator")

    # ------------------------------------------------- ledger and bundle
    def unproved_list():
        tail = au2b2[au2b2.find("## 未證"):] if "## 未證" in au2b2 else ""
        want = ["CASP", "Terras", "Collatz"]
        missing = [w for w in want if w not in tail]
        return (bool(tail) and not missing), {"missing": missing}

    check("SRC19_the_paper_lists_casp_terras_and_collatz_as_unproved",
          unproved_list, "§34")

    check("SRC19_the_route_map_carries_both_constants",
          lambda: (("0.03585676003404866" in routemap
                    and "0.3689789787331466" in routemap
                    and "0.36" in routemap),
                   {"routemap_len": len(routemap)}),
          "v1.3 must publish the first-order and second-order constants together")

    check("SRC19_the_paper_records_the_first_order_no_gain",
          lambda: (("First-Order No-Gain" in au2b2
                    and "does not improve the first-order packing constant"
                    in routemap),
                   {}),
          "§12: the negative half must be stated as plainly as the positive half")

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
        for pat in ("Hard_Zeta_Phase_II_Round_AU1_bundle.zip",
                    "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip",
                    "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip",
                    "Hard_Zeta_Phase_II_Round_AU2b1_bundle.zip"):
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
        return (not edited and len(same) == 4 and len(fresh) == 7), {
            "reshipped_identical": len(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh)}

    check("SRC19_the_bundle_reships_its_predecessors_unedited", bundle_faithful,
          "four predecessor rounds byte-identical; SEVEN files new — the paper, "
          "the route map, the script, the constants JSON and three figures")

    # ------------------------------------------------------ own measurement
    def which_lever_was_pulled():
        # A-U.2b.1 §28 named five levers. This records which one this round used
        # and what it bought, against the previous round's own numbers.
        d = A.second_order_constant(DIGITS)
        c = A.packing_constant(DIGITS)
        rows = measured.get("queue_table", [])
        measured["lever"] = {
            "lever_used": "queue entropy (§28 item 1)",
            "first_order_gain": 0.0,
            "c_pack_unchanged": str(+c)[:20],
            "second_order_gain_d_pack": float(d),
            "queue_rate_at_r_5000": rows[-1]["rate"] if rows else None,
            "beta": float(BETA_D),
            "reading": ("the lever produced NO first-order gain — that is the "
                        "round's own Prefix-Constraint No-Gain theorem — and the "
                        "second-order term came from the Stirling prefactor "
                        "instead, which was not on the list of five. Four levers "
                        "remain untried.")}
        return (rows and abs(rows[-1]["rate"] - float(BETA_D)) < 0.01
                and d > Decimal("0.36")), {
            "c_pack_unchanged": True, "d_pack": float(d)}

    check("SRC19_the_queue_lever_gave_no_first_order_gain",
          which_lever_was_pulled,
          "measurement: which of A-U.2b.1's five levers this round used, and "
          "what it actually bought")

    rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
    rep["counts"] = {"checks": len(checks),
                     "passed": sum(1 for v in checks.values() if v["pass"]),
                     "digits": DIGITS}
    rep["ok"] = not rep["failures"]
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
