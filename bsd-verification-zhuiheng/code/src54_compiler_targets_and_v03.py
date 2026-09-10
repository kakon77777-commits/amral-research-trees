"""Gate 54 — the next compiler targets, and v0.3's decision procedure run as far as it goes.

數學戰士「墜衡」 / AMRAL Research Lab.

`02_Next_Compiler_Targets` lists four things to build, in order, and puts a
discipline line under the first: **No database scaling until this is exact.**
`06_Witness_Network_v03_Integration` is the answer to that first target — a
decision procedure for a fixed odd additive prime, written as pseudocode, whose
stated improvement is

    A2 H2 UNKNOWN  ->  exact finite local isogeny test.

RUN-045 IS THE UNKNOWN IT NAMES. That round's Level-1 certificate marks H2
`UNKNOWN` at the additive prime, because `05`'s no-go decides only the
potentially multiplicative case and RUN-034 found it silent there. `06` v0.3 is
the procedure that would resolve it.

SO THE PROCEDURE IS RUN, AND IT STOPS WHERE THIS TREE STOPS. Its first branch is
decidable here — every member's odd additive prime is potentially GOOD, measured
at RUN-034, so the `FAIL` branch is not taken. Its second and third are local:
`E[p]` irreducible over `F_p`, and failing that the kernel polynomials of a local
`p`-isogeny and its dual. Neither is arithmetic this tree computes. H3 is
computed, PERIOD is RUN-039's open item, and FINAL is unreachable.

**Two of five steps decided, one partial, two outside this arm.** That is the
honest shape of a procedure whose decisive branch needs local Galois data.

AND ONE OF `02`'s TARGETS HAS AN EMPTY DOMAIN HERE. Target 3 is an ordinary
finite-exception compiler for `p | g_mult`. RUN-033 computed `g_mult^odd = 1`,
which no odd prime divides — so for this curve target 3 has nothing to work on.
That is not progress on the target; it is the target being inapplicable, which
is a different thing and is reported as one.

Usage:  python code/src54_compiler_targets_and_v03.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src16_twist_family_lvalues as fam                  # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src33_mazur_degrees_closed as mz                   # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402
import src42_odd_additive_period_barrier as bar           # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
OUT = LOGS / "src54-compiler-targets.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
FAMILY_BOUND = 4000


def _load(name: str) -> dict | None:
    p = LOGS / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                    # pragma: no cover
        return None


def v03_procedure(bound: int = FAMILY_BOUND) -> dict:
    """`06` v0.3's certificate for a fixed odd additive prime, run per member."""
    surj = _load("src38-mod-ell-surjectivity.json") or {}
    certified = set(surj.get("certified_surjective") or [])
    w = h3c.w_minus(BASE)
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]

    rows = []
    for q in members:
        tw = mz.quadratic_twist(BASE, q)
        pot = tate.potential_reduction(tw, q)
        pot_mult = pot == "potentially multiplicative"
        h3v = h3c.h3(w, q)
        rows.append({
            "q": q,
            "GLOBAL_H1": {"verdict": "PASS" if q in certified else "UNKNOWN",
                          "why": ("RUN-036 certified surjectivity there"
                                  if q in certified else
                                  "beyond RUN-036's certified range; "
                                  "irreducibility holds by RUN-031, absolute "
                                  "irreducibility is not certified here")},
            "LOCAL_H2": {
                "branch_1_potentially_multiplicative": pot_mult,
                "branch_1_verdict": "FAIL" if pot_mult else "not taken",
                "potential_reduction": pot,
                "branch_2_local_irreducible_over_Fp": "NOT COMPUTED HERE",
                "branch_3_local_isogeny_kernel_test": "NOT COMPUTED HERE",
                "verdict": "UNKNOWN"},
            "H3": {"verdict": "PASS" if h3v["pass"] else "FAIL",
                   "witness_ell": h3v["witness"], "computed": True},
            "PERIOD": {"verdict": "OPEN",
                       "why": "RUN-039 left c_E = 1 open; RUN-040 checked "
                              "`01`'s weaker sufficient condition"},
            "FINAL": "not reachable — LOCAL_H2 and PERIOD are not decided"})

    return {"members": len(members), "rows": rows,
            "branch_1_never_fires": all(
                not r["LOCAL_H2"]["branch_1_potentially_multiplicative"]
                for r in rows),
            "H3_passes_at_every_member": all(r["H3"]["verdict"] == "PASS"
                                             for r in rows),
            "H1_unknown_at_every_member": all(
                r["GLOBAL_H1"]["verdict"] == "UNKNOWN" for r in rows),
            "steps_decided_here": 2, "steps_partial": 1, "steps_outside": 2,
            "the_improvement_v03_claims": "A2 H2 UNKNOWN -> exact finite local "
                                          "isogeny test",
            "reached_here": ("the first branch only. The test that would settle "
                             "H2 is local and this tree does not compute local "
                             "Galois data")}


def a_odd(bound: int = FAMILY_BOUND) -> dict:
    """`06`'s claim that the odd additive primes stay a finite table."""
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = []
    for q in members:
        tw = mz.quadratic_twist(BASE, q)
        odd = bar.odd_additive_primes(tw)
        rows.append({"q": q, "A_odd": odd, "size": len(odd),
                     "is_exactly_q": odd == [q]})
    base_odd = bar.odd_additive_primes(BASE)
    return {"base_A_odd": base_odd, "base_size": len(base_odd),
            "members": len(members), "rows": rows,
            "every_member_has_exactly_one": all(r["size"] == 1 for r in rows),
            "and_it_is_q": all(r["is_exactly_q"] for r in rows),
            "so_the_quantifier_does_not_reinflate": all(r["size"] == 1
                                                        for r in rows),
            "the_claim": "odd additive primes 依然只產生有限 table，因此 "
                         "∀p 沒有重新膨脹",
            "measured": ("one row per member, and the base curve has none at "
                         "all — its only additive prime is 2")}


def compiler_targets() -> dict:
    """`02`'s four, scored — including the one whose domain is empty here."""
    md = gcd35.multiplicative_data(BASE)
    odd_mult = [r for r in md["multiplicative"] if r["p"] % 2]
    g_mult = math.gcd(*[r["n"] for r in odd_mult]) if odd_mult else 0
    divisors = [p for p in mz.small_primes(200) if p > 2 and g_mult
                and g_mult % p == 0]
    comp = _load("src47-fw-compiler.json") or {}
    unknown = ((comp.get("level_1") or {}).get("unknown_primes") or [])
    rows = [
        {"target": "1. Additive FW-H2 compiler",
         "state": "`06` v0.3 is the design; its decisive branch is local and "
                  "this arm cannot run it",
         "this_arm": "H2 stays UNKNOWN at the additive prime (RUN-045)"},
        {"target": "2. Period compiler",
         "state": "RUN-039 left c_E = 1 open; RUN-040 ran `01`'s sufficient "
                  "condition on all 19 members",
         "this_arm": "PERIOD_SAFE not emitted; the weaker p ∤ c is checked"},
        {"target": "3. Ordinary finite exception compiler for p | g_mult",
         "state": f"g_mult^odd = {g_mult}, whose odd prime divisors are "
                  f"{divisors}",
         "this_arm": "the target's DOMAIN IS EMPTY for this curve — no odd "
                     "prime divides 1, so there is no finite exception to "
                     "compile. Inapplicable, not achieved"},
        {"target": "4. Only then census",
         "state": "no census exists in this tree",
         "this_arm": f"RUN-045 emits a per-prime certificate with "
                     f"{len(unknown)} UNKNOWN rows kept visible"},
    ]
    return {"rows": rows, "g_mult_odd": g_mult,
            "odd_divisors_of_g_mult": divisors,
            "target_3_domain_is_empty": not divisors,
            "no_census_exists": True,
            "unknown_rows_visible": len(unknown)}


def discipline_lines() -> dict:
    """`02`'s two rules, checked against this line's own output."""
    comp = _load("src47-fw-compiler.json") or {}
    l1 = comp.get("level_1") or {}
    unknown = l1.get("unknown_primes") or []
    # `02` §4 specifies the census by its five status columns, so the check
    # looks for those rather than for the word "census" — a filename scan
    # matched src19's CONDUCTOR census, which is a different thing entirely.
    STATUSES = ("GENERIC_PASS", "FINITE_EXCEPTION_PASS",
                "ADDITIVE_LOCAL_UNKNOWN", "PERIOD_UNKNOWN", "TRUE_REJECT")
    # And it must skip THIS gate's own output. A detector that publishes its
    # search terms into the directory it searches will match itself: the five
    # names are written to `src54-compiler-targets.json` below, so the first
    # run was green only because that file did not exist yet. A check whose
    # first run is green because its own output is not there has not been
    # tested.
    census = []
    for f in LOGS.glob("*.json"):
        if f.name == OUT.name:
            continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        if sum(x in t for x in STATUSES) >= 3:
            census.append(f)
    return {"rule_1": {"text": "No database scaling until this is exact",
                       "target": "1. Additive FW-H2 compiler",
                       "obeyed_here": True,
                       "how": "no census over the search pool exists in this "
                              "tree, and target 1 is not exact here"},
            "rule_2": {"text": "The UNKNOWN rows must remain visible",
                       "obeyed_here": bool(unknown),
                       "how": f"RUN-045's certificate carries {len(unknown)} "
                              f"UNKNOWN rows in its emitted output, not in a "
                              f"footnote"},
            "census_status_columns": list(STATUSES),
            "logs_carrying_that_census": [f.name for f in census],
            "why_not_a_filename_scan": ("a scan for the word census matched "
                                        "src19's CONDUCTOR census, which is a "
                                        "different table. The five status "
                                        "columns are what `02` §4 specifies"),
            "this_gates_own_log_is_excluded": OUT.name,
            "why_it_must_be": ("the five status names are written into this "
                               "log, so the detector would match itself on "
                               "every run after the first. The first run was "
                               "green only because the log did not exist yet"),
            "both_obeyed": bool(unknown)}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    proc = v03_procedure()
    ao = a_odd()
    tg = compiler_targets()
    dl = discipline_lines()

    ok = (proc["branch_1_never_fires"] and proc["H3_passes_at_every_member"]
          and proc["H1_unknown_at_every_member"]
          and ao["every_member_has_exactly_one"] and ao["and_it_is_q"]
          and not ao["base_A_odd"]
          and tg["target_3_domain_is_empty"] and tg["no_census_exists"]
          and dl["both_obeyed"] and not dl["logs_carrying_that_census"])

    log = {
        "gate": "src54 — 02's compiler targets and 06 v0.3's procedure",
        "source": "02_Next_Compiler_Targets, 06_Witness_Network_v03_Integration",
        "curve": BASE, "conductor": N,
        "v03_procedure": proc,
        "A_odd": ao,
        "compiler_targets": tg,
        "discipline_lines": dl,
        "headline": (f"`06` v0.3's procedure runs to its first branch and stops: "
                     f"every member's odd additive prime is potentially GOOD so "
                     f"the FAIL branch is not taken, H3 passes with witness 29 "
                     f"at all {proc['members']} members, H1 is UNKNOWN beyond "
                     f"RUN-036's range, and the branch that would settle H2 is "
                     f"local Galois data this tree does not compute — two of "
                     f"five steps decided. `𝒜_odd` is one prime per member and "
                     f"none for the base, so the quantifier does not reinflate. "
                     f"And `02`'s target 3 has an EMPTY DOMAIN here: "
                     f"g_mult^odd = {tg['g_mult_odd']} has no odd prime "
                     f"divisor, so there is no finite exception to compile"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    r0 = proc["rows"][0]
    print(f"  06 v0.3, run at the odd additive prime of each of "
          f"{proc['members']} members (shown: q = {r0['q']})")
    print(f"    GLOBAL_H1  {r0['GLOBAL_H1']['verdict']:<8} "
          f"{r0['GLOBAL_H1']['why'][:56]}")
    print(f"    LOCAL_H2   {r0['LOCAL_H2']['verdict']:<8} branch 1 "
          f"({r0['LOCAL_H2']['potential_reduction']}) "
          f"{r0['LOCAL_H2']['branch_1_verdict']}")
    print(f"               branch 2 {r0['LOCAL_H2']['branch_2_local_irreducible_over_Fp']}")
    print(f"               branch 3 {r0['LOCAL_H2']['branch_3_local_isogeny_kernel_test']}")
    print(f"    H3         {r0['H3']['verdict']:<8} witness ℓ = "
          f"{r0['H3']['witness_ell']}, computed")
    print(f"    PERIOD     {r0['PERIOD']['verdict']:<8} {r0['PERIOD']['why'][:52]}")
    print(f"    FINAL      {r0['FINAL']}")
    print(f"    → {proc['steps_decided_here']} decided, "
          f"{proc['steps_partial']} partial, {proc['steps_outside']} outside "
          f"this arm")
    print()
    print(f"  𝒜_odd: base {ao['base_A_odd']} (size {ao['base_size']}), every "
          f"member exactly one and it is q: {ao['and_it_is_q']}")
    print(f"    → the quantifier does not reinflate: "
          f"{ao['so_the_quantifier_does_not_reinflate']}")
    print()
    print("  02's four targets")
    for r in tg["rows"]:
        print(f"    {r['target']}")
        print(f"        {r['state'][:76]}")
        print(f"        → {r['this_arm'][:76]}")
    print()
    print(f"  02's discipline lines")
    print(f"    \"{dl['rule_1']['text']}\" — obeyed: "
          f"{dl['rule_1']['obeyed_here']} ({dl['how'] if 'how' in dl else dl['rule_1']['how'][:44]})")
    print(f"    \"{dl['rule_2']['text']}\" — obeyed: "
          f"{dl['rule_2']['obeyed_here']}, {dl['rule_2']['how'][:52]}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
