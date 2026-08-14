# 08｜Period Compiler Logic

## Output vocabulary

```text
PERIOD_PASS_UNIFORM_FAMILY
PERIOD_PASS_THIS_CURVE
PERIOD_UNKNOWN
PERIOD_FAIL
```

`PERIOD_FAIL` 只有在 exact evidence證明 \(p\mid c_E\) 時才能使用。

## Decision tree

### Branch U — Edixhoven family-uniform

If:

```text
p >= 11
additive at p
twist locally trivial at p throughout family
optimality convention closed
NOT (potentially ordinary AND Kodaira in {II,III,IV})
```

then:

```text
PERIOD_PASS_UNIFORM_FAMILY
```

### Branch D — direct exact Manin

If exact \(c_A\) known:

```text
p ∤ c_A -> PERIOD_PASS_THIS_CURVE
p | c_A -> PERIOD_FAIL
```

### Branch M — CNS modular degree, p>=5

If:

```text
p >= 5
p ∤ modular_degree(A)
```

then:

```text
PERIOD_PASS_THIS_CURVE
```

### Branch M3 — CNS at p=3

If:

```text
p = 3
3 ∤ modular_degree(A)
AND (
  v_3(N_A) <= 2
  OR exists r | N_A with r ≡ 2 mod 3
  OR rational-singularity certificate
)
```

then:

```text
PERIOD_PASS_THIS_CURVE
```

Otherwise:

```text
PERIOD_UNKNOWN
```

## Mandatory warning

A per-twist modular-degree certificate does not close an infinite-family theorem.
