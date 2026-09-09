"""Gate 22 — the witness-network criterion: its lemmas, and whether it generalises anything.

數學戰士「墜衡」 / AMRAL Research Lab.

`31_Witness_Network_Criterion_v0.2` strengthens the two-witness criterion of
`30` by replacing the valuation-one hypotheses with gcd conditions. With
n_ℓ = v_ℓ(Δ_E) over the odd multiplicative primes M and the nonsplit ones M⁻,

    g_mult = gcd_{ℓ∈M} n_ℓ,     g_- = gcd_{ℓ∈M⁻} n_ℓ,
    R_mult = odd primes dividing g_mult,   R_- likewise,

and §3 states the point of the change:

    R_mult ∪ R_- is a finite exceptional-prime set … This is strictly stronger
    than requiring both gcds to be powers of 2.

THREE THINGS ARE CHECKABLE, AND THEY ARE OF THREE DIFFERENT KINDS.

**Lemma 2.1 and 2.2 are elementary and are verified as such.** "Some ℓ has
p ∤ n_ℓ" fails exactly when p divides every n_ℓ, which is exactly p | gcd. There
is nothing to approximate, so the gate checks the equivalence directly on every
base curve that has multiplicative primes at all — including the edge cases the
statement quietly needs (M ≠ ∅ for the gcd to exist, and M∖{p} ≠ ∅ for the
leave-one-out form).

**The leave-one-out condition is a finite check and is run as one.** LOO(p) can
fail, and where it does the network has to route p by hand. How often that
happens is a fact about a population, not about the theorem.

**"Strictly stronger" is a claim about non-emptiness, and it is measured.** A
generalisation that admits nothing new is not one. Two populations are used: the
40,749 base curves, where the gcd statistic is computable even though the
criteria do not apply to them (they are all semistable — RUN-016), and a direct
search over small models for curves that actually meet the certificate's
arithmetic conditions — additive reduction only at 2, negative discriminant, no
rational 2-torsion, S₃ two-division field, with M and M⁻ both non-empty.

Usage:  python code/src22_witness_network.py
"""

from __future__ import annotations

import collections
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src08_modular_curve_confirmation as x0n            # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src10_phase2_density_and_base as ph2               # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src22-witness-network.json"

SEARCH_A4 = 30
SEARCH_A6 = 30


def odd_part(n: int) -> int:
    while n and n % 2 == 0:
        n //= 2
    return n


def odd_prime_divisors(n: int) -> set[int]:
    out, n, d = set(), abs(n), 3
    while n % 2 == 0:
        n //= 2
    while d * d <= n:
        if n % d == 0:
            out.add(d)
            while n % d == 0:
                n //= d
        d += 2
    if n > 1:
        out.add(n)
    return out


def witness_sets(ainvs, cond_primes) -> dict:
    """M, M⁻ and their discriminant valuations, from Tate's algorithm."""
    M, Mminus = {}, {}
    for p in cond_primes:
        if p == 2:
            continue
        d = tate.reduction_data(ainvs, p)
        kod = d["kodaira"]
        if not (kod.startswith("I") and not kod.endswith("*") and kod != "I0"):
            continue
        M[p] = d["v_disc"]
        if d.get("split_multiplicative") is False:
            Mminus[p] = d["v_disc"]
    return {"M": M, "M_minus": Mminus}


def gcds(ws: dict) -> dict:
    M, Mm = ws["M"], ws["M_minus"]
    g_mult = math.gcd(*M.values()) if len(M) > 1 else (next(iter(M.values()))
                                                       if M else None)
    g_minus = math.gcd(*Mm.values()) if len(Mm) > 1 else (next(iter(Mm.values()))
                                                          if Mm else None)
    R = set()
    if g_mult is not None:
        R |= odd_prime_divisors(g_mult)
    if g_minus is not None:
        R |= odd_prime_divisors(g_minus)
    return {"g_mult": g_mult, "g_minus": g_minus,
            "R": sorted(R), "exceptional_set_empty": not R}


def lemma_21_holds(ws: dict, p: int) -> bool:
    """∃ℓ ∈ M with p ∤ n_ℓ  ⟺  p ∤ g_mult, for odd p ∉ M."""
    M = ws["M"]
    if not M or p in M:
        return True                       # outside the lemma's hypotheses
    exists = any(n % p for n in M.values())
    g = math.gcd(*M.values()) if len(M) > 1 else next(iter(M.values()))
    return exists == (g % p != 0)


def loo(ws: dict, p: int):
    """The leave-one-out condition at a fixed multiplicative prime p."""
    rest = {ell: n for ell, n in ws["M"].items() if ell != p}
    if not rest:
        return {"holds": False, "why": "M minus p is empty"}
    exists = any(n % p for n in rest.values())
    g = math.gcd(*rest.values()) if len(rest) > 1 else next(iter(rest.values()))
    return {"holds": exists, "gcd_form_agrees": exists == (g % p != 0),
            "gcd_without_p": g}


def certificate_candidates(a4_range: int, a6_range: int) -> list[dict]:
    """Small models meeting the certificate's arithmetic conditions.

    Additive reduction only at 2, Δ < 0, no rational 2-torsion, S₃ two-division
    field, and both M and M⁻ non-empty — the conditions (T2)–(T5) share with
    `31`'s standing assumptions, checked here rather than assumed.
    """
    out = []
    for a1 in (0, 1):
        for a2 in (-1, 0, 1):
            for a3 in (0, 1):
                for a4 in range(-a4_range, a4_range + 1):
                    for a6 in range(-a6_range, a6_range + 1):
                        inv = [a1, a2, a3, a4, a6]
                        b2, b4, b6, _b8, disc = anchor.b_invariants(inv)
                        if disc >= 0:
                            continue
                        c3, c2, c1, c0 = 4, b2, 2 * b4, b6
                        if any((((c3 * x + c2) * x + c1) * x + c0) == 0
                               for x in range(-60, 61)):
                            continue           # a rational 2-torsion x-coordinate
                        dc = (18 * c3 * c2 * c1 * c0 - 4 * c2 ** 3 * c0
                              + c2 * c2 * c1 * c1 - 4 * c3 * c1 ** 3
                              - 27 * c3 * c3 * c0 * c0)
                        if dc == 0 or (dc > 0 and math.isqrt(dc) ** 2 == dc):
                            continue           # square discriminant → C₃, not S₃
                        primes = _small_primes_of(abs(disc))
                        if primes is None:
                            continue
                        # Additive at p is exactly p | c4, an O(1) test. Running
                        # Tate first to find out was what made this search
                        # unusable: a curve with additive reduction at 3 pays
                        # for the step-7 search and an I_m* chain before being
                        # rejected, and most candidates are rejected.
                        c4 = b2 * b2 - 24 * b4
                        if 2 not in primes or c4 % 2 != 0:
                            continue
                        if any(c4 % p == 0 for p in primes if p != 2):
                            continue
                        try:
                            red = {p: tate.reduction_data(inv, p) for p in primes}
                        except Exception:
                            continue
                        if [p for p in primes if red[p]["f"] >= 2] != [2]:
                            continue
                        ws = witness_sets(inv, primes)
                        if not ws["M"] or not ws["M_minus"]:
                            continue
                        g = gcds(ws)
                        out.append({"ainvs": inv, "discriminant": disc,
                                    "bad_primes": primes,
                                    "M": {str(k): v for k, v in ws["M"].items()},
                                    "M_minus": {str(k): v for k, v
                                                in ws["M_minus"].items()},
                                    **{k: v for k, v in g.items() if k != "R"},
                                    "R": g["R"]})
    return out


def which_criterion_applies(c: dict) -> dict:
    """Which of `30`, `31` can phrase this candidate at all.

    `30`'s (T4)/(T5) name an odd multiplicative prime and a nonsplit one, each
    of valuation exactly 1. `31` asks instead that the gcds be understood, and
    puts their odd prime divisors into a finite exceptional set. The two are
    not the same weakening: a curve whose only nonsplit prime has valuation 2
    fails (T5) while its g_- = 2 leaves the exceptional set EMPTY, so it is
    reached by `31` without any exceptional prime at all.
    """
    M = {int(k): v for k, v in c["M"].items()}
    Mm = {int(k): v for k, v in c["M_minus"].items()}
    t4 = any(v == 1 for v in M.values())
    t5 = any(v == 1 for v in Mm.values())
    return {"criterion_30_applies": t4 and t5,
            "T4_satisfiable": t4, "T5_satisfiable": t5,
            "exceptional_set_empty": not c["R"]}


def is_analytic_rank_zero(res: dict) -> bool:
    """Rank 0 needs a DECIDED root number of +1 and a non-vanishing L(E,1).

    An undecided sign is not weak evidence for +1, it is no evidence, and
    folding it in would silently inflate the population counts below. Split out
    so the drill can plant that exact confusion.
    """
    return bool(res["analytic_rank_is_zero"])


def ord_2_l_alg_is_zero(l_alg: float, tol: float = 1e-6) -> bool:
    """(T1)'s own condition, tested on L^alg = L(E,1)/Ω itself.

    The BSD quotient L·|E_tors|²/(Ω·∏c_p) is a different number, and testing
    that one instead is a silent way to get (T1) wrong: at [0,−1,0,0,−27] the
    quotient is 1 while L^alg is 2, so the curve passes on the wrong quantity
    and fails on the right one.
    """
    r = round(l_alg)
    return abs(l_alg - r) < tol and r % 2 == 1


def analytic_side(candidates, conductor_cap=60000, limit=4000):
    """Do any network-only candidates satisfy (T1)'s analytic hypotheses too?

    Non-emptiness of the arithmetic conditions is the weaker claim: it says the
    gcd form admits models `30` cannot phrase. The certificate also demands an
    analytic input — analytic rank 0 and ord₂ L^alg(E,1) = 0 — and a family that
    met the arithmetic and never the analytic would still leave `31` with an
    empty domain.

    This does NOT compute Ш. The quotient L·|E_tors|²/(Ω·∏c_p) is the *analytic*
    order, and reporting it as an order of Ш is exactly the substitution Phase
    0 §6 names as not-progress. It is used here only as a consistency test on
    the numerics: a quotient that is not a positive square integer means the
    period, the L-value, the torsion bound or a Tamagawa number is wrong, and
    the row is not counted.
    """
    rows, counted, ord2_zero, skipped = [], 0, 0, []
    for c in candidates:
        inv, primes = c["ainvs"], c["bad_primes"]
        N = 1
        tam, ok = {}, True
        for p in primes:
            d = tate.reduction_data(inv, p, want_c=True)
            N *= p ** d["f"]
            if d["c"] is None:
                ok = False
            tam[str(p)] = d["c"]
        if not ok or N > conductor_cap:
            skipped.append({"ainvs": inv, "conductor": N,
                            "why": "a Tamagawa number is unresolved" if not ok
                                   else f"conductor {N} above the cap"})
            continue
        res = anchor.analyse("candidate", inv, N, limit=limit)
        if not is_analytic_rank_zero(res):
            # An undecided root number is NOT evidence of positive rank. The
            # three outcomes are kept apart: w = −1 forces odd rank, w = +1 with
            # L(E,1) vanishing indicates rank ≥ 2, and an undecided sign at
            # this truncation says only that this gate did not resolve it.
            w = res["root_number"]
            rows.append({"ainvs": inv, "conductor": N, "root_number": w,
                         "status": ("root number undecided at this truncation"
                                    if w is None else
                                    "w = −1, so the rank is odd" if w == -1 else
                                    "w = +1 but L(E,1) vanishes — rank ≥ 2")})
            continue
        prod_c = 1
        for v in tam.values():
            prod_c *= v
        t = res["torsion_bound_gcd"]
        l_alg = res["L_at_1"] / res["real_period"]
        quotient = l_alg * t * t / prod_c
        near = round(quotient)
        square = near > 0 and math.isqrt(near) ** 2 == near
        consistent = square and abs(quotient - near) < 1e-6
        odd_l_alg = ord_2_l_alg_is_zero(l_alg)
        if consistent:
            counted += 1
            if odd_l_alg:
                ord2_zero += 1
        rows.append({"ainvs": inv, "conductor": N, "M": c["M"],
                     "M_minus": c["M_minus"], "R": c["R"],
                     "tamagawa": tam, "torsion_bound": t,
                     "L_over_Omega": l_alg,
                     "ord_2_L_alg_is_zero": odd_l_alg,
                     "quotient": quotient, "nearest_integer": near,
                     "numerics_consistent": consistent,
                     "status": "rank 0" if consistent else "rank 0, quotient off"})
    return {"examined": len(candidates), "tested": len(rows),
            "not_tested": skipped,
            "with_rank_zero_and_consistent": counted,
            "and_with_ord_2_L_alg_zero": ord2_zero,
            "note": ("ord₂ L^alg = 0 is (T1)'s own condition; a candidate that "
                     "is rank 0 but has L/Ω even fails the certificate, so the "
                     "second number is the one that bounds the criterion's "
                     "domain"),
            "rows": rows}


def _small_primes_of(n: int, cap: int = 4000):
    """Prime divisors of n, or None if a cofactor exceeds the trial-division cap."""
    out, d = [], 2
    while d * d <= n and d < cap:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        if n >= cap * cap:
            return None
        out.append(n)
    return out


def squarefree_products(members, k_max=3, cap=12):
    """§5: squarefree products of support primes stay in the family.

    The claims are that d ≡ 1 (mod 8) and that every conductor prime splits in
    Q(√d) — both of which follow from the same holding for each factor, but
    both of which are worth checking, because the per-prime results of RUN-015
    and RUN-016 were only ever established one prime at a time.
    """
    import itertools
    out = []
    for k in range(2, k_max + 1):
        for combo in itertools.islice(itertools.combinations(members, k), cap):
            d = 1
            for q in combo:
                d *= q
            row = {"factors": list(combo), "d": d, "d_mod_8": d % 8,
                   "d_is_1_mod_8": d % 8 == 1}
            row["splits_at_every_conductor_prime"] = all(
                (ph2.legendre(d, ell) == 1) if ell != 2 else (d % 8 == 1)
                for ell in (2, 3, 29))
            row["every_factor_inert_in_the_cubic"] = all(
                ph2.cubic_root_count(ph2.F2, q) == 0 for q in combo)
            out.append(row)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    records = json.loads(x0n.ARITH.read_text(encoding="utf-8"))["records"]
    lemma_checks = lemma_fail = 0
    loo_agree = loo_disagree = loo_fails = 0
    r_sizes = collections.Counter()
    g_mult_odd = collections.Counter()
    g_minus_odd = collections.Counter()
    no_nonsplit = 0
    examples = []

    for idx, r in enumerate(records):
        if idx and idx % 5000 == 0:
            print(f"    … {idx:,}/{len(records):,}", file=sys.stderr)
        ws = witness_sets(r["ainvs"], r["conductor_primes"])
        if not ws["M"]:
            continue
        g = gcds(ws)
        g_mult_odd[odd_part(g["g_mult"])] += 1
        if g["g_minus"] is None:
            no_nonsplit += 1
        else:
            g_minus_odd[odd_part(g["g_minus"])] += 1
        r_sizes[len(g["R"])] += 1
        if g["R"] and len(examples) < 10:
            examples.append({"label": r["curve_label"],
                             "M": {str(k): v for k, v in ws["M"].items()},
                             "M_minus": {str(k): v for k, v
                                         in ws["M_minus"].items()},
                             "R": g["R"]})
        for p in (3, 5, 7, 11, 13):
            lemma_checks += 1
            if not lemma_21_holds(ws, p):
                lemma_fail += 1
        for p in ws["M"]:
            res = loo(ws, p)
            if res.get("gcd_form_agrees") is False:
                loo_disagree += 1
            elif "gcd_form_agrees" in res:
                loo_agree += 1
            if not res["holds"]:
                loo_fails += 1

    print("  searching small models for certificate candidates …",
          file=sys.stderr)
    cands = certificate_candidates(SEARCH_A4, SEARCH_A6)
    both_powers_of_two = [c for c in cands if not c["R"]]
    network_only = [c for c in cands if c["R"]]
    anchor_row = [c for c in cands if c["ainvs"] == [0, 1, 0, 8, -16]]
    ana = analytic_side(network_only)
    verdicts = [which_criterion_applies(c) for c in cands]
    reach = collections.Counter(
        ("both" if v["criterion_30_applies"] else
         "31 only, exceptional set empty" if v["exceptional_set_empty"] else
         "31 only, an odd exceptional prime")
        for v in verdicts)
    t5_fails = sum(1 for v in verdicts if not v["T5_satisfiable"])
    t4_fails = sum(1 for v in verdicts if not v["T4_satisfiable"])

    members = [q for q in anchor.sieve(4000) if fam.in_P(q)]
    products = squarefree_products(members)
    ramified = {2, 3, 29} | odd_prime_divisors(-174)
    deleted = [q for q in members if q in ramified]

    log = {
        "gate": "src22_witness_network",
        "section_5_squarefree_products": {
            "claim": ("any positive squarefree d supported on 𝒫° satisfies "
                      "d ≡ 1 (mod 8) and has every conductor prime split in "
                      "Q(√d), so the family is not only prime twists"),
            "products_checked": len(products),
            "all_are_1_mod_8": all(r["d_is_1_mod_8"] for r in products),
            "all_split_at_every_conductor_prime": all(
                r["splits_at_every_conductor_prime"] for r in products),
            "all_factors_inert_in_the_cubic": all(
                r["every_factor_inert_in_the_cubic"] for r in products),
            "sample": products[:6],
            "note": ("RUN-015 established these one prime at a time; this is "
                     "the composite case the 2-primary theorem actually needs"),
        },
        "finite_deletion_at_696e1": {
            "R_mult_union_R_minus": [],
            "why": "n_3 = n_29 = 1, so both gcds are 1 and neither has an odd "
                   "divisor",
            "ramified_primes_of_L_E_K_E": sorted(ramified),
            "members_below_4000_removed_by_the_deletion": deleted,
            "deletion_is_vacuous_here": not deleted,
        },
        "lemmas_2_1_and_2_2": {
            "statement": ("for odd p ∉ M: some ℓ ∈ M has p ∤ n_ℓ  ⟺  p ∤ "
                          "gcd_{ℓ∈M} n_ℓ"),
            "instances_checked": lemma_checks,
            "failures": lemma_fail,
            "note": ("elementary — the failure of every witness is exactly "
                     "p | n_ℓ for all ℓ, which is p dividing the gcd. Checked "
                     "rather than asserted because the statement needs M ≠ ∅ "
                     "for the gcd to exist at all"),
        },
        "leave_one_out": {
            "statement": ("LOO(p): some ℓ ≠ p in M has p ∤ n_ℓ; equivalently "
                          "p ∤ gcd over M∖{p}, when that set is non-empty"),
            "gcd_form_agrees": loo_agree,
            "gcd_form_disagrees": loo_disagree,
            "LOO_fails_at_some_fixed_multiplicative_prime": loo_fails,
            "note": ("a failure is not an error in the theorem — it is a prime "
                     "the network must route individually, which is what makes "
                     "the exception set finite rather than empty"),
        },
        "gcd_statistics_over_the_base": {
            "curves_with_a_multiplicative_prime": sum(r_sizes.values()),
            "odd_part_of_g_mult": {str(k): v for k, v in g_mult_odd.most_common()},
            "odd_part_of_g_minus": {str(k): v for k, v
                                    in g_minus_odd.most_common(10)},
            "curves_with_no_nonsplit_multiplicative_prime": no_nonsplit,
            "size_of_R_mult_union_R_minus": {str(k): v for k, v
                                             in r_sizes.most_common()},
            "fraction_with_a_nonempty_exceptional_set": (
                sum(v for k, v in r_sizes.items() if k) / sum(r_sizes.values())),
            "caveat": ("the base is entirely semistable (RUN-016), so neither "
                       "criterion applies to any of these curves. The gcd "
                       "statistic is still computable, and this is the largest "
                       "population this arm has to compute it on"),
            "examples": examples,
        },
        "is_the_generalisation_non_empty": {
            "search": (f"a1 ∈ {{0,1}}, a2 ∈ {{−1,0,1}}, a3 ∈ {{0,1}}, "
                       f"|a4| ≤ {SEARCH_A4}, |a6| ≤ {SEARCH_A6}"),
            "conditions": ("Δ < 0, no rational 2-torsion, S₃ two-division "
                           "field, additive reduction only at 2, M and M⁻ "
                           "both non-empty"),
            "candidates_found": len(cands),
            "both_gcds_a_power_of_2": len(both_powers_of_two),
            "an_odd_gcd_divisor_present": len(network_only),
            "network_only_sample": network_only[:10],
            "network_only_on_the_analytic_side": ana,
            "which_criterion_reaches_each_candidate": {
                "counts": dict(reach),
                "candidates_30_cannot_phrase": (
                    len(cands) - reach["both"]),
                "T5_unsatisfiable": t5_fails,
                "T4_unsatisfiable": t4_fails,
                "impossible_cell": sum(
                    1 for c, v in zip(cands, verdicts)
                    if v["criterion_30_applies"] and c["R"]),
                "reading": ("(T4) and (T5) holding forces both gcds to 1, so "
                            "the fourth cell must be empty; it is measured "
                            "rather than assumed. The 38 with an odd "
                            "exceptional prime are the ones §3's sentence is "
                            "about, and they are not the whole gap"),
            },
            "anchor_696e1_in_the_search": anchor_row,
            "verdict": (
                "the generalisation is NOT vacuous" if network_only else
                "no candidate in this range needs the generalisation"),
        },
        "ok": (lemma_fail == 0 and loo_disagree == 0 and len(cands) > 0
               and all(r["d_is_1_mod_8"] and r["splits_at_every_conductor_prime"]
                       and r["every_factor_inert_in_the_cubic"]
                       for r in products)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")

    print()
    print(f"  Lemma 2.1/2.2: {lemma_checks:,} instances, {lemma_fail} failures")
    print(f"  leave-one-out: gcd form agrees {loo_agree:,}, disagrees "
          f"{loo_disagree}   LOO fails at {loo_fails:,} fixed primes")
    print()
    gs = log["gcd_statistics_over_the_base"]
    print(f"  base curves with a multiplicative prime: "
          f"{gs['curves_with_a_multiplicative_prime']:,}")
    print(f"    odd part of g_mult : {dict(list(g_mult_odd.most_common(5)))}")
    print(f"    odd part of g_-    : {dict(list(g_minus_odd.most_common(5)))}"
          f"   (plus {no_nonsplit:,} with no nonsplit prime at all)")
    print(f"    |R_mult ∪ R_-|     : {dict(r_sizes.most_common())}")
    print(f"    non-empty exceptional set: "
          f"{gs['fraction_with_a_nonempty_exceptional_set']:.1%}")
    print()
    n = log["is_the_generalisation_non_empty"]
    print(f"  certificate candidates in the search range: {len(cands)}")
    print(f"    both gcds a power of 2 (two-witness style) : "
          f"{len(both_powers_of_two)}")
    print(f"    an odd gcd divisor (network only)          : "
          f"{len(network_only)}")
    print(f"    → {n['verdict']}")
    for c in network_only[:5]:
        print(f"      {c['ainvs']}  M={c['M']}  M⁻={c['M_minus']}  R={c['R']}")
    print(f"    which criterion reaches them: {dict(reach)}")
    print(f"      (T5) unsatisfiable for {t5_fails}, (T4) for {t4_fails}; "
          f"impossible cell "
          f"{log['is_the_generalisation_non_empty']['which_criterion_reaches_each_candidate']['impossible_cell']}")
    print(f"    of the {ana['examined']} network-only candidates, "
          f"{ana['tested']} testable here, "
          f"{ana['with_rank_zero_and_consistent']} of analytic rank 0, "
          f"{ana['and_with_ord_2_L_alg_zero']} of those with ord₂ L^alg = 0")
    print()
    s5 = log["section_5_squarefree_products"]
    print(f"  §5 squarefree products: {s5['products_checked']} checked   "
          f"all ≡ 1 mod 8: {s5['all_are_1_mod_8']}   all split at 2, 3, 29: "
          f"{s5['all_split_at_every_conductor_prime']}")
    fd = log["finite_deletion_at_696e1"]
    print(f"  finite deletion at 696.e1: ramified primes "
          f"{fd['ramified_primes_of_L_E_K_E']}, members removed "
          f"{fd['members_below_4000_removed_by_the_deletion']} — vacuous: "
          f"{fd['deletion_is_vacuous_here']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
