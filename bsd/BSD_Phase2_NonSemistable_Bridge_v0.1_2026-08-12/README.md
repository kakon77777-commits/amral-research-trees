# BSD Phase 2 — Non-Semistable Bridge v0.1

**日期：** 2026-08-12  
**定位：** 從 Banwait–Huang reproduction 轉入外部文獻型新綜合  
**主目標：** 測試能否以 Fouquet–Wan arbitrary-reduction Iwasawa/BSD 結果替換 Banwait–Huang odd-prime 路線中的 semistability 依賴。

---

## Phase 2 第一個重要修正

原本候選：

> positive $v_2(\Sha_{\rm an})$ → higher $2$-power descent

經最新版 Banwait–Huang Remark 2.19 查核後 **降級**。

作者明確指出：

> 所有真正走到 `check_BSD_at_2` 的 LMFDB curves，其 analytic Sha 都是 odd。

所以在 current 500K pipeline：

$$
\boxed{
\text{higher }2\text{-descent不是實際 coverage bottleneck。}
}
$$

它仍是一般 BSD 工具，但不是目前 Phase 2 首選。

---

## 新主線

$$
\boxed{
\text{Non-semistable rank-0 twist families}
}
$$

Banwait–Huang 本身稱 semistability 為 strong restriction。

目前可觀察域：

- conductor $<500000$ 全曲線：約 $3.06$M；
- analytic rank $0$：約 $1.17$M；
- semistable analytic rank $0$：約 $274.9$K。

因此 non-semistable analytic-rank-0 pool 約：

$$
895{,}988.
$$

這只是 search pool，不是 theorem-qualified curves。

---

## 核心橋

Banwait–Huang Theorem 2.14：

- 不要求 semistable；
- 對符合 $2$-part twist 條件的 $E_d$：
  - 給 $L(E_d,1)\ne0$；
  - 給 $\operatorname{BSD}(E_d,2)$。

Fouquet–Wan Theorem 1.7 / Corollary 1.10：

- odd $p>2$；
- 允許 arbitrary reduction type at $p$；
- residual Galois hypotheses成立時；
- $L(E_d,1)\ne0$ 可推出 $p$-part BSD。

因此候選綜合：

$$
\boxed{
\text{Banwait }2\text{-part/nonvanishing}
+
\text{Fouquet–Wan odd-}p
}
$$

有可能把 semistability 從 family theorem 中移除。

---

## 尚未解決的真正難點

不是 Iwasawa theorem 本身，而是：

$$
\boxed{
\text{如何把 Fouquet–Wan residual-representation hypotheses
編譯成可有限判定的 base-curve predicates？}
}
$$

以及：

$$
\boxed{
\forall p>2
}
$$

如何縮成有限 exceptional-prime audit。

這是 Phase 2 的正式 proof obligation。

---

## 文件

- `docs/00_Phase2_Global_Enclosure_Consensus.md`
- `docs/01_Phase2_Route_Matrix.md`
- `docs/02_Fouquet_Wan_Hypothesis_Compiler.md`
- `docs/03_Quadratic_Twist_Invariance_Bridge.md`
- `docs/04_Finite_Exceptional_Prime_Problem.md`
- `docs/05_NonSemistable_Family_Theorem_Schema.md`
- `docs/06_Phase2_Agent_Experiment.md`
- `docs/07_Stop_Rules_and_Claim_Ladder.md`
- `schemas/fw_predicate.schema.json`
- `schemas/phase2_candidate.schema.json`
- `scripts/fw_router_skeleton.py`
- `sources/SOURCES.md`

---

## 裁決

$$
\boxed{\text{GO — 但先做 hypothesis compiler，不先掃 89 萬 curves。}}
$$
