# RUN-002 — the ladder has eleven rungs, and every summary of it has six

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Phase 0 doc 03, *BSD Certificate Ladder* — the object the other three sub-lines reason with
**Tools:** [`src01_ladder_vocabulary.py`](../code/src01_ladder_vocabulary.py)
**Logs:** [`src01-ladder-vocabulary.json`](../data/gate-logs/src01-ladder-vocabulary.json)

**Result: no document in the corpus uses a rung the framework does not define — the vocabulary is clean where it is used. But the framework defines eleven rungs and all three places that summarise it render six, dropping the same five every time, including the pair that separates numerical evidence from rigorous proof. One of the three was this arm's own README, written earlier the same day.**

---

## The framework's object

Doc 03 opens with the reason the ladder exists:

> 每一條曲線都不能只存一個布林值：`BSD true / false`
> 而要存「哪一層已被什麼證書關閉」。

It then defines eleven rungs. Two of them carry the distinction the rest of the
document is built around:

| rung | | |
| --- | --- | --- |
| **C2** | Numerical analytic rank | high-precision computation gives `r_an = r`, "但未必有 rigorous zero-order certificate". Status: **`evidence`** |
| **C3** | Rigorous analytic rank | an auditable L-function algorithm, interval arithmetic, a Turing-type count, or a theorem |

And the document's own **絕對禁止** list, item 2, forbids the collapse between
them in as many words: *「`rank()` 回傳一個整數就當成有完整 proof」*.

## What was measured

Every rung named in each of the 85 curated documents, against the eleven the
framework defines. Then the same question of the three places that summarise
the ladder for a reader.

| | |
| --- | ---: |
| rungs defined by the framework | **11** |
| documents naming at least one rung | 4 |
| **documents using a rung the framework does not define** | **0** |
| rungs never used outside the framework | 0 |

Each rung is named in three or four documents. That is coverage, not a finding:
the corpus reasons in its own sub-line vocabulary and reaches for the ladder at
the joins.

## The finding

| where | rungs named | dropped |
| --- | --- | --- |
| `agent/bsd` tree README | C0, C6, C7, C8, C9, C10 | **C1–C5** |
| the public BSD page | C0, C6, C7, C8, C9, C10 | **C1–C5** |
| this arm's README, as first written | C0, C6, C7, C8, C9, C10 | **C1–C5** |

Three independent renderings, identical abbreviation, the same five rungs gone.

An abbreviation is not a defect. Showing a ladder's arc — identity, weak, strong,
family — is a reasonable thing for a summary to do, and the public page's prose
is careful elsewhere: it says P5's core comparison is still OPEN rather than
rounding it up.

What makes this worth a round is *which* five vanish. C1–C5 are not decoration
between C0 and C6; they are the rungs where the ladder does its actual
discriminating, and **C2/C3 is the one boundary the framework explicitly forbids
crossing**. A reader who meets the ladder only as `C0 → C6 → …` has been shown a
ladder that does not distinguish a number a computation produced from a number a
proof produced — in a framework whose first sentence is that a curve must not
store a bare boolean.

## Where this arm sits in its own finding

The third row is mine. This tree's README carried the six-rung chain within an
hour of the line opening, copied from the archive README — a derived summary —
without opening doc 03. That happened on the same day this arm published a
report whose subject was a claim taken from a derived source instead of the
original.

Corrected: the README now carries all eleven, with C2 and C3 spelled out and the
reason attached. The gate that measured it now reads this file too, so the
correction is checked rather than asserted.

## Two defects in this gate, both caught before its output was used

* **It hung rather than failing.** `git cat-file --batch` was handed a `str`
  through a binary pipe (`text=False`). That does not raise; it stalls, past two
  minutes. Encoded, and noted in the code — a gate that hangs produces no verdict
  either.
* **A filter aimed at noise removed the signal.** The rung scanner stripped
  fenced code blocks first, to avoid matching a stray `C1` inside a JSON sample.
  But **every abbreviated ladder in this corpus is written inside a code fence** —
  so the gate reported this arm's own README as naming *no rungs at all*, and
  reported the archive README unreadable because it lives on another branch and
  was being opened by path.

The second is the more instructive: the exclusion was defensible in the
abstract, and it deleted exactly the thing the gate existed to find. Both were
caught by reading the output against a fact already known — that the README
*did* contain a ladder — rather than by any check.

## What this round does not claim

* **Nothing about BSD**, and nothing about whether any curve reaches any rung.
* **No document misuses the ladder.** Zero documents name an undefined rung, and
  no contradiction between a rung's use and its definition was found.
* **It does not claim the abbreviation misled anyone.** It measures that three
  renderings agree with each other and disagree with the source, and states why
  those particular five rungs are the ones worth not losing.
