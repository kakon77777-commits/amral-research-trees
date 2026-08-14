"""Independent recheck of Operation Translation Series — Paper 02.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *Collatz Local Affine Atlas*, Paper 02 v0.1.1.

Independence
------------
This file is written from the paper's *statements*, not from the package's
`tools/verify_math_claims.py`. Every quantity is computed by at least two
routes that do not share a derivation:

  route 1  symbolic composition of the branch operators D(x)=x/2 and
           U(x)=(3x+1)/2 on an affine form, using nothing but their
           definitions — this assumes no theorem of the paper at all
  route 2  the closed form of Theorem C
  route 3  the upper-triangular matrix product of Theorem E
  route 4  (transport only) the k-step congruence tables of this arm's own
           Rust engine, which are derived by direct simulation

Route 1 is the referee. If a theorem is false, route 1 is what disagrees with
it, because route 1 never used it.

Scope: exact finite algebra. Nothing here bears on the Collatz conjecture.

Usage:  python code/ot_paper02_recheck.py [max_k]
"""

from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction

MAX_K_DEFAULT = 16


def words(k: int):
    """All 2^k words of length k over {D, U}, read left to right."""
    for bits in itertools.product("DU", repeat=k):
        yield "".join(bits)


# --- route 1: no theorem assumed ------------------------------------------
def compose_affine(word: str) -> tuple[int, int, int]:
    """Apply the operators one at a time to the affine form (A*x + B)/Dn.

    D: (A x + B)/Dn      -> (A x + B)/(2 Dn)
    U: (A x + B)/Dn      -> (3(A x + B)/Dn + 1)/2 = (3A x + 3B + Dn)/(2 Dn)

    Both lines are read straight off the definitions of D and U in §1.
    """
    A, B, Dn = 1, 0, 1
    for c in word:
        if c == "D":
            Dn = 2 * Dn
        else:
            A, B, Dn = 3 * A, 3 * B + Dn, 2 * Dn
    return A, B, Dn


# --- route 2: Theorem C ----------------------------------------------------
def closed_form_b(word: str) -> int:
    positions = [j + 1 for j, c in enumerate(word) if c == "U"]  # 1-indexed j_t
    u = len(positions)
    return sum(2 ** (jt - 1) * 3 ** (u - t) for t, jt in enumerate(positions, start=1))


# --- route 3: Theorem E ----------------------------------------------------
def matrix_b(word: str) -> tuple[int, int, int]:
    """M_w = M_{sigma_k} ... M_{sigma_1}, with M_D and M_U from §15."""
    M = [[1, 0], [0, 1]]
    MD = [[1, 0], [0, 2]]
    MU = [[3, 1], [0, 2]]
    for c in word:
        N = MD if c == "D" else MU
        # left-multiply, because the newest letter is applied last
        M = [
            [N[0][0] * M[0][0], N[0][0] * M[0][1] + N[0][1] * M[1][1]],
            [0, N[1][1] * M[1][1]],
        ]
    return M[0][0], M[0][1], M[1][1]


def actual_word(n: int, k: int) -> tuple[str, int]:
    """The genuine parity word of n, by running T. Used for admissibility."""
    out = []
    x = n
    for _ in range(k):
        if x % 2 == 0:
            out.append("D")
            x //= 2
        else:
            out.append("U")
            x = (3 * x + 1) // 2
    return "".join(out), x


def check(report: dict, name: str, condition: bool, detail: str = "") -> None:
    report["checks"][name] = {"pass": bool(condition), **({"detail": detail} if detail else {})}
    if not condition:
        report["failures"].append(name + (f": {detail}" if detail else ""))


def main() -> int:
    max_k = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_K_DEFAULT
    report = {
        "tool": "ot_paper02_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 02 v0.1.1 (Neo.K)",
        "scope": "exact finite algebra only; says nothing about the Collatz conjecture",
        "max_word_length": max_k,
        "checks": {},
        "counts": {},
        "failures": [],
    }

    # ---- Theorems A, B, C, E, across every word up to max_k ---------------
    words_checked = 0
    thmA = thmB = thmC = thmE = True
    b_table: dict[str, int] = {}
    for k in range(1, max_k + 1):
        for w in words(k):
            A, B, Dn = compose_affine(w)
            u = w.count("U")
            b_table[w] = B
            words_checked += 1

            # Theorem A: the composition really is (3^u x + b)/2^k
            if A != 3 ** u or Dn != 2 ** k:
                thmA = False
            # Theorem C: closed form agrees with the composition
            if closed_form_b(w) != B:
                thmC = False
            # Theorem E: matrix product agrees with the composition
            if matrix_b(w) != (A, B, Dn):
                thmE = False
            # Theorem B: the two recurrences, checked against the prefix
            if k > 1:
                head, last = w[:-1], w[-1]
                bh = b_table[head]
                expect = bh if last == "D" else 3 * bh + 2 ** (k - 1)
                if expect != B:
                    thmB = False

    check(report, "ThmA_finite_word_affine_closure", thmA)
    check(report, "ThmB_correction_recurrence", thmB)
    check(report, "ThmC_closed_form_of_b", thmC)
    check(report, "ThmE_matrix_representation", thmE)
    report["counts"]["words_checked"] = words_checked

    # ---- Theorem D: concatenation ----------------------------------------
    thmD = True
    pairs = 0
    for kw in range(1, min(max_k, 8) + 1):
        for kv in range(1, min(max_k, 8) + 1):
            for w in words(kw):
                for v in words(kv):
                    _, b_wv, _ = compose_affine(w + v)
                    if b_wv != 3 ** v.count("U") * b_table[w] + 2 ** kw * b_table[v]:
                        thmD = False
                    pairs += 1
    check(report, "ThmD_concatenation_law", thmD)
    report["counts"]["concatenation_pairs"] = pairs

    # ---- Theorem F and the §25 width formula ------------------------------
    thmF = width_ok = argext_ok = True
    ku_cases = 0
    for k in range(1, max_k + 1):
        by_u: dict[int, list[tuple[int, str]]] = {}
        for w in words(k):
            by_u.setdefault(w.count("U"), []).append((b_table[w], w))
        for u, vals in by_u.items():
            lo, w_lo = min(vals)
            hi, w_hi = max(vals)
            if lo != 3 ** u - 2 ** u or hi != 2 ** (k - u) * (3 ** u - 2 ** u):
                thmF = False
            if hi - lo != (2 ** (k - u) - 1) * (3 ** u - 2 ** u):
                width_ok = False
            # §21: the extremes are attained at U^u D^{k-u} and D^{k-u} U^u.
            # For u = 0 every word is D^k and the argmin/argmax are not unique,
            # so the claim is checked as "the stated word attains the extreme".
            if b_table["U" * u + "D" * (k - u)] != lo:
                argext_ok = False
            if b_table["D" * (k - u) + "U" * u] != hi:
                argext_ok = False
            ku_cases += 1
    check(report, "ThmF_order_extremal_bounds", thmF)
    check(report, "S21_extremes_attained_at_stated_words", argext_ok)
    check(report, "S25_correction_width_formula", width_ok)
    report["counts"]["(k,u)_cases"] = ku_cases

    # ---- §30 / Paper 03 preview: residue cylinder and transport -----------
    # r_w = -b_w * 3^{-u} mod 2^k, Omega_w = (r_w + 2^k Z) cap Z_{>0},
    # and T^k(r_w + 2^k a) = m_w + 3^u a with m_w = F_w(r_w).
    residue_bijection = admissible = transport = m_integral = True
    transport_cases = 0
    max_k_res = min(max_k, 14)
    for k in range(1, max_k_res + 1):
        seen = set()
        for w in words(k):
            u = w.count("U")
            b = b_table[w]
            r = (-b * pow(3, -u, 2 ** k)) % 2 ** k
            if r in seen:
                residue_bijection = False
            seen.add(r)

            m_w = Fraction(3 ** u * r + b, 2 ** k)
            if m_w.denominator != 1:
                m_integral = False
            for a in range(0, 6):
                n = r + 2 ** k * a
                if n <= 0:
                    continue  # r = 0 with a = 0 leaves the positive domain
                aw, y = actual_word(n, k)
                if aw != w:
                    admissible = False
                if y != m_w.numerator + 3 ** u * a:
                    transport = False
                transport_cases += 1
        if len(seen) != 2 ** k:
            residue_bijection = False
    check(report, "P03_parity_word_to_residue_is_a_bijection", residue_bijection)
    check(report, "P03_residue_cylinder_is_the_admissible_domain", admissible)
    check(report, "P03_m_w_is_an_integer", m_integral)
    check(report, "P03_exact_cylinder_transport", transport)
    report["counts"]["transport_cases"] = transport_cases
    report["counts"]["residue_max_k"] = max_k_res

    # ---- the r_w = 0 boundary the repair was about ------------------------
    # AUDIT_AND_CORRECTIONS records that the all-D cylinder has canonical
    # r_w = 0, which the positive-integer domain excludes, and that the repaired
    # proof uses the representative r_w + 2^k. Checked directly.
    allD_ok = True
    for k in range(1, max_k_res + 1):
        w = "D" * k
        u, b = 0, b_table[w]
        r = (-b * pow(3, -u, 2 ** k)) % 2 ** k
        if r != 0:
            allD_ok = False
        rep = r + 2 ** k
        aw, y = actual_word(rep, k)
        if aw != w or y != 1:
            allD_ok = False
        m_w = Fraction(3 ** u * rep + b, 2 ** k)
        if m_w.denominator != 1:
            allD_ok = False
    check(report, "P02_repair_allD_cylinder_needs_the_r_plus_2k_representative", allD_ok)

    report["ok"] = not report["failures"]
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
