"""Gate 37 — the quadratic-twist invariance bridge, and what its split condition buys.

數學戰士「墜衡」 / AMRAL Research Lab.

`03_Quadratic_Twist_Invariance_Bridge` exists to push the Fouquet–Wan hypotheses
from the twist back down to the base, so that one certificate at `E` covers
infinitely many `d`. It offers three candidate lemmas:

    A  irreducibility invariance          rho-bar_{E,p} abs. irreducible
                                          <=> rho-bar_{E_d,p} abs. irreducible
    B  local semisimplification           the FW-forbidden shape is preserved
       degeneracy invariance              under twisting
    C  split-at-ell local preservation    if ell | N splits in Q(sqrt d) then
                                          chi_d is trivial on G_{Q_ell}, so the
                                          local representation is unchanged

and then states the bridge: A ∧ B ∧ C ⟹ FW(E, p) ⟹ FW(E_d, p).

THE DOCUMENT MARKS B UNFINISHED IN ITS OWN TEXT — 「狀態：標準表示論推導候選；
正式文件需逐 theorem version 核對」 — so the bridge is not established, and this
gate reports that rather than quietly running the two lemmas that are checkable
and calling the conclusion measured.

WHAT IS MEASURED IS LEMMA C, IN BOTH DIRECTIONS. Its computable content is
sharp: at an `ell | N` that **splits**, every local invariant of `E_d` at `ell`
must equal `E`'s; at an `ell` that is **inert**, the twisting character is
nontrivial on `G_{Q_ell}` and the local data must genuinely move. Running only
the split side would confirm a preservation that a constant function would also
satisfy.

AND IT CLOSES WHAT RUN-033 LEFT OPEN. That round found the FW-H3 route holds a
single witness — 29, the only nonsplit multiplicative prime — with nothing in
reserve. Twisting swaps split and nonsplit multiplicative reduction at an inert
prime, so a member with 29 inert in `Q(sqrt q)` would turn 29 split, empty the
nonsplit set, and take the witness away. `𝒫`'s condition that 2, 3 and 29 split
is exactly what prevents it, and that is measured here rather than argued.

Usage:  python code/src37_twist_invariance_bridge.py
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
import src33_mazur_degrees_closed as mz                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gate-logs" / "src37-twist-bridge.json"

BASE = [0, 1, 0, 8, -16]                  # 696.e1
N = 696
CONDUCTOR_PRIMES = (2, 3, 29)             # 696 = 2^3 * 3 * 29
FAMILY_BOUND = 4000
INERT_SEARCH = 4000
SIEVE_PRIMES = 300                        # for lemma A's computable shadow

B_STATUS = ("標準表示論推導候選；正式文件需逐 theorem version 核對")


def chi_trivial_at(d: int, ell: int) -> bool:
    """Is the quadratic character χ_d trivial on G_{Q_ell}?

    Equivalently: does ell split in Q(sqrt d)? For odd ell coprime to d that is
    the Legendre symbol; at 2 it is d ≡ 1 (mod 8). Both are the standard
    splitting criteria and both are the condition `03` §4 asks for.
    """
    if ell == 2:
        return d % 8 == 1
    if d % ell == 0:
        return False                       # ramified, neither split nor inert
    return ph2.legendre(d, ell) == 1


def local_invariants(ainvs: list[int], ell: int) -> dict:
    """Everything about the reduction at ell that this tree can compute."""
    r = tate.reduction_data(ainvs, ell, want_c=True)
    return {"kodaira": r.get("kodaira"), "f": r.get("f"), "c": r.get("c"),
            "v_disc": r.get("v_disc"),
            "split_multiplicative": r.get("split_multiplicative")}


def lemma_C(bound: int = FAMILY_BOUND) -> dict:
    """The split side: every member, every conductor prime, base against twist."""
    base = {ell: local_invariants(BASE, ell) for ell in CONDUCTOR_PRIMES}
    members = [q for q in anchor.sieve(bound) if fam.in_P(q)]
    rows = []
    for q in members:
        tw = mz.quadratic_twist(BASE, q)
        per = {}
        for ell in CONDUCTOR_PRIMES:
            split = chi_trivial_at(q, ell)
            got = local_invariants(tw, ell)
            per[ell] = {"chi_trivial_on_G_Q_ell": split,
                        "identical_to_base": got == base[ell],
                        "twist": got}
        rows.append({"q": q,
                     "all_conductor_primes_split": all(
                         per[e]["chi_trivial_on_G_Q_ell"]
                         for e in CONDUCTOR_PRIMES),
                     "all_local_data_preserved": all(
                         per[e]["identical_to_base"] for e in CONDUCTOR_PRIMES),
                     "per_prime": {str(k): v for k, v in per.items()}})
    return {"base": {str(k): v for k, v in base.items()},
            "members": len(members), "rows": rows,
            "every_member_splits_at_2_3_29": all(
                r["all_conductor_primes_split"] for r in rows),
            "every_member_preserves_all_local_data": all(
                r["all_local_data_preserved"] for r in rows)}


def lemma_C_converse(bound: int = INERT_SEARCH) -> dict:
    """The inert side. Preservation at split primes means nothing unless the
    same computation moves at an inert one.

    The change to look for is specific: twisting by a `d` at which `ell` is
    inert makes the quadratic character nontrivial on `G_{Q_ell}`, and for a
    multiplicative `ell` that swaps split and nonsplit reduction. The Kodaira
    type and the valuation stay put; the split flag flips.

    AT ell = 2 NOTHING THIS TREE COMPUTES CAN MOVE, AND THAT IS REPORTED AS
    UNTESTABLE RATHER THAN AS A PASS. Every member has `q ≡ 1 (mod 4)`, so the
    twist is unramified at 2 and preserves the Kodaira type and `v_2(Δ)`; the
    type is `II*`, whose component group is trivial, so the Tamagawa number is
    the constant 1; and 2 is additive, so there is no split flag. The whole
    invariant set is forced. A prime where the measurement cannot move is not a
    prime where the measurement succeeded.
    """
    out = {}
    for ell in CONDUCTOR_PRIMES:
        tried, moved = 0, None
        for d in anchor.sieve(bound):
            if d % 4 != 1 or N % d == 0 or chi_trivial_at(d, ell):
                continue
            tried += 1
            base = local_invariants(BASE, ell)
            got = local_invariants(mz.quadratic_twist(BASE, d), ell)
            if got != base:
                moved = {"d": d, "base": base, "twist": got,
                         "changed_fields": sorted(k for k in base
                                                  if base[k] != got[k]),
                         "split_flag_flipped": (
                             base.get("split_multiplicative") is not None
                             and base.get("split_multiplicative")
                             != got.get("split_multiplicative"))}
                break
        base = local_invariants(BASE, ell)
        out[ell] = {"inert_d_tried": tried, "moved": moved,
                    "reduction": ("multiplicative"
                                  if base.get("split_multiplicative") is not None
                                  else "additive"),
                    "testable": moved is not None,
                    "why_not": None if moved else (
                        f"every invariant available here is forced at {ell}: "
                        f"q ≡ 1 (mod 4) makes the twist unramified there, so "
                        f"the Kodaira type {base.get('kodaira')} and v(Δ) = "
                        f"{base.get('v_disc')} are preserved; that type has "
                        f"Tamagawa number {base['c']} for every curve carrying "
                        f"it; and additive reduction has no split flag. "
                        f"{tried} inert d were tried and none moved anything")}
    mult = [e for e in CONDUCTOR_PRIMES
            if out[e]["reduction"] == "multiplicative"]
    return {"per_prime": {str(k): v for k, v in out.items()},
            "moved_at_every_multiplicative_conductor_prime":
                all(out[e]["testable"] for e in mult),
            "untestable_primes": [e for e in CONDUCTOR_PRIMES
                                  if not out[e]["testable"]],
            "why": ("preservation at a split prime is only a finding if the "
                    "same computation moves at an inert one — otherwise a "
                    "constant would pass lemma C. Where no available invariant "
                    "can move, the prime is reported untestable, not passing")}


def the_witness_that_depends_on_it() -> dict:
    """RUN-033's single nonsplit witness, and the twist that would remove it.

    29 is the only nonsplit multiplicative prime of the base, so it is the only
    FW-H3 witness there is. If a member had 29 inert in Q(sqrt q), the twist
    would make 29 split, the nonsplit set would be empty, and — the gcd of an
    empty set being 0 — every odd p would fail lemma 3 of `00_GCD_Witness_Lemmas`.
    """
    base29 = local_invariants(BASE, 29)
    d = None
    for cand in anchor.sieve(INERT_SEARCH):
        if cand % 4 == 1 and N % cand and not chi_trivial_at(cand, 29):
            d = cand
            break
    tw = mz.quadratic_twist(BASE, d) if d else None
    got = local_invariants(tw, 29) if tw else None
    members = [q for q in anchor.sieve(FAMILY_BOUND) if fam.in_P(q)]
    still = all(local_invariants(mz.quadratic_twist(BASE, q),
                                 29).get("split_multiplicative") is False
                for q in members)
    return {"base_29_is_nonsplit": base29.get("split_multiplicative") is False,
            "a_d_with_29_inert": d,
            "its_twist_at_29": got,
            "witness_would_be_lost_there": (got is not None
                                            and got.get("split_multiplicative")
                                            is True),
            "29_stays_nonsplit_for_every_member": still,
            "members_checked": len(members),
            "reading": ("the FW-H3 witness survives the family because 𝒫 "
                        "requires 29 to split in Q(sqrt q); a twist by a d "
                        "where 29 is inert turns it split and there is no "
                        "second nonsplit prime to fall back on")}


def lemma_A_shadow(limit: int = SIEVE_PRIMES) -> dict:
    """Lemma A is representation theory; its computable shadow is the sieve input.

    Tensoring by a 1-dimensional character is an auto-equivalence, so
    irreducibility is invariant — that is the lemma, and it is not a computation.
    What this tree can measure is the quantity the reducibility sieve reads:
    `a_ell^2 - 4 ell`, which RUN-031 showed is unchanged because
    `a_ell(E^(d)) = chi_d(ell) a_ell(E)` squares the sign away. Re-measured here
    at the two smallest members so the bridge's section cites this tree.
    """
    primes = mz.small_primes(limit)
    rows = []
    for d in (241, 313):
        tw = mz.quadratic_twist(BASE, d)
        same = flips = compared = 0
        for ell in primes:
            if N % ell == 0 or d % ell == 0:
                continue
            a0 = anchor.point_count_ap(BASE, ell)
            a1 = anchor.point_count_ap(tw, ell)
            compared += 1
            same += (a0 * a0 - 4 * ell) == (a1 * a1 - 4 * ell)
            flips += (a0 != a1)
        rows.append({"d": d, "good_primes_compared": compared,
                     "discriminant_identical": same, "a_ell_sign_flips": flips})
    return {"lemma": "A — irreducibility invariance",
            "status": "representation theory, cited",
            "computable_shadow": "a_ell^2 - 4 ell, the sieve's input",
            "rows": rows,
            "all_identical": all(r["discriminant_identical"]
                                 == r["good_primes_compared"] for r in rows),
            "flips_seen": all(r["a_ell_sign_flips"] >= 10 for r in rows)}


def lemma_B_status() -> dict:
    """B is reported exactly as the document reports it."""
    return {"lemma": "B — local semisimplification degeneracy invariance",
            "documents_own_status": B_STATUS,
            "established_here": False,
            "why_not": ("the document marks it a candidate derivation needing "
                        "per-theorem-version checking, and this arm has no way "
                        "to check a theorem version it does not hold"),
            "consequence_for_the_bridge": ("A ∧ B ∧ C is what gives "
                                           "FW(E,p) ⟹ FW(E_d,p). With B open "
                                           "the bridge is not established, and "
                                           "C being measured does not change "
                                           "that")}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:                               # pragma: no cover
        pass

    c = lemma_C()
    cc = lemma_C_converse()
    w = the_witness_that_depends_on_it()
    a = lemma_A_shadow()
    b = lemma_B_status()

    ok = (c["every_member_splits_at_2_3_29"]
          and c["every_member_preserves_all_local_data"]
          and cc["moved_at_every_multiplicative_conductor_prime"]
          and all(cc["per_prime"][str(e)]["why_not"]
                  for e in cc["untestable_primes"])
          and w["base_29_is_nonsplit"] and w["witness_would_be_lost_there"]
          and w["29_stays_nonsplit_for_every_member"]
          and a["all_identical"] and a["flips_seen"]
          and b["established_here"] is False)

    log = {
        "gate": "src37 — the quadratic-twist invariance bridge",
        "source": "03_Quadratic_Twist_Invariance_Bridge",
        "curve": BASE, "conductor": N,
        "lemma_A": a, "lemma_B": b,
        "lemma_C": c, "lemma_C_converse": cc,
        "the_witness_that_depends_on_it": w,
        "bridge_status": ("NOT established. C is measured on both sides and A's "
                          "computable shadow holds, but the document itself "
                          "marks B a candidate, and the bridge needs all three"),
        "ok": ok,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes((json.dumps(log, indent=2, ensure_ascii=False) + "\n")
                    .encode("utf-8"))

    print(f"  lemma C — {c['members']} members, conductor primes "
          f"{CONDUCTOR_PRIMES}")
    print(f"    all split in Q(√q) for every member : "
          f"{c['every_member_splits_at_2_3_29']}")
    print(f"    every local invariant preserved     : "
          f"{c['every_member_preserves_all_local_data']}")
    print()
    print("  the inert side — the same computation must move")
    for ell, r in cc["per_prime"].items():
        if r["moved"]:
            m = r["moved"]
            print(f"    ℓ = {ell:<4} d = {m['d']:<6} changed "
                  f"{m['changed_fields']}"
                  + ("   split flag flipped" if m["split_flag_flipped"] else ""))
        else:
            print(f"    ℓ = {ell:<4} UNTESTABLE — {r['inert_d_tried']} inert d "
                  f"tried, nothing this tree computes can move there")
    print(f"    moved at every multiplicative conductor prime: "
          f"{cc['moved_at_every_multiplicative_conductor_prime']}   "
          f"untestable: {cc['untestable_primes']}")
    print()
    print("  the witness RUN-033 found has exactly one holder")
    print(f"    29 nonsplit for the base                  : "
          f"{w['base_29_is_nonsplit']}")
    print(f"    a d with 29 inert                         : d = {w['a_d_with_29_inert']}"
          f"  → 29 becomes split: {w['witness_would_be_lost_there']}")
    print(f"    29 stays nonsplit for all {w['members_checked']} members    : "
          f"{w['29_stays_nonsplit_for_every_member']}")
    print()
    print("  lemma A — computable shadow (a_ℓ² − 4ℓ)")
    for r in a["rows"]:
        print(f"    d = {r['d']:<5} {r['discriminant_identical']}/"
              f"{r['good_primes_compared']} identical, "
              f"{r['a_ell_sign_flips']} sign flips in a_ℓ")
    print()
    print(f"  lemma B — {b['documents_own_status']}")
    print(f"    established here: {b['established_here']}")
    print(f"  bridge: {log['bridge_status'][:52]}…")
    print()
    print(f"wrote {OUT.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
