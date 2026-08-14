# 23｜Fouquet–Wan Supersingular Source Audit

對 $E_q$ 的任意 odd good supersingular prime $p$。

## H1

Fouquet–Wan要求 global residual representation absolutely irreducible。

base `696.e1` 的 mod-$p$ image maximal；quadratic twist保持 absolute irreducibility。

PASS。

## H2

FW Theorem 1.7排除：

$$
\bar\rho|_{G_{\mathbf Q_p}}^{ss}
=
\chi\oplus\chi_{\rm cyc}\chi.
$$

good supersingular local residual representation是不可約的 niveau-2 type，
所以不可能是 character direct sum。

PASS。

## H3

不用自行猜 representation normalization。

FW Theorem 1.1附近原文明確說 Assumption 3等價於：

- local automorphic representation為 special Steinberg；
- twist by unramified character taking $\ell$ to
  $(-1)\ell^{k/2-1}$；
- residual representation ramified。

weight $k=2$：

$$
(-1)\ell^0=-1.
$$

對 elliptic newform：

$$
a_\ell=-1
$$

即 nonsplit multiplicative。

取：

$$
\ell=29.
$$

`696.e1` 在 29 nonsplit multiplicative，且 admissible $q$ 使 29 split in
$\mathbf Q(\sqrt q)$，所以 local quadratic twist trivial。

又：

$$
v_{29}(\Delta)=1,
$$

故任意 odd $p\ne29$ residual仍 ramified。

good supersingular $p$ 當然不等於 bad prime 29。

PASS。

## BSD conclusion

Theorem 2.14先給：

$$
L(E_q,1)\ne0.
$$

Fouquet–Wan Corollary 1.10因此給相應 $p$-part BSD，
period issue另見下一份 audit。
