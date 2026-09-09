"""Gate 30 — every number Phase 1 states, against every number this tree computed.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-027 measured that **none of Phase 1's 25 documents has been the subject of a
round**, while six rounds verified that line's arithmetic down to 122,247
isogeny determinations and all 247,391 twist pairs. Those rounds were aimed at
the artefacts the documents describe, so the documents themselves have never
been read on the record.

Reading them is one job. This gate does the harder half, which reading cannot
do: **does the arithmetic the documents state agree with the arithmetic this
tree computed?** Every integer of four digits or more in the 25 documents is
extracted with its context, and matched against every integer appearing anywhere
in this tree's own gate logs.

FOUR OUTCOMES, AND THE SECOND ONE IS THE POINT.

  confirmed  — the number appears in our logs too. Not proof the claim is right,
               but the two computations produced the same figure.
  absent     — we have no counterpart. Either a quantity no round computed, or
               one computed differently. This is the list worth reading, and it
               is printed with context so it can be.
  malformed  — a digit run too long to be a count, produced by a table whose
               columns ran together in the markdown.
  masked     — a git SHA, an LMFDB curve label, or a LaTeX argument pair: a
               digit run that is not a magnitude at all.

Both of the last two are reported rather than silently dropped, because a filter
that quietly discards is how a scan comes to under-report — this tree's most
repeated failure, four rounds running by RUN-027's count. This gate's first
version had the mirror fault, a loud over-report, and its third mask was found
by reading its own absent list rather than by any check.

WHAT A CONFIRMATION IS WORTH. It is a coincidence of integers, not a proof: two
different quantities can share a value. So the gate reports the context of every
match as well, and the report reads the ones that carry weight rather than
counting them all as agreement.

Usage:  python code/src30_phase1_numeric_crosscheck.py
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHASE1 = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
LOGS = ROOT / "data" / "gate-logs"
OUT = LOGS / "src30-phase1-numeric-crosscheck.json"

# Four digits or more, with optional thousands separators, not glued to another
# digit or a decimal point. The upper bound on length is what separates a count
# from a table whose columns ran together.
NUM = re.compile(r"(?<![\d.,])(\d{1,3}(?:,\d{3})+|\d{4,})(?![\d.,])")
MAX_DIGITS = 12
CONTEXT = 90

# Two of the three masks, and the first
# version of this gate reported 30 absent values of which most were one or the
# other. The four rounds before this one all produced silent UNDER-reports; this
# was the same fault pointed the other way, a loud over-report, and from the same
# root — a pattern built from what the author imagined the corpus contains.
#
#   a git SHA. `1a0489c3c3099dd0c248624e6621df73ae8f0d43` yields 248624, 3099,
#   6621 and more, because stretches of hex happen to be all digits.
#   an LMFDB curve label. `66166b1`, `104474a1`, `302606a1` are conductors with
#   an isogeny class attached, not quantities the document is asserting.
SHA_LIKE = re.compile(r"\b[0-9a-f]{7,40}\b")
CURVE_LABEL = re.compile(r"\b\d{2,7}[a-z]{1,2}\d*\b")

# And a third, found by reading this gate's own absent list rather than by any
# check: `\gcd(3,138)=3` is a LaTeX argument pair, and the thousands-separator
# form read it as the number 3,138. A comma-separated pair opening with `(` or
# following another comma is an argument list, not a magnitude.
ARG_PAIR = re.compile(r"[(,]\s*\d{1,3},\d{1,3}\s*[),]")


def _masked_spans(text: str) -> list[tuple[int, int]]:
    """Character ranges that are a git SHA, an LMFDB curve label, or a LaTeX
    argument pair — the three things in these documents that look like a
    number and are not one."""
    spans = [(m.start(), m.end()) for m in SHA_LIKE.finditer(text)
             if any(c.isdigit() for c in m.group(0))
             and any(c.isalpha() for c in m.group(0))]
    spans += [(m.start(), m.end()) for m in CURVE_LABEL.finditer(text)]
    spans += [(m.start(), m.end()) for m in ARG_PAIR.finditer(text)]
    return spans


def document_numbers() -> tuple[list[dict], list[dict], list[dict]]:
    """Every candidate integer in the Phase 1 documents, with context.

    Returns (counts, malformed, masked). The third is reported rather than
    dropped: a filter that quietly discards is exactly how a scan comes to
    under-report, and this gate's first version over-reported for the mirror
    reason. Both directions are now visible in the log.
    """
    good, malformed, masked = [], [], []
    for f in sorted(PHASE1.glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        spans = _masked_spans(text)
        for m in NUM.finditer(text):
            inside = next((s for s in spans
                           if s[0] <= m.start() and m.end() <= s[1]), None)
            if inside:
                masked.append({"document": f.name, "written": m.group(1),
                               "line": text[:m.start()].count("\n") + 1,
                               "masked_by": text[inside[0]:inside[1]][:48]})
                continue
            raw = m.group(1)
            digits = raw.replace(",", "")
            lo = max(0, m.start() - CONTEXT)
            hi = min(len(text), m.end() + CONTEXT)
            row = {"document": f.name, "written": raw,
                   "line": text[:m.start()].count("\n") + 1,
                   "context": " ".join(text[lo:hi].split())[:170]}
            if len(digits) > MAX_DIGITS:
                row["why"] = (f"{len(digits)} digits — a run-together table "
                              "column, not a count")
                malformed.append(row)
            else:
                row["value"] = int(digits)
                good.append(row)
    return good, malformed, masked


def our_numbers() -> set[int]:
    """Every integer of four digits or more anywhere in this tree's gate logs."""
    out: set[int] = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lstrip("-").isdigit():
                    out.add(abs(int(k)))
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, bool):
            return
        elif isinstance(o, int):
            out.add(abs(o))
        elif isinstance(o, float):
            return
        elif isinstance(o, str):
            for m in NUM.findall(o):
                d = m.replace(",", "")
                if len(d) <= MAX_DIGITS:
                    out.add(int(d))

    for g in sorted(LOGS.glob("*.json")):
        if g.name == OUT.name:
            continue
        walk(json.loads(g.read_text(encoding="utf-8")))
    return {n for n in out if n >= 1000}


# The Q9 block exactly as `V0_5_EXACT_CENSUS_REPORT` prints it. At module level
# so the drill can corrupt one stated value and see whether the identity check
# notices — a defect planted inside the function would be patching the thing
# under test rather than its input.
Q9_STATED = {"old_total_twist_pairs": 293482, "new_total_twist_pairs": 247391,
             "lhs": 46091, "upstream_removed": 24785, "stable_removed": 21306,
             "stable_added": 0, "newbase_added": 0, "rhs": 46091}


def q9_accounting_identity() -> dict:
    """`V0_5_EXACT_CENSUS_REPORT` §Q9, checked as arithmetic and as provenance.

    The report states a closed accounting of the twist census:

        old_total_twist_pairs = 293482    new_total_twist_pairs = 247391
        lhs = 46091                       upstream_removed = 24785
        stable_removed = 21306            stable_added = 0
        newbase_added = 0                 rhs = 46091

    Two things are separable and both are done. **The arithmetic**: lhs must be
    old − new and rhs must be upstream + stable_removed − stable_added −
    newbase_added, and the two must agree. **The provenance**: which of the five
    independent inputs this tree has computed for itself, and which it has not.

    RUN-012 rebuilt all 247,391 twist pairs and measured the entry-level census
    at 21,306 removed with 0 added, the expansion branch being empty over the
    whole domain. So three of the five are ours. `old_total_twist_pairs` and
    `upstream_removed` are not — and because the identity ties them, confirming
    either would pin the other.
    """
    v = dict(Q9_STATED)
    lhs = v["old_total_twist_pairs"] - v["new_total_twist_pairs"]
    rhs = (v["upstream_removed"] + v["stable_removed"]
           - v["stable_added"] - v["newbase_added"])
    ours = {"new_total_twist_pairs": "RUN-012 rebuilt all 247,391 twist pairs",
            "stable_removed": "RUN-012: 21,306 removed at entry level",
            "stable_added": "RUN-012: 0 added",
            "newbase_added": "RUN-012: the expansion branch is empty over the "
                             "whole domain"}
    return {
        "stated": v,
        "lhs_recomputed": lhs, "lhs_agrees": lhs == v["lhs"],
        "rhs_recomputed": rhs, "rhs_agrees": rhs == v["rhs"],
        "identity_holds": lhs == rhs == v["lhs"] == v["rhs"],
        "inputs_this_tree_computed": ours,
        "inputs_this_tree_has_not": {
            "old_total_twist_pairs": "no round has counted the pre-change twist "
                                     "census",
            "upstream_removed": "no round has counted Algorithm 1's own twist "
                                "removals",
        },
        "reading": ("the identity is correct arithmetic and four of its inputs "
                    "are independently ours. The two that are not are tied by "
                    "the identity, so one measurement would close both — that "
                    "is the cheapest open item this round found"),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    docs = sorted(PHASE1.glob("*.md"))
    if len(docs) != 25:
        raise SystemExit(f"expected Phase 1's 25 documents, read {len(docs)}")

    good, malformed, masked = document_numbers()
    ours = our_numbers()
    for r in good:
        r["in_our_logs"] = r["value"] in ours

    confirmed = [r for r in good if r["in_our_logs"]]
    absent = [r for r in good if not r["in_our_logs"]]
    distinct_conf = sorted({r["value"] for r in confirmed}, reverse=True)
    distinct_abs = sorted({r["value"] for r in absent}, reverse=True)
    by_doc = collections.Counter(r["document"] for r in absent)

    log = {
        "gate": "src30 — Phase 1's stated numbers against this tree's computed ones",
        "documents": len(docs),
        "gate_logs_read": len(list(LOGS.glob("*.json"))) - 1,
        "distinct_integers_in_our_logs": len(ours),
        "counts": {
            "occurrences_in_the_documents": len(good),
            "distinct_values": len({r["value"] for r in good}),
            "confirmed_occurrences": len(confirmed),
            "confirmed_distinct": len(distinct_conf),
            "absent_occurrences": len(absent),
            "absent_distinct": len(distinct_abs),
            "malformed": len(malformed),
            "masked_as_sha_or_curve_label": len(masked),
        },
        "confirmed_values": distinct_conf,
        "absent_values": distinct_abs,
        "absent_by_document": dict(by_doc.most_common()),
        "absent_rows": absent,
        "malformed_rows": malformed,
        "masked_rows": masked[:40],
        "why_masking_is_reported": (
            "the first version of this gate reported 30 absent values, most of "
            "them digit runs inside a git SHA or an LMFDB curve label. The four "
            "rounds before this one produced silent UNDER-reports; that was the "
            "same fault pointed the other way. Both directions are visible here"),
        "what_a_confirmation_is_worth": (
            "a coincidence of integers, not a proof. Two different quantities "
            "can share a value, so the contexts are kept and the report reads "
            "the ones that carry weight rather than counting them all as "
            "agreement"),
        "q9_accounting_identity": q9_accounting_identity(),
        "ok": (len(docs) == 25 and len(good) > 0 and len(ours) > 0
               and q9_accounting_identity()["identity_holds"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    c = log["counts"]
    print(f"  {len(docs)} Phase 1 documents, {log['gate_logs_read']} gate logs")
    print(f"  integers >= 1000: {c['occurrences_in_the_documents']} occurrences, "
          f"{c['distinct_values']} distinct")
    print(f"    confirmed by our own logs : {c['confirmed_distinct']} distinct "
          f"({c['confirmed_occurrences']} occurrences)")
    print(f"    no counterpart here       : {c['absent_distinct']} distinct "
          f"({c['absent_occurrences']} occurrences)")
    print(f"    malformed (run-together)  : {c['malformed']}")
    print(f"    masked (SHA / curve label): "
          f"{c['masked_as_sha_or_curve_label']}")
    print()
    print(f"  confirmed: {distinct_conf[:14]}")
    print(f"  absent   : {distinct_abs[:14]}")
    print()
    print("  absent, by document (where to look):")
    for k, v in list(by_doc.most_common())[:10]:
        print(f"    {v:3d}  {k}")
    q9 = log["q9_accounting_identity"]
    print()
    print(f"  Q9 accounting identity: lhs {q9['lhs_recomputed']} "
          f"({q9['lhs_agrees']}), rhs {q9['rhs_recomputed']} "
          f"({q9['rhs_agrees']}), holds: {q9['identity_holds']}")
    print(f"    inputs this tree computed itself: "
          f"{sorted(q9['inputs_this_tree_computed'])}")
    print(f"    and has not                     : "
          f"{sorted(q9['inputs_this_tree_has_not'])}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
