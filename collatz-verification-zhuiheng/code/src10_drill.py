"""Mutation drill for src10_hardzeta_round03a1_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 03-A.1 is a change of coordinates, so almost every check here is a
confrontation between two descriptions of the same object. Ten defects damage the
accelerated-code arithmetic itself — the valuation, the offset recurrence, the
source congruence, its modulus, the mechanical code, the pruned search — and each
asks whether the confrontation with direct iteration would notice.

Two more damage the branch-and-bound prune, because a headline computed under a
prune that nobody drilled is a headline resting on an assumption.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src10_drill.py <tau-records.json>
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
TOOL = CODE / "src10_hardzeta_round03a1_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_I_Round_03A1_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A1_Small_Anchor_Event_Arithmetic_v0.1.md"
TIMEOUT_S = 1800

ACCEL_DEFECTS = [
    ("A01_valuation_read_one_bit_short",
     "SRC10_the_accelerated_code_reproduces_direct_iteration",
     ("        k = (y & -y).bit_length() - 1      # v_2(y)",
      "        k = max(1, (y & -y).bit_length() - 2)")),
    ("A02_offset_recurrence_loses_its_power_of_two",
     "SRC10_the_affine_endpoint_formula_reproduces_the_walk",
     ("        B = 3 * B + 2 ** K", "        B = 3 * B + 1")),
    ("A03_source_modulus_drops_the_extra_digit",
     "SRC10_each_canonical_source_really_realizes_its_own_code",
     ("    mod = 2 ** (K + 1)\n    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod",
      "    mod = 2 ** K\n    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod")),
    ("A04_source_congruence_loses_its_inverse",
     "SRC10_each_canonical_source_really_realizes_its_own_code",
     ("    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod",
      "    return ((2 ** K - offset(kappa)) * pow(3, m, mod)) % mod")),
    ("A05_floor_beta_off_by_one",
     "SRC10_the_strict_and_floor_forms_of_subcriticality_agree",
     ("    return (3 ** j).bit_length() - 1", "    return (3 ** j).bit_length()")),
    ("A06_subcritical_test_uses_the_wrong_index",
     "SRC10_subcritical_means_the_coefficient_has_not_crossed",
     ("        if K > floor_beta(j):", "        if K > floor_beta(j + 1):")),
    ("A07_mechanical_code_increments_shifted",
     "SRC10_the_mechanical_code_is_the_maximal_subcritical_path",
     ("    return tuple(floor_beta(j) - floor_beta(j - 1) for j in range(1, m + 1))",
      "    return tuple(floor_beta(j + 1) - floor_beta(j) for j in range(1, m + 1))")),
    # Admitting a supercritical code does not break monotonicity — the sources
    # still only grow. What it breaks is the minimum, so the diagnostic table is
    # the check that can see it.
    ("A08_code_enumeration_admits_supercritical_codes",
     "SRC10_section_34s_diagnostic_table_reproduces_exactly",
     ("               for k in range(1, cap - K + 1)]",
      "               for k in range(1, cap - K + 2)]")),
    ("A09_endpoint_formula_uses_the_wrong_exponent",
     "SRC10_the_affine_endpoint_formula_reproduces_the_walk",
     ("    num = 3 ** len(kappa) * n + offset(kappa)",
      "    num = 3 ** (len(kappa) + 1) * n + offset(kappa)")),
    ("A10_residue_rate_normalized_by_the_wrong_quantity",
     "SRC10_a_nonzero_lift_always_spikes_the_rate_above_alpha",
     ("    return (r.bit_length() - 1) / K if K else 0.0",
      "    return (r.bit_length() - 1) / (2 * K) if K else 0.0")),
]

PRUNE_DEFECTS = [
    ("P01_prune_cap_lowered_below_the_answer",
     "SRC10_the_branch_and_bound_prune_is_exact_on_this_run",
     ("def minimum_anchor(maxlen: int, cap: int = 10 ** 7) -> list[dict]:",
      "def minimum_anchor(maxlen: int, cap: int = 20) -> list[dict]:")),
    ("P02_prune_drops_codes_it_should_keep",
     "SRC10_the_deep_anchor_agrees_with_the_full_enumeration",
     ("                if r <= cap:", "                if r <= cap and r % 3 != 1:")),
]

TOOL_DEFECTS = [
    ("T01_the_papers_table_is_transcribed_wrong",
     "SRC10_section_34s_diagnostic_table_reproduces_exactly",
     ("PAPER_TABLE = {1: (3, 3), 2: (7, 11), 3: (7, 27), 4: (27, 123),",
      "PAPER_TABLE = {1: (3, 3), 2: (7, 11), 3: (7, 29), 4: (27, 123),")),
    ("T02_the_anchor_bridge_uses_the_wrong_beatty_depth",
     "SRC10_each_anchor_leaves_exactly_at_the_beatty_depth_of_its_own_tau_c",
     ("                want = A.crossing_depth(m_switch)",
      "                want = A.crossing_depth(m_switch + 1)")),
    ("T03_the_count_bridge_is_shifted",
     "SRC10_subcritical_code_count_equals_round_03As_first_crossing_count",
     ("            Km1 = A.crossing_depth(m + 1)", "            Km1 = A.crossing_depth(m + 2)")),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_ledger",
     "SRC10_paper_keeps_an_explicit_proved_and_unproved_ledger", "ledger"),
    ("D02_bundle_loses_the_v04_route_map",
     "SRC10_bundle_carries_the_earlier_rounds_and_the_v04_map", "map"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    if kind == "ledger":
        keep[PAPER] = keep[PAPER].decode("utf-8").replace("## 未證", "## 附註",
                                                          1).encode("utf-8")
    elif kind == "map":
        keep = {n: b for n, b in keep.items() if "ROUTE_MAP_v0.4" not in n}
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def main() -> int:
    records = pathlib.Path(sys.argv[1])
    rep = {
        "tool": "src10_drill.py",
        "subject": "src10_hardzeta_round03a1_recheck.py and hz_accel_code.py",
        "defects": {}, "controls": {},
    }
    original_accel = ACCEL.read_text(encoding="utf-8")
    original_tool = TOOL.read_text(encoding="utf-8")

    def run(src_dir, tool, accel_module="hz_accel_code") -> dict:
        env = {**os.environ, "PYTHONUTF8": "1", "HZ_SOURCE_DIR": str(src_dir),
               "HZ_ACCEL_MODULE": accel_module}
        out = subprocess.run([sys.executable, str(tool), str(records)],
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

        baseline = run(base, TOOL)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "failures": baseline.get("failures", baseline)},
                             indent=2, ensure_ascii=False))
            return 2

        for group in (ACCEL_DEFECTS, PRUNE_DEFECTS):
            for name, target, (old, new) in group:
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

        mod = "_drill_accel_null10"
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
        (s / "UNREAD_SCRATCH.txt").write_text("read by nothing\n", encoding="utf-8")
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
        "defects_in_the_accelerated_code_arithmetic": len(ACCEL_DEFECTS),
        "defects_in_the_branch_and_bound_prune": len(PRUNE_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
