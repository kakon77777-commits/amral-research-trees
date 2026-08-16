"""Mutation drill for src21_hardzeta_au2e_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

This round's checks split cleanly in two, and the drill has to treat them
differently.

The exact identities — the deviation identity, the directional split, the reset
affine identity, the first-return bound — are tight, so almost any damage to the
definitions turns them red. Those get ordinary defects.

The two *inequalities* do not behave that way. Measured before the drill was
written: J_N runs 0.55 to 0.69 of N on real spines, while the packing floor
(N-2r)/r lands between 0.08 and 1.50. No perturbation of the bound, the peak, or
the exponent can push a measured J_N of 15..54 below a floor of 1.5. **The
packing inequality cannot be made to fail at these sizes.** That is a fact about
the round, not about the drill, and it is precisely the class of check a mutation
drill is blind to — a vacuous check passes, so it never goes red.

The response is the one the earlier rounds settled on: the falsifiable content is
moved into checks that *can* fail and those are what get drilled.

  - SRC21_..._are_one_line asserts the algebraic equivalence between the
    contamination cap and the packing floor, with both outcomes required to occur.
  - SRC21_..._different_finite_quality asserts the measured quality itself:
    fraction_pinned below 0.25, saturation above 0.5.
  - SRC21_..._packing_bound_holds keeps its own defect on the separation
    *precondition*, which is checkable; its inequality is not.

Every check must have at least one defect naming it; `audit()` enforces that
before the mutation loop runs. No defect loosens a comparison.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src21_drill.py
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
TOOL = CODE / "src21_hardzeta_au2e_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_II_Round_AU2e_bundle.zip"
AU2E = "Hard_Zeta_Phase_II_Round_AU2e_Multiscale_Return_Arithmetic_v0.1.md"
ROUTEMAP = "Hard_Zeta_A_Line_ROUTE_MAP_v1.5_AU2e.md"
AU2B1 = "Hard_Zeta_Phase_II_Round_AU2b1_Sharp_Packing_Entropy_Threshold_v0.1.md"
COMPANIONS = ["Hard_Zeta_Phase_II_Round_AU2b3_bundle.zip"]
TIMEOUT_S = 900

ACCEL_DEFECTS = [
    ("A01_the_mechanical_word_is_read_one_step_ahead",
     "SRC21_the_deficit_increment_is_the_mechanical_deviation",
     ("    return floor_beta(m) - floor_beta(m - 1)",
      "    return floor_beta(m + 1) - floor_beta(m)")),
    ("A02_the_deviation_forgets_the_absolute_value",
     "SRC21_the_deviation_is_the_deficit_paths_total_variation",
     ("    V = sum(abs(q[i] - a[i]) for i in range(N))",
      "    V = sum(q[i] - a[i] for i in range(N))")),
    ("A03_the_downward_variation_counts_the_agreements_too",
     "SRC21_the_two_directions_reconstruct_the_deficit_and_its_variation",
     ("    W = sum(max(q[i] - a[i], 0) for i in range(N))",
      "    W = sum(max(q[i] - a[i], 0) + (q[i] == a[i]) for i in range(N))")),
    ("A04_a_skipped_credit_is_read_as_a_spent_one",
     "SRC21_the_upward_variation_counts_exactly_the_skipped_credits",
     ("               if mechanical_valuation(m) == 2 and q[m - 1] == 1)",
      "               if mechanical_valuation(m) == 2 and q[m - 1] == 2)")),
    # The Sturmian claim is about mechanical_code, which builds from floor_beta
    # directly rather than through mechanical_valuation — so A01 does not reach
    # it and this defect is not redundant with it.
    ("A05_the_mechanical_word_picks_up_a_third_symbol",
     "SRC21_the_mechanical_word_has_complexity_r_plus_one",
     ("    return tuple(floor_beta(j) - floor_beta(j - 1) for j in range(1, m + 1))",
      "    return tuple(floor_beta(j) - floor_beta(j - 1) + (j % 97 == 0)\n"
      "                 for j in range(1, m + 1))")),
    ("A06_the_deficit_record_takes_the_smallest_excursion",
     "SRC21_the_peak_exponent_is_bounded_by_the_deficit_record_and_log_n",
     ("    return max(deficit(n, m) for m in range(1, N + 1))",
      "    return min(deficit(n, m) for m in range(1, N + 1))")),
    ("A07_the_reset_identity_misplaces_a_power_of_three",
     "SRC21_the_reset_affine_identity_holds_in_exact_integers",
     ("           + sum(3 ** (b - 1 - i) * 2 ** K[i] for i in range(a, b)))",
      "           + sum(3 ** (b - i) * 2 ** K[i] for i in range(a, b)))")),
    ("A08_the_slack_test_subtracts_the_threshold",
     "SRC21_the_first_return_reset_bound_holds_in_exact_integers",
     ("    return 3 ** (m * h_den) > 2 ** (K * h_den + h_num)",
      "    return 3 ** (m * h_den) > 2 ** (K * h_den - h_num)")),
]

TOOL_DEFECTS = [
    # Measured first: dropping the r factor breaks 7 of the 42 rows, at r = 5
    # and r = 6. Scaling J instead is a NO-OP — the cap has 3.6x to 9.4x of
    # slack, so it cannot detect even a halving of the mismatch count.
    ("T01_the_contamination_cap_charges_each_mismatch_once",
     "SRC21_the_factor_complexity_obeys_the_contamination_bound",
     ("                cap = (r + 1) + r * J", "                cap = (r + 1) + J")),
    ("T02_the_informative_column_reads_the_complexity_not_the_cap",
     "SRC21_the_contamination_bound_and_the_packing_floor_are_one_line",
     ('                             "informative": cap < trivial_ceiling,',
      '                             "informative": p < trivial_ceiling,')),
    # The packing inequality itself is not breakable here (see the module
    # docstring). What IS checkable is that the tool verifies the separation
    # hypothesis 2^{r+1} > M_N instead of assuming it.
    ("T03_the_separation_hypothesis_is_tested_one_bit_short",
     "SRC21_the_mismatch_packing_bound_holds_on_real_spines",
     ("            if not 2 ** (r_N + 1) > M_N:", "            if not 2 ** (r_N - 1) > M_N:")),
    ("T04_the_monotone_stretch_looks_for_the_opposite_skip",
     "SRC21_on_a_nondecreasing_stretch_every_mismatch_is_a_skipped_credit",
     ("                              if A.mechanical_valuation(m) == 2 and q[m - 1] == 1)",
      "                              if A.mechanical_valuation(m) == 1 and q[m - 1] == 2)")),
    ("T05_the_rising_step_scan_stops_after_the_first_move",
     "SRC21_a_nonincreasing_nonnegative_integer_deficit_would_be_constant",
     ("            if any(A.deficit(n, m + 1) > A.deficit(n, m) for m in range(1, N)):",
      "            if any(A.deficit(n, m + 1) > A.deficit(n, m) for m in range(1, 2)):")),
    ("T06_the_local_valuation_drops_a_step",
     "SRC21_a_deficit_drop_is_exactly_a_locally_contracting_block",
     ("                    contracts = 3 ** (b - a) < 2 ** (K[b] - K[a])",
      "                    contracts = 3 ** (b - a) < 2 ** (K[b] - K[a] - 1)")),
    # NOT "drop the (b-a) factor" — measured to be a no-op, because the
    # contraction term alone already bounds Y_b at all 190 windows. That fact now
    # has its own check, and T07b below is the defect that names it.
    ("T07_the_first_return_threshold_enters_with_the_wrong_sign",
     "SRC21_the_first_return_reset_bound_holds_in_exact_integers",
     ("                    contraction = 3 * 2 ** (h + K[a]) * Y[a]\n"
      "                    rhs = contraction + 3 ** a * (b - a)",
      "                    contraction = 3 * 2 ** (K[a] - h) * Y[a]\n"
      "                    rhs = contraction + 3 ** a * (b - a)")),
    ("T07b_the_correction_weight_is_measured_against_the_full_bound",
     "SRC21_the_affine_correction_never_carries_the_first_return_bound",
     ("                    contraction = 3 * 2 ** (h + K[a]) * Y[a]\n"
      "                    tested += 1",
      "                    contraction = 3 * 2 ** (h + K[a]) * Y[a] // 2\n"
      "                    tested += 1")),
    ("T08_the_unproved_list_is_read_from_the_proved_section",
     "SRC21_the_paper_lists_casp_terras_and_collatz_as_unproved",
     ('        tail = au2e[au2e.find("### 未證"):] if "### 未證" in au2e else ""',
      '        tail = au2e[au2e.find("### 已證"):au2e.find("### 未證")] '
      'if "### 未證" in au2e else ""')),
    ("T09_the_regimes_are_looked_for_in_the_route_map",
     "SRC21_the_paper_states_its_dichotomy_as_two_named_regimes",
     ('        return (("Regime M" in au2e and "Regime R" in au2e\n'
      '                 and "One-Sided Deficit Dichotomy" in au2e), {})',
      '        return (("Regime M" in routemap and "Regime R" in routemap\n'
      '                 and "One-Sided Deficit Dichotomy" in routemap), {})')),
    ("T10_the_route_map_successors_are_sought_in_the_paper",
     "SRC21_the_route_map_carries_the_same_three_successors",
     ('        missing = [w for w in want if w not in routemap]\n'
      '        return (not missing and len(routemap) > 500)',
      '        missing = [w for w in want if w not in routemap]\n'
      '        return (not missing and len(routemap) > 500000)')),
    ("T11_the_provenance_check_flags_every_file_as_edited",
     "SRC21_whatever_the_trimmed_bundle_reships_is_unedited",
     ("        edited = [n for n, h in big.items() if n in prev and prev[n] != h]",
      "        edited = [n for n in big]")),
    ("T12_the_quality_measure_reads_the_slack_instead_of_the_fraction",
     "SRC21_the_rounds_three_inequalities_have_different_finite_quality",
     ('        pinned = [r["fraction_pinned"] for r in pack if r["fraction_pinned"]]',
      '        pinned = [r["slack"] for r in pack if r["slack"]]')),
]

DOC_DEFECTS = [
    ("D01_the_unproved_ledger_loses_the_conjecture_itself",
     "SRC21_the_paper_lists_casp_terras_and_collatz_as_unproved", "unproved"),
    ("D02_the_dichotomy_loses_one_of_its_two_regimes",
     "SRC21_the_paper_states_its_dichotomy_as_two_named_regimes", "regime"),
    ("D03_the_route_map_drops_the_transducer_route",
     "SRC21_the_route_map_carries_the_same_three_successors", "successor"),
    ("D04_a_reshipped_predecessor_is_edited_in_place",
     "SRC21_whatever_the_trimmed_bundle_reships_is_unedited", "reship"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    key = {"unproved": AU2E, "regime": AU2E, "successor": ROUTEMAP,
           "reship": AU2B1}[kind]
    name = next(n for n in keep if pathlib.PurePosixPath(n).name == key)
    t = keep[name].decode("utf-8")
    before = t
    if kind == "unproved":
        head, sep, tail = t.partition("### 未證")
        t = head + sep + tail.replace("Collatz", "the conjecture")
    elif kind == "regime":
        t = t.replace("Regime R", "the other case", 1)
    elif kind == "successor":
        t = t.replace("A-U.2d", "a later route")
    elif kind == "reship":
        t = t.replace("\n", "\n", 1) + "\n<!-- edited in place -->\n"
    if t == before:
        raise SystemExit(f"doc mutation {kind!r} changed nothing; anchor is stale")
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
        "tool": "src21_drill.py",
        "subject": "src21_hardzeta_au2e_recheck.py and the A-U.2e layer of "
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

        mod = "_drill_accel_null21"
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
