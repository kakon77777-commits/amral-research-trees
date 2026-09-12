# BSD Proof Attack 04

2026-09-12。向前推導的證明稿及新計算。

先讀 `BSD_Proof_Attack_04_Mu_Zero_Descent.md`。本輪給出：

- 一個完整證明的整群環 saturation 引理：tame 增廣的 cyclotomic μ = 0，足以消除 character 比較後的有界 11-分母。
- E389a1、p = 11 的新 conductor-121 計算：primitive ordinary p-adic L-function 的 μ = 0、λ = 2。
- 接合 Kato 一側界、實際 Galois 複形、局部 Euler 因子與既有 finite primitivity，得到指定 relaxed 複形的 Kato／cofactor 類相差整群環 unit，以及對應 Fitting ideal 等式。

這是依賴明列既有輸入與已發表／預印本文獻定理的證明稿，尚未經獨立審查。沒有證明完整 BSD；原 R318 的完整 filtered regulator 比較與 R319 的複數主項比較仍未關閉。

Windows PowerShell 執行新計算：

```powershell
py -3 .\cyclotomic_mu.py --output .\cyclotomic_result_local.json
```

Python 3.9 以上，無額外套件。macOS／Linux 將 `py -3` 換為 `python3`。

預期 t-係數：`[0,0,2,2,2,0,5,6,10,7,0]`。

`eigenline_input.json` 保留既有向量與來源雜湊；程式接受它，不重新審查 Hecke eigenspace 或 canonical period。`cyclotomic_result.json` 保留本輪實際執行產生的 110 項求和，供外部審查新計算與符號慣例。

本包不重播原 392040 項 Kurihara certificate，也不修改既有 canonical frontier。
