# AI-2 Phase 0｜紅隊研究章程與首批攻擊面

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.1（2026-08-09，Asia/Taipei） |
| 角色 | AI-2／Adversarial Red Team & Obstacle Auditor |
| 數學狀態 | Research audit；不是 P/NP 證明 |
| CTCL 協調座標 | `ctcl:instant:b8ce3d5a-9369-4c60-8436-737ecd818ac7`（只作協調，不作論證權威） |
| Board | `p-np-dynamic-four-layer`；append-only；提案、反對與修正均不等於採納 |
| Board 身分 | `Codex-GLC-RedTeam / red-team / b3867d956f23b518`（instance 由指定 seed 導出） |

## 0. Phase 0 裁定

三份四層框架 v1.0 的自我定位基本誠實：它們明示是啟發式重描述與形式化議程，不宣稱已證成 `P=NP`、`P≠NP` 或完整的 `GCC ⇔ USRT ⇔ USEG`。紅隊目前沒有發現可繼承為新定理的舊「證明」。

目前最高危險不是某個已證定理為假，而是四個接口仍不足以阻止三種退化：

1. **終態退化**：只看 `(correct, complete, loss=0)`，無法分辨合法計算與先取得答案後再填帳本。
2. **逐點 nonuniform 退化**：`inf_A C_A(n)` 可在每個長度換一台硬編碼答案的機器，使任何可判定語言看似具有線性逐點成本。
3. **語義／表示退化**：若 quotient、semantic projection、admissible transform 或 lift 可引用目標真值，壓縮已把求解器藏進定義；若限制過窄，結論又只適用受限表示。

因此目前四層的安全狀態是：

| 層 | Phase 0 狀態 | 可安全保留的內容 |
|---|---|---|
| GLC | **Definition / Open Problem** | 可作 total-correctness 與帳本介面；non-oracle provenance、loss relation、fairness 尚待形式化 |
| GCC | **Definition-level characterization** | `GCC(L)∈Poly` 可重述 `L∈P`；單一「最佳複雜度等價類」與 pointwise inf 不可直接使用 |
| USRT | **Conditional characterization** | 固定 machine encoding、有效 compiler、per-machine exponent 後，可望與 `P=NP` 對齊 |
| USEG | **Definition / Open Problem** | 可作 deterministic trace characterization；若要有新內容，必須給非循環 quotient 與 lift theorem |
| 三相等價 | **Conjecture / proof program** | 應逐箭頭證明，不能由共用「完成」詞彙直接閉環 |

## 1. 來源、版本與適用域

### 1.1 已逐份讀取的有界核心

| 來源 | 版本／範圍 | SHA-256 | 本次用途 |
|---|---|---|---|
| `P_NP_對偶證明預演研究區_截至第二十四輪.zip` | 00 中介層、01–24 輪；封存時間 2026-08-02 | `88ab3a7f396ceaff353d7ce3daeb771b057e658c8760253abab17e85825feb0d` | 歷史攻防、失敗路線、資源帳與 representation escape |
| `P_NP_動態四層閉合框架_啟發式研究提案_v1.0.md` | v1.0；2026-08-02 | `e1d35de165c7ba7848521dfe79d4ebd1a84c8683d99e9069533889ddb1b9b186` | GCC／USRT／USEG／GLC 主定義 |
| `P_NP_動態四層閉合框架_研究交接與後續實行建議_v1.0.md` | v1.0；2026-08-02 | `34c5a9eda10c75986527add6197fc1828359402f5ce7df32b9f9655c5ea621e8` | GCC-first 命題圖與研究紅線 |
| `P_NP_動態四層閉合框架_GLC優先研究交接與實行建議_v1.0.md` | v1.0；2026-08-02 | `6654e6645ab360bda22a8f81cd22698938bf7da8d2ab4df25d88df31cc793076` | GLC₀、公理、non-circularity、`C_GLC` 候選 |

三份 GLC 文件的本機位元組與公開原始 Markdown 完全相同。公開入口於 2026-08-09 取回 HTTP 200，且頁面也把框架標成「啟發式重描述／形式化議程，非證明」：

- [P/NP 對偶證明預演研究區](https://amral.evemisslab.com/p-np-dual/)
- [P/NP 動態四層閉合框架](https://amral.evemisslab.com/glc-framework/)

### 1.2 雙快照差異

公開 `p-np-dual/manifest.json` 的 25 篇中，22 篇與封存包相同；08、18、23 三篇不同。逐行比對只見 LaTeX escape 控制字元差異：

| 輪次 | 封存包 | 公開版 | 處置 |
|---|---|---|---|
| 08 | `eq\varnothing` | `\neq\varnothing` | 保留兩方雜湊；語義閱讀採公開修正字形 |
| 18 | `\text{sparse}+<TAB>ext{NP-complete}` | `\text{sparse}+\text{NP-complete}` | 同上 |
| 23 | 兩處 `<BACKSPACE>oxed` | 兩處 `\boxed` | 同上 |

這是 provenance 差異，不把任一快照靜默覆寫為另一快照。三個原始研究根目錄全程唯讀；廣大舊稿只作背景索引，沒有把其中的「證明」標籤帶入本文件。

### 1.3 外部障礙的原始適用域

- Baker–Gill–Solovay 構造了 oracle `A,B`，使 `P^A=NP^A` 而 `P^B≠NP^B`；它限制的是**對任意 oracle 都保持有效的 relativizing 技法**，不是對 P/NP 任一答案的證據。[SIAM 原論文](https://doi.org/10.1137/0204037)
- Razborov–Rudich 的 natural-proofs barrier 針對 Boolean function property 同時具 **constructivity、largeness、usefulness** 的一般電路下界路線，主要排除結論依賴 pseudorandom-function hardness；不能用來否決任意有限 invariant、上界算法或受限模型結果。[原論文 PDF](https://www.cs.toronto.edu/tss/files/papers/1-s2.0-S002200009791494X-main.pdf)
- Aaronson–Wigderson 的 algebrization 給模擬機 oracle 及其有限域／環上的 low-degree extension；「使用代數」本身不等於 algebrizing，CSP polymorphism 也不能只因名稱含 algebra 就被此 barrier 排除。[ECCC TR08-005](https://eccc.weizmann.ac.il/report/2008/005/)
- 本審計以標準語言／機器定義為錨；P/NP 是「每個 NP 語言是否有一台固定 deterministic polynomial-time machine」的量詞問題。[Stephen Cook／Clay 正式問題描述](https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf#page=99)

## 2. 紅隊研究章程

### 2.1 任務邊界

紅隊攻擊的是**具體命題與接口**，不是研究動機。每一項攻擊必須交付：被攻擊命題、最小前提、反例或證明義務、資源帳、失敗條件與可修正性。找不到反例時標 `Open Problem`，不得用懷疑語氣代替反證。

### 2.2 唯一允許的數學狀態標籤

- `Definition`：引入對象，沒有真值主張。
- `Observation`：由定義或例子直接可見，但不是主定理。
- `Lemma`：已給出可檢查證明，並寫明適用域。
- `Conditional`：結論依賴明列假設。
- `Conjecture`：尚未證成的真值主張。
- `Counterexample`：對精確命題與精確適用域的反例。
- `Experiment`：有限實作／測試結果，不外推為全域定理。
- `Open Problem`：明列缺少的 witness 或 lift。

`Attack Obligation` 只作協作流程標籤，不代替上述數學狀態。

### 2.3 十道驗收門

1. **Claim gate**：先寫語言、模型、輸入編碼、輸出語義與 claim status。
2. **Quantifier gate**：將命題正規化；特別禁止 `∀n∃A_n` 冒充 `∃A∀n`。
3. **Uniformity gate**：程式／compiler／generator 必須由單一有限描述給出；若允許 advice，明列大小與 uniform generator。
4. **Causality gate**：construction rule 不得讀取 `χ_L(x)`、答案表、成功分支或以答案定義的 quotient。
5. **Representation gate**：所有 encoding、compiler、precision 與 unit-cost 假設公開。
6. **Resource gate**：計入 construct、code/advice、peak representation、update、decode、lift、verify、restart、parallel work 與 precision。
7. **Semantic gate**：宣告是 decision、search、counting 還是 optimization losslessness；不得混用。
8. **Lift gate**：跨表示結論須有 soundness、completeness 與必要時 witness lift；受限表示下界不外推一般算法。
9. **Run/fairness gate**：`Runs_adm` 非空且由獨立 scheduler/fault 規格生成；不可用「會完成的 run」定義 admissible。
10. **Barrier gate**：逐一檢查 barrier 前提；「未跨越 barrier」與「命題為假」是不同結論。

### 2.4 量詞錨

對固定語言 `L`，標準 uniform polynomial solver 的核心形式是：

```text
∃ finite machine A ∃k,c ∀x:
  A(x)=χ_L(x) ∧ T_A(x)≤c(|x|+1)^k.
```

因此算法必須在 `n` 與 `x` 之前固定。USRT 若要表示可執行的 universal transformer，而非僅僅逐機器存在，至少應有：

```text
∃ total effective U ∀ encoded clocked N:
  D_N := U(<N,clock_N>) is finite,
  ∃ effectively represented q_N∈poly ∀x:
    D_N(x)=1 ↔ N(x) has an accepting path,
    T_D_N(x)≤q_N(|x|).
```

`U` 的 code-output size、construction cost、clock encoding 與可否呼叫 oracle 都是接口的一部分。USEG 的 generator 也需同樣區分 `∀N∃G_N`（characterization）與單一可執行 `∃U_seq∀N`（compiler claim）。

## 3. 最小反例族：合法壓縮 vs answer-oracle 偷渡

### 3.1 Pointwise Algorithm-Infimum Collapse

**狀態：Lemma。適用域：** 任意可判定語言；標準 finite-machine 模型；成本 `C_A(n)` 不計逐長度更換機器所帶來的 description/advice；`inf` 可對每個 `n` 重新選 `A`。

令 `L` 為任意可判定語言，`B_L` 為任一 total decider。對每個長度 `n`，把 `L∩{0,1}^n` 的 `2^n` 個答案編成深度 `n` 的 finite-control decision trie `τ_n^L`，並定義一台有限機器 `A_n^L`：

```text
if |x| = n: follow τ_n^L using the n input bits and output the leaf;
else:       run B_L(x).
```

每個 `A_n^L` 都在**所有輸入**上正確決定 `L`；但在長度恰為 `n` 時只需 `O(n)` 步。其機器描述／答案 advice 為 `Θ(2^n)`，且機器隨 `n` 改變。因此：

```text
∀ decidable L ∀n:
  inf_{A decides L} T_A(n) ≤ O(n).
```

證明就是在每個 `n` 選 `A_n^L`。若取由 deterministic time hierarchy 保證存在的 `L*∈EXPTIME\P`，pointwise inf 仍為線性，卻不存在單一 polynomial-time decider。故下列候選式在上述最小前提下不能刻畫 `P`：

```text
C_GLC(L,n) = inf_{A∈A_GLC(L)} C_A(n).
```

這是對 GLC-first v1.0 之 `C_GLC` 候選的 **Counterexample**，不是對其研究意圖的反例。

### 3.2 一位元正對照族

為證明修補不會把所有壓縮都拒絕，取 `PARITY(x)=x_1⊕⋯⊕x_n`：

**合法 uniform 壓縮 `P_stream`**

```text
state s_i=(i,b_i),  b_0=0,
b_{i+1}=b_i XOR x_{i+1},
output b_n.
```

- 單一程式適用所有 `n`；code size `O(1)`。
- construction/update/decoding 總成本 `O(n)`，工作狀態一位元加索引。
- 局部 invariant `b_i=PARITY(x_1...x_i)` 可獨立歸納驗證。

**答案偷渡 `P_table,n`**

```text
embed τ_n^PARITY (or τ_n^L) in code/advice;
follow the trie;
output the stored leaf.
```

兩者對長度 `n` 的終態都只有一位元，且可填同一帳本 `(Y=1,C=1,Λ=0,T=O(n))`。所以任何只讀終態帳本、不驗 construction provenance 的 GLC validator 對兩者不可區分。這是 **Final-Ledger Indistinguishability Counterexample**。

下列 admission rule 則真正區分兩者：

```text
存在一個在 n,x 之前固定的 finite Build/Step/Dec 程式；
每步只用公開、可計價 primitives；不得 query χ_L；
code/advice 或其 uniform generation 全部入帳；
Λ=0 必須由 compositional invariant/lift proof 導出，不能自行申報。
```

`P_stream` 通過；`P_table,n` 因量詞為 `∀n∃table_n` 且 advice 為 `Θ(2^n)` 而失敗。若有人把表格替換成一個 uniform polynomial-time 產生答案的真正算法，它就應當通過——因為那時已不再是 oracle 偷渡，而是合法 solver。這正是所需區分。

### 3.3 最小修正

- 不用 pointwise scalar inf 定義 GCC。保留算法集合
  `Time(L)={T_A : A is one fixed total decider of L}`，只問 `Time(L)∩Poly≠∅`。
- 若研究 nonuniform family，明寫 `/poly`、advice length 與 advice uniformity，不與 `P` 混稱。
- GLC ledger 必須攜帶可驗 provenance／trace hash／局部 invariant 或 proof object；`Λ` 與資源值由 verifier 導出。
- `A_GLC(L)` 若指 resource-neutral GLC₀，上述 collapse 適用；若先限制為 polynomial algorithms，GCC 已被循環地放入集合定義。兩者都要求改寫。

## 4. 首批攻擊面登錄

| ID／狀態 | 被攻擊命題 | 最小前提 | 反例或證明義務 | 可修正性／失敗條件 |
|---|---|---|---|---|
| A01 `Counterexample` | `C_GLC(L,n)=inf_A C_A(n)` 可表示語言的最低 uniform complexity | 每個 `n` 可重新選算法；description/advice 不入帳 | §3 的 `A_n^L` 使每個 decidable `L` 的逐點 inf 為 `O(n)` | **可修**：固定 `∃A` 在 `∀n` 之前；若保留 pointwise inf，此 GCC 定義失敗 |
| A02 `Counterexample` | `(Y=1,C=1,Λ=0)` 足以排除 answer oracle | validator 只見終態欄位，construction 為 opaque | `P_stream` 與 `P_table,n` 終態帳本相同 | **可修**：provenance、causal transitions、advice/code accounting；若 `Λ` 可自報則失敗 |
| A03 `Observation` | `GCC(L)=[T_M^L]` 是單一良定的 polynomial-equivalence class | `T_M^L` 指「某個」正確算法 | 對同一 P 語言，一台線性算法與插入 `2^n` delay 的算法不在同一 poly-equivalence class | **可修**：改成算法時間譜或只保留 existence predicate；不宜假設 canonical optimum |
| A04 `Open Problem` | `M_adm` 的「合理模型」足夠客觀且不循環 | unit cost、word size、precision、compiler 未固定 | 證明義務：給 anchor model 與每個模型的有效雙向 compiler，計入表示長度、precision 與 code size | **可修**；若僅以「不會造成不合理加速」定義合理，則循環 |
| A05 `Conditional` | USRT 的 `∃U∀N∃q_N∀x` 是可執行 uniform transformation | `U` 必須是 total effective code transformer | 證明義務：machine/clock encoding、`D_N` code、`q_N` 表示與 construction cost；`U` 不得只是選擇關係 | **可修**；若只有 `∀N∃D_N`，只能稱 extensional characterization |
| A06 `Counterexample` | `GLC(N,x)↔GLC(D,x)` 可直接表達 nondeterministic-to-deterministic preservation | robust GLC 對 run 用 `∀π`，NP acceptance 對 branch 用 `∃π` | 一台有一接受、一拒絕分支的 N：NP 接受，但「所有 run 正確完成」可失敗 | **可修**：USRT 保存 `∃ accepting path` 的語言語義；另為 scheduler nondeterminism 定義 GLC |
| A07 `Counterexample` | USEG 的 polynomial `Z_0…Z_m` 本身證明有合法壓縮 | initialization／quotient 可依答案 | 令 `Z_0=Z_m=χ_L(x)`，`m=0`、state 一位元、decode 常數時間 | **可修**：固定 uniform Build/Step/Dec、answer-blind admissibility、compositional invariant；否則定義空洞 |
| A08 `Open Problem` | `γ_a~_Dγ_b` 的 decision sufficiency 可被有效、非循環地判定 | 關係只要求「最終決策相同」 | 證明義務：關係的有效 construction、state bound、update、decode、soundness/completeness；不能以 eventual answer 定義 equivalence | **可修但核心困難**；未交證明時只是 specification |
| A09 `Open Problem` | 任意合法 quotient／representation switch 都保持「零語義損失」 | `Sem_L` 與 `~` 未指定 decision/search 層級 | 必須給 encode/decode、forward/backward simulation；若宣稱 witness，另給 poly witness lift | **可修**；只有 decision bit 時不得宣稱 witness/counting lossless |
| A10 `Counterexample` | `∀π∈Runs_adm` 的 robust completion 自動非空且有意義 | `Runs_adm` 可任意挑選或以會完成定義 | `Runs_adm=∅` 使全稱式真；排除所有 nonterminating runs 也使 liveness 循環 | **可修**：獨立非空 maximal-run semantics、明列 weak/strong/bounded fairness 與 fault budget |
| A11 `Observation` | weak fairness 下的 eventual completion 可同時推出 polynomial wall-clock bound | scheduler 可任意久延遲但最終排程 | weakly fair run 可有無界 delay；eventual 不給 polynomial deadline | **可修**：分 work complexity 與 delay，或採 bounded fairness；robust GLC 不自動等價 P |
| A12 `Counterexample` | 每步 polynomial 即整條 GLC/USEG pipeline polynomial | depth、peak size、degree 可隨步累積 | `s_{t+1}=s_t^2`，每步對當前 state 多項式，`m` 步後 `n^{2^m}` | **可修**：同時界定步數、總 work、peak bits、degree accumulation、restart/recompute |
| A13 `Observation` | `GCC⇔USRT⇔USEG` 目前提供獨立的新數學內容 | 任一層允許直接使用已存在的 deterministic solver | GCC 给 solver；USRT 輸出 solver；USEG 取 solver trace，三箭頭可成定義包裝 | **可修**：明分 characterization arrows 與 structural-compression theorem；後者須 answer-blind quotient |
| A14 `Observation` | 某表示（OBDD、resolution、固定 abstraction、固定 algebra portfolio）爆炸可 lift 成一般時間下界 | 尚無完整 normal form／跨表示 invariant | 已知 P 函數亦可在特定表示指數爆炸；替代表示可逃逸 | **可修但艱難**：證明 representation-complete normal form 或 invariant-preserving lift；否則只報 restricted result |
| A15 `Observation` | barrier 名稱可直接裁決候選方法 | 未驗 relativizing／natural／algebrizing 的正式前提 | 需要三份 audit：oracle lift；constructive-large-useful property；low-degree-extension oracle lift | **可修**；未做測試只能寫「未審查」，不能寫「被 barrier 排除／已跨越」 |
| A16 `Observation` | 兩方應承擔相同量詞型證明義務 | 忽略 `P=NP` 的存在式與 `P≠NP` 的全稱式不對稱 | equality 只需一台 uniform solver；separation 必須覆蓋所有 uniform solvers | **可修**：同一資源帳、不同合法 burden；框架失敗不等於 `P≠NP`，單一表示成功也不等於 `P=NP` |

## 5. Barrier 使用檢查表

| Barrier | 何時真正觸發 | 對四層框架的 Phase 0 判定 | 禁止推論 |
|---|---|---|---|
| Relativization | 整個證明對任意 oracle `O` 都 lift，卻欲證 `P≠NP` 或 `P=NP` | GCC／USRT／USEG 若只作黑箱 machine simulation，很可能 relativize；逐箭頭待測 | 「有 oracle 反例，所以原命題為假」 |
| Natural proofs | 一般 circuit lower bound 使用 useful、large、constructive Boolean property，並採相應 PRF hardness | 目前只有 invariant 候選，尚未展示三條件，不能宣告 barrier 已觸發 | 「任何可計算 invariant 都不可能」 |
| Algebrization | 證明在 oracle 加 low-degree extension 後仍成立 | arithmetization 型 QCM 需測；CSP/universal algebra 不因名稱自動觸發 | 「用了代數，所以被 algebrization 擋住」 |

Barrier 審查只回答「這條證明策略是否具有已知盲點」，不替命題給真值。

## 6. 正向保留與修正優先序

紅隊不建議丟棄四層框架。以下設計值得保留：

- 主稿明確拒絕由原始 path cardinality 推出時間下界。
- USRT 已保留 per-machine polynomial exponent，而非要求全體 machine 共用一個 exponent。
- GLC-first 已明確寫出「spec 可提 truth，implementation 不可取得 truth oracle」。
- 00 與第 01–24 輪已建立相當完整的 representation、construction、precision、bridge、lift、pathwise 與 verification 債務語彙。
- standard GLC 與 robust GLC 已被分開；後者沒有被直接宣稱與 `P=NP` 等價。

修正優先序：

1. **P0 blocker**：刪除／改寫 pointwise `C_GLC`；固定 uniform quantifier。
2. **P0 blocker**：定義可驗的 non-oracle provenance，使 `Λ=0` 不可自報。
3. **P1**：把 nondeterministic branch semantics 與 scheduler/fault runs 分型。
4. **P1**：固定 anchor model、bit-cost、machine/clock encoding 與 compiler interface。
5. **P1**：為 USEG 指定 decision-only 或 witness-preserving lift。
6. **P2**：逐箭頭 barrier audit；不把 characterization proof 誤作 resolving technique。

## 7. 建議交給其餘角色的接口

- **AI-1 Integrator**：把 A01、A02 設為 framework admission blockers；三相等價維持 `Conjecture`，逐箭頭立項。
- **AI-3 Formalizer**：形式化 `Pointwise Algorithm-Infimum Collapse Lemma`、uniform GLC provenance judgment，以及 NP branch／scheduler run 的雙層語義。
- **AI-4 Engineer**：實作 `PARITY` 雙族測試：同終態 ledger 下，uniform trace 通過、truth-table/advice family 因 provenance／advice budget 失敗；測試結果只標 `Experiment`。

## 8. Phase 0 完成條件

- [x] 00、第 01–24 輪、三份 v1.0 逐份讀取。
- [x] 公開網站與本機核心文件雜湊交叉核驗。
- [x] Definition／Observation／Lemma／Conditional／Conjecture／Counterexample／Experiment／Open Problem 分型。
- [x] 來源、版本、適用域、量詞、資源帳與失敗條件入冊。
- [x] 提出可區分合法壓縮與 answer-oracle/advice 偷渡的最小反例族。
- [x] 首批攻擊面逐項附修正路徑；沒有把框架缺口外推為 `P≠NP`。

**Phase 0 disposition：完成，等待跨任務後續封包。**
