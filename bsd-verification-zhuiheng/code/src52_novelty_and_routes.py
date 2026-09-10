"""Gate 52 — the novelty rule and the route matrix, audited against what this line did.

數學戰士「墜衡」 / AMRAL Research Lab.

Two documents about discipline rather than arithmetic.

`26_Novelty_Search_Log` runs a literature search, finds nothing, and then boxes
the only sentence that matters:

    NO HIT != NOVELTY PROOF

and lists four things that must still happen before priority is claimed —
MathSciNet/zbMATH/Scholar citation chaining, Fouquet–Wan's citing papers, a
number theorist checking whether it is a corollary of something general, and the
2026 preprints. **None of the four is work this arm can do**, and the honest
report says so rather than scoring the box as passed.

`01_Phase2_Route_Matrix` grades eight routes — STOP, GO as baseline, PRIMARY GO,
supporting, HOLD, niche, separate Phase later — and orders them by
extensibility of the Banwait–Huang family theorem.

THIS ARM'S COVERAGE IS NOT THAT ORDERING, AND SHOULD NOT BE. `01` orders routes
by what is worth extending; a verification arm's order is what has been written
down. The measurement is worth making precisely because the two differ: the
route marked STOP is untouched, PRIMARY GO is where most rounds went — and two
rounds worked routes marked HOLD and separate Phase later, because documents on
those routes existed and were verifiable. That is stated rather than defended.

Usage:  python code/src52_novelty_and_routes.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd"
OUT = LOGS / "src52-novelty-and-routes.json"

NOVELTY_TERMS = ("novelty", "new theorem", "priority claim", "first to prove")
REFUSAL_WORDS = ("not", "never", "untouched", "deferred", "cited", "no round",
                 "cannot", "does not", "separate")

REMAINING_STEPS = (
    "MathSciNet / zbMATH / Google Scholar citation chaining",
    "search Fouquet–Wan's citing papers",
    "a number theorist referee checking whether it is a direct corollary of "
    "some general theorem",
    "check the 2026 preprints",
)

ROUTES = (
    ("Higher 2-power descent", "STOP as mainline", ()),
    ("Non-semistable + existing odd-p patchwork", "GO as baseline",
     ("12_Hybrid_Odd_Prime_Router", "17_696e1_All_Prime_Router",
      "27_Revised_Derived_Theorem_Candidate", "18_Provisional_Derived_Theorem")),
    ("Fouquet–Wan arbitrary reduction", "PRIMARY GO",
     ("02_Fouquet_Wan_Hypothesis_Compiler", "03_FW_H2_Jordan_Holder_Lemma",
      "08_FW_Weight2_Exact_Translation", "09_FW_H3_Exact_Compiler",
      "10_FW_H2_and_Ordinary_Obstruction", "11_Derived_Supersingular_FW_Bridge",
      "04_Finite_Exceptional_Prime_Problem",
      "23_FW_Supersingular_Source_Audit")),
    ("BCS ordinary non-semistable", "supporting route",
     ("22_Odd_Prime_Source_Audit",)),
    ("Full rational 2-torsion", "HOLD", ()),
    ("Analytic rank 1", "HOLD", ()),
    ("Prime conductor", "niche", ()),
    ("High rank 2+", "separate Phase later", ()),
)

# rounds of this line that worked a route the matrix does not prioritise, and why
OFF_PRIORITY = (
    ("RUN-026", "Analytic rank 1", "HOLD",
     "the rank-1 BSD identity at 37a1 and 43a1, closed with every term computed "
     "in this tree. It verified an identity, not an extension of the family "
     "theorem"),
    ("RUN-023", "High rank 2+", "separate Phase later",
     "the rank-2 identity at 389.a1, closing at ratio 1.0. Same shape: a "
     "document existed and was checkable"),
)


# Sentences that carry a novelty term without asserting novelty, classified
# once by hand. A crude refusal-word test called all five of these assertions —
# RUN-027 named that failure mode, a scan built on the shapes the author
# remembers rather than the shapes the corpus contains — so they are pinned
# here with their reason, and any NEW unclassified mention turns the check red.
CLASSIFIED_MENTIONS = (
    ("RUN-019", "freezes any route that for three consecutive rounds",
     "quoting Phase 0's own freeze rule"),
    ("RUN-030", "Independent expert referee reproduces all source mappings",
     "quoting `28_Submission_Gate`'s checklist, whose boxes this arm does not "
     "tick"),
    ("RUN-047", "defers one to a novelty audit",
     "describing what `27` defers, not claiming the result is novel"),
    ("RUN-047", "The claim label is consistent across all three documents",
     "reporting the labels the documents carry"),
    ("RUN-047", "as what a novelty/citation referee could unlock",
     "quoting `27`'s own next rung"),
    # and five in the report of THIS round, which audits the novelty rule and
    # therefore cannot avoid naming it. A round that exempted its own report
    # would have written itself a loophole, so they are pinned like the rest.
    ("RUN-050", "26_Novelty_Search_Log`](../../../amral",
     "this round's own subject line"),
    ("RUN-050", "is the finding, and it stands",
     "reporting that `26`'s box holds, which is a refusal to claim novelty"),
    ("RUN-050", "a first, cruder version",
     "describing this gate's own earlier scan"),
    ("RUN-050", "NO HIT}",
     "the box itself, displayed; pinned on a backslash-free fragment"),
    ("RUN-050", "sentences carrying a novelty term",
     "the scan's own tally row"),
)


def novelty_rule() -> dict:
    """`26`'s box, its four remaining steps, and what this arm can do with them."""
    p = DOCS / "phase2" / "files" / "26_Novelty_Search_Log.md"
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    return {"document_found": bool(text),
            "the_box": "NO HIT != NOVELTY PROOF",
            "box_present": "NOVELTY PROOF" in text,
            "searches_were_arXiv": "arXiv" in text,
            "remaining_steps": list(REMAINING_STEPS),
            "steps_this_arm_can_do": [],
            "why_none": ("all four are literature work against external "
                         "databases. This tree has no external access, and the "
                         "standing rule on unpublished AMRAL research forbids "
                         "sending it to a third-party provider while it lives "
                         "only on GitHub"),
            "so": ("`26`'s own box is the finding: a search that returned "
                   "nothing is not a proof of novelty, and this arm can neither "
                   "extend the search nor score the box as passed")}


def no_round_claims_novelty() -> dict:
    """Every mention of novelty in this line's reports must be a refusal."""
    rows = []
    for f in sorted(REPORTS.glob("RUN-*.md")):
        text = f.read_text(encoding="utf-8")
        for sent in re.split(r"(?<=[.!?])\s+|\n\n", text):
            low = sent.lower()
            if any(t in low for t in NOVELTY_TERMS):
                refused = any(w in low for w in REFUSAL_WORDS)
                flat = " ".join(sent.split())
                cls = next((c for c in CLASSIFIED_MENTIONS
                            if c[0] in f.name and c[1] in flat), None)
                rows.append({"report": f.name, "refused": refused,
                             "classified_as_descriptive": bool(cls),
                             "why_not_a_claim": cls[2] if cls else None,
                             "sentence": flat[:150]})
    unaccounted = [r for r in rows
                   if not r["refused"] and not r["classified_as_descriptive"]]
    return {"reports_scanned": len(list(REPORTS.glob("RUN-*.md"))),
            "mentions": len(rows),
            "refusals": sum(r["refused"] for r in rows),
            "classified_descriptive": sum(r["classified_as_descriptive"]
                                          for r in rows),
            "unaccounted": unaccounted,
            "no_unaccounted_mention": not unaccounted,
            "rows": rows[:12],
            "why_scanned_this_way": ("a mention is not a claim, and a crude "
                                     "refusal-word test called five quotations "
                                     "assertions. Every sentence carrying a "
                                     "novelty term must be a refusal or one of "
                                     "the classified quotations; a new one is "
                                     "unaccounted and turns the check red")}


def subjects() -> set[str]:
    """Which corpus documents are the subject of a round, from the gate logs."""
    out = set()
    for f in sorted(LOGS.glob("src*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:                                # pragma: no cover
            continue
        src = d.get("source")
        if isinstance(src, str):
            for piece in src.split(","):
                name = piece.strip().split(":")[0].strip()
                if name:
                    out.add(name.replace(".md", ""))
    return out


def route_matrix() -> dict:
    """`01`'s eight routes, against which of their documents this line ran."""
    subs = subjects()
    rows = []
    for name, verdict, docs in ROUTES:
        hit = sorted(d for d in docs if any(d in s for s in subs))
        rows.append({"route": name, "verdict": verdict,
                     "documents_mapped": list(docs),
                     "documents_this_line_made_a_subject": hit,
                     "count": len(hit), "of": len(docs)})
    primary = next(r for r in rows if r["verdict"] == "PRIMARY GO")
    stop = next(r for r in rows if r["verdict"].startswith("STOP"))
    return {"rows": rows,
            "primary_go_coverage": f"{primary['count']} of {primary['of']}",
            "primary_go_is_the_most_covered":
                primary["count"] == max(r["count"] for r in rows),
            "stop_route_untouched": stop["count"] == 0,
            "the_mapping_is_a_judgement": ("documents are assigned to routes by "
                                           "reading, not by a field in the "
                                           "corpus. What is computed is the "
                                           "count given that assignment"),
            "documents_subject_total": len(subs)}


def off_priority_rounds() -> dict:
    """Rounds of this line on routes `01` does not prioritise, named not excused."""
    return {"rows": [{"round": a, "route": b, "verdict": c, "why": d}
                     for a, b, c, d in OFF_PRIORITY],
            "count": len(OFF_PRIORITY),
            "reading": ("`01` orders routes by extensibility of the family "
                        "theorem. A verification arm orders by what has been "
                        "written down and is checkable. The two orderings are "
                        "different and should be — but the difference is worth "
                        "measuring rather than assuming, and these two rounds "
                        "are where it shows")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    nov = novelty_rule()
    claims = no_round_claims_novelty()
    routes = route_matrix()
    off = off_priority_rounds()

    ok = (nov["document_found"] and nov["box_present"]
          and not nov["steps_this_arm_can_do"]
          and claims["no_unaccounted_mention"]
          and claims["classified_descriptive"] == len(CLASSIFIED_MENTIONS)
          and routes["stop_route_untouched"]
          and routes["primary_go_is_the_most_covered"]
          and off["count"] == 2)

    log = {
        "gate": "src52 — the novelty rule and the route matrix",
        "source": "26_Novelty_Search_Log, 01_Phase2_Route_Matrix",
        "novelty_rule": nov,
        "no_round_claims_novelty": claims,
        "route_matrix": routes,
        "off_priority_rounds": off,
        "headline": (f"`26`'s box — NO HIT is not a novelty proof — stands, and "
                     f"none of the four steps it still requires is work this arm "
                     f"can do: all four are external literature searches, and "
                     f"the standing rule forbids routing unpublished work to a "
                     f"third party. {claims['mentions']} sentences across "
                     f"{claims['reports_scanned']} reports carry a novelty term "
                     f"and every one is a refusal or a classified quotation. "
                     f"`01`'s PRIMARY GO route is "
                     f"the most covered at {routes['primary_go_coverage']} and "
                     f"its STOP route is untouched — but two rounds worked "
                     f"routes marked HOLD and separate Phase later, which is "
                     f"named rather than defended"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  26's box: {nov['the_box']}   present in the document: "
          f"{nov['box_present']}")
    print(f"    four steps still required, of which this arm can do "
          f"{len(nov['steps_this_arm_can_do'])}:")
    for s in nov["remaining_steps"]:
        print(f"      · {s}")
    print(f"    {nov['why_none'][:96]}…")
    print()
    print(f"  novelty terms across {claims['reports_scanned']} reports: "
          f"{claims['mentions']} sentences — {claims['refusals']} refusals, "
          f"{claims['classified_descriptive']} classified quotations, "
          f"{len(claims['unaccounted'])} unaccounted")
    for r in claims["rows"][:4]:
        print(f"    {r['report'][:28]:28s} {r['sentence'][:74]}")
    print()
    print("  01's route matrix, against what this line ran")
    print(f"    {'route':<44} {'verdict':<22} covered")
    for r in routes["rows"]:
        print(f"    {r['route'][:44]:<44} {r['verdict']:<22} "
              f"{r['count']}/{r['of']}")
    print(f"    PRIMARY GO most covered: {routes['primary_go_is_the_most_covered']}"
          f"   STOP untouched: {routes['stop_route_untouched']}")
    print()
    print("  rounds on routes the matrix does not prioritise")
    for r in off["rows"]:
        print(f"    {r['round']}  {r['route']:<22} ({r['verdict']})")
        print(f"           {r['why'][:88]}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
