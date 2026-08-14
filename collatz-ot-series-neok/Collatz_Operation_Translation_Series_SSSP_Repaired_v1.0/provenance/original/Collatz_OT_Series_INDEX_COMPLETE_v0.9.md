# Collatz Operation Translation Series — COMPLETE

作者：Neo.K  
機構：一言諾科技有限公司（EveMissLab）  
狀態：**9/9 完成**  
封頂日期：2026-08-11

## 系列核心句

> Collatz dynamics is locally affine-trivializable, finitely certificate-compressible, but globally itinerary-unresolved.

中文：

> 考拉茲動力在有限合法判定域內可以被精確仿射化甚至局部平凡化；任意有限驗證域可以被壓縮成可機器檢查的證書覆蓋問題；但全域猜想仍要求排除所有由普通正整數錨定的無限未下降 itinerary。

## 九篇完成系列

1. **Paper 01 — 考拉茲猜想既有研究的重新分類與校正**
   - 完成 v0.1
2. **Paper 02 — Collatz Local Affine Atlas：有限奇偶字的精確仿射化**
   - 完成 v0.1
3. **Paper 03 — Parity Word、Residue Cylinder 與局部 Identity 化**
   - 完成 v0.1
4. **Paper 04 — 雙向殘餘類轉譯：2^k Cylinder 與 3^u Progression**
   - 完成 v0.1
5. **Paper 05 — 有限字收縮邊界與二項式 Cylinder Law**
   - 完成 v0.1
6. **Paper 06 — Valuation Language 與 Accelerated Collatz**
   - 完成 v0.1
7. **Paper 07 — 廣義 mx+r 系統與 Residue-Class Operation Translation**
   - 完成 v0.1
8. **Paper 08 — 代數判定域與結構斷裂定理**
   - 完成 v0.1
9. **Paper 09 — Finite Certificate Frontier：Collatz 有限精確覆蓋與全域鴻溝**
   - 完成 v0.1

## Paper 09 核心

Coefficient stopping time:

sigma(n) = inf { j>=1 : T^j(n)<n }

Hard prefix domain:

H_w = {n in Omega_w : T^j(n)>=n for all prefixes j}

Exact hard height:

H_w = Omega_w intersect [1,h(w)]

Finite hard frontier:

F_k(N) = {w length k : H_w intersect [2,N] nonempty}

Frontier extinction:

F_k(N)=empty iff sigma(n)<=k for all 2<=n<=N

Global quantifier form:

Collatz iff for every N there exists finite K(N) with F_{K(N)}(N)=empty

Integer-anchored obstruction:

Collatz iff there is no infinite hard branch whose canonical residues eventually stabilize to a fixed positive integer n>1.

## 系列封頂

本系列後續不再追加 Paper 10。

若繼續：
- hard frontier asymptotics
- formal verification
- certificate minimization
- generalized RCOT frontier

應另立新系列。
