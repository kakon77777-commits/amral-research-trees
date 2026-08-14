"""Independent recheck of Operation Translation Series — Paper 01.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *考拉茲猜想既有研究的重新分類與校正*, Paper 01 v0.1.

Correcting a second judgement of mine
-------------------------------------
An earlier note in this tree said Paper 01's content is "bibliographic rather than
arithmetic — a different instrument again: this arm can check numbers, not
literature." Half of that was wrong twice over.

**Citations are externally checkable.** An arXiv identifier either resolves to a
record with the stated title, authors and date, or it does not. A DOI either
resolves to the stated journal, volume and year, or it does not. That is an
external anchor of exactly the kind this arm values most — the expectations are
not authored here.

**And Paper 01 is not only bibliographic.** Its Claim Ledger classifies old
results by evidence strength, and every entry it labels `T` (Theorem / Exact
Structural Result) is a concrete arithmetic statement that can be settled here.
Mislabelling those would be a real defect: a merely heuristic claim filed as `T`
would be the exact failure the ledger exists to prevent.

So this recheck has two halves: the ledger's arithmetic, and the bibliography.

The subject's regression suite has no Paper 01 test.

Sources are snapshotted under ../data/external/bibliography/ so the run is
reproducible offline; the live URLs are recorded beside each check.

Usage:  python code/ot_paper01_recheck.py
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re

import os

# COLLATZ_TREE_ROOT lets the mutation drill run a mutant from a scratch directory
# while still pointing at the archived bibliography snapshots. Absence of a
# snapshot is a failure, not a skip.
ROOT = pathlib.Path(
    os.environ.get("COLLATZ_TREE_ROOT", pathlib.Path(__file__).resolve().parent.parent))
BIB = ROOT / "data" / "external" / "bibliography"

# Each entry: arXiv id -> what Paper 01 / the package's reference audit states.
CITED_ARXIV = {
    "1805.00133": {
        "file": "ax_1805.00133.xml",
        "title": "Parity sequences of the 3x+1 map on the 2-adic integers and Euclidean embedding",
        "authors": ["Olivier Rozier"],
        "url": "https://arxiv.org/abs/1805.00133",
    },
    "1909.03562": {
        "file": "ax_1909.03562.xml",
        "title": "Almost all orbits of the Collatz map attain almost bounded values",
        "authors": ["Terence Tao"],
        "journal_contains": "Forum Math. Pi 10 (2022)",
        "url": "https://arxiv.org/abs/1909.03562",
    },
    "2111.06170": {
        "file": "ax_2111.06170.xml",
        "title": "Generalized Collatz Maps with Almost Bounded Orbits",
        "authors": ["Felipe Gonçalves", "Rachel Greenfeld", "Jose Madrid"],
        "url": "https://arxiv.org/abs/2111.06170",
    },
    "2602.10466": {
        "file": "ax_2602.10466.xml",
        "title": "An improved algorithm for checking the Collatz conjecture for all n < 2^N",
        "authors": ["Vigleik Angeltveit"],
        "url": "https://arxiv.org/abs/2602.10466",
    },
    "2605.13886": {
        "file": "ax_2605.13886.xml",
        "title": "Parity vectors and paradoxical sequences in the accelerated Collatz map",
        "authors": ["Tong Niu"],
        "url": "https://arxiv.org/abs/2605.13886",
    },
    "math/0411140": {
        "file": "ax_semigroup.xml",
        "title": "The 3x+1 Semigroup",
        "authors": ["David Applegate", "Jeffrey C. Lagarias"],
        "journal_contains": "Journal of Number Theory 117 (2006)",
        "url": "https://arxiv.org/abs/math/0411140",
    },
}


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def col(n: int) -> int:
    return n // 2 if n % 2 == 0 else 3 * n + 1


def v2(n: int) -> int:
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


def norm(s: str) -> str:
    return " ".join(s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").split())


def rotate_right(node):
    """A standard binary-tree right rotation. Nodes are (label, left, right)."""
    if node is None:
        return None
    label, L, R = node
    if L is None:
        return node
    l_label, LL, LR = L
    return (l_label, LL, (label, LR, R))


def node_labels(node) -> list:
    if node is None:
        return []
    label, L, R = node
    return node_labels(L) + [label] + node_labels(R)


def main() -> int:
    rep = {
        "tool": "ot_paper01_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 01 v0.1 (Neo.K)",
        "scope": (
            "the Claim Ledger's T-class arithmetic, plus external verification of the "
            "cited bibliography against arXiv and Crossref. Not a Collatz proof."
        ),
        "note": "the subject's regression suite contains no Paper 01 test",
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    # ================= Part 1: the ledger's T-class arithmetic =============

    # §4.1 (T): n has a legal ODD predecessor under the original map iff
    # n = 4 (mod 6). Checked against brute-force search for an odd m with
    # 3m + 1 = n, which assumes nothing.
    pred_ok = True
    N = 30000
    for n in range(1, N):
        has_odd_pred = ((n - 1) % 3 == 0) and ((n - 1) // 3) > 0 and ((n - 1) // 3) % 2 == 1
        if has_odd_pred != (n % 6 == 4):
            pred_ok = False
            break
    check("P01_S4_1_odd_predecessor_iff_n_is_4_mod_6", pred_ok)

    # §4.2 (T): that residue class has natural density 1/6.
    hits = sum(1 for n in range(1, 60001) if n % 6 == 4)
    check("P01_S4_2_branch_point_density_is_one_sixth",
          abs(hits / 60000 - 1 / 6) < 1e-4, f"measured {hits/60000:.6f}")

    # §4.3 (T/E): unique odd-core decomposition, and coverage of Z>0 reduces to
    # coverage of the odd integers.
    core_ok = cover_ok = True
    for n in range(1, 20000):
        a, m = v2(n), n // 2 ** v2(n)
        if m % 2 == 0 or 2 ** a * m != n:
            core_ok = False

        def reaches_one(s: int, cap: int = 3000) -> bool:
            x = s
            for _ in range(cap):
                if x == 1:
                    return True
                x = T(x)
            return False

        if reaches_one(n) != reaches_one(m):
            cover_ok = False
    check("P01_S4_3_unique_odd_core_decomposition", core_ok)
    check("P01_S4_3_coverage_reduces_to_the_odd_integers", cover_ok)

    # §5 (E): a trajectory reaches 1 iff it meets a power of two. Under the
    # ORIGINAL map, which is the form §5 states it in.
    pow2_ok = True
    for n in range(1, 20000):
        x, hit_pow2, hit_one = n, False, False
        for _ in range(3000):
            if x & (x - 1) == 0:
                hit_pow2 = True
            if x == 1:
                hit_one = True
                break
            x = col(x)
        if hit_one != hit_pow2:
            pow2_ok = False
    check("P01_S5_reaching_one_iff_meeting_a_power_of_two", pow2_ok)

    # §6.1 (T): exactly v2(n) legal halving steps precede the odd core.
    v2_ok = True
    for n in range(1, 20000):
        steps, x = 0, n
        while x % 2 == 0:
            x //= 2
            steps += 1
        if steps != v2(n) or x % 2 == 0:
            v2_ok = False
    check("P01_S6_1_v2_reduction_gives_exactly_v2_halvings", v2_ok)

    # §111 (N): binary tree rotation preserves the node set, so it cannot change
    # whether the inverse tree covers Z>0. A no-go claim, checked on concrete
    # trees rather than argued.
    rot_ok = True
    trees = [
        ("a", ("b", ("d", None, None), ("e", None, None)), ("c", None, None)),
        ("1", ("2", ("3", ("4", None, None), None), None), None),
        ("x", ("y", None, ("z", None, None)), ("w", ("v", None, None), None)),
    ]
    for t in trees:
        before = sorted(node_labels(t))
        after = sorted(node_labels(rotate_right(t)))
        if before != after:
            rot_ok = False
    check("P01_S111_tree_rotation_preserves_the_node_set", rot_ok)

    # §7.1 (C): the stated Barina milestone ladder, as a monotone sequence of
    # exponents. The 2^71 entry is checked against the live project page below.
    ladder = {2020: 68, 2021: 69, 2023: 70, 2025: 71}
    check("P01_S7_1_barina_ladder_is_monotone_and_ends_at_2_71",
          list(ladder.values()) == sorted(ladder.values()) and max(ladder.values()) == 71)

    # Paper 07's threshold, restated in Paper 01's calibration: the general
    # condition q < p^{p/(p-1)} becomes q < 4 exactly at p = 2.
    from fractions import Fraction
    p = 2
    check("P01_GGM_threshold_at_p_equals_2_is_exactly_4",
          p ** Fraction(p, p - 1) == 4)

    rep["counts"]["arithmetic_domain"] = {"predecessor_scan": N, "orbit_scan": 20000}

    # ================= Part 2: the bibliography, externally ================
    arxiv_ok = True
    bib = {}
    for aid, want in CITED_ARXIV.items():
        path = BIB / want["file"]
        raw = path.read_bytes()
        x = raw.decode("utf-8")
        ent = re.search(r"<entry>(.*?)</entry>", x, re.S)
        if not ent:
            arxiv_ok = False
            bib[aid] = {"error": "no entry in snapshot"}
            continue
        e = ent.group(1)
        title = norm(re.search(r"<title>(.*?)</title>", e, re.S).group(1))
        authors = [norm(a) for a in re.findall(r"<name>(.*?)</name>", e, re.S)]
        published = re.search(r"<published>(.*?)</published>", e, re.S).group(1)[:10]
        jm = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", e, re.S)
        journal = norm(jm.group(1)) if jm else None

        title_ok = norm(want["title"]).lower() == title.lower()
        authors_ok = authors[: len(want["authors"])] == want["authors"]
        journal_ok = ("journal_contains" not in want) or (
            journal is not None and want["journal_contains"].split("(")[0].strip().lower()
            in journal.lower())
        if not (title_ok and authors_ok and journal_ok):
            arxiv_ok = False
        bib[aid] = {
            "url": want["url"],
            "snapshot_sha256": hashlib.sha256(raw).hexdigest()[:32],
            "title_matches": title_ok,
            "authors_match": authors_ok,
            "journal_matches": journal_ok,
            "record_title": title,
            "record_authors": authors,
            "record_published": published,
            "record_journal": journal,
        }
    check("P01_all_cited_arxiv_records_match_title_authors_and_journal", arxiv_ok,
          f"{ {k: v for k, v in bib.items() if not v.get('title_matches', True)} }")
    rep["measured"]["arxiv_records"] = bib

    # Barina 2025, via Crossref
    cr = json.loads((BIB / "crossref_barina_2025.json").read_text(encoding="utf-8"))["message"]
    cr_ok = (
        cr["DOI"] == "10.1007/s11227-025-07337-0"
        and "Improved verification limit" in cr["title"][0]
        and cr["author"][0]["family"] == "Barina"
        and "Journal of Supercomputing" in cr["container-title"][0]
        and cr["volume"] == "81"
        and str(cr.get("article-number") or cr.get("page")) == "810"
    )
    check("P01_barina_2025_doi_matches_the_stated_journal_volume_and_article", cr_ok,
          f"got {cr.get('container-title')} vol {cr.get('volume')} art "
          f"{cr.get('article-number')}")
    rep["measured"]["barina_2025"] = {
        "doi": cr["DOI"],
        "title": cr["title"][0],
        "journal": cr["container-title"][0],
        "volume": cr["volume"],
        "article": cr.get("article-number"),
        "issued": cr.get("published", cr.get("issued", {})).get("date-parts"),
        "url": "https://doi.org/10.1007/s11227-025-07337-0",
    }

    # The live verification frontier, from Barina's own project page
    page = (BIB / "pcbarina_project_page.html").read_text(encoding="utf-8", errors="replace")
    flat = " ".join(re.sub(r"<[^>]+>", " ", page).split())
    frontier_ok = ("2075" in flat and "71.02" in flat) or "2 71" in flat
    check("P01_S7_1_project_page_supports_the_2_71_calibration", frontier_ok,
          "could not find the frontier statement in the snapshot")
    m = re.search(r"convergence of all numbers below ([^.]{0,80})", flat, re.I)
    rep["measured"]["verification_frontier"] = {
        "source": "https://pcbarina.fit.vut.cz/",
        "snapshot_sha256": hashlib.sha256(
            (BIB / "pcbarina_project_page.html").read_bytes()).hexdigest()[:32],
        "statement": norm(m.group(1)) if m else None,
        "supports_2_71": frontier_ok,
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
