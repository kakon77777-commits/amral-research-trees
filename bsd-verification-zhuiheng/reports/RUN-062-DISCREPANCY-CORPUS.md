# RUN-062 — `02`'s four adversarial curves fail this line's 8b instrument, 4 of 4; and the ecdata pin that only reproduces as CRLF

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** [`02_Official_Discrepancy_Corpus`](../../../amral/public/bsd/phase1/files/02_Official_Discrepancy_Corpus.md) — the corpus's own adversarial regression set
**Tools:** [`src64_discrepancy_corpus.py`](../code/src64_discrepancy_corpus.py), [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src64-discrepancy-corpus.json`](../data/gate-logs/src64-discrepancy-corpus.json), [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)
**Data:** [`data/external/ecdata-25cec5e-allcurves.00000-09999`](../data/external/ecdata-25cec5e-allcurves.00000-09999), fetched from the pinned commit with its [provenance record](../data/external/ecdata-25cec5e-allcurves.00000-09999.provenance.json)

**Result: `02` names four curves — 62a1, 66b1, 105a1, 141c1 — that pass every early gate and are rejected by CURRENT Algorithm 1 on four counts, one being that **`f'(x₀)` is a rational square**. RUN-055 computed exactly that condition on all 3,747 CLZ20 curves of the accepted base and found **zero** squares. A check that has only ever seen passing data has not been tested — RUN-042's discipline — and until this round the 8b instrument had never seen a curve that must fail. **It fails all four.** Read from the pinned ecdata shard, each has exactly one rational 2-torsion point and `4·f'(x₀) ∈ {64, 64, 16, 144}`, all perfect squares; none is in the 40,749 base; the other two non-square conditions hold on every one, so `f'` is the *only* one of the three that fails, which is consistent with `02` listing it alone among the four rejection reasons. `02` calls the four a *theorem-router adversarial regression corpus* and says a version that accepts them earns the label `REGRESSION?`, not `NEW BSD BREAKTHROUGH!`; this round makes that a standing check on this line's own instrument. **Three of the four a-invariant lists the first draft typed from memory were wrong** — the shard is the source, and the gate reads it. And the shard's pin came out sharp: the package records the shard at 2,211,088 bytes, SHA-256 `8a6073c4…`; the blob at the pinned commit is 2,146,401 bytes, `259f3846…` — **64,687 bytes short, one per line**. CRLF-converted, it hashes to the package's value exactly. **The census hashed a Windows checkout of ecdata**, though its own `PROVENANCE.md` says the twist JSONs were pulled with `git cat-file blob` to avoid precisely this. Content identical modulo line endings; arithmetic unaffected; pin, as recorded, not verifiable against upstream without knowing to convert.**

---

## The four, from the shard

| curve | `ainvs` (shard) | in the 40,749 base | `X₀ = 4x₀` | `4·f'(x₀)` | square | `−f'` square | `−Δ` square |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| 62a1 | `[1,−1,1,−1,1]` | no | −4 | **64** | **✔** | ✘ | ✘ |
| 66b1 | `[1,1,1,−2,−1]` | no | 4 | **64** | **✔** | ✘ | ✘ |
| 105a1 | `[1,0,1,−3,1]` | no | 4 | **16** | **✔** | ✘ | ✘ |
| 141c1 | `[1,0,0,−2,3]` | no | −8 | **144** | **✔** | ✘ | ✘ |

Same code path as RUN-055 — the monic 2-division cubic in `X = 4x`, exact
integer bisection between critical points, `4·f'(x₀) = 3X₀² + 2b₂X₀ + 8b₄`.
Exactly one integer root each, as `E(Q)[2] ≅ Z/2` requires.

## What this is a control for

| | RUN-055 | this round |
| --- | ---: | ---: |
| CLZ20 curves checked | 3,747 accepted | 4 rejected |
| `f'(x₀)` a square | **0** | **4** |

Before this round, "0 of 3,747" was consistent with an instrument that could
not see a square at all. Now it is an instrument that finds every square the
corpus says is there and none the corpus says is not.

`02`'s other three reasons — `ord₂ L^alg = −2` where CLZ20 needs `−1`,
`E'(Q)[2] ≅ (2,2)` rather than cyclic, the `𝒮 ≠ ∅` gate — are not computed here.

## The regression rule, adopted

> 未來若某版本突然接受這四條，第一個標籤應是 `REGRESSION?`，不是 `NEW BSD BREAKTHROUGH!`。

The drill check for this gate asserts that all four fail `f'(x₀)` non-square.
If a future change to the 8b instrument accepts one, the drill goes red with
`02`'s label already attached.

## Three of four typed wrong

The first draft carried the four curves' `ainvs` from memory. 62a1 was right;
66b1, 105a1 and 141c1 were not, and on the wrong coefficients the root finder
found no 2-torsion at all — which would have read as "the instrument cannot
see these curves' torsion" had it been believed. The shard was fetched instead.
RUN-029's rule, again: a number from memory is a number from nowhere.

## The pin that only reproduces as CRLF

| | bytes | SHA-256 |
| --- | ---: | --- |
| package records `allcurves.00000-09999` | 2,211,088 | `8a6073c4703d…` |
| blob at `25cec5e`, fetched | 2,146,401 | `259f38463293…` |
| gap | **64,687** | = the file's line count |
| the fetched blob, CRLF-converted | 2,211,088 | **`8a6073c4703d…`** |

The package's `PROVENANCE.md` says of the twist JSONs: *`extract_exact_git_blobs.py`
uses `git cat-file blob`, bypassing Windows checkout newline conversion.* The
ecdata shards were not pulled that way; their recorded hashes are of a CRLF
checkout. Every arithmetic value in the package that derives from the shards is
unaffected — line endings carry no coefficients — but a reader who verifies the
package's ecdata pins against the upstream repository will get a mismatch on
every shard, as this round did, and will not be told why.

This is `02` §6's *file SHA* pin — scored PRESENT at RUN-056 — being present
and **not reproducible as stated**. RUN-056's row is corrected to *present,
reproduces only after CRLF conversion*.

## The drill

**260 defects, 260 caught by the check named for each**, 0 uncaught, 0 caught by the wrong check, 52 controls undisturbed, over 90 checks.

The 4 planted for this gate, each turning `discrepancy-corpus` red and nothing else:

| planted defect | went red |
| --- | --- |
| the square test always answers 'not a square', which the accepted base could never have exposed | `discrepancy-corpus` |
| the four curves are read from memory instead of the shard: 66b1's a-invariants as the first draft typed them | `discrepancy-corpus` |
| the shard's LF hash is reported as matching the package | `discrepancy-corpus` |
| 62a1 is reported as present in the 40,749 base | `discrepancy-corpus` |


## What this round does not claim

* **One shard was fetched, not all.** The four curves have conductors below
  10,000; the other shards' pins are inferred to have the same defect from the
  same script and are not checked.
* **`f'(x₀)` is one of `02`'s four reasons.** That it fails on all four does not
  by itself reject them; `02` says all four reasons apply, and three are not
  computed here.
* **The shard is trusted on its hash.** Its content was verified against the
  package's record, CRLF-adjusted; it was not compared to any third source.
* **Nothing about the router.** `02`'s "theorem-router" framing concerns
  Algorithm 1's dispatch; this round tests one predicate.
