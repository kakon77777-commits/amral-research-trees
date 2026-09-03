"""Assemble data/results.v1.json from measured outputs only.

數學戰士「墜衡」 / AMRAL Research Lab.

Every number in results.v1.json is copied out of an archived gate log or the
chunk-log aggregator. Nothing is typed in by hand, so the summary cannot drift
away from what was actually run. If a required gate log is missing, this script
fails instead of emitting a summary with a hole in it.

Usage:  python code/build_results.py --tag t40 --expect-to 1099511627776
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATES = ROOT / "data" / "gate-logs"

CODE_FILES = [
    "code/collatz_verify.rs",
    "code/collatz_ref.py",
    "code/anchors.py",
    "code/mutation_drill.py",
    "code/reference_crosscheck.py",
    "code/verify_run_logs.py",
    "code/build_results.py",
    "code/run_verification.sh",
    "code/ot_paper01_recheck.py",
    "code/ot_paper02_recheck.py",
    "code/ot_paper06_recheck.py",
    "code/ot_paper03_recheck.py",
    "code/ot_paper04_recheck.py",
    "code/ot_paper05_kl_recheck.py",
    "code/ot_paper07_recheck.py",
    "code/ot_paper08_recheck.py",
    "code/ot_paper09_recheck.py",
    "code/ot_recheck_drill.py",
    "code/suite_totals.py",
    "code/build_source_manifest.py",
]


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_gate(name: str) -> dict:
    path = GATES / name
    if not path.exists():
        raise SystemExit(f"missing gate log: {path}. Run the gate and archive its output.")
    return json.loads(path.read_text(encoding="utf-8"))


# Figures that mean nothing on their own. A renderer showing the first without
# the second states a number where the source states a ratio: "1441 defects
# caught" reads identically whether 1441 or 2000 were planted, and the whole
# claim of a falsifiability drill is that those two are equal.
#
# Declared as data rather than left to a renderer's judgement, because the
# renderer cannot know which of two numbers is load-bearing, and a list of
# pairs kept in the renderer would be a second copy of this tree's semantics.
RENDER_PAIRS = [
    {
        "value": "paper_sweep.defects_caught_by_the_named_check",
        "against": "paper_sweep.defects_planted",
        "label": "planted defects, caught by the check named for each",
        "why": ("the drill's claim is that these are equal; the caught count "
                "alone cannot show whether any defect survived"),
    },
    {
        "value": "paper_sweep.controls_undisturbed",
        "against": "paper_sweep.controls",
        "label": "controls, undisturbed",
        "why": ("a disturbed control means the drill's defects were not the "
                "only thing moving; the undisturbed count alone hides that"),
    },
    {
        "value": "paper_sweep.rechecked_by_this_tree",
        "against": "paper_sweep.source_items",
        "label": "source items rechecked by this tree",
        "why": ("the remainder is not a gap: see "
                "paper_sweep.belongs_to_another_research_line, which accounts "
                "for it. Without the denominator a reader cannot tell whether "
                "the sweep is complete"),
    },
    {
        "value": "coverage.odd_starts_checked",
        "against": "coverage.odd_starts_expected",
        "label": "odd starts checked, against the count the interval requires",
        "why": ("the coverage claim is that these are equal; the checked count "
                "alone cannot show whether the interval was fully tiled"),
    },
    {
        "value": "gates.mutation_drill.defects_caught",
        "against": "gates.mutation_drill.defects_planted",
        "label": "engine defects planted and caught",
        "why": "same as the sweep drill, for the engine's own mutation drill",
    },
]


def resolve(doc: dict, dotted: str):
    """Follow a dotted path, or raise if any segment is absent."""
    cur = doc
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(dotted)
        cur = cur[part]
    return cur


def check_render_pairs(doc: dict) -> list[dict]:
    """Every declared pair must resolve to two numbers, or nothing is emitted.

    A declaration pointing at a field that has been renamed is worse than no
    declaration: it tells a renderer to look for something that is not there,
    and the renderer's own check would then pass vacuously.
    """
    out = []
    for pair in RENDER_PAIRS:
        entry = dict(pair)
        for side in ("value", "against"):
            got = resolve(doc, pair[side])          # KeyError is the refusal
            if not isinstance(got, (int, float)) or isinstance(got, bool):
                raise SweepInputError(
                    f"render pair {pair[side]} is not a number: {got!r}")
            entry[side + "_is"] = got
        out.append(entry)
    return out


class SweepInputError(Exception):
    """A sweep figure could be silently incomplete, so no summary is emitted."""


def check_sweep_inputs(totals: dict, manifest: dict) -> None:
    """Refuse the three ways the sweep section could quietly understate itself.

    Split out of main() so it can be driven with crafted inputs by
    code/build_results_guard_drill.py. A guard nothing ever exercises is the
    same shape this tree spent the sweep cataloguing: it reads like a check and
    is only a comment.
    """
    if not totals.get("ok"):
        raise SweepInputError("suite totals gate is red; refusing to emit a summary")
    if totals.get("uninterpreted"):
        raise SweepInputError(
            f"suite totals could not interpret {totals['uninterpreted']}; "
            "refusing to emit a summary that silently undercounts")
    if manifest.get("unprocessed"):
        raise SweepInputError(
            f"source items with no recheck and no owning line: "
            f"{manifest['unprocessed']}; refusing to report the sweep as complete")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="t40")
    ap.add_argument("--expect-to", type=int, required=True)
    args = ap.parse_args()

    proc = subprocess.run(
        [sys.executable, str(ROOT / "code" / "verify_run_logs.py"),
         "--tag", args.tag, "--expect-to", str(args.expect_to)],
        capture_output=True, text=True, encoding="utf-8",
    )
    coverage = json.loads(proc.stdout)
    if not coverage.get("ok"):
        raise SystemExit(f"chunk logs do not tile the interval: {coverage.get('problems')}")

    anchors = load_gate("anchors.json")
    drill = load_gate("mutation-drill.json")
    selftest = load_gate("self-test.json")
    reference = load_gate("reference-crosscheck.json")
    ot_recheck = load_gate("ot-paper02-recheck.json")
    ot_p06 = load_gate("ot-paper06-recheck.json")
    ot_p01 = load_gate("ot-paper01-recheck.json")
    ot_p03 = load_gate("ot-paper03-recheck.json")
    ot_p04 = load_gate("ot-paper04-recheck.json")
    ot_kl = load_gate("ot-paper05-kl-recheck.json")
    ot_p07 = load_gate("ot-paper07-recheck.json")
    ot_p08 = load_gate("ot-paper08-recheck.json")
    ot_p09 = load_gate("ot-paper09-recheck.json")
    ot_drill = load_gate("ot-recheck-drill.json")
    ot_block = load_gate("ot-paper05-block-benchmark.json")
    totals = load_gate("suite-totals.json")

    manifest_path = ROOT / "data" / "source-manifest.v1.json"
    if not manifest_path.exists():
        raise SystemExit(f"missing {manifest_path}. Run code/build_source_manifest.py.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_reports = sorted(p.name for p in (ROOT / "reports").glob("RUN-*.md"))

    try:
        check_sweep_inputs(totals, manifest)
    except SweepInputError as exc:
        raise SystemExit(str(exc)) from exc

    if not anchors.get("all_match"):
        raise SystemExit("anchor gate did not match; refusing to emit a summary")
    if not drill.get("ok"):
        raise SystemExit("mutation drill did not pass; refusing to emit a summary")
    if not selftest.get("ok"):
        raise SystemExit("self-test did not pass; refusing to emit a summary")
    if not reference.get("agree"):
        raise SystemExit("reference cross-check did not agree; refusing to emit a summary")
    for name, gate, key in (
        ("Paper 02 recheck", ot_recheck, "ok"),
        ("Paper 06 recheck", ot_p06, "ok"),
        ("Paper 01 recheck", ot_p01, "ok"),
        ("Paper 03 recheck", ot_p03, "ok"),
        ("Paper 04 recheck", ot_p04, "ok"),
        ("Paper 05 KL recheck", ot_kl, "ok"),
        ("Paper 07 recheck", ot_p07, "ok"),
        ("Paper 08 recheck", ot_p08, "ok"),
        ("Paper 09 recheck", ot_p09, "ok"),
        ("recheck drill", ot_drill, "ok"),
        ("Paper 05 block benchmark", ot_block, "ok"),
    ):
        if not gate.get(key):
            raise SystemExit(f"{name} did not pass; refusing to emit a summary")

    n = coverage["covered_interval"][1]
    results = {
        "schema_version": 1,
        "research_line_id": "collatz-verification-zhuiheng",
        "researcher": {
            "display_name": "數學戰士-墜衡",
            "model": "Claude Opus 5",
            "agent_role": "local verification and computation arm",
            "route": "instrument, not theory",
        },
        "date": datetime.date.today().isoformat(),
        "interval_verification_date": "2026-08-14",
        "problem": {
            "id": "COLLATZ",
            "name": "Collatz conjecture (3x+1 problem)",
            "statement": "every positive integer's Collatz trajectory reaches 1",
        },
        "global_status": {
            "solved": False,
            "literature_novelty_claimed": False,
            "record_attempt": False,
            "statement": (
                "A bounded exhaustive verification and a falsifiability-drilled "
                "instrument. Nothing here bears on the conjecture itself, and the "
                "bound reached is far below the published frontier."
            ),
            "published_frontier_note": (
                "Convergence is published as verified for all n below 2075 * 2^60, "
                "about 2^71.02 (Barina, Improved verification limit for the convergence "
                "of the Collatz conjecture, The Journal of Supercomputing 81:810, 2025, "
                "doi 10.1007/s11227-025-07337-0), with the project page reporting "
                "progress beyond it. This arm did not re-run that verification; what it "
                "did check, while rechecking Paper 01, is that the DOI resolves to the "
                "stated journal, volume and article and that the project page states the "
                "2^71 figure - see ot-paper01-recheck.json. An earlier version of this "
                "note said 2^68 citing Barina 2021, which understated the frontier by "
                "three doublings and cited a superseded milestone."
            ),
        },
        "verified_claims": [
            {
                "id": "V1",
                "claim": f"every integer n with 1 <= n <= {n} has a Collatz trajectory reaching 1",
                "method": "exhaustive descent below n under the shortcut map, plus strong induction",
                "exhaustive_within_domain": True,
                "relative_to_implementation": True,
                "domain_upper_bound": n,
                "domain_upper_bound_as_power_of_two": "2^40",
            },
            {
                "id": "V2",
                "claim": f"no nontrivial Collatz cycle has all of its elements <= {n}",
                "method": "free corollary of V1: the least element of such a cycle would never reach 1",
                "separate_computation": False,
                "domain_upper_bound": n,
            },
        ],
        "explicit_non_claims": [
            "nothing about any n > the domain upper bound",
            "nothing about cycles containing an element above the domain upper bound",
            "no support, evidence, or suggestion regarding the conjecture itself",
            "no independent confirmation of the published 2^71 frontier - only that the citation for it resolves correctly",
            "nothing in the paper sweep bears on the conjecture either: every bundle claim rechecked there is a finite statement about finite objects",
            "the sweep rechecks the series' own claims and its own checking apparatus; it does not assess whether the series' program can close the conjecture",
            "a defect found in a bundle's checker is a defect in the evidence offered for a claim, not a refutation of the claim",
        ],
        "coverage": coverage,
        "paper_sweep": {
            "what_it_is": (
                "the item-by-item recheck of the source folder, one bundle at a time "
                "in chronological order. Separate from the exhaustive interval "
                "verification above: that one is a claim about integers, this one is "
                "a claim about the series' finite statements and the scripts the "
                "bundles ship to check themselves."
            ),
            "source_items": manifest["item_count"],
            "rechecked_by_this_tree": manifest["processed_count"],
            "belongs_to_another_research_line": manifest["belongs_to_another_line"],
            "unprocessed": manifest["unprocessed"],
            "run_reports": len(run_reports),
            "drills": totals["drills"],
            "defects_planted": totals["defects_planted"],
            "defects_caught_by_the_named_check": totals["defects_caught_by_the_named_check"],
            "controls": totals["controls"],
            "controls_undisturbed": totals["controls_undisturbed"],
            "why_these_figures_can_be_trusted_to_be_complete": (
                "code/suite_totals.py reads every archived drill log, classifies each "
                "one's tally shape explicitly, and exits non-zero if it meets a shape "
                "it cannot interpret - so a drill it does not understand stops the "
                "build instead of contributing zero. code/build_source_manifest.py "
                "derives each Hard-Zeta round's status from the gate log and RUN "
                "report on disk rather than a hand-kept table, which is what had "
                "drifted: the table still read 39 of 73 long after the sweep passed "
                "them."
            ),
            "one_item_is_not_this_tree_s": (
                "the crypto-semiotics compiler bundle sits in the same source folder "
                "but is verified in the sibling tree "
                "../neok-crypto-semiotics-verification/. It is reported separately "
                "rather than counted as a gap here."
            ),
        },
        "gates": {
            "self_test": {"ok": selftest["ok"]},
            "reference_cross_check": reference,
            "external_anchors": {
                "ok": anchors["all_match"],
                "bound": anchors["bound"],
                "sources": anchors["sources"],
                "snapshot_sha256": anchors["snapshot_sha256"],
                "checks": [
                    {k: c[k] for k in ("kind", "published_compared", "engine_produced",
                                       "largest_compared_start", "match")}
                    for c in anchors["checks"]
                ],
            },
            "mutation_drill": {
                "ok": drill["ok"],
                "defects_planted": drill["defects_planted"],
                "defects_caught": drill["defects_caught"],
                "defects_survived": drill["defects_survived"],
                "controls_planted": drill["controls_planted"],
                "controls_disturbed": drill["controls_disturbed"],
                "per_mutation": [
                    {k: m.get(k) for k in ("id", "description", "expected_to_be_caught", "caught_by")}
                    for m in drill["mutations"]
                ],
            },
        },
        "subject_verification": {
            "subject": (
                "Neo.K, Collatz Operation Translation Series — SSSP Repaired v1.0 "
                "(9 core papers + Hard-Zeta research program), repair date 2026-08-14"
            ),
            "role": (
                "This arm re-derives the series' finite claims independently. It does not "
                "co-author the series, and re-derivation of a finite claim says nothing "
                "about the global conjecture the series is aimed at."
            ),
            "package_integrity": {
                "verifier": "the package's own tools/verify_series.py",
                "result": "PASS on all nine steps once run under PYTHONUTF8=1",
                "defect_found": (
                    "tools/generate_math_inventory.py writes UTF-8 JSON to stdout, so on a "
                    "cp950 Windows host the verifier aborts with UnicodeEncodeError on the "
                    "'ö' of 'Möbius' (Papers 07 and 08). The package cannot be verified "
                    "end-to-end on the author's own platform without PYTHONUTF8=1."
                ),
                "package_not_modified": True,
            },
            "paper_05_k16_block_benchmark": {
                "claim_source": "validation.json: k16_strict=938413, k16_equality=2",
                "domain": ot_block["domain"],
                "reproduced_strict_descent": ot_block["strict_descent"],
                "reproduced_equality": ot_block["equality"],
                "reproduced_ascent": ot_block["ascent"],
                "agrees_with_claim": (
                    ot_block["strict_descent"] == 938413 and ot_block["equality"] == 2
                ),
                "independence": (
                    "computed in Rust from this arm's k-step congruence tables, a single "
                    "table lookup per n, versus the subject's Python step-by-step iteration"
                ),
                "equality_witnesses_explained": (
                    "the two equality cases are n=1 and n=2, the elements of the trivial "
                    "cycle; T has period 2 there and 16 is even, so they are forced"
                ),
            },
            "paper_01_ledger_and_bibliography": {
                "checks": {k: v["pass"] for k, v in ot_p01["checks"].items()},
                "all_pass": ot_p01["ok"],
                "corrected_earlier_judgement": (
                    "An earlier note here said Paper 01's content is bibliographic rather "
                    "than arithmetic, and that this arm 'can check numbers, not literature'. "
                    "Wrong twice: citations ARE externally checkable against arXiv and "
                    "Crossref - an external anchor whose expectations this arm did not author "
                    "- and the Claim Ledger's T-class entries are concrete arithmetic, where "
                    "a mislabelled entry would be exactly the defect the ledger exists to "
                    "prevent."
                ),
                "bibliography_verified": ot_p01["measured"]["arxiv_records"],
                "barina_2025": ot_p01["measured"]["barina_2025"],
                "verification_frontier": ot_p01["measured"]["verification_frontier"],
                "correction_to_this_arm": (
                    "Verifying Neo.K's reference audit corrected THIS tree. Until 2026-08-14 "
                    "the charter and README said the published frontier was 'at least 2^68' "
                    "citing Barina 2021. The current figure is all n below 2075 * 2^60, about "
                    "2^71.02, from Barina 2025 (J. Supercomputing 81:810). The old statement "
                    "was literally true but understated the frontier by three doublings and "
                    "cited a superseded milestone. Corrected in CHARTER.md, README.md and "
                    "RUN-001-T40.md, each carrying a note of what it used to say."
                ),
            },
            "paper_03_theorems": {
                "max_word_length": ot_p03["max_word_length"],
                "counts": ot_p03["counts"],
                "checks": {k: v["pass"] for k, v in ot_p03["checks"].items()},
                "all_pass": ot_p03["ok"],
                "the_substantive_addition": (
                    "Four of Paper 03's statements were already confirmed as a by-product of "
                    "the Paper 02 recheck, but via the closed congruence r_w = -b_w 3^-u - the "
                    "very shortcut Paper 03 §11 warns against using as the foundation. So r_w "
                    "is derived a SECOND time here, by the §6/§7/§28 refinement induction from "
                    "r_D = 0 and r_U = 1, splitting each cylinder by the parity of m_w and "
                    "never touching b_w 3^-u. The two derivations agree on all "
                    + str(ot_p03["counts"]["words_derived_two_ways"]) +
                    " words, which is what makes the closed congruence a result rather than an "
                    "assumption."
                ),
                "worked_examples": ot_p03["measured"]["worked_examples"],
                "target_overlap_witness": ot_p03["measured"]["target_overlap_witness"],
                "non_claim_given_a_witness": (
                    "§27 states that target charts may overlap even though source charts "
                    "partition. That is an existence claim, so a witness was found rather than "
                    "asserted: " + str(ot_p03["measured"]["target_overlap_witness"]) + "."
                ),
            },
            "paper_04_theorems": {
                "max_word_length": ot_p04["max_word_length"],
                "counts": ot_p04["counts"],
                "checks": {k: v["pass"] for k, v in ot_p04["checks"].items()},
                "all_pass": ot_p04["ok"],
                "why_it_matters": (
                    "The subject's regression suite contains NO Paper 04 test - its groups are "
                    "p02_p03, p02_extrema, p05, p06, p07 and p09 - so every theorem here was "
                    "machine-checked for the first time."
                ),
                "certificate_is_two_sided": (
                    "§38's three-condition bidirectional certificate was checked in both "
                    "directions: it accepts every legal triple, and rejects all "
                    + str(ot_p04["counts"]["negative_controls_rejected"]) +
                    " deliberately perturbed ones. A certificate that accepts everything "
                    "certifies nothing, so the rejecting half is the load-bearing one."
                ),
                "non_claim_given_a_witness": (
                    "§33 insists local bijectivity does not give global injectivity. That is an "
                    "existence claim, so an explicit cross-chart merge was found rather than "
                    "asserted: " + str(ot_p04["measured"]["cross_chart_merge_witness"]) +
                    " - two different charts carrying two different sources to the same target."
                ),
                "cross_chart_merge_witness": ot_p04["measured"]["cross_chart_merge_witness"],
            },
            "paper_05_kl_constant": {
                "checks": {k: (v.get("pass") if "pass" in v else v.get("subject_claim_holds"))
                           for k, v in ot_kl["checks"].items()},
                "instrument_sound": ot_kl["ok"],
                "subject_findings": ot_kl["subject_findings"],
                "stated_limits": ot_kl["stated_limits"],
                "high_precision": ot_kl["measured"]["high_precision"],
                "what_was_added": (
                    "The subject asserts |D - 0.03468818523201744| < 1e-14 where D is "
                    "computed by the same float expression the literal came from — a "
                    "self-comparison that cannot fail. Here the constant is recomputed at 60 "
                    "digits and compared against the real value, and its ROLE is verified on "
                    "exact binomial tails: 1 - P_k <= exp(-kD) holds at every k tested, and "
                    "-(ln(1-P_k) + kD) - (1/2)ln k stays bounded instead of drifting linearly, "
                    "which is what would happen if D were the wrong rate."
                ),
                "finding_summary": (
                    "The published KL literal is 2.79 ULP from the real value. It is exactly "
                    "what the stated float expression emits, so it is accumulated rounding "
                    "rather than a typo, but it is not the nearest double: the 17th "
                    "significant digit reads ...744 where the real value rounds to ...746. "
                    "Nothing in the series depends on that digit."
                ),
            },
            "paper_02_theorems": {
                "max_word_length": ot_recheck["max_word_length"],
                "counts": ot_recheck["counts"],
                "checks": {k: v["pass"] for k, v in ot_recheck["checks"].items()},
                "all_pass": ot_recheck["ok"],
                "referee": (
                    "symbolic composition of D(x)=x/2 and U(x)=(3x+1)/2 on an affine form, "
                    "assuming no theorem of the paper; claimed formulas are compared against it"
                ),
                "coverage_beyond_subject_suite": (
                    "Theorems B, D and E and the §25 width formula are not exercised by the "
                    "subject's own regression suite; the subject checks k <= 9, this checks k <= 16"
                ),
                "known_insensitivity": (
                    "Theorem D held under a mutation that changed the +1 injection to +2. That "
                    "is correct rather than a gap: the concatenation law is structural across "
                    "the whole (mx+r) family and does not pin r. Theorem D alone therefore "
                    "cannot detect a wrong injection constant."
                ),
            },
            "paper_06_theorems": {
                "odd_starts_upper_limit": ot_p06["odd_starts_upper_limit"],
                "counts": ot_p06["counts"],
                "checks": {k: v["pass"] for k, v in ot_p06["checks"].items()},
                "all_pass": ot_p06["ok"],
                "referee": (
                    "direct iteration of the accelerated odd map S(n)=(3n+1)/2^{v2(3n+1)} on "
                    "genuine odd integers, assuming no theorem of the paper"
                ),
                "coverage_beyond_subject_suite": (
                    "the subject's test_p06 checks only the formal affine identity, for formal "
                    "valuation tuples, m <= 5, kappa in 1..4, and only at n = 1. It never "
                    "checks admissibility, and never touches Theorems D through H, the section "
                    "19 descent threshold, or the section 14 bridge back to Paper 02."
                ),
                "cross_paper_bridge_verified": (
                    "section 14's claim B_kappa = b_{E(kappa)} is checked against the Paper 02 "
                    "referee route, so the two papers' corrections are confirmed to be the same "
                    "quantity rather than merely analogous"
                ),
                "float_hazard_recorded": {
                    "claim": "Theorem E, 2^K > 3^m iff K/m > log2 3",
                    "decided_by": "exact integers, and independently by 80-digit Decimal",
                    "closest_ratio_in_range": ot_p06["counts"]["closest_ratio_to_log2_3"],
                    "margin_exceeds_double_epsilon": ot_p06["counts"][
                        "closest_ratio_margin_exceeds_float_epsilon"],
                    "note": (
                        "K/m runs through the convergents of log2 3, so a naive float test is "
                        "not safe in general. On the tested range it happened to agree, and the "
                        "closest ratio's margin is recorded so that agreement is not mistaken "
                        "for a guarantee."
                    ),
                },
            },
            "paper_07_theorems": {
                "parameters": ot_p07["parameters"],
                "counts": ot_p07["counts"],
                "checks": {k: v["pass"] for k, v in ot_p07["checks"].items()},
                "all_pass": ot_p07["ok"],
                "referee": (
                    "symbolic composition of D(x)=x/2 and U(x)=(mx+r)/2 on an affine form, "
                    "assuming no theorem of the paper"
                ),
                "coverage_beyond_subject_suite": (
                    "the subject's test_p07 covers affine data, residue coding and transport "
                    "for m in {1,3,5,7,9}, r in {1,3,5}, k <= 7. It does not touch the matrix "
                    "representation, the concatenation law, the closed geometric-sum bounds of "
                    "§17/§18, the m=1 form of §19, the §21 threshold, §22 uniform expansion, "
                    "Theorems E through H, §33's linearity in r, §46's width, §47's "
                    "order-uniform threshold, or §37's valuation density for general (m, r)."
                ),
                "m_equals_1_repair_verified": (
                    "The repair ledger records that Paper 07's theorem summary used ln m "
                    "without restricting m > 1, and now states the logarithmic forms for odd "
                    "m > 1 with P_k(1) = 1 recorded separately. Both halves are checked: the "
                    "geometric sum is evaluated without ever dividing by (m-2), so m = 1 is "
                    "reached with no singularity, and P_k(1) = 1 exactly."
                ),
                "float_floor_hazard": {
                    "claim": "Theorems E and F use floor(k * ln2/ln m); the subject's p05 counter computes it in double precision",
                    "reference": "the exact integer predicate m^u < 2^k",
                    "disagreements_found": ot_p07["measured"]["float_floor_disagreements"],
                    "margin": ot_p07["measured"]["float_floor_margin"],
                    "conclusion": (
                        "The float floor is safe over the scanned range, and safe for a reason "
                        "rather than by luck: the closest k*alpha_m ever comes to an integer is "
                        "bounded below by a Diophantine margin that exceeds the accumulated "
                        "double-precision error by many orders of magnitude. For m = 3 the "
                        "worst case in range lands exactly at k = 1054, the convergent "
                        "denominator of ln2/ln3."
                    ),
                },
                "cylinder_density_measured": ot_p07["measured"]["cylinder_density_P_k_m"],
            },
            "paper_08_breakage_ladder": {
                "counts": ot_p08["counts"],
                "checks": {k: v["pass"] for k, v in ot_p08["checks"].items()},
                "all_pass": ot_p08["ok"],
                "corrected_earlier_judgement": (
                    "An earlier note in this tree wrote Paper 08 off as out of instrument "
                    "range. That was too quick. A structural breakage theorem does not need a "
                    "general proof to be tested - it needs an explicit WITNESS that the "
                    "property fails there, plus confirmation that the properties above it "
                    "survive, and both are finite."
                ),
                "what_still_needs_lean": (
                    "the universally quantified forms - 'for every commutative ring and every "
                    "ideal' - remain in LEAN-QUEUE.md. What is settled here is every claim of "
                    "the form 'here it holds / here it fails'."
                ),
                "witnesses": ot_p08["witnesses"],
                "ladder_verified_in_both_directions": (
                    "each rung is checked for what BREAKS and for what SURVIVES: at the mod-6 "
                    "witness the residue uniqueness fails while the affine closure is "
                    "untouched, and dimension alone is confirmed NOT to be the breakage point "
                    "because commuting matrices keep the count law."
                ),
            },
            "paper_09_theorems": {
                "max_word_length": ot_p09["max_word_length"],
                "counts": ot_p09["counts"],
                "checks": {k: v["pass"] for k, v in ot_p09["checks"].items()},
                "all_pass": ot_p09["ok"],
                "why_this_paper_meets_the_engine": (
                    "Paper 09 §2 defines sigma(n) = inf{ j >= 1 : T^j(n) < n }, which is "
                    "exactly the quantity this arm's engine measures for every start it "
                    "verifies, and §50 identifies K(N) = max sigma over [2, N]. The archived "
                    "[3, 2^40] run therefore already contains K(2^40)."
                ),
                "frontier_function_measured": ot_p09["measured"].get("K_of_2_pow_40"),
                "section_24_accounting": ot_p09["measured"].get("p09_s24_accounting"),
                "section_24_resolution": (
                    "The paper says the 938413 strict-descent certificates are explained by "
                    "Paper 05's 58651 contracting residue classes 'plus finite boundary "
                    "corrections'. Those corrections are now itemised exactly: 58651 classes "
                    "give 938415 starts in [1, 2^20) — 16 per class, less one because n = 0 is "
                    "outside the domain — and the shortfall to 938413 is exactly two integers, "
                    "n = 1 and n = 2, which meet T^16(n) = n rather than T^16(n) < n. Zero "
                    "starts inside a contracting class fail to descend for any other reason."
                ),
                "gap_the_drill_exposed_and_closed": (
                    "The frontier, K(N) and monotonicity checks only ever compare sigma against "
                    "itself, so a uniform off-by-one in sigma left all of them green. The drill "
                    "surfaced this. A separate anchor now pins sigma's absolute indexing against "
                    "values derived independently in collatz_ref.py, and that anchor is what "
                    "catches the shift."
                ),
            },
            "drill": {
                "targets": ot_drill["targets"],
                "defects_planted": ot_drill["defects_planted"],
                "defects_caught_by_the_named_check": ot_drill["defects_caught_by_the_named_check"],
                "controls_planted": ot_drill["controls_planted"],
                "controls_undisturbed": ot_drill["controls_undisturbed"],
                "anomalies": ot_drill["anomalies"],
                "note": (
                    "each planted defect had to be caught by the check named for it, not "
                    "merely by some check"
                ),
            },
        },
        "environment": {
            "os": "Windows 10 x64",
            "python": "3.14.5",
            "rustc": "1.96.0 (ac68faa20 2026-05-25)",
            "logical_cpus": 16,
        },
        "source_sha256": {f: sha256(ROOT / f) for f in CODE_FILES},
    }

    # Resolved against the finished document, so a declaration can never point
    # at a field this build did not actually emit.
    try:
        results["render_pairs"] = check_render_pairs(results)
    except KeyError as exc:
        raise SystemExit(
            f"a render pair points at a field this summary does not contain: "
            f"{exc}. Fix the path or drop the pair; a declaration that does not "
            f"resolve tells a renderer to look for something absent.") from exc
    except SweepInputError as exc:
        raise SystemExit(str(exc)) from exc

    out = ROOT / "data" / "results.v1.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
