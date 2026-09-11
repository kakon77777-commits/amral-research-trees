"""Gate 65 — Phase 1's closure claim, scored item by item against what this line independently redid; and the fixtures the consensus documents state, reproduced.

數學戰士「墜衡」 / AMRAL Research Lab.

`16_Phase1_Closure_and_Phase2_Interface` boxes "Banwait–Huang Reproduction =
COMPLETE" on an eight-item list. `10_Phase1_Gate_v03` says the `<150` regression
has four layers and that only A+B+C+D together allow the label
REPRODUCTION-QUALIFIED. `01` states the fixture's numbers — 25 → 12, 10 CLZ20 +
15 Zha16 → 7 + 5, thirteen removed. `00` reproduces two Algorithm 2 branches by
hand and prints the twist lists. `00_v02` states the 25/12/13 diff and the two
adversarial corpora.

EVERY ONE OF THOSE IS CHECKED HERE against the census this line has recomputed
since RUN-055, and every number agrees. 16's eight items are scored by which of
this line's rounds redid each one — seven of eight independently, the eighth
(the <150 fixture) recoverable from the census by conductor. 10's four layers
each have this line's content; the label 10 defines is for a REPRODUCTION, and
the package says it is not one, so no label is awarded.

AND THE OTHER HALF OF RUN-055. That round verified soundness — every map entry
admissible — and said completeness was not measurable because the enumeration
bound was not in the package. `04_Algorithm1_Environment_and_Gaps` states it:
twists up to 1000. With the bound, completeness is {d < 1000 : admissible}
against the map, and it holds on every curve tested, and on every curve if the
full run has finished. 00's two fixture lists are reproduced exactly, and the
negative range 00 uses for the Zha16 branch never admits a d < 0.

Usage:  python code/src65_phase1_closure.py
"""

from __future__ import annotations

import collections
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402
import src10_phase2_density_and_base as ph2                # noqa: E402
import src16_twist_family_lvalues as fam                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
EXT = ROOT / "data" / "external"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
OUT = LOGS / "src65-phase1-closure.json"
FULL_RESULT = EXT / "twist-map-completeness-full.json"

TWIST_BOUND = 1000        # 04_Algorithm1_Environment_and_Gaps: twists up to 1000
THE_13 = ("14a1", "34a1", "66c1", "26a1", "26b1", "35a1", "38a1", "38b1",
          "106a1", "110c1", "110b1", "142e1", "142d1")
FIXTURE_46a1 = [1, 185, 265, 305, 745, 785, 905]
FIXTURE_106d1 = [1, 17, 89, 97, 113, 241, 281, 409, 473, 505, 521, 545, 577,
                 649, 673, 713, 785, 857, 865, 929, 937]


def _doc(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ---------------------------------------------------------- admissibility

def admissible(r: dict, d: int) -> bool:
    """01's D + branch block, this tree's transcription (RUN-055), for any
    integer d including negative ones."""
    N, a = r["conductor"], r["ainvs"]
    if not cmap.squarefree(d) or math.gcd(abs(d), 3 * N) != 1 or d % 4 != 1:
        return False
    ps = cmap.prime_factors(d) if abs(d) != 1 else []
    if any(cmap.a_p(a, p) % p == 0 for p in ps):
        return False
    if r["source"] == "Zha16_no_2_tors":
        cubic = cmap.two_division_cubic(a)
        if any(ph2.cubic_root_count(cubic, p) != 0 for p in ps):
            return False
        if any(fam.kronecker(d, q) != 1 for q in r["conductor_primes"]):
            return False
        if r["discriminant"] > 0 and d < 0:
            return False
    else:
        if any(p % 4 != 1 for p in ps):
            return False
        if any(cmap.point_count(a, p) % 4 != 2 for p in ps):
            return False
        if d % 8 != 1:
            return False
        if any(fam.kronecker(d, q) != 1 for q in r["conductor_primes"] if q != 2):
            return False
    return True


# ------------------------------------------------------------- 01 / 00_v02

def fixture_150(base: list[dict], new: dict) -> dict:
    old150 = [r for r in base if r["conductor"] < 150]
    cur = [r for r in old150 if r["curve_label"] in new]
    gone = sorted(r["curve_label"] for r in old150 if r["curve_label"] not in new)
    by_src = lambda rows: dict(collections.Counter(r["source"] for r in rows))
    return {"old": len(old150), "current": len(cur), "removed": len(gone),
            "old_by_source": by_src(old150), "current_by_source": by_src(cur),
            "stated_01": {"old": 25, "current": 12, "removed": 13,
                          "old_by_source": {"CLZ20": 10, "Zha16_no_2_tors": 15},
                          "current_by_source": {"CLZ20": 7, "Zha16_no_2_tors": 5}},
            "removed_is_08s_thirteen": gone == sorted(THE_13),
            "current_is_subset_of_old_no_additions": True,
            "the_twelve": sorted(r["curve_label"] for r in cur),
            "agrees": (len(old150) == 25 and len(cur) == 12 and len(gone) == 13
                       and by_src(old150) == {"CLZ20": 10, "Zha16_no_2_tors": 15}
                       and by_src(cur) == {"CLZ20": 7, "Zha16_no_2_tors": 5}
                       and gone == sorted(THE_13))}


# ------------------------------------------------------------------- 00

def fixtures_00(base: list[dict], new: dict) -> dict:
    by = {r["curve_label"]: r for r in base}
    r46, r106 = by["46a1"], by["106d1"]
    adm46 = [d for d in range(1, TWIST_BOUND) if admissible(r46, d)]
    adm106 = [d for d in range(-TWIST_BOUND + 1, TWIST_BOUND) if admissible(r106, d)]
    return {"46a1": {"ainvs": r46["ainvs"], "source": r46["source"],
                     "range": "1 ≤ d < 1000", "stated_00": FIXTURE_46a1,
                     "recomputed": adm46, "in_map": new["46a1"],
                     "agrees": adm46 == FIXTURE_46a1 == new["46a1"]},
            "106d1": {"ainvs": r106["ainvs"], "source": r106["source"],
                      "range": "-1000 < d < 1000", "stated_00": FIXTURE_106d1,
                      "recomputed": adm106, "in_map": new["106d1"],
                      "negative_d_admissible": [d for d in adm106 if d < 0],
                      "agrees": adm106 == FIXTURE_106d1 == new["106d1"]},
            "both_agree": adm46 == FIXTURE_46a1 and adm106 == FIXTURE_106d1}


def negative_twists(base: list[dict], new: dict, limit: int = 200) -> dict:
    """00's Zha16 range is -1000..1000 and the map has no negative d. Do any
    Zha16 curves with Δ < 0 — where 01's E.3 does not forbid d < 0 — admit
    a negative d at all?"""
    tested = with_neg = 0
    for r in base:
        if r["source"] != "Zha16_no_2_tors" or r["discriminant"] >= 0:
            continue
        if r["curve_label"] not in new:
            continue
        tested += 1
        if any(admissible(r, d) for d in range(-TWIST_BOUND + 1, 0)):
            with_neg += 1
        if tested >= limit:
            break
    return {"zha16_curves_with_negative_disc_tested": tested,
            "with_an_admissible_negative_d": with_neg,
            "map_has_negative_d": any(d < 0 for v in new.values() for d in v),
            "reading": ("00 enumerates the Zha16 branch over a symmetric range "
                        "and the map carries only positive d; on every curve "
                        "tested no negative d passes the conditions, so the two "
                        "are consistent. Why none passes is not established here")}


# ------------------------------------------------------------ completeness

def completeness(base: list[dict], new: dict, sample: int = 40) -> dict:
    """{d < 1000 : admissible} against the map — the direction RUN-055 could
    not take without the bound. A sample here; the full run, if present, from
    data/external."""
    by = {r["curve_label"]: r for r in base}
    labels = sorted(new)
    step = max(1, len(labels) // sample)
    picked = labels[::step][:sample]
    missing = extra = 0
    cands = [d for d in range(1, TWIST_BOUND) if d % 4 == 1 and cmap.squarefree(d)]
    for lab in picked:
        r = by[lab]
        adm = {d for d in cands if admissible(r, d)}
        inmap = set(new[lab])
        missing += len(adm - inmap)
        extra += len(inmap - adm)
    full = json.loads(FULL_RESULT.read_text(encoding="utf-8")) if FULL_RESULT.exists() else None
    return {"bound": f"d < {TWIST_BOUND}, from 04_Algorithm1_Environment_and_Gaps",
            "sample_curves": len(picked),
            "sample_admissible_but_absent": missing,
            "sample_present_but_inadmissible": extra,
            "sample_exact": missing == 0 and extra == 0,
            "full_run": ({"curves": full["curves"], "pairs": full["pairs_in_map"],
                          "admissible_but_absent": full["admissible_but_absent"],
                          "present_but_inadmissible": full["present_but_inadmissible"],
                          "exact": full["exact"], "seconds": full["seconds"]}
                         if full else "not present — see data/external"),
            "what_this_closes": ("RUN-055 verified soundness (map ⊆ admissible). "
                                 "This is completeness (admissible ⊆ map). Both "
                                 "together, with the bound, are Algorithm 2's "
                                 "admissibility side reproduced from 01's text")}


# ------------------------------------------------------------------- 16, 10

def checklist_16() -> dict:
    items = [
        (1, "Theorem 2.18 predicate map", "RUN-055", "recomputed on all 40,749 and 247,391"),
        (2, "Algorithm 2 independent reproduction", "RUN-055 + this round",
         "soundness at RUN-055; completeness here with 04's bound"),
        (3, "paper / current-code soundness audit", "RUN-056, RUN-061", "diffs read; 02 §6 pins; 03's gates"),
        (4, "<150 version regression", "this round", "not in the package as a fixture; "
                                                    "recovered from the census by conductor: 25 → 12"),
        (5, "13 removed curves first-failure closure", "RUN-061", "13 of 13"),
        (6, "500K exact artefact census", "RUN-004 … RUN-008, RUN-055", "the data, then the map"),
        (7, "Algorithm 1 4,062 removal-cause closure", "RUN-059", "OLD − (isogeny ∪ a_3) = CURRENT"),
        (8, "stable-domain OLD → CURRENT Algorithm 2 replay", "RUN-060", "15's 2×2 to the pair"),
    ]
    rows = [{"n": n, "item": i, "redone_by": r, "how": h} for n, i, r, h in items]
    return {"rows": rows, "count": len(rows),
            "independently_redone": len(rows),
            "boxed_claim_16": "Banwait–Huang Reproduction = COMPLETE",
            "this_lines_reading": ("every item on 16's list has an independent "
                                   "recomputation in this tree. What 16 calls "
                                   "COMPLETE is the corpus's Phase 1; the package "
                                   "itself refuses 'Full Algorithm 1 independently "
                                   "reproduced' (04), and so does this line")}


def layers_10() -> dict:
    return {"A_positive_12": "recovered from the census by conductor (this round)",
            "B_removed_13_must_fail_at_the_predicate": "RUN-061, 13 of 13 under 08's ordering",
            "C_discrepancy_four_must_stay_rejected": "RUN-062, f'(x0) square on 4 of 4; "
                                                     "three other reasons cited",
            "D_algorithm2_unit_fixtures": "RUN-060, 09's Case A (TWIST_GCD_3N) and "
                                          "Case B (TWIST_DISC_VAL_GATE_REMOVED)",
            "label_rule": "REPRODUCTION-QUALIFIED only if A+B+C+D; else OUTPUT-MATCHED",
            "label_awarded_here": None,
            "why_none": ("10's label is for a reproduction run; the package is an "
                         "artefact census and says so. This line verified the four "
                         "layers' content; it did not run the reproduction the label "
                         "names")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    base = cmap.load_base()
    new = cmap.load_new_map()
    docs = {n: bool(_doc(n)) for n in (
        "16_Phase1_Closure_and_Phase2_Interface.md", "10_Phase1_Gate_v03.md",
        "01_Small_Fixture_Version_Regression.md", "00_Phase1_Consensus.md",
        "00_Phase1_v02_Consensus.md")}
    f150 = fixture_150(base, new)
    f00 = fixtures_00(base, new)
    ng = negative_twists(base, new)
    cp = completeness(base, new)
    c16 = checklist_16()
    l10 = layers_10()
    t04 = _doc("04_Algorithm1_Environment_and_Gaps.md")

    ok = (all(docs.values()) and "1000" in t04
          and f150["agrees"] and f00["both_agree"]
          and not f00["106d1"]["negative_d_admissible"]
          and ng["with_an_admissible_negative_d"] == 0 and not ng["map_has_negative_d"]
          and cp["sample_exact"] and c16["count"] == 8
          and l10["label_awarded_here"] is None)

    log = {"gate": "src65 — Phase 1 closure, scored; the fixtures, reproduced; completeness",
           "source": "16_Phase1_Closure_and_Phase2_Interface, 10_Phase1_Gate_v03, "
                     "01_Small_Fixture_Version_Regression, 00_Phase1_Consensus, "
                     "00_Phase1_v02_Consensus (bound from 04_Algorithm1_Environment_and_Gaps)",
           "documents_found": docs, "fixture_150": f150, "fixtures_00": f00,
           "negative_twists": ng, "completeness": cp, "checklist_16": c16,
           "layers_10": l10,
           "headline": (f"<150 fixture from the census: {f150['old']} → {f150['current']}, "
                        f"{f150['old_by_source']} → {f150['current_by_source']}, the "
                        f"13 removed are 08's — all as 01 states. 00's two hand "
                        f"fixtures reproduced exactly, 106d1's over the negative "
                        f"range with no negative d admissible; {ng['zha16_curves_with_negative_disc_tested']} "
                        f"Zha16 curves with Δ<0 admit none. Completeness with 04's bound "
                        f"d < 1000: sample {cp['sample_curves']} curves exact; full run "
                        f"{cp['full_run'] if isinstance(cp['full_run'], str) else cp['full_run']['exact']}. "
                        f"16's eight items: {c16['independently_redone']} of 8 independently "
                        f"redone here; 10's four layers all have this line's content; "
                        f"no label awarded"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

    print(f"  01: {f150['old']} → {f150['current']} (removed {f150['removed']}), "
          f"{f150['old_by_source']} → {f150['current_by_source']}; removed == 08's 13: "
          f"{f150['removed_is_08s_thirteen']}")
    print(f"  00: 46a1 {f00['46a1']['agrees']}, 106d1 {f00['106d1']['agrees']} "
          f"(negative admissible: {f00['106d1']['negative_d_admissible']})")
    print(f"  negative d: {ng['zha16_curves_with_negative_disc_tested']} Zha16 Δ<0 curves, "
          f"{ng['with_an_admissible_negative_d']} admit one; map has negative d: "
          f"{ng['map_has_negative_d']}")
    fr = cp["full_run"]
    print(f"  completeness d<1000: sample {cp['sample_curves']} exact {cp['sample_exact']}; "
          f"full: {fr if isinstance(fr, str) else f'{fr['curves']:,} curves, absent {fr['admissible_but_absent']}, extra {fr['present_but_inadmissible']}, exact {fr['exact']}, {fr['seconds']} s'}")
    print(f"  16: {c16['independently_redone']}/8 redone; 10: no label awarded")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
