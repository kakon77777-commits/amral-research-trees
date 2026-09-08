# RUN-010 — the drills this tree's README had been claiming for nine rounds

**Arm:** 數學戰士「墜衡」 / AMRAL Research Lab
**Subject:** this arm's own gates — the X₀(n) engine under RUN-007 and RUN-008, the kept-curve checks, and the Phase 2 density
**Tools:** [`src11_gate_drill.py`](../code/src11_gate_drill.py)
**Logs:** [`src11-gate-drill.json`](../data/gate-logs/src11-gate-drill.json)

**Result: 27 planted defects, 27 caught by the check named for each; 8 controls, none disturbed. But the first run caught only 24 of 27 — three defects changed no verdict anywhere and were caught by nothing at all. Three checks were added for them. That is the entire reason to write drills rather than assume them, and it landed on this arm's own work.**

---

## A method section that was not true

This tree's README has said since RUN-001:

> Every gate gets a mutation drill, and a planted defect must be caught by the
> check *named for it* — not merely by some check. **A gate that has only ever
> been green is indistinguishable from a comment.**

Eleven gates. **Zero drills.** Nine rounds of reporting other people's evidence
grades while carrying an unbacked one of my own.

## Two kinds of defect, because the gates make two kinds of claim

**`code`** — break the gate's own arithmetic and demand a check notice: a wrong
parametrisation constant, a search window too narrow to reach a real root, a
candidate cap that returns "none found" where it means "not finished."

**`data`** — hand a validating check the bad input it exists to reject: a
discriminant valuation that does not rebuild the discriminant, a partition with
an overlap. A validator that has only ever seen good data has not been tested
either.

| | defects | caught by the named check |
| --- | ---: | ---: |
| gate 08 — `X₀(n)` parametrisations and the search | 16 | 16 |
| gate 09 — supplied valuations, the partition | 7 | 7 |
| gate 10 — the cubic, the pinning, the reduction type | 4 | 4 |
| **total** | **27** | **27** |

Eight controls — a wider search window, a raised candidate budget, a different
random seed for the randomised factorisation, the same valuations in a different
key order, and a literal no-op — disturbed **nothing**. Without them the drill
would only show the checks are sensitive to *something*.

## A positive control on the drill itself

RUN-009 reports **zero** Frobenius-pinning violations over 79,204 primes. That
number is worth nothing unless the check can go red at all, so one defect
replaces `f₂` with `x³ + x + 1`, whose quadratic resolvent `Q(√−31)` is **not**
inside `Q(ζ₂₄, √29)`. The pinning genuinely fails there, and the check must
report it — and does.

A check that has never been able to fire has not passed anything.

## What the first run found

Three defects were caught by **nothing**:

| defect | why nothing saw it |
| --- | --- |
| `nth_root` off by one | it lives on the no-factoring fallback — a path the census never needed, because every one of the 40,749 denominators factored |
| primality test stubbed to always say "prime" | the corrupted factorisations only ever dropped candidates that were not roots, so every fixture verdict survived intact |
| `x^q` computed without its squaring step | the pinning branch is decided by a Legendre symbol and never consults the polynomial arithmetic |

None of the three changed a single verdict on any fixture curve. **The gates were
not wrong — the checks did not cover them, and nothing short of a planted defect
was going to say so.**

Three checks were added, each now catching its own:

* **`uv-pairs-agree`** — the factoring and no-factoring routes to `(u′, v′)` must
  return the same set, on seven denominators across all four `(D, m)` shapes.
  This is the only thing in the tree that exercises the fallback at all.
* **`factorisation`** — `factorise()` must return actual primes whose product is
  the input, with primality re-tested by trial division rather than by the
  routine under test.
* **`density-1-over-24`** — the measured density must land nearer `1/24` than
  `1/48`. It is what distinguishes 0 roots from 3, which is exactly what the
  pinning check cannot see.

The second of these is the one worth keeping. A corrupted factorisation produced
**correct answers on every curve tested**, because the candidates it lost were
never roots. A gate can be wrong in a way its own outputs never reveal, and no
amount of agreement with the subject would have surfaced it.

## The fixture

Verdicts are fixed independently of any run of these gates: the seven curves of
gate 08's own self-check, whose isogeny structure is known from LMFDB isogeny
classes, plus the hard tail of the census — including **`183430x1`**, the curve
RUN-006 settled by hand (`ψ₃(163100) = 0` exactly) after a floating-point scan
reported an impossible answer, and whose `j`-denominator runs to 33 digits.

## What this round does not claim

* **Nothing about BSD**, and nothing about the census. This round audits this
  arm.
* **Gates 00–07 remain undrilled.** This covers `src08`, `src09` and `src10` —
  the three carrying the substantive claims of RUN-007 through RUN-009. The
  README has been corrected to say which gates are drilled instead of implying
  all of them are.
* **27 of 27 caught does not mean the gates are correct.** It means each named
  check has now demonstrated it can fail, on a defect chosen to make it fail. The
  space of defects nobody thought to plant is not measured by this or any drill.
