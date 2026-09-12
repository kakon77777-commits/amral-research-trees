# RUN-076 — Attack 09, rewritten from this side: the auxiliary character of an Eisenstein degeneration for 389.a1 at p = 11 — GPT-6's χ₈ has root number −1 and a vanishing even first layer (L(E, χ₈ψ, 1) = 0 for the order-5 ψ of conductor 11 as well), the quadratic characters whose central value survives are listed with their twisted L-values as exact integers, and the mod-11 eigenline is tied to those integers by one unit per sign

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** GPT-6's **Attack 09**, known only from its progress narration pasted by Neo on 2026-09-12 (quoted in §0); the package itself has not arrived and this round does not wait for it — it writes down, with this tree's own arithmetic, what the attack's one new number can and cannot be
**Tools:** [`src78_attack09_auxiliary_character.py`](../code/src78_attack09_auxiliary_character.py), [`src70_kurihara_modular_symbols.py`](../code/src70_kurihara_modular_symbols.py), [`src15_phase2_anchor.py`](../code/src15_phase2_anchor.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src78-attack09-auxiliary-character.json`](../data/gate-logs/src78-attack09-auxiliary-character.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

> **Postscript, written before commit.** This round was computed from the narration. The package arrived the next morning and is verified at [RUN-077](./RUN-077-ATTACK09-EISENSTEIN-LEADING-TERM.md): its number is **not the central value**. It is `λ₈(0) = L₁₁(E ⊗ χ₈, x⁻¹)` — the ordinary 11-adic L-function of the twist at the full character `x ↦ x⁻¹`, the odd Teichmüller branch at `s = 0`, a non-critical point — computed on the **minus** modular symbol, normalised at its first nonzero coordinate (index 3), which is exactly this round's minus eigenline. That value is `≡ 5 (mod 11)`, and RUN-077 reproduces it coordinate for coordinate. Everything computed below stands; §1–§2 are about the central value and the even (plus-line) first layer, which the package does not use, and §5's replacement list is for that reading only. The relation between the two: this round's minus-line branch `T₉⁻ = 3` for `χ₈` is `−8⁹` times the package's weighted sum `9`, i.e. the same number in another convention. The unit `λ⁻ = 6` of §4 also settles a point the package flags: its index-3 normalisation is a unit multiple of the `Ω⁻`-normalised symbol, so its mod-11 statement is meaningful in the Néron normalisation.

**Result: Attack 09, as narrated, runs a Loeffler–Rivero Eisenstein degeneration with the auxiliary form `E₂(1, χ₈)` and reports one new number — "the extra twisted 11-adic L-value ≡ 5 (mod 11), so nonzero", over forty cusp paths. For 389.a1 at 11 the central value of that twist is zero, and so is the whole even first layer — the package, when it arrived (RUN-077), turned out to use neither; see the postscript. A weight-2 Eisenstein series `E₂(1, χ)` exists only for `χ` even, so `χ₈ = (8/·)`; the root number of `E ⊗ χ₈` is `χ₈(−389)·w(E) = (2/389) = −1` because `389 ≡ 5 (mod 8)`, so `L(E, χ₈, 1) = 0` exactly, and no normalisation moves a zero. Beyond the sign, `L(E, χ₈ψ, 1) = 0` for the four order-5 characters `ψ` of conductor 11 as well — one Galois orbit, hence one event — computed two ways: from this tree's `a_n` by the functional-equation series, `|L| ≤ 3.2·10⁻¹⁵` against controls of size 1; and on RUN-068's mod-11 plus eigenline, where every `χ₈`-twisted symbol `[a/11]_{χ₈}⁺` and every one of the ten tame branches is 0. The entire even part of the first cyclotomic layer of `L₁₁(E ⊗ χ₈)` vanishes, and the narrated `5 (mod 11)` is not any first-layer quantity of `χ₈` on the plus line — it is one on the minus line, the value at `x⁻¹`, which RUN-077 identifies and reproduces. Then the constructive half: for all 54 fundamental discriminants `|D| ≤ 100` prime to 11, the root number of `E ⊗ χ_D`, the twisted sum `S_D = Σ χ_D(b)[b/|D|]^±` on the eigenline of the right sign, the level-`11|D|` sum with its Hecke identity `Σ χ_D(c)[c/11|D|] = (a₁₁ − 2χ_D(11))·S_D`, the first-layer total of the Mazur–Tate–Teitelbaum measure against `(1 − χ_D(11)/α)²·S_D`, and — for root number +1 — `L(E, χ_D, 1)·√|D|/Ω^±` from the `a_n`, which is an exact integer every time: `4` for 22 twists, `16` for `D = −51`, `36` for `D = −43`, `0` for `D = 65, 93, −47`. **One unit per sign, `λ⁺ = 10` and `λ⁻ = 6`, carries those integers onto the mod-11 sums for all 27 twists, zero sets included** — the first time this tree's eigenline is tied to archimedean L-values rather than to Hecke eigenvalues alone. The smallest admissible even character is `χ₅`: root number +1, `L(E, χ₅, 1)√5/Ω⁺ = 4`, all five even tame branches nonzero mod 11, Euler factor `(1 − 1/α)² ≡ 5` a unit; the smallest odd one, for a weight-1 Eisenstein series and the minus symbols, is `χ₋₃`. **Loeffler–Rivero's comparison factor is not reproduced here; nothing about `𝔰₁₁`, `C`, `B₂` or BSD moves.**

---

## §0 — what Attack 09 said

The only record of Attack 09 is GPT-6's own progress narration, pasted by
Neo on 2026-09-12. The sentences this round answers:

> 我選到一個可具體使用的輔助形式：E₂(1, χ₈)，其中 χ₈ 是模 8 的二次特徵。在 p = 11，它滿足退化理論需要的 decency 與 non-criticality 條件 …
>
> 有一個關鍵新結果：額外出現的扭曲 11-adic L 值，我算到它在明確的模符號正規化下為 5 mod 11，所以確實非零。這使退化後的類能沿 cyclotomic 方向除去兩次零點 …
>
> Attack 09 的新程式已執行完成，四十條 cusp 路徑與每項測度值都附在輸出中。交接稿也分清楚了：twisted moment 的非零性是本輪新算出的；退化比較引用已發表定理；C、B₂ 的實際座標及 s₁₁ 仍未算出。

Forty cusp paths is `φ(88) = 40`: the units modulo `8·11`, the first layer
of the cyclotomic tower twisted by a character of conductor 8. That is the
object computed below.

## §1 — the parity and the root number

| step | fact | recomputed |
| --- | --- | --- |
| a weight-2 `E₂(ψ, φ)` needs `(ψφ)(−1) = (−1)² = +1` | with `ψ = 1`, `φ = χ₈` must be even: `χ₈ = (8/·)`, kernel `{±1 mod 8}` | `χ₈(−1) = +1` |
| `w(E)` for prime conductor with multiplicative reduction is `a_N` | `a₃₈₉ = +1` (split, counted on the node) | `+1` |
| `w(E ⊗ χ_D) = χ_D(−N)·w(E)` for `D` prime to `N` | `χ₈(−389) = (8/389) = (2/389)`, and `389 ≡ 5 (mod 8)` | `−1` |
| hence `L(E, χ₈, 1) = 0` | exactly, by the functional equation | — |
| on the plus eigenline (RUN-068, `λ(1,5) = 1`) | `[1/8]⁺ = [3/8]⁺ = 0`, so `S₈ = Σ χ₈(b)[b/8]⁺ = 0` | `0` |
| the forty paths | `Σ_{c ∈ (Z/88)^×} χ₈(c)[c/88]⁺ = 0`; the first-layer total `α⁻¹Σχ₈(c)[c/88]⁺ − 10α⁻²S₈ = 0` | `0`, `0` |

The two symbols `[1/8]⁺`, `[3/8]⁺` are the whole plus part at level 8, and
both are forced to zero over `Q`: their sum is a multiple of `[0]⁺ = L(E,1)/Ω⁺ = 0`,
their difference is `L(E, χ₈, 1)` up to a nonzero constant. The forty
per-path values are in the log (`forty_paths`); 32 of the 40 plus symbols
`[c/88]⁺` are nonzero individually, and their `χ₈`-weighted sums vanish.

## §2 — beyond the sign: the whole even first layer

The tame branches of the twisted first layer are
`T_j = Σ_{c ∈ (Z/88)^×} χ₈(c)·c^j·[c/88]^±`, `j = 0..9`, with `ω^j(c) ≡ c^j
(mod 11)`; `T_j` is the mod-11 value of `L₁₁(E ⊗ χ₈)` at the tame character
`ω^j`, up to the unit `(χ₈(11)α)⁻¹` and a Gauss sum.

| line | `T_0 … T_9` | twisted symbols `[a/11]_{χ₈}⁺ = Σ_b χ₈(b)[a/11 + b/8]⁺`, `a = 1..10` |
| --- | --- | --- |
| plus (even branches live here) | `(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)` | `(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)` |
| minus (odd branches) | `(0, 9, 0, 4, 0, 10, 0, 3, 0, 3)` | — |

Every even branch is zero mod 11, i.e. every `χ₈`-twisted plus symbol at
the cusps `a/11` is zero mod 11. That is more than the root number forces
(`j = 0` only), so it was checked over `C`: for the four characters `ψ` of
`(Z/11)^×` of exact order 5, the newform `f ⊗ χ₈ψ` has level `389·88²` and
root number `w(E)·χ(389)·τ(χ)²/88`, and

| `ψ` | `|L(E, χ₈ψ, 1)|` | `|L|·√88/Ω⁺` | terms |
| --- | --- | --- | --- |
| `ψ₁` | `1.17·10⁻¹⁵` | `2.2·10⁻¹⁵` | 12,431 |
| `ψ₂` | `1.26·10⁻¹⁵` | `2.4·10⁻¹⁵` | 12,431 |
| `ψ₃` | `2.89·10⁻¹⁵` | `5.4·10⁻¹⁵` | 12,431 |
| `ψ₄` | `3.18·10⁻¹⁵` | `6.0·10⁻¹⁵` | 12,431 |
| control `χ₅ψ_t` | `0.6716` each | `1.000` each | 7,252 |
| control `χ₁₃ψ_t` | `1.7643`, `0.0983`, `0.0983`, `1.7643` | `4.236`, `0.236`, `0.236`, `4.236` | 15,000 |

The four values are Galois conjugates of one algebraic number of bounded
denominator (Shimura), so this is one zero, not four coincidences; the
controls show the same series producing values of size 1 for the
neighbouring characters (`χ₁₃ψ`'s algebraic parts are the units
`2 ± √5`). Two independent computations — the `a_n` over `C` and the Manin
symbols mod 11 — agree that `L(E, χ₈ψ, 1) = 0` for every character `ψ` of
`Gal(Q(ζ₁₁)⁺/Q)`, the trivial one by the root number and the order-5 ones
outright. In BSD terms `E ⊗ χ₈` should gain rank over the quintic field
`Q(ζ₁₁)⁺`; in Iwasawa terms the mod-11 reduction of `L₁₁(E ⊗ χ₈)` has a
zero constant term in every even branch. Either way, **on the plus line — at the central point and at the four
order-5 characters — `χ₈` at `p = 11` has no nonzero first-layer value.**
The odd side is alive (`T_j⁻ ≠ 0`; the package's factor lives there, see
the postscript), and so is the odd character `(−8/·)` — root number `+1`,
`S₋₈⁻ = 2`, `L(E, χ₋₈, 1)√8/Ω⁻ = 4`.

## §3 — every quadratic character to 100

For each fundamental `D` with `|D| ≤ 100` prime to 11 (and to 389): the
root number `w = χ_D(−389)`; the sum `S_D = Σ_{b ∈ (Z/|D|)^×} χ_D(b)[b/|D|]^±`
on the plus line for `D > 0` and the minus line for `D < 0`; the level-`11|D|`
sum `T = Σ χ_D(c)[c/11|D|]^±` over the `10·φ(|D|)` units, which must equal
`(a₁₁ − 2χ_D(11))·S_D`; the first-layer total `α⁻¹T − 10α⁻²S_D` of the
Mazur–Tate–Teitelbaum measure, which must equal `(1 − χ_D(11)/α)²·S_D`
(`α ≡ 7`, `a₁₁ = −4`); and for `w = +1` the archimedean value
`A_D = L(E, χ_D, 1)·√|D|/Ω^±`, `L(E, χ_D, 1) = 2·Σ a_n χ_D(n) e^{−2πn/(|D|√389)}/n`,
`Ω⁺ = 4.980425121710` (both components, RUN-017's convention),
`Ω⁻ = π/AGM(√(e₁−e₃), √(e₂−e₃)) = 1.971737701552`. All mod-11 values are
at RUN-068's scale (`λ(1,5) = 1` on the plus line; the minus line is
normalised at its first nonzero coordinate, index 3).

| `D` | `w` | `χ_D(11)` | `S_D` | `T` | total = Euler·`S_D` | `A_D` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | +1 | +1 | 7 | 2 | 2 = 2 | **4** |
| 8 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| 12 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| 13 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 17 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 21 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| 24 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 28 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 29 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| 37 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| 40 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| 41 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 53 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| 56 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| 57 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| 60 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| 61 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| 65 | +1 | −1 | 0 | 0 | 0 = 0 | **0** |
| 69 | +1 | +1 | 7 | 2 | 2 = 2 | **4** |
| 73 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 76 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 85 | +1 | −1 | 7 | 8 | 6 = 6 | **4** |
| 89 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| 92 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| 93 | +1 | +1 | 0 | 0 | 0 = 0 | **0** |
| 97 | +1 | +1 | 7 | 2 | 2 = 2 | **4** |
| −3 | +1 | −1 | 2 | 7 | 8 = 8 | **4** |
| −4 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| −7 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −8 | +1 | +1 | 2 | 10 | 10 = 10 | **4** |
| −15 | +1 | −1 | 2 | 7 | 8 = 8 | **4** |
| −19 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −20 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| −23 | +1 | −1 | 2 | 7 | 8 = 8 | **4** |
| −24 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −31 | +1 | −1 | 2 | 7 | 8 = 8 | **4** |
| −35 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −39 | +1 | +1 | 2 | 10 | 10 = 10 | **4** |
| −40 | +1 | +1 | 2 | 10 | 10 = 10 | **4** |
| −43 | +1 | +1 | 7 | 2 | 2 = 2 | **36** |
| −47 | +1 | −1 | 0 | 0 | 0 = 0 | **0** |
| −51 | +1 | +1 | 8 | 7 | 7 = 7 | **16** |
| −52 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −56 | +1 | −1 | 2 | 7 | 8 = 8 | **4** |
| −59 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| −67 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| −68 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −71 | +1 | −1 | 2 | 7 | 8 = 8 | **4** |
| −79 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −83 | +1 | +1 | 2 | 10 | 10 = 10 | **4** |
| −84 | +1 | +1 | 2 | 10 | 10 = 10 | **4** |
| −87 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |
| −91 | −1 | −1 | 0 | 0 | 0 = 0 | (0) |
| −95 | −1 | +1 | 0 | 0 | 0 = 0 | (0) |

`(0)` marks a value that is zero by the functional equation and was not
summed. Three things hold on all 54 rows: the Hecke identity at level
`11|D|`; the first-layer total equals `(1 − χ_D(11)/α)²·S_D`; and **every
root-number `−1` row has `S_D ≡ 0`** — a linear identity among the Manin
symbols that the functional equation predicts and the eigenline obeys, 27
times. The Euler factor is `(1 − 1/α)² ≡ 5` or `(1 + 1/α)² ≡ 4`, a unit
either way: `α` is not `±1`, so no quadratic twist has an exceptional zero
at 11.

## §4 — the cross-check: one unit per sign

The 27 values `A_D` are recognised as rationals with denominator ≤ 64 to an
error ≤ `2.7·10⁻¹⁵`, and every one is an integer: `4` (22 times), `16`,
`36`, `0` (three times) — the pattern `4·c²` of the Waldspurger–Kohnen–Zagier
formula, noted, not used. Reduced mod 11 and set against the mod-11 sums:

| sign | pairs `(A_D mod 11, S_D)` | unit `λ` with `S_D ≡ λ·A_D` | nonzero pairs |
| --- | --- | ---: | ---: |
| plus | `(4,7)` ×11, `(0,0)` ×2 | **10** | 11 |
| minus | `(4,2)` ×11, `(16 ≡ 5, 8)`, `(36 ≡ 3, 7)`, `(0,0)` | **6** | 13 |

`10·4 = 40 ≡ 7`, `6·4 = 24 ≡ 2`, `6·5 = 30 ≡ 8`, `6·3 = 18 ≡ 7`; the zero
sets `{65, 93}` and `{−47}` agree on both sides. The plus eigenline of
RUN-068 (checked there against the stress-test package's numbers and four
Hecke eigenvalues, and at RUN-071 against Attack 04's 110 summands) is
therefore `10 ×` the reduction of the `Ω⁺`-normalised modular symbol, and
the minus line `6 ×` the reduction of the `Ω⁻`-normalised one, on every
twist tested. A wrong Kronecker symbol, a wrong root-number formula, a wrong
conductor, a wrong unit root or a wrong measure sign breaks one of the
three identities or this correspondence (the drill plants each).

## §5 — the characters whose central value survives

(The central-value criterion. The package's own criterion, `λ_D(0) ≢ 0`, is
evaluated for every even `D` at RUN-077.)

| route | Eisenstein series | symbols | admissible `D`, `|D| ≤ 100` | `A_D` | unusable (root number +1, `L = 0`) |
| --- | --- | --- | --- | --- | --- |
| even | weight 2, `E₂(1, χ_D)` | plus | **5**, 13, 17, 24, 28, 41, 69, 73, 76, 85, 97 | 4 each | 65, 93 |
| odd | weight 1, `E₁(1, χ_D)` | minus | **−3**, −8, −15, −23, −31, −39, −40, −43, −51, −56, −71, −83, −84 | 4 (36 at −43, 16 at −51) | −47 |

For `χ₅`: `χ₅(11) = +1`, Euler factor `(1 − 1/α)² ≡ 5`, first-layer total
`≡ 2` at this scale, and the ten tame branches on the plus line are
`(2, 0, 8, 0, 2, 0, 6, 0, 7, 0)` — every even branch nonzero mod 11, so the
`χ₅`-twisted first layer is nonvanishing at every character it can be
evaluated at, which is exactly what `χ₈` fails. Whether `E₂(1, χ₅)` meets
Loeffler–Rivero's decency and non-criticality hypotheses at 11 is for
whoever applies their theorem to check; the numbers those hypotheses read
(`χ_D(11)`, the Euler factor, the branch values) are in the log for every
`D`.

## The labels

| where | what |
| --- | --- |
| the narration | "額外出現的扭曲 11-adic L 值 … 5 mod 11 … 確實非零" — not a plus-line quantity: there every first-layer value of `χ₈` is 0; identified at RUN-077 as the minus-line value at `x⁻¹` and reproduced |
| the narration | "退化比較引用已發表定理" — Loeffler–Rivero's comparison factor is not reproduced here; this round fixes the arithmetic input any version of it consumes |
| the narration | "C、B₂ 的實際座標及 s₁₁ 仍未算出" — untouched here too |
| this round's output | `BSD_proved: false`; `canonical_frontier_updated: false`; the exact vanishing of `L(E, χ₈ψ, 1)` is a numerical identification of an algebraic number of bounded denominator with 0, backed by the independent mod-11 computation — not a proof |

## The drill

**326 defects, 326 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 69 controls undisturbed, over 104 checks.

The 7 planted for this gate, each turning `attack09-auxiliary` red and nothing else:

| planted defect | went red |
| --- | --- |
| the Kronecker symbol (D/2) is taken as +1 for D = +-3 mod 8 | `attack09-auxiliary` |
| the twisted root number is written chi_D(N) w(E) without chi_D(-1) | `attack09-auxiliary` |
| the Euler factor (1 - chi(11)/alpha) enters to the first power, not squared | `attack09-auxiliary` |
| the level-11D Hecke identity is written with a_11 - chi(11) instead of a_11 - 2 chi(11) | `attack09-auxiliary` |
| the unit root is taken as 4 (a_11 read as +4) | `attack09-auxiliary` |
| the twisted conductor is taken as N |D| instead of N D^2 | `attack09-auxiliary` |
| the measure's second term alpha^-2 [a] is added instead of subtracted | `attack09-auxiliary` |


## What this round does not claim

* **Loeffler–Rivero's degeneration formula is not applied.** The extra
  L-value it produces is whichever twisted value the theorem names; this
  round shows that for `χ₈` at `p = 11` every candidate on the even side of
  the first layer is zero, and lists the characters for which none is.
* **`L(E, χ₈ψ, 1) = 0` is numerical**, to `10⁻¹⁵` against controls of size
  1, plus the mod-11 agreement; the Galois-orbit argument makes it one
  event. It is not a proof, and no rank of `E ⊗ χ₈` over `Q(ζ₁₁)⁺` is
  asserted.
* **`A_D = 4·c²` is an observation** on 27 twists; nothing about Ш or
  half-integral-weight coefficients is claimed.
* **The reading of the narration.** This round took "the extra twisted
  11-adic L-value" to be the central value; the package uses
  `L₁₁(E ⊗ χ₈, x⁻¹)`, which is not. The computations here are about the
  objects they name; the inference "so the auxiliary form must change" was
  about the wrong object and is withdrawn (RUN-077).
* **Nothing about `𝔰₁₁`, `C`, `B₂`, the regulator or `L''(E, 1)`.**
