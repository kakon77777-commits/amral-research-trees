# 10｜Phase 1 Gate v0.3

Phase 1 的 `<150` regression現在分四層：

## A. Positive base fixture

現行 $12$ 條：

```text
must PASS
```

## B. Historical removed fixture

舊-only $13$ 條：

```text
must FAIL at the now-closed predicate map
```

不再允許只回傳 `not in final output`。

## C. Explicit discrepancy corpus

官方四條 discrepancy curves：

```text
must remain rejected for theorem-level reasons
```

## D. Algorithm2 semantic unit fixtures

即使 12 條 positive twist outputs完全沒變，仍要直接測：

- `TWIST_GCD_3N`
- `TWIST_DISC_VAL_GATE_REMOVED`

## 500K Gate

只有 A+B+C+D 全通過，才允許把 500K 結果標：

```text
REPRODUCTION-QUALIFIED
```

否則最多只能標：

```text
OUTPUT-MATCHED
```

這兩個標籤不可混用。
