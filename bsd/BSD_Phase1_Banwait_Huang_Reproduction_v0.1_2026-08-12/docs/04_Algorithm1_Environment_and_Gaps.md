# 04｜Algorithm 1 的執行環境與尚缺項

## 完整重跑需要

- SageMath；
- LMFDB local database；
- `lmfdb` Python package與設定；
- pandas / numpy；
- PARI 2-descent；
- mwrank；
- Sage native 2-isogeny descent；
- 足夠記憶體與本地資料。

---

# 本環境未完成

本輪沒有：

- 連線本地 LMFDB PostgreSQL；
- 執行 Sage；
- 執行 2-descent；
- 重掃 conductor $<500000$；
- 獨立證明官方 36,687 curve count。

因此不能寫：

```text
Full Algorithm 1 independently reproduced.
```

---

# 已完成的替代工作

1. 逐條拆 theorem conditions；
2. 讀取目前官方 implementation；
3. 審計證書強度；
4. 取得官方小樣本 fixtures；
5. 獨立重現 Algorithm 2；
6. 建立下輪 Sage execution plan。

---

# Phase 1 v0.2 的最低環境測試

先執行：

```bash
sage -python Algorithm1.py --cond_upper_bound 150
```

預期輸出十二條 base curves。

再執行：

```bash
sage -python Algorithm2.py output/ec_labels_150.txt
```

比較：

- curve labels；
- source branch；
- twists up to $1000$；
- file SHA；
- pass/fail metadata。

在小樣本完全一致後，才允許進入 500K。
