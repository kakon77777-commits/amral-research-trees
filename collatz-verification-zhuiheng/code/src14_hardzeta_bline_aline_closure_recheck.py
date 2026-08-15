"""Recheck of source items 29 and 30 — the B-line handoff and the A-line closure.

數學戰士「墜衡」 / AMRAL Research Lab.

Item 29 hands the correction-delay frontier off to a separate line, restating
Round 02's first-crossing test as an exact integer slack. Item 30 closes the
coefficient line: Round 03-A.5 plus `A_Line_Closure_v1.0` plus route map v0.8.

The closure is a claim about *scope*, not a theorem, so it is checked as one:
what it says is settled must be settled, what it says is open must still be
open, and it must not claim more than that. Its one external dependency — a
López–Stoll preprint — is checked against an archived record of the source
rather than taken on the citation's word.

Everything decidable is decided in exact integers or Fractions.

Usage:  python code/src14_hardzeta_bline_aline_closure_recheck.py
Env:    HZ_SOURCE_DIR, HZ_ALGEBRA_MODULE, HZ_ACCEL_MODULE, HZ_EXTERNAL_DIR
"""

from __future__ import annotations

import hashlib
import importlib
import io
import json
import math
import os
import pathlib
import sys
import zipfile
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))
EXTERNAL = pathlib.Path(os.environ.get("HZ_EXTERNAL_DIR", str(ROOT / "data" / "external")))

C = importlib.import_module(os.environ.get("HZ_ALGEBRA_MODULE", "hz_chart_algebra"))
A = importlib.import_module(os.environ.get("HZ_ACCEL_MODULE", "hz_accel_code"))

HANDOFF = "Hard_Zeta_B_Line_Handoff_v0.1.md"
BUNDLE = "Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip"
A5 = "Hard_Zeta_Phase_I_Round_03A5_Exceptional_Occupancy_Rigidity_v0.1.md"
CLOSURE = "Hard_Zeta_A_Line_Closure_v1.0.md"
ROUTEMAP = "Hard_Zeta_ROUTE_MAP_v0.8_A_CLOSED.md"

WORD_LEN = 24                 # RUN-006's enumeration depth, reused deliberately
SPINES = [27, 103, 703, 1407, 10087, 15039, 35655]

# The closure's own list of completed reductions (§35), each tied to the report
# in this tree that rechecked it. A reduction the closure claims but no report
# covers is a gap in this arm's coverage, not a defect in the closure.
REDUCTION_TO_REPORT = {
    "local affine atlas": "RUN-005-HARD-ZETA-ROUND-01.md",
    "coefficient/correction split": "RUN-006-HARD-ZETA-ROUND-02.md",
    "Hard-Zeta atomic globalizer": "RUN-005-HARD-ZETA-ROUND-01.md",
    "Beatty coefficient events": "RUN-007-HARD-ZETA-ROUND-03A.md",
    "source-anchor head reduction": "RUN-007-HARD-ZETA-ROUND-03A.md",
    "exact exponent-code lifts": "RUN-008-HARD-ZETA-ROUND-03A1.md",
    "2–3 synchronization": "RUN-009-HARD-ZETA-ROUND-03A2.md",
    "unique zero-lift spine": "RUN-010-HARD-ZETA-ROUND-03A3.md",
    "valuation deficit queue": "RUN-011-HARD-ZETA-ROUND-03A4.md",
    "exact excursion identity": "RUN-011-HARD-ZETA-ROUND-03A4.md",
    "finite-local no-go": "RUN-012-HARD-ZETA-A-LINE-CLOSURE.md",
    "critical saturation reduction": "RUN-012-HARD-ZETA-A-LINE-CLOSURE.md",
    "occupancy/tail dichotomy": "RUN-012-HARD-ZETA-A-LINE-CLOSURE.md",
}


def read_sources() -> dict[str, str]:
    out = {HANDOFF: (SOURCE / HANDOFF).read_text(encoding="utf-8")}
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        names = {pathlib.PurePosixPath(n).name: n for n in z.namelist()}
        for want in (A5, CLOSURE, ROUTEMAP):
            if want in names:
                out[want] = z.read(names[want]).decode("utf-8")
    return out


def T(x: int) -> int:
    return (3 * x + 1) // 2 if x % 2 else x // 2


def main() -> int:
    rep = {
        "tool": "src14_hardzeta_bline_aline_closure_recheck.py",
        "subject": "Hard_Zeta_B_Line_Handoff_v0.1.md (item 29) and "
                   "Hard_Zeta_A_Line_COMPLETE_Rounds_01_03A5_v1.0.zip (item 30)",
        "source_items": [29, 30],
        "scope": "the correction-delay handoff's slack algebra, Round 03-A.5's "
                 "finite-local no-go and occupancy dichotomy, and whether the "
                 "A-line closure claims exactly what it has",
        "checks": {}, "counts": {}, "measured": {}, "failures": [],
    }
    checks, measured = rep["checks"], rep["measured"]

    def check(name, fn, note=""):
        try:
            ok, detail = fn()
        except Exception as exc:                      # one broken check must not
            ok, detail = False, f"{type(exc).__name__}: {exc}"   # hide the others
        checks[name] = {"pass": bool(ok), "detail": detail, "note": note}

    docs = read_sources()
    handoff, a5 = docs.get(HANDOFF, ""), docs.get(A5, "")
    closure, routemap = docs.get(CLOSURE, ""), docs.get(ROUTEMAP, "")

    # ---------------------------------------------------------------- item 29
    fc = C.first_crossing_words(WORD_LEN)
    measured["first_crossing_words_enumerated"] = len(fc)

    def prefixes_expanding():
        bad = 0
        for w in fc[:4000]:
            x = C.ROOT
            for ch in w.word[:-1]:
                d, u = C.children(x)
                x = u if ch == "U" else d
                if 3 ** x.u <= 2 ** x.k:
                    bad += 1
            if 3 ** w.u >= 2 ** w.k:
                bad += 1
        return bad == 0, {"words_walked": min(len(fc), 4000), "violations": bad}

    check("SRC14_first_crossing_prefixes_are_uniformly_expanding", prefixes_expanding,
          "§3: every proper prefix expands, the word itself contracts")

    def no_early_descent():
        # §3's consequence, by direct iteration rather than by the word algebra.
        bad, tested = 0, 0
        for w in fc:
            if w.k > 14:
                continue
            n = C.nu(w)
            x = n
            for _ in range(w.k - 1):
                x = T(x)
                tested += 1
                if x <= n:
                    bad += 1
            if T(x) >= n:
                bad += 1
        return bad == 0 and tested > 0, {"steps_checked": tested, "violations": bad}

    check("SRC14_no_member_of_a_first_crossing_cylinder_descends_early", no_early_descent,
          "§3: T^j(n) > n for every j < |w|, checked by iterating T")

    def trichotomy():
        # Both branches must appear, so the equivalence is not graded on a set
        # where one side is constantly true. Contracting words that are *not*
        # first-crossing supply the delay branch.
        pos = neg = zero = 0
        bad = []
        stack, seen = [C.ROOT], 0
        while stack and seen < 60000:
            w = stack.pop()
            seen += 1
            if w.k and C.delta_of(w.k, w.u) > 0:
                lam = C.correction_slack(w)
                n = C.nu(w)
                descends = w.F(n) < n
                if (lam > 0) != descends:
                    bad.append(w.word)
                if lam > 0:
                    pos += 1
                elif lam == 0:
                    zero += 1
                else:
                    neg += 1
            if w.k < 14:
                stack.extend(C.children(w))
        return (not bad and pos > 0 and neg > 0), {
            "immediate_descent": pos, "boundary": zero, "correction_delay": neg,
            "mismatches": bad[:5],
            "_both_outcomes_seen": pos > 0 and neg > 0}

    check("SRC14_the_slack_trichotomy_is_exactly_descent_on_the_least_member", trichotomy,
          "§4: Lambda(w) > 0 iff F_w(nu) < nu; both branches required to appear")

    def ratio_matches_slack():
        bad = []
        for w in fc:
            r = C.normalized_correction_ratio(w)
            lam = C.correction_slack(w)
            if (r < 1) != (lam > 0) or (r == 1) != (lam == 0):
                bad.append(w.word)
        return not bad, {"words": len(fc), "mismatches": bad[:5]}

    check("SRC14_the_ratio_and_the_integer_slack_classify_identically", ratio_matches_slack,
          "§12 vs §13: R(w) < 1 exactly when Lambda(w) > 0")

    def terras_integer_form():
        lams = [(C.correction_slack(w), w.word) for w in fc]
        lo = min(lams)
        measured["min_correction_slack"] = {"value": lo[0], "word": lo[1] or "(root)"}
        return lo[0] >= 1, {"minimum": lo[0], "at": lo[1], "words": len(lams)}

    check("SRC14_terras_equality_holds_as_an_integer_lower_bound_on_every_word",
          terras_integer_form, "§13: Terras equality on W_fc is exactly Lambda >= 1")

    def reproduces_run006():
        # RUN-006 measured max c_w/nu(w) = 19/39 at UUUDUUDD by Round 02's route.
        # The handoff's coordinates must land on the same word and value.
        best = max(fc, key=lambda w: Fraction(w.b // C.delta_of(w.k, w.u), C.nu(w)))
        got = Fraction(best.b // C.delta_of(best.k, best.u), C.nu(best))
        return (best.word == "UUUDUUDD" and got == Fraction(19, 39)), {
            "argmax": best.word, "c_over_nu": str(got),
            "run_006_recorded": "19/39 at UUUDUUDD"}

    check("SRC14_the_slack_form_reproduces_run_006s_measured_binding_ratio",
          reproduces_run006, "cross-run: two formulas, one word, one value")

    def b_extremals():
        bad = []
        for k in range(2, 13):
            for u in range(1, k):
                if 3 ** u >= 2 ** k:
                    continue
                e = C.b_extremals(k, u)
                fam = C.words_of_shape(k, u)
                if not fam:
                    continue
                lo, hi = min(fam, key=lambda w: w.b), max(fam, key=lambda w: w.b)
                if (e["b_min"] != e["b_min_closed"] or e["b_max"] != e["b_max_closed"]
                        or lo.b != e["b_min"] or hi.b != e["b_max"]):
                    bad.append((k, u))
        return not bad, {"shapes_checked": "k=2..12", "mismatches": bad[:5]}

    check("SRC14_b_extremals_match_their_closed_forms", b_extremals,
          "§11: min at U^u D^{k-u} = 3^u - 2^u, max at D^{k-u} U^u = 2^{k-u}(3^u - 2^u), "
          "confronted with a full enumeration of each shape")

    def b_extremal_is_not_slack_extremal():
        # §11's warning, and No-Go 2: a witness shape where the slack minimiser is
        # neither of the two b-extremal words.
        wit = []
        for k in range(4, 13):
            for u in range(1, k):
                if 3 ** u >= 2 ** k:
                    continue
                fam = C.words_of_shape(k, u)
                if len(fam) < 3:
                    continue
                lo = min(fam, key=lambda w: w.b).word
                hi = max(fam, key=lambda w: w.b).word
                s = min(fam, key=C.correction_slack).word
                if s not in (lo, hi):
                    wit.append({"k": k, "u": u, "b_min_word": lo,
                                "b_max_word": hi, "slack_min_word": s})
        measured["shapes_where_b_extremal_is_not_slack_extremal"] = len(wit)
        return bool(wit), {"witnesses": len(wit), "first": wit[:3]}

    check("SRC14_b_extremal_is_not_slack_extremal", b_extremal_is_not_slack_extremal,
          "§11 and No-Go 2: needs a witness, so it fails if the warning is empty")

    check("SRC14_the_handoff_states_its_own_no_gos",
          lambda: (handoff.count("No-Go") >= 5 and "Average drift" in handoff,
                   {"no_go_mentions": handoff.count("No-Go")}),
          "§24: five named method no-gos")

    check("SRC14_the_handoff_lists_what_must_not_be_reasked",
          lambda: ("不應再重問的問題" in handoff and "已完成" in handoff,
                   {"present": "不應再重問的問題" in handoff}),
          "§31: the settled list the next line must not restart from")

    # ---------------------------------------------------------------- item 30
    def lifts_realize_the_code():
        bad, tested = [], 0
        for kappa in [(1,), (1, 1, 1), (2, 1, 3), (1, 2, 1, 4), (3, 1, 1, 2, 1)]:
            for n in A.code_lifts(kappa, 12):
                tested += 1
                if A.accel_code(n, len(kappa)) != kappa:
                    bad.append((kappa, n))
        return (not bad and tested > 0), {"lifts_tested": tested, "mismatches": bad[:5]}

    check("SRC14_every_finite_code_is_realized_by_infinitely_many_positive_integers",
          lifts_realize_the_code,
          "§2: n = r_m + t 2^{K_m+1} realizes the same code for every t >= 0")

    def all_one_family():
        bad = []
        for m in range(1, 41):
            kappa = (1,) * m
            if (A.offset(kappa) != A.all_ones_offset(m)
                    or A.source_residue(kappa) != A.all_ones_source(m)
                    or A.accel_code(A.all_ones_source(m), m) != kappa):
                bad.append(m)
        return not bad, {"m_range": "1..40", "mismatches": bad[:5]}

    check("SRC14_the_all_one_family_has_the_claimed_source_and_offset", all_one_family,
          "§4: B_m = 3^m - 2^m and r_m = 2^{m+1} - 1, and 2^{m+1}-1 really runs it")

    check("SRC14_the_all_one_code_is_subcritical_at_every_prefix",
          lambda: (all(A.is_subcritical((1,) * m) for m in range(1, 61)),
                   {"m_range": "1..60"}),
          "§4: K_j = j < j log2 3 for every prefix")

    def zero_occupancy():
        bad = []
        for m in range(1, 41):
            if A.occupancy_count(A.all_ones_source(m), m, 2) != 0:
                bad.append(m)
        return not bad, {"m_range": "1..40", "nonzero_at": bad[:5]}

    check("SRC14_arbitrarily_long_zero_occupancy_prefixes_exist", zero_occupancy,
          "§5: N_{>=2}(m) = 0 for n = 2^{m+1} - 1, at every m")

    def mod_four():
        hi = lo = 0
        bad = []
        for y in range(1, 40000, 2):
            q = (3 * y + 1) & -(3 * y + 1)
            q = q.bit_length() - 1
            want = (y % 4 == 1)
            if want != (q >= 2):
                bad.append(y)
            hi += want
            lo += not want
        return (not bad and hi > 0 and lo > 0), {
            "odd_y_tested": 20000, "mismatches": bad[:5],
            "q_at_least_2": hi, "q_equals_1": lo, "_both_outcomes_seen": hi > 0 and lo > 0}

    check("SRC14_high_valuation_is_exactly_the_one_mod_four_class", mod_four,
          "§10: Y = 1 mod 4 iff v2(3Y+1) >= 2; both outcomes required")

    def endpoint_u_count():
        bad, tested = [], 0
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            m_top = min(life, 30)
            K = A.cumulative(A.accel_code(n, m_top))
            word = A.shortcut_parity(n, K[-1] + 4)
            for m in range(1, m_top + 1):
                tested += 1
                # cumulative() returns [K_0=0, K_1, ..., K_m], so K_m is K[m].
                if A.u_count(word, K[m]) != m:
                    bad.append((n, m))
        return (not bad and tested > 0), {"pairs": tested, "mismatches": bad[:5]}

    check("SRC14_the_accelerated_endpoint_carries_exactly_m_up_steps", endpoint_u_count,
          "§12: h(K_m) = m, with the parity word generated by iterating T directly")

    def block_minimum():
        # §13: within a block the ratio h/l falls only after the U, so the block's
        # local minimum is at its end. Checked on the real parity words.
        bad, tested = [], 0
        for n in SPINES:
            m_top = min(A.subcritical_lifetime(n), 30)
            K = A.cumulative(A.accel_code(n, m_top))
            word = A.shortcut_parity(n, K[-1] + 2)
            for m in range(1, m_top + 1):
                end, start = K[m], K[m - 1]
                here = Fraction(A.u_count(word, end), end)
                for ell in range(start + 1, end):
                    tested += 1
                    if Fraction(A.u_count(word, ell), ell) < here:
                        bad.append((n, m, ell))
        return (not bad and tested > 0), {"interior_points": tested,
                                          "below_the_block_end": bad[:5]}

    check("SRC14_the_parity_ratio_bottoms_out_at_block_ends", block_minimum,
          "§13: liminf over l equals liminf over m because each block's minimum is "
          "at its end")

    def deficit_gap():
        bad = []
        for n in SPINES:
            for m in range(1, min(A.subcritical_lifetime(n), 40) + 1):
                K = A.cumulative(A.accel_code(n, m))[-1]
                d = A.deficit(n, m)
                # delta_m - d_m = frac(m log2 3), which lies in [0, 1) exactly when
                # 2^{K+d} <= 3^m < 2^{K+d+1}.
                if not (2 ** (K + d) <= 3 ** m < 2 ** (K + d + 1)):
                    bad.append((n, m))
        return not bad, {"mismatches": bad[:5]}

    check("SRC14_the_real_and_integer_deficits_differ_by_less_than_one", deficit_gap,
          "§16: |delta_m - d_m| < 1, decided by exact integer bracketing")

    def indicator_sum():
        bad, tested = [], 0
        for n in SPINES:
            for q in A.orbit_valuations(n, min(A.subcritical_lifetime(n), 40)):
                tested += 1
                if sum(1 for r in range(2, q + 2) if q >= r) != q - 1:
                    bad.append(q)
        return (not bad and tested > 0), {"valuations": tested, "mismatches": bad[:5]}

    check("SRC14_cylinder_indicators_sum_to_the_excess", indicator_sum,
          "§21: q - 1 = sum over r >= 2 of 1{q >= r}")

    def occupancy_split():
        bad, tested = [], 0
        for n in SPINES:
            m = min(A.subcritical_lifetime(n), 40)
            if m < 1:
                continue
            total = Fraction(A.excess(n, m), m)
            for R in range(2, 9):
                tested += 1
                if A.truncated_occupancy(n, m, R) + A.tail_leakage(n, m, R) != total:
                    bad.append((n, R))
        return (not bad and tested > 0), {"splits": tested, "mismatches": bad[:5]}

    check("SRC14_the_occupancy_tail_split_is_an_exact_identity", occupancy_split,
          "§22-23: E_m/m = G_R(m) + L_R(m), in exact Fractions, for every R")

    def citation():
        rec = json.loads((EXTERNAL / "lopez-stoll-arxiv-2101.12747.json")
                         .read_text(encoding="utf-8"))
        bib = a5[a5.find("參考文獻"):] if "參考文獻" in a5 else ""
        needed = ["2101.12747", "López", "Stoll"]
        in_bib = [t for t in needed if t in bib]
        # The archived abstract must actually contain the equality the subject
        # leans on, in the subject's own notation.
        abstract = rec["abstract_sentence_supporting_it"]
        supports = ("ln(2)" in abstract and "ln(3)" in abstract
                    and "\\lim" in abstract and "non-cyclic" in abstract)
        flagged = "preprint" in bib
        return (len(in_bib) == 3 and supports and flagged), {
            "bibliography_fields_found": in_bib,
            "archived_abstract_states_the_liminf_equality": supports,
            "subject_flags_it_as_a_preprint": flagged,
            "not_verified": rec["not_verified"]}

    check("SRC14_the_lopez_stoll_citation_resolves_to_the_claimed_statement", citation,
          "§14's only external dependency, checked against an archived record of "
          "the arXiv abstract")

    def declines_a_proof():
        disclaimed = "未宣稱" in closure and "已證" in closure
        # The forbidden sentence must appear only as the one it labels incorrect.
        idx = closure.find("A 線已證明")
        labelled_incorrect = idx > 0 and "Incorrect statement" in closure[:idx]
        no_collatz_claim = "Collatz conjecture 已證" in closure  # in the 未宣稱 line
        return (disclaimed and labelled_incorrect and no_collatz_claim), {
            "has_an_explicit_disclaimer": disclaimed,
            "the_proof_sentence_appears_only_as_the_incorrect_one": labelled_incorrect}

    check("SRC14_the_closure_declines_to_claim_a_proof", declines_a_proof,
          "§9: the closure must say reduction complete, conjecture not proved")

    def open_ledger():
        tail = a5[a5.find("# 35."):] if "# 35." in a5 else ""
        opened = tail.find("## Open")
        listed = tail[opened:] if opened > 0 else ""
        return ("CASP" in listed and "未完成" in tail), {
            "open_section_names_casp": "CASP" in listed,
            "status_line_says_unfinished": "未完成" in tail}

    check("SRC14_the_closure_ledger_lists_casp_as_the_single_open_item", open_ledger,
          "§35: exactly one open item, and it is CASP")

    def reductions_map_to_reports():
        missing_in_doc, missing_report = [], []
        for phrase, report in REDUCTION_TO_REPORT.items():
            if phrase not in a5:
                missing_in_doc.append(phrase)
            if not (ROOT / "reports" / report).exists():
                missing_report.append(report)
        return (not missing_in_doc and not missing_report), {
            "reductions": len(REDUCTION_TO_REPORT),
            "claimed_but_absent_from_the_document": missing_in_doc,
            "mapped_to_a_report_that_does_not_exist": sorted(set(missing_report))}

    check("SRC14_every_completed_reduction_maps_to_a_report_in_this_tree",
          reductions_map_to_reports,
          "§35's completed list, each tied to the run in this arm that rechecked it")

    def bundle_is_faithful():
        # "COMPLETE" re-ships Rounds 01-03A4, which this arm verified one at a
        # time as items 19-28 in their own bundles. If any copy were edited, none
        # of that verification would transfer to item 30. Compared by digest.
        def members(path):
            out = {}
            with zipfile.ZipFile(path) as z:
                for n in z.namelist():
                    if n.endswith("/"):
                        continue
                    out[pathlib.PurePosixPath(n).name] = hashlib.sha256(
                        z.read(n)).hexdigest()
            return out

        big = members(SOURCE / BUNDLE)
        earlier = {p.name: members(p)
                   for p in sorted(SOURCE.glob("Hard_Zeta_Phase_I_Round_*_bundle.zip"))}
        same, edited, fresh = [], [], []
        for name, h in big.items():
            hit = next(((z, m[name]) for z, m in earlier.items() if name in m), None)
            if hit is None:
                fresh.append(name)
            elif hit[1] == h:
                same.append(name)
            else:
                edited.append({"file": name, "differs_from": hit[0]})
        measured["complete_bundle"] = {
            "reshipped_identical": sorted(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh)}
        # both halves must be non-empty, or the comparison saw nothing
        return (not edited and len(same) >= 7 and len(fresh) == 3), {
            "reshipped_identical": len(same), "reshipped_edited": edited,
            "new_in_this_bundle": sorted(fresh),
            "standalone_bundles_compared_against": len(earlier)}

    check("SRC14_the_complete_bundle_reships_the_rounds_unedited", bundle_is_faithful,
          "item 30 claims to bundle Rounds 01-03A5; the seven already rechecked as "
          "items 19-28 must be byte-identical to their standalone bundles, and "
          "exactly three files must be new")

    check("SRC14_the_route_map_and_the_closure_state_the_same_obstruction",
          lambda: ("CASP" in routemap and "CASP" in closure
                   and "finite forbidden-pattern" in routemap
                   and "finite forbidden-pattern" in closure,
                   {"routemap_len": len(routemap)}),
          "v0.8 and the closure must not disagree about what is left")

    # ------------------------------------------------------- own measurements
    def sup_is_short():
        per = {}
        for w in fc:
            r = C.normalized_correction_ratio(w)
            per[w.k] = max(per.get(w.k, Fraction(0)), r)
        top_k = max(per, key=lambda k: per[k])
        after = {k: v for k, v in per.items() if k > top_k}
        measured["ratio_max_by_length"] = {str(k): str(v) for k, v in sorted(per.items())}
        measured["ratio_supremum"] = {"value": str(per[top_k]), "length": top_k,
                                      "max_after": str(max(after.values())) if after else None}
        return (top_k <= 8 and bool(after) and max(after.values()) < per[top_k] / 10), {
            "argmax_length": top_k, "value": str(per[top_k]),
            "largest_at_greater_length": str(max(after.values())) if after else None}

    check("SRC14_the_ratio_supremum_is_attained_at_a_short_word", sup_is_short,
          "measurement: where sup R lives, and by how much longer words fall short")

    def witness_cost():
        rows = []
        for m in (8, 12, 16, 20, 24, 28, 32, 36):
            cheap = next((n for n in range(3, 200000, 2)
                          if A.subcritical_lifetime(n) >= m), None)
            rows.append({"m": m, "all_ones_witness": A.all_ones_source(m),
                         "cheapest_witness": cheap,
                         "ratio": (A.all_ones_source(m) // cheap) if cheap else None})
        measured["finite_local_witness_cost"] = rows
        return all(r["cheapest_witness"] and r["all_ones_witness"] > r["cheapest_witness"]
                   for r in rows), {"rows": rows[:3], "widest": rows[-1]}

    check("SRC14_the_finite_local_witness_is_exponentially_far_from_the_minimal_one",
          witness_cost,
          "measurement: §5's explicit witness 2^{m+1}-1 against the smallest start "
          "with the same subcritical reach")

    def shortfall_identity():
        # "E_m/m stays under gamma" cannot fail: subcriticality *forces* it, since
        # E_m = K_m - m <= floor(beta m) - m = floor(gamma m). So the bound is
        # tested in the only form that can fail — the exact integer identity that
        # says by how much — and the loop runs one step PAST the lifetime so both
        # signs of the deficit appear.
        gamma = math.log2(3) - 1
        bad, rows, signs = [], [], [0, 0]
        for n in SPINES:
            life = A.subcritical_lifetime(n)
            for m in range(1, life + 2):
                d = A.deficit(n, m)
                signs[0 if d >= 0 else 1] += 1
                if A.excess(n, m) != A.sturmian_credit(m) - d:
                    bad.append((n, m))
            rows.append({"n": n, "lifetime": life,
                         "excess": A.excess(n, life),
                         "budget": A.sturmian_credit(life),
                         "final_deficit": A.deficit(n, life),
                         "deficit_after_death": A.deficit(n, life + 1),
                         "density": float(Fraction(A.excess(n, life), life)),
                         "shortfall_from_gamma": gamma - A.excess(n, life) / life})
        measured["saturation"] = {"gamma": gamma, "spines": rows}
        return (not bad and min(signs) > 0), {
            "mismatches": bad[:5], "deficits_nonnegative": signs[0],
            "deficits_negative": signs[1], "_both_outcomes_seen": min(signs) > 0}

    check("SRC14_the_saturation_shortfall_is_exactly_the_budget_minus_the_deficit",
          shortfall_identity,
          "§19-20: E_m = floor(gamma m) - d_m, so gamma - E_m/m = ({gamma m} + d_m)/m; "
          "the inequality alone is forced by subcriticality and cannot fail")

    def tail_observable():
        # L_R = 0 for R above the largest valuation is likewise forced. The
        # falsifiable statement is that the observable is non-empty below it.
        rows, nonzero, zero = [], 0, 0
        for n in SPINES:
            m = A.subcritical_lifetime(n)
            if m < 1:
                continue
            top = max(A.orbit_valuations(n, m))
            # at R = top the observable is empty by definition, since (q - top)_+
            # is zero for every q on the spine; R = top - 1 is the last level that
            # can still see the largest valuation
            below = A.tail_leakage(n, m, top - 1)
            above = A.tail_leakage(n, m, top)
            nonzero += below > 0
            zero += above == 0
            rows.append({"n": n, "largest_valuation": top,
                         "L_just_below_the_top": str(below),
                         "L_at_and_above_the_top": str(above)})
        measured["tail_leakage"] = rows
        return (nonzero == len(rows) and zero == len(rows)), {
            "spines": len(rows), "nonzero_below_the_top": nonzero,
            "zero_above_the_top": zero,
            "_both_outcomes_seen": nonzero > 0 and zero > 0}

    check("SRC14_the_tail_leakage_observable_is_nonempty_only_below_the_top_valuation",
          tail_observable,
          "§23, §26: every finite spine has a bounded valuation, so Regime L is "
          "invisible to any bounded computation — checked with both outcomes")

    rep["failures"] = sorted(k for k, v in checks.items() if not v["pass"])
    rep["counts"] = {"checks": len(checks),
                     "passed": sum(1 for v in checks.values() if v["pass"]),
                     "first_crossing_words": len(fc),
                     "spines": len(SPINES)}
    rep["ok"] = not rep["failures"]
    out = io.StringIO()
    json.dump(rep, out, indent=2, ensure_ascii=False)
    print(out.getvalue())
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
