# 03｜FW-H2 Jordan–Hölder Lemma

令：

\[
V=E[p]|_{G_{\mathbf Q_p}},
\qquad
\omega=\bar\chi_{\rm cyc}.
\]

若 \(V\) reducible，寫：

\[
V^{ss}=\lambda\oplus\mu.
\]

Weil pairing給：

\[
\lambda\mu=\omega.
\]

Fouquet–Wan Theorem 1.7 的 local forbidden form是：

\[
\chi\oplus\omega\chi.
\]

## Lemma

\[
V^{ss}\simeq\chi\oplus\omega\chi
\]

for some \(\chi\) iff：

\[
\lambda^2=1
\quad\text{or}\quad
\mu^2=1.
\]

### Proof

若：

\[
\{\lambda,\mu\}
=
\{\chi,\omega\chi\},
\]

determinant比較：

\[
\omega
=
\omega\chi^2,
\]

故：

\[
\chi^2=1.
\]

所以其中一個 constituent平方為 \(1\)。

反之若：

\[
\lambda^2=1,
\]

則：

\[
\mu
=
\omega\lambda^{-1}
=
\omega\lambda,
\]

故：

\[
V^{ss}
=
\lambda\oplus\omega\lambda.
\]

\(\mu^2=1\) 情形對稱。

因此：

\[
\boxed{
\mathrm{FW17-H2\ FAIL}
\iff
\text{a Jordan--Hölder character is quadratic or trivial}.
}
\]

若 \(V\) 在 \(\mathbf F_p\) 上 irreducible，則不可能是 character direct sum，
故 H2 PASS。
