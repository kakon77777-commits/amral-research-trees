"""Gate 01 — is the certificate ladder used the way its framework defines it?

數學戰士「墜衡」 / AMRAL Research Lab.

Phase 0 doc 03 defines the object every later BSD sub-line reasons with: a
per-curve certificate ladder, so that a curve never stores a bare `BSD
true/false` but records *which rung has been closed by what certificate*.

The framework defines **eleven** rungs, C0 through C10. Two of them carry the
distinction the whole ladder exists for:

    C2  numerical analytic rank — high-precision computation says r_an = r,
        "但未必有 rigorous zero-order certificate". Status: `evidence`.
    C3  rigorous analytic rank — an auditable L-function algorithm, interval
        arithmetic, a Turing-type count, or a theorem.

And the document's own 絕對禁止 list, item 2, forbids exactly the collapse
between them: "`rank()` 回傳一個整數就當成有完整 proof".

WHAT THIS GATE MEASURES. Two things, and the second is why it exists:

  1. Which rungs each of the 85 curated documents actually names, and whether
     any names a rung the framework does not define.
  2. Whether the ladder as SUMMARISED downstream still contains the rungs the
     framework defines — because a summary that drops C1-C5 drops the boundary
     between evidence and proof from a ladder built to hold it.

The second check is aimed at this arm as much as at anyone: the abbreviated
six-rung chain was copied into this tree's own README on the day it opened,
from a derived source, without reading doc 03 first.

Usage:  python code/src01_ladder_vocabulary.py
"""

from __future__ import annotations

import io
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
CURATED = REPO.parent / "amral" / "public" / "bsd"
SUBLINES = ("phase0", "p5", "phase1", "phase2")
LADDER_DOC = CURATED / "phase0" / "files" / "03_BSD_Certificate_Ladder.md"
OUT = ROOT / "data" / "gate-logs" / "src01-ladder-vocabulary.json"

# Where an abbreviated rendering of the ladder is repeated. Each is a file this
# arm can read; each is checked for whether it still carries every defined rung.
# (label, how to read it). The archive README lives on another branch, so it is
# read through git rather than by path — a summary this gate cannot reach must
# be reported unreadable, never counted as carrying every rung.
SUMMARIES = [
    ("agent/bsd tree README", ("git", "origin/agent/bsd:bsd/README.md")),
    ("this arm's own README", ("file", str(ROOT / "README.md"))),
    ("the public BSD page's own summary", ("file", str(CURATED / "index.html"))),
]

RUNG = re.compile(r"\bC(\d{1,2})\b")


def defined_rungs() -> dict[str, str]:
    """Rung -> its heading text, read from the framework document itself."""
    if not LADDER_DOC.exists():
        raise SystemExit(f"framework document not found: {LADDER_DOC}")
    out = {}
    for line in LADDER_DOC.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#+\s*(C\d{1,2})\s*[—\-–|｜]?\s*(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def rungs_in(text: str) -> set[str]:
    """C-rungs named anywhere in a text, code blocks included.

    An earlier version of this function stripped fenced code first, to avoid
    matching a `C1` inside a JSON sample. That made it blind to the thing it
    was written to find: every abbreviated rendering of the ladder in this
    corpus is written INSIDE a code fence, so the gate reported this arm's own
    README as naming no rungs at all. A filter aimed at noise removed the
    signal.
    """
    return {"C" + m.group(1) for m in RUNG.finditer(text)}


def read_summary(how: tuple[str, str]) -> str | None:
    kind, where = how
    if kind == "file":
        p = pathlib.Path(where)
        return p.read_text(encoding="utf-8", errors="replace") if p.exists() else None
    out = subprocess.run(["git", "show", where], cwd=REPO, capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    return out.stdout if out.returncode == 0 and out.stdout else None


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    defined = defined_rungs()
    if not defined:
        raise SystemExit(
            "no rung headings parsed from the framework document. A gate that "
            "silently reads an empty ladder would report every document clean.")

    per_doc, undefined_uses = [], []
    for sub in SUBLINES:
        for m in sorted((CURATED / sub / "files").glob("*.md")):
            used = rungs_in(m.read_text(encoding="utf-8"))
            unknown = sorted(u for u in used if u not in defined)
            if used:
                per_doc.append({"subline": sub, "name": m.name,
                                "rungs": sorted(used, key=lambda r: int(r[1:])),
                                "undefined": unknown})
            if unknown:
                undefined_uses.append({"subline": sub, "name": m.name,
                                       "undefined": unknown})

    coverage = {r: sorted({f"{d['subline']}/{d['name']}" for d in per_doc
                           if r in d["rungs"]}) for r in defined}

    summaries = []
    for label, how in SUMMARIES:
        text = read_summary(how)
        if text is None:
            summaries.append({"where": label, "readable": False,
                              "source": how[1]})
            continue
        used = rungs_in(text)
        dropped = sorted((set(defined) - used), key=lambda r: int(r[1:]))
        summaries.append({
            "where": label, "readable": True,
            "rungs_named": sorted(used, key=lambda r: int(r[1:])),
            "defined_rungs_dropped": dropped,
            "drops_the_evidence_proof_boundary": ("C2" in dropped
                                                  and "C3" in dropped),
        })

    never = sorted((r for r in defined if not coverage[r]),
                   key=lambda r: int(r[1:]))
    log = {
        "gate": "src01_ladder_vocabulary",
        "framework_document": str(LADDER_DOC.relative_to(CURATED.parent.parent)),
        "rungs_defined": {r: defined[r] for r in
                          sorted(defined, key=lambda r: int(r[1:]))},
        "counts": {
            "rungs_defined": len(defined),
            "documents_naming_a_rung": len(per_doc),
            "documents_using_an_undefined_rung": len(undefined_uses),
            "rungs_never_used_outside_the_framework": len(never),
        },
        "rungs_never_used_outside_the_framework": never,
        "documents_using_an_undefined_rung": undefined_uses,
        "coverage_by_rung": {r: len(coverage[r]) for r in
                             sorted(coverage, key=lambda r: int(r[1:]))},
        "summaries": summaries,
        "why_C2_and_C3_matter": (
            "C2 is numerical analytic rank, whose own status line reads "
            "`evidence` and which the framework says need not carry a rigorous "
            "zero-order certificate; C3 is the rigorous one. Doc 03's 絕對禁止 "
            "list forbids treating an integer returned by rank() as a proof. A "
            "summary that renders the ladder as C0 → C6 → … drops both, and "
            "with them the boundary the ladder exists to hold."),
        "not_a_defect": (
            "a rung no document outside the framework uses is not necessarily "
            "unused work — the corpus may simply not have reached it. It is "
            "reported as coverage, not as a finding."),
        "ok": len(undefined_uses) == 0,
    }
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print(f"rungs defined by the framework: {len(defined)}")
    for r in sorted(defined, key=lambda x: int(x[1:])):
        print(f"  {r:<4} {defined[r][:44]:<46} used in {len(coverage[r]):>2} doc(s)")
    print()
    for s in summaries:
        if not s["readable"]:
            print(f"  {s['where']}: NOT READABLE")
            continue
        print(f"  {s['where']}")
        print(f"     names   : {s['rungs_named']}")
        print(f"     drops   : {s['defined_rungs_dropped']}")
        print(f"     drops the evidence/proof boundary (C2+C3): "
              f"{s['drops_the_evidence_proof_boundary']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
