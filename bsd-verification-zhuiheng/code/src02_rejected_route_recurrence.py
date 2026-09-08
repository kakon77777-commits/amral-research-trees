"""Gate 02 — did the rejected route stay rejected?

數學戰士「墜衡」 / AMRAL Research Lab.

Phase 0 doc 05 is the corpus's most self-critical act: a formal audit of Neo.K's
own earlier "lattice-point rank convergence" idea, ending in

    Archive as exploratory analogy; do not use as Phase 1 proof route.

Reading the audit is one job and is done in RUN-003. This gate does the other
one, which reading cannot do: **a verdict that nothing downstream honours is a
verdict in name only.** So the whole corpus is scanned for the vocabulary of the
rejected route, and every hit is attributed to the document that carries it.

WHAT A HIT MEANS, AND WHAT IT DOES NOT. A later document mentioning the grid
route is not a violation. Doc 05 itself keeps four engineering ideas from it —
multi-scale checking, representation consistency, exact certificates, limit
audit — and says so. The finding would be a document *leaning on* the rejected
inference, and no regex can decide that. So this gate reports **where to look**,
with enough context to read, and refuses to call a hit a defect.

The one thing it can decide mechanically: whether the four salvage conditions
GR-1 to GR-4, which doc 05 says are all unmet, are ever claimed as met.

Usage:  python code/src02_rejected_route_recurrence.py
"""

from __future__ import annotations

import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
CURATED = REPO.parent / "amral" / "public" / "bsd"
SUBLINES = ("phase0", "p5", "phase1", "phase2")
AUDIT = "05_Internal_Grid_Rank_Audit.md"
OUT = ROOT / "data" / "gate-logs" / "src02-rejected-route.json"

# The rejected route's own vocabulary, taken from doc 05's description of it.
ROUTE = {
    "grid/lattice object": re.compile(r"格點|\bgrid\b|\blattice\b", re.I),
    "the a -> 0 limit": re.compile(r"a\s*(?:\\to|→|->)\s*0"),
    "continuity guarantees equality": re.compile(r"連續性.{0,12}(?:保證|推出)|continuity.{0,20}(?:guarantee|imply)", re.I),
    "lattice L-function": re.compile(r"L_?\{?a\}?\s*\(\s*E"),
}
# The four salvage conditions. Doc 05: 目前四項皆未完成.
SALVAGE = re.compile(r"\bGR-?([1-4])\b")
CLAIMED_MET = re.compile(r"(GR-?[1-4])[^\n]{0,60}?(PASS|closed|已完成|成立|滿足|proved)", re.I)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    docs = []
    for sub in SUBLINES:
        d = CURATED / sub / "files"
        if not d.is_dir():
            raise SystemExit(f"curated corpus not found: {d}")
        for m in sorted(d.glob("*.md")):
            docs.append((sub, m))
    if not docs:
        raise SystemExit("no documents read; an empty scan reports every route clean")

    audit_seen = any(m.name == AUDIT for _, m in docs)
    if not audit_seen:
        raise SystemExit(
            f"{AUDIT} is not in the corpus. This gate measures whether a verdict "
            "held; without the verdict there is nothing to measure.")

    hits, salvage_hits, claimed = [], [], []
    for sub, m in docs:
        text = m.read_text(encoding="utf-8")
        lines = text.splitlines()
        for label, pat in ROUTE.items():
            for i, line in enumerate(lines):
                if pat.search(line):
                    hits.append({"subline": sub, "name": m.name, "signal": label,
                                 "line_no": i + 1, "line": line.strip()[:160]})
        for mm in SALVAGE.finditer(text):
            salvage_hits.append({"subline": sub, "name": m.name,
                                 "condition": "GR-" + mm.group(1)})
        for mm in CLAIMED_MET.finditer(text):
            claimed.append({"subline": sub, "name": m.name,
                            "text": mm.group(0).strip()[:120]})

    outside = [h for h in hits if h["name"] != AUDIT]
    by_doc: dict[str, list[str]] = {}
    for h in outside:
        by_doc.setdefault(f"{h['subline']}/{h['name']}", []).append(h["signal"])

    log = {
        "gate": "src02_rejected_route_recurrence",
        "verdict_audited": ("Phase 0 doc 05: archive as exploratory analogy; "
                            "do not use as Phase 1 proof route"),
        "what_a_hit_means": (
            "a mention is not a violation. Doc 05 itself keeps four engineering "
            "ideas from the rejected route and says so. This gate reports where "
            "to look, with the line, and refuses to call a hit a defect — that "
            "judgement needs reading, and is made in the report, not here."),
        "counts": {
            "documents_scanned": len(docs),
            "route_signal_hits_total": len(hits),
            "hits_inside_the_audit_itself": len(hits) - len(outside),
            "hits_outside_the_audit": len(outside),
            "documents_outside_the_audit_with_a_hit": len(by_doc),
            "GR_condition_mentions_outside_the_audit": sum(
                1 for s in salvage_hits if s["name"] != AUDIT),
            "GR_conditions_claimed_met_anywhere": len(claimed),
        },
        "documents_outside_the_audit_with_a_hit": {
            k: sorted(set(v)) for k, v in sorted(by_doc.items())},
        "hits_outside_the_audit": outside,
        "GR_conditions_claimed_met": claimed,
        "ok": len(claimed) == 0,
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print(json.dumps(log["counts"], indent=2, ensure_ascii=False))
    if by_doc:
        print()
        print("  documents outside the audit carrying route vocabulary:")
        for k, v in sorted(by_doc.items()):
            print(f"    {k}")
            print(f"       {sorted(set(v))}")
    if claimed:
        print()
        print("  GR-condition claimed met (doc 05 says all four are unmet):")
        for c in claimed:
            print(f"    {c['subline']}/{c['name']}: {c['text']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
