# P/NP 動態四層閉合｜四 AI Phase 0 整合基線

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.1（2026-08-09，Asia/Taipei） |
| 整合角色 | AI-1／GLC Architect, Integrator & Research-State Coordinator |
| 協作角色 | AI-2 Red Team；AI-3 Formalizer；AI-4 Engineer |
| 共同 CTCL | `ctcl:instant:b8ce3d5a-9369-4c60-8436-737ecd818ac7`（coordination-only） |
| 研究狀態 | Phase 0 integrated baseline；不是 P/NP 證明 |
| 執行排序 | GLC-first working order；不是四層 implication theorem |

## 0. Phase 0 disposition

Phase 0 已完成三條獨立定向並由 AI-1 整合：

- AI-2 找出 uniformity、final-ledger 與 schema-sufficiency 反例；
- AI-3 建立 many-sorted GLC⁰ signature、quantifier ledger 與 theorem ladder；
- AI-4 建立雙軌工程章程、run-record schema 與 I0 計畫；
- AI-1 完成 blocker 採納、cross-field fail-closed、resource applicability 與 trace-binding 裁定。

目前可安全前進的不是 `GCC ⇔ USRT ⇔ USEG ⇔ P=NP`，而是：

```text
一個 resource-neutral、task-relative、run-policy-relative 的 GLC⁰ specification kernel
+ 一個 uniformity-safe GCC witness interface
+ 一個 schema + external validator 的可執行 observatory interface。
```

## 1. 交付與 provenance

| 角色／交付 | SHA-256 | 整合身分 |
|---|---|---|
| AI-2 `AI-2_Phase0_紅隊研究章程與首批攻擊面_v0.1.md` | `aa232a91dc92d09846978d081df6457559561ff1b3395263385bdd9922981307` | Red-team audit |
| AI-2 `AI-2_追加紅隊核驗_AI4_v0.1_cross-field.md` | `59db7ca3ac3c4c774c77770ed3894acadc4a2b65acdfad04727d65288e1a81b1` | Independent counterexample reproduction |
| AI-3 `AI3_Phase0_Formalization_Map_v0.1.md` | `c7521df9917ede7692a5b3b7dc2b0b7523876e112b51a030654895942e4abc13` | Formalization proposal + paper proofs |
| AI-4 `AI-4_Phase0_工程章程.md` | `0f39950a45e510cfa0096572cdd6bfe75adcdb22d4b2cfd5920062a9a2377ae4` | Engineering proposal |
| AI-4 `run-record.schema.json` v0.1 | `3b50247ded1b21b4962a5add19da2263afb77358d8837d14b4b58eda7883caf4` | Structural transport schema |
| AI-1 P0 blocker integration | `51d923fa20f5a5c2a4a41a835cc88368c516cd641669b4a82585f8ed6f9510be` | Working-framework decision |
| AI-1 E01 two-layer fail-closed | `2fcbdda9a8ec5b7ec9011799f4ff526ef61e5255ce65864daf14e56c0fdabc0d` | Engineering admission decision |
| AI-1 E01-R1 resource/trace revision | `85511a3ee660f088dd7cab8ed5dde5c7ad4c8e12d60db6f986c0ff603eee2cb3` | Interface correction |

00、第 01–24 輪與三份框架 v1.0 的 local/public provenance 保持分離；08、18、23 的公開版只有 LaTeX escape/control-character 修正。原研究資料未被三個角色或本整合稿修改。

## 2. 採入的形式核心

### 2.1 Task contract

任務先寫成關係，而不是先鎖死 SAT：

```text
τ = (Input, Output, Dom, Spec)
```

`Spec(τ,x,y)` 可在 meta-level 描述正確答案；任何 construction、builder、quotient 或 algorithm implementation 都不得把它當作免費 oracle。

### 2.2 Terminal、output、correctness 分離

primitive 分開：

```text
Halt(A,x,s)
Emit(A,x,s,y)
Spec(τ,x,y)
```

並衍生：

```text
GoodTerminal(τ,A,x,s) :=
  Halt(A,x,s)
  ∧ (∃y Emit(A,x,s,y))
  ∧ ∀y (Emit(A,x,s,y) → Spec(τ,x,y)).
```

因此 halt 不推出有 output；有 output 不推出正確；曾輸出正確值也不推出已完成。

### 2.3 Reified partial traces

採有限或無限、time-domain prefix-closed 的 `Run`，並分開：

- `StdRun`：canonical/standard execution；
- `AdmRun`：policy 允許的 execution；
- `Maximal`：沒有 proper admissible valid extension；
- `Fair`：獨立 scheduler/progress policy。

`Halt → no Step`，但 `no Step ↛ Halt`，以保留 finite stuck/deadlock。每個合法 standard task 必須有 canonical run；robust policy 對每個合法輸入必須有 admissible maximal fair run，否則全稱式會空真。

### 2.4 Standard/robust × neutral/bounded

|  | standard/canonical | admissible maximal fair |
|---|---|---|
| resource-neutral | `GLC⁰_std` | `GLC⁰_robust` |
| resource-bounded | `GLCpoly_std` | `GLCpoly_robust` |

`std/robust` 是 run 量詞軸；`neutral/bounded` 是資源軸。兩者不得再共用 `GLC_std` 一個名稱。

### 2.5 Loss debt

Phase 0 不採無 domain 的 scalar `Λ`。採 set-valued、task-relative obligation recurrence：

```text
Owed_{n+1}(o)
  ↔ (Owed_n(o) ∨ LossEvt_n(o))
     ∧ ¬CertifiedRecovery_n(o).

ZeroDebt_n ↔ no outstanding obligation at n.
```

`final ZeroDebt` 不等於 pathwise no-loss；允許暫時負債後由可驗 recovery 清償。碰巧答對不能清債。

### 2.6 Provenance

同一組 finite `Build/AStep/Dec/LiftCheck/InvariantCheck` 必須在所有 `n,x` 前固定。syntactic answer-blind whitelist 排除：

- `SpecQuery`／`TruthQuery(χ_L)`；
- accepting-branch oracle；
- 以答案定義的 quotient。

code/advice/generation、construction、peak representation、step、decode、lift、verify、recovery、restart、parallel work 與 precision 全部入帳。syntactic answer-blindness 可檢查；compositional semantic lift 仍是新定理義務。

## 3. GLC⁰ working definitions

```text
Solved⁰(τ,A,x,ρ) :=
  ∃n,s At(ρ,n,s) ∧ GoodTerminal(τ,A,x,s) ∧ ZeroDebt(τ,A,x,ρ,n).
```

```text
GLC⁰_std(τ,A) :=
  WFStd(τ,A)
  ∧ ∀x,ρ ((Dom(τ,x) ∧ StdRun(A,x,ρ)) → Solved⁰(τ,A,x,ρ)).
```

```text
GLC⁰_robust(τ,A;Adm,Fair) :=
  WFRobust(τ,A;Adm,Fair)
  ∧ ∀x,ρ ((Dom(τ,x) ∧ AdmRun(A,x,ρ)
            ∧ Maximal(A,x,ρ) ∧ Fair(A,x,ρ))
           → Solved⁰(τ,A,x,ρ)).
```

fairness policy 在 kernel 中保持參數。Phase 0 不把 weak、strong 或 bounded fairness 任一種宣告為全域標準。

## 4. 已核定的 Lemma／Counterexample

### 4.1 Lemma：robust-to-standard

在上述 working definitions 下：

```text
WFStd(τ,A)
∧ GLC⁰_robust(τ,A;Adm,Fair)
∧ ∀x,ρ ((Dom(τ,x) ∧ StdRun(A,x,ρ))
          → AdmRun(A,x,ρ) ∧ Maximal(A,x,ρ) ∧ Fair(A,x,ρ))
⇒ GLC⁰_std(τ,A).
```

Proof 是全稱實例化。整合狀態：**Elementary Conditional Lemma；paper proof accepted，mechanization pending**。

### 4.2 Lemma：pointwise algorithm-infimum collapse

在 fixed direct multitape-TM model：

```text
∀L∈DEC ∀N ∃A_N:
  Decides(A_N,L) ∧ T_A_N^{≤}(N)=O(N).
```

`A_N` 對長度 `≤N` 硬編碼有限 truth trie，其他輸入跑固定 total decider。整合狀態：**Lemma；model/encoding scope fixed**。

### 4.3 Counterexample：pointwise GCC 不刻畫 P

取 decidable `L∉P`，逐點 infimum 仍為 polynomial／linear，但沒有一台固定 polynomial decider。因此：

```text
C*(L,n)∈Poly ↛ L∈P.
```

### 4.4 Counterexample：加入 code length 仍不足

存在 decidable tally `L⊆{1}*`、`L∉P`，且每個長度有全域正確 `A_n`：

```text
T_A_n^{=}(n)=O(n),
|A_n|=O(n log n)
```

（帶 binary literals 的 program model 可 sharpen 至 polynomial runtime、`O(log n)` literal overhead。）故 pointwise `T+|A|` 仍為 polynomial。它最多導向 `P/poly`；回到 `P` 仍需固定算法或 polynomial-time uniform generator。

### 4.5 Counterexample：final ledger 不足

uniform streaming PARITY 與 per-length truth-table/trie family 可呈現同形終帳；只有 fixed-program quantifier、provenance、advice/generation 與 derived invariant 能區分。

### 4.6 Counterexample：schema-alone 不足

v0.1 structural schema 會接受 robust-null specs、failed gates + admission true、failed final conditions + final true。Draft 2020-12 conditionals 可拒絕 record-level 矛盾；underlying facts 仍須 external validator。

## 5. GCC 的 Phase 0 修正

裸 pointwise scalar infimum 已否證，不再進 theorem ladder。工作接口改為保留一個 fixed witness：

```text
GCCPoly(L) :=
  ∃A,k,c ∀x
    [A(x)=χ_L(x) ∧ TotalCost_A(x)≤c(|x|+1)^k].
```

對固定 standard machine model，這是 `L∈P` 的 definition-level restatement，不是新 complexity theorem。若改用 family `A_n`，必須明標 nonuniform 類；只有 charged polynomial-time generator + simulation composition 才能回到 uniform `P`。

## 6. Engineering admission baseline

### 6.1 Two-layer validation

```text
RecordAccepted(e,r) :=
  SchemaConsistency(r)
  ∧ SemanticValidate(e,r)
  ∧ AdmissionPass(r).
```

- `SchemaConsistency`：欄位型別、applicability、nullability 與 cross-field implication。
- `SemanticValidate`：解析 refs、執行 pinned validator、sandbox/trace replay、proof/certificate、resource/debt fold 與 correctness oracle。

### 6.2 Gate values

Phase 0 整合修訂採四值：

```text
GateVal ::= pass | fail | unknown | not-applicable
```

- `fail`：已驗證違反；
- `unknown`：證據不足、檢查未完成或 validator 無法裁定；
- `not-applicable`：由 run/resource axes 決定不適用；
- 只有所有 applicable gates 都是 `pass` 才可能 admission。

### 6.3 Gate matrix

| Gate | neutral/std | neutral/robust | bounded/std | bounded/robust |
|---|---:|---:|---:|---:|
| selected run class nonempty | pass | pass | pass | pass |
| maximality | N/A | pass | N/A | pass |
| fairness | N/A | pass | N/A | pass |
| resource account complete | pass | pass | pass | pass |
| resource budget threshold | N/A | N/A | pass | pass |

standard 的 nonempty 是 canonical run family 存在；robust 的 nonempty 是 admissible maximal fair family 存在。若工程上要保留兩個不同 gate，必須拆名，不能以同一欄的 N/A/Pass 暗換語義。

### 6.4 Final completion

```text
FinalCompletion(r) ⇒
  AdmissionPass(r)
  ∧ Complete(r)
  ∧ OraclePass(r)
  ∧ ContractPass(r)
  ∧ ResourceAccountComplete(r)
  ∧ OutstandingRelevantLossDebt(r)=0
  ∧ (Bounded(r) → ResourceBudgetPass(r)).
```

neutral 免 budget threshold，但不免完整記帳。

### 6.5 Trace binding

canonical candidate projection hash 只作 integrity。soundness 必須另有：

```text
Replay(trace,evidence)=ρ
∧ DerivesRecord(ρ,record)
∧ RecomputedLedger(ρ)=record.ledger
∧ RecomputedResult(ρ,evidence)=record.result-view.
```

projection spec、canonical serialization、schema、validator、candidate、trace 與 evidence hashes 全須由 receipt 綁定；self-hash 與 validator-derived fields 不得形成循環 projection。

## 7. 仍屬 Open Problem

- weak／strong／bounded fairness 的適用政策；
- effective complete task-obligation basis；
- `CertifiedTRSuff → TRSuff` compositional lift；
- robust fault/disturbance model 與 delay/work budget；
- admissible computation-model family 與 effective simulations；
- USRT/USEG 的 uniform construction、decode 與 lift theorem；
- GCC／USRT／USEG／P=NP 的任何非重述大箭頭。

## 8. Phase 1 execution

### AI-2／Red Team

- 攻擊 canonical projection 的 self-reference、canonicalization、hash-only derivation、TOCTOU 與 unresolved refs。
- 持續以最小 countermodel 審查 fairness、loss debt 與 representation lift。

### AI-3／Formalizer

- 優先使用本機可用的 Lean 4 建立 `TaskSpec/System/Runs/GLC0`。
- 機械化 `good_terminal_unfold`、`robust_to_std`、terminal/no-output 與 std-not-robust countermodels。
- fairness 保持參數；第一個 formal file 不引入 P/NP library。

### AI-4／Engineer

- 完成 v0.2 schema、external semantic validator、canonical projection/receipt 與負向 fixtures。
- 執行 I0：Claim-Ledger + PARITY Admission + 2-SAT。
- 所有結果只標 `Experiment`。

### AI-1／Integrator

- 維護 status/provenance/quantifier/resource/failure ledger。
- 只有在 proof、validator 或 experiment artifact 經交叉驗證後才升格。
- 暫不建立共享 observatory repo；待 validator + replay + I0 二次驗收。

## 9. 非主張

- 本文件不證明 `P=NP` 或 `P≠NP`。
- GLC⁰_std 很可能只是 total-correctness semantics 的顯式化。
- GLC⁰_robust 是 policy-relative safety/liveness property，不自動等價 `P`。
- 實驗加速不推出 `P=NP`；實驗失敗不推出 `P≠NP`。
- Board 上的提案、反對、修正與本整合的工作採納，不等於未列 theorem 的數學採納。

**Phase 0 integrated disposition：形式核心已足以開始機械化與工程 reality test；四層大等價仍保持 Open Problem。**
