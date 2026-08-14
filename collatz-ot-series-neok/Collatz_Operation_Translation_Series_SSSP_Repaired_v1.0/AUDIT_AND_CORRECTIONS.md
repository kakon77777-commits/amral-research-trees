# Audit and Corrections — Collatz Operation Translation Series

**Audit date:** 2026-08-14  
**Output package:** SSSP Repaired v1.0

## Executive result

The uploaded archive was usable but incomplete as a closed series: it contained Papers 01–08 plus the later Hard-Zeta research program, while Paper 09 was absent. The user's existing Library contained the completed Paper 09 and a 9/9 complete series index, so the actual Paper 09 was recovered rather than reconstructed.

The full ten-source set was then read and audited as one dependency chain. The repair intentionally avoids rewriting the research direction. It applies only corrections that could be concretely justified by domain logic, exact finite checks, source-format policy, or external reference verification.

## Content-level corrections

### Paper 02 — positive residue-cylinder boundary

The preview

$$
\Omega_w=r_w+2^k\mathbb Z_{\ge0}
$$

is ambiguous at canonical residue $r_w=0$ because the positive-integer domain excludes $0$. It is replaced by the exact form

$$
\Omega_w=(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0},
\qquad 0\le r_w<2^k.
$$

### Paper 03 — induction proof at $r_w=0$

The original proof used $r_w\in\Omega_w$. This fails for the all-$D$ residue cylinder where canonical $r_w=0$. The theorem itself is not false. The proof is repaired by using the always-positive representative $r_w+2^k$:

$$
r_w+2^k\in\Omega_w,
$$

and hence

$$
F_w(r_w+2^k)=m_w+3^{u(w)}\in\mathbb Z,
$$

which implies $m_w\in\mathbb Z$.

### Paper 07 — $m=1$ logarithmic boundary

The body already treated $m=1$ separately, but the final theorem summary used $\ln m$ without restricting $m>1$. The summary now states the logarithmic formulas only for odd $m>1$ and separately records

$$
P_k(1)=1.
$$

### Paper 08 — quotient formula typo

`A_wr+B_w` is corrected to `A_wx+B_w`.

### Paper 08 — Möbius/projective coefficient domain

The original subsection wrote $ad-bc\ne0$ without stating the coefficient domain. That condition is sufficient over a field. Over a general commutative ring, invertibility requires

$$
ad-bc\in R^\times.
$$

The subsection is now explicitly field-scoped and records the ring-level unit condition.

### Paper 09 — package recovery and language typo

The actual completed Paper 09 was recovered from the user's Library. `若さらに` is corrected to `若進一步`.

### Hard-Zeta — stopping-domain integration

The v0.1.1 corrigendum correctly said the stopping-time domain is $n\ge2$, but the main body still wrote

$$
E_k^C=\bigsqcup H_w.
$$

The correction is now integrated into the main argument:

$$
\widetilde H_w=H_w\cap[2,\infty),
\qquad
E_k^C=\bigsqcup_{|w|=k}\widetilde H_w,
$$

and the chart Dirichlet mass is parameterized directly by the exact quotient bounds for $\widetilde H_w$, so the $n=1$ boundary cannot silently re-enter through the Hurwitz-zeta representation.

### Hard-Zeta — invariant-measure route qualification

The phrase that a subsequential empirical limit *must* produce an invariant/quasi-invariant object was too strong without a specified state space and limit-passage assumptions. The route is now explicitly conditional on an appropriate compactification/state space, tightness, and the regularity needed to pass dynamics to a weak limit.

## Canonical source normalization

Papers 07, 08, 09 and Hard-Zeta used legacy Markdown TeX delimiters `\\(...\\)` and line-delimited `\\[...\\]`. These were mechanically converted to the project canonical delimiters `$...$` and `$$...$$`.

No normalization is disclosed only in prose. Exact original sources and mechanically generated unified diffs are retained under `provenance/`.

## Unchanged core papers

Papers 01, 04, 05 and 06 are byte-preserved in the repaired source set; their diff files are empty. They were still included in full-series validation and MathJax rendering.

## Validation

### Source and renderer layer

- ten repaired Markdown scholarly sources decode as strict UTF-8;
- no replacement characters were introduced;
- no canonical-source `\\(...\\)` or line-delimited `\\[...\\]` remains;
- MathJax rendered 3,027 extracted formulas with zero errors;
- 2,204 were display formulas and 823 inline formulas.

### Finite/algebraic regression layer

Independent programs rechecked:

- Paper 02/03 affine closure, residue coding and exact transport: 4,079 finite cases;
- Paper 02 correction extrema: 54 $(k,u)$ cases;
- Paper 05 binomial counts and $k=16$ direct benchmark;
- Paper 06 accelerated affine formula: 1,364 valuation-word cases;
- Paper 07 generalized odd $(m,r)$ affine/residue transport: 11,325 finite cases;
- Paper 09 hard-height prediction: 8,167 finite cases.

For Paper 05 the direct $1\le n<2^{20}$, $k=16$ run reproduced 938,413 strict descents and exactly two equality cases.

These tests are regression checks, not a global Collatz proof.

## SSSP commit

A public SSSP repair-audit document anchors the deterministic aggregate hash of the exact repaired source bytes and stores the correction ledger plus five key corrected formulas.

- document: `Collatz_OT_Series_Repair_Audit_2026_08_14_v1`
- revision: 8
- validation: PASS / 0 issues
- SSSP key math blocks rendered: 5
- document hash: `sha256:5c38f568dc4bf377c5029f8edd1a52e02b3a480226c4fe1503b5f2ac695984a9`
- snapshot: `sssp://Collatz_OT_Series_Repair_Audit_2026_08_14_v1/versions/r000008-5c38f568dc4b`
- repaired source-set aggregate SHA-256: `96b1b9ccb64a62a0d4fc3942d6cdf7af63c5ffe2ae3369799b7c20d1fe24f155`

## Why SSSP does not contain a chat-retranscribed copy of every paper

The exact formal source bytes already exist as UTF-8 artifacts. Sending hundreds of kilobytes through a chat/tool JSON transcription merely to duplicate them in a public record would add a new source-corruption boundary. The stronger design is to preserve exact bytes in the package, hash them deterministically, and commit the aggregate identity plus repair semantics in SSSP.

The package is therefore the exact portable source payload; SSSP is the immutable public repair/provenance anchor.
