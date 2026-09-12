# BSD Proof Attack 09

本包包含完整原始推導、Python 程式、已接受的輸入、實際輸出及雜湊清單。所有數學原稿均為 UTF-8 Markdown。

先讀 **BSD_Proof_Attack_09_Eisenstein_Leading_Term.md**。本輪新增的是導子 $8$ 的 twisted moment 與具體 Eisenstein 退化抽取；沒有重跑舊 Kurihara certificate。

## Windows PowerShell

解壓 ZIP，進入其中的 **BSD_Proof_Attack_09** 資料夾。需要 Python 3.9 或更新版本；無外部套件。

~~~powershell
py -3 .\attack09_eisenstein.py --output .\attack09_result_local.json
if ($LASTEXITCODE -ne 0) { throw "Attack 09 exact calculation failed." }
$result = Get-Content .\attack09_result_local.json -Raw -Encoding UTF8 | ConvertFrom-Json
$result.shifted_twisted_moment.lambda8_at_zero_mod11
$result.unit_anchor
$result.invertible_factors
$result.derived_comparison
$result.open
~~~

如果系統只有 **python** 指令，把 **py -3** 改為 **python**。

檢查來源完整性：

~~~powershell
$manifest = Get-Content .\MANIFEST.json -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($entry in $manifest.files) {
    $actual = (Get-FileHash -LiteralPath $entry.file -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $entry.sha256) { throw "Hash mismatch: $($entry.file)" }
}
Write-Output "All manifest hashes match."
~~~

## Linux / macOS

~~~bash
python3 attack09_eisenstein.py --output attack09_result_local.json
~~~

## 預期輸出與範圍

新的 twisted moment 應為 $5\bmod11$，輔助單位的正規化 log 也為 $5\bmod11$，smoothing 常數為 $26$。兩個 $5$ 是不同計算，不能因此認定兩個完整的 $11$-adic 數相等。

程式從 **INPUTS.json** 接受舊的二維 Hecke 空間；只計算本輪新的負號線及四十條 cusp 路徑。輸出中保留所有路徑 indices 與十項 residue-measure 表，方便獨立檢查。

類的二次消失及 regulator 的三次消失，使用正文列明的退化定理與先前接受的 Kato 輸入。程式檢查的是其形式 leading-coefficient 代數，並未計算實際 Beilinson–Flach cohomology 類。

**C_value、n_value、B2_coordinates、s11** 應皆為 JSON null。**BSD_proved** 與 **canonical_frontier_updated** 應皆為 false。這些保留真實未完成的數學步驟，不是執行失敗。

二次驗證優先看正文第 3 節：負號路徑慣例、Gauss／period 規範、ordinary 測度，以及 $x^{-1}$ 的 odd Teichmüller 分支；再檢查式 (17)–(20) 的兩種 leading 操作與比例。
