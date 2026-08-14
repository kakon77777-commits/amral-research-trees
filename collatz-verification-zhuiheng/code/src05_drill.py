"""Mutation drill for src05_provenance_chain_recheck.py.

數學戰士「墜衡」 / AMRAL Research Lab.

The provenance recheck passed 21/21 on the first run. That is exactly the
situation this tree treats as unverified: a suite that agrees with expectation
has not yet been shown capable of disagreeing.

So the SSSP package is copied to a scratch tree, one defect is planted at a time,
and the recheck is re-run against the damaged copy. A defect counts as caught
only if **the check named for it** fails — not merely if the run goes red, since
almost any edit under `core_series/` also trips the checksum verifier and would
otherwise produce a comfortable-looking catch for the wrong reason.

Two NULL controls disturb nothing a check reads. If they go red, the suite is
reacting to the drill rather than to the defects.

Usage:  python code/src05_drill.py
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SSSP = (ROOT.parent / "collatz-ot-series-neok"
        / "Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0")
TOOL = ROOT / "code" / "src05_provenance_chain_recheck.py"
SOURCE = pathlib.Path(
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper")
TIMEOUT_S = 300


def core(tree: pathlib.Path, stem_fragment: str) -> pathlib.Path:
    hits = [p for p in (tree / "core_series").glob("*.md") if stem_fragment in p.name]
    if len(hits) != 1:
        raise SystemExit(f"drill setup: {stem_fragment!r} matched {len(hits)} files")
    return hits[0]


def sub(p: pathlib.Path, old: str, new: str, count: int = 1) -> None:
    t = p.read_text(encoding="utf-8")
    if old not in t:
        raise SystemExit(f"drill setup: {old!r} not found in {p.name} — "
                         "the defect would not have been planted")
    p.write_text(t.replace(old, new, count), encoding="utf-8")


# ---------------------------------------------------------------- the defects
# (id, target check that MUST fail, mutate(tree))

def d01(t): sub(core(t, "考拉茲猜想既有研究"), "Neo.K", "Neo.Q")
def d02(t): sub(core(t, "有限字收縮邊界"), "Neo.K", "Neo.Q")
def d03(t):
    p = t / "provenance" / "diffs" / "07.diff"
    lines = p.read_text(encoding="utf-8").split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("+") and not ln.startswith("+++"):
            lines[i] = ln[:-1] if len(ln) > 2 else "+"
            break
    p.write_text("\n".join(lines), encoding="utf-8")
def d04(t): sub(core(t, "廣義 (mx+r)"), r"\boxed{P_k(1)=1.}", r"\boxed{P_k(1)=0.}")
def d13(t): sub(core(t, "廣義 (mx+r)"), "對 odd $m>1$：", "對 odd $m$：", count=-1)
def d14(t): sub(core(t, "Collatz Local Affine Atlas"),
                r"(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}", r"r_w+2^k\mathbb Z_{\ge0}")
def d15(t): sub(core(t, "代數判定域"), r"R^\times", r"R^\ast", count=-1)
def d16(t): sub(core(t, "Parity Word"), r"0\le r_w<2^k.", r"0\le r_w\le 2^k.")
def d17(t):
    """A 'correction' that was never new: plant it in the original too.

    This drills the anti-vacuity half specifically. The repaired text still has
    the string, so a presence-only check stays green; only comparing against the
    original can notice.
    """
    p = next((t / "provenance" / "original").glob("07__*.md"))
    txt = p.read_text(encoding="utf-8")
    p.write_text(txt.replace("## Theorem G", "\\[\n\\boxed{P_k(1)=1.}\n\\]\n\n## Theorem G", 1),
                 encoding="utf-8")
def d05(t): sub(core(t, "代數判定域"), "A_wx+B_w", "A_wr+B_w")
def d06(t): sub(core(t, "Paper_09_Finite"), "$", r"\(")
def d07(t): (t / "provenance" / "diffs" / "04.diff").write_text("@@ -1,1 +1,1 @@\n", encoding="utf-8")
def d08(t):
    p = t / "CHECKSUMS.sha256"
    lines = p.read_text(encoding="utf-8").split("\n")
    lines[0] = "0" * 64 + lines[0][64:]
    p.write_text("\n".join(lines), encoding="utf-8")
def d09(t): sub(next((t / "research_program").glob("*.md")),
                r"\bigsqcup_{|w|=k}\widetilde H_w.", r"\bigsqcup_{|w|=k}H_w.", count=-1)
def d18(t): sub(next((t / "research_program").glob("*.md")),
                r"先定義真正對應 stopping-time domain $n\ge2$ 的 chart",
                r"先定義 chart")
def d10(t):
    p = core(t, "Valuation Language")
    p.write_bytes(p.read_bytes().replace("Neo.K".encode(), "Neo�K".encode(), 1))
def d11(t): sub(next((t / "provenance" / "original").glob("02__*.md")), "Neo.K", "Neo.Q")
def d12(t): sub(core(t, "Parity Word"), "r_w+2^k", "r_w+2^j", count=-1)

DEFECTS = [
    ("D01_byte_preserved_paper_01_altered",
     "SRC05_papers_claimed_byte_preserved_really_are", d01),
    ("D02_undeclared_change_to_paper_05",
     "SRC05_no_paper_changed_that_the_audit_did_not_declare", d02),
    ("D03_one_added_line_shortened_in_diff_07",
     "SRC05_every_published_diff_reproduces_the_repaired_file_exactly", d03),
    ("D04_P07_summary_m_equals_1_statement_removed",
     "SRC05_P07_summary_records_the_m_equals_1_case_separately", d04),
    ("D05_P08_quotient_typo_reinstated",
     "SRC05_P08_quotient_typo_is_corrected", d05),
    ("D06_legacy_delimiter_reintroduced_into_paper_09",
     "SRC05_no_legacy_tex_delimiters_remain_in_the_repaired_sources", d06),
    ("D07_empty_diff_for_byte_preserved_paper_04_filled_in",
     "SRC05_diff_files_are_empty_exactly_for_the_byte_preserved_papers", d07),
    ("D08_checksum_entry_corrupted",
     "SRC05_checksums_file_matches_every_shipped_byte", d08),
    ("D09_HZ_main_body_reverted_to_the_unrestricted_union",
     "SRC05_HZ_main_body_no_longer_uses_the_unrestricted_union", d09),
    ("D10_replacement_character_planted_in_paper_06",
     "SRC05_repaired_sources_decode_as_strict_utf8_without_replacement_chars", d10),
    ("D11_provenance_original_02_no_longer_matches_the_draft",
     "SRC05_v08_drafts_are_byte_identical_to_the_sssp_provenance_originals", d11),
    ("D12_P03_positive_representative_replaced",
     "SRC05_P03_induction_uses_the_always_positive_representative", d12),
    ("D13_P07_odd_m_greater_than_1_restriction_weakened",
     "SRC05_P07_summary_restricts_the_log_formulas_to_odd_m_greater_than_1", d13),
    ("D14_P02_ambiguous_cylinder_preview_reinstated",
     "SRC05_P02_positive_integer_cylinder_replaces_the_ambiguous_preview", d14),
    ("D15_P08_ring_unit_condition_altered",
     "SRC05_P08_states_the_ring_level_unit_condition", d15),
    ("D16_P03_canonical_representative_bound_loosened",
     "SRC05_P03_fixes_the_canonical_representative_explicitly", d16),
    ("D17_P07_summary_statement_was_never_new",
     "SRC05_P07_summary_records_the_m_equals_1_case_separately", d17),
    ("D18_HZ_restricted_chart_demoted_out_of_the_main_argument",
     "SRC05_HZ_hoists_the_n_at_least_2_chart_into_the_main_argument", d18),
]

# NULL controls: touch nothing any check reads
def n01(t): (t / "UNREAD_SCRATCH_FILE.txt").write_text("not listed in CHECKSUMS\n", encoding="utf-8")
def n02(t): pass

CONTROLS = [
    ("N01_unrelated_file_added_outside_the_checksum_manifest", n01),
    ("N02_no_change_at_all", n02),
]


def run_against(tree: pathlib.Path) -> dict:
    out = subprocess.run(
        [sys.executable, str(TOOL), str(SOURCE), str(tree)],
        capture_output=True, text=True, encoding="utf-8", timeout=TIMEOUT_S,
        env={**__import__("os").environ, "PYTHONUTF8": "1"})
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "checks": {}, "_crash": (out.stdout + out.stderr)[-400:]}


def main() -> int:
    rep = {
        "tool": "src05_drill.py",
        "subject": "src05_provenance_chain_recheck.py",
        "why": ("the recheck passed 21/21 on first run; this establishes that it "
                "is capable of failing, and that each defect is caught by the "
                "check named for it rather than by a bystander"),
        "defects": {},
        "controls": {},
    }

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        base = pathlib.Path(tmp) / "base"
        shutil.copytree(SSSP, base)

        baseline = run_against(base)
        if not baseline.get("ok"):
            print(json.dumps({"error": "baseline is not green; drill is meaningless",
                              "baseline": baseline}, indent=2, ensure_ascii=False))
            return 2

        for name, target, mutate in DEFECTS:
            work = pathlib.Path(tmp) / name
            shutil.copytree(base, work)
            mutate(work)
            res = run_against(work)
            checks = res.get("checks", {})
            named_failed = target in checks and not checks[target]["pass"]
            also = sorted(k for k, v in checks.items() if not v["pass"] and k != target)
            rep["defects"][name] = {
                "target_check": target,
                "caught_by_the_named_check": bool(named_failed),
                "run_went_red": not res.get("ok", True),
                "other_checks_that_also_fired": also,
                **({"crash": res["_crash"]} if "_crash" in res else {}),
            }
            shutil.rmtree(work, ignore_errors=True)

        for name, mutate in CONTROLS:
            work = pathlib.Path(tmp) / name
            shutil.copytree(base, work)
            mutate(work)
            res = run_against(work)
            failed = sorted(k for k, v in res.get("checks", {}).items() if not v["pass"])
            rep["controls"][name] = {
                "undisturbed": bool(res.get("ok")) and not failed,
                "checks_that_fired": failed,
            }
            shutil.rmtree(work, ignore_errors=True)

    caught = sum(1 for v in rep["defects"].values() if v["caught_by_the_named_check"])
    quiet = sum(1 for v in rep["controls"].values() if v["undisturbed"])
    rep["counts"] = {
        "defects_planted": len(DEFECTS),
        "defects_caught_by_the_named_check": caught,
        "controls": len(CONTROLS),
        "controls_undisturbed": quiet,
    }
    rep["ok"] = caught == len(DEFECTS) and quiet == len(CONTROLS)
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
