# CPL / Claude PairCeiling Research Pack v6

**日期：** 2026-08-11

本版完成一個重要里程碑：

$$
\boxed{
\text{$N=4$ toy model 的 boundary escape 已有 exact $70\%$ certificate。}
}
$$

主結論：

若 toy configuration law 滿足

$$
\mathbb E[S(1)]=\frac14,\quad
\mathbb E[S(2)]=\frac12,\quad
\mathbb E[S(3)]=\frac34
$$

且

$$
\mathbb E[S(4)]
\le
\frac{11254781}{3068556}
=
3.667777612662112\ldots,
$$

則可由 exact-rational configuration-wise dual certificate 嚴格推出

$$
\mathbb E[p]\ge70\%.
$$

三種 multiplicity patterns全部以 exact rational arithmetic 驗證；fully-simple pattern 使用 Newton identities + 3D Bernstein subdivision，在一個比真 root-data domain 更大的盒子上證正。

## 新增檔案

- `notes/09_Exact_P70_Boundary_Escape_Certificate.md`
- `scripts/certify_N4_boundary_P70_exact.py`
- `results/N4_boundary_P70_exact_output.txt`
- `results/N4_boundary_P70_exact_certificate.json`

上一版 `CPL_Claude_Research_Pack_v5_2026-08-11.zip` 已封存於本包。
