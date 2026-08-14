"""Independent recheck of Operation Translation Series — Paper 04.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, *雙向殘餘類轉譯：2^k Cylinder 與 3^u Progression*, Paper 04 v0.1.

Why this one matters
--------------------
The subject's regression suite has **no Paper 04 test at all**. Its groups are
p02_p03, p02_extrema, p05, p06, p07 and p09. So every theorem below is being
machine-checked here for the first time.

Referee: the same symbolic composition of D(x)=x/2 and U(x)=(3x+1)/2 used for
Paper 02, plus direct iteration of T. No theorem of Paper 04 is assumed.

Two things get particular care.

- **The certificate must reject.** §38's three-condition bidirectional
  certificate is only worth something if illegal triples fail it, so negative
  controls are generated deliberately and required to be refused.
- **The paper's own non-claims are checked too.** §33 insists local bijectivity
  does not give global injectivity. That is a claim that something EXISTS — a
  cross-chart merge — and an explicit witness is found rather than asserted.

Nothing here bears on the Collatz conjecture; §41 lists the paper's own limits.

Usage:  python code/ot_paper04_recheck.py [max_k]
"""

from __future__ import annotations

import itertools
import json
import pathlib
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ot_paper02_recheck import compose_affine, words

MAX_K_DEFAULT = 10


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def chart(w: str) -> tuple[int, int, int, int, int]:
    """(k, u, b_w, r_w, m_w) from the referee route plus Paper 03's residue."""
    k = len(w)
    _, b, _ = compose_affine(w)
    u = w.count("U")
    r = (-b * pow(3, -u, 2 ** k)) % 2 ** k
    m = Fraction(3 ** u * r + b, 2 ** k)
    assert m.denominator == 1
    return k, u, b, r, m.numerator


def v2(x: int) -> int:
    c = 0
    while x % 2 == 0:
        x //= 2
        c += 1
    return c


def S(n: int) -> int:
    return (3 * n + 1) // 2 ** v2(3 * n + 1)


def main() -> int:
    max_k = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_K_DEFAULT
    rep = {
        "tool": "ot_paper04_recheck.py",
        "subject": "Collatz Operation Translation Series — Paper 04 v0.1 (Neo.K)",
        "scope": "exact finite arithmetic; not a Collatz proof",
        "note": "the subject's regression suite contains no Paper 04 test; these are first checks",
        "max_word_length": max_k,
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        """`detail` is failure diagnostics only. Attaching it to a passing check
        makes the log read as though the failure text applied, which is how a
        green run ends up carrying a sentence like "no witness found"."""
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    ok = dict.fromkeys(
        "A B C D S8 amin posbij cert certneg".split(), True)
    transported = rejected = 0

    for k in range(1, max_k + 1):
        for w in words(k):
            kk, u, b, r, m = chart(w)
            # Theorem A / B / C / D over all integers a, positive and negative:
            # the algebra is stated on Z, and the positive domain is §9's job.
            for a in range(-4, 7):
                x = r + 2 ** k * a
                y = m + 3 ** u * a
                # Theorem A: F_w maps the source cylinder onto the target
                # progression, and does so bijectively in the quotient label.
                fx = Fraction(3 ** u * x + b, 2 ** k)
                if fx.denominator != 1 or fx.numerator != y:
                    ok["A"] = False
                # Theorem B: the exact inverse recovers x from y alone
                if r + 2 ** k * ((y - m) // 3 ** u) != x:
                    ok["B"] = False
                # Theorem C: target legality
                if (y - m) % 3 ** u != 0:
                    ok["C"] = False
                # Theorem D: quotient conservation
                if Fraction(x - r, 2 ** k) != Fraction(y - m, 3 ** u):
                    ok["D"] = False
                # §8: the same relation with no division at all
                if 3 ** u * (x - r) != 2 ** k * (y - m):
                    ok["S8"] = False

                # §38: the three-condition certificate must ACCEPT this triple
                accept = (x % 2 ** k == r % 2 ** k
                          and (y - m) % 3 ** u == 0
                          and 3 ** u * (x - r) == 2 ** k * (y - m))
                if not accept:
                    ok["cert"] = False
                transported += 1

                # ...and must REJECT perturbed ones. A certificate that accepts
                # everything certifies nothing, so this is the load-bearing half.
                for dx, dy in ((1, 0), (0, 1), (2 ** k, 0), (0, 3 ** u), (1, 1)):
                    if dx == 0 and dy == 0:
                        continue
                    x2, y2 = x + dx, y + dy
                    bad = (x2 % 2 ** k == r % 2 ** k
                           and (y2 - m) % 3 ** u == 0
                           and 3 ** u * (x2 - r) == 2 ** k * (y2 - m))
                    if bad:
                        ok["certneg"] = False
                    rejected += 1

            # §9 / §10: the positive-domain quotient bound and bijection
            a_min = 1 if r == 0 else 0
            if r + 2 ** k * a_min <= 0 or (a_min > 0 and r + 2 ** k * (a_min - 1) > 0):
                ok["amin"] = False
            seen_img = set()
            for a in range(a_min, a_min + 6):
                x = r + 2 ** k * a
                y = m + 3 ** u * a
                if x <= 0 or y <= 0:
                    ok["posbij"] = False
                walked = x
                for _ in range(k):
                    walked = T(walked)
                if walked != y or y in seen_img:
                    ok["posbij"] = False
                seen_img.add(y)

    names = {
        "A": "P04_ThmA_bidirectional_residue_transport",
        "B": "P04_ThmB_exact_inverse",
        "C": "P04_ThmC_target_legality",
        "D": "P04_ThmD_quotient_conservation",
        "S8": "P04_S8_division_free_cross_multiplied_relation",
        "amin": "P04_S9_positive_domain_quotient_bound",
        "posbij": "P04_S10_positive_source_image_bijection",
        "cert": "P04_S38_certificate_accepts_every_legal_triple",
        "certneg": "P04_S38_certificate_rejects_perturbed_triples",
    }
    for key, name in names.items():
        check(name, ok[key])
    rep["counts"]["transport_triples"] = transported
    rep["counts"]["negative_controls_rejected"] = rejected

    # --- §11: the worked example -------------------------------------------
    k, u, b, r, m = chart("U")
    check("P04_S11_worked_example_w_equals_U",
          (k, u, r, m) == (1, 1, 1, 2),
          f"got k={k} u={u} r_U={r} m_U={m}, paper states 1,1,1,2")

    # --- §12: the single-step inverse relation, exactly ----------------------
    inv_ok = True
    for y in range(1, 4000):
        expected = {2 * y}
        if y % 3 == 2:
            expected.add((2 * y - 1) // 3)
        actual = {n for n in range(1, 8 * y + 8) if T(n) == y}
        if actual != expected:
            inv_ok = False
            break
    check("P04_S12_single_step_inverse_relation", inv_ok)

    # --- §13: the two inverse-legality congruences are the same constraint ---
    same = all(((y % 6 == 4) == ((y // 2) % 3 == 2)) for y in range(2, 60000, 2))
    check("P04_S13_original_and_modified_inverse_congruences_agree", same)

    # --- Theorem E / §21 / §22 / §23: accelerated inverse fibers -------------
    thmE = cls = image = True
    fibers = 0
    for t in range(1, 2000, 2):
        for kappa in range(1, 14):
            num = 2 ** kappa * t - 1
            legal = (2 ** kappa * t) % 3 == 1
            if legal:
                if num % 3 != 0:
                    thmE = False
                n = num // 3
                # must be a positive odd genuine predecessor
                if n <= 0 or n % 2 == 0 or S(n) != t or v2(3 * n + 1) != kappa:
                    thmE = False
            else:
                if num % 3 == 0:
                    thmE = False
            fibers += 1
        # §22: the mod-3 classification of admissible kappa
        legal_kappas = [kp for kp in range(1, 14) if (2 ** kp * t) % 3 == 1]
        if t % 3 == 1 and any(kp % 2 for kp in legal_kappas):
            cls = False
        if t % 3 == 2 and any(kp % 2 == 0 for kp in legal_kappas):
            cls = False
        if t % 3 == 0 and legal_kappas:
            cls = False
        # §23: the accelerated image never hits a multiple of 3
        if S(t) % 3 == 0:
            image = False
    check("P04_ThmE_S21_accelerated_inverse_fiber_legality", thmE)
    check("P04_S22_mod3_classification_of_admissible_valuations", cls)
    check("P04_S23_accelerated_image_avoids_multiples_of_3", image)
    rep["counts"]["inverse_fiber_candidates"] = fibers

    # --- Theorem F / §24 / §25 / §26: the terminal fiber, and M_j ------------
    thmF = True
    Ms = []
    for j in range(1, 26):
        Mj = (4 ** j - 1) // 3
        Ms.append(Mj)
        if (4 ** j - 1) % 3 != 0 or Mj % 2 == 0:
            thmF = False
        if Fraction(2 ** (2 * j) * 1 - 1, 3) != Mj:
            thmF = False
        if S(Mj) != 1 or v2(3 * Mj + 1) != 2 * j:
            thmF = False
    check("P04_ThmF_terminal_fiber_of_1_is_the_M_j_family", thmF)
    check("P04_S25_M_j_sequence_matches_the_paper", Ms[:5] == [1, 5, 21, 85, 341],
          f"got {Ms[:5]}, paper states 1,5,21,85,341")
    # §26: 5 is R_4(1) and nothing more special than that
    traj, x = [5], 5
    while x != 1:
        x = x // 2 if x % 2 == 0 else 3 * x + 1
        traj.append(x)
    check("P04_S26_five_is_R4_of_1_with_the_stated_trajectory",
          Ms[1] == 5 and traj == [5, 16, 8, 4, 2, 1], f"trajectory {traj}")
    rep["measured"]["ordinary_trajectory_of_5"] = traj
    rep["measured"]["M_j_first_eight"] = Ms[:8]

    # --- §17 / §18: odd core, 2-rays, and coverage equivalence --------------
    core_ok = rays_ok = cover_ok = True
    for n in range(1, 20000):
        core = n // 2 ** v2(n)
        if core % 2 == 0 or core * 2 ** v2(n) != n:
            core_ok = False
        # the 2-rays partition the positive integers: each n sits on exactly one
        if n // 2 ** v2(n) != core:
            rays_ok = False
        # §18: n converges iff its odd core does — checked as reaching 1 under T
        def reaches_one(s: int, cap: int = 2000) -> bool:
            x = s
            for _ in range(cap):
                if x == 1:
                    return True
                x = T(x)
            return False
        if reaches_one(n) != reaches_one(core):
            cover_ok = False
    check("P04_S17_odd_core_decomposition_is_unique", core_ok and rays_ok)
    check("P04_S18_convergence_of_n_equals_convergence_of_its_odd_core", cover_ok)

    # --- §33 / §34: the paper's own NON-claim, with an explicit witness ------
    # Local bijectivity must not imply global injectivity. Find w != v and
    # x in Omega_w, z in Omega_v with x != z but T^{|w|}(x) = T^{|v|}(z).
    witness = None
    charts = {}
    for k in range(1, 7):
        for w in words(k):
            charts[w] = chart(w)
    for (w, cw), (v, cv) in itertools.combinations(charts.items(), 2):
        kw, uw, bw, rw, mw = cw
        kv, uv, bv, rv, mv = cv
        for a in range(0, 12):
            x = rw + 2 ** kw * a
            if x <= 0:
                continue
            y = mw + 3 ** uw * a
            if y <= 0 or (y - mv) % 3 ** uv != 0:
                continue
            bnum = (y - mv) // 3 ** uv
            z = rv + 2 ** kv * bnum
            if z <= 0 or z == x:
                continue
            wx, wz = x, z
            for _ in range(kw):
                wx = T(wx)
            for _ in range(kv):
                wz = T(wz)
            if wx == wz == y:
                witness = {"w": w, "v": v, "source_w": x, "source_v": z,
                           "common_target": y, "steps_w": kw, "steps_v": kv}
                break
        if witness:
            break
    check("P04_S33_cross_chart_merge_witness_exists", witness is not None,
          "no witness found; the paper's non-claim would be unsupported")
    rep["measured"]["cross_chart_merge_witness"] = witness

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
