# P/NP 動態四層閉合框架
## 研究交接與後續實行建議 v1.0

- **專案性質**：長期理論研究／形式化／演算法實驗交接文件
- **目前定位**：啟發式 Characterization Program，不宣稱已證明 $P=NP$ 或 $P\neq NP$
- **主導概念**：P/NP 動態四層閉合框架
- **核心四層**：
  - $\mathrm{GCC}$：Global Computational Complexity，全域計算複雜度態
  - $\mathrm{USRT}$：Universal State-Rate Transformation，全稱狀態速率變換態
  - $\mathrm{USEG}$：Universal Effective Sequence Generation，全稱有效序列生成態
  - $\mathrm{GLC}$：Global Lossless Completion，全域無損完成態
- **交接目的**：使後續 AI、研究者或形式化工具可以在不重新猜測專案意圖的情況下，持續推進定義、數學推導、形式化證明、演算法實作、反例測試與障礙映射。
- **關聯主稿**：`P_NP_動態四層閉合框架_啟發式研究提案_v1.0.md`

---

# 0. 最重要的總原則

本專案目前**不是**一篇「已證明 $P=NP$ 或 $P\neq NP$」的論文。

目前正確定位是：

$$
\boxed{
\text{P/NP Characterization Program}
}
$$

研究目標是：

> 將傳統 $P/NP$ 問題重新投影到資源、動態速率、有效序列生成與最終無損完成四個層面，研究這些描述與標準複雜度類之間的精確邏輯關係。

任何後續 AI 必須避免將：

- 啟發式重描述；
- 定義等價；
- 受限模型定理；
- 實驗觀察；
- 局部形式化結果；

誤寫成：

$$
P=NP
$$

或：

$$
P\neq NP
$$

的完整證明。

---

# 1. 目前框架的核心結構

## 1.1 第一層：GCC

### 名稱

$$
\boxed{
\mathrm{GCC}
=
\text{Global Computational Complexity}
}
$$

### 目的

研究一個問題在「合理、可接受、彼此多項式可模擬」的計算模型族中的全域複雜度類。

不應使用單一實體機器的絕對 clock time 作為 GCC。

建議定義 admissible computation-model family：

$$
\mathfrak M_{\mathrm{adm}}
$$

至少要求：

1. 有限描述；
2. uniform；
3. 不含 oracle；
4. 不含不可計算 advice；
5. 不含免費無限精度常數；
6. 模型之間具有 polynomial simulation 關係。

候選形式：

$$
\mathrm{GCC}(L)
=
[T_M^L]_{\equiv_{\mathrm{poly}}}.
$$

### 後續任務

- 嚴格定義 $\mathfrak M_{\mathrm{adm}}$；
- 明確指定 equivalence relation；
- 分清 deterministic / nondeterministic model；
- 驗證 GCC 是否只是標準 $P$ 的機器不變性重描述；
- 找出 GCC 中真正非平凡的新內容。

---

## 1.2 第二層：USRT

### 名稱

$$
\boxed{
\mathrm{USRT}
=
\text{Universal State-Rate Transformation}
}
$$

### 目的

把 NP 型 polynomial nondeterministic computation 的「狀態完成速率」轉換成 deterministic polynomial completion-rate process。

給定演算法／機器 $A$：

$$
S_A(x,0)
\rightarrow
S_A(x,1)
\rightarrow
\cdots
$$

定義完成時間：

$$
\tau_A(x)
=
\min\{t:S_A(x,t)\in H_L(x)\}.
$$

最壞情況：

$$
T_A(n)
=
\max_{|x|\le n}\tau_A(x).
$$

可用完成速率：

$$
R_A(n)
=
\frac{1}{1+T_A(n)}.
$$

### 關鍵限制

「速率近似」不能要求：

$$
R_D(n)\approx R_N(n)
$$

的數值接近。

真正應要求：

$$
T_D(n)\in\operatorname{poly}(n)
$$

或兩者處於同一個：

$$
\boxed{
\text{polynomial completion-rate cone}.
}
$$

### 正確量詞方向

應優先研究：

$$
\exists \mathcal U
\;
\forall (N,p)
\;
\exists q_{N,p}\in\operatorname{poly}
\;
\forall x.
$$

不要無意間強化成：

$$
\exists \mathcal U
\exists K
\forall N
\forall x
$$

都使用同一固定 exponent $K$。

後者一般比標準 $P=NP$ 強得多。

---

## 1.3 第三層：USEG

### 名稱

$$
\boxed{
\mathrm{USEG}
=
\text{Universal Effective Sequence Generation}
}
$$

### 目的

研究 nondeterministic computation 中大量可能的 computation sequences，能否被 deterministic polynomial process 壓縮成一條「決策充分」的有效序列。

對 NTM $N$ 與輸入 $x$：

$$
\Gamma_N(x)
=
\{\gamma_1,\gamma_2,\ldots\}.
$$

NP 接受：

$$
x\in L
\iff
\exists\gamma\in\Gamma_N(x):
\operatorname{Accept}(\gamma).
$$

### 絕對禁止的錯誤

不要把：

$$
|\Gamma_N(x)|
$$

本身當成複雜度下界。

一個 $P$ 問題可以被故意設計成具有指數多條無用 nondeterministic branches。

真正應研究：

$$
\boxed{
\text{effective / decision-relevant sequence cardinality}
}
$$

以及 sequence quotient：

$$
\Gamma_N(x)/{\sim_D}.
$$

候選有效基數：

$$
\kappa_{\mathrm{eff}}(N,x)
=
|\Gamma_N(x)/{\sim_D}|.
$$

但必須把構造 $\sim_D$ 的成本算入：

$$
T_{\mathrm{construct}}(\sim_D).
$$

否則會出現循環：

> 先把 SAT 解掉，再宣稱所有路徑其實只剩兩個等價類。

### USEG 的最低合法版本

需要存在 deterministic sequence generator $G_N$：

$$
Z_0,Z_1,\ldots,Z_m
$$

使：

$$
m\le\operatorname{poly}(n),
$$

$$
|Z_t|\le\operatorname{poly}(n),
$$

$$
Z_{t+1}=F_N(Z_t,x)
$$

可在 polynomial time 內計算，且：

$$
\operatorname{Dec}(Z_m)=1
\iff
\exists\gamma\in\Gamma_N(x):
\operatorname{Accept}(\gamma).
$$

---

## 1.4 第四層：GLC

### 名稱

$$
\boxed{
\mathrm{GLC}
=
\text{Global Lossless Completion}
}
$$

### 定位

GLC 不是目前應直接與前三層並列為「第四個等價命題」。

更合理的定位：

$$
\boxed{
\text{前三層負責 polynomial realization，GLC 負責封頂驗收。}
}
$$

框架表示：

$$
\left[
\mathrm{GCC}
\equiv
\mathrm{USRT}
\equiv
\mathrm{USEG}
\right]
\overset{\mathrm{GLC}}{\Longrightarrow}
\text{Closed Exact Computation}.
$$

### GLC 的最終帳本觀點

本專案採用：

$$
\boxed{
\text{過程自由，最終帳本不自由。}
}
$$

演算法中途可以：

- 換路；
- rollback；
- checkpoint；
- representation switching；
- 重算；
- branch pruning；
- 改用其他合法算法；
- 暫時中斷；
- 恢復。

但最終必須符合：

$$
\boxed{
\mathcal L_A(x)
\in
\mathcal A_{\mathrm{final}}.
}
$$

最終帳本最低欄位：

$$
\mathcal L_A(x)
=
(
\mathrm{Correct},
\mathrm{Complete},
\mathrm{Resource},
\mathrm{Rate},
\mathrm{Sequence},
\mathrm{Loss}
).
$$

最低驗收：

$$
\mathrm{Correct}=1,
$$

$$
\mathrm{Complete}=1,
$$

$$
\mathrm{Resource}\in\mathbf{Poly},
$$

$$
\mathrm{Loss}=0.
$$

### GLC 必須分兩版

#### $\mathrm{GLC}_{std}$

標準可靠 deterministic model。

本質接近：

$$
\text{total correctness}
+
\text{polynomial runtime}.
$$

它很可能只是標準 $P$ 語義的顯式化。

#### $\mathrm{GLC}_{robust}$

允許：

- rollback；
- rerouting；
- representation switching；
- restart；
- 有限可恢復故障；

仍要求所有 admissible runs 最終正確完成。

這是比標準 $P=NP$ 更強的 robustness extension。

不得將：

$$
\mathrm{GLC}_{robust}
$$

與標準：

$$
P=NP
$$

直接宣稱等價。

---

# 2. 當前最重要的研究命題

目前可將整個研究計畫寫成：

$$
\boxed{
\text{Characterize the exact relationships among }
\mathrm{GCC},
\mathrm{USRT},
\mathrm{USEG},
\mathrm{GLC},
P,
NP.
}
$$

不要一次試圖證明大等價式。

必須拆成單向箭頭。

建議建立正式命題表：

| 編號 | 命題 | 狀態 |
|---|---|---|
| C1 | $P=NP\Rightarrow \mathrm{GCC}$ | 待嚴格定義後證明 |
| C2 | $\mathrm{GCC}\Rightarrow P=NP$ | 待證 |
| C3 | $P=NP\Rightarrow\mathrm{USRT}$ | 高優先 |
| C4 | $\mathrm{USRT}\Rightarrow P=NP$ | 高優先 |
| C5 | $\mathrm{USRT}\Rightarrow\mathrm{USEG}$ | 高優先 |
| C6 | $\mathrm{USEG}\Rightarrow\mathrm{USRT}$ | 可能需要額外條件 |
| C7 | $\mathrm{USEG}\Rightarrow P=NP$ | 高優先 |
| C8 | $P=NP\Rightarrow\mathrm{USEG}$ | 待形式化 |
| C9 | $\mathrm{GLC}_{std}$ 與標準 total correctness 的關係 | 高優先 |
| C10 | $\mathrm{GLC}_{robust}$ 是否嚴格強於標準 $P=NP$ | 獨立研究線 |

每一條箭頭必須標示：

- Definition-level；
- Standard theorem；
- New theorem；
- Conditional theorem；
- Conjecture；
- False / counterexample。

---

# 3. 後續建議採用八條平行研究線

---

## Track A：公理化與定義

### 目的

把所有名詞從口語概念改造成可檢查數學物件。

### 任務

1. 定義 admissible computation models；
2. 定義 state space；
3. 定義 terminal state；
4. 定義 semantic preservation；
5. 定義 completion rate；
6. 定義 polynomial-rate cone；
7. 定義 effective sequence；
8. 定義 decision-sufficient quotient；
9. 定義 final ledger；
10. 定義 admissible execution history。

### 完成標準

任何符號不得依賴：

> 「大家知道我的意思。」

所有量詞必須明確。

---

## Track B：等價箭頭與數學推導

### 目的

逐條研究：

$$
\mathrm{GCC},
\mathrm{USRT},
\mathrm{USEG},
P,
NP
$$

之間的 implications。

### 方法

每次只做一條箭頭。

例如：

$$
\mathrm{USRT}\Rightarrow P=NP.
$$

必須寫：

1. 假設；
2. domain；
3. codomain；
4. uniformity；
5. polynomial bound；
6. correctness；
7. conclusion；
8. 是否使用 SAT NP-completeness；
9. 是否使用 Cook–Levin；
10. 是否有隱藏 machine dependence。

---

## Track C：非循環性與合法轉換

### 名稱建議

$$
\boxed{
\text{Admissible Transformation Theory}
}
$$

### 目的

阻止所有「先解答案，再定義壓縮」的循環。

禁止：

- SAT oracle；
- hidden advice；
- answer-dependent equivalence relation；
- 無限 precision；
- 免費預計算；
- nonuniform exponential lookup table；
- 把 exponential construction cost 放在 preprocessing 後不記帳；
- 直接將 final answer 當 abstract state。

### 產物

一份：

`Admissible_Transformation_Axioms.md`

這可能成為整套理論最重要的基礎文件之一。

---

## Track D：形式化證明

### 建議工具

優先：

- Lean 4；
- Coq；
- Isabelle/HOL。

### 不要一開始形式化大命題

先建立 theorem ladder。

建議順序：

1. polynomial bound algebra；
2. machine simulation relation；
3. total deterministic computation；
4. completion-time definition；
5. completion-rate equivalence lemma；
6. polynomial-rate cone；
7. state transformation correctness；
8. finite computation sequence；
9. decision-sufficient sequence；
10. USRT $\Rightarrow$ deterministic polynomial solver；
11. USEG $\Rightarrow$ deterministic polynomial solver；
12. 最後才碰三相 equivalence。

### 每一個 theorem

必須有：

- statement；
- dependencies；
- proof status；
- countermodel status；
- formal file path；
- version。

---

## Track E：演算法實作與 Observatory

### 目的

不是實驗證明 $P/NP$。

而是測：

> 四層框架是否能真實描述不同算法。

### 第一批 benchmark

建議：

1. 2-SAT；
2. Horn-SAT；
3. XOR-SAT；
4. bounded-treewidth SAT；
5. general 3-SAT；
6. Tseitin formulas；
7. Pigeonhole Principle；
8. planted SAT；
9. random $k$-SAT。

### 每次執行記錄

$$
\mathcal O
=
(
T,
M,
N_{\mathrm{states}},
N_{\mathrm{branches}},
\kappa_{\mathrm{raw}},
\kappa_{\mathrm{eff}},
N_{\mathrm{switch}},
N_{\mathrm{rollback}},
S_{\mathrm{peak}},
R_{\mathrm{completion}},
\mathrm{final\ ledger}
).
$$

### 建議產物

建立：

$$
\boxed{
\text{Dynamic Complexity Observatory}
}
$$

工程上可先 Python MVP。

---

## Track F：反例與破壞性測試

### 目的

專門攻擊自己的框架。

每一個新定義都要嘗試構造：

- trivialization；
- oracle smuggling；
- preprocessing smuggling；
- nonuniform smuggling；
- path-cardinality counterexample；
- precision blow-up；
- representation blow-up；
- model dependence；
- sequence quotient construction blow-up；
- false GLC；
- robust GLC impossibility under permanent fault。

### 規則

如果反例推翻定義：

不要修飾。

直接：

1. 保存反例；
2. 修改定義；
3. 更新版本；
4. 記錄 breaking change。

---

## Track G：模型不變性

### 目的

確認哪些量屬於問題本身，哪些只是機器表示。

需要分類：

### 可能高度 invariant

$$
\text{Polynomial-time class membership}.
$$

### 可能不 invariant

$$
\text{local state-change velocity}.
$$

### 可能 quotient-invariant

$$
\text{completion-rate polynomial class}.
$$

### 研究問題

若：

$$
M_1\equiv_{\mathrm{poly}}M_2,
$$

則：

$$
\mathrm{GCC}_{M_1}(L)
\stackrel{?}{=}
\mathrm{GCC}_{M_2}(L).
$$

而：

$$
R_{M_1}(n)
$$

與：

$$
R_{M_2}(n)
$$

應以什麼 equivalence relation 比較？

---

## Track H：Complexity Barrier Mapping

任何聲稱接近一般 P/NP separation/equality 的結果，都必須檢查：

1. relativization；
2. natural proofs；
3. algebrization；
4. oracle dependence；
5. restricted-model lower bounds；
6. proof-system-specific lower bounds；
7. nonuniformity；
8. hidden advice；
9. hidden precision；
10. hidden compilation。

每篇正式研究稿末尾建議固定加入：

## Barrier Status

而不是：

## Future Work

---

# 4. 建議新增一條獨立主線：Complexity Ledger Calculus

這條線不需要等待 $P/NP$ 成果。

---

## 4.1 核心物件

定義計算帳本：

$$
\mathcal L
=
(
C_{\mathrm{correct}},
C_{\mathrm{time}},
C_{\mathrm{space}},
C_{\mathrm{construct}},
C_{\mathrm{repr}},
C_{\mathrm{sequence}},
C_{\mathrm{precision}},
C_{\mathrm{recover}},
C_{\mathrm{loss}}
).
$$

---

## 4.2 表示轉換

若：

$$
R_i\rightarrow R_j,
$$

則對應：

$$
\mathcal T_{ij}:
\mathcal L_i\mapsto\mathcal L_j.
$$

---

## 4.3 研究問題

是否存在 composition law：

$$
\mathcal T_{ik}
=
\mathcal T_{jk}\circ\mathcal T_{ij}?
$$

哪些成本：

- 可加；
- 可乘；
- 可攤銷；
- 可交換；
- 會隱藏；
- 會爆炸；
- 可被 quotient；
- 無法被無損壓縮。

---

## 4.4 獨立價值

即使最終沒有解決 P/NP，這條線也可能形成：

- algorithm-analysis formalism；
- agent computation ledger；
- compiler cost calculus；
- adaptive algorithm analysis；
- representation-transition theory。

因此推薦獨立立項。

---

# 5. 建議研究階段

---

## Phase I：Definition & Consistency

### 目標

不是證明 P/NP。

而是完成：

$$
\boxed{
\text{框架自洽}
}
$$

### 必須交付

1. Symbol table；
2. Definitions；
3. Quantifier table；
4. Admissibility axioms；
5. Counterexample suite；
6. GCC model invariance；
7. GLC std/robust split；
8. Three-phase implication map。

### Gate

只有當 Phase I 完成，才能進 Phase II。

---

## Phase II：Characterization Theorems

### 目標

證：

$$
A\Rightarrow B
$$

或找：

$$
A\not\Rightarrow B
$$

的 counterexample。

### 不要求

不要求：

$$
P=NP
$$

或：

$$
P\neq NP.
$$

### 成功標準

哪怕只得到：

$$
\mathrm{USRT}
\Rightarrow
\mathrm{USEG}
$$

需要條件 $X,Y,Z$，

也是真正理論成果。

---

## Phase III：Formalization & Experimental Validation

與 Phase II 可部分平行。

### Formal

Lean/Coq/Isabelle。

### Experimental

Dynamic Complexity Observatory。

---

## Phase IV：P/NP Attack

只有當某條 theorem 已真正跨過：

$$
\text{characterization}
\rightarrow
\text{complexity consequence}
$$

才進入這一階段。

此時才允許提出：

$$
P=NP
$$

或：

$$
P\neq NP
$$

候選證明。

---

# 6. AI 交接標準作業流程

每一個接手 AI 應按照以下順序工作。

---

## Step 1：閱讀

優先閱讀：

1. 本交接文件；
2. `P_NP_動態四層閉合框架_啟發式研究提案_v1.0.md`；
3. 當前最新 Definitions；
4. 當前最新 theorem index；
5. 當前 counterexample index。

---

## Step 2：確認任務類型

先標記當前任務：

- Definition；
- Proof；
- Formalization；
- Counterexample；
- Algorithm；
- Benchmark；
- Literature；
- Barrier check；
- Engineering。

不要把不同任務混成一篇。

---

## Step 3：建立依賴

每個新結果需寫：

### Depends on

- 定義；
- lemma；
- theorem；
- 外部定理；
- 假設。

---

## Step 4：標註結果等級

只能使用：

- `Definition`
- `Observation`
- `Lemma`
- `Proposition`
- `Theorem`
- `Conditional Theorem`
- `Conjecture`
- `Counterexample`
- `Experimental Result`
- `Open Problem`

不得把 Conjecture 寫成 Theorem。

---

## Step 5：做反例測試

任何新命題至少問：

1. trivial P language 是否破壞？
2. intentionally branching P machine 是否破壞？
3. oracle 是否讓定義退化？
4. nonuniform advice 是否偷渡？
5. exponential preprocessing 是否偷渡？
6. arbitrary machine encoding 是否影響？
7. robust GLC 是否因永久 fault 變不可能？

---

## Step 6：更新研究圖

推薦維護：

`THEOREM_GRAPH.md`

格式：

```text
GCC
 ├──?→ USRT
 ├──?→ P=NP
USRT
 ├──?→ USEG
 └──?→ P=NP
USEG
 └──?→ P=NP
GLC_std
 └── relation → Total Correctness
GLC_robust
 └── stronger extension
```

箭頭狀態：

- `✓`
- `✗`
- `?`
- `conditional`

---

## Step 7：更新失敗紀錄

建立：

`FAILED_ROUTES.md`

每個失敗路線保留：

- 原命題；
- 為何失敗；
- counterexample；
- 是否可修正；
- 禁止再次重複的錯誤。

---

# 7. 建議專案目錄

```text
P_NP_Dynamic_Closure/
│
├── 00_overview/
│   ├── framework_v1.md
│   ├── research_handoff.md
│   └── terminology.md
│
├── 01_definitions/
│   ├── GCC.md
│   ├── USRT.md
│   ├── USEG.md
│   ├── GLC_std.md
│   └── GLC_robust.md
│
├── 02_axioms/
│   └── admissible_transformations.md
│
├── 03_theorems/
│   ├── implication_map.md
│   ├── lemmas/
│   └── conditional_results/
│
├── 04_counterexamples/
│   ├── path_cardinality.md
│   ├── hidden_preprocessing.md
│   ├── oracle_smuggling.md
│   └── robust_glc_faults.md
│
├── 05_formal/
│   ├── lean/
│   ├── coq/
│   └── isabelle/
│
├── 06_algorithms/
│   ├── 2sat/
│   ├── hornsat/
│   ├── xorsat/
│   └── 3sat/
│
├── 07_observatory/
│   ├── metrics.md
│   ├── benchmark_schema.md
│   └── experiments/
│
├── 08_ledger_calculus/
│   ├── ledger_definition.md
│   ├── transformations.md
│   └── composition_rules.md
│
├── 09_barriers/
│   ├── relativization.md
│   ├── natural_proofs.md
│   └── algebrization.md
│
├── 10_failed_routes/
│   └── FAILED_ROUTES.md
│
└── THEOREM_GRAPH.md
```

---

# 8. 下一批建議任務

按優先級排序。

---

## Priority 0

### Task 0.1

建立：

`P_NP_Dynamic_Closure_Definitions_v0.1.md`

只做嚴格定義。

不做大證明。

### Task 0.2

建立：

`Admissible_Transformation_Axioms_v0.1.md`

專門定義什麼叫合法轉換。

---

## Priority 1

### Task 1.1

形式化：

$$
\mathrm{USRT}
\Rightarrow
P=NP
$$

候選 proposition。

### Task 1.2

形式化：

$$
\mathrm{USEG}
\Rightarrow
P=NP
$$

候選 proposition。

### Task 1.3

檢查：

$$
P=NP
\Rightarrow
\mathrm{USRT}
$$

究竟需要何種 uniform transformation schema。

---

## Priority 2

### Task 2.1

建立：

`Sequence_Cardinality_Counterexamples.md`

證明 raw path cardinality 不足。

### Task 2.2

定義：

$$
\kappa_{\mathrm{eff}}.
$$

並嘗試找：

- trivial example；
- useful example；
- circular example；
- impossible example。

---

## Priority 3

### Task 3.1

建立 Dynamic Complexity Observatory MVP。

先做：

- 2-SAT；
- XOR-SAT；
- 3-SAT。

### Task 3.2

實作 final ledger。

---

## Priority 4

### Task 4.1

開始 Lean theorem ladder。

第一批只處理：

- polynomial functions；
- completion time；
- completion rate；
- elementary implications。

---

# 9. 研究紅線

任何後續 AI 都必須遵守。

### 紅線 1

不得因：

$$
\text{候選數量指數級}
$$

直接推出：

$$
P\neq NP.
$$

---

### 紅線 2

不得因某種：

- OBDD；
- resolution；
- monotone circuit；
- LP；
- DNNF；

有 exponential lower bound，直接推出 general lower bound。

---

### 紅線 3

不得把：

$$
\text{找算法很難}
$$

當成：

$$
\text{算法不存在}.
$$

---

### 紅線 4

不得把：

$$
\mathrm{GLC}_{robust}
$$

冒充：

$$
P=NP
$$

的同義式。

---

### 紅線 5

不得使用 answer-dependent abstraction／quotient 而不記錄其構造成本。

---

### 紅線 6

不得把一次實驗成功當成 asymptotic theorem。

---

### 紅線 7

不得把 AI 自己生成的 proof sketch 稱為形式化證明。

---

# 10. 每次研究輸出的建議模板

```markdown
# Title

## Status
Definition / Lemma / Conjecture / Experiment / Counterexample

## Scope
本結果在哪個 model 成立？

## Definitions Used

## Statement

## Assumptions

## Derivation / Proof

## Resource Accounting

## Uniformity Check

## Non-Circularity Check

## Counterexample Search

## Barrier Status

## Formalization Status

## Experimental Status

## Dependencies

## Open Questions

## Next Handoff Task
```

---

# 11. 長期成功標準

本專案不應把：

$$
P=NP
$$

或：

$$
P\neq NP
$$

作為唯一成功標準。

分層成功標準如下。

### Level 1

四層定義完整、自洽。

### Level 2

得到非平凡 implication / separation。

### Level 3

形成可形式化 theorem family。

### Level 4

形成可實作 Complexity Ledger / Observatory。

### Level 5

形成新的 machine-independent dynamic complexity characterization。

### Level 6

若某個 theorem 真正足以推出：

$$
P=NP
$$

或：

$$
P\neq NP,
$$

才進入正式 P/NP proof verification。

---

# 12. 最終交接摘要

本專案下一階段的正確路線不是：

> 「繼續辯論 $P=NP$ 還是 $P\neq NP$。」

而是：

$$
\boxed{
\text{Definition}
\rightarrow
\text{Characterization}
\rightarrow
\text{Formalization}
\rightarrow
\text{Experiment}
\rightarrow
\text{Counterexample}
\rightarrow
\text{Barrier Review}
}
$$

再視結果決定是否進入：

$$
\boxed{
\text{P/NP Attack}.
}
$$

核心研究骨架：

$$
\boxed{
\mathrm{GCC}
\quad
\mathrm{USRT}
\quad
\mathrm{USEG}
\quad
\mathrm{GLC}
}
$$

核心研究態度：

$$
\boxed{
\text{過程可以自由，定義、量詞、帳本與證明不能自由。}
}
$$

核心最終原則：

$$
\boxed{
\text{先建立一套值得成立的理論，再問它能不能解 P/NP。}
}
$$
