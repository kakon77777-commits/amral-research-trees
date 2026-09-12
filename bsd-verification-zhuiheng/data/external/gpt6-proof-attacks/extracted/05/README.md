# BSD Proof Attack 05

2026-09-12。曲線 $389a1$，素數 $11$，秩二。

先讀 `BSD_Proof_Attack_05_Rank_Two_Regulator.md`。它是原始 UTF-8 正式稿；數學使用 `$` 與 `$$`。這是一份依賴明列既有輸入及外部定理的證明工作稿，尚未經獨立審查。

本輪推導的結果：

- 正規化局部 log 映射滿射，模 $11$ 的向量是 $(4,10)$。
- 全有限 ordinary Selmer 複形可化為 $[\Lambda^2\xrightarrow{tI_2}\Lambda^2]$；其 cyclotomic 高度矩陣的行列式是 $11$-adic unit。
- primitive 導出 Kato 類等於高度矩陣的伴隨矩陣作用在 log 向量上，差一個明確保留、尚未計算的 unit。
- relaxed 全域 $H^2$ 的 torsion 是 $\mathbb Z/11$；兩個輔助點的合併格指數是 $11^2$。

完整 BSD、複數主項比較，以及原 finite-$F$ 比較的全部 canonical 規範仍未解決。沒有把此稿的推導直接登錄成已獨立認證的 frontier。

## 檔案

| 檔案 | 用途 |
|---|---|
| `BSD_Proof_Attack_05_Rank_Two_Regulator.md` | 完整推導、正規化、引用、未解命題 |
| `local_log.py` | 本輪新增的精確有理數／形式群計算 |
| `local_log_result.json` | 本輪實際執行輸出，包含精確座標 |
| `INPUTS.json` | 沿用的算術輸入及來源包識別 |
| `MANIFEST.json` | 檔案雜湊、執行結果與文件檢查範圍 |

## 執行新計算

Python 3.9 以上，僅需標準函式庫。將 ZIP 解壓後，在這個目錄執行。

Windows PowerShell：

```powershell
py -3 .\local_log.py --output .\local_log_result_local.json
```

macOS／Linux：

```bash
python3 ./local_log.py --output ./local_log_result_local.json
```

預期兩個形式參數模 $121$ 為 $99,66$；正規化 log 向量模 $11$ 為 $(4,10)$。這個程式只計算局部 log；高度不退化、Selmer 模結構和 torsion 指數是正文中的數學推導，並非程式驗證的全域結論。

本包引用前輪輸入，不附帶或重跑舊證書。下一個主攻命題是正文第 10 節的 motivic／複數 realization 比較。
