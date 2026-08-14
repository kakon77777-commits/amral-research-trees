# 21｜Base BSD Anchor Repair

## v0.3 的問題

Banwait–Huang 的 historical review使用的是：

> Miller verified full BSD for **most** rank 0/1 curves below conductor 5000.

所以不能由：

$$
696<5000
$$

直接推出 Miller個人已驗證 `696.e1`。

## Correct source

Creutz–Miller, *Second Isogeny Descents and the BSD Conjectural Formula*,
Theorem 1.1：

$$
\boxed{
N<5000,\quad r_{\rm an}\le1
\Longrightarrow
\text{full BSD}.
}
$$

`696.e1`：

$$
N=696,\qquad r_{\rm an}=0.
$$

故 full BSD(E)成立，特別：

$$
\boxed{\operatorname{BSD}(E,2).}
$$

這是嚴格 source-level repair，不再依賴 analytic Sha冒充 actual Sha。
