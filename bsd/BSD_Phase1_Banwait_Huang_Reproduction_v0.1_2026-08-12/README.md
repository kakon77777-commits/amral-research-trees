# BSD Phase 1 — Banwait–Huang Reproduction v0.1

**日期：** 2026-08-12  
**範圍：** Banwait–Huang 2026，Theorem 2.18 / Algorithms 1–2  
**方法：** 全局包圍、theorem applicability、證書分型、純 Python 小樣本重現

---

## 本版實際完成

1. 把 Theorem 2.18 拆成 machine-readable condition map。
2. 對照論文 pseudocode 與目前官方 GitHub 實作。
3. 特別審計最新程式對 $\operatorname{BSD}(E,2)$ 的防過度宣稱處理。
4. 建立不依賴 Sage 的 Algorithm 2 純 Python mirror。
5. 在兩個代表分支上重現官方 $B=1000$ 輸出：
   - `46a1 / 46.a2`：CLZ20（有一個 rational 2-torsion）；
   - `106d1 / 106.b1`：Zha16（無 rational 2-torsion）。
6. 建立官方 conductor $<150$ fixture 與回歸測試。
7. 明確區分：
   - base curve 已通過 Algorithm 1；
   - twist $d$ 通過 Algorithm 2；
   - 這些判定依賴外部定理；
   - 純 Python mirror 本身不是 BSD 證明器。

---

## 最重要的結論

$$
\boxed{
\text{Algorithm 2 的低階算術條件可以脫離 Sage 獨立重播。}
}
$$

在官方兩個代表曲線上，純 Python 輸出與官方 fixture 完全一致。

但：

$$
\boxed{
\text{Algorithm 1 的 }\operatorname{BSD}(E,2)\text{、isogeny、descent 與 LMFDB 全域掃描}
}
$$

仍需要 SageMath、LMFDB 資料與 descent backends。

因此 Phase 1 v0.1 是：

```text
Theorem/implementation audit
+
Algorithm 2 independent reproduction
+
Algorithm 1 execution plan
```

不是完整 500K 重跑。

---

## 入口

- `docs/00_Phase1_Consensus.md`
- `docs/01_Theorem_2_18_Condition_Map.md`
- `docs/02_Paper_vs_Current_Code_Audit.md`
- `docs/03_Algorithm2_Independent_Reproduction.md`
- `docs/04_Algorithm1_Environment_and_Gaps.md`
- `docs/05_Global_Enclosure_and_Stop_Rules.md`
- `docs/06_Local_Agent_Handoff.md`
- `src/algorithm2_pure_python.py`
- `src/run_reproduction.py`
- `fixtures/official_ec_labels_150.csv`
- `fixtures/official_twists_B1000.json`
- `fixtures/representative_curves.json`
- `results/reproduction_report.json`
- `schemas/theorem_2_18_predicate_map.json`
- `figures/official_small_range_twist_counts.png`

上一階段完整 ZIP 已放入 `prior/`。
