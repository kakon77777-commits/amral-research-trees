# PARITY streaming invariant

After processing prefix `x[0:i]`, state `(i,b)` satisfies
`b = XOR(x[0], ..., x[i-1])`. The base case is `(0,0)`. Each step applies
`b' = b XOR x[i]`, so the invariant is locally checkable without answer access.
