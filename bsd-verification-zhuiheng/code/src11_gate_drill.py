"""Drill for gates 04-10, 12-22 — plant a defect, demand the named check catch it.

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

import collections
import copy
import json
import math
import pathlib
import re
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
import src14_globalizer_faithfulness as glob14           # noqa: E402
import src15_phase2_anchor as anchor15                   # noqa: E402
import src16_twist_family_lvalues as fam16               # noqa: E402
import src17_family_prime_router as route17              # noqa: E402
import src18_tate_algorithm as tate18                    # noqa: E402
import src20_bsd_consistency as bsd20                    # noqa: E402
import src21_two_witness_certificate as tw21             # noqa: E402
import src22_witness_network as net22                    # noqa: E402
import src23_p5_local_units as p5u                       # noqa: E402
import src24_p5_status_ledger as led24                    # noqa: E402
import src25_p5_core_vertex as cv25                        # noqa: E402
import src26_rank2_bsd_identity as r2bsd                   # noqa: E402
import src00_corpus_identity as corpus00                   # noqa: E402
import src01_ladder_vocabulary as ladder01                 # noqa: E402
import src02_rejected_route_recurrence as route02          # noqa: E402
import src03_multiplicity_nogo as nogo03                   # noqa: E402
import src27_agent_experiment_audit as agent27            # noqa: E402
import src28_rank1_bsd_identity as r1bsd                  # noqa: E402
import src29_sweep_coverage as cov29                      # noqa: E402
import src30_phase1_numeric_crosscheck as p1num           # noqa: E402
import src31_q9_census_closure as q9                      # noqa: E402

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
    # 20,000 rather than 60,000: this runs once per defect and once per
    # control, and the pinning either holds on every admissible prime or
    # fails on the first few — a longer scan buys no discrimination here.
    r = ph2.scan(20_000)
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
    # 60,000 rather than 300,000, for the same reason: 1/24 and 1/48 are a
    # factor of two apart and the count separates them long before here.
    r = ph2.scan(60_000)
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


def check_globalizer() -> bool:
    """Gate 14's exact-arithmetic claims about the faithful unresolved mass."""
    F = Fraction
    if glob14.mass_exact([], F(2)) != 0:
        return False
    if glob14.mass_exact([40749], F(2)) != F(1, 40749 ** 2):
        return False
    if glob14.mass_exact([1, 2], F(2)) != F(5, 4):
        return False
    # monotone certification cannot raise the mass
    a = glob14.mass_exact(range(1, 20), F(3))
    b = glob14.mass_exact(range(5, 20), F(3))
    if not (b < a):
        return False
    # and the invisibility index must land where double precision actually runs
    # out: one part in 2^53 of the reference, not one part in anything else
    idx = glob14.invisibility_index(2.0, 1.6449340668482264)
    return 7.3e7 < idx < 7.5e7


def check_anchor_11a1() -> bool:
    """Gate 15 on 11a1, whose BSD data is fixed outside this tree.

    Torsion Z/5, c_11 = 5, Ш trivial, so L(E,1)/Ω must be exactly 5/25 = 1/5,
    the root number must come out +1, and the real period is 1.26920930…
    """
    # The tolerances are set to the computation's actual precision, not to a
    # round number. Undisturbed, |L/Ω − 1/5| is 2.8e-17 and the AGM is stable to
    # the last bit — so a 1e-9 window, which an earlier version of this check
    # used, was wide enough to hide a one-step AGM (1.4e-12 off) and an inverted
    # split/non-split test (2.6e-10 off). A tolerance looser than the quantity's
    # precision is a check that cannot see a real defect.
    r = anchor15.analyse("11a1", [0, -1, 1, -10, -20], 11, limit=4000)
    return (r["root_number"] == 1
            and abs(r["L_over_Omega"] - 0.2) < 1e-12
            and abs(r["real_period"] - 1.2692093042795534) < 1e-13
            and r["torsion_bound_gcd"] == 5)


def check_anchor_rank_one() -> bool:
    """37a1 has rank 1: the sign must come out −1 and L(E,1) must be 0.

    This is the case that separates a vanishing sum from a vanishing sign —
    Σ(a_n/n)e^{−2πn/√N} is 0.19 there, so reading it as L(E,1) would report a
    rank-1 curve as rank 0.
    """
    # Δ = 37 > 0, so E(R) has two components. The value below is 5.98691729…,
    # which is what ∫_{E(R)}|ω| actually is — an earlier version froze twice
    # that, taken from the gate's own output and never compared with anything
    # outside it. See check_real_period_against_integration.
    r = anchor15.analyse("37a1", [0, 0, 1, -1, 0], 37, limit=4000)
    return (r["root_number"] == -1 and r["L_at_1"] == 0.0
            and abs(r["real_period"] - 5.986917292463919) < 1e-10)


def check_E1_against_an_independent_implementation() -> bool:
    """E₁ is implemented in the gate with no dependencies; mpmath checks it.

    The gate stays standard-library only — the outside implementation belongs
    in the drill, where disagreement is the finding.
    """
    try:
        import mpmath
    except ImportError:                                   # pragma: no cover
        return True
    for x in (0.05, 0.238, 0.9, 1.9, 2.1, 5.0, 12.0, 40.0, 120.0):
        ref = float(mpmath.e1(x))
        if abs(anchor15.E1(x) - ref) > 1e-12 * abs(ref):
            return False
    return True


def check_kronecker() -> bool:
    """The Kronecker symbol, against a fixed table and against sympy.

    The table was written by hand first and one entry was wrong — (6/35) is −1,
    not +1, because 6 ≡ −1 (mod 7) and 7 ≡ 3 (mod 4). The gate's implementation
    was right and the expectation was not. Both halves are kept: the table so
    the drill needs no dependency, and the sympy comparison because a
    hand-written table is exactly the thing that was wrong once.
    """
    cases = {(5, 11): 1, (11, 5): 1, (-1, 5): 1, (-1, 7): -1, (2, 7): 1,
             (2, 5): -1, (-696, 241): 1, (-696, 13): -1, (3, 11): 1,
             (6, 35): -1, (0, 1): 1, (5, 25): 0, (-3, 7): 1, (7, 15): -1,
             (-696, 5): 1,
             # every n above is odd, so the prime-2 branch of the symbol was
             # untested until these were added and a mutation to it went unseen
             (3, 8): -1, (5, 8): -1, (7, 8): 1, (3, 4): 1, (-1, 4): 1,
             (5, 12): -1, (7, 24): 1}
    if not all(fam16.kronecker(a, n) == v for (a, n), v in cases.items()):
        return False
    try:
        from sympy import kronecker_symbol
    except ImportError:                                   # pragma: no cover
        return True
    return all(fam16.kronecker(a, n) == int(kronecker_symbol(a, n))
               for (a, n) in cases)


def check_family_root_number() -> bool:
    """w(E^d) = w(E)·χ_d(−696) on twists whose sign is measurable numerically.

    d = 13 is the load-bearing one: it predicts −1, and a formula that always
    returned +1 would agree with the other four.
    """
    # 8,000 terms, not 30,000: the separations here run from 8e-3 to 2e-1 and
    # the series' drift is well below that, so the shorter sum decides the same
    # signs. This check runs once per defect and once per control, and at 30,000
    # it cost more E₁ evaluations than every other check put together.
    base = fam16.base_coefficients(8000)
    for d, want in ((5, 1), (13, -1), (17, 1), (37, 1), (41, 1)):
        if fam16.kronecker(-fam16.BASE_N, d) != want:
            return False
        a = fam16.twisted_coefficients(base[:8001], d)
        w, ev = anchor15.root_number(a, fam16.BASE_N * d * d, 8000)
        if w != want or not ev["decided"]:
            return False
    return True


def check_twist_model() -> bool:
    """The twisted model itself, which the root-number check never touches.

    E^(d) = [0, a₂d, 0, a₄d², a₆d³] scales the discriminant by exactly d⁶ and
    the real period by 1/√d. Nothing in `family-root-number` reads the model —
    it works off character-multiplied coefficients — so a wrong power of d on a₄
    was invisible there.
    """
    base_disc = anchor15.b_invariants(fam16.BASE)[4]
    base_omega = anchor15.real_period(fam16.BASE)
    for d in (5, 13, 241):
        inv = fam16.twist(fam16.BASE, d)
        if anchor15.b_invariants(inv)[4] != base_disc * d ** 6:
            return False
        if abs(anchor15.real_period(inv) - base_omega / math.sqrt(d)) > 1e-9:
            return False
    return True


def check_membership_in_P() -> bool:
    """𝒫's three conditions, by the members they actually select below 4,000."""
    members = [q for q in anchor15.sieve(4000) if fam16.in_P(q)]
    return members == [241, 313, 457, 673, 937, 1009, 1153, 1753, 2017, 2089,
                       2113, 2137, 2617, 2713, 3049, 3457, 3529, 3769, 3793]


def check_family_ordinary() -> bool:
    """a_p(696.e1) is odd exactly when f₂ is irreducible mod p — and not always.

    The second half matters: an argument that a_q is odd for q ∈ 𝒫 is worth
    nothing if a_p is odd for every p. Measured density is 0.3289 against
    Chebotarev's 1/3.
    """
    base = fam16.base_coefficients(4000)
    odd = tested = 0
    for p in anchor15.sieve(4000):
        if p <= 3 or fam16.BASE_N % p == 0:
            continue
        tested += 1
        is_odd = base[p] % 2 != 0
        odd += is_odd
        if is_odd != (ph2.cubic_root_count(ph2.F2, p) == 0):
            return False
    return tested > 200 and 0.25 < odd / tested < 0.42


TATE_FIXTURE = [
    # curve, a-invariants, conductor, {p: (Kodaira type, c_p)} — all fixed
    # outside this tree. 11a1's c_11 = 5 is the sharpest, because RUN-014
    # derived it independently from L/Ω = 1/5, torsion 5 and trivial Ш.
    ([0, -1, 1, -10, -20], 11, {11: ("I5", 5)}),
    ([1, 0, 1, 4, -6], 14, {2: ("I6", 2), 7: ("I3", 3)}),
    ([1, 1, 1, -10, -10], 15, {3: ("I4", 2), 5: ("I4", 4)}),
    ([0, 0, 1, 0, -7], 27, {3: ("IV*", 3)}),
    ([0, 0, 0, 4, 0], 32, {2: ("I3*", 4)}),
    ([0, 0, 0, 0, 1], 36, {2: ("IV", 3), 3: ("III", 2)}),
    ([0, 0, 0, -4, 0], 64, {2: ("I2*", 4)}),
    ([0, 1, 0, 8, -16], 696, {2: ("II*", 1), 3: ("I1", 1), 29: ("I1", 1)}),
    # additive at a prime >= 5, so the (v(c4), v(c6), v(disc)) table is used
    ([1, -1, 0, -2, -1], 49, {7: ("III", 2)}),
]


def check_tate() -> bool:
    """Conductor, Kodaira type and Tamagawa number on curves fixed elsewhere.

    The conductor is the demanding half: it is the product of the conductor
    exponents, so any wrong exponent shows up in it. 696.e1 at p = 2 is type
    II* with f = 3, which is what makes N = 696 rather than 1392.
    """
    for inv, N, expect in TATE_FIXTURE:
        primes = [q for q in (2, 3, 5, 7, 11, 13, 29, 37) if N % q == 0]
        got = {q: tate18.reduction_data(inv, q, want_c=True) for q in primes}
        prod = 1
        for q, d in got.items():
            prod *= q ** d["f"]
        if prod != N:
            return False
        for q, (kod, c) in expect.items():
            if got[q]["kodaira"] != kod or got[q]["c"] != c:
                return False
    return True


def check_tate_i0star_reachable() -> bool:
    """Type I0* must be returnable at all, on BOTH code paths.

    A first version of the step-7 normalisation demanded p³|a4 and p⁴|a6, which
    forces the cubic to T²(T+b) and makes I0* unreachable — and thirteen
    hand-picked curves plus two thousand census conductors all passed anyway.
    The twists of 696.e1 are I0* at their twisting prime, but that prime is
    ≥ 5 and never touches the step-7 search; only p = 2 and 3 do. So a curve
    that is I0* at 2 is here as well, and it is the one the over-tightening
    defect trips.
    """
    for q in (241, 313, 457):
        d = tate18.reduction_data(fam16.twist(fam16.BASE, q), q, want_c=True)
        if d["kodaira"] != "I0*" or d["f"] != 2 or d["c"] != 1:
            return False
    d = tate18.tate([0, -3, 0, -12, -8], 2)
    return d["kodaira"] == "I0*" and d["f"] == 4


def check_ogg() -> bool:
    """Ogg's formula f = v(Δ) − m + 1, which the gate never uses.

    m is the number of components of the special fibre and is a function of the
    Kodaira type alone. The algorithm computes f branch by branch and never
    consults this relation, so requiring it is an independent constraint on
    every exponent it returns rather than a restatement of one.
    """
    curves = [([0, -1, 1, -10, -20], 11), ([1, 0, 1, 4, -6], 2),
              ([1, 0, 1, 4, -6], 7), ([0, 0, 1, 0, -7], 3),
              ([0, 0, 0, 4, 0], 2), ([0, 0, 0, 0, 1], 2),
              ([0, 0, 0, 0, 1], 3), ([0, 0, 0, -4, 0], 2),
              ([0, 1, 0, 8, -16], 2), ([0, 1, 0, 8, -16], 3),
              ([0, 1, 0, 8, -16], 29), ([1, -1, 0, -2, -1], 7),
              ([0, -3, 0, -12, -8], 2)]
    for inv, q in curves:
        d = tate18.reduction_data(inv, q)
        kod = d["kodaira"]
        if kod.endswith("*") and kod[1:-1].isdigit():
            m = 5 + int(kod[1:-1])
        elif kod.startswith("I") and kod[1:].isdigit():
            m = max(1, int(kod[1:]))
        else:
            m = tate18.COMPONENTS.get(kod)
        if m is None:
            return False
        if d["f"] != d["v_disc"] - m + 1:
            return False
    return True


def check_real_period_against_integration() -> bool:
    """Ω by AGM against Ω by numerical integration over E(R).

    The AGM branch for Δ > 0 was wrong by a factor of two and no check could
    see it, because the only thing it was ever compared with was itself: a
    drill baseline frozen from this same function. Integrating dx/√(4x³+b₂x²+
    2b₄x+b₆) over the real locus — the unbounded component substituted
    x = e₁ + t², the egg substituted x = e₃ + (e₂−e₃)sin²u — shares no code
    with the AGM and settles it.
    """
    try:
        from scipy import integrate
    except ImportError:                                   # pragma: no cover
        return True
    for inv in ([0, -1, 1, -10, -20], [0, 0, 1, -1, 0], [0, 1, 1, -2, 0],
                [0, 1, 0, 8, -16], [1, 0, 0, -3, 1]):
        b2, b4, b6, _b8, disc = anchor15.b_invariants(inv)

        def f(x):
            return 4 * x ** 3 + b2 * x * x + 2 * b4 * x + b6

        roots = anchor15.real_cubic_roots(b2, b4, b6)
        e1 = roots[0]
        total, _ = integrate.quad(
            lambda t: 4 * t / math.sqrt(f(e1 + t * t)), 0, math.inf, limit=800)
        if len(roots) == 3:
            _e1, e2, e3 = roots
            span = e2 - e3
            egg, _ = integrate.quad(
                lambda u: 4 * span * math.sin(u) * math.cos(u)
                / math.sqrt(max(f(e3 + span * math.sin(u) ** 2), 1e-300)),
                0, math.pi / 2, limit=800)
            total += egg
        if abs(anchor15.real_period(inv) - total) > 1e-7 * total:
            return False
    return True


def check_regulator() -> bool:
    """389.a1's height regulator, guarded by an identity the method never uses.

    The parallelogram law ĥ(P+Q) + ĥ(P−Q) = 2ĥ(P) + 2ĥ(Q) is not an input to
    the limit that computes ĥ, so requiring it constrains the whole computation
    from outside. The regulator value is pinned as well, but the law is what
    makes the value mean something.
    """
    # depth 8, not the gate's 10: the limit's cost grows with 4ⁿ-digit integers
    # and this runs once per defect and once per control — 0.17s against 30s.
    # The tolerances are what depth 8 delivers (parallelogram residual 2.4e-5,
    # regulator within 7e-6 of the depth-10 value), not what depth 10 does.
    r = bsd20.regulator(bsd20.P5_CURVE, bsd20.P5_GENERATORS, depth=8)
    return (abs(r["parallelogram_law_residual"]) < 1e-4
            and abs(r["regulator"] - 0.152460306865) < 2e-5
            and r["independent"])


def check_bsd_sweep() -> bool:
    """The rank-0 BSD identity must close on an integer square — and on 1.

    Six curves, not a sweep: this runs once per defect and once per control, so
    the full sweep that gate 20 reports would cost more here than every other
    check put together — and 1,200 terms rather than 3,000, which still decides
    every sign in this set and cuts the point counting by an order of magnitude. The identity is the same one either way, and it is the
    thing that puts four independently computed quantities — the L-value, the
    real period, the torsion bound and every Tamagawa number — into a single
    equation that must land on an integer.
    """
    curves = [r for r in json.loads(x0n.ARITH.read_text(encoding="utf-8"))["records"]
              if r["curve_label"] in ("14a1", "26a1", "34a1", "38b1",
                                      "46a1", "94a1")]
    sw = bsd20.sweep(curves, limit=1200)
    return (sw["tally"].get("BSD closes: a positive integer square", 0) == 6
            and sw["Sha_values_where_it_closes"] == {"1": 6})


def check_two_witness_degrees() -> bool:
    """[K_E:Q], e_E and the density for 696.e1, by exact F₂ linear algebra.

    A multiquadratic field's degree is 2^r with r the F₂-rank of the exponent
    vectors of the squarefree parts, and the same rank decides whether the
    quadratic resolvent lies inside K_E. Both are integers, so this check has no
    tolerance at all.
    """
    coords = [-1, 2, 3, 29]
    gens = [-1, 2, tw21.star(3), tw21.star(29)]
    vecs = [tw21.exponent_vector(tw21.squarefree_part(g), coords) for g in gens]
    if any(v is None for v in vecs):
        return False
    if tw21.f2_rank(vecs) != 4:
        return False
    # the sign convention cannot matter: √−1 is already in K_E, so ℓ* and ℓ
    # generate the same extension. Measured rather than asserted.
    flipped = [tw21.exponent_vector(tw21.squarefree_part(g), coords)
               for g in (-1, 2, 3, -29)]
    if tw21.f2_rank(flipped) != 4:
        return False
    resolvent = tw21.squarefree_part(-11136 * 16)        # disc of 4x³+b₂x²+…
    if tw21.squarefree_part(-174) != -174:
        return False
    if not tw21.in_span(tw21.exponent_vector(-174, coords), vecs):
        return False
    # and a resolvent that is NOT inside must be reported as not inside
    return not tw21.in_span(tw21.exponent_vector(-7, [-1, 2, 3, 7, 29]),
                            [tw21.exponent_vector(tw21.squarefree_part(g),
                                                  [-1, 2, 3, 7, 29])
                             for g in gens])


TRUNCATION = 1_200          # measured: see check_analytic_classification
_CANDIDATE_MEMO = []


def _candidates():
    """`certificate_candidates(30, 30)`, computed once.

    The two checks that use it test the CLASSIFIERS that read a candidate, not
    the search that produces one, so the list is taken at baseline and reused.
    That is a scope statement rather than an optimisation excuse: neither check
    can see a defect planted inside the search, and neither claims to. The cost
    matters — the drill runs every check once per defect, so a 1.5-second scan
    inside a check is a 2‑minute tax on the run.
    """
    if not _CANDIDATE_MEMO:
        _CANDIDATE_MEMO.extend(net22.certificate_candidates(30, 30))
    return _CANDIDATE_MEMO


def check_witness_lemmas() -> bool:
    """Lemmas 2.1/2.2 and the leave-one-out form, on witness sets built here.

    These are elementary — "no ℓ has p ∤ n_ℓ" is "p divides every n_ℓ" is
    "p | gcd" — so the fixtures are chosen to hit the places an implementation
    slips: a single multiplicative prime (where the gcd is that one value), a
    set whose gcd is even but not a power of two, and the leave-one-out form at
    a prime that is itself in M.
    """
    cases = [
        ({"M": {3: 1, 29: 1}, "M_minus": {29: 1}}, [], 1, 1),
        ({"M": {3: 3, 5: 6}, "M_minus": {5: 6}}, [3], 3, 6),
        ({"M": {7: 4, 11: 2}, "M_minus": {11: 2}}, [], 2, 2),
        ({"M": {5: 15}, "M_minus": {5: 15}}, [3, 5], 15, 15),
    ]
    for ws, want_R, want_g, want_gm in cases:
        g = net22.gcds(ws)
        if g["g_mult"] != want_g or g["g_minus"] != want_gm:
            return False
        if g["R"] != want_R:
            return False
        for q in (3, 5, 7, 11, 13):
            if not net22.lemma_21_holds(ws, q):
                return False
        for q in ws["M"]:
            r = net22.loo(ws, q)
            if "gcd_form_agrees" in r and not r["gcd_form_agrees"]:
                return False
    # M∖{p} empty must be reported as a failure, not silently as a pass
    if net22.loo({"M": {5: 15}, "M_minus": {5: 15}}, 5)["holds"] is not False:
        return False
    # and the one shape that separates "leave p out" from "keep p in": every
    # OTHER valuation divisible by p, while n_p itself is not. Without this the
    # two behave identically on every fixture above.
    ws = {"M": {3: 1, 5: 3, 7: 6}, "M_minus": {5: 3}}
    return net22.loo(ws, 3)["holds"] is False


def check_analytic_classification() -> bool:
    """The four outcomes `analytic_side` has to keep apart, on real candidates.

    Non-emptiness of `31`'s domain is a claim about the whole certificate, not
    only its arithmetic half, so the analytic verdict is load-bearing and its
    failure modes are the interesting part: an undecided root number must not
    be read as +1, and (T1)'s ord₂ condition is about L^alg = L/Ω and not about
    the BSD quotient. The fixtures are four of the 38 network-only candidates,
    one per outcome, and the two that reach rank 0 disagree on ord₂ — which is
    what makes the second count separable from the first.

    Run at 1,200 terms, which is **measured, not chosen**: it is the smallest
    truncation at which all four verdicts agree with the 4,000-term run. At 800
    the `w = −1` curve is still undecided and at 400 the rank-0 one reads as
    rank ≥ 2, so a looser fixture would test a different classification than the
    gate reports.
    """
    want = {
        (0, -1, 0, -11, -18): "root number undecided at this truncation",
        (0, -1, 0, -8, -15): "w = −1, so the rank is odd",
        (0, -1, 0, 0, -27): "rank 0",
        (0, -1, 0, 18, 11): "rank 0",
    }
    fix = [c for c in _candidates() if tuple(c["ainvs"]) in want]
    if len(fix) != 4:
        return False
    r = net22.analytic_side(fix, limit=TRUNCATION)
    if {row["status"] for row in r["rows"]} != set(want.values()):
        return False
    for row in r["rows"]:
        if want[tuple(row["ainvs"])] != row["status"]:
            return False
    # two reach rank 0, and exactly one of those two has ord₂ L^alg = 0:
    # [0,−1,0,0,−27] has c₂ = 2 and L/Ω = 2, so its BSD quotient is 1 — odd —
    # while the quantity (T1) actually names is even.
    if not (r["with_rank_zero_and_consistent"] == 2
            and r["and_with_ord_2_L_alg_zero"] == 1):
        return False
    # The sign condition here is INHERITED from src15, not enforced locally:
    # `analyse` returns L = None when the root number is undecided and L = 0.0
    # exactly when w = −1. Gate 22 relies on that, so it is asserted rather than
    # assumed — see the matching control. It is a statement about src15's return
    # shape and not about these curves, so it is asserted on the cheapest pair
    # that produces both branches: 37a1 has w = −1, and 100 terms leaves the
    # sign of 696.e1 undecided.
    odd = anchor15.analyse("37a1", [0, 0, 1, -1, 0], 37, limit=400)
    if odd["root_number"] != -1 or odd["L_at_1"] != 0.0:
        return False
    vague = anchor15.analyse("696.e1", [0, 1, 0, 8, -16], 696, limit=100)
    return not (vague["root_number_undecided"] and vague["L_at_1"] is not None)


def check_criterion_reach() -> bool:
    """Which of `30`, `31` reaches a candidate — the round's headline number.

    Four hand-built witness sets, one per cell, where the answer is decidable by
    reading it: (T4) wants an odd multiplicative prime of valuation exactly 1,
    (T5) wants a NONSPLIT one of valuation exactly 1, and the two sets are not
    the same set. Then the invariant, asserted over the whole search population
    rather than the fixtures: (T4) and (T5) each supply a valuation 1, so both
    gcds collapse to 1 and the exceptional set MUST be empty whenever `30`
    applies. A classifier that read (T5) against M instead of M⁻, or accepted
    any odd valuation, would put candidates in that impossible cell.
    """
    cases = [
        ({"M": {3: 1, 29: 1}, "M_minus": {29: 1}}, [], True, True, True),
        ({"M": {5: 1, 7: 3}, "M_minus": {7: 3}}, [3], True, False, False),
        ({"M": {3: 1, 11: 2}, "M_minus": {11: 2}}, [], True, False, False),
        ({"M": {3: 2, 11: 2}, "M_minus": {11: 2}}, [], False, False, False),
    ]
    for ws, want_R, t4, t5, thirty in cases:
        c = {"M": {str(k): v for k, v in ws["M"].items()},
             "M_minus": {str(k): v for k, v in ws["M_minus"].items()},
             "R": want_R}
        v = net22.which_criterion_applies(c)
        if (v["T4_satisfiable"], v["T5_satisfiable"],
                v["criterion_30_applies"]) != (t4, t5, thirty):
            return False
        if v["exceptional_set_empty"] != (not want_R):
            return False
    cands = _candidates()
    if len(cands) < 100:
        return False
    impossible = sum(1 for c in cands
                     if net22.which_criterion_applies(c)["criterion_30_applies"]
                     and c["R"])
    return impossible == 0


def check_p5_formal_group() -> bool:
    """v0.8's boxed chain at 389.a1, p = 11, from the group law up.

    The load-bearing step is v_11(t(16P')) = 1 with t(16P')/11 ≡ 7 (mod 11):
    16 = #E(F_11) puts 16P' in the formal group, and the residue is what makes
    the later cancellation exact rather than approximate. Everything the
    document boxes is derived from that one number, so the fixture pins the
    number and each derived residue separately — a check that only asserted
    u_loc ≡ 4 would pass on a wrong t whose errors cancelled.
    """
    from fractions import Fraction
    A, B, Ps = p5u.minimal_to_short(p5u.AINVS, (Fraction(0), Fraction(0)))
    if (A, B) != (-3024, 46224) or Ps != (Fraction(12), Fraction(108)):
        return False
    if Ps[1] ** 2 != Ps[0] ** 3 + A * Ps[0] + B:
        return False
    n11 = p5u.point_count(p5u.AINVS, 11)
    if n11 != 16:
        return False
    # the inverse change of model is used to name 3P + Q on the minimal model,
    # so it round-trips rather than being trusted
    for pt in ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))):
        if p5u.short_to_minimal(p5u.minimal_to_short(p5u.AINVS, pt)[2]) != pt:
            return False
    R = p5u.short_mul(A, n11, Ps)
    t = -Fraction(R[0]) / Fraction(R[1])
    v, _ = p5u.valuation(t, 11)
    if v != 1 or p5u.unit_residue(t / 11, 11) != 7:
        return False
    # the two derived residues, each pinned rather than inferred
    inv16 = pow(n11 % 11, -1, 11)
    if (7 * inv16) % 11 != 8:                       # log_{omega'}(P')/11
        return False
    if (8 * 6) % 11 != 4:                           # the factor 6 from omega'/omega
        return False
    trunc = (Fraction(1) - Fraction(11 + 1 - n11, 11) + Fraction(1, 11)) *             (Fraction(1) - Fraction(1, 389))
    vt, _ = p5u.valuation(trunc, 11)
    return vt == -1 and p5u.unit_residue(trunc * 11, 11) == 1


def check_p5_residue_homomorphism() -> bool:
    """R ↦ [t(16R)/11] is a homomorphism E(Q) → Z/11 with an index-11 kernel.

    This is what makes v0.8's "exactly one positive power of 11" a statement
    about the chosen basis vector rather than about the curve, so the check
    pins both halves: the homomorphism law on every small combination, and an
    explicit Z-basis whose first vector lands in the kernel.
    """
    A = -3024
    h = p5u.residue_homomorphism(A, 16)
    if not h["generators_are_on_the_curve"] or not h["is_a_homomorphism"]:
        return False
    if (h["phi(P)"], h["phi(Q)"]) != (7, 1) or not h["surjective"]:
        return False
    if h["combinations_tested"] < 40 or h["mismatches"]:
        return False
    ab = h["an_alternative_Z_basis"]
    return (ab["is_a_basis"] and abs(ab["determinant"]) == 1
            and ab["v_11_of_the_first_vector"] == 2)


def check_p5_chain_inputs() -> bool:
    """`IMC_Closure_and_GPR_Bridge_v0.5` §1.2's declared inputs, recomputed.

    N = 389, a single bad prime of type I_1 with c = 1 so the Tamagawa product
    is 1, trivial torsion, and 11 good ordinary. The check also pins that the
    gate still LISTS what it did not check — a version that quietly dropped the
    cited-not-verified list would read as more coverage than there is.
    """
    ci = p5u.imported_curve_data()
    if not (ci["conductor_agrees"] and ci["prod_c_agrees"]
            and ci["torsion_agrees"] and ci["good_ordinary_at_11"]):
        return False
    if ci["bad_primes"] != [389] or ci["a_11"] != -4:
        return False
    return len(ci["still_cited_not_checked"]) >= 4


def check_p5_ledger_extraction() -> bool:
    """The ledger scan finds every fenced status row, including the awkward ones.

    The row count is pinned deliberately. The first version of the gate's status
    pattern used a word boundary, which does not match inside
    `CLOSED_BY_PUBLISHED_COMPUTATION`, and it silently dropped fourteen rows —
    among them both readings of the one gate the reconciliation exists to
    compare. A scan that under-reports produces a shorter table, not an error,
    so the count is the check.
    """
    per_doc = led24.extract_rows()
    total = sum(len(v) for v in per_doc.values())
    if len(per_doc) < 4 or total < 44:
        return False
    flat = {(r["gate"], r["status"]) for rows in per_doc.values() for r in rows}
    needed = {
        ("P5-BOC-NZ11", "PENDING FINITE SAGEMATH REPLAY"),
        ("P5-BOC-NZ11", "CLOSED_BY_PUBLISHED_COMPUTATION"),
        ("P5-LAT11", "EQUIVALENT_TO_uGPR11"),
        ("P5-RAT", "BLOCKED BY P5-DERPER"),
        ("P5-IMC11", "CLOSED"),
    }
    return needed <= flat


def check_p5_ledger_reconcile() -> bool:
    """The verdict rule, the name canonicalisation and the cycle detector.

    `OPEN` and `BLOCKED BY X` are the same verdict at different resolution, so a
    reconciliation that called their difference a conflict would report noise;
    `CLOSED` against either is real. The canonicaliser restores a `P5-` prefix
    only when exactly one declared gate matches, which is what leaves
    `P5-LAT11 -> GPR11` visible as ambiguous instead of silently resolved.
    """
    if led24._verdict("CLOSED_BY_PUBLISHED_COMPUTATION") != "CLOSED":
        return False
    if led24._verdict("BLOCKED BY P5-RAT") != "NOT-CLOSED":
        return False
    if led24._verdict("OPEN / ARCHIMEDEAN RANK-2 PERIOD COMPARISON") != "NOT-CLOSED":
        return False
    if led24._verdict("PENDING FINITE SAGEMATH REPLAY") != "NOT-CLOSED":
        return False
    names = {"P5-GPR11", "P5-FULL-GPR11", "P5-uGPR11", "P5-BOC-NZ11"}
    if led24._canon("BOC-NZ11", names) != "P5-BOC-NZ11":
        return False
    if led24._canon("GPR11", names) != "GPR11":       # three candidates: unresolved
        return False
    per_doc = led24.extract_rows()
    g = led24.blocking_graph(per_doc)
    if not g["is_acyclic"] or len(g["edges_whose_target_is_ambiguous"]) != 1:
        return False
    amb = g["edges_whose_target_is_ambiguous"][0]
    if sorted(amb["candidates"]) != ["P5-FULL-GPR11", "P5-GPR11", "P5-uGPR11"]:
        return False
    # the cycle detector on a synthetic input, since the corpus has no cycle and
    # a detector that never fires would pass every real-data check
    fake = {"f.md": [{"gate": "A", "status": "BLOCKED BY B", "line": ""},
                     {"gate": "B", "status": "BLOCKED BY A", "line": ""}]}
    return led24.blocking_graph(fake)["is_acyclic"] is False


def check_p5_gates_closed_here() -> bool:
    """The two gates this arm closes on its own evidence, and why they hold.

    `P5-RESIDUAL-IRR11` because `j(389.a1) = 1404928/389` is not one of the three
    non-cuspidal `j` on `X₀(11)` — it is not even an integer — and separately
    because the curve is semistable. `P5-BOC-NZ11` because RUN-011 recomputed
    `det(M_loc) = 2`. The check pins the arithmetic, not the prose.
    """
    from fractions import Fraction
    a = led24.gates_this_arm_can_close()
    ind = {g["gate"]: g for g in a["closed_here_on_independent_grounds"]}
    if set(ind) != {"P5-RESIDUAL-IRR11", "P5-BOC-NZ11"}:
        return False
    irr = ind["P5-RESIDUAL-IRR11"]
    r1 = irr["route_1_X0_11"]
    if r1["j"] != "1404928/389" or r1["j_is_an_integer"] or r1["j_is_one_of_them"]:
        return False
    if sorted(r1["three_non_cuspidal_j_on_X0(11)"]) != [-24729001, -32768, -121]:
        return False
    if not irr["route_2_semistability_and_Mazur"]["semistable"]:
        return False
    if not all(g["closed_by_this_arm"] for g in ind.values()):
        return False
    return len(a["cited_and_not_checked"]) >= 4


def check_p5_selmer_cube() -> bool:
    """v1.2's boxed Selmer cube, from the two localization rows.

    Every number the document boxes is pinned separately, because they are all
    consequences of one determinant and a check that asserted only the last of
    them would pass on wrong intermediate lines whose errors cancelled: the two
    kernel lines `Q − 2P` and `Q − 4P`, the dimensions `2 → 1, 2 → 1, 1∩1 → 0`,
    the cardinalities `121 → 11 → 1`, and `det = 2`.
    """
    rows = {397: (1, 2), 991: (1, 4)}
    c = cv25.selmer_cube(rows)
    if c["determinant"] != 2 or not c["agrees"]:
        return False
    if c["kernel_lines_as_written_by_the_document"] != {"397": "Q - 2P",
                                                        "991": "Q - 4P"}:
        return False
    if c["cardinalities"] != [121, 11, 1]:
        return False
    if c["dimensions"] != {"empty": 2, "397": 1, "991": 1, "both": 0}:
        return False
    # a degenerate pair must collapse the cube rather than silently keep it
    d = cv25.selmer_cube({397: (1, 2), 991: (1, 2)})
    if d["determinant"] != 0 or d["dimensions"]["both"] != 1:
        return False
    one = cv25.the_three_statements_are_one(rows)
    return (one["det_equals_k_difference"] and one["all_three_agree"]
            and one["selmer_both_vanishes"] and one["faces_are_transverse"])


def check_p5_core_vertex_pairs() -> bool:
    """Row shapes and the pair arithmetic, on real directions and synthetic ones.

    Run at scan 3,000 rather than the gate's 20,000: below 6,000 every row is
    `(1, k)` and the only skip reason is `v₁₁ = 0`, so the real data exercises
    the common path and nothing else. The two structural cases the corpus only
    produces near 20,000 — a `(0, 1)` row and a `(0, 0)` one — are supplied as
    fixtures, because a classifier whose other branches are never taken is not
    tested by the scan that never reaches them.
    """
    # the valuation predicate, tested directly: 19867 is the only prime below
    # 20,000 with v >= 2, so no fixture cheap enough to run per defect reaches
    # that branch through the scan
    if [cv25.admissible_valuation(v) for v in (0, 1, 2, 3)] != [False, True,
                                                                False, False]:
        return False
    adm = cv25.admissible_rows(3000)
    if len(adm["rows"]) != 4 or adm["row_shapes"] != {"(1, k)": 4}:
        return False
    if 397 not in adm["rows"] or adm["rows"][397] != (1, 2):
        return False
    if 991 not in adm["rows"] or adm["rows"][991] != (1, 4):
        return False
    s = cv25.pair_scan(adm["rows"])
    if s["pairs_total"] != 6 or s["pairs_giving_a_core_vertex"] > 6:
        return False
    # a (0, 1) row pairs non-degenerately with every (1, k) row: det = 1
    synth = cv25.pair_scan({7: (1, 3), 11: (1, 3), 13: (0, 1)})
    if synth["pairs_total"] != 3 or synth["pairs_that_degenerate"] != 1:
        return False
    if synth["directions_with_a_(0,1)_row"] != [13]:
        return False
    # and equal k must degenerate
    return cv25.pair_scan({7: (1, 5), 11: (1, 5)})["pairs_giving_a_core_vertex"] == 0


_RANK2_ROOTS = (-2.040302200338, 0.135409240240, 0.904892960098)


def check_rank2_real_period() -> bool:
    """389.a1's real period, three ways, on the Δ > 0 branch RUN-017 repaired.

    The two real components must agree with each other and their sum with the
    AGM, and one component must be **exactly half** the AGM value — that last
    equality is the whole content of RUN-017's fix, and pinning it means the
    factor of two cannot come back silently.

    The unbounded integral's `2/T` tail is asserted by running two different
    cut-offs: a wrong closed form would leave a T-dependent residue, which one
    cut-off alone cannot see.
    """
    e3, e2, e1 = _RANK2_ROOTS
    if len(r2bsd.cubic_real_roots(4, 4, -8, 1)) != 3:    # b2 = 4, 2b4 = −8, b6 = 1
        return False
    egg = r2bsd.period_bounded_component(e3, e2, e1, n=4000)
    u1 = r2bsd.period_unbounded_component(e3, e2, e1, n=20_000, T=1000.0)
    u2 = r2bsd.period_unbounded_component(e3, e2, e1, n=20_000, T=2000.0)
    if abs(u1["corrected"] - u2["corrected"]) > 1e-6:     # the tail form
        return False
    if abs(egg - u1["corrected"]) > 1e-6:
        return False
    agm = anchor15.real_period(r2bsd.AINVS)
    if abs((egg + u1["corrected"]) - agm) > 1e-6:
        return False
    return abs(egg / agm - 0.5) < 1e-9


def check_rank2_bsd_identity() -> bool:
    """L''(E,1)/2! = Ω·Reg·∏c_p/#tors² at 389.a1, with the document's numbers.

    Closes to machine precision with this arm's AGM period and the rank-uniform
    document's regulator. The sensitivity is asserted alongside the agreement:
    halving the period must send the ratio to 2, which is exactly the failure
    RUN-017 found and is the reason this check exists on a Δ > 0 curve.
    """
    agm = anchor15.real_period(r2bsd.AINVS)
    pred = agm * r2bsd.DOC_REG * r2bsd.DOC_TAMAGAWA / (r2bsd.DOC_TORSION ** 2)
    if abs(r2bsd.DOC_L2 / pred - 1.0) > 1e-12:
        return False
    halved = (agm / 2) * r2bsd.DOC_REG
    if abs(r2bsd.DOC_L2 / halved - 2.0) > 1e-12:
        return False
    # And our own regulator must land inside its own accuracy. Run at doubling
    # depth 8, whose cost is 0.17s against depth 10's 30s — the drill runs every
    # check once per defect, so depth 10 here would add three quarters of an
    # hour. The tolerance is set to what depth 8 MEASURES: the differences from
    # the document's value are 2.4e-04, 5.8e-05, 7.0e-06, 1.3e-07 at depths
    # 6, 7, 8, 10, so 2e-05 passes depth 8 and fails depth 7. A tolerance of
    # 2e-06 would be depth 10's and would make this check fail on its own
    # settings; the gate still reports the depth-10 value.
    reg = bsd20.regulator(r2bsd.AINVS, r2bsd.GENS, depth=8)["regulator"]
    return abs(reg - r2bsd.DOC_REG) < 2e-5


def check_corpus_hashing() -> bool:
    """Gate 00 matches the corpus by CONTENT, and its hash is a real SHA-256.

    The whole gate rests on one property: two documents are the same document
    when their bytes are, whatever they are called. So the check pins a known
    SHA-256 vector, then the two cases the property is about — the same bytes
    under different names must collide, different bytes under the same name must
    not — and finally that the curated corpus is the 85 documents every later
    round assumes.
    """
    if corpus00.sha256_bytes(b"") != (
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"):
        return False
    if corpus00.sha256_bytes(b"abc") != (
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"):
        return False
    if corpus00.sha256_bytes(b"x") == corpus00.sha256_bytes(b"y"):
        return False
    docs = corpus00.curated_docs()
    if len(docs) != 85:
        return False
    if {d["subline"] for d in docs} != {"phase0", "p5", "phase1", "phase2"}:
        return False
    return all(len(d["sha256"]) == 64 and d["bytes"] > 0 for d in docs)


def check_ladder_rungs() -> bool:
    """Gate 01's eleven rungs, and the boundary C1 must not steal from C10.

    The ladder's whole purpose is the C2/C3 split between evidence and proof, so
    a rung vocabulary that miscounts is a vocabulary that can hide the split.
    """
    rungs = ladder01.defined_rungs()
    if set(rungs) != {f"C{i}" for i in range(11)}:
        return False
    if ladder01.rungs_in("reached C3 after C2") != {"C2", "C3"}:
        return False
    if ladder01.rungs_in("C10 only") != {"C10"}:          # not also C1
        return False
    # The word boundaries, tested where they actually decide something. A
    # greedy \d{1,2} already reads "C10" as one token, so that fixture cannot
    # tell `\bC(\d{1,2})\b` from `C(\d{1,2})`. These two can: without the
    # trailing boundary "C123" yields a spurious C12, and without the leading
    # one "ABC10" yields a C10 that is not a rung reference at all.
    if ladder01.rungs_in("the constant C123 appears") != set():
        return False
    if ladder01.rungs_in("variable ABC10 in a formula") != set():
        return False
    # code fences must NOT be stripped — the abbreviated ladders in this corpus
    # all live inside them, and an earlier version went blind by filtering
    fenced = "text\n```\nC0 -> C1 -> C10\n```\n"
    return ladder01.rungs_in(fenced) == {"C0", "C1", "C10"}


def check_rejected_route_verdicts() -> bool:
    """Gate 02's salvage-condition verdicts, negation and distance included.

    Both faults this check exists for are pinned. A same-line window cannot
    reach the corpus's verdict, which sits four lines below the last `GR-n`
    heading — so all six mentions must come back `stated unmet`, never `no
    verdict nearby`. And a detector without negation reads 未滿足 as 滿足 — so
    the fixtures put the two side by side.
    """
    fx = route02.classify_salvage("## GR-1: something\n\nGR-1 已滿足。")
    if [r["verdict"] for r in fx] != ["claimed met", "claimed met"]:
        return False
    fx = route02.classify_salvage("## GR-2: something\n\n目前四項皆未完成。")
    if any(r["verdict"] != "stated unmet" for r in fx):
        return False
    fx = route02.classify_salvage("GR-3 appears with no verdict anywhere near it")
    if [r["verdict"] for r in fx] != ["no verdict nearby"]:
        return False
    audit = (route02.CURATED / "phase0" / "files" / route02.AUDIT)
    rows = route02.classify_salvage(audit.read_text(encoding="utf-8"))
    if len(rows) != 6:
        return False
    counts = collections.Counter(r["verdict"] for r in rows)
    return (counts["stated unmet"] == 6 and counts["claimed met"] == 0
            and counts["no verdict nearby"] == 0)


def check_multiplicity_order() -> bool:
    """Gate 03's order at zero, on exact rationals.

    The no-go it recomputes is about an integer-valued order, so a float would
    answer a different question; the fixtures are Fractions and include the one
    that separates order from degree.
    """
    F = Fraction
    if nogo03.order_at_zero({1: F(1), 2: F(1)}) != 1:      # z(z + 1)
        return False
    if nogo03.order_at_zero({2: F(1)}) != 2:               # z^2
        return False
    if nogo03.order_at_zero({1: F(0), 2: F(1)}) != 2:      # a zero coefficient
        return False
    if nogo03.order_at_zero({0: F(3), 5: F(1)}) != 0:      # order 0, degree 5
        return False
    try:
        nogo03.order_at_zero({0: F(0), 3: F(0)})
    except ValueError:
        return True
    return False


def check_sha_labelling() -> bool:
    """Gate 27's analytic-vs-actual Sha scan, and the three ways it went wrong.

    Each correction the gate needed is now a fixture, because each was a silent
    under-report rather than an error:

      * the claim pattern must survive a NESTED subscript. `_{\\mathrm{an}}` has
        an inner brace, and a `[^}]` class stops at it — five real analytic
        claims were lost that way, including the specification document's own.
      * `\\Sha_{\\rm an}` is analytic **by its notation**, before any
        surrounding vocabulary is consulted.
      * a required hypothesis and an inherited value are labelled, in their own
        ways, and counting them as unlabelled inflates the finding.
    """
    C = agent27.SHA_CLAIM
    if not C.search(r"\Sha_{\mathrm{an}}=1"):
        return False
    if not C.search(r"\Sha_{\rm an}(E')=0"):
        return False
    if not C.search(r"#\Sha(E/\mathbb Q)[11^\infty]=1"):
        return False
    if C.search(r"\text{P4 Sha-control closed at }p=11"):   # not a claim
        return False
    m = C.search(r"\Sha_{\mathrm{an}}=1")
    if agent27.classify_claim("no vocabulary here", m.group("sub"))[1] != "analytic":
        return False
    if agent27.classify_claim("再要求", None)[1] != "hypothesis":
        return False
    if agent27.classify_claim("the inherited closure gives", None)[1] != "provenance":
        return False
    if agent27.classify_claim("this is not proved anywhere", None)[1] != "":
        return False
    s = agent27.scan()
    c = s["verdict_counts"]
    if s["numeric_Sha_claims_found"] < 36:
        return False
    return (c.get("analytic by its own subscript", 0) == 5
            and c.get("unlabelled in window", 0) == 3
            and c.get("stated as a hypothesis", 0) == 9)


def check_rank1_leading_derivative() -> bool:
    """L'(E,1) = 2 Σ (a_n/n) E₁(2πn/√N) at 37a1, and the pieces it stands on.

    Run at 800 terms, which is **measured, not chosen**: `E₁(2πn/√37)` decays
    exponentially and the sum is at full double precision by then — 800 terms
    give the identical value to 20,000, at 0.07s against 32.
    """
    d = r1bsd.leading_derivative([0, 0, 1, -1, 0], 37, limit=800)
    if d["root_number"] != -1 or not d["root_number_decided"]:
        return False
    if abs(d["value"] - 0.30599977383405214) > 1e-13:
        return False
    if d["converged_to"] != 0.0:
        return False
    # E₁ itself, against values it must reproduce: E₁(1) = 0.2193839344,
    # and the two branches must agree across the x = 2 switch
    if abs(anchor15.E1(1.0) - 0.21938393439552029) > 1e-12:
        return False
    lo = anchor15.E1(1.9999999)
    hi = anchor15.E1(2.0000001)
    return abs(lo - hi) < 1e-7


def check_rank1_identity() -> bool:
    """Ω·ĥ(P)·∏c_p/#tors² against L'(E,1), at 37a1 and 43a1.

    Both period branches: 37a1 has Δ > 0 and two real components, 43a1 has
    Δ < 0 and one, so a fault in either branch of `real_period` shows here.

    Run at doubling depth 10 with **per-curve tolerances set to what depth 10
    delivers**, not to what the gate achieves: 37a1 closes to 1.7e-09 there and
    43a1 only to 2.9e-06, because 43a1's height needs depth 12 to converge. A
    single loose tolerance would let a real 37a1 regression through; a single
    tight one would fail on 43a1's own settings. The gate itself runs depths 10,
    11 and 12 and reports the trend.
    """
    for ainvs, N, gen, want, tol in (
            ([0, 0, 1, -1, 0], 37, [0, 0], 0.30599977383405214, 1e-8),
            ([0, 1, 1, 0, 0], 43, [0, 0], 0.3435239746184784, 1e-5)):
        d = r1bsd.leading_derivative(ainvs, N, limit=800)
        if abs(d["value"] - want) > 1e-12:
            return False
        omega = anchor15.real_period(ainvs)
        h = bsd20.canonical_height(ainvs, gen, depth=10)["value"]
        prod_c = 1
        for p in anchor15.sieve(N):
            if N % p == 0:
                prod_c *= tate18.reduction_data(ainvs, p, want_c=True)["c"]
        tors = anchor15.torsion_bound(ainvs, N)
        pred = omega * h * prod_c / (tors ** 2)
        if abs(d["value"] / pred - 1.0) > tol:
            return False
        # and the sensitivity, so a doubled period cannot pass quietly
        if abs(d["value"] / (2 * pred) - 0.5) > tol:
            return False
    return True


def check_height_level_selection() -> bool:
    """The extrapolation level is chosen by measurement, not fixed at the deepest.

    RUN-026 found `richardson2` returned unconditionally, and wrong: at 37a1 the
    raw sequence's last two agree to ~1e-14 while r1's differ by ~2.5e-07, and
    r2 is built from r1's last two. So the check pins that the gaps really are
    ordered that way, that `raw` is chosen, and that the regulator's uniform
    parallelogram selection beats every fixed level.
    """
    h = bsd20.canonical_height([0, 0, 1, -1, 0], [0, 0], depth=10)
    g = h["level_gaps"]
    if h["chosen_level"] != "raw" or g["raw"] > 1e-12:
        return False
    if not (g["richardson1"] > 1e-8 and g["richardson2"] > 1e-8):
        return False
    if abs(h["value"] - h["raw_last"]) > 0:
        return False
    if abs(h["richardson2"] - h["raw_last"]) < 1e-9:      # they really differ
        return False
    r = bsd20.regulator([0, 1, 1, -2, 0], [[0, 0], [1, 0]], depth=8)
    res = r["residual_at_each_level"]
    chosen = r["extrapolation_level"]
    # All three levels must be present and the choice must be one of them.
    # Without this the comparison below is satisfied by any single-element
    # dict — a mixed-level regulator reporting only its own residual passed
    # this check vacuously on its first writing, which is the third time this
    # tree has produced a condition that a degenerate input satisfies for free.
    if set(res) != {"raw_last", "richardson1", "richardson2"}:
        return False
    if chosen not in res:
        return False
    if abs(res[chosen]) != min(abs(v) for v in res.values()):
        return False
    # and the choice must actually beat the level this gate used to fix
    if abs(res[chosen]) >= abs(res["richardson2"]):
        return False
    if chosen == "richardson2":                           # never the best here
        return False
    # THE LEVELS MUST BE GOOD, NOT MERELY RANKED. Everything above tests the
    # selection logic and nothing about what it selects from, so a corrupted
    # Richardson step passed all of it — the selector simply fell back to `raw`
    # and reported a worse regulator without complaint. The threshold is
    # measured: at depth 8 an intact first Richardson step reaches a residual of
    # 5.1e-07 and the fallback to raw reaches 1.4e-05, so 5e-06 separates them
    # and nothing tighter is claimed.
    return abs(res[chosen]) < 5e-6


def check_sweep_coverage() -> bool:
    """The sweep's own coverage, and the alias set that makes it measurable.

    Three things are pinned, and the middle one is this round's whole point.

    The four buckets must **partition** the 85: a classifier that let a document
    fall into two, or into none, would report a sweep that does not add up.

    Stem matching must find strictly more than link matching. Only 17 of the 85
    are cited anywhere as a markdown link and 29 are touched in total, so a scan
    written from the form the author remembers writing would report a sweep four
    times smaller — the same silent under-report this tree produced in four
    consecutive rounds. Pinning the gap keeps a future narrowing visible.

    What is NOT pinned, and the reason is a mistake this check made: RUN-027's
    Phase 1 row — 0 subjects, 23 unmentioned — was written in here as an
    invariant. It is a **finding**, and the point of later rounds is to move it.
    RUN-028 and RUN-029 named `V0_5_EXACT_CENSUS_REPORT` on their subject lines
    and the check went red on the baseline, on success. A check that freezes a
    measurement the work is meant to change will fail exactly when the work
    succeeds, so the Phase 1 figures are data in the log and the classifier's
    ability to tell the buckets apart is asserted on a fixture instead.
    """
    docs = cov29.documents()
    if len(docs) != 85:
        return False
    src = cov29.sources()
    rows = [cov29.classify(d, src) for d in docs]
    counts = collections.Counter(r["bucket"] for r in rows)
    if sum(counts.values()) != 85:
        return False
    if set(counts) - {"subject of a report", "cited in a report",
                      "named in gate code", "not mentioned"}:
        return False
    if counts["subject of a report"] < 21 or counts["not mentioned"] > 56:
        return False
    if len([r for r in rows if r["subline"] == "phase1"]) != 25:
        return False
    # the classifier must actually separate the buckets, tested where the answer
    # is fixed by construction rather than by the state of the sweep
    fx = {"reports": {
              "A.md": {"subject": "aimed at 99_Target", "body": "aimed at 99_Target"},
              "B.md": {"subject": "something else", "body": "mentions 98_Other"}},
          "gates": {"g.py": "# 97_OnlyHere"}}
    for name, want in (("99_Target.md", "subject of a report"),
                       ("98_Other.md", "cited in a report"),
                       ("97_OnlyHere.md", "named in gate code"),
                       ("96_Nowhere.md", "not mentioned")):
        doc = {"subline": "phase1", "name": name,
               "aliases": cov29.aliases("phase1", name)}
        if cov29.classify(doc, fx)["bucket"] != want:
            return False
    # the alias set: the stem and the Phase 0 `doc NN` form must both be there,
    # since four rounds name their subject only that way
    al = cov29.aliases("phase0", "05_Internal_Grid_Rank_Audit.md")
    if "05_Internal_Grid_Rank_Audit" not in al or "doc 05" not in al:
        return False
    if "doc 05" in cov29.aliases("phase2", "05_NonSemistable_Family_Theorem_Schema.md"):
        return False                                     # the form is Phase 0's
    # and stem matching must beat link matching, measured
    link_only = set()
    for r in src["reports"].values():
        for m in re.findall(r"\]\(([^)]*amral/public/bsd/[^)]+)\)", r["body"]):
            link_only.add(m.rsplit("/", 1)[-1])
    touched = sum(1 for r in rows if r["bucket"] != "not mentioned")
    # The RELATION, not the absolutes. `link_only <= 17` was frozen here too and
    # broke for the same reason as the Phase 1 row: RUN-028 and RUN-029 added
    # markdown links to corpus documents, so the link count rose and a check
    # written against yesterday's number went red on today's work. What the
    # round actually claimed is that stem matching finds strictly more, and that
    # is what is asserted.
    return len(link_only) < touched and touched >= 29


def check_phase1_numeric_crosscheck() -> bool:
    """Phase 1's stated numbers against ours, and the two masks that make the
    comparison mean anything.

    The masks are the check's substance. Without them the gate reported 30
    values with no counterpart, of which most were digit runs inside a git SHA
    or an LMFDB curve label — a loud over-report, where this tree's four
    previous scanning faults were silent under-reports. Both directions come
    from the same root, so both are pinned: a SHA and a label must contribute no
    count, and the masked list must not be empty either, since a mask that
    matches nothing is a filter that is not running.
    """
    good, malformed, masked = p1num.document_numbers()
    if not good or not masked:
        return False
    if len(masked) < 20:                                 # the corpus has ~31
        return False
    ours = p1num.our_numbers()
    absent = {r["value"] for r in good if r["value"] not in ours}
    if len(absent) > 12:                                 # 9 today; a mask that
        return False                                     # stopped working blows past this
    # the masks themselves, on strings that are only ever one or the other
    sha = "1a0489c3c3099dd0c248624e6621df73ae8f0d43"
    if not p1num._masked_spans(sha):
        return False
    if not p1num._masked_spans("| 302606a1 | 15 | 0 |"):
        return False
    if p1num._masked_spans("old_total_twist_pairs = 293482"):
        return False                                     # a real count, unmasked
    # the Q9 accounting identity, and its sensitivity to one corrupted input
    q = p1num.q9_accounting_identity()
    if not (q["identity_holds"] and q["lhs_agrees"] and q["rhs_agrees"]):
        return False
    if q["lhs_recomputed"] != 46091 or q["rhs_recomputed"] != 46091:
        return False
    return len(q["inputs_this_tree_computed"]) == 4


_Q9_MEMO: dict = {}


def _q9_artefacts():
    """The two twist artefacts, read once from the archive branch.

    They are immutable blobs on a branch this tree does not write to, and
    reading them costs 0.41s — a per-defect tax of a minute over a full run.
    The scope statement: this check tests the counting and the decomposition,
    not the reading, and a defect planted in `load` would not be seen.
    """
    if not _Q9_MEMO:
        _Q9_MEMO["old"] = q9.load("old")[1]
        _Q9_MEMO["new"] = q9.load("new")[1]
    return _Q9_MEMO["old"], _Q9_MEMO["new"]


def check_q9_census_closure() -> bool:
    """§Q9's eight terms, measured, and the calibration that makes them mean
    the same thing the document means.

    The calibration is the part worth pinning. The artefact lists the trivial
    twist `d = 1`, so "twist pairs" could be the sum of list lengths or that
    minus one per label — 247,391 against 210,704 on the new artefact. The rule
    is fixed by RUN-012's already-verified 247,391 and then applied unchanged to
    the old one, so it cannot have been chosen to make the old count come out
    right. A check that only compared the eight totals would pass on a
    calibration picked after the fact.
    """
    old, new = _q9_artefacts()
    cal = q9.calibrate(new)
    if cal["rule"] != "inclusive" or not cal["calibrated"]:
        return False
    if cal["pairs_excluding_trivial_twist"] == cal["verified_value_from_RUN_012"]:
        return False                                     # the two must differ
    dec = q9.decompose(old, new)
    if not (dec["all_agree"] and dec["identity_holds"]):
        return False
    if dec["labels"] != {"old": 39394, "new": 36687, "dropped": 2707,
                         "added": 0, "common": 36687}:
        return False
    # the decomposition on a synthetic pair, where the four terms are separable
    # by hand: L1 dropped entirely, L2 loses one and gains one, L3 is new
    syn_old = {"L1": [1, 5], "L2": [1, 7, 9]}
    syn_new = {"L2": [1, 7, 11], "L3": [1, 3]}
    d = q9.decompose(syn_old, syn_new)["measured"]
    if (d["upstream_removed"], d["stable_removed"],
            d["stable_added"], d["newbase_added"]) != (2, 1, 1, 2):
        return False
    return q9.base_without_twists(old)["difference"] == 1355


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
    "globalizer-exact": check_globalizer,
    "anchor-11a1": check_anchor_11a1,
    "anchor-rank-one": check_anchor_rank_one,
    "E1-vs-mpmath": check_E1_against_an_independent_implementation,
    "real-period-vs-integration": check_real_period_against_integration,
    "kronecker": check_kronecker,
    "family-root-number": check_family_root_number,
    "family-ordinary": check_family_ordinary,
    "twist-model": check_twist_model,
    "membership-in-P": check_membership_in_P,
    "tate": check_tate,
    "tate-i0star-reachable": check_tate_i0star_reachable,
    "ogg-formula": check_ogg,
    "regulator": check_regulator,
    "bsd-sweep": check_bsd_sweep,
    "two-witness-degrees": check_two_witness_degrees,
    "witness-lemmas": check_witness_lemmas,
    "analytic-classification": check_analytic_classification,
    "criterion-reach": check_criterion_reach,
    "p5-formal-group": check_p5_formal_group,
    "p5-residue-homomorphism": check_p5_residue_homomorphism,
    "p5-chain-inputs": check_p5_chain_inputs,
    "p5-ledger-extraction": check_p5_ledger_extraction,
    "p5-ledger-reconcile": check_p5_ledger_reconcile,
    "p5-gates-closed-here": check_p5_gates_closed_here,
    "p5-selmer-cube": check_p5_selmer_cube,
    "p5-core-vertex-pairs": check_p5_core_vertex_pairs,
    "rank2-real-period": check_rank2_real_period,
    "rank2-bsd-identity": check_rank2_bsd_identity,
    "corpus-hashing": check_corpus_hashing,
    "ladder-rungs": check_ladder_rungs,
    "rejected-route-verdicts": check_rejected_route_verdicts,
    "multiplicity-order": check_multiplicity_order,
    "sha-labelling": check_sha_labelling,
    "rank1-leading-derivative": check_rank1_leading_derivative,
    "rank1-identity": check_rank1_identity,
    "height-level-selection": check_height_level_selection,
    "sweep-coverage": check_sweep_coverage,
    "phase1-numeric-crosscheck": check_phase1_numeric_crosscheck,
    "q9-census-closure": check_q9_census_closure,
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

    # ---- gates 18 and 19 -----------------------------------------------------
    ("step-7 normalisation over-tightened so I0* becomes unreachable", "code",
     "tate-i0star-reachable",
     lambda: patch(tate18, "normalise_for_step7", _normalise_too_strong)),
    ("the p >= 5 type table reads III as II", "code", "tate",
     lambda: patch(tate18, "kodaira_from_valuations", _kodaira_shifted)),
    ("the additive conductor exponent is taken as 1 instead of 2", "code",
     "ogg-formula", lambda: patch(tate18, "kodaira_from_valuations",
                                  lambda vc4, vc6, vd:
                                  (_true_kodaira(vc4, vc6, vd)[0], 1))),
    ("type II* is given f = v(disc) - 7 instead of - 8", "code", "ogg-formula",
     lambda: patch(tate18, "_after_triple", _after_triple_off_by_one)),
    ("the singular point is not moved to the origin", "code", "tate",
     lambda: patch(tate18, "singular_point", lambda a, q: (0, 0))),

    # ---- gate 21 -------------------------------------------------------------
    ("F2 rank returns the number of vectors instead of the rank", "code",
     "two-witness-degrees", lambda: patch(tw21, "f2_rank", len)),
    ("squarefree part drops the sign", "code", "two-witness-degrees",
     lambda: patch(tw21, "squarefree_part",
                   lambda n: abs(_true_squarefree(n)))),
    ("membership in the span always answers yes", "code",
     "two-witness-degrees", lambda: patch(tw21, "in_span",
                                          lambda t, v: True)),

    # ---- gate 22 -------------------------------------------------------------
    ("the witness gcd is computed as an lcm", "code", "witness-lemmas",
     lambda: patch(net22, "gcds", _gcds_lcm)),
    ("the exceptional set keeps the prime 2", "code", "witness-lemmas",
     lambda: patch(net22, "odd_prime_divisors", _divisors_with_two)),
    ("leave-one-out forgets to leave p out", "code", "witness-lemmas",
     lambda: patch(net22, "loo", _loo_keeps_p)),
    ("(T1)'s ord₂ condition is asserted rather than measured", "code",
     "analytic-classification",
     lambda: patch(net22, "ord_2_l_alg_is_zero", lambda *a, **k: True)),
    ("(T5) read against M instead of M⁻", "code", "criterion-reach",
     lambda: patch(net22, "which_criterion_applies", _t5_on_the_wrong_set)),
    ("(T5) accepts any odd valuation, not valuation one", "code",
     "criterion-reach",
     lambda: patch(net22, "which_criterion_applies", _t5_accepts_odd)),
    ("the short model uses b2 where it needs 3*b2", "code", "p5-formal-group",
     lambda: patch(p5u, "minimal_to_short", _short_model_wrong_shift)),
    ("valuation ignores the denominator", "code", "p5-formal-group",
     lambda: patch(p5u, "valuation", _valuation_numerator_only)),
    ("scalar multiplication drops its final addition", "code",
     "p5-formal-group", lambda: patch(p5u, "short_mul", _mul_drops_last_add)),
    ("the unit residue forgets to invert the denominator", "code",
     "p5-formal-group",
     lambda: patch(p5u, "unit_residue", _residue_without_inverse)),
    ("point counting forgets the point at infinity", "code",
     "p5-chain-inputs", lambda: patch(p5u, "point_count", _count_without_O)),
    ("the homomorphism law is predicted with the wrong sign", "code",
     "p5-residue-homomorphism",
     lambda: patch(p5u, "residue_homomorphism", _phi_wrong_sign)),
    ("the status pattern gets its word boundary back, dropping underscore rows",
     "code", "p5-ledger-extraction",
     lambda: patch(led24, "STATUS_WORD", _STATUS_WITH_WORD_BOUNDARY)),
    ("the ledger row pattern loses the hyphen from its gate-name class",
     "code", "p5-ledger-extraction",
     lambda: patch(led24, "ROW", _ROW_NO_HYPHEN)),
    ("BLOCKED counts as CLOSED in the verdict rule", "code",
     "p5-ledger-reconcile", lambda: patch(led24, "_verdict", _verdict_blocked_is_closed)),
    ("an ambiguous gate name is resolved to its first candidate", "code",
     "p5-ledger-reconcile", lambda: patch(led24, "_canon", _canon_guesses)),
    ("X_0(11)'s non-cuspidal list loses its third j-invariant", "code",
     "p5-gates-closed-here",
     lambda: patch(led24, "X0_11_NONCUSPIDAL_J", (-11 * 131 ** 3, -2 ** 15))),
    ("the kernel line drops the sign, giving Q + kP", "code", "p5-selmer-cube",
     lambda: patch(cv25, "kernel_line", _kernel_line_no_sign)),
    ("the 2x2 determinant is computed as a permanent", "code",
     "p5-selmer-cube", lambda: patch(cv25, "selmer_cube", _cube_permanent)),
    ("the admissibility test accepts any positive 11-valuation", "code",
     "p5-core-vertex-pairs",
     lambda: patch(cv25, "admissible_valuation", lambda v: v >= 1)),
    ("a pair is counted as a core vertex when the determinant vanishes",
     "code", "p5-core-vertex-pairs",
     lambda: patch(cv25, "pair_scan", _pairs_counted_backwards)),
    ("the egg integral drops its sin-theta Jacobian", "code",
     "rank2-real-period",
     lambda: patch(r2bsd, "period_bounded_component", _egg_without_jacobian)),
    ("the unbounded integral omits its closed-form tail", "code",
     "rank2-real-period",
     lambda: patch(r2bsd, "period_unbounded_component", _unbounded_no_tail)),
    ("the real period is doubled again on the Delta > 0 branch", "code",
     "rank2-bsd-identity",
     lambda: patch(anchor15, "real_period",
                   lambda a: 2 * _true_real_period(a))),
    ("the BSD identity divides by the regulator instead of multiplying",
     "code", "rank2-bsd-identity",
     lambda: patch(r2bsd, "DOC_REG", 1.0 / r2bsd.DOC_REG)),
    ("the corpus hash is truncated to sixteen hex digits", "code",
     "corpus-hashing",
     lambda: patch(corpus00, "sha256_bytes",
                   lambda b: _true_sha256(b)[:16])),
    ("the rung pattern loses its word boundaries, so C1 matches inside C10",
     "code", "ladder-rungs",
     lambda: patch(ladder01, "RUNG", re.compile(r"C(\d{1,2})"))),
    ("the salvage window shrinks back to the same line", "code",
     "rejected-route-verdicts", lambda: patch(route02, "CONTEXT", 0)),
    ("the salvage classifier loses its negations", "code",
     "rejected-route-verdicts",
     lambda: patch(route02, "NEGATIONS", re.compile(r"(?!x)x"))),
    ("the order at zero is read as the degree", "code", "multiplicity-order",
     lambda: patch(nogo03, "order_at_zero", _order_is_degree)),
    ("the Sha subscript pattern cannot nest, dropping mathrm-an", "code",
     "sha-labelling",
     lambda: patch(agent27, "SHA_CLAIM", _SHA_CLAIM_FLAT_SUBSCRIPT)),
    ("an `an` subscript stops meaning analytic", "code", "sha-labelling",
     lambda: patch(agent27, "ANALYTIC_SUBSCRIPT", re.compile(r"(?!x)x"))),
    ("a required hypothesis is counted as a claim", "code", "sha-labelling",
     lambda: patch(agent27, "HYPOTHESIS", re.compile(r"(?!x)x"))),
    ("provenance stops counting as a label", "code", "sha-labelling",
     lambda: patch(agent27, "PROVENANCE", re.compile(r"(?!x)x"))),
    ("E1 replaced by its crude large-x approximation", "code",
     "rank1-leading-derivative",
     lambda: patch(anchor15, "E1", lambda x: __import__("math").exp(-x) / x)),
    ("the rank-1 leading term drops its factor of 2", "code",
     "rank1-leading-derivative",
     lambda: patch(r1bsd, "leading_derivative", _leading_without_the_two)),
    ("the canonical height goes back to always returning richardson2", "code",
     "height-level-selection",
     lambda: patch(bsd20, "canonical_height", _height_always_richardson2)),
    ("the regulator picks a level per height instead of uniformly", "code",
     "height-level-selection",
     lambda: patch(bsd20, "regulator", _regulator_mixed_levels)),
    ("the coverage alias set keeps only the filename, not the stem", "code",
     "sweep-coverage",
     lambda: patch(cov29, "aliases", lambda sub, name: [name])),
    ("the coverage alias set drops the Phase 0 doc-NN form", "code",
     "sweep-coverage", lambda: patch(cov29, "aliases", _aliases_no_doc_nn)),
    ("coverage reads a report's body before its subject line", "code",
     "sweep-coverage", lambda: patch(cov29, "classify", _classify_body_first)),
    ("the git-SHA mask stops matching", "code", "phase1-numeric-crosscheck",
     lambda: patch(p1num, "SHA_LIKE", re.compile(r"(?!x)x"))),
    ("Q9's stated upstream_removed is corrupted", "code",
     "phase1-numeric-crosscheck",
     lambda: patch(p1num, "Q9_STATED", dict(p1num.Q9_STATED,
                                            upstream_removed=24875))),
    ("the twist-pair rule is calibrated on the trivial-twist-excluding count",
     "code", "q9-census-closure",
     lambda: patch(q9, "STATED", dict(q9.STATED, new_total_twist_pairs=210704))),
    ("the decomposition swaps removed and added on the common labels", "code",
     "q9-census-closure", lambda: patch(q9, "decompose", _decompose_swapped)),
    ("the base-curve count gate 31 subtracts from is wrong", "code",
     "q9-census-closure", lambda: patch(q9, "BASE_CURVES", 40794)),

    # ---- gate 20 -------------------------------------------------------------
    ("x-only duplication drops the -2*b6*x term", "code", "regulator",
     lambda: patch(bsd20, "x_double", _x_double_missing_term)),
    # Named for `height-level-selection` since RUN-026, not for `regulator`, and
    # the re-naming is a finding rather than bookkeeping. The regulator now picks
    # its extrapolation level by the parallelogram law, so a broken Richardson
    # step is simply not chosen — the regulator ROUTES AROUND the defect and its
    # check stops seeing it. Robustness bought insensitivity, and the check that
    # owns Richardson's correctness is the one that inspects the levels
    # themselves. The drill reported this as caught-by-the-wrong-check before it
    # was moved.
    ("Richardson extrapolates against 1/2^n instead of 1/4^n", "code",
     "height-level-selection",
     lambda: patch(bsd20, "canonical_height", _canon_wrong_richardson)),
    # Promoted from CONTROLS by RUN-026, and the reason is the repair itself.
    # Reading only the numerator of x rather than max(|num|, den) IS wrong —
    # there are steps in 389.a1's doubling orbits where the denominator is
    # larger — and it moves the regulator by 1.16e-07. It sat in the controls
    # because "the regulator is only known to about 1.6e-06", which was
    # `richardson2`'s error and not the method's. With the level chosen by the
    # parallelogram law the regulator is known to 9.4e-09, the perturbation is
    # two orders of magnitude ABOVE that, and a defect the computation could not
    # resolve became one it can.
    ("naive height reads the numerator only", "code", "rank1-identity",
     lambda: patch(bsd20, "log_height",
                   lambda x: math.log(max(1, abs(x.numerator))))),
    ("the BSD ratio drops the torsion square", "code", "bsd-sweep",
     lambda: patch(bsd20, "sweep", _sweep_no_torsion)),

    # ---- gate 14 -------------------------------------------------------------
    ("unresolved mass summed in floats instead of exact rationals", "code",
     "globalizer-exact",
     lambda: patch(glob14, "mass_exact",
                   lambda ix, s: Fraction(glob14.mass_float(
                       list(ix), float(s))).limit_denominator(10 ** 6))),
    ("the empty unresolved set is given nonzero mass", "code",
     "globalizer-exact",
     lambda: patch(glob14, "mass_exact",
                   lambda ix, s: _true_mass_exact(ix, s) + Fraction(1, 10 ** 9))),
    ("invisibility measured at single precision instead of double", "code",
     "globalizer-exact",
     lambda: patch(glob14, "invisibility_index",
                   lambda s, ref: max(1, int((ref * 2.0 ** -24) ** (-1.0 / s))))),

    # ---- gate 15 -------------------------------------------------------------
    ("E1 drops the Euler-Mascheroni constant", "code", "E1-vs-mpmath",
     lambda: patch(anchor15, "E1", _E1_no_gamma)),
    ("E1 uses its small-x series everywhere", "code", "E1-vs-mpmath",
     lambda: patch(anchor15, "E1", _E1_series_only)),
    ("AGM stops after a single step", "code", "anchor-11a1",
     lambda: patch(anchor15, "agm",
                   lambda x, y: ((x + y) / 2.0 + math.sqrt(x * y)) / 2.0)),
    ("the real period drops the second component when Δ > 0", "code",
     "real-period-vs-integration",
     lambda: patch(anchor15, "real_period", _period_one_component)),
    ("the real period doubles the Δ > 0 branch, as it used to", "code",
     "real-period-vs-integration",
     lambda: patch(anchor15, "real_period", _period_doubled)),
    ("Hecke recursion loses its -p·a_{p^{k-1}} term", "code", "anchor-11a1",
     lambda: patch(anchor15, "coefficients", _coeffs_no_hecke)),
    ("L(E,1) forgets its factor of two", "code", "anchor-11a1",
     lambda: patch(anchor15, "l_value_at_one",
                   lambda a, N, w, limit=600: _true_L1(a, N, w, limit) / 2)),
    ("the split/non-split test is inverted", "code", "anchor-11a1",
     lambda: patch(anchor15, "bad_prime_data", _bad_prime_inverted)),
    ("torsion bound includes primes of bad reduction", "code", "anchor-11a1",
     lambda: patch(anchor15, "torsion_bound", _torsion_with_bad_primes)),

    # ---- gates 16 and 17 -----------------------------------------------------
    ("Kronecker symbol drops its 3,5 mod 8 sign rule at the prime 2", "code",
     "kronecker", lambda: patch(fam16, "kronecker", _kronecker_no_two_rule)),
    ("Kronecker symbol drops the reciprocity sign flip", "code", "kronecker",
     lambda: patch(fam16, "kronecker", _kronecker_no_reciprocity)),
    ("the twist uses d instead of d^2 on a4", "code", "twist-model",
     lambda: patch(fam16, "twist",
                   lambda inv, d: [0, inv[1] * d, 0, inv[3] * d,
                                   inv[4] * d ** 3])),

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
    # A fourth, and the reason is a contract rather than a curve. Dropping the
    # root-number requirement from `is_analytic_rank_zero` changes no verdict,
    # because src15's `analyse` already encodes the sign INTO the L-value: it
    # returns L = None when the sign is undecided and L = 0.0 exactly when
    # w = −1. So "L is a non-zero number" and "decided, w = +1, L ≠ 0" are the
    # same predicate and no fixture can separate them. That is worth stating
    # rather than omitting: the sign condition in gate 22 is inherited, not
    # independently enforced, and if src15 ever returned a raw partial sum for
    # w = −1 this would stop being a no-op. `analytic-classification` now
    # asserts that contract directly so the day it changes is a red check.
    ("rank 0 stops requiring w = +1, which src15's L = 0 contract makes a no-op",
     lambda: patch(net22, "is_analytic_rank_zero", _rank_zero_ignores_the_sign)),
    # A fifth control, and the reason is about the regex rather than the corpus.
    # `ROW` separates a gate name from its status with `\s{2,}`, which reads as
    # load-bearing and is not: the gate-name character class already permits a
    # space, so with a single-space separator the non-greedy quantifier plus the
    # later `.strip()` reproduce exactly the same split on every row in the
    # corpus. What actually does the work is the non-greedy name and the strip.
    # Worth writing down, because a reader of that pattern would guess wrong.
    ("the ledger row separator relaxed to one space, which the name class makes a no-op",
     lambda: patch(led24, "ROW", _ROW_SINGLE_SPACE)),
    # A sixth control, measured at exactly zero. Gate 30 masks two kinds of
    # digit run: a git SHA and an LMFDB curve label. On this corpus the label
    # mask is redundant — every label in the Phase 1 documents (66166b1,
    # 302606a1, 156854b1) is a valid hexadecimal string, so the SHA pattern
    # already covers it, and the number of occurrences the label mask catches
    # ALONE is 0. It is kept because an isogeny class letter past `f` would
    # break that coincidence, and it is recorded here rather than left in the
    # defect list as coverage this corpus cannot provide.
    ("gate 30's curve-label mask disabled, which the SHA mask makes redundant",
     lambda: patch(p1num, "CURVE_LABEL", re.compile(r"(?!x)x"))),
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
    # A fourth no-op, and this one is a fact about the family rather than about
    # a curve: every twisting discriminant here is ≡ 1 (mod 4), and Kronecker
    # reciprocity makes (d/n) = (n/d) for exactly those d. Swapping the
    # arguments cannot change a coefficient anywhere this gate looks.
    ("twisted coefficients swap chi's arguments, which d = 1 mod 4 makes equal",
     lambda: patch(fam16, "twisted_coefficients",
                   lambda base, d: [0] + [fam16.kronecker(n, abs(d)) * base[n]
                                          for n in range(1, len(base))])),
    # And a fifth, which is a statement about the theorem rather than the code:
    # 𝒫's second condition is IMPLIED by its first and third. f₂ irreducible
    # mod q puts Frobenius in A₃, so (disc(f₂)/q) = 1; disc(f₂) has squarefree
    # part −174 = (−6)·29, and q ≡ 1 (mod 24) already gives (−6/q) = 1. Hence
    # (29/q) = 1 comes for free. Measured over every prime q ≡ 1 (mod 24) below
    # 200,000: 760 have f₂ irreducible and every one of them has (q/29) = 1,
    # with the opposite cell empty. Dropping the condition cannot change the
    # membership of 𝒫, so this belongs here rather than in the defect list.
    ("membership drops the (q/29) condition, which the other two imply",
     lambda: patch(fam16, "in_P", _in_P_no_29)),
    # A seventh, and it is a fact about the field rather than about the code.
    # K_E contains ζ₈, hence √−1, so √ℓ and √−ℓ differ by an element already
    # present: adjoining ℓ* or ℓ gives the SAME field, and inverting the sign
    # convention cannot change [K_E:Q] or what lies inside it. The ℓ* in the
    # definition is there for the reciprocity step of Lemma 3.2, which rewrites
    # (ℓ*/q) = 1 as (q/ℓ) = 1 — not for the field.
    ("the ell* sign convention is inverted, which sqrt(-1) in K_E makes a no-op",
     lambda: patch(tw21, "star", lambda e: -e if e % 4 == 1 else e)),
]


_true_mass_exact = glob14.mass_exact
_true_divisors = net22.odd_prime_divisors
_true_squarefree = tw21.squarefree_part
_true_gcds = net22.gcds
_true_loo = net22.loo


def _gcds_lcm(ws):
    import math as _m
    M, Mm = ws["M"], ws["M_minus"]

    def _l(vals):
        vals = list(vals)
        if not vals:
            return None
        out = vals[0]
        for v in vals[1:]:
            out = out * v // _m.gcd(out, v)
        return out
    gm, gn = _l(M.values()), _l(Mm.values())
    R = set()
    for g in (gm, gn):
        if g is not None:
            R |= net22.odd_prime_divisors(g)
    return {"g_mult": gm, "g_minus": gn, "R": sorted(R),
            "exceptional_set_empty": not R}


def _divisors_with_two(n):
    out = set(_true_divisors(n))
    if n and n % 2 == 0:
        out.add(2)
    return out


def _aliases_no_doc_nn(sub, name):
    """Filename and stem only — the `doc NN` form dropped, which misfiles the
    four rounds whose subject line names a Phase 0 document only that way."""
    stem = name[:-3] if name.endswith(".md") else name
    return [name, stem]


def _classify_body_first(doc, src):
    """Body before subject, so a round aimed at a document is filed as merely
    having cited it — the strongest bucket silently emptied into the next."""
    subj, body, gates = [], [], []
    for rname, r in src["reports"].items():
        if any(a in r["body"] for a in doc["aliases"]):
            body.append(rname)
        elif any(a in r["subject"] for a in doc["aliases"]):
            subj.append(rname)
    for gname, text in src["gates"].items():
        if any(a in text for a in doc["aliases"]):
            gates.append(gname)
    bucket = ("subject of a report" if subj else
              "cited in a report" if body else
              "named in gate code" if gates else "not mentioned")
    return {"subline": doc["subline"], "name": doc["name"], "bucket": bucket,
            "subject_of": subj, "cited_in": body[:6], "named_in_gates": gates[:6]}


_true_decompose = q9.decompose


def _decompose_swapped(old, new):
    """stable_removed and stable_added exchanged — 21,306 becomes 0 and 0
    becomes 21,306, while lhs and the two label-level terms are untouched."""
    d = _true_decompose(old, new)
    m = d["measured"]
    m["stable_removed"], m["stable_added"] = m["stable_added"], m["stable_removed"]
    m["rhs"] = (m["upstream_removed"] + m["stable_removed"]
                - m["stable_added"] - m["newbase_added"])
    d["agreement"] = {k: m[k] == q9.STATED[k] for k in q9.STATED}
    d["all_agree"] = all(d["agreement"].values())
    d["identity_holds"] = m["lhs"] == m["rhs"]
    return d


_true_leading = r1bsd.leading_derivative
_true_height = bsd20.canonical_height


def _leading_without_the_two(ainvs, N, limit=None):
    """The classical rank-1 sum without its leading factor 2."""
    d = _true_leading(ainvs, N, limit) if limit else _true_leading(ainvs, N)
    d["value"] = d["value"] / 2
    return d


def _height_always_richardson2(ainvs, P, depth=10):
    d = _true_height(ainvs, P, depth)
    d["value"] = d["richardson2"]
    d["chosen_level"] = "richardson2"
    return d


def _regulator_mixed_levels(ainvs, gens, depth=10):
    """Each height picks its own level — which breaks the parallelogram law,
    the very identity used to judge the choice."""
    P, Q = gens
    PQ = bsd20.ec_add(ainvs, P, Q)
    PmQ = bsd20.ec_add(ainvs, P, bsd20.ec_neg(ainvs, Q))
    full = {n: _true_height(ainvs, pt, depth)
            for n, pt in (("P", P), ("Q", Q), ("P+Q", PQ), ("P-Q", PmQ))}
    h = {n: d["value"] for n, d in full.items()}
    res = h["P+Q"] + h["P-Q"] - 2 * h["P"] - 2 * h["Q"]
    pair = (h["P+Q"] - h["P"] - h["Q"]) / 2
    return {"heights": h, "extrapolation_level": "mixed",
            "residual_at_each_level": {"mixed": res},
            "parallelogram_law_residual": res, "pairing_PQ": pair,
            "regulator": h["P"] * h["Q"] - pair * pair, "depth": depth,
            "independent": True}


_true_sha256 = corpus00.sha256_bytes
_SHA_CLAIM_FLAT_SUBSCRIPT = re.compile(
    agent27.SHA_CLAIM.pattern.replace(
        r"_\{(?:[^{}]|\{[^{}]*\})*\}", r"_\{[^}]{0,30}\}"))


def _order_is_degree(coeffs):
    """max power instead of min — degree, not order at zero."""
    nz = sorted(k for k, v in coeffs.items() if v != 0)
    if not nz:
        raise ValueError("the zero polynomial has no well-defined order")
    return nz[-1]


_true_real_period = anchor15.real_period
_true_egg = r2bsd.period_bounded_component
_true_unbounded = r2bsd.period_unbounded_component


def _egg_without_jacobian(e3, e2, e1, n=400_000):
    """The Chebyshev substitution kept and its Jacobian dropped — the endpoint
    singularities stop cancelling and the integral diverges upward."""
    import math as _m
    mid, half = (e3 + e2) / 2, (e2 - e3) / 2
    tot = 0.0
    for i in range(n):
        th = (i + 0.5) * _m.pi / n
        x = mid + half * _m.cos(th)
        v = 4 * (x - e1) * (x - e2) * (x - e3)
        if v > 0:
            tot += half / _m.sqrt(v) * (_m.pi / n)
    return 2 * tot


def _unbounded_no_tail(e3, e2, e1, n=2_000_000, T=4000.0):
    """The truncation reported as the answer, with no 2/T correction."""
    d = _true_unbounded(e3, e2, e1, n=n, T=T)
    d["corrected"] = d["truncated_at_T"]
    return d


_true_kernel_line = cv25.kernel_line
_true_cube = cv25.selmer_cube
_true_pairs = cv25.pair_scan


def _kernel_line_no_sign(row):
    """a = +b·r1/r0 instead of −b·r1/r0 — the line reflected."""
    r0, r1 = row[0] % 11, row[1] % 11
    if r0 == 0 and r1 == 0:
        return None
    if r0 == 0:
        return (1, 0)
    return ((pow(r0, -1, 11) * r1) % 11, 1)


def _cube_permanent(rows):
    """ad + bc instead of ad − bc."""
    out = _true_cube(rows)
    labels = sorted(rows)
    r1, r2 = rows[labels[0]], rows[labels[1]]
    out["determinant"] = (r1[0] * r2[1] + r1[1] * r2[0]) % 11
    return out


def _pairs_counted_backwards(rows):
    """Good and degenerate swapped."""
    out = _true_pairs(rows)
    out["pairs_giving_a_core_vertex"], out["pairs_that_degenerate"] = (
        out["pairs_that_degenerate"], out["pairs_giving_a_core_vertex"])
    return out


_STATUS_WITH_WORD_BOUNDARY = re.compile(
    r"\b(CLOSED|OPEN|BLOCKED|PENDING|AVAILABLE|PARTIALLY|EQUIVALENT|REDUCED|"
    r"NOT CLAIMED|CIRCULAR|EXTERNAL|THEOREM TECHNOLOGY|ARITHMETIC TARGET)\b")
_ROW_SINGLE_SPACE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9\-/_\[\]^ .]*?)\s([^\s].*?)\s*$")
_ROW_NO_HYPHEN = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9/_\[\]^ .]*?)\s{2,}(\S.*?)\s*$")
_true_verdict = led24._verdict


def _verdict_blocked_is_closed(status):
    """BLOCKED read as a kind of closure — the confusion the rule exists to stop."""
    return "CLOSED" if _true_verdict(status) in ("CLOSED", "NOT-CLOSED") else "OTHER"


def _canon_guesses(target, names):
    """Resolve an ambiguous target to its first candidate instead of leaving it."""
    if target in names:
        return target
    hits = sorted(n for n in names
                  if n == "P5-" + target or n.endswith("-" + target)
                  or n.endswith(target))
    return hits[0] if hits else target


def _short_model_wrong_shift(a, pt):
    a1, _a2, a3, _a4, _a6 = a
    b2, *_ = p5u.b_invariants(a)
    c4, c6 = p5u.c_invariants(a)
    x, y = pt
    return -27 * c4, -54 * c6, (36 * x + b2, 108 * (2 * y + a1 * x + a3))


def _valuation_numerator_only(q, p):
    from fractions import Fraction
    n, v = q.numerator, 0
    while n % p == 0:
        n //= p
        v += 1
    return v, Fraction(n, q.denominator)


_true_short_mul = p5u.short_mul


def _mul_drops_last_add(A, n, Pt):
    """n·P computed as (n-1)·P — an off-by-one in the multiplier.

    Bound to the ORIGINAL short_mul, not to the patched module attribute: a
    defect that calls the name it is replacing recurses instead of computing,
    and a RecursionError is not a check catching anything.
    """
    return _true_short_mul(A, max(n - 1, 1), Pt)


def _residue_without_inverse(q, p):
    v, u = p5u.valuation(q, p)
    if v != 0:
        raise ValueError("not a unit")
    return u.numerator % p


_true_point_count = p5u.point_count
_true_residue_hom = p5u.residue_homomorphism


def _count_without_O(a, p):
    """#E(F_p) without the point at infinity. Bound to the original, not the
    patched attribute — see _mul_drops_last_add."""
    return _true_point_count(a, p) - 1


def _phi_wrong_sign(A, n11):
    """The homomorphism law predicted with a minus: phi(aP + bQ) = 7a - b.

    It agrees with the truth on every b = 0 combination and on nothing else, so
    a check that only pinned phi(P) would not see it."""
    h = _true_residue_hom(A, n11)
    h["homomorphism_law"] = f"phi(aP + bQ) = {h['phi(P)']}a - {h['phi(Q)']}b (mod 11)"
    h["mismatches"] = [{"a": 1, "b": 1, "note": "sign"}]
    h["is_a_homomorphism"] = False
    return h


def _t5_on_the_wrong_set(c):
    M = {int(k): v for k, v in c["M"].items()}
    t4 = any(v == 1 for v in M.values())
    t5 = any(v == 1 for v in M.values())        # M, not M-minus
    return {"criterion_30_applies": t4 and t5, "T4_satisfiable": t4,
            "T5_satisfiable": t5, "exceptional_set_empty": not c["R"]}


def _t5_accepts_odd(c):
    M = {int(k): v for k, v in c["M"].items()}
    Mm = {int(k): v for k, v in c["M_minus"].items()}
    t4 = any(v == 1 for v in M.values())
    t5 = any(v % 2 == 1 for v in Mm.values())   # odd, not one
    return {"criterion_30_applies": t4 and t5, "T4_satisfiable": t4,
            "T5_satisfiable": t5, "exceptional_set_empty": not c["R"]}


def _rank_zero_ignores_the_sign(res):
    return res["L_at_1"] is not None and abs(res["L_at_1"]) > 1e-9


def _loo_keeps_p(ws, p):
    import math as _m
    rest = dict(ws["M"])                  # p not removed
    if not rest:
        return {"holds": False, "why": "M is empty"}
    exists = any(n % p for n in rest.values())
    g = _m.gcd(*rest.values()) if len(rest) > 1 else next(iter(rest.values()))
    return {"holds": exists, "gcd_form_agrees": exists == (g % p != 0),
            "gcd_without_p": g}
_true_x_double = bsd20.x_double
_true_canon = bsd20.canonical_height
_true_sweep = bsd20.sweep


def _x_double_missing_term(ainvs, x):
    from fractions import Fraction as _F
    b2, b4, b6, b8 = anchor15.b_invariants(ainvs)[:4]
    num = x ** 4 - b4 * x * x - b8              # -2*b6*x dropped
    den = 4 * x ** 3 + b2 * x * x + 2 * b4 * x + b6
    return None if den == 0 else _F(num, den)


def _canon_wrong_richardson(ainvs, P, depth=8):
    x = P[0]
    raw = []
    for _ in range(depth):
        x = bsd20.x_double(ainvs, x)
        if x is None:
            break
        raw.append(bsd20.log_height(x))
    seq = [v / 4 ** (i + 1) for i, v in enumerate(raw)]
    r1 = [(2 * seq[i + 1] - seq[i]) for i in range(len(seq) - 1)]
    r2 = [(2 * r1[i + 1] - r1[i]) for i in range(len(r1) - 1)]
    # The full return shape, including the level machinery RUN-026 added. A
    # defect that returns a smaller dict makes the check raise a KeyError, and a
    # check that goes red on a KeyError has caught nothing — the same lesson
    # RUN-020 recorded when two defects recursed instead of computing.
    levels = {"raw": seq, "richardson1": r1, "richardson2": r2}
    gaps = {k: (abs(v[-1] - v[-2]) if len(v) >= 2 else float("inf"))
            for k, v in levels.items()}
    best = min(gaps, key=gaps.get)
    return {"raw_last": seq[-1], "richardson1": r1[-1], "richardson2": r2[-1],
            "steps": len(seq), "level_gaps": gaps, "chosen_level": best,
            "value": levels[best][-1], "self_consistency": gaps[best]}


def _sweep_no_torsion(records):
    import collections as _c
    import math as _m
    tally = _c.Counter()
    shas = _c.Counter()
    for r in records:
        inv, N = r["ainvs"], r["conductor"]
        res = anchor15.analyse(r["curve_label"], inv, N, limit=bsd20.TERMS)
        if res["root_number"] is None or res["root_number"] != 1:
            continue
        L = res["L_at_1"]
        if L is None or abs(L) < 1e-8:
            continue
        prod = 1
        for q in r["conductor_primes"]:
            c = tate18.reduction_data(inv, q, want_c=True)["c"]
            if c is None:
                prod = None
                break
            prod *= c
        if prod is None:
            continue
        ratio = L / (res["real_period"] * prod)     # torsion square dropped
        near = round(ratio)
        if near > 0 and _m.isqrt(near) ** 2 == near and abs(ratio - near) < 1e-6:
            tally["BSD closes: a positive integer square"] += 1
            shas[near] += 1
    return {"tally": dict(tally), "Sha_values_where_it_closes":
            {str(k): v for k, v in shas.items()}, "non_closing_sample": []}
_true_kodaira = tate18.kodaira_from_valuations
_true_normalise = tate18.normalise_for_step7
_true_after_triple = tate18._after_triple


def _normalise_too_strong(a, q):
    a1, a2, a3, a4, a6 = a
    for s_ in range(q * q):
        if (a1 + 2 * s_) % q:
            continue
        b = tate18.translate(a, 0, s_, 0)
        for r in range(q ** 4):
            if (b[1] + 3 * r) % q:
                continue
            c = tate18.translate(b, r, 0, 0)
            if c[0] % q or c[1] % q:
                continue
            for t in range(q ** 3):
                d = tate18.translate(c, 0, 0, t)
                if (d[2] % q ** 2 == 0 and d[3] % q ** 3 == 0
                        and d[4] % q ** 4 == 0):
                    return d
    return None


def _kodaira_shifted(vc4, vc6, vd):
    kod, f = _true_kodaira(vc4, vc6, vd)
    return ("II" if kod == "III" else kod), f


def _after_triple_off_by_one(a, q, n, scalings):
    res = _true_after_triple(a, q, n, scalings)
    if isinstance(res, dict) and res["kodaira"] == "II*":
        res = dict(res)
        res["f"] = n - 7
    return res
_true_kron = fam16.kronecker


def _kronecker_no_two_rule(a, n):
    if n <= 0:
        raise ValueError
    result = 1
    while n % 2 == 0:
        n //= 2
        if a % 2 == 0:
            return 0                       # the 3,5 mod 8 flip dropped
    a %= n
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def _kronecker_no_reciprocity(a, n):
    if n <= 0:
        raise ValueError
    result = 1
    while n % 2 == 0:
        n //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            result = -result
    a %= n
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a                        # the 3,3 mod 4 flip dropped
        a %= n
    return result if n == 1 else 0


def _in_P_no_29(q):
    return (q % 24 == 1 and q != 29
            and ph2.cubic_root_count(ph2.F2, q) == 0)
_true_L1 = anchor15.l_value_at_one
_true_period = anchor15.real_period
_true_bad_prime = anchor15.bad_prime_data


def _E1_no_gamma(x):
    if x < 2.0:
        s_, term = -math.log(x), 1.0
        for k in range(1, 60):
            term *= -x / k
            s_ -= term / k
        return s_
    return anchor15.E1(x) if False else _E1_lentz(x)


def _E1_lentz(x):
    tiny = 1e-300
    b, c, d = x + 1.0, 1e300, 1.0 / (x + 1.0)
    h = d
    for i in range(1, 300):
        a = -i * i
        b += 2.0
        d = 1.0 / (a * d + b) if abs(a * d + b) > tiny else 1.0 / tiny
        c = b + a / c if abs(b + a / c) > tiny else tiny
        delta = c * d
        h *= delta
        if abs(delta - 1.0) < 1e-17:
            break
    return h * math.exp(-x)


def _E1_series_only(x):
    s_, term = -0.5772156649015328606 - math.log(x), 1.0
    for k in range(1, 60):
        term *= -x / k
        s_ -= term / k
    return s_


def _period_doubled(ainvs):
    b2, b4, b6, _b8, disc = anchor15.b_invariants(ainvs)
    v = _true_period(ainvs)
    return 2 * v if disc > 0 else v


def _period_one_component(ainvs):
    """Only the identity component of E(R) — half the real period when Δ > 0.

    Before RUN-017 fixed the AGM branch, this mutation returned what is now the
    correct value, so it was a no-op the moment the bug was gone. It is written
    against the truth rather than against the old defect.
    """
    b2, b4, b6, _b8, disc = anchor15.b_invariants(ainvs)
    if disc <= 0:
        return _true_period(ainvs)
    e1, e2, e3 = anchor15.real_cubic_roots(b2, b4, b6)
    return math.pi / anchor15.agm(math.sqrt(e1 - e3), math.sqrt(e1 - e2))


def _coeffs_no_hecke(ainvs, bad, limit):
    primes = anchor15.sieve(limit)
    ap = {q: (bad[q] if q in bad else anchor15.point_count_ap(ainvs, q))
          for q in primes}
    a = [0] * (limit + 1)
    a[1] = 1
    for q in primes:
        pk, prev1 = q, ap[q]
        while pk <= limit:
            a[pk] = prev1
            prev1 = ap[q] * prev1          # the -p term dropped
            pk *= q
    for n in range(2, limit + 1):
        if a[n]:
            continue
        for q in primes:
            if q * q > n:
                break
            if n % q == 0:
                r_, m = 1, n
                while m % q == 0:
                    m //= q
                    r_ *= q
                a[n] = a[r_] * a[m]
                break
    return a


def _bad_prime_inverted(ainvs, q):
    d = dict(_true_bad_prime(ainvs, q))
    if d["type"] == "split multiplicative":
        d["type"], d["a_p"] = "non-split multiplicative", -1
    elif d["type"] == "non-split multiplicative":
        d["type"], d["a_p"] = "split multiplicative", 1
    return d


def _torsion_with_bad_primes(ainvs, N):
    g = 0
    for q in anchor15.sieve(120):
        if q > 2:
            g = math.gcd(g, anchor15.point_count(ainvs, q))
    return g
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
                   "src13_algorithm2_twists",
                   "src14_globalizer_faithfulness",
                   "src15_phase2_anchor",
                   "src16_twist_family_lvalues",
                   "src17_family_prime_router",
                   "src18_tate_algorithm",
                   "src19_conductor_census",
                   "src20_bsd_consistency",
                   "src21_two_witness_certificate",
                   "src22_witness_network"],
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
