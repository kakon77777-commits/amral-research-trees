# RUN-001 — the corpus, and the one document the site's own claim does not cover

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** the BSD corpus as published at [amral.evemisslab.com/bsd/](https://amral.evemisslab.com/bsd/), against the research packages archived on `agent/bsd`
**Tools:** [`src00_corpus_identity.py`](../code/src00_corpus_identity.py)
**Logs:** [`src00-corpus-identity.json`](../data/gate-logs/src00-corpus-identity.json)

**Result: 84 of the 85 curated documents are byte-identical to their archived original, which is what the site claims. The 85th is not. Seven of its eight changed lines are full-width to half-width punctuation; the eighth translated an English technical word into Chinese, inside a rules document whose whole subject is that a backend must not be allowed to substitute a weaker thing for the thing named.**

---

## Why this is round one and not a preliminary

The site's BSD page closes with a claim about itself:

> SHA-256 逐篇核驗 · 原始位元組，不重新打包
> *(per-document SHA-256 verification · original bytes, not repackaged)*

Every later round of this sweep will read a curated document and reason about it
as though it were the archived original. If that is not true, every later round
inherits the gap silently. So it is checked first, and it is checked in the only
way that can settle it: **by content hash, never by filename.**

Filename matching would have been wrong in both directions here. The curated
copies carry ordering prefixes the originals do not — `29_Theorem_Note_v1.0.md`
is `BSD_696e1_Theorem_Note_v1.0_2026-08-13/…` — so a name comparison reports four
renames as mismatches. Worse in the other direction: `README.md` occurs in
sixteen packages, and matching on it would pair documents that share nothing but
a name.

## What was compared

| side | what | count |
| --- | --- | ---: |
| curated | `amral/public/bsd/{phase0,p5,phase1,phase2}/files/*.md` | **85** |
| archived | `agent/bsd`, every `.md` inside the 25 mirrored packages | **292** |

| | |
| --- | ---: |
| byte-identical to an archived original | **84** |
| of those, renamed on the way in | 4 |
| **curated with no byte-identical original** | **1** |
| archived but not curated | 201 |

The 201 are not a finding. The site presents a selected reading path; the
packages also carry READMEs, handoffs, checksum manifests and intermediate
notes. Only the other direction is a claim about fidelity.

| sub-line | curated | witnessed |
| --- | ---: | ---: |
| Phase 0 | 10 | 10 |
| P5 | 10 | 10 |
| Phase 1 | 25 | 25 |
| **Phase 2** | 40 | **39** |

## The finding

`phase2/files/07_Local_Agent_Implementation_Spec.md` — 1,917 bytes curated,
1,935 archived. Its original **does** exist, at the same filename:
`BSD_FW_H2_Local_Isogeny_Compiler_v0.3_2026-08-13/docs/07_Local_Agent_Implementation_Spec.md`.
It is not a missing document. It is a modified one.

Eight lines differ. **Seven are punctuation only** — full-width `：` and `，`
normalised to `:` and `,`. Cosmetic, and a byte change all the same.

The eighth is not punctuation:

```
archived:  優先使用 Sage/Magma 已有的 certified local isogeny / local factorization machinery。
curated :  優先使用 Sage/Magma 已有的 certified local isogeny / local factorization機械。
```

An English technical term was rendered into Chinese, and the space before it
closed up. In this sentence *machinery* means the certified apparatus a computer
algebra system already provides; 機械 in Chinese carries the sense of a physical
mechanical device. The reading shifts.

**Why it lands where it does.** This document is the FW-H2 local agent's rules
sheet, and its four rules are, in substance, one rule: *a backend must not
substitute a weaker thing for the thing named.* Rule 2 forbids treating "a local
p-isogeny exists" as an H2 verdict when no kernel character evidence is produced.
Rule 3 requires an exact p-adic factorization or a Hensel certificate, not an
approximation. Rule 4 forbids promoting a heuristic certificate to `PASS`. The
document's own closing block lists four inferences as **禁止 shortcut**.

A silent substitution in the sentence naming what the backend must use is the
same shape as what the document forbids, one level up.

## What this round does not claim

* **It does not claim the mathematics is affected.** One word in a rules
  document is not a defect in Phase 2's family construction, and nothing here
  reaches the 696.e1 result.
* **It does not claim the change was careless.** Normalising punctuation for a
  web page is an ordinary editorial act. The finding is that the page states it
  did not do that.
* **It does not certify the other 84 beyond byte-identity.** A document
  identical to its archive is a faithful copy of what was written; whether what
  was written is correct is what rounds 2 through 85 are for.
* **It says nothing about BSD.** No round of this sweep will.

## What this establishes for the sweep

The corpus is settled, and it is bigger than the site: **292 archived `.md` plus
scripts, input data, results and `SHA256SUMS.json` inside 25 packages**, against
85 curated documents. Where a later round needs to recompute rather than read,
the executable material is on `agent/bsd`, not on the site.

One thing the earlier reconnaissance got wrong and this gate corrected: comparing
*25 packages* against *85 documents* looked like a month-stale archive missing
53 documents. They are different units. The archive is ahead of the site, not
behind it, and the site's 2026-08-18 date is a curation date.
