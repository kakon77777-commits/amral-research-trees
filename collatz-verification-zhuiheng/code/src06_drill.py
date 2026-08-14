"""Mutation drill for src06_hardzeta_origin_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The recheck has three kinds of input, so the drill plants defects in all three:

  * the **measurement** — a damaged copy of the Z_k JSON;
  * the **documents** — damaged copies of the v0.1 bundle, v0.1.1 and the SSSP
    research_program text, reached through the recheck's path overrides;
  * the recheck's **own inline arguments** — the two-case proof that
    sigma(n) != 3, and the non-monotone counterexample, mutated in its source.

The third surface matters most. Those two are the only places in this suite where
the tool reasons rather than compares, and a check that agrees with its own
expectation is exactly the shape this tree has been bitten by before.

A defect counts as caught only if **the check named for it** fails. Almost any
edit to the measurement also disturbs the monotonicity checks, so "the run went
red" would hand back catches for the wrong reason.

Usage:  python code/src06_drill.py <measured.json> <small.json>
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOL = ROOT / "code" / "src06_hardzeta_origin_recheck.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
SSSP = (ROOT.parent / "collatz-ot-series-neok"
        / "Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0")
BUNDLE = "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1_bundle.zip"
V011 = "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1.1.md"
PAPER = "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1.md"
MAP = "Faithful_Global_Quantifier_Compression_ROUTE_MAP_v0.1.md"
TIMEOUT_S = 900

# a stub standing in for the measurer, used only to drill the containment check
STUB = '''import json, sys
a = dict(zip(sys.argv[1::2], sys.argv[2::2]))
k = int(a["--ks"])
print(json.dumps({"tool": "stub", "domain_lo": 2, "domain_hi": int(a["--to"]),
                  "scanned": 0, "max_sigma": 0, "max_sigma_at": 0, "sigma_cap": k + 1,
                  "rows": [{"k": k, "count_E_k": 10 ** 12, "min_E_k": 27,
                            "z": {"2": 1.0}}]}))
'''


# --------------------------------------------------------- measurement defects
def rows_of(d):
    return {r["k"]: r for r in d["rows"]}


def m01(d, _t):  # counts rise with k
    rows_of(d)[64]["count_E_k"] = rows_of(d)[32]["count_E_k"] + 1


def m02(d, _t):  # Z rises with k
    rows_of(d)[64]["z"]["3"] = rows_of(d)[32]["z"]["3"] * 2


def m03(d, _t):  # sigma = 3 suddenly occurs
    rows_of(d)[3]["count_E_k"] -= 1


def m04(d, _t):  # Z_2 != Z_3
    for s in rows_of(d)[3]["z"]:
        rows_of(d)[3]["z"][s] *= (1 - 1e-12)


def m05(d, _t):  # max sigma disagrees with the engine
    d["max_sigma"] += 1


def m06(d, _t):  # argmax points somewhere python can refute
    d["max_sigma_at"] = 3


def m07(d, _t):  # a reported minimum is not hard at that depth
    rows_of(d)[32]["min_E_k"] = 4


def m08(d, _t):  # a gap of 3 between occurring stopping times
    r = rows_of(d)
    for k in (13, 14):
        r[k]["count_E_k"] = r[12]["count_E_k"]


def m09(d, _t):  # an inadmissible stopping time occurs
    r = rows_of(d)
    r[6]["count_E_k"] = r[5]["count_E_k"] - 1000


def m10(d, _t):  # measured sum falls below its own exact floor
    rows_of(d)[16]["z"]["2"] = 0.0


def m11(d, _t):  # nothing ever decreases strictly
    r = rows_of(d)
    base = r[1]["z"]
    for row in d["rows"]:
        row["z"] = dict(base)


def s01(d, _t):  # the fsum cross-check target is perturbed (small file)
    rows_of(d)[8]["z"]["3"] *= 1.001


# ------------------------------------------------------------ document defects
def rewrite_bundle(tree: pathlib.Path, paper=None, route_map=None) -> None:
    src = tree / BUNDLE
    with zipfile.ZipFile(src) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    if paper:
        keep[PAPER] = paper(keep[PAPER].decode("utf-8")).encode("utf-8")
    if route_map:
        keep[MAP] = route_map(keep[MAP].decode("utf-8")).encode("utf-8")
    with zipfile.ZipFile(src, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def d01(src, _sssp):  # the body loses the monotonicity hypothesis
    rewrite_bundle(src, paper=lambda t: t.replace(
        r"C_k(x)\Rightarrow C_{k+1}(x)", r"C_k(x)\Rightarrow C_k(x)"))


def d02(src, _sssp):  # the map carries it after all
    rewrite_bundle(src, route_map=lambda t: t.replace(
        "## 已完成的一般橋", "## 已完成的一般橋（monotone certificate system）"))


def d03(src, _sssp):  # v0.1 already has the restricted form
    rewrite_bundle(src, paper=lambda t: t.replace(
        r"\bigsqcup_{|w|=k}H_w", r"\bigsqcup_{|w|=k}\widetilde H_w"))


def d04(src, _sssp):  # v0.1.1 loses its corrigendum section
    p = src / V011
    p.write_text(p.read_text(encoding="utf-8").replace(
        "## v0.1.1 Domain Corrigendum", "## 附註"), encoding="utf-8")


def d05(src, _sssp):  # v0.1.1 fixed both unions, leaving nothing for v0.1.2
    p = src / V011
    p.write_text(p.read_text(encoding="utf-8").replace(
        r"\bigsqcup_{|w|=k}H_w", r"\bigsqcup_{|w|=k}\widetilde H_w"), encoding="utf-8")


def d06(src, _sssp):  # v0.1.1 no longer matches the SSSP original
    p = src / V011
    p.write_text(p.read_text(encoding="utf-8").replace("Neo.K", "Neo.Q", 1),
                 encoding="utf-8")


def d07(_src, sssp):  # v0.1.2 keeps a bare union
    p = next((sssp / "research_program").glob("*.md"))
    p.write_text(p.read_text(encoding="utf-8").replace(
        r"\bigsqcup_{|w|=k}\widetilde H_w", r"\bigsqcup_{|w|=k}H_w", 1),
        encoding="utf-8")


def d08(_src, sssp):  # v0.1.2 still carries the corrigendum as an appendix
    p = next((sssp / "research_program").glob("*.md"))
    p.write_text(p.read_text(encoding="utf-8") + "\n## v0.1.1 Domain Corrigendum\n",
                 encoding="utf-8")


# -------------------------------------------------------------- source defects
def t01(code: str) -> str:
    """The two-case proof's second branch is misstated."""
    return code.replace("            t2 = (9 * n + 5) // 4",
                        "            t2 = (9 * n + 5) // 16", 1)


def t02(code: str) -> str:
    """The counterexample is made monotone, so it stops being one."""
    return code.replace("        return k % 2 == 0", "        return True", 1)


def t03(code: str) -> str:
    """The admissible-stopping-time boundary is off by one.

    The first version of this defect swapped the exact `bit_length()` for a float
    logarithm — and was NOT caught, because the two agree for every u < 640,
    past where 3**u leaves float range. That is a fact about the scale, not a
    hole in the check, and the recheck's docstring now says so instead of
    claiming the exact route was load-bearing. The defect planted here is the
    slip that would actually change the answer.
    """
    return code.replace("        j = p.bit_length()", "        j = p.bit_length() + 1", 1)


MEASURE_DEFECTS = [
    ("M01_E_k_counts_rise_with_k", "SRC06_E_k_counts_are_non_increasing_in_k", m01),
    ("M02_Z_k_rises_with_k", "SRC06_Z_k_is_non_increasing_in_k_for_every_s", m02),
    ("M03_sigma_equal_to_3_starts_occurring",
     "SRC06_sigma_equals_3_occurs_for_no_n_on_the_range", m03),
    ("M04_Z_2_and_Z_3_differ_by_one_ulp",
     "SRC06_Z_2_equals_Z_3_exactly_so_L_equals_1_admits_no_q_below_1", m04),
    ("M05_max_sigma_off_by_one",
     "SRC06_measurer_max_sigma_agrees_with_the_engine", m05),
    ("M06_argmax_sigma_points_at_3",
     "SRC06_argmax_sigma_reproduces_under_exact_python_iteration", m06),
    ("M07_min_E_k_is_not_hard_at_that_depth",
     "SRC06_reported_minima_of_E_k_are_really_minimal", m07),
    ("M08_a_gap_of_3_between_occurring_stopping_times",
     "SRC06_gaps_between_occurring_stopping_times_are_at_most_2", m08),
    ("M09_an_inadmissible_stopping_time_occurs",
     "SRC06_occurring_stopping_times_are_exactly_the_admissible_ones", m09),
    ("M10_measured_sum_drops_below_its_exact_floor",
     "SRC06_the_exact_lower_bound_sits_inside_the_measured_bracket", m10),
    ("M11_no_step_decreases_strictly",
     "SRC06_most_steps_do_strictly_decrease_so_the_route_is_not_dead", m11),
]

SMALL_DEFECTS = [
    ("S01_kahan_sum_perturbed_in_the_cross_check_range",
     "SRC06_kahan_sums_match_exactly_rounded_python_fsum", s01),
]

DOC_DEFECTS = [
    ("D01_v01_body_loses_the_monotonicity_hypothesis",
     "SRC06_the_paper_body_states_the_monotonicity_hypothesis", d01),
    ("D02_route_map_carries_the_hypothesis_after_all",
     "SRC06_the_route_map_omits_the_hypothesis_the_body_carries", d02),
    ("D03_v01_already_uses_the_restricted_union",
     "SRC06_v01_carries_the_unrestricted_union_twice", d03),
    ("D04_v011_corrigendum_section_removed",
     "SRC06_v011_adds_the_corrigendum_and_the_restricted_chart", d04),
    ("D05_v011_fixed_both_unions",
     "SRC06_v011_fixed_only_one_of_the_two_unrestricted_unions", d05),
    ("D06_v011_no_longer_matches_the_sssp_original",
     "SRC06_v011_is_the_hz_original_inside_the_sssp_package", d06),
    ("D07_v012_keeps_a_bare_union",
     "SRC06_v012_removes_the_last_unrestricted_union", d07),
    ("D08_v012_still_appends_the_corrigendum",
     "SRC06_v012_dissolves_the_corrigendum_into_the_body", d08),
]

SOURCE_DEFECTS = [
    ("T01_the_two_case_proof_is_misstated",
     "SRC06_the_two_case_proof_that_sigma_never_equals_3_holds_pointwise", t01),
    ("T02_the_counterexample_is_made_monotone",
     "SRC06_without_monotonicity_the_bridge_is_false", t02),
    ("T03_admissible_boundary_off_by_one",
     "SRC06_occurring_stopping_times_are_exactly_the_admissible_ones", t03),
]


def null_measure(d, _t):
    d["tool"] = d["tool"] + " (annotated, read by nothing)"


def null_doc(src, _sssp):
    (src / "UNREAD_SCRATCH.txt").write_text("read by nothing\n", encoding="utf-8")


def main() -> int:
    measured_src = pathlib.Path(sys.argv[1])
    small_src = pathlib.Path(sys.argv[2])

    rep = {
        "tool": "src06_drill.py",
        "subject": "src06_hardzeta_origin_recheck.py",
        "surfaces": ["the measurement JSON", "the source and SSSP documents",
                     "the recheck's own inline arguments"],
        "defects": {},
        "controls": {},
    }

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)

        def run(measured: pathlib.Path, small: pathlib.Path,
                src_dir: pathlib.Path, sssp_dir: pathlib.Path,
                tool: pathlib.Path, measure_bin: pathlib.Path | None = None) -> dict:
            env = {**os.environ, "PYTHONUTF8": "1",
                   "HZ_SOURCE_DIR": str(src_dir), "HZ_SSSP_DIR": str(sssp_dir)}
            if measure_bin:
                env["HZ_MEASURE_BIN"] = str(measure_bin)
            out = subprocess.run(
                [sys.executable, str(tool), str(measured), str(small)],
                capture_output=True, text=True, encoding="utf-8", timeout=TIMEOUT_S,
                env=env)
            try:
                return json.loads(out.stdout)
            except json.JSONDecodeError:
                return {"ok": False, "checks": {},
                        "_crash": (out.stdout + out.stderr)[-400:]}

        base_src = tmp / "source"
        base_src.mkdir()
        for nm in (BUNDLE, V011):
            shutil.copy2(SOURCE / nm, base_src / nm)
        base_sssp = tmp / "sssp"
        shutil.copytree(SSSP, base_sssp)

        baseline = run(measured_src, small_src, base_src, base_sssp, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "baseline": baseline}, indent=2, ensure_ascii=False))
            return 2

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

        # --- measurement surface
        for name, target, mutate in MEASURE_DEFECTS:
            d = json.loads(measured_src.read_text(encoding="utf-8"))
            mutate(d, None)
            f = tmp / f"{name}.json"
            f.write_text(json.dumps(d), encoding="utf-8")
            record(name, target, run(f, small_src, base_src, base_sssp, TOOL))

        for name, target, mutate in SMALL_DEFECTS:
            d = json.loads(small_src.read_text(encoding="utf-8"))
            mutate(d, None)
            f = tmp / f"{name}.json"
            f.write_text(json.dumps(d), encoding="utf-8")
            record(name, target, run(measured_src, f, base_src, base_sssp, TOOL))

        # --- document surface
        for name, target, mutate in DOC_DEFECTS:
            s = tmp / f"src_{name}"
            shutil.copytree(base_src, s)
            p = tmp / f"sssp_{name}"
            shutil.copytree(base_sssp, p)
            mutate(s, p)
            record(name, target, run(measured_src, small_src, s, p, TOOL))
            shutil.rmtree(s, ignore_errors=True)
            shutil.rmtree(p, ignore_errors=True)

        # --- the recheck's own reasoning
        original = TOOL.read_text(encoding="utf-8")
        for name, target, mutate in SOURCE_DEFECTS:
            code = mutate(original)
            if code == original:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": "the source mutation did not apply, so nothing was tested"}
                continue
            # The mutant must live beside the original: the recheck derives ROOT
            # from its own __file__, so a copy in a scratch directory loses the
            # engine it cross-checks against and crashes instead of failing the
            # named check — which would score as a catch for entirely the wrong
            # reason.
            f = TOOL.parent / f"_drill_mutant_{name}.py"
            try:
                f.write_text(code, encoding="utf-8")
                record(name, target, run(measured_src, small_src, base_src, base_sssp, f))
            finally:
                f.unlink(missing_ok=True)

        # --- the containment check, via a stub standing in for the measurer
        stub = tmp / "stub_measure.py"
        stub.write_text(STUB, encoding="utf-8")
        record("X01_a_measurer_reporting_more_hard_starts_than_fallbacks",
               "SRC06_E_k_is_contained_in_the_Paper_05_k_block_fallback_set",
               run(measured_src, small_src, base_src, base_sssp, TOOL, stub))

        # --- controls
        d = json.loads(measured_src.read_text(encoding="utf-8"))
        null_measure(d, None)
        f = tmp / "null.json"
        f.write_text(json.dumps(d), encoding="utf-8")
        res = run(f, small_src, base_src, base_sssp, TOOL)
        rep["controls"]["N01_measurement_annotated_where_nothing_reads"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

        s = tmp / "src_null"
        shutil.copytree(base_src, s)
        p = tmp / "sssp_null"
        shutil.copytree(base_sssp, p)
        null_doc(s, p)
        res = run(measured_src, small_src, s, p, TOOL)
        rep["controls"]["N02_unrelated_file_added_beside_the_documents"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(rep["defects"]),
        "defects_caught_by_the_named_check": caught,
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
