# P/NP 動態四層閉合框架：從全域複雜度、狀態速率、有效序列到無損完成的啟發式重描述

**Dynamic Four-Layer Closure Framework for P/NP: A Heuristic Reformulation via Global Complexity, State-Rate Transformation, Effective Sequence Generation, and Lossless Completion**

**作者：Neo.K（許筌崴）**  
**協作整理：Aletheia**  
**機構：EveMissLab（一言諾科技有限公司）**  
**日期：2026-08-02**  
**版本：v1.0**  
**文件性質：概念論文／啟發式研究綱領；非 P vs. NP 證明**

---

## 摘要

P vs. NP 的標準問題，是判斷所有能由非確定性多項式時間演算法接受的語言，是否也能由確定性多項式時間演算法接受。本文不試圖證明 \(P=NP\) 或 \(P\neq NP\)，而提出一個與既有「動態速率」研究線相容的四層閉合框架，將傳統 P/NP 問題重新投影到四個彼此關聯但概念功能不同的觀察面：**全域計算複雜度態（GCC）**、**全稱狀態速率變換態（USRT）**、**全稱有效序列生成態（USEG）**，以及作為封頂驗收條件的 **全域無損完成態（GLC）**。

本文的基本立場是：若限制在彼此具有多項式模擬關係的「合理計算模型」中，則傳統的多項式時間分類可被視為一種跨模型的複雜度等價類；同一分類也可以重寫為狀態完成速率是否能由非確定性多項式動力學轉換為確定性多項式動力學；進一步，非確定性計算中的大量候選序列是否能被壓縮為一條決策充分、可確定性多項式生成的有效序列，也可作為第三個觀察面。本文因此提出啟發式三相等價綱領：

\[
\mathrm{GCC}\;\Longleftrightarrow\;\mathrm{USRT}\;\Longleftrightarrow\;\mathrm{USEG},
\]

並主張在適當形式化後，三者應可與標準 \(P=NP\) 命題建立等價關係。

第四層 GLC 並非單純的第四個平行等價量，而是「最終帳本」式的閉合條件：計算過程可暫停、改寫、切換表示、回滾或換路，只要所有被納入允許集合的執行歷史，最終都交付正確、完整、零語義損失且資源帳符合規格的結果。在標準可靠確定性計算模型中，此弱版 GLC 基本上已包含於多項式時間決策演算法的 total correctness 要求；若進一步要求在合法 rerouting、restart 或有限可恢復故障下仍能收斂，則得到較傳統 \(P=NP\) 更強的 robust GLC 延伸。

本文的目的，是提出一個可供後續形式化證明、反例構造、演算法設計與複雜度不變量研究使用的動態座標系，而非宣告已解決 P vs. NP。

**關鍵詞：** P vs. NP、動態速率、全域計算複雜度、狀態完成速率、非確定性計算、有效序列生成、無損完成、計算模型不變性、啟發式框架

---

## 1. 問題背景與研究定位

P vs. NP 的標準形式可表述為：是否每一個由某個非確定性多項式時間演算法接受的語言，也都可以由某個確定性多項式時間演算法接受。等價地，NP 也可透過多項式時間 verifier 與多項式長度 certificate 來定義 [1]。

本文接受上述標準定義，不修改 P、NP、NP-complete 或 polynomial-time reduction 的傳統含義。本文真正改變的是**觀察座標**。

傳統寫法主要關注：

\[
T_A(n)\in \operatorname{poly}(n)?
\]

本文則提出四個問題：

1. 若排除不合理的計算捷徑，不同合理計算模型是否落在同一多項式複雜度等價類？
2. 非確定性多項式完成過程，能否被全稱地轉換為確定性多項式完成速率？
3. 大量可能的非確定性計算序列，能否被壓縮為一條決策充分的確定性有效序列？
4. 不論中間合法過程如何變化，最終是否都能交付同一正確、完整、無損且資源合格的結果？

因此，本文不是試圖用新術語代替 P/NP，而是希望建立：

\[
\text{標準複雜度分類}
\longleftrightarrow
\text{動態狀態描述}
\longleftrightarrow
\text{序列生成描述}
\longrightarrow
\text{最終閉合驗收}.
\]

---

## 2. 模型邊界：不是「任何可計算機器」，而是合理計算模型族

若只要求兩種機器都具有 Turing-complete 能力，並不能推出它們具有相同的時間複雜度。傳統複雜度理論之所以能把 P 視為具有相當穩健的跨模型意義，是因為常見的「合理」計算模型通常能以多項式 overhead 互相模擬；這正是計算複雜度中的 invariance thesis / Cobham–Edmonds 觀點之一 [2,3]。

因此本文定義一個可接受模型族：

\[
\mathfrak M_{\mathrm{adm}}.
\]

其中每個模型原則上應滿足：

- 有限可描述；
- uniform；
- 不預置問題答案；
- 不使用不可計價的無限精度常數；
- 不含 oracle 式外部答案源；
- 不含未計價的超多項式 advice；
- 與族內其他模型存在多項式 overhead 的有效模擬。

若 \(M_i,M_j\in\mathfrak M_{\mathrm{adm}}\)，以

\[
M_i\equiv_{\mathrm{poly}}M_j
\]

表示兩者可相互以多項式 overhead 模擬。

本文所有「全域」一詞，原則上都限制在 \(\mathfrak M_{\mathrm{adm}}\) 內，而不是對任意物理裝置、任意 oracle 模型或任意超常計算模型量化。

---

## 3. 第一層：全域計算複雜度態 GCC

### 3.1 定義

對決策語言 \(L\)，令

\[
T_M^L(n)
\]

表示模型 \(M\in\mathfrak M_{\mathrm{adm}}\) 上某個正確決策 \(L\) 的確定性演算法之最壞情況時間。

本文將「全域計算複雜度態」記為：

\[
\mathrm{GCC}(L)
=
[T_M^L]_{\equiv_{\mathrm{poly}}},
\]

即忽略合理模型之間的多項式 overhead，只保留其多項式等價類。

定義：

\[
\mathrm{GCC}(L)\in\mathbf{Poly}
\]

若且唯若存在某個 \(M\in\mathfrak M_{\mathrm{adm}}\) 與某個確定性演算法 \(A\)，使

\[
T_{M,A}^L(n)\le n^{O(1)}.
\]

### 3.2 與標準 P 的關係

在合理模型的多項式不變性假設下：

\[
\mathrm{GCC}(L)\in\mathbf{Poly}
\]

可視為

\[
L\in P
\]

的跨模型重述，而不是新的複雜度類。

因此：

\[
\forall L\in NP,\quad
\mathrm{GCC}(L)\in\mathbf{Poly}
\]

應與標準的

\[
P=NP
\]

具有相同的目標內容。

GCC 的作用，是將「是否有多項式時間演算法」重寫成「該問題是否在所有合理計算基底下落入同一多項式資源等價域」。

---

## 4. 第二層：全稱狀態速率變換態 USRT

### 4.1 狀態與完成時間

令演算法 \(A\) 在輸入 \(x\) 上的計算狀態為：

\[
S_A(x,t).
\]

令正確完成態集合為：

\[
H_L(x)
=
\{s:
s\text{ 已停止且輸出 }\chi_L(x)\}.
\]

定義 hitting time：

\[
\tau_A(x)
=
\min\{t:
S_A(x,t)\in H_L(x)\}.
\]

再定義最壞情況完成時間：

\[
T_A(n)
=
\max_{|x|\le n}\tau_A(x).
\]

本文使用一個簡單的完成速率參數化：

\[
R_A(n)
=
\frac{1}{1+T_A(n)}.
\]

因此：

\[
T_A(n)\le n^k
\]

等價於：

\[
R_A(n)
\ge
\frac{1}{1+n^k}.
\]

### 4.2 「速率一致」的正確含義

本文不要求非確定性與確定性計算具有相同的逐步速度，也不要求：

\[
T_D(n)=T_N(n).
\]

若 \(P=NP\)，一個非確定性 \(n^2\) 過程完全可能只被轉換成確定性的 \(n^{20}\) 演算法；兩者依然都屬於 polynomial time。

因此「速率一致」應定義為：

\[
\boxed{\text{同屬 polynomial completion-rate cone}}
\]

而不是數值相等。

### 4.3 USRT

令 \(N\) 為一台 polynomially clocked nondeterministic machine。定義一個全稱狀態速率變換 schema：

\[
\mathcal U_{\mathrm{rate}}:
N\mapsto D_N,
\]

使 \(D_N\) 為確定性機器，並滿足：

**語義保存：**

\[
D_N(x)=1
\iff
N(x)\text{ 存在接受路徑}.
\]

**確定完成：**

\[
\forall x,\quad
D_N(x)\text{ 最終停止}.
\]

**多項式速率保存：**

\[
\exists q_N\in\operatorname{poly}
\quad
\forall n,
\quad
T_{D_N}(n)\le q_N(n).
\]

量詞次序尤其重要：

\[
\exists\mathcal U_{\mathrm{rate}}
\;\forall N\;
\exists q_N\in\operatorname{poly}
\;\forall x.
\]

不能錯寫成所有 \(N\) 共用同一個固定 exponent 的 universal runtime bound；後者比標準 \(P=NP\) 強得多。

---

## 5. 第三層：全稱有效序列生成態 USEG

### 5.1 原始序列基數不是複雜度

對非確定性機器 \(N\) 與輸入 \(x\)，記全部合法計算路徑為：

\[
\Gamma_N(x)
=
\{\gamma_1,\gamma_2,\ldots\}.
\]

若每一步最多有 \(b\) 個分支，路徑長度至多 \(p(n)\)，則可能有：

\[
|\Gamma_N(x)|
\le
b^{p(n)}
\]

條原始路徑。

然而，原始路徑數量本身不能直接推出困難性。

一個本來在 P 的問題，也可以被故意寫成先 nondeterministically 猜大量無用 bit、再忽略它們並呼叫原來 P 演算法的機器。此時 \(|\Gamma_N(x)|\) 可指數巨大，但語言仍在 P。

因此本文明確拒絕以下推論：

\[
|\Gamma_N(x)|\text{ 指數大}
\Rightarrow
L\notin P.
\]

### 5.2 有效序列基數

真正可能具有複雜度意義的是「決策上不可再合併的序列差異」。

令：

\[
\gamma_a\sim_D\gamma_b
\]

表示兩條計算路徑在最終決策所需要的資訊上可被同一摘要精確代表。

定義：

\[
\kappa_{\mathrm{eff}}(N,x)
=
|\Gamma_N(x)/{\sim_D}|.
\]

這裡的重點不是 \(\kappa_{\mathrm{eff}}\) 的數值本身，而是：

1. 等價關係能否有效構造；
2. quotient 是否可用 polynomial-size representation 表示；
3. quotient transition 是否可 polynomial-time 更新；
4. 最終答案是否能由 quotient state 精確讀出。

否則可以循環地「先解掉問題，再宣稱所有路徑其實只有一個決策類」。

### 5.3 USEG

定義全稱有效序列生成態：

\[
\mathrm{USEG}.
\]

對每一台 polynomial-time nondeterministic machine \(N\)，要求存在 deterministic generator \(G_N\)，對每個輸入 \(x\) 生成：

\[
Z_0,Z_1,\ldots,Z_m,
\]

其中每個 \(Z_t\) 是對整批 nondeterministic computation histories 的**決策充分摘要**，且：

\[
m\le\operatorname{poly}(|x|),
\]

\[
|Z_t|\le\operatorname{poly}(|x|),
\]

\[
Z_{t+1}
=
F_N(Z_t,x)
\]

可在 polynomial time 中計算，並且：

\[
\operatorname{Dec}(Z_m)=1
\iff
\exists\gamma\in\Gamma_N(x):
\operatorname{Accept}(\gamma).
\]

USEG 因而不是「逐條生成所有 nondeterministic branches」，而是：

\[
\boxed{
\text{把整個 sequence family 精確壓縮成一條 deterministic effective sequence}.
}
\]

---

## 6. 三相等價：本文的核心啟發式命題

在上述定義與模型邊界下，本文提出以下**待形式化驗證的啟發式等價綱領**：

\[
\boxed{
\mathrm{GCC}
\Longleftrightarrow
\mathrm{USRT}
\Longleftrightarrow
\mathrm{USEG}
}
\]

並預期：

\[
\boxed{
\mathrm{GCC}
\Longleftrightarrow
\mathrm{USRT}
\Longleftrightarrow
\mathrm{USEG}
\Longleftrightarrow
P=NP
}
\]

可以在適當形式系統中被證成真正等價，或至少被拆成若干方向分別證明。

目前本文不聲稱已完成此證明。

其直觀理由如下。

### 6.1 GCC \(\Rightarrow\) USRT

若每個 NP 語言的確定性全域複雜度都落入 \(\mathbf{Poly}\)，則任意 polynomial-time nondeterministic machine 所決定的語言，都有某個 deterministic polynomial-time realization，因此可建立對應的 polynomial completion-rate realization。

### 6.2 USRT \(\Rightarrow\) USEG

若 \(N\) 已被轉換成 deterministic polynomial machine \(D_N\)，則：

\[
S_{D_N}(x,0)
\to
S_{D_N}(x,1)
\to
\cdots
\to
S_{D_N}(x,T)
\]

本身就是一條 polynomial-length、decision-sufficient 的有效 deterministic sequence。

### 6.3 USEG \(\Rightarrow\) GCC

若每一個 NP computation family 都能被 deterministic polynomially generated 的：

\[
Z_0\to Z_1\to\cdots\to Z_m
\]

精確代表，則確定性機器只需生成此序列並讀出 \(\operatorname{Dec}(Z_m)\)，從而得到 polynomial-time deterministic decision procedure。

此處需要後續工作補足的，不是上述直覺，而是每個定義中的 uniformity、encoding、construction cost、state size、precision 與 simulation overhead 的完整形式化。

---

## 7. 第四層：全域無損完成態 GLC

前三層回答：

> 能不能在多項式資源中做到？

第四層回答：

> 最後是否真的交付一個無條件符合驗收規格的完成結果？

因此 GLC 是**閉合條件**，而不是簡單的第四個等價參數。

### 7.1 最終帳本

對演算法 \(A\) 與輸入 \(x\)，定義最終帳本：

\[
\mathcal L_A(x)
=
(
C_A,
F_A,
B_A,
R_A,
S_A,
\Lambda_A
),
\]

其中可分別理解為：

- \(C_A\)：Correctness；
- \(F_A\)：Completion / Finality；
- \(B_A\)：Resource Budget；
- \(R_A\)：Completion Rate；
- \(S_A\)：Effective Sequence Cost；
- \(\Lambda_A\)：Semantic Loss。

定義合格集合：

\[
\mathcal A_{\mathrm{final}}.
\]

最終驗收只要求：

\[
\forall x,\quad
\mathcal L_A(x)
\in
\mathcal A_{\mathrm{final}}.
\]

其最低規格為：

\[
C_A=1,
\]

\[
F_A=1,
\]

\[
B_A\in\mathbf{Poly},
\]

\[
R_A\in\text{Polynomial Completion Cone},
\]

\[
S_A\in\mathbf{Poly},
\]

以及：

\[
\Lambda_A=0.
\]

因此本文採取一種**outcome-accounting** 視角：

\[
\boxed{
\text{過程自由，最終帳本不自由。}
}
\]

演算法中間可以：

- 切換資料結構；
- 切換表示；
- 使用不同局部演算法；
- rollback；
- restart；
- prune；
- recompute；
- 暫停後繼續；

但只要這些操作被允許，就必須全部被計入最終資源帳，且最終輸出不可錯誤、不可遺失決策語義。

---

## 8. GLC 的弱版與強版

這裡必須區分兩種不同主張。

### 8.1 標準 GLC

在標準 deterministic Turing-machine / RAM-style complexity setting 中，一個宣稱決定語言 \(L\) 的 P 演算法，本來就必須：

\[
\forall x
\]

在 polynomial time 內停止並輸出正確答案。

這與程式驗證中的 total correctness——「停止且結果正確」——具有直接類比 [4]。

因此：

\[
\boxed{
\mathrm{GLC}_{\mathrm{std}}
}
\]

主要是把傳統 P 中已經隱含的 correctness + termination 顯式寫入最終帳本。

它不應被宣稱為比 \(P=NP\) 更強的新結論。

### 8.2 Robust GLC

若進一步允許一個執行歷史集合：

\[
\operatorname{Runs}_{\mathrm{adm}}(A,x),
\]

其中包含：

- rerouting；
- representation switching；
- rollback；
- restart；
- 有限可恢復故障；
- 合法 scheduler variation；

並要求：

\[
\forall\pi\in
\operatorname{Runs}_{\mathrm{adm}}(A,x),
\]

最終都存在：

\[
t<\infty
\]

使：

\[
\pi_t\in H_L(x),
\]

且：

\[
\operatorname{out}(\pi_t)=\chi_L(x),
\]

則得到：

\[
\boxed{
\mathrm{GLC}_{\mathrm{robust}}.
}
\]

這是一個更強的 resilient / dynamical property，不再與傳統 \(P=NP\) 自動等價。

同時，若允許「永久斷電、永久不調度、不可恢復物理毀滅」仍要求一定完成，則命題本身不可能。因此 robust GLC 必須只量化於**合法且最終可繼續的擾動集合**。

---

## 9. P/NP 動態四層閉合框架

本文最終提出：

\[
\boxed{
\textbf{P/NP Dynamic Four-Layer Closure Framework}
}
\]

其結構為：

### Layer I：Global Complexity

\[
\boxed{\mathrm{GCC}}
\]

回答：

> 最終所需確定性計算資源，是否位於合理模型下的 polynomial equivalence class？

### Layer II：State-Rate Transformation

\[
\boxed{\mathrm{USRT}}
\]

回答：

> 非確定性 polynomial completion dynamics，是否可全稱轉成確定性 polynomial completion dynamics？

### Layer III：Effective Sequence Generation

\[
\boxed{\mathrm{USEG}}
\]

回答：

> 非確定性 sequence family，是否可被精確壓縮成 deterministic polynomial effective sequence？

### Layer IV：Global Lossless Completion

\[
\boxed{\mathrm{GLC}}
\]

回答：

> 在最終帳本中，是否所有要求均被滿足，且錯誤結果為零、語義損失為零、計算真正完成？

因此整體可寫為：

\[
\boxed{
\left[
\mathrm{GCC}
\equiv
\mathrm{USRT}
\equiv
\mathrm{USEG}
\right]
\overset{\mathrm{GLC}}{\Longrightarrow}
\text{Closed Exact Computation}.
}
\]

在標準可靠計算模型中，若前三項最終被證明皆與 \(P=NP\) 等價，則 \(\mathrm{GLC}_{\mathrm{std}}\) 可視為其顯式終態要求；robust GLC 則保留為更強的後續動態延伸。

---

## 10. 「最終帳本」與過程不可知的界線

本文的「只驗收最終帳本」不等於完全忽略過程成本。

如果演算法：

\[
A
\]

中途做了：

\[
2^{2^n}
\]

步計算，最後才交出正確答案，那麼它的 Resource 欄位必然不合格。

因此：

\[
\boxed{
\text{不問過程細節}
\neq
\text{不計過程成本}.
}
\]

比較精確的說法是：

> 驗收層不要求演算法遵守固定內部機制，但所有內部機制所造成的可計價資源成本，必須被壓縮進最終帳本。

所以最終帳本是一個**path-agnostic but cost-complete** 的 interface。

這個區分對框架非常重要。

---

## 11. 本文不主張的內容

為避免與正式 P/NP 證明混淆，本文明確不主張：

1. 已證明 \(\mathrm{GCC}\iff\mathrm{USRT}\iff\mathrm{USEG}\) 的完整形式定理；
2. 已證明上述三者與 \(P=NP\) 的全部方向；
3. 已找到對 SAT 有效的 polynomial sequence quotient；
4. 原始 nondeterministic path cardinality 本身能推出時間下界；
5. 任意 Turing-complete 計算模型都具有相同複雜度；
6. robust GLC 與標準 \(P=NP\) 等價；
7. 本框架排除了 relativization、natural proofs、algebrization 等既有 barrier；
8. 本文提供 \(P=NP\) 或 \(P\neq NP\) 的證明。

本文目前的學術定位應為：

\[
\boxed{
\text{heuristic reformulation + formalization agenda}.
}
\]

---

## 12. 形式化研究主線

若此框架要從概念論文進一步成為可檢驗數學理論，至少需要完成以下工作。

### 12.1 GCC 的模型定理

明確定義：

\[
\mathfrak M_{\mathrm{adm}}
\]

及可接受 simulation relation，證明 GCC 不依賴某個特定機器表示。

### 12.2 USRT 的等價定理

證明或反駁：

\[
P=NP
\iff
\mathrm{USRT}
\]

並固定：

- machine encoding；
- clock encoding；
- uniform transformation；
- transformation construction cost；
- per-machine polynomial exponent 的量詞次序。

### 12.3 USEG 的非循環定義

最困難的工作之一，是定義「decision-sufficient effective sequence」而不把 SAT solver 偷藏進 quotient relation 本身。

必須精確控制：

\[
T_{\mathrm{construct}},
\quad
L_{\mathrm{state}},
\quad
T_{\mathrm{update}},
\quad
T_{\mathrm{decode}}.
\]

### 12.4 三相等價

分別證明：

\[
\mathrm{GCC}\Rightarrow\mathrm{USRT},
\]

\[
\mathrm{USRT}\Rightarrow\mathrm{USEG},
\]

\[
\mathrm{USEG}\Rightarrow\mathrm{GCC},
\]

並確認沒有任何方向只是定義上的循環。

### 12.5 GLC 驗收語義

將最終帳本：

\[
\mathcal L_A(x)
\]

形式化，區分：

\[
\mathrm{GLC}_{\mathrm{std}}
\]

與：

\[
\mathrm{GLC}_{\mathrm{robust}},
\]

並避免把工程容錯性誤寫成傳統 complexity-theoretic 必要條件。

---

## 13. 討論

這套四層框架的核心價值，不在於把「多項式時間」改名為「速率」，而在於將 P/NP 的同一個核心困難拆成四種研究接口。

第一個接口問資源：

\[
\text{需要多少？}
\]

第二個接口問動力學：

\[
\text{完成態如何以何種速率到達？}
\]

第三個接口問表示與生成：

\[
\text{大量可能歷史如何被精確壓縮？}
\]

第四個接口問封閉性：

\[
\text{最後交付的結果是否真的符合全部規格？}
\]

其中真正可能產生新數學內容的部分，尤其集中於 USEG。因為由一個已知 deterministic polynomial algorithm 產生 polynomial state sequence 並不困難；困難的是在尚未假設 \(P=NP\) 時，能否獨立構造一種有效 quotient / aggregation mechanism，將 NP computation family 的存在量詞精確折疊為 polynomial deterministic sequence。

同樣地，GCC 與 USRT 可能最終證明只是標準 P/NP 的不同座標，而 USEG 的形式化可能迫使研究者明確回答：

> 「究竟什麼叫做不逐一展開候選、卻仍精確保留所有與最終決策相關的資訊？」

這與動態規劃、狀態壓縮、知識編譯、代數消元、quotient construction 等既有技術具有結構上的相似性，但本文目前不主張存在一個可覆蓋一般 SAT 的通用形式。

---

## 14. 結論

本文提出「P/NP 動態四層閉合框架」，將傳統 P vs. NP 的核心問題重新表述為四個相互銜接的層次：

\[
\boxed{
\mathrm{GCC}
:
\text{全域計算複雜度}
}
\]

\[
\boxed{
\mathrm{USRT}
:
\text{全稱狀態速率變換}
}
\]

\[
\boxed{
\mathrm{USEG}
:
\text{全稱有效序列生成}
}
\]

以及：

\[
\boxed{
\mathrm{GLC}
:
\text{全域無損完成}.
}
\]

前三層被提出為與 \(P=NP\) 可能等價的三種觀察座標：

\[
\boxed{
\mathrm{GCC}
\stackrel{?}{\Longleftrightarrow}
\mathrm{USRT}
\stackrel{?}{\Longleftrightarrow}
\mathrm{USEG}
\stackrel{?}{\Longleftrightarrow}
P=NP.
}
\]

問號表示本文尚未提供完整形式化證明。

第四層 GLC 則不是用來改變 P/NP 的標準定義，而是把「最後一定要正確完成」顯式寫成閉合條件。其最簡潔的工程式表述為：

\[
\boxed{
\text{過程自由，最終帳本不自由。}
}
\]

計算可以換路、改表示、重算或使用任何合法中介機制；但最終必須：

\[
\boxed{
\text{Correct}
=
1,
\qquad
\text{Complete}
=
1,
}
\]

\[
\boxed{
\text{Resource}
\in
\mathbf{Poly},
}
\]

\[
\boxed{
\text{Semantic Loss}
=
0.
}
\]

因此，本文真正提出的不是一個 P/NP 結論，而是一條新的形式化研究路線：

\[
\boxed{
\text{資源}
\rightarrow
\text{速率}
\rightarrow
\text{序列}
\rightarrow
\text{無損完成}.
}
\]

若未來能夠在不循環定義、不隱藏超多項式成本、且保持標準 uniform complexity accounting 的前提下，證明前三者與傳統 \(P=NP\) 的完整等價，並對其中某一層建立非平凡的構造或不可能性定理，則此框架才會從啟發式概念進一步成為真正的複雜度理論工具。

目前，本文僅主張：**這是一個可被形式化、可被反駁、也可被逐層證明或拆解的研究框架。**

---

## 參考文獻

[1] Cook, S. A. *The P versus NP Problem*. In: **The Millennium Prize Problems**. Clay Mathematics Institute / American Mathematical Society.

[2] Cobham, A. “The Intrinsic Computational Difficulty of Functions.” Proceedings of the 1964 International Congress for Logic, Methodology, and Philosophy of Science, 1965.

[3] Computational Complexity Theory, *Stanford Encyclopedia of Philosophy*. 關於 Cobham–Edmonds Thesis、Invariance Thesis 與合理計算模型之多項式模擬。

[4] Cornell University CS3110 / CS4110 course materials. 關於 partial correctness、termination 與 total correctness 的標準區分。

[5] Blum, M. “A Machine-Independent Theory of the Complexity of Recursive Functions.” *Journal of the ACM*, 1967.

---

## 作者註記

本文屬於 P/NP 動態速率研究線的概念重整稿。其目的不是將尚未證明的等價寫成定理，而是把先前分散於「計算資源、狀態轉移、序列生成、結果驗收」的直覺，統一到同一個形式化框架中。後續所有證明工作應以標準 P/NP 定義為基準，並將任何新定義逐一與既有複雜度類、計算模型與資源界進行嚴格對照。
