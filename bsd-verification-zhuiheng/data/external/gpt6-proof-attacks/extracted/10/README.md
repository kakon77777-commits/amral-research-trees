# BSD Proof Attack 10

本包接續 Attack 09，只包含本輪的新推導、精確計算及必要輸入。舊 Kurihara、模符號、高度計算不會被重新執行。

## 先看哪個檔案

- **BSD_Proof_Attack_10_Unit_and_Trace_Bridge.md**：完整書面推導，尤其第 5 節的 trace 重建及 cup 零同倫，第 7 節的精確未完成步驟。
- **attack10_unit_tangent.py**：Python 3.9 以上，僅用標準函式庫。
- **INPUTS.json**：接受的前輪邊界、角色／period 規範與文獻來源。
- **attack10_result.json**：本輪已執行的結果。
- **MANIFEST.json**：上述五個 payload 的 SHA-256 及狀態。

## Windows PowerShell 重播

先解壓 ZIP，進入其中的 **BSD_Proof_Attack_10** 資料夾，再執行：

~~~powershell
py -3 .\attack10_unit_tangent.py --output .\local_result.json
(Get-FileHash .\local_result.json -Algorithm SHA256).Hash -eq (Get-FileHash .\attack10_result.json -Algorithm SHA256).Hash
~~~

預期第一行程式 exit code 為 0，第二行顯示 True。若本機使用 python 而非 py，改用：

~~~powershell
python .\attack10_unit_tangent.py --output .\local_result.json
~~~

macOS／Linux：

~~~bash
python3 attack10_unit_tangent.py --output local_result.json
~~~

可用 --precision 指定 3 至 30 的 log 精度；更改精度後，整個結果檔的雜湊自然不再與包內預設 precision=10 的結果相同。

## 本輪實際輸出

$$
u_{\mathrm{bot}}=17-12\sqrt2=(1+\sqrt2)^{-4},
$$

$$
q_{\mathrm{bot}}
=4L_{11}^{\mathrm{std}}(1,\chi_8)
\equiv9\pmod{11}.
$$

標準 Kubota–Leopoldt 值模 $11$ 是 $5$。新 Bernoulli 規範檢查同樣得到 $5$。精確 dual-number 模型完成 $26$ 個 words 的 $676$ 對計算。

## 核查的意義與界線

本地重播核查圓分單位身份、具尾項界限的局部 log、Frobenius 係數及 trace／cup 公式的有限模型。它不構成文獻定理的形式化證明，也不產生真實 Coleman-family Galois traces。

模型數字在 JSON 中標為 EXACT ALGEBRA MODEL，並非本例的 Hecke／Galois 數據。真實 trace jets、$n$、$C$、$B_2$ 座標和 $s_{11}$ 保留為 null。BSD_proved 與 canonical_frontier_updated 均為 false。

沒有提供本地端此次驗證日誌；使用者的「未見重大失誤」回報被如實保留，沒有擴張為外部驗證已完全通過。

