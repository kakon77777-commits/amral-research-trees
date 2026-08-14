"""Mutation drill for src09_hardzeta_round03a_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 03-A compresses the coefficient frontier down to one unproved quantity,
`m_k`. Nine of the defects below damage Round 03-A's own formulas — the survivor
condition, the DP recursion, the Beatty schedule, the normalized residue, the
lift assignment, the loss ratio, the head mass, the crossing depth — and each
asks whether the confrontation with direct iteration would notice.

Three more damage the measured `m_k` itself, since it is this run's headline and
a headline nobody drills is a number nobody has checked.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src09_drill.py <tau-records.json>
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
TOOL = CODE / "src09_hardzeta_round03a_recheck.py"
ALGEBRA = CODE / "hz_chart_algebra.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_I_Round_03A_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A_Coefficient_Frontier_v0.1.md"
TIMEOUT_S = 1200

ALGEBRA_DEFECTS = [
    # `>` -> `>=` is a NO-OP here for the fourth time in this arm: 3^u and 2^k
    # are never equal on the range in use. Widening the exponent instead really
    # does change which words survive.
    # The power-vs-floor check computes both forms INLINE, so it cannot see a
    # damaged `survives()`. What can is the cross-check against
    # `first_crossing_words`, which carries its own independent condition — the
    # same reason that cross-check is worth having at all.
    ("A01_survival_threshold_widened",
     "SRC09_DP_counts_match_RUN_006s_first_crossing_enumeration",
     ("    return 3 ** u > 2 ** k", "    return 3 ** u > 2 ** (k - 1)")),
    ("A02_crossing_depth_off_by_one",
     "SRC09_beatty_event_depths_are_the_bit_lengths_of_powers_of_three",
     ("    return (3 ** u).bit_length()", "    return (3 ** u).bit_length() + 1")),
    ("A03_survivor_DP_drops_the_D_branch",
     "SRC09_survivor_DP_reproduces_the_enumerated_tree",
     ("            a[(k, u)] = a.get((k - 1, u), 0) + a.get((k - 1, u - 1), 0)",
      "            a[(k, u)] = a.get((k - 1, u - 1), 0)")),
    ("A04_survivor_tree_forgets_to_prune",
     "SRC09_the_chart_algebra_evaluates_without_error",
     ("        nxt = [c for w in frontier for c in children(w) if survives(c.k, c.u)]",
      "        nxt = [c for w in frontier for c in children(w)]")),
    ("A05_normalized_residue_uses_the_wrong_modulus",
     "SRC09_exact_coefficient_mass_lands_inside_the_brute_force_bracket",
     ("    return w.r / 2 ** w.k", "    return w.r / 2 ** (w.k + 1)")),
    ("A06_lift_assignment_swapped",
     "SRC09_small_x_asymptotics_split_the_two_parities",
     ("    return x / 2 if p == 0 else (x + 1) / 2",
      "    return (x + 1) / 2 if p == 0 else x / 2")),
    ("A07_event_loss_ratio_drops_its_scale_factor",
     "SRC09_the_event_loss_ratio_is_a_proper_fraction",
     ("    return 2 ** -s * hurwitz_zeta(s, chi_D(x, p)) / hurwitz_zeta(s, x)",
      "    return hurwitz_zeta(s, chi_D(x, p)) / hurwitz_zeta(s, x)")),
    ("A08_coefficient_mass_loses_the_cylinder_scale",
     "SRC09_exact_coefficient_mass_lands_inside_the_brute_force_bracket",
     ("    return 2 ** (-k * s) * math.fsum(", "    return 1.0 * math.fsum(")),
    ("A09_head_mass_sums_the_wrong_representative",
     "SRC09_head_tail_reduction_bounds_hold_in_both_forms",
     ("    return math.fsum(w.r ** -s for w in words)",
      "    return math.fsum((w.r + 2 ** w.k) ** -s for w in words)")),
]

TOOL_DEFECTS = [
    ("T01_minimum_anchor_reads_the_wrong_record",
     "SRC09_the_minimum_anchor_plateaus_until_its_own_tau_c",
     ("            if r[\"tau_c\"] > k:", "            if r[\"tau_c\"] >= k:")),
    # A widened brute-force tau_c shifts every crossing, but the shifted depths
    # can still land inside the Beatty set; what it cannot survive is the
    # comparison against the exact Hurwitz mass.
    ("T02_brute_force_tau_c_condition_widened",
     "SRC09_exact_coefficient_mass_lands_inside_the_brute_force_bracket",
     ("        if 3 ** u < 2 ** j:", "        if 3 ** u < 2 ** (j + 1):")),
    ("T03_the_frontier_bracket_drops_its_truncation_tail",
     "SRC09_exact_coefficient_mass_lands_inside_the_brute_force_bracket",
     ("        tail = N_BRUTE ** -1.0", "        tail = 0.0")),
]

RECORD_DEFECTS = [
    ("R01_a_record_holder_is_not_actually_a_record",
     "SRC09_the_measured_anchors_are_strictly_increasing_records", "notrecord"),
    # The plateau check derives m_k FROM the record list, so an overstated tau_c
    # is self-consistent with it. Only re-deriving the record by iteration can
    # see this.
    ("R02_a_record_tau_c_is_overstated",
     "SRC09_every_reported_record_reproduces_under_exact_python_iteration",
     "overstate"),
    ("R03_the_record_list_is_reordered",
     "SRC09_the_measured_anchors_are_strictly_increasing_records", "reorder"),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_proved_unproved_ledger",
     "SRC09_paper_keeps_an_explicit_proved_and_unproved_ledger", "ledger"),
    ("D02_bundle_no_longer_carries_the_earlier_rounds",
     "SRC09_bundle_carries_rounds_01_02_and_the_v03_map", "rounds"),
]


def mutate_records(d: dict, kind: str) -> dict:
    recs = [dict(r) for r in d["records"]]
    if kind == "notrecord":
        recs.insert(3, {"n": recs[3]["n"] + 1, "tau_c": recs[2]["tau_c"]})
    elif kind == "overstate":
        recs[3]["tau_c"] += 7
    elif kind == "reorder":
        recs[4], recs[5] = recs[5], recs[4]
    return {**d, "records": recs}


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    if kind == "ledger":
        keep[PAPER] = keep[PAPER].decode("utf-8").replace("## 未證", "## 附註",
                                                          1).encode("utf-8")
    elif kind == "rounds":
        keep = {n: b for n, b in keep.items() if "Round_01" not in n}
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def main() -> int:
    records_path = pathlib.Path(sys.argv[1])
    rep = {
        "tool": "src09_drill.py",
        "subject": "src09_hardzeta_round03a_recheck.py, Round 03-A's additions to "
                   "hz_chart_algebra.py, and the measured tau_c records",
        "defects": {}, "controls": {},
    }
    original_algebra = ALGEBRA.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, recs, algebra_module="hz_chart_algebra") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ALGEBRA_MODULE": algebra_module}
        out = subprocess.run([sys.executable, str(tool), str(recs)],
                             capture_output=True, text=True, encoding="utf-8",
                             timeout=TIMEOUT_S, env=env)
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

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        base = tmp / "source"
        base.mkdir()
        shutil.copy2(SOURCE / BUNDLE, base / BUNDLE)

        baseline = run(base, TOOL, records_path)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

        for name, target, (old, new) in ALGEBRA_DEFECTS:
            if old not in original_algebra:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} absent; nothing was tested"}
                continue
            mod = f"_drill_algebra_{name}"
            f = CODE / f"{mod}.py"
            try:
                f.write_text(original_algebra.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, TOOL, records_path, mod))
            finally:
                f.unlink(missing_ok=True)

        for name, target, (old, new) in TOOL_DEFECTS:
            if old not in original_tool:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} absent; nothing was tested"}
                continue
            f = CODE / f"_drill_mutant_{name}.py"
            try:
                f.write_text(original_tool.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, f, records_path))
            finally:
                f.unlink(missing_ok=True)

        orig_recs = json.loads(records_path.read_text(encoding="utf-8"))
        for name, target, kind in RECORD_DEFECTS:
            f = tmp / f"{name}.json"
            f.write_text(json.dumps(mutate_records(orig_recs, kind)), encoding="utf-8")
            record(name, target, run(base, TOOL, f))

        for name, target, kind in DOC_DEFECTS:
            s = tmp / f"src_{name}"
            shutil.copytree(base, s)
            mutate_docs(s, kind)
            record(name, target, run(s, TOOL, records_path))
            shutil.rmtree(s, ignore_errors=True)

        mod = "_drill_algebra_null09"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original_algebra + "\n# a comment nothing reads\n",
                         encoding="utf-8")
            res = run(base, TOOL, records_path, mod)
        finally:
            f.unlink(missing_ok=True)
        rep["controls"]["N01_algebra_annotated_where_nothing_reads"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

        f = tmp / "null_records.json"
        f.write_text(json.dumps({**orig_recs, "tool": "annotated, read by nothing"}),
                     encoding="utf-8")
        res = run(base, TOOL, f)
        rep["controls"]["N02_record_file_annotated_where_nothing_reads"] = {
            "undisturbed": bool(res.get("ok")),
            "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                        if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(rep["defects"]),
        "defects_caught_by_the_named_check": caught,
        "defects_in_round_03as_own_formulas": len(ALGEBRA_DEFECTS),
        "defects_in_the_measured_records": len(RECORD_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
