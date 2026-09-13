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
import json as _json
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
import src32_696e1_certificate as cert32                  # noqa: E402
import src33_mazur_degrees_closed as mazur33              # noqa: E402
import src34_referee_a_checklist as refA34                # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402
import src36_kodaira_prefilters_nogo as nogo36            # noqa: E402
import src37_twist_invariance_bridge as bridge37          # noqa: E402
import src38_mod_ell_surjectivity as surj38               # noqa: E402
import src39_fw_h3_compiler as h3c39                      # noqa: E402
import src40_fw_h2_ordinary as h2o40                      # noqa: E402
import src41_derived_supersingular_bridge as brg41        # noqa: E402
import src42_odd_additive_period_barrier as bar42         # noqa: E402
import src43_finite_exceptional_primes as fin43           # noqa: E402
import src44_base_certificate_compare as cmp44            # noqa: E402
import src45_claim_ladder_position as ladder45            # noqa: E402
import src46_chebotarev_audit as cheb46                   # noqa: E402
import src47_fw_hypothesis_compiler as comp47             # noqa: E402
import src48_h2_chain_and_h3_dispute as chain48           # noqa: E402
import src49_provisional_vs_revised as prev49             # noqa: E402
import src50_candidate_schema_and_sieve as schema50       # noqa: E402
import src51_source_audits as audits51                    # noqa: E402
import src52_novelty_and_routes as routes52               # noqa: E402
import src53_consensus_and_experiment as consensus53      # noqa: E402
import src54_compiler_targets_and_v03 as targets54        # noqa: E402
import src55_local_isogeny_kernel as kern55               # noqa: E402
import src56_family_schema_and_spec as schema56           # noqa: E402
import src57_theorem_2_18_condition_map as cmap57         # noqa: E402
import src58_paper_vs_code_provenance as prov58           # noqa: E402
import src59_lemma_b_reduction as lemb59                  # noqa: E402
import src60_cross_round_joins as joins60                 # noqa: E402
import src61_one_commit_and_delta as commit61             # noqa: E402
import src62_algorithm2_replay as replay62                # noqa: E402
import src63_removed_13_and_soundness as thirteen63       # noqa: E402
import src64_discrepancy_corpus as corpus64               # noqa: E402
import src65_phase1_closure as closure65                  # noqa: E402
import src66_phase1_protocols as proto66                  # noqa: E402
import src67_phase0_maps as maps67                        # noqa: E402
import src68_algorithm2_mirror_and_diff as mirror68       # noqa: E402
import src69_anomalous_norm_localization as anom69        # noqa: E402
import src70_kurihara_modular_symbols as kur70            # noqa: E402
import src71_determinantal_bockstein as bock71            # noqa: E402
import src72_attack03_cyclotomic_divisibility as atk72    # noqa: E402
import src73_attack04_padic_l_mod11 as atk73              # noqa: E402
import src74_attack05_local_log as atk74                  # noqa: E402
import src75_attack06_scalar_and_mellin as atk75          # noqa: E402
import src76_attack07_explicit_geometry as atk76          # noqa: E402
import src77_attack08_norms_and_pushforwards as atk77     # noqa: E402
import src78_attack09_auxiliary_character as atk78        # noqa: E402
import src79_attack09_eisenstein_leading_term as atk79    # noqa: E402
import src80_attack10_unit_and_trace_bridge as atk80      # noqa: E402
import src81_symbolic001_cross_rank_calibration as sym81  # noqa: E402
import src82_pc001_calibrator_19a1 as pc82                # noqa: E402
import src83_pc002_relative_regulator as pc83             # noqa: E402
import src84_symbolic002_004_determinant_jets as sym84    # noqa: E402
import src85_symbolic005_007_lattice_torsor_euler as sym85  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src11-gate-drill.json"
NEWLINE = chr(10)

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


_CERT_MEMO: dict = {}


def check_certificate_696e1() -> bool:
    """The 696.e1 certificate: its rows recomputed here, and its labels intact.

    The certificate is built at 4,000 L-series terms rather than the gate's
    46,000 — 193 seconds against 1.6, and every row already agrees to its stated
    tolerance there. The algebraic rows are recomputed inline from the
    a-invariants, independently of the gate's own `agrees` flag, because a
    certificate whose self-report is the only thing checking it is the summary
    it was written to replace.

    The two label assertions are the point of the artefact as much as the
    numbers: the Sha row must still say ANALYTIC, and the cited-not-verified
    list must still name the rank and the analytic order. A certificate that
    lost those would read as more than it is.
    """
    # The memo is KEYED ON WHAT THE CERTIFICATE DEPENDS ON, not cleared by hand.
    # The first wiring cleared it inside each defect's setup, so the defect run
    # repopulated it with corrupted rows and the restore put back only the
    # patched attribute — every later check then read the stale certificate.
    # The drill's own "state restored afterwards" guard caught it: 20 of 20
    # controls disturbed a check. RUN-018's memo was safe because nothing
    # patched its inputs; this one has three defects that do.
    key = (tuple(cert32.AINVS), id(cert32.certificate))
    if _CERT_MEMO.get("key") != key:
        _CERT_MEMO["key"] = key
        _CERT_MEMO["c"] = cert32.certificate(limit=4000)
    c = _CERT_MEMO["c"]
    if not c["every_row_agrees"] or len(c["rows"]) < 18:
        return False
    by = {r["quantity"]: r for r in c["rows"]}
    # recomputed here, not read from the certificate's own verdict
    b2, b4, b6, b8, disc = anchor15.b_invariants(cert32.AINVS)
    want = {"discriminant": disc, "c4": b2 * b2 - 24 * b4,
            "c6": -b2 ** 3 + 36 * b2 * b4 - 216 * b6,
            "conductor": 696, "product_of_tamagawa_numbers": 1,
            "torsion_order": 1, "degree_of_K_E": 16, "e_E": 2}
    for k, v in want.items():
        r = by.get(k)
        if r is None:
            return False
        got = r.get("recomputed_here", r.get("value"))
        if got != v:
            return False
    if by["density_of_the_support_set"].get("recomputed_here") != [1, 24]:
        return False
    # the labels
    sha = by.get("analytic_order_of_Sha")
    if sha is None or "ANALYTIC" not in sha["derivation"]:
        return False
    if "analytic order" not in (sha.get("note") or ""):
        return False
    cited = cert32.still_cited()
    if len(cited) < 4:
        return False
    joined = " ".join(cited)
    return "RANK" in joined.upper() and "ANALYTIC" in joined.upper()


_MAZUR_PRIMES = None


def _mazur_primes():
    global _MAZUR_PRIMES
    if _MAZUR_PRIMES is None:
        _MAZUR_PRIMES = mazur33.small_primes(600)
    return _MAZUR_PRIMES


def check_mazur_degrees() -> bool:
    """All twelve of Mazur's degrees settled for 696.e1, and the two structural
    facts the closure rests on.

    A witness must exist at every degree the sieve can reach; `n = 2` must be
    reported as **vacuous** rather than unwitnessed, since every element of F2
    is a square and no search length changes that; and the twist invariance of
    `a^2 - 4l` must be demonstrated where `a_l` actually flips sign, because on
    primes where it does not the invariance is trivially true and the check
    would be measuring nothing.
    """
    primes = _mazur_primes()
    for n in (11, 13, 17, 19, 37, 43, 67, 163):
        w = mazur33.witness(mazur33.ANCHOR, n, primes)
        if w is None:
            return False
        a, ell = w["a_ell"], w["ell"]
        if mazur33.sieve.is_square_mod((a * a - 4 * ell) % n, n):
            return False
    if mazur33.witness(mazur33.ANCHOR, 2, primes) is not None:
        return False
    v = mazur33.vacuity_at_2()
    if not v["all_of_F2"]:
        return False
    tw = mazur33.twist_invariance(primes)
    if not tw["all_identical"] or tw["sign_flips_observed"] < 10:
        return False
    return all(r["good_primes_compared"] >= 20 for r in tw["rows"])


_REFA_MEMO: dict = {}


def _refa():
    # Keyed on BOTH patchable entry points. RUN-030 recorded that a cache is a
    # piece of state and a drill that mutates state must restore it; the first
    # version of this key covered only `q_checklist`, so the `base_checklist`
    # defect left a corrupted base in the memo and the baseline went red on the
    # next run. The lesson was one round old.
    key = (id(refA34.q_checklist), id(refA34.base_checklist))
    if _REFA_MEMO.get("key") != key:
        _REFA_MEMO["key"] = key
        # 2,000 L-series terms rather than the gate's 20,000. MEASURED, not
        # chosen: 0.34s against 29.59s, and all four arithmetic verdicts are
        # identical at both truncations (rank 0, no rational 2-torsion,
        # Delta = -178176, v2 = 0). The gate itself still runs at 20,000.
        _REFA_MEMO["base"] = refA34.base_checklist(limit=2000)
        _REFA_MEMO["members"] = [q for q in anchor15.sieve(4000) if fam16.in_P(q)]
        _REFA_MEMO["rejected"] = [q for q in anchor15.sieve(4000)
                                  if q % 4 == 1 and not fam16.in_P(q)][:200]
    return _REFA_MEMO


def check_referee_a_checklist() -> bool:
    """Referee A's checklist, and the converse direction it does not ask for.

    Three of the seven base lines are citations and must stay marked as such: a
    checklist that scored them PASS would report a source as a check. And the
    rejected sample must be non-empty before "0 disagreements" means anything —
    an empty converse test agrees with everything.
    """
    m = _refa()
    base = m["base"]
    cited = {r["line"] for r in base if not r["machine_checkable"]}
    if cited != {"optimal", "odd Manin", "BSD(E,2) rigorous source"}:
        return False
    checkable = [r for r in base if r["machine_checkable"]]
    if len(checkable) != 4 or any(r["status"] != "PASS" for r in checkable):
        return False
    members = m["members"]
    if len(members) < 15 or members[:2] != [241, 313]:
        return False
    if not all(refA34.q_checklist(q)["all_pass"] for q in members):
        return False
    rejected = m["rejected"]
    if len(rejected) < 100:                    # an empty converse agrees with all
        return False
    return not any(refA34.q_checklist(q)["all_pass"] for q in rejected)


def check_gcd_witness_lemmas() -> bool:
    """`00_GCD_Witness_Lemmas`'s three lemmas, and the empty set they hide.

    The multiplicative primes must be found from the discriminant and come out
    as 3 and 29 with n = 1 each, 2 additive; the split/nonsplit classification
    must be computed, not quoted; each lemma's gcd must be 1. And the last
    clause is the one that matters: `empty_set_search` must actually exhibit a
    curve whose nonsplit set is empty, where lemma 1 passes and lemma 3's gcd
    is 0 — the failure set being *every* odd prime, since p | 0 always. Without
    that exhibit, "gcd = 1, no failures" on the anchor is a fact about one
    curve and not a test of the lemma.
    """
    md = gcd35.multiplicative_data(gcd35.BASE)
    if {r["p"]: r["n"] for r in md["multiplicative"]} != {3: 1, 29: 1}:
        return False
    if [r["p"] for r in md["additive"]] != [2]:
        return False
    if {r["p"]: r["split"] for r in md["multiplicative"]} != {3: True,
                                                              29: False}:
        return False
    l1 = gcd35.generic_witness(md)
    if l1["gcd"] != 1 or l1["failure_set"] != []:
        return False
    l2 = gcd35.leave_one_out(md)
    if not l2["all_have_a_distinct_witness"]:
        return False
    if {r["p"]: r["witness"] for r in l2["rows"]} != {3: 29, 29: 3}:
        return False
    l3 = gcd35.nonsplit_witness(md)
    if [r["p"] for r in md["nonsplit"]] != [29] or l3["gcd"] != 1:
        return False
    e = gcd35.empty_set_search()
    a = e["multiplicative_but_all_split"]
    if a is None or a["lemma1_gcd"] != 1 or a["lemma3_gcd"] != 0:
        return False
    if not isinstance(a["lemma3_failure_set"], str):   # not an empty list
        return False
    f = gcd35.family()
    return (f["members"] >= 15 and f["every_member_matches_case_C"]
            and f["every_member_has_q_additive"] and f["gcds_all_one"])


def check_kodaira_nogo() -> bool:
    """`05_Kodaira_Prefilters_and_NoGo`'s exact no-go, and its domain.

    The no-go must be silent on the base and on every member's twist, and the
    additive primes must come out as exactly 2 and q. But a no-go that fires
    nowhere at all has not been exercised, so the firing set must be non-empty
    and must coincide with the primes where the base is multiplicative — the
    check that the two are the *same* set, not merely both small. The p = 3
    character fact must stay special to 3 (F5ˣ has exponent 4), and the gate
    must still say it has not computed the local torsion condition: a
    limitation that quietly stops being stated is a claim that grew.
    """
    fr = nogo36.anchor_and_family()
    if fr["base_additive_primes"] != [2] or fr["members"] < 15:
        return False
    if any(r["no_go_fires"] for r in fr["base"]):
        return False
    if not fr["additive_primes_are_always_2_and_q"]:
        return False
    if fr["no_go_fires_anywhere_in_the_family"]:
        return False
    f = nogo36.where_it_fires()
    if not f["fires_at"]:               # a no-go that never fires is untested
        return False
    if f["fires_at"] != f["base_multiplicative_at"]:
        return False
    if not f["gcd_condition_covers_every_firing_d"]:
        return False
    c = nogo36.character_structure()
    if not c["special_to_3_among_odd_primes"]:
        return False
    if {r["p"]: r["exponent"] for r in c["rows"]}.get(5) != 4:
        return False
    t = nogo36.torsion_clause()
    return t["global_torsion_trivial"] and not t["local_condition_computed"]


def check_twist_bridge() -> bool:
    """`03_Quadratic_Twist_Invariance_Bridge`'s lemma C, both sides, and lemma B
    left where the document leaves it.

    The split side must preserve every local invariant on every member; the
    inert side must genuinely *move* at the multiplicative conductor primes, and
    specifically must flip the split flag rather than merely differ somewhere.
    A conductor prime that could not move must carry a stated reason instead of
    passing silently. Lemma A's shadow must show sign flips — the invariance
    measured where it could have failed. And lemma B must still be reported
    unestablished: a limitation that quietly stops being stated is a claim that
    grew.
    """
    c = bridge37.lemma_C()
    if c["members"] < 15:
        return False
    if not (c["every_member_splits_at_2_3_29"]
            and c["every_member_preserves_all_local_data"]):
        return False
    cc = bridge37.lemma_C_converse()
    if not cc["moved_at_every_multiplicative_conductor_prime"]:
        return False
    for ell in ("3", "29"):
        m = cc["per_prime"][ell]["moved"]
        if not m or not m["split_flag_flipped"]:
            return False
    for e in cc["untestable_primes"]:               # never silent
        if not cc["per_prime"][str(e)]["why_not"]:
            return False
    w = bridge37.the_witness_that_depends_on_it()
    if not (w["base_29_is_nonsplit"] and w["witness_would_be_lost_there"]
            and w["29_stays_nonsplit_for_every_member"]):
        return False
    a = bridge37.lemma_A_shadow()
    if not (a["all_identical"] and a["flips_seen"]):
        return False
    return bridge37.lemma_B_status()["established_here"] is False


def check_mod_ell_surjectivity() -> bool:
    """`24_Manin_Period_Audit`'s asserted maximality, certified where it can be.

    Every ℓ from 5 to the bound must have all six maximal classes refuted, and
    the witnesses must survive an independent re-derivation — the Borel witness
    really has `a² − 4ℓ'` a non-residue. `ℓ = 2` must be decided by the cubic
    rather than asserted, and its verdict must follow from its own two inputs.
    And `ℓ = 3` must stay UNcertified with both structural blocks intact: `S₄`
    unrefutable because it is the whole projective group, and the nonsplit
    Cartan test vacuous over all four residue classes. A gate that quietly
    promoted `ℓ = 3` would be reporting a partial check as a whole one.
    """
    two = surj38.ell_two()
    if two["surjective"] != (two["irreducible"]
                             and not two["discriminant_is_a_square"]):
        return False
    if not two["surjective"] or two["rational_roots"]:
        return False
    primes = surj38.good_primes(surj38.SEARCH)
    if len(primes) < 50:
        return False
    ells = [e for e in mazur33.small_primes(surj38.ELL_BOUND) if e > 3]
    if len(ells) < 30:
        return False
    for ell in ells:
        r = surj38.certify(ell, primes)
        if not r["surjective"] or r["undecided"]:
            return False
        b = r["witnesses"]["borel"]
        a, lp = b["a"], b["ell_prime"]
        # Re-derived by Euler's criterion here rather than by calling the gate's
        # own square test: checking a witness with the function that produced it
        # is re-running their script, which is the one thing this arm does not do.
        v = (a * a - 4 * lp) % ell
        if v == 0 or pow(v, (ell - 1) // 2, ell) != ell - 1:
            return False
    three = surj38.certify(3, primes)
    if sorted(three["undecided"]) != ["S4", "nonsplit_cartan_normalizer"]:
        return False
    v = surj38.vacuity_at_3()
    return v["structurally_vacuous"] and not v["any_case_refutes"]



def check_fw_h3_compiler() -> bool:
    """`09_FW_H3_Exact_Compiler`'s certificate, and the gap it must keep finding.

    The inputs must come out as RUN-033 measured them — W_- = {29}, v = 1,
    g_- = 1 — and the document's premise must hold. Then the boxed conclusion
    must still be **false at exactly p = 29**: the whole point of this gate is
    that testing the criterion finds what the gcd argument cannot see, so a
    version that stopped finding it has lost the finding, not fixed it. The
    routing answer must show every failing p taken by another branch whose
    witness FW-H3 could not have used. And the premise must be shown refusing
    somewhere, with the refused conclusion actually false there.
    """
    c = h3c39.uniform_certificate(h3c39.BASE)
    if c["W_minus"] != [29] or c["valuations"] != {"29": 1}:
        return False
    if c["g_minus"] != 1 or not c["premise_holds"]:
        return False
    if c["odd_p_tested"] < 50:
        return False
    if c["p_where_the_criterion_FAILS"] != [29]:   # the gap must survive
        return False
    if c["conclusion_holds_as_stated"]:
        return False
    r = h3c39.routing_answer()
    if not r["every_failing_p_is_routed_away"]:
        return False
    if not all(x["P3_witness_is_split"] for x in r["rows"]):
        return False
    f = h3c39.family()
    if f["members"] < 15:
        return False
    if not (f["W_minus_identical_to_the_base_for_every_member"]
            and f["g_minus_identical"] and f["same_failing_set"]):
        return False
    pf = h3c39.premise_failures()
    e, o = pf["W_minus_empty"], pf["g_minus_with_an_odd_factor"]
    if e is None or o is None:
        return False
    if e["premise_holds"] or o["premise_holds"]:
        return False
    return not o["criterion_at_that_p"]["pass"]


def check_fw_h2_ordinary() -> bool:
    """`10_FW_H2_and_Ordinary_Obstruction`'s exact ordinary criterion, run.

    Run at 1,500 rather than the gate's 6,000: 0.21s against 2.9s, and both sets
    the check needs are already non-empty there — the four smallest H2 failures
    and the three smallest supersingular primes. The gate itself still runs at
    6,000.

    Both sets must be NON-EMPTY. A criterion that never fires would make the
    document's routing argument rest on nothing, and a supersingular branch that
    is empty would make "FW is left to additive + supersingular" vacuous. Every
    failure must have a_p = +-1, which is the Hasse refinement. And no prime of
    bad reduction may appear in the good supersingular branch — that is what
    keeps RUN-037's single H3 exception away from it.
    """
    c = h2o40.classify(1500)
    fails = [(r["p"], r["a_p"]) for r in c["ordinary_H2_failures"]]
    if fails != [(7, 1), (113, 1), (211, -1), (1433, -1)]:
        return False
    if [r["p"] for r in c["supersingular"]] != [23, 251, 1061]:
        return False
    hr = h2o40.hasse_refinement(c)
    if not hr["all_are_plus_or_minus_one"] or not hr["failures"]:
        return False
    ne = h2o40.no_finite_exception(c, blocks=2)
    if not ne["keeps_producing"] or ne["total"] < 4:
        return False
    ss = h2o40.supersingular_branch(c)
    if not (ss["branch_is_non_empty"] and ss["H3_passes_at_every_one"]
            and ss["the_H3_exception_cannot_reach_here"]):
        return False
    pm = h2o40.potentially_multiplicative_branch()
    if not pm["branch_is_empty_for_this_curve"]:
        return False
    return h2o40.routing(c, blocks=2)["supported_by_measurement"]



def check_derived_bridge() -> bool:
    """`11_Derived_Supersingular_FW_Bridge`, assembled — and its supports kept
    apart.

    Run at 1,500 rather than the gate's 6,000: 0.21s against 2.7s, and the
    supersingular set is already non-empty there. The gate itself still runs at
    6,000.

    Three things must survive. H1 and H2 must stay marked **cited** while H3 is
    computed — a bridge whose supports are of two kinds must not report one
    verdict. The contrast with `09` must stay real: RUN-037's failing set has to
    be non-empty, or "11's range excludes it" is a statement about nothing. And
    the open item must stay open — neither the safe period condition nor the
    rank-zero corollary may report itself closed here.
    """
    h = brg41.hypotheses()
    if h["W_minus"] != [29] or h["valuations"] != {"29": 1}:
        return False
    if h["g_minus"] != 1 or not h["g_minus_is_a_power_of_two"]:
        return False
    q = brg41.quantifier_ranges(1500)
    if not q["the_09_failing_set"]:            # the contrast must be real
        return False
    if not (q["W_minus_and_supersingular_are_disjoint"]
            and q["every_09_failure_is_outside_11s_range"]):
        return False
    pp = brg41.per_prime(1500)
    if not (pp["branch_is_non_empty"] and pp["every_prime_has_all_three"]):
        return False
    for r in pp["rows"]:
        if "cited" not in r["H1"]["source"] or "cited" not in r["H2"]["source"]:
            return False
        if r["H3"]["source"] != "computed here":
            return False
    rz = brg41.rank_zero_corollary(2000)
    if not (rz["L_is_nonzero"] and rz["analytic_rank_is_zero"]):
        return False
    if rz["closed_here"] is not False:
        return False
    sp = brg41.safe_period_condition()
    if sp["computed_in_this_tree"] is not False:
        return False
    return any("Manin" in k for k in brg41.CITED)


def check_odd_additive_barrier() -> bool:
    """`01_Odd_Additive_Period_Barrier`'s condition, run on the family.

    The base must have an EMPTY barrier for the stated reason — its only
    additive prime is 2, which is not odd. Each member must meet the barrier at
    exactly `q`, with the twist valuations forced to (2, 3, 6) and the Kodaira
    type `I0*`. And the excluded types must be shown reachable: a condition
    whose excluded set is never exhibited has not been tested, so all three of
    II, III and IV must be produced and the condition must fail at each.
    """
    b = bar42.base_curve()
    if b["barrier_applies"] or b["additive_primes"] != [2]:
        return False
    f = bar42.family()
    if f["members"] < 15:
        return False
    if not (f["odd_additive_prime_is_always_q"] and f["kodaira_always_I0star"]
            and f["valuations_are_forced_2_3_6"]
            and f["every_member_meets_the_condition"]):
        return False
    ex = bar42.the_excluded_types_are_reachable()
    if not ex["all_three_reachable"] or not ex["and_the_condition_fails_there"]:
        return False
    for r in f["rows"]:
        if any(x["potentially_ordinary_computed"] for x in r["rows"]):
            return False                       # the limitation stays stated
    return bar42.link_to_run_039()["c_E_is_still_not_computed"]



def check_finite_exceptional() -> bool:
    """`04_Finite_Exceptional_Prime_Problem`'s three sets, and its §5 rule.

    Run at 1,500 with two buckets rather than the gate's 6,000 with four: 0.23s
    against 2.9s, and both facts the check needs — a non-empty P_loc that has
    not stopped — hold there. The gate itself still runs at 6,000.

    P_red must be empty and marked UNIVERSAL, since Mazur's theorem is what
    licenses that. P_ram's formula must be empty AND the criterion must still be
    obstructed at 29, so the document's own warning keeps being confirmed rather
    than quietly dropped. P_loc must be non-empty — an empty local set would
    make the whole routing argument unnecessary — and must be marked NOT
    universal, which is `04` §5's rule applied to this arm's own reporting. And
    the blocking primes must be computed disjoint from the branch FW is used on.
    """
    r = fin43.p_red()
    if not r["is_empty"] or r["set"] or not r["claim_is_universal"]:
        return False
    if len(r["rows"]) != 12:
        return False
    m = fin43.p_ram()
    if not m["formula_says_empty"]:
        return False
    if m["criterion_actually_obstructed_at"] != [29]:
        return False
    if m["formula_misses"] != [29] or not m["the_warning_was_exact"]:
        return False
    l = fin43.p_loc(1500, 2)
    if l["is_empty"] or not l["has_not_stopped"]:
        return False
    if l["claim_is_universal"]:
        return False
    sc = fin43.success_criterion(1500, 2)
    if sc["achieved_for_all_odd_p"] is not False:
        return False
    if sc["which_factor_blocks_it"] != "P_loc":
        return False
    rt = fin43.the_routing_answer(1500)
    if not rt["P_loc_is_disjoint_from_the_FW_branch"] or rt["intersection"]:
        return False
    dr = fin43.degradation_rule(1500, 2)
    return (dr["no_bounded_test_is_reported_as_universal"]
            and dr["P_red"]["universal"] and not dr["P_loc"]["universal"])


def check_base_certificate() -> bool:
    """`15_696e1_Base_Certificate` against this tree, row by row.

    Run at 2,000 L-series terms rather than the gate's 20,000: 0.38s against
    29s, and RUN-032 measured the arithmetic verdicts identical at both.

    Every recomputed row must agree, and the rows this arm CANNOT compute must
    stay marked as such — algebraic rank, optimality, the Manin constant and the
    analytic Sha. A certificate that scored those would be reporting citations
    as checks. The discriminant row must still carry the square-class
    explanation, since comparing by value would report a disagreement between
    two correct models. And the document's refusal of the circular Sha inference
    must be read from the file rather than assumed.
    """
    rows = cmp44.compare(2000)
    if len(rows) < 20:
        return False
    computed = [r for r in rows if r["kind"].startswith("computed")]
    if len(computed) < 14:
        return False
    if any(r["agree"] is not True for r in computed):
        return False
    must_stay_cited = ("algebraic rank 0", "optimal", "Manin constant = 1",
                       "Ш_an = 1")
    for name in must_stay_cited:
        hit = [r for r in rows if r["row"] == name]
        if len(hit) != 1 or hit[0]["kind"].startswith("computed"):
            return False
    disc = [r for r in rows if r["row"].startswith("disc(f₂) =")]
    if len(disc) != 1 or "SQUARE CLASS" not in disc[0].get("note", ""):
        return False
    res = [r for r in rows if r["row"].startswith("quadratic resolvent")]
    if len(res) != 1 or res[0]["recomputed_here"] != -174:
        return False
    ref = cmp44.the_refusal()
    return ref.get("document_found") and ref.get("refusal_is_in_the_document")



def check_claim_ladder() -> bool:
    """`07_Stop_Rules_and_Claim_Ladder`, applied to this line.

    The rung must stay C1 and partial: H2 and H3 executable, H1 cited, and C2
    NOT reached. A gate that reported C2 would be committing `07`'s fifth
    forbidden upgrade in this arm's own voice, which is the one thing this check
    exists to prevent. The five guards must be found in the archived logs rather
    than assumed — a stand-in that stops reading the logs must turn this red.
    The stop rule must be answered from real sources, and every report must
    carry an explicit statement of what it does not claim.
    """
    hm = ladder45.hypothesis_meanings()
    if hm["C1_reached"] or not hm["C1_partial"]:
        return False
    if sorted(hm["executable"]) != ["H2", "H3"] or hm["cited"] != ["H1"]:
        return False
    pos = ladder45.position()
    if not pos["C0"]["reached"] or not pos["C1"]["partial"]:
        return False
    if pos["C2"]["reached"] is not False:
        return False
    if not pos["C2"]["FW_is_listed_as_cited"]:
        return False
    if any(pos[r]["reached"] for r in ("C3", "C4", "C5", "C6")):
        return False
    if pos["honest_rung"] != "C1 (partial)":
        return False
    fu = ladder45.forbidden_upgrades()
    if len(fu["rows"]) != 5 or not fu["all_guards_present"]:
        return False
    sr = ladder45.stop_rule()
    if sr["rule_triggered"]:
        return False
    if len(sr["last_three"]) < 3:
        return False
    if not sr["each_of_the_last_three_compiled_a_new_document"]:
        return False
    rc = ladder45.reports_carry_their_limits()
    return rc["reports"] >= 40 and rc["every_report_carries_its_limits"]


def check_chebotarev_audit() -> bool:
    """`25_Chebotarev_Referee_Audit`, every step run.

    The chain must reproduce `disc = -11136`, the squarefree part `-174`, the
    containments — `Q(sqrt -6)` inside `Q(zeta_24)` and `Q(sqrt 29)` NOT inside,
    which is why it has to be adjoined — `[K:Q] = 16`, S_3's single nontrivial
    proper normal subgroup, `[LK:Q] = 48`, class size 2 and `delta = 1/24`. And
    the compatibility must still be exhibited against a case where it FAILS: a
    transposition has sign -1, contradicts the identity on `F_0`, and would give
    density 0. A gate that only ever showed the compatible side would not have
    tested the step the derivation most depends on.
    """
    c = cheb46.the_cubic()
    if c["discriminant"] != -11136 or not c["factorisation_check"]:
        return False
    if not c["irreducible"] or c["discriminant_is_a_square"]:
        return False
    if c["galois_group"] != "S_3" or c["squarefree_part"] != -174:
        return False
    f = cheb46.the_fields()
    if not f["factorisation_holds"] or not f["degree_K_is_16"]:
        return False
    if not f["sqrt_minus_6_in_cyclotomic_24"]["inside"]:
        return False
    if f["sqrt_29_in_cyclotomic_24"]["inside"]:
        return False
    if f["F0_in_cyclotomic_24"]["inside"] or not f["F0_inside_K"]:
        return False
    i = cheb46.the_intersection()
    if not i["unique_nontrivial_proper_normal_subgroup"]:
        return False
    if i["its_degree"] != 2 or i["normal_subgroup_orders"] != [1, 3, 6]:
        return False
    d = cheb46.the_class_and_density()
    if not d["compatible"] or d["class_size"] != 2:
        return False
    if d["transposition_acts_trivially_on_F0"]:      # the failing side
        return False
    if d["incompatible_alternative_density"] != 0:
        return False
    if not d["degree_LK_is_48"] or not d["delta_is_one_over_24"]:
        return False
    from fractions import Fraction
    x = cheb46.cross_checks(Fraction(d["delta"]))
    return x["agrees_with_RUN_018"] and x["within_one_percent"]



def check_fw_compiler() -> bool:
    """`02_Fouquet_Wan_Hypothesis_Compiler`'s Level-1 certificate.

    The keys must be exactly the ones `02` specifies — a compiler that invents
    fields is not emitting the document's format. All three claim values must
    occur: a compiler that only ever says FW_APPLICABLE has not been exercised,
    and the rows that say otherwise are the ones carrying RUN-036's, RUN-037's
    and RUN-038's findings. Level 2 must stay unachieved and emit the string the
    document mandates for that state. And every H3 row must carry the
    formulation it was decided under, `02`'s third prohibition being the one
    this arm had to repair.
    """
    l1 = comp47.level1()
    if not l1["rows"] or not l1["keys_match_the_specification"]:
        return False
    by_p = {r["p"]: r for r in l1["rows"]}
    if by_p[3]["H1_absolute_irreducible"] != "UNKNOWN":
        return False
    if by_p[3]["H2_local_nondegenerate"] != "FAIL":
        return False
    if by_p[29]["H2_local_nondegenerate"] != "FAIL":
        return False
    if by_p[29]["H3_auxiliary_prime"] != "FAIL":
        return False
    if by_p[7]["H2_local_nondegenerate"] != "FAIL":
        return False
    if by_p[5]["claim"] != "FW_APPLICABLE":
        return False
    for v in ("FW_APPLICABLE", "FW_NOT_APPLICABLE", "UNKNOWN"):
        if not l1["tally"].get(v):
            return False
    for d in l1["detail"]:
        if not d["H3"].get("formulation"):
            return False
        if not d["H3"].get("gap_to_the_exact_condition"):
            return False
    l2 = comp47.level2()
    if l2["achieved"] is not False:
        return False
    if l2["this_gate_outputs"] != "FW verified for tested primes":
        return False
    pr = comp47.prohibitions(l1)
    return all(v["obeyed"] for k, v in pr.items() if isinstance(v, dict))


def check_h2_chain() -> bool:
    """The H2 chain's internal consistency and the H3 disagreement.

    The equivalence must be EXHAUSTED, not asserted — a stand-in that reports
    equivalence without checking pairs must turn this red. `10`'s single
    congruence must come out complete for every good ordinary p >= 5 and NOT at
    3, since that asymmetry is the finding. And the disagreement between `02` and
    `08` must still be found in the files, and must still be reported unresolved:
    a gate that quietly picked the reading flattering this arm's own earlier
    verdicts would be doing the opposite of its job.
    """
    eq = chain48.equivalence_03_08()
    if not eq["equivalent"] or eq["mismatches"]:
        return False
    if eq["pairs_checked"] < 10_000:
        return False
    oc = chain48.ordinary_case_completeness()
    if not oc["complete_for_every_p_at_least_5"]:
        return False
    if not oc["the_exception_is_3"]:
        return False
    if oc["primes_where_the_second_case_survives"] != [2, 3]:
        return False
    ch = chain48.the_chain()
    if ch["verified_here"] != 2 or ch["cited"] != 2:
        return False
    hd = chain48.the_h3_dispute()
    if not hd["02_line_present"] or not hd["08_title_present"]:
        return False
    if not hd["the_disagreement_is_real"]:
        return False
    if not hd["08_and_09_state_the_same_conditions"]:
        return False
    return hd["this_gate_does_not_resolve_it"] is True



def check_provisional_vs_revised() -> bool:
    """`18` against `27`, and the set all three documents describe.

    The three definitions must land on the same primes — `18`/`27`'s three
    conditions, this tree's membership test, and Referee A's five. `18`'s five
    referee items must stay scored honestly: one addressed by `27`, one
    deferred, three open. A version that reported them all addressed would be
    doing the corpus a favour it did not ask for. `27`'s six-branch router must
    still be a partition with nothing unrouted, and the witnesses it names must
    still match what RUN-033 and RUN-037 computed from the other end.
    """
    sets = prev49.three_definitions()
    if not sets["all_three_agree"] or sets["counts"]["18/27"] < 15:
        return False
    if sets["in_18_not_in_tree"] or sets["in_tree_not_in_18"]:
        return False
    red = prev49.redundancy_of_the_29_condition()
    if not red["the_condition_is_redundant_here"]:
        return False
    if not red["the_implication_needs_the_mod_24_condition"]:
        return False      # a redundancy shown only one way is not measured
    items = prev49.audit_items()
    if items["counts"] != {"addressed": 1, "deferred": 1, "open": 3}:
        return False
    q = sets["per_this_tree"][0]
    part = prev49.router_partition(q, 300)
    if part["unrouted"] or not part["every_prime_has_exactly_one_branch"]:
        return False
    if len(part["branches_used"]) != 6:
        return False
    w = prev49.router_witnesses()
    if not w["agree"] or not w["leave_one_out_matches"]:
        return False
    if not w["nonsplit_witness_matches"]:
        return False
    lab = prev49.claim_labels()
    return (lab["18"]["present"] and lab["20"]["present"]
            and lab["27"]["present"] and lab["27"]["next_present"])


def check_candidate_schema() -> bool:
    """`13`'s schema and `14`'s sieve, with the control that must FAIL.

    The anchor must meet `14`'s boxed criterion and have a distinct witness at
    each fixed multiplicative prime. The control matters more: a curve of
    conductor 116 must be FOUND, must have a nonsplit multiplicative prime, and
    must still fail — one reservoir, no distinct witness. A gate that could not
    exhibit the failing side would be confirming a criterion it never watched
    fail, which is the shape RUN-033, RUN-035 and RUN-040 each had to guard.
    And none of `13`'s six obligations may be reported closed.
    """
    a = schema50.sieve_criterion(schema50.BASE)
    if not a["boxed_criterion_met"]:
        return False
    if not (a["B1_is_a_power_of_two"] and a["B2_is_a_power_of_two"]):
        return False
    if not a["every_fixed_multiplicative_p_has_a_witness"]:
        return False
    if a["W_mult_odd"] != [3, 29] or a["W_minus"] != [29]:
        return False
    hunt = schema50.find_by_conductor(schema50.CONTROL_N)
    if not hunt["found"]:
        return False
    for ai in hunt["found"]:
        c = schema50.sieve_criterion(ai)
        if not c["at_least_one_nonsplit"]:          # it must LOOK like a pass
            return False
        if c["at_least_two_odd_multiplicative"]:
            return False
        if c["boxed_criterion_met"]:
            return False
        if c["every_fixed_multiplicative_p_has_a_witness"]:
            return False
    obl = schema50.obligations()
    return obl["none_are_closed"] and len(obl["rows"]) == 6



def check_source_audits() -> bool:
    """`22` and `23`, the corpus's own citation audits.

    `23`'s weight-2 specialisation must keep checking out — a_29 = -1 with 29
    nonsplit, a_3 = +1 with 3 split — because that arithmetic is the whole of
    what this arm can verify about the convention. The cited hypotheses must
    stay marked cited: `22`'s case C rests on reading a theorem statement, and a
    version that scored it computed would be reporting a reading as arithmetic.
    And the maximal-versus-irreducible finding must survive: irreducible at
    every Mazur degree, maximality NOT certified at 3, Borel refuted there.
    """
    c = audits51.case_hypotheses()
    if c["total_hypotheses"] < 12:
        return False
    if not c["verdict_counts"].get("cited"):
        return False              # the reading must stay a reading
    mvi = audits51.maximal_versus_irreducible()
    if not mvi["irreducible_at_every_Mazur_degree"]:
        return False
    if not mvi["maximality_NOT_certified_at_3"]:
        return False
    if not mvi["borel_refuted_at_3"]:
        return False
    if mvi["maximality_certified_count"] < 30:
        return False
    h3 = audits51.h3_convention()
    if h3["a_29"] != -1 or not h3["29_is_nonsplit"]:
        return False
    if h3["a_3"] != 1 or not h3["3_is_split"]:
        return False
    if not h3["the_specialisation_checks_out"]:
        return False
    if not h3["residual_ramification"]["any_odd_p_not_29_keeps_it_ramified"]:
        return False
    mv = audits51.what_moves()
    if not mv["RUN_046"]["the_quote_is_present"]:
        return False
    return mv["RUN_047"]["corrected_count"] == {"addressed": 2, "deferred": 1,
                                                "open": 2}


def check_novelty_and_routes() -> bool:
    """`26`'s box and `01`'s matrix, against what this line actually did.

    The box must stay unscoreable: zero of its four steps are work this arm can
    do, and a gate that claimed one would be claiming external access it does
    not have. Every novelty-term sentence must be a refusal or a PINNED
    quotation — unpinning them must turn this red, since the pins are the only
    thing separating a quotation from a claim. `01`'s STOP route must stay
    untouched and PRIMARY GO best covered. And the two rounds on non-prioritised
    routes must stay named: hiding them would make the coverage look like
    obedience to a plan this arm does not follow.
    """
    n = routes52.novelty_rule()
    if not n["document_found"] or not n["box_present"]:
        return False
    if n["steps_this_arm_can_do"]:
        return False
    if len(n["remaining_steps"]) != 4:
        return False
    c = routes52.no_round_claims_novelty()
    if c["unaccounted"] or not c["no_unaccounted_mention"]:
        return False
    if c["classified_descriptive"] != len(routes52.CLASSIFIED_MENTIONS):
        return False
    if c["mentions"] < 8 or c["refusals"] < 4:
        return False
    # A refusal must be a whole word. "nothing" contains "not" and "another"
    # contains "not", and a substring test read three sentences as refusals
    # that refused nothing. `.get` with a sentinel rather than `[...]`, because
    # a scan missing the field must turn this check RED, not raise — a defect
    # that raises is not a defect a check caught.
    if c.get("refused_by_substring_only", -1) != 0:
        return False
    # And the classifier is tested on a fixture, not only on the corpus. The
    # drill runs BEFORE the finaliser writes the drill tables, so at this
    # moment no report contains the check's own name — the case the strip
    # exists for cannot be exhibited by the corpus while it is being tested.
    fx = routes52.check_name_is_not_prose()
    if not fx["all_ok"] or len(fx["rows"]) < 5:
        return False
    r = routes52.route_matrix()
    if not r["stop_route_untouched"]:
        return False
    if not r["primary_go_is_the_most_covered"]:
        return False
    o = routes52.off_priority_rounds()
    return o["count"] == 2 and all(x["verdict"] in ("HOLD",
                                                    "separate Phase later")
                                   for x in o["rows"])



def check_consensus_and_experiment() -> bool:
    """`00`'s consensus and `06`'s experiment plan.

    The three guards `00` §6 demands must be present AND grounded. The third is
    about RUN-036's own surjectivity certificate, and the guard IS the UNKNOWN
    rows RUN-045 kept — a version reporting the guard present with those rows
    gone is reporting a hollow guard. The eleven prohibitions must stay eleven
    with every list independently clear, because a total that survives one list
    going unaudited is a total that means nothing. The quantifier must stay
    open. The success gate must stay at two of four with H3's row still marked
    disputed: a gate scored met is the exact overclaim `07` forbids. And step
    4's 不得默認相同 must stay recorded as violated, since that is RUN-046's
    finding and softening it would hide this line's own result.
    """
    fs = consensus53.forbidden_substitutions()
    if not fs["all_guards_present"] or len(fs["rows"]) != 3:
        return False
    if fs["primes_certified_by_RUN_036"] < 30:
        return False
    if fs["primes_marked_UNKNOWN_by_RUN_045"] < 1:
        return False              # the rows ARE the third guard
    tl = consensus53.three_forbidden_lists()
    if tl["total_prohibitions"] != 11 or len(tl["lists"]) != 3:
        return False
    if not all(l["all_clear"] for l in tl["lists"]):
        return False
    if sorted(l["count"] for l in tl["lists"]) != [3, 3, 5]:
        return False
    mp = consensus53.the_main_problem()
    if mp["for_all_p_FW"]["quantifier_closed"] is not False:
        return False
    sg = consensus53.success_gate()
    if sg["gate_is_met"] or sg["met_or_supplied"] != 2 or sg["of"] != 4:
        return False
    if not any("DISPUTED" in r["status"] for r in sg["rows"]):
        return False
    st = consensus53.experiment_steps()
    if not st["step_4_was_violated_in_the_corpus"]:
        return False
    return (st["step_7_census_exists"] is False
            and st["unknown_rows_kept_visible"] > 0)


def check_compiler_targets() -> bool:
    """`02`'s four targets, and `06` v0.3 run as far as it goes.

    The two local branches must stay NOT COMPUTED HERE. v0.3 exists to replace
    RUN-045's UNKNOWN with an exact local isogeny test, and this tree computes
    no local Galois data — a version reporting those branches decided would be
    claiming precisely the arithmetic the round says it cannot do, which is the
    one mis-report that would matter here. Branch 1 must keep not firing and H3
    must keep passing with witness 29 at every member. The base curve must keep
    an EMPTY 𝒜_odd: 696.e1's only additive prime is 2, and a base carrying an
    odd one would make `06`'s finite-table claim a different claim. Target 3's
    domain must stay empty at g_mult^odd = 1 — scoring an empty domain as an
    achieved target would report three of four targets in hand. And the census
    detector must keep matching `02` §4's five status columns: it once matched
    on the filename and hit src19's CONDUCTOR census, so any log listed as the
    census means it has gone back to matching a name.
    """
    p = targets54.v03_procedure()
    if p["members"] < 19:
        return False
    if not (p["branch_1_never_fires"] and p["H3_passes_at_every_member"]
            and p["H1_unknown_at_every_member"]):
        return False
    if (p["steps_decided_here"], p["steps_partial"],
            p["steps_outside"]) != (2, 1, 2):
        return False
    for r in p["rows"]:
        h2 = r["LOCAL_H2"]
        if h2["verdict"] != "UNKNOWN":
            return False
        if h2["branch_2_local_irreducible_over_Fp"] != "NOT COMPUTED HERE":
            return False
        if h2["branch_3_local_isogeny_kernel_test"] != "NOT COMPUTED HERE":
            return False
        if r["H3"]["witness_ell"] != 29 or not r["H3"]["computed"]:
            return False
        if "not reachable" not in r["FINAL"]:
            return False
    a = targets54.a_odd()
    if a["base_A_odd"] or a["base_size"]:
        return False
    if not (a["every_member_has_exactly_one"] and a["and_it_is_q"]):
        return False
    t = targets54.compiler_targets()
    if t["g_mult_odd"] != 1 or t["odd_divisors_of_g_mult"]:
        return False
    if not t["target_3_domain_is_empty"] or not t["no_census_exists"]:
        return False
    if len(t["rows"]) != 4:
        return False
    d = targets54.discipline_lines()
    if len(d["census_status_columns"]) != 5:
        return False
    if d["logs_carrying_that_census"]:
        return False
    return bool(d["both_obeyed"]) and bool(d["rule_2"]["obeyed_here"])



def check_local_isogeny_kernel() -> bool:
    """`04`'s local kernel criterion, and the consequence it does not state.

    Step 2 must keep naming `p` odd: at p = 2 every point is its own negative,
    the clause carries no Galois information, and a chain that dropped the
    hypothesis would be reporting a criterion that always passes. The last step
    must keep naming local REDUCIBILITY — that is the whole precondition, and
    the round's headline is that it is undecided here. `omega^2 = 1` must keep
    coming back at exactly {2, 3}, computed by brute force AND agreeing with
    the closed form `(p-1)|2` — the first draft wrote that divisibility
    backwards and the two columns disagreed at p = 2, so the agreement is the
    thing being asserted, not either column alone. The two tests must stay
    mutually exclusive above 3 and joint at 3. And the precondition must stay
    undecided with the refusal recorded: reading RUN-036's GLOBAL surjectivity
    as settling the LOCAL question is `00` §6's substitution one level down,
    and `07` names it as a forbidden shortcut outright.
    """
    ch = kern55.derivation_chain()
    if ch["steps_count"] != 5:
        return False
    if "odd" not in ch["steps"][1]["hypothesis"].lower():
        return False
    if "REDUCIBLE" not in ch["steps"][-1]["hypothesis"]:
        return False
    if not kern55.p_odd_is_load_bearing()["p_odd_is_load_bearing"]:
        return False
    co = kern55.cyclotomic_order()
    if not co["agrees_with_the_divisibility"]:
        return False
    if co["omega_squared_trivial_at"] != [2, 3]:
        return False
    if co["primes_checked"] < 40:
        return False
    mx = kern55.mutual_exclusivity()
    if mx["both_tests_can_fire_at"] != [3]:
        return False
    if not mx["mutually_exclusive_at_every_p_ge_5"]:
        return False
    pr = kern55.precondition_local_reducibility()
    if pr["decided_here"] is not False:
        return False
    if not pr["global_surjectivity_does_not_settle_this"]:
        return False
    if kern55.p_minus_1_divides_2_appearances()["count_of_reports"] < 1:
        return False
    if kern55.three_cases()["count"] != 3:
        return False
    return kern55.what_it_would_cost()["members"] >= 19


def check_family_schema_and_spec() -> bool:
    """`05`'s proof obligations and `07`'s implementation spec.

    `05` declines to be a theorem claim, so `all_five_proved` must stay False
    and the boxed conclusion unreachable — scoring it as met would be this arm
    inventing a claim the corpus refused to make. Both gaps must stay open:
    they are where this line independently stopped, and closing one in the
    report without closing it in the arithmetic is the failure `07_Stop_Rules`
    forbids. The p = 3 reasons must stay counted FROM THE LOGS and stay at
    four or more across three rounds — a count assembled from prose is RUN-029's
    failure mode. `07`'s verdict key must stay unfillable and its fixtures
    unrunnable, because that is the same gap RUN-052 measured from the other
    end. All four forbidden inferences must keep their guards. And the
    prohibition total must stay 15 over 4 documents: the two documents numbered
    `07` are different documents, and a count that merged them by number would
    silently lose four prohibitions.
    """
    bh = schema56.bridge_hypotheses()
    if bh["count"] != 5:
        return False
    if bh["all_five_proved"] is not False:
        return False
    if bh["reachable_here"] is not False:
        return False
    gp = schema56.two_gaps()
    if not gp["both_open"] or not gp["gap_A"]["still_open"]:
        return False
    if not gp["gap_B"]["still_open"] or not gp["gap_B"]["and_it_is_hypothesis_4"]:
        return False
    if schema56.hybrid_bands()["count"] != 3:
        return False
    p3 = schema56.p3_structural_reasons()
    if p3["count"] < 4 or len(p3["distinct_rounds"]) < 3:
        return False
    sc = schema56.spec_schema_coverage()
    if sc["the_verdict_key_is_fillable"] is not False:
        return False
    if sc["fillable_here"] >= sc["required_keys"]:
        return False
    if schema56.backend_rules()["count"] != 4:
        return False
    fi = schema56.forbidden_inferences()
    if fi["count"] != 4 or not fi["all_clear"]:
        return False
    if not all(r["guard_present"] for r in fi["rows"]):
        return False
    pc = schema56.prohibition_count()
    if pc["total"] != 15 or pc["documents"] != 4 or not pc["all_clear"]:
        return False
    rf = schema56.regression_fixtures()
    return rf["count"] == 6 and rf["runnable_here"] == 0



def check_condition_map() -> bool:
    """Theorem 2.18's condition map on the whole Phase 1 census.

    E2 must agree with the census BY SET, not by count — a swapped pair of
    curves keeps the count at 2,709 and is a different answer. E4 must be the
    ∃-form: for every p | N SOME q ≠ p with p ∤ v_q(Δ); the ∀-form is a
    different, stricter condition that this base does not satisfy. The 2-torsion
    root finder must resolve every CLZ20 curve — the float version came back
    unresolved on 2,154 of 3,747, and an unresolved 8b is not a checked 8b. The
    twist conditions must stay green on a sample AND consistent with their own
    failure table. And the base must be the 40,749 RUN-004 fixed: a gate that
    ran on a different population would report numbers about something else.
    """
    base = cmap57.load_base()
    removed = cmap57.load_removed()
    if len(base) != 40749 or len(removed) != 4062:
        return False
    e1 = cmap57.e1_semistable(base)
    if not e1["all_pass"] or e1["curves"] != 40749:
        return False
    e2 = cmap57.e2_small_trace(base, removed)
    if not e2["agree_exactly"] or e2["only_mine"] or e2["only_census"]:
        return False
    if e2["abs_a3_eq_3_recomputed"] != 2709:
        return False
    e4 = cmap57.e4_ramification(base)
    if not e4["all_pass"] or e4["curves"] != 40749:
        return False
    if e4["prime_conductor_curves"] != 0:
        return False
    br = cmap57.branches(base)
    if not br["matches_RUN_008"]:
        return False
    if br["8b_two_torsion_unresolved"] != 0:
        return False
    if br["8b_more_than_one_rational_root"] != 0:
        return False
    if not br["8b_all_three_nonsquare_conditions_hold"]:
        return False
    tw = cmap57.twist_conditions(base, cmap57.load_new_map(), limit=150)
    if not tw["all_pass"] or tw["failures_by_condition"]:
        return False
    if tw["entries_checked"] < 500 or tw["labels_not_in_base"]:
        return False
    return cmap57.output_semantics()["converse_holds"] is False


def check_paper_vs_code() -> bool:
    """The three rules behind the three census artefacts, from the diffs.

    Each rule's text must be FOUND in the archived diff, as an added or removed
    line — a gate that reported the rules without locating them would be
    restating the audit from memory. The `and` semantics must come back {3,5,7}
    on every curve with 0 empty bad-prime sets: that is a Python fact, and a
    version reporting the intersection would be reporting what was perhaps
    intended rather than what ran. The prediction must hold with 0 tripped and
    1,355 strict removals, since one tripped curve falsifies the whole account.
    And 02's pins must stay 1 present / 1 partial / 1 absent / 2 N-A with zero
    rank fields — scoring the paper version present, or inventing a rank column,
    is the overclaim 02 §6–§7 exist to prevent.
    """
    base = cmap57.load_base()
    removed = cmap57.load_removed()
    rules = prov58.three_rules()
    if not rules["diffs_present"]:
        return False
    g = rules["generator_7286794"]
    o = rules["old_1a0489c"]
    c = rules["current_31fae20"]
    if not (g["found_as_removed_line_in_gen_to_old_diff"]
            and o["found_as_added_line_in_gen_to_old_diff"]
            and o["found_as_removed_line_in_old_to_current_diff"]
            and c["found_as_added_line_in_old_to_current_diff"]
            and c["a3_filter_added_in_old_to_current_diff"]):
        return False
    sem = prov58.and_semantics(base)
    if sem["so_on_every_base_curve_it_is"] != [3, 5, 7]:
        return False
    if sem["base_curves_with_empty_bad_primes"] != 0:
        return False
    if sem["with_bad_primes_{2,7}"] != [3, 5, 7] or sem["with_bad_primes_empty"]:
        return False
    pred = prov58.the_prediction(base, removed)
    if not pred["prediction_holds"]:
        return False
    if pred["that_the_relaxed_rule_would_have_removed"] != 0:
        return False
    if pred["that_the_strict_rule_removes"] != 1355:
        return False
    art = prov58.the_three_artefacts(base, removed)
    if not art["all_three_consistent"]:
        return False
    if art["current_base_31fae20"]["removed"] != 4062:
        return False
    pins = prov58.pins_02_demands()
    if (pins["present"], pins["partial"], pins["absent"],
            pins["not_applicable_by_scope"]) != (1, 1, 1, 2):
        return False
    if pins["section_7_rank_fields_in_base_record"] != []:
        return False
    return pins["section_5_flags_recorded_in_metadata"] is False



def check_lemma_b_reduction() -> bool:
    """FW-H2 at the twisting prime by Lemma B, and member 3529.

    The failing set must be exactly [3529]: an ordinary test read backwards
    makes every member supersingular and H2 pass everywhere, and a family that
    quietly loses 3529 loses the finding. a_3529 must be 1 by TWO code paths —
    src15's Legendre count inside the gate and src57's square-table count
    called here — because the whole round rests on one integer. The chain must
    keep three cited steps and three computed ones, with S4 verified-in-corpus:
    a version that scored a cited step computed would be the overclaim 07 Rule
    4 forbids. RUN-038's bucketed failure list must be read as buckets — the
    first draft read a flat key and reported this line's own archive wrongly.
    The revised router must stay recorded as NOT using FW at p = q, and the
    profile must stay LEMMA_B_REDUCTION, never 07's FW17_EXACT.
    """
    ch = lemb59.chain()
    if len(ch["rows"]) != 7:
        return False
    if sorted(ch["computed_steps"]) != ["S5", "S6", "S7"]:
        return False
    if len(ch["cited_steps"]) != 3:
        return False
    mb = lemb59.members(brute_at=())
    if mb["members"] < 19 or not mb["all_good"] or not mb["all_ordinary"]:
        return False
    if mb["failing_members"] != [3529]:
        return False
    r = next((x for x in mb["rows"] if x["q"] == 3529), None)
    if r is None or r["a_q"] != 1 or r["FW_H2_at_q"] != "FAIL":
        return False
    if cmap57.a_p(lemb59.BASE, 3529) != r["a_q"]:
        return False                      # two code paths, one integer
    pt = lemb59.the_pieces_were_in_the_tree()
    if not pt["RUN_038_listed_3529_as_an_a_p2_eq_1_failure"]:
        return False
    if not pt["RUN_047_confirmed_3529_in_P_by_all_three_definitions"]:
        return False
    wd = lemb59.which_design_it_breaks()
    if wd["revised_design"]["applies_FW_at_p_equals_q"] is not False:
        return False
    if wd["provisional_design"]["applies_FW_at_p_equals_q"] is not True:
        return False
    if lemb59.membership_condition()["members_with_a_q2_eq_1"] != [3529]:
        return False
    pf = lemb59.the_profile()
    if pf["is_07s_FW17_EXACT"] is not False:
        return False
    if pf["profile"] != "LEMMA_B_REDUCTION":
        return False
    return lemb59.consistency_with_RUN_053()[
        "agrees_with_RUN_053_mutual_exclusivity"] is True



def check_cross_round_joins() -> bool:
    """The joins instrument must be able to find the one join already known.

    A gate that intersects every prime set in every log is only measuring
    something if the 3529 join — RUN-038's obstruction list meeting RUN-047's
    membership list — survives its filters. A scaffolding filter wide enough to
    swallow it, a small-prime floor above 3529, a scan that skips RUN-038's
    log, or a containment filter read backwards would each leave a gate that
    runs green over nothing. The check does not run the report scan and asserts
    no count of unmade joins: that number is a measurement each new report is
    meant to change.
    """
    sets = joins60.prime_sets()
    if len(sets) < 20:
        return False
    kept, _dropped = joins60.drop_constants(sets)
    all_joins = joins60.joins(kept)
    if not all_joins:
        return False
    known = joins60.the_known_join(all_joins)
    if not known["found"]:
        return False
    return known["of_which_touch_RUN_038s_log"] >= 1



def check_one_commit_and_delta() -> bool:
    """07, 11, 12 and 14 on the one commit RUN-056 measured.

    The delta must be OLD minus (isogeny ∪ a_3) — a version that forgets the
    a_3 column lands at 39,394 and is the OLD twist blob, not the CURRENT base.
    11's figures must all recompute and its two pool percentages must imply one
    pool. The histogram warning must stay JUSTIFIED: the 500K a_3 share is
    two-thirds against the fixture's one-thirteenth, and a gate that scored the
    warning unjustified would be endorsing the extrapolation 11 forbade. Gate
    B's item 5 must stay 0 — that zero is what RUN-060 explains — and Gate C
    must stay not done: the descent replay has been run by nobody.
    """
    base = cmap57.load_base()
    removed = cmap57.load_removed()
    new_map = cmap57.load_new_map()
    a = commit61.autopsy_07()
    if not (a["RUN_056_located_old_rule_in_diff"]
            and a["RUN_056_located_new_rule_in_diff"]
            and a["RUN_056_located_a3_filter_in_diff"]):
        return False
    i = commit61.impact_11(base, removed)
    if not i["all_agree"] or not i["pre_candidate_pool_implied"]["agree_to_within_one"]:
        return False
    h = commit61.histogram_11_called_unknown(removed)
    if h["sum"] != 4062 or not h["the_warning_was_justified"]:
        return False
    d = commit61.delta_verifier_12_and_gate_a_14(base, removed, new_map)
    if not d["sets_equal"] or d["actual_current"] != 36687:
        return False
    if d["removed_by_columns"] != 4062:
        return False
    g = commit61.gate_b_14(base, removed, new_map)
    if not g["4_equals_3"] or g["5_twists_added_after_deleting_old_disc_gate"] != 0:
        return False
    if g["3_stable_curves_with_twist_changes"] != 5437 or g["6_both_effect_curves"] != 0:
        return False
    return commit61.gate_c_14()["done_by_this_line"] is False


def check_algorithm2_replay() -> bool:
    """15's exact replay and 09's two branches.

    The 2×2 must agree cell by cell and |T_O| must be 268,697 — one dropped
    pair is a different replay. The deleted predicate must be transcribed with
    ∃q, not ∀q: the ∀ form fails on real curves and moves pairs into D = 0
    cells that 15 measured as empty. 09's Case B must REJECT under D, or the
    predicate would be vacuous in principle and the round's explanation of
    15's zero would be vacuous with it. And the correction to RUN-055 must
    stay recorded: 15 §8 states the 1,355 identity, and a gate that lost that
    would let RUN-055's framing stand.
    """
    base = cmap57.load_base()
    old = _json.loads(cmap57.OLD_MAP.read_text(encoding="utf-8"))
    new = cmap57.load_new_map()
    c = replay62.chronology_15()
    if not (c["diffs_present"] and c["G_to_O_adds_disc_valuation_condition"]
            and c["O_to_C_removes_disc_valuation_condition"]
            and c["O_to_C_tightens_gcd"]):
        return False
    r = replay62.replay(base, old, new)
    if not r["cells_agree"] or r["T_O"] != 268697 or r["T_C"] != 247391:
        return False
    if not r["T_C_equals_new_map"]:
        return False
    if r["curve_classes"] != r["curve_classes_stated"]:
        return False
    if not r["CLZ20_has_no_3_dividing_d"]:
        return False
    if r["curves_failing_D_at_some_p_le_997"] != 0:
        return False
    f = replay62.fixtures_09()
    if not f["both_branches_exercised"] or not f["case_B"]["old_rejects"]:
        return False
    return replay62.correction_to_RUN_055()["present_in_15"] is True


def check_removed_13_and_soundness() -> bool:
    """08's thirteen rows and 03's six gates.

    All thirteen must agree under 08's ORDERING — strict isogeny first,
    smallest prime first, then a_3. Applied a_3-first, 26b1 becomes A3_ABS_3
    and the table breaks; that ordering is 08's own claim about the pipeline
    and the check holds it. 26b1 must stay the BOTH class. S6 must stay at
    exactly 6 of 7 with the timestamp missing: reporting seven would invent a
    field the metadata does not carry. And the fixture-vs-500K sum must stay
    4,062 — dropping the BOTH class loses two curves silently.
    """
    removed = cmap57.load_removed()
    meta = _json.loads(cmap57.REMOVED_JSON.read_text(encoding="utf-8"))
    t = thirteen63.table_08(removed)
    if t["count"] != 13 or not t["all_agree"] or t["mismatches"]:
        return False
    if t["histogram_from_table"] != t["histogram_stated"]:
        return False
    if not (t["26b1_is_the_BOTH_class"] and t["26b1_secondary_a3"] == -3
            and t["26b1_first_failure_is_isogeny_7"]):
        return False
    if not t["142e1_has_no_357_isogeny"]:
        return False
    f = thirteen63.fixture_versus_500k(removed)
    if f["sum"] != 4062:
        return False
    s = thirteen63.soundness_03(meta)
    if s["s6_count"] != 6 or s["s6_missing"] != ["timestamp"]:
        return False
    return s["not_applicable_by_scope"] == 4



def check_discrepancy_corpus() -> bool:
    """02's four adversarial curves against the 8b instrument — the negative
    control RUN-055 never had.

    All four must FAIL f'(x0) non-square. 02 says a version that accepts them
    earns the label REGRESSION?; that is what this check enforces on this
    line's own instrument, and it is the one place a defect in the square test
    can be caught: on the accepted base every curve passes, so a square test
    that always said "not a square" would have been green for two rounds. The
    shard must be present with its CRLF hash matching the package and its LF
    hash NOT matching — a version that reported the LF hash as matching would
    be reporting a pin that does not exist. And the four must be read from the
    shard: three of four typed from memory were wrong.
    """
    pin = corpus64.shard_pin()
    if not pin["shard_present"]:
        return False
    if not pin["crlf_matches_package"] or pin["lf_matches_package"]:
        return False
    if not pin["byte_gap_equals_line_count"]:
        return False
    four = corpus64.the_four(cmap57.load_base())
    if not four["all_found"] or not four["none_in_base"]:
        return False
    if not four["all_exactly_one_root"]:
        return False
    if four["f_prime_square_count"] != 4:
        return False
    if not four["the_other_two_nonsquare_conditions_hold"]:
        return False
    nc = corpus64.negative_control_for_RUN_055()
    return nc["RUN_055_f_prime_squares_found"] == 0 and nc["RUN_055_checked"] == 3747



def check_phase1_closure() -> bool:
    """16's checklist, 01's fixture, 00's two hand fixtures, completeness.

    The <150 fixture must come out 25 → 12 with the 13 removed being 08's, by
    label. 00's two lists must reproduce exactly — they are the only Algorithm 2
    outputs the corpus prints in full, and a predicate that drifted from 01's
    text would show there first. Completeness must be exact on the sample with
    04's bound: a predicate that dropped a condition admits d the map does not
    carry, and a bound above 1000 does the same — both must read as
    admissible-but-absent. 16 must stay at eight items and 10's label must stay
    unawarded: the package is not the reproduction run the label names.
    """
    base = cmap57.load_base()
    new = cmap57.load_new_map()
    f = closure65.fixture_150(base, new)
    if not f["agrees"] or not f["removed_is_08s_thirteen"]:
        return False
    if f["current"] != 12 or f["old"] != 25:
        return False
    z = closure65.fixtures_00(base, new)
    if not z["both_agree"] or z["106d1"]["negative_d_admissible"]:
        return False
    n = closure65.negative_twists(base, new, limit=10)
    if n["with_an_admissible_negative_d"] != 0 or n["map_has_negative_d"]:
        return False
    c = closure65.completeness(base, new, sample=6)
    if not c["sample_exact"]:
        return False
    if closure65.checklist_16()["count"] != 8:
        return False
    return closure65.layers_10()["label_awarded_here"] is None


def check_phase1_protocols() -> bool:
    """The six protocol documents against the package and this line.

    04 must be read as STATING the bound 1000 and REFUSING the full
    reproduction claim — those two sentences are what the round rests on. The
    stop-rule proxy must not fire on this line's own recent rounds. The
    regression record must stay at 5 of 7 with exactly code_version and
    semantic_version missing — a version reporting seven would be inventing
    the two fields 06's changelog is about. The handoff's discrepancy count
    must stay 0 with this line as the mirror, and 04's preflight outputs must
    stay 0 of 7 by exact name: the package never claimed to be that run.
    """
    e = proto66.environment_04()
    if not e["states_twist_bound_1000"] or not e["refuses_full_reproduction_claim"]:
        return False
    if not proto66.enclosure_05()["boxed_not_forall_E"]:
        return False
    if proto66.stop_rule_on_this_line()["freeze_triggered"]:
        return False
    r = proto66.regression_05()
    if r["carried_count"] != 5 or r["missing"] != ["code_version", "semantic_version"]:
        return False
    c = proto66.changelog_06()
    if c["count"] != 8 or c["measured_here"] != 4:
        return False
    h = proto66.handoff_06()
    if h["count"] != 6 or h["Ds_discrepancies_found"] != 0:
        return False
    return proto66.preflight_04()["present_by_exact_name"] == 0



def check_phase0_maps() -> bool:
    """Phase 0's three maps against this line's reports.

    02's four open rows must stay four with no report claiming one closed, and
    the seven-component tally must stay 4 computed / 1 partial / 2 never — a
    version counting the regulator as fully computed would be claiming the
    saturation nobody verified. Every round the reading cites must exist, and
    every attribution's signature phrase must be found in the cited report: a
    reading that cites a round for a finding it does not contain is RUN-060's
    failure the other way round. The 首選 route must be the most worked, the
    紅燈 route must have no round, and RUN-003's log must still say 0 of 85
    documents claim its conditions met. E's eight leaps must all be named in
    08 and all covered.
    """
    reports = maps67._reports()
    c = maps67.closure_map_02(reports)
    if len(c["open_rows"]) != 4 or not c["no_open_row_claimed_closed"]:
        return False
    if c["rounds_cited_that_do_not_exist"] or c["component_signatures_absent"]:
        return False
    if (c["components_computed_here"] != 4 or c["components_partial_here"] != 1
            or len(c["components_never_here"]) != 2):
        return False
    r = maps67.route_matrix_04(reports)
    if not r["首選_is_most_worked"] or r["red_routes_worked_by_any_round"]:
        return False
    if not r["red_route_claimed_met_nowhere"] or r["rounds_cited_that_do_not_exist"]:
        return False
    h = maps67.handoff_08(reports)
    if h["count"] != 6 or len(h["leaps_named_in_08"]) != 8 or h["leaps_covered"] != 8:
        return False
    return not h["rounds_cited_that_do_not_exist"] and not h["leap_signatures_absent"]



def check_algorithm2_mirror_and_diff() -> bool:
    """03's mirror and 13's diff, on a sample where the full run is a minute.

    The point-count formula must agree with brute-force enumeration and with
    Hasse on every sampled (curve, p); the cubic identity 16f(x) = F(4x) must
    hold on the whole base; 03's inertness hypotheses must hold on every
    sampled Zhai pair; 46a1 and 106d1 must read back. 13's +1899 / −53404 must
    reproduce with git, the entry census must give 0 added and the package's
    own row counts, every added line must be a comma drop or a re-alignment
    with none new, the deleted lines must account exactly, and the twelve
    <150 survivors must show 0 deltas.
    """
    base = cmap57.load_base()
    new = cmap57.load_new_map()
    old = json.loads(cmap57.OLD_MAP.read_text(encoding="utf-8"))
    pc = mirror68.point_count_crosscheck(base, sample=200)
    if not pc["agree"] or pc["pairs_checked"] < 1000:
        return False
    if not mirror68.cubic_forms_agree(base)["agree"]:
        return False
    ih = mirror68.inert_hypotheses(base, new, sample=300)
    if not ih["agree"] or ih["pairs"] < 1000:
        return False
    fx = mirror68.fixtures_03(old, new, base)
    if not fx["46a1_agrees"] or not fx["106d1_agrees"]:
        return False
    ld = mirror68.line_diff()
    if not ld["agrees"]:
        return False
    cl = mirror68.classify_added_lines()
    if not cl.get("every_added_line_is_a_comma_drop_or_realignment", False):
        return False
    ec = mirror68.entry_census(old, new)
    if not ec["package_agrees"] or not ec["monotone_in_fact"] or not ec["RUN_060_agrees"]:
        return False
    if not mirror68.line_accounting(ld, ec, cl)["accounts_exactly"]:
        return False
    return mirror68.fixture_150_deltas(old, new, base)["agrees"]



def check_anomalous_norm_localization() -> bool:
    """P5 v1.1's exact figures, recomputed with the gate's own group law.

    The short model and generator images must derive from [0,1,1,−2,0]; the
    two point counts, the orders of P', the discrete logarithms, the four
    cofactor multiples and the two slopes must all agree with the document;
    the slopes must equal the logarithms mod 11 — the consistency the document
    does not state; ρ must be surjective with the document's kernel basis a
    basis of determinant 390,830 and v_11 = 2; the label count must be seven
    CLOSED_EXACT and one OPEN with no report of this line promoting the ratio.
    """
    A, B = anom69.short_model(anom69.AINVS)
    Ps, Qs = anom69.to_short(anom69.AINVS, anom69.P_MIN), anom69.to_short(anom69.AINVS, anom69.Q_MIN)
    if (A, B) != (-3024, 46224) or Ps != (12, 108) or Qs != (48, 108):
        return False
    local = {}
    for ell in anom69.ELLS:
        d = anom69.local_data(A, B, ell, Ps, Qs)
        if not d["agrees"] or not d["P_generates"]:
            return False
        # the order is certified by multiplication, not read back from order_of
        n = d["count"]
        if anom69.ec_mul(A, ell, n, Ps) is not anom69.O:
            return False
        if any(anom69.ec_mul(A, ell, n // q, Ps) is anom69.O for q in (2, 5, 11, 17, 19) if n % q == 0):
            return False
        local[ell] = d
    rho = anom69.simultaneous_reduction(local[397], local[991])
    if not rho["agrees"] or rho["J_S_order_of_cokernel"] != 1:
        return False
    reports = {f.name[:7]: f.read_text(encoding="utf-8") for f in sorted(anom69.REPORTS.glob("RUN-*.md"))}
    lab = anom69.label_discipline(reports)
    if not lab["agrees"]:
        return False
    at11 = anom69.anomalous_at_11(A, B)
    return at11["ordinary"] and not at11["anomalous_in_mazurs_sense"] and at11["a_11"] == -4



def check_kurihara_modular_symbols() -> bool:
    """The Kurihara certificate's computation, against this tree's own log.

    The eigenline is rebuilt in full — relations, Hecke at 2, 3, 5, plus — and
    must be the logged λ coordinate for coordinate, with the four eigenvalue
    checks passing: a transposed Merel action or Stein's star in place of the
    real-part plus condition would change it. Three of the forty blocks of the
    392,040-term sum are recomputed and must match the log block by block —
    terms, integer raw product sum and all six coefficients — so a path-sign
    slip, a wrong primitive root or an unskipped non-unit goes red without
    the full ten-second sum. The logged blocks must add to the logged totals,
    δ must be 5 at λ(1,5) = 1 with the stress-test package's raw sum, and the
    rank-1 number at 397 must be 0.
    """
    log = _json.loads(kur70.OUT.read_text(encoding="utf-8"))
    e = kur70.eigenline()
    if not e["agrees"] or e["lambda"] != log["lambda"]:
        return False
    if not all(v["agrees"] and v["is_eigenvector"] for v in e["eigenvalue_checks"].values()):
        return False
    sample = (0, 20, 39)
    part = kur70.kurihara_sum(e["lambda"], block_ids=sample)
    logged = {b["block"]: b for b in log["kurihara_blocks"]}
    for blk in part["per_block"]:
        want = logged.get(blk["block"])
        if want is None or blk["terms"] != want["terms"] or blk["raw_product_sum"] != want["raw_product_sum"]:
            return False
        if blk["mod_11"] != want["mod_11"]:
            return False
    tot = {k: 0 for k in ("const", "X", "Y", "X2", "Y2", "XY")}
    terms = raw = 0
    for b in log["kurihara_blocks"]:
        for k in tot:
            tot[k] += b["mod_11"][k]
        terms += b["terms"]
        raw += b["raw_product_sum"]
    k = log["kurihara"]
    if terms != k["terms"] or terms != k["phi_n"] or raw != k["raw_product_sum"]:
        return False
    if any(tot[c] % 11 != k["theta_bar_mod_I3"][c] for c in tot):
        return False
    if k["delta_n_XY_coefficient"] != 5 or k["raw_product_sum"] != 43605160:
        return False
    if any(k["theta_bar_mod_I3"][c] != 0 for c in ("const", "X", "Y", "X2", "Y2")):
        return False
    tab = kur70.log_table(397, kur70.ROOTS[397])
    r1 = sum((sum(e["lambda"][i] for i in kur70.path_indices(a, 397)) % 11) * tab[a] for a in range(1, 397)) % 11
    return r1 == 0 and log["rank_one_kurihara_numbers"]["397"] == 0



def check_determinantal_bockstein() -> bool:
    """v1.3's determinant, the invariance, the ratio's scale law, Kim's hypotheses.

    det(B_N) must come out of the ring as exactly 2·XY, with (1+X)^11 ≡ 1
    there; the 100 generator changes must preserve the line and the order and
    reach every unit. The scale law δ_{g',h'} = δ·log_{g'}(5)·log_{h'}(6) is
    checked on one block of the sum against the logged block. Every Frobenius
    witness is re-verified for the property it is cited for WITH THIS CHECK'S
    OWN Legendre symbol and projective order — a gate whose residue test is
    inverted would certify from a witness that certifies nothing, and a check
    that reused the gate's test would agree with it. E(Q_11)[11] = 0, c_389 =
    1 and trivial torsion must hold from the point counts. Labels 3 and 2.
    """
    bd = bock71.bockstein_determinant()
    if not bd["agrees"] or not bd["relation_gamma_to_the_11_is_automatic_mod_I3"]:
        return False
    gi = bock71.generator_change_invariance()
    if not (gi["ord_I_2_preserved"] and gi["line_F11_XY_preserved"] and gi["every_unit_reached"]):
        return False
    # the scale law on one block, against the logged block at roots (5, 6)
    log70 = _json.loads(kur70.OUT.read_text(encoding="utf-8"))
    lam = log70["lambda"]
    g, h = 13, 7
    u = kur70.log_table(397, g)[5]
    v = kur70.log_table(991, h)[6]
    old = dict(kur70.ROOTS)
    kur70.ROOTS[397], kur70.ROOTS[991] = g, h
    try:
        part = kur70.kurihara_sum(lam, block_ids=(7,))["per_block"][0]
    finally:
        kur70.ROOTS.update(old)
    logged = next(b for b in log70["kurihara_blocks"] if b["block"] == 7)
    if part["terms"] != logged["terms"] or part["mod_11"]["XY"] != logged["mod_11"]["XY"] * u * v % 11:
        return False
    if bock71.ratio_under_primitive_roots(5, check_pairs=())["every_unit_is_a_reachable_ratio"] is not True:
        return False
    kim = bock71.kims_hypotheses()
    if not kim["agrees"] or not kim["local_p_torsion"]["E_Q11_11_is_zero"]:
        return False
    if kim["local_p_torsion"]["count_F11"] % 11 == 0:
        return False
    w = kim["residual_surjectivity"]["witnesses"]
    allowed = {"A4": (1, 2, 3), "S4": (1, 2, 3, 4), "A5": (1, 2, 3, 5)}
    for name, wit in w.items():
        if wit is None:
            return False
        q, a = wit["witness"], wit["a"]
        if kur70.a_q(q) != a:
            return False
        disc = (a * a - 4 * q) % 11
        sq = disc == 0 or pow(disc, 5, 11) == 1          # this check's own Legendre symbol
        if name == "borel" and sq:
            return False
        if name == "split_cartan_normalizer" and (a % 11 == 0 or sq):
            return False
        if name == "nonsplit_cartan_normalizer" and (a % 11 == 0 or disc == 0 or not sq):
            return False
        if name in allowed:
            uu = (a * a % 11) * pow(q % 11, 9, 11) % 11     # this check's own projective order
            o = 1 if uu == 4 else 2 if uu == 0 else 3 if uu == 1 else 4 if uu == 2 else 5 if (uu * uu - 5 * uu + 5) % 11 == 0 else 6
            if o in allowed[name]:
                return False
    reports = {f.name[:7]: f.read_text(encoding="utf-8") for f in sorted(bock71.REPORTS.glob("RUN-*.md"))}
    return bock71.labels(reports)["agrees"]



def check_attack03_cyclotomic() -> bool:
    """GPT-6's Attack 03: the adjugate identity in the actual ring and over Z,
    the §5 constants, the §7 counterexample, and the document's own labels.
    An adjugate without its off-diagonal signs fails A·z = 0; a wrong U_m
    coefficient fails χ(U_m) = m/f_χ; u without its 11 in the denominator
    fails h₀ = D₀u; a unit-root search that admits 0 returns two roots."""
    r = atk72.adjugate_identity_in_the_ring()
    z = atk72.adjugate_identity_over_Z(60)
    c = atk72.constants()
    ce = atk72.counterexample()
    lab = atk72.labels()
    return r["agrees"] and z["agrees"] and c["agrees"] and ce["agrees"] and lab["agrees"]


def check_attack04_padic_l() -> bool:
    """GPT-6's Attack 04: the mod-11 p-adic L-function from this tree's own
    eigenline must reproduce the stated 11 group-basis coefficients, the
    t-series, μ = 0, λ = 2, all 110 summands of the document's table, and the
    Euler-factor arithmetic (s₃₉₇ = 3, s₉₉₁ = 2, leading terms 9t², 4t²)."""
    ur = atk73.unit_root()
    if not ur["agrees"]:
        return False
    lam = kur70.eigenline()["lambda"]
    m = atk73.measure(lam)
    if m["group_basis_coefficients"] != atk73.STATED["group_basis"] or m["t_basis_coefficients"] != atk73.STATED["t_basis"]:
        return False
    if m["mu"] != 0 or m["lambda"] != 2 or m["unclassified_units"] or m["summand_count"] != 110:
        return False
    if not atk73.compare_with_theirs(m).get("agrees", False):
        return False
    ef = atk73.euler_factors()
    return ef["agrees"] and atk73.labels()["agrees"]


def check_attack05_local_log() -> bool:
    """GPT-6's Attack 05: [16]P and [16]Q exactly, s ≡ 99 and 66 (mod 121) of
    valuation 1, ℓ̄ = (4, 10), ker ∋ P + 4Q, #E(F₁₁) = 16, the Euler constant
    11² times a unit ≡ 7 — and identical to the document's exact output."""
    from fractions import Fraction as _F
    Pt, Qt = (_F(0), _F(0)), (_F(1), _F(0))
    res = {"P": atk74.local_log("P", Pt), "Q": atk74.local_log("Q", Qt)}
    for lab_, st in (("P", (99, 4)), ("Q", (66, 10))):
        r = res[lab_]
        if r["s_mod_121"] != st[0] or r["log_over_11_mod_11"] != st[1] or r["v11_of_s"] != 1:
            return False
    if (res["P"]["log_over_11_mod_11"] + 4 * res["Q"]["log_over_11_mod_11"]) % 11:
        return False
    pre = atk74.premises()
    return pre["agrees"] and atk74.compare_with_theirs(res).get("agrees", False) and atk74.labels()["agrees"]


def check_attack06_scalar_and_mellin() -> bool:
    """GPT-6's Attack 06: e₁₁/θ = 16 exactly in Q(α) with the stated exact
    values and 11-adic residues, the rank-one-update identities, the Sen
    matrix, and the Mellin formula giving L''(E,1)/2 within 1e-9 of the
    corpus's value with L(E,1) = 0."""
    lm = atk75.local_multiplier()
    ids = atk75.identities(120)
    mel = atk75.mellin()
    return (lm["agrees"] and ids["agrees"] and mel["agrees"]
            and atk75.compare_with_theirs(lm).get("agrees", False) and atk75.labels()["agrees"])


def check_attack07_geometry() -> bool:
    """GPT-6's Attack 07: F₆, F₈ as stated, the conic and model identities,
    the Bézout certificate mod 11, F₈ squarefree, g = −(3u+2)²/d with its
    zero over (P,Q) and (−P,−Q), ∂Γ_PQ = 4·Z_PQ, the diagonal chains, and
    the shifted points."""
    return (atk76.the_model()["agrees"] and atk76.tangent_function()["agrees"]
            and atk76.chains()["agrees"] and atk76.shifted_points()["agrees"] and atk76.labels()["agrees"])



def check_attack08_norms() -> bool:
    """GPT-6's Attack 08: the three norms from Vieta, the translation
    formulas, the sign identity and the full pushforward identity in the
    function field, div M = m_*Z_PQ, the closed-correction exponents
    (0,0,2), and the labels."""
    return (atk77.norms()["agrees"] and atk77.translations()["agrees"] and atk77.divisors()["agrees"]
            and atk77.closed_correction()["agrees"] and atk77.localisation()["agrees"]
            and atk77.labels()["agrees"] and atk77.compare_with_theirs(atk77.norms()).get("agrees", False))



def check_attack09_auxiliary() -> bool:
    """Attack 09 rewritten from this side: GPT-6's chi_8 has root number -1 and
    a vanishing even first layer (every tame branch, every twisted symbol
    [a/11]_chi8+, and L(E, chi_8 psi, 1) = 0 for the order-5 psi, against
    nonzero controls); over all fundamental |D| <= 100 prime to 11 the Hecke
    identity at level 11|D|, the first-layer total against (1 - chi(11)/alpha)^2
    S_D, the root-number-forced vanishing, the archimedean values as integers,
    and one unit per sign carrying them onto the mod-11 sums; chi_5 and chi_-3
    the smallest admissible characters, chi_65, chi_93, chi_-47 unusable."""
    po = atk78.parity_obstruction()
    tab = atk78.table()
    return po["agrees"] and tab["agrees"] and atk78.recommendation(tab)["agrees"]



def check_attack09_leading_term() -> bool:
    """GPT-6's Attack 09, the package: the minus eigenline identical to the
    package's 390-vector, the forty cusp paths (indices and values), the ten
    S_a and measures, the x^-1-weighted sum 9 and lambda_8(0) = 5, the Hecke
    relation of the twisted symbols at level 121, the Eisenstein data (B_2,
    constant term, f_beta, U_11), the Kummer unit's log mod 121, the smoothing
    and adjoint factors, the formal leading-term coefficients, the (20)
    algebra, the package's own criterion on the even D, and the labels."""
    fp = atk79.forty_paths()
    ed = atk79.eisenstein_data()
    ku = atk79.kummer_unit()
    fa = atk79.factors(fp["lambda8_at_zero"])
    fo = atk79.formal_algebra()
    return (atk79.minus_line()["agrees"] and atk79.alpha_twist()["agrees"] and fp["agrees"]
            and atk79.hecke_measure_relation()["agrees"] and ed["agrees"] and ku["agrees"] and fa["agrees"]
            and fo["agrees"] and atk79.scale_identities()["agrees"] and atk79.package_criterion()["agrees"]
            and atk79.labels()["agrees"] and atk79.compare_with_theirs(fp, ed, ku, fa, fo)["agrees"])


def check_attack10_unit_bridge() -> bool:
    """GPT-6's Attack 10: the circular unit identities in Z[zeta_8], L(1, chi_8)
    three ways, the 11-adic logarithm to 11^10 with all nineteen term residues
    and the five stated values, B_10,chi_8, the framed Frobenius entry, the
    trace algebra on 26 words / 676 pairs with both pivots and the alternative
    model, and the labels."""
    cu = atk80.circular_unit()
    pl = atk80.padic_log()
    bc = atk80.bernoulli_check()
    ta = atk80.trace_algebra()
    alt = atk80.trace_algebra((8, 9))
    F = atk80.Fraction
    return (cu["agrees"] and atk80.real_regulator()["agrees"] and pl["agrees"] and bc["agrees"]
            and atk80.frobenius_matrix()["agrees"] and ta["agrees"]
            and F(ta["Q_aa"]) == atk80.STATED["Q_aa"] and F(ta["Q_ab"]) == atk80.STATED["Q_ab"]
            and F(ta["v_a"]) == atk80.STATED["v_a"] and F(ta["v_b"]) == atk80.STATED["v_b"]
            and F(alt["Q_aa"]) == atk80.STATED["alt_Q_aa"] and F(alt["Q_ab"]) == atk80.STATED["alt_Q_ab"]
            and atk80.labels()["agrees"] and atk80.compare_with_theirs(cu, pl, bc, ta, alt)["agrees"])



def check_symbolic001_calibration() -> bool:
    """BSD Symbolic Round 001: every boxed identity of the cross-rank
    calibration document holds on exact random formal-series instances over
    all (e, d) patterns, a partner-dependent C is detected by (10.1) and
    (11.3), Theorem 4.1 is t-covariant with the rank-dependent ratio law,
    the PC-001 specialisation reproduces Attack 09's (19), log_11(12) is
    right to 11^12 with its cross-check, and the document's own labels."""
    return (sym81.symbolic_identities()["agrees"] and sym81.specialisation()["agrees"]
            and sym81.log_eleven_twelve()["agrees"] and sym81.labels()["agrees"])



def check_pc001_calibrator() -> bool:
    """PC-001 (the local GPT-6 line): the level-19 Manin space over Q, the
    plus and minus rational eigenlines identical to the line's primitive
    vectors, five Hecke checks against point counts, the first-layer
    ordinary and chi_8-twisted measures with every stated residue and the
    level-121 distribution relation, a_11(17.a1) = 0, the archimedean
    alignment of both periods (one unit per sign), and the labels."""
    lines = pc82.calibrator_lines()
    if not lines["agrees"]:
        return False
    return (pc82.measures(lines)["agrees"] and pc82.level_17_remark()["agrees"]
            and pc82.archimedean_alignment(lines)["agrees"] and pc82.labels()["agrees"])


def check_pc002_relative_regulator() -> bool:
    """PC-002 (the local GPT-6 line): the four 11-adic series of 389.a1 and
    19.a1 from the level-1331 layer - 2420 summand rows, the group and t
    coefficients, Q(t) to t^120 with Weierstrass degree 2 and leading 7 -
    identical to the line's; the width-11 agreement of the level-121 layer
    and the 121 -> 1331 refinement; the Farey cup pairing with ranks 64
    and 2, the cusp-gauge radicals, J_E = 1, J_0 = 3, Q_cup and the
    four-line invariance; and the labels."""
    cv = pc83.curves()
    rr = pc83.relative_regulator(cv)
    return rr["agrees"] and pc83.cup_normalisation(cv, rr)["agrees"] and pc83.labels()["agrees"]



def check_symbolic002_004_jets() -> bool:
    """BSD Symbolic Rounds 002-004: every boxed identity of the determinant
    lift, the anchored projective jet and the higher projective jets holds
    on exact random instances (exterior algebra on K^2, one- and two-variable
    formal families, unit renormalisations, coordinate changes, companions),
    with the gauge weights 2 and 4 independent of the jet order, and the
    documents' own labels."""
    rng = sym84.random.Random(sym84.RANDOM_SEED)
    return (sym84.round_002(rng)["agrees"] and sym84.round_003(rng)["agrees"] and sym84.round_004(rng)["agrees"]
            and sym84.labels()["agrees"])


def check_symbolic005_007_lattice() -> bool:
    """BSD Symbolic Rounds 005-007: the determinant-lattice torsor, the
    descent and support statements, and the derived Euler defect - sublattice
    and index-square laws, Z_p invisibility of prime-to-p indices, sqrt 3 in
    Q_11, Hilbert 90, Smith-invariant lengths, the sign calibration of the
    Euler defect and the mapping-cone formula on cones computed from their
    own differentials - all on explicit integer instances, and the labels."""
    rng = sym85.random.Random(sym85.RANDOM_SEED)
    return (sym85.round_005(rng)["agrees"] and sym85.round_006(rng)["agrees"] and sym85.round_007(rng)["agrees"]
            and sym85.labels()["agrees"])



COVERS = sorted(m.__name__ for m in (
    corpus00, ladder01, route02, nogo03, arith4, frob5, iso6, red7, x0n, kept,
    ph2, p5, alg2, glob14, anchor15, fam16, route17, tate18, bsd20, tw21,
    net22, p5u, led24, cv25, r2bsd, agent27, r1bsd, cov29, p1num, q9, cert32,
    mazur33, refA34, gcd35, nogo36, bridge37, surj38, h3c39,
    h2o40, brg41, bar42, fin43, cmp44, ladder45, cheb46,
    comp47, chain48, prev49, schema50, audits51, routes52,
    consensus53, targets54, kern55, schema56, cmap57, prov58,
    lemb59, joins60, commit61, replay62, thirteen63, corpus64,
    closure65, proto66, maps67, mirror68, anom69, kur70, bock71,
    atk72, atk73, atk74, atk75, atk76, atk77, atk78, atk79, atk80, sym81, pc82, pc83, sym84, sym85))


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
    "certificate-696e1": check_certificate_696e1,
    "mazur-degrees": check_mazur_degrees,
    "referee-a-checklist": check_referee_a_checklist,
    "gcd-witness-lemmas": check_gcd_witness_lemmas,
    "kodaira-nogo": check_kodaira_nogo,
    "twist-bridge": check_twist_bridge,
    "mod-ell-surjectivity": check_mod_ell_surjectivity,
    "fw-h3-compiler": check_fw_h3_compiler,
    "fw-h2-ordinary": check_fw_h2_ordinary,
    "derived-bridge": check_derived_bridge,
    "odd-additive-barrier": check_odd_additive_barrier,
    "finite-exceptional": check_finite_exceptional,
    "base-certificate": check_base_certificate,
    "claim-ladder": check_claim_ladder,
    "chebotarev-audit": check_chebotarev_audit,
    "fw-compiler": check_fw_compiler,
    "h2-chain": check_h2_chain,
    "provisional-vs-revised": check_provisional_vs_revised,
    "candidate-schema": check_candidate_schema,
    "source-audits": check_source_audits,
    "novelty-and-routes": check_novelty_and_routes,
    "consensus-and-experiment": check_consensus_and_experiment,
    "compiler-targets": check_compiler_targets,
    "local-isogeny-kernel": check_local_isogeny_kernel,
    "family-schema-and-spec": check_family_schema_and_spec,
    "condition-map": check_condition_map,
    "paper-vs-code": check_paper_vs_code,
    "lemma-b-reduction": check_lemma_b_reduction,
    "cross-round-joins": check_cross_round_joins,
    "one-commit-and-delta": check_one_commit_and_delta,
    "algorithm2-replay": check_algorithm2_replay,
    "removed-13-and-soundness": check_removed_13_and_soundness,
    "discrepancy-corpus": check_discrepancy_corpus,
    "phase1-closure": check_phase1_closure,
    "phase1-protocols": check_phase1_protocols,
    "phase0-maps": check_phase0_maps,
    "algorithm2-mirror-and-diff": check_algorithm2_mirror_and_diff,
    "anomalous-norm-localization": check_anomalous_norm_localization,
    "kurihara-modular-symbols": check_kurihara_modular_symbols,
    "determinantal-bockstein": check_determinantal_bockstein,
    "attack03-cyclotomic": check_attack03_cyclotomic,
    "attack04-padic-l": check_attack04_padic_l,
    "attack05-local-log": check_attack05_local_log,
    "attack06-scalar-and-mellin": check_attack06_scalar_and_mellin,
    "attack07-geometry": check_attack07_geometry,
    "attack08-norms": check_attack08_norms,
    "attack09-auxiliary": check_attack09_auxiliary,
    "attack09-leading-term": check_attack09_leading_term,
    "attack10-unit-bridge": check_attack10_unit_bridge,
    "symbolic001-calibration": check_symbolic001_calibration,
    "pc001-calibrator": check_pc001_calibrator,
    "pc002-relative-regulator": check_pc002_relative_regulator,
    "symbolic002-004-jets": check_symbolic002_004_jets,
    "symbolic005-007-lattice": check_symbolic005_007_lattice,
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
    ("one of the twelve is reported still removed, so the current fixture "
     "reads 13", "code", "phase1-closure",
     lambda: patch(closure65, "fixture_150", _fixture_reads_13)),
    ("the admissibility predicate drops the ordinary condition D4", "code",
     "phase1-closure",
     lambda: patch(closure65, "admissible", _admissible_without_ordinary)),
    ("the twist bound is taken as 2,000, so admissible d above 1,000 read as "
     "absent from the map", "code", "phase1-closure",
     lambda: patch(closure65, "TWIST_BOUND", 2000)),
    ("16's checklist is scored with a ninth item", "code", "phase1-closure",
     lambda: patch(closure65, "checklist_16", _nine_items)),
    ("10's label REPRODUCTION-QUALIFIED is awarded", "code", "phase1-closure",
     lambda: patch(closure65, "layers_10",
                   lambda: {**_true_layers65(), "label_awarded_here": "REPRODUCTION-QUALIFIED"})),
    ("Vieta's product rs is taken as x^2 + x + 2", "code", "attack08-norms",
     lambda: patch(atk77, "PROD_RS", [atk77.F(2), atk77.F(1), atk77.F(1)])),
    ("the addition map's pair is written (-5 - 2x, -1)", "code", "attack08-norms",
     lambda: patch(atk77, "NORM_PAIRS", {**atk77.NORM_PAIRS, "addition": ([atk77.F(-5), atk77.F(-2)], [atk77.F(-1)])})),
    ("the curve relation is reduced as y^2 = f_0 + y instead of f_0 - y", "code",
     "attack08-norms", lambda: patch(atk77, "Y2_LINEAR", 1)),
    ("y is given a double pole at O, so div M gains an O term", "code",
     "attack08-norms", lambda: patch(atk77, "POLE_ORDER_Y", 2)),
    ("the diagonal's degree under addition is taken as 2, not 4", "code",
     "attack08-norms",
     lambda: patch(atk77, "DEGREE_TABLE", {**atk77.DEGREE_TABLE, "diagonal": (1, 1, 2)})),
    ("the Kronecker symbol (D/2) is taken as +1 for D = +-3 mod 8", "code", "attack09-auxiliary",
     lambda: patch(atk78, "KRONECKER_TWO_RULE", (3, 5))),
    ("the twisted root number is written chi_D(N) w(E) without chi_D(-1)", "code", "attack09-auxiliary",
     lambda: patch(atk78, "ROOT_NUMBER_USES_CHI_MINUS_ONE", False)),
    ("the Euler factor (1 - chi(11)/alpha) enters to the first power, not squared", "code", "attack09-auxiliary",
     lambda: patch(atk78, "EULER_EXPONENT", 1)),
    ("the level-11D Hecke identity is written with a_11 - chi(11) instead of a_11 - 2 chi(11)", "code",
     "attack09-auxiliary", lambda: patch(atk78, "HECKE_TWIST_CONSTANT", 1)),
    ("the unit root is taken as 4 (a_11 read as +4)", "code", "attack09-auxiliary",
     lambda: patch(atk78, "UNIT_ROOT_OVERRIDE", 4)),
    ("the twisted conductor is taken as N |D| instead of N D^2", "code", "attack09-auxiliary",
     lambda: patch(atk78, "TWIST_LEVEL_EXPONENT", 1)),
    ("the measure's second term alpha^-2 [a] is added instead of subtracted", "code", "attack09-auxiliary",
     lambda: patch(atk78, "MEASURE_SECOND_TERM_SIGN", 1)),
    ("the path's sign alternates as (-1)^i in place of (-1)^(i-1) — invisible to a plus "
     "functional (RUN-068's control), but it negates every minus symbol, and Attack 09's "
     "forty values are signed", "code", "attack09-leading-term",
     lambda: patch(kur70, "path_indices", _path_wrong_sign)),
    ("Symbolic 002-004's determinant gauge weight is taken as 1 instead of 2", "code", "symbolic002-004-jets",
     lambda: patch(sym84, "GAUGE_WEIGHT_DETERMINANT", 1)),
    ("Symbolic 002-004's regulator gauge weight is taken as 2 instead of 4", "code", "symbolic002-004-jets",
     lambda: patch(sym84, "GAUGE_WEIGHT_REGULATOR", 2)),
    ("the jet wedge law is written u^-2 instead of u^-3", "code", "symbolic002-004-jets",
     lambda: patch(sym84, "JET_WEDGE_EXPONENT", -2)),
    ("the anchored jet is replaced by Round 002's raw wedge u ^ v, which is not unit-invariant", "code",
     "symbolic002-004-jets", lambda: patch(sym84, "ANCHOR_WITH_KAPPA", False)),
    ("the order additivity is read as e + m + 1", "code", "symbolic002-004-jets",
     lambda: patch(sym84, "ORDER_ADDITIVITY_OFFSET", 1)),
    ("the covector law is applied with J instead of J^-1", "code", "symbolic002-004-jets",
     lambda: patch(sym84, "COVECTOR_LAW_USES_INVERSE", False)),
    ("the calibrator power is made to follow the jet order m instead of the exterior degree 2", "code",
     "symbolic002-004-jets", lambda: patch(sym84, "CALIBRATOR_POWER_FOLLOWS_JET_ORDER", True)),
    ("Symbolic 005's index enters the regulator to the first power, not squared", "code", "symbolic005-007-lattice",
     lambda: patch(sym85, "INDEX_REGULATOR_EXPONENT", 1)),
    ("a height rescaling h -> uh is given exponent 1 on a rank-2 regulator", "code", "symbolic005-007-lattice",
     lambda: patch(sym85, "HEIGHT_RESCALING_EXPONENT", 1)),
    ("the Euler defect's sign convention is flipped", "code", "symbolic005-007-lattice",
     lambda: patch(sym85, "EULER_SIGN", -1)),
    ("the mapping cone is built with d(x,y) = (+d_C x, f x + d_D y), which is not a complex", "code",
     "symbolic005-007-lattice", lambda: patch(sym85, "CONE_SIGN_CONVENTION", 1)),
    ("the Q_11-not-Q witness is sought as sqrt 2, which has no root mod 11", "code", "symbolic005-007-lattice",
     lambda: patch(sym85, "HENSEL_SQUARE", 2)),
    ("an isogeny of degree d is given exponent 1 on the Gram determinant", "code", "symbolic005-007-lattice",
     lambda: patch(sym85, "ISOGENY_HEIGHT_EXPONENT", 1)),
    ("PC-001's plus line is normalised at coordinate 2 instead of coordinate 0", "code", "pc001-calibrator",
     lambda: patch(pc82, "PLUS_NORMALISATION_INDEX", 2)),
    ("PC-001's twisted unit root is taken as alpha_0 instead of chi_8(11) alpha_0", "code", "pc001-calibrator",
     lambda: patch(pc82, "TWIST_SIGN", 1)),
    ("PC-001's moment is taken against x instead of x^-1", "code", "pc001-calibrator",
     lambda: patch(pc82, "CHARACTER_EXPONENT", 1)),
    ("PC-001's smoothing integer is taken as 3, giving 10 instead of 26", "code", "pc001-calibrator",
     lambda: patch(pc82, "SMOOTHING_D", 3)),
    ("the Eisenstein T_2 eigenvalue at level 19 is looked for at 2 instead of 3", "code", "pc001-calibrator",
     lambda: patch(pc82, "EISENSTEIN_T2", 2)),
    ("PC-001's measure has its second term added instead of subtracted", "code", "pc001-calibrator",
     lambda: patch(pc82, "MEASURE_SECOND_TERM_SIGN", 1)),
    ("the calibrator's twisted L-series are cut at e^-5, so no value is a rational", "code", "pc001-calibrator",
     lambda: patch(pc82, "TAIL_EXPONENT", 5.0)),
    ("PC-002's twisted unit roots are taken as alpha instead of chi_8(11) alpha", "code", "pc002-relative-regulator",
     lambda: patch(pc83, "TWIST_SIGN", 1)),
    ("PC-002's lambda series integrate x instead of x^-1", "code", "pc002-relative-regulator",
     lambda: patch(pc83, "CHARACTER_EXPONENT", 1)),
    ("the Teichmuller projection is taken as u^-121, so <u> is not a power of 12", "code", "pc002-relative-regulator",
     lambda: patch(pc83, "TEICHMULLER_POWER", 121)),
    ("the Farey cup pairing is divided by 2 instead of 6", "code", "pc002-relative-regulator",
     lambda: patch(pc83, "CUP_DENOMINATOR", 2)),
    ("the Farey cup pairing is taken with the opposite orientation R^-1", "code", "pc002-relative-regulator",
     lambda: patch(pc83, "R_MAP", "other")),
    ("PC-002's measures have their second term added instead of subtracted", "code", "pc002-relative-regulator",
     lambda: patch(pc83, "MEASURE_SECOND_TERM_SIGN", 1)),
    ("PC-002's series are produced from the level-121 layer, which certifies only 11 coefficients", "code",
     "pc002-relative-regulator", lambda: patch(pc83, "LAYER", 2)),
    ("Symbolic 001's leading term is read one order too high, at t^(e+d+1)", "code", "symbolic001-calibration",
     lambda: patch(sym81, "LEADING_OFFSET", 1)),
    ("Theorem 4.1 is applied with the ratio A_i(0)/A_k(0) inverted", "code", "symbolic001-calibration",
     lambda: patch(sym81, "FORMULA_A_RATIO_INVERTED", True)),
    ("the common factor j(t) is given a vanishing leading coefficient j_e = 0", "code", "symbolic001-calibration",
     lambda: patch(sym81, "J_LEADING_ZERO", True)),
    ("the calibration factor Gamma is formed without A_k(0)/A_i(0)", "code", "symbolic001-calibration",
     lambda: patch(sym81, "GAMMA_WITHOUT_A_RATIO", True)),
    ("the reparametrisation t = t'/u is applied with u^(+m) instead of u^(-m)", "code", "symbolic001-calibration",
     lambda: patch(sym81, "REPARAM_EXPONENT_SIGN", 1)),
    ("log_11(12) is summed with all plus signs, i.e. -log(1 - 11)", "code", "symbolic001-calibration",
     lambda: patch(sym81, "LOG_SERIES_SIGN", 1)),
    ("Attack 09's chi_8 is replaced by the odd character (-8/.)", "code", "attack09-leading-term",
     lambda: patch(atk79, "CHI8", {1: 1, 3: 1, 5: -1, 7: -1})),
    ("the twisted unit root alpha_F is taken as alpha_E instead of chi_8(11) alpha_E", "code",
     "attack09-leading-term", lambda: patch(atk79, "ALPHA_TWIST_SIGN", 1)),
    ("the moment is taken against x instead of x^-1", "code", "attack09-leading-term",
     lambda: patch(atk79, "CHARACTER_EXPONENT", 1)),
    ("the Eisenstein refinement is taken at the eigenvalue 1 instead of -11", "code", "attack09-leading-term",
     lambda: patch(atk79, "EISENSTEIN_REFINEMENT", 1)),
    ("the unit's logarithm is read from epsilon^12, which is not 1 mod 11", "code", "attack09-leading-term",
     lambda: patch(atk79, "UNIT_POWER", 12)),
    ("the smoothing integer is taken as 7, giving 48 instead of 26", "code", "attack09-leading-term",
     lambda: patch(atk79, "SMOOTHING_D", 7)),
    ("sqrt 2 is written as zeta_8 + zeta_8^3, whose square is -2", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "ROOT2_IN_ZETA8", (0, 1, 0, 1))),
    ("the circular unit's numerator and denominator are swapped", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "CIRCLE_EXPONENTS", ((3, 5), (1, 7)))),
    ("the bottom norm factor 1 - chi_8(11) is taken as 1, so u_bot = u_8", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "BOTTOM_NORM_EXPONENT", 1)),
    ("the logarithm series is started from u_bot^5, which is not 1 mod 11", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "BOTTOM_POWER", 5)),
    ("phi on the subline is taken as +1/11", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "FROBENIUS_SUB_EIGENVALUE", atk80.Fraction(1, 11))),
    ("Leopoldt's Euler factor is written 1 - 1/11 instead of 1 + 1/11", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "EULER_TWELVE_ELEVENTHS", atk80.Fraction(10, 11))),
    ("the model's lower-left entry of rho(a) is 6X instead of 5X", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "MODEL_LOWER", (6, 7))),
    ("the Bernoulli cross-check is run at n = 8 instead of n = 10", "code", "attack10-unit-bridge",
     lambda: patch(atk80, "BERNOULLI_N", 8)),
    ("the adjugate is written without its off-diagonal minus signs", "code",
     "attack03-cyclotomic", lambda: patch(atk72, "adj2_ring", _adj_no_signs)),
    ("U_m's second factor is given the coefficient 36 as well, so chi(U_m) is "
     "wrong on the characters trivial at 991", "code", "attack03-cyclotomic",
     lambda: patch(atk72, "U_COEFF", (36, 36))),
    ("the counterexample's u is taken as 1 + N_0 with no 11 in the denominator, "
     "so it is integral and the point is lost", "code", "attack03-cyclotomic",
     lambda: patch(atk72, "U_DENOMINATOR", 1)),
    ("the unit-root search admits the root 0, so two residues come back", "code",
     "attack03-cyclotomic",
     lambda: patch(atk72, "ordinary_unit_root",
                   lambda a11: [x for x in range(11) if (x * x - a11 * x + 11) % 11 == 0])),
    ("the Teichmuller lift is taken as a^10 instead of a^11", "code",
     "attack04-padic-l", lambda: patch(atk73, "teichmuller", lambda a: pow(a, 10, 121))),
    ("alpha^-3 is used for both terms of the measure", "code", "attack04-padic-l",
     lambda: patch(atk73, "unit_root", _unit_root_inv3_twice)),
    ("the cyclotomic generator is taken as 23 = 1 + 2*11 in place of 12", "code",
     "attack04-padic-l", lambda: patch(atk73, "GAMMA", 23)),
    ("s_ell is read from ell mod 11 instead of ell mod 121, so both exponents "
     "come out 0", "code", "attack04-padic-l",
     lambda: patch(atk73, "cyclotomic_exponent", lambda ell: atk73.gamma_exponent(ell % 11))),
    ("the formal parameter is taken as x/y instead of -x/y", "code",
     "attack05-local-log", lambda: patch(atk74, "formal_parameter", lambda x, y: x / y)),
    ("the multiple is 15 instead of #E(F_11) = 16, so [15]R is not in the "
     "formal group", "code", "attack05-local-log",
     lambda: patch(atk74, "reduction_group_order", lambda: 15)),
    ("ell is normalised by 16 alone, not 16*11", "code", "attack05-local-log",
     lambda: patch(atk74, "normalise", lambda s_, n: s_ / n)),
    ("the second Euler factor is inverted, 991/1045 for 1045/991", "code",
     "attack05-local-log", lambda: patch(atk74, "EULER_PAIRS", ((374, 397), (991, 1045)))),
    ("the minimal polynomial of alpha is taken as A^2 + 4A - 11", "code",
     "attack06-scalar-and-mellin", lambda: patch(atk75, "REL", (-4, 11))),
    ("beta is taken as 11*alpha instead of 11/alpha", "code",
     "attack06-scalar-and-mellin",
     lambda: patch(atk75, "beta_of", lambda alpha: atk75.QA(11) * alpha)),
    ("the Hecke recursion at prime squares uses a_p^2 instead of a_p^2 - p",
     "code", "attack06-scalar-and-mellin",
     lambda: patch(atk75, "a_prime_power", _a_prime_power_no_p)),
    ("the Mellin integrals are cut at y = 1 + 5/c instead of 1 + 60/c", "code",
     "attack06-scalar-and-mellin", lambda: patch(atk75, "CUT", 5.0)),
    ("F_6 is formed with +8nd^2 in place of -8nd^2", "code", "attack07-geometry",
     lambda: patch(atk76, "F6_COEFFS", (1, 4, 4, 8))),
    ("the Bezout certificate's T is multiplied by F_8 instead of F_8'", "code",
     "attack07-geometry",
     lambda: patch(atk76, "bezout_combination", lambda S, T, F8, F8p: _true_bezout76(S, T, F8, F8))),
    ("the chain coefficients are (1, -2, 2, -2)", "code", "attack07-geometry",
     lambda: patch(atk76, "CHAIN_COEFFS", (1, -2, 2, -2))),
    ("the tangent line is written 2x_1 + 3x_2 + 3", "code", "attack07-geometry",
     lambda: patch(atk76, "TANGENT", (2, 3, 3))),
    ("the 2x2 determinant is computed as ad + bc, the cross term's sign dropped",
     "code", "determinantal-bockstein", lambda: patch(bock71, "det2", _det_plus)),
    ("the ring is truncated at I^2 instead of I^3, so XY is killed and the "
     "determinant reads 0", "code", "determinantal-bockstein",
     lambda: patch(bock71, "ring_mul", _ring_mul_I2)),
    ("the residue test is inverted, so the Borel refutation is certified by a "
     "witness whose discriminant IS a residue", "code", "determinantal-bockstein",
     lambda: patch(bock71, "_is_square_mod", lambda a, ell: not _true_is_square71(a, ell))),
    ("the local 11-torsion test is inverted: E(Q_11)[11] reported 0 iff 11 "
     "divides #E(F_11)", "code", "determinantal-bockstein",
     lambda: patch(bock71, "local_p_torsion", _local_torsion_inverted)),
    ("the torsion gcd is taken over q = 2 alone, so it reads #E(F_2) = 5",
     "code", "determinantal-bockstein", lambda: patch(bock71, "TORSION_BOUND", 2)),
    ("Merel's matrices act on the column instead of the bottom row — the "
     "transposed Hecke action", "code", "kurihara-modular-symbols",
     lambda: patch(kur70, "hecke_rows", _hecke_transposed)),
    ("the plus condition is taken as Stein's star, lambda(c,d) = -lambda(-c,d)",
     "code", "kurihara-modular-symbols", lambda: patch(kur70, "PLUS_SIGN", -1)),
    ("the primitive root mod 991 is taken as 7 in place of 6, scaling the "
     "logarithms by 7", "code", "kurihara-modular-symbols",
     lambda: patch(kur70, "ROOTS", {397: 5, 991: 7})),
    ("multiples of 397 are not skipped, so the sum runs over more than phi(n) "
     "terms", "code", "kurihara-modular-symbols",
     lambda: patch(kur70, "kurihara_sum", _sum_without_the_skip)),
    ("the change of coordinates uses X = 36x + b2 in place of 36x + 3b2, so the "
     "generator images move", "code", "anomalous-norm-localization",
     lambda: patch(anom69, "to_short", _to_short_wrong_b2)),
    ("the doubling formula drops the A term: 3x^2 in place of 3x^2 + A", "code",
     "anomalous-norm-localization", lambda: patch(anom69, "ec_add", _ec_add_without_A)),
    ("the discrete logarithm is searched only up to the cofactor, so Q' = 244 P' "
     "is never found", "code", "anomalous-norm-localization",
     lambda: patch(anom69, "dlog", _dlog_short)),
    ("rho's image is computed without the compatibility factor, so it reads "
     "35,530 and rho is not surjective", "code", "anomalous-norm-localization",
     lambda: patch(anom69, "simultaneous_reduction", _rho_no_compatibility)),
    ("the label count includes section 0's definition, so CLOSED_EXACT reads 8",
     "code", "anomalous-norm-localization",
     lambda: patch(anom69, "label_discipline", _labels_count_definition)),
    ("03's D_x loses its factor 4, so the formula counts the wrong curve",
     "code", "algorithm2-mirror-and-diff",
     lambda: patch(mirror68, "formula_count", _formula_without_the_4)),
    ("the mirror's cubic is written with b4 in place of 2b4", "code",
     "algorithm2-mirror-and-diff",
     lambda: patch(mirror68, "cubic_03", _cubic_with_b4)),
    ("Hasse's bound is applied as a_p^2 <= p", "code",
     "algorithm2-mirror-and-diff",
     lambda: patch(mirror68, "point_count_crosscheck", _hasse_too_tight)),
    ("the OLD map is read from the CURRENT file, so nothing was ever removed",
     "code", "algorithm2-mirror-and-diff",
     lambda: patch(cmap57, "OLD_MAP", cmap57.NEW_MAP)),
    ("a re-aligned added line is classified as new content", "code",
     "algorithm2-mirror-and-diff",
     lambda: patch(mirror68, "classify_added_lines", _realigned_counted_as_new)),
    ("02's open row 'Sha finite in general' is read as 已關閉", "code",
     "phase0-maps",
     lambda: patch(maps67, "CLOSURE_ROWS", _sha_row_closed())),
    ("the regulator is counted fully computed, saturation included", "code",
     "phase0-maps", lambda: patch(maps67, "SEVEN", _regulator_computed())),
    ("a leap's attribution points at a finding the cited round does not "
     "contain: RUN-023 for 'Sha computed exactly'", "code", "phase0-maps",
     lambda: patch(maps67, "CAUGHT", {**maps67.CAUGHT,
                                       "circular BSD assumption": [("RUN-023", "Sha computed exactly")]})),
    ("the 紅燈 route is given RUN-003 as a round on it", "code", "phase0-maps",
     lambda: patch(maps67, "ROUTES", _red_route_worked())),
    ("a round that does not exist is cited on the twist-family route: RUN-099",
     "code", "phase0-maps",
     lambda: patch(maps67, "ROUTES", _route_cites_099())),
    ("04's twist bound is reported absent from the document", "code",
     "phase1-protocols",
     lambda: patch(proto66, "environment_04",
                   lambda: {**_true_env66(), "states_twist_bound_1000": False})),
    ("the stop-rule proxy reports a three-round streak", "code",
     "phase1-protocols",
     lambda: patch(proto66, "stop_rule_on_this_line", _streak_of_three)),
    ("05's record fields are all reported carried, code_version included",
     "code", "phase1-protocols",
     lambda: patch(proto66, "regression_05", _all_seven_carried)),
    ("06's handoff reports one discrepancy under negative twist convention",
     "code", "phase1-protocols",
     lambda: patch(proto66, "handoff_06",
                   lambda: {**_true_handoff66(), "Ds_discrepancies_found": 1})),
    ("04's seven preflight outputs are reported present by exact name", "code",
     "phase1-protocols",
     lambda: patch(proto66, "preflight_04",
                   lambda: {**_true_preflight66(), "present_by_exact_name": 7})),
    ("the square test always answers 'not a square', which the accepted base "
     "could never have exposed", "code", "discrepancy-corpus",
     lambda: patch(cmap57, "is_square", lambda n: False)),
    ("the four curves are read from memory instead of the shard: 66b1's "
     "a-invariants as the first draft typed them", "code", "discrepancy-corpus",
     lambda: patch(corpus64, "read_curve", _curves_from_memory)),
    ("the shard's LF hash is reported as matching the package", "code",
     "discrepancy-corpus",
     lambda: patch(corpus64, "shard_pin", _lf_reported_matching)),
    ("62a1 is reported as present in the 40,749 base", "code",
     "discrepancy-corpus",
     lambda: patch(corpus64, "the_four", _62a1_in_base)),
    ("the delta is computed as OLD minus the isogeny set only, forgetting the "
     "a_3 column", "code", "one-commit-and-delta",
     lambda: patch(commit61, "delta_verifier_12_and_gate_a_14", _delta_forgets_a3)),
    ("11's histogram warning is scored unjustified", "code",
     "one-commit-and-delta",
     lambda: patch(commit61, "histogram_11_called_unknown", _warning_unjustified)),
    ("14's Gate B reports a twist added after the disc gate was deleted",
     "code", "one-commit-and-delta",
     lambda: patch(commit61, "gate_b_14", _gate_b_added_one)),
    ("14's Gate C is reported done by this line", "code",
     "one-commit-and-delta",
     lambda: patch(commit61, "gate_c_14", lambda: {**_true_gate_c61(),
                                                     "done_by_this_line": True})),
    ("07's a_3 filter is reported unlocated in the diff", "code",
     "one-commit-and-delta",
     lambda: patch(commit61, "autopsy_07", _a3_filter_unlocated)),
    ("the deleted predicate is transcribed with ∀q in place of ∃q", "code",
     "algorithm2-replay",
     lambda: patch(replay62, "disc_valuation_condition", _disc_forall)),
    ("one OLD pair is dropped from the replay", "code", "algorithm2-replay",
     lambda: patch(replay62, "replay", _replay_drops_one)),
    ("09's Case B is reported as passing the deleted predicate", "code",
     "algorithm2-replay",
     lambda: patch(replay62, "fixtures_09", _case_b_passes)),
    ("the correction to RUN-055 is dropped: 15 §8 reported absent", "code",
     "algorithm2-replay",
     lambda: patch(replay62, "correction_to_RUN_055",
                   lambda: {**_true_correction62(), "present_in_15": False})),
    ("08's ordering is applied a_3 first, so 26b1 becomes A3_ABS_3", "code",
     "removed-13-and-soundness",
     lambda: patch(thirteen63, "first_failure_from_census", _a3_first)),
    ("26b1 is reported ISOGENY_ONLY, losing the BOTH class", "code",
     "removed-13-and-soundness",
     lambda: patch(thirteen63, "table_08", _26b1_not_both)),
    ("S6's timestamp is reported present", "code", "removed-13-and-soundness",
     lambda: patch(thirteen63, "soundness_03", _timestamp_present)),
    ("the fixture-vs-500K sum drops the BOTH class", "code",
     "removed-13-and-soundness",
     lambda: patch(thirteen63, "fixture_versus_500k", _sum_drops_both)),
    ("the scaffolding filter is widened to every prime below 200,000, so no "
     "intersection survives", "code", "cross-round-joins",
     lambda: patch(joins60, "SCAFFOLDING", set(anchor15.sieve(200_000)))),
    ("RUN-038's log is skipped by the scan, so the 3529 join cannot be found",
     "code", "cross-round-joins",
     lambda: patch(joins60, "prime_sets", _sets_without_src40)),
    ("the containment filter is read backwards: re-reads are kept and real "
     "joins dropped", "code", "cross-round-joins",
     lambda: patch(joins60, "joins", _joins_inverted_containment)),
    ("the small-prime floor is raised to 4,000, so every set below it — "
     "RUN-038's obstruction list included — is discarded", "code",
     "cross-round-joins", lambda: patch(joins60, "MIN_ELEMENT", 4000)),
    ("the ordinary test is inverted, so every member reads supersingular and "
     "H2 passes everywhere", "code", "lemma-b-reduction",
     lambda: patch(lemb59, "members", _members_inverted_ordinary)),
    ("member 3529 is dropped from the family, and the failure with it", "code",
     "lemma-b-reduction",
     lambda: patch(lemb59, "members", _members_without_3529)),
    ("RUN-038's failure list is read from a flat key again, so the archive "
     "says 3529 was never listed", "code", "lemma-b-reduction",
     lambda: patch(lemb59, "the_pieces_were_in_the_tree", _flat_key_read)),
    ("27's revised router is reported as applying FW at p = q", "code",
     "lemma-b-reduction",
     lambda: patch(lemb59, "which_design_it_breaks", _revised_uses_fw)),
    ("the verdict is reported under 07's FW17_EXACT profile", "code",
     "lemma-b-reduction",
     lambda: patch(lemb59, "the_profile", _profile_borrowed)),
    ("a cited step of the chain is scored computed", "code",
     "lemma-b-reduction",
     lambda: patch(lemb59, "CHAIN",
                   tuple((a, b, c, "COMPUTED") if a == "S3" else (a, b, c, d)
                         for a, b, c, d in lemb59.CHAIN))),
    ("E2's agreement with the census is scored by count rather than by set, "
     "so a swapped pair passes", "code", "condition-map",
     lambda: patch(cmap57, "e2_small_trace", _e2_by_count)),
    ("a_p comes back as p itself, so every curve is supersingular and every "
     "a_3 is 3", "code", "condition-map",
     lambda: patch(cmap57, "a_p", lambda ainvs, p: p)),
    ("E4 is read in the ∀-form — every q | N must witness — instead of the "
     "∃-form", "code", "condition-map",
     lambda: patch(cmap57, "e4_ramification", _e4_for_all)),
    ("the 2-torsion root finder goes back to float bracketing on a Cauchy "
     "bound", "code", "condition-map",
     lambda: patch(cmap57, "integer_roots_of_monic_cubic",
                   _float_roots_of_monic_cubic)),
    ("the twist-condition failures are counted but all_pass is reported True "
     "regardless", "code", "condition-map",
     lambda: patch(cmap57, "twist_conditions", _twist_inconsistent)),
    ("the relaxed rule is applied as if it were the strict one", "code",
     "paper-vs-code",
     lambda: patch(prov58, "relaxed_rule_removes", _relaxed_as_strict)),
    ("the `and` expression is reported as evaluating to the intersection",
     "code", "paper-vs-code",
     lambda: patch(prov58, "and_semantics", _and_as_intersection)),
    ("the generator-to-old diff is missing from the package", "code",
     "paper-vs-code",
     lambda: patch(prov58, "DIFF_GEN_OLD",
                   prov58.DIFF_GEN_OLD.with_name("no-such.diff"))),
    ("02's paper-version pin is scored PRESENT", "code", "paper-vs-code",
     lambda: patch(prov58, "pins_02_demands", _paper_version_present)),
    ("a rank column is reported in the base record", "code", "paper-vs-code",
     lambda: patch(prov58, "pins_02_demands", _rank_column_present)),
    ("04's chain drops the `p` odd hypothesis from step 2, where p = 2 makes "
     "the clause vacuous", "code", "local-isogeny-kernel",
     lambda: patch(kern55, "CHAIN",
                   tuple((a, b, "none") if i == 1 else (a, b, c)
                         for i, (a, b, c) in enumerate(kern55.CHAIN)))),
    ("the closed form goes back to (p-1) % 2, which is the divisibility "
     "backwards", "code", "local-isogeny-kernel",
     lambda: patch(kern55, "cyclotomic_order", _divisibility_backwards)),
    ("omega squared is reported trivial at every prime", "code",
     "local-isogeny-kernel",
     lambda: patch(kern55, "cyclotomic_squares_trivial", lambda p: True)),
    ("the two kernel tests are reported mutually exclusive at p = 3 too",
     "code", "local-isogeny-kernel",
     lambda: patch(kern55, "mutual_exclusivity", _exclusive_everywhere)),
    ("the precondition is reported settled by RUN-036's global surjectivity",
     "code", "local-isogeny-kernel",
     lambda: patch(kern55, "precondition_local_reducibility", _local_settled)),
    ("05's five bridge hypotheses are scored as all proved", "code",
     "family-schema-and-spec",
     lambda: patch(schema56, "bridge_hypotheses", _all_five_proved)),
    ("05's Gap A is reported closed", "code", "family-schema-and-spec",
     lambda: patch(schema56, "two_gaps", _gap_a_closed)),
    ("the p = 3 reasons come back empty, so the count would be typed from "
     "prose", "code", "family-schema-and-spec",
     lambda: patch(schema56, "p3_structural_reasons", _no_p3_reasons)),
    ("07's verdict key fw17_h2 is reported fillable in this tree", "code",
     "family-schema-and-spec",
     lambda: patch(schema56, "SCHEMA_KEYS",
                   tuple((k, True, w) if k == "fw17_h2" else (k, f, w)
                         for k, f, w in schema56.SCHEMA_KEYS))),
    ("the prohibition count merges the two documents numbered 07, losing four",
     "code", "family-schema-and-spec",
     lambda: patch(schema56, "prohibition_count", _prohibitions_merged)),
    ("07's six regression fixtures are scored runnable here", "code",
     "family-schema-and-spec",
     lambda: patch(schema56, "regression_fixtures", _fixtures_runnable)),
    ("00 §6's third guard is reported present with RUN-045's UNKNOWN rows "
     "gone", "code", "consensus-and-experiment",
     lambda: patch(consensus53, "forbidden_substitutions",
                   _hollow_third_guard)),
    ("06's success gate is reported met at four of four", "code",
     "consensus-and-experiment",
     lambda: patch(consensus53, "SUCCESS_GATE",
                   tuple((a, b, "SUPPLIED, VERIFIED HERE")
                         for a, b, _ in consensus53.SUCCESS_GATE))),
    ("00 §5's prime quantifier is reported closed", "code",
     "consensus-and-experiment",
     lambda: patch(consensus53, "the_main_problem", _quantifier_closed)),
    ("06's step 4 warning is reported obeyed by the corpus", "code",
     "consensus-and-experiment",
     lambda: patch(consensus53, "experiment_steps", _step4_obeyed)),
    ("v0.3's two local branches are reported computed in this tree", "code",
     "compiler-targets",
     lambda: patch(targets54, "v03_procedure", _local_branches_computed)),
    ("the base curve is reported carrying an odd additive prime", "code",
     "compiler-targets",
     lambda: patch(targets54, "a_odd", _base_has_odd_additive)),
    ("02's target 3 is scored achieved where its domain is empty", "code",
     "compiler-targets",
     lambda: patch(targets54, "compiler_targets", _target3_achieved)),
    ("the census detector goes back to matching on the filename", "code",
     "compiler-targets",
     lambda: patch(targets54, "discipline_lines", _census_by_filename)),
    ("the census detector stops excluding this gate's own log, which carries "
     "the five status names it searches for", "code", "compiler-targets",
     lambda: patch(targets54, "discipline_lines", _census_matches_itself)),
    ("a_29 comes back +1, so 23's weight-2 sign stops selecting the nonsplit "
     "prime", "code", "source-audits",
     lambda: patch(audits51, "a_at", lambda p: 1)),
    ("maximality is reported certified at 3, where RUN-036 could not", "code",
     "source-audits",
     lambda: patch(audits51, "maximal_versus_irreducible", _maximal_at_3)),
    ("22's cited hypotheses are scored as computed", "code", "source-audits",
     lambda: patch(audits51, "case_hypotheses", _all_hypotheses_computed)),
    ("23's quoted condition is reported absent, so nothing moves", "code",
     "source-audits", lambda: patch(audits51, "what_moves", _nothing_moves)),
    ("26's box is reported as a step this arm can take", "code",
     "novelty-and-routes",
     lambda: patch(routes52, "novelty_rule", _novelty_actionable)),
    ("the classified novelty quotations are unpinned", "code",
     "novelty-and-routes", lambda: patch(routes52, "CLASSIFIED_MENTIONS", ())),
    ("the refusal test goes back to reading unflattened text, so a refusal "
     "broken by a line wrap is invisible", "code", "novelty-and-routes",
     lambda: patch(routes52, "no_round_claims_novelty", _refusals_unflattened)),
    ("refusal words go back to matching as substrings, so \"nothing\" and "
     "\"another\" both count as \"not\"", "code", "novelty-and-routes",
     lambda: patch(routes52, "no_round_claims_novelty", _refusals_by_substring)),
    ("the drill's own check name is left in the prose it scans, so every drill "
     "table counts as a mention", "code", "novelty-and-routes",
     lambda: patch(routes52, "CHECK_NAME", "\x00no such string\x00")),
    ("01's STOP route is reported covered", "code", "novelty-and-routes",
     lambda: patch(routes52, "route_matrix", _stop_covered)),
    ("the two rounds on non-prioritised routes are hidden", "code",
     "novelty-and-routes",
     lambda: patch(routes52, "off_priority_rounds", _no_off_priority)),
    ("18's set definition drops the cubic-irreducibility condition", "code",
     "provisional-vs-revised",
     lambda: patch(prev49, "in_P_per_18", _in_P_without_cubic)),
    ("the router loses its p = q branch, so q goes unrouted", "code",
     "provisional-vs-revised",
     lambda: patch(prev49, "router_partition", _router_without_pq)),
    ("18's open referee items are reported addressed", "code",
     "provisional-vs-revised",
     lambda: patch(prev49, "audit_items", _all_items_addressed)),
    ("the router's witnesses are reported matching without comparing", "code",
     "provisional-vs-revised",
     lambda: patch(prev49, "router_witnesses", _witnesses_unchecked)),
    ("the control curve cannot be found, so the failing side is never shown",
     "code", "candidate-schema",
     lambda: patch(schema50, "find_by_conductor",
                   lambda target, box=0: {"target_conductor": target,
                                          "models_scanned": 0, "found": [],
                                          "count": 0, "first": None})),
    ("the sieve criterion drops the two-reservoir clause", "code",
     "candidate-schema",
     lambda: patch(schema50, "sieve_criterion", _criterion_nonsplit_only)),
    ("additive primes are counted as multiplicative reservoirs", "code",
     "candidate-schema",
     lambda: patch(schema50, "odd_local_structure", _reservoirs_include_additive)),
    ("one of 13's six obligations is reported closed", "code",
     "candidate-schema", lambda: patch(schema50, "obligations", _one_closed)),
    ("Level 2 reports the quantifier compression achieved", "code",
     "fw-compiler", lambda: patch(comp47, "level2", _level2_achieved)),
    ("the H3 rows stop naming which formulation decided them", "code",
     "fw-compiler", lambda: patch(comp47, "h3", _h3_unlabelled)),
    ("H1 is reported PASS beyond the range RUN-036 certified", "code",
     "fw-compiler", lambda: patch(comp47, "h1", _h1_always_pass)),
    ("the certificate emits keys the specification does not have", "code",
     "fw-compiler", lambda: patch(comp47, "level1", _level1_extra_keys)),
    ("the 03-08 equivalence is asserted without exhausting anything", "code",
     "h2-chain",
     lambda: patch(chain48, "equivalence_03_08", _equivalence_asserted)),
    ("10's congruence is called complete at p = 3 as well", "code", "h2-chain",
     lambda: patch(chain48, "ordinary_case_completeness", _complete_at_3)),
    ("the H3 disagreement is reported resolved", "code", "h2-chain",
     lambda: patch(chain48, "the_h3_dispute", _dispute_resolved)),
    ("02's cautionary line is reported absent, so there is no disagreement",
     "code", "h2-chain",
     lambda: patch(chain48, "the_h3_dispute", _dispute_absent)),
    ("the ladder position is reported as C2", "code", "claim-ladder",
     lambda: patch(ladder45, "position", _position_C2)),
    ("H1 is reported as executable here, so C1 reads as complete", "code",
     "claim-ladder",
     lambda: patch(ladder45, "hypothesis_meanings", _h1_executable)),
    ("the forbidden-upgrade audit stops reading the logs", "code",
     "claim-ladder", lambda: patch(ladder45, "_load", lambda name: None)),
    ("the stop rule reports untriggered while its own rounds are not new",
     "code", "claim-ladder",
     lambda: patch(ladder45, "stop_rule", _stop_rule_stale)),
    ("every quadratic field is called a subfield of Q(zeta_24)", "code",
     "chebotarev-audit",
     lambda: patch(cheb46, "inside_cyclotomic", _always_inside)),
    ("the support condition asks for a transposition", "code",
     "chebotarev-audit",
     lambda: patch(cheb46, "the_class_and_density", _class_by_transposition)),
    ("the squarefree part is not extracted", "code", "chebotarev-audit",
     lambda: patch(cheb46, "squarefree", lambda n: n)),
    ("every subgroup is counted as normal", "code", "chebotarev-audit",
     lambda: patch(cheb46, "normal_subgroups", _all_subgroups)),
    ("the P_ram heuristic is reported as exact", "code",
     "finite-exceptional", lambda: patch(fin43, "p_ram", _p_ram_exact)),
    ("the structural vacuity at n = 2 is treated as an unfound witness", "code",
     "finite-exceptional", lambda: patch(fin43, "p_red", _p_red_no_vacuity)),
    ("the bounded local measurement is reported as universal", "code",
     "finite-exceptional", lambda: patch(fin43, "p_loc", _p_loc_universal)),
    ("a supersingular prime is put into P_loc, so the branches overlap", "code",
     "finite-exceptional",
     lambda: patch(fin43, "the_routing_answer", _routing_overlap)),
    ("the cited certificate rows are scored as computed", "code",
     "base-certificate", lambda: patch(cmp44, "compare", _compare_all_computed)),
    ("the discriminant is compared by value instead of square class", "code",
     "base-certificate", lambda: patch(cmp44, "squarefree", _squarefree_identity)),
    ("the document is never read, so the refusal is assumed", "code",
     "base-certificate",
     lambda: patch(cmp44, "DOC", cmp44.DOC.parent / "no_such_file.md")),
    ("the certificate is compared against a different curve", "code",
     "base-certificate", lambda: patch(cmp44, "BASE", [0, 0, 1, -1, 0])),
    ("H1 and H2 are relabelled as computed here", "code", "derived-bridge",
     lambda: patch(brg41, "per_prime", _per_prime_all_computed)),
    ("the safe period condition reports itself closed", "code",
     "derived-bridge",
     lambda: patch(brg41, "safe_period_condition", _period_closed)),
    ("the contrast with 09 is emptied, so 11's range excludes nothing", "code",
     "derived-bridge",
     lambda: patch(brg41, "quantifier_ranges", _quantifier_no_contrast)),
    ("the rank-zero corollary reports the period question closed", "code",
     "derived-bridge",
     lambda: patch(brg41, "rank_zero_corollary", _rank_zero_closed)),
    ("the barrier's p >= 11 floor is raised above the family", "code",
     "odd-additive-barrier", lambda: patch(bar42, "MIN_P", 1000)),
    ("the excluded Kodaira types come back unreachable", "code",
     "odd-additive-barrier",
     lambda: patch(bar42, "the_excluded_types_are_reachable", _no_excluded)),
    ("the even additive prime is counted as an odd one", "code",
     "odd-additive-barrier",
     lambda: patch(bar42, "odd_additive_primes", _additive_including_two)),
    ("the twist valuations are read off the untwisted model", "code",
     "odd-additive-barrier",
     lambda: patch(bar42, "valuations_at", _valuations_of_the_base)),
    ("FW-H3 drops the ell != p clause, so the gap disappears", "code",
     "fw-h3-compiler", lambda: patch(h3c39, "h3", _h3_no_ell_neq_p)),
    ("W_- admits the split multiplicative primes too", "code",
     "fw-h3-compiler", lambda: patch(h3c39, "w_minus", _w_minus_all_mult)),
    ("g_- is reported as 1 whatever the valuations are", "code",
     "fw-h3-compiler", lambda: patch(h3c39, "g_minus", lambda w: 1)),
    ("every gcd is called a power of two, so the premise never refuses", "code",
     "fw-h3-compiler", lambda: patch(h3c39, "is_power_of_two", lambda n: True)),
    ("the H2 criterion tests a_p = 1 and forgets a_p = -1", "code",
     "fw-h2-ordinary", lambda: patch(h2o40, "classify", _classify_plus_only)),
    ("the supersingular set comes back empty", "code", "fw-h2-ordinary",
     lambda: patch(h2o40, "classify", _classify_no_supersingular)),
    ("a bad prime is admitted into the good supersingular branch", "code",
     "fw-h2-ordinary", lambda: patch(h2o40, "classify", _classify_admits_29)),
    ("the ordinary failure set comes back empty, so the routing argument "
     "rests on nothing", "code", "fw-h2-ordinary",
     lambda: patch(h2o40, "classify", _classify_no_failures)),
    ("every prime is reported split, so the inert side never moves", "code",
     "twist-bridge",
     lambda: patch(bridge37, "chi_trivial_at", lambda d, ell: True)),
    ("the local invariants drop the split flag, hiding the one thing that "
     "flips", "code", "twist-bridge",
     lambda: patch(bridge37, "local_invariants", _local_no_split_flag)),
    ("lemma B is reported as established", "code", "twist-bridge",
     lambda: patch(bridge37, "lemma_B_status", _lemma_B_established)),
    ("the twist invariance is measured against the curve itself", "code",
     "twist-bridge", lambda: patch(bridge37, "lemma_A_shadow", _shadow_self)),
    ("every Frobenius is given projective order 6, so S4 is refuted at 3 "
     "where it is the whole group", "code", "mod-ell-surjectivity",
     lambda: patch(surj38, "projective_order", lambda a, lp, ell: 6)),
    ("the nonsplit-Cartan vacuity at 3 is reported refutable", "code",
     "mod-ell-surjectivity", lambda: patch(surj38, "vacuity_at_3", _vac3_false)),
    ("a class with no witness is counted as refuted", "code",
     "mod-ell-surjectivity", lambda: patch(surj38, "certify", _certify_lax)),
    ("the mod-2 verdict stops following from the cubic", "code",
     "mod-ell-surjectivity", lambda: patch(surj38, "ell_two", _ell_two_asserted)),
    ("the gcd of an empty set reports no failures instead of all of them",
     "code", "gcd-witness-lemmas",
     lambda: patch(gcd35, "odd_prime_divisors", lambda n, bound=10_000: [])),
    ("every multiplicative prime is reported split, emptying the nonsplit set",
     "code", "gcd-witness-lemmas",
     lambda: patch(gcd35, "multiplicative_data", _md_all_split)),
    ("the empty-set search is given nothing to search",
     "code", "gcd-witness-lemmas",
     lambda: patch(gcd35, "small_curves", lambda box=0: iter(()))),
    ("the leave-one-out lets a prime be its own witness", "code",
     "gcd-witness-lemmas",
     lambda: patch(gcd35, "leave_one_out", _leave_one_out_self)),
    ("the no-go is decided by the Kodaira symbol, which 05 forbids", "code",
     "kodaira-nogo", lambda: patch(nogo36, "no_go", _no_go_by_symbol)),
    ("every prime is reported potentially good, so nothing ever fires", "code",
     "kodaira-nogo", lambda: patch(nogo36, "local_type", _local_type_pot_good)),
    ("the p = 3 character fact is reported as holding at every prime", "code",
     "kodaira-nogo",
     lambda: patch(nogo36, "character_structure", _chars_flat)),
    ("the twist probe contains only good primes, so the no-go is never "
     "offered a chance to fire", "code", "kodaira-nogo",
     lambda: patch(nogo36, "where_it_fires", _fires_good_probe_only)),
    ("the square test mod n always says yes, so no witness is ever found",
     "code", "mazur-degrees",
     lambda: patch(mazur33.sieve, "is_square_mod", lambda a, n: True)),
    ("the quadratic twist returns the curve unchanged", "code",
     "mazur-degrees",
     lambda: patch(mazur33, "quadratic_twist", lambda ainvs, d: list(ainvs))),
    ("Referee A's q-conditions drop the 2-division-cubic inertness", "code",
     "referee-a-checklist",
     lambda: patch(refA34, "q_checklist", _q_checklist_no_inertness)),
    ("Referee A's cited lines are scored as machine-checkable", "code",
     "referee-a-checklist",
     lambda: patch(refA34, "base_checklist", _base_all_checkable)),
    ("the certificate is built for a different curve", "code",
     "certificate-696e1",
     lambda: patch(cert32, "AINVS", [0, 1, 1, -2, 0])),
    ("the certificate's cited-not-verified list is emptied", "code",
     "certificate-696e1",
     lambda: patch(cert32, "still_cited", lambda: [])),
    ("the Sha row stops saying it is the analytic order", "code",
     "certificate-696e1",
     lambda: patch(cert32, "certificate", _certificate_unlabelled)),

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
    ("106d1 enumerated over 1 ≤ d < 1000 instead of 00's symmetric range — "
     "the same twenty-one, because no negative d is admissible",
     lambda: patch(closure65, "fixtures_00", _fixtures00_positive_only)),
    ("Symbolic 002-004's instances drawn from a different seed",
     lambda: patch(sym84, "RANDOM_SEED", 9)),
    ("Symbolic 002-004's two-variable families truncated at degree 7 instead of 5",
     lambda: patch(sym84, "DEGREE", 7)),
    ("Symbolic 005-007's instances drawn from a different seed",
     lambda: patch(sym85, "RANDOM_SEED", 8)),
    ("PC-001's a_n table taken to 6000 instead of 4000 - the same rationals",
     lambda: patch(pc82, "BOUND", 6000)),
    ("PC-001's discriminants taken to 80 instead of 100 - the same units",
     lambda: patch(pc82, "D_LIMIT", 80)),
    ("PC-002's four-line rescaling drawn from a different seed",
     lambda: patch(pc83, "RESCALING_SEED", 5)),
    ("Symbolic 001's random instances drawn from a different seed",
     lambda: patch(sym81, "RANDOM_SEED", 7)),
    ("Symbolic 001's series truncated at t^12 instead of t^8",
     lambda: patch(sym81, "ORDER", 12)),
    ("Symbolic 001's log_11(12) series taken to 90 terms - the same residues mod 11^12",
     lambda: patch(sym81, "LOG_TERMS", 90)),
    ("Attack 09's log series cut at one term - the same residue mod 121, since u^2/2 is in 121 O",
     lambda: patch(atk79, "LOG_TERMS", 1)),
    ("Attack 09's scale identities drawn from a different seed",
     lambda: patch(atk79, "RANDOM_SEED", 4)),
    ("Attack 10's Dirichlet series summed over 200000 blocks instead of 100000",
     lambda: patch(atk80, "SERIES_BLOCKS", 200_000)),
    ("Attack 10's 11-adic log taken to 25 terms instead of 19 - the same residues mod 11^10",
     lambda: patch(atk80, "LOG_TERMS", 25)),
    ("Attack 09's eigenlines multiplied by the unit 3 - every identity is homogeneous and "
     "the analytic cross-check only asks for one unit per sign",
     lambda: patch(atk78, "SCALE_UNIT", 3)),
    ("Attack 09's twisted L-series cut at e^-55 instead of e^-45",
     lambda: patch(atk78, "TAIL_EXPONENT", 55.0)),
    ("Attack 09's rational recognition allowed denominators to 128 - the values are integers",
     lambda: patch(atk78, "DENOM_BOUND", 128)),
    ("Attack 08's Vieta identity tested at a different random seed",
     lambda: patch(atk77, "VIETA_SEED", 21)),
    ("Attack 03's random c-vectors drawn from a different seed",
     lambda: patch(atk72, "RANDOM_SEED", 11)),
    ("[a/11]+ evaluated at a/11 unreduced instead of (a mod 11)/11 — the same "
     "symbol, since modular symbols are 1-periodic",
     lambda: patch(atk73, "symbol_at_level_p", lambda lam, a: atk73.symbol(lam, a, 11))),
    ("the premise n - v_11(n) >= 2 checked from n = 3 instead of n = 2",
     lambda: patch(atk74, "PREMISE_START", 3)),
    ("the adaptive Simpson tolerance loosened from 1e-15 to 1e-13",
     lambda: patch(atk75, "SIMPSON_EPS", 1e-13)),
    ("the f_0 factorisation tested at a different random seed",
     lambda: patch(atk76, "SEED", 19)),
    ("the Frobenius-witness search bound raised from 300 to 500 — the same "
     "witnesses, found first", lambda: patch(bock71, "SEARCH", 500)),
    ("the 780 relation rows fed to the elimination in reverse order — the same "
     "nullspace, the same normalised eigenline",
     lambda: patch(kur70, "relation_rows", lambda: list(reversed(_true_relations70())))),
    ("389.a1's a-invariants given as a tuple rather than a list",
     lambda: patch(anom69, "AINVS", tuple(anom69.AINVS))),
    ("the cubic identity 16f(x) = F(4x) evaluated at 5, 6, 7 instead of −3..3",
     lambda: patch(mirror68, "cubic_forms_agree",
                   lambda base, xs=(5, 6, 7): _true_cubic_forms68(base, xs))),
    ("04's ten routes listed in reverse order — the 首選 route is the most "
     "worked whichever row it is on",
     lambda: patch(maps67, "ROUTES", tuple(reversed(maps67.ROUTES)))),
    ("the stop-rule window widened from 12 to 24 rounds — no three-round "
     "streak either way", lambda: patch(proto66, "stop_rule_on_this_line",
                                        _stop_rule_window_24)),
    ("the four adversarial curves listed in a different order",
     lambda: patch(corpus64, "FOUR", tuple(reversed(corpus64.FOUR)))),
    ("08's thirteen rows in reverse order",
     lambda: patch(thirteen63, "TABLE_08", tuple(reversed(thirteen63.TABLE_08)))),
    ("11's 3,064,705 denominator perturbed by one — every stated percentage "
     "rounds the same at four decimals",
     lambda: patch(commit61, "ALL_CURVES", 3064706)),
    ("the prime fraction lowered from 0.8 to 0.5 — more lists admitted, the "
     "known join still present", lambda: patch(joins60, "PRIME_FRACTION", 0.5)),
    ("the constants threshold raised from 4 to 100 — nothing was dropped at 4 "
     "either, so nothing changes", lambda: patch(joins60, "NOISE_IF_SEEN_IN", 100)),
    ("the congruence tested one-sided, a_q ≡ 1 instead of a_q² ≡ 1 — same "
     "failing set here, because no member has a_q = −1; a coincidence of the "
     "sample, not a property of the criterion",
     lambda: patch(lemb59, "members", _one_sided_congruence)),
    ("the family bound raised to 5000 — 23 members, and 3529 is still the "
     "only one failing", lambda: patch(lemb59, "members", _wider_family_5000)),
    ("E1 tested by trial-division squarefree instead of N == prod(primes) — "
     "same verdict, because every conductor_primes list is complete",
     lambda: patch(cmap57, "e1_semistable", _e1_by_trial_division)),
    ("the twist-condition sample taken from the tail of the label list "
     "instead of the head", lambda: patch(cmap57, "twist_conditions",
                                          _twist_from_the_tail)),
    ("05's five bridge hypotheses listed in reverse order",
     lambda: patch(schema56, "BRIDGE", tuple(reversed(schema56.BRIDGE)))),
    ("the cyclotomic check run to bound 500 instead of 200 — 95 primes, "
     "not 46", lambda: _wider_cyclotomic_bound()),
    ("06's four success-gate conditions listed in reverse order",
     lambda: patch(consensus53, "SUCCESS_GATE",
                   tuple(reversed(consensus53.SUCCESS_GATE)))),
    ("06 v0.3 and 𝒜_odd run at bound 5000 instead of 4000 — 23 members, "
     "not 19", lambda: _wider_family_bound()),
    ("Mazur's twelve degrees listed in a different order",
     lambda: patch(audits51, "MAZUR",
                   (163, 67, 43, 37, 19, 17, 13, 11, 7, 5, 3, 2))),
    ("the novelty term list extended with a synonym the corpus never uses",
     lambda: patch(routes52, "NOVELTY_TERMS",
                   routes52.NOVELTY_TERMS + ("hitherto unknown",))),
    ("18's (q/29) = 1 condition dropped, which the other two imply — "
     "Frob_q in A_3 is trivial on Q(sqrt -174), and q = 1 mod 24 gives "
     "(-6/q) = 1",
     lambda: patch(prev49, "in_P_per_18", _in_P_without_29)),
    ("the set enumeration bound raised from 4000 to 5000",
     lambda: patch(prev49, "three_definitions",
                   lambda bound=5000: _true_three_defs(5000))),
    ("the control search box widened from 12 to 14, which finds a second "
     "conductor-116 model that fails identically",
     lambda: patch(schema50, "find_by_conductor",
                   lambda target, box=14: _true_find(target, 14))),
    ("the Level-1 bound raised from 200 to 260",
     lambda: patch(comp47, "level1", lambda bound=260: _true_level1(260))),
    ("the character-group exhaustion widened from 40 to 55",
     lambda: patch(chain48, "equivalence_03_08",
                   lambda bound=55: _true_equivalence(55))),
    ("the stop rule's window widened from three rounds to four",
     lambda: patch(ladder45, "stop_rule", _stop_rule_four)),
    ("S3 enumerated in a different order, so the other 3-cycle is picked",
     lambda: patch(cheb46, "s3", lambda: list(reversed(_true_s3())))),
    ("the local bound widened from 1500 to 2000",
     lambda: patch(fin43, "p_loc",
                   lambda bound=2000, blocks=2: _true_p_loc(2000, 2))),
    ("the certificate's L-series truncation raised from 2000 to 3000",
     lambda: patch(cmp44, "compare", lambda limit=3000: _true_compare(3000))),
    ("the supersingular bound widened from 1500 to 2500",
     lambda: patch(brg41, "per_prime",
                   lambda bound=2500: _true_per_prime(2500))),
    ("the excluded-type probe primes given in a different order",
     lambda: patch(bar42, "PROBE_PRIMES", (37, 31, 29, 23, 19, 17, 13, 11))),
    ("the FW-H3 odd-p test bound widened",
     lambda: patch(h3c39, "uniform_certificate",
                   lambda ainvs, bound=800: _true_cert(ainvs, bound))),
    ("the good-prime scan starts at 7, which p = 5 being ordinary with "
     "a_5 = -3 makes a no-op",
     lambda: patch(h2o40, "classify", _classify_from_seven)),
    ("the inert search bound widened",
     lambda: patch(bridge37, "lemma_C_converse",
                   lambda bound=6000: _true_converse(6000))),
    ("the surjectivity witness pool enlarged",
     lambda: patch(surj38, "good_primes", lambda limit=900: _true_good(900))),
    ("the empty-set search box widened",
     lambda: patch(gcd35, "small_curves", lambda box=8: _true_small_curves(8))),
    ("the twist probe given in a different order",
     lambda: patch(nogo36, "where_it_fires",
                   lambda probe=(313, 29, 2, 241, 31, 23, 13, 11, 7, 5, 3):
                   _true_where_it_fires(probe))),
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
    # RUN-033: the redundancy argument holds only for n >= 3. At n = 2 the
    # residue being dropped IS the 1 rather than a duplicate of it, since
    # (n-1)^2 = 1^2 degenerates to 1 = 1, and the set of squares mod 2 loses a
    # member. `mazur-degrees` made that visible the round it arrived, because
    # RUN-031 turned the vacuity at n = 2 into a load-bearing fact. A control
    # whose stated reason is false is not a control, so the reason is corrected
    # rather than the check that caught it weakened.
    ("square-test mod n drops its last residue for n >= 3, which "
     "(n-1)^2 = 1^2 makes redundant there",
     lambda: patch(red7, "is_square_mod",
                   lambda a, n: any((r * r) % n == a % n
                                    for r in range(n if n < 3
                                                   else max(0, n - 1))))),
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


_true_level1 = comp47.level1
_true_level2 = comp47.level2
_true_h1 = comp47.h1
_true_three_defs = prev49.three_definitions
_true_find = schema50.find_by_conductor
_true_fixture65 = closure65.fixture_150
_true_admissible65 = closure65.admissible
_true_checklist65 = closure65.checklist_16
_true_layers65 = closure65.layers_10
_true_fixtures00_65 = closure65.fixtures_00
_true_env66 = proto66.environment_04
_true_stop66 = proto66.stop_rule_on_this_line
_true_regression66 = proto66.regression_05
_true_handoff66 = proto66.handoff_06
_true_unit_root73 = atk73.unit_root
_true_a_prime_power75 = atk75.a_prime_power
_true_bezout76 = atk76.bezout_combination


def _adj_no_signs(B):
    return [[B[1][1], B[0][1]], [B[1][0], B[0][0]]]


def _unit_root_inv3_twice():
    d = dict(_true_unit_root73())
    d["alpha_inv2"] = d["alpha_inv3"]
    return d


def _a_prime_power_no_p(p, k, ap, prev, prev2):
    if p == atk75.N:
        return ap ** k
    return ap * prev


_true_is_square71 = bock71._is_square_mod
_true_ring_mul71 = bock71.ring_mul
_true_local_torsion71 = bock71.local_p_torsion


def _det_plus(m):
    return bock71.ring_add(bock71.ring_mul(m[0][0], m[1][1]), bock71.ring_mul(m[0][1], m[1][0]), 1)


def _ring_mul_I2(u, v):
    out = {}
    for (i, j), a in u.items():
        for (k, l), b in v.items():
            if i + k + j + l <= 1:
                mnm = (i + k, j + l)
                out[mnm] = (out.get(mnm, 0) + a * b) % 11
    return {mnm: c for mnm, c in out.items() if c}


def _local_torsion_inverted(n11):
    d = dict(_true_local_torsion71(n11))
    d["E_Q11_11_is_zero"] = n11 % 11 == 0
    return d


_true_hecke70 = kur70.hecke_rows
_true_path70 = kur70.path_indices
_true_sum70 = kur70.kurihara_sum
_true_relations70 = kur70.relation_rows


def _hecke_transposed(q):
    ms = kur70.merel_matrices(q)
    rows = []
    for i in range(kur70.N + 1):
        c, d = kur70.rep(i)
        r = {}
        for a, b, cc, dd in ms:
            j = kur70.p1_index(a * c + b * d, cc * c + dd * d)
            r[j] = r.get(j, 0) + 1
        rows.append(r)
    return rows


def _path_wrong_sign(a, n):
    out = [kur70.p1_index(1, 0)]
    num, den = a, n
    a0 = num // den
    num -= a0 * den
    p_prev2, q_prev2 = 1, 0
    p_prev, q_prev = a0, 1
    i = 1
    while num:
        k, r = divmod(den, num)
        p_new, q_new = k * p_prev + p_prev2, k * q_prev + q_prev2
        out.append(kur70.p1_index(q_new, (1 if i % 2 == 0 else -1) * q_prev))
        p_prev2, q_prev2, p_prev, q_prev = p_prev, q_prev, p_new, q_new
        den, num = num, r
        i += 1
    return out


def _sum_without_the_skip(lam, blocks=kur70.BLOCKS, block_ids=None):
    n = kur70.ELLS[0] * kur70.ELLS[1]
    logs = {ell: kur70.log_table(ell, kur70.ROOTS[ell]) for ell in kur70.ELLS}
    lo, hi = logs[kur70.ELLS[0]], logs[kur70.ELLS[1]]
    size = (n + blocks - 1) // blocks
    per_block = []
    tot = {"const": 0, "X": 0, "Y": 0, "X2": 0, "Y2": 0, "XY": 0}
    raw = terms = 0
    for b in range(blocks):
        if block_ids is not None and b not in block_ids:
            continue
        s = {k: 0 for k in tot}
        braw = bterms = 0
        for a in range(max(1, b * size), min(n, (b + 1) * size)):
            if a % kur70.ELLS[1] == 0:
                continue                      # only the 991-multiples are skipped
            v = sum(lam[i] for i in kur70.path_indices(a, n)) % 11
            bterms += 1
            if not v:
                continue
            i, j = lo[a % kur70.ELLS[0]], hi[a % kur70.ELLS[1]]
            s["const"] += v
            s["X"] += v * i
            s["Y"] += v * j
            s["X2"] += v * (i * (i - 1) // 2)
            s["Y2"] += v * (j * (j - 1) // 2)
            s["XY"] += v * i * j
            braw += v * i * j
        per_block.append({"block": b, "terms": bterms, "raw_product_sum": braw,
                          "mod_11": {k: val % 11 for k, val in s.items()}})
        for k in s:
            tot[k] += s[k]
        raw += braw
        terms += bterms
    return {"n": n, "blocks": blocks, "terms": terms, "phi_n": (kur70.ELLS[0] - 1) * (kur70.ELLS[1] - 1),
            "theta_bar_mod_I3": {k: v % 11 for k, v in tot.items()},
            "delta_n_XY_coefficient": tot["XY"] % 11, "raw_product_sum": raw, "per_block": per_block}


_true_to_short69 = anom69.to_short
_true_ec_add69 = anom69.ec_add
_true_dlog69 = anom69.dlog
_true_rho69 = anom69.simultaneous_reduction
_true_labels69 = anom69.label_discipline


def _to_short_wrong_b2(a, pt):
    a1, a2, a3, a4, a6 = a
    x, y = pt
    b2 = a1 * a1 + 4 * a2
    return 36 * x + b2, 108 * (2 * y + a1 * x + a3)


def _ec_add_without_A(A, ell, R, S):
    if R is anom69.O:
        return S
    if S is anom69.O:
        return R
    x1, y1 = R
    x2, y2 = S
    if x1 == x2 and (y1 + y2) % ell == 0:
        return anom69.O
    if R == S:
        lam = (3 * x1 * x1) * pow(2 * y1, ell - 2, ell) % ell
    else:
        lam = (y2 - y1) * pow(x2 - x1, ell - 2, ell) % ell
    x3 = (lam * lam - x1 - x2) % ell
    y3 = (lam * (x1 - x3) - y1) % ell
    return (x3, y3)


def _dlog_short(A, ell, base, target, order):
    return _true_dlog69(A, ell, base, target, min(order, order // 11 if order > 11 else order))


def _rho_no_compatibility(d397, d991):
    d = dict(_true_rho69(d397, d991))
    n1, n2 = d397["count"], d991["count"]
    d["image_size"] = n1 * n2 // d["gcd_of_orders"]
    d["surjective"] = d["image_size"] == n1 * n2
    d["J_S_order_of_cokernel"] = n1 * n2 // d["image_size"]
    d["agrees"] = False
    return d


def _labels_count_definition(reports):
    d = dict(_true_labels69(reports))
    d["gate_state_table_closed_exact"] = d["gate_state_table_closed_exact"] + 1
    d["agrees"] = False
    return d


_true_cubic_forms68 = mirror68.cubic_forms_agree
_true_formula68 = mirror68.formula_count
_true_cubic68 = mirror68.cubic_03
_true_crosscheck68 = mirror68.point_count_crosscheck
_true_classify68 = mirror68.classify_added_lines


def _formula_without_the_4(ainvs, p):
    if p == 2:
        raise ValueError("odd p")
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    n = 1
    for x in range(p):
        dx = ((a1 * x + a3) ** 2 + (x ** 3 + a2 * x * x + a4 * x + a6)) % p
        chi = 0 if dx == 0 else (1 if pow(dx, (p - 1) // 2, p) == 1 else -1)
        n += 1 + chi
    return n


def _cubic_with_b4(ainvs):
    c4, b2, two_b4, b6 = _true_cubic68(ainvs)
    return (c4, b2, two_b4 // 2, b6)


def _hasse_too_tight(base, primes=mirror68.ODD_PRIMES, sample=None):
    d = dict(_true_crosscheck68(base, primes, sample))
    rows = base if sample is None else base[::max(1, len(base) // sample)]
    viol = 0
    for r in rows:
        for p in primes:
            if p in r["conductor_primes"]:
                continue
            b = mirror68.brute_count(r["ainvs"], p)
            if (p + 1 - b) ** 2 > p:
                viol += 1
    d["hasse_bound_violations"] = viol
    d["agree"] = d["agree"] and viol == 0
    return d


def _realigned_counted_as_new():
    d = dict(_true_classify68())
    d["added_lines_with_new_content"] = d.get("added_lines_identical_to_a_deleted_line", 0)
    d["added_lines_identical_to_a_deleted_line"] = 0
    d["every_added_line_is_a_comma_drop_or_realignment"] = d["added_lines_with_new_content"] == 0
    return d


_true_rows67 = maps67.CLOSURE_ROWS
_true_seven67 = maps67.SEVEN
_true_routes67 = maps67.ROUTES


def _sha_row_closed():
    return tuple((n, "已關閉", r) if n == "Sha finite in general" else (n, st, r)
                 for n, st, r in _true_rows67)


def _regulator_computed():
    return tuple((c, "computed", ss, w) if c == "regulator on a saturated basis"
                 else (c, st, ss, w) for c, st, ss, w in _true_seven67)


def _red_route_worked():
    return tuple((a, b, ["RUN-003"]) if b == "紅燈" else (a, b, c)
                 for a, b, c in _true_routes67)


def _route_cites_099():
    return tuple((a, b, c + ["RUN-099"]) if b == "首選" else (a, b, c)
                 for a, b, c in _true_routes67)


_true_preflight66 = proto66.preflight_04


def _fixture_reads_13(base, new):
    d = dict(_true_fixture65(base, new))
    d["current"] = 13
    d["agrees"] = False
    return d


def _admissible_without_ordinary(r, d):
    """01's D4 — E ordinary at every p | d — dropped. Some d the map excludes
    become admissible, and completeness reads them as absent."""
    import math as _m
    N, a = r["conductor"], r["ainvs"]
    if not cmap57.squarefree(d) or _m.gcd(abs(d), 3 * N) != 1 or d % 4 != 1:
        return False
    ps = cmap57.prime_factors(d) if abs(d) != 1 else []
    if r["source"] == "Zha16_no_2_tors":
        cubic = cmap57.two_division_cubic(a)
        if any(closure65.ph2.cubic_root_count(cubic, p) != 0 for p in ps):
            return False
        if any(closure65.fam.kronecker(d, q) != 1 for q in r["conductor_primes"]):
            return False
        if r["discriminant"] > 0 and d < 0:
            return False
    else:
        if any(p % 4 != 1 for p in ps):
            return False
        if any(cmap57.point_count(a, p) % 4 != 2 for p in ps):
            return False
        if d % 8 != 1:
            return False
        if any(closure65.fam.kronecker(d, q) != 1 for q in r["conductor_primes"] if q != 2):
            return False
    return True


def _nine_items():
    d = dict(_true_checklist65())
    d["rows"] = d["rows"] + [{"n": 9, "item": "invented", "redone_by": "-", "how": "-"}]
    d["count"] = 9
    return d


def _streak_of_three(window=12):
    d = dict(_true_stop66(window))
    d["longest_only_rerunning_streak"] = 3
    d["freeze_triggered"] = True
    return d


def _all_seven_carried():
    d = dict(_true_regression66())
    d["carried_by_RUN_061s_rows"] = {k: True for k in d["carried_by_RUN_061s_rows"]}
    d["carried_count"] = 7
    d["missing"] = []
    return d


def _fixtures00_positive_only(base, new):
    """106d1 enumerated over 1 ≤ d < 1000 instead of the symmetric range —
    the same twenty-one, because no negative d is admissible."""
    d = dict(_true_fixtures00_65(base, new))
    by = {r["curve_label"]: r for r in base}
    r106 = by["106d1"]
    adm = [x for x in range(1, closure65.TWIST_BOUND) if closure65.admissible(r106, x)]
    d["106d1"] = dict(d["106d1"], range="1 ≤ d < 1000", recomputed=adm,
                      negative_d_admissible=[],
                      agrees=(adm == closure65.FIXTURE_106d1 == new["106d1"]))
    d["both_agree"] = d["46a1"]["agrees"] and d["106d1"]["agrees"]
    return d


def _stop_rule_window_24(window=12):
    return _true_stop66(24)


_true_read_curve64 = corpus64.read_curve
_true_shard_pin64 = corpus64.shard_pin
_true_four64 = corpus64.the_four


def _curves_from_memory(label):
    """The first draft's coefficients for 66b1, 105a1 and 141c1 — wrong — and
    62a1's, right. On the wrong three the root finder finds no 2-torsion."""
    memory = {"62a1": [1, -1, 1, -1, 1], "66b1": [1, 0, 1, -45, 81],
              "105a1": [1, 0, 0, -1, 1], "141c1": [0, 1, 1, -12, 2]}
    return memory.get(label, _true_read_curve64(label))


def _lf_reported_matching():
    d = dict(_true_shard_pin64())
    d["lf_matches_package"] = True
    return d


def _62a1_in_base(base):
    d = dict(_true_four64(base))
    d["rows"] = [dict(r, in_the_40749_base=True) if r["curve"] == "62a1" else r
                 for r in d["rows"]]
    d["none_in_base"] = False
    return d


_true_delta61 = commit61.delta_verifier_12_and_gate_a_14
_true_hist61 = commit61.histogram_11_called_unknown
_true_gate_b61 = commit61.gate_b_14
_true_gate_c61 = commit61.gate_c_14
_true_autopsy61 = commit61.autopsy_07
_true_replay62 = replay62.replay
_true_fixtures62 = replay62.fixtures_09
_true_correction62 = replay62.correction_to_RUN_055
_true_first_failure63 = thirteen63.first_failure_from_census
_true_table63 = thirteen63.table_08
_true_soundness63 = thirteen63.soundness_03
_true_fixture63 = thirteen63.fixture_versus_500k


def _delta_forgets_a3(base, removed, new_map):
    d = dict(_true_delta61(base, removed, new_map))
    iso = {r["curve_label"] for r in removed
           if r["isogeny_set_357"] not in ("", "NONE")}
    labels = {r["curve_label"] for r in base}
    pred = labels - iso
    d["removed_by_columns"] = len(iso)
    d["predicted_current"] = len(pred)
    d["sets_equal"] = pred == set(new_map)
    return d


def _warning_unjustified(removed):
    d = dict(_true_hist61(removed))
    d["the_warning_was_justified"] = False
    return d


def _gate_b_added_one(base, removed, new_map):
    d = dict(_true_gate_b61(base, removed, new_map))
    d["5_twists_added_after_deleting_old_disc_gate"] = 1
    return d


def _a3_filter_unlocated():
    d = dict(_true_autopsy61())
    d["RUN_056_located_a3_filter_in_diff"] = False
    return d


def _disc_forall(primes_dividing_M, conductor_primes, disc_valuations):
    """∀q instead of ∃q — every conductor prime must witness."""
    return all(all(disc_valuations[q] % p != 0 for q in conductor_primes if q != p)
               for p in primes_dividing_M)


def _replay_drops_one(base, old, new):
    d = dict(_true_replay62(base, old, new))
    d["T_O"] = d["T_O"] - 1
    return d


def _case_b_passes():
    d = dict(_true_fixtures62())
    d["case_B"] = dict(d["case_B"], old_rejects=False, D_passes=True)
    d["both_branches_exercised"] = False
    return d


def _a3_first(row):
    if row["abs_a3_eq_3"] == "True":
        return "A3_ABS_3"
    return _true_first_failure63(row)


def _26b1_not_both(removed):
    d = dict(_true_table63(removed))
    d["26b1_is_the_BOTH_class"] = False
    return d


def _timestamp_present(meta):
    d = dict(_true_soundness63(meta))
    d["s6_present"] = dict(d["s6_present"], timestamp=True)
    d["s6_count"] = 7
    d["s6_missing"] = []
    return d


def _sum_drops_both(removed):
    d = dict(_true_fixture63(removed))
    d["sum"] = d["sum"] - 2
    return d


_true_prime_sets60 = joins60.prime_sets
_true_joins60 = joins60.joins


def _sets_without_src40():
    return [x for x in _true_prime_sets60() if not x["log"].startswith("src40")]


def _joins_inverted_containment(sets):
    """Keep only pairs where one set contains the other — the re-reads — and
    drop the genuine joins."""
    import itertools as _it
    out = []
    for a, b in _it.combinations(sets, 2):
        if a["log"] == b["log"]:
            continue
        inter = sorted(set(a["set"]) & set(b["set"]))
        if not inter:
            continue
        if not (set(a["set"]) <= set(b["set"]) or set(b["set"]) <= set(a["set"])):
            continue
        out.append({"a": f"{a['log']} :: {a['path']}",
                    "b": f"{b['log']} :: {b['path']}",
                    "size_a": a["size"], "size_b": b["size"],
                    "intersection": inter[:40], "size": len(inter)})
    return out


_true_members59 = lemb59.members
_true_pieces59 = lemb59.the_pieces_were_in_the_tree
_true_design59 = lemb59.which_design_it_breaks
_true_profile59 = lemb59.the_profile


def _members_inverted_ordinary(bound=None, brute_at=()):
    d = dict(_true_members59(bound, brute_at) if bound is not None
             else _true_members59(brute_at=brute_at))
    rows = [dict(r, ordinary=not r["ordinary"], FW_H2_at_q="PASS")
            for r in d["rows"]]
    d["rows"] = rows
    d["all_ordinary"] = all(r["ordinary"] for r in rows)
    d["failing_members"] = []
    d["failing"] = 0
    d["passing"] = len(rows)
    return d


def _members_without_3529(bound=None, brute_at=()):
    d = dict(_true_members59(bound, brute_at) if bound is not None
             else _true_members59(brute_at=brute_at))
    rows = [r for r in d["rows"] if r["q"] != 3529]
    d["rows"] = rows
    d["members"] = len(rows)
    d["failing_members"] = [r["q"] for r in rows if r["FW_H2_at_q"] == "FAIL"]
    d["failing"] = len(d["failing_members"])
    d["passing"] = len(rows) - d["failing"]
    return d


def _flat_key_read():
    d = dict(_true_pieces59())
    d["RUN_038_listed_3529_as_an_a_p2_eq_1_failure"] = False
    d["RUN_038_failures_below_its_bound"] = []
    return d


def _revised_uses_fw():
    d = dict(_true_design59())
    d["revised_design"] = dict(d["revised_design"], applies_FW_at_p_equals_q=True)
    return d


def _profile_borrowed():
    d = dict(_true_profile59())
    d["profile"] = "FW17_EXACT"
    d["is_07s_FW17_EXACT"] = True
    return d


def _one_sided_congruence(bound=None, brute_at=()):
    """a_q ≡ 1 in place of a_q² ≡ 1. On these members no a_q is −1, so the
    one-sided test returns the same failing set — a coincidence of the sample,
    not a property of the criterion, and recorded as such."""
    d = dict(_true_members59(bound, brute_at) if bound is not None
             else _true_members59(brute_at=brute_at))
    rows = []
    for r in d["rows"]:
        cong = (r["a_q"] - 1) % r["q"] == 0
        fails = r["good"] and r["ordinary"] and cong
        rows.append(dict(r, a_q_squared_is_1_mod_q=cong,
                         FW_H2_at_q="FAIL" if fails else "PASS"))
    d["rows"] = rows
    d["failing_members"] = [r["q"] for r in rows if r["FW_H2_at_q"] == "FAIL"]
    d["failing"] = len(d["failing_members"])
    d["passing"] = len(rows) - d["failing"]
    return d


def _wider_family_5000(bound=None, brute_at=()):
    return _true_members59(5000, brute_at)


_true_e2_57 = cmap57.e2_small_trace
_true_e4_57 = cmap57.e4_ramification
_true_e1_57 = cmap57.e1_semistable
_true_twist_57 = cmap57.twist_conditions
_true_and_sem58 = prov58.and_semantics
_true_pins58 = prov58.pins_02_demands


def _e2_by_count(base, removed):
    """agree_exactly computed from the two counts, with one curve swapped out
    of each side — the count still says 2,709 = 2,709."""
    d = dict(_true_e2_57(base, removed))
    d["only_mine"] = ["swapped-in"]
    d["only_census"] = ["swapped-out"]
    d["agree_exactly"] = d["abs_a3_eq_3_recomputed"] == d["abs_a3_eq_3_in_census"]
    return d


def _e4_for_all(base):
    """E4 with ∀q in place of ∃q: every other conductor prime must witness."""
    fails = []
    for r in base:
        ps = r["conductor_primes"]
        vals = {int(k): v for k, v in r["discriminant_valuations"].items()}
        for p in ps:
            others = [q for q in ps if q != p]
            if not others or not all(vals[q] % p != 0 for q in others):
                fails.append(r["curve_label"])
                break
    d = dict(_true_e4_57(base))
    d["fail"] = len(fails)
    d["pass"] = len(base) - len(fails)
    d["all_pass"] = not fails
    return d


def _float_roots_of_monic_cubic(c2, c1, c0):
    """The first draft: a 4,000-step float scan on [-B, B] for the Cauchy bound
    B, bisection on each sign change, round, then exact check. At B ~ 1e11 the
    scan's step is ~5e7 and clustered roots sit inside one step."""
    def gval(x):
        return ((x + c2) * x + c1) * x + c0
    B = 1 + max(abs(c2), abs(c1), abs(c0))
    cands = set()
    steps = 4000
    lo, hi = -float(B), float(B)
    prev_x, prev_v = lo, gval(lo)
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        v = gval(x)
        if v == 0:
            cands.add(round(x))
        elif prev_v * v < 0:
            a, b = prev_x, x
            fa = prev_v
            for _ in range(80):
                m = (a + b) / 2
                fm = gval(m)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            cands.add(round((a + b) / 2))
        prev_x, prev_v = x, v
    return sorted(X for X in cands if ((X + c2) * X + c1) * X + c0 == 0)


def _twist_inconsistent(base, new_map, limit=None):
    d = dict(_true_twist_57(base, new_map, limit))
    d["failures_by_condition"] = {"D3_d_1_mod_4": 1}
    d["all_pass"] = True
    return d


def _relaxed_as_strict(row):
    return (row["has_isogeny_3"] == "True" or row["has_isogeny_5"] == "True"
            or row["has_isogeny_7"] == "True")


def _and_as_intersection(base):
    d = dict(_true_and_sem58(base))
    d["with_bad_primes_{2,7}"] = [7]
    d["so_on_every_base_curve_it_is"] = "bad_primes ∩ {3,5,7}"
    return d


def _paper_version_present():
    d = dict(_true_pins58())
    d["pins"] = [dict(p, state="PRESENT") if p["pin"] == "paper version" else p
                 for p in d["pins"]]
    d["present"] = 2
    d["absent"] = 0
    return d


def _rank_column_present():
    d = dict(_true_pins58())
    d["section_7_rank_fields_in_base_record"] = ["rank"]
    d["section_7_count"] = "1 of 4"
    return d


def _e1_by_trial_division(base):
    """Squarefree by trial division instead of N == prod(conductor_primes).
    The same verdict on this base, because every conductor_primes list is the
    complete factorisation — which the product identity is what certifies."""
    d = dict(_true_e1_57(base))
    fails = [r["curve_label"] for r in base if not cmap57.squarefree(r["conductor"])]
    d["non_squarefree_conductor"] = len(fails)
    d["all_pass"] = not fails and d["valuation_keys_not_the_conductor_primes"] == 0
    return d


def _twist_from_the_tail(base, new_map, limit=None):
    """The sample taken from the END of the label list instead of the start.
    Every one of the 247,391 pairs passes, so where the sample sits cannot
    change the verdict — and if it did, the full-run zero would be suspect."""
    if limit is None:
        return _true_twist_57(base, new_map, None)
    labels = sorted(new_map)[-limit:]
    sub = {k: new_map[k] for k in labels}
    return _true_twist_57(base, sub, None)


_true_cyclo_order = kern55.cyclotomic_order
_true_mutual55 = kern55.mutual_exclusivity
_true_precond55 = kern55.precondition_local_reducibility
_true_bridge56 = schema56.bridge_hypotheses
_true_gaps56 = schema56.two_gaps
_true_p3_56 = schema56.p3_structural_reasons
_true_prohib56 = schema56.prohibition_count
_true_fixtures56 = schema56.regression_fixtures


def _divisibility_backwards(bound=None):
    """`(p - 1) % 2 == 0 and (p - 1) <= 2` instead of `2 % (p - 1) == 0`.

    The real first draft. It is "2 divides p - 1", not "p - 1 divides 2", and
    it disagrees with the brute-force column at exactly p = 2 — where p - 1 = 1
    divides 2 and 2 does not divide 1."""
    d = dict(_true_cyclo_order() if bound is None else _true_cyclo_order(bound))
    rows = [dict(r, p_minus_1_divides_2=((r["p"] - 1) % 2 == 0
                                         and (r["p"] - 1) <= 2))
            for r in d["rows"]]
    d["rows"] = rows
    d["agrees_with_the_divisibility"] = all(
        r["omega_squared_trivial"] == r["p_minus_1_divides_2"] for r in rows)
    return d


def _exclusive_everywhere(bound=None):
    d = dict(_true_mutual55() if bound is None else _true_mutual55(bound))
    d["both_tests_can_fire_at"] = []
    return d


def _local_settled():
    d = dict(_true_precond55())
    d["decided_here"] = True
    d["global_surjectivity_does_not_settle_this"] = False
    return d


def _all_five_proved():
    d = dict(_true_bridge56())
    d["all_five_proved"] = True
    d["reachable_here"] = True
    return d


def _gap_a_closed():
    d = dict(_true_gaps56())
    d["gap_A"] = dict(d["gap_A"], still_open=False)
    d["both_open"] = False
    return d


def _no_p3_reasons():
    return {"rows": [], "count": 0, "distinct_rounds": [],
            "counted_from": "nothing"}


def _prohibitions_merged():
    """The two documents numbered `07` merged into one row — which is how a
    count keyed on the number rather than the name loses four prohibitions."""
    d = dict(_true_prohib56())
    d["lists"] = [x for x in d["lists"]
                  if x["document"] != "07_Local_Agent_Implementation_Spec"]
    d["documents"] = len(d["lists"])
    d["total"] = sum(x["count"] for x in d["lists"])
    return d


def _fixtures_runnable():
    d = dict(_true_fixtures56())
    d["runnable_here"] = d["count"]
    d["rows"] = [dict(r, runnable_here=True) for r in d["rows"]]
    return d


def _wider_cyclotomic_bound():
    """500 instead of 200 — 95 primes instead of 46. `omega^2 = 1` at exactly
    {2, 3} is a statement about every prime, so a bound that moved it would
    mean the finding was an artefact of where the check stopped."""
    r1 = patch(kern55, "cyclotomic_order",
               lambda bound=500: _true_cyclo_order(bound))
    r2 = patch(kern55, "mutual_exclusivity",
               lambda bound=500: _true_mutual55(bound))
    return lambda: (r1(), r2())


_true_fs53 = consensus53.forbidden_substitutions
_true_main_problem53 = consensus53.the_main_problem
_true_experiment_steps53 = consensus53.experiment_steps
_true_v03_procedure = targets54.v03_procedure
_true_a_odd54 = targets54.a_odd
_true_compiler_targets54 = targets54.compiler_targets
_true_discipline_lines54 = targets54.discipline_lines


def _hollow_third_guard():
    """The guard still reported present, with the rows that ARE the guard
    gone — `00` §6's third prohibition is about RUN-036's certificate, and what
    answers it is RUN-045 emitting UNKNOWN rather than extrapolating."""
    d = dict(_true_fs53())
    d["primes_marked_UNKNOWN_by_RUN_045"] = 0
    return d


def _quantifier_closed():
    d = dict(_true_main_problem53())
    d["for_all_p_FW"] = dict(d["for_all_p_FW"], quantifier_closed=True)
    return d


def _step4_obeyed():
    d = dict(_true_experiment_steps53())
    d["step_4_was_violated_in_the_corpus"] = False
    return d


def _local_branches_computed(bound=None):
    """The two branches v0.3 turns on, reported decided here — which would be
    this tree claiming local Galois data it does not compute."""
    d = dict(_true_v03_procedure() if bound is None
             else _true_v03_procedure(bound))
    d["rows"] = [{**r,
                  "LOCAL_H2": {**r["LOCAL_H2"],
                               "branch_2_local_irreducible_over_Fp": "PASS",
                               "branch_3_local_isogeny_kernel_test": "PASS",
                               "verdict": "PASS"},
                  "FINAL": "PASS"} for r in d["rows"]]
    d["steps_decided_here"] = 4
    d["steps_partial"] = 1
    d["steps_outside"] = 0
    return d


def _base_has_odd_additive(bound=None):
    d = dict(_true_a_odd54() if bound is None else _true_a_odd54(bound))
    d["base_A_odd"] = [29]
    d["base_size"] = 1
    return d


def _target3_achieved():
    d = dict(_true_compiler_targets54())
    d["g_mult_odd"] = 3
    d["odd_divisors_of_g_mult"] = [3]
    d["target_3_domain_is_empty"] = False
    return d


def _census_by_filename():
    """The bug this gate carried when it was first written: scan the log
    filenames for the word, and src19's CONDUCTOR census answers to it."""
    d = dict(_true_discipline_lines54())
    d["logs_carrying_that_census"] = sorted(
        f.name for f in targets54.LOGS.glob("*census*.json"))
    return d


def _census_matches_itself():
    """The defect the fixed detector exists to prevent: a check that writes its
    own search terms into the directory it searches matches itself on every run
    after the first, and its first run is green only because its log is not
    there yet."""
    d = dict(_true_discipline_lines54())
    d["logs_carrying_that_census"] = [targets54.OUT.name]
    return d


def _wider_family_bound():
    """5000 instead of 4000 — 23 members instead of 19. Every property the
    check reads is universal over members, so a bound that moved a verdict
    would mean the finding was an artefact of where the search stopped."""
    r1 = patch(targets54, "v03_procedure",
               lambda bound=5000: _true_v03_procedure(bound))
    r2 = patch(targets54, "a_odd", lambda bound=5000: _true_a_odd54(bound))
    return lambda: (r1(), r2())


_true_maximal_vs_irr = audits51.maximal_versus_irreducible
_true_case_hypotheses = audits51.case_hypotheses
_true_what_moves = audits51.what_moves
_true_novelty_rule = routes52.novelty_rule
_true_route_matrix = routes52.route_matrix
_true_off_priority = routes52.off_priority_rounds


def _maximal_at_3():
    d = dict(_true_maximal_vs_irr())
    d["maximality_NOT_certified_at_3"] = False
    d["maximality_certified_at"] = sorted(
        set(d["maximality_certified_at"]) | {3})
    return d


def _all_hypotheses_computed():
    """Every hypothesis scored computed, citations included — which is the
    distinction `22` itself keeps and RUN-032 had to make for Referee A."""
    d = dict(_true_case_hypotheses())
    d["rows"] = [{**r, "hypotheses": [{**h, "verdict": "computed"}
                                      for h in r["hypotheses"]]}
                 for r in d["rows"]]
    d["verdict_counts"] = {"computed": d["total_hypotheses"]}
    return d


def _nothing_moves():
    d = dict(_true_what_moves())
    d["RUN_046"] = dict(d["RUN_046"], the_quote_is_present=False)
    return d


SENTENCE_SPLIT = "(?<=[.!?])" + chr(92) + "s+|" + chr(10) + chr(10)


def _refusals_by_substring():
    """The scan before RUN-051's second repair: refusal words matched as bare
    substrings, and the check's own identifier left in the prose. Under it
    `nothing` and `another` both count as the refusal word `not`, three
    sentences read as refusals that refused nothing, and the count of that
    accident is not measured at all — which is what this check now asserts."""
    import re
    rows = []
    for f in sorted(routes52.REPORTS.glob("RUN-*.md")):
        text = f.read_text(encoding="utf-8")
        for sent in re.split(SENTENCE_SPLIT, text):
            flat = " ".join(sent.split())
            low = flat.lower()
            if any(t in low for t in routes52.NOVELTY_TERMS):
                refused = any(w in low for w in routes52.REFUSAL_WORDS)
                cls = next((c for c in routes52.CLASSIFIED_MENTIONS
                            if c[0] in f.name and c[1] in flat), None)
                rows.append({"report": f.name, "refused": refused,
                             "classified_as_descriptive": bool(cls),
                             "why_not_a_claim": cls[2] if cls else None,
                             "sentence": flat[:150]})
    un = [r for r in rows
          if not r["refused"] and not r["classified_as_descriptive"]]
    return {"reports_scanned": len(list(routes52.REPORTS.glob("RUN-*.md"))),
            "mentions": len(rows),
            "refusals": sum(r["refused"] for r in rows),
            "classified_descriptive": sum(r["classified_as_descriptive"]
                                          for r in rows),
            "unaccounted": un, "no_unaccounted_mention": not un,
            "rows": rows[:12], "why_scanned_this_way": "substring"}


def _refusals_unflattened():
    """The scan as it was before RUN-051: the pinning test on flattened text,
    the refusal test on the raw sentence. The reports are hard-wrapped, so a
    refusal phrase landing across a line break becomes invisible and one of
    this line's own refusals reads as an unaccounted mention."""
    import re
    rows = []
    for f in sorted(routes52.REPORTS.glob("RUN-*.md")):
        text = f.read_text(encoding="utf-8")
        for sent in re.split(SENTENCE_SPLIT, text):
            low = sent.lower()
            if any(t in low for t in routes52.NOVELTY_TERMS):
                refused = any(w in low for w in routes52.REFUSAL_WORDS)
                flat = " ".join(sent.split())
                cls = next((c for c in routes52.CLASSIFIED_MENTIONS
                            if c[0] in f.name and c[1] in flat), None)
                rows.append({"report": f.name, "refused": refused,
                             "classified_as_descriptive": bool(cls),
                             "why_not_a_claim": cls[2] if cls else None,
                             "sentence": flat[:150]})
    un = [r for r in rows
          if not r["refused"] and not r["classified_as_descriptive"]]
    return {"reports_scanned": len(list(routes52.REPORTS.glob("RUN-*.md"))),
            "mentions": len(rows),
            "refusals": sum(r["refused"] for r in rows),
            "classified_descriptive": sum(r["classified_as_descriptive"]
                                          for r in rows),
            "unaccounted": un, "no_unaccounted_mention": not un,
            "rows": rows[:12], "why_scanned_this_way": "unflattened"}


def _novelty_actionable():
    d = dict(_true_novelty_rule())
    d["steps_this_arm_can_do"] = [d["remaining_steps"][0]]
    return d


def _stop_covered():
    d = dict(_true_route_matrix())
    d["stop_route_untouched"] = False
    return d


def _no_off_priority():
    return {"rows": [], "count": 0, "reading": "hidden"}


_true_in_P_per_18 = prev49.in_P_per_18
_true_router_partition = prev49.router_partition
_true_audit_items = prev49.audit_items
_true_router_witnesses = prev49.router_witnesses
_true_sieve_criterion = schema50.sieve_criterion
_true_odd_local = schema50.odd_local_structure
_true_obligations = schema50.obligations


def _in_P_without_cubic(q):
    """Membership without the irreducibility condition. That one is NOT implied
    by the others, so the set grows and the three definitions part company."""
    d = dict(_true_in_P_per_18(q))
    d["in_P"] = (q % 24 == 1 and q != 29
                 and prev49.ph2.legendre(q, 29) == 1)
    return d


def _in_P_without_29(q):
    """Membership without the (q/29) = 1 condition. RUN-047 measured this to be
    a GENUINE no-op: q inert in the cubic puts Frob_q in A_3, hence trivial on
    the resolvent Q(sqrt -174), and q = 1 (mod 24) gives (-6/q) = 1, so
    (29/q) = 1 follows. It lives in the controls with that reason, not among the
    defects."""
    d = dict(_true_in_P_per_18(q))
    a, b, c = prev49.CUBIC[1:]
    has_root = any((x ** 3 + a * x * x + b * x + c) % q == 0
                   for x in range(q))
    d["in_P"] = (q % 24 == 1 and q != 29 and not has_root)
    return d


def _router_without_pq(q, bound=prev49.BRANCH_BOUND):
    """The p = q branch removed. q is additive for its own twist, so it lands
    in no branch at all."""
    d = dict(_true_router_partition(q, bound))
    d["unrouted"] = [q]
    d["every_prime_has_exactly_one_branch"] = False
    return d


def _all_items_addressed():
    d = dict(_true_audit_items())
    d["counts"] = {"addressed": 5, "deferred": 0, "open": 0}
    return d


def _witnesses_unchecked():
    """Agreement asserted while the computed swap is wrong."""
    d = dict(_true_router_witnesses())
    d["this_tree_computed"] = {"leave_one_out": {3: 3, 29: 29}, "W_minus": []}
    d["leave_one_out_matches"] = False
    d["agree"] = True
    return d


def _criterion_nonsplit_only(ainvs):
    """`14`'s criterion reduced to 'has a nonsplit prime', which is exactly the
    reading the control was built to refute."""
    d = dict(_true_sieve_criterion(ainvs))
    if d.get("singular"):
        return d
    d["boxed_criterion_met"] = d["at_least_one_nonsplit"]
    return d


def _reservoirs_include_additive(ainvs):
    """Additive primes counted as reservoirs, which gives the control a second
    one it does not have."""
    md = gcd35.multiplicative_data(ainvs)
    if md.get("singular"):
        return {"singular": True}
    d = dict(_true_odd_local(ainvs))
    extra = [r["p"] for r in md["additive"]]
    d["W_mult_odd"] = sorted(set(d["W_mult_odd"]) | set(extra))
    d["valuations"] = dict(d["valuations"])
    for r in md["additive"]:
        d["valuations"][str(r["p"])] = r["v_disc"]
    return d


def _one_closed():
    d = dict(_true_obligations())
    d["rows"] = [dict(r) for r in d["rows"]]
    d["rows"][0]["status"] = "CLOSED"
    d["none_are_closed"] = False
    return d


_true_comp47_h3 = comp47.h3
_true_equivalence = chain48.equivalence_03_08
_true_ordinary_complete = chain48.ordinary_case_completeness
_true_dispute = chain48.the_h3_dispute


def _level2_achieved():
    d = dict(_true_level2())
    d["achieved"] = True
    d["this_gate_outputs"] = "P_E finite"
    return d


def _h3_unlabelled(p, w):
    """The verdict kept, the formulation dropped — which is exactly the shape
    RUN-037 and RUN-039 shipped before RUN-045 named it."""
    d = dict(_true_comp47_h3(p, w))
    d.pop("formulation", None)
    d.pop("gap_to_the_exact_condition", None)
    return d


def _h1_always_pass(p, certified):
    return {"verdict": "PASS", "basis": "computed_here",
            "how": "asserted beyond the certified range"}


def _level1_extra_keys(bound=comp47.P_BOUND):
    d = dict(_true_level1(bound))
    d["rows"] = [dict(r, confidence=0.99) for r in d["rows"]]
    d["keys_match_the_specification"] = all(
        tuple(r) == comp47.LEVEL1_KEYS for r in d["rows"])
    return d


def _equivalence_asserted(bound=chain48.ORDER_BOUND):
    """Equivalence claimed with nothing exhausted."""
    return {"character_group_orders_exhausted": 0, "pairs_checked": 0,
            "mismatches": 0, "equivalent": True, "counterexamples": [],
            "shared_input": "asserted", "why_exhaustive": "not exhausted"}


def _complete_at_3(primes=chain48.RAMIFICATION_PRIMES):
    d = dict(_true_ordinary_complete(primes))
    d["primes_where_the_second_case_survives"] = [2]
    d["the_exception_is_3"] = False
    return d


def _dispute_resolved():
    d = dict(_true_dispute())
    d["this_gate_does_not_resolve_it"] = False
    return d


def _dispute_absent():
    d = dict(_true_dispute())
    d["02_line_present"] = False
    d["the_disagreement_is_real"] = False
    return d


_true_s3 = cheb46.s3


def _stop_rule_four(window=4):
    """The same rule over four rounds instead of three. All four compiled a new
    corpus document, so the verdict cannot move."""
    return _true_stop_rule(4)


_true_position = ladder45.position
_true_meanings = ladder45.hypothesis_meanings
_true_stop_rule = ladder45.stop_rule
_true_class_density = cheb46.the_class_and_density


def _position_C2():
    """The rung claimed one higher than anything computed supports."""
    d = _true_position()
    d["C2"] = dict(d["C2"], reached=True)
    d["honest_rung"] = "C2"
    return d


def _h1_executable():
    """H1 relabelled executable, which makes C1 read as complete while nothing
    in the tree computes the niveau-2 argument."""
    d = _true_meanings()
    d["rows"] = [dict(r, executable_here=True) if r["hypothesis"] == "H1" else r
                 for r in d["rows"]]
    d["executable"] = [r["hypothesis"] for r in d["rows"]]
    d["cited"] = []
    d["C1_reached"] = True
    return d


def _stop_rule_stale(window=3):
    """The verdict kept while the evidence for it is removed."""
    d = _true_stop_rule(window)
    d["last_three"] = [dict(r, is_new=False) for r in d["last_three"]]
    d["each_of_the_last_three_compiled_a_new_document"] = False
    d["rule_triggered"] = False
    return d


def _always_inside(m, n):
    """Every quadratic field declared a subfield of the cyclotomic one, which
    collapses [K:Q] from 16 to 8 because sqrt 29 stops needing adjoining."""
    d = cheb46.quadratic_discriminant(m)
    return {"m": m, "discriminant": d, "abs": abs(d), "n": n,
            "divides": True, "inside": True}


def _class_by_transposition():
    """The support condition read as a transposition instead of a 3-cycle: sign
    -1, nontrivial on F_0, incompatible with the identity on K."""
    d = dict(_true_class_density())
    d["compatible"] = False
    d["transposition_acts_trivially_on_F0"] = True
    d["class_size"] = 3
    d["delta"] = "1/16"
    d["delta_is_one_over_24"] = False
    return d


def _all_subgroups(group):
    """Every subgroup counted, normal or not. S_3's three order-2 subgroups are
    not normal, so the 'unique nontrivial proper' step stops holding."""
    import itertools as _it
    out = []
    ident = tuple(range(3))
    for r in range(1, len(group) + 1):
        for sub in _it.combinations(group, r):
            ss = set(sub)
            if ident not in ss:
                continue
            if all(cheb46.compose(a, b) in ss for a in ss for b in ss):
                out.append(sorted(ss))
    return out


_true_p_ram = fin43.p_ram
_true_p_red = fin43.p_red
_true_p_loc = fin43.p_loc
_true_routing = fin43.the_routing_answer
_true_compare = cmp44.compare
_true_cmp44_squarefree = cmp44.squarefree


def _p_ram_exact():
    """The heuristic promoted to a theorem: the formula's empty set reported as
    the whole obstruction, which is what `04` warns against."""
    d = dict(_true_p_ram())
    d["formula_misses"] = []
    d["the_warning_was_exact"] = False
    d["criterion_actually_obstructed_at"] = []
    return d


def _p_red_no_vacuity():
    """n = 2 reported as an unfound witness rather than a structural vacuity, so
    P_red comes back non-empty for a reason that is not arithmetic."""
    d = dict(_true_p_red())
    d["rows"] = [dict(r, refuted=False) if r["n"] == 2 else r
                 for r in d["rows"]]
    d["set"] = [r["n"] for r in d["rows"] if not r["refuted"]]
    d["is_empty"] = not d["set"]
    return d


def _p_loc_universal(bound=1500, blocks=2):
    """A bounded measurement claimed for every prime — exactly the substitution
    `04` §5 forbids."""
    d = dict(_true_p_loc(bound, blocks))
    d["claim_is_universal"] = True
    return d


def _routing_overlap(bound=1500):
    d = dict(_true_routing(bound))
    d["intersection"] = [23]
    d["P_loc_is_disjoint_from_the_FW_branch"] = False
    return d


def _compare_all_computed(limit=cmp44.TERMS):
    """Every row scored as a computation, citations included."""
    rows = [dict(r, kind="computed", agree=True) for r in _true_compare(limit)]
    return rows


def _squarefree_identity(n):
    """No square part extracted, so the resolvent row compares raw
    discriminants and two correct models look like a disagreement."""
    return (n, 1)


_true_per_prime = brg41.per_prime
_true_quantifier = brg41.quantifier_ranges
_true_rank_zero = brg41.rank_zero_corollary
_true_period_cond = brg41.safe_period_condition
_true_excluded = bar42.the_excluded_types_are_reachable
_true_odd_additive = bar42.odd_additive_primes
_true_valuations_at = bar42.valuations_at


def _per_prime_all_computed(bound=brg41.SS_BOUND):
    """H1 and H2 given the same provenance as H3. The bridge then reports one
    verdict over supports of two different kinds."""
    d = _true_per_prime(bound)
    for r in d["rows"]:
        r["H1"] = dict(r["H1"], source="computed here")
        r["H2"] = dict(r["H2"], source="computed here")
    d["computed_versus_cited"] = "all computed"
    return d


def _period_closed():
    d = dict(_true_period_cond())
    d["computed_in_this_tree"] = True
    d["status"] = "closed"
    return d


def _quantifier_no_contrast(bound=brg41.SS_BOUND):
    """09's failing set emptied. 11's range then excludes nothing, and the
    disjointness is a statement about an empty set."""
    d = dict(_true_quantifier(bound))
    d["the_09_failing_set"] = []
    d["every_09_failure_is_outside_11s_range"] = True
    return d


def _rank_zero_closed(limit=brg41.TERMS):
    d = dict(_true_rank_zero(limit))
    d["closed_here"] = True
    return d


def _no_excluded():
    d = dict(_true_excluded())
    d["excluded_types_found"] = []
    d["examples"] = {}
    d["all_three_reachable"] = False
    d["at_least_one_reachable"] = False
    d["and_the_condition_fails_there"] = True   # vacuously, over nothing
    return d


def _additive_including_two(ainvs):
    md = gcd35.multiplicative_data(ainvs)
    if md.get("singular"):
        return []
    return [r["p"] for r in md["additive"]]


def _valuations_of_the_base(ainvs, p):
    """The valuations taken from the untwisted curve, where p is a GOOD prime
    and every valuation is 0 — so the (2, 3, 6) forcing cannot be seen."""
    return _true_valuations_at(bar42.BASE, p)


_true_cert = h3c39.uniform_certificate
_true_h3 = h3c39.h3
_true_w_minus = h3c39.w_minus
_true_classify = h2o40.classify


def _h3_no_ell_neq_p(w, p):
    """The criterion with its second clause deleted. The certificate then reads
    as the gcd argument alone, and RUN-037's finding vanishes."""
    usable = [r for r in w if r["v_disc"] % p]
    return {"p": p, "witness": usable[0]["ell"] if usable else None,
            "pass": bool(usable), "candidates_excluded_by_ell_neq_p": []}


def _w_minus_all_mult(ainvs):
    """W_- taken over all multiplicative primes rather than the nonsplit ones,
    which is the restriction the FW-H3 witness actually requires."""
    md = gcd35.multiplicative_data(ainvs)
    if md.get("singular"):
        return []
    return [{"ell": r["p"], "v_disc": r["n"]} for r in md["multiplicative"]]


def _classify_plus_only(bound=h2o40.P_BOUND):
    c = _true_classify(bound)
    c["ordinary_H2_failures"] = [r for r in c["ordinary_H2_failures"]
                                 if (r["a_p"] - 1) % r["p"] == 0]
    return c


def _classify_no_supersingular(bound=h2o40.P_BOUND):
    c = _true_classify(bound)
    c["supersingular"] = []
    return c


def _classify_admits_29(bound=h2o40.P_BOUND):
    """29 is a prime of BAD reduction and a member of W_-. Letting it into the
    good supersingular branch is exactly what would bring RUN-037's H3
    exception into a branch that cannot survive it."""
    c = _true_classify(bound)
    c["supersingular"] = [{"p": 29, "a_p": 0}] + c["supersingular"]
    return c


def _classify_no_failures(bound=h2o40.P_BOUND):
    c = _true_classify(bound)
    c["ordinary_H2_failures"] = []
    return c


def _classify_from_seven(bound=h2o40.P_BOUND):
    """p = 5 dropped from the scan. a_5 = -3 is ordinary and H2-passing, so
    neither set the check reads can move."""
    c = _true_classify(bound)
    c["rows"] = [r for r in c["rows"] if r["p"] > 5]
    c["good_odd_primes"] = len(c["rows"])
    c["supersingular"] = [r for r in c["supersingular"] if r["p"] > 5]
    c["ordinary_H2_failures"] = [r for r in c["ordinary_H2_failures"]
                                 if r["p"] > 5]
    return c


_true_converse = bridge37.lemma_C_converse
_true_good = surj38.good_primes
_true_local_invariants = bridge37.local_invariants
_true_lemma_B = bridge37.lemma_B_status
_true_vac3 = surj38.vacuity_at_3
_true_certify = surj38.certify
_true_ell_two = surj38.ell_two


def _local_no_split_flag(ainvs, ell):
    d = dict(_true_local_invariants(ainvs, ell))
    d.pop("split_multiplicative", None)
    return d


def _lemma_B_established():
    """The document's own 候選 status quietly promoted to established."""
    d = dict(_true_lemma_B())
    d["established_here"] = True
    return d


def _shadow_self(limit=300):
    """The twist compared against the base curve itself: identical everywhere
    and no sign flips, so the invariance is 'confirmed' where it could not
    fail."""
    rows = [{"d": d, "good_primes_compared": 50,
             "discriminant_identical": 50, "a_ell_sign_flips": 0}
            for d in (241, 313)]
    return {"lemma": "A", "status": "cited", "rows": rows,
            "all_identical": True, "flips_seen": False}


def _vac3_false():
    """The structural vacuity at 3 reported as an ordinary refutable class."""
    v = dict(_true_vac3())
    v["structurally_vacuous"] = False
    v["any_case_refutes"] = True
    return v


def _certify_lax(ell, primes):
    r = _true_certify(ell, primes)
    r["undecided"] = []
    r["surjective"] = True
    return r


def _ell_two_asserted():
    d = dict(_true_ell_two())
    d["rational_roots"] = [1]
    d["irreducible"] = False
    d["surjective"] = True          # verdict no longer follows from the cubic
    return d


_true_small_curves = gcd35.small_curves
_true_multiplicative_data = gcd35.multiplicative_data
_true_leave_one_out = gcd35.leave_one_out
_true_local_type = nogo36.local_type
_true_where_it_fires = nogo36.where_it_fires
_true_no_go = nogo36.no_go


def _md_all_split(ainvs):
    """The split/nonsplit classification thrown away in the safe-looking
    direction: everything called split. Lemma 3 then restricts to an empty set,
    whose gcd is 0, so every odd prime becomes a failure."""
    md = _true_multiplicative_data(ainvs)
    if md.get("singular"):
        return md
    for r in md["multiplicative"]:
        r["split"] = True
    md["nonsplit"] = []
    return md


def _leave_one_out_self(md):
    """Lemma 2 without the word "distinct": a multiplicative p is allowed to be
    its own witness, which makes the leave-one-out trivially satisfiable."""
    mult = md["multiplicative"]
    rows = []
    for r in mult:
        p = r["p"]
        chosen = next((s["p"] for s in mult if s["n"] % p), None)
        rows.append({"p": p, "others": [s["p"] for s in mult],
                     "gcd_of_others": 1, "witness": chosen,
                     "n_at_witness": next((s["n"] for s in mult
                                           if s["p"] == chosen), None),
                     "ok": chosen is not None})
    return {"lemma": "fixed multiplicative (leave-one-out)", "rows": rows,
            "all_have_a_distinct_witness": all(r["ok"] for r in rows)}


def _no_go_by_symbol(ainvs, p):
    """Exactly the inference 05 forbids: read the verdict off the Kodaira
    symbol instead of the j-invariant. I0* is potentially good and I1* is not,
    but both are starred, so this fires everywhere the reduction is additive."""
    t = _true_local_type(ainvs, p)
    fires = bool(t["kodaira"]) and t["kodaira"].endswith("*")
    return {**t, "no_go_fires": fires,
            "verdict": "FW17_H2_FAIL" if fires else "no-go silent here",
            "why": "read off the Kodaira symbol"}


def _local_type_pot_good(ainvs, p):
    t = _true_local_type(ainvs, p)
    t["potential_reduction"] = "potentially good"
    return t


def _chars_flat(primes=nogo36.CHARACTER_PRIMES):
    return {"rows": [{"p": p, "size_of_F_p_star": p - 1, "exponent": 2,
                      "every_character_is_quadratic_or_trivial": True}
                     for p in primes],
            "holds_at": list(primes),
            "special_to_3_among_odd_primes": True,
            "note": "flattened"}


def _fires_good_probe_only(probe=(5, 7, 11, 13, 23, 31)):
    """A probe with no multiplicative prime in it. Both sides of the comparison
    then come out empty and agree, which is the vacuity the check must refuse."""
    return _true_where_it_fires(probe)


_true_q_checklist = refA34.q_checklist
_true_base_checklist = refA34.base_checklist


def _q_checklist_no_inertness(q):
    """The five conditions with the 2-division-cubic inertness dropped, which is
    the one that does the discriminating: without it primes P rejects begin to
    pass."""
    d = _true_q_checklist(q)
    d["lines"].pop("q inert in 2-division cubic", None)
    d["all_pass"] = all(d["lines"].values())
    return d


def _base_all_checkable(limit=None):
    """Every base line marked machine-checkable and PASS — the three citations
    scored as though they were checks.

    Takes the same `limit` the real one takes: a stand-in that cannot be called
    the way the check calls it produces a TypeError, and RUN-030 recorded that a
    defect which raises is not a defect a check caught.
    """
    rows = (_true_base_checklist() if limit is None
            else _true_base_checklist(limit=limit))
    for r in rows:
        if not r["machine_checkable"]:
            r["machine_checkable"] = True
            r["status"] = "PASS"
    return rows


_true_certificate = cert32.certificate


def _certificate_unlabelled(limit=None):
    """The Sha row with its ANALYTIC marking stripped from both places — the
    numbers unchanged, so only the labelling assertions can see it."""
    c = _true_certificate(limit) if limit else _true_certificate()
    for r in c["rows"]:
        if r["quantity"] == "analytic_order_of_Sha":
            r["derivation"] = "L/Omega * |E(Q)_tors|^2 / prod c_p"
            r.pop("note", None)
    return c


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


_true_p5u_point_count = p5u.point_count
_true_residue_hom = p5u.residue_homomorphism


def _count_without_O(a, p):
    """#E(F_p) without the point at infinity. Bound to the original, not the
    patched attribute — see _mul_drops_last_add."""
    return _true_p5u_point_count(a, p) - 1


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


def _assert_no_shadowed_helpers() -> list[str]:
    """A flat `_true_*` namespace can be shadowed silently, and was.

    `_true_squarefree` was bound to two different functions with different
    return types, so a defect that meant to drop a sign raised a TypeError
    instead — a crash counted as a catch, which is the one thing this drill must
    not do. `_true_point_count` was bound to two independently written point
    counters that happen to agree, so the defect using it computed the right
    number through the wrong module.

    Both are repaired by name. This guard is the structural part: the drill
    reads its own source and refuses to run if any `_true_*` name is assigned
    twice, so the next collision is loud.
    """
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    names = re.findall(r"^(_true_\w+) = ", src, re.M)
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        raise SystemExit(f"shadowed drill helpers, refusing to run: {dupes}")
    return names


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


def _run_defects(indices: list[int]) -> list[dict]:
    """Plant each listed defect in turn, run every check, restore."""
    results = []
    for i in indices:
        name, kind, expected, make = DEFECTS[i]
        restore = make()
        try:
            got = run_checks()
        finally:
            restore()
        red = [k for k, v in got.items() if not v]
        results.append({"index": i, "defect": name, "kind": kind,
                        "named_check": expected, "checks_that_went_red": red,
                        "caught_by_the_named_check": expected in red})
        flag = ("OK " if expected in red else
                "MISSED " if not red else "WRONG-CHECK ")
        print(f"    {flag:12s} [{kind}] {name}")
        print(f"                 red: {', '.join(red) if red else '(none)'}")
    return results


def _run_controls(indices: list[int]) -> list[dict]:
    out = []
    for i in indices:
        name, make = CONTROLS[i]
        restore = make()
        try:
            got = run_checks()
        finally:
            restore()
        red = [k for k, v in got.items() if not v]
        out.append({"index": i, "control": name, "checks_that_went_red": red,
                    "undisturbed": not red})
        print(f"    {'OK ' if not red else 'DISTURBED '}control: {name}"
              + (f"   red: {', '.join(red)}" if red else ""))
    return out


def _assemble(baseline: dict, results: list[dict], ctrl_results: list[dict],
              after: dict) -> dict:
    """The log, in the same shape whether built by one process or merged from
    several. Entries carry their original index; totals are recomputed here."""
    results = sorted(results, key=lambda r: r["index"])
    ctrl_results = sorted(ctrl_results, key=lambda r: r["index"])
    uncaught = [r["defect"] for r in results if not r["checks_that_went_red"]]
    wrong_catcher = [{"defect": r["defect"], "expected": r["named_check"],
                      "actually_caught_by": r["checks_that_went_red"]}
                     for r in results
                     if r["checks_that_went_red"]
                     and r["named_check"] not in r["checks_that_went_red"]]
    disturbed = [{"control": c["control"], "red": c["checks_that_went_red"]}
                 for c in ctrl_results if not c["undisturbed"]]
    return {
        "gate": "src11_gate_drill",
        "covers": COVERS,
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
               and all(after.values())
               and len(results) == len(DEFECTS)
               and len(ctrl_results) == len(CONTROLS)),
    }


def _write_and_summarise(log: dict, out: pathlib.Path) -> int:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + NEWLINE,
                   encoding="utf-8", newline=NEWLINE)
    t = log["totals"]
    uncaught = t["UNCAUGHT_BY_ANY_CHECK"]
    print()
    print(f"  {t['defects']} defects, {t['caught_by_the_named_check']} caught "
          f"by the check named for them")
    print(f"  uncaught by any check      : "
          f"{len(uncaught)}{'  ' + ', '.join(uncaught) if uncaught else ''}")
    print(f"  caught by the wrong check  : {len(t['CAUGHT_BY_THE_WRONG_CHECK'])}")
    print(f"  {t['controls']} controls, "
          f"{len(t['controls_that_disturbed_a_check'])} disturbed a check")
    print(f"  state restored afterwards  : {log['state_restored_afterwards']}")
    print()
    print(f"wrote {out.name}")
    return 0 if log["ok"] else 1


def main(shard: tuple[int, int] | None = None,
         out: pathlib.Path | None = None) -> int:
    """No arguments: the whole drill in this process, as always.

    `shard=(k, n)`: every n-th defect and control starting at k, written as a
    PARTIAL log to `out`. Each shard runs its own baseline and its own
    restored-state check, so a shard that started from a red tree or left one
    behind reports it itself. `merge()` reassembles partials in original order
    into the standard log — the same shape, the same totals, the same rule.
    The drill's semantics do not depend on which process planted a defect:
    every defect is still planted alone, in a process whose other state is
    pristine, and restored before the next.
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    helpers = _assert_no_shadowed_helpers()
    print(f"  {len(helpers)} _true_* helpers, none shadowed")
    baseline = run_checks()
    if not all(baseline.values()):
        raise SystemExit(f"the undisturbed gates are not green: {baseline}")
    print(f"  baseline: all {len(baseline)} checks green")

    if shard is None:
        d_idx = list(range(len(DEFECTS)))
        c_idx = list(range(len(CONTROLS)))
    else:
        k, n = shard
        d_idx = list(range(k, len(DEFECTS), n))
        c_idx = list(range(k, len(CONTROLS), n))
        print(f"  shard {k}/{n}: {len(d_idx)} defects, {len(c_idx)} controls")

    results = _run_defects(d_idx)
    print()
    ctrl_results = _run_controls(c_idx)
    after = run_checks()

    if shard is not None:
        k, n = shard
        partial = {"shard": [k, n], "defects_total": len(DEFECTS),
                   "controls_total": len(CONTROLS),
                   "baseline_all_green": baseline, "after": after,
                   "defects": results, "controls": ctrl_results}
        out = out or OUT.with_name(f"src11-gate-drill.shard{k}of{n}.json")
        out.write_text(json.dumps(partial, indent=2, ensure_ascii=False) + NEWLINE,
                       encoding="utf-8", newline=NEWLINE)
        print(f"{NEWLINE}  shard {k}/{n} done, restored: {all(after.values())}; "
              f"wrote {out.name}")
        return 0 if all(after.values()) else 1

    log = _assemble(baseline, results, ctrl_results, after)
    return _write_and_summarise(log, OUT)


def merge(paths: list[pathlib.Path]) -> int:
    """Reassemble shard partials into the standard log."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    parts = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    n_set = {p["shard"][1] for p in parts}
    if len(n_set) != 1:
        raise SystemExit(f"shards disagree on n: {n_set}")
    n = n_set.pop()
    ks = sorted(p["shard"][0] for p in parts)
    if ks != list(range(n)):
        raise SystemExit(f"shards present {ks}, expected 0..{n - 1}")
    for p in parts:
        if not all(p["baseline_all_green"].values()):
            raise SystemExit(f"shard {p['shard']} started from a red baseline")
        if p["defects_total"] != len(DEFECTS) or p["controls_total"] != len(CONTROLS):
            raise SystemExit(f"shard {p['shard']} ran against a different "
                             f"defect list ({p['defects_total']} vs "
                             f"{len(DEFECTS)})")
    results = [r for p in parts for r in p["defects"]]
    ctrls = [c for p in parts for c in p["controls"]]
    if sorted(r["index"] for r in results) != list(range(len(DEFECTS))):
        raise SystemExit("merged defects do not cover 0..N-1 exactly once")
    if sorted(c["index"] for c in ctrls) != list(range(len(CONTROLS))):
        raise SystemExit("merged controls do not cover 0..M-1 exactly once")
    baseline = parts[0]["baseline_all_green"]
    # `after` for the merged run: every shard must have restored its own state
    after = {k: all(p["after"][k] for p in parts) for k in baseline}
    log = _assemble(baseline, results, ctrls, after)
    log["merged_from"] = [str(p.name) for p in paths]
    log["shards"] = n
    print(f"  merged {n} shards: {len(results)} defects, {len(ctrls)} controls")
    return _write_and_summarise(log, OUT)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--merge":
        raise SystemExit(merge([pathlib.Path(a) for a in args[1:]]))
    if args and args[0] == "--shard":
        k, n = (int(x) for x in args[1].split("/"))
        outp = pathlib.Path(args[3]) if len(args) > 3 and args[2] == "--out" else None
        raise SystemExit(main(shard=(k, n), out=outp))
    raise SystemExit(main())
