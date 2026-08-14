# BSD Phase 1 — Banwait–Huang v0.5 Exact Artifact Census

狀態：**COMPLETE**（主流程 27/27 checks PASS；獨立驗證 27/27 checks PASS）。

這個 artifact 完成 `V0_5_Exact_Census_Local_AI_Handoff_2026-08-12.md` 指定的工作：

- byte-for-byte 物化 OLD／CURRENT 四個 giant Git blobs；
- 對 base labels 做完整 set diff；
- 對 4,062 條 removed curves 做 3/5/7-isogeny 與 `|a3| = 3` gate census；
- 只在 36,687 條 stable base curves 上做 twist pair diff；
- 把 upstream Algorithm1 deletion 與 stable Algorithm2 delta 分離；
- 以整數 accounting identity 關閉全部 pair 數。

## 核心結果

```text
Base curves
  OLD       40,749
  CURRENT   36,687
  removed    4,062
  added          0
  stable    36,687

Algorithm1 removed-curve failure census
  ISOGENY_ONLY   1,353
  A3_ONLY        2,707
  BOTH               2
  UNEXPLAINED        0

Twist pairs (archived giant outputs)
  OLD total             293,482
  CURRENT total         247,391
  upstream removed       24,785
  stable removed         21,306
  stable added                0
  new-base added              0

Accounting
  293,482 - 247,391 = 46,091
  24,785 + 21,306 - 0 - 0 = 46,091   PASS
```

在 stable domain 上，CURRENT twist map 精確等於 OLD map 移除所有 `3 | M` 的結果；
逐 curve mismatch 數為 0。曲線級分類為 `UNCHANGED = 31,250`、
`SHRINK_ONLY = 5,437`、`EXPAND_ONLY = 0`、`MIXED = 0`。

## 重要 provenance 發現

選定的 OLD commit 是：

```text
1a0489c3c3099dd0c248624e6621df73ae8f0d43
```

但其中的 OLD twist JSON blob 最後一次變更發生於：

```text
72867942accf94b9513857a2c0bae3895af8e9bc
```

該 JSON 有 39,394 個 keys，與 `72867942` 的 base set 完全相同。其後
`1a0489c` 新增了 1,355 個 base labels，也修改了 `Algorithm2.py`
（包括加入 `disc_valuation_condition`），卻沒有改動 twist JSON blob。

因此：

- 本 artifact 對四個 archived giant outputs 的 census 是 exact；
- 1,355 個缺少 OLD twist entry 的 base curves不做虛構補值；
- 這 1,355 條恰好等於後加的 base labels，也恰好等於 4,062 removed curves 中
  命中 3/5/7-isogeny gate 的集合；
- stable domain 在 OLD／CURRENT 兩張 map 中都有完整 keys；
- OLD twist JSON 不能被描述成 `1a0489c` source tree 的 fresh end-to-end rerun。

完整逐條清單見 `results/old_base_curves_missing_from_old_twist_map.csv`。

## 先看哪些檔案

- `results/V0_5_EXACT_CENSUS_REPORT.md`：九個研究問題與閉合結果。
- `results/summary.json`：machine-readable 總結與 27 個 completion checks。
- `logs/independent_verification.json`：獨立重解析與交叉驗證結果。
- `results/algorithm1_removed_census.csv`：4,062 條 removed curves 的 gate 證據。
- `results/algorithm2_stable_curve_census.csv`：36,687 條 stable curves 的逐曲線差分。
- `results/algorithm2_removed_twists.csv`：21,306 個 stable-domain removals。
- `results/twists_removed_by_upstream_base_deletion.csv`：24,785 個 upstream removals。
- `results/raw_file_manifest.json`：Git blob SHA-1、SHA-256、bytes 與行數。
- `results/results_sha256.json`：所有 results 檔案的 SHA-256。

`inputs/metadata/old_base_curve_arithmetic.json` 是後續若要做 coherent historical
replay 時可直接使用的輔助資料；它不是本次 archived-output accounting 的必要輸入。

## 重跑方式

需要 Python 3.11+、官方 `ants_xvii` checkout，以及 John Cremona `ecdata` checkout。
Windows 的全域 `core.autocrlf=true` 會改變 checkout bytes，所以 giant inputs 必須用
提供的 extractor 從 Git object database 直接取 blob：

```powershell
python scripts/extract_exact_git_blobs.py --repo <ants_xvii_checkout> --root .
python scripts/build_algorithm1_metadata.py --root . --ecdata <ecdata_checkout>
python scripts/build_curve_arithmetic.py --root . --ecdata <ecdata_checkout>
python scripts/exact_census.py --root .
python scripts/verify_outputs.py --root .
```

`build_curve_arithmetic.py` 產生的是可選的後續 replay 資料；其餘四步足以重建並驗證
v0.5 census。所有 CSV／JSON／MD 產物採 UTF-8、穩定排序與固定欄位順序。

## 數學邊界

這是 theorem-producing computation 的 archived-output census 與 provenance audit，
不是所有 OLD curves 的新鮮 Sage 重跑，也不是一般橢圓曲線 Birch–Swinnerton-Dyer
猜想的證明。`UNEXPLAINED = 0` 僅表示這個有限 500K universe 中的 4,062 個移除項，
全部可由指定 gate 規則解釋。

來源與精確 commits／blobs 詳見 `sources/PROVENANCE.md`。
