# 04｜Local \(p\)-Isogeny Kernel Criterion

假設：

\[
E[p]|_{G_{\mathbf Q_p}}
\]

reducible。

選一條 stable cyclic subgroup：

\[
C\simeq\mathbf Z/p
\]

得到 local isogeny：

\[
\phi:E\to E'.
\]

令：

\[
\sigma(P)=\lambda(\sigma)P
\]

for generator \(P\in C\)。

因：

\[
x(P)=x(-P),
\]

且 \(p\) odd：

\[
x(P)\in\mathbf Q_p
\]

iff：

\[
\sigma(P)=\pm P
\quad\forall\sigma,
\]

iff：

\[
\lambda(G_{\mathbf Q_p})\subset\{\pm1\},
\]

iff：

\[
\lambda^2=1.
\]

所以：

\[
\boxed{
\lambda^2=1
\iff
\ker\phi\text{ 的 kernel polynomial有 }\mathbf Q_p\text{-linear factor}.
}
\]

另一個 JH character：

\[
\mu=\omega\lambda^{-1}
\]

是 dual isogeny：

\[
\widehat\phi:E'\to E
\]

的 kernel character。

因此：

\[
\boxed{
\mathrm{FW17-H2\ FAIL}
}
\]

iff `phi` 或 `dual(phi)` 的 kernel polynomial在 \(\mathbf Q_p\) 有 linear factor。

## 為什麼一條 isogeny + dual就夠？

- nonsplit reducible extension：original \(E[p]\) 只有一條 stable line；
  quotient constituent出現在 dual kernel；
- split representation：兩 constituent直接由 \(\phi,\widehat\phi\) 捕捉；
- 不必 enumerate所有 local p-isogenies。
