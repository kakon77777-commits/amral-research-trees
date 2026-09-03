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
PAIRS = "results-pairs/1"
FIGURES = "results-figures/1"


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

    # D9-D12 - results-pairs/1. A declaration that does not resolve is worse
    # than no declaration: it tells a renderer to look for something absent,
    # and the renderer's own check then passes vacuously.
    def paired(doc: dict) -> dict:
        doc["render_pairs"] = [{
            "value": "counts.caught", "against": "counts.planted",
            "label": "planted and caught", "why": "the claim is that they are equal",
        }]
        doc["counts"] = {"caught": 10, "planted": 10}
        return doc

    def plant_pair(name: str, why: str, mutate, needle: str):
        doc = paired(good_doc())
        mutate(doc)
        res = V.evaluate(doc)
        missing = res["gaps"].get(PAIRS, [])
        defects[name] = {
            "why": why,
            "refused": PAIRS not in res["satisfies"],
            "named_check": any(needle in m for m in missing),
            "reported": missing,
        }

    plant_pair("D9_a_pair_pointing_at_a_field_that_is_not_there",
               "a renamed field must break the declaration loudly, not silently",
               lambda d: d["render_pairs"][0].__setitem__("against", "counts.gone"),
               "does not resolve")

    plant_pair("D10_a_pair_pointing_at_something_that_is_not_a_number",
               "a boolean denominator renders as a ratio against true",
               lambda d: d["counts"].__setitem__("planted", True),
               "is not a number")

    plant_pair("D11_a_pair_with_no_stated_reason",
               "a pair nobody can review is a rule nobody can challenge",
               lambda d: d["render_pairs"][0].pop("why"),
               "needs a why")

    plant_pair("D12_render_pairs_present_but_empty",
               "an empty array must not read as 'pairs declared'",
               lambda d: d.__setitem__("render_pairs", []),
               "non-empty array")

    # D13-D16 - results-figures/1. The load-bearing rule is the last one: a
    # figure that belongs to a pair and is ALSO offered standalone reintroduces
    # the bare-numerator defect through the mechanism built to prevent it.
    def figured(doc: dict) -> dict:
        doc = paired(doc)
        doc["counts"]["runs"] = 52
        doc["headline_figures"] = [{"path": "counts.runs", "label": "run reports"}]
        return doc

    def plant_fig(name: str, why: str, mutate, needle: str):
        doc = figured(good_doc())
        mutate(doc)
        res = V.evaluate(doc)
        missing = res["gaps"].get(FIGURES, [])
        defects[name] = {
            "why": why,
            "refused": FIGURES not in res["satisfies"],
            "named_check": any(needle in m for m in missing),
            "reported": missing,
        }

    plant_fig("D13_a_figure_pointing_at_a_field_that_is_not_there",
              "a renamed field must break the declaration, not render blank",
              lambda d: d["headline_figures"][0].__setitem__("path", "counts.gone"),
              "does not resolve")

    plant_fig("D14_a_figure_with_no_label",
              "a bare number under no heading is not a figure",
              lambda d: d["headline_figures"][0].pop("label"),
              "needs a label")

    plant_fig("D15_a_figure_that_is_also_half_of_a_pair",
              "offering a paired value standalone is the bare-numerator defect "
              "reintroduced by the mechanism meant to prevent it",
              lambda d: d["headline_figures"][0].__setitem__("path", "counts.caught"),
              "also part of a render pair")

    plant_fig("D16_headline_figures_present_but_empty",
              "an empty array must not read as 'figures declared'",
              lambda d: d.__setitem__("headline_figures", []),
              "non-empty array")

    # D17-D19 - the `kind` discriminator. A range declared as a number would
    # render as "[3, 1099511627776]"; a number declared as a range would render
    # as nothing at all. Both are silent, so the declared kind is checked
    # against what actually resolves rather than trusted.
    plant_fig("D17_a_range_declared_as_a_number",
              "an interval shown through a number renderer is not a figure",
              lambda d: (d["counts"].__setitem__("span", [3, 40]),
                         d["headline_figures"][0].update(path="counts.span")),
              "declared a number and is not")

    plant_fig("D18_a_number_declared_as_a_range",
              "a renderer told to draw two ends will find one and draw neither",
              lambda d: d["headline_figures"][0].update(kind="range"),
              "must resolve to exactly two numbers")

    plant_fig("D19_an_unknown_kind",
              "a renderer must never be asked to guess how to draw something",
              lambda d: d["headline_figures"][0].update(kind="sparkline"),
              "unknown kind")

    # D20-D21 - the archive guard. This one is not hypothetical either: an
    # ad-hoc `--paths` run twice replaced the cross-branch measurement with a
    # one-file one, and the second time the file was under a temp directory, so
    # the archived gate log briefly cited a scratchpad path as this tree's
    # evidence. Neither run reported anything wrong, because nothing was: the
    # measurement was accurate about the file it was handed.
    from_git = [{"ref": "origin/agent/x", "path": "x/data/results.v1.json"}]

    msg = V.why_not_archivable(from_git, True)
    defects["D20_an_ad_hoc_paths_run_must_not_archive"] = {
        "why": "an ad-hoc query and the archived measurement are different artifacts",
        "refused": msg is not None,
        "named_check": bool(msg and "--paths" in msg),
        "reported": msg,
    }

    msg = V.why_not_archivable(
        [{"ref": None, "path": "C:/tmp/scratch/results.v1.json"}], False)
    defects["D21_a_file_not_read_from_a_git_ref_must_not_archive"] = {
        "why": ("the archived log must cite what a consumer cloning this "
                "repository receives, never a path on one machine"),
        "refused": msg is not None,
        "named_check": bool(msg and "not read from a git ref" in msg),
        "reported": msg,
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
            "the file a renderer will actually read must satisfy all four, or "
            "it loses the protection this tree asked for",
            real, [ENVELOPE, CLAIMS, PAIRS, FIGURES])

    pairs_no_figs = paired(good_doc())
    control("C6_declaring_pairs_without_figures_is_a_legal_state",
            "a line may protect its ratios without nominating headlines; the "
            "profiles are independent, not a ladder",
            pairs_no_figs, [ENVELOPE, CLAIMS, PAIRS])

    envelope_only = good_doc()
    envelope_only.pop("verified_claims")
    envelope_only.pop("explicit_non_claims")
    control("C4_envelope_only_is_a_valid_state_not_a_failure",
            "a line outside results-claims/1 is a rendering branch, not a defect",
            envelope_only, [ENVELOPE])

    from_git = [{"ref": "origin/agent/x", "path": "x/data/results.v1.json"}]
    ok_msg = V.why_not_archivable(from_git, False)
    controls["C7_a_full_cross_branch_scan_must_archive"] = {
        "why": ("the guard must not become a refusal that never lets the "
                "canonical measurement be written at all"),
        "undisturbed": ok_msg is None,
        "message": ok_msg,
    }

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
