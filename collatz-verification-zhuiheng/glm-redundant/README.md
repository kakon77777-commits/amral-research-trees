# The GLM redundant-verification layer

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Ran:** 2026-09-02/03, after the 73/73 source sweep completed.

A second, independent reader over the same evidence — not a second opinion on
the mathematics, which this arm verified exactly, but a check on the *findings*
this arm published about the bundles' own verification scripts.

## Why this layer exists, and what it is not

Across the sweep the mathematics held everywhere it could be reached. What did
not hold was the *checking apparatus*: assertions that cannot fail, counters
that report a construction rather than a test, bounds looser than they read.
Those findings are judgements about code, and a judgement about code is exactly
the kind of claim a second reader can dispute.

It is **not** a re-verification of the theorems. GLM 5.3 Flash is a bounded text
worker under MACR: fixed model, no tools, no filesystem, no retry, no fallback,
no web access, and no verification or acceptance authority. It produces
*candidates*. Every candidate that disagrees with this arm is re-derived by hand
before anything is changed.

## The design, and the one thing that makes it a measurement

Each call shows GLM **one assertion** from a bundle's own checker, with the whole
script as context, and asks a single question: can this assertion ever fail?

GLM sees no verdict of mine, no report, no gate. The 28 assertions are shuffled
under a fixed seed, so position carries no signal.

**9 of the 28 are controls** — assertions this arm judges *can* fail, because
their truth depends on the paper's mathematics rather than on the code around
them. They are the reason this is a measurement rather than a chorus: a worker
that answers "cannot fail" to everything agrees with all 19 of my findings and
has told me nothing. The controls are what makes that visible, and the score
reports control accuracy beside agreement, never agreement alone.

It started as 11 controls and 17 findings. Two controls were **corrected to
findings** during the pre-dispatch audit, each before its own answer arrived;
`judgement_key.json` records both corrections with the batch position at the
time. Two further controls were found to be forced as well and were
**deliberately left unmoved** — continuing to edit the key as I discovered
things would start to look like fitting it to the result.

`judgement_key.json` — my verdict for every one of the 28 — was written and
committed **before any answer came back**, so the scoring is mechanical rather
than retrospective.

## What was sent, and under what authority

To `https://api.z.ai/api/paas/v4/chat/completions`, model `glm-5.3-flash`:
the three bundles' `verify_*.py` scripts and one assertion per call. Nothing
else — not the papers, not the theorem ledgers, not this arm's gates, drills or
reports.

Each dispatch passed MACR's GLM policy gate and carries a host-authorized,
expiring approval record bound to the exact task digest (`glm-preflight` →
`glm-approve` → `invoke --allow-network`). Privacy level `internal_approved`.

The standing rule [`no-third-party-delegation-until-authorship-page`] sets two
conditions for this layer: the 73-item sweep finished, and the AMRAL
authorship-verification page published. **The first is met; the second is not** —
the AMRAL site is mid-rebuild. Neo authorized this run explicitly on 2026-09-02
with that state known. Recorded here so the exception is visible rather than
implied.

## Two earlier designs that did not fit, and why

Worth keeping, because both failures are facts about the worker's profile:

1. **Whole-script discovery** ("find every assertion here that cannot fail")
   timed out. MACR caps the provider call at 300 s and the task needed longer.
2. **Section-scoped discovery** finished in ~70–85 s but returned nothing:
   `finish_reason: length`, with `reasoning_tokens` equal to the entire output
   budget. The model's output ceiling for this endpoint is 4096 tokens and
   MACR fixes `reasoning_effort: max`, so any task needing more than ~4096
   tokens of thinking cannot return an answer at all — raising the contract's
   `max_output_tokens` to 20000 changed nothing.

So open-ended discovery is out of reach at this profile, and the layer tests
*judgement* rather than *recall*. That is a real limit on what this layer can
say: it can confirm or dispute the findings this arm made, and it cannot find a
finding this arm missed.

## Files

| file | what it is |
| --- | --- |
| `judgement_key.json` | my verdict per assertion, fixed before any answer |
| `my_findings.json` | the cannot-fail findings, with the RUN report each came from |
| `tasks/` | one MACR TaskContract per assertion |
| `raw/` | the provider envelopes, verbatim |
| `score_judgement.py` | the scorer: agreement, controls, disputes |
| `judgement_result.json` | its output |
| `compare.py` | the scorer for the discovery design that did not fit, kept with it |

## What the layer actually cost and returned

An earlier version of this section, written while the batch was still running,
said that almost all the value arrived before the second reader answered
anything. **That was wrong.** It is left corrected rather than deleted, because
being wrong about it is part of the result.

**The reader found something I had missed after auditing the same set twice.**
`assert -(2**q) < d < 3` — A-U.2d.25's Theorem 3.1, which RUN-053 made its
headline as "a bound that is finally sharp" — is forced by the residue ranges
`0 <= r,s < M` alone. GLM returned a complete proof of it; verified on 33,281
integral cases with no Collatz orbit anywhere. I had classified that assertion
as a control, audited my controls twice, and kept it both times. See
`corrections.md`, correction 5.

**Building the control set found four more**, before any answer came back:
A-U.2d.24's Theorems 7.1 and 7.2, A-U.2d.25's synchronized alignment clauses,
and A-U.2d.25's Theorem 5.1 — together ~756,000 instances presented as evidence
in two published reports.

**The control arm failed as an instrument, and I built it wrong.** GLM answered
`can_fail: false` to every question in both passes, which reads like a worker
that never disagrees. But of the four controls that ever got an answer it was
right on three and had a defensible criterion disagreement on the fourth. The
constancy is not evidence of a mirror; it is evidence that most of my controls
were not controls. So **GLM's discrimination remains unmeasured** — the
instrument meant to measure it was made of the same misjudgements it was meant
to catch.

**The structural limit is real and independent of context size.** Nine of
twenty-eight pass-1 questions returned nothing at `finish_reason: length`. Pass 2
re-asked them with the context cut — in one case from 3077 to 1455 input tokens
— and they still burned the entire 4096-token output budget on reasoning. What
exhausts the ceiling is the *question*: "can this fail?" is an open-ended search
over inputs, while "is this forced?" terminates as soon as the guard is found.
That asymmetry is why the answered set skews to one side, and it cannot be
engineered away at this profile.

## The numbers

| | pre-registered key | adjudicated |
| --- | ---: | ---: |
| findings answered / confirmed | 17 / 17 | 20 / 20 |
| controls answered | 4 | 1 |
| controls GLM got right | 0 | 0 |

28 assertions, **21 answered** (19 in pass 1, 2 in pass 2), 7 never answered.
**GLM said `can_fail: false` on every one of the 21 — not once did it say an
assertion can fail.**

The two columns differ because three of the four answered controls have since
been *proved* forced (`post_hoc_verified.json`), one of them by GLM. The fourth
is the open criterion disagreement on `TV <= runs*H`. So after adjudication
**not one answered control survives as a fair negative test**, and the honest
statement is the uncomfortable one: GLM's discrimination is **unmeasured**. The
instrument built to measure it was made of the same misjudgements it was meant
to catch.

What can be said without qualification: it confirmed 20 of 20 findings it
answered, deriving each mechanism itself, and it overturned one of my
classifications with a proof I checked and accepted.

