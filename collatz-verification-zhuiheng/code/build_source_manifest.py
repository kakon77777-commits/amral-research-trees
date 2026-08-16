"""Chronological manifest of Neo.K's Collatz source folder.

數學戰士「墜衡」 / AMRAL Research Lab.

Neo.K's instruction (2026-08-14): all new material lands in one folder, and it is
to be unpacked **one at a time, in chronological order**, deciding for each item
whether it is new or continues something earlier.

Sixty-four items is more than can be tracked in prose, and "which have I already
done" is exactly the sort of thing that goes wrong silently. So the manifest is
generated, not maintained by hand: it reads the folder, hashes every file, sorts
by modification time, classifies each item by its name, and marks what the
verification tree has already processed.

It **reads only**. It does not extract anything. Unpacking is a separate,
deliberate step, one item at a time.

Usage:  python code/build_source_manifest.py [--source PATH]
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import zipfile

DEFAULT_SOURCE = r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"
ROOT = pathlib.Path(__file__).resolve().parent.parent

# What this tree has already independently rechecked, and where.
PROCESSED = {
    "Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0.zip": (
        "archived as ../collatz-ot-series-neok/ and fully rechecked; "
        "see reports/RUN-002-OT-SERIES.md"
    ),
    "collatz_operation_translation_finite_verification_prototype.zip": (
        "item 03. archived byte-exact at "
        "../collatz-ot-series-neok/early-experiments/; all 58651 certificate rows "
        "rechecked by code/src03_finite_prototype_recheck.py, scaling cross-checked "
        "against the Rust engine"
    ),
    "Collatz_OT_Series_Paper_01_v0.1_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_02_v0.2_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_03_v0.3_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_04_v0.4_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_05_v0.5_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_06_v0.6_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_07_v0.7_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_Papers_01_08_v0.8_bundle.zip": (
        "the draft chain; rechecked for provenance by code/src05_provenance_chain_recheck.py — "
        "strictly additive, and byte-identical to the SSSP provenance/original text"
    ),
    "Collatz_OT_Series_INDEX_v0.1.md": (
        "loose series index beside the bundles; confirmed byte-identical to the "
        "bundled copy by code/src05_provenance_chain_recheck.py"
    ),
    "Collatz_OT_Series_Paper_01_Reclassification_and_Calibration_v0.1.md": (
        "loose Paper 01 beside the bundles; confirmed byte-identical to the "
        "bundled copy by code/src05_provenance_chain_recheck.py"
    ),
    "Collatz_OT_Series_Paper_02_Local_Affine_Atlas_Finite_Word_v0.1.md": (
        "loose Paper 02 beside the bundles; confirmed byte-identical to the "
        "bundled copy by code/src05_provenance_chain_recheck.py"
    ),
    "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1_bundle.zip": (
        "item 17, the Hard-Zeta origin. Rechecked by "
        "code/src06_hardzeta_origin_recheck.py: Z_k(s) measured on [2, 2^32) with "
        "two-sided bounds, the L = 1 uniform route refuted, and the ROUTE MAP's "
        "missing monotonicity hypothesis reported; see reports/RUN-004-HARD-ZETA-ORIGIN.md"
    ),
    "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1.1.md": (
        "item 18. Rechecked with item 17: byte-identical to the SSSP package's "
        "archived HZ original, and the v0.1 -> v0.1.1 -> v0.1.2 chain counted — "
        "v0.1.1 fixed one of the two unrestricted unions, the E_k^C one survived"
    ),
    "Hard_Zeta_Phase_I_Round_01_Exact_Refinement_v0.1.md": (
        "item 19. Rechecked by code/src07_hardzeta_round01_recheck.py against "
        "direct iteration: the child recursion, recursive hard height, four-way "
        "refinement identity, exact mass conservation, trichotomy, zero-loss zone, "
        "the per-chart No-Go construction and the U^k closed form all hold; "
        "see reports/RUN-005-HARD-ZETA-ROUND-01.md"
    ),
    "Hard_Zeta_Phase_I_Round_01_bundle.zip": (
        "item 20. Rechecked with item 19; the bundled Round 01 is byte-identical "
        "to the loose copy, and the exact Z_k(s) from this chart algebra lands "
        "inside RUN-004's independently measured bracket at all 22 depths"
    ),
    "Hard_Zeta_Phase_I_Round_02_Atomic_Hazard_Coefficient_Correction_v0.1.md": (
        "item 21. Rechecked by code/src08_hardzeta_round02_recheck.py: the "
        "quotient-coordinate thresholds, beta_k zones and parity-restricted sums "
        "all agree with Round 01; the mass-weighted hazard is the right object by "
        "up to 94x; Terras's RCOT reformulation holds on all 81,119 first-crossing "
        "words to length 24; see reports/RUN-006-HARD-ZETA-ROUND-02.md"
    ),
    "Hard_Zeta_ROUTE_MAP_v0.2.md": (
        "item 22. Rechecked with item 21. Unlike v0.1's map this one states the "
        "C/R split rather than the general weighted bridge, so RUN-004's finding "
        "about the missing monotonicity hypothesis does not carry over"
    ),
    "Hard_Zeta_Phase_I_Round_02_bundle.zip": (
        "item 23. Rechecked with items 21-22; both loose files are byte-identical "
        "to the bundled copies, and the bundle also carries Round 01"
    ),
    "Hard_Zeta_Phase_I_Round_03A_bundle.zip": (
        "item 24. Rechecked by code/src09_hardzeta_round03a_recheck.py: the "
        "irrational ballot tree, survivor DP, Beatty event schedule, exact "
        "Hurwitz-zeta mass, anchor ejection, event-loss operator and Head-Tail "
        "Reduction all hold. Headline: the minimum surviving anchor m_k measured "
        "from 23 tau_c records on [2, 2^32), giving rigorous upper bounds on the "
        "true C_k(s); see reports/RUN-007-HARD-ZETA-ROUND-03A.md"
    ),
    "Hard_Zeta_Phase_I_Round_03A1_bundle.zip": (
        "item 25. Rechecked by code/src10_hardzeta_round03a1_recheck.py against "
        "direct iteration: the accelerated exact code, affine endpoint formula, "
        "source congruence, nested lift digits, monotonicity, residue-rate gap, "
        "mechanical code and both §30-§31 counterexamples all hold. §34's table "
        "reproduced exactly and extended from m=8 to m=60; a_m shown to be the "
        "same anchor sequence RUN-007 measured for m_k, switching at k = K_m; "
        "see reports/RUN-008-HARD-ZETA-ROUND-03A1.md"
    ),
    "Hard_Zeta_Phase_I_Round_03A2_bundle.zip": (
        "item 26. Rechecked by code/src11_hardzeta_round03a2_recheck.py: the exact "
        "2-3 bridge, Q_m positivity, coarse/exact split, synchronization bit and "
        "§12's three equivalent bits all hold; §30's finite diagnostic reproduces "
        "to the digit; §22's redundancy boundary confirmed on all three anchors. "
        "Finding: §24's endpoint-parity route is equivalent to CST, not cheaper - "
        "the longest odd-M runs are held by the ANCHORED codes; "
        "see reports/RUN-009-HARD-ZETA-ROUND-03A2.md"
    ),
    "Hard_Zeta_Phase_I_Round_03A3_bundle.zip": (
        "item 27. Rechecked by code/src12_hardzeta_round03a3_recheck.py over 13,929 "
        "node/exponent pairs: the endpoint 2-adic state, bit-selection theorem, "
        "cut-and-shift recurrence, Unique Zero-Lift Edge and Spine Ejection "
        "Criterion all hold, and no node ever had two source-preserving children. "
        "§13's parity-only example reproduces to the digit. Measured: spine length "
        "= the canonical source's own subcritical lifetime minus node depth; "
        "see reports/RUN-010-HARD-ZETA-ROUND-03A3.md"
    ),
    "Hard_Zeta_Phase_II_Round_AU2b3_bundle.zip": (
        "item 36. Rechecked by code/src20_hardzeta_au2b3_recheck.py. THE SUBJECT "
        "CORRECTED A DEFECT THIS ARM REPRODUCED FAITHFULLY AND DID NOT NOTICE: "
        "A-U.2b.2's queue DP counted POINTED paths where its own section 4 "
        "defined an UNPOINTED word set (66 vs 48 at r=4,D=2). RUN-017 verified "
        "the program against a brute force written from the program's reading, "
        "so both shared the misreading. Everything here is implemented from the "
        "PROSE definitions instead, and Q = P_D - P_(D-1) is checked against a "
        "direct enumeration of WORDS. Cost to RUN-017: the label, not the "
        "conclusion — the rate shifts by at most 1.5e-3, and 1.4e-4 at r=5000, "
        "so first-order saturation stands and the second-order barrier never "
        "used the DP at all. All nine diagnostic rows reproduce with worst "
        "deviation exactly 0. Measured: the pointing ratio P/Q settles at 1.638, "
        "which is why the correction cannot move the exponential rate. The "
        "packing branch is declared closed. "
        "See reports/RUN-018-HARD-ZETA-AU2B3-PREFACTOR-SATURATION.md"
    ),
    "Hard_Zeta_Phase_II_Round_AU2e_bundle.zip": (
        "item 37. Rechecked by code/src21_hardzeta_au2e_recheck.py. Every exact "
        "identity holds: the deviation identity d_m - d_(m-1) = a_m - q_m, the "
        "directional split U - W = d_N with U counting skipped credits exactly, "
        "the Reset Affine Identity cleared to INTEGERS at 1554 windows with no "
        "floating point, and the deficit-drop slope identity. THE ROUND'S TWO "
        "INEQUALITIES TURN OUT TO BE ONE LINE: the contamination bound is "
        "informative only when J_N < (N-2r)/r, which is exactly the packing "
        "theorem's floor — verified row by row with 0 disagreements. Every "
        "computable spine sits on the vacuous side of it: J_N/N runs 0.55-0.69 "
        "while the floor is 0.08-1.50, so the barrier pins only 3.1%-6.7% of the "
        "mismatches present and CANNOT FAIL at these sizes; the drill says so "
        "instead of implying coverage. By contrast the reset geometry does bind "
        "— across 190 first-return windows Y_b reaches 0.203-0.938 of its cap — "
        "but its affine correction is never what makes the bound true (0 windows "
        "need it; it moves the worst case by 4.6e-4). "
        "See reports/RUN-019-HARD-ZETA-AU2E-MULTISCALE-RETURN.md"
    ),
    "NeoK_Crypto_Semiotics_Theory_Compiler_v0.8.zip": (
        "item 38. THE SWEEP LEAVES HARD-ZETA HERE — a different subject, so the "
        "instruments changed. Verified in a separate tree: "
        "../neok-crypto-semiotics-verification/, RUN-020. Every countable figure "
        "reproduces (264 claims / 2490 obligations / 608 evidence gaps / 714 "
        "dependency edges), their three pytest suites reproduce CROSS-PLATFORM "
        "(18 passed on Windows against their Linux capture), and the CTCL trust "
        "model re-derives from its own TLA+ at 10 states with 0 cloud-only "
        "secrecy violations. TWO THINGS DO NOT, both artifacts never re-run "
        "against the layer after them: (1) the shipped "
        "PersistentSecurityRuntime.tla pins authorized and verificationOK TRUE "
        "with no action changing them, so it reaches 16 states and Rollback is "
        "UNREACHABLE against the reported 62 — adding the two environment "
        "actions their Python takes reproduces 62 exactly with both safety "
        "properties intact, so the gap is coverage not correctness; (2) exactly "
        "1 profile of 264 is rejected by the shipped JSON Schema (CL-N21-005, "
        "promotion_decision 'ready_at_target'), and it is the SAME claim that is "
        "the only exception to the prose gate rule. Also: readiness_score is the "
        "v0.8 report's headline metric and cannot be re-derived from the package "
        "at all. Payload NOT mirrored (23.9 MiB); source sha256 recorded. "
        "See ../neok-crypto-semiotics-verification/reports/RUN-020-CRYPTO-SEMIOTICS-V08.md"
    ),
    "Hard_Zeta_Phase_II_Round_AU2b2_bundle.zip": (
        "item 35. Rechecked by code/src19_hardzeta_au2b2_recheck.py. Pulls the "
        "FIRST of A-U.2b.1's five levers (queue entropy) and it returns ZERO at "
        "first order — that is the round's own Prefix-Constraint No-Gain "
        "theorem, and the queue rate climbs monotonically to within 0.00246 of "
        "beta at r=5000. The second-order gain came from the Stirling prefactor "
        "instead, which was not on the list; four levers remain untried. Their "
        "queue DP was checked by REIMPLEMENTATION (opposite accumulation "
        "direction, exact integer credits, validated against brute force first) "
        "and all nine rows reproduce. Constants agree to 80-82 digits, and the "
        "block-scale optimum sits exactly at s=0 with d_pack — third round "
        "running published at its own supremum. FINDING: the shipped JSON was "
        "NOT produced by the shipped script (9 rows vs 8, renamed fields), "
        "though every number in it is correct — a stale generator/output "
        "pairing, a realization defect with the mathematics intact. "
        "See reports/RUN-017-HARD-ZETA-AU2B2-QUEUE-ENTROPY.md"
    ),
    "Hard_Zeta_Phase_II_Round_AU2b1_bundle.zip": (
        "item 34. Rechecked by code/src18_hardzeta_au2b1_recheck.py. The FIRST "
        "round to ship its own numerical artifact (a script + an 80-digit "
        "constants JSON), so it is checked as one: the constants are recomputed "
        "from scratch by decimal bisection against the subject's mpmath "
        "findroot, and agree to 80-83 digits — every digit published. "
        "c_pack = 0.03585676003404867, which is 2.388x the ceiling RUN-015 "
        "measured for the PREVIOUS round's scheme; the new argument is "
        "multi-occurrence packing, exactly the kind of change RUN-015 said would "
        "be needed. Also verified: both entropy identities, the variational "
        "supremum, and §27's optimality as TWO exhibited failures rather than an "
        "assertion. This round publishes AT its supremum where the previous "
        "published 67% of its own. "
        "See reports/RUN-016-HARD-ZETA-AU2B1-PACKING-THRESHOLD.md"
    ),
    "Hard_Zeta_Phase_II_Round_AU2b_bundle.zip": (
        "item 33. Rechecked by code/src17_hardzeta_au2b_recheck.py. The FIRST "
        "positive round of Phase II — it eliminates classes instead of blocking "
        "routes, and it settles what RUN-014 left open: the mechanical code is "
        "unanchored because d_m = 0 identically, a different argument from the "
        "lift-flux one. The whole result turns on Lambda_gamma = "
        "2.83951373049775... < 3, verified at 60 digits, and on two explicit "
        "inequalities at c=0.645 that clear by 1.0e-4 and 6.0e-4. Also verified: "
        "return separation, the complexity-peak law, the excursion bound, the "
        "Sturmian complexity p(r)=r+1, and negative sources for periodic tails. "
        "Measured: the same proof scheme supports eps ~ 0.0150, not just the "
        "published 0.01 — a 50% gain with no new idea, which is what "
        "A-U.2b.1 asks for. "
        "See reports/RUN-015-HARD-ZETA-AU2B-SPARSE-LIFT-RIGIDITY.md"
    ),
    "Hard_Zeta_Phase_II_Round_AU2a_bundle.zip": (
        "item 32. Rechecked by code/src16_hardzeta_au2a_recheck.py. Almost all "
        "exact algebra and all of it holds: the inverse-code series and its "
        "functional equation, the Source Block-Digit Theorem (the lift IS a "
        "binary block of the source), the amplification law Etilde-E = 2t*3^m, "
        "the X/Z/C recurrences, the Decoupling (C is identical for every source "
        "in a cylinder), the synchronization bound, the flux balance, and both "
        "rival completions (the negative one reaches -1 on exact rationals). "
        "Measured: the A-U.1 countermodel has POSITIVE lift flux (lambda-bar "
        "~0.34 stable to M=400), so it sits in the class the Zero-Flux Boundary "
        "Theorem already excludes — it is not a witness for the sparse class "
        "A-U.2b must handle. See reports/RUN-014-HARD-ZETA-AU2A-LIFT-COUPLING.md"
    ),
    "Hard_Zeta_Phase_II_Round_AU1_bundle.zip": (
        "item 31. Rechecked by code/src15_hardzeta_au1_recheck.py. A NEGATIVE "
        "round and it holds: the Critical Invariant-Limit Theorem's finite "
        "arithmetic checks out, and both countermodels behind the Pure "
        "Occupation No-Go are verified exactly — the Bernoulli measure's mean is "
        "1+p, and the mechanical code telescopes to floor(beta m), stays in "
        "{1,2}, is subcritical at every prefix to m=300, and its 2-density "
        "reaches gamma to 8.8e-5 by m=8000. Its formula agrees with the "
        "implementation RUN-008 wrote from Round 03-A.1. Measured: the anchor "
        "cocycle separates them — every genuine integer's lift digits settle by "
        "m=11, while the mechanical code still lifts at m=59 and its source "
        "grows 13 to 93 bits. See reports/RUN-013-HARD-ZETA-AU1-ANCHOR-ERASURE.md"
    ),
    "Hard_Zeta_B_Line_Handoff_v0.1.md": (
        "item 29. Rechecked by "
        "code/src14_hardzeta_bline_aline_closure_recheck.py. Its integer slack "
        "Lambda(w) = Delta_w nu(w) - b_w holds on all 81,119 first-crossing "
        "words to length 24, and reproduces RUN-006's 19/39 at UUUDUUDD by a "
        "different formula. Measured: sup R(w) is attained at LENGTH 8 "
        "(251/507), and no length 10-24 comes within a factor of ten; section "
        "11's warning that b-extremal is not slack-extremal has 41 witnesses. "
        "See reports/RUN-012-HARD-ZETA-A-LINE-CLOSURE.md"
    ),
    "Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip": (
        "item 30. Rechecked by the same tool. The closure is correctly scoped: "
        "'A line reduction program complete', explicitly NOT a proof of Terras "
        "or Collatz, with CASP left open. Its one external dependency "
        "(Lopez-Stoll, arXiv:2101.12747) was fetched and the claimed liminf "
        "equality appears verbatim in that abstract; archived at "
        "data/external/. Measured: section 5's witness 2^(m+1)-1 is up to 5e9 "
        "times larger than the cheapest start with the same subcritical reach "
        "(n=27), and spines die having spent 93-98% of the Sturmian budget, so "
        "sections 19-20's near-saturation is the normal end state. "
        "See reports/RUN-012-HARD-ZETA-A-LINE-CLOSURE.md"
    ),
    "Hard_Zeta_Phase_I_Round_03A4_bundle.zip": (
        "item 28. Rechecked by code/src13_hardzeta_round03a4_recheck.py: the "
        "deficit queue, Sturmian credit ledger, valuation cylinders and occupancy "
        "bound, the excursion identity (in exact integers), the logarithmic and "
        "bounded-deficit brackets, and the Legendre gate all hold; beta's "
        "continued fraction anchored against 19/12 and 84/53. Measured: the gate "
        "opens on 2 of 168 depths, so CF tools reach almost none of the spine; "
        "see reports/RUN-011-HARD-ZETA-ROUND-03A4.md"
    ),
    "collatz_ot_v3_threshold_benchmark.csv": (
        "archived byte-exact at ../collatz-ot-series-neok/early-experiments/; "
        "all 15 (k, domain) rows rechecked by code/src04_v3_threshold_recheck.py, "
        "each cross-checked against the Rust engine; prune ratios confirmed to be "
        "Paper 05's P_k = A_k/2^k, and the non-monotonicity in k reproduced from "
        "the closed form"
    ),
    "collatz_operation_translation_v3_threshold_bundle.zip": (
        "archived byte-exact at ../collatz-ot-series-neok/early-experiments/; "
        "rechecked with the benchmark by code/src04_v3_threshold_recheck.py"
    ),
    "dimension_aware_log_physics_stress_bundle.zip": (
        "item 02. archived byte-exact at "
        "../collatz-ot-series-neok/early-experiments/; rechecked by "
        "code/src02_log_physics_recheck.py. Not a Collatz item."
    ),
    "finite_collatz_additive_coordinate_mvp_bundle.zip": (
        "item 01. archived byte-exact at "
        "../collatz-ot-series-neok/early-experiments/; rechecked by "
        "code/src01_additive_coordinate_recheck.py"
    ),
}


def classify(name: str) -> dict:
    """Sort an item into the research line it belongs to, from its name alone."""
    n = name.lower()
    if "sssp_repaired" in n:
        return {"line": "nine-paper series", "role": "final repaired package"}
    if re.search(r"papers?_01[_-]0\d_v0\.\d_bundle", n) or "paper_01_v0.1_bundle" in n:
        return {"line": "nine-paper series", "role": "incremental bundle, superseded by SSSP v1.0"}
    if re.match(r"collatz_ot_series_paper_0\d", n) or "collatz_ot_series_index" in n:
        return {"line": "nine-paper series", "role": "loose manuscript or index"}
    if "faithful_global_quantifier_compression" in n:
        return {"line": "Hard-Zeta", "role": "proof-route origin"}
    if "hard_zeta_route_map" in n:
        return {"line": "Hard-Zeta", "role": "route map"}
    if "hard_zeta" in n and "handoff" in n:
        return {"line": "Hard-Zeta", "role": "handoff"}
    if "hard_zeta" in n and "a_line_complete" in n:
        return {"line": "Hard-Zeta", "role": "Phase I A-line consolidation"}
    if "hard_zeta_phase_i_" in n:
        return {"line": "Hard-Zeta", "role": "Phase I round"}
    if "hard_zeta_phase_ii_" in n:
        return {"line": "Hard-Zeta", "role": "Phase II round"}
    if "crypto_semiotics" in n:
        return {"line": "other project", "role": "not Collatz; parked here"}
    if "collatz_ot_series_paper.zip" == n:
        return {"line": "nine-paper series", "role": "large consolidated archive"}
    if any(t in n for t in ("mvp_bundle", "stress_bundle", "prototype", "threshold")):
        return {"line": "early experiments", "role": "prototype / benchmark"}
    return {"line": "unclassified", "role": "needs a look"}


def round_key(name: str):
    """Sort key for Hard-Zeta rounds, so AU2d2 lands before AU2d10."""
    m = re.search(r"round_([a-z]*)(\d+)([a-z]*)(\d*)", name.lower())
    if not m:
        return None
    a, b, c, d = m.groups()
    return (a, int(b), c, int(d) if d else -1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    args = ap.parse_args()
    src = pathlib.Path(args.source)
    if not src.is_dir():
        raise SystemExit(f"source folder not found: {src}")

    items = []
    for p in sorted((q for q in src.rglob("*") if q.is_file()),
                    key=lambda q: q.stat().st_mtime):
        st = p.stat()
        raw = p.read_bytes()
        entry = {
            "name": p.relative_to(src).as_posix(),
            "mtime_local": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(
                timespec="seconds"),
            "bytes": st.st_size,
            "sha256": hashlib.sha256(raw).hexdigest(),
            **classify(p.name),
            "processed_by_this_tree": PROCESSED.get(p.name),
        }
        rk = round_key(p.name)
        if rk:
            entry["round_sort_key"] = list(rk)
        if p.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(p) as z:
                    infos = [i for i in z.infolist() if not i.is_dir()]
                    entry["zip_entries"] = len(infos)
                    entry["zip_uncompressed_bytes"] = sum(i.file_size for i in infos)
                    entry["zip_top_level"] = sorted({i.filename.split("/")[0] for i in infos})[:6]
            except zipfile.BadZipFile:
                entry["zip_entries"] = "UNREADABLE"
        items.append(entry)

    lines: dict[str, int] = {}
    for it in items:
        lines[it["line"]] = lines.get(it["line"], 0) + 1

    manifest = {
        "tool": "build_source_manifest.py",
        "source_folder": str(src),
        "generated_from": "file modification times and names; nothing was extracted",
        "item_count": len(items),
        "total_bytes": sum(i["bytes"] for i in items),
        "earliest": items[0]["mtime_local"] if items else None,
        "latest": items[-1]["mtime_local"] if items else None,
        "items_per_line": lines,
        "processed_count": sum(1 for i in items if i["processed_by_this_tree"]),
        "items": items,
    }
    out = ROOT / "data" / "source-manifest.v1.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"{len(items)} items, {manifest['total_bytes']/2**20:.1f} MiB, "
          f"{manifest['earliest']} .. {manifest['latest']}")
    for line, count in sorted(lines.items(), key=lambda kv: -kv[1]):
        print(f"  {count:3d}  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
