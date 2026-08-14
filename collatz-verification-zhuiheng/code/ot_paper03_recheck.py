"""Independent recheck of Operation Translation Series — Paper 03.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *Parity Word、Residue Cylinder 與局部 Identity 化*, Paper 03 v0.1.1.

The point of doing this separately
----------------------------------
Four of Paper 03's statements were already confirmed as a by-product of the
Paper 02 recheck, using the closed congruence r_w = -b_w 3^{-u} (mod 2^k) of
Theorem C. That is exactly the shortcut Paper 03 §11 warns against taking as the
*foundation*:

  > 若沒有另外證明 finite parity coding 的唯一性,
  > 直接從「最終整數」跳到「每個 intermediate parity branch 都正確」會留下論證缺口。

So the substantive check here is a **second, independent derivation of r_w** by
the refinement induction of §6/§7/§28 — start from r_D = 0, r_U = 1, and at each
step split a cylinder into r_w and r_w + 2^k according to the parity of m_w —
and confirm it agrees with the closed formula for every word. Two derivations,
one of which never uses the congruence, is what makes the congruence a *result*
rather than an assumption.

Referee for admissibility throughout: the genuine parity word of n, obtained by
running T. No theorem of Paper 03 is assumed by it.

Usage:  python code/ot_paper03_recheck.py [max_k]
"""

from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ot_paper02_recheck import compose_affine, words

MAX_K_DEFAULT = 13


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def parity_word(n: int, k: int) -> str:
    out, x = [], n
    for _ in range(k):
        out.append("U" if x % 2 else "D")
        x = T(x)
    return "".join(out)


def r_by_congruence(w: str) -> int:
    """Theorem C — the closed formula."""
    k = len(w)
    _, b, _ = compose_affine(w)
    u = w.count("U")
    return (-b * pow(3, -u, 2 ** k)) % 2 ** k


class NotACylinder(Exception):
    """Raised when a claimed residue does not make m_w integral.

    This is a detection, not a crash: an inconsistent residue is exactly what a
    wrong derivation produces. Raising a named exception lets the comparison
    below report it as a disagreement, instead of the whole run dying on an
    assertion and being recorded only as "crashed"."""


def m_of(w: str, r: int) -> int:
    k = len(w)
    _, b, _ = compose_affine(w)
    u = w.count("U")
    val = Fraction(3 ** u * r + b, 2 ** k)
    if val.denominator != 1:
        raise NotACylinder(f"m_w not integral for {w} with r={r}")
    return val.numerator


def refinement_table(max_k: int) -> dict[str, int]:
    """§6/§7/§28 — r_w built purely by cylinder refinement.

    Base: r_D = 0, r_U = 1 (§3). Step: a cylinder r_w mod 2^k splits into the two
    children r_w and r_w + 2^k mod 2^{k+1}; which child carries D is decided by
    the parity of m_w, because T^k(r_w + 2^k a) = m_w + 3^u a is congruent to
    m_w + a mod 2.

    This never touches b_w 3^{-u}.
    """
    tab: dict[str, int] = {"D": 0, "U": 1}
    for k in range(1, max_k):
        for w in [x for x in tab if len(x) == k]:
            r = tab[w]
            try:
                m = m_of(w, r)
            except NotACylinder:
                # a wrong derivation shows up here first; record an impossible
                # residue so the comparison below reports the word rather than
                # the whole run dying
                tab[w + "D"] = tab[w + "U"] = -1
                continue
            # child with a even keeps residue r; child with a odd gets r + 2^k
            # a = m_w mod 2 selects D, a = 1 - m_w mod 2 selects U
            a_for_D = m % 2
            tab[w + "D"] = (r + 2 ** k * a_for_D) % 2 ** (k + 1)
            tab[w + "U"] = (r + 2 ** k * (1 - a_for_D)) % 2 ** (k + 1)
    return tab


def main() -> int:
    max_k = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_K_DEFAULT
    rep = {
        "tool": "ot_paper03_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 03 v0.1.1 (Neo.K)",
        "scope": "exact finite arithmetic; not a Collatz proof",
        "max_word_length": max_k,
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    # --- the two independent derivations of r_w -----------------------------
    refine = refinement_table(max_k)
    agree = True
    mismatch = None
    for w, r_ref in sorted(refine.items(), key=lambda kv: (len(kv[0]), kv[0])):
        r_con = r_by_congruence(w)
        if r_ref != r_con:
            agree = False
            mismatch = {"word": w, "by_refinement": r_ref, "by_congruence": r_con}
            break
    check("P03_ThmC_closed_formula_agrees_with_the_refinement_induction",
          agree, f"first mismatch {mismatch}")
    rep["counts"]["words_derived_two_ways"] = len(refine)

    # §32: the residues form an inverse system, r_{k+1} = r_k mod 2^k
    nested = all(refine[w + c] % 2 ** len(w) == refine[w]
                 for w in refine for c in "DU" if w + c in refine)
    check("P03_S32_nested_residues_form_an_inverse_system", nested)

    # §7: the two children are exactly {r_w, r_w + 2^k}
    split = all(
        {refine[w + "D"], refine[w + "U"]} == {refine[w], refine[w] + 2 ** len(w)}
        for w in refine if w + "D" in refine
    )
    check("P03_S7_children_are_exactly_r_w_and_r_w_plus_2k", split)

    # --- Theorems A, B, D, E, F, and §19, §29 -------------------------------
    ok = dict.fromkeys("A B D E F faith qbit".split(), True)
    cases = 0
    for k in range(1, max_k + 1):
        seen: dict[int, str] = {}
        for w in words(k):
            r = refine[w]
            try:
                m = m_of(w, r)
            except NotACylinder:
                ok["A"] = ok["D"] = False
                continue
            u = w.count("U")
            # Theorem B: distinct words get distinct residues
            if r in seen:
                ok["B"] = False
            seen[r] = w
            for a in range(0, 7):
                n = r + 2 ** k * a
                if n <= 0:
                    continue
                # Theorem A: membership in the cylinder is exactly admissibility
                if parity_word(n, k) != w:
                    ok["A"] = False
                y = n
                for _ in range(k):
                    y = T(y)
                # Theorem D: exact cylinder transport
                if y != m + 3 ** u * a:
                    ok["D"] = False
                # Theorem E: the charts trivialise T^k to the identity
                phi = Fraction(n - r, 2 ** k)
                psi = Fraction(y - m, 3 ** u)
                if phi != a or psi != a or phi != psi:
                    ok["E"] = False
                # Theorem F: exact recovery from the target alone
                if r + 2 ** k * ((y - m) // 3 ** u) != n:
                    ok["F"] = False
                # §29: the next branch is decided by the quotient bit alone
                if y % 2 != (m + a) % 2:
                    ok["qbit"] = False
                cases += 1
            # §19: F_w is injective on the cylinder
            imgs = [m + 3 ** u * a for a in range(0, 7)]
            if len(set(imgs)) != len(imgs):
                ok["faith"] = False
        # §9 / §26: the level-k charts partition the positive integers
        if len(seen) != 2 ** k:
            ok["B"] = False

    for key, name in {
        "A": "P03_ThmA_cylinder_is_exactly_the_admissible_domain",
        "B": "P03_ThmB_word_residue_bijection_and_partition",
        "D": "P03_ThmD_exact_cylinder_transport",
        "E": "P03_ThmE_local_identity_trivialization",
        "F": "P03_ThmF_exact_recovery",
        "faith": "P03_S19_faithfulness_F_w_is_injective_on_its_cylinder",
        "qbit": "P03_S29_next_branch_decided_by_the_quotient_bit",
    }.items():
        check(name, ok[key])
    rep["counts"]["transport_cases"] = cases

    # §9 as an explicit partition of an initial segment of the positive integers
    part_ok = True
    for k in range(1, min(max_k, 11) + 1):
        buckets: dict[str, int] = {}
        N = 4 * 2 ** k
        for n in range(1, N + 1):
            buckets[parity_word(n, k)] = buckets.get(parity_word(n, k), 0) + 1
        if len(buckets) != 2 ** k or sum(buckets.values()) != N:
            part_ok = False
        # every residue class of size N/2^k, since N is a multiple of 2^k
        if any(v != N // 2 ** k for v in buckets.values()):
            part_ok = False
    check("P03_S9_level_k_atlas_partitions_the_positive_integers", part_ok)

    # --- §20-§24: the five worked examples, with the paper's own numbers -----
    stated = {
        "D": {"r": 0, "m": 0},
        "U": {"r": 1, "m": 2},
        "UD": {"r": 1, "m": 1},
        "DU": {"r": 2, "m": 2},
        "UUDD": {"r": 3, "m": 2, "k": 4, "u": 2, "b": 5},
    }
    ex_ok = True
    got = {}
    for w, want in stated.items():
        r = refine[w]
        try:
            m = m_of(w, r)
        except NotACylinder:
            ex_ok = False
            continue
        _, b, _ = compose_affine(w)
        got[w] = {"r": r, "m": m, "b": b}
        if r != want["r"] or m != want["m"]:
            ex_ok = False
        if "b" in want and b != want["b"]:
            ex_ok = False
    # §24 also states the explicit orbit 3 -> 5 -> 8 -> 4 -> 2
    orbit, x = [3], 3
    for _ in range(4):
        x = T(x)
        orbit.append(x)
    if orbit != [3, 5, 8, 4, 2]:
        ex_ok = False
    check("P03_S20_S24_worked_examples_match_the_stated_numbers", ex_ok,
          f"got {got}, orbit {orbit}")
    rep["measured"]["worked_examples"] = got
    rep["measured"]["UUDD_orbit_of_3"] = orbit

    # --- §27: target charts may overlap, unlike source charts ---------------
    # A non-claim again, so it needs a witness rather than an assertion.
    overlap = None
    k = 4
    targets: dict[int, str] = {}
    for w in words(k):
        r = refine[w]
        try:
            m = m_of(w, r)
        except NotACylinder:
            continue
        u = w.count("U")
        for a in range(0, 40):
            n = r + 2 ** k * a
            if n <= 0:
                continue
            y = m + 3 ** u * a
            if y in targets and targets[y] != w:
                overlap = {"target": y, "chart_1": targets[y], "chart_2": w, "depth": k}
                break
            targets.setdefault(y, w)
        if overlap:
            break
    check("P03_S27_target_charts_overlap_witness_exists", overlap is not None,
          "no overlapping target found; §27's non-claim would be unsupported")
    rep["measured"]["target_overlap_witness"] = overlap

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
