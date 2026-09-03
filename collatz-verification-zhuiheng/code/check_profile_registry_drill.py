"""Drill: does the registry-agreement check actually refuse anything?

數學戰士「墜衡」 / AMRAL Research Lab.

On the real registry every comparison agrees, which is the state in which a
check stops being evidence. Each way the two artifacts can diverge is driven
here with a crafted registry.

The last defect is the one that matters most and is the easiest to get wrong:
with no registry reachable, the answer must be `unmeasured` and NOT ok. A check
that cannot run has no verdict, and a green light in that state is worse than
no check at all — it is the shape this sweep spent seventy-three rounds
cataloguing, applied to the mechanism built from those lessons.

Usage:  python code/check_profile_registry_drill.py
"""

from __future__ import annotations

import copy
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

import check_profile_registry as R  # noqa: E402


def good_registry() -> dict:
    return {
        "registry": "amral-results-profiles",
        "profiles": [{"key": k, "label": k, "description": "", "status": "active",
                      "history": []} for k in sorted(R.V.PROFILES)],
        "lines": [
            {"research_line_id": "line-a", "satisfies": ["results-envelope/1"]},
        ],
    }


def good_log() -> dict:
    return {"files": [{"research_line_id": "line-a",
                       "satisfies": ["results-envelope/1"]}]}


def main() -> int:
    try:
        # reconfigure, not a fresh TextIOWrapper: wrapping sys.stdout.buffer a
        # second time in one process closes the first wrapper and takes the
        # underlying buffer with it, so main() could not be called twice.
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):                 # pragma: no cover
        pass

    defects: dict[str, dict] = {}
    controls: dict[str, dict] = {}

    # D1 - a profile registered that this tree does not implement.
    reg = good_registry()
    reg["profiles"].append({"key": "results-invented/9", "label": "x",
                            "description": "", "status": "active", "history": []})
    got = R.compare(reg)
    defects["D1_a_registered_profile_nobody_implements"] = {
        "why": ("a renderer told a profile exists would ask for a verdict no "
                "code can produce"),
        "refused": not got["agree"],
        "named_check": got["registered_not_implemented"] == ["results-invented/9"],
        "reported": got,
    }

    # D2 - a profile implemented that the registry does not carry.
    reg = good_registry()
    dropped = reg["profiles"].pop()["key"]
    got = R.compare(reg)
    defects["D2_an_implemented_profile_nobody_registered"] = {
        "why": ("a rule with no registered reason is a rule nobody agreed to; "
                "the registry exists so a profile cannot appear without one"),
        "refused": not got["agree"],
        "named_check": got["implemented_not_registered"] == [dropped],
        "reported": got,
    }

    # D3 - the registry's satisfaction has drifted from the measurement.
    reg = good_registry()
    reg["lines"][0]["satisfies"] = ["results-envelope/1", "results-claims/1"]
    got = R.compare_measurement(reg, good_log())
    defects["D3_registry_satisfaction_drifted_from_the_measurement"] = {
        "why": ("the registry is built from that log; drift means one was "
                "regenerated without the other and the registry now describes "
                "a state that does not hold"),
        "refused": not got["agree"],
        "named_check": got["drifted"] == ["line-a"],
        "reported": got,
    }

    # D4 - a line measured but absent from the registry entirely.
    reg = good_registry()
    reg["lines"] = []
    got = R.compare_measurement(reg, good_log())
    defects["D4_a_measured_line_missing_from_the_registry"] = {
        "why": "a line the registry has never heard of is not a governed line",
        "refused": not got["agree"],
        "named_check": got["drifted"] == ["line-a"],
        "reported": got,
    }

    # D5 - nothing readable. The verdict must be `unmeasured`, and not ok.
    keep_mirror, keep_live = R.MIRROR, R.LIVE
    try:
        R.MIRROR = ROOT / "data" / "external" / "__no_such_registry__.json"
        R.LIVE = ROOT / "__no_such_live_registry__.json"
        rc = R.main()
        state = json.loads(R.OUT.read_text(encoding="utf-8"))
    finally:
        R.MIRROR, R.LIVE = keep_mirror, keep_live
        R.main()                       # restore the real archived verdict
    defects["D5_no_registry_reachable_is_unmeasured_not_agreement"] = {
        "why": ("a check that cannot run has no verdict; reporting agreement "
                "there is worse than not checking at all"),
        "refused": rc != 0 and state.get("ok") is False,
        "named_check": state.get("state") == "unmeasured",
        "reported": {"exit": rc, "state": state.get("state"), "ok": state.get("ok")},
    }

    # Controls.
    got = R.compare(good_registry())
    controls["C1_the_healthy_registry_agrees"] = {
        "why": "the real state must pass, or the drill above proves nothing",
        "undisturbed": got["agree"] and got["count"] == len(R.V.PROFILES),
        "detail": got,
    }

    reg = good_registry()
    for p in reg["profiles"]:
        p["status"] = "converged"
        p["description"] = "rewritten by the registry's own governance"
        p["history"] = [{"event": "converged", "reason": "because"}]
    got = R.compare(reg)
    controls["C2_status_and_prose_are_the_registry_s_to_change"] = {
        "why": ("this check owns the SET of profiles, not their lifecycle or "
                "wording; over-reaching would make the registry unable to "
                "govern the thing it was moved out to govern"),
        "undisturbed": got["agree"],
        "detail": got,
    }

    got = R.compare_measurement(good_registry(), {"not_a_log": True})
    controls["C3_an_absent_measurement_is_reported_not_assumed"] = {
        "why": ("with nothing to compare against, the answer is 'not "
                "comparable', which the caller treats as failure rather than "
                "silently as agreement"),
        "undisturbed": got.get("comparable") is False and "agree" not in got,
        "detail": got,
    }

    planted = len(defects)
    caught = sum(1 for d in defects.values() if d["refused"] and d["named_check"])
    undisturbed = sum(1 for c in controls.values() if c["undisturbed"])

    log = {
        "tool": "check_profile_registry_drill.py",
        "subject": "code/check_profile_registry.py",
        "note": ("each defect must be refused by the comparison named for it. "
                 "D5 is the load-bearing one: an unreachable registry must "
                 "report `unmeasured`, never agreement"),
        "defects": defects,
        "controls": controls,
        "counts": {
            "defects_planted": planted,
            "defects_caught_by_the_named_check": caught,
            "controls": len(controls),
            "controls_undisturbed": undisturbed,
        },
        "ok": caught == planted and undisturbed == len(controls),
    }
    out = ROOT / "data" / "gate-logs" / "profile-registry-drill.json"
    out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"counts": log["counts"], "ok": log["ok"]},
                     indent=2, ensure_ascii=False))
    for name, d in defects.items():
        if not (d["refused"] and d["named_check"]):
            print("  SURVIVED:", name, d)
    for name, c in controls.items():
        if not c["undisturbed"]:
            print("  DISTURBED:", name, c)
    print(f"wrote {out.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
