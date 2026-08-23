#!/usr/bin/env python3
"""Recheck of the Hard-Zeta Collatz New-Chat Handoff v1.0 (source item 48).

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, `Hard_Zeta_Collatz_New_Chat_Handoff_v1.0.zip`
(2026-08-13). Two new documents — a handoff and a start prompt — plus six round
documents that also ship in item 47.

## This item is not a round, and the right check is different

Every earlier item in the sweep asserted mathematics. This one asserts *what the
other documents say*. It is a **compression** of nine rounds into fifteen pages,
and it is the document a fresh conversation is bootstrapped from — so an error in
it does not sit in one round, it seeds every round after.

The question is therefore fidelity, and it is mechanical:

  * **every number** in the handoff must be traceable to a round document, either
    verbatim or as a correct rounding of one;
  * **every document** it reships must be byte-identical to the copy in the
    bundle it came from;
  * **every status** it carries must match the round's own — nothing conditional
    promoted, nothing external presented as proved;
  * and its stated *intermediate* lemmas must actually be the round's lemmas,
    not stronger ones that happen to imply the same conclusion.

That last one is where compressions fail quietly, and it is where this one does.

## What is deliberately NOT checked

Whether the mathematics holds. RUN-019 through RUN-029 did that, round by round.
This file checks only that the handoff reports it faithfully.

Usage:
  python code/src48_handoff_fidelity.py --bundle DIR --corpus DIR [--source DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import zipfile
from fractions import Fraction

import mpmath as mp

WORKING_DPS = 400

HANDOFF = "Hard_Zeta_Collatz_New_Chat_Handoff_v1.0.md"
START_PROMPT = "Hard_Zeta_Collatz_New_Chat_Start_Prompt_v1.0.md"

#: literals of at least this many decimals are treated as claims to be traced
DECIMALS = 5

#: constants the handoff prints that have a closed form, so they can be checked
#: against arithmetic rather than only against another document
CLOSED_FORMS = {
    "beta = log2 3": (lambda: mp.log(3, 2), "1.5849625007"),
    "eta_beta = 1/(6 ln 2)": (lambda: 1 / (6 * mp.log(2)), "0.24044917348"),
    "kappa_rot = 1/(12 sqrt 2)": (lambda: 1 / (12 * mp.sqrt(2)), "0.05892556510"),
    "cf leading = 6 (ln2)^2": (lambda: 6 * mp.log(2) ** 2, "2.8827180835"),
    "cf second = 3 (ln2)^3/sqrt2":
        (lambda: 3 * mp.log(2) ** 3 / mp.sqrt(2), "0.7064519692"),
}

#: exact rationals, from rho_star = 4.1164 being a terminating decimal (RUN-029)
RATIONALS = {
    "theta_star = 1/(rho+1)": (Fraction(2500, 12791), "0.195449925729"),
    "sigma_star = 1/(1+theta)": (Fraction(12791, 15291), "0.836505133739"),
    "1 - sigma_star": (Fraction(2500, 15291), "0.163494866261"),
}

#: statements the handoff must carry, and statements it must not.
#: Each negative is paired with a string it DOES match, so an absence check
#: cannot pass merely by being a pattern that matches nothing.
REQUIRED_PRESENT = {
    "disclaims proving Collatz / Terras / CASP":
        r"不宣稱已證\s*Collatz\s*/\s*Terras\s*/\s*CASP",
    "flags the Diophantine exponent as an external input":
        r"外部\s*Diophantine\s*input",
    "flags the criticality theorem as an external input":
        r"外部\s*criticality\s*theorem\s*input",
    "carries the G non-telescoping no-go":
        r"當成\s*actual correction-bank expenditure直接相加",
    "keeps the first-crossing index caveat":
        r"與\s*modified-step B-line exact crossing的時間\s*index\s*不完全相同",
    "states the frontier as a disjunction":
        r"Sparse.*Highly Nested.*Huge Partial Quotients",
}
REQUIRED_ABSENT = {
    "does not claim CASP is proved":
        (r"CASP\s*(已證明|已被證明|is proved|已證$)", "CASP 已證明"),
    "does not claim the Collatz conjecture is proved":
        (r"(Collatz\s*(猜想)?\s*已證明|已證明\s*Collatz)", "Collatz 猜想已證明"),
    "does not present the Diophantine exponent as derived here":
        (r"(本輪|我們)\s*(證明|推導).{0,12}rho_?\\?star", "本輪證明了 rho_star"),
}


# ---------------------------------------------------------------------------

ARXIV = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})")


def arxiv_ids(text: str) -> list[str]:
    return sorted(set(ARXIV.findall(text)))


def literals(text: str) -> list[str]:
    """Numeric CLAIMS, which is not the same as numeric strings.

    `2111.02635` matches any pattern for "a number with five decimals" and is an
    arXiv identifier. A first version reported it as a constant appearing in no
    round document -- true, and completely the wrong reading of it: it is a
    reference the handoff adds, and the right check for a reference is whether it
    resolves and says what it is said to say, not whether an earlier round used
    it. Identifiers are separated out here and checked as references.
    """
    ids = set(arxiv_ids(text))
    return sorted(set(m.group(0) for m in re.finditer(r"\d+\.\d{%d,}" % DECIMALS, text)
                      if m.group(0) not in ids))


def decimals_of(text: str) -> int:
    return len(text.split(".")[1])


def is_correct_rounding(shown: str, longer: str) -> bool:
    """Is `shown` the correct rounding of the longer decimal `longer`?"""
    places = decimals_of(shown)
    if decimals_of(longer) <= places:
        return False
    scale = 10 ** places
    ref = Fraction(longer)
    truncated = Fraction(int(ref * scale), scale)
    remainder = ref * scale - int(ref * scale)
    rounded = truncated + (Fraction(1, scale) if remainder >= Fraction(1, 2) else 0)
    return Fraction(shown) in (truncated, rounded)


def trace_literal(value: str, corpus: dict[str, str]) -> dict:
    """Where a number in the handoff comes from: verbatim, rounded, or nowhere."""
    verbatim = sorted(n for n, t in corpus.items() if value in t)
    if verbatim:
        return {"how": "verbatim", "documents": len(verbatim),
                "example": verbatim[0], "ok": True}
    head = value.split(".")[0] + "." + value.split(".")[1][:DECIMALS]
    longer = set()
    for name, text in corpus.items():
        for cand in re.finditer(r"\d+\.\d{%d,}" % (decimals_of(value) + 1), text):
            if cand.group(0).startswith(head[:-1]) and is_correct_rounding(value, cand.group(0)):
                longer.add((cand.group(0), name))
    if longer:
        source, name = sorted(longer)[0]
        return {"how": "correct rounding of a longer literal", "source": source,
                "example": name, "documents": len({n for _, n in longer}), "ok": True}
    return {"how": "NOT FOUND in any round document", "ok": False}


# ---------------------------------------------------------------------------

def check_cross_bundle_identity(source: pathlib.Path | None) -> dict:
    """A document reshipped in several bundles must be the same bytes each time.

    The line reships its prior rounds in every bundle, so two copies of one
    filename drifting apart is a live risk and a silent one -- a reader takes
    whichever copy is nearest.
    """
    if source is None or not source.exists():
        return {"skipped": "no --source given", "ok": True, "checked": 0}
    hashes: dict[str, set[str]] = {}
    bundles: dict[str, set[str]] = {}
    for zpath in sorted(source.glob("Hard_Zeta*.zip")):
        try:
            zf = zipfile.ZipFile(zpath)
        except zipfile.BadZipFile:                       # pragma: no cover
            continue
        for name in zf.namelist():
            if not name.lower().endswith(".md"):
                continue
            base = pathlib.Path(name).name
            hashes.setdefault(base, set()).add(
                hashlib.sha256(zf.read(name)).hexdigest())
            bundles.setdefault(base, set()).add(zpath.name)
    reshipped = {k: v for k, v in bundles.items() if len(v) > 1}
    divergent = sorted(k for k, v in hashes.items() if len(v) > 1)
    return {
        "distinct_documents": len(hashes),
        "documents_reshipped_in_more_than_one_bundle": len(reshipped),
        "most_reshipped": max(((len(v), k) for k, v in bundles.items()), default=(0, ""))[1],
        "most_reshipped_count": max((len(v) for v in bundles.values()), default=0),
        "documents_with_more_than_one_hash": divergent,
        "ok": not divergent and len(reshipped) > 0,
    }


def check_constants(handoff: str, prompt: str, corpus: dict) -> dict:
    with mp.workdps(WORKING_DPS):
        closed = {}
        for name, (fn, printed) in CLOSED_FORMS.items():
            value = fn()
            places = decimals_of(printed)
            whole = len(mp.nstr(value, 5).split(".")[0].lstrip("-"))
            reference = mp.nstr(value, places + whole + 12, strip_zeros=False)
            closed[name] = {
                "handoff_prints": printed,
                "correct": bool(Fraction(printed) == Fraction(reference[:len(printed)])
                                or is_correct_rounding(printed, reference)),
                "in_the_handoff": printed in handoff,
            }
    rational = {}
    for name, (exact, printed) in RATIONALS.items():
        places = decimals_of(printed)
        digits = []
        num, den = exact.numerator, exact.denominator
        whole, num = divmod(num, den)
        for _ in range(places + 12):
            num *= 10
            d, num = divmod(num, den)
            digits.append(str(d))
        reference = "%d.%s" % (whole, "".join(digits))
        rational[name] = {
            "exact": "%d/%d" % (exact.numerator, exact.denominator),
            "handoff_prints": printed,
            "correct": is_correct_rounding(printed, reference)
                       or printed == reference[:len(printed)],
            "in_the_handoff": printed in handoff,
        }

    traced = {}
    for value in literals(handoff) + literals(prompt):
        if value in traced:
            continue
        traced[value] = trace_literal(value, corpus)

    wrong_closed = sorted(k for k, v in closed.items() if not v["correct"])
    wrong_rational = sorted(k for k, v in rational.items() if not v["correct"])
    missing = sorted(k for k, v in closed.items() if not v["in_the_handoff"])
    missing += sorted(k for k, v in rational.items() if not v["in_the_handoff"])
    untraceable = sorted(k for k, v in traced.items() if not v["ok"])
    return {
        "closed_forms": closed,
        "exact_rationals": rational,
        "literals_traced": len(traced),
        "traced_verbatim": sum(1 for v in traced.values() if v["how"] == "verbatim"),
        "traced_as_a_correct_rounding": sum(
            1 for v in traced.values() if v["how"].startswith("correct rounding")),
        "trace": traced,
        "constants_disagreeing_with_their_closed_form": wrong_closed + wrong_rational,
        "constants_the_handoff_does_not_actually_print": missing,
        "numbers_in_no_round_document": untraceable,
        "ok": not (wrong_closed or wrong_rational or missing or untraceable),
    }


def check_references_introduced(handoff: str, corpus: dict, lit: dict) -> dict:
    """arXiv identifiers in the handoff, and whether any round ever cited them."""
    verified = {r.get("arxiv"): r for r in lit.get("references", [])}
    rows = []
    for ident in arxiv_ids(handoff):
        cited_in = [n for n, text in corpus.items() if ident in text]
        rec = verified.get(ident, {})
        rows.append({
            "arxiv": ident,
            "cited_in_round_documents": len(cited_in),
            "new_in_the_handoff": not cited_in,
            "checked_in_the_literature_record": bool(rec),
            "status": rec.get("status", "not checked"),
        })
    new_ones = [r for r in rows if r["new_in_the_handoff"]]
    return {
        "identifiers": rows,
        "introduced_by_the_handoff": [r["arxiv"] for r in new_ones],
        "introduced_and_unchecked": [r["arxiv"] for r in new_ones
                                     if not r["checked_in_the_literature_record"]],
    }


def check_occupancy_bound(handoff: str, corpus: dict) -> dict:
    """The handoff's stated lemma against the round's stated lemma.

    A-U.2d.2 proves an explicit occupancy bound and then divides by 12:

        O_L >= (sqrt(H^2 + 2N) - H)/2 - 1,     Lambda_L >= O_L/12

    With H = o(sqrt L) and N = L - 1 that gives O_L >~ sqrt(L)/sqrt(2), and hence
    kappa_rot = 1/(12 sqrt 2). The handoff carries the SAME conclusion and the
    same 1/12, but states the lemma as `O_L >~ sqrt L` -- which is the round's
    bound multiplied by sqrt 2, and which, combined with the 1/12 the handoff
    also prints, yields 1/12 rather than 1/(12 sqrt 2).

    So the two lines are internally inconsistent, and the intermediate is the
    stronger of the two. That is the failure mode a compression has: the
    conclusion is copied correctly and the step that produced it is rounded off.
    """
    with mp.workdps(60):
        rows = []
        for L in (10 ** 4, 10 ** 6, 10 ** 8, 10 ** 10, 10 ** 12):
            N = mp.mpf(L - 1)
            H = mp.mpf(0)                     # the o(sqrt L) limit the round takes
            bound = (mp.sqrt(H ** 2 + 2 * N) - H) / 2 - 1
            rows.append({"L": "1e%d" % len(str(L - 1)),
                         "round_s_occupancy_bound_over_sqrt_L":
                             mp.nstr(bound / mp.sqrt(L), 10)})
        limit = 1 / mp.sqrt(2)
        ratio = mp.mpf(rows[-1]["round_s_occupancy_bound_over_sqrt_L"])
        converges = abs(ratio - limit) < mp.mpf("1e-5")

        kappa_round = 1 / (12 * mp.sqrt(2))
        kappa_from_handoff_lemma = mp.mpf(1) / 12
        factor = kappa_from_handoff_lemma / kappa_round

    def squeeze(s: str) -> str:
        """Strip ALL whitespace. Needles must be squeezed the same way.

        A first version squeezed only the haystack and left `\\mathcal O_L` in the
        needle -- which becomes `\\mathcalO_L` in the squeezed text and never
        matches. The gate then reported the handoff as NOT making the claim it
        plainly makes, and the finding below silently disappeared. A search that
        normalises one side only is a search that answers "no".
        """
        return re.sub(r"\s+", "", s)

    au2d2 = next((t for n, t in corpus.items() if "AU2d2_Rotation_Envelope" in n), "")
    flat_round, flat_handoff = squeeze(au2d2), squeeze(handoff)
    round_states_explicit = bool(re.search(r"H_\{y,N\}\^2\+2N", flat_round))
    handoff_states_sqrt_L = squeeze(r"\mathcal O_L\gtrsim\sqrt L") in flat_handoff
    handoff_states_twelfth = squeeze(r"\Lambda_L\ge\mathcal O_L/12") in flat_handoff
    handoff_keeps_kappa = "0.05892556510" in handoff
    round_states_sqrt_L_alone = squeeze(r"\mathcal O_L\gtrsim\sqrt L") in flat_round
    handoff_states_the_lemma_somehow = (
        handoff_states_sqrt_L or squeeze(r"H_{y,N}^2+2N") in flat_handoff)
    # The finding needs BOTH halves of the handoff's own arithmetic. If either
    # locator stops finding its line, the contradiction disappears from the
    # report while everything still looks green -- so each gets a failure.
    handoff_states_the_divisor = handoff_states_twelfth

    return {
        "the_round_states_an_explicit_occupancy_bound": round_states_explicit,
        "the_handoff_states_the_lemma_in_some_recognised_form":
            handoff_states_the_lemma_somehow,
        "the_handoff_s_divisor_line_was_located": handoff_states_the_divisor,
        "the_round_never_states_the_bare_sqrt_L_form": not round_states_sqrt_L_alone,
        "the_handoff_states_it_as_O_L_gtrsim_sqrt_L": handoff_states_sqrt_L,
        "the_handoff_also_states_Lambda_ge_O_over_12": handoff_states_twelfth,
        "the_handoff_keeps_the_round_s_kappa_rot": handoff_keeps_kappa,
        "round_bound_over_sqrt_L": rows,
        "its_limit_is_1_over_sqrt_2": bool(converges),
        "kappa_implied_by_the_handoff_s_own_two_lines": mp.nstr(kappa_from_handoff_lemma, 10),
        "kappa_the_round_proves_and_the_handoff_prints": mp.nstr(kappa_round, 10),
        "overstatement_factor": mp.nstr(factor, 10),
        "internally_inconsistent": bool(
            handoff_states_sqrt_L and handoff_states_twelfth and handoff_keeps_kappa),
    }


def check_status_fidelity(handoff: str) -> dict:
    present, absent, vacuous = {}, {}, []
    for name, pattern in REQUIRED_PRESENT.items():
        present[name] = bool(re.search(pattern, handoff, re.S))
    for name, (pattern, counterexample) in REQUIRED_ABSENT.items():
        hit = re.search(pattern, handoff)
        # An absence check that matches nothing anywhere is not evidence; each
        # pattern is shown to fire on a string that SHOULD trip it.
        fires = bool(re.search(pattern, counterexample))
        if not fires:
            vacuous.append(name)
        absent[name] = {"absent_from_the_handoff": not hit,
                        "pattern_fires_on_its_counterexample": fires}
    return {
        "required_present": present,
        "required_absent": absent,
        "missing_statements": sorted(k for k, v in present.items() if not v),
        "forbidden_statements_found": sorted(
            k for k, v in absent.items() if not v["absent_from_the_handoff"]),
        "absence_checks_that_could_never_fire": vacuous,
        "ok": all(present.values())
              and all(v["absent_from_the_handoff"] for v in absent.values())
              and not vacuous,
    }


def check_reference_hygiene(handoff: str, lit: dict) -> dict:
    """The reference list a new conversation is told to work from."""
    section = handoff.split("# 25.")[-1].split("# 26.")[0]
    entries = [ln.strip("- ").strip() for ln in section.splitlines()
               if ln.strip().startswith("-")]
    # Counting bullets is not enough to know this is the reference list -- the
    # section after it is a list of working-style bullets and would pass a
    # bullet count. Aiming the locator there made the whole check evaporate
    # without a single failure, so the locator has to recognise its subject.
    identifiers_here = len(ARXIV.findall(section))
    with_caveat = [e for e in entries if "caveat" in e or "保留" in e]
    withdrawn = {r["arxiv"]: r for r in lit["references"]
                 if r.get("status") == "WITHDRAWN"}
    rows = []
    for arxiv, rec in withdrawn.items():
        cited = [e for e in entries if arxiv in e]
        rows.append({"arxiv": arxiv, "withdrawn_on": rec.get("withdrawn_on"),
                     "occurrence": rec.get("OCCURRENCE"),
                     "listed_in_section_25": bool(cited),
                     "entry": cited[0] if cited else None,
                     "carries_a_caveat": bool(cited) and any(
                         "caveat" in c or "撤" in c or "withdraw" in c.lower()
                         for c in cited)})
    return {
        "entries_in_the_standing_reference_list": len(entries),
        "arxiv_identifiers_in_the_located_section": identifiers_here,
        "entries_carrying_a_caveat": len(with_caveat),
        "caveat_examples": with_caveat,
        "withdrawn_references": rows,
        "a_withdrawn_reference_is_listed_without_a_caveat": any(
            r["listed_in_section_25"] and not r["carries_a_caveat"] for r in rows),
    }


def check_file_manifest(handoff: str, corpus: dict) -> dict:
    section = handoff.split("# 24.")[-1].split("# 25.")[0]
    named = sorted(set(re.findall(r"`([A-Za-z0-9_.]+\.(?:md|py|json))`", section)))
    found = [n for n in named if n in corpus]
    missing = [n for n in named if n not in corpus]
    return {
        "files_named": len(named),
        "markdown_found_in_the_corpus": len([n for n in found if n.endswith(".md")]),
        "not_markdown_so_not_in_this_corpus": [n for n in missing
                                               if not n.endswith(".md")],
        "markdown_named_but_missing": [n for n in missing if n.endswith(".md")],
    }


# ---------------------------------------------------------------------------

def main() -> int:
    # This report quotes Traditional Chinese and accented names, and a Windows
    # console defaults to cp950 here. Without this the gate dies on its own
    # output, which is a way of failing that says nothing about the subject.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True, type=pathlib.Path)
    ap.add_argument("--corpus", required=True, type=pathlib.Path)
    ap.add_argument("--source", type=pathlib.Path)
    ap.add_argument("--literature", type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    handoff = (args.bundle / HANDOFF).read_text(encoding="utf-8")
    prompt = (args.bundle / START_PROMPT).read_text(encoding="utf-8")
    corpus = {p.name: p.read_text(encoding="utf-8", errors="replace")
              for p in sorted(args.corpus.glob("*.md"))
              if "New_Chat" not in p.name}
    lit = (json.loads(args.literature.read_text(encoding="utf-8"))
           if args.literature and args.literature.exists()
           else {"references": []})

    rep = {
        "round": "Hard-Zeta Collatz New-Chat Handoff v1.0",
        "source_item": 48,
        "corpus_documents": len(corpus),
        "cross_bundle_identity": check_cross_bundle_identity(args.source),
        "constants": check_constants(handoff, prompt, corpus),
        "references_introduced": check_references_introduced(handoff, corpus, lit),
        "occupancy_bound": check_occupancy_bound(handoff, corpus),
        "status_fidelity": check_status_fidelity(handoff),
        "reference_hygiene": check_reference_hygiene(handoff, lit),
        "file_manifest": check_file_manifest(handoff, corpus),
    }

    cb, cs, ob = rep["cross_bundle_identity"], rep["constants"], rep["occupancy_bound"]
    sf, rh, fm = rep["status_fidelity"], rep["reference_hygiene"], rep["file_manifest"]
    ri = rep["references_introduced"]

    failures = []
    if cb.get("documents_with_more_than_one_hash"):
        failures.append("a reshipped document differs between bundles")
    if not cb.get("ok"):
        failures.append("the cross-bundle identity check did not exercise anything")
    if cs["constants_disagreeing_with_their_closed_form"]:
        failures.append("a handoff constant disagrees with its closed form: %s"
                        % cs["constants_disagreeing_with_their_closed_form"])
    if cs["constants_the_handoff_does_not_actually_print"]:
        failures.append("a constant this check claims to read is not in the handoff")
    if cs["numbers_in_no_round_document"]:
        failures.append("the handoff prints numbers found in no round document: %s"
                        % cs["numbers_in_no_round_document"])
    if sf["missing_statements"]:
        failures.append("the handoff drops required statements: %s"
                        % sf["missing_statements"])
    if sf["forbidden_statements_found"]:
        failures.append("the handoff overclaims: %s" % sf["forbidden_statements_found"])
    if sf["absence_checks_that_could_never_fire"]:
        failures.append("an absence check is vacuous: %s"
                        % sf["absence_checks_that_could_never_fire"])
    if not ob["the_round_states_an_explicit_occupancy_bound"]:
        failures.append("the occupancy comparison could not find the round's bound")
    if not ob["its_limit_is_1_over_sqrt_2"]:
        failures.append("the round's occupancy bound does not tend to sqrt(L)/sqrt(2)")
    if ri["introduced_and_unchecked"]:
        failures.append("the handoff introduces references no round cites and this "
                        "run did not check them: %s" % ri["introduced_and_unchecked"])
    if not ob["the_handoff_states_the_lemma_in_some_recognised_form"]:
        failures.append("the occupancy comparison cannot find the handoff's own "
                        "lemma in any form, so it is reading nothing")
    if not ob["the_handoff_s_divisor_line_was_located"]:
        failures.append("the occupancy comparison cannot find the handoff's "
                        "divisor line, so half its arithmetic is unread")
    if (rh["entries_in_the_standing_reference_list"] < 5
            or rh["arxiv_identifiers_in_the_located_section"] < 4):
        failures.append("the standing reference list could not be located")
    if fm["files_named"] < 5:
        failures.append("the handoff's file manifest could not be located")
    if not ob["the_round_never_states_the_bare_sqrt_L_form"]:
        failures.append("the occupancy comparison found the bare sqrt-L form in the "
                        "round too, so there is nothing to compare")
    if fm["markdown_named_but_missing"]:
        failures.append("the handoff names markdown files that do not exist: %s"
                        % fm["markdown_named_but_missing"])

    findings = []
    if ob["internally_inconsistent"]:
        findings.append(
            "the handoff states the occupancy lemma as `O_L >~ sqrt L`, which is "
            "the round's own bound times sqrt 2. Combined with the `Lambda >= "
            "O_L/12` the handoff also prints, that yields kappa_rot = %s, while "
            "the handoff prints the round's correct %s three lines later. The "
            "conclusion was copied and the step that produces it was rounded off, "
            "so the two lines contradict each other by a factor of %s."
            % (ob["kappa_implied_by_the_handoff_s_own_two_lines"],
               ob["kappa_the_round_proves_and_the_handoff_prints"],
               ob["overstatement_factor"]))
    if rh["a_withdrawn_reference_is_listed_without_a_caveat"]:
        for row in rh["withdrawn_references"]:
            if row["listed_in_section_25"] and not row["carries_a_caveat"]:
                findings.append(
                    "arXiv:%s, withdrawn %s, is listed in the standing reference "
                    "list a new conversation is told to work from, with no note — "
                    "occurrence %s. The list does annotate elsewhere (%d of %d "
                    "entries carry a caveat), so the omission is not a format "
                    "limitation."
                    % (row["arxiv"], row["withdrawn_on"], row["occurrence"],
                       rh["entries_carrying_a_caveat"],
                       rh["entries_in_the_standing_reference_list"]))

    rep["findings"] = findings
    rep["failures"] = failures
    rep["passed"] = not failures

    text = json.dumps(rep, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
