# BSD Phase 1 — Banwait–Huang Reproduction v0.2

**日期：** 2026-08-12

本版主題：

$$
\boxed{
\text{版本化 theorem semantics + adversarial regression}.
}
$$

新增：

- 舊版 $25$ 條 vs 現行 $12$ 條 exact diff；
- official discrepancy corpus 四條；
- failure taxonomy；
- Algorithm 1 soundness gates；
- 500K preflight；
- Agent regression protocol；
- semantic-version changelog；
- executable fixture regression test。

關鍵原則：

1. version regression與 explicit discrepancy分開；
2. 500K 尚未在本 runtime獨立重算；
3. 本地 Sage/LMFDB Agent先過三層 regression gate，再放大。

上一版 v0.1 ZIP 已封存在 `prior/`。
