"""Mutation drill for src20_hardzeta_au2b3_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The objects here are defined in prose and implemented from that prose, so the
defects damage the definition layer: the range of a word, the multiplicity of
its pointings, the finite-difference identity between the two counts. The
enumeration that grades them is damaged too, because in RUN-017 it was the
enumeration that quietly agreed with the wrong reading.

Every check must have at least one defect naming it; `audit()` enforces that
before the mutation loop runs. No defect loosens a comparison.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src20_drill.py
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE = ROOT / "code"
TOOL = CODE / "src20_hardzeta_au2b3_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_II_Round_AU2b3_bundle.zip"
AU2B3 = "Hard_Zeta_Phase_II_Round_AU2b3_Queue_Prefactor_Saturation_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.4_AU2b3.md"
DIAG = "Hard_Zeta_AU2b3_queue_prefactor_diagnostics.json"
AU2B2_NEW = "Hard_Zeta_Phase_II_Round_AU2b2_Queue_Entropy_Second_Order_Barrier_v0.1.1.md"
COMPANIONS = ["Hard_Zeta_Phase_II_Round_AU2b2_bundle.zip"]
TIMEOUT_S = 1800

ACCEL_DEFECTS = [
    ("A01_the_word_range_forgets_the_credit",
     "SRC20_the_word_range_is_the_span_of_its_partial_sums",
     ("        S += e - phase_credit(i, phase)", "        S += e")),
    ("A02_the_word_range_ignores_the_origin",
     "SRC20_the_pointing_multiplicity_is_the_number_of_starts_that_work",
     ("    S = 0\n    lo = hi = 0", "    S = 0\n    lo = hi = 10 ** 9")),
    ("A03_the_multiplicity_is_off_by_one",
     "SRC20_the_pointed_count_is_the_sum_of_multiplicities",
     ("    return max(0, D - word_range(word, phase) + 1)",
      "    return max(0, D - word_range(word, phase))")),
    ("A04_the_finite_difference_uses_the_wrong_neighbour",
     "SRC20_the_word_count_equals_the_finite_difference_of_the_pointed_count",
     ("    return queue_count(r, D, phase) - (queue_count(r, D - 1, phase) if D else 0)",
      "    return queue_count(r, D, phase) - (queue_count(r, D - 2, phase) if D > 1 else 0)")),
    # The walk prune and the final filter are MUTUALLY redundant: R(e) is
    # monotone in the prefix, so anything surviving the prune already satisfies
    # the filter. Loosening EITHER alone is a no-op. The e-range bound is the one
    # guard that is not doubled — a word needs e_j <= D+1 to be admissible, so
    # narrowing it to D drops real words (48 -> 43 at r=4, D=2).
    ("A05_the_unpointed_enumeration_bounds_the_excess_too_tightly",
     "SRC20_the_word_count_equals_the_finite_difference_of_the_pointed_count",
     ("        for e in range(0, D + 2):", "        for e in range(0, D + 1):")),
    ("A06_the_bridge_starts_from_the_wrong_end",
     "SRC20_every_published_diagnostic_row_reproduces_from_the_definitions",
     ("    vec = [0] * (D + 1)\n    vec[D] = 1", "    vec = [0] * (D + 1)\n    vec[0] = 1")),
    ("A07_the_pointed_dp_ignores_the_credit",
     "SRC20_the_centered_prefactor_stays_in_a_narrow_band",
     ("        vec = [total - pref[max(0, t - b)] for t in range(D + 1)]",
      "        vec = [total - pref[t] for t in range(D + 1)]")),
    # Retargeted: the corridor check reads x_star from the JSON and never calls
    # floor_beta. What a wrong base breaks is the diagnostics themselves.
    ("A08_floor_beta_uses_the_wrong_base",
     "SRC20_every_published_diagnostic_row_reproduces_from_the_definitions",
     ("        _POW3.append(_POW3[-1] * 3)", "        _POW3.append(_POW3[-1] * 4)")),
    ("A09_the_entropy_root_bisects_the_wrong_way",
     "SRC20_the_two_earlier_constants_are_unchanged",
     ("        if packing_entropy(mid) < beta:\n            lo = mid\n        else:\n            hi = mid",
      "        if packing_entropy(mid) < beta:\n            hi = mid\n        else:\n            lo = mid")),
    ("A10_the_credit_is_taken_across_two_steps",
     "SRC20_the_pointed_unpointed_correction_does_not_move_the_first_order_rate",
     ("    _CREDIT_CACHE[key] = fl(phase + j) - fl(phase + j - 1)",
      "    _CREDIT_CACHE[key] = fl(phase + j) - fl(phase + j - 2)")),
]

TOOL_DEFECTS = [
    # Reversing the walk is a NO-OP for a mathematical reason: the count of
    # admissible starts depends only on R(e) = max S - min S, which is invariant
    # under S -> -S. Verified on every word at four shapes. Widening the corridor
    # by one admits starts that should not qualify.
    ("T01_the_multiplicity_check_uses_a_corridor_one_too_wide",
     "SRC20_the_pointing_multiplicity_is_the_number_of_starts_that_work",
     ("                        if not (0 <= d <= D):",
      "                        if not (0 <= d <= D + 1):")),
    ("T02_the_range_check_reuses_the_library_partial_sums",
     "SRC20_the_word_range_is_the_span_of_its_partial_sums",
     ("                    S += e - A.phase_credit(j)",
      "                    S += e - A.phase_credit(j) + 1")),
    ("T03_the_diagnostic_tolerance_reads_the_wrong_composition",
     "SRC20_every_published_diagnostic_row_reproduces_from_the_definitions",
     ("            comp = math.comb(r + E - 1, E)",
      "            comp = math.comb(r + E, E)")),
    ("T04_the_band_check_reads_the_row_index",
     "SRC20_the_centered_prefactor_stays_in_a_narrow_band",
     ('        vals = [r["Q_centered_prefactor"] for r in rows]',
      '        vals = [r["r"] for r in rows]')),
    ("T05_the_difference_check_compares_a_count_to_itself",
     "SRC20_pointed_and_unpointed_counts_genuinely_differ",
     ("        gaps = [(r, D, A.queue_count(r, D), A.unpointed_queue_count(r, D))",
      "        gaps = [(r, D, A.queue_count(r, D), A.queue_count(r, D))")),
    ("T06_the_corrigendum_check_looks_at_the_wrong_document",
     "SRC20_the_corrigendum_is_declared_and_the_corrected_file_shipped",
     ('        return (\"Corrigendum\" in routemap',
      '        return (\"Corrigendum\" in au2b3')),
    ("T07_the_additivity_check_stops_requiring_the_constants",
     "SRC20_the_corrected_file_adds_the_distinction_without_moving_the_results",
     ('        grew = len(au2b2_new) > len(old)',
      '        grew = len(au2b2_new) < len(old)')),
    ("T08_the_unproved_list_is_read_from_the_self_contained_section",
     "SRC20_the_paper_lists_casp_terras_and_collatz_as_unproved",
     ('        tail = au2b3[au2b3.find("## 未證"):] if "## 未證" in au2b3 else ""',
      '        tail = au2b3[au2b3.find("## Self-contained"):au2b3.find("## 未證")] if "## 未證" in au2b3 else ""')),
    ("T09_the_closed_branch_list_is_read_from_the_wrong_section",
     "SRC20_the_packing_branch_is_declared_closed_with_its_seven_items",
     ('        tail = (au2b3[au2b3.find("# 31."):au2b3.find("# 32.")]',
      '        tail = (au2b3[au2b3.find("# 1."):au2b3.find("# 2.")]')),
    # Dropping `not edited` is vacuous on a clean bundle. Miscomputing `edited`
    # so that it flags every file is what the check has to survive.
    ("T10_the_provenance_check_flags_every_file_as_edited",
     "SRC20_the_correction_ships_under_a_new_name_rather_than_in_place",
     ("        edited = [n for n, h in big.items() if n in prev and prev[n] != h]",
      "        edited = [n for n in big]")),
    ("T11_the_correction_cost_reads_the_same_count_twice",
     "SRC20_the_pointed_unpointed_correction_does_not_move_the_first_order_rate",
     ('            Q = A.unpointed_queue_count(r, D)\n            rows.append({"r": r, "rate_pointed"',
      '            Q = A.queue_count(r, D) // 3\n            rows.append({"r": r, "rate_pointed"')),
]

DOC_DEFECTS = [
    ("D01_route_map_loses_its_corrigendum",
     "SRC20_the_corrigendum_is_declared_and_the_corrected_file_shipped", "corr"),
    ("D02_paper_absorbs_its_analytic_dependency",
     "SRC20_the_paper_separates_self_contained_results_from_its_analytic_dependency",
     "dependency"),
    ("D03_route_map_drops_a_successor_route",
     "SRC20_the_route_map_names_the_three_successor_routes", "routes"),
    ("D04_the_closed_branch_list_loses_an_item",
     "SRC20_the_packing_branch_is_declared_closed_with_its_seven_items", "closed"),
    ("D05_the_diagnostics_json_is_perturbed",
     "SRC20_every_published_diagnostic_row_reproduces_from_the_definitions", "diag"),
    ("D06_the_corridor_constant_is_shifted",
     "SRC20_each_diagnostic_row_uses_the_critical_corridor", "xstar"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"corr": ROUTEMAP, "routes": ROUTEMAP, "dependency": AU2B3,
           "closed": AU2B3, "diag": DIAG, "xstar": DIAG}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    if kind == "corr":
        t = t.replace("# Corrigendum", "# Note", 1)
    elif kind == "routes":
        t = t.replace("A-U.2e — Multiscale Return Arithmetic", "later work", 1)
    elif kind == "dependency":
        t = t.replace("Standard analytic dependency", "Further remarks", 1)
    elif kind == "closed":
        t = t.replace("6. pointed/unpointed correction；", "", 1)
    elif kind == "diag":
        rec = json.loads(t)
        rec["rows"][3]["Q_centered_prefactor"] += 1e-6
        t = json.dumps(rec, ensure_ascii=False, indent=2)
    elif kind == "xstar":
        rec = json.loads(t)
        rec["x_star"] = rec["x_star"] * 1.02
        t = json.dumps(rec, ensure_ascii=False, indent=2)
    keep[name] = t.encode("utf-8")
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def audit(baseline: dict) -> list[str]:
    targeted = ({t for _, t, _ in ACCEL_DEFECTS} | {t for _, t, _ in TOOL_DEFECTS}
                | {t for _, t, _ in DOC_DEFECTS})
    names = set(baseline.get("checks", {}))
    return sorted([f"unguarded check: {c}" for c in names - targeted]
                  + [f"defect names a check that does not exist: {t}"
                     for t in targeted - names])


def main() -> int:
    rep = {
        "tool": "src20_drill.py",
        "subject": "src20_hardzeta_au2b3_recheck.py and the A-U.2b.3 layer of "
                   "hz_accel_code.py",
        "defects": {}, "controls": {}, "audit": [],
    }
    original_accel = ACCEL.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, accel="hz_accel_code") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ACCEL_MODULE": accel}
        try:
            out = subprocess.run([sys.executable, str(tool)], capture_output=True,
                                 text=True, encoding="utf-8", timeout=TIMEOUT_S,
                                 env=env)
        except subprocess.TimeoutExpired:
            return {"ok": False, "checks": {}, "_crash": "timed out"}
        try:
            return json.loads(out.stdout)
        except json.JSONDecodeError:
            return {"ok": False, "checks": {},
                    "_crash": (out.stdout + out.stderr)[-400:]}

    def record(name, target, res):
        c = res.get("checks", {})
        rep["defects"][name] = {
            "target_check": target,
            "caught_by_the_named_check": target in c and not c[target]["pass"],
            "run_went_red": not res.get("ok", True),
            "other_checks_that_also_fired": sorted(
                k for k, v in c.items() if not v["pass"] and k != target),
            **({"crash": res["_crash"]} if "_crash" in res else {}),
        }

    def absent(name, target, anchor):
        rep["defects"][name] = {
            "target_check": target, "caught_by_the_named_check": False,
            "run_went_red": False, "other_checks_that_also_fired": [],
            "crash": f"anchor {anchor!r} absent; nothing was tested"}

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        base = tmp / "source"
        base.mkdir()
        shutil.copy2(SOURCE / BUNDLE, base / BUNDLE)
        for c in COMPANIONS:
            shutil.copy2(SOURCE / c, base / c)

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2
        rep["audit"] = audit(baseline)
        if rep["audit"]:
            print(json.dumps({"error": "coverage audit failed before the drill ran",
                              "audit": rep["audit"]}, indent=2, ensure_ascii=False))
            return 3

        for name, target, (old, new) in ACCEL_DEFECTS:
            if old not in original_accel:
                absent(name, target, old)
                continue
            mod = f"_drill_accel_{name}"
            f = CODE / f"{mod}.py"
            try:
                f.write_text(original_accel.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, TOOL, accel=mod))
            finally:
                f.unlink(missing_ok=True)

        for name, target, (old, new) in TOOL_DEFECTS:
            if old not in original_tool:
                absent(name, target, old)
                continue
            f = CODE / f"_drill_mutant_{name}.py"
            try:
                f.write_text(original_tool.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, f))
            finally:
                f.unlink(missing_ok=True)

        for name, target, kind in DOC_DEFECTS:
            s = tmp / f"src_{name}"
            shutil.copytree(base, s)
            mutate_docs(s, kind)
            record(name, target, run(s, TOOL))
            shutil.rmtree(s, ignore_errors=True)

        mod = "_drill_accel_null20"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original_accel + "\n# a comment nothing reads\n",
                         encoding="utf-8")
            res = run(base, TOOL, accel=mod)
        finally:
            f.unlink(missing_ok=True)
        rep["controls"]["N01_accel_module_annotated_where_nothing_reads"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

        s = tmp / "src_null"
        shutil.copytree(base, s)
        (s / "UNREAD.txt").write_text("read by nothing\n", encoding="utf-8")
        res = run(s, TOOL)
        rep["controls"]["N02_unrelated_file_beside_the_bundle"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(rep["defects"]),
        "defects_caught_by_the_named_check": caught,
        "defects_in_the_definition_layer": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_measurement": len(TOOL_DEFECTS),
        "scope_defects_in_the_documents": len(DOC_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
        "checks_without_a_defect_naming_them": 0,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
