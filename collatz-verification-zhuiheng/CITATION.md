# Citing this tree, and its timestamp

## What is being cited

This is one research tree inside a repository that holds several, each with its
own author. **Cite the tree and the commit, not the repository**, and read the
tree's [`README.md`](./README.md) and
[`reports/CHARTER.md`](./reports/CHARTER.md) for what it does and does not claim
before citing any number from it.

> 數學戰士「墜衡」 (Zhuì Héng), Claude Opus 5, under Neo.K / AMRAL Research Lab.
> *Collatz — verification and computation arm.* AMRAL Research Trees,
> `collatz-verification-zhuiheng/`, commit `26e6d90`, 2026-08-14.
> https://github.com/kakon77777-commits/amral-research-trees

Repository-level citation metadata is in [`../CITATION.cff`](../CITATION.cff),
which GitHub renders as a "Cite this repository" button. That file names Neo.K as
the repository's principal; per-tree authorship is stated in each tree, as the
repository protocol requires.

The subject series this tree verifies is **Neo.K's own work** and is cited
separately — see [`../collatz-ot-series-neok/`](../collatz-ot-series-neok/). This
tree's conclusions are its own and do not amend anything in that package.

## Timestamp

The state of this work is timestamped through **CTCL**
([commoninstant.org](https://commoninstant.org/)), Neo.K's common temporal
coordinate layer, rather than by a hand-typed date. The instant is registered,
retrievable and Ed25519-signed, and its metadata binds it to the exact git commit
and tree hash.

| | |
|---|---|
| CTCL instant | `ctcl:instant:69790ea7-a6e6-4181-beed-5de98ec024ba` |
| Shareable | https://commoninstant.org/i/69790ea7-a6e6-4181-beed-5de98ec024ba |
| UTC | `2026-08-14T08:43:05.868Z` |
| Unix ns | `1786696985868000000` |
| TAI (approx) | `1786697022.868` |
| Signature | Ed25519, key `ctcl-ed25519-1`, over `instant_id\|unix_ns\|timescale` |
| Verify key at | `/v1/pubkey` on the CTCL service |
| Git commit | `26e6d909bc34d55a70bef61733dd9dbdbcf29ef2` |
| Git tree | `3a375a0b2be9607e2d170a0c79620ef7e4fe9d15` |
| Branch | `agent/collatz-verification-zhuiheng` |

### What the timestamp does and does not assert

It asserts that **this exact repository state existed at that instant**, and it is
checkable: the instant's stored metadata carries the commit and tree hashes, so
anyone can retrieve the instant, read the hashes out of it, and compare them
against the repository.

It does **not** assert that anything in this tree is correct. It is a temporal
coordinate, not a review. The tree's own status boundary stands: the Collatz
conjecture is not proved here, every result is finite and bounded by its stated
domain, and a finite verification to any `N` is not evidence for the conjecture.

The instant's source is a synchronised edge wall clock with a stated uncertainty
of about 5 ms, and its `ns`/`µs` fields are zero-padded from a millisecond source
— the service says so itself, and precision is not accuracy. For a provenance
timestamp that is far more resolution than the claim needs.

### State certified by this instant

- exhaustive descent verification of `[3, 2^40]` — 549,755,813,887 odd starts,
  16 separately logged chunks, no guard trips;
- `K(2^40) = 550` at `n = 898,696,369,947`, Paper 09 §50's frontier function
  evaluated at that bound;
- Papers 02, 03, 04, 05, 06, 07 and 09 of the Operation Translation Series
  independently re-derived from their own theorem statements;
- 54 of 54 planted defects caught by the check named for each, across seven
  rechecks, with 7 controls undisturbed.

## Re-timestamping

A later state needs a **new** instant, not an edit to this one. Register it
against the new commit and add a row here; do not overwrite the record above.
Instants are retrievable by id, so the history stays readable.
