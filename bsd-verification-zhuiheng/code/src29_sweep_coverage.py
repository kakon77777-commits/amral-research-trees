"""Gate 29 — how much of the 85-document sweep has actually been walked.

數學戰士「墜衡」 / AMRAL Research Lab.

The plan for this line is 85 curated documents, one per round, with order and
depth at the author's discretion. Twenty-six rounds in, the tree's own
checkpoint carries "Phase 1 ~22; Phase 2 ~27" — **estimates**, written by hand
and carried forward. This arm's standing rule is that a number in its records
should be a measurement, and it has not applied that rule to its own progress.

WHAT IS MEASURED, AND IN FOUR BUCKETS BECAUSE ONE WOULD LIE. "Cited" is not
"verified", so a single count would overstate the sweep. Each document lands in
exactly one of:

  subject of a report   — named on a report's `**Subject:**` line. The strongest
                          reading: a round was aimed at it.
  cited in a report     — named in a report's body but not its subject. It was
                          read and used, which is real and is less.
  named in gate code    — appears in a gate's source or docstring but in no
                          report. Something computed from it; nobody wrote it up.
  not mentioned         — no round has touched it in any of the three ways.

MATCHING IS BY FILENAME STEM, NOT BY LINK. Only 17 of the 85 are cited as
markdown links; the rest are named in prose — `30_Two_Witness_Criterion_v0.1`,
"Phase 0 doc 03", `BSD_P5_uGPR_Minimal_Gate…`. A link scan would have reported a
sweep four times smaller than it is, which is the same silent-under-report this
tree has now produced three rounds running (RUN-024's `src02`, RUN-025's Sha
scanner, RUN-026's regulator check). So each document contributes several
aliases, including the `doc NN` form the Phase 0 documents are referred to by,
and the alias set is printed with the result so a reader can see what was
matched on.

Usage:  python code/src29_sweep_coverage.py
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CURATED = ROOT.parent.parent / "amral" / "public" / "bsd"
SUBLINES = ("phase0", "p5", "phase1", "phase2")
OUT = ROOT / "data" / "gate-logs" / "src29-sweep-coverage.json"

SUBJECT_LINE = re.compile(r"^\*\*Subject:\*\*(.*)$", re.M)


def aliases(sub: str, name: str) -> list[str]:
    """The strings a report or gate might use to name this document.

    The stem is the reliable one. The `doc NN` form exists because the Phase 0
    documents are routinely called "Phase 0 doc 05" rather than by filename, and
    dropping it would misfile the four rounds that do exactly that.
    """
    stem = name[:-3] if name.endswith(".md") else name
    out = [name, stem]
    m = re.match(r"^(\d{2})_", stem)
    if m and sub == "phase0":
        n = m.group(1)
        out += [f"doc {n}", f"doc {int(n)}", f"Phase 0 doc {int(n)}"]
    return out


def documents() -> list[dict]:
    rows = []
    for sub in SUBLINES:
        d = CURATED / sub / "files"
        if not d.is_dir():
            raise SystemExit(f"curated corpus not found: {d}")
        for m in sorted(d.glob("*.md")):
            rows.append({"subline": sub, "name": m.name,
                         "aliases": aliases(sub, m.name)})
    return rows


def sources() -> dict:
    reports, gates = {}, {}
    for f in sorted((ROOT / "reports").glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        subj = " ".join(SUBJECT_LINE.findall(text))
        reports[f.name] = {"subject": subj, "body": text}
    for f in sorted((ROOT / "code").glob("src*.py")):
        gates[f.name] = f.read_text(encoding="utf-8", errors="replace")
    return {"reports": reports, "gates": gates}


def classify(doc: dict, src: dict) -> dict:
    subj_hits, body_hits, gate_hits = [], [], []
    for rname, r in src["reports"].items():
        if any(a in r["subject"] for a in doc["aliases"]):
            subj_hits.append(rname)
        elif any(a in r["body"] for a in doc["aliases"]):
            body_hits.append(rname)
    for gname, text in src["gates"].items():
        if any(a in text for a in doc["aliases"]):
            gate_hits.append(gname)
    if subj_hits:
        bucket = "subject of a report"
    elif body_hits:
        bucket = "cited in a report"
    elif gate_hits:
        bucket = "named in gate code"
    else:
        bucket = "not mentioned"
    return {"subline": doc["subline"], "name": doc["name"], "bucket": bucket,
            "subject_of": subj_hits, "cited_in": body_hits[:6],
            "named_in_gates": gate_hits[:6]}


ARTEFACT = re.compile(
    r"`([A-Za-z0-9_./-]*(?:results/[A-Za-z0-9_.-]+|"
    r"[A-Za-z0-9_.-]+\.(?:json|csv|sage|py|txt)))`")


def artefacts_named(src: dict) -> dict:
    """The data artefacts the reports name, as a second axis of coverage.

    This exists because the first axis alone would libel the Phase 1 rounds.
    RUN-004 through RUN-008 and RUN-012 verified that line's computational
    content down to 122,247 isogeny determinations and 247,391 twist pairs —
    and named `results/summary.json`, `algorithm1_removed_census.csv`, the
    `has_isogeny_3` column. They never named a single `.md` in `phase1/files/`.

    So there are two senses of "walked" and this tree has been conflating them:
    the line's computational content verified, and the documents read on the
    record. The plan's unit is the second. Both are counted, and neither is
    presented as the other.
    """
    per_report = {}
    for rname, r in src["reports"].items():
        hits = sorted({m for m in ARTEFACT.findall(r["body"])
                       if not m.endswith(".py")})
        if hits:
            per_report[rname] = hits[:10]
    allhits = sorted({h for v in per_report.values() for h in v})
    return {"reports_naming_a_data_artefact": len(per_report),
            "distinct_artefacts_named": len(allhits),
            "artefacts": allhits[:40],
            "by_report": per_report}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    docs = documents()
    if len(docs) != 85:
        raise SystemExit(f"expected the 85 curated documents, read {len(docs)}")
    src = sources()
    rows = [classify(d, src) for d in docs]

    order = ("subject of a report", "cited in a report", "named in gate code",
             "not mentioned")
    counts = collections.Counter(r["bucket"] for r in rows)
    per_sub = {s: collections.Counter(r["bucket"] for r in rows
                                      if r["subline"] == s)
               for s in SUBLINES}
    untouched = [r for r in rows if r["bucket"] == "not mentioned"]

    log = {
        "gate": "src29 — the sweep's own coverage",
        "documents": len(docs),
        "reports_read": len(src["reports"]),
        "gates_read": len(src["gates"]),
        "matching": ("by filename stem and, for Phase 0, the `doc NN` form. "
                     "Only 17 of the 85 are cited as markdown links, so a link "
                     "scan would report a sweep four times smaller than it is"),
        "bucket_order_strongest_first": list(order),
        "counts": {k: counts.get(k, 0) for k in order},
        "per_subline": {s: {k: per_sub[s].get(k, 0) for k in order}
                        for s in SUBLINES},
        "not_mentioned": [f"{r['subline']}/{r['name']}" for r in untouched],
        "caveat": ("a bucket is a measure of attention, not of correctness. "
                   "Being the subject of a round says a round was aimed at the "
                   "document; what that round actually settled is in its own "
                   "'what this round does not claim' section, every time"),
        "second_axis_data_artefacts": artefacts_named(src),
        "two_senses_of_walked": (
            "the documents read on the record, and the line's computational "
            "content verified. The plan's unit is the first; the Phase 1 rounds "
            "did the second thoroughly and named no document at all. Neither "
            "number is presented as the other"),
        "rows": rows,
        "ok": len(docs) == 85 and len(src["reports"]) > 0,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  {len(docs)} documents, {len(src['reports'])} reports, "
          f"{len(src['gates'])} gates")
    for k in order:
        print(f"    {k:22s} {counts.get(k, 0):3d}")
    print()
    print(f"  {'sub-line':8s} " + "  ".join(f"{k[:9]:>9s}" for k in order))
    for s in SUBLINES:
        print(f"  {s:8s} " + "  ".join(f"{per_sub[s].get(k, 0):9d}" for k in order))
    if untouched:
        print()
        print(f"  not mentioned anywhere ({len(untouched)}):")
        for r in untouched:
            print(f"    {r['subline']}/{r['name']}")
    art = log["second_axis_data_artefacts"]
    print()
    print(f"  second axis: {art['reports_naming_a_data_artefact']} reports name "
          f"a data artefact, {art['distinct_artefacts_named']} distinct")
    print(f"    e.g. {', '.join(art['artefacts'][:6])}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
