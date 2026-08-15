"""Mutation drill for src12_hardzeta_round03a3_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 03-A.3's content is one chain: endpoint recurrence -> 2-adic state -> bit
selection -> zero-lift edge -> spine. Ten defects damage that chain a link at a
time, and each asks whether the confrontation with direct iteration would notice.

Three more damage this run's own spine measurement, since the survival identity
and the profile are what the report leads with.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src12_drill.py
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
TOOL = CODE / "src12_hardzeta_round03a3_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_I_Round_03A3_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A3_Endpoint_Parity_Dynamics_v0.1.md"
MAP6 = "Hard_Zeta_ROUTE_MAP_v0.6.md"
TIMEOUT_S = 1800

ACCEL_DEFECTS = [
    ("A01_endpoint_state_loses_its_sign",
     "SRC12_the_coarse_digit_is_the_low_bits_of_the_endpoint_state",
     ("    return (-(3 * canonical_endpoint(kappa) + 1) * pow(3, -(m + 1), mod)) % mod",
      "    return ((3 * canonical_endpoint(kappa) + 1) * pow(3, -(m + 1), mod)) % mod")),
    ("A02_endpoint_state_uses_the_wrong_power_of_three",
     "SRC12_the_coarse_digit_is_the_low_bits_of_the_endpoint_state",
     ("    return (-(3 * canonical_endpoint(kappa) + 1) * pow(3, -(m + 1), mod)) % mod",
      "    return (-(3 * canonical_endpoint(kappa) + 1) * pow(3, -m, mod)) % mod")),
    ("A03_zero_lift_exponent_reads_the_coarse_endpoint",
     "SRC12_zero_lift_happens_exactly_at_the_self_generated_exponent",
     ("    y = 3 * exact_endpoint(kappa) + 1",
      "    y = 3 * canonical_endpoint(kappa) + 1")),
    ("A04_zero_lift_exponent_off_by_one",
     "SRC12_the_two_routes_to_the_self_generated_exponent_agree",
     ("    return (y & -y).bit_length() - 1", "    return (y & -y).bit_length()")),
    ("A05_subcritical_budget_shifted",
     "SRC12_the_spine_ejection_criterion_matches_following_the_edge",
     ("    return floor_beta(len(kappa) + 1) - cumulative(kappa)[-1]",
      "    return floor_beta(len(kappa) + 2) - cumulative(kappa)[-1]")),
    ("A06_spine_survival_test_uses_the_wrong_comparison",
     "SRC12_the_spine_ejection_criterion_matches_following_the_edge",
     ("    return zero_lift_exponent(kappa) <= subcritical_budget(kappa)",
      "    return zero_lift_exponent(kappa) < subcritical_budget(kappa)")),
    ("A07_spine_trace_extends_by_a_fixed_exponent",
     "SRC12_the_spine_keeps_its_canonical_source_fixed",
     ("        node = node + (q,)", "        node = node + (1,)")),
    ("A08_spine_trace_stops_one_step_early",
     "SRC12_spine_length_is_exactly_the_sources_remaining_subcritical_life",
     ("        if q > Q:", "        if q >= Q:")),
    ("A09_subcritical_lifetime_counts_one_too_many",
     "SRC12_spine_length_is_exactly_the_sources_remaining_subcritical_life",
     ("    while m < limit and is_subcritical(accel_code(n, m + 1)):",
      "    while m < limit and is_subcritical(accel_code(n, m)):")),
    ("A10_endpoint_state_truncated_too_far",
     "SRC12_the_endpoint_state_carries_enough_precision",
     ("XI_PRECISION = 96", "XI_PRECISION = 4")),
]

TOOL_DEFECTS = [
    ("T01_the_papers_example_is_transcribed_wrong",
     "SRC12_section_13s_parity_only_example_reproduces_exactly",
     ('S13 = {"K4": 5, "r4": 27, "M4": 71,',
      'S13 = {"K4": 5, "r4": 27, "M4": 73,')),
    ("T02_the_spine_identity_compares_against_the_node_not_the_source",
     "SRC12_spine_length_is_exactly_the_sources_remaining_subcritical_life",
     ("            if len(kap) + tr[\"steps\"] != C.subcritical_lifetime(src):",
      "            if len(kap) + tr[\"steps\"] != C.subcritical_lifetime(src) + 1:")),
    # Probing one exponent cannot find two keepers — "at most one" passes for
    # free. The companion guard is what sees it.
    ("T03_the_uniqueness_check_probes_only_one_exponent",
     "SRC12_the_uniqueness_probe_could_have_found_a_second_child",
     ("                span = range(1, Q_MAX + 1)",
      "                span = range(1, 2)")),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_ledger",
     "SRC12_paper_keeps_an_explicit_proved_and_unproved_ledger", "ledger"),
    ("D02_the_route_map_no_longer_retires_the_parity_route",
     "SRC12_the_paper_states_the_parity_only_no_go_itself", "route"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    if kind == "ledger":
        keep[PAPER] = keep[PAPER].decode("utf-8").replace("## 未證", "## 附註",
                                                          1).encode("utf-8")
    elif kind == "route":
        keep[MAP6] = keep[MAP6].decode("utf-8").replace(
            "sufficient but too strong", "sufficient", 1).encode("utf-8")
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def main() -> int:
    rep = {
        "tool": "src12_drill.py",
        "subject": "src12_hardzeta_round03a3_recheck.py and the spine layer of "
                   "hz_accel_code.py",
        "defects": {}, "controls": {},
    }
    original_accel = ACCEL.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, accel_module="hz_accel_code") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ACCEL_MODULE": accel_module}
        out = subprocess.run([sys.executable, str(tool)], capture_output=True,
                             text=True, encoding="utf-8", timeout=TIMEOUT_S, env=env)
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

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

        for name, target, (old, new) in ACCEL_DEFECTS:
            if old not in original_accel:
                rep["defects"][name] = {
                    "target_check": target, "caught_by_the_named_check": False,
                    "run_went_red": False, "other_checks_that_also_fired": [],
                    "crash": f"anchor {old!r} absent; nothing was tested"}
                continue
            mod = f"_drill_accel_{name}"
            f = CODE / f"{mod}.py"
            try:
                f.write_text(original_accel.replace(old, new, 1), encoding="utf-8")
                record(name, target, run(base, TOOL, mod))
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
                record(name, target, run(base, f))
            finally:
                f.unlink(missing_ok=True)

        for name, target, kind in DOC_DEFECTS:
            s = tmp / f"src_{name}"
            shutil.copytree(base, s)
            mutate_docs(s, kind)
            record(name, target, run(s, TOOL))
            shutil.rmtree(s, ignore_errors=True)

        mod = "_drill_accel_null12"
        f = CODE / f"{mod}.py"
        try:
            f.write_text(original_accel + "\n# a comment nothing reads\n",
                         encoding="utf-8")
            res = run(base, TOOL, mod)
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
        "defects_in_the_spine_chain": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_measurement": len(TOOL_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
