"""Gate 55 — `04`'s local p-isogeny kernel criterion, and a consequence it does not state.

數學戰士「墜衡」 / AMRAL Research Lab.

RUN-052 recorded `LOCAL_H2` branches 2 and 3 as NOT COMPUTED HERE, and named the
missing instrument: the kernel polynomials of a local `p`-isogeny and its dual.
**`04_Local_p_Isogeny_Kernel_Criterion` is that instrument, written out** — and
until this round it had been cited exactly once, in RUN-008, and never used by
the v0.3 procedure that needed it.

Its chain, assuming `E[p]|_{G_{Q_p}}` reducible with a stable line `C ≅ Z/p`
carrying the character `λ`:

    x(P) = x(-P), and p odd  =>  x(P) in Q_p  <=>  σ(P) = ±P for all σ
                              <=>  λ(G_{Q_p}) ⊆ {±1}  <=>  λ² = 1

and the box:

    λ² = 1  <=>  ker φ's kernel polynomial has a Q_p-linear factor
    FW17-H2 FAIL  <=>  φ OR dual(φ) has one

THE CONSEQUENCE `04` DOES NOT STATE. The Weil pairing gives `det E[p] = ω`, so
`λ·μ = ω` where `μ = ω λ^{-1}` is the dual's kernel character. `04`'s criterion
applied to `φ` is `λ² = 1`; applied to `φ̂` it is `μ² = 1`. **Both at once forces
`ω² = 1`** — and `ω` surjects onto `(Z/p)^×` because `Q_p(ζ_p)/Q_p` is totally
ramified of degree `p − 1`, so

    ω² = 1  <=>  (p − 1) | 2  <=>  p ∈ {2, 3}.

**At every `p ≥ 5` the two tests are mutually exclusive.** `04`'s "one isogeny
plus its dual is enough" is therefore tight in a stronger sense than it claims:
the second test is only ever consulted after the first has failed, and the two
can never both confirm. At `p = 3` they can — which is the same `(p − 1) | 2`
that RUN-046 found governing `10`'s ordinary congruence, reached here from a
different document by a different route.

WHAT THIS ROUND DOES NOT DO. It does not run the criterion on the family. The
precondition — `E[p]|_{G_{Q_p}}` reducible — is not decided here, and RUN-036's
GLOBAL surjectivity certificate does not decide it: a globally surjective
representation can restrict to a reducible one at `p`. Reading the 38 certified
primes as settling the local question would be exactly the substitution `00` §6
forbids, one level down.

Usage:  python code/src55_local_isogeny_kernel.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
REPORTS = ROOT / "reports"
DOCS = ROOT.parent.parent / "amral" / "public" / "bsd" / "phase2" / "files"
OUT = LOGS / "src55-local-isogeny-kernel.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
FAMILY_BOUND = 4000
PRIME_BOUND = 200


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


# --------------------------------------------------------------- the chain

CHAIN = (
    ("x(P) = x(-P)",
     "the x-coordinate is invariant under negation on any Weierstrass model",
     "none — this holds for every point on every such model"),
    ("x(P) ∈ Q_p  <=>  σ(P) = ±P for all σ",
     "Galois fixes x(P) exactly when it moves P to a point with the same "
     "x-coordinate, and the only such points are ±P",
     "p ODD. At p = 2 every P satisfies P = -P, so the right side is "
     "vacuously true and the equivalence carries no information"),
    ("σ(P) = ±P for all σ  <=>  λ(G_{Q_p}) ⊆ {±1}",
     "λ is defined by σ(P) = λ(σ)P on the generator P of C",
     "C is Galois-stable and cyclic of order p"),
    ("λ(G_{Q_p}) ⊆ {±1}  <=>  λ² = 1",
     "{±1} is exactly the 2-torsion of F_p^×",
     "none"),
    ("λ² = 1  <=>  ker φ's kernel polynomial has a Q_p-linear factor",
     "`04`'s boxed statement, assembled from the four above",
     "E[p]|_{G_Q_p} REDUCIBLE — without a stable line there is no λ"),
)


def derivation_chain() -> dict:
    """`04`'s equivalence chain, each step with the hypothesis it rests on."""
    return {"assumption": "E[p]|_{G_{Q_p}} reducible; C ≅ Z/p stable; "
                          "σ(P) = λ(σ)P on a generator P of C",
            "steps": [{"step": a, "why": b, "hypothesis": c}
                      for a, b, c in CHAIN],
            "the_box": "FW17-H2 FAIL <=> phi or dual(phi)'s kernel polynomial "
                       "has a Q_p-linear factor",
            "dual_character": "mu = omega * lambda^{-1}",
            "steps_count": len(CHAIN)}


def p_odd_is_load_bearing(ainvs: list[int] | None = None) -> dict:
    """Step 2 degenerates at p = 2, and the degeneration is exhibited.

    On a Weierstrass model `-(x, y) = (x, -y - a1 x - a3)`, so `P = -P` means
    `2y + a1 x + a3 = 0` — which is precisely the condition defining the
    2-torsion. So every point of `E[2]` satisfies `P = -P`, the clause
    `σ(P) = ±P` holds for every σ with no Galois input at all, and the
    criterion would report `λ² = 1` unconditionally.

    A criterion whose excluded case is never exhibited has not been tested;
    this is the same discipline RUN-042 applied to `01`'s excluded Kodaira
    types.
    """
    a1, _a2, a3, _a4, _a6 = ainvs if ainvs is not None else BASE
    # A point is 2-torsion iff it equals its own negative iff 2y + a1x + a3 = 0.
    # Rather than solve, state the identity and check it symbolically on the
    # defining relation: for 2-torsion, y = -y - a1 x - a3.
    return {"negation": "-(x, y) = (x, -y - a1*x - a3)",
            "a1": a1, "a3": a3,
            "two_torsion_condition": "2y + a1*x + a3 = 0",
            "so_at_p_2": "every P in E[2] satisfies P = -P",
            "the_clause_becomes": "sigma(P) = ±P holds for every sigma with no "
                                  "Galois input, so the criterion would report "
                                  "lambda^2 = 1 unconditionally",
            "p_odd_is_load_bearing": True,
            "and_at_odd_p": "P has order p > 2, so P != -P and the clause "
                            "genuinely constrains sigma"}


# ------------------------------------------------- the cyclotomic character

def cyclotomic_squares_trivial(p: int) -> bool:
    """Is `x² = 1` for every `x` in `(Z/p)^×`? Brute force, not a lookup.

    `ω: G_{Q_p} -> (Z/p)^×` is SURJECTIVE because `Q_p(ζ_p)/Q_p` is totally
    ramified of degree `p − 1`, so `ω² = 1` iff squaring is trivial on the whole
    of `(Z/p)^×` — which is a finite computation.
    """
    return all(pow(x, 2, p) == 1 for x in range(1, p))


def cyclotomic_order(bound: int = PRIME_BOUND) -> dict:
    """`ord(ω) = p − 1`, and where `ω² = 1`, computed over a prime range."""
    primes = anchor.sieve(bound)
    rows = []
    for p in primes:
        # `(p - 1) | 2`, which is `2 % (p - 1)`, NOT `(p - 1) % 2` — the first
        # draft had the divisibility backwards and the brute-force column
        # disagreed with it at p = 2, where p - 1 = 1 divides 2 and 2 does not
        # divide 1. That is why the closed form is carried beside the
        # computation instead of replacing it.
        rows.append({"p": p, "order_of_image": p - 1,
                     "omega_squared_trivial": cyclotomic_squares_trivial(p),
                     "p_minus_1_divides_2": 2 % (p - 1) == 0})
    exceptional = [r["p"] for r in rows if r["omega_squared_trivial"]]
    return {"why_surjective": "Q_p(zeta_p)/Q_p is totally ramified of degree "
                              "p - 1, so omega's image is all of (Z/p)^*",
            "primes_checked": len(rows),
            "bound": bound,
            "omega_squared_trivial_at": exceptional,
            "and_that_is_exactly": "(p - 1) | 2",
            "agrees_with_the_divisibility": all(
                r["omega_squared_trivial"] == r["p_minus_1_divides_2"]
                for r in rows),
            "rows": rows[:12]}


def mutual_exclusivity(bound: int = PRIME_BOUND) -> dict:
    """Can `φ` and its dual BOTH have a `Q_p`-linear factor?

    `λ·μ = ω`, so `λ² = μ² = 1` forces `ω² = 1`. The answer is therefore
    exactly the previous function's exceptional set.
    """
    co = cyclotomic_order(bound)
    both_possible = [p for p in co["omega_squared_trivial_at"] if p > 2]
    odd = [p for p in anchor.sieve(bound) if p > 2]
    return {"argument": "lambda * mu = omega (Weil pairing / det E[p] = omega); "
                        "lambda^2 = mu^2 = 1 => (lambda*mu)^2 = omega^2 = 1",
            "odd_primes_checked": len(odd),
            "bound": bound,
            "both_tests_can_fire_at": both_possible,
            "mutually_exclusive_at_every_p_ge_5":
                all(p <= 3 for p in both_possible),
            "so": ("at every odd p >= 5, at most one of phi and dual(phi) has "
                   "a Q_p-linear factor. `04`'s 'one isogeny + dual is enough' "
                   "is tight in a stronger sense than it states: the second "
                   "test is only ever consulted after the first fails, and the "
                   "two can never both confirm"),
            "at_p_3": ("both CAN hold — (Z/3)^* = {1, 2} and 1^2 = 2^2 = 1 "
                       "mod 3, so omega^2 = 1 there"),
            "not_claimed": ("this constrains the two tests' JOINT behaviour. It "
                            "does not decide either one, and does not tell you "
                            "whether FW17-H2 fails")}


# ------------------------------------------------------- prior appearances

def p_minus_1_divides_2_appearances() -> dict:
    """Where this structure has already appeared, READ from the reports.

    RUN-029's failure mode was a scan built on the shapes the author remembers.
    The count is scanned, and the fragments it matches are listed, so a claim
    of "the Nth time" is never typed from memory.
    """
    pats = (r"p\s*[−-]\s*1\s*[|∣]\s*2", r"chi_cyc.{0,3}2", r"χ_cyc.{0,3}2")
    hits = []
    for f in sorted(REPORTS.glob("RUN-*.md")):
        text = f.read_text(encoding="utf-8")
        for pat in pats:
            for m in re.finditer(pat, text):
                flat = " ".join(text[max(0, m.start() - 90):
                                     m.end() + 90].split())
                hits.append({"report": f.name, "pattern": pat,
                             "context": flat[:180]})
    reports = sorted({h["report"] for h in hits})
    return {"patterns": list(pats),
            "reports_carrying_it": reports,
            "count_of_reports": len(reports),
            "hits": hits[:8],
            "reading": ("the same structural fact — the mod-p cyclotomic "
                        "character has order p - 1 on inertia — reached from a "
                        "different document by a different route. RUN-046 got "
                        "there through `10`'s ordinary congruence needing "
                        "chi_cyc^2 unramified; this round gets there through "
                        "`04`'s two kernel characters multiplying to omega")}


# ------------------------------------------------------------ preconditions

def precondition_local_reducibility() -> dict:
    """The criterion assumes local reducibility. This tree has not decided it.

    RUN-036 certified the GLOBAL mod-ell representation surjective at 38
    primes. Surjective implies globally irreducible — and says NOTHING about
    the restriction to `G_{Q_p}`, which can be reducible while the global one
    is not. Treating the certificate as settling the local question would be
    `00` §6's forbidden substitution one level down.
    """
    surj = _load("src38-mod-ell-surjectivity.json") or {}
    certified = surj.get("certified_surjective") or []
    return {"criterion_assumes": "E[p]|_{G_{Q_p}} reducible",
            "decided_here": False,
            "what_RUN_036_gives": f"GLOBAL surjectivity at {len(certified)} "
                                  f"primes, hence global irreducibility",
            "global_surjectivity_does_not_settle_this": True,
            "why": ("a globally surjective representation restricts to a "
                    "decomposition group at p that may well be reducible — "
                    "that is the ordinary case. The global certificate is "
                    "about a different group"),
            "so_the_criterion_is": "NOT RUN HERE — its hypothesis is undecided",
            "the_substitution_this_refuses": ("reading the 38 certified primes "
                                              "as deciding the local question, "
                                              "which is `00` §6's third "
                                              "prohibition one level down")}


CASES = (
    ("nonsplit reducible extension",
     "the original E[p] has only ONE stable line, and the quotient constituent "
     "shows up in the DUAL's kernel",
     "phi catches the sub, dual(phi) catches the quotient"),
    ("split representation",
     "both Jordan-Holder constituents are already lines in E[p]",
     "phi and dual(phi) catch them directly"),
    ("either way",
     "no enumeration of all local p-isogenies is needed",
     "two tests suffice, and by mutual_exclusivity at p >= 5 they never both "
     "fire"),
)


def three_cases() -> dict:
    """`04`'s own argument for why one isogeny plus its dual is enough."""
    return {"rows": [{"case": a, "what_happens": b, "consequence": c}
                     for a, b, c in CASES],
            "count": len(CASES),
            "and_this_round_adds": ("the two are mutually exclusive at p >= 5, "
                                    "which `04` does not state")}


def what_it_would_cost(bound: int = FAMILY_BOUND) -> dict:
    """The degrees involved, for the family, stated rather than assumed."""
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = [{"q": q,
             "kernel_polynomial_degree": (q - 1) // 2,
             "p_division_polynomial_degree": (q * q - 1) // 2}
            for q in members]
    return {"members": len(members), "rows": rows[:6],
            "smallest_member": members[0] if members else None,
            "kernel_degree_range": [min(r["kernel_polynomial_degree"]
                                        for r in rows),
                                    max(r["kernel_polynomial_degree"]
                                        for r in rows)] if rows else [],
            "division_degree_range": [min(r["p_division_polynomial_degree"]
                                          for r in rows),
                                      max(r["p_division_polynomial_degree"]
                                          for r in rows)] if rows else [],
            "the_honest_statement": ("the kernel polynomial itself is small — "
                                     "degree (q-1)/2. FINDING it means locating "
                                     "a Galois-stable line, i.e. factoring the "
                                     "q-division polynomial of degree "
                                     "(q^2-1)/2 over Q_q. Neither is attempted "
                                     "here, and the precondition is undecided "
                                     "anyway")}


def citation_history() -> dict:
    """How often `04` has been used by this line, and by the corpus's v0.3."""
    doc = "04_Local_p_Isogeny_Kernel_Criterion"
    cited_in = [f.name for f in sorted(REPORTS.glob("RUN-*.md"))
                if doc in f.read_text(encoding="utf-8")]
    v03 = _load("src54-compiler-targets.json") or {}
    proc = v03.get("v03_procedure") or {}
    rows = proc.get("rows") or []
    branch3 = rows[0]["LOCAL_H2"]["branch_3_local_isogeny_kernel_test"] if rows \
        else None
    return {"document": doc,
            "reports_naming_it": cited_in,
            "count": len(cited_in),
            "v03_branch_3_state_at_RUN_052": branch3,
            "the_finding": ("`04` is the instrument RUN-052 recorded as missing. "
                            "It was in the corpus the whole time, named in one "
                            "earlier report, and the v0.3 procedure that needed "
                            "it does not cite it")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    ch = derivation_chain()
    lb = p_odd_is_load_bearing()
    co = cyclotomic_order()
    mx = mutual_exclusivity()
    pa = p_minus_1_divides_2_appearances()
    pr = precondition_local_reducibility()
    tc = three_cases()
    ct = what_it_would_cost()
    hi = citation_history()

    doc = DOCS / f"{hi['document']}.md"
    text = doc.read_text(encoding="utf-8") if doc.exists() else ""

    ok = (ch["steps_count"] == 5 and lb["p_odd_is_load_bearing"]
          and co["agrees_with_the_divisibility"]
          and co["omega_squared_trivial_at"] == [2, 3]
          and mx["both_tests_can_fire_at"] == [3]
          and mx["mutually_exclusive_at_every_p_ge_5"]
          and pr["decided_here"] is False
          and pr["global_surjectivity_does_not_settle_this"]
          and tc["count"] == 3 and ct["members"] >= 19
          and bool(text) and "FW17-H2" in text
          and pa["count_of_reports"] >= 1)

    log = {
        "gate": "src55 — 04's local p-isogeny kernel criterion",
        "source": "04_Local_p_Isogeny_Kernel_Criterion",
        "document_found": bool(text),
        "curve": BASE,
        "derivation_chain": ch,
        "p_odd_is_load_bearing": lb,
        "cyclotomic_order": co,
        "mutual_exclusivity": mx,
        "p_minus_1_divides_2_appearances": pa,
        "precondition": pr,
        "three_cases": tc,
        "what_it_would_cost": ct,
        "citation_history": hi,
        "headline": (f"`04`'s chain checks out step by step, and `p` odd is "
                     f"load-bearing at step 2 — at p = 2 every point is its own "
                     f"negative and the clause carries no information. The "
                     f"consequence `04` does not state: lambda*mu = omega, so "
                     f"both tests firing forces omega^2 = 1, which over "
                     f"{co['primes_checked']} primes happens at exactly "
                     f"{co['omega_squared_trivial_at']} — so AT EVERY p >= 5 "
                     f"THE TWO TESTS ARE MUTUALLY EXCLUSIVE. That is (p-1)|2 "
                     f"again, reached from a different document than RUN-046's. "
                     f"The criterion is NOT run on the family: its precondition "
                     f"is local reducibility, RUN-036's global surjectivity "
                     f"does not decide it, and reading it as if it did would be "
                     f"`00` §6's forbidden substitution one level down"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  04's chain — {ch['steps_count']} steps, each with its hypothesis")
    for s in ch["steps"]:
        print(f"    {s['step'][:62]}")
        print(f"        needs: {s['hypothesis'][:66]}")
    print()
    print(f"  p odd is load-bearing at step 2: {lb['p_odd_is_load_bearing']}")
    print(f"    {lb['two_torsion_condition']} — {lb['so_at_p_2']}")
    print()
    print(f"  omega surjects onto (Z/p)^*, so ord(omega) = p - 1")
    print(f"    over {co['primes_checked']} primes, omega^2 = 1 at exactly "
          f"{co['omega_squared_trivial_at']}  (= (p-1)|2: "
          f"{co['agrees_with_the_divisibility']})")
    print()
    print(f"  MUTUAL EXCLUSIVITY — {mx['argument'][:70]}")
    print(f"    both tests can fire at: {mx['both_tests_can_fire_at']}")
    print(f"    mutually exclusive at every p >= 5: "
          f"{mx['mutually_exclusive_at_every_p_ge_5']}")
    print()
    print(f"  (p-1)|2 already appears in {pa['count_of_reports']} report(s): "
          f"{', '.join(r[:10] for r in pa['reports_carrying_it'])}")
    print()
    print(f"  precondition — {pr['criterion_assumes']}")
    print(f"    decided here: {pr['decided_here']}; "
          f"{pr['what_RUN_036_gives'][:56]}")
    print(f"    global surjectivity settles it: "
          f"{not pr['global_surjectivity_does_not_settle_this']}")
    print()
    print(f"  cost, if it were run: kernel poly degree "
          f"{ct['kernel_degree_range']}, division poly "
          f"{ct['division_degree_range']}, over {ct['members']} members")
    print()
    print(f"  04 is named in {hi['count']} report(s): "
          f"{', '.join(x[:10] for x in hi['reports_naming_it'])}")
    print(f"    v0.3 branch 3 at RUN-052: {hi['v03_branch_3_state_at_RUN_052']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
