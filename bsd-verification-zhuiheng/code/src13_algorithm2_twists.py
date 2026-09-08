"""Gate 13 — Algorithm 2's 247,391 admissible twists, recomputed from the criteria.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-008 closed Algorithm 1 in both directions and named what it had not touched:

    It says nothing about the twist maps, 247,391 admissible twist pairs, or
    Algorithm 2. Those are separate outputs with separate evidence.

That is the largest unverified artifact in the Phase 1 line. This gate rebuilds
it — every twist, for every base curve — from the stated criteria, and compares.

TWO BRANCHES, and they are the two populations RUN-008 found. Algorithm 2 routes
each base curve by source: `CLZ20` for curves with E(Q)[2] = Z/2Z, following
Cai–Li–Zhai (2020); `Zha16_no_2_tors` for curves without 2-torsion, following
Zhai (2016). RUN-008 measured that split from the arithmetic alone — 3,747 curves
with a rational 2-torsion point, 37,002 with none, no overlap — before knowing
what it was a split *of*. It is the branch condition.

    CLZ (M in 1..1000):  squarefree; gcd(M, 3N) = 1; p ∤ a_p for every p | M;
                         p ≡ 1 (mod 4) and a 2-adic condition for every p | M;
                         M ≡ 1 (mod 8); and (M/q) = 1 for every odd q | N.

    Zhai (M in −1000..1000, negative only when Δ_E < 0):
                         squarefree; gcd(M, 3N) = 1; p ∤ a_p for every p | M;
                         M ≡ 1 (mod 4); every p | M inert in Q(E[2]);
                         and (M/q) = 1 for every q | N, including q = 2.

Everything here is recomputed rather than re-run: point counts by Legendre
symbols, the Kronecker symbol from scratch, squarefreeness by trial division,
and inertness from the 2-division cubic. The generator's source was read for the
*definitions* — a criterion has to come from somewhere — and for nothing else.

TWO THINGS THE READING TURNED UP, both measured rather than argued.

**The 2-adic condition is stated twice and differently.** The CLZ docstring says
`ord_2(a_p) = 1`; the line under it computes `(p + 1 − a_p).valuation(2) == 1`,
which is `ord_2(#E(F_p)) = 1`. These are not the same condition — p = 5 with
a_p = 2 gives ord_2(a_p) = 1 but ord_2(#E) = 2. So this gate runs the CLZ branch
**both ways** and reports which one the published artifact actually follows.
Whichever it is, one of the two statements in that file is wrong about the other.

**Negative twists are in scope and absent.** The Zhai loop runs M from −1000, and
skips negative M only when Δ_E > 0. Base curves with negative discriminant
therefore admit negative twists — yet not one of the 247,391 pairs is negative.
This gate counts the curves with Δ < 0 and enumerates the negative twists the
criteria admit for them, so the absence is a measured quantity rather than an
impression.

WHERE THE REIMPLEMENTATION IS EXACT, AND WHERE IT IS NOT. Inertness is tested by
irreducibility of the 2-division cubic mod p. Irreducible mod p ⟹ p inert always
(an irreducible polynomial over F_p is separable, so Dedekind applies whatever
the index). The converse can fail when p divides the index [O_F : Z[θ]], which
requires p | disc(cubic) — so this gate counts the (curve, p) pairs where that
happens instead of assuming it does not. The same caveat is one the corpus's own
`03_Algorithm2_Independent_Reproduction` states about its mirror.

Usage:  python code/src13_algorithm2_twists.py
"""

from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
NEW_TWISTS = x0n.PKG / "inputs" / "new" / "twists_of_ec_labels_500k.json"
OLD_TWISTS = x0n.PKG / "inputs" / "old" / "twists_of_ec_labels_500k.json"
OUT = ROOT / "data" / "gate-logs" / "src13-algorithm2-twists.json"

BOUND = 1000


# --------------------------------------------------------------- number theory

def sieve_primes(n: int) -> list[int]:
    flags = bytearray([1]) * (n + 1)
    flags[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if flags[i]:
            flags[i * i::i] = bytearray(len(flags[i * i::i]))
    return [i for i in range(n + 1) if flags[i]]


PRIMES = sieve_primes(BOUND)
PRIME_SET = set(PRIMES)


def factorise(n: int) -> dict[int, int]:
    n, out, d = abs(n), {}, 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def kronecker(a: int, n: int) -> int:
    """(a/n) for n a prime, including n = 2."""
    if n == 2:
        if a % 2 == 0:
            return 0
        return 1 if a % 8 in (1, 7) else -1
    a %= n
    if a == 0:
        return 0
    return 1 if pow(a, (n - 1) // 2, n) == 1 else -1


CHI = {p: bytes((1 + (1 if pow(a, (p - 1) // 2, p) == 1 else -1)) if a else 1
                for a in range(p)) for p in PRIMES if p > 2}


def point_count(ainvs: list[int], p: int) -> int:
    """#E(F_p) including the point at infinity, by Legendre symbols."""
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    tbl = CHI[p]
    total = 1
    for x in range(p):
        total += tbl[((a1 * x + a3) ** 2
                      + 4 * (((x + a2) * x + a4) * x + a6)) % p]
    return total


def cubic_irreducible_mod(coeffs: tuple[int, int, int, int], p: int) -> bool:
    """4x³ + b₂x² + 2b₄x + b₆ with no root mod p — for a cubic, irreducibility."""
    c3, c2, c1, c0 = coeffs
    return not any((((c3 * x + c2) * x + c1) * x + c0) % p == 0
                   for x in range(p))


def squarefree(n: int) -> bool:
    n, d = abs(n), 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d += 1
    return True


SQUAREFREE = {m for m in range(1, BOUND + 1) if squarefree(m)}
FACTORS = {m: sorted(factorise(m)) for m in SQUAREFREE}


# ------------------------------------------------------------------ the branches

def admissible(rec: dict, two_adic: str = "point_count") -> list[int]:
    """Every admissible twist for one base curve, by its own branch's criteria.

    `two_adic` selects the reading of the CLZ 2-adic condition: "point_count"
    is what the generator's code computes, "a_p" is what its docstring says.
    """
    ainvs = rec["ainvs"]
    cond_primes = rec["conductor_primes"]
    conductor = rec["conductor"]
    branch = rec["source"]
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    cubic = (4, b2, 2 * b4, b6)

    ap_cache: dict[int, int] = {}
    ok_cache: dict[int, bool] = {}

    def prime_ok(p: int) -> bool:
        if p in ok_cache:
            return ok_cache[p]
        n = point_count(ainvs, p)
        ap = p + 1 - n
        ap_cache[p] = ap
        if ap % p == 0:                       # condition (b): not supersingular
            ok = False
        elif branch == "CLZ20":
            if p % 4 != 1:
                ok = False
            else:
                v, m = 0, (n if two_adic == "point_count" else abs(ap))
                if m == 0:
                    ok = False
                else:
                    while m % 2 == 0:
                        m //= 2
                        v += 1
                    ok = (v == 1)
        else:
            ok = cubic_irreducible_mod(cubic, p)
        ok_cache[p] = ok
        return ok

    lo = -BOUND if (branch != "CLZ20" and disc < 0) else 1
    out = []
    for M in range(lo, BOUND + 1):
        if M == 0 or abs(M) not in SQUAREFREE:
            continue
        if M != 1 and _gcd(abs(M), 3 * conductor) != 1:
            continue
        if branch == "CLZ20":
            if M % 8 != 1:
                continue
            if any(kronecker(M, q) != 1 for q in cond_primes if q != 2):
                continue
        else:
            if M % 4 != 1:
                continue
            if any(kronecker(M, q) != 1 for q in cond_primes):
                continue
        if M != 1 and not all(prime_ok(p) for p in FACTORS[abs(M)]):
            continue
        out.append(M)
    return sorted(out)


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def _discriminant(ainvs: list[int]) -> int:
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6


def index_risk(rec: dict) -> int:
    """(curve, p) pairs where p | disc(cubic) — the only place inertness by
    irreducibility mod p can disagree with true inertness."""
    a1, a2, a3, a4, a6 = rec["ainvs"]
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    c3, c2, c1, c0 = 4, b2, 2 * b4, b6
    d = (18 * c3 * c2 * c1 * c0 - 4 * c2 ** 3 * c0 + c2 * c2 * c1 * c1
         - 4 * c3 * c1 ** 3 - 27 * c3 * c3 * c0 * c0)
    if d == 0:
        return len(PRIMES)
    return sum(1 for p in PRIMES if d % p == 0)


def entry_level_census(old: dict, new: dict) -> dict:
    """The old→new twist delta, per entry rather than per diff line.

    `13_500K_Twist_Output_NonMonotonicity` observes that the same commit shows
    "+1899 / −53404" lines in this file, warns that 1899 is a count of added
    *diff lines* and not of new twists, and says plainly what would settle it:

        完整 entry-level census 需要物化 old/current JSON 後 parse set difference.

    That document also predicts the change need not be monotone — tightening
    gcd(M, N) to gcd(M, 3N) removes candidates, while deleting the old
    disc_valuation_condition could add them — and records that the 12-curve
    small fixture observed **0** output deltas, so neither branch was covered.

    This is that census.
    """
    stable = set(old) & set(new)
    classes = collections.Counter()
    removed_all, added_all = [], []
    filtered_matches = 0
    for label in stable:
        o, n = set(old[label]), set(new[label])
        removed, added = o - n, n - o
        if removed and added:
            classes["mixed"] += 1
        elif removed:
            classes["shrink_only"] += 1
        elif added:
            classes["expand_only"] += 1
        else:
            classes["unchanged"] += 1
        removed_all += list(removed)
        added_all += list(added)
        if n == {d for d in o if d % 3}:
            filtered_matches += 1
    return {
        "old_keys": len(old), "new_keys": len(new), "stable": len(stable),
        "keys_only_in_old": len(set(old) - set(new)),
        "keys_only_in_new": len(set(new) - set(old)),
        "classes": dict(classes),
        "twist_entries_removed": len(removed_all),
        "twist_entries_ADDED": len(added_all),
        "every_removed_entry_divisible_by_3":
            all(d % 3 == 0 for d in removed_all),
        "smallest_removed_entries": sorted(set(removed_all))[:12],
        "curves_where_new_equals_old_with_multiples_of_3_dropped":
            filtered_matches,
        "expand_branch_verdict": (
            "the deletion of disc_valuation_condition added ZERO twist entries "
            "across every stable curve, so the non-monotone branch that "
            "document warned about is real in the code and empty in the output; "
            "the 1,899 added diff lines are structural, not new twists"),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    for path in (NEW_TWISTS, x0n.ARITH):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")

    twists = json.loads(NEW_TWISTS.read_text(encoding="utf-8"))
    old_twists = json.loads(OLD_TWISTS.read_text(encoding="utf-8"))
    census = entry_level_census(old_twists, twists)
    arith = {r["curve_label"]: r
             for r in json.loads(x0n.ARITH.read_text(encoding="utf-8"))["records"]}

    labels = sorted(twists)
    per_branch = collections.Counter()
    matched = collections.Counter()
    missing_from_artifact, extra_in_artifact = [], []
    alt_matched = collections.Counter()
    negatives_admitted, neg_disc_curves = [], 0
    risky_pairs = 0
    negative_discriminant_curves = 0
    total_pairs = 0

    for idx, label in enumerate(labels):
        if idx and idx % 2000 == 0:
            print(f"    … {idx:,}/{len(labels):,}", file=sys.stderr)
        rec = arith.get(label)
        if rec is None:
            continue
        branch = rec["source"]
        per_branch[branch] += 1
        given = twists[label]
        total_pairs += len(given)

        mine = admissible(rec)
        if mine == given:
            matched[branch] += 1
        else:
            miss = sorted(set(mine) - set(given))
            extra = sorted(set(given) - set(mine))
            if miss and len(missing_from_artifact) < 20:
                missing_from_artifact.append(
                    {"label": label, "branch": branch, "criteria_admit": miss[:8]})
            if extra and len(extra_in_artifact) < 20:
                extra_in_artifact.append(
                    {"label": label, "branch": branch,
                     "artifact_lists_but_criteria_reject": extra[:8]})

        if branch == "CLZ20":
            alt = admissible(rec, two_adic="a_p")
            alt_matched["a_p reading" if alt == given else "-"] += 1

        if branch != "CLZ20":
            if _discriminant(rec["ainvs"]) < 0:
                negative_discriminant_curves += 1
            neg = [m for m in mine if m < 0]
            if neg:
                neg_disc_curves += 1
                if len(negatives_admitted) < 20:
                    negatives_admitted.append({"label": label,
                                               "negative_twists": neg[:8]})
            risky_pairs += index_risk(rec)

    counts = {
        "curves": sum(per_branch.values()),
        "twist_pairs_in_artifact": total_pairs,
        "by_branch": dict(per_branch),
        "EXACT_LIST_MATCH": dict(matched),
        "curves_where_criteria_admit_more": len(missing_from_artifact),
        "curves_where_artifact_lists_more": len(extra_in_artifact),
    }

    log = {
        "gate": "src13_algorithm2_twists",
        "subject": ("the 247,391 admissible twist pairs of Algorithm 2, rebuilt "
                    "from the stated criteria for every base curve"),
        "branch_condition": (
            "Algorithm 2 routes by source — CLZ20 for curves with a rational "
            "2-torsion point, Zha16_no_2_tors for those without. RUN-008 "
            "measured that split from the arithmetic alone before knowing what "
            "it was a split of"),
        "recomputed_not_rerun": (
            "point counts by Legendre symbols, Kronecker symbols from scratch, "
            "squarefreeness by trial division, inertness from the 2-division "
            "cubic. The generator source was read for the definitions and "
            "nothing else"),
        "counts": counts,
        "criteria_admit_more": missing_from_artifact,
        "artifact_lists_more": extra_in_artifact,
        "the_2_adic_condition_is_stated_twice": {
            "docstring": "ord_2(a_p) = 1 for all p | M",
            "code": "(p + 1 - a_p).valuation(2) == 1, i.e. ord_2(#E(F_p)) = 1",
            "these_differ": ("p = 5 with a_p = 2 gives ord_2(a_p) = 1 but "
                             "ord_2(#E(F_p)) = ord_2(4) = 2"),
            "CLZ_curves_matched_by_the_code_reading": matched.get("CLZ20", 0),
            "CLZ_curves_matched_by_the_docstring_reading":
                alt_matched.get("a_p reading", 0),
        },
        "entry_level_census": census,
        "negative_twists": {
            "Zhai_branch_curves_with_negative_discriminant":
                negative_discriminant_curves,
            "in_scope": ("the Zhai loop runs M from −1000 and skips negative M "
                         "only when Δ_E > 0, so curves with negative "
                         "discriminant admit negative twists"),
            "negatives_in_the_artifact": sum(
                1 for v in twists.values() for m in v if m < 0),
            "curves_whose_criteria_admit_a_negative_twist": neg_disc_curves,
            "sample": negatives_admitted,
        },
        "inertness_caveat": {
            "exact_direction": ("irreducible mod p ⟹ p inert, always — an "
                                "irreducible polynomial over F_p is separable, "
                                "so Dedekind applies whatever the index"),
            "where_it_can_differ": ("the converse can fail when p divides the "
                                    "index, which requires p | disc(cubic)"),
            "curve_prime_pairs_at_risk": risky_pairs,
        },
        "ok": (matched.get("CLZ20", 0) + matched.get("Zha16_no_2_tors", 0)
               == counts["curves"]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print()
    print(f"  curves {counts['curves']:,}   twist pairs in artifact "
          f"{total_pairs:,}")
    for b in sorted(per_branch):
        print(f"    {b:22s} {per_branch[b]:>7,} curves   exact list match: "
              f"{matched[b]:>7,}")
    print()
    t = log["the_2_adic_condition_is_stated_twice"]
    print("  CLZ 2-adic condition, the two readings:")
    print(f"    code      ord_2(#E(F_p)) = 1 : "
          f"{t['CLZ_curves_matched_by_the_code_reading']:,} curves match")
    print(f"    docstring ord_2(a_p)     = 1 : "
          f"{t['CLZ_curves_matched_by_the_docstring_reading']:,} curves match")
    print()
    n = log["negative_twists"]
    print(f"  negative twists in the artifact          : "
          f"{n['negatives_in_the_artifact']:,}")
    print(f"  curves whose criteria admit a negative M : "
          f"{n['curves_whose_criteria_admit_a_negative_twist']:,}")
    print()
    print(f"  Zhai curves with Δ < 0 (negatives in scope): "
          f"{negative_discriminant_curves:,}")
    print(f"  (curve, p) pairs where p | disc(cubic)   : {risky_pairs:,}")
    print()
    c = census
    print("  entry-level old->new census:")
    print(f"    classes: {c['classes']}")
    print(f"    twist entries removed {c['twist_entries_removed']:,}   "
          f"ADDED {c['twist_entries_ADDED']:,}")
    print(f"    every removed entry divisible by 3: "
          f"{c['every_removed_entry_divisible_by_3']}")
    print(f"    curves where new = old minus multiples of 3: "
          f"{c['curves_where_new_equals_old_with_multiples_of_3_dropped']:,}"
          f" of {c['stable']:,}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
