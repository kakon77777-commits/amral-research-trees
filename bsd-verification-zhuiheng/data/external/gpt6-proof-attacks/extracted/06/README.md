# BSD Proof Attack 06

2026-09-12。接續 Attack 05；曲線 $389a1$，素數 $11$。

正式原稿是 `BSD_Proof_Attack_06_Balanced_Determinant_Descent.md`，使用原始 UTF-8 與單一套 `$`／`$$` 數學 delimiter。

本輪主攻 motivic／複數比較。實際結果：

- 固定尺度後，導出 Kato 類的公式是 $\kappa^\dagger=16\mathfrak s_{11}\operatorname{adj}(H)\ell$。已確定局部 multiplier $16$；未知全域 scalar $\mathfrak s_{11}$ 並未算出。
- 證明 $H\mapsto H+c\ell\ell^{\mathsf T}$ 不改變 $\operatorname{adj}(H)\ell$。
- 直接 motivic first-jet 升格在 Hodge–Tate 條件失敗：Sen 算子有非零冪零塊。
- 正、反 universal characters 在係數配對中所有階相消，給出固定幾何係數上的替代路徑。
- 普通 cup product 是零，因此必須保留 secondary pairing 的資料。
- 構造不依賴所列相容選擇的 $11$-adic regulator-line 元素，並給出複數側的精確 Mellin kernel。

**仍未完成：** 這個 $11$-adic 元素的 rational secondary lift，以及其複數 regulator 與 Mellin kernel 的比較（正文 BD6）。BD6 仍含真正的 rank-two 比較難題；其重新表述不是證明。完整 BSD 與既有 canonical frontier 均未標為完成。

| 檔案 | 內容 |
|---|---|
| `BSD_Proof_Attack_06_Balanced_Determinant_Descent.md` | 推導、失敗步驟、替代構造、引用與未證命題 |
| `attack06_algebra.py` | 本輪精確局部因子與符號多項式計算 |
| `attack06_result.json` | 實際執行輸出 |
| `INPUTS.json` | 前輪依賴與外部定理 |
| `MANIFEST.json` | 檔案雜湊及文件檢查範圍 |

Python 3.9 以上，僅需標準函式庫。解壓後，Windows PowerShell 執行：

```powershell
py -3 .\attack06_algebra.py --output .\attack06_result_local.json
```

預期 `local_multiplier` 為 `16`，Euler factor 模 $11$ 為 `5`，Coleman 座標倍率模 $11$ 為 `1`；兩個符號恆等式的 residual 為零。程式明確保留 `canonical_global_scalar_s11: null`，並不以代數計算替代未完成的幾何構造。

本稿在明列前提下提供書面證明，尚未經獨立學者或形式化審查。最有價值的下一個工作是正文第 8 節的 rational secondary determinant 構造。
