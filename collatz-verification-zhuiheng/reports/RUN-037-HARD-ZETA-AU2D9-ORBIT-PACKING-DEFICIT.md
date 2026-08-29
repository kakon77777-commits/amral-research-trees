# RUN-037 — Hard-Zeta A-U.2d.9: one line of arithmetic closes the previous round's open problem, a theorem whose premise real orbits actually meet, and a rounding chain with four links

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d9_Orbit_Packing_Deficit_Rigidity_bundle_v0.1.zip` (source item 55) — 20 sections. Ships a checker, its report, a constants frontier, a theorem ledger, a `CHECKSUMS.sha256`, and a source-validation record in a shape not seen before.
**Tools:** [`src55_orbit_packing_deficit.py`](../code/src55_orbit_packing_deficit.py) · [`src55_drill.py`](../code/src55_drill.py) · [`src55_emit_report_block.py`](../code/src55_emit_report_block.py)
**Logs:** [`src55-au2d9.json`](../data/gate-logs/src55-au2d9.json) · [`src55-drill.json`](../data/gate-logs/src55-drill.json)

**Result: A-U.2d.8 listed as open that a real orbit ought to beat the consecutive-odd packing envelope, with no quantitative theorem. This round closes it in one line — `3n+1 ≡ 1 (mod 3)`, so no accelerated image is ever divisible by three — and the local exponent moves from `1/6` to `1/9`. Nearly all of it is decidable, and all of it holds. Section 11 is the round's most useful feature: its premise is first-crossing subcriticality, which is what a first-crossing interval *is*, so unlike the last two rounds' depth caps it is genuinely testable — and it was tested on every prefix. Two findings: a rounding chain in which four derived constants each inherit their parent's last-bit error rather than being computed from their closed forms, and a constant published with two different values in two artifacts of the same bundle.**

---

## The whole deficit, in one congruence

A-U.2d.8 bounded the multiplicative correction by the consecutive-odd envelope
`𝒫_odd(y,L)`, and named in its own ledger the thing it could not prove: that a
genuine orbit should do strictly better, with no quantitative statement
available.

The answer turns out to need no machinery at all. `3n+1 ≡ 1 (mod 3)`, and
dividing by a power of two cannot introduce a factor of three, so **no
accelerated image is ever divisible by three**. The states are therefore packed
not into the odd numbers but into the integers coprime to 6 — mean spacing 3
rather than 2 — and the envelope tightens from `Θ(L^{1/6})` to `Θ(L^{1/9})`,
with the ratio decaying like `L^{−1/18}`.

Two further refinements fall out of the same congruence. Every post-entry state
lies in `{1,5} (mod 6)`; and combined with A-U.2d.5's `3 (mod 4)`, every
post-entry B-anchor lies in `{7,11} (mod 12)`, whose gaps alternate `4, 8` with
mean `6` — sharpening the nested-anchor spacing from 4 to 6.

All of that is decidable in integers, and the measured block below reports it:
the sieve on tens of thousands of images, the residue sets on every post-entry
state, the admissible positions, the envelope, and the two-progression Gamma
form — with **zero** disagreements throughout.

## The Gamma form, again needing no Gamma

Section 5 writes the sieved envelope as a product of two Gamma quotients. As at
RUN-036, at integer parameters each quotient is a **Pochhammer ratio** —
`∏(a+m)/(b+m)` with `a = (y+c)/6 + 1/18` — which is the product it was built
from. So both sides are the same rational, and this run's error is zero where the
shipped checker reports `2.0×10⁻¹³`.

The independent `math.lgamma` cross-check ran anyway, with the cancellation-aware
tolerance RUN-036 had to learn: `ln 𝒫₆` is a difference of eight log-gammas, and
relative error under that much cancellation means nothing.

## The theorem whose premise real orbits actually meet

The last two rounds both produced depth caps that could not be tested. A-U.2d.8's
section 9.1 needed `z₁ > y_r`, met by none of 24,010 chains; this round's
Lemma 7.1 and Theorem 8.1 need the same thing and fare the same way. Their
combinatorial core can still be checked, and was: **499,149** enumerated sets of
`{7,11} (mod 12)` anchors, with zero spans below the proof's own `6(r−1) − 2`
allowance and zero failures of the phase rule that closes the remaining gap.
Theorem 8.1's two forms were checked for equivalence on every chain, which is
universal algebra and holds.

Section 11 is different, and it is the reason this round is worth more than the
last two. Theorem 11.2 assumes **first-crossing subcriticality**, `Σq_j < βm`.
That is not a survival hypothesis — it is the defining property of a
first-crossing interval, and it is decidable as the exact integer comparison
`2^Q < 3^m`. Every prefix tested satisfies it, so the theorem was applied to all
of them, and it holds on all of them.

Its `17/24` is worth checking rather than accepting, because the coefficient is
where the sieve does its work. Lemma 11.1 says `q(n) = k` selects exactly one
residue class mod `2^{k+1}`; among `W` consecutive integers the odd **3-free**
ones in that class number at most `W/(3·2^k) + 1`, and `3·(1/6) + 2·(1/12) +
1/24 = 17/24`. Without the 3-sieve the same sum gives `17/16`. Both the
per-valuation capacity and the weighted bound were enumerated directly.

## Finding 1 — a rounding chain with four links

Five constants here have closed forms, and the derived ones drift:

> `C₆ = e^{1/21+1/27}·4^{1/9}` — **exact**
> `C₉ = C₆/6` — **−1 ulp**
> `c₉ = C₉^{−9/8}` — **+1 ulp**
> `μ9 = (9θ★−1)/8 = 9709/102328` — **3 ulps**

and the mechanism reproduces at every link. Dividing the *published double* `C₆`
by six gives the published `C₉` bit for bit; raising that `C₉` to `−9/8` in
float64 gives the published `c₉`; putting the float64 `θ★` through `μ9`'s own
formula gives the published `μ9`. Each derived constant is computed from its
already-rounded parent rather than from its closed form, so the error compounds
down the chain.

RUN-036 found two links of this at A-U.2d.8. Here there are four, and `μ9`'s
three ulps are the largest drift the sweep has measured. Still last-bit — no
result changes — but it is now a pattern with a named cause rather than an
oddity. Everything *not* derived is exact: `β`, `C₆`, the density, and the three
rational exponents `1/6`, `1/9`, `1/18`.

## Finding 2 — one constant, two values, one bundle

`qclass_span_mean_spacing_lower` is `24(4−β)/17`. The checker report gives
`3.40946470486425` and the constants frontier gives `3.4094647048642504`. These
are different doubles, one ulp apart.

The report is right: `3.40946470486425` is the correctly rounded double of
`24(4−β)/17`, and it is also what the paper prints. The frontier's copy is the
outlier. So two of the bundle's three statements of this constant agree with each
other and with the arithmetic, and the third does not.

The same two artifacts also **rename** two constants between them — `beta` /
`beta_log2_3` and `new_3_sieved_product_exponent` /
`syracuse_sieved_product_exponent`. Nothing is wrong with either name; a reader
joining the two files on key names would simply lose both.

## The manifests, and a fifth schema

`CHECKSUMS.sha256` and the source-validation record agree on every digest they
share, and every digest in both reproduces. Only `CHECKSUMS.sha256` itself is
covered by neither — unavoidable for a self-manifest — but unlike A-U.2d.8 there
is now no `scope_note` declaring that gap.

The validation record's shape has changed again, and this is the fifth in six
bundles: a dict under `artifact_sha256_before_manifest` at item 50, a list under
`files` at 51 and 52, a dict under `files` at 53, a list again at 54, and here
**three purpose-named blocks with no `files` key at all**. A reader written for
any one of the others sees zero files and reports zero mismatches, which is
indistinguishable from a clean bill — so the reader names which shape it used and
guards on an empty read.

One of those blocks, `checker_script`, carries a digest with **no filename**. It
resolves — by looking the digest up among the files actually present, it is the
checker — but the record identifies that file by its position in the schema
rather than by name, and a manifest that cannot say what it is describing is
worth noting.

---

<!-- BEGIN GENERATED measured block: python code/src55_emit_report_block.py -->

**The sieve and what it buys, on real orbits.** Every row is decided in integers.

| what | measured against | value |
| --- | --- | --- |
| odd integers mapped through `Syr` | Theorem 3.1 | `20000` |
| …**images divisible by three** | must be zero | `0` |
| post-entry orbit states | Corollary 3.2, `1` or `5 (mod 6)` | `24688` |
| …outside `{1,5} (mod 6)` | must be zero | `0` |
| post-entry sources with `L ≥ 2` | 999 pre-entry sources excluded | `11914` |
| …not `3 (mod 4)` / not `7` or `11 (mod 12)` | A-U.2d.5's result and Corollary 3.3's refinement of it | `0 / 0` |
| **sources with `L = 1`, which the premise excludes** | of which 11775 are outside `{7,11} (mod 12)` | `11775` |

That last row is the reason the premise is stated. Corollary 3.3 refines a result that needs `L ≥ 2`; applied to every first-crossing source instead, **11775** of them would have been reported as violations of a theorem that holds.

**The sieved packing and its Gamma form.**

| what | measured against | value |
| --- | --- | --- |
| segments meeting the packing premise | source minimal and states distinct; 0 fail | `23689` |
| …sorted states below their admissible position `a_k(y)` | Definition 4.1, longest `L` = 51 | `0` |
| …explicit admissible positions wrong | `a_{2m} = y+6m`, `a_{2m+1} = y+6m+4` or `+2` | `0` |
| …`a_k(y)` below the uniform bound `y+3k−1` | must be zero | `0` |
| …**violations of Theorem 4.2** `𝒫 ≤ 𝒫₆(y,L)` | must be zero | `0` |
| …where the sieved envelope exceeds the odd one | the deficit must point the right way | `0` |
| …**where Theorem 5.1's two-progression form ≠ the product** | as exact Pochhammer quotients | `0` |
| designed `(y,L)` pairs for Theorem 5.1, largest `L` = 400 | exact disagreements: 0 | `42` |
| …disagreeing with `math.lgamma` beyond its cancellation bound | worst error `1.137e-12`, `0.12×` the bound the subtraction costs | `0` |

The shipped checker reports `max_gamma_relative_error = 1.9774418778912632e-13`. This run's is `0`: at integer `n` the Gamma quotient is the Pochhammer product it was built from, so both sides are one rational.

**The exponents, empirically.** `𝒫₆ = Θ(L^{1/9})` and `𝒫₆/𝒫_odd = Θ(L^{−1/18})` are asymptotic, so what is checked is that the measured exponent moves toward the claim and that the deficit stays negative — not that either is reached at finite `L`.

| `y` | `L` | sieved exponent → `1/9` | odd exponent → `1/6` | deficit |
| --- | --- | --- | --- | --- |
| `7` | `200` | `0.09645` | `0.13160` | `-0.03515` |
| `7` | `800` | `0.09936` | `0.13858` | `-0.03922` |
| `7` | `3200` | `0.10135` | `0.14335` | `-0.04200` |
| `7` | `12800` | `0.10278` | `0.14675` | `-0.04398` |
| `11` | `200` | `0.08777` | `0.11626` | `-0.02849` |
| `11` | `800` | `0.09242` | `0.12625` | `-0.03382` |
| `11` | `3200` | `0.09559` | `0.13309` | `-0.03750` |
| `11` | `12800` | `0.09786` | `0.13799` | `-0.04013` |

Non-monotone steps toward `1/9`: `0`; toward `1/6`: `0`; deficits not negative: `0`.

**Lemma 7.1, split into the half that can be enumerated and the half that cannot be tested.**

| what | measured against | value |
| --- | --- | --- |
| residue sets of `{7,11} (mod 12)` anchors enumerated | depths 2 to 6 | `499149` |
| …**spans below `6(r−1) − 2`** | the proof's own phase allowance | `0` |
| …tight sets whose last anchor is not `11 (mod 12)` | the proof's phase claim | `0` |
| …tight sets whose next admissible state is not exactly `2` higher | what closes the gap to `6(r−1)` | `0` |
| chains built | deepest `r` = 16 | `15832` |
| …**where `z₁ > y_r`**, the premise Lemma 7.1 needs | a first-crossing endpoint is where the slack drops | `0` |
| …Lemma 7.1 applied / violated | premise-gated | `0 / 0` |
| **Theorem 8.1's two forms disagreeing** | universal algebra, checked on all 15832 chains | `0` |
| …Theorem 8.1 applied / violated | 3060 chains are in the low-source regime `7 ≤ y₁ ≤ L` | `0 / 0` |

**Section 11 — the one theorem here whose premise real orbits do meet.** Theorem 11.2 assumes first-crossing subcriticality, `Σq_j < βm`, which is what a first-crossing interval *is*; the test is the exact integer comparison `2^Q < 3^m`.

| what | measured against | value |
| --- | --- | --- |
| valuations `k` checked for Lemma 11.1 | `q(n) = k` must select exactly one class mod `2^{k+1}` | `10` |
| …selecting a number of classes other than one | must be zero | `0` |
| capacity windows enumerated | `N_k ≤ W/(3·2^k) + 1` — the `3` is the sieve | `20` |
| …exceeding that per-valuation capacity | must be zero | `0` |
| …**exceeding the weighted bound `17W/24 + 12`** | where the `17/24` in the theorem comes from | `0` |
| proper prefixes examined | longest `m` = 50 | `9517` |
| …**meeting subcriticality** `2^Q < 3^m` | 0 fail; 0 have a repeated state | `9517` |
| …**Theorem 11.2 applied / violated** | `W > (24/17)((4−β)(L−1) − 12)` | `9517 / 0` |

**Sections 6 and 8 as implications**, over `36` grid points of which `14` are low-source:

| derivation | violations |
| --- | --- |
| **Theorem 6.1** the 3-sieved harmonic bound | `0` |
| **Corollary 6.2** `𝒫₆ ≤ C₆(L/y)^{1/9}` | `0` |
| **Corollary 8.2** follows from the exact cap of 8.1 | `0` |
| **Corollary 8.3** inverts it | `0` |
| `μ9 = (9θ★−1)/8` as stated | `0` |
| `1/18 = 1/6 − 1/9` | `0` |

**Constants, against their closed forms.** `θ★ = 2500/12791` and `μ9 = 9709/102328` are exactly rational.

| constant | published | closed form | ulps |
| --- | --- | --- | --- |
| `C6_uniform_product` | `1.2695833698941745` | `exp(1/21+1/27) * 4^(1/9)` | `0` |
| `C9_depth` | `0.21159722831569575` | `C6/6` | `-1` |
| `c9_inversion` | `5.738538220631228` | `C9^(-9/8)` | `1` |
| `qclass_span_mean_spacing_lower` | `3.4094647048642504` | `24(4-beta)/17` | `1` |
| `qclass_span_density_upper` | `0.2933011738098681` | `17/(24(4-beta))` | `0` |
| `theta_star` | `0.19544992572902825` | `1/(rho+1) = 2500/12791` | `1` |
| `dense_root_source_floor_exponent_mu9` | `0.09488116644515679` | `(9 theta-1)/8 = 9709/102328` | `3` |
| `dense_root_source_floor_exponent_mu8` | `0.03453991087483388` | `(6 theta-1)/5 = 2209/63955` | `2` |
| `old_low_source_product_exponent` | `0.16666666666666666` | `1/6` | `0` |
| `syracuse_sieved_product_exponent` | `0.1111111111111111` | `1/9` | `0` |
| `dynamic_deficit_exponent` | `0.05555555555555555` | `1/6 - 1/9` | `0` |
| `beta_log2_3` | `1.584962500721156` | `log2 3` | `0` |

The drift is a chain, and every link reproduces. `C₉` is the published `C₆` divided by six **as doubles**: `True`. `c₉` is that `C₉` raised to `−9/8` as doubles: `True`. `μ9` is the float64 `θ★` put through its own formula: `True`. And the checker report's spacing is the float64 reciprocal of the density: `True`. Each derived constant inherits its parent's rounding instead of being computed from the closed form.

**The two artifacts disagree on `1` constant** and rename `2`:

| constant | checker report | constants frontier | ulps apart |
| --- | --- | --- | --- |
| `qclass_span_mean_spacing_lower` | `3.40946470486425` | `3.4094647048642504` | `1` |
| renamed | `beta` | `beta_log2_3` | — |
| renamed | `new_3_sieved_product_exponent` | `syracuse_sieved_product_exponent` | — |

| the paper prints | verdict |
| --- | --- |
| `C9_depth` = `0.21159722831569575…` | OVER-PUBLISHED |
| `c9_inversion` = `5.738538220631228…` | correctly rounded at the last digit |
| `qclass_span_mean_spacing_lower` = `3.40946470486425…` | exact to every published digit |
| `theta_star` = `0.19544992572902825…` | OVER-PUBLISHED |
| `mu8` = `0.03453991087483388…` | OVER-PUBLISHED |
| `mu9` = `0.09488116644515679…` | OVER-PUBLISHED |
| `C6_uniform_product` = `1.2695833698941745…` | truncated rather than rounded at the last digit |
| `qclass_span_density_upper` = `0.2933011738098681…` | correctly rounded at the last digit |
| `one_sixth` = `0.166666…` | truncated rather than rounded at the last digit |
| `one_ninth` = `0.111111…` | exact to every published digit |

**The ledger against the paper's own section 18.**

| the paper says | the JSON ledger says | shortfall |
| --- | --- | --- |
| §18.1 proved internally: `15` | `proved_internally`: `12` | `3` |
| §18.2 inherited: `8` | `inherited_internal`: `0` | `8` |
| §18.3 external grounding: `3` | `external_technical_input`: `0` | `3` |
| §18.4 explicitly open: `5` | `heuristic_or_open`: `3` | `2` |

§14's `7` `NO-GO` headings against the ledger's `0`; titles with no ledger entry sharing a distinctive word: *14.1 all-odd consecutive packing as a dynamically sharp envelope*; *14.2 only constant-factor loss from exact transition arithmetic*; *14.3 sixth-root low-source exponent as the final local exponent*; *14.4 B-anchor spacing remains $4$*; *14.5 pure $3$-sieve exhausts the transition geometry*; *14.6 diameter improvement may be silently promoted to harmonic improvement*; *14.7 any use of the old rotation headroom as a telescope*.

**The manifests.**

| what | measured against | value |
| --- | --- | --- |
| files in the bundle | `CHECKSUMS.sha256` lists 8, the validation record 7 | `9` |
| …digests that do not reproduce, in either manifest | must be zero | `0` |
| …where the two manifests disagree | on the files both list | `0` |
| …**digests the record gives with no filename at all** | resolved by looking the digest up among the files: checker_script → verify_Hard_Zeta_AU2d9_orbit_packing_deficit.py | `1` |
| …files covered by neither manifest | `CHECKSUMS.sha256`; a scope note declares it: `False` | `1` |
| validation-record shape | three purpose-named blocks, no `files` key (item 55): formal_source_validation, json_validation, checker_script | `—` |
| the record says its checker rerun matches its report | its own claim, not rechecked here | `True` |
| the checker's named checks independently confirmed | of 8; 3 named as not covered here | `5` |
| this run's own bracket self-checks | 0 failed | `8` |
| defects planted / caught by the check named for each | 1 robustness property; 0 malformed; 2 controls, 2 undisturbed | `31 / 31` |

**Not covered here**, named rather than implied: *harmonic_envelope*; *b_anchor_endpoint_gap*; *asymptotic_exponent_ratio*.

Every figure above is emitted by `code/src55_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

Brackets are imported from `src53_plateau_reset` and `src54_low_source_saturation`,
certified there rather than re-derived. Two of this gate's own errors were caught
before publication.

**A false 11,775.** Corollary 3.3 refines A-U.2d.5's `3 (mod 4)`, and that result
needs `L ≥ 2`. Applied to every first-crossing source instead, half of them
"violate" it — because an `L = 1` source is not what the theorem is about. The
premise-first habit caught it; the drill's `D4` deletes the `L ≥ 2` branch and
requires the run to go red, which is what proves the gate is load-bearing rather
than merely exclusive.

**Three constants that could not be decided.** The certified `β` bracket is exact
but `10⁻⁶` wide, which cannot pin a double, so the two q-class constants and `β`
itself came back undecided. `β = ln3/ln2` from two certified logarithms is sixty
digits wide and every comparison decides. That the coarse bracket contains the
tight one is now a named check rather than an assertion — RUN-036's lesson, since
an assertion crashes and a crashed gate is a malformed drill result rather than a
caught defect. There are eight such self-checks, and three drill defects aimed at
them.

## What the checker claims and this run did not check

The report names eight checks. Five are independently confirmed here — the image
sieve, the Gamma formula, the sieved packing, the q-class residue capacity, and
the proper-prefix span budget. The other three are **named** in the log: the
harmonic envelope, the B-anchor endpoint gap, and the asymptotic exponent ratio.

The checker's scope warning — that it instantiates no divergent orbit and proves
neither Collatz nor linear B-density nor the global asymptotic conjecture — is
intact and correct. The validation record adds two notes in the same spirit,
including that the q-class span theorem is a diameter result and is not promoted
to a harmonic exponent. That restraint is the round's own `NO-GO 14.6`, and it is
the right one: the span bound controls the diameter of the realized state set,
not the spacing of its order statistics.

## Route map

`ROUTE_MAP v2.9`. The constants frontier names item 56 as
`A-U.2d.10 — Valuation-Class Harmonic Deficit Rigidity`.

## What this run does not claim

1. That Lemma 7.1 or Theorem 8.1 hold. Their premise `z₁ > y_r` is met by no
   real chain. Lemma 7.1's combinatorial core was enumerated and its algebra
   checked; the orbit statements were not tested.
2. That `𝒫₆ = Θ(L^{1/9})` or the `L^{−1/18}` deficit hold asymptotically. What
   was measured is that the finite-`L` exponents move toward `1/9` and `1/6` and
   that the deficit stays negative — a trend, not a proof.
3. That the dense-support root-source floor (§12) or the collision-surface
   exponents (§13) hold. Only their constants and the relations between them were
   recomputed.
4. That the q-class span theorem gives a harmonic-product improvement. It does
   not, the round says so, and this run did not test the stronger statement.
5. That the shipped checker is correct. It was read, never run. The validation
   record's claim that a rerun matches its report is that record's claim, not a
   result of this run.
