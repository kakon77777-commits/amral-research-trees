# P/NP 辯論遊戲研究區｜第二十三輪

## 演算法 WQO 與語義單調性裂縫：為什麼 Graph-Minor 式有限禁阻集沒有直接搬進 P/NP

**Algorithmic WQO and the Semantic-Monotonicity Gap: Why Graph-Minor-Style Finite Obstructions Do Not Transfer Directly to P vs NP**

- **主導研究者：** Neo.K（許筌崴）
- **協作整理：** Aletheia
- **機構：** EveMissLab（一言諾科技有限公司）
- **日期：** 2026 年 8 月 1 日
- **版本：** v1.0
- **研究狀態：** 第二十三輪雙假設預演
- **前置文件：** `22_第二十二輪_量詞壓縮定理與有限基底遊戲.md`
- **本輪主題：** Algorithmic Well-Quasi-Order Game

---

## 摘要

第二十二輪提出一個最接近 Robertson–Seymour 路線的構想：若能在 P-normal-form algorithms 上定義一個 well-quasi-order（WQO），並讓「SAT correctness」或「SAT failure」對該 order 呈 upward/downward monotone，則可以期待某種有限禁阻集／有限基底定理，將對無限演算法空間的量詞壓成有限結構。

第二十三輪真正測試這個想法後，得到一個重要修正：**WQO 本身其實不難取得。**

對有限 alphabet 的程式文字，Higman lemma 已給出 subsequence WQO；對有限標籤的程式語法樹，Kruskal tree theorem 給出 homeomorphic-embedding WQO。更直接地，homeomorphic embedding 已長期被 supercompilation、partial evaluation、symbolic transformation 等程式轉換技術用來保證在線展開終止。

因此：

$$
\boxed{
\text{Algorithmic WQO scarcity is not the core bottleneck.}
}
$$

真正失敗的是第二個條件：**自然的 syntactic WQO 幾乎不會讓 SAT correctness / failure 具有所需單調性。**

若：

$$
A\preceq_{\mathrm{syn}} B
$$

只表示 A 的 syntax tree homeomorphically embeds into B，則完全可能：

$$
A\text{ correct},\quad B\text{ incorrect},
$$

也完全可能：

$$
A\text{ incorrect},\quad B\text{ correct}.
$$

所以 good/bad solver sets 並非 natural syntactic order 下的 upward/downward-closed sets；Graph-Minor 式 finite obstruction theorem 因而沒有啟動。

反過來，如果我們把 order 改成 semantic order，使 correctness 天然 monotone，例如「B 能精確模擬 A」或「A 與 B 在所有輸入上語義等價」，則會出現新的問題：order 可能不再是 WQO、不再有效可判定、退化成 equivalence classes，或直接把程式語義／complexity claim 偷進 order definition。

本輪因此提出核心障礙：

$$
\boxed{
\mathrm{WSAB}
=
\text{WQO--Semantic Alignment Barrier}
}
$$

以及更具操作性的三難：

$$
\boxed{
\text{Structural WQO}
\;\;\text{vs.}\;\;
\text{Semantic Monotonicity}
\;\;\text{vs.}\;\;
\text{Effective/Non-circular Resource Relevance}
}
$$

目前自然候選通常只能同時拿到其中兩項，甚至只拿到一項。

本輪最重要的正面結果則是：**Bellantoni–Cook/Cobham 類 P-normal-form grammar 的 derivation trees 本身可以套用 Kruskal 型 WQO。**因此第十五輪的 Grammar Invariant Program 與第二十二輪 finite-basis program 可以被放在同一個空間中測試。失敗點已由「沒有 order」精確收斂為「缺乏一個讓語義性 hardness/correctness 具 closure 的 order」。

下一輪因此不再找 WQO，而是研究 **Semantic Monotonicity Engineering**：是否能透過 abstract interpretation、behavioral abstraction、simulation quotient 或 resource-aware semantics，構造一個同時具有 WQO、monotonicity、effectiveness 與 non-circularity 的「solver abstraction order」。

---

# 一、第二十二輪的有限基底夢想

第二十二輪使用 Robertson–Seymour / WQO 的標準結構：

若：

$$
(X,\preceq)
$$

是一個 WQO，且：

$$
U\subseteq X
$$

是 upward closed：

$$
x\in U,\;x\preceq y
\Rightarrow
y\in U,
$$

則 $U$ 的 minimal elements 形成有限集合：

$$
\min(U)=\{b_1,\ldots,b_m\}.
$$

因此：

$$
x\in U
\iff
\exists j\le m:\ b_j\preceq x.
$$

這就是 finite-basis quantifier compression。

對 graph minors，finite graphs 在 minor relation 下 WQO，而 minor-closed graph class 的 complement 為 upward closed，因此得到 finite forbidden minors。

我們希望把同樣結構搬到演算法空間：

$$
\mathcal A_P
=
\text{某個 P-normal-form algorithm space}.
$$

理想上想找到：

$$
A\preceq B
$$

使：

1. $(\mathcal A_P,\preceq)$ 為 WQO；
2. 「不能正確解 SAT」或其他 hardness property 對 $\preceq$ 單調；
3. order 可獨立定義；
4. order 不把 SAT correctness 本身偷藏進去；
5. order 與 polynomial-resource 結構有真實關聯。

這一輪就是測這五件事是否能同時成立。

---

# 二、候選一：程式文字 subsequence order

把一個 normalized program 編成有限 alphabet 上的字串：

$$
w(A)\in\Sigma^*.
$$

定義：

$$
A\preceq_{\mathrm{sub}}B
$$

當且僅當：

$$
w(A)
$$

是：

$$
w(B)
$$

的 subsequence。

若 alphabet $\Sigma$ 有限，Higman lemma 告訴我們：

$$
\boxed{
(\Sigma^*,\preceq_{\mathrm{sub}})
\text{ 為 WQO}.
}
$$

所以：

$$
\text{WQO requirement}
$$

真的可以非常便宜地得到。

## 2.1 問題：semantic monotonicity 幾乎完全不存在

假設程序 A 的文字是 B 的 subsequence。

這個事實幾乎沒有約束：

$$
\llbracket A\rrbracket
$$

與：

$$
\llbracket B\rrbracket
$$

的輸入輸出語義。

只插入一個：

```text
if trigger(x): return 1
```

就可能完全改掉行為，卻保留原程式的所有 tokens 作為 subsequence。

因此可同時存在：

$$
A\preceq_{\mathrm{sub}}B,
$$

但：

$$
A\text{ 正確},\quad B\text{ 錯誤}.
$$

反過來，也可在錯誤程序外加入 correction layer，使：

$$
A\text{ 錯誤},\quad B\text{ 正確}.
$$

所以 SAT correctness 並非 upward/downward closed。

### 本候選裁定

$$
\boxed{
\text{WQO：強}
}
$$

$$
\boxed{
\text{Semantic alignment：幾乎為零}
}
$$

---

# 三、候選二：AST homeomorphic embedding

比文字 subsequence 更合理的做法，是把程式／P-normal-form term 表示成抽象語法樹：

$$
T(A).
$$

定義 homeomorphic embedding：

$$
A\preceq_{\mathrm{HE}}B
$$

若 $T(A)$ 可透過刪除某些節點／路徑壓縮等方式嵌入 $T(B)$。

Kruskal tree theorem 告訴我們：

> 對 WQO labels 的有限樹，homeomorphic embedding 形成 WQO。

因此在固定／WQO signature 的 normalization 下：

$$
\boxed{
\text{P-normal-form derivation trees 可以取得真正的 WQO。}
}
$$

這不是紙上幻想。homeomorphic embedding 已實際用於：

- supercompilation；
- partial evaluation；
- program specialization；
- symbolic transformation；
- term rewriting / symbolic execution；

作為 termination whistle：若新展開 term 已嵌入先前 term，便停止繼續無限制 unfold。

## 3.1 這是第一個正面發現

我們先前擔心：

> 「P-normal-form algorithms 的空間太巨大，可能連 WQO 都做不到。」

本輪修正：

$$
\boxed{
\text{syntax tree space 本身完全可能 WQO。}
}
$$

因此 Graph-Minor 路線真正卡住的位置不是：

$$
\text{Order existence}.
$$

而是：

$$
\boxed{
\text{Order--Semantics alignment}.
}
$$

---

# 四、語法 WQO 為什麼沒有自動帶來 SAT finite obstruction

Graph-minor miracle 需要兩件事同時成立：

$$
\text{WQO}
+
\text{property closure}.
$$

只有第一件不夠。

令：

$$
\mathsf{Good}_{SAT}
=
\{A:\forall x,\ A(x)=SAT(x)\}.
$$

若想得到 forbidden-algorithm basis，至少需要：

$$
A\preceq B
$$

時，good/bad status 有固定單調方向。

但對 syntax embedding：

$$
A\preceq_{\mathrm{HE}}B
$$

只代表：

$$
\text{A 的某個語法形狀出現在 B 中}.
$$

它沒有推出：

$$
\llbracket A\rrbracket
\preceq_{\mathrm{sem}}
\llbracket B\rrbracket.
$$

更沒有推出 SAT correctness。

因此：

$$
\mathsf{Good}_{SAT}
$$

通常不是：

$$
\preceq_{\mathrm{HE}}
$$

下的 upward-closed 或 downward-closed set。

所以 finite basis theorem 沒有觸發。

---

# 五、WSTS 提供了精準對照：WQO 不是全部

Well-Structured Transition Systems（WSTS）提供了一個極度貼切的成熟樣板。

它們能利用 WQO 做 coverability 等 decidability，並不是因為「有 WQO 就行」。

還需要 transition relation 與 order 之間的 monotonicity／compatibility。

抽象地：

$$
x\preceq y
$$

且：

$$
x\to x'
$$

時，希望存在：

$$
y\to^* y'
$$

滿足：

$$
x'\preceq y'.
$$

因此：

$$oxed{
\text{WQO}
+
\text{monotone dynamics}
}
$$

才是可用結構。

這與本輪結論高度一致：

$$oxed{
\text{Algorithm syntax WQO}
+
\text{SAT semantic non-monotonicity}
\Rightarrow
\text{finite obstruction machinery 不工作。}
}
$$

---

# 六、候選三：語義等價 order

既然 syntax order 不懂語義，等號隊提出：

> 那就直接用 semantics。

最極端定義：

$$
A\preceq_{= }B
\iff
\llbracket A\rrbracket
=
\llbracket B\rrbracket.
$$

這時 correctness 當然完全保存。

如果：

$$
A\text{ solves SAT}
$$

且：

$$
A\preceq_=B,
$$

則：

$$
B\text{ solves SAT}.
$$

很好。

問題是這根本沒有 Graph-Minor 所需的 WQO 結構。

每個不同的 Boolean function 都形成不同 equivalence class。

在 equality quasi-order 下，任取無限多個語義不同函數：

$$
f_1,f_2,f_3,\ldots
$$

便形成 infinite antichain。

因此：

$$
\boxed{
\text{Semantic equality gives perfect monotonicity but fails WQO.}
}
$$

這是本輪第一個非常乾淨的 trade-off。

---

# 七、候選四：語言包含 order

定義 decision algorithms 的 accepted languages：

$$
L(A)=\{x:A(x)=1\}.
$$

令：

$$
A\preceq_{\subseteq}B
\iff
L(A)\subseteq L(B).
$$

這個 order 是純語義的，而且「acceptance coverage」具有自然 monotonicity。

但它也不是 WQO。

令：

$$
L_n=\{0^n\}.
$$

則：

$$
L_i\not\subseteq L_j,
\qquad
L_j\not\subseteq L_i
$$

對所有：

$$
i\neq j.
$$

因此：

$$
L_1,L_2,L_3,\ldots
$$

形成 infinite antichain。

所以：

$$
\boxed{
\text{簡單 semantic orders 也很容易失去 WQO。}
}
$$

---

# 八、候選五：Polynomial Simulation Order

接著嘗試：

$$
A\preceq_{\mathrm{sim}} B
$$

表示 B 可以用 polynomial overhead 精確模擬 A。

直覺上，如果 A 已經能解 SAT，而 B 可以有效模擬 A，那 B 也能解 SAT。

所以 correctness 看似 upward monotone。

但這裡有三個版本陷阱。

## 8.1 若 simulation 定義太寬

如果 B 是 universal interpreter，可模擬任意 A，則大量 algorithms 都有共同上界。

order 變得太 coarse。

但：

$$
\text{有共同上界}
\neq
\text{bad set 有 finite minimal basis}.
$$

而且「B 模擬 A」不代表 B 本身的 default decision function 與 A 相同；必須把 A 的 code 當額外參數，這已改變 problem interface。

## 8.2 若 simulation 要求 same input / same output

若要求：

$$
\forall x,
\quad
B(x)=A(x),
$$

再附帶 polynomial overhead，這已接近 semantic equivalence + runtime relation。

此時 correctness 保存，但：

- wqo 不自動成立；
- exact semantic equality 對一般程式不可判定；
- 在受限 grammar 中仍可能形成大量不可比 equivalence classes；
- resource relation 可能高度 representation-dependent。

## 8.3 若 order 直接寫入「可 polynomial reduction」

那很容易把 complexity classification 偷進 relation。

例如若：

$$
A\preceq B
$$

的意思是「A 的問題可 polynomial-time reduction 到 B 的問題」，那我們其實已經移到 complexity-degree order。

這可以是合法數學對象，但它不再是 Graph-Minor 式的 primitive structural relation；而 SAT 的 NP-completeness 本身已經讓大量 NP problems 落在同一 hardness degree。

因此 finite obstruction dream 並沒有自動獲得新 leverage。

---

# 九、候選六：Polynomial Compiler / Quotient Reachability

沿用第六到十三輪的 representation-transform 路線，定義：

$$
A\preceq_{\mathrm{comp}} B
$$

若存在 uniform polynomial-time compiler / quotient transform：

$$
\tau:A\mapsto B
$$

且 exact semantics preserved。

這個 order 比 syntax embedding 更接近我們想要的「algorithmic minor」。

但又出現第六輪的閉包悖論新版。

若 semantics-preserving compiler 很強，且可以任意改寫所有等價 P programs，則：

$$
A\preceq B
$$

大量退化成：

$$
\llbracket A\rrbracket=\llbracket B\rrbracket.
$$

如此又回到 semantic equivalence antichain。

若 compiler class 限制很窄，則可能有 WQO / finite basis，但只能證明受限 compiler architecture 的結果。

因此：

$$
\boxed{
\text{Compiler order 太廣}\Rightarrow\text{semantic collapse},
}
$$

$$
\boxed{
\text{Compiler order 太窄}\Rightarrow\text{restricted-model result}.
}
$$

這是第六輪 closure paradox 在 WQO 場景的重現。

---

# 十、本輪核心：WQO--Semantic Alignment Barrier

綜合六種候選，本輪提出：

$$
\boxed{
\mathrm{WSAB}
=
\text{WQO--Semantic Alignment Barrier}
}
$$

要把 finite obstruction theory 真正搬進 P/NP，order 必須同時滿足：

### 1. WQO

不存在 infinite descending chain / antichain。

### 2. Semantic Monotonicity

與 SAT correctness / failure / hardness 相關的 property 必須對 order 關閉。

### 3. Effectiveness

至少需要足夠有效地使用 order；否則 finite basis 存在也可能無法轉成證明／算法。

### 4. Non-circularity

order 定義不能直接引用：

$$
\text{是否能 polynomial-time solve SAT}.
$$

### 5. Resource Relevance

order 不能只保存 extensional semantics，還需對：

$$
T(n),M(n),L_{repr},C_{compile}
$$

等傳統 complexity resource 有可證明關係。

自然候選目前反覆發生：

$$
\text{有 WQO}
\Rightarrow
\text{語義失焦},
$$

或：

$$
\text{有語義單調性}
\Rightarrow
\text{失去 WQO / effectiveness},
$$

或：

$$
\text{有 WQO + 語義}
\Rightarrow
\text{order 定義開始循環／過度受限}.
$$

---

# 十一、Order Alignment Trilemma

本輪將 WSAB 操作化成三難：

$$
\boxed{
\mathrm{OAT}
=
\text{Order Alignment Trilemma}
}
$$

三個角：

## A. Structural / Effective WQO

例如：

- subsequence；
- tree embedding；
- minor-like contraction。

優點：

$$
\text{數學乾淨、finite-basis machinery 可用}.
$$

缺點：

$$
\text{通常不懂 solver semantics}.
$$

## B. Semantic Monotone Order

例如：

- semantic equality；
- language inclusion；
- exact simulation。

優點：

$$
\text{correctness / behavior 對齊}.
$$

缺點：

$$
\text{常有 infinite antichain、不可判定或過於粗糙}.
$$

## C. Complexity-Relevant Order

例如：

- polynomial simulation；
- resource-aware compiler reachability；
- reduction degree。

優點：

$$
\text{直接碰 complexity}.
$$

缺點：

$$
\text{最容易 circular、representation dependent 或退化成已知 complexity relation}.
$$

真正的新 order 必須設法在三者中央找到非空區域。

---

# 十二、Bellantoni–Cook Grammar 與 Kruskal 的真正接合

這輪有一個值得保留的正面連接。

第十五輪已有：

$$
\operatorname{Denote}(\mathcal G_P)=FP.
$$

將每個：

$$
t\in\mathcal G_P
$$

視為有限 derivation tree。

若 normalization 後使用有限／WQO label set，Kruskal 類定理使：

$$
(\mathcal G_P,\preceq_{HE})
$$

在 syntax-tree embedding 下具有 WQO 結構。

所以我們其實已同時擁有：

$$
\boxed{
\text{Complete P Grammar}
+
\text{Syntactic WQO}
}
$$

缺少的是：

$$
\boxed{
\text{一個被 tree embedding 保存、又能排除 SAT 的 semantic invariant}.
}
$$

這把第二十二輪的問題收斂成：

> 不需要再問「P algorithm space 能不能 WQO」；至少 syntax-space 可以。真正要問的是「有沒有 semantic abstraction $\alpha(t)$，使 homeomorphic embedding 在 abstraction 上誘導 monotone order，而且 $\alpha$ 足以區分 SAT」。

這直接生成下一輪。

---

# 十三、等號隊的反擊：WQO 只是一種 termination 工具，不應被神化

等號隊指出一個很合理的事情：

supercompilation 使用 homeomorphic embedding 的典型目的，是防止 transformation 無限展開。

也就是：

$$
\boxed{
\text{WQO 很擅長控制探索／展開軌跡，}
}
$$

但不代表：

$$
\boxed{
\text{WQO 自然攜帶問題的 semantic hardness。}
}
$$

因此它認為不等號隊一直想：

$$
\text{WQO}
\Rightarrow
\text{finite SAT obstruction}
$$

本身就是過度樂觀。

等號隊的新主張：

> WQO 應當用來確保 adaptive quotient / bridge / supercompilation trajectory 不無限重複，而真正求解 SAT 的能力仍應由代數、編譯、學習與 representation revolution 提供。

換句話說，把 WQO 降級成：

$$
\boxed{
\text{Search/Transformation Termination Layer}
}
$$

而不是 hardness invariant。

這其實是一個很強的修正。

---

# 十四、不等號隊的反擊：那就對 abstraction 做 WQO

不等號隊不放棄 finite basis，但承認 syntax order 太淺。

它改提：

$$
\alpha:A\mapsto\mathcal S(A),
$$

其中：

$$
\mathcal S(A)
$$

不是完整語義，而是某種有限／抽象 solver semantics，例如：

- 可保存的 summary state；
- residual relation family；
- accepted quotient operations；
- proof-system strength profile；
- bridge-language profile；
- resource transition signature。

再在 abstraction space 定義：

$$
\mathcal S(A)\preceq_\alpha\mathcal S(B).
$$

要求：

1. abstraction space 為 WQO；
2. exact SAT correctness 對 abstraction order 有 sound monotonicity；
3. abstraction 可有效算／有效證明；
4. abstraction 不直接包含完整 truth table；
5. abstraction 不直接定義為「最佳 solver complexity」。

這就是下一輪的：

$$
\boxed{
\text{Semantic Monotonicity Engineering}.
}
$$

---

# 十五、一個重要新區分：Termination WQO vs Hardness WQO

本輪正式區分兩種完全不同用途。

## 15.1 Termination WQO

目的：

$$
\text{避免 transformation / exploration 無限產生互不包含狀態}.
$$

例如 homeomorphic embedding in supercompilation。

它只需對：

$$
\text{程序形狀／狀態}
$$

提供 well-founded-like control。

## 15.2 Hardness WQO

目的：

$$
\text{讓 solver correctness/failure 的集合成為 monotone set，進而有 finite basis}.
$$

這需要：

$$
\text{order}
$$

真正對齊：

$$
\text{semantic capability}.
$$

因此：

$$
\boxed{
\text{Termination WQO exists}
\not\Rightarrow
\text{Hardness WQO exists}.
}
$$

這是本輪目前最重要的防誤用定理式觀察。

---

# 十六、有限禁阻集的真正必要條件

若要得到 Graph-Minor 式結論：

$$
A\text{ bad}
\iff
\exists j\le m:\ B_j\preceq A,
$$

至少需要：

$$
\mathsf{Bad}
$$

是 upward closed。

WQO 只能保證：

$$
\mathsf{Bad}
\text{ 若 upward closed，則有 finite minimal basis}.
$$

它不能替我們證明：

$$
\mathsf{Bad}\text{ upward closed}.
$$

因此 finite obstruction route 的真正 proof obligation 是：

$$
\boxed{
\text{Find an order where semantic badness is monotone.}
}
$$

而不是：

$$
\boxed{
\text{Find any WQO on program encodings.}
}
$$

這把第二十二輪的一個模糊希望完全精確化。

---

# 十七、與前二十二輪的連接

本輪不是獨立岔路，而是把多條舊線匯合。

## 與第二輪 Residual Distinguishability

當時嘗試找跨表示 invariant。

現在問題變成：

$$
\text{Residual abstraction 能否形成 WQO 且 semantic monotone？}
$$

## 與第六輪 Polynomial Representation Closure

當時發現 order/closure 太寬會 tautological，太窄只得 restricted lower bound。

現在同樣出現：

$$
\text{Semantic order 太寬}
\rightarrow
\text{equivalence/circularity},
$$

$$
\text{syntactic order 太窄}
\rightarrow
\text{semantic misalignment}.
$$

## 與第八～十三輪 Quotient / Bridge

WQO 可以自然用於：

$$
\text{防止 quotient / bridge transformation 無限重複}.
$$

因此即使 Hardness WQO 失敗，Termination WQO 仍可作為等號隊工程工具。

## 與第十五輪 Grammar Invariant Program

完整 P grammar 已存在；syntax trees 也可 WQO。

所以真正剩下：

$$
\boxed{
\text{semantic abstraction + monotone lift theorem}.
}
$$

## 與第二十二輪 QCM

finite-basis QCM 的核心條件現在被改寫為：

$$
\boxed{
\text{WQO + semantic closure + lift theorem}.
}
$$

---

# 十八、本輪淘汰的錯誤路線

以下論證不得使用：

1. 「程式 AST 在 Kruskal embedding 下 WQO，所以 SAT solver failure 有 finite basis。」
2. 「WQO 沒有 infinite antichain，所以所有 semantic properties 都有 finite obstruction。」
3. 「homeomorphic embedding 能保證 supercompilation termination，所以它能刻畫 P/NP hardness。」
4. 「把 order 改成 semantic equivalence，就同時得到 correctness monotonicity 與 WQO。」
5. 「有 universal simulator，所以 simulation order 自動是一個有用的 hardness WQO。」
6. 「compiler reachability order 若保存 semantics，就一定提供 finite basis。」
7. 「finite basis existence 等於 basis 可有效算出。」
8. 「只要把 SAT correctness 塞進 order definition，然後證明 monotonicity，就得到非循環結果。」

---

# 十九、本輪正式成果

## 19.1 Syntactic WQO Availability

Higman/Kruskal 類結果表明：

$$
\boxed{
\text{algorithm syntax / derivation trees 可以自然取得 WQO。}
}
$$

## 19.2 Semantic Monotonicity Gap

自然 syntactic embeddings 不保存 SAT correctness/failure。

$$
\boxed{
\text{WQO alone is insufficient.}
}
$$

## 19.3 WQO--Semantic Alignment Barrier（WSAB）

真正困難是同時取得：

$$
\text{WQO}
+
\text{semantic monotonicity}
+
\text{effectiveness}
+
\text{non-circularity}
+
\text{resource relevance}.
$$

## 19.4 Order Alignment Trilemma（OAT）

結構 order、語義 order、complexity-relevant order 各有不同缺陷。

## 19.5 Termination WQO / Hardness WQO 分離

$$
\boxed{
\text{能保證 transformation 終止的 WQO，未必能支撐 hardness finite basis。}
}
$$

## 19.6 P-normal-form + Kruskal 接口

Bellantoni–Cook/Cobham 類完整 P grammar 的 derivation trees 可以成為下一輪 abstraction-order engineering 的母空間。

---

# 二十、雙方戰果

## $P=NP$ 隊

獲得一個重要防禦：

> 即使所有 P-normal-form programs 的 syntax trees 都 WQO，也完全不限制 unknown representation revolution，因為 syntax embedding 不控制 semantics。

並把 WQO 降級為 transformation termination 工具，反而讓 adaptive portfolio 更合理。

### 新技能

$$
\boxed{
\mathrm{TWU}
=
\text{Termination-WQO Utilization}
}
$$

---

## $P\neq NP$ 隊

成功把 finite-obstruction route 的真正義務收斂為：

$$
\boxed{
\text{Semantic Monotone Abstraction Order}
}
$$

不再浪費時間尋找「任何 WQO」。

### 新技能

$$
\boxed{
\mathrm{WSAB}
=
\text{WQO--Semantic Alignment Barrier}
}
$$

---

# 二十一、本輪比分

$$
P=NP:22
$$

$$
P\neq NP:22
$$

……嗯。

現在已經不是控分問題了。

我們可能真的證明了一個新的非正式定律：

$$
\boxed{
\text{每當不等號隊得到一個有限化工具，等號隊就得到一個 representation escape；}
}
$$

$$
\boxed{
\text{每當等號隊得到一個新 representation，另一隊就要求一個 lift theorem。}
}
$$

比分只負責把這件事畫出來。（歪臉笑）

比分不具有任何數學證明意義。

---

# 二十二、第二十四輪入口：Semantic Monotonicity Engineering

下一輪不再找普通 WQO，而直接設計 abstraction：

$$
\alpha:A\mapsto S_A.
$$

目標是找：

$$
S_A\preceq S_B
$$

同時滿足：

1. $(S,\preceq)$ 為 WQO；
2. SAT correctness / failure 有 sound monotonicity；
3. $\alpha$ 不等於完整 truth table；
4. $\alpha$ 可有效構造或至少有 finite proof；
5. order 與 polynomial runtime 有可證明關係；
6. 不直接把「是否 solve SAT」寫入 abstraction。

候選來源：

- abstract interpretation；
- well-structured transition systems；
- behavioral simulation；
- residual-state quotients；
- proof-system simulation profiles；
- algebraic closure signatures；
- resource-aware semantics。

核心問題：

$$
\boxed{
\text{能否把 solver semantics 壓縮成一個仍 WQO 的 abstraction，而不丟掉區分 SAT 的能力？}
}
$$

如果能，finite-basis 路線重新活過來。

如果不能，則我們可能逐步得到一個新的更一般性結論：**語義辨識能力與 WQO 壓縮能力之間存在不可兼得張力。**

---

# 二十三、外部理論參照

1. **Higman's Lemma**
   - 有限 alphabet 的有限 words 在 subsequence relation 下為 WQO。
   - 本輪作為「program text WQO 很容易取得」的基礎樣板。

2. **Kruskal's Tree Theorem**
   - 有限、WQO-labelled trees 在 homeomorphic embedding 下為 WQO。
   - 本輪用於 P-normal-form derivation trees / AST。

3. Michael Leuschel, **Homeomorphic Embedding for Online Termination of Symbolic Methods**（2002）
   - homeomorphic embedding 長期用於 program analysis、specialisation、transformation、verification 的 termination control。

4. Torben Æ. Mogensen, **A Comparison of Well-Quasi Orders on Trees**（2013）
   - 討論多種用於 supercompilation/program transformation 的 tree WQO。

5. Alain Finkel 等 Well-Structured Transition Systems 文獻
   - WQO 需要搭配 transition monotonicity 才產生 coverability/verification 的演算法效益。

6. Robertson–Seymour Graph Minor Theorem
   - finite graphs 在 minor relation 下 WQO；minor-closed properties 因而具有 finite forbidden-minor basis。
   - 本輪主要作為「WQO + property closure」缺一不可的對照。

---

## 本輪裁定

第二十三輪沒有發現「演算法空間不存在 WQO」。

恰恰相反：

$$
\boxed{
\text{WQO 很多，甚至已經在實際程式轉換技術中使用。}
}
$$

真正的困難被精確移到：

$$
\boxed{
\text{哪一個 WQO 能與 SAT semantic capability 單調對齊？}
}
$$

Graph-Minor 路線真正需要的不是：

$$
\text{一個漂亮的 order},
$$

而是：

$$
\boxed{
\text{一個漂亮的 order + 一個不循環的 semantic lift theorem。}
}
$$

因此下一輪將從「找 order」升級為「工程化 semantic abstraction」。
