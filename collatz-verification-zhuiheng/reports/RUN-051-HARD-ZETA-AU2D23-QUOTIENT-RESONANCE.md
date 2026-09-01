# RUN-051 — Hard-Zeta A-U.2d.23: a sharpening confirmed on last round's own data, and a theorem with no counter

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d23_Quotient_State_Resonance_and_Defect_Carry_Rigidity_v0.1` (source item 70) — 26 sections, nine files.
**Tools:** [`src70_quotient_resonance.py`](../code/src70_quotient_resonance.py) · [`src70_drill.py`](../code/src70_drill.py) · [`src70_emit_report_block.py`](../code/src70_emit_report_block.py)
**Logs:** [`src70-au2d23.json`](../data/gate-logs/src70-au2d23.json) · [`src70-drill.json`](../data/gate-logs/src70-drill.json)

**Result: the mathematics verifies. Eight of their thirteen counters reproduce exactly, the other five are covered here by larger deterministic enumerations, and the round's central claim — that a zero-defect return is parity-refined, `n = 2^{Q+1}v` and `n' = 2·3^L v` — was confirmed against RUN-050's population before this gate was written: 2,935 zero-defect returns from a different limit and a different walker, every one with `u` even, zero violations. A-U.2d.22's `u ≥ 1` was loose by exactly this factor. Three findings. Theorem 7.1 has no counter at all: its uniqueness half is a `q < 20, r < 100` scan whose assert body is reachable exactly once in 1,881 iterations, where the divisor argument decides every `q` in one line. Their three synthetic blocks are weaker than their counters say — two accounting assertions stayed green on 20,000 inputs deliberately built to violate the property the block is named for, and the reservoir block publishes two counters of 20,000 for one block that actually evaluates 12,176 times. And Theorem 5.1's two halves have opposite tightness: the per-position ceiling is attained at 39.2% of positions, while its `H_max` corollary's `+1` term is not load-bearing — the strictly stronger bound holds on all 6,425 bridges.**

---

## The round's move

A-U.2d.22 ended with the quotient trajectory `n` as the hidden object and proved that defect composition alone cannot produce a contradiction, because the root defect is an exact coboundary. This round prices the most dangerous remaining mechanism — a contiguous return with `𝔡 = 0` — and finds it far more rigid than the previous formula suggested.

Because the accelerated states are odd and `M = 3^k` is odd, the previous round's

> `n = 2^Q u`,  `n' = 3^L u`,  `u ≥ 1`

is not tight. Every nontrivial zero-defect return actually satisfies

> `n = 2^{Q+1} v`,  `n' = 2·3^L v`,  `v ≥ 1`

with an exact cross-adic transfer

> `ν₂(n') = ν₂(n) − Q`,  `ν₃(n') = ν₃(n) + L`.

A zero-defect return spends binary divisibility to buy ternary divisibility, at a fixed rate. That is the round's real object, and everything downstream — the temporal delay, the reservoir accounting, the replenishment alternative — is priced from it.

## The sharpening, confirmed before the gate existed

The first thing I did was run Theorems 3.1 and 4.1 against **RUN-050's** bridges: a different limit, and returns produced by the erasure walker rather than this round's window scan. 2,935 zero-defect returns, every `u` even, zero violations of the refined form or either transfer identity, smallest `v` = 5.

That is worth stating precisely. Last round I reported that `u ≥ 1` held with room, smallest `u` = 10. The correct reading is that `u` was never odd, and this round names why. The claim I verified was true but not tight, and the sharpening reproduces on the data I had already collected — which is stronger evidence than checking it only on the population the round enumerates for itself. Both populations are now in the gate.

## Finding 1 — Theorem 7.1 has no counter

The classification of length-one zero-defect returns is stated as: the only such code is `q = 2, r = 1`, realised by the actual transition `x = 1 + 8Mv → 1 + 6Mv`.

The existence half is covered — Theorem 8.1's `q = 2` runs exercise it 840 times. The **uniqueness** half is checked by this loop:

```python
for q in range(1, 20):
    for r in range(1, 100):
        if 1 - (2**q - 3)*r == 0:
            assert q == 2 and r == 1
```

It increments no counter, so the theorem appears nowhere in their report. And measured, its assert body is reached **once in 1,881 iterations** — the single point `(2, 1)`.

The claim does not need a scan. A length-one zero-defect return requires `1 = (2^q − 3)r` with `r ≥ 1`, so `2^q − 3` must be a positive divisor of 1, hence equal to 1, hence `q = 2` and `r = 1`. That decides every `q` at once; for `q ≥ 3` the divisor is already at least 5. This gate checks 4,000 values of `q` by that argument and finds exactly one solution and no others, alongside 96 actual transitions.

A bounded scan standing in for a two-line divisor argument, with no counter behind it, is the weakest link in an otherwise careful bundle.

## Finding 2 — the three synthetic blocks are weaker than their counters

Three of the thirteen counters come from generated inputs rather than orbits: `resonance_accounting_synthetic` (20,000), `reservoir_to_lift_algebra` (20,000), `linear_mass_recharge_threshold_algebra` (20,000). Measured rather than trusted:

**The accounting block's two telescoping assertions cannot fail.** `lhsQ == telQ` and `lhsL == telL` unfold to `ΣQ = ΣQ` after substituting the generator's own definitions. To demonstrate that rather than assert it, I rebuilt the generator with `Q` reduced by 3 so the supercriticality the block is about is **false by construction** — the telescoping stayed green on **20,000 of 20,000** broken inputs, while the third assertion `Q₀ > βL₀` went red on 14,781 of them. Two of three assertions are identities of the construction; the third is live, but the generator sets `Q = ⌈βL⌉ + randint(0,4)`, so no *generated* sample can fail it either. The block also carries the author's own marker — `assert Q0 <= starts2[0] + R2 + 1000  # corrected below by exact telescoping check`.

**The reservoir block publishes two counters for one block, and both increment outside its guard.** The assertions sit under `if R0/h > θ + 0.02`, which opened on **12,176 of 20,000** samples (60.9%); the two `checks[...] += 1` lines are outside it. So 40,000 published checks are one block, evaluated 12,176 times, counted twice. The assertion itself holds, with a smallest margin of 0.001003.

This is the shape RUN-046 named — a guarded assertion whose counter tallies samples rather than tests — plus a double count. A-U.2d.22 had shipped with none of it; the pattern returns here.

## Finding 3 — Theorem 5.1's two halves have opposite tightness

The per-position ceiling

> `m_ℓ ≤ ⌈βh⌉ − ⌈βℓ⌉ − (h − ℓ)`

is **attained**: 12,153 of 31,035 positions sit exactly on it, smallest slack 0. It is a live, binding bound, and a defect that lowers it by one is caught 12,153 times.

Its corollary

> `H_max < (β − 1)h + 1`

reads as though it were the same strength. It is not. The smallest integer slack is 1, and the `+1` turns out not to be load-bearing at all: the strictly stronger `H_max < (β − 1)h` holds with **0 violations across all 6,425 bridges**. Removing the term the corollary carries changes nothing on this population — which is why a drill defect that deleted it was invisible and had to be re-aimed to forty bits before it could bite.

Both halves are true. Only one of them is tight, and a reader who takes the boxed corollary as the sharp statement would be carrying a spare term.

## What this gate adds beyond theirs

* **Four `β`-inequalities re-derived in exact integers.** The round states four inequalities containing `β` and evaluates every one in float64 with a `1e-12` fudge. Under `2^{βm} = 3^m` each is exact:
  `Q > βL ⟺ 2^Q > 3^L`; `m_in > Q + log₂(M/Z₀) ⟺ 2^{m_in}Z₀ > 2^Q M`; `cap < (β−1)p + 1 ⟺ 2^{cap+p} < 2·3^p`; and `L < ((β−1)p − log₂(M/Z₀) + 1)/β ⟺ 3^L M 2^p < 2·3^p Z₀`. Both routes are computed; they agree everywhere, so the fudge is not deciding anything.
* **Theorem 15.1's converse and Theorem 16.1's `only if` half, counted.** Their checker counts only the low-activation branch (`ν₃(𝔡) < L`); the converse `raise`s but increments nothing, leaving 8,641 high-activation nodes invisible in their report. Theorem 16.1's converse is not tested at all. Both are counted here, over 2.2 million probes.
* **`v₂`/`v₃` of zero return `None`, not `10⁹`.** Their helpers return a sentinel that is a real number and participates in comparisons; a `None` cannot silently win one.
* **The toll cross-read against RUN-050.** A-U.2d.22 stated it with a `−1`; this round drops it, exactly one bit stronger. RUN-050's archived log records a tightest margin of 15.1667×, and the measurement here is 7.5833× — half, as it must be. The strengthening is real and still holds.
* **A frontier constant with no generator.** `ternary_reset_at_faithful_benchmark` appears in the constants frontier, is never computed by the checker, and shares its exact value with `faithful_minus_resonance_threshold`. Neither fact is visible to a per-file check.

## Standing items

The self-validation record carries **zero digests** for the tenth round running, and its pass flag has been renamed again — `all_pass` → `overall_pass`. Reading only the old name would have rendered a real `False` as `None`, so the gate now accepts either and says which it found. One NO-GO heading (20.4) has no ledger counterpart, and the ledger carries 9 no-go entries against the paper's 7 headings. Per the RUN-032 line, these are findings in this log, not gate failures.

<!-- BEGIN GENERATED measured block: python code/src70_emit_report_block.py -->

**The population.** **6425** zero-lift local bridges from **6017** distinct sources, longest tail 73 — reproducing their `finite_zero_lift_bridges` exactly at their own limit.

**Theorem 3.1, the parity refinement.** Over **143131** congruent windows giving **143131** returns, **2862** carry zero defect. Every one satisfies `n = 2^{Q+1} v`, `n' = 2·3^L v` with `v ≥ 1`: **0** violations of the refinement, **0** outputs not in the refined form, **0** non-positive quotients, and **0** returns where the previous round's `u = n/2^Q` came out ODD — that is, `u` is even on all of them, which is exactly the sharpening this round adds. The smallest `v` is **5**, so A-U.2d.22's `u ≥ 1` was loose by the factor this round identifies, not by an accident of the sample. Longest zero-defect return seen: **4**.

**Confirmed against the previous round's own population.** Theorems 3.1 and 4.1 are also run against RUN-050's **7845** bridges, whose returns come from the erasure walker rather than this round's window scan — different limit, different objects, **2935** zero-defect returns. Result: **0** with `u` odd, **0** and **0** violations of the refined form and its parity, **0** and **0** of the two transfer identities, smallest `v` again **5**. The sharpening holds on data collected before the claim existed.

**Theorem 4.1, the cross-adic transfer.** `ν₂(n') = ν₂(n) − Q` failed **0** times and `ν₃(n') = ν₃(n) + L` failed **0** times. The return spends binary divisibility and buys ternary divisibility at a fixed rate, exactly.

**Theorem 5.1, whose two halves have opposite tightness.** The per-position ceiling `m_ℓ ≤ ⌈βh⌉ − ⌈βℓ⌉ − (h−ℓ)` failed **0** times over **31035** positions and is **attained at 12153 of them (39.2%)**, smallest slack **0** — a live, binding bound. Its corollary `H_max < (β−1)h + 1` failed **0** times, with a smallest integer slack of **1** and a largest `H_max` of **12**. But the `+1` is not load-bearing: the strictly stronger `H_max < (β−1)h` also holds, with **0** violations across all **6425** bridges. The same theorem is attained in one half and carries a spare term in the other.

**Theorem 6.1, the temporal delay, in exact integers.** The round states four inequalities containing `β` and evaluates every one in float64. All four are exact under `2^{βm} = 3^m`, and both routes were computed on **2862** zero-defect nodes: the lift toll `2^{m_in} Z₀ > 2^Q M` failed **0** times, the capacity side **0**, the chained bound `2·3^p Z₀ > 2^{Q+p} M` **0**, and the length bound `3^L M 2^p < 2·3^p Z₀` **0**. The two float routes disagreed with exact arithmetic **0** and **0** times — so their `1e-12` fudge is not deciding anything here. The toll's tightest margin is **7.5833**, with **0** nodes one bit from failing; the earliest prefix at which a zero-defect return appears is **p = 2**.

**The toll, cross-read against the previous round.** A-U.2d.22 stated it as `m > Q + log₂(M/Z₀) − 1`, and RUN-050's archived log records its tightest margin as **15.1667×**. This round drops the `−1`, which is exactly one bit stronger, and the margin measured here is **7.5833** — half of it, as it must be. The strengthening is real and still holds.

**Theorem 7.1, decided rather than scanned.** A length-one zero-defect return needs `1 = (2^q − 3)r` with `r ≥ 1`, so `2^q − 3` must be a positive divisor of 1. Over **4000** values of `q` there is **1** solution and **0** others; for **3998** of those `q` the divisor already exceeds 1, which is what settles every remaining `q` at once. **The bundle scans `q < 20, r < 100` instead — 1881 iterations whose assert body is reached exactly 1 time, and which increments no counter at all**, so this theorem is absent from their report. The existence half was checked separately on **96** actual transitions `x = 1 + 8Mv`: **0** wrong valuations, **0** wrong targets, **0** non-zero defects, **0** misaligned endpoints.

**Theorem 8.1, the q = 2 resonance runs.** **840** runs over **17220** steps, longest **40**: **0** wrong valuations, **0** states not congruent to 1, **0** wrong start quotients, **0** wrong endpoints, **0** wrong binary spends, **0** wrong ternary gains, and **0** runs whose whole word failed to be a zero-defect return.

**Theorems 15.1 and 16.1, both halves each.** Over **587716** nonzero-defect nodes, **579075** are low-activation (`ν₃(𝔡) < L`) and **8641** are high-activation. The reset `ν₃(n') = ν₃(𝔡)` failed **0** times on the first group. **The bundle counts only that group**; its converse branch raises but increments nothing, so the **8641** high-activation nodes are invisible in their report — measured here, **0** violations. Theorem 16.1's `ν₂(n') ≥ b ⟺ 3^L n + 𝔡 ≡ 0 (mod 2^{Q+b})` was probed **2203444** times up to `b = 7`: **0** failures of the forward direction and **0** of the converse, which the bundle does not test at all.

**Their three synthetic blocks, measured rather than trusted.** The accounting block runs **20000** trials. Its two telescoping assertions hold — **0** and **0** failures — but that is not evidence: rebuilding the generator with `Q` reduced so the supercriticality it is about is FALSE by construction, the telescoping stayed green on **20000 of 20000** broken inputs while the supercriticality assertion went red on **14781**. Two of the three assertions are identities of the construction; the third is live but true by construction of the generator, which sets `Q = ⌈βL⌉ + randint(0,4)`. The reservoir block reports **two** counters of 20,000 each, and **both increment outside a guard** that opened on **12176 of 20000** samples (60.9%) — so 40,000 published checks are one block, evaluated 12176 times, counted twice. Its assertion held (**0** violations) with a smallest margin of **0.001003**.

**The published rows.** **24** zero-defect and **12** nonzero-defect rows recomputed from their own fields: **0** quotient-identity failures, **0** parity-refinement failures, **0** valuation fields disagreeing, **0** supercriticality failures, and on the nonzero rows **0** identity and **0** defect-valuation disagreements.

**The constants, and one with no generator.** **8** checked, **2** exact to the last bit, **6** matching the float64 chain rather than the nearest double, **0** disagreeing with both, **0** undecided, **0** missing, **0** where frontier and report disagree. Two of them are differences of nearly-equal quantities and land 21 and 16 ulps out, which is the chain and not an error. **Cross-read, the frontier carries 1 constant that the checker never computes** — `ternary_reset_at_faithful_benchmark` — and it shares its exact value with `faithful_minus_resonance_threshold`. A per-file check cannot see either fact; only the two artifacts side by side can.

**Their thirteen counters.** **8** reproduce exactly. **5** are covered here by a deterministic enumeration larger than theirs, and the cross-report table names my counter rather than leaving a blank that would read as *not reproduced*. **0** of their checks are covered by nothing here, and **0** report zero. One theorem — 7.1 — has no counter of theirs to compare against at all.

**The bundle as shipped.** **9** files, **8** digests listed, **0** mismatches, **0** checksum lines naming a missing file, and `CHECKSUMS.sha256` with no digest anywhere. The validation record carries **7** per-file entries of which **0** carry a digest — the tenth round in a row recording `pass` without recording what it hashed — and its pass flag has been renamed again, to `overall_pass`. `CHECKSUMS.sha256`, `SOURCE_VALIDATION_AU2d23.json` absent from it entirely. Against the paper, the ledger lists **15** proved items to the paper's **15**, **8** open to **8**, and **9** no-go entries to the paper's **7** headings; **0** open items and **1** no-go headings have no ledger counterpart (20.4). The coverage heuristic passed both its controls.

**The drill.** The instrument self-tests **9** properties before the gate runs, **0** of them failing. **42** defects were planted one at a time: **42** caught by the counter they attack, **0** missed, **0** malformed, 0 caught only by another counter; 2 of 2 controls left the gate undisturbed. Five aim at non-vacuity entries rather than failure counters, because every finding this round is about a population smaller than the counter reporting it.

<!-- END GENERATED measured block -->

## Verdict

Every theorem I can reach independently holds, and the round's central sharpening is confirmed on a population collected before the claim existed. The three findings are about a theorem their report never mentions, three counters that overstate what they test, and one corollary carrying a term it does not need. None contradicts a result.

Next: item 71, `A-U.2d.24 — Binary Replenishment / Ternary Reset Rigidity`.
