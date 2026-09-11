"""Gate 68 — Phase 1's `03` (the standard-library mirror of Algorithm 2) and `13` (the twist JSON's non-monotone line diff), each recomputed against the package and against this tree's own instruments.

數學戰士「墜衡」 / AMRAL Research Lab.

`03_Algorithm2_Independent_Reproduction` gives a point-count formula
(odd p, D_x = (a₁x+a₃)² + 4(x³+a₂x²+a₄x+a₆), #{y} = 1 + χ_p(D_x)), a
2-division cubic 4x³ + b₂x² + 2b₄x + b₆, the claim that for a cubic *no root
mod p ⟺ irreducible ⟺ p inert* once (d, 3N) = 1 has excluded the ramified
primes, and two fixtures: 46a1 → the seven twists 1, 185, 265, 305, 745, 785,
905 and 106d1 → 21. `13_500K_Twist_Output_NonMonotonicity` observes one
commit's diff of the twist JSON as +1899 / −53404 lines, argues twist output
need not be monotone under a shrink (gcd(M,N) → gcd(M,3N)) and an expand (the
deleted disc predicate), warns that 1,899 added LINES are not 1,899 new twists,
and records that the twelve surviving `<150` curves show 0 output deltas.

What this gate computes:

  03 §1   the formula against a brute-force count of (x, y) ∈ F_p² — a
          different computation, not the same one twice — on every base curve
          at every odd prime ≤ 23, with Hasse's bound as a third witness
  03 §4   the cubic in x against this tree's monic form in X = 4x: 16·f(x) = F(4x)
  03 §5   on every Zhai pair of the CURRENT map, every p | d is odd, prime to
          3N, and of good reduction — so the cubic is separable mod p and
          Dedekind applies — and the cubic has no root mod p
  03 §3/6 46a1's seven and 106d1's twenty-one, read from both maps
  13      the line diff, recomputed with git (+1899 / −53404 exactly); the
          entry-level census (0 added, 21,306 removed on the stable base, 24,785
          removed with their base curves); every one of the 1,899 added lines
          classified — all are a deleted line's neighbour losing its trailing
          comma or a line git re-aligned unchanged, none new content; and the
          twelve `<150` survivors' lists, identical in both maps

Usage:  python code/src68_algorithm2_mirror_and_diff.py
"""

from __future__ import annotations

import json
import math
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import src57_theorem_2_18_condition_map as cmap            # noqa: E402
import src65_phase1_closure as closure                     # noqa: E402

LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
OUT = LOGS / "src68-algorithm2-mirror-and-diff.json"

STATED_03_46A1 = [1, 185, 265, 305, 745, 785, 905]
STATED_03_106D1_COUNT = 21
STATED_13_DIFF = (1899, 53404)
ODD_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23)


def _doc(name: str) -> str:
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ------------------------------------------------------------------- 03 §1

def brute_count(ainvs: list[int], p: int) -> int:
    """#E(F_p) by enumerating every (x, y) ∈ F_p² — O(p²), no character sums."""
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    n = 1
    for x in range(p):
        rhs = (x ** 3 + a2 * x * x + a4 * x + a6) % p
        for y in range(p):
            if (y * y + a1 * x * y + a3 * y - rhs) % p == 0:
                n += 1
    return n


def formula_count(ainvs: list[int], p: int) -> int:
    """03 §1 as written: for odd p, 1 + Σ_x (1 + χ_p(D_x)), χ by Euler's criterion."""
    if p == 2:
        raise ValueError("03 §1 states the formula for odd p")
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    n = 1
    for x in range(p):
        dx = ((a1 * x + a3) ** 2 + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % p
        chi = 0 if dx == 0 else (1 if pow(dx, (p - 1) // 2, p) == 1 else -1)
        n += 1 + chi
    return n


def point_count_crosscheck(base: list[dict], primes=ODD_PRIMES, sample: int | None = None) -> dict:
    rows = base if sample is None else base[::max(1, len(base) // sample)]
    checked = disagree = hasse_fail = tree_disagree = 0
    for r in rows:
        for p in primes:
            if p in r["conductor_primes"]:
                continue                       # 03 §2's test is for good primes
            f, b = formula_count(r["ainvs"], p), brute_count(r["ainvs"], p)
            checked += 1
            if f != b:
                disagree += 1
            if (p + 1 - b) ** 2 > 4 * p:                 # Hasse: |a_p| ≤ 2√p
                hasse_fail += 1
            if cmap.point_count(r["ainvs"], p) != b:
                tree_disagree += 1
    return {"curves": len(rows), "primes": list(primes), "pairs_checked": checked,
            "formula_vs_brute_disagreements": disagree,
            "hasse_bound_violations": hasse_fail,
            "this_trees_point_count_vs_brute_disagreements": tree_disagree,
            "formula_defined_at_2": False,
            "agree": disagree == 0 and hasse_fail == 0 and tree_disagree == 0}


# ------------------------------------------------------------------- 03 §4

def cubic_03(ainvs: list[int]) -> tuple[int, int, int, int]:
    """4x³ + b₂x² + 2b₄x + b₆, coefficients high to low, b's as 03 writes them."""
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    return (4, b2, 2 * b4, b6)


def cubic_forms_agree(base: list[dict], xs=(-3, -2, -1, 0, 1, 2, 3)) -> dict:
    """16·f(x) must equal F(4x) where F is this tree's monic cubic in X = 4x."""
    bad = 0
    for r in base:
        c4, c2, c1, c0 = cubic_03(r["ainvs"])
        F = cmap.two_division_cubic(r["ainvs"])          # [16b6, 8b4, b2, 1], low to high
        for x in xs:
            f = c4 * x ** 3 + c2 * x * x + c1 * x + c0
            X = 4 * x
            Fx = F[3] * X ** 3 + F[2] * X * X + F[1] * X + F[0]
            if 16 * f != Fx:
                bad += 1
    return {"curves": len(base), "evaluation_points": list(xs),
            "identity_16f_x_equals_F_4x_failures": bad, "agree": bad == 0}


# ------------------------------------------------------------------- 03 §5

def root_count_mod_p(cubic: tuple[int, int, int, int], p: int) -> int:
    c3, c2, c1, c0 = (c % p for c in cubic)
    return sum(1 for x in range(p) if (c3 * x ** 3 + c2 * x * x + c1 * x + c0) % p == 0)


def inert_hypotheses(base: list[dict], new: dict, sample: int | None = None) -> dict:
    """On every Zhai pair (E, d): each p | d is odd, coprime to 3N, good for E
    (so the cubic is separable mod p and no-root ⟺ irreducible ⟺ inert), and
    the cubic has no root mod p. 03 §5 says (d, 3N) = 1 does this work."""
    by_label = {r["curve_label"]: r for r in base}
    labels = [l for l in new if by_label[l]["source"] == "Zha16_no_2_tors"]
    if sample is not None:
        labels = labels[::max(1, len(labels) // sample)]
    pairs = primes_seen = 0
    even = not_coprime_3N = bad_reduction = has_root = 0
    for l in labels:
        r = by_label[l]
        cub = cubic_03(r["ainvs"])
        for d in new[l]:
            pairs += 1
            if math.gcd(abs(d), 3 * r["conductor"]) != 1:
                not_coprime_3N += 1
            for p in (cmap.prime_factors(abs(d)) if abs(d) != 1 else []):
                primes_seen += 1
                if p == 2:
                    even += 1
                if r["discriminant"] % p == 0:
                    bad_reduction += 1
                if root_count_mod_p(cub, p) != 0:
                    has_root += 1
    return {"zhai_curves": len(labels), "pairs": pairs, "prime_divisors_seen": primes_seen,
            "d_even": even, "gcd_d_3N_not_1": not_coprime_3N,
            "p_dividing_discriminant": bad_reduction, "cubic_has_root_mod_p": has_root,
            "no_root_iff_irreducible_for_degree_3": True,
            "agree": even == 0 and not_coprime_3N == 0 and bad_reduction == 0 and has_root == 0}


# ------------------------------------------------------------------- 03 §3, §6

def fixtures_03(old: dict, new: dict, base: list[dict]) -> dict:
    f00 = closure.fixtures_00(base, new)
    return {"46a1_new": new.get("46a1"), "46a1_old": old.get("46a1"),
            "46a1_stated_03": STATED_03_46A1,
            "46a1_agrees": new.get("46a1") == STATED_03_46A1 == old.get("46a1"),
            "106d1_new_count": len(new.get("106d1", [])), "106d1_old_count": len(old.get("106d1", [])),
            "106d1_stated_03": STATED_03_106D1_COUNT,
            "106d1_agrees": len(new.get("106d1", [])) == STATED_03_106D1_COUNT == len(old.get("106d1", [])),
            "RUN_063_recomputation_agrees": bool(f00.get("agrees", f00.get("both_agree", False))),
            "RUN_063_fixtures_00": {k: v for k, v in f00.items() if not isinstance(v, (list, dict))}}


# ------------------------------------------------------------------- 13

def line_diff() -> dict:
    """git diff --no-index --numstat, the statistic 13 quotes. difflib is not a
    fallback: on 370,000 lines it does not finish, and its alignment would
    not be the one 13 read anyway."""
    try:
        out = subprocess.run(["git", "diff", "--no-index", "--numstat",
                              str(cmap.OLD_MAP), str(cmap.NEW_MAP)],
                             capture_output=True, text=True, check=False).stdout
        added, deleted = (int(x) for x in out.split()[:2])
        how = "git diff --no-index --numstat"
    except (ValueError, FileNotFoundError, IndexError):
        added = deleted = -1
        how = "git unavailable — not computed"
    return {"added_lines": added, "deleted_lines": deleted, "how": how,
            "stated_13": {"added_lines": STATED_13_DIFF[0], "deleted_lines": STATED_13_DIFF[1]},
            "agrees": (added, deleted) == STATED_13_DIFF}


def classify_added_lines() -> dict:
    """Every '+' line of the unified diff: is it a '−' line that lost its
    trailing comma (the neighbour of a deleted last element), or something new?"""
    try:
        out = subprocess.run(["git", "diff", "--no-index", "-U0", str(cmap.OLD_MAP), str(cmap.NEW_MAP)],
                             capture_output=True, text=True, check=False, encoding="utf-8").stdout
    except FileNotFoundError:
        return {"classified": False}
    plus, minus = [], []
    for line in out.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            plus.append(line[1:].strip())
        elif line.startswith("-"):
            minus.append(line[1:].strip())
    minus_set = set(minus)
    comma_drop = sum(1 for s in plus if s + "," in minus_set)
    # the other kind: a line git deleted and re-added unchanged because a
    # neighbouring deletion shifted the alignment — same text, no new content
    realigned = sum(1 for s in plus if s + "," not in minus_set and s in minus_set)
    new_content = [s for s in plus if s + "," not in minus_set and s not in minus_set]
    return {"classified": True, "added_lines": len(plus), "deleted_lines": len(minus),
            "added_lines_that_are_a_deleted_line_minus_its_comma": comma_drop,
            "added_lines_identical_to_a_deleted_line": realigned,
            "added_lines_with_new_content": len(new_content),
            "new_content_sample": new_content[:5],
            "every_added_line_is_a_comma_drop_or_realignment": not new_content}


def entry_census(old: dict, new: dict) -> dict:
    po = {(l, d) for l, ds in old.items() for d in ds}
    pn = {(l, d) for l, ds in new.items() for d in ds}
    added = pn - po
    removed = po - pn
    gone_labels = set(old) - set(new)
    with_base = {(l, d) for l, d in removed if l in gone_labels}
    stable = removed - with_base
    changed = sum(1 for l in new if old[l] != new[l])
    last_dropped = sum(1 for l in new if old[l] and new[l] and old[l][-1] != new[l][-1])
    pkg_removed = _csv_rows(cmap.PKG / "results" / "algorithm2_removed_twists.csv")
    pkg_with_base = _csv_rows(cmap.PKG / "results" / "twists_removed_by_upstream_base_deletion.csv")
    pkg_added = _csv_rows(cmap.PKG / "results" / "algorithm2_added_twists.csv")
    return {"old_keys": len(old), "new_keys": len(new), "keys_removed": len(gone_labels),
            "keys_added": len(set(new) - set(old)),
            "old_pairs": len(po), "new_pairs": len(pn),
            "pairs_added": len(added), "pairs_removed": len(removed),
            "pairs_removed_with_their_base_curve": len(with_base),
            "pairs_removed_on_the_stable_base": len(stable),
            "stable_curves_with_any_twist_removed": changed,
            "stable_curves_whose_last_listed_twist_was_removed": last_dropped,
            "RUN_060_section_7_stable_curves_with_a_removal": 5437,
            "package_csv_rows": {"algorithm2_removed_twists": pkg_removed,
                                 "twists_removed_by_upstream_base_deletion": pkg_with_base,
                                 "algorithm2_added_twists": pkg_added},
            "package_agrees": (pkg_removed == len(stable) and pkg_with_base == len(with_base)
                               and pkg_added == len(added)),
            "monotone_in_fact": not added,
            "RUN_060_stable_base_figures": {"T_O": 268697, "T_C": 247391, "removed": 21306},
            "RUN_060_agrees": len(stable) == 21306 and len(pn) == 247391 and changed == 5437}


def _csv_rows(path: pathlib.Path) -> int:
    if not path.exists():
        return -1
    with path.open(encoding="utf-8") as fh:
        return sum(1 for _ in fh) - 1


def line_accounting(diff: dict, census: dict, classified: dict) -> dict:
    """53,404 deleted lines = removed twist lines + the deleted keys' two
    structural lines each + the comma-drop neighbours; 1,899 added = the
    comma-drop neighbours re-added without their comma."""
    twist_lines = census["pairs_removed"]
    key_lines = 2 * census["keys_removed"]
    comma = classified.get("added_lines_that_are_a_deleted_line_minus_its_comma", 0)
    realigned = classified.get("added_lines_identical_to_a_deleted_line", 0)
    predicted_deleted = twist_lines + key_lines + comma + realigned
    return {"removed_twist_lines": twist_lines, "deleted_keys_x2_structural_lines": key_lines,
            "comma_drop_neighbours": comma, "realigned_lines": realigned,
            "predicted_deleted_lines": predicted_deleted,
            "git_deleted_lines": diff["deleted_lines"],
            "predicted_added_lines": comma + realigned, "git_added_lines": diff["added_lines"],
            "accounts_exactly": predicted_deleted == diff["deleted_lines"]
                                and comma + realigned == diff["added_lines"]}


def fixture_150_deltas(old: dict, new: dict, base: list[dict]) -> dict:
    f = closure.fixture_150(base, new)
    twelve = f["the_twelve"]
    deltas = [l for l in twelve if old.get(l) != new.get(l)]
    return {"the_twelve": twelve, "lists_differ": deltas, "output_deltas": len(deltas),
            "stated_13": 0, "agrees": len(twelve) == 12 and not deltas}


# ------------------------------------------------------------------- main

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    base = cmap.load_base()
    new = cmap.load_new_map()
    old = json.loads(cmap.OLD_MAP.read_text(encoding="utf-8"))
    pc = point_count_crosscheck(base)
    cf = cubic_forms_agree(base)
    ih = inert_hypotheses(base, new)
    fx = fixtures_03(old, new, base)
    ld = line_diff()
    cl = classify_added_lines()
    ec = entry_census(old, new)
    la = line_accounting(ld, ec, cl)
    f150 = fixture_150_deltas(old, new, base)
    ok = (pc["agree"] and cf["agree"] and ih["agree"] and fx["46a1_agrees"] and fx["106d1_agrees"]
          and ld["agrees"] and cl.get("every_added_line_is_a_comma_drop_or_realignment", False)
          and ec["package_agrees"] and ec["monotone_in_fact"] and ec["RUN_060_agrees"]
          and la["accounts_exactly"] and f150["agrees"])
    log = {"gate": "src68 — 03's Algorithm 2 mirror and 13's non-monotone diff, recomputed",
           "source": "03_Algorithm2_Independent_Reproduction.md, 13_500K_Twist_Output_NonMonotonicity.md",
           "docs_found": {"03": bool(_doc("03_Algorithm2_Independent_Reproduction.md")),
                          "13": bool(_doc("13_500K_Twist_Output_NonMonotonicity.md"))},
           "03_point_count_formula_vs_brute_force": pc,
           "03_cubic_vs_this_trees_monic_form": cf,
           "03_inertness_hypotheses_on_every_zhai_pair": ih,
           "03_fixtures": fx,
           "13_line_diff": ld, "13_added_lines_classified": cl, "13_entry_census": ec,
           "13_line_accounting": la, "13_fixture_150_deltas": f150,
           "headline": (f"03's formula agrees with brute force on {pc['pairs_checked']:,} (curve, p) pairs, "
                        f"its cubic is this tree's monic form under X = 4x on all {cf['curves']:,} curves, "
                        f"its inertness hypotheses hold on all {ih['pairs']:,} Zhai pairs, 46a1's seven and "
                        f"106d1's 21 read back from both maps. 13's +{ld['added_lines']:,} / "
                        f"−{ld['deleted_lines']:,} reproduces with git to the line; at entry level "
                        f"{ec['pairs_added']} twists were added and {ec['pairs_removed']:,} removed "
                        f"({ec['pairs_removed_on_the_stable_base']:,} on the stable base, "
                        f"{ec['pairs_removed_with_their_base_curve']:,} with their base curves); every one "
                        f"of the {cl.get('added_lines', 0):,} added lines is a deleted line's neighbour "
                        f"losing its comma ({cl.get('added_lines_that_are_a_deleted_line_minus_its_comma', 0):,}) "
                        f"or a line git re-aligned unchanged ({cl.get('added_lines_identical_to_a_deleted_line', 0)}), "
                        f"none new content; the twelve <150 survivors show {f150['output_deltas']} deltas"),
           "ok": ok}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"  03 §1: {pc['pairs_checked']:,} pairs, formula≠brute {pc['formula_vs_brute_disagreements']}, "
          f"Hasse {pc['hasse_bound_violations']}, tree≠brute {pc['this_trees_point_count_vs_brute_disagreements']}")
    print(f"  03 §4: 16f(x)=F(4x) failures {cf['identity_16f_x_equals_F_4x_failures']} on {cf['curves']:,} curves")
    print(f"  03 §5: {ih['pairs']:,} Zhai pairs, {ih['prime_divisors_seen']:,} p | d: even {ih['d_even']}, "
          f"gcd≠1 {ih['gcd_d_3N_not_1']}, bad {ih['p_dividing_discriminant']}, root {ih['cubic_has_root_mod_p']}")
    print(f"  03 §3/6: 46a1 {fx['46a1_agrees']}, 106d1 {fx['106d1_agrees']}")
    print(f"  13: git +{ld['added_lines']} −{ld['deleted_lines']} ({ld['agrees']}); entries +{ec['pairs_added']} "
          f"−{ec['pairs_removed']:,} = {ec['pairs_removed_on_the_stable_base']:,} stable + "
          f"{ec['pairs_removed_with_their_base_curve']:,} with base; package {ec['package_agrees']}; "
          f"comma-drops {cl.get('added_lines_that_are_a_deleted_line_minus_its_comma')} + realigned "
          f"{cl.get('added_lines_identical_to_a_deleted_line')} of {cl.get('added_lines')}, new content "
          f"{cl.get('added_lines_with_new_content')}; "
          f"accounting {la['accounts_exactly']}; <150 deltas {f150['output_deltas']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
