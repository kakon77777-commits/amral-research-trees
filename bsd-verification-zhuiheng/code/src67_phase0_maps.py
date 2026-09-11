"""Gate 67 — Phase 0's three maps: the theorem closure table, the external route matrix, and the six agent prompts — each held against what this line's 64 rounds actually did.

數學戰士「墜衡」 / AMRAL Research Lab.

Phase 0 wrote three documents that route rather than prove, and none had been a
round's subject:

  02_Known_Theorem_Closure_Map    eight rows, four closed and four open; seven
                                  components of strong BSD; a box: every
                                  component must close independently
  04_External_Route_Matrix        ten routes with verdicts — the twist-family
                                  route 首選, exact computational BSD 綠燈,
                                  Neo's own lattice-rank idea 紅燈
  08_Local_Agent_Handoff_Prompts  six agent briefs, A–F, with per-brief
                                  prohibitions and required output shapes

Each is scored the way RUN-050 scored 01's route matrix and RUN-064 scored
06's handoff: which rounds of this line sit on which row. The round-to-row
mapping is a reading — but every round it cites must exist, every finding it
attributes to a round must be found in that round's report by a signature
phrase, no round may claim a row the map marks OPEN as closed, and the route
the matrix marks 紅燈 must have no round and (RUN-003's log) no document in
the corpus claiming its conditions met.

Usage:  python code/src67_phase0_maps.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase0" / "files"
OUT = LOGS / "src67-phase0-maps.json"

THREE = ("02_Known_Theorem_Closure_Map.md", "04_External_Route_Matrix.md",
         "08_Local_Agent_Handoff_Prompts.md")

RUN_RE = re.compile(r"RUN-\d{3}")
SELF = "src67_phase0_maps"          # the report that names this gate quotes its phrases


def _doc(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _reports() -> dict[str, str]:
    return {f.name[:7]: f.read_text(encoding="utf-8") for f in sorted(REPORTS.glob("RUN-*.md"))}


def _cited(*texts: str) -> list[str]:
    out: list[str] = []
    for t in texts:
        for m in RUN_RE.findall(t):
            if m not in out:
                out.append(m)
    return out


def _missing(reports: dict[str, str], cited: list[str]) -> list[str]:
    return [r for r in cited if r not in reports]


def _signatures_absent(reports: dict[str, str], sigs: list[tuple[str, str]]) -> list[dict]:
    """Each (round, phrase): the phrase must appear verbatim in that round's report."""
    absent = []
    for rn, phrase in sigs:
        if phrase not in reports.get(rn, ""):
            absent.append({"round": rn, "phrase": phrase})
    return absent


# ---------------------------------------------------------------- 02

CLOSURE_ROWS = (
    ("modularity and analytic continuation", "已關閉", []),
    ("weak BSD at analytic rank 0/1", "核心已關閉", ["RUN-014", "RUN-026"]),
    ("p-parts at rank 0/1", "大量新閉包", ["RUN-011", "RUN-020", "RUN-021", "RUN-022"]),
    ("infinite strong-BSD twist families", "已存在",
     ["RUN-009", "RUN-015", "RUN-033", "RUN-037", "RUN-045", "RUN-057"]),
    ("weak BSD at rank >= 2", "開放", ["RUN-023"]),
    ("Sha finite in general", "開放", []),
    ("full leading coefficient", "開放", ["RUN-014", "RUN-017", "RUN-023", "RUN-026", "RUN-030"]),
    ("all E/Q", "開放", []),
)

OPEN_ROW_PHRASES = {
    "weak BSD at rank >= 2": ("rank 2 bsd is proved", "rank-2 bsd closed", "closes weak bsd at rank 2"),
    "Sha finite in general": ("sha is finite for all", "sha finite in general"),
    "full leading coefficient": ("leading coefficient proved for all", "strong bsd proved"),
    "all E/Q": ("bsd for all e/q", "for all elliptic curves over q"),
}

# 02 §5's seven components of a strong-BSD certificate, and where this line
# computed each; the signature phrase is what the cited report must contain
SEVEN = (
    ("actual Sha finite", "never", [("RUN-023", "BSD-inferred")],
     "never computed; RUN-023 records #Ш = 1 as BSD-inferred, i.e. as input"),
    ("actual order of Sha", "never", [], "not computed"),
    ("regulator on a saturated basis", "partial",
     [("RUN-023", "Reg"), ("RUN-026", "height")],
     "regulator computed at RUN-023 (rank 2) and RUN-026 (rank 1, heights here); saturation verified in neither"),
    ("local Tamagawa factors", "computed", [("RUN-016", "c₂"), ("RUN-023", "c_p")],
     "RUN-016 (c₂ closed on the base), RUN-023 (∏c_p = 1 at 389.a1)"),
    ("torsion", "computed", [("RUN-023", "#tors"), ("RUN-031", "Mazur")],
     "RUN-023, RUN-026, RUN-030; RUN-031 (Mazur's twelve degrees closed for 696.e1)"),
    ("period convention", "computed", [("RUN-017", "period"), ("RUN-014", "Ω")],
     "RUN-017 (the real period wrong for three rounds, found by the identity), RUN-014, RUN-023, RUN-030"),
    ("exact leading term", "computed",
     [("RUN-014", "L(E,1)"), ("RUN-023", "L''"), ("RUN-026", "L'(E,1)")],
     "RUN-014 (L(E,1) = Ω), RUN-023 (L''(1)/2!), RUN-026 (L'(1))"),
)


def closure_map_02(reports: dict[str, str]) -> dict:
    t = _doc("02_Known_Theorem_Closure_Map.md")
    rows = [{"row": name, "status_02": status, "rounds_here": rounds, "open": status == "開放"}
            for name, status, rounds in CLOSURE_ROWS]
    cited = _cited(*(" ".join(r) for _, _, r in CLOSURE_ROWS))
    missing = _missing(reports, cited)
    # the part that can fail: no report may claim an OPEN row closed. The
    # report ABOUT this scan quotes the phrases it looks for, so it is not a
    # subject of the scan — the self-match src54's census detector had (RUN-054)
    violations = []
    scanned = []
    for row, phrases in OPEN_ROW_PHRASES.items():
        for rn, txt in reports.items():
            if SELF in txt:
                continue
            if rn not in scanned:
                scanned.append(rn)
            low = txt.lower()
            if any(ph in low for ph in phrases):
                violations.append({"report": rn, "row": row})
    seven = [{"component": c, "state_here": s, "where": w} for c, s, _, w in SEVEN]
    sigs = [x for _, _, ss, _ in SEVEN for x in ss]
    sig_absent = _signatures_absent(reports, sigs)
    return {"document_found": bool(t),
            "table_present": "閉包表" in t,
            "rows": rows,
            "rounds_cited": cited, "rounds_cited_that_do_not_exist": missing,
            "open_rows": [r["row"] for r in rows if r["open"]],
            "reports_scanned_for_a_closure_claim": len(scanned),
            "open_rows_claimed_closed_by_any_report": violations,
            "no_open_row_claimed_closed": not violations,
            "the_box": "完整 BSD 證書是可工程化的，但每個 component 都必須獨立閉合",
            "box_present": "獨立閉合" in t,
            "seven_components_of_strong_BSD": seven,
            "components_computed_here": sum(1 for c in seven if c["state_here"] == "computed"),
            "components_partial_here": sum(1 for c in seven if c["state_here"] == "partial"),
            "components_never_here": [c["component"] for c in seven if c["state_here"] == "never"],
            "component_signatures_checked": len(sigs),
            "component_signatures_absent": sig_absent,
            "reading": ("this line's rounds sit on the closed-or-existing rows (the rank 0/1 "
                        "identities; the P5 p-part chain; the twist family) and, as "
                        "computations only, on two open rows: the rank-2 identity with Sha "
                        "as input, and the leading-coefficient identities at finitely many "
                        "curves. No report says an open row is closed")}


# ---------------------------------------------------------------- 04

ROUTES = (
    ("Gross–Zagier–Kolyvagin", "基線", []),
    ("p-adic zeta / Iwasawa", "綠燈", ["RUN-011", "RUN-020", "RUN-021", "RUN-022"]),
    ("Strong-BSD twist families", "首選",
     ["RUN-009", "RUN-012", "RUN-015", "RUN-018", "RUN-029", "RUN-031", "RUN-033", "RUN-034",
      "RUN-035", "RUN-036", "RUN-037", "RUN-038", "RUN-039", "RUN-040", "RUN-044", "RUN-045",
      "RUN-046", "RUN-047", "RUN-052", "RUN-053", "RUN-055", "RUN-057", "RUN-063"]),
    ("p-converse", "綠燈", []),
    ("generalized Kato / higher GZ", "黃燈", []),
    ("exact computational BSD", "綠燈", ["RUN-014", "RUN-017", "RUN-023", "RUN-026", "RUN-030"]),
    ("Selmer arithmetic statistics", "輔助", []),
    ("numerical BSD atlas", "僅作資料層", ["RUN-004", "RUN-005", "RUN-006", "RUN-007", "RUN-008", "RUN-016"]),
    ("lattice-point rank convergence (格點秩收斂)", "紅燈", []),
    ("Faithful certificate frontier", "控制層",
     ["RUN-002", "RUN-010", "RUN-013", "RUN-024", "RUN-027", "RUN-032", "RUN-043", "RUN-048", "RUN-058"]),
)


def route_matrix_04(reports: dict[str, str]) -> dict:
    t = _doc("04_External_Route_Matrix.md")
    rows = [{"route": a, "verdict_04": b, "rounds_here": c, "count": len(c)} for a, b, c in ROUTES]
    cited = _cited(*(" ".join(c) for _, _, c in ROUTES))
    missing = _missing(reports, cited)
    red = [r for r in rows if r["verdict_04"] == "紅燈"]
    red_worked = [r["route"] for r in red if r["count"]]
    # RUN-003 scanned all 85 documents for the rejected route's conditions being claimed met
    r3 = LOGS / "src02-rejected-route.json"
    r3d = json.loads(r3.read_text(encoding="utf-8")) if r3.exists() else {}
    claimed_met = (r3d.get("counts") or {}).get("GR_conditions_claimed_met_anywhere")
    scanned = (r3d.get("counts") or {}).get("documents_scanned")
    first = max(rows, key=lambda r: r["count"])
    runner_up = sorted(rows, key=lambda r: -r["count"])[1]
    return {"document_found": bool(t), "rows": rows,
            "rounds_cited": cited, "rounds_cited_that_do_not_exist": missing,
            "首選_route": "Strong-BSD twist families",
            "most_worked_route_here": first["route"], "most_worked_count": first["count"],
            "runner_up": runner_up["route"], "runner_up_count": runner_up["count"],
            "首選_is_most_worked": first["route"] == "Strong-BSD twist families",
            "red_routes": [r["route"] for r in red],
            "red_routes_worked_by_any_round": red_worked,
            "RUN_003_documents_scanned": scanned,
            "RUN_003_documents_claiming_the_red_routes_conditions_met": claimed_met,
            "red_route_claimed_met_nowhere": claimed_met == 0,
            "mcdm_line": "(G5, U3, X2–X3, P4–P5) — 04 calls it a routing estimate, not a theorem",
            "mcdm_present": "G5" in t and "U3" in t and "不是數學定理" in t,
            "reading": ("the mapping of rounds to routes is a reading, as at RUN-050; the "
                        "computed facts are that every cited round exists, the 首選 route "
                        "is the most worked by a wide margin, the 紅燈 route has no round "
                        "here and no document in the corpus claims its conditions met")}


# ---------------------------------------------------------------- 08

AGENTS = (
    ("A", "Statement Auditor — BSD-W/F/S dependency DAG; never rank equality = full BSD; never analytic Sha = actual Sha",
     "RUN-004 (01 §6's arithmetic table recomputed), RUN-002 (the ladder's eleven rungs), RUN-043 (this line's position on the claim ladder), RUN-051 (eleven prohibitions in one place)",
     "fulfilled"),
    ("B", "Banwait–Huang Reproducer — samples, then conductor <= 500,000; unknown, never guessed",
     "RUN-055 … RUN-064 (Phase 1's census recomputed, no Sage run); 'unknown' kept visible: RUN-045's LOCAL_H2 = UNKNOWN",
     "fulfilled on the artefact side"),
    ("C", "Certificate Schema Engineer — numeric evidence / rigorous computation / external theorem / conditional theorem / actual proof kept apart",
     "RUN-030 (the 696.e1 certificate), RUN-032 (Referee A's checklist as a program), RUN-048 (the schema and the sieve)",
     "fulfilled"),
    ("D", "Rank-2 Wall Analyst — 389.a1: r_alg, r_an, Ω, Reg, c_p, E_tors, Sha, L''(1)/2!, each with value / how / rigorous? / theorem? / assumption? / missing certificate?",
     "RUN-023 (every term at 389.a1; #Ш BSD-inferred, i.e. an assumption), RUN-026 (rank 1 with every term computed here)",
     "fulfilled, with Sha the named assumption"),
    ("E", "Adversarial Referee — eight leaps to hunt; verdict PASS/FAIL/OPEN only",
     "RUN-010 (the drill, and every round after it); RUN-062 (the adversarial corpus); RUN-037 (a false box); RUN-046 (the corpus disagreeing with itself)",
     "fulfilled — this line is that referee"),
    ("F", "Internal Theory Quarantine — Neo.K's lattice/PRC drafts vs BSD: translatable / circular / new obligations; never into the external proof",
     "RUN-003 (the rejection holds and the corpus strengthened it), RUN-019 (the witness-network generalisation admits nothing new)",
     "fulfilled by measurement"),
)

LEAPS_E = ("circular BSD assumption", "numerical-to-proof leap", "finite-to-global leap",
           "p-part-to-full leap", "rank0/1-to-high-rank leap", "isogeny double counting",
           "database incompleteness", "normalization mismatch")

# for each of E's leaps: the rounds that caught an instance, each with the
# phrase its report must contain for the attribution to stand
CAUGHT = {
    "circular BSD assumption": [("RUN-023", "BSD-inferred")],
    "numerical-to-proof leap": [("RUN-013", "float64"), ("RUN-017", "period"), ("RUN-055", "float")],
    "finite-to-global leap": [("RUN-041", "P_loc"), ("RUN-051", "substitut")],
    "p-part-to-full leap": [("RUN-043", "C1"), ("RUN-021", "ledger")],
    "rank0/1-to-high-rank leap": [("RUN-050", "High rank 2+"), ("RUN-026", "rank-1")],
    "isogeny double counting": [("RUN-008", "122,247"), ("RUN-031", "Mazur")],
    "database incompleteness": [("RUN-063", "36,687"), ("RUN-055", "247,391")],
    "normalization mismatch": [("RUN-042", "square class"), ("RUN-062", "CRLF")],
}


def handoff_08(reports: dict[str, str]) -> dict:
    t = _doc("08_Local_Agent_Handoff_Prompts.md")
    rows = [{"agent": a, "brief": b, "this_line": c, "state": d} for a, b, c, d in AGENTS]
    cited = _cited(*(c for _, _, c, _ in AGENTS))
    missing = _missing(reports, cited)
    briefs_in_doc = [a for a, *_ in AGENTS if f"Agent {a}" in t]
    leaps_in_doc = [k for k in LEAPS_E if k in t]
    sigs = [x for k in LEAPS_E for x in CAUGHT.get(k, [])]
    sig_absent = _signatures_absent(reports, sigs)
    absent_pairs = {(s["round"], s["phrase"]) for s in sig_absent}
    covered = [k for k in LEAPS_E if CAUGHT.get(k)
               and not any((rn, ph) in absent_pairs for rn, ph in CAUGHT[k])]
    return {"document_found": bool(t), "rows": rows, "count": len(rows),
            "briefs_named_in_08": briefs_in_doc,
            "rounds_cited": cited, "rounds_cited_that_do_not_exist": missing,
            "fulfilled": [r["agent"] for r in rows if r["state"].startswith("fulfilled")],
            "Es_eight_leaps": list(LEAPS_E), "leaps_named_in_08": leaps_in_doc,
            "Es_leaps_caught_here": {k: [f"{rn} ({ph})" for rn, ph in v] for k, v in CAUGHT.items()},
            "leap_signatures_checked": len(sigs), "leap_signatures_absent": sig_absent,
            "leaps_covered": len(covered),
            "reading": ("08 was written before any round ran. Read after 64 rounds, every "
                        "brief has rounds that did it, and every one of E's eight leaps has "
                        "rounds that caught an instance — several of them in this line's own "
                        "earlier work (RUN-017's period, RUN-055's float, RUN-026's rank-1 hold)")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    reports = _reports()
    c02 = closure_map_02(reports)
    r04 = route_matrix_04(reports)
    h08 = handoff_08(reports)
    ok = (c02["document_found"] and c02["table_present"] and c02["box_present"]
          and c02["no_open_row_claimed_closed"] and len(c02["open_rows"]) == 4
          and not c02["rounds_cited_that_do_not_exist"]
          and not c02["component_signatures_absent"]
          and r04["document_found"] and r04["首選_is_most_worked"]
          and not r04["red_routes_worked_by_any_round"] and r04["red_route_claimed_met_nowhere"]
          and not r04["rounds_cited_that_do_not_exist"] and r04["mcdm_present"]
          and h08["document_found"] and h08["count"] == 6
          and len(h08["briefs_named_in_08"]) == 6 and len(h08["leaps_named_in_08"]) == 8
          and not h08["rounds_cited_that_do_not_exist"]
          and not h08["leap_signatures_absent"] and h08["leaps_covered"] == 8)
    log = {"gate": "src67 — Phase 0's three maps against 64 rounds",
           "source": ", ".join(THREE),
           "closure_map_02": c02, "route_matrix_04": r04, "handoff_08": h08,
           "headline": (f"02's table: four open rows, and no report claims any of them "
                        f"closed; {c02['components_computed_here']} of strong BSD's seven "
                        f"components computed here, the regulator without saturation, Sha "
                        f"never. 04's matrix: the 首選 route is the most worked "
                        f"({r04['most_worked_count']} rounds to the runner-up's "
                        f"{r04['runner_up_count']}), the 紅燈 route has no round and RUN-003 "
                        f"found {r04['RUN_003_documents_claiming_the_red_routes_conditions_met']} "
                        f"of {r04['RUN_003_documents_scanned']} documents claiming its conditions "
                        f"met. 08's six briefs all have rounds; E's eight leaps all have a caught "
                        f"instance, {h08['leap_signatures_checked']} attributions verified by "
                        f"signature phrase"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  02: open rows {len(c02['open_rows'])}; claimed closed by a report: "
          f"{c02['open_rows_claimed_closed_by_any_report'] or 'none'}; components "
          f"computed {c02['components_computed_here']}/7, partial {c02['components_partial_here']}, "
          f"never {c02['components_never_here']}; signatures absent {c02['component_signatures_absent'] or 'none'}")
    print(f"  04: 首選 most worked {r04['首選_is_most_worked']} ({r04['most_worked_count']} vs "
          f"{r04['runner_up_count']}); red route worked {r04['red_routes_worked_by_any_round'] or 'none'}; "
          f"claimed met in corpus: {r04['RUN_003_documents_claiming_the_red_routes_conditions_met']}")
    print(f"  08: briefs {h08['briefs_named_in_08']}; leaps named {len(h08['leaps_named_in_08'])}/8; "
          f"covered {h08['leaps_covered']}/8; signatures absent {h08['leap_signatures_absent'] or 'none'}")
    print(f"  rounds cited that do not exist: "
          f"{c02['rounds_cited_that_do_not_exist'] + r04['rounds_cited_that_do_not_exist'] + h08['rounds_cited_that_do_not_exist'] or 'none'}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
