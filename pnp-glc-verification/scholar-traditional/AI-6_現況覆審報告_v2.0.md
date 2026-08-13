# AI-6 現況覆審報告 v2.0

## 傳統複雜度理論學者／外部審稿人

日期：2026-08-09（Asia/Taipei）  
狀態：**第二輪現況覆審；凍結候選；不構成 P/NP 結論**

本報告保留第一輪凍結檔，不覆寫：  
`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-scholar-traditional\outputs\傳統學者盲讀報告_P_NP動態四層閉合框架_v1.0.md`

本輪只讀取使用者授權的 AI-7 凍結報告、五個指定任務的歷史與直接交付，以及 AI-2／AI-3／AI-4／AI-5 的形式化、反例、Lean、validator、AEREC 與候選狀態。沒有修改來源、沒有聯絡 AI-1 至 AI-5、沒有發布 Board。

---

## 0. 結論先行

第二輪證據使我比第一輪更肯定：這已經不是只有術語堆疊的研究草圖。它現在有三項真正可審核的增量：

1. AI-3 將 GLC⁰ 的兩種 run semantics、四象限 gate applicability、非空性與 standard／robust 分離寫成可編譯的 Lean 核心，並給出 standard 不推出 robust 的明確反例。
2. AI-2／AI-4 將 `PROV-DERIVE-01`、`REF-TYPE-01` 與 schema cross-field 反例變成可重放的工程測試；v0.2.2 候選對已知三種 REF-TYPE 變體均 fail closed。
3. AI-5 的 AEREC 真的保留歷史負例並在 v0.2.1 失敗時選回 `no-change-control`；不可變快照也帶來有界驗證批次的實測吞吐改善。

但這些增量沒有把原本的核心定理義務變成已完成的定理。我的總判定如下：

> **作為研究綱領、形式化議程或明確標示範圍的工程驗證候選：可繼續，且比第一輪成熟。**  
> **作為傳統複雜度理論的 P/NP characterization theorem paper：仍不可接受；若投稿，至少是 major revision，且需先重寫主張範圍。**  
> **作為已證明 P=NP、P≠NP、或已建立新複雜度類的材料：不成立。**

最重要的 epistemic distinction 是：

- 「已知有限攻擊在候選 validator 中被拒絕」是工程結果；
- 「所有符合抽象規格的輸入、模型、run 與 resource ledger 都因此正確」是普遍定理；
- 前者目前有證據，後者目前沒有。

---

## 1. 現況材料與審查基線

### 1.1 可核查材料

| 材料 | 本輪讀取的學術／工程內容 | 審查地位 |
|---|---|---|
| AI-7 跨範式映射報告 v1.0 | GCC／USRT／GLC／USEG 的標準翻譯、四象限、uniformity、engineering boundary | 交叉參考，不是權威替代品 |
| AI-2 Phase 0 與 v0.2.1 red-team | pointwise infimum、NP branch／robust split、PROV-DERIVE、REF-TYPE、schema cross-field | 反例與障礙證據 |
| AI-3 Phase 0 與 Phase 1 Lean | GLC⁰ signature、run policy、four-valued gates、countermodels、axiom scope | 形式化範圍證據 |
| AI-4 I0 v0.2.2 candidate | role-aware closure、pinned replay、resource fold、PARITY／2-SAT fixtures | 有界 executable experiment |
| AI-5 AEREC v0.1 | frozen identity、歷史負例、no-change、immutable snapshot、timing | 工程選擇與成本實驗 |
| Clarify WTF issue／AI-1 current history | v0.2.2 二次驗收仍在進行中的狀態 | 不能當作已完成的獨立 acceptance |

### 1.2 候選的實際狀態

AI-4 `CURRENT-v0.2.2-candidate.md` 的狀態是：

```text
CANDIDATE_UNPROMOTED / pending independent acceptance
```

它報告 old 14/14、v0.2.1 11/11、v0.2.2 15/15、2-SAT 小規模 1500 cases、31 fixtures 與 72 個生成檔的候選內結果；AI-1／AI-2／AI-3 的 frozen checksum read-only acceptance 尚未完成。Clarify WTF issue 的最新歷史仍顯示 AI-1 正在進行 v0.2.2 二次 code review，因此本報告不把 candidate self-test 寫成 promotion。

---

## 2. 用標準複雜度語言重建現況主張

在現況下，作者／協作線實際上同時主張四種不同層級的事情：

### 2.1 GCC

GCC 可安全地讀成一個關於 deterministic algorithms、admissible models、cost semantics 與 polynomial simulation 的 characterization agenda。AI-2／AI-3 已明確拒絕把

\[
C(L,n)=\inf_{A} C_A(n)
\]

在每個輸入長度重新選算法的 pointwise infimum 當成 uniform P witness。由每個長度硬編答案表的 `A_n` 可使逐點成本很小，但不提供單一 polynomial-time decider。這是重要的反例修正；它不是 GCC 的 replacement theorem。

若 admissible model family 有固定 encoding、primitive cost、uniform enumeration 與 polynomial-overhead compiler，GCC 最可能仍是 P 的 model-invariance presentation；這個 presentation 可以有價值，但需要明確承認其內容。

### 2.2 USRT

USRT 仍可重建為：給定一個 polynomially clocked NTM 或其有效 encoding，存在一個 deterministic machine，並可能要求一個有效、uniform、cost-controlled transformer 產生它。現有材料尚未提供這個 transformer 的完整 formal signature，也沒有證明 combined input、compilation、initialization、state encoding 與 acceptance preservation 的成本界限。

### 2.3 USEG

USEG 的非循環版本必須至少要求 answer-blind、uniformly constructible、可更新、可 decode、sound／complete 的 quotient 或 aggregate。AI-2 已把 `m=0`、以答案初始化、two-point perfect abstraction、hidden preprocessing 與 per-length family 列為反例面。AI-3／AI-7 也承認 certified sufficiency 可能本身是未解的有效性問題。現況沒有強 USEG theorem。

### 2.4 GLC

AI-3 現在有一個 resource-neutral、task-relative、run-policy-relative 的 GLC⁰ kernel：

- terminal、output existence、output soundness 分開；
- standard run 與 robust admissible maximal fair run 分開；
- nonempty run family 不再被全稱式 vacuity 偷渡；
- resource-neutral 與 resource-bounded 是另一個正交軸；
- `zeroDebt`、fairness、Maximality 的一般語義仍是參數或未完成義務。

AI-4／AI-5 則實作了一個只支援 PARITY／2-SAT 的 I0 claim-ledger 與 external validator。它是 bounded verification interface，不是 GLC⁰ 的普遍實作，也不是 P/NP solver。

---

## 3. 第一輪盲審意見逐條覆審分類

分類含義：

- **已實質解決**：在明確聲稱的形式化或工程範圍內，原問題已被定義、證明或關閉；不外推到更大範圍。
- **部分解決**：反例、局部定義或條件 lemma 已有，但完整 theorem obligation 尚未完成。
- **只在工程層解決**：有 validator／fixture／replay／測量結果，尚未有與之對應的普遍數學定理。
- **尚未解決**：仍缺少決定命題真假的基本定義、量詞、模型或 proof。
- **出現更深的新問題**：後續成果不只是填補空白，還暴露出更強的信任、語義或 uniformity 義務。

| 第一輪意見 | v2 主分類 | 現況裁定 |
|---|---|---|
| F01 GCC 的 `T_M^L`／canonical algorithm 未固定 | **部分解決** | pointwise infimum 的 nonuniform collapse 已被 AI-2／AI-3 明確反例化，並改要求 fixed witness；但尚無新的 GCC 正式定義與 machine-invariance theorem。 |
| F02 admissible model family 只有「合理」描述 | **尚未解決** | 仍缺 model encoding、unit cost、precision、primitive cost、enumeration 與有效雙向 compiler。AI-4 的 pinned I0 只是單一 bounded family。 |
| F03 polynomial completion-rate cone／rate object 未定義 | **尚未解決** | `R=1/(1+T)` 仍只是 coordinate change；沒有 rate invariant、比較定理或 model-independent meaning。 |
| F04 NTM state／hitting time 被當成單一路徑 | **部分解決** | Lean 與 AI-7 明確分開 run semantics；但尚無 NTM existential acceptance 的正式 bridge。 |
| F05 rate conversion 未比較原速率與 overhead | **尚未解決** | 沒有 USRT 的 source／target cost relation，也沒有 transformation overhead theorem。 |
| F06 `~_D`、`κ_eff` 不是良定數學物件 | **尚未解決** | 仍缺 domain、encoding、decidability、state bound、construction 與 decode theorem。 |
| F07 USEG 可藏入 solver、advice 或答案 | **部分解決** | m=0、answer-dependent quotient、truth-table／advice family 與 hidden preprocessing 已被具體化為攻擊面；但強 USEG 的非循環 quotient 尚未建立。 |
| F08 semantic losslessness 可能冗餘或過強 | **部分解決** | AI-3 把 scalar loss debt 改成 obligation／recovery 方向；AI-4 有 event debt fold；兩者都尚未給 semantic preservation、recovery soundness／completeness。 |
| F09 Final Ledger 不是現成 complexity object | **只在工程層解決** | I0 ledger 可由事件與 trace 做 bounded replay；它尚未成為 machine-independent complexity measure，且部分測量依賴 signed raw evidence。 |
| F10 GLC-first 是研究依賴，不是 implication | **已實質解決** | AI-7、AI-3、AI-4 現況均把它當 workflow／interface dependency；沒有把箭頭升格為數學 implication。 |
| F11 GLC⁰、GLCpoly、standard、robust 版本張力 | **部分解決** | AI-3 明確採 resource regime × run quantifier 四象限與 gate matrix；一般 resource semantics 與 robust theorem 仍未完成。 |
| F12 USRT 的 `U` 未證明為有效 uniform transformer | **尚未解決** | 沒有 machine code、totality、compiler、construction cost 與 combined runtime theorem。 |
| F13 USEG quotient 的 sound／complete／lift | **尚未解決** | 目前只有 obligation map、counterexamples 與局部工程 admission；沒有一般 lift theorem。 |
| F14 每步 polynomial 不保證總成本 polynomial | **只在工程層解決** | I0 對固定兩步 transition、event time、counts、budget 做 fold；沒有任意 depth／state growth／restart／decode 的 general cost theorem。 |
| F15 robust 的非空性、Maximality、fairness | **已實質解決（定義核）／部分解決（一般語義）** | Lean 加入 nonempty guard，並機械化 Maximal 的 proper-extension exclusion；fairness 仍是 uninterpreted predicate，沒有 weak／strong／bounded 選擇。 |
| F16 NP existential branch 與 robust all-run 混淆 | **部分解決** | Lean 三狀態 countermodel 實際證明 standard 可真而 robust 可假；但尚未形式化 NTM acceptance 到 GLC run family 的保真 translation。 |
| F17 SchemaConsistency 與 SemanticValidate 混為一層 | **只在工程層解決** | AI-2 cross-field 反例與 AI-4 v0.2.2 的 external validator／`ValidateBytes` 已分出兩層；尚無 schema-to-semantics soundness theorem。 |
| F18 PROV-DERIVE／REF-TYPE 等 provenance sufficiency | **只在工程層解決** | v0.2.1 的兩種 provenance 造假與 REF-TYPE blocker 有 bounded 修補；v0.2.2 已知三種 REF-TYPE case 自測拒絕，但完整 provenance theorem、origin trust 與 independent acceptance 尚不存在。 |
| F19 P/poly、uniformity、advice | **部分解決** | pointwise hardwired family、tally code-size counterexample、PARITY streaming/table separation 已清楚；validator 的 uniformity gate 仍是 I0 mechanism-specific check，不是一般 P／P/poly theorem。 |
| F20 relativization、natural proofs、algebrization | **已實質解決（誤用審查）** | 目前沒有 lower-bound 或 equality proof，故正確標示為 not yet engaged；沒有證明已跨越任何 barrier。 |

此表的關鍵不是把較多項目標成「已解決」，而是將「局部反例已關閉」與「一般命題已證成」分開。

---

## 4. 指定重點核查

### 4.1 GLC 四象限：目前是真正的形式化介面，但不是四象限完成定理

AI-3 Phase 1 的 matrix 是一致且有用的：

| run mode | resource regime | run nonempty | maximality | fairness | account completeness | budget |
|---|---|---:|---:|---:|---:|---:|
| standard | neutral | applicable | N/A | N/A | applicable | N/A |
| standard | bounded | applicable | N/A | N/A | applicable | applicable |
| robust | neutral | applicable | applicable | applicable | applicable | N/A |
| robust | bounded | applicable | applicable | applicable | applicable | applicable |

這裡有三個實質進步：

1. neutral 只免除 threshold，不免除完整 account；
2. standard 不再被錯誤要求 maximality／fairness；
3. robust 的 universal claim 有 `AdmissibleMaxFairRunFamilyExists` nonempty guard，避免空集合全稱式 vacuity。

Lean 的 `GateVal = pass | fail | unknown | notApplicable`、`AllApplicablePass`、`GLC0Std`、`GLC0Robust` 與 countermodels 讓這個 gate／definition layer 已可審核。

但不能把它叫做完整 GLC theorem，原因是：

- `RunPolicy.fair` 是任意 predicate，尚未是 weak、strong 或 bounded fairness；
- `Maximal` 是「不存在 admissible valid proper extension」的定義，尚無有限／無限 trace encoding 的一般等價；
- `zeroDebt` 是外加的 `Input → Run → Nat → Prop`，沒有 obligation type、recovery certificate 或 recurrence；
- resource-bounded 只在 Lean gate applicability 層出現，沒有 polynomial resource semantics；
- AI-4 的 robust I0 明說採 singleton deterministic finite run，scheduler／fault nondeterminism 不在候選範圍。

因此 GLC 四象限的準確評語是：

> **Definition/gate matrix：已實質建立。**  
> **一般 semantics、resource theorem、robust complexity result：尚未建立。**

### 4.2 Uniformity：反例成熟了，uniform compiler 尚未出現

AI-2／AI-3 的 pointwise collapse 是這一輪最重要的理論增量。對每個長度選一台硬編答案的 `A_n`，可讓

\[
\forall n\;\exists A_n
\]

看起來很快，但不能推出

\[
\exists A\;\forall n.
\]

AI-3 更指出，即使只加 code length penalty，tally language 的 per-length hardwired program 仍可能保持 polynomial-size；所以「加一點描述長度」不是充分修補。這直接把第一輪對 P/poly／advice 的警告提升成正式攻擊義務。

AI-4 的 PARITY 對照也有實證價值：

- `parity-stream` 以固定 uniform program、prefix invariant、無 advice 通過；
- `parity-table-family` 的答案正確，但以 per-length table、advice generation 與 access cost 被 admission 拒絕；
- `2sat-kosaraju` 是固定的 bounded uniform mechanism。

然而 validator 的 `_uniformity_status` 是依 mechanism id 與固定字串（例如 `exists-one-program-for-all-input-lengths`）判定；這是對兩個 I0 family 的 executable policy，不是「所有 admissible generators 均 uniform」的定理。沒有 general compiler、uniform enumeration、advice generator theorem，也沒有把 AEREC history 置於 uniform complexity model 中。

裁定：**uniformity 的問題被正確辨識並部分 operationalized；未被一般解決。**

### 4.3 NP branch vs robust run：區分已證，橋接未證

AI-3 的 `splitSystem` 有 `start → good` 與 `start → bad`：standard policy 只選 good run，robust admissible family 同時含 good／bad，兩者 valid、maximal、fair。Lean 因而得到：

\[
GLC^0_{std}\quad\text{成立},\qquad GLC^0_{robust}\quad\text{不成立}.
\]

這是一個真正有效的局部 countermodel，且排除了 empty-family vacuity。它清楚說明：

- NP acceptance 是「存在 accepting branch」；
- robust GLC 是「所有 admissible maximal fair runs 都完成且正確」。

但這還沒有給出 NTM semantics、accept／reject／non-halting branch、scheduler run、fault run 之間的 formal translation。尤其 AI-4 的 robust candidate 只有 deterministic singleton run，不能代替 NP 的 existential branch，也不能代表一般 scheduler fault model。

裁定：**語義區分已部分解決；NP↔GLC bridge 尚未解決。**

### 4.4 Semantic loss／debt：從口號進入 bookkeeping，尚未成為 semantic theorem

目前有三個層次：

1. AI-3 Phase 0 將 scalar `Λ` 改成 obligation set／recovery obligation 的方向；
2. Lean `Solved0` 只要求外加 predicate `zeroDebt x ρ n`；
3. AI-4 `_replay_trace` 對 `debt_added`／`debt_retired` 做 set fold，驗證 registered、peak_open、outstanding 與事件一致。

第 3 層可證明「帳本依事件自洽」，但不能證明事件中標記的 debt 真的是語義損失，也不能證明 retire event 是合法 recovery。Lean countermodel 甚至使用：

```lean
noDebt := fun _ _ _ => True
```

在這個形式化範圍，`zeroDebt` 可以被任意 predicate 取代；因此 GLC⁰ 目前的 loss condition 仍可能被平凡化。這是本輪出現的更深問題之一：

> **把 loss debt 從一個 scalar 改成 obligation bookkeeping，解決了表示問題，卻把 soundness／completeness／recovery certificate 的 theorem obligation 暴露得更清楚。**

裁定：**部分解決，且出現更深的新問題。**

### 4.5 SchemaConsistency vs SemanticValidate：架構分工已成立，只在工程層成立

AI-2 對原 v0.1 schema 生成三個 cross-field contradictions：

- robust 卻沒有 maximal／fairness specs；
- failed uniformity／provenance gates 卻 `admission_pass=true`；
- oracle／contract／budget 失敗、debt=1 卻 `final_completion=true`。

原 JSON Schema 全部接受，這反駁的是 schema-alone sufficiency，不是「形狀 schema 本身格式錯誤」。這個 distinction 是正確的。

AI-4 v0.2.2 做了下列工程修補：

- `GateAssignmentConformant` 把 always-applicable gate 的 N/A 禁掉；
- `ValidateBytes(recordBytes, schemaBytes, artifactSnapshot)` 以相同 bytes 內部解析與 hash；
- mapping helper 不再作為支援的 trust-boundary API；
- admission／completion 由 external validator 導出，而不是 candidate 自報。

這使「已知 record-level contradiction」在 bounded interface 中可被拒絕。但仍沒有一個形式化 theorem 證明：只要通過 SchemaConsistency 與 SemanticValidate，就一定存在真實 execution、正確 provenance、正確 resource 或 semantic losslessness。AI-1 history 也把 `validate_record` 的 schema-hash 問題精確降級為：若 helper 不暴露則是 private implementation issue；若拿它作 soundness API，則仍是 blocker。

裁定：**工程分層已實質落地，但 theorem 層只在工程層解決。**

### 4.6 PROV-DERIVE-01：已知 fabricated ledger／digest 已關閉，origin trust 仍未關閉

v0.2.1 的初始 `PROV-DERIVE-01` 是有效 blocker：同步修改 record、trace、hash chain 後，`states=999` 與 fabricated transition digest 仍能被接受。AI-2 將它正確分類為「mirror／closure consistency，不是 execution derivation」。

v0.2.2 的 source 目前做了較實質的事情：

- `_transition_execution_status` 只支援固定 PARITY／2-SAT，依 pinned rule bytes 重算 candidate result 與兩個 transition；
- `_derived_event_counts` 從 events 重算 counts；
- time 從 event components fold 到 ledger；
- debt 從 event deltas fold；
- problem size、failure-frontier axes、answer-access family binding 由 pinned instance／mechanism 導出；
- space、description、admission cost、precision 則由 signed trace 的 raw measurements 綁定。

因此已知 v0.2.1 的兩個 fabricated cases 在 v0.2.2 candidate self-test 中被拒絕，這是實質工程進步。

但 source 自己也明說：

- validator 是 bounded executable interface，不是 proof assistant kernel 或 universal interpreter；
- raw measurements 只綁定 test signer，不是 production measurement authority；
- 只支援 PARITY／2-SAT，不能由 2-SAT 推廣到 3-SAT 或一般 SAT；
- 若 artifact root 的 origin、sandbox execution、measurement source 沒有獨立可信前提，簽章只是 attestation，不是由執行導出的證明。

裁定：**已知反例在工程層解決；一般 provenance／resource derivation 尚未解決，並出現 measurement authority 的更深問題。**

### 4.7 REF-TYPE：bounded known family 已修補，typed closure theorem 未有

v0.2.1 的 two no-resign variants 是有效 blocker：

1. robust `run_spec_ref` 換成 standard run spec；
2. robust run／maximal／fairness／sandbox refs 全換成 Ed25519 public-key artifact。

signature 與 untyped closure 通過，但 operational role semantics 沒有被綁定。AI-4 v0.2.2 candidate 新增：

- direct role → expected artifact type；
- transitive edge `{role, expected_type, sha256}`；
- parent／child role relation；
- family／mechanism／contract／oracle／rule／invariant binding；
- signed operational map 與 validator-derived expected map 比對。

其 reproduction report 顯示三案均 `record_accepted=false`，第三案甚至使用新的 valid signature 與 signed map，仍因 role／type／family mismatch 被拒絕。這說明 v0.2.2 對已知 REF-TYPE attack family 的修補比 v0.2.1 實質得多。

但候選仍是 `CANDIDATE_UNPROMOTED`，且「這三案被拒絕」不等於：

- 所有 role map 都由一個 sound／complete type system 描述；
- 所有 correctness-bearing references 都被完整遍歷；
- artifact type classifier 本身不會錯；
- signed map 的 origin 與 production execution 一致。

裁定：**部分解決；已知 bounded attack family 只在工程層關閉。**

### 4.8 Lean 實際 theorem scope：scope 已釐清，原始大義務沒有被證明

直接讀取 Lean source 後，實際 theorem scope 是：

| Lean 結果 | 精確性質 | 不是什麼 |
|---|---|---|
| `good_terminal_unfold` | `Iff.rfl` 的 definitional unfolding | 不是新的 correctness theorem |
| `robust_to_std` | 在 `WFStd`、`GLC0Robust` 與 `hInclude` 下，把 robust universal property specialize 到 standard runs | 不是一般 robust→standard inclusion theorem；`hInclude` 正是額外 premise |
| `terminal_no_output` | halt 不推出 output existence | 不是 P/NP result |
| `std_not_robust_countermodel` | standard GLC⁰ 可成立而 robust GLC⁰ 可失敗 | 不是 NTM-to-GLC bridge |
| gate lemmas | four-valued gates、applicability、unknown fail-closed | 不是 SemanticValidate correctness theorem |

Lean source 沒有 GCC、USRT、USEG、P、NP、SAT、resource-bounded complexity 或四層大箭頭 library。`fair` 是 predicate parameter；`zeroDebt` 是 predicate parameter；`Maximal` 是 extension-exclusion definition。即使 clean build、archive round-trip 與 axiom audit 都如交付所報告，它們最多證明「這些被寫入的 Lean 命題可編譯／可檢查」，不會把參數化 kernel 自動提升成作者原先想要的強語義。

裁定：**Lean scope 的誤讀已實質排除；原始 theorem obligations 尚未解決。**

### 4.9 AI-5 AEREC：自適應選擇已實作，複雜度上的 adaptive claim 未成立

AI-5 的實際 AEREC 行為是：

- 固定 v0.2.1 frozen parent hashes；hash drift 即 no-change；
- 先跑正例與已知負例，避免 reject-all 假解；
- 讀取歷史 probe，依 mismatch rate、prior 與 timing cost 排 fail-fast 順序；
- full mode 仍跑完整 corpus，故歷史排序不改變完整 acceptance decision；
- v0.2.1 的新 REF-TYPE 負例仍被接受，所以 selection 退回 `no-change-control`；
- batch snapshot 將 138 files／1,177,012 bytes 一次讀入，報告的 fixture-median aggregate 由 1682.701 ms 降到 222.530 ms，約 7.56×。

這是好的工程閉環，但不能被叫成已證明的「自適應複雜度計算論」：

1. 7.56× 只量到 validation batch 的 wall time，且是單機、固定 22 fixtures、9 repetitions 的 empirical result；不是 solver speedup，也不是 asymptotic improvement。
2. `adaptive_fixture_order` 是依歷史 corpus 的 data-dependent ordering；若要納入 uniform complexity，必須明確界定 history 的來源、長度、生成成本與是否可含 advice。
3. fail-fast order 的成本模型尚未把 history storage、probe generation、candidate construction、rollback、deployment、independent acceptance 與 worst-case full corpus cost 統一計入。
4. AI-5 的下一步「expected downstream cost avoided × failure probability / gate cost」是合理 heuristic，但尚未是 competitive ratio、regret、amortized bound 或 uniform controller theorem。
5. relocated candidate 仍需要外部 v0.1 schema compatibility path；這是 package topology 的現實缺口。

裁定：**AEREC 的 adaptive loop 只在工程層解決；若主張一般 adaptive algorithm 或 polynomial overhead，尚未解決，且暴露了 history-as-advice 的新 uniformity 問題。**

---

## 5. 這一輪真正改變了什麼，什麼沒有改變

### 5.1 改變了第一輪初判的部分

第一輪認為「這主要是研究綱領，缺少可審核形式核」。現在這個判斷需要細化：

- GLC⁰ 不再只有自然語言；已有可讀的 Lean signature、四象限 gate matrix、nonempty guard 與兩個重要 countermodels。
- `∀n∃A_n` 與 `∃A∀n` 的差異不再只是審稿人警告；已有 pointwise hardwired family 與 code-length-only repair 失效的具體反例。
- schema-only acceptance、untyped closure、mirror ledger 的缺陷都被真實負例擊中，再有版本化 bounded 修補。
- AEREC 不是只寫「會自我演化」；它真的使用歷史負例造成 no-change selection，且有可量測的 snapshot batching 結果。
- AI-7 的跨範式對照與這些直接 source／fixture／Lean evidence 相互一致；我把它視為獨立 corroboration，而不是權威。

因此，作為「形式化研究議程＋工程驗證方法」的成熟度，比 v1 高一級。

### 5.2 沒有改變第一輪核心否定的部分

下列事項仍完全不能由最新成果推出：

- GCC 的 model-independent dynamic invariant；
- 有效 uniform USRT compiler；
- 強 USEG 的 answer-blind quotient、soundness、completeness 與 lift；
- semantic losslessness 或 recovery 的一般 theorem；
- robust scheduler／fault model 與 polynomial wall-clock bound；
- 任一 GCC／USRT／USEG 大箭頭；
- GLC 與 P=NP 的 theorem-level equivalence；
- P=NP、P≠NP、或任何 barrier 已被跨越。

工程 candidate 的 15/15、1500 小型 2-SAT cases、31 fixtures、72 byte-identical outputs、7.56× throughput，全部不改變上述結論。

---

## 6. 出現更深的新問題

後續成果不是只填洞，也使以下問題變得不可再迴避：

### N1. `zeroDebt` 可被平凡化

若 `zeroDebt` 是 GLC0 的任意參數，形式化定理可在 `zeroDebt := True` 下通過。工程上的 debt ID fold 只驗 bookkeeping，不驗 token 的語義指涉。下一版必須給 obligation type、合法 add／retire transition、recovery certificate、soundness 與 completeness。

### N2. robust 四象限的實作只是 singleton deterministic I0

候選中的 robust pass 來自「唯一 pinned finite run 成功，因此 singleton family nonempty、maximal、fair」。這可以是合法 I0 model，但不能代表一般 scheduler、reroute、rollback、restart 或 fault nondeterminism。若不明示這個限制，`robust` 名稱會再次超出 theorem scope。

### N3. signed measurement 不是 independent measurement

Ed25519 能證明某個 test signer 簽了某些 bytes，不能單獨證明 bytes 是由 production sandbox、真實 clock、peak space 或 transition execution 產生。若 provenance theorem 依賴 origin，origin attestation／sandbox authority 必須變成 formal premise，而不是藏在 `trusted artifact root` 的描述中。

### N4. candidate 的 mechanism map 是 hardcoded bounded policy

v0.2.2 對 PARITY／2-SAT 的 role map、family context、transition rule 與 oracle 都是明確的，這是優點；但 unsupported family 只能 unknown／fail closed，不能因此推出一般 SAT、NP 或 arbitrary GLC closure。

### N5. candidate projection 與 semantic acceptance 有意分離

terminal-only projection 仍可能對 uniform stream 與 per-length table 給出相同 projection；差別由外部 admission／provenance／advice gates 判定。這是合理架構，但代表「projection 相同」不是 semantic equivalence theorem，且任何只讀 projection 的消費者都不能獨立推出 closed computation。

### N6. AEREC history 可能成為未宣告 advice

只要 adaptive controller 依過往 mismatch、fixture corpus、failure cost 或 candidate lineage 作選擇，就必須明列 history 是固定常數、uniformly generated input，還是 advice／training state。否則「自適應」可能把 nonuniform information 從演算法主體移到控制平面。

### N7. Lean gate layer 與 Python validator 沒有 refinement theorem

Lean 的 gate applicability reference 與 Python 的 v0.2.2 validator 是兩個 artefact。AI-4 已明說 Lean artifact 只是 gate-matrix reference，不是 validator proof。下一版若要宣稱形式化保證工程 validator，必須建立 refinement／extraction／correspondence theorem；否則兩者只能並列為不同證據。

---

## 7. 最小 theorem obligations（下一個 theorem-grade gate）

以下是我認為最小、不可再用「之後補」帶過的義務。它們不要求現在解出 P/NP；它們要求每個箭頭先成為可審的 theorem statement。

### 7.1 共通基礎

1. 固定 alphabet、input encoding、language／task domain、output type、machine／system encoding。
2. 固定 deterministic／nondeterministic transition、halt、accept、reject、non-halting 與 run semantics。
3. 每個成本明列 input length、program length、advice、precision、space、parallel work、construction、update、decode、recovery、verification 與 restart。
4. 每個 `∃`／`∀` 明列順序；禁止以 `∀n∃A_n` 代替 `∃A∀n`，也禁止以未計價 history 代替 uniform controller。
5. 將 claim 標為 Definition、Lemma、Conditional、Counterexample、Experiment 或 Theorem；formal compile 不可自動改標。

### 7.2 GCC

1. 以固定演算法 witness 或明確的 algorithm set 取代未定義的「某個正確算法」。
2. 若保留 admissible model family，給有效 enumeration、primitive cost、word／bit model、precision 與 pairwise polynomial compiler。
3. 證明 standard machine simulation 的方向、overhead 對 model description 與 input length 的依賴。
4. 明確排除 unit-cost SAT／oracle／unbounded advice／infinite precision；若保留 nonuniform version，正式命名 P/poly 或相應 class。
5. 最後選擇：證明 GCC 是 P 的 machine-invariance restatement，或給出一個不等同 P membership 的新 invariant。

### 7.3 USRT

1. 定義 machine／clock code 與 total effective `U`；不能只用 extensional `∀N∃D_N`。
2. 定義 `D_N` 的 construction、code、initialization、compile、decode 與 online runtime。
3. 對 NTM 使用 existential acceptance，不把所有 branch 的 output 強行設成同一 decision bit。
4. 證明 `U` 的 soundness、completeness、combined-input polynomial bound；若宣稱與 P=NP 等價，證明兩方向而非只寫直覺。

### 7.4 USEG

1. 固定 answer-blind admissibility；`Z_0`、generator、quotient、decode 不得讀 `χ_L(x)` 或答案表。
2. 給一個 uniform generator，並計入 generator code、preprocessing、advice、state size、step count、peak size、decode、lift。
3. 給 quotient 的有效 construction、soundness、completeness；若是 search／witness／counting，給相應 witness lift，不得只證 decision bit。
4. 先在 2-SAT、Horn-SAT、XOR-SAT 或 bounded-treewidth 類別交付一個非平凡 theorem；不要由單一 I0 fixture 外推一般 NP。

### 7.5 GLC

1. 先固定 GLC⁰ 的 semantic domain：decision-only、search、witness、counting 或 optimization，不能混用。
2. 將 loss debt 定義成可辨識的 obligation object；證明 add／retire／recovery 的 soundness、completeness 與 final zero-debt 意義。
3. 形式化 `Runs_adm` 的生成方式、nonempty、Maximal 與 fairness；選 weak／strong／bounded fairness，並說明 fault budget。
4. 對 standard／robust × neutral／bounded 四象限各給完整 theorem signature；neutral 仍需完整 ledger，bounded 才多 threshold。
5. 若要和 P 連接，證明每個 admissible run 的 total work、peak space、delay、recovery overhead 具有同一 uniform polynomial bound；eventual completion 本身不夠。
6. 給一個真正 nondeterministic branch model 與 robust scheduler model 的分離及 translation theorem，不能用 singleton deterministic I0 代替。

### 7.6 Schema、provenance、AEREC

1. 若工程 validator 仍要承擔「admission sufficient」語言，需有對 SchemaConsistency／SemanticValidate／DerivesRecord 的 formal soundness theorem；否則標為 executable acceptance policy。
2. provenance 要求可驗的 execution origin、measurement authority 或明示 trusted-sandbox premise；test signature 不能獨自承擔這個 premise。
3. typed closure 要給角色集合的 completeness、artifact type classifier 的 scope 與 cycle／missing／unknown classification theorem。
4. AEREC 要定義固定 controller、history encoding、history cost、candidate generation cost、selection overhead、worst-case acceptance cost；若只依 empirical failure probability，稱 heuristic policy，不稱 complexity theorem。
5. AI-3 Lean 與 AI-4 Python 若要合併成一個形式保證，需給 refinement／correspondence proof；否則清楚分為 formal reference 與 bounded implementation。

---

## 8. 發表級別更新

相對第一輪，發表判定改成三軌：

| 投稿定位 | v2 建議 |
|---|---|
| 研究綱領／position／formalization agenda | **可繼續，接近可送審**；需把 GCC／USRT／USEG 箭頭、GLC semantic debt、open obligations 明確標為 conjecture／agenda。 |
| bounded verification／artifact engineering paper | **有條件可送審**；可報告 AI-2 負例、AI-3 Lean GLC0、AI-4 I0、AI-5 AEREC，但標題與摘要不得寫 P/NP breakthrough、general provenance theorem 或 general SAT result。需保留 candidate-unpromoted 與 measurement limits。 |
| 傳統複雜度理論 theorem paper，宣稱新 class 或 P/NP characterization | **仍不接受；major revision**。核心缺口是 uniform compiler、model simulation、USEG lift、semantic debt theorem、robust run model 與完整 resource quantifiers，而不是更多 fixture 數量。 |

因此 v2 比 v1 更正面的地方，是「研究與工程方法本身已形成可審對象」；沒有改變的地方，是「定理紙的核心結論仍未開始被證明」。

---

## 9. 最終覆審裁定

### 已實質解決

- GLC⁰ 四象限的 gate applicability 與 nonempty／fail-closed definition kernel；
- standard 與 robust 不可互換的基本 countermodel；
- GLC-first 是研究依賴而非數學 implication 的文字與現況邊界；
- barrier 名稱未被誤用為已突破，且目前正確標示為 not yet engaged；
- v0.2.1 已知 schema／provenance 反例被保留為 negative corpus，而不是被綠燈覆蓋。

### 部分解決

- pointwise nonuniformity、P/poly 邊界與 uniformity diagnostics；
- NP existential branch 與 robust all-run 的概念分離；
- semantic loss debt 的 obligation／event bookkeeping 方向；
- REF-TYPE 已知三變體的 bounded 修補；
- Lean theorem scope 的準確界定。

### 只在工程層解決

- PROV-DERIVE 的 pinned replay、resource folds 與 signed measurements；
- SchemaConsistency／SemanticValidate 的雙層 validator 架構；
- 31 fixtures、1500 小型 2-SAT cases、72 byte-identical outputs；
- AEREC 的 no-change、歷史負例排序與 immutable snapshot throughput；
- v0.2.2 candidate 的 known-attack rejection。

### 尚未解決

- admissible model family 與 GCC model invariance；
- rate cone／rate conversion theorem；
- effective uniform USRT compiler；
- general USEG quotient、sufficiency、lift；
- semantic losslessness／recovery theorem；
- general robust scheduler／fairness／fault／polynomial delay；
- GCC／USRT／USEG 與 P=NP 的大箭頭；
- P/NP 或任何 lower-bound barrier crossing result。

### 出現更深的新問題

- Lean `zeroDebt` 可由任意 predicate、甚至 trivial predicate 實例化；
- robust I0 的 singleton deterministic semantics 不能代表一般 robust system；
- signed raw measurement 不等於獨立 execution provenance；
- history-fed AEREC 可能成為未宣告 advice，且 adaptation cost 尚未入帳；
- Lean gate kernel 與 Python validator 之間沒有 refinement theorem；
- role-aware closure 修補後仍需證明 classifier／origin／typed-closure 的完整性，而非只累積更多負例。

**最終判定：**最新成果實質改變了我對「形式化與工程紀律成熟度」的初判；沒有改變我對「傳統複雜度 theorem readiness 與 P/NP 結論」的初判。這份工作目前最可信的身份，是一個已經開始產生真實局部 lemma、countermodel 與 bounded validation artifact 的研究程序，而不是已完成的 P/NP 理論。

---

## 10. 凍結聲明

本檔為 **AI-6 現況覆審報告 v2.0**。寫入後凍結，不覆寫第一輪盲讀報告，不修改任何授權來源，不作 Board 發布，不對 AI-1 至 AI-5 發送訊息。後續若要更改，應建立新的版本並保留本檔位元組。

