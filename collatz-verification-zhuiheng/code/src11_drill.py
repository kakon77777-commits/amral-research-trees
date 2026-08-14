"""Mutation drill for src11_hardzeta_round03a2_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Round 03-A.2's content is a chain of exact identities, so nine defects damage
those identities one at a time — the canonical endpoint, its range convention,
the bridge numerator, the synchronization bit, the endpoint reconstruction — and
each asks whether the confrontation with direct iteration would notice.

Three more damage this run's own finding about §24's route, because a negative
result that nobody drilled is an opinion.

A defect counts as caught only if the check named for it fails.

Usage:  python code/src11_drill.py
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
TOOL = CODE / "src11_hardzeta_round03a2_recheck.py"
ACCEL = CODE / "hz_accel_code.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
BUNDLE = "Hard_Zeta_Phase_I_Round_03A2_bundle.zip"
PAPER = "Hard_Zeta_Phase_I_Round_03A2_2_3_Infinity_Anchor_Compatibility_v0.1.md"
TIMEOUT_S = 1800

ACCEL_DEFECTS = [
    ("A01_canonical_endpoint_uses_the_wrong_inverse",
     "SRC11_the_exact_2_3_bridge_identity_holds",
     ("    M = (pow(2, -K, 3 ** m) * offset(kappa)) % 3 ** m",
      "    M = (pow(2, K, 3 ** m) * offset(kappa)) % 3 ** m")),
    # RETIRED as a no-op, with the reason: B_m is congruent to 2^{K_{m-1}} mod 3
    # because every other term of B carries a factor of 3, so B_m is never
    # divisible by 3, M_m never lands on 0 mod 3^m, and §4's range convention
    # never binds. Replaced by a defect that does move M.
    # Reducing M by 3^{m+1} shifts M and Q together, so the bridge identity
    # 3^m Q + B = 2^K M still holds exactly. Only the RANGE convention sees it.
    ("A02_canonical_endpoint_reduced_by_the_wrong_modulus",
     "SRC11_the_canonical_endpoint_lies_in_its_stated_range",
     ("    M = (pow(2, -K, 3 ** m) * offset(kappa)) % 3 ** m",
      "    M = (pow(2, -K, 3 ** m) * offset(kappa)) % 3 ** (m + 1)")),
    ("A03_bridge_numerator_sign_flipped",
     "SRC11_the_coarse_source_is_strictly_inside_its_binary_range",
     ("    num = 2 ** K * canonical_endpoint(kappa) - offset(kappa)",
      "    num = offset(kappa) - 2 ** K * canonical_endpoint(kappa)")),
    ("A04_sync_bit_is_the_parity_rather_than_its_complement",
     "SRC11_the_sync_bit_is_the_complement_of_endpoint_parity",
     ("    return 1 - (canonical_endpoint(kappa) % 2)",
      "    return canonical_endpoint(kappa) % 2")),
    ("A05_exact_endpoint_wraps_by_the_wrong_power",
     "SRC11_the_exact_source_really_reaches_that_endpoint",
     ("    return canonical_endpoint(kappa) + sync_bit(kappa) * 3 ** len(kappa)",
      "    return canonical_endpoint(kappa) + sync_bit(kappa) * 2 ** len(kappa)")),
    ("A06_source_residue_modulus_reduced",
     "SRC11_the_exact_source_is_the_coarse_one_plus_the_sync_bit",
     ("    mod = 2 ** (K + 1)\n    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod",
      "    mod = 2 ** K\n    return ((2 ** K - offset(kappa)) * pow(3, -m, mod)) % mod")),
    # Q and M are BOTH derived from B, so the bridge identity survives a damaged
    # B unchanged. Only the B-free walk can see it.
    ("A07_offset_recurrence_damaged",
     "SRC11_the_endpoint_and_code_reproduce_under_plain_iteration",
     ("        B = 3 * B + 2 ** K", "        B = 3 * B + 2 ** (K + 1)")),
    ("A08_subcritical_cone_widened",
     "SRC11_the_subcritical_cone_is_exactly_where_the_coefficient_survives",
     ("        if K > floor_beta(j):", "        if K > floor_beta(j) + 2:")),
    ("A09_accel_code_valuation_truncated",
     "SRC11_the_modules_code_reader_matches_the_independent_walk",
     ("        k = (y & -y).bit_length() - 1      # v_2(y)",
      "        k = min(2, (y & -y).bit_length() - 1)")),
]

TOOL_DEFECTS = [
    ("T01_the_papers_diagnostic_is_transcribed_wrong",
     "SRC11_section_30s_finite_diagnostic_reproduces_exactly",
     ('S30 = {"m": 10, "K": 13, "coarse": 27, "M": 206, "eps": 1,',
      'S30 = {"m": 10, "K": 13, "coarse": 27, "M": 208, "eps": 1,')),
    ("T02_the_odd_run_search_keeps_only_one_candidate",
     "SRC11_the_longest_odd_run_grows_with_depth",
     ("        BEAM = 20000", "        BEAM = 1")),
    ("T03_the_run_holder_is_read_from_the_wrong_code",
     "SRC11_the_longest_odd_M_runs_are_held_by_anchored_sources",
     ("                          \"run_holder_source\": C.source_residue(top[0])})",
      "                          \"run_holder_source\": C.source_residue(beam[-1][0])})")),
]

DOC_DEFECTS = [
    ("D01_paper_loses_its_ledger",
     "SRC11_paper_keeps_an_explicit_proved_and_unproved_ledger", "ledger"),
    ("D02_bundle_reverts_03A1_to_v0_1",
     "SRC11_this_bundle_carries_the_upgraded_03A1", "revert"),
]


def mutate_docs(src: pathlib.Path, kind: str) -> None:
    with zipfile.ZipFile(src / BUNDLE) as z:
        keep = {n: z.read(n) for n in z.namelist()}
    if kind == "ledger":
        keep[PAPER] = keep[PAPER].decode("utf-8").replace("## 未證", "## 附註",
                                                          1).encode("utf-8")
    elif kind == "revert":
        keep = {(n.replace("v0.1.1", "v0.1") if "03A1" in n else n): b
                for n, b in keep.items()}
    with zipfile.ZipFile(src / BUNDLE, "w") as z:
        for n, b in keep.items():
            z.writestr(n, b)


def main() -> int:
    rep = {
        "tool": "src11_drill.py",
        "subject": "src11_hardzeta_round03a2_recheck.py and the 2-3 bridge layer "
                   "of hz_accel_code.py",
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

        mod = "_drill_accel_null11"
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
        "defects_in_the_bridge_arithmetic": len(ACCEL_DEFECTS),
        "defects_in_this_runs_own_finding": len(TOOL_DEFECTS),
        "controls": len(rep["controls"]),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
