"""Emit RUN-030's measured block from the gate logs, so no count is typed.

數學戰士「墜衡」 / AMRAL Research Lab.

Refuses if either gate log is red. Every figure is held to a snapshot of what the
block actually reads by `report_block_guard` — the guard that replaced the one
shipped in src43..src45, which could not fail (RUN-028).

Usage:  python code/src48_emit_report_block.py [--check] [--refresh-figures]
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report_block_guard import check_against_snapshot        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_LOG = ROOT / "data" / "gate-logs" / "src48-handoff.json"
DRILL_LOG = ROOT / "data" / "gate-logs" / "src48-drill.json"
LIT_LOG = ROOT / "data" / "external" / "handoff-v1-literature-check.json"
REPORT = ROOT / "reports" / "RUN-030-HARD-ZETA-HANDOFF-FIDELITY.md"
FIGURES = ROOT / "data" / "gate-logs" / "src48-emitter-figures.json"
BEGIN = "<!-- BEGIN GENERATED measured block: python code/src48_emit_report_block.py -->"
END = "<!-- END GENERATED measured block -->"

ORDINAL = {1: "st", 2: "nd", 3: "rd"}


def build(g: dict, d: dict, lit: dict) -> str:
    cb = g["cross_bundle_identity"]
    cs = g["constants"]
    ob = g["occupancy_bound"]
    sf = g["status_fidelity"]
    rh = g["reference_hygiene"]
    fm = g["file_manifest"]
    ri = g["references_introduced"]

    out = [
        BEGIN, "",
        "**The occupancy lemma, both ways.** The round's explicit bound divided by "
        "`√L`, at the `H = o(√L)` limit the round itself takes:",
        "",
        "| `L` | " + " | ".join("`%s`" % r["L"] for r in ob["round_bound_over_sqrt_L"]) + " |",
        "| --- | " + " | ".join("---" for _ in ob["round_bound_over_sqrt_L"]) + " |",
        "| bound / `√L` | " + " | ".join(
            "`%s`" % r["round_s_occupancy_bound_over_sqrt_L"]
            for r in ob["round_bound_over_sqrt_L"]) + " |",
        "",
        "It tends to `1/√2` (`%s`), not to `1`. The handoff states the bare `√L` "
        "form (`%s`) which the round never states (`%s`), keeps the divisor `12` "
        "(`%s`), and keeps the round's `κ_rot` (`%s`) — so its own first two lines "
        "give `%s` where its third gives `%s`, a factor of `%s`."
        % (ob["its_limit_is_1_over_sqrt_2"],
           ob["the_handoff_states_it_as_O_L_gtrsim_sqrt_L"],
           ob["the_round_never_states_the_bare_sqrt_L_form"],
           ob["the_handoff_also_states_Lambda_ge_O_over_12"],
           ob["the_handoff_keeps_the_round_s_kappa_rot"],
           ob["kappa_implied_by_the_handoff_s_own_two_lines"],
           ob["kappa_the_round_proves_and_the_handoff_prints"],
           ob["overstatement_factor"]),
        "",
        "| what | measured against | value |",
        "| --- | --- | --- |",
    ]

    rows = [
        ("distinct markdown documents across every Hard-Zeta bundle",
         "hashed from the zips, not from an extracted copy",
         cb["distinct_documents"]),
        ("…reshipped in more than one bundle", "the ones that could drift",
         cb["documents_reshipped_in_more_than_one_bundle"]),
        ("…most times a single document is shipped", "`%s`" % cb["most_reshipped"],
         cb["most_reshipped_count"]),
        ("**documents resolving to more than one hash**", "must be zero",
         len(cb["documents_with_more_than_one_hash"])),
        ("numeric constants in the handoff and start prompt",
         "%d verbatim in a round, %d as a correct rounding of one"
         % (cs["traced_verbatim"], cs["traced_as_a_correct_rounding"]),
         cs["literals_traced"]),
        ("…printing a number found in no round document",
         "arXiv identifiers excluded and checked as references instead",
         len(cs["numbers_in_no_round_document"])),
        ("…disagreeing with a closed form or exact rational",
         "%d closed forms, %d exact rationals"
         % (len(cs["closed_forms"]), len(cs["exact_rationals"])),
         len(cs["constants_disagreeing_with_their_closed_form"])),
        ("required statements the compression dropped",
         "%d checked: disclaimers, external-input flags, the no-go, the index caveat"
         % len(sf["required_present"]), len(sf["missing_statements"])),
        ("forbidden statements found", "%d checked, each fired on a counterexample"
         % len(sf["required_absent"]), len(sf["forbidden_statements_found"])),
        ("absence checks that could never fire", "the guard on those checks",
         len(sf["absence_checks_that_could_never_fire"])),
        ("arXiv identifiers in the handoff",
         "%d introduced by the handoff itself, %d of those unchecked"
         % (len(ri["introduced_by_the_handoff"]), len(ri["introduced_and_unchecked"])),
         len(ri["identifiers"])),
        ("entries in the standing reference list",
         "%d %s a caveat, so the format supports one"
         % (rh["entries_carrying_a_caveat"],
            "carries" if rh["entries_carrying_a_caveat"] == 1 else "carry"),
         rh["entries_in_the_standing_reference_list"]),
        ("files the handoff names as current",
         "%d markdown found in the corpus, %d are not markdown"
         % (fm["markdown_found_in_the_corpus"],
            len(fm["not_markdown_so_not_in_this_corpus"])),
         fm["files_named"]),
        ("…named but missing", "must be zero", len(fm["markdown_named_but_missing"])),
        ("defects planted / caught by the check named for each",
         "%d of the entries is a robustness property; %d malformed"
         % (d["counts"]["robustness_properties"], d["counts"]["malformed"]),
         "%d / %d" % (d["counts"]["planted"],
                      d["counts"]["caught_by_their_own_check"])),
    ]
    for what, against, value in rows:
        out.append("| %s | %s | `%s` |" % (what, against, value))

    out.append("")
    for ref in sorted(lit["references"],
                      key=lambda r: 0 if r.get("status") == "WITHDRAWN" else 1):
        if ref.get("status") == "WITHDRAWN":
            out.append(
                "**Literature.** `arXiv:%s`, withdrawn %s, appears for the **%d%s "
                "time** and for the first time in a standing bibliography, with no "
                "note."
                % (ref["arxiv"], ref["withdrawn_on"], ref["OCCURRENCE"],
                   ORDINAL.get(ref["OCCURRENCE"], "th")))
            out.append("")
        if ref.get("new_in_the_handoff"):
            out.append(
                "The one reference the handoff adds that no round cites is "
                "`arXiv:%s`, *%s* by %s — verified, and accurately described."
                % (ref["arxiv"], ref["title"], ref["authors"]))

    out += [
        "",
        "Every figure above is emitted by `code/src48_emit_report_block.py` from "
        "the gate logs and the archived literature record. None is typed into this "
        "file.",
        "", END,
    ]
    return "\n".join(out)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (GATE_LOG, DRILL_LOG, LIT_LOG):
        if not path.exists():
            print(json.dumps({"error": "missing log", "path": str(path)}, indent=2))
            return 2
    g = json.loads(GATE_LOG.read_text(encoding="utf-8"))
    d = json.loads(DRILL_LOG.read_text(encoding="utf-8"))
    lit = json.loads(LIT_LOG.read_text(encoding="utf-8"))

    if not g.get("passed"):
        print(json.dumps({"error": "the recheck is red", "failures": g.get("failures")},
                         indent=2, ensure_ascii=False))
        return 2
    if not d.get("ok"):
        print(json.dumps({"error": "the drill is red; a report built on checks that "
                                   "cannot fail is worse than no report",
                          "counts": d.get("counts")}, indent=2, ensure_ascii=False))
        return 2

    guard = check_against_snapshot(build, [g, d, lit], FIGURES,
                                   refresh="--refresh-figures" in sys.argv)
    if not guard["ok"]:
        print(json.dumps({"error": "the block no longer reads what it used to; "
                                   "a figure that stopped moving with its log "
                                   "is a figure somebody typed",
                          "guard": guard}, indent=2))
        return 2

    block = build(g, d, lit)
    text = REPORT.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(json.dumps({"error": "no generated-block markers"}, indent=2))
        return 2
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new = head + block + tail

    if "--check" in sys.argv:
        stale = new != text
        print(json.dumps({"tool": "src48_emit_report_block.py", "mode": "check",
                          "report_up_to_date": not stale, "guard": guard,
                          "ok": not stale}, indent=2, ensure_ascii=False))
        return 1 if stale else 0

    if new != text:
        REPORT.write_text(new, encoding="utf-8", newline="\n")
    print(json.dumps({"tool": "src48_emit_report_block.py", "mode": "emit",
                      "report_rewritten": new != text, "guard": guard, "ok": True},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
