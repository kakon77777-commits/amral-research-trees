# P/NP 辯論遊戲研究區｜第九輪

## 尋找 SAT 的 Blossom：精確商化候選、表示反殺與商化債務

**Round 09: Searching for SAT's Blossom — Exact Quotients, Representation Counterattacks, and Quotient Debt**

- **主導研究者：** Neo.K（許筌崴）
- **協作整理：** Aletheia
- **機構：** EveMissLab（一言諾科技有限公司）
- **日期：** 2026 年 8 月 1 日
- **版本：** v1.0
- **研究狀態：** 第九輪雙假設預演
- **前置文件：** `08_第八輪_演算法代數橋壓力測試與精確商結構.md`
- **遊戲態度：** 這輪先讓等號隊認真造武器，再讓不等號隊逐一拆掉
- **文件標準：** 所有「定理」只在明示的模型內成立；尚未證明的一律標作猜想、候選或研究物件

---

## 摘要

第八輪從 matching、flow、determinant、shortest path 與 treewidth-DP 中抽出一個共同現象：高效演算法往往不是逐一處理所有微觀候選，而是建立某種**精確商結構**，把對未來答案作用相同的狀態合併，只保留必要摘要。由此提出暫定的 Polynomial Exact Quotient Scheme（PEQS）。

第九輪直接把這個思想推向 SAT，進行「尋找 SAT 的 Blossom」實驗。我們依序檢查六種現實且成熟的精確／半精確商化路線：變數消去、OBDD／DNNF 知識編譯、XOR／affine 抽取、對稱商、backdoor condensation，以及 CDCL learned-clause compression。結果顯示：每一種路線都能在特定結構上大幅壓縮搜索，但也都有可辨識的爆炸參數，例如 elimination fill-in、表示寬度、非線性殘餘核、對稱破缺成本、backdoor 大小、證明系統強度與 learned-clause 成長。

本輪最重要的反例來自 OBDD：存在本身屬於多項式時間可計算的函數，例如整數除法的輸出位元，其 OBDD 在任何變數順序下仍可需要指數大小。這證明「某種精確商表示必然爆炸」甚至不只不能證明 $P\neq NP$，它連「函數不在 $P$」都不能推出。表示大小與演算法時間之間不存在如此直接的一一對應。

因此本輪不再尋找單一「神奇表示」，而提出新的研究物件：**商化債務（Quotient Debt）**。任何精確商化若壓低了在線搜索，可能把成本轉移到編譯時間、摘要大小、邊界寬度、例外變數、代數殘餘、證明長度或答案 lifting。商化債務不是已證明的守恆律，而是一個用來統一比較不同 SAT 壓縮方法的資源帳本。

本輪最後提出下一步問題：是否存在 SAT 實例族，在多種已知商化結構上**同時缺乏低成本逃逸通道**？若存在，便可研究「多重反結構核心」（Multi-Anti-Structure Core）；若不存在，等號隊則可能利用多表示 portfolio 逐層剝離所有困難。

---

# 一、上輪戰果：精確商化到底是什麼？

第八輪觀察到：

$$
\text{matching}
\rightarrow
\text{blossom contraction},
$$

$$
\text{max-flow}
\rightarrow
\text{residual-network summary},
$$

$$
\text{determinant}
\rightarrow
\text{elimination},
$$

$$
\text{shortest path}
\rightarrow
\text{semiring aggregation},
$$

$$
\text{bounded-treewidth DP}
\rightarrow
\text{separator state quotient}.
$$

它們的共同形式是：

$$
\Omega
\xrightarrow{\sim}
\Omega/\!\sim
\xrightarrow{\text{exact evaluation}}
\{0,1\}\text{ 或最優值}.
$$

其中 $\Omega$ 是巨大微觀候選空間，而等價關係 $\sim$ 只合併那些「對剩餘計算具有相同作用」的狀態。

若 SAT 也存在類似 blossom 的局部—全域 contraction，就可能出現：

$$
2^n\text{ 個賦值}
\longrightarrow
\operatorname{poly}(n)\text{ 個等價摘要}
\longrightarrow
\text{精確 SAT/UNSAT 判定}.
$$

本輪的任務不是假設這個結構存在，而是拿現有 SAT 技術逐一檢驗：它們是否已經是 SAT Blossom 的局部版本？

---

# 二、等號隊的武器一：變數消去（Variable Elimination）

考慮 CNF 公式 $F$ 與變數 $x$。將包含 $x$ 的子句與包含 $\neg x$ 的子句做 resolution，產生 resolvents，再刪除所有含 $x$ 的原子句，可以得到與原公式在可滿足性上等價的消去結果。

抽象地寫：

$$
F
\xrightarrow{\operatorname{elim}(x)}
F',
$$

且：

$$
F\text{ 可滿足}
\iff
F'\text{ 可滿足}.
$$

這就是非常直接的精確 quotient：變數 $x$ 的兩種可能性不再顯式存在，而被投影進新的子句關係。

SAT preprocessing 中的 bounded variable elimination 也確實是重要實務技術；Eén 與 Biere 的工作展示，variable/clause elimination 結合 subsumption 等手段能顯著縮小許多工業 SAT 實例並改善求解時間。

## 2.1 等號隊的理想劇本

若存在一個變數順序：

$$
\pi=(x_{\pi(1)},\ldots,x_{\pi(n)}),
$$

使每次消去後的公式大小都保持：

$$
|F_i|\leq\operatorname{poly}(n),
$$

則：

$$
F_0\to F_1\to\cdots\to F_n\in\{\top,\bot\}
$$

便可能形成一個直接的多項式求解路線。

## 2.2 不等號隊反擊：fill-in 與 induced width

消去不會憑空消除依賴；它可能把原本分散的局部依賴轉成更大的新約束。圖論上，這與 elimination ordering 產生的 fill-in、treewidth／induced width 密切相關。

因此真正的成本不是「消掉一個變數要幾步」，而是：

$$
\operatorname{Debt}_{\mathrm{elim}}
=
\max_i |F_i|
$$

或更結構化地用消去寬度刻畫。

若寬度 $w$ 很小，動態規劃／消去確實能在大致指數於 $w$、多項式於輸入大小的時間求解；若 $w$ 隨 $n$ 成長，這個路線便可能爆炸。

**本輪裁定：** 變數消去是 SAT Blossom 的真實局部版本，但其逃逸條件受 elimination width 控制，尚非一般多項式壓縮器。

---

# 三、等號隊的武器二：OBDD／DNNF 知識編譯

第二種策略更加貼近影片的原始啟發：先把公式編譯成一個可直接求值的數學／圖形物件。

令：

$$
\operatorname{Compile}(F)=R_F.
$$

若 $R_F$ 是 OBDD、DNNF、d-DNNF 等結構，則許多查詢可以在編譯後快速完成。

理想情況：

$$
T_{\mathrm{compile}}(F)\in\operatorname{poly}(n),
$$

$$
|R_F|\in\operatorname{poly}(n),
$$

$$
T_{\mathrm{query}}(R_F)\in\operatorname{poly}(n).
$$

那麼 SAT 就被真正「函數化」了。

## 3.1 不等號隊反擊：表示大小會爆炸

OBDD 與 structured DNNF 已知存在強 size lower bounds。這說明某些布林函數的精確知識編譯，不可能在該表示族中保持小尺寸。

但這裡出現本輪最重要的反殺。

### 反殺：P 中函數也可以有指數 OBDD

已有結果顯示，整數除法某些輸出位元函數，對任何變數順序，其 OBDD 都需要指數大小。

然而整數除法本身顯然可以在多項式時間計算。

因此：

$$
\boxed{
\text{OBDD size}=2^{\Omega(n)}
\not\Rightarrow
f\notin P
}
$$

甚至：

$$
\boxed{
\text{所有 ordering 都爆炸}
\not\Rightarrow
\text{不存在另一種多項式演算法}
}
$$

這是對不等號隊非常重要的警告：表示下界與時間下界之間必須另外建立橋樑，不能直接偷接。

**本輪裁定：** Knowledge Compilation 是最接近「先構造、後直接求值」的 SAT Blossom 候選之一，但任何特定 compilation language 的 size lower bound 都不能直接升格為 $P\neq NP$。

---

# 四、等號隊的武器三：XOR／Affine Extraction

許多 CNF 實例中可能藏有 parity 關係：

$$
x_1\oplus x_2\oplus\cdots\oplus x_k=b.
$$

若能抽取成 $\mathbb F_2$ 線性系統：

$$
Ax=b,
$$

便可以用 Gaussian／Gauss-Jordan elimination 做多項式時間推理。

現代 SAT 研究中已有把 clause learning 與完整 parity reasoning 結合的 DPLL(XOR) 類方法；cryptographic SAT 也顯示，保留 ANF/XOR 結構有時比把一切壓回普通 CNF 更有效。

## 4.1 等號隊主張

一般 SAT 也許只是把多種隱含代數結構混在一起：

$$
F
=
F_{\mathrm{affine}}
\wedge
F_{\mathrm{Horn}}
\wedge
F_{\mathrm{2SAT}}
\wedge
F_{\mathrm{residual}}.
$$

若每次都抽取可 tractable 的結構，剩餘核心可能逐步縮小。

## 4.2 不等號隊反擊

affine extraction 只能解決確實具有 affine closure 的部分。混合 CNF + XOR 並不因此自動進入 $P$；真正困難可能集中在：

$$
F_{\mathrm{residual}}.
$$

所以：

$$
\operatorname{Debt}_{\mathrm{affine}}
=
|F_{\mathrm{nonlinear\ residual}}|.
$$

**本輪裁定：** 表示革命可以打穿錯誤座標系造成的假困難，但剩餘非線性核心仍可能保存真正困難。

---

# 五、等號隊的武器四：Symmetry Quotient

若兩組賦值在問題對稱群 $G$ 下等價：

$$
a\sim b
\iff
\exists g\in G,
\quad
b=g(a),
$$

那麼搜索所有軌道成員是浪費。

可將搜索空間縮成：

$$
\{0,1\}^n/G.
$$

symmetry-breaking predicates 的經典工作表明，在許多搜索問題中加入適當對稱破缺條件可以顯著削減冗餘；但一般情況下完整 symmetry breaking 本身也可能難以生成，只能使用部分 predicates。

因此：

$$
\operatorname{Debt}_{\mathrm{sym}}
=
T_{\mathrm{detect}}
+
T_{\mathrm{break}}
+
|\{0,1\}^n/G|.
$$

若公式幾乎沒有有用的對稱性：

$$
|G|\approx1,
$$

此 quotient 幾乎沒有收益。

**本輪裁定：** 對稱商是真實而漂亮的候選壓縮，但它只消除「重複」，不能保證消除「本質不同的候選」。

---

# 六、等號隊的武器五：Backdoor Condensation

令 $B$ 是一組變數，使得對 $B$ 的每個賦值 $\beta$，剩餘公式都進入某個 tractable class $\mathcal C$：

$$
F\!
estriction_\beta\in\mathcal C.
$$

則：

$$
\operatorname{SAT}(F)
=
\bigvee_{\beta\in\{0,1\}^{B}}
\operatorname{SAT}(F\!\restriction_\beta).
$$

若：

$$
|B|=O(\log n),
$$

則即使枚舉所有 backdoor assignments：

$$
2^{|B|}=\operatorname{poly}(n).
$$

這簡直像 SAT 的「小型控制面」：只要先決定少量關鍵變數，其餘部分就全部落入容易世界。

Backdoor 研究確實把 SAT/CSP 中「少量關鍵變數控制整體難度」正式化，並研究不同 base classes 下 backdoor detection 的 parameterized complexity。

## 6.1 不等號隊反擊

問題有兩層：

1. 小 backdoor 是否存在？
2. 即使存在，能否低成本找到？

總成本至少為：

$$
\operatorname{Debt}_{\mathrm{backdoor}}
=
T_{\mathrm{detect}}(B)
+2^{|B|}\operatorname{poly}(n).
$$

若最小 backdoor 為：

$$
|B|=\Theta(n),
$$

則這條路線仍然指數化。

**本輪裁定：** Backdoor 是最清楚的「困難濃縮成少數自由度」模型，但它本身把問題轉成：一般 SAT 是否總存在 polylog-size、polytime-detectable 的 backdoor？目前沒有這樣的結果。

---

# 七、等號隊的武器六：CDCL Learned-Clause Compression

現代 CDCL 求解器不只是搜索，它會從衝突中學習新子句：

$$
\text{conflict history}
\longrightarrow
\text{learned clause}
\longrightarrow
\text{大量未來分支被同時排除}.
$$

這非常符合「精確商化」：一條 learned clause 可代表大量已被證明無效的微觀路徑。

可暫時寫成：

$$
H_t
\xrightarrow{\operatorname{learn}}
C_t,
$$

其中 $H_t$ 是龐大的衝突歷史，$C_t$ 是較短的可重複摘要。

CDCL 與 resolution proof complexity 有深刻關係；現代研究仍在探索如何壓縮 learned clauses。2026 年 SAT Conference 的工作甚至直接研究 learned-clause factoring，顯示「如何把已學資訊再壓縮」本身仍是活躍技術問題。

## 7.1 不等號隊反擊：proof-system debt

若某類 UNSAT 公式在 resolution 中需要指數證明，則任何被限制在相應證明能力的求解流程都可能遇到巨大 learned-clause／衝突歷史成本。

但這仍不是一般下界，因為：

$$
\text{resolution hard}
\not\Rightarrow
\text{all proof systems hard}.
$$

而且已有工作展示，改換到 MaxSAT／更強推理框架後，某些對 resolution/CDCL 困難的公式可以被不同形式的推理快速處理。

因此：

$$
\operatorname{Debt}_{\mathrm{proof}}
=
\text{所選 proof system 中的最小證明資源}.
$$

**本輪裁定：** Clause learning 是「用歷史製造未來 quotient」的實務範例，但任何基於 resolution 的下界都有 proof-system escape。

---

# 八、SAT Blossom 候選矩陣

| 商化方法 | 被商掉的東西 | 精確性 | 成功參數 | 主要爆炸點 | 是否一般 SAT Blossom？ |
|---|---|---:|---|---|---|
| Variable Elimination | 被消去變數的分支 | 是 | 小 elimination width | fill-in / resolvents | 否 |
| OBDD / DNNF | 等價子函數 | 是 | 小 representation width/size | compiled size | 否 |
| XOR / Affine | parity 關係 | 是 | affine structure 強 | nonlinear residual | 否 |
| Symmetry Quotient | 對稱軌道 | 是 | 大 symmetry group | detection / orbit count | 否 |
| Backdoor | 例外自由度 | 是 | 小 backdoor | detection + $2^k$ | 否 |
| CDCL Learning | 衝突歷史 | 是 | 短 proof / reusable clauses | proof length / clause database | 否 |

目前沒有一個候選能單獨覆蓋一般 SAT。

但它們也不是互相重複。它們壓縮的是不同種類的冗餘：

$$
\text{變數冗餘},
\text{函數冗餘},
\text{代數冗餘},
\text{對稱冗餘},
\text{例外自由度},
\text{歷史冗餘}.
$$

這讓等號隊得到一個新的主意：

> 也許 SAT Blossom 不是單一 contraction，而是一個自適應 quotient portfolio。

---

# 九、等號隊升級：Hybrid Quotient Portfolio

設 quotient operators 為：

$$
\mathcal Q
=
\{Q_{\mathrm{elim}},Q_{\mathrm{KC}},Q_{\mathrm{xor}},Q_{\mathrm{sym}},Q_{\mathrm{bd}},Q_{\mathrm{learn}},\ldots\}.
$$

建立一個統籌器：

$$
\operatorname{ORCH}(F_t)
\rightarrow
Q_i,
$$

每一步根據當前公式選擇最適合的商化：

$$
F_{t+1}=Q_i(F_t).
$$

理想情況是存在某個勢函數：

$$
\Phi(F_t)
$$

使每次商化都保證：

$$
\Phi(F_{t+1})<\Phi(F_t),
$$

且經過多項式步驟後：

$$
F_T\in\mathcal C_{\mathrm{easy}}.
$$

若每步構造與中間表示都保持多項式界，這就會是一條真正的 $P=NP$ 候選機制。

這比「一定存在一個神奇函數」更接近實際演算法工程：不同結構用不同武器。

---

# 十、不等號隊的新主張：Quotient Debt

面對 hybrid portfolio，不等號隊不能再只證明其中一種方法會爆炸。

因此提出新的資源帳本：

$$
\boxed{
\mathbf D_Q(F)
=
(D_{\mathrm{build}},
D_{\mathrm{size}},
D_{\mathrm{width}},
D_{\mathrm{residual}},
D_{\mathrm{detect}},
D_{\mathrm{proof}},
D_{\mathrm{lift}})
}
$$

其中：

- $D_{\mathrm{build}}$：商結構建構成本；
- $D_{\mathrm{size}}$：摘要／編譯表示大小；
- $D_{\mathrm{width}}$：邊界、消去或分解寬度；
- $D_{\mathrm{residual}}$：未被商掉的困難核心；
- $D_{\mathrm{detect}}$：尋找 symmetry/backdoor/結構的成本；
- $D_{\mathrm{proof}}$：為證明 UNSAT 所累積的證明資源；
- $D_{\mathrm{lift}}$：從商化結果恢復原問題答案／見證的成本。

這稱為：

$$
\boxed{\text{Quotient Debt / 商化債務}}
$$

但必須立刻聲明：

> 商化債務目前不是守恆定律，也沒有證明它必須超多項式。它只是跨方法比較成本轉移的統一帳本。

不等號隊真正需要證明的是某種非循環下界，例如：

$$
\forall\text{ admissible quotient pipelines }\Pi,
\quad
\max_t \|\mathbf D_Q(F_t)\|
\geq
n^{\omega(1)}
$$

對某個顯式 SAT 實例族成立。

目前完全沒有這個一般定理。

---

# 十一、本輪最重要的反例：表示爆炸不等於計算爆炸

這一點值得獨立記錄，因為它會阻止未來很多假證明。

假設某布林函數 $f_n$ 對某表示族 $\mathcal R$ 滿足：

$$
\forall R\in\mathcal R(f_n),
\quad
|R|\geq2^{\Omega(n)}.
$$

不能推出：

$$
f_n\notin P.
$$

整數除法的 OBDD 下界就是具體反例：函數可以有多項式時間演算法，卻沒有小 OBDD。

因此任何未來的「跨表示不變量」若要真正碰到 $P/NP$，必須建立：

$$
\boxed{
\text{表示／結構下界}
\Longrightarrow
\text{一般 uniform time lower bound}
}
$$

的額外橋樑。

這個橋樑本身可能比找到某個漂亮下界更困難。

---

# 十二、影片啟發在第九輪的重新解讀

最初影片展示：

$$
\text{多條條件分支}
\rightarrow
\text{一個數學函數}
\rightarrow
\text{直接求值}.
$$

第九輪的結果不是否定這種可能，而是把它精確化：

$$
\text{SAT 的條件空間}
\rightarrow
\text{某種 quotient representation}
\rightarrow
\text{快速判定}
$$

完全可能在**特定結構**上發生，而且現代 SAT 技術每天都在做局部版本。

真正未知的是：

$$
\boxed{
\text{是否存在一個 uniform、polynomial、exact 的 quotient portfolio，}
}
$$

$$
\boxed{
\text{能對所有 SAT 實例把商化債務都保持在多項式界？}
}
$$

這其實已經非常接近本系列目前的 $P=NP$ 方最強構造版本。

反方則要證明：

$$
\boxed{
\text{存在一族 SAT 實例，使所有 admissible quotient portfolio}
}
$$

$$
\boxed{
\text{都至少在一個商化債務維度上超多項式爆炸。}
}
$$

---

# 十三、下一輪：多重反結構核心

第十輪不再逐個問「這種方法有沒有 hard example」，而改成：

> 能否找到或構造一族公式，讓多個已知低成本逃逸通道同時失效？

例如希望同一公式族同時具有：

$$
\text{high elimination/treewidth},
$$

$$
\text{no small backdoor},
$$

$$
\text{little useful symmetry},
$$

$$
\text{large OBDD / compilation size},
$$

$$
\text{weak affine extractability},
$$

$$
\text{long proofs in selected proof systems}.
$$

暫稱：

$$
\boxed{\text{MASC = Multi-Anti-Structure Core}}
$$

或「多重反結構核心」。

## 等號隊下一輪任務

證明上述條件即使同時成立，也可能還有未列入的新表示逃逸；最好拿一個本來就在 $P$ 的函數／問題作反例，展示「多種 representation hardness 仍不等於 time hardness」。

## 不等號隊下一輪任務

尋找顯式 SAT／CSP 家族，在多種已知 quotient measure 上同時具有大下界，並研究這些大下界是否來自某個共同原因，而非偶然疊加。

---

# 十四、本輪淘汰的錯誤路線

1. 「Variable elimination 會爆炸，所以 $P\neq NP$。」——只限制消去型方法。
2. 「所有 variable ordering 的 OBDD 都指數大，所以不在 $P$。」——被整數除法直接反例擊破。
3. 「XOR 很好解，所以一般 SAT 也可能線性化。」——只對 affine 結構成立。
4. 「把所有 symmetry quotient 掉就能 polynomial。」——一般公式可能沒有足夠 symmetry，完整破缺也有成本。
5. 「SAT 都有小 backdoor，只是我們還沒找到。」——沒有普遍結果支持。
6. 「CDCL 已很強，所以 learned clauses 會收斂成 polynomial。」——受 proof-system complexity 限制，且未有一般保證。
7. 「把六種方法混合就一定能覆蓋所有公式。」——portfolio 的完備低成本性正是待證問題。
8. 「商化債務一定守恆。」——目前只是研究猜想，尚無守恆定理。

---

# 十五、本輪裁定

## 等號隊得分

等號隊成功證明：

- SAT 已存在大量真實、精確的局部 quotient 技術；
- 不同技術處理不同結構；
- 特定表示的指數下界不能排除別的多項式演算法；
- hybrid quotient portfolio 仍是一條邏輯上開放的 $P=NP$ 路線。

## 不等號隊得分

不等號隊成功證明：

- 每一個已知 quotient 都有可明示的結構參數與爆炸點；
- 把搜索壓掉常常只是把成本移到 compilation、width、residual、detection 或 proof；
- 要證明 $P=NP$，不能只展示一兩類公式被商化，而必須處理所有 worst-case SAT instances。

本輪遊戲比分：

$$
P=NP:8
\qquad
P\neq NP:8.
$$

比分只是研究遊戲介面，不構成任何數學證據。

---

# 十六、外部理論參照

1. Niklas Eén and Armin Biere, **Effective Preprocessing in SAT Through Variable and Clause Elimination**, SAT 2005.
   - 用於 SAT variable/clause elimination 與實務 preprocessing。
2. Jan Krajíček, **An exponential lower bound for a constraint propagation proof system based on ordered binary decision diagrams**.
   - 用於 OBDD-based proof system 的指數下界。
3. Takashi Horiyama and Shuzo Yajima, **Exponential Lower Bounds on the Size of Variants of OBDD Representing Integer Division**, 1998.
   - 關鍵反例：P-time function 仍可在所有 OBDD ordering 下需要指數大小。
4. Thammanit Pipatsrisawat and Adnan Darwiche, **A Lower Bound on the Size of Decomposable Negation Normal Form**, AAAI 2010.
   - 用於 structured DNNF／OBDD 類表示下界。
5. Tero Laitinen, Tommi Junttila, Ilkka Niemelä, **Extending Clause Learning SAT Solvers with Complete Parity Reasoning**, 2012.
   - 用於 DPLL(XOR) 與增量 Gauss-Jordan parity reasoning。
6. James Crawford, Matthew Ginsberg, Eugene Luks, Amitabha Roy, **Symmetry-Breaking Predicates for Search Problems**, KR 1996.
   - 用於 SAT/search symmetry quotient 與 symmetry-breaking predicates。
7. Serge Gaspers et al., **Backdoors into Heterogeneous Classes of SAT and CSP**, AAAI 2014；以及 Gaspers & Szeider, **Backdoors to satisfaction continued**, 2026 survey.
   - 用於 backdoor condensation 與 parameterized complexity。
8. Florian Pollitt et al., **Factoring Learned Clauses**, SAT 2026.
   - 用於現代 CDCL learned-clause compression 的最新實例。
9. Alexey Ignatiev, Antonio Morgado, João Marques-Silva, **On Tackling the Limits of Resolution in SAT Solving**, 2017.
   - 用於「resolution/CDCL hard 不等於所有推理框架 hard」的表示／proof-system escape。

---

## 第九輪一句話結論

$$
\boxed{
\text{我們找到了很多 SAT 的「局部 Blossom」，但還沒有找到 SAT 的 Blossom。}
}
$$

更精確地說：

$$
\boxed{
\text{真正的爭點不再是能不能壓縮，而是能不能對所有實例，}
}
$$

$$
\boxed{
\text{以 uniform polynomial cost 持續找到正確的精確商。}
}
$$
