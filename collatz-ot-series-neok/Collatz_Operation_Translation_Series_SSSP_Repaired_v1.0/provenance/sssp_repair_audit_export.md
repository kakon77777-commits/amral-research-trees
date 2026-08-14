# Collatz Operation Translation Series — SSSP Repair Audit and Source-Set Anchor

**Claim [claim / artifact-anchor]**

The repaired portable source set consists of nine core Collatz Operation Translation Series papers plus one Hard-Zeta research-program paper. Exact UTF-8 source bytes remain in the portable package; this SSSP record anchors them by a deterministic source-set digest rather than retranscribing hundreds of kilobytes through chat/tool serialization. Aggregate SHA-256: 96b1b9ccb64a62a0d4fc3942d6cdf7af63c5ffe2ae3369799b7c20d1fe24f155. The aggregate is SHA-256 of canonical JSON over the sorted list of relative source paths, per-file SHA-256 values, and byte sizes. Paper 09 was recovered from the user's existing Library because it was omitted from the uploaded 7z while the series index and dependent papers identify the series as Papers 01–09.

Corrections applied before commit: (1) Paper 02: exact positive-integer residue-cylinder boundary for canonical residue r_w=0; (2) Paper 03: induction proof repaired because canonical r_w may equal 0 and therefore need not itself lie in Omega_w; the proof now uses r_w+2^k in Omega_w; (3) Paper 07: logarithmic contraction/binomial formulas restricted to odd m>1 and m=1 treated separately; (4) Paper 08: A_wr typo corrected to A_w x, and the Mobius determinant condition scoped to a field with unit-determinant clarification over general commutative rings; (5) Paper 09: recovered missing source, corrected a language typo, and normalized formal math delimiters; (6) Hard-Zeta: integrated the n>=2 stopping-domain corrigendum into the main decomposition and Dirichlet-mass bounds, and qualified the invariant-measure route with compactness/tightness/dynamical assumptions; (7) Papers 07, 08, 09 and Hard-Zeta: legacy TeX Markdown delimiters were mechanically converted to the canonical $...$ and $$...$$ source policy. Every transformation is preserved by original files and machine-generated unified diffs in the portable package.

$$
\Omega_w=(r_w+2^k\mathbb Z)\cap\mathbb Z_{>0},\qquad 0\le r_w<2^k.
$$

$$
r_w+2^k\in\Omega_w,\qquad F_w(r_w+2^k)=m_w+3^{u(w)}\in\mathbb Z\;\Longrightarrow\;m_w\in\mathbb Z.
$$

$$
\text{odd }m>1:\quad m^u<2^k\iff \frac{u}{k}<\frac{\ln2}{\ln m},\qquad m=1:\quad P_k(1)=1.
$$

$$
\text{over a field }K:\ ad-bc\ne0;\qquad \text{over a commutative ring }R:\ ad-bc\in R^\times.
$$

$$
\widetilde H_w:=H_w\cap[2,\infty),\qquad E_k^C=\bigsqcup_{|w|=k}\widetilde H_w,\qquad Z_w(s)=\sum_{n\in\widetilde H_w}n^{-s}.
$$

**Claim [claim / validated-artifact-report]**

Before SSSP commit, the repaired ten-source set passed strict UTF-8 and canonical-delimiter checks; 3,027 extracted formulas were independently rendered with MathJax (2,204 display and 823 inline) with zero render errors. Independent finite regression programs also rechecked finite-word affine/residue transport, correction extrema, the Paper 05 k=16 finite benchmark, accelerated valuation affine closure, generalized odd (m,r) transport, and Paper 09 hard-height behavior. These computational checks are finite/algebraic regression evidence only and are explicitly not a proof of the global Collatz conjecture.

---
<!-- SSSP source revision: 8 -->
<!-- SSSP source hash: sha256:5c38f568dc4bf377c5029f8edd1a52e02b3a480226c4fe1503b5f2ac695984a9 -->
