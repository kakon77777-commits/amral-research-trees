# AI-7 跨範式映射報告 v1.0

**狀態：凍結候選（read-only review complete）**  
**日期：2026-08-09（Asia/Taipei）**  
**任務：在不嘗試解 P/NP、不中途改動研究來源的前提下，將 P/NP 動態四層閉合框架翻譯成標準計算複雜度、形式方法、狀態轉移系統與演算法工程語言。**

## 0. 範圍、邊界與結論先行

本報告只做跨範式重建，不宣稱 P=NP、P≠NP，也不把任何工程測試、Lean 編譯成功或網站上的研究提案當成複雜度定理。AI-6 的實際反應未被閱讀；未向 AI-1 至 AI-5 傳訊，未發布 Board，未修改研究來源。

已閱讀的證據包括：

- `D:\我的研究\學術討論\論文\數學\p=np專區\P_NP_數學構造狀態機` 中的中介層、動態四層閉合框架、GCC-first 與 GLC-first 交接文件及其相關輪次材料；
- [AMRAL P/NP 對偶證明預演研究區](https://amral.evemisslab.com/p-np-dual/)；
- [AMRAL P/NP 動態四層閉合框架（GLC）](https://amral.evemisslab.com/glc-framework/)；
- 五個指定 Codex 任務及其可取得的輸出；
- AI-2 的紅隊審計、AI-3 的 Lean 形式化、AI-4 的工程章程與驗證材料、AI-5 的 AEREC 承接與探針材料。

### 結論摘要

四層框架最穩妥的學術定位如下：

1. **GCC** 在採用固定、均勻、無 oracle、無免費超多項式 advice 的模型後，基本上是對「存在一個固定多項式時間演算法」的跨模型或座標化重述；它本身不是新複雜度類別。
2. **USRT** 是把演算法改寫成配置／狀態軌跡、終止命中時間與均勻轉換器的語言。若只重命名時間或以倒數表示速率，多半是座標變換；若要求一個真正均勻、可構造、成本受控的 universal transformer，則增加了明確的證明義務。
3. **GLC_std** 可翻成「語義契約 + total correctness + 完整資源帳本」。在帳本沒有漏掉構造、解碼、驗證、恢復與表示成本時，它主要是更精細的規格／審計接口，不是 P/NP 新理論。
4. **GLC_robust** 不是普通 total correctness 的同義詞。它要求在明確定義、非空、最大、適當公平的 admissible runs 上，所有允許執行都最終正確；這是政策相依的 safety/liveness 義務，可能產生真正的新研究，但不能直接等同 NP 的「存在一條接受分支」。
5. **USEG** 只有在 quotient／abstraction 對答案盲、可均勻構造、可多項式更新、可解碼並有 soundness/completeness/lift 證明時，才可能成為新的數學問題。原始路徑數量本身不能推出困難度；答案依賴的 quotient 或 `Z_0=Z_m=χ_L(x)` 則是循環。
6. 目前工程線證明了「可以把主張拆成可重播的 schema、provenance、closure、admission 與負例測試」，沒有證明四層箭頭，更沒有觸及 P/NP。v0.2.1 的 `REF-TYPE-01` 反例顯示：hash reachability／envelope closure 不等於 field-role／type-safe evidence closure。

一句話的翻譯是：**四層框架提供了一套把同一個計算對象從複雜度、軌跡、抽象與執行治理四個角度觀測的坐標系；其中 GLC 的 robust 語義與 USEG 的非循環壓縮條件才是可能超出單純改座標的部分。**

## 1. 標準學術基線

為避免名稱先行，先固定一個最小任務模型。令

\[
  \mathcal T=(X,Y,\mathrm{Dom},\mathrm{Spec})
\]

其中 `X` 是輸入、`Y` 是輸出、`Dom` 是合法輸入集合，`Spec(x,y)` 是正確性關係。決策語言是 `Y={0,1}` 的特例，語言 `L` 的規格是 `Spec_L(x,b) :⇔ b=χ_L(x)`。

一個演算法以狀態轉移系統表示為

\[
  \Sigma=(S,I,O,\mathrm{Init},\mathrm{Step},\mathrm{Halt},\mathrm{Emit}).
\]

對固定輸入 `x`，軌跡是

\[
  s_0=\mathrm{Init}(x),\qquad s_{t+1}=\mathrm{Step}(s_t,x),
\]

直到 `Halt(s_t,x)`，並由 `Emit(s_t,x)` 產出結果。若 `Step` 是關係而非函數，則一個輸入有多條 run；這時必須明確寫出是存在、所有、最大、有限或公平 run 的量詞。

### P/NP 的量詞骨架

對決定性演算法，標準的 P 型要求可寫成：

\[
  \exists A\;\exists k,c\;\forall x\in\mathrm{Dom}:
  A(x)\downarrow\ \land\ \mathrm{Spec}(x,A(x))\ \land
  T_A(x)\le c(|x|+1)^k.
\]

關鍵是 **先固定一個有限描述的 `A`，再對所有輸入長度與輸入量化**。錯誤的替代式是

\[
  \forall n\;\exists A_n\quad T_{A_n}(n)\le \mathrm{poly}(n),
\]

因為 `A_n` 可以把長度 `n` 的全部答案表、trie 或 truth table 藏在演算法描述中；這是 nonuniformity/advice 問題，不是 P 的 uniform witness。

對 NP，最安全的決策語言翻譯是：

\[
  x\in L \iff \exists w\;(|w|\le p(|x|)\land V(x,w)=1)
\]

或等價地，非決定性機器有 **至少一條** 接受分支。這個存在量詞與 robust 執行中「所有 admissible runs 都正確」的全稱量詞不可混用。

### Total correctness 與 partial correctness

- partial correctness：若執行終止，輸出滿足規格；
- total correctness：對每一個合法輸入，執行終止且輸出滿足規格；
- polynomial total correctness：再加上最壞情況時間、空間及其他被宣告資源的多項式界。

這三者已經能表達 GLC_std 的大部分核心。GLC 的附加價值不在把「正確且終止」換一個縮寫，而在於把語義、表示、證據、恢復與跨 run 的義務明確列為帳本欄位，並在需要時把它們分離。

## 2. 四層框架的標準化重建

### 2.1 GCC：模型族與複雜度座標

GCC 的穩健翻譯不是「所有可能的模型都很快」，而是：

> 在一個事先封閉的 admissible model family 中，是否存在一個固定、均勻、無 oracle、無免費無限精度／超多項式 advice，且可由標準模型以多項式成本模擬的決定性演算法，對所有合法輸入完成正確計算？

若答案是「是」，而模型族確實滿足多項式模擬與表示成本的 invariance，則 GCC 的 `Poly` 判定與 `P` 是同一個類別判定的不同包裝。若 `GCC(L)=[T_M^L]_{\equiv poly}` 沒有說清楚 `M` 是否固定、模型描述是否計入、模擬器是否均勻，則它仍是研究規格，不是完整定義。

### 2.2 USRT：軌跡、命中時間與均勻轉換器

USRT 把 `A(x)` 拆成配置序列 `S_A(x,t)`，指定正確終端集合 `Good_L(x)`，並使用命中時間

\[
  \tau_A(x)=\min\{t:S_A(x,t)\in Good_L(x)\}
\]

與最壞情況 `T_A(n)=\max_{|x|=n}\tau_A(x)`。`R_A(n)=1/(1+T_A(n))` 只是單調重參數化；「速率相等」若只表示同一個 polynomial cone，也不是逐點時間相等。

真正有內容的 USRT 主張必須指定：

- 輸入機器 `N` 的有限描述與 clock；
- 一個固定的 universal transformer `U`；
- `U` 的生成、模擬、狀態更新、終止與解碼成本；
- 量詞是 `∃U ∀N ∃q_N`，還是更強的 `∃U ∃q ∀N`；
- `q_N` 是否允許依賴 `N`、是否仍為統一可計算的多項式界。

因此「USRT 等價於 P」只有在上述 uniformity、可構造性與資源界已證明時才成立；只把時間軸換成速率不會產生等價定理。

### 2.3 USEG：路徑壓縮與決策充分抽象

對非決定性系統，原始接受路徑集合 `Γ_N(x)` 可能指數大。單純聲稱「路徑很多」或「把路徑合併」都沒有複雜度結論。USEG 需要一個固定、答案盲的抽象：

\[
  Z_0=\mathrm{Build}(N,x),\qquad
  Z_{t+1}=\mathrm{Step}(Z_t,N,x),\qquad
  b=\mathrm{Dec}(Z_m),
\]

並證明：

1. `Build` 不取得 `χ_L(x)` 或接受答案 oracle；
2. `m`、每個 `Z_t` 的表示長度、構造、更新與解碼成本都受宣告界控制；
3. `Dec(Z_m)=1` 當且僅當原系統存在接受分支；
4. 若 `Z` 是 quotient／抽象狀態，必須有 answer-blind equivalence、soundness、completeness，以及從抽象答案回到原問題的 lift/refinement 證明；
5. 若使用自適應摘要，摘要的生成與更新也要計入成本，不能把答案依賴的摘要當作輸入。

這裡才有可能出現真正新的數學問題：對一般 NP 計算，是否存在一個均勻、答案盲、可多項式更新且決策充分的壓縮？這與一般的 quotient、bisimulation、abstract interpretation、symbolic model checking、dynamic programming、knowledge compilation 有家族相似性，但不能僅靠換名聲稱它們已經給出 USEG。

### 2.4 GLC：最後驗收層，而非第四個免費等價量

GLC 的核心口號「過程自由，最終帳本不自由」可以嚴格化為：允許內部使用不同的表示、路徑、重排或策略，但所有被接受的實作必須在同一份 task-relative contract 下交付可核查的結果與成本證據。

建議將 GLC 分為兩個不可混淆的軸：

- **resource-neutral / bounded**：前者只問正確、完成、語義不失真與帳本有效；後者再要求時間、空間、構造、更新、解碼、驗證、恢復、生成、lift、restart、parallel、precision、code/advice/proof bytes 等均滿足指定界；
- **standard / robust**：前者針對規格指定的正常 run；後者對一個明確的 admissible run class 做全稱驗收。

resource-neutral 不代表「過程不花資源」，而是暫時不把某種多項式界當作 GLC 基礎公理；一旦要談 P/NP，資源界必須回到明確的計算模型。

robust 版本至少需要：

\[
  \mathrm{Runs}_{adm}(A,x)\ne\varnothing,
\]

並對每條最大、適當公平的允許 run `ρ` 要求最終抵達 `Good_L(x)`，且恢復、重路由、rollback、representation switch 的代價納入帳本。否則 `Runs_adm=∅` 會使全稱命題真空成立；只有 weak fairness 也不會自動給出多項式 wall-clock 界。

## 3. 精確對應表

| 四層／術語 | 標準對應 | 只是換坐標，還是新增義務 | 必須防止的誤讀 |
|---|---|---|---|
| GCC | 固定模型下的 uniform polynomial-time decision；在良好 invariance 假設下即 P 的模型族表述 | 主要是坐標化；模型封閉、模擬與表示成本是額外前提 | `∀n∃A_n` 被誤當 `∃A∀n`；pointwise inf 被誤當 uniform witness |
| USRT | 配置／transition system、正確終端、hitting time、worst-case runtime | 狀態軌跡與倒數速率是坐標化；universal transformer 的均勻構造與界是新增義務 | 速率相等不是時間逐點相等；universal 不等於同一個固定 exponent |
| USEG | quotient／abstraction／symbolic summary／dynamic-program state | 非答案依賴、決策充分、可更新、可解碼、sound/complete/lift 是實質新增義務 | 路徑數量不等於 hardness；答案依賴 quotient 是循環 |
| GLC_std | task-relative total correctness + semantic contract + cost-complete ledger | 若不加新 run policy，主要是規格與驗收接口 | 「只看 final ledger」不能刪除構造、驗證與表示成本 |
| GLC_robust | all-admissible-run safety/liveness、fault/recovery policy、fairness/maximality | 明確新增且 policy-relative；不是普通 total correctness 的同義詞 | `∀` run 不等於 NP 的 `∃` accepting branch；空 run 集造成 vacuity |
| GLC_0 | correctness + eventual completion + semantic losslessness，暫不綁定 polynomial bound | 是資源軸的拆分，不是 P 的證明 | resource-neutral 不是 cost-free |
| `S=(B,Q,I,O,δ,λ)` | 標準有限／無限狀態 transition system；TM configuration 是其特例 | 表示換坐標；狀態不應偷藏答案或未計入 advice | state count、transition cost、precision、memory 必須分開計 |
| semantic loss debt | abstraction/refinement 尚未證明的 obligation set | 是有用的證明管理結構，不是已知複雜度量 | debt 不是標量，未退役的 debt 不能被零化 |
| adaptive algorithm | 依觀測歷史選擇下一個已驗證動作或演算法的 controller／portfolio | 自適應本身不是新類別；uniformity、最壞界、無答案 oracle、rollback/termination 是新增驗收條件 | 實驗中較快不等於最壞複雜度改善 |
| AEREC／工程閉合 | immutable snapshot、replay、provenance、external validator、negative corpus、no-change control | 工程治理與證據接口；可發現規格缺陷，但不替代定理 | hash closure 不等於類型安全、語義安全或 P/NP 結論 |

## 4. 六個容易混淆的精確交叉點

### 4.1 Uniform algorithms 與 nonuniform families

「每個長度都有一個短方法」不是「有一個對所有長度工作的演算法」。至少要記錄：

- 描述 `A` 是否固定且有限；
- 是否有 advice `a_n`，其長度與生成成本是否計入；
- `A_n` 是否可由單一 generator 均勻產生；
- code length、table/trie size、preprocessing 與 construction 是否在 ledger 中；
- 模型是否允許隱含無限精度或未宣告的外部資料。

AI-2 的 PARITY 對照已精確展示：uniform streaming program 與逐長度 truth-table/trie 可以有相同的 final ledger `(Y=1,C=1,Λ=0,T=O(n))`，但後者的 provenance、uniformity、advice 與生成成本完全不同。這正是「最終帳本不自由」必須把 code/advice/provenance 納入，而不能只記答案與運行時間的原因。

### 4.2 Transition systems 與 total correctness

標準決定性演算法可視為每個輸入只有一條 canonical run 的 transition system。GLC 的 `C`、`F`、`B`、`R`、`S`、`Λ` 等欄位可以拆成：

- `C`：輸出／語義 correctness；
- `F`：是否完成、是否命中 terminal；
- `B`：資源 bound；
- `R`：多項式或其他資源 cone；
- `S`：執行序列、轉換與狀態歷史；
- `Λ`：抽象或表示造成的 semantic loss。

這使 GLC 成為比單一 `T(n)` 更完整的驗收接口，但不應把欄位數量誤當成複雜度分離。AI-3 的 Lean Phase 1 已形式化最小的 run、terminal、account、budget 與 gate 組合，但明確沒有形式化 P/NP/GCC/USRT/USEG 四層等價。

### 4.3 Quotient／abstraction 與 semantic losslessness

一個 quotient 只有在它保留所需觀測量時才可用。至少要回答：

1. 等價關係是否不看答案、不看未來 oracle、且可由輸入與當前摘要決定？
2. 抽象 transition 是否模擬或 refine 原 transition？
3. `Dec` 是否 sound 且 complete？
4. 從抽象 witness、路徑或終端能否 lift 回原系統？
5. quotient 的構造、canonicalization、更新、解碼與驗證是否在宣告資源內？

若只是把語義相同的終端都映成 `1`，那可能只是輸出投影；若把「是否存在接受路徑」直接放進 quotient label，則是把待證答案放進輸入。`Λ=0` 因而不是一句宣告，而是待證的 refinement／lifting obligation。

### 4.4 Robust execution 與 NP nondeterminism

NP 的非決定性是「存在一條可接受分支」：

\[
  x\in L\iff\exists \rho\in\mathrm{Runs}(N,x):
  \rho\text{ reaches an accepting terminal}.
\]

robust GLC 則更接近：

\[
  \mathrm{Runs}_{adm}(A,x)\ne\varnothing\ \land
  \forall\rho\in\mathrm{Runs}_{adm}(A,x):
  \rho\text{ is maximal/fair and eventually reaches a correct terminal}.
\]

這兩種量詞描述不同對象。AI-2 的 A06 已指出，若沒有將「分支選擇」與「故障／排程／重路由」分型，`GLC(N,x)↔GLC(D,x)` 對 NTM 會直接混淆 existential branch 與 universal fault semantics。

### 4.5 Adaptive algorithms 與 recursive evolution

自適應系統可寫成

\[
  (x_t,m_t)\mapsto(a_t,m_{t+1}),
\]

其中 `m_t` 是有限且可核查的記憶／策略狀態。學術翻譯應使用「verified adaptive controller」、「online algorithm」、「algorithm portfolio」或「iterative synthesis with rollback」，並問：

- adaptation policy 是否固定且均勻？
- 觀測是否包含答案、未宣告 advice 或超多項式歷史？
- 每次更新、試錯、重啟與 rollback 是否收費？
- 是否保證每個合法輸入終止？
- 最壞情況而非單次平均或 bounded corpus median 是否受界？

AI-5 的 `no-change-control` 是有價值的工程控制：當外部 negative probe 已經重現 `REF-TYPE-01` 時，保持候選不變而不是把新行為升格。但這仍是 evidence governance，不是自適應演算法的複雜度定理。

### 4.6 Rate、cone 與逐點等式

`R(n)=1/(1+T(n))` 保留單調性，但會丟失常數、低階項與逐點結構；「同一 polynomial cone」只表示存在某個多項式界的同一大類。若研究主張需要精確的 uniform exponent、constructive compiler 或 fine-grained lower bound，cone 等價不夠。USRT 應把以下三件事分開：

- 逐點時間等式；
- 多項式階的等價；
- 有證據的均勻轉換器。

## 5. 哪裡只是改座標，哪裡增加義務，哪裡值得研究

### A. 主要是改座標／重述

- 把 TM configuration 寫成 state transition；
- 把終止時間寫成 terminal hitting time；
- 把多項式時間寫成 polynomial cone 或單調速率座標；
- 把 correctness、termination、resource bound 拆成 ledger 欄位；
- 在已知多項式模擬成立的模型族之間使用 GCC 語言；
- 將普通演算法的正確性改寫成 GLC_std 的 contract。

這些重述有工程與教學價值，尤其能防止把「有輸出」誤當「有正確輸出」，但不應單獨被宣稱為新類別或 P/NP 障礙突破。

### B. 明確增加的新義務

- `∃固定A∀輸入` 的 uniformity 與非 uniform advice 排除；
- 生成、表示、解碼、驗證、lift、恢復、重啟、平行化與 precision 的成本完整性；
- 抽象的 answer-blindness、soundness、completeness、refinement；
- robust runs 的非空性、最大性、公平性與故障政策；
- provenance、schema／field-role／type-safe binding，而不只是 hash reachability；
- 自適應策略的固定性、最壞界、終止與 rollback；
- 由局部 step bound 推到總時間時的乘積／狀態增長分析；
- 把「可驗收的報告」與「可證明的定理」分開。

AI-2 已展示多個具體漏洞：`m=0` 的 USEG 循環、空 admissible-run 集合造成真空、weak fairness 不給 wall-clock 界、逐步多項式不給總多項式、以及 restricted representation lower bound 不可自動提升為 general time lower bound。

### C. 可能是真正的新數學問題

下列問題值得獨立命名，但目前只能稱為 conjecture/open problem：

1. 對一大類非決定性或分支計算，是否存在均勻、答案盲、決策充分、可多項式構造／更新／解碼的 USEG 摘要？
2. 在明確的 transition-system 與 fault model 下，何種 abstraction/refinement 條件能保證 GLC_robust 且保留多項式成本？
3. 是否存在與模型族無關、可組合且不允許 witness laundering 的 complexity-ledger calculus？
4. 何種 `GCC→USRT` 或 `USRT→USEG` 轉換真正具有獨立內容，而不是把同一個 deterministic solver 重新包裝三次？
5. 在 uniformity、representation、construction 與 recovery 都收費的前提下，adaptive portfolio／recursive evolution 能否有嚴格的 worst-case characterization？

這些問題有研究價值，但只有在先固定模型、量詞、成本與驗收語義後，才是可證偽的數學命題。

## 6. 五線輸出的證據如何影響映射

| 線路 | 已觀察結果 | 對本報告的正確解讀 |
|---|---|---|
| Clarify WTF issue／AI-1 整合 | 將 AI-2/3/4 的材料整合；形式候選 v0.2.1 因 `REF-TYPE-01` 未通過；保留兩個 PROV-DERIVE 修復的正面證據 | 是 acceptance／scope reconciliation；沒有 shared repo、Board success 或 P/NP inference |
| AI-2 紅隊 | 15 項 probe exit 0；重現 robust-legit receipt-only reference 被替換後仍通過 closure/admission/final 的 `REF-TYPE-01` | 顯示 envelope-aware hash closure 不等於 field-role/type-safe semantic closure；也提供 uniformity、vacuity、circularity 的反例族 |
| AI-3 形式化 | Lean 4 Phase 1 可編譯；gate、run、terminal、budget、countermodel 與 robust→standard 基礎引理成立 | 是受限的形式骨架；未包含 Mathlib、SAT、P/NP、GCC、USRT、USEG 或四層等價 |
| AI-4 工程審計 | schema、validator、projection、closure、signed evidence、replay ledger 與 parity/2-SAT fixture 的本地驗證材料 | 是可重播的工程接口；本地 PASS 不等於硬體真實性、漸近界或理論閉合 |
| AI-5 AEREC | 138 files／1,177,012 bytes 的 immutable snapshot；22/22 fixture outcomes；全樹重掃與快照批次差異為 7.56× throughput，不是 solver speedup；外部 REF-TYPE-01 rejected=false，候選 no-change | 展示治理、負例與 no-change 控制的價值；也展示 packaging／external compatibility 依賴，不構成 P/NP 證據 |

相關輸出索引：

- [AI-2 bounded red-team revalidation](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-redteam\outputs\AI-2_I0_v0.2.1_bounded_redteam_revalidation_FAIL_REF-TYPE-01_v0.1.md>)；
- [AI-3 Phase 0 formalization map](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-formal\outputs\AI3_Phase0_Formalization_Map_v0.1.md>)；
- [AI-3 Phase 1 Lean addendum](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-formal\outputs\AI3_Phase1_Lean4_Addendum_v0.1.md>)；
- [AI-4 Phase 0 engineering charter](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\AI-4_Phase0_工程章程.md>)；
- [AI-4 current candidate record](<C:\Users\kakon\Documents\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0\CURRENT-v0.2.1.md>)；
- [AI-5 AEREC handoff baseline](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-ai5\outputs\ai5-aerec-i0\AI5_AEREC_承接基線_v0.1.md>)；
- [AI-5 REF-TYPE probe report](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-ai5\outputs\ai5-aerec-i0\ai5_probe_report_ref_type_v0.2.json>)。

工程 hash 只證明某一份檔案內容與某一份 manifest 的關係；它不證明欄位所代表的語義、角色、型別或證據生成過程。`REF-TYPE-01` 正好把這個差異從口號變成可重播反例，因此應保留在學術映射中，而不是只視為工程瑕疵。

## 7. 傳統學者最可能卡住的地方

1. **縮寫先於定義。** GCC、USRT、USEG、GLC 都容易被看成新類別；實際上至少前三者的一部分內容仍是既有概念的重新切片。
2. **“global” 的量詞不清。** 它可能指跨模型、跨輸入、跨 run 或跨演算法；每一種都要寫成明確的 `∀` 或 `∃`。
3. **“universal” 的誤導。** universal machine 的存在不代表 uniform polynomial-time simulation，也不代表所有機器共享一個 exponent。
4. **終端答案與正確性混淆。** 有 terminal、輸出 bit、答案投影，與證明 `Spec(x,y)` 是三件事。
5. **路徑壓縮的循環。** 若 quotient 已知道接受與否，它只是把目標放進表示；若沒有 lift，壓縮不保證保真。
6. **robust 與 nondeterministic 的語義衝突。** fault scheduler 的 all-runs 和 NP branch 的 exists-run 必須使用不同型別。
7. **語義無損的尺度。** 它可能只對 decision output 無損，也可能要求 witness、計數、路徑或可逆重建；不指定觀測任務就沒有定理內容。
8. **“過程自由” 看起來像忽略成本。** 若 construction、representation、verification、recovery 不入帳，口號確實會掩蓋成本；若入帳，它就是審計規格而非免費捷徑。
9. **局部成功推總體成功。** 每一步 poly、每個 fixture 通過、或 median 變快，都不能自動推出 total polynomial、worst-case 或 class equality。
10. **工程證據與數學證明混層。** signature、hash、replay、external validator 能建立 provenance；它們不能代替 uniform selector、quotient theorem 或 lower bound。
11. **認知／生成語彙進入複雜度句子。** “cognitive discovery”、“genesis”、“recursive evolution” 可作設計或工程層語言，但必須翻譯成 code generation、preprocessing、online state、advice 或 controller 後才可進入定理。

## 8. 最小共同詞彙與建議替換

跨傳統學術社群時，建議只先使用下列最小詞彙：

| 應共用的詞 | 最小定義 |
|---|---|
| task / decision language | 輸入域、輸出域與 correctness relation；決策語言是 bit-output 特例 |
| algorithm | 固定有限描述的有效程序；若隨 `n` 改變，另標 nonuniform family |
| verifier / certificate | 多項式長度 witness 與可驗證關係 |
| uniform | 單一 generator／machine 對所有輸入長度工作，且其描述、生成與模擬成本明示 |
| nonuniform / advice | `A_n` 或 `a_n` 依長度改變；大小、生成與使用規則明示 |
| configuration / state | 計算的完整當前資訊；不得偷偷省略收費的 memory、precision 或 history |
| transition system / run | 狀態、轉移規則與一條執行軌跡；分支與故障 run 分型 |
| terminal / total correctness | 終止狀態；終止且滿足規格 |
| invariant | 對所有允許步驟保持的性質 |
| abstraction / quotient | 對狀態或軌跡的壓縮；要指定保留的觀測任務 |
| sound / complete / lift | 不引入假答案、不漏真答案、能從抽象證據回到具體證據 |
| maximal / fair run | 不可再延伸的 run；公平政策與 wall-clock／step 關係需另定義 |
| resource ledger | time、space、construction、update、decode、verify、recovery、code/advice 等收費欄位 |
| provenance | 證據來自哪個輸入、程式、版本、生成器與驗證步驟；hash 不自動等於語義型別安全 |
| theorem / conjecture / experiment | 已證明命題、可證偽待證命題、受限實驗結果；三者不可互換 |

建議的直接替換：

- 「全域」→ 寫成「對所有合法輸入」或「對所有 admissible runs」；
- 「通用」→ 寫成「uniform transformer」並附上生成與模擬界；
- 「無損」→ 寫成「對 decision output／witness／counting／path observation 的哪一種語義保真」；
- 「壓縮了所有路徑」→ 寫成「有何種 answer-blind quotient，如何構造、更新、解碼及證明 sound/complete」；
- 「最終帳本為 poly」→ 列出帳本欄位與是否包含 construction、advice、verification、recovery；
- 「自我演化」→ 寫成「固定 controller 的 adaptive update，帶 termination、rollback 與 worst-case cost」；
- 「閉合」→ 分別寫「定義閉合、型別閉合、證據閉合、語義閉合或定理閉合」。

## 9. 對後續研究的最低門檻

在任何人重新聲稱 `GCC⇔USRT⇔USEG` 或 GLC 與 P/NP 有關前，至少應交付：

1. 所有對象的 formal signature、輸入／輸出型別與量詞；
2. 一個固定的 uniform witness 或明確標為 nonuniform／advice；
3. 每個 abstraction 的 answer-blindness、soundness、completeness、lift；
4. 對 robust runs 的非空、最大、公平與故障模型；
5. 完整 cost ledger，包括一次性 genesis／preprocessing 與 per-input use；
6. 反例 fixture：pointwise inf、truth-table family、`m=0` circular USEG、empty-run vacuity、fairness delay、stepwise-poly／total-superpoly、wrong-role reference；
7. 形式化範圍的真實聲明：哪些 lemma 已機械驗證，哪些箭頭仍是 open；
8. 將 engineering PASS、candidate admission、theorem proof、P/NP implication 分成四種不同狀態。

最安全的研究順序仍是：

\[
  \text{GLC contract and run semantics}
  \longrightarrow
  \text{uniformity and ledger obligations}
  \longrightarrow
  \text{abstraction/lift theorem}
  \longrightarrow
  \text{only then any GCC/USRT/USEG implication}.
\]

這是研究依賴圖，不是已證明的數學箭頭。

## 10. 最終判定

本輪能夠合理成立的判定是：

- 四層框架是一個有用的跨範式研究語言與審計議程；
- GCC、部分 USRT、GLC_std 與普通 transition-system 表示，大多是已知概念的結構化重述；
- uniformity、nonuniformity、semantic lift、robust run policy、resource completeness 與 provenance typing 是必須補上的新義務；
- USEG 的非循環、決策充分、均勻多項式摘要，以及 GLC_robust 的政策相依閉合，可能是真正值得研究的數學問題；
- 目前沒有任何證據支持 P=NP 或 P≠NP，也沒有理由把工程候選的閉合狀態升格為複雜度定理。

**本報告不解 P/NP；它只把哪些句子已經是標準理論、哪些句子需要額外證明、哪些句子仍是開放問題分開。**

## 11. 凍結記錄

本檔案完成後以 SHA-256 另存於同一 `outputs` 目錄的 freeze manifest。後續若要修改，應建立新版本，不覆寫本版本；本版本的結論以本檔案內容與 manifest hash 為準。

