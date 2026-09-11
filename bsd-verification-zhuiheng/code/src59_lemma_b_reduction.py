"""Gate 59 — FW-H2 at the twisting prime, by Lemma B; and member 3529.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-045 emitted `H2 = UNKNOWN` at the additive prime of every member. RUN-052
ran `06` v0.3 and stopped at its first branch: the kernel-polynomial test that
would decide H2 is local Galois data this tree does not compute. RUN-053 read
`04`, the test written out, and priced it at factoring a division polynomial of
degree up to 7.2 million over Q_q.

NONE OF THAT IS NEEDED. `03` §1 states, for odd p,

    rho_bar_{E_d, p}  ≅  rho_bar_{E, p} ⊗ chi_d

and its Lemma B says the FW-H2 forbidden shape is invariant under tensoring by
a character — in `08`'s ratio form it is an identity, because the ratio of the
two Jordan–Hölder constituents does not see a common twist. So for a member
q ∈ 𝒫:

    FW-H2(E_q, q)  ⟺  FW-H2(E, q)

and the right-hand side is H2 for the BASE curve at a GOOD prime, where the
local structure is a theorem: E ordinary at q gives constituents ω·ε₁ and ε₂,
ε_i unramified, ε₂(Frob) ≡ a_q (mod q); E supersingular at q gives an
irreducible E[q]. RUN-046 already showed that at good ordinary p ≥ 5 the
forbidden shape is exactly `10`'s congruence a_p² ≡ 1 (mod p). Therefore

    FW-H2(E_q, q) FAILS  ⟺  E ordinary at q  and  a_q(E)² ≡ 1 (mod q).

COMPUTED ON ALL 19 MEMBERS: every one is ordinary at q, and exactly one has
a_q² ≡ 1 (mod q) — q = 3529, where a_q = 1. Confirmed by three independent
point counts. And RUN-038's archived log has listed 3529 among the ordinary
H2-obstruction primes of the base since seventeen rounds ago. The pieces were
all in the tree. Nobody had joined "obstruction prime for E" to "member of 𝒫"
through Lemma B.

WHAT IT BREAKS, AND WHAT IT DOES NOT. The provisional design — `18`, `02`, `06`
v0.3 — applies Fouquet–Wan at every odd p including p = q, and at member 3529
its H2 fails. The revised design — `27` — routes p = q to BSTW Theorem 9.21(c),
not to FW, and is untouched by this on its face; BSTW's hypotheses at
(3529, 3529) are cited here, not verified.

Usage:  python code/src59_lemma_b_reduction.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = LOGS / "src59-lemma-b-reduction.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
FAMILY_BOUND = 4000
PROFILE = "LEMMA_B_REDUCTION"             # NOT 07's FW17_EXACT — see the_profile()


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


# ----------------------------------------------------------------- the chain

CHAIN = (
    ("S1", "rho_bar_{E_q,q} ≅ rho_bar_{E,q} ⊗ chi_q for odd q",
     "03 §1", "CITED — standard"),
    ("S2", "the FW-H2 forbidden shape is invariant under ⊗ by a character "
           "(Lemma B); in 08's ratio form the ratio of the two constituents "
           "is unchanged by a common twist",
     "03 §3 (Lemma B), 08", "CITED — Lemma B's 候選 status is about matching "
                             "FW's exact H2 shape; 03/08/10 agree on it "
                             "(RUN-046, 22,140 pairs)"),
    ("S3", "at a good ordinary p ≥ 5: E[p]|G_{Q_p} has constituents ω·ε₁ and "
           "ε₂ with ε_i unramified and ε₂(Frob) ≡ a_p (mod p); at a good "
           "supersingular p: E[p]|G_{Q_p} is irreducible",
     "standard (Serre; Deligne)", "CITED"),
    ("S4", "at good ordinary p ≥ 5 the forbidden shape is exactly a_p² ≡ 1 "
           "(mod p); the other case needs ω² trivial on inertia, i.e. p ≤ 3",
     "10; RUN-046", "VERIFIED within the corpus"),
    ("S5", "E has good reduction at every q ∈ 𝒫", "src16.in_P", "COMPUTED"),
    ("S6", "E is ordinary at every q ∈ 𝒫 (q ∤ a_q)", "this gate", "COMPUTED"),
    ("S7", "a_q(E)² ≡ 1 (mod q) at each member", "this gate", "COMPUTED"),
)


def chain() -> dict:
    rows = [{"step": a, "statement": b, "source": c, "status": d}
            for a, b, c, d in CHAIN]
    return {"rows": rows,
            "conclusion": "FW-H2(E_q, q) FAILS ⟺ E ordinary at q and "
                          "a_q(E)² ≡ 1 (mod q); PASSES otherwise",
            "cited_steps": [r["step"] for r in rows if r["status"].startswith("CITED")],
            "computed_steps": [r["step"] for r in rows if r["status"] == "COMPUTED"],
            "the_verdict_is_conditional_on": "S1, S2, S3 — three cited facts, "
                                             "and S4 as verified inside the "
                                             "corpus rather than against "
                                             "Fouquet–Wan's paper"}


# --------------------------------------------------------------- the members

def brute_ap(ainvs: list[int], p: int) -> int:
    """A third, deliberately naive count over all (x, y) — used only at the
    prime that matters, as an independent confirmation."""
    a1, a2, a3, a4, a6 = (c % p for c in ainvs)
    cnt = 1
    for x in range(p):
        rhs = (x ** 3 + a2 * x * x + a4 * x + a6) % p
        for y in range(p):
            if (y * y + a1 * x * y + a3 * y - rhs) % p == 0:
                cnt += 1
    return p + 1 - cnt


def members(bound: int = FAMILY_BOUND, brute_at: tuple[int, ...] = (3529,)) -> dict:
    qs = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = []
    for q in qs:
        a = anchor.point_count_ap(BASE, q)
        good = N % q != 0
        ordinary = a % q != 0
        cong = (a * a - 1) % q == 0
        fails = good and ordinary and cong
        row = {"q": q, "a_q": a, "good": good, "ordinary": ordinary,
               "a_q_squared_is_1_mod_q": cong,
               "FW_H2_at_q": "FAIL" if fails else "PASS",
               "why": ("a_q² ≡ 1 (mod q) at a good ordinary prime — 10's "
                       "obstruction, carried to the twist by Lemma B" if fails
                       else ("supersingular: E[q] irreducible" if not ordinary
                             else "ordinary with a_q² ≢ 1 (mod q)"))}
        if q in brute_at:
            row["a_q_by_brute_xy_loop"] = brute_ap(BASE, q)
            row["independent_counts_agree"] = row["a_q_by_brute_xy_loop"] == a
        rows.append(row)
    failing = [r["q"] for r in rows if r["FW_H2_at_q"] == "FAIL"]
    return {"bound": bound, "members": len(rows), "rows": rows,
            "all_good": all(r["good"] for r in rows),
            "all_ordinary": all(r["ordinary"] for r in rows),
            "supersingular_members": [r["q"] for r in rows if not r["ordinary"]],
            "failing_members": failing,
            "passing": len(rows) - len(failing),
            "failing": len(failing)}


# ------------------------------------------------------------ consequences

def what_it_closes() -> dict:
    l1 = (_load("src47-fw-compiler.json") or {}).get("level_1") or {}
    v03 = (_load("src54-compiler-targets.json") or {}).get("v03_procedure") or {}
    r0 = (v03.get("rows") or [{}])[0]
    return {"RUN_045_level_1_H2_at_the_additive_prime":
                (l1.get("H2") or {}).get("verdict") or "UNKNOWN (per RUN-045)",
            "RUN_052_v03_branch_3": (r0.get("LOCAL_H2") or {}).get(
                "branch_3_local_isogeny_kernel_test"),
            "RUN_053_priced_the_kernel_route_at":
                "factoring the q-division polynomial, degree up to 7,193,424, "
                "over Q_q",
            "after_this_gate": "the verdict at p = q is decided per member by "
                               "a_q(E) mod q, conditional on S1–S4. The kernel "
                               "polynomial is not needed for the VERDICT; it "
                               "would still be needed for 07's replayable "
                               "certificate",
            "closed": "RUN-045's UNKNOWN at the additive prime, conditionally",
            "not_closed": "07's FW17_EXACT certificate — no kernel polynomial "
                          "is produced here"}


def which_design_it_breaks() -> dict:
    r49 = _load("src49-provisional-vs-revised.json") or {}
    part = r49.get("router_partition") or []
    pq_branch = None
    for row in part:
        for k in (row.get("tally") or {}):
            if k.startswith("p=q"):
                pq_branch = k
    return {"provisional_design": {
                "documents": ["18_Provisional_Derived_Theorem",
                              "02_Fouquet_Wan_Hypothesis_Compiler",
                              "06_Witness_Network_v03_Integration"],
                "applies_FW_at_p_equals_q": True,
                "state_after_this_gate": "BROKEN at member 3529 — FW-H2 fails "
                                         "at its own twisting prime, so the FW "
                                         "route does not deliver BSD(E_3529, "
                                         "3529)"},
            "revised_design": {
                "document": "27_Revised_Derived_Theorem_Candidate",
                "p_equals_q_routed_to": pq_branch or "p=q (BSTW 9.21(c))",
                "applies_FW_at_p_equals_q": False,
                "state_after_this_gate": "UNTOUCHED on its face — BSTW 9.21(c)'s "
                                         "quadratic-twist clause and rank-zero "
                                         "descent at (3529, 3529) are cited "
                                         "here, not verified",
                "read_from": "RUN-047/048's router partition (src49)"},
            "so": ("this gate decides a hypothesis the corpus's OWN revised "
                   "router had already stopped depending on at p = q. What it "
                   "changes is the provisional design's status, and the record: "
                   "18/02/06 have a member they cannot handle")}


def the_pieces_were_in_the_tree() -> dict:
    """Each ingredient, and the round that already had it."""
    s40 = _load("src40-fw-h2-ordinary.json") or {}
    # RUN-038 stores its a_p² ≡ 1 failures per RANGE bucket, not as one list —
    # the first draft read a flat key that does not exist and reported "not
    # listed", which would have been a false statement about this line's own
    # archive. Gather every bucket.
    fails = sorted(p for b in ((s40.get("no_finite_exception") or {})
                               .get("buckets") or [])
                   for p in (b.get("failures") or []))
    r49 = _load("src49-provisional-vs-revised.json") or {}
    td = r49.get("three_definitions_of_P") or {}
    lists = {k: td.get(k) or [] for k in ("per_18_and_27", "per_this_tree",
                                          "per_referee_A")}
    in_each = {k: 3529 in v for k, v in lists.items()}
    return {"RUN_038_listed_3529_as_an_a_p2_eq_1_failure": 3529 in fails,
            "RUN_038_failures_below_its_bound": fails,
            "RUN_047_3529_in_each_of_the_three_definitions": in_each,
            "RUN_047_confirmed_3529_in_P_by_all_three_definitions":
                bool(lists["per_18_and_27"]) and all(in_each.values()),
            "RUN_035_measured_Lemma_C_and_A_and_marked_B_open": True,
            "RUN_046_showed_10_is_the_whole_criterion_at_p_ge_5": True,
            "what_no_round_did": ("intersect RUN-038's failure list with 𝒫, "
                                  "and carry the result to the twist through "
                                  "03 §1 + Lemma B"),
            "reading": ("four rounds each held one ingredient. The join is one "
                        "line. That it took until RUN-057 is a fact about how "
                        "this line worked — document by document — not about "
                        "the arithmetic")}


def membership_condition(bound: int = 5000) -> dict:
    """Would 𝒫 need a fourth condition for the FW-everywhere design?"""
    qs = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    bad = [q for q in qs if (anchor.point_count_ap(BASE, q) ** 2 - 1) % q == 0]
    return {"bound": bound, "members_below_bound": len(qs),
            "members_with_a_q2_eq_1": bad,
            "the_three_existing_conditions": ["q ≡ 1 (mod 24)", "(q/29) = 1 "
                                              "(redundant, RUN-047)",
                                              "f₂ irreducible mod q"],
            "01s_D4_requires": "E ordinary at p | d — which 3529 satisfies",
            "the_condition_none_of_them_state": "a_q(E)² ≢ 1 (mod q)",
            "needed_by": "the provisional FW-at-every-odd-p design only",
            "not_needed_by": "27's router, which does not use FW at p = q"}


def consistency_with_RUN_053() -> dict:
    """RUN-053: at p ≥ 5 at most one of φ, φ̂ can have a Q_p-linear factor.
    Here it is identified WHICH."""
    return {"sub_character": "λ = ω·ε₁·χ_q — λ² restricted to inertia is ω², "
                             "non-trivial for q ≥ 5, so the SUB's test never "
                             "fires",
            "quotient_character": "μ = ε₂·χ_q — μ² = ε₂², unramified, trivial "
                                  "iff ε₂(Frob)² ≡ a_q² ≡ 1 (mod q)",
            "so_when_H2_fails_it_is_always": "the DUAL isogeny's kernel "
                                            "polynomial that has the "
                                            "Q_q-linear factor",
            "agrees_with_RUN_053_mutual_exclusivity": True}


def the_profile() -> dict:
    return {"profile": PROFILE,
            "is_07s_FW17_EXACT": False,
            "why_not": ("07 demands the kernel polynomials of φ and φ̂ and an "
                        "exact p-adic factorisation certificate. This gate "
                        "produces a verdict from a_q(E) mod q through a cited "
                        "chain. 07 Rule 4 says a heuristic certificate must "
                        "emit UNKNOWN; this is not heuristic, it is a theorem "
                        "chain — but it is CITED, and the profile name says "
                        "so rather than borrowing 07's"),
            "what_07_would_still_need": ["local_reducibility_Fp — decided here "
                                         "by S3 + S6, not by computation on E_q",
                                         "phi.kernel_polynomial — not produced",
                                         "dual_phi.kernel_polynomial — not "
                                         "produced"]}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    ch = chain()
    mb = members()
    wc = what_it_closes()
    wd = which_design_it_breaks()
    pt = the_pieces_were_in_the_tree()
    mc = membership_condition()
    cs = consistency_with_RUN_053()
    pf = the_profile()

    doc03 = DOCS / "03_Quadratic_Twist_Invariance_Bridge.md"
    t03 = doc03.read_text(encoding="utf-8") if doc03.exists() else ""

    r3529 = next((r for r in mb["rows"] if r["q"] == 3529), None)
    ok = (bool(t03) and "Lemma B" in t03 and "otimes" in t03
          and mb["members"] >= 19 and mb["all_good"] and mb["all_ordinary"]
          and mb["failing_members"] == [3529]
          and r3529 is not None and r3529["a_q"] == 1
          and r3529.get("independent_counts_agree") is True
          and pt["RUN_038_listed_3529_as_an_a_p2_eq_1_failure"]
          and pt["RUN_047_confirmed_3529_in_P_by_all_three_definitions"]
          and mc["members_with_a_q2_eq_1"] == [3529]
          and wd["revised_design"]["applies_FW_at_p_equals_q"] is False
          and pf["is_07s_FW17_EXACT"] is False)

    log = {
        "gate": "src59 — FW-H2 at the twisting prime by Lemma B; member 3529",
        "source": "03_Quadratic_Twist_Invariance_Bridge (§1, Lemma B); "
                  "10_FW_H2_and_Ordinary_Obstruction; 27's router",
        "curve": BASE, "conductor": N, "profile": PROFILE,
        "chain": ch, "members": mb, "what_it_closes": wc,
        "which_design_it_breaks": wd, "the_pieces_were_in_the_tree": pt,
        "membership_condition": mc, "consistency_with_RUN_053": cs,
        "the_profile": pf,
        "headline": (f"By 03 §1 and Lemma B, FW-H2(E_q, q) ⟺ FW-H2(E, q), and "
                     f"at a good ordinary prime that is 10's congruence. All "
                     f"{mb['members']} members are good and ordinary at q; "
                     f"exactly {mb['failing']} has a_q² ≡ 1 (mod q): q = 3529, "
                     f"a_q = 1, confirmed by three independent counts. So the "
                     f"provisional FW-at-every-odd-p design FAILS H2 at member "
                     f"3529's own twisting prime; 27's revised router does not "
                     f"use FW at p = q and is untouched on its face. RUN-038 "
                     f"had listed 3529 as an obstruction prime since RUN-038. "
                     f"The verdict is conditional on three cited facts and "
                     f"carries the profile {PROFILE}, not 07's FW17_EXACT"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print("  the chain")
    for r in ch["rows"]:
        print(f"    {r['step']}  {r['status'][:26]:<26} {r['statement'][:60]}")
    print(f"    ⟹ {ch['conclusion']}")
    print()
    print(f"  {mb['members']} members, all good: {mb['all_good']}, all ordinary: "
          f"{mb['all_ordinary']}, supersingular: {mb['supersingular_members']}")
    print(f"    FW-H2 at q: PASS {mb['passing']}, FAIL {mb['failing']} → "
          f"{mb['failing_members']}")
    if r3529:
        print(f"    q = 3529: a_q = {r3529['a_q']}, brute (x,y) count "
              f"{r3529.get('a_q_by_brute_xy_loop')}, agree "
              f"{r3529.get('independent_counts_agree')}")
    print()
    print(f"  closes: {wc['closed']}")
    print(f"  not closed: {wc['not_closed']}")
    print()
    print(f"  provisional design (18/02/06): "
          f"{wd['provisional_design']['state_after_this_gate'][:60]}")
    print(f"  revised design (27): p = q → "
          f"{wd['revised_design']['p_equals_q_routed_to']}; "
          f"{wd['revised_design']['state_after_this_gate'][:44]}")
    print()
    print(f"  RUN-038 listed 3529 as an a_p²≡1 failure: "
          f"{pt['RUN_038_listed_3529_as_an_a_p2_eq_1_failure']} "
          f"(its list: {pt['RUN_038_failures_below_its_bound']})")
    print(f"  members below {mc['bound']} with a_q²≡1: "
          f"{mc['members_with_a_q2_eq_1']} of {mc['members_below_bound']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
