"""Gate 50 — the candidate schema and the sieve that found the anchor, with its control.

數學戰士「墜衡」 / AMRAL Research Lab.

`13_Candidate_NonSemistable_Strong_BSD_Family` is a schema — B0 through B5, plus
six obligations and the line 六項完成前，不升級為 theorem. `14_Candidate_Sieve`
is why 696.e1 came out of it, and it carries something most of the corpus does
not: **a control curve that fails**.

    116.b1   rank 0, a clean cheap 2-part anchor, nonsplit multiplicative at 29
             — but its odd bad structure is only {29}, so at p = 29 there is no
             second q || N to serve as the ramification witness, and the sieve
             eliminates it as FAIL_FIXED_MULTIPLICATIVE_WITNESS.

and then draws the conclusion the whole family rests on:

    至少兩個 odd multiplicative reservoirs，其中至少一個 nonsplit。

THE CONTROL IS THE POINT, SO THE CONTROL IS RUN. A gate that checked only 696.e1
would confirm a criterion it never watched fail. `116.b1` is **found by its
conductor** rather than taken from recollection — RUN-030 caught three numbers
quoted from memory and the repair was structural — and then put through the same
leave-one-out RUN-033 ran, where it has no witness at all.

`13`'s B1 AND B2 ARE RUN-033's LEMMA 1 AND RUN-037's PREMISE UNDER OTHER NAMES.
`g_mult^odd(E)` is the gcd over the odd multiplicative primes and `g_-(E)` the
gcd over the nonsplit ones; both must be powers of two. This tree computed both
before reading `13`, so the schema is checked against arithmetic that did not
come from it.

Usage:  python code/src50_candidate_schema_and_sieve.py
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import src15_phase2_anchor as anchor                      # noqa: E402
import src18_tate_algorithm as tate                       # noqa: E402
import src35_gcd_witness_lemmas as gcd35                  # noqa: E402
import src39_fw_h3_compiler as h3c                        # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGS = ROOT / "data" / "gate-logs"
OUT = LOGS / "src50-candidate-schema.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
BASE_N = 696
CONTROL_N = 116                           # 14's control curve, found not quoted
SEARCH_BOX = 12


def odd_local_structure(ainvs: list[int]) -> dict:
    """`14`'s odd local table, recomputed."""
    md = gcd35.multiplicative_data(ainvs)
    if md.get("singular"):
        return {"singular": True}
    rows = []
    for r in md["rows"]:
        rows.append({"p": r["p"], "type": r["type"], "kodaira": r["kodaira"],
                     "v_disc": r["v_disc"],
                     "split": r.get("split")})
    odd_mult = [r for r in md["multiplicative"] if r["p"] % 2]
    nonsplit = [r for r in md["nonsplit"] if r["p"] % 2]
    return {"singular": False, "rows": rows,
            "W_mult_odd": [r["p"] for r in odd_mult],
            "W_minus": [r["p"] for r in nonsplit],
            "valuations": {str(r["p"]): r["n"] for r in odd_mult},
            "g_mult_odd": (math.gcd(*[r["n"] for r in odd_mult])
                           if odd_mult else 0),
            "g_minus": (math.gcd(*[r["n"] for r in nonsplit])
                        if nonsplit else 0)}


def sieve_criterion(ainvs: list[int]) -> dict:
    """`14`'s boxed conclusion, and `13`'s B1/B2 powers of two."""
    s = odd_local_structure(ainvs)
    if s.get("singular"):
        return {"singular": True}
    two_reservoirs = len(s["W_mult_odd"]) >= 2
    one_nonsplit = len(s["W_minus"]) >= 1
    # the fixed-multiplicative leave-one-out, for each odd multiplicative p
    loo = []
    for p in s["W_mult_odd"]:
        others = [q for q in s["W_mult_odd"] if q != p
                  and s["valuations"][str(q)] % p]
        loo.append({"p": p, "witness": others[0] if others else None,
                    "has_a_distinct_witness": bool(others)})
    return {"W_mult_odd": s["W_mult_odd"], "W_minus": s["W_minus"],
            "at_least_two_odd_multiplicative": two_reservoirs,
            "at_least_one_nonsplit": one_nonsplit,
            "boxed_criterion_met": two_reservoirs and one_nonsplit,
            "B1_g_mult_odd": s["g_mult_odd"],
            "B1_is_a_power_of_two": h3c.is_power_of_two(s["g_mult_odd"]),
            "B2_g_minus": s["g_minus"],
            "B2_is_a_power_of_two": h3c.is_power_of_two(s["g_minus"]),
            "fixed_multiplicative_leave_one_out": loo,
            "every_fixed_multiplicative_p_has_a_witness":
                bool(loo) and all(r["has_a_distinct_witness"] for r in loo)}


def find_by_conductor(target: int, box: int = SEARCH_BOX) -> dict:
    """Find a curve of the given conductor rather than quote its a-invariants.

    RUN-030's certificate quoted three numbers from memory and all three were
    wrong; the repair was to derive rather than recall. `14` names its control
    by LMFDB label, and a label is a name, not arithmetic — so the curve is
    searched for by the one thing that is arithmetic about it.
    """
    found, scanned = [], 0
    for a1 in (0, 1):
        for a2 in (-1, 0, 1):
            for a3 in (0, 1):
                for a4 in range(-box, box + 1):
                    for a6 in range(-box, box + 1):
                        ai = [a1, a2, a3, a4, a6]
                        _, _, _, _, disc = anchor.b_invariants(ai)
                        if disc == 0:
                            continue
                        scanned += 1
                        bad = sorted(gcd35.factor(disc))
                        if not bad or max(bad) > 4000:
                            continue
                        try:
                            n = tate.conductor(ai, bad)
                        except Exception:                # pragma: no cover
                            continue
                        if n == target:
                            found.append(ai)
    return {"target_conductor": target, "models_scanned": scanned,
            "found": found, "count": len(found),
            "first": found[0] if found else None}


SCHEMA = (
    ("B0", "2-part anchor: Banwait–Huang 2.14 branch, BSD(E,2), twist "
           "local/splitting conditions, 建議 c_E = 1",
     "PARTLY COMPUTED",
     "RUN-014/030 computed v2(L^alg) = 0, trivial torsion, Delta < 0; BSD(E,2) "
     "is cited; c_E = 1 is the open item RUN-039 named"),
    ("B1", "W_mult^odd non-empty and g_mult^odd a power of two",
     "COMPUTED", "RUN-033's lemma 1, under another name"),
    ("B2", "W_- non-empty and g_- a power of two",
     "COMPUTED", "RUN-037's premise, under another name"),
    ("B3", "fixed additive odd primes: exact FW-H1, FW-H2, period/Manin",
     "OPEN", "RUN-045 marks H2 UNKNOWN at the additive prime; RUN-040 checked "
             "`01`'s sufficient condition for p not dividing c"),
    ("B4", "fixed multiplicative odd primes: finite check per prime plus a "
           "distinct ramified witness",
     "COMPUTED", "RUN-033's leave-one-out gives 3 -> 29 and 29 -> 3"),
    ("B5", "twist support restrictions: avoid 3, good ordinary, avoid residual "
           "exceptions, keep 2.14's splitting/inertness",
     "COMPUTED", "RUN-032's five conditions on all 19 members; RUN-036 "
                 "certified the residual images at 38 primes"),
)

OBLIGATIONS = (
    ("fixed additive primes' exact H1 backend", "PARTLY",
     "RUN-036 certified surjectivity at 38 primes, which gives H1 there; the "
     "additive primes of E^(q) are 2 and q, and 2 is not certified"),
    ("fixed additive primes' exact H2 local residual backend", "OPEN",
     "RUN-034 found `05`'s no-go silent at the additive prime and RUN-045 marks "
     "it UNKNOWN. Silence is not a PASS"),
    ("fixed multiplicative branch formal theorem table", "CITED",
     "`27`'s proof router names Skinner Theorem C for p = 3 and p = 29"),
    ("Manin-period compatibility", "OPEN",
     "RUN-039 left c_E = 1 open; RUN-040 checked the weaker p not dividing c"),
    ("all support restrictions' Chebotarev / CRT simultaneous compatibility",
     "PARTLY", "RUN-044 computed the Chebotarev half — the 3-cycle and the "
               "identity on K agree on F_0, and a transposition would not"),
    ("final all-prime cover proof", "PARTLY",
     "RUN-047 ran `27`'s six-branch router as a partition; the branches' "
     "theorems are cited, not proved"),
)


def schema(ainvs: list[int]) -> dict:
    sc = sieve_criterion(ainvs)
    rows = [{"item": a, "text": b, "status": c, "where": d}
            for a, b, c, d in SCHEMA]
    return {"rows": rows,
            "computed": [r["item"] for r in rows if r["status"] == "COMPUTED"],
            "partly": [r["item"] for r in rows if r["status"] == "PARTLY COMPUTED"],
            "open": [r["item"] for r in rows if r["status"] == "OPEN"],
            "B1_holds": sc["B1_is_a_power_of_two"],
            "B2_holds": sc["B2_is_a_power_of_two"]}


def obligations() -> dict:
    rows = [{"obligation": a, "status": b, "where": c}
            for a, b, c in OBLIGATIONS]
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {"rows": rows, "counts": counts,
            "none_are_closed": all(r["status"] != "CLOSED" for r in rows),
            "the_documents_own_rule": "六項完成前，不升級為 theorem",
            "so": ("none of the six is closed by this arm, and `13`'s own rule "
                   "keeps the label where `20` and `27` put it")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    anchor_s = odd_local_structure(BASE)
    anchor_c = sieve_criterion(BASE)
    hunt = find_by_conductor(CONTROL_N)
    ctrl = hunt["first"]
    ctrl_s = odd_local_structure(ctrl) if ctrl else None
    ctrl_c = sieve_criterion(ctrl) if ctrl else None
    # every model of that conductor, not just the first: the elimination is a
    # statement about 116 = 2^2 * 29 having one odd prime, not about one curve
    all_ctrl = [{"ainvs": a,
                 "rows": [(r["p"], r["type"], r["kodaira"], r["v_disc"],
                           r.get("split")) for r in odd_local_structure(a)["rows"]],
                 "criterion": sieve_criterion(a)} for a in hunt["found"]]
    all_fail = all(not c["criterion"]["boxed_criterion_met"]
                   and not c["criterion"]["every_fixed_multiplicative_p_has_a_witness"]
                   for c in all_ctrl)
    sch = schema(BASE)
    obl = obligations()

    ok = (anchor_c["boxed_criterion_met"]
          and anchor_c["B1_is_a_power_of_two"] and anchor_c["B2_is_a_power_of_two"]
          and anchor_c["every_fixed_multiplicative_p_has_a_witness"]
          and ctrl is not None
          and ctrl_c["at_least_one_nonsplit"]
          and not ctrl_c["at_least_two_odd_multiplicative"]
          and not ctrl_c["boxed_criterion_met"]
          and not ctrl_c["every_fixed_multiplicative_p_has_a_witness"]
          and all_fail and len(all_ctrl) == hunt["count"]
          and obl["none_are_closed"])

    log = {
        "gate": "src50 — 13's schema and 14's sieve, with the control run",
        "source": "13_Candidate_NonSemistable_Strong_BSD_Family, "
                  "14_Candidate_Sieve",
        "anchor": {"ainvs": BASE, "conductor": BASE_N,
                   "local_structure": anchor_s, "criterion": anchor_c},
        "the_control": {"conductor": CONTROL_N, "search": hunt,
                        "ainvs": ctrl, "local_structure": ctrl_s,
                        "criterion": ctrl_c,
                        "eliminated_as": "FAIL_FIXED_MULTIPLICATIVE_WITNESS",
                        "every_model_found": all_ctrl,
                        "all_models_of_this_conductor_fail": all_fail,
                        "why": ("its odd bad structure is a single "
                                "multiplicative prime, so the leave-one-out at "
                                "that prime has no distinct candidate")},
        "the_boxed_criterion": "至少兩個 odd multiplicative reservoirs，"
                               "其中至少一個 nonsplit",
        "schema_B0_to_B5": sch,
        "the_six_obligations": obl,
        "headline": (f"`14`'s odd local table for the anchor recomputes exactly "
                     f"— 2 additive, 3 split multiplicative, 29 nonsplit, all "
                     f"valuations 1 — and its boxed criterion is met. The "
                     f"control `116.b1`, found by conductor rather than quoted, "
                     f"has a nonsplit prime and still fails: one reservoir, no "
                     f"distinct witness at p = 29. `13`'s B1 and B2 are RUN-033's "
                     f"lemma 1 and RUN-037's premise under other names, and none "
                     f"of its six obligations is closed"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  696.e1 — `14`'s odd local table, recomputed")
    for r in anchor_s["rows"]:
        extra = ("split" if r.get("split") else
                 "nonsplit" if r.get("split") is False else "")
        print(f"    {r['p']:>4}  {r['type']:<16} {str(r['kodaira']):<5} "
              f"vΔ = {r['v_disc']:<3} {extra}")
    print(f"    W_mult^odd = {anchor_c['W_mult_odd']}   W_- = "
          f"{anchor_c['W_minus']}")
    print(f"    g_mult^odd = {anchor_c['B1_g_mult_odd']} (power of 2: "
          f"{anchor_c['B1_is_a_power_of_two']})   g_- = "
          f"{anchor_c['B2_g_minus']} ({anchor_c['B2_is_a_power_of_two']})")
    print(f"    boxed criterion met: {anchor_c['boxed_criterion_met']}")
    print()
    print(f"  the control — conductor {CONTROL_N}, found not quoted "
          f"({hunt['count']} model(s) over {hunt['models_scanned']} scanned)")
    if ctrl:
        print(f"    {ctrl}")
        for r in ctrl_s["rows"]:
            extra = ("split" if r.get("split") else
                     "nonsplit" if r.get("split") is False else "")
            print(f"    {r['p']:>4}  {r['type']:<16} {str(r['kodaira']):<5} "
                  f"vΔ = {r['v_disc']:<3} {extra}")
        print(f"    W_mult^odd = {ctrl_c['W_mult_odd']}   W_- = "
              f"{ctrl_c['W_minus']}")
        print(f"    at least two reservoirs: "
              f"{ctrl_c['at_least_two_odd_multiplicative']}   at least one "
              f"nonsplit: {ctrl_c['at_least_one_nonsplit']}")
        print(f"    leave-one-out: {ctrl_c['fixed_multiplicative_leave_one_out']}")
        print(f"    → boxed criterion met: {ctrl_c['boxed_criterion_met']}  "
              f"eliminated as FAIL_FIXED_MULTIPLICATIVE_WITNESS")
    print(f"    all {len(all_ctrl)} model(s) of conductor {CONTROL_N} fail the "
          f"same way: {all_fail}")
    for c in all_ctrl:
        print(f"      {str(c['ainvs']):<20} {c['rows']}")
    print()
    print("  13's schema")
    for r in sch["rows"]:
        print(f"    {r['item']}  {r['status']:<16} {r['text'][:48]}")
    print()
    print(f"  13's six obligations: {obl['counts']}")
    for r in obl["rows"]:
        print(f"    {r['status']:<7} {r['obligation'][:56]}")
    print(f"    {obl['the_documents_own_rule']} → none closed: "
          f"{obl['none_are_closed']}")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
