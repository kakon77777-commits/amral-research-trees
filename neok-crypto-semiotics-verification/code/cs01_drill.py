"""Mutation drill for cs01_v08_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

Every check must have at least one defect naming it, and a defect counts as
caught only if **the check named for it** fails — not merely some check. That is
the rule that exposes checks which test nothing.

Two of this run's checks assert a NEGATIVE about the package (readiness is not
re-derivable; the shipped TLA+ is weaker than the validated model). A negative
assertion is easy to make unfalsifiable by accident, so both are drilled by
making the negative FALSE — the readiness check is fed a circular computation
that trivially matches, and the TLA+ check is given the missing actions — and
each must go red.

No defect loosens a comparison; every one changes what is computed.

Usage:  python code/cs01_drill.py
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE = ROOT / "code"
TOOL = CODE / "cs01_v08_recheck.py"
TIMEOUT_S = 1800

DEFECTS = [
    ("D01_the_manifest_is_hashed_over_the_wrong_bytes",
     "CS01_the_integrity_manifest_verifies_except_the_two_timing_outputs",
     ("                elif hashlib.sha256(f.read_bytes()).hexdigest() == h:",
      "                elif hashlib.sha256(f.read_bytes() + b'x').hexdigest() == h:")),
    ("D02_the_timing_agreement_is_sought_under_a_mangled_key",
     "CS01_the_two_stale_files_still_agree_with_each_other",
     ('            missing = [r for r in csv_rows\n'
      '                       if not all(f in blob for f in r.split(",")[1:3])]',
      '            missing = [r for r in csv_rows\n'
      '                       if not all(f + "Z" in blob for f in r.split(",")[1:3])]')),
    ("D03_an_extra_obligation_is_counted",
     "CS01_the_readme_headline_counts_recompute_from_the_shipped_data",
     ('                "formal_obligations": len(jsonl(v7 / "obligations_v0.7.jsonl")),',
      '                "formal_obligations": len(jsonl(v7 / "obligations_v0.7.jsonl")) + 1,')),
    ("D04_the_population_check_reads_the_previous_layer",
     "CS01_the_v08_layer_carries_the_same_claim_population",
     ('            pr = jsonl(v8 / "promotion_profiles_v0.8.jsonl")\n'
      '            return (len(ob) == 2490 and len(pr) == 264',
      '            pr = jsonl(v8 / "obligations_v0.8.jsonl")\n'
      '            return (len(ob) == 2490 and len(pr) == 264')),
    ("D05_the_gate_order_restriction_is_dropped_from_the_scope",
     "CS01_the_gate_rule_from_the_prose_reproduces_every_profile_but_one",
     ('                scope = [r for r in rows if r.get("blocking")\n'
      '                         and GATE_IX.get(r.get("gate"), 99) <= k]',
      '                scope = [r for r in rows if r.get("blocking")]')),
    # The negative assertion, made false on purpose: compute readiness FROM the
    # answer. Every scope then "reproduces" it and the check must notice.
    ("D06_readiness_is_computed_from_the_value_it_is_checking",
     "CS01_the_readiness_score_cannot_be_rederived_from_the_package",
     ('                    v = sum(weight(r.get("state")) for r in s) / len(s)',
      '                    v = float(p["readiness_score"])')),
    ("D07_the_schema_check_validates_against_an_empty_schema",
     "CS01_the_shipped_schema_rejects_exactly_one_v08_profile",
     ('                sch = json.load(io.open(v7 / sch_name, encoding="utf-8"))\n'
      '                V = jsonschema.Draft202012Validator(sch)',
      '                sch = json.load(io.open(v7 / sch_name, encoding="utf-8"))\n'
      '                V = jsonschema.Draft202012Validator({})')),
    ("D08_the_ctcl_model_lets_decryption_happen_without_the_stolen_key",
     "CS01_the_ctcl_trust_model_reproduces_from_its_own_tla",
     ("        if u and s and not p:", "        if u and not p:")),
    # The other negative assertion, made false: give the .tla the two actions it
    # is missing, so "as written" and "with environment" agree.
    ("D09_the_tla_transcription_always_takes_the_environment_actions",
     "CS01_the_shipped_tla_does_not_specify_the_model_that_was_validated",
     ("    if environment_may_choose:", "    if True:")),
    # NOT "drop the (risk == LOW or approved) conjunct" — measured to be a
    # no-op with a reason: PrioritizeDone already refuses to enter Respond while
    # risk is High and approved is False, so 0 of the 8 reachable Respond states
    # satisfy it. That conjunct is redundant with the upstream guard. The
    # `authorized` conjunct is the one that is not doubled.
    ("D10_the_runtime_applies_a_response_from_an_unauthorized_actor",
     "CS01_the_runtime_safety_properties_survive_on_the_larger_model",
     ("        if authorized and (risk == LOW or approved):",
      "        if (risk == LOW or approved):")),
    ("D11_their_suite_is_run_from_the_wrong_directory",
     "CS01_their_own_test_suites_reproduce_on_this_platform",
     ('                                   cwd=str(v8 / sub), capture_output=True, text=True,',
      '                                   cwd=str(v8), capture_output=True, text=True,')),
]


def audit(baseline: dict) -> list[str]:
    targeted = {t for _, t, _ in DEFECTS}
    names = set(baseline.get("checks", {}))
    return sorted([f"unguarded check: {c}" for c in names - targeted]
                  + [f"defect names a check that does not exist: {t}"
                     for t in targeted - names])


def run(tool: pathlib.Path) -> dict:
    try:
        p = subprocess.run([sys.executable, str(tool)], capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=TIMEOUT_S,
                           env={**os.environ, "PYTHONUTF8": "1",
                                "PYTHONDONTWRITEBYTECODE": "1"})
    except subprocess.TimeoutExpired:
        return {"ok": False, "checks": {}, "_crash": "timed out"}
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "checks": {},
                "_crash": (p.stdout + p.stderr)[-400:]}


def main() -> int:
    rep = {"tool": "cs01_drill.py", "subject": "cs01_v08_recheck.py",
           "defects": {}, "controls": {}, "audit": []}
    original = TOOL.read_text(encoding="utf-8")

    baseline = run(TOOL)
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

    for name, target, (old, new) in DEFECTS:
        if original.count(old) != 1:
            rep["defects"][name] = {
                "target_check": target, "caught_by_the_named_check": False,
                "crash": f"anchor matched {original.count(old)} times; nothing tested"}
            continue
        f = CODE / f"_drill_{name}.py"
        try:
            f.write_text(original.replace(old, new, 1), encoding="utf-8")
            res = run(f)
        finally:
            f.unlink(missing_ok=True)
        c = res.get("checks", {})
        rep["defects"][name] = {
            "target_check": target,
            "caught_by_the_named_check": target in c and not c[target]["pass"],
            "run_went_red": not res.get("ok", True),
            "other_checks_that_also_fired": sorted(
                k for k, v in c.items() if not v["pass"] and k != target),
            **({"crash": res["_crash"]} if "_crash" in res else {})}

    f = CODE / "_drill_null.py"
    try:
        f.write_text(original + "\n# a comment nothing reads\n", encoding="utf-8")
        res = run(f)
    finally:
        f.unlink(missing_ok=True)
    rep["controls"]["N01_the_tool_annotated_where_nothing_reads"] = {
        "undisturbed": bool(res.get("ok")),
        "checks_that_fired": sorted(k for k, v in res.get("checks", {}).items()
                                    if not v["pass"])}

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {"defects_planted": len(rep["defects"]),
                     "defects_caught_by_the_named_check": caught,
                     "controls": len(rep["controls"]),
                     "controls_undisturbed": quiet,
                     "checks_without_a_defect_naming_them": 0}
    rep["ok"] = caught == len(rep["defects"]) and quiet == len(rep["controls"])
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
