"""Drill for gates 04-10, 12, 13 — plant a defect, demand the named check catch it.

數學戰士「墜衡」 / AMRAL Research Lab.

This tree's README has stated since RUN-001 that

    Every gate gets a mutation drill, and a planted defect must be caught by the
    check *named for it* — not merely by some check. A gate that has only ever
    been green is indistinguishable from a comment.

and until now the BSD line had none. Ten gates, zero drills, and a method section
saying otherwise. RUN-010 closed that for the three gates then carrying the
substantive claims; RUN-011 and RUN-012 added their own gates' drills in the same
commit as the gates, and RUN-012 went back for src04 through src07 — the
Weierstrass arithmetic, the Frobenius counts over F₃, ψ₃ and its two root tests,
and the reducibility sieve. Only the four corpus-scanning gates src00–src03,
whose claims are about text rather than arithmetic, remain undrilled.

TWO KINDS OF DEFECT, because the gates make two kinds of claim.

  `code` — break the gate's own arithmetic and demand a check notice. A wrong
  parametrisation constant, a search window too narrow to reach a real root, a
  candidate cap that returns "none found" instead of "not finished".

  `data` — hand a check the bad input it exists to reject. A discriminant
  valuation that does not rebuild the discriminant, a partition with an overlap.
  A validator that has only ever seen good data has not been tested either.

AND A POSITIVE CONTROL ON THE DRILL ITSELF. Gate 10 reports zero Frobenius-pinning
violations over 79,204 primes. That number means nothing unless the check can
report a violation at all, so one defect replaces f₂ with x³ + x + 1, whose
quadratic resolvent Q(√−31) is *not* inside Q(ζ₂₄, √29) — the pinning genuinely
does not hold there, and violations must appear. A check that cannot go red has
not passed anything.

CONTROLS are perturbations that must leave every check green: a wider search
window, a larger candidate budget, a different random seed for the randomised
factorisation, the same valuations in a different key order. Without them the
drill only shows that the checks are sensitive to *something*.

One control is there for a different reason and is worth reading as a scope
statement: 389.a1 has a1 = 0, so removing the −a1·y term from the group law is
identically a no-op. No drill on that curve can test that branch, and a defect
list that quietly left it out would read as coverage it does not have.

WHAT THE RUNS FOUND, which is the reason to write drills rather than assume them.
The first pass caught 24 of 27; the pass that added gates 04-07 and 13 caught 44
of 49. Every miss was one of two things, and both are worth more than the passes.

Some were checks that could not see a real defect, and they were fixed: a
relational assertion on the F₃ point counts survived subtracting one from both;
a fixture with 3 ∤ N could not exercise gcd(M, 3N); the Hasse guard in RUN-007's
a_p was **unreachable** — at a prime of bad reduction a_p is 0 or ±1, always
inside Hasse, so the branch was dead and its comment was false. It is now the
condition it was pretending to be, and RUN-007's log re-runs byte-identical.

The rest were mutations that are no-ops on the actual population, and they moved
to CONTROLS with the reason attached rather than being dropped. 389.a1 has
a₁ = 0. (n−1)² ≡ 1² (mod n). And dropping the denominator-3 half of RUN-006's
rational root theorem changes no verdict on any of the 4,062 census curves —
1,232 stay True, 2,805 stay False, 25 stay undecided — because every curve with a
root of denominator 3 also has an integer root. A defect list that quietly
omitted these would read as coverage the tree does not have.

The first run's three misses, kept here because they are the clearest case — an off-by-one in `nth_root`,
a primality test stubbed to always say "prime", and `x^q` computed without its
squaring step. None of them changed a single verdict on any fixture curve. The
first two live on the no-factoring fallback, a path the census never needed
because every denominator factored; the third is invisible to the pinning check,
whose branch is decided by a Legendre symbol and never consults the polynomial
arithmetic. Three checks were added for them — `uv-pairs-agree`, `factorisation`
and `density-1-over-24` — and each now catches its own. The gates were not
wrong; the checks did not cover them, and nothing but a planted defect was going
to say so.

Usage:  python code/src11_gate_drill.py
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src09_kept_curves_removal_gate as kept             # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402
import src12_p5_localization as p5                       # noqa: E402
import src13_algorithm2_twists as alg2                   # noqa: E402
import src04_curve_arithmetic_recompute as arith4        # noqa: E402
import src05_frobenius_at_three as frob5                 # noqa: E402
import src06_three_isogeny_sieve as iso6                 # noqa: E402
import src07_isogeny_reducibility_sieve as red7          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src11-gate-drill.json"

# Curves whose verdicts are fixed independently of any run of these gates:
# the six of gate 08's own self-check plus the hard tail of the census, where
# 183430x1's 3-isogeny was established by hand in RUN-006 (ψ₃(163100) = 0).
HARD = [
    ("458626a1", [1, -1, 0, -3322098119425, 2330590303502505277],
     {2: False, 3: False, 5: False, 7: False}),            # den 35 digits
    ("183430x1", [1, 0, 1, -35912323909, 2502914884498672],
     {2: False, 3: True, 5: False, 7: False}),             # den 33 digits
    ("105830f1", [1, 0, 1, -3787689128, -21214699861002],
     {2: False, 3: True, 5: False, 7: False}),             # den 31 digits
    ("38b1", [1, 1, 1, 0, 1], {2: False, 3: False, 5: True, 7: False}),
    ("26b1", [1, -1, 1, -3, 3], {2: False, 3: False, 5: False, 7: True}),
]

GOOD_RECORD = {
    "curve_label": "14a1",
    "ainvs": [1, 0, 1, 4, -6],
    "discriminant_valuations": {"2": 6, "7": 3},           # −21952 = −2⁶·7³
}


# ------------------------------------------------------------------- the checks

def check_x0n_self_check() -> bool:
    """Gate 08 refuses to run unless it reproduces answers known outside it."""
    try:
        x0n.self_check()
    except SystemExit:
        return False
    except Exception:
        return False
    return True


def check_x0n_hard_fixture() -> bool:
    """The same engine on the tail of the census, where the searches are hard."""
    for _label, ainvs, want in HARD:
        j = x0n.j_invariant(ainvs)
        if j is None:
            return False
        fac = {} if j.denominator == 1 else x0n.factorise(j.denominator)
        for n, expected in want.items():
            pts = x0n.rational_points(j, n, fac)
            if pts is None or bool(pts) is not expected:
                return False
    return True


def check_disc_valuations(record=None) -> bool:
    """Gate 09 rebuilds ∏p^v and compares it to the Δ it computes itself."""
    agrees, _rebuilt, primes = kept.verify_discriminant_valuations(
        record or GOOD_RECORD)
    return agrees and bool(primes)


def check_partition(triple=None) -> bool:
    """kept ⊔ removed = the old base, recomputed rather than read."""
    k, r, o = triple or ({"a", "b"}, {"c"}, {"a", "b", "c"})
    return kept.verify_partition(k, r, o)["ok"]


def check_cubic_discriminant() -> bool:
    """disc(f₂) recomputed from the formula must be −11136."""
    return ph2.cubic_discriminant(ph2.F2) == -11136


def check_frobenius_pinning() -> bool:
    """For q ≡ 1 (24) with (q/29) = 1, f₂ mod q never has exactly one root."""
    r = ph2.scan(60_000)
    return not r["violations"] and r["cond12"] > 0


def check_reduction_type() -> bool:
    """29 is nonsplit multiplicative on 696.e1: #E_ns(F₂₉) = 30 = 29 + 1."""
    return (ph2.singular_point_count(ph2.AINVS, 29) == 30
            and ph2.singular_point_count(ph2.AINVS, 3) == 2)


def _prime_by_trial(v: int) -> bool:
    """Deterministic, and deliberately not the routine under test."""
    if v < 2:
        return False
    d = 2
    while d * d <= v:
        if v % d == 0:
            return False
        d += 1
    return True


def check_factorisation() -> bool:
    """factorise() must return actual primes whose product is the input.

    Added because the first run of this drill showed that stubbing the
    primality test to always say "prime" changed no fixture verdict — the
    corrupted factorisations only ever dropped candidates that were not roots.
    A gate can be wrong in a way its own outputs never reveal.
    """
    v = 32 * 3 * 1000003 * 1000033
    fac = x0n.factorise(v)
    if fac is None:
        return False
    prod = 1
    for q, e in fac.items():
        prod *= q ** e
    return prod == v and all(_prime_by_trial(q) for q in fac)


def check_uv_pairs_agree() -> bool:
    """The factoring and no-factoring routes to (u', v') must give one answer.

    The no-factoring route is the one the census never needed — every
    denominator factored — so nothing in RUN-007 or RUN-008 exercised it. It is
    still in the gate, so it is still a claim.
    """
    for dn in (32, 243, 1024, 7776, 15625, 100_000, 371_293):
        for D, m in ((3, 1), (1, 5), (1, 7), (1, 2)):
            a = x0n.uv_pairs(dn, x0n.factorise(dn), D, m)
            b = x0n.uv_pairs(dn, None, D, m)
            if a is None or b is None or sorted(a) != sorted(b):
                return False
    return True


def check_density_one_over_24() -> bool:
    """The measured density must land on 1/24 and not on 1/48.

    Separate from the pinning check, because the pinning branch is decided by a
    Legendre symbol and never consults the polynomial arithmetic — so "zero
    violations" cannot detect a broken x^q. The density can: it is what
    distinguishes 0 roots from 3.
    """
    r = ph2.scan(300_000)
    if not r["primes_total"]:
        return False
    d = r["in_P"] / r["primes_total"]
    return abs(d - 1 / 24) < abs(d - 1 / 48) and abs(d * 24 - 1) < 0.05


def check_p5_localization() -> bool:
    """Gate 12 recomputes P5 v1.1's matrix; it must come back [[1,2],[1,4]]."""
    rows = [p5.localization_row(e).get("row_normalised") for e in p5.DIRECTIONS]
    if rows != [[1, 2], [1, 4]]:
        return False
    return (rows[1][1] - rows[0][1]) % 11 != 0


def check_p5_short_model() -> bool:
    """The short model and the images of P and Q, derived rather than copied."""
    sm = p5.short_model()
    return (sm["A"] == -3024 and sm["B"] == 46224
            and sm["images"]["P"]["short_model"] == [12, 108]
            and sm["images"]["Q"]["short_model"] == [48, 108]
            and all(sm["images"][k]["satisfies_short_model"] for k in "PQ")
            and p5.on_curve(p5.P0) and p5.on_curve(p5.Q0))


# Twist lists the corpus states for two named curves, in
# 03_Algorithm2_Independent_Reproduction — 7 for 46a1 on the CLZ branch and 21
# for 106d1 on the Zhai branch. Fixed outside this gate, so they can test it.
ALG2_FIXTURE = {
    "46a1": {"ainvs": [1, -1, 0, -10, -12], "conductor": 46,
             "conductor_primes": [2, 23], "source": "CLZ20",
             "twists": [1, 185, 265, 305, 745, 785, 905]},
    # 100457b1 is in the shrink_only class: its OLD twist list carried 177,
    # 501 and 669, all divisible by 3, which the gcd(M, 3N) tightening removed.
    # Nothing else in this fixture exercises that condition — 3 ∤ N for both
    # curves below, and on the CLZ branch 3 ≢ 1 (mod 4) kills every multiple of
    # 3 anyway, so the gcd is redundant there.
    "100457b1": {"ainvs": [1, 0, 1, -11, 19], "conductor": 100457,
                 "conductor_primes": [7, 113, 127],
                 "source": "Zha16_no_2_tors",
                 "twists": [1, 149, 389, 569, 653, 709, 809]},
    "106d1": {"ainvs": [1, 1, 0, -27, -67], "conductor": 106,
              "conductor_primes": [2, 53], "source": "Zha16_no_2_tors",
              "twists": [1, 17, 89, 97, 113, 241, 281, 409, 473, 505, 521,
                         545, 577, 649, 673, 713, 785, 857, 865, 929, 937]},
}


def check_alg2_fixture() -> bool:
    """Both branches of Algorithm 2 rebuilt, against the corpus's own fixture."""
    for _label, f in ALG2_FIXTURE.items():
        rec = {k: f[k] for k in ("ainvs", "conductor", "conductor_primes",
                                 "source")}
        if alg2.admissible(rec) != f["twists"]:
            return False
    return True


# Curves whose Weierstrass arithmetic is fixed outside this tree.
ARITH_FIXTURE = [
    ("14a1", [1, 0, 1, 4, -6], -21952),
    ("389a1", [0, 1, 1, -2, 0], 389),
    ("696b1", [0, 1, 0, 8, -16], -178176),
    ("37a1", [0, 0, 1, -1, 0], 37),
]


def check_discriminant_formula() -> bool:
    """src04's Δ, against curves whose discriminant is known independently."""
    for _label, inv, disc in ARITH_FIXTURE:
        if arith4.discriminant(*inv) != disc:
            return False
    return arith4.valuation(-21952, 2) == 6 and arith4.valuation(-21952, 7) == 3


def check_frobenius_at_three() -> bool:
    """src05's point counts over F₃, split by singularity.

    37a1 has good reduction at 3 (3 ∤ 37), so every projective point is
    nonsingular and the two counts agree. 696b1 has additive reduction at 3
    dividing its conductor, so they must not.
    """
    # Pinned absolutely, not by relation: subtracting one from both counts
    # preserves "equal" and "differ by one", so a relational check cannot see a
    # dropped point at infinity. The first drill run proved exactly that.
    return (frob5.point_counts(0, 0, 1, -1, 0) == (7, 7)
            and frob5.point_counts(0, 1, 0, 8, -16) == (3, 2))


def check_psi3_and_roots() -> bool:
    """src06's ψ₃ and its two root tests, on the curve RUN-006 settled by hand.

    183430x1 has the rational 3-isogeny whose root x = 163100 a floating-point
    scan missed; 37a1's isogeny class is trivial, so ψ₃ must have no rational
    root there. Both tests are asked, because the gate has two.
    """
    hard = [1, 0, 1, -35912323909, 2502914884498672]
    c = iso6.psi3_coeffs(*hard)
    if sum(x * 163100 ** k for k, x in enumerate(c)) != 0:
        return False
    if not iso6.rational_root_by_monic_scan(c):
        return False
    trivial = iso6.psi3_coeffs(0, 0, 1, -1, 0)
    if iso6.rational_root_by_monic_scan(trivial):
        return False
    if iso6.rational_root_exists(trivial) is not False:
        return False
    # 14a1's ψ₃ root is −1/3, so this is the only thing here that exercises the
    # denominator-3 half of the rational root theorem. Without it, dropping
    # v = 3 from the search changes no answer in the fixture.
    denom3 = iso6.psi3_coeffs(1, 0, 1, 4, -6)
    return (iso6.rational_root_exists(denom3) is True
            and sum(x * Fraction(-1, 3) ** k
                    for k, x in enumerate(denom3)) == 0)


def check_reducibility_sieve() -> bool:
    """src07's a_p and its residue test, against values computed here.

    a_p for 37a1 at the first few good primes, and the fact that a_p² − 4p is
    negative and so never a square in Z — the test must be modular, not integral.
    """
    for q, want in ((5, -2), (7, -1), (11, -5), (13, -2)):
        if red7.a_p([0, 0, 1, -1, 0], q) != want:
            return False
    if red7.legendre(4, 7) != 1 or red7.legendre(3, 7) != -1:
        return False
    # The bad-reduction refusal, which nothing exercised until now: at p = 37
    # the old Hasse-based guard returned −1, comfortably inside Hasse, because
    # a singular reduction always has a_p in {0, ±1}.
    if red7.a_p([0, 0, 1, -1, 0], 37) is not None:
        return False
    return (red7.is_square_mod(4, 5) and not red7.is_square_mod(2, 5)
            and red7.is_square_mod(0, 5)
            and red7.divides_discriminant([0, 1, 0, 8, -16], 29))


CHECKS = {
    "x0n-self-check": check_x0n_self_check,
    "x0n-hard-fixture": check_x0n_hard_fixture,
    "disc-valuations": check_disc_valuations,
    "partition": check_partition,
    "cubic-discriminant": check_cubic_discriminant,
    "frobenius-pinning": check_frobenius_pinning,
    "reduction-type": check_reduction_type,
    "factorisation": check_factorisation,
    "uv-pairs-agree": check_uv_pairs_agree,
    "density-1-over-24": check_density_one_over_24,
    "p5-localization": check_p5_localization,
    "p5-short-model": check_p5_short_model,
    "alg2-fixture": check_alg2_fixture,
    "disc-formula": check_discriminant_formula,
    "frobenius-at-3": check_frobenius_at_three,
    "psi3-and-roots": check_psi3_and_roots,
    "reducibility-sieve": check_reducibility_sieve,
}


# ------------------------------------------------------------------ the patches

def patch(mod, attr, value):
    old = getattr(mod, attr)
    setattr(mod, attr, value)
    return lambda: setattr(mod, attr, old)


def patch_param(n, coeffs=None, m=None):
    old = copy.deepcopy(x0n.PARAM)
    c, mm = x0n.PARAM[n]
    x0n.PARAM[n] = (coeffs if coeffs is not None else c,
                    m if m is not None else mm)
    return lambda: x0n.PARAM.update(old)


def _bad_j(ainvs):                       # b₈ sign flipped on one term
    a1, a2, a3, a4, a6 = ainvs
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 + a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    from fractions import Fraction
    return None if disc == 0 else Fraction(c4 ** 3, disc)


def _partial_factorise(v):               # trial division only, no rho
    fac, d = {}, 2
    while d * d <= v and d < 1_000_000:
        while v % d == 0:
            fac[d] = fac.get(d, 0) + 1
            v //= d
        d += 1 if d == 2 else 2
    return fac                           # silently drops any large cofactor


def _no_singular_subtraction(ainvs, p):
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    total = 1
    for x in range(p):
        d = ((a1 * x + a3) ** 2 + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % p
        total += 1 if d == 0 else 1 + (1 if pow(d, (p - 1) // 2, p) == 1 else -1)
    return total


DEFECTS = [
    # ---- gate 08: the X₀(n) parametrisations ---------------------------------
    ("X0(3) constant 27 becomes 26", "code", "x0n-self-check",
     lambda: patch_param(3, x0n.polymul([26, 1], x0n.polypow([3, 1], 3)))),
    ("X0(3) cube becomes a square", "code", "x0n-self-check",
     lambda: patch_param(3, x0n.polymul([27, 1], x0n.polypow([3, 1], 2)))),
    ("X0(3) pole order 1 becomes 2", "code", "x0n-self-check",
     lambda: patch_param(3, None, 2)),
    ("X0(5) coefficient 250 becomes 205", "code", "x0n-self-check",
     lambda: patch_param(5, x0n.polypow([3125, 205, 1], 3))),
    ("X0(5) constant 3125 becomes 3120", "code", "x0n-self-check",
     lambda: patch_param(5, x0n.polypow([3120, 250, 1], 3))),
    ("X0(5) pole order 5 becomes 4", "code", "x0n-self-check",
     lambda: patch_param(5, None, 4)),
    ("X0(7) coefficient 13 becomes 31", "code", "x0n-self-check",
     lambda: patch_param(7, x0n.polymul([49, 31, 1],
                                        x0n.polypow([2401, 245, 1], 3)))),
    ("X0(7) constant 2401 becomes 2400", "code", "x0n-self-check",
     lambda: patch_param(7, x0n.polymul([49, 13, 1],
                                        x0n.polypow([2400, 245, 1], 3)))),
    ("X0(2) constant 256 becomes 255", "code", "x0n-self-check",
     lambda: patch_param(2, x0n.polypow([255, 1], 3))),
    ("X0(2) pole order 2 becomes 3", "code", "x0n-self-check",
     lambda: patch_param(2, None, 3)),

    # ---- gate 08: the surrounding arithmetic ---------------------------------
    ("j-invariant: a1a3a4 term in b8 flips sign", "code", "x0n-self-check",
     lambda: patch(x0n, "j_invariant", _bad_j)),
    ("search window narrowed below what a real root needs", "code",
     "x0n-self-check", lambda: patch(x0n, "GAMMA_PAD", -40)),
    ("candidate budget cut to zero: 'none found' replaces 'not finished'",
     "code", "x0n-hard-fixture", lambda: patch(x0n, "MAX_CANDIDATES", 1)),
    ("factorisation drops its large cofactor instead of returning None",
     "code", "x0n-hard-fixture",
     lambda: patch(x0n, "factorise", _partial_factorise)),
    ("nth_root off by one, so the no-factoring fallback misses", "code",
     "uv-pairs-agree",
     lambda: patch(x0n, "nth_root", lambda x, k: max(0, _true_nth_root(x, k) - 1))),
    ("primality test always says prime, corrupting every factorisation",
     "code", "factorisation",
     lambda: patch(x0n, "_is_probable_prime", lambda v: True)),

    # ---- gate 09: the checks that guard supplied data ------------------------
    ("valuation exponent wrong by one", "data", "disc-valuations",
     lambda: _record_patch({"2": 5, "7": 3})),
    ("a prime of the discriminant omitted", "data", "disc-valuations",
     lambda: _record_patch({"2": 6})),
    ("a prime that does not divide the discriminant added", "data",
     "disc-valuations", lambda: _record_patch({"2": 6, "7": 3, "11": 1})),
    ("valuations absent entirely", "data", "disc-valuations",
     lambda: _record_patch({})),
    ("kept and removed overlap", "data", "partition",
     lambda: _partition_patch(({"a", "b"}, {"b", "c"}, {"a", "b", "c"}))),
    ("a base curve in neither kept nor removed", "data", "partition",
     lambda: _partition_patch(({"a"}, {"c"}, {"a", "b", "c"}))),
    ("a kept label absent from the base", "data", "partition",
     lambda: _partition_patch(({"a", "z"}, {"c"}, {"a", "c"}))),

    # ---- gate 10 -------------------------------------------------------------
    ("cubic discriminant formula: 18abcd term dropped", "code",
     "cubic-discriminant",
     lambda: patch(ph2, "cubic_discriminant",
                   lambda f: (-4 * f[2] ** 3 * f[0] + f[2] ** 2 * f[1] ** 2
                              - 4 * f[3] * f[1] ** 3
                              - 27 * f[3] ** 2 * f[0] ** 2))),
    ("f2 replaced by x^3+x+1, whose resolvent escapes Q(zeta24, sqrt29)",
     "code", "frobenius-pinning", lambda: patch(ph2, "F2", [1, 1, 0, 1])),
    ("x^q computed without the squaring step", "code", "density-1-over-24",
     lambda: patch(ph2, "x_pow_q", _bad_x_pow_q)),
    ("singular point never subtracted from the point count", "code",
     "reduction-type",
     lambda: patch(ph2, "singular_point_count", _no_singular_subtraction)),

    # ---- gate 12 -------------------------------------------------------------
    ("group law: doubling drops its 2*a2*x term", "code", "p5-localization",
     lambda: patch(p5, "ec_add", _bad_double)),
    ("group law: y3 drops the a3 correction", "code", "p5-localization",
     lambda: patch(p5, "ec_add", _bad_y3)),
    ("scalar multiplication never doubles its accumulator", "code",
     "p5-localization",
     lambda: patch(p5, "ec_mul", lambda k, A, ell: A if k else None)),
    ("point count forgets the point at infinity", "code", "p5-localization",
     lambda: patch(p5, "npoints", _npoints_no_infinity)),
    ("b2 formula uses 2*a2 instead of 4*a2", "code", "p5-short-model",
     lambda: patch(p5, "short_model", _bad_short_model)),
    ("the wrong generators are used for the localization", "data",
     "p5-localization", lambda: patch(p5, "Q0", (0, -1))),

    # ---- gate 13 -------------------------------------------------------------
    ("Kronecker symbol at 2 accepts 3 and 5 mod 8", "code", "alg2-fixture",
     lambda: patch(alg2, "kronecker",
                   lambda a, n: (0 if a % 2 == 0 else 1) if n == 2
                   else _true_kronecker(a, n))),
    ("point count omits the point at infinity", "code", "alg2-fixture",
     lambda: patch(alg2, "point_count",
                   lambda inv, q: _true_point_count(inv, q) - 1)),
    ("coprimality asks gcd(M, N) instead of gcd(M, 3N)", "code",
     "alg2-fixture", lambda: patch(alg2, "_gcd", _gcd_ignoring_three)),
    ("squarefree set admits squares", "code", "alg2-fixture",
     lambda: patch(alg2, "SQUAREFREE", set(range(1, alg2.BOUND + 1)))),
    ("the 2-division cubic is tested for roots with the wrong leading term",
     "code", "alg2-fixture",
     lambda: patch(alg2, "cubic_irreducible_mod",
                   lambda c, q: not any(
                       (((1 * x + c[1]) * x + c[2]) * x + c[3]) % q == 0
                       for x in range(q)))),
    ("the twist bound is cut below what the artifact used", "code",
     "alg2-fixture", lambda: patch(alg2, "BOUND", 500)),

    # ---- gates 04-07, undrilled until now ------------------------------------
    ("discriminant: the -27*b6^2 term becomes -26*b6^2", "code", "disc-formula",
     lambda: patch(arith4, "discriminant",
                   lambda a1, a2, a3, a4, a6: _disc_wrong(a1, a2, a3, a4, a6))),
    ("valuation returns one too many", "code", "disc-formula",
     lambda: patch(arith4, "valuation",
                   lambda n, q: _true_valuation(n, q) + 1)),
    ("point count over F_3 forgets the point at infinity", "code",
     "frobenius-at-3",
     lambda: patch(frob5, "point_counts",
                   lambda *inv: tuple(c - 1 for c in _true_counts(*inv)))),
    ("singularity test drops one partial derivative", "code",
     "frobenius-at-3", lambda: patch(frob5, "point_counts", _counts_one_partial)),
    ("psi3: the 3*b4 coefficient becomes b4", "code", "psi3-and-roots",
     lambda: patch(iso6, "psi3_coeffs", _psi3_wrong)),
    ("monic scan uses 9*b8 where the substitution gives 27*b8", "code",
     "psi3-and-roots", lambda: patch(iso6, "rational_root_by_monic_scan",
                                     _monic_scan_nine)),
    ("a_p keeps counts Hasse cannot accommodate", "code",
     "reducibility-sieve",
     lambda: patch(red7, "a_p", lambda inv, q: _true_ap(inv, q) or 0)),
    ("Legendre symbol uses the wrong exponent", "code", "reducibility-sieve",
     lambda: patch(red7, "legendre",
                   lambda a, q: 0 if a % q == 0
                   else (1 if pow(a, (q - 1), q) == 1 else -1))),
    ("square-test mod n skips the residue 0", "code", "reducibility-sieve",
     lambda: patch(red7, "is_square_mod",
                   lambda a, n: any((r * r) % n == a % n
                                    for r in range(1, n)))),
]

CONTROLS = [
    ("search window widened", lambda: patch(x0n, "GAMMA_PAD", 12)),
    ("candidate budget raised", lambda: patch(x0n, "MAX_CANDIDATES", 400_000)),
    ("different random seed for the factorisation",
     lambda: _reseed(987654321)),
    ("rho budget raised", lambda: patch(x0n, "RHO_BUDGET", 800)),
    ("label-file header length re-read as the same value",
     lambda: patch(kept, "LABEL_HEADER_LINES", 6)),
    ("valuations given in a different key order", lambda: _record_patch(
        {"7": 3, "2": 6})),
    ("partition sets given as different objects with the same members",
     lambda: _partition_patch((set(["a", "b"]), set(["c"]),
                               set(["c", "b", "a"])))),
    ("no change at all", lambda: (lambda: None)),
    ("gate 12's admissible-prime scan limit changed",
     lambda: patch(p5, "SCAN", 5_000)),
    ("the two ramified directions given in the other order",
     lambda: patch(p5, "DIRECTIONS", (397, 991))),
    # This one is a control on purpose, and the reason is a scope statement:
    # 389.a1 has a1 = 0, so the −a1·y term of the doubling formula is
    # identically zero and removing it cannot change any answer. No drill on
    # this curve can test that branch, and a defect list that quietly omitted
    # it would read as coverage it does not have.
    ("group law: the -a1*y term removed, which a1 = 0 makes a no-op",
     lambda: patch(p5, "ec_add", _a1_branch_removed)),
    ("gate 13's factor table rebuilt with the same contents",
     lambda: patch(alg2, "FACTORS", dict(alg2.FACTORS))),
    # Another control on purpose: (n−1)² ≡ 1² (mod n), so the last residue of
    # the square test is always redundant and dropping it cannot change an
    # answer. Listed with the reason rather than left out.
    ("square-test mod n drops its last residue, which (n-1)^2 = 1^2 makes redundant",
     lambda: patch(red7, "is_square_mod",
                   lambda a, n: any((r * r) % n == a % n
                                    for r in range(max(0, n - 1))))),
    # And a third, measured rather than assumed. Dropping the denominator-3 half
    # of RUN-006's rational root theorem changes no verdict on ANY of the 4,062
    # census curves: 1,232 stay True, 2,805 stay False, 25 stay undecided. Every
    # curve with a root of denominator 3 also has an integer root, so that
    # branch never decided anything. The gate still computes it, and the check
    # still asserts it computes it correctly — but no defect planted in it can
    # be caught through the verdict, which is all the gate exposes.
    ("rational-root theorem forgets the denominator 3, which decides nothing here",
     lambda: patch(iso6, "rational_root_exists", _root_exists_v1_only)),
]


_true_kronecker = alg2.kronecker
_true_point_count = alg2.point_count
_true_valuation = arith4.valuation
_true_counts = frob5.point_counts
_true_ap = red7.a_p
_true_psi3 = iso6.psi3_coeffs


def _disc_wrong(a1, a2, a3, a4, a6):
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4 ** 3 - 26 * b6 * b6 + 9 * b2 * b4 * b6


def _counts_one_partial(a1, a2, a3, a4, a6):
    a1, a2, a3, a4, a6 = (c % 3 for c in (a1, a2, a3, a4, a6))
    total = nonsingular = 1
    for x in range(3):
        for y in range(3):
            f = (y * y + a1 * x * y + a3 * y
                 - (x ** 3 + a2 * x * x + a4 * x + a6)) % 3
            if f:
                continue
            total += 1
            if (2 * y + a1 * x + a3) % 3:          # df/dx never consulted
                nonsingular += 1
    return total, nonsingular


def _psi3_wrong(a1, a2, a3, a4, a6):
    c = list(_true_psi3(a1, a2, a3, a4, a6))
    c[2] //= 3                                     # 3*b4 -> b4
    return c


def _monic_scan_nine(coeffs):
    """The exact mistake RUN-006 made: the substitution y = 3x gives a constant
    term 27*b8, and the first version of that gate multiplied by 9."""
    b8, tb6, tb4, b2, _ = coeffs
    mono = [9 * b8, 9 * (tb6 // 3), 3 * (tb4 // 3) * 3, b2, 1]
    bound = 1 + sum(abs(c) for c in mono[:-1])
    step = 1
    for w in range(-min(bound, 400000), min(bound, 400000) + 1, step):
        if sum(c * w ** k for k, c in enumerate(mono)) == 0:
            return True
    return False


def _root_exists_v1_only(coeffs):
    from fractions import Fraction
    c0 = coeffs[0]
    if c0 == 0:
        return True
    divs = iso6.divisors_within_budget(c0)
    if divs is None:
        return None
    for u in divs:
        for su in (u, -u):
            x = Fraction(su, 1)                    # v = 3 never tried
            if sum(Fraction(c) * x ** k for k, c in enumerate(coeffs)) == 0:
                return True
    return False


def _gcd_ignoring_three(a, b):
    while a % 3 == 0 and b % 3 == 0:
        b //= 3
    x, y = a, b
    while y:
        x, y = y, x % y
    return x


def _a1_branch_removed(A, B, ell):
    a1, a2, a3, a4, _ = p5.AINVS
    if A is None:
        return B
    if B is None:
        return A
    x1, y1 = A
    x2, y2 = B
    if x1 == x2 and (y1 + y2 + a1 * x2 + a3) % ell == 0:
        return None
    if A == B:
        num = (3 * x1 * x1 + 2 * a2 * x1 + a4) % ell
        den = (2 * y1 + a1 * x1 + a3) % ell
    else:
        num = (y2 - y1) % ell
        den = (x2 - x1) % ell
    lam = num * pow(den, -1, ell) % ell
    nu = (y1 - lam * x1) % ell
    x3 = (lam * lam + a1 * lam - a2 - x1 - x2) % ell
    y3 = (-(lam + a1) * x3 - nu - a3) % ell
    return (x3, y3)


def _bad_short_model():
    a1, a2, a3, a4, a6 = p5.AINVS
    b2 = a1 * a1 + 2 * a2                                    # 4*a2 -> 2*a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    A, B = -27 * c4, -54 * c6
    images = {}
    for name, (x, y) in (("P", p5.P0), ("Q", p5.Q0)):
        X = 36 * x + 3 * b2
        Y = 216 * y + 108 * a1 * x + 108 * a3
        images[name] = {"minimal_model": [x, y], "short_model": [X, Y],
                        "satisfies_short_model": Y * Y == X ** 3 + A * X + B}
    return {"b2": b2, "c4": c4, "c6": c6, "disc": 0, "A": A, "B": B,
            "images": images}


_true_nth_root = x0n.nth_root
_RECORD_OVERRIDE: dict | None = None
_PARTITION_OVERRIDE: tuple | None = None


def _record_patch(vals):
    global _RECORD_OVERRIDE
    rec = dict(GOOD_RECORD)
    rec["discriminant_valuations"] = vals
    _RECORD_OVERRIDE = rec

    def restore():
        global _RECORD_OVERRIDE
        _RECORD_OVERRIDE = None
    return restore


def _partition_patch(triple):
    global _PARTITION_OVERRIDE
    _PARTITION_OVERRIDE = triple

    def restore():
        global _PARTITION_OVERRIDE
        _PARTITION_OVERRIDE = None
    return restore


def _reseed(seed):
    import random
    random.seed(seed)
    return lambda: random.seed(20260908)


def _bad_x_pow_q(f, q):
    result, base, e = [1, 0, 0], [0, 1, 0], q
    while e:
        if e & 1:
            result = ph2.poly_mulmod(result, base, f, q)
        e >>= 1                          # base never squared
    return result


def _bad_double(A, B, ell):
    """Doubling formula missing its 2·a2·x term (a2 = 1 on 389.a1)."""
    a1, a2, a3, a4, _ = p5.AINVS
    if A is None:
        return B
    if B is None:
        return A
    x1, y1 = A
    x2, y2 = B
    if x1 == x2 and (y1 + y2 + a1 * x2 + a3) % ell == 0:
        return None
    if A == B:
        num = (3 * x1 * x1 + a4 - a1 * y1) % ell            # 2·a2·x1 dropped
        den = (2 * y1 + a1 * x1 + a3) % ell
    else:
        num = (y2 - y1) % ell
        den = (x2 - x1) % ell
    lam = num * pow(den, -1, ell) % ell
    nu = (y1 - lam * x1) % ell
    x3 = (lam * lam + a1 * lam - a2 - x1 - x2) % ell
    y3 = (-(lam + a1) * x3 - nu - a3) % ell
    return (x3, y3)


def _bad_y3(A, B, ell):
    """y3 without the a3 correction."""
    a1, a2, a3, a4, _ = p5.AINVS
    if A is None:
        return B
    if B is None:
        return A
    x1, y1 = A
    x2, y2 = B
    if x1 == x2 and (y1 + y2 + a1 * x2 + a3) % ell == 0:
        return None
    if A == B:
        num = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) % ell
        den = (2 * y1 + a1 * x1 + a3) % ell
    else:
        num = (y2 - y1) % ell
        den = (x2 - x1) % ell
    lam = num * pow(den, -1, ell) % ell
    nu = (y1 - lam * x1) % ell
    x3 = (lam * lam + a1 * lam - a2 - x1 - x2) % ell
    y3 = (-(lam + a1) * x3 - nu) % ell                      # a3 dropped
    return (x3, y3)


def _npoints_no_infinity(ell):
    a1, a2, a3, a4, a6 = (c % ell for c in p5.AINVS)
    total = 0                                                # O never counted
    for x in range(ell):
        d = ((a1 * x + a3) ** 2
             + 4 * (x ** 3 + a2 * x * x + a4 * x + a6)) % ell
        total += 1 + p5.legendre(d, ell)
    return total


def run_checks() -> dict[str, bool]:
    out = {}
    for name, fn in CHECKS.items():
        try:
            if name == "disc-valuations":
                out[name] = fn(_RECORD_OVERRIDE)
            elif name == "partition":
                out[name] = fn(_PARTITION_OVERRIDE)
            else:
                out[name] = fn()
        except Exception:
            out[name] = False            # a crash is a red check, not a pass
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    baseline = run_checks()
    if not all(baseline.values()):
        raise SystemExit(f"the undisturbed gates are not green: {baseline}")
    print(f"  baseline: all {len(baseline)} checks green")

    results, uncaught, wrong_catcher = [], [], []
    for name, kind, expected, make in DEFECTS:
        restore = make()
        try:
            got = run_checks()
        finally:
            restore()
        red = [k for k, v in got.items() if not v]
        entry = {"defect": name, "kind": kind, "named_check": expected,
                 "checks_that_went_red": red,
                 "caught_by_the_named_check": expected in red}
        results.append(entry)
        if not red:
            uncaught.append(name)
        elif expected not in red:
            wrong_catcher.append({"defect": name, "expected": expected,
                                  "actually_caught_by": red})
        flag = ("OK " if expected in red else
                "MISSED " if not red else "WRONG-CHECK ")
        print(f"    {flag:12s} [{kind}] {name}")
        print(f"                 red: {', '.join(red) if red else '(none)'}")

    print()
    ctrl_results, disturbed = [], []
    for name, make in CONTROLS:
        restore = make()
        try:
            got = run_checks()
        finally:
            restore()
        red = [k for k, v in got.items() if not v]
        ctrl_results.append({"control": name, "checks_that_went_red": red,
                             "undisturbed": not red})
        if red:
            disturbed.append({"control": name, "red": red})
        print(f"    {'OK ' if not red else 'DISTURBED '}control: {name}"
              + (f"   red: {', '.join(red)}" if red else ""))

    after = run_checks()
    log = {
        "gate": "src11_gate_drill",
        "covers": ["src08_modular_curve_confirmation",
                   "src09_kept_curves_removal_gate",
                   "src10_phase2_density_and_base",
                   "src12_p5_localization",
                   "src13_algorithm2_twists"],
        "rule": ("a planted defect must be caught by the check NAMED for it, "
                 "not merely by some check; and controls must disturb nothing"),
        "two_kinds": {
            "code": "break the gate's own arithmetic, demand a check notice",
            "data": ("hand a validating check the bad input it exists to "
                     "reject — a validator that has only seen good data has "
                     "not been tested either"),
        },
        "positive_control_on_the_drill": (
            "replacing f2 with x^3+x+1, whose quadratic resolvent Q(sqrt-31) is "
            "NOT inside Q(zeta24, sqrt29), must make the pinning check go red — "
            "otherwise gate 10's 'zero violations over 79,204 primes' would be "
            "indistinguishable from a check that cannot fire"),
        "baseline_all_green": baseline,
        "defects": results,
        "controls": ctrl_results,
        "totals": {
            "defects": len(DEFECTS),
            "caught_by_the_named_check": sum(
                1 for r in results if r["caught_by_the_named_check"]),
            "UNCAUGHT_BY_ANY_CHECK": uncaught,
            "CAUGHT_BY_THE_WRONG_CHECK": wrong_catcher,
            "controls": len(CONTROLS),
            "controls_that_disturbed_a_check": disturbed,
        },
        "state_restored_afterwards": all(after.values()),
        "ok": (not uncaught and not wrong_catcher and not disturbed
               and all(after.values())),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    t = log["totals"]
    print()
    print(f"  {t['defects']} defects, {t['caught_by_the_named_check']} caught "
          f"by the check named for them")
    print(f"  uncaught by any check      : "
          f"{len(uncaught)}{'  ' + ', '.join(uncaught) if uncaught else ''}")
    print(f"  caught by the wrong check  : {len(wrong_catcher)}")
    print(f"  {t['controls']} controls, "
          f"{len(disturbed)} disturbed a check")
    print(f"  state restored afterwards  : {log['state_restored_afterwards']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
