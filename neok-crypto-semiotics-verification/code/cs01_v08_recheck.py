"""Recheck of NeoK_Crypto_Semiotics_Theory_Compiler_v0.8.zip (source item 38).

數學戰士「墜衡」 / AMRAL Research Lab.

This is the first item in the sweep that leaves Hard-Zeta, and the instruments
change with the subject. The package is not a paper; it is a *theory compiler*:
264 claims carrying 2490 formal obligations, a promotion-gate model, and a v0.8
"obligation execution" layer that advances three claims by shipping executable
security models with their own test suites.

So the questions are different too. Not "does the proof hold" but:

  - do the package's own integrity hashes still verify;
  - do its headline counts recompute from the data it ships;
  - do the profile fields recompute from the PROSE gate rule, rather than from
    a generator (which is not shipped);
  - does the shipped data validate against the shipped JSON Schema;
  - do the formal artifacts (TLA+) specify the model that was actually
    validated (Python);
  - and does "7/7 tests passed" mean the guards are pinned, or only that the
    suite is green?

The last two are where this run found things.

Usage:  python code/cs01_v08_recheck.py
Env:    CS_SOURCE_ZIP  path to the .zip (default: Neo's source folder)
"""

from __future__ import annotations

import collections
import hashlib
import io
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
DEFAULT_ZIP = (pathlib.Path(r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新"
                            r"\Collatz_OT_Series_Paper")
               / "NeoK_Crypto_Semiotics_Theory_Compiler_v0.8.zip")
SRC_ZIP = pathlib.Path(os.environ.get("CS_SOURCE_ZIP", str(DEFAULT_ZIP)))
TOP = "NeoK_Crypto_Semiotics_Theory_Compiler_v0.8"
V7 = "11_formal_obligations_v0.7"
V8 = "12_obligation_execution_v0.8"

GATES = ["G0_source_captured", "G1_typed_and_scoped",
         "G2_formalized_or_operationalized", "G3_internal_validation",
         "G4_external_validation", "G5_independent_review",
         "G6_doctrine_or_standard"]
GATE_IX = {g: i for i, g in enumerate(GATES)}
PASSING = {"satisfied", "waived_historical"}


def jsonl(p: pathlib.Path) -> list[dict]:
    return [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]


# --------------------------------------------------------------------------
# The Persistent Security Runtime transition relation, transcribed from the
# package's PersistentSecurityRuntime.tla TEXT — not from its runtime_model.py.
# Reimplementing the SPEC rather than the PROGRAM is the whole point; a referee
# written from the program can only confirm the program's own reading.
# --------------------------------------------------------------------------
LOW, HIGH = "Low", "High"


def psr_successors(s, *, environment_may_choose: bool):
    stage, risk, approved, authorized, applied, verified, rolled = s
    out = []
    if stage == "Observe":
        out.append(("Model", risk, approved, authorized, applied, verified, rolled))
    if stage == "Model":
        out.append(("Detect", risk, approved, authorized, applied, verified, rolled))
    if stage == "Detect":
        out.append(("Prioritize", LOW, approved, authorized, applied, verified, rolled))
        out.append(("Prioritize", HIGH, approved, authorized, applied, verified, rolled))
    if stage == "Prioritize":
        if risk == HIGH and not approved:
            out.append(("AwaitApproval", risk, approved, authorized, applied, verified, rolled))
        if risk == LOW or approved:
            out.append(("Respond", risk, approved, authorized, applied, verified, rolled))
    if stage == "AwaitApproval":
        out.append(("Respond", risk, True, authorized, applied, verified, rolled))
        out.append(("Learn", risk, False, authorized, False, verified, rolled))
    if stage == "Respond":
        if authorized and (risk == LOW or approved):
            out.append(("Verify", risk, approved, authorized, True, verified, rolled))
        else:
            out.append(("Learn", risk, approved, authorized, False, verified, rolled))
    if stage == "Verify":
        if verified:
            out.append(("Learn", risk, approved, authorized, applied, verified, rolled))
        else:
            out.append(("Rollback", risk, approved, authorized, applied, verified, rolled))
    if stage == "Rollback":
        out.append(("Learn", risk, approved, authorized, False, verified, True))
    if stage == "Learn":
        out.append(("Observe", risk, False, authorized, False, verified, False))
    if environment_may_choose:
        # The two actions the shipped .tla does NOT have. Their Python model
        # takes them at exactly these two stage boundaries.
        if stage == "Respond":
            out += [(stage, risk, approved, a, applied, verified, rolled) for a in (False, True)]
        if stage == "Verify":
            out += [(stage, risk, approved, authorized, applied, v, rolled) for v in (False, True)]
    return out


def psr_reachable(*, environment_may_choose: bool) -> set:
    init = ("Observe", LOW, False, True, False, True, False)
    seen, stack = {init}, [init]
    while stack:
        s = stack.pop()
        for t in psr_successors(s, environment_may_choose=environment_may_choose):
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


# CTCL trust-state model, likewise transcribed from CTCL_CloudCompromise.tla.
def ctcl_reachable() -> set:
    init = (False, False, False, False)          # uploaded, cloud, stolen, known
    seen, stack = {init}, [init]
    while stack:
        u, c, s, p = stack.pop()
        nxt = []
        if not u:
            nxt.append((True, c, s, p))
        if not c:
            nxt.append((u, True, s, p))
        if not s:
            nxt.append((u, c, True, p))
        if u and s and not p:
            nxt.append((u, c, s, True))
        for t in nxt:
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


def main() -> int:
    rep = {
        "tool": "cs01_v08_recheck.py",
        "subject": "NeoK_Crypto_Semiotics_Theory_Compiler_v0.8.zip (source item 38)"
                   " — the theory compiler through its v0.8 obligation-execution"
                   " layer",
        "source_items": [38],
        "scope": "the package's own integrity manifest, the headline counts, the"
                 " promotion-profile fields re-derived from the PROSE gate rule,"
                 " JSON Schema conformance, and whether the shipped TLA+"
                 " artifacts specify the models the Python actually validated",
        "checks": {}, "counts": {}, "measured": {}, "failures": [],
    }
    checks, measured = rep["checks"], rep["measured"]

    def check(name, fn, note=""):
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        checks[name] = {"pass": bool(ok), "detail": detail, "note": note}

    if not SRC_ZIP.exists():
        print(json.dumps({"error": f"source zip not found: {SRC_ZIP}"}, indent=2))
        return 2
    rep["source_sha256"] = hashlib.sha256(SRC_ZIP.read_bytes()).hexdigest()
    rep["source_bytes"] = SRC_ZIP.stat().st_size

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="cs38_"))
    try:
        with zipfile.ZipFile(SRC_ZIP) as z:
            z.extractall(tmp)
        pkg = tmp / TOP
        v7, v8 = pkg / V7, pkg / V8

        # ------------------------------------------------ integrity manifest
        def integrity():
            man = v8 / "integrity_manifest.sha256"
            rows = [l.strip() for l in io.open(man, encoding="utf-8") if l.strip()]
            ok, mismatch, missing = 0, [], []
            for l in rows:
                m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", l)
                if not m:
                    mismatch.append(("unparsed", l[:60]))
                    continue
                h, rel = m.group(1).lower(), m.group(2).strip()
                f = v8 / rel
                if not f.exists():
                    missing.append(rel)
                elif hashlib.sha256(f.read_bytes()).hexdigest() == h:
                    ok += 1
                else:
                    mismatch.append(rel)
            measured["integrity"] = {"entries": len(rows), "verified": ok,
                                     "mismatched": mismatch, "missing": missing}
            # The two files that do not match are the ONLY two that carry
            # wall-clock timings, and their runner rewrites both. That is a
            # stale manifest, not altered content — and the check says so by
            # naming the expected pair rather than tolerating any two failures.
            expected = {"01_omega_wrapper/benchmark_results.csv",
                        "validation_results.json"}
            return (not missing and set(mismatch) == expected), {
                "entries": len(rows), "verified": ok,
                "mismatched": sorted(mismatch), "missing": missing}

        check("CS01_the_integrity_manifest_verifies_except_the_two_timing_outputs",
              integrity,
              "49 of 51 entries verify. The two that do not are the benchmark CSV "
              "and validation_results.json — the only files carrying wall-clock "
              "timings, and run_v08_validation.py rewrites both, so the manifest "
              "was hashed before the last run.")

        def timing_pair_is_consistent():
            # The distinguishing evidence for "stale manifest" over "edited
            # content": the CSV's numbers must appear verbatim inside the JSON's
            # captured stdout. If they had drifted apart, the story would be
            # different and this check would go red.
            csv_rows = [l.strip() for l in
                        io.open(v8 / "01_omega_wrapper" / "benchmark_results.csv",
                                encoding="utf-8") if l.strip()][1:]
            blob = json.dumps(json.load(io.open(v8 / "validation_results.json",
                                                encoding="utf-8")))
            missing = [r for r in csv_rows
                       if not all(f in blob for f in r.split(",")[1:3])]
            return (csv_rows and not missing), {"csv_rows": len(csv_rows),
                                                "rows_not_found_in_the_json": missing}

        check("CS01_the_two_stale_files_still_agree_with_each_other",
              timing_pair_is_consistent,
              "each benchmark timing appears verbatim in the captured stdout, "
              "which is what separates a stale manifest from altered content")

        # ------------------------------------------------------ the counts
        def headline_counts():
            got = {
                "claims": len(jsonl(v7 / "promotion_profiles_v0.7.jsonl")),
                "formal_obligations": len(jsonl(v7 / "obligations_v0.7.jsonl")),
                "evidence_gaps": len(jsonl(v7 / "evidence_gap_registry_v0.7.jsonl")),
                "obligation_dependency_edges":
                    len(jsonl(v7 / "obligation_dependencies_v0.7.jsonl")),
                "promotion_profiles": len(jsonl(v7 / "promotion_profiles_v0.7.jsonl")),
            }
            said = {"claims": 264, "formal_obligations": 2490, "evidence_gaps": 608,
                    "obligation_dependency_edges": 714, "promotion_profiles": 264}
            bad = {k: (got[k], said[k]) for k in said if got[k] != said[k]}
            measured["headline_counts"] = {"README_v0.7": said, "recomputed": got}
            return not bad, {"recomputed": got, "disagreements": bad}

        check("CS01_the_readme_headline_counts_recompute_from_the_shipped_data",
              headline_counts,
              "README_v0.7 states 264 / 2490 / 608 / 714; every one is a row "
              "count over a shipped JSONL")

        def v8_carries_the_same_population():
            ob = jsonl(v8 / "obligations_v0.8.jsonl")
            pr = jsonl(v8 / "promotion_profiles_v0.8.jsonl")
            return (len(ob) == 2490 and len(pr) == 264
                    and len({o["claim_id"] for o in ob}) == 264
                    and len({p["claim_id"] for p in pr}) == 264), {
                "obligations": len(ob), "profiles": len(pr),
                "distinct_claims_in_obligations": len({o["claim_id"] for o in ob}),
                "distinct_claims_in_profiles": len({p["claim_id"] for p in pr})}

        check("CS01_the_v08_layer_carries_the_same_claim_population",
              v8_carries_the_same_population,
              "the execution layer advances three claims; it must not change the "
              "population underneath them")

        # ------------------- the profile fields, re-derived from the PROSE rule
        def profile_fields_from_the_prose_rule():
            # 02_promotion_gate_spec.md: for target gate G_k, every blocking
            # obligation with gate order <= k must be satisfied or
            # waived_historical; partially_satisfied only raises readiness.
            ob = jsonl(v8 / "obligations_v0.8.jsonl")
            pr = jsonl(v8 / "promotion_profiles_v0.8.jsonl")
            by = collections.defaultdict(list)
            for o in ob:
                by[o["claim_id"]].append(o)
            in_scope_bad, unres_bad, decision_bad, n = [], [], [], 0
            for p in pr:
                k = GATE_IX.get(p["target_gate"])
                if k is None:
                    continue                      # ARCHIVE targets are out of scope
                n += 1
                rows = by[p["claim_id"]]
                if (len(rows) != p["obligation_count"]
                        or sum(1 for r in rows if r.get("blocking"))
                        != p["blocking_obligation_count"]):
                    in_scope_bad.append(p["claim_id"])
                scope = [r for r in rows if r.get("blocking")
                         and GATE_IX.get(r.get("gate"), 99) <= k]
                unres = sum(1 for r in scope if r.get("state") not in PASSING)
                if unres != p["unresolved_blocking_count"]:
                    unres_bad.append({"claim": p["claim_id"], "said":
                                      p["unresolved_blocking_count"], "derived": unres,
                                      "out_of_scope_blocking_not_passing":
                                      sum(1 for r in rows if r.get("blocking")
                                          and GATE_IX.get(r.get("gate"), 99) > k
                                          and r.get("state") not in PASSING)})
            measured["prose_rule"] = {
                "profiles_in_scope": n,
                "population_disagreements": in_scope_bad,
                "unresolved_blocking_disagreements": unres_bad}
            return (not in_scope_bad and len(unres_bad) == 1
                    and unres_bad[0]["claim"] == "CL-N21-005"), {
                "profiles_in_scope": n,
                "population_disagreements": len(in_scope_bad),
                "unresolved_blocking_disagreements": unres_bad}

        check("CS01_the_gate_rule_from_the_prose_reproduces_every_profile_but_one",
              profile_fields_from_the_prose_rule,
              "the quantifier is in the prose, not the field name: only "
              "obligations at gate order <= the TARGET gate count. 205 of 206 "
              "profiles follow it; CL-N21-005 counts one that sits above its "
              "target gate.")

        def readiness_is_not_rederivable():
            # readiness_score is the v0.8 report's headline metric ("0.3182 ->
            # 0.75"), but no shipped document defines it and no shipped script
            # computes it — promotion_gate.py only prints it. Four candidate
            # scopes are tried; the check asserts that NONE reproduces all 264,
            # which is a falsifiable statement about the package.
            ob = jsonl(v8 / "obligations_v0.8.jsonl")
            pr = jsonl(v8 / "promotion_profiles_v0.8.jsonl")
            by = collections.defaultdict(list)
            for o in ob:
                by[o["claim_id"]].append(o)

            def weight(st):
                return 1.0 if st in PASSING else 0.5 if st == "partially_satisfied" else 0.0

            scopes = {
                "blocking, gate<=target": lambda rows, k: [r for r in rows if r.get("blocking") and GATE_IX.get(r.get("gate"), 99) <= k],
                "blocking, all gates": lambda rows, k: [r for r in rows if r.get("blocking")],
                "all obligations": lambda rows, k: rows,
                "all, gate<=target": lambda rows, k: [r for r in rows if GATE_IX.get(r.get("gate"), 99) <= k],
            }
            out = {}
            for nm, f in scopes.items():
                bad = tot = 0
                for p in pr:
                    k = GATE_IX.get(p["target_gate"])
                    if k is None:
                        continue
                    s = f(by[p["claim_id"]], k)
                    if not s:
                        continue
                    tot += 1
                    v = sum(weight(r.get("state")) for r in s) / len(s)
                    if abs(round(v, 4) - round(float(p["readiness_score"]), 4)) > 5e-5:
                        bad += 1
                out[nm] = {"checked": tot, "mismatch": bad}
            measured["readiness"] = {
                "scopes_tried": out,
                "reading": ("readiness_score is the v0.8 report's headline metric "
                            "and no shipped artefact defines or computes it. The "
                            "closest reading leaves "
                            f"{min(v['mismatch'] for v in out.values())} of "
                            f"{max(v['checked'] for v in out.values())} claims "
                            "unexplained, so the figure cannot be re-derived from "
                            "the package.")}
            return all(v["mismatch"] > 0 for v in out.values()), {"scopes": out}

        check("CS01_the_readiness_score_cannot_be_rederived_from_the_package",
              readiness_is_not_rederivable,
              "a falsifiable claim about the package: if a future version ships "
              "the generator or defines the metric, one of these scopes starts "
              "matching and this check goes red on purpose")

        # ------------------------------------------------ schema conformance
        def schema_conformance():
            try:
                import jsonschema
            except ImportError:
                return False, "jsonschema not installed; cannot make this claim"
            out, rejected = {}, {}
            pairs = [("promotion_schema_v0.7.json", v7 / "promotion_profiles_v0.7.jsonl", "v0.7 profiles"),
                     ("obligation_schema_v0.7.json", v7 / "obligations_v0.7.jsonl", "v0.7 obligations"),
                     ("promotion_schema_v0.7.json", v8 / "promotion_profiles_v0.8.jsonl", "v0.8 profiles"),
                     ("obligation_schema_v0.7.json", v8 / "obligations_v0.8.jsonl", "v0.8 obligations")]
            for sch_name, data, label in pairs:
                sch = json.load(io.open(v7 / sch_name, encoding="utf-8"))
                V = jsonschema.Draft202012Validator(sch)
                bad = []
                for r in jsonl(data):
                    e = next(V.iter_errors(r), None)
                    if e:
                        bad.append({"id": r.get("claim_id") or r.get("obligation_id"),
                                    "error": e.message[:120]})
                out[label] = {"rows": len(jsonl(data)), "rejected": len(bad)}
                if bad:
                    rejected[label] = bad[:5]
            measured["schema"] = {"summary": out, "rejections": rejected}
            return (out["v0.7 profiles"]["rejected"] == 0
                    and out["v0.7 obligations"]["rejected"] == 0
                    and out["v0.8 obligations"]["rejected"] == 0
                    and out["v0.8 profiles"]["rejected"] == 1
                    and rejected["v0.8 profiles"][0]["id"] == "CL-N21-005"), {
                "summary": out, "rejections": rejected}

        check("CS01_the_shipped_schema_rejects_exactly_one_v08_profile",
              schema_conformance,
              "the v0.7 data validates clean on both schemas and so do the v0.8 "
              "obligations. Exactly one v0.8 profile fails: CL-N21-005 carries "
              "promotion_decision 'ready_at_target', which the shipped enum does "
              "not contain. It is the same claim the gate rule misses.")

        # ---------------------------- the formal artifacts vs the tested models
        def ctcl_state_model():
            seen = ctcl_reachable()
            viol = [s for s in seen if s[0] and s[1] and not s[2] and s[3]]
            rollback_boundary = [s for s in seen if s[3]]
            return (len(seen) == 10 and not viol and len(rollback_boundary) == 2), {
                "reachable_states": len(seen),
                "cloud_only_secrecy_violations": len(viol),
                "states_with_plaintext_known": len(rollback_boundary),
                "note": "derived from CTCL_CloudCompromise.tla, not from their "
                        "finite_model.py; matches the reported 10 and 0"}

        check("CS01_the_ctcl_trust_model_reproduces_from_its_own_tla",
              ctcl_state_model,
              "10 reachable states and 0 cloud-only secrecy violations, and both "
              "plaintext-known states require the client key to be stolen — so "
              "the model does not overclaim endpoint security")

        def psr_tla_is_weaker_than_the_validated_model():
            as_written = psr_reachable(environment_may_choose=False)
            with_env = psr_reachable(environment_may_choose=True)
            stages_written = {s[0] for s in as_written}
            stages_env = {s[0] for s in with_env}
            measured["persistent_security_runtime"] = {
                "tla_as_written_states": len(as_written),
                "tla_as_written_stages": sorted(stages_written),
                "rollback_reachable_as_written": "Rollback" in stages_written,
                "with_two_environment_actions_states": len(with_env),
                "rollback_reachable_with_env": "Rollback" in stages_env,
                "reported_by_the_package": 62,
                "reading": ("the shipped PersistentSecurityRuntime.tla pins "
                            "authorized = TRUE and verificationOK = TRUE in Init "
                            "and no action ever changes them, so VerifyFail can "
                            "never fire and the Rollback stage is unreachable. "
                            "Running TLC on it as written would explore 16 states "
                            "and would never exercise the rollback behaviour the "
                            "report highlights. Their runtime_model.py takes an "
                            "environment choice at the Respond and Verify "
                            "boundaries; adding those two actions to the .tla "
                            "reproduces the reported 62 exactly.")}
            return (len(as_written) == 16 and "Rollback" not in stages_written
                    and len(with_env) == 62 and "Rollback" in stages_env), {
                "as_written": len(as_written), "with_environment": len(with_env),
                "reported": 62}

        check("CS01_the_shipped_tla_does_not_specify_the_model_that_was_validated",
              psr_tla_is_weaker_than_the_validated_model,
              "16 states as written with Rollback unreachable, against the "
              "reported 62. Two environment actions close the gap exactly. The "
              "report says TLC was not run, which is why this survived.")

        def psr_safety_survives_the_repair():
            # The gap is in coverage, not in safety: both properties still hold
            # over the larger state space. Saying so is the difference between
            # "the artifact is weaker than advertised" and "the claim is wrong".
            with_env = psr_reachable(environment_may_choose=True)
            high_risk = [s for s in with_env if s[1] == HIGH and s[4] and not s[2]]
            unauthorized = [s for s in with_env if s[4] and not s[3]]
            return (not high_risk and not unauthorized and len(with_env) == 62), {
                "states": len(with_env),
                "high_risk_applied_without_approval": len(high_risk),
                "applied_while_unauthorized": len(unauthorized)}

        check("CS01_the_runtime_safety_properties_survive_on_the_larger_model",
              psr_safety_survives_the_repair,
              "over all 62 states, no response is applied at high risk without "
              "approval and none is applied unauthorized — the repair widens "
              "coverage without breaking the claim")

        # ------------------------------------------- do their tests have teeth
        def their_suite_reproduces():
            out = {}
            for sub, test in (("01_omega_wrapper", "test_omega_wrapper.py"),
                              ("02_ctcl_cloud_compromise", "test_ctcl_cloud.py"),
                              ("03_persistent_security_runtime", "test_runtime_model.py")):
                p = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", test],
                                   cwd=str(v8 / sub), capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", timeout=900,
                                   env={**os.environ, "PYTHONUTF8": "1",
                                        "PYTHONDONTWRITEBYTECODE": "1"})
                out[sub] = {"rc": p.returncode,
                            "summary": (p.stdout or "").strip().splitlines()[-1:]}
            measured["their_suite"] = out
            return all(v["rc"] == 0 for v in out.values()), out

        check("CS01_their_own_test_suites_reproduce_on_this_platform",
              their_suite_reproduces,
              "the shipped validation_results.json was captured on Linux under "
              "/opt/pyvenv; this reruns it on Windows with a different pytest and "
              "cryptography, which is the cross-platform half the package cannot "
              "claim for itself")

        rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
        rep["counts"] = {"checks": len(checks),
                         "passed": sum(1 for v in checks.values() if v["pass"])}
        rep["ok"] = not rep["failures"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
