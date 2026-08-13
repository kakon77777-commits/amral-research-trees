# AI-7 盲審對照與橋接報告 v2.0

**階段：第二輪「對照與現況刷新」**  
**日期：2026-08-09（Asia/Taipei）**  
**狀態：凍結候選；不覆寫 v1.0**  
**用途：把 AI-6 傳統複雜度盲審與後續五線的實際形式／工程進度逐條對照。**

## 0. 邊界與總判定

本輪已讀取 AI-6 凍結盲讀報告，並重新刷新 `Clarify WTF issue`、AI-2、AI-3、AI-4、AI-5 的最新 thread 狀態與直接交付。所有閱讀與本報告建立均為唯讀對照；沒有聯絡 AI-1 至 AI-5、沒有發布 Board、沒有修改研究來源，也沒有修改已凍結的 [AI-7 v1.0 映射報告](C:\Users\kakon\Documents\Codex\2026-08-09\pnp-scholar-bridge\outputs\AI-7_跨範式映射報告_v1.0.md)。

### 結論先行

**AI-6 的 `major revision` 判定仍然正確。**後續成果讓形式骨架、工程驗證接口與反例治理明顯變得更精確，但沒有把 GCC⇔USRT⇔USEG 變成定理，沒有把 GLC 變成新的已定義複雜度類，也沒有產生 P=NP 或 P≠NP 結論。

本輪最重要的現況更新有五點：

1. AI-6 對 GCC、USRT、USEG、GLC 分層、uniformity、answer-dependent quotient、total correctness 與 robust semantics 的主要批評，經後續實作與形式化反覆支持，而不是被推翻。
2. `PROV-DERIVE-01` 把「簽名／重播／資源折疊不能只靠自報」從抽象風險變成可重播工程反例；v0.2.1 確實修掉兩個該族負例。
3. `REF-TYPE-01` 又把問題推深一層：即使 signature、hash closure、structural/semantic/admission/final 全部通過，receipt-only reference 仍可指向錯誤 role/type 的 artifact。v0.2.1 因此維持 FAIL；這是證據閉合接口的 blocker，不是 P/NP 結果。
4. AI-4 的 v0.2.2 已形成新的 frozen candidate，加入 role-bearing edges、expected type/version/mode、signed/derived operational map、同源 bytes schema API、canonical domain 與 derived context gates；但它目前仍是 `CANDIDATE_UNPROMOTED / pending independent acceptance`。這些是工程候選修補，不是 theorem closure。
5. AI-5 的 AEREC 線實際證明的是「驗證吞吐與反例治理可以演化」：在固定 22 fixtures 上，immutable snapshot 相對逐筆全樹重掃為 7.56× validation-throughput；它不是 solver speedup、worst-case improvement、asymptotic theorem 或 P/NP evidence。

## 1. 證據與狀態索引

### 1.1 已凍結的前提

| 對象 | 目前狀態 | 本輪如何使用 |
|---|---|---|
| AI-7 v1.0 | 已凍結，SHA-256 `2DB3AAAF2D3603DD79D78E163575AA47C13A101CE4E6A70821E62883F7944959` | 只作前一輪坐標基線，不覆寫 |
| AI-6 盲讀報告 | 已讀、外部檔案未修改，SHA-256 `A8C364583EAA82BE459341A0955817E0EB415C625535FD0B7E9E70A3D31232E4` | 逐條對照 |
| v0.2.1 candidate | `FAIL / REF-TYPE-01`，frozen counterexample snapshot | 保留其正面修補與 blocker，不回溯改判 |
| v0.2.2 candidate | 本地 self-test pass；`CANDIDATE_UNPROMOTED / pending independent acceptance` | 只作現況候選，不作已驗收結果 |

### 1.2 五線刷新

| 任務 | 最新 thread 狀態 | 最新直接交付與判定 |
|---|---|---|
| `Clarify WTF issue` | active；目前承接 AI-4→AI-1 的 v0.2.2 二次驗收請求 | AI-1 對 v0.2.1 的二次報告仍為 FAIL；R1 將 schema API 與 `-0` 分類精確化；v0.2.2 尚待獨立回覆 |
| AI-2 紅隊 | active；已接收 v0.2.2 frozen candidate，正在隔離副本重跑與找 sibling bypass | 直接報告仍是 v0.2.1 `FAIL / REF-TYPE-01`；尚無 v0.2.2 最終獨立報告 |
| AI-3 形式化 | active；已接收 v0.2.2，正在核對 formal boundary、mutation probes 與 robust singleton scope | 直接交付仍是 Lean Phase 1 compiled artifact；未宣稱 v0.2.2 或四層 theorem |
| AI-4 工程審計 | active；v0.2.2 candidate bytes 已凍結，等待外部驗收 | 31 fixtures、14/14 + 11/11 + 15/15、1500 個固定 seed 2-SAT 小例、72 outputs byte-identical；仍 unpromoted |
| AI-5 工程協作 | idle；第一階段 AEREC 承接完成 | 以 v0.2.1 作 negative control；22/22 fixtures、138 files/1,177,012 bytes snapshot、7.56× validation throughput；未把 v0.2.2 當已驗收父代 |

直接交付索引：

- [AI-6 傳統學者盲讀報告](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-scholar-traditional\outputs\傳統學者盲讀報告_P_NP動態四層閉合框架_v1.0.md>)；
- [AI-2 v0.2.1 bounded red-team report](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-redteam\outputs\AI-2_I0_v0.2.1_bounded_redteam_revalidation_FAIL_REF-TYPE-01_v0.1.md>)；
- [AI-3 Phase 1 Lean addendum](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-formal\outputs\AI3_Phase1_Lean4_Addendum_v0.1.md>)；
- [AI-4 v0.2.2 current candidate](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0\CURRENT-v0.2.2-candidate.md>)；
- [AI-4 v0.2.2 validation report](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0\VALIDATION-REPORT-v0.2.2-candidate.md>)；
- [AI-4 v0.2.2 REF-TYPE reproduction](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0\REF-TYPE-01-REPRO-v0.2.2.md>)；
- [AI-5 AEREC baseline](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-ai5\outputs\ai5-aerec-i0\AI5_AEREC_承接基線_v0.1.md>)；
- [AI-5 latest REF-TYPE probe](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-ai5\outputs\ai5-aerec-i0\ai5_probe_report_ref_type_v0.2.json>)；
- [AI-1 v0.2.1 second acceptance](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-integrator\outputs\AI-1_I0_v0.2.1_二次唯讀驗收_FAIL_REF-TYPE-01_v0.1.md>)；
- [AI-1 classification R1](<C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-integrator\outputs\AI-1_I0_v0.2.1_紅隊追加分類_R1_v0.2.md>)。

## 2. 對照標記

以下逐條使用五種判定：

- **[A／同意]**：AI-6 的批評被後續證據支持，AI-7 仍採納。
- **[M／盲讀缺後續事實]**：AI-6 在只讀 v1.0 的限制下沒有看見後來的工程／形式結果；批評本身不因此失效。
- **[F／真補缺]**：後續成果確實關閉一個可重播的定義、接口或工程缺口，但只在明示範圍內成立。
- **[N／非完全補缺]**：看似補上，實際仍是 Definition、Experiment 或 Engineering，不滿足 AI-6 要求的普遍 theorem obligation。
- **[D／更深問題]**：後續紅隊或工程線暴露出 AI-6 在盲讀階段無法觀察的更深層風險。

## 3. 逐條盲審對照

### A01. 總判定：可作研究綱領，定理稿 major revision

**AI-6 判斷：**框架可理解、有自我限制，但尚未達到 characterization theorem；投稿定理稿應 major revision。

**對照：**[A／M／F] 後續沒有推翻此判定。AI-3 的 Lean artifact、AI-4 的 candidate、AI-5 的 throughput 都是範圍受限的正面結果；AI-2 與 AI-1 反而以 `REF-TYPE-01` 證明工程接口仍有 blocker。後續真正補的是「可以把問題拆成可機械檢查／可重播的子義務」，不是「已完成四層 characterization」。

**現況判定：**AI-6 的 major revision 仍是本輪總判定；若文字定位為研究綱領或 formalization agenda，可以繼續；若宣稱新複雜度理論或 P/NP characterization，仍不可接受。

### A02. GCC 大致是 P 的跨模型重述

**AI-6 批評：**若固定模型編碼並有 uniform polynomial simulation，GCC membership 就是 `L∈P` 的跨模型表述；`T_M^L` 若非最小成本或固定 witness，甚至不是語言不變量。

**對照：**[A／N] AI-3 後來明確將 resource-neutral 與 bounded 分軸，並把 pointwise infimum/nonuniformity 列入 theorem ladder；AI-4 也把 ledger、construction、advice、code bytes 列為工程欄位。但這些沒有交付 AI-6 要求的 model family、encoding、pairwise simulator 或 GCC-1/GCC-2 定理。

**真正補上的部分：**把「GCC 不能只靠一句 admissible model」轉成可驗收 schema／cost 欄位與反例要求。

**仍未橋接：**未證明 `\mathfrak M_adm` 的正式閉包、有效 enumeration、simulation overhead 或 GCC 與標準 P 的等價。GCC 仍應暫譯為「P 的模型／資源坐標」。

### A03. admissible model 不由「合理」二字自動得到 invariance

**AI-6 批評：**有限描述、uniform、無 oracle、無免費無限精度與無超多項式 advice，仍不足以排除 unit-cost SAT primitive；必須另交 simulation theorem。

**對照：**[A／D] 後續工程把同一件事具體化為 no hidden power、code/advice/precision/resource ledger 與 positive/negative fixtures，但仍沒有建立模型級 simulator。v0.2.2 的「固定 PARITY／2-SAT transition」只是 candidate validator 的 mechanism family，不是對所有 admissible machines 的 simulator。

**分類：**[N] Definition obligation + Engineering observation，未達 theorem。

### A04. USRT 需要真正的 uniform compiler

**AI-6 批評：**`∀N∃D_N`、`∃U∀N`、固定 exponent、combined-input runtime 與 compiler cost 不同；不可計算的 choice function 不能稱 uniform transformer。

**對照：**[A／M／N] AI-3 將 uniform selector composition 與 quantifier ladder 保留下來，AI-4／AI-5 將 immutable candidate identity、generator output hash 與 construction cost 放進工程治理；但沒有任何後續交付 `U(⟨N⟩)` 的 general compiler theorem。AI-4 的 72 generated files byte-identical 只表示同一 fixture producer 可重播，不表示從任意 NTM 產生 deterministic decider。

**仍未橋接的 theorem obligation：**固定 machine encoding、可計算／可計價的 `U`、`D_N` 的 code size、初始化成本、combined-input 或 per-N runtime，以及 acceptance soundness/completeness。

### A05. rate cone 是重參數化，不是新的 dynamic invariant

**AI-6 批評：**`R_A(n)=1/(1+T_A(n))` 依賴 clock refinement；inverse-polynomial cone 沒有自動提供 machine-independent local velocity。

**對照：**[A／N] 後續沒有提出反證。AI-5 的 7.56× 是 wall-clock validation throughput，反而強化了「速度指標必須標明測量層級」的要求；它沒有變成 rate theorem。

**現況：**rate 可作記號與 cone 分類，但不能把 throughput、median 或 reciprocal runtime 寫成 P/NP separation/equality evidence。

### A06. NTM path semantics 不能直接套 deterministic single trace

**AI-6 批評：**`S_N(x,t)` 對 NTM 不是唯一狀態；NP acceptance 是 existential branch，不能把每一分支都當成 `χ_L(x)`；hitting time 的 min/max/aggregate semantics 必須指定。

**對照：**[A／F／D] AI-3 的 Lean Phase 1 只形式化固定 algorithm witness 與 standard/robust run policy，並建立 standard-not-robust countermodel；AI-4 v0.2.2 的 robust I0 明確聲明使用 singleton deterministic finite run，scheduler/fault nondeterminism 在候選外。這確實封閉了一個「不要假裝已處理所有 robust runs」的接口邊界，但也直接確認 AI-6 的核心批評：一般 NTM／fault run semantics 尚未完成。

**更深問題：**工程中的 `robust` mode 目前是 candidate policy metadata 與 bounded replay gate；它不是對 NP existential path 的全稱轉換，也不是一般 resilient computation theorem。

### A07. USEG 弱版會退化為 solver trace，強版才可能有新內容

**AI-6 批評：**若 USEG 只要求一條 polynomial deterministic sequence 最終答對，它就是 P solver 的另一種表示；若要求所有 histories 的受限 quotient，必須正式限制摘要類別。

**對照：**[A／同意／未解] 後續沒有產生強 USEG theorem。AI-4 的 trace、event、projection、validator 是對「一份工程 record 如何被驗收」的摘要，不是對任意 NTM computation histories 的 decision-sufficient quotient。AI-5 的 immutable bundle snapshot 更是驗證資料的 content-addressed cache，不是計算路徑壓縮。

**現況：**AI-6 提議的二選一仍是正確路線：要麼承認 USEG_weak 是 solver trace interface；要麼對一個明確 representation class、local transition、uniform generator、decode 與 lift theorem 做強版研究。

### A08. quotient／abstraction 的非循環性與 lift

**AI-6 批評：**`\sim_D` 的 domain、可計算性、canonical encoding、answer-blindness、transition closure、soundness/completeness/lift 都未定義；把所有 paths 依答案分組是 circular。

**對照：**[A／F／D] 後續把這個抽象問題在工程證據層具體化：`REF-TYPE-01` 顯示「hash closure」沒有保證 role/type/semantic binding；v0.2.2 以 role-bearing edges、validator-derived maps 與 field context 修補已知 substitution family。這是真正的工程缺口修補，但不是 computation-history quotient 的 lift theorem。

**關鍵區分：**artifact closure ≠ path quotient；reference role binding ≠ semantic abstraction preservation。兩者都談「保留必要關係」，但對象、證明義務與量詞不同，不能互相冒充。

### A09. GLC0、GLCpoly、GLCstd、GLCrobust 應正交分層

**AI-6 批評：**resource-neutral、polynomial resource、standard 與 robust 尚未整理成不衝突層次；建議 `GLC0`、`GLCpoly` 與 `GLCstd/robust` 分軸。

**對照：**[F] AI-3 已實際編譯一個四格 applicability matrix：standard/robust × neutral/bounded；`account` 在兩個 resource regime 都適用，`budget` 只有 bounded 適用；`runClassNonempty` 對兩種 mode 都適用。這是對 AI-6 要求的局部真正補缺。

**仍未補足：**Lean 中的 `zeroDebt` 是 parameter，不是一般 semantic obligation basis；fairness 是抽象 predicate，未選 weak/strong/bounded；`SemanticValidate`、`DerivesRecord` 與 resource-bounded GLC 沒有整體機械化。因此這是 Definition/Formal scaffold，不是 GLC hierarchy theorem。

### A10. semantic losslessness 不能只寫 `Λ=0`

**AI-6 批評：**`Λ=0` 若只表示最後答對，與 correctness 重複；若要求每個 state 與完整 computation 等價，又可能過強；應改以 task-relative abstraction、concretization、soundness/completeness 或 invariant。

**對照：**[A／D／未解] AI-4 的 projection、trace、derived gate 與 role map 讓「哪些欄位保留、哪些由原材料重算」更清楚，但仍沒有選定 computation-level `Sem_L`。AI-2 的 `REF-TYPE-01` 還揭露另一種 loss：即使 final record 的 visible projection 不變，receipt-only operational semantics 可能變掉。

**判定：**後續補了 provenance/field-binding 的工程語義，沒有補出一般 semantic losslessness 定義或 abstraction theorem。這仍是雙方未橋接的核心詞。

### A11. final ledger 是 acceptance record，不自動是 complexity object

**AI-6 批評：**ledger 是 trace function、proof witness 還是 meta-level audit record 未定；`Resource∈Poly` 的量化、sequence、compiler cost 與 ledger 產生成本都要正式化。

**對照：**[F／N] AI-4 確實把 construction、update、decode、verify、recovery、code/advice/proof bytes 等列入工程 schema，並由外部 validator 導出部分 facts；AI-5 也把 snapshot indexing 與 validation wall time 分開量測。這是 evidence ledger 的實戰閉合，不是 complexity ledger calculus 的 theorem。

**更深問題：**`REF-TYPE-01` 證明「有一份一致、可簽、可閉包的 receipt」仍不等於「receipt 所稱的 evidence semantic role 正確」。所以 ledger 的欄位存在、hash 完整與語義正確必須分三層。

### A12. robust run 的 nonempty、maximal、fairness 與 vacuity

**AI-6 批評：**robust property 依 fault/scheduler policy；空 run family 造成 vacuity；不公平 scheduler 破壞 eventual completion；recovery overhead 與 uniform budget 必須列明。

**對照：**[F／A] AI-3 已機械化 `runClassNonempty`、maximal/fair 的 mode 分界與 standard-not-robust countermodel；AI-4 v0.2.2 將 robust I0 限定為 singleton deterministic finite run，並明說 scheduler/fault nondeterminism 在 candidate 外。

**判定：**這是「安全地縮小 scope」的真補缺，不是 robust theorem。AI-6 要求的 general all-admissible-run semantics、fairness choice、fault budget、wall-clock bound 仍未完成。

### A13. GLC-first 是研究依賴，不是 implication

**AI-6 批評：**文件已自稱箭頭是 research dependency；傳統讀者仍可能誤把它當數學 implication。

**對照：**[A] 後續所有工程文件都保留「no P/NP inference」「no Board success」「candidate unpromoted」；AI-3 也把四層 arrows 留在 Open Problems。這個語義邊界被維持，而非被證明成定理。

**現況：**`GLC→{GCC,USRT,USEG}` 仍只能表示研究順序／驗收依賴圖，不能寫成已證明的 logical entailment。

### A14. genesis/use、preprocessing、construction 與 representation cost

**AI-6 批評：**一次性編譯或 preprocessing 不能因為稱為 genesis 就從 polynomial claim 消失；需要拆 `T_compile`、code size、online `T_D(x)`。

**對照：**[F／N] AI-4 的 candidate ledger 已將 construction、generation、lift、verify、restart、precision 與 code/advice bytes 變成欄位；AI-5 也把一次 snapshot build 與每筆驗證分開。然而這些是被測試的成本接口，尚未有一般 `T_compile` theorem 或 P/poly exclusion theorem。

**現況：**AI-6 的成本審查完全保留。任何「單次建立後反覆使用」的結果，仍需說明 preprocessing 是否屬模型允許資源、是否依 `N`／`n`／instance 變動，以及生成成本是否可均勻支付。

### A15. formalization 的成功只對已形式化命題負責

**AI-6 批評：**Lean／Coq 編譯成功不能替代論文中較強直覺；若 solver、quotient 或 answer 已被當參數，證明不代表 P=NP。

**對照：**[F／A] AI-3 自己明確限定：無 Mathlib、SAT、P/NP、GCC、USRT、USEG；`good_terminal_unfold` 是 definitional unfolding，`robust_to_std` 是 elementary conditional lemma；Axiom audit 無 custom axiom。這是後續最清楚的自我校準之一。

**判定：**AI-6 的要求已得到「範圍聲明」的真補缺，但尚未得到 theorem-level bridge。形式化 artifact 是 formal scaffold，非四層 closure。

### A16. relativization、natural proofs、algebrization 尚未真正進入

**AI-6 批評：**材料列出 barriers，但沒有 lower-bound/equality theorem 或 barrier analysis；應標 `not yet engaged`。

**對照：**[A] 後續沒有新增 barrier proof。AI-2 的反例與 AI-4 的 candidate 都是 admission/provenance 層，不是 circuit lower-bound argument；AI-5 的 AEREC 也沒有進入 oracle world、natural property 或 algebrization。

**現況：**AI-6 的 `not yet engaged` 仍是精確標籤。不得用「已排除某些工程捷徑」宣稱繞過三大 barrier。

### A17. P/poly／nonuniformity 是最直接的共同風險

**AI-6 批評：**每個 `N` 的不可計算 `D_N`、每長度 quotient table、lookup table、answer-dependent relation、advice 或超強 primitive 都可能偷入 P/poly。

**對照：**[F／D] AI-2 的 PARITY uniform streaming vs per-length truth-table 對照，直接把「相同 final ledger 不代表 uniformity」變成可重播分離；AI-4 v0.2.2 的 `problem.size`、failure-frontier、answer-access derived gates 又把 context mirror 風險納入。這是真正增加了可操作的負例，但沒有給出 P/poly separation theorem。

**仍未橋接：**engineering 的 `answer_access` gate 如何翻成 machine-level no-advice/no-oracle 定理？目前只有 bounded validator rule，沒有一般量詞。

### A18. AI-6 建議的正例／破壞性反例套件正在變成工程 corpus

**AI-6 建議：**addition、sorting、reachability、2-SAT/Horn-SAT/XOR-SAT、bounded-treewidth；以及 branching P、answer-dependent quotient、hidden preprocessing、nonuniform family、unit-cost superprimitive、lossy-but-accidentally-correct、permanent fault、NP yes-input with rejecting branches。

**對照：**[F／N] AI-4 已將 PARITY、2-SAT、standard/robust × neutral/bounded、self-report、unknown、circular、tampered record/trace、PROV-DERIVE、REF-TYPE 等納入 fixtures；AI-5 將 negative corpus 與 no-change 帶入 AEREC。這確實補了「反例不是口頭提醒」的工程缺口。

**限制：**現有 corpus 仍是 bounded examples。它沒有涵蓋一般 SAT、一般 NTM quotient、永久 fault 的 formal impossibility 或所有 unit-cost model。`31 fixtures` 是 coverage count，不是 general completeness proof。

### A19. theorem ladder 與箭頭拆分

**AI-6 建議：**將 GCC、USRT、USEG、GLC 分成 definition、standard theorem、conditional theorem、conjecture、counterexample、open；尤其分開 `P=NP⇒USRT_uniform`、`USRT_uniform⇒P=NP`、weak/strong USEG 與 GLC0/robust。

**對照：**[F] AI-3 Phase 0 的 theorem ladder 已把 robust→standard、pointwise inf collapse、uniform selector composition、GLC poly characterization 與四層 arrows 分級；Phase 1 實際只編譯了最小 GLC0 core。AI-1／AI-4／AI-5 的報告也用 `Experiment`、`Candidate`、`FAIL`、`unpromoted`、`no-change` 分開 epistemic status。

**判定：**分類架構是真補缺；箭頭本身沒有補成 theorem。這是目前最接近 AI-6 建議、也最容易被誤讀成「已完成」的部分。

### A20. 下一版應先做小而完整的 formal core，USEG 必須二選一

**AI-6 建議：**先固定 deterministic TM 的 terminal、correctness、termination、abstraction relation、GLC0、poly refinement、正例與 answer-oracle 反例；USEG 要承認弱版重述，或定義強版 representation class。

**對照：**[F／N] AI-3 已完成最小 deterministic GLC0／run／gate／countermodel core；AI-4／AI-5 完成了小型 PARITY／2-SAT／I0 engineering slice。但仍沒有 sorting/reachability 的完整 semantic abstraction theorem，也沒有強 USEG class。

**現況：**AI-6 的下一版路線仍是最保守、最可橋接的路線。後續工程不應被描述為已經完成它；只能說已經提供候選 fixture 與 formal interface。

## 4. 後續成果真正補上的缺口

### 4.1 AI-3：補上「最小形式語義的可編譯骨架」

AI-3 Phase 1 真正完成的內容是：

- `TaskSpec`、固定 system witness、`init/step/halt/emit` 分離；
- partial trace、prefix、proper prefix、maximal run 的最小結構；
- standard 與 robust 的 run-class nonempty semantics 分開；
- `pass/fail/unknown/notApplicable` 四值 gate，且 unknown/fail fail closed；
- standard/robust × neutral/bounded applicability matrix；
- terminal-without-output countermodel；
- standard-valid but robust-invalid countermodel；
- robust→standard 的條件式 inclusion lemma；
- clean build、archive round-trip 與 no-sorry/no-custom-axiom audit。

這些確實把 AI-6 說的「語義對象不能只留在自然語言」往前推了一步。它沒有完成：

- 一般 fairness policy；
- zero-debt 到 recovery/obligation recurrence 的連接；
- SemanticValidate／DerivesRecord 的整體機械化；
- GCC model invariance；
- USEG quotient/lift；
- P/NP 或四層 arrows。

### 4.2 AI-2／AI-1：把 provenance 風險變成反例與分類

AI-2 的 v0.2.1 bounded report 與 AI-1 的獨立重驗真正補了三件事：

1. `PROV-DERIVE-01` 的 `states=999` 與 fabricated transition digest 在有效 signature 下仍會被 derived resource/transition gates 拒絕；
2. `REF-TYPE-01` 將 v0.2.1 的 closure sufficiency 主張以最小 mutation 反駁；
3. AI-3／AI-1 R1 將 `SCHEMA-BIND-API-01`、`CANON-NEGZERO-01`、`CLOSURE-CLASS-01` 的 epistemic classification 從「全部 blocker」細分為 unconditional blocker、conditional interface blocker、definition ambiguity、fail-closed mismatch 與 hardening。

這是 evidence governance 的真正進展：它防止綠燈、簽名與 hash 被過度解讀，也防止次要問題被誇大成第二個無條件 blocker。

### 4.3 AI-4：把已知 blocker 封裝成新的工程候選

v0.2.2 的候選修補面是具體的：

- operational references 由 mode/family 與 pinned policy 導出，並綁到 signed trace map；
- edge 帶 role、expected type、version、hash，而不是只有裸 hash；
- run/maximal/fairness/sandbox/contract/invariant 使用 typed wrappers；
- `ValidateBytes(recordBytes,schemaBytes,artifactSnapshot)` 以同一 bytes 產生 parse object 與 digest；
- raw `-0` 在 lexical domain 被拒絕；NFC／Unicode scalar domain 有明示規則；
- malformed envelope 先判 required members，unsupported 才判 unknown；
- gate applicability 以 schema／semantic layer 分工；
- PARITY/2-SAT transition、event counts、time/debt、problem size、failure-frontier、answer-access 由 validator 導出或重算。

這些修補補的是「工程 record 不可任意自報」與「證據欄位不能跨角色互換」的 bounded interface gap。它沒有補「一個抽象是否保留 NP computation semantics」的 theorem。

### 4.4 AI-5：把 AEREC 的有效部分變成 adaptive governance

AI-5 真正拿來的不是 RC1 `sum_squares` backend 的泛化能力，而是：

- immutable candidate identity；
- known-negative corpus；
- external validation；
- measured validation cost；
- Pareto／no-change selection；
- history-fed fail-fast ordering；
- candidate 不因 local green light 自動升格。

這使「自適應」變成可觀察的治理迴圈，而不是「系統自己變強」的敘事。它仍然不是 adaptive complexity theorem。

## 5. AI-4 最新 candidate／blocker 刷新

### 5.1 v0.2.2 的 frozen identity

AI-4 的 v0.2.2 candidate 狀態文件列出：

- schema：`BDBB386CE7EAAB5377344BF29762CCBE45EA6371AC72742DE509467CB70BB556`；
- external validator：`7DA459E8AD9FB3F8A49FAA312A612F05484588143F36FF0918D090D6B1965AE5`；
- projection：`7860AA7A741FAE5DCC6846B614C16450D29D17573563D6373A243931B9B51E57`；
- role-bearing closure：`11F6CB511ADFCF9528D11390E59CE1B52D8F709053FF5AA7295230F5B3E604EB`；
- evidence role spec：`2FEFA7AACB9B6D914C3B78CDB2C187262D12A35BD56B14FD5882A71B84991A3F`；
- fixture manifest：`501A4D067040217C3AC0595AA5D9BD726B8E43A9C821242F7C170D38236E4E56`；
- live report：`D7CE9B3A6610603681177CC943B86CE955AEE8693DD46BD0802EC1B75069814B`。

checksum surface 是 98 entries。此身份只能證明候選內容固定；不能證明候選已獲獨立採納。

### 5.2 Candidate self-test 的正確讀法

目前自測結果是：

- frozen v0.2：14/14；
- frozen v0.2.1：11/11；
- v0.2.2：15/15；
- 2-SAT fixed-seed exhaustive crosscheck：6 個 variable-count × 250 cases = 1500；
- v0.2.2 manifest：31 fixtures，6 accepted、2 structurally/semantically valid but admission=false、23 fail-closed negatives、0 mismatch；
- fixture producer 隔離重跑：72 generated files byte-identical；
- 三種 valid-signature `REF-TYPE-01` variants 均被拒絕。

這是本地 self-test／candidate experiment。AI-4 文件自己將 external disposition 寫為 `PENDING AI-1/AI-2/AI-3 READ-ONLY ACCEPTANCE`，因此不能簡化成「v0.2.2 已修好」或「工程閉合完成」。

### 5.3 v0.2.1 與 v0.2.2 的 blocker 界線

| 版本 | 已證明的正面項目 | 仍然／曾經的 blocker | 目前地位 |
|---|---|---|---|
| v0.2 | schema／I0 structural experiment；部分測試 | `PROV-DERIVE-01` | 反例／前代基線 |
| v0.2.1 | PROV-DERIVE 兩個負例在有效 signature 下被拒；TOCTOU、oracle、gate 等 bounded probes | `REF-TYPE-01`；另有條件式 API／canonical 分類問題 | frozen FAIL counterexample |
| v0.2.2 | role/type/version/mode、signed/derived map、bytes binding、derived context、31 fixture self-test | 外部獨立驗收尚未完成；仍需找 sibling role-map/closure/signature/schema/resource/context bypass | frozen candidate, unpromoted |

`REF-TYPE-01` 的實質含義是：v0.2.1 的「envelope-aware transitive hash closure」不能稱為 `type-safe evidence closure`。v0.2.2 的三個負例成功拒絕，只能說已封閉該已知 attack family，不能說任意 role/type/semantic substitution 均不可能。

## 6. AI-5 AEREC 實戰線刷新

### 6.1 已完成的實戰閉環

AI-5 以 v0.2.1 frozen candidate 作父代，在不改 candidate bytes 的前提下完成：

- 22/22 fixtures 的 outcome 與 manifest expectation 一致；
- 138 files、1,177,012 bytes 的 immutable content-addressed snapshot；
- snapshot 前後核心 pins 穩定；
- `REF-TYPE-01` external negative probe 明確觀察到 `closure=pass`、`record_accepted=true`，因此選擇 `no-change-control`；
- 搬移 candidate 後發現原測試依賴外部 `ROOT.parent/run-record.schema.json`；補上精確 v0.1 schema 後 14/14 與 11/11 才能重跑通過；
- control full-tree rescan 與 one-snapshot batch 的 bounded wall-time 比較：`1682.701 ms` 對 `222.530 ms`，約 7.56×。

### 6.2 六種結果必須分開

| 結果 | AI-5 證據 | 不可推成 |
|---|---|---|
| 速度提升 | 固定 22 fixtures、單機、9 repetitions 的 validation throughput | SAT solver speedup、一般輸入漸近改善 |
| 驗證閉合 | pins、manifest、negative corpus、no-change、immutable snapshot | 完整 validator correctness theorem |
| adaptive governance | 新反例進入歷史後，候選退回 no-change；失敗前沿可影響 gate ordering | adaptive algorithm 的 worst-case theorem |
| packaging finding | 單獨搬移 candidate 的測試路徑依賴 | 算法語義失敗或 P/NP obstruction |
| local PASS | 受限環境與 fixture 的可重播結果 | independent acceptance、production measurement truth |
| no-change | 不把 v0.2.1 綠燈升格，保留負例控制組 | 新候選 v0.2.2 已獲 promotion |

### 6.3 AI-5 尚未刷新到 v0.2.2 的地方

截至本輪直接交付，AI-5 還沒有一份對 v0.2.2 的獨立 full acceptance；它的 AEREC baseline 明確把 v0.2.1 當作 negative control，等待 v0.2.2 frozen bytes 後再承接。因此不能把 AI-5 的 7.56×、22/22 或 no-change 結果寫成 v0.2.2 的驗收結果。

## 7. AI-6 未看到、但現行紅隊／工程暴露出的更深問題

AI-6 在盲讀中已經抓到 hidden solver、answer-dependent quotient、nonuniform advice、成本與 semantics 的抽象版本。後續工程又暴露出幾個更細的層次；它們不是替代 AI-6，而是把其批評落到接口結構。

### D01. hash closure 與 role/type/semantic closure 是不同命題

v0.2.1 的變異只改 receipt-only `run_spec_ref`，重算 closure，不重簽，仍然通過。這說明：

```text
signature validity
  + transitive hash reachability
  + envelope shape
≠ role-correct operational evidence
```

這是 AI-6「quotient/lift 尚未定義」在 evidence graph 上的同構風險：保留了結構可達性，不代表保留了任務所需語義。

### D02. projection boundary 可能排除真正重要的語義欄位

如果 receipt-only refs 不在 candidate projection、也不在 signed trace map，record 的 visible identity 可以不變而 operational meaning 改變。這比單純「hash 不完整」更精確：需要先定義哪些欄位屬 task semantics、哪些只是 metadata，然後將 semantic boundary 綁進 theorem／validator。

### D03. schema mapping 與 claimed digest 的 API 分裂

AI-2 找到的 `SCHEMA-BIND-API-01` 顯示：若 API 同時接受 parsed mapping 與 caller-claimed hash，卻未由同一 bytes snapshot 內部導出二者，呼叫者可以把不相干 schema object 與正確 hash 組合。R1 後來精確分類為 conditional interface blocker，而非 v0.2.1 path interface 的第二個 unconditional blocker。

這是傳統 theorem 語言常忽略的 boundary：`schema` 不是一個抽象值就夠，必須說明其 representation、digest、parse origin 與 trust boundary。

### D04. derived facts 與 signed self-report 的角色不同

`problem.size`、failure-frontier、answer-access、transition counts、resource fold 如果只由 signed record 自報，會重現 hidden solver／advice 問題；若由 validator 從 pinned bytes、family、mechanism、trace 與 oracle 重算，才是較強的 derived gate。v0.2.2 將這些列入，但仍是 bounded validator semantics，並非一般 complexity proof。

### D05. classification order 會改變 epistemic status

缺 `spec_id` 的 envelope 應先判 malformed/fail；只有 shape-valid 但版本未知才是 unsupported/unknown。這不是 cosmetic error：`fail`、`unknown`、`notApplicable` 的順序會改變「證據不足」是否被誤當「未知但可接受」。AI-3 的四值 gate 與 AI-4 的 `GateAssignmentConformant` 正在處理這個接口層，但尚未轉成一般 theorem logic。

### D06. candidate 可攜性是新的工程成本義務

AI-5 搬移 snapshot 發現測試依賴 workspace parent 的 v0.1 schema。這不證明演算法錯，但說明「frozen candidate」不等於「self-contained relocatable artifact」。若要把驗證包當成 reproducible evidence，external compatibility layout、packaging topology、dependency identity 也要進 provenance／cost ledger。

### D07. AEREC 的 adaptation 可能是安全的治理，但不是演算法自我證明

AI-5 的 no-change、history ordering、failure frontier 與 Pareto selection 是一個有用的 controller；它仍需把「何時改變候選」與「何時保持不變」視為 policy。這個 policy 可以保護 theorem work 不被工程綠燈污染，但它自身沒有證明新候選在 worst-case 或一般語言上更快。

### D08. bounded validator 的 scope 可能被誤讀成 general robust semantics

v0.2.2 的 robust I0 使用 singleton deterministic finite run，並明示 scheduler/fault nondeterminism 在候選外。這是正確的 fail-closed scope；但如果摘要只寫「robust PASS」，讀者會回到 AI-6 所擔心的 all-runs 誤讀。robust 必須始終帶著 run-policy、fairness、maximality、fault budget 與 scope。

## 8. 看似補上、其實仍屬 Definition／Experiment／Engineering 的項目

| 看似補上 | 實際分類 | 尚缺的 theorem obligation |
|---|---|---|
| v0.2.2 role-bearing closure | Engineering candidate | 對任意 computation abstraction 的 semantic preservation/lift |
| 31 fixtures 全過 | Experiment／bounded regression | 對所有輸入、所有 machine family 的 universal quantifier |
| Lean `robust_to_std` | Small formal lemma | 一般 robust policy、fairness、resource bound 與四層 implication |
| 1500 2-SAT cases | Experiment／oracle crosscheck | 一般 3-SAT、NP language、asymptotic theorem |
| 72 generated files byte-identical | Reproducibility evidence | Uniform compiler theorem與生成成本界 |
| 7.56× snapshot throughput | Performance experiment | solver worst-case、fine-grained bound、P/NP conclusion |
| no-change-control | Adaptive governance | controller 的 formal safety、liveness、regret／worst-case analysis |
| hashes／Ed25519 receipts | Provenance attestation | hardware truth、semantic role theorem、cryptographic trust model |
| four-valued gates | Definition/formal schema | domain-specific soundness/completeness of semantic validation |
| `GLC0` module | Formal scaffold | GLC semantic losslessness 的 selected definition與一般 abstraction theorem |
| candidate promotion gate | Engineering acceptance | mathematical characterization theorem |

## 9. 雙方仍無法橋接的詞彙與 theorem obligation

### 9.1 詞彙對照

| 框架詞 | 傳統學術最接近的翻譯 | 仍缺什麼 |
|---|---|---|
| GCC | fixed-model polynomial-time membership／machine-invariance presentation | admissible model class、simulator、encoding與 cost theorem |
| USRT | uniform compiler／determinization transformation | `U` 的有效性、codegen、per-N vs combined-input polynomial bound |
| USEG | succinct computation representation／restricted quotient process | answer-blind construction、transition closure、decode、sound/complete/lift |
| GLC0 | task-relative total correctness plus semantic contract | semantic losslessness 的 domain與可驗證 predicate |
| GLCpoly | GLC0 加 resource refinement | resource ledger 的 asymptotic quantifiers與存在性 |
| GLCrobust | policy-relative all-admissible-run safety/liveness | nonempty/maximal/fair/fault semantics與 uniform wall-clock bound |
| final ledger | audit record／proof witness／trace-derived certificate 的候選交集 | 不是三者中哪一個尚未決定 |
| semantic loss debt | unresolved abstraction/refinement obligations | debt basis、retirement proof、是否為 set 而非 scalar |
| global | 對某個明示 domain 的全稱量化 | domain 是 model、input、run、family 還是 evidence graph |
| universal | effective uniform construction／interpreter | 是否同一 exponent、是否包含 machine description、是否收費 |
| robust | fault/scheduler policy 下的 all-runs property | 不可與 NP existential branch 混型 |
| closure | graph reachability、schema validation、semantic admission 的不同層次 | 必須說是哪一種 closure |
| adaptive governance | verified controller／portfolio selection／no-change policy | 不是自動得到 adaptive algorithm complexity |

### 9.2 尚未完成的 theorem obligations

1. **Model obligation：**正式定義 `\mathfrak M_adm`、編碼、cost semantics、uniform enumeration 與 pairwise polynomial simulation。
2. **Uniformity obligation：**將 `∀N∃D_N` 升格為有效 `∃U∀N`，並計入 compiler、code size、initialization 與 online runtime。
3. **NTM semantics obligation：**分離 existential accepting branch、all-run robust execution、configuration aggregate 與 deterministic decision state。
4. **USEG obligation：**選 weak 或 strong；若 strong，定義 answer-blind quotient／abstraction、local transition、canonical representation、decode、soundness/completeness/lift。
5. **GLC semantic obligation：**選定 decision-relative、witness-relative、trace-relative 或 state-relative losslessness，並展示正常丟棄無關資訊的 positive example 與必要資訊丟失的 negative example。
6. **Robust obligation：**定義 nonempty、maximal、fair、fault budget、recovery、scheduler 與 wall-clock／step bound，並說明與 standard property 的 implication 或 incomparability。
7. **Ledger obligation：**把 `T_compile`、`T_construct`、`T_use`、`T_decode`、`T_verify`、`T_recover`、code/advice/proof bytes 分成可量化函數，而非只作事後欄位。
8. **Barrier obligation：**對任何 equality/lower-bound theorem 標示 relativization、natural-proof、algebrization、P/poly/advice 狀態；目前仍是 not yet engaged。
9. **Formal correspondence obligation：**Lean theorem 的 statement、quantifiers、assumptions、scope 必須與論文完全相同；compiled artifact 不能替代未形式化的強版本。
10. **Engineering-to-math obligation：**說明 bounded validator 的 admission property 是否只是 interface invariant，還是能被抽象成對任意 machine／run／input 的 theorem；目前尚未建立此抽象。

## 10. AI-7 的橋接裁定

### 10.1 AI-6 正確理解且應保留的批評

以下全部保留：

- GCC 目前大致是 P 的重述；
- admissible model 必須有正式 simulation，不靠「合理」；
- USRT 必須是有效 uniform compiler，而不是存在性選擇；
- rate cone 是 runtime 的重參數化；
- NTM path semantics 不能假裝是 deterministic single trace；
- USEG 弱版會退化為 solver trace，強版需要獨立 representation restriction；
- answer-dependent quotient、hidden preprocessing、advice 與 code size 是 nonuniformity 風險；
- semantic losslessness、final ledger、robust fairness/maximality 需正式定義；
- GLC-first 是研究依賴，不是 implication；
- barriers 尚未真正進入；
- 以 theorem graph、small formal core、positive/negative suite 推進，比維持一個大等價式更可審核。

### 10.2 後續成果真正改變的，是「可觀察性」而非 P/NP 狀態

後續進度讓研究團隊現在可以更清楚地回答：

- 哪一個 gate 是 definition、哪一個是 semantic derivation、哪一個是 external attestation；
- 哪些 negative mutation 可以在不重簽下重現；
- 哪些 blocker 是 unconditional、conditional、definition ambiguity 或 hardening；
- 哪些 candidate bytes、fixture expectations、generated outputs 可被重播；
- 哪些 speed figures 只是 validation throughput；
- 哪些 robust claims 其實只在 singleton deterministic run scope；
- 什麼時候應停止演化並選 no-change。

這是重要且實用的研究基礎，但不是傳統複雜度 theorem 的替代品。

### 10.3 不能把工程閉合升格成數學閉合

目前最容易發生的誤讀是：v0.2.2 的 31 fixtures、role/type binding、Lean gate matrix、AEREC no-change 與 7.56× throughput 被拼成「四層已閉合」。這個拼接不成立，因為它混合了：

```text
Definition        : 對象與 gate 的命名／型別
Formal scaffold   : 對一小組命題的機械證明
Experiment        : 固定 corpus／固定 seed／固定環境的觀測
Engineering       : provenance、snapshot、candidate、promotion治理
Theorem           : 對明示 domain 的普遍量化與證明
P/NP conclusion   : 另外更高層的 complexity implication
```

v2.0 的橋接原則是：**每一項結果只可向上移動一層，且必須有新的 theorem obligation；不能由多個工程綠燈的數量直接跨到 P/NP conclusion。**

## 11. 後續最低安全順序

若繼續研究，最小且不過度承諾的順序是：

1. 等待 AI-1／AI-2／AI-3 對 v0.2.2 frozen checksum candidate 的二次唯讀結果；在此之前，v0.2.2 只保持 unpromoted。
2. 將 v0.2.2 的工程 scope 固定為「bounded evidence validator」，不稱 universal proof assistant、general robust semantics 或 P/NP engine。
3. 在固定 deterministic TM core 上，完成 AI-6 建議的 GLC0 semantic abstraction positive/negative pair。
4. 另立 `USEG_weak` 與 `USEG_strong`；弱版承認是 solver trace，強版只在一個明確 representation class 上先做小類別 theorem。
5. 對任一 GCC／USRT arrow，先交付完整 quantifier table、machine encoding、compiler cost 與 no-advice statement。
6. 把 AEREC 的 adaptive governance 保留為工程方法：候選生成、失敗前沿、no-change、成本回饋；不要把它直接命名為新 complexity class。
7. 只有在 theorem graph 中某條箭頭已完成、scope 與 assumptions 無歧義後，才討論其對 P/NP 的 conditional implication；本報告不做該推進。

## 12. 最終判定與凍結聲明

AI-6 盲審的 major revision 沒有被後續成果推翻；它被後續成果具體化、細分並在工程層得到反例支持。後續最強的正面結果是：

- 一個可編譯的 GLC0／run／gate／countermodel 最小骨架；
- 一套能發現並保存 `PROV-DERIVE-01`、`REF-TYPE-01` 的外部紅隊流程；
- 一個包含 role/type/context binding 的 v0.2.2 工程候選；
- 一個以 immutable snapshot、negative corpus、no-change 與成本回饋運作的 AEREC governance loop。

後續最強的負面結果是：工程驗收本身暴露出「hash closure 不等於 role-safe semantic closure」，而 v0.2.2 尚未完成獨立 acceptance。這使研究更誠實，但不會把工程 blocker變成 P/NP blocker。

**本報告不解 P/NP，不代表任何 P=NP 或 P≠NP 立場，也不把 v0.2.2 promotion、AEREC throughput 或 Lean compilation 誤寫成 theorem。**

本檔案完成後另存 freeze manifest；後續如需修改，建立 v2.1 或 v3，不覆寫本檔案與 v1.0。

