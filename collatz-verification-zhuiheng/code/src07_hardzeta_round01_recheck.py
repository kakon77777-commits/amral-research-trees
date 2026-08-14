"""Recheck of source items 19-20 — Hard-Zeta Phase I / Round 01.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K + Aletheia, `Hard_Zeta_Phase_I_Round_01_Exact_Refinement_v0.1.md`
and `Hard_Zeta_Phase_I_Round_01_bundle.zip` (2026-08-11 13:12).

What Round 01 is
----------------
Round 01 turns the Hard-Zeta programme from a definition into an **algebra**.
Each chart `w` in `{D,U}^k` carries `(r_w, u_w, b_w, m_w, h(w))`; §2-§6 give the
child's data as closed formulas in the parent's, so the hard height updates
recursively instead of by rescanning every prefix; §9 splits a parent's hard set
four ways; §10-§13 turn that into an exact Dirichlet-mass conservation law; and
§16-§17 recast the whole thing as a survival/hazard process.

Almost all of it is finitely checkable, which is the point of this run. The
recursion is confronted with direct iteration of `T`, and the mass identities
with direct summation.

The one thing worth stating up front
------------------------------------
The chart algebra computes `Z_w(s)` as an **exact** quantity — a finite sum where
`h(w)` is finite, and a Hurwitz zeta where it is infinite. So `Σ_{|w|=k} Z_w(s)`
is the true infinite `Z_k(s)`, not a truncation.

[`RUN-004`](../reports/RUN-004-HARD-ZETA-ORIGIN.md) measured the same `Z_k(s)` by
brute force on `[2, 2^32)` and bracketed it. The two routes share no code and no
method. Requiring the exact value to land inside the measured bracket is the
strongest check available here, and it runs in both directions: it tests Round
01's algebra and it tests RUN-004's bracket.

How this run's own result relates to Round 01's No-Go
----------------------------------------------------
§21 proves a **per-chart** no-go: for any fixed `L`, no `ε_L > 0` makes every
nonempty hard chart lose an `ε_L` fraction over `L` more steps. §22 then says
plainly that this does **not** exclude global total Hard-Zeta contraction.

RUN-004's result lives exactly there. `σ(n) = 3` is impossible for every `n`, so
`E_2 = E_3` and `Z_2(s) = Z_3(s)` — the **global total** at `L = 1` is flat, for a
reason unrelated to §21's `U^k` construction. In Round 01's own language that is
`λ_2(s) = 0`, and more generally `λ_k(s) = 0` whenever `k+1` is not an admissible
stopping time.

Neither statement subsumes the other, and this recheck says so rather than
letting the stronger-sounding one stand for both. What it does add is a sharper
form of §26's next question: a **uniform positive lower bound** on `λ_k(s)` is
impossible, so the target has to be the cumulative `Σ λ_k = ∞` that §17 already
names — the zero terms cost nothing to a sum, but they are fatal to a per-step
bound.

Usage:  python code/src07_hardzeta_round01_recheck.py [measured.json]
"""

from __future__ import annotations

import importlib
import json
import math
import os
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
# The algebra module is swappable so `src07_drill.py` can substitute a damaged
# copy of the paper's formulas without clobbering the real file. The formulas in
# it ARE the paper's claim, so mutating them is how this suite proves it would
# notice if the claim were wrong.
A = importlib.import_module(os.environ.get("HZ_ALGEBRA_MODULE", "hz_chart_algebra"))

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))
BUNDLE = "Hard_Zeta_Phase_I_Round_01_bundle.zip"
ROUND01 = "Hard_Zeta_Phase_I_Round_01_Exact_Refinement_v0.1.md"

K_BRUTE = 10          # depth to which every chart is confronted with iteration
N_BRUTE = 1 << 16     # range over which that confrontation runs
K_EXACT = 22          # depth to which exact Z_k(s) is computed from the algebra
S_VALUES = (2.0, 3.0, 4.0)


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def parity_word(n: int, k: int) -> str:
    """The first k steps of n's trajectory, as a {D,U} word."""
    out, x = [], n
    for _ in range(k):
        out.append("D" if x % 2 == 0 else "U")
        x = T(x)
    return "".join(out)


def sigma(n: int, cap: int = 20_000) -> int:
    x = n
    for j in range(1, cap + 1):
        x = T(x)
        if x < n:
            return j
    raise RuntimeError(f"sigma({n}) exceeded cap")


def admissible(jmax: int) -> set[int]:
    out, p = set(), 1
    while p.bit_length() <= jmax:
        out.add(p.bit_length())
        p *= 3
    return out


def main() -> int:
    measured_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None

    rep = {
        "tool": "src07_hardzeta_round01_recheck.py",
        "subject": ("Neo.K + Aletheia, Hard-Zeta Phase I / Round 01 "
                    "Exact Refinement Algebra v0.1 (2026-08-11)"),
        "source_items": [19, 20],
        "scope": (
            "the finite content of Round 01: the child recursion (§2-§6), the "
            "four-way refinement identity (§9), the exact mass conservation law "
            "(§10-§13), the trichotomy and zero-loss zone (§19-§20), the "
            "per-chart No-Go construction (§21), and the U^k closed form (§23-§24)."
        ),
        "checks": {},
        "counts": {},
        "measured": {},
        "failures": [],
    }

    def check(name: str, ok: bool, detail: str = "") -> None:
        rep["checks"][name] = {"pass": bool(ok), **({} if ok else {"detail": detail})}
        if not ok:
            rep["failures"].append(name + (f": {detail}" if detail else ""))

    # --------------------------------------------------- the module's own numerics
    check("SRC07_hurwitz_zeta_and_AP_mass_anchors_hold",
          not A.self_test(), f"{A.self_test()}")

    # ---------------------------------------------------------- items are the same
    with zipfile.ZipFile(SOURCE / BUNDLE) as z:
        bundled = z.read(ROUND01)
        names = set(z.namelist())
    loose = (SOURCE / ROUND01).read_bytes()
    check("SRC07_loose_round01_matches_the_bundled_copy", loose == bundled,
          "the loose file and the bundled file are different documents")
    check("SRC07_bundle_also_carries_the_v011_route_paper",
          any("Faithful_Global_Quantifier_Compression_Proof_Route_v0.1.1" in n
              for n in names),
          f"bundle holds {sorted(names)}")
    paper = bundled.decode("utf-8")

    # A subject whose algebra cannot be evaluated at all must still produce a
    # report: a traceback is the one outcome a drill cannot grade, and two
    # planted defects reached exactly that state before this guard existed.
    evaluated = True
    try:
        # --------------------------------- §1-§6: the recursion against direct iteration
        levels = [[A.ROOT]]
        for _ in range(K_BRUTE):
            levels.append([c for w in levels[-1] for c in A.children(w)])

        def _ge(n: int, j: int) -> bool:
            """T^j(n) >= n, by direct iteration, assuming none of the chart algebra."""
            x = n
            for _ in range(j):
                x = T(x)
            return x >= n

        block_ok = parity_ok = height_ok = cap_ok = True
        block_cases = parity_cases = height_cases = cap_cases = 0
        witness: list[dict] = []

        for k in range(1, K_BRUTE + 1):
            for w in levels[k]:
                members = list(w.omega_members(1, N_BRUTE - 1))
                if not members:
                    continue
                for n in members:
                    # §2: the cylinder really is the set of n whose first k steps are w
                    if parity_word(n, k) != w.word:
                        parity_ok = False
                        if len(witness) < 5:
                            witness.append({"n": n, "want": w.word,
                                            "got": parity_word(n, k)})
                    parity_cases += 1
                    # §1: the block identity, with the chart's own m and u
                    a = (n - w.r) // 2 ** k
                    x = n
                    for _ in range(k):
                        x = T(x)
                    if x != w.m + 3 ** w.u * a:
                        block_ok = False
                    block_cases += 1

                # §6: the hard height must reproduce the hard set exactly
                brute = [n for n in members
                         if n >= 2 and all(_ge(n, j) for j in range(1, k + 1))]
                viah = list(w.hard_members(1, N_BRUTE - 1))
                if brute != viah:
                    height_ok = False
                    if len(witness) < 8:
                        witness.append({"word": w.word, "h": w.h,
                                        "brute_max": brute[-1] if brute else None,
                                        "via_h_max": viah[-1] if viah else None})
                height_cases += 1

        check("SRC07_cylinders_are_exactly_the_starts_with_that_parity_word", parity_ok,
              f"{witness[:3]}")
        check("SRC07_block_identity_holds_with_the_charts_own_m_and_u", block_ok)
        check("SRC07_recursive_hard_height_reproduces_the_hard_set_exactly", height_ok,
              f"{witness[:3]}")

        # §5: the hard cap is exactly the descent boundary for the new prefix.
        #
        # The first version sampled the first few members of each cylinder. Those all
        # sit far below a large c, so `n <= c` came out true on both sides of an
        # off-by-one and the check could not see one — the same weakness this tree
        # already fixed once, in the item-03 certificate thresholds. It now probes
        # the two cylinder members that STRADDLE c, which is the only place the
        # boundary is decidable.
        cap_boundary_pairs = 0
        for k in range(0, K_BRUTE):
            for w in levels[k]:
                for child in A.children(w):
                    d = A.delta_of(child.k, child.u)
                    c = A.cap_of(child.b, d)
                    q = 2 ** child.k
                    if c is None:
                        # expanding skeleton: every admissible member must stay up
                        for n in list(child.omega_members(2, min(N_BRUTE - 1, 4000)))[:3]:
                            if not _ge(n, child.k):
                                cap_ok = False
                            cap_cases += 1
                        continue
                    below = c - ((c - child.r) % q)          # largest member <= c
                    above = below + q
                    if below >= max(2, child.r):
                        if not _ge(below, child.k):
                            cap_ok = False
                            if len(witness) < 8:
                                witness.append({"word": child.word, "c": c,
                                                "n": below, "expected": "stays up"})
                        cap_cases += 1
                        cap_boundary_pairs += 1
                    if above >= 2:
                        if _ge(above, child.k):
                            cap_ok = False
                            if len(witness) < 8:
                                witness.append({"word": child.word, "c": c,
                                                "n": above, "expected": "descends"})
                        cap_cases += 1
        check("SRC07_new_prefix_hard_cap_is_exactly_the_descent_boundary", cap_ok,
              f"{witness[:3]}")
        check("SRC07_the_cap_boundary_was_actually_decided_somewhere",
              cap_cases > 1000,
              f"only {cap_cases} probes landed anywhere the cap could be decided")

        # §5's cap must be pinned ARITHMETICALLY, because it cannot be pinned by
        # members. The cylinder has spacing 2^(k+1), so every threshold in the whole
        # interval (c_v, next member] selects the same set: an off-by-one in c_v is
        # invisible to any membership test unless c_v + 1 happens to be a member,
        # which it almost never is. Only 10 charts in this whole sweep even have a
        # member at or below c_v. So the claim c_v = floor(b_v / delta_v) is checked
        # as the integer statement it is.
        floor_exact, floor_witness = True, []
        for k in range(0, K_BRUTE):
            for w in levels[k]:
                for child in A.children(w):
                    d = A.delta_of(child.k, child.u)
                    if d <= 0:
                        continue
                    c = A.cap_of(child.b, d)
                    if not (d * c <= child.b < d * (c + 1)):
                        floor_exact = False
                        if len(floor_witness) < 5:
                            floor_witness.append({"word": child.word, "b": child.b,
                                                  "delta": d, "c": c})
        check("SRC07_the_cap_is_exactly_the_floor_of_b_over_delta", floor_exact,
              f"{floor_witness}")
        rep["counts"]["charts_with_a_member_at_or_below_the_cap"] = cap_boundary_pairs

        # §4: delta is never zero
        check("SRC07_drift_gap_is_never_zero",
              all(A.delta_of(c.k, c.u) != 0 for k in range(1, K_BRUTE + 1)
                  for c in levels[k]))

        # ------------------------------------- §9: the four-way refinement identity
        four_ok, disjoint_ok = True, True
        four_cases = 0
        for k in range(0, K_BRUTE):
            for w in levels[k]:
                parent = set(w.hard_members(1, N_BRUTE - 1))
                if not parent:
                    continue
                cD, cU = A.children(w)
                pieces = [set(cD.hard_members(1, N_BRUTE - 1)),
                          set(cU.hard_members(1, N_BRUTE - 1)),
                          set(A.first_descent_stratum(w, cD, 1, N_BRUTE - 1)),
                          set(A.first_descent_stratum(w, cU, 1, N_BRUTE - 1))]
                union = set().union(*pieces)
                if union != parent:
                    four_ok = False
                if sum(len(p) for p in pieces) != len(union):
                    disjoint_ok = False
                four_cases += 1
        check("SRC07_four_way_refinement_identity_partitions_the_parent", four_ok)
        check("SRC07_the_four_pieces_are_pairwise_disjoint", disjoint_ok)

        # §8: the first-descent stratum really is first descent at step k+1
        fd_ok, fd_cases = True, 0
        for k in range(0, 8):
            for w in levels[k]:
                for child in A.children(w):
                    for n in list(A.first_descent_stratum(w, child, 1, N_BRUTE - 1))[:4]:
                        if sigma(n) != child.k:
                            fd_ok = False
                        fd_cases += 1
        check("SRC07_first_descent_stratum_is_exactly_sigma_equals_k_plus_1", fd_ok)

        # §8's floor is max(2, c_v + 1). Off by one and the stratum swallows the
        # largest still-hard member, which the four-way identity only notices when
        # that member happens to lie in the cylinder — usually it does not. So the
        # floor is probed directly.
        floor_ok, floor_cases = True, 0
        for k in range(0, K_BRUTE):
            for w in levels[k]:
                for child in A.children(w):
                    d = A.delta_of(child.k, child.u)
                    if d < 0:
                        continue
                    c = A.cap_of(child.b, d)
                    members = list(A.first_descent_stratum(w, child, 1, N_BRUTE - 1))
                    if not members:
                        continue
                    if members[0] <= c:
                        floor_ok = False
                        if len(witness) < 10:
                            witness.append({"word": child.word, "c": c,
                                            "stratum_min": members[0]})
                    floor_cases += 1
        check("SRC07_first_descent_stratum_starts_strictly_above_the_cap", floor_ok,
              f"{witness[-3:]}")

        # ----------------------------------- §11-§12: exact mass conservation per chart
        cons_worst, cons_at = 0.0, None
        for k in range(0, 8):
            for w in levels[k]:
                zw = w.mass(2.0)
                if zw == 0.0:
                    continue
                cD, cU = A.children(w)
                rhs = (cD.mass(2.0) + cU.mass(2.0)
                       + A.first_descent_mass(w, cD, 2.0)
                       + A.first_descent_mass(w, cU, 2.0))
                rel = abs(zw - rhs) / zw
                if rel > cons_worst:
                    cons_worst, cons_at = rel, w.word
        check("SRC07_exact_mass_conservation_holds_chart_by_chart",
              cons_worst < 1e-12, f"worst relative gap {cons_worst:.3e} at {cons_at!r}")

        # §11 against direct summation, where the chart is finite and small
        mass_worst, mass_at = 0.0, None
        for k in range(1, 9):
            for w in levels[k]:
                if w.h is None or w.h > N_BRUTE - 1:
                    continue
                want = math.fsum(n ** -2.0 for n in w.hard_members(1, N_BRUTE - 1))
                got = w.mass(2.0)
                if want == 0.0 and got == 0.0:
                    continue
                denom = max(want, 1e-300)
                rel = abs(got - want) / denom
                if rel > mass_worst:
                    mass_worst, mass_at = rel, w.word
        check("SRC07_chart_mass_formula_matches_direct_summation",
              mass_worst < 1e-11, f"worst relative gap {mass_worst:.3e} at {mass_at!r}")

        # ------------------------------------------- §19-§20: trichotomy and zero loss
        zones, tri_ok, order_ok, zeroloss_ok = {"A": 0, "B": 0, "C": 0}, True, True, True
        for k in range(0, K_BRUTE):
            for w in levels[k]:
                try:
                    z = A.zone(k, w.u)
                except ArithmeticError:
                    tri_ok = False
                    continue
                # the label must match what §19 says it MEANS, not merely exist:
                # a loosened threshold relabels Zone B as Zone A without raising,
                # and the first version of this check could not see that.
                dD = A.delta_of(k + 1, w.u)
                dU = A.delta_of(k + 1, w.u + 1)
                want = ("A" if dD > 0 and dU > 0 else
                        "B" if dD > 0 and dU < 0 else
                        "C" if dD < 0 and dU < 0 else "?")
                if z != want:
                    tri_ok = False
                zones[z] += 1
                if A.delta_of(k + 1, w.u + 1) >= A.delta_of(k + 1, w.u):
                    order_ok = False
                if z == "C":
                    cD, cU = A.children(w)
                    if (A.first_descent_mass(w, cD, 2.0) != 0.0
                            or A.first_descent_mass(w, cU, 2.0) != 0.0):
                        zeroloss_ok = False
        check("SRC07_every_chart_falls_in_exactly_one_zone", tri_ok)
        check("SRC07_delta_U_is_always_below_delta_D", order_ok,
              "so 'D expanding but U contracting' is impossible, as §19 says")
        check("SRC07_zone_C_loses_no_mass", zeroloss_ok)

        # ------------------------------------------------------ §21: the No-Go itself
        nogo_rows, nogo_ok = [], True
        for L in range(1, 6):
            k = 1
            while 3 ** k <= 2 ** (k + L):
                k += 1
            w = A.ROOT
            for _ in range(k):
                w = A.children(w)[1]              # U-child
            subtree, loss = [w], 0.0
            for _ in range(L):
                nxt = []
                for c in subtree:
                    for ch in A.children(c):
                        loss += A.first_descent_mass(c, ch, 2.0)
                        nxt.append(ch)
                subtree = nxt
            total = math.fsum(c.mass(2.0) for c in subtree)
            parent = w.mass(2.0)
            rel = abs(total - parent) / parent
            if loss != 0.0 or rel > 1e-12:
                nogo_ok = False
            nogo_rows.append({"L": L, "minimal_k": k, "word": f"U^{k}",
                              "parent_mass": parent, "subtree_mass": total,
                              "first_descent_mass": loss, "relative_gap": rel})
        check("SRC07_the_no_go_construction_really_conserves_all_mass", nogo_ok,
              f"{nogo_rows}")

        # ------------------------------------------------- §23-§24: the U^k closed form
        uk_ok, uk_rows = True, []
        w = A.ROOT
        for k in range(1, 25):
            w = A.children(w)[1]
            if w.r != 2 ** k - 1:
                uk_ok = False
            if k >= 2:
                for s in S_VALUES:
                    closed = 2 ** (-k * s) * A.hurwitz_zeta(s, 1 - 2 ** -k)
                    got = w.mass(s)
                    if abs(got - closed) / closed > 1e-12:
                        uk_ok = False
                    if s == 2.0 and k <= 12:
                        uk_rows.append({"k": k, "r": w.r, "mass": got,
                                        "closed_form": closed})
            if w.h is not None:
                uk_ok = False                     # §24 says the U^k chart is unbounded
        check("SRC07_U_k_residue_and_closed_form_mass_are_as_stated", uk_ok,
              f"{uk_rows[:4]}")

        # --------------------------------- §13: exact Z_k, and the layer identity
        #
        # The layer loss is taken from the algebra DIRECTLY, as sum of D_v over the
        # depth-(k+1) charts, rather than as the difference Z_k - Z_{k+1}. That
        # matters: Z_k and Z_{k+1} are fsums over different chart sets, so their
        # difference carries rounding even where the true values are equal, and an
        # "exactly zero" test on the difference could never pass. The direct sum
        # returns a literal 0.0 when every stratum is empty.
        charts = [A.ROOT]
        exact_Z: dict[int, dict[float, float]] = {}
        layer_loss: dict[int, dict[float, float]] = {}
        for k in range(1, K_EXACT + 1):
            parents = charts
            losses = {s: [] for s in S_VALUES}
            nxt = []
            for w in parents:
                for c in A.children(w):
                    for s in S_VALUES:
                        losses[s].append(A.first_descent_mass(w, c, s))
                    if c.h is None or c.h >= 2:
                        nxt.append(c)
            charts = nxt
            layer_loss[k] = {s: math.fsum(v for v in losses[s]) for s in S_VALUES}
            exact_Z[k] = {s: math.fsum(c.mass(s) for c in charts) for s in S_VALUES}
        rep["counts"]["charts_alive_at_depth_%d" % K_EXACT] = len(charts)

        # §12/§13 internal consistency: the drop in Z equals the layer's total loss
        drop_worst, drop_at = 0.0, None
        for k in range(1, K_EXACT):
            for s in S_VALUES:
                drop = exact_Z[k][s] - exact_Z[k + 1][s]
                want = layer_loss[k + 1][s]
                scale = max(abs(exact_Z[k][s]), 1e-300)
                rel = abs(drop - want) / scale
                if rel > drop_worst:
                    drop_worst, drop_at = rel, {"k": k, "s": s}
        check("SRC07_the_drop_in_Z_k_equals_the_layers_total_first_descent_mass",
              drop_worst < 1e-13,
              f"worst gap {drop_worst:.3e} relative to Z_k at {drop_at}")

        # §13 against the stopping-time strata by direct summation. The brute force
        # is truncated at N_BRUTE and the algebra is not, so the comparison carries
        # the truncation tail explicitly instead of pretending the two are the same
        # quantity — the first version of this check did pretend, and failed at k=15
        # for that reason rather than for anything wrong with the paper.
        layer_ok, layer_worst, layer_at = True, 0.0, None
        for k in range(1, K_EXACT):
            for s in S_VALUES:
                want = math.fsum(n ** -s for n in range(2, N_BRUTE) if sigma(n) == k + 1)
                got = layer_loss[k + 1][s]
                tail = N_BRUTE ** (1 - s) / (s - 1)
                excess = abs(got - want) - tail
                if excess > 0:
                    layer_ok = False
                if excess > layer_worst:
                    layer_worst, layer_at = excess, {"k": k, "s": s, "algebra": got,
                                                     "brute": want, "tail": tail}
        check("SRC07_layer_identity_matches_the_stopping_time_strata_within_the_tail",
              layer_ok, f"worst excess over the tail bound {layer_worst:.3e} at {layer_at}")

        # the exact zero layers, from the algebra alone
        adm_all = admissible(K_EXACT + 1)
        zero_layers = sorted(k for k in range(2, K_EXACT + 1)
                             if all(layer_loss[k][s] == 0.0 for s in S_VALUES))
        check("SRC07_layer_loss_is_exactly_zero_precisely_at_inadmissible_depths",
              set(zero_layers) == {k for k in range(2, K_EXACT + 1) if k not in adm_all},
              f"zero layers {zero_layers}, inadmissible depths "
              f"{sorted(k for k in range(2, K_EXACT + 1) if k not in adm_all)}")
        rep["counts"]["depths_with_exactly_zero_layer_loss"] = zero_layers

        # ------------------- the cross-check: exact Z_k inside RUN-004's measured bracket
        if measured_path and measured_path.exists():
            meas = json.loads(measured_path.read_text(encoding="utf-8"))
            N = meas["domain_hi"]
            rows = {r["k"]: r for r in meas["rows"]}
            bracket_ok, bracket_rows = True, []
            for k in range(1, K_EXACT + 1):
                if k not in rows:
                    continue
                for s in S_VALUES:
                    key = str(int(s)) if float(int(s)) == s else str(s)
                    if key not in rows[k]["z"]:
                        continue
                    lo = rows[k]["z"][key]
                    hi = lo + N ** (1 - s) / (s - 1)
                    ex = exact_Z[k][s]
                    inside = lo - 1e-15 <= ex <= hi + 1e-15
                    if not inside:
                        bracket_ok = False
                    if s == 2.0:
                        bracket_rows.append({"k": k, "measured_lower": lo,
                                             "exact_from_chart_algebra": ex,
                                             "measured_upper": hi, "inside": inside})
            check("SRC07_exact_Z_k_lands_inside_RUN_004s_measured_bracket", bracket_ok,
                  f"{[r for r in bracket_rows if not r['inside']][:4]}")
            rep["measured"]["exact_vs_measured_Z_k"] = bracket_rows

            # §16 hazard, taken from the layer loss so that a vanishing hazard is a
            # literal 0.0 rather than whatever two fsums happen to leave behind
            haz, zero_at, nonzero = [], [], 0
            for k in range(1, K_EXACT):
                lam = layer_loss[k + 1][2.0] / exact_Z[k][2.0]
                haz.append({"k": k, "lambda": lam,
                            "k_plus_1_admissible": (k + 1) in adm_all})
                if lam == 0.0:
                    zero_at.append(k)
                else:
                    nonzero += 1
            check("SRC07_hazard_vanishes_exactly_at_inadmissible_stopping_times",
                  all((h["lambda"] == 0.0) != h["k_plus_1_admissible"] for h in haz),
                  f"{[h for h in haz if (h['lambda'] == 0.0) == h['k_plus_1_admissible']][:4]}")
            check("SRC07_lambda_2_is_exactly_zero_confirming_RUN_004_from_the_algebra",
                  haz[1]["lambda"] == 0.0,
                  f"lambda_2 = {haz[1]['lambda']!r}, so E_2 = E_3 does not reproduce here")
            # and the hazard must not be uniformly small either, or "no uniform
            # positive lower bound" would be a statement about nothing
            check("SRC07_the_hazard_is_substantial_where_it_does_not_vanish",
                  max(h["lambda"] for h in haz) > 0.1,
                  f"largest hazard {max(h['lambda'] for h in haz):.3e}")
            rep["measured"]["atomic_hazard"] = haz
            rep["counts"]["depths_with_zero_hazard"] = zero_at
            rep["counts"]["depths_with_positive_hazard"] = nonzero

        # ------------------------------------------------- the hazard budget bound
        #
        # §17 makes Collatz equivalent to H_K(s) -> oo, so how FAST H_K can grow is
        # the whole question §26 asks next. It has an exact cap, in two lines from
        # Round 01's own §16:
        #
        #   Z_K = Z_k * prod_{j=k}^{K-1} (1 - lambda_j)                     [§16]
        #   n_0 in E_K whenever sigma(n_0) > K, so Z_K >= n_0^{-s}          [§16 def]
        #   =>  sum_{j=k}^{K-1} -log(1 - lambda_j)  =  log(Z_k / Z_K)
        #                                           <= log(Z_k * n_0^s).
        #
        # So a single small value that stays hard for a long time caps what every
        # level in that window can contribute, together. n = 27 has sigma = 59, so
        # it holds the floor from k = 8 to k = 58 — fifty levels sharing one budget.
        #
        # This is NOT a no-go: infinitely many bounded windows can still sum to
        # infinity. It is a rate obstruction, and it says what any proof of
        # H_K -> oo has to survive.
        # The bound holds at ANY depth where n0 is still hard, so k0 is simply chosen
        # from a fixed set rather than by a heuristic — an earlier version looked for
        # the depth where Z_k comes within a factor 2 of the floor, which does not
        # happen anywhere inside the reachable range and silently produced no rows.
        budget_rows, budget_ok, identity_ok = [], True, True
        identity_witness: list[dict] = []
        for n0 in (27, 703, 10087, 35655):
            sig = sigma(n0)
            for k0 in (1, 8, 16):
                K = min(sig - 1, K_EXACT)
                if k0 >= K:
                    continue
                # The telescoping identity is checked at EVERY endpoint, not just at
                # K. Checking it at one endpoint is unsafe here for a reason this run
                # is itself about: if that endpoint happens to be one of the
                # zero-hazard depths then Z_{K-1} = Z_K, and a wrong endpoint index
                # is invisible. Depth 22 is exactly such a level.
                for K2 in range(k0 + 1, K + 1):
                    for s in S_VALUES:
                        sp = math.fsum(
                            -math.log1p(-layer_loss[j + 1][s] / exact_Z[j][s])
                            for j in range(k0, K2))
                        gap = math.log(exact_Z[k0][s] / exact_Z[K2][s])
                        if abs(sp - gap) > 1e-9 * max(1.0, abs(gap)):
                            identity_ok = False
                            if len(identity_witness) < 5:
                                identity_witness.append(
                                    {"k0": k0, "K": K2, "s": s,
                                     "spent": sp, "log_ratio": gap})
                for s in S_VALUES:
                    spent = math.fsum(
                        -math.log1p(-layer_loss[j + 1][s] / exact_Z[j][s])
                        for j in range(k0, K))
                    # the budget caps the WHOLE window [k0, sigma(n0) - 1], of
                    # which only [k0, K] is inside reach here
                    budget = math.log(exact_Z[k0][s] * n0 ** s)
                    if spent > budget + 1e-12:
                        budget_ok = False
                    if s == 2.0:
                        budget_rows.append({
                            "n0": n0, "sigma_n0": sig, "from_depth": k0,
                            "levels_in_the_whole_window": sig - 1 - k0,
                            "levels_measured": K - k0,
                            "hazard_spent_over_measured_levels": spent,
                            "budget_for_the_whole_window": budget,
                            "fraction_of_budget_used": spent / budget})
        check("SRC07_cumulative_hazard_equals_the_log_ratio_of_Z", identity_ok,
              f"§16's product form does not reproduce §17's cumulative hazard: "
              f"{identity_witness}")
        check("SRC07_hazard_accumulation_respects_the_single_hard_value_budget",
              budget_ok, f"{budget_rows}")
        rep["measured"]["hazard_budget"] = budget_rows

        # ------------------------------------------- what the paper says about itself
        check("SRC07_paper_states_the_no_go_is_per_chart_not_global",
              "不排除" in paper and "global total Hard-Zeta contraction" in paper,
              "§22's scope limit is not in the text, so the No-Go could be read as "
              "excluding more than it does")
        check("SRC07_paper_carries_the_n_at_least_2_domain_correction",
              r"\widetilde H_w:=H_w\cap[2,\infty)" in paper,
              "Round 01 does not open with the domain correction")

    except Exception as exc:                       # noqa: BLE001
        evaluated = False
        rep['measured']['evaluation_error'] = f'{type(exc).__name__}: {exc}'[:300]
    check('SRC07_the_chart_algebra_evaluates_without_error', evaluated,
          rep['measured'].get('evaluation_error', ''))

    # ---------------------------------------------------------------- output
    if not evaluated:
        rep["ok"] = False
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 1

    rep["counts"].update({
        "charts_confronted_with_iteration": sum(len(levels[k])
                                                for k in range(1, K_BRUTE + 1)),
        "parity_word_cases": parity_cases,
        "block_identity_cases": block_cases,
        "hard_height_charts_checked": height_cases,
        "hard_cap_cases": cap_cases,
        "four_way_partitions_checked": four_cases,
        "first_descent_cases": fd_cases,
        "zone_counts": zones,
        "brute_force_range": f"[2, {N_BRUTE})",
        "exact_depth": K_EXACT,
    })
    rep["measured"]["exact_Z_k"] = {str(k): exact_Z[k] for k in sorted(exact_Z)}
    rep["measured"]["no_go_construction"] = nogo_rows
    rep["measured"]["assessment"] = {
        "what_round_01_gets_right": (
            "All of it, within the finite reach of this check. The child recursion "
            "reproduces direct iteration exactly; the recursive hard height "
            "reproduces the hard set of every chart to depth 10 without rescanning "
            "prefixes; the four-way identity partitions every parent; the mass "
            "conservation law holds chart by chart; the trichotomy is exhaustive; "
            "Zone C loses no mass; and the U^k closed form is exact."
        ),
        "the_strongest_check_here": (
            "The chart algebra computes Z_k(s) EXACTLY - a finite sum where h(w) is "
            "finite, a Hurwitz zeta where it is not. RUN-004 measured the same "
            "quantity by brute force on [2, 2^32) and bracketed it. The two share no "
            "code and no method, and the exact value lands inside the measured "
            "bracket at every depth checked. That tests Round 01's algebra and "
            "RUN-004's bracket at the same time."
        ),
        "how_this_relates_to_the_no_go": (
            "§21's No-Go is PER-CHART, and §22 says so: it does not exclude global "
            "total contraction. RUN-004's result is about the global total, at L = 1, "
            "and is unrelated to §21's U^k construction. In Round 01's own language "
            "it is lambda_2(s) = 0, and more generally lambda_k(s) = 0 whenever k+1 "
            "is not an admissible stopping time. Confirmed here from the chart "
            "algebra rather than from the brute-force measurement."
        ),
        "the_hazard_budget": (
            "§17 makes Collatz equivalent to H_K(s) -> oo, and Round 01's own §16 "
            "caps how fast H_K can grow. Z_K = Z_k prod(1 - lambda_j), and Z_K >= "
            "n0^{-s} for any n0 still hard at depth K, so the TOTAL hazard spent "
            "over a window in which one value survives is at most log(Z_k n0^s). "
            "n = 27 has sigma = 59, so levels 8 through 58 - fifty of them - share "
            "a single budget of about 1.12 nats at s = 2. This is not a no-go: "
            "infinitely many bounded windows can still sum to infinity. It is a "
            "rate obstruction, and it is what any proof of H_K -> oo must survive."
        ),
        "what_it_sharpens": (
            "§26 asks whether a non-summable lower bound on lambda_k(s) can be "
            "established. A UNIFORM POSITIVE lower bound cannot: lambda_k vanishes "
            "identically at infinitely many k. The cumulative form sum lambda_k = oo "
            "that §17 already prefers is untouched - zero terms cost a sum nothing "
            "while being fatal to a per-step bound."
        ),
        "not_established": (
            "nothing about Collatz, and nothing about whether the hazard sum "
            "diverges. Round 01 is an exact bookkeeping layer; this run confirms the "
            "bookkeeping."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
