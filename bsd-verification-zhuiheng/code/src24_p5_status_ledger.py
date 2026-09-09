"""Gate 24 — the P5 chain's status ledger, reconciled across all ten documents.

數學戰士「墜衡」 / AMRAL Research Lab.

P5 is not one argument, it is a chain of ten documents that each declare gate
statuses in a fenced block: `P5-IMC11 CLOSED`, `P5-RAT BLOCKED BY P5-DERPER`,
and so on. A reader who wants to build on the chain has to know three things
that no single document answers:

  1. does any gate carry **different statuses in different documents**, and if
     so is that a version-ordered upgrade or an unexplained conflict;
  2. is the blocking graph **acyclic**, and what are its roots;
  3. for each `CLOSED`, is it closed by an **exact finite computation** that can
     be reproduced, or by a **cited external theorem** — the ledgers write both
     as the same word.

That third question is the one this arm exists to answer, and the answer is not
uniform. Two of the gates the chain marks closed-by-citation are closed **here**
by this tree's own recomputation, on independent grounds:

  * `P5-BOC-NZ11` — the Bockstein non-vanishing. `v1.3` §3 derives it from
    `det(M_loc) = 2`, and RUN-011 recomputed that matrix from the group law up.
    `v0.5` lists the gate as PENDING FINITE SAGEMATH REPLAY and `v0.6` as
    CLOSED_BY_PUBLISHED_COMPUTATION; neither is what this tree relies on.
  * `P5-RESIDUAL-IRR11` — irreducibility of the mod-11 representation. `v0.5`
    closes it with "maximal 11-adic image", which RUN-020 recorded as cited and
    unverified. It follows instead from `j(E) ∉ {−11·131³, −2¹⁵, −11²}`, the
    three non-cuspidal rational points of `X₀(11)` — and `j(389.a1)` is not even
    an integer. Semistability, recomputed in RUN-020, gives it a second time
    through Mazur's isogeny theorem.

EXTRACTION IS MECHANICAL AND QUOTED. The gate parses the fenced blocks verbatim
and prints what it parsed. A ledger audit that paraphrased its sources would be
worth nothing; every row below can be diffed against the document by eye.

Usage:  python code/src24_p5_status_ledger.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src23_p5_local_units as p5u                        # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT.parent.parent / "amral" / "public" / "bsd" / "p5" / "files"
OUT = ROOT / "data" / "gate-logs" / "src24-p5-status-ledger.json"

FENCE = re.compile(r"```(?:text)?\n(.*?)```", re.S)
# The underscore is a word character, so `\bCLOSED\b` does NOT match inside
# `CLOSED_BY_PUBLISHED_COMPUTATION` — and v0.6 writes every status that way. The
# first version of this pattern had that word boundary and silently dropped nine
# of v0.6's ten rows, including the one gate this ledger exists to reconcile.
# The trailing `[A-Z_]*` is the fix, and the drill pins the row count so a
# future narrowing shows up as a red check rather than as a shorter table.
STATUS_WORD = re.compile(
    r"\b(CLOSED|OPEN|BLOCKED|PENDING|AVAILABLE|PARTIALLY|EQUIVALENT|REDUCED|"
    r"NOT CLAIMED|CIRCULAR|EXTERNAL|THEOREM TECHNOLOGY|ARITHMETIC TARGET)[A-Z_]*")
# a ledger row is a name, two-or-more spaces, then a status phrase
ROW = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9\-/_\[\]^ .]*?)\s{2,}(\S.*?)\s*$")

# The three non-cuspidal rational points of X_0(11) (the curve 11a1, whose
# Mordell-Weil group is Z/5: two cusps and three non-cuspidal points).
X0_11_NONCUSPIDAL_J = (-11 * 131 ** 3, -2 ** 15, -11 ** 2)


def extract_rows() -> dict:
    """Every fenced ledger row in the P5 corpus, verbatim."""
    per_doc = {}
    for f in sorted(CORPUS.glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        rows = []
        for block in FENCE.findall(text):
            if not STATUS_WORD.search(block):
                continue
            for line in block.splitlines():
                if not line.strip():
                    continue
                m = ROW.match(line)
                if m and STATUS_WORD.search(m.group(2)):
                    rows.append({"gate": m.group(1).strip(),
                                 "status": m.group(2).strip(),
                                 "line": line.rstrip()})
        if rows:
            per_doc[f.name] = rows
    return per_doc


def _verdict(status: str) -> str:
    """CLOSED / NOT-CLOSED / OTHER — the only distinction a reconciliation needs.

    `OPEN` and `BLOCKED BY X` are the same verdict stated at different
    resolution, so treating their difference as a conflict would report noise.
    `CLOSED` against either is a real one.
    """
    s = status.upper()
    if s.startswith("CLOSED"):
        return "CLOSED"
    if s.startswith(("OPEN", "BLOCKED", "PENDING")) or "BLOCKED BY" in s:
        return "NOT-CLOSED"
    return "OTHER"


def _canon(target: str, names: set) -> str:
    """`BLOCKED BY BOC-NZ11 + GPR11` names gates their own rows call
    `P5-BOC-NZ11` and `P5-GPR11`. The prefix is restored when, and only when,
    exactly one declared gate name matches; otherwise the string is left as
    written rather than guessed at."""
    if target in names:
        return target
    hits = [n for n in names if n == "P5-" + target or n.endswith("-" + target)]
    return hits[0] if len(hits) == 1 else target


def _doc_version(name: str):
    """The version a filename declares, for ordering. None when it declares none."""
    m = re.search(r"_v(\d+)\.(\d+)", name)
    return (int(m.group(1)), int(m.group(2))) if m else None


def reconcile(per_doc: dict) -> dict:
    """Gates that carry more than one status, split by whether order explains it."""
    by_gate: dict[str, list] = {}
    for doc, rows in per_doc.items():
        for r in rows:
            by_gate.setdefault(r["gate"], []).append({"doc": doc, **r})
    multi = {g: v for g, v in by_gate.items()
             if len({x["status"] for x in v}) > 1}
    ordered, unexplained = [], []
    for g, v in multi.items():
        versions = [_doc_version(x["doc"]) for x in v]
        entry = {"gate": g,
                 "readings": [{"doc": x["doc"], "version": _doc_version(x["doc"]),
                               "status": x["status"]} for x in v]}
        kinds = {_verdict(x["status"]) for x in v}
        entry["verdicts"] = sorted(kinds)
        if len(kinds) == 1:
            entry["explained_by"] = ("same verdict at different resolution — "
                                     f"every reading is {sorted(kinds)[0]}")
            entry["explained_by_version_order"] = True
            entry["latest"] = v[-1]["status"]
            ordered.append(entry)
        elif all(w is not None for w in versions) and len(set(versions)) == len(versions):
            entry["explained_by"] = "version order, and the verdict moved"
            entry["explained_by_version_order"] = True
            entry["latest"] = max(v, key=lambda x: _doc_version(x["doc"]))["status"]
            ordered.append(entry)
        else:
            entry["explained_by_version_order"] = False
            unexplained.append(entry)
    return {
        "distinct_gate_names": len(by_gate),
        "gates_with_more_than_one_status": len(multi),
        "explained_by_version_order": ordered,
        "not_explained_by_version_order": unexplained,
        "all_conflicts_explained": not unexplained,
    }


def blocking_graph(per_doc: dict) -> dict:
    """`BLOCKED BY X` and `EQUIVALENT_TO X` edges, and whether they cycle."""
    names = {r["gate"] for rows in per_doc.values() for r in rows}
    edges = []
    for doc, rows in per_doc.items():
        for r in rows:
            for m in re.finditer(r"(?:BLOCKED BY|EQUIVALENT[_ ]TO)\s+([A-Za-z0-9\-_+ ]+)",
                                 r["status"]):
                for target in re.split(r"\s*\+\s*", m.group(1).strip()):
                    t = target.strip()
                    if t:
                        edges.append({"from": r["gate"], "to": _canon(t, names),
                                      "written_as": t, "doc": doc})
    adj: dict[str, set] = {}
    for e in edges:
        adj.setdefault(e["from"], set()).add(e["to"])
    # depth-first cycle detection over the declared edges
    colour: dict[str, int] = {}
    cycles = []

    def walk(n, path):
        colour[n] = 1
        for m in sorted(adj.get(n, ())):
            if colour.get(m) == 1:
                cycles.append(path + [n, m])
            elif colour.get(m) is None:
                walk(m, path + [n])
        colour[n] = 2

    for n in sorted(adj):
        if colour.get(n) is None:
            walk(n, [])
    roots = sorted({e["to"] for e in edges} - set(adj))
    # An edge whose target could not be resolved to exactly one declared gate is
    # a defect in the ledger, not in the parser, and it is reported as one.
    ambiguous = []
    for e in edges:
        if e["to"] == e["written_as"] and e["to"] not in names:
            cands = sorted(n for n in names
                           if n == "P5-" + e["written_as"]
                           or n.endswith("-" + e["written_as"])
                           or n.endswith(e["written_as"]))
            ambiguous.append({"edge": f"{e['from']} -> {e['written_as']}",
                              "doc": e["doc"], "candidates": cands})
    return {"edges": edges, "is_acyclic": not cycles, "cycles": cycles,
            "roots_of_the_blocking_chain": roots,
            "edges_whose_target_is_ambiguous": ambiguous,
            "reading": ("an un-prefixed target that matches more than one "
                        "declared gate name is left as written rather than "
                        "guessed at. Which gate is meant changes what theorem "
                        "an attack has to go and find")}


def gates_this_arm_can_close() -> dict:
    """Which ledger gates rest on evidence this tree produced, not on a citation.

    The ledgers write "closed by an exact finite computation" and "closed by a
    cited theorem" with the same word. Separated here, and where this arm has
    its own computation it is named with the round that produced it.
    """
    b2, b4, b6, b8, disc = p5u.b_invariants(p5u.AINVS)
    c4, _c6 = p5u.c_invariants(p5u.AINVS)
    j = Fraction(c4 ** 3, disc)
    n11 = p5u.point_count(p5u.AINVS, 11)
    a11 = 11 + 1 - n11
    bad = [p for p in (2, 3, 5, 7, 11, 13, 389) if disc % p == 0]
    red = {p: tate.reduction_data(p5u.AINVS, p, want_c=True) for p in bad}
    semistable = all(d["f"] == 1 for d in red.values())

    irr11 = {
        "gate": "P5-RESIDUAL-IRR11",
        "ledger_says": "CLOSED (maximal 11-adic image) — v0.5",
        "why_that_is_weak": ("maximal image for EVERY l is a much stronger claim "
                             "than irreducibility at 11, and RUN-020 recorded it "
                             "as cited and unverified"),
        "route_1_X0_11": {
            "j": str(j),
            "j_is_an_integer": j.denominator == 1,
            "three_non_cuspidal_j_on_X0(11)": list(X0_11_NONCUSPIDAL_J),
            "j_is_one_of_them": j in {Fraction(v) for v in X0_11_NONCUSPIDAL_J},
            "conclusion": ("X_0(11) is the curve 11a1 with Mordell-Weil group "
                           "Z/5 — two cusps and three non-cuspidal rational "
                           "points. A rational 11-isogeny would put j among "
                           "those three. j(389.a1) is not even an integer"),
        },
        "route_2_semistability_and_Mazur": {
            "bad_primes": bad,
            "reduction": {str(p): d["kodaira"] for p, d in red.items()},
            "semistable": semistable,
            "conclusion": ("Mazur's isogeny theorem: a semistable E/Q admits a "
                           "rational p-isogeny only for p in {2, 3, 5, 7}. The "
                           "semistability is recomputed here; the theorem is "
                           "cited"),
        },
        "closed_by_this_arm": (j.denominator != 1
                               or j not in {Fraction(v) for v in X0_11_NONCUSPIDAL_J}),
        "independent_of_the_ledgers_justification": True,
    }

    boc = {
        "gate": "P5-BOC-NZ11",
        "ledger_says": {"v0.5": "PENDING FINITE SAGEMATH REPLAY",
                        "v0.6": "CLOSED_BY_PUBLISHED_COMPUTATION"},
        "what_it_needs": ("det(B_N) != 0. v1.3 §3 gives "
                          "det(B_N)(P^Q) = det(M_loc)(e_397 ^ e_991) (x) "
                          "X_397 X_991, so it is exactly det(M_loc) != 0"),
        "this_arm": ("RUN-011 recomputed the localization matrix [[1,2],[1,4]] "
                     "from the group law up and got determinant 2 mod 11 — "
                     "src12-p5-localization.json"),
        "closed_by_this_arm": True,
        "independent_of_the_ledgers_justification": True,
    }

    good_ord = {
        "gate": "P5-GOOD-ORD11",
        "ledger_says": "CLOSED (curve data)",
        "this_arm": f"RUN-020: Delta = {disc}, 11 does not divide it; a_11 = {a11}, "
                    f"11 does not divide that either",
        "closed_by_this_arm": disc % 11 != 0 and a11 % 11 != 0,
        "independent_of_the_ledgers_justification": False,
    }

    cited = [
        {"gate": "P4-SHA11", "ledger_says": "CLOSED (imported exact project certificate)",
         "this_arm": "not checked — the Kurihara witness at n = 397·991 plus the "
                     "Chan-Ho Kim Selmer structure theorem"},
        {"gate": "P5-IMC11", "ledger_says": "CLOSED (Burungale--Castella--Skinner)",
         "this_arm": "not checked — an external theorem"},
        {"gate": "P5-BCS-IM-CONDITION", "ledger_says": "CLOSED (explicit unipotent certificate)",
         "this_arm": "not checked — the certificate is not reproduced here"},
        {"gate": "P5-MAZUR-TATE-WEAK11", "ledger_says": "CLOSED AS EXTERNAL THEOREM INPUT",
         "this_arm": "not checked — the ledger already labels it external"},
    ]
    return {"closed_here_on_independent_grounds": [irr11, boc],
            "closed_here_but_agreeing_with_the_ledger": [good_ord],
            "cited_and_not_checked": cited}


def main() -> int:
    per_doc = extract_rows()
    rec = reconcile(per_doc)
    graph = blocking_graph(per_doc)
    arm = gates_this_arm_can_close()
    log = {
        "gate": "src24 — the P5 status ledger, reconciled",
        "documents_with_a_ledger": sorted(per_doc),
        "rows_extracted_verbatim": per_doc,
        "reconciliation": rec,
        "blocking_graph": graph,
        "what_this_arm_can_close_itself": arm,
        "ok": (bool(per_doc) and graph["is_acyclic"]
               and all(g["closed_by_this_arm"]
                       for g in arm["closed_here_on_independent_grounds"])),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    total = sum(len(v) for v in per_doc.values())
    print(f"  ledger rows extracted: {total} across {len(per_doc)} documents")
    print(f"  distinct gate names: {rec['distinct_gate_names']}, "
          f"carrying more than one status: {rec['gates_with_more_than_one_status']}")
    for e in rec["explained_by_version_order"]:
        rs = "  |  ".join(f"{r['doc'].split('_')[-1][:5]} {r['status']}"
                          for r in e["readings"])
        print(f"    [version-ordered] {e['gate']}: {rs}")
    for e in rec["not_explained_by_version_order"]:
        rs = "  |  ".join(f"{r['doc']} {r['status']}" for r in e["readings"])
        print(f"    [UNEXPLAINED]     {e['gate']}: {rs}")
    print(f"  blocking graph: {len(graph['edges'])} edges, acyclic: "
          f"{graph['is_acyclic']}, roots: {graph['roots_of_the_blocking_chain']}")
    for a in graph["edges_whose_target_is_ambiguous"]:
        print(f"    [AMBIGUOUS EDGE] {a['edge']} — candidates {a['candidates']}")
    print()
    print("  gates this arm closes on its OWN evidence:")
    for g in arm["closed_here_on_independent_grounds"]:
        print(f"    {g['gate']}: {g['closed_by_this_arm']}  "
              f"(ledger: {g['ledger_says'] if isinstance(g['ledger_says'], str) else g['ledger_says']})")
    print(f"  cited and not checked: "
          f"{[g['gate'] for g in arm['cited_and_not_checked']]}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
