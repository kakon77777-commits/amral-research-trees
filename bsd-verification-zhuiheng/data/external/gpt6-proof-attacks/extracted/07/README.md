# BSD Proof Attack 07

本包交付一個新構造：在

$$
E:y^2+y=x^3+x^2-2x,\quad P=(0,0),\quad Q=(1,0)
$$

上，以明確曲線與有理函數證明

$$
\partial\Gamma_{PQ}
=4\bigl([(P,Q)]-[(P,O)]-[(O,Q)]+[(O,O)]\bigr).
$$

同時給出 $P,Q$ 四種配對的 rational 消零鏈，及保留 Tate 部分的 $1$-motive 資料。

先讀 **BSD_Proof_Attack_07_Explicit_Secondary_Geometry.md**。完整局部參數與 divisor 重數的論證在正文，程式重現它使用的精確代數。

本輪未證明這份幾何資料與 Kato 導出類的比較，未算出 $\mathfrak s_{11}$，未證明複數主項公式，亦未證明 BSD。整個 Albanese kernel 的消失也不在本包主張之內。

## 本地執行

Python 3.9 或更新版本，僅用標準函式庫，不需要 SageMath、SymPy、網路或舊證書。

Windows PowerShell，在解壓縮目錄內執行：

~~~powershell
py -3 .\attack07_cycle.py --output .\attack07_result_local.json
~~~

macOS／Linux：

~~~bash
python3 ./attack07_cycle.py --output ./attack07_result_local.json
~~~

成功時退出碼為 0，輸出 genus 3、smooth_mod_11 為 true、boundary_residual 為空，Kato_comparison 為 open。如果精確代數不一致，程式會在相關步驟拋出例外並返回非零退出碼。

程式不是一套普遍的 Chow group 判定器。它檢查本次曲線、函數、多項式條件及有限 cycle 係數，不把不存在的比較映射標為通過。

## 檔案

| 檔案 | 內容 |
|---|---|
| BSD_Proof_Attack_07_Explicit_Secondary_Geometry.md | 正式 UTF-8 研究工作稿 |
| attack07_cycle.py | 本輪精確代數程式 |
| attack07_result.json | 本輪執行輸出 |
| INPUTS.json | 輸入、來源、依賴與未完成步驟 |
| MANIFEST.json | 檔案雜湊與 source 格式檢查 |
| README.md | 本說明 |

主定理獨立於舊證書。外推到全部 rational Mordell–Weil 配對時，才沿用 $P,Q$ 張成 rank-two 空間的既有輸入。本包沒有重播舊計算，也沒有修改 canonical frontier。
