# RUN-056 — Three rules, three commits, one frozen blob: the mechanism behind RUN-055's provenance finding, read from the diffs and tested on the data

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`02_Paper_vs_Current_Code_Audit`](../../../amral/public/bsd/phase1/files/02_Paper_vs_Current_Code_Audit.md) — the audit that opens with 「目前 GitHub 實作不是單純照抄 paper pseudocode」
**Tools:** [`src58_paper_vs_code_provenance.py`](../code/src58_paper_vs_code_provenance.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src58-paper-vs-code-provenance.json`](../data/gate-logs/src58-paper-vs-code-provenance.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)
**Data:** the census package's own `sources/*.diff`, `sources/PROVENANCE.md`, `logs/run.log`

**Result: RUN-055 measured that the upstream twist blob is missing exactly the 1,355 isogeny curves and contains all 2,707 `a₃` curves, without knowing why. The package archives the upstream diffs, and they say why. **Algorithm 1's isogeny condition changed three times across the three pinned commits**: at `7286794`, which generated the blob, it reads `set(bad_primes) and set([3,5,7])` — and Python's `and` returns its second operand whenever the first is truthy, so on every curve of conductor `> 1` that is **unconditionally `{3,5,7}`**, whatever was meant. At `1a0489c`, the OLD base, it became **conditional**: `A := {3 if 3∣N or |a₃|=3} ∪ {5 if 5∣N} ∪ {7 if 7∣N}` — strictly weaker. At `31fae20`, CURRENT, it is unconditional again **plus a separate `a₃ ≠ ±3` filter**. Strict → relaxed → strict + `a₃`, with the blob frozen at the first stage. **That predicts something testable**: if the OLD base came from the relaxed rule, every one of its 1,355 isogeny curves must escape that rule's trigger. **1,355 of 1,355 do**, and the strict rule removes all 1,355. All three artefacts — blob keys, OLD base, CURRENT base — match the rule that made them. Separately, `02` §6's five pins for a reproduction: **1 present, 1 partial, 1 absent, 2 not applicable** by the package's own scope, which states in as many words that no Sage replay happened. §7's four rank fields: **0 of 4** in the base record — and Theorem 2.18 is stated for analytic rank 0.**

---

## `02`'s opening line, made exact

> 目前 GitHub 實作不是單純照抄 paper pseudocode。

`02` says the implementation drifted from the paper. The package archives three
snapshots of the implementation, and this round reads what drifted.

| commit | role | isogeny condition in `filter_CONDITION_p_isogeny` |
| --- | --- | --- |
| `7286794` | generated the OLD twist blob | `non_isogeny_primes = set(bad_primes) and set([3,5,7])` |
| `1a0489c` | OLD — the 40,749 base | `A := {3 if 3∣N or |a₃|=3} ∪ {5 if 5∣N} ∪ {7 if 7∣N}` |
| `31fae20` | CURRENT — the 36,687 base | every `p ∈ {3,5,7}`, no rational `p`-isogeny; **and** `filter_CONDITION_a3: a₃ ≠ ±3` |

Each line is located in the archived diff as an added or removed line — the
gate checks the text is there, not a paraphrase of it.

### What `and` does

```python
set([2, 7]) and set([3, 5, 7])   # -> {3, 5, 7}
set()       and set([3, 5, 7])   # -> set()
```

`x and y` is `y` when `x` is truthy, and a non-empty set is truthy. Every base
curve has a non-empty bad-prime set (0 of 40,749 are empty), so at `7286794` the
expression was `{3, 5, 7}` on every curve. **`&` would have given
`bad_primes ∩ {3,5,7}`** — which is the *shape* of the OLD rule. Which was
intended is not measurable here. What it evaluates to is.

## The prediction, and the test

If the OLD base was produced by the relaxed rule, then an isogeny curve survives
only when its isogeny sits at a prime the rule does not inspect:

* a 3-isogeny, with `3 ∤ N` **and** `|a₃| ≠ 3`;
* a 5-isogeny, with `5 ∤ N`;
* a 7-isogeny, with `7 ∤ N`.

**One counterexample and the account is wrong.** Applied to all 1,355:

| | |
| --- | ---: |
| isogeny curves in the removed census | 1,355 |
| of which in the OLD base | **1,355** |
| that the relaxed rule would have removed | **0** |
| that the strict rule removes | **1,355** |

The prediction holds without exception.

## Three artefacts, three rules

| artefact | curves | rule | matches |
| --- | ---: | --- | --- |
| twist blob keys (`7286794`) | 39,394 | strict `{3,5,7}`, no `a₃` | = base minus the isogeny set ✔ |
| OLD base (`1a0489c`) | 40,749 | relaxed `A`-set | contains all 1,355 isogeny curves and all 2,709 `a₃` curves ✔ |
| CURRENT base (`31fae20`) | 36,687 | strict + `a₃` | = OLD minus (isogeny ∪ `a₃`), 4,062 removed ✔ |

This is the mechanism behind `PROVENANCE.md`'s sentence — *OLD base and OLD
`Algorithm2.py` changed after the OLD twist JSON's last-change commit, while the
JSON blob stayed identical* — with the change named. The package said the blob
was stale and refused to synthesise the missing keys; it did not say what rule
the blob obeyed. Now it is measured: the strict one.

**And the map's E2 + E3 as stated in `01` correspond to CURRENT.** The
40,749-curve "OLD base" this line has worked with since RUN-004 is the output of
an intermediate rule that neither the paper's Theorem 2.18 nor the blob's
generator used.

## `02` §6: the five pins, against the package's stated scope

`02` §6 says a reproduction must lock: paper version, repository commit / file
SHA, Sage version, LMFDB release, runtime flags.

| pin | state | evidence |
| --- | --- | --- |
| paper version | **ABSENT** | no arXiv id or version string anywhere in the package |
| repository commit / file SHA | **PRESENT** — *corrected at RUN-062: the ecdata per-shard SHA-256s reproduce only after CRLF conversion; the package hashed a Windows checkout, not the git blob* | three commits, four blob SHA-1s, ecdata commit `25cec5e`, per-shard SHA-256 |
| Sage version | **N/A by scope** | `PROVENANCE.md`: a Sage/LMFDB replay "is intentionally not represented as completed here" — no Sage ran |
| LMFDB release | **PARTIAL** | no release pinned; the ecdata commit is pinned, and ecdata is LMFDB's upstream for these tables |
| runtime flags | **N/A by scope** | `skip_filter_S` / `skip_BSD_at_2_check` appear only in the archived upstream source, never as recorded values — no Algorithm 2 run happened |

The package calls itself an *exact artefact census* and says explicitly what it
is not. `02`'s pins are for a reproduction. Scoring the N/A rows as failures
would be holding the package to a claim it declined to make — the same
discipline RUN-054 applied to `05`.

The absent one is real. **No document in the package names which version of the
paper Theorem 2.18 is Theorem 2.18 in.**

## `02` §5 and §7

| | demanded | in the package |
| --- | --- | --- |
| §5 soundness flags recorded as metadata values | `skip_filter_S`, `skip_BSD_at_2_check` | **no** — only in source |
| §7 rank fields kept distinct | algebraic rank, analytic rank, special-value nonvanishing, proof/evidence type | **0 of 4** in the base record |

§7 is the one to keep. `02` warns against silently merging algebraic and analytic
rank into one column. The base record has *no* rank column at all: the census
carries `ainvs`, conductor, primes, discriminant, valuations, labels, source —
and Theorem 2.18 is stated for **analytic rank 0**. Every curve in the base is
rank 0 by construction of the paper's list, and that fact lives nowhere in this
package's data. It is E6, cited, as RUN-055 recorded.

## The drill

**233 defects, 233 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 45 controls undisturbed, over 84 checks.

The 5 planted for this gate, each turning `paper-vs-code` red and nothing else:

| planted defect | went red |
| --- | --- |
| the relaxed rule is applied as if it were the strict one | `paper-vs-code` |
| the `and` expression is reported as evaluating to the intersection | `paper-vs-code` |
| the generator-to-old diff is missing from the package | `paper-vs-code` |
| 02's paper-version pin is scored PRESENT | `paper-vs-code` |
| a rank column is reported in the base record | `paper-vs-code` |


## What this round does not claim

* **Nothing about intent.** `and` versus `&` is reported as what Python
  evaluates, not as a bug or a choice.
* **The three rules are read from the archived diffs**, which the package
  extracted with `git cat-file blob`. This round trusts that extraction; it did
  not fetch the upstream repository.
* **The prediction test is about which rule produced the OLD base.** It says
  nothing about whether the relaxed rule was mathematically adequate.
* **N/A by scope is the package's scope, not this arm's judgement** of what a
  census ought to include.
* **`02` §1–§4 (2-descent, `E'` hardening, the descent backend, Proposition
  2.16's deterministic criterion) are not examined.** They concern Algorithm 2's
  certificate machinery, which this tree does not run.
