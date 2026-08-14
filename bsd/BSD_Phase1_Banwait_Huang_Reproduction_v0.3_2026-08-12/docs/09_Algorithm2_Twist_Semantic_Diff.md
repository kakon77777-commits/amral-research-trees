# 09｜Algorithm 2 Twist Semantic Diff

## Code semantics changed

### 收緊

$$
\gcd(M,N)=1
\to
\gcd(M,3N)=1.
$$

當 $3\nmid N$ 時，任何 $3\mid M$ 的舊候選會在新 gate被剔除。

### 放寬

舊版額外要求一個 twist-side discriminant-valuation ramification-style condition。

現行版刪除了這個 predicate。

因此存在候選：

- 舊版被此 gate剔除；
- 新版不再因此被剔除。

## 但 small fixture 沒測到

對 12 條 surviving base curves，old/current `twists_of_ec_labels_150.json`：

$$
\boxed{
\text{exact match}.
}
$$

所以這份 fixture只能驗證「目前結果沒變」，不能驗證兩個新語義分支真的被 exercise。

## 解法

新增兩個 synthetic semantic cases。

### Case A

取：

$$
N=46,\qquad M=3.
$$

則：

$$
\gcd(3,46)=1,
$$

但：

$$
\gcd(3,138)=3.
$$

可直接區分 old/new coprimality gate。

### Case B

抽象設定：

$$
p=3,\quad q\in\{2,5\},
$$

且：

$$
v_2(\Delta)=3,\quad v_5(\Delta)=6.
$$

舊 `disc_valuation_condition` 對 $p=3$ 找不到 valuation非 3 倍數的 witness，因此 reject；現行程式已無此 gate。

這只是 predicate-level regression fixture，不宣稱對應實際 theorem-eligible twist。
