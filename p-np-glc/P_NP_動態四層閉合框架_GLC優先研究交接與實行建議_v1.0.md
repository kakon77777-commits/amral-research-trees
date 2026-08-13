# P/NP 動態四層閉合框架
## GLC 優先研究交接與實行建議 v1.0

- **文件性質**：長期研究交接／執行順序修訂文件
- **核心修訂**：動態四層研究順序由「前三層 → GLC 封頂」調整為「GLC 先行 → 其餘三層建立於 GLC 之上」
- **目前定位**：啟發式 Characterization Program；不宣稱已證明 $P=NP$ 或 $P\neq NP$
- **核心四層**：
  - $\mathrm{GLC}$：Global Lossless Completion，全域無損完成
  - $\mathrm{GCC}$：Global Computational Complexity，全域計算複雜度
  - $\mathrm{USRT}$：Universal State-Rate Transformation，全稱狀態速率變換
  - $\mathrm{USEG}$：Universal Effective Sequence Generation，全稱有效序列生成
- **交接目的**：確保任何後續 AI、研究者或形式化工具，在推進 GCC／USRT／USEG 前，先完成 GLC 的語義、公理、驗收與非循環基底。

---

# 0. 本次最重要的架構修訂

舊研究順序偏向：

$$
\mathrm{GCC}
\rightarrow
\mathrm{USRT}
\rightarrow
\mathrm{USEG}
\rightarrow
\mathrm{GLC}.
$$

新研究順序改為：

$$
\boxed{
\mathrm{GLC}
\rightarrow
\{\mathrm{GCC},\mathrm{USRT},\mathrm{USEG}\}.
}
$$

這不是單純的工作排序調整，而是理論角色的重新定位。

新架構中：

$$
\boxed{
\mathrm{GLC}
=
\text{Specification / Semantic Foundation Layer}.
}
$$

也就是：

> GLC 先定義「什麼叫真正完成」。

之後：

- GCC 研究「達成這種完成需要多少全域資源」；
- USRT 研究「狀態如何在保持這種完成語義下合法變換」；
- USEG 研究「序列如何生成、壓縮、商化而仍保持這種完成」。

因此：

$$
\boxed{
\text{GLC 定義完成；其他三層研究如何完成。}
}
$$

---

# 1. 為何 GLC 必須先完成

如果 GLC 尚未嚴格定義：

## 1.1 GCC 會缺失目標函數

GCC 會問：

> 「這個問題的最低全域計算複雜度是多少？」

但若沒有先定義：

$$
\text{什麼叫合法完成},
$$

則「最低複雜度」沒有統一的驗收終點。

## 1.2 USRT 會缺失完成態

USRT 常使用：

$$
T_A(n)
=
\text{到達完成態所需時間}.
$$

但如果沒有先定義：

$$
H_L(x)
=
\text{合法完成態集合},
$$

那麼 completion rate 本身就可能依賴不同的隱含語義。

## 1.3 USEG 會缺失「決策充分」標準

USEG 要研究：

$$
\Gamma_N(x)
\rightarrow
Z_0\rightarrow Z_1\rightarrow\cdots\rightarrow Z_m.
$$

但如果沒有 GLC，就無法嚴格判斷：

> 哪種 sequence summary 算「足夠」？

因此新的原則是：

$$
\boxed{
\text{Decision sufficiency must be defined relative to GLC.}
}
$$

---

# 2. GLC 的第一版必須「資源中立」

這是本文件的核心執行原則之一。

第一版 GLC 不得一開始就要求：

$$
T(n)\in\operatorname{poly}(n),
$$

否則 GCC 已被偷偷塞進 GLC。

因此首先建立：

$$
\boxed{
\mathrm{GLC}_0
=
\text{Resource-Neutral Global Lossless Completion}.
}
$$

$\mathrm{GLC}_0$ 只回答：

> 一個計算是否對所有合法輸入最終正確、完整、無損地完成？

而不問它用了多久。

初始核心：

$$
\boxed{
\mathrm{GLC}_0
=
\mathrm{Correctness}
+
\mathrm{Completion}
+
\mathrm{Semantic\ Losslessness}.
}
$$

之後才另外疊加：

- resource constraints；
- rate constraints；
- sequence constraints。

---

# 3. GLC 建議拆成五個核心公理

## GLC-1：Semantic Correctness

對問題／語言 $L$ 與輸入 $x$：

$$
\operatorname{Out}(A,x)
=
\chi_L(x).
$$

對 exact deterministic computation：

$$
\boxed{
\text{Wrong Terminal Result}=0.
}
$$

不是「錯誤率趨近 0」，也不是「大部分輸入正確」，而是：

$$
\boxed{
\forall x,\quad
\operatorname{Out}(A,x)=\chi_L(x).
}
$$

## GLC-2：Eventual Completion

不能只有 partial correctness。

必須：

$$
\forall x,\exists t<\infty:
S_A(x,t)\in H_L(x).
$$

其中 $H_L(x)$ 是合法完成態集合。

核心要求：

$$
\boxed{
\text{最後一定交件。}
}
$$

## GLC-3：Semantic Losslessness

演算法中途可以：壓縮、表示轉換、換路、rollback、branch pruning、restart、decomposition、quotient、abstraction、re-encoding。

但不能失去最終決策所需要的語義。

因此不要求：

$$
S_t=S_{t+1}.
$$

真正要求的是某種：

$$
\boxed{
\operatorname{Sem}_L(S_t)
\sim
\operatorname{Sem}_L(S_{t+1}).
}
$$

或一個較弱、但足以保證最終答案的 preservation relation。

## GLC-4：Final Ledger Validity

採用：

$$
\boxed{
\text{過程自由，最終帳本不自由。}
}
$$

定義最終帳本：

$$
\mathcal L_A(x).
$$

第一版建議最少包含：

$$
\mathcal L_A(x)
=
(Y,C,\Lambda),
$$

其中：

- $Y$：answer correctness；
- $C$：completion；
- $\Lambda$：semantic loss。

$\mathrm{GLC}_0$ 驗收：

$$
Y=1,
\qquad
C=1,
\qquad
\Lambda=0.
$$

注意：第一版不要把 GCC／USRT／USEG 的資源欄位強行塞入 GLC 基底定義。

## GLC-5：Admissible Execution Closure

如果研究的不只是標準單一路徑 deterministic execution，而允許 restart、rollback、rerouting、representation switching、finite recoverable faults，則必須先定義：

$$
\operatorname{Runs}_{adm}(A,x).
$$

強版要求：

$$
\forall \pi\in\operatorname{Runs}_{adm}(A,x),
\exists t<\infty:
\pi_t\in H_L(x).
$$

並且：

$$
\operatorname{Out}(\pi_t)=\chi_L(x).
$$

永久斷電、永久不排程、不可恢復物理毀滅等情形不能默認放入 admissible disturbance，否則完成要求會變成邏輯不可能。

---

# 4. GLC 必須拆成標準版與強韌版

## 4.1 $\mathrm{GLC}_{std}$

適用：標準 deterministic model、無外部永久故障、正常執行。

近似：

$$
\boxed{
\mathrm{GLC}_{std}
=
\text{Total Correctness}.
}
$$

後續要檢查：

> $\mathrm{GLC}_{std}$ 是否只是標準 $P$／DECIDER 語義的重新顯式化？

若是，也沒有問題。這表示 GLC 成為其餘三層共享的語義介面。

## 4.2 $\mathrm{GLC}_{robust}$

允許 rerouting、recovery、restart、representation switching、finite transient faults，仍要求：

$$
\boxed{
\forall\text{ admissible runs},\quad
\text{eventual exact completion}.
}
$$

此版本可能嚴格強於標準 $P=NP$。

因此：

$$
\boxed{
\mathrm{GLC}_{robust}
\not\equiv
P=NP
}
$$

除非未來另有證明。

---

# 5. GLC 第一階段必須完成的數學物件

在研究 GCC／USRT／USEG 前，至少要完成：

1. Input Domain：$X_L$。
2. State Space：$\mathcal S_A$。
3. Transition Relation：$\rightarrow_A\subseteq\mathcal S_A\times\mathcal S_A$。
4. Terminal-State Set：$H_L(x)\subseteq\mathcal S_A$。
5. Output Map：$\operatorname{Out}:H_L(x)\rightarrow\{0,1\}$，或更一般 codomain。
6. Semantic Projection：$\operatorname{Sem}_L:\mathcal S_A\rightarrow\mathcal D_L$。
7. Loss Relation：$\Lambda_L(S_i,S_j)$。
8. Admissible Run：$\pi=S_0,S_1,\ldots$ 以及 $\operatorname{Runs}_{adm}(A,x)$。
9. Completion Predicate：$\operatorname{Complete}_{GLC}(A,x)$。
10. Final Ledger：$\mathcal L_A(x)$。

---

# 6. GLC 的非循環性要求

GLC 最容易出現的錯誤是：

> 用最終正確答案定義「合法狀態」，再宣稱所有合法狀態都導向正確答案。

因此必須區分：

- Verification Definition：用於描述「結果是否正確」；
- Construction Rule：演算法實際可以使用的資訊。

後續必須建立：

$$
\boxed{
\text{GLC Non-Circularity Principle}.
}
$$

核心要求：

> GLC 可以在 meta-level 使用 $\chi_L(x)$ 描述 correctness，但演算法 construction 不得免費存取 $\chi_L(x)$。

也就是：

$$
\boxed{
\text{Specification may mention truth; implementation may not receive truth as oracle.}
}
$$

---

# 7. 完成 GLC 後，再重新定義 GCC

新的 GCC 不應再先驗地問「問題 $L$ 的 complexity 是什麼」，而應改成：

> 所有滿足 GLC 的合法算法中，最低可達全域資源複雜度是什麼？

定義候選：

$$
\mathcal A_{\mathrm{GLC}}(L)
=
\{A:A\text{ satisfies GLC for }L\}.
$$

再定義：

$$
\boxed{
C_{\mathrm{GLC}}(L,n)
=
\inf_{A\in\mathcal A_{\mathrm{GLC}}(L)}
C_A(n).
}
$$

GCC 研究：

$$
[C_{\mathrm{GLC}}(L,n)]_{\equiv_{\mathrm{poly}}}.
$$

---

# 8. 完成 GLC 後，再重新定義 USRT

USRT 改為研究：

$$
\boxed{
\text{GLC-preserving state-rate transformations}.
}
$$

對 transformation：

$$
\mathcal U:N\mapsto D,
$$

至少需要：

### GLC preservation

$$
\mathrm{GLC}(N,x)
\Longleftrightarrow
\mathrm{GLC}(D,x)
$$

或適合 nondeterministic-to-deterministic setting 的對應版本。

### Rate condition

$$
T_D(n)\le q_N(n),
$$

其中：

$$
q_N\in\operatorname{poly}.
$$

因此 USRT 不再自行定義「完成」。它只負責：在保持 GLC 語義下，能否完成合法的速率轉換？

---

# 9. 完成 GLC 後，再重新定義 USEG

USEG 改為：

$$
\boxed{
\text{GLC-preserving effective sequence generation}.
}
$$

給定：

$$
\Gamma_N(x)
$$

需要產生：

$$
Z_0\rightarrow Z_1\rightarrow\cdots\rightarrow Z_m.
$$

最終要求：

$$
\mathrm{GLC}(Z_m,x).
$$

而每個 quotient／compression／summary 必須保持 GLC 指定的 semantic invariants。

因此：

$$
\boxed{
\text{Decision sufficiency}
=
\text{GLC-relative sufficiency}.
}
$$

---

# 10. 新的整體研究順序

## Phase 0：GLC Foundations

**最高優先級。**

完成：

1. $\mathrm{GLC}_0$；
2. semantic correctness；
3. terminal states；
4. completion；
5. semantic losslessness；
6. final ledger；
7. admissible runs；
8. non-circularity；
9. $\mathrm{GLC}_{std}$；
10. $\mathrm{GLC}_{robust}$。

此階段禁止主攻 P/NP 等價證明。

## Phase 1：GCC over GLC

研究：

$$
\boxed{
\text{達成 GLC 的最低全域資源複雜度。}
}
$$

## Phase 2：USRT over GLC

研究：

$$
\boxed{
\text{保持 GLC 的全稱狀態速率轉換。}
}
$$

## Phase 3：USEG over GLC

研究：

$$
\boxed{
\text{保持 GLC 的有效序列生成與商化。}
}
$$

## Phase 4：Characterization Closure

此時才重新研究：

$$
\mathrm{GCC}
\stackrel{?}{\Longleftrightarrow}
\mathrm{USRT}
\stackrel{?}{\Longleftrightarrow}
\mathrm{USEG}.
$$

以及 $P=NP$ 與這些 characterization 的精確關係。

## Phase 5：Formal P/NP Attack

只有當某條新定理真正超越定義重寫與受限模型結果時，才進入。

---

# 11. GLC 優先版專案結構建議

```text
P_NP_Dynamic_Closure/
│
├── 00_overview/
│   ├── framework_v1.md
│   ├── research_handoff.md
│   └── glc_first_handoff.md
│
├── 01_GLC/
│   ├── GLC0_resource_neutral.md
│   ├── semantics.md
│   ├── terminal_states.md
│   ├── completion.md
│   ├── losslessness.md
│   ├── final_ledger.md
│   ├── admissible_runs.md
│   ├── GLC_std.md
│   ├── GLC_robust.md
│   └── non_circularity.md
│
├── 02_GCC_over_GLC/
├── 03_USRT_over_GLC/
├── 04_USEG_over_GLC/
├── 05_characterization/
├── 06_formal/
├── 07_counterexamples/
├── 08_algorithms/
├── 09_observatory/
├── 10_barriers/
└── FAILED_ROUTES.md
```

---

# 12. 下一批任務：只做 GLC

以下任務未完成前，不建議進入 GCC／USRT／USEG 正式主線。

## Priority G0

### G0.1
建立：`GLC0_Resource_Neutral_Definition_v0.1.md`

### G0.2
建立：`GLC_Semantic_State_Model_v0.1.md`

### G0.3
建立：`GLC_Final_Ledger_v0.1.md`

先只包含：

$$
(\mathrm{Correct},\mathrm{Complete},\mathrm{Loss}).
$$

## Priority G1

### G1.1
建立：`GLC_Admissible_Runs_v0.1.md`

### G1.2
建立：`GLC_NonCircularity_Principle_v0.1.md`

### G1.3
建立：`GLC_std_vs_GLC_robust_v0.1.md`

## Priority G2

建立正例與反例測試集。

正例至少包含：addition、sorting、graph reachability、2-SAT。

反例至少包含：

- 永不停止但從不輸出錯誤；
- 停止但輸出錯誤；
- 中間 loss 但最後碰巧答對；
- rollback 後恢復；
- 永久 crash；
- answer-oracle cheating。

## Priority G3

在簡化 deterministic machine model 下，以 Lean／Coq／Isabelle 形式化：

$$
\text{Correctness}
+
\text{Termination}
\Rightarrow
\mathrm{GLC}_{std}.
$$

---

# 13. GLC 研究紅線

1. 不得把 polynomial runtime 放進 $\mathrm{GLC}_0$ 的基本定義。
2. 不得用最終答案當作 implementation 可免費讀取的 state information。
3. 不得把「中間資訊 bit-level 無損」和「decision semantics 無損」混為一談。
4. 不得要求永久硬體毀滅後仍完成。
5. 不得把 $\mathrm{GLC}_{robust}$ 與標準 $P=NP$ 宣稱天然等價。
6. 不得在 GLC 尚未穩定前用 GCC／USRT／USEG 的結果反向修改 GLC 以配合想要的結論。

---

# 14. 後續 AI 的執行規則

任何接手本專案的 AI：

1. 先讀本文件；
2. 確認 GLC 當前版本；
3. 不得跳過 GLC 直接主攻三相等價；
4. 每新增 GLC 定義必須附 scope、quantifiers、counterexample、non-circularity check；
5. 每修改 GLC 必須記錄 breaking changes；
6. GLC 穩定前不得宣稱：

$$
\mathrm{GCC}\equiv\mathrm{USRT}\equiv\mathrm{USEG}.
$$

---

# 15. GLC 完成門檻

只有以下項目全部具備，才視為 GLC Foundation v1.0 完成：

- [ ] $\mathrm{GLC}_0$ 正式定義
- [ ] State space 定義
- [ ] Semantic projection 定義
- [ ] Terminal-state 定義
- [ ] Exact correctness 定義
- [ ] Eventual completion 定義
- [ ] Losslessness 定義
- [ ] Final ledger 定義
- [ ] Admissible-run 定義
- [ ] Non-circularity principle
- [ ] $\mathrm{GLC}_{std}$
- [ ] $\mathrm{GLC}_{robust}$
- [ ] 至少 5 個正例
- [ ] 至少 5 個反例
- [ ] resource-neutrality audit
- [ ] 初步 formalization
- [ ] theorem / dependency graph

只有完成後，才能正式開啟：

$$
\boxed{
\text{GCC over GLC}.
}
$$

---

# 16. 最終交接摘要

新的研究架構不再把 GLC 當成「最後才檢查的第四層」，而是把它升格為：

$$
\boxed{
\text{整個四層框架的語義地基。}
}
$$

新的研究順序：

$$
\boxed{
\mathrm{GLC}
\rightarrow
\mathrm{GCC}
\rightarrow
\mathrm{USRT}
\rightarrow
\mathrm{USEG}
\rightarrow
\text{Characterization Closure}.
}
$$

其中箭頭表示研究依賴，不代表數學 implication。

核心哲學：

$$
\boxed{
\text{先定義什麼叫完成，再討論怎麼完成。}
}
$$

進一步：

$$
\boxed{
\text{GLC 定義驗收規格；GCC 計算成本；USRT 管理速率；USEG 管理序列。}
}
$$

而整個專案的最終原則仍是：

$$
\boxed{
\text{過程自由，最終帳本不自由。}
}
$$
