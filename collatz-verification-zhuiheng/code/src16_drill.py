"""Mutation drill for src16_hardzeta_au2a_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

A-U.2a is almost entirely exact algebra, so almost every defect here is an
arithmetic one: a dropped series term, a bit block read at the wrong offset, a
recurrence with the wrong power. Two of them reproduce mistakes actually made
while writing this run — the missing `j = m` term in the inverse-code series,
and the off-by-one in the flux balance's telescoping range.

Every check must have at least one defect naming it; `audit()` enforces that
before the drill runs.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src16_drill.py
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
TOOL = CODE / "src16_hardzeta_au2a_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip"
AU2A = "Hard_Zeta_Phase_II_Round_AU2a_Lift_Occupation_Coupling_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.0_AU2a.md"
PRED = "Hard_Zeta_Phase_II_Round_AU1_Critical_Occupation_Anchor_Erasure_v0.1.md"
COMPANIONS = ["Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip",
              "Hard_Zeta_Phase_II_Round_AU1_bundle.zip"]
TIMEOUT_S = 1200

ACCEL_DEFECTS = [
    # the exact bug made while writing this run
    ("A01_inverse_series_drops_the_last_term",
     "SRC16_the_inverse_code_series_converges_to_the_exact_source",
     ("    for j in range(len(kappa) + 1):", "    for j in range(len(kappa)):")),
    ("A02_shift_code_drops_the_wrong_end",
     "SRC16_the_source_satisfies_the_shift_functional_equation",
     ("    return kappa[1:]", "    return kappa[:-1]")),
    ("A03_block_digit_reads_from_the_wrong_bit_offset",
     "SRC16_the_lift_digit_is_a_binary_block_of_the_source",
     ("    return sum(((r >> (K[m] + 1 + j)) & 1) << j for j in range(kappa[m]))",
      "    return sum(((r >> (K[m] + j)) & 1) << j for j in range(kappa[m]))")),
    ("A04_lift_digit_divides_by_the_wrong_power",
     "SRC16_the_source_is_one_plus_the_weighted_lift_series",
     ("    return (source_residue(kappa) - r_prev) // 2 ** (K_prev + 1)",
      "    return (source_residue(kappa) - r_prev) // 2 ** K_prev")),
    # Retargeted: a halved modulus still gives R = n once 2^K passes n, so the
    # dichotomy survives it. What it destroys is the extra digit that makes the
    # endpoint ODD.
    ("A05_source_residue_loses_the_oddness_digit",
     "SRC16_the_canonical_prefix_endpoint_is_a_positive_odd_integer",
     ("    mod = 2 ** (K + 1)", "    mod = 2 ** K")),
    ("A15_source_residue_is_shifted_off_the_cylinder",
     "SRC16_the_adelic_lift_dichotomy_separates_the_two_branches",
     ("    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod",
      "    return (((2 ** K - offset(kappa)) * pow(3, -m, mod)) + 2) % mod")),
    # Retargeted: R_m is DERIVED from B_m, so a damaged B propagates into R and
    # cancels inside E — the endpoint check is structurally blind to it. Only a
    # check that recomputes B independently can see it.
    ("A06_offset_advances_before_accumulating",
     "SRC16_the_affine_offset_matches_its_closed_form",
     ("    for k in kappa:\n        B = 3 * B + 2 ** K\n        K += k",
      "    for k in kappa:\n        K += k\n        B = 3 * B + 2 ** K")),
    ("A07_x_coord_normalizes_by_the_wrong_power",
     "SRC16_the_source_coordinate_follows_its_skew_product_recurrence",
     ("    return Fraction(source_residue(kappa), 1 << (cumulative(kappa)[-1] + 1))",
      "    return Fraction(source_residue(kappa), 1 << cumulative(kappa)[-1])")),
    ("A08_z_coord_normalizes_by_the_wrong_power_of_three",
     "SRC16_the_endpoint_coordinate_follows_its_skew_product_recurrence",
     ("    return Fraction(prefix_endpoint(kappa), 3 ** len(kappa))",
      "    return Fraction(prefix_endpoint(kappa), 3 ** (len(kappa) + 1))")),
    ("A09_correction_uses_the_wrong_multiple_of_x",
     "SRC16_the_correction_coordinate_is_the_affine_offset_normalized",
     ("    return z_coord(kappa) - 2 * x_coord(kappa)",
      "    return z_coord(kappa) - x_coord(kappa)")),
    ("A10_lift_flux_normalizes_by_the_wrong_power",
     "SRC16_the_lift_flux_balance_is_an_exact_identity",
     ("    return Fraction(lift_digit(kappa[:m + 1]), 1 << kappa[m])",
      "    return Fraction(lift_digit(kappa[:m + 1]), 1 << (kappa[m] + 1))")),
    ("A11_anchor_height_is_not_the_source",
     "SRC16_the_anchor_height_is_monotone_and_bounded_only_when_it_settles",
     ("def anchor_height(kappa: tuple[int, ...]) -> int:\n    \"\"\"§23: A_m = 2^{K_m+1} X_m = R_m — faithful, monotone, and noncompact.\"\"\"\n    return source_residue(kappa)",
      "def anchor_height(kappa: tuple[int, ...]) -> int:\n    \"\"\"§23: A_m = 2^{K_m+1} X_m = R_m — faithful, monotone, and noncompact.\"\"\"\n    return source_residue(kappa) % 1024")),
    ("A12_negative_completion_loses_its_sign",
     "SRC16_the_negative_completion_shares_the_whole_finite_code",
     ("    return Fraction(-(2 ** K + offset(kappa)), 3 ** len(kappa))",
      "    return Fraction(2 ** K + offset(kappa), 3 ** len(kappa))")),
    ("A13_critical_completion_starts_from_the_wrong_index",
     "SRC16_every_subcritical_prefix_extends_to_a_critical_completion",
     ("    return kappa + tuple(floor_beta(m + j) - floor_beta(m + j - 1)\n"
      "                         for j in range(1, extra + 1))",
      "    return kappa + tuple(floor_beta(j) - floor_beta(j - 1)\n"
      "                         for j in range(1, extra + 1))")),
    ("A14_v2_rational_reads_the_denominator",
     "SRC16_the_negative_completion_shares_the_whole_finite_code",
     ("    n = x.numerator\n    return (n & -n).bit_length() - 1",
      "    n = x.denominator\n    return (n & -n).bit_length() - 1")),
]

TOOL_DEFECTS = [
    # the other bug made while writing this run
    ("T01_flux_balance_telescopes_over_the_wrong_range",
     "SRC16_the_lift_flux_balance_is_an_exact_identity",
     ("                rhs = (sum((1 - Fraction(1, 2 ** kappa[m])) * A.x_coord(kappa[:m])\n"
      "                           for m in range(M)) / M\n"
      "                       + (A.x_coord(kappa[:M]) - A.x_coord(())) / M)",
      "                rhs = (sum((1 - Fraction(1, 2 ** kappa[m])) * A.x_coord(kappa[:m + 1])\n"
      "                           for m in range(M)) / M\n"
      "                       + (A.x_coord(kappa[:M + 1]) - A.x_coord(kappa[:1])) / M)")),
    ("T02_the_amplification_law_uses_the_wrong_power",
     "SRC16_a_source_lift_amplifies_to_twice_it_times_three_to_the_m",
     ("if E_tilde - E != 2 * t * 3 ** m:", "if E_tilde - E != 2 * t * 3 ** (m - 1):")),
    ("T03_the_correction_recurrence_forgets_its_source_term",
     "SRC16_the_correction_recurrence_does_not_mention_the_lift",
     ("                rhs = (A.correction_coord(kappa[:m])\n"
      "                       + Fraction(1, 3 ** (m + 1))) / 2 ** q",
      "                rhs = A.correction_coord(kappa[:m]) / 2 ** q")),
    # A mutation that makes a check VACUOUS is invisible to a drill — a vacuous
    # check passes. So this one makes it compare against the wrong cylinder.
    ("T04_the_decoupling_baseline_comes_from_the_wrong_prefix",
     "SRC16_the_correction_is_the_same_for_every_source_in_a_cylinder",
     ("                base = A.correction_coord(pre)",
      "                base = A.correction_coord(pre[:-1])")),
    ("T05_the_synchronization_cap_is_transcribed_loosely",
     "SRC16_the_correction_obeys_the_exponential_synchronization_bound",
     ("                cap = Fraction(1, 2 ** m) * (1 - Fraction(2 ** m, 3 ** m))",
      "                cap = Fraction(1, 2 ** (m + 1)) * (1 - Fraction(2 ** m, 3 ** m))")),
    ("T06_the_mean_bracket_drops_its_lower_half",
     "SRC16_mean_lift_is_bracketed_by_mean_source_height",
     ("            if not (xb / 2 - bdry <= lb <= xb + bdry):",
      "            if not (xb - bdry <= lb <= xb + bdry):")),
    ("T07_the_collapse_check_never_looks_at_the_flux",
     "SRC16_every_positive_anchor_collapses_to_the_same_boundary_point",
     ("            settled = all(x == 0 for x in lam[20:])",
      "            settled = all(x == 0 for x in lam[0:])")),
    ("T08_the_sparse_bound_uses_the_wrong_mean_exponent",
     "SRC16_the_sparse_lift_counting_bound_holds",
     ("            cap = 2 ** R * lb + qbar / R", "            cap = 2 ** R * lb / 100 + qbar / (R * 100)")),
    ("T09_the_flux_measurement_reads_a_genuine_anchor",
     "SRC16_the_au1_countermodel_has_positive_lift_flux",
     ("        mech = A.mechanical_code(FLUX_M)\n        rows = []",
      "        mech = A.accel_code(27, FLUX_M)\n        rows = []")),
    ("T10_the_separation_compares_the_countermodel_to_itself",
     "SRC16_the_compact_coordinate_separates_anchors_from_the_countermodel",
     ('for label, kappa in [("27", A.accel_code(27, 60)),',
      'for label, kappa in [("27", A.mechanical_code(60)),')),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_unproved_ledger",
     "SRC16_the_paper_keeps_an_explicit_proved_and_unproved_ledger", "ledger"),
    ("D02_unproved_list_drops_the_conjecture",
     "SRC16_the_paper_lists_casp_cst_and_collatz_as_unproved", "collatz"),
    ("D03_paper_hides_its_quantifier_gap",
     "SRC16_the_paper_marks_its_own_quantifier_gap", "gap"),
    ("D04_route_map_loses_a_successor_route",
     "SRC16_the_route_map_and_the_paper_agree_on_the_next_routes", "routemap"),
    ("D05_bundle_edits_the_reshipped_predecessor",
     "SRC16_the_bundle_reships_its_predecessors_unedited", "reship"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"ledger": AU2A, "collatz": AU2A, "gap": AU2A,
           "routemap": ROUTEMAP, "reship": PRED}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    if kind == "ledger":
        t = t.replace("## 未證", "## 附註", 1)
    elif kind == "collatz":
        head, _, tail = t.partition("## 未證")
        t = head + "## 未證" + tail.replace("Collatz conjecture", "後續工作", 1)
    elif kind == "gap":
        t = t.replace("\\not\\Rightarrow", "\\Rightarrow")
    elif kind == "routemap":
        t = t.replace("Sparse Lift Rigidity", "Sparse Lift Note")
    elif kind == "reship":
        t = t + "\n<!-- edited inside the AU2a bundle -->\n"
    keep[name] = t.encode("utf-8")
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def audit(baseline: dict) -> list[str]:
    """Every check must have a defect naming it, and every target must exist."""
    targeted = ({t for _, t, _ in ACCEL_DEFECTS} | {t for _, t, _ in TOOL_DEFECTS}
                | {t for _, t, _ in DOC_DEFECTS})
    names = set(baseline.get("checks", {}))
    return sorted([f"unguarded check: {c}" for c in names - targeted]
                  + [f"defect names a check that does not exist: {t}"
                     for t in targeted - names])


def main() -> int:
    rep = {
        "tool": "src16_drill.py",
        "subject": "src16_hardzeta_au2a_recheck.py and the A-U.2a layer of "
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

        mod = "_drill_accel_null16"
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
        "defects_in_the_au2a_layer": len(ACCEL_DEFECTS),
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
