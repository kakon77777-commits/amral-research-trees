"""Mutation drill for src07_hardzeta_round01_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The interesting surface here is `hz_chart_algebra.py`. That file is not my
derivation — it is **Round 01's formulas rendered executable**, copied from the
paper without rearrangement. So mutating it asks the question that matters:

> if the paper's recursion were wrong in this specific way, would the brute-force
> confrontation notice?

Twelve of the defects below damage exactly one formula each — a child residue, an
affine offset, the hard-height minimum, the cap boundary, the zone thresholds,
the Hurwitz correction terms. The remaining defects damage the documents and the
recheck's own derived bound.

A defect counts as caught only if **the check named for it** fails. Breaking the
recursion turns almost everything red at once, so "the run went red" would be
worthless here — more so than in any earlier drill in this tree.

Usage:  python code/src07_drill.py <measured.json>
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
TOOL = CODE / "src07_hardzeta_round01_recheck.py"
ALGEBRA = CODE / "hz_chart_algebra.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_I_Round_01_bundle.zip"
ROUND01 = "Hard_Zeta_Phase_I_Round_01_Exact_Refinement_v0.1.md"
TIMEOUT_S = 900


# ------------------------------------- defects in the paper's own formulas
ALGEBRA_DEFECTS = [
    ("A01_U_child_residue_uses_the_wrong_parity",
     "SRC07_cylinders_are_exactly_the_starts_with_that_parity_word",
     ('r_U = w.r + q * (1 - p)', 'r_U = w.r + q * p')),
    # b_w enters only through the cap and the children's b, never through the
    # block identity, which uses m and u. And the arithmetic floor check cannot
    # see a wrong b either — c is derived FROM b, so d*c <= b < d*(c+1) stays
    # true. Only the probe against real iteration can tell.
    ("A02_U_child_affine_offset_off_by_a_factor",
     "SRC07_new_prefix_hard_cap_is_exactly_the_descent_boundary",
     ('u_U, b_U = w.u + 1, 3 * w.b + q', 'u_U, b_U = w.u + 1, 3 * w.b + 2 * q')),
    ("A03_U_child_forgets_to_count_the_up_step",
     "SRC07_the_chart_algebra_evaluates_without_error",
     ('u_U, b_U = w.u + 1, 3 * w.b + q', 'u_U, b_U = w.u, 3 * w.b + q')),
    ("A04_U_child_target_base_numerator_wrong",
     "SRC07_block_identity_holds_with_the_charts_own_m_and_u",
     ('num_U = 3 * (w.m + 3 ** w.u * (1 - p)) + 1',
      'num_U = 3 * (w.m + 3 ** w.u * (1 - p)) + 3')),
    ("A05_hard_height_drops_the_parents_constraint",
     "SRC07_recursive_hard_height_reproduces_the_hard_set_exactly",
     ('h = c if w.h is None else min(w.h, c)', 'h = c')),
    ("A06_hard_cap_boundary_off_by_one",
     "SRC07_the_cap_is_exactly_the_floor_of_b_over_delta",
     ('    return b // delta if delta > 0 else None',
      '    return b // delta + 1 if delta > 0 else None')),
    # Shifting the stratum floor by one is a NO-OP: the cylinder has spacing
    # 2^(k+1), so every threshold in (c_v, next member] selects the same set.
    # The defect planted instead drops the parent's hard height, which does
    # change the set — an honest mutation rather than one that tests nothing.
    ("A07_first_descent_stratum_ignores_the_parents_hard_height",
     "SRC07_first_descent_stratum_is_exactly_sigma_equals_k_plus_1",
     ('    top = hi if parent.h is None else min(hi, parent.h)',
      '    top = hi')),
    ("A08_drift_gap_sign_flipped",
     "SRC07_the_chart_algebra_evaluates_without_error",
     ('    return 2 ** k - 3 ** u', '    return 3 ** u - 2 ** k')),
    ("A09_zone_A_threshold_loosened",
     "SRC07_every_chart_falls_in_exactly_one_zone",
     ('    if 3 ** (u + 1) < 2 ** (k + 1):', '    if 3 ** u < 2 ** (k + 1):')),
    # Callers all pass lo >= 2, which forces A >= 1 on its own, so this guard
    # was dead code and the drill came back silent. hz_chart_algebra's anchors
    # now call with lo = 0, which makes it load-bearing somewhere.
    ("A10_AP_mass_forgets_to_skip_n_equals_zero",
     "SRC07_hurwitz_zeta_and_AP_mass_anchors_hold",
     ('    a_pos = 1 if r == 0 else 0', '    a_pos = 0')),
    ("A11_hurwitz_euler_maclaurin_corrections_dropped",
     "SRC07_hurwitz_zeta_and_AP_mass_anchors_hold",
     ('    for j in range(1, corrections + 1):', '    for j in range(1, 1):')),
    ("A12_chart_mass_includes_n_equals_1",
     "SRC07_chart_mass_formula_matches_direct_summation",
     ('        return ap_dirichlet_mass(s, 2 ** self.k, self.r, 2, self.h)',
      '        return ap_dirichlet_mass(s, 2 ** self.k, self.r, 1, self.h)')),
    ("A13_U_k_chart_wrongly_given_a_finite_height",
     "SRC07_U_k_residue_and_closed_form_mass_are_as_stated",
     ('            h = w.h                                           # c = +infinity',
      '            h = 10 ** 9 if w.h is None else w.h')),
]

# ------------------------------------------------------- defects in the documents
DOC_DEFECTS = [
    ("D01_loose_file_diverges_from_the_bundled_copy",
     "SRC07_loose_round01_matches_the_bundled_copy",
     "loose"),
    ("D02_paper_loses_the_scope_limit_on_its_own_no_go",
     "SRC07_paper_states_the_no_go_is_per_chart_not_global",
     "scope"),
    ("D03_paper_loses_the_domain_correction",
     "SRC07_paper_carries_the_n_at_least_2_domain_correction",
     "domain"),
    ("D04_bundle_no_longer_carries_the_route_paper",
     "SRC07_bundle_also_carries_the_v011_route_paper",
     "route"),
]

# ------------------------------------------ defects in the recheck's own reasoning
TOOL_DEFECTS = [
    ("T01_admissible_stopping_times_shifted",
     "SRC07_hazard_vanishes_exactly_at_inadmissible_stopping_times",
     ('        out.add(p.bit_length())', '        out.add(p.bit_length() + 1)')),
    ("T02_hazard_budget_asserted_tighter_than_it_is",
     "SRC07_hazard_accumulation_respects_the_single_hard_value_budget",
     ('                budget = math.log(exact_Z[k0][s] * n0 ** s)',
      '                budget = math.log(exact_Z[k0][s] * n0 ** s) / 50')),
    # The first version mutated a single-endpoint restatement of the identity and
    # was NOT caught: that endpoint is depth 22, one of the zero-hazard levels, so
    # Z_21 = Z_22 and the wrong index made no difference. The phenomenon this run
    # is about defeated the drill for this run. The redundant line is gone and the
    # mutation now lands on the telescoping test, which visits every endpoint
    # including the ones where the hazard is real.
    ("T03_cumulative_hazard_compared_against_the_wrong_ratio",
     "SRC07_cumulative_hazard_equals_the_log_ratio_of_Z",
     ('                        gap = math.log(exact_Z[k0][s] / exact_Z[K2][s])',
      '                        gap = math.log(exact_Z[k0][s] / exact_Z[K2 - 1][s])')),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    if kind == "loose":
        p = src / ROUND01
        p.write_text(p.read_text(encoding="utf-8").replace("Neo.K", "Neo.Q", 1),
                     encoding="utf-8")
        return
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    if kind == "scope":
        keep[ROUND01] = keep[ROUND01].decode("utf-8").replace(
            "但這**不排除**", "但這也排除", 1).encode("utf-8")
    elif kind == "domain":
        keep[ROUND01] = keep[ROUND01].decode("utf-8").replace(
            r"\widetilde H_w:=H_w\cap[2,\infty)",
            r"\widetilde H_w:=H_w", 1).encode("utf-8")
    elif kind == "route":
        keep = {n: b for n, b in keep.items()
                if "Faithful_Global_Quantifier_Compression" not in n}
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)
    if kind in ("scope", "domain"):
        (src / ROUND01).write_bytes(keep[ROUND01])


def main() -> int:
    measured = pathlib.Path(sys.argv[1])
    rep = {
        "tool": "src07_drill.py",
        "subject": "src07_hardzeta_round01_recheck.py and hz_chart_algebra.py",
        "why": ("hz_chart_algebra.py is Round 01's formulas rendered executable, "
                "so damaging one formula at a time asks whether the brute-force "
                "confrontation would notice if the paper's recursion were wrong"),
        "defects": {},
        "controls": {},
    }
    original_algebra = ALGEBRA.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir: pathlib.Path, tool: pathlib.Path,
            algebra_module: str = "hz_chart_algebra") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ALGEBRA_MODULE": algebra_module}
        out = subprocess.run([sys.executable, str(tool), str(measured)],
                             capture_output=True, text=True, encoding="utf-8",
                             timeout=TIMEOUT_S, env=env)
        try:
            return json.loads(out.stdout)
        except json.JSONDecodeError:
            return {"ok": False, "checks": {},
                    "_crash": (out.stdout + out.stderr)[-400:]}

    def record(name: str, target: str, res: dict) -> None:
        checks = res.get("checks", {})
        rep["defects"][name] = {
            "target_check": target,
            "caught_by_the_named_check": target in checks and not checks[target]["pass"],
            "run_went_red": not res.get("ok", True),
            "other_checks_that_also_fired": sorted(
                k for k, v in checks.items() if not v["pass"] and k != target),
            **({"crash": res["_crash"]} if "_crash" in res else {}),
        }

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        base_src = tmp / "source"
        base_src.mkdir()
        for nm in (BUNDLE, ROUND01):
            shutil.copy2(SOURCE / nm, base_src / nm)

        baseline = run(base_src, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

        # --- the paper's formulas
        for name, target, (old, new) in ALGEBRA_DEFECTS:
            if old not in original_algebra:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} not present; nothing was tested"}
                continue
            mod = f"_drill_algebra_{name}"
            f = CODE / f"{mod}.py"
            try:
                f.write_text(original_algebra.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base_src, TOOL, mod))
            finally:
                f.unlink(missing_ok=True)

        # --- the documents
        for name, target, kind in DOC_DEFECTS:
            s = tmp / f"src_{name}"
            shutil.copytree(base_src, s)
            mutate_docs(s, kind)
            record(name, target, run(s, TOOL))
            shutil.rmtree(s, ignore_errors=True)

        # --- the recheck's own reasoning
        for name, target, (old, new) in TOOL_DEFECTS:
            if old not in original_tool:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} not present; nothing was tested"}
                continue
            f = CODE / f"_drill_mutant_{name}.py"
            try:
                f.write_text(original_tool.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base_src, f))
            finally:
                f.unlink(missing_ok=True)

        # --- controls
        mod = "_drill_algebra_null"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original_algebra + "\n# a comment nothing reads\n",
                         encoding="utf-8")
            res = run(base_src, TOOL, mod)
        finally:
            f.unlink(missing_ok=True)
        rep["controls"]["N01_algebra_annotated_where_nothing_reads"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

        s = tmp / "src_null"
        shutil.copytree(base_src, s)
        (s / "UNREAD_SCRATCH.txt").write_text("read by nothing\n", encoding="utf-8")
        res = run(s, TOOL)
        rep["controls"]["N02_unrelated_file_beside_the_documents"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(rep["defects"]),
        "defects_caught_by_the_named_check": caught,
        "defects_in_the_papers_own_formulas": len(ALGEBRA_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
