"""Mutation drill for src15_hardzeta_au1_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

A-U.1 is a negative round, so the defects that matter are of two kinds: damage
to the countermodels it stands on (if the Bernoulli measure or the mechanical
code were mis-implemented, the no-go would be checked against nothing), and
damage to the anchor cocycle, which is the datum the whole round says is
load-bearing. Both are planted, plus scope edits to the documents and to the
bundle's re-shipped Phase I files.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src15_drill.py
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
TOOL = CODE / "src15_hardzeta_au1_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_II_Round_AU1_bundle.zip"
AU1 = "Hard_Zeta_Phase_II_Round_AU1_Critical_Occupation_Anchor_Erasure_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v0.9_AU1.md"
PHASE_I = "Hard_Zeta_Phase_I_Round_03A5_Exceptional_Occupancy_Rigidity_v0.1.md"
COMPANION = "Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip"
TIMEOUT_S = 900

ACCEL_DEFECTS = [
    ("A01_shift_code_drops_two_symbols",
     "SRC15_the_code_map_intertwines_with_the_shift",
     ("    return kappa[1:]", "    return kappa[2:]")),
    ("A02_code_cylinder_loses_the_oddness_bit",
     "SRC15_a_finite_code_is_exactly_one_clopen_cylinder",
     ("    return source_residue(kappa), 1 << (cumulative(kappa)[-1] + 1)",
      "    return source_residue(kappa), 1 << cumulative(kappa)[-1]")),
    ("A03_anchor_cocycle_skips_the_first_prefix",
     "SRC15_a_positive_integer_anchor_is_exactly_an_eventually_zero_lift",
     ("    return [lift_digit(kappa[:j]) for j in range(1, len(kappa) + 1)]",
      "    return [lift_digit(kappa[:j]) for j in range(2, len(kappa) + 1)]")),
    ("A04_mechanical_valuation_uses_the_wrong_predecessor",
     "SRC15_the_mechanical_code_matches_its_stated_formula",
     ("    return floor_beta(m) - floor_beta(m - 1)",
      "    return floor_beta(m) - floor_beta(m - 2)")),
    ("A05_two_frequency_counts_the_other_symbol",
     "SRC15_the_mechanical_two_frequency_converges_to_gamma",
     ("if mechanical_valuation(j) == 2), m)", "if mechanical_valuation(j) == 1), m)")),
    ("A06_bernoulli_mean_weights_swapped",
     "SRC15_the_bernoulli_critical_measure_has_mean_beta",
     ("    return 1 * (1 - p) + 2 * p", "    return 1 * p + 2 * (1 - p)")),
    ("A07_singular_cylinder_modulus_off_by_one",
     "SRC15_the_singular_cylinders_nest_and_are_exactly_high_valuation",
     ("    return cylinder_residue(r), 1 << r", "    return cylinder_residue(r), 1 << (r + 1)")),
    ("A08_singular_membership_ignores_the_residue",
     "SRC15_the_truncated_observable_is_the_clipped_valuation",
     ("    return y % mod == res", "    return y % mod != res")),
    ("A09_lift_digit_divides_by_the_wrong_power",
     "SRC15_the_anchor_cocycle_recursion_is_exact",
     ("    return (source_residue(kappa) - r_prev) // 2 ** (K_prev + 1)",
      "    return (source_residue(kappa) - r_prev) // 2 ** K_prev")),
    ("A10_source_residue_drops_the_extra_digit",
     "SRC15_the_positive_integers_are_dense_but_not_closed",
     ("    mod = 2 ** (K + 1)", "    mod = 2 ** K")),
    ("A11_mechanical_code_telescopes_from_the_wrong_index",
     "SRC15_the_mechanical_cumulative_telescopes_to_floor_beta",
     ("    return tuple(floor_beta(j) - floor_beta(j - 1) for j in range(1, m + 1))",
      "    return tuple(floor_beta(j + 1) - floor_beta(j) for j in range(1, m + 1))")),
    # Six checks initially had no defect naming them. Each gets one, because a
    # drill count says nothing about a check nothing points at.
    ("A12_source_residue_forgets_the_modular_inverse",
     "SRC15_exact_cylinders_nest_as_the_code_extends",
     ("    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod",
      "    return ((2 ** K - offset(kappa)) * pow(3, m, mod)) % mod")),
    ("A13_offset_accumulates_after_advancing_the_exponent",
     "SRC15_every_finite_code_including_large_valuations_is_realized",
     ("    for k in kappa:\n        B = 3 * B + 2 ** K\n        K += k",
      "    for k in kappa:\n        K += k\n        B = 3 * B + 2 ** K")),
    ("A14_excess_double_counts_the_step_length",
     "SRC15_the_singular_mass_bound_holds_on_real_spines",
     ("    return cumulative(accel_code(n, m))[-1] - m",
      "    return cumulative(accel_code(n, m))[-1] - 2 * m")),
    # NOT "rounds up": floor_beta appears in the mechanical code only as a
    # DIFFERENCE, so a constant offset telescopes away and the mutation is a
    # no-op — the same cancellation that retired a defect in RUN-011. Changing
    # the base survives telescoping and really moves K*_m.
    ("A15_floor_beta_uses_the_wrong_base",
     "SRC15_the_mechanical_code_is_subcritical_at_every_prefix",
     ("    return (3 ** j).bit_length() - 1", "    return (4 ** j).bit_length() - 1")),
    ("A16_mechanical_valuation_steps_two_at_a_time",
     "SRC15_the_mechanical_code_uses_only_the_two_symbol_alphabet",
     ("    return floor_beta(m) - floor_beta(m - 1)",
      "    return floor_beta(2 * m) - floor_beta(2 * (m - 1))")),
    # NOT a widened modulus: r + t·2^{K+2} is a SUBSET of the cylinder, so
    # widening is a no-op. Narrowing it admits starts outside the cylinder.
    ("A17_code_lifts_step_by_half_the_modulus",
     "SRC15_every_finite_cylinder_holds_infinitely_many_positive_integers",
     ("    r, step = source_residue(kappa), 1 << (cumulative(kappa)[-1] + 1)",
      "    r, step = source_residue(kappa), 1 << cumulative(kappa)[-1]")),
]

TOOL_DEFECTS = [
    ("T01_the_settle_search_accepts_a_single_zero",
     "SRC15_a_positive_integer_anchor_is_exactly_an_eventually_zero_lift",
     ("            settle = next((j for j in range(len(t))\n"
      "                           if all(x == 0 for x in t[j:])), None)",
      "            settle = next((j for j in range(len(t))\n"
      "                           if t[j] == 0), None)")),
    # Loosening the separation threshold would be a NO-OP: the mechanical code
    # clears it by a wide margin either way. Feeding the check a genuine
    # integer's code instead is what moves the answer.
    ("T02_the_separation_measures_an_integer_instead_of_the_countermodel",
     "SRC15_the_anchor_cocycle_separates_the_mechanical_code_from_integers",
     ("        mech = A.mechanical_code(DEPTH)\n        t_mech = A.anchor_cocycle(mech)",
      "        mech = A.accel_code(27, DEPTH)\n        t_mech = A.anchor_cocycle(mech)")),
    ("T03_the_bundle_comparison_globs_nothing",
     "SRC15_the_bundle_reships_phase_i_unedited",
     ('SOURCE.glob("Hard_Zeta_*Rounds_01_03A5*.zip")',
      'SOURCE.glob("Hard_Zeta_*NO_SUCH_BUNDLE*.zip")')),
    # Dropping an entry from the want-list is a NO-OP: it only weakens the
    # requirement, and the real document satisfies both versions. Reading the
    # PROVED section instead moves the answer — that list names none of the four.
    ("T04_the_unproved_list_is_read_from_the_proved_section",
     "SRC15_the_paper_lists_terras_and_collatz_as_unproved",
     ('tail = au1[au1.find("## 未證"):] if "## 未證" in au1 else ""',
      'tail = au1[au1.find("## 已證"):au1.find("## 未證")] if "## 未證" in au1 else ""')),
    ("T05_the_source_growth_check_accepts_a_settled_source",
     "SRC15_the_mechanical_source_grows_without_settling",
     ("        mech = A.mechanical_code(DEPTH)\n        bits = [A.source_residue",
      "        mech = A.accel_code(27, DEPTH)\n        bits = [A.source_residue")),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_unproved_ledger",
     "SRC15_the_paper_keeps_an_explicit_proved_and_unproved_ledger", "ledger"),
    ("D02_unproved_list_drops_the_conjecture",
     "SRC15_the_paper_lists_terras_and_collatz_as_unproved", "collatz"),
    ("D03_route_map_loses_the_no_go",
     "SRC15_the_route_map_and_the_paper_agree_on_the_no_go", "routemap"),
    ("D04_bundle_edits_the_reshipped_phase_i_round",
     "SRC15_the_bundle_reships_phase_i_unedited", "reship"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"ledger": AU1, "collatz": AU1, "routemap": ROUTEMAP, "reship": PHASE_I}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    if kind == "ledger":
        t = t.replace("## 未證", "## 附註", 1)
    elif kind == "collatz":
        head, _, tail = t.partition("## 未證")
        t = head + "## 未證" + tail.replace("Collatz conjecture", "後續工作", 1)
    elif kind == "routemap":
        t = t.replace("Pure occupation no-go", "Pure occupation note", 1)
    elif kind == "reship":
        t = t + "\n<!-- edited inside the AU1 bundle -->\n"
    keep[name] = t.encode("utf-8")
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def main() -> int:
    rep = {
        "tool": "src15_drill.py",
        "subject": "src15_hardzeta_au1_recheck.py and the A-U.1 layer of "
                   "hz_accel_code.py",
        "defects": {}, "controls": {},
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
        checks = res.get("checks", {})
        rep["defects"][name] = {
            "target_check": target,
            "caught_by_the_named_check": target in checks and not checks[target]["pass"],
            "run_went_red": not res.get("ok", True),
            "other_checks_that_also_fired": sorted(
                k for k, v in checks.items() if not v["pass"] and k != target),
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
        shutil.copy2(SOURCE / COMPANION, base / COMPANION)   # the faithfulness peer

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

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

        mod = "_drill_accel_null15"
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
        "defects_in_the_au1_layer": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_measurement": len(TOOL_DEFECTS),
        "scope_defects_in_the_documents": len(DOC_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
