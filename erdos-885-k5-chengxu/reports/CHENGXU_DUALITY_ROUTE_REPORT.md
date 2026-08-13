# 澄序（MCDM Agent D）— ERDOS-885-K5 Duality Route

Date: 2026-08-13 (Asia/Taipei)

Scope: independent read-only research. Nothing in `D:\Ai\work together\MCDM`
was edited, committed, or sent to Agents A/B/C. All generated artifacts are in
this temporary directory.

## Status boundary

- **ERDOS-885 k=5 is not solved here.**
- Algebraic reductions and displayed finite packets are exact integer facts.
- Search exclusions below are exhaustive only inside their stated bounds and
  relative to the checked implementations; they are not global impossibility
  theorems.
- Literature novelty is not claimed. In particular, the main `K_{6,3}` packet
  independently rediscovered here is already present on Thomas Egense's public
  2019 `4 x 6` square-sumset page.

## 1. Dual/closure formulation

For positive roots `Y` and positive shifts `T`, define

```
Phi(Y) = { t > 0 : y^2 + t is a square for every y in Y }
Psi(T) = { y > 0 : y^2 + t is a square for every t in T }.
```

These are order-reversing and satisfy

```
T subset Phi(Y)  iff  Y subset Psi(T).
```

When either input has at least two elements, the opposite set is finite by the
difference-of-squares factorization. Thus packets can be completed to exact
two-sided concepts instead of being treated as arbitrary partial lists.

For a factor-difference packet with `m` common differences and `n` rows,
choosing the least difference `d0` gives the exact transpose

```
K_(m,n) -> K_(n+1,m-1),
M_j = d_j^2 - d0^2,
new differences = {2*d0} union {2*sqrt(d0^2 + 4*N_i)}.
```

Consequently ERDOS-885 `K_(5,5)` is equivalent to finding `K_(6,4)`, or in
normalized square-sum language six roots and four positive shifts (plus zero).

## 2. Exact public precursor rediscovered independently

The exhaustive ascending `(q,p)` search first finds, at `(p,q)=(2988,4356)`,

```
N = [4148640, 34418880, 300736800]
D = [2988, 4356, 5787, 11164, 17046, 23948].
```

The square-root matrix for `d^2 + 4N` is

```
[ 5052,  5964,  7077, 11884, 17526, 24292]
[12108, 12516, 13083, 16196, 20694, 26668]
[34812, 34956, 35163, 36436, 38646, 42148].
```

Independent direct divisor enumeration proves the full common intersection is
exactly `D`, not merely that these six values work.

The same data occur publicly in compact square-sum notation as

```
A = [2988, 5052, 12108, 34812]
B = [2988, 4356, 5787, 11164, 17046, 23948].
```

Transposition produces the five-row, four-difference near miss

```
N = [10046592, 24561225, 115706752, 281637972, 564578560]
D = [5976, 10104, 24216, 69624],
```

whose full common factor-difference intersection is exactly the displayed four
values. It is one difference short of `k=5`.

Search coverage establishes that no lexicographically earlier anchor exists:
there is no `K_(6,3)` with canonical second difference `q < 4356`, and no
further hit for `4357 <= q <= 6000`. The unscanned tail `p>2988` at the single
level `q=4356` means this does not assert uniqueness at that level.

## 3. Direct bounded target search

The Rust search exhausts every canonical anchor `0 <= p < q <= 6000`, every
compatible row in the pair fiber, and every four-row subset. Totals:

```
anchors                    18,003,000
eligible pair fibers       14,040,082
pair-fiber rows           209,917,507
retained differences          465,004
four-row support updates      767,726
K_(5,4) hits                         0
K_(6,4) hits                         0
```

The search includes `p=0`, uses no random sampling or per-fiber truncation, and
was rerun with unbounded-by-128 row-index groups after larger fibers exposed the
original engineering mask limit. A separate SymPy implementation matched all
Rust counts at `q <= 100`; direct packet checks use a third, divisor-enumeration
path.

Any `K_(5,5)` witness transposes to `K_(6,4)` with canonical second difference

```
q = 2*sqrt(d0^2 + 4*N_min).
```

Therefore this finite search implies only the bounded necessary condition

```
sqrt(d0^2 + 4*N_min) > 3000,
equivalently d0^2 + 4*N_min > 9,000,000.
```

## 4. Public `4 x 6` closure audit

The public page currently contains 71 compact primitive `4 x 6` packets. The
parser verified all square identities and recorded dataset digest

```
SHA256 4699a0379d41dc851722c0909cde6df59f293f3023142d112aaba78acdb3f57a
```

Exact results:

```
71 / 71  exact in the root -> positive-shift direction
71 / 71  exact in the positive-shift -> root direction
71 / 71  exact in signed factor-difference coordinates
426      five-root subsets checked after dropping one of six roots
4        largest signed shift-closure size among those subsets
```

Thus none of these primitive packets can be extended directly by a fifth
common factor difference, and none yields the adjacent `5 x 5` square-sum
problem merely by dropping one root and adding one shift. Signed enumeration
includes negative shifts, both parities of a new factor difference, and `d=0`.

### Scalar-induced closure jumps

Scaling a compact packet can create new divisor splittings, so it is not
discarded as a cosmetically equivalent operation. For every one of the 71
packets and every integer multiplier `1 <= c <= 1000`, the exact five-row
factor-difference packet was recomputed in signed coordinates:

```
packet-multiplier pairs       71,000
full divisors enumerated     847,896,082
signed closure entries           284,000
expected inherited entries       284,000 = 4 * 71,000
new fifth differences                  0
```

For the smallest core packet (the packet containing `2988,4356,...`), the same
complete signed test was extended through `c=10000`; all `40,000` closure
entries are exactly its four inherited differences.

Geometrically, for fixed six roots a new rational shift lies on the complete
intersection of five quadrics in `P^6`; when smooth this curve has genus 49.
The multiplier scan is therefore a bounded denominator/integral-dilation search
on a fixed high-genus curve. The next non-brute-force step is to exploit its
sign quotients and elliptic-cover tower, rather than increasing raw divisor
counts alone.

## 5. Other exact boundary checks

- The public same-parity sextuple
  `[744,912,1104,1808,2928,6932]` has pair spectrum
  `[24,366,536,744,1896]`, but its full five-row spectrum is only
  `[24,744,1896]`; it is structurally dead for the target.
- A separate exact `K_(4,4)` packet found in this route is
  `N=[472500,6448000,21285396,59440500]` with exact common differences
  `[120,1185,5160,15720]`. This is another instance at the already-known
  `k=4` level, not a new theorem.
- In Choudhry's seven-parameter `(5,3)` family, the positive parameter box
  `[1,6]^7` contains `279,936` tuples, `116,720` nondegenerate packets, and
  `10,777` distinct exact packets. Every packet has only its two inherited
  positive shifts; no right-side/positive-shift adjacent `5 x 5` candidate
  occurs in that box.

## 6. Reproduction

Principal commands (from this directory):

```powershell
.\search_dual_generic.exe --self-test
python .\verify_boundary_packets.py
python .\audit_public_4x6.py
python .\search_signed_scaled_public_4x6.py --scale-min 1 --scale-max 1000
python .\search_signed_scaled_public_4x6.py --scale-min 1001 --scale-max 10000 --packet-min 2 --packet-max 2
python .\search_choudhry_closure.py --bound 6
```

The all-packet multiplier run was split into disjoint packet ranges for wall
time only; the aggregate counts above use each packet-multiplier pair exactly
once.

Principal artifact hashes:

```
search_dual_k64.rs                 c16102ab05bd98a0b5c4768e4dbfb4b2b83741df1d3dee3340c5e2e5c3b9b379
search_dual_generic.exe            eaa867f5094013eed57a4a6fb3859a1003e51848a0b11a95f7ed5f5f45e929a7
verify_boundary_packets.py         fc06139c661042657d414c205c88b6a8f5fd3cc7b36b97328f1aa9a6adec340e
audit_public_4x6.py                f171b69f1ece22b6b879e0736ba55529cde8cf7710c7202897cd17f788061342
search_signed_scaled_public_4x6.py f98bffc79cb537586585bf845f86589789c8762e6c8edd0dcc099de46b26da2c
search_choudhry_closure.py         4e97bcac4dc2f7255b289e36401e10801fca34f38b1cccefbf442d4d7cdf2acb
```
