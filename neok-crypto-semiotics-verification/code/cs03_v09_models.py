"""Recheck of NeoK_Crypto_Semiotics_Theory_Compiler_v0.9.zip (source item 39).

數學戰士「墜衡」 / AMRAL Research Lab.

v0.9 adds one layer, `13_external_formal_attempt_v0.9`, and it is a direct answer
to what item 38 found: the v0.8 TLA+ runtime model specified a weaker system than
the one that had been validated, and TLC had never been run. v0.9 repairs the
model, revalidates symbolically with SymPy, and — honestly — refuses to promote
anything to G4 because no model checker was available in its sandbox.

So the questions here are:

  - does the repaired model really reach the 62 states the report claims, when
    the TLA+ text is transcribed independently rather than by running the
    package's own script;
  - what exactly was dead in v0.8, measured rather than recalled;
  - do the CTCL symbolic results reproduce under a DIFFERENT method — exhaustion
    over all sixteen states, not SymPy satisfiability;
  - and does the obligation this model serves actually ask for what the model
    now contains.

The last one is where this run found something.

`--tlc-log FILE` additionally reconciles a real TLC transcript against both.
That matters more than it looks: this script and the package's script are both
TRANSCRIPTIONS of the TLA+ text, and two transcriptions can be wrong in the same
place. TLC is the only participant that reads the artifact itself.

Usage:  python code/cs03_v09_models.py [--tlc-log data/tlc-v09.log]
Env:    CS_SOURCE_ZIP  path to the .zip (default: Neo's source folder)
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import sys
import zipfile
from collections import deque
from itertools import product

HERE = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_ZIP = pathlib.Path(os.environ.get("CS_SOURCE_ZIP", "")) if os.environ.get(
    "CS_SOURCE_ZIP") else (
    pathlib.Path("D:/我的研究/學術討論/論文/數學/考拉茲猜想/最新/"
                 "Collatz_OT_Series_Paper/"
                 "NeoK_Crypto_Semiotics_Theory_Compiler_v0.9.zip"))

ROOT = "NeoK_Crypto_Semiotics_Theory_Compiler_v0.9"
LAYER = ROOT + "/13_external_formal_attempt_v0.9"

# What the package's own report states. Every one of these is compared against a
# quantity this file computes; none is copied into the prose of the report.
REPORTED = {
    "reachable_states": 62,
    "nonstuttering_edges": 86,
    "cycle_avoiding_learn_exists": False,
    "init_implies_strong_invariant": True,
    "cloud_only_secrecy_inductive_by_itself": False,
    "cloud_only_action_results": {"Upload": False, "CompromiseCloud": False,
                                  "StealClientKey": True, "Decrypt": True,
                                  "Stutter": True},
    "strengthened_invariant_implies_cloud_only_secrecy": True,
    "client_key_stolen_decrypt_counterexample_exists": True,
    # The package's headline claim about the repair. It was computed here and
    # compared against nothing until a drill deleted the auxiliary invariants and
    # this file stayed green: a quantity that is emitted but never graded is
    # decoration.
    "strengthened_invariant_action_results": {"Upload": True,
                                              "CompromiseCloud": True,
                                              "StealClientKey": True,
                                              "Decrypt": True, "Stutter": True},
}

LOW, HIGH = "Low", "High"
STAGES = {"Observe", "Model", "Detect", "Prioritize", "AwaitApproval",
          "Respond", "Verify", "Rollback", "Learn"}
RUNTIME_ACTIONS = {"ObserveDone", "ModelDone", "DetectLow", "DetectHigh",
                   "RequestApproval", "PrioritizeDone", "Approve", "Reject",
                   "ApplyResponse", "Deny", "VerifyOK", "VerifyFail",
                   "RollbackDone", "NextCycle"}
# state = (stage, risk, approved, authorized, responseApplied, verificationOK,
#          rollbackRecorded)
RUNTIME_INIT = ("Observe", LOW, False, True, False, True, False)


def succs_v09(s):
    """PersistentSecurityRuntime_v09.tla, transcribed by hand from the text."""
    stage, risk, appr, auth, resp, vok, rb = s
    out = []
    if stage == "Observe":
        out.append(("ObserveDone", ("Model", risk, appr, auth, resp, vok, rb)))
    if stage == "Model":
        out.append(("ModelDone", ("Detect", risk, appr, auth, resp, vok, rb)))
    if stage == "Detect":
        out.append(("DetectLow", ("Prioritize", LOW, appr, auth, resp, vok, rb)))
        out.append(("DetectHigh", ("Prioritize", HIGH, appr, auth, resp, vok, rb)))
    if stage == "Prioritize" and risk == HIGH and not appr:
        out.append(("RequestApproval",
                    ("AwaitApproval", risk, appr, auth, resp, vok, rb)))
    if stage == "Prioritize" and (risk == LOW or appr):
        out.append(("PrioritizeDone", ("Respond", risk, appr, auth, resp, vok, rb)))
    if stage == "AwaitApproval":
        out.append(("Approve", ("Respond", risk, True, auth, resp, vok, rb)))
        out.append(("Reject", ("Learn", risk, False, auth, False, vok, rb)))
    if stage == "Respond" and (risk == LOW or appr):
        out.append(("ApplyResponse", ("Verify", risk, appr, True, True, vok, rb)))
    if stage == "Respond":
        out.append(("Deny", ("Learn", risk, appr, False, False, vok, rb)))
    if stage == "Verify":
        out.append(("VerifyOK", ("Learn", risk, appr, auth, resp, True, rb)))
        out.append(("VerifyFail", ("Rollback", risk, appr, auth, resp, False, rb)))
    if stage == "Rollback":
        out.append(("RollbackDone", ("Learn", risk, appr, auth, False, vok, True)))
    if stage == "Learn":
        out.append(("NextCycle", ("Observe", risk, False, auth, False, vok, False)))
    return out


def succs_v08(s):
    """The SHIPPED v0.8 model, for the before/after.

    The difference that matters: `authorized` and `verificationOK` are never
    assigned by any action there. `Init` sets both TRUE and every action leaves
    them UNCHANGED, so the two guards that test their negation can never hold.
    """
    stage, risk, appr, auth, resp, vok, rb = s
    out = []
    if stage == "Observe":
        out.append(("ObserveDone", ("Model", risk, appr, auth, resp, vok, rb)))
    if stage == "Model":
        out.append(("ModelDone", ("Detect", risk, appr, auth, resp, vok, rb)))
    if stage == "Detect":
        out.append(("DetectLow", ("Prioritize", LOW, appr, auth, resp, vok, rb)))
        out.append(("DetectHigh", ("Prioritize", HIGH, appr, auth, resp, vok, rb)))
    if stage == "Prioritize" and risk == HIGH and not appr:
        out.append(("RequestApproval",
                    ("AwaitApproval", risk, appr, auth, resp, vok, rb)))
    if stage == "Prioritize" and (risk == LOW or appr):
        out.append(("PrioritizeDone", ("Respond", risk, appr, auth, resp, vok, rb)))
    if stage == "AwaitApproval":
        out.append(("Approve", ("Respond", risk, True, auth, resp, vok, rb)))
        out.append(("Reject", ("Learn", risk, False, auth, False, vok, rb)))
    if stage == "Respond" and auth and (risk == LOW or appr):
        out.append(("ApplyResponse", ("Verify", risk, appr, auth, True, vok, rb)))
    if stage == "Respond" and not (auth and (risk == LOW or appr)):
        out.append(("Deny", ("Learn", risk, appr, auth, False, vok, rb)))
    if stage == "Verify" and vok:
        out.append(("VerifyOK", ("Learn", risk, appr, auth, resp, vok, rb)))
    if stage == "Verify" and not vok:
        out.append(("VerifyFail", ("Rollback", risk, appr, auth, resp, vok, rb)))
    if stage == "Rollback":
        out.append(("RollbackDone", ("Learn", risk, appr, auth, False, vok, True)))
    if stage == "Learn":
        out.append(("NextCycle", ("Observe", risk, False, auth, False, vok, False)))
    return out


def walk(succ, init):
    """BFS returning states, non-stuttering edges, depth and the actions ever
    enabled. The depth here is the EDGE distance; TLC counts states on the
    longest path, which is one more, and the report reconciles the two."""
    dist, q, edges, fired = {init: 0}, deque([init]), set(), set()
    while q:
        s = q.popleft()
        for name, t in succ(s):
            fired.add(name)
            if t != s:
                edges.add((s, t))
            if t not in dist:
                dist[t] = dist[s] + 1
                q.append(t)
    return set(dist), edges, max(dist.values()), fired


def has_cycle_avoiding(states, edges, avoid_stage):
    """Is there a cycle in the subgraph that never visits `avoid_stage`?"""
    sub = {s for s in states if s[0] != avoid_stage}
    adj = {s: [] for s in sub}
    for a, b in edges:
        if a in sub and b in sub:
            adj[a].append(b)
    colour, found = {}, [False]

    def dfs(u):
        colour[u] = 1
        for v in adj[u]:
            if colour.get(v, 0) == 1:
                found[0] = True
            elif colour.get(v, 0) == 0:
                dfs(v)
        colour[u] = 2

    for s in sub:
        if colour.get(s, 0) == 0:
            dfs(s)
    return found[0]


# ---- the CTCL model, all sixteen states

CTCL_ALL = list(product([False, True], repeat=4))
CTCL_INIT = (False, False, False, False)
CTCL_ACTIONS = ["Upload", "CompromiseCloud", "StealClientKey", "Decrypt",
                "Stutter"]


def ctcl_succs(s):
    """CTCL_CloudCompromise_v09.tla. `Stutter` is the unchanged step, which the
    package's own action table includes."""
    up, cc, ks, pk = s
    out = []
    if not up:
        out.append(("Upload", (True, cc, ks, pk)))
    if not cc:
        out.append(("CompromiseCloud", (up, True, ks, pk)))
    if not ks:
        out.append(("StealClientKey", (up, cc, True, pk)))
    if up and ks and not pk:
        out.append(("Decrypt", (up, cc, ks, True)))
    out.append(("Stutter", s))
    return out


def cloud_only(s):
    up, cc, ks, pk = s
    return (not (up and cc and not ks)) or (not pk)


def strengthened(s):
    """CloudOnlySecrecy plus the two auxiliary invariants v0.9 adds."""
    return cloud_only(s) and ((not s[3]) or s[2]) and ((not s[3]) or s[0])


def preserved_by(inv, action):
    """Does `inv` survive `action` from EVERY state satisfying it, reachable or
    not? That is what inductiveness means, and it is why the answer differs from
    'holds on all reachable states'."""
    for s in CTCL_ALL:
        if not inv(s):
            continue
        for a, t in ctcl_succs(s):
            if a == action and not inv(t):
                return False, (s, t)
    return True, None


def parse_tlc(log_text):
    """Pull both TLC results out of a real transcript."""
    runs = []
    pat = (r"(\d+) states generated, (\d+) distinct states found, "
           r"(\d+) states left on queue\.\s*\n"
           r"The depth of the complete state graph search is (\d+)\.")
    for m in re.finditer(pat, log_text):
        runs.append({"generated": int(m.group(1)), "distinct": int(m.group(2)),
                     "left_on_queue": int(m.group(3)),
                     "depth": int(m.group(4))})
    return {
        "runs": runs,
        "errors_found": log_text.count("Error:"),
        "completed_without_error":
            log_text.count("Model checking completed. No error has been found."),
        "temporal_properties_checked":
            "Checking temporal properties" in log_text,
        "tlc_version": (re.search(r"TLC2 Version [^\r\n]+", log_text) or
                        [None])[0] if re.search(r"TLC2 Version", log_text)
                       else None,
    }


def main():
    rep = {"tool": "cs03_v09_models.py", "subject": "source item 39, v0.9",
           "problems": [], "controls": {}}

    # ---- 0. the archive, its manifest, and the obligation this model serves
    if DEFAULT_ZIP.exists():
        raw = DEFAULT_ZIP.read_bytes()
        rep["source"] = {"name": DEFAULT_ZIP.name, "bytes": len(raw),
                         "sha256": hashlib.sha256(raw).hexdigest()}
        z = zipfile.ZipFile(DEFAULT_ZIP)
        names = set(z.namelist())
        man_name = LAYER + "/manifest_v0.9.json"
        if man_name in names:
            man = json.loads(z.read(man_name).decode("utf-8"))
            bad = []
            for e in man:
                p = ROOT + "/" + e["path"]
                if p not in names:
                    bad.append([e["path"], "missing"])
                    continue
                b = z.read(p)
                if hashlib.sha256(b).hexdigest() != e["sha256"]:
                    bad.append([e["path"], "sha256"])
                elif len(b) != e["size"]:
                    bad.append([e["path"], "size"])
            listed = {e["path"] for e in man}
            actual = {n[len(ROOT) + 1:] for n in names
                      if n.startswith(LAYER + "/") and not n.endswith("/")}
            rep["manifest"] = {"entries": len(man), "mismatches": bad,
                               "unlisted_in_layer_13": sorted(actual - listed)}
            if bad:
                rep["problems"].append("manifest mismatches: %r" % (bad[:4],))
        obl_files = [n for n in names if n.endswith("obligations_v0.8.jsonl")]
        if obl_files:
            for line in z.read(obl_files[0]).decode("utf-8").splitlines():
                if "OBL-N21-005-008" in line:
                    o = json.loads(line)
                    rep["obligation"] = {
                        "id": o["obligation_id"], "claim_id": o["claim_id"],
                        "state": o["state"], "gate": o["gate"],
                        "blocking": o.get("blocking"),
                        "claim_text": o.get("claim_text"),
                        "completion_criteria": o["completion_criteria"],
                        "symbol_ids": o.get("symbol_ids", []),
                        "symbol_count": len(o.get("symbol_ids", [])),
                    }
                    break
        prof_files = [n for n in names if n.endswith("promotion_profiles_v0.8.jsonl")]
        if prof_files:
            rows = [json.loads(l) for l in
                    z.read(prof_files[0]).decode("utf-8").splitlines() if l.strip()]
            hit = [r for r in rows if r.get("claim_id") == "CL-N21-005"]
            rep["promotion_profile"] = {
                "profiles_total": len(rows),
                "CL-N21-005": hit[0] if hit else None,
                "ready_at_target_with_unresolved_blocking": [
                    r["claim_id"] for r in rows
                    if r.get("promotion_decision") == "ready_at_target"
                    and r.get("unresolved_blocking_count", 0) > 0],
            }
        blob = "\n".join(z.read(n).decode("utf-8", "replace") for n in names
                         if n.endswith((".jsonl", ".json", ".csv", ".md")))
        rep["runtime_symbols_in_package"] = sorted(
            set(re.findall(r"SYM-RUNTIME-[A-Z]+", blob)))
    else:
        rep["problems"].append("source archive not found at %s" % DEFAULT_ZIP)

    # ---- 1. the repaired runtime model, and the one it replaces
    s9, e9, d9, f9 = walk(succs_v09, RUNTIME_INIT)
    s8, e8, d8, f8 = walk(succs_v08, RUNTIME_INIT)
    rep["runtime_v09"] = {
        "reachable_states": len(s9), "nonstuttering_edges": len(e9),
        "edge_depth": d9, "stages_reached": sorted({s[0] for s in s9}),
        "actions_never_enabled": sorted(RUNTIME_ACTIONS - f9),
        "rollback_reachable": any(s[0] == "Rollback" for s in s9),
        "rollback_recorded_states": sum(1 for s in s9 if s[6]),
        "cycle_avoiding_learn_exists": has_cycle_avoiding(s9, e9, "Learn"),
        "invariants": {
            "TypeOK": all(s[0] in STAGES and s[1] in (LOW, HIGH) for s in s9),
            "HighRiskApproval":
                all((not (s[1] == HIGH and s[4])) or s[2] for s in s9),
            "NoUnauthorizedResponse": all((not s[4]) or s[3] for s in s9),
            "RollbackRecordedOnlyAtLearn":
                all((not s[6]) or s[0] == "Learn" for s in s9),
        },
    }
    rep["runtime_v08_for_comparison"] = {
        "reachable_states": len(s8), "nonstuttering_edges": len(e8),
        "edge_depth": d8, "stages_reached": sorted({s[0] for s in s8}),
        "actions_never_enabled": sorted(RUNTIME_ACTIONS - f8),
        "authorized_ever_false": any(not s[3] for s in s8),
        "verificationOK_ever_false": any(not s[5] for s in s8),
        "rollback_recorded_ever_true": any(s[6] for s in s8),
    }
    for k in ("reachable_states", "nonstuttering_edges",
              "cycle_avoiding_learn_exists"):
        if rep["runtime_v09"][k] != REPORTED[k]:
            rep["problems"].append(
                "package reports %s = %r; independent enumeration gives %r"
                % (k, REPORTED[k], rep["runtime_v09"][k]))
    for k, v in rep["runtime_v09"]["invariants"].items():
        if not v:
            rep["problems"].append("runtime invariant %s fails" % k)
    if not rep["runtime_v09"]["rollback_reachable"]:
        rep["problems"].append("Rollback still unreachable in v0.9")

    # ---- 2. the CTCL model, by exhaustion rather than by satisfiability
    cs, ce, cd, _cf = walk(ctcl_succs, CTCL_INIT)
    cloud_by_action = {a: preserved_by(cloud_only, a)[0] for a in CTCL_ACTIONS}
    strong_by_action = {a: preserved_by(strengthened, a)[0] for a in CTCL_ACTIONS}
    strong_set = {s for s in CTCL_ALL if strengthened(s)}
    rep["ctcl"] = {
        "states_enumerated": len(CTCL_ALL),
        "reachable_states": len(cs), "nonstuttering_edges": len(ce),
        "edge_depth": cd,
        "init_implies_strong_invariant": strengthened(CTCL_INIT),
        "cloud_only_secrecy_inductive_by_itself": all(cloud_by_action.values()),
        "cloud_only_action_results": cloud_by_action,
        "strengthened_invariant_action_results": strong_by_action,
        "strengthened_invariant_implies_cloud_only_secrecy":
            all(cloud_only(s) for s in CTCL_ALL if strengthened(s)),
        "client_key_stolen_decrypt_counterexample_exists":
            any(s[2] and s[3] for s in cs),
        "cloud_only_holds_on_every_reachable_state":
            all(cloud_only(s) for s in cs),
        # Not claimed by the package, and stronger than what it does claim: the
        # strengthening is not merely sufficient for induction, it characterises
        # reachability exactly, so no further auxiliary invariant is available.
        "strengthened_set_equals_reachable_set": strong_set == cs,
        "counterexamples_to_cloud_only_induction": {
            a: {"from": list(preserved_by(cloud_only, a)[1][0]),
                "to": list(preserved_by(cloud_only, a)[1][1])}
            for a in CTCL_ACTIONS if not cloud_by_action[a]},
    }
    for k in ("init_implies_strong_invariant",
              "cloud_only_secrecy_inductive_by_itself",
              "cloud_only_action_results",
              "strengthened_invariant_action_results",
              "strengthened_invariant_implies_cloud_only_secrecy",
              "client_key_stolen_decrypt_counterexample_exists"):
        if rep["ctcl"][k] != REPORTED[k]:
            rep["problems"].append(
                "package reports %s = %r; exhaustion gives %r"
                % (k, REPORTED[k], rep["ctcl"][k]))
    if not rep["ctcl"]["cloud_only_holds_on_every_reachable_state"]:
        rep["problems"].append("CloudOnlySecrecy fails on a reachable state")
    # This one is not the package's claim, it is this run's. A finding that is
    # published has to be graded by something that runs, or it is prose.
    if not rep["ctcl"]["strengthened_set_equals_reachable_set"]:
        rep["problems"].append(
            "the strengthened invariant no longer characterises reachability "
            "exactly, so this run's claim that it is the strongest available "
            "inductive invariant is stale")

    # ---- 3. a real TLC transcript, if one was supplied
    log = None
    if "--tlc-log" in sys.argv:
        log = pathlib.Path(sys.argv[sys.argv.index("--tlc-log") + 1])
    elif (HERE / "data" / "tlc-v09.log").exists():
        log = HERE / "data" / "tlc-v09.log"
    if log and log.exists():
        t = parse_tlc(log.read_text(encoding="utf-8", errors="replace"))
        rep["tlc"] = t
        # TLC's depth counts STATES on the longest path; `walk` counts EDGES, so
        # the prediction is one more. Stating the convention is the difference
        # between a reconciliation and an off-by-one nobody chased.
        want = [
            {"distinct": len(cs), "generated": 1 + len(ce), "depth": cd + 1},
            {"distinct": len(s9), "generated": 1 + len(e9), "depth": d9 + 1},
        ]
        rep["tlc_predicted_by_this_file"] = want
        if len(t["runs"]) != 2:
            rep["problems"].append(
                "expected two TLC runs in the transcript, found %d"
                % len(t["runs"]))
        else:
            for i, (got, exp) in enumerate(zip(t["runs"], want)):
                for k in exp:
                    if got[k] != exp[k]:
                        rep["problems"].append(
                            "TLC run %d reports %s = %r; this file predicts %r"
                            % (i, k, got[k], exp[k]))
        if t["completed_without_error"] != 2:
            rep["problems"].append(
                "TLC did not report both models clean (%d clean completions)"
                % t["completed_without_error"])
        if not t["temporal_properties_checked"]:
            rep["problems"].append(
                "the TLC transcript contains no temporal-property check, so the "
                "liveness property was not actually verified")
    else:
        rep["tlc"] = None

    # ---- controls. A comparison that cannot reject proves nothing.
    rep["controls"]["C1_the_two_models_differ"] = {
        "detected": len(s9) != len(s8) and len(e9) != len(e8),
        "v09_states": len(s9), "v08_states": len(s8)}
    rep["controls"]["C2_v08_really_had_dead_actions"] = {
        "detected": 0 < len(RUNTIME_ACTIONS - f8) < len(RUNTIME_ACTIONS),
        "dead": sorted(RUNTIME_ACTIONS - f8)}
    rep["controls"]["C3_v09_has_no_dead_actions"] = {
        "detected": not (RUNTIME_ACTIONS - f9)}
    s_less, e_less, _d, _f = walk(
        lambda s: [(n, t) for n, t in succs_v09(s) if n != "VerifyFail"],
        RUNTIME_INIT)
    rep["controls"]["C4_removing_an_action_changes_the_walk"] = {
        "detected": len(s_less) < len(s9) and len(e_less) < len(e9),
        "states_without_VerifyFail": len(s_less)}
    rep["controls"]["C5_the_induction_check_can_reject"] = {
        "detected": sum(1 for v in cloud_by_action.values() if not v) == 2}
    rep["controls"]["C6_strengthening_is_strict"] = {
        "detected": len(strong_set) < sum(1 for s in CTCL_ALL if cloud_only(s)),
        "cloud_only_states": sum(1 for s in CTCL_ALL if cloud_only(s)),
        "strengthened_states": len(strong_set)}
    rep["controls"]["C7_the_cycle_detector_can_say_yes"] = {
        "detected": has_cycle_avoiding(s9, e9, "NoSuchStage")}

    rep["ok"] = (not rep["problems"]
                 and all(c["detected"] for c in rep["controls"].values()))
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
