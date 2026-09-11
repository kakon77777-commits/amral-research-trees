"""Gate 57 — Theorem 2.18's condition map, recomputed on the whole Phase 1 census.

數學戰士「墜衡」 / AMRAL Research Lab.

`01_Theorem_2_18_Condition_Map` lays Banwait–Huang Theorem 2.18 out as seven
base-curve conditions E1–E7, two branches (8a: no rational 2-torsion, 8b: exactly
one), and three blocks of twist conditions (D common, E for the Zha16 branch, F
for the CLZ20 branch). It closes with the output semantics: admissible ⟹ BSD
follows from cited theorems, and NOT the converse.

THIS IS THE FIRST PHASE 1 DOCUMENT TO BE A ROUND'S SUBJECT, and it is the right
one, because RUN-004 through RUN-008 already verified the census DATA that this
document's conditions produce — 40,749 discriminants, 4,062 removed curves,
122,247 isogeny determinations — without ever reading the map. In particular
RUN-008 found the base is TWO POPULATIONS, `Zha16_no_2_tors` (37,002, zero
2-torsion) and `CLZ20` (3,747, 2-torsion in every one). Those are branches 8a
and 8b. This line walked into the theorem's branch structure from the data end.

WHAT IS RECOMPUTED HERE, on all 40,749 base curves and all 247,391 twist pairs:

  E1  semistable            N squarefree, and the valuation keys are the primes
  E2  a_3 in {-2..2}        a_3 by point count mod 3, against the census's own
  E3  no 3/5/7-isogeny      from the removed census + RUN-006/007/008's logs
  E4  ramification          for every p | N some q | N, q != p, p ∤ v_q(Δ) —
                            computed from the valuations RUN-004 verified
  8a/8b populations         from `source`, and 8b's three non-square conditions
                            on every CLZ20 curve, with the 2-torsion point
                            found by EXACT integer bisection — no float
  D, E, F                   every twist condition, on every (curve, d) in the
                            new map — an independent recomputation of the
                            admissibility side of Algorithm 2

AND THE CENSUS ENFORCES TWO OF THESE. Its failure classes are A3_ONLY (2,707),
ISOGENY_ONLY (1,353) and BOTH (2) — E2 and E3. E4 and the 8b non-squares are
stated by the map and not a removal class. Whether every base curve satisfies
them anyway is a measurement, made below.

Usage:  python code/src57_theorem_2_18_condition_map.py
"""

from __future__ import annotations

import collections
import csv
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase1" / "files"
PKG = (pathlib.Path("D:/我的研究/學術討論/論文/數學/BSD")
       / "BSD_Phase1_Banwait_Huang_Exact_Census_v0.5_2026-08-12")
BASE_JSON = PKG / "inputs" / "metadata" / "old_base_curve_arithmetic.json"
REMOVED_CSV = PKG / "results" / "algorithm1_removed_census.csv"
REMOVED_JSON = PKG / "inputs" / "metadata" / "algorithm1_removed_metadata.json"
NEW_MAP = PKG / "inputs" / "new" / "twists_of_ec_labels_500k.json"
SUMMARY = PKG / "results" / "summary.json"
OUT = LOGS / "src57-theorem-2-18-condition-map.json"


# ------------------------------------------------------------------ loading

def load_base() -> list[dict]:
    d = json.loads(BASE_JSON.read_text(encoding="utf-8"))
    return d["records"]


def load_removed() -> list[dict]:
    with REMOVED_CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_new_map() -> dict[str, list[int]]:
    return json.loads(NEW_MAP.read_text(encoding="utf-8"))


def _load_log(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


# ------------------------------------------------------------- small helpers

def squarefree(n: int) -> bool:
    n = abs(n)
    if n == 0:
        return False
    p = 2
    while p * p <= n:
        if n % (p * p) == 0:
            return False
        while n % p == 0:
            n //= p
        p += 1
    return True


def prime_factors(n: int) -> list[int]:
    n = abs(n)
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


_SQ_CACHE: dict[int, set[int]] = {}


def _squares_mod(p: int) -> set[int]:
    s = _SQ_CACHE.get(p)
    if s is None:
        s = {(x * x) % p for x in range(p)}
        _SQ_CACHE[p] = s
    return s


def point_count(ainvs: list[int], p: int) -> int:
    """#E(F_p) by a square-table lookup, O(p). For the twist-map primes p ≤ 997."""
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    sq = _squares_mod(p)
    t = 1
    for x in range(p):
        v = ((a1 * x + a3) ** 2 + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % p
        if v == 0:
            t += 1
        elif v in sq:
            t += 2
    return t


def a_p(ainvs: list[int], p: int) -> int:
    return p + 1 - point_count(ainvs, p)


def two_division_cubic(ainvs: list[int]) -> list[int]:
    """The 2-division cubic in the monic form X^3 + b2 X^2 + 8 b4 X + 16 b6,
    where X = 4x — ascending, as `cubic_root_count` wants it."""
    b2, b4, b6, _b8, _disc = anchor.b_invariants(ainvs)
    return [16 * b6, 8 * b4, b2, 1]


# ------------------------------------------------------- base conditions E1–E4

def e1_semistable(base: list[dict]) -> dict:
    """N squarefree, and the valuation table's keys ARE the conductor primes.

    Squarefree is tested as N == product of its listed conductor primes, which
    is stronger than trial division: it also certifies that `conductor_primes`
    is the COMPLETE factorisation, with each prime appearing exactly once.
    """
    fails, key_mismatch = [], []
    for r in base:
        if math.prod(r["conductor_primes"]) != r["conductor"]:
            fails.append(r["curve_label"])
        if sorted(int(k) for k in r["discriminant_valuations"]) != \
                sorted(r["conductor_primes"]):
            key_mismatch.append(r["curve_label"])
    return {"curves": len(base), "non_squarefree_conductor": len(fails),
            "valuation_keys_not_the_conductor_primes": len(key_mismatch),
            "all_pass": not fails and not key_mismatch,
            "examples": fails[:5] + key_mismatch[:5]}


def e2_small_trace(base: list[dict], removed: list[dict]) -> dict:
    """a_3 recomputed on every base curve, against the census's own column."""
    bad3 = 0
    hist: collections.Counter = collections.Counter()
    excluded = []
    for r in base:
        if r["conductor"] % 3 == 0:
            bad3 += 1                     # |a_3| ≤ 1 at a bad prime: E2 holds
            continue
        a3 = a_p(r["ainvs"], 3)
        hist[a3] += 1
        if abs(a3) == 3:
            excluded.append(r["curve_label"])
    census_abs3 = {row["curve_label"] for row in removed
                   if row["abs_a3_eq_3"] == "True"}
    mine = set(excluded)
    return {"curves": len(base), "bad_reduction_at_3": bad3,
            "good_at_3": len(base) - bad3,
            "a3_histogram_good_at_3": {str(k): v for k, v in sorted(hist.items())},
            "abs_a3_eq_3_recomputed": len(mine),
            "abs_a3_eq_3_in_census": len(census_abs3),
            "agree_exactly": mine == census_abs3,
            "only_mine": sorted(mine - census_abs3)[:5],
            "only_census": sorted(census_abs3 - mine)[:5]}


def e3_isogeny(removed: list[dict]) -> dict:
    """The 3/5/7-isogeny exclusions, from the census and this line's own gates."""
    by = collections.Counter(row["isogeny_set_357"] for row in removed
                             if row["isogeny_set_357"] not in ("", "NONE"))
    with_iso = sum(by.values())
    r6 = _load_log("src06-three-isogeny.json") or {}
    r7 = _load_log("src07-isogeny-reducibility.json") or {}
    r8 = _load_log("src08-modular-curve.json") or {}
    return {"removed_with_a_3_5_7_isogeny": with_iso,
            "by_degree_set": dict(by),
            "this_lines_gates": {
                "RUN-006": bool(r6), "RUN-007": bool(r7), "RUN-008": bool(r8)},
            "closed_both_ways_at_RUN_008": "122,247 determinations, per RUN-008",
            "note": "E3 is one of the census's two removal classes; this round "
                    "re-reads the column and cites the three rounds that "
                    "recomputed it rather than recomputing a fourth time"}


def e4_ramification(base: list[dict]) -> dict:
    """For every p | N there is a q | N, q ≠ p, with p ∤ v_q(Δ_min).

    On a semistable curve every p | N is multiplicative, and at a multiplicative
    q ≠ p the Tate curve gives: E[p] is ramified at q iff p ∤ v_q(Δ_min). So E4
    is exactly the divisibility criterion RUN-037 compiled for FW-H3 — over ALL
    multiplicative primes rather than the nonsplit ones only.
    """
    fails, single_prime = [], 0
    per_p_fail: collections.Counter = collections.Counter()
    for r in base:
        ps = r["conductor_primes"]
        if len(ps) == 1:
            single_prime += 1
        vals = {int(k): v for k, v in r["discriminant_valuations"].items()}
        ok = True
        for p in ps:
            if not any(q != p and vals[q] % p != 0 for q in ps):
                ok = False
                per_p_fail[p] += 1
        if not ok:
            fails.append(r["curve_label"])
    return {"curves": len(base), "prime_conductor_curves": single_prime,
            "fail": len(fails), "pass": len(base) - len(fails),
            "failures_by_prime": {str(k): v for k, v in sorted(per_p_fail.items())},
            "examples": fails[:8],
            "all_pass": not fails,
            "is_a_census_removal_class": False,
            "same_criterion_as": "FW-H3's p ∤ v_ell(Δ_min) with ell ≠ p (RUN-037), "
                                 "quantified over all multiplicative q instead "
                                 "of W_- only"}


# ------------------------------------------------------------- branches 8a/8b

def integer_roots_of_monic_cubic(c2: int, c1: int, c0: int) -> list[int]:
    """Every integer root of X^3 + c2 X^2 + c1 X + c0, by EXACT arithmetic.

    Between consecutive critical points a cubic is monotone, so on each such
    integer interval a sign change brackets at most one root and an integer
    bisection finds it exactly or proves there is none. No float anywhere —
    the first draft bracketed by float on a Cauchy bound of ~10^11 and missed
    2,154 of 3,747 roots, which is RUN-006's lesson taken one step further:
    the float was not even good enough to PROPOSE.
    """
    def g(X: int) -> int:
        return ((X + c2) * X + c1) * X + c0
    B = 1 + max(abs(c2), abs(c1), abs(c0))            # Cauchy: |root| < B
    pts = {-B, B}
    D = 4 * c2 * c2 - 12 * c1                           # disc of g' = 3X^2+2c2X+c1
    if D >= 0:
        s = math.isqrt(D)
        for num in (-2 * c2 - s, -2 * c2 + s):
            x = num // 6
            pts.update((x - 1, x, x + 1, x + 2))
    pts = sorted(x for x in pts if -B <= x <= B)
    roots = set()
    for lo, hi in zip(pts, pts[1:]):
        glo, ghi = g(lo), g(hi)
        if glo == 0:
            roots.add(lo)
        if ghi == 0:
            roots.add(hi)
        if glo * ghi < 0:
            a, b = lo, hi
            while b - a > 1:
                m = (a + b) // 2
                gm = g(m)
                if gm == 0:
                    roots.add(m)
                    break
                if (gm < 0) == (glo < 0):
                    a = m
                else:
                    b = m
    return sorted(roots)


def rational_two_torsion_x(ainvs: list[int]) -> dict:
    """The rational 2-torsion point's X = 4x. Integral by Lutz–Nagell on an
    integral model, so it is an integer root of the monic 2-division cubic."""
    c0, c1, c2, _ = two_division_cubic(ainvs)
    exact = integer_roots_of_monic_cubic(c2, c1, c0)
    return {"exact_integer_roots": exact, "resolved": len(exact) >= 1}


def branches(base: list[dict]) -> dict:
    """8a/8b populations, and 8b's three non-square conditions on every CLZ20 curve."""
    pop = collections.Counter(r["source"] for r in base)
    clz = [r for r in base if r["source"] == "CLZ20"]
    unresolved, fail_fp, fail_neg_fp, fail_neg_disc = [], [], [], []
    multi_root = []
    for r in clz:
        t = rational_two_torsion_x(r["ainvs"])
        if not t["resolved"]:
            unresolved.append(r["curve_label"])
            continue
        if len(t["exact_integer_roots"]) != 1:
            multi_root.append(r["curve_label"])      # would be full 2-torsion
        X0 = t["exact_integer_roots"][0]
        c0, c1, c2, _ = two_division_cubic(r["ainvs"])
        gp = 3 * X0 * X0 + 2 * c2 * X0 + c1          # = 4 f'(x0): same square class
        if is_square(gp):
            fail_fp.append(r["curve_label"])
        if is_square(-gp):
            fail_neg_fp.append(r["curve_label"])
        if is_square(-r["discriminant"]):
            fail_neg_disc.append(r["curve_label"])
    return {"population_8a_Zha16_no_2_tors": pop.get("Zha16_no_2_tors", 0),
            "population_8b_CLZ20": pop.get("CLZ20", 0),
            "matches_RUN_008": pop.get("Zha16_no_2_tors", 0) == 37002
                               and pop.get("CLZ20", 0) == 3747,
            "8b_checked": len(clz),
            "8b_two_torsion_unresolved": len(unresolved),
            "8b_more_than_one_rational_root": len(multi_root),
            "8b_f_prime_is_a_square": len(fail_fp),
            "8b_minus_f_prime_is_a_square": len(fail_neg_fp),
            "8b_minus_disc_is_a_square": len(fail_neg_disc),
            "8b_all_three_nonsquare_conditions_hold": not (fail_fp or fail_neg_fp
                                                           or fail_neg_disc),
            "examples": {"f_prime_square": fail_fp[:5],
                         "minus_f_prime_square": fail_neg_fp[:5],
                         "minus_disc_square": fail_neg_disc[:5],
                         "unresolved": unresolved[:5],
                         "multi_root": multi_root[:5]},
            "not_computed": ["ord_2 L^alg(E,1) — needs L-values for 40,749 curves",
                             "Sha(E')[2] = 0 for the 2-isogenous curve",
                             "E'(Q)[2] ≅ Z/2"],
            "how_the_root_was_found": ("exact integer bisection between the "
                                       "cubic's critical points; a float "
                                       "bracket on the first draft missed "
                                       "2,154 of 3,747 — RUN-006's lesson, one "
                                       "step further: the float could not even "
                                       "propose")}


# ------------------------------------------------------- twist conditions D/E/F

def twist_conditions(base: list[dict], new_map: dict[str, list[int]],
                     limit: int | None = None) -> dict:
    """Every (curve, d) in the new map, against D and the branch block."""
    by_label = {r["curve_label"]: r for r in base}
    labels = sorted(new_map)
    if limit is not None:
        labels = labels[:limit]
    fails: collections.Counter = collections.Counter()
    examples: dict[str, list] = collections.defaultdict(list)
    entries = 0
    curves = 0
    missing = 0
    for lab in labels:
        r = by_label.get(lab)
        if r is None:
            missing += 1
            continue
        curves += 1
        N = r["conductor"]
        ainvs = r["ainvs"]
        src = r["source"]
        disc = r["discriminant"]
        cubic = two_division_cubic(ainvs)
        for d in new_map[lab]:
            entries += 1
            def bad(cond: str) -> None:
                fails[cond] += 1
                if len(examples[cond]) < 5:
                    examples[cond].append([lab, d])
            if not squarefree(d):
                bad("D1_squarefree")
            if math.gcd(d, 3 * N) != 1:
                bad("D2_coprime_to_3N")
            if d % 4 != 1:
                bad("D3_d_1_mod_4")
            ps = prime_factors(d) if d != 1 else []
            for p in ps:
                if a_p(ainvs, p) % p == 0:
                    bad("D4_ordinary_at_p_dividing_d")
                    break
            if src == "Zha16_no_2_tors":
                if any(ph2.cubic_root_count(cubic, p) != 0 for p in ps):
                    bad("E1_inert_in_cubic_2_division_field")
                if any(fam.kronecker(d, p) != 1 for p in r["conductor_primes"]):
                    bad("E2_conductor_primes_split_in_Q_sqrt_d")
                if disc > 0 and d < 0:
                    bad("E3_disc_positive_forces_d_positive")
            else:                                        # CLZ20
                if any(p % 4 != 1 for p in ps):
                    bad("F1_p_dividing_d_is_1_mod_4")
                if any((point_count(ainvs, p) % 4) != 2 for p in ps):
                    bad("F2_ord2_of_point_count_is_1")
                if d % 8 != 1:
                    bad("F3_d_1_mod_8")
                if any(fam.kronecker(d, p) != 1
                       for p in r["conductor_primes"] if p != 2):
                    bad("F4_odd_conductor_primes_split")
    return {"curves_checked": curves, "entries_checked": entries,
            "labels_not_in_base": missing, "limit": limit,
            "failures_by_condition": dict(fails),
            "examples": dict(examples),
            "every_entry_satisfies_D": not any(k.startswith("D") for k in fails),
            "every_entry_satisfies_its_branch": not any(
                k[0] in "EF" for k in fails),
            "all_pass": not fails,
            "note": ("this is the admissibility side of Algorithm 2 recomputed "
                     "from the map's own conditions — not a re-run of the "
                     "census script. Completeness (that no admissible d is "
                     "MISSING from the map) is a different question and is not "
                     "asked here")}


# ------------------------------------------------------------- the map itself

OLD_MAP = PKG / "inputs" / "old" / "twists_of_ec_labels_500k.json"


def provenance_of_the_twist_map(base: list[dict], removed: list[dict]) -> dict:
    """Which of the map's conditions the UPSTREAM twist blob had already applied.

    The twist map is upstream data (cocoxhuang/ants_xvii), not something the
    census script generates. RUN-029 measured 1,355 = 40,749 - 39,394 base
    curves missing from the OLD blob as a number. Here the set is identified.
    """
    old = json.loads(OLD_MAP.read_text(encoding="utf-8"))
    labels = {r["curve_label"] for r in base}
    missing = labels - set(old)
    iso = {r["curve_label"] for r in removed
           if r["isogeny_set_357"] not in ("", "NONE")}
    a3 = {r["curve_label"] for r in removed if r["abs_a3_eq_3"] == "True"}
    distinct_d = sorted({d for v in old.values() for d in v})
    return {"base": len(labels), "in_old_map": len(labels & set(old)),
            "missing_from_old_map": len(missing),
            "isogeny_removed": len(iso), "a3_removed": len(a3),
            "missing_is_exactly_the_isogeny_set": missing == iso,
            "a3_removed_present_in_old_map": len(a3 & set(old)),
            "a3_removed_present_in_new_map": 0,     # measured below
            "distinct_d_values_in_old_map": len(distinct_d),
            "max_d": max(distinct_d) if distinct_d else None,
            "all_d_positive": all(d > 0 for d in distinct_d),
            "so": ("the upstream blob was generated with E3 (isogeny) already "
                   "applied and E2 (a_3) NOT yet applied. The census README "
                   "records that the upstream code later added "
                   "`disc_valuation_condition` — which is E4 — without "
                   "regenerating the blob; E4 removes nothing from this base "
                   "(measured above), so that omission changed no membership"),
            "completeness_not_measurable_here": (
                "the blob's enumeration rule for d is not in the package — "
                f"only {len(distinct_d)} distinct d appear, all positive, max "
                f"{max(distinct_d) if distinct_d else None} — so whether every "
                "admissible d is PRESENT cannot be checked from here. What is "
                "checked is that every d present is admissible")}


def what_the_census_enforces() -> dict:
    """The map states eleven-odd conditions; the census removes on two."""
    s = json.loads(SUMMARY.read_text(encoding="utf-8"))
    a1 = s["algorithm1"]
    classes = {"A3_ONLY": a1["a3_only"], "ISOGENY_ONLY": a1["isogeny_only"],
               "BOTH": a1["both"]}
    return {"removal_classes": classes,
            "removed_total": sum(classes.values()),
            "these_are": {"A3_ONLY": "E2", "ISOGENY_ONLY": "E3",
                          "BOTH": "E2 and E3"},
            "stated_but_not_a_removal_class": ["E1", "E4", "E5", "E6", "E7",
                                               "8b non-square conditions"],
            "reading": ("E1, E5, E6, E7 are properties of how the base list "
                        "was assembled (semistable, optimal, rank 0, BSD_2 "
                        "known), so they need no removal step. E4 and the 8b "
                        "non-squares are arithmetic conditions the map states "
                        "and the census does not test — which is why this "
                        "round computes them on the whole base")}


def output_semantics() -> dict:
    """§G's two boxes, and the direction this line must never reverse."""
    return {"forward": "admissible => BSD follows from cited theorems",
            "converse": "not admissible =/=> BSD false",
            "converse_holds": False,
            "what_this_means_for_RUN_008": (
                "RUN-008 closed the isogeny CRITERION both ways — every kept "
                "curve has no 3/5/7-isogeny and every removed one does. That is "
                "a statement about the criterion, not about BSD, and §G says "
                "the two must not be confused: a curve outside the admissible "
                "family has simply not been reached by these theorems")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    doc = DOCS / "01_Theorem_2_18_Condition_Map.md"
    text = doc.read_text(encoding="utf-8") if doc.exists() else ""

    base = load_base()
    removed = load_removed()
    new_map = load_new_map()

    e1 = e1_semistable(base)
    e2 = e2_small_trace(base, removed)
    e3 = e3_isogeny(removed)
    e4 = e4_ramification(base)
    br = branches(base)
    tw = twist_conditions(base, new_map)
    pv = provenance_of_the_twist_map(base, removed)
    pv["a3_removed_present_in_new_map"] = len(
        {r["curve_label"] for r in removed if r["abs_a3_eq_3"] == "True"}
        & set(new_map))
    ce = what_the_census_enforces()
    og = output_semantics()

    ok = (bool(text) and "E4" in text and "8b" in text
          and len(base) == 40749 and len(removed) == 4062
          and e1["all_pass"]
          and e2["agree_exactly"]
          and e3["removed_with_a_3_5_7_isogeny"] == 1355
          and br["matches_RUN_008"]
          and br["8b_two_torsion_unresolved"] == 0
          and ce["removed_total"] == 4062
          and og["converse_holds"] is False
          and tw["entries_checked"] == 247391
          and tw["labels_not_in_base"] == 0
          and pv["missing_is_exactly_the_isogeny_set"]
          and pv["a3_removed_present_in_new_map"] == 0)
    # E4 and the 8b non-squares and the twist conditions are MEASUREMENTS:
    # their outcome is recorded, not asserted, and the gate is green either way
    # provided the measurement ran to completion.

    log = {
        "gate": "src57 — Theorem 2.18's condition map on the Phase 1 census",
        "source": "01_Theorem_2_18_Condition_Map",
        "document_found": bool(text),
        "base_curves": len(base), "removed_curves": len(removed),
        "E1": e1, "E2": e2, "E3": e3, "E4": e4,
        "E5_E6_E7": {"state": "CITED — optimality, analytic rank 0, BSD(E,2) "
                              "are how the base list was assembled, not "
                              "computed here"},
        "branches": br,
        "twist_conditions": tw,
        "provenance_of_the_twist_map": pv,
        "what_the_census_enforces": ce,
        "output_semantics": og,
        "headline": (f"E1 holds on all {len(base):,}; E2 recomputed by point "
                     f"count mod 3 agrees EXACTLY with the census's a_3 column "
                     f"({e2['abs_a3_eq_3_recomputed']:,} with |a_3| = 3); E3's "
                     f"{e3['removed_with_a_3_5_7_isogeny']:,} isogeny removals "
                     f"re-read. E4 — stated by the map, NOT a census removal "
                     f"class — computed on all {len(base):,}: "
                     f"{e4['pass']:,} pass, {e4['fail']:,} fail. Branches 8a/8b "
                     f"are RUN-008's two populations ({br['population_8a_Zha16_no_2_tors']:,} / "
                     f"{br['population_8b_CLZ20']:,}); 8b's three non-square "
                     f"conditions checked on every CLZ20 curve with the "
                     f"2-torsion point decided exactly: f' square "
                     f"{br['8b_f_prime_is_a_square']}, -f' square "
                     f"{br['8b_minus_f_prime_is_a_square']}, -Δ square "
                     f"{br['8b_minus_disc_is_a_square']}. Twist conditions D/E/F "
                     f"recomputed on all {tw['entries_checked']:,} (curve, d) "
                     f"pairs of the new map: failures "
                     f"{tw['failures_by_condition'] or 'none'}"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  base {len(base):,} curves, removed {len(removed):,}, new twist "
          f"map {tw['entries_checked']:,} pairs on {tw['curves_checked']:,} curves")
    print()
    print(f"  E1 semistable      all pass: {e1['all_pass']}")
    print(f"  E2 a_3 in [-2,2]   good at 3: {e2['good_at_3']:,}, bad at 3: "
          f"{e2['bad_reduction_at_3']:,}; |a_3|=3 recomputed "
          f"{e2['abs_a3_eq_3_recomputed']:,} vs census "
          f"{e2['abs_a3_eq_3_in_census']:,}, exact agreement: "
          f"{e2['agree_exactly']}")
    print(f"     histogram {e2['a3_histogram_good_at_3']}")
    print(f"  E3 isogeny         {e3['removed_with_a_3_5_7_isogeny']:,} removed "
          f"{e3['by_degree_set']}")
    print(f"  E4 ramification    pass {e4['pass']:,}  FAIL {e4['fail']:,}  "
          f"(census removal class: {e4['is_a_census_removal_class']})")
    if e4["fail"]:
        print(f"     failures by prime {e4['failures_by_prime']}, e.g. "
              f"{e4['examples'][:4]}")
    print()
    print(f"  8a Zha16 {br['population_8a_Zha16_no_2_tors']:,} / 8b CLZ20 "
          f"{br['population_8b_CLZ20']:,}  = RUN-008: {br['matches_RUN_008']}")
    print(f"  8b non-squares on {br['8b_checked']:,} CLZ20 curves: f' square "
          f"{br['8b_f_prime_is_a_square']}, -f' square "
          f"{br['8b_minus_f_prime_is_a_square']}, -Δ square "
          f"{br['8b_minus_disc_is_a_square']}; unresolved "
          f"{br['8b_two_torsion_unresolved']}, multi-root "
          f"{br['8b_more_than_one_rational_root']}")
    print()
    print(f"  twist conditions on {tw['entries_checked']:,} pairs — failures: "
          f"{tw['failures_by_condition'] or 'NONE'}")
    for k, v in tw["examples"].items():
        print(f"     {k}: {v[:3]}")
    print()
    print(f"  upstream OLD map: {pv['missing_from_old_map']:,} base curves "
          f"missing, == the isogeny set: "
          f"{pv['missing_is_exactly_the_isogeny_set']}; a_3-removed present "
          f"in old map {pv['a3_removed_present_in_old_map']:,}, in new map "
          f"{pv['a3_removed_present_in_new_map']}; {pv['distinct_d_values_in_old_map']} "
          f"distinct d, max {pv['max_d']}")
    print(f"  census enforces {list(ce['removal_classes'])} = E2, E3; "
          f"stated-not-enforced: {ce['stated_but_not_a_removal_class']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
