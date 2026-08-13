# 傳統學者盲讀報告：P/NP 動態四層閉合框架 v1.0

**審閱角色：** AI-6，傳統複雜度理論學者／外部審稿人  
**審閱日期：** 2026-08-09  
**審閱階段：** 隔離第一輪盲讀  
**報告狀態：** 冷凍；僅為審查意見，不修改來源材料

## 0. 審閱範圍與總判定

本報告只讀取以下三份材料：

1. P_NP_動態四層閉合框架_啟發式研究提案_v1.0.md
2. P_NP_動態四層閉合框架_研究交接與後續實行建議_v1.0.md
3. P_NP_動態四層閉合框架_GLC優先研究交接與實行建議_v1.0.md

未讀取公開網頁、AI Board、其他任務、AI-1 至 AI-5 產物、AEREC 或其他內部紀錄。因此下列判斷是對三份交付材料本身的盲讀，不是對作者整個研究背景的評價。

### 總判定

作為一份明確標示為「啟發式研究綱領／Characterization Program」的材料，框架是可理解的，而且有幾個重要的自我約束：它沒有把路徑數量直接當作下界，注意到模型不變性不是任意 Turing-complete 機器都自動享有的性質，也反覆提醒不能把研究草圖寫成 \(P=NP\) 或 \(P\neq NP\) 證明。

但作為傳統複雜度理論的定理論文，現在尚未達到可審證程度。主要原因不是「尚未解出 P/NP」本身，而是核心物件仍分成三類：

- GCC 在目前寫法下大致是標準 \(P\) 的跨模型重述；
- USRT 若補上有效 uniform compiler，可能是 \(P=NP\) 的另一種機器級表述，但現有量詞還不足以固定這件事；
- USEG 若允許任意 polynomial-size、polynomial-time 的摘要，會直接退化為「存在 deterministic polynomial-time solver」；若要它成為非平凡理論，必須對摘要、商關係與生成器施加獨立而可檢查的限制；
- GLC 的資源中立版、含 polynomial resource 的版本、標準版與 robust 版尚未被整理成不衝突的正式層次。

因此我的審查結論是：**可作為研究綱領或概念性 position paper 繼續；若以數學定理稿投稿，應判為 major revision，暫不能接受為已建立的 characterization theorem。**

## 1. 用標準複雜度語言重建作者的主張

以下不是替作者增加主張，而是把三份材料中可辨識的內容翻譯回標準語言。

### 1.1 基本設定

預期的標準設定應是：取有限輸入字母表 \(\Sigma\)，語言 \(L\subseteq\Sigma^*\)，以及一台 polynomially clocked nondeterministic Turing machine \(N\)。對每個輸入 \(x\)，\(N\) 的接受語義是

\[
x\in L
\quad\Longleftrightarrow\quad
\text{存在一條 }N\text{ 在 }x\text{ 上的接受路徑}.
\]

標準問題是是否存在 deterministic polynomial-time machine \(D\) 決定同一個 \(L\)。利用 NP-completeness，可等價地問是否存在 polynomial-time algorithm 決定 SAT。

材料沒有打算改寫 \(P\)、\(NP\)、certificate 或 polynomial-time reduction 的標準定義；它打算新增觀察座標。

### 1.2 GCC 的標準重建

GCC 想描述的是：在一個被稱為 admissible 的計算模型族 \(\mathfrak M_{\mathrm{adm}}\) 中，某語言的 deterministic 資源複雜度是否落在 polynomial-time 等價類。

若把定義補成標準形式，例如固定輸入編碼並令

\[
C_M(L,n)=\min_{A\text{ decides }L}
\max_{|x|\le n}\operatorname{time}_M(A,x),
\]

再要求所有 \(M\in\mathfrak M_{\mathrm{adm}}\) 與一個標準機器有 uniform polynomial simulation，那麼

\[
\exists M\in\mathfrak M_{\mathrm{adm}}\; C_M(L,n)\le n^{O(1)}
\]

就只是 \(L\in P\) 的跨模型表述。對所有 \(L\in NP\) 量化，便是 \(P=NP\) 的標準內容。

所以目前 GCC 的可辨識主張不是新的複雜度類，而是：**在適當固定的模型不變性假設下，\(P\) 的 membership 不依賴所選的合理機器表示。**

### 1.3 USRT 的標準重建

USRT 想主張：存在一個有效的 deterministic transformation \(\mathcal U\)，將任意 polynomially clocked NTM \(N\) 轉成 deterministic machine \(D_N\)，使

\[
D_N(x)=1
\quad\Longleftrightarrow\quad
N\text{ 在 }x\text{ 上存在接受路徑},
\]

且對每個固定 \(N\)，存在 polynomial \(q_N\) 使

\[
\operatorname{time}(D_N,x)\le q_N(|x|).
\]

材料用

\[
R_A(n)=\frac{1}{1+T_A(n)}
\]

把完成時間換寫成「完成速率」，並明確說不要求 deterministic 與 nondeterministic 的數值時間相等，只要求都落在 inverse-polynomial rate cone。

在補上 machine encoding、有效轉換、初始化、編譯成本、狀態編碼與 nondeterministic run semantics 後，這個主張最接近：**NP computation 可被 deterministic polynomial-time 決策程序取代。**這在對所有 NP machine 量化時，與 \(P=NP\) 高度接近，甚至可能就是 \(P=NP\) 的機器級等價。

### 1.4 USEG 的標準重建

USEG 想把 \(N\) 在 \(x\) 上的指數多條可能計算歷史，轉成一條 deterministic、長度 polynomial、每一狀態大小 polynomial、每一步可 polynomial-time 更新的摘要序列

\[
Z_0\to Z_1\to\cdots\to Z_m.
\]

最終摘要應精確回答「是否存在接受路徑」。作者正確指出，原始路徑數量

\[
|\Gamma_N(x)|
\]

本身不能推出任何一般時間下界；一台屬於 P 的機器可以故意猜無用 bit，產生指數多條無用分支。

若 USEG 只要求「存在某個 polynomial deterministic sequence，最後能正確回答 \(N\) 的語言」，那它就是 deterministic polynomial-time solver 的另一個表示。若 USEG 另要求 \(Z_t\) 是依據某個事先固定、可有效構造、非 answer-dependent 的 quotient 對全部 computation histories 的精確摘要，則它可能成為一個更具體的 characterization；但這個額外限制目前尚未正式給出。

### 1.5 GLC 的標準重建

GLC 有兩個互相接近但必須分開的版本。

第一個是資源中立的 \(\mathrm{GLC}_0\)：對所有合法輸入，執行最終停止，輸出正確，並滿足某種尚未定義的 semantic losslessness。這個版本近似程式驗證中的 total correctness 加上一個額外語義保持條件；它不是 P/NP 的資源命題，因為它可允許指數時間。

第二個是資源受限版本：在 GLC 的正確／完成／無損條件外，再要求 polynomial time、space 或其他帳本欄位合格。對 decision language 而言，若「無損」不比正確輸出更強，這就是 \(L\in P\)。因此對所有 NP 語言量化才得到 \(P=NP\)。

最後是 \(\mathrm{GLC}_{robust}\)：對所有明確列入 \(\operatorname{Runs}_{adm}(A,x)\) 的 rerouting、rollback、restart、scheduler 或有限可恢復故障執行歷史，均要求最終正確完成。這比較像 fault-tolerant program semantics 或 resilient computation property，而非標準 complexity class。

### 1.6 整體命題的標準讀法

目前最安全的標準讀法是：

\[
\begin{aligned}
&\text{GCC：}&&L\text{ 是否在 P；}\\
&\text{USRT：}&&\text{是否能以有效方式把每台 poly-time NTM 換成 poly-time DTM；}\\
&\text{USEG：}&&\text{是否有受限且可有效構造的 polynomial succinct computation representation；}\\
&\text{GLC：}&&\text{這些程序的 correctness、termination、semantic preservation 與（另加的）resource acceptance。}
\end{aligned}
\]

所以材料提出的是一組 **representation / characterization agenda**，不是一個現成的新複雜度類，也不是已完成的 \(P=NP\) 證明。

## 2. 可理解且值得保留的部分

### 2.1 研究定位是誠實的

三份材料都明確寫出「不宣稱已證明 \(P=NP\) 或 \(P\neq NP\)」，把大型等價式標成待形式化或帶問號。這是必要且正確的學術定位，避免把名詞創新誤當成定理。

### 2.2 對 raw path cardinality 的警惕是正確的

材料明確給出一台 P 問題也可被故意寫成有指數多條無用 branches 的反例方向。這排除了常見但錯誤的推論：候選數量指數大，所以問題必然不在 P。這一點與標準複雜度審查相容。

### 2.3 量詞次序的敏感度是正確的

材料注意到

\[
\exists\mathcal U\;\forall N\;\exists q_N\in\operatorname{poly}\;\forall x
\]

與「所有 \(N\) 共用一個固定 exponent」不同。對語言級的 P 定義，polynomial exponent 可以依演算法／語言而定；這個區分值得保留。

不過，這個量詞仍不足以完成 uniformity，見第 5 節。

### 2.4 沒有把「合理模型」無條件擴展為任意 Turing-complete 模型

材料指出 Turing completeness 不會自動保證相同時間複雜度，並提出不含 oracle、不可計價無限精度與免費答案源的限制。這個方向正確。

### 2.5 GLC_std 與 GLC_robust 的分開是必要的

材料沒有直接把容錯、rollback 或 scheduler variation 塞進標準 \(P=NP\)。也注意到永久斷電、永久不排程、不可恢復毀滅不能默認放入 admissible disturbance。這是良好的模型邊界意識。

### 2.6 GLC-first 文件補上了兩個重要自我約束

GLC 優先文件明確要求第一版 \(\mathrm{GLC}_0\) resource-neutral，避免把 GCC 偷塞入語義基底；也明確提出「specification 可以提及真值，但 implementation 不可把真值當 oracle 讀取」。這兩點是後續處理 answer-dependent abstraction 時不可缺少的檢查。

## 3. 目前主要是標準重述的部分

| 材料中的物件 | 以標準語言讀取 | 當前判定 |
|---|---|---|
| GCC | 在多項式可互模擬模型中問 \(L\in P\) | 目前主要是 P 的 machine-invariance 重述 |
| USRT | 對每個 poly-time NTM 產生 poly-time DTM，保持接受語義 | 補上有效 compiler 後高度接近、可能等價於 \(P=NP\) |
| \(R=1/(1+T)\) | 對 runtime 的單調反函數重參數化 | 可作記號，但尚未顯示新的 dynamic invariant |
| USEG（無額外限制） | 用一個 deterministic polynomial process 決定同一語言 | 直接退化為 P solver 的另一種表示 |
| GLC_std | 正確、停機，另加未定義的 semantic losslessness | 至少 total correctness 是標準語義的顯式化 |
| GLC_robust | 所有指定擾動歷史均最終正確 | fault-tolerance 性質；與 \(P=NP\) 非同類命題 |

這不是負面評價。重述可以有價值，尤其當它導出精確的新 interface、可形式化語義或非平凡的受限模型定理。但材料不能把「新的座標名稱」本身當作新的 complexity-theoretic content。

## 4. 非標準、未定義或容易造成錯誤的核心項目

### 4.1 GCC 的 \(T_M^L\) 沒有固定究竟是哪一個演算法

提案把 \(T_M^L(n)\) 描述成「某個正確決策演算法」的最壞時間，隨後又把 \([T_M^L]_{\equiv_{poly}}\) 當成語言的 GCC。若是任意某個演算法，GCC 不是語言的不變量；同一語言可有一個 polynomial algorithm 和一個人為放慢的 exponential algorithm。若要描述語言，應使用最小成本或直接使用「存在一個 \(A\)」的 class-membership 定義。

建議只選一種：

1. 定義 \(C_M(L,n)\) 為在固定模型上的最小 deterministic worst-case cost；或
2. 不定義一個新的函數類，直接定義 \(\mathrm{GCC}_{poly}(L)\) 為「存在 \(M,A,k\) 使 \(A\) 在 \(M\) 上以 \(O(n^k)\) 決定 \(L\)」。

後者會更誠實地呈現它與 P 的關係。

### 4.2 \(\mathfrak M_{\mathrm{adm}}\) 的限制仍不足以保證模型不變性

「有限可描述、uniform、無 oracle、無免費無限精度、無超多項式 advice」不能單獨推出 polynomial simulation。可以設計一個有限描述、uniform、沒有外部 oracle 的模型，給一個單步完成巨大計算的 primitive；它仍然會違反多項式可模擬。若要求族內 pairwise polynomial simulation，這一性質本身必須作為正式公理或由明確 simulator theorem 證明，不能由「合理」二字代替。

此外還要處理：

- 每個模型的 input/output encoding；
- 每一 primitive 的 cost；
- simulator 是否 uniform、是否可由有效程序產生；
- simulation overhead 對模型描述長度與輸入長度的依賴；
- 是否允許 polynomial advice、randomness、並行度、實數或其他非標準資源。

若這些不固定，GCC 的「global」只是一個宣稱，不是定義完成的 complexity invariant。

### 4.3 「polynomial completion-rate cone」沒有正式定義

以 \(R_A(n)=1/(1+T_A(n))\) 作單調變換可以表示

\[
T_A(n)\le n^k
\quad\Longleftrightarrow\quad
R_A(n)\ge \frac1{1+n^k},
\]

但它不代表一個獨立的「速率動力學」。它依賴 clock step 的選擇；只要把一個 machine 的一步細拆成 polynomial 多步，數值速率就改變。若只研究「inverse-polynomial rate」這個等價類，最好直接定義 rate cone，例如

\[
\mathcal R_{poly}=
\{R:\exists k,c,n_0\;\forall n\ge n_0,
R(n)\ge c n^{-k}\},
\]

並說明它只是 polynomial-time class 的重參數化，而不是新的 machine-independent local velocity。

### 4.4 USRT 的狀態與 hitting time 對 NTM 不適用於單一路徑

對 nondeterministic machine，\(S_N(x,t)\) 不是唯一狀態；它是某條 run 的狀態，或所有 configurations 的集合／關係。現在的

\[
\tau_A(x)=\min\{t:S_A(x,t)\in H_L(x)\}
\]

沒有說明是：

- 沿某一指定 run；
- 對所有 runs 取最大；
- 對接受 runs 取最小；
- 對 configuration graph 做 reachability；還是
- 對 deterministic simulation 的 aggregate state。

對 NP，接受是 existential；不能把 NTM 的整體輸出直接寫成每一分支都等於 \(\chi_L(x)\)。一個 yes-input 可以有接受分支，也有拒絕分支。若要把 USRT 寫成正式命題，必須分開 nondeterministic acceptance semantics 與 deterministic decision semantics。

### 4.5 「速率轉換」沒有比較原速率

目前 USRT 的條件只要求 \(D_N\) 有某個 polynomial runtime。它沒有要求 \(D_N\) 與 \(N\) 的 runtime 有任何函數關係，也沒有要求保留某個狀態級 invariant。因此嚴格說它是 polynomial determinization，不是 rate preservation。這個名稱可以保留作研究語言，但正式 theorem 必須使用可驗證的 runtime statement。

### 4.6 \(\sim_D\) 與 \(\kappa_{\mathrm{eff}}\) 尚不是數學物件

材料說兩條路徑若在最終決策所需資訊上可由同一摘要精確代表，便令

\[
\gamma_a\sim_D\gamma_b.
\]

但以下問題均未回答：

- \(\sim_D\) 的 domain 是完整 paths、partial paths、configurations 還是 certificates？
- 它是否必須是可計算的、polynomial-time decidable 的 equivalence relation？
- 等價是對固定 \(x,N\) 定義，還是對所有 inputs 的 machine-level 定義？
- 摘要的 canonical encoding 是什麼？
- relation 的建構是否需要知道 \(\chi_L(x)\)？
- quotient transition 是否獨立於答案？
- 只有 final decision 等價，還是每一步都要 compositional、sound、complete？

若只要求「最後答案相同」，則把所有 paths 放進同一個等價類就可能合法，\(\kappa_{\mathrm{eff}}=1\)；但如何找到這個類本身已經包含原問題。若要求更強的可計算／組合條件，則 USEG 可能不再由 \(P=NP\) 自動推出。這是整個框架最重要的未決分叉。

### 4.7 USEG 的存在量詞容許 hidden solver

「存在 \(G_N,F_N,Z_0,\ldots,Z_m\)」還不等於「有一個可由 \(N\) 有效構造的 generator」。若 \(F_N\) 的程式碼可以任意硬編一個已知 solver，若 \(Z_0\) 可以在未計價 preprocessing 中先含有答案，或若 \(\operatorname{Dec}\) 的成本不計，USEG 會變成任意答案程序的包裝。

至少要規定：

- \(N\) 與 \(G_N\) 的有效編碼；
- \(G_N\) 的建構器是單一 uniform algorithm；
- 建構時間、輸出程式長度、初始化時間均記帳；
- \(Z_0\) 只能由 \(N,x\) 經指定成本產生；
- \(F_N\) 與 \(\operatorname{Dec}\) 的程式碼長度與執行成本；
- 所有摘要的 bit-length 與 precision；
- quotient 的 soundness/completeness 與 non-circularity。

### 4.8 GLC 的「semantic losslessness」可能是冗餘或過強

若 \(\Lambda_A=0\) 只表示最終輸出正確，那它與 correctness 重複；若它要求每個中間 state 都與完整 computation semantically equivalent，則一般的 branch pruning、丟棄已證無關 bit、抽象化或壓縮都可能被排除，即使演算法完全正確。材料提出 \(\operatorname{Sem}_L\) 與 preservation relation 的方向，但沒有選定其中哪一種。

對 decision problem，較可行的方向不是要求 bit-level 無損，而是定義一個抽象語義、concretization 或 sound/complete invariant：中間摘要可以丟掉資訊，但不能丟掉對最終 decision 必要的資訊。這仍需明確指定，否則 GLC 的核心判準不可審查。

### 4.9 最終帳本不是現成的 complexity-theoretic object

「過程自由，最終帳本不自由」是一個可理解的工程原則，但 \(\mathcal L_A(x)\) 目前是事後描述欄位，不是演算法可計算或審核的正式結構。需要說明：

- ledger 是 trace 的函數、證明 witness，還是 meta-level audit record？
- Resource \(\in\) Poly 是對單一 \(x\) 的欄位，還是對 \(n\) 的 asymptotic bound？
- Sequence 如何定義，是否包括所有中間資料結構與 compiler cost？
- Loss=0 的判定是否可有效驗證？
- ledger 本身是否可能比原計算更難產生？

沒有這些規格，GLC 只能作語義口號，不能作 theorem premise。

### 4.10 GLC-first 是研究依賴，不是數學 implication

第三份文件把研究順序改為

\[
\mathrm{GLC}\to\{\mathrm{GCC},\mathrm{USRT},\mathrm{USEG}\}.
\]

文件也正確註明箭頭表示研究依賴，不表示數學 implication。這一點應在所有正式圖表中保持。從標準複雜度觀點，語言的接受語義、terminal output 與 runtime 本來就可以先定義，沒有數學上的必要性說 USRT 或 USEG 必須等待一個名為 GLC 的外層。GLC-first 可以是好的工程／公理化策略，但不能被寫成已證明的理論層級關係。

### 4.11 三份材料之間存在版本張力

啟發式提案與一般交接文件中的 GLC 帳本包含 \(B,R,S\) 等 polynomial resource/rate/sequence 欄位；GLC 優先文件又明確規定第一版 \(\mathrm{GLC}_0\) 必須 resource-neutral，只包含 correctness、completion、losslessness。

這不是不可修正的矛盾，但須正式分層。建議至少使用：

\[
\mathrm{GLC}_0 \quad\text{(semantic, resource-neutral)},
\]

\[
\mathrm{GLC}_{poly}\quad\text{(GLC}_0\text{ plus polynomial resource bounds)},
\]

\[
\mathrm{GLC}_{std},\qquad \mathrm{GLC}_{robust}.
\]

並明確說 \(\mathrm{GLC}_{std}\) 是 execution model／fault scope，\(\mathrm{GLC}_{poly}\) 是 resource refinement；兩者不是同一個維度。

## 5. 缺失的量詞、uniformity、成本與模型條件

這一節列出若要把材料變成正式命題，最低限度需要補上的項目。

### 5.1 輸入、機器與時間的基本 domain

必須固定：

\[
\Sigma,\quad L\subseteq\Sigma^*,\quad
\langle N\rangle,\quad \langle A\rangle,\quad
|x|,\quad |\langle N\rangle|.
\]

還要說明 polynomial clock 是：

- 每一 branch 都在 \(p_N(|x|)\) 步內停止；或
- 只有 nondeterministic choice 深度受限；或
- clock machine 的 description 是 \(N\) 的一部分。

若不是所有 branches 都 halt，NP acceptance、GLC completion 與 \(T_N(n)\) 的定義會彼此衝突。

### 5.2 必須區分語言量詞與機器量詞

至少有四種不同命題：

\[
\forall L\in NP\;\exists D_L,
\]

\[
\forall N\;\exists D_N,
\]

\[
\exists\mathcal U\;\forall N\;\mathcal U(N)=D_N,
\]

以及

\[
\exists U\;\forall N,x\;
U(\langle N\rangle,x)=\chi_{L_N}(x).
\]

它們的 machine encoding、compiler uniformity 與 combined-input runtime 不同。現有材料把這些方向放在同一個「USRT」標籤下，尚未選定正式對象。

### 5.3 USRT 的 transformation 必須是有效對象

需要明確要求 \(\mathcal U\) 是：

- 一個 total computable compiler；或
- 一個 polynomial-time compiler；或
- 一個 uniform construction whose one-time cost is separately accounted。

若只寫 \(\exists\mathcal U\) 而不規定有效性，這個符號可代表不可計算的選擇函數。若允許每一台 \(N\) 私下挑一台 \(D_N\)，就會引入 nonuniform flavour；它不應再直接叫 uniform determinization。

### 5.4 編譯、初始化與線上執行成本必須分開

至少需要三個函數：

\[
T_{\mathrm{compile}}(\langle N\rangle),
\qquad
|\langle D_N\rangle|,
\qquad
T_{D_N}(x).
\]

若 \(D_N\) 是先離線建構後反覆使用，必須說明這是不是研究問題允許的 preprocessing。若 \(N\) 是固定常數，\(|\langle D_N\rangle|\) 可被硬編；若 \(N\) 是輸入的一部分，則必須把它納入總成本。不能把 exponential compilation 放在「一次性」欄位後就從 polynomial claim 消失。

### 5.5 每個 polynomial exponent 的依賴要明示

標準 P 允許 exponent 依語言／演算法而定，但不允許依 input \(x\) 非可控地變動，也不允許把一個長度超過 polynomial 的 machine description 當成常數免費使用。正式命題應標示：

\[
\exists k_N,c_N,n_N\;\forall x,\quad
T_{D_N}(x)\le c_N |x|^{k_N}+c_N.
\]

若研究的是 universal combined-input solver，則應改成一個以 \(|\langle N\rangle|+|x|\) 為參數的固定 polynomial bound。兩者不能混寫。

### 5.6 NTM 的 path-level semantics 必須補齊

應明確定義：

- \(\Gamma_N(x)\) 是否包含完整 path 或 partial path；
- path 的長度上限；
- accept、reject、nonhalting 的分類；
- aggregate state 是 set、multiset、DAG、formula、circuit 還是其他 encoding；
- 對 yes/no input 的 soundness 與 completeness；
- deterministic summary 是否要回答存在接受 path，還是要保留每條 path 的完整 output。

不能用 deterministic machine 的單一路徑符號 \(S_A(x,t)\) 直接代表 NTM 的全部分支。

### 5.7 USEG 的 state size、transition、decode 必須全部計價

目前已提及 \(m\)、\(|Z_t|\)、\(F_N\) 的 polynomial 性質，仍需補上：

\[
T_{Z_0}(N,x),\quad
T_{F_N}(Z_t,x),\quad
T_{\operatorname{Dec}}(Z_m),\quad
|\langle F_N\rangle|,\quad
\text{precision/encoding cost}.
\]

總成本應有一個明確式子，例如

\[
T_G(N,x)=T_{Z_0}+
\sum_{t<m}T_{F_N}(Z_t,x)+T_{\operatorname{Dec}},
\]

再證明它對所選參數是 polynomial。只說「每步 polynomial」不足以排除 exponential number of steps、exponential initialization 或巨大隱含常數／程式碼。

### 5.8 Quotient 的非循環性必須是定義內條件

至少需要一個 relation \(Q\) 或 abstraction algorithm，並證明：

1. 它的程式碼獨立於待求答案；
2. 建構 \(Q\) 的成本被計入；
3. \(Q\) 對 transition closed 或有明確 refinement property；
4. final decode 對 acceptance 的 soundness/completeness；
5. 所有 representation switching 均有 polynomially bounded encoding。

否則「decision-sufficient」只是在結果正確後的追認。

### 5.9 GCC 的 simulation theorem 與 model boundary

必須選擇下列兩條路之一：

- 固定一個標準 deterministic TM/RAM 模型，只把其他模型作輔助，並證明它們的 polynomial simulation；或
- 正式定義 \(\mathfrak M_{\mathrm{adm}}\) 為一個帶有效 enumeration、cost semantics 與 pairwise simulator 的模型族。

不能用「合理模型」作未定義的全稱量詞，也不能把 Cobham–Edmonds 類 thesis 當成無條件數學定理。

### 5.10 GLC 的 semantic domain 與 fault quantifier

需要固定：

\[
\mathcal S_A,\quad
\to_A,\quad
H_L(x),\quad
\operatorname{Out},\quad
\operatorname{Sem}_L,\quad
\operatorname{Runs}_{adm}(A,x).
\]

對 robust 版還要量化：

- 每次 fault 的類型；
- 每一 run 的 fault 數量上限；
- scheduler 是否 fair；
- recovery code 的時間與空間；
- 所有 admissible runs 是否有 uniform polynomial bound，還是只要求 finite termination；
- fault budget 是否是輸入的一部分。

「有限可恢復故障」若沒有 uniform bound，可能仍允許任意長的 recovery sequence；若 scheduler 不要求 fairness，永久不調度的一條 run 會使 eventual completion 不可能。

### 5.11 Reduction 與 completeness 的位置必須明確

若用 \(P=NP\) 對 USRT 或 USEG 的方向證明，至少要固定一個標準路線：

\[
L\in NP
\xrightarrow{\text{Cook--Levin / poly reduction}}
SAT
\xrightarrow{D_{SAT}}
\chi_L.
\]

要計入 reduction 的建構時間、formula size、SAT solver 的 runtime，並說明 fixed \(D_{SAT}\) 是 theorem witness 的一部分。否則「\(P=NP\) 所以存在一個 universal U」只停留在直覺。

## 6. 最小 proof obligations

這些不是要求作者現在解決 P/NP，而是若要把每一個箭頭升格成 theorem，至少要交付的證明義務。

### 6.1 基礎形式化義務

先交付一份 definitions file，內容至少包含：

1. alphabet、input、language、machine encoding；
2. deterministic / nondeterministic transition semantics；
3. totality、acceptance、rejection；
4. polynomial function 與 worst-case cost；
5. uniform transformation、compiler 與 advice 的定義；
6. state encoding、size、precision；
7. GLC0 的 semantic predicate；
8. robust run 與 fault model；
9. soundness、completeness、non-circularity。

任何後續 theorem 都只能引用這份 definitions file，不應在每份交接文件中以自然語言重新漂移。

### 6.2 GCC 的最低 theorem ladder

**GCC-1（definition-level）。**證明 \(\mathrm{GCC}_{poly}(L)\) 的正式定義與標準 \(L\in P\) 相符，或清楚說明差異。

**GCC-2（simulation）。**對每個 admissible model \(M\)，證明一台標準機器可在 polynomial overhead 模擬 \(M\)，並證明反方向若宣稱 model-independent。

**GCC-3（no hidden power）。**排除 unit-cost SAT gate、oracle、unbounded advice、infinite precision、nonuniform circuit family 等捷徑。

若 GCC-1 至 GCC-3 完成，最可能的結果是 GCC 不是新的 class，而是 P 的 machine-invariant presentation。那也是有效結果，但不應再宣稱已產生獨立 P/NP mechanism。

### 6.3 GCC \(\Rightarrow\) USRT 的最低義務

需證明：給定 GCC 的 deterministic polynomial realization，如何從任意 \(N\) 有效產生 \(D_N\)，而不是只說「因為語言在 P，所以有某個 D」。

可接受的路線之一是：固定一個 SAT solver witness，對 \(N,x\) 構造 Cook–Levin formula，組合 reduction 與 SAT solver。必須寫出：

- \(N\) 的 clock 與 encoding；
- formula size 的 polynomial bound；
- reduction 的 uniform construction；
- \(D_N\) 或 universal evaluator 的 code／compile cost；
- 組合後的 runtime；
- acceptance semantics 的 soundness/completeness。

若不用 reduction，則要提供一個真正的 machine-level compiler theorem。

### 6.4 USRT \(\Rightarrow P=NP\) 的最低義務

在假設 USRT 的正式版本下，對任意 \(L\in NP\) 選一台 polynomially clocked \(N_L\)，令 \(D_L=\mathcal U(N_L)\)，證明：

\[
\forall x,\quad
D_L(x)=\chi_L(x),
\qquad
\exists q_L\in\operatorname{poly}\;
\forall x,\quad
T_{D_L}(x)\le q_L(|x|).
\]

這個方向本身不難，但只有在 \(\mathcal U(N_L)\) 是一台真實可表示的 deterministic machine、沒有 hidden advice/oracle、且 state/run semantics 已定義時才是 theorem。若 USRT 只是一個不可計算的 selection schema，不能稱為 uniform transformation。

### 6.5 \(P=NP\Rightarrow\) USRT 的最低義務

不能只引用「每個 NP 語言都有一個 D」。若 USRT 要求單一 \(\mathcal U\)，需證明如何從一個固定的 SAT solver witness 與 \(N\) 的 description 有效產生 \(D_N\)，或正式說明 theorem 中 \(\mathcal U\) 可以把該固定 solver 作為常數內嵌。

這是

\[
\forall N\;\exists D_N
\]

到

\[
\exists\mathcal U\;\forall N
\]

之間的 uniformity obligation。數學上的存在性不能自動提供一個 compiler。

### 6.6 USRT \(\Rightarrow\) USEG 的最低義務

「沿著 \(D_N\) 的 deterministic configuration trace」確實可產生一條 polynomial-length state sequence，但這不會自動證明它是「對 \(N\) 的所有 computation histories 的 quotient」。需選定兩種解讀之一：

- **弱 USEG：**只要求最終 sequence 能正確決定 \(N\) 的語言。此時 USRT 幾乎直接推出 USEG，但 USEG 只是 solver trace 的改名；或
- **強 USEG：**要求每個 \(Z_t\) 是對 all histories 的明確 aggregate/quotient，transition 由預先固定的 local/compositional rule 產生。此時必須額外證明 \(D_N\) trace 具有該 aggregate semantics；不能從任意 deterministic solver trace 直接推出。

若選強 USEG，USRT \(\Rightarrow\) USEG 未必是無條件命題。

### 6.7 USEG \(\Rightarrow\) GCC 或 \(P=NP\) 的最低義務

需由 generator 直接建立一台 deterministic decider，並展示總成本：

\[
T_G=T_{\mathrm{construct}}+T_{Z_0}+
\sum_{t<m}T_{F_N}+T_{\operatorname{Dec}}.
\]

要證明它 polynomial，且 generator 的 code 與所有摘要不含答案 oracle、nonuniform advice 或 exponential preprocessing。

若 USEG 定義對每個固定 \(N\) 只要求存在 \(G_N\)，則從 USEG 得到 \(L\in P\) 是可行的；但要反向得到一個 universal USEG compiler，必須另證 uniformity。若 USEG 的摘要 class 有額外限制，還要證明該限制對所有 NP machines 適用。

### 6.8 GLC0 的最低義務

先不要把 polynomial time 塞進基本 GLC。應在固定 machine model 下定義：

\[
\forall x,\;
\exists t<\infty,\quad
S_t\in H_L(x),\quad
\operatorname{Out}(S_t)=\chi_L(x).
\]

接著明確定義 semantic losslessness。必須給出至少一個正常但會丟棄無關資訊的演算法，說明它是否滿足 GLC；也必須給出一個中途丟失決策必要資訊但偶然答對的演算法，說明它為何不滿足或滿足哪一個較弱版本。

### 6.9 GLC_std 與 GLC_poly 的最低義務

需證明：

- 若 GLC_std 只表達 total correctness，它適用於所有 total deciders，不等於 P；
- 若 GLC_poly = GLC_std + polynomial resource，則對 decision language 它與 \(L\in P\) 的關係是什麼；
- 若 semantic losslessness 比 correctness 更強，則 \(L\in P\) 是否仍保證存在一個滿足它的演算法。

只有在第三點也證明後，才能寫

\[
\forall L\in NP,\quad
L\in\mathrm{GLC}_{poly}
\Longleftrightarrow P=NP.
\]

### 6.10 GLC_robust 的最低義務

先定義 fault model，再研究關係。至少要提供：

- 一個 singleton run model，說明它退化為 standard total correctness；
- 一個有限且有 uniform budget 的 recoverable fault model；
- 一個 scheduler 不公平或永久 fault 的 impossibility example；
- recovery overhead 的 time/space bound；
- robust property 與 \(P=NP\) 的精確 implication、incomparability 或 conditional result。

「可能嚴格強於」只能作 conjectural orientation，不能當作已知性質。

### 6.11 形式證明規範的最低義務

若以 Lean、Coq 或 Isabelle 形式化，形式化的 theorem 必須與論文 theorem 完全同一個 statement，包括：

- 所有 quantifiers；
- machine encoding；
- asymptotic bound；
- admissible model assumptions；
- no-oracle/no-advice assumptions；
- semantic preservation；
- compilation cost。

形式系統證明的是「被形式化的命題」，不是作者想表達的較強直覺。若 formal file 把 solver、quotient 或 answer 當作已有參數，形式化成功也不代表一般 \(P=NP\) 結果。

## 7. Relativization、natural proofs、algebrization 與 P/poly 審查

三份材料列出這些 barrier 作為後續工作，但目前沒有任何 barrier analysis 或 theorem-level status。傳統審查應先把它們標記為「未進入」，不能宣稱框架已繞過。

### 7.1 Relativization

若 GCC／USRT／USEG 的所有定義、compiler、reduction 與 proof 都能對任意 oracle \(A\) 原封不動地加上 superscript \(A\)，那麼該證明很可能是 relativizing。這種方法不能單獨解決 P vs NP，因為存在 oracle 世界分別使 \(P^A=NP^A\) 與 \(P^B\ne NP^B\)。

因此未來若宣稱三相等價導向實質 P/NP 結論，必須說明：

- theorem 是否 relativizes；
- 若不 relativize，非相對化的具體步驟在哪裡；
- quotient construction 是否偷偷使用答案、全域結構或不可相對化的語義。

### 7.2 Natural proofs

目前材料沒有 lower-bound proof，也沒有 circuit property，因此尚不能說觸及 natural proofs。可是若後續嘗試由「所有有效 sequence／quotient 都必然大」推出 circuit lower bound，就必須檢查該 property 是否 constructive、large、且可能被小電路計算。若三項同時成立，natural-proofs barrier 會成為直接審查問題。

### 7.3 Algebrization

目前沒有 algebraic extension、low-degree oracle 或 polynomial identity testing 等結構，故 algebrization 尚未被實際處理。未來若用代數摘要或消元證明一般 SAT 的結果，仍需檢查 proof 是否在 algebraic oracle extension 下成立。

### 7.4 P/poly 與 nonuniformity

這是當前最直接的風險。下列物件若依 \(N\)、輸入長度或 instance family 任意選取，都可能把 P/poly 式非 uniform 資訊偷入 USEG/USRT：

- 每個 \(N\) 的不可計算 \(D_N\)；
- 每個長度 \(n\) 的 quotient table；
- 未計價的 SAT lookup table；
- 以 \(x\) 或正確答案決定的 equivalence relation；
- 隨 \(n\) 增長的 advice；
- 一個固定描述卻蘊含巨大 truth table 的 primitive。

「沒有超多項式 advice」仍不夠；若研究對象是 P 而非 P/poly，應明確排除未計價 advice，或把 advice 長度與生成成本列入模型。

### 7.5 Barrier status 的最低標註

未來每一份正式結果應固定填：

Relativizes: yes / no / not applicable / unknown  
Natural-proof risk: yes / no / unknown  
Algebrizes: yes / no / unknown  
Uniformity: uniform / nonuniform / unresolved  
Advice/oracle/precision: absent / present / unresolved  
Reduction used: exact reduction and cost

目前三份材料的正確狀態是：**尚未提出 lower-bound 或 equality theorem，因此 barrier status 為 not yet engaged；不能寫成已克服。**

## 8. 可能的誤讀點與標準修正

| 可能誤讀 | 標準修正 |
|---|---|
| GCC 是一個比 P 更新的複雜度類 | 目前是 P 的跨模型描述；要成為新類需給出不同於 P 的可測量內容 |
| USRT 代表逐條把所有 nondeterministic path 在 polynomial time 展開 | 目標是決策等價的 deterministic procedure，不是逐條列舉所有 paths |
| \(R=1/(1+T)\) 表示真正的物理或局部狀態速度 | 它只是 runtime 的反函數重參數化，clock refinement 會改變數值 |
| 路徑數量指數大即可推出 \(P\ne NP\) | 明確錯誤；材料本身已否定此推論 |
| 有一個 polynomial-size quotient 就已經證明容易 | 還要證明 quotient 可 uniform 構造、可更新、可 decode，且成本 polynomial |
| \(\sim_D\) 可以先用正確答案定義再稱為有效摘要 | 這是 answer-dependent circularity，必須禁止或把建構成本完整記帳 |
| \(\forall N\exists D_N\) 自動給出一個 uniform U | 不自動給出；需證明 compiler／選擇函數可計算，或採用固定 SAT witness 的構造 |
| GLC 先行表示 GLC 數學上推出 GCC/USRT/USEG | 文件自己說箭頭是研究依賴；不能改讀成 implication |
| GLC_std 已比 \(P=NP\) 更強 | 若只為 total correctness，它甚至不含 polynomial resource；若加 polynomial resource，需看 losslessness 是否額外限制 |
| GLC_robust 自動等價於 P/NP | 它依賴 fault、scheduler、recovery 模型；目前最多是獨立的 robustness extension |
| 一次實驗產生短 sequence 就證明一般 NP 有 polynomial quotient | 只能是 instance-level experimental observation，不是 asymptotic theorem |

## 9. 「不理解、反對、未證、可修正」分類

### 9.1 不理解／目前無法審核的部分

以下不是說文字完全不可讀，而是說材料沒有提供足夠 formal object，傳統審稿人無法判定真偽：

1. \(\mathrm{GCC}(L)=[T_M^L]_{\equiv_{poly}}\) 中 \(T_M^L\) 是哪個 algorithm 的成本，以及 equivalence relation 的正式定義。
2. 「decision-sufficient」與 \(\sim_D\) 的實際 domain、encoding、decidability 與 transition semantics。
3. GLC 的 \(\Lambda_A=0\) 究竟是 bit-level、state-level、decision-semantic 還是 trace-level 的無損。
4. Final Ledger 是可計算資料結構、證明 witness，還是事後審計概念。
5. robust runs 的 scheduler/fault quantifiers、fairness、fault budget 與 resource bound。
6. USRT 中 \(S_N(x,t)\)、\(\tau_N(x)\) 對多分支 NTM 的確切語義。

在這些物件未固定前，不能對相關 theorem 給真或假的結論。

### 9.2 我反對或不接受的目前表述

這裡的「反對」是對現有理論表述的審查判斷，不是聲稱作者的潛在修正版必然錯誤。

1. 不接受把 \(\mathfrak M_{\mathrm{adm}}\) 的自然語言限制當成已足以推出模型不變性。
2. 不接受把 \(R=1/(1+T)\) 稱為已有獨立理論內容；目前沒有超出 runtime class 的證據。
3. 不接受把任意 deterministic solver trace 直接當成對所有 nondeterministic histories 的 USEG quotient。
4. 不接受把 GLC-first 的研究順序解讀成數學基礎定理。
5. 不接受在沒有 semantic losslessness 定義時，宣稱 GLC 的「零語義損失」已構成可檢驗驗收條件。
6. 不接受以「所有後續都要 count」取代對 compiler、state representation、precision、advice 與 decode 的實際 cost theorem。

### 9.3 未證但有清楚研究價值的部分

以下是合理的 conjecture/open problem，但不是現有材料已證明的結果：

1. GCC、USRT、USEG 三者在某個正式版本下的完整雙向等價。
2. \(P=NP\Rightarrow\) 存在一個單一 uniform USRT compiler。
3. USEG 的強版 quotient formulation 是否由 \(P=NP\) 推出。
4. USEG 是否能在不引入 answer-dependent abstraction 的前提下，對一般 SAT 給出 polynomial aggregate。
5. \(\mathrm{GLC}_{robust}\) 是否嚴格強於某個標準 resource-bounded completion class。
6. GCC 是否能在不只是 P 的重新命名下產生 machine-independent dynamic invariant。

### 9.4 大多可修正的部分

這些問題不必等待 P/NP 解決，透過版本化定義與反例即可處理：

1. 把 GCC 改為固定標準模型加 simulation theorem，或明確承認它是 P 的重述。
2. 把 USRT 分成 USRT-existence、USRT-uniform-compiler、USRT-combined-input 三個命題。
3. 把 USEG 分成弱版與強版，分別說明一個是 solver trace，另一個是 restricted quotient theory。
4. 將 GLC 分成 \(\mathrm{GLC}_0\)、\(\mathrm{GLC}_{poly}\)、\(\mathrm{GLC}_{std}\)、\(\mathrm{GLC}_{robust}\)。
5. 以抽象語義／soundness-completeness 取代未定義的 Loss=0。
6. 加入 compiler、initialization、transition、decode、precision 的 ledger schema。
7. 用小型正例與破壞性反例測試每一條定義。

## 10. 建議的最小反例與正例套件

在聲稱任何 characterization 前，建議至少完成以下 thought experiments；它們不需要解 P/NP。

### 正例

1. addition：確認 GLC0 的正確、完成與語義描述不會把普通算術排除。
2. sorting：確認丟棄比較過程中的無關 bit 不等於 semantic loss。
3. graph reachability：確認摘要可以保存 reachability invariant，而不必保存所有歷史。
4. 2-SAT/Horn-SAT/XOR-SAT：測試 USEG 是否能給出清楚、可更新的 aggregate state。
5. bounded-treewidth SAT：測試 quotient 大小如何依結構參數而非只依 \(n\) 計算。

### 破壞性反例

1. **Branching P machine：**一個本來屬於 P 的語言，先猜 \(n\) 個無用 bit 再執行原演算法；打破 raw path cardinality heuristic。
2. **Answer-dependent quotient：**把所有接受路徑依真實答案分成一類；測試 non-circularity 是否真的禁止它。
3. **Hidden preprocessing：**先用 exponential procedure 建立一張 lookup table，再把 table 當 \(Z_0\)；測試 compilation/initialization ledger。
4. **Nonuniform family：**每個 \(n\) 選一個最佳摘要或 advice string；測試 P 與 P/poly 邊界。
5. **Unit-cost superprimitive：**給模型一個單步 SAT 或巨大整數 primitive；測試 GCC model admissibility。
6. **Semantically lossy but accidentally correct run：**中途刪除必要資訊但在特定 input 上碰巧答對；測試 GLC 的 loss definition。
7. **Permanent-fault run：**永久 crash 或不公平 scheduler；測試 robust GLC 的 admissible-run 邊界。
8. **Nondeterministic yes-input with rejecting branches：**測試 GLC correctness 是否錯把 existential acceptance 當成 every-branch output。

## 11. 具體審稿建議與可接受的下一版形態

### 11.1 下一版不應再把大等價式當作一個工作單位

應把主命題拆成一個 theorem graph，每個箭頭標為 definition、standard theorem、conditional theorem、conjecture、counterexample 或 open。至少要分開：

\[
\begin{array}{c}
P=NP\Rightarrow\mathrm{USRT}_{\mathrm{uniform}},\\
\mathrm{USRT}_{\mathrm{uniform}}\Rightarrow P=NP,\\
\mathrm{USRT}_{\mathrm{weak}}\Rightarrow\mathrm{USEG}_{\mathrm{weak}},\\
\mathrm{USEG}_{\mathrm{strong}}\Rightarrow P=NP,\\
\mathrm{GLC}_0\leftrightarrow\text{某種 total correctness},\\
\mathrm{GLC}_{robust}\;?\;\text{standard complexity property}.
\end{array}
\]

### 11.2 先交付一個很小但完整的 formal core

建議先在一個固定、簡化的 deterministic TM model 中完成：

1. terminal state；
2. exact output correctness；
3. finite termination；
4. semantic abstraction relation；
5. GLC0；
6. polynomial cost refinement；
7. 一個 sorting 或 graph reachability 的正例；
8. 一個 answer-oracle abstraction 的反例。

這會比先寫全域四相等價更能顯示 GLC 是否有獨立可用的內容。

### 11.3 對 USEG 必須作二選一

**路線 A：承認弱版是重述。**明確寫：USEG_weak 等價於存在 deterministic polynomial solver，價值在於提供一種狀態序列 interface；不要再暗示它已經提供額外壓縮機制。

**路線 B：定義強版。**選定一個受限表示類、局部 transition rule、uniform compiler 與 canonical quotient，然後先對 2-SAT/Horn-SAT/XOR-SAT 或 bounded-treewidth 類別證明 theorem。只有在有非平凡 generalization 後，才談一般 NP。

### 11.4 對 GCC 應避免「全球」造成額外負擔

若研究重點不是模型理論，直接使用標準固定模型與 polynomial simulation lemma 會更清楚。若保留 GCC，需把 \(\mathfrak M_{\mathrm{adm}}\) 當成明確的 model class object，而不是以「合理」作未定義總括。

### 11.5 對 GLC 應把語義層與成本層正交化

推薦的層次是：

\[
\mathrm{GLC}_0
\quad\text{(what counts as exact completion)},
\]

\[
\mathrm{Cost}_{poly}
\quad\text{(time/space/representation/precision accounting)},
\]

\[
\mathrm{GLC}_{poly}=\mathrm{GLC}_0+\mathrm{Cost}_{poly},
\]

\[
\mathrm{GLC}_{robust}=\mathrm{GLC}_0+\mathrm{admissible disturbance semantics}.
\]

這樣可以避免用同一個 GLC 符號同時承擔 correctness、resource、rate、sequence、fault tolerance 五種不同問題。

## 12. 最終審稿意見

### 對「可理解」的判定

作者正在提出一個以四種視角重述 P/NP 的形式化研究計畫：資源（GCC）、deterministic 化的完成時間（USRT）、對 nondeterministic histories 的有效摘要（USEG）、以及 correctness/termination/semantic acceptance 的閉合規格（GLC）。這個意圖可以從三份材料穩定重建。

### 對「反對」的判定

我反對目前把模型族、rate cone、quotient、ledger、semantic losslessness 當作已足夠精確的數學定義；也反對把任意 deterministic trace 直接等同於對 nondeterministic path family 的有效 quotient。這些不是措辭小瑕疵，而是會決定命題真偽的核心條件。

### 對「未證」的判定

GCC \(\Leftrightarrow\) USRT \(\Leftrightarrow\) USEG、它們與 \(P=NP\) 的完整關係、強 USEG 的非循環構造、GLC robust 的嚴格強度，都仍是未證或未定義後才可證明的研究問題。材料把它們標為待形式化，這一點是正確的。

### 對「可修正」的判定

大部分問題可藉由正式定義、量詞表、machine encoding、cost ledger、反例套件與 theorem ladder 修正，不需要先解決 P/NP。真正需要決定的是：作者是否願意把 USEG 強版限制到一個明確的 representation class，以及是否接受 GCC/USRT 的相當部分是標準 P 的重新座標化。

### 發表級別建議

若投稿類型是「研究綱領、概念框架、形式化議程」：可在大幅補充定義邊界與 related standard notions 後考慮。

若投稿類型是「新複雜度理論、已建立的 P/NP characterization」：目前應退回 major revision；沒有足夠正式定義與 theorem proof，不能以等價式或「closed exact computation」語言替代。

最公平的總結是：**這不是一份失敗的 P/NP 證明；它目前也不是 P/NP 證明。它是一個已經辨認出若干常見陷阱、但尚未把核心新詞彙固定成可證偽數學物件的研究綱領。**

## 13. 冷凍聲明

本報告完成後不再修改上述盲讀判斷。未讀取對照材料，未聯絡其他任務，未修改三份來源文件，未發布 Board。後續可在對照階段將本報告與其他觀點並置，但不應把對照結果倒灌回本輪的盲讀內容。

