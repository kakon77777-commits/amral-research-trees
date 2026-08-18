"""Can the item-39 recheck actually fail?

數學戰士「墜衡」 / AMRAL Research Lab.

`cs03_v09_models.py` confirms six numbers the package reports, and confirms them
against a real TLC transcript. Confirmation is the failure mode to worry about: a
comparison that agrees is indistinguishable from a comparison that cannot
disagree. So each check is broken in turn and the recheck must go red **for the
reason named**.

Two of the defects target the TLC reconciliation rather than the model walk,
because that is the newest part and the part with the least history.

Every mutation is byte-level and restored under `try/finally`, with a byte
equality check afterwards: a drill that corrupts the tree it audits is a bad
drill.

Usage:  python code/cs03_drill.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
GATE = HERE / "code" / "cs03_v09_models.py"
TLC_LOG = HERE / "data" / "tlc-v09.log"

# (name, file, old, new, substring that must appear in a reported problem)
DEFECTS = [
    # --- the runtime walk
    ("D1_rollback_becomes_unreachable_again", GATE,
     '        out.append(("VerifyFail", ("Rollback", risk, appr, auth, resp, False, rb)))',
     '        pass  # VerifyFail removed',
     "Rollback still unreachable"),
    ("D2_an_unauthorized_response_becomes_possible", GATE,
     '        out.append(("ApplyResponse", ("Verify", risk, appr, True, True, vok, rb)))',
     '        out.append(("ApplyResponse", ("Verify", risk, appr, False, True, vok, rb)))',
     "NoUnauthorizedResponse"),
    ("D3_the_state_count_stops_matching_the_package", GATE,
     '    if stage == "Learn":\n        out.append(("NextCycle", ("Observe", risk, False, auth, False, vok, False)))\n    return out\n\n\ndef succs_v08',
     '    if stage == "Learn":\n        pass\n    return out\n\n\ndef succs_v08',
     "independent enumeration gives"),
    # --- the CTCL exhaustion
    ("D4_the_auxiliary_invariants_are_dropped", GATE,
     '    return cloud_only(s) and ((not s[3]) or s[2]) and ((not s[3]) or s[0])',
     '    return cloud_only(s)',
     "exhaustion gives"),
    # --- the TLC reconciliation
    # This defect is aimed at the RUNTIME counts in spirit, but it mutates the
    # CTCL run instead, and the reason is worth keeping. The runtime counts appear
    # TWICE in a TLC transcript — once on a `Progress(...)` line and again in the
    # final summary — so the obvious anchor matched two look-alikes and the
    # drill's `count == 1` guard reported it UNCAUGHT. Spanning the newline to
    # disambiguate then failed too: TLC's output here is MIXED CRLF and LF, so a
    # literal separator is not portable. The CTCL model finishes in one step and
    # prints no progress line, so its counts occur exactly once. Same check, same
    # reconciliation, an anchor that cannot drift.
    ("D5_the_tlc_transcript_disagrees_with_the_walk", TLC_LOG,
     "16 states generated, 10 distinct states found",
     "16 states generated, 11 distinct states found",
     "this file predicts"),
    ("D6_the_liveness_check_never_ran", TLC_LOG,
     "Checking temporal properties",
     "Skipping temporal properties",
     "liveness property was not actually verified"),
]

TOUCHED = sorted({str(d[1]) for d in DEFECTS})


def run_gate() -> dict:
    p = subprocess.run([sys.executable, str(GATE)], cwd=str(HERE),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=1800)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"ok": None, "problems": ["gate produced no JSON"],
                "tail": (p.stdout + p.stderr)[-800:]}


def main() -> int:
    rep = {"tool": "cs03_drill.py", "subject": str(GATE.name),
           "defects": {}, "controls": {}}

    base = run_gate()
    if not base.get("ok"):
        print(json.dumps({"error": "baseline recheck is not green; refusing to "
                                   "drill from a red baseline",
                          "problems": base.get("problems")},
                         indent=2, ensure_ascii=False))
        return 2
    rep["baseline"] = {"reachable_states": base["runtime_v09"]["reachable_states"],
                       "tlc_runs": len((base.get("tlc") or {}).get("runs", []))}
    if rep["baseline"]["tlc_runs"] != 2:
        print(json.dumps({"error": "no TLC transcript in the baseline, so the "
                                   "two transcript defects would test nothing"},
                         indent=2))
        return 2

    snapshot = {p: pathlib.Path(p).read_bytes() for p in TOUCHED}

    for name, path, old, new, expect in DEFECTS:
        f = pathlib.Path(path)
        raw = f.read_bytes()
        text = raw.decode("utf-8")
        if text.count(old) != 1:
            rep["defects"][name] = {
                "caught": False,
                "note": "anchor matched %d times in %s" % (text.count(old), f.name)}
            continue
        try:
            f.write_bytes(text.replace(old, new, 1).encode("utf-8"))
            res = run_gate()
        finally:
            f.write_bytes(raw)
        if f.read_bytes() != raw:
            rep["defects"][name] = {
                "caught": False, "note": "%s was not restored byte-exactly" % f.name}
            continue
        problems = " | ".join(res.get("problems", []))
        rep["defects"][name] = {
            "caught": (not res.get("ok")) and expect in problems,
            "expected_substring": expect,
            "reported": res.get("problems", [])[:3]}

    # N1 -- a comment must not be a problem, or the gate is simply always red
    f = GATE
    raw = f.read_bytes()
    try:
        f.write_bytes(raw + b"\n# a comment nothing reads\n")
        res = run_gate()
    finally:
        f.write_bytes(raw)
    rep["controls"]["N1_a_comment_is_not_a_problem"] = {
        "undisturbed": bool(res.get("ok")) and f.read_bytes() == raw}

    # N2 -- every touched file restored byte-exactly
    rep["controls"]["N2_every_file_restored_byte_exactly"] = {
        "undisturbed": all(pathlib.Path(p).read_bytes() == snapshot[p]
                           for p in TOUCHED),
        "per_file": {p: pathlib.Path(p).read_bytes() == snapshot[p]
                     for p in TOUCHED}}

    caught = sum(1 for v in rep["defects"].values() if v["caught"])
    rep["counts"] = {"defects_planted": len(DEFECTS), "caught": caught,
                     "controls": len(rep["controls"]),
                     "controls_undisturbed":
                         sum(1 for c in rep["controls"].values()
                             if c["undisturbed"])}
    rep["ok"] = (caught == len(DEFECTS)
                 and all(c["undisturbed"] for c in rep["controls"].values()))
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
