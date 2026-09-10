"""Gate 51 — the corpus auditing its own citations, audited.

數學戰士「墜衡」 / AMRAL Research Lab.

`22_Odd_Prime_Source_Audit` and `23_FW_Supersingular_Source_Audit` are the two
places where the corpus checks its own citation chain: each lists the hypotheses
of the theorem it invokes and marks them PASS for 696.e1. Every one of those
hypotheses is either arithmetic this tree has computed or a citation, and
separating the two is the job.

TWO OF THIS ARM'S OWN CONCLUSIONS MOVE.

    RUN-046 reported the corpus disagreeing with itself about whether the
    divisibility criterion IS FW-H3 — `02` forbids the identification, `08` and
    `09` make it — and said resolving it needs FW Theorem 1.7's exact local
    condition, "an external theorem this arm does not hold". `23` QUOTES THAT
    CONDITION. It gives Assumption 3 as: special Steinberg, twist by an
    unramified character sending ell to (-1) ell^{k/2-1}, residual ramified —
    and at weight 2 that is a_ell = -1, which is nonsplit multiplicative. The
    derivation `02` asked for is in the corpus; it is in a document neither `02`
    nor `08` references.

    RUN-047 scored `18`'s first referee item — the exact convention match at the
    nonsplit multiplicative witness — as OPEN because `27` does not address it.
    `23`'s H3 section IS that convention match. The item is addressed, by a
    document RUN-047 did not read.

AND `22` INVOKES A STRONGER PREMISE THAN ITS THEOREM ASKS FOR. Its Important
simplification rests on 「base curve mod-ell image 對所有 ell maximal」, while
Skinner Theorem C asks only that `E_q[p]` be irreducible. RUN-031 refuted
reducibility at every one of Mazur's twelve, so irreducibility holds everywhere;
RUN-036 could certify **maximality** at `ell = 2` and every prime `5 <= ell <=
167` but NOT at 3 — and `22`'s case C is `p = 3`. The audit leans on the one
statement this tree cannot certify at the one prime where it matters, and the
weaker statement its theorem actually needs is certified there.

Usage:  python code/src51_source_audits.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402
import src38_mod_ell_surjectivity as surj                 # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = LOGS / "src51-source-audits.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
MAZUR = (2, 3, 5, 7, 11, 13, 17, 19, 37, 43, 67, 163)
SEARCH = 600


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


def a_at(p: int) -> int:
    return anchor.bad_prime_data(BASE, p)["a_p"]


def valuations() -> dict:
    md = gcd35.multiplicative_data(BASE)
    return {r["p"]: r["n"] for r in md["multiplicative"]}


def case_hypotheses() -> dict:
    """`22`'s four cases, each hypothesis marked computed here or cited."""
    v = valuations()
    rows = [
        {"case": "A — p = q, additive twist (BSTW 9.21(c) via BH 2.9)",
         "hypotheses": [
             {"h": "p >= 5", "verdict": "computed",
              "how": "every member is >= 241 (RUN-032/047)"},
             {"h": "p does not divide 6N", "verdict": "computed",
              "how": "q = 1 (mod 24) and (q/29) = 1 force q coprime to 6N"},
             {"h": "p good ordinary for the base", "verdict": "computed",
              "how": "RUN-018: inertness in the 2-division cubic makes a_q odd, "
                     "so a_q != 0 and q is ordinary"},
             {"h": "rho-bar_{E,p} irreducible", "verdict": "computed",
              "how": "RUN-031 refuted a rational p-isogeny at every Mazur "
                     "degree; RUN-036 refuted the Borel at 38 primes"},
             {"h": "(ramK): some ell || N, ell not dividing D_K, residually "
                   "ramified", "verdict": "computed",
              "how": f"ell = 29 with v_29(Delta) = {v.get(29)}, and 29 does not "
                     f"divide D_K = q for any member"}]},
        {"case": "B — good ordinary p (Skinner Theorem C)",
         "hypotheses": [
             {"h": "p >= 3", "verdict": "computed", "how": "by branch"},
             {"h": "good ordinary", "verdict": "computed",
              "how": "RUN-038 classified every good prime below 6,000"},
             {"h": "E_q[p] irreducible", "verdict": "computed",
              "how": "RUN-031 + RUN-036's Borel refutations, and the twist "
                     "tensors a character (RUN-035's lemma A shadow)"},
             {"h": "another multiplicative ell residually ramified",
              "verdict": "computed",
              "how": f"ell = 29, p != 29, p does not divide v_29(Delta) = "
                     f"{v.get(29)}"},
             {"h": "L(E_q,1) != 0", "verdict": "cited + computed for members",
              "how": "Theorem 2.14 in general; RUN-015/016 computed it for the "
                     "members it reached"}]},
        {"case": "C — multiplicative p = 3 (Skinner Theorem C)",
         "hypotheses": [
             {"h": "Skinner C states p >= 3 explicitly", "verdict": "cited",
              "how": "a reading of the theorem's statement, not arithmetic"},
             {"h": "witness ell = 29", "verdict": "computed",
              "how": f"v_29(Delta) = {v.get(29)}, and 3 does not divide it"}]},
        {"case": "D — multiplicative p = 29 (Skinner Theorem C)",
         "hypotheses": [
             {"h": "witness ell = 3", "verdict": "computed",
              "how": f"v_3(Delta) = {v.get(3)}, and 29 does not divide it"},
             {"h": "the witness must be distinct from p", "verdict": "computed",
              "how": "RUN-033's leave-one-out; the control at RUN-048 shows "
                     "what a curve without a second reservoir does"}]},
    ]
    counts = {}
    for r in rows:
        for h in r["hypotheses"]:
            counts[h["verdict"]] = counts.get(h["verdict"], 0) + 1
    return {"rows": rows, "verdict_counts": counts,
            "total_hypotheses": sum(len(r["hypotheses"]) for r in rows)}


def maximal_versus_irreducible() -> dict:
    """`22`'s simplification asks for more than Skinner C does.

    「base curve mod-ell image 對所有 ell maximal」 is the premise; irreducibility
    is what the theorem lists. RUN-031 settles irreducibility everywhere by
    Mazur's theorem plus twelve refutations. RUN-036 settles MAXIMALITY at
    ell = 2 and every prime 5 <= ell <= 167, and cannot at ell = 3 — where two
    obstructions are structural, not a short search. `22`'s case C is p = 3.
    """
    log = _load("src38-mod-ell-surjectivity.json") or {}
    certified = set(log.get("certified_surjective") or [])
    three = log.get("ell_3") or {}
    primes = mz.small_primes(SEARCH)
    irreducible = []
    for n in MAZUR:
        if n == 2:
            irreducible.append({"n": 2, "irreducible": True,
                                "how": "X_0(2), RUN-007 (the sieve is vacuous "
                                       "at 2)"})
        else:
            w = mz.witness(BASE, n, primes)
            irreducible.append({"n": n, "irreducible": w is not None,
                                "witness": w["ell"] if w else None,
                                "how": "reducibility sieve, RUN-031"})
    return {"the_premise": "base curve mod-ell image maximal for all ell",
            "what_Skinner_C_lists": "E_q[p] irreducible",
            "irreducible_at_every_Mazur_degree":
                all(r["irreducible"] for r in irreducible),
            "irreducibility_rows": irreducible,
            "maximality_certified_at": sorted(certified),
            "maximality_certified_count": len(certified),
            "maximality_NOT_certified_at_3": 3 not in certified,
            "why_not_at_3": three.get("scope"),
            "borel_refuted_at_3": bool((three.get("witnesses") or {}).get("borel")),
            "22_case_C_is_p_equals_3": True,
            "reading": ("the audit leans on maximality, which this tree cannot "
                        "certify at 3, at the one case that IS 3. The weaker "
                        "premise Skinner C actually lists — irreducibility — is "
                        "certified there, by RUN-031's witness and RUN-036's "
                        "Borel refutation. Nothing is wrong with the conclusion; "
                        "the stated reason is stronger than the one available")}


def h3_convention() -> dict:
    """`23`'s H3, which is the convention `18` asked a referee to check.

    It refuses to guess — 不用自行猜 representation normalization — and quotes
    FW's Assumption 3 as: special Steinberg, twist by an unramified character
    sending ell to (-1) ell^{k/2-1}, residual ramified. At weight 2 the exponent
    is 0 and the value is -1, so a_ell = -1: nonsplit multiplicative. That last
    step is arithmetic and is checked here.
    """
    v = valuations()
    a29, a3 = a_at(29), a_at(3)
    r29 = tate.reduction_data(BASE, 29, want_c=True)
    r3 = tate.reduction_data(BASE, 3, want_c=True)
    return {"FW_assumption_3_as_23_states_it": [
                "local automorphic representation special Steinberg",
                "twist by an unramified character taking ell to "
                "(-1) ell^{k/2-1}",
                "residual representation ramified"],
            "weight_2_specialisation": "(-1) ell^0 = -1, so a_ell = -1",
            "a_29": a29, "a_3": a3,
            "29_is_nonsplit": r29.get("split_multiplicative") is False,
            "3_is_split": r3.get("split_multiplicative") is True,
            "a_29_equals_minus_1": a29 == -1,
            "the_specialisation_checks_out": a29 == -1 and r29.get(
                "split_multiplicative") is False,
            "the_other_multiplicative_prime_has_a_plus_1": a3 == 1,
            "why_that_matters": ("a_ell = -1 picks out exactly the nonsplit "
                                 "prime, and 3 with a_3 = +1 is the split one "
                                 "the criterion must exclude. The weight-2 sign "
                                 "is doing real work"),
            "residual_ramification": {
                "v_29_Delta": v.get(29),
                "any_odd_p_not_29_keeps_it_ramified": v.get(29) == 1},
            "local_twist_trivial_at_29": ("admissible q have 29 split in "
                                          "Q(sqrt q), which RUN-035 measured on "
                                          "19 of 19 members"),
            "still_cited": ("that FW's Assumption 3 IS that triple is `23`'s "
                            "reading of the paper. This gate checks its "
                            "weight-2 arithmetic, not the reading")}


def what_moves() -> dict:
    """The two conclusions of this arm that `23` changes."""
    def has(name: str, needle: str) -> bool:
        p = DOCS / name
        return p.exists() and needle in p.read_text(encoding="utf-8")
    quoted = has("23_FW_Supersingular_Source_Audit.md",
                 "不用自行猜 representation normalization")
    return {
        "RUN_046": {
            "said": "the corpus disagrees about whether the divisibility "
                    "criterion IS H3, and resolving it needs FW Theorem 1.7's "
                    "exact local condition, which this arm does not hold",
            "what_23_supplies": "the exact condition, quoted, with the weight-2 "
                                "specialisation that produces the criterion",
            "the_quote_is_present": quoted,
            "so": "the derivation `02` asked for is IN the corpus, in a "
                  "document neither `02` nor `08` references. The disagreement "
                  "is between `02` and `08` as written; `23` is the missing "
                  "link and RUN-046 did not have it",
            "still_cited": "whether FW says what `23` says it says"},
        "RUN_047": {
            "said": "`18`'s item 1 — exact convention match at the nonsplit "
                    "multiplicative witness — is OPEN, because `27` does not "
                    "address it",
            "what_23_supplies": "`23`'s H3 section IS that convention match",
            "so": "the item is ADDRESSED, by a document RUN-047 did not read. "
                  "The scoring was right about `27` and wrong about the corpus",
            "corrected_count": {"addressed": 2, "deferred": 1, "open": 2}},
        "both_corrections_are_from_reading_further":
            "neither is an arithmetic error; both are this arm scoring a corpus "
            "it had not finished reading",
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    cases = case_hypotheses()
    mvi = maximal_versus_irreducible()
    h3 = h3_convention()
    mv = what_moves()

    ok = (cases["total_hypotheses"] >= 12
          and mvi["irreducible_at_every_Mazur_degree"]
          and mvi["maximality_NOT_certified_at_3"]
          and mvi["borel_refuted_at_3"]
          and h3["the_specialisation_checks_out"]
          and h3["the_other_multiplicative_prime_has_a_plus_1"]
          and h3["residual_ramification"]["any_odd_p_not_29_keeps_it_ramified"]
          and mv["RUN_046"]["the_quote_is_present"])

    log = {
        "gate": "src51 — 22 and 23, the corpus's own source audits",
        "source": "22_Odd_Prime_Source_Audit, 23_FW_Supersingular_Source_Audit",
        "curve": BASE, "conductor": N,
        "case_hypotheses": cases,
        "maximal_versus_irreducible": mvi,
        "h3_convention": h3,
        "what_moves_in_this_arms_own_conclusions": mv,
        "headline": ("`23` quotes the exact local condition RUN-046 said this "
                     "arm did not hold, and its weight-2 specialisation "
                     "a_ell = -1 checks out — a_29 = -1 and nonsplit, a_3 = +1 "
                     "and split. That resolves the `02`/`08` seam inside the "
                     "corpus and addresses `18`'s first referee item, which "
                     "RUN-047 scored open. And `22`'s Important simplification "
                     "invokes maximality where Skinner C lists irreducibility — "
                     "the stronger premise is the one this tree cannot certify "
                     "at 3, and case C is p = 3"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  22's four cases — {cases['total_hypotheses']} hypotheses, "
          f"{cases['verdict_counts']}")
    for r in cases["rows"]:
        print(f"    {r['case']}")
        for h in r["hypotheses"]:
            print(f"      {h['verdict']:<26} {h['h'][:50]}")
    print()
    print("  22's simplification asks for more than Skinner C lists")
    print(f"    premise stated : {mvi['the_premise']}")
    print(f"    theorem lists  : {mvi['what_Skinner_C_lists']}")
    print(f"    irreducible at every Mazur degree: "
          f"{mvi['irreducible_at_every_Mazur_degree']}")
    print(f"    maximality certified at {mvi['maximality_certified_count']} "
          f"primes; at 3: {not mvi['maximality_NOT_certified_at_3']}   "
          f"Borel refuted at 3: {mvi['borel_refuted_at_3']}")
    print(f"    and 22's case C is p = 3")
    print()
    print("  23's H3 convention, and its weight-2 arithmetic")
    for line in h3["FW_assumption_3_as_23_states_it"]:
        print(f"    · {line}")
    print(f"    weight 2 → {h3['weight_2_specialisation']}")
    print(f"    a_29 = {h3['a_29']} (nonsplit: {h3['29_is_nonsplit']})   "
          f"a_3 = {h3['a_3']} (split: {h3['3_is_split']})")
    print(f"    the specialisation checks out: "
          f"{h3['the_specialisation_checks_out']}")
    print()
    print("  what moves in this arm's own conclusions")
    print(f"    RUN-046: {mv['RUN_046']['so'][:96]}…")
    print(f"    RUN-047: item 1 is ADDRESSED, not open → corrected counts "
          f"{mv['RUN_047']['corrected_count']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
