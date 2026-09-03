"""Drill: can the profile validator actually refuse anything?

數學戰士「墜衡」 / AMRAL Research Lab.

On the two real files in this monorepo the validator reports no hard failure,
because neither declares a profile it does not satisfy. A validator that has
only ever agreed is the shape this tree spent the sweep cataloguing, so each
rule is driven with a document crafted to break it.

Documents are built in memory. No file on disk is read except the two real
ones used as controls, and neither is written.

The bar is this suite's usual one: a planted defect must be caught by the rule
NAMED for it. A document that fails for some other reason is a survivor.

Usage:  python code/validate_results_profiles_drill.py
"""

from __future__ import annotations

import copy
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

import validate_results_profiles as V  # noqa: E402

ENVELOPE = "results-envelope/1"
CLAIMS = "results-claims/1"


def good_doc() -> dict:
    """A minimal document that satisfies both profiles."""
    return {
        "schema_version": 1,
        "research_line_id": "drill-line",
        "researcher": {"display_name": "drill"},
        "date": "2026-09-03",
        "problem": {"id": "DRILL"},
        "global_status": {"solved": False, "statement": "nothing is claimed"},
        "verified_claims": [{"id": "V1", "claim": "a finite statement"}],
        "explicit_non_claims": ["nothing beyond the finite statement"],
    }


def main() -> int:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    except (AttributeError, ValueError):                 # pragma: no cover
        pass

    defects: dict[str, dict] = {}

    def plant(name: str, why: str, mutate, *, profile: str, needle: str):
        doc = good_doc()
        mutate(doc)
        res = V.evaluate(doc)
        missing = res["gaps"].get(profile, [])
        defects[name] = {
            "why": why,
            "refused": profile not in res["satisfies"],
            "named_check": any(needle in m for m in missing),
            "reported": missing,
        }

    plant("D1_no_boundary_statement",
          "a results file with no stated boundary must not pass the envelope",
          lambda d: d["global_status"].pop("statement"),
          profile=ENVELOPE, needle="global_status.statement")

    plant("D2_solved_is_a_string_not_a_boolean",
          "'false' is truthy; the solved flag must be typed, not merely present",
          lambda d: d["global_status"].__setitem__("solved", "false"),
          profile=ENVELOPE, needle="global_status.solved")

    plant("D3_a_verified_claim_without_its_text",
          "an id with no claim renders as an empty claim-box row",
          lambda d: d["verified_claims"].__setitem__(0, {"id": "V1"}),
          profile=CLAIMS, needle="needs both id and claim")

    plant("D4_an_empty_non_claim_string",
          "a blank non-claim is worse than none: it renders as a silent boundary",
          lambda d: d["explicit_non_claims"].append(""),
          profile=CLAIMS, needle="non-empty string")

    plant("D5_verified_claims_present_but_empty",
          "an empty array must not read as 'claims satisfied'",
          lambda d: d.__setitem__("verified_claims", []),
          profile=CLAIMS, needle="non-empty array")

    plant("D6_no_researcher",
          "a results file with no attributable author fails the envelope",
          lambda d: d.__setitem__("researcher", {}),
          profile=ENVELOPE, needle="researcher.display_name")

    # D7 - the prerequisite gate: claims must not be reported satisfied on a
    # document whose envelope is broken, even when the claims fields are perfect.
    doc = good_doc()
    doc["problem"] = {}
    res = V.evaluate(doc)
    defects["D7_claims_must_not_pass_over_a_broken_envelope"] = {
        "why": "a renderer told 'claims ok' would trust an unidentifiable file",
        "refused": CLAIMS not in res["satisfies"],
        "named_check": any("requires " + ENVELOPE in m
                           for m in res["gaps"].get(CLAIMS, [])),
        "reported": res["gaps"].get(CLAIMS, []),
    }

    # D8 - the one hard failure: declaring a profile and not satisfying it.
    doc = good_doc()
    doc.pop("explicit_non_claims")
    doc["profiles"] = [ENVELOPE, CLAIMS]
    res = V.evaluate(doc)
    defects["D8_declares_a_profile_it_does_not_satisfy"] = {
        "why": "an inferred gap is information; a false declaration is a lie",
        "refused": bool(res["declared_but_not_satisfied"]),
        "named_check": res["declared_but_not_satisfied"] == [CLAIMS],
        "reported": res["declared_but_not_satisfied"],
    }

    controls: dict[str, dict] = {}

    def control(name: str, why: str, doc: dict, expect: list[str]):
        res = V.evaluate(doc)
        controls[name] = {
            "why": why,
            "undisturbed": res["satisfies"] == expect
                           and not res["declared_but_not_satisfied"],
            "satisfies": res["satisfies"],
        }

    control("C1_a_document_meeting_both_profiles",
            "the healthy shape must pass, or the drill above proves nothing",
            good_doc(), [ENVELOPE, CLAIMS])

    extra = good_doc()
    extra["some_line_specific_section"] = {"whatever": [1, 2, 3]}
    extra["another"] = "line-specific"
    control("C2_line_specific_sections_are_not_policed",
            "profiles constrain the shared envelope, never a line's own content",
            extra, [ENVELOPE, CLAIMS])

    real = json.loads((ROOT / "data" / "results.v1.json").read_text(encoding="utf-8"))
    control("C3_this_tree_s_real_published_file",
            "the file a renderer will actually read must satisfy both",
            real, [ENVELOPE, CLAIMS])

    envelope_only = good_doc()
    envelope_only.pop("verified_claims")
    envelope_only.pop("explicit_non_claims")
    control("C4_envelope_only_is_a_valid_state_not_a_failure",
            "a line outside results-claims/1 is a rendering branch, not a defect",
            envelope_only, [ENVELOPE])

    planted = len(defects)
    caught = sum(1 for d in defects.values() if d["refused"] and d["named_check"])
    undisturbed = sum(1 for c in controls.values() if c["undisturbed"])

    log = {
        "tool": "validate_results_profiles_drill.py",
        "subject": "code/validate_results_profiles.py evaluate()",
        "note": ("each defect must be refused by the rule named for it; the "
                 "envelope-only control exists because NOT satisfying a profile "
                 "must stay a legal state, or the validator becomes a gate that "
                 "excludes an honest line"),
        "defects": defects,
        "controls": controls,
        "counts": {
            "defects_planted": planted,
            "defects_caught_by_the_named_check": caught,
            "controls": len(controls),
            "controls_undisturbed": undisturbed,
        },
        "ok": caught == planted and undisturbed == len(controls),
    }
    out = ROOT / "data" / "gate-logs" / "results-profiles-drill.json"
    out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps({"counts": log["counts"], "ok": log["ok"]},
                     indent=2, ensure_ascii=False))
    for name, d in defects.items():
        if not (d["refused"] and d["named_check"]):
            print("  SURVIVED:", name, d)
    for name, c in controls.items():
        if not c["undisturbed"]:
            print("  DISTURBED:", name, c)
    print(f"wrote {out}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
