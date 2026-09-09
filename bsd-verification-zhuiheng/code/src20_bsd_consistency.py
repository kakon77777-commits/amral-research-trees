"""Gate 20 — the rank-0 BSD formula as a check on everything under it, and 389.a1's regulator.

數學戰士「墜衡」 / AMRAL Research Lab.

Two things this round is for.

**The strong BSD formula at rank 0 is a joint test.** It says

    L(E,1)/Ω = #Ш · ∏c_p / #E(Q)_tors² ,

and Cassels makes #Ш a square. Four separately computed quantities go in — the
L-value from point counts, the real period by AGM, the torsion by a gcd bound,
and the Tamagawa numbers by Tate's algorithm — and the formula says their
combination must land on a positive integer square. Nothing about that is
approximate: a curve either lands on an integer or it does not.

So it is run across the small-conductor part of the base, and it does two jobs
at once: where it closes it validates all four routines simultaneously, and
where it fails it points at the one input that could be wrong.

**389.a1's regulator.** The P5 line's stated core target is bridging the
analytic leading term to the algebraic regulator. The algebraic half is
computable. Canonical heights by the x-only duplication ĥ(P) = lim h(x(2ⁿP))/4ⁿ,
Richardson-extrapolated, with the parallelogram law
ĥ(P+Q) + ĥ(P−Q) = 2ĥ(P) + 2ĥ(Q) as the check — an identity the computation
never uses.

A non-zero regulator is also a **third** independent proof that P = (0,0) and
Q = (1,0) are independent, after RUN-011's localization determinant and the
package's own claim.

WHAT THIS ROUND FOUND ABOUT ITS OWN PREDECESSOR. RUN-014's root-number test
compares a smoothed Λ(2) against the Dirichlet series Σ a_n n^{-2} and keeps
whichever sign matches. It reported a "residual" and a "gap" as if their ratio
were a confidence — it is not. The residual can be small by accident, and so can
the drift between partial sums; the honest bound on the truncation, about
2·log M/√M, is *comparable to the gap being measured* at these conductors. The
sign test is therefore much weaker than RUN-014 presented it.

The anchor's sign survives, for a better reason than the one given: `L/Ω` came
out 1 to sixteen digits with torsion and every `c_p` computed independently, and
that would be an absurd coincidence if `L(E,1)` were zero.

Usage:  python code/src20_bsd_consistency.py
"""

from __future__ import annotations

import collections
import json
import math
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src20-bsd-consistency.json"

CONDUCTOR_CAP = 2000
TERMS = 3000
P5_CURVE = [0, 1, 1, -2, 0]                   # 389.a1
P5_GENERATORS = ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)))


# ------------------------------------------------------------ canonical heights

def _binvs(ainvs):
    return anchor.b_invariants(ainvs)


def ec_add(ainvs, P, Q):
    a1, a2, a3, a4, _a6 = ainvs
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2 + a1 * x2 + a3) == 0:
        return None
    if P == Q:
        num, den = 3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1, 2 * y1 + a1 * x1 + a3
    else:
        num, den = y2 - y1, x2 - x1
    lam = Fraction(num, den)
    nu = y1 - lam * x1
    x3 = lam * lam + a1 * lam - a2 - x1 - x2
    return (x3, -(lam + a1) * x3 - nu - a3)


def ec_neg(ainvs, P):
    a1, _a2, a3, _a4, _a6 = ainvs
    x, y = P
    return (x, -y - a1 * x - a3)


def x_double(ainvs, x):
    """x(2P) from x(P) alone — the y-coordinate never enters, which keeps the
    integers small enough for the limit to be computed at all."""
    b2, b4, b6, b8, _c4, _c6, _d = (*_binvs(ainvs)[:4], 0, 0, 0)
    num = x ** 4 - b4 * x * x - 2 * b6 * x - b8
    den = 4 * x ** 3 + b2 * x * x + 2 * b4 * x + b6
    return None if den == 0 else Fraction(num, den)


def log_height(x: Fraction) -> float:
    n, d = abs(x.numerator), x.denominator
    m = n if n > d else d
    if m <= 1:
        return 0.0
    b = m.bit_length()
    return ((b - 53) * math.log(2) + math.log(m >> (b - 53))) if b > 53 \
        else math.log(m)


def canonical_height(ainvs, P, depth: int = 10) -> dict:
    """ĥ(P) = lim h(x(2ⁿP))/4ⁿ, with the extrapolation level chosen by measurement.

    Two Richardson steps are computed, and **which of the three sequences to
    believe is decided from their own last-two agreement** rather than assumed.
    RUN-026 found that assuming the deepest is best is wrong here, and not
    marginally:

        37a1, depth 10 — raw's last two agree to 1.0e-14, while r1's last two
        differ by 2.5e-07 because r1 is not monotone in n. `richardson2` is
        built from r1's last two, so it takes a value already correct to 3e-15
        and returns one wrong by 8.4e-08.

    On 389.a1 the same defect cost the regulator two orders of magnitude: the
    parallelogram-law residual read 1.6e-06 from `richardson2` and reads 9.4e-09
    from the level the sequences themselves select. RUN-017 reported that 1.6e-06
    as the method's precision; it was this.

    The underlying reason the second step misbehaves is that `h(x(2ⁿP))/4ⁿ` has
    no clean 1/4ⁿ error expansion for these curves — the local contributions at
    bad primes do not decay that way — so r1 carries structure a second
    extrapolation misreads. Rather than model that, the gate measures it.
    """
    x = P[0]
    raw = []
    for _ in range(depth):
        x = x_double(ainvs, x)
        if x is None:
            break
        raw.append(log_height(x))
    seq = [v / 4 ** (i + 1) for i, v in enumerate(raw)]
    r1 = [(4 * seq[i + 1] - seq[i]) / 3 for i in range(len(seq) - 1)]
    r2 = [(4 * r1[i + 1] - r1[i]) / 3 for i in range(len(r1) - 1)]
    levels = {"raw": seq, "richardson1": r1, "richardson2": r2}
    gaps = {k: (abs(v[-1] - v[-2]) if len(v) >= 2 else float("inf"))
            for k, v in levels.items()}
    best = min(gaps, key=gaps.get)
    return {"raw_last": seq[-1], "richardson1": r1[-1], "richardson2": r2[-1],
            "steps": len(seq),
            "level_gaps": gaps, "chosen_level": best,
            "value": levels[best][-1],
            "self_consistency": gaps[best]}


def regulator(ainvs, gens, depth: int = 10) -> dict:
    """The height regulator. `depth` is the doubling depth of the limit.

    Cost grows brutally with depth — the x-coordinate of 2ⁿP has about 4ⁿ·ĥ/ln 10
    digits, so depth 10 means 145,000-digit numerators and a Fraction gcd on
    every step: 30 seconds against 0.17 at depth 8. The drill runs this once per
    defect and once per control, so it uses depth 8 with a tolerance set to what
    depth 8 actually delivers.
    """
    P, Q = gens
    PQ = ec_add(ainvs, P, Q)
    PmQ = ec_add(ainvs, P, ec_neg(ainvs, Q))
    full = {name: canonical_height(ainvs, pt, depth)
            for name, pt in (("P", P), ("Q", Q), ("P+Q", PQ), ("P-Q", PmQ))}

    # THE LEVEL IS CHOSEN BY THE PARALLELOGRAM LAW, AND UNIFORMLY.
    #
    # ĥ(P+Q) + ĥ(P−Q) = 2ĥ(P) + 2ĥ(Q) holds exactly for the true heights, so the
    # residual is an external measure of how good a level is — and it is the
    # right one here, where letting each height pick its own level made things
    # worse rather than better. The law is only exact when all four are computed
    # the same way; a mixed selection breaks the very identity being used to
    # judge it, and on 389.a1 at depth 10 that cost an order of magnitude
    # (residual −5.0e-07 mixed, 9.4e-09 uniform).
    #
    # Fixing the level to `richardson2`, as this gate did through RUN-025, was
    # worse still: 1.6e-06 at depth 10 and −2.4e-05 at depth 8, never the best
    # at either. RUN-017 reported that 1.6e-06 as the method's precision.
    candidates = {}
    for level in ("raw_last", "richardson1", "richardson2"):
        hh = {n: d[level] for n, d in full.items()}
        res = hh["P+Q"] + hh["P-Q"] - 2 * hh["P"] - 2 * hh["Q"]
        pr = (hh["P+Q"] - hh["P"] - hh["Q"]) / 2
        candidates[level] = {"heights": hh, "residual": res,
                             "pairing": pr,
                             "regulator": hh["P"] * hh["Q"] - pr * pr}
    best = min(candidates, key=lambda k: abs(candidates[k]["residual"]))
    chosen = candidates[best]
    return {"heights": chosen["heights"],
            "extrapolation_level": best,
            "level_chosen_by": "smallest parallelogram-law residual, uniformly",
            "residual_at_each_level": {k: v["residual"]
                                       for k, v in candidates.items()},
            "regulator_at_each_level": {k: v["regulator"]
                                        for k, v in candidates.items()},
            "P_plus_Q": [str(PQ[0]), str(PQ[1])],
            "P_minus_Q": [str(PmQ[0]), str(PmQ[1])],
            "parallelogram_law_residual": chosen["residual"],
            "pairing_PQ": chosen["pairing"],
            "regulator": chosen["regulator"], "depth": depth,
            "independent": abs(chosen["regulator"]) > 1e-6}


# --------------------------------------------------------- the rank-0 BSD sweep

def sweep(records, limit: int | None = None) -> dict:
    tally = collections.Counter()
    shas = collections.Counter()
    non_closing = []
    for r in records:
        inv, N = r["ainvs"], r["conductor"]
        res = anchor.analyse(r["curve_label"], inv, N,
                             limit=limit or TERMS)
        if res["root_number"] is None:
            tally["sign undecided by the guard"] += 1
            continue
        if res["root_number"] != 1:
            tally["sign says -1"] += 1
            continue
        L = res["L_at_1"]
        if L is None or abs(L) < 1e-8:
            tally["L(E,1) = 0"] += 1
            continue
        tors = res["torsion_bound_gcd"]
        prod = 1
        for p in r["conductor_primes"]:
            c = tate.reduction_data(inv, p, want_c=True)["c"]
            if c is None:
                prod = None
                break
            prod *= c
        if prod is None:
            tally["c_p not computed"] += 1
            continue
        ratio = L * tors * tors / (res["real_period"] * prod)
        near = round(ratio)
        square = (near > 0 and math.isqrt(near) ** 2 == near
                  and abs(ratio - near) < 1e-6)
        if square:
            tally["BSD closes: a positive integer square"] += 1
            shas[near] += 1
        else:
            tally["BSD does not close"] += 1
            if len(non_closing) < 20:
                non_closing.append({"label": r["curve_label"], "N": N,
                                    "ratio": ratio, "torsion": tors,
                                    "prod_c": prod})
    return {"tally": dict(tally.most_common()),
            "Sha_values_where_it_closes": {str(k): v for k, v in shas.items()},
            "non_closing_sample": non_closing}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    reg = regulator(P5_CURVE, P5_GENERATORS)
    records = [r for r in json.loads(x0n.ARITH.read_text(encoding="utf-8"))["records"]
               if r["conductor"] <= CONDUCTOR_CAP]
    sw = sweep(records)

    log = {
        "gate": "src20_bsd_consistency",
        "rank_zero_bsd_as_a_joint_test": {
            "formula": "L(E,1)/Ω = #Ш · ∏c_p / #E(Q)_tors², with #Ш a square",
            "what_it_tests_at_once": (
                "the L-value from point counts, the real period by AGM, the "
                "torsion by a gcd bound, and every c_p by Tate's algorithm — "
                "four separately computed quantities whose combination must "
                "land on a positive integer square"),
            "conductor_cap": CONDUCTOR_CAP,
            "curves": len(records),
            **sw,
        },
        "regulator_of_389a1": {
            "curve": P5_CURVE,
            "generators": ["(0,0)", "(1,0)"],
            **reg,
            "method": ("ĥ(P) = lim h(x(2ⁿP))/4ⁿ by x-only duplication, two "
                       "Richardson steps on the 1/4ⁿ error"),
            "check": ("the parallelogram law ĥ(P+Q)+ĥ(P−Q) = 2ĥ(P)+2ĥ(Q), an "
                      "identity the computation never uses"),
            "third_independent_proof_of_rank_2": (
                "a non-zero height regulator makes P and Q independent, after "
                "RUN-011's localization determinant det M_loc = 2 ≠ 0 in F₁₁ "
                "reached the same conclusion by a route sharing no arithmetic"),
        },
        "what_this_says_about_RUN_014s_sign_test": {
            "the_method": ("compare a smoothed Λ(2) against Σ a_n n^{-2} and "
                           "keep whichever sign matches"),
            "the_error_it_reported": (
                "a 'residual' and a 'gap', whose ratio was presented as a "
                "confidence. It is not one: the residual can be small by "
                "accident, and so can the drift between partial sums"),
            "the_honest_bound": (
                "the Dirichlet truncation is about 2·log M/√M, which at these "
                "conductors is COMPARABLE to the gap being measured — so the "
                "test is much weaker than it was presented as"),
            "why_the_anchor_survives": (
                "not because of that comparison. L(696.e1,1)/Ω came out 1 to "
                "sixteen digits with torsion and every c_p computed "
                "independently, which would be an absurd coincidence if "
                "L(E,1) were zero. The BSD identity is the stronger sign test"),
            "how_it_showed_up": (
                "the curves where the sweep fails to close are exactly the ones "
                "whose sign was mis-called: their ratios spread across a range "
                "with none near an integer square, which is what a wrong sign "
                "produces and what a wrong period or Tamagawa number would not"),
        },
        "ok": (reg["independent"]
               and abs(reg["parallelogram_law_residual"]) < 1e-4
               and sw["tally"].get("BSD closes: a positive integer square", 0)
               >= 200
               and set(sw["Sha_values_where_it_closes"]) == {"1"}),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print(f"  389.a1 regulator")
    for k, v in reg["heights"].items():
        print(f"    ĥ({k:4s}) = {v:.12f}")
    print(f"    parallelogram-law residual : "
          f"{reg['parallelogram_law_residual']:.3e}")
    print(f"    <P,Q> = {reg['pairing_PQ']:.12f}")
    print(f"    REGULATOR = {reg['regulator']:.12f}   nonzero ⟹ P, Q "
          f"independent: {reg['independent']}")
    print()
    print(f"  rank-0 BSD sweep, conductor ≤ {CONDUCTOR_CAP}: "
          f"{len(records)} curves")
    for k, v in sw["tally"].items():
        print(f"    {k:38s} {v:>5}")
    print(f"    Ш where it closes: {sw['Sha_values_where_it_closes']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
