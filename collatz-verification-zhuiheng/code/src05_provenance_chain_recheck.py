"""Recheck of source items 08-16 — the draft chain, and what the repair repaired.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, `Collatz_OT_Series_Paper_01_v0.1_bundle.zip` through
`Collatz_OT_Series_Papers_01_08_v0.8_bundle.zip` (2026-08-10 22:58 .. 08-11
00:02), read against the `provenance/` tree of the SSSP Repaired v1.0 package.

Why these items get a different kind of check
---------------------------------------------
The mathematics of Papers 01-09 has already been rechecked in this tree, on the
final v1.0 text, in `reports/RUN-002-OT-SERIES.md`. Re-running that against
drafts of the same papers would measure nothing new.

What the draft chain uniquely supports is a **provenance** measurement, and it is
one nobody outside can perform without these files: the drafts are an independent
archive of the pre-repair text, written down three days before the repair
existed. That makes it possible to ask whether the repair's own account of itself
is complete.

The claim under test is `AUDIT_AND_CORRECTIONS.md`. It says which papers were
left byte-identical, which were corrected and why, and it ships per-paper unified
diffs under `provenance/diffs/`. A correction ledger is only worth something if
the diffs are load-bearing, so the central check here is:

    apply each published diff to the published original
        -> must reproduce the repaired file BYTE FOR BYTE.

If that holds for all ten sources, then the ledger is not a summary of the
changes; it *is* the changes, and an undisclosed edit has nowhere to hide.

Making it able to fail
----------------------
Two ways this could pass without meaning anything, both guarded:

- A patcher that ignores context would "reproduce" anything. So the applier
  demands exact context and exact line counts, and CHECK_PATCHER_REJECTS runs it
  against a one-character mutation of the original and against the wrong paper's
  diff. Both must be rejected.
- "Papers 01/04/05/06 are byte-preserved" is trivially true if nothing was ever
  compared. So the same comparison is required to report DIFFERENCES for
  02/03/07/08 — the byte-preservation claim and the correction claim are checked
  by one instrument, which therefore cannot pass both by being blind.

Likewise, "no legacy TeX delimiters remain" is vacuous unless some were there to
begin with, so their presence in the originals is a separate check.

Usage:  python code/src05_provenance_chain_recheck.py [source-folder] [sssp-root]
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
DEFAULT_SSSP = (ROOT.parent / "collatz-ot-series-neok"
                / "Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0")

# the draft chain, in the order it was written
DRAFT_BUNDLES = ["Collatz_OT_Series_Paper_01_v0.1_bundle.zip"] + [
    f"Collatz_OT_Series_Papers_01_{n:02d}_v0.{n}_bundle.zip" for n in range(2, 9)]

DRAFT_PAPERS = {
    1: "Collatz_OT_Series_Paper_01_Reclassification_and_Calibration_v0.1.md",
    2: "Collatz_OT_Series_Paper_02_Local_Affine_Atlas_Finite_Word_v0.1.md",
    3: "Collatz_OT_Series_Paper_03_Parity_Word_Residue_Cylinder_Identity_v0.1.md",
    4: "Collatz_OT_Series_Paper_04_Bidirectional_Residue_Transport_v0.1.md",
    5: "Collatz_OT_Series_Paper_05_Contraction_Boundary_Binomial_Cylinder_Law_v0.1.md",
    6: "Collatz_OT_Series_Paper_06_Valuation_Language_Accelerated_Collatz_v0.1.md",
    7: "Collatz_OT_Series_Paper_07_Generalized_mx_plus_r_RCOT_v0.1.md",
    8: "Collatz_OT_Series_Paper_08_Algebraic_Domains_Structural_Breakage_v0.1.md",
}

# the audit's own claim about which papers it left alone
CLAIMED_BYTE_PRESERVED = {"01", "04", "05", "06"}
CLAIMED_CORRECTED = {"02", "03", "07", "08", "09", "HZ"}


class PatchRejected(Exception):
    """The diff does not apply cleanly to the text it was given."""


def apply_unified_diff(original: str, diff: str) -> str:
    """Apply a unified diff, demanding exact context. Raises on any mismatch.

    Deliberately strict: every context and deletion line must match the source
    character for character, and every hunk's declared line counts must be
    exactly what the hunk body contains. A lenient applier would make the
    reproduction check meaningless.
    """
    src = original.split("\n")
    dl = diff.split("\n")
    out: list[str] = []
    pos = 0          # 0-based index into src
    i = 0
    hunk_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")

    while i < len(dl):
        line = dl[i]
        if line.startswith("--- ") or line.startswith("+++ "):
            i += 1
            continue
        m = hunk_re.match(line)
        if not m:
            if line == "":
                i += 1
                continue
            raise PatchRejected(f"unexpected line outside a hunk: {line[:60]!r}")
        i += 1
        old_start = int(m.group(1))
        old_len = int(m.group(2)) if m.group(2) is not None else 1
        new_len = int(m.group(4)) if m.group(4) is not None else 1

        # copy the untouched run before this hunk
        start = old_start - 1
        if start < pos:
            raise PatchRejected(f"hunk at {old_start} overlaps or moves backwards")
        out.extend(src[pos:start])
        pos = start

        consumed = produced = 0
        while i < len(dl) and (consumed < old_len or produced < new_len):
            body = dl[i]
            if body.startswith("@@"):
                break
            tag, text = (body[:1], body[1:]) if body else (" ", "")
            if tag == " ":
                if pos >= len(src) or src[pos] != text:
                    raise PatchRejected(
                        f"context mismatch at source line {pos + 1}: "
                        f"diff has {text[:50]!r}, source has "
                        f"{(src[pos] if pos < len(src) else '<EOF>')[:50]!r}")
                out.append(text)
                pos += 1
                consumed += 1
                produced += 1
            elif tag == "-":
                if pos >= len(src) or src[pos] != text:
                    raise PatchRejected(
                        f"deletion mismatch at source line {pos + 1}: "
                        f"diff removes {text[:50]!r}, source has "
                        f"{(src[pos] if pos < len(src) else '<EOF>')[:50]!r}")
                pos += 1
                consumed += 1
            elif tag == "+":
                out.append(text)
                produced += 1
            else:
                raise PatchRejected(f"unknown diff marker {tag!r}")
            i += 1

        if consumed != old_len or produced != new_len:
            raise PatchRejected(
                f"hunk at {old_start} declared -{old_len}/+{new_len} but "
                f"consumed {consumed}/produced {produced}")

    out.extend(src[pos:])
    return "\n".join(out)


def main() -> int:
    src_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    sssp = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_SSSP

    rep = {
        "tool": "src05_provenance_chain_recheck.py",
        "subject": ("Neo.K, Collatz OT Series draft bundles v0.1..v0.8 "
                    "(2026-08-10 22:58 .. 08-11 00:02), against the SSSP "
                    "Repaired v1.0 provenance tree"),
        "source_items": list(range(8, 17)),
        "scope": (
            "provenance, not mathematics. The mathematics of Papers 01-09 was "
            "rechecked on the final text in reports/RUN-002-OT-SERIES.md; this "
            "asks instead whether the repair's account of itself is complete."
        ),
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    # ---------------------------------------------------------------- drafts
    # 1. the chain is strictly additive: v0.N repeats v0.(N-1) byte for byte
    chain = []
    for nm in DRAFT_BUNDLES:
        with zipfile.ZipFile(src_dir / nm) as z:
            chain.append({n: z.read(n) for n in z.namelist()})

    additive = True
    index_moves = True
    added_per_step = []
    additive_witness = []
    for step in range(1, len(chain)):
        prev, cur = chain[step - 1], chain[step]
        papers_prev = {k: v for k, v in prev.items() if "INDEX" not in k}
        papers_cur = {k: v for k, v in cur.items() if "INDEX" not in k}
        for k, v in papers_prev.items():
            if papers_cur.get(k) != v:
                additive = False
                if len(additive_witness) < 5:
                    additive_witness.append({"step": f"v0.{step}->v0.{step+1}", "file": k})
        added = set(papers_cur) - set(papers_prev)
        added_per_step.append(len(added))
        idx_prev = next(v for k, v in prev.items() if "INDEX" in k)
        idx_cur = next(v for k, v in cur.items() if "INDEX" in k)
        if idx_prev == idx_cur:
            index_moves = False

    check("SRC05_draft_chain_carries_earlier_papers_byte_identical", additive,
          f"{additive_witness}")
    check("SRC05_each_draft_step_adds_exactly_one_paper",
          all(a == 1 for a in added_per_step), f"added per step: {added_per_step}")
    check("SRC05_the_series_index_is_rewritten_at_every_step", index_moves,
          "an unchanged INDEX would mean the bundles are not really successive")

    # 1b. three papers also sit loose in the source folder beside the bundles;
    # they must be the same bytes, or "the bundle" and "the file" would be two
    # different documents wearing one name.
    loose = ["Collatz_OT_Series_INDEX_v0.1.md",
             DRAFT_PAPERS[1],
             DRAFT_PAPERS[2]]
    loose_ok, loose_witness = True, []
    for nm in loose:
        f = src_dir / nm
        if not f.exists():
            loose_ok = False
            loose_witness.append({"file": nm, "why": "not in the source folder"})
            continue
        want = next((v for step in chain for k, v in step.items() if k == nm), None)
        if want is None or f.read_bytes() != want:
            loose_ok = False
            loose_witness.append({"file": nm, "why": "differs from the bundled copy"})
    check("SRC05_loose_markdown_files_match_their_bundled_copies", loose_ok,
          f"{loose_witness}")

    # 2. the drafts authenticate the SSSP provenance/original directory
    origs = {p.name[:2]: p for p in (sssp / "provenance" / "original").glob("0*__*.md")}
    hz_orig = next((sssp / "provenance" / "original").glob("HZ__*.md"))
    origs["HZ"] = hz_orig

    drafts_match = True
    draft_witness = []
    for n, fname in DRAFT_PAPERS.items():
        d = chain[-1][fname]
        o = origs[f"{n:02d}"].read_bytes()
        if d != o:
            drafts_match = False
            draft_witness.append({"paper": n, "draft_sha": hashlib.sha256(d).hexdigest()[:16],
                                  "orig_sha": hashlib.sha256(o).hexdigest()[:16]})
    check("SRC05_v08_drafts_are_byte_identical_to_the_sssp_provenance_originals",
          drafts_match,
          "the provenance directory does not reproduce the independently "
          f"archived pre-repair text: {draft_witness}")

    # ------------------------------------------------------------- checksums
    lines = (sssp / "CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines()
    bad_sum, checked_files = [], 0
    for ln in lines:
        if not ln.strip():
            continue
        want, rel = ln.split("  ", 1)
        f = sssp / rel
        if not f.exists():
            bad_sum.append({"file": rel, "why": "missing"})
            continue
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        checked_files += 1
        if got != want:
            bad_sum.append({"file": rel, "want": want[:16], "got": got[:16]})
    check("SRC05_checksums_file_matches_every_shipped_byte", not bad_sum, f"{bad_sum[:5]}")

    # ------------------------------------------------- originals vs repaired
    core = sssp / "core_series"
    repaired = {}
    for key, p in origs.items():
        if key == "HZ":
            repaired[key] = next((sssp / "research_program").glob("*.md"))
        elif key == "09":
            repaired[key] = core / "Collatz_OT_Series_Paper_09_Finite_Certificate_Frontier_v0.1.1.md"
        else:
            repaired[key] = core / p.name[4:]

    identical, differing = set(), set()
    for key, p in origs.items():
        if p.read_bytes() == repaired[key].read_bytes():
            identical.add(key)
        else:
            differing.add(key)

    check("SRC05_papers_claimed_byte_preserved_really_are",
          CLAIMED_BYTE_PRESERVED <= identical,
          f"claimed byte-preserved but differ: {sorted(CLAIMED_BYTE_PRESERVED - identical)}")
    # the same instrument must be able to see change, or the check above is blind
    check("SRC05_papers_claimed_corrected_really_do_differ",
          CLAIMED_CORRECTED <= differing,
          f"claimed corrected but identical: {sorted(CLAIMED_CORRECTED - differing)}")
    check("SRC05_no_paper_changed_that_the_audit_did_not_declare",
          differing == CLAIMED_CORRECTED,
          f"undeclared changes in: {sorted(differing - CLAIMED_CORRECTED)}")

    # ------------------------------------------------------------ the diffs
    diffs = {p.stem: p for p in (sssp / "provenance" / "diffs").glob("*.diff")}
    empty_right = (
        all(diffs[k].stat().st_size == 0 for k in CLAIMED_BYTE_PRESERVED)
        and all(diffs[k].stat().st_size > 0 for k in CLAIMED_CORRECTED))
    check("SRC05_diff_files_are_empty_exactly_for_the_byte_preserved_papers",
          empty_right,
          {k: diffs[k].stat().st_size for k in sorted(diffs)})

    # THE central check: the ledger is the change, not a summary of it
    repro, repro_witness, hunks_applied = True, [], 0
    for key in sorted(diffs):
        o = origs[key].read_text(encoding="utf-8")
        r = repaired[key].read_text(encoding="utf-8")
        d = diffs[key].read_text(encoding="utf-8")
        hunks_applied += d.count("\n@@ ") + (1 if d.startswith("@@ ") else 0)
        try:
            got = apply_unified_diff(o, d)
        except PatchRejected as exc:
            repro = False
            repro_witness.append({"paper": key, "rejected": str(exc)[:140]})
            continue
        if got != r:
            repro = False
            repro_witness.append({
                "paper": key,
                "why": "applied cleanly but did not reproduce the repaired file",
                "got_sha": hashlib.sha256(got.encode()).hexdigest()[:16],
                "want_sha": hashlib.sha256(r.encode()).hexdigest()[:16]})
    check("SRC05_every_published_diff_reproduces_the_repaired_file_exactly",
          repro, f"{repro_witness}")

    # ...and the applier must be capable of rejecting, or the above proves nothing
    rejects = 0
    probes = 2
    o07 = origs["07"].read_text(encoding="utf-8")
    d07 = diffs["07"].read_text(encoding="utf-8")
    mutated = o07.replace("Neo.K", "Neo.X", 1)          # one context line disturbed
    assert mutated != o07
    try:
        apply_unified_diff(mutated, d07)
    except PatchRejected:
        rejects += 1
    try:                                                 # wrong paper's diff
        apply_unified_diff(origs["08"].read_text(encoding="utf-8"), d07)
    except PatchRejected:
        rejects += 1
    check("SRC05_the_patch_applier_rejects_text_it_should_reject",
          rejects == probes,
          f"only {rejects} of {probes} deliberately wrong inputs were rejected, "
          "so a clean application is not evidence of anything")

    # ------------------------------------- each named correction, individually
    #
    # Every one of these asserts the correction is present in the repaired text
    # AND absent from the original, because presence alone is not evidence of a
    # repair — the first version of this file checked only that "P_k(1)=1"
    # appeared somewhere in Paper 07, and that string was already in the
    # original body, so the check could not fail for its stated reason.
    #
    # The absence half has its own trap: Papers 07/08/09/HZ were also mechanically
    # renotated from \(..\) to $..$, so a naive absence test would come out true
    # for every string containing math, for purely cosmetic reasons. The original
    # is therefore delimiter-normalized first, and absence must survive that.

    def normalize_delims(text: str) -> str:
        text = re.sub(r"^\s*\\\[\s*$", "$$", text, flags=re.M)
        text = re.sub(r"^\s*\\\]\s*$", "$$", text, flags=re.M)
        return text.replace(r"\(", "$").replace(r"\)", "$")

    repaired_text = {k: p.read_text(encoding="utf-8") for k, p in repaired.items()}
    orig_norm = {k: normalize_delims(p.read_text(encoding="utf-8"))
                 for k, p in origs.items()}

    def added(key: str, needle: str) -> bool:
        """Present in the repaired text, and not merely renotated from the original."""
        return needle in repaired_text[key] and needle not in orig_norm[key]

    def removed(key: str, needle: str) -> bool:
        """Present in the original, and gone from the repaired text."""
        return needle in orig_norm[key] and needle not in repaired_text[key]

    check("SRC05_P02_positive_integer_cylinder_replaces_the_ambiguous_preview",
          added("02", r"(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}")
          and removed("02", r"r_w+2^k\mathbb Z_{\ge0}"),
          "the r_w = 0 boundary correction is not both added and replacing the "
          "ambiguous Z_{>=0} preview")
    check("SRC05_P03_induction_uses_the_always_positive_representative",
          added("03", r"r_w+2^k\in\Omega_w.")
          and removed("03", "r_w\\in\\Omega_w,"),
          "Paper 03's induction still rests on r_w in Omega_w, which fails for the "
          "all-D cylinder where canonical r_w = 0")
    check("SRC05_P03_fixes_the_canonical_representative_explicitly",
          added("03", r"0\le r_w<2^k."),
          "the canonical representative is still not pinned down")
    check("SRC05_P07_summary_records_the_m_equals_1_case_separately",
          added("07", r"\boxed{P_k(1)=1.}")
          and added("07", r"須獨立處理而不能代入 $\ln m$ 分母"),
          "the theorem summary still leaves ln(1) = 0 in the denominator; note "
          "P_k(1)=1 was ALREADY in the original body, so its bare presence proves "
          "nothing — what the repair added is the summary statement")
    check("SRC05_P07_summary_restricts_the_log_formulas_to_odd_m_greater_than_1",
          repaired_text["07"].count("對 odd $m>1$：") >= 2
          and orig_norm["07"].count("對 odd $m>1$：") == 0,
          "Theorems E and F do not both carry the odd m > 1 restriction")
    # `A_wx+B_w` is Paper 08's standard form and appears throughout the original,
    # so its presence is no evidence of anything. The typo was the single §7
    # instance that wrote `A_wr`, so the correction is that string disappearing
    # and the §7 congruence appearing in corrected form.
    check("SRC05_P08_quotient_typo_is_corrected",
          removed("08", "A_wr+B_w")
          and added("08", "A_wx+B_w\n" + r"\equiv0" + "\n" + r"\pmod{D_w}."),
          "the A_w r -> A_w x correction is absent, or was never needed")
    check("SRC05_P08_states_the_ring_level_unit_condition",
          added("08", r"R^\times"),
          "ad - bc != 0 is still stated without a coefficient domain")
    check("SRC05_P09_language_typo_is_corrected",
          added("09", "若進一步") and removed("09", "若さらに"),
          "the 若さらに -> 若進一步 correction is absent, or was never needed")
    # Same trap, and this one is sharper: the ORIGINAL already contained both
    # `\widetilde H_w` and `H_w\cap[2,\infty)` — the v0.1.1 corrigendum had said
    # the stopping-time domain is n >= 2. The audit's complaint is precisely that
    # the main body still wrote the UNRESTRICTED union anyway. So the correction
    # is the disappearance of `\bigsqcup_{|w|=k}H_w`, not the appearance of a
    # tilde that was there all along.
    check("SRC05_HZ_main_body_no_longer_uses_the_unrestricted_union",
          removed("HZ", r"\bigsqcup_{|w|=k}H_w.")
          and added("HZ", r"\bigsqcup_{|w|=k}\widetilde H_w."),
          "the main body still decomposes E_k^C over the unrestricted H_w, so "
          "n = 1 can re-enter through the Hurwitz-zeta representation")
    check("SRC05_HZ_hoists_the_n_at_least_2_chart_into_the_main_argument",
          added("HZ", r"\boxed{" + "\n" + r"\widetilde H_w:=H_w\cap[2,\infty)." + "\n}")
          and added("HZ", r"先定義真正對應 stopping-time domain $n\ge2$ 的 chart"),
          "the restricted chart is still only defined inline inside Z_w, as a "
          "corrigendum rather than as part of the argument")

    # ------------------------------------------- the normalization claim, both ways
    legacy = re.compile(r"\\\(|\\\)|^\s*\\\[|^\s*\\\]", re.M)
    remaining = {k: len(legacy.findall(repaired[k].read_text(encoding="utf-8")))
                 for k in repaired}
    check("SRC05_no_legacy_tex_delimiters_remain_in_the_repaired_sources",
          all(v == 0 for v in remaining.values()),
          f"{ {k: v for k, v in remaining.items() if v} }")
    before = {k: len(legacy.findall(origs[k].read_text(encoding="utf-8"))) for k in origs}
    check("SRC05_legacy_delimiters_actually_existed_in_the_originals",
          all(before[k] > 0 for k in ("07", "08", "09", "HZ")),
          f"nothing to normalize, so the claim above is vacuous: {before}")

    # -------------------------------------------------------------- encoding
    bad_enc = []
    for k, p in repaired.items():
        raw = p.read_bytes()
        try:
            txt = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            bad_enc.append({"paper": k, "why": str(exc)[:80]})
            continue
        if "\ufffd" in txt:
            bad_enc.append({"paper": k, "why": "contains U+FFFD replacement characters"})
    check("SRC05_repaired_sources_decode_as_strict_utf8_without_replacement_chars",
          not bad_enc, f"{bad_enc}")

    # ---------------------------------------------------------------- output
    rep["counts"] = {
        "draft_bundles_read": len(chain),
        "draft_papers_compared_to_provenance": len(DRAFT_PAPERS),
        "sha256_entries_verified": checked_files,
        "diffs_applied": len(diffs),
        "diff_hunks_applied": hunks_applied,
        "papers_byte_preserved": sorted(identical),
        "papers_corrected": sorted(differing),
        "legacy_delimiters_in_originals": before,
    }
    rep["measured"]["assessment"] = {
        "what_it_establishes": (
            "The correction ledger is complete and load-bearing. Every one of the ten "
            "published diffs applies to its published original under an applier that "
            "demands exact context, and reproduces the repaired file byte for byte - so "
            "the repair contains no edit that AUDIT_AND_CORRECTIONS.md does not declare. "
            "Exactly the four papers it calls byte-preserved are byte-preserved, exactly "
            "the six it calls corrected differ, and no seventh source changed."
        ),
        "why_the_drafts_matter": (
            "Papers 01-08 inside the v0.8 draft bundle, archived on 2026-08-11, are "
            "byte-identical to provenance/original/. The pre-repair text is therefore "
            "attested by an archive that predates the repair by three days, rather than "
            "only by the repaired package's own account of what it started from."
        ),
        "on_the_draft_chain_itself": (
            "v0.1 through v0.8 is strictly additive: each step appends exactly one paper "
            "and rewrites the index, and never touches a paper already written. So there "
            "is no hidden revision history inside the chain - the revisions all happen "
            "later, at the repair, and are the ones listed."
        ),
        "what_it_does_not_establish": (
            "nothing mathematical. That every declared correction is present in the "
            "repaired text says the ledger is honest, not that the corrected statements "
            "are true. Their truth was checked separately, on the final text, in "
            "reports/RUN-002-OT-SERIES.md."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
