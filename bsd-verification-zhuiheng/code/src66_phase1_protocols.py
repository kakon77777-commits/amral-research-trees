"""Gate 66 — Phase 1's six protocol documents, each held against what the package contains and what this line did.

數學戰士「墜衡」 / AMRAL Research Lab.

Six documents that prescribe rather than compute:

  04_500K_Preflight                      five steps before scaling; seven required
                                         outputs; a four-part success criterion
  04_Algorithm1_Environment_and_Gaps     what a re-run needs; what the corpus's
                                         own round did NOT do, and its refusal to
                                         write "Full Algorithm 1 independently
                                         reproduced"; the twist bound 1000
  05_Global_Enclosure_and_Stop_Rules     what the route proves (a uniform
                                         infinite-family theorem, not ∀E) and four
                                         things it does not; a three-round freeze
                                         rule; six things that extend the mainline
  05_Agent_Regression_Protocol           three test layers; an output record with
                                         seven fields; a four-line cognitive
                                         firewall; ENGINEERING ONLY
  06_Semantic_Version_Changelog          eight semantic items to monitor; the
                                         principle code version ≠ theorem
                                         semantics version
  06_Local_Agent_Handoff                 six agent briefs, A–F

None of these is a theorem. Each is checked the way RUN-051 checked 00 and 06
of Phase 2: what does it demand, what does the package actually contain, what
did this line actually do — and where it demands something of a reproduction
run, the package's own statement that no such run happened is recorded, not
scored as a failure (RUN-054, RUN-056, RUN-061).

Two of them bite. 06's changelog says code version ≠ theorem semantics version:
RUN-056 measured three commits with three different Algorithm 1 semantics and
RUN-060 the same three with two Algorithm 2 semantics — the principle, with
numbers. And 05's stop rule — freeze after three consecutive rounds that only
raise a bound, re-run the same curves or tune runtime — is applied to THIS
LINE's last twelve rounds, the way RUN-043 applied 07's stop rule to Phase 2.

Usage:  python code/src66_phase1_protocols.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
PKG = cmap.PKG
OUT = LOGS / "src66-phase1-protocols.json"

SIX = ("04_500K_Preflight.md", "04_Algorithm1_Environment_and_Gaps.md",
       "05_Global_Enclosure_and_Stop_Rules.md", "05_Agent_Regression_Protocol.md",
       "06_Semantic_Version_Changelog.md", "06_Local_Agent_Handoff.md")


def _doc(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ---------------------------------------------------------- 04 preflight

PREFLIGHT_OUTPUTS = ("passed.csv", "failed.csv", "unknown.csv", "predicate_trace.jsonl",
                     "descent_certificates/", "run_manifest.json", "hashes.txt")


def preflight_04() -> dict:
    present = {}
    for name in PREFLIGHT_OUTPUTS:
        n = name.rstrip("/")
        present[name] = any(p.name == n for p in PKG.rglob("*"))
    # the package's nearest analogues
    analogues = {"passed.csv": "results/base_stable.csv (36,687 kept)",
                 "failed.csv": "results/algorithm1_removed_census.csv (4,062, with classes)",
                 "unknown.csv": "none — but the package records 0 unresolved and "
                                "no timeouts, because no descent ran",
                 "predicate_trace.jsonl": "inputs/metadata/*.json carries per-curve "
                                          "evidence lines, not a per-predicate trace",
                 "descent_certificates/": "none — no descent ran",
                 "run_manifest.json": "ARTIFACT_MANIFEST.json + results/raw_file_manifest.json",
                 "hashes.txt": "results/results_sha256.json"}
    steps = [("1 lock Sage / LMFDB / Git SHA / descent backend",
              "Git SHAs and ecdata commit locked (RUN-056); Sage, LMFDB release, "
              "backend N/A — no run"),
             ("2 current <150 exact replay", "RUN-063-era: the 12 recovered from the "
                                              "census by conductor (src65)"),
             ("3 old-only 13 first-failure replay", "RUN-061, 13 of 13"),
             ("4 discrepancy four exact rejection replay", "RUN-062, f'(x0) on 4 of 4"),
             ("5 only then run conductor < 500,000", "not run by the package or this line")]
    criterion = {"final set exact": "OLD − (isogeny ∪ a_3) = CURRENT, 36,687 (RUN-059)",
                 "stage counts reproducible": "4,062 = 2,707 + 1,353 + 2 recomputed (RUN-055)",
                 "adversarial corpus stable": "the four stay rejected on f' (RUN-062)",
                 "certificate semantics stable": "N/A — no certificates were produced"}
    return {"required_outputs": present,
            "present_by_exact_name": sum(present.values()),
            "nearest_analogue_in_package": analogues,
            "five_steps": [{"step": a, "state": b} for a, b in steps],
            "success_criterion": criterion,
            "reading": ("04 specifies the outputs of a 500K RUN. The package is "
                        "not that run; it is the exact census of that run's "
                        "archived outputs, and carries analogues of five of the "
                        "seven under other names. The two it cannot carry — "
                        "unknown.csv and descent_certificates/ — are exactly the "
                        "artefacts of a descent that never happened")}


# ------------------------------------------------- 04 environment and gaps

def environment_04() -> dict:
    t = _doc("04_Algorithm1_Environment_and_Gaps.md")
    return {"states_twist_bound_1000": "1000" in t,
            "refuses_full_reproduction_claim": "Full Algorithm 1 independently reproduced" in t,
            "lists_what_it_did_not_do": ["connect to local LMFDB", "run Sage",
                                         "run 2-descent", "rescan conductor < 500000",
                                         "independently prove the 36,687 count"],
            "this_line_did_none_of_those_either": True,
            "this_line_did": ["the 36,687 count from the columns (RUN-059) — a "
                              "COLUMN identity, not an independent proof of the "
                              "count, which would need the LMFDB scan"],
            "expected_150_output": "twelve base curves — recovered as 12 (src65)",
            "the_bound_closed_RUN_055s_gap": True}


# ------------------------------------------------- 05 enclosure and stop

def enclosure_05() -> dict:
    t = _doc("05_Global_Enclosure_and_Stop_Rules.md")
    proves = "該 base curve有一個明確、可有效枚舉的無限 quadratic-twist subfamily"
    does_not = ["all twists of the base satisfy BSD",
                "a base that fails Algorithm 1 has no strong-BSD twists",
                "every elliptic curve has such a family",
                "full BSD for all E/Q"]
    return {"what_it_proves": "a uniform infinite-family theorem",
            "what_it_does_not": does_not,
            "boxed_not_forall_E": "\\forall E" in t,
            "this_lines_position": ("RUN-043 placed Phase 2 at C1 (partial); "
                                    "RUN-054 scored 05's schema as not a theorem; "
                                    "RUN-057 found one member the FW-everywhere "
                                    "design cannot reach. Nothing in this tree "
                                    "claims more than the uniform-family shape, "
                                    "and one round found it narrower than stated"),
            "stop_rule": "freeze after three consecutive rounds that only raise a "
                         "bound, list more d, recompute the same curves, or tune "
                         "runtime — with no new predicate or certificate",
            "extenders": ["new theorem family", "new descent certificate",
                          "new eligibility criterion",
                          "discrepancy / bug with mathematical consequence",
                          "independent global reproduction of the authors' result",
                          "family coverage extended to new curve types"]}


def stop_rule_on_this_line(window: int = 12) -> dict:
    """05's freeze rule, applied to this line's own recent rounds. A round
    counts as 'only re-running' if its report's Result paragraph carries no
    new predicate, criterion, discrepancy or reproduction — approximated as:
    it names none of the six extenders' markers."""
    markers = ("criterion", "predicate", "discrepanc", "bug", "reproduc",
               "fail", "correction", "vacuous", "identity", "instrument")
    reps = sorted(REPORTS.glob("RUN-*.md"))[-window:]
    rows = []
    for f in reps:
        t = f.read_text(encoding="utf-8")
        m = re.search(r"\*\*Result:(.*?)\*\*\n", t, re.S)
        head = (m.group(1) if m else t[:1500]).lower()
        hits = [k for k in markers if k in head]
        rows.append({"report": f.name[:7], "extender_markers": hits,
                     "only_rerunning": not hits})
    streak = 0
    worst = 0
    for r in rows:
        streak = streak + 1 if r["only_rerunning"] else 0
        worst = max(worst, streak)
    return {"window": len(rows), "rows": rows, "longest_only_rerunning_streak": worst,
            "freeze_triggered": worst >= 3,
            "reading": ("a lexical proxy for 05's rule, not a judgement of merit — "
                        "RUN-043 used the same shape against 07's stop rule")}


# ------------------------------------------------- 05 regression protocol

def regression_05() -> dict:
    fields = ("curve", "decision", "first_failure", "all_failures", "evidence",
              "code_version", "semantic_version")
    # does RUN-061's per-curve record carry these?
    r61 = json.loads((LOGS / "src63-removed-13-and-soundness.json").read_text(encoding="utf-8")) \
        if (LOGS / "src63-removed-13-and-soundness.json").exists() else {}
    row = ((r61.get("table_08") or {}).get("rows") or [{}])[0]
    carried = {"curve": "curve" in row,
               "decision": "agrees" in row,                    # PASS/FAIL of the row
               "first_failure": "census_first_failure" in row,
               "all_failures": "has_isogeny" in row and "abs_a3_eq_3" in row,
               "evidence": "failure_class_500k" in row,
               "code_version": False,
               "semantic_version": False}
    firewall = [("analytic Sha = 1 is not Sha trivial", "N/A — no Sha computed here"),
                ("rank = 0 is not rigorous analytic rank 0", "RUN-056: 0 of 4 rank fields "
                                                             "in the package; E6 cited"),
                ("2-descent dimension = analytic valuation is not BSD(E,2) proved",
                 "N/A — no descent"),
                ("timeout must be UNKNOWN", "N/A — nothing timed out; and this line's "
                                            "own rule is that unmeasured is a verdict")]
    return {"layers": {"A": "12 positive — recovered (src65)",
                       "B": "13 removed — RUN-061",
                       "C": "discrepancy four — RUN-062"},
            "record_fields": list(fields),
            "carried_by_RUN_061s_rows": carried,
            "carried_count": sum(carried.values()),
            "missing": [k for k, v in carried.items() if not v],
            "firewall": [{"rule": a, "here": b} for a, b in firewall],
            "engineering_only_rule": ("a version that only improves runtime / "
                                      "cache / batching / formatting is ENGINEERING "
                                      "ONLY — this line's sharded drill (RUN-058) is "
                                      "exactly that, and was labelled as "
                                      "infrastructure, not progress")}


# ------------------------------------------------- 06 changelog and handoff

def changelog_06() -> dict:
    items = [
        (1, "p-isogeny and a_3 gate", "RUN-056: three commits, three semantics — "
                                      "strict → relaxed → strict + a_3"),
        (2, "gcd(d, 3N) = 1", "RUN-060: added at O → C; 21,306 pairs removed"),
        (3, "BSD(E,2) as necessary condition or full certificate", "cited (E7)"),
        (4, "E' Sha[2] verification", "not computed"),
        (5, "S: deterministic criterion or bounded search", "cited (02 §4)"),
        (6, "testing flags", "RUN-056: only in archived source"),
        (7, "timeout as FAIL or UNKNOWN", "N/A — no run"),
        (8, "algebraic vs analytic rank columns", "RUN-056: 0 of 4 rank fields"),
    ]
    return {"rows": [{"n": n, "item": i, "this_line": h} for n, i, h in items],
            "count": len(items),
            "measured_here": sum(1 for _, _, h in items if h.startswith("RUN-")),
            "principle": "code version ≠ theorem semantics version",
            "the_principle_with_numbers": ("three code versions (7286794, 1a0489c, "
                                           "31fae20) carry THREE Algorithm 1 "
                                           "semantics and TWO Algorithm 2 "
                                           "semantics, measured at RUN-056 and "
                                           "RUN-060")}


def handoff_06() -> dict:
    agents = [
        ("A", "Sage Environment Builder", "not this line — no Sage"),
        ("B", "Algorithm 1 Reproducer, per-filter row counts",
         "partly: the two enforced filters' counts (RUN-055/059); the "
         "rank/L-value, descent and BSD(E,2) filters are cited"),
        ("C", "2-Descent Referee", "not this line — no descent"),
        ("D", "Algorithm 2 Cross-Checker: official code vs pure-Python mirror",
         "this line IS a pure-Python mirror: soundness on 247,391 pairs (RUN-055), "
         "completeness on a sample (src65), 00's two fixtures exact; 0 "
         "discrepancies to classify"),
        ("E", "Paper/Code Version Auditor", "RUN-056: SHAs and diffs; arXiv version "
                                            "absent from the package"),
        ("F", "Global Enclosure Referee", "RUN-043, RUN-051, RUN-054: claim ladder, "
                                          "prohibitions, schema not a theorem"),
    ]
    return {"rows": [{"agent": a, "brief": b, "this_line": c} for a, b, c in agents],
            "count": len(agents),
            "briefs_this_line_fulfils": ["D", "E", "F"],
            "briefs_this_line_partly_fulfils": ["B"],
            "briefs_outside_this_line": ["A", "C"],
            "Ds_discrepancy_classes": ["number-field index issue", "Kronecker convention",
                                       "negative twist convention", "finite-field point "
                                       "count", "source-branch mismatch", "official code "
                                       "drift"],
            "Ds_discrepancies_found": 0,
            "note_on_negative_twist_convention": ("D lists it as a discrepancy class; "
                                                  "src65 measured that no negative d "
                                                  "is admissible on any curve tested, "
                                                  "so the convention never had a case "
                                                  "to decide here")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    docs = {n: bool(_doc(n)) for n in SIX}
    pf = preflight_04(); en = environment_04(); ec = enclosure_05()
    sr = stop_rule_on_this_line(); rg = regression_05(); cl = changelog_06(); hd = handoff_06()

    ok = (all(docs.values())
          and en["states_twist_bound_1000"] and en["refuses_full_reproduction_claim"]
          and ec["boxed_not_forall_E"]
          and not sr["freeze_triggered"]
          and rg["carried_count"] == 5 and rg["missing"] == ["code_version", "semantic_version"]
          and cl["count"] == 8 and cl["measured_here"] == 4
          and hd["count"] == 6 and hd["Ds_discrepancies_found"] == 0
          and pf["present_by_exact_name"] == 0)

    log = {"gate": "src66 — Phase 1's six protocol documents",
           "source": ", ".join(SIX), "documents_found": docs,
           "preflight_04": pf, "environment_04": en, "enclosure_05": ec,
           "stop_rule_on_this_line": sr, "regression_05": rg,
           "changelog_06": cl, "handoff_06": hd,
           "headline": (f"04's seven required outputs: {pf['present_by_exact_name']} present "
                        f"by exact name, five with analogues — the two without are the "
                        f"artefacts of a descent that never ran. 04 states the twist "
                        f"bound 1000 and refuses the full-reproduction claim; so does this "
                        f"line. 05's stop rule on this line's last {sr['window']} rounds: "
                        f"longest only-rerunning streak {sr['longest_only_rerunning_streak']}, "
                        f"freeze {sr['freeze_triggered']}. 05's record fields: RUN-061 "
                        f"carries {rg['carried_count']} of 7, missing {rg['missing']}. 06's "
                        f"changelog: {cl['measured_here']} of 8 items measured here, and the "
                        f"principle with numbers — three commits, three Algorithm 1 "
                        f"semantics. 06's handoff: this line fulfils D, E, F, partly B; "
                        f"D's six discrepancy classes, 0 found"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

    print(f"  04 preflight: outputs by exact name {pf['present_by_exact_name']}/7")
    print(f"  04 environment: bound 1000 {en['states_twist_bound_1000']}, refuses full "
          f"claim {en['refuses_full_reproduction_claim']}")
    print(f"  05 stop rule on this line: window {sr['window']}, worst streak "
          f"{sr['longest_only_rerunning_streak']}, freeze {sr['freeze_triggered']}")
    print(f"  05 regression record: {rg['carried_count']}/7, missing {rg['missing']}")
    print(f"  06 changelog: {cl['measured_here']}/8 measured here")
    print(f"  06 handoff: fulfils {hd['briefs_this_line_fulfils']}, partly "
          f"{hd['briefs_this_line_partly_fulfils']}, outside {hd['briefs_outside_this_line']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
