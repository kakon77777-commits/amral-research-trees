"""Gate 34 — Referee A's checklist, run as a program.

數學戰士「墜衡」 / AMRAL Research Lab.

`19_Independent_Referee_Handoff` opens by saying what it wants:

    不要再搜尋更多 curves。先嘗試推翻: 696.e1 family theorem.

and hands Referee A a checklist with an explicit instruction — 輸出 PASS/FAIL.
Seven lines about the base curve and five about a symbolic `q ∈ 𝒫`. Most of
them are machine-checkable, and eleven rounds of this arm have checked them one
at a time in other contexts. This runs the checklist **as the checklist**, in
its own order, and produces the PASS/FAIL it asks for.

WHAT IS AND IS NOT MACHINE-CHECKABLE, SEPARATED RATHER THAN SCORED TOGETHER.
Three of the base lines are not arithmetic this arm can settle:

    optimal                   an isogeny-class statement. RUN-031 closed its
                              premise — no rational n-isogeny at any of Mazur's
                              twelve degrees — but optimality also asks which
                              curve the modular parametrisation lands on, and
                              that is not computed here.
    odd Manin                 the Manin constant. Cited, in `24_Manin_Period_Audit`
                              and in RUN-030's certificate.
    BSD(E,2) rigorous source  a citation to the verification of BSD to conductor
                              5000, which is a source and not a computation.

The other four base lines and all five `q` lines are run. A checklist that
scored the cited lines as PASS would be reporting a citation as a check.

Usage:  python code/src34_referee_a_checklist.py
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src10_phase2_density_and_base as ph2               # noqa: E402
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src34-referee-a.json"

BASE = [0, 1, 0, 8, -16]
N = 696
Q_BOUND = 4000
TERMS = 20_000


def base_checklist(limit: int = TERMS) -> list[dict]:
    """Referee A's seven base lines, in the order the document lists them."""
    b2, b4, b6, b8, disc = anchor.b_invariants(BASE)
    res = anchor.analyse("696.e1", BASE, N, limit=limit)
    ratio = (res["L_at_1"] / res["real_period"]
             if res["L_at_1"] and res["real_period"] else None)
    # v_2(L^alg) with L^alg = L/Omega: 0 exactly when L/Omega is an odd integer
    v2 = (0 if ratio is not None and abs(ratio - round(ratio)) < 1e-9
          and round(ratio) % 2 == 1 else None)
    # E(Q)[2] = 0 is the absence of a rational 2-torsion point, i.e. the
    # 2-division cubic 4x^3 + b2 x^2 + 2 b4 x + b6 has no rational root.
    two_torsion = any(
        4 * x ** 3 + b2 * x * x + 2 * b4 * x + b6 == 0 for x in range(-200, 201))
    return [
        {"line": "optimal", "machine_checkable": False,
         "status": "cited",
         "note": "RUN-031 closed its premise (no rational n-isogeny at any of "
                 "Mazur's twelve), but which curve the modular parametrisation "
                 "lands on is not computed here"},
        {"line": "odd Manin", "machine_checkable": False, "status": "cited",
         "note": "the Manin constant, from 24_Manin_Period_Audit"},
        {"line": "analytic rank 0", "machine_checkable": True,
         "measured": 0 if res["analytic_rank_is_zero"] else None,
         "status": "PASS" if res["analytic_rank_is_zero"] else "FAIL",
         "from": "RUN-014, recomputed here"},
        {"line": "BSD(E,2) rigorous source", "machine_checkable": False,
         "status": "cited",
         "note": "the verification of BSD to conductor 5000; a source, not a "
                 "computation"},
        {"line": "E(Q)[2]=0", "machine_checkable": True,
         "measured": "no rational root of the 2-division cubic"
                     if not two_torsion else "a rational 2-torsion point exists",
         "status": "PASS" if not two_torsion else "FAIL",
         "from": "the 2-division cubic, and RUN-007's X_0(2) independently"},
        {"line": "Delta<0", "machine_checkable": True, "measured": disc,
         "status": "PASS" if disc < 0 else "FAIL", "from": "RUN-014"},
        {"line": "v2(Lalg)=0", "machine_checkable": True,
         "measured": v2, "status": "PASS" if v2 == 0 else "FAIL",
         "from": "L/Omega = 1 (RUN-014); ord_2(1) = 0",
         "note": "L^alg here is L(E,1)/Omega, the reading RUN-018 and RUN-020 "
                 "used"},
    ]


def q_checklist(q: int) -> dict:
    """Referee A's five conditions on a member of the support set."""
    sf = all((q % (p * p)) for p in range(2, int(q ** 0.5) + 1))
    g = 1
    a, b = q, N
    while b:
        a, b = b, a % b
    g = a
    splits = {}
    for ell in (2, 3, 29):
        if ell == 2:
            splits[ell] = q % 8 == 1
        else:
            splits[ell] = ph2.legendre(q, ell) == 1
    inert = ph2.cubic_root_count(ph2.F2, q) == 0
    lines = {
        "squarefree": sf,
        "gcd(q,696)=1": g == 1,
        "q mod 4 = 1": q % 4 == 1,
        "2,3,29 split in Q(sqrt(q))": all(splits.values()),
        "q inert in 2-division cubic": inert,
    }
    return {"q": q, "lines": lines, "all_pass": all(lines.values()),
            "splits": {str(k): v for k, v in splits.items()}}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass
    base = base_checklist()
    checkable = [r for r in base if r["machine_checkable"]]
    cited = [r for r in base if not r["machine_checkable"]]
    base_pass = all(r["status"] == "PASS" for r in checkable)

    members = [q for q in anchor.sieve(Q_BOUND) if fam.in_P(q)]
    rows = [q_checklist(q) for q in members]
    all_members_pass = all(r["all_pass"] for r in rows)
    # and the converse direction: a prime the membership test rejects should
    # fail at least one of Referee A's five, or the two disagree about 𝒫
    rejected = [q for q in anchor.sieve(Q_BOUND)
                if q % 4 == 1 and not fam.in_P(q)][:200]
    rejected_rows = [q_checklist(q) for q in rejected]
    disagreements = [r["q"] for r in rejected_rows if r["all_pass"]]

    log = {
        "gate": "src34 — Referee A's checklist, run",
        "source": "19_Independent_Referee_Handoff, Referee A",
        "curve": BASE,
        "base_checklist": base,
        "base_lines_machine_checkable": len(checkable),
        "base_lines_cited": len(cited),
        "base_verdict": "PASS" if base_pass else "FAIL",
        "base_verdict_scope": ("over the four lines that are arithmetic. The "
                               "three cited lines are reported as cited, not "
                               "scored — a checklist that marked a citation "
                               "PASS would be reporting a source as a check"),
        "support_set": {
            "bound": Q_BOUND,
            "members": len(members),
            "all_members_pass_all_five": all_members_pass,
            "first_members": members[:12],
            "sample": rows[:5],
        },
        "converse_direction": {
            "primes_1_mod_4_rejected_by_the_membership_test": len(rejected_rows),
            "of_those_passing_all_five_of_Referee_As_conditions": disagreements,
            "agree": not disagreements,
            "why_this_matters": ("if a prime the membership test rejects passes "
                                 "Referee A's five, then the checklist and the "
                                 "corpus's own 𝒫 disagree about who is in the "
                                 "family. Checking only the members would never "
                                 "see it"),
        },
        "ok": base_pass and all_members_pass and not disagreements,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print("  Referee A — base curve [0, 1, 0, 8, -16]")
    for r in base:
        mark = ("PASS" if r["status"] == "PASS" else
                "FAIL" if r["status"] == "FAIL" else "cited")
        print(f"    {mark:5s}  {r['line']:26s} {str(r.get('measured', ''))[:28]}")
    print(f"    -> {log['base_verdict']} over the "
          f"{len(checkable)} arithmetic lines; {len(cited)} cited")
    print()
    print(f"  Referee A — support set below {Q_BOUND}: {len(members)} members")
    print(f"    all five conditions on every member: {all_members_pass}")
    print(f"    members: {members[:12]}")
    print()
    cv = log["converse_direction"]
    print(f"  converse: {cv['primes_1_mod_4_rejected_by_the_membership_test']} "
          f"rejected primes tested, "
          f"{len(cv['of_those_passing_all_five_of_Referee_As_conditions'])} "
          f"pass all five → agree: {cv['agree']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if log["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
