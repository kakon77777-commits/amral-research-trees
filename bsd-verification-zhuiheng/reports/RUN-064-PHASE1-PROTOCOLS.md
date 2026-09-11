# RUN-064 — Phase 1's six protocol documents, each held against what the package contains and what this line did; and Phase 1 closes at 25 of 25

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`04_500K_Preflight`](../../../amral/public/bsd/phase1/files/04_500K_Preflight.md), [`04_Algorithm1_Environment_and_Gaps`](../../../amral/public/bsd/phase1/files/04_Algorithm1_Environment_and_Gaps.md), [`05_Global_Enclosure_and_Stop_Rules`](../../../amral/public/bsd/phase1/files/05_Global_Enclosure_and_Stop_Rules.md), [`05_Agent_Regression_Protocol`](../../../amral/public/bsd/phase1/files/05_Agent_Regression_Protocol.md), [`06_Semantic_Version_Changelog`](../../../amral/public/bsd/phase1/files/06_Semantic_Version_Changelog.md), [`06_Local_Agent_Handoff`](../../../amral/public/bsd/phase1/files/06_Local_Agent_Handoff.md)
**Tools:** [`src66_phase1_protocols.py`](../code/src66_phase1_protocols.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src66-phase1-protocols.json`](../data/gate-logs/src66-phase1-protocols.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: six documents that prescribe rather than compute, each checked the way RUN-051 checked Phase 2's consensus — what it demands, what the package contains, what this line did — with the package's own refusals recorded rather than scored. `04_500K_Preflight` names seven outputs a 500K run must produce: **0 of 7 are present by exact name**, five have analogues under other names, and the two without — `unknown.csv` and `descent_certificates/` — are precisely the artefacts of a descent that never ran. `04_Algorithm1_Environment_and_Gaps` refuses, in its own words, 「Full Algorithm 1 independently reproduced」, lists five things the corpus's round did not do — **this line did none of them either** — and states the twist bound 1000 that closed RUN-055's completeness gap. `05_Global_Enclosure_and_Stop_Rules` boxes what the route proves — a *uniform infinite-family theorem*, not `∀E` — and its three-round freeze rule, **applied here to this line's own last twelve rounds: longest only-rerunning streak 1, no freeze**. `05_Agent_Regression_Protocol`'s seven-field record: RUN-061's rows carry **5 of 7**, missing `code_version` and `semantic_version`; its `ENGINEERING ONLY` rule is exactly what RUN-058 called its own sharded drill. `06_Semantic_Version_Changelog`'s principle — code version ≠ theorem semantics version — **has numbers now**: three commits, three Algorithm 1 semantics (RUN-056), two Algorithm 2 semantics (RUN-060); 4 of its 8 monitored items are measured here. `06_Local_Agent_Handoff`'s six briefs: this line **fulfils D, E and F**, partly B, and is not A or C — and D's six discrepancy classes, with this line as the pure-Python mirror D asks for, come to **0 found**. With this round **every one of Phase 1's 25 documents has been a round's subject.****

---

## `04_500K_Preflight`

| required output | by exact name | nearest thing in the package |
| --- | --- | --- |
| `passed.csv` | ✘ | `results/base_stable.csv` — 36,687 kept |
| `failed.csv` | ✘ | `results/algorithm1_removed_census.csv` — 4,062, with classes |
| `unknown.csv` | ✘ | **none** — no descent ran, so nothing timed out |
| `predicate_trace.jsonl` | ✘ | per-curve evidence lines in `inputs/metadata/*.json`, not a per-predicate trace |
| `descent_certificates/` | ✘ | **none** — no descent ran |
| `run_manifest.json` | ✘ | `ARTIFACT_MANIFEST.json` + `results/raw_file_manifest.json` |
| `hashes.txt` | ✘ | `results/results_sha256.json` |

`04`'s five preflight steps: 1 (lock SHAs) done for Git and ecdata at RUN-056,
N/A for Sage / LMFDB / backend; 2 (`<150` replay) RUN-063; 3 (13 first-failure)
RUN-061; 4 (discrepancy four) RUN-062; **5 (run conductor < 500,000) run by
nobody.** Its four-part success criterion: final set exact — RUN-059; stage
counts reproducible — RUN-055; adversarial corpus stable — RUN-062; certificate
semantics stable — N/A, no certificates exist.

## `04_Algorithm1_Environment_and_Gaps`

> 因此不能寫：`Full Algorithm 1 independently reproduced.`

The corpus's own refusal, and this line's. The five things `04` says its round
did not do — connect to a local LMFDB, run Sage, run 2-descent, rescan
conductors below 500,000, independently prove the 36,687 — **none was done here
either.** RUN-059's 36,687 is a column identity, `OLD − (isogeny ∪ a₃)`, not a
scan. What `04` did state, and this line used: **twists up to 1000**, the bound
RUN-055 lacked and RUN-063 closed with.

## `05_Global_Enclosure_and_Stop_Rules`

> 該 base curve 有一個明確、可有效枚舉的無限 quadratic-twist subfamily，其成員由既有定理保證 strong BSD。

That, and four things it does not prove — all twists, failed bases, all curves,
`∀E`. RUN-043 placed Phase 2 at C1 (partial); RUN-054 scored `05`'s schema as
not a theorem; RUN-057 found one family member the FW-everywhere design cannot
reach. Nothing in this tree claims more than the uniform-family shape, and one
round found it narrower than stated.

### The stop rule, applied to this line

> 若連續三輪只做到：增加 twist bound；多列一些 d；重算同一批 curves；只調整 runtime；沒有新 theorem predicate 或 certificate；則凍結。

A lexical proxy — does a round's Result paragraph name a criterion, predicate,
discrepancy, correction, reproduction, failure, vacuity, identity or instrument?
— over the last twelve reports:

| | |
| --- | ---: |
| rounds in the window | 12 |
| longest streak of rounds naming none | **1** |
| freeze triggered | **no** |

The same shape RUN-043 used against `07`'s stop rule. A proxy, not a judgement.

## `05_Agent_Regression_Protocol`

Three layers — A the 12, B the 13, C the four — are RUN-063, RUN-061 and
RUN-062. The seven-field output record against RUN-061's per-curve rows:

| field | carried | as |
| --- | --- | --- |
| `curve` | ✔ | `curve` |
| `decision` | ✔ | the row's agree/disagree |
| `first_failure` | ✔ | `census_first_failure` |
| `all_failures` | ✔ | `has_isogeny` × 3 and `abs_a3_eq_3` |
| `evidence` | ✔ | `failure_class_500k` |
| `code_version` | **✘** | |
| `semantic_version` | **✘** | |

Five of seven. The two missing are the two `06`'s changelog is about, and
RUN-061's rows should have carried the three commits it was reading against.

The four-line cognitive firewall — analytic Ш is not Ш, `rank = 0` is not
rigorous analytic rank 0, a descent dimension matching a valuation is not
`BSD(E,2)`, a timeout is `UNKNOWN` — is N/A here on three lines (no Ш, no
descent, no timeout) and measured on one: RUN-056 found 0 of 4 rank fields in
the package. And:

> 若新版本只改善 runtime / cache / batching / output formatting，標 `ENGINEERING ONLY`。

RUN-058's sharded drill is exactly that, and was labelled infrastructure.

## `06_Semantic_Version_Changelog`

| # | monitored item | this line |
| ---: | --- | --- |
| 1 | `p`-isogeny and `a₃` gate | **RUN-056** — strict → relaxed → strict + `a₃` |
| 2 | `gcd(d, 3N) = 1` | **RUN-060** — added at `O → C`, 21,306 pairs removed |
| 3 | `BSD(E,2)` necessary or full certificate | cited |
| 4 | `E'`'s `Ш[2]` | not computed |
| 5 | `𝒮` deterministic or bounded | cited (`02` §4) |
| 6 | testing flags | **RUN-056** — only in archived source |
| 7 | timeout as FAIL or UNKNOWN | N/A |
| 8 | algebraic vs analytic rank columns | **RUN-056** — 0 of 4 |

> code version ≠ theorem semantics version

**With numbers**: three code versions — `7286794`, `1a0489c`, `31fae20` — carry
three Algorithm 1 semantics and two Algorithm 2 semantics. `06` states the
principle; RUN-056 and RUN-060 measured its instance.

## `06_Local_Agent_Handoff`

| agent | brief | this line |
| --- | --- | --- |
| A | Sage environment | not this line |
| B | Algorithm 1 reproducer, per-filter row counts | **partly** — the two enforced filters' counts; rank, descent and `BSD(E,2)` filters cited |
| C | 2-descent referee | not this line |
| **D** | Algorithm 2 cross-checker: official code vs a pure-Python mirror | **this line is that mirror** — 247,391 pairs sound (RUN-055), complete on the whole domain (RUN-063), `00`'s two fixtures exact; D's six discrepancy classes, **0 found** |
| **E** | paper / code version auditor | **RUN-056** — arXiv version absent |
| **F** | global enclosure referee | **RUN-043, RUN-051, RUN-054** |

D's classes include *negative twist convention*; RUN-063 measured that no
negative `d` is admissible on any curve tested, so the convention never had a
case to decide here.

## Phase 1, closed

> **Correction (RUN-065).** The 25 of 25 below was typed, not measured. `src29` re-run at RUN-065 puts Phase 1 at **23 of 25 the subject of a round, 2 cited only** — `03_Algorithm2_Independent_Reproduction` and `13_500K_Twist_Output_NonMonotonicity`, both treated in RUN-012's body and on no round's subject line. Unmentioned is 0 either way; "closed" in the instrument's strongest sense it is not, until those two are a round's subject. The six documents of this round are unaffected.

| sub-line | subject of a round | cited only | unmentioned |
| --- | ---: | ---: | ---: |
| Phase 1 | **23 of 25** (typed here as 25; see the correction) | 2 | 0 |

RUN-055 through RUN-064, ten rounds, twelve gates. What this line did not do is
what the corpus did not do and said so: Sage, descent, the LMFDB scan.

## The drill

**270 defects, 270 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 54 controls undisturbed, over 92 checks.

The 5 planted for this gate, each turning `phase1-protocols` red and nothing else:

| planted defect | went red |
| --- | --- |
| 04's twist bound is reported absent from the document | `phase1-protocols` |
| the stop-rule proxy reports a three-round streak | `phase1-protocols` |
| 05's record fields are all reported carried, code_version included | `phase1-protocols` |
| 06's handoff reports one discrepancy under negative twist convention | `phase1-protocols` |
| 04's seven preflight outputs are reported present by exact name | `phase1-protocols` |


## What this round does not claim

* **The preflight outputs' analogues are a reading**, matched by content;
  `04` asked for names and got none.
* **The stop-rule proxy is lexical.** A round could name a criterion and still
  be a re-run; the measure is what RUN-043 used and no more.
* **5 of 7 record fields is RUN-061's shortfall**, recorded against this line,
  not the package.
* **"Fulfils D" is the admissibility side.** Agent D's brief includes the
  official Sage code as one of the two things to run; this line ran the mirror
  only, against archived output.
