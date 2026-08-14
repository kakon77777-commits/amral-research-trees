# RUN-003 — The draft chain, and what the repair repaired

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** Neo.K, `Collatz_OT_Series_Paper_01_v0.1_bundle.zip` … `Collatz_OT_Series_Papers_01_08_v0.8_bundle.zip` (2026-08-10 22:58 → 08-11 00:02), read against the `provenance/` tree of **SSSP Repaired v1.0**
**Tools:** [`src05_provenance_chain_recheck.py`](../code/src05_provenance_chain_recheck.py), [`src05_drill.py`](../code/src05_drill.py)
**Logs:** [`src05-provenance-chain-recheck.json`](../data/gate-logs/src05-provenance-chain-recheck.json) · [`src05-drill.json`](../data/gate-logs/src05-drill.json)

**Result: 25/25 checks. 18/18 planted defects caught by the check named for each. 2/2 null controls undisturbed.**

---

## Why these items got a different kind of check

The mathematics of Papers 01–09 was already rechecked in this tree, independently,
on the final v1.0 text — [`RUN-002-OT-SERIES.md`](RUN-002-OT-SERIES.md), 9/9 papers,
68/68 drill. Re-running that against *drafts of the same papers* would measure
nothing that has not been measured.

What the draft chain uniquely supports is a **provenance** measurement, and it is
one that cannot be performed from the repaired package alone: the drafts are an
independent archive of the pre-repair text, written down three days before the
repair existed.

That makes a question askable which is otherwise unaskable — **is the repair's
account of itself complete?**

## The chain is strictly additive

v0.1 → v0.8 appends exactly one paper per step and never touches a paper already
written. Every earlier paper is carried forward byte-identical; only the series
index is rewritten each time.

So there is no hidden revision history inside the drafting. All the revisions
happen later, at the repair, and are the ones the audit lists.

## The pre-repair text is attested from outside the package

Papers 01–08 inside the v0.8 bundle are **byte-identical** to
`provenance/original/`. The package's claim about what it started from is
therefore confirmed against an archive that predates it by three days, rather
than resting on the package's own word.

## The central check: the ledger *is* the change

`AUDIT_AND_CORRECTIONS.md` ships per-paper unified diffs. A correction ledger is
only worth something if those diffs are load-bearing, so:

> every published diff was applied to its published original, under an applier
> that demands exact context and exact hunk line-counts, and had to reproduce the
> repaired file **byte for byte**.

**All ten do — 276 hunks, zero rejections, zero mismatches.** The repair therefore
contains no edit that the audit does not declare.

Supporting, in the same instrument:

| | claimed | measured |
|---|---|---|
| byte-preserved | 01, 04, 05, 06 | 01, 04, 05, 06 |
| corrected | 02, 03, 07, 08, 09, HZ | 02, 03, 07, 08, 09, HZ |
| any seventh source changed | — | none |
| empty diff files | for the byte-preserved four | exactly those four |
| `CHECKSUMS.sha256` | — | 49/49 entries verify |

The byte-preservation claim and the correction claim are checked by **one**
comparison, which therefore cannot pass both by being blind.

## Two of my own checks were vacuous, and the drill is what found them

The first version of this recheck passed on every check as well. That is exactly the
situation this arm treats as unverified, so the SSSP package was copied to a
scratch tree and damaged one defect at a time.

The drill missed one defect — and chasing why exposed a defect in the *check*,
which then turned out to have a twin:

- **Paper 07.** The check asked whether `P_k(1)=1` appears in the repaired text.
  It does. It also appears in the **original** — the audit says so itself:
  *"The body already treated `m=1` separately."* What the repair added was the
  statement in the **theorem summary**. So the check could not fail for its
  stated reason.
- **Hard-Zeta.** Same shape, sharper. The check asked whether `\widetilde H_w`
  and `H_w∩[2,∞)` appear. Both were **already in the original** — the v0.1.1
  corrigendum had said the stopping-time domain is `n ≥ 2`. The audit's actual
  complaint is that the main body went on using the *unrestricted* union anyway.
  The correction is the disappearance of `⨆_{|w|=k} H_w`, not the appearance of a
  tilde that was there all along.

Both are now stated as **added-and-not-previously-present**, against the original
rather than against nothing.

That fix has its own trap, which is guarded too: Papers 07/08/09/HZ were also
mechanically renotated from `\(…\)` to `$…$`, so a naive "absent from the
original" test would come out true for *any* string containing math, for purely
cosmetic reasons. The original is delimiter-normalized first, and absence must
survive that normalization.

The same reasoning corrected Paper 08: `A_wx+B_w` is the standard form all
through the original, so its presence is no evidence of anything. The typo was
the single §7 instance reading `A_wr`, and the check now looks for that string
**leaving**.

## Every declared correction, individually

Each of these is now present in the repaired text *and* absent from the
delimiter-normalized original:

| Paper | what the repair did | how it is pinned |
|---|---|---|
| 02 | positive-integer residue cylinder replaces the ambiguous `ℤ_{≥0}` preview, fixing the `r_w = 0` boundary | `(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0}` in, `r_w+2^k\mathbb Z_{\ge0}` out |
| 03 | induction uses the always-positive representative `r_w+2^k`, which the all-`D` cylinder needs | `r_w+2^k\in\Omega_w.` in, bare `r_w\in\Omega_w,` out |
| 03 | canonical representative pinned | `0\le r_w<2^k.` in |
| 07 | summary records the `m = 1` case instead of leaving `ln 1 = 0` in a denominator | `\boxed{P_k(1)=1.}` and the 分母 caveat in |
| 07 | Theorems E and F restricted to odd `m > 1` | `對 odd $m>1$：` twice, zero times before |
| 08 | quotient typo | `A_wr+B_w` out, `A_wx+B_w ≡ 0 (mod D_w)` in |
| 08 | Möbius coefficient domain gets the ring-level unit condition | `R^\times` in |
| 09 | language typo | `若さらに` out, `若進一步` in |
| HZ | main body stops using the unrestricted union | `⨆_{|w|=k}H_w.` out, `⨆_{|w|=k}\widetilde H_w.` in |
| HZ | the `n ≥ 2` chart hoisted into the argument, not left as a corrigendum | boxed `\widetilde H_w:=H_w\cap[2,\infty).` in |

Plus: no legacy `\(…\)` or line-form `\[…\]` remains anywhere in the repaired
sources — and, as a guard against that being vacuous, **720 / 634 / 740 / 532** of
them did exist in the originals of 07 / 08 / 09 / HZ. All ten repaired sources
decode as strict UTF-8 with no replacement characters.

## The drill

18 defects, each required to fail **the check named for it** — not merely to turn
the run red, since almost any edit under `core_series/` also trips the checksum
verifier and would otherwise hand back a comfortable catch for the wrong reason.

Among them, deliberately:

- **D03** shortens one added line inside `07.diff` by a single character. Caught
  by the reproduction check.
- **D17** plants the Paper 07 summary statement into the **original** as well, so
  the "correction" was never new. A presence-only check stays green; only the
  comparison against the original notices. This is the defect that the first
  version of the suite would have shipped past.
- Two NULL controls — an unrelated file added outside the checksum manifest, and
  no change at all — must disturb nothing. Both quiet.

And separately, the patch applier itself is confronted with two inputs it must
reject: a one-character mutation of the original, and the wrong paper's diff.
Both rejected. Without that, a clean application would be evidence of nothing.

**One check is not drilled, and should be named as such.** The drill damages a
scratch copy of the SSSP package, so it cannot reach
`SRC05_loose_markdown_files_match_their_bundled_copies`, whose other input is
Neo's source folder — which this arm treats as read-only. That check is the one
claim here resting on a single unfalsified run.

## What this does not establish

Nothing mathematical.

That every declared correction is present in the repaired text says the ledger is
**honest**, not that the corrected statements are **true**. Their truth was checked
separately, on the final text, in [`RUN-002-OT-SERIES.md`](RUN-002-OT-SERIES.md).

The two are worth keeping apart. A complete and honest correction ledger is a
claim about bookkeeping. It happens to be one that almost no paper series can
support, which is why it was worth measuring — but it is not a claim about
Collatz.
