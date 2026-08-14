# BSD Global Enclosure / Phase 0

**日期：** 2026-08-12  
**範圍：** 先限定橢圓曲線 $E/\mathbb Q$  
**方法：** MCDM + Faithful Globalizer + Quantifier Audit + Representation Escape  
**研究定位：** 全局包圍、證書分層、外部文獻主線選擇與第一批 Agent 任務

---

## 這一包做了什麼？

它不宣稱證明 BSD，也不把 LMFDB 的數值吻合當成證明。

本包完成：

1. 拆分弱 BSD、$\Sha$ 有限性與強 BSD 首項公式；
2. 建立目前已知定理的 closure map；
3. 建立曲線級 BSD certificate ladder；
4. 審計外部可用路線；
5. 審計 Neo.K 舊稿中的「格點秩收斂」主張；
6. 設計第一個可執行 Agent 實驗；
7. 建立 machine-readable JSON schema 與樣本；
8. 建立一個「未證明／未認證曲線」的忠實證書前沿。

---

## 核心結論

$$
\boxed{
\text{BSD 值得進入 Phase 1。}
}
$$

但 Phase 1 不應直接叫「解 BSD」，而應叫：

> **BSD Certificate Atlas + Strong-BSD Twist-Family Reproduction**

第一批主工作：

- 重現 Banwait–Huang 2026 對 conductor $\le 500{,}000$ 曲線的算法判定；
- 對每個 isogeny class 建立 theorem-applicability certificate；
- 分離「數值吻合」「弱 BSD 已證」「指定 $p$-part 已證」「完整強 BSD 已證」；
- 以 rank $2$ 的 389.a1 作為高秩牆樣本。

---

## 文件

- `docs/00_BSD_Global_Enclosure_Consensus.md`
- `docs/01_BSD_Statement_and_Quantifier_Audit.md`
- `docs/02_Known_Theorem_Closure_Map.md`
- `docs/03_BSD_Certificate_Ladder.md`
- `docs/04_External_Route_Matrix.md`
- `docs/05_Internal_Grid_Rank_Audit.md`
- `docs/06_Phase1_Agent_Experiment.md`
- `docs/07_BSD_Certificate_Globalizer.md`
- `docs/08_Local_Agent_Handoff_Prompts.md`
- `schemas/bsd_curve_certificate.schema.json`
- `examples/11a1_rank0.json`
- `examples/389a1_rank2.json`
- `scripts/validate_bsd_record.py`
- `scripts/check_bsd_numeric_identity.py`
- `figures/bsd_closure_map.png`
- `sources/SOURCES.md`
- `sources/paper_manifest.json`

---

## 來源檔案說明

本輪已直接查核官方 Clay、LMFDB、arXiv 與近期學術資料。

由於目前執行環境未能將外部 PDF bytes 穩定下載到工作容器，ZIP 內沒有假裝嵌入 PDF；`paper_manifest.json` 保留每份核心論文的 URL、角色與下載狀態，供本地 Agent 直接抓取。
