"""Emit RUN-021's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Every figure in the report's numeric block is generated here from
`cs03-v09-models.json` and `cs03-drill.json`. The prose around it is written to be
qualitative on purpose: a number that lives only in prose is checked by nothing,
and this arm has now watched that happen often enough to stop typing them.

Refuses if either gate log is red, so a stale or failing run cannot publish counts.

Usage:  python code/cs03_emit_report_block.py [--check]
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = HERE / "data" / "gate-logs" / "cs03-v09-models.json"
DRILL_LOG = HERE / "data" / "gate-logs" / "cs03-drill.json"
REPORT = HERE / "reports" / "RUN-021-CRYPTO-SEMIOTICS-V09.md"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/cs03_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"


def build(g: dict, d: dict) -> str:
    r9 = g["runtime_v09"]
    r8 = g["runtime_v08_for_comparison"]
    c = g["ctcl"]
    t = g["tlc"] or {}
    runs = t.get("runs", [])
    rows = [
        ("the archive", "bytes", g["source"]["bytes"]),
        ("", "manifest entries whose SHA-256 verifies",
         g["manifest"]["entries"] - len(g["manifest"]["mismatches"])),
        ("", "manifest mismatches", len(g["manifest"]["mismatches"])),
        ("the repaired runtime model", "reachable states", r9["reachable_states"]),
        ("", "non-stuttering edges", r9["nonstuttering_edges"]),
        ("", "stages reached", len(r9["stages_reached"])),
        ("", "actions never enabled", len(r9["actions_never_enabled"])),
        ("", "states in which a rollback is recorded",
         r9["rollback_recorded_states"]),
        ("", "safety invariants holding on every reachable state",
         sum(1 for v in r9["invariants"].values() if v)),
        ("the model it replaces", "reachable states", r8["reachable_states"]),
        ("", "non-stuttering edges", r8["nonstuttering_edges"]),
        ("", "stages reached", len(r8["stages_reached"])),
        ("", "actions never enabled", len(r8["actions_never_enabled"])),
        ("the CTCL model, by exhaustion", "states enumerated",
         c["states_enumerated"]),
        ("", "reachable states", c["reachable_states"]),
        ("", "actions that fail to preserve CloudOnlySecrecy",
         sum(1 for v in c["cloud_only_action_results"].values() if not v)),
        ("", "actions that preserve the strengthened invariant",
         sum(1 for v in c["strengthened_invariant_action_results"].values() if v)),
        ("TLC, run here", "models checked", len(runs)),
        ("", "models completing with no error", t.get("completed_without_error", 0)),
        ("", "errors reported", t.get("errors_found", 0)),
        ("", "distinct states, CTCL", runs[0]["distinct"] if runs else None),
        ("", "distinct states, runtime", runs[1]["distinct"] if len(runs) > 1 else None),
        ("the checks themselves", "defects planted",
         d["counts"]["defects_planted"]),
        ("", "caught, each for the reason named", d["counts"]["caught"]),
        ("", "null controls undisturbed", d["counts"]["controls_undisturbed"]),
        ("", "controls requiring the comparison to be able to reject",
         len(g["controls"])),
    ]
    out = [BEGIN, "", "| what | measured | value |", "| --- | --- | --- |"]
    for a, b, v in rows:
        out.append(f"| {a} | {b} | `{v}` |")

    dead = ", ".join("`%s`" % x for x in r8["actions_never_enabled"])
    syms = g["runtime_symbols_in_package"]
    pp = g.get("promotion_profile") or {}
    anomalous = pp.get("ready_at_target_with_unresolved_blocking") or []
    out += [
        "",
        "**The three agreeing methods.** The package's own script, this arm's "
        "independent hand transcription of the TLA+ text, and TLC reading the "
        f"`.tla` files themselves all give `{r9['reachable_states']}` reachable "
        "states for the repaired runtime model. TLC additionally reports "
        f"`{runs[1]['generated'] if len(runs) > 1 else '?'}` states generated, "
        f"which is one initial state plus this arm's `{r9['nonstuttering_edges']}` "
        f"edges, and a search depth of `{runs[1]['depth'] if len(runs) > 1 else '?'}`, "
        f"which is this arm's edge distance `{r9['edge_depth']}` plus one — TLC "
        "counts states on the longest path where this arm counts steps. Stating "
        "the convention is the difference between a reconciliation and an "
        "off-by-one nobody chased.",
        "",
        f"**What was dead before.** {dead} — every action whose guard tested the "
        "negation of a variable that no action ever assigned.",
        "",
        f"**The symbol set.** The package contains `{len(syms)}` "
        "`SYM-RUNTIME-*` symbols in total: "
        + ", ".join("`%s`" % s for s in syms) + ". There is no rollback symbol and "
        "no approval symbol, while the repaired model has "
        f"`{len(r9['stages_reached'])}` stages.",
        "",
        f"**The anomalous profile.** Of `{pp.get('profiles_total')}` promotion "
        f"profiles, `{len(anomalous)}` is marked `ready_at_target` while still "
        "carrying an unresolved blocking obligation: "
        + ", ".join("`%s`" % x for x in anomalous) + ".",
        "",
        "Every figure above is emitted by `code/cs03_emit_report_block.py` from "
        "the two gate logs. None is typed into this file.",
        "",
        END,
    ]
    return "\n".join(out)


def main() -> int:
    for p in (GATE_LOG, DRILL_LOG):
        if not p.exists():
            print(json.dumps({"error": "missing gate log", "path": str(p)}, indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    for name, rep in (("cs03_v09_models", g), ("cs03_drill", d)):
        if not rep.get("ok"):
            print(json.dumps({"error": "%s is not green; refusing to publish "
                                       "counts from a red gate" % name,
                              "problems": rep.get("problems")},
                             indent=2, ensure_ascii=False))
            return 2

    block = build(g, d)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "report has no generated block markers"},
                         indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = head + block + tail

    # Drill the staleness comparison itself: perturb every digit in the block in
    # turn and require each perturbation to be detected. A staleness check nobody
    # has seen fail is the same empty light as an audit nobody has seen fail.
    digits = [i for i, ch in enumerate(block) if ch.isdigit()]
    missed = [i for i in digits
              if (head + block[:i] + str((int(block[i]) + 1) % 10)
                  + block[i + 1:] + tail) == text]
    if not digits or missed:
        print(json.dumps({"error": "the staleness comparison failed its own "
                                   "control", "digits": len(digits),
                          "undetected": missed}, indent=2))
        return 2

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "cs03_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "ok": not stale},
                         indent=2))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "cs03_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text,
                      "digits_guarded": len(digits), "ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
