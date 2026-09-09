"""Gate 27 — the Phase 1 agent experiment against its own success and freeze conditions.

數學戰士「墜衡」 / AMRAL Research Lab.

`06_Phase1_Agent_Experiment` is the corpus's specification for the run that
produced Phase 1 and Phase 2. It sets five success conditions (§6) and five
conditions under which "本輪不算有效研究" — the round does not count as valid
research (§7). Those are the corpus's own standards for its own methodology,
and an attack about to reuse that methodology should know whether it met them.

Most of §6 and §7 need reading. **One of them does not, and it is the one this
arm has already caught itself failing:**

    將 analytic Sha 當 actual Sha
    (treating analytic Sha as actual Sha)

RUN-019 audited that pattern against this tree and found RUN-017's headline
guilty of it. The question is symmetric, so this gate asks it of the corpus:
every numeric claim about Sha in all 85 documents is located, and each is
classified by whether its surrounding text marks it as analytic/inferred,
as actual/proved, as both, or as **neither**.

WHAT AN UNLABELLED CLAIM IS AND IS NOT. It is not a violation. The label may
sit in a section heading, a status line, or the sentence before the window. So
this gate reports **where to look**, with the sentence, and refuses to call an
unlabelled claim a failure — the same discipline `src02` uses for the rejected
route's vocabulary. What it can decide is the count, and a count is what makes
"the corpus separates the two" a measurement instead of an impression.

THE SCANNING LESSONS OF RUN-024 ARE APPLIED HERE BY CONSTRUCTION. That round
found `src02`'s salvage detector could not fire, because its window was
same-line while the verdict it looked for sat four lines away, and because it
read 滿足 inside 未滿足. So this gate's window spans lines, its classifier knows
negation, and it reports every bucket — including the one that says the
detector found nothing to read.

Usage:  python code/src27_agent_experiment_audit.py
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CURATED = ROOT.parent.parent / "amral" / "public" / "bsd"
SUBLINES = ("phase0", "p5", "phase1", "phase2")
SPEC = "06_Phase1_Agent_Experiment.md"
OUT = ROOT / "data" / "gate-logs" / "src27-agent-experiment-audit.json"

# A NUMERIC claim about Sha. The structure is pinned rather than a loose "Sha
# … = digits" span: an optional subscript, then optional (…) and […] arguments,
# then the equals. The loose version's first run produced two false positives
# out of eight flagged rows — `\text{P4 Sha-control closed at }p=11`, which is
# not a claim about an order at all, and it would flag any prose that happened
# to put a number after the word.
SHA_CLAIM = re.compile(
    r"(?:#\s*)?(?:\\Sha|Sha|Ш)"
    # The subscript may nest one level: the corpus writes both `_{\rm an}` and
    # `_{\mathrm{an}}`, and a `[^}]` class stops at the inner brace of the
    # second, dropping every analytic claim written that way. Five real claims
    # were lost to exactly that before this was widened.
    r"(?P<sub>_\{(?:[^{}]|\{[^{}]*\})*\}|_[A-Za-z]{1,3})?"
    r"\s*(?:\([^)\n]{0,40}\))?\s*(?:\[[^\]\n]{0,40}\])?\s*&?=\s*\{?\s*(\d+)\b")
CONTEXT = 300

# An `an` subscript makes the symbol itself say analytic — `\Sha_{\rm an}` is
# how phase2/00 writes it, and no amount of surrounding vocabulary is needed.
ANALYTIC_SUBSCRIPT = re.compile(r"\ban\b|analytic", re.I)

ANALYTIC = re.compile(
    r"(analytic|BSD-inferred|inferred|predicted|prediction|conjectur|"
    r"解析|預測|推得)", re.I)
ACTUAL = re.compile(
    r"(actual|proved|proven|rigorous|certified|unconditional|theorem|"
    r"實際|真實|已證|嚴格)", re.I)
# Provenance is a label too, and the corpus uses it constantly: a value that
# says where it came from is not an unlabelled value. Missing this vocabulary
# is what made six of the first run's eight flagged rows look unlabelled.
PROVENANCE = re.compile(
    r"(inherited|imported|from the (?:project|phase)|承襲|繼承|"
    r"引用|沿用|imported from|inherited closure)", re.I)
# A required hypothesis is not a claim about the world and needs no such label.
HYPOTHESIS = re.compile(
    r"(要求|假設|假定|assume|assuming|require|requires|hypothes|"
    r"suppose|條件)", re.I)
NEGATION = re.compile(
    r"(not\s|no\s|un(?:proved|certified|known)|未|尚未|不|"
    r"沒有|unknown)", re.I)


def documents() -> list[tuple[str, pathlib.Path]]:
    out = []
    for sub in SUBLINES:
        d = CURATED / sub / "files"
        if not d.is_dir():
            raise SystemExit(f"curated corpus not found: {d}")
        out.extend((sub, m) for m in sorted(d.glob("*.md")))
    return out


def classify_claim(window: str, subscript: str | None = None) -> tuple[str, str]:
    """How the claim is labelled, in the order the labels bind.

    The symbol's own subscript comes first and needs nothing else: `\\Sha_{\\rm
    an}` says analytic in the notation. Then a hypothesis marker, because a
    required condition is not a claim about the world and needs no
    analytic/actual label at all. Then the two labels, negation-aware — "not
    proved" is not an actual-Sha label. Then provenance, because a value that
    says it was inherited or imported has said where it stands. Only what
    survives all of that is unlabelled.
    """
    if subscript and ANALYTIC_SUBSCRIPT.search(subscript):
        return "analytic by its own subscript", "analytic"

    def present(pat):
        m = pat.search(window)
        if not m:
            return False
        lo = max(0, m.start() - 16)
        return not NEGATION.search(window[lo:m.start()])

    if HYPOTHESIS.search(window):
        return "stated as a hypothesis", "hypothesis"
    a, c = present(ANALYTIC), present(ACTUAL)
    if a and c:
        return "both labels present", "analytic+actual"
    if a:
        return "labelled analytic", "analytic"
    if c:
        return "labelled actual", "actual"
    if PROVENANCE.search(window):
        return "labelled by provenance", "provenance"
    return "unlabelled in window", ""


def scan() -> dict:
    rows = []
    for sub, m in documents():
        text = m.read_text(encoding="utf-8", errors="replace")
        for hit in SHA_CLAIM.finditer(text):
            lo = max(0, hit.start() - CONTEXT)
            hi = min(len(text), hit.end() + CONTEXT)
            verdict, kind = classify_claim(text[lo:hi], hit.group("sub"))
            line_no = text[:hit.start()].count("\n") + 1
            rows.append({
                "subline": sub, "name": m.name, "line_no": line_no,
                "claim": hit.group(0).replace("\n", " ").strip()[:80],
                "verdict": verdict, "kind": kind,
            })
    counts = collections.Counter(r["verdict"] for r in rows)
    unlabelled = [r for r in rows if r["verdict"] == "unlabelled in window"]
    by_doc = collections.Counter(f"{r['subline']}/{r['name']}" for r in unlabelled)
    return {
        "numeric_Sha_claims_found": len(rows),
        "documents_carrying_one": len({(r["subline"], r["name"]) for r in rows}),
        "verdict_counts": dict(counts),
        "unlabelled_by_document": dict(by_doc.most_common()),
        "unlabelled_sample": unlabelled[:12],
        "what_an_unlabelled_claim_is_not": (
            "a violation. The label may sit in a heading, a status line, or "
            "outside the 300-character window. This gate reports where to look "
            "and refuses to call a hit a failure; the count is the measurement"),
        "rows": rows,
    }


def success_conditions() -> list[dict]:
    """§6's five, each with what this arm can say and what it cannot.

    Only the third is settled here, and it is settled by rounds that did not
    set out to answer it: the Banwait-Huang reproduction is either reproducible
    or it is not, and this tree reproduced it independently.
    """
    return [
        {"condition": "1. 完整 schema",
         "this_arm": "not measured. A schema's completeness is a reading of the "
                     "spec's Steps A-E against the artefacts, not a computation"},
        {"condition": "2. 至少三類曲線的證書",
         "this_arm": "partly. R2+ is 389.a1, verified in RUN-011, RUN-020, "
                     "RUN-022 and RUN-023. R0 is 696.e1, whose analytic rank 0 "
                     "was established in RUN-014. No R1 certificate has passed "
                     "through this arm"},
        {"condition": "3. Banwait-Huang 算法可重現",
         "this_arm": "MET, and independently. RUN-007 and RUN-008 closed 122,247 "
                     "isogeny determinations both ways; RUN-012 rebuilt all "
                     "247,391 twist pairs exactly, 36,687 of 36,687 curves "
                     "agreeing. Reproduction by a second implementation is a "
                     "stronger reading of this condition than the experiment "
                     "asserting it"},
        {"condition": "4. 每個結果能區分 evidence / theorem",
         "this_arm": "measurable and measured elsewhere: this is src01's ladder "
                     "vocabulary check, and RUN-021's ledger separated "
                     "computation from citation across the P5 chain"},
        {"condition": "5. 找到高秩前三大共同瓶頸",
         "this_arm": "the corpus names them. P5_E1_ETNC_ESCAPE_AUDIT §6 lists "
                     "four targets, and its blocking chain roots at P5-DERPER; "
                     "whether that is the right three is not a computation"},
    ]


def freeze_conditions(sha: dict) -> list[dict]:
    """§7's five. The fourth is the one this gate decides."""
    counts = sha["verdict_counts"]
    unl = counts.get("unlabelled in window", 0)
    total = sha["numeric_Sha_claims_found"]
    return [
        {"condition": "只抄 LMFDB",
         "this_arm": "not triggered as far as this arm can see: RUN-004 "
                     "recomputed 40,749 discriminants and 135,787 valuations, "
                     "RUN-016 recomputed 40,749 conductors, and all agreed. A "
                     "corpus that only copied would still agree, so this is "
                     "consistency and not proof of independence"},
        {"condition": "只算數值比",
         "this_arm": "not triggered: the corpus carries exact finite "
                     "certificates (det M_loc = 2, the Selmer cube, the "
                     "localization rows) that RUN-011 and RUN-022 recomputed "
                     "in exact arithmetic"},
        {"condition": "無法追溯 theorem hypotheses",
         "this_arm": "not triggered: RUN-021 traced every P5 gate to either an "
                     "exact finite computation or a named external theorem, and "
                     "found no gate that could not be traced"},
        {"condition": "將 analytic Sha 當 actual Sha",
         "this_arm": f"MEASURED HERE. {total} numeric Sha claims across the "
                     f"corpus; {unl} carry neither label within 300 characters. "
                     f"An unlabelled claim is not a violation — see the gate's "
                     f"own caveat — but the count is what makes the separation "
                     f"a measurement",
         "counts": counts},
        {"condition": "無法分辨 weak / strong / p-part",
         "this_arm": "not triggered: the three appear as distinct headings in "
                     "01_BSD_Statement_and_Quantifier_Audit §1.1-1.3 and are "
                     "used distinctly downstream"},
    ]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    docs = documents()
    if len(docs) != 85:
        raise SystemExit(f"expected the 85 curated documents, read {len(docs)}")
    if not any(m.name == SPEC for _, m in docs):
        raise SystemExit(f"{SPEC} is not in the corpus; there is nothing to audit against")

    sha = scan()
    log = {
        "gate": "src27 — the Phase 1 agent experiment against its own conditions",
        "spec": SPEC,
        "documents_scanned": len(docs),
        "sha_labelling": sha,
        "success_conditions_section_6": success_conditions(),
        "freeze_conditions_section_7": freeze_conditions(sha),
        "ok": (len(docs) == 85 and sha["numeric_Sha_claims_found"] > 0),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  documents scanned: {len(docs)}")
    print(f"  numeric Sha claims: {sha['numeric_Sha_claims_found']} across "
          f"{sha['documents_carrying_one']} documents")
    for k, v in sorted(sha["verdict_counts"].items()):
        print(f"    {k:24s} {v}")
    if sha["unlabelled_by_document"]:
        print("  unlabelled, by document (where to look, not a verdict):")
        for k, v in list(sha["unlabelled_by_document"].items())[:8]:
            print(f"    {v:3d}  {k}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
