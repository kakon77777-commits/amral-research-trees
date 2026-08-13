# P/NP 辯論遊戲研究區｜第十二輪

## 介面語言格、Schaefer 臨界與遞迴 SAT：Bridge Language Hierarchy 的正式化

**Round 12: Bridge-Language Lattices, the Schaefer Frontier, and Recursive SAT**

- **主導研究者：** Neo.K（許筌崴）
- **協作整理：** Aletheia
- **機構：** EveMissLab（一言諾科技有限公司）
- **日期：** 2026 年 8 月 1 日
- **版本：** v1.0
- **研究狀態：** 第十二輪雙假設預演
- **前置文件：** `11_第十一輪_共同保存結構崩塌與動態橋接.md`
- **遊戲態度：** 等號隊與不等號隊互相拆台
- **文件標準：** 文件內容保持正式；比分與吐槽只是互動介面

---

## 摘要

第十一輪將異質局部求解器的協作形式化為 Boundary Extension Relation（BER）：每個局部模組先消去私有變數，只保留可延伸的邊界關係，然後由 bridge 再次協調這些關係。這導出「存在量詞再現」：局部存在量詞雖被消去，全域存在性問題仍可能在共享邊界上重新生成。

本輪進一步研究 bridge 本身的**表達語言**。原先直覺上的「Bridge Language Hierarchy」若被理解成一條線性的強弱階梯並不精確；Horn、bijunctive（2-SAT）、affine（XOR）等 tractable Boolean constraint languages 並不存在天然的單一線序。更合適的數學對象，是由 primitive-positive definability（pp-definability）誘導的**偏序／co-clone 格**。

令 $\Gamma_B$ 為 bridge 可以使用的固定有限 Boolean 關係語言。若 bridge coordination 恰可表示為 $\operatorname{CSP}(\Gamma_B)$，則 Schaefer dichotomy 給出一個嚴格而重要的受限分類：若 $\Gamma_B$ 全部落在某一個 Schaefer tractable 家族中，則 coordination 屬於 $P$；否則為 NP-complete。此處的 NP-complete 不等於無條件證明「不在 $P$」，因此本輪仍不宣稱完成 $P\neq NP$。

本輪得到三個主要新結果。第一，**bridge 的臨界不是單純表達力大小，而是其 pp-closure 是否離開所有 tractable co-clone**。第二，Dynamic Bridge Portfolio 若允許任意混合多個個別 tractable 語言，真正需要檢查的是它們的聯合語言 $\bigcup_i\Gamma_i$；個別都在 $P$ 不保證聯合仍在 $P$。第三，局部求解—邊界投影—再協調形成一種「遞迴 SAT」：若每層投影後產生的 bridge language 重新具備一般 SAT 的表達能力，則存在量詞沒有消失，只是向上搬運。

本輪因此將下一個核心問題推進為：是否存在一種**多項式穩定的橋接閉包**，使 Dynamic Algebra Switching 在反覆投影、pp-definition 與組合之後，始終停留於 tractable 區域？若不能，造成語言漂移（language drift）的最小結構是什麼？

---

# 一、上輪遺留問題：Bridge 到底能說多少話？

第十一輪把全域公式分解為：

$$
F=\bigwedge_{i=1}^{m}F_i(B_i,Y_i),
$$

其中 $Y_i$ 是局部私有變數，$B_i$ 是共享邊界變數。

局部模組投影為：

$$
\mathcal E_i(B_i)
=
\{b_i:\exists Y_i\,F_i(b_i,Y_i)\}.
$$

全域可滿足性變成：

$$
\exists B\;\bigwedge_i[B_i\in\mathcal E_i].
$$

於是局部 solver 是否快速，不再是唯一問題。真正需要協調的是：

$$
\mathcal E_1,\ldots,\mathcal E_m
$$

在共享邊界 $B$ 上是否存在共同賦值。

第十一輪稱此現象為：

$$
\boxed{\text{Existential Reappearance／存在量詞再現}}
$$

本輪追問：

> 如果 bridge 只能使用 equality，可能很容易；如果 bridge 可以使用 XOR、Horn、2-SAT，仍有成熟的多項式演算法；如果 bridge 再變強，什麼時候 coordination 本身重新擁有一般 SAT 的表達能力？

---

# 二、先修正名稱：「階層」其實更像一個格

若把 bridge language 寫成：

$$
\Gamma=
\{R_1,\ldots,R_k\},
$$

其中每個 $R_i$ 都是有限 arity 的 Boolean relation，則兩個語言之間未必能用單一「強／弱」比較。

例如：

- Horn relations 由 conjunction 型 closure 支配；
- dual-Horn relations 對應 disjunction 型 closure；
- bijunctive relations 對應 majority 型 closure；
- affine relations 對應 parity／minority 型 closure。

它們是不同 tractable islands，而非一條：

$$
\text{Equality}<\text{2-SAT}<\text{Horn}<\text{XOR}<\cdots
$$

的自然線序。

因此，本輪把 Bridge Language Hierarchy 修正為：

$$
\boxed{\text{Bridge Language Poset／Bridge Co-clone Lattice}}
$$

---

# 三、pp-definability：Bridge 語言的真正「可表達」關係

## 3.1 Primitive-positive definition

一個 relation $R(\mathbf x)$ 若能由語言 $\Gamma$ 透過：

- conjunction；
- existential quantification；
- variable identification；
- equality；

寫成：

$$
R(\mathbf x)
\iff
\exists \mathbf y\;
\bigwedge_j
R_j(\mathbf z_j),
\qquad
R_j\in\Gamma,
$$

則稱 $R$ 可由 $\Gamma$ primitive-positively 定義。

記所有可 pp-define 的 relations 為：

$$
\langle\Gamma\rangle_{pp}.
$$

這個 closure 非常適合本系列，因為它的形式正好就是：

$$
\text{局部 constraints}
+
\text{私有輔助變數}
+
\text{存在量詞消去}
\rightarrow
\text{新的 boundary relation}.
$$

也就是說，pp-definition 本身就是一種正式的「局部模組黏成 bridge relation」語言。

## 3.2 Bridge 表達偏序

定義：

$$
\Gamma_1\preceq_{pp}\Gamma_2
$$

若：

$$
\Gamma_1\subseteq
\langle\Gamma_2\rangle_{pp}.
$$

直覺上：$\Gamma_2$ 的 bridge 能用 polynomial-size gadget 模擬 $\Gamma_1$ 的所有基本關係。

因此 bridge 的能力不是看表面 relation 個數，而要看其 closure：

$$
\boxed{
\text{真正 bridge capability}
=
\langle\Gamma_B\rangle_{pp}
}
$$

---

# 四、正式工具：Schaefer Bridge Dichotomy

考慮固定有限 Boolean bridge language $\Gamma_B$，並假設全域 coordination 問題正是：

$$
\operatorname{SAT}(\Gamma_B)
$$

或等價的 Boolean $\operatorname{CSP}(\Gamma_B)$。

Schaefer 的 generalized satisfiability dichotomy 告訴我們：對固定 Boolean constraint language，satisfiability either polynomial-time decidable or NP-complete；tractable cases 由若干特殊 relation families 構成。

在標準版本下，若整個 $\Gamma_B$ 同時屬於以下至少一類：

1. $0$-valid；
2. $1$-valid；
3. Horn；
4. dual-Horn；
5. bijunctive；
6. affine；

則 $\operatorname{SAT}(\Gamma_B)\in P$；否則為 NP-complete。

因此，在本系列的受限 bridge coordination 模型內，可以得到：

## 命題 4.1｜Bridge-Schaefer 分類

若所有局部模組已被多項式時間投影成固定 Boolean relation language $\Gamma_B$，且剩餘全域工作完全是 $\operatorname{SAT}(\Gamma_B)$，則：

$$
\Gamma_B\text{ 落在 Schaefer tractable family}
\Rightarrow
\text{bridge coordination}\in P,
$$

否則：

$$
\text{bridge coordination is NP-complete}.
$$

這是一個真正在既有定理上成立的**受限分類結果**。

但必須立刻加上紅字級警告：

$$
\boxed{
\text{NP-complete}
\not\Rightarrow
\text{已證明不在 }P
}
$$

否則就把 $P\neq NP$ 偷塞進前提。

---

# 五、不等號隊出牌：Bridge Expressivity Frontier

不等號隊重新定義「臨界點」。

它不是一個單一數值：

$$
\lambda_B=0,1,2,3,\ldots
$$

而是 bridge language 在 pp-co-clone 格中的位置。

定義暫定：

$$
\operatorname{BEF}(\Gamma)
=
\text{Bridge Expressivity Frontier status of }\langle\Gamma\rangle_{pp}.
$$

若 $\Gamma$ 保持在某個 tractable co-clone 中：

$$
\operatorname{BEF}(\Gamma)=\text{tractable-side}.
$$

若 $\Gamma$ 的 closure 離開所有 Schaefer tractable classes：

$$
\operatorname{BEF}(\Gamma)=\text{NP-complete-side}.
$$

不等號隊的遊戲主張變成：

> 任意足以精確承載一般 SAT 邊界語義的 bridge portfolio，其聯合 pp-closure 最終會越過 tractable frontier。

目前這只是方向，不是一般定理。

---

# 六、等號隊反擊：NP-complete-side 仍不是封鎖線

等號隊立刻指出兩個問題。

## 6.1 第一個問題：你只是重新得到 NP-completeness

如果：

$$
\operatorname{SAT}(\Gamma_B)
$$

是 NP-complete，那麼這只說：

$$
SAT\leq_p SAT(\Gamma_B),
$$

與：

$$
SAT(\Gamma_B)\leq_p SAT.
$$

它並沒有證明：

$$
SAT(\Gamma_B)\notin P.
$$

所以 BEF 很適合分類 bridge 的「已知結構難度」，卻不是最終 $P\neq NP$ 下界。

## 6.2 第二個問題：演算法不一定使用固定 constraint language

一般 SAT 演算法可以：

- 動態改寫 constraint；
- 建立新輔助 relation；
- 切換 algebra；
- 進入非-CSP 表示；
- 使用 spectral、linear-algebraic、proof-search、compilation 等不同空間。

所以就算某個固定 $\Gamma_B$ 在 NP-complete side，等號隊仍可說：

> 我不在這個 bridge language 裡解。

這是第六輪「表示逃逸」與第十一輪「dynamic bridging」的回歸。

---

# 七、Dynamic Bridge Portfolio 的正式化

令等號隊擁有一組 bridge languages：

$$
\mathfrak B
=
\{\Gamma_1,\Gamma_2,\ldots,\Gamma_r\},
$$

其中每個：

$$
\operatorname{SAT}(\Gamma_i)\in P.
$$

表面上看，每一把武器都安全。

但如果全域 coordination 可以任意混合來自不同 $\Gamma_i$ 的 constraints，實際語言是：

$$
\Gamma_{\cup}
=
\bigcup_{i=1}^{r}\Gamma_i.
$$

因此真正應檢查的是：

$$
\left\langle
\bigcup_i\Gamma_i
\right\rangle_{pp}.
$$

而不是分別檢查每個 $\Gamma_i$。

## 命題 7.1｜Portfolio Union Principle

若 Dynamic Bridge Portfolio 允許在同一共享變數集合上任意 conjunction 地使用所有 $\Gamma_i$ constraints，則其 general coordination capability 至少等價於：

$$
\operatorname{SAT}
\left(
\bigcup_i\Gamma_i
\right).
$$

因此：

$$
\forall i,
\operatorname{SAT}(\Gamma_i)\in P
$$

並不能推出：

$$
\operatorname{SAT}
\left(
\bigcup_i\Gamma_i
\right)
\in P.
$$

這就是本輪最重要的 bridge composition 警告。

---

# 八、最乾淨的思維實驗：兩個「自己必勝」的語言黏出硬問題

令：

$$
R_+(x,y,z)=x\lor y\lor z,
$$

與：

$$
R_-(x,y,z)=\neg x\lor\neg y\lor\neg z.
$$

若公式只使用 $R_+$，全設為：

$$
x_i=1
$$

即可滿足。

所以其 satisfiability 是 trivial。

若公式只使用 $R_-$，全設為：

$$
x_i=0
$$

即可滿足。

所以也 trivial。

然而允許兩者混合後，得到 monotone 3-SAT 型 coordination：每個 clause 全正或全負，但全域需要同時協調兩種方向；此類 generalized satisfiability 落到 Schaefer dichotomy 的 NP-complete 側。

這給出極乾淨的例子：

$$
\boxed{
P\text{-local language}
+
P\text{-local language}
\not\Rightarrow
P\text{-union language}
}
$$

再次說明第十輪的 Heterogeneous Gluing Debt 不是修辭，而有正式 constraint-language 模型可對應。

---

# 九、Polymorphism Intersection 再次出現，但位置更精確

對 constraint language $\Gamma$，令：

$$
\operatorname{Pol}(\Gamma)
$$

表示保存所有 relations 的 polymorphisms。

若：

$$
\Gamma=\Gamma_1\cup\Gamma_2,
$$

則：

$$
\operatorname{Pol}(\Gamma)
=
\operatorname{Pol}(\Gamma_1)
\cap
\operatorname{Pol}(\Gamma_2).
$$

所以不同 tractable islands 混合時，共同 polymorphism 會做交集。

第十輪提出的：

$$
\operatorname{PIS}(\Gamma_1,\ldots,\Gamma_m)
$$

因此可以重新理解為：

$$
\operatorname{PIS}
\sim
\operatorname{Pol}(\Gamma_1)
\cap\cdots\cap
\operatorname{Pol}(\Gamma_m).
$$

若交集仍保留某個足以支撐 tractability 的操作，bridge 可能仍在 P-side；若共同保存結構全部崩塌，則在 Boolean fixed-language CSP 中會跨到 Schaefer NP-complete side。

這是一個比「語言越多所以越難」更精確的結構機制。

---

# 十、與 Post/co-clone 格的連接

Boolean co-clone theory 提供了本輪非常適合的數學地圖。

一個 co-clone 是對自然 relational closure operations（包括 pp-definition）封閉的 Boolean relation 類。不同 bases 可以生成同一 co-clone，因此：

$$
\text{不同表面 relation sets}
$$

可能其實具有：

$$
\text{同一 expressive closure}.
$$

所以「bridge language」真正該記錄的不是原始 syntax，而是：

$$
\boxed{
[\Gamma]_{pp}
=
\langle\Gamma\rangle_{pp}
}
$$

這也讓第五輪的 Representation Escape Profile 得到一個更正式的局部版本：在 Boolean CSP 世界中，許多表面表示其實可以被 co-clone quotient 商掉。

---

# 十一、遞迴 SAT：存在量詞如何一層一層搬家

現在考慮多層分解。

第 $0$ 層：

$$
F^{(0)}=F.
$$

將其分成局部模組：

$$
F^{(k)}
=
\bigwedge_i
F_i^{(k)}(B_i^{(k)},Y_i^{(k)}).
$$

局部消去：

$$
\mathcal E_i^{(k)}
=
\exists Y_i^{(k)}F_i^{(k)}.
$$

再形成下一層 coordination instance：

$$
F^{(k+1)}
=
\bigwedge_i
\mathcal E_i^{(k)}.
$$

因此得到：

$$
F^{(0)}
\rightarrow
F^{(1)}
\rightarrow
F^{(2)}
\rightarrow\cdots
$$

如果每一層都真的讓：

$$
|F^{(k+1)}|
\ll
|F^{(k)}|
$$

且 bridge language 始終 tractable，等號隊就可能形成真正的 hierarchical solver。

但另一種可能是：

$$
\text{local existential elimination}
\rightarrow
\text{boundary relations}
\rightarrow
\text{新的 generalized SAT}
\rightarrow
\text{再分解}
\rightarrow\cdots
$$

也就是：

$$
\boxed{\text{Recursive SAT／遞迴 SAT}}
$$

存在量詞不斷被局部消去，卻又不斷在更高層 interface 上再現。

---

# 十二、Bridge Language Drift：真正的新風險

本輪提出新的暫定量：

$$
\boxed{\operatorname{BLD}=\text{Bridge Language Drift}}
$$

令第 $k$ 層 bridge language 為：

$$
\Gamma^{(k)}.
$$

則在局部投影、組合與 pp-definition 後：

$$
\Gamma^{(k+1)}
\subseteq
\left\langle
\Gamma^{(k)}\cup\Delta^{(k)}
\right\rangle_{pp},
$$

其中 $\Delta^{(k)}$ 是該輪新引入的摘要／bridge relations。

如果：

$$
\Gamma^{(0)},\Gamma^{(1)},\ldots
$$

一直留在同一 tractable co-clone，則稱為：

$$
\boxed{\text{Bridge-Closure Stable}}
$$

若某一步：

$$
\Gamma^{(k)}
$$

跨出所有 tractable Boolean co-clones，則稱該步發生：

$$
\boxed{\text{Bridge Expressivity Transition}}
$$

這不等於證明運行時間必然爆炸，但它精確標記了「已知 tractability certificate 消失」的時刻。

---

# 十三、等號隊的新戰術：Tractable Bridge Invariant

等號隊提出：

> 我不需要一個固定 bridge language；只需要保證每次動態生成的新 relation，仍然被某個 tractable algebraic structure 保存。

也就是希望維持：

$$
\forall k,
\quad
\exists \mathcal O_k
$$

使：

$$
\mathcal O_k
\subseteq
\operatorname{Pol}(\Gamma^{(k)}),
$$

且 $\mathcal O_k$ 足以支持 polynomial-time coordination。

甚至允許：

$$
\mathcal O_k\neq\mathcal O_{k+1}.
$$

也就是動態切換：

$$
\text{Horn}
\rightarrow
\text{Affine}
\rightarrow
\text{Bijunctive}
\rightarrow\cdots
$$

只要每一步都安全即可。

這可稱為：

$$
\boxed{\text{Dynamic Tractable Bridge Invariant}}
$$

如果真存在一個 uniform polynomial-time meta-algorithm，總能為任意 SAT instance 找到這樣的安全序列，它將是一條非常強的 $P=NP$ 候選路線。

---

# 十四、不等號隊反擊：安全島之間的切換也可能產生硬 union

不等號隊指出：

$$
\Gamma^{(k)}\in\mathcal T_a,
\qquad
\Gamma^{(k+1)}\in\mathcal T_b
$$

各自 tractable，不代表它們的中介 coordination：

$$
\Gamma^{(k)}\cup\Gamma^{(k+1)}
$$

仍然 tractable。

如果切換需要同時記住兩邊語義，bridge transition 本身就可能位於：

$$
\left\langle
\Gamma^{(k)}\cup\Gamma^{(k+1)}
\right\rangle_{pp}
$$

的更高表達位置。

因此 Dynamic Algebra Switching 真正需要證明的不是：

$$
\text{每一站都在 P},
$$

而是：

$$
\boxed{
\text{每一次站與站之間的 translation／coordination 也在 P，}
}
$$

且中間表示：

$$
\boxed{
\text{保持 polynomial size、precision、construction cost。}
}
$$

這正是第十一輪 Bridge Coordination Debt 的語言格版本。

---

# 十五、Bridge Debt 升級：加入 expressivity 項

第十一輪已有：

$$
\mathbf D_B
=
(
D_{\mathrm{project}},
D_{\mathrm{summary}},
D_{\mathrm{interface}},
D_{\mathrm{arrange}},
D_{\mathrm{propagate}},
D_{\mathrm{join}},
D_{\mathrm{lift}}
).
$$

本輪新增：

$$
D_{\mathrm{express}}
$$

表示 bridge language 因 projection、union、pp-definition 或 dynamic switching 而擴張的成本／風險。

因此：

$$
\boxed{
\mathbf D_B^{+}
=
(
D_{\mathrm{project}},
D_{\mathrm{summary}},
D_{\mathrm{interface}},
D_{\mathrm{arrange}},
D_{\mathrm{propagate}},
D_{\mathrm{join}},
D_{\mathrm{lift}},
D_{\mathrm{express}}
)
}
$$

注意：$D_{\mathrm{express}}$ 目前不是傳統時間複雜度，而是結構診斷量。它只有在能被進一步連接到實際 resource lower bound 時，才有資格進入 $P\neq NP$ 證明。

---

# 十六、這一輪真正得到的嚴格部分

本輪最重要的不是新猜想，而是我們終於得到一塊相對乾淨的**正式可證區域**：

## 16.1 固定 Boolean bridge language

若 bridge coordination 確實是一個 fixed-template Boolean CSP，Schaefer dichotomy 可以直接分類 tractable／NP-complete side。

## 16.2 pp-definability

如果 bridge language $\Gamma_2$ pp-defines $\Gamma_1$，則 $\Gamma_1$ constraints 可透過 gadgets 編進 $\Gamma_2$；因此 expressive reductions 可以被正式追蹤，而不是只靠「這個看起來更強」。

## 16.3 co-clone quotient

不同 surface relation bases 可以生成同一 pp-closure，因此 bridge language 可以先按 co-clone 商掉大量語法差異。

## 16.4 portfolio union

允許多個局部 bridge languages 任意混合時，不能逐個證明它們 tractable 就結束；必須研究 union language 與其 pp-closure。

這四項都是後續雙方都可以重複使用的正式工具。

---

# 十七、但它仍然沒有解決 P/NP

必須再次自我審查。

### 17.1 Schaefer dichotomy 不是 $P\neq NP$ 證明

NP-complete side 仍可能在假設 $P=NP$ 的世界中全部屬於 P。

### 17.2 fixed constraint language 不是一般演算法

SAT solver 可以離開固定 CSP representation。

### 17.3 pp-closure 是表達能力工具，不是一般 time lower bound

它能追蹤 gadget expressibility，但不能直接證明任何圖靈機必須花超多項式時間。

### 17.4 language drift 只是 tractability-certificate loss

當 bridge 離開 Horn／affine／bijunctive 等已知 tractable 區域時，我們只能說：

$$
\text{這個已知低成本理由失效了},
$$

不能說：

$$
\text{所有可能低成本理由都不存在}.
$$

---

# 十八、障礙審查

## 18.1 相對化

本輪主要工具是 constraint-language expressibility、pp-reduction 與 universal algebra，不是單純 oracle black-box argument；但若未來試圖從這些分類直接推出一般 TM lower bound，仍需重新檢查是否以可相對化方式延伸。

## 18.2 Natural Proofs

目前不是直接做一般 circuit property 下界，因此尚未直接撞上 Natural Proofs；但任何把「bridge hard property」提升成可有效辨識的大函數集合性質時，都需要重審。

## 18.3 Algebraization

本輪高度依賴 algebraic preservation／polymorphism，因此若企圖把這些工具直接變成 $P\neq NP$ 證明，必須警惕 algebraization barrier。

## 18.4 Restricted-model trap

本輪最嚴格的結果只對 fixed Boolean CSP bridge coordination 成立，文件禁止外推成一般 deterministic computation lower bound。

---

# 十九、本輪淘汰的錯誤路線

1. 「bridge language 越多 relation，所以一定越難。」——錯；真正重要的是 pp-closure 與保存結構。
2. 「每個 bridge solver 都在 P，所以 portfolio 也在 P。」——錯；union language 可能離開所有 tractable classes。
3. 「Schaefer 說 NP-complete，所以證明了 $P\neq NP$。」——錯；這是最嚴重的偷渡之一。
4. 「沒有共同 polymorphism，所以任何算法都慢。」——錯；一般算法可離開 fixed CSP algebra。
5. 「只要每一層遞迴都能局部消去 existential，就會越來越容易。」——錯；存在量詞可在 boundary 上再現。
6. 「bridge hierarchy 是一條線。」——不精確；Boolean relation expressivity 更自然地形成偏序／co-clone lattice。
7. 「動態切換只要每個節點 tractable 即可。」——錯；transition／union／interface 本身也要算帳。

---

# 二十、雙方本輪正式攻防

## 20.1 不等號隊

本輪最佳主張：

> 一般 SAT 的困難可能不是任何單一 bridge relation，而是任意足夠完整的 dynamic bridge portfolio 在反覆 projection、union 與 pp-definition 後，無法保持在一個 polynomially stable tractable closure 中。

暫定候選：

$$
\boxed{
\text{Bridge-Closure Instability Conjecture (BCIC)}
}
$$

非正式版本：對足以表達一般 SAT 的 uniform exact decomposition scheme，bridge language 的遞迴 closure 必然在某層失去所有已知 Schaefer 型 tractability certificate，或付出超多項式的 construction／representation debt。

目前未證。

## 20.2 等號隊

本輪最佳主張：

> 固定 co-clone frontier 只限制固定語言；真正的多項式 solver 可以讓 bridge language 隨狀態改變，並使用新的摘要 relation，使每一步都落入當下合適的 tractable normal form。

暫定候選：

$$
\boxed{
\text{Dynamic Tractable Closure Scheme (DTCS)}
}
$$

若存在 uniform polynomial-time DTCS，使：

$$
F^{(0)}\to F^{(1)}\to\cdots\to F^{(k)}
$$

每一步皆：

- polynomial construction；
- polynomial representation；
- exact answer preservation；
- bridge coordination tractable；
- recursion depth polynomial；

則它將構成一條實質的 $P=NP$ 路線。

目前也未證。

---

# 二十一、本輪裁定

這一輪等號隊沒有找到 DTCS；不等號隊也沒有證成 BCIC。

但不等號隊第一次拿到了一個相對正式的「bridge 臨界地圖」：

$$
\boxed{
\text{Schaefer tractable co-clones}
\quad\text{vs.}\quad
\text{NP-complete Boolean bridge languages}
}
$$

等號隊則成功提醒：

$$
\boxed{
\text{固定語言分類}
\neq
\text{一般演算法分類}
}
$$

所以遊戲比分：

$$
P=NP:11
\qquad
P\neq NP:11.
$$

又平手。（這個比分制度可能已經被兩隊聯手操縱了。）

---

# 二十二、第十三輪入口

第十三輪建議題目：

## Tractable Closure Stability：動態 bridge 能否永遠留在安全島？

核心問題：

$$
\boxed{
\text{一串 individually tractable 的 bridge transformations，}
}
$$

$$
\boxed{
\text{能否在多項式成本內對一般 SAT 保持全程 closure-stable？}
}
$$

將研究：

1. 最小 hard union：哪些 tractable islands 的最小組合已跨入 NP-complete side？
2. language drift rate：每次 projection／summary 會增加多少 expressive power？
3. recursion depth：bridge SAT 反覆再現多少層？
4. interface width 與 expressive closure 是否存在 tradeoff？
5. 是否能建立一種**不依賴 solver identity** 的 tractable-closure certificate？
6. 等號隊能否構造 adaptive DTCS；不等號隊能否構造讓所有 DTCS 都發生 drift 的 adversarial formula family？

這將把「Bridge Language Hierarchy」從靜態分類推進成真正的**動態流**。

---

# 二十三、歷史依賴

本輪直接依賴：

1. `10_第十輪_多重反結構核心與異質黏合債務.md`
   - HGD、PIS、Dynamic Algebra Switching。
2. `11_第十一輪_共同保存結構崩塌與動態橋接.md`
   - BER、Existential Reappearance、Polynomial Bridge Principle、Bridge Universality Trap、BCD。
3. `07_第七輪_代數不變量爭奪戰與演算法代數橋.md`
   - polymorphism／CSP tractability 的代數視角。
4. `06_第六輪_多項式表示變換閉包與閉包悖論.md`
   - 避免把「所有 polynomial transforms」直接納入定義造成同義反覆。

本輪也與原始動態速率系列保持一致：困難可在搜索、表示、構造、記憶與認知之間轉移；但傳統 $P/NP$ 最終仍要求對固定計算模型建立嚴格的漸近結論。

---

# 二十四、外部理論參照

1. Thomas J. Schaefer, **The Complexity of Satisfiability Problems**, STOC 1978. DOI: 10.1145/800133.804350.
   - generalized Boolean satisfiability dichotomy 的原始來源。
2. Victor Lagerkvist, **Weak Bases of Boolean Co-Clones**, Information Processing Letters, 2014；以及 Böhler 等關於 Boolean blocks／Post's lattice 的工作。
   - 用於 co-clone、bases 與 Boolean constraint expressivity 的格結構。
3. Manuel Bodirsky 等關於 polymorphism／pp-definability Galois correspondence 的工作。
   - 在有限結構中，pp-definable relations 與 polymorphism invariance 形成完整對應。
4. Jakub Bulín and Michael Kompatscher, **Short Definitions in Constraint Languages**, 2023.
   - 研究 pp-definable relation 的短定義與表示長度，與本系列的 summary／construction debt 直接相關。
5. Dejan Jovanović and Clark Barrett, **Being Careful about Theory Combination**, Formal Methods in System Design 42(1), 2013.
   - theory combination 中 shared-variable arrangements 的 coordination cost。
6. Guilherme V. Toledo, Yoni Zohar, Clark Barrett, **Combining Combination Properties, Part I: Nelson-Oppen and Politeness**, Journal of Automated Reasoning, 2026.
   - 當代理論組合對多種 model-theoretic combination properties 的系統分析。

---

## 本輪一句話版本

$$
\boxed{
\text{Bridge 的真正危險不是「說得太多」，而是它的 closure 在組合與投影後跨出了 tractable algebra。}
}
$$

但：

$$
\boxed{
\text{跨出 tractable algebra 目前只能證明進入 NP-complete side，還不能單獨證明 }P\neq NP.
}
$$
