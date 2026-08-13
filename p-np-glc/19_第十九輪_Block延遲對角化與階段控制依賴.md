# P/NP 辯論遊戲研究區｜第十九輪

## Block／Delayed Diagonalization：密度逃逸、階段控制與條件性進度

**Block and Delayed Diagonalization: Density Escape, Stage Control, and Conditional Progress**

- **主導研究者：** Neo.K（許筌崴）
- **協作整理：** Aletheia
- **機構：** EveMissLab（一言諾科技有限公司）
- **日期：** 2026 年 8 月 1 日
- **版本：** v1.0
- **研究狀態：** 第十九輪雙假設預演
- **前置文件：** `18_第十八輪_對角切片壓縮與稀疏性上推陷阱.md`
- **遊戲態度：** 研究已進入「複雜度理論妖魔鬼怪區」，但所有結論繼續做嚴格分層

---

## 摘要

第十八輪發現：若 diagonal slice 每台 P 機器只配置少數 designated points，所構造語言容易變成 sparse／tally-like；若此稀疏語言真的落在 $NP-P$，Hartmanis–Immerman–Sewelson 的 upward-separation 結果會牽動更高 deterministic／nondeterministic single-exponential time separation。若反過來把 diagonal family 做得太密，又容易回到第十六、十七輪的 uniform exponent barrier 與 universalization complexity jump。

本輪因此測試一條自然中間路線：不用單點 diagonalization，而使用長度區塊、階段（stage）與延遲（delay）機制。令

$$
I_s=[N_s,N_{s+1})
$$

為第 $s$ 個長度 block，在不同 block 中讓語言呈現不同模式，例如 SAT-like、empty-like、或某種可計算局部模式。直覺上，若 SAT-like blocks 無限出現且足夠寬，語言可以避免 sparse barrier；若每個 requirement 只在極晚期才處理，又似乎可能替昂貴 diagonalization 爭取時間。

本輪結果是：**block/delay 確實能避開「太稀」這個結構性陷阱，但不能靠單純等待消除同一輸入上的無界 polynomial exponent。** 對任意固定 $K$ 與 $k>K$，不存在「等到 $n$ 夠大」就讓

$$
n^k\le n^K
$$

成立；所以第十六輪的 Uniform Exponent Barrier 不會因 block 變大而消失。

Ladner delayed diagonalization 的真正技巧不是「等到輸入夠大後硬模擬所有高 exponent machines」，而是改變 construction 的控制方式：語言在 SAT-like 與 easy-like phases 之間極慢地切換，phase controller 只在找到有限 counterexample／requirement witness 後才前進。若假設 $P\neq NP$，相應 counterexamples 會存在，因此 controller 會持續推進；若某一階段永久凍結，通常正表示某個候選 P machine／reduction 成功，導向原先假設的 collapse。也就是：

$$
\boxed{
\text{Delayed diagonalization 的 progress 本身是 conditional。}
}
$$

這形成本輪的 **Freeze-or-Separate Principle（FSP）**：

$$
\text{controller 永久凍結}
\Rightarrow
\text{對應 collapse／成功模擬事件},
$$

$$
\text{controller 無限前進}
\Rightarrow
\text{可逐項滿足 diagonal requirements}.
$$

Ladner theorem 正是一個漂亮的例子：在假設 $P\neq NP$ 下，可利用 delayed diagonalization 構造 NP-intermediate language；但這不是 $P\neq NP$ 的證明，因為「階段永遠前進」正由 $P\neq NP$ 保證。

本輪因此把上一輪的 Density--Uniformity Squeeze 修正成更精確的三角壓力：

$$
\boxed{
\text{Density}
\;\text{vs.}\;
\text{Uniform Exponent}
\;\text{vs.}\;
\text{Stage-Control Knowledge}
}
$$

第十九輪沒有得到 separation，但找到了 delayed diagonalization 真正藏成本的位置：**不是 block size，而是 stage controller 知道何時可以安全前進所需的證據。** 第十九輪因此將第二十輪推進到：Stage Controller Complexity——若想讓 controller 無條件、有效且永遠前進，它究竟需要知道什麼？這個 controller 是否會偷偷變成一個 SAT/P-equivalence oracle？

---

# 一、上一輪：為什麼要從「點」改成「塊」？

第十八輪的 diagonal slice：

$$
D=\{x_i:C_i(x_i)=0\}
$$

具有兩個問題。

第一，若每台 machine 只配置很少 designated inputs，$D$ 容易變 sparse。

第二，若直接要求：

$$
D(x_i)=1-C_i(x_i),
$$

則為了計算 $D(x_i)$，可能必須支付：

$$
|x_i|^{k_i},
$$

其中 $k_i$ 無界。

所以提出 block：

$$
I_s=[N_s,N_{s+1}).
$$

希望用一大段長度區間對付第 $s$ 個 requirement，而不是只用一個點。

---

# 二、第一個思想實驗：直接 block diagonalization

最直接的幻想是：

在第 $s$ 個 block 中，對所有 $x$ 定義：

$$
D(x)=1-C_s(x).
$$

這樣整個 block 都與 $C_s$ 相反，當然能保證：

$$
D\neq C_s.
$$

但若：

$$
T_{C_s}(n)=n^{k_s},
$$

那麼 deciding $D(x)$ 在這個 block 仍需：

$$
n^{k_s}.
$$

即使把：

$$
N_s
$$

選得再巨大，也不能讓某個固定全域 $K$ 滿足：

$$
n^{k_s}\le n^K
$$

對所有 $s$ 成立。

---

# 三、Same-Input Exponent Invariance

## 命題 3.1

給定：

$$
k>K.
$$

則對所有：

$$
n>1,
$$

都有：

$$
n^k>n^K.
$$

所以不存在某個 threshold $N$，使：

$$
\forall n\ge N,
\quad n^k\le n^K.
$$

這看似廢話，但對 block diagonalization 很重要。

它說明：

$$
\boxed{
\text{「等久一點」不能修掉同一輸入上的 exponent mismatch。}
}
$$

本輪把它記為：

$$
\boxed{\mathrm{SIEI}=\text{Same-Input Exponent Invariance}.}
$$

因此 delayed diagonalization 若有效，必須做的不是：

> 把同一個昂貴 simulation 延後到更大的同長度輸入。

而是：

> 改變被模擬的對象、輸入尺度、requirement 設計，或讓未完成 requirement 暫時不影響當前 membership computation。

這是 Ladner-style delay 與 naive waiting 的根本差別。

---

# 四、第二個幻想：把一個 diagonal bit 放大成整個 dense block

假設先得到一個 bit：

$$
b_s=1-C_s(y_s),
$$

再定義：

$$
\forall x\in I_s,
\quad
D(x)=b_s.
$$

這樣只用一個 diagonal event，就能把整個 block 填成：

$$
\emptyset
$$

或：

$$
\Sigma^{I_s},
$$

看起來可以立刻避免 sparse。

但 membership algorithm 必須知道：

$$
b_s.
$$

若計算 $b_s$ 仍需要昂貴 simulation，成本只是從「每個 x」搬到「block controller」。

因此引入：

$$
\boxed{\mathrm{AKD}=\text{Amplification Knowledge Debt}.}
$$

即：

$$
\text{把一個 hard bit 放大成很多 strings}
$$

並不會讓 hard bit 變容易。

若 $b_s$ 很容易計算，則 density amplification 很容易；但 diagonal power 也可能隨之消失。

---

# 五、第三個幻想：只要語言夠 dense 就會比較 hard

錯。

例如：

$$
L=\{x:|x|\text{ 為偶數}\}
$$

極度 dense，但：

$$
L\in P.
$$

或者 block language：

$$
L=\bigcup_{s\text{ even}}\{0,1\}^{I_s}
$$

同樣可以 density oscillate，卻 trivial。

所以：

$$
\boxed{
\text{density 是 barrier-management parameter，不是 hardness invariant。}
}
$$

這一點正式淘汰：

$$
\text{dense}
\Rightarrow
\text{hard}
$$

的直覺。

本輪把這叫：

$$
\boxed{\mathrm{DEHG}=\text{Density Escape without Hardness Gain}.}
$$

---

# 六、真正的 delayed diagonalization：不是 block，而是 controller

Ladner theorem 的核心背景是：

假設：

$$
P\neq NP.
$$

則存在：

$$
L\in NP
$$

使：

$$
L\notin P,
$$

但：

$$
L
$$

又不是 NP-complete。

一種常見的理解方式是讓 $L$ 在不同階段／長度上極慢地在：

$$
SAT
$$

與：

$$
\emptyset
$$

或其相關受控版本之間切換。

抽象寫成：

$$
L_g
=
\{x:x\in SAT\land g(|x|)\in A\},
$$

其中：

$$
g(n)
$$

是一個極慢增長、可計算的 stage function。

真正困難不是「讓 $g$ 慢」。

真正困難是：

$$
\boxed{
\text{什麼事件允許 }g\text{ 從 stage }s\text{ 前進到 }s+1？
}
$$

---

# 七、Requirement-driven stage controller

令要求序列為：

$$
R_1,R_2,R_3,\ldots
$$

例如交替要求：

- 第 $i$ 個 P machine 不等於 $L$；
- 第 $i$ 個 polynomial reduction 不能證明 $L$ NP-complete；
- 或 equivalently，在 oracle-machine 版本中讓相應機器出現 disagreement。

stage controller 在 stage $s$ 做：

$$
\text{搜尋一個有限 witness，證明 }R_s\text{ 已被滿足。}
$$

找到 witness 後：

$$
s\leftarrow s+1.
$$

找不到時：

$$
s\text{ 不變}.
$$

重點：語言 membership 不需要一次完成未來所有 stages；它只需要在輸入長度允許的資源內重新計算「目前已經到哪一階段」。

這就是 delayed／lazy diagonalization 的真正結構。

---

# 八、Freeze-or-Separate Principle

本輪把上述邏輯抽象成：

$$
\boxed{\mathrm{FSP}=\text{Freeze-or-Separate Principle}.}
$$

對某一 requirement $R_s$：

## Case A：找到 finite disagreement witness

則：

$$
R_s\text{ 被滿足},
$$

controller 可前進。

## Case B：永遠找不到 witness

則候選 machine／reduction 可能真的在所有相關輸入上成功。

在 Ladner 類構造中，這通常會推出：

$$
SAT\in P
$$

或其他與假設：

$$
P\neq NP
$$

矛盾的 collapse。

因此在假設：

$$
P\neq NP
$$

下，Case B 被排除，stage controller 必須持續前進。

所以：

$$
\boxed{
P\neq NP
\Rightarrow
\text{all finite requirements eventually progress}.
}
$$

但注意量詞方向。

Ladner theorem 使用：

$$
P\neq NP
$$

作為前提來保證 controller progress。

它沒有從：

$$
\text{controller progress}
$$

無條件推出：

$$
P\neq NP.
$$

---

# 九、Assumption-Activated Progress

這是本輪最重要的校正。

定義：

$$
\boxed{\mathrm{AAP}=\text{Assumption-Activated Progress}.}
$$

若某 construction 的 stage unboundedness：

$$
g(n)\rightarrow\infty
$$

需要先假設：

$$
P\neq NP,
$$

那麼該 construction 可以證明：

> **若 $P\neq NP$，則存在具有某些精細結構的語言。**

但不能把這個結構反過來當作 $P\neq NP$ 的無條件證明。

這正是 Ladner theorem 的地位。

---

# 十、為什麼 Ladner delay 能做 block，而 naive direct diagonalization 不行？

## Naive direct diagonalization

要求在 input $x$ 當下計算：

$$
1-C_i(x).
$$

因此直接支付：

$$
|x|^{k_i}.
$$

UEB 立即出現。

## Delayed requirement construction

不是要求 membership algorithm 在每個 stage 都立刻完成：

$$
1-C_i(x)
$$

這個 same-input complement。

而是：

1. 語言當前維持一個已知 NP-safe mode；
2. controller 慢慢搜尋 requirement witness；
3. witness 找到後，才改變未來區間的 mode；
4. 對任意固定輸入，只需重建有限 stage history。

因此 delay 解決的是：

$$
\boxed{
\text{construction scheduling／finite injury／stage accounting}
}
$$

而不是：

$$
\boxed{
\text{把任意 }n^{k_i}\text{ 壓成固定 }n^K.
}
$$

---

# 十一、與第十八輪 sparse barrier 的關係

Hartmanis–Immerman–Sewelson（1985）證明，在他們使用的 single-exponential EXPTIME／NEXPTIME 記號下：

$$
\boxed{
\exists\text{ sparse }S\in NP-P
\iff
EXPTIME\neq NEXPTIME.
}
$$

該文還特別指出：Ladner-style delayed diagonalization 在僅假設 $P\neq NP$ 的前提下，不能僅靠修改 construction 就產生 sparse $NP-P$ witness，除非同時得到更高階 separation。

這與第十八輪結果完全一致。

所以 block/density schedule 真正的功能之一是：

$$
\boxed{
\text{讓構造不再被迫 sparse。}
}
$$

例如只要 SAT-like active blocks 無限出現，且每個 active block 含有足夠多 strings，整體語言就可以是 non-sparse。

但：

$$
\text{non-sparse}
$$

只表示你避開 SUST；並不表示你獲得 lower bound。

---

# 十二、Density Schedule 作為第三種資源

本輪把第十八輪：

$$
\text{Density--Uniformity Squeeze}
$$

升級為：

$$
\boxed{
\text{Density--Uniformity--Control Triangle}
}
$$

三個頂點：

## 12.1 Density

太稀：

$$
\rightarrow
\text{upward-separation pressure}.
$$

## 12.2 Uniform Runtime

太直接／太 universal：

$$
\rightarrow
\text{UEB / UCJ / certificate escalation}.
$$

## 12.3 Stage-Control Knowledge

若使用 adaptive delay：

$$
\rightarrow
\text{controller 必須知道何時 requirement 已真正被滿足}.
$$

因此「中間密度」不是免費第三條路。

它把成本推到：

$$
\boxed{
\text{schedule/controller knowledge}.
}
$$

---

# 十三、Block Size 不能取代 Stage Witness

假設 requirement：

$$
R_s:
\quad
M_s\neq SAT.
$$

把下一個 block：

$$
I_s
$$

設得再大，都不能憑 block size 本身證明：

$$
M_s\neq SAT.
$$

真正允許 controller 前進的是某個：

$$
y_s
$$

使：

$$
M_s(y_s)\neq SAT(y_s).
$$

所以：

$$
\boxed{
\text{geometric delay}
\neq
\text{semantic witness}.
}
$$

本輪把需要這個 witness 的成本記為：

$$
\boxed{\mathrm{SWD}=\text{Stage Witness Debt}.}
$$

---

# 十四、等號隊的反擊：如果 stage 永遠凍結呢？

等號隊突然發現 delayed diagonalization 很適合自己。

若 construction 在某個 candidate machine：

$$
M_s
$$

上永遠找不到：

$$
M_s(y)\neq SAT(y),
$$

那麼可能正因：

$$
M_s=SAT.
$$

如果 $M_s$ 是 polynomial-time machine，這直接給：

$$
SAT\in P.
$$

所以等號隊的新口號是：

> 你們的 controller 不動，也許不是 construction 壞了；也許是我贏了。（歪臉笑）

因此 delayed diagonalization 天生是一個 conditional bifurcation machine：

$$
\boxed{
\text{freeze}
\quad\text{vs.}\quad
\text{progress}
}
$$

兩個 branch 分別對應不同 complexity world。

---

# 十五、不等號隊的反擊：那我能不能讓 controller 無條件前進？

這就是下一個真正危險的想法。

若能設計一個 polynomially reconstructible controller：

$$
\mathcal C(s,n)
$$

使它：

1. 對每個 P-machine requirement 都最終前進；
2. 不假設 $P\neq NP$；
3. 每次前進都附帶 sound finite witness；
4. 整體構造的語言仍在 NP；
5. 最終又與所有 P machines 不同；

那麼它本身已經非常接近：

$$
\boxed{P\neq NP}
$$

的構造性證明。

所以問題被重新定位為：

$$
\boxed{
\text{Stage controller 如何知道「現在可以安全前進」？}
}
$$

---

# 十六、Controller Completeness Trap

若 controller 的規則是：

> 當且僅當找到 counterexample 才前進。

那它是 sound，但是否 progress 取決於 counterexample 是否存在。

若改成：

> 即使沒有找到 counterexample，我也會在某個時間點猜測前進。

則可能失去 diagonal guarantee。

若 controller 能正確判斷：

$$
\forall y,
\quad
M_s(y)=SAT(y),
$$

它就在判斷一個極強的 semantic equivalence property。

所以形成：

$$
\boxed{\mathrm{CCT}=\text{Controller Completeness Trap}.}
$$

- 太保守：可能永遠 freeze；
- 太積極：可能錯過 requirement；
- 太全知：controller 自己就攜帶接近原問題的能力。

---

# 十七、Ladner theorem 真正教了我們什麼？

不是：

> 「delay 可以證明 $P\neq NP$。」

而是：

$$
\boxed{
\text{若已知 separation，delay 可以把 separation 塑造成更精細的內部結構。}
}
$$

即：

$$
P\neq NP
\Rightarrow
\text{NP 裡不只有 P 與 NP-complete 兩層。}
$$

這是一個 **structure-from-separation** theorem，
而不是 **separation-from-structure** theorem。

這個方向不能偷換。

---

# 十八、本輪對兩隊的實際意義

## $P=NP$ 隊

新策略：

$$
\boxed{
\text{找一個 stage requirement 永遠無法產生 disagreement witness。}
}
$$

若對應的是 P machine deciding SAT，controller freeze 就反而成為 equality certificate 的候選。

當然，證明「永遠無 disagreement」本身就是難點。

---

## $P\neq NP$ 隊

新策略：

$$
\boxed{
\text{把所有 requirement 的 progress 證明從假設中拔掉，變成無條件 structural theorem。}
}
$$

也就是證明：

$$
\forall s,
\quad
\exists\text{ finite disagreement witness},
$$

而不能預先使用：

$$
P\neq NP.
$$

這幾乎就是 separation 的核心。

---

# 十九、已知障礙審查

## 19.1 Relativization

Ladner-style diagonalization／stage arguments高度依賴 diagonalization；Baker–Gill–Solovay 告訴我們，純 relativizing diagonal argument 不可能單獨解決 $P$ vs $NP$。

因此若未來 controller 真能無條件 progress，必須檢查其中是否出現 non-relativizing ingredient。

## 19.2 Sparse upward separation

block/dense phases 可以避開 sparse witness，但只是避障，不是 lower bound。

## 19.3 Uniform exponent

delay 不改變 SIEI；若同一輸入仍須模擬 $n^{k_i}$，UEB 原封不動。

## 19.4 Discovery vs runtime

controller 在數學家腦中「知道」某 requirement 應該有 counterexample，不能算作 language decider 已經有該 witness。

---

# 二十、本輪淘汰的錯誤路線

1. 「block 夠大就能讓任意 $n^{k_i}$ 變成固定 $n^K$。」——錯，SIEI。
2. 「把一個 diagonal bit 複製到整個 block 就能免費增加 hardness。」——錯，AKD。
3. 「non-sparse 所以比較可能不在 P。」——無此推論。
4. 「Ladner theorem 已經靠 diagonalization 證明存在 $NP-P$。」——它以 $P\neq NP$ 為前提。
5. 「stage function 很慢，所以 construction 自動可行。」——慢只是 scheduling；progress 還需 requirement witness。
6. 「只要永遠等待，counterexample 總會出現。」——只有在相應 separation／non-equivalence 已成立時才保證。
7. 「若 controller freeze 就表示 construction 失敗。」——可能恰好表示 candidate machine 真成功，對等號隊反而是訊號。

---

# 二十一、本輪正式新增概念

$$
\boxed{\mathrm{SIEI}}
$$
Same-Input Exponent Invariance

$$
\boxed{\mathrm{AKD}}
$$
Amplification Knowledge Debt

$$
\boxed{\mathrm{DEHG}}
$$
Density Escape without Hardness Gain

$$
\boxed{\mathrm{FSP}}
$$
Freeze-or-Separate Principle

$$
\boxed{\mathrm{AAP}}
$$
Assumption-Activated Progress

$$
\boxed{\mathrm{SWD}}
$$
Stage Witness Debt

$$
\boxed{\mathrm{CCT}}
$$
Controller Completeness Trap

以及：

$$
\boxed{
\text{Density--Uniformity--Control Triangle}
}
$$

---

# 二十二、本輪比分

這輪一開始看起來像不等號隊終於拿到 Ladner delayed diagonalization 這把大武器。

結果仔細一看：

$$
\text{它的 progress 保證居然先假設 }P\neq NP.
$$

等號隊立刻表示：

> 那你卡住的時候，搞不好就是我贏了啊？

所以：

$$
P=NP:18
$$

$$
P\neq NP:18.
$$

比分守恆定律持續成立。

這已經不是控分了，這像 Hamiltonian。（歪臉笑）

比分僅為遊戲介面，不具有證明意義。

---

# 二十三、第二十輪入口：Stage Controller Complexity

下一輪不再研究 block 本身，而研究：

$$
\boxed{
\text{誰在控制 block？}
}
$$

核心問題：

$$
\boxed{
\text{能否設計一個無條件、有效、sound 且永遠 progress 的 stage controller？}
}
$$

具體拆成：

1. controller 如何確認第 $s$ 個 candidate P machine 已被擊敗？
2. finite disagreement witness 是否足夠？
3. 若 witness 尚未出現，controller 如何區分「只是還沒找到」與「永遠不存在」？
4. controller 若能判斷後者，是否已具備 SAT/P-machine equivalence oracle 的能力？
5. 是否能使用 non-relativizing algebraic／arithmetization information 替代純搜索？
6. 是否存在一種 proof-carrying stage transition：

$$
(s,\pi_s)\rightarrow s+1
$$

其中 $\pi_s$ 可在固定 polynomial overhead 驗證？
7. 如果所有 stages 都有短 proof，是否又會撞回第十七輪的 universal certificate compression jump？

第二十輪因此會把：

- delayed diagonalization；
- proof certificates；
- controller knowledge；
- non-relativizing ingredients

四條線正式合流。

---

# 二十四、外部理論參照

1. Richard E. Ladner, 1975/1970s NP-intermediate theorem line；現代 complexity lecture notes常以 delayed／lazy diagonalization 說明：若 $P\neq NP$，NP 中存在既不在 P、也非 NP-complete 的語言。

2. MIT 6.841 / 18.405J Advanced Complexity Theory, Lecture 2: Diagonalization, Ladner's Theorem, Relativization。講義明確展示以 polynomial-time oracle machines、SAT-like／empty-like 行為與延遲 requirement search 構造 Ladner language 的方式。

3. J. Hartmanis, N. Immerman, V. Sewelson, **Sparse Sets in NP-P: EXPTIME versus NEXPTIME**, Information and Control 65 (1985), 158–181。該文證明 sparse $NP-P$ sets 與其所定義 single-exponential deterministic/nondeterministic time separation 的等價，並明確討論 Ladner delayed diagonalization 無法只靠修改就產生 sparse $NP-P$ witness，除非得到更高階 separation。

4. Stephen Mahaney, **Sparse Complete Sets for NP: Solution of a Conjecture of Berman and Hartmanis**, JCSS 25 (1982)。若 NP 有 sparse many-one complete set，則 $P=NP$。

5. Baker–Gill–Solovay relativization barrier：純 relativizing diagonalization 不能單獨解決原始 $P$ vs $NP$。

---

## 本輪裁定

$$
\boxed{
\text{Block / delay 可以重新安排何時付帳，但不能讓帳單本身消失。}
}
$$

更精確地：

$$
\boxed{
\text{Ladner delay 的核心資源不是 block size，而是 stage-controller progress。}
}
$$

而 stage progress 若由：

$$
P\neq NP
$$

保證，就只能得到 conditional structural theorem。

因此下一步真正值得攻擊的是：

$$
\boxed{
\text{Stage Controller Knowledge / Proof Complexity}.
}
$$
