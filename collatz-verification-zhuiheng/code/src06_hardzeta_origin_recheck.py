"""Recheck of source items 17-18 — the Hard-Zeta origin.

數學戰士「墜衡」 / AMRAL Research Lab.
Subject: Neo.K, `Faithful_Global_Quantifier_Compression_Proof_Route_v0.1_bundle.zip`
(2026-08-11 11:40) and the loose `v0.1.1.md` (13:11). The origin of the whole
Hard-Zeta line — 44 of the 64 items in the source folder descend from it.

What the paper does
-------------------
§12-§14 build a general bridge: for a countable domain with a **monotone**
certificate system `C_k(x) => C_{k+1}(x)`, and any strictly positive summable
weights,

    forall x exists k : C_k(x)   <=>   Q_k -> 0,   Q_k = sum_{x in E_k} w_x.

§15-§16 instantiate it at `sigma(n) = inf{ j>=1 : T^j(n) < n }` with weights
`n^{-s}`, giving

    Collatz   <=>   Z_k(s) -> 0,   Z_k(s) = sum_{ n>=2, sigma(n)>k } n^{-s}

for any fixed `s > 1`. §21 then names the proof obligation: **Hard-Zeta Decay**,
in a uniform form `Z_{k+L} <= q Z_k` with `q < 1`, or a weaker cumulative form.

The bridge is correct, and this recheck confirms the parts that are decidable.
But a logical translation is not where a verification arm earns its keep. Two
things here are:

1. **`Z_k(s)` has never been computed.** It is measurable. This arm measures it
   on `[2, 2^32)` and brackets the true value:

       Z_k^[2,N](s)  <=  Z_k(s)  <=  Z_k^[2,N](s) + sum_{n>N} n^{-s}

   with the tail bounded by `N^(1-s)/(s-1)`, plus the exact lower bound
   `Z_k(s) >= (min E_k)^{-s}` — exact because `min E_k` is not truncated: no `n`
   beyond `N` can be smaller than one already found.

2. **The uniform route at `L = 1` is refutable, and this recheck refutes it.**
   `sigma(n) = 3` is impossible for every `n >= 2`:

       n even                  => sigma(n) = 1.
       n odd, (3n+1)/2 even    => T^2(n) = (3n+1)/4 < n for n > 1, so sigma = 2.
       n odd, (3n+1)/2 odd     => T^2(n) = (9n+5)/4 > n, and then T^3(n) is
                                  either (9n+5)/8 > n or (27n+19)/8 > n.
                                  Either way T^3(n) > n, so sigma > 3.

   So `E_2 = E_3` **as sets, exactly**, hence `Z_2(s) = Z_3(s)` for every `s`,
   hence no `q < 1` satisfies `Z_{k+1} <= q Z_k`. The `L = 1` form of §21's
   uniform route is false — not unproven, false.

   That is a statement about the true infinite sums, not about the measured
   range, and the measurement confirms it independently.

The same mechanism explains the plateaus the measurement shows: `Z_k` is pinned
from below by `(min E_k)^{-s}`, and `min E_k` moves only when the current
smallest hard value is finally settled. `n = 27` holds the floor for `k = 8..58`.

A finding about the ROUTE MAP
-----------------------------
`ROUTE_MAP_v0.1.md` states the general bridge as an unconditional iff and does
**not** carry §12's monotonicity requirement. The paper body is right; the map is
a lossy summary of it. The omitted hypothesis is load-bearing, and this recheck
exhibits a counterexample rather than asserting it.

Usage:  python code/src06_hardzeta_origin_recheck.py <measured.json> [small.json]
"""

from __future__ import annotations

import json
import math
import os
import pathlib
import re
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Overridable so `src06_drill.py` can point the text checks at a damaged copy.
# Without these the document checks could never be shown capable of failing, and
# an undrillable check is one this tree does not get to count.
SOURCE = pathlib.Path(os.environ.get(
    "HZ_SOURCE_DIR",
    r"D:\我的研究\學術討論\論文\數學\考拉茲猜想\最新\Collatz_OT_Series_Paper"))
SSSP = pathlib.Path(os.environ.get(
    "HZ_SSSP_DIR",
    str(ROOT.parent / "collatz-ot-series-neok"
        / "Collatz_Operation_Translation_Series_SSSP_Repaired_v1.0")))
MEASURE_BIN = pathlib.Path(os.environ.get(
    "HZ_MEASURE_BIN", str(ROOT / "build" / "hz_zeta_measure.exe")))


def T(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def sigma(n: int, cap: int = 10_000) -> int:
    """sigma(n) by direct iteration, exact integers, assuming nothing."""
    x = n
    for j in range(1, cap + 1):
        x = T(x)
        if x < n:
            return j
    raise RuntimeError(f"sigma({n}) exceeded cap {cap}")


def admissible_stopping_times(jmax: int) -> set[int]:
    """{ j : exists u >= 0 with 2^(j-1) <= 3^u < 2^j }.

    `bit_length()` gives that j directly and exactly, so the boundary needs no
    argument about how near u*log2(3) comes to an integer.

    An earlier note here claimed the exact route was necessary because a float
    logarithm could move a boundary. The drill tested that and it is not true at
    this scale: `int(log(3**u, 2)) + 1` agrees with `bit_length()` for every
    u < 640, which is past where 3**u leaves float range altogether. Exactness
    here is a robustness choice, not something the measurement can distinguish,
    and saying otherwise would have credited a check with work it is not doing.
    """
    out, u, p = set(), 0, 1
    while True:
        j = p.bit_length()          # the unique j with 2^(j-1) <= 3^u < 2^j
        if j > jmax:
            return out
        out.add(j)
        u += 1
        p *= 3


def tail_bound(N: int, s: float) -> float:
    """sum_{n > N} n^{-s} <= integral_N^inf x^{-s} dx = N^(1-s)/(s-1)."""
    return N ** (1 - s) / (s - 1)


def main() -> int:
    measured = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    small_path = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None

    rep = {
        "tool": "src06_hardzeta_origin_recheck.py",
        "subject": ("Neo.K, Faithful Global Quantifier Compression Proof Route "
                    "v0.1 bundle + v0.1.1 (2026-08-11)"),
        "source_items": [17, 18],
        "scope": (
            "the decidable content of the §12-§16 bridge, the first measured values "
            "of Z_k(s), and the refutability of §21's uniform route. The bridge "
            "itself is a logical translation and is not re-proved here."
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

    N = measured["domain_hi"]
    rows = {r["k"]: r for r in measured["rows"]}
    ks = sorted(rows)
    # keys stay strings: the measurer writes "2", not "2.0"
    ss = sorted(rows[ks[0]]["z"], key=float)

    # ------------------------------------------------ the measurer is trustworthy
    # 1. its sigma against this arm's engine, a separate implementation
    engine = ROOT / "build" / "collatz_verify.exe"
    out = subprocess.run([str(engine), "--verify", "--from", "2", "--to", str(N)],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    eng = json.loads(out.stdout)
    check("SRC06_measurer_max_sigma_agrees_with_the_engine",
          eng["max_sigma"] == measured["max_sigma"]
          and eng["max_sigma_at"] == measured["max_sigma_at"],
          f"engine {eng['max_sigma']}@{eng['max_sigma_at']} vs measurer "
          f"{measured['max_sigma']}@{measured['max_sigma_at']}")

    # 2. its sigma against exact Python bigint iteration, on the values that matter
    probe = [2, 3, 4, 7, 27, 703, 10087, 35655, 270271, measured["max_sigma_at"]]
    py_sigma = {n: sigma(n) for n in probe}
    check("SRC06_argmax_sigma_reproduces_under_exact_python_iteration",
          py_sigma[measured["max_sigma_at"]] == measured["max_sigma"],
          f"python says sigma({measured['max_sigma_at']}) = "
          f"{py_sigma[measured['max_sigma_at']]}")

    # 3. every reported min_E_k must really be hard at that depth, and every
    #    integer below it must really not be — otherwise "min" means nothing
    mins_ok, mins_witness = True, []
    for k in ks:
        m = rows[k]["min_E_k"]
        if m == 0:
            continue
        if sigma(m) <= k:
            mins_ok = False
            mins_witness.append({"k": k, "min": m, "sigma": sigma(m)})
        elif m < 2000 and any(sigma(x) > k for x in range(2, m)):
            mins_ok = False
            mins_witness.append({"k": k, "min": m, "why": "a smaller hard n exists"})
    check("SRC06_reported_minima_of_E_k_are_really_minimal", mins_ok, f"{mins_witness}")

    # 4. Kahan against an exactly-rounded independent summation
    if small_path and small_path.exists():
        small = json.loads(small_path.read_text(encoding="utf-8"))
        n_small = small["domain_hi"]
        sig = [0, 0] + [sigma(n) for n in range(2, n_small)]
        worst, worst_at = 0.0, None
        for r in small["rows"]:
            k = r["k"]
            for s_str, got in r["z"].items():
                s = float(s_str)
                want = math.fsum(n ** (-s) for n in range(2, n_small) if sig[n] > k)
                if want != 0.0:
                    rel = abs(got - want) / want
                    if rel > worst:
                        worst, worst_at = rel, {"k": k, "s": s}
        check("SRC06_kahan_sums_match_exactly_rounded_python_fsum",
              worst < 1e-14, f"worst relative disagreement {worst:.3e} at {worst_at}")
        rep["counts"]["fsum_crosscheck_domain"] = n_small
        rep["measured"]["fsum_worst_relative_disagreement"] = worst

    # ------------------------------------------------------- §12 monotone system
    # 5. E_k must be nested decreasing, or §13's continuity-from-above does not apply
    counts = [rows[k]["count_E_k"] for k in ks]
    check("SRC06_E_k_counts_are_non_increasing_in_k",
          all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1)),
          f"{counts}")
    zs_ok = all(rows[ks[i]]["z"][s] >= rows[ks[i + 1]]["z"][s]
                for i in range(len(ks) - 1) for s in ss)
    check("SRC06_Z_k_is_non_increasing_in_k_for_every_s", zs_ok)

    # 6. the sigma histogram, derived from the nesting
    consecutive = [k for k in ks if k + 1 in rows]
    hist = {k + 1: rows[k]["count_E_k"] - rows[k + 1]["count_E_k"] for k in consecutive}
    check("SRC06_derived_sigma_histogram_is_non_negative",
          all(v >= 0 for v in hist.values()),
          f"{ {k: v for k, v in hist.items() if v < 0} }")

    # ---------------------------------------- the result: L = 1 is refuted
    # 7. sigma(n) = 3 occurs for no n on the measured range...
    check("SRC06_sigma_equals_3_occurs_for_no_n_on_the_range",
          hist.get(3) == 0, f"count of sigma = 3 is {hist.get(3)}")
    # ...and this arm proves it holds for every n, by the case split in the
    # docstring. The proof is confirmed here on the algebra it rests on, so a
    # slip in the derivation cannot pass unnoticed.
    algebra_ok = True
    for n in range(3, 200_003, 2):                       # odd n only
        t1 = (3 * n + 1) // 2
        if t1 % 2 == 0:
            if not (3 * n + 1) // 4 < n:
                algebra_ok = False
        else:
            t2 = (9 * n + 5) // 4
            if not t2 > n:
                algebra_ok = False
            t3 = t2 // 2 if t2 % 2 == 0 else (3 * t2 + 1) // 2
            if not t3 > n:
                algebra_ok = False
    check("SRC06_the_two_case_proof_that_sigma_never_equals_3_holds_pointwise",
          algebra_ok,
          "the case split behind 'sigma(n) != 3 for all n' fails somewhere")

    # 8. therefore Z_2 = Z_3 exactly, so no q < 1 works at L = 1
    l1 = all(rows[2]["z"][s] == rows[3]["z"][s] for s in ss)
    check("SRC06_Z_2_equals_Z_3_exactly_so_L_equals_1_admits_no_q_below_1", l1,
          f"{ {s: (rows[2]['z'][s], rows[3]['z'][s]) for s in ss} }")

    # 9. the same must NOT happen for every step, or the route would be dead
    #    rather than merely needing L >= 2
    strict_steps = sum(1 for k in consecutive
                       if rows[k + 1]["z"][ss[0]] < rows[k]["z"][ss[0]])
    check("SRC06_most_steps_do_strictly_decrease_so_the_route_is_not_dead",
          strict_steps > len(consecutive) // 2,
          f"only {strict_steps} of {len(consecutive)} steps decrease strictly")

    # 10. gaps between occurring stopping times bound the admissible L
    occurring = sorted(j for j, v in hist.items() if v > 0)
    gaps = [b - a for a, b in zip(occurring, occurring[1:])]
    max_gap = max(gaps) if gaps else 0
    check("SRC06_gaps_between_occurring_stopping_times_are_at_most_2",
          max_gap <= 2, f"largest gap {max_gap}")

    # 11. and the occurring set is exactly the arithmetically admissible one
    adm = admissible_stopping_times(max(occurring))
    adm_in_range = {j for j in adm if j >= min(occurring)}
    check("SRC06_occurring_stopping_times_are_exactly_the_admissible_ones",
          set(occurring) == adm_in_range,
          f"occurring-not-admissible {sorted(set(occurring) - adm_in_range)[:8]}, "
          f"admissible-not-occurring {sorted(adm_in_range - set(occurring))[:8]}")

    # ------------------------------------------------- the bracket on true Z_k
    brackets, informative = [], {s: 0 for s in ss}
    bracket_ok = True
    for k in ks:
        r = rows[k]
        for s in ss:
            sv = float(s)
            zm = r["z"][s]
            tail = tail_bound(N, sv)
            floor = (r["min_E_k"] ** -sv) if r["min_E_k"] else 0.0
            # the exact floor must sit inside the bracket, or something is wrong
            if floor > zm + tail:
                bracket_ok = False
            if tail < zm / 10:
                informative[s] = max(informative[s], k)
            brackets.append({"k": k, "s": sv, "lower_exact": floor,
                             "measured": zm, "upper": zm + tail, "tail": tail})
    check("SRC06_the_exact_lower_bound_sits_inside_the_measured_bracket", bracket_ok,
          "min(E_k)^{-s} exceeds the measured partial sum plus its tail bound, "
          "which cannot happen if both are computed correctly")

    # 12. the Paper 05 bridge: E_k is contained in the k-block fallback set
    e24 = 24
    incl_ok, incl_rows = True, []
    for k in (8, 16, 24):        # the engine's sieve exponent is capped at 26
        if k not in rows:
            continue
        out = subprocess.run([str(engine), "--block", str(k), "--to", str(2 ** e24)],
                             capture_output=True, text=True, encoding="utf-8", check=True)
        d = json.loads(out.stdout)
        fallback = (d["equality"] - 1) + d["ascent"]     # drop n = 1
        cmd = ([sys.executable, str(MEASURE_BIN)] if MEASURE_BIN.suffix == ".py"
               else [str(MEASURE_BIN)])
        out2 = subprocess.run(cmd + ["--to", str(2 ** e24), "--ks", str(k), "--s", "2"],
                              capture_output=True, text=True, encoding="utf-8", check=True)
        small_e = json.loads(out2.stdout)["rows"][0]["count_E_k"]
        if small_e > fallback:
            incl_ok = False
        incl_rows.append({"k": k, "count_E_k": small_e, "fallback": fallback,
                          "tightness": small_e / fallback})
    check("SRC06_E_k_is_contained_in_the_Paper_05_k_block_fallback_set", incl_ok,
          f"{incl_rows}")

    # ------------------------------------- the ROUTE MAP's missing hypothesis
    with zipfile.ZipFile(
            SOURCE / "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1_bundle.zip") as z:
        route_map = z.read(
            "Faithful_Global_Quantifier_Compression_ROUTE_MAP_v0.1.md").decode("utf-8")
        paper_v01 = z.read(
            "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1.md").decode("utf-8")

    body_has = r"C_k(x)\Rightarrow C_{k+1}(x)" in paper_v01
    map_has = bool(re.search(r"C_k.*\\Rightarrow.*C_\{k\+1\}|單調|monotone|Monotone",
                             route_map))
    check("SRC06_the_paper_body_states_the_monotonicity_hypothesis", body_has,
          "§12's C_k => C_{k+1} is not in the v0.1 body, which would make the "
          "bridge itself wrong rather than only its summary")
    check("SRC06_the_route_map_omits_the_hypothesis_the_body_carries",
          body_has and not map_has,
          "the map does carry it after all — then there is nothing to report")

    # and the omission is load-bearing: a non-monotone system where the
    # left side holds and Q_k does not converge to 0
    weights = [2.0 ** -(i + 1) for i in range(40)]

    def C(k: int, i: int) -> bool:
        """Deliberately non-monotone: true only at even k, for every x."""
        return k % 2 == 0

    Q = [math.fsum(w for i, w in enumerate(weights) if not C(k, i)) for k in range(12)]
    lhs = all(any(C(k, i) for k in range(12)) for i in range(len(weights)))
    check("SRC06_without_monotonicity_the_bridge_is_false",
          lhs and max(Q[6:]) > 0.4,
          f"forall-exists holds = {lhs}, Q_k tail = {Q[6:]}; if Q_k -> 0 here "
          "then the counterexample is wrong and the omission is harmless")

    # ------------------------------------------- version chain v0.1 -> .1 -> .2
    v011 = (SOURCE / "Faithful_Global_Quantifier_Compression_Proof_Route_v0.1.1.md"
            ).read_text(encoding="utf-8")
    v012 = next((SSSP / "research_program").glob("*.md")).read_text(encoding="utf-8")
    orig_hz = next((SSSP / "provenance" / "original").glob("HZ__*.md")
                   ).read_text(encoding="utf-8")
    check("SRC06_v011_is_the_hz_original_inside_the_sssp_package",
          v011 == orig_hz,
          "the loose v0.1.1 is not the same bytes the SSSP package archived as "
          "its HZ original, so the two lines are different documents")
    # The three versions are compared by COUNTING the two forms of the chart
    # decomposition, not by asking whether a string appears somewhere. v0.1
    # carries the unrestricted union twice — once as `E_k=` and once as `E_k^C=` —
    # and which of those a given version still has is the whole content of the
    # chain. Delimiter-normalized, so the \(..\) -> $..$ rewrite cannot answer
    # for the mathematics. See feedback-presence-is-not-evidence-of-a-fix.
    def norm(x: str) -> str:
        x = re.sub(r"^\s*\\\[\s*$", "$$", x, flags=re.M)
        x = re.sub(r"^\s*\\\]\s*$", "$$", x, flags=re.M)
        return x.replace(r"\(", "$").replace(r"\)", "$")

    UNRESTRICTED = r"\\bigsqcup_\{\|w\|=k\}H_w"
    RESTRICTED = r"\\bigsqcup_\{\|w\|=k\}\\widetilde H_w"
    TILDE_DEF = r"\\widetilde H_w\s*:?=\s*H_w\\cap\[2,\\infty\)"
    chain = {"v0.1": norm(paper_v01), "v0.1.1": norm(v011), "v0.1.2": v012}
    bare = {v: len(re.findall(UNRESTRICTED, x)) for v, x in chain.items()}
    tilde = {v: len(re.findall(RESTRICTED, x)) for v, x in chain.items()}
    tdef = {v: len(re.findall(TILDE_DEF, x)) for v, x in chain.items()}
    corrig = {v: x.count("Domain Corrigendum") for v, x in chain.items()}

    check("SRC06_v01_carries_the_unrestricted_union_twice",
          bare["v0.1"] == 2 and tilde["v0.1"] == 0 and tdef["v0.1"] == 0,
          f"bare {bare}, tilde {tilde}, definitions {tdef}")
    check("SRC06_v011_adds_the_corrigendum_and_the_restricted_chart",
          corrig["v0.1.1"] == 1 and corrig["v0.1"] == 0 and tdef["v0.1.1"] > 0,
          f"corrigendum sections {corrig}, tilde definitions {tdef}")
    check("SRC06_v011_fixed_only_one_of_the_two_unrestricted_unions",
          bare["v0.1.1"] == 1,
          f"v0.1.1 has {bare['v0.1.1']} bare unions, not the 1 that makes the "
          "SSSP audit's complaint about the surviving E_k^C form correct")
    check("SRC06_v012_removes_the_last_unrestricted_union",
          bare["v0.1.2"] == 0 and tilde["v0.1.2"] > tilde["v0.1.1"],
          f"bare {bare}, tilde {tilde}")
    check("SRC06_v012_dissolves_the_corrigendum_into_the_body",
          corrig["v0.1.2"] == 0 and corrig["v0.1.1"] == 1,
          "the corrigendum is still a trailing section in v0.1.2, so it was "
          "appended rather than integrated")
    rep["measured"]["version_chain"] = {
        "bare_unrestricted_unions": bare,
        "restricted_unions": tilde,
        "tilde_definitions": tdef,
        "corrigendum_sections": corrig,
    }

    # ------------------------------------------------------------------ output
    rep["counts"] = {
        "domain": f"[2, {N})",
        "values_scanned": measured["scanned"],
        "depths_measured": len(ks),
        "max_sigma": measured["max_sigma"],
        "max_sigma_at": measured["max_sigma_at"],
        "occurring_stopping_times": len(occurring),
        "largest_gap_between_occurring_stopping_times": max_gap,
        "deepest_k_with_an_informative_bracket": {s: informative[s] for s in ss},
        **rep["counts"],
    }
    rep["measured"]["sigma_histogram"] = hist
    rep["measured"]["occurring_stopping_times"] = occurring
    rep["measured"]["Z_k_brackets"] = brackets
    rep["measured"]["E_k_vs_paper05_fallback"] = incl_rows
    rep["measured"]["assessment"] = {
        "the_result": (
            "The L = 1 form of §21's uniform route is FALSE, not merely unproven. "
            "sigma(n) = 3 is impossible for every n >= 2 by a two-case split on the "
            "parity of (3n+1)/2, so E_2 = E_3 as sets and Z_2(s) = Z_3(s) exactly for "
            "every s > 1. No q < 1 can satisfy Z_{k+1} <= q Z_k. This is a statement "
            "about the true infinite sums, and the measurement confirms it "
            "independently on [2, 2^32)."
        ),
        "what_bounds_L": (
            "More generally Z_{k+1} = Z_k exactly whenever k+1 is not an admissible "
            "stopping time, i.e. whenever no u has 2^k <= 3^u < 2^(k+1). Those k occur "
            "infinitely often. On the measured range the gaps between occurring "
            "stopping times never exceed 2, so L = 2 is the smallest L this "
            "measurement does not refute — it does not follow that L = 2 works."
        ),
        "first_measured_values": (
            "Z_k(s) has not previously been computed. Measured on [2, 2^32) for "
            "k = 1..160 and s = 2, 3, 4, and bracketed as "
            "Z^meas <= Z <= Z^meas + N^(1-s)/(s-1), with the exact lower bound "
            "(min E_k)^{-s} — exact because no n beyond N can be smaller than one "
            "already found."
        ),
        "why_Z_k_plateaus": (
            "Z_k is pinned from below by (min E_k)^{-s}, and min E_k moves only when "
            "the current smallest hard value is finally settled. n = 27 holds the "
            "floor for k = 8..58, and Z_58(2) = 1.3765e-3 against 27^-2 = 1.3717e-3, "
            "so by that depth E_58 is essentially the single value 27."
        ),
        "route_map_finding": (
            "ROUTE_MAP_v0.1.md states the general bridge as an unconditional iff and "
            "omits §12's monotonicity requirement C_k => C_{k+1}. The body is right; "
            "the map is a lossy summary. The omission is load-bearing and the "
            "counterexample is exhibited rather than asserted. The Collatz "
            "instantiation is unaffected, because sigma's certificate system is "
            "monotone."
        ),
        "not_established": (
            "nothing about Collatz. A finite range cannot see lim Z_k: the truncated "
            "sum tends to 0 whether or not the conjecture holds, which is why the "
            "tail bound is carried explicitly and the depth at which the bracket "
            "stops being informative is reported rather than hidden."
        ),
    }

    rep["ok"] = not rep["failures"]
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
