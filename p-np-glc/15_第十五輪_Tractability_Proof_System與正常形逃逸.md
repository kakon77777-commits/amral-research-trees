# P/NP 辯論遊戲研究區｜第十五輪

## Tractability Proof System：可解性證書、正常形逃逸與 clocked enumeration

**Tractability Proof Systems: Certificates, Normal-Form Escape, and Clocked Enumeration**

- **主導研究者：** Neo.K（許筌崴）
- **協作整理：** Aletheia
- **機構：** EveMissLab（一言諾科技有限公司）
- **日期：** 2026 年 8 月 1 日
- **版本：** v1.0
- **研究狀態：** 第十五輪雙假設預演
- **前置文件：** `14_第十四輪_複雜度勢能遊戲與證書完備性陷阱.md`

---

## 摘要

第十四輪提出 **Potential Certificate Completeness Trap**：若 tractability certificate language 太弱，certificate 缺失不能推出超多項式下界；若太強，又容易把原問題偷藏進證書。第十五輪原本因此準備研究：是否可能存在一套 sound、complete、non-circular 的 polynomial-tractability proof system。

本輪首先作出一個重要校正：對**任意圖靈機程式碼**判斷其是否在 polynomial time 內運行，確實不可一般自動判定；但這並不阻止我們建立一個**外延完備（extensionally complete）**的 P 正常形語言。Cobham 的 bounded recursion 與 Bellantoni–Cook 的 safe recursion 都給出此類經典結果：一個函數可在 polynomial time 計算，當且僅當它可由特定受限遞迴語法表示。

因此，本輪區分三種「完備性」：

1. **Machine-index completeness**：對每台任意機器 $M$ 判定它是否 polynomial；
2. **Proof completeness**：每台 polynomial machine 是否都有可驗證 runtime proof；
3. **Extensional normal-form completeness**：每個 P/FP 可計算函數，都存在一個屬於受限語法的等價正常形。

第一種在一般 Turing-machine setting 下不可期待；第三種卻早已有成熟理論。這直接改變遊戲局勢。

等號隊取得新戰略：不必從任意 SAT solver 出發再證明它 polynomial；可以直接在一個「語法即保證 polynomial」的正常形語言裡構造 SAT。若成功構造

$$
t_{\mathrm{SAT}}\in\mathcal G_P
$$

且

$$
\llbracket t_{\mathrm{SAT}}\rrbracket=\chi_{\mathrm{SAT}},
$$

則直接得到

$$
P=NP.
$$

不等號隊得到精確對偶：找一個語義性質 $\mathcal I$，證明它被 $\mathcal G_P$ 的初始函數、composition、safe/bounded recursion 等生成規則保存，但 SAT characteristic function 不具有 $\mathcal I$。若成功，便得到

$$
\chi_{\mathrm{SAT}}\notin FP,
$$

從而

$$
P\neq NP.
$$

這是本系列第一次把「跨表示不變量」與一個已知**完備刻畫 P 的生成語法**接起來。

本輪同時提出第二個正常形：**clocked Turing machines**。對任意機器 $M$ 與固定多項式 clock，建立超時即停止的機器。所有 clocked machines 都在 P，而任何 P 語言都至少有一個等價 clocked representation。這說明「任意程式碼是否屬於 P 的 index property 很難判定」與「P 是否有有效正常形呈現」是兩件不同的事。

下一輪因此進入 **Clocked Enumeration and Diagonalization Game**：既然 P-normal forms 可以有效枚舉，能否逐一對角化擊敗它們，同時讓 diagonal language 保持在 NP？

---

# 一、三種完備性不能混在一起

## 1.1 Machine-index completeness

輸入任意 Turing machine code：

$$
\langle M\rangle.
$$

希望存在演算法判定：

$$
M\text{ 是否在某個 polynomial time bound 內運行。}
$$

一般情況下這類 runtime property 不可判定。

所以不能期待一個萬能 classifier，替任意程式碼自動判定 P/non-P。

## 1.2 Proof completeness

另一種問題是：每個 polynomial machine 是否都有一份有限 runtime certificate？這牽涉 formal proof system、proof strength、formalization 與可能的獨立性，不能與「任意程式碼可被 classifier 判定」混為一談。

## 1.3 Extensional normal-form completeness

真正重要的是：是否存在受限語言 $\mathcal G_P$ 滿足

$$
t\in\mathcal G_P
\Rightarrow
\llbracket t\rrbracket\in FP,
$$

以及

$$
f\in FP
\Rightarrow
\exists t\in\mathcal G_P:
\llbracket t\rrbracket=f.
$$

這種完備性是可能的，而且是 Implicit Computational Complexity 的經典方向。

因此：

$$
\boxed{
\text{無法分類任意程式碼}
\not\Rightarrow
\text{無法給 P 一個 complete normal-form language}
}
$$

---

# 二、Bellantoni–Cook／Cobham：語法本身就是 tractability certificate

Cobham 使用 bounded recursion on notation 刻畫 polynomial-time computable functions；Bellantoni–Cook 則以 safe recursion 建立不必顯式攜帶外部多項式時間界的刻畫。

抽象地寫：

$$
\mathcal G_P
=
\operatorname{Closure}
(\mathcal F_0;\operatorname{Comp},\operatorname{SafeRec}).
$$

其核心結果是：

$$
\boxed{
\operatorname{Denote}(\mathcal G_P)=FP.
}
$$

因此 term membership 本身就是一種 **by-construction tractability certificate**。

這和第十四輪 ATC 不同：

- ATC：事後證明 trajectory polynomial；
- ICC normal form：語法設計使超多項式 growth 根本無法被合法生成。

---

# 三、等號隊的新戰略：直接在 P-normal form 裡寫 SAT

SAT characteristic function：

$$
\chi_{\mathrm{SAT}}(\varphi)
=
\begin{cases}
1,&\varphi\text{ 可滿足},\\
0,&\varphi\text{ 不可滿足}.
\end{cases}
$$

如果等號隊能構造：

$$
t_{\mathrm{SAT}}\in\mathcal G_P
$$

且：

$$
\llbracket t_{\mathrm{SAT}}\rrbracket
=\chi_{\mathrm{SAT}},
$$

由 soundness：

$$
\chi_{\mathrm{SAT}}\in FP.
$$

因 SAT 為 NP-complete：

$$
\boxed{P=NP.}
$$

這條路的優勢是 runtime accounting 被 normal-form meta-theorem 吸收。

---

# 四、不等號隊的新戰略：Grammar Invariant Program

不等號隊現在不用對「所有可能演算法形式」逐一追殺，而可以針對已知 extensionally complete 的 P grammar 做 structural induction。

尋找語義性質：

$$
\mathcal I(f)
$$

使其滿足：

### 基底保存

所有初始函數都有：

$$
\mathcal I(f).
$$

### Composition 保存

若成分皆有 $\mathcal I$，則 composition 後仍有 $\mathcal I$。

### Safe Recursion 保存

若 safe recursion 的前提函數皆有 $\mathcal I$，則生成函數亦有 $\mathcal I$。

因此 structural induction 得：

$$
\forall t\in\mathcal G_P,
\quad
\mathcal I(\llbracket t\rrbracket).
$$

若再能證明：

$$
\neg\mathcal I(\chi_{\mathrm{SAT}}),
$$

則：

$$
\chi_{\mathrm{SAT}}\notin FP,
$$

故：

$$
\boxed{P\neq NP.}
$$

這形成 **Normal-Form Invariant Problem**。

---

# 五、它是否只是把 P/NP 換名字？

如果定義：

$$
\mathcal I(f):=[f\in FP],
$$

當然完全循環。

有價值的 $\mathcal I$ 必須：

1. 由更基本的數學結構獨立定義；
2. 不直接引用 polynomial algorithm 的存在；
3. 能逐生成規則證明 closure；
4. 能獨立證明 SAT 違反；
5. 接受 relativization、natural proofs、algebrization 等障礙審查。

前幾輪尋找的 cross-representation invariant、exact quotientability、algebraic preservation、bridge stability，現在第一次有了一個明確的「歸納域」。

---

# 六、第二個正常形：Clocked Turing Machines

取任意 Turing machine $M$、整數 $k$ 與常數 $c$，建立 clocked machine：

$$
M^{[k,c]}.
$$

對輸入 $x$：

1. 模擬 $M(x)$；
2. 最多執行

$$
c(|x|+1)^k
$$

步；
3. 超時強制停止並輸出固定值。

每個 $M^{[k,c]}$ 都在 P。

枚舉所有有限 machine descriptions 與 $(k,c)$：

$$
C_1,C_2,C_3,\ldots
$$

得到所有 clocked polynomial machines 的有效列舉。

若 $L\in P$，存在某個 $M,k,c$ 使：

$$
T_M(n)\le c(n+1)^k,
$$

故對應 clocked machine 與 $M$ 在所有輸入上等價。

所以：

$$
\boxed{
P\text{ 有有效的正常形呈現。}
}
$$

這不要求判斷任意給定 $M$ 本身是否 polynomial。

---

# 七、對第十四輪 Completeness Trap 的正式修正

第十四輪的二分：

$$
\text{證書太弱}\Rightarrow\text{漏掉 P},
$$

$$
\text{證書太強}\Rightarrow\text{循環},
$$

需要加入第三條路：

$$
\boxed{
\text{改變表示域，使用 by-construction P-normal form。}
}
$$

因此：

$$
\boxed{
\text{Classification completeness}
\neq
\text{Representation completeness}.
}
$$

前者對任意 machine index 太強；後者已有成熟成功案例。

---

# 八、Clocked Enumeration 的誘惑：直接 diagonalize？

既然有：

$$
C_1,C_2,C_3,\ldots
$$

列出所有 P-normal-form machines，不等號隊立刻提出：

$$
L_D(x_i)=1-C_i(x_i).
$$

這能對角化擊敗每個 $C_i$。

但要證明 $P\neq NP$，不只需要：

$$
L_D\notin P.
$$

還必須：

$$
\boxed{
L_D\in NP.
}
$$

而這正是難點。

---

# 九、Exponent Escalation Trap

clocked machines 的 exponent 沒有共同固定上界：

$$
n^{k_1},n^{k_2},n^{k_3},\ldots
$$

若 diagonal machine 在第 $i$ 個對角輸入上完整模擬：

$$
C_i
$$

至：

$$
|x_i|^{k_i},
$$

則自身 runtime exponent 也可能隨 $i$ 增長。

這不保證存在固定 $K$：

$$
T_D(n)\le n^K.
$$

因此：

$$
\boxed{
\text{逐一擊敗所有 polynomial exponents}
}
$$

與：

$$
\boxed{
\text{自己仍停留在固定 polynomial exponent}
}
$$

形成直接張力。

這是 **Exponent Escalation Trap**。

---

# 十、Universal Simulation Overhead 與 NP Witness Trap

即使 exponent 問題可管理，universal diagonal machine 還需解析：

$$
\langle C_i\rangle
$$

並模擬其運行，產生 universal simulation overhead。

更關鍵的是，簡單的 complement diagonal：

$$
1-C_i(x_i)
$$

沒有天然提供 polynomial witness。

所以：

$$
\boxed{
\text{可 diagonalize}
\not\Rightarrow
\text{可 NP-verify}.
}
$$

普通 time hierarchy 可以造出 $P$ 外的 decidable language；真正困難是把 diagonal language 壓進 NP。

---

# 十一、Relativization 警報

若下一輪 diagonalization argument 加上任意 oracle 後仍原樣成立，便會撞上 Baker–Gill–Solovay 類 relativization barrier。

因此下一輪每個候選 diagonal construction 都必須檢查：

$$
\boxed{
\text{加入 oracle 後，論證是否原封不動？}
}
$$

若答案為是，即高度可疑。

---

# 十二、三個等價遊戲介面

經過十五輪，可把傳統問題寫成三種介面。

## 12.1 Algorithm Interface

$$
P=NP
\iff
\exists A_{\mathrm{SAT}}\in P.
$$

## 12.2 Normal-Form Interface

若：

$$
\operatorname{Denote}(\mathcal G_P)=FP,
$$

則：

$$
P=NP
\iff
\exists t\in\mathcal G_P:
\llbracket t\rrbracket=\chi_{\mathrm{SAT}}.
$$

## 12.3 Invariant Interface

若能證明：

$$
\forall t\in\mathcal G_P,
\quad
\mathcal I(\llbracket t\rrbracket),
$$

則：

$$
\neg\mathcal I(\chi_{\mathrm{SAT}})
\Rightarrow
P\neq NP.
$$

這第三種是目前不等號隊最清晰的 structural target。

---

# 十三、與原始動態速率系列接合

原始系列將：

$$
T_{\mathrm{search}},
T_{\mathrm{exec}},
T_{\mathrm{verify}}
$$

分開，並研究智慧體如何生成新表示、記憶與解題策略。

第十五輪則為傳統物件層補上一個乾淨接口：

$$
\boxed{
\text{Discovery Dynamics}
\rightarrow
\text{Normal-Form Compilation}
\rightarrow
\text{Traditional Complexity Claim}.
}
$$

無論智慧體如何發明新演算法，只要聲稱傳統 $P=NP$，最後都必須產生一個在 P-normal form 中有代表的 SAT characteristic function。

---

# 十四、本輪淘汰／修正

## 修正 1

錯誤：

> P 的所有算法無法有效列舉。

修正：

$$
\text{任意 machine index 是否 polynomial 不可一般判定，}
$$

但：

$$
\boxed{
P\text{ 可由 clocked machines／ICC normal forms 有效呈現。}
}
$$

## 修正 2

錯誤：

> sound+complete tractability language 必然不存在。

修正：

對 arbitrary machine classification 太強；extensionally complete P-normal form 則存在。

## 保留 1

certificate failure 不能直接推出下界，除非該 certificate/normal form 對 P 已有 completeness theorem。

## 保留 2

歷史發現成本不能偷算進傳統 runtime。

---

# 十五、雙方戰果

## 等號隊：Normal-Form Escape

新任務：

$$
\boxed{
\text{直接構造 }t_{\mathrm{SAT}}\in\mathcal G_P.
}
$$

## 不等號隊：Grammar Invariant Program

新任務：

$$
\boxed{
\text{找 }\mathcal I\text{，使完整 P grammar 保存它，而 SAT 違反它。}
}
$$

這比前面追逐無限未知表示更適合 structural induction。

---

# 十六、本輪比分

等號隊拿到 Bellantoni–Cook/Cobham 正常形武器：

$$
P=NP:14
$$

不等號隊則把全稱量詞收斂成 Grammar Invariant Program：

$$
P\neq NP:14.
$$

……還是平手。

可能不是控分，是某種 conservation law。歪臉笑。

比分只屬遊戲介面，沒有證明意義。

---

# 十七、第十六輪入口：Clocked Enumeration and Diagonalization Game

下一輪直接玩：

$$
\boxed{
C_1,C_2,C_3,\ldots
}
$$

既然所有 P-normal-form machines 可有效枚舉，能否構造：

$$
L_D
$$

逐一打敗它們，同時保持：

$$
L_D\in NP?
$$

必須正面處理：

1. Exponent Escalation；
2. Universal Simulation Overhead；
3. NP Witness Preservation；
4. Self-reference / indexing；
5. Relativization Barrier；
6. 為何 ordinary time hierarchy diagonalization 沒有早已給出 $P\neq NP$。

---

# 十八、外部理論參照

1. Stephen Bellantoni, Stephen A. Cook, **A New Recursion-Theoretic Characterization of the Polytime Functions**, *Computational Complexity* 2 (1992), 97–110.
2. Alan Cobham, polynomial-time functions via bounded recursion on notation.
3. David Gajser, **Verifying Time Complexity of Turing Machines**, *Theoretical Computer Science* 600 (2015), 86–97.
4. Martin Avanzini, Naohi Eguchi, Georg Moser, **A New Order-theoretic Characterisation of the Polytime Computable Functions**.
5. Implicit Computational Complexity literature on safe recursion, tiering and syntactic characterizations of FP/PTIME.

---

## 本輪裁定

$$
\boxed{
\text{完整的 P 正常形語言不是幻想；真正困難是把 SAT 放進去，或證明它永遠放不進去。}
}
$$

更精確地：

$$
\boxed{
\text{Machine-index verification}
\neq
\text{Extensional P presentation}.
}
$$

這個區分修正了第十四輪的一個過度悲觀傾向，也為兩隊提供了目前最乾淨的對偶任務：

$$
\boxed{
P=NP:\quad\text{構造 SAT 的 P-normal form};
}
$$

$$
\boxed{
P\neq NP:\quad\text{找出完整 P grammar 保存、但 SAT 違反的語義不變量}.
}
$$
