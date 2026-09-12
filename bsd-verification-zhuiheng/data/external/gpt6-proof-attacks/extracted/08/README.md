# BSD Proof Attack 08

本包接續 Attack 07，包含新推導、標準 Python 精確代數及本次輸出。沒有重播先前 certificates。canonical frontier 未更新。

先讀 **BSD_Proof_Attack_08_Norms_Localization_and_Scale.md**。接受的舊輸入與引用版本在 **INPUTS.json**；檔案雜湊與驗證範圍在 **MANIFEST.json**。

## Windows PowerShell

解壓 ZIP，進入其中的 **BSD_Proof_Attack_08** 資料夾。需要 Python 3.9 或更新版本，無外部套件。

~~~powershell
py -3 .\attack08_correspondence.py --output .\attack08_result_local.json
if ($LASTEXITCODE -ne 0) { throw "Attack 08 exact calculation failed." }
$localResult = Get-Content .\attack08_result_local.json -Raw -Encoding UTF8 | ConvertFrom-Json
$localResult.complete_pushforwards
$localResult.residual_closed_ambiguity
$localResult.localization
$localResult.open
~~~

如果系統只有 **python** 指令，將第一行的 **py -3** 改為 **python**。

檢查包內來源完整性：

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
python3 attack08_correspondence.py --output attack08_result_local.json
~~~

## 預期結果

三個完整推送為 $7,\ 7,\ 7((x+2)/y)^4$。平移比值及完整加法恆等式的殘差皆為兩個零多項式。封閉修正 $\Theta_c$ 的推送指數為 $(0,0,2)$；使用有理係數修正後，三個推送可成為 $1,\ 1,\ ((x+2)/y)^4$，而原邊界保持不變。

定位懸吊的邊界分別是 $P-O$、$Q-O$。程式檢查其除子記帳；定位定理、映射次數、regulator 型別及分裂的證明見本稿，並非程式自動證明。

**s11** 應為 JSON null，**BSD_proved** 與 **canonical_frontier_updated** 應皆為 false。這些標記不代表執行失敗；它們保留真正尚未完成的數學比較。

本地端二次驗證可優先檢查新稿式 (8)–(14) 的平移、符號與尺度修正，以及式 (20) 的定位分裂。所有本輪代數由本包自足執行，不需要舊包或 Sage。
