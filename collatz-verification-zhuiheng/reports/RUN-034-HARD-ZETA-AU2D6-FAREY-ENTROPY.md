# RUN-034 — Hard-Zeta A-U.2d.6: a closed-form count checked against brute-force enumeration, the extra bit of section 6 is really there, and a continued fraction that was right when I expected it to be wrong

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K + Aletheia, `Hard_Zeta_Phase_II_Round_AU2d6_Farey_Order_Entropy_Collision_bundle_v0.1.zip` (source item 52) — 21 numbered results across 19 sections. Ships a checker, its report, a constants frontier, a source-validation record and a stdout transcript.
**Tools:** [`src52_farey_entropy.py`](../code/src52_farey_entropy.py) · [`src52_drill.py`](../code/src52_drill.py) · [`src52_emit_report_block.py`](../code/src52_emit_report_block.py)
**Logs:** [`src52-au2d6.json`](../data/gate-logs/src52-au2d6.json) · [`src52-drill.json`](../data/gate-logs/src52-drill.json)

**Result: the decidable core holds, and one part of it is the most decisive check anywhere in this sweep — a closed-form count against brute-force enumeration, which needs no tolerance and no sampling. §5's rational-Catalan capacity agrees with enumeration on 34 coprime pairs up to 3,876 members. §3's binary bridge and concatenation law are exact. §6's extra bit is real, verified in both directions. Two findings, neither mathematical. Four of the checker's nine claims are independently confirmed and the other five are named rather than implied.**

---

## The check that needs nothing

Most of this sweep compares one computation against another and has to argue that
the reference is better. §5 does not need that argument. It gives a closed form

> `#W_{p,g} = binom(p−1, g−1)/g = binom(p, g)/p`   for `gcd(p,g) = 1`

for a set that can simply be **enumerated**: positive compositions of `p` into `g`
parts with `P_j ≤ jp/g`. Enumeration against formula is decidable, needs no
tolerance, and cannot be fooled by a shared bug in a shared method.

**34 coprime pairs with `p/g < β`, up to `(20,13)` with 3,876 members. Zero
disagreements**, and the two closed forms agree with each other on every pair.
All five of the shipped report's own capacity examples recompute, including the
129-digit one at `(485, 306)`.

## The extra bit of section 6, checked in both directions

Item 51 proved a repeated code forces `|x−x′| ≥ 2^{p+1}`. Section 6 sharpens that
to `2^{p+2}` by using the fact — item 51's own §6 — that both lower-wing endpoints
are B anchors and hence `3 (mod 4)`.

One extra bit is exactly the sort of claim that is either right or off by a factor
of two, so it is checked the way RUN-033 established: **376** codes with a
`3 (mod 4)` destination, class violations **0**; and **1,128** members drawn from
the claimed class *at which the code was never observed*, each required to realize
the same code **and** land on a `3 (mod 4)` destination — **0** failures. Without
that second half the check passes on a class twice too large, which is precisely
the size of the claim.

The result it rests on was re-verified rather than assumed: **12,419** real
sources with `L ≥ 2`, **0** not `≡ 3 (mod 4)`.

## Finding 1 — two names, one file, for the third bundle — and this time not byte-identical

`checker_stdout.txt` is the checker report **plus a single trailing newline** and
nothing else. Items 50 and 51 shipped the two byte-identical; here one byte
separates them — enough for a byte comparison to say they differ, not enough to
make them different documents.

Worth stating precisely rather than either dropping the observation or letting the
streak language carry it. The bundle still ships the same content twice under two
names, and its own validation record lists both.

## Finding 2 — the artifacts have stayed corrected

The three inherited exponents are the **exact** nearest doubles of their
rationals. Item 51's were too; item 50's were 1 and 2 ulps out, measured at
RUN-032. Two bundles running is not yet a habit, but it is no longer a one-off,
and reporting an improvement is the same obligation as reporting a defect.

## The continued fraction I expected to be wrong

The checker publishes 30 partial quotients of `β` and of `θ`. The `β` list's first
sixteen are **exactly** the terms RUN-029 certified by integer comparison alone —
a pleasing closure, since that certification evaluated no logarithm.

The `θ` list evaluates to `0.5849625…`, not to `1/β = 0.6309…`, and looked one
term short of `[0] + β`'s expansion. That had the shape of a real finding.

It is not one. **The round defines `θ = β − 1` at §9**, so its expansion must be
`[0] + β_cf[1:]` — which is exactly what is published. The check now asserts that
relation, plus `θ + 1 = β` on the published expansions, plus `θ ≠ 1/β`.

Third time this session that reading the source overturned a candidate finding
before it was published. It is also the reason D15 exists: the drill replants the
wrong expectation so it cannot come back quietly.

---

<!-- BEGIN GENERATED measured block: python code/src52_emit_report_block.py -->

**The capacity count, formula against enumeration.** A sample of the coprime pairs enumerated exhaustively:

| `p` | `g` | enumerated | `binom(p,g)/p` |
| --- | --- | --- | --- |
| `3` | `2` | `1` | `1` |
| `4` | `3` | `1` | `1` |
| `5` | `4` | `1` | `1` |
| `6` | `5` | `1` | `1` |
| `7` | `5` | `3` | `3` |
| `7` | `6` | `1` | `1` |
| `8` | `7` | `1` | `1` |
| `9` | `7` | `4` | `4` |

| what | measured against | value |
| --- | --- | --- |
| coprime pairs enumerated exhaustively | largest `[20, 13]`, with `3876` members | `34` |
| …**enumeration disagreeing with the closed form** | must be zero | `0` |
| …the two closed forms disagreeing with each other | `binom(p−1,g−1)/g` against `binom(p,g)/p` | `0` |
| shipped capacity examples recomputed | 0 disagreements, including the 129-digit one | `5` |
| **§3** binary-bridge violations `C(d(w)) = B_w` | exact integers, 800 random codes | `0` |
| …normalized-correction violations | `c(w) = (1/3)Σ2^(P_j)/3^j` as exact Fractions | `0` |
| …concatenation violations on `B` / on `c` | must be zero | `0 / 0` |
| **§6** codes with a `3 (mod 4)` destination | the theorem's own hypothesis | `376` |
| …class violations mod `2^(p+2)` | forward direction | `0` |
| …**class members failing the code or the residue** | the reverse direction, 1128 members drawn from the class itself | `0` |
| …source gaps below `2^(p+2)` / destination gaps not `4·3^g` | 376 repeated-code pairs | `0 / 0` |
| …pairs where the modulus is exactly twice item 51's | the extra bit, counted | `376` |
| **item 51 carryover** real sources with `L ≥ 2` | re-verified, not assumed | `12419` |
| …**not `≡ 3 (mod 4)`** | must be zero | `0` |
| published `β` partial quotients | of which the first 16 match the terms RUN-029 certified by integer comparison: `True` | `30` |
| `θ` expansion equals `[0] + β`'s shifted | which is what `θ = β − 1` requires; and `θ ≠ 1/β` is `True` | `True` |
| inherited exponents off the exact rational's nearest double | of 3 checked | `0` |
| validation-record files verified | shape: list of file records (items 51, 52); uncovered: 1 | `8` |
| the checker's stated claims independently confirmed | of 9; 5 named as not covered here | `4` |
| defects planted / caught by the check named for each | 1 robustness property; 0 malformed; first-pass | `19 / 19` |

**The two transcripts.** `checker_stdout.txt` is byte-identical to the checker report: `False`. It is the report plus `'\n'`.

**Not covered here**, named rather than implied: *unit Farey first-passage prefix domination by rational Christoffel positions*; *Christoffel correction maximum and Gamma >= M/24, strict for M>0, on every enumerated unit code*; *origin-span correction decomposition and additive Christoffel replacement deficit*; *local continued-fraction lower bound ||q beta|| > 1/((M_L+2)q) on tested ranges*; *non-unit determinant dichotomy Xi>=2 => A>=1/H or E>=1/g*.

Every figure above is emitted by `code/src52_emit_report_block.py` from the gate logs. None is typed into this file.

<!-- END GENERATED measured block -->

---

## The instrument

**Drill 19/19 by the check named for each, both controls clean, no malformed
mutations — and the first drill in this sweep to pass on its first attempt.**
Every earlier item needed at least one defect re-aimed after the pre-flight named
it; this one did not, which is what six items of accumulated habits are supposed
to buy.

One guard did fire on the first gate run, and it was mine: the capacity
enumeration window stopped at `g = 8`, capping the largest enumerated class at
**30** — too small to separate `binom(p,g)/p` from anything else it might have
been. The `largest_count < 100` guard caught it. A formula-versus-enumeration
check is only as sharp as the largest case it reaches.

## What the checker claims and this run did not check

The shipped report states **nine** verified claims. **Four** are independently
confirmed here — the bridge, the concatenation law, the capacity count, and the
B-to-B class and separation. The other **five** are named in the log rather than
waved at: the Farey prefix domination, the Christoffel deficit `Γ ≥ M/24`, the
origin-span decomposition, the local continued-fraction lower bound, and the
non-unit determinant dichotomy. They are not disputed; they are unchecked, and a
count of four is the honest one.

The checker also publishes its own `not_verified` list — a divergent orbit, global
boundedness of `log₂3`'s partial quotients, inherited density claims, and a full
contradiction. That list is intact and correct.

## Route map

`ROUTE_MAP v2.6`. Item 53 is `A-U.2d.7 — Plateau-Reset Quantization Rigidity`,
which this bundle's constants frontier names as the next round.

## What this run does not claim

1. That the Farey-Order Entropy Collision theorem (§8) holds. It quantifies over
   nested B-configurations; only its arithmetic inputs were checked.
2. That the square-root depth cap (§9) or the non-unit caps (§10) hold. Not
   checked, and both rest on the local continued-fraction bound that is also not
   checked here.
3. That the five uncovered checker claims are true or false.
4. That the capacity formula holds beyond the enumerated window. Thirty-four
   pairs up to `(20,13)` were verified exhaustively; the closed form is a theorem
   and this run tested it, it did not prove it.
5. That the shipped checker is correct. It was read, never run.
