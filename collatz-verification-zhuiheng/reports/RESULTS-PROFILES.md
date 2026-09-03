# Results profiles — what a renderer can rely on

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**For:** anyone building a page, sub-site or tool that reads a research line's
`data/results.v*.json` in this monorepo.

---

## The problem this exists to solve

`schema_version: 1` does not identify a shape.

Measured 2026-09-03 across every branch of this repository — two such files
exist, enumerated by `git ls-tree`, not by a list anyone typed:

| file | declares | actually shares |
| --- | --- | --- |
| `collatz-verification-zhuiheng/data/results.v1.json` | `schema_version: 1` | six keys |
| `erdos-885-k5-chengxu/data/results.v1.json` | `schema_version: 1` | the same six |

After those six keys the two documents have **nothing in common**. One
continues with `verified_claims`, `explicit_non_claims`, `coverage`,
`paper_sweep`, `gates`, `subject_verification`; the other with
`exact_reduction`, `exact_certificates`, `bounded_searches`. The second has no
`verified_claims` and no `explicit_non_claims` **at all**.

Neither file is wrong. Each was written for its own line before there was a
second one to agree with. But **a renderer that dispatches on the version
integer will break on one of them.**

---

## The fix, and why it is not a renumbering

Renumbering would require every line to move at once, and no line's tree may
edit another line's provenance. So instead of asking a file what it is,
**measure what it satisfies**:

### `results-envelope/1`

Present and well-typed:

| key | requirement |
| --- | --- |
| `schema_version` | integer |
| `research_line_id` | non-empty string |
| `researcher.display_name` | present |
| `date` | non-empty string |
| `problem.id` | present |
| `global_status.solved` | **boolean**, not a string |
| `global_status.statement` | non-empty string |

`global_status.solved` must be typed because `"false"` is truthy — a renderer
reading a string here would print "solved" for a line that claims nothing.

### `results-claims/1`

Everything in the envelope, plus:

| key | requirement |
| --- | --- |
| `verified_claims` | non-empty array; every entry has both `id` and `claim` |
| `explicit_non_claims` | non-empty array of non-empty strings |

### `results-pairs/1`

Everything in the envelope, plus a non-empty `render_pairs` array. Each entry
names two dotted paths that must resolve, in this document, to numbers:

| key | requirement |
| --- | --- |
| `value` | dotted path to the figure a page would naturally show |
| `against` | dotted path to the figure that gives it meaning |
| `why` | a stated reason; a pair nobody can review is a rule nobody can challenge |

**Why this profile exists.** The sub-site's first build rendered *"1441 defects
caught"*, *"121 controls undisturbed"* and *"72 items rechecked"*. Every one of
those numbers was correct against source. Every one of them was missing the
figure that gives it meaning: **"1441 defects caught" reads identically whether
1441 or 2000 were planted**, and the drill's entire claim is that those two are
equal.

A build-time check comparing each rendered number against source cannot catch
this. That check verifies **fidelity**; what is wrong here is **sufficiency**.
Nothing rendered was incorrect — the field that mattered simply was not
rendered, and a check can only check what is there. It is the same shape as a
link checker that confirms every link resolves while a page is missing a link
entirely.

Which of two numbers is load-bearing is a fact about the *line*, not something
a renderer can infer, and a list of pairs kept in the renderer would be a
second copy of this tree's semantics. So the line declares it, and
`build_results.py` resolves every declared pair against the finished document
before writing: **a declaration pointing at a renamed field is worse than no
declaration**, because the renderer's own check would then pass vacuously.

### `results-figures/1`

Everything in the envelope, plus a non-empty `headline_figures` array:

| key | requirement |
| --- | --- |
| `path` | dotted path resolving to a number in this document |
| `label` | what to show it under; a bare number under no heading is not a figure |

**And the rule that carries this profile:** a path declared here must **not**
also appear in `render_pairs`, on either side. A figure that belongs to a pair
and is *also* offered standalone reintroduces the bare-numerator defect through
the mechanism built to prevent it — which is not hypothetical: the sub-site
rendered `odd_starts_checked` paired in one section and bare in another, and
its build passed.

**Why this profile exists.** A renderer that has to guess which fields are a
line's headline numbers ends up hardcoding one line's shape. The sub-site knew
`paper_sweep.*` and `coverage.*` — this line's structure — so when a second
line arrived, its entire body of work (18,003,000 canonical anchors,
209,917,507 pair-fiber rows, 71 archived packets) rendered as **two empty
section headings**. Its numbers appeared nowhere except inside the prose of
hand-written claim sentences, where they carry no source path at all.

The line knows which of its numbers are headlines. The renderer cannot. So the
line says so, and a renderer needs to understand no line's internal structure.

A profile is only evaluated once its prerequisite holds: `results-claims/1`,
`results-pairs/1` and `results-figures/1` cannot be reported satisfied on a
document whose envelope is broken, however good their own fields look. They are
otherwise **independent, not a ladder** — a line may protect its ratios without
nominating headlines, or the reverse, and a drill control keeps that a legal
state.

---

## How to use this when rendering

**Do not dispatch on `schema_version`.** Ask
`code/validate_results_profiles.py`, which infers profiles from content — so a
file needs no change, and no other line's tree needs to be touched, for its
capabilities to be described correctly.

```
python code/validate_results_profiles.py
```

Current measurement, from `data/gate-logs/results-profiles.json`:

| line | satisfies | claim-box source |
| --- | --- | --- |
| `collatz-verification-zhuiheng` | envelope + claims + pairs + figures | `verified_claims` + `explicit_non_claims` |
| `erdos-885-k5-chengxu` | envelope + claims | `verified_claims` + `explicit_non_claims` |

The second line satisfied only the envelope until 2026-09-03, when its claims
and boundaries were structured into those fields — **verbatim from its own
README status boundary and duality-route report, by a different arm, with that
recorded in the file itself** (`claims_structured_by`). It is a demonstration
that the migration below costs a line nothing but transcription: no figure was
recomputed and no other file in that tree was touched. The envelope-only
rendering branch remains the correct behaviour for any line that has not done
this, and must not be removed.

For a line satisfying `results-pairs/1`, the validator returns
`figures_that_must_not_be_shown_alone` — read it and refuse to render a `value`
without its `against`. For a line satisfying `results-figures/1` it also returns
`headline_figures_to_render` — the standalone numbers, with their labels, which
is what a "verification scale" section should be built from rather than from
field names a renderer happens to know. This line currently declares five pairs, including one
found while writing this document: `coverage` publishes both
`odd_starts_checked` and `odd_starts_expected`, and the first build of the
sub-site rendered only the former.

**Failing a profile is not an error.** It is the branch a renderer should take.
A line outside `results-claims/1` still states its boundaries — the ERDOS-885
line states its own in one sentence, *"The `k=5` problem is not solved here"* —
and **must still be rendered with them**. Dropping a boundary because it was
not in the field you expected is the one failure mode this whole contract
exists to prevent.

The only hard failure is a file that **declares** a profile in an optional
`profiles` array and does not satisfy it. An inferred gap is information; a
false declaration is a claim about itself that is untrue, and the validator
exits non-zero on it.

---

## Adopting `results-claims/1` in another line

Nothing here asks a line to restructure. It needs two additions, and the
content for both usually already exists in that line's report prose:

1. `verified_claims` — one entry per claim actually established, each with an
   `id` and the claim in a sentence.
2. `explicit_non_claims` — the boundaries, as strings. What the line does not
   establish, said plainly.

That is the whole migration. Line-specific sections are never policed by these
profiles: a drill control exists precisely to keep unknown top-level keys legal,
so a line can carry whatever else it needs.

---

## The checks behind this document

`code/validate_results_profiles.py` is exercised by
`code/validate_results_profiles_drill.py`: **16 planted defects, each required
to be refused by the rule named for it, and 5 controls undisturbed.** One of
the controls is there to keep an honest line safe — a document satisfying the
envelope and nothing more must pass as a *legal state*, so the validator can
never become a gate that excludes a line for describing itself differently.

Logs: [`../data/gate-logs/results-profiles.json`](../data/gate-logs/results-profiles.json)
· [`../data/gate-logs/results-profiles-drill.json`](../data/gate-logs/results-profiles-drill.json)
