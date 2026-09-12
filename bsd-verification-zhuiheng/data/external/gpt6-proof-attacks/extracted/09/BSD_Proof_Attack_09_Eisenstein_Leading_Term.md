# BSD Proof Attack 09：可用的 Eisenstein 退化與二次 leading term

日期：2026-09-12  
狀態：新輔助資料、精確有限計算與書面推導完成；未宣稱計算出 Coleman 族、其 period 常數或 Beilinson–Flach 類的座標。  
交接：使用者回報本地端重新執行新程式及其他驗證，未見重大失誤；本輪未收到該次驗證日誌或具體修正，因此將其記為使用者回報，不冒充本輪獨立重播。

本輪不重新執行舊 Kurihara 計算。它使用既有的二維 Hecke 特徵空間，計算一個新的負號分量及導子 $8$ 的扭曲 moment，證明退化公式中的額外因子非零。由此取得一條具體的 leading-term 比較：

$$
\boxed{
\kappa^\dagger
=\frac{\log_{11}(12)D_E}{26C\,\lambda_8(0)}
\,[t^2]\widehat{\mathcal B}_E(t).
}
\tag{1}
$$

式中 $\lambda_8(0)$ 的非零性已由本輪有限計算解決；$D_E$ 的非零性來自 adjoint interpolation；$C$ 是固定規範後仍未知的 Eisenstein leading period。右側 Beilinson–Flach leading class 的存在使用已發表的退化定理，並非本輪程式已算出的 cohomology vector。

## 1. 輸入與三種不同參數

沿用

$$
E:y^2+y=x^3+x^2-2x,\qquad N_E=389,\qquad p=11,
$$

$$
P=(0,0),\quad Q=(1,0),\quad
a_{11}(E)=-4,\quad \alpha_E\equiv7\pmod{11}.
$$

先前接受的算術資料包括殘餘像含 $\mathrm{SL}_2(\mathbb F_{11})$、ordinary 且非異常，以及固定規範的

$$
z^\dagger_\infty(t)=t\kappa^\dagger+O(t^2),\qquad
\operatorname{Col}_E(z^\dagger_\infty)=a_2t^2+O(t^3),
\tag{2}
$$

其中 $\kappa^\dagger\ne0$、$a_2\ne0$。Attack 06 給出的尺度關係是

$$
\kappa^\dagger=16s_{11}\operatorname{adj}(H)\ell.
\tag{3}
$$

以上不是本輪重新計算的項目。

| 記號 | 所屬方向 | 本稿規範 |
|---|---|---|
| $X$ | 輔助 Eisenstein 族的權重方向 | 權重角色在 $12$ 的值減 $1$；權重 $2$ 的中心為 $X=0$ |
| $t$ | 橢圓曲線的 cyclotomic 方向 | $\gamma-1$，且 $\chi_{\mathrm{cyc}}(\gamma)=12$ |
| $t_{\mathrm{dR}}$ | Fontaine／Robba 的 period | 不是前兩個參數 |

文獻可能對後兩者都使用字母 $t$。本稿始終區分。Attack 08 的幾何參數 $\tau$ 也沒有被認作以上任一參數。

令 $\sigma_t$ 是 cyclotomic 權重空間的平凡有限角色分支，滿足

$$
\sigma_t(12)=1+t,\qquad
j(t)=\frac{\log(1+t)}{\log_{11}(12)}.
\tag{4}
$$

故文獻的一次 logarithmic distribution 在此分支是 $j(t)$。

## 2. 一個確實可用的輔助 Eisenstein 形式

令 $\chi_8$ 為 primitive 二次特徵：

$$
\chi_8(a)=
\begin{cases}
1,&a\equiv1,7\pmod8,\\
-1,&a\equiv3,5\pmod8,\\
0,&2\mid a.
\end{cases}
$$

選定

$$
f=E_2(1,\chi_8),\qquad
f_\beta(q)=f(q)-f(q^{11}).
\tag{5}
$$

它的 tame level 是 $8$，與 $389$ 互質。其正整數 Fourier 係數及常數項為

$$
a_n(f)=\sum_{d\mid n}\chi_8(d)d,\qquad
a_0(f)=-\frac12.
\tag{6}
$$

例如廣義 Bernoulli 數可以直接算成

$$
B_{2,\chi_8}
=8\sum_{a=1}^{8}\chi_8(a)
\left(\frac{a^2}{64}-\frac a8+\frac16\right)=2,
$$

故常數項是 $-B_{2,\chi_8}/4=-1/2$。

因為 $\chi_8(11)=-1$，Hecke 多項式是

$$
U^2+10U-11=(U-1)(U+11).
$$

兩個 refinement 的特徵值是 $1$ 與 $-11$；式 (5) 選擇 slope $1$ 的後者。由除數和公式，寫 $n=11^km$、$11\nmid m$，有

$$
a_n(f_\beta)=(-11)^k a_m(f),
$$

所以 $U_{11}f_\beta=-11f_\beta$。本輪程式也給出有限 Fourier 係數及相應恆等式的實際輸出。

### 命題 09.1：decency 與 non-criticality

$f_\beta$ 滿足本例退化構造所用的 decency 與 non-criticality 條件。

**證明。** $\chi_8$ 非平凡且為 even；在 level 的唯一素數 $2$，比值特徵的 conductor 被 $2$ 整除；在 $11$，其值為 $-1\ne1$。這正好滿足權重 $2$ 情形的 decency 條件。

non-criticality 可透過局部 Kummer 類直接確認。取

$$
K=\mathbb Q(\sqrt2),\qquad \epsilon=1+\sqrt2,\qquad N_{K/\mathbb Q}(\epsilon)=-1.
$$

共軛滿足 $\epsilon^\sigma=-\epsilon^{-1}$，故其有理 Kummer 類在 $\chi_8$ 分量。$2$ 在模 $11$ 非平方，於是 $K$ 在 $11$ 的完備化是非分裂的非分歧二次擴張。

直接整數運算給出

$$
\epsilon^{24}=768398401+543339720\sqrt2
\equiv1+110\sqrt2\pmod{121}.
$$

由 $\log(\epsilon)=\log(\epsilon^{24})/24$，且 log 級數的二次及以上項都被 $121$ 整除，

$$
\boxed{
\log_{11}(\epsilon)\equiv55\sqrt2\pmod{121},\qquad
\frac{\log_{11}(\epsilon)}{11\sqrt2}\equiv5\pmod{11}.
}
\tag{7}
$$

尾項估計是 $v_{11}(u^m/m)\ge m-v_{11}(m)\ge2$，其中 $u\in11\mathcal O_{K_{11}}$、$m\ge2$。故式 (7) 證明的是實際局部 log 非零，不只是浮點訊號。

因此

$$
H_f^1(\mathbb Q,\mathbb Q_{11}(\chi_8)(1))
\longrightarrow H_f^1(\mathbb Q_{11},\mathbb Q_{11}(\chi_8)(1))
$$

非零。non-criticality 與此條件的等價性使用 [Bellaïche–Dasgupta，The p-adic L-functions of evil Eisenstein series，Remark 1.5](https://arxiv.org/html/1208.4352v1)，以及包含本例 decency 規範的 [Loeffler–Rivero，Theorem A4.5](https://arxiv.org/html/2201.02078v2)。證畢。

同一退化框架於是提供通過 $f_\beta$ 的局部 Coleman 族。橢圓曲線一側使用通過 $f_E$ 的 ordinary 族；大殘餘像及 ordinary 條件使用已接受的輸入。因為此處 $\psi=1$，退化所選的 Kato 分量對應原來的 $E$。

**尚未計算的量。** 式 (7) 是輔助 Kummer 單位的 regulator，不是下面的 $C$；兩者都在某個正規化下非零，不代表它們相等。

## 3. 新計算：額外扭曲因子在中心不消失

令

$$
F=f_E\otimes\chi_8,\qquad
\alpha_F=-\alpha_E\equiv4\pmod{11}.
$$

需要處理的函數是

$$
\lambda_8(t)=L_p(F,\sigma_t x^{-1}),
\qquad
\lambda_8(0)=L_p(F,x^{-1}).
\tag{8}
$$

$x^{-1}$ 是 $\mathbb Z_{11}^\times$ 上的完整角色，包含 odd 的 Teichmüller 分量。不能把式 (8) 改成平凡分支的中心值，也不能把它等同於複數 $L(F,1)$。

### 3.1 接受既有二維空間，計算新的負號線

**INPUTS.json** 嵌入先前 certificate 的二維 Hecke 特徵空間 $B$，其行對應

$$
(1,0),(1,1),\ldots,(1,388),(0,1)
\quad\text{於 }\mathbb P^1(\mathbb F_{389}).
$$

這份既有輸入的身份及雜湊在包內保留。本輪只對此空間求

$$
v(c,d)+v(-c,d)=0,
\tag{9}
$$

取得唯一負號線；依固定順序，第一個非零座標是 index $3$，將其設為 $1$。

記對應的 primitive 負號模符號為 $\Phi_E^-$。既有特徵空間確實包含 $E$ 的 characteristic-zero 特徵線之 primitive reduction，故一維性識別了本輪使用的 reduction。這個識別是接受舊 certificate 的位置，不是從新的四十項和式倒推 eigenvector。

此正規化也可取成 $\Phi_E^-(1/3)=1$，其中 cusp 記號表示路徑 $\{\infty,1/3\}$。本輪所有模 $11$ 精確數值都相對於這個負號 period；不把它未經比較便當作 Néron 負號週期。

### 3.2 扭曲 period 的明確選擇

對 $r\in\mathbb Q$ 定義

$$
\Phi_F(r)=
\sum_{b\in\{1,3,5,7\}}\chi_8(b)\,
\Phi_E^-(r+b/8).
\tag{10}
$$

若 $G(\chi_8)=\sum_b\chi_8(b)e^{2\pi ib/8}$，則 Fourier 扭曲公式

$$
F(z)=G(\chi_8)^{-1}\sum_b\chi_8(b)f_E(z+b/8)
$$

說明式 (10) 對應 period $\Omega_F^-=\Omega_E^-/G(\chi_8)$。這是本稿扭曲因子的尺度規範。下面引用退化公式時，所有 period 與表示 transport 都採相容規範；未對齊規範的文獻常數不能直接代入。

因為 $\chi_8$ 為 even 而 $\Phi_E^-$ 為 odd，$\Phi_F(0)=0$。

### 3.3 由 Hecke 關係得到有界測度

對 $a\in\mathbb Z$、$n\ge1$，置

$$
\mu_F(a+11^n\mathbb Z_{11})
=\alpha_F^{-n}\Phi_F(a/11^n)
-\alpha_F^{-n-1}\Phi_F(a/11^{n-1}).
\tag{11}
$$

此處符號取值於 $\mathbb Z_{11}$ 且 $\alpha_F$ 是 unit，故有界性成立。相容性也可直接由 Hecke 關係推出：

$$
\sum_{b=0}^{10}
\Phi_F\!\left(\frac{a+b11^n}{11^{n+1}}\right)
=a_{11}(F)\Phi_F(a/11^n)-\Phi_F(a/11^{n-1}),
$$

再用 $a_{11}(F)=\alpha_F+11/\alpha_F$，便得小球測度之和等於大球測度。

式 (11) 是本稿 ordinary $L$ 函數的測度規範，因此

$$
\lambda_8(0)=\int_{\mathbb Z_{11}^\times}x^{-1}\,d\mu_F(x).
$$

在 $a+11\mathbb Z_{11}$ 上，$x^{-1}\equiv a^{-1}\pmod{11}$。積分模 $11$ 只需四十個新 cusp 值：

$$
S_a=\sum_{b\in\{1,3,5,7\}}\chi_8(b)
\Phi_E^-\!\left(\frac{8a+11b}{88}\right),
$$

$$
\lambda_8(0)\equiv
4^{-1}\sum_{a=1}^{10}a^{-1}S_a\pmod{11}.
\tag{12}
$$

### 命題 09.2：本例的額外因子是非零的

在上述明確 period 規範下，

$$
\boxed{\lambda_8(0)\equiv5\pmod{11}.}
\tag{13}
$$

**有限計算。** continued fractions 將每條 $\{\infty,(8a+11b)/88\}$ 路徑分解為行列式 $\pm1$ 的邊，再由其底列讀取模符號。程式輸出每一條路徑的 indices 及值；壓縮表如下。所有表格項均在 $\mathbb F_{11}$。

| $a$ | $S_a$ | $a^{-1}$ | $a^{-1}S_a$ | $\mu_F(a+11\mathbb Z_{11})$ |
|---:|---:|---:|---:|---:|
| $1$ | $4$ | $1$ | $4$ | $1$ |
| $2$ | $9$ | $6$ | $10$ | $5$ |
| $3$ | $3$ | $4$ | $1$ | $9$ |
| $4$ | $4$ | $3$ | $1$ | $1$ |
| $5$ | $3$ | $9$ | $5$ | $9$ |
| $6$ | $8$ | $2$ | $5$ | $2$ |
| $7$ | $7$ | $8$ | $1$ | $10$ |
| $8$ | $8$ | $7$ | $1$ | $2$ |
| $9$ | $2$ | $5$ | $10$ | $6$ |
| $10$ | $7$ | $10$ | $4$ | $10$ |

第四欄之和是 $9$，乘 $4^{-1}=3$ 得 $5$。由有界測度及前述模 $11$ 同餘，這是一個真正的非零性證明，條件是使用本節明列的已接受模符號輸入。證畢。

改用其他非零 period 會改變數值尺度，卻不會把非零變成零；「為 $11$-unit」則是相對於本節所選的整規範。

## 4. 其他局部因子不會新增零點

選 smoothing 整數 $d=5$；它與 $6\cdot8\cdot389\cdot11$ 互質。Eisenstein 與橢圓曲線的權重參數都在 $0$，cyclotomic 角色平凡時，退化公式中的 smoothing 因子為

$$
\mathscr S_5(0)=5^2-\chi_8(5)^{-1}=26.
\tag{14}
$$

記

$$
D_E=L_p(\operatorname{Ad}\mathbf g)(0),
$$

其中 $\mathbf g$ 是 ordinary 橢圓曲線族，period 與前述選擇相容。其 interpolation 是非零 Petersson／period 比值乘上

$$
\left(1-\frac{\beta_E}{\alpha_E}\right)
\left(1-\frac{\beta_E}{11\alpha_E}\right),
\qquad \beta_E=11/\alpha_E.
$$

此 Euler 乘數模 $11$ 是

$$
1\cdot(1-7^{-2})\equiv3\pmod{11},
$$

所以 $D_E\ne0$。本輪沒有計算其值，也沒有把 Petersson／period 比值說成 $11$-unit。

因此

$$
\mathscr A_E(t)=
\frac{\mathscr S_5(t)\lambda_8(t)}{D_E}
\in L[[t]]^\times,\qquad
A_0:=\mathscr A_E(0)=\frac{26\lambda_8(0)}{D_E}\ne0.
\tag{15}
$$

$L$ 表示足以容納所選表示與 period 的有限 $11$-adic 係數域。$L[[t]]$ 中的 unit 僅要求常數項非零，不是在斷言所有係數都於 $\mathcal O_L$ 中可逆。

式 (14) 的 smoothing 規範、adjoint interpolation 與下節使用的比較，取自 [Loeffler–Rivero，§B2.3、式 (8)、Theorem C1.13](https://arxiv.org/html/2201.02078v2)。

## 5. 實際 Euler-system 比較與二次抽取

固定輔助族的權重座標 $X$，以及 crystalline quotient 的 period frame。令該 frame 相對於 meromorphic Eichler–Shimura 比較的函數為

$$
c_{\mathbf f}(X)=X^n(C+O(X)),\qquad n\ge0,\quad C\in L^\times.
\tag{16}
$$

權重纖維的 frame、Gauss sums、表示 transport、Kato period 與 Coleman 規範必須一同固定。本稿在橢圓曲線側使用式 (2) 的 $z^\dagger_\infty$；若以其他 period 執行計算，必須先換算兩側。$C$ 指完成這些相容選擇後的 leading 比較常數，不能無條件與另一套 frame 下的常數逐數字比較。

令 $\widehat{\mathcal B}_E(t)$ 為先按 $X^n$ 取 Eisenstein leading term、再投影至 $\psi=1$ 商分量、最後將 $\mathbf g$ 特殊化至 $E$ 的 Beilinson–Flach 類；保留其 logarithmic distribution 因子。以此記號，[Loeffler–Rivero，Proposition C1.12 與 Theorem C1.13](https://arxiv.org/html/2201.02078v2) 給出

$$
\boxed{
\widehat{\mathcal B}_E(t)
=C\,\mathscr A_E(t)\,
\frac{\log(1+t)}{\log_{11}(12)}
\,z^\dagger_\infty(t).
}
\tag{17}
$$

這裡引用的是其實際 family-level 定理；沒有把中心秩二 Selmer 群假設成零。文獻使用的是 Iwasawa 族上的 Greenberg 消失／regulator 注入性，不能把該結論直接搬到中心纖維。

### 命題 09.3：兩種消失階數與固定比例

在式 (2) 的已接受非零輸入及第 3 節的新非零計算下，

$$
\operatorname{ord}_t\widehat{\mathcal B}_E=2,\qquad
\operatorname{ord}_t\operatorname{Col}_E(\widehat{\mathcal B}_E)=3.
\tag{18}
$$

若

$$
B_2=[t^2]\widehat{\mathcal B}_E(t)
=\left.(\widehat{\mathcal B}_E/t^2)\right|_{t=0},
$$

則

$$
B_2=\frac{26C\lambda_8(0)}
{D_E\log_{11}(12)}\,\kappa^\dagger.
\tag{19}
$$

**證明。** $\mathscr A_E(t)$ 在 $t=0$ 可逆，而

$$
\log(1+t)=t-\frac12t^2+\cdots.
$$

將式 (2) 代入式 (17)，最低非零類係數是

$$
\frac{CA_0}{\log_{11}(12)}\,t^2\kappa^\dagger.
$$

此係數非零，給出第一個階數及式 (19)。再利用 Coleman 映射的係數線性及式 (2)，得到

$$
\operatorname{Col}_E(\widehat{\mathcal B}_E)
=\frac{CA_0}{\log_{11}(12)}\,a_2t^3+O(t^4),
$$

係數仍非零，給出第二個階數。證畢。

兩個類零點的來源不同：一個來自 Eisenstein 投影的 logarithmic distribution；另一個來自 $z^\dagger_\infty(0)=0$。regulator 的第三個零點來自式 (2) 的 Coleman 消失。這些不是在宣布複數 $L(E,s)$ 的消失階數變成 $3$。

式 (19) 反解即為本稿開頭的式 (1)。進一步，由式 (3)，對 $\ell(x)\ne0$ 的 $x$，

$$
\boxed{
s_{11}
=\frac{\log_{11}(12)D_E}{416C\lambda_8(0)}
\frac{h(x,B_2)}{\det(H)\ell(x)}.
}
\tag{20}
$$

其中 $416=16\cdot26$。此處 $h$、$H$、$\ell$ 的符號及尺度沿用 Attack 06。式 (20) 給出一個明確的新比較目標；沒有把未知的 $B_2$ 或 $C$ 代成已知數。

## 6. 如何攜帶 period，才不重犯尺度錯誤

Attack 08 顯示固定邊界不能排除封閉 cycle 的尺度歧義。本輪不能以「把 $C$ 設為 $1$」跳過相同問題。可完成的形式修正是：把 leading period 與 leading class 留在同一條線中。

### 引理 09.4：leading-line 商消除共同規範變換

令 $R$ 為局部一維光滑係數環，極大理想 $\mathfrak m=(X)$，殘餘域為 $L$。令 $\mathcal P$ 為可逆 $R$-模，$\pi\in\mathfrak m^n\mathcal P$ 具有恰為 $n$ 的消失階數，並令

$$
\mathcal Y\in
\mathfrak m^n\bigl(\mathcal P\otimes_R M\bigr),
$$

其中 $M$ 為自由模。兩個 leading term 位於同一條線

$$
\pi_n\in\mathcal P_0\otimes_L\mathfrak m^n/\mathfrak m^{n+1},
$$

$$
\mathcal Y_n\in
\left(\mathcal P_0\otimes_L\mathfrak m^n/\mathfrak m^{n+1}\right)
\otimes_L M_0.
$$

由 $\pi_n\ne0$，存在唯一 $v\in M_0$ 使

$$
\mathcal Y_n=\pi_n\otimes v.
\tag{21}
$$

$v$ 不依賴所用的局部 frame 或 uniformizer。

**證明。** 選 frame $e$，寫

$$
\pi=X^n(C+O(X))e,\qquad
\mathcal Y=X^n(B+O(X))e.
$$

則 $v=B/C$。若改成 $e'=u(X)e$，兩個座標同乘 $u(0)^{-1}$；若改成 $X'=v_0X+O(X^2)$，兩個 leading 座標同乘 $v_0^{-n}$。商不變，正好對應式 (21) 的內在描述。證畢。

這個引理說明應比較帶有 period-line 及 cotangent 冪的 leading 資料。它沒有證明這條線具有所需的有理 motivic 來源。應用到實際 Euler-system 構造時，還必須確認所採的 quotient identification 確實讓 period 與類使用同一條線；不能分別重新正規化後仍宣稱其商已被固定。

尤其，先前的 Kummer 單位 $\epsilon$ 可以提供一個明確、非零的 Eisenstein 擴張類；但本輪尚未建立它與式 (16) 的 meromorphic Eichler–Shimura leading period 的精確比較。

這個缺口在現有研究中也有清楚位置：[Polo–Rivero，Eisenstein degeneration of Beilinson–Kato classes and circular units，§2.3 與 Theorem 1.3 後的討論](https://arxiv.org/html/2501.01514v2) 將相關常數連到 canonical differential 的插值，未給出可直接代入本例的數值。該文另有假設；本稿沒有把其圓分單位比較直接當成無條件的 $C$ 計算。

### 兩個方向不可隨便合併

取 weight-leading term 後再取 cyclotomic-leading term，是式 (17) 指定的操作。直接令 $X=t$ 並不等價。最小代數例子是

$$
F(X,t)=X^n(t^2v+Xw).
$$

先除 $X^n$ 再令 $X=0$ 得 $t^2v$；沿對角線卻得到

$$
F(t,t)=t^{n+2}v+t^{n+1}w.
$$

新項可以先出現。這不是說實際 Beilinson–Flach 族一定有該項，而是說沒有額外可除性證明時，不能把兩種 leading 操作換成單一方向導數。

## 7. 本輪推進到哪裡，下一個數學目標是什麼

本輪已把 Attack 08 的「尋找 Kato 相容族」具體化為 $E_2(1,\chi_8)$ 的退化路徑，並完成先前未知的一個必要非零因子：

$$
\lambda_8(0)\ne0.
$$

因此式 (1) 的抽取不再需要猜測額外 twist 是否又多出零點。輔助族的存在與 family-level 比較使用已發表定理；本稿不是聲稱創造了該定理。

下一個尚待解決的核心比較是：將固定規範的 $C$、$B_2$ 及高度 pairing 合併成一個有理 determinant 元素，並識別其無窮遠 regulator。具體尚未完成者如下。

| 步驟 | 本輪狀態 |
|---|---|
| 輔助形式、decency、non-criticality | 具體選定並完成所需算術與書面論證 |
| 額外 twisted moment 非零 | 四十條新 cusp 路徑精確計算，得到 $5\bmod11$ |
| smoothing 及 adjoint 因子的非零性 | 已確定 |
| 二次類／三次 regulator 的 leading 比例 | 由已發表比較定理與新非零結果推導完成 |
| $n=\operatorname{ord}_Xc_{\mathbf f}$ | 存在性有理論保證，尚未算出 |
| $C$ 的數值及 rational period 比較 | 尚未完成 |
| $B_2$ 的實際 cohomology 座標 | 尚未完成 |
| 與 Attack 07 相對 cycle 的識別 | 尚未構造 |
| $s_{11}$ 與複數 $L''(E,1)/2$ 的比較 | 尚未完成 |

單純將式 (20) 的右端稱為「幾何尺度」不構成這個比較。需要的是同一個原始幾何／determinant 物件的兩種 realization，而非依已知 $11$-adic 等式反過來定義一個候選值。

## 8. 執行證據與本地端核查重點

**attack09_eisenstein.py** 使用 Python 3.9 以上的標準函式庫，讀取包內的 **INPUTS.json**。它不執行舊 eigenline producer、舊 Kurihara 和式或先前高度計算。

新程式完成：

1. 在接受的二維空間內求出新的負號線，先固定 normalization，再計算 twist。
2. 展開四十條導子 $88$ 的 cusp 路徑，建立十個 ordinary residue measures，積分 $x^{-1}$ 模 $11$。
3. 計算輔助 Eisenstein 的 Bernoulli 常數、refinement 係數與單位的精確局部 log。
4. 用有理數 sparse polynomial arithmetic 檢查式 (17) 的 leading 係數抽取，保留 $C,A_0,\kappa^\dagger,a_2$ 為形式未知量。

本次實際輸出為

$$
\lambda_8(0)\equiv5,\qquad
\log(\epsilon)/(11\sqrt2)\equiv5,\qquad
\mathscr S_5(0)=26.
$$

前兩個 $5$ 來自不同計算，並沒有被視為兩個完整 $11$-adic 數相等。

程式不證明 family-level Euler-system 定理，也沒有產生 $C$、$n$、$B_2$ 或 $s_{11}$ 的數值。這些在 JSON 中明確保留為 null／未完成。

本地端下一次可優先核查：負號 involution 與 $\{\infty,r\}$ 的方向、式 (10) 的 Gauss／period 規範、式 (11) 的 ordinary 測度，以及式 (8) 必須保留的 odd Teichmüller 分支。這些是本輪最可能影響比例與非零判斷的實際新節點。

**BSD 尚未證明；canonical frontier 不更新。本輪增加的是一個可用且額外因子不消失的 Euler-system 退化路徑，以及明確的二次 leading-term 抽取公式。**
