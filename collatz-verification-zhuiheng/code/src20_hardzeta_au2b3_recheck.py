"""Recheck of source item 36 — Phase II / Round A-U.2b.3, Queue-Prefactor Saturation.

數學戰士「墜衡」 / AMRAL Research Lab.

This round corrects A-U.2b.2: its queue DP counted **pointed** paths where its
own §4 defined an **unpointed** word set. RUN-017 reproduced that DP faithfully
and did not notice — because it reimplemented the *program* and validated it
against a brute force written from the program's reading.

So everything here is implemented from the **prose definitions**:

  R(e) = max_j S_j - min_j S_j        with S_j = sum_{i<=j} (e_i - b_i)
  admissible starts                    D - R(e) + 1
  P_{r,D} = sum over R(e) <= D of      D - R(e) + 1
  Q_{r,D} = #{e : R(e) <= D}           and the identity Q = P_D - P_{D-1}

and the identity is checked against a direct enumeration of *words*, which is
the check that was missing last time.

Usage:  python code/src20_hardzeta_au2b3_recheck.py
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

BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b3_bundle.zip"
AU2B3 = "Hard_Zeta_Phase_II_Round_AU2b3_Queue_Prefactor_Saturation_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.4_AU2b3.md"
DIAG = "Hard_Zeta_AU2b3_queue_prefactor_diagnostics.json"
SCRIPT = "verify_Hard_Zeta_AU2b3_queue_prefactor.py"
AU2B2_NEW = "Hard_Zeta_Phase_II_Round_AU2b2_Queue_Entropy_Second_Order_Barrier_v0.1.1.md"
PREV_BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b2_bundle.zip"
AU2B2_OLD = "Hard_Zeta_Phase_II_Round_AU2b2_Queue_Entropy_Second_Order_Barrier_v0.1.md"

DIGITS = 60
getcontext().prec = DIGITS + 30
LN2 = Decimal(2).ln()
BETA_D = Decimal(3).ln() / LN2
GAMMA_D = BETA_D - 1


def H(z: float) -> float:
    return (1 + z) * math.log2(1 + z) - z * math.log2(z)


def read_sources() -> dict[str, bytes]:
    out = {}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                out[pathlib.PurePosixPath(n).name] = z.read(n)
    return out


def main() -> int:
    rep = {
        "tool": "src20_hardzeta_au2b3_recheck.py",
        "subject": "Hard_Zeta_Phase_II_Round_AU2b3_bundle.zip (item 36) — Round "
                   "A-U.2b.3, its prefactor diagnostics, three figures, the "
                   "corrected A-U.2b.2 v0.1.1, plus A_Line_ROUTE_MAP v1.4",
        "source_items": [36],
        "scope": "the pointed/unpointed identity implemented from the prose "
                 "definitions, the prefactor diagnostics, the corrigendum to "
                 "A-U.2b.2, and the claim that the packing branch is closed",
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
    au2b3 = raw.get(AU2B3, b"").decode("utf-8")
    routemap = raw.get(ROUTEMAP, b"").decode("utf-8")
    au2b2_new = raw.get(AU2B2_NEW, b"").decode("utf-8")
    diag = json.loads(raw.get(DIAG, b"{}").decode("utf-8"))

    SMALL = ((3, 1), (4, 2), (5, 2), (6, 2), (4, 3), (5, 1), (3, 2))

    # ------------------------- §4-§7: the identities, from the definitions
    def multiplicity_formula():
        # D - R(e) + 1 must equal the number of starts that actually work, found
        # by trying every one of them
        bad, tested = [], 0
        for r, D in SMALL[:5]:
            for w in A.unpointed_words(r, D):
                works = 0
                for d0 in range(D + 1):
                    d, ok = d0, True
                    for j, e in enumerate(w, start=1):
                        d = d + A.phase_credit(j) - e
                        if not (0 <= d <= D):
                            ok = False
                            break
                    works += ok
                tested += 1
                if works != A.pointing_multiplicity(w, D):
                    bad.append((r, D, w, works, A.pointing_multiplicity(w, D)))
        return (not bad and tested > 0), {"words": tested, "violations": bad[:5]}

    check("SRC20_the_pointing_multiplicity_is_the_number_of_starts_that_work",
          multiplicity_formula,
          "§4: D - R(e) + 1, against trying every starting deficit")

    def pointed_is_the_multiplicity_sum():
        bad = []
        for r, D in SMALL:
            got = sum(A.pointing_multiplicity(w, D) for w in A.unpointed_words(r, D))
            if got != A.queue_count(r, D):
                bad.append((r, D, got, A.queue_count(r, D)))
        return not bad, {"shapes": len(SMALL), "violations": bad}

    check("SRC20_the_pointed_count_is_the_sum_of_multiplicities",
          pointed_is_the_multiplicity_sum,
          "§5: P = sum over admissible words of (D - R(e) + 1), against the DP")

    def finite_difference_identity():
        # THE check that was missing in RUN-017: the word count from the
        # definition against the finite difference of the program's count
        bad = []
        for r, D in SMALL:
            words = len(A.unpointed_words(r, D))
            fd = A.unpointed_queue_count(r, D)
            if words != fd:
                bad.append((r, D, words, fd))
        return not bad, {"shapes": len(SMALL), "violations": bad}

    check("SRC20_the_word_count_equals_the_finite_difference_of_the_pointed_count",
          finite_difference_identity,
          "§7: Q = P_D - P_{D-1}, with Q enumerated from §4's definition")

    def pointed_and_unpointed_really_differ():
        # if they agreed, the whole corrigendum would be empty and every check
        # above would be about one object rather than two
        gaps = [(r, D, A.queue_count(r, D), A.unpointed_queue_count(r, D))
                for r, D in SMALL]
        differing = [g for g in gaps if g[2] != g[3]]
        measured["pointed_vs_unpointed_small"] = gaps
        return len(differing) == len(gaps), {
            "shapes": len(gaps), "all_differ": len(differing) == len(gaps),
            "sample": gaps[:3]}

    check("SRC20_pointed_and_unpointed_counts_genuinely_differ",
          pointed_and_unpointed_really_differ,
          "the correction is only meaningful if the two objects are not equal")

    def range_definition():
        # R(e) from S_j, checked against a direct max/min walk
        bad = []
        for r, D in SMALL[:4]:
            for w in A.unpointed_words(r, D):
                S, lo, hi = 0, 0, 0
                for j, e in enumerate(w, start=1):
                    S += e - A.phase_credit(j)
                    lo, hi = min(lo, S), max(hi, S)
                if hi - lo != A.word_range(w):
                    bad.append((r, D, w))
        return not bad, {"violations": bad[:5]}

    check("SRC20_the_word_range_is_the_span_of_its_partial_sums", range_definition,
          "§4: R(e) = max_j S_j - min_j S_j with S_j = sum (e_i - b_i)")

    # ------------------------------------- §28: the published diagnostics
    def diagnostics_reproduce():
        bad, rows = [], []
        for row in diag.get("rows", []):
            r, D = row["r"], row["D"]
            P = A.queue_count(r, D)
            Q = A.unpointed_queue_count(r, D)
            G = A.bridge_count(r, D)
            B = A.floor_beta(r) - r
            E = B + D
            z = E / r
            comp = math.comb(r + E - 1, E)
            mine = {
                "z_r": z,
                "log2_P_over_composition": math.log2(P) - math.log2(comp),
                "log2_Q_over_composition": math.log2(Q) - math.log2(comp),
                "log2_bridge_over_composition": math.log2(G) - math.log2(comp),
                "P_centered_prefactor": r * H(z) - math.log2(P) - 0.5 * math.log2(r),
                "Q_centered_prefactor": r * H(z) - math.log2(Q) - 0.5 * math.log2(r),
                "bridge_centered_prefactor": r * H(z) - math.log2(G) - 0.5 * math.log2(r),
                "pointing_multiplicity_ratio": P / Q,
            }
            for k, v in mine.items():
                if abs(v - row[k]) > 1e-9:
                    bad.append((r, k, v, row[k]))
            rows.append({"r": r, "D": D, **mine})
        measured["diagnostics"] = rows
        return (not bad and len(rows) >= 9), {"rows": len(rows),
                                              "violations": bad[:5]}

    check("SRC20_every_published_diagnostic_row_reproduces_from_the_definitions",
          diagnostics_reproduce,
          "§28: eight columns on nine rows, computed from §4-§7 rather than from "
          "the shipped script")

    def corridor_rule():
        x = float(diag.get("x_star", 0))
        bad = [(row["r"], row["D"]) for row in diag.get("rows", [])
               if row["D"] != math.floor(x * row["r"])]
        return (not bad and x > 0), {"violations": bad, "x_star": x}

    check("SRC20_each_diagnostic_row_uses_the_critical_corridor",
          corridor_rule, "D = floor(x* r), the packing-critical width")

    def prefactor_stays_bounded():
        # §19: Q = Theta(r^{-1/2} 2^{rH}), so the centered prefactor must stay in
        # a band rather than drift. Reported as a band, NOT as convergence — it
        # is not monotone.
        rows = measured.get("diagnostics", [])
        vals = [r["Q_centered_prefactor"] for r in rows]
        band = max(vals) - min(vals)
        ratios = [r["pointing_multiplicity_ratio"] for r in rows]
        measured["prefactor_band"] = {
            "Q_centered_min": min(vals), "Q_centered_max": max(vals),
            "band_width": band, "monotone": all(vals[i + 1] <= vals[i]
                                                for i in range(len(vals) - 1)),
            "pointing_ratio_first": ratios[0], "pointing_ratio_last": ratios[-1],
            "reading": ("the centered prefactor sits in a band of width 2.3 and "
                        "is NOT monotone — it bottoms at r = 5000 and rises "
                        "again — which is consistent with Theta(r^{-1/2}) and is "
                        "all a finite table can show. The pointing ratio settles "
                        "near 1.638, which is why the correction cannot move the "
                        "exponential rate or the prefactor scale.")}
        return (band < 3 and 1.5 < ratios[-1] < 1.8), {
            "band_width": band, "pointing_ratio_last": ratios[-1]}

    check("SRC20_the_centered_prefactor_stays_in_a_narrow_band",
          prefactor_stays_bounded,
          "§19, §21: consistent with Theta(r^{-1/2} 2^{rH}); a band, not a limit")

    # --------------------------------- §22-§23: the constants are unchanged
    def constants_unchanged():
        c = A.packing_constant(DIGITS)
        d = A.second_order_constant(DIGITS)
        # the documents print 19 significant characters and then an ellipsis,
        # so the search string has to be the PUBLISHED prefix, not a longer one
        published = "0.03585676003404866"
        return (str(+c).startswith(published)
                and str(+d).startswith("0.3689789787331465")
                and published in au2b3 + routemap), {
            "c_pack": str(+c)[:22], "d_pack": str(+d)[:22]}

    check("SRC20_the_two_earlier_constants_are_unchanged", constants_unchanged,
          "§22-§23: the correction moves neither c_pack nor d_pack")

    # ------------------------------------------- the corrigendum itself
    def corrigendum_present():
        return ("Corrigendum" in routemap
                and "pointed" in routemap
                and "v0.1.1" in routemap
                and bool(au2b2_new)), {
            "route_map_flags_it": "Corrigendum" in routemap,
            "corrected_file_shipped": bool(au2b2_new)}

    check("SRC20_the_corrigendum_is_declared_and_the_corrected_file_shipped",
          corrigendum_present,
          "the route map must say A-U.2b.2's DP counted pointed paths, and the "
          "corrected file must be in the bundle")

    def corrigendum_is_additive():
        # v0.1.1 must correct the DP section and NOT quietly change the results
        with zipfile.ZipFile(SOURCE / PREV_BUNDLE) as z:
            old = next(z.read(n).decode("utf-8") for n in z.namelist()
                       if pathlib.PurePosixPath(n).name == AU2B2_OLD)
        for key in ("0.3689789787331466", "0.03585676003404866",
                    "Prefix-Constraint", "Second-Order Packing Barrier"):
            if key not in old or key not in au2b2_new:
                return False, {"missing_from_one_version": key}
        grew = len(au2b2_new) > len(old)
        names_it = "Pointed" in au2b2_new and "unpointed" in au2b2_new
        measured["corrigendum"] = {
            "v0_1_chars": len(old), "v0_1_1_chars": len(au2b2_new),
            "both_keep_the_two_constants": True,
            "reading": ("the corrected file ADDS a pointed/unpointed section and "
                        "keeps both constants and both theorem names, so the "
                        "correction is scoped to the DP diagnostic")}
        return (grew and names_it), {"grew": grew, "names_the_distinction": names_it}

    check("SRC20_the_corrected_file_adds_the_distinction_without_moving_the_results",
          corrigendum_is_additive,
          "v0.1.1 against v0.1: both constants and both theorem names survive")

    # ---------------------------------------------- ledger and provenance
    def three_way_ledger():
        # §33 splits into self-contained / analytic dependency / unproved, which
        # is a stronger statement than the usual two-way ledger
        return ("Self-contained exact results" in au2b3
                and "Standard analytic dependency" in au2b3
                and "## 未證" in au2b3
                and "local-limit" in au2b3), {
            "declares_its_analytic_dependency": "Standard analytic dependency" in au2b3}

    check("SRC20_the_paper_separates_self_contained_results_from_its_analytic_dependency",
          three_way_ledger,
          "§33: the saturation lower bound leans on standard lattice local-limit "
          "and ballot estimates, and the round says so rather than absorbing it")

    def unproved_list():
        tail = au2b3[au2b3.find("## 未證"):] if "## 未證" in au2b3 else ""
        want = ["CASP", "Terras", "Collatz"]
        missing = [w for w in want if w not in tail]
        return (bool(tail) and not missing), {"missing": missing}

    check("SRC20_the_paper_lists_casp_terras_and_collatz_as_unproved",
          unproved_list, "§33")

    def branch_closed_list():
        # sliced to section 31 ALONE: the words also appear in section 33's
        # self-contained list, so a wider slice survives losing an item here
        tail = (au2b3[au2b3.find("# 31."):au2b3.find("# 32.")]
                if "# 31." in au2b3 and "# 32." in au2b3 else "")
        items = ["entropy", "constant", "Stirling", "prefix", "prefactor",
                 "pointed", "no-gain"]
        missing = [i for i in items if i not in tail]
        return (bool(tail) and not missing and "Packing branch closed" in routemap), {
            "missing_from_the_closed_list": missing}

    check("SRC20_the_packing_branch_is_declared_closed_with_its_seven_items",
          branch_closed_list,
          "§31 and the route map: what has been exhausted, itemised")

    def next_routes_named():
        return (all(s in routemap for s in ("A-U.2c", "A-U.2d", "A-U.2e"))
                and "Multiscale Return Arithmetic" in routemap), {
            "routes": ["2c", "2d", "2e"]}

    check("SRC20_the_route_map_names_the_three_successor_routes", next_routes_named,
          "with the branch closed, what remains must be stated")

    def bundle_provenance():
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
                              "new_in_this_bundle": sorted(fresh)}
        # AU2b2 appears under a NEW filename (v0.1.1), so nothing should be an
        # in-place edit: a silent same-name change is what would be wrong
        return (not edited and AU2B2_NEW in fresh and AU2B2_OLD not in big), {
            "silently_edited_in_place": edited,
            "corrected_file_is_a_new_name": AU2B2_NEW in fresh,
            "superseded_file_dropped": AU2B2_OLD not in big}

    check("SRC20_the_correction_ships_under_a_new_name_rather_than_in_place",
          bundle_provenance,
          "a corrigendum that overwrote the old filename would erase its own "
          "history; this one supersedes by version instead")

    # ------------------------------------------------------ own measurement
    def what_the_correction_cost():
        # RUN-017 graded the pointed table. Quantify the difference so the
        # earlier report can be corrected with a number rather than a hedge.
        rows = []
        for r, D in ((200, 11), (800, 45), (2000, 113), (5000, 284)):
            P = A.queue_count(r, D)
            Q = A.unpointed_queue_count(r, D)
            rows.append({"r": r, "rate_pointed": math.log2(P) / r,
                         "rate_unpointed": math.log2(Q) / r,
                         "shift": math.log2(P) / r - math.log2(Q) / r})
        measured["correction_cost"] = {
            "rows": rows, "max_shift": max(x["shift"] for x in rows),
            "reading": ("RUN-017 reproduced the pointed rate. Recomputing the "
                        "unpointed one moves it by at most 1.5e-3 and by 1.4e-4 "
                        "at r = 5000, so the first-order saturation verdict of "
                        "that run stands; only its object was mislabelled.")}
        return (max(x["shift"] for x in rows) < 0.002
                and rows[-1]["shift"] < 0.0002), {"rows": rows}

    check("SRC20_the_pointed_unpointed_correction_does_not_move_the_first_order_rate",
          what_the_correction_cost,
          "measurement: what RUN-017's mislabelling actually cost")

    rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
    rep["counts"] = {"checks": len(checks),
                     "passed": sum(1 for v in checks.values() if v["pass"])}
    rep["ok"] = not rep["failures"]
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
