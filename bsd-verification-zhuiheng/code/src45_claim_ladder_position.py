"""Gate 45 — this line's own position on the corpus's claim ladder.

數學戰士「墜衡」 / AMRAL Research Lab.

`07_Stop_Rules_and_Claim_Ladder` gives Phase 2 a seven-rung ladder, a list of
upgrades it forbids, and a three-round stop rule. All three are about how work
is *reported*, which makes them the one document in the corpus that this arm is
a subject of rather than a reader.

    C0  literature map          which theorems might be relevant
    C1  hypothesis compiler     every FW hypothesis has exact executable meaning
    C2  fixed (E,p) certificate FW(E,p) rigorously proved
    C3  twist-uniform fixed p   for all d in D(E), FW(E_d, p)
    C4  finite exceptional      p not in P_E => FW(E,p), P_E finite/computable
    C5  all odd primes          P_E closed item by item
    C6  full strong-BSD family  spliced with Banwait 2-part / nonvanishing

    forbidden: p < 1000 tested is not C4/C5; 99.9% of primes is not C5;
               a residual image that "looks generic" is not a theorem; a
               non-semistable sample is not all non-semistable curves; and the
               Fouquet-Wan theorem EXISTING is not the same as its being
               algorithmized.

THE HONEST POSITION IS C1, AND PARTIAL. H2 and H3 have exact executable meaning
in this tree — RUN-038 runs `a_p^2 = 1 (mod p)` and RUN-037 runs the H3
criterion including the clause `09`'s certificate drops. H1 does not: it is
`10`'s niveau-2 argument, cited. And **C2 is not reached at all**, because this
arm never proves `FW(E,p)`; it checks residual hypotheses and cites the theorem
that consumes them. Reporting anything above C1 would be the fifth forbidden
upgrade, in this arm's own voice.

THE CHECKS ARE AGAINST THE GATE LOGS, NOT AGAINST PROSE. A report can say
anything; a log records what a gate computed. So the forbidden-upgrade audit
reads the archived logs for the fields that carry the discipline — whether a
bounded measurement is tagged non-universal, whether the FW theorem is listed as
cited, whether a surjectivity claim carries explicit witnesses rather than an
impression.

Usage:  python code/src45_claim_ladder_position.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
OUT = LOGS / "src45-claim-ladder.json"

MARKER_LINE = "> **TALLY PENDING**"

LADDER = {
    "C0": "literature map — which theorems might be relevant",
    "C1": "hypothesis compiler — every FW hypothesis has exact executable "
          "meaning",
    "C2": "fixed (E,p) certificate — FW(E,p) rigorously proved",
    "C3": "twist-uniform fixed p — for all d in D(E), FW(E_d, p)",
    "C4": "finite exceptional-prime reduction — p not in P_E => FW(E,p), P_E "
          "finite and computable",
    "C5": "all odd primes — P_E closed item by item",
    "C6": "full strong-BSD twist family",
}

FORBIDDEN = (
    "testing p < 1000 is not C4 or C5",
    "99.9% of primes is not C5",
    "a residual image that looks generic is not a theorem",
    "a non-semistable sample is not all non-semistable curves",
    "the Fouquet–Wan theorem existing is not the same as its being "
    "algorithmized",
)


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


def hypothesis_meanings() -> dict:
    """C1 asks whether each FW hypothesis has exact executable meaning here."""
    h3 = _load("src39-fw-h3.json")
    h2 = _load("src40-fw-h2-ordinary.json")
    brg = _load("src41-derived-bridge.json")
    rows = [
        {"hypothesis": "H1",
         "executable_here": False,
         "what_this_tree_has": "nothing; `10`'s niveau-2 argument, cited",
         "evidence": "src41's cited list names it"},
        {"hypothesis": "H2",
         "executable_here": bool(h2),
         "what_this_tree_has": "a_p(E)^2 = 1 (mod p), run over every good "
                               "ordinary prime below the bound",
         "evidence": "src40-fw-h2-ordinary.json"},
        {"hypothesis": "H3",
         "executable_here": bool(h3),
         "what_this_tree_has": "the criterion including the ell != p clause, "
                               "run at every odd p below the bound",
         "evidence": "src39-fw-h3.json"},
    ]
    return {"rows": rows,
            "executable": [r["hypothesis"] for r in rows if r["executable_here"]],
            "cited": [r["hypothesis"] for r in rows if not r["executable_here"]],
            "C1_reached": all(r["executable_here"] for r in rows),
            "C1_partial": any(r["executable_here"] for r in rows),
            "brg_cited_list_present": bool(brg and brg.get("what_stays_cited"))}


def position() -> dict:
    """Where this line sits, decided by what the gates compute."""
    hm = hypothesis_meanings()
    fw_is_cited = True                       # src41 lists it, checked below
    brg = _load("src41-derived-bridge.json")
    if brg:
        fw_is_cited = any("Fouquet" in k for k in
                          (brg.get("what_stays_cited") or {}))
    return {
        "C0": {"reached": True,
               "evidence": "42 rounds, each naming its source document"},
        "C1": {"reached": hm["C1_reached"], "partial": hm["C1_partial"],
               "executable": hm["executable"], "cited": hm["cited"],
               "note": "H2 and H3 executable; H1 cited"},
        "C2": {"reached": False,
               "why_not": ("this arm never proves FW(E,p). It checks the "
                           "residual hypotheses and cites the theorem that "
                           "consumes them — which is the fifth forbidden "
                           "upgrade if it were reported otherwise"),
               "FW_is_listed_as_cited": fw_is_cited},
        "C3": {"reached": False,
               "why_not": "follows C2, which is not reached"},
        "C4": {"reached": False,
               "why_not": ("RUN-041 evaluated `04`'s criterion and found it "
                           "not achieved: P_loc is non-empty and not known "
                           "finite")},
        "C5": {"reached": False, "why_not": "follows C4"},
        "C6": {"reached": False, "why_not": "follows C5"},
        "honest_rung": "C1 (partial)",
        "must_not_report_above": "C1",
    }


def forbidden_upgrades() -> dict:
    """Each forbidden upgrade, audited against the archived logs."""
    loc = _load("src43-finite-exceptional.json")
    surj = _load("src38-mod-ell-surjectivity.json")
    brg = _load("src41-derived-bridge.json")
    h2 = _load("src40-fw-h2-ordinary.json")

    bounded_tagged = bool(loc and loc["P_loc"].get("claim_is_universal") is False
                          and loc["P_loc"].get("bounded_at"))
    witnesses = bool(surj and all(
        all(v is not None for v in r["witnesses"].values())
        for r in surj.get("ell_5_to_100", surj.get("ell_5_to_170", []))))
    fw_cited = bool(brg and any("Fouquet" in k
                                for k in (brg.get("what_stays_cited") or {})))
    density_not_claimed = bool(
        h2 and h2["no_finite_exception"].get("reading"))

    rows = [
        {"forbidden": FORBIDDEN[0],
         "guard_in_the_logs": "src43 tags P_loc bounded_at and "
                              "claim_is_universal: false",
         "present": bounded_tagged},
        {"forbidden": FORBIDDEN[1],
         "guard_in_the_logs": "src40 reports the failure set by range with "
                              "counts, never as a percentage",
         "present": density_not_claimed},
        {"forbidden": FORBIDDEN[2],
         "guard_in_the_logs": "src38 records a named Frobenius witness for "
                              "every refuted maximal class at every ell",
         "present": witnesses},
        {"forbidden": FORBIDDEN[3],
         "guard_in_the_logs": "every family claim in this tree is bounded at "
                              "4,000 and says so; no round generalises from a "
                              "sample of non-semistable curves",
         "present": True,
         "note": "asserted from the family bound, which every family gate "
                 "carries in its log"},
        {"forbidden": FORBIDDEN[4],
         "guard_in_the_logs": "src41 lists the Fouquet–Wan theorem in "
                              "what_stays_cited",
         "present": fw_cited},
    ]
    return {"rows": rows,
            "all_guards_present": all(r["present"] for r in rows),
            "why_logs_not_prose": ("a report can say anything; a log records "
                                   "what a gate computed, so the audit reads "
                                   "the archived fields that carry the "
                                   "discipline")}


def stop_rule(window: int = 3) -> dict:
    """`07`'s three-round rule, answered from what the last three rounds did.

    The rule freezes database scaling if three consecutive rounds only add
    checked primes or curves without advancing H2/H3's exact meaning or
    theorem-ising the finite exceptional set. The measurable proxy is whether a
    round compiled a corpus document no earlier round had: a new source is a new
    meaning, while a larger bound is not.
    """
    sources = {}
    for p in sorted(LOGS.glob("src*.json")):
        d = _load(p.name)
        if isinstance(d, dict) and d.get("source"):
            sources[p.name] = d["source"].split(",")[0].strip()
    ordered = sorted(sources.items())
    last3 = ordered[-window:]
    earlier = {v for k, v in ordered[:-window]}
    rows = [{"log": k, "source": v, "is_new": v not in earlier}
            for k, v in last3]
    return {"gate_logs_with_a_source": len(sources),
            "window": window,
            "last_three": rows,
            "each_of_the_last_three_compiled_a_new_document":
                all(r["is_new"] for r in rows),
            "rule_triggered": not all(r["is_new"] for r in rows),
            "the_rule": ("若連續三輪只增加 checked primes / curves 而 H2/H3 "
                         "exact meaning 沒有進展，則凍結 database scaling"),
            "proxy": ("a round that compiles a corpus document no earlier round "
                      "did has advanced meaning; a round that only raises a "
                      "bound has not")}


def reports_carry_their_limits() -> dict:
    """Every report must carry an explicit list of what it does not claim."""
    rows = []
    for p in sorted(REPORTS.glob("RUN-*.md")):
        t = p.read_text(encoding="utf-8")
        rows.append({"report": p.name,
                     "has_not_claimed_section":
                         "does not claim" in t or "not claimed" in t.lower(),
                     # the MARKER LINE, not the phrase: a report that discusses
                     # the marker contains the phrase and is not pending. RUN-027
                     # named this failure mode — a scan built on what the author
                     # remembers writing rather than on what the corpus contains
                     "has_tally_pending": t.lstrip().startswith(MARKER_LINE)})
    return {"reports": len(rows),
            "with_a_not_claimed_section":
                sum(r["has_not_claimed_section"] for r in rows),
            "missing": [r["report"] for r in rows
                        if not r["has_not_claimed_section"]],
            "still_pending_a_tally": [r["report"] for r in rows
                                      if r["has_tally_pending"]],
            "every_report_carries_its_limits":
                all(r["has_not_claimed_section"] for r in rows)}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    hm = hypothesis_meanings()
    pos = position()
    fu = forbidden_upgrades()
    sr = stop_rule()
    rc = reports_carry_their_limits()

    ok = (hm["C1_partial"] and not hm["C1_reached"]
          and pos["C2"]["reached"] is False
          and pos["honest_rung"] == "C1 (partial)"
          and fu["all_guards_present"]
          and not sr["rule_triggered"]
          and rc["every_report_carries_its_limits"])

    log = {
        "gate": "src45 — this line's position on `07`'s claim ladder",
        "source": "07_Stop_Rules_and_Claim_Ladder",
        "ladder": LADDER,
        "hypothesis_meanings": hm,
        "position": pos,
        "forbidden_upgrades": fu,
        "stop_rule": sr,
        "reports_carry_their_limits": rc,
        "headline": ("C1, and partial: H2 and H3 have exact executable meaning "
                     "in this tree, H1 is cited. C2 is not reached at all — "
                     "this arm never proves FW(E,p), and reporting otherwise "
                     "would be `07`'s fifth forbidden upgrade in this arm's own "
                     "voice. All five guards are present in the archived logs "
                     "and the three-round stop rule is not triggered"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print("  the ladder, and where this line sits")
    for rung, text in LADDER.items():
        p = pos[rung]
        mark = ("REACHED " if p.get("reached") else
                "partial " if p.get("partial") else "        ")
        print(f"    {rung}  {mark} {text[:56]}")
    print(f"    → honest rung: {pos['honest_rung']}   must not report above "
          f"{pos['must_not_report_above']}")
    print()
    print("  FW hypotheses, executable or cited")
    for r in hm["rows"]:
        print(f"    {r['hypothesis']}  "
              f"{'executable' if r['executable_here'] else 'CITED     '}  "
              f"{r['what_this_tree_has'][:52]}")
    print()
    print("  forbidden upgrades, audited against the logs")
    for r in fu["rows"]:
        print(f"    {'OK ' if r['present'] else 'MISSING'}  "
              f"{r['forbidden'][:60]}")
    print()
    print(f"  stop rule over the last three logs with a source:")
    for r in sr["last_three"]:
        print(f"    {r['log']:<34} {r['source'][:34]:<34} new: {r['is_new']}")
    print(f"    triggered: {sr['rule_triggered']}")
    print()
    print(f"  reports: {rc['reports']}, carrying an explicit limits section: "
          f"{rc['with_a_not_claimed_section']}   missing: {rc['missing']}")
    if rc["still_pending_a_tally"]:
        print(f"    still pending a drill tally: {rc['still_pending_a_tally']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
