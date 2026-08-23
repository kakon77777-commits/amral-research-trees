# RUN-032 — Hard-Zeta A-U.2d.4: the first round in this line whose core holds on orbits that exist, verified in exact integers, and the identity its own checker evaluates in floating point

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d4_Renewal_Congestion_Rigidity_bundle_v0.1.zip` (source item 50) — Laminar First-Crossing Forests, Annular Farey Structure, and a Quantitative Congestion Envelope. Ships a checker, its report, a constants JSON, a source-validation record and a stdout transcript.
**Tools:** [`src50_congestion_rigidity.py`](../code/src50_congestion_rigidity.py) · [`src50_drill.py`](../code/src50_drill.py) · [`src50_emit_report_block.py`](../code/src50_emit_report_block.py)
**Logs:** [`src50-au2d4.json`](../data/gate-logs/src50-au2d4.json) · [`src50-drill.json`](../data/gate-logs/src50-drill.json)

**Result: every structural claim in this round holds, and — for the first time in the A-U.2d line — it holds on orbits the sweep can exhibit rather than on surviving crossings that have never been seen. Theorem 3.1 and laminarity verified with zero violations, the annulus identity verified as exactly zero in integer arithmetic, the determinant identity exact on every strict-drop edge, and all eight of the shipped checker's smoke-test figures reproduced independently field for field. The bundle's declared input state closes against RUN-030 and RUN-031. Three findings, none mathematical.**

---

## Why this round is different from the eight before it

Every A-U.2d round so far had the same shape: a theorem about **surviving**
crossings, of which RUN-023 measured **0** below `2·10⁵`. The interesting half
was always conditional and never testable.

Theorem 3.1 is not that. It says

> `e(s) = min{u > s : δ_u < δ_s}`

and that is not a statement about CASP candidates. It is an identity about the
scalar sequence `δ_m = βm − K_m`, true of any orbit whatsoever — the crossing
condition `K_u − K_s > β(u−s)` *is* `δ_u < δ_s`, rearranged. Laminarity (Theorem
4.1) follows for the reason next-smaller-element intervals are laminar in any
sequence at all. The annulus and determinant identities are algebra in the slack
values.

**So the whole structural core applies to real Collatz orbits**, and this run
tests it on four of them.

## Verified in exact integers, with no floating point anywhere

`δ_u < δ_s` is `3^(u−s) < 2^(K_u−K_s)` — a comparison of two integers. And every
quantity the round defines is `aβ + b` for integers `a, b`:

| | as a β-linear pair |
| --- | --- |
| `A_i = βg_i − p_i` | `(g_i, −p_i)` |
| `D_i = δ_{s_i} − δ_{e_i}` | `(s_i − e_i, K_{e_i} − K_{s_i})` |
| `E_i = r_i − βh_i` | `(−h_i, r_i)` |

So `A_i + D_i − D_{i+1} − E_i` is not a small number. It is the **pair `(0, 0)`**,
and the run reports it as such over 229 nested edges. The determinant likewise:
`g_i E_i + h_i A_i` has β-coefficient `−g_i h_i + h_i g_i = 0` exactly, leaving
the integer `r_i g_i − p_i h_i`.

Two independent routes computed the crossings — a quadratic scan that asks the
defining question at every pair, and a monotone stack that assumes transitivity
of the slack order — and they agree everywhere. If they had not, the assumption
would have been the thing that broke.

## Finding 1 — the identity is exact, and its own checker evaluates it in `float`

The bundle's `SOURCE_VALIDATION_AU2d4.json` reports its checker gate as

```
"max_annulus_identity_error": 2.3092638912203256e-14
```

That number exists because `verify_Hard_Zeta_AU2d4_congestion_rigidity.py` sets
`BETA = math.log2(3.0)` and carries the slacks as doubles. Recomputed as
β-linear integer pairs the error is **0** — not small, absent.

**Third time in this line.** RUN-027 found `U_β(L)` to be rational while the
shipped script computed it in 80-digit `mpmath`; RUN-029 found the entire
exponent chain to be exactly rational; here the central identity of the round is
exactly integral. The pattern is consistent enough to be worth naming: this line
reaches for higher precision where it could reach for exactness.

**And the float route was not wrong.** Their next-smaller comparison is a
comparison of doubles that can in principle be arbitrarily close, so the run
measured the margin: the smallest gap the scan actually had to resolve is
`3.0e-3`, against a double spacing of `4.4e-15` at that magnitude — a margin of
**11.8 orders of magnitude** across 3,151 comparisons. The failure mode was
looked for and is not present.

## Finding 2 — two names, one file

`checker_stdout.txt` is **byte-identical** to `Hard_Zeta_AU2d4_checker_report.json`.
The README describes them as different artifacts — "deterministic checker output"
and "human-readable checker run output" — and the validation record lists both,
with the same hash. The human-readable transcript is the JSON.

## Finding 3 — the exponents are exact rationals published as drifted doubles

Every published exponent derives from `ρ★ = 4.1164`, a terminating decimal, so
each is an exact rational. Six of the seven differ from the nearest double of
their exact value by 1 to 6 ulps — chained float arithmetic where an exact
rational was available.

**This is a note, not a defect.** Every one is right to 15 significant digits,
nothing in the round turns on it, and the round's own two self-consistency
identities (`θ★ + ρ★/(ρ★+1) = 1` and `(1+1/ρ★)·(ρ★/(ρ★+1)) = 1`) hold exactly
as rationals. Reporting it as anything more would be inflation.

## What the bundle gets right, and it is worth saying

RUN-031 found a shipped `SHA256SUMS` covering only the files that cannot change.
This bundle's `SOURCE_VALIDATION_AU2d4.json` is the opposite case, and the
contrast is the point:

- it lists **8 of the 9** files, and the one it omits is **itself** — the only
  file a manifest cannot hash;
- all 8 hashes and byte counts verify;
- its `markdown_checks` — UTF-8, delimiter policy, dollar-count parity — all
  reproduce;
- it records `unicode_escape_round_trip_used: false`, which is a hazard this arm
  has its own scars from;
- and its `input_state_sha256` names the two upstream items **RUN-030 and RUN-031
  examined**, with hashes that match what this tree recorded. The provenance
  chain closes against an independent record rather than asking to be trusted.

The round's scope refusals also survive: the paper's status line, the abstract's
"not eliminated", the restated Headroom Non-Telescoping No-Go, and the constants
JSON's `rotation_headroom_telescope_allowed: false`.

---

<!-- BEGIN GENERATED measured block: python code/src50_emit_report_block.py -->

**The shipped checker's own figures, recomputed in exact integers.** Read from its report, never run:

| start | accelerated steps | max active depth | at time | chain plateau / strict-drop edges |
| --- | --- | --- | --- | --- |
| `27` | `41` | `17` | `32` | `13 / 3` |
| `703` | `62` | `15` | `34` | `10 / 4` |
| `6171` | `96` | `15` | `87` | `11 / 3` |
| `837799` | `195` | `23` | `49` | `16 / 6` |

Every field of every row agrees with the shipped report (`4` starts compared, `5` fields each, `0` disagreements), and so do all `4` of its mechanical-word rows (`0` disagreements).

| what | measured against | value |
| --- | --- | --- |
| **Theorem 3.1** — proper prefixes with a smaller-or-equal slack | exact integer comparison over 394 intervals on 4 orbits | `0` |
| …the two independent routes disagreeing | a quadratic scan against a monotone stack | `0` |
| **Theorem 4.1** — interval pairs that properly cross | must be zero | `0` |
| …nested pairs / disjoint pairs | both branches must be inhabited or laminarity is untested | `2757 / 23429` |
| **annulus identity** `A+D = D'+E` — errors | as β-linear integer pairs over 229 nested edges, so the residual is a pair and not a small number | `0` |
| …the residual the bundle's own validation record reports | its checker evaluates the same identity in `float` | `2.3092638912203256e-14` |
| plateau edges / strict-drop edges | the dichotomy must be exercised in both branches | `123 / 106` |
| **determinant** `Δ = rg − ph = gE + hA` — disagreements | β cancels exactly; checked on every strict-drop edge | `0` |
| …determinants below one | must be zero | `0` |
| smallest slack gap the float comparison had to resolve | 3151 comparisons, exactly | `0.0030125382` |
| …double spacing at that magnitude |  | `4.4258624e-15` |
| …**margin, in orders of magnitude** | the failure mode looked for | `11.8` |
| published exponents differing from the exact rational's nearest double | of 7, largest drift 6 ulps | `6` |
| …wrong beyond 15 significant digits | must be zero | `0` |
| validation-record hashes verified | of 8 listed, over 9 files in the bundle | `8` |
| …files present but uncovered | the only one is the record itself (`True`) | `1` |
| …declared upstream hashes agreeing with this tree's own records | RUN-030 and RUN-031 | `2` |
| defects planted / caught by the check named for each | 1 of the entries is a robustness property; 0 malformed | `18 / 18` |

The bracketed floor route used for the mechanical word agrees with exact powers of three on `0..399` (`True`) and needed the exact fallback `0` times at `N = 100000`.

Every figure above is emitted by `code/src50_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

**Drill 18/18 by the check named for each, both controls clean, no malformed
mutations in the final pass.** Four defects in my own gate, and one of them cost
an hour.

**A comparison that silently answers one direction.** `slack_is_smaller` returned
`False` whenever `K_u < K_s` instead of handling the sign, so every reversed
query answered "no" — and the Theorem 3.1 prefix check, which asks `δ_s < δ_u`,
reported **2757 violations of a theorem that holds**. A comparison that refuses
half its domain is worse than one that raises: it answers.

**Two different quantities wearing one label.** I reported orbit-wide nested-edge
counts under the shipped report's `chain_plateau_edges` field name and called the
disagreement theirs. Their field counts the edges of the *deepest chain*:
`13 + 3 = 16 = 17 − 1`. Not a discrepancy — a mislabelling, and the artifact was
right.

**A killed drill left a planted defect on disk.** The drill ran past a ten-minute
tool timeout and was killed from outside, so its `finally` never ran and D1's
mutation stayed live in the gate until the next run reported those 2757
violations again. Every drill in this arm has carried a subprocess timeout since
item 42 — but that protects against a hanging *gate*, not against the drill
itself being killed. The drill now writes the pristine file to a sidecar before
planting anything, restores from it at startup if one is found, reports
`a_previous_run_was_interrupted_and_the_gate_was_restored`, and removes it on
clean exit.

**And the reason it was killed was a quadratic sweep.** Asking "which intervals
are live at `t`" for every `t` is `O(N²)`, and at `N = 100000` that was nine and
a half minutes. Replaced with an event sweep — which was then **off by one**,
because at a position where one interval ends and another begins the end must be
processed first. Caught only because the shipped report says 6 and the sweep said
7. The artifact was the oracle again.

Two further defects were re-aimed after the pre-flight named them: a mutation of
a command-line default the drill always overrides, and a reversed comparison that
reverses the prefix check too and so stays self-consistently green. Fifth item
running that the pre-flight has paid for itself.

## Route map

`ROUTE_MAP v2.4`. Item 51 is `A-U.2d.5 — Annular Farey–Residue Coupling`, which
the constants JSON names as the next round.

## What this run does not claim

1. That the congestion envelope holds. `ω_N° = O(N^0.80455 (log N)^0.19545)`
   quantifies over B-injection intervals in a CASP candidate; the structural
   core was tested on real orbits, the envelope was not.
2. That Highly Nested is eliminated. The round says plainly that it is not, and
   this run confirms only that its own arithmetic and structure are sound.
3. That the shipped checker is correct. It was **read**, never run; what was
   compared is its published figures against an independent recomputation.
4. That the float route is safe in general. Its margin was measured **at the
   comparisons these four orbits required** and is enormous there; a longer orbit
   could bring two slacks closer.
5. That the Diophantine exponent is anything other than the external input
   RUN-029 traced to Fan–Queffélec–Queffélec.
