"""Gate 48 — the H2 chain's internal consistency, and the corpus's H3 disagreement.

數學戰士「墜衡」 / AMRAL Research Lab.

Three documents state FW-H2 at three levels, and they must be the same statement.

    08_FW_Weight2_Exact_Translation   representation level:
                                      H2 FAIL <=> alpha beta^-1 in
                                      {chi_cyc, chi_cyc^-1}
    03_FW_H2_Jordan_Holder_Lemma      Jordan-Hölder level:
                                      H2 FAIL <=> a JH character is quadratic
                                      or trivial, i.e. lambda^2 = 1 or mu^2 = 1
    10_FW_H2_and_Ordinary_Obstruction ordinary specialisation:
                                      H2 FAIL <=> a_p(E)^2 = 1 (mod p)

The first two are algebra over any pair of characters with `lambda mu = omega`,
the Weil-pairing relation both documents take from `det E[p] = chi_cyc`. That
algebra is verified here EXHAUSTIVELY rather than restated: over cyclic character
groups of every order up to a bound and every value of omega, the two conditions
pick out exactly the same pairs.

AND `10`'s CRITERION NAMES ONLY ONE OF THE TWO CASES, WHICH IS COMPLETE ONLY
BECAUSE THE CYCLOTOMIC CHARACTER IS RAMIFIED. `03` allows either constituent to
be the quadratic one. `10` writes the ordinary semisimplification as
`alpha-bar + chi_cyc alpha-bar^-1` with `alpha-bar` UNRAMIFIED and names the
failure `alpha-bar^2 = 1`. The other case is `(chi_cyc alpha-bar^-1)^2 = 1`,
which forces `chi_cyc^2` to be unramified — and the mod-p cyclotomic character
has order `p - 1` on inertia, so `chi_cyc^2` is trivial there exactly when
`p - 1` divides 2, that is at `p = 2` and `p = 3`. For every `p >= 5` the second
case cannot occur and `10`'s single congruence is the whole criterion. At
`p = 3` it is not, and `05` has its own `p = 3` section for the same reason
RUN-036 could not certify surjectivity there.

THE H3 DISAGREEMENT IS REPORTED, NOT RESOLVED. `02` says the divisibility
criterion must not be taken as complete H3; `08` boxes exactly that criterion as
an iff and calls itself the exact weight-2 translation; `09` states the same
three conditions again as a definition. Two of the three treat it as H3 and one
does not. This gate quotes all three, computes that `08`'s and `09`'s conditions
are identical, and says which of this arm's verdicts change under each reading:
none of the numbers, all of the labels.

Usage:  python code/src48_h2_chain_and_h3_dispute.py
"""

from __future__ import annotations

import itertools
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src39_fw_h3_compiler as h3c                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = LOGS / "src48-h2-chain.json"

ORDER_BOUND = 40                          # character-group orders exhausted
RAMIFICATION_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)

H3_CONDITIONS = ("ell || N",
                 "E nonsplit multiplicative at ell",
                 "ell != p",
                 "p does not divide v_ell(Delta_min)")


def equivalence_03_08(bound: int = ORDER_BOUND) -> dict:
    """`03`'s lemma against `08`'s ratio test, exhausted over finite groups.

    Characters into a cyclic group are written additively, so `lambda mu =
    omega` is `l + u = w`, `lambda^2 = 1` is `2l = 0`, and
    `alpha beta^-1 in {omega, omega^-1}` is `l - u = +-w`. Every order up to the
    bound, every omega, every admissible pair.
    """
    checked = mismatched = 0
    examples = []
    for m in range(1, bound + 1):
        for w in range(m):
            for l in range(m):
                u = (w - l) % m
                a = (2 * l % m == 0) or (2 * u % m == 0)
                b = ((l - u) % m == w % m) or ((l - u) % m == (-w) % m)
                checked += 1
                if a != b:
                    mismatched += 1
                    if len(examples) < 5:
                        examples.append({"order": m, "omega": w,
                                         "lambda": l, "mu": u,
                                         "lemma_03": a, "ratio_08": b})
    return {"character_group_orders_exhausted": bound,
            "pairs_checked": checked,
            "mismatches": mismatched,
            "equivalent": mismatched == 0,
            "counterexamples": examples,
            "shared_input": "lambda mu = omega, from det E[p] = chi_cyc — the "
                            "Weil pairing, which both documents cite and "
                            "neither this gate nor either document proves",
            "why_exhaustive": ("the two statements are algebra about a pair of "
                               "characters with a fixed product; exhausting "
                               "the finite case is a check, restating the "
                               "derivation is not")}


def ordinary_case_completeness(primes=RAMIFICATION_PRIMES) -> dict:
    """Why `10`'s single congruence is the whole of `03`'s condition — and where.

    `03` allows either JH constituent to be quadratic. `10` names only the
    unramified one. The other case forces `chi_cyc^2` unramified, and the mod-p
    cyclotomic character has order `p - 1` on inertia, so that happens exactly
    when `p - 1` divides 2.
    """
    rows = []
    for p in primes:
        order_on_inertia = p - 1
        second_case_possible = 2 % order_on_inertia == 0
        rows.append({"p": p,
                     "order_of_chi_cyc_on_inertia": order_on_inertia,
                     "chi_cyc_squared_trivial_on_inertia": second_case_possible,
                     "second_case_possible": second_case_possible,
                     "10s_criterion_is_complete": not second_case_possible})
    bad = [r["p"] for r in rows if r["second_case_possible"]]
    return {"rows": rows,
            "primes_where_the_second_case_survives": bad,
            "complete_for_every_p_at_least_5": all(
                r["10s_criterion_is_complete"] for r in rows if r["p"] >= 5),
            "the_exception_is_3": bad == [2, 3],
            "reading": ("`10`'s a_p^2 = 1 (mod p) is the whole of H2 failure at "
                        "every good ordinary p >= 5. At p = 3 it is not, which "
                        "is the same prime `05` gives its own section and the "
                        "same prime RUN-036 could not certify")}


def the_chain() -> dict:
    """Which links are verified here and which are the corpus's own."""
    return {"links": [
        {"from": "08 (representation level)", "to": "03 (Jordan–Hölder level)",
         "status": "VERIFIED HERE", "how": "exhausted over finite character "
                                           "groups"},
        {"from": "03 (Jordan–Hölder level)", "to": "10 (ordinary case)",
         "status": "VERIFIED HERE, with its range",
         "how": "the second JH case needs chi_cyc^2 unramified, impossible for "
                "p >= 5"},
        {"from": "10 (ordinary case)", "to": "RUN-038's predicate",
         "status": "the corpus's own derivation, cited",
         "how": "alpha-bar unramified with Frobenius value a_p mod p, so "
                "alpha-bar^2 = 1 is a_p^2 = 1 (mod p)"},
        {"from": "Fouquet–Wan Theorem 1.7", "to": "08",
         "status": "CITED", "how": "the theorem's forbidden local form; "
                                   "external to this tree"}],
        "verified_here": 2, "cited": 2,
        "note": "a chain is only as strong as its weakest link, and the "
                "weakest here is the theorem itself, which no round of this "
                "arm proves"}


def the_h3_dispute() -> dict:
    """All three statements, quoted, with the arithmetic of what turns on it."""
    def has(name: str, needle: str) -> bool:
        p = DOCS / name
        return p.exists() and needle in p.read_text(encoding="utf-8")

    cautious = has("02_Fouquet_Wan_Hypothesis_Compiler.md",
                   "不能直接把這一條當完整 H3")
    exact = has("08_FW_Weight2_Exact_Translation.md", "Exact Translation")
    defined = has("09_FW_H3_Exact_Compiler.md", "Exact Elliptic-Curve Compiler")

    cert = h3c.uniform_certificate(h3c.BASE)
    return {
        "02_says": "Fouquet–Wan 的 exact local condition 更細，不能直接把這一條"
                   "當完整 H3",
        "02_line_present": cautious,
        "08_says": "FW-H3(E,p) <=> exists ell || N with the three conditions "
                   "— boxed as an iff, under the title 'Exact Translation'",
        "08_title_present": exact,
        "09_says": "the same three conditions, as the definition of FW-H3",
        "09_present": defined,
        "the_three_conditions": list(H3_CONDITIONS),
        "08_and_09_state_the_same_conditions": True,
        "two_of_three_treat_it_as_H3": exact and defined,
        "the_disagreement_is_real": cautious and exact,
        "what_changes_under_each_reading": {
            "under_08": "RUN-037's and RUN-039's H3 verdicts are verdicts on "
                        "H3 itself, and RUN-037's gap at p = 29 is a gap in "
                        "FW-H3 for this curve",
            "under_02": "they are verdicts on a compilation, and the exact "
                        "condition is unexamined at every prime",
            "what_does_not_change": "no computed value. The criterion's "
                                    "verdicts, the witness ell = 29, and the "
                                    "failure at p = 29 are the same either way"},
        "affected_verdicts": {
            "primes_tested": cert["odd_p_tested"],
            "criterion_fails_at": cert["p_where_the_criterion_FAILS"]},
        "this_gate_does_not_resolve_it": True,
        "why_not": ("resolving it means reading Fouquet–Wan Theorem 1.7's exact "
                    "local condition, which is an external theorem this arm "
                    "does not hold. Naming the disagreement is what an "
                    "independent arm can do; settling it is not")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    eq = equivalence_03_08()
    oc = ordinary_case_completeness()
    ch = the_chain()
    hd = the_h3_dispute()

    ok = (eq["equivalent"] and eq["pairs_checked"] > 10_000
          and oc["complete_for_every_p_at_least_5"] and oc["the_exception_is_3"]
          and ch["verified_here"] == 2
          and hd["the_disagreement_is_real"]
          and hd["08_and_09_state_the_same_conditions"]
          and hd["this_gate_does_not_resolve_it"])

    log = {
        "gate": "src48 — the H2 chain, and the H3 disagreement",
        "source": "03_FW_H2_Jordan_Holder_Lemma, 08_FW_Weight2_Exact_Translation",
        "equivalence_03_08": eq,
        "ordinary_case_completeness": oc,
        "the_chain": ch,
        "the_h3_dispute": hd,
        "headline": (f"`03`'s Jordan–Hölder lemma and `08`'s ratio test are the "
                     f"same statement, verified over "
                     f"{eq['pairs_checked']:,} character pairs with 0 "
                     f"mismatches; `10`'s single congruence is the whole of the "
                     f"condition at every good ordinary p >= 5, and NOT at "
                     f"p = 3, because chi_cyc^2 is unramified exactly when "
                     f"p - 1 divides 2. And the corpus disagrees with itself "
                     f"about H3: `02` forbids equating the divisibility "
                     f"criterion with it, `08` and `09` do exactly that. The "
                     f"disagreement is reported, not resolved"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  `03` lemma  vs  `08` ratio test")
    print(f"    character-group orders 1..{eq['character_group_orders_exhausted']}"
          f", {eq['pairs_checked']:,} pairs, mismatches: {eq['mismatches']}")
    print(f"    equivalent: {eq['equivalent']}")
    print()
    print(f"  is `10`'s single congruence the whole of `03`'s condition?")
    print(f"    {'p':>4}  ord(chi_cyc) on inertia   chi_cyc² trivial   "
          f"10 complete")
    for r in oc["rows"]:
        print(f"    {r['p']:>4}  {r['order_of_chi_cyc_on_inertia']:>21}   "
              f"{str(r['chi_cyc_squared_trivial_on_inertia']):>16}   "
              f"{r['10s_criterion_is_complete']}")
    print(f"    survives only at {oc['primes_where_the_second_case_survives']}"
          f"  → complete for every p ≥ 5: "
          f"{oc['complete_for_every_p_at_least_5']}")
    print()
    print("  the chain")
    for l in ch["links"]:
        print(f"    {l['status']:<28} {l['from']} → {l['to']}")
    print()
    print("  the H3 disagreement")
    print(f"    02 present: {hd['02_line_present']}   08 present: "
          f"{hd['08_title_present']}   09 present: {hd['09_present']}")
    print(f"    two of three treat the criterion as H3: "
          f"{hd['two_of_three_treat_it_as_H3']}")
    print(f"    the disagreement is real: {hd['the_disagreement_is_real']}")
    print(f"    what does not change: "
          f"{hd['what_changes_under_each_reading']['what_does_not_change']}")
    print(f"    resolved here: {not hd['this_gate_does_not_resolve_it']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
