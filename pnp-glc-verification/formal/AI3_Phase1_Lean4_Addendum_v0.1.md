# AI-3 Phase 1：GLC0 Lean 4 最小機械化 addendum v0.1

- 日期：2026-08-09（Asia/Taipei）
- 狀態：**Compiled formalization artifact**
- Phase 0 baseline：`AI3_Phase0_Formalization_Map_v0.1.md`，SHA-256
  `C7521DF9917EDE7692A5B3B7DC2B0B7523876E112B51A030654895942E4ABC13`
- 邊界：不引入 Mathlib、SAT、P/NP、GCC、USRT 或 USEG library；不主張四層等價。

## 1. Phase 1 definition revisions

### 1.1 Shared nonempty-run gate

`runClassNonempty` 對 standard 與 robust 都 applicable，但由 mode 決定其語義：

```text
RunClassNonempty standard = CanonicalRunFamilyExists
RunClassNonempty robust   = AdmissibleMaxFairRunFamilyExists
```

Lean declarations：

- `GLC0.CanonicalRunFamilyExists`
- `GLC0.AdmissibleMaxFairRunFamilyExists`
- `GLC0.RunClassNonempty`
- `GLC0.runClass_applicable`
- `GLC0.standard_runClass_meaning`
- `GLC0.robust_runClass_meaning`

這避免把 standard 的 canonical-run existence 誤標為 N/A，也避免把 robust
的 nonempty/maximal/fair 三義混成同一個沒有 mode 的 boolean。

### 1.2 Four-valued gates

`GateVal` 已機械化為：

```text
pass | fail | unknown | notApplicable
```

`unknown` 表示證據不足或驗證尚未完成；`fail` 表示已建立違反。兩者都不能滿足
`GatePass`。Lean 已證：

- `fail_fails_closed : ¬ GatePass .fail`
- `unknown_fails_closed : ¬ GatePass .unknown`
- `unknown_blocks_admission`：任一 applicable gate 為 unknown 時，
  `AllApplicablePass` 不成立。

### 1.3 Applicable gate matrix

| run mode | resource regime | run-class nonempty | maximality | fairness | account completeness | budget |
|---|---|---:|---:|---:|---:|---:|
| standard | neutral | applicable | N/A | N/A | applicable | N/A |
| standard | bounded | applicable | N/A | N/A | applicable | applicable |
| robust | neutral | applicable | applicable | applicable | applicable | N/A |
| robust | bounded | applicable | applicable | applicable | applicable | applicable |

`ApplicableResource accountCompleteness` 對兩種 resource regime 都成立；
`ApplicableResource budget` 當且僅當 resource-bounded。neutral 免除的是 threshold，
不是完整 ledger。

## 2. Lean module map

| Module | Formalized content |
|---|---|
| `GLC0.TaskSpec` | `dom` 與 `spec` task contract |
| `GLC0.System` | 固定 algorithm witness；`init/step/halt/emit` 分離 |
| `GLC0.Runs` | partial trace、`At/Prefix/ProperPrefix/Maximal`、run policies、兩種 nonempty-run semantics |
| `GLC0.Core` | `OutDef/OutSound/GoodTerminal/Solved0/GLC0Std/GLC0Robust` |
| `GLC0.Countermodels` | terminal/no-output 與 well-formed std-not-robust models |
| `GLC0.Admission` | four-valued gates、run/resource applicability、unknown fail-closed |

Fairness 是 `RunPolicy.fair` 的抽象 predicate；本階段沒有選 weak、strong 或
bounded fairness。Loss debt 以 `zeroDebt` predicate parameter 注入 `Solved0`，
尚未假裝一般 obligation basis 已存在。

## 3. Mechanized results and epistemic status

### 3.1 Definition restatement

```lean
good_terminal_unfold :
  GoodTerminal task sys x s ↔
    sys.halt x s ∧ OutDef sys x s ∧ OutSound task sys x s
```

Lean kernel audit：不依賴任何 axioms。這是 definitional unfolding，不是新的
correctness theorem。

### 3.2 Elementary conditional lemma

```lean
robust_to_std :
  WFStd task sys policy →
  GLC0Robust task sys policy zeroDebt →
  (∀ x ρ, task.dom x → policy.std x ρ →
    policy.adm x ρ ∧ Maximal sys policy x ρ ∧ policy.fair x ρ) →
  GLC0Std task sys policy zeroDebt
```

Lean kernel audit：不依賴任何 axioms。證明只是將 standard run inclusion
代入 robust 全稱式。

### 3.3 Counterexample: terminal does not imply output

`terminal_no_output` 建立：

```text
halt () () ∧ ¬ OutDef () ()
```

`terminal_no_output_not_good` 進一步否證該 halted state 是
`GoodTerminal`。Axiom audit 只列 Lean standard `propext`，沒有 custom axiom。

### 3.4 Counterexample: standard does not imply robust

三狀態系統有 `start → good` 與 `start → bad`。standard policy 只選
`goodRun`；admissible policy 同時允許 `goodRun` 與 `badRun`，兩者都是
valid、maximal、fair，故不是 empty-family vacuity。

- `split_wfStd`：standard run family well formed。
- `split_wfRobust`：admissible maximal fair family well formed。
- `split_glc0Std`：standard GLC0 成立。
- `std_not_robust_countermodel`：standard GLC0 成立且 robust GLC0 不成立。

Axiom audit 只列 Lean standard `propext`、`Quot.sound`；沒有 custom axiom。

## 4. Toolchain and reproducible commands

```text
Lean (version 4.30.0, x86_64-w64-windows-gnu,
      commit d024af099ca4bf2c86f649261ebf59565dc8c622, Release)
Lake version 5.0.0-src+d024af0 (Lean version 4.30.0)
```

專案由 `lean-toolchain` 鎖定 `leanprover/lean4:v4.30.0`。

```powershell
lake clean
lake build
lake env lean AxiomAudit.lean
```

2026-08-09 clean build：

```text
Built GLC0.TaskSpec
Built GLC0.System
Built GLC0.Runs
Built GLC0.Core
Built GLC0.Countermodels
Built GLC0.Admission
Built GLC0
Build completed successfully (9 jobs).
```

`rg` audit 未找到 `sorry`、`admit`、`axiom` 或 `opaque` declarations。

## 5. Archive round-trip verification

交付 ZIP 解壓到獨立目錄後：

1. `SHA256SUMS.txt` 全部比對成功：`SHA256SUMS_OK=True`。
2. 從解壓內容執行 `lake build`：成功，9 jobs。
3. 從解壓內容執行 `lake env lean AxiomAudit.lean`：成功。

因此編譯證據對應實際交付 archive，不只對原工作目錄成立。

## 6. Hashes

- Source manifest `SHA256SUMS.txt`：
  `7959F5F13D039C9996E153CAA4DD8074F6333105006F5FB2ABC905D7BB94D3CC`
- Source archive `AI3_Phase1_GLC0_Lean4_v0.1.zip`：
  `712D331E7000F59DDE83569F78175F2B09306CBB312CD69F5B3839D79BD932F4`
- Archive size：7,629 bytes。

每一 source file 的獨立 SHA-256 位於 archive 內的 `SHA256SUMS.txt`。

## 7. Remaining obligations

- Fairness policy 仍是參數；尚未選 weak/strong/bounded。
- `zeroDebt` 尚未連接一般 obligation/recovery certificate recurrence。
- `Maximal` 已形式化為 admissible proper-extension exclusion，但尚未建立
  finite/infinite trace encoding 的一般等價定理。
- Admission schema 的 `SchemaConsistency/SemanticValidate/DerivesRecord`
  尚未整體機械化；本階段只完成 gate type/applicability/fail-closed kernel。
- GCC uniformity、resource-bounded GLC 與所有四層 arrows 仍不在本 Lean project。
