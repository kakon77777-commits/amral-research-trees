# BSD Next Handoff — P5 Rank-2 Analytic-to-Regulator Bridge

Date: 2026-08-14

## Fixed state

Do not reopen P4 for $389.a1$ at $p=11$ unless auditing the computation.

Current certified theorem-chain result:

$$
\Sha(389.a1/\mathbb Q)[11^\infty]=0.
$$

The exact witness is

$$
n=397\cdot991=393427,
$$

with a deterministic mod-$11$ eigenline evaluation

$$
\delta_n^{(\lambda)}=6\ne0.
$$

Canonical nonvanishing follows from the one-dimensional plus Hecke eigenspace together with Kim's good-ordinary nonvanishing theorem.

## Next target

Attack P5 only:

$$
\frac{L^{(2)}(E,1)}{2!}
\longleftrightarrow
\det(\text{height pairing})
$$

for

$$
E=389.a1,
\qquad
p=11,
$$

without assuming the strong BSD leading-coefficient identity.

Audit the strongest available derived Kato / generalized Perrin--Riou / determinant-line result and classify every needed hypothesis as:

```text
PROVED_FOR_389a1_p11
COMPUTABLE_CERTIFICATE
EXTERNAL_THEOREM_INPUT
CONJECTURAL
CIRCULAR_WITH_BSD
```

The Burns--Kurihara--Sano route may now use

$$
\Sha(389.a1/\mathbb Q)[11^\infty]=0
$$

as an independently established input. It must not use $\operatorname{BSD}_{11}(E)$ itself as an assumption if the goal is to prove the $11$-part leading term.

## Stop rule

If the best available rank-$2$ leading-term comparison still assumes $\operatorname{BSD}_{11}(E)$ or an equivalent leading-term statement, stop and record the exact circularity boundary rather than promoting it to a proof.
